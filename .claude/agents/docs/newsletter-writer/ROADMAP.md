# Newsletter Writer Agent - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial agent with full pipeline |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

The newsletter writer becomes a true "writing room" - not just drafting single articles but managing the entire newsletter calendar. Schedule, draft, review, publish.

Eventually:
- Content calendar management
- Topic queue with research pre-done
- Multi-format output (Substack, LinkedIn, X threads)
- Performance tracking and content optimization

## Planned Improvements

- [ ] **Multi-Source Synthesis** - "Write about X using these 3 videos and this article"
- [ ] **Series Support** - Multi-part newsletters with continuity
- [ ] **Draft Versioning** - Track revisions, compare versions

## Ideas (Not Committed)

- **Content Calendar** - Plan and track newsletter schedule
- **Topic Queue** - Bank of researched topics ready to draft
- **Platform Adaptation** - Same content adapted for different platforms
- **Performance Integration** - Learn from what performs well
- **Voice Calibration** - Fine-tune voice based on feedback
- **Image Suggestions** - Recommend or generate hero images

## What We've Learned

**Skill chaining works.** youtube-processor → mission-context → hook-stack → ai-slop-detector creates a comprehensive pipeline. Each skill does one thing well.

**Automation signals are essential.** When Ed says "automatically," he means it. The agent shouldn't stop to ask questions that have obvious answers.

**The 80/20 applies.** The agent gets you 80% of the way. The final 20% - personal anecdotes, specific phrasing, the perfect ending - that's Ed's job. Don't try to automate taste.

**Save location matters.** Drafts in the Zettelkasten means they're findable, linkable, and part of the knowledge system. Random file locations create orphaned content.

## Decision Log

Decisions about newsletter-writer improvements get planned in `plans/` and archived in `plans/archive/`.
