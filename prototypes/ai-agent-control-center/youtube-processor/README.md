# YouTube Transcript Processor

**Direct pipeline**: YouTube URL → Transcript → Claude Summary → Obsidian-ready Markdown

No Make.com. No Zapier. Just a clean API endpoint.

---

## What It Does

1. Takes a YouTube URL
2. Extracts the transcript using `youtube-transcript-api`
3. Sends transcript to Claude for summarization
4. Returns Obsidian-formatted markdown
5. Optionally saves directly to your Obsidian vault

---

## Quick Start

### 1. Install Dependencies

```bash
cd youtube-processor
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run Locally

```bash
python main.py
```

The API will be running at `http://localhost:8000`

### 4. Test It

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "summary_type": "detailed"
  }'
```

---

## API Endpoints

### POST `/process`

Process a YouTube video and return summary.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "summary_type": "detailed",
  "save_to_obsidian": false,
  "obsidian_vault_path": "/path/to/vault"
}
```

**Summary Types:**
- `brief`: 2-3 sentence summary
- `detailed`: Full analysis with key points, takeaways, action items (default)
- `bullets`: Key points as bulleted list

**Response:**
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "summary": "...",
  "markdown_output": "...",
  "saved_to": "/path/to/file.md"
}
```

### GET `/health`

Check API health and configuration.

---

## Deployment Options

### Option 1: Railway (Recommended for Simplicity)

**Why Railway:**
- Dead simple deployment from GitHub
- Always-on (not serverless)
- Free tier includes 500 hours/month
- Perfect for this use case

**Steps:**
1. Push this code to a GitHub repo
2. Go to [railway.app](https://railway.app)
3. Create new project → Deploy from GitHub
4. Add environment variable: `ANTHROPIC_API_KEY`
5. Railway will auto-deploy from `main.py`
6. You get a URL like: `https://your-app.railway.app`

### Option 2: Render

Similar to Railway:
1. Connect GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add `ANTHROPIC_API_KEY` to environment

### Option 3: Self-Hosted (Docker)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Run:
```bash
docker build -t youtube-processor .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_key youtube-processor
```

### Option 4: Vercel (Not Recommended)

Vercel is optimized for serverless Next.js. While you CAN deploy FastAPI to Vercel, it requires extra config and has cold start issues. Railway or Render are better for this.

---

## iOS Shortcut Integration

### Creating the Shortcut

1. Open **Shortcuts** app on iOS
2. Create new shortcut
3. Add these actions:

**Action 1: Ask for Input**
- Prompt: "YouTube URL"
- Input Type: URL

**Action 2: Get Contents of URL**
- URL: `https://your-api.railway.app/process`
- Method: POST
- Headers:
  - `Content-Type`: `application/json`
- Request Body: JSON
  ```json
  {
    "url": "[Provided Input]",
    "summary_type": "detailed"
  }
  ```

**Action 3: Get Dictionary Value**
- Get: `markdown_output` from `Contents of URL`

**Action 4: Save File**
- Destination: iCloud Drive/Obsidian/
- Filename: `YT-Summary-[Current Date].md`

### Advanced: Direct Obsidian Save

If you're running the API on your local network or have Obsidian vault synced:

```json
{
  "url": "[Provided Input]",
  "summary_type": "detailed",
  "save_to_obsidian": true,
  "obsidian_vault_path": "/Users/yourusername/Documents/Obsidian/Vault"
}
```

The API will save directly to your vault (requires API to have file system access to vault).

---

## Error Handling

The API handles these edge cases:

### No Transcript Available
```json
{
  "success": false,
  "error": "No transcript found for this video",
  "video_id": "..."
}
```

**Common reasons:**
- Video creator disabled transcripts
- Video is too new (transcripts not generated yet)
- Video is age-restricted

### Invalid URL
```json
{
  "success": false,
  "error": "Could not extract video ID from URL"
}
```

### API Key Issues
```json
{
  "success": false,
  "error": "Error calling Claude API: authentication error"
}
```

---

## Architecture

This is intentionally simple - one file, one purpose:

```
YouTube URL
    ↓
extract_video_id()      # Parse the URL
    ↓
get_transcript()        # Call YouTube API
    ↓
summarize_with_claude() # Send to Claude
    ↓
format_for_obsidian()   # Create markdown
    ↓
save_to_vault()         # (Optional) Write to file
    ↓
Return JSON response
```

**Why FastAPI?**
- Auto-generated docs at `/docs`
- Type validation with Pydantic
- Async support (if you want to batch later)
- Easy to test

**Why youtube-transcript-api?**
- No YouTube API key needed
- Works with auto-generated and manual transcripts
- Handles multiple languages
- Lightweight and reliable

---

## Testing Locally from iOS

1. Get your local IP: `ipconfig getifaddr en0` (Mac) or `hostname -I` (Linux)
2. Run the server: `python main.py`
3. In iOS Shortcut, use: `http://YOUR_LOCAL_IP:8000/process`

**Note**: Your phone and computer must be on the same network.

---

## Next Steps / Enhancements

Once the basic flow works, you could add:

1. **Caching**: Store processed videos to avoid re-processing
2. **Batch processing**: Handle playlists
3. **Custom prompts**: Let iOS Shortcut pass a custom summarization prompt
4. **Webhook**: Push to Obsidian via webhook instead of file system
5. **Video metadata**: Fetch title, channel, description from YouTube
6. **Alternative transcription**: Fall back to Whisper API for videos without transcripts

---

## Troubleshooting

### "Transcripts are disabled for this video"
Some creators disable transcripts. Nothing you can do except:
- Try Whisper API (requires downloading video → expensive)
- Skip the video

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
lsof -ti:8000 | xargs kill  # Kill process on port 8000
python main.py
```

### Claude API rate limits
Free tier: 50 requests/day
Paid tier: Much higher, but check your usage

---

## Cost Estimate

**Per video processed:**
- YouTube transcript API: Free
- Claude API: ~$0.02-0.05 (depending on transcript length)

**Monthly estimate** (100 videos):
- YouTube API: $0
- Claude API: ~$2-5
- Hosting (Railway): Free tier sufficient

**This is dead cheap to run.**

---

## Why This Approach?

**vs. Make.com/Zapier:**
- No monthly subscription ($10-30/month saved)
- No rate limits
- Full control over processing logic
- Can customize Claude prompts easily

**vs. Native iOS app:**
- No App Store approval needed
- Works on any device (can add Android later)
- Easy to update (just push to GitHub)

**vs. Browser extension:**
- Works mobile-first
- No permission issues
- Can run headless

---

**Built for**: Vibe Coders who want URL in, summary out, no BS.
