# Mission Context - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial context document |
| v1.1 | 2026-01 | Added tech stack details |
| v1.2 | 2026-01 | Added runtime differences (CLI vs Claude.ai) |
| v1.3 | 2026-01 | Added skill architecture section |
| v1.4 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

Right now, mission-context is a flat document. You load it and get everything at once.

The vision: context that adapts. When building a skill, load the skill architecture section. When writing content, load the voice and terminology. When debugging, load the iron rules and tech stack.

Modular context that gives you what you need, not everything at once.

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Modular Sections** - Break into separate files that can be loaded independently. `mission-context/voice` vs `mission-context/tech` vs `mission-context/terminology`.

- [ ] **Auto-Update Triggers** - When Ed says "I'm using X now" or "add Y to my terminology," automatically update the relevant section without manual editing.

- [ ] **Version History** - Track what changed and when. "When did I add the runtime differences section?"

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Context Freshness Check** - Periodically verify tech stack is still accurate. "You mentioned Antigravity IDE - are you still using that?"

- **Terminology Glossary Generator** - Auto-generate a standalone glossary from the terminology section for sharing with collaborators.

- **Voice Samples Integration** - Link to actual newsletter examples that demonstrate the voice described in context.

- **Project Status Section** - Dynamic section that updates based on what's actively being worked on in powerhouse-lab.

- **Contact/Team Section** - Key people Ed works with, how to reference them, communication preferences.

- **Calendar Integration** - Current priorities based on what's actually scheduled. "This week is focused on X."

## What We've Learned

Building this skill taught us a few things:

**Context is foundational.** When other skills know who Ed is, outputs are dramatically better. The investment in this document pays dividends everywhere.

**The translation layer is critical.** Tech people and copywriters speak different languages. The translation table bridges that gap without either side having to change how they think.

**Runtime differences matter.** Skills that work in Claude Code can fail in Claude.ai. Documenting this saves debugging time.

**The prime directive filters everything.** "First AI win in 30 days. Then compound." When in doubt, check against this. It prevents scope creep and shiny object syndrome.

**Keep it updated.** Stale context causes confusion. When the tech stack changes, when new terminology emerges, when focus shifts - update immediately.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
