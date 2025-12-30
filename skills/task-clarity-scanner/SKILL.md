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

## Instructions

This skill uses the **Batch Pattern** - clarify all tasks first, then execute work.

---

### PASS 1: Clarify (One by One)

**Step 1: Read the Daily Note**
Read the file the user specifies (typically their Obsidian daily note).
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

Move to the next task after each response. Keep momentum.

**Step 4: Rewrite Principles**
When suggesting rewrites:
- State the specific action
- Include context needed
- Define the done state
- Make it agent-handoff ready

Example:
- Before: "Make Google Drive AI Ready"
- After: "Organize Google Drive for AI access: Create 'AI-Ready' folder, move key docs, document what each folder contains"

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
