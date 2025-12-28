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
mkdir -p skills/my-skill-name
```

**What this does:** Creates a new folder for your skill inside the `skills/` directory.

**Plain English:** You're creating a new drawer in the filing cabinet for this skill.

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

```bash
./scripts/package-skills.sh
```

Then:
1. Go to claude.ai
2. Click your profile -> Settings
3. Go to Features section
4. Upload `dist/skills-bundle.zip`

**What this does:** Creates a ZIP file containing all your skills, formatted for Claude.ai upload.

**Plain English:** You're exporting your skills library so you can use it in the web browser version of Claude.

---

## QUICK REFERENCE

| Step | Command | What It Does |
|------|---------|--------------|
| Start clean | `git checkout main && git pull && git checkout -b skill/name` | Fresh branch from latest |
| Create folder | `mkdir -p skills/name` | New skill directory |
| Wire up | `./scripts/setup-skills.sh` | Link to all AI tools |
| Test | Ask Claude "What skills are available?" | Verify it works |
| Save | `git add . && git commit -m "feat: Add name skill"` | Commit your work |
| Publish | `git checkout main && git merge skill/name && git push` | Make it official |
| Web export | `./scripts/package-skills.sh` | Create ZIP for Claude.ai |

---

## HOW IT WORKS (The Plumbing)

```
skills/                    <- You edit here (source of truth)
   |
   +-> .claude/skills/     <- Claude Code reads here (symlink)
   +-> .github/skills/     <- GitHub Copilot reads here (symlink)
   +-> .codex/skills/      <- OpenAI Codex reads here (symlink)
   +-> .agent/workflows/   <- Antigravity reads here (symlink)
   +-> dist/skills-bundle.zip <- Claude.ai upload (generated)
```

**One source, multiple destinations.** Edit a skill once, all tools see the change.

---

## CURRENT SKILLS

| Skill | Description |
|-------|-------------|
| [newsletter-coach](newsletter-coach/) | Writing coach that turns daily experiences into newsletter drafts |

---

## FOR CLIENTS

To use these skills in your own projects:

1. Clone/fork this repository
2. Run `./scripts/setup-skills.sh`
3. For Claude.ai: Run `./scripts/package-skills.sh` and upload the ZIP

You can add your own skills to the `skills/` folder following the same pattern.
