# Newsletter Writer Agent - From Spark to Draft

## What It Does (In Plain English)

You have an idea. Maybe it's a YouTube video that sparked something. Maybe it's an experience you had. Maybe it's just a topic you want to explore.

This agent turns that spark into a complete newsletter draft, saved to your knowledge base, ready for final polish and publish.

It's like having a writing partner who handles the heavy lifting - research, structure, first draft - so you can focus on the finishing touches.

## Why It Exists

Writing newsletters is valuable but time-consuming. The process involves:
1. Finding/researching the topic
2. Structuring the argument
3. Writing the draft
4. Crafting a compelling headline
5. Cleaning up AI-isms if you used AI help
6. Saving it properly

This agent automates the entire pipeline. You provide the spark, it provides the draft.

## When to Use It

**Perfect for:**
- Turning YouTube videos into articles (uses youtube-processor)
- Developing ideas into full articles
- Writing about recent experiences or lessons
- Topic-based content creation

**Input types it handles:**
- YouTube URLs → transcript extraction → article
- Topics → web research → article
- Ideas/experiences → direct development → article

## The Pipeline

```
Input → Research → Outline → Draft → Hook Scoring → Slop Cleaning → Save
```

**Stage 1: Input Processing**
Agent identifies what you gave it (URL? Topic? Raw idea?) and routes accordingly.

**Stage 2: Research/Extraction**
For videos: extracts transcript. For topics: searches web. For experiences: works with what you provided.

**Stage 3: Outline Development**
Structures the article - intro, body sections, conclusion. Ensures logical flow.

**Stage 4: Draft Writing**
Writes the full article in Ed's voice (uses mission-context skill).

**Stage 5: Hook Evaluation**
Runs the headline through Hook Stack to score and potentially improve it.

**Stage 6: Slop Detection**
Removes AI writing patterns (uses ai-slop-detector skill).

**Stage 7: Save & Link**
Saves to Zettelkasten with proper filename, links in daily note.

## What You Get

A complete draft saved to your Obsidian vault:
- **Location:** `Zettelkasten/Newsletter Draft - [Title] - YYYY-MM-DD.md`
- **Format:** Ready for final review and publish
- **Linked:** Appears in your daily note's Captures section

## The Analogy

Think of this agent like a staff writer who knows your voice. You hand them a topic and say "write this up." They come back with a solid draft that sounds like you wrote it. You review, polish the bits that need your personal touch, and publish.

You're the editor and final voice. The agent is the writer who gets you 80% there.

## Automation vs Interactive

**Say "automatically" or "just do it" when:**
- You trust the agent to make good decisions
- You want the full pipeline without interruptions
- You're batch processing multiple articles

**Skip automation when:**
- You want input on the direction
- The topic is sensitive or nuanced
- You prefer to guide each stage

## Pro Tips

**On YouTube videos:**
The agent can process any YouTube URL with captions. Works best with educational/thought-leadership content. Interview formats extract well too.

**On headlines:**
The Hook Stack evaluation happens automatically. If the headline scores low, the agent generates alternatives. Strong hooks = better open rates.

**On voice:**
The mission-context skill ensures content sounds like Ed. If something feels off, it's usually a slop pattern that the detector caught.

**On editing:**
The output is a draft, not final copy. Spend 15 minutes on final polish - your personal touches make it yours.
