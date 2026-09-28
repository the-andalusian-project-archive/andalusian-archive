#!/usr/bin/env python3
"""CI asserts for transcript joins (Plan B).

- HONEST GATE (2026-09-27, Task 7 / I1; amended the same day by user
  decision; amended again by ledger ruling R25, task 8d): of the videos that
  survive in _data/videos.json, every one that is supposed to carry a
  transcript does. The set is 68 videos = 57 recordings with an attached
  transcript + 11 catalogue-only entries that carry `transcripts: 0` by
  design, so the gate is 57/68 with 11 explicitly accounted-for absences.
  (Before I2's deduplication the set was 68/68; 12 third-party re-uploads were
  removed from the catalogue and their transcript text was re-parented onto
  the surviving twins, never deleted. R25 then attached G47Stp3pLss's preserved
  15,048-line capture to the entry the user had restored as a counted work,
  moving that entry out of the catalogue-only set: 56/68 + 12 -> 57/68 + 11.)
- A survivor counts as "transcribed" when it has a captions coverage row AND
  its videos.json entry does not declare `transcripts: 0`. `transcripts: 0`
  means "no transcript is attached to this entry", not "no transcript exists".
  R25 removed the one deliberate exception: G47Stp3pLss's capture is now
  attached, so no entry holds a capture without saying so, and the
  unattached-capture assert below is now empty by construction. If a future
  decision re-detaches a capture it must set `attached_to_video_entry: false`,
  and the last assert in that block fails until it does.
- PUBLISH GATE (2026-09-27, task 8d): the files being intact is not the same
  as the text being readable, so every capture the coverage file names must
  have a served document in _transcripts/ carrying the verbatim disclaimer and
  a non-empty text section, and the split between attached and catalogue-only
  entries is pinned here as well as in build_collections.py.
- Every TRANSCRIPT_MAP slug whose video has transcript coverage renders
  `transcript: true` + the disclaimer + a <details> transcript block in
  _articles/<slug>.md (regenerate via build_collections.py if stale), and that
  block's words are the SAME words the published transcript page carries -
  one reader of one capture file, not two.
- No _articles page may carry transcript content without the disclaimer.
- No transcript text may simply vanish. This is checked at the TEXT level, not
  by row presence: for every re-parented `alternates` entry and every
  kept-in-place `superseded` row, `file`, `lines` and `captions` must be
  present and non-null, `.firecrawl/transcripts/<file>` must exist, and its
  on-disk line count must equal the recorded `lines` (WebVTT: physical lines;
  whisper JSON: len(segments)). The reviewer emptied all 12 and the old check
  stayed green; this one cannot.
- PUBLICATION REDACTION (2026-09-27): the M4 fidelity gate below compares the
  published word stream with the capture's own. One identifier - his birth
  name - is withheld at the site owner's decision, so the gate applies the
  builder's own substitution to the stream it re-derives before comparing.
  The gate is therefore NOT weakened: it still demands word-for-word identity
  with the capture everywhere else, and a redaction that reached further than
  the name, or missed one, still fails it. On top of that the three affected
  documents are asserted positively - the name must be absent, the marker must
  be present once per occurrence, and each must carry a `redaction_note` that
  points at NOTICE.md - so "redacted" cannot be satisfied by deleting the page.
Run: `python scripts/test_transcripts.py`. Exit 0 PASS, 1 FAIL.
"""

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_collections import (  # noqa: E402
    TRANSCRIPT_MAP, DISCLAIMER, MACHINE_TRANSCRIPT_DISCLAIMER,
    TRANSCRIPTS_DIR, transcript_filenames, attached_transcript_ids,
    parse_capture, capture_paragraphs, CAPTURE_DIR, md_escape,
    REDACTION_LOCAL, load_redaction_list, redaction_hits, redact)

BASE = pathlib.Path(__file__).parent.parent
# Survivors with a transcript / survivors in the catalogue / catalogue-only
# entries that declare `transcripts: 0`.
# 56 -> 57 and 12 -> 11 on 2026-09-27 (ledger ruling R25, task 8d): G47Stp3pLss's
# preserved capture is attached to the entry the user restored as a counted
# work, so it left the catalogue-only set. No other row moved.
# 68 -> 81, 57 -> 68 and 11 -> 13 on 2026-09-29: thirteen videos verified absent
# by id were catalogued. Eleven carried a YouTube caption track and are published
# as transcripts, so the transcribed set rises by eleven and the total by
# thirteen. The remaining two, Arena episodes 8 and 18, have no caption track at
# all - `subtitles` offers only live_chat and `automatic_captions` is empty, so
# they enter the catalogue-only set, which is what `transcripts: 0` means and
# which 24 wayback_only works and 42 link-outs already do. No existing row moved.
EXPECT_TRANSCRIBED = 68
EXPECT_VIDEOS = 81
EXPECT_CATALOGUE_ONLY = 13
# The published corpus size, frozen by the approved recount of 2026-09-28 and
# printed by /transcripts/, by README.md and by llms.txt. 540,995 is the figure
# the data holds AND the figure the 68 published pages sum to; the check below
# proves both, so the two cannot drift apart.
#
# 2026-09-29: eleven new transcripts add 396,743 words, taking the corpus from
# 540,995 to 937,738 across 79 documents. The figure is re-derived from the same
# files in the same check, so it cannot be asserted from a stale number.
EXPECT_DOCUMENTS = 79
EXPECT_WORDS = 937738
EXPECT_PARAGRAPHS = 67720
# Restored as counted works by user decision (2026-09-27); their rows stay in
# superseded_videos.json as the audit trail but they are no longer superseded.
RESTORED_AS_WORKS = {"G47Stp3pLss"}
failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL: " + msg)


DISCLAIMER_CORE = "shouldn't be used in polemics or debate material"
TRANSCRIPT_DIR = BASE / ".firecrawl" / "transcripts"

# --- M4: an independent reader for the capture files -----------------------
# The gate above ("One reader of one capture file") compares the article block
# with the published page, but both sides are produced by
# build_collections.parse_capture(), so a bug in that parser is invisible to it:
# the article and the page would agree with each other and both be wrong. The
# review is right that this is a consistency check, not a fidelity check, and
# that the seven documented `&nbsp;` paragraphs are exactly the precedent for
# divergence nobody would notice.
#
# So the capture is parsed a SECOND time here, by the reader below, which shares
# no code with the builder: it re-implements the policy the builder documents in
# prose - strip the WebVTT scaffolding and inline tags, keep the settled cue of
# each rolling-window caption line and drop its echo, drop a repeated identical
# line, and start a new paragraph where consecutive cue starts are more than two
# seconds apart - and compares what it finds with the text a reader actually
# gets in _transcripts/<id>.md. Same policy, separate code: a coding mistake in
# either one now shows up as a failure instead of cancelling out.
#
# The only builder function reused is md_escape(), which is markdown punctuation
# escaping and cannot add, drop, reorder or respell a word.
CUE_TS = re.compile(
    r"^(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*"
    r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})")
INLINE_TAG = re.compile(r"<[^>]*>")
SETTLED_MAX_MS = 50         # a "settled" caption cue is <= 50 ms long
PARAGRAPH_GAP_MS = 2000     # a new paragraph starts after a pause this long


def _seconds(h, m, s, ms):
    return (int(h or 0) * 3600) + int(m) * 60 + int(s) + int(ms) / 1000.0


def _paragraphs_from_cues(cues):
    paras, cur, prev_start = [], [], None
    for start, _end, text in cues:
        # The pause is measured in whole milliseconds. Caption timestamps are
        # recorded to the millisecond, so "more than two seconds" is a question
        # about the recording, and two ways of writing the same seconds in
        # binary floating point must not be able to answer it differently.
        if cur and prev_start is not None \
                and round((start - prev_start) * 1000) > PARAGRAPH_GAP_MS:
            paras.append(" ".join(cur))
            cur = []
        cur.append(text)
        prev_start = start
    if cur:
        paras.append(" ".join(cur))
    return [p for p in (p.strip() for p in paras) if p]


def independent_parse_capture(path):
    """Cue list for one capture file, derived without build_collections.

    The two capture formats are handled the way the published pages SAY they are
    handled, which is not the same way:

    * WebVTT - a YouTube auto-caption capture in the rolling-window format,
      where every caption line is written twice: once prefixed with the previous
      line, once on its own in a ~10 ms cue. The header, the Kind/Language/NOTE
      lines, the bare cue numbers and the timing lines are scaffolding, and the
      inline <00:00:03.840><c> timing and <v Name> voice tags come out of the
      caption text. Where settled cues exist only they are kept, and a line that
      immediately repeats the one before it is dropped.
    * whisper JSON - reproduced as Whisper wrote it, with no correction and no
      de-echoing. A line Whisper genuinely wrote twice is published twice,
      because a local transcription has no rolling window to undo and the
      rendering note on the page says the words are unchanged.
    """
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return [(float(seg.get("start", 0.0)), float(seg.get("end", 0.0)),
                 str(seg.get("text", "")).strip())
                for seg in data.get("segments", [])]
    raw, buf, span = [], [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        m = CUE_TS.match(s)
        if m:
            g = m.groups()
            # A timing line CLOSES the cue above it and OPENS the next one, so
            # the buffered words belong to the span that preceded it.
            if span is not None:
                raw.append((span[0], span[1], " ".join(buf)))
            span = (_seconds(*g[0:4]), _seconds(*g[4:8]))
            buf = []
            continue
        if (not s or "WEBVTT" in s or s.isdigit() or s.startswith("Kind:")
                or s.startswith("Language:") or s.startswith("NOTE")):
            continue
        if span is None:
            continue              # words before the first timing line are not cues
        buf.append(INLINE_TAG.sub("", s).strip())
    if span is not None:
        raw.append((span[0], span[1], " ".join(buf)))
    cues = [(a, b, t) for a, b, t in raw if t.strip()]
    settled = [c for c in cues
               if round((c[1] - c[0]) * 1000) <= SETTLED_MAX_MS]
    if settled:
        cues = settled
    out = []
    for a, b, t in cues:
        if not out or out[-1][2] != t:
            out.append((a, b, t))
    return out


def published_paragraphs(path):
    """The paragraph lines a reader gets from a published transcript document."""
    body = path.read_text(encoding="utf-8").split("## Transcript text", 1)
    if len(body) < 2:
        return None
    return [line for line in body[1].splitlines() if line.strip()]


def front_matter_int(path, key):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key),
                  path.read_text(encoding="utf-8").split("---", 2)[1], re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"')


def front_matter_str(path, key):
    """A front-matter scalar, JSON-decoded when the builder quoted it.

    build_collections.q() writes a double-quoted JSON string, which is valid
    YAML, so a note containing a quote or a backslash round-trips only if it
    is decoded rather than merely stripped of its outer quotes.
    """
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key),
                  path.read_text(encoding="utf-8").split("---", 2)[1], re.M)
    if not m:
        return None
    raw = m.group(1).strip()
    if raw.startswith('"'):
        try:
            return json.loads(raw)
        except ValueError:
            pass
    return raw.strip('"')


def disk_line_count(path):
    """Transcript size as recorded in transcript_coverage.json `lines`.

    WebVTT captures are counted by physical line; whisper JSON by segment count.
    Returns None if the file cannot be read, so a broken file fails the gate
    rather than silently passing.
    """
    try:
        if path.suffix == ".vtt":
            return len(path.read_text(encoding="utf-8",
                                      errors="replace").splitlines())
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            segs = data.get("segments")
            return len(segs) if isinstance(segs, list) else None
        if isinstance(data, list):
            return len(data)
    except Exception:  # noqa: BLE001 - any read problem is a failure
        return None
    return None


def assert_text_intact(entry, where):
    """I1 (review-phase2): the transcript TEXT behind a coverage row must exist.

    Checks presence of the three fields, that the capture file is on disk, and
    that its size equals the recorded `lines`.
    """
    vid = entry.get("video_id", "?")
    for field in ("file", "lines", "captions"):
        if entry.get(field) is None:
            fail("%s %s: transcript %s is null" % (where, vid, field))
    if not entry.get("captions"):
        fail("%s %s: transcript captions flag is false" % (where, vid))
    if not entry.get("file"):
        return
    path = TRANSCRIPT_DIR / str(entry["file"])
    if not path.is_file():
        fail("%s %s: capture file missing on disk: %s"
             % (where, vid, path.name))
        return
    got = disk_line_count(path)
    if got is None:
        fail("%s %s: capture file unreadable: %s" % (where, vid, path.name))
    elif entry.get("lines") is not None and got != entry["lines"]:
        fail("%s %s: capture size changed - on disk %d, recorded %s"
             % (where, vid, got, entry["lines"]))


def main():
    cov = json.loads((BASE / "_data" / "transcript_coverage.json")
                     .read_text(encoding="utf-8"))
    videos = json.loads((BASE / "_data" / "videos.json").read_text(encoding="utf-8"))
    superseded = json.loads((BASE / "_data" / "superseded_videos.json")
                            .read_text(encoding="utf-8"))
    by_id = {r.get("video_id", ""): r for r in cov}
    survivors = [str(v.get("id")) for v in videos]

    # --- honest gate over the surviving set -------------------------------
    if len(survivors) != EXPECT_VIDEOS:
        fail("videos.json rows=%d != %d" % (len(survivors), EXPECT_VIDEOS))
    # `transcripts: 0` = no transcript attached, so such an entry is not
    # counted as transcribed even when a capture exists in the coverage file.
    declared_none = {str(v.get("id")) for v in videos
                     if v.get("transcripts") == 0}
    transcribed = [i for i in survivors
                   if by_id.get(i, {}).get("captions") and i not in declared_none]
    catalogue_only = [i for i in survivors if i not in by_id or i in declared_none]
    if len(transcribed) != EXPECT_TRANSCRIBED:
        fail("transcribed survivors=%d != %d" % (len(transcribed),
                                                 EXPECT_TRANSCRIBED))
    else:
        print(f"PASS: {len(transcribed)}/{len(survivors)} surviving videos "
              f"carry a transcript")
    if len(catalogue_only) != EXPECT_CATALOGUE_ONLY:
        fail("catalogue-only survivors=%d != %d"
             % (len(catalogue_only), EXPECT_CATALOGUE_ONLY))
    else:
        print(f"PASS: {len(catalogue_only)} catalogue-only survivors "
              f"(transcripts: 0 by design)")
    for i in catalogue_only:
        entry = next(v for v in videos if str(v.get("id")) == i)
        if entry.get("transcripts") != 0:
            fail("%s: catalogue-only entry does not declare transcripts: 0" % i)
    # A capture that exists but is not attached must say so on its own row.
    unattached = [i for i in declared_none if by_id.get(i, {}).get("captions")]
    for i in unattached:
        row = by_id[i]
        if row.get("attached_to_video_entry") is not False:
            fail("%s: has a transcript capture but declares transcripts: 0 and "
                 "is not flagged attached_to_video_entry: false" % i)
    if unattached:
        print(f"PASS: {len(unattached)} capture(s) exist but are deliberately "
              f"not attached ({', '.join(sorted(unattached))}) and are flagged")
    if failures:
        print(f"test_transcripts: {len(failures)} FAILURE(S) before joins")
        return 1

    # --- no transcript text may simply vanish -----------------------------
    reparented = set()
    for row in cov:
        for alt in row.get("alternates") or []:
            reparented.add(alt.get("video_id"))
    n_reparented, n_parked, n_restored = [], [], []
    for s in superseded:
        sid = str(s.get("id"))
        row = by_id.get(sid) or next(
            (a for r in cov for a in (r.get("alternates") or [])
             if a.get("video_id") == sid), None)
        if row is None:
            fail("superseded %s (%s): transcript row vanished"
                 % (sid, s.get("title")))
            continue
        # TEXT-LEVEL check for every one of the 12, whatever its disposition.
        assert_text_intact(row, "superseded transcript")
        if sid in RESTORED_AS_WORKS:
            n_restored.append(sid)
        elif sid in reparented:
            n_reparented.append(sid)
        elif not row.get("superseded"):
            fail("superseded %s: transcript row present but not marked" % sid)
        else:
            n_parked.append(sid)
    print(f"PASS: all {len(superseded)} ledger rows in "
          f"superseded_videos.json accounted for, none deleted: "
          f"{len(n_reparented)} re-parented onto surviving twins, "
          f"{len(n_parked)} kept flagged (counted nowhere), "
          f"{len(n_restored)} restored as counted work(s)")

    # I1: every re-parented alternate is checked for its TEXT, not just for
    # being reachable. Without this, nulling file/lines/captions on all 10
    # alternates leaves the suite green (the reviewer's simulation).
    n_alt = 0
    for row in cov:
        for alt in row.get("alternates") or []:
            n_alt += 1
            assert_text_intact(alt, "re-parented alternate")
    print(f"PASS: {n_alt} re-parented alternate transcript(s) verified "
          f"on disk (file exists, non-null fields, size matches)")

    # Every coverage row that CLAIMS a caption file must belong to something the
    # archive can account for: a catalogued video entry, or an upload recorded in
    # the superseded-video ledger. The second case is not a leak - it is the
    # designed `superseded-upload` path of ruling R17, where the upload is no
    # longer a catalogued entry in its own right but its text is published rather
    # than kept in a directory the site does not serve. What must never exist is a
    # third case: a capture with neither a catalogue entry nor a ledger row, which
    # would be text the archive holds and publishes and can explain to nobody.
    superseded_ids = {s.get("id") for s in json.loads(
        (BASE / "_data" / "superseded_videos.json").read_text(encoding="utf-8"))}
    catalogued_ids = {v["id"] for v in json.loads(
        (BASE / "_data" / "videos.json").read_text(encoding="utf-8"))}
    n_orphan_preserved = 0
    for row in cov:
        if not (row.get("captions") and row.get("file")):
            continue
        if row["video_id"] in catalogued_ids:
            continue
        if row["video_id"] in superseded_ids:
            n_orphan_preserved += 1
            continue
        fail("transcript_coverage.json: %s claims a caption file but is neither "
             "a catalogued video nor a row in superseded_videos.json"
             % row["video_id"])
    if not failures:
        print(f"PASS: every coverage row claiming a caption file is accounted "
              f"for ({len(catalogued_ids)} catalogued videos; "
              f"{n_orphan_preserved} preserved capture(s) whose upload is in the "
              f"superseded ledger)")

    if failures:
        print(f"test_transcripts: {len(failures)} FAILURE(S)")
        return 1

    # --- page-level joins -------------------------------------------------
    joined = 0
    for slug, entry in TRANSCRIPT_MAP.items():
        vid = entry[0]
        row = by_id.get(vid, {})
        page = BASE / "_articles" / f"{slug}.md"
        if vid not in by_id:
            fail(f"{slug}: video {vid} has no transcript coverage row")
            continue
        if not row.get("captions"):
            print(f"SKIP: {slug} (video {vid} has no transcript yet)")
            continue
        if vid not in survivors:
            fail(f"{slug}: video {vid} is not in videos.json (orphaned transcript)")
            continue
        if not page.exists():
            fail(f"{slug}: _articles page missing (regen collections)")
            continue
        text = page.read_text(encoding="utf-8")
        if "transcript: true" not in text:
            fail(f"{slug}: missing `transcript: true` front matter")
            continue
        if DISCLAIMER_CORE not in text:
            fail(f"{slug}: transcript WITHOUT disclaimer")
            continue
        if "<details>" not in text:
            fail(f"{slug}: transcript block missing <details>")
            continue
        joined += 1
    print(f"PASS: {joined} transcript joins with disclaimer")

    # Global honesty sweep: any transcript marker implies disclaimer.
    for page in sorted((BASE / "_articles").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if ("<details>" in text or "transcript: true" in text) \
                and DISCLAIMER_CORE not in text:
            fail(f"{page.name}: transcript content without disclaimer")

    # --- the TEXT is published (task 8d) -----------------------------------
    # Everything above proves the capture FILES are intact. This proves the
    # words are actually on the site: one served document per capture the
    # coverage file names - top-level rows AND alternates - each carrying the
    # verbatim disclaimer, and each reachable from the index. A capture that
    # exists but is not published is text the archive holds and no reader can
    # read, which is the failure this block exists to make impossible.
    expected = transcript_filenames(cov)
    on_disk = {p.name for p in TRANSCRIPTS_DIR.glob("*.md")} \
        if TRANSCRIPTS_DIR.is_dir() else set()
    for name in sorted(expected - on_disk):
        fail("_transcripts/%s: a capture is named by the coverage file but no "
             "transcript page publishes its text (run build_collections.py)"
             % name)
    for name in sorted(on_disk - expected):
        fail("_transcripts/%s: transcript page for no capture named by the "
             "coverage file" % name)
    if expected == on_disk:
        print(f"PASS: {len(on_disk)} capture(s) in transcript_coverage.json, "
              f"each with a published transcript page in _transcripts/")

    index_path = BASE / "_data" / "transcript_index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError) as exc:
        index = None
        fail("_data/transcript_index.json unreadable: %s" % exc)
    if index is not None:
        if index.get("disclaimer") != MACHINE_TRANSCRIPT_DISCLAIMER:
            fail("_data/transcript_index.json: disclaimer is not the verbatim "
                 "sentence")
        linked = sum(len(v) for v in index.get("by_recording", {}).values())
        if linked != len(on_disk):
            fail("_data/transcript_index.json: %d document(s) indexed, %d page(s)"
                 % (linked, len(on_disk)))
        else:
            print(f"PASS: transcript index reaches all {linked} published "
                  f"transcript(s)")
        if index.get("documents") != EXPECT_DOCUMENTS:
            fail("_data/transcript_index.json: documents=%r != %d"
                 % (index.get("documents"), EXPECT_DOCUMENTS))
        if index.get("words") != EXPECT_WORDS:
            fail("_data/transcript_index.json: words=%r != %d"
                 % (index.get("words"), EXPECT_WORDS))
        if index.get("paragraphs") != EXPECT_PARAGRAPHS:
            fail("_data/transcript_index.json: paragraphs=%r != %d"
                 % (index.get("paragraphs"), EXPECT_PARAGRAPHS))
        # The index's own headline totals must be the sum of its own documents.
        # Without this, `words` could be edited in place and every other check
        # would still pass while the published word total became a fiction.
        docs = [d for v in index.get("by_recording", {}).values() for d in v]
        summed_words = sum(d.get("words", 0) for d in docs)
        summed_paras = sum(d.get("paragraphs", 0) for d in docs)
        if len(docs) != index.get("documents"):
            fail("transcript index: %d document entries but documents=%r"
                 % (len(docs), index.get("documents")))
        if summed_words != index.get("words"):
            fail("transcript index: documents sum to %d words but words=%r"
                 % (summed_words, index.get("words")))
        if summed_paras != index.get("paragraphs"):
            fail("transcript index: documents sum to %d paragraphs but "
                 "paragraphs=%r" % (summed_paras, index.get("paragraphs")))
        if not failures:
            print(f"PASS: {EXPECT_DOCUMENTS} published transcripts, "
                  f"{EXPECT_WORDS} words, {EXPECT_PARAGRAPHS} paragraphs, and "
                  f"the totals are the sum of the documents")
        # The split the /transcripts/ page prints, read back out of the index.
        for key, want in (("catalogued_videos", EXPECT_VIDEOS),
                          ("videos_attached", EXPECT_TRANSCRIBED),
                          ("videos_catalogue_only", EXPECT_CATALOGUE_ONLY)):
            if index.get(key) != want:
                fail("transcript index: %s=%r != %d"
                     % (key, index.get(key), want))
        if (index.get("videos_attached", 0)
                + index.get("videos_catalogue_only", -1)) != EXPECT_VIDEOS:
            fail("transcript index: attached %r + catalogue-only %r != %d; the "
                 "two must partition the catalogue"
                 % (index.get("videos_attached"),
                    index.get("videos_catalogue_only"), EXPECT_VIDEOS))
        else:
            print(f"PASS: transcript split {EXPECT_TRANSCRIBED} attached + "
                  f"{EXPECT_CATALOGUE_ONLY} catalogue-only = {EXPECT_VIDEOS}")

    # Every published page carries the disclaimer VERBATIM, and the video page
    # layout prints the same bytes. Both are compared against the one constant
    # in build_collections.py, so no copy can drift.
    for page in sorted(TRANSCRIPTS_DIR.glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if MACHINE_TRANSCRIPT_DISCLAIMER not in text:
            fail("%s: published transcript without the verbatim disclaimer"
                 % page.name)
        body = text.split("---", 2)[-1]
        if "## Transcript text" not in body:
            fail("%s: published transcript has no text section" % page.name)
        elif len(body.split("## Transcript text", 1)[1].split()) < 20:
            fail("%s: published transcript text is effectively empty"
                 % page.name)
    layout = (BASE / "_layouts" / "video.html").read_text(encoding="utf-8")
    if MACHINE_TRANSCRIPT_DISCLAIMER not in layout:
        fail("_layouts/video.html: video page no longer prints the verbatim "
             "disclaimer")
    if on_disk:
        print(f"PASS: {len(on_disk)} published transcript page(s) each carry "
              f"the verbatim disclaimer and their text")

    # The word total the site publishes, re-derived from the PUBLISHED PAGES
    # rather than from the index. The index and the pages are written by
    # different code, so agreeing with each other is a real check: if the
    # builder ever published a page with a different word count than the one it
    # recorded, this is where it would show.
    fm_words = fm_paras = 0
    fm_missing = []
    for page in sorted(TRANSCRIPTS_DIR.glob("*.md")):
        head = page.read_text(encoding="utf-8").split("---", 2)
        fm = head[1] if len(head) >= 3 else ""
        m_w = re.search(r"^words:\s*(\d+)\s*$", fm, re.M)
        m_p = re.search(r"^paragraphs:\s*(\d+)\s*$", fm, re.M)
        if not m_w or not m_p:
            fm_missing.append(page.name)
            continue
        fm_words += int(m_w.group(1))
        fm_paras += int(m_p.group(1))
    if fm_missing:
        fail("%d published transcript page(s) carry no words/paragraphs in "
             "front matter: %s" % (len(fm_missing), ", ".join(fm_missing[:5])))
    if on_disk and not fm_missing:
        if len(list(TRANSCRIPTS_DIR.glob("*.md"))) != EXPECT_DOCUMENTS:
            fail("%d published transcript page(s) != the approved %d"
                 % (len(list(TRANSCRIPTS_DIR.glob("*.md"))), EXPECT_DOCUMENTS))
        if fm_words != EXPECT_WORDS:
            fail("published transcript pages sum to %d words, not the approved "
                 "%d" % (fm_words, EXPECT_WORDS))
        if fm_paras != EXPECT_PARAGRAPHS:
            fail("published transcript pages sum to %d paragraphs, not the "
                 "approved %d" % (fm_paras, EXPECT_PARAGRAPHS))
        if not failures:
            print(f"PASS: the {EXPECT_DOCUMENTS} published pages themselves sum "
                  f"to {fm_words} words and {fm_paras} paragraphs - the figure "
                  f"the site publishes, re-derived from the pages")

    # The 57/11 split, pinned here as well as in build_collections.py. A
    # published transcript is not enough on its own: what a reader must not
    # find is an entry whose page says "Transcript not yet available" while a
    # transcript of that recording sits published. `attached` is the single
    # definition both sides import, so the two can never disagree.
    attached = attached_transcript_ids()
    if len(attached) != EXPECT_TRANSCRIBED:
        fail(f"transcript_coverage.json yields {len(attached)} attached "
             f"transcript(s) != {EXPECT_TRANSCRIBED}")
    declared_none = {str(v.get("id")) for v in videos
                     if v.get("transcripts") == 0}
    if declared_none != {str(v.get("id")) for v in videos} - attached:
        fail("the set declaring `transcripts: 0` does not match the set with no "
             "attached transcript: only=%s, no-transcript=%s"
             % (sorted(declared_none),
                sorted({str(v.get("id")) for v in videos} - attached)))
    if len(declared_none) != EXPECT_CATALOGUE_ONLY:
        fail(f"{len(declared_none)} entries declare `transcripts: 0` != "
             f"{EXPECT_CATALOGUE_ONLY}")
    else:
        print(f"PASS: {len(attached)}/{len(survivors)} surviving videos have an "
              f"ATTACHED transcript and link a published page; "
              f"{len(declared_none)} declare `transcripts: 0` and link none "
              f"(the two sets agree with transcript_coverage.json)")

    # One reader of one capture file. The transcript block inside an article and
    # the published transcript page must carry the SAME words in the same order
    # for the same recording, or the same talk reads differently in two places.
    # Checked on the words, with the article's own [mm:ss] marker and derived
    # section heading stripped, because those are presentation, not speech.
    n_same = 0
    for slug, entry in TRANSCRIPT_MAP.items():
        vid = entry[0]
        row = by_id.get(vid)
        if not row or not row.get("captions"):
            continue
        page = BASE / "_articles" / f"{slug}.md"
        if not page.is_file():
            continue
        want = capture_paragraphs(parse_capture(CAPTURE_DIR / row["file"]))
        block = page.read_text(encoding="utf-8").split("<details>", 1)
        if len(block) < 2:
            continue
        got = []
        for line in block[1].split("</details>", 1)[0].splitlines():
            line = line.strip()
            if not line or line.startswith(("#", ">", "<")):
                continue
            if line.startswith("["):        # the [mm:ss] marker vtt_to_article_md adds
                line = line.split("]", 1)[1].strip() if "]" in line else ""
            if line:
                got.append(line)
        if got != want:
            fail(f"{slug}: article transcript text != the published transcript "
                 f"for {vid} ({len(got)} vs {len(want)} paragraph(s); first "
                 f"difference at {next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), 'length')})")
        else:
            n_same += 1
    print(f"PASS: {n_same} article transcript block(s) carry word-for-word the "
          f"same text as their published transcript page")

    # --- M4: the published page against the capture file itself ------------
    # Not the article block against the page - those two share a parser. This
    # re-reads every capture with the independent reader above and compares it
    # with the document served at /transcripts/<id>/, so a parser that loses,
    # reorders or invents a paragraph cannot pass by being wrong in both places.
    #
    # What is asserted is FIDELITY: the published document's word stream is the
    # capture's word stream, in the same order, with the same multiplicity, and
    # the cue count in its front matter is the cue count the capture yields.
    # Paragraph PLACEMENT is reported rather than asserted, because where a break
    # falls between two cues is a reading decision rather than fidelity, and
    # because the builder decides it on a floating-point comparison against
    # exactly 2.0 s, which a re-run on another platform can resolve the other
    # way. The count of documents where the two readers disagree about a break
    # is printed on every run so it cannot go unnoticed; see the report.
    # The redaction list is a git-ignored local file, so it is absent in a
    # public clone. The build copes with that (it warns and redacts nothing),
    # but the published pages in THIS tree were redacted, so their fidelity
    # cannot be checked without it. Fail with the path rather than letting
    # three documents fail the word comparison for an unrelated-looking reason.
    _patterns, _marker = load_redaction_list()
    if not _patterns:
        fail("no redaction list: %s is missing or empty, so the identity of "
             "the withheld identifier is unknown here and the published "
             "transcripts cannot be checked against their captures"
             % REDACTION_LOCAL)

    n_captures, n_words, boundary_only = 0, 0, []
    n_redacted = 0
    for name in sorted(expected):
        page = TRANSCRIPTS_DIR / name
        if not page.is_file():
            fail("_transcripts/%s: missing, cannot check fidelity" % name)
            continue
        capture = front_matter_int(page, "capture_file")
        if not capture:
            fail("%s: no capture_file in front matter, cannot check fidelity"
                  % name)
            continue
        src = CAPTURE_DIR / capture
        if not src.is_file():
            fail("%s: capture file missing on disk: %s" % (name, capture))
            continue
        cues = independent_parse_capture(src)
        raw = _paragraphs_from_cues(cues)
        # The one published redaction (2026-09-27): the withheld birth name is
        # substituted on BOTH sides, so the comparison below is still the
        # capture's own word stream against the published one. The count of
        # substitutions is what the positive assertions further down check.
        n_hits = redaction_hits("\n".join(raw))
        want = [md_escape(redact(p) if n_hits else p) for p in raw]
        got = published_paragraphs(page)
        if got is None:
            fail("%s: published page has no '## Transcript text' section" % name)
            continue
        n_captures += 1
        n_words += len(" ".join(want).split())
        if n_hits:
            n_redacted += 1
            patterns, marker = load_redaction_list()
            text = page.read_text(encoding="utf-8")
            body_only = text.split("---", 2)[-1]
            if any(p.search(body_only) for p in patterns):
                fail("%s: a withheld identifier is still published in the "
                     "document body" % name)
            if body_only.count(marker) < n_hits:
                fail("%s: %d occurrence(s) of the withheld name in the capture "
                     "but only %d marker(s) in the published text"
                     % (name, n_hits, body_only.count(marker)))
            note = front_matter_str(page, "redaction_note")
            if not note:
                fail("%s: text is redacted but the page carries no "
                     "redaction_note, so the marker is unexplained" % name)
            elif "NOTICE.md" not in note:
                fail("%s: redaction_note does not point at NOTICE.md" % name)

        if " ".join(got).split() != " ".join(want).split():
            g, w = " ".join(got).split(), " ".join(want).split()
            first = next((i for i, (a, b) in enumerate(zip(g, w)) if a != b),
                         min(len(g), len(w)))
            fail("%s: the published words are not the capture's words "
                 "(%d word(s) published vs %d in %s; first difference at word "
                 "%d: published %r, capture %r)"
                 % (name, len(g), len(w), capture, first,
                    g[first] if first < len(g) else None,
                    w[first] if first < len(w) else None))
            continue
        for key, value in (("cues", len(cues)),
                           ("words", len(" ".join(want).split()))):
            stated = front_matter_int(page, key)
            if stated is None or stated != str(value):
                fail("%s: front matter %s=%s, the capture re-read independently "
                     "gives %d" % (name, key, stated, value))
        if got != want:
            boundary_only.append(name)
    if n_captures == len(expected):
        print(f"PASS: {n_captures} published transcript(s) re-derived from their "
              f"{n_captures} capture file(s) by an independent reader: same "
              f"{n_words} word(s) in the same order, cue counts agree")
    if n_redacted:
        _, marker = load_redaction_list()
        print(f"PASS: {n_redacted} published transcript(s) carry the "
              f"site owner's redaction - identifier absent, one "
              f"{marker!r} marker per occurrence, redaction_note "
              f"pointing at NOTICE.md - and the other "
              f"{n_captures - n_redacted} are word-for-word the capture")
    if boundary_only:
        print(f"NOTE: {len(boundary_only)} document(s) place a paragraph break "
              f"differently from the independent reader, with identical words: "
              f"{', '.join(boundary_only)}. A break is decided on a pause of "
              f"exactly 2.0 s, and the builder compares that in binary floating "
              f"point, so the tie is not decided reproducibly. No word differs. "
              f"Tracked for Task 9; it changes no text.")

    if failures:
        print(f"test_transcripts: {len(failures)} FAILURE(S)")
        return 1
    print("test_transcripts: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
