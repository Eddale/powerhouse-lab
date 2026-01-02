# Mobile Claude API Tools & Apps - Comparison Matrix

**Last Updated:** 2026-01-02

---

## QUICK REFERENCE

| Solution | Best For | Setup Time | Monthly Cost | API Key Security |
|----------|----------|------------|--------------|------------------|
| iOS Shortcuts + Make | Quick automation | 1 hour | $0-9 | Excellent |
| iOS Shortcuts Direct | Simplest start | 30 min | API only | Poor |
| Chatbox.ai | Manual queries | 5 min | Free | Good |
| TypingMind | Power users | 10 min | $0-8 | Good |
| Custom PWA | Full control | 8 hours | Hosting | Excellent |
| Native iOS App | Best UX | 16 hours | Dev time | Excellent |

---

## AUTOMATION PLATFORMS

### Make.com (Integromat)

**Type:** Visual automation platform
**Claude Support:** Via HTTP module (not native)

**Specs:**
- Visual workflow builder
- 1,000+ app integrations
- Built-in error handling
- Scheduling and routing
- Webhook triggers

**Pricing:**
- Free: 1,000 operations/month
- Core: $9/month - 10,000 ops
- Pro: $16/month - 10,000 ops + advanced

**Your Use Case:**
- Rating: 9/10
- Perfect for YouTube → Summary → Tasks
- Easy to add transcript extraction
- Can integrate with any task system

**Pros:**
- Visual debugging
- Easy to modify
- Reliable
- Good free tier

**Cons:**
- Another dependency
- Learning curve for complex scenarios
- Operation limits on free tier

**Setup Guide:** See quick-start-ios-shortcut-make.md

---

### Zapier

**Type:** Automation platform
**Claude Support:** Via Webhooks or Code steps

**Specs:**
- 6,000+ app integrations
- More polished than Make
- Better documentation
- Easier for non-technical

**Pricing:**
- Free: 100 tasks/month (too low)
- Starter: $20/month - 750 tasks
- Professional: $49/month

**Your Use Case:**
- Rating: 7/10
- Works but more expensive than Make
- Better if you already use Zapier

**Pros:**
- Huge app ecosystem
- Very reliable
- Great support

**Cons:**
- Expensive for this use case
- Free tier too limited
- No native Claude support yet

---

### n8n

**Type:** Self-hosted automation (open source)
**Claude Support:** HTTP Request node

**Specs:**
- Unlimited workflows
- Full control
- Can modify source
- Docker deployment

**Pricing:**
- Self-hosted: Free (hosting costs only)
- Cloud: $20/month

**Your Use Case:**
- Rating: 6/10
- Overkill unless you're already hosting

**Pros:**
- Free (except hosting)
- Unlimited everything
- Full control

**Cons:**
- Need to maintain server
- Setup complexity
- Requires technical skills

---

## MOBILE APPS (BRING YOUR OWN KEY)

### Chatbox.ai

**Type:** Cross-platform chat client
**Platforms:** iOS, Android, macOS, Windows, Web
**Claude Support:** Yes, full API support

**Features:**
- Multiple AI providers
- Custom prompts
- Conversation history
- Markdown support
- Image support (when available)

**Pricing:**
- Free with your API key
- Optional Pro features

**Your Use Case:**
- Rating: 5/10
- Good for manual queries
- Not automation-friendly
- Can't integrate with task systems

**Pros:**
- Free
- Cross-platform
- Good UI
- Active development

**Cons:**
- Manual process
- No automation
- No integrations

**Download:** Search App Store for "Chatbox AI"

---

### TypingMind

**Type:** Web-based Claude client
**Platforms:** Web (works on mobile), iOS app
**Claude Support:** Full support

**Features:**
- Custom prompts library
- Folders and organization
- Search conversations
- Plugin system
- Voice input
- GPT-4, Claude, etc.

**Pricing:**
- One-time: $39 (lifetime)
- Or subscription: $8/month

**Your Use Case:**
- Rating: 6/10
- Better than Chatbox for repeated prompts
- Still manual
- No direct task integration

**Pros:**
- One-time payment option
- Custom prompt library
- Good for repeated tasks
- Plugin ecosystem

**Cons:**
- Costs money
- Still manual
- No automation

**URL:** https://typingmind.com

---

### OpenCat

**Type:** iOS/macOS native app
**Platforms:** iOS, iPadOS, macOS
**Claude Support:** Yes

**Features:**
- Native Apple design
- Multiple AI models
- Custom characters/prompts
- Siri shortcuts (limited)
- iCloud sync

**Pricing:**
- $9.99 one-time (iOS)
- $14.99 one-time (macOS)

**Your Use Case:**
- Rating: 5/10
- Nice UI but limited automation
- Siri Shortcuts integration is basic

**Pros:**
- Native Apple experience
- One-time payment
- Good for manual use

**Cons:**
- Limited automation
- No advanced integrations

**Download:** iOS App Store

---

### AI Chat & Ask AI Chatbot

**Type:** iOS app
**Platforms:** iOS
**Claude Support:** Check current version

**Note:** Multiple apps with similar names exist. Quality varies.

**Your Use Case:**
- Rating: 3/10
- Most are subscription-based
- Limited features
- Better free alternatives exist

**Recommendation:** Skip unless you find one with specific features you need.

---

## DEVELOPMENT FRAMEWORKS

### React Native + Anthropic SDK

**Type:** Cross-platform mobile framework
**Complexity:** Medium
**Time to MVP:** 8-16 hours

**Stack:**
```
React Native
+ @anthropic-ai/sdk (via polyfills)
+ React Navigation
+ AsyncStorage (for API key)
```

**Your Use Case:**
- Rating: 7/10
- Good if you know React
- Can deploy to iOS and Android
- Full customization

**Pros:**
- Cross-platform
- Use React knowledge
- Large ecosystem
- Hot reload

**Cons:**
- Heavier than native
- Need to handle API key security
- Deployment complexity

---

### Swift + SwiftUI

**Type:** Native iOS development
**Complexity:** Medium-High
**Time to MVP:** 8-12 hours

**Stack:**
```swift
SwiftUI (UI)
+ URLSession (networking)
+ Keychain (API key storage)
+ Share Extension (URL capture)
```

**Your Use Case:**
- Rating: 8/10
- Best performance
- Best UX possible
- iOS only

**Pros:**
- Native performance
- Native UX
- Full iOS features
- Secure key storage

**Cons:**
- iOS only
- Steeper learning curve
- Longer development time

**Starter Code:**
```swift
import Foundation

class ClaudeAPI {
    private let apiKey: String
    private let baseURL = "https://api.anthropic.com/v1/messages"

    init(apiKey: String) {
        self.apiKey = apiKey
    }

    func summarize(url: String) async throws -> String {
        var request = URLRequest(url: URL(string: baseURL)!)
        request.httpMethod = "POST"
        request.setValue(apiKey, forHTTPHeaderField: "x-api-key")
        request.setValue("2023-06-01", forHTTPHeaderField: "anthropic-version")
        request.setValue("application/json", forHTTPHeaderField: "content-type")

        let body: [String: Any] = [
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 1024,
            "messages": [
                [
                    "role": "user",
                    "content": "Summarize this YouTube video: \(url)"
                ]
            ]
        ]

        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(ClaudeResponse.self, from: data)

        return response.content.first?.text ?? ""
    }
}

struct ClaudeResponse: Codable {
    let content: [Content]

    struct Content: Codable {
        let text: String
    }
}
```

---

### Flutter

**Type:** Cross-platform mobile framework
**Complexity:** Medium
**Time to MVP:** 10-16 hours

**Your Use Case:**
- Rating: 6/10
- Good if you know Dart/Flutter
- Probably overkill for this

**Pros:**
- Cross-platform
- Fast development
- Beautiful UI

**Cons:**
- Need to learn Dart
- Larger app size
- Less native feel

---

## PROGRESSIVE WEB APPS

### Next.js + PWA

**Type:** React framework with PWA support
**Complexity:** Low-Medium
**Time to MVP:** 4-8 hours

**Stack:**
```
Next.js
+ next-pwa plugin
+ Anthropic SDK
+ Vercel deployment
```

**Your Use Case:**
- Rating: 8/10
- Great middle ground
- Easy to deploy
- Can add native features later

**Pros:**
- Fast development
- Free hosting (Vercel)
- Cross-platform
- Can install to home screen

**Cons:**
- Less native feel
- Requires internet
- Share sheet support limited

**Starter Template:**
```javascript
// pages/api/summarize.js
import Anthropic from '@anthropic-ai/sdk';

export default async function handler(req, res) {
  const { url } = req.body;

  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: `Summarize: ${url}`
    }]
  });

  res.json({ summary: message.content[0].text });
}
```

**Deploy:**
```bash
npm install next-pwa @anthropic-ai/sdk
# Add pwa config to next.config.js
vercel deploy
```

---

### SvelteKit + PWA

**Type:** Svelte framework with PWA support
**Complexity:** Low
**Time to MVP:** 4-6 hours

**Your Use Case:**
- Rating: 7/10
- Simpler than Next.js
- Smaller bundle size
- Less ecosystem

**Pros:**
- Very fast
- Clean code
- Small bundle
- Easy to learn

**Cons:**
- Smaller ecosystem
- Less resources
- Fewer integrations

---

## HELPER SERVICES

### Jina Reader API

**Purpose:** Clean webpage extraction
**Cost:** Free tier available
**Use:** Convert web pages to clean text for Claude

```bash
# Instead of sending URL to Claude
# Send cleaned content
curl https://r.jina.ai/https://example.com
```

**Your Use Case:**
- Rating: 9/10
- Perfect for article summarization
- Works with YouTube → transcript

---

### RapidAPI - YouTube Transcript

**Purpose:** Get YouTube video transcripts
**Cost:** Free tier: 500 requests/month
**Use:** Extract transcript before sending to Claude

**Your Use Case:**
- Rating: 9/10
- Essential for good video summaries
- Cheap/free

---

### Cloudflare Workers

**Purpose:** Serverless API proxy
**Cost:** Free tier: 100k requests/day
**Use:** Hide API keys from client

**Your Use Case:**
- Rating: 8/10
- Better than exposing key in Shortcut
- Free and fast
- Global edge network

**Example Worker:**
```javascript
export default {
  async fetch(request) {
    const { url } = await request.json();

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': ANTHROPIC_API_KEY, // env variable
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-5-20250929',
        max_tokens: 1024,
        messages: [{ role: 'user', content: `Summarize: ${url}` }]
      })
    });

    return response;
  }
}
```

---

## RECOMMENDATION BY SCENARIO

### "I want to test this idea today"
**Use:** iOS Shortcuts → Cloudflare Worker → Claude
- Time: 2 hours
- Cost: $0
- Setup: Medium complexity

### "I want a reliable workflow I can use daily"
**Use:** iOS Shortcuts → Make.com → Claude → Tasks
- Time: 1 hour
- Cost: $0-9/month
- Setup: Easy

### "I want to build a product others can use"
**Use:** Next.js PWA or Native iOS app
- Time: 8-40 hours
- Cost: Hosting + dev time
- Setup: High complexity

### "I just want to ask Claude questions on mobile"
**Use:** TypingMind or Chatbox.ai
- Time: 5 minutes
- Cost: $0-39
- Setup: Zero

### "I want the best possible mobile experience"
**Use:** Native Swift app
- Time: 16+ hours
- Cost: Dev time
- Setup: High complexity

---

## DECISION TREE

```
Do you need automation?
├─ No → Use Chatbox.ai or TypingMind
└─ Yes
   └─ How many videos per day?
      ├─ < 5 → iOS Shortcuts + Cloudflare Worker
      ├─ 5-20 → iOS Shortcuts + Make.com
      └─ > 20 → Custom app
         └─ iOS only or cross-platform?
            ├─ iOS only → Swift + SwiftUI
            └─ Cross-platform → Next.js PWA
```

---

## TECHNICAL REQUIREMENTS BY APPROACH

### iOS Shortcuts Only
**Skills needed:**
- None (visual builder)

**Time investment:**
- 30-60 minutes

**Ongoing maintenance:**
- Very low

---

### iOS Shortcuts + Make
**Skills needed:**
- Basic JSON understanding
- Basic automation concepts

**Time investment:**
- 1-2 hours initial
- 15 min per enhancement

**Ongoing maintenance:**
- Very low
- Occasional Make scenario update

---

### PWA (Next.js)
**Skills needed:**
- JavaScript/React
- API integration
- Basic deployment (Vercel)

**Time investment:**
- 4-8 hours MVP
- 2-4 hours per feature

**Ongoing maintenance:**
- Low
- Dependency updates
- API changes

---

### Native iOS (Swift)
**Skills needed:**
- Swift/SwiftUI
- iOS APIs
- Keychain
- Share Extensions
- URLSession

**Time investment:**
- 8-12 hours MVP
- 4-8 hours per feature

**Ongoing maintenance:**
- Medium
- iOS updates
- API changes
- TestFlight/App Store

---

## STARTER REPOS

### Swift iOS App Template
```
Search GitHub: "swift claude api example"
Suggested: anthropic-sdk-ios-example
```

### Next.js PWA Template
```
npx create-next-app my-claude-pwa
npm install next-pwa @anthropic-ai/sdk
```

### iOS Shortcut Template
```
Download: [Link to iCloud shared shortcut]
Customize: Add your webhook URL
```

---

## COMMON PITFALLS

### API Key Exposure
**Problem:** Storing key in Shortcut
**Solution:** Use webhook proxy (Make, Cloudflare, etc.)

### No Error Handling
**Problem:** Shortcut fails silently
**Solution:** Add "Show Notification" for errors

### Rate Limiting
**Problem:** Too many requests
**Solution:** Add debouncing/queueing

### Large Transcripts
**Problem:** Exceeding context window
**Solution:** Chunk or summarize transcript first

### Task System Integration
**Problem:** Can't add to preferred app
**Solution:** Use Make.com or Zapier for integrations

---

## NEXT STEPS

1. **Pick your approach** based on:
   - Technical skill
   - Time available
   - Usage volume
   - Budget

2. **Start with MVP:**
   - iOS Shortcut → Make → Claude → Notification
   - Test with 5-10 videos
   - Validate it solves your problem

3. **Iterate:**
   - Add transcript extraction
   - Add task system integration
   - Add custom prompts
   - Add filtering

4. **Graduate if needed:**
   - Move to PWA for better UX
   - Move to native for best experience
   - Move to SaaS if others want it

---

## RESOURCES

### Documentation
- Anthropic API: https://docs.anthropic.com
- Make.com: https://www.make.com/en/help
- iOS Shortcuts: https://support.apple.com/guide/shortcuts
- Cloudflare Workers: https://developers.cloudflare.com/workers

### Code Examples
- GitHub: "awesome-claude"
- GitHub: "claude api ios"
- GitHub: "anthropic sdk examples"

### Communities
- r/ClaudeAI (Reddit)
- Anthropic Discord
- iOS Shortcuts Reddit

---

**Last Updated:** 2026-01-02
**Version:** 1.0
