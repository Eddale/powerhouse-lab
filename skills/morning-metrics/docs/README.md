# Morning Metrics - Technical Reference

## What It Does

Fetches and formats Ed's daily metrics from Gmail and Google Calendar into a scannable morning briefing. Designed to be the metrics component of the win-the-day morning routine.

## Dependencies

**Tools required:** `Read, Bash, WebFetch`

**Python packages:**
- google-auth
- google-auth-oauthlib
- google-api-python-client

**Credentials:**
- `~/.config/claude-code-apis/credentials.json` - OAuth client secrets
- `~/.config/claude-code-apis/token.pickle` - Cached auth token

## Architecture

```
morning-metrics/
├── SKILL.md                    # Instructions for Claude
├── scripts/
│   └── fetch_metrics.py        # Python script that calls Google APIs
├── docs/
│   ├── README.md               # This file
│   ├── GUIDE.md                # Business-friendly explanation
│   └── ROADMAP.md              # Feature history and plans
└── references/
    └── TESTING.md              # Test plan
```

## Data Flow

1. Claude invokes skill via trigger phrase
2. Skill runs `fetch_metrics.py`
3. Script authenticates via OAuth (token.pickle)
4. Script fetches Gmail + Calendar data
5. Script outputs JSON to stdout
6. Claude parses JSON and formats briefing

## API Scopes Used

| Scope | Purpose |
|-------|---------|
| `gmail.readonly` | Read emails and labels |
| `gmail.modify` | Mark as read (future) |
| `calendar.readonly` | List calendars |
| `calendar.events.readonly` | Read event details |

## Usage

**Trigger phrases:**
- "check my metrics"
- "morning metrics"
- "show my stats"
- "what's my day look like"

## Testing

```bash
# Test the Python script directly
python3 skills/morning-metrics/scripts/fetch_metrics.py

# Invoke via Claude
"morning metrics"
```

## Troubleshooting

**"Token expired" error:**
Delete `token.pickle` and re-authenticate:
```bash
rm ~/.config/claude-code-apis/token.pickle
python3 skills/morning-metrics/scripts/fetch_metrics.py
```

**"Credentials not found":**
Ensure environment variables are set:
```bash
export GOOGLE_CREDENTIALS_PATH="$HOME/.config/claude-code-apis/credentials.json"
export GOOGLE_TOKEN_PATH="$HOME/.config/claude-code-apis/token.pickle"
```
