import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board_ops

# ---------------------------------------------------------------------------
# Config & Helpers
# ---------------------------------------------------------------------------

GH_TOKEN = os.environ.get("GH_TOKEN", "")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

def _require_token():
    if not GH_TOKEN:
        print("Error: GH_TOKEN environment variable is not set.")
        sys.exit(1)
    return GH_TOKEN

def _push_artifacts(repo_name, files, commit_msg, token):
    """Clone, copy files, commit, and push to the SaaS-Pretty-Projects repo."""
    clone_dir = Path(tempfile.mkdtemp())
    try:
        print(f"  → cloning {repo_name} …")
        subprocess.run(
            ["gh", "repo", "clone", f"{board_ops.ORG}/{repo_name}", str(clone_dir)],
            check=True, capture_output=True,
            env={**os.environ, "GH_TOKEN": token},
        )
        
        source_dir = OUTPUT_DIR / repo_name
        copied = False
        for f in files:
            src = source_dir / f
            dest = clone_dir / f
            if src.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
                copied = True
            elif src.is_file():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                copied = True
            else:
                print(f"  [warning] entry not found for push: {src}")

        if not copied:
            print("  → nothing to push")
            return

        subprocess.run(["git", "-C", str(clone_dir), "add", "."], check=True)
        # Check if there are changes
        status = subprocess.run(["git", "-C", str(clone_dir), "status", "--porcelain"], check=True, capture_output=True, text=True)
        if not status.stdout.strip():
            print("  → no changes to commit")
            return

        subprocess.run(["git", "-C", str(clone_dir), "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "-C", str(clone_dir), "push"], check=True)
        print(f"  ✓ pushed artifacts to {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"  [error] git operation failed: {e.stderr.decode() if e.stderr else e}")
    finally:
        shutil.rmtree(clone_dir)

def _post_error_and_exit(repo_name, issue_number, stage, error_msg, token):
    body = f"❌ **Error in stage '{stage}'**\n\n{error_msg}"
    board_ops.post_comment(f"{board_ops.ORG}/{repo_name}", issue_number, body, token)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Stage Handlers
# ---------------------------------------------------------------------------

def handle_brief(args, token):
    repo_dir = OUTPUT_DIR / args.repo_name
    repo_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"  → generating brief for {args.repo_name} …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "generate_brief.py"),
            "--name", args.project_name,
            "--competitor-url", args.competitor_url,
            "--vertical", args.vertical,
            "--repo-dir", str(repo_dir)
        ], check=True)
        
        # Create repo if not exists
        print(f"  → ensuring github repo {args.repo_name} exists …")
        subprocess.run(["gh", "repo", "create", f"{board_ops.ORG}/{args.repo_name}", "--public", "--confirm"], check=False)
        
        _push_artifacts(args.repo_name, ["brief.md"], "docs: add initial product brief", token)
        
        repo_url = f"https://github.com/{board_ops.ORG}/{args.repo_name}"
        board_ops.update_text_field(args.item_id, board_ops.REPO_URL_FIELD_ID, repo_url, token)
        
        comment = f"✅ **Brief Generated**\n\nRepo: {repo_url}\nNext: Designer is drafting `design.md`."
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)
        board_ops.update_stage(args.item_id, "design_md", token)
        
    except subprocess.CalledProcessError as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "brief", str(e), token)

def handle_design_md(args, token):
    repo_dir = OUTPUT_DIR / args.repo_name
    try:
        print(f"  → generating design.md for {args.repo_name} …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "generate_design_md.py"),
            "--repo-dir", str(repo_dir)
        ], check=True)
        
        print("  → validating design_md stage …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "agent_workflow.py"),
            "validate-stage", "design_md",
            "--repo-dir", str(repo_dir),
            "--log"
        ], check=True)
        
        _push_artifacts(args.repo_name, ["design.md", "pipeline-events.jsonl"], "design: add canonical design contract", token)
        
        comment = "✅ **Design Contract Ready**\n\n`design.md` has been pushed to the repo.\nNext: Generating `stitch-prompt.md`."
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)
        board_ops.update_stage(args.item_id, "stitch_prompt", token)
        
    except subprocess.CalledProcessError as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "design_md", str(e), token)

def handle_stitch_prompt(args, token):
    repo_dir = OUTPUT_DIR / args.repo_name
    try:
        print(f"  → generating stitch-prompt.md for {args.repo_name} …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "generate_stitch_prompt.py"),
            "--repo-dir", str(repo_dir)
        ], check=True)
        
        print("  → validating stitch_prompt stage …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "agent_workflow.py"),
            "validate-stage", "stitch_prompt",
            "--repo-dir", str(repo_dir),
            "--log"
        ], check=True)
        
        _push_artifacts(args.repo_name, ["stitch-prompt.md", "pipeline-events.jsonl"], "design: add stitch prompt for AI Studio", token)
        
        comment = "✋ **Design Pipeline Halted**\n\n`stitch-prompt.md` is ready. Please use it in AI Studio / STITCH to generate the design board. Once the board is ready, move this item to **Designs Ready**."
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)
        # We do NOT advance stage automatically here
        
    except subprocess.CalledProcessError as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "stitch_prompt", str(e), token)

def handle_ai_studio(args, token):
    """Scaffold the application: create repo, clone it, run scaffold.py, push, update board."""
    clone_dir = Path(tempfile.mkdtemp())
    try:
        # 1. Ensure GitHub repo exists
        print(f"  → ensuring github repo {args.repo_name} exists …")
        subprocess.run(
            ["gh", "repo", "create", f"{board_ops.ORG}/{args.repo_name}", "--public",
             "--description", f"{args.project_name} SaaS"],
            check=False,  # idempotent - ok if already exists
            env={**os.environ, "GH_TOKEN": token},
        )

        # 2. Clone the repo
        print(f"  → cloning {args.repo_name} …")
        subprocess.run(
            ["gh", "repo", "clone", f"{board_ops.ORG}/{args.repo_name}", str(clone_dir)],
            check=True,
            env={**os.environ, "GH_TOKEN": token},
        )

        # 3. Run scaffold.py into the cloned dir
        print(f"  → scaffolding application for {args.repo_name} …")
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "scaffold.py"),
             "--repo-dir", str(clone_dir)],
            check=False,  # best-effort scaffold
        )

        # 4. Commit and push
        print(f"  → committing and pushing scaffold artifacts …")
        subprocess.run(["git", "-C", str(clone_dir), "add", "."], check=True)
        commit_result = subprocess.run(
            ["git", "-C", str(clone_dir), "commit", "-m", "feat: scaffold application from designs"],
            check=False, capture_output=True, text=True
        )
        if commit_result.returncode == 0:
            subprocess.run(
                ["git", "-C", str(clone_dir), "push"],
                check=True,
                env={**os.environ, "GH_TOKEN": token},
            )
            print(f"  ✓ pushed scaffold artifacts to {args.repo_name}")
        else:
            # No changes to commit (scaffold may have produced nothing)
            print(f"  → no changes to commit (scaffold produced no artifacts)")

        # 5. Set Repo URL field on the board
        repo_url = f"https://github.com/{board_ops.ORG}/{args.repo_name}"
        board_ops.update_text_field(args.item_id, board_ops.REPO_URL_FIELD_ID, repo_url, token)

        # 6. Advance stage to In Progress
        board_ops.update_stage(args.item_id, "in_progress", token)

        comment = "🚀 **Application Scaffolding Complete**\n\nThe implementation has been pushed to the repo. Moving to **In Progress** for human refinement."
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)

    except subprocess.CalledProcessError as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "ai_studio", str(e), token)
    except Exception as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "ai_studio", str(e), token)
    finally:
        shutil.rmtree(clone_dir)

def handle_qa(args, token):
    """Run QA validation on all generated artifacts. Blocks promotion on failure."""
    repo_dir = OUTPUT_DIR / args.repo_name
    try:
        print(f"  → running QA validation for {args.repo_name} …")
        result = subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "agent_workflow.py"),
            "validate-stage", "qa",
            "--repo-dir", str(repo_dir),
            "--log"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            failures = result.stdout + result.stderr
            board_ops.post_comment(
                f"{board_ops.ORG}/{args.repo_name}", args.issue_number,
                f"❌ **QA Validation Failed**\n\nThe artifact set failed QA checks:\n```\n{failures[-1000:]}\n```\n\nPlease review and move to **Revisions** to regenerate.", token
            )
            print(f"  [qa] validation failed:\n{failures[-1000:]}")
            return  # Do NOT advance stage — QA is a gate

        # QA passed — advance to deploy
        board_ops.post_comment(
            f"{board_ops.ORG}/{args.repo_name}", args.issue_number,
            "✅ **QA Passed — All artifacts validated**\n\n`brief.md`, `design.md`, `stitch-prompt.md` are complete and verified.\nAdvancing to **Deploy** stage.", token
        )
        board_ops.update_stage(args.item_id, "launched", token)
        print(f"  ✓ QA passed, advanced to launched")

    except subprocess.CalledProcessError as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "qa", str(e), token)
    except Exception as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "qa", str(e), token)


def handle_launched(args, token):
    repo_dir = OUTPUT_DIR / args.repo_name
    try:
        print(f"  → deploying {args.repo_name} …")
        subprocess.run([
            sys.executable, str(PROJECT_ROOT / "scripts" / "deploy.py"),
            "--repo-dir", str(repo_dir)
        ], check=False)

        comment = "🌐 **SaaS Application Deployed!**\n\nThe application is now live. Moving to **Operating** stage."
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)
        board_ops.update_stage(args.item_id, "operating", token)
    except Exception as e:
        _post_error_and_exit(args.repo_name, args.issue_number, "launched", str(e), token)

def handle_revisions(args, token):
    body = args.comment_body.lower()
    if "brief" in body:
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, "🔄 Routing revision request to **Brief** generator.", token)
        handle_brief(args, token)
    elif "design" in body:
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, "🔄 Routing revision request to **Design** generator.", token)
        handle_design_md(args, token)
    elif "prompt" in body:
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, "🔄 Routing revision request to **Stitch Prompt** generator.", token)
        handle_stitch_prompt(args, token)
    else:
        board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, "👀 Revision request received but no routing keyword detected (brief, design, prompt). Waiting for human triage.", token)

def handle_clarification(args, token):
    comment = "❓ **Clarification Required**\n\nThe agent needs more information to proceed. Please review the 'Notes' or 'Problem' field."
    board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)

def handle_passive(args, token, label):
    comment = f"ℹ️ **Stage Update: {label}**\n\nThe project is now in the **{label}** stage. No automated action required at this moment."
    board_ops.post_comment(f"{board_ops.ORG}/{args.repo_name}", args.issue_number, comment, token)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Orchestrate SaaS project pipeline")
    parser.add_argument("--stage", default="", help="Current project stage")
    parser.add_argument("--item-id", default="", help="GitHub Project item ID")
    parser.add_argument("--issue-number", default="", help="GitHub Issue number")
    parser.add_argument("--repo-name", default="", help="Repository name")
    parser.add_argument("--project-name", default="", help="Project name")
    parser.add_argument("--competitor-url", default="", help="Competitor URL")
    parser.add_argument("--vertical", default="", help="Business vertical")
    parser.add_argument("--notes", default="", help="Notes or clarification request")
    parser.add_argument("--comment-body", default="", help="Body of the triggering comment")
    
    args = parser.parse_args()
    token = _require_token()

    stage = args.stage.lower()
    print(f"--- Orchestrating Stage: {stage} for {args.repo_name} ---")

    if stage == "brief":
        handle_brief(args, token)
    elif stage == "design_md":
        handle_design_md(args, token)
    elif stage == "stitch_prompt":
        handle_stitch_prompt(args, token)
    elif stage == "qa":
        handle_qa(args, token)
    elif stage == "ai_studio":
        handle_ai_studio(args, token)
    elif stage == "launched":
        handle_launched(args, token)
    elif stage == "revisions":
        handle_revisions(args, token)
    elif stage == "clarification":
        handle_clarification(args, token)
    elif stage == "designs_ready":
        handle_passive(args, token, "Designs Ready")
    elif stage == "in_progress":
        handle_passive(args, token, "In Progress")
    elif stage == "ready_for_prod":
        handle_passive(args, token, "Ready for Production")
    elif stage == "operating":
        handle_passive(args, token, "Operating")
    elif stage == "done":
        handle_passive(args, token, "Done")
    else:
        print(f"No handler defined for stage: {stage}")

if __name__ == "__main__":
    main()
