# Testing Plan for blackbelt-meeting-summary

## Pre-flight Checks

- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json` as `Skill(blackbelt-meeting-summary)`
- [ ] New terminal session started (settings refresh)
- [ ] Transcripts folder exists: `Zettelkasten/Transcripts/`
- [ ] Processed folder exists: `Zettelkasten/Transcripts/Processed/`

## Skill Discovery Test

- [ ] Run: "What skills are available?"
- [ ] Expected: `blackbelt-meeting-summary` appears in list with correct description

## Basic Invocation Test

- [ ] Run: "Process meeting transcripts"
- [ ] Expected: Skill activates, scans Transcripts folder, reports what it finds

## Happy Path Test

1. Place a sample transcript in `Zettelkasten/Transcripts/`
2. Name it something like `GamePlan-TestClient-Jan5.md`
3. Run: "Process meeting transcripts"
4. Expected:
   - [ ] Skill shows dry-run preview with detected client/type
   - [ ] AskUserQuestion lets you confirm or correct
   - [ ] After confirmation, generates summary
   - [ ] Summary saved to Zettelkasten
   - [ ] Link added to daily note Captures
   - [ ] Transcript moved to Processed folder
   - [ ] Copyable code block displayed

## Empty Folder Test

- [ ] Clear all files from Transcripts folder
- [ ] Run: "Process meeting transcripts"
- [ ] Expected: Skill reports "No transcripts to process"

## Multiple Transcripts Test

- [ ] Place 2-3 transcripts in folder
- [ ] Run: "Process meeting transcripts"
- [ ] Expected: All shown in preview table, can approve all or select individual

## Edge Cases

- [ ] File with no clear speaker labels: Should still process, may need manual client name
- [ ] Very long transcript (Game Plan 2hr): Should still generate summary within word limit
- [ ] Transcript with only one speaker: Handle gracefully

## Integration Test

- [ ] Verify ai-slop-detector skill is registered
- [ ] Check that summary passes through slop detector before save
- [ ] Verify daily note link format is correct

## Output Quality Check

- [ ] Summary is 250-400 words
- [ ] Voice sounds like Ed (direct, practical, Australian)
- [ ] Direct quotes are attributed properly
- [ ] Areas of concern are noted when present
- [ ] Ready to paste directly into Basecamp
