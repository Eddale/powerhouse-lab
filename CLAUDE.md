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
| Ultrathink / Research Swarm | Multi-angle parallel research - attacking a question from 3-5 simultaneous perspectives |
| Zettelkasten Integration | Knowledge capture via daily notes and research docs in Obsidian |

### Output Formatting

- Wrap prose at 90 characters with blank lines between paragraphs
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

1. **Think through the problem** - Read the codebase for relevant files
2. **Write a plan** to `tasks/todo.md` - A checklist you'll work through
3. **Check in with me** - I verify the plan before you start

### While You Work

4. **Execute the todo items** - Mark complete as you go
5. **Give me high-level summaries** - What changed and why
6. **Keep changes minimal** - Every edit should be as small as possible

### When You Finish

7. **Add a review section** to `tasks/todo.md` - Summary of changes and any notes

### End of Session (When Ed says "wrapping up", "end of session", "syncing", etc.)

8. **Update daily notes:**
   - Add any research reports to Captures section
   - **Mark completed tasks as done** (`- [x]`)
   - Log key decisions made
   - Flag any blockers or follow-ups

9. **Complete git sync:**
   - Check `git status` for any uncommitted changes
   - Commit and push all work to GitHub
   - Verify local and remote are aligned

10. **Package any new/modified skills:**
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

---

## RESEARCH WORKFLOWS

### When to Use Ultrathink (Research Swarm)

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

All Ultrathink outputs:
1. Generate markdown report in Zettelkasten: `Ultrathink - [Topic] - YYYY-MM-DD.md`
2. Link in daily note Captures section
3. Mark original research tasks with inline findings: `→ **Finding:** [summary]. See [[doc]]`
4. New tasks discovered go to Surfaced Tasks section

### The "More Planning = Less Coding" Pattern

For complex skill builds or features:
1. **Ultrathink first** - Generate research doc with open questions
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
- **Research docs:** Same folder, named `Ultrathink - [Topic] - YYYY-MM-DD.md`
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
2. [ ] SKILL.md has valid YAML frontmatter
3. [ ] Symlinks created: `./scripts/setup-skills.sh`
4. [ ] **Registered in settings:** `Skill(<name>)` in `.claude/settings.local.json`
5. [ ] New terminal session started (settings refresh)

**The pattern:**
```
Symlinks make a skill VISIBLE
Settings registration makes a skill USABLE
```

Root cause 90% of the time: Step 4 is missing. The skill exists but isn't registered.

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

### Session Caching

Claude Code caches certain definitions during a session:
- Agent definitions (`.claude/agents/*.md`)
- Possibly skill definitions

**When changes to an agent don't take effect:**
1. Start a new terminal session
2. Re-test the agent

This isn't a bug - it's how the runtime works. Just be aware.

### Claude.ai Sandbox

Claude.ai (Mac client, web) has sandbox restrictions:
- Cannot reach external domains via WebFetch
- Cannot run Bash commands
- Limited filesystem access

Skills that work in Claude Code may not work in Claude.ai. See mission-context for Runtime Differences.

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
**Version:** 2.1 - Added Skill Registration Checklist, Dry Run Pattern, Debugging Agent Failures
