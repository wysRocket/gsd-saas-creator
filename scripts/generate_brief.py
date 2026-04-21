"""
generate_brief.py — AI-powered product brief generator
=======================================================
Reads designlang output (design-language.md) from a competitor URL,
pairs it with the brief template, and calls Gemini to produce a
structured brief.md for the new SaaS product.

Usage:
    python scripts/generate_brief.py \\
        --name "Terrastone" \\
        --competitor-url "https://kingdomofarcane.com" \\
        --vertical Gaming \\
        --repo-dir ./output/terrastone

Environment variables:
    GEMINI_API_KEY     — Google AI Studio key (required)

Outputs:
    <repo_dir>/brief.md
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import google.generativeai as genai  # pip install google-generativeai


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
BRIEF_TEMPLATE = TEMPLATES_DIR / "brief-template.md"

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_env(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        sys.exit(f"Error: environment variable {key} is not set.")
    return val


def _run_designlang(url: str, output_dir: Path) -> Path:
    """Run designlang on the competitor URL and return path to design-language.md."""
    print(f"  → running designlang on {url} …")
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]", "-", url.lower().split("//")[-1].split("/")[0])
    result = subprocess.run(
        ["npx", "designlang", url, "--full", "--screenshots", "--output", str(output_dir)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  [warning] designlang exited {result.returncode}: {result.stderr[:400]}")

    # Locate the output file — designlang names it <slug>-design-language.md
    candidates = sorted(output_dir.glob("*design-language.md"))
    if candidates:
        return candidates[-1]

    # Fall back: look for any .md file produced
    md_files = sorted(output_dir.glob("*.md"))
    if md_files:
        return md_files[-1]

    return Path("/dev/null")


def _load_brief_template() -> str:
    if BRIEF_TEMPLATE.exists():
        return BRIEF_TEMPLATE.read_text()
    # Minimal embedded fallback
    return textwrap.dedent("""\
        # {{PROJECT_NAME}} — Product Brief

        ## Summary
        ## Brand
        ## MVP Scope
        ## Key Pages
        ## Design Direction
        ## Personas
        ## Pricing
        ## Tech Stack
        ## Launch Success Metric
    """)


# ---------------------------------------------------------------------------
# Gemini call
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a senior product strategist and SaaS founder. Your job is to
    produce a detailed, actionable product brief for a new SaaS application.

    Rules:
    - Use the provided brief template structure EXACTLY.
    - Populate every section with concrete, specific content.
    - Extract colors, fonts, and design patterns from the competitor
      design-language.md provided.
    - Invent realistic persona names, company names, and pain points.
    - Suggest 3 pricing tiers with realistic prices.
    - Write English only, keep < 1500 words total.
    - Do NOT add commentary outside the template sections.
""")


def generate_brief(
    name: str,
    competitor_url: str,
    vertical: str,
    design_language_md: str,
    template: str,
) -> str:
    genai.configure(api_key=_require_env("GEMINI_API_KEY"))
    model = genai.GenerativeModel(GEMINI_MODEL)

    user_prompt = (
        f"Product name: {name}\n"
        f"Vertical: {vertical}\n"
        f"Competitor URL: {competitor_url}\n\n"
        "=== Competitor Design Language ===\n"
        f"{design_language_md[:6000]}\n\n"
        "=== Brief Template to Fill ===\n"
        f"{template}\n\n"
        "Produce the completed brief.md now."
    )

    response = model.generate_content(
        [{"role": "user", "parts": [user_prompt]}],
        generation_config={"temperature": 0.4, "max_output_tokens": 2048},
        system_instruction=SYSTEM_PROMPT,
    )
    return response.text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate brief.md via Gemini")
    parser.add_argument("--name", required=True, help="SaaS product name")
    parser.add_argument("--competitor-url", required=True, help="Competitor website URL")
    parser.add_argument("--vertical", default="Other", help="Business vertical (Gaming, Hosting…)")
    parser.add_argument("--repo-dir", default="./output", help="Target repo directory")
    parser.add_argument("--design-language", help="Path to existing design-language.md (skip designlang run)")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir)
    repo_dir.mkdir(parents=True, exist_ok=True)

    # Step 1 — get design language
    if args.design_language and Path(args.design_language).exists():
        dl_path = Path(args.design_language)
        print(f"  → using existing design language: {dl_path}")
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            dl_path = _run_designlang(args.competitor_url, Path(tmpdir))
            design_language_md = dl_path.read_text() if dl_path.exists() else ""
            # Also save it to repo
            out_dl = repo_dir / "design" / "competitor-design-language.md"
            out_dl.parent.mkdir(parents=True, exist_ok=True)
            out_dl.write_text(design_language_md)
            print(f"  → design language saved: {out_dl}")

    design_language_md = dl_path.read_text() if dl_path.exists() else ""

    # Step 2 — load template
    template = _load_brief_template()

    # Step 3 — call Gemini
    print(f"  → generating brief via Gemini ({GEMINI_MODEL}) …")
    brief_md = generate_brief(
        name=args.name,
        competitor_url=args.competitor_url,
        vertical=args.vertical,
        design_language_md=design_language_md,
        template=template,
    )

    # Step 4 — write output
    out_path = repo_dir / "brief.md"
    out_path.write_text(brief_md)
    print(f"\n✓ brief.md written to {out_path} ({len(brief_md):,} chars)")


if __name__ == "__main__":
    main()
