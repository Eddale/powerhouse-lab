#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Production-ready implementation for AI agent use

This module provides robust YouTube transcript extraction with multiple fallback methods.
Optimized for use in AI agent workflows.

Usage:
    from youtube_transcript_extractor import extract_transcript

    result = extract_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if result['success']:
        print(result['transcript'])
    else:
        print(f"Error: {result['error']}")
"""

import re
import time
from typing import Dict, Optional, List


class TranscriptExtractor:
    """Main class for extracting YouTube transcripts"""

    def __init__(self, cache_enabled: bool = True):
        """
        Initialize the extractor

        Args:
            cache_enabled: Whether to cache transcripts (useful for repeated requests)
        """
        self.cache_enabled = cache_enabled
        self._cache = {}

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        """
        Extract YouTube video ID from URL or validate existing ID

        Args:
            url_or_id: YouTube URL or video ID

        Returns:
            str: 11-character YouTube video ID

        Examples:
            >>> TranscriptExtractor.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            'dQw4w9WgXcQ'
            >>> TranscriptExtractor.extract_video_id("dQw4w9WgXcQ")
            'dQw4w9WgXcQ'
        """
        video_id = url_or_id

        if 'youtube.com' in url_or_id or 'youtu.be' in url_or_id:
            patterns = [
                r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
                r'youtu\.be\/([0-9A-Za-z_-]{11})',
                r'embed\/([0-9A-Za-z_-]{11})',
                r'watch\?v=([0-9A-Za-z_-]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, url_or_id)
                if match:
                    video_id = match.group(1)
                    break

        # Validate video ID format
        if not re.match(r'^[0-9A-Za-z_-]{11}$', video_id):
            raise ValueError(f"Invalid YouTube video ID: {video_id}")

        return video_id

    @staticmethod
    def clean_transcript_text(text: str) -> str:
        """
        Clean and normalize transcript text

        Args:
            text: Raw transcript text

        Returns:
            str: Cleaned text suitable for AI processing
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove common transcript artifacts
        text = re.sub(r'\[.*?\]', '', text)  # [Music], [Applause], etc.
        text = re.sub(r'\(.*?\)', '', text)  # (inaudible), etc.

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")

        return text.strip()

    def _extract_with_youtube_transcript_api(
        self,
        video_id: str,
        languages: Optional[List[str]] = None
    ) -> Dict:
        """
        Extract transcript using youtube-transcript-api library

        Args:
            video_id: YouTube video ID
            languages: List of language codes to try (default: English variants)

        Returns:
            dict: Result with success status and transcript or error
        """
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            from youtube_transcript_api._errors import (
                TranscriptsDisabled,
                NoTranscriptFound,
                VideoUnavailable
            )
        except ImportError:
            return {
                'success': False,
                'error': 'youtube-transcript-api not installed. Install with: pip install youtube-transcript-api',
                'method': 'youtube-transcript-api'
            }

        if languages is None:
            languages = ['en', 'en-US', 'en-GB']

        try:
            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=languages
            )

            # Combine segments
            full_text = ' '.join([segment['text'] for segment in transcript_list])

            # Clean text
            full_text = self.clean_transcript_text(full_text)

            # Get metadata about available transcripts
            available_transcripts = []
            try:
                transcript_metadata = YouTubeTranscriptApi.list_transcripts(video_id)
                for t in transcript_metadata:
                    available_transcripts.append({
                        'language': t.language,
                        'language_code': t.language_code,
                        'is_generated': t.is_generated
                    })
            except:
                pass  # Metadata is nice to have but not critical

            return {
                'success': True,
                'transcript': full_text,
                'video_id': video_id,
                'method': 'youtube-transcript-api',
                'segment_count': len(transcript_list),
                'available_transcripts': available_transcripts,
                'char_count': len(full_text),
                'word_count': len(full_text.split())
            }

        except TranscriptsDisabled:
            return {
                'success': False,
                'error': 'Transcripts are disabled for this video',
                'video_id': video_id,
                'method': 'youtube-transcript-api'
            }
        except NoTranscriptFound:
            return {
                'success': False,
                'error': f'No transcript found in requested languages: {languages}',
                'video_id': video_id,
                'method': 'youtube-transcript-api'
            }
        except VideoUnavailable:
            return {
                'success': False,
                'error': 'Video is unavailable',
                'video_id': video_id,
                'method': 'youtube-transcript-api'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'video_id': video_id,
                'method': 'youtube-transcript-api'
            }

    def _extract_with_ytdlp(
        self,
        video_id: str,
        language: str = 'en'
    ) -> Dict:
        """
        Extract transcript using yt-dlp (fallback method)

        Args:
            video_id: YouTube video ID
            language: Language code for subtitles

        Returns:
            dict: Result with success status and transcript or error
        """
        try:
            import yt_dlp
        except ImportError:
            return {
                'success': False,
                'error': 'yt-dlp not installed. Install with: pip install yt-dlp',
                'method': 'yt-dlp'
            }

        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'skip_download': True,
                'writeautomaticsub': True,
                'writesubtitles': True,
                'subtitleslangs': [language],
                'subtitlesformat': 'vtt',
                'outtmpl': f'{tmpdir}/%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            try:
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)

                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)

                    # Find subtitle file
                    subtitle_file = f"{tmpdir}/{video_id}.{language}.vtt"

                    if not os.path.exists(subtitle_file):
                        return {
                            'success': False,
                            'error': 'No subtitles available for this video',
                            'video_id': video_id,
                            'method': 'yt-dlp'
                        }

                    # Read and parse VTT file
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Parse VTT to clean text
                    lines = content.split('\n')
                    text_lines = []

                    for line in lines:
                        # Skip timestamps, empty lines, and headers
                        if '-->' not in line and line.strip() and not line.startswith('WEBVTT'):
                            # Remove VTT formatting tags
                            clean_line = re.sub(r'<[^>]+>', '', line)
                            if clean_line.strip():
                                text_lines.append(clean_line.strip())

                    full_text = ' '.join(text_lines)
                    full_text = self.clean_transcript_text(full_text)

                    return {
                        'success': True,
                        'transcript': full_text,
                        'video_id': video_id,
                        'method': 'yt-dlp',
                        'title': title,
                        'duration': duration,
                        'char_count': len(full_text),
                        'word_count': len(full_text.split())
                    }

            except Exception as e:
                return {
                    'success': False,
                    'error': f'yt-dlp extraction failed: {str(e)}',
                    'video_id': video_id,
                    'method': 'yt-dlp'
                }

    def extract(
        self,
        url_or_id: str,
        languages: Optional[List[str]] = None,
        use_fallback: bool = True,
        rate_limit_delay: float = 0.0
    ) -> Dict:
        """
        Extract transcript with automatic fallback

        Args:
            url_or_id: YouTube URL or video ID
            languages: List of language codes to try (default: English)
            use_fallback: Whether to try yt-dlp if primary method fails
            rate_limit_delay: Seconds to wait before making request (for bulk operations)

        Returns:
            dict: Result containing transcript and metadata

        Example:
            >>> extractor = TranscriptExtractor()
            >>> result = extractor.extract("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            >>> if result['success']:
            ...     print(result['transcript'])
        """
        # Rate limiting
        if rate_limit_delay > 0:
            time.sleep(rate_limit_delay)

        # Extract video ID
        try:
            video_id = self.extract_video_id(url_or_id)
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }

        # Check cache
        if self.cache_enabled and video_id in self._cache:
            cached_result = self._cache[video_id].copy()
            cached_result['from_cache'] = True
            return cached_result

        # Try primary method: youtube-transcript-api
        result = self._extract_with_youtube_transcript_api(video_id, languages)

        # If failed and fallback enabled, try yt-dlp
        if not result['success'] and use_fallback:
            result = self._extract_with_ytdlp(video_id)

        # Cache successful results
        if self.cache_enabled and result['success']:
            self._cache[video_id] = result.copy()

        result['from_cache'] = False
        return result

    def bulk_extract(
        self,
        video_urls: List[str],
        rate_limit_delay: float = 1.0,
        progress_callback: Optional[callable] = None
    ) -> List[Dict]:
        """
        Extract transcripts from multiple videos

        Args:
            video_urls: List of YouTube URLs or video IDs
            rate_limit_delay: Delay between requests (default: 1 second)
            progress_callback: Optional callback function(current, total)

        Returns:
            list: List of result dictionaries

        Example:
            >>> extractor = TranscriptExtractor()
            >>> urls = ["video1_url", "video2_url", "video3_url"]
            >>> results = extractor.bulk_extract(urls, rate_limit_delay=2.0)
            >>> successful = [r for r in results if r['success']]
            >>> print(f"Extracted {len(successful)}/{len(urls)} transcripts")
        """
        results = []

        for i, url in enumerate(video_urls):
            if progress_callback:
                progress_callback(i + 1, len(video_urls))

            result = self.extract(url, rate_limit_delay=rate_limit_delay)
            results.append(result)

        return results

    def clear_cache(self):
        """Clear the transcript cache"""
        self._cache = {}


# Convenience function for simple use cases
def extract_transcript(url_or_id: str, languages: Optional[List[str]] = None) -> Dict:
    """
    Quick transcript extraction (uses default settings)

    Args:
        url_or_id: YouTube URL or video ID
        languages: Optional list of language codes

    Returns:
        dict: Result with transcript and metadata

    Example:
        >>> result = extract_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        >>> if result['success']:
        ...     print(result['transcript'])
    """
    extractor = TranscriptExtractor(cache_enabled=False)
    return extractor.extract(url_or_id, languages=languages)


# CLI interface
if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript_extractor.py <youtube_url_or_id>")
        print("\nExample:")
        print("  python youtube_transcript_extractor.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        print("  python youtube_transcript_extractor.py dQw4w9WgXcQ")
        sys.exit(1)

    url_or_id = sys.argv[1]

    # Extract transcript
    result = extract_transcript(url_or_id)

    if result['success']:
        print(f"✅ Success!")
        print(f"\nVideo ID: {result['video_id']}")
        print(f"Method: {result['method']}")
        print(f"Characters: {result['char_count']}")
        print(f"Words: {result['word_count']}")
        print(f"\nTranscript:\n{'-'*80}")
        print(result['transcript'])
        print('-'*80)

        # Also save to file
        output_file = f"{result['video_id']}_transcript.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['transcript'])
        print(f"\n💾 Saved to: {output_file}")

        # Save metadata as JSON
        metadata = {k: v for k, v in result.items() if k != 'transcript'}
        metadata_file = f"{result['video_id']}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"💾 Metadata saved to: {metadata_file}")

    else:
        print(f"❌ Failed to extract transcript")
        print(f"Error: {result['error']}")
        sys.exit(1)
