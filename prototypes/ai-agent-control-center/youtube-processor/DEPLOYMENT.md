# Deployment Guide

Step-by-step instructions for getting this live.

---

## Option 1: Railway (Recommended)

**Why Railway**: Dead simple, always-on, free tier is generous.

### Steps

1. **Push to GitHub**
   ```bash
   cd youtube-processor
   git init
   git add .
   git commit -m "Initial YouTube processor"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repo
   - Railway auto-detects Python and runs `main.py`

3. **Add Environment Variable**
   - In Railway dashboard → Variables
   - Add: `ANTHROPIC_API_KEY` = your API key
   - Railway auto-redeploys

4. **Get Your URL**
   - Railway generates a URL like: `https://youtube-processor-production.up.railway.app`
   - Test it: `curl https://your-url/health`

5. **Custom Domain (Optional)**
   - Settings → Domains
   - Add custom domain: `yt.yourdomain.com`

**Done.** Your API is live.

---

## Option 2: Render

Similar to Railway, but slightly different UI.

### Steps

1. **Push to GitHub** (same as above)

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - New → Web Service
   - Connect GitHub repo
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Environment**: Python 3

3. **Add Environment Variable**
   - Environment tab
   - Add: `ANTHROPIC_API_KEY`

4. **Deploy**
   - Render auto-deploys
   - You get a URL like: `https://youtube-processor.onrender.com`

**Note**: Render's free tier spins down after inactivity (cold starts).

---

## Option 3: Self-Hosted (VPS)

If you have a VPS (DigitalOcean, Linode, etc.)

### Using Docker

1. **Create Dockerfile** (already in repo if you created it):
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**:
   ```bash
   docker build -t youtube-processor .
   docker run -d \
     -p 8000:8000 \
     -e ANTHROPIC_API_KEY=your_key \
     --name youtube-api \
     youtube-processor
   ```

3. **Use nginx as reverse proxy**:
   ```nginx
   server {
       listen 80;
       server_name yt.yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Add SSL with Let's Encrypt**:
   ```bash
   sudo certbot --nginx -d yt.yourdomain.com
   ```

---

## Option 4: Local Network (Mac/PC)

If you just want to use it from your iPhone on your home network:

1. **Run the server**:
   ```bash
   python main.py
   ```

2. **Get your local IP**:
   ```bash
   # Mac
   ipconfig getifaddr en0

   # Linux
   hostname -I | awk '{print $1}'
   ```

3. **Access from iOS Shortcut**:
   - Use: `http://YOUR_LOCAL_IP:8000/process`
   - Must be on same WiFi network

**Pros**: Free, private
**Cons**: Only works at home, requires computer to be on

---

## Testing Your Deployment

Once deployed, test with curl:

```bash
# Health check
curl https://your-deployed-url/health

# Process a video
curl -X POST "https://your-deployed-url/process" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "summary_type": "brief"
  }'
```

You should get back JSON with a summary.

---

## Setting Up the iOS Shortcut

Once your API is live, create the iOS Shortcut:

### Step-by-Step

1. **Open Shortcuts app** on iPhone
2. **Tap + to create new shortcut**
3. **Add actions in this order**:

**Action 1: Ask for Input**
```
Type: URL
Prompt: "YouTube URL to summarize"
```

**Action 2: Get Contents of URL**
```
URL: https://your-deployed-url/process
Method: POST
Headers:
  Content-Type: application/json
Request Body:
{
  "url": [Provided Input],
  "summary_type": "detailed"
}
```

**Action 3: Get Dictionary Value**
```
Key: markdown_output
From: Contents of URL
```

**Action 4: Save File**
```
Service: iCloud Drive
Destination: Shortcuts/YouTube Summaries/
File Name: YT-[Current Date].md
Contents: [Dictionary Value]
```

**Optional: Add to Share Sheet**
- Settings → Share Sheet Types
- Enable: URLs, Safari Web Pages
- Now you can share YouTube URLs directly from Safari/YouTube app

---

## Monitoring & Logs

### Railway
- Dashboard → Deployments → View Logs
- Real-time log streaming
- Automatic crash recovery

### Render
- Logs tab in dashboard
- Can set up email alerts for downtime

### Self-Hosted
```bash
# View Docker logs
docker logs -f youtube-api

# View last 100 lines
docker logs --tail 100 youtube-api
```

---

## Updating After Changes

### Railway/Render
```bash
git add .
git commit -m "Update prompt/feature"
git push
```
Auto-deploys. That's it.

### Docker
```bash
git pull
docker build -t youtube-processor .
docker stop youtube-api
docker rm youtube-api
docker run -d -p 8000:8000 -e ANTHROPIC_API_KEY=your_key --name youtube-api youtube-processor
```

---

## Troubleshooting

### API returns 500 errors
- Check logs for Claude API errors
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check API rate limits

### "No transcript found"
- Some videos don't have transcripts
- Creator may have disabled them
- Try a different video

### iOS Shortcut fails
- Check URL is correct (https, not http)
- Verify API is responding: test in browser at `/health`
- Check request body formatting in Shortcut

### Slow response times
- Large transcripts take 10-30 seconds to process
- This is normal - Claude needs time to read and summarize
- Consider adding a loading indicator in Shortcut

---

## Cost Breakdown

### Railway (Recommended)
- Free tier: $5 credit/month
- This API uses ~$0.50/month (always-on tiny container)
- **Effectively free** unless you process thousands of videos

### Render
- Free tier: Limited to 750 hours/month
- Spins down after inactivity (slow cold starts)

### Self-Hosted
- VPS: $5-10/month
- More control, more setup

### Claude API
- ~$0.02-0.05 per video processed
- 100 videos/month = ~$2-5

**Total monthly cost**: ~$0-15 depending on usage

---

## Security Considerations

### API Key Security
- Never commit `.env` to git
- Use environment variables in Railway/Render
- Rotate keys if compromised

### Rate Limiting (Optional)
If you want to add rate limiting:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/process")
@limiter.limit("10/minute")
async def process_youtube_video(request: YouTubeRequest):
    # ... existing code
```

### Authentication (Optional)
For private use, add a simple API key:

```python
from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header()):
    if x_api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.post("/process", dependencies=[Depends(verify_token)])
async def process_youtube_video(request: YouTubeRequest):
    # ... existing code
```

Then in iOS Shortcut, add header:
```
X-API-Key: your_secret_key
```

---

## Next Steps After Deployment

1. **Test with real videos** from your workflow
2. **Adjust Claude prompt** in `summarize_with_claude()` to match your style
3. **Add custom summary types** based on content type (tutorial, interview, lecture)
4. **Set up monitoring** (Uptime Robot, BetterStack)
5. **Create more iOS Shortcuts** for different summary styles

---

**You're live. Time to summarize some videos.**
