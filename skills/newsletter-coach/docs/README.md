# Newsletter Coach - Technical Reference

## What It Does

A conversational writing coach that extracts educational content from daily experiences through a structured 7-phase interview process. Outputs publish-ready newsletter drafts for The Little Blue Report.

## Architecture

```
newsletter-coach/
├── SKILL.md              # Main skill definition (7-phase process)
├── docs/
│   ├── README.md         # This file
│   ├── GUIDE.md          # Business-friendly explanation
│   ├── ROADMAP.md        # Future ideas
│   └── plans/            # Improvement plans
├── resources/
│   ├── idea-development-questions.md   # Phase 1 question bank
│   ├── outliner.md                     # Phase 5 post type formats
│   ├── section-writer.md               # Phase 6 expansion framework
│   └── newsletter-examples.md          # Phase 7 style reference
├── scripts/              # (empty - no automation yet)
├── references/           # (empty - context docs if needed)
└── assets/               # (empty - binary files if needed)
```

## Dependencies

**Tools required:**
- `Read` - Loads resource files during phases
- `Glob` - Finds files in resources/
- `WebSearch` - Research if needed during writing
- `WebFetch` - Pull reference material if needed

**No external APIs or scripts.** Pure conversational skill.

## Usage

**Trigger phrases:**
- "Help me write a newsletter"
- "I want to brainstorm newsletter ideas"
- "Turn this experience into an article"
- "Writing coach" / "newsletter coach"

**Input:** User's daily experiences, ideas, or rough concepts

**Output:** Publish-ready newsletter draft in The Little Blue Report style

## The 7-Phase Process

| Phase | Purpose | Resource File |
|-------|---------|---------------|
| 1. Get Actions | Extract what happened | `idea-development-questions.md` |
| 2. Name Audience | Who benefits from this? | - |
| 3. Clarity Statement | Full picture articulation | - |
| 4. Headlines | 10 options, 5 proven styles | - |
| 5. Outline | 4-8 subheads by post type | `outliner.md` |
| 6. Expand | Fill sections using 14 ways | `section-writer.md` |
| 7. Write | Final draft in LBR style | `newsletter-examples.md` |

## Testing

**Manual verification:**
1. Invoke with "help me write a newsletter"
2. Walk through a real experience
3. Verify each phase transition happens naturally
4. Confirm final output matches The Little Blue Report voice

**Quality checks:**
- [ ] Asks one question at a time (not overwhelming)
- [ ] Reads resource files at correct phases
- [ ] Headlines use the 5 proven styles
- [ ] Subheads are story-driven hooks (not numbered steps)
- [ ] Final draft has short paragraphs, white space, conversational tone

## Known Limitations

- No automated publishing (manual copy to Substack)
- No image generation for headers
- No A/B testing of headlines
- Relies on user's memory of experiences (no calendar integration)

## Related Skills

- `hook-stack-evaluator` - Can score headlines from Phase 4
- `ai-slop-detector` - Clean final draft before publishing
- `youtube-processor` - If experience involves a video
