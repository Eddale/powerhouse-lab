# MELCHIOR - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01 | Initial MAGI agent for technical analysis |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |

## The Vision

MELCHIOR becomes the go-to technical research and analysis agent. Any question about "how does this work" gets routed to MELCHIOR for a thorough, accurate answer.

Eventually, MELCHIOR could:
- Maintain a technical knowledge base of analyzed systems
- Auto-document code as it's written
- Generate architecture decision records automatically
- Provide technical review of proposed changes

## Planned Improvements

- [ ] **Technical Knowledge Base** - Store and retrieve previous analyses
- [ ] **Code Documentation Generation** - Auto-generate docs from code analysis
- [ ] **Architecture Decision Records** - Template for capturing technical decisions

## Ideas (Not Committed)

- **Dependency Analysis** - Map dependencies across the project
- **Security Review** - Basic security analysis of implementations
- **Performance Analysis** - Identify potential bottlenecks
- **Tech Debt Tracking** - Log and prioritize technical debt items
- **API Compatibility Checks** - Verify external API changes don't break integrations

## What We've Learned

MELCHIOR's power is in having access to the full toolkit - Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch. This allows comprehensive technical analysis that spans code, documentation, and external resources.

The key is scope. MELCHIOR should stay technical. When questions drift into "should we do this?" territory, that's BALTHASAR (for human impact) or Ed (for business decisions).

## Decision Log

Decisions about MELCHIOR improvements get planned in `plans/` and archived in `plans/archive/`.
