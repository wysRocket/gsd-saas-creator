#!/usr/bin/env python3
"""
ruflo_board_poller.py — GitHub Projects board poller for Ruflo/Claude Code integration.

Polls the SaaS-Pretty-Projects board and emits JSON payloads for each actionable item.
Claude Code (with Ruflo) reads these payloads and dispatches the appropriate agent.

Usage:
  python scripts/ruflo_board_poller.py                    # one-shot: print actionable items
  python scripts/ruflo_board_poller.py --watch            # poll every 60s
  python scripts/ruflo_board_poller.py --stage Brief      # filter by stage
  python scripts/ruflo_board_poller.py --item "FreelancePay"  # single item
  python scripts/ruflo_board_poller.py --dispatch         # emit shell commands to run pipeline
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any

# ─── Constants ──────────────────────────────────────────────────────────────

PROJECT_ID = os.environ.get("PROJECT_ID", "PVT_kwDOEHzfoM4BU-0M")
ORG = os.environ.get("GITHUB_ORG", "SaaS-Pretty-Projects")
PIPELINE_OUTPUT_DIR = os.environ.get("PIPELINE_OUTPUT_DIR", "output")

STAGE_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQD56k"
VERTICAL_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQhuNE"
COMPETITOR_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQv9f8"
REPO_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQhuOI"
DEPLOY_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQv9gA"

# Stages that agents can act on automatically
ACTIONABLE_STAGES = {"Brief", "Design.md", "In Progress", "Ready for Prod", "Launched"}

# Stages that require a human to advance manually
HUMAN_GATE_STAGES = {"STITCH Prompt", "Designs Ready", "AI Studio", "Revisions"}

# ─── Board Query ─────────────────────────────────────────────────────────────

_BOARD_QUERY = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      title
      items(first: 50) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              url
              repository { name owner { login } }
            }
          }
          fieldValues(first: 15) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2Field { name id } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                optionId
                field { ... on ProjectV2SingleSelectField { name id } }
              }
            }
          }
        }
      }
    }
  }
}
"""


def _graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a GraphQL query via gh CLI."""
    cmd = ["gh", "api", "graphql", "--paginate", "-f", f"query={query}"]
    if variables:
        for k, v in variables.items():
            cmd += ["-f", f"{k}={v}"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(
            f"gh graphql failed (exit {result.returncode}):\n{result.stderr}"
        )
    return json.loads(result.stdout)


def fetch_board_items() -> list[dict[str, Any]]:
    """Fetch all items from the project board and normalize them."""
    data = _graphql(_BOARD_QUERY, {"projectId": PROJECT_ID})
    raw_items = (
        data.get("data", {})
        .get("node", {})
        .get("items", {})
        .get("nodes", [])
    )

    items = []
    for raw in raw_items:
        content = raw.get("content") or {}
        if not content.get("title"):
            continue  # draft item, skip

        fields: dict[str, str] = {}
        for fv in raw.get("fieldValues", {}).get("nodes", []):
            name = fv.get("field", {}).get("name", "")
            value = fv.get("text") or fv.get("name") or ""
            if name and value:
                fields[name] = value

        repo_info = content.get("repository") or {}
        item = {
            "item_node_id": raw["id"],
            "project_name": content["title"],
            "issue_number": content.get("number"),
            "issue_url": content.get("url"),
            "repo_name": repo_info.get("name", ""),
            "repo_owner": (repo_info.get("owner") or {}).get("login", ORG),
            "stage": fields.get("Stage", ""),
            "vertical": fields.get("Vertical", ""),
            "competitor_url": fields.get("Competitor URL", ""),
            "repo_url": fields.get("Repo URL", ""),
            "deploy_url": fields.get("Deploy URL", ""),
            "repo_dir": os.path.join(
                PIPELINE_OUTPUT_DIR,
                _slugify(content["title"]),
            ),
        }
        items.append(item)

    return items


def _slugify(name: str) -> str:
    """Convert a project name to a directory-safe slug."""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


# ─── Dispatch logic ──────────────────────────────────────────────────────────

def build_dispatch_command(item: dict[str, Any]) -> str | None:
    """Return the shell command to run the appropriate pipeline stage for this item."""
    stage = item["stage"]
    name = item["project_name"]
    repo_dir = item["repo_dir"]
    competitor = item["competitor_url"]
    vertical = item["vertical"]

    if stage == "Brief":
        return (
            f"python scripts/generate_brief.py "
            f"--name {_quote(name)} "
            f"--competitor-url {_quote(competitor)} "
            f"--vertical {_quote(vertical)} "
            f"--repo-dir {_quote(repo_dir)}"
        )
    elif stage == "Design.md":
        return (
            f"python scripts/generate_design_md.py --repo-dir {_quote(repo_dir)} && "
            f"python scripts/agent_workflow.py validate-stage design_md "
            f"--repo-dir {_quote(repo_dir)} --log"
        )
    elif stage == "In Progress":
        return f"PROJECT_NAME={_quote(name)} python scripts/scaffold.py {_quote(repo_dir)}"
    elif stage == "Ready for Prod":
        return f"python scripts/agent_workflow.py status --repo-dir {_quote(repo_dir)}"
    elif stage == "Launched":
        return f"python scripts/deploy.py"  # run from within repo_dir
    return None


def _quote(s: str) -> str:
    """Shell-quote a string."""
    import shlex
    return shlex.quote(s)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def print_items(items: list[dict], stage_filter: str | None, item_filter: str | None) -> None:
    """Print actionable items as JSON."""
    results = []
    for item in items:
        if stage_filter and item["stage"] != stage_filter:
            continue
        if item_filter and item_filter.lower() not in item["project_name"].lower():
            continue
        is_actionable = item["stage"] in ACTIONABLE_STAGES
        is_human_gate = item["stage"] in HUMAN_GATE_STAGES
        entry = {**item, "actionable": is_actionable, "human_gate": is_human_gate}
        results.append(entry)

    print(json.dumps(results, indent=2))


def print_dispatch(items: list[dict]) -> None:
    """Print shell commands to run each actionable item."""
    for item in items:
        if item["stage"] not in ACTIONABLE_STAGES:
            continue
        cmd = build_dispatch_command(item)
        if cmd:
            print(f"\n# {item['project_name']} (stage: {item['stage']})")
            print(f"# item_node_id: {item['item_node_id']}")
            print(cmd)


def print_summary(items: list[dict]) -> None:
    """Print a human-readable pipeline health summary."""
    from collections import Counter
    stages = Counter(item["stage"] for item in items if item["stage"])
    actionable = [i for i in items if i["stage"] in ACTIONABLE_STAGES]
    human_gates = [i for i in items if i["stage"] in HUMAN_GATE_STAGES]

    print("\n🟢 SaaS Pipeline Board — SaaS-Pretty-Projects/projects/1")
    print(f"   Total items: {len(items)}")
    print(f"   Actionable:  {len(actionable)} items ready for agents")
    print(f"   Human gates: {len(human_gates)} items waiting for human")
    print()
    print("📋 Stage breakdown:")
    for stage, count in sorted(stages.items()):
        marker = "🤖" if stage in ACTIONABLE_STAGES else "👤" if stage in HUMAN_GATE_STAGES else "  "
        print(f"   {marker} {stage:<20} {count}")
    print()
    if actionable:
        print("🚀 Actionable items:")
        for item in actionable:
            print(f"   [{item['stage']}] {item['project_name']}")
            if item["competitor_url"]:
                print(f"           competitor: {item['competitor_url']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Poll the SaaS GitHub Projects board and emit actionable items."
    )
    parser.add_argument("--watch", action="store_true", help="Poll every 60 seconds")
    parser.add_argument("--stage", help="Filter by stage name (e.g. Brief)")
    parser.add_argument("--item", help="Filter by project name substring")
    parser.add_argument("--dispatch", action="store_true", help="Emit shell dispatch commands")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (default: summary)")
    parser.add_argument("--interval", type=int, default=60, help="Watch interval in seconds")
    args = parser.parse_args()

    def run_once() -> None:
        try:
            items = fetch_board_items()
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return

        if args.dispatch:
            print_dispatch(items)
        elif args.json:
            print_items(items, args.stage, args.item)
        else:
            print_summary(items)
            if args.stage or args.item:
                filtered = [
                    i for i in items
                    if (not args.stage or i["stage"] == args.stage)
                    and (not args.item or args.item.lower() in i["project_name"].lower())
                ]
                print("\nFiltered items:")
                print(json.dumps(filtered, indent=2))

    if args.watch:
        print(f"Watching board every {args.interval}s (Ctrl+C to stop)...\n")
        while True:
            run_once()
            time.sleep(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
