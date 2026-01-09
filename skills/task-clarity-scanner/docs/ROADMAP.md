# Task Clarity Scanner - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2025-12 | Initial Kanban-aware task scanner |
| v1.1 | 2026-01 | Added staleness tracking with (MM-DD) suffix |
| v1.2 | 2026-01 | Added project file creation option |
| v1.3 | 2026-01 | Added docs/ folder (README, GUIDE, ROADMAP) |
| v1.4 | 2026-01-09 | Waiting For System: blocked item tracking, follow-up dates, name fuzzy-match, resolve flow |

## The Vision

Right now, the skill clarifies tasks and manages Kanban flow. You still execute the tasks yourself.

The vision: execution handoff. Clarify a task, approve it, and optionally spin up an agent to do it. "This task is ready to go. Want me to start working on it?"

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **Execution Mode** - After clarifying, offer to execute clear tasks immediately via agent handoff.

- [ ] **Weekly Review Integration** - End-of-week scan across all daily notes from the week. Surface patterns, stale items, wins.

- [ ] **Smart Scheduling** - When clarifying, suggest which day a task should actually happen based on estimated size and calendar load.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **Time Estimates** - Ask for time estimates during clarification. "This looks like 2 hours. Is that right?"

- **Energy Matching** - Tag tasks as high/low energy. Help match tasks to time of day.

- **Dependency Mapping** - Visual graph of which tasks block which others.

- **Someday/Maybe Review** - Periodic scan of parked items. "You parked this 30 days ago. Still interested?"

- **Team Mode** - Waiting For items could integrate with team tools. "Sarah was supposed to send X - want to follow up?"

- **Call Links** - When bb-meeting-summary processes a call, auto-link to Waiting For items for that client. Builds contact history over time. (Template already has `call-links: []` field ready.)

- **Calendar Integration** - Know what meetings are coming. "You have 3 hours before your next call - here's what you could finish."

## What We've Learned

Building this skill taught us a few things:

**WIP limits work.** Three tasks in Today's 3 feels limiting until you realize you actually complete things. Without limits, everything is "in progress" and nothing is done.

**Staleness needs a system.** The (MM-DD) suffix enables automatic age tracking. Without it, you can't distinguish "I added this yesterday" from "this has been rolling for two weeks."

**Batch before execute.** Clarifying one task often surfaces related tasks. Batching all clarifications before applying changes prevents partial updates.

**Project files save tasks.** When something's too big to clarify, the project file upgrade prevents it from becoming stale. It's not a task anymore - it's a living document.

**The health check catches drift.** Without it, Today's 3 slowly becomes Today's 7. The explicit count keeps the system honest.

**Waiting For needs its own system.** Blocked items aren't tasks - they're dependencies. Mixing them with active work creates confusion. The separate Waiting For section keeps the board honest about what you can actually act on.

**Name consistency prevents fragmentation.** The fuzzy-match check before creating Waiting For items catches spelling variations (Jon/John). First occurrence becomes canonical. Small friction that prevents big mess.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
