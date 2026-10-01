"""A broad validity check on the sitemap, beyond "every URL was built".

`scripts/check_sitemap.py` proves one thing: every URL the sitemap advertises
corresponds to a file the build produced. That is the property that was broken,
and it is the one worth failing a deploy over. This script is the wider sweep,
run against the LIVE site, and it exists because "the sitemap is valid" means
more than that.

It checks, against production:

  1. XML WELL-FORMEDNESS. Parsed, not regex-matched. A sitemap that does not
     parse is not a sitemap.
  2. Sitemap protocol shape. `<urlset>`, 50 KB / 50,000-URL limits, absolute
     URLs, HTTPS.
  3. DUPLICATES, including case-insensitively and after unquoting - a sitemap
     listing the same page twice in two casings advertises one page as two.
  4. THE TWO KNOWN URL SHAPES: legacy permalinks containing an apostrophe, and
     anything with a space or other character that must be percent-encoded.
  5. NO STRAY ENTITIES. `&apos;` was a real 404 here; any XML entity other than
     the three predefined ones, or a bare `&`, is suspect.
  6. LIVE REACHABILITY. Every URL fetched. This is the check that would have
     caught the `&apos;` bug on the day it shipped, and it is the reason this
     script exists rather than another source-level assertion.
  7. COVERAGE. Sitemap against the site's real pages. A sitemap that omits half
     the site is valid and useless.
  8. `robots.txt` CONSISTENCY. Whether the sitemap it advertises is the one
     actually published, and whether the host root serves one at all.
  9. `lastmod` FORMAT where present - W3C datetime, not a filename.

Network-dependent findings are labelled, not assumed: an unreachable URL is
reported as UNREACHABLE and never folded into a pass or a fail count, because a
timeout is a fact about the network and not about the sitemap.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE = "https://the-andalusian-project-archive.github.io"
BASE = f"{SITE}/andalusian-archive"
UA = "andalusian-archive-sitemap-audit/1.0 (+sitemap validity check)"
TIMEOUT = 45

# 50 MB, the documented protocol limit (52,428,800 bytes) - NOT 50 KB.
#
# The first version of this script set 50 * 1024 and reported the 85,876-byte
# sitemap as a protocol violation, which would have justified splitting it into
# a sitemap index: a real refactor of the one file every crawler reads, taken on
# the strength of a limit invented here. The actual limit, per sitemaps.org and
# Google Search Central, is 50 MB uncompressed. The sitemap is 0.08 MB.
#
# A checker that states a limit it cannot cite will eventually be believed.
MAX_BYTES = 52_428_800
MAX_URLS = 50000

#: The only entities an XML document may use without a DTD. Anything else in a
#: sitemap is a bug that happens to render.
PREDEFINED = {"amp", "lt", "gt", "quot", "apos"}


def get(url: str) -> tuple[int, str, str]:
    """Return (status, body, error). status 0 means the request never completed."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Range": "bytes=0-200000"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", errors="replace"), ""
    except urllib.error.HTTPError as e:
        return e.code, "", f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return 0, "", type(e).__name__


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="fetch every URL over the network (default: structure only)")
    args = ap.parse_args()

    sm_url = f"{BASE}/sitemap.xml"
    status, body, err = get(sm_url)
    print(f"sitemap validity  {sm_url}")
    print()

    # 206 as well as 200: the Range header above makes GitHub Pages answer a
    # partial content, and a 206 is a complete sitemap for our purposes. The
    # first version demanded exactly 200 and failed the whole audit over it.
    if status not in (200, 206):
        print(f"FAIL: sitemap did not return 200/206 (status {status}, {err})")
        return 1

    problems: list[str] = []
    notes: list[str] = []
    unreachable = 0

    # 1 + 2. parses, and the shape is a sitemap
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print(f"FAIL: sitemap is not well-formed XML: {e}")
        return 1
    print(f"  [1] well-formed XML          : yes ({len(body):,} bytes)")

    if not root.tag.endswith("urlset"):
        problems.append(f"root element is {root.tag!r}, expected a urlset")
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [e.text.strip() for e in root.iter(f"{ns}loc") if e.text]
    if not locs:
        problems.append("no <loc> elements found")
    print(f"  [2] root <urlset>, {len(locs)} <loc>: "
          f"{'yes' if root.tag.endswith('urlset') and locs else 'NO'}")

    if len(body) > MAX_BYTES:
        problems.append(f"{len(body):,} bytes exceeds the 50 MB (52,428,800) protocol limit")
    if len(locs) > MAX_URLS:
        problems.append(f"{len(locs)} URLs exceeds the 50,000 limit")

    # 3. duplicates, case-insensitively and after unquoting
    raw_dupes = [u for u, n in collections.Counter(locs).items() if n > 1]
    norm = [urllib.parse.unquote(u) for u in locs]
    norm_dupes = [u for u, n in collections.Counter(norm).items() if n > 1]
    lower = [u.lower() for u in norm]
    lower_dupes = [u for u, n in collections.Counter(lower).items() if n > 1]
    for label, dupes in (("exact", raw_dupes), ("after unquoting", norm_dupes),
                         ("case-insensitively", lower_dupes)):
        if dupes:
            problems.append(f"{len(dupes)} duplicate URL(s) {label}, e.g. {dupes[0]}")
    print(f"  [3] duplicates               : "
          f"{len(raw_dupes) + len(norm_dupes) + len(lower_dupes)}")

    # 4. the apostrophe shape that broke, and encoding in general
    apos = [u for u in locs if "qur%27an" in u.lower() or "qur'an" in u]
    bad_enc = [u for u in locs if "'" in u or " " in u]
    for u in bad_enc:
        problems.append(f"URL needs percent-encoding and does not have it: {u}")
    print(f"  [4] apostrophe permalinks    : {len(apos)} "
          f"({'%27 encoded' if all('%27' in u for u in apos) else 'RAW APOSTROPHE'})")

    # 5. stray entities
    ents = re.findall(r"&([A-Za-z][A-Za-z0-9]*);", body)
    stray = sorted({e for e in ents if e not in PREDEFINED})
    if stray:
        problems.append(f"non-predefined XML entit(ies) in the sitemap: {stray}")
    bare_amp = len(re.findall(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", body))
    if bare_amp:
        problems.append(f"{bare_amp} bare `&` with no entity - the XML is only "
                        "parseable by accident")
    print(f"  [5] stray entities / bare &  : {len(stray)} / {bare_amp}")

    # 9. lastmod format
    lastmods = [e.text.strip() for e in root.iter(f"{ns}lastmod") if e.text]
    bad_lm = [m for m in lastmods
              if not re.match(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}"
                              r"([+-]\d{2}:\d{2}|Z))?$", m)]
    for m in bad_lm[:3]:
        problems.append(f"lastmod is not a W3C datetime: {m}")
    print(f"  [9] lastmod present/valid    : {len(lastmods)} / {len(lastmods) - len(bad_lm)}")

    # 6. live reachability
    if args.live:
        print()
        print("  [6] live fetch of every URL ...")
        bad: list[tuple[int, str, str]] = []
        for u in locs:
            st, _, e = get(u)
            if st in (200, 206):
                continue
            if st == 0:
                unreachable += 1
                notes.append(f"UNREACHABLE {u} ({e})")
            else:
                bad.append((st, u, e))
        for st, u, e in bad[:12]:
            problems.append(f"live {st}: {u} ({e})")
        print(f"      200/206     : {len(locs) - len(bad) - unreachable}/{len(locs)}")
        print(f"      4xx/5xx     : {len(bad)}")
        print(f"      unreachable : {unreachable}")
    else:
        print("  [6] live fetch               : skipped (pass --live)")

    # 7. coverage: sitemap against the pages actually built
    #
    # The two sides must be NORMALISED before comparison, and the first version
    # did not, so it reported 22 advertised-but-unbuilt and 23 built-but-
    # unadvertised URLs that were the same 22 pages twice over: the sitemap spells
    # them with `%20` and the filesystem spells them with spaces. This is the
    # same percent-encoding trap `scripts/check_sitemap.py` already handles, met
    # again in a new place.
    site_dir = ROOT / "_site"
    if site_dir.is_dir():
        built: set[str] = set()
        stubs: set[str] = set()
        for p in site_dir.rglob("*.html"):
            rel = urllib.parse.unquote(
                "/" + p.relative_to(site_dir).as_posix().replace("index.html", ""))
            # jekyll-redirect-from emits ~700-byte redirect pages for every
            # `redirect_from` entry. They are NOT pages, and they must not appear
            # in a sitemap - the canonical URL is the target. The first version
            # of this check counted them as "built but not advertised" and
            # reported the identity page as missing from the sitemap when the
            # sitemap had it exactly right.
            try:
                head = p.read_text(encoding="utf-8", errors="replace")[:4000]
            except OSError:
                head = ""
            is_stub = (p.stat().st_size < 4096 and
                       ('http-equiv="refresh"' in head
                        or "Redirecting" in head
                        or "window.location.replace" in head))
            (stubs if is_stub else built).add(rel)

        advertised = {urllib.parse.unquote(urllib.parse.urlparse(u).path)
                      for u in locs}
        base_prefix = "/andalusian-archive"
        advertised = {a[len(base_prefix):] if a.startswith(base_prefix) else a
                      for a in advertised}

        # A sitemap must never advertise a redirect target's alias.
        stub_advertised = sorted(advertised & stubs)

        missing = sorted(u for u in advertised if u not in built)
        extra = sorted(b for b in built if b not in advertised and b.count("/") > 1
                       and not b.startswith(("/topics", "/search", "/feed", "/llms",
                                            "/assets", "/_", "/.")))
        print(f"  [7] built real pages        : {len(built)}")
        print(f"      redirect stubs (skipped): {len(stubs)}")
        print(f"      advertised in the sitemap: {len(advertised)}")
        print(f"      advertised but not built : {len(missing)}")
        print(f"      built but not advertised : {len(extra)}")
        for m in missing[:5]:
            problems.append(f"advertised but no such built page: {m}")
        for s in stub_advertised[:5]:
            problems.append(f"the sitemap advertises a REDIRECT STUB: {s}. "
                            "Advertise the canonical target instead.")
        for e in extra[:5]:
            notes.append(f"built but not in the sitemap: {e}")

    # 8. robots.txt consistency
    print()
    for label, u in (("site  ", f"{BASE}/robots.txt"), ("host root", f"{SITE}/robots.txt")):
        st, b, e = get(u)
        if st not in (200, 206):
            notes.append(f"robots.txt ({label}) did not return 200: {st or e}")
            continue
        declared = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", b)
        print(f"  [8] robots.txt ({label})    : 200, {len(declared)} Sitemap line(s)")
        for d in declared:
            if urllib.parse.urlparse(d).path.rstrip("/") != "/andalusian-archive/sitemap.xml":
                problems.append(f"robots.txt ({label}) advertises {d}, which is "
                                "not the published sitemap")

    # ---- report
    print()
    for n in notes[:14]:
        print(f"NOTE: {n}")
    if len(notes) > 14:
        print(f"NOTE: ... and {len(notes) - 14} more")
    if problems:
        print()
        for p in problems:
            print(f"FAIL: {p}")
        print(f"\nsitemap validity: {len(problems)} problem(s), "
              f"{len(notes)} note(s), {unreachable} unreachable")
        return 1
    print(f"sitemap validity: 0 problems, {len(notes)} note(s), "
          f"{unreachable} unreachable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
