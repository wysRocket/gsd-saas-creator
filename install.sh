#!/usr/bin/env bash
# install.sh — Install the GSD SaaS Creator skill into any Antigravity project.
#
# Usage:
#   curl -sSL <repo-raw-url>/install.sh | bash
#   OR clone the repo and run: ./install.sh [target_dir]
#
# The script copies the skill into .agents/skills/saas-creator/ and the
# workflow command into .agents/workflows/ in the target directory.

set -euo pipefail

SKILL_NAME="saas-creator"
SKILL_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"
AGENTS_DIR="$TARGET_DIR/.agents"
SKILL_DEST="$AGENTS_DIR/skills/$SKILL_NAME"
WORKFLOW_DEST="$AGENTS_DIR/workflows"

echo ""
echo "GSD SaaS Creator — Skill Installer"
echo "==================================="
echo "Source : $SKILL_SOURCE"
echo "Target : $TARGET_DIR"
echo ""

# Validate target
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: target directory '$TARGET_DIR' does not exist."
  exit 1
fi

# Create .agents structure
mkdir -p "$SKILL_DEST"
mkdir -p "$WORKFLOW_DEST"

# Copy skill files
echo "Installing skill files..."
cp -r "$SKILL_SOURCE/scripts"    "$SKILL_DEST/"
cp -r "$SKILL_SOURCE/templates"  "$SKILL_DEST/"
cp -r "$SKILL_SOURCE/reference"  "$SKILL_DEST/"
cp -r "$SKILL_SOURCE/examples"   "$SKILL_DEST/"
cp    "$SKILL_SOURCE/SKILL.md"   "$SKILL_DEST/"

echo "  copied: scripts/, templates/, reference/, examples/, SKILL.md"

# Copy workflow command
cp "$SKILL_SOURCE/workflows/saas-create.md" "$WORKFLOW_DEST/"
echo "  copied: workflows/saas-create.md → .agents/workflows/"

# Copy agents.md (merge if already exists)
AGENTS_MD="$AGENTS_DIR/agents.md"
if [[ -f "$AGENTS_MD" ]]; then
  echo ""
  echo "Warning: $AGENTS_MD already exists."
  echo "The following personas from this skill need to be added manually:"
  echo "  @pm, @engineer, @qa, @devops"
  echo "Reference: $SKILL_SOURCE/agents.md"
else
  cp "$SKILL_SOURCE/agents.md" "$AGENTS_MD"
  echo "  copied: agents.md → .agents/agents.md"
fi

# Copy .env.example to project root (don't overwrite)
ENV_EXAMPLE="$TARGET_DIR/.env.example"
if [[ ! -f "$ENV_EXAMPLE" ]]; then
  cp "$SKILL_SOURCE/.env.example" "$ENV_EXAMPLE"
  echo "  copied: .env.example → project root"
else
  echo "  skipped: .env.example already exists in project root"
fi

echo ""
echo "Installation complete."
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and fill in your API keys"
echo "  2. Install Python deps: pip install jinja2 requests"
echo "  3. In Antigravity, type: /saas-create <your product idea>"
echo ""
