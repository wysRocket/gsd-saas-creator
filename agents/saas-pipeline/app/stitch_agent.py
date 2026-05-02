"""
stitch_agent.py — @stitch Design DNA extractor sub-agent.

Connects to Stitch MCP and extracts design tokens (colors, typography,
components) into design_tokens.json. Falls back to reference schema
if Stitch MCP is unreachable or no project ID is provided.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import extract_stitch_dna

_INSTRUCTION = """
You are @stitch — the Design DNA extractor in the SaaS creation pipeline.

Your job:
1. Check if a Stitch Project ID was provided in the pipeline payload.
2. If yes: call extract_stitch_dna with that project_id and output to
   <repo_dir>/design_tokens.json
3. If no Stitch ID or MCP is unavailable: report that you are using the
   fallback reference schema — this is acceptable.
4. Report what was extracted: number of colors, screens, fonts.

You do NOT generate design decisions. You only extract existing Stitch tokens.
If the MCP is unreachable, extraction will fall back automatically — this is not an error.
"""

stitch_agent = Agent(
    name="stitch_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[extract_stitch_dna],
)
