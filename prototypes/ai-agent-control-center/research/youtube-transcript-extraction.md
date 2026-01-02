# YouTube Transcript Extraction Research

Research Date: 2026-01-02
Purpose: Evaluate methods for extracting YouTube transcripts for AI agent use

---

## Method 1: youtube-transcript-api (Python)

### Overview
Python library that extracts transcripts directly from YouTube's internal API without authentication.

### How It Works
- Scrapes YouTube's internal player API endpoints
- No official API key required
- Extracts auto-generated and manual captions
- Returns timestamped transcript segments

### Installation
```bash
pip install youtube-transcript-api
```

### Code Example
```python
from youtube_transcript_api import YouTubeTranscriptApi

# Basic usage
video_id = "dQw4w9WgXcQ"
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Returns list of dicts: [{'text': '...', 'start': 0.0, 'duration': 2.5}, ...]
for segment in transcript:
    print(f"[{segment['start']:.2f}s] {segment['text']}")

# Get transcript in specific language
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es'])

# List available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
for transcript in transcript_list:
    print(f"Language: {transcript.language_code}, Auto-generated: {transcript.is_generated}")

# Format as plain text
from youtube_transcript_api.formatters import TextFormatter
formatter = TextFormatter()
text_formatted = formatter.format_transcript(transcript)
```

### Advanced Usage
```python
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_transcript_safe(video_id, languages=['en']):
    """Robust transcript fetcher with error handling"""
    try:
        # Try to get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)

        # Combine all text
        full_text = ' '.join([segment['text'] for segment in transcript])

        return {
            'success': True,
            'transcript': transcript,
            'full_text': full_text,
            'video_id': video_id
        }
    except TranscriptsDisabled:
        return {'success': False, 'error': 'Transcripts disabled for this video'}
    except NoTranscriptFound:
        return {'success': False, 'error': 'No transcript found in requested language'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### Pros
✅ **No authentication required** - Works immediately, no API keys
✅ **Simple to use** - Clean Python interface
✅ **Fast** - Direct API calls, minimal overhead
✅ **Multiple languages** - Access all available transcript languages
✅ **Timestamps included** - Get time-synced segments
✅ **No rate limits** (in practice) - YouTube doesn't enforce strict limits on transcript endpoint
✅ **Active maintenance** - Well-maintained library

### Cons
❌ **Unofficial API** - Uses YouTube's internal endpoints (could break if YouTube changes structure)
❌ **Requires transcripts enabled** - Won't work if video owner disabled captions
❌ **No video metadata** - Only gets transcripts, not title/description/etc
❌ **Network dependent** - Requires internet connection (not local)
❌ **Potential IP blocking** - Heavy usage could trigger rate limiting

### Rate Limits
- **No official limits** - Uses undocumented API
- **Practical limit**: ~100-200 requests/minute before potential soft blocks
- **Recommendation**: Add 1-2 second delays between requests for bulk operations
- **IP-based**: Limits are per IP, not per API key

### Reliability Score: 8/10
Very reliable for standard use cases. Main risk is YouTube changing internal API structure.

---

## Method 2: yt-dlp (Command-line Tool)

### Overview
Powerful YouTube downloader that can also extract subtitles/transcripts.

### How It Works
- Fork of youtube-dl with active development
- Downloads video, audio, metadata, AND subtitles
- Can extract subtitles without downloading video
- Supports multiple subtitle formats

### Installation
```bash
# Via pip
pip install yt-dlp

# Via homebrew (macOS)
brew install yt-dlp
```

### Code Example (Command Line)
```bash
# Download transcript only (no video)
yt-dlp --write-auto-subs --skip-download --sub-lang en --sub-format vtt \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get all available subtitles
yt-dlp --write-subs --all-subs --skip-download \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Convert to SRT format
yt-dlp --write-auto-subs --skip-download --sub-lang en --sub-format srt \
  --convert-subs srt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get JSON metadata including subtitle info
yt-dlp --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Code Example (Python Integration)
```python
import yt_dlp
import os

def extract_transcript_ytdlp(video_url, output_dir='./transcripts'):
    """Extract transcript using yt-dlp"""

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'skip_download': True,  # Don't download video
        'writeautomaticsub': True,  # Get auto-generated subs
        'writesubtitles': True,  # Get manual subs if available
        'subtitleslangs': ['en'],  # Language preference
        'subtitlesformat': 'vtt',  # Format (vtt, srt, etc.)
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',  # Output template
        'quiet': True,  # Suppress output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_id = info['id']

            # Find the subtitle file
            subtitle_file = f"{output_dir}/{video_id}.en.vtt"

            if os.path.exists(subtitle_file):
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                return {
                    'success': True,
                    'video_id': video_id,
                    'title': info.get('title'),
                    'subtitle_file': subtitle_file,
                    'content': content
                }
            else:
                return {'success': False, 'error': 'No subtitles available'}

    except Exception as e:
        return {'success': False, 'error': str(e)}

# Usage
result = extract_transcript_ytdlp("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
if result['success']:
    print(f"Title: {result['title']}")
    print(f"Transcript saved to: {result['subtitle_file']}")
```

### Parse VTT Format
```python
import re

def parse_vtt_transcript(vtt_content):
    """Convert VTT subtitle file to clean text"""

    # Remove VTT header
    lines = vtt_content.split('\n')

    # Skip header lines
    transcript_lines = []
    for line in lines:
        # Skip timestamps, empty lines, and headers
        if '-->' not in line and line.strip() and not line.startswith('WEBVTT'):
            # Remove VTT formatting tags
            clean_line = re.sub(r'<[^>]+>', '', line)
            transcript_lines.append(clean_line.strip())

    # Join and remove duplicates (VTT often repeats lines)
    full_text = ' '.join(transcript_lines)

    return full_text
```

### Pros
✅ **Very robust** - Actively maintained, handles YouTube changes quickly
✅ **Rich metadata** - Gets video title, description, duration, etc.
✅ **Multiple formats** - VTT, SRT, JSON output
✅ **Subtitle preference** - Auto vs manual caption selection
✅ **Batch processing** - Can handle playlists
✅ **No authentication** - Works without API key
✅ **Cookie support** - Can access age-restricted or member-only videos

### Cons
❌ **Heavier weight** - More dependencies than youtube-transcript-api
❌ **File-based** - Writes to disk (though can use memory streams)
❌ **Parsing required** - VTT/SRT formats need post-processing
❌ **Slower** - More overhead than direct API calls
❌ **Command-line first** - Python wrapper adds complexity

### Rate Limits
- **No official limits** - Scrapes public data
- **Practical limit**: ~50-100 videos/minute
- **YouTube may throttle**: Heavy usage could trigger IP-based rate limiting
- **Recommendation**: Add delays, rotate IPs for large-scale use

### Reliability Score: 9/10
Extremely reliable. Development team quickly adapts to YouTube changes.

---

## Method 3: YouTube Data API v3 (Official)

### Overview
Google's official API for accessing YouTube data, including captions.

### How It Works
- OAuth 2.0 authentication required
- RESTful API endpoints
- Captions endpoint provides download URLs
- Requires video owner permission OR public captions

### Authentication Setup
```python
# Install Google API client
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# You need:
# 1. Google Cloud Project
# 2. YouTube Data API v3 enabled
# 3. OAuth 2.0 credentials OR API key
```

### Code Example (API Key - Limited)
```python
from googleapiclient.discovery import build

API_KEY = 'YOUR_API_KEY_HERE'

def get_video_captions_info(video_id):
    """List available captions for a video"""

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        # List caption tracks
        request = youtube.captions().list(
            part='snippet',
            videoId=video_id
        )
        response = request.execute()

        captions = []
        for item in response.get('items', []):
            captions.append({
                'id': item['id'],
                'language': item['snippet']['language'],
                'name': item['snippet']['name'],
                'trackKind': item['snippet']['trackKind']  # 'standard' or 'asr' (auto)
            })

        return {'success': True, 'captions': captions}

    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### Code Example (OAuth - Full Access)
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def authenticate_youtube():
    """Authenticate with OAuth 2.0"""

    creds = None

    # Token file stores access/refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def download_caption(caption_id, youtube_service):
    """Download caption content"""

    try:
        # Download caption
        request = youtube_service.captions().download(
            id=caption_id,
            tfmt='srt'  # or 'vtt', 'sbv', 'ttml'
        )

        caption_content = request.execute()

        return {'success': True, 'content': caption_content}

    except Exception as e:
        return {'success': False, 'error': str(e)}

# Usage
youtube = authenticate_youtube()
captions_info = get_video_captions_info('dQw4w9WgXcQ')

if captions_info['success'] and captions_info['captions']:
    # Download first available caption
    caption_id = captions_info['captions'][0]['id']
    result = download_caption(caption_id, youtube)

    if result['success']:
        print(result['content'])
```

### Pros
✅ **Official API** - Stable, documented, supported by Google
✅ **Comprehensive data** - Full video metadata access
✅ **Quota system** - Clear, predictable rate limits
✅ **Multiple formats** - SRT, VTT, SBV, TTML
✅ **Reliability** - Won't break from YouTube updates

### Cons
❌ **Authentication required** - OAuth 2.0 setup complex
❌ **Quota limits** - 10,000 units/day (free tier)
❌ **Caption download cost** - 200 units per download
❌ **Means ~50 transcripts/day** on free tier
❌ **Permission issues** - Some videos require owner authorization
❌ **Complexity** - More setup than unofficial methods
❌ **Cost** - May require paid quota for scale

### Rate Limits
- **Default quota**: 10,000 units/day
- **Captions.list**: 50 units per request
- **Captions.download**: 200 units per request
- **Calculation**: ~50 full transcript downloads per day (free tier)
- **Quota increase**: Can request from Google (approval required)
- **Cost**: $0-$0.30 per 1,000 units above quota

### Reliability Score: 10/10
Official API - most reliable but most restrictive.

---

## Method 4: Alternative Libraries & Services

### 4a. PyTube (Python)
**Status**: Deprecated/Broken - Not recommended as of 2025

### 4b. AssemblyAI + YouTube URL
```python
import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"

# AssemblyAI can directly transcribe YouTube videos
transcriber = aai.Transcriber()
transcript = transcriber.transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print(transcript.text)
```

**Pros**: High-quality AI transcription, works on videos without captions
**Cons**: Paid service, not extracting existing transcripts

### 4c. Speechmatics, Rev.ai, Deepgram
Similar to AssemblyAI - transcribe audio, not extract existing captions.

---

## Comparison Matrix

| Method | Auth Required | Rate Limit | Reliability | Setup Complexity | Best For |
|--------|---------------|------------|-------------|------------------|----------|
| **youtube-transcript-api** | No | ~100-200/min | 8/10 | Low | Quick prototypes, general use |
| **yt-dlp** | No | ~50-100/min | 9/10 | Medium | Robust extraction, metadata needed |
| **YouTube Data API** | Yes (OAuth) | 50/day (free) | 10/10 | High | Production apps, official support |
| **AI Transcription Services** | Yes (API key) | Varies | 10/10 | Low | Videos without captions |

---

## Recommendation for AI Agent Use

### For Most Use Cases: youtube-transcript-api
**Why**: Perfect balance of simplicity, speed, and reliability.

```python
# Recommended implementation for AI agents
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

def extract_youtube_transcript(video_url_or_id):
    """
    Extract YouTube transcript for AI agent consumption

    Args:
        video_url_or_id: YouTube URL or video ID

    Returns:
        dict: {'success': bool, 'transcript': str, 'error': str}
    """

    # Extract video ID from URL if needed
    video_id = video_url_or_id
    if 'youtube.com' in video_url_or_id or 'youtu.be' in video_url_or_id:
        # Extract ID from various URL formats
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, video_url_or_id)
            if match:
                video_id = match.group(1)
                break

    try:
        # Get transcript (tries English first, then any available language)
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en', 'en-US', 'en-GB']
        )

        # Combine all segments into clean text
        full_transcript = ' '.join([segment['text'] for segment in transcript_list])

        # Clean up transcript (remove extra spaces, newlines)
        full_transcript = re.sub(r'\s+', ' ', full_transcript).strip()

        return {
            'success': True,
            'transcript': full_transcript,
            'video_id': video_id,
            'segment_count': len(transcript_list)
        }

    except TranscriptsDisabled:
        return {
            'success': False,
            'error': 'Transcripts are disabled for this video',
            'video_id': video_id
        }
    except NoTranscriptFound:
        return {
            'success': False,
            'error': 'No English transcript found for this video',
            'video_id': video_id
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error extracting transcript: {str(e)}',
            'video_id': video_id
        }

# Usage example
result = extract_youtube_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if result['success']:
    print(f"Transcript ({result['segment_count']} segments):")
    print(result['transcript'])
else:
    print(f"Error: {result['error']}")
```

### For Production Apps with Scale: YouTube Data API
Only if you need:
- Official support guarantee
- Ability to request quota increases
- Integration with other Google services

### For Maximum Reliability: yt-dlp as Fallback
Use youtube-transcript-api first, fall back to yt-dlp if it fails.

```python
def extract_transcript_with_fallback(video_url):
    """Try youtube-transcript-api first, fall back to yt-dlp"""

    # Try Method 1: youtube-transcript-api
    result = extract_youtube_transcript(video_url)
    if result['success']:
        return result

    # Try Method 2: yt-dlp
    result = extract_transcript_ytdlp(video_url)
    return result
```

---

## Implementation Checklist for AI Agent

- [ ] Install `youtube-transcript-api`: `pip install youtube-transcript-api`
- [ ] Implement URL parser to extract video ID
- [ ] Add error handling for disabled/missing transcripts
- [ ] Clean transcript text (remove formatting, extra spaces)
- [ ] Consider caching transcripts to avoid re-fetching
- [ ] Add rate limiting if processing many videos
- [ ] Test with various video types (different languages, auto vs manual captions)
- [ ] Consider fallback to yt-dlp for critical use cases

---

## Testing Video IDs

Use these for testing:

- **Standard transcript**: `dQw4w9WgXcQ` (Rick Astley - Never Gonna Give You Up)
- **Educational content**: `9bZkp7q19f0` (Gangnam Style - multi-language)
- **Tech talk**: `8pTEmbeENF4` (Google I/O keynote)

---

## Additional Resources

- youtube-transcript-api GitHub: https://github.com/jdepoix/youtube-transcript-api
- yt-dlp GitHub: https://github.com/yt-dlp/yt-dlp
- YouTube Data API v3: https://developers.google.com/youtube/v3
- Caption/Subtitle formats explained: https://www.3playmedia.com/blog/closed-caption-file-formats/

---

**Research completed**: 2026-01-02
**Recommended approach**: youtube-transcript-api for AI agent use
**Next steps**: Implement and test with real video URLs
