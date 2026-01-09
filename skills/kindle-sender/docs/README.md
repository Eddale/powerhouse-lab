# Kindle Sender - Technical Reference

## What It Does

Converts markdown documents from Zettelkasten to EPUB and emails them to your Kindle.
Amazon's Send-to-Kindle service converts EPUB to proper Kindle format automatically.

## Dependencies

**Tools required:**
- Read - Load daily notes and markdown files
- Bash - Run Python conversion script
- Glob - Find files in Zettelkasten
- Write - (reserved for future logging)
- AskUserQuestion - Confirm before sending

**Python dependencies:**
```bash
pip3 install pypandoc pypandoc_binary
```

**System dependencies:**
- pandoc (included via pypandoc_binary, or install separately via `brew install pandoc`)

## Environment Variables

```bash
export KINDLE_EMAIL="your-name@kindle.com"
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

## Usage

**Trigger phrases:**
- "Send my research to Kindle"
- "Send today's research to Kindle"
- "Send someday-maybe to Kindle"
- "Kindle my research"

**CLI usage:**
```bash
cd skills/kindle-sender/tools

# From daily note
python3 send_to_kindle.py --daily-note "2026-01-10" --dry-run
python3 send_to_kindle.py --daily-note "2026-01-10"

# Someday-Maybe backlog
python3 send_to_kindle.py --someday-maybe --dry-run
python3 send_to_kindle.py --someday-maybe

# Someday-Maybe with linked documents expanded (includes full research content)
python3 send_to_kindle.py --someday-maybe --expand-links --dry-run
python3 send_to_kindle.py --someday-maybe --expand-links

# Specific files
python3 send_to_kindle.py --files "Research Swarm - Topic.md"

# Specific files with links expanded
python3 send_to_kindle.py --files "Someday-Maybe" --expand-links
```

## How It Works

1. **Parse daily note** - Extracts `[[Research Swarm - *]]` wikilinks from Captures section
2. **Find files** - Locates corresponding .md files in Zettelkasten
3. **Expand links (optional)** - If `--expand-links` flag is set:
   - Finds all `[[wikilinks]]` in the document
   - Loads content of each linked file
   - Annotates original links with "(see Appendix)"
   - Appends full content of linked docs as an appendix
4. **Convert to EPUB** - Uses pypandoc (Pandoc wrapper) with metadata
5. **Email to Kindle** - SMTP via Gmail with "Convert" subject line
6. **Amazon converts** - Send-to-Kindle service converts EPUB to Kindle format

## Testing

1. **Verify environment:**
   ```bash
   echo $KINDLE_EMAIL $GMAIL_USER
   # Should show your addresses
   ```

2. **Dry run:**
   ```bash
   python3 send_to_kindle.py --daily-note "2026-01-10" --dry-run
   ```

3. **Send single test file:**
   ```bash
   python3 send_to_kindle.py --files "Someday-Maybe" --dry-run
   python3 send_to_kindle.py --files "Someday-Maybe"
   ```

4. **Check Kindle library** - Document should appear within 1-5 minutes

## Error Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Partial failure (some docs failed) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing environment variables" | Add to ~/.zshrc, run `source ~/.zshrc` |
| "Gmail authentication failed" | Use App Password, not regular password |
| "File not found" | Check filename matches exactly |
| "pypandoc not found" | `pip3 install pypandoc pypandoc_binary` |
| "Document not on Kindle" | Check sender whitelisted in Amazon settings |
