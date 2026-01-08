# Research Swarm Agent - Multiple Brains, One Answer

## What It Does (In Plain English)

When you have a complex question that needs more than one perspective, this agent attacks it from multiple angles simultaneously. Instead of researching one thing at a time, it spins up multiple researchers who work in parallel.

Think of it like asking five different experts the same question at once, then getting a synthesis of all their answers.

## Why It Exists

Complex questions have multiple facets. "Should I use AI for my coaching business?" isn't one question - it's actually:
- What AI capabilities exist? (technical)
- What are competitors doing? (market)
- How would I implement this? (practical)
- What do my clients want? (user)
- What could go wrong? (risk)

Researching these sequentially takes forever. Researching them in parallel gets you comprehensive insights in a fraction of the time.

## When to Use It

**Use Research Swarm when:**
- You need 3+ distinct research angles
- You're making a strategic decision with multiple valid options
- You're evaluating technology or competitive landscape
- Time-to-insight matters (parallel beats sequential)
- The question is complex enough to warrant multiple perspectives

**Don't use Research Swarm when:**
- You need one specific fact
- The question is straightforward (API docs, syntax, etc.)
- You already know the angle you're investigating
- Speed is critical and depth is secondary

## How It Works

```
Topic → Identify Angles → Spawn Researchers → Parallel Investigation → Synthesis → Document
```

**Stage 1: Angle Identification**
What are the 3-5 distinct perspectives this topic needs? The agent determines these based on the question type.

**Stage 2: Parallel Spawning**
Each angle gets its own sub-agent (using the Task tool). They all start at the same time.

**Stage 3: Independent Research**
Each sub-agent investigates its angle - web searches, document reads, whatever it needs.

**Stage 4: Result Collection**
When all sub-agents complete, their findings are gathered.

**Stage 5: Synthesis**
The agent combines insights into a unified document. Not just concatenation - actual synthesis that identifies patterns, conflicts, and key takeaways.

**Stage 6: Save & Link**
The research document goes to your Zettelkasten and gets linked in your daily note.

## The Analogy

It's like having a war room with five researchers who each have a different specialty. You walk in with a question, they all scatter to investigate their angle, and they reconvene to give you the full picture.

One researcher might miss something. Five researchers covering different angles rarely do.

## What You Get

A comprehensive research document saved to your Zettelkasten:
- **Overview** - The question and why it matters
- **Angle-by-angle findings** - What each perspective uncovered
- **Synthesis** - Key themes, patterns, conflicts
- **Recommendations** - What the research suggests you should do
- **Open questions** - What wasn't resolved, needs more investigation

## Time Savings

| Approach | 5 Angles @ 5min each |
|----------|---------------------|
| Sequential | 25 minutes |
| Parallel (Swarm) | 8-10 minutes |

The time savings compound with complexity. More angles, more savings.

## Pro Tips

**On angle selection:**
The agent picks angles based on the question type. You can also specify: "Research X with particular focus on Y and Z angles."

**On video research:**
The swarm can process YouTube videos using the youtube-processor skill. Great for topic research where video content exists.

**On follow-up:**
Research swarm outputs often surface new questions. These go in the "Open Questions" section. You can spawn another swarm for those.

**On synthesis:**
Don't skip the synthesis. The individual angle findings are useful, but the real insight comes from seeing how they connect.
