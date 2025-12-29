# Skills Library

Portable AI skills that work across Claude Code, GitHub Copilot, OpenAI Codex, Antigravity IDE, and Claude.ai.

---

## FROM IDEA TO DEPLOYED SKILL (Step by Step)

Use this every time you create a new skill.

### 1. START CLEAN

Open terminal and run:
```bash
cd ~/Documents/GitHub/powerhouse-lab
git checkout main
git pull origin main
git checkout -b skill/my-skill-name
```

**What this does:** Gets you the latest code and creates a fresh branch for your work. This prevents merge conflicts later.

**Plain English:** You're opening a new blank page that's based on the latest version of everything.

---

### 2. CREATE THE SKILL FOLDER

```bash
mkdir -p skills/my-skill-name/{scripts,references,resources,assets}
touch skills/my-skill-name/{scripts,references,resources,assets}/.gitkeep
```

**What this does:** Creates a new folder for your skill with all optional subdirectories.

**Folder structure:**
```
skills/my-skill-name/
├── SKILL.md        # Required - the skill instructions
├── scripts/        # Optional - executable Python/Bash
├── references/     # Optional - docs Claude loads when needed
├── resources/      # Optional - templates and data files
└── assets/         # Optional - binary files, images, logos
```

**Plain English:** You're creating a filing cabinet with labeled drawers, ready for future expansion.

---

### 3. WRITE THE SKILL FILE

Create a file called `SKILL.md` inside your new folder. You can do this in your IDE or with:
```bash
touch skills/my-skill-name/SKILL.md
```

Then open it and paste this template:

```yaml
---
name: my-skill-name
description: What this skill does and when to use it. Include words users would naturally say when they need this skill. Max 1024 characters.
allowed-tools: Read, Glob, Grep
---

# My Skill Name

## What This Does
One sentence explaining the benefit.

## Instructions
Step-by-step guidance for Claude to follow when this skill is activated.

1. First, do this...
2. Then do this...
3. Finally...

## Examples
Show what good output looks like.

## Guidelines
- Important rule 1
- Important rule 2
```

**The `description` is the most important part.** This is what AI tools read to decide whether to activate your skill. Include trigger words users would naturally say.

**Good description:** "Writing coach that turns daily experiences into newsletter drafts. Use when brainstorming newsletter ideas, writing content for The Little Blue Report, or turning experiences into articles."

**Bad description:** "Helps with writing."

---

### 4. WIRE IT UP

```bash
./scripts/setup-skills.sh
```

**What this does:** Creates shortcuts (symlinks) so Claude Code, GitHub Copilot, OpenAI Codex, and Antigravity can all find your skill.

**Plain English:** You're telling all the AI tools "hey, there's a new skill over here."

---

### 5. TEST IT

1. Open a new Claude Code session (or refresh your current one)
2. Ask: "What skills are available?"
3. Try a prompt that should trigger your skill
4. If it doesn't work right, edit the SKILL.md and try again

**Keep iterating until it works the way you want.**

---

### 6. SAVE YOUR WORK

```bash
git add skills/my-skill-name/
git commit -m "feat: Add my-skill-name skill"
git push -u origin skill/my-skill-name
```

**What this does:** Saves your skill to GitHub on your feature branch.

**Plain English:** You're saving a snapshot of your work and backing it up to the cloud.

---

### 7. MERGE TO MAIN

```bash
git checkout main
git pull origin main
git merge skill/my-skill-name
git push origin main
```

**What this does:** Merges your skill into the main codebase so it's available everywhere.

**Plain English:** You're publishing your skill so it's part of the official collection.

---

### 8. DISTRIBUTE TO CLAUDE.AI (Optional)

If you use Claude.ai web client:

**Package a single skill:**
```bash
./scripts/package-skill.sh my-skill-name
```

**Or package all skills at once:**
```bash
./scripts/package-all-skills.sh
```

Then for EACH skill:
1. Go to claude.ai
2. Click your profile -> Settings
3. Go to Features section
4. Upload `dist/my-skill-name.zip`
5. Toggle the skill ON

**Important:** Claude.ai requires individual skill uploads (one ZIP per skill). You cannot upload a bundle of multiple skills.

**What this does:** Creates a ZIP file for each skill, formatted for Claude.ai upload.

**Plain English:** You're exporting each skill as its own package, then uploading them one at a time.

---

## QUICK REFERENCE

| Step | Command | What It Does |
|------|---------|--------------|
| Start clean | `git checkout main && git pull && git checkout -b skill/name` | Fresh branch from latest |
| Create folder | `mkdir -p skills/name/{scripts,references,resources,assets}` | New skill directory with all folders |
| Wire up | `./scripts/setup-skills.sh` | Link to all AI tools |
| Test | Ask Claude "What skills are available?" | Verify it works |
| Save | `git add . && git commit -m "feat: Add name skill"` | Commit your work |
| Publish | `git checkout main && git merge skill/name && git push` | Make it official |
| Package one | `./scripts/package-skill.sh name` | Create ZIP for one skill |
| Package all | `./scripts/package-all-skills.sh` | Create ZIPs for all skills |

---

## HOW IT WORKS (The Plumbing)

```
skills/                    <- You edit here (source of truth)
   |
   +-> .claude/skills/     <- Claude Code reads here (symlink)
   +-> .github/skills/     <- GitHub Copilot reads here (symlink)
   +-> .codex/skills/      <- OpenAI Codex reads here (symlink)
   +-> .agent/workflows/   <- Antigravity reads here (symlink)
   +-> dist/<skill>.zip    <- Claude.ai upload (one ZIP per skill)
```

**One source, multiple destinations.** Edit a skill once, all tools see the change.

---

## CURRENT SKILLS

| Skill | Description |
|-------|-------------|
| [newsletter-coach](newsletter-coach/) | Writing coach that turns daily experiences into newsletter drafts |
| [new-skill-wizard](new-skill-wizard/) | Automates skill creation - just say "create a new skill called X" |
| [mission-context](mission-context/) | Ed's business context, terminology, and mission |

---

## UPDATING AN EXISTING SKILL

When you need to improve or modify a skill:

### The Easy Way (Just Ask)

Say: "Update my mission-context skill to include..." or "Add X to the newsletter-coach skill"

I'll edit the SKILL.md file directly and handle the git workflow.

### The Manual Way

1. **Edit the file directly** in `skills/skill-name/SKILL.md`
2. **Test it** - refresh your session and try triggering the skill
3. **Commit and push:**
   ```bash
   git add skills/skill-name/
   git commit -m "update: Improve skill-name skill"
   git push
   ```
4. **Update Claude.ai** (if needed): `./scripts/package-skill.sh skill-name` and re-upload

### Using Antigravity IDE Comments

If you're in Antigravity:
1. Open the SKILL.md file
2. Select the text you want to change
3. Add a Google Docs-style comment with your edit
4. The agent incorporates your feedback

---

## THE AUTOMATED WAY (Recommended)

Instead of running terminal commands, just tell Claude:

**To create a new skill:**
> "I want to create a new skill called brand-voice"

**To update a skill:**
> "Update my mission-context to include my new terminology"

**To publish to Claude.ai:**
> "Package my skills for Claude.ai"

The `new-skill-wizard` skill handles all the git workflow automatically.

---

## FOR CLIENTS

To use these skills in your own projects:

1. Clone/fork this repository
2. Run `./scripts/setup-skills.sh`
3. For Claude.ai: Run `./scripts/package-all-skills.sh` and upload each ZIP individually

You can add your own skills to the `skills/` folder following the same pattern.
