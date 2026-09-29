"""Assert the built sitemap promises only URLs that exist.

WHY THIS IS SEPARATE FROM THE OTHER SUITES
===========================================
Every other gate runs BEFORE `jekyll build`, because they read the source
tree. The sitemap only exists after the build, and it is the one place where a
wrong URL is a promise rather than a cosmetic error: a sitemap says "these pages
are here, come and read them", and an entry that 404s spends a crawler's
attention to tell it nothing.

The defect this was written for
-------------------------------
jekyll-sitemap 1.4.0 pipes every URL through `| xml_escape`, which is correct
XML and the wrong URL. Two full-text pages have a legacy permalink containing an
apostrophe, and the escape rendered it as the entity `&apos;`:

    .../articles/qur&apos;an/science/backbone-ribs/     -> 404

The real page is at `.../articles/qur%27an/...` and appeared in no sitemap at
all. Fixed by the custom `sitemap.xml` template in the repository root; this
script is what stops it coming back.

Run after a build. Exits non-zero on any failure.
"""

from __future__ import annotations

import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
SITEMAP = SITE / "sitemap.xml"

#: XML entities that encode characters which belong in a URL path as themselves
#: or as a percent-escape. `&amp;` is legitimate in a query string, so it is
#: reported separately rather than as a failure.
PATH_ENTITIES = re.compile(r"&(?:apos|quot|#0*39|#x0*27);")
AMP = re.compile(r"&amp;")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def baseurl_prefix() -> str:
    """The `baseurl:` from _config.yml, e.g. "/andalusian-archive".

    Needed because sitemap URLs are absolute and therefore carry the baseurl,
    while `_site/` is the build root WITHOUT it. `/andalusian-archive/topics/`
    in the sitemap is `_site/topics/index.html` on disk. Skipping this made all
    355 URLs look unbuilt, which is the failure this script exists to report.
    """
    cfg = ROOT / "_config.yml"
    for line in cfg.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^\s*baseurl:\s*"?([^"\s]*)"?\s*$', line)
        if m:
            return m.group(1).rstrip("/")
    return ""


def main() -> int:
    if not SITEMAP.is_file():
        fail(f"no built sitemap at {SITEMAP.relative_to(ROOT)} - run "
             f"`bundle exec jekyll build` first")
        return 1

    text = SITEMAP.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]*)</loc>", text)
    problems = 0
    prefix = baseurl_prefix()

    if not locs:
        fail("sitemap contains no <loc> entries")
        return 1

    # 1. No path character was entity-encoded instead of percent-encoded.
    for url in locs:
        m = PATH_ENTITIES.search(url)
        if m:
            fail(f"path character entity-encoded instead of percent-encoded: "
                 f"{url}  (found {m.group(0)}; the correct form is %27)")
            problems += 1

    # 2. Every URL resolves to a file that was actually built. This is the check
    #    that would have caught the two dead entries on their own.
    checked = 0
    for url in locs:
        path = urllib.parse.urlsplit(url).path
        if prefix and path.startswith(prefix):
            path = path[len(prefix):]
        # Percent-decode before touching the filesystem. Jekyll writes the
        # directory with a literal space or apostrophe, so `current%20issues/`
        # and `qur%27an/` are `current issues/` and `qur'an/` on disk. 22 of the
        # 355 URLs looked unbuilt until this was added.
        rel = urllib.parse.unquote(path).lstrip("/")
        candidates = [
            SITE / rel,
            SITE / rel / "index.html",
            SITE / (rel + "index.html"),
        ]
        if not any(c.is_file() for c in candidates):
            fail(f"sitemap advertises a URL that was not built: {url}")
            problems += 1
        checked += 1

    # 3. Informational: entities that may be legitimate in a query string.
    amps = [u for u in locs if AMP.search(u)]

    # 4. Every URL is absolute and https, or the sitemap is not portable.
    for url in locs:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "https":
            fail(f"sitemap URL is not https: {url}")
            problems += 1

    print(f"sitemap              : {len(locs)} <loc>, {checked} checked against "
          f"the build, {len(amps)} carrying a query-string &amp;")
    if problems:
        print(f"check_sitemap        : {problems} problem(s)")
        return 1
    print("check_sitemap        : 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
