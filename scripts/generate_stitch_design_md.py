"""
generate_stitch_design_md.py — Stitch-native DESIGN.md generator
=============================================================
Reads brief.md and designlang design-language.md, then calls Gemini to produce
a Stitch-compatible DESIGN.md in the official Stitch DESIGN.md format
(Brand, Color, Typography, Components, Spacing, Depth, Do's/Don'ts, Responsive).

Usage:
    python scripts/generate_stitch_design_md.py --repo-dir ./output/guidenza

Environment variables:
    GEMINI_API_KEY     — Google AI Studio key (required)

Outputs:
    <repo_dir>/DESIGN.md          (Stitch-native format)
"""

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path

from google import genai                      # pip install google-genai
from google.genai import types as genai_types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GEMINI_MODEL = "gemini-2.5-pro"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_env(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        sys.exit(f"Error: environment variable {key} is not set.")
    return val


def _load(path: Path, label: str, required: bool = False) -> str:
    if path.exists():
        return path.read_text()
    msg = f"{label} not found at {path}"
    if required:
        sys.exit(f"Error: {msg}")
    print(f"  [warning] {msg} — using empty string")
    return ""


def _resolve_brief(repo_dir: Path, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.exists():
            return p
        sys.exit(f"Error: brief.md not found at {p}")
    default = repo_dir / "brief.md"
    if default.exists():
        return default
    sys.exit(f"Error: brief.md not found at {default} and no --brief given.")


def _resolve_design_language(repo_dir: Path, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.exists():
            return p
        sys.exit(f"Error: design-language.md not found at {p}")

    for pattern in (
        "design/*design-language.md",
        "designs/*design-language.md",
        "*design-language.md",
        "design-extract-output/*design-language.md",
    ):
        candidates = sorted(repo_dir.glob(pattern), key=lambda x: x.stat().st_mtime)
        if candidates:
            return candidates[-1]

    fallback = repo_dir / "design" / "competitor-design-language.md"
    if fallback.exists():
        return fallback
    sys.exit(f"Error: design-language.md not found. Searched: design/*design-language.md, etc.")


def _resolve_tokens(repo_dir: Path, dl_path: Path, explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        if p.exists():
            return p
        return None

    # Try sibling of design-language.md
    sibling = Path(str(dl_path).replace("-design-language.md", "-design-tokens.json"))
    if sibling.exists():
        return sibling

    for pattern in (
        "design/*design-tokens.json",
        "designs/*design-tokens.json",
        "design-extract-output/*design-tokens.json",
    ):
        candidates = sorted(repo_dir.glob(pattern), key=lambda x: x.stat().st_mtime)
        if candidates:
            return candidates[-1]
    return None


def _collect_color_tokens(node: dict, trail: tuple = ()) -> list[tuple[str, str, str]]:
    """Recursively collect color tokens with their hex values."""
    results = []
    if isinstance(node, dict):
        if "$value" in node:
            name = ".".join(trail)
            # Try to extract hex from various formats
            val = str(node["$value"])
            token_type = node.get("$type", "color")
            results.append((name, token_type, val))
        for k, v in node.items():
            if not k.startswith("$"):
                results.extend(_collect_color_tokens(v, (*trail, k)))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            results.extend(_collect_color_tokens(v, (*trail, str(i))))
    return results


def _summarize_colors(tokens_path: Path | None) -> str:
    """Extract a clean color table from design-tokens.json."""
    if not tokens_path or not tokens_path.exists():
        return ""

    try:
        data = json.loads(tokens_path.read_text())
    except json.JSONDecodeError:
        return ""

    colors = []
    for name, _, value in _collect_color_tokens(data):
        # Only include hex-like values
        clean_value = value.strip()
        if clean_value.startswith("#") or clean_value.startswith("rgb"):
            colors.append((name, clean_value))

    if not colors:
        return ""

    lines = []
    for name, value in colors[:40]:
        lines.append(f"| `{name}` | {value} |")
    return "\n".join(lines)


def _extract_style_section(dl_md: str) -> str:
    """Pull the most useful sections from a designlang artifact."""
    lines = dl_md.splitlines()
    useful = []
    capturing = False
    for line in lines:
        # Capture color, typography, spacing, border sections
        low = line.lower()
        if any(k in low for k in ["color", "typography", "font", "spacing", "radius", "shadow", "background", "surface", "text", "style"]):
            capturing = True
        if capturing:
            useful.append(line)
            if len(useful) > 200:
                break
    return "\n".join(useful[:200])


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a senior design systems architect. Your job is to produce a
    Stitch-compatible DESIGN.md — the open standard format used by Google Stitch
    (stitch.withgoogle.com).

    The Stitch DESIGN.md format has these exact sections:

    1. Overview / Visual Theme & Atmosphere
       — Mood, density, visual philosophy, who this is for

    2. Color Palette & Roles
       — Semantic token table: Token | Hex | Role/Usage
       — Group by: Brand/Accent, Surface/Background, Text, Border, Semantic (success/warning/error)

    3. Typography Rules
       — Font families with fallbacks
       — Full type scale table: Role | Font | Size | Weight | Line Height | Letter Spacing | Use

    4. Component Stylings
       — Buttons (primary, secondary, ghost, disabled), cards, inputs, navigation
       — Include: background, text color, border, padding, radius, shadow, hover/active states

    5. Spacing System
       — Base unit + scale table: Token | Value | Use

    6. Layout Principles
       — Grid, max-width, section rhythm, responsive collapsing

    7. Depth & Elevation
       — Shadow system with formula + use cases

    8. Do's and Don'ts
       — 3-5 concrete rules each, design guardrails

    9. Responsive Behavior
       — Breakpoints, touch targets, collapsing behavior

    Rules:
    - Follow the section structure EXACTLY as above.
    - Use semantic color names (primary, surface, text-primary, border, etc.) alongside hex.
    - Every table must have a header row.
    - Never leave placeholder text in the final output.
    - Keep it thorough but under 6000 tokens total output.
""")


def generate_stitch_design_md(
    brief_md: str,
    design_language_md: str,
    color_table: str,
    product_name: str,
    style_snippet: str,
) -> str:
    client = genai.Client(api_key=_require_env("GEMINI_API_KEY"))

    user_prompt = (
        f"# Product: {product_name}\n\n"
        f"=== brief.md ===\n{brief_md[:2500]}\n\n"
        f"=== Design Colors & Style ===\n{style_snippet[:3000]}\n\n"
        f"=== Extracted Colors ===\n{color_table or 'No token file — use style section above'}\n\n"
        "Produce the Stitch DESIGN.md now. Follow the 9-section structure exactly. "
        "Be concrete and specific — no placeholders."
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_prompt,
        config=genai_types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=8192,
        ),
    )
    if not response.text:
        finish = getattr(response, "prompt_feedback", None) or getattr(response, "candidates", None)
        sys.exit(f"Error: Gemini returned empty response. Detail: {finish}")
    return response.text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Stitch-native DESIGN.md via Gemini"
    )
    parser.add_argument("--repo-dir", default="./output", help="Target repo directory")
    parser.add_argument("--brief", help="Explicit path to brief.md")
    parser.add_argument(
        "--design-language",
        help="Explicit path to design-language.md",
    )
    parser.add_argument(
        "--design-tokens",
        help="Explicit path to design-tokens.json",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if DESIGN.md exists",
    )
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir)
    repo_dir.mkdir(parents=True, exist_ok=True)

    brief_path = _resolve_brief(repo_dir, args.brief)
    dl_path = _resolve_design_language(repo_dir, args.design_language)
    tokens_path = _resolve_tokens(repo_dir, dl_path, args.design_tokens)

    out_path = repo_dir / "DESIGN.md"

    # Idempotent skip
    if out_path.exists() and not args.force:
        existing = out_path.read_text().strip()
        if existing:
            print(f"  → DESIGN.md already exists ({len(existing):,} chars), skipping. Use --force to regenerate.")
            return

    brief_md = _load(brief_path, "brief.md", required=True)
    dl_md = _load(dl_path, "design-language.md")
    color_table = _summarize_colors(tokens_path)

    # Extract product name from brief.md (look for "Name:" line)
    product_name = repo_dir.name
    for line in brief_md.splitlines():
        if line.strip().startswith("Name:") or line.strip().startswith("**Name:**"):
            product_name = line.split(":", 1)[-1].strip().rstrip("*")
            break

    style_snippet = _extract_style_section(dl_md)

    print(f"  → brief:      {brief_path}")
    print(f"  → designlang: {dl_path}")
    if tokens_path:
        print(f"  → tokens:     {tokens_path}")
    print(f"  → generating DESIGN.md via Gemini ({GEMINI_MODEL}) …")

    design_md = generate_stitch_design_md(
        brief_md=brief_md,
        design_language_md=dl_md,
        color_table=color_table,
        product_name=product_name,
        style_snippet=style_snippet,
    )

    out_path.write_text(design_md)
    print(f"\n✓ DESIGN.md written to {out_path} ({len(design_md):,} chars)")


if __name__ == "__main__":
    main()
