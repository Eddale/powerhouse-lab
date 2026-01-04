---
name: inbox-triage
description: Processes Drafts Pro captures from the Inbox folder, classifies content by intent, and routes to appropriate Obsidian destinations. Use when triaging inbox, processing captures, or as part of daily task review. Triggers on "triage inbox", "process captures", "check my inbox", "what's in my inbox".
allowed-tools: Read, Glob, Grep, Edit, Write
skills: mission-context
---

# Inbox Triage

## What This Does

Turns your mobile captures into properly filed notes, tasks, and ideas - no manual sorting
required.

## Who It's For

Ed - capturing quick thoughts in Drafts Pro throughout the day.

## The Problem It Solves

Mobile captures pile up in an inbox folder. Without triage, they become noise. This skill
reads each capture, understands intent, and routes it where it belongs.

---

## Paths

```
Inbox:      /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
Processed:  /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/Processed/
Daily note: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
Projects:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
Contacts:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/CONTACT - *.md
```

---

## Instructions

### Step 1: Check Inbox

```
Glob: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/*.md
```

If empty: Report "Inbox empty" and stop.
If items: Continue to Step 2.

### Step 2: Load Active Projects

Pull active project names from mission-context skill AND:

```
Glob: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
```

Build a list of project names for matching (e.g., "BlackBelt", "Little Blue Report",
"Powerhouse Lab").

### Step 3: Read Each Capture

For each `.md` file in Inbox:
1. Read full content
2. Check for Drafts frontmatter (captured date, tags)
3. Extract the main content

### Step 4: Classify Each Capture

**Priority Rule:** Inline hints override auto-detection. Check for these FIRST:
- `IDEA:` or `Idea:` → IDEA
- `Research:` or `?` at end → RESEARCH
- `for [Project Name]` → PROJECT_UPDATE
- `Task:` or `TODO:` → TASK

**Auto-Detection (if no inline hint):**

| Signal | Classification |
|--------|----------------|
| Starts with verb (call, email, buy, check, send, schedule) | TASK |
| Contains question mark | RESEARCH |
| "What if..." or speculative language | IDEA |
| Mentions active project name | PROJECT_UPDATE |
| Person's name + action context | CONTACT |
| Short observation, no action implied | QUICK_THOUGHT |

**Confidence Levels:**
- **High confidence:** Route automatically
- **Medium confidence:** Route with `[?]` flag, include in summary
- **Low confidence:** Ask Ed before routing

### Step 5: Route by Classification

| Classification | Destination | Format |
|----------------|-------------|--------|
| TASK | Daily note → `## Ready` | `- [ ] [content] (MM-DD)` |
| IDEA | Daily note → `## Captures` | `- [IDEA] [content]` |
| RESEARCH | Trigger research-swarm | See Step 6 |
| PROJECT_UPDATE | Project file → `## Context Gathered` | Timestamped append |
| QUICK_THOUGHT | Daily note → `## Scratch` | `- [content]` |
| CONTACT | Create contact note | See Step 7 |

### Step 6: Handle Research (Parallel Execution)

For EACH capture classified as RESEARCH:

1. Extract the research question
2. Launch research-swarm in background:

```
Task(
  description="Research: [Topic]",
  prompt="Research question: [Full capture content]

  Use research-swarm pattern to investigate. Save findings to Zettelkasten.",
  subagent_type="research-swarm",
  run_in_background=true
)
```

3. Add placeholder to daily note Captures:
   `- [RESEARCH] [Topic] - swarm running in background`

**Critical:** If multiple RESEARCH items exist, launch ALL agents simultaneously. Do not
wait for one to complete before starting the next.

### Step 7: Handle Contacts

When a capture mentions a person with action context:

1. Check if `CONTACT - [Name].md` exists
2. If exists: Append to `## Interactions` section
3. If new: Create contact note using template below
4. Always add follow-up task to daily note Ready section

**Contact Note Template:**

```markdown
---
type: contact
created: YYYY-MM-DD
source: inbox-triage
---

# [Person Name]

## Context
[Original capture content]

## Interactions
- YYYY-MM-DD: Initial capture - [summary]

## Follow-up
[Any implied next steps]
```

### Step 8: Move to Processed

After routing each capture:

```bash
mv "[Inbox file]" "[Processed folder]"
```

Never delete - always move to Processed/ as safety net.

### Step 9: Generate Triage Summary

```markdown
## Inbox Triage - YYYY-MM-DD HH:MM

**Processed:** N items | **Research spawned:** M background agents

| Capture | Classification | Routed To |
|---------|----------------|-----------|
| "Call dentist Mon..." | TASK | Daily note → Ready |
| "What if hooks...?" | IDEA | Daily note → Captures |
| "How do coaches u..." | RESEARCH | research-swarm (bg) |

### Research Running in Background
- [Topic 1] - spawned at HH:MM
- [Topic 2] - spawned at HH:MM

### Needs Review [?]
- [Any low-confidence routing decisions]

### Actions Taken
- Moved N files to Inbox/Processed/
- Created CONTACT - [Name].md
- Updated PROJECT - [Name].md
```

---

## Examples

### Example 1: Mixed Inbox

**Inbox contains:**
```
Inbox-001.md: "Call dentist Monday about cleaning"
Inbox-002.md: "What if we did a 5-day hook challenge?"
Inbox-003.md: "How do successful coaches use AI for client onboarding?"
Inbox-004.md: "for BlackBelt - new testimonial from Sarah"
```

**Skill does:**
1. Routes "Call dentist..." → TASK → Ready section
2. Routes "What if..." → IDEA → Captures section
3. Spawns research-swarm for "How do coaches..." → RESEARCH
4. Appends testimonial to PROJECT - BlackBelt.md → PROJECT_UPDATE
5. Moves all 4 files to Processed/
6. Generates triage summary

### Example 2: Contact Capture

**Inbox contains:**
```
Inbox-005.md: "Follow up with John Smith about the proposal we discussed"
```

**Skill does:**
1. Detects person name + action context → CONTACT
2. Creates `CONTACT - John Smith.md` with context
3. Adds task to Ready: `- [ ] Follow up with John Smith about proposal (01-05)`
4. Moves to Processed/

---

## Guidelines

- Respect inline hints - they always override auto-detection
- When confidence is low, flag with `[?]` and include in Needs Review section
- Never delete inbox files - always move to Processed/
- For CONTACT: Always create a follow-up task, even if just "Follow up with [Name]"
- Launch all RESEARCH agents in parallel - don't wait for sequential completion
- The triage summary IS the audit trail - log everything

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-05 | Initial build |

---

## Notes & Learnings

<!-- What we discovered building this. Update after each use. -->
