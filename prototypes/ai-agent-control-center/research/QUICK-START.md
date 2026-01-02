# YouTube Transcript Extraction - Quick Start

Get YouTube transcripts in 60 seconds.

---

## Installation

```bash
# Install the recommended library
pip install youtube-transcript-api

# Optional: Install fallback method
pip install yt-dlp
```

---

## Simplest Use Case

```python
from youtube_transcript_api import YouTubeTranscriptApi

# Extract transcript
transcript = YouTubeTranscriptApi.get_transcript("dQw4w9WgXcQ")

# Print it
for line in transcript:
    print(line['text'])
```

---

## Production-Ready Code

Use the included `youtube_transcript_extractor.py`:

```python
from youtube_transcript_extractor import extract_transcript

# Extract transcript
result = extract_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if result['success']:
    print(result['transcript'])
    print(f"Words: {result['word_count']}")
else:
    print(f"Error: {result['error']}")
```

---

## Command Line Usage

```bash
# Run the extractor directly
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Saves transcript to file automatically
```

---

## For AI Agent Integration

```python
from youtube_transcript_extractor import TranscriptExtractor

# Create reusable extractor with caching
extractor = TranscriptExtractor(cache_enabled=True)

# Extract transcript (cached for repeated requests)
result = extractor.extract("https://www.youtube.com/watch?v=VIDEO_ID")

if result['success']:
    # Send to AI agent
    prompt = f"Summarize this video:\n\n{result['transcript']}"
    # ... send to Claude/GPT/etc
```

---

## Bulk Extraction

```python
from youtube_transcript_extractor import TranscriptExtractor

extractor = TranscriptExtractor()

video_urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3",
]

# Extract all (with rate limiting)
results = extractor.bulk_extract(
    video_urls,
    rate_limit_delay=2.0,  # 2 seconds between requests
    progress_callback=lambda current, total: print(f"{current}/{total}")
)

# Filter successful extractions
successful = [r for r in results if r['success']]
print(f"Extracted {len(successful)}/{len(video_urls)} transcripts")
```

---

## Error Handling

```python
from youtube_transcript_extractor import extract_transcript

result = extract_transcript(video_url)

if not result['success']:
    error = result['error']

    if 'disabled' in error.lower():
        print("Transcripts disabled by video owner")
    elif 'not found' in error.lower():
        print("No transcript available")
    elif 'unavailable' in error.lower():
        print("Video doesn't exist or is private")
    else:
        print(f"Unknown error: {error}")
```

---

## Common Video URL Formats (All Work)

```python
# All these formats are supported:
extract_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
extract_transcript("https://youtu.be/dQw4w9WgXcQ")
extract_transcript("https://www.youtube.com/embed/dQw4w9WgXcQ")
extract_transcript("dQw4w9WgXcQ")  # Just the ID
```

---

## Test It Now

```bash
# Test with the included test script
python test-transcript-methods.py

# Or test a specific video
python test-transcript-methods.py "https://www.youtube.com/watch?v=YOUR_VIDEO"
```

---

## Next Steps

1. Read `youtube-transcript-extraction.md` for full documentation
2. Review `youtube_transcript_extractor.py` for implementation details
3. Check `test-transcript-methods.py` to see comparison of methods

---

## Pro Tips

**For AI agents:**
- Use caching to avoid re-fetching the same video
- Add rate limiting (1-2 seconds delay) for bulk operations
- Handle errors gracefully - not all videos have transcripts

**For production:**
- Use `youtube-transcript-api` as primary method
- Add `yt-dlp` as fallback for critical applications
- Consider the official YouTube Data API for guaranteed uptime (requires auth)

**For scale:**
- Implement exponential backoff if you hit rate limits
- Cache results in Redis or similar for multi-agent systems
- Monitor for API changes (subscribe to library GitHub repos)

---

**Questions?** Check the full research doc: `youtube-transcript-extraction.md`
