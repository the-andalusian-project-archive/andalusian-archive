"""Post-build assertions on the rendered pages.

Every other suite runs BEFORE `jekyll build` and reads the source tree. Nothing
can see the rendered output, which is where the defect that prompted this file
lived: five layouts were changed to render `page.display_title`, a key only the
four GENERATED collections carry, with no fallback. All 54 `_posts` pages then
rendered an EMPTY `<h1>`.

It was invisible for two reasons. The page still looked finished, because the
recovered WordPress export carries its own `<h1>` in the body, so the title was
present one heading level down. And the output was valid HTML. Nothing in the
build failed, so nothing stopped.

So: assert the rendered document, not the source.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

COLLECTIONS = ("articles", "papers", "transcripts", "videos", "topics")

H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
TITLE = re.compile(r"<title>(.*?)</title>", re.S)
CANON = re.compile(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I)
CANON2 = re.compile(r'<link[^>]+href="([^"]+)"[^>]+rel="canonical"', re.I)
DESC = re.compile(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', re.I)
DESC2 = re.compile(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', re.I)
HREFLANG = re.compile(r'hreflang=', re.I)


def text_of(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("&amp;", "&").strip()


def source_newer_than_build() -> list[str]:
    """List source trees whose files are newer than `_site`.

    This exists because of a false green, and it is the most important function
    in the file.

    A `jekyll build` that fails on a Liquid syntax error leaves the previous
    `_site` exactly where it was. The build exits 1, prints to stderr, and the
    stale output is still there to be read. A post-build gate reading `_site`
    then reports the PREVIOUS build's numbers - and reports them as clean.

    That is not hypothetical. It happened here: a `truncate` replacement left a
    stray `endfor` closing an `{% if %}`, every build failed, and this script
    printed "0 problem(s)" three times over an unbuilt site, including a run
    that appeared to prove a description fix had worked. The number it reported
    was stale and the fix had never been rendered.

    So the gate now refuses to answer unless the build it is inspecting is
    newer than the sources that produce it. A stale `_site` is a failure, not a
    pass.
    """
    if not SITE.exists():
        return ["_site/ does not exist"]
    built = SITE.stat().st_mtime
    stale: list[str] = []
    for d in ("_includes", "_layouts", "_data", "_articles", "_papers",
              "_videos", "_transcripts", "_posts", "_config.yml"):
        p = ROOT / d
        if not p.exists():
            continue
        newest = p.stat().st_mtime if p.is_file() else max(
            (f.stat().st_mtime for f in p.rglob("*") if f.is_file()), default=0)
        if newest > built + 1:  # 1s tolerance for filesystem granularity
            stale.append(d)
    return stale


def main() -> int:
    if not SITE.is_dir():
        print("FAIL: no _site/ - run `bundle exec jekyll build` first")
        return 1

    stale = source_newer_than_build()
    if stale:
        print("FAIL: _site is OLDER than the sources that build it, so every")
        print("      number below would be the previous build's. Rebuild first.")
        for d in stale:
            print(f"        stale: {d}")
        print("      (a failed `jekyll build` leaves the old _site in place - this")
        print("       check is what turns that from a false green into a failure)")
        return 1

    pages = [p for d in COLLECTIONS for p in (SITE / d).rglob("*.html")]
    pages += [p for p in (SITE / "topics").glob("*.html")]
    pages = sorted(set(pages))
    if not pages:
        print("FAIL: found no rendered collection pages to check")
        return 1

    fails: list[str] = []
    empty_h1 = 0
    long_titles: list[tuple[str, int]] = []
    cut_descs = 0
    multi_h1 = 0
    no_canon = 0

    for p in pages:
        rel = p.relative_to(SITE).as_posix()
        html = p.read_text(encoding="utf-8", errors="replace")

        h1s = H1.findall(html)
        if h1s and not text_of(h1s[0]):
            empty_h1 += 1
            fails.append(f"{rel}: empty <h1> - a layout asked for a front-matter "
                         f"key this page does not have")
        if len(h1s) > 1:
            multi_h1 += 1

        t = TITLE.search(html)
        if not t or not text_of(t.group(1)):
            fails.append(f"{rel}: missing or empty <title>")
        else:
            n = len(text_of(t.group(1)))
            if n > 60:
                long_titles.append((rel, n))

        m = CANON.search(html) or CANON2.search(html)
        if not m:
            no_canon += 1
            fails.append(f"{rel}: no rel=canonical")

        d = DESC.search(html) or DESC2.search(html)
        if d:
            raw = d.group(1)
            if raw and len(raw) >= 158 and not raw.endswith((".", "…", "?")):
                cut_descs += 1

    print(f"built pages         : {len(pages)} checked under {', '.join(COLLECTIONS)}/")
    print(f"  empty <h1>        : {empty_h1}")
    print(f"  missing canonical : {no_canon}")
    print(f"  title > 60 chars  : {len(long_titles)}  (SERP truncation, reported)")
    print(f"  description cut mid-word at ~160: {cut_descs}  (reported)")
    print(f"  pages with >1 <h1> : {multi_h1}  (imported WordPress headings)")

    if long_titles:
        worst = sorted(long_titles, key=lambda kv: -kv[1])[:3]
        for rel, n in worst:
            print(f"    longest title: {n} chars  {rel[:70]}")

    if fails:
        for f in fails[:20]:
            print(f"FAIL: {f}")
        print(f"check_built_pages  : {len(fails)} problem(s)")
        return 1
    print("check_built_pages  : 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
