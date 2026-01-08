# AI Slop Detector - Technical Reference

## What It Does

Takes any text and rewrites it to remove common AI writing patterns, making it sound authentically human. Returns only the cleaned final version - no before/after comparisons.

## Architecture

```
ai-slop-detector/
├── SKILL.md              # Main skill definition (pattern lists + instructions)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/            # Improvement plans
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load text from files if needed
- `Write` - Save cleaned output to files
- `Edit` - Modify text in place

**No external APIs or scripts.** Pure pattern-matching and rewriting skill.

## Usage

**Trigger phrases:**
- "Run through slop detector"
- "Clean this up"
- "Remove AI fingerprints"
- "Make this sound more human"

**Input:** Any AI-generated or AI-assisted text

**Output:** Cleaned text with AI patterns removed - returned directly, no preamble

## Detection Categories

| Category | What It Catches |
|----------|-----------------|
| Promotional/Puffery | "testament to", "rich heritage", "breathtaking" |
| Editorializing | "it's important to note", "no discussion would be complete" |
| Overused transitions | "moreover", "furthermore", "in addition" |
| Direct contrasts | "This isn't X—it's Y" patterns |
| Corporate speak | "leverages", "facilitates", "utilized" |
| Structural patterns | Essay format, rule-of-three, excessive em-dashes |

## Testing

**Manual verification:**
1. Take any AI-generated text
2. Run "clean this up" with the text
3. Compare output against the 10-point verification checklist in SKILL.md
4. Verify no preamble or explanation in output

**Quality checks:**
- [ ] No section ends with summary statement
- [ ] No title case in headings
- [ ] No promotional language
- [ ] No direct contrast formulations
- [ ] Natural sentence variety

## Known Limitations

- Pattern-based, not contextual - may miss novel AI patterns
- No learning from user feedback
- Single-pass rewrite (no iterative refinement)
- Can't detect AI in code, only prose

## Related Skills

- `newsletter-coach` - Uses slop detector before final output
- `hook-stack-evaluator` - Complementary quality check for headlines
