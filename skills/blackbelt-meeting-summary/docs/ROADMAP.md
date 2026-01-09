# BlackBelt Meeting Summary - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial transcript processing with template |
| v1.1 | 2026-01 | Dry-run preview before processing |
| v1.2 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |
| v2.0 | 2026-01-10 | **Basecamp API integration** - post summaries directly to client todos |

## The Vision

Right now, this skill processes transcripts you drop into a folder. You still need to record, transcribe, and initiate the process.

The vision: transcripts arrive automatically, get processed in the background, and summaries appear in Basecamp without you lifting a finger.

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **MacWhisper Integration** - Auto-detect when MacWhisper finishes a transcription and move it to the watch folder. Remove the manual file drop step.

- [ ] **Client Name Memory** - Remember client names from previous sessions. If "GamePlan-Jan5.md" was Bren last time, assume it's Bren this time unless filename says otherwise.

- [ ] **Concern Flagging** - Highlight potential issues more prominently. If someone mentions feeling overwhelmed, stuck, or frustrated, surface that clearly in the summary.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Waiting For Call Links** - When processing a call summary, auto-link it to any Waiting For items for that client. The Waiting For docs have a `call-links: []` frontmatter field ready for this. When summary is created, search for matching client name in `/Waiting For/` folder and append the call link. This builds a contact history over time.

- **Call Trend Tracking** - Over time, track patterns across calls. "Christy mentioned confidence issues in 3 of last 5 Velocity calls."

- **Automatic Session Type Detection** - Use call duration + content patterns to guess Game Plan vs Velocity vs Red. Currently relies on filename.

- **Quote Highlighting** - When displaying the Basecamp summary, highlight the direct quotes so they're easy to verify against transcript.

- **Multi-Client Calls** - Handle calls with multiple clients (rare but happens). Would need different template structure.

- **Audio Direct Processing** - Skip the transcription step entirely. Upload audio, get summary. Would need Whisper API integration.

- **Slack Notifications** - When summaries are ready, ping a Slack channel. Useful if processing happens in the background.

## What We've Learned

Building this skill taught us a few things:

**The dry-run pattern is essential.** Early versions just processed everything. Wrong client names ended up in summaries. The preview step adds 10 seconds but prevents embarrassing mistakes.

**Direct quotes make summaries valuable.** A summary without quotes feels like a report. A summary with quotes feels like you were there. Always include 1-3 direct quotes.

**The "Call Vibes" section catches what data misses.** Metrics don't show if someone's losing steam. But "they sounded tired" or "energy was low" gives the ops team early warning.

**250-400 words is the sweet spot.** Shorter and you miss important context. Longer and nobody reads it. This range forces prioritization.

**Running through slop detector matters.** AI-generated summaries sound generic. The cleanup pass makes them sound like notes you'd actually write.

**Basecamp API is simpler than expected.** Despite no search API, the consistent todo naming convention (`DD.MM.YYYY | Client Name | (email) | Location`) makes fuzzy matching reliable. OAuth setup took ~15 min total. The refresh token lasts 10 years, so we won't need to re-auth for a long time.

**Post to todos, not messages.** The BB Onboarding Queue uses a todo list structure with groups (Template, Holding Pen, For 1st Velocity, etc.). Clients move between groups but keep the same todo ID. Comments on todos notify all subscribers automatically.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
