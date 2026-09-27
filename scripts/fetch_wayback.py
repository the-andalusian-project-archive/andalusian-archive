#!/usr/bin/env python3
"""
Fetch blog posts from Wayback Machine CDX API.
Saves metadata and optionally downloads full content.
"""

import argparse
import json
import re
import requests
import time
import os
from datetime import datetime

# Configuration
CDX_API = "https://web.archive.org/cdx/search/cdx"
SITE_URL = "asadullahali.com"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '_data')

# Date-prefixed post path, e.g. /2014/05/12/some-post/ (replaces fragile '/20' substring).
DATE_PATH_RE = re.compile(r'/\d{4}/\d{2}/\d{2}/')
BLOG_SUBSTRINGS = ('/blog/', '/post/', '/article/')


def is_blog_like(url):
    lowered = url.lower()
    if any(path in lowered for path in BLOG_SUBSTRINGS):
        return True
    return bool(DATE_PATH_RE.search(url))

def fetch_cdx_records(url, match_type="domain", output="json", limit=100, offset=0):
    """Fetch one page of records from Wayback Machine CDX API."""
    params = {
        "url": url,
        "matchType": match_type,
        "output": output,
        "limit": limit,
        "offset": offset,
        "fl": "timestamp,original,statuscode,mimetype",
        "filter": "statuscode:200",
        "collapse": "urlkey"
    }

    response = requests.get(CDX_API, params=params)
    response.raise_for_status()
    return response.json()


def fetch_all_cdx_records(url, match_type="domain", limit=100):
    """Paginate through CDX API (limit/offset) until a short page or empty."""
    header = None
    data = []
    offset = 0
    while True:
        records = fetch_cdx_records(url, match_type=match_type, limit=limit,
                                    offset=offset)
        if not records:
            break
        if header is None:
            header = records[0]
            page = records[1:]
        elif records[0] == header:
            page = records[1:]
        else:
            page = records
        data.extend(page)
        if len(page) < limit:
            break
        offset += limit
    return header, data

def get_wayback_url(original_url, timestamp):
    """Generate Wayback Machine URL."""
    return f"https://web.archive.org/web/{timestamp}/{original_url}"

def main(limit=100):
    print(f"Fetching CDX records for {SITE_URL}...")

    try:
        header, data = fetch_all_cdx_records(SITE_URL, limit=limit)
        print(f"Found {len(data)} records")
        
        blog_posts = []
        for record in data:
            timestamp, original, status, mimetype = record
            
            # Filter for blog-like content
            if is_blog_like(original):
                post = {
                    "title": original.split('/')[-1].replace('-', ' ').title(),
                    "url": original,
                    "wayback_url": get_wayback_url(original, timestamp),
                    "timestamp": timestamp,
                    "status": status,
                    "mimetype": mimetype
                }
                blog_posts.append(post)
        
        print(f"Filtered to {len(blog_posts)} blog posts")
        
        # Save to JSON
        output_path = os.path.join(OUTPUT_DIR, 'blog_posts.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(blog_posts, f, indent=2, ensure_ascii=False)
        
        print(f"Saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch blog posts from Wayback CDX API")
    parser.add_argument("--limit", type=int, default=100,
                        help="Page size for CDX pagination (default: 100)")
    args = parser.parse_args()
    exit(main(limit=args.limit))
