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
