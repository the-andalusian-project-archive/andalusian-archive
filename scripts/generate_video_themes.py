#!/usr/bin/env python3
"""
Generate neutral theme descriptions for videos.
Avoids revealing specific arguments or triggering prejudices.
"""

import json
import pathlib
import re
import os

BASE = pathlib.Path(__file__).parent.parent  # andalusian-archive/
# Input lives at repo root (sibling of andalusian-archive/); output in _data/.
INPUT_JSON = BASE.parent / "archive_org_videos.json"
OUTPUT_JSON = BASE / "_data" / "videos.json"

# Theme mapping based on video titles
THEME_MAP = {
    "atheism": {
        "themes": ["Philosophical foundations of atheistic thought", "Epistemological frameworks for belief systems", "Historical context of secular philosophy"],
        "topics": ["philosophy", "atheism", "epistemology"],
        "tone": "academic lecture"
    },
    "islam": {
        "themes": ["Islamic theological principles", "Comparative religious studies", "Islamic intellectual tradition"],
        "topics": ["islam", "theology", "comparative religion"],
        "tone": "educational"
    },
    "debate": {
        "themes": ["Structured intellectual discourse", "Argumentation and critical analysis", "Cross-cultural philosophical dialogue"],
        "topics": ["debate", "philosophy", "critical thinking"],
        "tone": "dialogue"
    },
    "jihad": {
        "themes": ["Islamic jurisprudential concepts", "Historical analysis of Islamic law", "Contemporary interpretations of Islamic principles"],
        "topics": ["islamic law", "jurisprudence", "history"],
        "tone": "academic lecture"
    },
    "aisha": {
        "themes": ["Historical methodology in Islamic studies", "Biographical analysis of early Islamic figures", "Interdisciplinary approaches to historical questions"],
        "topics": ["history", "methodology", "biography"],
        "tone": "academic research"
    },
    "science": {
        "themes": ["Islamic contributions to scientific knowledge", "Historical development of scientific methodology", "Relationship between religion and science"],
        "topics": ["science", "history", "islamic civilization"],
        "tone": "educational"
    },
    "book": {
        "themes": ["Literary analysis and recommendations", "Intellectual resource curation", "Scholarly work discussions"],
        "topics": ["literature", "education", "resources"],
        "tone": "informal discussion"
    },
    "comment": {
        "themes": ["Community engagement and dialogue", "Response to intellectual inquiries", "Interactive discussion format"],
        "topics": ["community", "dialogue", "engagement"],
        "tone": "conversational"
    },
    "default": {
        "themes": ["Islamic studies discourse", "Intellectual exploration", "Contemporary issues analysis"],
        "topics": ["islamic studies", "intellectual discourse"],
        "tone": "educational"
    }
}

def get_theme_from_title(title):
    """Extract theme from video title."""
    title_lower = title.lower()
    
    # Check for specific themes
    for key in THEME_MAP:
        if key != "default" and key in title_lower:
            return THEME_MAP[key]
    
    # Check for series patterns
    if "session" in title_lower or "lecture" in title_lower:
        return THEME_MAP["default"]
    if "debate" in title_lower or "dialogue" in title_lower:
        return THEME_MAP["debate"]
    
    return THEME_MAP["default"]

def main():
    # Read video metadata
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    print(f"Processing {len(videos)} videos...")
    
    enriched_videos = []
    for video in videos:
        title = video.get('title', '') or video.get('name', '').replace('.mp4', '').replace('.webm', '')
        
        # Get theme based on title
        theme_data = get_theme_from_title(title)
        
        enriched_video = {
            "id": video.get('name', '').split('[')[-1].split(']')[0] if '[' in video.get('name', '') else "",
            "title": title,
            "archive_url": f"https://archive.org/download/andalusian-project/{video.get('name', '')}",
            "archive_org_id": "andalusian-project",
            "filename": video.get('name', ''),
            "size_bytes": video.get('size', 0),
            "duration": video.get('length', ''),
            "themes": theme_data["themes"],
            "topics": theme_data["topics"],
            "tone": theme_data["tone"],
            "format": video.get('format', ''),
            "preserved_in_repo": True
        }
        enriched_videos.append(enriched_video)
    
    # Save enriched videos
    output_path = OUTPUT_JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_videos, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(enriched_videos)} videos to {output_path}")

if __name__ == "__main__":
    main()
