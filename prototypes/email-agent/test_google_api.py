#!/usr/bin/env python3
"""
Test script for Google API credentials (Gmail + Calendar)
First run will open browser for OAuth consent.
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Gmail and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly',
]

def get_credentials():
    """Get or refresh OAuth credentials."""
    creds_path = os.environ.get('GOOGLE_CREDENTIALS_PATH',
                                 os.path.expanduser('~/.config/claude-code-apis/credentials.json'))
    token_path = os.environ.get('GOOGLE_TOKEN_PATH',
                                 os.path.expanduser('~/.config/claude-code-apis/token.pickle'))

    creds = None

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print(f"Starting OAuth flow...")
            print(f"Using credentials from: {creds_path}")
            print("Browser will open for Google consent...")
            print()
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print(f"Token saved to: {token_path}")

    return creds

def test_gmail(creds):
    """Test Gmail API connection."""
    print("\n--- Testing Gmail API ---")
    try:
        service = build('gmail', 'v1', credentials=creds)

        # Get profile info
        profile = service.users().getProfile(userId='me').execute()
        print(f"Email: {profile.get('emailAddress')}")
        print(f"Total messages: {profile.get('messagesTotal')}")
        print(f"Total threads: {profile.get('threadsTotal')}")

        # Get recent unread count
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        unread_estimate = results.get('resultSizeEstimate', 0)
        print(f"Unread messages: ~{unread_estimate}")

        # Get labels
        labels = service.users().labels().list(userId='me').execute()
        print(f"Labels: {len(labels.get('labels', []))}")

        print("Gmail API: OK")
        return True
    except Exception as e:
        print(f"Gmail API Error: {e}")
        return False

def test_calendar(creds):
    """Test Google Calendar API connection."""
    print("\n--- Testing Calendar API ---")
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Get calendar list
        calendars = service.calendarList().list().execute()
        print(f"Calendars: {len(calendars.get('items', []))}")

        for cal in calendars.get('items', [])[:3]:
            print(f"  - {cal.get('summary')}")

        # Get today's events from primary calendar
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        print(f"\nUpcoming events: {len(events)}")
        for event in events[:3]:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"  - {start}: {event.get('summary', 'No title')}")

        print("Calendar API: OK")
        return True
    except Exception as e:
        print(f"Calendar API Error: {e}")
        return False

def main():
    print("=" * 50)
    print("Google API Credentials Test")
    print("=" * 50)

    # Check credentials file exists
    creds_path = os.environ.get('GOOGLE_CREDENTIALS_PATH',
                                 os.path.expanduser('~/.config/claude-code-apis/credentials.json'))

    if not os.path.exists(creds_path):
        print(f"ERROR: Credentials file not found at {creds_path}")
        print("Make sure GOOGLE_CREDENTIALS_PATH is set correctly.")
        return

    print(f"Credentials: {creds_path}")

    # Get credentials (may trigger OAuth flow)
    creds = get_credentials()

    # Test both APIs
    gmail_ok = test_gmail(creds)
    calendar_ok = test_calendar(creds)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Gmail API:    {'PASS' if gmail_ok else 'FAIL'}")
    print(f"Calendar API: {'PASS' if calendar_ok else 'FAIL'}")

    if gmail_ok and calendar_ok:
        print("\nAll APIs working! Ready to build morning-metrics skill.")
    else:
        print("\nSome APIs failed. Check errors above.")

if __name__ == '__main__':
    main()
