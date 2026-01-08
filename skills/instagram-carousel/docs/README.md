# Instagram Carousel - Technical Reference

## Status: DEPRECATED

This skill has been converted to an **agent** at `.claude/agents/instagram-carousel.md`.

## Why Deprecated

Skills can't properly orchestrate other skills. The carousel pipeline needs to invoke hook-stack-evaluator with Automation Mode, which requires agent-level orchestration.

## What's Still Here

This folder contains resource files used by the agent:
- `resources/visual-metaphors.md` - Image metaphor library
- `resources/secondary-characters.md` - Supporting character options
- `resources/carousel-formats.md` - Slide layout templates
- `resources/prompt-templates.md` - Nano Banana Pro prompt patterns

**Do NOT delete this folder** - only the SKILL.md was deprecated.

## How to Invoke

Use any of these trigger phrases (routes to agent):
- "Create an Instagram carousel from this article"
- "Turn this into slides"
- "Make a carousel for [topic]"

## Architecture (Post-Deprecation)

```
skills/instagram-carousel/
├── SKILL.md              # Deprecated stub pointing to agent
├── resources/            # Still active - used by agent
│   ├── visual-metaphors.md
│   ├── secondary-characters.md
│   ├── carousel-formats.md
│   └── prompt-templates.md
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas (for the agent)
    └── plans/
        └── archive/
```

## See Also

- `.claude/agents/instagram-carousel.md` - The active agent implementation
- `.claude/agents/docs/instagram-carousel/` - Agent-specific documentation
