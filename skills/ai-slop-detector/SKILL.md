---
name: ai-slop-detector
description: Detects and removes AI writing patterns from text. Use when polishing drafts, cleaning AI-generated content, or ensuring writing sounds authentically human. Invoke with "run through slop detector", "clean this up", or "remove AI fingerprints".
allowed-tools: Read, Write, Edit
---

# AI Slop Detector

## What This Does
Takes any text and rewrites it to remove common AI writing patterns, making it sound authentically human. Returns only the cleaned final version.

## When to Use
- After generating any AI-assisted content
- Before publishing newsletters, articles, or social posts
- When text feels "too polished" or generic
- As a final quality gate in any writing workflow

## Instructions

When given text to clean:

1. **Analyze** the text against the detection patterns below
2. **Rewrite** to eliminate AI fingerprints while preserving meaning
3. **Return only the final cleaned version** (no before/after comparison needed)

---

## LANGUAGE AND TONE PATTERNS TO ELIMINATE

### Promotional/Puffery Phrases
Remove these entirely or replace with specific facts:
- "stands as / serves as / is a testament"
- "plays a vital/significant role"
- "continues to captivate"
- "leaves a lasting impact"
- "rich cultural heritage/tapestry"
- "nestled in the heart of"
- "breathtaking," "must-visit," "stunning natural beauty"
- "enduring/lasting legacy"

**Fix:** Use specific, factual descriptions
- BAD: "The museum stands as a testament to the city's rich cultural heritage"
- GOOD: "The museum houses 3,000 artifacts spanning four centuries of local history"

### Editorializing Phrases
Remove these - present facts directly:
- "it's important to note/remember/consider"
- "it is worth noting"
- "no discussion would be complete without"
- "this article wouldn't exist without"

**Fix:** Just state the thing
- BAD: "It's important to note that the company expanded rapidly"
- GOOD: "The company opened 15 new locations between 2020-2023"

### Overused Conjunctions
Replace excessive use of:
- "moreover," "furthermore," "in addition," "on the other hand"

**Fix:** Use varied, natural transitions or combine sentences
- BAD: "Moreover, the company expanded. Furthermore, it hired new staff."
- GOOD: "The company expanded while hiring additional staff and opening three regional offices."

### Section Summaries
Never end paragraphs with "In summary," "In conclusion," "Overall" followed by a restatement.

**Fix:** End with the most important or forward-looking information
- BAD: "In summary, the research shows climate change affects migration patterns"
- GOOD: "These migration shifts may accelerate as temperatures continue rising"

---

## STYLE AND FORMATTING PATTERNS

### Title Case in Headings
Use sentence case instead:
- BAD: "Early Life and Educational Background"
- GOOD: "Early life and education"

### Excessive Boldface
Use bold sparingly - only for true emphasis or introducing technical terms for the first time.

### Formulaic Lists
Write in flowing paragraphs instead of numbered/bulleted lists:
- BAD: "The benefits include: 1. Cost savings 2. Efficiency gains 3. Better outcomes"
- GOOD: "The program reduces costs by 15%, improves processing speed, and enhances patient satisfaction scores"

### Em-dash Overuse
Replace with varied punctuation (commas, parentheses, colons, or sentence breaks):
- BAD: "The solution is elegant — simple, effective, and affordable — exactly what we need"
- GOOD: "The solution combines simplicity with effectiveness at an affordable price point"

---

## ANALYTICAL WRITING PATTERNS

### Superficial Analysis with -ing Phrases
Don't attach vague analytical comments using present participles:
- BAD: "The study found a 20% increase, highlighting the importance of early intervention"
- GOOD: "The study found a 20% increase in recovery rates when treatment began within 48 hours"

### Vague Attributions
Never use weasel words without specific sources:
- BAD: "Industry experts believe the trend will continue"
- GOOD: "Tesla's Q3 report projects 25% growth in the electric vehicle sector"

### False Ranges
Don't use "from...to..." when not describing actual ranges:
- BAD: "The menu features dishes from pasta to grilled meats"
- GOOD: "The menu includes pasta dishes, grilled meats, and seasonal vegetables"

---

## DIRECT CONTRAST FORMULATIONS - ELIMINATE ON SIGHT

These patterns scream AI:
- "This isn't about X—it's about Y"
- "It's not X, it's Y"
- "The problem isn't X—it's Y"
- "Rather than X, focus on Y"
- "Instead of X, consider Y"
- Any sentence with "but rather" construction

**Fix:** Replace with direct positive assertions
- BAD: "Success isn't about working harder but working smarter."
- GOOD: "Success comes from working smarter and more strategically."

**Exception:** Contrast is acceptable ONLY if spaced out with substantial content between negative and positive (2-3+ sentences of expansion).

---

## WORD SUBSTITUTIONS

| AVOID | USE INSTEAD |
|-------|-------------|
| "leverages" | "uses" |
| "encompasses" | "includes" |
| "facilitates" | "enables" or "allows" |
| "utilized" | "used" |
| "commenced" | "began" or "started" |
| "subsequent to" | "after" |
| "prior to" | "before" |
| "in order to" | "to" |
| "serves to" | "helps" or omit entirely |

---

## STRUCTURAL PATTERNS

### Essay-like Organization
Don't structure content like a five-paragraph essay with thesis statements and conclusions. Use inverted pyramid (important info first) or natural flow.

### Rule-of-Three Overuse
Don't constantly group things in threes:
- BAD: "The platform is fast, reliable, and secure"
- GOOD: "The platform processes requests in under 200ms with 99.9% uptime and bank-level encryption"

### Knowledge Disclaimers
Never include "as of [date]," "based on available information," "while specific details are limited."

### Chatbot Hedging
Don't use excessive qualifying language:
- BAD: "The data appears to suggest that users tend to prefer the new interface"
- GOOD: "Users prefer the new interface by a 3:1 margin in testing"

---

## VERIFICATION CHECKLIST

Before returning cleaned text, verify:
1. No section ends with a summary statement
2. No "challenges and future prospects" formulaic sections
3. No excessive em-dashes or repeated punctuation patterns
4. No title case in headings
5. No promotional language about "rich heritage" or "cultural significance"
6. No vague attributions without specific sources
7. Varied sentence structures and lengths
8. Specific facts and figures rather than general statements
9. Natural flow between paragraphs without formulaic transitions
10. No direct contrast formulations ("This isn't X—it's Y")

---

## Output Format

Return only the cleaned text. No preamble, no explanation of changes, no "Here's the cleaned version:" - just the polished content ready to use.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial creation from Write with AI prompt |
