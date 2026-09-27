#!/usr/bin/env python3
"""Derive the transcript series index, and write it to _data/series.json.

WHY THIS FILE EXISTS
--------------------
The archive's single most unique asset is 68 machine transcripts, 540,995
words, that exist nowhere else - and until now they were one flat list. A
reader who wants the third session of *Understanding Atheism* has no page to land
on. This file decides which recordings form a SERIES, so that each series can
get a page of its own.

The question the brief posed was whether the data supports real groupings, and
the honest answer was: not in the fields it named, yes in a different one. The
evidence for both halves is recorded below, because the difference matters and
because a reader deciding whether to trust this index needs to know which parts
of the corpus it covers and which it deliberately leaves alone.

WHAT THE DATA DOES NOT SUPPORT
------------------------------
`_data/videos.json` carries `themes`, `topics` and `tone` on every row, and they
look like a topic taxonomy. They are not. `scripts/generate_video_themes.py`
produced them with a first-match-wins substring test over a ten-key map:

    for key in THEME_MAP:
        if key != "default" and key in title_lower:
            return THEME_MAP[key]

The consequences are measurable and they disqualify these fields as a grouping
key:

  * 34 distinct theme strings are produced, but they are the SAME three strings
    for every title that matches no keyword. 19 rows carry
    "Islamic studies discourse", 21 carry "Intellectual exploration" and 25
    carry "Contemporary issues analysis" - so the largest bucket is not a topic,
    it is the classifier's `default` branch.
  * All six sessions of *Understanding Atheism* and all three parts of
    *iKhalifa* land in that same default bucket, because neither title contains
    one of the eight keywords. Grouping on it would put a lecture series and an
    unrelated short talk in one "topic".
  * The rows carry no per-transcript topic at all. Neither
    `_data/transcript_index.json` (fields: transcript_id, title, role, url,
    capture_video_id, recording_url, source, lang, lines, words, paragraphs,
    file) nor `_data/transcript_coverage.json` (video_id, title, captions, lang,
    lines, source, file) has a topic or series key.

So no index is built on `themes`/`topics`/`tone`, and none is invented.

WHAT THE DATA DOES SUPPORT
--------------------------
The channel numbered its own uploads and used one title shape for every series
member:

    NN - <series name> [| <part label>] [<video id>]

That shape is in the preserved titles themselves, which are recovered evidence
and are reproduced verbatim everywhere they appear. Parsing it is reading the
archive's own record, not categorising it. Each rule below is a regex over that
shape; the series NAME is the channel's own string, not a label this file chose.
A row that matches no rule is left ungrouped and is counted, never forced into a
group, because a category built to fill a gap is exactly what this archive will
not do.

THE OUTPUT
----------
`_data/series.json` - the series registry, the parts in the channel's own order,
and an explicit list of what did not match. Nothing on the published pages types
a count; they read this file and count its rows at build time.

Run:
    python scripts/build_series_index.py           # write _data/series.json
    python scripts/build_series_index.py --check   # verify only; exit 1 on drift
"""

import json
import pathlib
import re
import sys
import unicodedata

BASE = pathlib.Path(__file__).resolve().parent.parent
DATA = BASE / "_data"
VIDEOS_JSON = DATA / "videos.json"
COVERAGE_JSON = DATA / "transcript_coverage.json"
INDEX_JSON = DATA / "transcript_index.json"
OUT_JSON = DATA / "series.json"

# ------------------------------------------------------------- the rules ---
# (slug, series title as the channel wrote it, framing sentence, regex).
# The regex is anchored on the channel's own `NN - ` numbering, so a row only
# matches when the title really is one of the channel's numbered series members.
SERIES_RULES = [
    (
        "understanding-atheism",
        "Understanding Atheism",
        "A six-session lecture series on atheism, naturalism and the epistemology "
        "of belief without evidence, numbered 01 to 06 by the channel itself and "
        "each session published as a separate recording. All six sessions are in "
        "this archive and all six have a published transcript.",
        r"^(\d+)\s*-\s*Understanding Atheism\b",
    ),
    (
        "a-muslims-guide-to-science-and-scientism",
        "A Muslim's Guide to Science and Scientism",
        "A five-part Al Balagh Academy lecture course on science, scientism and "
        "the claim that one commits the other, numbered 16 to 20 by the channel. "
        "This is the series the archive's own data records as his Al Balagh "
        "teaching: it is the only multi-part course in the corpus that is "
        "attested in _data/ as well as in the recording titles.",
        r"^(\d+)\s*-\s*A Muslims Guide to Science and Scientism\b",
    ),
    (
        "ijihad",
        "iJihad",
        "A six-episode run responding to the online material published under the "
        "name The Masked Arab. The episodes are numbered in the titles "
        "themselves - Ep. 1, Ep. 3, Ep. 4, Ep. 5, Ep. 6, plus one untitled "
        "instalment - and the numbering is the channel's, not this archive's. "
        "This series is a record of a reply, and is preserved as one.",
        r"^(\d+)\s*-\s*iJihad\b",
    ),
    (
        "ikalifa",
        "iKhalifa",
        "A three-part series numbered 1, 2 and 3 in the titles. The name is the "
        "channel's own; this archive does not expand or translate it.",
        r"^(\d+)\s*-\s*iKhalifa\b",
    ),
    (
        "understanding-jihad-with-robert-spencer",
        "Understanding Jihad with Robert Spencer",
        "Three recordings - a preface and two numbered parts - in which he "
        "responds to Robert Spencer. Held as a series because the three titles "
        "name the same interlocutor and carry the channel's own preface/part "
        "numbering.",
        r"^(\d+)\s*-\s*Understanding Jihad\b",
    ),
    (
        "book-recommendations",
        "Book Recommendations",
        "Three numbered recommendation videos, #1 to #3. The only series in the "
        "corpus that is neither a lecture course nor a debate run.",
        r"^(\d+)\s*-\s*Book Recommendations\b",
    ),
    (
        "atheism-doubting-your-doubts",
        "Atheism: Doubting Your Doubts (Yaqeen in New York)",
        "Two recordings of one event, a Yaqeen Institute lecture in New York, "
        "catalogued as two entries: one is the event upload and one names him in "
        "the title. They are the same lecture, and the archive keeps them as two "
        "catalogue rows because it does not merge records.",
        r"^(\d+)\s*-\s*Atheism\D{0,4}\s*Doubting Your Doubts\b",
    ),
]

# The titles carry full-width and other non-ASCII punctuation - the channel's own
# `｜`, `：`, `⧸` and curly quotes - so the shape is matched after a NFKC
# normalisation and a small explicit fold. NFKC alone does not fold every
# character in this set, and the fold list is written out rather than left
# implicit so a reader can see exactly what was changed before matching.
FOLD = {
    "\uff5c": "|",   # ｜ FULLWIDTH VERTICAL LINE, the channel's separator
    "\uff1a": ":",   # ： FULLWIDTH COLON, the channel's title/subtitle separator
    "\uff0f": "/",   # ／ FULLWIDTH SOLIDUS
    "\u29f8": "/",   # ⧸ BIG SOLIDUS, used in "w/ Robert Spencer"
    "\u3014": "]",
    "\u3015": "[",
    "\u2013": "-",
    "\u2014": "-",
    "\u2010": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u00a0": " ",
}


# Trailing byline segments the channel closed some of these titles with, after a
# `｜` or `||` separator. Listed, not guessed at: a name is not a part
# designation, and printing it as one would be a false label on a reader-facing
# page. Compared case-insensitively after stripping spaces and dashes.
BYLINE_SEGMENTS = (
    "asadullah andalusi",
    "asadullah ali",
    "the andalusian project",
    "andalusian project",
    "by andalusian project",
)


def fold(text):
    text = unicodedata.normalize("NFKC", str(text))
    for bad, good in FOLD.items():
        text = text.replace(bad, good)
    return text


def own_docs(index, video_id):
    """The one transcript published for this recording, not a duplicate-upload one.

    A recording transcribed twice yields two documents; the extra one is an
    additional transcript of the same recording, not a second part, so the
    series counts the recording once and names the additional capture separately.
    """
    return [d for d in index.get(video_id, [])
            if d.get("role") != "duplicate-upload"]


def own_url(index, video_id):
    docs = own_docs(index, video_id)
    return docs[0]["url"] if docs else ""


def own_words(index, video_id):
    docs = own_docs(index, video_id)
    return docs[0]["words"] if docs else 0


def part_label(title, match_end, video_id):
    """The channel's own part wording: what is left of the title after the
    series name, with the trailing `[video id]` and the trailing byline removed.

    Kept as the channel wrote it so the page can print "Session 3" or "Ep. 4" or
    "Part 1" in his own words rather than in a numbering this file made up.

    The byline removal is an explicit list, not a heuristic. The channel closed
    some of these titles with its own byline after a `｜` or `||` separator, and
    that byline is a name, not a part designation, so leaving it in would print
    "#1 | Asadullah Andalusi | The Andalusian Project" as the label for part one.
    Only the segments named in BYLINE_SEGMENTS are dropped; a segment this list
    does not know about is kept, because an unrecognised segment is far more
    likely to be a real part designation than a stray byline.

    Returns "" when nothing is left, and the page then shows the channel's own
    upload number instead of inventing a part number.
    """
    rest = title[match_end:]
    rest = re.sub(r"\s*\[\s*%s\s*\]\s*$" % re.escape(video_id), "", rest)
    kept = []
    for seg in rest.split("|"):
        s = seg.strip(" \t-:")
        if not s:
            continue
        low = s.lower()
        if any(low == b or low.endswith(" " + b) or low.endswith(" " + b + " project")
               for b in BYLINE_SEGMENTS):
            continue
        kept.append(s)
    return " | ".join(kept)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    videos = load(VIDEOS_JSON)
    coverage = {r["video_id"]: r for r in load(COVERAGE_JSON)}
    index = load(INDEX_JSON)["by_recording"]

    series = []
    assigned = {}
    for slug, title, framing, pattern in SERIES_RULES:
        rx = re.compile(pattern, re.I)
        parts = []
        for row in videos:
            m = rx.match(fold(row["title"]))
            if not m:
                continue
            if row["id"] in assigned:
                raise SystemExit(
                    "row %s matched both %s and %s; the rules must be disjoint"
                    % (row["id"], assigned[row["id"]], slug))
            assigned[row["id"]] = slug
            vid = row["id"]
            parts.append({
                "number": int(m.group(1)),
                "part_label": part_label(fold(row["title"]), m.end(), vid),
                "video_id": vid,
                "title": row["title"],
                "recording_url": "/videos/%s/" % vid,
                "transcript_url": own_url(index, vid),
                "transcript_words": own_words(index, vid),
                "transcript_of_same_recording": len(index.get(vid, [])) - (
                    1 if own_url(index, vid) else 0),
                "archive_org": bool(row.get("archive_org_id")),
                "in_coverage_data": vid in coverage,
            })
        parts.sort(key=lambda p: p["number"])
        if len(parts) < 2:
            # A single match is not a series. Refusing here is the whole point of
            # the rule: a "series" of one is a category invented to fill a page.
            raise SystemExit(
                "rule %s matched %d row(s); a series needs 2 or more"
                % (slug, len(parts)))
        series.append({
            "slug": slug,
            "title": title,
            "framing": framing,
            "parts": parts,
            "part_count": len(parts),
            "numbers": [p["number"] for p in parts],
            "transcript_words": sum(p["transcript_words"] for p in parts),
        })

    series.sort(key=lambda s: (-s["part_count"], s["title"]))

    ungrouped = [{"video_id": r["id"], "title": r["title"]}
                 for r in videos if r["id"] not in assigned]

    return {
        "built": "2026-09-28",
        "built_by": "scripts/build_series_index.py. The rules are in that file and "
                    "the command is `python scripts/build_series_index.py --check`. "
                    "This file is generated; edit the script, not the JSON.",
        "purpose": "Groups the preserved recordings into the multi-part series the "
                   "channel itself numbered, so each series can be indexed. It is "
                   "the grouping signal for /transcripts/by-series/ and the seven "
                   "series pages under it.",
        "grouping_signal": "The channel's own `NN - <series name>` title shape, "
                           "recovered verbatim in the preserved recording titles. "
                           "Not `themes`, `topics` or `tone`: those are produced by "
                           "a first-match-wins substring classifier "
                           "(scripts/generate_video_themes.py) whose largest bucket "
                           "is its `default` branch, so they relabel rows rather "
                           "than group them, and no per-transcript topic field "
                           "exists in _data/transcript_index.json or "
                           "_data/transcript_coverage.json.",
        "series": series,
        "series_count": len(series),
        "grouped_videos": len(assigned),
        "ungrouped_videos": len(ungrouped),
        "ungrouped": ungrouped,
        "ungrouped_note": "Left ungrouped on purpose. A row that matches no series "
                          "rule is not filed under an invented category, and the "
                          "index page says so with this count. These recordings are "
                          "all in the archive and all listed on the full transcript "
                          "index and in the video catalogue; they simply are not "
                          "parts of a series.",
        "totals_are_not_counts_of_content": "Nothing on this page adds to the "
                                            "archive's published total of counted "
                                            "content. A series is a view over "
                                            "recordings that are already counted "
                                            "once each in _data/videos.json.",
    }


def main():
    check = "--check" in sys.argv[1:]
    built = build()
    text = json.dumps(built, indent=2, ensure_ascii=False) + "\n"
    if check:
        if not OUT_JSON.is_file():
            print("build_series_index: %s does not exist" % OUT_JSON.name)
            return 1
        current = OUT_JSON.read_text(encoding="utf-8")
        if current != text:
            print("build_series_index: %s has drifted from the rule in "
                  "scripts/build_series_index.py (run it without --check)"
                  % OUT_JSON.name)
            return 1
        print("build_series_index: %s matches the rule (%d series, %d grouped, "
              "%d ungrouped)" % (OUT_JSON.name, built["series_count"],
                                 built["grouped_videos"],
                                 built["ungrouped_videos"]))
        return 0
    OUT_JSON.write_text(text, encoding="utf-8")
    print("build_series_index: wrote %s (%d series, %d grouped videos, %d "
          "ungrouped)" % (OUT_JSON.name, built["series_count"],
                          built["grouped_videos"], built["ungrouped_videos"]))
    for s in built["series"]:
        print("   %-42s %d parts  %s" % (s["slug"], s["part_count"],
                                         s["numbers"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
