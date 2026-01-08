# BALTHASAR - Technical Reference

## Overview

BALTHASAR is one of the three MAGI system agents. Named after the MAGI supercomputers from Neon Genesis Evangelion, BALTHASAR represents the "Mother" perspective - focused on context-gathering, brand voice, coaching perspective, audience understanding, and empathetic analysis.

**Role:** The "what does this mean for people" brain.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
skills: mission-context
```

## Trigger Phrases

- When you need context about Ed's business, voice, or audience
- When you need to understand the "why" behind a decision
- For coaching perspective and empathetic analysis
- When gathering brand voice or audience understanding

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read existing files for context |
| Write | Create new analysis documents |
| Edit | Modify existing documents |
| Glob | Find files by pattern |
| Grep | Search content across files |
| WebFetch | Retrieve web content |
| WebSearch | Search the web for context |

## Skills Used

- **mission-context** - Provides Ed's business context, terminology, and voice

## MAGI System Context

The three MAGI agents work together:
- **MELCHIOR** (Scientist) - Technical analysis, "how does this work"
- **BALTHASAR** (Mother) - Context and voice, "what does this mean for people"
- **CASPER** (QA) - Testing and edge cases, "what could go wrong"

## Typical Use Cases

1. **Context gathering** - Understanding Ed's audience, business model, terminology
2. **Brand voice analysis** - Ensuring content matches Ed's voice
3. **Coaching perspective** - Viewing problems through a coach's lens
4. **Empathetic analysis** - Understanding user/customer perspective
5. **Audience understanding** - Who is Ed speaking to, what do they need

## Output Patterns

BALTHASAR typically produces:
- Context summaries
- Voice guidelines
- Audience profiles
- Empathy maps
- Coaching framework applications

## Integration Notes

BALTHASAR is designed to provide the human/emotional context that complements MELCHIOR's technical analysis. Use BALTHASAR first when you need to understand "why" before MELCHIOR figures out "how."
