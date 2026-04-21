"""
extract_dna.py — Stitch MCP Design DNA Extractor
=================================================
Connects to the Stitch MCP proxy server via JSON-RPC and pulls:
  • Project metadata & design theme (47 named colors, fonts, roundness)
  • All screens (name, title, screenshot URL)
  • Design systems (tokens, designMd documentation)

Output: design_tokens.json — the canonical Design DNA consumed by render_templates.py

MCP Endpoint: set STITCH_MCP_ENDPOINT in .env
API Key:      set STITCH_API_KEY in .env
"""

import json
import os
import sys
import time
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

STITCH_MCP_ENDPOINT = os.environ.get("STITCH_MCP_ENDPOINT", "http://136.111.153.224:8080")
STITCH_API_KEY = os.environ.get("STITCH_API_KEY", "")

RETRY_ATTEMPTS = 3
RETRY_BACKOFF_BASE = 1.5   # seconds; doubles each retry
REQUEST_TIMEOUT = 30       # seconds per call


# ---------------------------------------------------------------------------
# MCP JSON-RPC transport
# ---------------------------------------------------------------------------

def _mcp_call(tool_name: str, arguments: dict, call_id: int = 1) -> dict:
    """
    Invoke a Stitch MCP tool via JSON-RPC 2.0.
    Returns the parsed result dict, or raises on error.
    """
    headers = {"Content-Type": "application/json"}
    if STITCH_API_KEY:
        headers["Authorization"] = f"Bearer {STITCH_API_KEY}"

    payload = {
        "jsonrpc": "2.0",
        "id": call_id,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }

    url = f"{STITCH_MCP_ENDPOINT}/message"

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            body = resp.json()

            # JSON-RPC error block
            if "error" in body:
                raise RuntimeError(f"MCP error: {body['error']}")

            result = body.get("result", {})
            if result.get("isError"):
                content_text = result.get("content", [{}])[0].get("text", "unknown error")
                raise RuntimeError(f"Tool '{tool_name}' returned error: {content_text}")

            return result

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt == RETRY_ATTEMPTS:
                raise RuntimeError(
                    f"Could not reach Stitch MCP at {url} after {RETRY_ATTEMPTS} attempts: {e}"
                ) from e
            wait = RETRY_BACKOFF_BASE ** attempt
            print(f"  [retry {attempt}/{RETRY_ATTEMPTS}] connection error — waiting {wait:.1f}s …")
            time.sleep(wait)
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP {resp.status_code} from Stitch MCP: {e}") from e


def _parse_content_json(result: dict) -> dict:
    """Extract and parse the first content[].text as JSON from an MCP result."""
    content = result.get("content", [])
    for item in content:
        text = item.get("text", "")
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
    return {}


# ---------------------------------------------------------------------------
# Stitch tool wrappers
# ---------------------------------------------------------------------------

def get_project(project_id: str) -> dict:
    print(f"  → get_project (id={project_id})")
    result = _mcp_call("get_project", {"name": f"projects/{project_id}"}, call_id=1)
    return _parse_content_json(result)


def list_screens(project_id: str) -> list:
    print(f"  → list_screens (project={project_id})")
    result = _mcp_call("list_screens", {"projectId": project_id}, call_id=2)
    data = _parse_content_json(result)
    return data.get("screens", [])


def list_design_systems(project_id: str) -> list:
    print(f"  → list_design_systems (project={project_id})")
    result = _mcp_call("list_design_systems", {"projectId": project_id}, call_id=3)
    data = _parse_content_json(result)
    return data.get("designSystems", [])


# ---------------------------------------------------------------------------
# Design DNA assembly
# ---------------------------------------------------------------------------

def _build_color_palette(named_colors: dict) -> dict:
    """
    Return a structured subset of named colors suitable for template rendering.
    Groups: brand, surface, semantic, text, outline.
    """
    groups = {
        "brand": ["primary", "secondary", "tertiary", "primary_container",
                  "secondary_container", "tertiary_container"],
        "surface": ["background", "surface", "surface_bright", "surface_dim",
                    "surface_variant", "surface_container", "surface_container_low",
                    "surface_container_lowest", "surface_container_high",
                    "surface_container_highest"],
        "semantic": ["error", "error_container", "on_error", "on_error_container"],
        "text": ["on_background", "on_surface", "on_surface_variant", "on_primary",
                 "on_secondary", "on_tertiary", "on_primary_container",
                 "on_secondary_container", "on_tertiary_container"],
        "outline": ["outline", "outline_variant"],
    }
    palette = {}
    for group, keys in groups.items():
        palette[group] = {k: named_colors[k] for k in keys if k in named_colors}
    palette["all"] = named_colors
    return palette


def _build_typography(theme: dict) -> dict:
    return {
        "headline": theme.get("headlineFont", theme.get("font", "SYSTEM")),
        "body": theme.get("bodyFont", theme.get("font", "SYSTEM")),
        "label": theme.get("labelFont", theme.get("font", "SYSTEM")),
        "general": theme.get("font", "SYSTEM"),
    }


def _build_design_dna(project: dict, screens: list, design_systems: list) -> dict:
    theme = project.get("designTheme", {})
    named_colors = theme.get("namedColors", {})

    # Pick the first design system's documentation if present
    ds_doc = ""
    ds_name = ""
    if design_systems:
        ds = design_systems[0]
        ds_name = ds.get("designSystem", {}).get("displayName", "")
        ds_doc = ds.get("designSystem", {}).get("theme", {}).get("designMd", "")

    return {
        "project": {
            "id": project.get("name", "").split("/")[-1],
            "title": project.get("title", ""),
            "device_type": project.get("deviceType", "MOBILE"),
            "visibility": project.get("visibility", "PRIVATE"),
            "origin": project.get("origin", "STITCH"),
        },
        "design_system": {
            "name": ds_name,
            "documentation": ds_doc,
        },
        "theme": {
            "color_mode": theme.get("colorMode", "LIGHT"),
            "roundness": theme.get("roundness", "ROUND_NONE"),
            "custom_color": theme.get("customColor", ""),
        },
        "typography": _build_typography(theme),
        "colors": _build_color_palette(named_colors),
        "screens": [
            {
                "id": s.get("name", "").split("/")[-1],
                "title": s.get("title", ""),
                "name": s.get("name", ""),
            }
            for s in screens
        ],
        "_meta": {
            "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": "stitch-mcp",
            "endpoint": STITCH_MCP_ENDPOINT,
        },
    }


# ---------------------------------------------------------------------------
# Fallback
# ---------------------------------------------------------------------------

def _load_fallback(fallback_path: str) -> dict:
    """Load stitch_schema.json as a fallback when the MCP is unreachable."""
    if os.path.exists(fallback_path):
        with open(fallback_path) as f:
            data = json.load(f)
        print(f"  [fallback] Loaded local schema from {fallback_path}")
        return data
    return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_tokens(project_id: str, output_path: str = "design_tokens.json") -> dict:
    """
    Pull design DNA from Stitch MCP and write to output_path.
    Falls back to reference/stitch_schema.json if MCP is unreachable.

    Returns the assembled design DNA dict.
    """
    fallback_path = os.path.join(
        os.path.dirname(__file__), "..", "reference", "stitch_schema.json"
    )

    print(f"Connecting to Stitch MCP at {STITCH_MCP_ENDPOINT} …")

    try:
        project = get_project(project_id)
        if not project:
            raise RuntimeError("get_project returned empty response")

        screens = list_screens(project_id)
        design_systems = list_design_systems(project_id)

    except RuntimeError as e:
        print(f"\n  [warning] Stitch MCP unavailable: {e}")
        fallback = _load_fallback(fallback_path)
        if not fallback:
            print("  [error] No fallback schema found. Aborting.")
            sys.exit(1)
        return fallback

    dna = _build_design_dna(project, screens, design_systems)

    with open(output_path, "w") as f:
        json.dump(dna, f, indent=2)

    print(
        f"\n✓ Design DNA extracted:"
        f"\n  project : {dna['project']['title']}"
        f"\n  screens : {len(dna['screens'])}"
        f"\n  colors  : {len(dna['colors'].get('all', {}))}"
        f"\n  fonts   : {dna['typography']}"
        f"\n  saved → {output_path}"
    )
    return dna


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_dna.py <stitch_project_id> [output_path]")
        print("")
        print("Environment variables:")
        print("  STITCH_MCP_ENDPOINT  MCP proxy URL (default: http://136.111.153.224:8080)")
        print("  STITCH_API_KEY       API key for the MCP server")
        sys.exit(1)

    project_id = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "design_tokens.json"
    extract_tokens(project_id, out)
