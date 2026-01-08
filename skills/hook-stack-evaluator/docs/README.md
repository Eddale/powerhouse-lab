# Hook Stack Evaluator - Technical Reference

## What It Does

Evaluates any content hook (headline, opening line, video intro, carousel opener) against The Hook Stack™ 5-layer framework. Provides scoring, feedback, and refinement suggestions. Operates in automatic mode (pipeline) or interactive mode (sparring session).

## Architecture

```
hook-stack-evaluator/
├── SKILL.md              # Main skill definition (framework + scoring)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/            # Improvement plans
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load existing hooks from files
- `Write` - Save scored hooks
- `Edit` - Refine hooks in place

**No external APIs or scripts.** Pure evaluation and refinement skill.

## Usage

**Trigger phrases:**
- "Evaluate this hook"
- "Run through hook stack"
- "Score my headline"
- "Rate this opening"
- "Help me sharpen this hook"

**Input:** Any hook text (headline, opening, video intro)

**Output:** Hook Scorecard™ with layer-by-layer scores (X/15) plus actionable feedback

## The Hook Stack™ Framework

| Layer | Name | Key Question |
|-------|------|--------------|
| 1 | Earn the Stop | Would YOU stop scrolling for this? |
| 2 | Start at the End | Is there a clear payoff to stick around for? |
| 3 | The Three C's | Does it have Clarity, Context, and Curiosity? |
| 4 | Speak Their Lingo | Is it specific? Their words, not coach-speak? |
| 5 | Make It Yours | Could anyone else have written this? |

**Rating scale:** 1 (Weak) / 2 (OK) / 3 (Strong)

**Threshold:** < 12/15 needs work, >= 12/15 is ready

## Mode Detection

| Mode | Triggers | Behavior |
|------|----------|----------|
| Automatic | "automatic", pipeline calls, batch processing | Skip questions, deliver scorecard, auto-improve if weak |
| Interactive | Direct user request, "help me with" | Ask questions, deliver scorecard, "Keep/Tweak/Trash?" |

**Default:** Interactive for direct requests, Automatic for agent invocations.

## Scorecard Format

```
THE HOOK SCORECARD™

Your Hook: "[hook text]"

1. Earn the Stop: X / 3
2. Start at the End: X / 3
3. The Three C's: X / 3
4. Speak Their Lingo: X / 3
5. Make It Yours: X / 3

Total Score: X / 15
```

## Testing

**Manual verification:**
1. Run "evaluate this hook" with test headline
2. Verify all 5 layers scored
3. Check feedback is specific and actionable
4. Test automatic mode with "automatically score this hook"
5. Verify no questions asked in automatic mode

**Quality checks:**
- [ ] All 5 layers evaluated
- [ ] Scores match 1/2/3 rating guide
- [ ] Feedback references framework concepts by name
- [ ] Interactive mode asks Keep/Tweak/Trash
- [ ] Automatic mode generates alternatives if score < 12

## Known Limitations

- Audience context required for accurate Layer 4 (Speak Their Lingo) scoring
- Subjective scoring - different evaluators may score differently
- No persistent storage of scored hooks
- Can't evaluate visual elements of video hooks
