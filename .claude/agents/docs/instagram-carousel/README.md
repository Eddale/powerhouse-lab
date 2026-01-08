# Instagram Carousel Agent - Technical Reference

## Overview

The Instagram Carousel agent transforms articles, newsletters, or ideas into complete Instagram carousel packages. It handles the full pipeline from content analysis to slide creation to image prompt generation.

## Agent Configuration

```yaml
model: sonnet
tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
skills: mission-context
```

## Trigger Phrases

- "create a carousel"
- "turn this into slides"
- "Instagram carousel from article"
- Any request to convert content to carousel format

## Tools Access

| Tool | Purpose |
|------|---------|
| Read | Read source content (articles, newsletters) |
| Write | Create slide markdown and prompt files |
| Edit | Modify carousel content |
| Glob | Find source files |
| Grep | Search content |
| AskUserQuestion | Confirm style, character, platform choices |

## Skills Used

- **mission-context** - Provides Ed's voice, audience context, and terminology

## Pipeline Stages

1. **Content Ingestion** - Read and analyze source material
2. **Hook Extraction** - Identify the strongest hook for slide 1
3. **Story Arc Design** - Structure the carousel narrative (10 slides typical)
4. **Slide Writing** - Write copy for each slide
5. **Visual Planning** - Determine what each slide should show
6. **Prompt Generation** - Create Nano Banana Pro prompts for images

## Output Files

The agent creates a package folder with:
- `carousel-brief.md` - Overview and hook analysis
- `slides.md` - All slide copy in sequence
- `image-prompts.md` - Nano Banana Pro prompts for each slide
- Individual prompt files if requested

## Nano Banana Pro Integration

Image prompts follow Nano Banana Pro requirements:
- Reference image instruction for character consistency
- "the man from the reference image" phrasing (not "you")
- Specific style and mood guidance
- 16:9 or 4:5 aspect ratio specifications

## Notes

This agent supersedes the deprecated instagram-carousel skill. The skill remains for backwards compatibility but points users to this agent.
