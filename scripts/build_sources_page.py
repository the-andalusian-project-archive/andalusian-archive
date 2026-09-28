#!/usr/bin/env python3
"""Build /sources/ - the third-party record page.

WHY THIS PAGE EXISTS. `_data/secondary_sources.json` held 70 records about this
author written by other people - reprints, critiques, biographies, mentions - and
every one had a URL. None of them was rendered anywhere on the site. The archive
was, in effect, holding a private index of other people's writing about him, and
publishing none of it. A record no reader can reach is not an archive record.

The page groups them by kind, gives each its own URL, links whatever archive item
it concerns, and says plainly what the group means. It is also the one place the
corpus's own limits are stated: how many records carry an established referent
and how many do not, because a reader deserves to know which is which.

Usage: python scripts/build_sources_page.py
"""

from __future__ import annotations

import collections
import json
import pathlib
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SS = ROOT / "_data" / "secondary_sources.json"
LINKS = ROOT / "_data" / "secondary_links.json"
OUT = ROOT / "sources.md"

TYPE_BLURB = {
    "reprint": "Work of his, republished by someone else. The archive holds the "
               "original; these are the other copies, and the differences between "
               "them are the reason the capture records exist.",
    "critique": "Arguments written against his. Kept because an archive that only "
                "holds the friendly versions is not an archive.",
    "mention": "Pages that refer to him or to a work of his, including third-party "
               "pages that carry a video or a talk rather than reproducing it.",
    "bio": "Biographies, profiles and CVs written by other people. They are kept "
           "because they are evidence of how he was described, and they are the "
           "rows most likely to have gone out of date.",
}


def esc(t: str) -> str:
    return (str(t or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def main() -> int:
    rows = json.loads(SS.read_text(encoding="utf-8"))
    rows = rows if isinstance(rows, list) else list(rows.values())[0]
    meta = json.loads(LINKS.read_text(encoding="utf-8"))
    today = date.today().isoformat()

    by_type: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_type[r.get("type") or "other"].append(r)

    related = sum(1 for r in rows if r.get("relates_to"))
    sections = []
    for kind in ("reprint", "critique", "mention", "bio", "other"):
        group = by_type.get(kind) or []
        if not group:
            continue
        items = []
        for r in sorted(group, key=lambda x: ((x.get("date") or ""), x.get("title") or "")):
            when = r.get("date") or ""
            title = r.get("title") or "(untitled record)"
            src = r.get("source") or ""
            links = r.get("relates_to") or []
            if links:
                bits = []
                for l in links:
                    pl = l.get("permalink") or ""
                    label = esc(l.get("label") or l.get("ref", ""))
                    if pl:
                        bits.append(f'<a href="{{{{ site.baseurl }}}}{pl}">{label}</a>')
                    else:
                        bits.append(label)
                rel = ('<p class="rel">Concerns '
                       + "; ".join(bits)
                       + f' &mdash; <em>{esc(links[0].get("how",""))}</em></p>')
            else:
                # Say what is known, not what the record appears to be.
                #
                # This used to read "No single archive item established as its
                # subject - it is a record about the author, not about one work."
                # The first clause is a fact about the archive. The second is an
                # inference drawn from that absence, and it is false: the record
                # was asadullahali.wordpress.com, the site that carried dozens of
                # his works. Failing to establish a referent says nothing about
                # what a record concerns; it says we have not established it.
                # Fifty of seventy records carried the invented clause.
                rel = ('<p class="rel rel-none">No archive item linked to this '
                       'record yet &mdash; it is catalogued, and its subject has '
                       'not been established.</p>')
            items.append(
                f"""    <li class="src">
      <h3><a href="{esc(r.get('url',''))}" target="_blank" rel="noopener noreferrer">{esc(title)}</a></h3>
      <p class="src-meta">{esc(src)}{' &middot; ' + esc(when) if when else ''} &middot; {esc(kind)}</p>
      {rel}
    </li>"""
            )
        sections.append(
            f"""<h2 id="{kind}">{esc(kind.capitalize())} ({len(group)})</h2>
<p class="note">{esc(TYPE_BLURB.get(kind, ""))}</p>
<ul class="src-list">
{chr(10).join(items)}
</ul>"""
        )

    page = f"""---
layout: default
title: Third-party sources about this author
description: "Reprints, critiques, biographies and mentions of Asadullah Ali Al-Andalusi written by other people, with links to the archive item each one concerns."
permalink: /sources/
last_modified_at: {today}
---

<h1>Third-party sources about this author</h1>

<p class="lead">What other people have written about this work, and where it has
been republished.</p>

<p>{len(rows)} records, all with a source URL, catalogued but <strong>not counted
as content</strong> &mdash; they are other people's writing, and counting them
would be counting the archive against itself. {related} of them name an item this
archive holds; the rest are records about the author rather than about one work,
and are listed as such rather than given a subject they do not have.</p>

<p class="note">These are catalogued for two reasons. A reader who has found a
reprint or a biography deserves to know it exists and what it says. And an archive
that only holds the friendly versions of a contested subject is not an archive:
the critiques are here for the same reason the works are.</p>

<p>Built {today} by <code>scripts/build_sources_page.py</code>; the relationships
are derived by <code>scripts/relate_secondary_sources.py</code> and checked by
<code>scripts/test_quotes.py</code>.</p>

{''.join(sections)}
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote sources.md: {len(rows)} records in {len(by_type)} groups, "
          f"{related} with an established referent")
    for kind in sorted(by_type):
        print(f"  {kind:10s} {len(by_type[kind])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
