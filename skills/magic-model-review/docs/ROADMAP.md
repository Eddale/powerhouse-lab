# Magic Model Review - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial skill with five-element evaluation |
| v1.1 | 2026-01 | Added resource files for calibration |
| v1.2 | 2026-01 | Added Zettelkasten saving + daily note linking |
| v1.3 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

Right now, Magic Model Review produces one-off feedback for individual submissions. You paste the output, the coach gets value, done.

The vision: feedback that builds on itself. Track patterns across multiple reviews. "You've tightened your Reds significantly since last time. Now the Greens are the leverage point."

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Review History** - When reviewing for a client who's submitted before, reference their previous feedback. Show progress.

- [ ] **Common Patterns Library** - Build a library of the most common issues and their fixes. Speed up reviews while keeping them personalized.

- [ ] **Offer Diamond Cross-Reference** - When reviewing a Magic Model, check if they've also submitted an Offer Diamond. Reference both for more holistic feedback.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Video Response** - Instead of text, generate a script for Ed to record a 2-minute video review. More personal, same framework.

- **Before/After Comparison** - When a coach resubmits, auto-generate a comparison. "Here's what changed. Here's what improved. Here's what to look at next."

- **Pattern Reports** - Aggregate insights across all reviews. "70% of Magic Models have Blues named as activities instead of results."

- **Self-Review Mode** - Let coaches run their own Magic Model through the skill before submitting. Pre-flight check.

- **Team Training** - Generate examples and anti-examples from anonymized reviews. Training material for new reviewers.

- **Symmetry Visualizer** - Auto-generate a visual representation of the Magic Model's structure to show balance issues.

## What We've Learned

Building this skill taught us a few things:

**Facebook constraints shape everything.** The 100 line break limit is more restrictive than character count. Bulleted feedback wastes that budget. Flowing prose fits more value.

**Suggestion language matters.** "You should" feels like criticism. "Worth looking at" feels like partnership. Same content, different reception.

**Reference materials improve calibration.** The training files in resources/ help the skill understand what "good" looks like. Reviewing them before generating feedback produces tighter output.

**Five elements is the right scope.** Early versions drifted into positioning, funnels, copy critique. Staying focused on Yellow/Reds/Greens/Blues/Symmetry keeps feedback actionable.

**The coach's emotional state matters.** The goal isn't just accurate feedback - it's feedback that lands. Seen, safe, encouraged, clear. That's the bar.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
