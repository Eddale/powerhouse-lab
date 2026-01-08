# Magic Model Review - Technical Reference

## What It Does

Evaluates Magic Model (Triangle) frameworks for BlackBelt and Million Dollar Coach members. Produces Facebook-ready feedback comments in Ed Dale's voice. Reviews five elements: Yellow, Reds, Greens, Blues, and Symmetry.

## Architecture

```
magic-model-review/
├── SKILL.md              # Main skill definition (evaluation criteria + voice)
├── resources/            # Training materials for calibration
│   ├── Designing Your Hero Product.txt
│   ├── Triangle ACD.txt
│   ├── Yellows.txt
│   ├── Greens.txt
│   ├── Reds.txt
│   ├── Blues.txt
│   └── Test Your Triangle.txt
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load reference materials from resources/
- `Write` - Save reviews to Zettelkasten
- `Edit` - Update daily notes
- `Glob` - Find resource files
- `Grep` - Search reference materials

**Related skills:**
- `ai-slop-detector` - Cleans output before delivery

**No external APIs.** Evaluation skill with reference materials.

## Usage

**Trigger phrases:**
- "Review this Magic Model"
- "Review this Triangle"
- "Give me feedback on this framework"
- "Help me improve my triangle"

**Input:** Screenshot or image of filled Magic Model, optional context

**Output:** Facebook-ready comment (8,000 char max, minimal line breaks)

## The Five Elements

| Element | Color | What to Evaluate |
|---------|-------|------------------|
| Yellow | Goal/Result | Clear, concrete, sized correctly, emotionally desirable |
| Reds | Problems | Prospect's words, symptoms not causes, non-judgmental |
| Greens | Milestones | Outcomes not areas, feel like destinations, advance to Yellow |
| Blues | Projects | Named as results, minimal and sufficient, 2-3 per Green |
| Symmetry | Balance | Same Blues per Green, similar word counts, elegant |

## Output Constraints

- **8,000 character limit** (Facebook)
- **100 line breaks limit** (whichever hits first)
- Flowing paragraphs, no bullets/headers
- Ed's voice: short sentences, compassionate, calm authority
- No em dashes, no lecturing, no comparisons

## Saved Review Format

```
Filename: Magic Model Review - [Client] - YYYY-MM-DD.md
Location: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/
```

With YAML frontmatter (type, client, program, date, elements-reviewed).

## Testing

**Manual verification:**
1. Upload a Magic Model screenshot
2. Run "review this Magic Model"
3. Verify feedback covers all five elements
4. Check character count < 8,000
5. Verify no bullets, headers, or em dashes
6. Confirm voice sounds like Ed, not AI

**Quality checks:**
- [ ] All five elements evaluated
- [ ] Suggestion language used (not "you should")
- [ ] Flows as conversational prose
- [ ] Under character/line limits
- [ ] Saved to Zettelkasten
- [ ] Daily note updated

## Known Limitations

- Requires readable screenshot (OCR quality matters)
- No memory of previous reviews for same client
- Can't see actual client programs to verify accuracy
- Manual copy/paste to Facebook required
