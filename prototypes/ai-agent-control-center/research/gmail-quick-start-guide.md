# Gmail API Quick Start Guide

**Goal:** Get Gmail working with Claude Code in 30 minutes

---

## Prerequisites
- Python 3.7+
- Google account with Gmail
- Terminal access

---

## Step 1: Google Cloud Setup (10 min)

### 1.1 Create Project
```
1. Visit: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "Claude Code Gmail"
4. Click "Create"
```

### 1.2 Enable Gmail API
```
1. In the search bar, type "Gmail API"
2. Click "Gmail API"
3. Click "Enable"
```

### 1.3 Create OAuth Credentials
```
1. Go to: APIs & Services → Credentials
2. Click "+ Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: "Claude Code Gmail"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your email
   - Click "Save and Continue"
4. Back to Create OAuth Client ID:
   - Application type: "Desktop app"
   - Name: "Claude Code Desktop"
   - Click "Create"
5. Download JSON file
6. Rename to: credentials.json
```

### 1.4 Move Credentials
```bash
# Create secure directory
mkdir -p ~/.config/gmail-tool

# Move credentials
mv ~/Downloads/credentials.json ~/.config/gmail-tool/

# Secure permissions
chmod 600 ~/.config/gmail-tool/credentials.json
```

---

## Step 2: Install Python Client (5 min)

```bash
# Install Gmail API client
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## Step 3: Test Authentication (5 min)

Create test script:

```bash
cat > ~/test_gmail_auth.py << 'EOF'
#!/usr/bin/env python3
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_PATH = os.path.expanduser('~/.config/gmail-tool/credentials.json')
TOKEN_PATH = os.path.expanduser('~/.config/gmail-tool/token.pickle')

def main():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Test: List 5 recent messages
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    print(f"✓ Authentication successful!")
    print(f"✓ Found {len(messages)} recent messages")

    # Show first message subject
    if messages:
        msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='metadata').execute()
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        print(f"✓ Most recent: {subject}")

if __name__ == '__main__':
    main()
EOF

# Make executable
chmod +x ~/test_gmail_auth.py

# Run test
python ~/test_gmail_auth.py
```

**Expected:**
- Browser opens for Google OAuth consent
- Click "Allow"
- Terminal shows: "✓ Authentication successful!"

---

## Step 4: Simple Search Script (10 min)

```bash
cat > ~/gmail_search.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import pickle
import base64
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser('~/.config/gmail-tool/token.pickle')

def get_service():
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('gmail', 'v1', credentials=creds)

def search_emails(query, max_results=10):
    service = get_service()

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    print(f"\nFound {len(messages)} messages:\n")

    for msg in messages:
        message = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata'
        ).execute()

        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        print(f"From: {from_addr}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")
        print(f"ID: {msg['id']}")
        print("-" * 80)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python gmail_search.py 'search query'")
        print("\nExamples:")
        print("  python gmail_search.py 'from:someone@example.com'")
        print("  python gmail_search.py 'subject:proposal newer_than:7d'")
        print("  python gmail_search.py 'has:attachment'")
        sys.exit(1)

    query = sys.argv[1]
    search_emails(query)
EOF

chmod +x ~/gmail_search.py
```

### Test It:
```bash
# Search recent emails
python ~/gmail_search.py "newer_than:7d"

# Search by sender
python ~/gmail_search.py "from:someone@example.com"

# Search by subject
python ~/gmail_search.py "subject:proposal"
```

---

## Common Queries Cheat Sheet

```bash
# Time-based
"newer_than:7d"              # Last 7 days
"older_than:30d"             # Older than 30 days
"after:2025/12/01"           # After specific date
"before:2026/01/01"          # Before specific date

# Sender/Recipient
"from:john@example.com"      # From specific person
"to:sarah@example.com"       # To specific person
"cc:mike@example.com"        # CC'd to person

# Content
"subject:proposal"           # Subject contains
"has:attachment"             # Has attachments
"filename:pdf"               # Specific file type
"is:unread"                  # Unread only
"is:starred"                 # Starred only

# Labels
"label:important"            # Has label
"-label:spam"                # Exclude label

# Combined
"from:john subject:proposal newer_than:7d has:attachment"
```

---

## Troubleshooting

### "credentials.json not found"
```bash
# Check file exists
ls -la ~/.config/gmail-tool/credentials.json

# If missing, re-download from Google Cloud Console
```

### "Token expired"
```bash
# Delete old token
rm ~/.config/gmail-tool/token.pickle

# Re-run authentication
python ~/test_gmail_auth.py
```

### "Permission denied"
```bash
# Check OAuth scopes in code match consent screen
# May need to delete token and re-authenticate with new scopes
```

### "Import error"
```bash
# Reinstall dependencies
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## Next Steps

### For Claude Code Integration:
1. Copy search script to Claude Code tools directory
2. Make it output JSON for easy parsing
3. Add send/draft/tracking capabilities
4. Create wrapper scripts for common tasks

### Useful Enhancements:
```bash
# Read full email body
python gmail_read.py <message_id>

# Send email
python gmail_send.py --to="..." --subject="..." --body="..."

# Create draft
python gmail_draft.py --to="..." --subject="..." --body="..."
```

See `claude-code-gmail-tool-spec.md` for full implementation details.

---

## Security Reminders

1. **Never commit credentials.json or token.pickle to git**
```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo "token.pickle" >> .gitignore
```

2. **Secure file permissions**
```bash
chmod 600 ~/.config/gmail-tool/*.json
chmod 600 ~/.config/gmail-tool/*.pickle
```

3. **Revoke access if compromised**
```
Visit: https://myaccount.google.com/permissions
Remove: "Claude Code Gmail"
Delete token.pickle
Re-authenticate
```

---

## Success Checklist

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] Python client installed
- [ ] Test authentication successful
- [ ] Search script working
- [ ] Common queries tested
- [ ] Credentials secured

**Time to complete:** ~30 minutes
**You're now ready to integrate Gmail with Claude Code!**
