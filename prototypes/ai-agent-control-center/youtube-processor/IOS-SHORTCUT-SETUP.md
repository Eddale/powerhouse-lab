# iOS Shortcut Setup - Quick Reference

Copy-paste configuration for your iOS Shortcut.

---

## Basic Shortcut (Minimal)

**4 Actions. 2 minutes to set up.**

### Action 1: Ask for Input
```
Question: YouTube URL to summarize
Type: URL
Default Answer: [leave empty]
```

### Action 2: Get Contents of URL
```
URL: https://YOUR-API-URL.railway.app/process
Method: POST

Headers:
  Content-Type: application/json

Request Body: JSON
{
  "url": "PROVIDED_INPUT",
  "summary_type": "detailed"
}
```

**Important**: Replace `PROVIDED_INPUT` with the magic variable from Action 1.

### Action 3: Get Dictionary Value
```
Get: markdown_output
From: Contents of URL
```

### Action 4: Copy to Clipboard
```
[Dictionary Value from previous action]
```

**Done.** Run the shortcut, paste URL, get summary on clipboard.

---

## Advanced Shortcut (Save to Obsidian)

Add these actions after Action 3:

### Action 5: Set Variable
```
Variable Name: Summary
Value: [Dictionary Value]
```

### Action 6: Get Current Date
```
Format: Custom
Date Format: yyyy-MM-dd-HHmm
```

### Action 7: Set Variable
```
Variable Name: Timestamp
Value: [Current Date]
```

### Action 8: Save File
```
Service: iCloud Drive
File Path: Shortcuts/YouTube/YT-[Timestamp].md
Contents: [Summary]
Overwrite if File Exists: Yes
```

---

## Expert Shortcut (With Menu)

Lets you choose summary type before processing.

### Action 1: Ask for Input
(same as basic)

### Action 2: Choose from Menu
```
Prompt: Summary Type
Menu Items:
  - Quick Summary
  - Detailed Analysis
  - Bullet Points
```

### Action 3a: (Inside "Quick Summary")
Set Variable:
```
Variable: SummaryType
Value: brief
```

### Action 3b: (Inside "Detailed Analysis")
Set Variable:
```
Variable: SummaryType
Value: detailed
```

### Action 3c: (Inside "Bullet Points")
Set Variable:
```
Variable: SummaryType
Value: bullets
```

### Action 4: Get Contents of URL
```
URL: https://YOUR-API-URL.railway.app/process
Method: POST
Headers:
  Content-Type: application/json

Request Body: JSON
{
  "url": "PROVIDED_INPUT",
  "summary_type": "SUMMARYTYPE_VARIABLE"
}
```

### Action 5-8: Same as Advanced version above

---

## Share Sheet Integration

**Make it work from YouTube app:**

1. Edit your Shortcut
2. Tap the info icon (ⓘ)
3. Enable "Show in Share Sheet"
4. Under "Share Sheet Types":
   - Enable: **URLs**
   - Enable: **Safari Web Pages**

Now:
- Open YouTube app
- Tap Share on any video
- Select your Shortcut
- Get instant summary

---

## Troubleshooting

### "Invalid Response"
- Your API might be down
- Test in browser: `https://your-api-url/health`

### "Could not connect to server"
- Check URL is `https://` not `http://`
- Verify Railway/Render deployment is running

### "No transcript found"
- Video doesn't have transcripts
- Not a Shortcut issue - try different video

### Summary is cut off
- Increase `max_tokens` in `main.py`
- Change from 2000 to 4000 for longer summaries

---

## Example URLs to Test

These all have transcripts:

1. **TED Talk**: `https://www.youtube.com/watch?v=8S0FDjFBj8o`
2. **Tutorial**: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. **Interview**: Any recent YouTube interview

---

## Copy-Paste JSON for Shortcuts

### Request Body (Method 1: Basic)
```json
{
  "url": "PROVIDED_INPUT",
  "summary_type": "detailed"
}
```

### Request Body (Method 2: With Variables)
```json
{
  "url": "YOUTUBE_URL_VARIABLE",
  "summary_type": "SUMMARY_TYPE_VARIABLE"
}
```

**Remember**: In iOS Shortcuts, tap to add Magic Variables - don't type these literally.

---

## Widget Setup (iOS 14+)

1. **Create Shortcut** (as above)
2. **Add to Home Screen**:
   - Long press home screen
   - Tap + (top left)
   - Search "Shortcuts"
   - Select widget size
   - Tap widget → Choose Shortcut

Now you have a one-tap YouTube summarizer on your home screen.

---

## Siri Integration

Your shortcut automatically works with Siri.

Just say:
> "Hey Siri, [Shortcut Name]"

Siri will:
1. Ask for YouTube URL
2. Process it
3. Save to Obsidian or copy to clipboard

---

## Advanced: Multiple Shortcuts for Different Use Cases

Create 3 separate shortcuts:

### 1. "Quick YT Summary"
- summary_type: `brief`
- Action: Copy to clipboard
- **Use case**: Fast summaries while browsing

### 2. "Deep YT Analysis"
- summary_type: `detailed`
- Action: Save to Obsidian
- **Use case**: Research videos you want to reference

### 3. "YT Key Points"
- summary_type: `bullets`
- Action: Copy to clipboard
- **Use case**: Quick takeaways for sharing

All hit the same API, different configs.

---

## Security Note

If you add API key authentication (see DEPLOYMENT.md), add this header:

```
Headers:
  Content-Type: application/json
  X-API-Key: your_secret_key_here
```

**Better**: Store API key in a Shortcut variable so you can update it once.

---

## Performance Tips

1. **Transcript length matters**:
   - 5min video: ~5-10 seconds
   - 30min video: ~15-30 seconds
   - 2hr video: ~60-90 seconds

2. **Summary type affects speed**:
   - `brief`: Fastest
   - `bullets`: Medium
   - `detailed`: Slowest (but still under 30s usually)

3. **Cold starts** (Render free tier):
   - First request after inactivity: ~30s
   - Subsequent requests: 5-15s
   - Railway doesn't have this issue

---

## Next Level: Automation

### Auto-process videos from a playlist

1. Use Shortcuts' **"Get URLs from Input"** action
2. Use **"Repeat with Each"** to loop
3. Process each video
4. Combine all summaries into one note

Example:
```
Get URLs from Input →
Repeat with Each URL →
  Call API →
  Append to variable →
End Repeat →
Save combined file
```

---

**You're set. Start summarizing.**
