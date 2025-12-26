# Powerhouse Lab

**The Leverage Skunkworks** - Where AI tools and skills get built, tested, and validated before going live.

This is Ed's personal lab for creating AI leverage assets using the Prompt Whispering™ methodology.

---

## How This Works

### The Lifecycle

```
prototypes/     →     skills/        →     [Own Repo]
(Experiments)        (Validated)           (Graduated)
```

1. **Prototypes** - New ideas, rough builds, testing concepts
2. **Skills** - Working, documented, reusable assets
3. **Graduates** - Client-facing tools get their own repo

### When Things Don't Work

```
prototypes/     →     archive/
(Experiments)        (Kill rule applied)
```

Failed experiments go to archive. We learn from them, we don't delete them.

---

## Folder Structure

```
powerhouse-lab/
├── CLAUDE.md                # Operating manual for Claude
├── _templates/              # Starting points for new builds
│   ├── skill-template/      # For Claude skills
│   └── tool-template/       # For standalone tools
├── skills/                  # Validated, reusable skills
├── prototypes/              # Works in progress
└── archive/                 # Retired experiments (learn from these)
```

---

## Quick Commands

```bash
# Start working on a prototype
cp -r _templates/skill-template prototypes/my-new-idea

# Promote to validated skill
mv prototypes/my-skill skills/my-skill

# Retire something that didn't work
mv prototypes/failed-experiment archive/failed-experiment
```

---

## Project Types

| Type | Location | Purpose |
|------|----------|---------|
| `powerhouse-prototype` | prototypes/ | Proof of concept, learning |
| `skill-build` | skills/ | Reusable Claude skill |
| `blackbelt-tool` | Own repo | Client-facing, polished |
| `content-engine` | Either | Speed tools for content creation |

---

## The Philosophy

> Ship This = Win Day

No dabbling. No endless tinkering. Build, validate, ship or kill.

Every skill here should either become a deployed leverage asset or teach us something worth knowing.
