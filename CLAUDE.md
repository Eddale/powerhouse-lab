# CLAUDE.md - Vibe Coder's Operating Manual

## CURRENT FOCUS
<!-- Update this section each session - like a creative brief -->
```
Working on: [What you're building today]
Why: [The leverage it creates]
Next: [What ships after this]
```

---

## WHO I AM

I'm Ed, a **Vibe Coder**. I focus on the product, the feel, and the outcome - not the syntax.

**My background:** World-class copywriter and coach. I think in headlines, hooks, and frameworks. I built BlackBelt coaching and the AI Amplified Coaching Powerhouse program. I publish "The Little Blue Report" on Substack.

**My superpower:** I know what good looks like. I don't need to know how to build it - I need you to translate my vision into working code.

**My mental models come from:** Gary Halbert, Bond Halbert, Stephen King, William Zinsser. If you can explain something using a copywriting or coaching analogy, do it.

---

## THIS REPO: POWERHOUSE LAB

This is my **Leverage Skunkworks** - where AI tools and skills get built, tested, and validated.

### The Lifecycle
```
prototypes/  →  skills/  →  [Own Repo]
     ↓
  archive/   (kill rule applied)
```

### Folder Purposes
- `_templates/` - Starting points (copy, don't modify)
- `prototypes/` - Active experiments
- `skills/` - Validated, documented, reusable
- `archive/` - Retired with lessons captured

---

## HOW TO TALK TO ME

### The Translation Layer (Tech → Copywriter Speak)

| Technical Term | What It Means to Me |
|----------------|---------------------|
| Component | A reusable template (like a swipe file element) |
| Props | Variables you pass in (like merge tags in an email) |
| State | What the page remembers (like cookies tracking a visitor) |
| API | The backend conversation (like a database query) |
| Deploy | Publish live (like hitting "send" on a campaign) |
| Refactor | Editing for clarity without changing meaning |
| Debug | Finding why the copy isn't converting |
| Dependencies | The tools in your toolbox |
| Environment variables | Private keys - like your merchant account credentials |
| Repository | Your master swipe file for this project |

### My Terminology (Use These)

| My Term | What It Means |
|---------|---------------|
| Capabilities X-Ray | Scanning for what a project needs |
| Plays Shortlist | Prioritized task list, riskiest assumption first |
| Leverage Asset | Any tool that does the lifting |
| Kill rules | When to stop and pivot vs. keep pushing |
| Ship This = Win Day | The only metric that matters |
| Prompt Whispering™ | Building AI tools through conversation |
| Prompt Wrangling™ | Debugging and refinement |
| Research Swarm | Multi-angle parallel research - attacking a question from 3-5 simultaneous perspectives |
| Zettelkasten Integration | Knowledge capture via daily notes and research docs in Obsidian |
| Verify With Data | Prove something works with code, not just eyeballs |
| Screenshots as Spec | Visual feedback that shows exactly what's wrong - accelerates debugging |

### Output Formatting

- **Soft wrap only** - Let text flow naturally, no hard line breaks mid-paragraph
- Use blank lines between paragraphs for readability
- Do not wrap tables or code blocks - keep them as-is
- Short responses stay short; longer explanations get proper paragraph breaks

---

## THE IRON RULES

1. **DO NOT BE LAZY. NEVER BE LAZY.** If there's a bug, find the root cause and fix it. No temporary fixes. You are a senior developer.

2. **MAKE ALL FIXES AS SIMPLE AS HUMANLY POSSIBLE.** Impact as little code as possible. Your goal is zero new bugs. Simplicity is everything.

3. **ALWAYS EXPLAIN THE WHY.** When you make a change, tell me what you did AND why - in plain English, using copywriter/coach analogies when they fit.

### Iron Rules vs. Guidelines

**Iron Rules** (CRITICAL, MUST, DO NOT):
- Use sparingly - only for known failure modes
- Reserved for steps that actually broke something
- The three rules above qualify - they prevent real problems

**Guidelines** (should, consider, typically):
- Default style for new instructions
- Trust Claude to apply good judgment
- Upgrade to Iron Rule only after something fails

Pattern: Start soft, harden only where bugs bite.

---

## THE WORKFLOW

### Before You Touch Code

0. **Check git status** - Know the state before touching anything (uncommitted changes, untracked files)
1. **Parallel session check** (for builds/prototypes) - Ask Ed:
   - "Are other Claude Code sessions running that might touch this repo?"
   - If yes: "Should I work on a branch? Suggested name: `build/[feature-name]`"
   - This prevents git conflicts when background builds are running
2. **Think through the problem** - Read the codebase for relevant files
3. **Write a plan** to `tasks/todo.md` - A checklist you'll work through
4. **Check in with me** - I verify the plan before you start

### While You Work

5. **Execute the todo items** - Mark complete as you go
6. **Give me high-level summaries** - What changed and why
7. **Keep changes minimal** - Every edit should be as small as possible

### When You Finish

8. **Add a review section** to `tasks/todo.md` - Summary of changes and any notes

### End of Session (When Ed says "wrapping up", "end of session", "syncing", etc.)

9. **Update daily notes:**
   - Add any research reports to Captures section
   - **Mark completed tasks as done** (`- [x]`)
   - Log key decisions made
   - Flag any blockers or follow-ups

10. **Complete git sync:**
    - Check `git status` for any uncommitted changes
    - Commit and push all work to GitHub
    - Verify local and remote are aligned

11. **Package any new/modified skills:**
    - Run `./scripts/package-skill.sh <skill-name>` for each skill created or updated
    - Confirm ZIPs are in `dist/` folder ready for Claude.ai upload
    - Remind Ed which ZIPs need uploading

### When to Stop and Ask vs. Make the Call

**STOP AND ASK:**
- Structural decisions (what to build, how to architect)
- Anything that changes the user experience
- When you're choosing between two valid approaches
- When you hit something that feels wrong

**MAKE THE CALL AND FLAG IT:**
- Naming conventions
- Minor implementation details
- Code organization within files
- Which library to use for a standard task

### Automation Signals (Override Ask Instructions)

When Ed uses these phrases, run the full workflow without stopping to ask:

**Trigger phrases:**
- "automatic" / "automatically"
- "in the background"
- "without asking" / "don't ask"
- "just do it" / "handle it" / "take care of it"
- "run the whole thing"

**What this means:**
- Skip optional confirmation steps
- Make reasonable decisions instead of asking
- Complete the full pipeline end-to-end
- Only stop for actual errors or blockers

**This overrides skill instructions.** If a skill says "ASK the user" but Ed said "automatic",
skip the ask and make the call. Skill "ask" instructions are defaults, not iron rules.

**Example:**
- Ed: "Run this through the hook evaluator automatically"
- Wrong: Score it, then ask "Keep / Tweak / Trash?"
- Right: Score it, if weak generate alternatives, pick the best, output final hook

---

## ARCHITECTURE PHILOSOPHY

### The Three Layers

| Layer | What It Is | Who Maintains It |
|-------|------------|------------------|
| **Tools** | Python scripts, APIs, Bash commands | Hidden inside skills |
| **Skills** | SKILL.md with instructions | Edit markdown to change behavior |
| **Agents** | Orchestrators that pull skills | Reference skills, don't touch tools |

### The Golden Rule

```
WRONG: Agent → has Bash → calls tool directly
RIGHT: Agent → pulls Skill → Skill contains tool instructions → Claude executes
```

**Why:** If an API breaks, fix one skill - not 58 agents. Skills encapsulate complexity. Non-coders edit markdown, not code.

### Claude IS the Runtime

When a skill says "run `python3 script.py`", Claude executes it. The agent doesn't need direct tool access - the skill brings its tools with it.

### The Tool Access Rule

**Skills tell Claude what to run. Agents grant permission to run it.**

When an agent pulls a skill that says "run python3 script.py", the agent must have `Bash` in its tools list. The skill brings instructions, not permissions.

**Checklist when building agents:**
1. Read each skill in the `skills:` list
2. Note what tools those skills require (Bash for scripts, WebFetch for APIs, AskUserQuestion for prompts, etc.)
3. Add all required tools to the agent's `tools:` frontmatter

Common gotcha: Skill says "run python3 script.py" but agent doesn't have `Bash` → agent fails silently or goes rogue.

---

## PROJECT TYPES

| Type | Location | Speed vs Polish |
|------|----------|-----------------|
| `powerhouse-prototype` | prototypes/ | Speed - ship in 30-90 min |
| `skill-build` | skills/ | Balanced - needs good docs |
| `blackbelt-tool` | Own repo | Polish - client-facing |
| `content-engine` | Either | Speed - function over form |

### Dual Documentation Standard

Every prototype should have:
- **README.md** - Technical reference (file structure, deployment, dependencies)
- **HOW-IT-WORKS.md** - Vibe Coder explanation (what it does, why it matters, in copywriter language)

The README is for future-you debugging. The HOW-IT-WORKS is for present-you understanding.

### Tool Documentation (GitHub = Single Source of Truth)

**Core principle:** Once a tool exists in GitHub, ALL documentation lives in GitHub.

Why? Web and desktop Claude clients can't reliably access Zettelkasten. GitHub is accessible from everywhere.

**Zettelkasten is for:** Session debriefs, daily captures, research swarm outputs - things that capture the *process*, not the *product*.

**Documentation is part of creation, not a follow-up task.** When you create any new app, tool, agent, or skill, the `docs/` folder gets created at the same time. Shipping without docs is like shipping without tests - technically possible, but you're setting up future-you for pain.

**Every skill gets a `docs/` folder:**
```
skills/[skill-name]/
├── SKILL.md              # Required - the skill itself
├── docs/
│   ├── README.md         # Technical reference (for Claude and devs)
│   ├── GUIDE.md          # Business-friendly (Ed's voice, analogies)
│   ├── ROADMAP.md        # Shipped history + future ideas
│   └── plans/            # Improvement plans
│       ├── current.md    # Active improvement
│       └── archive/      # Decision log
```

**Every prototype gets the same:**
```
prototypes/[name]/
├── README.md             # Technical reference
├── HOW-IT-WORKS.md       # Vibe coded explanation
├── docs/
│   ├── ROADMAP.md        # Future ideas + learnings
│   └── plans/
```

**Document voice:**
- **README.md** - Technical, factual, for debugging
- **GUIDE.md / HOW-IT-WORKS.md** - Ed's voice, business coach analogies, explains the "why"
- **ROADMAP.md** - Ed's voice, what's shipped, what's planned, what we learned

**The improvement cycle:**
1. Ed says "Improve [tool]: [description]"
2. Claude reads docs/ROADMAP.md and docs/README.md
3. Claude creates docs/plans/current.md with plan
4. Ed approves verbally
5. Claude executes (Ralph Wiggum loop if complex)
6. Claude updates ROADMAP.md, archives plan, commits

See `tasks/todo.md` for full pipeline documentation.

---

## RESEARCH WORKFLOWS

### When to Use Research Swarm

Use the parallel research pattern (`.claude/agents/research-swarm.md`) when:
- Topic needs 3+ distinct research angles
- Strategic decision with multiple valid options
- Technology evaluation or competitive analysis
- Time-to-insight matters (parallel beats sequential)

### When to Use Single-Agent Research

Use targeted research instead when:
- You need one specific fact or piece of information
- The question is straightforward (API docs, syntax, etc.)
- You already know the angle you're investigating
- Speed is critical and depth is secondary

### Research Output Pattern

All Research Swarm outputs:
1. Generate markdown report in Zettelkasten: `Research Swarm - [Topic] - YYYY-MM-DD.md`
2. Link in daily note Captures section
3. Mark original research tasks with inline findings: `→ **Finding:** [summary]. See [[doc]]`
4. New tasks discovered go to Surfaced Tasks section

### The "More Planning = Less Coding" Pattern

For complex skill builds or features:
1. **Research Swarm first** - Generate research doc with open questions
2. **Ed comments inline** - Answer questions directly in the doc using `> [!Note] AI CONTEXT` callouts
3. **Read the commented doc** - All decisions are captured before coding starts
4. **Build from spec** - Implementation becomes straightforward execution

This pattern works because:
- Ed's expertise is captured in writing, not lost in conversation
- Questions get answered once, referenced forever
- The doc becomes the spec AND the decision log
- "More planning = less coding" - smooth builds, fewer loops

### Obsidian Integration

Ed's knowledge management lives in Obsidian:
- **Daily notes:** `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md`
- **Research docs:** Same folder, named `Research Swarm - [Topic] - YYYY-MM-DD.md`
- **Captures section:** Links to all research completed that day

### Zettelkasten Rule

**When saving any document to Ed's Zettelkasten, always add a link to that day's Captures section.**

```
Location: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
Section: ## Captures
Format: - [[Document Name]] - Brief description
```

This applies to: YouTube notes, research docs, project files, articles, anything saved to the vault.

### Iron Rule: Never Write Daily Notes

**When updating Ed's daily note:**
1. **Glob first** - Search for `202*-MM-DD.md` to find the actual file (don't assume the year)
2. **Read it** - Confirm it exists and see its structure
3. **Edit to append** - Use Edit to add to the appropriate section (Captures, Ready, etc.)
4. **Never use Write** - Write overwrites the entire file and destroys Ed's tasks

If Read returns "file does not exist" for a daily note, something is wrong. Stop and verify
the filename before creating anything.

### Where to Find Ed's Files

When searching for files Ed mentions, check these locations in order:

| Location | What Lives There |
|----------|------------------|
| `~/Downloads/` | Most files end up here first |
| `~/Documents/` | Organized project files |
| `~/Documents/COPYobsidian/MAGI/Zettelkasten/` | Knowledge base, notes, research |
| MacWhisper database | Audio transcriptions (search for `.txt` files from transcripts) |

**MacWhisper:** Ed uses MacWhisper for all audio transcriptions. Transcripts are saved as
`.txt` files, often in Downloads or the MacWhisper database folder at:
`~/Library/Application Support/MacWhisper/Database/`

---

## TECH CONTEXT

### My Stack Preferences
- **Frontend:** React/Next.js (the face)
- **Backend:** Python when we need AI brains
- **Hosting:** Vercel (easy deploy)
- **Repository:** GitHub

### Environment
- **IDE:** Antigravity (Google's IDE) with Claude extension
- **Also using:** Claude Code directly

### The Vibe Coder Rule
> "If I want it to *think* smart, use Python.
> If I want it to *look* cool, use React."

---

## SKILLS PROTOCOL

Before creating documents, presentations, spreadsheets, or PDFs:
1. Check `/mnt/skills` for relevant SKILL.md files
2. Read the skill documentation FIRST
3. Follow the established patterns

### Skill Design Principles

When building skills:
1. **Tools live inside skills** - `tools/` folder with Python scripts, etc.
2. **SKILL.md instructs Claude** - What to run, how to parse output, where to save
3. **Agents pull skills** - Add to `skills:` list in frontmatter, not `tools:`
4. **Package for distribution** - `./scripts/package-skill.sh <skill-name>` creates ZIP for Claude.ai

### Context Propagation Pattern

When a skill needs user context (like audience):
1. Detect if provided in input
2. If not, ask once using AskUserQuestion
3. Store in output metadata (frontmatter)
4. Pass to downstream skills that need it

Example: newsletter-writer asks audience once, passes to hook-stack for "Speak Their Lingo" scoring.

### Iron Rule: Always Use new-skill-wizard

**When creating ANY new skill:**
1. Invoke the `new-skill-wizard` skill FIRST
2. Let the wizard create the scaffolding
3. THEN add your content to SKILL.md

Never create skill folders or SKILL.md files manually.

**YAML frontmatter (Anthropic spec):**
```yaml
---
name: kebab-case-name
description: One sentence. Use when [trigger phrases].
allowed-tools: Read, Write, Edit, Glob, Grep
---
```

**`allowed-tools` rules:**
- Only actual tools: `Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch`
- Patterns allowed: `Bash(python:*)`, `WebFetch(domain:example.com)`
- **Skills do NOT go here** - skills chain via instructions in markdown body
- Missing frontmatter = Claude.ai upload fails

**Skill chaining:**
- Put "run through ai-slop-detector skill" in the markdown instructions
- Do NOT put `ai-slop-detector` in `allowed-tools`
- Claude discovers and invokes referenced skills automatically

### Skill Registration Checklist

**When a skill doesn't work, check these in order:**

1. [ ] Skill folder exists in `skills/<name>/`
2. [ ] SKILL.md has valid YAML frontmatter (starts/ends with `---`)
3. [ ] Skill name in frontmatter uses lowercase, numbers, hyphens only
4. [ ] Symlinks created: `./scripts/setup-skills.sh`
5. [ ] **Registered in settings:** `Skill(<name>)` in `.claude/settings.local.json`
6. [ ] Skill description is specific and includes trigger keywords
7. [ ] New terminal session started **for settings changes only** (skill file edits are instant)

**The pattern:**
```
Valid SKILL.md with good description → Auto-discovered by Claude
Permissions in settings.json → Needs new terminal session
Editing SKILL.md content → Takes effect immediately
```

Root cause 90% of the time: Step 5 is missing. The skill exists but isn't registered in settings.

### Dry Run Pattern (AskUserQuestion)

For skills that process multiple items or trigger expensive operations:

1. Read and classify all items
2. Show preview table using AskUserQuestion
3. Let user approve, modify, or skip
4. Only then execute approved actions

**Example preview:**
```markdown
| # | Item | Classification | Suggested Action |
|---|------|----------------|------------------|
| 1 | "Call dentist..." | TASK | → Ready |
| 2 | "What if we..." | IDEA | → Ready: "Consider: [idea]" |
| 3 | [link to article] | RESEARCH | → Spawn research-swarm? |

Options: Approve all | Modify | Skip items
```

**Why it matters:**
- Prevents runaway operations (12 research agents spawning unexpectedly)
- Keeps user in control of their knowledge system
- Batch processing without batch surprises

---

## KILL RULES

Stop and pivot when:
- We've looped on the same bug 3+ times
- The "simple fix" keeps getting more complex
- My energy drops (I'll tell you)
- 90 minutes on a prototype with no working v1

When killing a project:
1. Move to `archive/`
2. Add `POSTMORTEM.md` capturing the lesson
3. Note any salvageable parts

---

## VERIFICATION PATTERNS

### The "Verify With Data" Rule

Don't assume code works. Prove it programmatically.

**Pattern:**
1. Deploy/run the thing
2. Test with real inputs
3. **Verify outputs with code** (not just eyeballs)

**Example:** After generating a DOCX:
```python
from docx import Document
doc = Document("output.docx")
print(f"Tables: {len(doc.tables)}")  # Proves tables rendered
print(f"Paragraphs: {len(doc.paragraphs)}")
```

This is the difference between "it should work" and "it does work."

### Browser Testing with Claude in Chrome

For deployed web apps, use browser automation to test end-to-end:
1. Fill forms with real data
2. Click buttons
3. Verify downloads/outputs
4. Screenshot results

**Production is truth.** Local testing is useful, but the real test happens at the deployed URL.

### The Ship → Test → Fix Loop

Vercel deploys in 45 seconds. Use this:
1. Deploy v1 (basic, maybe broken)
2. Find issues in production
3. Fix specific things
4. Deploy v2
5. Verify

Faster than trying to get it perfect locally.

---

## KNOWN GOTCHAS

### Debugging Agent Failures

When an agent doesn't work as expected, **fix the skill, not the agent.**

**Diagnostic order:**
1. **Test the skill standalone** - Run trigger phrase directly, without the agent
2. **Check skill registration** - Is `Skill(<name>)` in settings.local.json?
3. **Check skill tools** - Does allowed-tools have what the skill needs?
4. **Only then check agent wiring** - Is skill in agent's `skills:` list?

**Anti-pattern:** Adding "CRITICAL", "MUST", "IRON RULE" language to agents to force
behavior. This masks the real problem and makes agents brittle.

**The principle:** Agents orchestrate. Skills execute. If execution fails, the skill is
broken - not the orchestration.

### Positive Framing in Agent/Skill Instructions

**Anti-pattern:** "DO NOT reimplement" or "DO NOT do your own version"
**Problem:** Negative instructions prime the unwanted behavior (pink elephant problem)

**Pattern that works:**
- "The [skill-name] skill handles X, Y, Z"
- "Continue when the skill completes"
- Trust automatic skill discovery via description matching

**Anti-pattern:** Showing implementation details before delegation
**Problem:** Gives Claude the recipe to DIY instead of delegating

**Pattern that works:**
- Remove glob paths, file locations, and logic from agents
- Let skills own their own implementation details
- Agents describe WHAT happens, skills describe HOW

### Session Caching & Settings Refresh

Skills and settings have different refresh behavior in Claude Code:

**Settings files** (`.claude/settings.json`, `.claude/settings.local.json`):
- Changes to permissions, Skill registrations, and other settings require a **new terminal session**
- This includes adding `Skill(<name>)` to the permissions array
- Use `/config` in an interactive session to modify some settings without restarting

**Skills** (SKILL.md files):
- Changes take effect **immediately** - no restart required
- Skills are auto-discovered based on their description
- When you modify a SKILL.md file, Claude loads the updated version on the next matching request
- This means you can iterate on skill instructions without restarting

**Agents** (`.claude/agents/*.md`):
- Agent definitions may be cached during a session
- If changes to an agent don't take effect, start a new terminal session

**Practical implication:**
- Editing SKILL.md content? Just save and test - it's instant
- Adding a new skill to settings.local.json? Need new terminal session
- Changing agent definitions? Need new terminal session

### Permission Path Syntax (Double Slash)

Paths in `settings.local.json` permissions follow gitignore spec. **A leading `/` is relative to
the settings file, not the filesystem root.**

```
WRONG: Read(/Users/eddale/**)     → Looks for ./Users/eddale/** (relative)
RIGHT: Read(//Users/eddale/**)    → Looks for /Users/eddale/** (absolute)
```

The double slash `//` means "absolute filesystem path". Without it, permissions silently fail
because the relative path doesn't exist.

### Global vs Project Settings

Two settings files, different purposes:

| Location | Purpose | What Goes Here |
|----------|---------|----------------|
| `~/.claude/settings.local.json` | Universal | Read/Write/Edit home folder, WebSearch, git commands, common domains |
| `.claude/settings.local.json` | Project-specific | Skill registrations, repo scripts, project-specific Bash commands |

**Rule:** If you'd want the permission in ANY project, put it in global. Project settings add on top.

Keep them in sync by design - universal stuff in global, project stuff in project. Don't duplicate.

### Settings File Hygiene

The `.claude/settings.local.json` file grows organically as you approve commands. Left unchecked,
it becomes bloated with one-off approvals that break the `/doctor` command.

**Use wildcards, not specific commands:**
```
WRONG: Approving "git commit -m 'fix: something'" → saves full command with message
RIGHT: "Bash(git:*)" → covers ALL git commands
```

**Never approve commands with secrets inline:**
When Claude asks to run something like `AUTH_TOKEN="abc123" bird bookmarks`, say no and configure
the secret properly (environment variable, config file). Approving saves the token to the
permissions file permanently.

**Periodic cleanup signals:**
- `/doctor` shows "Unmatched quote in Bash pattern" errors
- Settings file exceeds ~80 entries
- You see full commit messages or file paths in the permissions list

**The fix:** Review settings, keep wildcards and skill registrations, delete specific one-off
commands that are already covered by wildcards.

### Claude Runtime Landscape (CLI vs Web vs Desktop)

Three different products, different CLAUDE.md behavior:

| Product | CLAUDE.md? | Source | Best For |
|---------|------------|--------|----------|
| **Claude Code CLI** | ✅ Auto-loads | `~/.claude/` + `./` (merged) | Agentic coding in terminal |
| **Claude Code Web** | ✅ Auto-loads | `./` from GitHub repo only | Remote/browser coding |
| **Claude Desktop App** | ❌ No | N/A (different product) | Chat + light tasks |

**Key implications:**

1. **Keep CLAUDE.md in GitHub repos** - This ensures both CLI and Web see it
2. **Global `~/.claude/CLAUDE.md`** - Only CLI sees this, Web cannot access your local filesystem
3. **Claude Desktop ignores CLAUDE.md** - It treats GitHub files as context, not instructions

**For this repo:** CLAUDE.md lives here in the project root. Works for CLI and Web. Claude Desktop
users would need to manually reference it.

**Claude.ai sandbox restrictions** (applies to Desktop and Web chat, NOT Claude Code):
- Cannot reach external domains via WebFetch
- Cannot run Bash commands
- Limited filesystem access

Skills that work in Claude Code CLI may not work in Claude.ai chat. See mission-context for details.

### Image Generation with Nano Banana Pro

When generating carousel images or any multi-image set with a consistent character:
1. **Reference image required** - Upload photo with first prompt
2. **Add consistency instruction** - Include "maintain consistent character appearance from reference" in all prompts
3. **Test before finalizing** - Generate in Google AI Studio, verify quality, then commit
4. **API consideration** - Programmatic reference image upload is an unsolved problem for automation

**Prompt language:** Use "the man from the reference image" not "you" - Nano Banana Pro doesn't understand second person.

**Saving prompts for Ed:**
When creating image prompts (hero images, carousels, etc.), save as markdown file in Zettelkasten:
- Location: `Hero Image Prompt - [Title] - YYYY-MM-DD.md`
- Put the prompt in a code block for one-click copy
- Include metadata: article, platform, aspect ratio, model
- Add to daily note Captures section

---

## LIVING DOCUMENT

This file evolves. When we discover something that should be standard, I'll add it here.

**Last updated:** January 2026
**Version:** 2.10 - Added parallel session check before builds (branch workflow to avoid git conflicts)
