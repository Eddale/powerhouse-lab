# Reflect - Technical Reference

## What It Does

Captures session learnings and proposes updates to skill files. Turns corrections and discoveries during conversations into persistent improvements. Bridges the gap between "Claude makes a mistake" and "that mistake never happens again."

## Architecture

```
reflect/
├── SKILL.md              # Main skill definition (process + examples)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load skill files for updates
- `Write` - Create new sections
- `Edit` - Modify existing skills
- `Glob` - Find relevant skills
- `Grep` - Search for patterns
- `Bash` - Git commits

**No external APIs.** Conversation analysis + file editing.

## Usage

**Trigger phrases:**
- "/reflect"
- "Reflect on this session"
- "What did we learn"
- "Update skills from this session"

**Input:** Current conversation context

**Output:** Proposed skill updates with approval workflow

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| HIGH | Explicit correction from user | Propose immediate update |
| MEDIUM | Pattern that worked without explicit approval | Suggest addition |
| LOW | Observation worth noting | Note for later |

## Workflow

1. **Scan** - Find corrections, approvals, failed attempts, new patterns
2. **Classify** - Assign confidence level to each finding
3. **Match** - Identify relevant skill file
4. **Propose** - Show old → new change
5. **Approve** - User confirms or modifies
6. **Commit** - Edit file, git commit with `reflect:` prefix

## Output Format

```markdown
## Session Learnings

### HIGH Confidence (Propose Immediate Update)
- [Finding] → Update skill: [name]
  Proposed change: [specific edit]

### MEDIUM Confidence (Consider Adding)
- [Finding] → Could update: [name]

### LOW Confidence (Note for Later)
- [Observation]

Approve changes? [Yes / Modify / Skip]
```

## Commit Convention

All reflect commits use prefix: `reflect: [summary of learning]`

## Testing

**Manual verification:**
1. Have a conversation with corrections
2. Run "/reflect"
3. Verify corrections identified
4. Check confidence levels appropriate
5. Approve and verify skill file updated

**Quality checks:**
- [ ] Only HIGH confidence auto-proposes
- [ ] Shows old → new for changes
- [ ] Correct skill file identified
- [ ] Git commit created with prefix
