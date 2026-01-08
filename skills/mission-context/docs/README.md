# Mission Context - Technical Reference

## What It Does

Provides comprehensive context about Ed Dale, his mission, terminology, business, and technical environment. Loaded by other skills and agents to ensure consistent understanding and voice across all outputs.

## Architecture

```
mission-context/
├── SKILL.md              # Main context document (who Ed is, mission, tech stack)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load context files
- `Glob` - Find related files
- `Grep` - Search context
- `WebSearch` - Research related topics
- `WebFetch` - Pull external references
- `Write` - Update context when requested
- `Edit` - Modify specific sections

**No external APIs.** Pure context/reference skill.

## Usage

**When to activate:**
- Working on any Ed project
- Writing content in Ed's voice
- Building tools for the coaching business
- Creating materials for clients
- Discussing strategy or positioning

**How skills/agents use it:**
- Load via `skills: mission-context` in agent frontmatter
- Reference terminology for consistent language
- Use translation layer for tech communication

## Key Context Areas

| Section | What It Contains |
|---------|------------------|
| Who Ed Is | Background, company, superpowers |
| The Mission | Prime directive, Triangle Model |
| Terminology | Ed's specific terms and meanings |
| Translation Layer | Tech → Copywriter speak |
| Iron Rules | Non-negotiables for building |
| Tech Stack | Hardware, software, platforms |
| Skill Architecture | Three-layer pattern |
| Current Focus | Active projects and priorities |

## The Prime Directive

> "First AI win in 30 days. Then compound."

Every decision filters through this. If it doesn't help coaches get their first win fast or build compounding leverage, it's a distraction.

## The Triangle Model

- **Red (Problems):** Moving too slow, tech nightmares, AI toys without lift
- **Green (Milestones):** Opportunities mapped, Assets live, Engine amplifying
- **Blue (Projects):** Specific deliverables for each milestone

## Runtime Differences

Skills must account for which Claude runtime executes them:

| Capability | Claude Code (CLI) | Claude.ai (Mac/Web) |
|------------|-------------------|---------------------|
| Filesystem | Full access | Sandboxed |
| External APIs | Yes | Blocked |
| Bash/Python | Yes | No |
| Best for | Automation | Conversation |

## Updating Context

Ed can update by saying:
- "Update my mission context to include..."
- "Add this to my terminology..."
- "Change my current focus to..."

Edit SKILL.md directly when requested.

## Testing

**Manual verification:**
1. Load mission-context in a fresh conversation
2. Ask about Ed's terminology
3. Verify correct definitions returned
4. Test translation layer accuracy
5. Check tech stack is current

**Quality checks:**
- [ ] Terminology matches CLAUDE.md
- [ ] Tech stack reflects current setup
- [ ] Triangle Model complete and accurate
- [ ] Prime directive prominent

## Known Limitations

- Single source (no backup verification)
- Manual updates required when things change
- Large file - loads significant context
- No version tracking of changes
