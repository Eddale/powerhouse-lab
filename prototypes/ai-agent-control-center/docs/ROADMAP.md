# AI Agent Control Center - Roadmap

## Status: Prototype

Early-stage concept for a "Personal AI Operating System" - a central hub for managing AI agents.

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v0.1 | 2024-12 | Initial concept with README, SKILL.md, CLAUDE.md |
| v0.2 | 2026-01 | Added docs/ folder with ROADMAP |

## The Concept

A centralized system where:
- **Agent Inbox.md** - Drop-zone for new requests
- **Active Agents.md** - Live dashboard of running tasks
- **SKILL.md** - Manager agent that orchestrates work

Leverages Obsidian for storage, GitHub for skill definitions. Agents pick up tasks, execute using skills, report back.

## Why It Paused

The problem it solves (tracking multiple AI agents) became less urgent once Claude Code's Task tool enabled background agent management. The native solution may be sufficient.

Worth revisiting if:
- Agent coordination becomes complex again
- Multi-user/team scenarios emerge
- Need for persistent agent state across sessions

## Ideas (If Resumed)

- **Queue Management** - Priority ordering of agent tasks
- **Status Dashboard** - Visual view of what's running
- **Agent Memory** - Persistent context between sessions
- **Team Mode** - Multiple users coordinating agents

## Lessons Captured

- Sometimes the platform evolves faster than the prototype
- Good to document concepts even if paused
- May become relevant again at scale

## Decision Log

When/if we resume, plans go in `plans/` and decisions get archived to `plans/archive/`.
