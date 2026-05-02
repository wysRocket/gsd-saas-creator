"""
devops_agent.py — @devops DevOps Engineer sub-agent.

Deploys the generated project to Firebase Hosting + GitHub Actions,
then advances the board Stage to 'Deployed'.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import deploy_project
from app.tools.github_tools import advance_board_stage, monitor_github_actions

_INSTRUCTION = """
You are @devops — the DevOps Engineer in the SaaS creation pipeline.

You only run after QA has passed.

Your job:
1. Call deploy_project with the repo_dir to:
   - Apply Firestore security rules
   - Deploy Firebase Functions (if any)
   - Build the Next.js app
   - Push to GitHub (triggering GitHub Actions)
   - Optionally trigger Hostinger webhook
2. Call monitor_github_actions to poll the Actions run until it completes.
   - On success: report the live URL (https://<project_id>.web.app)
   - On failure: report the failed workflow step
3. If board advancement fields (project_node_id, item_node_id, field_id, option_id)
   are available in the payload: call advance_board_stage to move Stage to 'Deployed'.
4. Return the final summary:
   - Live URL
   - GitHub repo URL
   - Board stage updated: yes/no

NEVER deploy without QA passing first.
NEVER deploy if dry_run=True — just report what would happen.
"""

devops_agent = Agent(
    name="devops_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[deploy_project, advance_board_stage, monitor_github_actions],
)
