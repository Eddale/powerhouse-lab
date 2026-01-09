#!/usr/bin/env python3
"""
Fetch morning metrics from Gmail, iCloud Mail, and Google Calendar.
Outputs JSON for Claude to format into a briefing.
"""

import os
import json
import pickle
import imaplib
import email
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly',
]

def get_credentials():
    """Get OAuth credentials, refreshing if needed."""
    creds_path = os.environ.get('GOOGLE_CREDENTIALS_PATH',
                                os.path.expanduser('~/.config/claude-code-apis/credentials.json'))
    token_path = os.environ.get('GOOGLE_TOKEN_PATH',
                                os.path.expanduser('~/.config/claude-code-apis/token.pickle'))

    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_gmail_metrics(creds):
    """Get Gmail unread count and recent important emails."""
    try:
        service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

        # Get profile
        profile = service.users().getProfile(userId='me').execute()

        # Get unread count
        unread = service.users().messages().list(
            userId='me', q='is:unread', maxResults=1
        ).execute()
        unread_count = unread.get('resultSizeEstimate', 0)

        # Get primary inbox unread
        primary_unread = service.users().messages().list(
            userId='me', q='is:unread category:primary', maxResults=1
        ).execute()
        primary_count = primary_unread.get('resultSizeEstimate', 0)

        # Get recent important/starred unread
        important = service.users().messages().list(
            userId='me', q='is:unread is:important', maxResults=5
        ).execute()
        important_count = important.get('resultSizeEstimate', 0)

        # Get subjects of important unread emails
        important_emails = []
        for msg in important.get('messages', [])[:5]:
            msg_data = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['Subject', 'From']
            ).execute()
            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            important_emails.append({
                'subject': headers.get('Subject', '(no subject)'),
                'from': headers.get('From', 'Unknown')
            })

        return {
            'email': profile.get('emailAddress'),
            'unread_total': unread_count,
            'unread_primary': primary_count,
            'unread_important': important_count,
            'important_emails': important_emails,
            'status': 'ok'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def get_icloud_metrics():
    """Get iCloud Mail (eddale@mac.com) unread count via IMAP."""
    try:
        icloud_email = os.environ.get('ICLOUD_ADDRESS', 'eddale@mac.com')
        icloud_password = os.environ.get('ICLOUD_APP_PASSWORD')

        if not icloud_password:
            return {'status': 'error', 'error': 'ICLOUD_APP_PASSWORD not set'}

        # Connect to iCloud IMAP
        imap = imaplib.IMAP4_SSL('imap.mail.me.com')
        imap.login(icloud_email, icloud_password)

        # Get unread count from INBOX
        imap.select('INBOX')
        _, messages = imap.search(None, 'UNSEEN')
        unread_ids = messages[0].split() if messages[0] else []
        unread_count = len(unread_ids)

        # Get recent unread subjects (up to 5)
        recent_unread = []
        for msg_id in unread_ids[:5]:
            _, msg_data = imap.fetch(msg_id, '(RFC822.HEADER)')
            if msg_data and msg_data[0]:
                msg = email.message_from_bytes(msg_data[0][1])
                subject = msg.get('Subject', '(no subject)')
                from_addr = msg.get('From', 'Unknown')
                # Decode subject if needed
                if subject:
                    decoded = email.header.decode_header(subject)
                    subject = ''.join(
                        part.decode(charset or 'utf-8') if isinstance(part, bytes) else part
                        for part, charset in decoded
                    )
                recent_unread.append({
                    'subject': subject[:100],  # Truncate long subjects
                    'from': from_addr
                })

        imap.logout()

        return {
            'email': icloud_email,
            'unread_total': unread_count,
            'recent_unread': recent_unread,
            'status': 'ok'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def get_calendar_metrics(creds):
    """Get today's calendar events."""
    try:
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

        # Get today's date range in local timezone
        now = datetime.now(timezone.utc)

        # Start of today (midnight local time)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # Get events for today
        events_result = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat(),
            timeMax=today_end.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = []
        for event in events_result.get('items', []):
            start = event['start'].get('dateTime', event['start'].get('date'))
            events.append({
                'time': start,
                'summary': event.get('summary', 'No title'),
                'location': event.get('location', ''),
            })

        # Also get upcoming events (next 7 days) for context
        week_end = today_start + timedelta(days=7)
        upcoming_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=week_end.isoformat(),
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        upcoming = []
        for event in upcoming_result.get('items', []):
            start = event['start'].get('dateTime', event['start'].get('date'))
            upcoming.append({
                'time': start,
                'summary': event.get('summary', 'No title'),
            })

        return {
            'today_count': len(events),
            'today_events': events,
            'upcoming_count': len(upcoming),
            'upcoming_events': upcoming,
            'status': 'ok'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def main():
    """Fetch all metrics and output as JSON."""
    output = {
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%B %d, %Y'),
        'gmail': {},
        'icloud': {},
        'calendar': {}
    }

    try:
        creds = get_credentials()
        output['gmail'] = get_gmail_metrics(creds)
        output['calendar'] = get_calendar_metrics(creds)
    except Exception as e:
        output['google_error'] = str(e)

    # iCloud doesn't need Google creds
    output['icloud'] = get_icloud_metrics()

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
