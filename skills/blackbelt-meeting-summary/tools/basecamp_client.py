#!/usr/bin/env python3
"""
Basecamp API client for BlackBelt Meeting Bot.

Handles authentication, client lookup, and comment posting.
Configuration loaded from ~/.config/blackbelt-basecamp.yaml
"""

import os
import re
import requests
import yaml
from pathlib import Path
from difflib import SequenceMatcher
from typing import Optional, Dict, List, Any


class BasecampClient:
    """Client for interacting with Basecamp API."""

    CONFIG_PATH = Path.home() / ".config" / "blackbelt-basecamp.yaml"
    BASE_URL = "https://3.basecampapi.com"
    USER_AGENT = "BlackBelt Meeting Bot (ed@eddale.com)"

    def __init__(self):
        self.config = self._load_config()
        self.account_id = self.config["credentials"]["account_id"]
        self.access_token = self.config["credentials"]["access_token"]
        self.project_id = self.config["onboarding"]["project_id"]
        self.groups = self.config["onboarding"]["groups"]

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Config not found at {self.CONFIG_PATH}. "
                "Run the OAuth setup first."
            )
        with open(self.CONFIG_PATH) as f:
            return yaml.safe_load(f)

    def _headers(self) -> dict:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": self.USER_AGENT,
        }

    def _api_url(self, path: str) -> str:
        """Build full API URL."""
        return f"{self.BASE_URL}/{self.account_id}{path}"

    def _get(self, path: str) -> Any:
        """Make GET request to API."""
        response = requests.get(self._api_url(path), headers=self._headers())
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, data: dict) -> Any:
        """Make POST request to API."""
        response = requests.post(
            self._api_url(path),
            headers=self._headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    def refresh_access_token(self) -> str:
        """Use refresh token to get new access token."""
        refresh_token = self.config["credentials"]["refresh_token"]
        client_id = self.config["credentials"]["client_id"]
        client_secret = self.config["credentials"]["client_secret"]

        response = requests.post(
            "https://launchpad.37signals.com/authorization/token",
            data={
                "type": "refresh",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        )
        response.raise_for_status()
        data = response.json()

        # Update config with new token
        self.config["credentials"]["access_token"] = data["access_token"]
        self.access_token = data["access_token"]

        # Save updated config
        with open(self.CONFIG_PATH, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

        return data["access_token"]

    def get_all_clients(self) -> List[Dict]:
        """Get all clients from all onboarding groups."""
        all_clients = []

        for group_name, group_id in self.groups.items():
            try:
                todos = self._get(
                    f"/buckets/{self.project_id}/todolists/{group_id}/todos.json"
                )
                for todo in todos:
                    client_info = self._parse_client_title(todo["title"])
                    client_info["todo_id"] = todo["id"]
                    client_info["group"] = group_name
                    client_info["full_title"] = todo["title"]
                    all_clients.append(client_info)
            except Exception as e:
                # Group might be empty or inaccessible
                continue

        return all_clients

    def _parse_client_title(self, title: str) -> Dict:
        """
        Parse client info from todo title.
        Format: DD.MM.YYYY | Client Name | (email) | Location
        """
        parts = title.split("|")
        result = {"name": title, "email": "", "location": "", "date": ""}

        if len(parts) >= 2:
            result["date"] = parts[0].strip()
            result["name"] = parts[1].strip()

        if len(parts) >= 3:
            # Extract email from parentheses
            email_part = parts[2].strip()
            email_match = re.search(r'\(([^)]+)\)', email_part)
            if email_match:
                result["email"] = email_match.group(1)
            else:
                result["email"] = email_part

        if len(parts) >= 4:
            result["location"] = parts[3].strip()

        return result

    def find_client(self, search_name: str) -> Optional[Dict]:
        """Find client by name using fuzzy matching."""
        clients = self.get_all_clients()

        best_match = None
        best_score = 0

        for client in clients:
            # Match against client name
            score = SequenceMatcher(
                None,
                search_name.lower(),
                client["name"].lower()
            ).ratio()

            if score > best_score:
                best_score = score
                best_match = {**client, "score": score}

        if best_match and best_score > 0.5:
            return best_match

        return None

    def find_clients(self, search_name: str, limit: int = 5) -> List[Dict]:
        """Find multiple potential client matches."""
        clients = self.get_all_clients()
        scored = []

        for client in clients:
            score = SequenceMatcher(
                None,
                search_name.lower(),
                client["name"].lower()
            ).ratio()
            scored.append({**client, "score": score})

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

    def post_comment(self, todo_id: int, content: str) -> Dict:
        """
        Post a comment to a client's todo.

        Args:
            todo_id: The Basecamp todo ID
            content: HTML content for the comment

        Returns:
            API response with comment details
        """
        path = f"/buckets/{self.project_id}/recordings/{todo_id}/comments.json"
        return self._post(path, {"content": content})

    def get_client_comments(self, todo_id: int) -> List[Dict]:
        """Get all comments on a client's todo."""
        path = f"/buckets/{self.project_id}/recordings/{todo_id}/comments.json"
        return self._get(path)


def markdown_to_basecamp_html(markdown_text: str) -> str:
    """
    Convert markdown to Basecamp-compatible HTML.

    Basecamp supports: div, h1, br, strong, em, a, pre, ol, ul, li, blockquote
    """
    html = markdown_text

    # Convert headers (only h1 supported)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<strong>\1</strong>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<strong>\1</strong>', html, flags=re.MULTILINE)

    # Convert bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Convert bullet lists
    # Find consecutive lines starting with - and wrap in <ul>
    def replace_ul(match):
        items = match.group(0)
        items = re.sub(r'^- (.+)$', r'<li>\1</li>', items, flags=re.MULTILINE)
        return f'<ul>{items}</ul>'

    html = re.sub(r'(^- .+$\n?)+', replace_ul, html, flags=re.MULTILINE)

    # Convert numbered lists
    def replace_ol(match):
        items = match.group(0)
        items = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', items, flags=re.MULTILINE)
        return f'<ol>{items}</ol>'

    html = re.sub(r'(^\d+\. .+$\n?)+', replace_ol, html, flags=re.MULTILINE)

    # Convert line breaks (double newline = paragraph break, single = br)
    html = re.sub(r'\n\n', '<br><br>', html)
    html = re.sub(r'\n', '<br>', html)

    # Wrap in div
    return f'<div>{html}</div>'


if __name__ == "__main__":
    # Quick test
    client = BasecampClient()
    print("Config loaded successfully!")
    print(f"Account ID: {client.account_id}")
    print(f"Project ID: {client.project_id}")

    # Test finding a client
    result = client.find_client("Brad Twynham")
    if result:
        print(f"\nFound: {result['name']} (score: {result['score']:.2f})")
        print(f"Todo ID: {result['todo_id']}")
        print(f"Group: {result['group']}")
