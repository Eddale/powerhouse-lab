# Kindle Sender - Roadmap

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.1 | 2026-01-10 | `--expand-links` flag: include linked document content as appendix |
| v1.0 | 2026-01-10 | Initial release: Research Swarm docs + Someday-Maybe support |

## Planned

- [ ] **Date ranges** - "Send last week's research to Kindle"
- [ ] **Custom patterns** - Support patterns beyond Research Swarm (e.g., `[[YT - *]]` for YouTube notes)
- [ ] **Batch confirmation** - Show all docs in a table before sending

## Ideas (Not Committed)

- Newsletter drafts to Kindle for review
- Weekly digest of all captures
- Kindle highlights back to Zettelkasten (would need Kindle API or export parsing)
- Support for other markdown folders (not just Zettelkasten)

## What We've Learned

- Amazon accepts EPUB natively now (no MOBI needed)
- Subject line "Convert" triggers Kindle format conversion
- pypandoc_binary includes pandoc, no separate brew install needed
- Gmail app passwords are mandatory (regular passwords blocked)
- Documents typically arrive on Kindle within 1-5 minutes
- Wikilinks are dead text on Kindle - need `--expand-links` to include actual content
- Single-layer expansion is enough - recursive expansion would create massive EPUBs

## Decision Log

| Date | Decision | Why |
|------|----------|-----|
| 2026-01-10 | One-layer expansion only | Prevents massive EPUBs, research rarely needs nested refs |
| 2026-01-10 | EPUB over MOBI | Amazon deprecated MOBI for new uploads |
| 2026-01-10 | Gmail SMTP over API | Simpler setup, app password is sufficient |
| 2026-01-10 | Dry-run first | Prevents accidental batch sends before setup verified |
| 2026-01-10 | Research Swarm pattern | Most common use case, expand patterns later |
