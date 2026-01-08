# Webfluence - Technical Reference

## What It Does

Provides the Webfluence framework for diagnosing and fixing content-to-conversion pathway problems. Used when someone has traffic but no sales, or when offer docs aren't converting.

## Architecture

```
webfluence/
├── SKILL.md              # Framework definition (layers + diagnostics)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load case studies
- `Glob` - Find related files
- `Grep` - Search for patterns

**No external APIs.** Framework/diagnostic skill.

## Usage

**Trigger phrases:**
- "Why aren't they buying?"
- "Diagnose my funnel"
- "I have traffic but no sales"
- "They're not clicking through to the offer"
- Questions about offer doc usage

**Input:** Description of content-to-conversion problem

**Output:** Diagnosis + specific fix prescription

## The Golden Rule

**Nobody sees the offer doc without seeing content and a warming-up VSL before it.**

```
Content → VSL → Offer Doc
    OR
Workshop/Event → Offer Doc
```

## The Five Layers

| Layer | Purpose | Examples |
|-------|---------|----------|
| CORE | Convert belief to buying | VSL, paid workshop |
| MIDDLE RING | Build authority | YouTube, podcast, email sequences |
| OUTER RING | Drive reach | Short-form, social posts |
| CONNECTORS | Link everything | ManyChat, GPT tools, automations |
| COMPOUNDER | Keep evergreen | YouTube channel as binge machine |

## Scoring (Out of 5)

| Dimension | Question |
|-----------|----------|
| Coverage | Content for cold, warm, and hot? |
| Consistency | Rhythmic showing up? |
| Conversion | Clear CTAs on everything? |
| Connection | Physical links between pieces? |
| Belief Flow | Building belief, not just awareness? |

## Common Diagnostic Patterns

| Pattern | Diagnosis | Fix |
|---------|-----------|-----|
| Sent to offer doc, no sales | Skipping steps | Content → VSL → Offer |
| High opens, low clicks | Missing connectors | CTAs to belief-building content |
| Watched VSL, didn't apply | Insufficient warmup | More touchpoints before VSL |

## The 47-Minute Rule

Research showed buyers consumed ~47 minutes of content before buying. Filter: "Is my web architected to deliver enough time on brand?"

## Testing

**Manual verification:**
1. Present a conversion problem scenario
2. Run through webfluence skill
3. Verify correct layer identified
4. Check fix is specific and actionable
