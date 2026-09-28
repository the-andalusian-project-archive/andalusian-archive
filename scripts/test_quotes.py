#!/usr/bin/env python3
"""Verify every quote in the topic layer is real.

WHY THIS EXISTS. The topic specs under `_data/topics/*.json` were written by eight
independent research agents, each instructed to read the ACTUAL material and to
cite verbatim quotes carrying a `path:line` reference. Nothing forced them to
comply. This suite does.

A quote passes only if all of the following hold:
  * the cited `path` exists in the repository;
  * the `quote` appears VERBATIM, after whitespace normalisation, beginning at the
    cited line in that file.

It also checks that every `supports` label names a query that actually exists in
the same file's query buckets, so no claim can be attached to invented search
terms.

A fabricated quote in a published archive is a serious failure: it puts words in a
living person's mouth, on a page whose entire purpose is to be trustworthy. This
is the check that makes the topic layer safe to publish.

Usage:  python scripts/test_quotes.py
Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOPIC_DIR = ROOT / "_data" / "topics"
QUOTES = TOPIC_DIR / "*.json"

# Markdown hard-wraps, so a verbatim quote of a sentence is routinely split across
# three or four lines - and a long transcript passage can run past 1,400
# characters across dozens of lines. The window therefore has to be sized from the
# quote, not fixed. Thirty characters per line is deliberately conservative for
# wrapped prose: anything tighter under-counts the lines a quote needs and reports
# a real quote as missing.
CHARS_PER_LINE = 30
MIN_WINDOW = 12

BUCKETS = ("head", "mid", "long_tail", "question_forms", "ai_phrased")


def window_for(quote: str) -> int:
    """How many source lines a quote of this length can possibly span."""
    return max(MIN_WINDOW, -(-len(quote) // CHARS_PER_LINE) + 4)


def norm(text: str) -> str:
    """Collapse all whitespace so markdown line-wrapping cannot hide a mismatch."""
    return re.sub(r"\s+", " ", text).strip()


def load_specs() -> list[tuple[pathlib.Path, dict]]:
    specs = []
    for path in sorted(TOPIC_DIR.glob("*.json")):
        specs.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return specs


def check_pages() -> list[str]:
    """Each generated cluster page must carry its own shelf, not another's."""
    problems: list[str] = []
    tax_path = ROOT / "_data" / "topic_taxonomy.json"
    if not tax_path.exists():
        return ["_data/topic_taxonomy.json missing - run scripts/build_topic_pages.py"]

    tax = json.loads(tax_path.read_text(encoding="utf-8"))
    href_re = re.compile(r'<a href="\{\{ site\.baseurl \}\}([^"]+)"')

    claimed: set[str] = set()
    for cluster in tax["clusters"]:
        page = ROOT / "topics" / f"{cluster['id']}.md"
        if not page.exists():
            problems.append(f"{cluster['id']}: topics/{cluster['id']}.md not generated")
            continue
        html = page.read_text(encoding="utf-8")
        start = html.find("<h2>Everything else on this subject</h2>")
        end = html.find("<h2>Everything in this cluster</h2>")
        block = html[start:end] if (start >= 0 and end > start) else ""
        found = set(href_re.findall(block))
        expected = {s["url"] for s in cluster.get("shelf") or []}
        if found != expected:
            problems.append(
                f"{cluster['id']}: shelf on the page ({len(found)}) does not match "
                f"the taxonomy ({len(expected)}); "
                f"unexpected={sorted(found - expected)[:3]} missing={sorted(expected - found)[:3]}"
            )
        claimed |= expected

    # The catch-all must be the exact remainder: an item listed on both a subject
    # page and the miscellany page is counted twice, which is the exact error the
    # four-category taxonomy exists to prevent.
    misc_path = ROOT / "topics" / "miscellany.md"
    if misc_path.exists():
        misc = set(href_re.findall(misc_path.read_text(encoding="utf-8")))
        both = misc & claimed
        if both:
            problems.append(
                f"miscellany lists {len(both)} item(s) that a subject page also "
                f"claims: {sorted(both)[:3]}"
            )

    # ---- the byline gate must hold on the generated pages -------------------
    #
    # Four items in this corpus are bylined to other people - a guest
    # contributor, the other man also called Al-Andalusi, and a republication of
    # someone else's paper - while their front matter claims the subject. A
    # review found eight substantial passages by the other Al-Andalusi published
    # as the subject's answers, including the sharpest line on the terrorism page.
    # Nothing else in the pipeline could see it: the quotes are genuine, they are
    # in the right files, and they verify. So the gate is asserted here.
    for _spec_path, spec in load_specs():
        cid = spec.get("id")
        for item in spec.get("material") or []:
            why = gate_reason(item.get("path", ""))
            if not why:
                continue
            slug = item.get("slug", "?")
            page = ROOT / "topics" / f"{cid}.md"
            if not page.exists():
                continue
            html = page.read_text(encoding="utf-8")
            for claim in item.get("key_claims") or []:
                quote = re.sub(r"\s+", " ", claim.get("quote", "")).strip()
                if len(quote) < 60:
                    continue
                if quote[:120] in re.sub(r"\s+", " ", html):
                    problems.append(
                        f"{cid}/{slug}: a passage by ANOTHER AUTHOR is rendered as "
                        f"the subject's ({why}). Bylined material must not be "
                        f"quoted on a subject page."
                    )
                    break

    # ---- the material table must actually render ---------------------------
    #
    # The rows were markdown pipes inside a raw <table>, which kramdown does not
    # parse; the browser foster-parented the text out and every subject page
    # shipped a header-only table with a run-on line of raw markdown above it.
    # Nothing caught it because the suite read the markdown source, not the
    # built page.
    for _p2, spec in load_specs():
        cid = spec.get("id")
        page = ROOT / "topics" / f"{cid}.md"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        m = re.search(
            r"<h2>Everything in this cluster</h2>(.*?)</table>", html, re.S
        )
        if not m:
            problems.append(f"{cid}: no material table found")
            continue
        rows = m.group(1).count("<tr>")
        expected = len(spec.get("material") or []) + 1
        if rows != expected:
            problems.append(
                f"{cid}: material table has {rows} <tr>, expected {expected} "
                f"(1 header + {len(spec.get('material') or [])} items)"
            )
    return problems


def gate_reason(path: str) -> str:
    """Why this source is not the subject's own words, or "" if it is.

    Deliberately a re-implementation rather than an import: test_quotes.py must
    not depend on the generator it is testing, or a bug in the generator's
    authorship logic would silence the check on itself. It reads the BYLINE in
    the post body, because three of these posts carry
    `author: "Asadullah Ali Al-Andalusi"` in front matter while the body says
    someone else - the archive's own written rule is that a row counts as his on
    the strength of the byline, never on the strength of a title or a key.
    """
    if not path:
        return ""
    target = ROOT / path
    if not target.exists():
        return ""
    body = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "",
                  target.read_text(encoding="utf-8", errors="replace"),
                  count=1, flags=re.S)
    for line in body.splitlines()[:40]:
        s = line.strip()
        low = s.lower()
        if re.match(r"^(by|written by)\s+\S", s, re.I):
            if "abdullah al-andalusi" in low or "as-sufi" in low or "as sufi" in low:
                return s
            if "asadullah" in low:
                return ""
        if "this is a response by" in low:
            return s
    return ""


def check() -> int:
    specs = load_specs()
    if not specs:
        print("no topic specs found under _data/topics/", file=sys.stderr)
        return 1

    failures: list[str] = []
    checked = 0
    total_quotes = 0
    total_queries = 0
    total_material = 0

    for path, spec in specs:
        cluster = spec.get("id", path.stem)
        queries: set[str] = set()
        buckets = spec.get("queries") or {}
        for bucket in BUCKETS:
            for q in buckets.get(bucket) or []:
                if isinstance(q, str):
                    queries.add(norm(q))
        total_queries += len(queries)

        material = spec.get("material") or []
        total_material += len(material)

        for item in material:
            slug = item.get("slug", "?")
            src = item.get("path", "")
            claims = item.get("key_claims") or []

            target = ROOT / src
            if not src:
                failures.append(f"{cluster}/{slug}: no path")
                continue
            if not target.exists():
                failures.append(f"{cluster}/{slug}: path does not exist: {src}")
                continue

            lines = target.read_text(encoding="utf-8", errors="replace").splitlines()

            if not claims:
                # An availability record quoted for the archive's own status line
                # is legitimate; it just must not pretend to carry prose.
                continue

            for claim in claims:
                total_quotes += 1
                checked += 1
                quote = claim.get("quote", "")
                ref = claim.get("ref", "")
                supports = claim.get("supports", "")

                m = re.match(r"^(.*):(\d+)$", ref)
                if not m:
                    failures.append(f"{cluster}/{slug}: malformed ref {ref!r}")
                    continue
                ref_path, ref_line = m.group(1), int(m.group(2))

                if ref_path.replace("\\", "/") != src.replace("\\", "/"):
                    failures.append(
                        f"{cluster}/{slug}: ref {ref!r} does not match path {src!r}"
                    )
                    continue

                if not (1 <= ref_line <= len(lines)):
                    failures.append(
                        f"{cluster}/{slug}: ref line {ref_line} out of range "
                        f"({len(lines)} lines)"
                    )
                    continue

                window = norm(" ".join(lines[ref_line - 1 : ref_line - 1 + window_for(quote)]))
                needle = norm(quote)

                if not needle:
                    failures.append(f"{cluster}/{slug}: empty quote at {ref}")
                elif needle not in window:
                    failures.append(
                        f"{cluster}/{slug}: QUOTE NOT FOUND at {ref} -> "
                        f"{needle[:70]!r}"
                    )

                if supports and norm(supports) not in queries:
                    failures.append(
                        f"{cluster}/{slug}: supports {supports[:50]!r} is not a "
                        f"declared query"
                    )

    print(f"topic specs      : {len(specs)}")
    print(f"material items   : {total_material}")
    print(f"quotes verified  : {checked}")
    print(f"queries declared : {total_queries}")

    # ---- the generated pages must match the taxonomy they were built from ----
    #
    # This exists because of a real bug. The shelf on each page is built from the
    # cluster's tag matches, and the shelf block was computed in the loop that
    # writes `_data/topic_taxonomy.json` and consumed in the loop that writes the
    # page. Same variable name, two loops, so every page rendered the shelf of
    # whichever cluster happened to run last - and the taxonomy was correct the
    # whole time, which is exactly what made it hard to see.
    failures.extend(check_pages())

    if failures:
        print()
        print(f"TEST_FAIL: {len(failures)} problem(s)", file=sys.stderr)
        for f in failures[:60]:
            print(f"  {f}", file=sys.stderr)
        if len(failures) > 60:
            print(f"  ... and {len(failures) - 60} more", file=sys.stderr)
        return 1

    print("TEST_PASS: every quote resolves verbatim at its cited line")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
