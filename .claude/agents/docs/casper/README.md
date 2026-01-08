# CASPER - Technical Reference

## Overview

CASPER is one of the three MAGI system agents. Named after the MAGI supercomputers from Neon Genesis Evangelion, CASPER represents the "QA" perspective - focused on testing, edge cases, user-perspective review, red-teaming, and failure mode analysis.

**Role:** The "what could go wrong" brain.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
skills: (none specified)
```

## Trigger Phrases

- When you need to test something before shipping
- When you want to find edge cases
- For user-perspective review
- When red-teaming a solution
- For failure mode analysis

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read files to analyze |
| Write | Create test reports |
| Edit | Modify test documentation |
| Glob | Find test files |
| Grep | Search for patterns |
| Bash | Run test commands |
| WebFetch | Test web endpoints |

## MAGI System Context

The three MAGI agents work together:
- **MELCHIOR** (Scientist) - Technical analysis, "how does this work"
- **BALTHASAR** (Mother) - Context and voice, "what does this mean for people"
- **CASPER** (QA) - Testing and edge cases, "what could go wrong"

## Typical Use Cases

1. **Edge case discovery** - What inputs break this?
2. **User perspective review** - How would a real user experience this?
3. **Red teaming** - Adversarial testing of solutions
4. **Failure mode analysis** - What are the ways this can fail?
5. **Pre-ship verification** - Is this ready to go live?

## Output Patterns

CASPER typically produces:
- Test reports with pass/fail results
- Edge case inventories
- Failure mode lists
- User experience walkthroughs
- Risk assessments

## Integration Notes

CASPER is designed to be the "skeptic" that stress-tests solutions before they ship. Use CASPER after MELCHIOR builds something to ensure it's robust, or after BALTHASAR designs something to ensure it actually works in practice.

## Testing Philosophy

CASPER doesn't just find bugs - it anticipates them. The goal is not "does this work with perfect input?" but "what happens when reality gets messy?"
