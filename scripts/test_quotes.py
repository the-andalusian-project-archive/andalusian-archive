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
from html import unescape
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


def check_pages(total_queries: int = 0) -> list[str]:
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
    # ---- llms.txt must not drift from the data ---------------------------
    #
    # llms.txt is hand-maintained and states "731 questions". Every other count
    # on the site is computed at build time, so this one number was the only
    # figure on the site that could silently go stale - and it is the figure an
    # AI summariser is most likely to quote back.
    llms = ROOT / "llms.txt"
    if llms.exists():
        text = llms.read_text(encoding="utf-8")
        stated = re.search(r"(\d+)\s+questions", text)
        if stated is None:
            problems.append("llms.txt: no question count found to check")
        elif int(stated.group(1)) != total_queries:
            problems.append(
                f"llms.txt states {stated.group(1)} questions; the cluster specs "
                f"declare {total_queries}. Update the number or the specs."
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

                window_lines = window_for(quote)
                window = norm(" ".join(lines[ref_line - 1 : ref_line - 1 + window_lines]))
                needle = norm(quote)

                if not needle:
                    failures.append(f"{cluster}/{slug}: empty quote at {ref}")
                elif needle not in window:
                    failures.append(
                        f"{cluster}/{slug}: QUOTE NOT FOUND at {ref} -> "
                        f"{needle[:70]!r}"
                    )
                else:
                    # The window extends FORWARD, so `in` is satisfied by a match
                    # anywhere inside it, not necessarily at the cited line. That
                    # looseness is invisible in the common case and a review
                    # measured it at zero - but the docstring claims the quote
                    # begins at the cited line, so it is now enforced.
                    #
                    # The whole file is normalised LINE BY LINE, recording where
                    # each line begins in the normalised string, so a match index
                    # maps back to an exact line. Mapping proportionally instead
                    # - start/len(flat)*len(raw) - is wrong, because collapsing
                    # whitespace changes the length of a line by an amount that
                    # is not uniform across the file.
                    #
                    # A quotation may legitimately begin partway through a line, so
                    # the cited line must be one of the lines the quote occupies,
                    # not necessarily its first.
                    #
                    # `flat` is built the same way the window is built - one
                    # normalised string for the whole file - and the offsets are
                    # derived from it by walking the lines in order. An earlier
                    # version joined the per-line normalisations and searched
                    # that, which disagreed with the window on every file
                    # containing a blank line: joining ["a","","b"] gives "a  b"
                    # while normalising the joined string gives "a b", so a quote
                    # spanning the blank line matched the window and not this.
                    flat = norm("\n".join(lines))
                    offsets: list[int] = []
                    pos = 0
                    for ln in lines:
                        offsets.append(pos)
                        n = norm(ln)
                        if n:
                            pos += len(n) + 1

                    occupied: set[int] = set()
                    start = flat.find(needle)
                    while start != -1:
                        lo, hi = 0, len(offsets) - 1
                        while lo < hi:
                            mid = (lo + hi + 1) // 2
                            if offsets[mid] <= start:
                                lo = mid
                            else:
                                hi = mid - 1
                        occupied.add(lo + 1)
                        start = flat.find(needle, start + 1)

                    if ref_line not in occupied:
                        where = sorted(occupied)[:4] or ["nowhere in the file"]
                        failures.append(
                            f"{cluster}/{slug}: quote cited at line {ref_line} "
                            f"actually occurs on line(s) {where}"
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
    failures.extend(check_pages(total_queries))
    failures.extend(check_palette())
    failures.extend(check_measure())

    # ---- third-party source relationships -----------------------------------
    #
    # The 70 records in _data/secondary_sources.json were, until this layer
    # existed, written to disk and never rendered: a private index of other
    # people's writing, invisible to readers. Now that /sources/ exists, three
    # things have to hold at once. Every record must be published. Every
    # relates_to target must name an item that actually exists - a relation to a
    # non-existent page is a link to a 404, which is worse than no link. And the
    # reverse index must agree with the forward one, because _includes/
    # secondary_links.html reads only the reverse index, so a disagreement shows
    # up as a silently missing back-reference rather than as an error.
    # ---- recordings of an item --------------------------------------------
    #
    # A reader who opened a work or paper was shown one route to the material
    # and it led to a private YouTube embed, while the archive held a verified
    # preserved copy and mentioned it nowhere on that page. Every recording in
    # _data/videos.json has such a copy, so every link emitted here must have
    # one: a link to a video page whose own download is dead would move the
    # problem rather than fix it.
    rec = json.loads((ROOT / "_data" / "recording_links.json").read_text(encoding="utf-8"))
    vids = {v.get("id"): v for v in json.loads(
        (ROOT / "_data" / "videos.json").read_text(encoding="utf-8"))}
    by_url = rec.get("by_url", {})
    for perm, links in by_url.items():
        for l in links:
            vid = l.get("video_id")
            if vid not in vids:
                failures.append(
                    f"recording_links.json: {perm} points at video {vid!r} which "
                    f"is not in videos.json")
                continue
            if not l.get("archive_url"):
                failures.append(
                    f"recording_links.json: {perm} -> {vid} has no preserved copy, "
                    f"so the block would offer no watchable route")
            if perm not in _collection_permalinks():
                failures.append(
                    f"recording_links.json: {perm} is not a collection permalink")
    print(f"recordings linked: {len(by_url)} items, "
          f"{sum(len(v) for v in by_url.values())} recordings")

    # ---- every archive_url emission site must escape the fragment ------------
    #
    # A STATIC check, and the one that matters, because the CI gates run before
    # `jekyll build`: a check that reads the built output is skipped in CI
    # entirely. Two attempts at a build-output check were both useless — the
    # first was never exercised in CI, and the second passed *vacuously* when a
    # deliberately broken template made the build fail and leave the previous
    # good `_site` in place. Neither would have caught the regression.
    #
    # The defect is a missing `replace: '#', '%23'` in a template, so assert on
    # the templates. Jekyll's `uri_escape` is
    # `Addressable::URI.normalize_component`: it percent-encodes spaces and
    # non-ASCII but leaves `#` alone, and a fragment is never transmitted to the
    # server. Six Internet Archive filenames contain a literal `#` ("Book
    # Recommendations #1"), so a missing replace is six live pages with a dead
    # Download button.
    for tmpl in sorted(list((ROOT / "_layouts").glob("*.html"))
                       + list((ROOT / "_includes").glob("*.html"))
                       + [p for p in ROOT.glob("*.md") if p.is_file()]):
        try:
            text = tmpl.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in re.finditer(r"\{\{([^}]*archive_url[^}]*)\}\}", text):
            expr = m.group(1)
            if "replace: '#', '%23'" in expr:
                continue
            # jsonify/escape_once are attribute-safety filters, not encoders.
            if "archive_url | uri_escape" in expr:
                rel = tmpl.relative_to(ROOT).as_posix()
                failures.append(
                    f"{rel}: an archive_url is emitted with uri_escape but no "
                    f"'#' replacement, so filenames containing '#' 404: "
                    f"{{{{{expr}}}}}"
                )
    print("archive_url emission sites checked : all templates")

    # And the rendered output, when a build is present, for the shapes a static
    # check cannot see.
    built = ROOT / "_site"
    if built.is_dir():
        attr = re.compile(r'(href|content)="([^"]*)"')
        bad_syntax = 0
        checked = 0
        for f in built.rglob("*.html"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            for m in attr.finditer(t):
                u = unescape(m.group(2))
                if "archive.org/download" not in u:
                    continue
                checked += 1
                # An entity-encoded apostrophe is legitimate HTML; a literal
                # space or `#` in a filename is not a requestable URL.
                for ch, why in ((" ", "raw space"), ("#", "raw # (a fragment is "
                                                          "never sent to the "
                                                          "server)")):
                    if ch in u:
                        bad_syntax += 1
                        rel = f.relative_to(built).as_posix()
                        failures.append(
                            f"rendered href: {rel} emits a {why}: "
                            f"...{u[-64:]}")
                        if bad_syntax > 8:
                            break
        print(f"download hrefs checked : {checked}")
    else:
        print("download hrefs checked : 0 (no _site; run jekyll build first)")

    failures.extend(check_secondary_sources())

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


_PERMALINK_CACHE: set[str] | None = None


def _collection_permalinks() -> set[str]:
    """Every permalink the collections declare, read from front matter.

    Deliberately independent of `_site`. The CI gates run before
    `jekyll build`, so a check that reads the build output fails on a clean
    checkout with every page reported missing. Front matter is what generates
    those permalinks, so it is the authority worth asserting against.

    Three ways a naive regex here goes wrong, all of which would let a
    fabricated relation target pass, so the front matter is located by its
    delimiters and only that span is searched:

      * `^permalink:` matches a BODY line, so a page whose front matter is
        short or absent injects whatever `permalink:` string appears in its
        text into the valid set.
      * `[^"'\\s]+` truncates a quoted permalink that contains a space, so the
        real value is lost and the truncated one is admitted.
      * A fixed-size head window silently loses the permalink of any file with
        a long front matter block.
    """
    global _PERMALINK_CACHE
    if _PERMALINK_CACHE is not None:
        return _PERMALINK_CACHE

    out: set[str] = set()
    for folder in ("_articles", "_papers", "_videos", "_transcripts"):
        d = ROOT / folder
        if not d.is_dir():
            continue
        for f in d.glob("*.md"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            head = text[:end]
            for m in re.finditer(r"^permalink:[ \t]*(\S.*?)[ \t]*$", head, re.M):
                val = m.group(1).strip().strip("\"'")
                val = val.rstrip("/") + "/"
                # A permalink is a path. Anything containing whitespace, a
                # scheme or a quote is a body line that slipped through.
                if re.fullmatch(r"/[A-Za-z0-9/._~%()\-]*", val):
                    out.add(val)
    _PERMALINK_CACHE = out
    return out


def _front_matter_urls() -> dict[str, str]:
    """Every external URL in collection front matter, mapped to its permalink.

    Used by the check that a third-party record may not be published as
    "related to no archive item" when its own URL is the source the archive
    recorded for an item it holds. Without this the archive states something
    false about its own holdings, which is the one class of error this project
    exists not to make.
    """
    found: dict[str, str] = {}
    for folder in ("_articles", "_papers", "_videos", "_transcripts"):
        d = ROOT / folder
        if not d.is_dir():
            continue
        for f in d.glob("*.md"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            head = text[:end]
            # Reuse the hardened parser rather than a second, looser regex.
            # The two disagreed on quoted or spaced permalinks, which is how a
            # helper ends up quietly checking something other than what the
            # other helper checks.
            pm = re.search(r"^permalink:[ \t]*(\S.*?)[ \t]*$", head, re.M)
            if not pm:
                continue
            perm = pm.group(1).strip().strip("\"'").rstrip("/") + "/"
            for u in re.findall(r"https?://[^\s\"'<>]+", head):
                found.setdefault(u.rstrip("/").lower(), perm)
    return found


def check_secondary_sources() -> list[str]:
    """Third-party records: all published, all targets real, index in agreement."""
    failures: list[str] = []

    rows = json.loads((ROOT / "_data" / "secondary_sources.json").read_text(encoding="utf-8"))
    rows = rows if isinstance(rows, list) else list(rows.values())[0]
    index = json.loads((ROOT / "_data" / "secondary_links.json").read_text(encoding="utf-8"))

    # 1. Every record with a URL is published on /sources/. A record with no URL
    #    is a metadata row and is allowed, but there should not be many of them.
    #    Compare on the unescaped form: the page writes `&amp;` into hrefs, which
    #    is correct HTML, so a raw comparison fails for every tracking-parameter
    #    URL and would read as "27 records were dropped from the page".
    page = (ROOT / "sources.md").read_text(encoding="utf-8")
    published = {unescape(u) for u in
                 re.findall(r'<a href="(https?://[^"]+)"', page)}
    for r in rows:
        url = r.get("url")
        if not url:
            failures.append(f"secondary_sources: {r.get('title', '?')!r} has no url")
            continue
        if url not in published:
            failures.append(
                f"secondary_sources: {r.get('title', '?')[:60]!r} is not published "
                f"on /sources/ (url {url[:70]})"
            )

    # 2. Every relates_to target must resolve to a real page. Permalinks are
    #    checked against the collection files' own front matter, NOT against
    #    _site. CI runs this gate before `jekyll build`, so anything that reads
    #    _site fails on a clean checkout with every page reported as missing -
    #    which is exactly how the first version of this check failed. Front
    #    matter is the authority that generates those permalinks, so it is also
    #    the right thing to assert against: a slug that disagrees with the
    #    collection would ship as a 404.
    valid = _collection_permalinks()
    for r in rows:
        seen: set[tuple[str, str]] = set()
        for rel in r.get("relates_to") or []:
            sig = (rel.get("kind", ""), rel.get("ref", ""))
            if sig in seen:
                failures.append(
                    f"secondary_sources: {r.get('title', '?')[:50]!r} relates to "
                    f"{sig} twice"
                )
                continue
            seen.add(sig)
            pl = rel.get("permalink") or ""
            if not pl:
                failures.append(
                    f"secondary_sources: {r.get('title', '?')[:50]!r} relates to "
                    f"{sig} with no permalink"
                )
                continue
            if pl not in valid:
                failures.append(
                    f"secondary_sources: {r.get('title', '?')[:50]!r} relates to "
                    f"{sig} -> {pl} which is not a collection permalink"
                )

    # 3. The reverse index must be a faithful mirror of the forward relations.
    #    The include reads only by_url, so a stale index hides back-references
    #    rather than raising.
    forward: dict[str, set[str]] = {}
    for r in rows:
        for rel in r.get("relates_to") or []:
            pl = rel.get("permalink") or ""
            if pl:
                forward.setdefault(pl, set()).add(r.get("url", ""))
    for pl, urls in forward.items():
        got = {n.get("url", "") for n in index.get("by_url", {}).get(pl, [])}
        if urls - got:
            failures.append(
                f"secondary_links.json: {pl} is missing "
                f"{sorted(urls - got)[:2]} from its by_url entry"
            )
    for pl in index.get("by_url", {}):
        if pl not in forward:
            failures.append(
                f"secondary_links.json: by_url has {pl} but no record relates "
                f"to it - the index is stale"
            )

    # 4. THE ONE THAT MATTERS MOST. A record must never be published as having
    #    no established referent when its own URL is the source this archive
    #    recorded for an item it holds. That sentence is an affirmative claim
    #    about the archive's own holdings, and the TOTETU row made it false in
    #    public: the archive holds that exact PDF as paper 7's full text, with
    #    a recorded sha256 proof of byte identity, while /sources/ said no item
    #    was established. Both review agents found this independently.
    fm_urls = _front_matter_urls()
    for r in rows:
        if r.get("relates_to"):
            continue
        url = (r.get("url") or "").rstrip("/").lower()
        if url and url in fm_urls:
            failures.append(
                f"secondary_sources: {r.get('title', '?')[:56]!r} publishes as "
                f"'no single archive item established', but its URL is recorded "
                f"in front matter for {fm_urls[url]}"
            )

    print(f"third-party records: {len(rows)} "
          f"({sum(1 for r in rows if r.get('relates_to'))} with a referent, "
          f"{sum(1 for r in rows if not r.get('relates_to'))} without)")
    print(f"reverse index      : {len(index.get('by_url', {}))} items")
    return failures


# The token pairs the redesign declares. Kept as literal data in the gate rather
# than parsed out of the stylesheet, so a careless token edit fails the build
# instead of quietly lowering the contrast floor with it.
#
# Token names are the file's existing `--color-*` names. All 2,400-odd lines of
# style.css reference them, so renaming would be a find/replace with no upside;
# changing the values restyles the site and leaves every untouched rule valid.
PALETTE_TEXT_PAIRS = [
    ("--color-text", "--color-bg"),
    ("--color-text", "--color-surface"),
    ("--color-text", "--color-surface-sunken"),
    ("--color-text", "--color-primary-subtle"),
    ("--color-text-secondary", "--color-bg"),
    ("--color-text-secondary", "--color-surface"),
    ("--color-text-secondary", "--color-surface-sunken"),
    ("--color-text-secondary", "--color-primary-subtle"),
    ("--color-primary", "--color-bg"),
    ("--color-primary", "--color-surface"),
    ("--color-primary", "--color-surface-sunken"),
    ("--color-primary", "--color-primary-subtle"),
    ("--color-primary-hover", "--color-bg"),
    ("--color-primary-hover", "--color-surface"),
    ("--color-success", "--color-bg"),
    ("--color-success", "--color-surface"),
    ("--color-success", "--color-surface-sunken"),
    ("--color-warning", "--color-bg"),
    ("--color-warning", "--color-surface"),
    ("--color-warning", "--color-surface-sunken"),
    ("--color-danger", "--color-bg"),
    ("--color-danger", "--color-surface"),
    ("--color-danger", "--color-surface-sunken"),
]
# Hairline rules are decorative dividers, so they take a visibility floor rather
# than the 3:1 of WCAG 1.4.11. 3:1 would force a divider to be visually heavy,
# which is the opposite of the design the three references use.
PALETTE_RULE_PAIRS = [
    ("--color-border", "--color-bg"),
    ("--color-border-strong", "--color-bg"),
]
TEXT_MIN = 4.5
RULE_MIN = 1.4

# The accent is SEP's red, measured rgb(140, 21, 21). Pinned explicitly because
# the first measurement to surface was the teal that IEP and Goodreads share,
# and a later edit back to it should be a deliberate decision, not a slip.
ACCENT_EXPECTED = {"light": "#8c1515", "dark": "#e08a8a"}


def _srgb_lum(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        ch.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _contrast(a: str, b: str) -> float:
    la, lb = _srgb_lum(a), _srgb_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _read_vars(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", block):
        out[m.group(1)] = m.group(2)
    return out


def check_palette() -> list[str]:
    """Every declared token pair clears its floor, in BOTH themes."""
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    failures: list[str] = []

    start = css.index(":root {")
    light = _read_vars(css[start:css.index("}", start) + 1])

    dm = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\n  \}",
                   css, re.S)
    if not dm:
        return ["style.css: no prefers-color-scheme dark :root block found"]
    dark = _read_vars(dm.group(1))
    for k, v in light.items():
        dark.setdefault(k, v)

    needed = ({n for n, _ in PALETTE_TEXT_PAIRS}
              | {n for n, _ in PALETTE_RULE_PAIRS})
    missing = sorted(needed - set(light))
    if missing:
        failures.append(f"style.css: tokens not declared in :root: {missing}")

    for theme_name, T in (("light", light), ("dark", dark)):
        for fg, bgn in PALETTE_TEXT_PAIRS:
            if fg not in T or bgn not in T:
                continue
            r = _contrast(T[fg], T[bgn])
            if r < TEXT_MIN:
                failures.append(
                    f"contrast {theme_name}: {fg} on {bgn} = {r:.2f} "
                    f"(< {TEXT_MIN})")
        for fg, bgn in PALETTE_RULE_PAIRS:
            if fg not in T or bgn not in T:
                continue
            r = _contrast(T[fg], T[bgn])
            if r < RULE_MIN:
                failures.append(
                    f"contrast {theme_name}: {fg} on {bgn} = {r:.2f} "
                    f"(< {RULE_MIN})")
        want = ACCENT_EXPECTED[theme_name]
        got = (T.get("--color-primary") or "").lower()
        if got and got != want:
            failures.append(
                f"style.css {theme_name}: --color-primary is {got}, expected "
                f"{want} (SEP's red)")

    # A palette token re-declared inside a `prefers-color-scheme` query is a
    # trap. The deleted `prefers-color-scheme: light` layer sat AFTER :root, so
    # in light mode it won the cascade and made --measure resolve to 68ch and
    # --color-text-secondary to a cool #545b68 - while this gate, reading the
    # first declaration in the file, reported a clean palette. That is the same
    # class of blind spot as the `_site` check in 1c177ba: validating a
    # declaration instead of the value the cascade resolves to.
    #
    # The dark block is exempt - re-declaring every token there is what a second
    # theme IS. So are width media queries: a token narrowed at 480px cannot
    # override the desktop palette. A *colour-scheme* query can, at every width.
    for qm in re.finditer(
            r"@media[^{]*prefers-color-scheme[^{]*\{(.*?)\n\}", css, re.S):
        if "dark" in qm.group(0)[:120]:
            continue  # the dark theme, which is meant to differ
        for token in sorted(set(re.findall(r"(--[\w-]+):", qm.group(1)))):
            if token in light:
                failures.append(
                    f"style.css: {token} is re-declared inside a "
                    f"prefers-color-scheme query other than the dark block; it "
                    f"wins the cascade and can silently override the palette")

    # The retired Tailwind values must be gone, not merely unused.
    for dead in ("#2563eb", "#7c3aed"):
        if dead in css.lower():
            failures.append(
                f"style.css: {dead} is still present; the old Tailwind palette "
                f"was replaced, not aliased")

    print(f"palette pairs checked : {len(PALETTE_TEXT_PAIRS)} text, "
          f"{len(PALETTE_RULE_PAIRS)} rule, in 2 themes")
    return failures


# 680px at an 18px serif lands near 66 characters, the midpoint of the three
# references (Goodreads 625, IEP 700, SEP 707). Assert a band rather than the
# pixel value so a later --max-width edit cannot quietly re-widen every
# paragraph, which is what an 860px measure did before this redesign.
MEASURE_MIN_CH = 60
MEASURE_MAX_CH = 80
MEASURE_MIN_PX = 620
MEASURE_MAX_PX = 720


def check_measure() -> list[str]:
    """The prose column must stay at a readable line length."""
    failures: list[str] = []
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")

    m = re.search(r"--measure:\s*(\d+)px", css)
    if not m:
        return ["style.css: --measure is not declared"]
    px = int(m.group(1))
    if not (MEASURE_MIN_PX <= px <= MEASURE_MAX_PX):
        failures.append(
            f"style.css: --measure is {px}px, outside the "
            f"{MEASURE_MIN_PX}-{MEASURE_MAX_PX}px band the references use")

    # An UPPER BOUND, deliberately. Georgia's average advance is about 0.5em,
    # so 18px gives ~9px per character, and the rendered text measure is the
    # token minus the container's horizontal padding - 680px renders as 632px,
    # about 70 characters. Reporting the larger number keeps the gate strict
    # rather than optimistic.
    approx_ch = px / 9.0
    if not (MEASURE_MIN_CH <= approx_ch <= MEASURE_MAX_CH):
        failures.append(
            f"measure: {px}px at 18px serif is about {approx_ch:.0f}ch, outside "
            f"{MEASURE_MIN_CH}-{MEASURE_MAX_CH}ch")

    print(f"measure               : {px}px, about {approx_ch:.0f}ch "
          f"(target {MEASURE_MIN_CH}-{MEASURE_MAX_CH}ch)")
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
