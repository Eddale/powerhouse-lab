# MELCHIOR - The Scientist's Perspective

## What It Does (In Plain English)

MELCHIOR is the technical brain of the MAGI system. When you need to understand how something works, how to build something, or how to evaluate technical options - MELCHIOR is your agent.

Think of MELCHIOR as having a senior engineer on call. Someone who can dive into code, read documentation, understand architectures, and explain it all in a way that makes sense.

## Why It Exists

Not everyone needs to understand the technical details. But someone does. MELCHIOR ensures there's always a "technical brain" available to:
- Analyze how existing code works
- Research how external APIs function
- Evaluate different technical approaches
- Build logical frameworks for complex problems

Named after the MAGI supercomputer that represented the "scientist" personality - logical, analytical, and focused on understanding.

## When to Use It

**Use MELCHIOR when:**
- You need to understand how something works technically
- You're evaluating architecture decisions
- You need API research or documentation analysis
- You're building something and need technical guidance
- The question starts with "how do I..." or "how does..."

**Don't use MELCHIOR for:**
- Voice/audience questions (use BALTHASAR)
- Testing and QA (use CASPER)
- Non-technical decision making

## The MAGI Trinity

| Agent | Role | Question It Answers |
|-------|------|---------------------|
| MELCHIOR | Scientist | "How does this work?" |
| BALTHASAR | Mother | "What does this mean for people?" |
| CASPER | QA | "What could go wrong?" |

## Real Examples

**Example 1: Code Analysis**
> Question: "How does the youtube-processor skill extract transcripts?"
> MELCHIOR: "It uses the youtube-transcript-api Python library. The `get_transcript.py` script takes a video ID, calls the API, and returns the raw transcript text. No API key needed - it uses YouTube's auto-generated captions."

**Example 2: Architecture Decision**
> Question: "Should we use a database or flat files for storing processed videos?"
> MELCHIOR: "For your current scale (< 1000 videos), flat files in the Zettelkasten work fine. Benefits: human-readable, searchable with grep, no dependencies. Trade-off: no relational queries. Recommendation: flat files now, reconsider if you need cross-video queries."

**Example 3: API Research**
> Question: "How does the Vercel API handle deployments?"
> MELCHIOR: "[researches docs] The Vercel API uses `/v13/deployments` endpoint. You POST a source (git URL or file uploads), it returns a deployment ID. You can poll the deployment status or use webhooks. Rate limit is 100 requests/minute."

## The Analogy

MELCHIOR is like having a technical co-founder who doesn't need equity. You can ask them anything technical - how something works, how to build something, what approach is best - and get a clear, informed answer.

They're not going to build it for you (that's what Claude Code does), but they'll tell you exactly how it should be built.

## Output You'll Get

- **Technical analyses** - Deep dives into how code/systems work
- **Architecture recommendations** - Which approach to take and why
- **API documentation summaries** - What you need to know about external services
- **Implementation guides** - Step-by-step technical instructions
- **Framework designs** - Logical structures for complex problems

## Pro Tip

When working on a complex problem, start with MELCHIOR to understand the technical landscape. Then bring in BALTHASAR to check if it matters to your audience. Finally, CASPER to test if it actually works.

MELCHIOR → BALTHASAR → CASPER is often the right sequence.
