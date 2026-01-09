---
name: win-the-day
description: Morning routine facilitator. Guides Ed through metrics, capture triage, and task clarity. Use at start of day with "win the day", "morning routine", "start my day", "let's get at it".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Win The Day

Ed's morning routine - metrics briefing, capture processing, and task clarity in one flow.

## Philosophy

This is a **guided workflow** where:
- Each step presents information or options
- Ed makes all decisions
- You orchestrate the sequence, Ed makes the calls
- Keep it fast - Ed is watching

## The Pipeline

Run these steps in sequence:

### Step 1: Morning Metrics

Run the morning-metrics skill to get the lay of the land:

```bash
python3 /Users/eddale/Documents/GitHub/powerhouse-lab/skills/morning-metrics/scripts/fetch_metrics.py
```

Parse the JSON and present a clean summary:

```markdown
### Metrics Snapshot
**Email**
- Gmail: [X] unread ([Y] primary)
- iCloud: [X] unread

**Calendar**
- Today: [N] meetings
- [List if any]
- Tomorrow preview: [N] meetings

**Flagged:** [Any urgent items - meetings in next 2 hours, important emails]
```

### Step 2: Process Captures

Invoke the **capture-triage** skill to process the Drafts inbox.

Say: "Now let's triage your captures."

The skill will:
- Check for files in the Inbox folder
- Classify and present a preview
- Route approved items to Ready

Note the summary for your final report.

### Step 3: Clarify Tasks

Invoke the **task-clarity-scanner** skill to review the board.

Say: "Let's review your tasks."

The skill will:
- Check Today's 3, Ready queue, stale items
- Present unclear items for clarification
- Apply approved changes

Note the board status for your final report.

### Step 4: Morning Summary

After all steps complete, provide the consolidated report:

```markdown
## Win The Day - [Date]

### Metrics
- Gmail: [X] unread | iCloud: [X] unread
- Today: [N] meetings | Tomorrow: [N] meetings
- [Any urgent flags]

### Captures
- Processed: [N] items
- [Notable items routed]

### Board Status
- Today's 3: [Status]
- Ready: [N] items
- Focus: [Ship This = Win Day]

### Ready to Win
[One line: key priority or any blockers]
```

## Automation Mode

If Ed says "win the day automatically" or "run the whole morning routine":
- Run metrics (always show the summary)
- Skip capture-triage if Inbox is empty
- Skip task-clarity-scanner interactive prompts - just report board status
- Present the final summary

## Trigger Phrases

- "win the day"
- "morning routine"
- "start my day"
- "let's get at it"
- "daily review"

## Guidelines

- **Speed matters** - Ed is watching, keep it snappy
- **Don't over-explain** - Brief summaries, not essays
- **Flag anomalies** - Unusually high unreads, meetings soon, stale tasks
- **Respect the flow** - Complete each step before moving on
