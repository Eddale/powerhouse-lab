# Research Swarm: Markdown to Kindle Workflow for Obsidian Vault

**Research Date:** 2026-01-09
**Angles Investigated:** Direct Send-to-Kindle, Conversion Tools, Obsidian Plugins, Automation/Scripting, Quality/Formatting

---

## Executive Summary

The ideal workflow for sending Obsidian markdown to Kindle is: **Pandoc + Send-to-Kindle Email**. Amazon doesn't accept markdown directly, so you need a conversion step. The best path is Markdown -> EPUB -> Kindle email. For Ed's use case ("send all research documents linked in my daily note to Kindle"), a Python script using pypandoc + smtplib is the winning approach - fully automatable by Claude Code.

**Key discovery:** Amazon now accepts EPUB natively via Send-to-Kindle (no more MOBI needed). Starting January 2026, Kindle is also allowing DRM-free EPUB downloads, signaling a major shift toward EPUB as the standard format.

---

## Angle 1: Direct Send-to-Kindle Approaches

### What Amazon Accepts

**Supported formats:** PDF, DOC, DOCX, TXT, RTF, HTM, HTML, PNG, GIF, JPG, JPEG, BMP, EPUB

**Notably absent:** Markdown (.md) is NOT supported directly.

### Send-to-Kindle Methods

1. **Email** - Send to your `[name]@kindle.com` address
   - Subject line "Convert" forces conversion to Kindle format (enables font resizing, notes)
   - Max 50 MB per email (200 MB via app)
   - Must whitelist sender email address

2. **Browser Extension** - Good for web articles, not local files

3. **Desktop/Mobile App** - Drag and drop files

### Recent Changes (2025-2026)

- **April 2025:** Only complete email addresses work (no domain wildcards)
- **November 2023:** MOBI support ended for new uploads
- **January 2026:** Amazon allowing DRM-free EPUB downloads from purchased books

### Verdict for Ed

Email is the automation-friendly option. The workflow must convert Markdown -> EPUB first, then email the EPUB.

**Sources:**
- [Amazon Send to Kindle Help](https://www.amazon.com/gp/help/customer/display.html?nodeId=G7NECT4B4ZWHQ8WV)
- [Send to Kindle Email](https://www.amazon.com/sendtokindle/email)
- [Good e-Reader: Amazon Changes](https://goodereader.com/blog/kindle/amazon-is-making-massive-changes-to-send-to-kindle)

---

## Angle 2: Markdown to EPUB/MOBI Conversion Tools

### Pandoc (The Gold Standard)

**Strengths:**
- Handles most markdown variants well
- Native EPUB3 output
- Extensible via Lua filters (critical for Obsidian callouts)
- Command line = scriptable

**Obsidian-Specific Support:**
- Pandoc 3.0+ has wikilinks extensions: `wikilinks_title_after_pipe` and `wikilinks_title_before_pipe`
- Image wikilinks (`![[image.png]]`) require Lua filter or pre-processing
- Callouts need Lua filter (see zsviczian's `export.lua`)

**Basic usage:**
```bash
pandoc input.md -o output.epub --metadata title="My Notes"
```

**With callout support:**
```bash
pandoc input.md -o output.epub --lua-filter callout.lua
```

### Calibre's ebook-convert

**Strengths:**
- Supports markdown with extensions: footnotes, tables, toc, wikilinks, admonition
- Can convert EPUB -> MOBI (legacy support)
- Powerful metadata editing

**macOS path:**
```bash
/Applications/calibre.app/Contents/MacOS/ebook-convert input.md output.epub
```

**Markdown extensions available:** abbr, admonition, attr_list, codehilite, def_list, fenced_code, footnotes, meta, tables, toc, wikilinks

### obsipub (Obsidian-Specific)

A Python tool purpose-built for Obsidian vaults:

**Strengths:**
- Handles wikilinks natively
- Preserves folder structure as chapters
- Embeds attachments automatically
- Excludes .obsidian, .git, .trash

**Installation:**
```bash
pip install obsipub
brew install pandoc  # dependency
```

**Usage:**
```bash
obsipub /path/to/vault output.epub --title "My Research" --author "Ed Dale"
```

**Python API:**
```python
from obsipub import ObsidianToEpubConverter

converter = ObsidianToEpubConverter(
    vault_path="/path/to/vault",
    output_epub_path="output.epub",
    title="My Research",
    include_attachments=True
)
converter.convert()
```

### Recommendation

For single files: **Pandoc** with Lua filters
For vault exports: **obsipub**
For Kindle specifically: Either, since EPUB is now native

**Sources:**
- [Pandoc EPUB Documentation](https://pandoc.org/epub.html)
- [Calibre ebook-convert](https://manual.calibre-ebook.com/generated/en/ebook-convert.html)
- [obsipub GitHub](https://github.com/tcsenpai/obsipub)
- [zsviczian Publishing Workflow](https://gist.github.com/zsviczian/db6c41d3698b13ed78f8e4f226706113)

---

## Angle 3: Obsidian-Specific Solutions

### obsidian-kindle-export Plugin

**What it does:** Exports notes + embedded images to EPUB, sends via email to Kindle

**How it works:**
1. Collects all embedded files and markdown
2. Sends to PHP backend (public or self-hosted)
3. Backend converts to EPUB
4. Emails to your Kindle address

**Features:**
- Image embedding
- Table of contents generation
- Footnote support
- Highlight syntax (`==text==`)
- "Mergedown" feature (combines embedded files)

**Limitations:**
- Requires sending data to external server (privacy concern)
- Self-hosting requires PHP server setup
- No batch processing of multiple notes

**Plugin URL:** [obsidian-kindle-export](https://github.com/SimeonLukas/obsidian-kindle-export)

### Obsidian Pandoc Plugin

Adds command palette options to export to EPUB, PDF, DOCX, HTML, etc. Uses local Pandoc installation.

**Good for:** One-off exports from within Obsidian
**Not for:** Batch processing or automation

**Plugin URL:** [obsidian-pandoc](https://github.com/OliverBalfour/obsidian-pandoc)

### Handling Obsidian Syntax

| Syntax | Solution |
|--------|----------|
| Wikilinks `[[note]]` | Pandoc wikilinks extension or obsipub |
| Image wikilinks `![[img.png]]` | Lua filter or obsidian-link-converter plugin first |
| Callouts `> [!note]` | zsviczian's export.lua filter |
| Embeds `![[note]]` | Templater script to flatten, or obsipub |
| Tags `#tag` | obsipub `--include-tags` or strip with sed |

### The zsviczian Workflow (Most Complete)

A Templater script + Lua filter + CSS combination that:
1. Expands all embeds recursively
2. Converts callouts to styled divs
3. Applies custom typography
4. Generates EPUB via Pandoc
5. Optionally converts to PDF via Calibre

**Best for:** Book-length projects
**Complexity:** High (requires Templater, custom Lua, CSS knowledge)

**Source:** [Publishing Workflow Gist](https://gist.github.com/zsviczian/db6c41d3698b13ed78f8e4f226706113)

---

## Angle 4: Automation/Scripting Approaches

### The Winning Script (Python)

For Ed's use case: "Send all research documents linked in daily note to Kindle"

**Components:**
1. **pypandoc** - Python wrapper for Pandoc
2. **smtplib** - Send email with attachment
3. **re** - Parse daily note for linked documents

**Installation:**
```bash
pip install pypandoc pypandoc_binary
# pypandoc_binary includes Pandoc - no separate install needed
```

**Script Architecture:**

```python
import pypandoc
import smtplib
import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Configuration
ZETTELKASTEN_PATH = "/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten"
KINDLE_EMAIL = "your_kindle_name@kindle.com"
SENDER_EMAIL = "your_gmail@gmail.com"
SENDER_PASSWORD = "app_specific_password"  # Use env var in production

def extract_linked_docs(daily_note_path: str) -> list[str]:
    """Extract wikilinks from Captures section of daily note"""
    with open(daily_note_path, 'r') as f:
        content = f.read()

    # Find Research Swarm links
    pattern = r'\[\[Research Swarm - .+?\]\]'
    matches = re.findall(pattern, content)
    return [m.strip('[]') for m in matches]

def convert_to_epub(md_path: str, output_path: str) -> str:
    """Convert markdown to EPUB using Pandoc"""
    title = Path(md_path).stem
    pypandoc.convert_file(
        md_path,
        'epub',
        outputfile=output_path,
        extra_args=['--metadata', f'title={title}']
    )
    return output_path

def send_to_kindle(epub_path: str):
    """Email EPUB to Kindle address"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = KINDLE_EMAIL
    msg['Subject'] = 'Convert'  # Forces Kindle format conversion

    # Attach EPUB
    with open(epub_path, 'rb') as f:
        part = MIMEBase('application', 'epub+zip')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                       f'attachment; filename="{Path(epub_path).name}"')
        msg.attach(part)

    # Send via Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def main(daily_note_path: str):
    """Main workflow: parse daily note -> convert -> send"""
    docs = extract_linked_docs(daily_note_path)

    for doc_name in docs:
        md_path = os.path.join(ZETTELKASTEN_PATH, f"{doc_name}.md")
        epub_path = f"/tmp/{doc_name}.epub"

        if os.path.exists(md_path):
            print(f"Converting: {doc_name}")
            convert_to_epub(md_path, epub_path)

            print(f"Sending to Kindle: {doc_name}")
            send_to_kindle(epub_path)

            os.remove(epub_path)  # Cleanup
            print(f"Done: {doc_name}")

if __name__ == "__main__":
    today = "2026-01-09"
    daily_note = os.path.join(ZETTELKASTEN_PATH, f"{today}.md")
    main(daily_note)
```

### Mac Shortcuts/Automator Option

Less flexible but possible:
1. Automator workflow to run shell script
2. Shell script calls pandoc + sendmail
3. Trigger via folder action or keyboard shortcut

**Limitation:** Automator can't easily parse Obsidian links; better for "send this specific file" vs. "send files linked in daily note"

### Claude Code Automation

Claude Code can:
1. Read Ed's daily note
2. Parse linked Research Swarm documents
3. Run pandoc via Bash
4. Construct and send email via Python

**Trigger phrase:** "Send today's research to Kindle"

**Sources:**
- [pypandoc Documentation](https://github.com/JessicaTegner/pypandoc)
- [Python Send Email with Gmail](https://mailtrap.io/blog/python-send-email-gmail/)
- [Real Python: Sending Emails](https://realpython.com/python-send-email/)

---

## Angle 5: Quality and Formatting Considerations

### Typography on Kindle

**Enhanced Typesetting (Automatic):**
- Kindle applies to all reflowable EPUB uploads
- Improved kerning, ligatures, hyphenation
- Bookerly font optimized for e-ink

**Best Practices:**
- Let body text use defaults (don't override fonts)
- Style headings explicitly (`text-align: left` or `center`)
- Sans-serif for headings, serif for body

### Headers and Structure

- H1 = Chapter titles
- H2 = Section headers
- H3 = Subsections
- Kindle auto-generates Table of Contents from headers

**Tip:** Always left-align headings in CSS to prevent word spacing issues:
```css
h1, h2, h3 { text-align: left; }
```

### Tables on Kindle

**Do:**
- Use HTML `<table>` markup (Pandoc handles this)
- Keep tables simple
- Avoid nested tables (Enhanced Typesetting doesn't support)

**Don't:**
- Render tables as images
- Use complex multi-column layouts

**Enhanced Typesetting Features:**
- Smart table layout for different screen sizes
- Pan and zoom for larger tables
- Selectable text in tables

### Images

- Embed images in EPUB (Pandoc does this automatically)
- Keep image sizes reasonable (< 1MB each)
- Use `--no-attachments` in obsipub if file size balloons

### Dark Mode Compatibility

- Kindle's dark mode inverts text and background automatically
- Images may look odd inverted
- PDFs flash white on page turn in dark mode
- EPUBs handle dark mode better than PDFs

**Devices with Dark Mode:** Kindle Paperwhite (2021+), Kindle Oasis 2/3
**Coming 2026:** Kindle Scribe Colorsoft dark mode

### Code Blocks

- Pandoc preserves code blocks in EPUB
- Kindle renders them in monospace
- Long lines may wrap awkwardly on narrow e-ink screens
- Consider using fenced code blocks with language hints

**Sources:**
- [Kindle Enhanced Typesetting](https://kdp.amazon.com/en_US/help/topic/G202087570)
- [KDP Table Guidelines](https://kdp.amazon.com/en_US/help/topic/GZ8BAXASXKB5JVML)
- [Kindle Dark Mode Help](https://www.amazon.com/gp/help/customer/display.html?nodeId=TZRTRCyYYbxMsMHDu8)
- [Good e-Reader Dark Mode Guide](https://goodereader.com/blog/kindle/everything-you-need-to-know-about-dark-mode-on-the-kindle)

---

## Recommendations for Ed

### Quick Win (Today)

1. Install obsipub: `pip install obsipub && brew install pandoc`
2. Test with one research doc:
   ```bash
   obsipub "/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Research Swarm - Some Topic.md" test.epub --title "Research"
   ```
3. Email test.epub to your Kindle address manually

### Medium-Term (This Week)

Build the Python skill script that:
- Parses daily note for Research Swarm links
- Converts each to EPUB via pypandoc
- Emails to Kindle automatically

I can build this as a `/skills/kindle-sender/` skill.

### Ideal Workflow

"Send my research to Kindle" ->

1. Claude reads today's daily note
2. Extracts `[[Research Swarm - *]]` links from Captures
3. Converts each to EPUB
4. Sends to Ed's Kindle email
5. Confirms: "Sent 3 documents to Kindle"

### Tools to Install

| Tool | Purpose | Install |
|------|---------|---------|
| Pandoc | Markdown -> EPUB conversion | `brew install pandoc` |
| pypandoc | Python wrapper | `pip install pypandoc` |
| obsipub | Obsidian-aware converter | `pip install obsipub` |

### Configuration Needed

1. Find your Kindle email: Amazon account -> Manage Content & Devices -> Preferences -> Personal Document Settings
2. Whitelist your sending email address in same location
3. Create Gmail app password (if using Gmail): Google Account -> Security -> 2FA -> App Passwords

---

## Comparison Matrix

| Approach | Setup Effort | Daily Use | Format Quality | Automation |
|----------|--------------|-----------|----------------|------------|
| Manual Pandoc + Email | Low | Medium | Excellent | Medium |
| obsipub + Email | Low | Easy | Good | High |
| Kindle Export Plugin | Low | Easy | Good | Low (no batch) |
| zsviczian Workflow | High | Easy | Excellent | High |
| Python Skill (Custom) | Medium | One command | Excellent | Full |

**Winner for Ed:** Custom Python skill using pypandoc. One-time setup, then "send to Kindle" becomes a single command.

---

## Open Questions

1. **Callout handling:** Does Ed want callouts preserved as styled boxes, or is plain text fine?
2. **Image handling:** Do research docs contain images that need to go to Kindle?
3. **Batch size:** How many documents typically need sending at once?
4. **Gmail vs other:** Which email service for sending?

---

## Next Steps

1. Ed confirms desired workflow (automated vs. manual)
2. Build `/skills/kindle-sender/` skill with:
   - `tools/send_to_kindle.py` - Core conversion + email logic
   - `SKILL.md` - Instructions for Claude Code
3. Test with a real research document
4. Document in skill GUIDE.md

---

*Generated by Research Swarm on 2026-01-09*
