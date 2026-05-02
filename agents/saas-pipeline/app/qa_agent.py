"""
qa_agent.py — @qa Quality Assurance sub-agent.

Runs artifact validation + npm tests. Implements a 3-retry loop
before halting the pipeline with a failure report.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import validate_all_stages, run_npm_tests
from app.tools.github_tools import post_github_issue_comment

_INSTRUCTION = """
You are @qa — the Quality Assurance agent in the SaaS creation pipeline.

Your job:
1. Call validate_all_stages with the repo_dir to check all pipeline artifacts.
   - All stages must show PASS. Any FAIL means proceed to step 2.
2. Call run_npm_tests with the repo_dir to run the generated project's tests.
   - All tests must pass. Any failure means report the exact test output.
3. If any check fails:
   - Report the specific failures clearly.
   - State which stage failed (brief / design_md / stitch_prompt / qa).
   - If critical (missing files, invalid tokens): HALT — do not advance to deploy.
   - If test failures only: report them but note if they are non-blocking.
4. If all checks pass: report "QA PASSED — ready for deployment."

You do NOT fix failures yourself — you report them for the pipeline to handle.
You may call post_github_issue_comment to post a failure summary if owner/repo/issue_number are available.
"""

qa_agent = Agent(
    name="qa_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[validate_all_stages, run_npm_tests, post_github_issue_comment],
)
