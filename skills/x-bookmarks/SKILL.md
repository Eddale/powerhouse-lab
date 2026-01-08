---
name: x-bookmarks
description: Fetches Twitter/X bookmarks and drops them into Inbox folder for capture-triage. Use when "process my X bookmarks", "fetch twitter bookmarks", "check my twitter bookmarks".
allowed-tools: Read, Write, Glob, Bash, WebFetch
---

# X Bookmarks

## What This Does

Fetches your Twitter/X bookmarks via bird CLI, expands shortened links, extracts basic
metadata, and drops them as markdown files into your Inbox folder. From there, capture-triage
handles classification and routing to Ready.

**The flow:**
```
bird CLI → expand t.co links → extract metadata → .md to Inbox/ → capture-triage handles rest
```

## Prerequisites

### bird CLI Setup

This skill requires the `bird` CLI for Twitter API access.

**Install bird:**
```bash
npm install -g bird-cli
# OR build from source for pagination support:
git clone https://github.com/steipete/bird.git
cd bird && pnpm install && pnpm run build:dist && npm link --force
```

**Get Twitter credentials:**
1. Open Twitter/X in your browser
2. Open Developer Tools → Application → Cookies
3. Copy these values:
   - `auth_token`
   - `ct0`

**Configure (one-time):**
Create `~/.bird/config.json`:
```json
{
  "authToken": "your_auth_token_here",
  "ct0": "your_ct0_here"
}
```

Or set environment variables:
```bash
export AUTH_TOKEN="your_auth_token"
export CT0="your_ct0"
```

---

## Paths

```
Inbox: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
```

---

## Instructions

### Step 1: Check bird CLI

Verify bird is available:
```bash
which bird && bird --version
```

If not found, stop and tell Ed to set up bird CLI (see Prerequisites above).

### Step 2: Fetch Bookmarks

**Default (recent 20):**
```bash
~/bin/bird bookmarks -n 20 --json
```

**Fetch more (paginated):**
```bash
~/bin/bird bookmarks --all --max-pages 5 --json
```

**Note:** Requires AUTH_TOKEN and CT0 environment variables set in ~/.zshrc

Parse the JSON output. Each bookmark has:
- `id` - Tweet ID
- `text` or `full_text` - Tweet content
- `author.username` - Handle
- `author.name` - Display name
- `createdAt` - Timestamp

### Step 3: Check for Duplicates

Before processing, check which bookmarks are already in Inbox:

```bash
ls /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/x-*.md 2>/dev/null
```

Skip any bookmark IDs that already have files.

### Step 4: Process Each New Bookmark

For each bookmark:

#### 4a: Expand t.co Links

Find all `https://t.co/xxxxx` links in the tweet text.

For each t.co link, use WebFetch to follow redirects:
```
WebFetch(url: "https://t.co/xxxxx", prompt: "What is the final URL after redirects?")
```

Or use curl:
```bash
curl -Ls -o /dev/null -w '%{url_effective}' "https://t.co/xxxxx"
```

#### 4b: Categorize Link Type

Based on expanded URL:
- `github.com` → type: github
- `youtube.com`, `youtu.be` → type: video
- `medium.com`, `substack.com`, blog patterns → type: article
- `x.com`, `twitter.com` (not media) → type: tweet (quote)
- Other → type: link

#### 4c: Extract Basic Metadata

**For GitHub repos:**
```bash
# Extract owner/repo from URL, fetch via API
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{name, description, stargazers_count, language}'
```

**For articles:** Fetch and summarize the full article content:

```
WebFetch(url: "[expanded URL]", prompt: "Extract the article title and main content, ignoring navigation, ads, and sidebars. Then summarize in this exact format:

TITLE: [article title]
SOURCE: [domain name]

TL;DR: [One sentence core takeaway]

KEY POINTS:
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]
- [Point 5]
(include up to 7 points if the article warrants it)

WHY IT MATTERS: [One sentence on relevance or application]")
```

**If WebFetch fails** (timeout, paywall, error): Still drop to Inbox with a note:
```
## Summary

*Fetch failed - article may be paywalled or unavailable. Visit link to read.*
```

**For videos:** Note for future transcription, capture title if visible.

**For plain tweets/quotes:** Use the tweet text as-is.

### Step 5: Write to Inbox

For each processed bookmark, create a markdown file:

**Filename:** `x-{id}.md` (e.g., `x-1234567890.md`)

**Template (non-article):**
```markdown
---
source: x-bookmark
author: @{username}
author_name: {display_name}
tweet_url: https://x.com/{username}/status/{id}
captured: {YYYY-MM-DD}
link_type: {github|video|tweet|link}
---

{Tweet text}

**Linked:** [{title or domain}]({expanded_url})

{Brief description or key info extracted}
```

**Template (article with summary):**
```markdown
---
source: x-bookmark
author: @{username}
author_name: {display_name}
tweet_url: https://x.com/{username}/status/{id}
captured: {YYYY-MM-DD}
link_type: article
article_title: "{Article Title}"
article_source: {domain.com}
---

{Tweet text}

**Linked:** [{Article Title}]({expanded_url})

## Summary

**TL;DR:** {One sentence core takeaway}

**Key Points:**
- {Point 1}
- {Point 2}
- {Point 3}
- {Point 4}
- {Point 5}

**Why It Matters:** {Relevance or application}

---
*Auto-summarized by x-bookmarks*
```

**Example output (GitHub):**
```markdown
---
source: x-bookmark
author: @simonw
author_name: Simon Willison
tweet_url: https://x.com/simonw/status/123456789
captured: 2026-01-08
link_type: github
---

Just discovered this amazing tool for real-time transcription https://t.co/abc123

**Linked:** [whisper-flow](https://github.com/dimastatz/whisper-flow)

Real-time speech-to-text using OpenAI Whisper with streaming support. 2.3k stars, Python.
```

**Example output (Article):**
```markdown
---
source: x-bookmark
author: @paulg
author_name: Paul Graham
tweet_url: https://x.com/paulg/status/987654321
captured: 2026-01-08
link_type: article
article_title: "How to Do Great Work"
article_source: paulgraham.com
---

This might be the most important thing I've written https://t.co/xyz789

**Linked:** [How to Do Great Work](https://paulgraham.com/greatwork.html)

## Summary

**TL;DR:** Great work comes from working on problems you're genuinely curious about, not from following a predetermined path.

**Key Points:**
- Curiosity is the compass - follow what genuinely interests you
- Great work requires both ability and interest in a specific domain
- You need to be working at the edge of your field to see good problems
- Consistency compounds - small daily progress beats sporadic bursts
- Avoid prestige traps - external validation often points away from important work

**Why It Matters:** Framework for choosing what to work on and staying motivated long-term.

---
*Auto-summarized by x-bookmarks*
```

### Step 6: Report Summary

After processing all bookmarks:

```markdown
## X Bookmarks Processed - YYYY-MM-DD HH:MM

**Fetched:** N bookmarks
**New:** M (skipped K duplicates)

### Dropped to Inbox
- x-123.md - @author: [brief description]
- x-456.md - @author: [brief description]
- ...

Ready for capture-triage.
```

---

## Options

The user can specify:

| Option | Default | Example |
|--------|---------|---------|
| count | 20 | "fetch my last 50 bookmarks" |
| all | false | "fetch all my bookmarks" |
| max-pages | 5 | "fetch all bookmarks, max 10 pages" |

---

## Integration with Daily Review

This skill can be invoked:
1. **Standalone:** "process my X bookmarks"
2. **Before daily-review:** Run this first, then daily-review's capture-triage picks them up

The skill does NOT invoke capture-triage directly - it just drops files. This keeps
the separation clean and lets Ed decide when to triage.

---

## Error Handling

**bird not found:**
> bird CLI is not installed. See Prerequisites in the skill docs for setup instructions.

**Auth expired (403 errors):**
> Twitter session expired. Get fresh auth_token and ct0 from browser cookies.

**No new bookmarks:**
> No new bookmarks to process. All recent bookmarks already in Inbox.

---

## Guidelines

- Always check for duplicates before processing
- Use tweet ID in filename for deduplication
- Articles get full summarization; other types stay light
- If article fetch fails, still drop to Inbox with "fetch failed" note
- Don't invoke capture-triage directly - just drop files
- Report what was processed so Ed knows what's ready

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial build - fetch, expand, drop to Inbox |
| 1.2 | 2026-01-08 | Article summarization - auto-summarize articles before dropping to Inbox |
