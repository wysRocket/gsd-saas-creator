"""
board_status.py — Inspect the Active Projects board and report pipeline state.

Usage:
    python scripts/board_status.py
    python scripts/board_status.py --stage "Brief"
    python scripts/board_status.py --repo "terrastone"
    python scripts/board_status.py --watch
    python scripts/board_status.py --stuck

Environment:
    GH_TOKEN     — GitHub PAT (defaults to `gh auth token`)
    ORG          — GitHub org (default: SaaS-Pretty-Projects)
    PROJECT_ID   — Project node ID (default: PVT_kwDOEHzfoM4BU-0M)
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ORG = "SaaS-Pretty-Projects"
PROJECT_ID = "PVT_kwDOEHzfoM4BU-0M"

GRAPHQL_QUERY = """
query {
  node(id: "%s") {
    ... on ProjectV2 {
      title
      items(first: 100) {
        nodes {
          id
          type
          content {
            ... on Issue {
              title
              number
              state
              url
              repository { name }
            }
            ... on PullRequest {
              title
              number
              state
              url
              repository { name }
            }
            ... on DraftIssue {
              title
            }
          }
          fieldValues(first: 30) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { id name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { id name } }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2FieldCommon { id name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2FieldCommon { id name } }
              }
            }
          }
        }
      }
    }
  }
}
""" % PROJECT_ID

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _token():
    token = subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True
    ).stdout.strip()
    return token


def _gh_graphql(query: str) -> dict:
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        capture_output=True, text=True
    )
    import json
    data = json.loads(result.stdout)
    if "errors" in data:
        print(json.dumps(data["errors"], indent=2), file=sys.stderr)
    return data.get("data", {})


def _flatten_fields(field_values: list) -> dict:
    """Return {field_name: value} for all filled fields."""
    flat = {}
    for fv in field_values:
        fname = fv.get("field", {}).get("name", "?")
        val = (
            fv.get("text")
            or fv.get("name")
            or str(fv.get("number", ""))
            or fv.get("date", "")
        )
        if fname and val:
            flat[fname] = val
    return flat


# ---------------------------------------------------------------------------
# Stage ordering (reflects pipeline sequence)
# ---------------------------------------------------------------------------

STAGE_ORDER = [
    "brief",
    "clarification",
    "design_md",
    "stitch_prompt",
    "designs_ready",
    "ai_studio",
    "in_progress",
    "revisions",
    "ready_for_prod",
    "launched",
    "operating",
    "done",
]

# Stages that should auto-advance (not waiting on human)
AUTO_STAGES = {"brief", "design_md", "qa"}
# Stages that are human-gate stops
HUMAN_GATE_STAGES = {"stitch_prompt", "designs_ready", "ai_studio", "in_progress", "revisions"}
# Stages that signal done-ness
DONE_STAGES = {"launched", "operating", "done"}


def classify(flat: dict) -> str:
    """Classify an item's state."""
    stage = flat.get("Stage", "").lower().replace(" ", "_").replace(".", "")
    # Normalize display names to keys
    mapping = {
        "brief": "brief",
        "clarification": "clarification",
        "design_md": "design_md",
        "stitch_prompt": "stitch_prompt",
        "designs_ready": "designs_ready",
        "ai_studio": "ai_studio",
        "in_progress": "in_progress",
        "revisions": "revisions",
        "ready_for_prod": "ready_for_prod",
        "launched": "launched",
        "operating": "operating",
        "done": "done",
    }
    return mapping.get(stage, stage)


# ---------------------------------------------------------------------------
# Fetch & parse
# ---------------------------------------------------------------------------

def fetch_board() -> list[dict]:
    data = _gh_graphql(GRAPHQL_QUERY)
    node = data.get("node", {})
    project_title = node.get("title", "unknown")
    items = node.get("items", {}).get("nodes", [])

    parsed = []
    for item in items:
        content = item.get("content") or {}
        flat = _flatten_fields(item.get("fieldValues", {}).get("nodes", []))
        stage_key = classify(flat)

        parsed.append({
            "item_id": item["id"],
            "type": item.get("type", "DRAFT_ISSUE"),
            "title": content.get("title", "(untitled draft)"),
            "issue_number": content.get("number"),
            "issue_url": content.get("url"),
            "repo": content.get("repository", {}).get("name", ""),
            "stage": flat.get("Stage", ""),
            "stage_key": stage_key,
            "competitor_url": flat.get("Competitor URL", ""),
            "vertical": flat.get("Vertical", ""),
            "repo_url": flat.get("Repo URL", ""),
            "ai_studio": flat.get("AI Studio", ""),
            "deploy_url": flat.get("Deploy URL", ""),
            "priority": flat.get("Priority", ""),
            "notes": flat.get("Notes", ""),
            "all_fields": flat,
        })
    return parsed


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def fmt_table(items: list[dict], stage_order: bool = False):
    """Print items as a compact table."""
    print(f"{'#':<5} {'Stage':<18} {'Title':<45} {'Repo':<20} {'URL'}")
    print("-" * 120)
    for item in items:
        title = (item["title"] or "(draft)")[:43]
        stage = item["stage"] or "(no stage)"
        repo = item["repo"] or "-"
        url = item.get("issue_url", item.get("repo_url", "")) or "-"
        num = f"#{item['issue_number']}" if item["issue_number"] else ""
        print(f"{num:<5} {stage:<18} {title:<45} {repo:<20} {url}")


def fmt_board_summary(items: list[dict]):
    """Print a one-line-per-item board summary."""
    print(f"\n{'='*100}")
    print(f"  Active Projects Board — {len(items)} items")
    print(f"{'='*100}")
    for item in items:
        title = (item["title"] or "(draft)")[:50]
        num = f"#{item['issue_number']}" if item["issue_number"] else "  "
        stage = item["stage"] or "(blank)"
        repo = item["repo"] or "-"
        url = item.get("repo_url", "")
        deploy = item.get("deploy_url", "")
        print(f"  {num:<4} | {stage:<18} | {title:<50} | {repo:<20} | {url or deploy or '-'}")


def fmt_stuck(items: list[dict], verbose: bool = False):
    """Identify items stuck at human-gate stages."""
    stuck = [
        i for i in items
        if i["stage_key"] in HUMAN_GATE_STAGES
        and i["stage_key"] not in {"ai_studio", "in_progress"}  # these can be long
    ]
    needs_attention = [
        i for i in items
        if i["stage_key"] in {"clarification", "revisions"}
    ]
    # Merge, keeping first occurrence (dedup by item_id)
    seen: set = set()
    merged = []
    for i in stuck + needs_attention:
        if i["item_id"] not in seen:
            seen.add(i["item_id"])
            merged.append(i)

    if not verbose:
        print(
            f"\n--- Stuck / Needs Attention "
            f"({len(stuck)} stuck, {len(needs_attention)} need review, {len(merged)} unique) ---"
        )
        for i in merged:
            num = f"#{i['issue_number']}" if i["issue_number"] else "  "
            gate = "🔒" if i["stage_key"] in HUMAN_GATE_STAGES else "⚠️ "
            print(f"  {gate} {num:<4} | {i['stage']:<18} | {i['title']:<50} | {i['repo'] or '-'}")
        return

    # Verbose: show all fields for stuck items
    for i in stuck + needs_attention:
        print(f"\n{'='*80}")
        num = f"#{i['issue_number']}" if i["issue_number"] else "(draft)"
        print(f"  [{num}] {i['title']}")
        print(f"  Stage:   {i['stage']}")
        print(f"  Repo:    {i['repo'] or '-'}")
        print(f"  Comp:    {i['competitor_url'] or '-'}")
        print(f"  Vertical:{i['vertical'] or '-'}")
        print(f"  Notes:   {i['notes'] or '-'}")
        print(f"  Fields:  {', '.join(f'{k}={v}' for k, v in i['all_fields'].items() if v)}")


def fmt_by_stage(items: list[dict]):
    """Print items grouped by stage."""
    by_stage: dict[str, list] = {}
    for i in items:
        s = i["stage_key"] or "none"
        by_stage.setdefault(s, []).append(i)

    for stage_key in STAGE_ORDER:
        stage_items = by_stage.get(stage_key, [])
        display_name = stage_items[0]["stage"] if stage_items else stage_key
        marker = " ← AUTO" if stage_key in AUTO_STAGES else " ← HUMAN-GATE" if stage_key in HUMAN_GATE_STAGES else ""
        print(f"\n[{len(stage_items)}] {display_name} ({stage_key}){marker}")
        for i in stage_items:
            num = f"#{i['issue_number']}" if i["issue_number"] else "  "
            print(f"      {num:<4} | {i['title'][:60]} | {i['repo'] or '-'}")


# ---------------------------------------------------------------------------
# Watch mode
# ---------------------------------------------------------------------------

def watch_board(interval: int = 60):
    print(f"Watching board every {interval}s. Ctrl+C to stop.\n")
    import time
    seen_ids = set()
    first = True
    while True:
        try:
            items = fetch_board()
            current_ids = {i["item_id"] for i in items}
            new_ids = current_ids - seen_ids

            if first:
                fmt_board_summary(items)
                seen_ids = current_ids
                first = False
            else:
                # Report changes
                prev = {i["item_id"]: i for i in [
                    dict(item_id="__placeholder")] * 0}  # will re-fetch
                # Just show current state in watch mode
                fmt_board_summary(items)
                if new_ids:
                    print(f"\n  [NEW] {len(new_ids)} new item(s) appeared")

            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopped.")
            break


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Inspect Active Projects board state")
    parser.add_argument("--stage", metavar="NAME", help="Filter by stage name (partial match)")
    parser.add_argument("--repo", metavar="NAME", help="Filter by repository name (partial match)")
    parser.add_argument("--stuck", action="store_true", help="Show items at human-gate stages")
    parser.add_argument("--by-stage", action="store_true", help="Group by stage")
    parser.add_argument("--watch", action="store_true", help="Poll every 60s")
    parser.add_argument("--watch-interval", type=int, default=60, help="Watch poll interval (default: 60s)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show full field details for stuck items")
    args = parser.parse_args()

    if args.watch:
        watch_board(args.watch_interval)
        return

    items = fetch_board()

    # Filters
    if args.stage:
        pat = args.stage.lower()
        items = [i for i in items if pat in (i["stage"] or "").lower() or pat in i["stage_key"]]
    if args.repo:
        pat = args.repo.lower()
        items = [i for i in items if pat in (i["repo"] or "").lower()]

    if args.stuck:
        fmt_stuck(items, verbose=args.verbose)
    elif args.by_stage:
        fmt_by_stage(items)
    else:
        fmt_board_summary(items)
        print(f"\nTotal: {len(items)} items")
        # Quick count by stage
        by_stage: dict[str, int] = {}
        for i in items:
            s = i["stage"] or "(none)"
            by_stage[s] = by_stage.get(s, 0) + 1
        print("\nBy stage:")
        for k in sorted(by_stage, key=lambda s: STAGE_ORDER.index(s) if s in STAGE_ORDER else 99):
            print(f"  {k:<20} {by_stage[k]}")


if __name__ == "__main__":
    main()
