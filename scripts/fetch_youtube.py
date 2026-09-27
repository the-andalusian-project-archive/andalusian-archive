#!/usr/bin/env python3
"""
Fetch YouTube video metadata using yt-dlp.
Extracts title, description, themes, and topics.
"""

import json
import subprocess
import os
import re
from datetime import datetime

# Configuration
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '_data')
CHANNEL_URL = "https://www.youtube.com/@TheAndalusianProject"

def extract_themes(description):
    """Extract theme keywords from video description."""
    themes = []
    
    # Common Islamic/philosophical themes
    theme_patterns = [
        r'islam', r'quran', r'atheism', r'philosophy', r'debate',
        r'christianity', r'apologetics', r'dawah', r'history',
        r'science', r'reason', r'faith', r'belief', r'god'
    ]
    
    for pattern in theme_patterns:
        if re.search(pattern, description, re.IGNORECASE):
            themes.append(pattern.title())
    
    return themes[:5]  # Limit to 5 themes

def fetch_video_metadata(video_id):
    """Fetch metadata for a single video."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching {video_id}: {e}")
    
    return None

def main():
    print(f"Fetching YouTube metadata for channel...")
    
    # First, get list of videos from channel
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-download",
        f"{CHANNEL_URL}/videos"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return 1
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    video_data = json.loads(line)
                    
                    # Extract themes from description
                    description = video_data.get('description', '')
                    themes = extract_themes(description)
                    
                    video = {
                        "id": video_data.get('id'),
                        "title": video_data.get('title'),
                        "description": description[:500],
                        "themes": themes,
                        "topics": video_data.get('tags', [])[:10],
                        "duration": video_data.get('duration'),
                        "upload_date": video_data.get('upload_date'),
                        "view_count": video_data.get('view_count'),
                        "url": f"https://www.youtube.com/watch?v={video_data.get('id')}"
                    }
                    videos.append(video)
                    
                except json.JSONDecodeError:
                    continue
        
        print(f"Found {len(videos)} videos")
        
        # Save to JSON
        output_path = os.path.join(OUTPUT_DIR, 'videos.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        
        print(f"Saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
