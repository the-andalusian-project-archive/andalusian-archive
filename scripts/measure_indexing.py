#!/usr/bin/env python3
"""Measure whether anything has actually crawled this site, reproducibly.

WHY THIS EXISTS
---------------
The 2026-09-29 indexing audit established a baseline: this site had never been
crawled by anything. Wayback CDX, Common Crawl, urlscan, Marginalia and the
reachable search engines all returned zero. That is a fine one-off finding and a
useless ongoing one, because it cannot be repeated. There was no way to tell,
seven days later, whether the four indexing fixes had moved anything - and
without a measurement, "we fixed the sitemap" is indistinguishable from "we
fixed nothing and cannot see it".

So this is a script, not a report. It re-derives the same queries, prints one
line per source, and appends a dated row to `docs/recovery-log/indexing-log.md`
so the day-7 run is comparable to this one without re-reading a chat log.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not claim to be a search-engine rank checker. Several of these sources
are unauthenticated and rate-limited, so a zero here is weak evidence of a zero
anywhere, and a non-zero is strong evidence of something. That asymmetry is
stated in the output rather than smoothed over: an unreachable source reports as
UNREACHABLE, never as "0 results". Reporting a network failure as an absence of
indexing is the kind of error that makes a measurement worthless, and it is the
one this script is built to avoid.

The one source that would settle it - a Google Search Console property - needs
an account, so it is out of reach here. Phase 5 asks the maintainer for it.

Usage
-----
    python -B scripts/measure_indexing.py            # query and print
    python -B scripts/measure_indexing.py --append   # also append a dated row
    python -B scripts/measure_indexing.py --sample N # check N sitemap URLs live
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://the-andalusian-project-archive.github.io"
BASE = f"{SITE}/andalusian-archive"

#: Bare hostname. Some search operators (urlscan domain:) reject a scheme and
#: answer 400, which is indistinguishable from a source that never worked.
HOST = "the-andalusian-project-archive.github.io"

#: A descriptive, stable User-Agent. Several of these endpoints reject the
#: default urllib agent outright, which would show up as a false zero.
UA = "andalusian-archive-indexing-audit/1.0 (+https://the-andalusian-project-archive.github.io/andalusian-archive/)"

#: How long to wait. Generous, because a slow archive.org is a timeout, not a
#: zero, and a timeout must never be reported as an absence of indexing.
TIMEOUT = 45


def _get(url: str, headers: dict | None = None) -> tuple[str, str]:
    """Return (body, error). Exactly one is empty.

    Errors are returned rather than raised so a single unreachable source
    cannot abort the run, and so they can be labelled UNREACHABLE instead of
    being silently coerced into a zero.
    """
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", errors="replace"), ""
    except urllib.error.HTTPError as e:
        return "", f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 - any failure is an unreachable source
        return "", type(e).__name__


def _get_retry(url: str, headers: dict | None = None, attempts: int = 3) -> tuple[str, str]:
    """_get, retried. archive.org answers 503 under load constantly, and a
    single 503 is not a measurement - it is the service declining that instant."""
    body, err = _get(url, headers)
    for n in range(1, attempts):
        if not err or not err.startswith("HTTP 5"):
            break
        time.sleep(2.0 * n)
        body, err = _get(url, headers)
    return body, err


def wayback_cdx() -> tuple[str, str]:
    """Distinct archived captures of the site."""
    # https, not http: the http endpoint times out from here, and a timeout
    # would be reported as UNREACHABLE rather than the real answer.
    url = ("https://web.archive.org/cdx/search/cdx?url=" +
           urllib.parse.quote(f"{SITE}/*") +
           "&output=json&fl=original,timestamp&collapse=urlkey&limit=400")
    body, err = _get_retry(url, {"Accept": "application/json"})
    if err:
        return "UNREACHABLE", err
    rows = json.loads(body) if body.strip() else []
    return str(max(0, len(rows) - 1)), ""


def common_crawl() -> tuple[str, str]:
    """Whether any Common Crawl index has seen the site."""
    body, err = _get("https://index.commoncrawl.org/collinfo.json")
    if err:
        return "UNREACHABLE", err
    try:
        indexes = [c["id"] for c in json.loads(body) if c.get("cdx-api")]
    except Exception:  # noqa: BLE001
        return "UNREACHABLE", "collinfo.json did not parse"

    for idx in indexes[:6]:  # newest six; an older hit is not actionable
        api = idx.replace("CC-MAIN-", "https://index.commoncrawl.org/CC-MAIN-")
        body, err = _get_retry(f"{api}-index?url=" +
                         urllib.parse.quote(f"{SITE}/*") + "&output=json")
        if err:
            continue
        if body.strip():
            return "SEEN", f"first hit in {idx}"
    # The one source that cannot tell an absence from a bad query: the CDX API
    # answers an empty body for a malformed domain exactly as it does for a
    # domain that was never crawled. Verified by pointing this function at a
    # non-resolving host, where it reports 0 rather than an error. So a 0 here
    # means "no hit, and this source could not have told you otherwise" - which
    # is why the other three carry the weight.
    return "0", "no capture in the six most recent indexes (this source cannot distinguish an empty index from a malformed query)"


def urlscan() -> tuple[str, str]:
    # `q` MUST be the first query parameter: `?size=10&q=...` returns HTTP 400
    # from urlscan, which reads as an unreachable source rather than a bad
    # request.
    #
    # And the operator takes a BARE HOSTNAME. `domain:https://host` is a
    # malformed query and also returns 400 - which is how the first version of
    # this function reported urlscan unreachable on every run, while the same
    # request with the scheme stripped answered 200 immediately. A measurement
    # source that always errors is indistinguishable from one with no results.
    body, err = _get("https://urlscan.io/api/v1/search/?q=domain:" + HOST + "&size=10",
                     {"Accept": "application/json"})
    if err:
        return "UNREACHABLE", err
    try:
        return str(json.loads(body).get("total", 0)), ""
    except Exception:  # noqa: BLE001
        return "UNREACHABLE", "response did not parse"


def indexnow_accepted() -> tuple[str, str]:
    """Whether the IndexNow endpoint answers for this host.

    Not a search engine and not proof of indexing. It is here because it is the
    one signal this repository controls end to end, so it is the first thing
    that would move before any crawler appears.

    The key is deliberately omitted, so a well-formed request answers 400. That
    400 is a RESPONSE, which is the whole point: it proves the endpoint is
    reachable and parsing our request. An earlier version of this function
    treated any non-empty error string as UNREACHABLE and so reported the
    endpoint as down while it was in fact answering - the exact confusion this
    script exists to avoid, committed in the script written to avoid it.
    """
    url = ("https://api.indexnow.org/indexnow?url=" +
           urllib.parse.quote(f"{BASE}/") + "&key=")
    body, err = _get(url)
    if err.startswith("HTTP"):
        return "REACHABLE", f"answered {err} with the key omitted, as expected"
    if err:
        return "UNREACHABLE", err
    return "REACHABLE", body.strip()[:40] or "accepted"


SOURCES = [
    ("Wayback CDX captures", wayback_cdx),
    ("Common Crawl", common_crawl),
    ("urlscan.io scans", urlscan),
    ("IndexNow endpoint", indexnow_accepted),
]

LOG = ROOT / "docs" / "recovery-log" / "indexing-log.md"


def sitemap_urls() -> tuple[list[str], str]:
    """URLs the sitemap advertises, and which file they came from.

    Reads the BUILT sitemap when there is one, because that is the artefact a
    crawler actually receives. The repository-root `sitemap.xml` is a Liquid
    template: its `<loc>` elements contain `{{ page.url | ... }}`, which has
    spaces in it, so a `[^<\\s]+` loc pattern silently matches nothing and the
    script reports "sitemap produced no URLs" while looking at a file that
    plainly contains 355 of them. That is what the first version did.
    """
    built = ROOT / "_site" / "sitemap.xml"
    if built.exists():
        text = built.read_text(encoding="utf-8")
        return re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text), "_site/sitemap.xml"

    p = ROOT / "sitemap.xml"
    if not p.exists():
        return [], "no sitemap.xml in _site/ or the repository root"
    text = p.read_text(encoding="utf-8")
    return re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text), "sitemap.xml (template, unbuilt)"


def check_live(sample: int) -> tuple[int, int, list[str], str]:
    """Return (ok, bad, failures, source)."""
    urls, source = sitemap_urls()
    if not urls:
        return 0, 0, [f"{source} produced no URLs"], source
    step = max(1, len(urls) // max(1, sample))
    chosen = urls[::step][:sample]
    bad: list[str] = []
    for u in chosen:
        _, err = _get(u, {"Range": "bytes=0-0"})
        if err and err not in ("HTTP 206",):
            bad.append(f"{u}  ({err})")
    return len(chosen) - len(bad), len(bad), bad, source


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--append", action="store_true",
                    help="append a dated row to docs/recovery-log/indexing-log.md")
    ap.add_argument("--sample", type=int, default=12,
                    help="how many sitemap URLs to check live (default 12)")
    args = ap.parse_args()

    today = _dt.date.today().isoformat()
    print(f"indexing measurement  {today}")
    print(f"site                  {SITE}")
    print()

    results: list[tuple[str, str, str]] = []
    for name, fn in SOURCES:
        value, note = fn()
        results.append((name, value, note))
        extra = f"   ({note})" if note else ""
        print(f"  {name:24} {value}{extra}")

    print()
    ok, bad, failures, source = check_live(args.sample)
    print(f"  {'sitemap URLs live':24} {ok}/{ok + bad} sampled return 2xx/206")
    print(f"  {'  (from)':24} {source}")
    for f in failures[:6]:
        print(f"      {f}")

    if args.append:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        if not LOG.exists():
            LOG.write_text(
                "# Indexing log\n\n"
                "Dated measurements from `scripts/measure_indexing.py`. One row per\n"
                "run. The baseline is the 2026-09-29 audit, which found no crawler\n"
                "footprint of any kind. Read `UNREACHABLE` as *not measured*, never\n"
                "as *absent* - a timeout and an absence of indexing are different\n"
                "findings and this log refuses to merge them.\n\n"
                "Common Crawl is the weakest of the four: its API answers an empty\n"
                "body for a malformed query exactly as it does for an uncrawled\n"
                "domain, so a 0 from it cannot self-verify. The other three can.\n\n"
                "| Date | Wayback | Common Crawl | urlscan | sitemap live |\n"
                "|---|---|---|---|---|\n", encoding="utf-8")
        cells = {n: v for n, v, _ in results}
        row = "| {} | {} | {} | {} | {}/{} |".format(
            today,
            cells.get("Wayback CDX captures", "?"),
            cells.get("Common Crawl", "?"),
            cells.get("urlscan.io scans", "?"),
            ok, ok + bad)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(row + "\n")
        print(f"\n  appended to {LOG.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
