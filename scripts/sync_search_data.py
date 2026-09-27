#!/usr/bin/env python3
"""Sync single source of truth _data/*.json -> data/*.json for client search.

Task 4 (issues C-06 + I-13). Runs automatically via ``npm run build``
(prebuild hook) or manually with ``npm run sync-data``. Pure stdlib, so it
works on Windows pwsh and Linux CI (``python`` locally, ``python3`` in CI).

Verbatim copies (parsed content identical to source):
  _data/videos.json       (68) -> data/videos.json
  _data/papers.json       (20) -> data/papers.json

Enriched builds (adds prebuilt excerpt/keyword index + zero-empty-title
guarantee used by search.md instead of title+URL-only matching):
  _data/blog_posts.json   (87 captures) -> data/blog_posts.json
  _data/canonical_works.json (72 works) -> data/canonical_works.json

Search defaults to the works list (72); captures stay available via
data/blog_posts.json. NOTE (Task 5): search detail links (/papers/, /videos/,
/articles/) resolve to the generated _papers/_videos/_articles collections;
build_collections.py's collection_drift() gate keeps those in step with the
data files.
"""

import json
import pathlib
import re

BASE = pathlib.Path(__file__).parent.parent
DATA_DIR = BASE / "data"
SRC_DIR = BASE / "_data"

URL_DATE_RE = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/([^/?#]+)/?")
TOKEN_RE = re.compile(r"[^a-z0-9]+")


def load(name):
    return json.loads((SRC_DIR / name).read_text(encoding="utf-8"))


def write(name, obj):
    dest = DATA_DIR / name
    dest.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    return dest


def strip_query(url):
    """Return url without ?query or #fragment (M-09: strip before slugify)."""
    return str(url or "").split("?")[0].split("#")[0]


def slug_from_url(url):
    """Derive a clean slug from a post URL (query/fragment stripped first)."""
    clean = strip_query(url).rstrip("/")
    m = URL_DATE_RE.search(clean + "/")
    if m:
        return m.group(4).strip().lower()
    parts = [p for p in clean.split("/") if p]
    return parts[-1].strip().lower() if parts else ""


def humanize_slug(slug, fallback="untitled"):
    text = re.sub(r"[-_]+", " ", str(slug or "")).strip()
    return text or fallback


def keywords_for(*texts):
    """Deterministic keyword tokens (lowercase alnum, len>=3, deduped)."""
    seen = []
    for text in texts:
        for tok in TOKEN_RE.split(str(text or "").lower()):
            if len(tok) >= 3 and tok not in seen:
                seen.append(tok)
    return seen


def needs_title_fix(title):
    t = str(title or "")
    return not t.strip() or t.strip().startswith("?")


def enrich_capture(row):
    """Enrich one CDX capture row: fix empty/??? titles, add slug/excerpt."""
    row = dict(row)
    slug = slug_from_url(row.get("url", ""))
    if not slug:
        slug = re.sub(r"[^a-z0-9]+", "-", str(row.get("title", "")).lower()
                      ).strip("-")
    if needs_title_fix(row.get("title")):
        row["title"] = humanize_slug(slug, fallback=str(row.get("url", "")))
    title = row["title"]
    date = str(row.get("date", "") or "")
    keywords = keywords_for(title, slug, date)
    excerpt = title
    if date:
        excerpt += " (%s)" % date
    excerpt += ". " + humanize_slug(slug) + "."
    row["slug"] = slug
    row["excerpt"] = excerpt[:280]
    row["keywords"] = keywords
    return row


def enrich_work(work):
    """Enrich one canonical work with the same prebuilt search index fields."""
    work = dict(work)
    title = work.get("title", "")
    slug = work.get("slug", "")
    date = str(work.get("date", "") or "")
    work["excerpt"] = ("%s (%s). %s." % (
        title, date, humanize_slug(slug)) if date else "%s. %s." % (
        title, humanize_slug(slug)))[:280]
    work["keywords"] = keywords_for(title, slug, date)
    return work


def main():
    DATA_DIR.mkdir(exist_ok=True)

    videos = load("videos.json")
    papers = load("papers.json")
    canon = load("canonical_works.json")
    caps = load("blog_posts.json")

    write("videos.json", videos)
    write("papers.json", papers)
    enriched_works = [enrich_work(w) for w in canon]
    write("canonical_works.json", enriched_works)
    enriched_caps = [enrich_capture(r) for r in caps]
    write("blog_posts.json", enriched_caps)

    fixed = sum(1 for src, out in zip(caps, enriched_caps)
                if src.get("title") != out["title"])
    print("videos=%d papers=%d works=%d captures=%d titles_fixed=%d"
          % (len(videos), len(papers), len(enriched_works),
             len(enriched_caps), fixed))
    print("wrote %s" % (DATA_DIR))


if __name__ == "__main__":
    main()
