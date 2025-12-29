# Skills Compliance Fix - Implementation Plan

## The Problem

Claude.ai skill uploads require:
1. **ONE top-level folder** (not multiple skills bundled together)
2. **ONE SKILL.md file** at root of that folder

Your current `package-skills.sh` creates a bundle with 3 folders and 3 SKILL.md files - that's why uploads fail.

**Root cause:** Claude.ai doesn't support bulk skill uploads. Each skill must be uploaded individually as its own ZIP.

---

## The Official Spec (From Anthropic)

### Required Structure
```
skill-name/
├── SKILL.md           # REQUIRED - Entry point
├── scripts/           # Optional - Executable Python/Bash
├── references/        # Optional - Docs loaded into context
├── resources/         # Optional - Templates, data files
└── assets/            # Optional - Binary files, logos
```

### Required YAML Frontmatter
```yaml
---
name: skill-name          # lowercase, hyphens, max 64 chars
description: What it does and when to use it  # max 1024 chars
---
```

### Optional YAML Fields
- `allowed-tools: Read, Glob, Grep` - Restricts which tools the skill can use
- `version: 1.0.0` - Version tracking

### Best Practices
- Keep SKILL.md under 5,000 tokens
- Use progressive disclosure - reference files for detailed content
- All .md files in root are available when skill loads
- Scripts execute without loading into context (only output uses tokens)

---

## Gaps Identified

| Current State | Required State |
|---------------|----------------|
| Bundle packages 3 skills into one ZIP | Each skill needs its own ZIP |
| Skills have only SKILL.md file | Skills need optional folders for future expansion |
| No `version` field in YAML | Should have `version` for tracking |
| Template doesn't match spec structure | Template should include all optional folders |
| New Skill Wizard creates minimal structure | Should create full structure with all folders |

---

## Implementation Plan

### Phase 1: Fix Packaging Script
- [ ] Rename `package-skills.sh` to `package-skill.sh` (singular)
- [ ] Change to accept skill name as argument: `./scripts/package-skill.sh newsletter-coach`
- [ ] Output: `dist/newsletter-coach.zip` (one skill per ZIP)
- [ ] Add `package-all-skills.sh` that creates individual ZIPs for each skill
- [ ] Update instructions to reflect new workflow

### Phase 2: Update Skill Folder Structure
For each existing skill (newsletter-coach, mission-context, new-skill-wizard):
- [ ] Create `scripts/` folder with `.gitkeep`
- [ ] Create `references/` folder with `.gitkeep`
- [ ] Create `resources/` folder with `.gitkeep`
- [ ] Create `assets/` folder with `.gitkeep`
- [ ] Add `version: 1.0.0` to YAML frontmatter

### Phase 3: Update Templates
- [ ] Update `_templates/skill-template/` to include all folders
- [ ] Update SKILL.md template with `version` field
- [ ] Add placeholder files explaining each folder's purpose

### Phase 4: Update New Skill Wizard
- [ ] Update wizard to create all optional folders
- [ ] Include `version: 1.0.0` in generated SKILL.md
- [ ] Update packaging instructions in wizard

### Phase 5: Update Documentation
- [ ] Update `skills/README.md` with new structure requirements
- [ ] Add instructions for Claude.ai upload workflow
- [ ] Document that skills must be uploaded individually

---

## New Folder Structure (After Fix)

```
skills/
├── README.md
├── newsletter-coach/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── .gitkeep
│   ├── references/
│   │   └── .gitkeep
│   ├── resources/
│   │   └── .gitkeep
│   └── assets/
│       └── .gitkeep
├── mission-context/
│   └── (same structure)
└── new-skill-wizard/
    └── (same structure)
```

---

## New Packaging Workflow

**Before (broken):**
```bash
./scripts/package-skills.sh
# Creates one bundle - FAILS on upload
```

**After (compliant):**
```bash
# Package single skill
./scripts/package-skill.sh newsletter-coach
# Creates: dist/newsletter-coach.zip

# Or package all (creates individual ZIPs)
./scripts/package-all-skills.sh
# Creates: dist/newsletter-coach.zip
#          dist/mission-context.zip
#          dist/new-skill-wizard.zip
```

---

## Success Signals

- [ ] Each skill uploads successfully to Claude.ai
- [ ] Skills toggle ON and work correctly
- [ ] New skills created by wizard have correct structure
- [ ] Documentation is clear and accurate

---

## Kill Rules

- If Claude.ai changes their upload spec again, reassess
- If this adds too much friction to skill creation, simplify

---

## Sources

- [Anthropic Skills GitHub](https://github.com/anthropics/skills)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [Claude Cookbooks - Skills Development](https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb)
