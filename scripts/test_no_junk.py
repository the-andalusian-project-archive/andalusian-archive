#!/usr/bin/env python3
"""CI gate: nothing that should not reach a reader reaches a reader.

Two legs, same idea.

1. `_posts/*.md` carries no ad/JS/tracking junk (Q5A - FAILS on any match).

   Covers WordPress.com ad/tracking artifacts observed 2026-09-07:
   __ATA/initAd/cmd.push/initSlot, wpcom_adclk_*, jQuery(, setTimeout(function,
   stat_gif/pixel.wp.com beacons, getElementById('crt-*), Criteo, atatags,
   new Image().src=document beacons.

2. `_site/**/*.html` names no internal path that does not exist after the
   recovery finishes (2026-09-27, task 8f, Phase-3 review I4).

   The recovery staged ~144 MB of raw captures under the gitignored `_staging/`,
   which is deleted at Task 9.5. The published channel page was printing 32
   `_staging/...` payload paths in its evidence column, so a reader was pointed
   at a file that will not exist - and 8b's own report claimed the page cited
   timestamps, not files. `docs/` was the same class of leak and reached
   `_site/` verbatim until it was excluded in `_config.yml` (R27).

   A path in reader-facing prose is only a citation if it resolves, so the
   rendered HTML is checked directly. When `_site/` does not exist the leg
   prints SKIP and says so; run `bundle exec jekyll build` first to gate it.
   `_data/` is allowed to keep such pointers, because nothing serves it: the
   per-row local filename and the staging-path index stay there for re-checking
   a claim against the Wayback Machine by capture timestamp.

Run: `python scripts/test_no_junk.py`. Exit 0 PASS, 1 FAIL.
"""

import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent.parent

PATTERNS = [
    r"__ATA", r"initAd", r"cmd\.push", r"initSlot", r"atatags",
    r"wpcom_", r"GA_google", r"googleAddAdSense", r"googleFillSlot", r"jQuery\(",
    r"setTimeout\(function",
    r"stat_gif", r"pixel\.wp\.com", r"getElementById",
    r"Criteo", r"new Image\(\)",
]

# Working-tree paths that must never appear in a rendered page. Each is
# (label, pattern); the boundary in the pattern matters, because "transcripts/"
# contains "scripts/" and "/docs/" is the leak R27 closed.
#
# `_posts/` and `scripts/` are deliberately NOT here. Both name files that exist
# in this repository for as long as the repository does, and both are named in
# reader-facing prose on purpose: an MDI page says which local post a text
# comparison was made against, and /search/ says which builder makes its detail
# pages. That is provenance, not a dangling citation. What is gated is the class
# that misleads: a path to something that is deleted at Task 9.5, or a tree the
# site excludes and therefore cannot serve.
LEAKS = [
    ("_staging/", r"_staging/"),
    (".superpowers/", r"\.superpowers/"),
    (".firecrawl/", r"\.firecrawl/"),
    ("docs/", r"""(?:^|[\s"'(\[>=/])docs/"""),
    ("node_modules/", r"node_modules/"),
    ("vendor/", r"""(?:^|[\s"'(\[>=/])vendor/"""),
]
LEAK_RE = [(label, re.compile(pat, re.M)) for label, pat in LEAKS]


def scan_posts(failures):
    for path in sorted((BASE / "_posts").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        hits = sorted({p for p in PATTERNS if re.search(p, text)})
        if hits:
            failures.append("%s: %s" % (path.name, hits))
            print("FAIL: %s: %s" % (path.name, hits))
    n = len(list((BASE / "_posts").glob("*.md")))
    if not failures:
        print("test_no_junk: %d _posts file(s) clean" % n)
    return n


def scan_site(failures):
    site = BASE / "_site"
    if not site.is_dir():
        print("SKIP: _site/ does not exist, so the rendered pages are not gated - "
              "run `bundle exec jekyll build` first")
        return 0
    pages = sorted(site.rglob("*.html"))
    for path in pages:
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = sorted({label for label, rx in LEAK_RE if rx.search(text)})
        if hits:
            rel = path.relative_to(site).as_posix()
            failures.append("_site/%s: %s" % (rel, hits))
            print("FAIL: _site/%s: %s" % (rel, hits))
    if not any(f.startswith("_site/") for f in failures):
        print("test_no_junk: %d rendered page(s) name no internal path that "
              "Task 9 deletes (%s)" % (len(pages),
                                       ", ".join(l for l, _ in LEAKS[:4]) + ", ..."))
    return len(pages)


def main():
    failures = []
    scan_posts(failures)
    scan_site(failures)
    if failures:
        print("test_no_junk: %d FAILURE(S)" % len(failures))
        return 1
    print("test_no_junk: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
