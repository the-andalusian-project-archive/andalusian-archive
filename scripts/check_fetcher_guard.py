"""The fetcher must not be able to write damage into the corpus.

`_write_canonical_file` and `refetch_existing_post` call
`_assert_fetch_is_clean` before writing, which raises if the fetched body still
trips an automatic residue or chrome rule in `fetch_damage.py`.

Two things can silently undo that, and neither shows up in a build:

  1. The guard stops being called. A third write path is added, or one of the
     two calls is removed, and the fetcher is free again.
  2. The guard stops agreeing with the detector. `fetch_damage.py` gains a rule,
     or loses one, and the fetcher's idea of "clean" drifts from the archive's -
     which is the exact failure that produced the 287-hit triage in the first
     place, because the fetcher's stripper list and the damage rules were two
     independent lists that fell out of step.

So this checks the call sites exist AND that the guard really rejects. The
second half is the part that matters: a guard which has never rejected anything
is a comment.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

ROOT = pathlib.Path(__file__).resolve().parent.parent
FETCHER = ROOT / "scripts" / "fetch_blog_content.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _stub_http_dependencies() -> list[str]:
    """Stub `bs4` and `requests` so the fetcher imports without them.

    The first version of this gate imported `fetch_blog_content` directly and
    worked locally, then failed in CI with

        ModuleNotFoundError: No module named 'bs4'

    - because the fetcher imports BeautifulSoup and requests at module level for
    the network fetching it does, and CI installs neither. The guard being tested
    touches no HTTP at all: it scans a string. So the dependencies are the wrong
    thing for this gate to require, and installing BeautifulSoup in CI to assert
    a string pattern would be a poor trade.

    The stubs are installed only if the real modules are absent, so a developer
    with the full environment exercises the real imports. If a stub is ever
    needed for something the guard actually uses, the failure will be an obvious
    AttributeError rather than a silent behaviour difference.
    """
    stubbed: list[str] = []

    if importlib.util.find_spec("bs4") is None:
        bs4 = types.ModuleType("bs4")

        class _Unused:
            def __init__(self, *a, **k):  # pragma: no cover - never called
                raise RuntimeError(
                    "BeautifulSoup is stubbed; this gate must not parse HTML")

        bs4.BeautifulSoup = _Unused
        bs4.XMLParsedAsHTMLWarning = type("XMLParsedAsHTMLWarning", (Warning,), {})
        sys.modules["bs4"] = bs4
        stubbed.append("bs4")

    if importlib.util.find_spec("requests") is None:
        requests = types.ModuleType("requests")

        class _UnusedSession:
            def __init__(self, *a, **k):  # pragma: no cover - never called
                raise RuntimeError(
                    "requests is stubbed; this gate must not make HTTP calls")

        requests.Session = _UnusedSession
        requests.exceptions = types.ModuleType("requests.exceptions")
        sys.modules["requests"] = requests
        sys.modules["requests.exceptions"] = requests.exceptions
        stubbed.append("requests")

    return stubbed

# Bodies that MUST be refused. Each was verified against `fetch_damage.py`
# before being used here - an earlier draft of this file guessed at the shapes
# and two of the three were not detected at all, so the guard passed them and
# the gate correctly reported a failure. A sample for a test has to be a
# sample the detector actually fires on, not one that merely looks alarming.
# These cover both automatic classes: residue (machine text in the body) and
# chrome (WordPress furniture in the body). No sentence the author wrote can
# look like them, which is the whole basis for refusing the write.
DAMAGED = {
    "ad payload block": (
        "The argument stands.\n"
        "    writeAd({\n"
        '      adSlot: "x",\n'
        "    });\n"
        "More text here.\n"),

    "orphaned JS terminators": (
        "Real sentence.\n"
        "}\n"
        ")\n"
        "}\n"
        "Another sentence.\n"),

    "injected stylesheet and script": (
        "Real sentence.\n"
        ".ad-123 { color: red; }\n"
        "var q = 1;\n"
        "var w = 2;\n"
        "Another sentence.\n"),

    "comment count in the body": (
        "Real sentence.\n"
        "2 Comments\n"
        "Another sentence.\n"),
}

# A real paragraph, and a real paragraph using characters the judgement rules
# watch for. Both must pass: the guard filters on `automatic`, so a curly quote
# must not block a write.
CLEAN = {
    "plain prose": "He argued the position clearly, and the second reading "
                   "follows from the first without further assumption.\n",
    "curly quotes and em dash": "\u201cThis is the point,\u201d he said \u2014 and "
                                "he was right about it, which is rare.\n",
    "empty": "",
    "whitespace only": "   \n\n  \n",
}


def main() -> int:
    stubbed = _stub_http_dependencies()
    import fetch_blog_content as F
    if stubbed:
        print(f"  stubbed for this run            : {', '.join(stubbed)}")

    fails: list[str] = []

    src = FETCHER.read_text(encoding="utf-8")

    # 1. every write of post content must be guarded.
    #
    #    Counting call sites and requiring >= 2 is not enough. An earlier
    #    version of this check did exactly that, and a mutation adding a THIRD
    #    write path with no guard passed it: the count went up, not down, and
    #    the unguarded path was invisible. The invariant that actually matters
    #    is per-write, not per-count - every `f.write(` of a body must have a
    #    guard call immediately above it.
    lines = src.split("\n")
    writes: list[tuple[int, str]] = []
    for i, ln in enumerate(lines):
        stripped = ln.lstrip()
        if not stripped.startswith("f.write("):
            continue
        # front-matter assembly writes are not body writes only if they do not
        # reference content_md; both real sites do.
        writes.append((i, ln))

    guarded = 0
    for i, ln in writes:
        window = "\n".join(lines[max(0, i - 3):i])
        if "_assert_fetch_is_clean(" in window:
            guarded += 1
        else:
            fails.append(f"scripts/fetch_blog_content.py:{i + 1} writes post "
                         "content with no _assert_fetch_is_clean() guard above it: "
                         f"{ln.strip()[:60]}")

    calls = sum(1 for ln in lines
                if ln.lstrip().startswith("_assert_fetch_is_clean(")
                and not ln.lstrip().startswith("def "))
    if calls < guarded:
        fails.append(f"{calls} guard call(s) for {guarded} guarded write(s) - "
                     "a guard call is being counted twice")

    # 2. the guard must exist and be reachable
    if not hasattr(F, "_assert_fetch_is_clean"):
        fails.append("fetch_blog_content has no _assert_fetch_is_clean")
        print(f"check_fetcher_guard: {len(fails)} problem(s)")
        for f in fails:
            print(f"FAIL: {f}")
        return 1

    guard = F._assert_fetch_is_clean

    # 3. damaged bodies must be refused
    for name, body in DAMAGED.items():
        try:
            guard(body, "test-slug", "<memory>")
        except ValueError:
            pass
        except Exception as exc:
            fails.append(f"{name}: guard raised {type(exc).__name__} instead of "
                         f"ValueError: {exc}")
        else:
            fails.append(f"{name}: the fetcher would have written a body the "
                         "damage detector flags")

    # 4. clean bodies must pass
    for name, body in CLEAN.items():
        try:
            guard(body, "test-slug", "<memory>")
        except Exception as exc:
            fails.append(f"{name}: guard REJECTED legitimate recovered text "
                         f"({type(exc).__name__}: {str(exc)[:60]})")

    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        print(f"check_fetcher_guard: {len(fails)} problem(s)")
        return 1

    print(f"  post-content writes          : {len(writes)}")
    print(f"  of which guarded             : {guarded}")
    print(f"  damaged bodies refused       : {len(DAMAGED)}")
    print(f"  legitimate bodies accepted   : {len(CLEAN)}")
    print("check_fetcher_guard: 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
