# Onboarding Doc Builder - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial skill based on Jennifer Waters' playbook system |
| v1.1 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

Right now, the skill generates a playbook template. You fill in the Loom links manually.

The vision: playbook management. Track which videos are recorded. Alert when playbooks need updating. Version control for onboarding content.

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Role Templates** - Pre-built templates for common roles:
  - Appointment Setter
  - Client Success Manager
  - Community Manager
  - Sales Closer
  - VA / Admin

- [ ] **Completion Tracking** - Generate a checklist that tracks which Loom videos have been recorded vs still needed.

- [ ] **Google Docs Export** - Instead of just markdown, optionally generate as Google Doc with proper formatting.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Loom Integration** - Check if Loom links are still valid. Alert if videos were deleted.

- **Playbook Versioning** - Track changes over time. "What did we update in the March revision?"

- **Quiz Generation** - Auto-generate simple quizzes to verify comprehension after each section.

- **Time Estimates** - Add estimated completion time for each section. "Section 2: ~45 minutes."

- **Multi-Language** - Generate playbooks in Spanish or Portuguese for international teams.

- **Notion/Coda Export** - Alternative formats beyond markdown and Google Docs.

- **Onboarding Analytics** - If connected to a tracking system, show where new hires get stuck.

## What We've Learned

Building this skill taught us a few things:

**Video over text.** Jennifer's insight holds: "They hate reading. They'd rather consume via video." The structure is designed around Loom placeholders, not paragraphs.

**Seven sections is complete.** Company, Tech, Training, Daily, Scorecard, Communication, Completion. That covers everything without being overwhelming.

**Checkboxes matter.** Every item they need to complete gets a checkbox. Progress becomes visible. Nothing gets skipped.

**Completion confirmation creates closure.** The "record a 2-minute intro and send it" step signals "I'm done." Without it, onboarding just fades out.

**The playbook IS the training.** Not supplementary material. Not reference docs. The playbook is the complete training system. That mindset shift changes how you write it.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
