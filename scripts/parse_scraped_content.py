#!/usr/bin/env python3
"""
Parse Firecrawl-scraped markdown files and create structured JSON data files
for The Andalusian Project Archive.

Sources parsed:
  1. mdi_articles.md         -> _data/mdi_articles.json
  2. yaqeen_profile.md       -> _data/yaqeen_papers.json
  3. albalagh_profile.md     -> _data/albalagh_courses.json
  4. traversing_tradition.md -> _data/external_interviews.json
  5. wordpress_site.md       -> (metadata used in secondary_sources.json)
"""

import json
import os
import pathlib
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths (relative to this script; no hardcoded absolute paths)
# ---------------------------------------------------------------------------
BASE = pathlib.Path(__file__).parent.parent  # andalusian-archive/
SCRAPED_DIR = BASE.parent  # repo root: mdi_articles.md, yaqeen_profile.md, ...
DATA_DIR = BASE / "_data"

# ---------------------------------------------------------------------------
# Helper: fix Firecrawl mojibake
# ---------------------------------------------------------------------------
_REPLACEMENTS = {
    "ΓÇÖ": "\u2019",  # right single quote
    "ΓÇ£": "\u201c",  # left double quote
    "ΓÇ¥": "\u201d",  # right double quote
    "ΓÇó": "\u2022",  # bullet
    "ΓÇô": "\u2013",  # en dash
    "ΓÇ║": "\u25b6",  # triangle
    "ΓÇ¡": "\u2020",  # dagger
    "ΓÇ░": "\u2018",  # left single quote
    "ΓåÉ": "\u25c0",
    "ΓåÆ": "\u25b6",
    "ΓÇò": "\u2014",  # em dash
    "ΓÇª": "...",
}


def fix_encoding(text: str) -> str:
    for bad, good in _REPLACEMENTS.items():
        text = text.replace(bad, good)
    return text


def write_json(filename: str, data) -> None:
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    count = len(data) if isinstance(data, list) else "object"
    print(f"  [OK] {filename}  ({count})")


# ===================================================================
# 1. Parse MDI articles (muslimdebate.org)
# ===================================================================
def parse_mdi_articles():
    filepath = os.path.join(SCRAPED_DIR, "mdi_articles.md")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    text = fix_encoding(raw)

    articles = []
    blocks = re.split(r"(?=^## \[)", text, flags=re.MULTILINE)

    for block in blocks:
        title_match = re.match(r"## \[(.+?)\]\((https?://[^\)]+)\)", block)
        if not title_match:
            continue

        title = title_match.group(1).strip()
        url = title_match.group(2).strip()

        date_match = re.search(r"on \[([A-Z][a-z]+ \d{1,2}, \d{4})\]", block)
        date = date_match.group(1) if date_match else ""

        summary = ""
        for line in block.split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("![") or stripped.startswith("By[") or stripped.startswith("on [") or stripped.startswith("#"):
                continue
            summary = stripped
            break

        articles.append({
            "title": title,
            "url": url,
            "date": date,
            "author": "Asadullah Ali Al-Andalusi",
            "source": "Muslim Debate Initiative",
            "summary": summary
        })

    write_json("mdi_articles.json", articles)
    return articles


# ===================================================================
# 2. Parse Yaqeen Institute profile
# ===================================================================
def parse_yaqeen_profile():
    filepath = os.path.join(SCRAPED_DIR, "yaqeen_profile.md")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    text = fix_encoding(raw)

    papers = []
    paper_blocks = text.split("[![")
    for block in paper_blocks[1:]:
        topic_match = re.search(
            r"\[([^\]]+?)\s*\u2022\s*(\d+\s*min)\]\((https?://yaqeeninstitute\.org/topic/[^\)]+)\)",
            block
        )
        title_match = re.search(
            r"\[\*\*(.+?)\*\*\]\((https?://yaqeeninstitute\.org/read/[^\)]+)\)",
            block
        )
        if title_match:
            topic = topic_match.group(1).strip() if topic_match else ""
            title = title_match.group(1).strip()
            url = title_match.group(2).strip()
            papers.append({
                "title": title,
                "url": url,
                "topic": topic,
                "author": "Asadullah Ali Al-Andalusi",
                "source": "Yaqeen Institute for Islamic Research"
            })

    seen = set()
    unique = []
    for p in papers:
        if p["url"] not in seen:
            seen.add(p["url"])
            unique.append(p)

    write_json("yaqeen_papers.json", unique)
    return unique


# ===================================================================
# 3. Parse Al Balagh Academy profile
# ===================================================================
def parse_albalagh_profile():
    filepath = os.path.join(SCRAPED_DIR, "albalagh_profile.md")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    text = fix_encoding(raw)

    # --- Asadullah Ali's own courses (explicit section, uses bold markdown) ---
    asadullah_courses = []
    bold_course_re = re.compile(
        r"\[\*\*(.+?)\*\*\]\((https?://www\.albalaghacademy\.org/course/[^\)]+)\)"
    )
    section_m = re.search(
        r"## Courses by Ustadh Asadullah Ali Al-Andalusi(.+?)## Popular Courses",
        text, re.DOTALL
    )
    if section_m:
        for m in bold_course_re.finditer(section_m.group(1)):
            asadullah_courses.append({
                "title": m.group(1).strip(),
                "url": m.group(2).strip(),
                "instructor": "Asadullah Ali Al-Andalusi",
                "source": "Al Balagh Academy",
                "description": "Course taught by Asadullah Ali Al-Andalusi"
            })

    # --- All unique courses (both bold and plain markdown links) ---
    # Pattern A: [**Bold Title**](url)
    # Pattern B: [Plain Title](url)
    all_course_re = re.compile(
        r"\[(?:\*\*(.+?)\*\*|([^\]]+))\]\((https?://www\.albalaghacademy\.org/course/[^\)]+)\)"
    )

    # URLs to skip (navigation/category links, not course detail pages)
    SKIP_PATTERNS = [
        "utm_source", "utm_medium", "utm_campaign", "utm_content",
        "project_category", "self-paced-courses", "free-online-courses",
        "testimonial", "our-team"
    ]

    all_courses = []
    seen_urls = set()
    for m in all_course_re.finditer(text):
        title = (m.group(1) or m.group(2)).strip()
        url = m.group(3).strip()

        # Skip category/nav links and duplicates
        clean_url = re.sub(r"\?.*$", "", url)
        if clean_url in seen_urls:
            continue
        # Skip very short titles (likely image alt text) and navigation items
        if len(title) < 5:
            continue
        seen_urls.add(clean_url)

        is_asad = any(ac["url"].startswith(clean_url) for ac in asadullah_courses)
        all_courses.append({
            "title": title,
            "url": url,
            "instructor": "Asadullah Ali Al-Andalusi" if is_asad else "",
            "source": "Al Balagh Academy",
            "description": "Course taught by Asadullah Ali Al-Andalusi" if is_asad else ""
        })

    write_json("albalagh_courses.json", all_courses)
    return all_courses, asadullah_courses


# ===================================================================
# 4. Parse Traversing Tradition Q&A
# ===================================================================
def parse_traversing_tradition():
    filepath = os.path.join(SCRAPED_DIR, "traversing_tradition.md")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    text = fix_encoding(raw)

    interviews = []

    title_m = re.search(r"^# (.+?)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else ""

    date_m = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
        text
    )
    date = date_m.group(0) if date_m else ""

    url_m = re.search(r"\[Skip to content\]\((https?://[^\)]+)\)", text)
    url = url_m.group(1).strip() if url_m else ""
    url = re.sub(r"#.*$", "", url)

    qa_count = len(re.findall(r"^\d+\.\s+\*\*", text, re.MULTILINE))

    tags_match = re.search(r"\[Featured\].*$", text, re.MULTILINE)
    tags = []
    if tags_match:
        tags = re.findall(
            r"\[([^\]]+)\]\(https://traversingtradition\.com/tag/[^\)]+\)",
            tags_match.group(0)
        )

    interviews.append({
        "title": title,
        "url": url,
        "date": date,
        "source": "Traversing Tradition",
        "type": "Q&A Interview",
        "author": "Asadullah Ali Al-Andalusi",
        "summary": (
            f"A Q&A interview covering science, history, and atheism "
            f"({qa_count} questions). Topics include the Golden Age of Islam, "
            "philosophy of science, Orientalist narratives, and the relationship "
            "between Islam and modern science."
        ),
        "tags": tags,
        "questions_count": qa_count
    })

    write_json("external_interviews.json", interviews)
    return interviews


# ===================================================================
# 5. Parse WordPress site metadata
# ===================================================================
def parse_wordpress_site():
    filepath = os.path.join(SCRAPED_DIR, "wordpress_site.md")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    text = fix_encoding(raw)

    bio_m = re.search(r"Asadullah Ali Al-Andalusi is (.+?)\.", text)
    bio = bio_m.group(1).strip() if bio_m else ""

    sections = re.findall(
        r"\[\*\*([^\*]+)\*\*\]\((https?://asadullahali\.wordpress\.com/[^\)]+)\)",
        text
    )
    seen = set()
    unique_sections = []
    for name, url in sections:
        if name not in seen:
            seen.add(name)
            unique_sections.append({"name": name, "url": url})

    return {
        "site_name": "The Andalusian Project",
        "url": "https://asadullahali.wordpress.com/",
        "bio": bio,
        "sections": unique_sections
    }


# ===================================================================
# 6. Build secondary_sources.json
# ===================================================================
def build_secondary_sources(mdi_articles, yaqeen_papers, albalagh_courses,
                            interviews, wp_data):
    sources = []

    for a in mdi_articles:
        sources.append({
            "title": a["title"],
            "url": a["url"],
            "source": "Muslim Debate Initiative",
            "type": "article",
            "summary": a["summary"],
            "date": a["date"]
        })

    for p in yaqeen_papers:
        sources.append({
            "title": p["title"],
            "url": p["url"],
            "source": "Yaqeen Institute",
            "type": "paper",
            "summary": f"Topic: {p['topic']}" if p["topic"] else "",
            "date": ""
        })

    for c in albalagh_courses:
        sources.append({
            "title": c["title"],
            "url": c["url"],
            "source": "Al Balagh Academy",
            "type": "course",
            "summary": c["description"],
            "date": ""
        })

    for i in interviews:
        sources.append({
            "title": i["title"],
            "url": i["url"],
            "source": "Traversing Tradition",
            "type": "interview",
            "summary": i["summary"],
            "date": i["date"]
        })

    sources.append({
        "title": wp_data["site_name"],
        "url": wp_data["url"],
        "source": "WordPress.com",
        "type": "website",
        "summary": wp_data["bio"],
        "date": ""
    })

    write_json("secondary_sources.json", sources)
    return sources


# ===================================================================
# 7. Update content_index.json
# ===================================================================
def update_content_index(mdi_articles, yaqeen_papers, albalagh_courses,
                         interviews, secondary_sources, asadullah_courses_count):
    index_path = os.path.join(DATA_DIR, "content_index.json")
    with open(index_path, "r", encoding="utf-8") as f:
        content_index = json.load(f)

    content_index["collections"]["mdi_articles"] = {
        "description": "Articles by Asadullah Ali on the Muslim Debate Initiative website",
        "count": len(mdi_articles),
        "storage": "LINKS (scraped via Firecrawl)",
        "risk_level": "MEDIUM - site active but content may change",
        "source_file": "mdi_articles.md"
    }
    content_index["collections"]["yaqeen_papers"] = {
        "description": "Research papers and blog posts on Yaqeen Institute by Asadullah Ali",
        "count": len(yaqeen_papers),
        "storage": "LINKS (scraped via Firecrawl)",
        "risk_level": "LOW - institutionally hosted",
        "source_file": "yaqeen_profile.md"
    }
    content_index["collections"]["albalagh_courses"] = {
        "description": "Online Islamic courses on Al Balagh Academy (including Asadullah Ali's courses)",
        "count": len(albalagh_courses),
        "storage": "LINKS (scraped via Firecrawl)",
        "risk_level": "LOW - institutionally hosted",
        "source_file": "albalagh_profile.md"
    }
    content_index["collections"]["external_interviews"] = {
        "description": "Interviews and Q&A features on external platforms",
        "count": len(interviews),
        "storage": "LINKS (scraped via Firecrawl)",
        "risk_level": "MEDIUM - third-party hosted",
        "source_file": "traversing_tradition.md"
    }
    content_index["collections"]["secondary_sources"] = {
        "description": "Combined index of all external content referencing Asadullah Ali and The Andalusian Project",
        "count": len(secondary_sources),
        "storage": "IN REPO",
        "risk_level": "LOW - derived data",
        "source_files": [
            "mdi_articles.md",
            "yaqeen_profile.md",
            "albalagh_profile.md",
            "traversing_tradition.md",
            "wordpress_site.md"
        ]
    }

    content_index["statistics"]["total_mdi_articles"] = len(mdi_articles)
    content_index["statistics"]["total_yaqeen_papers"] = len(yaqeen_papers)
    content_index["statistics"]["total_albalagh_courses"] = len(albalagh_courses)
    content_index["statistics"]["total_external_interviews"] = len(interviews)
    content_index["statistics"]["total_secondary_sources"] = len(secondary_sources)
    content_index["statistics"]["total_content"] = (
        content_index["statistics"].get("total_blog_posts", 0)
        + content_index["statistics"].get("total_videos", 0)
        + content_index["statistics"].get("total_papers", 0)
        + len(mdi_articles)
        + len(yaqeen_papers)
        + len(albalagh_courses)
        + len(interviews)
    )

    content_index["preservation_notes"]["mdi_articles"] = (
        f"{len(mdi_articles)} articles scraped from muslimdebate.org author archive page. "
        "Full article text is not available from the listing page; summaries and URLs preserved."
    )
    content_index["preservation_notes"]["yaqeen_papers"] = (
        f"{len(yaqeen_papers)} papers/blog posts from Asadullah Ali's Yaqeen Institute profile. "
        "Titles and URLs preserved; full content hosted by Yaqeen Institute."
    )
    content_index["preservation_notes"]["albalagh_courses"] = (
        f"{len(albalagh_courses)} unique courses from Al Balagh Academy, "
        f"including {asadullah_courses_count} taught by Asadullah Ali. "
        "URLs and titles preserved."
    )
    content_index["preservation_notes"]["external_interviews"] = (
        f"{len(interviews)} interview/Q&A features from external publications. "
        "Full Q&A text available in the scraped markdown."
    )

    content_index["last_updated"] = datetime.now().isoformat()
    write_json("content_index.json", content_index)


# ===================================================================
# Main
# ===================================================================
def main():
    print("=" * 60)
    print("  The Andalusian Project - Scraped Content Parser")
    print("=" * 60)
    print()

    print("[1/5] Parsing MDI articles (muslimdebate.org)...")
    mdi_articles = parse_mdi_articles()
    print()

    print("[2/5] Parsing Yaqeen Institute profile...")
    yaqeen_papers = parse_yaqeen_profile()
    print()

    print("[3/5] Parsing Al Balagh Academy profile...")
    albalagh_all, albalagh_asadullah = parse_albalagh_profile()
    print()

    print("[4/5] Parsing Traversing Tradition Q&A...")
    interviews = parse_traversing_tradition()
    print()

    print("[5/5] Parsing WordPress site metadata...")
    wp_data = parse_wordpress_site()
    print("  [OK] wordpress_site.md parsed (bio + navigation)")
    print()

    print("--- Building secondary_sources.json ---")
    secondary = build_secondary_sources(
        mdi_articles, yaqeen_papers, albalagh_all, interviews, wp_data
    )
    print()

    print("--- Updating content_index.json ---")
    update_content_index(
        mdi_articles, yaqeen_papers, albalagh_all, interviews, secondary,
        len(albalagh_asadullah)
    )
    print()

    print("=" * 60)
    print("  EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"  MDI Articles:          {len(mdi_articles)}")
    print(f"  Yaqeen Papers:         {len(yaqeen_papers)}")
    print(f"  Al Balagh Courses:     {len(albalagh_all)} (all unique)")
    print(f"    Asadullah's courses: {len(albalagh_asadullah)}")
    print(f"  External Interviews:   {len(interviews)}")
    print(f"  Secondary Sources:     {len(secondary)} (combined)")
    print(f"  WordPress Site:        metadata only")
    print("=" * 60)


if __name__ == "__main__":
    main()
