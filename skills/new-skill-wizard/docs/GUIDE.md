# New Skill Wizard - How It Works

## The One-Sentence Version

It's like having a senior developer set up all the boilerplate and wiring when you want to create a new capability.

## Why This Exists

Creating a skill manually involves a lot of steps. Create the folder. Create the right subfolders. Write the SKILL.md with correct frontmatter. Set up symlinks. Register in settings. Create a git branch. Write documentation.

Miss one step and the skill doesn't work. Forget the settings registration and Claude Code ignores it entirely.

This wizard handles all of that. You say what the skill should do, it creates everything correctly.

## The Mental Model: The Template Factory

Think of it like having a factory that stamps out perfectly structured skill folders. Every skill gets the same layout, the same documentation structure, the same testing plan format.

Consistency matters. When every skill looks the same, you can work on any of them without relearning the structure.

## How You Actually Use It

Say "create a new skill" or "new skill called brand-voice."

The wizard asks three questions (if you didn't already answer them):
1. What's the name? (kebab-case like `brand-voice`)
2. What does it do? (one sentence)
3. When should it trigger? (phrases like "check brand voice")

Then it does everything:
- Creates the git branch
- Makes all the folders
- Writes starter docs
- Sets up symlinks
- Registers in Claude Code
- Walks you through building the actual instructions

## The Wiring Problem

Here's what most people miss: a skill needs two things to work.

**Visibility:** Symlinks make Claude Code see the skill exists.
**Permission:** Settings registration makes Claude Code willing to use it.

The wizard does both. That's why skills created this way actually work, while manually-created skills often don't.

## What Gets Created

```
skills/brand-voice/
├── SKILL.md              # The instructions
├── docs/
│   ├── README.md         # Technical reference
│   ├── GUIDE.md          # This kind of explanation
│   └── ROADMAP.md        # Future ideas
├── scripts/              # Python/Bash if needed
├── references/           # Docs Claude loads
├── resources/            # Templates/data
└── assets/               # Images/binaries
```

Everything a skill might need, stubbed out and ready.

## The Documentation Philosophy

Notice docs/ gets created with the skill, not later. That's intentional.

Documentation is part of shipping. A skill without docs is a skill that future-you won't understand. The wizard enforces this by making docs creation automatic.

## What It's NOT

This isn't a skill that runs other skills. It creates them.

This isn't a code generator. It creates structure and stubs. You still fill in what the skill actually does.

This isn't optional if you want skills to work reliably. Manual creation skips steps.

## The Assembly Line Analogy

Think of building cars. You could hand-build each one, but you'd make mistakes. You'd forget parts. Quality would vary.

Or you could have an assembly line that ensures every car gets the same treatment. Same structure. Same quality checks. Same documentation.

That's what this wizard provides for skills. Consistent, complete, correctly wired.
