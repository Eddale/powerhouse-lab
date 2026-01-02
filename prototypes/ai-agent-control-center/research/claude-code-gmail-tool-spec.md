# Claude Code Gmail Tool Specification

**Date:** 2026-01-02
**Purpose:** Technical spec for implementing Gmail as a Claude Code tool

---

## Overview

This document outlines how to create a Gmail integration tool for Claude Code that enables:
1. Fast email search from the command line
2. Automated "Waiting For" tracking
3. Email drafting in Ed's voice
4. Send emails programmatically

---

## Architecture

```
Claude Code
    ↓
Gmail Tool (Python Script)
    ↓
Google Gmail API
    ↓
Ed's Gmail Account
```

### Files Structure
```
/tools/
  └── gmail/
      ├── gmail_tool.py          # Main CLI interface
      ├── auth.py                # OAuth2 authentication
      ├── search.py              # Search functionality
      ├── send.py                # Sending emails
      ├── tracking.py            # "Waiting For" system
      ├── config.py              # Configuration
      ├── requirements.txt       # Python dependencies
      ├── .env.example           # Environment template
      └── README.md              # Setup instructions
```

---

## Tool Interface Design

### Command Structure
```bash
# Search emails
python gmail_tool.py search "from:client@example.com newer_than:7d"

# Read specific email
python gmail_tool.py read <message_id>

# Send email
python gmail_tool.py send --to="client@example.com" --subject="Follow-up" --body="..."

# Draft email (for review)
python gmail_tool.py draft --to="client@example.com" --subject="Follow-up" --body="..."

# Check waiting-for status
python gmail_tool.py waiting-for list
python gmail_tool.py waiting-for check

# Track sent email
python gmail_tool.py send --to="client@example.com" --subject="Proposal" --body="..." --track
```

### JSON Output Format
All commands return JSON for easy parsing by Claude:

```json
{
  "success": true,
  "command": "search",
  "results": [
    {
      "id": "msg_123456",
      "thread_id": "thread_789",
      "from": "client@example.com",
      "to": "ed@example.com",
      "subject": "Re: Proposal",
      "date": "2026-01-01T10:30:00Z",
      "snippet": "Thanks for sending this over...",
      "labels": ["INBOX", "UNREAD"],
      "has_attachments": false
    }
  ],
  "count": 1
}
```

---

## Implementation: Core Modules

### 1. auth.py - Authentication Manager

```python
"""
Gmail OAuth2 authentication handler.
Manages token lifecycle and credential storage.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send'
]

class GmailAuth:
    def __init__(self, credentials_path=None, token_path=None):
        self.credentials_path = credentials_path or os.getenv('GMAIL_CREDENTIALS_PATH')
        self.token_path = token_path or os.getenv('GMAIL_TOKEN_PATH')

        if not self.credentials_path:
            raise ValueError("GMAIL_CREDENTIALS_PATH not set")

        # Ensure token directory exists
        Path(self.token_path).parent.mkdir(parents=True, exist_ok=True)

    def get_credentials(self):
        """Get or refresh OAuth2 credentials."""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def get_service(self):
        """Get authenticated Gmail API service."""
        creds = self.get_credentials()
        return build('gmail', 'v1', credentials=creds)

    def revoke(self):
        """Revoke access and delete stored token."""
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
            print("Token revoked and deleted")
```

### 2. search.py - Email Search

```python
"""
Gmail search functionality.
Supports Gmail query syntax and returns structured results.
"""

import base64
from email.utils import parsedate_to_datetime

class GmailSearch:
    def __init__(self, service):
        self.service = service

    def search(self, query, max_results=10, format='metadata'):
        """
        Search emails using Gmail query syntax.

        Args:
            query: Gmail search query
            max_results: Number of results to return
            format: 'minimal', 'metadata', 'full'

        Returns:
            List of message objects
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                return []

            # Fetch details based on format
            detailed = []
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format=format
                ).execute()
                detailed.append(self._parse_message(message, format))

            return detailed

        except Exception as e:
            raise Exception(f'Search failed: {str(e)}')

    def get_message(self, message_id, format='full'):
        """Fetch a single message by ID."""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format=format
            ).execute()
            return self._parse_message(message, format)
        except Exception as e:
            raise Exception(f'Failed to fetch message: {str(e)}')

    def _parse_message(self, message, format):
        """Parse message object into structured format."""
        parsed = {
            'id': message['id'],
            'thread_id': message['threadId'],
            'labels': message.get('labelIds', [])
        }

        if format == 'minimal':
            return parsed

        # Extract headers
        headers = message['payload']['headers']
        parsed.update({
            'from': self._get_header(headers, 'From'),
            'to': self._get_header(headers, 'To'),
            'subject': self._get_header(headers, 'Subject'),
            'date': self._get_header(headers, 'Date'),
            'snippet': message.get('snippet', '')
        })

        # Check for attachments
        parsed['has_attachments'] = 'parts' in message['payload'] and any(
            part.get('filename') for part in message['payload']['parts']
        )

        if format == 'full':
            parsed['body'] = self._get_body(message)

        return parsed

    def _get_header(self, headers, name):
        """Extract header value by name."""
        header = next((h for h in headers if h['name'] == name), None)
        return header['value'] if header else None

    def _get_body(self, message):
        """Extract email body (plain text preferred)."""
        payload = message['payload']

        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            # Simple message
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')

        return ''
```

### 3. send.py - Email Sending

```python
"""
Gmail email sending functionality.
Supports sending and drafting emails.
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GmailSend:
    def __init__(self, service):
        self.service = service

    def send(self, to, subject, body, body_html=None, cc=None, bcc=None):
        """
        Send an email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text body
            body_html: HTML body (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)

        Returns:
            Sent message object
        """
        message = self._create_message(to, subject, body, body_html, cc, bcc)

        try:
            sent = self.service.users().messages().send(
                userId='me',
                body={'raw': message}
            ).execute()

            return {
                'id': sent['id'],
                'thread_id': sent['threadId'],
                'label_ids': sent.get('labelIds', [])
            }

        except Exception as e:
            raise Exception(f'Failed to send email: {str(e)}')

    def draft(self, to, subject, body, body_html=None, cc=None, bcc=None):
        """
        Create a draft email.

        Args:
            Same as send()

        Returns:
            Draft object
        """
        message = self._create_message(to, subject, body, body_html, cc, bcc)

        try:
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': message}}
            ).execute()

            return {
                'id': draft['id'],
                'message_id': draft['message']['id'],
                'thread_id': draft['message']['threadId']
            }

        except Exception as e:
            raise Exception(f'Failed to create draft: {str(e)}')

    def send_draft(self, draft_id):
        """Send a previously created draft."""
        try:
            sent = self.service.users().drafts().send(
                userId='me',
                body={'id': draft_id}
            ).execute()

            return {
                'id': sent['id'],
                'thread_id': sent['threadId']
            }

        except Exception as e:
            raise Exception(f'Failed to send draft: {str(e)}')

    def _create_message(self, to, subject, body, body_html=None, cc=None, bcc=None):
        """Create RFC 2822 formatted message."""
        if body_html:
            message = MIMEMultipart('alternative')
            message.attach(MIMEText(body, 'plain'))
            message.attach(MIMEText(body_html, 'html'))
        else:
            message = MIMEText(body)

        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        return base64.urlsafe_b64encode(message.as_bytes()).decode()
```

### 4. tracking.py - "Waiting For" System

```python
"""
Email tracking system for "Waiting For" workflow.
"""

import re
from datetime import datetime, timedelta

class GmailTracking:
    def __init__(self, service):
        self.service = service
        self.label_ids = {}

    def setup(self):
        """Create necessary labels if they don't exist."""
        labels_config = {
            'Waiting For': {'backgroundColor': '#fad165', 'textColor': '#000000'},
            'Responded': {'backgroundColor': '#a4c2f4', 'textColor': '#000000'}
        }

        existing = self.service.users().labels().list(userId='me').execute()
        existing_names = {l['name']: l['id'] for l in existing.get('labels', [])}

        for name, color in labels_config.items():
            if name in existing_names:
                self.label_ids[name] = existing_names[name]
            else:
                label = self.service.users().labels().create(
                    userId='me',
                    body={
                        'name': name,
                        'labelListVisibility': 'labelShow',
                        'messageListVisibility': 'show',
                        'color': color
                    }
                ).execute()
                self.label_ids[name] = label['id']

        return self.label_ids

    def track_sent_email(self, message_id):
        """Apply 'Waiting For' label to sent email."""
        if not self.label_ids:
            self.setup()

        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [self.label_ids['Waiting For']]}
            ).execute()

            return {'tracked': True, 'message_id': message_id}

        except Exception as e:
            raise Exception(f'Failed to track email: {str(e)}')

    def list_waiting_for(self):
        """List all emails with 'Waiting For' label."""
        if not self.label_ids:
            self.setup()

        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=[self.label_ids['Waiting For']]
            ).execute()

            messages = results.get('messages', [])

            detailed = []
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata'
                ).execute()

                headers = message['payload']['headers']
                detailed.append({
                    'id': message['id'],
                    'to': self._get_header(headers, 'To'),
                    'subject': self._get_header(headers, 'Subject'),
                    'date': self._get_header(headers, 'Date'),
                    'snippet': message.get('snippet', '')
                })

            return detailed

        except Exception as e:
            raise Exception(f'Failed to list waiting emails: {str(e)}')

    def check_replies(self):
        """Check for replies to tracked emails and update labels."""
        if not self.label_ids:
            self.setup()

        waiting = self.list_waiting_for()
        updated = []

        for email in waiting:
            # Extract recipient email
            recipient = self._extract_email(email['to'])
            if not recipient:
                continue

            # Search for replies in thread
            try:
                thread = self.service.users().threads().get(
                    userId='me',
                    id=self.service.users().messages().get(
                        userId='me',
                        id=email['id']
                    ).execute()['threadId']
                ).execute()

                messages = thread.get('messages', [])

                # Check if thread has replies from recipient
                has_reply = False
                for msg in messages:
                    if msg['id'] == email['id']:
                        continue  # Skip original

                    headers = msg['payload']['headers']
                    from_addr = self._get_header(headers, 'From')

                    if recipient in from_addr:
                        has_reply = True
                        break

                if has_reply:
                    # Update labels
                    self.service.users().messages().modify(
                        userId='me',
                        id=email['id'],
                        body={
                            'removeLabelIds': [self.label_ids['Waiting For']],
                            'addLabelIds': [self.label_ids['Responded']]
                        }
                    ).execute()

                    updated.append({
                        'id': email['id'],
                        'subject': email['subject'],
                        'status': 'responded'
                    })

            except Exception as e:
                print(f"Error checking email {email['id']}: {str(e)}")
                continue

        return updated

    def _get_header(self, headers, name):
        """Extract header value."""
        header = next((h for h in headers if h['name'] == name), None)
        return header['value'] if header else None

    def _extract_email(self, address_str):
        """Extract email address from 'Name <email>' format."""
        match = re.search(r'[\w\.-]+@[\w\.-]+', address_str)
        return match.group(0) if match else None
```

### 5. gmail_tool.py - Main CLI Interface

```python
#!/usr/bin/env python3
"""
Gmail Tool for Claude Code
Main CLI interface
"""

import sys
import json
import argparse
from auth import GmailAuth
from search import GmailSearch
from send import GmailSend
from tracking import GmailTracking

def output(data):
    """Output JSON response."""
    print(json.dumps(data, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Gmail Tool for Claude Code')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search emails')
    search_parser.add_argument('query', help='Gmail search query')
    search_parser.add_argument('--max', type=int, default=10, help='Max results')
    search_parser.add_argument('--full', action='store_true', help='Include email body')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read specific email')
    read_parser.add_argument('message_id', help='Message ID')

    # Send command
    send_parser = subparsers.add_parser('send', help='Send email')
    send_parser.add_argument('--to', required=True, help='Recipient')
    send_parser.add_argument('--subject', required=True, help='Subject')
    send_parser.add_argument('--body', required=True, help='Email body')
    send_parser.add_argument('--html', help='HTML body')
    send_parser.add_argument('--track', action='store_true', help='Add to Waiting For')

    # Draft command
    draft_parser = subparsers.add_parser('draft', help='Create draft')
    draft_parser.add_argument('--to', required=True, help='Recipient')
    draft_parser.add_argument('--subject', required=True, help='Subject')
    draft_parser.add_argument('--body', required=True, help='Email body')
    draft_parser.add_argument('--html', help='HTML body')

    # Waiting-for commands
    wf_parser = subparsers.add_parser('waiting-for', help='Waiting For tracking')
    wf_subparsers = wf_parser.add_subparsers(dest='wf_command')
    wf_subparsers.add_parser('list', help='List tracked emails')
    wf_subparsers.add_parser('check', help='Check for replies')
    wf_subparsers.add_parser('setup', help='Set up labels')

    args = parser.parse_args()

    try:
        # Authenticate
        auth = GmailAuth()
        service = auth.get_service()

        # Execute command
        if args.command == 'search':
            searcher = GmailSearch(service)
            format = 'full' if args.full else 'metadata'
            results = searcher.search(args.query, args.max, format)

            output({
                'success': True,
                'command': 'search',
                'query': args.query,
                'count': len(results),
                'results': results
            })

        elif args.command == 'read':
            searcher = GmailSearch(service)
            message = searcher.get_message(args.message_id, 'full')

            output({
                'success': True,
                'command': 'read',
                'message': message
            })

        elif args.command == 'send':
            sender = GmailSend(service)
            result = sender.send(args.to, args.subject, args.body, args.html)

            # Track if requested
            if args.track:
                tracker = GmailTracking(service)
                tracker.setup()
                tracker.track_sent_email(result['id'])
                result['tracked'] = True

            output({
                'success': True,
                'command': 'send',
                'result': result
            })

        elif args.command == 'draft':
            sender = GmailSend(service)
            result = sender.draft(args.to, args.subject, args.body, args.html)

            output({
                'success': True,
                'command': 'draft',
                'result': result,
                'review_url': 'https://mail.google.com/mail/u/0/#drafts'
            })

        elif args.command == 'waiting-for':
            tracker = GmailTracking(service)

            if args.wf_command == 'setup':
                labels = tracker.setup()
                output({
                    'success': True,
                    'command': 'waiting-for setup',
                    'labels': labels
                })

            elif args.wf_command == 'list':
                emails = tracker.list_waiting_for()
                output({
                    'success': True,
                    'command': 'waiting-for list',
                    'count': len(emails),
                    'emails': emails
                })

            elif args.wf_command == 'check':
                updated = tracker.check_replies()
                output({
                    'success': True,
                    'command': 'waiting-for check',
                    'updated_count': len(updated),
                    'updated': updated
                })

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        output({
            'success': False,
            'error': str(e)
        })
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## Setup Instructions

### Step 1: Google Cloud Console
1. Go to https://console.cloud.google.com/
2. Create project: "Claude Code Gmail"
3. Enable Gmail API
4. Create OAuth2 credentials (Desktop app)
5. Download as `credentials.json`

### Step 2: Install Tool
```bash
cd /path/to/claude-code/tools
mkdir gmail
cd gmail

# Copy all Python files above
# Create requirements.txt:
cat > requirements.txt << EOF
google-api-python-client>=2.100.0
google-auth-httplib2>=0.1.1
google-auth-oauthlib>=1.1.0
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.pickle
EOF
```

### Step 3: First Run (Authentication)
```bash
# This will open browser for OAuth consent
python gmail_tool.py waiting-for setup
```

### Step 4: Add to Claude Code
Make tool executable:
```bash
chmod +x gmail_tool.py
```

Add alias (optional):
```bash
echo "alias gmail='python /path/to/tools/gmail/gmail_tool.py'" >> ~/.bashrc
source ~/.bashrc
```

---

## Usage Examples from Claude Code

### Search Recent Emails
```bash
gmail search "from:client@example.com newer_than:7d"
```

### Read Full Email
```bash
gmail read msg_187a9c8f3e4d2b1a
```

### Send and Track
```bash
gmail send \
  --to="client@example.com" \
  --subject="Proposal Follow-up" \
  --body="Hi John, Just checking if you had a chance to review the proposal. Best, Ed" \
  --track
```

### Check Waiting For Status
```bash
# List all tracked emails
gmail waiting-for list

# Check for new replies
gmail waiting-for check
```

### Create Draft for Review
```bash
gmail draft \
  --to="client@example.com" \
  --subject="Q1 Planning" \
  --body="Hey Sarah, Let's sync on Q1 goals. When works for you?"
```

---

## Integration with Claude Code Workflow

### Scenario 1: Quick Email Search
```
Ed: "Claude, find emails from John about the proposal"

Claude:
  1. Runs: gmail search "from:john proposal"
  2. Parses JSON results
  3. Presents: "Found 3 emails from John about proposals..."
```

### Scenario 2: Draft in Ed's Voice
```
Ed: "Claude, draft a follow-up to Sarah about Q1 planning"

Claude:
  1. Analyzes Ed's writing style (from previous emails)
  2. Generates draft text
  3. Runs: gmail draft --to="sarah@..." --subject="..." --body="..."
  4. Returns: "Draft created. Review at: [Gmail drafts URL]"
```

### Scenario 3: Waiting For Check
```
Ed: "Claude, check my waiting-for status"

Claude:
  1. Runs: gmail waiting-for list
  2. Runs: gmail waiting-for check
  3. Presents: "You're waiting for replies from 3 people:
               - John (sent 5 days ago)
               - Sarah (sent 2 days ago)
               - Mike (sent 1 day ago)"
```

---

## Performance Optimizations

### 1. Caching
Cache label IDs in local config file:
```json
{
  "label_ids": {
    "Waiting For": "Label_123",
    "Responded": "Label_456"
  },
  "last_updated": "2026-01-02T10:00:00Z"
}
```

### 2. Batch Requests
Fetch multiple messages in one API call:
```python
batch = service.new_batch_http_request()
for msg_id in message_ids:
    batch.add(service.users().messages().get(userId='me', id=msg_id))
batch.execute()
```

### 3. Minimal Format
Use `format='minimal'` when only IDs needed:
```python
# Fast: Only returns IDs
results = service.users().messages().list(userId='me', q=query).execute()

# Then fetch details only for messages Claude needs
```

---

## Error Handling

### Common Errors

1. **Token Expired**
   - Auto-refreshes if refresh token valid
   - Prompts re-auth if refresh token invalid

2. **Quota Exceeded**
   - Implement exponential backoff
   - Cache results when possible

3. **Network Errors**
   - Retry with exponential backoff
   - Max 3 retries

4. **Invalid Query**
   - Return helpful error message
   - Suggest corrected query

---

## Security Checklist

- [ ] credentials.json in .gitignore
- [ ] token.pickle in .gitignore
- [ ] File permissions: 600 on credentials/token files
- [ ] Environment variables for paths
- [ ] No hardcoded credentials
- [ ] OAuth2 refresh handling
- [ ] Secure token storage location

---

## Testing Plan

### Unit Tests
```python
# test_search.py
def test_search_query():
    # Mock service
    # Test query parsing
    # Verify results structure

# test_send.py
def test_create_message():
    # Test MIME message creation
    # Verify headers
    # Check encoding

# test_tracking.py
def test_label_creation():
    # Mock label API
    # Verify label config
    # Check error handling
```

### Integration Tests
```bash
# Real API tests (use test account)
python -m pytest tests/integration/
```

---

## Next Steps

1. Implement core modules (auth, search, send, tracking)
2. Create CLI interface (gmail_tool.py)
3. Test authentication flow
4. Test each command
5. Document setup process
6. Create video walkthrough
7. Integrate with Claude Code workflow

---

## Future Enhancements

1. **Attachment support** - Download/upload files
2. **Template system** - Save email templates
3. **Signature management** - Auto-append signatures
4. **Thread handling** - Better conversation tracking
5. **Batch operations** - Send multiple emails
6. **Scheduled sends** - Draft + send later
7. **Analytics** - Email response rates
8. **Voice analysis** - Learn Ed's writing style

---

**Status:** Ready for implementation
**Estimated time:** 4-6 hours for v1
**Dependencies:** Google Cloud project, OAuth2 credentials
