"""
agent_workflow.py — executable agent contracts for GSD SaaS Creator.

This script turns templates/agent-contracts.json into deterministic checks
that can run locally or inside the Design.md GitHub automation.

Usage:
    python scripts/agent_workflow.py status --repo-dir output/my-saas
    python scripts/agent_workflow.py route design_md
    python scripts/agent_workflow.py validate-stage design_md --repo-dir output/my-saas --log
    python scripts/agent_workflow.py record-stage design_md --repo-dir output/my-saas --status completed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTRACTS = ROOT / "templates" / "agent-contracts.json"
EVENT_LOG = "pipeline-events.jsonl"

PLACEHOLDER_PATTERNS = [
    re.compile(r"\[[^\]\n]*(Project Name|One paragraph|family|px|Page 2|Page 3|Component list|headline|layout|plan names|links|exact text|style description|list|competitor)[^\]\n]*\]", re.I),
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\b(TODO|TBD)\b", re.I),
]


class WorkflowError(Exception):
    """Raised when a contract check fails."""


def load_contracts(path: Path = DEFAULT_CONTRACTS) -> dict[str, Any]:
    if not path.exists():
        raise WorkflowError(f"agent contracts not found: {path}")
    return json.loads(path.read_text())


def repo_path(repo_dir: Path, pattern: str) -> Path:
    return repo_dir / pattern


def matches(repo_dir: Path, pattern: str) -> list[Path]:
    local_pattern = pattern
    if pattern.startswith("templates/"):
        local = repo_dir / pattern
        root = ROOT / pattern
        return [p for p in (local, root) if p.exists()]
    if any(ch in pattern for ch in "*?["):
        return sorted(repo_dir.glob(local_pattern))
    path = repo_path(repo_dir, local_pattern)
    return [path] if path.exists() else []


def read(repo_dir: Path, path: str) -> str:
    target = repo_path(repo_dir, path)
    return target.read_text() if target.exists() else ""


def write_event(repo_dir: Path, stage: str, status: str, message: str = "", details: dict[str, Any] | None = None) -> None:
    repo_dir.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "status": status,
        "message": message,
        "details": details or {},
    }
    with (repo_dir / EVENT_LOG).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def check_required_files(repo_dir: Path, stage_name: str, stage: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for group_name in ("required_inputs", "required_outputs"):
        for pattern in stage.get(group_name, []):
            if not matches(repo_dir, pattern):
                failures.append(f"{stage_name}: missing {group_name[:-1]} `{pattern}`")
    return failures


def has_placeholders(text: str) -> list[str]:
    found: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        found.extend(match.group(0) for match in pattern.finditer(text))
    return sorted(set(found))


def check_brief_present(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "brief.md").strip()
    if len(text) < 200:
        return ["brief.md is missing or too short to drive downstream generation"]
    return []


def check_design_md_present(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "design.md").strip()
    if len(text) < 600:
        return ["design.md is missing or too short to be a useful design contract"]
    return []


def check_stitch_prompt_present(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "stitch-prompt.md").strip()
    if len(text) < 600:
        return ["stitch-prompt.md is missing or too short for STITCH generation"]
    return []


def check_no_template_placeholders(repo_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in ("design.md", "stitch-prompt.md"):
        text = read(repo_dir, filename)
        if not text:
            continue
        placeholders = has_placeholders(text)
        if placeholders:
            sample = ", ".join(placeholders[:6])
            failures.append(f"{filename} still contains template placeholders: {sample}")
    return failures


def check_real_design_tokens(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "design.md")
    failures: list[str] = []
    hex_values = re.findall(r"#[0-9a-fA-F]{6}\b", text)
    if len(set(hex_values)) < 3:
        failures.append("design.md must include at least three concrete hex color tokens")
    if re.search(r"\*\*(Primary color|Secondary color|Background|Surface|Text primary|Accent):\*\*\s*#\s*$", text, re.M):
        failures.append("design.md still has empty color token placeholders")
    if not re.search(r"\*\*Font (heading|body):\*\*\s*[A-Za-z]", text):
        failures.append("design.md must include concrete font guidance")
    return failures


def check_designlang_reference_present(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "design.md")
    if "design-language.md" not in text and "designlang" not in text.lower():
        return ["design.md must reference the designlang source artifacts"]
    return []


def check_stitch_uses_design_md(repo_dir: Path) -> list[str]:
    text = read(repo_dir, "stitch-prompt.md").lower()
    if "design.md" not in text:
        return ["stitch-prompt.md must explicitly reference design.md as the design contract"]
    return []


def check_artifact_set_complete(repo_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in ("brief.md", "design.md", "stitch-prompt.md"):
        if not (repo_dir / filename).exists():
            failures.append(f"missing generated artifact `{filename}`")
    return failures


CHECKS = {
    "brief_present": check_brief_present,
    "design_md_present": check_design_md_present,
    "stitch_prompt_present": check_stitch_prompt_present,
    "no_template_placeholders": check_no_template_placeholders,
    "real_design_tokens": check_real_design_tokens,
    "designlang_reference_present": check_designlang_reference_present,
    "stitch_uses_design_md": check_stitch_uses_design_md,
    "artifact_set_complete": check_artifact_set_complete,
}


def validate_stage(repo_dir: Path, stage_name: str, contracts: dict[str, Any]) -> list[str]:
    stages = contracts.get("stages", {})
    if stage_name not in stages:
        known = ", ".join(sorted(stages))
        raise WorkflowError(f"unknown stage `{stage_name}`. Known stages: {known}")

    stage = stages[stage_name]
    failures = check_required_files(repo_dir, stage_name, stage)
    for check_name in stage.get("checks", []):
        check = CHECKS.get(check_name)
        if not check:
            failures.append(f"{stage_name}: unknown check `{check_name}`")
            continue
        failures.extend(check(repo_dir))
    return failures


def print_route(stage_name: str, contracts: dict[str, Any]) -> None:
    stage = contracts["stages"].get(stage_name)
    if not stage:
        known = ", ".join(sorted(contracts["stages"]))
        raise WorkflowError(f"unknown stage `{stage_name}`. Known stages: {known}")

    agent_name = stage["agent"]
    agent = contracts["agents"][agent_name]
    print(json.dumps({
        "stage": stage_name,
        "agent": agent_name,
        "role": agent["role"],
        "description": stage["description"],
        "required_inputs": stage.get("required_inputs", []),
        "required_outputs": stage.get("required_outputs", []),
        "checks": stage.get("checks", []),
        "next_stage": stage.get("next_stage"),
    }, indent=2))


def print_status(repo_dir: Path, contracts: dict[str, Any]) -> int:
    failed = False
    for stage_name in contracts["stages"]:
        failures = validate_stage(repo_dir, stage_name, contracts)
        status = "fail" if failures else "pass"
        if failures:
            failed = True
        print(f"{stage_name}: {status}")
        for failure in failures:
            print(f"  - {failure}")
    return 1 if failed else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and log GSD SaaS Creator agent workflow stages")
    parser.add_argument("--contracts", default=str(DEFAULT_CONTRACTS), help="Path to agent-contracts.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Validate all known stages")
    status_parser.add_argument("--repo-dir", default=".", help="Generated product repo directory")

    route_parser = subparsers.add_parser("route", help="Print the agent contract for one stage")
    route_parser.add_argument("stage", help="Stage name")

    validate_parser = subparsers.add_parser("validate-stage", help="Validate one stage")
    validate_parser.add_argument("stage", help="Stage name")
    validate_parser.add_argument("--repo-dir", default=".", help="Generated product repo directory")
    validate_parser.add_argument("--log", action="store_true", help="Append result to pipeline-events.jsonl")

    record_parser = subparsers.add_parser("record-stage", help="Append a pipeline event without validation")
    record_parser.add_argument("stage", help="Stage name")
    record_parser.add_argument("--repo-dir", default=".", help="Generated product repo directory")
    record_parser.add_argument("--status", required=True, choices=["started", "completed", "failed", "skipped"])
    record_parser.add_argument("--message", default="")

    args = parser.parse_args()
    contracts = load_contracts(Path(args.contracts))

    try:
        if args.command == "status":
            raise SystemExit(print_status(Path(args.repo_dir), contracts))
        if args.command == "route":
            print_route(args.stage, contracts)
            return
        if args.command == "validate-stage":
            repo_dir = Path(args.repo_dir)
            failures = validate_stage(repo_dir, args.stage, contracts)
            if failures:
                if args.log:
                    write_event(repo_dir, args.stage, "failed", "validation failed", {"failures": failures})
                for failure in failures:
                    print(f"FAIL: {failure}", file=sys.stderr)
                raise SystemExit(1)
            if args.log:
                write_event(repo_dir, args.stage, "completed", "validation passed")
            print(f"PASS: {args.stage}")
            return
        if args.command == "record-stage":
            write_event(Path(args.repo_dir), args.stage, args.status, args.message)
            print(f"RECORDED: {args.stage} {args.status}")
            return
    except WorkflowError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
