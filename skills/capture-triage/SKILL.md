---
name: capture-triage
description: Processes Drafts Pro captures from the Captures folder. Classifies by intent, shows preview for approval, routes to Ready as tasks. Use when triaging captures, processing mobile notes, or as part of daily review. Triggers on "triage captures", "process captures", "check my captures".
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
skills: mission-context
---

# Capture Triage

## What This Does

Turns mobile captures into actionable tasks in your Ready queue. Everything captured has
intent - this skill makes it explicit so task-clarity-scanner can decide what's important.

## Who It's For

Ed - capturing quick thoughts in Drafts Pro throughout the day.

## The Philosophy

> Everything captured has intent. Route to Ready, let task-clarity-scanner decide what
> moves to Someday/Maybe.

No passive filing. Every capture becomes a decision point.

---

## Paths

```
Captures:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Captures/
Processed:  /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Captures/Processed/
Daily note: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
Projects:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
Contacts:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/CONTACT - *.md
```

---

## Instructions

### Step 1: Check Captures Folder (Root Only)

**Important:** Only check files directly in Captures/, NOT subdirectories.

```bash
ls /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Captures/*.md 2>/dev/null
```

If no files found: Report "No captures waiting" and stop.
If files found: Continue to Step 2.

### Step 2: Load Context

Pull active project names from mission-context skill AND:

```
Glob: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
```

Build a list of project names for matching.

### Step 3: Read and Classify Each Capture

For each `.md` file in Captures:
1. Read full content
2. Detect if already-processed (see Step 3a)
3. Classify by intent (see Step 4)

### Step 3a: Detect Already-Processed Content

If capture content looks like a summary (has structure, headers, quotes sources):
- Flag as `[PROCESSED]`
- Will suggest routing as REFERENCE
- Won't offer research-swarm (already researched)

**Signals of processed content:**
- Has markdown headers (##, ###)
- Contains bullet lists with structured info
- Quotes or attributes other sources
- Looks like notes from a video/article

### Step 4: Classify Each Capture

**Priority Rule:** Inline hints override auto-detection. Check for these FIRST:
- `IDEA:` or `Idea:` → IDEA
- `Research:` → RESEARCH (triggers swarm option)
- `for [Project Name]` → PROJECT_UPDATE
- `Task:` or `TODO:` → TASK

**Auto-Detection (if no inline hint):**

| Signal | Classification |
|--------|----------------|
| Starts with verb (call, email, buy, check, send, schedule) | TASK |
| Contains `Research:` hint or explicit question needing investigation | RESEARCH |
| "What if..." or speculative language | IDEA |
| Mentions active project name | PROJECT_UPDATE |
| Person's name + action context | CONTACT |
| Links, articles, saved content, observations | REFERENCE |

### Step 5: Show Classification Preview (Dry Run)

**This is the standard flow.** Present classifications using AskUserQuestion:

```
## Capture Triage Preview

I've classified your [N] captures. Review and approve:

| # | Capture | Classification | Suggested Action |
|---|---------|----------------|------------------|
| 1 | "Call dentist..." | TASK | → Ready: "Call dentist (MM-DD)" |
| 2 | "What if we..." | IDEA | → Ready: "Consider: [idea] (MM-DD)" |
| 3 | [PROCESSED] "Article summary..." | REFERENCE | → Ready: "Review: [title] (MM-DD)" |
| 4 | "Research: how do..." | RESEARCH | → Spawn research-swarm? |

Options:
1. Approve all - Route as shown
2. Modify - Change specific classifications
3. Skip items - Don't route selected captures
4. Spawn research for #4 - Launch research-swarm agent
```

**Key points:**
- Show [PROCESSED] flag for already-summarized content
- RESEARCH items ask if user wants swarm, don't auto-spawn
- Let user approve, modify, or skip before any changes

### Step 6: Route by Classification

After approval, route each capture:

| Classification | Destination | Format |
|----------------|-------------|--------|
| TASK | Ready | `- [ ] [action] (MM-DD)` |
| IDEA | Ready | `- [ ] Consider: [idea] (MM-DD)` |
| REFERENCE | Ready | `- [ ] Review: [title/summary] (MM-DD)` |
| RESEARCH | If approved: spawn agent | See Step 7 |
| PROJECT_UPDATE | Project file | Timestamped append to `## Context Gathered` |
| CONTACT | Create note + Ready | `- [ ] Follow up with [Name] (MM-DD)` |

### Step 7: Handle Research (Only When Requested)

**Only spawn research-swarm if:**
- User explicitly approved during Step 5 preview
- Capture has `Research:` inline hint AND user confirmed

For each approved RESEARCH item:

```
Task(
  description="Research: [Topic]",
  prompt="Research question: [Full capture content]

  Use research-swarm pattern to investigate. Save findings to Zettelkasten.
  When complete, add review task to Ready: '- [ ] Review: [[Research - Topic]] (MM-DD)'",
  subagent_type="research-swarm",
  run_in_background=true
)
```

Add placeholder to daily note:
```
- [RESEARCH] [Topic] - swarm running in background
```

### Step 8: Handle Contacts

When a capture mentions a person with action context:

1. Check if `CONTACT - [Name].md` exists
2. If exists: Append to `## Interactions` section
3. If new: Create contact note using template
4. Always add follow-up task to Ready

**Contact Note Template:**

```markdown
---
type: contact
created: YYYY-MM-DD
source: capture-triage
---

# [Person Name]

## Context
[Original capture content]

## Interactions
- YYYY-MM-DD: Initial capture - [summary]

## Follow-up
[Any implied next steps]
```

### Step 9: Move to Processed

After routing each capture:

```bash
mv "[Captures file]" "[Processed folder]"
```

Never delete - always move to Captures/Processed/ as safety net.

### Step 10: Generate Triage Summary

```markdown
## Capture Triage - YYYY-MM-DD HH:MM

**Processed:** N items | **Research spawned:** M (if any)

### Routed to Ready
- [N] tasks
- [N] ideas (Consider:)
- [N] references (Review:)

### Research Running
- [Topic] - spawned at HH:MM

### Actions Taken
- Moved N files to Captures/Processed/
- Created CONTACT - [Name].md (if any)
- Updated PROJECT - [Name].md (if any)
```

---

## Examples

### Example 1: Dry Run Preview

**Captures folder contains 4 files:**

```
1. "Call dentist Monday about cleaning"
2. "What if we did a 5-day hook challenge?"
3. [PROCESSED] "Summary of Karpathy video - 6 paradigm shifts..."
4. "Research: how do successful coaches use AI?"
```

**Skill shows:**

```
## Capture Triage Preview

| # | Capture | Classification | Suggested Action |
|---|---------|----------------|------------------|
| 1 | "Call dentist..." | TASK | → Ready: "Call dentist Monday (01-05)" |
| 2 | "What if we..." | IDEA | → Ready: "Consider: 5-day hook challenge (01-05)" |
| 3 | [PROCESSED] "Summary of Karpathy..." | REFERENCE | → Ready: "Review: Karpathy video summary (01-05)" |
| 4 | "Research: how do coaches..." | RESEARCH | → Spawn research-swarm? |

Approve all, modify, or skip items?
```

### Example 2: After Approval

User approves all, including research swarm for #4.

**Result:**
- Ready gets 3 new tasks + 1 research placeholder
- Research-swarm spawns in background
- All 4 files moved to Processed/
- Summary generated

---

## Guidelines

- **Dry run is standard** - Always show preview, never auto-route
- **Respect inline hints** - They override auto-detection
- **Research-swarm is opt-in** - Don't auto-spawn, ask first
- **[PROCESSED] content** - Flag summaries, suggest REFERENCE routing
- **Everything to Ready** - Let task-clarity-scanner handle prioritization
- **Never delete** - Always move to Processed/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-05 | Initial build as inbox-triage |
| 2.0 | 2025-01-05 | Renamed to capture-triage, added dry run, AskUserQuestion flow, all routes to Ready |

---

## Notes & Learnings

- Day 1 test processed 32 captures with backlog - dry run prevented overwhelm
- [PROCESSED] detection helps avoid re-researching already-summarized content
- Research-swarm opt-in prevents runaway agent spawning
