# Instagram Carousel Agent - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial agent replacing the skill version |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

End-to-end carousel creation - from article to posted content - with minimal human intervention. The agent handles strategy, copy, and visuals. You approve and post.

Eventually:
- Direct integration with Instagram posting
- Template library for different carousel types
- Performance tracking and optimization suggestions
- Batch processing for content calendars

## Planned Improvements

- [ ] **Template Library** - Pre-built carousel structures (listicle, story, framework, etc.)
- [ ] **Hook A/B Testing** - Generate multiple hook options, let user choose
- [ ] **Platform Variations** - Adapt same carousel for LinkedIn, Twitter threads

## Ideas (Not Committed)

- **Auto-posting** - Connect to Buffer or Later for scheduled posting
- **Analytics Integration** - Track which carousel styles perform best
- **Reference Image Library** - Pre-approved Ed photos for different scenarios
- **Brand Style Guide** - Enforce consistent visual style across all carousels
- **Carousel Series** - Multi-part carousel sequences that build on each other

## What We've Learned

**The skill → agent evolution was necessary.** Carousels require multi-step orchestration that's better suited to an agent than a skill. The agent can make decisions mid-process.

**Character consistency is hard.** AI image generation struggles with consistent characters across multiple images. The reference image + explicit instruction approach helps but isn't perfect.

**Hook quality determines carousel success.** A mediocre carousel with a great hook outperforms a great carousel with a mediocre hook. The agent prioritizes hook extraction.

**Copy length matters.** Instagram slides have limited real estate. The agent learned to write tighter, punchier copy than typical article sections.

## Decision Log

Decisions about carousel agent improvements get planned in `plans/` and archived in `plans/archive/`.
