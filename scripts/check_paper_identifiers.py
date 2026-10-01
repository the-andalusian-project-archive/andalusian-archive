"""The ScholarlyArticle `sameAs` must name WORKS, and must not repeat one.

Two failure modes, both live in the data rather than hypothetical.

1. AN AUTHOR PAGE IS NOT A WORK. `_data/registries.json` carries four Semantic
   Scholar records whose `registry_url` is

       https://www.semanticscholar.org/author/1412648752

   - the AUTHOR page, identical across all four records, each attached to a
   different `archive_paper_id`. Wiring that file's `same_as` into this template
   without a filter would emit, on a ScholarlyArticle, a claim that the paper is
   the same entity as a person. That is the one class of error this repository
   exists to avoid: it already spends `NOTICE.md` section 6 holding back two
   personal names precisely because entity confusion about this subject has
   caused real harm. A false identity claim in structured data is the same
   mistake, made machine-readable and spread by every consumer that reads it.

   The author-page URLs are therefore correct IN `registries.json` - that file is
   a survey of what each registry holds, and the Semantic Scholar entry for these
   works genuinely is an author-level record. They are simply not `sameAs`
   material for a paper.

2. A DOI IS CASE-INSENSITIVE, SO `10.65061/hdxb1161` AND `10.65061/HDXB1161`
   ARE ONE IDENTIFIER. The dedup in `_includes/jsonld.html` compares tokens
   case-sensitively, so Understanding Aisha's Age emitted both, reading in the
   structured data as two separate registry records when it is one. Harmless to
   a human reader; noise to every consumer, and exactly the kind of thing that
   makes an identifier untrustworthy.

This checks the RENDERED output, because the whole question is what a consumer
receives. Source-level checks cannot see it: both defects live in the join
between front matter, `_data/papers.json` and `_data/registries.json`.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

#: URL path segments that denote a PERSON or PROFILE rather than a work. Matched
#: case-insensitively against the path, so /Author/ and /author/ both count.
PROFILE_MARKERS = (
    "/author/", "/authors/", "/profile/", "/user/", "/users/",
    "/researcher", "/orcid/", "/people/",
)

#: Registries whose work identifiers are recognisable enough to allow-list.
#:
#: Every pattern carries IGNORECASE. The first version of this file lowercased
#: the path in order to catch `/Author/` case-insensitively, then matched that
#: lowercased path against `^/W\d+` with an uppercase-only pattern - so all six
#: legitimate OpenAlex identifiers were reported as malformed. The gate was then
#: wrong about correct data and not only about wrong data, which is worse: a
#: checker that cries wolf on good input teaches people to ignore it.
WORK_HOSTS = {
    "openalex.org": re.compile(r"^/W\d+$", re.I),
    "doi.org": re.compile(r"^/10\.\d{4,9}/\S+$", re.I),
    "www.doi.org": re.compile(r"^/10\.\d{4,9}/\S+$", re.I),
    "semanticscholar.org": re.compile(r"^/paper/", re.I),
    "www.semanticscholar.org": re.compile(r"^/paper/", re.I),
    "zenodo.org": re.compile(r"^/record/", re.I),
    "core.ac.uk": re.compile(r"^/(?:reader|works)/", re.I),
    "www.jstor.org": re.compile(r"^/stable/", re.I),
    "api.crossref.org": None,
}


def main() -> int:
    papers = sorted((SITE / "papers").rglob("index.html"))
    if not papers:
        print("FAIL: no built paper pages; run `bundle exec jekyll build` first")
        return 1

    fails: list[str] = []
    blocks = 0
    with_same = 0
    total_urls = 0

    # Which papers SHOULD carry identifiers. Derived from the registry survey
    # rather than hardcoded, so it stays true as records are added.
    #
    # Checking only the site-wide total was the first version, and it missed a
    # page losing its `sameAs` outright: 4 pages carried identifiers, one of
    # them stopped, the total went 11 -> 8, and nothing fired. A per-page
    # expectation is the check that actually catches it.
    expected: dict[int, str] = {}
    rp = ROOT / "_data" / "registries.json"
    pp = ROOT / "_data" / "papers.json"
    if rp.exists() and pp.exists():
        try:
            reg = json.loads(rp.read_text(encoding="utf-8"))
            papers_data = json.loads(pp.read_text(encoding="utf-8"))
            for r in reg.get("registries") or []:
                for rec in (r.get("records") or []) + (r.get("additional_records") or []):
                    pid = rec.get("archive_paper_id")
                    if pid is None:
                        continue
                    title = next((q.get("title", "") for q in papers_data
                                  if q.get("id") == pid), "")
                    expected[pid] = title
        except Exception as exc:  # noqa: BLE001
            print(f"  note: could not read the registry join ({exc}); the "
                  "per-paper expectation is disabled for this run")
            expected = {}

    seen_ids: set[int] = set()
    for p in papers:
        rel = p.relative_to(SITE).as_posix()
        html = p.read_text(encoding="utf-8", errors="replace")
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                              html, re.S):
            try:
                doc = json.loads(raw)
            except Exception:  # noqa: BLE001 - unparseable JSON is its own failure
                fails.append(f"{rel}: a ld+json block did not parse")
                continue
            for node in (doc.get("@graph") or [doc]):
                if node.get("@type") != "ScholarlyArticle":
                    continue
                blocks += 1
                same = node.get("sameAs") or []
                if same:
                    with_same += 1
                total_urls += len(same)

                headline = node.get("headline") or ""
                for pid, want in expected.items():
                    if want and want[:40].lower() in headline.lower():
                        seen_ids.add(pid)
                        if not same:
                            fails.append(
                                f"{rel}: the registry survey records verified "
                                f"identifiers for this work (paper id {pid}) but "
                                f"the page emits no sameAs at all")
                        break

                lowered: dict[str, str] = {}
                for u in same:
                    lu = u.lower()
                    if lu in lowered:
                        fails.append(
                            f"{rel}: sameAs repeats one identifier in two casings "
                            f"({lowered[lu]} and {u}). A DOI is case-insensitive, "
                            "so these are one record, not two.")
                    else:
                        lowered[lu] = u

                    path = urlparse(u).path.lower()
                    if any(m in path for m in PROFILE_MARKERS):
                        fails.append(
                            f"{rel}: sameAs names a PERSON, not a work: {u}. "
                            "Emitting this asserts the paper is the same entity "
                            "as a person.")
                        continue

                    host = urlparse(u).netloc.lower()
                    pat = WORK_HOSTS.get(host, ...)
                    if pat is ...:
                        fails.append(f"{rel}: sameAs host {host!r} is not on the "
                                     f"allow-list of registries that issue "
                                     f"identifiers: {u}")
                    elif pat is not None and not pat.match(path):
                        fails.append(f"{rel}: {u} does not look like a work "
                                     f"identifier on {host} (path {path!r})")

    print(f"  ScholarlyArticle blocks : {blocks}")
    print(f"  carrying sameAs         : {with_same}")
    print(f"  sameAs URLs total       : {total_urls}")
    if expected:
        missing = sorted(set(expected) - seen_ids)
        print(f"  papers the survey says have identifiers : {len(expected)}")
        if missing:
            fails.append(
                f"no page was matched for paper id(s) {missing}, which the "
                "registry survey records identifiers for. Either the join or "
                "the titles have drifted.")
    if not total_urls:
        fails.append("no sameAs anywhere; the identifier join produced nothing")

    if fails:
        seen = set()
        for f in fails:
            if f not in seen:
                seen.add(f)
                print(f"FAIL: {f}")
        print(f"check_paper_identifiers: {len(seen)} problem(s)")
        return 1
    print("check_paper_identifiers: 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
