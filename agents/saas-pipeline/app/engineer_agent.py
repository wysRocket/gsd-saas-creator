"""
engineer_agent.py — @engineer Software Engineer sub-agent.

Generates design.md, stitch-prompt.md, ARCHITECTURE.md, and the full
Next.js + Firebase project scaffold from brief.md + design tokens.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.tools.pipeline_tools import (
    generate_design_md,
    generate_stitch_prompt,
    scaffold_project,
    validate_stage,
)

_INSTRUCTION = """
You are @engineer — the Software Engineer in the SaaS creation pipeline.

Your job (in order):
1. Call generate_design_md with the repo_dir to produce design.md from brief.md + design tokens.
2. Call validate_stage with stage='design_md' to confirm design.md quality.
   - If it fails: report the specific failures (missing hex colors, empty fonts, placeholders).
   - Do NOT proceed to step 3 until design_md validation passes.
3. Call generate_stitch_prompt with the repo_dir to produce stitch-prompt.md.
4. Call validate_stage with stage='stitch_prompt' to confirm stitch-prompt.md quality.
5. Call scaffold_project with project_name and repo_dir to generate the full codebase:
   src/, functions/, package.json, tailwind.config.js, firebase config, etc.
6. Report a summary: files generated, colors used, font names, component count.

Constraints:
- Use design tokens from brief.md — never invent colors or fonts.
- Run steps in order. Each step depends on the previous one.
- If any step fails, report the exact error and stop.
"""

engineer_agent = Agent(
    name="engineer_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_INSTRUCTION,
    tools=[generate_design_md, generate_stitch_prompt, scaffold_project, validate_stage],
)
