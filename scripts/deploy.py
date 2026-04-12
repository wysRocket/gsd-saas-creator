"""
deploy.py — Provisions Firebase and triggers the GitHub Actions deployment.

Usage:
    python scripts/deploy.py [--dry-run]

Requires environment variables:
    FIREBASE_TOKEN        — from `firebase login:ci`
    FIREBASE_PROJECT_ID   — your Firebase project ID
    GITHUB_TOKEN          — GitHub personal access token
    GITHUB_REPO           — e.g. "username/my-saas-app"
    HOSTINGER_WEBHOOK_URL — (optional) Hostinger deploy webhook URL
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def env(key: str, required: bool = True) -> str:
    val = os.environ.get(key, "")
    if required and not val:
        print(f"Error: required environment variable '{key}' is not set.")
        print("See .env.example for the full list of required variables.")
        sys.exit(1)
    return val


def run(cmd: str, dry_run: bool = False, check: bool = True) -> int:
    print(f"  $ {cmd}")
    if dry_run:
        print("    [dry-run] skipped")
        return 0
    result = subprocess.run(cmd, shell=True, check=False)
    if check and result.returncode != 0:
        print(f"  Error: command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result.returncode


def check_cli_tools() -> None:
    missing = []
    for tool in ["firebase", "gh", "git"]:
        result = subprocess.run(f"which {tool}", shell=True, capture_output=True)
        if result.returncode != 0:
            missing.append(tool)
    if missing:
        print(f"Error: missing required CLI tools: {', '.join(missing)}")
        print("Install them before running deploy.py:")
        print("  firebase: npm install -g firebase-tools")
        print("  gh:       https://cli.github.com")
        print("  git:      https://git-scm.com")
        sys.exit(1)


def deploy(dry_run: bool = False) -> None:
    firebase_token = env("FIREBASE_TOKEN")
    project_id = env("FIREBASE_PROJECT_ID")
    github_repo = env("GITHUB_REPO")
    hostinger_webhook = env("HOSTINGER_WEBHOOK_URL", required=False)

    print("\n=== SaaS Creator: Deploy to Production ===\n")
    check_cli_tools()

    # 1. Apply Firestore security rules
    print("[1/5] Applying Firestore security rules...")
    rules_file = Path("firestore.rules")
    if not rules_file.exists():
        reference = Path(__file__).parent.parent / "reference" / "firebase_security_rules.txt"
        if reference.exists():
            rules_file.write_text(reference.read_text())
            print("      Copied reference rules to firestore.rules")
        else:
            print("      Warning: firestore.rules not found, skipping rules deployment.")
    else:
        run(
            f"FIREBASE_TOKEN={firebase_token} firebase deploy --only firestore:rules --project {project_id}",
            dry_run=dry_run,
        )

    # 2. Deploy Firebase Functions (if functions/ directory exists)
    print("[2/5] Deploying Firebase Functions...")
    if Path("functions").exists() and any(Path("functions").iterdir()):
        run(
            f"FIREBASE_TOKEN={firebase_token} firebase deploy --only functions --project {project_id}",
            dry_run=dry_run,
        )
    else:
        print("      No functions found, skipping.")

    # 3. Build the Next.js app
    print("[3/5] Building Next.js app...")
    run("npm run build", dry_run=dry_run)

    # 4. Push to GitHub (triggers Actions)
    print("[4/5] Pushing to GitHub...")
    run("git add -A", dry_run=dry_run)
    run('git commit -m "chore: deploy via saas-creator pipeline" --allow-empty', dry_run=dry_run)
    run("git push origin main", dry_run=dry_run)
    print(f"      GitHub Actions will deploy to Firebase Hosting.")
    print(f"      Track progress: https://github.com/{github_repo}/actions")

    # 5. Trigger Hostinger webhook (optional)
    if hostinger_webhook:
        print("[5/5] Triggering Hostinger webhook...")
        run(f'curl -s -X POST "{hostinger_webhook}"', dry_run=dry_run)
    else:
        print("[5/5] Hostinger webhook not configured, skipping.")

    print(f"\nDeployment initiated.")
    print(f"Live URL (after Actions complete): https://{project_id}.web.app")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy SaaS to Firebase + GitHub Actions")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them")
    args = parser.parse_args()
    deploy(dry_run=args.dry_run)
