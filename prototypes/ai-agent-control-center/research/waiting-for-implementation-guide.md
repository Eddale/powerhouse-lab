# Waiting For - Implementation Guide (Phase 1 MVP)

**Target**: Ship a working system in 30-60 minutes
**Approach**: Manual capture, Obsidian storage, daily surfacing

---

## FOLDER STRUCTURE

Create in your Obsidian vault:

```
waiting-for/
├── _template.md
├── active/
│   └── .gitkeep
└── resolved/
    └── .gitkeep
```

---

## TEMPLATE: `_template.md`

Save to: `waiting-for/_template.md`

```markdown
---
person:
email:
subject: ""
sent: {{date:YYYY-MM-DD}}
expected:
status: pending
priority: normal
project: ""
---

# Waiting For: [Person] - [Brief Description]

## What I'm Waiting For


## Context
<!-- Why does this matter? What does it block? -->


## Email Details
- **Sent**: {{date:YYYY-MM-DD}}
- **Subject**:
- **Key points**:


## Follow-Up Plan
- If no response by [DATE] →
- Escalation:


## Resolution
<!-- Fill when resolved -->
- **Resolved**:
- **Outcome**:
```

---

## DAILY NOTE INTEGRATION

Add this section to your daily note template:

```markdown
## Follow-Ups Needed

<!-- Shows items due within 2 days -->
```dataview
TABLE
  person as "Who",
  subject as "What",
  sent as "Sent",
  expected as "Due By",
  choice(expected < date(today), "🔴 OVERDUE",
         choice(expected = date(today), "🟡 TODAY", "🟢 Soon")) as "Status"
FROM "waiting-for/active"
WHERE status = "pending"
SORT expected asc
```

<!-- Quick stats -->
Currently waiting on **$= dv.pages('"waiting-for/active"').where(p => p.status === "pending").length** items

---

## All Active Waiting-For Items

```dataview
TABLE
  person,
  subject,
  sent,
  expected,
  priority
FROM "waiting-for/active"
WHERE status = "pending"
SORT priority desc, expected asc
```
```

---

## QUICK CAPTURE WORKFLOW

### Desktop (Manual)

**Step 1**: After sending email, press CMD+N in Obsidian

**Step 2**: Use template (CMD+T or hotkey)

**Step 3**: Fill in fields:
- Person name
- Subject
- Expected response date
- Context (why it matters)

**Step 4**: Save to `waiting-for/active/YYYY-MM-DD-person-name.md`

**Time**: 60 seconds

### Mobile (iOS Shortcut)

**Step 1**: Create Shortcut with these actions:

```
1. Ask for Input → "Person name"
2. Ask for Input → "Email subject"
3. Ask for Input → "Expected response date (YYYY-MM-DD)"
4. Set Variable → "Person" to Input 1
5. Set Variable → "Subject" to Input 2
6. Set Variable → "Expected" to Input 3
7. Get Current Date → Format as YYYY-MM-DD
8. Text →
---
person: [Person]
subject: "[Subject]"
sent: [Current Date]
expected: [Expected]
status: pending
priority: normal
---

# Waiting For: [Person] - [Subject]

## What I'm Waiting For
[Subject]

## Email Details
- Sent: [Current Date]
- Subject: [Subject]

## Follow-Up Plan
- If no response by [Expected] → Send reminder

9. Create Note in Obsidian
   - Folder: waiting-for/active
   - Filename: [Current Date]-[Person].md
   - Content: [Text from step 8]
```

**Step 2**: Add to Share Sheet or widget

**Time**: 30 seconds after email sent

---

## WEEKLY REVIEW CHECKLIST

Add to your weekly review:

```markdown
### Waiting For Review

- [ ] Check all active waiting-for items
- [ ] Move resolved items to `waiting-for/resolved/`
- [ ] Update expected dates if needed
- [ ] Decide on follow-ups for overdue items
- [ ] Archive anything no longer relevant

**Stats:**
- Items resolved this week:
- Aging items (>7 days):
- Follow-ups needed:
```

---

## USAGE PATTERNS

### Pattern 1: Standard Email Follow-Up

**Scenario**: You sent proposal to client, expect response in 3 days

**Action**:
1. Send email
2. Create waiting-for note
3. Set expected date: 3 days from now
4. Daily note will surface it when due

**Follow-up**:
- Day 3: Check daily note, see reminder
- Day 4: If no response, send gentle nudge
- When reply arrives: Move to resolved, add outcome

### Pattern 2: Delegated Task

**Scenario**: Asked team member to complete deliverable

**Action**:
1. Send email with request
2. Create waiting-for note
3. Link to project: `project: "[[Client Onboarding]]"`
4. Set expected date: deadline

**Follow-up**:
- Track in project note AND waiting-for
- Daily note surfaces before deadline
- Move to resolved when delivered

### Pattern 3: Information Request

**Scenario**: Asked colleague for data/document

**Action**:
1. Send request
2. Create waiting-for note
3. Note what you'll do with the data (context)

**Follow-up**:
- If urgent: Set expected = tomorrow
- If not urgent: Set expected = 5 days
- When received: Move to resolved, link to where you used the data

---

## RESOLUTION WORKFLOW

### When Reply Arrives

**Step 1**: Open the waiting-for note

**Step 2**: Update resolution section:
```markdown
## Resolution
- **Resolved**: 2026-01-05
- **Outcome**: Received logo files, uploaded to assets folder
- **Next action**: [[Schedule newsletter with new logo]]
```

**Step 3**: Change frontmatter:
```yaml
status: resolved
resolved_date: 2026-01-05
```

**Step 4**: Move file:
```
FROM: waiting-for/active/2026-01-02-jane-logo.md
TO:   waiting-for/resolved/2026-01-02-jane-logo.md
```

**Optional**: Link to reply email or save relevant info

---

## METRICS TO TRACK

Add to monthly review:

```markdown
## Waiting For Metrics

**This Month:**
- Total items tracked:
- Average resolution time:
- Items requiring follow-up:
- Items that went stale:

**Insights:**
- Who responds fastest:
- Who needs nudging:
- What requests get ignored:

**Process improvements:**
-
```

---

## DATAVIEW QUERIES (ADVANCED)

### Overdue Items

```dataview
TABLE
  person,
  subject,
  sent,
  expected,
  date(today) - expected as "Days Overdue"
FROM "waiting-for/active"
WHERE expected < date(today) AND status = "pending"
SORT expected asc
```

### By Person

```dataview
TABLE
  rows.subject as "Items",
  rows.expected as "Due Dates"
FROM "waiting-for/active"
WHERE status = "pending"
GROUP BY person
SORT person asc
```

### By Priority

```dataview
TABLE
  person,
  subject,
  expected
FROM "waiting-for/active"
WHERE status = "pending" AND priority = "high"
SORT expected asc
```

### Resolution Stats (Last 30 Days)

```dataview
TABLE
  person,
  subject,
  resolved_date - sent as "Days to Resolve"
FROM "waiting-for/resolved"
WHERE resolved_date >= date(today) - dur(30 days)
SORT resolved_date desc
```

---

## INTEGRATION WITH PROJECTS

### Link from Project Note

In your project notes, add:

```markdown
## Waiting For

```dataview
TABLE
  person,
  subject,
  expected
FROM "waiting-for/active"
WHERE contains(project, this.file.name) AND status = "pending"
SORT expected asc
```
```

This shows all waiting-for items linked to this project.

### Link from Waiting-For Note

In waiting-for note frontmatter:
```yaml
project: "[[Newsletter Launch]]"
```

Creates bidirectional link.

---

## MOBILE WORKFLOW (iOS)

### After Sending Email (Mail App)

1. Tap Share button
2. Select "Log to Waiting For" shortcut
3. Fill in prompts (person, subject, expected)
4. Done - note created in Obsidian

### Checking Daily Note (Obsidian Mobile)

1. Open today's daily note
2. Scroll to "Follow-Ups Needed"
3. See what's due today
4. Tap to open waiting-for note
5. Mark resolved if reply received

---

## CLAUDE AGENT INTEGRATION (FUTURE)

### Agent Capability: Waiting-For Manager

**Skills:**
1. **Scan** - Check Gmail for unreplied sent emails
2. **Suggest** - Prompt user to create waiting-for items
3. **Detect** - Find replies, suggest closing items
4. **Report** - Daily summary of aging items
5. **Draft** - Generate follow-up email drafts

**Workflow:**
```
Morning:
- Agent scans sent folder
- Finds 3 unreplied emails from yesterday
- Prompts: "Want to track these as waiting-for?"
- User approves → Agent creates notes

Evening:
- Agent detects 2 replies received today
- Prompts: "Mark these as resolved?"
- User approves → Agent moves to resolved

Weekly:
- Agent reports: "5 items over 7 days old, want to follow up?"
- User selects 3 → Agent drafts gentle nudges
```

---

## TROUBLESHOOTING

### Dataview Queries Not Showing

**Issue**: Empty results in daily note

**Check:**
1. Dataview plugin installed and enabled?
2. Folder path correct? (`waiting-for/active/`)
3. Notes have frontmatter with `status: pending`?
4. Expected date format: `YYYY-MM-DD`

### Too Many Items Showing

**Issue**: Daily note cluttered with all items

**Fix:**
Adjust query date range:
```
WHERE expected <= date(today) + dur(1 days)
```
Change `2 days` to `1 days` for tighter focus.

### Forgetting to Log

**Issue**: Send emails but forget to create waiting-for note

**Solutions:**
1. **Trigger**: Set 10-minute timer after sending important email
2. **Batch**: End of day, review sent folder, create notes for key items
3. **Automate**: Use BCC or iOS shortcut to reduce friction

### Notes Piling Up

**Issue**: Too many active items, overwhelming

**Fix:**
1. Weekly review: Archive anything not critical
2. Be selective: Only track items that truly matter
3. Set priority: Focus on high-priority items only

---

## SUCCESS CRITERIA

You'll know this is working when:

1. **Zero mental overhead** - You don't think "Did they reply?" because system tracks it
2. **Timely follow-ups** - You catch things before they're awkward
3. **Nothing falls through cracks** - Every delegated item has a home
4. **Quick resolution** - Move from pending → resolved feels smooth
5. **Trust the system** - You check daily note, not your email anxiety

---

## NEXT PHASE TRIGGERS

Move to Phase 2 (automation) when:

- [ ] You've used manual system for 2+ weeks consistently
- [ ] You're creating 5+ waiting-for items per week
- [ ] Manual logging feels tedious
- [ ] You want automatic reply detection

**Don't rush automation.** Master the manual system first. The pattern needs to fit your workflow before you automate it.

---

## COPYWRITER ANALOGY

**This system is like:**

A "sent proposals" tracking spreadsheet from your agency days.

**Manual Phase (Phase 1):**
You log each proposal sent, follow-up date, client name. Once a week, you scan the list and nudge the slow responders.

**Automated Phase (Phase 2):**
The system watches your sent folder, auto-logs proposals, and tells you "Hey, 3 clients haven't responded in 7 days, want to ping them?"

**Full System (Phase 3):**
The system not only tracks but DRAFTS the follow-up: "Here's a gentle nudge email for those 3 clients, approve?"

You went from "I hope I remember to follow up" → "I have a list" → "The list reminds me" → "The list drafts the follow-up."

Same progression here. Start with the list. Build from there.
