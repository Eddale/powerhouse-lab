# Reflect - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v0.1 | 2026-01-06 | Initial scaffold - manual mode only |
| v0.2 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

Right now, reflect is manual. You trigger it when you remember to.

The vision: automatic reflection at session end. Every session gets scanned. High-confidence findings get committed automatically. You wake up to a changelog of what improved.

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Hook Integration** - Automatic reflection via Claude Code stop hook. Session ends, reflection runs.

- [ ] **Changelog Generation** - Track all reflect commits over time. "This week: 5 skill updates from 3 sessions."

- [ ] **Cross-Session Patterns** - Notice when the same correction happens multiple times across sessions. "You've corrected this 3 times now - definitely add to Iron Rules."

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Reflection Dashboard** - Visual summary of learnings over time. Categories, frequency, which skills updated most.

- **Undo Capability** - Revert a reflect commit if the learning turned out to be wrong.

- **Team Reflection** - If multiple people use the same skills, aggregate their corrections. "3 people corrected this - definitely update."

- **Learning Suggestions** - Proactively suggest corrections based on patterns. "You seem to prefer X over Y - want to codify that?"

- **Skill Health Score** - Track how often skills get reflected-on. Frequently corrected skills might need redesign.

- **Export to CLAUDE.md** - Some learnings belong in CLAUDE.md (project-wide rules) not skill files. Auto-detect and route appropriately.

## What We've Learned

Building this skill taught us a few things:

**Confidence levels prevent over-correction.** Without them, every observation becomes a rule. The three-tier system ensures only clear corrections get proposed for immediate update.

**Manual mode first.** Automatic mode is tempting but risky. Manual mode lets you validate the workflow before automating it.

**Git commits are the record.** The `reflect:` prefix makes learnings searchable. "What did we learn last month?" → `git log --grep="reflect:"`

**Corrections are gifts.** Every time you correct the AI, you're giving it information. Reflect makes that information stick.

**Start simple.** The initial version is a scaffold. Better to ship something that works than wait for the perfect automatic system.

## TODO (Implementation)

- [ ] Test manual `/reflect` workflow
- [ ] Add hook configuration for automatic mode
- [ ] Create `tools/reflect.sh` for hook integration
- [ ] Add to CLAUDE.md workflow documentation

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
