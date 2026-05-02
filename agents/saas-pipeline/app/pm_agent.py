"""
pm_agent.py — @pm Product Manager sub-agent.

Reads a GitHub Projects board item and generates brief.md
using generate_brief.py (Gemini + designlang competitor analysis).
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import generate_brief, validate_stage
from app.tools.github_tools import get_board_item_fields

_INSTRUCTION = """
You are @pm — the Product Manager agent in the SaaS creation pipeline.

Your job:
1. Read the board item fields (Title, Competitor URL, Vertical) from the payload you receive.
2. Determine the output repo directory: use PIPELINE_OUTPUT_DIR/<project_name>.
3. Call generate_brief with the project details to produce brief.md.
4. Call validate_stage with stage='brief' to confirm it meets quality standards.
5. Report: the brief.md path, word count, and any issues found.

If generate_brief fails, report the error clearly and stop — do not proceed.
If validate_stage fails, report the validation failures and stop.

You do NOT write code or make design decisions. Your only output artifact is brief.md.
"""

pm_agent = Agent(
    name="pm_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[generate_brief, validate_stage, get_board_item_fields],
)
