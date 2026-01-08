# Research: Agent vs Direct Execution Patterns

**Research Date:** 2026-01-08
**Source:** [[Research - Agent vs Direct Patterns - 2026-01-08]] in Zettelkasten

## Key Findings

### Anthropic's Official Guidance

> "Agentic systems often trade latency and cost for better task performance."
> "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed."

### Decision Framework

| Pattern | Use When | Example |
|---------|----------|---------|
| Direct/Skill | Interactive, sequential, user present | Morning routine, single-file edits |
| Workflow | Multi-step with dependencies | Capture -> classify -> route |
| Agent | Autonomous, parallel, context-isolating | Research swarm, parallel review |

### The Win-The-Day Diagnosis

Morning routine failed the agent test:
1. Ed was present and watching (interactive, not autonomous)
2. Sequential, dependent steps (no parallelization benefit)
3. Simple, well-defined task (skill-level complexity)
4. Fast turnaround needed

**Root Cause:** Agent overhead (context initialization, resume cycles) added latency without benefit.

### Heuristic

Before spawning any agent, ask:
1. Is Ed walking away? (autonomous required)
2. Are there 2+ independent tasks that can run in parallel?
3. Would the work bloat my context unacceptably?

**If no to all three: execute directly.**

### Recommendation for Win-The-Day

Redesign as a **skill** that main agent executes directly:
- Read today's note
- Apply task-clarity-scanner to tasks
- Apply capture-triage to captures
- Report summary

No delegation, no subagent spawn, no resume cycles.

---

*See full research document in Zettelkasten for complete sources and analysis.*
