# Plan: Internal Navigation Links in Expanded EPUBs

## The Problem

Currently, `--expand-links` annotates wikilinks with "(see Appendix)" but you can't tap them to jump there. On Kindle, you have to scroll through the whole document to find the research you want.

## The Solution

Add HTML anchor links so tapping a reference jumps directly to that section in the appendix.

**Before:**
```
**Research Swarm - Topic** _(see Appendix)_
```

**After:**
```markdown
[Research Swarm - Topic](#research-swarm-topic)
```

Which renders as a tappable link that jumps to the appendix section.

---

## Implementation

### Changes to `expand_wikilinks()`

1. **Generate anchor IDs** from document names:
   ```python
   def slugify(name: str) -> str:
       """Convert doc name to URL-safe anchor ID."""
       # "Research Swarm - Topic Name" → "research-swarm-topic-name"
       return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
   ```

2. **Update link annotation** to use markdown links with arrow hint:
   ```python
   # Before:
   return f"**{link_name}** _(see Appendix)_"

   # After:
   anchor_id = slugify(link_name)
   return f"[{link_name} ↓](#{anchor_id})"
   ```

3. **Add anchor ID to main content** for "back to top" navigation:
   ```python
   # Wrap original content with a top anchor
   annotated_content = f'<div id="top"></div>\n\n{annotated_content}'
   ```

4. **Add anchor IDs to appendix headers + back link**:
   ```python
   # Before:
   appendix_sections.append(f"\n\n---\n\n## {doc_name}\n\n{doc_content}")

   # After:
   anchor_id = slugify(doc_name)
   back_link = "\n\n[↑ Back to index](#top)"
   appendix_sections.append(f"\n\n---\n\n## {doc_name} {{#{anchor_id}}}\n\n{doc_content}{back_link}")
   ```

   Note: The `{#anchor-id}` syntax is Pandoc's attribute syntax for adding IDs to headers.

---

## Pandoc Anchor Syntax

Pandoc supports header attributes:
```markdown
## Section Title {#custom-id}
```

This generates:
```html
<h2 id="custom-id">Section Title</h2>
```

The markdown link `[text](#custom-id)` then navigates to it.

---

## Decisions

1. **Link text style** - Arrow hint to make it clear there's attached content:
   ```
   [Research Swarm - Topic ↓](#research-swarm-topic)
   ```
   The ↓ signals "jump down to this chapter"

2. **"Back to top" links** - Yes, add at the end of each appendix section:
   ```
   [↑ Back to index](#top)
   ```
   Makes it easy to return to Someday-Maybe and pick the next thing to read.

---

## Files to Modify

```
skills/kindle-sender/tools/send_to_kindle.py
├── Add: slugify() helper function
├── Modify: expand_wikilinks() - add top anchor to main content
├── Modify: expand_wikilinks() - link annotation with ↓ arrow
├── Modify: expand_wikilinks() - appendix headers with {#id} anchors
└── Modify: expand_wikilinks() - add "↑ Back to index" after each section
```

---

## Testing

1. Dry run to see the generated markdown:
   ```bash
   python3 send_to_kindle.py --someday-maybe --expand-links --dry-run
   ```

2. Could add a `--preview` flag that saves the combined markdown to a file for inspection before sending.

3. Send to Kindle, verify links are tappable and jump correctly.

---

## Verification Approach

Before sending to Kindle, I could:
1. Save the combined markdown to a temp file
2. Show you a snippet of how the links look
3. Confirm the anchor syntax is correct

This way we verify the format before the 5-minute Kindle delivery wait.
