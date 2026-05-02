"""
monitor_agent.py — Pipeline Monitor ambient agent.

Reads pipeline-events.jsonl across product repos, detects stuck pipelines,
and posts status updates to GitHub Projects board items.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.github_tools import post_github_issue_comment


def read_pipeline_events(repo_dir: str) -> str:
    """Read pipeline-events.jsonl for a product repo and return a status summary.

    Args:
        repo_dir: Path to the product repo directory.

    Returns:
        JSON summary of pipeline stage statuses and timestamps.
    """
    events_file = Path(repo_dir) / "pipeline-events.jsonl"
    if not events_file.exists():
        return json.dumps({"status": "no_events", "repo_dir": repo_dir})

    events: list[dict] = []
    for line in events_file.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    # Summarize: last status per stage
    stage_status: dict[str, dict] = {}
    for ev in events:
        stage = ev.get("stage", "")
        if stage:
            stage_status[stage] = {
                "status": ev.get("status"),
                "timestamp": ev.get("timestamp"),
                "message": ev.get("message", ""),
            }

    # Detect stuck pipeline: last event > 30 min ago and not completed
    stuck = False
    if events:
        last_ts = events[-1].get("timestamp", "")
        if last_ts:
            try:
                from datetime import datetime, timezone
                last_time = datetime.fromisoformat(last_ts)
                age_minutes = (datetime.now(timezone.utc) - last_time).total_seconds() / 60
                last_status = events[-1].get("status", "")
                if age_minutes > 30 and last_status not in ("completed", "failed"):
                    stuck = True
            except Exception:
                pass

    return json.dumps({
        "repo_dir": repo_dir,
        "total_events": len(events),
        "stages": stage_status,
        "stuck": stuck,
    }, indent=2)


_INSTRUCTION = """
You are the Pipeline Monitor — an ambient observability agent for the SaaS creation pipeline.

Your job when invoked:
1. Call read_pipeline_events with the repo_dir to get the current pipeline status.
2. Analyze the summary:
   - If all stages are 'completed': report success.
   - If any stage is 'failed': report which stage failed and the error message.
   - If 'stuck' is true: report that the pipeline is stuck and at which stage.
3. If owner/repo/issue_number are available and there is a failure or stuck state:
   call post_github_issue_comment with a clear status update.
4. Return a concise status report.

You are read-only — you do NOT modify pipeline artifacts or retry stages.
"""

monitor_agent = Agent(
    name="monitor_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[read_pipeline_events, post_github_issue_comment],
)
