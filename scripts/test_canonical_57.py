# scripts/test_canonical_57.py
# Quality-gated asserts (2026-09-07 bulk fetch 15 -> 31; 2026-09-08 junk-purge
# demotions 31 -> 30: lecture-series 52w stub, still-colonized 158w -> 76w;
# 2026-09-27 Task 7 / I1 integration: 57 -> 72 works - 15 recovered from the
# WordPress mirror + IDI, 2 stub-fills, lost 2 -> 1).
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_collections import (  # noqa: E402
    collection_drift, posts_by_front_matter_slug,
    articles_local_post_pointers, resolve_work_post)

base = pathlib.Path(__file__).parent.parent
canon = json.loads((base / "_data/canonical_works.json").read_text(encoding="utf-8"))
caps = json.loads((base / "_data/blog_posts.json").read_text(encoding="utf-8"))
notices = json.loads((base / "_data/notices.json").read_text(encoding="utf-8"))
# The approved recount, frozen. These are the figures the site publishes, so a
# data change that moves any of them is a change to a published number and must
# fail here rather than reach the built site.
assert len(canon) == 72, f"works={len(canon)} != 72"
assert len(caps) == 87, f"captures={len(caps)} != 87"
n_lost = sum(1 for w in canon if w["status"] == "lost")
n_found = sum(1 for w in canon if w["status"] == "found")
n_wayback = sum(1 for w in canon if w["status"] == "wayback_only")
assert n_lost == 1, f"lost={n_lost} != 1"
# Freeze gate (Reviewer A): builder assert is the other half; both must agree.
assert n_found == 47, f"found={n_found} != 47"
assert n_wayback == 24, f"wayback_only={n_wayback} != 24"
# The three status buckets must partition the catalogue. Without this, a fourth
# status value could be introduced and every count above would still pass while
# the published total silently stopped summing to 72.
assert n_found + n_wayback + n_lost == len(canon), (
    "status buckets do not partition the catalogue: %d + %d + %d != %d (a row "
    "must carry exactly one of found/wayback_only/lost)"
    % (n_found, n_wayback, n_lost, len(canon)))
assert {w["status"] for w in canon} == {"found", "wayback_only", "lost"}, (
    "unexpected status value(s): %s"
    % sorted({w["status"] for w in canon} - {"found", "wayback_only", "lost"}))
# The 24 Wayback-only works must hold no local text, or "no text held" is false.
for w in canon:
    if w["status"] == "wayback_only":
        assert not w.get("local_post"), \
            f"wayback_only work has a local post: {w['slug']}"
        assert not w.get("recovered_text_words"), \
            f"wayback_only work claims recovered words: {w['slug']}"

# Announcements are catalogued but must never be counted as works.
assert len(notices) == 3, f"notices={len(notices)} != 3"
assert all(n.get("counted_as_work") is False for n in notices), \
    "a notice is flagged counted_as_work"
assert not ({n["slug"] for n in notices} & {w["slug"] for w in canon}), \
    "a notice is also counted as a work"
# The 3 notices are catalogued, and the announcement text is preserved.
for n in notices:
    assert n.get("text", "").strip(), f"notice has no text: {n['slug']}"

try:
    log = {r["slug"]: r for r in json.loads(
        (base / "_data/recovery_log.json").read_text(encoding="utf-8"))}
except FileNotFoundError:
    log = {}

# Every found work must have a local _posts file with >=200 real words.
# THIN_ALLOWED is an explicit, audited exception list - not a lowered bar. A slug
# may only enter it with a recorded reason, and the work must still hold real
# recovered text. 2026-09-27: one entry, a lecture announcement whose substance is
# an embedded player (the same situation as 7 of the 17 MDI captions, which the
# brief directs be kept as published).
THIN_ALLOWED = {
    "contra-contemporary-atheism-lecture":
        "156 recovered words; the post announces a lecture whose substance is an "
        "embedded Farizmi player, so the prose is the caption. Genuine complete "
        "post, not a truncation - the whole capture is 52 KB and the article "
        "container holds nothing else.",
}
_by_fm = posts_by_front_matter_slug()
_pointers = articles_local_post_pointers()
thin_seen = set()
for w in canon:
    if w["status"] != "found":
        continue
    # N2 (re-review, 2026-09-27): resolve by SLUG. This line used to glob the
    # date and take matches[0], which reads whichever same-date file sorts first
    # rather than the one that belongs to this work.
    fname = resolve_work_post(w, _by_fm, _pointers)
    assert fname, f"found work has no _posts file: {w['slug']}"
    body = (base / "_posts" / fname).read_text(encoding="utf-8")
    text = body.split("---", 2)[-1] if body.count("---") >= 2 else body
    words = len(text.split())
    if words < 200:
        assert w["slug"] in THIN_ALLOWED, \
            f"found work thin ({words}w): {w['slug']}"
        assert words >= 100, \
            f"allowlisted thin work is under 100w: {w['slug']} ({words}w)"
        thin_seen.add(w["slug"])
# An exception that is no longer needed must be removed, not left to rot.
assert thin_seen == set(THIN_ALLOWED), (
    "THIN_ALLOWED lists works that are no longer thin: %s"
    % sorted(set(THIN_ALLOWED) - thin_seen))

# N2 regression, stated directly: a date is not an identity. Two files share
# 2015-05-12 and must resolve to two different works. Under the old date-only
# join both were attributed to the found work and the wayback_only work's file
# vanished from the unclaimed list.
_collide = {w["date"]: [] for w in canon}
for w in canon:
    _collide.setdefault(w["date"], []).append(w["slug"])
_shared = sorted(d for d, slugs in _collide.items() if len(slugs) > 1)
for date in _shared:
    files = sorted((base / "_posts").glob(date + "-*.md"))
    if len(files) < 2:
        continue
    for f in files:
        raw = f.read_text(encoding="utf-8")
        m = re.search(r"^slug:\s*(.+?)\s*$", raw.split("---", 2)[1], re.M)
        # A file identifies its work either by front-matter slug or by the
        # <date>-<slug> filename; 12 files carry only the latter.
        owner = m.group(1).strip() if m else f.stem
        if owner not in {w["slug"] for w in canon if w["date"] == date}:
            owner = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", f.stem)
        assert owner in {w["slug"] for w in canon if w["date"] == date}, (
            "file %s is attributed to no work dated %s" % (f.name, date))


# N1 (re-review, 2026-09-27): every MDI row must state an evidence class, and
# the class must match what the string actually claims. Nothing gated
# _data/mdi_articles.json before this, which is how 13 evidence strings came to
# assert a text comparison nobody had made. A row that cannot be proven may
# still be catalogued as a duplicate, but it must say the link is inferred.
mdi = json.loads((base / "_data/mdi_articles.json").read_text(encoding="utf-8"))
assert len(mdi) == 17, f"mdi rows={len(mdi)} != 17"
work_slugs = {w["slug"] for w in canon}
CLASSES = {"text_proven", "work_row_only", "counted"}
for r in mdi:
    slug, klass = r["slug"], r.get("evidence_class")
    assert klass in CLASSES, f"{slug}: no/unknown evidence_class {klass!r}"
    counted = r.get("counted_as_work", True) is not False
    assert (klass == "counted") == counted, \
        f"{slug}: evidence_class={klass} but counted_as_work={counted}"
    if counted:
        assert r.get("counted_as_work_evidence", "").strip(), \
            f"{slug}: counted with no evidence string"
        assert not r.get("duplicate_of"), f"{slug}: counted but has duplicate_of"
        continue
    dup, ev = r.get("duplicate_of"), r.get("duplicate_evidence", "")
    assert dup in work_slugs, f"{slug}: duplicate_of {dup!r} is not a work"
    # No dedup chain: the work a row points at must not itself be deduped to
    # something else. A row may share its work's slug (naked-kings-… does), so
    # self is excluded.
    assert dup not in {x["slug"] for x in mdi
                       if x.get("counted_as_work") is False
                       and x["slug"] != slug}, \
        f"{slug}: duplicate_of {dup!r} is itself a deduped MDI row"
    assert ev.strip(), f"{slug}: not counted with no evidence string"
    # The N1 core: a work-row-only row must NOT assert the texts were shown to
    # be the same, and must disclose that they were not comparable.
    if klass == "work_row_only":
        assert "INFERRED, NOT PROVEN" in ev, \
            f"{slug}: work_row_only row does not disclose the inference"
        assert "could not be compared" in ev, \
            f"{slug}: work_row_only row does not say why it could not compare"
        assert isinstance(r.get("containment"), (int, float)), \
            f"{slug}: work_row_only row must record the measured containment"
    else:
        c = r.get("containment")
        assert isinstance(c, (int, float)) and c >= 0.90, \
            f"{slug}: text_proven row needs a measured containment >= 0.90, got {c!r}"
        assert r.get("measured_against", "").endswith(".md"), \
            f"{slug}: text_proven row must name the local file compared against"
n_mdi_counted = sum(1 for r in mdi if r.get("counted_as_work", True) is not False)
n_mdi_dupes = len(mdi) - n_mdi_counted
# The MDI double count, frozen. 17 rows are catalogued and 4 are distinct items;
# the site publishes both numbers, and the MDI term in total_content is the 4.
assert n_mdi_counted == 4, f"mdi counted={n_mdi_counted} != 4"
assert n_mdi_dupes == 13, f"mdi republished={n_mdi_dupes} != 13"

# Every wayback_only work must carry fetch provenance from the bulk run.
for w in canon:
    if w["status"] != "wayback_only":
        continue
    assert w["slug"] in log, f"wayback_only missing recovery_log row: {w['slug']}"

# C1 (review-phase2): no generated collection may drift from its data file.
# The reviewed commit shipped a 67-row video catalogue against 68 _videos/ pages
# (11 search results 404'd, 12 uncounted videos stayed public) and no suite
# noticed. This is the gate. Run scripts/build_collections.py to fix.
drift = collection_drift()
assert not drift, "collection/data drift:\n  " + "\n  ".join(drift)

# The published total, computed here from the same files the builder reads, and
# checked against the string the site prints. The site says
#   Total 207 = 72 + 68 + 20 + 4 + 9 + 33 + 1
# so this assert fails if any term moves OR if content_index.json's stored total
# and its own stored formula stop agreeing with the data they summarise.
videos = json.loads((base / "_data/videos.json").read_text(encoding="utf-8"))
papers = json.loads((base / "_data/papers.json").read_text(encoding="utf-8"))
yaqeen = json.loads((base / "_data/yaqeen_papers.json").read_text(encoding="utf-8"))
albalagh = json.loads((base / "_data/albalagh_courses.json").read_text(encoding="utf-8"))
interviews = json.loads(
    (base / "_data/external_interviews.json").read_text(encoding="utf-8"))
terms = {
    "works": len(canon),
    "videos": len(videos),
    "papers": len(papers),
    "mdi_counted": n_mdi_counted,
    "yaqeen_linkouts": len(yaqeen),
    "albalagh_linkouts": len(albalagh),
    "interviews": len(interviews),
}
expected_total = sum(terms.values())
assert expected_total == 207, (
    "total_content computed from _data/ is %d, not the approved 207: %r"
    % (expected_total, terms))
ci = json.loads((base / "_data/content_index.json").read_text(encoding="utf-8"))
ci_stats = ci["statistics"]
assert ci_stats["total_content"] == expected_total, (
    "content_index.json total_content=%r but _data/ sums to %d; the published "
    "total has drifted from the data" % (ci_stats.get("total_content"),
                                         expected_total))
# The stored terms must be the data's terms, not a second set of numbers.
assert ci_stats["total_content_terms"] == terms, (
    "content_index.json total_content_terms=%r != the data's %r"
    % (ci_stats.get("total_content_terms"), terms))
# The published formula string must name every term, and the numbers it names
# must be the numbers above - so the arithmetic a reader can see is the
# arithmetic that was actually performed.
formula = ci_stats["total_content_formula"]
for label, value in (("works", terms["works"]), ("videos", terms["videos"]),
                     ("papers", terms["papers"]),
                     ("MDI items", terms["mdi_counted"]),
                     ("Yaqeen link-outs", terms["yaqeen_linkouts"]),
                     ("Al Balagh link-outs", terms["albalagh_linkouts"]),
                     ("interview", terms["interviews"])):
    assert ("%d %s" % (value, label)) in formula, (
        "published formula does not state '%d %s': %s" % (value, label, formula))
assert ("= %d " % expected_total) in formula, (
    "published formula does not state the total %d: %s" % (expected_total, formula))
# The announcements and the derived secondary sources are catalogued and must
# stay outside the total, or the site is counting the archive against itself.
assert ci_stats["total_notices"] == 3, f"notices={ci_stats['total_notices']} != 3"
secondary = json.loads(
    (base / "_data/secondary_sources.json").read_text(encoding="utf-8"))
assert ci_stats["total_secondary_sources"] == len(secondary), (
    "secondary_sources count %r != %d rows"
    % (ci_stats.get("total_secondary_sources"), len(secondary)))
assert all(s.get("counted_as_content") is False for s in secondary), \
    "a third-party source record is flagged counted_as_content"

print(f"TEST_PASS works={len(canon)} captures={len(caps)} notices={len(notices)} "
      f"found={n_found} wayback_only={n_wayback} lost={n_lost} "
      f"mdi={n_mdi_counted}/{len(mdi)} (all found have >=200w local files, "
      f"{len(thin_seen)} audited exception(s); 0 collection/data drift; "
      f"total_content={expected_total} matches the published formula)")
