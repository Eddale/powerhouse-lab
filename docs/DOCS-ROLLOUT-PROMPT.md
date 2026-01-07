# Docs Rollout Project - Claude Desktop Prompt

Copy everything below the line into Claude Desktop after restarting it with MCP enabled.

---

## PROJECT: Add docs/ folder to all tools in powerhouse-lab

**Location:** `/Users/eddale/Documents/GitHub/powerhouse-lab`

**Summary destination:** `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/`

### Context

We've established a documentation standard for all tools, skills, agents, and prototypes. Every tool gets a `docs/` folder that enables autonomous improvement - Claude can read these docs to understand how to improve the tool without asking questions.

**The principle:** GitHub = single source of truth. Documentation lives with the code.

### Reference Patterns (Already Complete)

Read these first to understand the pattern:

**Skill pattern:**
- `/Users/eddale/Documents/GitHub/powerhouse-lab/skills/newsletter-coach/docs/README.md`
- `/Users/eddale/Documents/GitHub/powerhouse-lab/skills/newsletter-coach/docs/GUIDE.md`
- `/Users/eddale/Documents/GitHub/powerhouse-lab/skills/newsletter-coach/docs/ROADMAP.md`

**Prototype pattern:**
- `/Users/eddale/Documents/GitHub/powerhouse-lab/prototypes/blackbelt-playbook-generator/docs/ROADMAP.md`

### Structure to Create

**For each SKILL, create:**
```
skills/<name>/docs/
├── README.md         # Technical reference
├── GUIDE.md          # Business-friendly (Ed's voice, analogies)
├── ROADMAP.md        # Shipped + planned + ideas + learnings
└── plans/
    └── archive/
```

**For each PROTOTYPE, create:**
```
prototypes/<name>/docs/
├── ROADMAP.md        # (README and HOW-IT-WORKS already exist at root)
└── plans/
    └── archive/
```

**For AGENTS, create:**
```
.claude/agents/docs/<agent-name>/
├── README.md
├── GUIDE.md
├── ROADMAP.md
└── plans/
    └── archive/
```

### Document Voice

- **README.md** - Technical, factual, for debugging. What it does, dependencies, how to test.
- **GUIDE.md** - Ed's voice. Business coach analogies. Explains the "why" like talking to a smart friend who doesn't code.
- **ROADMAP.md** - Ed's voice. What's shipped (with dates), what's planned, ideas (parking lot), what we've learned.

### Items Needing docs/

**Skills (15):**
1. ai-slop-detector
2. blackbelt-meeting-summary
3. capture-triage
4. hook-stack-evaluator
5. instagram-carousel
6. magic-model-review
7. mission-context
8. new-skill-wizard
9. offer-diamond-review
10. onboarding-doc-builder
11. reflect
12. task-clarity-scanner
13. webfluence
14. x-bookmarks
15. youtube-processor

**Prototypes (3):**
1. ai-agent-control-center
2. email-agent
3. newsletter-brainstorm

**Agents (7):**
1. balthasar
2. casper
3. daily-review
4. instagram-carousel
5. melchior
6. newsletter-writer
7. research-swarm

### Your Process

For each item:

1. **Read the existing SKILL.md or agent definition** to understand what it does
2. **Create the docs/ folder structure** with all subfolders
3. **Write README.md** - Technical reference based on the skill/agent
4. **Write GUIDE.md** - Business-friendly explanation in Ed's voice
5. **Write ROADMAP.md** - Shipped history, planned items, ideas, learnings
6. **Move to next item**

### After ALL Items Complete

1. **Create a summary file** in Zettelkasten:
   - Location: `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Docs Rollout Summary - YYYY-MM-DD.md`
   - Include: List of all items documented with one-line description of each
   - Format:
     ```markdown
     # Docs Rollout Summary - YYYY-MM-DD

     ## Skills Documented
     | Skill | What It Does | Key Insight from GUIDE |
     |-------|--------------|------------------------|
     | ai-slop-detector | ... | ... |

     ## Prototypes Documented
     ...

     ## Agents Documented
     ...
     ```

2. **Update today's daily note:**
   - Location: `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md`
   - Add to **Captures** section: `- [[Docs Rollout Summary - YYYY-MM-DD]] - Added docs/ to X skills, Y prototypes, Z agents`
   - Add to **Done Today** section: `- Completed docs rollout: X skills, Y prototypes, Z agents documented`

3. **Git commit:**
   - Stage all new docs/ folders
   - Commit message: `docs: Add docs/ folder to all skills, prototypes, and agents`
   - Push to main

### Kill Rules

- If a skill/prototype looks abandoned or broken, skip it and note why
- If you can't understand what something does after reading it, flag it for Ed
- Don't spend more than 10 minutes per item - these are starter docs, not perfect docs

### Success Signal

All 25 items have docs/ folders with README.md, GUIDE.md (where applicable), and ROADMAP.md. Summary saved to Zettelkasten. Daily note updated. Changes committed and pushed.

---

**Start by reading the reference patterns, then work through the skills alphabetically.**
