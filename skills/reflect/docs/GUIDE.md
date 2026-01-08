# Reflect - How It Works

## The One-Sentence Version

It's like having an assistant who takes notes when you correct them, then updates their own training manual so they don't make the same mistake twice.

## Why This Exists

Here's the frustrating truth about AI assistants: they don't learn from you.

Every conversation starts from zero. You correct a mistake on Monday. Tuesday, same mistake. Wednesday, same mistake. The learning doesn't stick.

This skill bridges that gap. When you say "never do X," reflect captures that correction and proposes an update to the relevant skill file. Now the instruction is permanent. Future conversations start with that knowledge baked in.

## The Mental Model: The Training Manual Update

Think of skills like training manuals. Each skill has instructions that Claude follows.

When you correct Claude, you're essentially saying "the manual is wrong" or "the manual is missing something." But unless someone updates the manual, the next person who reads it will make the same mistake.

Reflect is the update process. It notices corrections, proposes manual updates, and commits them with your approval.

## How You Actually Use It

Work normally. Correct mistakes as they happen.

At the end of a session (or whenever you want), say "/reflect" or "what did we learn?"

The skill scans the conversation for:
- Explicit corrections ("Never do X")
- Things that worked well (patterns to codify)
- Failed attempts that got fixed (lessons learned)

Then it proposes updates:

```
HIGH Confidence:
- Rule: No emojis in code comments
- Skill to update: mission-context
- Proposed addition to Iron Rules: "4. NO EMOJIS IN CODE."

Approve? [Yes / Modify / Skip]
```

You approve, and the skill file gets updated. Git commit created. Done.

## The Confidence System

Not all observations are equally certain. The skill uses three levels:

**HIGH** - You explicitly said something. "Never make up button styles." That's a clear rule. Propose immediate update.

**MEDIUM** - A pattern worked well, but you didn't explicitly approve it. "The header format worked three times in a row." Worth noting, but ask before adding to the manual.

**LOW** - An observation that might be useful. "User seemed to prefer shorter responses." Note it, but don't update anything yet.

This prevents over-eager updates while capturing the clear wins.

## What It's NOT

This isn't mind-reading. It captures what you explicitly said or clearly demonstrated.

This isn't automatic. You trigger it when you want to capture learnings. (Automatic mode via hooks is planned but not yet implemented.)

This isn't a replacement for good skill design. If a skill is fundamentally broken, reflect won't fix it. It captures refinements, not redesigns.

## The Coaching Analogy

Good coaches keep session notes. What worked? What didn't? What should we try differently next time?

Then they update their approach for the next session.

Reflect does the same thing for AI skills. Session notes become skill updates. The approach improves over time.

## The Learning Loop

```
Conversation happens
  → You make corrections
    → Reflect captures them
      → Skills get updated
        → Next conversation is better
          → (repeat)
```

This is the loop that makes AI assistants actually improve from working with you.
