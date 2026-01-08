# X Bookmarks - Technical Reference

## What It Does

Fetches Twitter/X bookmarks via bird CLI, expands t.co links, extracts metadata, and drops them as markdown files into the Inbox folder. **Articles are automatically summarized** with TL;DR, key points, and relevance. Capture-triage handles classification and routing from there.

## Architecture

```
x-bookmarks/
├── SKILL.md              # Main skill definition (fetch + process)
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Check existing files
- `Write` - Create markdown files
- `Glob` - Find duplicates
- `Bash` - Run bird CLI
- `WebFetch` - Expand t.co links

**External dependency:**
- `bird` CLI - Twitter API access tool

## Prerequisites

### bird CLI Setup

```bash
# Install
npm install -g bird-cli
# OR build from source for pagination
git clone https://github.com/steipete/bird.git
cd bird && pnpm install && pnpm run build:dist && npm link --force

# Configure (~/.bird/config.json)
{
  "authToken": "your_auth_token",
  "ct0": "your_ct0"
}
```

Get auth_token and ct0 from Twitter cookies in browser DevTools.

## Usage

**Trigger phrases:**
- "Process my X bookmarks"
- "Fetch twitter bookmarks"
- "Check my twitter bookmarks"

**Input:** None (fetches from Twitter API)

**Output:** Markdown files in Inbox/ folder

## Inbox Location

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
```

## Processing Pipeline

1. **Fetch** - bird CLI gets bookmarks as JSON
2. **Dedupe** - Skip IDs already in Inbox
3. **Expand** - Follow t.co redirects to real URLs
4. **Categorize** - github/article/video/tweet/link
5. **Metadata** - Extract title, description, stars (GitHub)
6. **Summarize** - For articles: fetch content, generate TL;DR + 5-7 key points + relevance
7. **Write** - Drop as `x-{id}.md` files
8. **Report** - Summary of what was processed

## File Format

**Standard format (non-article):**
```markdown
---
source: x-bookmark
author: @username
tweet_url: https://x.com/user/status/123
captured: YYYY-MM-DD
link_type: github|video|tweet|link
---

{Tweet text}

**Linked:** [title](expanded_url)

{Brief description}
```

**Article format (with summary):**
```markdown
---
source: x-bookmark
author: @username
tweet_url: https://x.com/user/status/123
captured: YYYY-MM-DD
link_type: article
article_title: "Title"
article_source: domain.com
---

{Tweet text}

**Linked:** [Article Title](expanded_url)

## Summary

**TL;DR:** One sentence takeaway.

**Key Points:**
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

**Why It Matters:** Relevance or application.

---
*Auto-summarized by x-bookmarks*
```

## Testing

**Manual verification:**
1. Run "fetch my X bookmarks"
2. Verify bird CLI runs
3. Check files created in Inbox/
4. Verify t.co links expanded
5. Confirm no duplicates created
6. For article bookmarks: verify Summary section present with TL;DR, Key Points, Why It Matters
7. For failed fetches: verify "fetch failed" note appears instead of summary
