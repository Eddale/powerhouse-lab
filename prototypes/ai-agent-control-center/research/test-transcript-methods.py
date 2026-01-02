#!/usr/bin/env python3
"""
Test YouTube Transcript Extraction Methods
Validates the approaches documented in youtube-transcript-extraction.md
"""

import re
import sys


def extract_video_id(url_or_id):
    """Extract YouTube video ID from URL or return ID if already extracted"""
    video_id = url_or_id

    if 'youtube.com' in url_or_id or 'youtu.be' in url_or_id:
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                video_id = match.group(1)
                break

    return video_id


# =============================================================================
# METHOD 1: youtube-transcript-api
# =============================================================================

def test_youtube_transcript_api(video_url):
    """Test extraction using youtube-transcript-api"""
    print("\n" + "="*80)
    print("METHOD 1: youtube-transcript-api")
    print("="*80)

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    except ImportError:
        print("❌ youtube-transcript-api not installed")
        print("   Install with: pip install youtube-transcript-api")
        return None

    video_id = extract_video_id(video_url)
    print(f"\nVideo ID: {video_id}")

    try:
        # Get transcript
        print("\n📥 Fetching transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en', 'en-US', 'en-GB']
        )

        print(f"✅ Success! Retrieved {len(transcript)} segments")

        # Show first 3 segments
        print("\nFirst 3 segments (with timestamps):")
        for i, segment in enumerate(transcript[:3]):
            print(f"  [{segment['start']:.2f}s - {segment['start'] + segment['duration']:.2f}s]")
            print(f"  {segment['text']}")

        # Combine full text
        full_text = ' '.join([seg['text'] for seg in transcript])
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        print(f"\nFull transcript length: {len(full_text)} characters")
        print(f"First 200 chars: {full_text[:200]}...")

        # List available transcripts
        print("\n📋 Available transcripts for this video:")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for t in transcript_list:
            auto_flag = " (auto-generated)" if t.is_generated else " (manual)"
            print(f"  - {t.language} ({t.language_code}){auto_flag}")

        return {
            'success': True,
            'method': 'youtube-transcript-api',
            'transcript': full_text,
            'segment_count': len(transcript)
        }

    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video")
        return {'success': False, 'error': 'Transcripts disabled'}
    except NoTranscriptFound:
        print("❌ No English transcript found")
        return {'success': False, 'error': 'No transcript found'}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'success': False, 'error': str(e)}


# =============================================================================
# METHOD 2: yt-dlp
# =============================================================================

def test_ytdlp(video_url):
    """Test extraction using yt-dlp"""
    print("\n" + "="*80)
    print("METHOD 2: yt-dlp")
    print("="*80)

    try:
        import yt_dlp
    except ImportError:
        print("❌ yt-dlp not installed")
        print("   Install with: pip install yt-dlp")
        return None

    video_id = extract_video_id(video_url)
    print(f"\nVideo ID: {video_id}")

    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'writesubtitles': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'outtmpl': f'{tmpdir}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            print("\n📥 Extracting metadata and subtitles...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)

                video_id = info['id']
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)

                print(f"✅ Video: {title}")
                print(f"   Duration: {duration}s")

                # Find subtitle file
                subtitle_file = f"{tmpdir}/{video_id}.en.vtt"

                if os.path.exists(subtitle_file):
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Parse VTT to clean text
                    lines = content.split('\n')
                    text_lines = []
                    for line in lines:
                        if '-->' not in line and line.strip() and not line.startswith('WEBVTT'):
                            clean_line = re.sub(r'<[^>]+>', '', line)
                            if clean_line.strip():
                                text_lines.append(clean_line.strip())

                    full_text = ' '.join(text_lines)
                    full_text = re.sub(r'\s+', ' ', full_text).strip()

                    print(f"\n✅ Subtitle extracted successfully")
                    print(f"   Length: {len(full_text)} characters")
                    print(f"   First 200 chars: {full_text[:200]}...")

                    return {
                        'success': True,
                        'method': 'yt-dlp',
                        'transcript': full_text,
                        'title': title
                    }
                else:
                    print("❌ No subtitle file found")
                    return {'success': False, 'error': 'No subtitles available'}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {'success': False, 'error': str(e)}


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def main():
    print("YouTube Transcript Extraction - Method Testing")
    print("="*80)

    # Test video - Rick Astley "Never Gonna Give You Up" (known to have transcripts)
    test_videos = [
        {
            'name': 'Rick Astley - Never Gonna Give You Up',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        },
        {
            'name': 'Short educational video',
            'url': 'https://www.youtube.com/watch?v=8pTEmbeENF4'
        }
    ]

    # Allow custom URL from command line
    if len(sys.argv) > 1:
        test_videos = [{'name': 'Custom video', 'url': sys.argv[1]}]

    for video in test_videos:
        print(f"\n\n{'#'*80}")
        print(f"Testing: {video['name']}")
        print(f"URL: {video['url']}")
        print(f"{'#'*80}")

        results = []

        # Test Method 1: youtube-transcript-api
        result1 = test_youtube_transcript_api(video['url'])
        if result1:
            results.append(result1)

        # Test Method 2: yt-dlp
        result2 = test_ytdlp(video['url'])
        if result2:
            results.append(result2)

        # Compare results
        if len(results) > 1:
            print("\n" + "="*80)
            print("COMPARISON")
            print("="*80)

            successful = [r for r in results if r.get('success')]

            if len(successful) > 1:
                print(f"\n✅ {len(successful)} methods succeeded")

                # Compare transcript lengths
                print("\nTranscript lengths:")
                for r in successful:
                    print(f"  {r['method']}: {len(r['transcript'])} characters")

                # Check if transcripts match (roughly)
                if len(successful) == 2:
                    t1 = successful[0]['transcript'][:500]
                    t2 = successful[1]['transcript'][:500]
                    similarity = len(set(t1.split()) & set(t2.split())) / len(set(t1.split() + t2.split()))
                    print(f"\nFirst 500 chars similarity: {similarity*100:.1f}%")

            else:
                print(f"\n⚠️  Only {len(successful)} method succeeded")

        print("\n")


if __name__ == '__main__':
    main()
