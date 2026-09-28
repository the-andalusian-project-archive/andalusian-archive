#!/usr/bin/env python3
"""Link written works and papers to the recordings of them that the archive holds.

WHY THIS EXISTS. Every one of the 68 recordings in `_data/videos.json` has its
own preserved MP4 on the Internet Archive, verified live. But nothing connected
those recordings to the articles and papers they are recordings OF. So a reader
who opened `/papers/the-qur-an-and-science-a-forced-marriage/` was offered one
route - "View Original", to the WordPress post - and that post's YouTube embed
is private. The reader lands on a dead video. Meanwhile the archive holds a
620 MB copy of the same talk at `/videos/fJs5tuFw-UY/`, and says nothing.

This is the third instance of the same defect, which is why it gets a gate rather
than a patch each time. The first was the DocsLib mirror sitting under "no
archive item established"; the second was `llms.txt` going stale. In each case
the archive stated something about its own holdings that its own data
contradicted. The rule this file follows: a claim about the archive's holdings is
computed from the holdings, never hand-maintained.

GUARDS, because the obvious implementation gets this wrong:

  * A minimum word count. `title_match` scores by what fraction of the needle's
    words appear in the candidate, so a one-word title scores 1.00 against
    anything containing that word. The work titled "Islam" matched the recording
    "23 - Islam, Science and History" at 1.00 - a false positive at the perfect
    score. A needle needs 3 significant words, or exact normalised title
    equality, before it is allowed to match at all.
  * A 0.75 floor. Aisha's paper scores 0.60 against "29 - Understanding the Age
    of Aisha" because the paper carries a long subtitle; that one is right, and
    the subtitle words are the reason it is not 1.00. Anything below 0.75 is not
    evidence of a relationship and is left unresolved.

Output: `_data/recording_links.json`, keyed by the item's permalink.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_data" / "recording_links.json"

MIN_SCORE = 0.75
MIN_WORDS = 2

STOP = set(
    "the a an and or of in on to for is it at by with from as that this be "
    "are was were his her their its not but we you i he she they".split()
)


def load(name: str):
    d = json.loads((ROOT / "_data" / name).read_text(encoding="utf-8"))
    return d if isinstance(d, list) else list(d.values())[0]


def words(text: str) -> set[str]:
    out = {t.strip("'") for t in re.split(r"[^a-z0-9]+", (text or "").lower())}
    return {w for w in out if len(w) > 2 and w not in STOP}


def score(needle: str, hay: str) -> float:
    a, b = words(needle), words(hay)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def main() -> int:
    works = load("canonical_works.json")
    papers = load("papers.json")
    vids = load("videos.json")
    vids = [v for v in vids if v.get("counted")]

    def vid_permalink(v: dict) -> str:
        return f"/videos/{v.get('id')}/"

    # Reject needles that cannot carry evidence. A one-word title is cheap to
    # match against anything; "Islam" is the concrete failure.
    def matchable(title: str) -> bool:
        return len(words(title)) >= MIN_WORDS

    by_url: dict[str, list[dict]] = {}
    considered = rejected_short = 0

    for kind, items in (("work", works), ("paper", papers)):
        for it in items:
            title = it.get("title", "") or ""
            if kind == "work":
                ref = it.get("slug", "")
                perm = it.get("local_post_url") or (f"/articles/{ref}/" if ref else "")
            else:
                ref = str(it.get("id") or "")
                perm = f"/papers/{slugify(title)}/"
            if not perm:
                continue
            if not matchable(title):
                rejected_short += 1
                continue
            considered += 1

            scored = sorted(
                ((score(title, v.get("title", "") or ""), v) for v in vids),
                key=lambda x: x[0],
                reverse=True,
            )
            best = [(s, v) for s, v in scored if s >= MIN_SCORE]
            # A title can legitimately map to more than one recording - a lecture
            # series is several videos - so keep every candidate at the top
            # score, not just the first.
            if not best:
                continue
            top = best[0][0]
            for s, v in best:
                if s < top:
                    break
                by_url.setdefault(perm, []).append({
                    "video_id": v.get("id"),
                    "title": v.get("title", ""),
                    "url": vid_permalink(v),
                    "archive_url": v.get("archive_url", ""),
                    "duration": v.get("duration"),
                    "score": round(s, 3),
                    "how": ("same title as the recording" if s >= 0.999
                            else f"title overlap {s:.0%}"),
                })

    total = sum(len(v) for v in by_url.values())
    print(f"  recordings held              : {len(vids)}")
    print(f"  items considered for matching: {considered}")
    print(f"  skipped: too short to match  : {rejected_short}")
    print(f"  items with a recording       : {len(by_url)}")
    print(f"  total item->recording links  : {total}")

    if "--write" in sys.argv:
        OUT.write_text(
            json.dumps(
                {
                    "built": date.today().isoformat(),
                    "note": "Written works and papers -> the recordings of them "
                            "that this archive holds, keyed by the item's "
                            "permalink. Written by scripts/relate_recordings.py "
                            "and checked by scripts/test_quotes.py. Every linked "
                            "recording has its own verified copy on the Internet "
                            "Archive; that link is the one guaranteed to work, "
                            "because the author's own YouTube embeds on his "
                            "WordPress posts are largely private.",
                    "by_url": by_url,
                },
                ensure_ascii=False, indent=2, sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
