# New Skill Wizard - Technical Reference

## What It Does

Creates new skills in the Powerhouse Lab library with complete folder structure, git workflow, documentation, and Claude Code registration. Handles everything from branch creation to final merge.

## Architecture

```
new-skill-wizard/
├── SKILL.md              # Main skill definition (process + templates)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Check existing skills
- `Write` - Create skill files
- `Bash` - Git operations, folder creation, symlinks
- `Glob` - Find files
- `Grep` - Search content

**No external APIs.** Git + filesystem operations.

## Usage

**Trigger phrases:**
- "Create a new skill"
- "I want to make a skill for..."
- "New skill called..."
- "Add a skill"
- "Build a skill"

**Input:** Skill name, description, trigger phrases

**Output:** Complete skill folder with SKILL.md, docs/, and all wiring

## The 9-Step Process

1. **Get basics** - Name, description, triggers
2. **Set up git** - Branch from main
3. **Create files** - Folder structure, SKILL.md, docs/
4. **Wire it up** - Symlinks + settings.local.json registration
5. **Develop content** - Build instructions together
6. **Create testing plan** - Pre-flight + invocation tests
7. **Execute tests** - User runs, reports back
8. **Publish** - Merge to main
9. **Claude.ai upload** - Package ZIP if requested

## Folder Structure Created

```
skills/<name>/
├── SKILL.md
├── docs/
│   ├── README.md
│   ├── GUIDE.md
│   ├── ROADMAP.md
│   └── plans/archive/
├── scripts/
├── references/
├── resources/
└── assets/
```

## YAML Frontmatter Rules

| Field | Required | Notes |
|-------|----------|-------|
| name | Yes | kebab-case |
| description | Yes | What + when (max 1024 chars) |
| allowed-tools | No | Tools only, not other skills |
| model | No | Specific model if needed |

## Critical Wiring Step

**Settings registration is required:**
```
"Skill(<name>)" in .claude/settings.local.json
```

Symlinks make skills visible. Registration makes them usable.

## Testing

**Pre-flight checks:**
- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started

**Verification:**
1. Run skill trigger phrase
2. Verify skill activates
3. Test full workflow
