"""
render_templates.py — Jinja2 template renderer for the SaaS Creator pipeline.

Usage:
    python scripts/render_templates.py DESIGN.md
    python scripts/render_templates.py REQUIREMENTS.md
    python scripts/render_templates.py deploy.yml

Reads design_tokens.json (for DESIGN.md) or a context JSON file,
renders the matching Jinja2 template from the templates/ directory,
and writes the output to the project root.
"""

import os
import sys
import json
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    print("Error: jinja2 is not installed. Run: pip install jinja2")
    sys.exit(1)


TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
TOKENS_FILE = Path("design_tokens.json")
REFERENCE_DIR = Path(__file__).parent.parent / "reference"

TEMPLATE_MAP = {
    "DESIGN.md": "DESIGN.md.j2",
    "REQUIREMENTS.md": "REQUIREMENTS.md.j2",
    "deploy.yml": "deploy.yml.j2",
}


def load_tokens() -> dict:
    """Load design tokens from design_tokens.json, falling back to the reference schema."""
    if TOKENS_FILE.exists():
        with open(TOKENS_FILE) as f:
            raw = json.load(f)
    else:
        fallback = REFERENCE_DIR / "stitch_schema.json"
        print(f"Warning: {TOKENS_FILE} not found. Using reference schema from {fallback}")
        with open(fallback) as f:
            raw = json.load(f)

    tokens = raw.get("tokens", [])
    colors = [t for t in tokens if t.get("type") == "color"]
    typography = [t for t in tokens if t.get("type") == "typography"]
    spacing = [t for t in tokens if t.get("type") == "spacing"]

    return {
        "colors": [{"name": t["id"], "hex": t["value"], "usage": t.get("metadata", {}).get("usage", "")} for t in colors],
        "typography": [{"role": t["id"], "family": t["value"], "size": t.get("metadata", {}).get("size", ""), "weight": t.get("metadata", {}).get("weight", "")} for t in typography],
        "components": [{"stitch_id": t["id"], "name": t.get("metadata", {}).get("react_name", t["id"])} for t in tokens if t.get("type") == "component"],
        "layout": {
            "max_width": next((t["value"] for t in spacing if t["id"] == "container-max-width"), "1280px"),
            "gutter": next((t["value"] for t in spacing if t["id"] == "grid-gutter"), "24px"),
        },
    }


def load_context(target: str) -> dict:
    """Build the Jinja2 render context for a given target document."""
    base = {
        "project_name": os.environ.get("PROJECT_NAME", "My SaaS App"),
    }

    if target == "DESIGN.md":
        return {**base, **load_tokens()}

    if target == "REQUIREMENTS.md":
        return {
            **base,
            "product_vision": os.environ.get("PRODUCT_VISION", ""),
            "user_stories": [],
            "frontend_stack": os.environ.get("FRONTEND_STACK", "React / Next.js with Tailwind CSS"),
            "backend_stack": os.environ.get("BACKEND_STACK", "Firebase Functions (Node.js)"),
            "database_stack": os.environ.get("DATABASE_STACK", "Cloud Firestore"),
            "features": [],
            "success_metrics": os.environ.get("SUCCESS_METRICS", ""),
        }

    if target == "deploy.yml":
        return {
            **base,
            "production_branch": os.environ.get("PRODUCTION_BRANCH", "main"),
            "node_version": os.environ.get("NODE_VERSION", "20"),
            "project_id": os.environ.get("FIREBASE_PROJECT_ID", "my-saas-app"),
            "deploy_hostinger": os.environ.get("DEPLOY_HOSTINGER", "false").lower() == "true",
        }

    return base


def render(target: str) -> None:
    template_name = TEMPLATE_MAP.get(target)
    if not template_name:
        print(f"Error: No template found for '{target}'. Known targets: {list(TEMPLATE_MAP.keys())}")
        sys.exit(1)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    try:
        template = env.get_template(template_name)
    except Exception as e:
        print(f"Error loading template {template_name}: {e}")
        sys.exit(1)

    context = load_context(target)

    try:
        output = template.render(**context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)

    output_path = Path(target)
    output_path.write_text(output)
    print(f"Rendered: {template_name} → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_templates.py <target>")
        print(f"Targets: {list(TEMPLATE_MAP.keys())}")
        sys.exit(1)

    render(sys.argv[1])
