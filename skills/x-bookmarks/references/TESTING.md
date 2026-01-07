# Testing Plan for x-bookmarks

## Pre-flight Checks

- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started (settings refresh)
- [ ] bird CLI installed: `which bird`
- [ ] Twitter auth configured (auth_token + ct0)

## Prerequisites Test

Before testing the skill, verify bird CLI works:

```bash
# Check bird is installed
bird --version

# Test fetching (should return JSON)
bird bookmarks -n 1 --json
```

**Expected:** JSON output with at least one bookmark.

**If 403 error:** Twitter cookies expired - get fresh ones from browser.

## Skill Discovery Test

- [ ] Run: "What skills are available?"
- [ ] Expected: x-bookmarks appears in list with description about Twitter bookmarks

## Basic Invocation Test

- [ ] Run: "fetch my twitter bookmarks"
- [ ] Expected: Skill activates, attempts to run bird CLI

## Happy Path Test

- [ ] Input: "process my X bookmarks" (with bird CLI configured)
- [ ] Expected:
  1. Fetches bookmarks via bird CLI
  2. Expands t.co links
  3. Creates .md files in Inbox folder
  4. Reports summary of what was processed

## Verification

After running, check:

```bash
# Should see new x-*.md files
ls /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/x-*.md

# Check content of one file
cat /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/x-*.md | head -30
```

## Edge Case Tests

### No bird CLI
- [ ] Run skill without bird installed
- [ ] Expected: Clear error message about installing bird CLI

### Auth expired
- [ ] Run with expired Twitter cookies
- [ ] Expected: Clear error about refreshing auth

### No new bookmarks
- [ ] Run twice in a row
- [ ] Expected: Second run reports "no new bookmarks" (duplicates skipped)

### Empty bookmarks
- [ ] Run when Twitter bookmarks are empty
- [ ] Expected: Graceful "no bookmarks found" message

## Integration Test

After x-bookmarks drops files to Inbox:

- [ ] Run capture-triage skill
- [ ] Expected: x-bookmark files classified as REFERENCE
- [ ] Expected: Routes to Ready section as "Review: [title]"

## Performance Test

- [ ] Fetch 20 bookmarks
- [ ] Expected: Completes in under 2 minutes
- [ ] Check: All 20 files created in Inbox

## Cleanup

After testing:
```bash
# Remove test files from Inbox
rm /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/x-*.md
```
