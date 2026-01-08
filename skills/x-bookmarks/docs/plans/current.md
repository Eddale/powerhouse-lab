# Plan: Article Summarization

**Feature:** Automatically summarize articles before dropping to Inbox
**Status:** Draft - awaiting approval
**Created:** 2026-01-08

## The Problem

Currently, bookmarked articles land in Inbox with just a title and link. Ed still has to click through and read to know if they're worth keeping. That's friction.

## The Vision

When x-bookmarks detects an article URL, it fetches the content and generates a summary. The bookmark arrives in Inbox ready to triage - you know what it says without clicking.

## Proposed Flow

```
Current:
bookmark → expand t.co → detect "article" → write title + link → Inbox

New:
bookmark → expand t.co → detect "article" → fetch content → summarize → write with summary → Inbox
```

## Implementation

### Step 1: Detect Article Type

Already done. Current skill categorizes `link_type: article` for:
- medium.com
- substack.com
- Blog patterns
- General article URLs

### Step 2: Fetch Article Content

For `article` type bookmarks, add after categorization:

```
Use WebFetch to retrieve article content:
WebFetch(url: "[expanded URL]", prompt: "Extract the main article content, ignoring navigation, ads, and sidebars")
```

### Step 3: Generate Summary

Process the fetched content:

```
Summarize in this format:
- **TL;DR:** One sentence core takeaway
- **Key Points:** 3-5 bullet points
- **Why It Matters:** One sentence on relevance/application
```

### Step 4: Enhanced File Format

Update the markdown output:

```markdown
---
source: x-bookmark
author: @username
tweet_url: https://x.com/user/status/123
captured: YYYY-MM-DD
link_type: article
article_title: "The Actual Article Title"
article_source: medium.com
---

{Tweet text}

**Linked:** [Article Title](expanded_url)

## Summary

**TL;DR:** One sentence core takeaway.

**Key Points:**
- Point one
- Point two
- Point three

**Why It Matters:** Relevance to Ed's work.

---
*Auto-summarized by x-bookmarks*
```

## Open Questions

Need Ed's input on these:

### 1. Opt-in or Default?
- **Option A:** Summarize all articles automatically (slower, more useful)
- **Option B:** Opt-in flag like "fetch bookmarks with summaries" (faster default, option for depth)

### 2. Paywall Handling
- **Option A:** Skip summarization for paywalled content, note "paywall detected"
- **Option B:** Summarize whatever WebFetch can retrieve (may be partial)

### 3. Summary Length
- **Option A:** Brief (TL;DR + 3 bullets) - faster triage
- **Option B:** Comprehensive (TL;DR + 5-7 bullets + context) - more info upfront

### 4. Error Behavior
When article fetch fails:
- **Option A:** Still drop to Inbox without summary, note "fetch failed"
- **Option B:** Skip entirely, report as error

## Risks

| Risk | Mitigation |
|------|------------|
| Slow processing | Parallel fetches where possible |
| Rate limiting | Add delay between fetches if needed |
| Bad summaries | Review first batch, tune prompt |
| Paywalled content | Detect and handle gracefully |

## Success Criteria

- [ ] Articles arrive with useful summaries
- [ ] Triage time reduced (Ed knows what's worth keeping faster)
- [ ] No broken bookmarks from fetch failures
- [ ] Processing time stays reasonable (<2 min for 20 bookmarks)

## Files to Modify

1. `skills/x-bookmarks/SKILL.md` - Add summarization step to instructions
2. `skills/x-bookmarks/docs/README.md` - Update architecture docs
3. `skills/x-bookmarks/docs/ROADMAP.md` - Move from Ideas to Shipped

## Rollout

1. Ed approves plan
2. Implement changes to SKILL.md
3. Test with real bookmarks
4. Verify summaries are useful
5. Update docs, archive plan, commit
