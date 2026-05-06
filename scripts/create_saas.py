"""
create_saas.py — Seed a new SaaS project onto the GitHub Project board
and trigger the pipeline automatically.

Usage:
    python scripts/create_saas.py \
        --name "ArcaneOps" \
        --competitor-url "https://kingdomofarcane.com" \
        --vertical "Gaming" \
        --repo-name "arcane-ops" \
        [--dry-run]

Environment:
    GH_TOKEN    — GitHub PAT (repo + project scopes)
    ORG         — GitHub org (default: SaaS-Pretty-Projects)
    PROJECT_ID  — GitHub Project node ID (default: PVT_kwDOEHzfoM4BU-0M)

What it does:
    1. Creates a draft issue in the org repo (title = project name)
    2. Adds it to the GitHub Project with all fields set
    3. Sets Stage = Brief, Competitor URL, Vertical, Repo URL
    4. Dispatches repository_dispatch to kick off orchestrate.py
"""

import argparse
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Board configuration (Active Projects board)
# ---------------------------------------------------------------------------

ORG = os.environ.get("ORG", "SaaS-Pretty-Projects")
PROJECT_ID = os.environ.get("PROJECT_ID", "PVT_kwDOEHzfoM4BU-0M")
TARGET_REPO = f"{ORG}/gsd-saas-creator"  # orchestrator repo

# Stage field and option IDs
STAGE_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQD56k"
STAGE_OPTION_IDS = {
    "brief":         "cddac2f5",
    "clarification": "0d90f5af",
    "design_md":     "67a099a3",
    "stitch_prompt": "e471f317",
    "designs_ready": "5339ae55",
    "ai_studio":     "cda08427",
    "in_progress":    "58cac058",
    "revisions":      "e7d47d45",
    "ready_for_prod":"5198760c",
    "launched":      "f01a3972",
    "operating":     "79fb3f03",
    "done":          "c15f4a82",
}

# Field IDs (TEXT fields)
REPO_URL_FIELD_ID      = "PVTF_lADOEHzfoM4BU-0MzhQhuOI"
COMPETITOR_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQv9f8"
AI_STUDIO_FIELD_ID     = "PVTF_lADOEHzfoM4BU-0MzhQtV7M"
NOTES_FIELD_ID         = "PVTF_lADOEHzfoM4BU-0MzhP_kGg"

# Vertical single-select field
VERTICAL_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQhuNE"
VERTICAL_OPTION_IDS = {
    "hosting":      "56a9c75a",
    "gaming":       "a263f297",
    "digital goods": "9bdacda3",
    "education":    "817d2a42",
    "career":       "79fc421b",
}

GRAPHQL_URL = "https://api.github.com/graphql"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _token():
    token = os.environ.get("GH_TOKEN", "").strip()
    if not token:
        token = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True
        ).stdout.strip()
    if not token:
        sys.exit("Error: GH_TOKEN not set and `gh auth token` failed.")
    return token


def _gh_graphql(query: str, variables: dict | None = None) -> dict:
    """Run a GraphQL query via gh CLI."""
    import json
    var_arg = ""
    if variables:
        var_arg = " ".join(f"-f {k}={v!r}" for k, v in variables.items())
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"] + (
            [f"variables={json.dumps(variables)}"] if variables else []
        ),
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data.get("data", {})


def _postgraphql(query: str, variables: dict | None = None) -> dict:
    """Run a GraphQL mutation via gh CLI."""
    import json
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    if variables:
        cmd.append("-f")
        cmd.append(f"variables={json.dumps(variables)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data.get("data", {})


# ---------------------------------------------------------------------------
# Step 1 — Create a draft issue in the gsd-saas-creator repo
# ---------------------------------------------------------------------------

def create_draft_issue(project_name: str, competitor_url: str, vertical: str) -> tuple[str, int]:
    """Create a draft issue in gsd-saas-creator. Returns (issue_node_id, issue_number)."""
    body = textwrap.dedent(f"""\
        ## SaaS Pipeline — New Project

        **Project:** {project_name}
        **Competitor:** {competitor_url}
        **Vertical:** {vertical}

        _This issue was auto-created by the SaaS Creator pipeline._
    """)

    query = """
        mutation CreateIssue($input: CreateIssueInput!) {
          createIssue(input: $input) {
            issue { id number }
          }
        }
    """
    variables = {
        "input": {
            "repositoryId": "",  # filled below
            "title": project_name,
            "body": body,
            "assignees": [],
        }
    }

    # First get the repo node ID
    repo_data = _gh_graphql(
        "query { repository(owner: $org, name: $name) { id } }",
        {"org": ORG, "name": "gsd-saas-creator"}
    )
    repo_id = repo_data["repository"]["id"]
    variables["input"]["repositoryId"] = repo_id

    data = _postgraphql(query, variables)
    issue = data["createIssue"]["issue"]
    print(f"  ✓ Draft issue #{issue['number']} created ({issue['id']})")
    return issue["id"], issue["number"]


# ---------------------------------------------------------------------------
# Step 2 — Add draft issue to the GitHub Project
# ---------------------------------------------------------------------------

def add_issue_to_project(issue_id: str) -> str:
    """Add an issue to the project. Returns the project item ID."""
    query = """
        mutation AddIssueToProject($input: AddProjectV2ItemByIdInput!) {
          addProjectV2ItemById(input: $input) {
            item { id }
          }
        }
    """
    variables = {"input": {"projectId": PROJECT_ID, "itemId": issue_id}}
    data = _postgraphql(query, variables)
    item_id = data["addProjectV2ItemById"]["item"]["id"]
    print(f"  ✓ Added to project (item_id={item_id})")
    return item_id


# ---------------------------------------------------------------------------
# Step 3 — Set project item fields
# ---------------------------------------------------------------------------

def set_text_field(item_id: str, field_id: str, value: str, token: str):
    """Set a text field on a project item."""
    import json
    query = """
        mutation SetTextField($input: UpdateProjectV2ItemFieldValueInput!) {
          updateProjectV2ItemFieldValue(input: $input) {
            projectV2Item { id }
          }
        }
    """
    variables = {
        "input": {
            "projectId": PROJECT_ID,
            "itemId": item_id,
            "fieldId": field_id,
            "value": {"text": value},
        }
    }
    _postgraphql(query, variables)
    print(f"  ✓ Set field {field_id} = {value[:60]}")


def set_single_select_field(item_id: str, field_id: str, option_id: str, token: str):
    """Set a single-select field on a project item."""
    import json
    query = """
        mutation SetSSField($input: UpdateProjectV2ItemFieldValueInput!) {
          updateProjectV2ItemFieldValue(input: $input) {
            projectV2Item { id }
          }
        }
    """
    variables = {
        "input": {
            "projectId": PROJECT_ID,
            "itemId": item_id,
            "fieldId": field_id,
            "value": {"singleSelectOptionId": option_id},
        }
    }
    _postgraphql(query, variables)
    print(f"  ✓ Set single-select {field_id} = {option_id}")


# ---------------------------------------------------------------------------
# Step 4 — Advance stage to "brief" (triggers orchestrate.py via webhook)
# ---------------------------------------------------------------------------

def advance_stage_to_brief(item_id: str, token: str):
    """Set Stage = Brief on the project item."""
    set_single_select_field(
        item_id, STAGE_FIELD_ID,
        STAGE_OPTION_IDS["brief"], token
    )
    print(f"  ✓ Stage set to Brief")


# ---------------------------------------------------------------------------
# Step 5 — Dispatch repository_dispatch to trigger orchestrate.py
# ---------------------------------------------------------------------------

def dispatch_pipeline(
    item_id: str,
    issue_number: int,
    repo_name: str,
    project_name: str,
    competitor_url: str,
    vertical: str,
):
    """Fire repository_dispatch on gsd-saas-creator to kick off orchestrate.py."""
    import json
    payload = {
        "event_type": "stage_changed",
        "client_payload": {
            "stage": "brief",
            "item_id": item_id,
            "issue_number": issue_number,
            "repo_name": repo_name,
            "project_name": project_name,
            "competitor_url": competitor_url,
            "vertical": vertical,
            "notes": "",
            "comment_body": "",
        },
    }
    cmd = [
        "gh", "api",
        f"repos/{ORG}/gsd-saas-creator/dispatches",
        "-F", f"event_type=stage_changed",
        "-F", f"client_payload={json.dumps(payload)}",
        "--input", "-",
    ]
    # Use --jq to suppress output, check return code
    result = subprocess.run(cmd, input=json.dumps(payload).encode(), capture_output=True)
    if result.returncode != 0 and "Nothing to see here" not in result.stderr:
        print(f"  [warning] dispatch may have failed: {result.stderr[:200]}")
    else:
        print(f"  ✓ Dispatched stage_changed → brief")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Create a new SaaS project on the board")
    parser.add_argument("--name", required=True, help="SaaS product name (used as issue title and project name)")
    parser.add_argument("--competitor-url", required=True, help="Competitor website URL")
    parser.add_argument("--vertical", required=True, help="Business vertical (e.g. Gaming, Education)")
    parser.add_argument("--repo-name", required=True, help="Kebab-case repo name (e.g. arcane-ops)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    args = parser.parse_args()

    token = _token()
    org_id = None

    if args.dry_run:
        print("[dry-run] No changes made.")
        print(f"  name:           {args.name}")
        print(f"  competitor-url:  {args.competitor_url}")
        print(f"  vertical:       {args.vertical}")
        print(f"  repo-name:      {args.repo_name}")
        print(f"  org:            {ORG}")
        print(f"  project_id:     {PROJECT_ID}")
        print(f"  stage:          brief ({STAGE_OPTION_IDS['brief']})")
        return

    print(f"\n=== Creating SaaS: {args.name} ===")
    print(f"  Org: {ORG}")
    print(f"  Project: {PROJECT_ID}")

    # Normalize vertical to lowercase key
    v_key = args.vertical.lower().strip()
    v_option = VERTICAL_OPTION_IDS.get(v_key)
    if not v_option:
        print(f"  [warning] Vertical '{args.vertical}' not in known options: {list(VERTICAL_OPTION_IDS.keys())}")
        v_option = VERTICAL_OPTION_IDS.get("hosting", "")

    repo_url = f"https://github.com/{ORG}/{args.repo_name}"

    # Step 1 — Create draft issue
    print("\n[1/5] Creating draft issue …")
    issue_node_id, issue_number = create_draft_issue(
        args.name, args.competitor_url, args.vertical
    )

    # Step 2 — Add to project
    print("\n[2/5] Adding to GitHub Project …")
    item_id = add_issue_to_project(issue_node_id)

    # Step 3 — Set fields
    print("\n[3/5] Setting project fields …")
    set_text_field(item_id, COMPETITOR_URL_FIELD_ID, args.competitor_url, token)
    if v_option:
        set_single_select_field(item_id, VERTICAL_FIELD_ID, v_option, token)
    set_text_field(item_id, REPO_URL_FIELD_ID, repo_url, token)

    # Step 4 — Set stage to Brief
    print("\n[4/5] Advancing stage to Brief …")
    advance_stage_to_brief(item_id, token)

    # Step 5 — Dispatch pipeline
    print("\n[5/5] Dispatching pipeline …")
    dispatch_pipeline(
        item_id=item_id,
        issue_number=issue_number,
        repo_name=args.repo_name,
        project_name=args.name,
        competitor_url=args.competitor_url,
        vertical=args.vertical,
    )

    print(f"\n✅ SaaS project '{args.name}' created and pipeline triggered!")
    print(f"   Issue:  https://github.com/{ORG}/gsd-saas-creator/issues/{issue_number}")
    print(f"   Board:  https://github.com/orgs/{ORG}/projects/{PROJECT_ID}")
    print(f"   Stage:   Brief — orchestrate.py is running …")


if __name__ == "__main__":
    main()
