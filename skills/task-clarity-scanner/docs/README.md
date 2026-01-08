# Task Clarity Scanner - Technical Reference

## What It Does

Scans daily notes using Personal Kanban structure. Identifies unclear tasks, manages Today's 3 vs Ready flow, flags stale items, suggests rewrites, and updates the file after approval.

## Architecture

```
task-clarity-scanner/
├── SKILL.md              # Main skill definition (Kanban + clarification)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load daily notes
- `Glob` - Find daily note files
- `Grep` - Search for patterns
- `Edit` - Update tasks
- `Write` - Create project files
- `AskUserQuestion` - Clarification workflow

**No external APIs.** Task management skill.

## Usage

**Trigger phrases:**
- "Scan my tasks"
- "Review my daily note"
- "Clarify my todos"
- "Check my task list"
- "Swap tasks"

**Input:** Daily note (auto-finds today's date if not specified)

**Output:** Clarified tasks, Kanban swaps, updated daily note

## Daily Note Location

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
```

## Kanban Structure

| Section | Purpose | WIP Limit |
|---------|---------|-----------|
| Ship This = Win Day | Single focus | 1 |
| Today's 3 | Active work | 3 |
| Ready | Backlog | None |
| Waiting For | Blocked items | None |
| Done Today | Completed | None |
| Captures | Document links | None |

## The Three Passes

1. **Pass 0: Health Check** - Count Today's 3, flag stale items, review Ready size
2. **Pass 1: Clarify** - One-by-one task clarification, project file creation
3. **Pass 2: Update** - Batch changes, apply edits after approval

## Task Categories

| Category | Meaning | Action |
|----------|---------|--------|
| Clear | Ready to act on | No changes needed |
| Unclear | Needs clarification | Suggest rewrite |
| Stale | Rolling 3+ days | Decision: do/delegate/drop |
| Done | Already completed | Move to Done Today |

## Staleness Tracking

Tasks use `(MM-DD)` suffix for age tracking:
- `- [ ] Task name (01-05)` - Created Jan 5
- `[STALE]` prefix added when rolling 3+ days

## Testing

**Manual verification:**
1. Run "scan my tasks"
2. Verify health check runs first
3. Confirm unclear tasks identified
4. Test Kanban swap interface
5. Verify edits applied correctly
