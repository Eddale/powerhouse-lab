"""
Waiting For - Gmail API Automation (Phase 2/3)

This is a CONCEPT SCRIPT showing how to automate:
1. Scanning sent emails for unreplied threads
2. Detecting when replies arrive
3. Creating/updating Obsidian notes

NOT PRODUCTION-READY - requires setup:
- Gmail API credentials
- OAuth2 authentication
- Obsidian vault path configuration
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import yaml
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ============================================================================
# CONFIGURATION
# ============================================================================

OBSIDIAN_VAULT_PATH = Path.home() / "Documents/Obsidian/YourVault"
WAITING_FOR_ACTIVE = OBSIDIAN_VAULT_PATH / "waiting-for/active"
WAITING_FOR_RESOLVED = OBSIDIAN_VAULT_PATH / "waiting-for/resolved"

# Email addresses to always track (important contacts)
TRACK_ALWAYS = [
    "important@client.com",
    "boss@company.com"
]

# Keywords that indicate expecting a reply
EXPECTING_REPLY_KEYWORDS = [
    "?",  # Questions usually expect replies
    "please",
    "could you",
    "can you",
    "let me know",
    "get back to me",
    "respond",
    "reply"
]

# Days before suggesting follow-up
FOLLOW_UP_THRESHOLD_DAYS = 5


# ============================================================================
# GMAIL API FUNCTIONS
# ============================================================================

def get_gmail_service(credentials_path):
    """
    Authenticate and return Gmail API service.

    Args:
        credentials_path: Path to OAuth2 credentials JSON

    Returns:
        Gmail API service object
    """
    creds = Credentials.from_authorized_user_file(credentials_path)
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unreplied_threads(service, days_back=7):
    """
    Find email threads where you sent the last message.

    Args:
        service: Gmail API service
        days_back: How many days to look back

    Returns:
        List of thread dictionaries with metadata
    """
    try:
        # Calculate date threshold
        date_threshold = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')

        # Search for emails you sent after the date
        query = f'from:me after:{date_threshold}'

        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=100
        ).execute()

        messages = results.get('messages', [])
        unreplied_threads = []

        for msg in messages:
            thread_id = msg['threadId']

            # Get full thread
            thread = service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()

            # Check if you sent the last message
            last_message = thread['messages'][-1]
            headers = {h['name']: h['value'] for h in last_message['payload']['headers']}

            # Get your email address
            profile = service.users().getProfile(userId='me').execute()
            my_email = profile['emailAddress']

            # If last message is from you, it's unreplied
            if headers.get('From', '').lower().find(my_email.lower()) != -1:
                # Extract metadata
                thread_data = {
                    'thread_id': thread_id,
                    'subject': headers.get('Subject', 'No Subject'),
                    'to': headers.get('To', ''),
                    'date': headers.get('Date', ''),
                    'snippet': last_message.get('snippet', ''),
                    'body': get_message_body(last_message)
                }

                unreplied_threads.append(thread_data)

        return unreplied_threads

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []


def get_message_body(message):
    """Extract plain text body from message."""
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                import base64
                body = part['body'].get('data', '')
                return base64.urlsafe_b64decode(body).decode('utf-8')
    return message.get('snippet', '')


def is_expecting_reply(subject, body):
    """
    Heuristic to determine if email expects a reply.

    Args:
        subject: Email subject
        body: Email body

    Returns:
        Boolean and confidence score
    """
    combined_text = (subject + ' ' + body).lower()

    matches = sum(1 for keyword in EXPECTING_REPLY_KEYWORDS if keyword in combined_text)

    # If multiple keywords found, likely expecting reply
    if matches >= 2:
        return True, 0.9
    elif matches == 1:
        return True, 0.6
    else:
        return False, 0.3


def extract_recipient_name(to_field):
    """Extract name from 'To:' field."""
    # Handle formats: "Name <email@domain.com>" or just "email@domain.com"
    if '<' in to_field:
        return to_field.split('<')[0].strip().strip('"')
    else:
        return to_field.split('@')[0].replace('.', ' ').title()


# ============================================================================
# OBSIDIAN NOTE FUNCTIONS
# ============================================================================

def create_waiting_for_note(thread_data, expected_days=3):
    """
    Create a waiting-for note in Obsidian.

    Args:
        thread_data: Dictionary with email metadata
        expected_days: Days until expected response
    """
    person = extract_recipient_name(thread_data['to'])
    sent_date = datetime.now().strftime('%Y-%m-%d')  # Simplified - should parse actual date
    expected_date = (datetime.now() + timedelta(days=expected_days)).strftime('%Y-%m-%d')

    # Create filename
    filename = f"{sent_date}-{person.lower().replace(' ', '-')}.md"
    filepath = WAITING_FOR_ACTIVE / filename

    # Build frontmatter
    frontmatter = {
        'person': person,
        'email': thread_data['to'],
        'subject': thread_data['subject'],
        'sent': sent_date,
        'expected': expected_date,
        'status': 'pending',
        'priority': 'normal',
        'thread_id': thread_data['thread_id']  # For tracking
    }

    # Build note content
    content = f"""---
{yaml.dump(frontmatter, default_flow_style=False)}---

# Waiting For: {person} - {thread_data['subject']}

## What I'm Waiting For
{thread_data['subject']}

## Context
{thread_data['snippet']}

## Email Details
- **Sent**: {sent_date}
- **Subject**: {thread_data['subject']}
- **Expected**: {expected_date}

## Email Preview
```
{thread_data['body'][:500]}...
```

## Follow-Up Plan
- If no response by {expected_date} → Send reminder


## Resolution

"""

    # Write note
    with open(filepath, 'w') as f:
        f.write(content)

    return filepath


def get_active_waiting_for_notes():
    """
    Load all active waiting-for notes.

    Returns:
        List of dictionaries with note metadata
    """
    notes = []

    for note_path in WAITING_FOR_ACTIVE.glob('*.md'):
        with open(note_path, 'r') as f:
            content = f.read()

        # Extract frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                frontmatter['filepath'] = note_path
                notes.append(frontmatter)

    return notes


def check_for_replies(service, waiting_notes):
    """
    Check if any waiting-for items have received replies.

    Args:
        service: Gmail API service
        waiting_notes: List of active waiting-for notes

    Returns:
        List of notes that should be marked as resolved
    """
    resolved_notes = []

    for note in waiting_notes:
        thread_id = note.get('thread_id')
        if not thread_id:
            continue

        # Get thread
        try:
            thread = service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()

            # Check if there are new messages
            messages = thread['messages']
            if len(messages) > 1:  # More than just your sent message
                # Check if last message is NOT from you
                last_message = messages[-1]
                headers = {h['name']: h['value'] for h in last_message['payload']['headers']}

                profile = service.users().getProfile(userId='me').execute()
                my_email = profile['emailAddress']

                if headers.get('From', '').lower().find(my_email.lower()) == -1:
                    # Reply received!
                    note['reply_date'] = headers.get('Date')
                    note['reply_from'] = headers.get('From')
                    resolved_notes.append(note)

        except HttpError as error:
            print(f'Error checking thread {thread_id}: {error}')
            continue

    return resolved_notes


def resolve_waiting_for_note(note):
    """
    Move note to resolved folder and update status.

    Args:
        note: Note metadata dictionary
    """
    filepath = note['filepath']

    # Read current content
    with open(filepath, 'r') as f:
        content = f.read()

    # Update frontmatter
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        frontmatter['status'] = 'resolved'
        frontmatter['resolved_date'] = datetime.now().strftime('%Y-%m-%d')

        # Update resolution section
        resolution_text = f"""## Resolution
- **Resolved**: {frontmatter['resolved_date']}
- **Reply from**: {note.get('reply_from', 'Unknown')}
- **Reply date**: {note.get('reply_date', 'Unknown')}
- **Outcome**: Reply received, auto-resolved by agent
"""

        body = parts[2].split('## Resolution')[0] + resolution_text

        new_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False)}---
{body}
"""

        # Write to resolved folder
        new_filepath = WAITING_FOR_RESOLVED / filepath.name
        with open(new_filepath, 'w') as f:
            f.write(new_content)

        # Delete from active folder
        filepath.unlink()

    return new_filepath


# ============================================================================
# AGENT WORKFLOW FUNCTIONS
# ============================================================================

def scan_and_suggest(service):
    """
    Main agent workflow: Scan for unreplied emails and suggest tracking.

    Returns:
        Dictionary with suggested items
    """
    print("Scanning sent emails for unreplied threads...")

    unreplied = get_unreplied_threads(service, days_back=7)

    # Filter to only those expecting replies
    suggestions = []

    for thread in unreplied:
        expecting, confidence = is_expecting_reply(thread['subject'], thread['body'])

        if expecting or thread['to'] in TRACK_ALWAYS:
            suggestions.append({
                'thread': thread,
                'confidence': confidence,
                'reason': 'Always track' if thread['to'] in TRACK_ALWAYS else f'Detected keywords ({confidence:.0%} confidence)'
            })

    return suggestions


def check_and_resolve(service):
    """
    Check active waiting-for items for replies and auto-resolve.

    Returns:
        List of resolved items
    """
    print("Checking active waiting-for items for replies...")

    active_notes = get_active_waiting_for_notes()
    resolved = check_for_replies(service, active_notes)

    for note in resolved:
        print(f"✓ Reply received: {note['person']} - {note['subject']}")
        resolve_waiting_for_note(note)

    return resolved


def generate_follow_up_report():
    """
    Generate daily report of items needing follow-up.

    Returns:
        Report string
    """
    active_notes = get_active_waiting_for_notes()

    today = datetime.now().date()
    overdue = []
    due_soon = []

    for note in active_notes:
        expected = datetime.strptime(note['expected'], '%Y-%m-%d').date()

        if expected < today:
            overdue.append(note)
        elif expected <= today + timedelta(days=2):
            due_soon.append(note)

    report = "# Waiting For - Daily Report\n\n"

    if overdue:
        report += "## ⚠️ Overdue (Need Follow-Up)\n\n"
        for note in overdue:
            days_overdue = (today - datetime.strptime(note['expected'], '%Y-%m-%d').date()).days
            report += f"- **{note['person']}** - {note['subject']} ({days_overdue} days overdue)\n"
        report += "\n"

    if due_soon:
        report += "## 📅 Due Soon\n\n"
        for note in due_soon:
            report += f"- **{note['person']}** - {note['subject']} (expected: {note['expected']})\n"
        report += "\n"

    if not overdue and not due_soon:
        report += "✅ No items need immediate follow-up.\n\n"

    report += f"**Total active items**: {len(active_notes)}\n"

    return report


# ============================================================================
# MAIN WORKFLOWS
# ============================================================================

def daily_morning_workflow(service):
    """
    Run this every morning to:
    1. Scan for new unreplied emails
    2. Suggest items to track
    3. Check for replies to existing items
    4. Generate follow-up report
    """
    print("\n=== Daily Morning Workflow ===\n")

    # 1. Scan and suggest
    suggestions = scan_and_suggest(service)

    if suggestions:
        print(f"\n📧 Found {len(suggestions)} emails that might need tracking:\n")
        for i, item in enumerate(suggestions, 1):
            print(f"{i}. {item['thread']['to']} - {item['thread']['subject']}")
            print(f"   Reason: {item['reason']}\n")

        # In real implementation, prompt user to approve
        # For now, auto-create (or skip)
        print("(In production, you'd approve each item here)\n")

    # 2. Check for replies
    resolved = check_and_resolve(service)

    if resolved:
        print(f"\n✅ {len(resolved)} items resolved (replies received)\n")

    # 3. Generate report
    report = generate_follow_up_report()
    print("\n" + report)

    # Save report to daily note (simplified)
    report_path = OBSIDIAN_VAULT_PATH / f"daily-notes/{datetime.now().strftime('%Y-%m-%d')}-waiting-for-report.md"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w') as f:
        f.write(report)

    print(f"\n📝 Report saved to: {report_path}")


def weekly_cleanup_workflow():
    """
    Run this weekly to:
    1. Identify aging items (7+ days)
    2. Suggest archiving irrelevant items
    3. Generate weekly stats
    """
    print("\n=== Weekly Cleanup Workflow ===\n")

    active_notes = get_active_waiting_for_notes()

    today = datetime.now().date()
    aging = []

    for note in active_notes:
        sent = datetime.strptime(note['sent'], '%Y-%m-%d').date()
        days_waiting = (today - sent).days

        if days_waiting >= 7:
            aging.append({
                'note': note,
                'days_waiting': days_waiting
            })

    if aging:
        print(f"⚠️ {len(aging)} items aging (7+ days waiting):\n")
        for item in sorted(aging, key=lambda x: x['days_waiting'], reverse=True):
            note = item['note']
            print(f"- {note['person']} - {note['subject']} ({item['days_waiting']} days)")

        print("\n(Review each item: Follow up? Archive? Still valid?)\n")

    # Generate stats
    resolved_notes_count = len(list(WAITING_FOR_RESOLVED.glob('*.md')))

    print(f"\n📊 Weekly Stats:")
    print(f"- Active items: {len(active_notes)}")
    print(f"- Resolved (all time): {resolved_notes_count}")
    print(f"- Aging (7+ days): {len(aging)}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example usage (requires Gmail API setup)
    """

    # This is a CONCEPT - you'd need to set up OAuth2 first
    # credentials_path = 'path/to/credentials.json'
    # service = get_gmail_service(credentials_path)

    # Run daily morning workflow
    # daily_morning_workflow(service)

    # Or run weekly cleanup
    # weekly_cleanup_workflow()

    print("""
    ============================================================
    WAITING FOR - GMAIL API AUTOMATION CONCEPT
    ============================================================

    This is a CONCEPT script showing the architecture for:

    Phase 2: Semi-Automatic
    - Scan sent emails for unreplied threads
    - Suggest items to track
    - Detect replies, auto-resolve

    Phase 3: Full Automation
    - Auto-create waiting-for items (with approval)
    - Auto-resolve when replies arrive
    - Generate daily/weekly reports
    - Surface follow-up recommendations

    TO USE THIS:
    1. Set up Gmail API credentials (Google Cloud Console)
    2. Install dependencies: google-auth, google-api-python-client, pyyaml
    3. Configure OBSIDIAN_VAULT_PATH
    4. Uncomment example usage code
    5. Run daily via cron or scheduled task

    RECOMMENDED APPROACH:
    - Start with Phase 1 (manual, iOS shortcut)
    - Validate the pattern for 2+ weeks
    - Then build Phase 2 (this script)
    - Test semi-automatic for 2+ weeks
    - Then add Phase 3 features (full automation)

    Don't rush to automate. The manual system teaches you the workflow.
    Then automation becomes obvious.
    ============================================================
    """)
