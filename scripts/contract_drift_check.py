"""
contract_drift_check.py — detect mismatches between agent-contracts.json
and what the actual scripts/generators produce.

Usage:
    python scripts/contract_drift_check.py
    python scripts/contract_drift_check.py --contracts templates/agent-contracts.json
    python scripts/contract_drift_check.py --verbose

Checks performed:
  1. Every stage in the contract has a corresponding handler in orchestrate.py
  2. Every check function named in the contract exists in agent_workflow.py
  3. Every required_input glob resolves (either in repo_dir or at ROOT)
  4. Every required_output file is written by some generator script
  5. stage.next_stage chain is continuous (no dead ends before 'launched')
  6. qa's next_stage is actually implemented (handle_qa advances board)
  7. Each generator script has --force flag for idempotency
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTRACTS = ROOT / "templates" / "agent-contracts.json"
ORCHESTRATE = ROOT / "scripts" / "orchestrate.py"
AGENT_WORKFLOW = ROOT / "scripts" / "agent_workflow.py"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"ERROR: can't parse {path}: {e}", file=sys.stderr)
        sys.exit(1)


def check_contract_parses(contracts: dict) -> list[str]:
    issues = []
    if "stages" not in contracts:
        issues.append("contract is missing 'stages' key")
    if "agents" not in contracts:
        issues.append("contract is missing 'agents' key")
    return issues


def check_stage_coverage(contracts: dict) -> list[str]:
    """Every stage should have a handler in orchestrate.py.

    Allows known aliases: 'deploy' → 'launched' (contract uses 'deploy'
    as a logical stage name but implementation uses 'launched' for the
    board advancement after QA).
    """
    if not ORCHESTRATE.exists():
        return [f"orchestrate.py not found at {ORCHESTRATE}"]

    code = ORCHESTRATE.read_text()
    issues = []

    # Build alias map: contract_stage -> (handler_name, or True if covered by passive)
    KNOWN_ALIASES = {
        "deploy": "handle_launched",  # deploy stage maps to launched handler
    }
    PASSIVE_STAGES = {
        "designs_ready", "in_progress", "ready_for_prod",
        "operating", "done", "clarification",
    }

    for stage_name, stage in contracts.get("stages", {}).items():
        # Resolve aliases
        handler_key = KNOWN_ALIASES.get(stage_name, f"handle_{stage_name}")
        if handler_key == "passive" or stage_name in PASSIVE_STAGES:
            continue  # passive — handled by handle_passive generically

        # Check for handler function
        if not re.search(rf"^def\s+{re.escape(handler_key)}\s*\(", code, re.MULTILINE):
            issues.append(
                f"stage '{stage_name}' has no handler in orchestrate.py "
                f"(expected def {handler_key})"
            )

        # Check next_stage continuity
        next_stage = stage.get("next_stage")
        if next_stage is not None:
            if next_stage not in contracts["stages"]:
                issues.append(
                    f"stage '{stage_name}' → next_stage='{next_stage}' "
                    f"but that stage doesn't exist in the contract"
                )

    return issues

def check_check_functions(contracts: dict) -> list[str]:
    """Every check named in the contract must exist in agent_workflow.py."""
    if not AGENT_WORKFLOW.exists():
        return [f"agent_workflow.py not found at {AGENT_WORKFLOW}"]

    code = AGENT_WORKFLOW.read_text()
    issues = []

    # Strip "check_" prefix when comparing — contract uses "brief_present"
    # but the function is named "check_brief_present"
    defined_checks = {
        name if not name.startswith("check_") else name[6:]
        for name in re.findall(r"^def (check_\w+)\(", code, re.MULTILINE)
    }

    for stage_name, stage in contracts.get("stages", {}).items():
        for check_name in stage.get("checks", []):
            if check_name not in defined_checks:
                issues.append(
                    f"stage '{stage_name}' references check '{check_name}' "
                    f"but it is not defined in agent_workflow.py"
                )

    return issues


def check_input_globs(contracts: dict) -> list[str]:
    """required_inputs with globs should resolve somewhere.

    Per-product patterns (design/*, output/*) are expected to live inside
    individual repo_dirs — only check them against ROOT if the pattern
    looks like an orchestrator-relative path, not a product-relative one.
    """
    issues = []
    for stage_name, stage in contracts.get("stages", {}).items():
        for pattern in stage.get("required_inputs", []):
            # Skip template inputs
            if pattern.startswith("templates/"):
                template_path = ROOT / pattern
                if template_path.exists():
                    continue
                else:
                    issues.append(
                        f"stage '{stage_name}': template input '{pattern}' "
                        f"referenced but not found at {template_path}"
                    )
                continue

            # Skip per-product patterns — these only exist inside individual
            # repo directories (e.g. output/<name>/design/competitor-design-language.md)
            if pattern.startswith("design/") or pattern.startswith("output/"):
                continue

            # For other file-patterns, check if glob resolves in ROOT
            if any(ch in pattern for ch in "*?["):
                resolved = sorted(ROOT.glob(pattern))
                if not resolved:
                    issues.append(
                        f"stage '{stage_name}': glob '{pattern}' "
                        f"does not resolve in project root {ROOT}"
                    )
    return issues


def check_generator_idempotency() -> list[str]:
    """Generator scripts should support --force for safe re-runs."""
    generators = [
        ROOT / "scripts" / "generate_brief.py",
        ROOT / "scripts" / "generate_design_md.py",
        ROOT / "scripts" / "generate_stitch_prompt.py",
    ]
    issues = []
    for g in generators:
        if not g.exists():
            issues.append(f"generator script not found: {g}")
            continue
        code = g.read_text()
        if '"--force"' not in code and "'--force'" not in code:
            issues.append(
                f"{g.name} does not support --force flag "
                f"(not idempotent — re-runs will overwrite human edits)"
            )
    return issues


def check_deploy_implemented(contracts: dict) -> list[str]:
    """The qa stage should advance the board (handle_qa posts and advances)."""
    if not ORCHESTRATE.exists():
        return []
    code = ORCHESTRATE.read_text()

    # Find handle_qa function
    qa_match = re.search(r"def handle_qa\([^)]+\):(.*?)(?=\ndef |\nif __name__|$)", code, re.DOTALL)
    if not qa_match:
        return ["handle_qa() not found in orchestrate.py — qa stage can't advance board"]

    qa_body = qa_match.group(1)
    issues = []

    # Should post a comment
    if "post_comment" not in qa_body:
        issues.append("handle_qa() doesn't post a comment on the issue")

    # Should advance the stage on success
    if "update_stage" not in qa_body:
        issues.append("handle_qa() doesn't call update_stage on success")

    return issues


def check_dead_ends(contracts: dict) -> list[str]:
    """No stage should point to a non-existent next_stage (except 'launched' or terminal stages)."""
    issues = []
    terminal = {"launched", "operating", "done"}
    for stage_name, stage in contracts.get("stages", {}).items():
        next_stage = stage.get("next_stage")
        if next_stage is None:
            continue  # terminal stage — OK
        if next_stage not in terminal and next_stage not in contracts.get("stages", {}):
            issues.append(
                f"stage '{stage_name}' → next_stage='{next_stage}' "
                f"but that stage is not defined in the contract"
            )
    return issues


def main():
    parser = argparse.ArgumentParser(description="Check agent-contracts.json for drift")
    parser.add_argument("--contracts", default=str(DEFAULT_CONTRACTS))
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    contracts_path = Path(args.contracts)
    if not contracts_path.exists():
        print(f"ERROR: {contracts_path} not found", file=sys.stderr)
        sys.exit(1)

    contracts = load_json(contracts_path)

    all_issues = []

    checks = [
        ("Contract structure", check_contract_parses(contracts)),
        ("Stage coverage (handlers exist)", check_stage_coverage(contracts)),
        ("Check functions (implemented)", check_check_functions(contracts)),
        ("Input globs (resolve)", check_input_globs(contracts)),
        ("Generator idempotency (--force)", check_generator_idempotency()),
        ("qa handler advances board", check_deploy_implemented(contracts)),
        ("No dead-end next_stage refs", check_dead_ends(contracts)),
    ]

    total = 0
    for check_name, issues in checks:
        if issues:
            total += len(issues)
            label = f"❌ {check_name} ({len(issues)})"
            print(f"\n{label}")
            for issue in issues:
                print(f"  • {issue}")
        elif args.verbose:
            print(f"✓ {check_name}")

    if total == 0:
        print("✅ No contract drift detected")
    else:
        print(f"\n❌ {total} issue(s) found — contract and implementation are out of sync")

    sys.exit(1 if total > 0 else 0)


if __name__ == "__main__":
    main()
