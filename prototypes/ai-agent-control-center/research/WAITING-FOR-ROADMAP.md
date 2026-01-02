# Waiting For Tracking - Visual Roadmap

**Quick reference for implementation phases**

---

## THE 3-PHASE APPROACH

```
┌─────────────────────────────────────────────────────────────────┐
│                         PHASE 1: MANUAL MVP                     │
│                         (Ship in 1 session)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐             │
│  │  Send    │  →   │  Run     │  →   │ Creates  │             │
│  │  Email   │      │ Shortcut │      │   Note   │             │
│  └──────────┘      └──────────┘      └──────────┘             │
│                                                                 │
│  Daily Note Shows:                                              │
│  ┌────────────────────────────────────────┐                    │
│  │ Follow-Ups Needed                      │                    │
│  │ • Jane - Logo (Due: Jan 5) 🟡         │                    │
│  │ • Bob - Contract (Due: Jan 3) 🔴      │                    │
│  └────────────────────────────────────────┘                    │
│                                                                 │
│  Time to build: 30-60 min                                       │
│  Time per use: 30 sec                                           │
│  Leverage: Never forget to follow up                            │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2: SEMI-AUTOMATIC                      │
│                    (Build after 2 weeks of Phase 1)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐      ┌──────────┐                                │
│  │  Send    │      │  Agent   │                                │
│  │  Email   │      │  Scans   │                                │
│  └──────────┘      └─────┬────┘                                │
│                           │                                     │
│                           ▼                                     │
│  ┌────────────────────────────────────────┐                    │
│  │ Morning Report:                        │                    │
│  │ "Found 3 unreplied emails:             │                    │
│  │  1. Jane - Logo design                 │                    │
│  │  2. Bob - Contract review              │                    │
│  │  3. Sarah - Calendar link              │                    │
│  │ Track these?" [Yes] [No]               │                    │
│  └────────────────────────────────────────┘                    │
│                           │                                     │
│                           ▼                                     │
│  ┌────────────────────────────────────────┐                    │
│  │ Evening Report:                        │                    │
│  │ "Jane replied! Mark resolved?"         │                    │
│  │ [Yes] [No]                             │                    │
│  └────────────────────────────────────────┘                    │
│                                                                 │
│  Time to build: 2-3 sessions                                    │
│  Time per use: 5 min daily (review)                             │
│  Leverage: Automatic detection, smart suggestions               │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 3: FULL AUTOMATION                    │
│                     (Future state)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐                                                   │
│  │  Send    │  →  Auto-logged (if matches criteria)            │
│  │  Email   │                                                   │
│  └──────────┘                                                   │
│                                                                 │
│  ┌──────────┐                                                   │
│  │  Reply   │  →  Auto-resolved                                │
│  │ Arrives  │                                                   │
│  └──────────┘                                                   │
│                                                                 │
│  ┌────────────────────────────────────────┐                    │
│  │ Weekly Report:                         │                    │
│  │ "3 items aging, want follow-ups?"     │                    │
│  │  1. Jane (7 days)                      │                    │
│  │  2. Bob (10 days)                      │                    │
│  │  3. Sarah (14 days)                    │                    │
│  │                                        │                    │
│  │ [Draft gentle nudges] [Archive]        │                    │
│  └────────────────────────────────────────┘                    │
│                           │                                     │
│                           ▼                                     │
│  ┌────────────────────────────────────────┐                    │
│  │ Draft Follow-Up Emails:                │                    │
│  │ "Hi Jane, following up on logo..."    │                    │
│  │ [Send] [Edit] [Skip]                   │                    │
│  └────────────────────────────────────────┘                    │
│                                                                 │
│  Time to build: Multiple sessions                               │
│  Time per use: 5 min weekly (approve)                           │
│  Leverage: Zero overhead, agent handles everything              │
└─────────────────────────────────────────────────────────────────┘
```

---

## DECISION TREE: WHICH PHASE TO START?

```
Do you send 10+ emails per week expecting responses?
│
├─ No  → Phase 1 might be overkill
│        Consider: Just use Gmail "Starred" for critical items
│
└─ Yes → Do you already have a daily note habit?
         │
         ├─ No  → Phase 1 (builds the habit)
         │        + Start daily notes at same time
         │
         └─ Yes → Do you want to validate the pattern first?
                  │
                  ├─ Yes → Phase 1 (manual for 2 weeks)
                  │        Then reassess
                  │
                  └─ No  → Jump to Phase 2 (semi-auto)
                           But expect more complexity
```

---

## FILE QUICK REFERENCE

```
research/
├── WAITING-FOR-SUMMARY.md           ← Start here (overview)
├── waiting-for-tracking-research.md ← Deep dive (methodology)
├── waiting-for-implementation-guide.md ← How to build Phase 1
│
├── obsidian-templates/
│   ├── waiting-for-template.md      ← Copy to your vault
│   ├── daily-note-waiting-for-section.md ← Add to daily template
│   └── weekly-review-waiting-for.md ← Add to weekly template
│
├── ios-shortcut-waiting-for.md      ← Build mobile shortcut
└── gmail-api-automation-concept.py  ← Phase 2/3 reference
```

---

## METRICS DASHBOARD (TRACK WEEKLY)

```
┌─────────────────────────────────────────┐
│  Waiting For - Weekly Stats             │
├─────────────────────────────────────────┤
│  Active Items:          12              │
│  Resolved This Week:     5              │
│  Overdue:                2  ⚠️          │
│  Avg Days to Resolve:    3.2            │
├─────────────────────────────────────────┤
│  Top Responders:                        │
│  • Jane (24h avg)                       │
│  • Bob (48h avg)                        │
│                                         │
│  Slow Responders:                       │
│  • Sarah (7+ days) 🐌                  │
│                                         │
│  Follow-Ups Sent:        3              │
│  Success Rate:          67%             │
└─────────────────────────────────────────┘
```

---

## SUCCESS INDICATORS

### After 1 Week
- [ ] Created 5+ waiting-for items
- [ ] Checked daily note every morning
- [ ] Caught 1+ item that would've slipped
- [ ] Logging feels natural (not forced)

### After 1 Month
- [ ] Never forget important follow-ups
- [ ] Can quickly answer "Who owes me what?"
- [ ] Weekly review takes < 10 minutes
- [ ] System feels trustworthy

### After 3 Months
- [ ] Reputation as "never drops the ball"
- [ ] Zero mental overhead tracking emails
- [ ] Identified patterns (who needs nudging)
- [ ] Considering automation (Phase 2)

---

## INTEGRATION MAP

```
┌────────────────────────────────────────────────────────┐
│                    YOUR WORKFLOW                       │
└────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Email   │    │ Obsidian │    │  Claude  │
    │  (Gmail) │    │  Vault   │    │  Agents  │
    └────┬─────┘    └─────┬────┘    └─────┬────┘
         │                │               │
         │    Phase 1     │               │
         └────────►─┬─────┘               │
                    │ (Manual log)        │
                    │                     │
         │    Phase 2                     │
         └───────────┼────────────────────┘
                     │ (Agent scans)
                     │
                     ▼
         ┌─────────────────────┐
         │  waiting-for/       │
         │    active/          │
         │    resolved/        │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Daily Note         │
         │  (Dataview query)   │
         └─────────────────────┘
```

---

## QUICK START COMMANDS

### Create Folder Structure (Obsidian)

```bash
# Navigate to your vault
cd /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten

# Create folders
mkdir -p waiting-for/active
mkdir -p waiting-for/resolved

# Copy template
cp /path/to/research/obsidian-templates/waiting-for-template.md waiting-for/_template.md
```

### Test the System (5 minutes)

1. Create a test waiting-for note
2. Add Dataview query to a scratch note
3. Verify it shows up
4. Move to resolved folder
5. Verify it disappears from query

### Build iOS Shortcut (10 minutes)

1. Open Shortcuts app
2. Create new shortcut
3. Follow steps in `ios-shortcut-waiting-for.md`
4. Test with dummy data
5. Refine until fast

---

## COMMON PITFALLS (AND FIXES)

### ❌ Logging EVERY email
**Fix:** Only track emails where you need a response

### ❌ Setting unrealistic expected dates
**Fix:** Most replies take 3-5 days, not 1 day

### ❌ Not reviewing weekly
**Fix:** Add to calendar, make it routine

### ❌ Forgetting to mark resolved
**Fix:** Check daily note, move to resolved when reply arrives

### ❌ Jumping to automation too fast
**Fix:** Stick with Phase 1 for 2+ weeks first

---

## NEXT SESSION PREP

If you decide to build Phase 1:

**Bring:**
- [ ] Path to your Obsidian vault
- [ ] Confirm you have Dataview plugin installed
- [ ] 2-3 real emails to test with

**I'll deliver:**
- [ ] Working folder structure in your vault
- [ ] Templates ready to use
- [ ] iOS shortcut recipe
- [ ] Test run with real email

**Time:** 30-60 minutes
**Output:** System you can use tomorrow morning

---

**Ready when you are.**
