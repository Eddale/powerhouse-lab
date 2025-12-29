# Portable Skills Architecture - Build Plan

## Overview
Create a portable skills library that works across Claude Code, GitHub Copilot, OpenAI Codex, Antigravity IDE, and Claude.ai - with a single source of truth and automated distribution.

---

## The Architecture

```
powerhouse-lab/
├── skills/                              # SOURCE OF TRUTH
│   ├── README.md                        # How to use/contribute
│   ├── newsletter-coach/
│   │   └── SKILL.md
│   └── [future skills...]
│
├── .claude/skills/       → symlinks to skills/   (Claude Code)
├── .github/skills/       → symlinks to skills/   (GitHub Copilot)
├── .codex/skills/        → symlinks to skills/   (OpenAI Codex)
├── .agent/workflows/     → symlinks to skills/   (Antigravity IDE)
│
├── dist/                                # DISTRIBUTION
│   └── skills-bundle.zip                # For Claude.ai upload
│
└── scripts/
    ├── setup-skills.sh                  # Creates symlinks for all platforms
    └── package-skills.sh                # Creates ZIP for Claude.ai
```

---

## SKILL CREATION CHECKLIST (The Daily Workflow)

Use this every time you create a new skill:

### Step 1: Git Hygiene (Before You Start)
```bash
cd ~/Documents/GitHub/powerhouse-lab
git checkout main
git pull origin main
git checkout -b skill/skill-name-here
```
**Why:** Fresh branch from latest main = no conflicts later.

### Step 2: Create the Skill Folder
```bash
mkdir -p skills/skill-name-here
```
**Why:** All skills live in `skills/` - this is your single source of truth.

### Step 3: Write the SKILL.md
Create `skills/skill-name-here/SKILL.md` with:
```yaml
---
name: skill-name-here
description: What this does and when to use it. Include trigger words users would say.
allowed-tools: Read, Glob, Grep
---

# Skill Name

[Your instructions here]
```

**The description is critical.** AI tools read this to decide when to activate your skill.
- Good: "Writing coach that turns daily experiences into newsletter drafts. Use when brainstorming newsletter ideas or writing content."
- Bad: "Helps with writing."

### Step 4: Wire It Up (Run Once)
```bash
./scripts/setup-skills.sh
```
**What happens:** Creates symlinks so Claude Code, Copilot, Codex, and Antigravity all see your skill.

### Step 5: Test the Skill
- Open a new Claude Code session
- Ask Claude "What skills are available?"
- Try a prompt that should trigger your skill
- Iterate on the SKILL.md until it works

### Step 6: Commit and Push
```bash
git add skills/skill-name-here/
git commit -m "feat: Add skill-name-here skill"
git push -u origin skill/skill-name-here
```

### Step 7: Merge to Main
```bash
git checkout main
git pull origin main
git merge skill/skill-name-here
git push origin main
```
**Why:** Skills on main = available everywhere.

### Step 8: Update Claude.ai (If Needed)
```bash
./scripts/package-skills.sh
```
Then upload `dist/skills-bundle.zip` to Claude.ai → Settings → Features.

---

## WHAT THE SCRIPTS DO (Plain English)

### setup-skills.sh - "Wire It Up"
**Analogy:** Like setting up call forwarding so all phone lines ring the same phone.

1. Creates folders each AI tool expects (`.claude/`, `.github/`, `.codex/`, `.agent/`)
2. Creates symlinks (shortcuts) pointing to your real `skills/` folder
3. Now all tools see the same skills - edit once, works everywhere

**Run when:** First time setup, or after adding a new skill folder.

### package-skills.sh - "Bundle for Web"
**Analogy:** Like exporting your swipe file as a PDF to email to a client.

1. Grabs all skills from `skills/` folder
2. Zips them into `dist/skills-bundle.zip`
3. You upload this to Claude.ai manually

**Run when:** You want to update skills on Claude.ai web client.

---

## Phase 1: Foundation

### 1.1 Create canonical skills/ structure
- [x] Move `.claude/skills/newsletter-coach/` → `skills/newsletter-coach/`
- [x] Update `skills/README.md` with usage instructions
- [x] Verify SKILL.md has proper YAML frontmatter format

### 1.2 Create setup-skills.sh
```bash
#!/bin/bash
# Creates symlinks from tool-specific folders to canonical skills/
# Works from anywhere - finds repo root automatically

# Find repo root (where skills/ folder lives)
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "❌ Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"
SKILLS_DIR="skills"

if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ No skills/ folder found at $REPO_ROOT"
    exit 1
fi

# Claude Code
mkdir -p .claude/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".claude/skills/$skill_name"  # Remove old symlink if exists
    ln -sf "../../$SKILLS_DIR/$skill_name" ".claude/skills/$skill_name"
done

# GitHub Copilot
mkdir -p .github/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".github/skills/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".github/skills/$skill_name"
done

# OpenAI Codex
mkdir -p .codex/skills
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".codex/skills/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".codex/skills/$skill_name"
done

# Antigravity IDE (workflows)
mkdir -p .agent/workflows
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill")
    rm -f ".agent/workflows/$skill_name"
    ln -sf "../../$SKILLS_DIR/$skill_name" ".agent/workflows/$skill_name"
done

echo "✅ Skills linked for Claude Code, GitHub Copilot, OpenAI Codex, and Antigravity"
echo "📁 Source: $REPO_ROOT/skills/"
```

### 1.3 Create package-skills.sh
```bash
#!/bin/bash
# Packages skills into ZIP for Claude.ai upload
# Works from anywhere - finds repo root automatically

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "❌ Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"

if [ ! -d "skills" ]; then
    echo "❌ No skills/ folder found"
    exit 1
fi

mkdir -p dist
rm -f dist/skills-bundle.zip

# Create ZIP with each skill as a folder
cd skills
zip -r ../dist/skills-bundle.zip */ -x "*.DS_Store" -x "README.md"
cd ..

echo "✅ Created dist/skills-bundle.zip"
echo "📁 Location: $REPO_ROOT/dist/skills-bundle.zip"
echo ""
echo "📤 To install on Claude.ai:"
echo "   1. Go to claude.ai"
echo "   2. Settings → Features"
echo "   3. Upload the ZIP file"
```

---

## Phase 2: Template Update

### 2.1 Update _templates/skill-template/SKILL.md
- [ ] Add YAML frontmatter with `name`, `description`, `allowed-tools`
- [ ] Keep existing documentation structure below the frontmatter
- [ ] Add notes about portability requirements

**New template format:**
```yaml
---
name: skill-name-here
description: What this skill does and when to use it. Be specific about trigger words.
allowed-tools: Read, Glob, Grep
---

# [SKILL NAME]

## What This Does
<!-- One sentence, benefit-driven -->

[...rest of existing template...]
```

---

## Phase 3: Verification

### 3.1 Run setup and verify
- [x] Run `./scripts/setup-skills.sh`
- [x] Verify symlinks created correctly
- [ ] Test that Claude Code discovers the skill

### 3.2 Generate and test ZIP
- [x] Run `./scripts/package-skills.sh`
- [x] Verify `dist/skills-bundle.zip` contents
- [x] Document Claude.ai upload process

---

## Phase 4: Documentation

### 4.1 Update skills/README.md
- [ ] Explain the portable architecture
- [ ] Document how to add new skills
- [ ] Document how to run setup for different platforms
- [ ] Document Claude.ai upload process

### 4.2 Client distribution notes
- [ ] How clients would clone/fork the skills
- [ ] How to customize for their business
- [ ] Platform-specific setup instructions

---

## Phase 5: Update New Prototype Workflow

### 5.1 Update `.agent/workflows/new-prototype.md`
The existing workflow creates prototypes but doesn't wire up skills. Update it to:
- [ ] After folder setup, run `./scripts/setup-skills.sh` to ensure symlinks exist
- [ ] Add note about skill creation vs prototype creation (different workflows)

**Decision:** Should prototypes have access to skills automatically?
- YES: Run setup-skills.sh as part of new-prototype workflow
- NO: Keep prototypes isolated, only wire skills when ready

**Note:** The new-prototype workflow is for creating tool/app prototypes. Skills have their own simpler workflow (see checklist above).

---

## Files Changed

| Action | File |
|--------|------|
| MOVE | `.claude/skills/newsletter-coach/` → `skills/newsletter-coach/` |
| CREATE | `scripts/setup-skills.sh` |
| CREATE | `scripts/package-skills.sh` |
| CREATE | `dist/skills-bundle.zip` (generated) |
| UPDATE | `_templates/skill-template/SKILL.md` |
| UPDATE | `skills/README.md` |
| CREATE | `.claude/skills/newsletter-coach` (symlink) |
| CREATE | `.github/skills/newsletter-coach` (symlink) |
| CREATE | `.codex/skills/newsletter-coach` (symlink) |

---

## Success Criteria

- [ ] `skills/` contains the canonical SKILL.md files
- [ ] Symlinks work for Claude Code (`.claude/skills/`)
- [ ] Symlinks work for GitHub Copilot (`.github/skills/`)
- [ ] Symlinks work for OpenAI Codex (`.codex/skills/`)
- [ ] ZIP file can be uploaded to Claude.ai
- [ ] Adding a new skill = add to `skills/`, run setup script, done
- [ ] Template updated so new skills follow the portable format

---

## Review
<!-- Add notes here upon completion -->
