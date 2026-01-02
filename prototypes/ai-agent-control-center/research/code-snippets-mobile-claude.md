# Copy-Paste Code Snippets for Mobile Claude Integration

**Quick reference for implementing mobile → Claude → tasks workflows**

---

## TABLE OF CONTENTS

1. [Cloudflare Worker Proxy](#cloudflare-worker-proxy)
2. [Next.js API Route](#nextjs-api-route)
3. [Swift iOS App](#swift-ios-app)
4. [iOS Shortcut JSON](#ios-shortcut-json)
5. [Make.com Scenarios](#makecom-scenarios)
6. [YouTube Transcript Extraction](#youtube-transcript-extraction)
7. [Helper Functions](#helper-functions)

---

## CLOUDFLARE WORKER PROXY

### Basic Claude API Proxy

```javascript
// worker.js
export default {
  async fetch(request, env) {
    // Only allow POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const { url, prompt } = await request.json();

      // Call Claude API
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-5-20250929',
          max_tokens: 1024,
          messages: [{
            role: 'user',
            content: prompt || `Summarize this URL: ${url}`
          }]
        })
      });

      const data = await response.json();

      return new Response(JSON.stringify({
        success: true,
        summary: data.content[0].text
      }), {
        headers: { 'content-type': 'application/json' }
      });

    } catch (error) {
      return new Response(JSON.stringify({
        success: false,
        error: error.message
      }), {
        status: 500,
        headers: { 'content-type': 'application/json' }
      });
    }
  }
};
```

### With Authentication

```javascript
// worker.js with auth token
export default {
  async fetch(request, env) {
    // Check auth token
    const authToken = request.headers.get('X-Auth-Token');
    if (authToken !== env.AUTH_TOKEN) {
      return new Response('Unauthorized', { status: 401 });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const { url } = await request.json();

      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-5-20250929',
          max_tokens: 1024,
          messages: [{
            role: 'user',
            content: `Summarize this YouTube video and extract 3-5 action items:\n\n${url}`
          }]
        })
      });

      const data = await response.json();

      return new Response(JSON.stringify({
        success: true,
        summary: data.content[0].text,
        url: url
      }), {
        headers: { 'content-type': 'application/json' }
      });

    } catch (error) {
      return new Response(JSON.stringify({
        success: false,
        error: error.message
      }), {
        status: 500,
        headers: { 'content-type': 'application/json' }
      });
    }
  }
};
```

### Deploy to Cloudflare

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Create new worker
wrangler init youtube-summarizer

# Copy code to src/worker.js

# Add secrets
wrangler secret put ANTHROPIC_API_KEY
wrangler secret put AUTH_TOKEN

# Deploy
wrangler deploy

# Get URL
# https://youtube-summarizer.YOUR_SUBDOMAIN.workers.dev
```

---

## NEXT.JS API ROUTE

### Basic Summarize Endpoint

```javascript
// pages/api/summarize.js
import Anthropic from '@anthropic-ai/sdk';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  try {
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: `Summarize this YouTube video: ${url}`
      }]
    });

    res.status(200).json({
      success: true,
      summary: message.content[0].text
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
```

### With YouTube Transcript

```javascript
// pages/api/summarize-video.js
import Anthropic from '@anthropic-ai/sdk';
import { YoutubeTranscript } from 'youtube-transcript';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url } = req.body;

  try {
    // Extract video ID
    const videoId = extractVideoId(url);

    // Get transcript
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    const transcriptText = transcript
      .map(item => item.text)
      .join(' ');

    // Summarize with Claude
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 2048,
      messages: [{
        role: 'user',
        content: `Video: ${url}\n\nTranscript:\n${transcriptText}\n\nProvide:\n1. Brief summary (2-3 sentences)\n2. Key points (bullet list)\n3. Action items (if any)`
      }]
    });

    res.status(200).json({
      success: true,
      summary: message.content[0].text,
      transcriptLength: transcriptText.length
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

function extractVideoId(url) {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/,
    /youtube\.com\/embed\/([^&\n?#]+)/,
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }

  throw new Error('Invalid YouTube URL');
}
```

### Deploy to Vercel

```bash
# Install dependencies
npm install @anthropic-ai/sdk youtube-transcript

# Add to .env.local
ANTHROPIC_API_KEY=your_key_here

# Deploy
vercel deploy

# Set environment variable
vercel env add ANTHROPIC_API_KEY

# Get URL
# https://your-app.vercel.app/api/summarize
```

---

## SWIFT iOS APP

### Basic Claude Service

```swift
// ClaudeService.swift
import Foundation

class ClaudeService {
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

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ClaudeError.invalidResponse
        }

        let claudeResponse = try JSONDecoder().decode(ClaudeResponse.self, from: data)
        return claudeResponse.content.first?.text ?? ""
    }
}

struct ClaudeResponse: Codable {
    let content: [Content]

    struct Content: Codable {
        let text: String
    }
}

enum ClaudeError: Error {
    case invalidResponse
    case noContent
}
```

### SwiftUI View

```swift
// ContentView.swift
import SwiftUI

struct ContentView: View {
    @State private var url: String = ""
    @State private var summary: String = ""
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?

    let claudeService = ClaudeService(apiKey: "YOUR_API_KEY") // TODO: Load from Keychain

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                TextField("YouTube URL", text: $url)
                    .textFieldStyle(.roundedBorder)
                    .autocapitalization(.none)

                Button("Summarize") {
                    Task {
                        await summarize()
                    }
                }
                .disabled(url.isEmpty || isLoading)

                if isLoading {
                    ProgressView()
                }

                if !summary.isEmpty {
                    ScrollView {
                        Text(summary)
                            .padding()
                    }
                }

                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                }

                Spacer()
            }
            .padding()
            .navigationTitle("YouTube Summarizer")
        }
    }

    func summarize() async {
        isLoading = true
        errorMessage = nil
        summary = ""

        do {
            summary = try await claudeService.summarize(url: url)
        } catch {
            errorMessage = "Error: \(error.localizedDescription)"
        }

        isLoading = false
    }
}
```

### Keychain Storage for API Key

```swift
// KeychainHelper.swift
import Foundation
import Security

class KeychainHelper {
    static let shared = KeychainHelper()

    func save(_ value: String, forKey key: String) -> Bool {
        guard let data = value.data(using: .utf8) else { return false }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)

        return status == errSecSuccess
    }

    func get(forKey key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            return nil
        }

        return value
    }
}

// Usage
KeychainHelper.shared.save("your_api_key", forKey: "anthropic_api_key")
let apiKey = KeychainHelper.shared.get(forKey: "anthropic_api_key")
```

### Share Extension

```swift
// ShareViewController.swift (in Share Extension target)
import UIKit
import Social

class ShareViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        guard let extensionItem = extensionContext?.inputItems.first as? NSExtensionItem,
              let itemProvider = extensionItem.attachments?.first else {
            extensionContext?.completeRequest(returningItems: nil, completionHandler: nil)
            return
        }

        if itemProvider.hasItemConformingToTypeIdentifier("public.url") {
            itemProvider.loadItem(forTypeIdentifier: "public.url", options: nil) { (url, error) in
                if let shareURL = url as? URL {
                    self.handleURL(shareURL.absoluteString)
                }
            }
        }
    }

    func handleURL(_ url: String) {
        Task {
            do {
                let apiKey = KeychainHelper.shared.get(forKey: "anthropic_api_key") ?? ""
                let service = ClaudeService(apiKey: apiKey)
                let summary = try await service.summarize(url: url)

                // Save to Reminders or clipboard
                UIPasteboard.general.string = summary

                DispatchQueue.main.async {
                    self.extensionContext?.completeRequest(returningItems: nil, completionHandler: nil)
                }
            } catch {
                print("Error: \(error)")
            }
        }
    }
}
```

---

## IOS SHORTCUT JSON

### Basic Shortcut Structure

```json
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.receiveinput",
      "WFWorkflowActionParameters": {
        "WFInputContentItemClasses": ["WFURLContentItem"]
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.geturl",
      "WFWorkflowActionParameters": {
        "WFURLActionURL": "YOUR_WEBHOOK_URL"
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.downloadurl",
      "WFWorkflowActionParameters": {
        "WFHTTPMethod": "POST",
        "WFHTTPHeaders": {
          "Content-Type": "application/json"
        },
        "WFHTTPBodyType": "JSON",
        "WFJSONValues": {
          "url": "{{Input}}"
        }
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.getdictionaryvalue",
      "WFWorkflowActionParameters": {
        "WFDictionaryKey": "summary"
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.addnewreminder",
      "WFWorkflowActionParameters": {
        "WFCalendarItemTitle": "YouTube Summary",
        "WFCalendarItemNotes": "{{Dictionary Value}}"
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.notification",
      "WFWorkflowActionParameters": {
        "WFNotificationActionBody": "Added to tasks!"
      }
    }
  ],
  "WFWorkflowInputContentItemClasses": ["WFURLContentItem"],
  "WFWorkflowTypes": ["ActionExtension"]
}
```

---

## MAKE.COM SCENARIOS

### JSON Blueprint (Import to Make)

```json
{
  "name": "YouTube to Tasks via Claude",
  "flow": [
    {
      "id": 1,
      "module": "webhooks:webhook",
      "parameters": {
        "hook": "youtube-summarize"
      }
    },
    {
      "id": 2,
      "module": "http:ActionSendData",
      "parameters": {
        "url": "https://api.anthropic.com/v1/messages",
        "method": "POST",
        "headers": [
          {
            "name": "x-api-key",
            "value": "{{YOUR_API_KEY}}"
          },
          {
            "name": "anthropic-version",
            "value": "2023-06-01"
          },
          {
            "name": "content-type",
            "value": "application/json"
          }
        ],
        "bodyType": "raw",
        "body": {
          "model": "claude-sonnet-4-5-20250929",
          "max_tokens": 1024,
          "messages": [
            {
              "role": "user",
              "content": "Summarize this YouTube video: {{1.url}}"
            }
          ]
        }
      }
    },
    {
      "id": 3,
      "module": "json:ParseJSON",
      "parameters": {
        "json": "{{2.data}}"
      }
    },
    {
      "id": 4,
      "module": "todoist:createTask",
      "parameters": {
        "content": "YouTube Summary",
        "description": "{{3.content[0].text}}\n\nSource: {{1.url}}"
      }
    },
    {
      "id": 5,
      "module": "webhooks:webhookResponse",
      "parameters": {
        "status": "200",
        "body": {
          "success": true,
          "summary": "{{3.content[0].text}}"
        }
      }
    }
  ]
}
```

---

## YOUTUBE TRANSCRIPT EXTRACTION

### Node.js with youtube-transcript Package

```javascript
// transcript.js
import { YoutubeTranscript } from 'youtube-transcript';

async function getTranscript(url) {
  try {
    const videoId = extractVideoId(url);
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);

    return transcript.map(item => item.text).join(' ');
  } catch (error) {
    console.error('Error fetching transcript:', error);
    throw error;
  }
}

function extractVideoId(url) {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/,
    /youtube\.com\/embed\/([^&\n?#]+)/,
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }

  throw new Error('Invalid YouTube URL');
}

// Usage
const transcript = await getTranscript('https://youtube.com/watch?v=VIDEO_ID');
console.log(transcript);
```

### Python with youtube-transcript-api

```python
# transcript.py
from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_transcript(url):
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    return ' '.join([item['text'] for item in transcript])

def extract_video_id(url):
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError('Invalid YouTube URL')

# Usage
transcript = get_transcript('https://youtube.com/watch?v=VIDEO_ID')
print(transcript)
```

### Using RapidAPI (HTTP Request)

```javascript
// rapidapi-transcript.js
async function getTranscriptViaRapidAPI(videoId) {
  const response = await fetch(
    `https://youtube-transcript3.p.rapidapi.com/api/transcript?videoId=${videoId}`,
    {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY',
        'X-RapidAPI-Host': 'youtube-transcript3.p.rapidapi.com'
      }
    }
  );

  const data = await response.json();
  return data.transcript.map(item => item.text).join(' ');
}
```

---

## HELPER FUNCTIONS

### Chunk Long Text for Claude

```javascript
// chunker.js
function chunkText(text, maxChunkSize = 3000) {
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  const chunks = [];
  let currentChunk = '';

  for (const sentence of sentences) {
    if ((currentChunk + sentence).length > maxChunkSize) {
      if (currentChunk) chunks.push(currentChunk.trim());
      currentChunk = sentence;
    } else {
      currentChunk += sentence;
    }
  }

  if (currentChunk) chunks.push(currentChunk.trim());

  return chunks;
}

// Usage with Claude
async function summarizeLongTranscript(transcript) {
  const chunks = chunkText(transcript, 3000);
  const summaries = [];

  for (const chunk of chunks) {
    const summary = await claudeService.summarize(chunk);
    summaries.push(summary);
  }

  // Final summary of summaries
  const finalSummary = await claudeService.summarize(
    `Combine these summaries into one cohesive summary:\n\n${summaries.join('\n\n')}`
  );

  return finalSummary;
}
```

### Detect Content Type

```javascript
// detector.js
function detectContentType(url) {
  const patterns = {
    youtube: /(?:youtube\.com|youtu\.be)/,
    article: /medium\.com|substack\.com|dev\.to/,
    tweet: /twitter\.com|x\.com/,
    pdf: /\.pdf$/,
  };

  for (const [type, pattern] of Object.entries(patterns)) {
    if (pattern.test(url)) return type;
  }

  return 'unknown';
}

// Different prompts per type
const prompts = {
  youtube: 'Summarize this YouTube video and extract key action items:',
  article: 'Summarize this article and highlight the main arguments:',
  tweet: 'Summarize this tweet thread:',
  pdf: 'Summarize this document:',
};

function getPrompt(url, content) {
  const type = detectContentType(url);
  const prompt = prompts[type] || 'Summarize this content:';
  return `${prompt}\n\n${content}`;
}
```

### Rate Limiter

```javascript
// rateLimiter.js
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }

  async acquire() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.windowMs);

    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = this.requests[0];
      const waitTime = this.windowMs - (now - oldestRequest);
      await new Promise(resolve => setTimeout(resolve, waitTime));
      return this.acquire();
    }

    this.requests.push(now);
  }
}

// Usage
const limiter = new RateLimiter(5, 60000); // 5 requests per minute

async function callClaude(prompt) {
  await limiter.acquire();
  return claudeService.summarize(prompt);
}
```

### Error Handler

```javascript
// errorHandler.js
async function withRetry(fn, maxRetries = 3, delay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;

      console.log(`Retry ${i + 1}/${maxRetries} after error:`, error.message);
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
    }
  }
}

// Usage
const summary = await withRetry(() =>
  claudeService.summarize(url)
);
```

---

## COMPLETE EXAMPLE: PWA WITH ALL FEATURES

```javascript
// pages/api/summarize-full.js
import Anthropic from '@anthropic-ai/sdk';
import { YoutubeTranscript } from 'youtube-transcript';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url } = req.body;

  try {
    // Detect content type
    const contentType = detectContentType(url);

    // Get content
    let content = '';
    if (contentType === 'youtube') {
      const videoId = extractVideoId(url);
      const transcript = await YoutubeTranscript.fetchTranscript(videoId);
      content = transcript.map(item => item.text).join(' ');
    } else {
      // For other URLs, use Jina Reader
      const response = await fetch(`https://r.jina.ai/${url}`);
      content = await response.text();
    }

    // Chunk if needed
    const chunks = chunkText(content, 3000);
    let summary;

    if (chunks.length === 1) {
      summary = await summarizeWithClaude(chunks[0], contentType);
    } else {
      const summaries = await Promise.all(
        chunks.map(chunk => summarizeWithClaude(chunk, contentType))
      );
      summary = await summarizeWithClaude(
        summaries.join('\n\n'),
        'summary'
      );
    }

    res.status(200).json({
      success: true,
      summary,
      contentType,
      chunkCount: chunks.length
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

async function summarizeWithClaude(content, type) {
  const prompts = {
    youtube: 'Summarize this YouTube video transcript. Include: 1) Brief summary 2) Key points 3) Action items',
    article: 'Summarize this article. Include main arguments and conclusions.',
    summary: 'Create a cohesive summary from these individual summaries:',
  };

  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 2048,
    messages: [{
      role: 'user',
      content: `${prompts[type] || prompts.article}\n\n${content}`
    }]
  });

  return message.content[0].text;
}

function detectContentType(url) {
  if (/(?:youtube\.com|youtu\.be)/.test(url)) return 'youtube';
  return 'article';
}

function extractVideoId(url) {
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/);
  if (!match) throw new Error('Invalid YouTube URL');
  return match[1];
}

function chunkText(text, maxChunkSize) {
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  const chunks = [];
  let currentChunk = '';

  for (const sentence of sentences) {
    if ((currentChunk + sentence).length > maxChunkSize) {
      if (currentChunk) chunks.push(currentChunk.trim());
      currentChunk = sentence;
    } else {
      currentChunk += sentence;
    }
  }

  if (currentChunk) chunks.push(currentChunk.trim());
  return chunks;
}
```

---

## TESTING

### Test Cloudflare Worker Locally

```bash
# Install wrangler
npm install -g wrangler

# Run locally
wrangler dev

# Test with curl
curl -X POST http://localhost:8787 \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Test Next.js API Route

```bash
# Start dev server
npm run dev

# Test with curl
curl -X POST http://localhost:3000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Test iOS Shortcut

1. Create shortcut with test URL hardcoded
2. Run from Shortcuts app (not share sheet first)
3. Check notification for errors
4. Add logging to webhook to see what's received

---

## SECURITY CHECKLIST

- [ ] API keys in environment variables (never in code)
- [ ] Webhook URLs not committed to Git
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] HTTPS only
- [ ] Authentication on webhooks (optional but recommended)
- [ ] Error messages don't leak sensitive info
- [ ] API key stored in Keychain (iOS apps)
- [ ] CORS configured properly (PWAs)

---

## DEPLOYMENT CHECKLIST

- [ ] Environment variables set
- [ ] Secrets configured
- [ ] DNS/domain configured (if needed)
- [ ] SSL certificate (automatic on Vercel/Cloudflare)
- [ ] Test in production
- [ ] Monitor first few requests
- [ ] Set up error logging
- [ ] Document webhook URL
- [ ] Add to password manager

---

**Ready to copy and paste!**

Each snippet is production-ready with minor customization (API keys, URLs, etc.)
