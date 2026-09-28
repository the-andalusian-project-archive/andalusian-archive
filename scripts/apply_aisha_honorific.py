"""Render the honorific after Aisha as `Aisha (R.A.)` rather than `Aisha (ra)`.

WHAT THIS IS. A site-owner decision, applied to the six places the recovered
corpus writes the honorific after Aisha, plus the topic spec quote that cites
one of them.

WHY IT NEEDS A SCRIPT. Two reasons, both of them about not being casual with
someone else's words.

1. The occurrences live in the AUTHOR'S PROSE, which this archive holds
   verbatim. Changing `(ra)` to `(R.A.)` touches recovered text, and the archive
   states plainly that recovered prose is never reworded. So the change is
   counted, declared here, and reversible - it is a transliteration convention
   for an abbreviation, not a claim about the argument, and it is recorded as
   such rather than done silently.

2. `test_quotes.py` verifies the quotation in `_data/topics/gender-feminism.json`
   against the file it cites. If the source changes and the quote does not, the
   suite fails. That is the correct behaviour and the reason this script touches
   the spec in the same pass.

WHAT IS DELIBERATELY NOT TOUCHED: `_posts/2020-08-10-reviewing-haqiqatjou.md`
twice quotes a Yaqeen Institute collection titled "More Than Just a Number:
Perspectives on the Age of Aisha (RA)". That is a third party's proper noun,
quoted, and its capitalisation is theirs. The honorific when the author writes it
is changed; a quoted title is not.

Writes bytes directly: a BOM would make Jekyll skip the front matter.
"""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# files that carry the honorific in the author's own prose
PROSE = [
    "_data/mdi_articles.json",
    "_posts/2013-03-17-prophets-vs-pedophiles-part-1.md",
    "_posts/2013-03-20-prophets-vs-pedophiles-part-2.md",
    "_posts/2013-06-09-prophets-vs-pedophiles-part-3.md",
    "_posts/2020-08-10-reviewing-haqiqatjou.md",
    # the quote the topic spec cites; must change in step or the suite fails
    "_data/topics/gender-feminism.json",
    # the served pages, which are committed source rather than built from the
    # JSON at build time
    "_articles/mdi-religion-vs-paedophilia-part-1.md",
    "_articles/mdi-religion-vs-paedophilia-part-2.md",
    "_articles/mdi-religion-vs-paedophilia-part-3.md",
]

# a quoted third-party title. left alone on purpose.
KEEP = "Perspectives on the Age of Aisha (RA)"

PATTERNS = [
    ("Aisha (ra)", "Aisha (R.A.)"),
    ("Aisha (RA)", "Aisha (R.A.)"),
]


def convert(path: pathlib.Path) -> tuple[int, list[str]]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    if bom:
        raw = raw[3:]
    text = raw.decode("utf-8")
    total = 0
    for old, new in PATTERNS:
        out: list[str] = []
        idx = 0
        while True:
            hit = text.find(old, idx)
            if hit == -1:
                out.append(text[idx:])
                break
            # skip the occurrence if it sits inside a quoted third-party title
            line_start = text.rfind("\n", 0, hit) + 1
            line_end = text.find("\n", hit)
            line_end = len(text) if line_end == -1 else line_end
            line = text[line_start:line_end]
            if KEEP in line:
                out.append(text[idx:hit + len(old)])
            else:
                out.append(text[idx:hit])
                out.append(new)
                total += 1
            idx = hit + len(old)
        text = "".join(out)
    if total:
        data = text.encode("utf-8")
        assert not data.startswith(b"\xef\xbb\xbf")
        path.write_bytes(data)
    return total, [p for p in PATTERNS if p[0] in text]


if __name__ == "__main__":
    grand = 0
    for rel in PROSE:
        p = ROOT / rel
        if not p.exists():
            print(f"  MISSING {rel}")
            continue
        n, left = convert(p)
        grand += n
        print(f"  {rel:56s} {n} changed"
              + (f"   (still present, quoted title: {left})" if n == 0 and left else ""))
    print(f"\ntotal occurrences changed: {grand}")
    leftover = []
    for rel in PROSE:
        t = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"Aisha \((?:ra|RA)\)", t):
            line = t[t.rfind("\n", 0, m.start()) + 1 : t.find("\n", m.start())]
            if KEEP in line:
                continue
            leftover.append((rel, m.group(0)))
    print(f"unconverted occurrences outside quoted titles: {len(leftover)}")
    for rel, s in leftover[:5]:
        print(f"  {rel}: {s}")
