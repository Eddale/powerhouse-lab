# Testing Plan for morning-metrics

## Pre-flight Checks

- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started (settings refresh)
- [ ] Google credentials exist at `~/.config/claude-code-apis/credentials.json`
- [ ] Token exists at `~/.config/claude-code-apis/token.pickle`

## Script Direct Test

```bash
python3 skills/morning-metrics/scripts/fetch_metrics.py
```

**Expected:** JSON output with gmail and calendar sections, both showing `"status": "ok"`

## Skill Discovery Test

- [ ] Run: "What skills are available?"
- [ ] Expected: morning-metrics appears in list

## Basic Invocation Test

- [ ] Run: "morning metrics"
- [ ] Expected: Skill activates, runs script, formats briefing

## Happy Path Test

**Input:** "check my metrics"

**Expected output:**
- Date header with current date
- Calendar section with meeting count and list
- Email section with unread counts
- No errors displayed

## Alternative Trigger Tests

- [ ] "show my stats" - should invoke skill
- [ ] "what's my day look like" - should invoke skill

## Error Handling Tests

### Missing Token
```bash
mv ~/.config/claude-code-apis/token.pickle ~/.config/claude-code-apis/token.pickle.bak
```
- [ ] Run: "morning metrics"
- [ ] Expected: Should trigger re-auth or report auth needed
- [ ] Restore: `mv ~/.config/claude-code-apis/token.pickle.bak ~/.config/claude-code-apis/token.pickle`

### No Internet
- [ ] Disconnect wifi, run "morning metrics"
- [ ] Expected: Graceful error message, not a crash

## Integration Test

- [ ] Run as part of win-the-day agent (when built)
- [ ] Verify metrics display before capture triage
