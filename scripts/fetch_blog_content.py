#!/usr/bin/env python3
"""
Fetch blog post content from Wayback Machine and create local markdown files.
Reads blog_posts.json, fetches HTML from wayback URLs, extracts content,
and saves markdown files with front matter in _posts/ directory.

Supports --retry-failed flag to re-attempt only failed/skipped entries.
"""

import json
import os
import pathlib
import re
import sys
import time
import traceback
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "_data")
POSTS_DIR = os.path.join(BASE_DIR, "_posts")
BLOG_POSTS_JSON = os.path.join(DATA_DIR, "blog_posts.json")

# Ensure output directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "AndalusianProjectArchive/1.0 (Academic research archive; polite bot)"
}

MAX_RETRIES = 3
RETRY_BACKOFF = [5, 15, 30]  # seconds between retries
REQUEST_DELAY = 1.5  # seconds between different URLs


def slug_to_title(url):
    """Extract a readable title from the URL slug."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    # Monthly archive pages: /2014/05 -> "May 2014 Archive"
    monthly = re.match(r"^/(\d{4})/(\d{2})/?$", path)
    if monthly:
        year, month = monthly.group(1), monthly.group(2)
        try:
            dt = datetime(int(year), int(month), 1)
            return dt.strftime("%B %Y") + " Archive"
        except ValueError:
            return f"{year}-{month} Archive"

    # Get the slug (last non-empty segment)
    segments = [s for s in path.split("/") if s]
    if not segments:
        return "Unknown Post"

    slug = segments[-1]

    # Clean up the slug
    slug = re.sub(r"\?.*$", "", slug)
    slug = slug.replace("-", " ").replace("_", " ")

    # Title-case it
    title = " ".join(word.capitalize() for word in slug.split())

    # Fix common small words (lowercase except first word)
    small_words = {"A", "An", "The", "And", "But", "Or", "For", "Nor", "On", "At",
                   "To", "In", "Of", "Vs", "Via", "Part"}
    words = title.split()
    if words:
        for i in range(1, len(words)):
            if words[i] in small_words:
                words[i] = words[i].lower()
        title = " ".join(words)

    return title


def classify_url(url):
    """Classify a URL entry type."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    query = parsed.query

    if re.match(r"^/\d{4}/\d{2}/?$", path):
        return "monthly_archive"
    if "/feed" in path.lower():
        return "feed"
    if "/amp/" in path.lower() or path.lower().endswith("/amp"):
        return "amp"
    if query and any(x in query.lower() for x in ["replytocom", "shared", "relatedposts"]):
        return "query_variant"
    if re.match(r"^/(\d{4})/(\d{2})/(\d{2})/[\w-]+/?$", path):
        return "actual_post"
    return "other"


def get_canonical_url(url):
    """Get the canonical base URL (strip query params, /feed, /amp)."""
    base = re.sub(r"\?.*$", "", url)
    base = re.sub(r"/feed/?$", "", base)
    base = re.sub(r"/amp/?$", "", base)
    return base.rstrip("/")


def make_filename(title, url):
    """Create a Jekyll-compatible filename from title and date."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    segments = [s for s in path.split("/") if s]

    # Extract date from URL
    date_match = re.match(r"(\d{4})/(\d{2})/(\d{2})", "/".join(segments))
    if date_match:
        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Create a safe slug from the title
    safe_slug = re.sub(r"[^\w\s-]", "", title.lower())
    safe_slug = re.sub(r"[\s]+", "-", safe_slug.strip())
    safe_slug = re.sub(r"-+", "-", safe_slug)

    return f"{date_str}-{safe_slug}.md"


def html_to_markdown(element):
    """Convert a BeautifulSoup element to simple markdown text."""
    if element is None:
        return ""

    lines = []
    for child in element.children:
        if hasattr(child, "name"):
            if child.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                level = int(child.name[1])
                text = child.get_text(strip=True)
                if text:
                    lines.append(f"\n{'#' * level} {text}\n")
            elif child.name == "p":
                text = child.get_text(strip=True)
                if text:
                    lines.append(f"\n{text}\n")
            elif child.name == "blockquote":
                text = child.get_text(strip=True)
                if text:
                    quoted = "\n".join(f"> {line}" for line in text.split("\n") if line.strip())
                    lines.append(f"\n{quoted}\n")
            elif child.name in ("ul", "ol"):
                for li in child.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        lines.append(f"- {text}")
            elif child.name == "pre":
                code = child.get_text()
                lines.append(f"\n```\n{code}\n```\n")
            elif child.name == "div":
                lines.append(html_to_markdown(child))
            elif child.name == "hr":
                lines.append("\n---\n")
            elif child.name == "img":
                src = child.get("src", "")
                alt = child.get("alt", "")
                if src:
                    lines.append(f"\n![{alt}]({src})\n")
            else:
                text = child.get_text(strip=True)
                if text:
                    lines.append(f"\n{text}\n")
        else:
            text = str(child).strip()
            if text:
                lines.append(text)

    return "\n".join(lines)


def fetch_wayback_page(wayback_url, timeout=30):
    """Single-fetch variant returning (title, date, content_md, error, soup).

    Same parsing as fetch_wayback_content plus Wayback-chrome stripping;
    soup returned for category/tag/comment harvesting (None on failure).
    """
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(wayback_url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                print(f"    Retry {attempt + 1}/{MAX_RETRIES} after {wait}s: {type(e).__name__}")
                time.sleep(wait)
    else:
        return None, None, None, str(last_error), None

    soup = BeautifulSoup(resp.text, "html.parser")
    soup = strip_wayback_chrome(soup)

    # Check for "Private Site" placeholder
    page_text = soup.get_text(strip=True)
    if "Private Site" in page_text and len(page_text) < 200:
        return None, None, None, "Private Site (content unavailable)", None

    # Extract title from h1.entry-title, h2.entry-title, or <title>
    title = None
    for selector in ["h1.entry-title", "h2.entry-title", "h1.post-title",
                      "h2.post-title", "h1.headline", "h1.post-title",
                      ".postarea h1", ".article h1", "article h1",
                      "article h2"]:
        el = soup.select_one(selector)
        if el:
            t = el.get_text(strip=True)
            if t and len(t) > 2 and "Andalusian Project" not in t:
                title = t
                break
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            raw = title_tag.get_text(strip=True)
            # Remove " | The Andalusian Project" suffix
            title = re.sub(r"\s*\|\s*The Andalusian Project.*$", "", raw).strip()
            title = re.sub(r"\s*[:\-|]\s*.*$", "", raw).strip()

    # Extract date
    date = None
    for selector in [".entry-date", ".post-date", "time", ".published"]:
        el = soup.select_one(selector)
        if el:
            date_text = el.get_text(strip=True)
            for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%B %d, %Y", "%b %d, %Y",
                        "%d %B %Y", "%d %b %Y", "%m/%d/%Y"]:
                try:
                    dt = datetime.strptime(date_text, fmt)
                    date = dt.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
            if date:
                break
    if not date:
        time_el = soup.select_one("time[datetime]")
        if time_el:
            date = time_el["datetime"][:10]

    # Extract content
    content_element = None
    for selector in [".entry-content", ".post-content", ".article-content",
                      ".postarea", ".article", ".single-holder", ".hentry",
                      "main", ".content-area", "article .content", "article"]:
        el = soup.select_one(selector)
        if el and len(el.get_text(strip=True)) > 500:
            content_element = el
            break
    if content_element is None:
        for selector in [".entry-content", ".post-content",
                          ".article-content", ".postarea", ".article",
                          "article"]:
            el = soup.select_one(selector)
            if el:
                content_element = el
                break

    content_md = ""
    if content_element:
        # Remove navigation, share buttons, related posts, comments,
        # plus ad/JS junk subtrees (Task R hardened selectors).
        clean_content_element(content_element)

        content_md = html_to_markdown(content_element).strip()
        content_md = scrub_ad_junk_lines(content_md)
        content_md = re.sub(r"\n{3,}", "\n\n", content_md)

    return title, date, content_md, None, soup


def fetch_wayback_content(wayback_url, timeout=30):
    """Fetch and parse content from a Wayback Machine URL with retries."""
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(wayback_url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                print(f"    Retry {attempt + 1}/{MAX_RETRIES} after {wait}s: {type(e).__name__}")
                time.sleep(wait)
    else:
        return None, None, None, str(last_error)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Check for "Private Site" placeholder
    page_text = soup.get_text(strip=True)
    if "Private Site" in page_text and len(page_text) < 200:
        return None, None, None, "Private Site (content unavailable)"

    # Extract title from h1.entry-title, h2.entry-title, or <title>
    title = None
    for selector in ["h1.entry-title", "h2.entry-title", "h1.post-title",
                      "h2.post-title", "article h1", "article h2"]:
        el = soup.select_one(selector)
        if el:
            t = el.get_text(strip=True)
            if t and len(t) > 2:
                title = t
                break
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            raw = title_tag.get_text(strip=True)
            # Remove " | The Andalusian Project" suffix
            title = re.sub(r"\s*\|\s*The Andalusian Project.*$", "", raw).strip()
            title = re.sub(r"\s*[:\-|]\s*.*$", "", raw).strip()

    # Extract date
    date = None
    for selector in [".entry-date", ".post-date", "time", ".published"]:
        el = soup.select_one(selector)
        if el:
            date_text = el.get_text(strip=True)
            for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%B %d, %Y", "%b %d, %Y",
                        "%d %B %Y", "%d %b %Y", "%m/%d/%Y"]:
                try:
                    dt = datetime.strptime(date_text, fmt)
                    date = dt.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
            if date:
                break
    if not date:
        time_el = soup.select_one("time[datetime]")
        if time_el:
            date = time_el["datetime"][:10]

    # Extract content
    content_element = None
    for selector in [".entry-content", ".post-content", ".article-content",
                      "article .content", "article"]:
        el = soup.select_one(selector)
        if el:
            content_element = el
            break

    content_md = ""
    if content_element:
        # Remove navigation, share buttons, related posts, comments,
        # plus ad/JS junk subtrees (Task R hardened selectors).
        clean_content_element(content_element)

        content_md = html_to_markdown(content_element).strip()
        content_md = scrub_ad_junk_lines(content_md)
        content_md = re.sub(r"\n{3,}", "\n\n", content_md)

    return title, date, content_md, None


def extract_date_from_url(url):
    """Extract date from a URL path."""
    parsed = urlparse(url)
    date_match = re.match(r"/(\d{4})/(\d{2})/(\d{2})", parsed.path)
    if date_match:
        return f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    monthly = re.match(r"/(\d{4})/(\d{2})", parsed.path)
    if monthly:
        return f"{monthly.group(1)}-{monthly.group(2)}-01"
    return None


def main():
    retry_failed_only = "--retry-failed" in sys.argv

    print("=" * 70)
    print("Andalusian Project Archive - Blog Content Fetcher")
    if retry_failed_only:
        print("MODE: Retrying only failed/skipped entries")
    print("=" * 70)

    # Load blog posts
    with open(BLOG_POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"\nLoaded {len(posts)} entries from blog_posts.json")

    # Classify all entries
    classified = {}
    for i, post in enumerate(posts):
        url = post["url"]
        ctype = classify_url(url)
        classified.setdefault(ctype, []).append(i)
        post["title"] = slug_to_title(url)
        post["url_type"] = ctype

    print("\nURL Classification:")
    for ctype, indices in sorted(classified.items()):
        print(f"  {ctype}: {len(indices)} entries")

    # Find unique actual blog posts to fetch
    seen_canonical = set()
    unique_posts = []  # List of (json_index, post_dict)

    for i, post in enumerate(posts):
        if post.get("url_type") not in ("actual_post", "query_variant", "feed"):
            continue
        canonical = get_canonical_url(post["url"])
        if canonical not in seen_canonical:
            seen_canonical.add(canonical)
            unique_posts.append((i, post))

    print(f"\nUnique posts to fetch: {len(unique_posts)}")

    # Filter for retry mode
    if retry_failed_only:
        to_fetch = []
        for idx, (json_idx, post) in enumerate(unique_posts):
            status = post.get("fetch_status", "")
            if not post.get("content_file") or status.startswith("failed") or status == "skipped_no_content":
                to_fetch.append((idx, json_idx, post))
        print(f"Entries needing retry: {len(to_fetch)}")
    else:
        to_fetch = [(idx, json_idx, post) for idx, (json_idx, post) in enumerate(unique_posts)]

    # Track results
    results = {"success": 0, "failed": 0, "skipped": 0}
    success_files = []

    # Fetch content
    for fetch_num, (orig_idx, json_idx, post) in enumerate(to_fetch):
        url = post["url"]
        wayback_url = post.get("wayback_url", "")
        title = post.get("title", slug_to_title(url))
        date_from_url = extract_date_from_url(url)

        label = f"[{fetch_num + 1}/{len(to_fetch)}]"
        print(f"\n{label} Fetching: {url}")
        print(f"  Title (from slug): {title}")

        if not wayback_url:
            print("  SKIPPED: No wayback URL available")
            results["skipped"] += 1
            post["content_file"] = None
            post["fetch_status"] = "skipped_no_wayback_url"
            continue

        fetched_title, fetched_date, content, error = fetch_wayback_content(wayback_url)

        if error:
            print(f"  FAILED: {error}")
            results["failed"] += 1
            post["content_file"] = None
            post["fetch_status"] = f"failed: {error}"
            continue

        # Use fetched title if available
        if fetched_title and len(fetched_title.strip()) > 2:
            post["title"] = fetched_title
            title = fetched_title
            print(f"  Title (from HTML): {title}")

        final_date = fetched_date or date_from_url or "unknown"
        post["date"] = final_date

        if not content or len(content.strip()) < 20:
            print(f"  WARNING: Very short or no content ({len(content or '')} chars)")
            results["skipped"] += 1
            post["content_file"] = None
            post["fetch_status"] = "skipped_no_content"
            continue

        # Create markdown filename
        md_filename = make_filename(title, url)
        md_path = os.path.join(POSTS_DIR, md_filename)

        # Create front matter and content
        safe_title = title.replace('"', "'")
        front_matter = f"""---
title: "{safe_title}"
date: {final_date}
original_url: "{url}"
wayback_url: "{wayback_url}"
author: "Asadullah Ali Al-Andalusi"
source: "The Andalusian Project Archive"
---

"""
        with open(md_path, "w", encoding="utf-8") as f:
            _assert_fetch_is_clean(content, work.get("slug", slug_to_title(url)),
                                   md_path)
            f.write(front_matter + content)

        rel_path = f"_posts/{md_filename}"
        post["content_file"] = rel_path
        post["fetch_status"] = "success"
        success_files.append(md_filename)
        results["success"] += 1
        print(f"  SAVED: {rel_path} ({len(content)} chars)")

        time.sleep(REQUEST_DELAY)

    # Update all posts that point to the same canonical URL
    print("\n" + "=" * 70)
    print("Updating all entries with content_file references...")

    canonical_to_content = {}
    for post in posts:
        cf = post.get("content_file")
        if cf:
            canonical = get_canonical_url(post["url"])
            canonical_to_content[canonical] = cf

    updated_count = 0
    for post in posts:
        if not post.get("content_file"):
            canonical = get_canonical_url(post["url"])
            if canonical in canonical_to_content:
                post["content_file"] = canonical_to_content[canonical]
                post["fetch_status"] = "alias_of_canonical"
                updated_count += 1

    print(f"  Updated {updated_count} duplicate entries")

    # Save updated blog_posts.json
    with open(BLOG_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated blog_posts.json saved.")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total entries in JSON:       {len(posts)}")
    print(f"  Unique posts to fetch:       {len(unique_posts)}")
    print(f"  Successfully fetched:        {results['success']}")
    print(f"  Failed:                      {results['failed']}")
    print(f"  Skipped (no content/URL):    {results['skipped']}")
    print(f"  Alias entries updated:       {updated_count}")

    with_title = sum(1 for p in posts if p.get("title") and p["title"].strip())
    with_content = sum(1 for p in posts if p.get("content_file"))
    print(f"\n  Entries with titles:         {with_title}/{len(posts)}")
    print(f"  Entries with content_file:   {with_content}/{len(posts)}")

    # List markdown files
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    print(f"\n  Markdown files in _posts/: {len(md_files)}")
    for f_name in sorted(md_files):
        size = os.path.getsize(os.path.join(POSTS_DIR, f_name))
        print(f"    - {f_name} ({size:,} bytes)")

    # List entries without content
    no_content = [p for p in posts if not p.get("content_file")]
    if no_content:
        print(f"\n  Entries WITHOUT content_file ({len(no_content)}):")
        for p in no_content:
            print(f"    - {p.get('title', 'N/A')}: {p['url'][:80]}...")

    print("\nDone!")
    return 0 if results["failed"] == 0 else 1


# ---------------------------------------------------------------------------
# Canonical mode: fetch the 57-list works (wayback_only + thin found) with
# quality gates. Trigger: `python scripts/fetch_blog_content.py --canonical
# [--only slug1,slug2]`. Serial, polite, checkpointed via recovery_log.json.
# ---------------------------------------------------------------------------

CANON_JSON = os.path.join(DATA_DIR, "canonical_works.json")
RECOVERY_LOG = os.path.join(DATA_DIR, "recovery_log.json")

FULL_MIN_WORDS = 200    # >=200 -> full _posts file
REVIEW_MIN_WORDS = 100  # 100-199 -> file + needs-review flag

WAYBACK_CHROME_SELECTORS = (
    "#wm-ipp, #wm-ipp-base, #wm-ipp-print, #donato, "
    "[id^='wm-'], .wayback-toolbar"
)


def strip_wayback_chrome(soup):
    """Remove Wayback toolbar/chrome injected into archived pages."""
    for el in soup.select(WAYBACK_CHROME_SELECTORS):
        el.decompose()
    for comment in soup.find_all(string=lambda s: isinstance(s, str) and "wm-ipp" in s):
        pass  # text-node markers carry no visible text; ignore
    return soup


# ---------------------------------------------------------------------------
# Task R (2026-09-11): hardened ad/JS junk stripping for the article track.
# Drops script/style/noscript wholesale inside content elements, removes
# WordPress.com / Criteo / ATA ad containers, and scrubs residual JS text
# lines (__ATA.initAd, wpcom_adclk_*, jQuery(, beacons) that older fetches
# stringified into _posts bodies. Polite UA + retries + serial fetching
# elsewhere in this file are unchanged.
# ---------------------------------------------------------------------------

AD_JUNK_SELECTORS = (
    "script, style, noscript, "
    ".wpa, .wpcom-ad, .wpcom_below_post, "
    "[id^='crt-'], [id*='criteo' i], [class*='criteo' i], .criteo, "
    "ins.adsbygoogle, .adsbygoogle"
)

LEGACY_UNWANTED_SELECTORS = (
    ".sharedaddy, .jp-relatedposts, .comment-respond, .comments-area, "
    ".site-navigation, .post-navigation, .social-sharing, .share, nav, "
    ".yarpp-related, .entry-meta, .post-navigation"
)

# Residual JS/ad text lines (converter damage from pre-Task-R fetches that
# stringified <script> bodies into markdown). A line is dropped only when it
# matches one of these identifier patterns; plain prose is never matched.
AD_JUNK_LINE_RES = (
    re.compile(r"__ATA\.initAd"),
    re.compile(r"__ATA\.cmd\.push"),
    re.compile(r"__ATA\."),
    re.compile(r"atatags"),
    re.compile(r"initVideoSlot|initSlot"),
    re.compile(r"wpcom_"),
    re.compile(r"GA_google"),
    re.compile(r"googleAddAdSense"),
    re.compile(r"googleFillSlot"),
    re.compile(r"jQuery\("),
    re.compile(r"[Cc]riteo"),
    re.compile(r"getElementById\(\s*['\"]crt-"),
    re.compile(r"new Image\(\)"),
    re.compile(r"stat_gif|pixel\.wp\.com"),
    re.compile(r"GS_googleAddAdSenseService|googleAddAdSenseService"),
    re.compile(r"virool\.com|shareth\.ru|boomvideo"),
    re.compile(r"<(script|style|noscript)[\s>]"),
)

# Exact-line WordPress.com ad labels (ad chrome, never author prose).
AD_JUNK_EXACT_LINES = frozenset({"about these ads", "advertisements"})


def clean_content_element(content_element):
    """Strip ad/JS/chrome subtrees from an extracted content element."""
    if content_element is None:
        return None
    for unwanted in content_element.select(
        LEGACY_UNWANTED_SELECTORS + ", " + AD_JUNK_SELECTORS
    ):
        unwanted.decompose()
    return content_element


def scrub_ad_junk_lines(content_md):
    """Drop residual ad/JS text lines from converted markdown (Task R).

    Converter damage only: lines matching AD_JUNK_LINE_RES or exactly equal
    (case-insensitive, stripped) to a member of AD_JUNK_EXACT_LINES. All
    other lines — including every author sentence — pass through untouched.
    """
    if not content_md:
        return content_md
    kept = []
    for line in content_md.split("\n"):
        stripped = line.strip()
        if not stripped:
            kept.append(line)
            continue
        if stripped.lower() in AD_JUNK_EXACT_LINES:
            continue
        if any(rx.search(line) for rx in AD_JUNK_LINE_RES):
            continue
        kept.append(line)
    return "\n".join(kept)


def extract_cats_tags(soup):
    """Harvest WordPress categories/tags from entry footer/meta areas."""
    cats, tags = [], []
    for area in soup.select(
        ".entry-meta, .entry-utility, .post-meta, footer.entry-footer, "
        ".entry-footer, .post-footer"
    ):
        for a in area.find_all("a", href=True):
            href = a["href"].lower()
            text = a.get_text(strip=True)
            if not text or len(text) > 60:
                continue
            if "/category/" in href and text not in cats:
                cats.append(text)
            elif "/tag/" in href and text not in tags:
                tags.append(text)
    return cats, tags


def count_comments(soup):
    """Count reader comments (bodies stripped as noise; count kept)."""
    box = soup.select_one(".comments-area, #comments, .comment-list")
    if not box:
        return 0
    return len(box.select("li.comment, .comment-body, li[class*='comment']"))


def original_from_wayback(wayback_url):
    """Derive the original URL from a Wayback snapshot URL."""
    m = re.sub(r"^https?://web\.archive\.org/web/\d+/", "", wayback_url or "")
    if m and not m.startswith("http"):
        m = "http://" + m
    return m.rstrip("/")


# ---------------------------------------------------------------------------
# Task R (2026-09-11): keep-better guardrail + all-37 refetch support.
# Binding rule: a fresh fetch replaces the on-disk file ONLY when
#   (a) new body words >= 90% of old body words, AND
#   (b) the fetched title matches the on-disk title (normalized).
# Otherwise the old file is left byte-identical and the recovery_log row
# records verdict `kept_existing_snapshot_drift`. Zero silent replacements.
# Grammar repair stays converter-damage-only (entity/whitespace cleanup in
# the fetch path); author sentences are never rewritten.
# ---------------------------------------------------------------------------

GUARDRAIL_MIN_RATIO = 0.90


def normalize_title_for_match(title):
    """Normalize a title for keep/replace comparison (decision only).

    Unifies case, NBSP/whitespace, curly quotes and dash variants. Used
    only for the guardrail decision; stored titles are never rewritten
    with the normalized form.
    """
    t = (title or "").replace(" ", " ")
    t = t.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    t = t.replace("—", "-").replace("–", "-").replace("‐", "-")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def read_post_file(path):
    """Read an existing _posts file -> (front_matter, body, title, words)."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    if text.count("---") >= 2:
        _, fm, body = text.split("---", 2)
    else:
        fm, body = "", text
    title = None
    m = re.search(r'^title:\s*"(.*)"\s*$', fm, re.M)
    if m:
        title = m.group(1)
    return fm, body, title, len(body.split())


def split_front_matter(text):
    """Split raw post text -> (fm_block_incl_dashes, body)."""
    if text.count("---") >= 2:
        _, fm, body = text.split("---", 2)
        return "---" + fm + "---", body
    return "", text


_EXISTING_POST_CACHE = None


def _existing_posts_index():
    """Map normalized original/canonical URLs and names to _posts files."""
    global _EXISTING_POST_CACHE
    if _EXISTING_POST_CACHE is not None:
        return _EXISTING_POST_CACHE
    index = {"wayback": {}, "original": {}, "name": {}}
    for p in sorted(pathlib.Path(POSTS_DIR).glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _body = split_front_matter(text) if text.count("---") >= 2 else ("", text)
        index["name"][p.name] = str(p)
        for key in ("wayback_url", "original_url"):
            m = re.search(r'^' + key + r':\s*"(.*)"\s*$', fm, re.M)
            if m:
                url = m.group(1).strip()
                index["wayback" if key == "wayback_url" else "original"][url] = str(p)
                norm = re.sub(r":80(?=/)", "",
                              original_from_wayback(url) if key == "wayback_url"
                              else url).lower().rstrip("/")
                index["original"].setdefault(norm, str(p))
    _EXISTING_POST_CACHE = index
    return index


def resolve_existing_post(work):
    """Resolve a canonical work to its frozen on-disk _posts file (if any).

    Never synthesizes a filename: returns an existing path or None.
    """
    index = _existing_posts_index()
    canon_slug = re.sub(r"[^a-z0-9]+", "-", work["slug"].lower()).strip("-")
    canon_name = "%s-%s.md" % (work["date"], canon_slug)
    if canon_name in index["name"]:
        return index["name"][canon_name]
    wb = work.get("wayback_url") or ""
    if wb and wb in index["wayback"]:
        return index["wayback"][wb]
    if wb:
        norm = re.sub(r":80(?=/)", "",
                      original_from_wayback(wb)).lower().rstrip("/")
        if norm in index["original"]:
            return index["original"][norm]
    return None


def _assert_fetch_is_clean(content_md, slug, path):
    """Refuse to write a fetch the damage detector would flag.

    THE ROOT CAUSE, NOT THE SYMPTOM. `clean_content_element` and
    `scrub_ad_junk_lines` above were hardened in Task R (2026-09-11) and they
    stop most injected markup at the source. But they are a FIXED list, written
    once, while `fetch_damage.py` has kept learning: the 2026-09-27 triage pass
    added rules for config runs, JS block openers, comment threads and taxonomy
    blocks, and the repair pass then removed damage those rules found. The
    fetcher never learned them.

    So the two files disagree by construction, and the gap is silent in the
    dangerous direction: a fresh fetch can write residue the repair pass would
    have caught, and nothing fails until a human notices it in a published page.
    That is the whole failure this repository cannot afford — publishing
    machine junk as the author's words — and it is why the 287-hit triage, the
    repair, and two rounds of review existed at all.

    The fix is not to copy the rules here. Any list duplicated into the fetcher
    goes stale the moment `fetch_damage.py` learns something new, which is
    exactly how the current gap opened. Instead the fetcher asks the detector
    directly, so a new rule is enforced in the fetch path the day it is written
    and there is no second copy to forget.

    `judgement=False` deliberately. Judgement rules fire on things the author
    may have written on purpose - curly quotes, em dashes, a category spelled
    with a capital - and blocking a fetch on those would reject correct text.
    Residue and chrome are different in kind: no sentence is shaped like
    `writeAd({ adUnit: ... })`, so an automatic hit is machine damage by
    construction and a write is never legitimate.

    Raising, rather than repairing, is the point. Auto-repairing here would
    quietly make the fetcher the second, unenforced copy of the rules, and it
    would repair text on the way IN rather than leave a record. A raised
    exception stops the fetch, writes nothing, and leaves the diagnosis in the
    traceback.
    """
    if not content_md or not content_md.strip():
        return
    here = pathlib.Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    from fetch_damage import scan_text

    hits = [h for h in scan_text(content_md, judgement=False) if h.automatic]
    if not hits:
        return

    shown = "\n".join(
        "    line %d  [%s]  %s" % (h.line, h.rule, h.text.strip()[:88])
        for h in hits[:8])
    more = "" if len(hits) <= 8 else "\n    ... and %d more" % (len(hits) - 8)
    raise ValueError(
        "refusing to write %r (%s): the fetched body still contains %d "
        "automatic damage hit(s).\n%s%s\n"
        "This is a fetcher gap, not bad luck: `clean_content_element` does not "
        "know every rule `fetch_damage.py` has learned. Fix the stripper above, "
        "or teach `fetch_damage.py` the new shape - but do NOT copy the rule "
        "list here, because a second copy is what created the gap."
        % (slug, path, len(hits), shown, more))


def _write_canonical_file(path, title, work, wayback_url, cats, tags,
                           words, content_md):
    """Write a canonical-schema _posts file (schema keys unchanged)."""
    canon_slug = re.sub(r"[^a-z0-9]+", "-", work["slug"].lower()).strip("-")
    review_line = "needs_review: true\n" if words < FULL_MIN_WORDS else ""
    ts_match = re.search(r"/web/(\d+)/", wayback_url or "")
    provenance = "wayback-" + (ts_match.group(1) if ts_match else "unknown")
    fm = (
        "---\n"
        + 'title: "' + title + '"\n'
        + "date: " + work["date"] + "\n"
        + "slug: " + canon_slug + "\n"
        + 'original_url: "' + original_from_wayback(wayback_url) + '"\n'
        + 'wayback_url: "' + wayback_url + '"\n'
        + "categories: [" + ", ".join(cats) + "]\n"
        + "tags: [" + ", ".join(tags) + "]\n"
        + 'author: "Asadullah Ali Al-Andalusi"\n'
        + 'source: "The Andalusian Project Archive"\n'
        + "provenance: \"" + provenance + "\"\n"
        + "word_count: " + str(words) + "\n"
        + "layout: post\n"
        + review_line
        + "---\n\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        _assert_fetch_is_clean(content_md, work.get("slug", "?"), path)
        f.write(fm + (content_md or "").strip() + "\n")


def refetch_existing_post(work, existing_path):
    """Re-fetch one work against its frozen on-disk file (Task R guardrail).

    Returns (kept_old: bool, log_row). `kept_old=True` means the on-disk
    file was left byte-identical. Never creates, renames, or deletes files.
    """
    slug = work["slug"]
    wayback_url = work.get("wayback_url")
    _fm, old_body, old_title, old_words = read_post_file(existing_path)
    rel = os.path.relpath(existing_path, BASE_DIR).replace(os.sep, "/")
    log_row = {"slug": slug, "method": "wayback-refetch",
               "checked": datetime.now().strftime("%Y-%m-%d"),
               "content_file": rel}
    if not wayback_url:
        log_row.update(words=old_words, source_url=None,
                       verdict="kept_existing_snapshot_drift",
                       keep_reason="no_wayback_url")
        return True, log_row

    title, _date, content_md, error, soup = fetch_wayback_page(wayback_url)
    if error or soup is None:
        log_row.update(words=old_words, source_url=wayback_url,
                       verdict="kept_existing_snapshot_drift",
                       keep_reason="fetch_failed:%s" % (error or "unknown"))
        return True, log_row

    cats, tags = extract_cats_tags(soup)
    n_comments = count_comments(soup)
    new_words = len((content_md or "").split())
    log_row.update(source_url=wayback_url, fetched_title=title,
                   categories=cats, tags=tags, comments=n_comments,
                   words=old_words, fetched_words=new_words)

    title_ok = (normalize_title_for_match(title)
                == normalize_title_for_match(old_title)
                if title and old_title else False)
    ratio_ok = old_words > 0 and new_words >= GUARDRAIL_MIN_RATIO * old_words
    if not (title_ok and ratio_ok):
        reason = ";".join([
            "" if title_ok else "title_mismatch",
            "" if ratio_ok else "thin_snapshot(%d<%d)" % (
                new_words, int(GUARDRAIL_MIN_RATIO * old_words)),
        ]).strip(";")
        log_row.update(verdict="kept_existing_snapshot_drift",
                       keep_reason=reason or "guardrail")
        # Residual-junk scrub on the KEPT file: drop converter-damage
        # ad/JS lines from the old body only (full-line pattern matches;
        # author sentences untouched). Front matter preserved verbatim.
        raw = pathlib.Path(existing_path).read_text(encoding="utf-8")
        fm_block, old_body_text = split_front_matter(raw)
        scrubbed = scrub_ad_junk_lines(old_body_text)
        n_dropped = len(old_body_text.split("\n")) - len(scrubbed.split("\n"))
        if scrubbed != old_body_text:
            with open(existing_path, "w", encoding="utf-8") as f:
                # Scrubbing drops KNOWN ad/JS lines, but `scrub_ad_junk_lines`
                # is the same fixed list that `_assert_fetch_is_clean` exists
                # to hold to account: anything in the kept file that the damage
                # rules classify automatically and the scrubber did not know
                # about would otherwise be written straight back out.
                _assert_fetch_is_clean(scrubbed, work.get("slug", "?"),
                                       existing_path)
                f.write(fm_block + scrubbed)
            log_row.update(scrubbed_residual_junk_lines=n_dropped,
                           words=len(scrubbed.split()))
        return True, log_row

    # Guardrail passed: replace BODY only. Canonical-schema files keep
    # their schema with refreshed word_count (same keys); legacy-schema
    # files keep their front matter block byte-identical.
    raw = pathlib.Path(existing_path).read_text(encoding="utf-8")
    if "\nslug:" in (raw.split("---", 2)[1] if raw.count("---") >= 2 else ""):
        keep_title = old_title  # zero silent title changes
        _write_canonical_file(existing_path, keep_title, work, wayback_url,
                              cats, tags, new_words, content_md)
    else:
        fm_block, _old = split_front_matter(raw)
        with open(existing_path, "w", encoding="utf-8") as f:
            _assert_fetch_is_clean(content_md, work.get("slug", "?"), existing_path)
            f.write(fm_block + "\n\n" + (content_md or "").strip() + "\n")
    log_row.update(words=new_words, old_words=old_words, guardrail="pass",
                   verdict=("full" if new_words >= FULL_MIN_WORDS
                            else "review"))
    return False, log_row


def fetch_canonical_entry(work):
    """Fetch one canonical work (single HTTP round-trip set).

    Task R guardrail: when the canonical target file already exists, the
    fresh fetch replaces it only on title match + >=90% word count;
    otherwise the old file is kept byte-identical with verdict
    `kept_existing_snapshot_drift`.
    """
    slug = work["slug"]
    wayback_url = work.get("wayback_url")
    log_row = {"slug": slug, "method": "wayback-fetch",
               "checked": datetime.now().strftime("%Y-%m-%d")}
    if not wayback_url:
        log_row.update(words=0, source_url=None, verdict="skipped_no_url")
        return None, log_row

    title, date, content_md, error, soup = fetch_wayback_page(wayback_url)
    if error:
        log_row.update(words=0, source_url=wayback_url,
                       verdict=f"failed: {error}")
        return None, log_row

    cats, tags = extract_cats_tags(soup)
    n_comments = count_comments(soup)
    words = len((content_md or "").split())
    log_row.update(words=words, source_url=wayback_url,
                   fetched_title=title, categories=cats, tags=tags,
                   comments=n_comments)

    if words < REVIEW_MIN_WORDS:
        log_row["verdict"] = "stub_justify"
        return None, log_row

    final_title = (title or work["title"]).replace('"', "'").replace(
        "\ufffd", "—").strip()
    canon_slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    md_name = f"{work['date']}-{canon_slug}.md"
    target = os.path.join(POSTS_DIR, md_name)
    if os.path.exists(target):
        # Keep-better guardrail (binding): compare against on-disk file.
        _fm, _body, old_title, old_words = read_post_file(target)
        title_ok = (normalize_title_for_match(title)
                    == normalize_title_for_match(old_title)
                    if title and old_title else False)
        ratio_ok = (old_words > 0
                    and words >= GUARDRAIL_MIN_RATIO * old_words)
        if not (title_ok and ratio_ok):
            reason = ";".join([
                "" if title_ok else "title_mismatch",
                "" if ratio_ok else "thin_snapshot(%d<%d)" % (
                    words, int(GUARDRAIL_MIN_RATIO * old_words)),
            ]).strip(";")
            log_row.update(words=old_words, fetched_words=words,
                           keep_reason=reason or "guardrail",
                           verdict="kept_existing_snapshot_drift",
                           content_file=f"_posts/{md_name}")
            return md_name, log_row
        final_title = old_title  # zero silent title changes
        log_row.update(old_words=old_words, guardrail="pass")
    _write_canonical_file(target, final_title, work, wayback_url,
                          cats, tags, words, content_md)
    log_row["verdict"] = ("full" if words >= FULL_MIN_WORDS
                          else "review")
    log_row["content_file"] = f"_posts/{md_name}"
    return md_name, log_row


def probe_canonical_entry(work):
    """Fetch + classify one work WITHOUT writing any file.

    Used by --refetch-posts for target works that have no on-disk _posts
    file: the _posts set stays frozen (no new files; counts are owned by a
    sibling agent), so even content-bearing snapshots only refresh the
    recovery_log row.
    """
    slug = work["slug"]
    wayback_url = work.get("wayback_url")
    log_row = {"slug": slug, "method": "wayback-refetch",
               "checked": datetime.now().strftime("%Y-%m-%d")}
    if not wayback_url:
        log_row.update(words=0, source_url=None, verdict="skipped_no_url")
        return log_row
    title, _date, content_md, error, soup = fetch_wayback_page(wayback_url)
    if error or soup is None:
        log_row.update(words=0, source_url=wayback_url,
                       verdict="failed: %s" % (error or "unknown"))
        return log_row
    cats, tags = extract_cats_tags(soup)
    n_comments = count_comments(soup)
    words = len((content_md or "").split())
    log_row.update(words=words, source_url=wayback_url,
                   fetched_title=title, categories=cats, tags=tags,
                   comments=n_comments)
    if words >= REVIEW_MIN_WORDS:
        log_row.update(
            verdict="stub_justify",
            note=("suppressed_new_file: _posts set frozen; "
                  "counts owned by sibling agent"))
    else:
        log_row["verdict"] = "stub_justify"
    return log_row


def main_canonical(only=None, refetch_posts=False):
    print("=" * 70)
    print("Canonical fetch: 57-list works with quality gates")
    if refetch_posts:
        print("MODE: Task R refetch — all _posts-backed works, guardrail-gated")
    print("=" * 70)
    with open(CANON_JSON, encoding="utf-8") as f:
        works = json.load(f)
    # Targets: all wayback_only + the two thin "found" (by date).
    thin_dates = {"2014-05-29", "2015-02-09"}
    targets = [w for w in works
               if w.get("status") == "wayback_only"
               or (w.get("status") == "found" and w.get("date") in thin_dates)]
    refetch_plan = {}  # slug -> existing _posts path
    if refetch_posts:
        # Extend coverage to every work backing an on-disk _posts file
        # (the 37: 31 found + 6 needs_review), resolved by frozen filename
        # / front-matter URL — never by synthesizing names.
        by_slug = {w["slug"]: w for w in works}
        for w in works:
            if w.get("status") == "lost":
                continue
            hit = resolve_existing_post(w)
            if hit:
                refetch_plan[w["slug"]] = hit
        # Second pass: date-prefix fallback for files carrying no
        # wayback/original URL in front matter (unique date only).
        index = _existing_posts_index()
        resolved_paths = set(refetch_plan.values())
        works_by_date = {}
        for w in works:
            if w.get("status") == "lost":
                continue
            works_by_date.setdefault(w["date"], []).append(w)
        for name, path in sorted(index["name"].items()):
            if path in resolved_paths:
                continue
            date_prefix = name[:10]
            cands = [w for w in works_by_date.get(date_prefix, [])
                     if w["slug"] not in refetch_plan]
            if len(cands) == 1:
                refetch_plan[cands[0]["slug"]] = path
                resolved_paths.add(path)
        # Fail safe BEFORE any fetch: every _posts file must resolve.
        index = _existing_posts_index()
        resolved_paths = set(refetch_plan.values())
        unmapped = sorted(p for p in index["name"].values()
                          if p not in resolved_paths)
        if unmapped:
            print("ABORT: unmapped _posts files (resolve before fetching):")
            for p in unmapped:
                print(f"  - {p}")
            return 2
        targets = [by_slug[s] for s in sorted(refetch_plan)
                   if by_slug[s] not in targets] + targets
        # De-dupe preserving order, then sort refetch-first for the table.
        seen, ordered = set(), []
        for w in targets:
            if w["slug"] not in seen:
                seen.add(w["slug"])
                ordered.append(w)
        targets = sorted([w for w in ordered if w["slug"] in refetch_plan],
                         key=lambda w: w["slug"]) + \
            [w for w in ordered if w["slug"] not in refetch_plan]
    if only:
        wanted = set(only)
        targets = [w for w in targets if w["slug"] in wanted]
    print(f"Targets: {len(targets)}"
          + (f" ({len(refetch_plan)} with on-disk files)" if refetch_posts else ""))
    try:
        with open(RECOVERY_LOG, encoding="utf-8") as f:
            log = {r["slug"]: r for r in json.load(f)}
    except FileNotFoundError:
        log = {}
    counts = {"full": 0, "review": 0, "stub_justify": 0,
              "failed": 0, "skipped_no_url": 0,
              "kept_existing_snapshot_drift": 0}
    table = []  # (slug, old_words, new_words, kept) for the Task R report
    for i, w in enumerate(targets):
        print(f"\n[{i + 1}/{len(targets)}] {w['slug']}")
        try:
            if refetch_posts and w["slug"] in refetch_plan:
                existing = refetch_plan[w["slug"]]
                _fm, _body, _t, old_words = read_post_file(existing)
                kept, row = refetch_existing_post(w, existing)
                new_words = row.get("fetched_words", row.get("words", 0))
                table.append((w["slug"], old_words,
                              new_words if not kept else row.get(
                                  "fetched_words", old_words), kept))
                print(f"  -> {'KEPT old' if kept else 'REPLACED'} "
                      f"(old={old_words}w new={row.get('fetched_words', row.get('words', 0))}w) "
                      f"{row.get('keep_reason', row.get('verdict', ''))}")
            elif refetch_posts:
                row = probe_canonical_entry(w)
                print(f"  -> {row['verdict']} ({row.get('words', 0)} words, no file)")
            else:
                _, row = fetch_canonical_entry(w)
                print(f"  -> {row['verdict']} ({row.get('words', 0)} words)")
        except Exception as e:  # noqa: BLE001 - logged, never fatal
            traceback.print_exc()
            row = {"slug": w["slug"], "method": "wayback-fetch",
                   "checked": datetime.now().strftime("%Y-%m-%d"),
                   "words": 0, "source_url": w.get("wayback_url"),
                   "verdict": f"failed: {type(e).__name__}: {e}"}
            print(f"  -> {row['verdict']}")
        key = row["verdict"].split(":")[0]
        counts[key] = counts.get(key, 0) + 1
        log[w["slug"]] = row
        with open(RECOVERY_LOG, "w", encoding="utf-8") as f:
            json.dump(sorted(log.values(), key=lambda r: r["slug"]), f,
                      indent=2, ensure_ascii=False)
        time.sleep(REQUEST_DELAY)
    print("\n" + "=" * 70)
    for k, v in counts.items():
        print(f"  {k}: {v}")
    if refetch_posts and table:
        print("\nKEEP/REPLACE TABLE (slug | old words | new words | kept)")
        for slug, old_w, new_w, kept in table:
            print(f"  {slug} | {old_w} | {new_w} | {kept}")
        print(f"\nkept={sum(1 for r in table if r[3])} "
              f"replaced={sum(1 for r in table if not r[3])} "
              f"of {len(table)} files")
    return 0 if counts.get("failed", 0) == 0 else 1


if __name__ == "__main__":
    if "--canonical" in sys.argv:
        only = None
        refetch_posts = "--refetch-posts" in sys.argv
        for a in sys.argv:
            if a.startswith("--only="):
                only = a.split("=", 1)[1].split(",")
        sys.exit(main_canonical(only, refetch_posts))
    sys.exit(main())
