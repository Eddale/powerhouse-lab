# Quick Start: iOS Shortcut + Make.com for YouTube Summarization

**Goal:** Drop a YouTube link from iPhone → Get Claude summary → Add to task system
**Time to Build:** 30-60 minutes
**Cost:** Free (Make free tier)

---

## WHAT YOU'LL BUILD

```
iPhone Share Sheet
    ↓ (YouTube URL)
iOS Shortcut
    ↓ (POST to webhook)
Make.com Scenario
    ↓ (Get transcript)
Claude API
    ↓ (Summary + action items)
Your Task System
    ↓
Notification: "Added to tasks"
```

---

## PREREQUISITES

- [ ] iPhone with iOS 14+
- [ ] Make.com account (free tier: https://make.com)
- [ ] Anthropic API key (https://console.anthropic.com)
- [ ] Task system account (Things, Todoist, Reminders, etc.)

---

## STEP 1: SET UP MAKE.COM SCENARIO

### 1.1 Create New Scenario

1. Go to Make.com
2. Click "Create a new scenario"
3. Name it: "YouTube to Tasks via Claude"

### 1.2 Add Webhook Trigger

1. Click the "+" to add module
2. Search "Webhooks"
3. Select "Custom webhook"
4. Click "Create a webhook"
5. Name it: "youtube-summarize"
6. **Copy the webhook URL** (you'll need this)
7. Click "OK"

### 1.3 Add YouTube Transcript Module

**Option A: Use HTTP Module (Free)**

1. Add "HTTP" → "Make a request"
2. URL: `https://www.youtube.com/watch?v={{1.url}}`
3. Method: GET
4. Parse response: Yes

**Note:** This gets the page, but not transcript. For real transcripts, use:

**Option B: Use RapidAPI (Requires account)**

1. Sign up at RapidAPI.com
2. Subscribe to "YouTube Transcript" API (free tier available)
3. In Make, add "HTTP" module
4. Configure with RapidAPI credentials

**Option C: Skip for MVP**

For testing, you can send just the URL to Claude and let it work with that.

### 1.4 Add Claude API Call

1. Add module: "HTTP" → "Make a request"
2. Configure:
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Method:** POST
   - **Headers:**
     - Name: `x-api-key` | Value: `YOUR_ANTHROPIC_API_KEY`
     - Name: `anthropic-version` | Value: `2023-06-01`
     - Name: `content-type` | Value: `application/json`
   - **Body type:** Raw
   - **Content type:** JSON (application/json)
   - **Request content:**
   ```json
   {
     "model": "claude-sonnet-4-5-20250929",
     "max_tokens": 1024,
     "messages": [
       {
         "role": "user",
         "content": "Summarize this YouTube video and extract 3-5 action items: {{1.url}}"
       }
     ]
   }
   ```

### 1.5 Parse Claude Response

1. Add module: "JSON" → "Parse JSON"
2. JSON string: `{{previous.data}}`

### 1.6 Add to Task System

**For Things 3:**
1. Add module: "Things"
2. Action: "Create a To-Do"
3. Configure:
   - Title: `YouTube: {{1.url}}`
   - Notes: `{{parsed.content[0].text}}`
   - When: Inbox

**For Todoist:**
1. Add module: "Todoist"
2. Action: "Create a Task"
3. Configure:
   - Content: `YouTube Summary`
   - Description: `{{parsed.content[0].text}}\n\nSource: {{1.url}}`

**For Apple Reminders:**
1. Add module: "HTTP"
2. You'll need to use Shortcuts integration (see next section)

### 1.7 Send Response Back

1. Add module: "Webhooks" → "Webhook response"
2. Status: 200
3. Body:
   ```json
   {
     "success": true,
     "summary": "{{parsed.content[0].text}}"
   }
   ```

### 1.8 Save and Activate

1. Click "Save"
2. Turn scenario "ON"
3. **Copy the webhook URL from step 1.2**

---

## STEP 2: CREATE iOS SHORTCUT

### 2.1 Open Shortcuts App

1. Open "Shortcuts" app on iPhone
2. Tap "+" to create new shortcut
3. Name it: "Summarize YouTube"

### 2.2 Build the Shortcut

**Action 1: Get Shortcut Input**
1. Search "Receive"
2. Add "Receive [Any] input from [Share Sheet]"
3. Tap "Any" → Change to "URLs"

**Action 2: Get URL**
1. Search "URL"
2. Add "Get URLs from Input"

**Action 3: Call Make Webhook**
1. Search "Get Contents"
2. Add "Get contents of [URL]"
3. Tap the URL field
4. Change to: `YOUR_MAKE_WEBHOOK_URL`
5. Tap "Show More"
6. Change Method to: POST
7. Add Header:
   - Key: `Content-Type`
   - Value: `application/json`
8. Change Request Body to: JSON
9. Add JSON:
   ```
   {"url": "SHORTCUT_INPUT_URL"}
   ```
   (Use magic variable for the URL from Action 2)

**Action 4: Parse Response**
1. Search "Get Dictionary"
2. Add "Get Dictionary Value"
3. Get: `summary`
4. From: "Contents of URL" (from Action 3)

**Action 5: Add to Reminders (if not using Make integration)**
1. Search "Add"
2. Add "Add new reminder"
3. Text: Dictionary Value (from Action 4)
4. List: Choose your list

**Action 6: Show Confirmation**
1. Search "Show"
2. Add "Show Notification"
3. Text: "Added YouTube summary to tasks"

### 2.3 Configure Share Sheet

1. Tap the (i) info icon
2. Enable "Show in Share Sheet"
3. Under "Share Sheet Types", enable:
   - Safari Web Pages
   - URLs
4. Tap "Done"

---

## STEP 3: TEST THE FLOW

### 3.1 Test Make Scenario

1. In Make, click "Run once"
2. Use Postman or curl to test webhook:
   ```bash
   curl -X POST YOUR_WEBHOOK_URL \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
   ```
3. Check Make execution log for errors
4. Verify Claude response
5. Check if task was created

### 3.2 Test iOS Shortcut

1. Open YouTube app or Safari
2. Find any video
3. Tap Share button
4. Find "Summarize YouTube" in share sheet
5. Tap it
6. Wait for notification
7. Check your task system

---

## TROUBLESHOOTING

### Webhook Not Triggering
- [ ] Verify webhook URL is correct in Shortcut
- [ ] Check Make scenario is "ON"
- [ ] Look at Make execution history
- [ ] Test with curl first

### Claude API Errors
- [ ] Verify API key is correct
- [ ] Check API key has credits
- [ ] Verify JSON format is correct
- [ ] Check model name is valid

### No Tasks Created
- [ ] Verify task system is connected in Make
- [ ] Check task system credentials
- [ ] Look at Make execution log for that step
- [ ] Test task creation manually in Make

### Shortcut Fails
- [ ] Check internet connection
- [ ] Verify webhook URL in Shortcut
- [ ] Look at Shortcut notification for error
- [ ] Try running Shortcut manually (not from share)

---

## ENHANCEMENTS

### Add Transcript Extraction

Update Claude API call to accept transcript:

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 2048,
  "messages": [
    {
      "role": "user",
      "content": "Video: {{1.url}}\n\nTranscript:\n{{transcript}}\n\nProvide:\n1. 2-3 sentence summary\n2. Key points (bullets)\n3. Action items (if any)"
    }
  ]
}
```

### Add Filtering

In Shortcut, add condition:
- If URL contains "youtube.com" → Continue
- Otherwise → Show alert "This only works with YouTube"

### Add Error Handling

In Make, add "Error handler" route:
- Send webhook response with error message
- Log to Google Sheets for debugging

### Custom Prompts

Add a "Choose from Menu" action in Shortcut:
- Quick summary
- Detailed analysis
- Extract action items
- Key quotes

Then pass choice to Make webhook.

---

## COSTS

### Make.com Free Tier
- 1,000 operations/month
- 2 active scenarios
- 15 minute interval

**Your usage:**
- 1 operation = 1 execution
- Each video = ~4-6 operations (webhook, Claude, task, response)
- ~150-250 videos/month on free tier

### Claude API
- Sonnet 4.5: ~$3 per million input tokens
- Average video summary: ~1,000 tokens
- Cost per video: ~$0.003 (less than a penny)
- 100 videos: ~$0.30

**Total monthly cost (moderate use): $0-9**
- Free tier: $0
- Make Pro (if needed): $9/month
- Claude API: ~$1-2/month

---

## SECURITY NOTES

### API Key Protection

Your Claude API key is stored in Make.com, not on your phone. This is good.

**Don't:**
- Share your webhook URL publicly
- Commit webhook URL to Git
- Share screenshots with API keys

**Do:**
- Regenerate API key if webhook URL leaks
- Use environment variables in Make
- Monitor API usage in Anthropic console

### Webhook Security

Add authentication to webhook:

1. In Make webhook, add "Verify" condition
2. Check for secret token in headers
3. In Shortcut, add custom header:
   - Key: `X-Auth-Token`
   - Value: `YOUR_SECRET_TOKEN`

---

## ALTERNATIVE: DIRECT SHORTCUT → CLAUDE

If you don't want to use Make, you can call Claude directly from Shortcut.

**Warning:** API key will be in Shortcut (less secure)

### Shortcut Configuration

**Action: Get Contents of URL**
- URL: `https://api.anthropic.com/v1/messages`
- Method: POST
- Headers:
  - `x-api-key`: `YOUR_API_KEY`
  - `anthropic-version`: `2023-06-01`
  - `content-type`: `application/json`
- Body:
  ```json
  {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": "Summarize: [YouTube URL]"
    }]
  }
  ```

Then parse response and add to Reminders.

**Pros:**
- Simpler
- Faster (one less hop)
- No Make.com dependency

**Cons:**
- API key in Shortcut
- Can't get transcripts easily
- Limited processing
- Harder to add features

---

## NEXT STEPS

Once this works:

1. **Add more content types:**
   - Articles (use Jina Reader API)
   - PDFs (extract text first)
   - Podcasts (get transcript)

2. **Enhance processing:**
   - Category detection
   - Auto-tagging
   - Due date extraction

3. **Build dashboard:**
   - See all processed items
   - Review summaries
   - Edit before adding to tasks

4. **Graduate to custom app:**
   - Better UX
   - Offline queueing
   - Batch processing

---

## RESOURCES

- Make.com Docs: https://www.make.com/en/help
- iOS Shortcuts Guide: https://support.apple.com/guide/shortcuts
- Anthropic API Docs: https://docs.anthropic.com
- YouTube Transcript API: https://github.com/jdepoix/youtube-transcript-api

---

**Questions? Issues? Updates?**

Document them in: `/tasks/mobile-integration-notes.md`
