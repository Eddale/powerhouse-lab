---
description: Create a new skill in the Powerhouse Lab skills library. Use when the user wants to create a new skill, add a skill, or says "new skill".
---

Use this workflow when the user asks to "create a new skill", "add a skill", "new skill called X", or similar.

## 1. Get the Skill Name

If not provided, ask:
> What would you like to call this skill? Give me a short name in kebab-case (e.g., `brand-voice`, `client-intake`, `proposal-writer`).

## 2. Get the Skill Description

Ask:
> In one or two sentences, what does this skill do? And when should I use it?
>
> Example: "Helps write client proposals. Use when creating proposals, quotes, or project scopes."

## 3. Git Preparation

```bash
cd ~/Documents/GitHub/powerhouse-lab
git checkout main
git pull origin main
git checkout -b skill/<name>
```

Confirm: "Created branch `skill/<name>` from latest main."

## 4. Create Skill Folder and File

```bash
mkdir -p skills/<name>
```

Create `skills/<name>/SKILL.md` with:

```yaml
---
name: <name>
description: <user's description>. Use when <trigger phrases>.
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# <Name in Title Case>

## What This Does
<One sentence benefit>

## Instructions

[To be developed with user]

## Examples

[To be added]

## Guidelines

- Guideline 1
- Guideline 2
```

## 5. Wire Up the Skill

```bash
./scripts/setup-skills.sh
```

Confirm: "Skill wired up for Claude Code, GitHub Copilot, OpenAI Codex, and Antigravity."

## 6. Develop the Skill Content

Ask:
> Now let's build out the instructions. What should I do when this skill is activated?
>
> - What's the step-by-step process?
> - Any specific rules or guidelines?
> - What does good output look like?

Work with the user to fill in the Instructions, Examples, and Guidelines sections.

## 7. Test the Skill

Tell the user:
> The skill is ready to test. In a new Claude Code session, try:
> 1. Ask "What skills are available?" to verify it shows up
> 2. Try a prompt that should trigger it
>
> Let me know if it needs adjustments.

## 8. Save and Publish (When Ready)

Once the user confirms the skill works:

```bash
git add skills/<name>/
git commit -m "feat: Add <name> skill"
git push -u origin skill/<name>
git checkout main
git pull origin main
git merge skill/<name>
git push origin main
```

Confirm: "Skill `<name>` is now live on main."

## 9. Update Claude.ai (Optional)

Ask:
> Do you want to update the Claude.ai web bundle too?

If yes:
```bash
./scripts/package-skills.sh
```

Then tell them:
> ZIP created at `dist/skills-bundle.zip`. Upload it to Claude.ai → Settings → Features.

---

## Quick Version (For Experienced Users)

If the user provides all info upfront like "Create a skill called `brand-voice` that helps write in my brand tone":

1. Run steps 3-5 without asking
2. Create a draft SKILL.md based on their description
3. Show them the draft and ask what to adjust
4. Continue from step 6
