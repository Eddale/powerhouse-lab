# Instagram Carousel Agent - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial agent replacing the skill version |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |
| v1.2 | 2026-01-10 | **Google API image generation** - Phase 13 auto-generates images via Gemini 3 Pro Image. Chat mode for character consistency. ~$1.07 per 8-slide carousel. |

## The Vision

End-to-end carousel creation - from article to posted content - with minimal human intervention. The agent handles strategy, copy, and visuals. You approve and post.

Eventually:
- Direct integration with Instagram posting
- Template library for different carousel types
- Performance tracking and optimization suggestions
- Batch processing for content calendars

## Planned Improvements

### v2.0 - Auto Quality Check
- [ ] **Slide Text Verification** - After generation, auto-read each image and check text rendering
- [ ] **Auto-flag issues** - Detect garbled text, misspellings, missing words
- [ ] **Selective regeneration** - Offer to regenerate only problematic slides while maintaining character consistency

### Other Planned
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

**Character consistency is SOLVED.** Previously hard - AI would generate different people across slides. Fix: use `model.start_chat()` with `chat.send_message()` instead of individual `generate_content()` calls. Chat mode maintains "thought signatures" that preserve character across the session. Reference image sent with first prompt only.

**Hook quality determines carousel success.** A mediocre carousel with a great hook outperforms a great carousel with a mediocre hook. The agent prioritizes hook extraction.

**Copy length matters.** Instagram slides have limited real estate. The agent learned to write tighter, punchier copy than typical article sections.

## Decision Log

Decisions about carousel agent improvements get planned in `plans/` and archived in `plans/archive/`.
