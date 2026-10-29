#!/usr/bin/env python3
"""Build a small, dependency-free semantic index for the archive.

The archive has several catalogues that describe the same work from different
angles: `_data/canonical_works.json`, the generated `_posts`/`_articles` pages,
papers, videos, MDI rows and the topic specs. Titles repeat, spellings drift and
the same essay can appear as a work, a post and an article. This script does
three things:

1. Collapses records that share a normalised title into one document.
2. Scores every document pair with TF-IDF cosine similarity over titles,
   summaries, themes, topics and (where available) body text.
3. Writes `_data/semantic_links.json`: the top related documents for each
   record, plus the duplicate groups it found.

It is deliberately pure stdlib. No embedding service, no API key and no network
call are needed, so the result is reproducible in CI and offline.

Usage:
    python -B scripts/build_semantic_index.py
    python -B scripts/build_semantic_index.py --check
"""

from __future__ import annotations

import ast
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
OUT = DATA / "semantic_links.json"

STOPWORDS = {
    "a", "about", "after", "against", "all", "also", "an", "and", "any",
    "are", "as", "at", "be", "because", "been", "before", "being", "between",
    "both", "but", "by", "can", "could", "did", "do", "does", "doing", "done",
    "for", "from", "had", "has", "have", "having", "he", "her", "here", "him",
    "his", "how", "i", "if", "in", "into", "is", "it", "its", "just", "may",
    "me", "more", "most", "my", "no", "nor", "not", "of", "on", "once", "only",
    "or", "other", "our", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "them", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "will", "with", "would", "you", "your",
}


def load(name: str):
    path = DATA / name
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str) and value.strip().startswith("["):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except (ValueError, SyntaxError):
            pass
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", str(value).lower())
    return value.strip("-")


def clean_title(value: str) -> str:
    value = re.sub(r"\[[^\]]*\]", " ", str(value))
    value = re.sub(r"^\s*\d+\s*[-:.]\s*", "", value)
    return re.sub(r"\s+", " ", value).strip()


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean_title(value).lower()).strip()


def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]{3,}", text.lower())
    return [w[:-1] if len(w) > 4 and w.endswith("s") else w
            for w in words if w not in STOPWORDS]


def read_body(path: Path, limit: int = 5000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    text = re.sub(r"[#>*_`\[\]()]", " ", text)
    return text[:limit]


def post_url(rel: str, slug: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    head = path.read_text(encoding="utf-8-sig", errors="replace").split("---", 2)
    meta = head[1] if len(head) > 2 else ""
    cats = re.search(r"^categories:\s*(.+)$", meta, re.M)
    parts = []
    if cats:
        parts = [part.strip().strip('"').lower()
                 for part in cats.group(1).strip().strip("[]").split(",")]
        parts = [part for part in parts if part]
    return quote("/" + "/".join(parts + [slug]) + "/", safe="/")


def build_documents():
    docs: dict[str, dict] = {}
    aliases: dict[str, str] = {}
    duplicate_rows: dict[str, list[str]] = {}

    def add(key, kind, title, text, url="", year=""):
        norm = normalise(title)
        # A numbered part is a different work, not a duplicate of its sibling.
        # `clean_title()` strips bracketed segments and leading numbers, so the
        # signature must be read from the raw title before normalisation.
        part = re.search(
            r"\b(?:part|pt|volume|vol|book|chapter)\s*"
            r"([0-9]+|[ivxlcdm]+)\b", str(title), re.I)
        if part:
            norm += "|" + part.group(1).lower()
        if not norm:
            return
        if norm in duplicate_rows:
            primary = duplicate_rows[norm][0]
            aliases[key] = primary
            docs[primary]["text"] += " " + text
            docs[primary]["aliases"].append(key)
            if len(duplicate_rows[norm]) == 1:
                duplicate_rows[norm].append(key)
            else:
                duplicate_rows[norm].append(key)
            return
        duplicate_rows[norm] = [key]
        docs[key] = {
            "key": key, "kind": kind, "title": clean_title(title),
            "text": text, "url": url, "year": year, "aliases": [],
        }

    for row in load("canonical_works.json"):
        slug = row.get("slug", "")
        if not slug:
            continue
        title = row.get("title", slug)
        local = row.get("local_post", "")
        if local:
            url = post_url(local, slug)
            body = read_body(ROOT / local)
        elif (ROOT / "_articles" / f"{slug}.md").exists():
            url = f"/articles/{slug}/"
            body = read_body(ROOT / "_articles" / f"{slug}.md")
        else:
            url, body = "", ""
        add(f"work:{slug}", "work", title,
            " ".join([title, row.get("category", ""), row.get("status", ""), body]),
            url, str(row.get("date", ""))[:4])

    for row in load("papers.json"):
        title = row.get("title", "")
        if not title:
            continue
        add(f"paper:{slugify(title)}", "paper", title,
            " ".join([title, row.get("publisher_journal", ""),
                      row.get("volume_issue", ""), row.get("type", ""),
                      row.get("note", ""), " ".join(as_list(row.get("co_authors")))]),
            f"/papers/{slugify(title)}/", str(row.get("publication_date", ""))[:4])

    for row in load("videos.json"):
        vid = row.get("id", "")
        title = clean_title(row.get("title", ""))
        if not vid or not title:
            continue
        add(f"video:{vid}", "video", title,
            " ".join([title, " ".join(as_list(row.get("themes"))),
                      " ".join(as_list(row.get("topics"))), row.get("tone", ""),
                      row.get("format", "")]),
            f"/videos/{vid}/")

    for row in load("mdi_articles.json"):
        slug, title = row.get("slug", ""), row.get("title", "")
        if not slug or not title:
            continue
        add(f"mdi:{slug}", "mdi", title,
            " ".join([title, row.get("summary", ""),
                      str(row.get("text", ""))[:5000]]),
            row.get("local_page") or f"/articles/mdi/{slug}/")

    for row in load("yaqeen_papers.json"):
        title = row.get("title", "")
        if not title:
            continue
        add(f"yaqeen:{slugify(title)}", "yaqeen", title,
            " ".join([title, row.get("topic", "")]), row.get("url", ""))

    for row in load("albalagh_courses.json"):
        title = row.get("title", "")
        if not title:
            continue
        add(f"albalagh:{slugify(title)}", "albalagh", title,
            " ".join([title, row.get("description", ""), row.get("source", "")]),
            row.get("url", ""))

    for row in load("external_interviews.json"):
        title = row.get("title", "")
        if not title:
            continue
        add(f"interview:{slugify(title)}", "interview", title,
            " ".join([title, row.get("summary", ""), " ".join(as_list(row.get("tags")))]),
            row.get("url", ""))

    # Generated article pages that are not already represented by a work.
    for path in sorted((ROOT / "_articles").glob("*.md")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        head = text.split("---", 2)
        meta = head[1] if len(head) > 2 else ""
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', meta, re.M)
        slug = re.search(r"^slug:\s*\"?([^\"]+)\"?\s*$", meta, re.M)
        permalink = re.search(r"^permalink:\s*\"?([^\"]+)\"?\s*$", meta, re.M)
        if not title:
            continue
        add(f"article:{slug.group(1) if slug else path.stem}", "article",
            title.group(1), " ".join([title.group(1), read_body(path)]),
            (permalink.group(1) if permalink else f"/articles/{path.stem}/"))

    for path in sorted((ROOT / "_transcripts").glob("*.md")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        head = text.split("---", 2)
        meta = head[1] if len(head) > 2 else ""
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', meta, re.M)
        permalink = re.search(r"^permalink:\s*\"?([^\"]+)\"?\s*$", meta, re.M)
        if not title:
            continue
        add(f"transcript:{path.stem}", "transcript", title.group(1),
            " ".join([title.group(1), read_body(path, 2500)]),
            permalink.group(1) if permalink else "")

    return docs, aliases, duplicate_rows


def cosine_links(docs: dict[str, dict]) -> dict[str, list[dict]]:
    frequencies = {k: Counter(tokens(d["text"])) for k, d in docs.items()}
    doc_freq = Counter()
    for tf in frequencies.values():
        doc_freq.update(tf.keys())
    total = max(len(docs), 1)
    vectors = {}
    for key, tf in frequencies.items():
        vec = {term: (1 + math.log(count)) * (math.log((1 + total) / (1 + doc_freq[term])) + 1)
               for term, count in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vectors[key] = (vec, norm)

    links = {}
    keys = list(docs)
    for key in keys:
        vec_a, norm_a = vectors[key]
        scored = []
        for other in keys:
            if other == key:
                continue
            vec_b, norm_b = vectors[other]
            if docs[key]["kind"] == docs[other]["kind"] and docs[key]["title"] == docs[other]["title"]:
                continue
            small, large = (vec_a, vec_b) if len(vec_a) < len(vec_b) else (vec_b, vec_a)
            dot = sum(value * large.get(term, 0.0) for term, value in small.items())
            score = dot / (norm_a * norm_b)
            if score > 0.08:
                scored.append((score, other))
        scored.sort(key=lambda pair: (-pair[0], docs[pair[1]]["title"]))
        picked = []
        seen_titles = set()
        for score, other in scored:
            target = docs[other]
            title_key = normalise(target["title"])
            if title_key in seen_titles or not target["url"]:
                continue
            seen_titles.add(title_key)
            picked.append({
                "key": other,
                "kind": target["kind"],
                "title": target["title"],
                "url": target["url"],
                "score": round(score, 4),
            })
            if len(picked) >= 5:
                break
        if picked:
            links[key] = picked
    return links


def build() -> dict:
    docs, aliases, duplicate_rows = build_documents()
    links = cosine_links(docs)
    for alias, primary in aliases.items():
        if primary in links:
            links[alias] = [dict(item) for item in links[primary] if item["key"] != alias]
    duplicates = [
        {"title": docs[keys[0]]["title"], "keys": keys}
        for keys in duplicate_rows.values() if len(keys) > 1
    ]
    duplicates.sort(key=lambda row: row["title"].lower())
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "documents": len(docs),
        "duplicate_groups": duplicates,
        "links": dict(sorted(links.items())),
    }


def main() -> int:
    result = build()
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"FAIL: {OUT.relative_to(ROOT)} is missing")
            return 1
        current = json.loads(OUT.read_text(encoding="utf-8"))
        a = {k: v for k, v in result.items() if k != "generated"}
        b = {k: v for k, v in current.items() if k != "generated"}
        if a != b:
            print("FAIL: semantic index is stale; run scripts/build_semantic_index.py")
            return 1
        print(f"OK: semantic index is current ({result['documents']} documents, "
              f"{len(result['links'])} link sets, {len(result['duplicate_groups'])} duplicate groups)")
        return 0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {result['documents']} documents, "
          f"{len(result['links'])} link sets, {len(result['duplicate_groups'])} duplicate groups")
    for row in result["duplicate_groups"][:10]:
        print(f"  duplicate: {row['title']} -> {', '.join(row['keys'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
