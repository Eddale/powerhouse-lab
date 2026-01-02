# Waiting For Tracking - Research & Design

**Date**: 2026-01-02
**Purpose**: Design a "Waiting For" tracking system that integrates with email, Obsidian, and Claude agents

---

## 1. GTD METHODOLOGY - "WAITING FOR" LIST

### Core Principles (David Allen's GTD)

The "Waiting For" list is one of GTD's fundamental tracking contexts. It captures:

**What It Tracks:**
- Items delegated to others
- Responses you're expecting
- Deliverables someone owes you
- Follow-up items on hold

**Why It Matters:**
- Frees your mind from tracking "did they respond yet?"
- Enables systematic follow-up without being pushy
- Prevents dropped balls on delegated work
- Creates accountability without micromanaging

**Key Elements to Track:**
1. **What** - The specific item/response expected
2. **Who** - Person responsible
3. **When** - Date you initiated (sent email, made request)
4. **Expected By** - Optional deadline or follow-up date
5. **Context** - Why it matters, what it blocks

### GTD Review Rhythm

- **Daily** - Scan for urgent follow-ups
- **Weekly Review** - Review entire list, decide on follow-ups
- **On Completion** - Archive with notes on outcome

---

## 2. EMAIL-BASED TRACKING PATTERNS

### Pattern A: Label/Folder System

**Gmail Labels:**
```
Waiting For/
├── Urgent (needs response this week)
├── Normal (standard timeline)
└── FYI (sent info, don't expect response)
```

**Workflow:**
1. Send email
2. Apply "Waiting For" label
3. Set expected response date (Gmail reminder/snooze)
4. When reply arrives → remove label, move to reference

**Pros:** Simple, visual, works in Gmail
**Cons:** Manual tagging, no structured data

### Pattern B: Sent Folder + Search

**Approach:**
- All sent emails are automatically in "Sent"
- Use search operators to find unreplied emails
- Gmail search: `in:sent -has:userlabels -in:chats`

**Pros:** Zero overhead, automatic
**Cons:** Hard to distinguish "expecting reply" from "FYI emails"

### Pattern C: BCC to Tracking System

**Approach:**
- BCC a special email address (like waitingfor@yourdomain.com)
- System logs the email data
- Tracks until reply detected

**Pros:** Automatic capture, structured database
**Cons:** Requires backend system, BCC feels clunky

### Pattern D: Email Client Rules

**Approach:**
- Create rule: "If I send email to X, copy to Waiting For folder"
- Review folder periodically
- Delete when resolved

**Pros:** Automatic, works in any email client
**Cons:** No detection of replies, manual cleanup

---

## 3. INTEGRATION PATTERNS FOR OBSIDIAN

### Pattern A: Daily Note Integration

**Template Addition:**
```markdown
## Waiting For

```dataview
TABLE
  person as "Who",
  item as "What",
  sent as "Sent",
  expected as "Expected By",
  days as "Days Waiting"
FROM "waiting-for"
WHERE status = "pending"
SORT expected asc
```

### Pattern B: Dedicated Waiting For Note

**Location:** `system/Waiting For.md`

**Structure:**
```markdown
# Waiting For

## Active

- [ ] **[Person Name]** - Brief description #waiting-for
  - Sent: 2026-01-02
  - Expected: 2026-01-05
  - Context: [[Related Project]]
  - Email: [[Link to sent email]]

## Resolved

- [x] **[Person Name]** - Brief description
  - Sent: 2025-12-28
  - Resolved: 2026-01-02
  - Outcome: Got the answer, moved forward
```

### Pattern C: Inline in Project Notes

**Approach:**
- Track "Waiting For" items directly in project notes
- Use tags to surface across vault
- Query with Dataview

**Example:**
```markdown
## Project: Newsletter Launch

### Next Actions
- [ ] Draft issue #2
- [ ] Upload to Substack

### Waiting For
- [ ] Logo from designer (sent 2026-01-01) #waiting-for
- [ ] Legal review from Sarah (sent 2025-12-30) #waiting-for
```

---

## 4. AUTOMATION OPTIONS

### Option A: Gmail API - Reply Detection

**What's Possible:**
- Search for threads where you sent last message
- Detect when new message arrives in thread
- Automatically mark "Waiting For" as resolved

**Implementation:**
```python
# Pseudocode
def check_replies():
    threads = get_threads_where_i_sent_last()
    for thread in threads:
        if new_message_from_other_person(thread):
            mark_resolved(thread.id)
            notify_user(thread.subject)
```

**Pros:** Fully automated, accurate
**Cons:** Requires Gmail API setup, auth, scheduled checks

### Option B: IMAP Monitoring

**What's Possible:**
- Monitor IMAP folders
- Track sent emails with special tag
- Watch for replies via thread ID

**Pros:** Works with any email provider
**Cons:** More complex than Gmail API, threading can be messy

### Option C: Manual Check + Smart Reminder

**What's Possible:**
- Log sent emails manually or via shortcut
- Set reminder dates
- Claude agent checks list daily, surfaces overdue items

**Pros:** Simple, no API complexity
**Cons:** No automatic resolution, relies on manual logging

### Option D: iOS Shortcut Trigger

**What's Possible:**
- After sending email via iOS Mail
- Trigger shortcut to log to Obsidian
- Create waiting-for entry with metadata

**Pros:** Mobile-friendly, automatic at send time
**Cons:** iOS only, requires Shortcut setup

---

## 5. RECOMMENDED PATTERN FOR ED

### The System Design

**Philosophy:**
Start simple, automate progressively. Think of it like a "sent email swipe file" that prompts you for follow-up.

### Components

#### A. Email Sending (Capture)

**Option 1 - Manual Log (MVP):**
- After sending important email
- Run iOS Shortcut or desktop command
- Logs to Obsidian: `waiting-for/YYYY-MM-DD-person-name.md`

**Option 2 - Semi-Automatic:**
- BCC special email address
- Zapier/Make catches it
- Creates Obsidian note via API

**Option 3 - Full Auto (Future):**
- Gmail API monitors sent folder
- Filters for non-FYI emails (heuristic: subject contains "?", sent to specific people)
- Auto-creates waiting-for entries

#### B. Storage (Obsidian)

**Folder Structure:**
```
waiting-for/
├── _template.md
├── active/
│   ├── 2026-01-02-jane-logo-design.md
│   └── 2026-01-01-bob-contract-review.md
└── resolved/
    └── 2025-12-28-sarah-calendar-link.md
```

**Note Template:**
```markdown
---
person: Jane Doe
email: jane@example.com
subject: "Logo design for Newsletter"
sent: 2026-01-02
expected: 2026-01-05
status: pending
priority: normal
project: "[[Newsletter Launch]]"
---

# Waiting For: Jane - Logo Design

## What I'm Waiting For
Final logo files (PNG + SVG) for newsletter header

## Context
Sent mockup and brand colors. Need this before Issue #2 launches on Jan 10.

## Email Thread
- Sent: [[Link to sent email or copy/paste]]
- Subject: Logo design for Newsletter
- Key points: Asked for 3 variations, horizontal lockup

## Follow-Up Plan
- If no response by Jan 5 → Gentle nudge
- If no response by Jan 7 → Find backup designer

## Resolution
<!-- Fill when resolved -->
```

#### C. Daily Surfacing (Integration)

**Add to Daily Note Template:**
```markdown
## Follow-Ups Needed

```dataview
TABLE
  person,
  subject,
  sent,
  expected as "Expected By"
FROM "waiting-for/active"
WHERE expected <= date(today) + dur(2 days)
SORT expected asc
```

**Translation for Ed:**
This query is like your "emails that need a follow-up" folder, automatically pulled into your daily note. You see what's coming due in the next 2 days.

#### D. Reply Detection (Future Automation)

**Phase 1 - Manual:**
- When you get reply, move note to `waiting-for/resolved/`
- Add outcome notes

**Phase 2 - Assisted:**
- Claude agent scans Gmail API daily
- Finds threads where you sent last message
- Checks if reply received
- Suggests which waiting-for items to close

**Phase 3 - Automatic:**
- Gmail API monitors threads
- Auto-moves notes to resolved
- Notifies you in daily note

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Manual MVP (Ship in 1 session)

**What:**
- Create Obsidian folder structure
- Template for waiting-for notes
- Add Dataview query to daily note template
- iOS Shortcut to create waiting-for note

**How It Works:**
1. Send email
2. Run shortcut (input: person, subject, expected date)
3. Creates note in `waiting-for/active/`
4. Shows up in tomorrow's daily note if due soon
5. Manually move to resolved when reply comes

**Leverage:**
You never forget to follow up. Your daily note reminds you who you're waiting on.

### Phase 2: Semi-Automatic (2-3 sessions)

**What:**
- Add Gmail API integration
- Claude agent that scans sent emails
- Suggests waiting-for items to create
- Detects replies, suggests closing items

**How It Works:**
1. Send email (normal process)
2. Daily: Claude agent reviews sent folder
3. Prompts: "Did you want to track these as waiting-for?"
4. You approve → creates notes
5. Detects replies → suggests resolution

**Leverage:**
Reduces manual logging, automatic detection of replies.

### Phase 3: Full Automation (Future)

**What:**
- Auto-creates waiting-for for specific people/subjects
- Auto-resolves when reply detected
- Integrates with task management for blocked items
- Weekly summary of aging waiting-for items

**How It Works:**
1. Send email → automatic log (smart filtering)
2. Reply arrives → automatic resolution
3. Weekly: "Here are 3 items aging, want to follow up?"

**Leverage:**
Zero overhead tracking, intelligent follow-up prompts.

---

## 7. TECHNICAL CONSIDERATIONS

### Gmail API Access

**What You Need:**
- Google Cloud project
- Gmail API enabled
- OAuth2 credentials
- Read access to sent/inbox

**Scopes Required:**
- `gmail.readonly` - Read emails
- `gmail.metadata` - Thread IDs, subjects

**Rate Limits:**
- 250 quota units per user per second
- 1 billion quota units per day
- Sufficient for personal use

### Thread Detection Logic

**Challenge:**
How do you know an email is a "reply" to one you sent?

**Solution:**
```python
def is_reply_received(thread_id):
    messages = get_thread_messages(thread_id)

    # Get last message you sent
    my_last_message = find_last_message_from_me(messages)

    # Check if there's a message after yours from someone else
    messages_after = [m for m in messages if m.date > my_last_message.date]

    return len(messages_after) > 0
```

### Obsidian Integration

**Options:**
1. **File System** - Direct write to vault folder
2. **Obsidian Local REST API** - Plugin that exposes REST API
3. **Git Sync** - Commit from script, Obsidian pulls
4. **Templater + Dataview** - Manual with smart queries

**Recommended:**
Start with file system writes (simplest). Obsidian auto-detects new files.

---

## 8. WORKFLOW DIAGRAM

```
┌─────────────────┐
│  Send Email     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Capture Decision       │
│  - Manual shortcut      │
│  - BCC trigger          │
│  - Auto-detect (future) │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Create Waiting-For     │
│  Note in Obsidian       │
│  (active folder)        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Daily Note Shows       │
│  Items Due Soon         │
│  (Dataview query)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Reply Arrives          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Resolution             │
│  - Manual move          │
│  - Agent suggestion     │
│  - Auto-detect (future) │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Move to Resolved       │
│  Add outcome notes      │
└─────────────────────────┘
```

---

## 9. COPYWRITER TRANSLATION

**What is "Waiting For" tracking?**

Think of it like your "sent proposals" folder from your copywriting days. You send a sales letter to a client → you track it → you follow up if they don't respond. Same concept, but for ALL emails where you need something back.

**The Email Problem:**
You send 20 emails a day. 5 of them need responses. Without a system, you're mentally tracking "Did Jane send that logo? Did Bob approve the contract?" It's cognitive overhead.

**The Solution:**
A "swipe file" of emails you're waiting on. Every morning, you see: "These 3 people owe you responses." You decide: nudge them, or let it ride.

**The Automation:**
Phase 1 = Manual tracking (you log it)
Phase 2 = Assisted (Claude suggests what to track)
Phase 3 = Automatic (Claude tracks, you just review)

It's like moving from "remember to follow up" → "here's your follow-up list" → "here's who hasn't responded, want me to draft the nudge?"

---

## 10. RECOMMENDED NEXT STEPS

1. **Validate the approach** - Does this pattern fit your workflow?
2. **Build Phase 1 MVP** - Obsidian structure + iOS shortcut
3. **Test for 1 week** - Manual logging, see if it sticks
4. **Iterate** - Add Gmail API if manual logging feels tedious
5. **Scale** - Full automation once pattern is validated

**Question for Ed:**
- Do you want to start with Phase 1 (manual MVP)?
- Should I create the Obsidian templates and folder structure?
- Do you want an iOS Shortcut to log waiting-for items?

---

## SOURCES & REFERENCES

**GTD Methodology:**
- David Allen's "Getting Things Done" (2001, 2015 edition)
- Core concept: Capture all "open loops" in external system
- Waiting For list is one of 7 standard GTD lists

**Email Tracking Patterns:**
- Gmail Labels system (common productivity practice)
- "Inbox Zero" methodology (Merlin Mann)
- Thread tracking via IMAP/Gmail API

**Obsidian Integration:**
- Dataview plugin for dynamic queries
- Daily note templates (Obsidian community practice)
- File-based note creation (compatible with git sync)

**Automation:**
- Gmail API documentation (Google)
- IMAP protocol for email monitoring
- iOS Shortcuts for mobile capture
