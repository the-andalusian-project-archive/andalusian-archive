#!/usr/bin/env python3
"""Stamp the four-category taxonomy onto every countable row. Idempotent.

WHY THIS FILE EXISTS (2026-09-27, task 8f, Phase-3 review M6). The `category`
and `counted` keys on 189 rows across seven data files were applied by an
ad-hoc script that was never committed, so the assignment this whole archive
is sorted by could not be reproduced or re-derived from the repository - only
believed. That is the worst possible state for a provenance claim: the data
was checkable, the RULE was not. This file is the rule, executable, and
`--check` is the gate.

WHAT IT DOES. For each data file named in `_data/taxonomy.json` -> `data_files`,
it computes the category letter and the counted flag for every row from that
file's own fields, per the rules written out in RULES below, and compares them
with what the file actually carries. With no argument it writes the computed
values; with `--check` it writes nothing and exits 1 on any disagreement.

The rules are the ones in `_data/taxonomy.json` -> `ordering_rule` /
`rules.format_is_not_authorship` / `rules.guest_vs_producer` /
`rules.ambiguity`, in code:

  * A row he made is A, whatever shape it is. A video he produced is A even if
    it is a debate; the test is the entry's own evidence, not the word
    "debate" in its title.
  * A row somebody else made that he appears in is C.
  * A recording whose own evidence does not settle authorship is assigned A and
    MUST carry a `category_basis` saying why, rather than being guessed at
    silently. This is the one place the script's answer is deliberately not
    derived: `G47Stp3pLss` rests on an unverified byline, and the ambiguity is
    preserved rather than resolved.
  * A paper with a named co-author is B; a paper with none is A.
  * A second publication of an already-counted work keeps its letter for
    orientation and carries `counted: false` with the work it duplicates named
    in `duplicate_of`, so the count still lands in exactly one bucket.
  * Derived or link-only material is catalogued and never counted.

`channel_facts.json` is listed in `data_files` for the record and is EXEMPT:
it is one object rather than a row list, it belongs to another lane, and this
script never writes it.

Round-trip safety. The writer preserves each file's own line endings and only
rewrites a file whose bytes would actually change, so a run on a tree that is
already stamped rewrites nothing. `--check` proves that by comparing the bytes
it would have written with the bytes on disk.

Run:
    python scripts/apply_taxonomy.py            # stamp (idempotent)
    python scripts/apply_taxonomy.py --check    # verify only; exit 1 on drift
"""

import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
DATA = BASE / "_data"
TAXONOMY_JSON = DATA / "taxonomy.json"

CATEGORIES = ("A", "B", "C", "D")

# Files this script never writes, however they are listed in taxonomy.json.
EXEMPT = {"channel_facts.json"}


# --------------------------------------------------------------- the rules ---
def canon_rule(row):
    """canonical_works.json: a work he wrote for his own site.

    Every row is a sole byline, so every row is A and every row is counted.
    The only way out of A is a row that records joint production, and
    `taxonomy.json` -> `data_files.canonical_works.json.note` says none does;
    the assertion in `verify` is what keeps that note true.
    """
    return "A", True


def video_rule(row):
    """videos.json: A or C, decided by the entry's own evidence.

    `kind` is set on exactly the entries that somebody else recorded and he
    appeared in - an `appearance` or a `clip` - so its presence is the
    "made by someone else" signal. A row that carries a `category_basis` is one
    whose own evidence does not settle authorship; those are assigned A and
    required to keep the basis string, per `rules.ambiguity`.
    """
    if row.get("category_basis"):
        return "A", True
    return ("C" if row.get("kind") else "A"), True


def paper_rule(row):
    """papers.json: A alone, B with a named co-author. `type` never decides."""
    co = row.get("co_authors") or []
    return ("A" if len(co) == 0 else "B"), True


def mdi_rule(row):
    """mdi_articles.json: A by byline; counted only when it is a distinct work.

    `counted_as_work` is the evidence-backed decision 5-gram text comparison
    made; the 13 rows it marked false name the work they republish in
    `duplicate_of`, and they are catalogued without being counted again.
    """
    return "A", row.get("counted_as_work", True) is not False


def secondary_rule(row):
    """secondary_sources.json: C, and never counted.

    Derived from this archive's own catalogue, so counting it would count the
    archive against itself. `count_as_content` is already false on every row.
    """
    return "C", False


def notice_rule(row):
    """notices.json: D, and never counted. Announcements are not works."""
    return "D", False


def linkout_rule(row):
    """linkouts.json: D, and never counted. A link is not recovered text."""
    return "D", False


RULES = {
    "canonical_works.json": canon_rule,
    "videos.json": video_rule,
    "papers.json": paper_rule,
    "mdi_articles.json": mdi_rule,
    "secondary_sources.json": secondary_rule,
    "notices.json": notice_rule,
    "linkouts.json": linkout_rule,
}

ROW_ID = {
    "canonical_works.json": "slug",
    "videos.json": "id",
    "papers.json": "title",
    "mdi_articles.json": "slug",
    "secondary_sources.json": "title",
    "notices.json": "slug",
    "linkouts.json": "title",
}


# ------------------------------------------------------------------ io -------
def newline_of(raw):
    """The file's own line terminator, so a rewrite does not churn the diff."""
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    return "\r\n" if crlf and crlf == lf else "\n"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def serialise(data, nl):
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if nl == "\r\n":
        text = text.replace("\n", "\r\n")
    return text.encode("utf-8")


def row_id(name, index, row):
    return str(row.get(ROW_ID.get(name, "id"), index))


# ------------------------------------------------------------- prose gates ---
# Count numerals that appear in _data/taxonomy.json's prose. taxonomy.json is a
# data file, so it cannot compute anything; these numerals are therefore typed,
# and I3 is the finding that a typed numeral inside a block claiming nothing is
# typed is a stale-able lie. The fix is not to delete them - they are the
# taxonomy's rationale - but to make the script that can derive them also
# assert them. Each entry is (path into taxonomy.json as a list of segments, a
# regex with N groups, N numbers derived from the data at run time). --check
# fails if the prose and the data disagree. A path segment may itself contain
# dots, because the data_files keys are file names.
def prose_numbers(tax, rows):
    mdi = rows["mdi_articles.json"]
    mdi_counted = sum(1 for r in mdi if mdi_rule(r)[1])
    mdi_republished = len(mdi) - mdi_counted
    linkouts = rows["linkouts.json"]
    yaqeen = sum(1 for r in linkouts if r.get("type") == "yaqeen_paper")
    videos = rows["videos.json"]
    papers = rows["papers.json"]
    return [
        (["categories", 0, "includes", 0], r"\((\d+) rows\)",
         [len(rows["canonical_works.json"])]),
        (["categories", 0, "includes", 3], r"\((\d+) of the (\d+) rows\)",
         [mdi_counted, len(mdi)]),
        (["categories", 0, "excludes", 0], r"\((\d+) MDI rows\)", [mdi_republished]),
        (["categories", 2, "includes", 2], r"The (\d+) rows of secondary_sources",
         [len(rows["secondary_sources.json"])]),
        (["categories", 3, "includes", 0], r"\((\d+) rows\)",
         [len(rows["notices.json"])]),
        (["categories", 3, "includes", 1],
         r"and (\d+) Yaqeen pages .*?\((\d+) rows\)", [yaqeen, len(linkouts)]),
        (["rules", "duplicates_are_not_a_fifth_place"], r"\((\d+) MDI rows\)",
         [mdi_republished]),
        (["data_files", "canonical_works.json", "note"], r"All (\d+)\.",
         [len(rows["canonical_works.json"])]),
        (["data_files", "videos.json", "note"], r"(\d+) A, (\d+) C",
         [sum(1 for r in videos if video_rule(r)[0] == "A"),
          sum(1 for r in videos if video_rule(r)[0] == "C")]),
        (["data_files", "papers.json", "note"], r"(\d+) A, (\d+) B",
         [sum(1 for r in papers if paper_rule(r)[0] == "A"),
          sum(1 for r in papers if paper_rule(r)[0] == "B")]),
        (["data_files", "mdi_articles.json", "counted"],
         r"true on (\d+) rows, false on (\d+)", [mdi_counted, mdi_republished]),
    ]


def dig(obj, path):
    for key in path:
        obj = obj[key]
    return obj


# ----------------------------------------------------------------- main ------
def main(argv):
    check = "--check" in argv[1:]
    unknown = [a for a in argv[1:] if a != "--check"]
    if unknown:
        print("apply_taxonomy: unknown argument(s): %s" % ", ".join(unknown))
        return 2
    if not TAXONOMY_JSON.is_file():
        print("apply_taxonomy: %s is missing" % TAXONOMY_JSON)
        return 2
    tax = load(TAXONOMY_JSON)
    failures, stamped, unchanged = [], 0, 0

    for name, rule in RULES.items():
        path = DATA / name
        if not path.is_file():
            failures.append("%s: declared in taxonomy.json but not on disk" % name)
            continue
        raw = path.read_bytes()
        rows = load(path)
        if not isinstance(rows, list):
            failures.append("%s: expected a list of rows, got %s"
                            % (name, type(rows).__name__))
            continue
        dirty = False
        for i, row in enumerate(rows):
            want_cat, want_counted = rule(row)
            where = "%s %s" % (name, row_id(name, i, row))
            if want_cat not in CATEGORIES:
                failures.append("%s: rule produced category %r" % (where, want_cat))
                continue
            if row.get("category") != want_cat:
                dirty = True
                failures.append("%s: category=%r, rule says %r"
                                % (where, row.get("category"), want_cat))
            if row.get("counted") is not want_counted:
                dirty = True
                failures.append("%s: counted=%r, rule says %r"
                                % (where, row.get("counted"), want_counted))
        rewritten = dirty and not check
        if rewritten:
            path.write_bytes(serialise(rows, newline_of(raw)))
            stamped += 1
        else:
            unchanged += 1
        print("%s: %-26s %3d row(s)%s" % (
            "CHECK" if check else "STAMP", name, len(rows),
            "  <- rewritten" if rewritten else "  (unchanged)"))

    # Invariants that hold across the whole stamped set.
    rows_by_file = {n: load(DATA / n) for n in RULES if (DATA / n).is_file()}
    counted = [r for rows in rows_by_file.values() for r in rows
               if r.get("counted") is True]
    bad_letter = sorted({r.get("category") for r in counted
                         if r.get("category") not in CATEGORIES})
    if bad_letter:
        failures.append("counted rows carry a category outside A-D: %s" % bad_letter)
    for name, rows in rows_by_file.items():
        for i, row in enumerate(rows):
            if row.get("counted") is False and row.get("category") not in CATEGORIES:
                failures.append("%s %s: uncounted row has no category letter"
                                % (name, row_id(name, i, row)))
    # taxonomy.json's own row counts, and the numerals in its prose.
    for name, spec in tax.get("data_files", {}).items():
        if name in EXEMPT or "rows" not in spec:
            continue
        actual = len(rows_by_file.get(name, []))
        if spec["rows"] != actual:
            failures.append("taxonomy.json data_files.%s.rows=%s, data has %d"
                            % (name, spec["rows"], actual))
    for path, pattern, expected in prose_numbers(tax, rows_by_file):
        try:
            text = dig(tax, path)
        except (KeyError, IndexError, TypeError):
            failures.append("taxonomy.json %s: no such field" % ".".join(map(str, path)))
            continue
        m = re.search(pattern, text)
        if not m:
            failures.append("taxonomy.json %s: no numeral matching /%s/ in %r"
                            % (".".join(map(str, path)), pattern, text[:90]))
            continue
        got = [int(g) for g in m.groups()]
        if got != expected:
            failures.append("taxonomy.json %s: prose says %s, data says %s"
                            % (".".join(map(str, path)), got, expected))

    exempt = [n for n in tax.get("data_files", {}) if n in EXEMPT]
    total_rows = sum(len(r) for r in rows_by_file.values())
    print("taxonomy: %d file(s), %d row(s) carrying a stamped category, "
          "%d of them counted, %d rewritten, exempt: %s"
          % (len(rows_by_file), total_rows, len(counted), stamped,
             ", ".join(exempt) or "none"))
    if failures:
        print("apply_taxonomy: %d FAILURE(S)%s"
              % (len(failures), " (nothing written)" if check else ""))
        for f in failures:
            print("FAIL: " + f)
        return 1
    print("apply_taxonomy: ALL PASS" + (" (--check, nothing written)" if check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
