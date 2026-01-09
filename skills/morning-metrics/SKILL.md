---
name: morning-metrics
description: Pull daily metrics briefing from Gmail, Calendar, and Substack. Use when "check my metrics", "morning metrics", "show my stats", "what's my day look like".
allowed-tools: Read, Bash, WebFetch
---

# Morning Metrics

## What This Does

Pulls Ed's daily metrics from multiple sources and presents a clean morning briefing:
- **Gmail:** Unread count, action-required emails
- **Calendar:** Today's meetings and schedule
- **Substack:** Subscriber stats (via browser if needed)

## Instructions

### Step 1: Load Google API Credentials

Run the metrics script to get Gmail and Calendar data:

```bash
python3 /Users/eddale/Documents/GitHub/powerhouse-lab/skills/morning-metrics/scripts/fetch_metrics.py
```

Parse the JSON output for the briefing.

### Step 2: Format the Briefing

Present metrics in this format:

```markdown
## Morning Metrics - [Today's Date]

### Calendar
**Today's meetings:** [count]
| Time | Event |
|------|-------|
| [time] | [event name] |

### Email (tedlegend@gmail.com)
- **Unread:** [count]
- **Action required:** [count if available]

### Substack (if available)
- **Subscribers:** [count]
- **Recent growth:** [trend]
```

### Step 3: Surface Action Items

After the briefing, note any:
- Meetings in the next 2 hours
- High-priority emails needing response
- Unusual metrics (spikes or drops)

## Configuration

**Credentials location:**
- `~/.config/claude-code-apis/credentials.json`
- `~/.config/claude-code-apis/token.pickle`

**Environment variables:**
- `GOOGLE_CREDENTIALS_PATH`
- `GOOGLE_TOKEN_PATH`

## Examples

**Input:** "morning metrics"

**Output:**
```
## Morning Metrics - January 10, 2026

### Calendar
**Today's meetings:** 2
| Time | Event |
|------|-------|
| 9:30 AM | ED And AM Weekly Biz CatchUp |
| 3:00 PM | 100x Founder Workshop |

### Email (tedlegend@gmail.com)
- **Unread:** 201
- **Primary inbox:** 45 unread

No urgent items requiring immediate attention.
```

## Guidelines

- Keep the briefing scannable (30 seconds to read)
- Highlight anything unusual or time-sensitive
- Don't overwhelm with data - focus on actionable info
- If APIs fail, report gracefully and suggest fixes
