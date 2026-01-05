---
name: reflect
description: Self-improving skills system. Analyzes conversation for corrections and learnings, proposes skill updates. Use when saying "reflect on this session", "what did we learn", or after completing significant work. Also triggered by /reflect command.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Reflect - Self-Improving Skills

## What This Does

Captures session learnings and proposes updates to skill files, closing the loop between
"Claude makes a mistake → You correct it → Same mistake next session."

## Who It's For

Ed and any vibe coder who wants their AI assistant to actually learn from corrections.

## The Problem It Solves

LLMs don't learn from us. Every conversation starts from zero. This skill bridges that gap
by turning corrections into persistent skill updates.

---

## Instructions

### Manual Mode (Default)

When user says "reflect", "/reflect", "what did we learn", or "update skills from this session":

1. **Scan the conversation** for:
   - Explicit corrections ("Never do X", "Always do Y", "Change this to...")
   - Approvals ("That's perfect", "Yes, like that", repeated patterns that worked)
   - Failed attempts that were fixed
   - New patterns discovered

2. **Classify each finding by confidence:**
   - **HIGH**: Explicit corrections from user ("Never make up button styles")
   - **MEDIUM**: Patterns that worked well without explicit approval
   - **LOW**: Observations worth noting but not confirmed

3. **For HIGH confidence findings:**
   - Identify the relevant skill file
   - Propose a specific edit (show old → new)
   - Generate commit message

4. **Present findings to user:**
   ```
   ## Session Learnings

   ### HIGH Confidence (Propose Immediate Update)
   - [Finding 1] → Update skill: [skill-name]
     Proposed change: [specific edit]

   ### MEDIUM Confidence (Consider Adding)
   - [Finding 2] → Could update: [skill-name]

   ### LOW Confidence (Note for Later)
   - [Observation]

   Approve changes? [Yes / Modify / Skip]
   ```

5. **On approval:**
   - Edit the skill file
   - Commit with message: `reflect: [summary of learning]`
   - Confirm completion

### Automatic Mode (Future - via Hook)

When enabled via stop hook, automatically run reflection at session end:
- Only commit HIGH confidence findings
- Show notification of what was updated
- Log to session summary

---

## Examples

### Example 1: Explicit Correction

**User said during session:**
```
"Never use emojis in code comments. I hate that."
```

**Reflect proposes:**
```
HIGH Confidence Finding:
- Rule: No emojis in code comments
- Relevant skill: mission-context
- Proposed addition to THE IRON RULES section:
  + 4. **NO EMOJIS IN CODE.** Unless explicitly requested.

Commit message: reflect: Add no-emojis rule to Iron Rules

Approve? [Yes / Modify / Skip]
```

### Example 2: Pattern Discovery

**User repeatedly approved same format:**
```
Session shows: User approved 3 research docs all using same header structure
```

**Reflect proposes:**
```
MEDIUM Confidence Finding:
- Pattern: Research docs use ## Executive Summary first
- Relevant skill: research-swarm agent
- Suggested note: "Always start research docs with Executive Summary section"

Add to Notes & Learnings? [Yes / Skip]
```

---

## Guidelines

- Only propose changes for HIGH confidence findings without explicit approval
- MEDIUM and LOW findings require user confirmation before any edits
- Never overwrite existing rules without showing the change
- Prefer adding to existing skills over creating new ones
- Commit messages always start with `reflect:` prefix

---

## Commands

| Command | Action |
|---------|--------|
| `/reflect` | Manual reflection on current session |
| `reflect on` | Enable automatic mode (requires hook setup) |
| `reflect off` | Disable automatic mode |
| `reflect status` | Show current mode and recent learnings |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-01-06 | Initial scaffold - manual mode only |

---

## Notes & Learnings

<!-- This section will be updated by the reflect skill itself -->
- Initial build based on Ras Mic's YouTube video approach
- Start with manual mode to validate workflow before adding hooks
- Confidence levels prevent over-eager updates

---

## TODO (Implementation)

- [ ] Test manual `/reflect` workflow
- [ ] Add hook configuration for automatic mode
- [ ] Create `tools/reflect.sh` for hook integration
- [ ] Add to CLAUDE.md workflow documentation
