# X Bookmarks - Roadmap

## What's Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01-08 | Initial build - fetch, expand, drop to Inbox |
| v1.1 | 2026-01-08 | Added docs/ folder (README, GUIDE, ROADMAP) |
| v1.2 | 2026-01-08 | Article summarization - auto-summarize articles with TL;DR, key points, relevance |

## The Vision

X-bookmarks fetches, categorizes, and enriches bookmarks before dropping to Inbox. Articles now arrive pre-summarized so you know what's worth keeping without clicking through.

Next: YouTube videos auto-processed with transcripts. Threads unrolled into single files. The goal is bookmarks that arrive ready to triage - not raw links that need research.

## Planned Improvements

These are on the list. Not "someday maybe" - actually planned.

- [ ] **YouTube Auto-Processing** - When a bookmark contains a YouTube URL, optionally run it through youtube-processor before dropping to Inbox. Arrive with transcript and summary already done.

- [ ] **Thread Unrolling** - For bookmarked threads (multi-tweet content), fetch the entire thread and drop as a single combined file.

- [ ] **Scheduled Fetching** - Run automatically at a set time (morning? evening?) so bookmarks are always waiting in Inbox.

## Ideas (Not Committed)

These are interesting but not proven necessary yet. Parking lot stuff.

- **GitHub Star Auto-Analysis** - For GitHub repos, fetch more metadata: language, recent activity, what problem it solves.

- **Bookmark Removal** - After successfully processing, optionally remove from Twitter bookmarks to prevent reprocessing.

- **Likes Integration** - Same pipeline but for liked tweets instead of bookmarks.

- **Lists Integration** - Monitor specific Twitter lists, capture new interesting items automatically.

- **Deduplication Across Sessions** - Track processed IDs persistently so restarts don't reprocess old bookmarks.

- **Priority Detection** - If Ed bookmarks the same person repeatedly, flag those as higher priority.

## What We've Learned

Building this skill taught us a few things:

**bird CLI is the key.** Twitter's API is restrictive. bird CLI works around the limitations using cookie auth. Setup takes a few minutes but then it just works.

**t.co expansion is essential.** Without expanding links, you can't categorize. A bookmark of "cool tool https://t.co/abc" is useless until you know what abc points to.

**Separation of concerns works.** X-bookmarks fetches. Capture-triage classifies. Neither needs to know the other's details. Clean interfaces.

**Deduplication prevents noise.** Using tweet ID in the filename makes deduplication trivial. If `x-123456.md` exists, skip it.

**Drop to Inbox, not Ready.** The skill doesn't make routing decisions. It drops raw material. Let the user (via capture-triage) decide what matters.

**Graceful degradation matters.** Article summarization fails sometimes - paywalls, timeouts, blocked domains. The skill still drops the bookmark with a "fetch failed" note. Partial information is better than nothing.

## Decision Log

When we make significant changes, the plan lives in `plans/` and the decision rationale gets archived in `plans/archive/`. That way we remember WHY we did things, not just what we did.
