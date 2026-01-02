# Python IMAP Email Integration Research

**Date:** 2026-01-02
**Purpose:** Evaluate IMAP vs Gmail API for "Waiting For" email tracking
**Target:** Gmail + iCloud (eddale@mac.com) integration

---

## TL;DR - The Verdict

**For your "Waiting For" tracker, use IMAP.** Here's why:

| Factor | IMAP | Gmail API |
|--------|------|-----------|
| **Setup complexity** | App password only | OAuth2 dance, credentials file, token refresh |
| **Works with iCloud** | Yes | No (Gmail only) |
| **Works with Mac Mail** | Yes (same protocol) | No |
| **Search speed** | Server-side, fast enough | Faster, but requires OAuth |
| **Code simplicity** | Straightforward | More boilerplate |
| **Best for** | Multi-provider, quick prototype | Gmail-only, high-volume |

**Translation:** IMAP is like using email's native language. Gmail API is like building a custom integration for one specific email system.

---

## Part 1: IMAP Basics - Connecting to Gmail & iCloud

### The Mental Model

IMAP = Internet Message Access Protocol. Think of it like FTP for email. The emails live on the server, and you're just viewing/searching them remotely.

- **Mac Mail uses IMAP** - So your Python script talks the same language as your Mail app
- **Gmail supports IMAP** - Need to enable it + use app password
- **iCloud supports IMAP** - Same deal, app password required

### Gmail Setup (One-Time)

1. **Enable IMAP** in Gmail settings (Settings > Forwarding and POP/IMAP > Enable IMAP)
2. **Create App Password** (Google Account > Security > 2-Step Verification > App passwords)
   - Select "Mail" and "Mac"
   - Copy the 16-character password

### iCloud Setup (One-Time)

1. **Enable 2FA** on Apple ID (if not already)
2. **Generate app-specific password** (appleid.apple.com > Security > App-Specific Passwords)
3. **Use these settings:**
   - Server: `imap.mail.me.com`
   - Port: `993`
   - SSL: Required

### Basic Connection Code

```python
import imaplib
import email
from email.header import decode_header

# Gmail connection
def connect_gmail(email_address, app_password):
    """Connect to Gmail via IMAP"""
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login(email_address, app_password)
    return imap

# iCloud connection
def connect_icloud(email_address, app_password):
    """Connect to iCloud via IMAP"""
    imap = imaplib.IMAP4_SSL("imap.mail.me.com", 993)
    imap.login(email_address, app_password)
    return imap

# Usage
try:
    gmail = connect_gmail("yourname@gmail.com", "your-app-password")
    print("Connected to Gmail:", gmail.list())

    icloud = connect_icloud("eddale@mac.com", "your-app-password")
    print("Connected to iCloud:", icloud.list())

except imaplib.IMAP4.error as e:
    print(f"Login failed: {e}")
```

**What just happened?**
- `IMAP4_SSL` = Secure connection (like HTTPS for email)
- `login()` = Authenticate with email + app password
- `list()` = Returns all available mailboxes (Inbox, Sent, etc.)

---

## Part 2: Server-Side Search (The Fast Way)

### IMAP SEARCH Command - Your Secret Weapon

IMAP search happens **on the server**, so you're not downloading thousands of emails just to filter them. Think of it like asking the librarian to find books for you vs. reading every title yourself.

### Common Search Criteria

```python
def search_emails(imap, criteria):
    """
    Search emails on the server using IMAP SEARCH

    Common criteria:
    - ALL: All messages
    - UNSEEN: Unread messages
    - SEEN: Read messages
    - FROM "sender@email.com": From specific sender
    - TO "recipient@email.com": To specific recipient
    - SUBJECT "keyword": Subject contains keyword
    - BODY "text": Body contains text
    - SINCE "1-Jan-2026": After date
    - BEFORE "31-Dec-2025": Before date
    - OR: Combine criteria
    """
    imap.select("INBOX")  # Select mailbox
    status, messages = imap.search(None, criteria)

    if status == "OK":
        # Returns list of message IDs as bytes
        message_ids = messages[0].split()
        return message_ids
    return []

# Examples for "Waiting For" tracker
gmail = connect_gmail("yourname@gmail.com", "app-password")

# All unread emails
unread = search_emails(gmail, "UNSEEN")

# Emails from specific person
from_john = search_emails(gmail, 'FROM "john@example.com"')

# Emails with "waiting" in subject
waiting = search_emails(gmail, 'SUBJECT "waiting"')

# Sent emails (to track what YOU'RE waiting on)
gmail.select("[Gmail]/Sent Mail")  # Gmail's sent folder
sent_last_week = search_emails(gmail, 'SINCE "25-Dec-2025"')

# Complex: Unread emails from client after Dec 25
complex = search_emails(gmail, '(FROM "client@example.com" SINCE "25-Dec-2025" UNSEEN)')
```

### Speed: Server-Side vs Client-Side

**Server-side (IMAP SEARCH):**
- Searches 10,000 emails in ~1-2 seconds
- Only returns message IDs (tiny data transfer)
- Server does the heavy lifting

**Client-side (download all, then filter):**
- Downloads all headers/bodies first (slow, bandwidth-heavy)
- Then filters locally in Python
- Only use if you need complex Python logic the server can't do

**Rule of thumb:** Always use server-side search unless you need regex or complex date math.

---

## Part 3: Fetching Email Content

### The Three Levels of Email Data

1. **Envelope** - Fastest, just IDs and flags
2. **Headers** - Fast, subject/from/to/date
3. **Full body** - Slower, includes HTML/text/attachments

### Fetching Headers Only (Recommended for Tracking)

```python
def fetch_email_headers(imap, message_id):
    """Fetch just the headers - fast and efficient"""
    status, msg_data = imap.fetch(message_id, "(RFC822.HEADER)")

    if status == "OK":
        email_msg = email.message_from_bytes(msg_data[0][1])

        # Decode subject (handles encoding like UTF-8, etc.)
        subject = decode_header(email_msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        return {
            "from": email_msg.get("From"),
            "to": email_msg.get("To"),
            "subject": subject,
            "date": email_msg.get("Date"),
            "message_id": email_msg.get("Message-ID")
        }
    return None

# Usage
message_ids = search_emails(gmail, 'SUBJECT "proposal"')
for msg_id in message_ids[:5]:  # First 5 results
    headers = fetch_email_headers(gmail, msg_id)
    print(f"Subject: {headers['subject']}")
    print(f"From: {headers['from']}")
    print(f"Date: {headers['date']}\n")
```

### Fetching Full Email (Body + Attachments)

```python
def fetch_full_email(imap, message_id):
    """Fetch complete email including body and attachments"""
    status, msg_data = imap.fetch(message_id, "(RFC822)")

    if status != "OK":
        return None

    email_msg = email.message_from_bytes(msg_data[0][1])

    # Extract body
    body = ""
    attachments = []

    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Get body
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()

            # Get attachments
            elif "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        "filename": filename,
                        "data": part.get_payload(decode=True)
                    })
    else:
        # Not multipart, just get payload
        body = email_msg.get_payload(decode=True).decode()

    return {
        "subject": decode_header(email_msg["Subject"])[0][0],
        "from": email_msg.get("From"),
        "to": email_msg.get("To"),
        "date": email_msg.get("Date"),
        "body": body,
        "attachments": attachments
    }

# Usage
full_email = fetch_full_email(gmail, message_ids[0])
print(f"Body preview: {full_email['body'][:200]}...")
print(f"Attachments: {len(full_email['attachments'])}")
```

---

## Part 4: Mac Mail Integration - How It Works

### The Key Insight

**Mac Mail and your Python script use the same protocol (IMAP), talking to the same server.**

Think of it like two web browsers looking at the same website. They both see the server's version of the emails.

### What This Means for You

1. **Emails are on the server** - Gmail/iCloud servers store the "master copy"
2. **Mac Mail is a client** - It syncs with the server
3. **Your Python script is also a client** - It also syncs with the server
4. **They don't talk to each other** - Both talk to the server

### Practical Example: "Waiting For" Workflow

```
You send email from Mac Mail
    ↓
Email goes to Gmail server (Sent folder)
    ↓
Python script reads Gmail server (Sent folder)
    ↓
Script finds "waiting for" emails
    ↓
Script marks them with a label/flag on server
    ↓
Mac Mail sees the label/flag (because it syncs with server)
```

### Can You Search Mac Mail's Local Database?

**No, and you don't want to.**

- Mac Mail stores emails in `~/Library/Mail/V10/` (proprietary SQLite database)
- Database format changes between macOS versions
- Would only work on your Mac
- IMAP is more reliable and portable

**Better approach:** Your Python script searches the same servers Mac Mail uses.

---

## Part 5: Gmail API vs IMAP Comparison

### Gmail API Advantages

1. **Faster search** - Uses Google's search index (same tech as Gmail web)
2. **Better Gmail-specific features** - Labels, threads, categories
3. **Rate limits** - Higher throughput (but you won't hit IMAP limits for personal use)
4. **Official Google support** - Better documentation

### Gmail API Disadvantages

1. **OAuth2 complexity** - Requires browser auth flow, token refresh logic
2. **Gmail only** - Won't work with iCloud, Outlook, etc.
3. **More code** - More boilerplate to maintain
4. **Credential management** - Need to store refresh tokens securely

### IMAP Advantages

1. **Universal** - Works with Gmail, iCloud, Outlook, any IMAP server
2. **Simple auth** - Just email + app password
3. **Standard protocol** - Been around since 1986, won't change
4. **Mac Mail compatibility** - Same protocol your email client uses

### IMAP Disadvantages

1. **Slower for huge volumes** - Gmail API is faster for 100,000+ emails
2. **Less Gmail-specific** - No thread grouping, limited label support
3. **Connection overhead** - Need to maintain connection or reconnect

### Code Comparison: Search for "Waiting For" Emails

**IMAP (Simple):**
```python
import imaplib

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login("you@gmail.com", "app-password")
imap.select("INBOX")
status, messages = imap.search(None, 'SUBJECT "waiting"')
print(f"Found {len(messages[0].split())} emails")
```

**Gmail API (Complex):**
```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Token management
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(
    userId='me', q='subject:waiting').execute()
messages = results.get('messages', [])
print(f"Found {len(messages)} emails")
```

**Line count:** IMAP = 6 lines, Gmail API = 25+ lines

---

## Part 6: Recommendation for "Waiting For" Tracker

### Use IMAP Because:

1. **You have multiple email accounts** (Gmail + iCloud)
2. **You want quick prototype** (30-90 min rule)
3. **Personal use** (not processing millions of emails)
4. **Simple search needs** (subject, sender, date - all supported by IMAP)
5. **Mac Mail integration** (same protocol = guaranteed compatibility)

### Sample "Waiting For" Implementation

```python
import imaplib
import email
from datetime import datetime, timedelta
from email.header import decode_header

class WaitingForTracker:
    def __init__(self, email_address, app_password, server="imap.gmail.com"):
        self.imap = imaplib.IMAP4_SSL(server)
        self.imap.login(email_address, app_password)

    def find_sent_emails_without_replies(self, days_back=7):
        """
        Find emails YOU sent that haven't gotten replies
        = Things you're waiting for
        """
        # Calculate date threshold
        date_threshold = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")

        # Search sent mail
        self.imap.select("[Gmail]/Sent Mail")  # Gmail sent folder
        status, sent_ids = self.imap.search(None, f'SINCE "{date_threshold}"')

        waiting_for = []

        for msg_id in sent_ids[0].split():
            # Get sent email headers
            status, data = self.imap.fetch(msg_id, "(RFC822.HEADER)")
            sent_email = email.message_from_bytes(data[0][1])

            # Check if there's a reply
            message_id = sent_email.get("Message-ID")

            # Search inbox for replies (emails with In-Reply-To matching our Message-ID)
            self.imap.select("INBOX")
            status, reply_ids = self.imap.search(None, f'HEADER In-Reply-To "{message_id}"')

            if not reply_ids[0]:
                # No reply found - you're waiting!
                subject = decode_header(sent_email["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                waiting_for.append({
                    "to": sent_email.get("To"),
                    "subject": subject,
                    "date": sent_email.get("Date"),
                    "message_id": message_id
                })

        return waiting_for

    def search_by_keyword(self, keyword, mailbox="INBOX"):
        """Search any mailbox for keyword in subject or body"""
        self.imap.select(mailbox)

        # Search subject OR body
        status, ids = self.imap.search(None, f'OR SUBJECT "{keyword}" BODY "{keyword}"')

        results = []
        for msg_id in ids[0].split():
            headers = self.fetch_headers(msg_id)
            results.append(headers)

        return results

    def fetch_headers(self, message_id):
        """Helper to fetch email headers"""
        status, data = self.imap.fetch(message_id, "(RFC822.HEADER)")
        email_msg = email.message_from_bytes(data[0][1])

        subject = decode_header(email_msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        return {
            "from": email_msg.get("From"),
            "to": email_msg.get("To"),
            "subject": subject,
            "date": email_msg.get("Date")
        }

    def close(self):
        self.imap.logout()

# Usage
tracker = WaitingForTracker("you@gmail.com", "your-app-password")

# Find unanswered emails from last 7 days
waiting = tracker.find_sent_emails_without_replies(days_back=7)
print(f"\nYou're waiting for {len(waiting)} responses:\n")
for item in waiting:
    print(f"To: {item['to']}")
    print(f"Subject: {item['subject']}")
    print(f"Sent: {item['date']}\n")

# Search for specific tracking tag
tagged = tracker.search_by_keyword("WAITING-FOR")
print(f"\nFound {len(tagged)} emails tagged WAITING-FOR")

tracker.close()
```

---

## Part 7: Quick Start Checklist

### To Build Your "Waiting For" Tracker:

- [ ] Enable IMAP in Gmail settings
- [ ] Generate Gmail app password
- [ ] Generate iCloud app-specific password (if using eddale@mac.com)
- [ ] Install Python: `pip install secure-smtplib` (imaplib is built-in)
- [ ] Test connection to Gmail
- [ ] Test connection to iCloud
- [ ] Implement sent-without-reply search
- [ ] Add keyword tagging (e.g., "WAITING-FOR" in subject)
- [ ] Schedule daily check (cron job or scheduled Python script)

### Security Notes

**App passwords are like keys to your email. Keep them safe:**
- Store in environment variables, not code
- Use `.env` file with `python-dotenv`
- Never commit to git
- Rotate periodically

```python
# Secure way to handle credentials
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

gmail_password = os.getenv("GMAIL_APP_PASSWORD")
icloud_password = os.getenv("ICLOUD_APP_PASSWORD")

tracker = WaitingForTracker("you@gmail.com", gmail_password)
```

---

## The Bottom Line

**IMAP is your friend for this project.**

It's like using the same language Mac Mail speaks. Simple, universal, fast enough for personal email volumes, and works with all your accounts.

Gmail API is like building a custom integration for Gmail only - more power, but way more complexity. Save it for when you're processing thousands of emails per hour.

**Translation to copywriting:** IMAP is like writing in plain English that works everywhere. Gmail API is like writing in Google-specific jargon that only works on their platform.

---

**Next Steps:** See `skills/email-waiting-tracker/` for implementation (once built).
