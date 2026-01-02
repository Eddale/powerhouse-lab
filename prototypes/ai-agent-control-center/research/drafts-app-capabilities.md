# Drafts App Research - Core Capabilities & Integration Potential

**Research Date:** January 2, 2026
**Purpose:** Evaluate Drafts as mobile capture inbox for Obsidian + Claude agent workflow

---

## 1. CORE CAPABILITIES

### What Drafts Does
Drafts is a "capture-first" text editor for iOS/iPadOS/macOS/watchOS that prioritizes quick text entry before deciding what to do with it.

**Core Philosophy:**
- Text goes in FIRST
- Decision about what to do with it comes SECOND
- "Where text starts" on Apple platforms

### Key Features
- **Instant Capture:** Opens to blank draft immediately (no navigation, no file naming)
- **Cross-platform:** iPhone, iPad, Mac, Apple Watch
- **Markdown Support:** Full markdown editing and preview
- **Workspace Organization:** Tag-based organization, saved filters/workspaces
- **Version History:** Every draft maintains complete edit history
- **Syntax Highlighting:** Supports multiple languages beyond markdown

---

## 2. ACTIONS SYSTEM

### What Are Actions?
Actions are the core automation engine in Drafts. They process text through steps like:
- Modify text (search/replace, templates, transformations)
- Send to other apps
- Run scripts
- Trigger HTTP requests
- Create files
- Send emails, messages, etc.

### Action Types
1. **Steps-based Actions** - Visual workflow builder
2. **Script Actions** - JavaScript automation
3. **Action Groups** - Organized collections shown in action bar
4. **Keyboard Shortcuts** - Assignable to any action

### Built-in Action Steps Include
- File operations (create, append, prepend)
- HTTP requests (GET, POST, etc.)
- Email, Messages, social media
- Text transformations
- Clipboard operations
- Prompt user input
- Conditional logic

### Action Directory
- Community-shared action library at https://directory.getdrafts.com
- Import actions via URL or QR code
- Customize any imported action

---

## 3. OBSIDIAN INTEGRATION

### Existing Obsidian Actions

**YES** - Multiple community actions exist for Drafts → Obsidian:

1. **"Append to Obsidian Note"**
   - Uses Obsidian's URL scheme (`obsidian://`)
   - Can append text to existing notes
   - Supports templates with date stamps, tags

2. **"Create Obsidian Daily Note"**
   - Creates or appends to daily note format
   - Common pattern: `YYYY-MM-DD.md`

3. **"Send to Obsidian Inbox"**
   - Sends draft to designated inbox note
   - Popular for GTD/capture workflows

### How They Work

**Method 1: URL Schemes**
```
obsidian://new?vault=VaultName&file=path/to/note&content=text
obsidian://advanced-uri (via Advanced URI plugin)
```

**Method 2: File System (Mac only)**
- Drafts can write directly to iCloud Drive folders
- If Obsidian vault is in iCloud Drive, Drafts can create/append to .md files
- Limitation: iOS sandboxing prevents direct file system access from Drafts on mobile

**Method 3: Shortcuts Integration**
- Drafts → Apple Shortcuts → Obsidian
- More flexible but requires Shortcuts app as bridge

### Community Resources
- Multiple Obsidian actions in Drafts Directory
- Active forum discussions about workflows
- Common pattern: Mobile capture in Drafts → Process in Obsidian desktop

---

## 4. SYNC MECHANISMS

### iCloud Sync (Primary Method)
- **Cross-platform:** All drafts sync via iCloud between iOS, iPadOS, macOS
- **Real-time:** Nearly instant sync when devices online
- **What Syncs:**
  - All draft content
  - Tags and metadata
  - Action groups (optional)
  - Workspaces
  - Themes and settings (optional)

### No Third-Party Sync
- Requires iCloud account
- No Dropbox, Google Drive, or other sync options
- Drafts data stays in iCloud

### Offline Capability
- Full functionality offline
- Syncs when connection restored
- No data loss risk

---

## 5. AUTOMATION CAPABILITIES

### Scripting Engine
**JavaScript (ES6+)** with extensive object model:

```javascript
// Example: Process draft and send to webhook
let d = draft.content;
let http = HTTP.create();
let response = http.request({
  "url": "https://your-webhook.com/endpoint",
  "method": "POST",
  "data": { "content": d },
  "headers": { "Content-Type": "application/json" }
});
```

### What Scripts Can Do
- Full access to draft content, tags, metadata
- Create/modify/delete drafts programmatically
- HTTP requests (webhooks, APIs)
- File system operations (Mac only)
- Prompt user for input
- Conditional logic and loops
- Access to system clipboard
- Date/time manipulation
- Text parsing and transformation

### External Integration Methods

1. **Webhooks/APIs**
   - HTTP requests via script or action steps
   - Can trigger Zapier, Make.com, n8n workflows
   - Can call custom APIs (including Claude API theoretically)

2. **Apple Shortcuts**
   - Drafts has deep Shortcuts integration
   - Can pass drafts to Shortcuts
   - Shortcuts can create/modify Drafts
   - Shortcuts can run Drafts actions

3. **x-callback-url**
   - Advanced URL scheme for chaining apps
   - Can trigger Drafts actions from other apps
   - Can return data to calling app

4. **Email**
   - Each Drafts account gets unique email address
   - Email → Drafts creates new draft
   - Good for external systems that can send email

---

## 6. URL SCHEMES

### Primary Schemes

**Basic URL Scheme:**
```
drafts://
```

**Common URL Actions:**

1. **Create New Draft**
```
drafts://create?text=Your+text+here
```

2. **Open Existing Draft**
```
drafts://open?uuid=[draft-uuid]
```

3. **Run Action on Text**
```
drafts://action?text=content&action=ActionName
```

4. **Search**
```
drafts://search?query=searchterm
```

5. **x-callback-url Support**
```
drafts://x-callback-url/create?text=content&x-success=[url]&x-error=[url]
```

### Use Cases for URL Schemes
- Trigger Drafts capture from other apps
- Deep link to specific drafts
- Run actions programmatically
- Chain actions between apps
- Create shortcuts that interact with Drafts

### Documentation
Full URL scheme documentation at: https://docs.getdrafts.com/docs/automation/urlschemes

---

## 7. APPLE WATCH & WIDGET SUPPORT

### Apple Watch

**Quick Capture:**
- Dictation to new draft
- Complications for watch face (tap to capture)
- Recently modified drafts list
- Run actions on drafts
- Predefined text snippets

**Limitations:**
- Text input via dictation or scribble only
- Limited action support (simple actions work)
- Syncs via iPhone

**Use Case:**
Perfect for "I need to remember this NOW" moments - dictate, it syncs to all devices instantly.

### iOS Widgets

**Multiple Widget Types:**

1. **Quick Capture Widget**
   - Tap to create new draft
   - Multiple sizes (small, medium, large)
   - Can specify default tags

2. **Recent Drafts Widget**
   - Shows recent drafts
   - Tap to open
   - Configurable count

3. **Action Widget**
   - Shows specific workspace/tags
   - Quick access to draft + run action
   - Custom action buttons

4. **Action List Widget**
   - Run specific actions from home screen
   - No need to open app

### Lock Screen Widgets (iOS 16+)
- Quick capture button
- View recent draft
- Circular or rectangular formats

---

## 8. INTEGRATION ARCHITECTURE FOR YOUR WORKFLOW

### Proposed Flow: Drafts → Obsidian → Claude Agent

```
Mobile Capture (Drafts)
    ↓
[Action: Send to Obsidian Inbox]
    ↓
Obsidian Vault (Inbox folder)
    ↓
[Obsidian on Mac syncs via iCloud]
    ↓
Claude Agent watches Inbox folder
    ↓
Process with AI, route to appropriate project
```

### Implementation Paths

**Option 1: Direct File Write (Mac Only)**
- Drafts action writes to Obsidian vault folder in iCloud Drive
- Limitation: Only works on Mac, not iOS

**Option 2: URL Scheme (Cross-platform)**
- Drafts action → Obsidian URL scheme → Creates note
- Works on all platforms
- Requires Obsidian Advanced URI plugin for flexibility

**Option 3: Webhook Bridge (Most Flexible)**
```
Drafts → Webhook → Cloud Function → Obsidian API/File
                    ↓
              Can trigger Claude agent directly
```

**Option 4: Shortcuts Bridge**
```
Drafts → Apple Shortcut → File System → Obsidian folder
                         ↓
                    Can add metadata, formatting
```

### Recommended Approach for Your Use Case

**Two-Stage Setup:**

**Stage 1: Mobile Capture**
- Drafts widget/Watch for instant capture
- Simple action: Tag as "inbox" + timestamp
- Optionally: Basic categorization via prompt or tags

**Stage 2: Sync to Obsidian**
- Mac: Direct file write to Obsidian inbox folder
- iOS: URL scheme to Obsidian or Shortcuts bridge
- Claude agent monitors inbox folder for new files

**Stage 3: Agent Processing**
- Claude agent runs on schedule or file watch
- Processes inbox items
- Routes to appropriate projects/agents
- Archives or deletes from inbox

---

## 9. TECHNICAL SPECIFICATIONS

### Platforms
- iOS 15+
- iPadOS 15+
- macOS 12+
- watchOS 8+

### Subscription Model
- Free version: Limited actions, basic features
- Pro subscription: Full features, unlimited actions
  - Monthly or annual
  - Separate purchase per platform (iOS vs Mac) - CHECK CURRENT STATUS

### Storage
- Drafts stored in iCloud
- No local-only option
- Each draft can be massive (no practical size limit mentioned)
- Thousands of drafts supported

### Export Options
- Plain text
- Markdown
- JSON (for backup/migration)
- Can export entire database

---

## 10. COMMUNITY & RESOURCES

### Official Resources
- Main site: https://getdrafts.com
- Documentation: https://docs.getdrafts.com
- Action Directory: https://directory.getdrafts.com
- Forums: https://forums.getdrafts.com

### Learning Resources
- Extensive scripting reference
- Action development guide
- Video tutorials
- Community forums very active

### Popular Workflows Documented
- GTD capture and processing
- Daily notes and journaling
- Blog post drafting
- Task management integration
- Email composition
- Social media posting

---

## 11. LIMITATIONS & CONSIDERATIONS

### What Drafts Doesn't Do Well
- **Not a full text editor:** No advanced formatting, images, etc.
- **iCloud only:** If you hate iCloud, this won't work
- **No collaboration:** Single-user tool
- **No end-to-end encryption:** Standard iCloud encryption only
- **Learning curve:** Action/scripting system takes time to master

### Privacy Considerations
- Data stored in iCloud
- Can use email-to-Drafts (goes through Agile Tortoise servers briefly)
- Actions can send data anywhere (user-controlled)

---

## 12. VERDICT FOR YOUR USE CASE

### Strengths for Obsidian + Claude Workflow

✅ **Fastest capture on iOS/Watch**
- Literally 1-2 seconds from thought to captured text
- No other tool is faster on Apple platforms

✅ **Powerful automation**
- Can format, tag, route text before sending to Obsidian
- JavaScript scripting = complex logic possible

✅ **Multiple integration paths**
- URL schemes, webhooks, file system, Shortcuts
- Can build whatever bridge you need

✅ **Reliable sync**
- iCloud sync is fast and dependable
- No weird edge cases

✅ **Apple Watch = game changer**
- Capture without phone out of pocket
- Friction is the enemy of capture - this eliminates it

### Potential Friction Points

⚠️ **iCloud dependency**
- If iCloud is down, sync stops
- Requires Apple ecosystem

⚠️ **Learning curve**
- Setting up actions takes time initially
- Worth it, but not instant

⚠️ **iOS → Obsidian not direct**
- Need URL scheme or Shortcuts bridge
- Mac can write files directly

### Recommendation

**YES - Drafts is ideal for this workflow**

Best architecture:
1. **Capture:** Drafts (iOS/Watch/Mac)
2. **Format:** Drafts action adds metadata, timestamps, tags
3. **Transfer:** URL scheme to Obsidian OR Shortcuts to write file
4. **Process:** Claude agent monitors Obsidian inbox folder
5. **Route:** Agent files to appropriate project/workflow

The speed of capture alone makes this worth it. The 3 seconds saved vs opening Obsidian on mobile = 10x more ideas captured.

---

## 13. NEXT STEPS TO TEST

1. **Install Drafts** (free version to test)
2. **Test basic capture** from Watch/widget
3. **Install Obsidian Advanced URI plugin**
4. **Create test action:** Drafts → Obsidian inbox note
5. **Verify sync** to desktop Obsidian
6. **Build simple Claude agent** to watch inbox folder
7. **Iterate on metadata format** that works for routing

---

## ADDITIONAL RESOURCES TO EXPLORE

- Drafts Field Guide: https://www.thoughtasylum.com/drafts/ (community resource)
- Rosemary Orchard's Drafts workflows (search her blog)
- MacSparky's Drafts coverage
- r/draftsapp on Reddit

---

**Document Status:** Initial research complete
**Confidence Level:** High (based on knowledge through Jan 2025)
**Validation Needed:** Current subscription model, iOS 18+ features, latest Obsidian integration methods

**Note:** Some specifics may have changed since my knowledge cutoff. Recommend verifying:
- Current pricing structure
- iOS 18/macOS 15 specific features
- Latest Obsidian Advanced URI capabilities
- Any new native integrations announced
