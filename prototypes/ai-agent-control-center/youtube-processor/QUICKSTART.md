# Quick Start - Get Running in 5 Minutes

**Goal**: Test the API locally, then deploy.

---

## Step 1: Install Dependencies (1 min)

```bash
cd youtube-processor
pip install -r requirements.txt
```

**What's installing**:
- FastAPI (web framework)
- youtube-transcript-api (transcript fetcher)
- anthropic (Claude SDK)

---

## Step 2: Configure API Key (1 min)

```bash
# Copy the example env file
cp .env.example .env

# Edit .env
nano .env  # or: code .env, vim .env, etc.
```

**Add your API key**:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Get your key from: [console.anthropic.com](https://console.anthropic.com)

---

## Step 3: Run Locally (30 seconds)

```bash
python main.py
```

**You should see**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**API is live at**: `http://localhost:8000`

---

## Step 4: Test It (2 min)

### Option A: Browser Test

Open: `http://localhost:8000/health`

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-02T10:30:00",
  "claude_api_configured": true
}
```

### Option B: Command Line Test

```bash
# In a new terminal window
python test_api.py
```

This will:
1. Check health endpoint
2. Process a real YouTube video
3. Show you the summary

### Option C: Manual curl Test

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "summary_type": "brief"
  }'
```

**Expected response** (takes 10-20 seconds):
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "summary": "This video is a classic internet meme...",
  "markdown_output": "---\nsource: YouTube\n...",
  "saved_to": null
}
```

---

## Step 5: Deploy (Optional, 5 min)

### Railway (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "YouTube processor API"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - New Project → Deploy from GitHub
   - Select your repo
   - Add environment variable: `ANTHROPIC_API_KEY`
   - Railway auto-deploys

3. **Get your URL**:
   - Railway gives you: `https://your-app.railway.app`
   - Test: `https://your-app.railway.app/health`

**Done. Your API is live.**

---

## Step 6: Set Up iOS Shortcut (5 min)

See: `IOS-SHORTCUT-SETUP.md` for detailed steps.

**Quick version**:

1. Open Shortcuts app
2. New Shortcut
3. Add 4 actions:
   - **Ask for Input** (URL)
   - **Get Contents of URL** (POST to your API)
   - **Get Dictionary Value** (extract markdown_output)
   - **Copy to Clipboard**

**Now you can**:
- Open Shortcut
- Paste YouTube URL
- Get summary instantly

---

## Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Could not connect to API"
- Is the server running? (`python main.py`)
- Check URL is `http://localhost:8000` (not https)

### "Error calling Claude API"
- Check your API key in `.env`
- Verify it's valid at console.anthropic.com
- Make sure there are no extra spaces/quotes

### "No transcript found"
- Try a different video (TED Talks always work)
- Some videos don't have transcripts

### Port 8000 already in use
```bash
# Mac/Linux
lsof -ti:8000 | xargs kill

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Next Steps

1. **Test with your own YouTube videos**
2. **Adjust Claude prompt** in `main.py` (line 136-147)
3. **Deploy to Railway** for always-on access
4. **Create multiple iOS Shortcuts** for different summary styles
5. **Read OVERVIEW.md** for extension ideas

---

## File Reference

```
youtube-processor/
├── main.py              ← The API (edit this to customize)
├── requirements.txt     ← Dependencies
├── .env                 ← Your API key (don't commit!)
├── README.md            ← Full documentation
├── DEPLOYMENT.md        ← Deployment options
├── IOS-SHORTCUT-SETUP.md ← iOS integration
├── OVERVIEW.md          ← Technical deep dive
└── QUICKSTART.md        ← You are here
```

---

## Customization Quick Wins

### Change the summary style

Edit `main.py`, line 136-147:

```python
prompts = {
    "brief": "Your custom brief prompt here",
    "detailed": "Your custom detailed prompt here",
    "bullets": "Your custom bullets prompt here"
}
```

### Add a new summary type

```python
prompts = {
    # ... existing types
    "academic": "Analyze this video from an academic perspective..."
}
```

Then in iOS Shortcut, use:
```json
{
  "summary_type": "academic"
}
```

### Change the Claude model

Line 157:
```python
model="claude-opus-4-5-20251101"  # Use Opus for deeper analysis
```

**Note**: Opus is slower and more expensive, but produces better summaries.

---

## Support

- **Bugs**: Check `main.py` error messages
- **API issues**: Test with `curl` first
- **iOS Shortcut issues**: Verify API works in browser

---

**You're ready. Start summarizing.**

Time from zero to working: **~5 minutes**
Time to deploy: **+5 minutes**
Time saved per video: **30+ minutes**

**Ship it.**
