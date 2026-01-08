# Instagram Carousel - Roadmap

## Status: DEPRECATED

This skill was converted to an agent in January 2026. See `.claude/agents/instagram-carousel.md` for the active implementation.

## What's Shipped (Historical)

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial skill with carousel generation |
| v2.0 | 2026-01 | Converted to agent for skill orchestration |

## Why the Migration

The skill pattern hit its limits:
- Couldn't invoke hook-stack-evaluator properly
- Couldn't coordinate multi-step pipeline
- Automation mode detection failed in skill-to-skill calls

Agent pattern solved all three. The capability is now more powerful.

## Resources Preserved

The skill folder is kept because the agent reads from:
- `resources/visual-metaphors.md`
- `resources/secondary-characters.md`
- `resources/carousel-formats.md`
- `resources/prompt-templates.md`

These are the "content library" the agent draws from. Expanding these expands carousel variety.

## Future Ideas (For the Agent)

See `.claude/agents/docs/instagram-carousel/ROADMAP.md` for current roadmap.

Ideas that would improve the resources in this folder:
- **More visual metaphors** - Expand the metaphor library beyond current options
- **Character variations** - More secondary character types for different niches
- **Format templates** - Additional slide layouts for different content types
- **Style presets** - Different visual styles (minimalist, bold, corporate, playful)

## What We Learned

**Pattern recognition matters.** When a skill starts needing to call other skills, that's the signal to convert to an agent. We didn't see it until hook-stack-evaluator integration failed.

**Keep resources separate from orchestration.** The skill folder holds assets. The agent holds logic. Clean separation.

**Deprecate, don't delete.** The skill folder has value even with a deprecated SKILL.md. Those resource files are still earning their keep.
