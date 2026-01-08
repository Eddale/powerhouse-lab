# Onboarding Doc Builder - Technical Reference

## What It Does

Creates role-specific onboarding playbooks in Jennifer Waters' style. Produces structured markdown documents with Loom video placeholders that let new hires self-onboard.

## Architecture

```
onboarding-doc-builder/
├── SKILL.md              # Main skill definition (template + customization)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load existing playbooks for reference
- `Write` - Save playbook to Zettelkasten
- `Edit` - Update existing playbooks
- `AskUserQuestion` - Gather role context

**No external APIs.** Template-based generation.

## Usage

**Trigger phrases:**
- "Create onboarding doc"
- "Build a playbook"
- "Onboarding for [role]"
- "New hire playbook"

**Input:** Role name, core function, tools used

**Output:** Complete playbook markdown saved to Zettelkasten

## Playbook Structure

1. **Company Foundation** - Mission, values, customer avatar
2. **Tech Setup (SOPs)** - Tools, accounts, setup checklist
3. **Role Training** - System overview, product knowledge, scripts
4. **Daily Activities** - Rhythm, pipeline workflow
5. **Scorecard & Compensation** - KPIs, pay structure, OTE
6. **Communication & Support** - Contacts, check-in schedule
7. **Completion Confirmation** - Final steps to mark onboarding done

## Role-Specific Customization

| Role Type | Additional Sections |
|-----------|---------------------|
| Setters/SDRs | Lead qualification, scripts, handoff process |
| Community Managers | Engagement playbook, escalation, events |
| Integrators/Ops | Project management, decision authority, reporting |

## Output Location

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Playbook - [Role] - YYYY-MM-DD.md
```

## Testing

**Manual verification:**
1. Run "create onboarding doc"
2. Provide role details when asked
3. Verify all 7 sections generated
4. Check Loom placeholders present
5. Confirm saved to Zettelkasten

**Quality checks:**
- [ ] All sections have checkboxes
- [ ] Loom placeholders in correct format
- [ ] Role-specific sections included
- [ ] Completion confirmation at end
