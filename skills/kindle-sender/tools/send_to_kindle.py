#!/usr/bin/env python3
"""
Send markdown documents to Kindle via email.

Converts markdown to EPUB using pypandoc, then emails to your Kindle address.
Amazon's Send-to-Kindle service converts EPUB to Kindle format automatically
when the subject line is "Convert".

Usage:
    python3 send_to_kindle.py --daily-note "2026-01-10" [--dry-run]
    python3 send_to_kindle.py --someday-maybe [--dry-run]
    python3 send_to_kindle.py --files "Doc1.md" "Doc2.md" [--dry-run]

Environment variables required:
    KINDLE_EMAIL - Your Kindle email (e.g., yourname@kindle.com)
    GMAIL_USER - Your Gmail address
    GMAIL_APP_PASSWORD - Gmail app password (not regular password)
"""

import argparse
import os
import re
import smtplib
import sys
import tempfile
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict, Optional

# Configuration
ZETTELKASTEN_PATH = Path("/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten")
SOMEDAY_MAYBE_FILE = ZETTELKASTEN_PATH / "Someday-Maybe.md"


def check_environment():
    """Verify all required environment variables are set."""
    # Support both GMAIL_USER and GMAIL_ADDRESS (Ed uses GMAIL_ADDRESS)
    gmail_user = os.environ.get("GMAIL_USER") or os.environ.get("GMAIL_ADDRESS")
    kindle_email = os.environ.get("KINDLE_EMAIL")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    missing = []
    if not kindle_email:
        missing.append("KINDLE_EMAIL")
    if not gmail_user:
        missing.append("GMAIL_USER or GMAIL_ADDRESS")
    if not gmail_password:
        missing.append("GMAIL_APP_PASSWORD")

    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        print("\nAdd these to ~/.zshrc:")
        print('  export KINDLE_EMAIL="your-name@kindle.com"')
        print('  export GMAIL_ADDRESS="your-email@gmail.com"')
        print('  export GMAIL_APP_PASSWORD="your-app-password"')
        print("\nThen run: source ~/.zshrc")
        sys.exit(1)

    return {
        "kindle_email": kindle_email,
        "gmail_user": gmail_user,
        "gmail_password": gmail_password,
    }


def extract_research_links(daily_note_path: Path) -> List[str]:
    """
    Extract Research Swarm wikilinks from the Captures section of a daily note.

    Returns list of document names (without [[ ]] brackets).
    """
    if not daily_note_path.exists():
        print(f"ERROR: Daily note not found: {daily_note_path}")
        return []

    content = daily_note_path.read_text()

    # Find Captures section
    captures_match = re.search(r"## Captures\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if not captures_match:
        print("WARNING: No Captures section found in daily note")
        return []

    captures_section = captures_match.group(1)

    # Find all Research Swarm wikilinks
    # Matches [[Research Swarm - anything]]
    pattern = r"\[\[(Research Swarm - [^\]]+)\]\]"
    matches = re.findall(pattern, captures_section)

    return matches


def find_markdown_file(doc_name: str) -> Optional[Path]:
    """Find the markdown file for a document name in Zettelkasten."""
    # Try exact match first
    md_path = ZETTELKASTEN_PATH / f"{doc_name}.md"
    if md_path.exists():
        return md_path

    # Try without date suffix variations
    print(f"WARNING: File not found: {md_path}")
    return None


def convert_to_epub(md_path: Path, output_path: Path, title: str = None) -> bool:
    """
    Convert markdown file to EPUB using pypandoc.

    Returns True on success, False on failure.
    """
    try:
        import pypandoc
    except ImportError:
        print("ERROR: pypandoc not installed. Run: pip3 install pypandoc pypandoc_binary")
        return False

    if title is None:
        title = md_path.stem

    try:
        pypandoc.convert_file(
            str(md_path),
            "epub",
            outputfile=str(output_path),
            extra_args=[
                f"--metadata=title:{title}",
                "--metadata=author:Ed Dale",
                "--standalone",
            ]
        )
        return True
    except Exception as e:
        print(f"ERROR converting {md_path.name}: {e}")
        return False


def send_email(epub_path: Path, config: dict) -> bool:
    """
    Send EPUB file to Kindle via Gmail SMTP.

    Subject line "Convert" tells Amazon to convert to Kindle format.
    Returns True on success, False on failure.
    """
    msg = MIMEMultipart()
    msg["From"] = config["gmail_user"]
    msg["To"] = config["kindle_email"]
    msg["Subject"] = "Convert"  # Magic subject for Kindle conversion

    # Body text (mostly ignored by Kindle)
    body = f"Sent via kindle-sender skill at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg.attach(MIMEText(body, "plain"))

    # Attach EPUB
    with open(epub_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="epub+zip")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=epub_path.name
        )
        msg.attach(attachment)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config["gmail_user"], config["gmail_password"])
            server.send_message(msg)
        return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed.")
        print("Make sure you're using an App Password, not your regular password.")
        print("Create one at: Google Account -> Security -> App passwords")
        return False
    except Exception as e:
        print(f"ERROR sending email: {e}")
        return False


def process_documents(doc_names: List[str], dry_run: bool = False) -> Dict:
    """
    Process a list of document names: convert to EPUB and send to Kindle.

    Returns dict with counts: {"found": N, "converted": N, "sent": N, "failed": []}
    """
    results = {"found": 0, "converted": 0, "sent": 0, "failed": []}

    if not dry_run:
        config = check_environment()

    for doc_name in doc_names:
        md_path = find_markdown_file(doc_name)
        if not md_path:
            results["failed"].append(f"{doc_name} (not found)")
            continue

        results["found"] += 1

        if dry_run:
            print(f"  [DRY RUN] Would send: {md_path.name}")
            continue

        # Convert to EPUB in temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            epub_path = Path(tmpdir) / f"{md_path.stem}.epub"

            print(f"  Converting: {md_path.name}")
            if not convert_to_epub(md_path, epub_path, title=doc_name):
                results["failed"].append(f"{doc_name} (conversion failed)")
                continue

            results["converted"] += 1

            print(f"  Sending: {epub_path.name}")
            if send_email(epub_path, config):
                results["sent"] += 1
                print(f"  Sent: {doc_name}")
            else:
                results["failed"].append(f"{doc_name} (send failed)")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Send markdown documents to Kindle"
    )
    parser.add_argument(
        "--daily-note",
        metavar="DATE",
        help="Date of daily note to extract Research Swarm links from (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--someday-maybe",
        action="store_true",
        help="Send the Someday-Maybe.md file"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        metavar="FILE",
        help="Specific markdown files to send (names or paths)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be sent without actually sending"
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.daily_note, args.someday_maybe, args.files]):
        parser.error("Must specify one of: --daily-note, --someday-maybe, or --files")

    doc_names = []

    # Mode 1: Extract from daily note
    if args.daily_note:
        daily_note_path = ZETTELKASTEN_PATH / f"{args.daily_note}.md"
        print(f"Scanning daily note: {daily_note_path.name}")
        doc_names = extract_research_links(daily_note_path)

        if not doc_names:
            print("No Research Swarm documents found in Captures section.")
            sys.exit(0)

        print(f"Found {len(doc_names)} Research Swarm document(s):")
        for name in doc_names:
            print(f"  - {name}")
        print()

    # Mode 2: Someday-Maybe file
    elif args.someday_maybe:
        if not SOMEDAY_MAYBE_FILE.exists():
            print(f"ERROR: Someday-Maybe.md not found at {SOMEDAY_MAYBE_FILE}")
            sys.exit(1)
        doc_names = ["Someday-Maybe"]
        print("Will send: Someday-Maybe.md")
        print()

    # Mode 3: Specific files
    elif args.files:
        for f in args.files:
            # Handle both full paths and names
            if os.path.isabs(f):
                doc_names.append(Path(f).stem)
            else:
                # Remove .md extension if present
                doc_names.append(f.replace(".md", ""))
        print(f"Will send {len(doc_names)} file(s):")
        for name in doc_names:
            print(f"  - {name}")
        print()

    # Process
    if args.dry_run:
        print("[DRY RUN MODE - No documents will actually be sent]\n")

    results = process_documents(doc_names, dry_run=args.dry_run)

    # Summary
    print("\n" + "=" * 40)
    if args.dry_run:
        print(f"DRY RUN COMPLETE: Would send {results['found']} document(s)")
    else:
        print(f"COMPLETE: Sent {results['sent']} of {results['found']} document(s)")

    if results["failed"]:
        print(f"\nFailed ({len(results['failed'])}):")
        for fail in results["failed"]:
            print(f"  - {fail}")

    # Exit code
    sys.exit(0 if not results["failed"] else 1)


if __name__ == "__main__":
    main()
