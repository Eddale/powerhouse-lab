# iOS Shortcut: Log to Waiting For

**Purpose**: Quick capture after sending email on mobile
**Time to build**: 5 minutes
**Time to use**: 30 seconds

---

## Shortcut Actions

### 1. Get Inputs

**Action**: Ask for Input
- Prompt: "Person name?"
- Input Type: Text
- Store as: `Person`

**Action**: Ask for Input
- Prompt: "Email subject?"
- Input Type: Text
- Default: (Leave blank)
- Store as: `Subject`

**Action**: Ask for Input
- Prompt: "Expected response date (days from now)?"
- Input Type: Number
- Default: 3
- Store as: `DaysOut`

**Action**: Ask for Input (Optional)
- Prompt: "Priority? (normal/high/urgent)"
- Input Type: Text
- Default: normal
- Store as: `Priority`

### 2. Calculate Dates

**Action**: Get Current Date
- Store as: `SentDate`

**Action**: Format Date
- Input: `SentDate`
- Format: Custom → `yyyy-MM-dd`
- Store as: `SentFormatted`

**Action**: Adjust Date
- Input: `SentDate`
- Add: `DaysOut` Days
- Store as: `ExpectedDate`

**Action**: Format Date
- Input: `ExpectedDate`
- Format: Custom → `yyyy-MM-dd`
- Store as: `ExpectedFormatted`

### 3. Generate Filename

**Action**: Text
```
{{SentFormatted}}-{{Person}}
```
- Store as: `Filename`

**Action**: Replace Text
- Input: `Filename`
- Find: Spaces
- Replace with: Dashes (-)
- Store as: `FilenameSafe`

### 4. Build Note Content

**Action**: Text
```
---
person: {{Person}}
subject: "{{Subject}}"
sent: {{SentFormatted}}
expected: {{ExpectedFormatted}}
status: pending
priority: {{Priority}}
---

# Waiting For: {{Person}} - {{Subject}}

## What I'm Waiting For
{{Subject}}

## Context


## Email Details
- **Sent**: {{SentFormatted}}
- **Subject**: {{Subject}}
- **Expected**: {{ExpectedFormatted}}

## Follow-Up Plan
- If no response by {{ExpectedFormatted}} → Send reminder


## Resolution

```
- Store as: `NoteContent`

### 5. Create Note in Obsidian

**If using Obsidian with Advanced URI plugin:**

**Action**: URL
```
obsidian://new?vault=YourVaultName&file=waiting-for/active/{{FilenameSafe}}&content={{NoteContent encoded}}
```

**Action**: Open URLs
- Input: URL from previous step

**If using file system (Shortcuts with Files access):**

**Action**: Save File
- Input: `NoteContent`
- Destination: iCloud Drive/Obsidian/YourVault/waiting-for/active/
- Filename: `{{FilenameSafe}}.md`
- Overwrite: No

### 6. Confirmation

**Action**: Show Notification
- Title: "Waiting For Logged"
- Body: "Tracking: {{Person}} - {{Subject}}"

---

## Setup Instructions

### Option A: Using Obsidian Advanced URI Plugin

1. Install "Advanced URI" plugin in Obsidian
2. Enable the plugin
3. Create shortcut using URL scheme actions above
4. Replace `YourVaultName` with your actual vault name
5. Test with sample email

### Option B: Using File System Access

1. Grant Shortcuts app access to iCloud Drive
2. Navigate to: iCloud Drive/Obsidian/[Your Vault]/
3. Create folder: `waiting-for/active/`
4. Use "Save File" action in shortcut
5. Obsidian will auto-detect new files

---

## Usage Workflow

### After Sending Email

1. **Tap Share** (if in Mail app) or **Run Shortcut** (from widget/home screen)
2. **Enter person name**: "Jane Doe"
3. **Enter subject**: "Logo design request"
4. **Enter days until expected**: 3
5. **Priority**: normal (or leave default)
6. **Done** - Note created in Obsidian

### Checking Status

1. Open Obsidian on mobile
2. Navigate to today's daily note
3. Scroll to "Follow-Ups Needed" section
4. See all items due today/soon

### Marking Resolved

1. Open the waiting-for note
2. Scroll to Resolution section
3. Add outcome and date
4. Change frontmatter: `status: resolved`
5. Move file to `waiting-for/resolved/` folder

---

## Advanced: Share Sheet Integration

To trigger from Mail app after sending:

### 1. Modify Shortcut

**Action**: Get Text from Input
- Store as: `SharedText`

**Action**: Match Text (Regex)
- Input: `SharedText`
- Pattern: `^(.*)`
- Store as: `MailSubject`

This extracts subject line if sharing from Mail.

### 2. Add to Share Sheet

1. In Shortcuts app → Your shortcut
2. Tap (i) icon
3. Enable "Show in Share Sheet"
4. Accept: Text
5. Done

### 3. Usage

1. After sending email in Mail
2. Tap email in Sent folder
3. Tap Share button
4. Select "Log to Waiting For" shortcut
5. Subject auto-filled from email
6. Just add person name and expected date

---

## Troubleshooting

### Shortcut Can't Find Obsidian Vault

**Issue**: File path errors

**Fix**:
1. Check vault location in iCloud Drive
2. Verify folder path matches exactly
3. Try creating folder manually first
4. Grant Shortcuts full access to iCloud Drive

### Note Not Appearing in Obsidian

**Issue**: Created file but don't see it

**Fix**:
1. Pull to refresh in Obsidian mobile
2. Check folder path is correct
3. Look in root vault folder (might be in wrong spot)
4. Check Obsidian settings → Files & Links → "Default location for new notes"

### Date Format Wrong

**Issue**: Dataview queries not working

**Fix**:
1. Ensure date format is `yyyy-MM-dd` (not `MM/dd/yyyy`)
2. Check frontmatter YAML syntax (colon after field name)
3. Verify no extra spaces in dates

### Shortcut Runs But Note Empty

**Issue**: File created but content missing

**Fix**:
1. Check text encoding in "Save File" action
2. Verify variables are populated (add "Show Result" actions to debug)
3. Check for special characters breaking YAML

---

## Variations

### Quick Version (Minimal Inputs)

Only ask for:
- Person name
- Subject

Auto-set:
- Expected: 3 days from now
- Priority: normal

**Use when**: Rapid logging, most items are similar timeline

### Detailed Version (Max Context)

Ask for:
- Person name
- Email address
- Subject
- Expected date
- Priority
- Project/context
- Notes

**Use when**: Complex delegations, project-critical items

### Meeting Follow-Up

Pre-fill context:
- "Follow-up from meeting"
- Expected: 5 days
- Priority: high

**Use when**: Meeting ends, you delegated action items

---

## Integration with Other Shortcuts

### Chain with "Send Email + Log"

1. Shortcut: Compose email
2. Send email
3. Automatically trigger "Log to Waiting For"
4. Pre-fill subject and recipient from email

### Daily Review Shortcut

1. Open Obsidian daily note
2. Scroll to "Follow-Ups Needed"
3. For each item, prompt: "Resolved? (Y/N)"
4. If Y → Move to resolved folder
5. If N → Prompt: "Send reminder? (Y/N)"
6. If Y → Open Mail with pre-filled reminder email

---

## Example Notes Created

### Example 1: Simple Email Follow-Up

**Filename**: `2026-01-02-jane-doe.md`

```markdown
---
person: Jane Doe
subject: "Logo design request"
sent: 2026-01-02
expected: 2026-01-05
status: pending
priority: normal
---

# Waiting For: Jane Doe - Logo design request

## What I'm Waiting For
Logo design request

## Email Details
- **Sent**: 2026-01-02
- **Subject**: Logo design request
- **Expected**: 2026-01-05

## Follow-Up Plan
- If no response by 2026-01-05 → Send reminder
```

### Example 2: High Priority Delegation

**Filename**: `2026-01-02-bob-smith.md`

```markdown
---
person: Bob Smith
subject: "Contract review needed ASAP"
sent: 2026-01-02
expected: 2026-01-03
status: pending
priority: high
---

# Waiting For: Bob Smith - Contract review needed ASAP

## What I'm Waiting For
Contract review needed ASAP

## Email Details
- **Sent**: 2026-01-02
- **Subject**: Contract review needed ASAP
- **Expected**: 2026-01-03

## Follow-Up Plan
- If no response by 2026-01-03 → Send reminder
```

---

## Success Metrics

Track in weekly review:
- Shortcut runs per week:
- Time saved vs manual logging:
- Capture rate (emails sent vs logged):

Goal: 80%+ of important sent emails logged to Waiting For

---

## Next Level: Automation

Once manual shortcut is habit, explore:
- **Gmail API** → Auto-detect sent emails, prompt to log
- **Claude agent** → Scan sent folder, suggest items to track
- **Reply detection** → Auto-resolve when response received

But start here. Master the capture habit first.
