# Mobile Claude API Integration Research

**Date:** 2026-01-02
**Use Case:** Drop YouTube link on mobile → Claude summarizes → Add to task system

---

## 1. iOS Shortcuts + Claude API

**STATUS: ✅ WORKS - Best Quick Solution**

### How It Works
iOS Shortcuts can make HTTP requests, so you can call the Claude API directly.

### Implementation Pattern
```
Shortcut Flow:
1. Share Sheet receives URL
2. Get Contents of URL (optional - for webpage text)
3. Make HTTP Request to Claude API
   - Method: POST
   - URL: https://api.anthropic.com/v1/messages
   - Headers:
     - x-api-key: [Your API Key]
     - anthropic-version: 2023-06-01
     - content-type: application/json
   - Body (JSON):
     {
       "model": "claude-sonnet-4-5-20250929",
       "max_tokens": 1024,
       "messages": [{
         "role": "user",
         "content": "Summarize this YouTube video: [URL]"
       }]
     }
4. Parse JSON response
5. Extract response.content[0].text
6. Send to task system (Reminders, Things, etc.)
```

### Limitations
- API key stored in Shortcut (security consideration)
- No streaming responses
- Limited error handling
- Need to manually construct JSON
- YouTube transcripts require separate API/service

### Security Improvement
Use a CloudFlare Worker or simple API endpoint to proxy requests and hide your API key.

---

## 2. Anthropic Mobile Apps

**STATUS: ⚠️ LIMITED**

### Official Claude App (iOS/Android)
- **Exists:** Yes
- **Custom Prompts:** Yes, via Projects feature
- **API Access:** No - uses web interface, not your API key
- **Automation:** Not supported
- **Use Case Fit:** Poor - can't automate or integrate with task systems

### Projects Feature
- Can set custom instructions per conversation
- Can upload knowledge documents
- BUT: No automation, no external integrations

---

## 3. Third-Party Claude API Clients

**STATUS: ✅ SEVERAL OPTIONS**

### Known Apps (verify availability in App Store)

**OpenCat** (iOS)
- Supports custom API keys (OpenAI, Claude, others)
- Custom prompts/instructions
- NOT automation-friendly
- Good for manual queries

**AI Chat - Claude & ChatGPT** (various names)
- Multiple apps with similar names
- Some support BYOK (Bring Your Own Key)
- Quality varies widely
- Check reviews for Claude API support

**Typing Mind** (PWA + iOS)
- Web-based, works on mobile
- Supports Claude API with your key
- Custom prompts and workflows
- Better for repeated tasks

### For Your Use Case
These are manual tools - you'd still need to:
1. Copy YouTube link
2. Open app
3. Paste and run
4. Copy result
5. Add to task system

**Not ideal for your capture-and-process workflow.**

---

## 4. Webhook Intermediaries

**STATUS: ✅ EXCELLENT FOR YOUR USE CASE**

### Make.com (Integromat)
```
Flow:
iOS Shortcut → Make Webhook → Claude API → Task System
```

**Setup:**
1. Create Make scenario with webhook trigger
2. Add Anthropic (Claude) module
3. Add task system integration (Todoist, Things, etc.)
4. iOS Shortcut sends YouTube URL to webhook
5. Make handles everything else

**Pros:**
- No API key in Shortcut
- Easy error handling
- Can chain multiple actions
- Visual workflow builder
- Built-in Claude integration

**Cons:**
- Requires Make account
- Free tier limits
- Another service dependency

### Zapier
```
Flow:
iOS Shortcut → Zapier Webhook → Claude API → Task System
```

**Similar to Make but:**
- Different pricing model
- May have native Claude integration (check current status)
- Can use Code steps if no native Claude
- More popular, potentially better task app integrations

### n8n (Self-Hosted Alternative)
```
Flow:
iOS Shortcut → n8n Webhook → Claude API → Task System
```

**Pros:**
- Self-hosted = full control
- Free (just hosting costs)
- Powerful automation

**Cons:**
- Setup complexity
- Need to maintain server

---

## 5. Custom iOS App

**STATUS: ✅ FEASIBLE BUT OVERKILL**

### Complexity Level
**Low** for basic implementation:
- Swift + SwiftUI
- URLSession for API calls
- Share Extension for URL capture
- ~200-300 lines of code

### Minimum Viable App
```swift
// Simplified structure
struct ClaudeService {
    func summarize(url: String) async throws -> String {
        // POST to Claude API
        // Parse response
        // Return summary
    }
}

// Share Extension
class ShareViewController: UIViewController {
    func receiveURL(_ url: String) {
        Task {
            let summary = try await ClaudeService().summarize(url: url)
            // Save to task system or clipboard
        }
    }
}
```

### Required Skills
- Swift basics
- Async/await
- URLSession/networking
- Share Extensions
- Keychain (for API key storage)

### Time Investment
- First build: 4-8 hours
- With YouTube transcript extraction: +4 hours
- Task system integration: +2-4 hours per system

### When It Makes Sense
- You want full control
- Plan to add more features
- Want offline queueing
- Need custom UI/UX

---

## 6. Progressive Web App (PWA)

**STATUS: ✅ PRACTICAL MIDDLE GROUND**

### How It Works
Build a simple web app that:
1. Accepts shared URLs via Web Share Target API
2. Calls Claude API
3. Returns results
4. Can be "installed" to iOS home screen

### Tech Stack
```javascript
// Example with Next.js
export default function API(req, res) {
    const { url } = req.body;

    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'x-api-key': process.env.ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        body: JSON.stringify({
            model: 'claude-sonnet-4-5-20250929',
            max_tokens: 1024,
            messages: [{
                role: 'user',
                content: `Summarize this YouTube video: ${url}`
            }]
        })
    });

    const data = await response.json();
    res.json({ summary: data.content[0].text });
}
```

### iOS Integration
1. Add to Home Screen
2. Configure Web Share Target in manifest
3. iOS Share Sheet → Your PWA
4. Process and display

### Pros
- Cross-platform (iOS + Android)
- Easier than native app
- Can host on Vercel/Netlify
- API key stays server-side

### Cons
- Less native feel
- Share target support varies
- Requires internet
- Not in App Store

---

## RECOMMENDED SOLUTION FOR YOUR USE CASE

### Phase 1: Quick Win (Today)
**iOS Shortcuts + Make.com Webhook**

1. **Set up Make scenario:**
   - Trigger: Webhook
   - Action: HTTP request to Claude API
   - Action: Add to your task system

2. **Create iOS Shortcut:**
   - Receive URL from Share Sheet
   - POST to Make webhook
   - Show notification when done

**Time to build:** 30-60 minutes
**Maintenance:** Minimal
**Cost:** Free tier likely sufficient

### Phase 2: Custom Solution (Later)
**PWA or Native App**

Build when:
- You want more features
- Processing volume increases
- You need offline capability
- You want to customize the summarization prompt based on content type

---

## YOUTUBE-SPECIFIC CONSIDERATIONS

### Getting Transcripts
Claude API can't directly access YouTube transcripts. Options:

1. **YouTube Transcript API** (Python)
   ```python
   from youtube_transcript_api import YouTubeTranscriptApi
   ```

2. **Third-party services:**
   - RapidAPI has YouTube transcript endpoints
   - Some free, some paid

3. **Your workflow:**
   - Mobile captures URL
   - Backend fetches transcript
   - Sends to Claude
   - Returns summary

### Make.com Implementation
Make has modules for:
- YouTube data extraction
- HTTP requests (for transcript APIs)
- Claude API calls
- Task management apps

Can build entire flow visually.

---

## CODE SNIPPETS

### iOS Shortcut (Pseudo-code)
```
Receive URLs from Share Sheet
Set Variable: videoURL to Shortcut Input

Get Contents of URL: https://your-webhook.make.com/youtube-summarize
  Method: POST
  Headers: Content-Type: application/json
  Request Body: {"url": "[videoURL]"}

Get Dictionary Value "summary" from Contents of URL

Add to Reminders
  List: Inbox
  Notes: [Dictionary Value]
  URL: [videoURL]

Show Notification: "Added to tasks"
```

### Make.com Scenario (Structure)
```
1. Webhook (Catch Hook)
   ↓
2. YouTube Transcript (Custom HTTP or module)
   ↓
3. Claude API (HTTP Request)
   ↓
4. Your Task System (Things, Todoist, etc.)
   ↓
5. Webhook Response (success message)
```

### Simple PWA API Route (Next.js)
```javascript
// pages/api/summarize.js
import Anthropic from '@anthropic-ai/sdk';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { url } = req.body;

    try {
        const anthropic = new Anthropic({
            apiKey: process.env.ANTHROPIC_API_KEY,
        });

        const message = await anthropic.messages.create({
            model: 'claude-sonnet-4-5-20250929',
            max_tokens: 1024,
            messages: [{
                role: 'user',
                content: `Summarize this YouTube video and extract key action items: ${url}`
            }]
        });

        res.status(200).json({
            summary: message.content[0].text
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
```

---

## SECURITY NOTES

### API Key Storage
- **Never** hardcode in iOS Shortcut shared publicly
- **Never** commit to Git
- **Do** use environment variables server-side
- **Do** use iOS Keychain if building native app
- **Do** use webhook proxy to hide key from device

### Best Practice
```
Mobile Device → Webhook (your server) → Claude API
                   ↑
              API key stored here
```

---

## NEXT STEPS

1. **Test the concept:** Build iOS Shortcut → Make → Claude flow
2. **Validate:** Does it solve your capture problem?
3. **Iterate:** Add YouTube transcript extraction
4. **Decide:** Stay with Make or build custom solution?

---

## TOOLS COMPARISON

| Approach | Setup Time | Control | Cost | Maintenance |
|----------|-----------|---------|------|-------------|
| Shortcuts + Make | 1 hour | Medium | Free-$9/mo | Very Low |
| Shortcuts Direct | 30 min | Low | API usage | Low |
| Third-party App | 5 min | Very Low | Free-$10/mo | None |
| Custom iOS App | 8-16 hours | Very High | API + Dev | Medium |
| PWA | 4-8 hours | High | Hosting + API | Low |
| Native + Backend | 16+ hours | Total | Hosting + API | Medium |

---

## RESOURCES TO CHECK

### Documentation
- Anthropic API Docs: https://docs.anthropic.com
- iOS Shortcuts User Guide (Apple)
- Make.com Claude Integration Docs
- Web Share Target API (MDN)

### Code Examples
- Search GitHub for: "claude api ios swift"
- Search GitHub for: "anthropic api shortcuts"
- Check awesome-claude repos for mobile examples

### Communities
- r/ClaudeAI (Reddit)
- Anthropic Discord
- iOS Shortcuts subreddit

---

## CONCLUSION

**For your YouTube → Summary → Tasks workflow:**

Best immediate solution: **iOS Shortcuts + Make.com**
- Fast to build
- Reliable
- Maintainable
- Extensible

If this becomes a core workflow you use 10+ times daily, graduate to a custom PWA or native app for better UX and control.

The key insight: Don't call Claude API directly from iOS Shortcut. Use a webhook intermediary (Make, Zapier, or your own endpoint) to keep API keys secure and enable richer processing (like transcript extraction).
