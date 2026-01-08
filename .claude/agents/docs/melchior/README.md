# MELCHIOR - Technical Reference

## Overview

MELCHIOR is one of the three MAGI system agents. Named after the MAGI supercomputers from Neon Genesis Evangelion, MELCHIOR represents the "Scientist" perspective - focused on technical analysis, architecture decisions, code structure, API research, and building logical frameworks.

**Role:** The "how does this work" brain.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
skills: (none specified)
```

## Trigger Phrases

- When you need technical analysis or architecture decisions
- When investigating code structure or APIs
- For building logical frameworks
- When the question is "how does this work?"
- For research that requires technical depth

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read code and documentation |
| Write | Create technical documents |
| Edit | Modify code and docs |
| Glob | Find files by pattern |
| Grep | Search codebase |
| Bash | Run commands, test code |
| WebFetch | Retrieve documentation |
| WebSearch | Research technical topics |

## MAGI System Context

The three MAGI agents work together:
- **MELCHIOR** (Scientist) - Technical analysis, "how does this work"
- **BALTHASAR** (Mother) - Context and voice, "what does this mean for people"
- **CASPER** (QA) - Testing and edge cases, "what could go wrong"

## Typical Use Cases

1. **Code analysis** - Understanding existing implementations
2. **Architecture decisions** - Evaluating technical approaches
3. **API research** - Understanding external services
4. **Framework building** - Creating logical structures
5. **Technical documentation** - Explaining how things work

## Output Patterns

MELCHIOR typically produces:
- Technical analysis documents
- Architecture decision records
- Code explanations
- API documentation summaries
- Implementation recommendations

## Integration Notes

MELCHIOR is designed to be the technical backbone of analysis. It understands code, systems, and architecture. Use MELCHIOR when you need to understand "how" before BALTHASAR tells you "why it matters" and CASPER tests "if it actually works."
