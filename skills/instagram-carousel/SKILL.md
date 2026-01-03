---
name: instagram-carousel
description: Turn articles into Instagram carousel concepts with Nano Banana Pro image prompts. Use when creating carousels, repurposing newsletter content for Instagram, or generating manga-style slide images. Triggers on "create a carousel", "turn this into slides", "Instagram carousel from article".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Instagram Carousel Skill

## What This Does

Transforms newsletter articles (or topics) into Instagram carousel concepts with image prompts optimized for Nano Banana Pro (`gemini-3-pro-image-preview`).

**Output package:**
- 5-7 carousel slides (text + image prompt each)
- Instagram caption with hook, body, CTA, and hashtags
- Hook evaluation via hook-stack-evaluator

## When to Use

- "Create an Instagram carousel from this article"
- "Turn this into slides"
- "Make a carousel for [topic]"
- "Repurpose this newsletter for Instagram"
- "Generate carousel prompts for..."

## Phases

### Phase 1: Parse Input

**If given an article:**
1. Read the full article
2. Identify the core argument/thesis
3. Extract 3-5 key teaching points
4. Note any surprising stats or quotes
5. Identify the transformation promised

**If given a topic:**
1. Ask clarifying questions about the angle
2. Identify the target audience
3. Determine the core insight to communicate

### Phase 2: Structure Carousel

Load `resources/carousel-formats.md` for structure options.

**Default: 7-slide structure**

| Slide | Purpose | What to Extract |
|-------|---------|-----------------|
| 1 | Hook | The most provocative claim or question |
| 2 | Problem/Context | What's broken, why this matters now |
| 3 | Value Point 1 | First teaching insight |
| 4 | Value Point 2 | Second teaching insight |
| 5 | Value Point 3 | Third teaching insight |
| 6 | Summary | The "so what" - the transformation |
| 7 | CTA | Follow, save, link in bio |

**Condensed: 5-slide structure** (for simpler topics)
- Hook → Problem → Value (combined) → Summary → CTA

### Phase 3: Write Slide Copy

For each slide, write the TEXT THAT APPEARS ON THE IMAGE.

**Rules:**
- Keep text SHORT - aim for 10 words or less per slide
- One idea per slide
- Use punchy, scroll-stopping language
- Front-load the most important word

**Examples:**
- GOOD: "30 days to 8 months. That's how long it takes now."
- BAD: "The average time from first contact to becoming a client has increased significantly from 30 days to 8 months"

### Phase 4: Generate Image Prompts

Load `resources/prompt-templates.md` for the Creative Director Framework.

**For EACH slide, generate an image prompt using this structure:**

```
PURPOSE: Instagram carousel slide [N of 7]. The viewer must instantly understand [one idea].

HIERARCHY:
- Eye goes to: [text/focal point]
- Supports that: [image element]
- Must not compete: [what to avoid - usually "clean background, no secondary text"]

COMPOSITION:
- Text placement: [top/center/bottom]
- Negative space: [where and why]
- Character/visual: [supporting element]

STYLE: Manga illustration, high contrast linework
TEXT TO RENDER: "[Exact slide copy]"
ASPECT: 4:5
```

**Key principle:** "The model fails when YOU haven't decided what matters."

### Phase 5: Evaluate Hook

Run slide 1's text through hook-stack-evaluator.

Provide:
- The hook text
- Target audience (from Phase 1)
- Context: "Instagram carousel hook"

If score is below 10/15, iterate on the hook before finalizing.

### Phase 6: Write Caption

Write the Instagram caption (the text that appears below the carousel).

**Structure:**
```
[Hook line - repeat or expand slide 1]

[Body - 3-5 bullet points summarizing value]
→ Point 1
→ Point 2
→ Point 3

[CTA - what you want them to do]

[Hashtags - 5-10 relevant tags]
```

**Rules:**
- First line must hook (it's the preview)
- Use → arrows for easy scanning
- Include "Save this" or "Share with..." CTA
- Hashtags at the end, not inline

### Phase 7: Save to Zettelkasten

Save the complete carousel output as a markdown file for easy copy/paste into Google AI Studio.

**File location:**
```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Carousel - [Short Title] - YYYY-MM-DD.md
```

**File format:**
```markdown
---
type: carousel
date: YYYY-MM-DD
source: [article title or topic]
status: draft
tags: [instagram, carousel, nano-banana-pro]
---

# Carousel: [Title]

[Full carousel output from Output Format section]
```

**After saving:**
1. Add link to today's daily note Captures section
2. Tell Ed the file path so he can open it

**Daily note location:**
```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
```

**Captures link format:**
```
- [[Carousel - [Short Title] - YYYY-MM-DD]] - Instagram carousel for [topic]
```

## Style Variants

### Default: Manga Reaction

Clean background, bold text, manga character reacting to the statement. Use for most slides.

Load `resources/manga-style-guide.md` for details.

### Variant: Narrator Mode

Ed appears as an illustrated narrator within the scene. Use for explainer-style slides where personal presence adds credibility.

When using Narrator Mode, include instruction: "Include the reference image of Ed as an illustrated manga character narrating the scene."

## Output Format

Present the complete carousel as:

```
# CAROUSEL: [Title]

## SLIDE 1 (Hook)
**Text:** [slide copy]
**Prompt:**
[full image prompt]

## SLIDE 2 (Problem)
**Text:** [slide copy]
**Prompt:**
[full image prompt]

[...continue for all slides...]

---

## INSTAGRAM CAPTION
[full caption with hashtags]

---

## HOOK EVALUATION
Score: [X]/15
[feedback from hook-stack-evaluator]
```

## Guidelines

1. **Less is more** - Short slide copy beats long explanations
2. **Hierarchy-first** - Always specify what the eye goes to FIRST
3. **"Must not compete"** - This constraint is the secret sauce for clean images
4. **One idea per slide** - If you're cramming, add a slide
5. **Test the hook** - Slide 1 makes or breaks the carousel

## Version History

- v1.1 (2026-01-03): Added Phase 7 - auto-save to Zettelkasten for easy copy/paste workflow
- v1.0 (2026-01-03): Initial release with Creative Director Framework, manga default style
