# Retrospective - Technical Reference

## What It Does

Scans the last 7 days of daily notes, extracts Done items, presents a week summary, facilitates reflection through structured questions, and saves the output as a searchable Zettelkasten document.

## Dependencies

**Tools required:** Read, Write, Edit, Glob, Grep, AskUserQuestion

**Data sources:**
- Daily notes at `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md`
- Parses `## Done Today` section from each

## Usage

**Trigger phrases:**
- "weekly review"
- "run retrospective"
- "what did I ship this week"
- "end of week review"
- "reflect on my week"

## Data Flow

```
1. Glob last 7 daily notes
2. Read each, extract ## Done Today items
3. Count completions by day
4. Present summary
5. Ask 4 reflection questions (AskUserQuestion)
6. Save to Zettelkasten
7. Link in today's Captures
```

## Output Location

Retrospective docs saved to:
```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Retrospective - YYYY-MM-DD.md
```

## Testing

1. Trigger with "weekly review"
2. Verify it finds recent daily notes
3. Verify Done count is accurate
4. Complete reflection questions
5. Verify output doc created
6. Verify link added to today's Captures

## Known Limitations

- Only scans last 7 days (by design - weekly scope)
- Requires daily notes to exist with `## Done Today` section
- No automatic pattern detection (manual reflection only)
