# YouTube Processor - Technical Reference

## What It Does

Takes YouTube URLs, extracts transcripts via Python script or API, summarizes the content, and outputs Obsidian-ready markdown. Zero friction: share a link, get actionable notes.

## Architecture

```
youtube-processor/
├── SKILL.md              # Main skill definition (extraction + summarization)
├── tools/
│   └── get_transcript.py # Local transcript extraction
└── docs/
    ├── README.md         # This file
    ├── GUIDE.md          # Business-friendly explanation
    ├── ROADMAP.md        # Future ideas
    └── plans/
        └── archive/
```

## Dependencies

**Tools required:**
- `Read` - Load files
- `Bash` - Run Python script (Claude Code)
- `Write` - Save to Zettelkasten
- `Glob` - Find files
- `WebFetch` - API access (Claude.ai)

**Python dependency:**
```bash
pip3 install youtube-transcript-api
```

## Methods by Environment

| Environment | Method |
|-------------|--------|
| Claude Code | Local Python: `python3 get_transcript.py --url "[URL]"` |
| Claude.ai / Mac | API: WebFetch to Vercel endpoint |

## API Endpoint

```
https://youtube-processor-eight.vercel.app/transcript?url=[VIDEO_URL]
```

Returns:
```json
{
  "success": true,
  "video_id": "abc123",
  "transcript": "...",
  "word_count": 850
}
```

## Usage

**Trigger phrases:**
- "Summarize this video: [URL]"
- "Turn this YouTube into notes"
- "What's this video about?"
- "Process this for my newsletter"

**Input:** YouTube URL

**Output:** Summarized notes in Obsidian format

## Summary Modes

| Mode | Output |
|------|--------|
| Quick Summary | Headline, 3-5 bullets, main takeaway |
| Detailed Analysis | Headline, key points with context, action items |
| Newsletter Mining | Hooks, core insight, story beats, angle for LBR |

## Output Location

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YT - [Topic] - YYYY-MM-DD.md
```

## Error Handling

| Error | Meaning |
|-------|---------|
| Transcripts disabled | Creator turned off captions |
| No transcript found | No English captions available |
| Video unavailable | Private, deleted, or age-restricted |

## Testing

**Manual verification:**
1. Run with YouTube URL
2. Verify transcript extracted
3. Check summary quality
4. Confirm Obsidian formatting correct
5. Test save to Zettelkasten
