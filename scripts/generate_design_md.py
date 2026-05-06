"""
generate_design_md.py — Design.md generator
===========================================
Reads brief.md plus designlang artifacts, then calls Gemini to produce the
canonical design.md consumed by the STITCH prompt generator.

Usage:
    python scripts/generate_design_md.py --repo-dir ./output/terrastone

Environment variables:
    GEMINI_API_KEY     — Google AI Studio key (required)

Outputs:
    <repo_dir>/design.md
"""

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path
from typing import Any

from google import genai                      # pip install google-genai
from google.genai import types as genai_types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
DESIGN_TEMPLATE = TEMPLATES_DIR / "design-template.md"
GEMINI_MODEL = "gemini-2.5-flash"

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
    message = f"{label} not found at {path}"
    if required:
        sys.exit(f"Error: {message}")
    print(f"  [warning] {message} — using empty string")
    return ""


def _latest(paths: list[Path]) -> Path | None:
    existing = [p for p in paths if p.exists()]
    if not existing:
        return None
    return sorted(existing, key=lambda p: (p.stat().st_mtime, str(p)))[-1]


def _glob_latest(repo_dir: Path, patterns: list[str]) -> Path | None:
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(repo_dir.glob(pattern))
    return _latest(candidates)


def _resolve_design_language(repo_dir: Path, explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        if path.exists():
            return path
        sys.exit(f"Error: design-language.md not found at {path}")

    candidate = _glob_latest(repo_dir, [
        "design/*design-language.md",
        "designs/*design-language.md",
        "*design-language.md",
        "design-extract-output/*design-language.md",
    ])
    if candidate:
        return candidate

    fallback = repo_dir / "design" / "competitor-design-language.md"
    print(f"  [warning] no designlang design-language.md found; defaulting to {fallback}")
    return fallback


def _resolve_tokens(repo_dir: Path, design_language_path: Path, explicit: str | None) -> Path | None:
    if explicit:
        path = Path(explicit)
        if path.exists():
            return path
        sys.exit(f"Error: design-tokens.json not found at {path}")

    sibling = Path(str(design_language_path).replace("-design-language.md", "-design-tokens.json"))
    if sibling.exists():
        return sibling

    return _glob_latest(repo_dir, [
        "design/*design-tokens.json",
        "designs/*design-tokens.json",
        "*design-tokens.json",
        "design-extract-output/*design-tokens.json",
    ])


def _load_design_template() -> str:
    if DESIGN_TEMPLATE.exists():
        return DESIGN_TEMPLATE.read_text()
    return textwrap.dedent("""\
        # Design — [Project Name]
        ## Overview
        ## Design Tokens (from designlang extraction)
        ## Pages & Key Components
        ## UX Copy
        ## Layout System
        ## Component Notes
        ## Tone & Atmosphere
        ## Competitor Reference
    """)


def _collect_token_values(node: Any, trail: tuple[str, ...] = ()) -> list[tuple[str, str, str]]:
    values: list[tuple[str, str, str]] = []
    if isinstance(node, dict):
        if "$value" in node:
            name = ".".join(trail)
            token_type = str(node.get("$type", "token"))
            value = str(node["$value"])
            values.append((name, token_type, value))
        for key, value in node.items():
            if not key.startswith("$"):
                values.extend(_collect_token_values(value, (*trail, key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            values.extend(_collect_token_values(value, (*trail, str(index))))
    return values


def _summarize_tokens(path: Path | None) -> str:
    if not path or not path.exists():
        return "No design-tokens.json artifact was found."

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return f"Could not parse {path.name}: {exc}"

    metadata = data.get("$metadata", {})
    values = _collect_token_values(data)
    by_type: dict[str, list[tuple[str, str]]] = {}
    for name, token_type, value in values:
        by_type.setdefault(token_type, []).append((name, value))

    lines = [
        f"Source: {metadata.get('source', 'unknown')}",
        f"Generated by: {metadata.get('generator', 'designlang')} {metadata.get('version', '')}".strip(),
    ]
    for token_type in ("color", "dimension", "fontFamily", "fontWeight", "shadow"):
        items = by_type.get(token_type, [])
        if not items:
            continue
        lines.append(f"\n{token_type}:")
        for name, value in items[:24]:
            lines.append(f"- {name}: {value}")
        if len(items) > 24:
            lines.append(f"- ... {len(items) - 24} more")

    return "\n".join(lines)


def _artifact_manifest(repo_dir: Path, design_language_path: Path) -> str:
    design_dir = design_language_path.parent if design_language_path.parent.exists() else repo_dir / "design"
    files = sorted(
        p for p in design_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".json", ".css", ".js", ".html", ".png", ".jpg", ".jpeg", ".webp"}
    )
    if not files:
        return "No additional designlang artifacts found."

    lines = []
    for path in files[:40]:
        rel = path.relative_to(repo_dir) if path.is_relative_to(repo_dir) else path
        lines.append(f"- {rel}")
    if len(files) > 40:
        lines.append(f"- ... {len(files) - 40} more")
    return "\n".join(lines)


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip() + "\n"
    return stripped + "\n"

# ---------------------------------------------------------------------------
# Gemini call (google-genai SDK)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a senior product designer and design systems architect.
    Your output becomes the canonical design.md for an AI-generated SaaS app.

    Rules:
    - Follow design-template.md structure EXACTLY.
    - Use brief.md for product intent, pages, UX copy, and positioning.
    - Use designlang artifacts as the source of truth for colors, typography,
      spacing, radius, shadows, component patterns, and visual references.
    - Populate every placeholder with concrete values. Never leave bracketed
      placeholder text in the final document.
    - Keep filenames and artifact references accurate and repo-relative.
    - Do NOT add commentary; output only the design.md content.
    - Be specific enough for STITCH and AI Studio to generate screens without
      asking follow-up questions.
""")


def generate_design_md(
    brief_md: str,
    design_language_md: str,
    token_summary: str,
    artifact_manifest: str,
    template: str,
) -> str:
    client = genai.Client(api_key=_require_env("GEMINI_API_KEY"))

    user_prompt = (
        "=== Product Brief ===\n"
        f"{brief_md[:5000]}\n\n"
        "=== designlang Design Language ===\n"
        f"{design_language_md[:7000]}\n\n"
        "=== designlang Token Summary ===\n"
        f"{token_summary[:5000]}\n\n"
        "=== Available designlang Artifacts ===\n"
        f"{artifact_manifest[:3000]}\n\n"
        "=== design-template.md to Fill ===\n"
        f"{template}\n\n"
        "Produce the complete design.md now."
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_prompt,
        config=genai_types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.25,
            max_output_tokens=4096,
        ),
    )
    if not response.text:
        finish = getattr(response, "prompt_feedback", None) or getattr(response, "candidates", None)
        sys.exit(f"Error: Gemini returned empty response. Check safety filters or API quota. Detail: {finish}")
    return _strip_code_fence(response.text)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate design.md via Gemini")
    parser.add_argument("--repo-dir", default="./output", help="Target repo directory")
    parser.add_argument("--brief", help="Explicit path to brief.md")
    parser.add_argument("--design-language", help="Explicit path to design-language.md")
    parser.add_argument("--design-tokens", help="Explicit path to design-tokens.json")
    parser.add_argument("--force", action="store_true", help="Regenerate even if design.md exists")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir)
    brief_path = Path(args.brief) if args.brief else repo_dir / "brief.md"
    dl_path = _resolve_design_language(repo_dir, args.design_language)
    tokens_path = _resolve_tokens(repo_dir, dl_path, args.design_tokens)

    out_path = repo_dir / "design.md"

    # Idempotent: skip if already generated (unless --force)
    if out_path.exists() and not args.force:
        existing = out_path.read_text().strip()
        if existing:
            print(f"  → design.md already exists ({len(existing):,} chars), skipping. Use --force to regenerate.")
            return

    brief_md = _load(brief_path, "brief.md", required=True)
    design_language_md = _load(dl_path, "design-language.md")
    if not design_language_md:
        sys.exit("Error: design-language.md is empty or missing. Run designlang first.")

    token_summary = _summarize_tokens(tokens_path)
    artifact_manifest = _artifact_manifest(repo_dir, dl_path)
    template = _load_design_template()

    print(f"  → using design language: {dl_path}")
    if tokens_path:
        print(f"  → using design tokens: {tokens_path}")
    print(f"  → generating design.md via Gemini ({GEMINI_MODEL}) …")
    design_md = generate_design_md(
        brief_md=brief_md,
        design_language_md=design_language_md,
        token_summary=token_summary,
        artifact_manifest=artifact_manifest,
        template=template,
    )

    out_path.write_text(design_md)
    print(f"\n✓ design.md written to {out_path} ({len(design_md):,} chars)")


if __name__ == "__main__":
    main()
