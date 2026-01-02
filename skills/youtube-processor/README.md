# YouTube Processor Skill

Extracts YouTube transcripts and lets Claude do the summarization. Works across all Claude environments.

## Architecture Decision: Dual Method Approach

This skill intentionally supports **two extraction methods**:

| Method | Environment | How It Works |
|--------|-------------|--------------|
| **Local Python** | Claude Code | Runs `get_transcript.py` directly |
| **API (Vercel)** | Claude.ai, Mac Client | WebFetch to hosted endpoint |

### Why Two Methods?

We considered API-only (simpler, one code path) vs dual approach. We chose dual because:

1. **Robustness** - Local script works if API is down
2. **Speed** - Local is faster (no network round-trip)
3. **Redundancy** - Claude Code users get the best experience, web users still work

### The Tradeoff

- **More complex**: SKILL.md has to explain both methods
- **More to maintain**: Two code paths to keep working
- **Worth it for**: Personal leverage tools where reliability matters

### If You're Refactoring

If simplicity becomes more important than redundancy:
- Delete `tools/` folder and local script references
- Update SKILL.md to only reference the API
- Everything uses WebFetch, one path

## File Structure

```
youtube-processor/
├── api/
│   └── main.py          # FastAPI app (deployed to Vercel)
├── tools/
│   └── get_transcript.py # Local Python script (Claude Code)
├── SKILL.md             # Instructions for Claude
├── vercel.json          # Vercel deployment config
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

## API Endpoint

**Production:** `https://youtube-processor-eight.vercel.app`

| Endpoint | Purpose |
|----------|---------|
| `/` | Usage info |
| `/health` | Health check |
| `/transcript?url=VIDEO_URL` | Extract transcript |

## Deployment

The API is deployed on Vercel (Ed's account). To redeploy:

```bash
cd skills/youtube-processor
npx vercel --prod --yes
```

## Dependencies

- `youtube-transcript-api` - Extracts transcripts (no API key needed)
- `fastapi` - API framework (Vercel deployment only)

---

*Part of Ed's Powerhouse Lab - leverage tools that do the lifting.*
