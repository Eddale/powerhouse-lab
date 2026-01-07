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
- `license` - License for the skill
- `compatibility` - Compatibility requirements
- `metadata` - Additional metadata

**Note:** `version` is NOT a valid frontmatter field. Track versions in a Version History table in the body instead.

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
| Version tracked in frontmatter | Version should be in body table, not frontmatter |
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
- [x] Remove `version` from YAML frontmatter (not a valid field)

### Phase 3: Update Templates
- [ ] Update `_templates/skill-template/` to include all folders
- [x] Confirmed SKILL.md template does NOT include `version` field (correct)
- [ ] Add placeholder files explaining each folder's purpose

### Phase 4: Update New Skill Wizard
- [ ] Update wizard to create all optional folders
- [x] Confirmed wizard does NOT include `version` in generated SKILL.md (correct)
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

## Verification Plan

### What We Can Verify Here (In This Environment)

After implementation, I'll run these checks:

- [ ] **ZIP Structure Check** - Unzip each file and confirm:
  - Exactly ONE top-level folder
  - SKILL.md exists at root of that folder
  - All optional folders present (scripts/, references/, resources/, assets/)

- [ ] **YAML Validation** - Confirm frontmatter has:
  - `name` field (lowercase, hyphens)
  - `description` field (under 1024 chars)
  - `allowed-tools` field (existing)
  - NO `version` field (invalid - causes upload errors)

- [ ] **Script Tests** - Run packaging scripts and confirm:
  - `package-skill.sh <name>` creates correct individual ZIP
  - `package-all-skills.sh` creates all individual ZIPs
  - No errors during execution

- [ ] **Template Check** - Verify updated template has all folders

### What YOU Need to Verify (On Claude.ai)

After I push the changes to GitHub:

1. **Pull the branch** to your local machine
2. **Run** `./scripts/package-all-skills.sh`
3. **Upload each ZIP** to Claude.ai → Settings → Features
4. **Confirm** no error messages on upload
5. **Toggle ON** each skill
6. **Test** each skill triggers correctly with a prompt

I'll provide exact test prompts for each skill when we get there.

---

## Success Signals

- [ ] ZIP structure passes all checks here
- [ ] Each skill uploads successfully to Claude.ai (you verify)
- [ ] Skills toggle ON and work correctly (you verify)
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

---
---

# Documentation & Autonomous Improvement Pipeline

**Created:** 2026-01-08
**Status:** Planning (awaiting Ed's approval)

## The Vision

Enable Ed to kick off improvement cycles from any Claude interface (web, desktop, CLI) that run completely autonomously through plan → code → test → fix loops.

**Core Principle: GitHub is the Single Source of Truth**

Once a tool exists in GitHub, ALL documentation lives in GitHub:
- Planning docs
- Improvement plans
- Roadmaps
- Technical docs
- Business-friendly guides

**Why:** Web and desktop Claude clients can't reliably access Zettelkasten. GitHub is accessible from everywhere.

**Zettelkasten is for:** Session debriefs, daily captures, research swarm outputs - things that capture the *process*, not the *product*.

---

## Part 1: Documentation Structure

### Pre-Tool (Before GitHub)

Ideas and early brainstorming can live anywhere - Zettelkasten, conversations, notes.

**Transition point:** The moment you create a folder in `skills/`, `prototypes/`, or `.claude/agents/`, all documentation moves to GitHub.

### Post-Tool (In GitHub)

**Every tool gets a `docs/` folder with three core files:**

```
skills/newsletter-coach/
├── SKILL.md              # Required - the skill itself
├── docs/
│   ├── README.md         # Technical reference (for Claude and devs)
│   ├── GUIDE.md          # Business-friendly explanation (vibe coded)
│   ├── ROADMAP.md        # Ideas for future features + shipped history
│   └── plans/            # Improvement plans (current and archived)
│       ├── current.md    # Active improvement being worked on
│       └── archive/      # Completed plans (decision log)
├── scripts/
├── references/
├── resources/
└── assets/
```

**For Prototypes:**
```
prototypes/blackbelt-playbook-generator/
├── README.md             # Technical reference
├── HOW-IT-WORKS.md       # Vibe coded explanation
├── docs/
│   ├── ROADMAP.md        # Future ideas
│   └── plans/
└── src/
```

**For Agents:**
```
.claude/agents/
├── research-swarm.md     # Agent definition
└── docs/
    └── research-swarm/
        ├── README.md
        ├── GUIDE.md
        ├── ROADMAP.md
        └── plans/
```

### Document Templates

**README.md (Technical):**
```markdown
# [Tool Name]

## What It Does
[One paragraph]

## Architecture
[Diagram or explanation]

## Dependencies
[What it needs]

## Usage
[How to invoke]

## Testing
[How to verify it works]
```

**GUIDE.md (Business-Friendly):**
```markdown
# [Tool Name] - How It Works

## The One-Sentence Version
[Like an elevator pitch]

## Why This Exists
[The problem it solves]

## How You Use It
[Step by step, in human terms]

## What It's NOT
[Scope clarity]
```

**ROADMAP.md (Future Ideas):**
```markdown
# [Tool Name] - Roadmap

## Shipped
| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01-08 | Initial release |

## Planned
- [ ] Add X feature - [brief why]
- [ ] Improve Y - [brief why]

## Ideas (Not Committed)
- Maybe add Z for [use case]
- Consider integrating with W

## Decision Log
Link to archived plans in `plans/archive/`
```

**plans/current.md (Active Improvement):**
```markdown
# Improvement Plan - [Tool Name]

**Status:** Draft / Approved / In Progress / Complete
**Created:** YYYY-MM-DD
**Approved:** [date or pending]

## Requested Change
[What Ed asked for]

## Current State Analysis
[What exists now]

## Proposed Changes
1. [Specific change 1]
2. [Specific change 2]

## Files Affected
- path/to/file1.md
- path/to/file2.py

## Testing Strategy
- [ ] Unit tests: [what to test]
- [ ] Integration: [how to verify end-to-end]
- [ ] Browser test: [if UI involved]

## Completion Criteria
[Exact conditions that mean "done"]

## Approval
- [ ] Ed approves this plan

## Execution Log
[Claude adds notes during execution]
```

---

## Part 2: Autonomous Improvement Pipeline

### The Dream Workflow

```
1. Ed triggers improvement (from any Claude interface)
   "Improve newsletter-coach: add word count limit"
   ↓
2. Claude reads docs/ROADMAP.md and docs/README.md
   ↓
3. Claude creates docs/plans/current.md with plan
   ↓
4. Claude asks for approval (or Ed checks async)
   ↓
5. Once approved, Claude Code runs improvement:
   - Ralph Wiggum loop with clear completion criteria
   - Automated testing (unit tests, Claude in Chrome for UI)
   - Self-correcting iteration
   ↓
6. Claude updates ROADMAP.md, archives plan, commits
   ↓
7. Summary added to Ed's daily note (session debrief)
```

### Implementation Components

**1. Improvement Trigger:**
```
"Improve [tool-name]: [description]"
```

Works from any interface because all context is in GitHub.

**2. Ralph Wiggum Integration:**

Once plan is approved:
```bash
/ralph-loop "Execute the improvement plan at [path/to/docs/plans/current.md].

Steps:
1. Read the plan file
2. Implement each proposed change
3. Run tests after each change
4. If tests fail, debug and fix
5. Update docs/ROADMAP.md with shipped item
6. Move plan to docs/plans/archive/[date]-[name].md
7. Commit with descriptive message

Output <promise>IMPROVEMENT_COMPLETE</promise> when:
- All proposed changes implemented
- All tests passing
- ROADMAP.md updated
- Plan archived
- Changes committed" \
--max-iterations 30 \
--completion-promise "IMPROVEMENT_COMPLETE"
```

**3. Testing Protocol:**

| Test Type | Tool | When |
|-----------|------|------|
| Unit tests | Bash (pytest, jest) | After each code change |
| Skill tests | Direct invocation | After SKILL.md changes |
| UI tests | Claude in Chrome | For deployed prototypes |
| Integration | Combined | Before completion |

**4. Claude in Chrome Testing:**
```
1. Deploy to Vercel (45-second cycle)
2. Navigate to deployed URL
3. Fill forms / click buttons
4. Verify output matches expected
5. Screenshot as evidence
6. If fail: fix and redeploy
```

---

## Part 3: Implementation Phases

### Phase 1: Documentation Structure
- [ ] Create `docs/` folder in 2-3 existing skills as pattern
- [ ] Write README.md, GUIDE.md, ROADMAP.md for those skills
- [ ] Create plans/ folder structure
- [ ] Update CLAUDE.md with new conventions
- [ ] Test: Can Claude find docs from web/desktop client?

### Phase 2: Improvement Skill
- [ ] Create `improve-tool` skill that:
  - Reads tool's docs/ROADMAP.md for context
  - Reads tool's docs/README.md for architecture
  - Creates docs/plans/current.md with plan
  - Asks for approval
- [ ] Test from web client

### Phase 3: Ralph Wiggum Integration
- [ ] Create standard prompt template for improvements
- [ ] Define completion criteria patterns
- [ ] Test with simple improvement
- [ ] Document cost expectations

### Phase 4: Full Pipeline Test
- [ ] End-to-end: trigger → plan → approve → execute → complete
- [ ] Session debrief captures summary in Zettelkasten
- [ ] Document workflow in CLAUDE.md

---

## Constraints & Considerations

### Agent Skill Framework Compatibility
The `docs/` folder doesn't conflict with Anthropic's skill spec:
- SKILL.md stays at root (required)
- `docs/` is just another subfolder (allowed)
- Contents loaded via Read tool, not automatic context

### Cost Control
Ralph Wiggum loops can be expensive:
- Always set `--max-iterations`
- Simple improvements: 10-15 iterations
- Complex improvements: 30-50 iterations
- Monitor and adjust

### Approval Options
1. **In-plan checkbox** - Ed marks `[x]` in current.md
2. **Verbal** - "Approved, run it"
3. **Async** - Check docs/plans/current.md, approve in next session

### What Stays in Zettelkasten
- Daily notes (tasks, wins, blockers)
- Session debriefs
- Research swarm outputs
- Captures from mobile
- Personal reflections

### What Lives in GitHub
- Tool documentation (README, GUIDE)
- Roadmaps
- Improvement plans
- Decision logs
- Test results
- Anything a tool needs to improve itself

---

## Success Metrics

1. **Accessibility:** Any Claude interface can read any tool's docs
2. **Plan quality:** Plans detailed enough to execute without clarification
3. **Autonomy rate:** % of improvements completing without intervention
4. **Cycle time:** Approval to completion
5. **Error rate:** Improvements that introduce bugs (<5%)

---

## Kill Rules

- If documentation overhead slows shipping: simplify structure
- If Ralph loops cost >$20 for simple improvements: adjust iteration limits
- If approval friction blocks progress: make lighter
- If autonomous changes introduce bugs: add more testing gates

---

## Decisions (Approved 2026-01-08)

1. **Approval mechanism:** Verbal (we're in terminal)
2. **First pilot:** newsletter-coach skill
3. **Cost tolerance:** $20 while figuring it out
4. **Next after pilot:** setter-playbook prototype
5. **Voice for GUIDE.md/ROADMAP.md:** Ed's tone - business coach friendly with analogies and metaphors

---

## Next Steps

1. ✅ Plan approved
2. Create docs/ for newsletter-coach as the pattern
3. Apply same pattern to setter-playbook
4. Build the `improve-tool` skill
5. Test end-to-end with one simple improvement
