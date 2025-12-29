#!/bin/bash
# package-all-skills.sh - Package all skills individually for Claude.ai upload
# Creates one ZIP per skill (Claude.ai requires individual uploads)
# Output: dist/<skill-name>.zip for each skill

set -e

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"

if [ ! -d "skills" ]; then
    echo "Error: No skills/ folder found"
    exit 1
fi

# Count and list skills
SKILL_COUNT=0
SKILLS=()

for skill_dir in skills/*/; do
    if [ -f "${skill_dir}SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        SKILLS+=("$skill_name")
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done

if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "No skills found to package"
    exit 0
fi

echo "Packaging $SKILL_COUNT skill(s)..."
echo ""

# Create dist folder
mkdir -p dist

# Package each skill individually
for skill_name in "${SKILLS[@]}"; do
    rm -f "dist/$skill_name.zip"

    cd skills
    zip -r "../dist/$skill_name.zip" "$skill_name" -x "*.DS_Store" -x "*/.git/*"
    cd ..

    echo "  Created: dist/$skill_name.zip"
done

echo ""
echo "All skills packaged!"
echo ""
echo "To upload to Claude.ai:"
echo "  1. Go to claude.ai -> Settings -> Features"
echo "  2. Upload EACH zip file individually:"
for skill_name in "${SKILLS[@]}"; do
    echo "     - dist/$skill_name.zip"
done
echo "  3. Toggle each skill ON after upload"
