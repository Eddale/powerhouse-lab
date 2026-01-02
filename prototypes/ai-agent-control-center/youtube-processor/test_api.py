"""
Quick test script for the YouTube Processor API
Run this to verify everything works before deploying
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = "http://localhost:8000"  # Change when deployed
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up


def test_health_check():
    """Test the health endpoint"""
    print("\n🏥 Testing health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200


def test_process_video(url=TEST_VIDEO_URL, summary_type="brief"):
    """Test video processing"""
    print(f"\n🎬 Testing video processing...")
    print(f"URL: {url}")
    print(f"Summary type: {summary_type}")

    payload = {
        "url": url,
        "summary_type": summary_type,
        "save_to_obsidian": False
    }

    response = requests.post(
        f"{API_URL}/process",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: {result['success']}")
        print(f"Video ID: {result['video_id']}")
        print(f"\n📝 Summary:\n{result['summary']}")
        print(f"\n📄 Markdown output length: {len(result['markdown_output'])} characters")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False


def test_invalid_url():
    """Test error handling with invalid URL"""
    print("\n🚫 Testing invalid URL handling...")

    payload = {
        "url": "https://not-a-youtube-url.com/video",
        "summary_type": "brief"
    }

    response = requests.post(
        f"{API_URL}/process",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_all_summary_types():
    """Test all three summary types"""
    types = ["brief", "detailed", "bullets"]

    for summary_type in types:
        print(f"\n{'='*60}")
        print(f"Testing summary type: {summary_type.upper()}")
        print(f"{'='*60}")

        success = test_process_video(
            url=TEST_VIDEO_URL,
            summary_type=summary_type
        )

        if not success:
            print(f"❌ Failed for summary type: {summary_type}")
            break


if __name__ == "__main__":
    print("🚀 YouTube Processor API Test Suite")
    print(f"Testing against: {API_URL}")
    print("\nMake sure the API is running: python main.py")

    # Check if API is accessible
    try:
        requests.get(f"{API_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API. Is it running?")
        print("Run: python main.py")
        exit(1)

    # Run tests
    health_ok = test_health_check()

    if not health_ok:
        print("\n❌ Health check failed. Check your ANTHROPIC_API_KEY")
        exit(1)

    # Test basic processing
    test_process_video(summary_type="brief")

    # Uncomment to test all summary types (will use more API credits)
    # test_all_summary_types()

    # Test error handling
    # test_invalid_url()

    print("\n✅ Basic tests completed!")
    print("\nNext steps:")
    print("1. Test with your own YouTube URLs")
    print("2. Deploy to Railway/Render")
    print("3. Update API_URL in this script to your deployed URL")
    print("4. Set up iOS Shortcut")
