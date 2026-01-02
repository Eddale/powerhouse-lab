---
name: task-clarity-scanner
description: Scans daily notes and task lists to flag unclear items, suggest agentic-ready rewrites, and modify the file with approval. Use when reviewing todos, scanning task lists, or clarifying vague tasks.
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
---

# Task Clarity Scanner

## What This Does
Scans your daily note or task list, identifies unclear or vague tasks, suggests agentic-ready rewrites, and updates the file once you approve the changes.

## When to Use
- "Scan my tasks"
- "Review my daily note"
- "Clarify my todos"
- "Check my task list for today"
- "What can you help me with today?"

## Default Daily Note Location

Ed's daily notes live in Obsidian at:
```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
```

When invoked without a specific file, check today's date and look for that file automatically.

## Instructions

This skill uses the **Batch Pattern** - clarify all tasks first, then execute work.

---

### PASS 1: Clarify (One by One)

**Step 1: Read the Daily Note**
If no file specified, use today's date to find the daily note in the Zettelkasten folder.
Look for the `## Key Tasks` section or any markdown task list (`- [ ]` items).

**Step 2: Quick Triage**
Briefly categorize tasks:
- **Ready** - Clear enough to act on
- **Unclear** - Needs clarification
- **Question** - Not a task, just a thought
- **Done** - Already completed, can skip

**Step 3: Clarify One at a Time**
For each unclear task, present it individually (NOT a wall of text):

```
**Task:** "[the task]"

- **Issue:** [what's unclear]
- **Suggested rewrite:** "[agentic-ready version]"
- **What's needed:** [missing context]
```

Then ask ONE question with options:
1. **Clarify** - "Here's what I mean: [context]"
2. **Accept rewrite** - Use the suggested version
3. **Skip** - Leave as-is for now
4. **Someday/Maybe** - Park it for later
5. **Create project file** - Start a living doc for this task (for complex/multi-session tasks)

Move to the next task after each response. Keep momentum.

**Step 3a: Project File Creation**
When user selects "Create project file":

1. **Create in Obsidian Zettelkasten** at:
   `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - [Task Name].md`

2. **Seed the file** with this template:
```markdown
---
type: project
status: planning
created: YYYY-MM-DD
linked-from: [[YYYY-MM-DD]]
---
# PROJECT: [Task Name]

## What We're Building
[One paragraph describing the goal and why it matters]

## Constraints & Scope
- In scope: ...
- Out of scope: ...
- Dependencies: ...

## Context Gathered
[Brainstorming notes, research findings, decisions made so far]

## Steps (when ready)
- [ ] Step 1
- [ ] Step 2

## Done State
[How we know this is complete]

## Open Questions
- [ ] Question 1
```

3. **Update daily note** - Replace original task with:
   `- [ ] [[PROJECT - Task Name]] - [brief description]`

4. **Offer to continue brainstorming** in the project file right now

**Step 4: Rewrite Principles**
When suggesting rewrites:
- State the specific action
- Include context needed
- Define the done state
- Make it agent-handoff ready
- **Include URLs/links** so tasks are self-contained (agents shouldn't have to ask for references)

Example:
- Before: "Make Google Drive AI Ready"
- After: "Organize Google Drive for AI access: Create 'AI-Ready' folder, move key docs, document what each folder contains"

**Setup / Configuration Tasks:**
Clarify what "done" means - distinguish between:
- **Just configured:** Created, not tested
- **Verified working:** Tested, confirmed functional
- **Fully integrated:** Working in daily workflow

Example:
- Before: "Set up Gmail App Password"
- After: "Set up Gmail App Password: Enable 2FA, create app password, test IMAP connection works"

**Step 4b: Flag Task Dependencies**
While clarifying, watch for blocking relationships:
```
- [ ] Convert project to skill ← Do first
  - [ ] Upload skill ZIP ← Blocked by above
```
Suggest marking these in the note during approval phase.

**Step 4c: Surfaced Tasks**
Clarifying one task often surfaces additional tasks. Track these as you go:
- New research needed
- Dependencies discovered
- Related updates required

These get added as a separate "Surfaced Tasks" section when updating the file.

**Step 4c: Final Check**
Before moving to PASS 2, ask: **"Did we miss anything?"**
This catches tasks that surfaced during conversation but weren't explicitly noted.

---

### PASS 2: Update the File

**Step 5: Batch the Changes**
After all tasks are clarified, summarize:
```
Ready to update your daily note:
- Task 1: [original] → [rewrite]
- Task 2: Skipped
- Task 3: [original] → [rewrite]
- Task 4: → Someday/Maybe
```

Get final approval before making edits.

**Step 6: Apply Edits**
- Use Edit tool to modify the original file
- Move Someday/Maybe items to designated file
- Preserve all other content exactly
- Confirm: "Updated [N] tasks."

---

### PASS 3: Execute (Future)

**Step 7: Spin Up Agents**
For tasks marked "Ready to Go", offer to spin up agents:
```
These tasks are ready for agents:
- [task 1] - I can do this now
- [task 2] - Needs a research agent
- [task 3] - I can do this now

Want me to start working on these?
```

Execute approved tasks, report back when done.

## Guidelines

1. **Don't over-engineer** - A slightly vague task that's obvious to Ed doesn't need rewriting
2. **Preserve voice** - Rewrites should sound like Ed, not like corporate jargon
3. **Flag unknowns honestly** - If you don't know what "CMM" means, say so
4. **Suggest, don't assume** - Always get approval before modifying the file
5. **Keep the human in the loop** - The goal is to help Ed move faster, not to take over

## The Project File Pattern

For tasks that are too big to clarify inline, create a project file instead:
- The file is a living document that grows over sessions
- Daily note links to the project file (keeps it visible)
- When ready to execute, the project file IS the spec
- If parked for 1+ week, move to [[Someday-Maybe]] file

**When to suggest a project file:**
- Task involves multiple sub-tasks
- Needs research before execution
- Will take multiple sessions to complete
- Has dependencies on other work
- User says "let me think about this"

**The GTD-inspired lifecycle:**
```
Daily Note Task
    ↓ (needs breaking up)
Project File in Obsidian
    ↓ (active brainstorming)
Still on daily note as link
    ↓ (not ready for 1+ week)
[[Someday-Maybe]] file
    ↓ (ready to build)
GitHub repo execution
```

## Task Grouping Patterns

When updating the daily note, group tasks by type:

- **Key Tasks** - Main work items for today
- **Surfaced Tasks** - New tasks discovered during clarification (often research or dependencies)

### Research Task Organization

**Single Research Tasks:** Follow the Research Task Pattern below.

**Research Swarms / Ultrathink Sessions:** When 3+ related research tasks emerge:
- Suggest grouping under a single "Ultrathink - [Topic] Research YYYY-MM-DD" document
- Individual research tasks reference findings in that doc
- All discoveries + architecture decisions captured together
- New dependencies/tasks discovered during research go to "Surfaced Tasks"

Example from Ed's workflow:
- [[Ultrathink - Agent Skills Framework Research 2026-01-02]] - bundled 5 agent/skills research tasks
- [[Research - Parallel Agent Findings - 2026-01-02]] - bundled API research (GHL, Google, Claude)

Research tasks are especially good to group - they can run in parallel (agents, Mac client, ChatGPT) while Ed continues other work.

## Research Task Pattern

Research tasks have a distinct completion format that captures findings inline:

**Format:**
```
- [x] ~~[Research Topic]~~ → **Finding:** [Summary]. See [[Document Name]]
```

**When to suggest this pattern:**
- Any task starting with "Research", "Investigate", "Explore"
- Tasks that will produce a findings document or architecture decision
- Multiple related research tasks (suggest grouping into "Ultrathink" session)

**Example transforms:**
- Before: `- [ ] Research Claude browser access`
- After: `- [x] ~~Research Claude browser access~~ → **Finding:** No official MCP browser server. Best: Use API tokens (Notion, GitHub). See [[Research - Browser Access - 2026-01-02]]`

**Ultrathink Bundling Suggestion:**
When you see 3+ related research tasks, suggest:
"These research tasks are related and could run in parallel. Consider bundling as 'Ultrathink - [Topic] Research YYYY-MM-DD'"

## Where Progressive Documents Live

Some tasks need working documents that build up over time:

| Phase | Location | What Happens |
|-------|----------|--------------|
| **Brainstorming** | Obsidian Zettelkasten | Project file accumulates ideas, context, decisions |
| **Parked (GTD)** | [[Someday-Maybe]] | Remove from daily note, park until ready |
| **Building** | GitHub repo | Execution uses repo protocols (tasks/todo.md, etc.) |

Rule of thumb: **All brainstorming starts in Obsidian.** When ready to actually build, GitHub protocols take over.

## Examples

### Input (from daily note):
```
## Key Tasks
- [ ] Make Google Drive AI Ready
- [ ] Setup CMM
- [ ] update mission-context to include my tech stack
```

### Output (report):
```
## Task Clarity Report

### Ready to Go
- "update mission-context to include my tech stack" - Clear action, clear location, could do this now

### Needs Clarification
- "Make Google Drive AI Ready"
  - Issue: What does "AI Ready" mean? Which folders?
  - Suggested rewrite: "Organize Google Drive for AI workflows: identify key folders, create consistent naming, note what each folder contains"
  - What's needed: Your definition of "AI Ready" for your use case

- "Setup CMM"
  - Issue: I don't know what CMM is
  - Suggested rewrite: [Need more context]
  - What's needed: What is CMM? Link or description?
```
