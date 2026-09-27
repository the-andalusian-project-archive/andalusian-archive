#!/usr/bin/env python3
"""CI assert for Task 4 search-data sync (issues C-06 + I-13).

Asserts the synced search files match their _data sources row-for-row and with
the expected row counts, and zero empty titles across all synced search files.
Also checks the prebuilt excerpt/keyword index and that verbatim files match
_data sources.
Run: ``python scripts/test_search_sync.py`` (or ``npm run test:search-sync``).
Exit 0 on PASS, 1 on any failure.
"""

import json
import pathlib
import sys

BASE = pathlib.Path(__file__).parent.parent
# Row counts, updated 2026-09-27 by Task 7 / I1, frozen again by the approved
# recount of 2026-09-28. These are the figures the site publishes.
#   works  57 -> 72  (15 recovered works integrated)
#   papers 18 -> 20  (2 legitimately obtained PDFs became new paper entries)
#   videos  68 -> 67 (I2: 12 superseded mirrors removed, 11 new entries added)
#              -> 68 (amendment A: G47Stp3pLss restored as a counted work by
#                      user decision, not as a mirror of 7KBCENktOOU)
#   captures 87     (CDX capture records; metadata, never counted as works)
EXPECT_COUNTS = {
    "videos.json": 68,
    "papers.json": 20,
    "canonical_works.json": 72,
    "blog_posts.json": 87,
}
# Files copied verbatim from _data/, which are therefore required to be
# byte-equal and not merely parse-equal. canonical_works.json and
# blog_posts.json are deliberately NOT in this set: sync_search_data.py adds an
# excerpt/keyword index to them, so byte-equality is the wrong claim for those
# two and would be a gate that could only ever fail.
VERBATIM = {
    "videos.json": "videos.json",
    "papers.json": "papers.json",
}
# data file -> _data source for freshness checks
SOURCES = {
    "videos.json": "videos.json",
    "papers.json": "papers.json",
    "canonical_works.json": "canonical_works.json",
    "blog_posts.json": "blog_posts.json",
}
failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL: " + msg)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report as test failure
        fail("%s unreadable: %s" % (path, exc))
        return None


def check_titles(name, rows):
    for i, row in enumerate(rows):
        title = row.get("title", "") if isinstance(row, dict) else ""
        if not str(title).strip():
            fail("%s[%d] has empty title" % (name, i))
            return
        if str(title).strip().startswith("?"):
            fail("%s[%d] title starts with '?': %r" % (name, i, title))
            return


def main():
    for name, expected in EXPECT_COUNTS.items():
        rows = load(BASE / "data" / name)
        if rows is None:
            continue
        if len(rows) != expected:
            fail("data/%s len=%d != %d" % (name, len(rows), expected))
        else:
            print("PASS: data/%s == %d" % (name, expected))
        check_titles("data/" + name, rows)

    # Freshness: the verbatim copies must be byte-equal to their _data source,
    # not merely parse-equal. Parse-equality would accept a reserialised file
    # with different key order, indentation or trailing newline - a drift that
    # shows up as a noisy diff in every future review of a generated file.
    for name in ("videos.json", "papers.json"):
        data_path = BASE / "data" / name
        src_path = BASE / "_data" / SOURCES[name]
        if not data_path.is_file() or not src_path.is_file():
            fail("%s or its _data source is missing" % name)
            continue
        if data_path.read_bytes() != src_path.read_bytes():
            fail("data/%s is not byte-equal to _data/%s (run sync)"
                 % (name, name))
        else:
            print("PASS: data/%s is byte-equal to _data/%s" % (name, name))
        data = load(data_path)
        src = load(src_path)
        if data is not None and src is not None:
            if data != src:
                fail("data/%s differs from _data/%s (run sync)" % (name, name))
            else:
                print("PASS: data/%s matches _data/%s" % (name, name))

    # Works: core fields preserved + prebuilt index present.
    works = load(BASE / "data" / "canonical_works.json")
    src_works = load(BASE / "_data" / "canonical_works.json")
    if works is not None and src_works is not None and len(works) == len(src_works):
        core = ("slug", "title", "date", "wayback_url", "status")
        for i, (w, s) in enumerate(zip(works, src_works)):
            if any(w.get(k) != s.get(k) for k in core):
                fail("data/canonical_works.json[%d] core fields drifted" % i)
                break
        else:
            print("PASS: data/canonical_works.json core fields match _data")
        for i, w in enumerate(works):
            if not w.get("excerpt") or not w.get("keywords"):
                fail("data/canonical_works.json[%d] missing excerpt/keywords" % i)
                break
        else:
            print("PASS: data/canonical_works.json has excerpt/keyword index")

    # Captures stay available: same row count as source, enriched + titled.
    caps = load(BASE / "data" / "blog_posts.json")
    src_caps = load(BASE / "_data" / "blog_posts.json")
    if caps is not None and src_caps is not None:
        if len(caps) != len(src_caps):
            fail("data/blog_posts.json len=%d != source %d"
                 % (len(caps), len(src_caps)))
        else:
            print("PASS: data/blog_posts.json preserves %d captures" % len(caps))
        check_titles("data/blog_posts.json", caps)
        for i, c in enumerate(caps):
            if not c.get("excerpt") or not c.get("keywords") or not c.get("slug"):
                fail("data/blog_posts.json[%d] missing slug/excerpt/keywords" % i)
                break
            if "?" in str(c.get("slug", "")) or "#" in str(c.get("slug", "")):
                fail("data/blog_posts.json[%d] slug not stripped: %r"
                     % (i, c.get("slug")))
                break
        else:
            print("PASS: data/blog_posts.json has clean slug/excerpt/keyword index")

    if failures:
        print("test_search_sync: %d FAILURE(S)" % len(failures))
        return 1
    # The searchable population the /search/ page prints is these three
    # collections. Gating it here means the page's figure cannot be right about
    # the data and wrong about itself.
    searchable = (EXPECT_COUNTS["canonical_works.json"]
                  + EXPECT_COUNTS["videos.json"]
                  + EXPECT_COUNTS["papers.json"])
    if searchable != 160:
        fail("searchable total is %d, not the published 160" % searchable)
    else:
        print("PASS: searchable total = %d (72 works + 68 videos + 20 papers)"
              % searchable)
    print("test_search_sync: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
