# Win The Day - Roadmap

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v2.0 | 2026-01-10 | Converted from agent to skill, added morning-metrics |
| v1.0 | 2026-01-08 | Original agent with capture-triage + task-clarity-scanner |

## Planned

- [ ] Substack metrics in morning briefing
- [ ] Revenue snapshot (Stripe integration)
- [ ] Smart urgency detection (meetings in next hour, VIP emails)
- [ ] Weekly summary mode ("win the week")

## Ideas (Not Committed)

- Slack/Discord integration for team updates
- Weather integration (affects energy/planning)
- Focus mode suggestion based on calendar density
- "End of day" counterpart skill

## What We've Learned

### 2026-01-10 - Agent → Skill Conversion
- Skills execute faster than agents for interactive workflows
- The "Ed is watching" test: if latency matters, use a skill
- Sub-skill orchestration works via natural language instruction
- Python scripts for API calls, skills for workflow logic

### 2026-01-08 - Original Build
- Facilitator pattern > autonomous pattern for morning routines
- Human-in-the-loop at each step prevents runaway operations
- AskUserQuestion is essential for batch approvals

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Skill over agent | Faster execution, less overhead for interactive work |
| Python for metrics | Clean API handling, JSON output for Claude to format |
| Sub-skill calls via instruction | Simpler than agent orchestration, Claude handles discovery |
| Automation mode | Sometimes Ed wants quick status, not full interactive flow |
