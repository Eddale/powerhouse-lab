# Email Agent - Roadmap

## Status: Early Prototype

IMAP connection testing completed. Next step would be building actual email processing capabilities.

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v0.1 | 2025-12 | IMAP connection test script for Gmail + iCloud |
| v0.2 | 2026-01 | Added docs/ folder with ROADMAP |

## The Vision

An AI agent that can:
- Read emails (via IMAP)
- Draft responses
- Search for specific messages
- Summarize inbox
- Route urgent items to daily review

## Current State

`test_imap_connection.py` verifies:
- Gmail IMAP connection with app password
- iCloud IMAP connection with app password

Both connections work. Foundation is ready.

## What's Blocking

AppleScript email search is too slow for large mailboxes. Spotlight search broken since Catalina. Need Python IMAP as the path forward.

## Next Steps (If Resumed)

1. **Inbox Summary** - Fetch recent emails, summarize by sender/topic
2. **Search** - Find emails by sender, subject, date range
3. **Draft Response** - Generate reply for review
4. **Integration** - Connect to capture-triage flow

## Technical Notes

**Environment variables needed:**
- `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`
- `ICLOUD_ADDRESS`, `ICLOUD_APP_PASSWORD`

**IMAP servers:**
- Gmail: `imap.gmail.com:993`
- iCloud: `imap.mail.me.com:993`

## Ideas (Not Committed)

- **Email Templates** - Pre-built responses for common scenarios
- **Auto-Categorization** - Sort by urgency/topic
- **Calendar Integration** - Extract meeting invites
- **Contact Linking** - Connect to Zettelkasten CONTACT notes

## Decision Log

When we resume, plans go in `plans/` and decisions get archived to `plans/archive/`.
