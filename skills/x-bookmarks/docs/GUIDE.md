# X Bookmarks - How It Works

## The One-Sentence Version

It's like having an assistant who empties your Twitter bookmarks into your inbox every day, with all the links expanded and categorized.

## Why This Exists

You bookmark things on Twitter. Interesting threads. Cool tools. Articles worth reading. GitHub repos to check out.

Then they sit there. Forever. Because Twitter's bookmark interface is terrible for actually processing what you saved.

This skill bridges Twitter bookmarks to your daily review system. Bookmarks become markdown files in your Inbox folder. From there, capture-triage handles them like any other capture.

## The Mental Model: The Bookmark Emptier

Think of Twitter bookmarks like a physical inbox tray that keeps filling up. You throw things in when you're scrolling, but you never empty it.

This skill is the emptying process. It takes everything from that tray, organizes it (what kind of thing is this?), and drops it into your main inbox where you'll actually deal with it.

## How You Actually Use It

Bookmark things on Twitter normally throughout the day/week.

When ready to process, say "fetch my X bookmarks."

The skill:
1. Connects to Twitter via bird CLI
2. Fetches your recent bookmarks
3. Expands all those short t.co links to real URLs
4. Categorizes each (GitHub repo? Article? Video? Just a tweet?)
5. Drops markdown files into your Inbox folder

Then, when you run your daily review, capture-triage picks them up along with everything else.

## Link Expansion Matters

Twitter shortens all links to t.co URLs. "https://t.co/abc123" tells you nothing.

The skill follows each redirect to get the real URL. Now you can see it's a GitHub repo, or a Substack article, or a YouTube video. The category becomes obvious.

## What Gets Captured

Each bookmark becomes a markdown file with:
- Who tweeted it
- What they said
- The expanded link
- A brief description (for articles and GitHub repos)
- Category tag

Example output:
```
@simonw: Just discovered this amazing tool...

Linked: whisper-flow (github.com/dimastatz/whisper-flow)

Real-time speech-to-text using Whisper. 2.3k stars, Python.
```

Now that's actionable. You can decide: task (check this out), idea (could use this for X), or just reference.

## What It's NOT

This isn't bookmark management. It doesn't organize your Twitter bookmarks - it empties them into your system.

This isn't automatic. You trigger it when you want to process bookmarks.

This isn't a replacement for capture-triage. It feeds INTO capture-triage. The skill drops files, capture-triage classifies and routes them.

## The Two-Stage Pattern

Notice the separation:
1. **X-bookmarks** - Fetch and drop files
2. **Capture-triage** - Classify and route

This keeps things clean. Each skill does one job. X-bookmarks doesn't need to know about Ready sections or research swarms. It just delivers raw material.

## The Collector Analogy

Like a coin collector who picks up interesting coins throughout the day, then sorts them at night. The collecting happens opportunistically (while scrolling Twitter). The sorting happens systematically (during daily review).

This skill handles the handoff between collecting and sorting.
