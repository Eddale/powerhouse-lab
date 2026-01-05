#!/usr/bin/env python3
"""
Test IMAP connections to Gmail and iCloud.
Verifies that app passwords are working correctly.
"""

import imaplib
import os
import sys


def test_gmail():
    """Test Gmail IMAP connection."""
    address = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")

    if not address or not password:
        print("❌ Gmail: Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD env vars")
        return False

    try:
        # Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(address, password)

        # Quick test - list mailboxes
        status, mailboxes = mail.list()
        mailbox_count = len(mailboxes) if mailboxes else 0

        mail.logout()
        print(f"✅ Gmail: Connected successfully ({mailbox_count} mailboxes found)")
        return True

    except imaplib.IMAP4.error as e:
        print(f"❌ Gmail: Authentication failed - {e}")
        return False
    except Exception as e:
        print(f"❌ Gmail: Connection error - {e}")
        return False


def test_icloud():
    """Test iCloud IMAP connection."""
    address = os.environ.get("ICLOUD_ADDRESS")
    password = os.environ.get("ICLOUD_APP_PASSWORD")

    if not address or not password:
        print("❌ iCloud: Missing ICLOUD_ADDRESS or ICLOUD_APP_PASSWORD env vars")
        return False

    try:
        # iCloud IMAP server
        mail = imaplib.IMAP4_SSL("imap.mail.me.com", 993)
        mail.login(address, password)

        # Quick test - list mailboxes
        status, mailboxes = mail.list()
        mailbox_count = len(mailboxes) if mailboxes else 0

        mail.logout()
        print(f"✅ iCloud: Connected successfully ({mailbox_count} mailboxes found)")
        return True

    except imaplib.IMAP4.error as e:
        print(f"❌ iCloud: Authentication failed - {e}")
        return False
    except Exception as e:
        print(f"❌ iCloud: Connection error - {e}")
        return False


if __name__ == "__main__":
    print("Testing IMAP connections...\n")

    gmail_ok = test_gmail()
    icloud_ok = test_icloud()

    print()
    if gmail_ok and icloud_ok:
        print("🎉 All connections working! Ready to build the Email Agent.")
        sys.exit(0)
    else:
        print("⚠️  Some connections failed. Check credentials above.")
        sys.exit(1)
