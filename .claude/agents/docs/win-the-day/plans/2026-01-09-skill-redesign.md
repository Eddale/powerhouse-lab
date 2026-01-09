# Win The Day: Agent → Skill Redesign

**Created:** 2026-01-09
**Shipped:** 2026-01-10
**Status:** Complete (v1.0)
**Trigger:** Ed's daily non-negotiables requirement + research findings on agent overhead

## The Problem

Win-the-day as an agent has latency issues:
- Context initialization overhead
- Resume cycles between skill calls
- Tool deliberation for sequential steps

This contradicts the interactive, "Ed is watching" nature of the morning routine.

## The Solution

Convert win-the-day from an AGENT to a SKILL that:
1. Executes directly (no agent spawn overhead)
2. Calls other skills inline (capture-triage, task-clarity-scanner)
3. Integrates with the new Daily Non-Negotiables template section
4. Adds metrics briefing capabilities

## Daily Non-Negotiables (Template - DONE)

Added to `Templates/Journal (template).md`:
- Weekday-only conditional (Mon-Fri)
- Checkboxes for each non-negotiable:
  - Check metrics (Substack, revenue, social, email)
  - Calendar review
  - BlackBelt FB check
  - Capture triage
  - Newsletter touch
  - AI tool improvement

## Win-The-Day Skill Pipeline

When Ed says "win the day", the skill should:

### Phase 1: Metrics Briefing
1. **Substack stats** - Via Claude in Chrome (dashboard scrape)
2. **Calendar** - Show today's meetings (need integration approach)
3. **Email/inbox** - Unread count summary
4. **Revenue** - Stripe dashboard or summary

### Phase 2: Capture Processing
1. Run capture-triage skill on Drafts inbox
2. Route approved items to Ready section
3. Summarize what was processed

### Phase 3: Task Clarity
1. Run task-clarity-scanner on today's note
2. Address stale items, clarify unclear tasks
3. Confirm Today's 3 is set

### Phase 4: Morning Summary
Output a clean status report with:
- Metrics snapshot
- Captures processed
- Board status
- Today's focus (Ship This = Win Day)

## Implementation Approach

### Option A: Single Skill with Inline Calls
```
skills/win-the-day/SKILL.md
```
- The skill instructions tell Claude to run other skills
- No agent overhead, direct execution
- Relies on Claude's skill discovery

### Option B: Orchestrator Skill with Sub-Skills
```
skills/win-the-day/SKILL.md (orchestrator)
skills/morning-metrics/SKILL.md (new)
skills/capture-triage/SKILL.md (existing)
skills/task-clarity-scanner/SKILL.md (existing)
```
- Each component is independently callable
- win-the-day orchestrates the sequence
- More modular, can run pieces standalone

**Recommendation:** Option B - modularity lets Ed run "just check metrics" or "just triage captures" without full routine.

## Metrics Briefing: Platform Access

| Platform | Access Method | v1 Scope | Future |
|----------|---------------|----------|--------|
| Substack | Browser (Claude in Chrome) | Dashboard stats | API if available |
| Calendar | Google Calendar API | Today's meetings list | Smart scheduling awareness |
| Email | Gmail API | Surface action-required emails | Smart triage, newsletters → read tasks |
| Revenue | Stripe API or dashboard | Daily awareness | Trend tracking |

**Ed's preference:** APIs over browser automation for speed and reliability.

## Email Intelligence (Gmail API)

**v1 Scope:**
- Surface emails that clearly require action from Ed
- Filter out newsletters, notifications, automated stuff
- Show sender, subject, quick preview

**Future Vision:**
- Turn useful emails into tasks automatically
- Newsletters become "read" tasks with links
- Learn who Ed interacts with, prioritize accordingly

## Open Questions (Answered)

1. **Calendar:** Google Calendar, synced to Mac client. Use API.
2. **Email:** Gmail API. v1 = action-required emails only.
3. **Revenue:** Yes, daily awareness. Source TBD (likely Stripe).
4. **BlackBelt FB:** Manual check for now (in template checklist).

## Next Steps

1. [x] Ed answers open questions (done via AskUserQuestion session)
2. [x] Set up Google Calendar API access
3. [x] Set up Gmail API access
4. [x] Create morning-metrics skill (Substack + Calendar + Email + Revenue)
5. [x] Move win-the-day from `.claude/agents/` to `skills/`
6. [x] Update skill to call sub-skills inline
7. [x] Test full pipeline (2026-01-10 morning routine)

---

## v1.0 Shipped - 2026-01-10

**What's working:**
- Gmail API: unread counts + important email preview
- iCloud: unread counts
- Google Calendar API: today + upcoming events from all calendars
- Morning-metrics skill: `fetch_metrics.py` returns clean JSON
- Win-the-day skill: orchestrates metrics → captures → tasks → summary
- Capture-triage integration: checks Inbox folder
- Task-clarity-scanner integration: reviews board status

**Not yet built (v1.1 candidates):**
- Substack stats (dashboard scrape via Claude in Chrome)
- Revenue/Stripe daily awareness
- Email intelligence (action-required filtering vs just unread count)

---

*Plan created via interactive Q&A session with Ed*
