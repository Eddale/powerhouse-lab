# Newsletter Brainstorm - Roadmap

## Status: Early Prototype / Likely Superseded

This prototype was an early exploration of newsletter ideation. The newsletter-coach skill has since been built and provides more comprehensive functionality.

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v0.1 | 2024-12 | Initial SKILL.md with concept |
| v0.2 | 2026-01 | Added docs/ folder with ROADMAP |

## The Original Concept

Generate hook angles, subject lines, and rough outlines for The Little Blue Report based on a topic.

**Inputs:**
- Topic (required)
- Audience context (optional)
- Constraints (optional)

**Outputs:**
- 3-5 hook angles
- 5+ subject lines per angle
- Rough outline for chosen angle

## Likely Superseded By

**newsletter-coach skill** - More comprehensive 7-phase process that includes:
- Experience extraction (Phase 1-3)
- Headline generation (Phase 4)
- Outline building (Phase 5)
- Section expansion (Phase 6)
- Final draft (Phase 7)

Newsletter-coach does what newsletter-brainstorm envisioned, plus more.

## Decision Point

Options:
1. **Archive** - Move to `archive/` with POSTMORTEM noting newsletter-coach supersedes it
2. **Differentiate** - If there's a use case newsletter-coach doesn't cover, develop that
3. **Merge** - Absorb any unique ideas into newsletter-coach

Recommendation: Archive with note. Newsletter-coach covers the use case.

## What We Learned

- Start with exploration prototypes
- Some prototypes become skills, some get absorbed
- Documentation captures the journey even for paths not taken

## Decision Log

When we make decisions about this prototype's fate, record in `plans/archive/`.
