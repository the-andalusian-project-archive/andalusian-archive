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
assert len(canon) == 72, f"works={len(canon)} != 72"
assert len(caps) == 87, f"captures={len(caps)} != 87"
assert sum(1 for w in canon if w["status"] == "lost") == 1
# Freeze gate (Reviewer A): builder assert is the other half; both must agree.
assert sum(1 for w in canon if w["status"] == "found") == 47
assert sum(1 for w in canon if w["status"] == "wayback_only") == 24

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

print(f"TEST_PASS works=72 captures=87 notices=3 "
      f"found={sum(1 for w in canon if w['status'] == 'found')} "
      f"wayback_only={sum(1 for w in canon if w['status'] == 'wayback_only')} "
      f"lost=1 (all found have >=200w local files, "
      f"{len(thin_seen)} audited exception(s); 0 collection/data drift)")
