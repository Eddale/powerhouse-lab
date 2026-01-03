---
name: instagram-carousel
description: Turn articles into Instagram carousel concepts with Nano Banana Pro image prompts. Creates carousels that deliver real VALUE, brighten their day, and create AHA moments - not just pretty slides. Triggers on "create a carousel", "turn this into slides", "Instagram carousel from article".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
skills: hook-stack-evaluator, mission-context
---

# Instagram Carousel Skill v2

## What This Does

Transforms newsletter articles (or topics) into Instagram carousels with:
- **Visual storytelling** through metaphor progression
- **Real value delivery** in every slide (not just slogans)
- **Audience-aware engagement** that makes them look smart
- **AHA moments** that brighten their day

**Output package:**
- 6-8 carousel slides with value-rich copy
- Image prompts optimized for Nano Banana Pro
- Instagram caption with status-appropriate engagement
- Hook evaluation via hook-stack-evaluator (auto-iterated if below 10/15)

---

## When to Use

- "Create an Instagram carousel from this article"
- "Turn this into slides"
- "Make a carousel for [topic]"
- "Repurpose this newsletter for Instagram"
- "Generate carousel prompts for..."

---

## The V2 Difference

**Old approach:** Short slogans (25 chars) that looked pretty but delivered nothing.

**New approach:** Value-rich teaching (80-180 chars) with visual storytelling that creates a journey.

The carousel should leave them with an **AHA moment** - real insight they can use.

---

## Phases

### Phase 1: Parse Input + Detect Audience

**If given an article:**
1. Read the full article
2. Identify the core argument/thesis
3. Extract the transformation promised
4. Note what's counterintuitive or surprising
5. Identify the target audience from content

**Audience Detection:**
1. Check mission-context skill for audience info
2. If not found, use AskUserQuestion:
   - "Who is this carousel for? (Role/level)"
   - "Are they established experts or still learning?"
3. Classify audience status:
   - **High-status:** Established experts ($30K+/month, years of experience)
   - **Low-status:** Learning, growing, building

**Main Character Selection:**
1. Ask: "Should the main character be male or female?" (Consider who the audience will most connect with)
2. Ask: "Do you want to appear as the narrator? If yes, you'll need to attach your reference photo to Slide 1."
3. If using reference photo: Note that all subsequent prompts will include "maintain consistent character appearance from reference"

**Why this matters:** High-status audiences won't engage with questions that make them look weak. Low-status audiences want connection through shared struggle. And seeing themselves (or someone like them) in the carousel increases connection.

---

### Phase 2: Extract Core Message

Answer these questions:
1. What's the ONE takeaway?
2. What transformation is promised?
3. What's counterintuitive or surprising?
4. What will make them go "AHA"?

The carousel builds to this AHA moment. Everything serves it.

---

### Phase 3: Develop Hook (3 C's Framework)

The hook must have:
- **Clarity:** What value will they get?
- **Context:** Who/what is this about?
- **Curiosity:** What open loop forces the swipe?

**Process:**
1. Generate 3-5 hook variations
2. Test each against the 3 C's
3. Ensure the winning hook creates an open loop
4. The hook is 80-120 characters (substantial but scannable)

---

### Phase 4: Select Visual Metaphor

**Default: Use a visual metaphor** (unless user requests literal visuals)

**Process:**
1. Deeply consider the article content and target audience
2. Look for angles, tensions, or transformations in the content itself
3. The metaphor should EMERGE from the article's core insight
4. Load `resources/visual-metaphors.md` for inspiration (not a menu to pick from)
5. Define start state → end state that mirrors the article's transformation

**Good metaphors are:**
- Visual (can be drawn as a progression)
- Universal (audience immediately gets it)
- Resonant (feels right for THIS specific message)

**Metaphor Override:** If user requests literal visuals, skip this phase and use direct imagery.

---

### Phase 5: Design Character Arc (Optional)

Load `resources/secondary-characters.md` for options.

**Ed's approved roster:**
- Black kitten (curious → peaceful)
- Shetland sheepdog (alert → satisfied)
- Kangaroo (energetic → relaxed)
- Quokka (cheerful throughout - amplifies emotion)
- Kookaburra (watching wisely → laughs at resolution)
- Koala (grumpy despite cute looks → won over and happy)

**Process:**
1. Select character that fits the tone
2. Plan character reactions across slides
3. Character amplifies emotional journey - they don't speak, they react

**Skip character when:** Content is very serious, metaphor is strong enough alone, or user requests no character.

---

### Phase 6: Write Slide Script (6-8 slides)

Load `resources/carousel-formats.md` for structure options.

**Character count targets:**
| Slide Type | Chars | Purpose |
|------------|-------|---------|
| Hook | 80-120 | Stop scroll, create open loop |
| Turn | 10-30 | Punchy pivot, sets up value |
| Value (body) | 80-180 | DELIVER TEACHING - this is where value lives |
| Pattern/Medicine | 120-180 | The AHA - the insight that ties it together |
| CTA | 80-120 | Engagement question + follow prompt |

**Value slides must TEACH something.** Not "Old advice kills" (slogan) but "The advice we got 10 years ago assumed clients would find us. Now they research for 8 months before reaching out." (teaching)

**Engagement question (final slide):**
- **High-status audience:** Invite expertise demonstration ("What did you STOP that made things click?")
- **Low-status audience:** Invite connection ("Who else feels this?")

Apply the **Golden Test:** Would commenting make them look SMARTER or WEAKER to peers/clients?

---

### Phase 7: Create Visual Progression Table

**Required format:**

| Slide | Text Summary | Metaphor State | Character Action | Energy |
|-------|--------------|----------------|------------------|--------|
| 1 | [Hook] | [Start state] | [Initial reaction] | High |
| 2 | [Turn] | [First shift] | [Noticing] | Medium-High |
| 3 | [Value 1] | [Progress visible] | [Engaging] | Medium |
| ... | ... | ... | ... | ... |
| 7 | [Pattern] | [Resolution revealed] | [AHA moment] | Peak |
| 8 | [CTA] | [Final peaceful state] | [Satisfied] | Calm |

**Why this matters:** Without this table, each slide is nice on its own but there's no JOURNEY. The table forces you to plan the arc.

**Validate:**
- Does the metaphor reach resolution?
- Does the character arc complete?
- Is there a satisfying visual journey?

---

### Phase 8: Generate Image Prompts

Load `resources/prompt-templates.md` for the Creative Director Framework.

**For EACH slide, generate a prompt using:**

**SLIDE 1 ONLY - Reference Image Reminder:**
```
=== REFERENCE IMAGE REQUIRED ===
[ATTACH: Your reference photo here before generating]
This image will be used to maintain consistent character appearance.
================================
```

**All prompts use this structure:**

```
PURPOSE: Instagram carousel slide [N of 8]. [What viewer must understand]

HIERARCHY:
- Eye goes to: [The ONE thing]
- Supports that: [Metaphor state from table]
- Must not compete: [What to exclude]

COMPOSITION:
- Text placement: [Position]
- Negative space: [Where and why]
- Character: [Action from table]

VISUAL STORY:
- Metaphor state: [From progression table]
- Character: [From progression table]

STYLE: Manga illustration, high contrast linework
CHARACTER CONSISTENCY: Maintain consistent character appearance from reference image
TEXT TO INCLUDE: "[Full slide copy]"
TEXT DELIVERY: [Speech bubble if talking, bold overlay if statement]
ASPECT: 4:5
```

**Note:** The "CHARACTER CONSISTENCY" line ensures the main character looks the same across all slides when using a reference photo.

**Text delivery options:**
- **Speech bubble:** When there's a narrator or voice speaking
- **Bold overlay:** When it's a statement or teaching point
- **Minimal/impact:** For punchy turn slides

---

### Phase 9: Evaluate Hook

Run slide 1's text through hook-stack-evaluator.

**Provide:**
- The hook text
- Target audience (from Phase 1)
- Context: "Instagram carousel for [audience type]"

**If score is below 10/15:** Auto-iterate. Generate 3 new variations, evaluate, select the best, and update the slide.

---

### Phase 10: Write Instagram Caption

**Structure:**
```
[Hook line - expand or riff on Slide 1]

[Body - 3-5 bullets summarizing the value]
→ Point 1
→ Point 2
→ Point 3

[Insight - the "so what"]

[Engagement question - mirrors Slide 8]

Save this for when you need it.
Follow @[handle] for more.

👇

[Hashtags - 5-10 relevant tags]
```

**Rules:**
- First line must hook (it's the preview)
- Use → arrows for easy scanning
- Engagement question matches audience status
- Hashtags at the end, not inline

---

### Phase 11: Output with Code Blocks

Present the complete carousel with **code blocks for easy copy/paste**:

```markdown
# CAROUSEL: [Title]

**Audience:** [Who this is for]
**Metaphor:** [Visual metaphor used]
**Character:** [Secondary character if used]

---

## Visual Progression Table

| Slide | Text Summary | Metaphor State | Character Action | Energy |
|-------|--------------|----------------|------------------|--------|
[Full table from Phase 7]

---

## SLIDE 1/8 (Hook)
**Text:** [slide copy] _(XX chars)_

**Prompt:**
\`\`\`
[full image prompt - inside code block for one-click copy]
\`\`\`

---

## SLIDE 2/8 (Turn)
**Text:** [slide copy] _(XX chars)_

**Prompt:**
\`\`\`
[full image prompt]
\`\`\`

[...continue for all slides...]

---

## INSTAGRAM CAPTION

\`\`\`
[full caption with hashtags - inside code block for one-click copy]
\`\`\`

---

## HOOK EVALUATION
**Score:** [X]/15
[feedback from hook-stack-evaluator]
[note if auto-iterated]
```

**Why code blocks matter:** Ed copies prompts directly into Google AI Studio. Code blocks = one click to copy the whole prompt.

---

### Phase 12: Save to Zettelkasten

Save the complete carousel output as a markdown file.

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
audience: [target audience]
metaphor: [visual metaphor used]
character: [secondary character if used]
hook_score: [X/15]
status: draft
tags: [instagram, carousel, nano-banana-pro]
---

# Carousel: [Title]

[Full carousel output from Phase 11]
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

---

## Quick Reference

### Slide Count Decision
- Can deliver AHA in 6 slides? → 6 slides
- Need more room for value? → 8 slides
- More than 4 teaching points? → Consider splitting into two carousels

### Audience Status Cheat Sheet
| Audience | Engagement Style | Example Question |
|----------|------------------|------------------|
| High-status | Expertise invitation | "What did you stop that made things click?" |
| Low-status | Connection invitation | "Who else feels this?" |

### Character Count Cheat Sheet
| Slide Type | Target | Min | Max |
|------------|--------|-----|-----|
| Hook | 100 | 80 | 120 |
| Turn | 20 | 10 | 30 |
| Value | 130 | 80 | 180 |
| Pattern | 150 | 120 | 180 |
| CTA | 100 | 80 | 120 |

---

## Future: API Automation Notes

When building an API version of this skill:
- **Reference image handling:** Need to solve programmatic upload of reference photo for character consistency
- **Multi-image generation:** Batch generate all 8 slides with consistent character
- **Character consistency token:** Explore Nano Banana Pro's approach to maintaining character across generations

---

## Version History

- v2.1 (2026-01-04): Added main character selection (male/female based on audience), reference image workflow with visual reminder, character consistency instructions
- v2.0 (2026-01-04): Major upgrade - visual metaphor system, character arcs, audience status detection, value-focused copy (80-180 chars), 6-8 slide structure, auto-iterate hooks
- v1.3 (2026-01-03): Code blocks around prompts and caption for one-click copy workflow
- v1.2 (2026-01-03): Added 25-char text limit enforcement, character counts in output
- v1.1 (2026-01-03): Added Phase 7 - auto-save to Zettelkasten
- v1.0 (2026-01-03): Initial release with Creative Director Framework
