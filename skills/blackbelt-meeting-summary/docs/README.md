# BlackBelt Meeting Summary - Technical Reference

## What It Does

Processes transcripts from BlackBelt coaching calls and generates Basecamp-ready summaries. Follows a scan → preview → confirm → process pipeline to ensure accurate client and session type detection before processing.

## Architecture

```
blackbelt-meeting-summary/
├── SKILL.md              # Main skill definition (template + workflow)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/            # Improvement plans
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load transcript files
- `Write` - Save summary documents to Zettelkasten
- `Edit` - Update daily notes with links
- `Glob` - Find transcripts in watch folder
- `Grep` - Search transcript content for patterns
- `AskUserQuestion` - Dry-run preview before processing
- `Bash` - Run Basecamp posting tool

**Related skills:**
- `ai-slop-detector` - Cleans summaries before saving

**External APIs:**
- Basecamp API (OAuth 2.0) - Post summaries directly to client todos

## Watch Folder

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Transcripts/
```

Processed transcripts move to `Transcripts/Processed/`.

## Usage

**Trigger phrases:**
- "Process meeting transcripts"
- "Summarize BlackBelt meetings"
- "Check for new transcripts"

**Input:** Transcript files (.md or .txt) in the watch folder

**Output:**
- Basecamp-ready summary (250-400 words)
- Saved to Zettelkasten with frontmatter
- Link added to daily note Captures

## Session Types

| Type | Duration | Focus |
|------|----------|-------|
| Game Plan | 45min-2hr | Onboarding strategy, foundations |
| Velocity | 20min | Progress check, adjustments |
| Red | 20min | Emergency/issue resolution |

## Processing Pipeline

1. **Scan** - Find unprocessed transcripts in watch folder
2. **Preview** - Show detected client + type, ask for confirmation
3. **Process** - Generate summary using template
4. **Clean** - Run through ai-slop-detector
5. **Save** - Write to Zettelkasten, update daily note
6. **Archive** - Move original transcript to Processed/

## Summary Template Sections

- Summary (2-3 paragraphs, includes direct quotes)
- Key Focus Areas
- Trainings Highlighted / Assigned
- Requests / Follow-Ups for BlackBelt Team
- Momentum & Culture - Call Vibes
- Next Steps / Action Items

## Testing

**Manual verification:**
1. Drop a test transcript in the watch folder
2. Run "process meeting transcripts"
3. Verify preview table appears before processing
4. Check summary matches template structure
5. Confirm file saved to Zettelkasten
6. Verify daily note updated

**Quality checks:**
- [ ] Client name detected or prompted
- [ ] Session type correct
- [ ] Summary length 250-400 words
- [ ] Direct quotes included and attributed
- [ ] No AI slop in final output
- [ ] Original transcript moved to Processed/

## Basecamp Integration

Post summaries directly to client todos in the BB Onboarding Queue.

**Setup:** Credentials stored in `~/.config/blackbelt-basecamp.yaml`

**How it works:**
1. Searches for client by name across all onboarding groups
2. Fuzzy matches to handle name variations
3. Posts as HTML comment on client's todo
4. Team members subscribed to the todo get notified

**Tools:** Located in `tools/` folder
- `basecamp_client.py` - API client library
- `post_to_basecamp.py` - CLI tool for posting

**Manual usage:**
```bash
python3 tools/post_to_basecamp.py --client "Brad Twynham" --summary /path/to/summary.md
python3 tools/post_to_basecamp.py --list-clients "Brad"  # Search for clients
```

## Known Limitations

- Requires readable transcript format (MacWhisper output works well)
- Can't auto-detect client from speaker diarization
- Doesn't handle multi-client calls
- Basecamp access token expires every 2 weeks (auto-refresh available)
