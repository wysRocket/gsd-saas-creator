"""
generate_stitch_prompt.py — AI Studio STITCH prompt generator
==============================================================
Reads brief.md + competitor design-language.md, then calls Gemini
to produce a production-ready stitch-prompt.md optimised for AI Studio.

Usage:
    python scripts/generate_stitch_prompt.py \\
        --repo-dir ./output/terrastone

    # Or supply individual paths:
    python scripts/generate_stitch_prompt.py \\
        --brief ./output/terrastone/brief.md \\
        --design-language ./output/terrastone/design/competitor-design-language.md

Environment variables:
    GEMINI_API_KEY     — Google AI Studio key (required)

Outputs:
    <repo_dir>/stitch-prompt.md
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

import google.generativeai as genai  # pip install google-generativeai


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
STITCH_TEMPLATE = TEMPLATES_DIR / "stitch-template.md"
GEMINI_MODEL = "gemini-2.0-flash"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_env(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        sys.exit(f"Error: environment variable {key} is not set.")
    return val


def _load(path: Path, label: str) -> str:
    if path.exists():
        return path.read_text()
    print(f"  [warning] {label} not found at {path} — using empty string")
    return ""


def _load_stitch_template() -> str:
    if STITCH_TEMPLATE.exists():
        return STITCH_TEMPLATE.read_text()
    # Minimal embedded fallback
    return textwrap.dedent("""\
        # STITCH PROMPT — {{PROJECT_NAME}}

        ## System Prompt (Global)
        ## Page: Landing
        ### Hero Section
        ### Features Section
        ### Pricing Section
        ### CTA Section
        ## Page: Dashboard
        ### Sidebar Navigation
        ### Main Content Area
    """)


# ---------------------------------------------------------------------------
# Gemini call
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are an expert AI Studio / STITCH prompt engineer.
    Your output is fed directly into STITCH to generate UI designs.

    Rules:
    - Follow the stitch-template.md structure EXACTLY.
    - Every section must contain precise visual instructions: colors (hex),
      fonts, spacing, layout, component variants, copy examples.
    - Reference the competitor's design DNA to ensure the generated UI
      matches the product vertical aesthetically.
    - Use the brief to determine page structure and feature copy.
    - Do NOT add commentary; output only the stitch-prompt.md content.
    - Be specific enough that a designer could implement without asking questions.
    - Aim for 2-4 pages minimum, each with 4-8 sections.
""")


def generate_stitch_prompt(
    brief_md: str,
    design_language_md: str,
    template: str,
) -> str:
    genai.configure(api_key=_require_env("GEMINI_API_KEY"))
    model = genai.GenerativeModel(GEMINI_MODEL)

    user_prompt = (
        "=== Product Brief ===\n"
        f"{brief_md[:4000]}\n\n"
        "=== Competitor Design Language ===\n"
        f"{design_language_md[:4000]}\n\n"
        "=== STITCH Template to Fill ===\n"
        f"{template}\n\n"
        "Produce the complete stitch-prompt.md now. Be exhaustive."
    )

    response = model.generate_content(
        [{"role": "user", "parts": [user_prompt]}],
        generation_config={"temperature": 0.3, "max_output_tokens": 4096},
        system_instruction=SYSTEM_PROMPT,
    )
    return response.text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate stitch-prompt.md via Gemini")
    parser.add_argument("--repo-dir", default="./output", help="Target repo directory (auto-discovers brief.md and design/)")
    parser.add_argument("--brief", help="Explicit path to brief.md")
    parser.add_argument("--design-language", help="Explicit path to design-language.md")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir)

    # Resolve input paths
    brief_path = Path(args.brief) if args.brief else repo_dir / "brief.md"
    dl_path = (
        Path(args.design_language) if args.design_language
        else next(repo_dir.glob("design/*design-language.md"), repo_dir / "design" / "competitor-design-language.md")
    )

    brief_md = _load(brief_path, "brief.md")
    design_language_md = _load(dl_path, "design-language.md")
    template = _load_stitch_template()

    if not brief_md:
        sys.exit("Error: brief.md is empty or missing. Run generate_brief.py first.")

    print(f"  → generating stitch-prompt.md via Gemini ({GEMINI_MODEL}) …")
    stitch_md = generate_stitch_prompt(brief_md, design_language_md, template)

    out_path = repo_dir / "stitch-prompt.md"
    out_path.write_text(stitch_md)
    print(f"\n✓ stitch-prompt.md written to {out_path} ({len(stitch_md):,} chars)")


if __name__ == "__main__":
    main()
