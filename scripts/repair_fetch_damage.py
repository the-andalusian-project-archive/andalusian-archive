"""Apply the fetch-damage repairs and record every change verbatim.

Run with --apply to write. Without it, this is a dry run that reports what would
change, so the diff is reviewed before anything is touched.

The log is the point. `CONTRIBUTING.md` calls contributions "corrections to the
record, not changes to the recovered material", and a correction nobody can
audit is indistinguishable from an edit. So every removed span is written to
docs/recovery-log/ with the file, the rule, and the exact text, and the log
commits alongside the change it describes.

    python -B scripts/repair_fetch_damage.py            # dry run
    python -B scripts/repair_fetch_damage.py --apply    # write, and log
    python -B scripts/repair_fetch_damage.py --encoding # also decode entities
"""

from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import fetch_damage as fd  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "docs" / "recovery-log" / "2026-09-29-fetch-damage-repair.md"


# --------------------------------------------------------------------------
# re-anchoring the 501 citations
# --------------------------------------------------------------------------
#
# Thirteen of the files this repairs are quoted from, and all 501 citations pin
# a line number. Removing a line above a quotation moves it, and a citation that
# points one line off is worse than no citation.
#
# The line number is therefore DERIVED FROM TEXT, never computed. For each
# citation we take the text of the line it currently points at, find that same
# line in the repaired file, and use the line it landed on. The repair only ever
# removes other lines, so that line's own bytes are untouched and the match is
# exact.
#
# Three things abort the file rather than guess:
#   - the cited line's text is not found (the repair altered his prose - a bug)
#   - it is found more than once and the quote cannot narrow it to one
#   - the cited line was itself removed
# Anything ambiguous is left alone and reported.

def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def occupied_lines(lines: list[str], quote: str) -> set[int]:
    """The lines `quote` occupies, using test_quotes.py's own algorithm."""
    flat = norm("\n".join(lines))
    offsets, pos = [], 0
    for ln in lines:
        offsets.append(pos)
        n = norm(ln)
        if n:
            pos += len(n) + 1
    needle = norm(quote)
    out: set[int] = set()
    start = flat.find(needle)
    while start != -1:
        lo, hi = 0, len(offsets) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if offsets[mid] <= start:
                lo = mid
            else:
                hi = mid - 1
        out.add(lo + 1)
        start = flat.find(needle, start + 1)
    return out


def reanchor(rel_path: str, before: str, after: str, specs: dict):
    """(updates, problems) for every citation into `rel_path`.

    Walks the topic specs directly: spec -> material item -> key_claims -> claim,
    and rewrites `claim["ref"]` in place when the cited line has moved.

    `specs` is the already-loaded, shared spec cache. It is passed in rather than
    re-read because two specs can cite the same repaired file: the first version
    of this loaded each spec from disk per repaired file, so the mutations made
    for spec A during file 1's pass were discarded when file 2 re-read A, and
    only the last pass survived. It wrote 76 corrected refs and left 76 stale,
    which the suite caught as 76 QUOTE NOT FOUND. Specs are loaded once, mutated
    in place, and written once.
    """
    old_lines = before.splitlines()
    new_lines = after.splitlines()
    norm_new = [norm(l) for l in new_lines]
    updates: list[tuple[str, str, str]] = []
    problems: list[str] = []

    for spec_path, spec in specs.items():
        rel_spec = str(spec_path.relative_to(ROOT))
        for item in spec.get("material") or []:
            for claim in item.get("key_claims") or []:
                ref = claim.get("ref", "")
                m = re.match(r"^(.*):(\d+)$", ref)
                if not m:
                    continue
                if m.group(1).replace("\\", "/") != rel_path:
                    continue
                line = int(m.group(2))
                if not (1 <= line <= len(old_lines)):
                    problems.append(
                        f"{rel_path}:{line} is out of range ({len(old_lines)} "
                        f"lines) before repair")
                    continue
                anchor = norm(old_lines[line - 1])
                if not anchor:
                    problems.append(
                        f"{rel_spec}: {ref} points at a blank line; not re-anchored")
                    continue
                candidates = [i + 1 for i, n in enumerate(norm_new) if n == anchor]
                if not candidates:
                    problems.append(
                        f"{rel_spec}: {ref} - the cited line {anchor[:56]!r} is not "
                        f"in the repaired file; the repair altered his prose")
                    continue
                if len(candidates) > 1:
                    narrowed = [c for c in candidates
                                if c in occupied_lines(new_lines,
                                                      claim.get("quote", ""))]
                    if len(narrowed) != 1:
                        problems.append(
                            f"{rel_spec}: {ref} matches {len(candidates)} lines "
                            f"and the quote narrows it to {len(narrowed)}; "
                            f"not re-anchored")
                        continue
                    candidates = narrowed
                new_line = candidates[0]
                if new_line != line:
                    claim["ref"] = f"{m.group(1)}:{new_line}"
                    updates.append((rel_spec, ref, claim["ref"]))
    return updates, problems


def load_specs() -> dict:
    """Every topic spec, loaded once, keyed by path."""
    return {p: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((ROOT / "_data" / "topics").glob("*.json"))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="write the repairs; without this nothing is changed")
    ap.add_argument("--encoding", action="store_true",
                    help="also decode HTML entities, which are judgement-class "
                         "and therefore not done by the gate")
    args = ap.parse_args()

    changed: list[tuple[str, list[tuple[str, str]], int, int]] = []
    pairs = []
    for path, hits in fd.scan_collections():
        auto = [h for h in hits if h.automatic]
        if not auto and not args.encoding:
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        fixed, removed = fd.repair_text(original, encoding=args.encoding)
        if fixed == original:
            continue
        rel = path.relative_to(ROOT).as_posix()
        pairs.append((rel, original, fixed))
        changed.append((rel, removed, len(original), len(fixed)))

    total_removed = sum(len(r) for _, r, _, _ in changed)
    print(f"{'would repair' if not args.apply else 'repaired'} "
          f"{len(changed)} file(s), {total_removed} span(s) removed")
    for rel, removed, before, after in changed:
        rules = ", ".join(sorted({r for r, _ in removed}))
        print(f"  {rel}  [{rules}]  {before} -> {after} B "
              f"({after - before:+d})")

    # Re-anchor every citation into a repaired file, BEFORE anything is written.
    updates: list[tuple[str, str, str]] = []
    problems: list[str] = []
    specs = load_specs()
    for rel, before, after in pairs:
        u, p = reanchor(rel, before, after, specs)
        updates.extend(u)
        problems.extend(p)
    print(f"\ncitations re-anchored: {len(updates)}")
    for sp, old, new in updates[:12]:
        print(f"  {sp}: {old.rsplit(':', 1)[-1]} -> {new.rsplit(':', 1)[-1]}")

    if problems:
        print(f"\n{len(problems)} citation(s) could NOT be re-anchored. "
              f"Nothing written.", file=sys.stderr)
        for p in problems[:20]:
            print("  " + p, file=sys.stderr)
        return 1

    # Derived, never hardcoded. The citation count moved on 2026-09-29 when one
    # claim was removed for citing a blog commenter instead of the author, so a
    # literal 501 in this log became wrong the moment that landed.
    n_claims = sum(
        len(row.get("key_claims") or [])
        for spec_path in sorted((ROOT / "_data" / "topics").glob("*.json"))
        for row in json.loads(spec_path.read_text(encoding="utf-8")).get(
            "material") or []
    )

    for rel, removed, before, after in changed:
        rules = ", ".join(sorted({r for r, _ in removed}))
        print(f"  {rel}  [{rules}]  {before} -> {after} B "
              f"({after - before:+d})")

    # Re-anchor every citation into a repaired file, BEFORE anything is written.
    updates: list[tuple[str, str, str]] = []
    problems: list[str] = []
    specs = load_specs()
    for rel, before, after in pairs:
        u, p = reanchor(rel, before, after, specs)
        updates.extend(u)
        problems.extend(p)
    print(f"\ncitations re-anchored: {len(updates)}")
    for sp, old, new in updates[:12]:
        print(f"  {sp}: {old.rsplit(':', 1)[-1]} -> {new.rsplit(':', 1)[-1]}")

    if problems:
        print(f"\n{len(problems)} citation(s) could NOT be re-anchored. "
              f"Nothing written.", file=sys.stderr)
        for p in problems[:20]:
            print("  " + p, file=sys.stderr)
        return 1

    # The log is composed BEFORE the dry-run/clean-state decision below, because
    # a run that finds nothing is the state this file is most useful in: it is
    # the record that the corpus was checked and is clean. An earlier ordering
    # returned here first, so the log kept describing a repair a later pass had
    # already superseded - and the file is generated, so nobody notices a stale
    # one is stale.
    # Derived, never hardcoded. The citation count moved on 2026-09-29 when one
    # claim was removed for citing a blog commenter instead of the author, so a
    # literal 501 in this log became wrong the moment that landed.
    n_claims = sum(
        len(row.get("key_claims") or [])
        for spec_path in sorted((ROOT / "_data" / "topics").glob("*.json"))
        for row in json.loads(spec_path.read_text(encoding="utf-8")).get(
            "material") or []
    )

    log_lines = [
        "# Fetch-damage repair - 2026-09-29",
        "",
        "Generated by `scripts/repair_fetch_damage.py --apply`. This file records",
        "ONE run, the one that wrote it. Earlier runs on the same day are recorded",
        "in the commit log, not here.",
        "",
        "Every span below was removed because the FETCHER put it there, not",
        "because it read badly: injected ad configuration and stylesheet/script,",
        "orphaned JavaScript terminators, WordPress byline and comment furniture,",
        "the taxonomy block that already exists in front matter, and `<!--more-->`.",
        "Nothing in the author's prose was edited, re-punctuated or re-worded.",
        "",
        "## What the first pass on this date got wrong",
        "",
        "It was recorded here, wrongly, that comment threads were \"removed in",
        "full\". They were not. The first pass removed the `1 Comment` count and",
        "the `### One Comment on \"...\"` heading; no rule matched the comment",
        "BODIES, and 33 lines of third-party commentary stayed inside eleven posts.",
        "It also reported residue 0 on a post that still held a nine-line",
        "`wpmrec2x` stylesheet and truncated script, because the ad rule qualified a",
        "line partly by proximity to a `});` terminator and that same pass had",
        "deleted the terminators. A detector must not depend on a token the repair",
        "removes. Both rules were rewritten to key on line content, and both gaps",
        "are now covered by `injected-script-run` and `comment-thread`.",
        "",
        "Comment bodies are removed because they are third-party blog commentary:",
        "not the author's work, and not a source this archive claims to hold. The",
        "archive keeps third-party *sources* in /sources/.",
        "",
        "## Citations",
        "",
        f"All {n_claims} citations pin a line number, so {len(updates)} of them",
        "were re-anchored in this run. No line number was computed: each was",
        "re-derived by finding the cited line's own text in the repaired file, so",
        "the anchor is the line's content rather than an arithmetic offset.",
        "`test_quotes.py` then re-verifies every citation independently.",
        "",
        f"The count is {n_claims}, not the 501 an earlier version of this log",
        "claimed, because one claim was removed on 2026-09-29: it cited a line",
        "that was a WordPress comment, and presented a reader's objection as the",
        "author's answer. `check_no_citation_into_damage` now fails the build if",
        "any spec cites a damaged line.",
        "",
        "| spec | was | now |",
        "|---|---|---|",
    ]
    for sp, old, new in updates:
        log_lines.append(f"| `{sp}` | `{old}` | `{new}` |")
    log_lines += ["", f"## Files", "",
                  f"**{len(changed)} file(s), {total_removed} span(s).**", ""]

    for rel, removed, before, after in changed:
        log_lines.append(f"### `{rel}`")
        log_lines.append("")
        log_lines.append(f"{before} B -> {after} B ({after - before:+d})")
        log_lines.append("")
        log_lines.append("| rule | text removed |")
        log_lines.append("|---|---|")
        for rule, text in removed:
            log_lines.append(f"| `{rule}` | `{text.replace('|', chr(92) + '|')}` |")
        log_lines.append("")

    if not args.apply or not changed:
        if not args.apply and changed:
            print("\ndry run: nothing written. Re-run with --apply.")
        elif not changed:
            # A run that finds nothing is the state this file is most useful in:
            # it is the record that the corpus was checked and is clean. Writing
            # it on every pass also means the log cannot sit there describing a
            # repair that a later pass has already superseded.
            LOG.parent.mkdir(parents=True, exist_ok=True)
            LOG.write_text("\n".join(log_lines), encoding="utf-8", newline="")
            print(f"\nno damage found; log written "
                  f"({LOG.relative_to(ROOT)}) recording the clean state")
        return 0

    for rel, _before, fixed in pairs:
        with open(ROOT / rel, "w", encoding="utf-8", newline="") as fh:
            fh.write(fixed)
    # One write per spec that changed, from the in-memory cache every reanchor
    # pass mutated.
    touched = sorted({ROOT / sp for sp, _, _ in updates})
    for spec_path in touched:
        spec_path.write_text(
            json.dumps(specs[spec_path], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8", newline="")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(chr(10).join(log_lines), encoding="utf-8", newline="")
    print(f"\nlog written to {LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
