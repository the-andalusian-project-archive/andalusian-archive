#!/usr/bin/env python3
"""Build _data/canonical_works.json - the 2026-09-06 recovery baseline.

!! HISTORICAL BUILDER - DO NOT RE-RUN OVER THE LIVE FILE. !!
This script reconstructs the ORIGINAL 57-work list from the 2026-09-06 session
context. Task 7 (2026-09-27) integrated 15 further recovered works and 3
announcements into _data/canonical_works.json (now 72 works, 47 found /
24 wayback_only / 1 lost). Re-running this builder would silently delete those
15 works and revert 2 status upgrades, so it refuses to run while the live file
holds rows this session list cannot produce. See GUARD below.

Sources (all paths relative to this script, no hardcoded absolute paths):
  ../../session_context.md        authoritative 57-entry manual list (titles, dates)
  ../../wayback_posts.json        56 Wayback capture rows (original_url -> wayback_url)
  ../_data/blog_posts.json        87 CDX capture rows (incl. 17 actual_post mappings)
  ../_posts/*.md                  full-text files preserved in repo

Output: ../_data/canonical_works.json - array of works
  {slug, title, date, wayback_url|null, status: found|wayback_only|lost}

Rules:
  - Library Take Down Notice 2014-03-17 -> wayback_url null, status wayback_only
    (feed only captured; see blog_posts.json feed row, content_file None).
  - The Making of Modern Western Civilization 2014-10-21 -> status lost.
  - Everything else -> found iff its content_file resolves in the blog_posts.json
    actual_post mapping (file exists in repo) or a matching _posts/*.md exists;
    otherwise wayback_only.
"""

import json
import pathlib
import re
import sys

SCRIPT_DIR = pathlib.Path(__file__).parent
BASE = SCRIPT_DIR.parent                      # andalusian-archive/
ROOT = BASE.parent                            # repo root (session_context.md lives here)

SESSION_CONTEXT = ROOT / "session_context.md"
WAYBACK_POSTS = ROOT / "wayback_posts.json"
BLOG_POSTS = BASE / "_data" / "blog_posts.json"
POSTS_DIR = BASE / "_posts"
OUTPUT = BASE / "_data" / "canonical_works.json"

# (date, slug) pairs known lost: no recoverable capture, no file in repo.
LOST = {
    ("2012-02-26", "the-inhumanity-of-human-rights"),
    ("2014-10-21", "the-making-of-modern-western-civilization-the-war-on-islam-guest-contribution"),
}

ENTRY_RE = re.compile(r"^(\d+)\.\s+(.+?)\s+\((\d{4}-\d{2}-\d{2})\)\s+[—–-]\s+(.+?)\s*$")
URL_DATE_RE = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/([^/]+)/?")

def slug_from_url(url):
    m = URL_DATE_RE.search(url or "")
    if not m:
        return None, None
    date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return date, m.group(4).strip().lower()


def parse_session_list(text):
    """Extract the 57 numbered entries under the Wayback Machine Content heading."""
    try:
        section = text.split("## Wayback Machine Content (57 Blog Posts)")[1]
    except IndexError:
        print("ERROR: 57-list section not found in session_context.md", file=sys.stderr)
        sys.exit(1)
    # Stop at the next top-level section (Reddit threads follow the list).
    section = section.split("## Reddit Threads")[0]
    entries = []
    for line in section.splitlines():
        m = ENTRY_RE.match(line.strip())
        if m:
            entries.append({
                "title": m.group(2).strip(),
                "date": m.group(3),
                "ref": m.group(4).strip(),
            })
    return entries


def main():
    session_entries = parse_session_list(
        SESSION_CONTEXT.read_text(encoding="utf-8"))
    if len(session_entries) != 57:
        print(f"ERROR: parsed {len(session_entries)} session entries, expected 57",
              file=sys.stderr)
        sys.exit(1)

    # GUARD (2026-09-27, Task 7 / I1): refuse to clobber rows this session
    # list cannot produce. The 57-entry session list predates the WordPress-mirror
    # and IDI recoveries; overwriting the live file with it would delete 15
    # recovered works and revert the 2 stub-fill status upgrades.
    if OUTPUT.is_file():
        live = {w.get("slug") for w in json.loads(OUTPUT.read_text(encoding="utf-8"))}
        recoverable = set()
        for entry in session_entries:
            key_date, slug = slug_from_url(entry["ref"])
            recoverable.add(slug or re.sub(r"[^a-z0-9]+", "-",
                                           entry["title"].lower()).strip("-"))
        recoverable |= {"%s-%s" % (s, d) for (d, s) in LOST}
        extra = sorted(s for s in live if s and s not in recoverable)
        if extra:
            print("ERROR: refusing to overwrite %s" % OUTPUT, file=sys.stderr)
            print("  it holds %d row(s) this 2026-09-06 session list cannot "
                  "produce, e.g. %s" % (len(extra), ", ".join(extra[:5])),
                  file=sys.stderr)
            print("  This builder is a historical record of the 57-work baseline. "
                  "Edit the live file directly, or pass an explicit output path.",
                  file=sys.stderr)
            sys.exit(2)

    wayback_rows = json.loads(WAYBACK_POSTS.read_text(encoding="utf-8"))
    # Map (post_date, slug) -> wayback_url. NOTE: wayback_posts.json `date`
    # is the capture date, so the post date is parsed from original_url.
    wayback_by_key = {}
    for row in wayback_rows:
        key_date, slug = slug_from_url(row.get("original_url", ""))
        if key_date and slug:
            wayback_by_key[(key_date, slug)] = row.get("wayback_url")

    caps = json.loads(BLOG_POSTS.read_text(encoding="utf-8"))
    # Map (post_date, slug) -> content_file for actual_post captures.
    content_by_key = {}
    for row in caps:
        if row.get("url_type") == "actual_post" or row.get("content_type") == "actual_post":
            key_date, slug = slug_from_url(row.get("url", ""))
            if key_date and slug:
                content_by_key[(key_date, slug)] = row.get("content_file")

    post_files = {p.name for p in POSTS_DIR.glob("*.md")} if POSTS_DIR.is_dir() else set()
    post_dates = {name[:10] for name in post_files}

    works = []
    seen_slugs = set()
    warnings = []
    for entry in session_entries:
        title, date, ref = entry["title"], entry["date"], entry["ref"]
        feed_only = ref.lower().startswith("feed only")
        wayback_url = None if feed_only else ref

        # Slug from the post URL (session ref URL, else wayback_posts original_url).
        key_date, slug = (None, None)
        if not feed_only:
            key_date, slug = slug_from_url(ref)
        if slug is None:
            # Derive from title as last resort (feed-only entry).
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        base_slug = slug
        if slug in seen_slugs:  # e.g. extremism-in-muslim-thought x2 -> date-suffix
            slug = f"{base_slug}-{date}"
        seen_slugs.add(slug)

        key = (date, base_slug)
        if key in LOST:
            status = "lost"
            # Keep the archival URL for reference even though content is unrecoverable.
            if wayback_url is None:
                wayback_url = wayback_by_key.get(key)
        elif feed_only:
            status = "wayback_only"
        else:
            content_file = content_by_key.get(key)
            resolved = (
                content_file is not None
                and (BASE / content_file).is_file()
            )
            date_match = date in post_dates
            if resolved or date_match:
                status = "found"
            else:
                status = "wayback_only"
            if wayback_url is None:
                wayback_url = wayback_by_key.get(key)
            if key not in content_by_key and key not in wayback_by_key:
                warnings.append(f"no capture row for {date} {base_slug}")

        works.append({
            "slug": slug,
            "title": title,
            "date": date,
            "wayback_url": wayback_url,
            "status": status,
        })

    works.sort(key=lambda w: (w["date"], w["slug"]))

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    n_found = sum(1 for w in works if w["status"] == "found")
    n_wayback = sum(1 for w in works if w["status"] == "wayback_only")
    n_lost = sum(1 for w in works if w["status"] == "lost")
    print(f"works={len(works)} found={n_found} wayback_only={n_wayback} lost={n_lost}")

    if len(works) != 57 or n_lost != 2:
        print("ERROR: expected 57 works with exactly 2 lost", file=sys.stderr)
        sys.exit(1)

    OUTPUT.write_text(json.dumps(works, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
