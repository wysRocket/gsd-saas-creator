"""
pipeline_tools.py — ADK tool wrappers for gsd-saas-creator scripts.

Each function is an ADK-compatible tool that wraps a script in scripts/.
All tools return a string result (success message or error).
"""

from __future__ import annotations

import os
import subprocess
import sys
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
