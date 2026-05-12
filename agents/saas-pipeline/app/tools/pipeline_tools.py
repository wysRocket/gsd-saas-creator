"""
pipeline_tools.py — ADK tool wrappers for gsd-saas-creator scripts.

Each function is an ADK-compatible tool that wraps a script in scripts/.
All tools return a string result (success message or error).

HITL tools (request_brief_review, request_deployment_approval,
request_qa_review) delegate high-stakes decisions to the hitl-approver
service. The service auto-resolves routine cases and pauses for human input
on critical ones, returning a JSON result the pipeline agents can act on.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Root of the gsd-saas-creator repo (two levels up from agents/saas-pipeline/)
_REPO_ROOT = Path(os.environ.get("PIPELINE_REPO_ROOT", str(Path(__file__).parent.parent.parent.parent)))
_SCRIPTS = _REPO_ROOT / "scripts"
_OUTPUT = Path(os.environ.get("PIPELINE_OUTPUT_DIR", str(_REPO_ROOT / "output")))


def _run_script(args: list[str], cwd: Path | None = None) -> str:
    """Run a Python script via uv and return stdout or raise on failure."""
    cmd = [sys.executable, "-m", "uv", "run", "python"] + args
    # Fallback: run directly with current python if uv not available
    try:
        result = subprocess.run(
            ["uv", "run", "python"] + args,
            capture_output=True,
            text=True,
            cwd=str(cwd or _REPO_ROOT),
            timeout=300,
        )
    except FileNotFoundError:
        result = subprocess.run(
            [sys.executable] + args,
            capture_output=True,
            text=True,
            cwd=str(cwd or _REPO_ROOT),
            timeout=300,
        )
    if result.returncode != 0:
        raise RuntimeError(
            f"Script failed (exit {result.returncode}):\n"
            f"STDOUT: {result.stdout[-2000:]}\n"
            f"STDERR: {result.stderr[-2000:]}"
        )
    return result.stdout


# ---------------------------------------------------------------------------
# @pm tools
# ---------------------------------------------------------------------------

def generate_brief(
    project_name: str,
    competitor_url: str,
    vertical: str,
    repo_dir: str,
) -> str:
    """Generate brief.md for a SaaS product using Gemini + designlang competitor analysis.

    Args:
        project_name: Name of the SaaS product.
        competitor_url: URL of a competitor site to extract design language from.
        vertical: Business vertical (e.g. Gaming, eCommerce, SaaS).
        repo_dir: Absolute or relative path to the product repo directory.

    Returns:
        Success message with the path to the generated brief.md.
    """
    out = _run_script([
        str(_SCRIPTS / "generate_brief.py"),
        "--name", project_name,
        "--competitor-url", competitor_url,
        "--vertical", vertical,
        "--repo-dir", repo_dir,
    ])
    return f"brief.md generated.\n{out}"


def validate_stage(stage: str, repo_dir: str) -> str:
    """Validate a pipeline stage using agent_workflow.py.

    Args:
        stage: Stage name — one of: brief, design_md, stitch_prompt, qa, deploy.
        repo_dir: Path to the product repo directory.

    Returns:
        'PASS: <stage>' on success, raises RuntimeError on failure.
    """
    out = _run_script([
        str(_SCRIPTS / "agent_workflow.py"),
        "validate-stage", stage,
        "--repo-dir", repo_dir,
        "--log",
    ])
    return out.strip()


def validate_all_stages(repo_dir: str) -> str:
    """Run validation checks across all pipeline stages.

    Args:
        repo_dir: Path to the product repo directory.

    Returns:
        Multi-line status report for all stages.
    """
    try:
        out = _run_script([
            str(_SCRIPTS / "agent_workflow.py"),
            "status",
            "--repo-dir", repo_dir,
        ])
        return out.strip()
    except RuntimeError as e:
        # status exits 1 if any stage fails — return the output anyway
        return str(e)


# ---------------------------------------------------------------------------
# @stitch tools
# ---------------------------------------------------------------------------

def extract_stitch_dna(project_id: str, output_path: str) -> str:
    """Extract design DNA from a Stitch project via MCP.

    Args:
        project_id: The Stitch project ID (e.g. 'abc123').
        output_path: Where to write design_tokens.json.

    Returns:
        Summary of extracted tokens (colors, screens, fonts).
    """
    out = _run_script([
        str(_SCRIPTS / "extract_dna.py"),
        project_id,
        output_path,
    ])
    return f"Design DNA extracted.\n{out}"


# ---------------------------------------------------------------------------
# @engineer tools
# ---------------------------------------------------------------------------

def generate_design_md(repo_dir: str) -> str:
    """Generate design.md from brief.md + design tokens.

    Args:
        repo_dir: Path to the product repo directory (must contain brief.md).

    Returns:
        Success message with character count of design.md.
    """
    out = _run_script([
        str(_SCRIPTS / "generate_design_md.py"),
        "--repo-dir", repo_dir,
    ])
    return f"design.md generated.\n{out}"


def generate_stitch_prompt(repo_dir: str) -> str:
    """Generate stitch-prompt.md from brief.md + design.md.

    Args:
        repo_dir: Path to the product repo directory.

    Returns:
        Success message with character count of stitch-prompt.md.
    """
    out = _run_script([
        str(_SCRIPTS / "generate_stitch_prompt.py"),
        "--repo-dir", repo_dir,
    ])
    return f"stitch-prompt.md generated.\n{out}"


def scaffold_project(project_name: str, repo_dir: str, design_tokens_path: str = "") -> str:
    """Generate the full Next.js + Firebase project scaffold.

    Args:
        project_name: Name of the SaaS product.
        repo_dir: Output directory for the generated project.
        design_tokens_path: Optional path to design_tokens.json for theming.

    Returns:
        Success message listing generated files.
    """
    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    if design_tokens_path:
        env["DESIGN_TOKENS"] = design_tokens_path

    try:
        result = subprocess.run(
            ["uv", "run", "python", str(_SCRIPTS / "scaffold.py"), repo_dir],
            capture_output=True,
            text=True,
            cwd=str(_REPO_ROOT),
            env=env,
            timeout=120,
        )
    except FileNotFoundError:
        result = subprocess.run(
            [sys.executable, str(_SCRIPTS / "scaffold.py"), repo_dir],
            capture_output=True,
            text=True,
            cwd=str(_REPO_ROOT),
            env=env,
            timeout=120,
        )
    if result.returncode != 0:
        raise RuntimeError(f"scaffold.py failed:\n{result.stderr[-2000:]}")
    return f"Project scaffolded at {repo_dir}.\n{result.stdout}"


# ---------------------------------------------------------------------------
# @qa tools
# ---------------------------------------------------------------------------

def run_npm_tests(repo_dir: str) -> str:
    """Run npm install + npm test in the generated project directory.

    Args:
        repo_dir: Path to the generated Next.js project directory.

    Returns:
        Test results summary.
    """
    result = subprocess.run(
        ["npm", "install", "--silent"],
        capture_output=True,
        text=True,
        cwd=repo_dir,
        timeout=300,
    )
    if result.returncode != 0:
        return f"npm install failed:\n{result.stderr[-1000:]}"

    result = subprocess.run(
        ["npm", "test", "--", "--passWithNoTests"],
        capture_output=True,
        text=True,
        cwd=repo_dir,
        timeout=300,
    )
    if result.returncode != 0:
        return f"Tests failed:\n{result.stdout[-2000:]}"
    return f"All tests passed.\n{result.stdout[-1000:]}"


# ---------------------------------------------------------------------------
# @devops tools
# ---------------------------------------------------------------------------

def deploy_project(repo_dir: str, dry_run: bool = False) -> str:
    """Deploy the generated project to Firebase + push to GitHub.

    Args:
        repo_dir: Path to the generated project directory.
        dry_run: If True, print commands without executing.

    Returns:
        Live URL on success.
    """
    args = [str(_SCRIPTS / "deploy.py")]
    if dry_run:
        args.append("--dry-run")

    try:
        result = subprocess.run(
            ["uv", "run", "python"] + args,
            capture_output=True,
            text=True,
            cwd=repo_dir,
            timeout=600,
        )
    except FileNotFoundError:
        result = subprocess.run(
            [sys.executable] + args,
            capture_output=True,
            text=True,
            cwd=repo_dir,
            timeout=600,
        )
    if result.returncode != 0:
        raise RuntimeError(f"deploy.py failed:\n{result.stderr[-2000:]}")
    return result.stdout


# ---------------------------------------------------------------------------
# HITL tools — delegate high-stakes decisions to the hitl-approver service
# ---------------------------------------------------------------------------

_HITL_BASE_URL = os.environ.get("HITL_APPROVER_URL", "http://localhost:3456")
_HITL_SECRET = os.environ.get("HITL_API_SECRET", "")
_HITL_POLL_INTERVAL = int(os.environ.get("HITL_POLL_INTERVAL_SECONDS", "10"))
_HITL_POLL_TIMEOUT = int(os.environ.get("HITL_POLL_TIMEOUT_SECONDS", "3600"))  # 1 hour


def _hitl_request(method: str, path: str, body: dict | None = None) -> dict:
    """Make an HTTP request to the hitl-approver service."""
    url = f"{_HITL_BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if _HITL_SECRET:
        headers["Authorization"] = f"Bearer {_HITL_SECRET}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"HITL service returned HTTP {exc.code}: {exc.read().decode()}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Cannot reach hitl-approver at {_HITL_BASE_URL}: {exc.reason}. "
            "Is the hitl-approver service running? See agents/hitl-approver/README.md."
        ) from exc


def _hitl_wait_for_human(session_id: str) -> dict:
    """Poll until the session is no longer awaiting_hitl (human has responded)."""
    deadline = time.time() + _HITL_POLL_TIMEOUT
    while time.time() < deadline:
        resp = _hitl_request("GET", f"/review/{session_id}")
        status = resp.get("status")
        if status in ("completed", "error"):
            return resp
        if status == "awaiting_hitl":
            pending = resp.get("pending_calls", [])
            print(
                f"[HITL] Waiting for human decision on session {session_id}. "
                f"Pending: {[c.get('name') for c in pending]}"
            )
            time.sleep(_HITL_POLL_INTERVAL)
        else:
            # Still running — model is executing tool hooks
            time.sleep(2)

    raise TimeoutError(
        f"HITL session {session_id} did not receive a human decision "
        f"within {_HITL_POLL_TIMEOUT}s."
    )


def request_brief_review(
    project_name: str,
    brief_content: str,
    competitor_url: str,
    word_count: int,
) -> str:
    """Submit a generated brief.md for HITL review.

    The hitl-approver will auto-approve if quality standards are met, or
    pause and wait for a human to review if the brief is weak or incomplete.

    Args:
        project_name:   Name of the SaaS product.
        brief_content:  Full content of the generated brief.md.
        competitor_url: Competitor URL that seeded the brief.
        word_count:     Word count of the brief.

    Returns:
        JSON string with the review decision: approved, feedback, quality_score.
    """
    payload = {
        "project_name": project_name,
        "brief_content": brief_content,
        "competitor_url": competitor_url,
        "word_count": word_count,
    }
    resp = _hitl_request("POST", "/review", {"type": "brief", "payload": payload})
    session_id = resp.get("session_id") or resp.get("id")
    if not session_id:
        raise RuntimeError(f"hitl-approver did not return a session_id: {resp}")

    if resp.get("status") in ("awaiting_hitl",):
        print(f"[HITL] Brief requires human review — session {session_id}")
        resp = _hitl_wait_for_human(session_id)

    if resp.get("status") == "error":
        raise RuntimeError(f"HITL error: {resp.get('error')}")

    result = resp.get("result") or {}
    return json.dumps(result, indent=2)


def request_deployment_approval(
    repo_name: str,
    project_name: str,
    firebase_project: str,
    qa_summary: str,
    scaffold_file_count: int = 0,
) -> str:
    """Request human approval before deploying to Firebase.

    This call ALWAYS pauses for human review — no automated deployment is
    permitted without explicit sign-off.

    Args:
        repo_name:            GitHub repository name.
        project_name:         Human-readable product name.
        firebase_project:     Firebase project ID.
        qa_summary:           One-paragraph QA validation summary.
        scaffold_file_count:  Number of files in the generated scaffold.

    Returns:
        JSON string with the approval decision: approved, notes, approved_by.
    """
    payload = {
        "repo_name": repo_name,
        "project_name": project_name,
        "firebase_project": firebase_project,
        "qa_summary": qa_summary,
        "scaffold_file_count": scaffold_file_count,
    }
    resp = _hitl_request("POST", "/review", {"type": "deployment", "payload": payload})
    session_id = resp.get("session_id") or resp.get("id")
    if not session_id:
        raise RuntimeError(f"hitl-approver did not return a session_id: {resp}")

    # Deployment always awaits human — block until resolved
    if resp.get("status") not in ("completed", "error"):
        print(f"[HITL] Deployment approval required — session {session_id}")
        resp = _hitl_wait_for_human(session_id)

    if resp.get("status") == "error":
        raise RuntimeError(f"HITL error: {resp.get('error')}")

    result = resp.get("result") or {}
    return json.dumps(result, indent=2)


def request_qa_review(
    repo_name: str,
    stage: str,
    failures: list[str],
    qa_output: str,
) -> str:
    """Request HITL review after a QA failure.

    Auto-approves non-critical failures (npm test stubs, lint warnings).
    Escalates to a human for critical failures (missing files, bad tokens,
    template placeholders).

    Args:
        repo_name:  Repository name.
        stage:      Pipeline stage where QA failed.
        failures:   List of specific failure messages from validate_all_stages.
        qa_output:  Full QA output text.

    Returns:
        JSON string with action ('approve', 'fix_and_retry', 'halt')
        and instructions for the pipeline.
    """
    payload = {
        "repo_name": repo_name,
        "stage": stage,
        "failures": failures,
        "qa_output": qa_output,
    }
    resp = _hitl_request("POST", "/review", {"type": "qa_failure", "payload": payload})
    session_id = resp.get("session_id") or resp.get("id")
    if not session_id:
        raise RuntimeError(f"hitl-approver did not return a session_id: {resp}")

    if resp.get("status") in ("awaiting_hitl",):
        print(f"[HITL] QA failure requires human review — session {session_id}")
        resp = _hitl_wait_for_human(session_id)

    if resp.get("status") == "error":
        raise RuntimeError(f"HITL error: {resp.get('error')}")

    result = resp.get("result") or {}
    return json.dumps(result, indent=2)
