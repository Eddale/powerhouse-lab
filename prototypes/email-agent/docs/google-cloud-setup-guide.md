# Google Cloud Console Setup Guide

**Project:** Claude Code APIs
**APIs:** Gmail API + Google Calendar API
**Account:** tedlegend@gmail.com
**Time:** ~15 minutes

---

## Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/

2. Sign in with **tedlegend@gmail.com**

3. Click the project dropdown (top-left, next to "Google Cloud")

4. Click **"New Project"**

5. Enter:
   - **Project name:** `Claude Code APIs`
   - **Organization:** Leave as default (or "No organization")

6. Click **"Create"**

7. Wait for project creation (10-20 seconds)

8. Make sure "Claude Code APIs" is selected in the project dropdown

---

## Step 2: Enable Gmail API

1. In the search bar at top, type: `Gmail API`

2. Click **"Gmail API"** in the results

3. Click the blue **"Enable"** button

4. Wait for it to enable (~5 seconds)

---

## Step 3: Enable Google Calendar API

1. In the search bar, type: `Google Calendar API`

2. Click **"Google Calendar API"** in the results

3. Click the blue **"Enable"** button

4. Wait for it to enable (~5 seconds)

---

## Step 4: Configure OAuth Consent Screen

Before creating credentials, Google requires an OAuth consent screen.

1. Go to: **APIs & Services → OAuth consent screen**
   (Left sidebar, or search "OAuth consent")

2. Select **"External"** user type
   (Internal is only for Google Workspace orgs)

3. Click **"Create"**

4. Fill in the **App Information**:
   - **App name:** `Claude Code APIs`
   - **User support email:** Select `tedlegend@gmail.com`
   - **App logo:** Skip (optional)

5. Scroll down to **Developer contact information**:
   - **Email:** `tedlegend@gmail.com`

6. Click **"Save and Continue"**

---

## Step 5: Add Scopes

1. Click **"Add or Remove Scopes"**

2. In the filter box, search for and check these scopes:

   **Gmail scopes:**
   - `https://www.googleapis.com/auth/gmail.readonly` - Read emails
   - `https://www.googleapis.com/auth/gmail.modify` - Modify labels
   - `https://www.googleapis.com/auth/gmail.send` - Send emails (optional, for drafts)

   **Calendar scopes:**
   - `https://www.googleapis.com/auth/calendar.readonly` - Read calendar events
   - `https://www.googleapis.com/auth/calendar.events.readonly` - Read event details

3. Click **"Update"**

4. Click **"Save and Continue"**

---

## Step 6: Add Test Users

While in "Testing" mode, only listed users can authorize the app.

1. Click **"Add Users"**

2. Enter: `tedlegend@gmail.com`

3. Click **"Add"**

4. Click **"Save and Continue"**

5. Review the summary and click **"Back to Dashboard"**

---

## Step 7: Create OAuth Credentials

1. Go to: **APIs & Services → Credentials**
   (Left sidebar)

2. Click **"+ Create Credentials"** (top of page)

3. Select **"OAuth client ID"**

4. For **Application type**, select: **"Desktop app"**

5. **Name:** `Claude Code Desktop`

6. Click **"Create"**

7. A popup appears with your credentials

8. Click **"Download JSON"**

9. The file downloads as something like:
   `client_secret_123456789-abc123.apps.googleusercontent.com.json`

---

## Step 8: Store Credentials Securely

1. Rename the downloaded file to `credentials.json`

2. Move it to a secure location:

```bash
# Create directory
mkdir -p ~/.config/claude-code-apis

# Move and rename the file (adjust the source filename)
mv ~/Downloads/client_secret_*.json ~/.config/claude-code-apis/credentials.json

# Secure permissions
chmod 600 ~/.config/claude-code-apis/credentials.json
```

3. Verify it's there:
```bash
ls -la ~/.config/claude-code-apis/
```

---

## Step 9: Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Google API credentials
export GOOGLE_CREDENTIALS_PATH="$HOME/.config/claude-code-apis/credentials.json"
export GOOGLE_TOKEN_PATH="$HOME/.config/claude-code-apis/token.pickle"
```

Then reload:
```bash
source ~/.zshrc
```

---

## Step 10: First Authentication (Browser Required)

When Claude runs the Gmail/Calendar tools for the first time, it will:

1. Open your browser to Google's consent screen
2. You select tedlegend@gmail.com
3. You'll see a warning "This app isn't verified" - click "Advanced" → "Go to Claude Code APIs (unsafe)"
4. Review permissions and click "Allow"
5. Browser says "The authentication flow has completed"
6. A `token.pickle` file is saved for future use (no browser needed again)

---

## Verification Checklist

After completing setup, verify:

- [ ] Project "Claude Code APIs" exists in Google Cloud Console
- [ ] Gmail API is enabled
- [ ] Google Calendar API is enabled
- [ ] OAuth consent screen configured with tedlegend@gmail.com as test user
- [ ] Desktop OAuth credentials created
- [ ] `credentials.json` saved to `~/.config/claude-code-apis/`
- [ ] Environment variables set in shell profile

---

## What Happens Next

Once you complete this guide, tell me and I'll:

1. Create the Gmail API tool (Python)
2. Create the Calendar API tool (Python)
3. Run first auth (will open browser for consent)
4. Test both connections
5. Build the morning-metrics skill

---

## Troubleshooting

**"This app isn't verified" warning:**
Normal for personal/testing apps. Click Advanced → Continue.

**"Access blocked" error:**
Make sure tedlegend@gmail.com is added as a test user in Step 6.

**"credentials.json not found":**
Check the file path and environment variable match.

**Token expired:**
Delete `token.pickle` and re-run auth flow.

---

## Cost Tracking

To view API usage and costs:

1. Go to: https://console.cloud.google.com/apis/dashboard
2. Select "Claude Code APIs" project
3. View quotas, traffic, and any billing (Gmail/Calendar APIs are free for personal use)

---

**Created:** 2026-01-10
**For:** Win-the-day metrics briefing setup
