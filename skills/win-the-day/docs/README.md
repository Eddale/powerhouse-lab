# Win The Day - Technical Reference

## What It Does

Orchestrates Ed's morning routine by calling three sub-skills in sequence:
1. **morning-metrics** - Email counts, calendar events
2. **capture-triage** - Process Drafts inbox
3. **task-clarity-scanner** - Review and clarify tasks

Produces a consolidated morning briefing.

## Dependencies

**Tools required:** `Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion`

**Sub-skills called:**
- `morning-metrics` - Via Python script
- `capture-triage` - Via skill invocation
- `task-clarity-scanner` - Via skill invocation

## Architecture

```
win-the-day orchestrates:
    │
    ├── morning-metrics (Python script)
    │   └── fetch_metrics.py → JSON
    │
    ├── capture-triage (skill)
    │   └── Drafts inbox → Ready section
    │
    └── task-clarity-scanner (skill)
        └── Board review → clarified tasks
```

## Usage

**Trigger phrases:**
- "win the day"
- "morning routine"
- "start my day"
- "let's get at it"

**Automation mode:**
- "win the day automatically"
- Skips interactive prompts, just reports status

## Data Flow

1. Metrics script runs → JSON output
2. Claude formats metrics summary
3. capture-triage skill invoked → waits for completion
4. task-clarity-scanner skill invoked → waits for completion
5. Claude compiles final summary

## Migration Notes

**Converted from:** `.claude/agents/win-the-day.md`

**Why skill instead of agent:**
- Faster execution (no subprocess spawn)
- Better for interactive "Ed is watching" workflows
- Direct tool access without agent overhead
