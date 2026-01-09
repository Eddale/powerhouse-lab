# Morning Metrics - Roadmap

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01-10 | Initial release - Gmail + Calendar via Google API |

## Planned

- [ ] Substack integration (subscriber count, recent growth)
- [ ] Stripe integration (daily revenue awareness)
- [ ] Email intelligence - surface action-required vs. newsletters
- [ ] Calendar intelligence - flag meeting prep needed
- [ ] iCloud mail summary (eddale@mac.com via IMAP)

## Ideas (Not Committed)

- **receipt-forwarder skill** - Separate skill to forward receipts to Hubdoc (neonmarillion.ff80@app.hubdoc.com). Auto-detect PayPal, Uber, invoices, etc. and forward on demand. Keeps morning-metrics focused on reading, new skill handles actions.
- Social media metrics (X followers, engagement)
- Website analytics summary
- BlackBelt community activity
- "Compared to last week" trends
- Natural language time parsing ("meetings this afternoon")

## What We've Learned

### 2026-01-10 - Initial Build
- Google Cloud project setup takes 15 minutes when automated
- OAuth Desktop app flow works well for CLI tools
- Token persistence via pickle means one-time browser auth
- IMAP is already working for both Gmail and iCloud (separate from API)

### 2026-01-10 - iCloud IMAP Gotcha
- **iCloud IMAP doesn't return message body with standard `RFC822` fetch** - returns empty `b'msgid ()'`
- **Fix:** Use `BODY.PEEK[]` instead - works correctly and doesn't mark as read
- This cost 4 debugging iterations; document for future reference

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Google API over IMAP for Gmail | API gives labels, categories, metadata; IMAP is basic read-only |
| Python script vs inline | Keep auth logic isolated; easier to test and maintain |
| JSON output | Claude parses structured data better than free text |
| Single script for all metrics | One invocation, one auth check, consistent output |
