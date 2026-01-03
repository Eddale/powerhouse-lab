# Nano Banana Pro Prompt Templates

## The Core Philosophy

**"The model fails when YOU haven't decided what matters. Most bad outputs are undecided prompts."**

Prompt like a **creative director**, not a poet:
- Less description, more intent and hierarchy
- Treat the model as a **layout engine**, not an artist
- Declare what matters before describing what exists
- Reduce ambiguity, don't increase detail

---

## The Creative Director Framework

Every prompt answers these questions IN THIS ORDER:

1. **What this image is FOR** (purpose, not subject)
2. **What must be immediately understood** (the one idea)
3. **Where the eye goes first** (visual hierarchy)
4. **What supports that** (secondary elements)
5. **What must NOT compete** (constraints)

---

## The Master Template (V2)

```
PURPOSE: [What is this image for? Who sees it? What must they feel/understand?]

HIERARCHY:
- Eye goes to: [The ONE thing - usually the text]
- Supports that: [Visual element that reinforces the message]
- Must not compete: [What to explicitly exclude]

COMPOSITION:
- Text placement: [top/center/bottom + positioning notes]
- Negative space: [where and why]
- Frame: [what's included, what's cropped]

VISUAL STORY:
- Metaphor state: [Where the metaphor is in its progression]
- Character: [What the secondary character is doing/feeling]

STYLE: Manga illustration, high contrast linework
TEXT TO INCLUDE: "[Full slide copy]"
TEXT DELIVERY: [Speech bubble if someone speaking, OR bold text overlay]
ASPECT: 4:5
```

---

## Text Delivery Options

### Speech Bubble (When Someone Is Talking)
Use when the slide has a narrator, character, or "voice" speaking.

```
TEXT DELIVERY: Speech bubble positioned in [location] to not obscure [key element].
The bubble contains the text: "[Full copy]"
Clean, bold, easy-to-read manga font.
```

### Bold Text Overlay (Informational)
Use when it's a statement, not someone speaking.

```
TEXT DELIVERY: Bold text [position], high contrast against background.
Text reads: "[Full copy]"
```

### Minimal/Impact Text
Use for punchy turn slides (10-30 chars).

```
TEXT DELIVERY: Large, centered, maximum impact.
Text reads: "[Short punchy copy]"
No decoration, let it breathe.
```

---

## Integrating Visual Metaphor

Pull the metaphor state from your Visual Progression Table:

```
VISUAL STORY:
- Metaphor: Bonsai tree
- State: Overgrown and chaotic, scissors visible but not yet cutting
- Progression: This is slide 2 of 8 - problem is visible but solution not yet started
```

The metaphor should tell its own story across slides. Each prompt describes WHERE the metaphor is in its journey.

---

## Integrating Secondary Character

Pull the character action from your Visual Progression Table:

```
VISUAL STORY:
- Character: Black kitten
- Action: Watching with wide curious eyes, tail twitching
- Position: Lower right corner, small, not competing with text
- Emotional state: Intrigued but uncertain
```

The character amplifies the emotion. They don't speak - they react.

---

## Slide-Specific Templates

### Hook Slide (Slide 1)

```
PURPOSE: Instagram carousel hook (slide 1 of 8). Stop the scroll and create an open loop.

HIERARCHY:
- Eye goes to: The hook text
- Supports that: [Metaphor in start state - chaos/problem visible]
- Must not compete: Clean background, no secondary text

COMPOSITION:
- Text: Upper portion, impossible to miss
- Negative space: Breathing room around text
- Character: [Initial reaction - curious, alert, or concerned]

VISUAL STORY:
- Metaphor state: [Start state from table]
- Character: [Initial reaction from table]

STYLE: Manga illustration, high contrast, energy lines for impact
TEXT TO INCLUDE: "[Hook copy - 80-120 chars]"
TEXT DELIVERY: [Speech bubble if narrator, bold overlay if statement]
ASPECT: 4:5
```

### Turn Slide (Slide 2)

```
PURPOSE: Instagram carousel turn (slide 2 of 8). Punchy pivot that sets up the value.

HIERARCHY:
- Eye goes to: The short punchy statement
- Supports that: [Metaphor beginning to shift]
- Must not compete: Keep minimal - let statement land

COMPOSITION:
- Text: Centered, bold, maximum breathing room
- Negative space: Generous - this slide needs to hit hard

VISUAL STORY:
- Metaphor state: [First hint of change]
- Character: [Noticing something]

STYLE: Manga, same visual language as slide 1
TEXT TO INCLUDE: "[Turn copy - 10-30 chars]"
TEXT DELIVERY: Large centered text, maximum impact
ASPECT: 4:5
```

### Value Slides (Slides 3-6)

```
PURPOSE: Instagram value slide (slide [N] of 8). Deliver real teaching - this is where value lives.

HIERARCHY:
- Eye goes to: The teaching point
- Supports that: [Metaphor showing progress]
- Must not compete: One visual focus only

COMPOSITION:
- Text: [Position based on metaphor/visual]
- Visual: Metaphor progressing through transformation
- Character: [Engaged, following along]

VISUAL STORY:
- Metaphor state: [Progress state from table]
- Character: [Engagement state from table]

STYLE: Manga, consistent with carousel
TEXT TO INCLUDE: "[Teaching content - 80-180 chars]"
TEXT DELIVERY: [Speech bubble or overlay based on voice]
ASPECT: 4:5
```

### Pattern/Medicine Slide (Slide 7)

```
PURPOSE: Instagram insight slide (slide 7 of 8). The AHA moment - the pattern that ties it together.

HIERARCHY:
- Eye goes to: The insight statement
- Supports that: [Metaphor at or near resolution]
- Must not compete: Clear visual payoff

COMPOSITION:
- Text: Prominent, this is the climax
- Visual: Metaphor transformed, result visible
- Character: [Aha moment - getting it]

VISUAL STORY:
- Metaphor state: [Resolution or near-resolution]
- Character: [Understanding landing]

STYLE: Manga, high contrast, moment of revelation
TEXT TO INCLUDE: "[Insight - 120-180 chars]"
TEXT DELIVERY: [Speech bubble or bold overlay]
ASPECT: 4:5
```

### CTA Slide (Slide 8)

```
PURPOSE: Instagram CTA slide (slide 8 of 8). Engagement question and follow prompt.

HIERARCHY:
- Eye goes to: The engagement question
- Supports that: [Metaphor in final peaceful state]
- Must not compete: Clean, resolved, inviting

COMPOSITION:
- Text: Clear, centered
- Visual: Metaphor complete, character at peace
- Character: [Satisfied, relaxed, content]

VISUAL STORY:
- Metaphor state: [Final resolved state]
- Character: [At peace after the journey]

STYLE: Manga, calm energy, resolution
TEXT TO INCLUDE: "[Engagement question + CTA - 80-120 chars]"
TEXT DELIVERY: Bold text, clear and inviting
ASPECT: 4:5
```

---

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

---

## Ultra-Minimal Alternative

When the Creative Director format feels heavy, use the condensed version:

```
Manga illustration: [scene with metaphor state]. [Character doing action]. Bold text [position]: "[exact text]". [One constraint]. 4:5.
```

Example:
```
Manga illustration: overgrown bonsai tree with visible chaos. Black kitten watching curiously from corner. Speech bubble upper portion: "I coached 6 business coaches yesterday. Each making $30K+ a month. You'd think they'd be cruising..." Clean background, no competing text. 4:5.
```

---

## Iteration Pattern

When a prompt doesn't work, iterate in passes:

1. **Concept pass** - Is the PURPOSE clear? What is this image FOR?
2. **Hierarchy pass** - Is it obvious what the eye goes to FIRST?
3. **Constraint pass** - Did you specify what must NOT compete?
4. **Story pass** - Does this slide fit the visual journey?

Change ONE variable per iteration. If style is drifting, start a new session.

---

## Technical Notes

- **Aspect ratio:** 4:5 for Instagram (takes up more screen)
- **Text length:** Nano Banana Pro handles longer text well - focus on VALUE not character counts
- **Resolution:** Specify "2K" if needed (uppercase K required)
- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro)
