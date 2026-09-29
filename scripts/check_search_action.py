"""Check that the SearchAction query template is one the search page honours.

`_includes/jsonld.html` declares the archive as a `WebSite` with a
`SearchAction` whose `urlTemplate` is `/search/?q={search_term_string}`.

The single-sited `view_` gates in `scripts/` and the `test_*.py` suites contain
no reference to `SearchAction` or `urlTemplate` at all. That node was therefore
uncovered by every assertion in the repository, and it went on asserting
something untrue: `/search/` read its query from `searchInput.value` and ignored
the parameter, so following the template as a consumer would - substituting the
term exactly as instructed - landed on a live page with an empty box, the
placeholder prompt, and no results. No error, no redirect, nothing to
distinguish it from a site with nothing to find.

That is the failure mode this file exists to prevent, and it is a specific one:
the two halves of one claim, in two files, that can drift apart silently. Any
one of these is a regression:

  * `urlTemplate` renamed `?q=` to `?query=` and search.md still reads `q`
  * search.md drops the `applyQueryParam()` call
  * search.md reads the param but stops calling `performSearch()`
  * the call moves above `loaded = true`, where it silently returns

So this asserts the correspondence, not the presence of either half. Checking
only that both exist would have passed on the broken version that motivated
this.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
JSONLD = ROOT / "_includes" / "jsonld.html"
SEARCH = ROOT / "search.md"

# The urlTemplate is never written as a literal URL in the source. jsonld.html
# assembles it: a `raw` capture holds the `q={search_term_string}` placeholder,
# and `search_url` concatenates it onto "/search/?". That construction exists
# because Liquid's tokenizer ends a variable at a SINGLE closing brace, so
# `?q={search_term_string}` written inline would truncate the whole `{{ ... }}`
# - the reason is documented at jsonld.html:38-43.
PLACEHOLDER = re.compile(r"(\w+)\s*=\s*\{search_term_string\}")
SEP_STRING = re.compile(r'append:\s*"/search/\?')
READS_PARAM = re.compile(r"URLSearchParams\([^)]*\)\.get\(\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*\)")
SETS_INPUT = re.compile(r"searchInput\.value\s*=\s*q\s*;")
CALLS_SEARCH = re.compile(r"performSearch\(\s*\)\s*;")
LOADED_TRUE = re.compile(r"loaded\s*=\s*true\s*;")
EARLY_RETURN = re.compile(r"function\s+performSearch\s*\([^)]*\)\s*\{\s*(?://[^\n]*\n\s*)*if\s*\(\s*!\s*loaded\s*\)\s*return\s*;")


def strip_comments(text: str) -> str:
    """Remove Liquid comment blocks and HTML comments before matching.

    This is not tidiness, it is a bug this file shipped with. The first version
    matched `{search_term_string}` anywhere in jsonld.html - and the comment
    explaining the placeholder contains the literal string
    `/search/?q={search_term_string}`. So the gate read its answer out of its own
    documentation: renaming the real parameter to `?query=` left the comment
    untouched, the gate kept finding `q` in the comment, and it reported the two
    halves matched when they no longer did. Three of five mutations slipped past
    for this reason.

    A gate must read the code, never the prose about the code.
    """
    text = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"(?m)^\s*#(?!\!).*$", "", text)  # YAML comments
    return text


def main() -> int:
    fails: list[str] = []

    for p in (JSONLD, SEARCH):
        if not p.exists():
            print(f"FAIL: missing {p.relative_to(ROOT)}")
            return 1

    jsonld = strip_comments(JSONLD.read_text(encoding="utf-8"))
    search = strip_comments(SEARCH.read_text(encoding="utf-8"))

    # 1. the template must exist and name a parameter
    if not SEP_STRING.search(jsonld):
        fails.append("_includes/jsonld.html no longer builds the urlTemplate from "
                     '"/search/?" + q={search_term_string}, so there is nothing '
                     "for search.md to honour")
    tmpl = PLACEHOLDER.search(jsonld)
    if not tmpl:
        fails.append("_includes/jsonld.html declares no {search_term_string} "
                     "placeholder, so there is nothing for search.md to honour")
        print("check_search_action: 1 problem(s)")
        for f in fails:
            print(f"FAIL: {f}")
        return 1
    param = tmpl.group(1)
    print(f"  declared urlTemplate param : ?{param}")

    # 2. search.md must read exactly that parameter
    reads = set(READS_PARAM.findall(search))
    if not reads:
        fails.append("search.md reads no query parameter at all - the "
                     f"SearchAction advertises ?{param} and the page ignores it")
    elif param not in reads:
        fails.append(f"search.md reads {sorted(reads)} but jsonld.html advertises "
                     f"?{param}; the template cannot be honoured")
    else:
        print(f"  search.md reads             : {param}")

    # 3. reading it is not enough - it has to be used
    if reads:
        if not SETS_INPUT.search(search):
            fails.append("search.md reads the parameter but never assigns it to "
                         "the search input")
        if not CALLS_SEARCH.search(search):
            fails.append("search.md reads the parameter but never calls "
                         "performSearch()")
        if not LOADED_TRUE.search(search):
            fails.append("search.md has no `loaded = true`, so the ordering that "
                         "makes the call safe cannot be checked")

    # 4. the call must exist, and must be after the load rather than before it.
    #    Presence is checked first: without it, a removed call reads as position
    #    -1 and gets reported as the much more confusing "called BEFORE loaded".
    call = search.rfind("applyQueryParam();")
    if reads:
        if call < 0:
            fails.append("search.md never calls applyQueryParam(), so the "
                         f"?{param} in the SearchAction is read by nothing")
        else:
            loaded = search.rfind("loaded = true;")
            fn = search.rfind("function applyQueryParam")
            if EARLY_RETURN.search(search) and fn > 0 and loaded > 0 and call < loaded:
                fails.append("applyQueryParam() is called BEFORE `loaded = true`; "
                             "performSearch() returns immediately when !loaded, "
                             "so the search would silently run against nothing")

    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        print(f"check_search_action: {len(fails)} problem(s)")
        return 1

    print("  performSearch() guarded     : if (!loaded) return  (so order matters)")
    print("  call site                   : after `loaded = true`")
    print("check_search_action: 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
