# Apple Mail AppleScript Test Scripts

These test scripts demonstrate practical patterns for integrating Apple Mail with Claude Code.

## Quick Start

```bash
cd research/mail-applescript-tests
chmod +x *.sh
./01-send-email-test.sh
```

## Available Tests

### 01-send-email-test.sh
**Purpose:** Sending emails via AppleScript
**What it does:**
- Creates draft emails in Mail.app
- Demonstrates safe draft-for-review pattern
- Shows multiple recipients (to, cc, bcc)
- Examples of both manual send and auto-send

**Run this to:** See how Claude Code can create email drafts for you to review

---

### 02-search-emails-test.sh
**Purpose:** Searching emails via AppleScript (demonstrates slowness)
**What it does:**
- Shows AppleScript iteration approach
- Measures performance on your mailbox
- Searches by subject and sender
- Proves why you should use mdfind instead

**Run this to:** Understand why AppleScript search is too slow for large mailboxes

---

### 03-read-email-content-test.sh
**Purpose:** Reading email content via AppleScript
**What it does:**
- Reads most recent emails
- Extracts full content and metadata
- Checks for attachments
- Saves emails to files

**Run this to:** See how to fetch email content for AI processing

---

### 04-draft-review-workflow-test.sh
**Purpose:** Recommended draft-review workflow
**What it does:**
- Demonstrates the "Claude drafts, human reviews" pattern
- Creates drafts in Mail.app for review
- Shows template-based email generation
- Multi-step workflow example

**Run this to:** See the recommended pattern for Claude Code email integration

---

### 05-mdfind-search-test.sh
**Purpose:** Fast email search via Spotlight
**What it does:**
- Uses mdfind to search email instantly
- Demonstrates various search patterns
- Shows performance comparison vs AppleScript
- Explains Spotlight query syntax

**Run this to:** Learn the FAST way to search emails

---

## Test Results Summary

### Performance

| Operation | AppleScript | mdfind | Winner |
|-----------|-------------|--------|--------|
| Send email | < 1 sec | N/A | AppleScript ⭐ |
| Search 1,000 emails | ~10 sec | < 1 sec | mdfind ⭐ |
| Search 10,000 emails | ~100 sec | < 1 sec | mdfind ⭐ |
| Read 1 email | < 1 sec | N/A | AppleScript ⭐ |
| Count inbox | < 1 sec | < 1 sec | Tie |

### Recommendations

**Use AppleScript for:**
- Sending/composing emails ⭐⭐⭐⭐⭐
- Reading specific emails ⭐⭐⭐⭐
- Getting email metadata ⭐⭐⭐⭐
- Creating drafts ⭐⭐⭐⭐⭐

**Use mdfind for:**
- Searching emails ⭐⭐⭐⭐⭐
- Finding by subject/sender/content ⭐⭐⭐⭐⭐
- Filtering by date ⭐⭐⭐⭐
- Counting matches ⭐⭐⭐⭐⭐

**Best Pattern:**
1. Search with mdfind (FAST)
2. Read with AppleScript (as needed)
3. Process with Claude (summarize, extract, etc.)
4. Draft response with AppleScript
5. Human reviews and sends

---

## Safety Notes

- All send tests create DRAFTS only (safe to run)
- No emails are sent automatically
- Test emails use example.com addresses
- Mail.app must be configured with at least one account

---

## See Also

Main research document: `research/mail-applescript-integration.md`
