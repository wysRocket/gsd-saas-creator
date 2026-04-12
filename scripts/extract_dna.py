import os
import requests
import json
import sys

STITCH_API_KEY = os.environ.get("STITCH_API_KEY")
STITCH_API_BASE = os.environ.get("STITCH_API_BASE", "https://stitch.google.com/api/v1")


def extract_tokens(project_id: str, output_path: str = "design_tokens.json") -> dict:
    """
    Extracts design tokens from a Google Stitch project via the Stitch API.

    Requires STITCH_API_KEY environment variable to be set.
    """
    if not STITCH_API_KEY:
        print("Error: STITCH_API_KEY environment variable is not set.")
        print("Copy .env.example to .env and fill in your API key.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {STITCH_API_KEY}",
        "Content-Type": "application/json",
    }

    url = f"{STITCH_API_BASE}/projects/{project_id}/tokens"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        tokens = response.json()

        with open(output_path, "w") as f:
            json.dump(tokens, f, indent=2)

        print(f"Successfully extracted {len(tokens.get('tokens', []))} tokens to {output_path}")
        return tokens

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from Stitch API: {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to Stitch API at {STITCH_API_BASE}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_dna.py <stitch_project_id> [output_path]")
        sys.exit(1)

    project_id = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "design_tokens.json"
    extract_tokens(project_id, out)
