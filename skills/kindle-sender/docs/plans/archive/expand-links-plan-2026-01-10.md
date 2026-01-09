# Plan: Kindle-Sender Link Expansion

## The Problem

Someday-Maybe.md contains wikilinks like `[[Research Swarm - Topic]]`. On Kindle, these are just text - you can't click them. Ed wants to read the actual research content, not just see references.

## The Solution

Add `--expand-links` flag that includes linked document content in the EPUB.

**Before (current):**
```
Someday-Maybe.md → EPUB with just the file (links are dead text)
```

**After (with --expand-links):**
```
Someday-Maybe.md → Combined EPUB with:
  1. Original content (as table of contents)
  2. Appendix with full content of each linked doc
```

---

## Implementation

### New Function: `expand_wikilinks()`

```python
def expand_wikilinks(md_path: Path, max_depth: int = 1) -> str:
    """
    Read markdown file and expand wikilinks by appending linked content.

    Returns combined markdown with:
    1. Original content (links converted to "see Appendix" notes)
    2. Appendix section with full content of each linked doc

    Only goes one layer deep (no recursive expansion).
    """
```

**Logic:**
1. Read source file content
2. Find all `[[wikilink]]` patterns (any wikilink, not just Research Swarm)
3. For each wikilink:
   - Try to find matching .md file in Zettelkasten
   - If found, read its content
   - Track for appendix
4. Build combined markdown:
   - Original content with links annotated
   - Horizontal rule
   - "## Appendix: Referenced Documents"
   - Each linked doc as a section with its full content

### New CLI Flag

```python
parser.add_argument(
    "--expand-links",
    action="store_true",
    help="Include content of linked documents in the EPUB"
)
```

### Modified `convert_to_epub()`

If `--expand-links` is set:
1. Call `expand_wikilinks()` to get combined markdown
2. Write to temp file
3. Convert temp file to EPUB (instead of original)

---

## File Structure in EPUB

```markdown
# Someday-Maybe

[Original content with wikilinks]

- [[Research Swarm - Topic A]] → (see Appendix)
- [[PROJECT - Email Agent]] → (see Appendix)

---

# Appendix: Referenced Documents

## Research Swarm - Topic A

[Full content of that file...]

---

## PROJECT - Email Agent

[Full content of that file...]
```

---

## Files to Modify

```
skills/kindle-sender/tools/send_to_kindle.py
├── Add: expand_wikilinks() function
├── Add: --expand-links CLI argument
└── Modify: convert_to_epub() to use expanded content when flag is set
```

---

## Edge Cases

1. **Missing linked file** - Skip and note in output (don't fail)
2. **Circular links** - Only go 1 layer deep (no recursion)
3. **Large files** - May hit Kindle size limits, but worth trying
4. **Non-Zettelkasten links** - Skip links that don't resolve to files

---

## Verification

1. Test with Someday-Maybe.md:
   ```bash
   python3 send_to_kindle.py --someday-maybe --expand-links --dry-run
   ```
   Should show which links will be expanded.

2. Test actual send:
   ```bash
   python3 send_to_kindle.py --someday-maybe --expand-links
   ```
   EPUB should contain original + all referenced docs.

3. Check on Kindle that content is readable and navigable.

---

## SKILL.md Update

Add new trigger and usage:
- "Send someday-maybe to Kindle with links expanded"
- `--expand-links` flag documentation
