# X Bookmarks - Technical Reference

## What It Does

Fetches Twitter/X bookmarks via bird CLI, expands t.co links, extracts metadata, and drops them as markdown files into the Inbox folder. Capture-triage handles classification and routing from there.

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
6. **Write** - Drop as `x-{id}.md` files
7. **Report** - Summary of what was processed

## File Format

```markdown
---
source: x-bookmark
author: @username
tweet_url: https://x.com/user/status/123
captured: YYYY-MM-DD
link_type: github|article|video|tweet|link
---

{Tweet text}

**Linked:** [title](expanded_url)

{Brief description}
```

## Testing

**Manual verification:**
1. Run "fetch my X bookmarks"
2. Verify bird CLI runs
3. Check files created in Inbox/
4. Verify t.co links expanded
5. Confirm no duplicates created
