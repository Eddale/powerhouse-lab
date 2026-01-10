# Testing Plan for retrospective

## Pre-flight Checks

- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started (settings refresh)

## Skill Discovery Test

- [ ] Run: "What skills are available?"
- [ ] Expected: retrospective appears in list with correct description

## Basic Invocation Test

- [ ] Run: "weekly review"
- [ ] Expected: Skill activates, starts scanning daily notes

## Happy Path Test

**Input:** "run retrospective"

**Expected behavior:**
1. Scans last 7 days of daily notes
2. Presents week summary with Done counts by day
3. Shows top completions
4. Asks 4 reflection questions (one at a time)
5. Creates `Retrospective - YYYY-MM-DD.md` in Zettelkasten
6. Links in today's Captures section

## Edge Case Tests

- [ ] **No daily notes found:** Should report "No daily notes found for the past week" gracefully
- [ ] **Empty Done sections:** Should report 0 items shipped, still run reflection questions
- [ ] **Missing Captures section:** Should create section if it doesn't exist, or append

## Verification Steps

After running retrospective:

1. Check Zettelkasten for new file:
   ```
   ls -la ~/Documents/COPYobsidian/MAGI/Zettelkasten/Retrospective*.md
   ```

2. Read the generated file and verify:
   - Frontmatter is correct (type, date, shipped count)
   - Reflections captured accurately
   - "One Change" is present

3. Check today's daily note:
   - Captures section has link to retrospective doc
