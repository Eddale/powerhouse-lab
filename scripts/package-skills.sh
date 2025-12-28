#!/bin/bash
# package-skills.sh - Bundle skills for Claude.ai upload
# Creates a ZIP file containing all skills for web client upload
# Works from anywhere - finds repo root automatically

set -e

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"

if [ ! -d "skills" ]; then
    echo "No skills/ folder found"
    exit 1
fi

# Count skills
SKILL_COUNT=$(find "skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')

if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "No skills found to package"
    exit 0
fi

mkdir -p dist
rm -f dist/skills-bundle.zip

# Create ZIP with each skill as a folder
cd skills
zip -r ../dist/skills-bundle.zip */ -x "*.DS_Store" -x "README.md"
cd ..

echo ""
echo "Created dist/skills-bundle.zip"
echo "Contains $SKILL_COUNT skill(s)"
echo ""
echo "To install on Claude.ai:"
echo "  1. Go to claude.ai"
echo "  2. Click your profile -> Settings"
echo "  3. Go to Features section"
echo "  4. Upload dist/skills-bundle.zip"
