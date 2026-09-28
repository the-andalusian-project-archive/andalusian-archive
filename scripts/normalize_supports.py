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


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip().lower()


def best_match(part: str, declared: dict[str, str]) -> tuple[str | None, float]:
    n = norm(part)
    if n in declared:
        return declared[n], 1.0
    for key, original in declared.items():
        if key.startswith(n) or n.startswith(key):
            return original, 0.95
    matches = difflib.get_close_matches(n, list(declared), n=1, cutoff=FLOOR)
    if matches:
        best = matches[0]
        return declared[best], difflib.SequenceMatcher(None, n, best).ratio()
    return None, 0.0


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
                    hit, score = best_match(parts[0], declared)
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
                    hit, _ = best_match(part, declared)
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
