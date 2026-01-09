# Build Plan: Basecamp API Integration

**Date:** 2026-01-10
**Goal:** Post meeting summaries directly to Basecamp instead of copy/paste
**Research:** [[Research Swarm - Basecamp API Integration - 2026-01-10]]
**Status:** REVISED after Ed's screenshots (2026-01-10)

---

## What We Learned From Screenshots

Ed's Basecamp structure:
- **Onboarding** project (bucket ID: `28135997`)
- **BB Onboarding Queue** is a TODO LIST (not a message board)
- Each client is a **TODO** with consistent naming: `DD.MM.YYYY | Client Name | (email) | Location`
- Clients move between lists (Template → Holding Pen → For 1st Velocity) but **todo ID stays the same**
- Meeting summaries go in the **comments** on each client's todo
- Account ID: `3087749`

**This is simpler than expected.** No manual config needed - we can search by client name.

---

## Current State

The skill generates Basecamp-ready summaries and displays them in a code block for copy/paste. Works well but manual. Ed wants one-click posting.

From `docs/README.md`:
> "No Basecamp API integration - copy/paste required"

This plan fixes that.

---

## The Build (In Order)

### Phase 1: API Access Setup (Ed does this - ~15 min)

**Why first:** Nothing works without credentials. Can't automate anything.

1. **Register app at 37signals**
   - Go to https://launchpad.37signals.com/integrations
   - Create new app: "BlackBelt Meeting Bot"
   - Get a personal access token (simplest for single-user)

2. **Store credentials**
   - Add to `~/.zshrc`:
     ```bash
     export BASECAMP_ACCOUNT_ID="3087749"
     export BASECAMP_ACCESS_TOKEN="your-access-token"
     ```

3. **Verify access**
   - Quick curl test to confirm token works

**Deliverable:** Working credentials that can hit the API

---

### Phase 2: Build Client Lookup Tool (~20 min)

**Why:** Find the todo ID for any client by name. No manual config needed.

**How it works:**
1. List all todos in the BB Onboarding Queue (todoset)
2. Parse client name from title: `DD.MM.YYYY | Client Name | (email) | Location`
3. Fuzzy match input name → return todo ID

**Create `tools/find-basecamp-client.py`:**

```python
#!/usr/bin/env python3
"""Find a client's todo ID by name in BB Onboarding Queue."""

import os
import re
import requests
from difflib import SequenceMatcher

ACCOUNT_ID = os.environ.get("BASECAMP_ACCOUNT_ID", "3087749")
ACCESS_TOKEN = os.environ.get("BASECAMP_ACCESS_TOKEN")
PROJECT_ID = "28135997"  # Onboarding project

# Need to discover this - the todoset ID for BB Onboarding Queue
TODOSET_ID = None  # Will fill in during build

BASE_URL = f"https://3.basecampapi.com/{ACCOUNT_ID}"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "BlackBelt Meeting Bot (ed@eddale.com)"
}

def parse_client_name(todo_title):
    """Extract client name from 'DD.MM.YYYY | Client Name | (email) | Location'"""
    parts = todo_title.split("|")
    if len(parts) >= 2:
        return parts[1].strip()
    return todo_title

def get_all_todos():
    """Fetch all todos from BB Onboarding Queue."""
    # First get the todoset, then iterate through todolists
    url = f"{BASE_URL}/buckets/{PROJECT_ID}/todosets/{TODOSET_ID}/todolists.json"
    response = requests.get(url, headers=HEADERS)
    todolists = response.json()

    all_todos = []
    for todolist in todolists:
        list_url = f"{BASE_URL}/buckets/{PROJECT_ID}/todolists/{todolist['id']}/todos.json"
        list_response = requests.get(list_url, headers=HEADERS)
        all_todos.extend(list_response.json())

    return all_todos

def find_client(search_name):
    """Find client todo by fuzzy name match."""
    todos = get_all_todos()

    best_match = None
    best_score = 0

    for todo in todos:
        client_name = parse_client_name(todo['title'])
        score = SequenceMatcher(None, search_name.lower(), client_name.lower()).ratio()

        if score > best_score:
            best_score = score
            best_match = {
                "name": client_name,
                "todo_id": todo['id'],
                "title": todo['title'],
                "score": score
            }

    if best_match and best_score > 0.6:
        return best_match
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: find-basecamp-client.py 'Client Name'")
        sys.exit(1)

    result = find_client(sys.argv[1])
    if result:
        print(f"Found: {result['name']} (score: {result['score']:.2f})")
        print(f"Todo ID: {result['todo_id']}")
    else:
        print("No matching client found")
```

**Deliverable:** Script that returns todo ID for any client name

---

### Phase 3: Build the Posting Tool (~20 min)

**Why:** Post comment to client's todo.

**Create `tools/post-to-basecamp.py`:**

```python
#!/usr/bin/env python3
"""Post a meeting summary to a client's Basecamp todo as a comment."""

import argparse
import os
import requests
import markdown

ACCOUNT_ID = os.environ.get("BASECAMP_ACCOUNT_ID", "3087749")
ACCESS_TOKEN = os.environ.get("BASECAMP_ACCESS_TOKEN")
PROJECT_ID = "28135997"

BASE_URL = f"https://3.basecampapi.com/{ACCOUNT_ID}"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "BlackBelt Meeting Bot (ed@eddale.com)"
}

def markdown_to_html(md_text):
    """Convert markdown to Basecamp-compatible HTML."""
    # Convert markdown to HTML
    html = markdown.markdown(md_text, extensions=['nl2br'])
    return f"<div>{html}</div>"

def post_comment(todo_id, summary_md):
    """Post summary as comment on the todo."""
    url = f"{BASE_URL}/buckets/{PROJECT_ID}/recordings/{todo_id}/comments.json"
    html_content = markdown_to_html(summary_md)

    response = requests.post(url, headers=HEADERS, json={"content": html_content})

    if response.status_code == 201:
        print(f"✓ Comment posted successfully")
        return response.json()
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--todo-id", required=True, help="Basecamp todo ID")
    parser.add_argument("--summary", required=True, help="Path to summary markdown")
    args = parser.parse_args()

    with open(args.summary) as f:
        summary = f.read()

    post_comment(args.todo_id, summary)
```

**Deliverable:** Script that posts HTML comment to any todo ID

---

### Phase 4: Combined Workflow Script (~15 min)

**Why:** Single command that does lookup + post.

**Create `tools/basecamp-post-summary.py`:**

```python
#!/usr/bin/env python3
"""Post meeting summary to Basecamp - finds client and posts in one step."""

import argparse
import sys
from find_basecamp_client import find_client
from post_to_basecamp import post_comment, markdown_to_html

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, help="Client name")
    parser.add_argument("--summary", required=True, help="Path to summary file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    args = parser.parse_args()

    # Find client
    result = find_client(args.client)
    if not result:
        print(f"✗ Could not find client matching '{args.client}'")
        sys.exit(1)

    print(f"Found: {result['name']} (match: {result['score']:.0%})")

    if result['score'] < 0.9:
        confirm = input(f"Post to '{result['name']}'? [y/N] ")
        if confirm.lower() != 'y':
            print("Cancelled")
            sys.exit(0)

    # Read summary
    with open(args.summary) as f:
        summary = f.read()

    if args.dry_run:
        print(f"\n[DRY RUN] Would post to todo {result['todo_id']}:")
        print(summary[:200] + "...")
        sys.exit(0)

    # Post it
    post_comment(result['todo_id'], summary)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python3 tools/basecamp-post-summary.py --client "Brad Twynham" --summary /tmp/summary.md
```

**Deliverable:** One command to find + post

---

### Phase 5: Update SKILL.md (~15 min)

**Changes to make:**

1. **Add `Bash` to allowed-tools**

2. **Add new step after "Display Copyable Output":**

   ```markdown
   ### Step 5: Offer Basecamp Posting

   After displaying the summary, ask Ed:

   "Post this summary to Basecamp for [Client Name]?"

   Options:
   - Yes, post it
   - No, I'll paste manually

   If yes:
   1. Save summary to temp file
   2. Run: `python3 tools/basecamp-post-summary.py --client "[Client]" --summary /tmp/summary.md`
   3. Report success or error
   4. Clean up temp file

   If client not found, show closest matches and ask to confirm.
   ```

3. **Add standalone trigger:**
   - "post summary to basecamp for [client]"

**Deliverable:** Skill can post directly after generating summary

---

### Phase 6: Update Documentation (~10 min)

1. **Update `docs/README.md`**
   - Remove "No Basecamp API integration" limitation
   - Add Basecamp credentials setup section
   - Document the tools

2. **Update `docs/ROADMAP.md`**
   - Move "Basecamp API Integration" to Shipped

3. **Add to CLAUDE.md env vars table**
   - `BASECAMP_ACCOUNT_ID`
   - `BASECAMP_ACCESS_TOKEN`

**Deliverable:** Docs reflect new capability

---

## Discovery Task: Find TODOSET_ID

Before Phase 2 works, we need to find the todoset ID for "BB Onboarding Queue".

Run this once Ed has credentials:
```bash
curl -s -H "Authorization: Bearer $BASECAMP_ACCESS_TOKEN" \
  "https://3.basecampapi.com/3087749/projects/28135997.json" | jq '.dock'
```

This returns the "dock" with all tools in the project. Find the todoset entry.

---

## Success Criteria

- [ ] Can post a summary to Basecamp with one confirmation
- [ ] Client lookup finds clients by name (fuzzy match)
- [ ] HTML formatting looks clean in Basecamp
- [ ] Credentials stored securely (env vars)
- [ ] Clear error when client not found
- [ ] Docs updated
- [ ] Manual paste still available as fallback

---

## Estimated Effort

| Phase | Time | Who |
|-------|------|-----|
| 1. API Setup | 15 min | Ed |
| 2. Client Lookup | 20 min | Claude |
| 3. Posting Tool | 20 min | Claude |
| 4. Combined Script | 15 min | Claude |
| 5. Update SKILL.md | 15 min | Claude |
| 6. Documentation | 10 min | Claude |
| **Total** | ~95 min | Both |

Phase 1 blocks everything else. Once Ed has credentials, the rest can be built in one session.

---

## Risk Assessment

**Low risk:**
- API is well-documented
- Todo structure is clear from screenshots
- Personal access tokens are simple

**Medium risk:**
- Fuzzy name matching (Brad vs Bradley)
- Rate limits if listing many todos

**Mitigation:**
- Show match confidence, ask for confirmation if <90%
- Cache todo list locally, refresh periodically
