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

### Step 1: Read the Daily Note
Read the file the user specifies (typically their Obsidian daily note).
Look for the `## Key Tasks` section or any markdown task list (`- [ ]` items).

### Step 2: Analyze Each Task
For each task, evaluate:

| Check | Question |
|-------|----------|
| **Clarity** | Is it clear what needs to be done? |
| **Context** | Is there enough info to act on it? |
| **Actionability** | Could an agent execute this, or is it just a thought? |
| **Success Signal** | How would you know it's done? |

### Step 3: Categorize and Report
Present findings using bullet lists (NOT tables - they render poorly in terminal):

```
## Task Clarity Report

### Ready to Go
- **"[task]"** - Why it's clear, what agent could do

### Needs Clarification
- **"[task]"**
  - Issue: [what's unclear]
  - Suggested rewrite: "[agentic-ready version]"
  - What's needed: [missing context, link, etc.]

### Questions, Not Tasks
- **"[item]"** - This is a question to explore, not a task to complete
```

**Important:** Avoid markdown tables in output. Use bullets and bold for scannability.

### Step 4: Suggest Rewrites
For unclear tasks, suggest a rewrite that:
- States the specific action
- Includes the context needed
- Has a clear done state
- Could be handed to an agent

**Example transformation:**
- Before: "Make Google Drive AI Ready"
- After: "Organize Google Drive for AI access: Create an 'AI-Ready' folder, move key documents there, and note which files are reference vs working docs"

### Step 5: Get Approval
For each unclear task, offer options:

1. **Clarify now** - Ed provides the missing context
2. **Accept rewrite** - Use the suggested rewrite
3. **Skip for now** - Leave as-is, move on
4. **Move to Someday/Maybe** - Park it in a separate file for later review

Use AskUserQuestion to confirm which tasks to update and how.

Present the specific changes that will be made before making them.

### Step 6: Update the File
If approved:
- Use the Edit tool to modify the original file
- Replace vague tasks with the approved rewrites
- Preserve all other content exactly as-is
- Confirm: "Updated [N] tasks in your daily note."

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
