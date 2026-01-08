# Task Clarity Scanner - How It Works

## The One-Sentence Version

It's like having a project manager look at your todo list and ask "what exactly does this mean?" for every vague item.

## Why This Exists

Here's the problem with todo lists: vague tasks don't get done.

"Research API options" sits there for days. What API? For what project? What counts as done?

But "Research 3 CRM APIs for lead capture - compare Pipedrive, HubSpot, Close - write 1-paragraph rec by Friday" - that gets done.

The difference is clarity. This skill takes your daily note and makes every task specific enough to actually execute.

## The Mental Model: Personal Kanban

Your daily note is a Kanban board with three key zones:

**Ship This = Win Day** - The ONE thing that matters most. If this ships, today was a win.

**Today's 3** - Active work. Three tasks, no more. This is your WIP limit. When you're at 3, you can't add a fourth until something's done.

**Ready** - The backlog. Everything waiting to be pulled. This is where tasks queue up until there's room in Today's 3.

The skill manages this flow. Pull from Ready to Today's 3. Complete and move to Done. Keep the board healthy.

## How You Actually Use It

Say "scan my tasks" or "review my daily note."

First, you get a health check:
- How many items in Today's 3? (Target: exactly 3)
- Any stale items? (Rolling 3+ days)
- How big is Ready? (Is backlog growing?)

Then, one by one, unclear tasks get surfaced:

```
Task: "Make Google Drive AI Ready"

Issue: What does "AI Ready" mean? What's the done state?
Suggested rewrite: "Organize Google Drive for AI access: Create 'AI-Ready' folder, move key docs, document what each folder contains (01-04)"
What's needed: Definition of "AI Ready"
```

You clarify, accept the rewrite, or skip. When done, changes get applied in a batch.

## The Stale Item Pattern

Tasks that roll for 3+ days get the `[STALE]` tag. That's a signal something's wrong.

Either:
- It's too big (break it down)
- It's not actually important (drop it)
- Something's blocking it (move to Waiting For)
- You're avoiding it (do it now or admit you won't)

The skill surfaces stale items and asks: "Do it now, delegate, drop, reframe, or Someday?"

## The Project File Upgrade

Sometimes a task is too big to clarify inline. "Build client onboarding system" isn't a task - it's a project.

For these, the skill offers to create a project file:
```
/Zettelkasten/PROJECT - Client Onboarding System.md
```

The daily note gets a link instead of the full task. The project file becomes a living document where you collect context, decisions, and steps.

## The Batch Pattern

Notice the skill doesn't edit as you go. It collects all clarifications first, then applies them in a batch at the end.

Why? Because you need to see the whole picture. One clarification often reveals related tasks. Batching lets you see everything before committing changes.

## What It's NOT

This isn't a task app. It works with your existing daily notes in Obsidian.

This isn't autopilot. It suggests rewrites, but you approve them. The human stays in the loop.

This isn't execution. It clarifies tasks, but you still do the work. (Though it can hand off to agents for execution.)

## The Copywriter Analogy

Good copy is specific. "Make money" is weak. "Earn your first $1,000 from freelance writing in 30 days" is strong.

Tasks are the same. The skill is like an editor who keeps asking "what exactly do you mean?" until every task is clear enough to act on.
