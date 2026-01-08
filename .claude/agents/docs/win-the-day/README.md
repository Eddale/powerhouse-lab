# Win The Day Agent - Technical Reference

## Overview

The Win The Day agent is a morning routine facilitator that guides the user through capture triage and task clarity. It helps start the day with intention by processing outstanding items and ensuring focus on what matters.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
skills: capture-triage, task-clarity-scanner
```

## Trigger Phrases

- "win the day"
- "morning routine"
- "start my day"
- "let's get at it"
- Any request to begin daily review

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read daily notes, inbox, task lists |
| Write | Create/update daily notes |
| Edit | Update task status |
| Glob | Find files (inbox, notes) |
| Grep | Search for tasks, captures |
| AskUserQuestion | Guide user through decisions |

## Skills Used

- **capture-triage** - Process items in the Inbox folder
- **task-clarity-scanner** - Review and clarify tasks in daily note

## Routine Sequence

1. **Inbox Check** - Are there captures waiting to be triaged?
2. **Capture Triage** - Process inbox items (if any)
3. **Task Scan** - Review tasks in Ready and Today's 3
4. **Clarity Check** - Are tasks clear and actionable?
5. **Day Setup** - Confirm Today's 3 priorities

## Personal Kanban Integration

Works with Ed's Personal Kanban structure:
- **Today's 3** - Maximum 3 tasks for today
- **Ready** - Clarified tasks ready to work
- **Waiting For** - Items blocked on others

## Output

The agent doesn't create new files - it updates existing structures:
- Daily note tasks get clarified
- Inbox items get routed
- Today's 3 gets confirmed

## Interaction Pattern

This is an interactive agent. It asks questions, presents options, and confirms decisions. Not designed for automation - the morning routine benefits from human engagement.
