#!/usr/bin/env python3
"""Build comprehensive content index for The Andalusian Project Archive.

Honest counting: blog truth is the works list (canonical_works.json), not 87 CDX
capture rows. total_content is the sum of collection counts.
All paths are relative to this script (pathlib); no hardcoded absolute paths.
"""

import json
import pathlib
from datetime import datetime

BASE = pathlib.Path(__file__).parent.parent  # andalusian-archive/
DATA_DIR = BASE / "_data"


def load_len(name):
    path = DATA_DIR / name
    if not path.is_file():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    return len(data)


def load(name, default=None):
    path = DATA_DIR / name
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def counted_mdi(rows):
    """MDI rows that are a distinct item of content, not a second copy of a
    work already counted in canonical_works.json.

    `counted_as_work` is decided by a 5-gram text comparison, not by title
    similarity (see the duplicate_evidence field on each row). A row without
    the key is counted, so a new row is never silently dropped from the total.
    """
    if not rows:
        return 0, 0
    counted = [r for r in rows if r.get("counted_as_work", True) is not False]
    return len(counted), len(rows)


def held_pdf_counts(rows):
    """(PDF files held, paper rows that hold at least one) for papers.json.

    Counted from the data rather than from the directory, so the published
    figure and the files in _papers/pdfs/ are reconciled by the builder's own
    assertion in build_collections.py. A paper's own `file` is one file; each
    entry in `additional_files` is a further file (a translation), not a
    further paper, which is why the two numbers differ.
    """
    files = 0
    with_pdf = 0
    for p in rows or []:
        own = 1 if p.get("file") else 0
        extra = p.get("additional_files") or []
        if own or extra:
            with_pdf += 1
        files += own + len(extra)
    return files, with_pdf


def main():
    print("Building comprehensive content index...")

    captures = load_len("blog_posts.json")
    videos = load_len("videos.json")
    papers = load_len("papers.json")
    held_pdf_files, held_pdf_papers = held_pdf_counts(load("papers.json", []))
    mdi_rows = load("mdi_articles.json", [])
    mdi_all = len(mdi_rows)
    mdi = counted_mdi(mdi_rows)[0]
    mdi_dupes = mdi_all - mdi
    yaqeen = load_len("yaqeen_papers.json")
    albalagh = load_len("albalagh_courses.json")
    interviews = load_len("external_interviews.json")
    secondary = load_len("secondary_sources.json")

    canon_path = DATA_DIR / "canonical_works.json"
    works = None
    status_counts = {}
    if canon_path.is_file():
        canon = json.loads(canon_path.read_text(encoding="utf-8"))
        works = len(canon)
        for w in canon:
            status_counts[w.get("status", "?")] = \
                status_counts.get(w.get("status", "?"), 0) + 1
    notices = load_len("notices.json")
    n_found = status_counts.get("found", 0)
    n_wayback = status_counts.get("wayback_only", 0)
    n_lost = status_counts.get("lost", 0)
    works_phrase = ("%d works (%d full-text in repo, %d Wayback-only, %d lost)"
                    % (works or 0, n_found, n_wayback, n_lost))
    # Every term is labelled and every term is a number read out of _data/, so
    # the published string cannot drift from the files it summarises. The seven
    # terms between the "+" signs are the arithmetic; the parentheticals name
    # what each term counts and are deliberately outside the sum.
    total_content = ((works or 0) + videos + papers + mdi + yaqeen + albalagh
                     + interviews)
    formula = ("%d works + %d videos + %d papers + %d MDI items (of %d rows; "
               "%d are a second publication of a work already counted, so they "
               "are not added again) + %d Yaqeen link-outs (row count; no page "
               "body was downloaded, so no size is stored) + %d Al Balagh "
               "link-outs (row count) + %d interview = %d (excludes the derived "
               "secondary_sources and the %d uncounted announcements; the blog "
               "term is the works list, not the %d CDX captures)"
               % (works or 0, videos, papers, mdi, mdi_all, mdi_dupes, yaqeen,
                  albalagh, interviews, total_content, notices, captures))

    # Preserve unsourced legacy stats if present (no source files exist).
    talks = translations = None
    index_path = DATA_DIR / "content_index.json"
    if index_path.is_file():
        old_stats = json.loads(index_path.read_text(encoding="utf-8")).get("statistics", {})
        talks = old_stats.get("total_talks")
        translations = old_stats.get("total_translations")

    collections = {
        "blog_posts": {
            "description": "%s; %d CDX captures preserved as metadata"
                           % (works_phrase, captures),
            "count": captures,
            "storage": ("METADATA IN REPO (full text for %d found works only)"
                        % n_found),
            "risk_level": "HIGH - original site offline",
        },
        "videos": {
            "description": "Video lectures and discussions from The Andalusian Project YouTube channel and mirrors",
            "count": videos,
            "storage": "IN REPO (Archive.org + YouTube mirrors)",
            "risk_level": "MEDIUM - YouTube channel deleted, mirrors exist",
        },
        "papers": {
            "description": "Academic papers and research articles",
            "count": papers,
            "storage": ("LINKS to institutional repositories, plus %d PDF files "
                        "held across %d of the %d papers"
                        % (held_pdf_files, held_pdf_papers, papers)),
            "risk_level": "LOW - institutionally hosted",
        },
        "mdi_articles": {
            "description": ("Articles by Asadullah Ali on the Muslim Debate "
                            "Initiative website; %d of the %d rows are a "
                            "second publication of a work already counted"
                            % (mdi_dupes, mdi_all)),
            "count": mdi,
            "rows": mdi_all,
            "duplicate_of_a_counted_work": mdi_dupes,
            "storage": "FULL TEXT IN REPO (recovered 2026-09-27, verbatim)",
            "risk_level": "MEDIUM - site active but content may change",
            "source_file": "mdi_articles.json",
        },
        "yaqeen_papers": {
            "description": ("Research papers and blog posts on Yaqeen Institute "
                            "by Asadullah Ali"),
            "count": yaqeen,
            "sizes_known": 2,
            "storage": ("LINK-OUTS ONLY (Global Constraint 4). Row count, not a "
                        "content count: 2 of the %d rows have a known word "
                        "count and %d have none, because no Yaqeen page body "
                        "was downloaded." % (yaqeen, yaqeen - 2)),
            "risk_level": "LOW - institutionally hosted",
            "source_file": "yaqeen_papers.json",
        },
        "albalagh_courses": {
            "description": "Online Islamic courses on Al Balagh Academy (including Asadullah Ali's courses)",
            "count": albalagh,
            "storage": "LINKS (scraped via Firecrawl)",
            "risk_level": "LOW - institutionally hosted",
            "source_file": "albalagh_courses.json",
        },
        "external_interviews": {
            "description": "Interviews and Q&A features on external platforms",
            "count": interviews,
            "storage": "LINKS (scraped via Firecrawl)",
            "risk_level": "MEDIUM - third-party hosted",
            "source_file": "external_interviews.json",
        },
        "secondary_sources": {
            "description": "Combined index of all external content referencing Asadullah Ali and The Andalusian Project",
            "count": secondary,
            "storage": "IN REPO",
            "risk_level": "LOW - derived data",
            "source_files": [
                "mdi_articles.json",
                "yaqeen_papers.json",
                "albalagh_courses.json",
                "external_interviews.json",
            ],
        },
    }

    statistics = {
        "total_blog_works": works if works is not None else captures,
        "total_blog_captures": captures,
        "total_notices": notices,
        "total_videos": videos,
        "total_papers": papers,
        # Task 0 ruling / Task 3: total is non-overlapping sum of works,
        # excluding derived secondary_sources (and legacy talks/translations)
        # and the announcement notices, which are catalogued but never counted
        # as works. The formula string is computed, never hardcoded, so it can
        # never drift from the data again.
        "total_content": total_content,
        "total_content_formula": formula,
        "total_content_terms": {
            "works": works if works is not None else captures,
            "videos": videos,
            "papers": papers,
            "mdi_counted": mdi,
            "yaqeen_linkouts": yaqeen,
            "albalagh_linkouts": albalagh,
            "interviews": interviews,
        },
        "blog_status_counts": status_counts,
        "total_mdi_articles": mdi,
        "total_mdi_rows": mdi_all,
        "total_mdi_duplicate_of_a_work": mdi_dupes,
        "total_yaqeen_papers": yaqeen,
        "total_albalagh_courses": albalagh,
        "total_external_interviews": interviews,
        "total_secondary_sources": secondary,
    }
    if talks is not None:
        statistics["total_talks"] = talks
    if translations is not None:
        statistics["total_translations"] = translations

    content_index = {
        "last_updated": datetime.now().isoformat(),
        "project_name": "The Andalusian Project Archive",
        "author": "Asadullah Ali Al-Andalusi",
        "description": "Digital preservation of Asadullah Ali Al-Andalusi's work for academic research and education",
        "statistics": statistics,
        "collections": collections,
        "sources": {
            "wayback_machine": {
                "url": "https://web.archive.org",
                "status": "Active",
                "content": "Blog posts and website content",
            },
            "archive_org": {
                "url": "https://archive.org/details/andalusian-project",
                "status": "Active",
                "content": "Video archive",
            },
            "yaqeen_institute": {
                "url": "https://yaqeeninstitute.org",
                "status": "Active",
                "content": "Academic papers",
            },
            "muslim_debate_initiative": {
                "url": "https://muslimdebate.org",
                "status": "Active",
                "content": "Articles and debates",
            },
            "al_balagh_academy": {
                "url": "https://www.albalaghacademy.org",
                "status": "Active",
                "content": "Course materials",
            },
        },
        "preservation_notes": {
            "blog_posts": ("%s; %d CDX captures preserved as metadata. Recovered "
                           "2026-09-07 via canonical Wayback fetch, junk-purged "
                           "2026-09-08; WordPress-mirror, IDI and best-capture "
                           "recoveries integrated 2026-09-27 (see recovery_log.json "
                           "and bibliography.json)." % (works_phrase, captures)),
            "notices": ("%d announcements (book lists, library updates, link posts) "
                        "catalogued in notices.json with counted_as_work=false. They "
                        "carry the recovered text but are excluded from every total."
                        % notices),
            "videos": ("%d videos catalogued in videos.json; mirrors attach as "
                       "mirror_urls and are never counted separately." % videos),
            "papers": ("Academic papers are hosted by Yaqeen Institute and other "
                       "institutions; links are provided for access, and the texts "
                       "legitimately obtained are held under _papers/pdfs/. See "
                       "bibliography.json for the full oa/restricted/dead ledger."),
            "mdi_articles": ("%d rows from the muslimdebate.org author archive, "
                             "of which %d are a second publication of a work "
                             "already counted (decided by 5-gram text "
                             "comparison, not title similarity) and %d are a "
                             "distinct item. Full text recovered 2026-09-27 and "
                             "stored in this repository; 7 of the %d are "
                             "<100-word captions for an embedded video and are "
                             "kept as published."
                             % (mdi_all, mdi_dupes, mdi, mdi_all)),
            "yaqeen_papers": "9 papers/blog posts from Asadullah Ali's Yaqeen Institute profile. Titles and URLs preserved; full content hosted by Yaqeen Institute.",
            "albalagh_courses": "33 unique courses from Al Balagh Academy (deduped by canonical URL 2026-09-07), including 3 taught by Asadullah Ali. URLs and titles preserved.",
            "external_interviews": "1 interview/Q&A features from external publications. Full Q&A text available in the scraped markdown.",
        },
    }

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(content_index, f, indent=2, ensure_ascii=False)

    print(f"Content index saved to {index_path}")
    print("Statistics:")
    for key, value in statistics.items():
        print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
