#!/bin/bash
# setup-skills.sh - Wire up skills for all AI platforms
# Creates symlinks from tool-specific folders to canonical skills/
# Works from anywhere - finds repo root automatically

set -e

# Find repo root (where skills/ folder lives)
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"
SKILLS_DIR="skills"

if [ ! -d "$SKILLS_DIR" ]; then
    echo "No skills/ folder found at $REPO_ROOT"
    exit 1
fi

# Count skills
SKILL_COUNT=$(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')

if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "No skills found in $SKILLS_DIR/"
    exit 0
fi

echo "Setting up $SKILL_COUNT skill(s)..."
echo ""

# Claude Code
mkdir -p .claude/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".claude/skills/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".claude/skills/$skill_name"
done
echo "  Claude Code:      .claude/skills/"

# GitHub Copilot
mkdir -p .github/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".github/skills/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".github/skills/$skill_name"
done
echo "  GitHub Copilot:   .github/skills/"

# OpenAI Codex
mkdir -p .codex/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".codex/skills/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".codex/skills/$skill_name"
done
echo "  OpenAI Codex:     .codex/skills/"

# Antigravity IDE (workflows)
mkdir -p .agent/workflows
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".agent/workflows/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".agent/workflows/$skill_name"
done
echo "  Antigravity:      .agent/workflows/"

echo ""
echo "Skills linked for all platforms"
echo "Source: $REPO_ROOT/skills/"
