# BlackBelt Playbook Generator - Roadmap

## The Vision

Every coaching business needs onboarding docs. Writing them manually is grunt work. This tool turns hours into 30 seconds.

**Current state:** Live at https://app-eight-indol-52.vercel.app - generating playbooks for BlackBelt members.

---

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial release - form → Claude → DOCX download |
| v1.1 | 2026-01 | Added docs/ folder with ROADMAP and plans structure |

### What V1 Does

- Fill a form (company, role, tools, manager)
- Claude writes complete playbook in Jennifer Waters' style
- Download as Word doc (properly formatted) or Markdown
- No login required - zero friction
- Cost: ~$0.01 per playbook

---

## Planned Improvements

These are on the list - not "someday maybe."

- [ ] **Setter-Specific Template** - Dedicated playbook optimized for Appointment Setters. Different structure than general roles. Scripts, objection handling, call frameworks baked in.

- [ ] **Role Template Library** - Pre-built templates for common coaching roles:
  - Appointment Setter
  - Client Success Manager
  - Community Manager
  - Sales Closer
  - VA / Admin

- [ ] **Claude in Chrome Testing** - Automated end-to-end tests. Fill form, generate playbook, verify DOCX downloads correctly. Catch regressions before users do.

- [ ] **Custom Branding Upload** - Let users add their own logo. Currently hardcoded to BlackBelt branding.

---

## Ideas (Not Committed)

Parking lot stuff. Interesting but not proven necessary yet.

- **Google Docs Export** - Some people live in Google. Would need different formatting approach.

- **Save to Library** - Generate once, access later. Would need user accounts though - adds friction.

- **Inline Editing** - Edit the playbook before download. Currently: download and edit in Word.

- **Multi-Language** - Spanish, Portuguese for international coaches. Prompt engineering challenge.

- **Loom Placeholder Generator** - Auto-insert "Record a Loom for [topic]" placeholders in the playbook. Reminds managers to add video walkthroughs.

- **GHL Integration** - When new team member added in GHL, auto-generate their playbook. True automation.

- **Playbook Versioning** - Track changes over time. "What did we change in the March 2026 update?"

---

## What We've Learned

Building this taught us a few things:

**The DOCX conversion was the hard part.** Getting Claude to write content is easy. Getting Word to render it properly with real headings, tables, and page breaks - that took most of the build time. The `docx` library does the heavy lifting but needs precise formatting instructions.

**Zero-friction beats features.** No login, no account, no email capture. Just fill form and download. Conversion rate is effectively 100% because there's nothing to abandon.

**The prompt is the product.** The 2000-word prompt template determines everything about playbook quality. Want different output? Change the prompt. The UI is just a wrapper.

**Page breaks matter more than you'd think.** Early versions dumped everything into one long scroll. Adding page breaks between sections made the output feel "professional" - even though the content was identical.

**Jennifer Waters' style is replicable.** We trained Claude on her existing playbooks. Now it writes in her voice consistently. Same pattern could work for any coach's unique style.

---

## The Leverage Asset Pattern

This tool demonstrates the core pattern:

1. **Identify grunt work** → Writing onboarding docs manually
2. **Template it** → Prompt that produces consistent output
3. **Wrap in UI** → Form makes it accessible to non-technical users
4. **Deploy it** → Vercel hosting, zero ops
5. **Document it** → README + HOW-IT-WORKS + ROADMAP

**Replicable for:** SOPs, email sequences, workshop outlines, client intake forms, coaching frameworks, any document you write repeatedly.

---

## Decision Log

When we make significant changes, the plan lives in `docs/plans/current.md` and gets archived to `docs/plans/archive/` when complete.

This creates a decision history - why we built what we built, what we considered, what we rejected.

---

## Success Signals

How we know it's working:

- [ ] BlackBelt members using it regularly (not just once)
- [ ] Playbook quality matches manually-written versions
- [ ] Time savings: 30 seconds vs 2+ hours
- [ ] DOCX downloads render correctly in Word
- [ ] No support requests about broken formatting

---

## Kill Rules

When to stop and reconsider:

- If playbook quality drops below "good enough to use"
- If DOCX generation breaks and can't be fixed quickly
- If Claude API costs spike unexpectedly
- If usage drops to near-zero (signal: wrong problem to solve)
