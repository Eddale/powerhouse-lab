#!/bin/bash
# package-skill.sh - Package a single skill for Claude.ai upload
# Usage: ./scripts/package-skill.sh <skill-name>
# Output: dist/<skill-name>.zip

set -e

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"

# Check for skill name argument
if [ -z "$1" ]; then
    echo "Usage: ./scripts/package-skill.sh <skill-name>"
    echo ""
    echo "Available skills:"
    for skill in skills/*/; do
        if [ -f "${skill}SKILL.md" ]; then
            echo "  - $(basename "$skill")"
        fi
    done
    exit 1
fi

SKILL_NAME="$1"
SKILL_PATH="skills/$SKILL_NAME"

# Verify skill exists
if [ ! -d "$SKILL_PATH" ]; then
    echo "Error: Skill '$SKILL_NAME' not found in skills/"
    exit 1
fi

if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
    echo "Error: No SKILL.md found in $SKILL_PATH"
    exit 1
fi

# Create dist folder
mkdir -p dist

# Remove old ZIP if exists
rm -f "dist/$SKILL_NAME.zip"

# Create ZIP with skill folder at root (Claude.ai requirement)
# We zip FROM the skills directory so the skill folder is at root level
cd skills
zip -r "../dist/$SKILL_NAME.zip" "$SKILL_NAME" -x "*.DS_Store" -x "*/.git/*"
cd ..

echo ""
echo "Created: dist/$SKILL_NAME.zip"
echo ""
echo "To upload to Claude.ai:"
echo "  1. Go to claude.ai"
echo "  2. Click your profile -> Settings"
echo "  3. Go to Features section"
echo "  4. Upload dist/$SKILL_NAME.zip"
echo "  5. Toggle the skill ON"
