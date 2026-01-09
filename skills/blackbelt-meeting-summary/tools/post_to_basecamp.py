#!/usr/bin/env python3
"""
Post a meeting summary to Basecamp.

Usage:
    python3 post_to_basecamp.py --client "Brad Twynham" --summary /path/to/summary.md
    python3 post_to_basecamp.py --client "Brad Twynham" --content "Direct content here"
    python3 post_to_basecamp.py --todo-id 9313565737 --summary /path/to/summary.md
    python3 post_to_basecamp.py --list-clients "Brad"  # Search for clients

Exit codes:
    0 - Success
    1 - Client not found
    2 - API error
    3 - Configuration error
"""

import argparse
import sys
import json
from pathlib import Path

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from basecamp_client import BasecampClient, markdown_to_basecamp_html


def find_and_confirm_client(client: BasecampClient, name: str, auto_confirm: bool = False) -> dict:
    """Find client and confirm if match score is low."""
    result = client.find_client(name)

    if not result:
        print(f"ERROR: No client found matching '{name}'", file=sys.stderr)
        print("\nTry searching with --list-clients to see available matches.", file=sys.stderr)
        sys.exit(1)

    print(f"Found: {result['name']} (match: {result['score']:.0%})")
    print(f"  Group: {result['group'].replace('_', ' ').title()}")
    print(f"  Todo ID: {result['todo_id']}")

    if result['score'] < 0.9 and not auto_confirm:
        print(f"\nMatch confidence is {result['score']:.0%}. Please confirm this is correct.")
        confirm = input(f"Post to '{result['name']}'? [y/N] ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            sys.exit(0)

    return result


def post_summary(client: BasecampClient, todo_id: int, content: str, is_markdown: bool = True):
    """Post content to a client's todo."""
    if is_markdown:
        html_content = markdown_to_basecamp_html(content)
    else:
        # Assume already HTML or plain text
        if not content.startswith('<'):
            html_content = f"<div>{content}</div>"
        else:
            html_content = content

    try:
        result = client.post_comment(todo_id, html_content)
        print(f"\n✓ Comment posted successfully!")
        print(f"  Comment ID: {result['id']}")
        print(f"  View at: {result.get('app_url', 'Check Basecamp')}")
        return result
    except Exception as e:
        print(f"\nERROR: Failed to post comment: {e}", file=sys.stderr)
        sys.exit(2)


def list_clients(client: BasecampClient, search: str = ""):
    """List clients matching search term."""
    if search:
        matches = client.find_clients(search, limit=10)
        print(f"Top matches for '{search}':\n")
    else:
        matches = client.get_all_clients()[:20]
        print("Recent clients (showing first 20):\n")

    for m in matches:
        score = f" ({m['score']:.0%})" if 'score' in m else ""
        group = m['group'].replace('_', ' ').title()
        print(f"  {m['name']}{score}")
        print(f"    ID: {m['todo_id']} | Group: {group}")


def main():
    parser = argparse.ArgumentParser(
        description="Post meeting summaries to Basecamp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Client identification (one required)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--client", "-c", help="Client name to search for")
    group.add_argument("--todo-id", "-t", type=int, help="Direct Basecamp todo ID")
    group.add_argument("--list-clients", "-l", nargs="?", const="", metavar="SEARCH",
                       help="List clients (optionally filtered by search term)")

    # Content (one required for posting)
    parser.add_argument("--summary", "-s", type=Path, help="Path to summary markdown file")
    parser.add_argument("--content", help="Direct content to post")

    # Options
    parser.add_argument("--yes", "-y", action="store_true",
                        help="Auto-confirm client match without prompting")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show what would be posted without posting")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output result as JSON")

    args = parser.parse_args()

    # Initialize client
    try:
        bc = BasecampClient()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    # Handle --list-clients
    if args.list_clients is not None:
        list_clients(bc, args.list_clients)
        return

    # Need either --client or --todo-id for posting
    if not args.client and not args.todo_id:
        parser.error("Either --client or --todo-id is required for posting")

    # Need either --summary or --content
    if not args.summary and not args.content:
        parser.error("Either --summary or --content is required")

    # Get content
    if args.summary:
        if not args.summary.exists():
            print(f"ERROR: Summary file not found: {args.summary}", file=sys.stderr)
            sys.exit(1)
        content = args.summary.read_text()
    else:
        content = args.content

    # Get todo ID
    if args.client:
        client_info = find_and_confirm_client(bc, args.client, args.yes)
        todo_id = client_info['todo_id']
    else:
        todo_id = args.todo_id
        print(f"Posting to todo ID: {todo_id}")

    # Dry run
    if args.dry_run:
        print(f"\n[DRY RUN] Would post to todo {todo_id}:")
        print("-" * 40)
        html = markdown_to_basecamp_html(content)
        print(html[:500] + "..." if len(html) > 500 else html)
        return

    # Post it
    result = post_summary(bc, todo_id, content)

    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
