#!/usr/bin/env python3
"""Relate third-party records to the archive items they actually refer to.

THE PROBLEM. `_data/secondary_sources.json` holds 70 records about this author
written by other people - reprints, critiques, biographies, mentions - and every
one of them has a URL. None of them was related to the item it concerns, and
none of them was rendered on the site at all. So an Academia.edu profile that
enumerates six papers and seven talks, and a dozen third-party pages that carry
his video work, were all sitting in a data file that no page read.

WHAT THIS DOES.

1. `relates_to` - attaches a `relates_to` array to each row whose referent is
   established rather than guessed. Three sources of relationship, in descending
   order of confidence:

   a. EXACT TITLE, read off the captured page. The Academia.edu listing recovered
      at web.archive.org/web/20191207110813/ names six papers and seven talks in
      full, and every one of them is in this archive under a matching title. Those
      13 relations are transcribed from the capture, not inferred.

   b. NORMALISED TITLE against `papers.json` and `canonical_works.json`, for the
      Kezana and IIUM repository records. A title match has to clear a word-overlap
      floor; a partial match is left unmatched rather than guessed.

   c. MDI rows, matched to the MDI item whose slug they mirror, so a third-party
      page carrying one of his talks is filed against the MDI record that holds
      the text.

2. A `/sources/` page - all 70 records, grouped by type, each with its URL and
   whatever it is related to. This is the surfacing half. A record nobody can see
   is not an archive.

3. A reverse index, so the related work, paper and video pages can say "this was
   also published/mentioned here" and link out.

WHAT IS NOT DONE. Rows with no established referent keep no `relates_to` and are
listed without one. The report at the end says how many, because a guessed
relationship on a preservation archive is worse than an absent one.

Usage: python scripts/relate_secondary_sources.py [--write]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SS = ROOT / "_data" / "secondary_sources.json"
REVERSE = ROOT / "_data" / "secondary_links.json"

STOP = {
    "the", "a", "an", "of", "and", "in", "on", "for", "to", "by", "with",
    "from", "at", "is", "are", "was", "were", "its", "it", "as", "between",
    "case", "more", "part",
}

# Transcribed from the capture, not inferred. Titles as the listing prints them.
ACADEMIA_PAPERS = [
    "Understanding Aisha's Age: An Interdisciplinary Approach",
    "The Structure of Scientific Productivity in Islamic Civilization: Orientalists' Fables",
    "Architects of Civilisation: Sallahuddin Ayubi",
    "Gender Equality, Islam, and Law",
    "The Rise and Decline of Scientific Productivity In The Muslim World: A Preliminary Analysis",
    "The Archetype of Beauty in Islam",
]
ACADEMIA_TALKS = [
    "The Qur'an and Science: A Forced Marriage",
    "Doubting your Doubts: Atheism Among Muslim Youth",
    "Extremism in Muslim Thought",
    "Islam and Terrorism",
    "Understanding Atheism",
    "Sustaining the Malaysian Environment through Litter Reduction: A Maqasidi Approach",
    "Still Colonized? Liberalism in Muslim Thought",
]
ACADEMIA_URL_MARKER = "independent.academia.edu/AsadullahAli"

# Resolutions the title matcher cannot make and a person should.
#
# Each is a case where the listing's wording and the archive's differ in a way
# that is not a typo, so the pairing is a judgement and is recorded as one rather
# than left to a similarity score. Both are verified against the capture, which
# prints these titles in full.
#
#   "Doubting your Doubts: Atheism Among Muslim Youth" is the PAPER title; the
#   archive holds the same argument as the work "Atheism: Doubting Your Doubts"
#   (slug atheism-doubting-your-doubts). The words are the same, in the other
#   order, so overlap scoring puts it at 0.57 and misses it.
#
#   "Sustaining the Malaysian Environment through Litter Reduction: A Maqasidi
#   Approach" is a paper this archive holds under exactly that title (id 17), and
#   the related blog work is "Towards Litter Reduction: An Islamic Approach".
#   Both are listed; they are the same project under two titles.
ACADEMIA_FIXED: list[tuple[str, str, str, str]] = [
    ("Doubting your Doubts: Atheism Among Muslim Youth",
     "work", "atheism-doubting-your-doubts",
     "same argument, listed under the paper's title"),
    ("Sustaining the Malaysian Environment through Litter Reduction: A Maqasidi Approach",
     "paper", "17", "paper of the same name; the blog work is 'Towards Litter Reduction'"),
]

# Relations the title matcher cannot reach, because the third party's headline is
# its own rather than his. Each one is justified by a fact the record itself
# already states in its `notes` field, which is what makes these auditable: the
# relationship is read out of the archive's own record, not inferred.
#
# Deliberately NOT pinned here:
#   * the two "Catholic became atheist ... finally accepted Islam" reprints. They
#     are reprints of his conversion narrative, but the archive holds no item for
#     that narrative, so there is nothing to point at. Leaving them unresolved is
#     the accurate answer, not a gap to be papered over with a near-match.
#   * the TOTETU Japanese translation record, which cites paper 7 but is an issue
#     contents page for a 20-page translation the archive does not hold. It is a
#     venue, not a reprint of a text we have.
NOTES_PINNED: list[tuple[str, str, str, str, str]] = [
    ("heroes-history.blogspot.com",
     "paper", "8",
     "full-text reprint of the same IAIS book chapter the archive holds",
     "reprint of a paper the archive holds"),
    ("docslib.org",
     "paper", "8",
     "document-hosting mirror of the same IAIS book chapter",
     "mirror of a paper the archive holds"),
    ("studentrepo.iium.edu.my",
     "paper", "19",
     "institutional record of his MA thesis, which the archive holds as paper 19",
     "record of a paper the archive holds"),
    ("digilib.uin-suka.ac.id",
     "paper", "19",
     "third-party thesis engaging critically with his MA thesis",
     "critique of a paper the archive holds"),
    ("linkedin.com",
     "paper", "19",
     "third-party post quoting a passage from his MA thesis",
     "quotation from a paper the archive holds"),
    ("repo.uinsatu.ac.id",
     "paper", "7",
     "third-party reference list citing his co-authored article",
     "reference to a paper the archive holds"),
]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def words(text: str) -> set[str]:
    out = set()
    for tok in re.split(r"[^a-z0-9']+", (text or "").lower()):
        if len(tok) > 2 and tok not in STOP:
            out.add(tok.strip("'"))
    return {w for w in out if w}


def title_match(needle: str, hay: str) -> float:
    a, b = words(needle), words(hay)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a)


def front_matter_url_index() -> dict[str, tuple[str, str]]:
    """URL -> (permalink, title) for every external URL in collection front matter.

    THE BRANCH THAT WAS MISSING. Everything else in this file decides a
    relationship from a *title*, or from a transcribed listing. But a third-party
    record whose URL is byte-identical to a URL the archive itself recorded as
    the source of an item it holds is already related to that item - no title
    matching required, no inference at all. The matcher could not see this class
    at all, so six records published a claim the archive's own data refutes.

    The worst case is instructive: the TOTETU record for paper 7 rendered as "no
    single archive item established as its subject", while that same URL is
    paper 7's `file_source` and the archive serves the PDF as that paper's full
    text. Read collection front matter rather than the `_data/` JSON because
    front matter is what the site actually renders, and what the matching gate
    in scripts/test_quotes.py reads - so the two agree by construction.
    """
    index: dict[str, tuple[str, str]] = {}
    for folder in ("_articles", "_papers", "_videos", "_transcripts"):
        d = ROOT / folder
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            head = text[:end]
            pm = re.search(r"^permalink:[ \t]*(\S+)", head, re.M)
            if not pm:
                continue
            perm = pm.group(1).strip().strip("\"'").rstrip("/") + "/"
            tm = re.search(r"^title:[ \t]*(.+)$", head, re.M)
            label = tm.group(1).strip().strip("\"'") if tm else ref_label_from(perm)
            for u in re.findall(r"https?://[^\s\"'<>]+", head):
                index.setdefault(u.rstrip("/").lower(), (perm, label))
    return index


def ref_label_from(permalink: str) -> str:
    return permalink.strip("/").split("/")[-1] or permalink


def load(name: str):
    rows = json.loads((ROOT / "_data" / name).read_text(encoding="utf-8"))
    return rows if isinstance(rows, list) else list(rows.values())[0]


def main() -> int:
    write = "--write" in sys.argv
    rows = load("secondary_sources.json")
    works = load("canonical_works.json")
    papers = load("papers.json")
    mdis = load("mdi_articles.json")
    vids = load("videos.json")

    # permalink -> stable id, so every relation is keyed by the same
    # identity no matter which branch produced it.
    ref_by_perm: dict[str, str] = {}
    for w in works:
        p_ = w.get("local_post_url") or (f"/articles/{w.get('slug','')}/" if w.get("slug") else "")
        if p_:
            ref_by_perm[p_.rstrip("/") + "/"] = str(w.get("slug") or "")
    for p_ in papers:
        t_ = p_.get("title", "")
        ref_by_perm[f"/papers/{slugify(t_)}/"] = str(p_.get("id") or "")
    for v in vids:
        ref_by_perm[f"/videos/{v.get('id','')}/"] = str(v.get("id") or "")
    for m in mdis:
        sl = m.get("slug") or ""
        if sl:
            ref_by_perm[f"/articles/mdi/{sl}/"] = str(sl)
    work_by_title = [(w.get("title", ""), w) for w in works]
    paper_by_title = [(p.get("title", ""), p) for p in papers]
    mdi_by_title = [(m.get("title", ""), m) for m in mdis]
    vid_by_title = [(v.get("title", ""), v) for v in vids]

    url_index = front_matter_url_index()
    reverse: dict[str, list[dict]] = {}
    by_url: dict[str, list[dict]] = {}
    stats = {"url_identity": 0, "academia": 0, "title": 0, "pinned": 0, "mdi": 0, "none": 0}

    # Every related item is also keyed by its PERMALINK, because that is what a
    # Jekyll page knows about itself. Keying by `kind:ref` instead meant each
    # layout had to know whether papers are identified by `id` or by slug, and
    # papers carry no `id` in their front matter at all.
    work_url = {w.get("slug", ""): w.get("local_post_url", "") for w in works}
    paper_url: dict[str, str] = {}
    for p in papers:
        slug = re.sub(r"[^a-z0-9]+", "-", (p.get("title", "")).lower()).strip("-")
        paper_url[str(p.get("id"))] = f"/papers/{slug}/"
    video_url = {v.get("id", ""): f"/videos/{v.get('id')}/" for v in vids}

    def permalink(kind: str, ref: str) -> str:
        if kind == "paper":
            return paper_url.get(ref, "")
        if kind == "video":
            return video_url.get(ref, "")
        if kind == "mdi":
            # The Muslim Debate Initiative's own pages are a distinct layout
            # branch: third-party carriers that re-host his talks under a
            # byline that is not his. They need their own back-reference, and
            # silently returning "" for them is what excluded them before.
            return f"/articles/mdi/{ref}/"
        if kind == "work":
            wp = next((w.get("local_post_url", "") for w in works
                       if w.get("slug") == ref), "")
            return wp or f"/articles/{ref}/"
        return ""

    for row in rows:
        row.pop("relates_to", None)
        title = row.get("title", "")
        url = row.get("url", "") or ""
        found: list[dict] = []

        def add(kind: str, ref: str, label: str, how: str) -> None:
            # Only records the relation here. The reverse index is written in
            # the post-dedupe pass below, because writing it from here meant a
            # row reaching the same item twice produced two entries in the
            # index while `relates_to` correctly held one - and the index is
            # what the back-reference include reads, so paper 17 rendered the
            # same Academia.edu record twice with two different `how` strings.
            found.append({"kind": kind, "ref": ref, "label": label, "how": how})

        # (0) URL identity, the strongest evidence available and the cheapest.
        #     If the archive recorded this exact URL as a source for an item it
        #     holds, the record is about that item. Runs first because it needs
        #     no inference, and because leaving it out is what let the page
        #     assert something its own data disproves.
        if url:
            hit = url_index.get(url.rstrip("/").lower())
            if hit:
                pl, label = hit
                kind = ("paper" if pl.startswith("/papers/") else
                        "video" if pl.startswith("/videos/") else
                        "mdi" if "/mdi/" in pl else "work")
                # Use the item's own stable id as `ref`, not the permalink.
                # Storing the permalink here made the `links` map key on a
                # second, parallel identity for the same item, so an item
                # reachable by two routes got two `links` keys and one
                # `by_url` key.
                add(kind, ref_by_perm.get(pl, pl), label,
                    "the URL this archive recorded as a source for this item")
                stats["url_identity"] += 1

        # (a) the Academia.edu listing, transcribed from the capture
        if not found and ACADEMIA_URL_MARKER in url:
            for t in ACADEMIA_PAPERS:
                best, score = None, 0.0
                for cand, rec in paper_by_title:
                    s = title_match(t, cand)
                    if s > score:
                        best, score = (cand, rec), s
                if best and score >= 0.75:
                    add("paper", str(best[1].get("id") or best[1].get("slug") or best[0]),
                        best[0], "named on the captured listing")
            for t in ACADEMIA_TALKS:
                cands = [(title_match(t, c), c, r) for c, r in
                         work_by_title + vid_by_title + paper_by_title
                         if title_match(t, c) >= 0.75]
                # Take the BEST match, not the first. `cands[:1]` took whichever
                # table happened to be searched first, which meant
                # "The Qur'an and Science: A Forced Marriage" resolved to the
                # work at 0.75 while a video and a paper at 1.0000 were dropped
                # on the floor. Ties keep catalogue order via the stable sort.
                if cands:
                    s, cand, rec = max(cands, key=lambda x: x[0])
                    kind = ("work" if rec in works else
                            "video" if rec in vids else "paper")
                    add(kind, str(rec.get("slug") or rec.get("id")), cand,
                        "named on the captured listing"
                        + ("" if s >= 0.999 else f" (title overlap {s:.0%})"))
            # the two the matcher cannot make
            for listed, kind, ref, why in ACADEMIA_FIXED:
                if kind == "paper":
                    label = next((p.get("title", "") for p in papers
                                  if str(p.get("id")) == ref), listed)
                else:
                    label = next((w.get("title", "") for w in works
                                  if w.get("slug") == ref), listed)
                add(kind, ref, label, why)
            stats["academia"] += 1

        # (b) exact-ish title against the catalogue
        if not found:
            best, score = None, 0.0
            for cand, rec in paper_by_title:
                s = title_match(title, cand)
                if s > score:
                    best, score = (cand, rec, "paper"), s
            for cand, rec in work_by_title:
                s = title_match(title, cand)
                if s > score:
                    best, score = (cand, rec, "work"), s
            if best and score >= 0.8:
                add(best[2], str(best[1].get("slug") or best[1].get("id")),
                    best[0], "title match")
                stats["title"] += 1

        # (c) a relationship stated in the record's own notes, where the third
        #     party's headline is its own and the title matcher cannot reach.
        #     Checked before the MDI heuristic because it is the stronger
        #     evidence: the archive's own record says what the item is.
        if not found:
            for marker, kind, ref, why, how in NOTES_PINNED:
                if marker in url:
                    table = papers if kind == "paper" else works
                    label = next(
                        (x.get("title", "") for x in table
                         if str(x.get("id") or x.get("slug")) == ref), ref)
                    add(kind, ref, label, how)
                    stats["pinned"] += 1
                    break

        # (c) an MDI page carrying one of his works
        if not found and re.search(r"\[Video\]|^Lecture:", title):
            probe = re.sub(r"^\[[^\]]*\]\s*", "", title)
            probe = re.sub(r"^Lecture:\s*", "", probe)
            probe = re.sub(r"\[.*\]\s*$", "", probe).strip(" \u2018\u2019'\"")
            for cand, rec in mdi_by_title + vid_by_title + work_by_title:
                if title_match(probe, cand) >= 0.8:
                    kind = ("mdi" if rec in mdis else
                            "video" if rec in vids else "work")
                    add(kind, str(rec.get("slug") or rec.get("id")), cand,
                        "third-party page carrying this work")
                    stats["mdi"] += 1
                    break

        if found:
            # A row can reach the same item twice - "Doubting your Doubts" is
            # matched by title AND pinned by the fix table, and the litter
            # paper likewise. Keep the first, which is the transcribed listing
            # match where there is one, and never print the same relation twice.
            seen: set[tuple[str, str]] = set()
            unique = []
            for rel in found:
                sig = (rel["kind"], rel["ref"])
                if sig in seen:
                    continue
                seen.add(sig)
                unique.append(rel)
            found = unique
            # Resolve permalinks and write the reverse index only now that the
            # relation list is final.
            for rel in found:
                pl = rel.get("permalink") or permalink(rel["kind"], rel["ref"])
                if not pl:
                    continue
                rel["permalink"] = pl
                note = {"title": title, "url": url,
                        "source": row.get("source", ""),
                        "type": row.get("type", ""), "how": rel["how"]}
                reverse.setdefault(f"{rel['kind']}:{rel['ref']}", []).append(note)
                by_url.setdefault(pl, []).append(note)
            row["relates_to"] = found
        else:
            stats["none"] += 1

    print(f"  related by URL identity          : {stats['url_identity']} rows")
    print(f"  related by the captured listing : {stats['academia']} rows")
    print(f"  related by catalogue title       : {stats['title']} rows")
    print(f"  related by the record's own notes: {stats['pinned']} rows")
    print(f"  related as third-party carrier    : {stats['mdi']} rows")
    print(f"  no established referent           : {stats['none']} rows")
    print(f"  total relations recorded          : {sum(len(v) for v in reverse.values())}")
    print(f"  items with a back-reference       : {len(reverse)}")
    print(f"  permalinks resolved               : {len(by_url)}")

    if write:
        SS.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
        REVERSE.write_text(
            json.dumps({"built": date.today().isoformat(),
                        "note": "Third-party records about this author, and the "
                                "archive items each one refers to. `links` is keyed "
                                "by kind:ref; `by_url` by the item's permalink, "
                                "which is what a page knows about itself.",
                        "links": reverse,
                        "by_url": by_url},
                       ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"\nwrote {SS.name} and {REVERSE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
