# Google API Key Setup Guide

**For:** Carousel image generation with `gemini-3-pro-image-preview`
**Time:** ~10 minutes
**Cost:** Pay-as-you-go (~$0.134 per image)

---

## Part 1: Generate Your API Key

### Step 1: Go to Google AI Studio

Open in your browser:
```
https://aistudio.google.com/apikey
```

You'll need to sign in with your Google account.

### Step 2: Create API Key

1. Click **"Create API key"** (blue button)

2. You'll see two options:
   - **"Create API key in new project"** - Choose this if you don't have a project
   - **"Create API key in existing project"** - Choose this if you already have a Google Cloud project

3. Click your choice. Google creates the key instantly.

4. **IMPORTANT:** Copy the key immediately. It looks like:
   ```
   AIzaSyD-EXAMPLE-KEY-HERE-1234567890abc
   ```

   You won't be able to see the full key again after closing this dialog.

### Step 3: Enable Billing (Required for API Use)

The free tier in AI Studio web interface doesn't extend to API calls. You need billing enabled.

1. Go to: `https://console.cloud.google.com/billing`

2. If prompted, select the project where you created your API key

3. Click **"Link a billing account"** or **"Enable billing"**

4. Add a payment method (credit card)

5. Set a budget alert (optional but recommended):
   - Go to: `https://console.cloud.google.com/billing/budgets`
   - Create budget: $20/month is plenty for carousel testing
   - Set alert at 50%, 90%, 100%

**Note:** You won't be charged until you use the API. Image generation is ~$0.134 per image.

---

## Part 2: Store Your API Key Securely

### The Golden Rule

**Never put your API key in:**
- Code files
- Git repositories
- Slack/email messages
- Screenshots

**Always store it in:**
- Environment variables (what we're doing)
- A secrets manager (for production apps)

### Step 1: Open Your Shell Config

You're on macOS, so you likely use zsh. Open Terminal and run:

```bash
open ~/.zshrc
```

If the file doesn't exist, create it:
```bash
touch ~/.zshrc && open ~/.zshrc
```

### Step 2: Add the API Key

Add this line at the end of the file:

```bash
# Google AI API Key (for Gemini image generation)
export GOOGLE_API_KEY="AIzaSyD-YOUR-ACTUAL-KEY-HERE"
```

**Replace** `AIzaSyD-YOUR-ACTUAL-KEY-HERE` with your actual key.

Save and close the file.

### Step 3: Reload Your Shell

Run this in Terminal:

```bash
source ~/.zshrc
```

### Step 4: Verify It Works

Run:

```bash
echo $GOOGLE_API_KEY
```

You should see your key printed (or at least confirm it's not empty).

**Better verification** (doesn't expose the full key):

```bash
echo "Key starts with: ${GOOGLE_API_KEY:0:10}..."
```

Should show something like: `Key starts with: AIzaSyD-EX...`

---

## Part 3: Security Best Practices

### What Your .zshrc Should Look Like

```bash
# ... other stuff ...

# === API KEYS (NEVER COMMIT THESE) ===
# Google AI API Key (for Gemini image generation)
export GOOGLE_API_KEY="AIzaSyD-your-key-here"

# ... other stuff ...
```

### Verify .zshrc is NOT in Git

Your `~/.zshrc` is in your home folder, not in any git repo. But let's verify:

```bash
cd ~ && git status
```

Should say "not a git repository" - that's good.

### If You Accidentally Commit a Key

1. **Immediately revoke it:** Go to `https://aistudio.google.com/apikey` and delete the key
2. **Create a new key**
3. **Update your .zshrc** with the new key
4. The old key is now useless to anyone who found it

### Additional Security: Restrict Your Key (Optional)

1. Go to: `https://console.cloud.google.com/apis/credentials`
2. Click on your API key
3. Under **"API restrictions"**, select **"Restrict key"**
4. Choose only the APIs you need:
   - Generative Language API (for Gemini)
5. Save

This means even if someone gets your key, they can only use it for Gemini, not other Google services.

---

## Part 4: Test the Connection

### Quick Python Test

Create a test file (don't commit this):

```bash
cat > /tmp/test_google_api.py << 'EOF'
#!/usr/bin/env python3
import os
from google import genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not set")
    print("Run: source ~/.zshrc")
    exit(1)

print(f"API key found: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    print("Client initialized successfully!")

    # List models to verify access
    models = list(client.models.list())
    print(f"Found {len(models)} models")
    print("Connection test PASSED")
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
EOF
```

Run it:

```bash
python3 /tmp/test_google_api.py
```

**Expected output:**
```
API key found: AIzaSyD-EX...
Client initialized successfully!
Found XX models
Connection test PASSED
```

### If It Fails

**"GOOGLE_API_KEY not set"**
- Run `source ~/.zshrc` and try again
- Check that the export line is correct in ~/.zshrc

**"Invalid API key" or authentication error**
- Verify you copied the full key (no extra spaces)
- Check the key is active at `https://aistudio.google.com/apikey`

**"Billing not enabled"**
- Go to `https://console.cloud.google.com/billing`
- Link a billing account to your project

**"Module not found: google.genai"**
- Run: `pip install google-generativeai`

---

## Part 5: Reference Image Setup

Once API is working, add your reference image:

### Step 1: Create the Assets Folder

```bash
mkdir -p ~/Documents/GitHub/powerhouse-lab/skills/instagram-carousel/assets
```

### Step 2: Add to .gitignore

The assets folder should already be gitignored, but let's verify:

```bash
echo "skills/instagram-carousel/assets/" >> ~/Documents/GitHub/powerhouse-lab/.gitignore
```

### Step 3: Copy Your Reference Photo

Copy a good headshot/reference photo to:
```
~/Documents/GitHub/powerhouse-lab/skills/instagram-carousel/assets/ed-reference.png
```

**Good reference photo characteristics:**
- Clear face, good lighting
- Neutral background
- The "you" you want to appear in carousels
- PNG or JPG, at least 512x512 pixels

---

## Checklist

Before running tests, confirm:

- [ ] API key created at aistudio.google.com/apikey
- [ ] Billing enabled at console.cloud.google.com/billing
- [ ] Key added to ~/.zshrc as `export GOOGLE_API_KEY="..."`
- [ ] Shell reloaded with `source ~/.zshrc`
- [ ] `echo $GOOGLE_API_KEY` shows the key
- [ ] Python test passes
- [ ] Reference image at `skills/instagram-carousel/assets/ed-reference.png`
- [ ] Python dependencies: `pip install google-generativeai pillow`

---

## Quick Reference

| What | Where |
|------|-------|
| Create/view API keys | https://aistudio.google.com/apikey |
| Billing setup | https://console.cloud.google.com/billing |
| API restrictions | https://console.cloud.google.com/apis/credentials |
| Usage dashboard | https://console.cloud.google.com/apis/dashboard |
| Your API key | `~/.zshrc` (environment variable) |
| Reference image | `skills/instagram-carousel/assets/ed-reference.png` |

---

*Guide created 2026-01-10*
