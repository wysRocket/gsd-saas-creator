"""
dry_run_design_pipeline.py — run the Design.md automation flow locally.

Live mode requires GEMINI_API_KEY and runs the real generators:
    python scripts/dry_run_design_pipeline.py --repo-dir output/dry-run

Offline mode creates deterministic fixture artifacts and exercises the same
agent workflow gates without calling Gemini:
    python scripts/dry_run_design_pipeline.py --repo-dir output/dry-run --offline-fixture
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)


def copy_design_artifacts(source_dir: Path, repo_dir: Path) -> None:
    target = repo_dir / "design"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source_dir, target)
    print(f"copied design artifacts: {source_dir} -> {target}")


def write_offline_fixtures(repo_dir: Path) -> None:
    brief = "# Brief\n\n" + (
        "ArcaneOps is a SaaS dashboard for game economy operators who need "
        "to monitor player inventory, market balance, and live event health. "
    ) * 12
    design = """# Design - ArcaneOps

## Overview
ArcaneOps is a dark fantasy operations dashboard for live game teams. The
product should feel precise, magical, and command-center ready while staying
legible during repeated daily use.

## Design Tokens (from designlang extraction)
**Primary color:** #00d9ff
**Secondary color:** #e8e8f0
**Background:** #0a0a0f
**Surface:** #0d0d18
**Text primary:** #e8e8f0
**Text muted:** #9ca3af
**Accent:** #00b1ff

**Font heading:** Cinzel, 600
**Font body:** Inter, 400
**Base spacing unit:** 4px
**Border radius:** 12px

## Pages & Key Components

### Landing Page
- Hero: left-aligned command-center headline with cyan gradient CTA.
- Features section: three dense operational modules in dark surfaces.
- Pricing section: three plans with glowing primary action.
- Footer: compact product links and trust copy.

### Dashboard
- Live economy ticker, item health cards, and event-risk table.

## UX Copy
**Hero headline:** Operate your game economy with arcane precision
**Hero subheadline:** Monitor inventory, player demand, and event risk from one command surface.
**Primary CTA:** Start monitoring
**Secondary CTA:** View demo
**Pricing headline:** Scale from indie launch to live-service studio
**Empty state message:** No market signals yet.
**Error message:** Signal sync failed. Try again in a moment.

## Layout System
- Max container width: 1280px
- Column grid: 12 columns
- Nav: sticky dark surface
- Mobile breakpoint: 768px

## Component Notes
- Buttons: cyan gradient, 12px radius, sharp focus ring.
- Cards: dark violet surface, cyan glow accents, no generic borders.
- Inputs: enclosed dark fields with cyan focus treatment.
- Nav: compact left-aligned links with right-side primary CTA.

## Tone & Atmosphere
The interface should feel like a premium fantasy command room, not a generic
SaaS template. Keep contrast high and decorative effects purposeful.

## Competitor Reference
See `design/competitor-design-language.md` for extracted designlang tokens and screenshots.
Notable patterns to adopt: cyan glow, dark layered surfaces, fantasy display headings.
Notable patterns to avoid: low-contrast text, excessive ornament, random gradients.
"""
    stitch = """# STITCH Prompt - ArcaneOps

## Product Context
ArcaneOps helps game economy operators monitor inventory, market balance, and
event health. Use `design.md` as the canonical design contract for all visual,
copy, and layout decisions.

## Design Style
Style: Dark fantasy operational SaaS
Mood: precise, premium, magical, data-confident
Inspiration: designlang extraction from the competitor reference.

## Color Palette
Primary: #00d9ff
Background: #0a0a0f
Surface: #0d0d18
Text: #e8e8f0
Accent: #00b1ff

## Typography
Heading font: Cinzel 600
Body font: Inter 400

## Page to Generate: Landing Page

### Layout
Full-width dark dashboard landing with sticky navigation, dense hero, feature
modules, pricing, and compact footer. Use 1280px desktop width and responsive
stacking below 768px.

### Hero Section
Headline: "Operate your game economy with arcane precision"
Subheadline: "Monitor inventory, player demand, and event risk from one command surface."
CTA: "Start monitoring"
Visual: full-bleed dashboard surface with cyan glow accents and data cards.

### Feature Modules
Three compact modules for economy signals, item health, and event risk.

### Pricing
Three tiers with clear CTAs and dark layered cards.

## Component Specs
- Buttons: cyan gradient, 12px radius, strong hover glow.
- Cards: #0d0d18 surfaces with cyan accents and restrained shadows.
- Nav: sticky dark bar with primary CTA.

## Visual References
Use `design.md` as the canonical design contract. See screenshots in
`design/screenshots/` for component-level references from designlang.

## Output Requirements
- Full-width desktop layout (1280px)
- Include hover states on interactive elements
- Dark mode: yes
- Mobile responsive: yes
"""
    (repo_dir / "brief.md").write_text(brief)
    (repo_dir / "design.md").write_text(design)
    (repo_dir / "stitch-prompt.md").write_text(stitch)


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run the Design.md automation pipeline")
    parser.add_argument("--repo-dir", default="output/design-pipeline-dry-run", help="Target dry-run output directory")
    parser.add_argument("--design-source", default="designs", help="Existing designlang artifacts to copy")
    parser.add_argument("--name", default="ArcaneOps", help="Product name for live mode")
    parser.add_argument("--competitor-url", default="https://kingdomofarcane.com", help="Competitor URL for live mode")
    parser.add_argument("--vertical", default="Gaming", help="Vertical for live mode")
    parser.add_argument("--offline-fixture", action="store_true", help="Skip Gemini and validate deterministic fixture files")
    args = parser.parse_args()

    repo_dir = (ROOT / args.repo_dir).resolve() if not Path(args.repo_dir).is_absolute() else Path(args.repo_dir)
    design_source = (ROOT / args.design_source).resolve() if not Path(args.design_source).is_absolute() else Path(args.design_source)

    if not design_source.exists():
        sys.exit(f"Error: design source not found: {design_source}")

    repo_dir.mkdir(parents=True, exist_ok=True)
    copy_design_artifacts(design_source, repo_dir)

    env = os.environ.copy()
    if args.offline_fixture:
        write_offline_fixtures(repo_dir)
    else:
        if not env.get("GEMINI_API_KEY"):
            sys.exit("Error: GEMINI_API_KEY is required for live dry run. Use --offline-fixture for local gate testing.")
        run([
            "python3", "scripts/generate_brief.py",
            "--name", args.name,
            "--competitor-url", args.competitor_url,
            "--vertical", args.vertical,
            "--repo-dir", str(repo_dir),
        ], env=env)
        run(["python3", "scripts/agent_workflow.py", "validate-stage", "brief", "--repo-dir", str(repo_dir), "--log"], env=env)
        run(["python3", "scripts/generate_design_md.py", "--repo-dir", str(repo_dir)], env=env)
        run(["python3", "scripts/agent_workflow.py", "validate-stage", "design_md", "--repo-dir", str(repo_dir), "--log"], env=env)
        run(["python3", "scripts/generate_stitch_prompt.py", "--repo-dir", str(repo_dir)], env=env)

    run(["python3", "scripts/agent_workflow.py", "validate-stage", "design_md", "--repo-dir", str(repo_dir), "--log"], env=env)
    run(["python3", "scripts/agent_workflow.py", "validate-stage", "stitch_prompt", "--repo-dir", str(repo_dir), "--log"], env=env)
    print(f"\nDry run complete: {repo_dir}")


if __name__ == "__main__":
    main()
