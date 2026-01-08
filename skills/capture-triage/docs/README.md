# Capture Triage - Technical Reference

## What It Does

Processes mobile captures from Drafts Pro, classifies them by intent, and routes them to the Ready queue as actionable tasks. Follows a preview → approve → route pipeline to prevent accidental processing.

## Architecture

```
capture-triage/
├── SKILL.md              # Main skill definition (classification + routing)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/            # Improvement plans
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load capture files and daily notes
- `Glob` - Find files in Inbox folder
- `Grep` - Search for project matches
- `Edit` - Append tasks to daily note Ready section
- `Write` - Create CONTACT notes
- `AskUserQuestion` - Preview approval flow

**Related skills:**
- `mission-context` - Pulls active project names for matching
- `task-clarity-scanner` - Downstream processing of Ready queue
- `research-swarm` - Spawned for RESEARCH classifications (opt-in)

## Paths

```
Inbox folder:  /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
Processed:     /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/Processed/
Daily note:    /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
```

## Usage

**Trigger phrases:**
- "Triage captures"
- "Process captures"
- "Check my captures"

**Input:** .md files in Inbox folder (from Drafts Pro)

**Output:**
- Tasks added to daily note `## Ready` section
- CONTACT notes created if people mentioned
- Original files moved to Processed/ folder

## Classification Types

| Type | Signal | Routing |
|------|--------|---------|
| TASK | Starts with verb (call, email, buy) | Ready: `- [ ] [action] (MM-DD)` |
| IDEA | "What if..." or speculative | Ready: `- [ ] Consider: [idea] (MM-DD)` |
| REFERENCE | Links, summaries, observations | Ready: `- [ ] Review: [title] (MM-DD)` |
| RESEARCH | `Research:` hint or investigation needed | Spawn research-swarm (opt-in) |
| PROJECT_UPDATE | Mentions active project | Append to project file |
| CONTACT | Person name + action | Create/update CONTACT note |

**Priority Rule:** Inline hints (`IDEA:`, `Research:`, `Task:`) override auto-detection.

## Processing Pipeline

1. **Scan** - Find .md files in Inbox/ (root only, not subdirectories)
2. **Context** - Load project names from mission-context + Glob
3. **Classify** - Detect intent using inline hints or signals
4. **Preview** - Show classification table, pause for user to absorb
5. **Decide** - Ask: Approve all / Go one-by-one / Modify / Skip
6. **Route** - Add to Ready section, create CONTACT notes
7. **Research** - Spawn research-swarm if approved
8. **Archive** - Move originals to Processed/
9. **Summarize** - Report what was done

## Testing

**Manual verification:**
1. Drop test .md files in Inbox folder
2. Run "triage captures"
3. Verify preview table appears
4. Approve and check daily note Ready section
5. Confirm files moved to Processed/

**Quality checks:**
- [ ] Only reads root of Inbox/ (not subdirectories)
- [ ] Shows preview before any changes
- [ ] Tasks go to Ready section (not Captures)
- [ ] Inline hints override auto-detection
- [ ] Research-swarm only spawns if approved
- [ ] Originals preserved in Processed/

## Known Limitations

- Single-user system (Ed's Zettelkasten paths hardcoded)
- No undo - but originals preserved in Processed/
- Research-swarm is background only (no inline results)
- Can't process images or non-.md captures
