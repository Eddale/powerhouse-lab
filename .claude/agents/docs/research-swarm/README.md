# Research Swarm Agent - Technical Reference

## Overview

The Research Swarm agent performs multi-angle parallel research by spawning multiple sub-agents, each investigating a topic from a different perspective. Results are gathered and synthesized into a comprehensive research document.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, Bash
skills: youtube-processor
```

## Trigger Phrases

- "research [topic] from multiple angles"
- "run a research swarm on..."
- "investigate [topic] comprehensively"
- When you need 3+ research perspectives simultaneously

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read existing research, context |
| Write | Create research documents |
| Edit | Refine research outputs |
| Glob | Find related files |
| Grep | Search knowledge base |
| WebFetch | Retrieve web content |
| WebSearch | Search for information |
| Task | Spawn parallel research sub-agents |
| Bash | Run tools (youtube-processor) |

## Skills Used

- **youtube-processor** - When research sources include YouTube videos

## How It Works

1. **Angle Identification** - Determine 3-5 distinct research angles
2. **Parallel Spawning** - Launch sub-agents for each angle simultaneously
3. **Independent Research** - Each sub-agent investigates its angle
4. **Result Collection** - Gather findings from all sub-agents
5. **Synthesis** - Combine insights into unified document
6. **Save & Link** - Save to Zettelkasten, link in daily note

## Research Angles (Examples)

For a topic like "AI for coaching":
- **Technical angle** - What AI capabilities are available?
- **Market angle** - Who's doing this well? What's selling?
- **Implementation angle** - How would you actually build this?
- **User angle** - What do coaches actually want/need?
- **Risk angle** - What could go wrong?

## Output Location

Research saved to: `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/`

Filename pattern: `Research Swarm - [Topic] - YYYY-MM-DD.md`

Automatically linked in the day's Captures section.

## Performance Notes

Parallel execution significantly reduces total research time compared to sequential investigation. A 5-angle swarm that would take 25 minutes sequentially can complete in 8-10 minutes parallel.
