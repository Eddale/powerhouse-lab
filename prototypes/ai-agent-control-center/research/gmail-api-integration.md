# Gmail API Integration Research

**Date:** 2026-01-02
**Purpose:** Claude Code integration for fast email search, "Waiting For" tracking, and email drafting

---

## Table of Contents
1. [Authentication Setup](#authentication-setup)
2. [Search Capabilities](#search-capabilities)
3. [Reading Emails](#reading-emails)
4. [Sending Emails](#sending-emails)
5. [Labels & Filters](#labels--filters)
6. [Setup Steps](#setup-steps)
7. [Code Examples](#code-examples)
8. [Rate Limits & Performance](#rate-limits--performance)

---

## 1. Authentication Setup

### Three Authentication Methods

#### **Option A: OAuth2 (Recommended for User Access)**
- **Best for:** Personal Gmail access, user-specific actions
- **Setup:** Requires Google Cloud Console project + OAuth consent screen
- **Token lifespan:** Access tokens expire in 1 hour, refresh tokens persist
- **Scopes needed:**
  - `https://www.googleapis.com/auth/gmail.readonly` - Read emails
  - `https://www.googleapis.com/auth/gmail.send` - Send emails
  - `https://www.googleapis.com/auth/gmail.labels` - Manage labels
  - `https://www.googleapis.com/auth/gmail.modify` - Add/remove labels from messages

#### **Option B: Service Account**
- **Best for:** Workspace accounts with domain-wide delegation
- **Setup:** Requires Google Workspace admin access
- **Use case:** Automated processes, server-to-server
- **Limitation:** Won't work with personal Gmail accounts

#### **Option C: App Passwords (Legacy)**
- **Status:** Being phased out by Google
- **Not recommended:** Use OAuth2 instead

### **Recommendation for Ed's Use Case**
Use **OAuth2** for personal Gmail access from Claude Code. Store credentials securely in environment variables.

---

## 2. Search Capabilities

### Query Syntax
Gmail API uses the same search syntax as the Gmail web interface:

```
from:sender@example.com
to:recipient@example.com
subject:"keyword"
has:attachment
is:unread
is:starred
after:2025/12/01
before:2026/01/01
newer_than:7d
older_than:30d
label:waiting-for
{keyword1 keyword2} (OR search)
"exact phrase"
```

### Advanced Queries for Your Use Cases

**"Waiting For" Tracking:**
```
from:me -label:replied newer_than:7d
```

**Search sent emails awaiting reply:**
```
from:me subject:"proposal" -label:responded
```

**Find attachments from specific sender:**
```
from:client@example.com has:attachment filename:pdf
```

### Performance
- **Speed:** Typically 200-500ms for simple queries
- **Indexing:** Real-time (new emails searchable immediately)
- **Pagination:** Returns 100 results max per request
- **Threading:** Can group by conversation threads

### Limitations
- No regex support in queries
- Cannot search inside attachments via API (Google's server-side feature only)
- Max 500 results per day for free tier (increases with paid workspace)

---

## 3. Reading Emails

### Message Formats
The API returns messages in different formats:

1. **`minimal`** - Just ID and thread ID
2. **`full`** - Complete message with headers and body
3. **`raw`** - RFC 2822 formatted email
4. **`metadata`** - Headers only, no body

### What You Can Fetch
- **Headers:** Subject, From, To, Date, Message-ID
- **Body:** Plain text and/or HTML
- **Attachments:** Download separately via attachment ID
- **Thread context:** All messages in a conversation
- **Labels:** Current labels applied to message

### Attachment Handling
- Attachments are fetched separately using `attachmentId`
- Base64 encoded in response
- Can download directly without full message fetch

---

## 4. Sending Emails

### Three Methods

#### **Method 1: Simple Send**
- Create RFC 2822 formatted message
- Base64 encode it
- POST to `/users/me/messages/send`

#### **Method 2: Draft Then Send**
- Create draft: `/users/me/drafts`
- Review/edit if needed
- Send: `/users/me/drafts/{id}/send`

#### **Method 3: Reply to Thread**
- Include `threadId` in message
- API handles threading automatically

### Features
- **Rich HTML:** Full HTML email support
- **Attachments:** MIME multipart messages
- **CC/BCC:** Standard email fields
- **Custom headers:** Add tracking headers
- **Thread continuity:** Auto-threads replies

### Use Case: Draft in Ed's Voice
1. Use Claude to generate email text
2. Create draft via API
3. Ed reviews in Gmail
4. Send programmatically or manually

---

## 5. Labels & Filters

### Label Management

**Creating Labels:**
```python
label = {
    'name': 'Waiting For',
    'labelListVisibility': 'labelShow',
    'messageListVisibility': 'show'
}
service.users().labels().create(userId='me', body=label).execute()
```

**Applying Labels to Messages:**
```python
service.users().messages().modify(
    userId='me',
    id=message_id,
    body={'addLabelIds': ['Label_ID']}
).execute()
```

**Listing Labels:**
```python
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])
```

### Filter Capabilities
- API can apply labels programmatically
- Cannot create Gmail filters via API (filters are user-facing feature)
- Workaround: Apply labels based on search criteria in your code

### Use Case: "Waiting For" System
1. Create label "Waiting For"
2. When Ed sends email via API, auto-apply label
3. Periodically check for replies: `from:recipient to:me`
4. When reply received, remove "Waiting For" label, add "Responded"

---

## 6. Setup Steps

### Step 1: Google Cloud Console Setup
```
1. Go to https://console.cloud.google.com/
2. Create new project: "Claude Code Gmail Integration"
3. Enable Gmail API:
   - APIs & Services → Library
   - Search "Gmail API"
   - Click Enable
4. Create OAuth2 credentials:
   - APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Application type: Desktop app
   - Download credentials.json
```

### Step 2: Install Python Client
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 3: First Authentication
```python
# This runs once to get token.json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None

    # Token file stores access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    from googleapiclient.discovery import build
    return build('gmail', 'v1', credentials=creds)
```

### Step 4: Environment Variables
```bash
# Store in .env file
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.pickle
```

---

## 7. Code Examples

### Example 1: Fast Email Search
```python
def search_emails(service, query, max_results=10):
    """
    Search emails using Gmail query syntax.

    Args:
        service: Gmail API service instance
        query: Gmail search query string
        max_results: Number of results to return

    Returns:
        List of message objects with metadata
    """
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return []

        # Fetch full message details
        detailed_messages = []
        for msg in messages:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            detailed_messages.append(message)

        return detailed_messages

    except Exception as e:
        print(f'Error searching emails: {e}')
        return []

# Usage examples:
# search_emails(service, 'from:client@example.com newer_than:7d')
# search_emails(service, 'subject:"proposal" has:attachment')
# search_emails(service, 'label:waiting-for')
```

### Example 2: Parse Email Content
```python
import base64

def get_email_content(message):
    """
    Extract subject, sender, date, and body from message object.

    Returns dict with parsed fields.
    """
    headers = message['payload']['headers']

    # Extract headers
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

    # Extract body
    body = ''
    if 'parts' in message['payload']:
        # Multipart message
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        # Simple message
        data = message['payload']['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    return {
        'subject': subject,
        'from': sender,
        'date': date,
        'body': body,
        'snippet': message.get('snippet', ''),
        'thread_id': message.get('threadId'),
        'message_id': message.get('id')
    }

# Usage:
# message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
# content = get_email_content(message)
# print(f"From: {content['from']}\nSubject: {content['subject']}\n{content['body']}")
```

### Example 3: Send Email
```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_email(service, to, subject, body_text, body_html=None):
    """
    Send an email via Gmail API.

    Args:
        service: Gmail API service
        to: Recipient email address
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)

    Returns:
        Sent message object
    """
    # Create message
    if body_html:
        message = MIMEMultipart('alternative')
        message.attach(MIMEText(body_text, 'plain'))
        message.attach(MIMEText(body_html, 'html'))
    else:
        message = MIMEText(body_text)

    message['to'] = to
    message['subject'] = subject

    # Encode message
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()

        print(f'Message sent. ID: {sent_message["id"]}')
        return sent_message

    except Exception as e:
        print(f'Error sending email: {e}')
        return None

# Usage:
# send_email(service, 'client@example.com', 'Follow-up', 'Just checking in...')
```

### Example 4: "Waiting For" System
```python
def setup_waiting_for_system(service):
    """
    Create labels for tracking sent emails.
    """
    labels_to_create = [
        {'name': 'Waiting For', 'color': {'backgroundColor': '#fad165'}},
        {'name': 'Responded', 'color': {'backgroundColor': '#a4c2f4'}}
    ]

    existing_labels = service.users().labels().list(userId='me').execute()
    existing_names = [label['name'] for label in existing_labels.get('labels', [])]

    label_ids = {}

    for label_config in labels_to_create:
        if label_config['name'] not in existing_names:
            label = service.users().labels().create(
                userId='me',
                body={
                    'name': label_config['name'],
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show',
                    'color': label_config['color']
                }
            ).execute()
            label_ids[label_config['name']] = label['id']
        else:
            # Get existing label ID
            label = next(l for l in existing_labels['labels'] if l['name'] == label_config['name'])
            label_ids[label_config['name']] = label['id']

    return label_ids

def send_and_track(service, to, subject, body, label_ids):
    """
    Send email and apply 'Waiting For' label.
    """
    sent_msg = send_email(service, to, subject, body)

    if sent_msg:
        # Apply "Waiting For" label
        service.users().messages().modify(
            userId='me',
            id=sent_msg['id'],
            body={'addLabelIds': [label_ids['Waiting For']]}
        ).execute()

        print(f'Email sent and marked as "Waiting For"')
        return sent_msg
    return None

def check_for_replies(service, label_ids):
    """
    Check for replies to 'Waiting For' emails and update labels.
    """
    # Get all "Waiting For" messages
    waiting_msgs = service.users().messages().list(
        userId='me',
        labelIds=[label_ids['Waiting For']]
    ).execute().get('messages', [])

    for msg in waiting_msgs:
        full_msg = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        # Get recipient from original email
        headers = full_msg['payload']['headers']
        to_header = next((h['value'] for h in headers if h['name'] == 'To'), '')

        # Extract email address (handle "Name <email>" format)
        import re
        recipient_email = re.search(r'[\w\.-]+@[\w\.-]+', to_header)
        if not recipient_email:
            continue
        recipient_email = recipient_email.group(0)

        # Search for replies from recipient
        thread_id = full_msg['threadId']
        replies = service.users().messages().list(
            userId='me',
            q=f'from:{recipient_email}',
            threadId=thread_id
        ).execute().get('messages', [])

        # If reply found, update labels
        if len(replies) > 1:  # More than just the original
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={
                    'removeLabelIds': [label_ids['Waiting For']],
                    'addLabelIds': [label_ids['Responded']]
                }
            ).execute()

            print(f'Reply received from {recipient_email} - label updated')

# Usage:
# label_ids = setup_waiting_for_system(service)
# send_and_track(service, 'client@example.com', 'Proposal', 'Here is my proposal...', label_ids)
# check_for_replies(service, label_ids)  # Run periodically
```

### Example 5: Draft Email for Review
```python
def create_draft(service, to, subject, body):
    """
    Create email draft for Ed to review before sending.
    """
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        draft = service.users().drafts().create(
            userId='me',
            body={'message': {'raw': raw}}
        ).execute()

        print(f'Draft created. ID: {draft["id"]}')
        print(f'Review in Gmail: https://mail.google.com/mail/u/0/#drafts')
        return draft

    except Exception as e:
        print(f'Error creating draft: {e}')
        return None

def send_draft(service, draft_id):
    """
    Send a previously created draft.
    """
    try:
        sent = service.users().drafts().send(
            userId='me',
            body={'id': draft_id}
        ).execute()

        print(f'Draft sent. Message ID: {sent["id"]}')
        return sent

    except Exception as e:
        print(f'Error sending draft: {e}')
        return None

# Usage:
# draft = create_draft(service, 'client@example.com', 'Follow-up', 'Just checking in...')
# # Ed reviews in Gmail
# send_draft(service, draft['id'])
```

---

## 8. Rate Limits & Performance

### Quota Limits (Free Tier)
- **Daily API calls:** 1 billion (realistically unlimited for personal use)
- **Per-user rate limit:** 250 quota units per second
- **Batch requests:** 100 requests per batch

### Quota Costs
- `messages.list`: 5 units
- `messages.get`: 5 units
- `messages.send`: 100 units
- `drafts.create`: 50 units
- `labels.create`: 5 units
- `labels.list`: 5 units

### Performance Tips
1. **Batch requests** - Fetch multiple messages in one call
2. **Use `minimal` format** - When you only need IDs
3. **Cache label IDs** - Don't fetch labels every time
4. **Pagination** - Use `pageToken` for large result sets
5. **Webhooks** - Use Gmail push notifications instead of polling

### Speed Benchmarks
- Search query: 200-500ms
- Fetch single message: 100-200ms
- Send email: 300-600ms
- Create draft: 200-400ms

---

## Implementation Roadmap for Claude Code

### Phase 1: Basic Search (30 min)
1. Set up OAuth2 authentication
2. Implement search function
3. Parse and display results

### Phase 2: "Waiting For" Tracking (45 min)
1. Create label system
2. Auto-label sent emails
3. Periodic reply checker

### Phase 3: Email Composition (30 min)
1. Draft creation function
2. Claude voice synthesis integration
3. Send with tracking

### Total estimated setup time: 2 hours

---

## Security Considerations

1. **Credential Storage**
   - Never commit `credentials.json` or `token.pickle` to git
   - Add to `.gitignore`
   - Store in secure location with restricted permissions

2. **Token Refresh**
   - Access tokens expire every hour
   - Refresh tokens are long-lived (until revoked)
   - Code should handle auto-refresh

3. **Scope Minimization**
   - Only request scopes you need
   - Consider separate credentials for read vs. send

4. **Error Handling**
   - Catch quota exceeded errors
   - Implement retry logic with exponential backoff
   - Log failures for debugging

---

## Next Steps

1. Create Google Cloud project
2. Enable Gmail API
3. Download credentials
4. Run authentication flow
5. Test search queries
6. Build "Waiting For" system
7. Integrate with Claude Code workflow

---

## Resources

- **Official Gmail API Docs:** https://developers.google.com/gmail/api
- **Python Client Library:** https://github.com/googleapis/google-api-python-client
- **Query Syntax Reference:** https://support.google.com/mail/answer/7190
- **OAuth2 Setup Guide:** https://developers.google.com/gmail/api/auth/about-auth

---

**Next Document:** `claude-code-gmail-tool-spec.md` (Claude Code tool implementation)
