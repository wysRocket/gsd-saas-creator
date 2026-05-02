"""
agent.py — Root orchestrator for the SaaS creation pipeline.

Receives a pipeline payload from GitHub Actions (repository_dispatch)
and coordinates the 5-stage pipeline:
  @pm → @stitch → @engineer → @qa → @devops

Each stage is a sub-agent. The orchestrator routes the payload,
passes outputs between stages, and halts on any gate failure.
"""

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.pm_agent import pm_agent
from app.stitch_agent import stitch_agent
from app.engineer_agent import engineer_agent
from app.qa_agent import qa_agent
from app.devops_agent import devops_agent
from app.monitor_agent import monitor_agent

try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    pass  # ADC not available; GEMINI_API_KEY will be used instead

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

_INSTRUCTION = """
You are the SaaS Pipeline Orchestrator — you coordinate a 5-stage automated pipeline
that creates a complete SaaS application from a GitHub Projects board item description.

Pipeline stages (in order):
1. @pm — generates brief.md from the board item (project name, competitor URL, vertical)
2. @stitch — extracts design DNA from Stitch MCP (or uses fallback schema)
3. @engineer — generates design.md, stitch-prompt.md, ARCHITECTURE.md, and full codebase
4. @qa — validates all artifacts and runs npm tests
5. @devops — deploys to Firebase + advances board Stage to 'Deployed'

How to route:
- Parse the payload you receive. Expected fields:
    project_name, competitor_url, vertical, repo_name,
    stitch_project_id (optional), repo_dir (computed if not given)
- If repo_dir is not in the payload, compute it as:
    $PIPELINE_OUTPUT_DIR/<repo_name>
- Pass the relevant context to each sub-agent in turn.
- If any stage reports a failure or says "STOP" / "HALT", do not proceed to the next stage.
  Instead, report the failure summary and exit.

Halt gates:
- After @pm: brief.md must exist and pass validation.
- After @engineer: design.md and stitch-prompt.md must pass validation.
- After @qa: all stages must show PASS.
- Before @devops: explicit confirmation that QA passed.

Report a final summary:
  - Project name
  - Stages completed
  - Live URL (if deployed)
  - Any failures
"""

root_agent = Agent(
    name="saas_pipeline_orchestrator",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    sub_agents=[
        pm_agent,
        stitch_agent,
        engineer_agent,
        qa_agent,
        devops_agent,
        monitor_agent,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
