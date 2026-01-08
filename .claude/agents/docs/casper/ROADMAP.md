# CASPER - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial MAGI agent for QA and testing |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

CASPER becomes the automated QA layer for everything in the Powerhouse Lab. Before any skill ships, before any agent goes live, CASPER reviews it.

Eventually, CASPER could:
- Run automated test suites on new skills
- Generate edge case tests automatically
- Maintain a "known issues" database
- Provide pre-flight checklists for different artifact types

## Planned Improvements

- [ ] **Automated Test Generation** - Given a skill's SKILL.md, generate test cases
- [ ] **Pre-Ship Checklist** - Standard QA checks that run before any commit
- [ ] **Edge Case Library** - Database of common edge cases to check across all skills

## Ideas (Not Committed)

- **Regression Testing** - Track what broke between versions
- **Performance Testing** - How does this handle load/scale?
- **Security Review** - Basic security checklist for new features
- **Accessibility Audit** - Does this work for all users?
- **Integration Testing** - Do these skills play nice together?

## What We've Learned

The best QA happens early. When CASPER is involved late, problems are expensive to fix. When CASPER is involved early, problems are design decisions.

CASPER needs Bash access to actually run tests - without it, CASPER can only theorize about what might break. With Bash, CASPER can prove what actually breaks.

## Decision Log

Decisions about CASPER improvements get planned in `plans/` and archived in `plans/archive/`.
