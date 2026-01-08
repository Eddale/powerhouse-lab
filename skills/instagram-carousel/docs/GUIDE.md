# Instagram Carousel - How It Works

## Status: DEPRECATED

This skill has been converted to an agent. This guide explains why and points you to the right place.

## What Happened

The carousel creator started as a skill. But it hit a wall: skills can't easily call other skills.

The carousel pipeline needs to:
1. Extract content from an article
2. Create slide copy
3. Run headlines through hook-stack-evaluator
4. Generate image prompts
5. Package everything together

That's orchestration work. That's what agents do.

## Where the Capability Went

The agent at `.claude/agents/instagram-carousel.md` now handles carousel creation. Same triggers work:
- "Create a carousel from this article"
- "Turn this into slides"

The resources in this folder (metaphors, characters, formats, prompts) are still used by the agent. The skill folder is kept for these assets.

## The Lesson

**Skills execute. Agents orchestrate.**

If something needs to call multiple skills in sequence, make it an agent. If it's a single capability with clear inputs/outputs, make it a skill.

The carousel creator crossed that line - it needed to coordinate multiple capabilities. Agent was the right pattern.
