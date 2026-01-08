# Newsletter Writer Agent - Technical Reference

## Overview

The Newsletter Writer agent is a fully automated pipeline for turning topics, YouTube URLs, ideas, or experiences into complete newsletter articles for The Little Blue Report. It handles the full process from input to Obsidian-saved, daily-note-linked draft.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Bash, AskUserQuestion
skills: youtube-processor, mission-context, hook-stack-evaluator, ai-slop-detector
```

## Trigger Phrases

- "write a newsletter about..."
- "turn this into a newsletter article"
- "newsletter from [topic/URL/idea]"
- Any request to create newsletter content

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read source materials, existing drafts |
| Write | Create article drafts |
| Edit | Revise and refine content |
| Glob | Find related files |
| Grep | Search for context |
| WebFetch | Retrieve URLs (YouTube, articles) |
| WebSearch | Research topics |
| Bash | Run skill tools (youtube-processor) |
| AskUserQuestion | Clarify direction, get feedback |

## Skills Used

- **youtube-processor** - Extract video transcripts for video-based articles
- **mission-context** - Ed's voice, audience, terminology
- **hook-stack-evaluator** - Score and improve headlines
- **ai-slop-detector** - Clean AI patterns from final draft

## Pipeline Stages

1. **Input Processing** - Identify input type (topic, URL, idea, experience)
2. **Research/Extraction** - Gather source material (transcript, web research, etc.)
3. **Outline Development** - Structure the article
4. **Draft Writing** - Write the full article
5. **Hook Evaluation** - Score headline with Hook Stack
6. **Slop Detection** - Clean AI writing patterns
7. **Save & Link** - Save to Zettelkasten, link in daily note

## Output Location

Drafts saved to: `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/`

Filename pattern: `Newsletter Draft - [Title] - YYYY-MM-DD.md`

Automatically linked in the day's Captures section.

## Automation Mode

When invoked with "automatically" or "without asking," the agent:
- Makes reasonable decisions without confirmation
- Completes the full pipeline end-to-end
- Only stops for actual errors

Without automation signals, the agent may pause for user feedback at key stages.
