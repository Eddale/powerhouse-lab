# Offer Diamond Review - Technical Reference

## What It Does

Evaluates Offer Diamonds for BlackBelt coaches. Reviews five points (Promise, Guarantee, Bonuses, Payment Plan, Urgency/Scarcity) and produces Facebook-ready feedback comments in Ed Dale's voice.

## Architecture

```
offer-diamond-review/
├── SKILL.md              # Main skill definition (evaluation criteria + voice)
├── resources/            # Training materials for calibration
│   ├── Original-Offer-Diamond-Training.md
│   ├── Original-Transcript-Offer-Diamond-Training.md
│   ├── Offer-Diamond-Workbook.pdf
│   ├── LaunchPad-Offer-Diamond-Summary.md
│   └── instructions-source.md
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

## Usage

**Trigger phrases:**
- "Review this Offer Diamond"
- "Give me feedback on this offer"
- "Help me improve my diamond"

**Input:** Screenshot of filled Offer Diamond, optional context

**Output:** Facebook-ready comment (conversational, no headers/bullets)

## The Five Points

| Point | What to Evaluate |
|-------|------------------|
| Promise | Specific outcome, clear timeframe, believable |
| Guarantee | Makes it safe to start, matches promise size |
| Bonuses | Congruent with promise, speed up results |
| Payment Plan | Easy yes, aligned with ROI speed |
| Urgency/Scarcity | Real and operationally true, no fake pressure |

## Output Constraints

- Written in Ed Dale's voice
- No em dashes (commas or periods instead)
- No headers, bullets, or numbered lists
- 2-5 sharp improvements maximum
- Immediately postable in Facebook
- Wrap in code block for copy/paste

## Saved Review Format

```
Filename: Offer Diamond Review - [Client] - YYYY-MM-DD.md
Location: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/
```

## Testing

**Manual verification:**
1. Upload an Offer Diamond screenshot
2. Run "review this offer diamond"
3. Verify all five points evaluated
4. Check output fits Facebook constraints
5. Confirm voice sounds like Ed

**Quality checks:**
- [ ] Five points covered
- [ ] Suggestion language used (not directives)
- [ ] No em dashes or lists
- [ ] Saved to Zettelkasten
- [ ] Daily note updated
