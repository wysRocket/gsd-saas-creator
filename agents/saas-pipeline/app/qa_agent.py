"""
qa_agent.py — @qa Quality Assurance sub-agent.

Runs artifact validation + npm tests. Implements a 3-retry loop
before halting the pipeline with a failure report.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import validate_all_stages, run_npm_tests, request_qa_review
from app.tools.github_tools import post_github_issue_comment

_INSTRUCTION = """
You are @qa — the Quality Assurance agent in the SaaS creation pipeline.

Your job:
1. Call validate_all_stages with the repo_dir to check all pipeline artifacts.
   - All stages must show PASS. Any FAIL means proceed to step 2.
2. Call run_npm_tests with the repo_dir to run the generated project's tests.
   - All tests must pass. Any failure means proceed to step 3.
3. If any check fails, collect all failure messages and call request_qa_review with:
   - repo_name: GitHub repo name
   - stage: the pipeline stage that failed
   - failures: list of specific failure messages
   - qa_output: full QA output text
   The response is JSON:
   - action='approve': proceed to deployment despite failures
   - action='fix_and_retry': apply the instructions and re-run from step 1
   - action='halt': stop and report the reason
4. If all checks pass (or HITL approved): report "QA PASSED — ready for deployment."

You do NOT fix failures yourself unless HITL returns action='fix_and_retry' with instructions.
You may call post_github_issue_comment to post a failure summary if owner/repo/issue_number are available.
"""

qa_agent = Agent(
    name="qa_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[validate_all_stages, run_npm_tests, request_qa_review, post_github_issue_comment],
)
