---
name: kindle-sender
description: Send Research Swarm documents to Kindle. Use when "send to Kindle", "send research to Kindle", "send someday-maybe to Kindle", "Kindle my research".
allowed-tools: Read, Bash, Glob, Write, AskUserQuestion
---

# Kindle Sender

## What This Does

Converts markdown documents from your Zettelkasten to EPUB and emails them to your Kindle for offline reading.

**Two modes:**
1. **Research mode** - Send all Research Swarm docs linked in today's daily note
2. **Review mode** - Send your Someday-Maybe.md backlog for Kindle review

## When to Use

- "Send my research to Kindle"
- "Send today's research to Kindle"
- "Send someday-maybe to Kindle"
- "Kindle my research"

## Prerequisites (One-Time Setup)

Before first use, configure these environment variables in `~/.zshrc`:

```bash
export KINDLE_EMAIL="your-name@kindle.com"
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

**Setup steps:**

1. **Find your Kindle email:**
   - Go to [Amazon → Manage Content & Devices](https://www.amazon.com/hz/mycd/digital-console/contentlist/pdocs)
   - Click "Preferences" tab
   - Look for "Personal Document Settings"
   - Your Kindle email ends in `@kindle.com`

2. **Whitelist your sender email:**
   - Same page, under "Approved Personal Document E-mail List"
   - Add your Gmail address

3. **Create Gmail app password:**
   - Go to [Google Account → Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification if not already
   - Go to "App passwords" (search for it)
   - Create a new app password for "Mail"
   - Use this password, NOT your regular Gmail password

4. **Install Python dependency:**
   ```bash
   pip3 install pypandoc pypandoc_binary
   ```

5. **Reload shell:**
   ```bash
   source ~/.zshrc
   ```

## Instructions

### For "Send my research to Kindle"

1. **Find today's daily note:**
   ```
   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
   ```

2. **Extract Research Swarm links from Captures section:**
   Look for wikilinks matching `[[Research Swarm - *]]` pattern.

3. **Run the sender script in dry-run mode first:**
   ```bash
   cd /Users/eddale/Documents/GitHub/powerhouse-lab/skills/kindle-sender/tools
   python3 send_to_kindle.py --daily-note "YYYY-MM-DD" --dry-run
   ```

4. **Show the user what will be sent:**
   Display the list of documents found.

5. **Ask for confirmation:**
   Use AskUserQuestion: "Send these X documents to Kindle?"

6. **If confirmed, run without dry-run:**
   ```bash
   python3 send_to_kindle.py --daily-note "YYYY-MM-DD"
   ```

7. **Report results:**
   "Sent X documents to your Kindle. They should arrive within a few minutes."

### For "Send someday-maybe to Kindle"

1. **Run the sender script with someday-maybe flag:**
   ```bash
   cd /Users/eddale/Documents/GitHub/powerhouse-lab/skills/kindle-sender/tools
   python3 send_to_kindle.py --someday-maybe --dry-run
   ```

2. **Show preview and ask for confirmation.**

3. **If confirmed, send:**
   ```bash
   python3 send_to_kindle.py --someday-maybe
   ```

### For specific files

User can also request specific files:
```bash
python3 send_to_kindle.py --files "Research Swarm - Topic.md" "Another Doc.md"
```

## Script Options

| Flag | Description |
|------|-------------|
| `--daily-note YYYY-MM-DD` | Send Research Swarm docs from that day's note |
| `--someday-maybe` | Send the Someday-Maybe.md file |
| `--files FILE1 FILE2...` | Send specific markdown files |
| `--dry-run` | Show what would be sent without sending |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "KINDLE_EMAIL not set" | Add to ~/.zshrc and run `source ~/.zshrc` |
| "Authentication failed" | Use app password, not regular Gmail password |
| "Document not delivered" | Check sender is whitelisted in Amazon settings |
| "pypandoc not found" | Run `pip3 install pypandoc pypandoc_binary` |

## Examples

**Example 1: Morning research review**
```
User: Send my research to Kindle
Claude: Found 3 Research Swarm documents in today's Captures:
  1. Research Swarm - Markdown to Kindle Workflow - 2026-01-09.md
  2. Research Swarm - API Design Patterns - 2026-01-09.md
  3. Research Swarm - Newsletter Growth - 2026-01-09.md

  Send these to your Kindle?
User: Yes
Claude: Sent 3 documents to your Kindle. They should arrive within a few minutes.
```

**Example 2: Review backlog**
```
User: Send someday-maybe to Kindle
Claude: Will send Someday-Maybe.md (your parked projects and tasks backlog).
  Send to Kindle?
User: Yes
Claude: Sent Someday-Maybe.md to your Kindle.
```
