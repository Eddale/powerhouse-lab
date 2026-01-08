# Offer Diamond Review - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial skill with five-point evaluation |
| v1.1 | 2026-01 | Added resource files for calibration |
| v1.2 | 2026-01 | Added Zettelkasten saving + daily note linking |
| v1.3 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

Right now, Offer Diamond Review evaluates single submissions. Same pattern every time: upload, review, paste.

The vision: offer evolution tracking. See how someone's diamond improved from version 1 to version 3. "Your guarantee has gotten much stronger. Now let's work on urgency."

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Review History** - Track previous reviews for the same coach. Show progress over versions.

- [ ] **Magic Model Cross-Reference** - When reviewing an Offer Diamond, check if they've also submitted a Magic Model. Ensure alignment.

- [ ] **Common Fixes Library** - The same issues come up repeatedly. Build a library of standard suggestions with variations.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Before/After Generator** - When a coach resubmits, auto-generate a comparison showing what improved.

- **Offer Audit Mode** - More comprehensive review beyond the five points. For coaches who want the full teardown.

- **Price Point Calibration** - Different advice for $2k offers vs $20k offers. Context matters.

- **Video Response Script** - Generate a script for Ed to record a personalized video review.

- **Batch Review Mode** - When multiple diamonds need review, process them efficiently with summary statistics.

## What We've Learned

Building this skill taught us a few things:

**Five points is the right focus.** Early versions drifted into copy critique, funnel strategy, messaging theory. Staying focused on Promise/Guarantee/Bonuses/Payment/Urgency keeps feedback actionable.

**Suggestion language changes reception.** "You should" creates resistance. "Worth experimenting with" creates openness. Same content, different landing.

**Facebook format is a feature.** The constraint forces prioritization. What are the 2-5 things that matter most? No room for comprehensive audits that overwhelm.

**Reference materials calibrate quality.** The training files in resources/ establish what "good" looks like. Reading them before generating feedback produces tighter output.

**Real scarcity only.** Never suggest fake urgency. The skill explicitly prohibits this because it erodes trust and doesn't work long-term.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
