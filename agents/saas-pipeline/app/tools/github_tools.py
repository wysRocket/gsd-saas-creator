"""
github_tools.py — ADK tools for GitHub API interactions.

Covers: reading project board fields, creating repos, posting comments,
advancing board stage, monitoring GitHub Actions.
"""

from __future__ import annotations

import os
import time
from typing import Any

import httpx

_GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_GH_ORG = os.environ.get("GITHUB_ORG", "SaaS-Pretty-Projects")
_GH_API = "https://api.github.com"
_GH_GRAPHQL = "https://api.github.com/graphql"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_GH_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "User-Agent": "saas-pipeline-agent/1.0",
    }


def _graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    resp = httpx.post(
        _GH_GRAPHQL,
        headers=_headers(),
        json={"query": query, "variables": variables or {}},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data.get("data", {})


# ---------------------------------------------------------------------------
# Board reader
# ---------------------------------------------------------------------------

def get_board_item_fields(project_node_id: str, item_node_id: str) -> str:
    """Read all field values for a GitHub Projects v2 item.

    Args:
        project_node_id: The node_id of the Projects v2 project.
        item_node_id: The node_id of the specific item.

    Returns:
        JSON-formatted string of field name → value pairs.
    """
    import json

    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field { ... on ProjectV2Field { name } }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field { ... on ProjectV2SingleSelectField { name } }
                  }
                  ... on ProjectV2ItemFieldNumberValue {
                    number
                    field { ... on ProjectV2Field { name } }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(query, {"projectId": project_node_id})
    items = data.get("node", {}).get("items", {}).get("nodes", [])
    target = next((n for n in items if n.get("id") == item_node_id), None)
    if not target:
        return json.dumps({"error": f"Item {item_node_id} not found in project"})

    fields: dict[str, str] = {}
    for fv in target.get("fieldValues", {}).get("nodes", []):
        name = fv.get("field", {}).get("name", "")
        value = fv.get("text") or fv.get("name") or str(fv.get("number", ""))
        if name and value:
            fields[name] = value
    return json.dumps(fields, indent=2)


# ---------------------------------------------------------------------------
# Board stage advancement
# ---------------------------------------------------------------------------

def advance_board_stage(project_node_id: str, item_node_id: str, field_id: str, option_id: str) -> str:
    """Advance a GitHub Projects v2 item's Stage field to a new value.

    Args:
        project_node_id: The node_id of the project.
        item_node_id: The node_id of the item.
        field_id: The field ID of the Stage single-select field.
        option_id: The option ID of the target stage value (e.g. 'Deployed').

    Returns:
        Confirmation message.
    """
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $projectId
          itemId: $itemId
          fieldId: $fieldId
          value: { singleSelectOptionId: $optionId }
        }
      ) {
        projectV2Item { id }
      }
    }
    """
    _graphql(mutation, {
        "projectId": project_node_id,
        "itemId": item_node_id,
        "fieldId": field_id,
        "optionId": option_id,
    })
    return f"Board stage advanced. item={item_node_id}"


# ---------------------------------------------------------------------------
# GitHub Actions monitoring
# ---------------------------------------------------------------------------

def monitor_github_actions(owner: str, repo: str, workflow_run_id: int, timeout_minutes: int = 20) -> str:
    """Poll a GitHub Actions workflow run until it completes or times out.

    Args:
        owner: Repository owner (org or user).
        repo: Repository name.
        workflow_run_id: The ID of the workflow run to monitor.
        timeout_minutes: How long to wait before giving up.

    Returns:
        Final status: 'success', 'failure', 'cancelled', or 'timed_out'.
    """
    deadline = time.time() + timeout_minutes * 60
    url = f"{_GH_API}/repos/{owner}/{repo}/actions/runs/{workflow_run_id}"

    while time.time() < deadline:
        resp = httpx.get(url, headers=_headers(), timeout=15)
        if resp.status_code == 200:
            run = resp.json()
            status = run.get("status", "")
            conclusion = run.get("conclusion", "")
            if status == "completed":
                return f"Workflow run {workflow_run_id} completed: {conclusion}"
        time.sleep(30)

    return f"Timed out waiting for workflow run {workflow_run_id} after {timeout_minutes} minutes"


# ---------------------------------------------------------------------------
# Post board comment
# ---------------------------------------------------------------------------

def post_github_issue_comment(owner: str, repo: str, issue_number: int, body: str) -> str:
    """Post a comment to a GitHub issue or pull request.

    Args:
        owner: Repository owner.
        repo: Repository name.
        issue_number: Issue or PR number.
        body: Comment body (markdown supported).

    Returns:
        URL of the created comment.
    """
    url = f"{_GH_API}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    resp = httpx.post(url, headers=_headers(), json={"body": body}, timeout=15)
    resp.raise_for_status()
    return resp.json().get("html_url", "Comment posted")
