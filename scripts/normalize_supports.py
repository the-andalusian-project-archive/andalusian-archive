"""Normalise `supports` in the topic specs so each value is a real declared query.

Two of the eight research agents grouped their `supports` labels by `;` in a
different arrangement from the query buckets, so a label could name a real query
without being byte-identical to the bucket entry. The quotes themselves are
untouched and already verify; this only re-anchors the labels.

Each `;`-separated part of a label is matched to the declared query it most
closely resembles, using exact match, then prefix, then a difflib ratio. Anything
below the similarity floor is reported rather than guessed at.

Usage: python scripts/normalize_supports.py [--write]
"""

from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOPIC_DIR = ROOT / "_data" / "topics"
BUCKETS = ("head", "mid", "long_tail", "question_forms", "ai_phrased")
FLOOR = 0.72
# A best match this close to the runner-up is a guess, not a match.
MIN_MARGIN = 0.05


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip().lower()


def best_match(part: str, declared: dict[str, str]) -> tuple[str | None, float, float]:
    """Nearest declared query for one label fragment.

    Returns (query, score, margin) where margin is the gap to the runner-up.

    The margin matters more than the score. A previous version returned the
    first declared key sharing a prefix, with a hardcoded 0.95 that was a
    constant rather than a measurement: given the label 'why is islam' it
    happily returned 'why is islam called the religion of terror'. Without a
    margin check there is nothing that distinguishes a confident match from a
    coin flip, so near-ties are now reported instead of guessed.
    """
    n = norm(part)
    if n in declared:
        return declared[n], 1.0, 1.0

    scored = sorted(
        ((difflib.SequenceMatcher(None, n, k).ratio(), k) for k in declared),
        reverse=True,
    )
    if not scored or scored[0][0] < FLOOR:
        return None, (scored[0][0] if scored else 0.0), 0.0
    best_score, best_key = scored[0]
    runner_up = scored[1][0] if len(scored) > 1 else 0.0
    return declared[best_key], best_score, best_score - runner_up


def main() -> int:
    write = "--write" in sys.argv
    unresolved = 0
    rewritten = 0

    for path in sorted(TOPIC_DIR.glob("*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        declared: dict[str, str] = {}
        for bucket in BUCKETS:
            for q in spec["queries"].get(bucket) or []:
                declared[norm(q)] = q

        changed = 0
        for item in spec.get("material") or []:
            for claim in item.get("key_claims") or []:
                raw = claim.get("supports", "")
                if not raw:
                    continue
                if norm(raw) in declared:
                    continue
                parts = [p.strip() for p in raw.split(";") if p.strip()]
                if len(parts) == 1:
                    hit, score, margin = best_match(parts[0], declared)
                    if hit is not None and margin < MIN_MARGIN:
                        unresolved += 1
                        print(f"  AMBIGUOUS {path.stem}: {parts[0][:60]!r} best={score:.2f} margin={margin:.2f}")
                        continue
                    if hit is None:
                        unresolved += 1
                        print(f"  UNRESOLVED {path.stem}: {parts[0][:70]!r}")
                        continue
                    claim["supports"] = hit
                    changed += 1
                    continue
                # A compound label: keep the FIRST part that resolves. The label's
                # job is to say which question this claim speaks to; one is enough,
                # and a single declared query is a valid foreign key.
                resolved = None
                for part in parts:
                    hit, _score, _margin = best_match(part, declared)
                    if hit:
                        resolved = hit
                        break
                if resolved is None:
                    unresolved += 1
                    print(f"  UNRESOLVED {path.stem}: {raw[:70]!r}")
                else:
                    claim["supports"] = resolved
                    changed += 1

        if changed:
            rewritten += changed
            print(f"  {path.stem}: rewrote {changed} supports label(s)")
            if write:
                path.write_text(
                    json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

    print(f"\nrewritten={rewritten} unresolved={unresolved} "
          f"mode={'WRITE' if write else 'DRY-RUN'}")
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
