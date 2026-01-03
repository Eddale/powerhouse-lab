# Nano Banana Pro Prompt Templates

## The Core Philosophy

**"The model fails when YOU haven't decided what matters. Most bad outputs are undecided prompts."**

Prompt like a **creative director**, not a poet:
- Less description, more intent and hierarchy
- Treat the model as a **layout engine**, not an artist
- Declare what matters before describing what exists
- Reduce ambiguity, don't increase detail

## The Creative Director Framework

Every prompt answers these questions IN THIS ORDER:

1. **What this image is FOR** (purpose, not subject)
2. **What must be immediately understood** (the one idea)
3. **Where the eye goes first** (visual hierarchy)
4. **What supports that** (secondary elements)
5. **What must NOT compete** (constraints)

## The Master Template

```
PURPOSE: [What is this image for? Who sees it? What must they feel/understand?]

HIERARCHY:
- Eye goes to: [The ONE thing - usually the text]
- Supports that: [Visual element that reinforces the message]
- Must not compete: [What to explicitly exclude]

COMPOSITION:
- Text placement: [top/center/bottom]
- Negative space: [where and why]
- Frame: [what's included, what's cropped]

STYLE: [Artistic approach - e.g., Manga illustration, high contrast linework]
TEXT TO RENDER: "[Exact text to appear in image]"
ASPECT: [Ratio - 4:5 for Instagram]
```

## Slide-Specific Templates

### Hook Slide (Slide 1)

```
PURPOSE: Instagram carousel hook (slide 1 of 7). The viewer must feel "[emotion]" and stop scrolling.

HIERARCHY:
- Eye goes to: The text "[hook text]" - this IS the image
- Supports that: [Character reacting with shock/curiosity/realization]
- Must not compete: Clean background, no secondary text, no distracting details

COMPOSITION:
- Text: Top third, massive, impossible to miss
- Negative space: Clean area around text for breathing room
- Character: Lower half, looking up at text or reacting to it

STYLE: Manga illustration, high contrast, speed lines for impact
TEXT TO RENDER: "[Hook text]"
ASPECT: 4:5
```

### Problem/Context Slide (Slide 2)

```
PURPOSE: Instagram carousel problem slide (slide 2 of 7). Viewer must understand what's broken/changed.

HIERARCHY:
- Eye goes to: The contrast or stat that shows the problem
- Supports that: Visual metaphor for the problem
- Must not compete: Keep background minimal

COMPOSITION:
- Text: Center or top, bold
- Visual: [Metaphor - e.g., "30 DAYS" crossed out, "8 MONTHS" emphasized]
- Negative space: Generous margins

STYLE: Manga illustration, same visual language as slide 1
TEXT TO RENDER: "[Problem statement]"
ASPECT: 4:5
```

### Value Slide (Slides 3-5)

```
PURPOSE: Instagram value slide (slide [N] of 7). Viewer must learn [specific insight].

HIERARCHY:
- Eye goes to: The key teaching point
- Supports that: Visual that makes the concept concrete
- Must not compete: One visual metaphor only

COMPOSITION:
- Text: [Position based on visual]
- Visual: [Simple metaphor that illustrates the point]
- Clean background

STYLE: Manga, consistent with carousel
TEXT TO RENDER: "[Teaching point]"
ASPECT: 4:5
```

### Summary Slide (Slide 6)

```
PURPOSE: Instagram summary slide (slide 6 of 7). Viewer must feel the transformation click.

HIERARCHY:
- Eye goes to: The "so what" statement
- Supports that: Character with expression of realization/confidence
- Must not compete: No new information, just the payoff

COMPOSITION:
- Text: Centered, definitive
- Character: Confident pose, looking forward
- Clean, open background

STYLE: Manga, high contrast
TEXT TO RENDER: "[Summary statement]"
ASPECT: 4:5
```

### CTA Slide (Slide 7)

```
PURPOSE: Instagram CTA slide (slide 7 of 7). Viewer must know exactly what to do next.

HIERARCHY:
- Eye goes to: The action word (Follow, Save, Comment)
- Supports that: Visual cue pointing to action
- Must not compete: No distracting elements

COMPOSITION:
- Text: Large, clear, centered
- Visual: Arrow, hand gesture, or character pointing
- Maximum breathing room

STYLE: Manga, consistent with carousel
TEXT TO RENDER: "[CTA text]"
ASPECT: 4:5
```

## What NOT to Do

### Don't: Keyword Soup
```
BAD: "dog, park, 4k, realistic, beautiful, award-winning, masterpiece, trending on artstation"
```

### Don't: Competing Goals
```
BAD: "Cinematic and dramatic with perfectly readable text overlay"
(Cinematic = moody/dark. Readable text = high contrast. These compete.)
```

### Don't: Vague Negatives
```
BAD: "No bad quality, no ugly elements"
(What is "bad"? What is "ugly"? These are too abstract.)
```

### Don't: Add More to Fix Problems
```
BAD: Image came out wrong, let me add 50 more words of description...
(Usually makes it worse. Change ONE thing. Or start fresh with clearer hierarchy.)
```

## Ultra-Minimal Alternative

When the Creative Director format feels heavy, use the 25-word version:

```
Manga illustration: [character/scene description]. Bold text [position]: "[exact text]". [One constraint]. 4:5.
```

Example:
```
Manga illustration: shocked business coach watching book burn. Bold text top: "The advice we were all taught is now destroying coaching businesses." Clean background. 4:5.
```

## Iteration Pattern

When a prompt doesn't work, iterate in passes:

1. **Concept pass** - Is the PURPOSE clear? What is this image FOR?
2. **Hierarchy pass** - Is it obvious what the eye goes to FIRST?
3. **Constraint pass** - Did you specify what must NOT compete?

Change ONE variable per iteration. If style is drifting, start a new session.

## Reference Images

When including Ed as narrator or for character consistency:
- Include the reference photo
- Add instruction: "Use the supplied image as reference for the character"
- Nano Banana Pro supports up to 14 reference images

## Technical Notes

- **Aspect ratio:** 4:5 for Instagram (takes up more screen)
- **Text:** Keep to 25 characters or less for best rendering
- **Resolution:** Specify "2K" if needed (uppercase K required)
- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro)
