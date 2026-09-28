#!/usr/bin/env python3
"""Build _papers/_videos/_articles collections (Task 5, issue C-07; FULL).

Reads (paths relative to this script, stdlib only, no network):
  ../_data/papers.json        20 rows (2 of them hold a PDF in ../_papers/pdfs/)
  ../_data/videos.json        row count owned by _data/videos.json (I2)
  ../_data/canonical_works.json  the works list (found|wayback_only|lost)
  ../_data/mdi_articles.json  17 rows, each with a local text page generated here
  ../_data/notices.json       3 announcement rows, never counted as works
  ../_data/transcript_coverage.json
  ../_posts/*.md              54 full-text files (link targets for found works)

Writes (clears stale *.md first, then regenerates):
  ../_papers/*.md    (20) filename = search.md slugify(title)
  ../_videos/*.md         filename = <video id> (matches search video.id link)
  ../_articles/*.md  (72 works + 17 mdi text pages) filename = <slug>
  ../_transcripts/*.md    filename = transcript-<capture key>, one per CAPTURE
                          named by ../_data/transcript_coverage.json (top-level
                          rows AND alternates), not one per video
  ../_data/transcript_index.json  the index _layouts/video.html and
                          transcripts.md read to link each capture

Ethics (user chose FULL collections, honestly labelled):
  - Link-outs by default. Six papers now legitimately hold a PDF obtained
    without circumvention (verified %PDF- header, %%EOF trailer and page
    counts); those render a "held in this repository" line plus the file
    name. Everything else still links out and mirrors nothing.
  - Institutional items (Yaqeen/MDI/AlBalagh) link out; Yaqeen attribution
    preserved in front matter (publisher_journal) + body credit line.
  - NO Reddit/Medium inlining: bodies quote nothing and link only to URLs
    already present in the source data (original/pdf/wayback/YouTube).
  - YouTube-only videos -> source: youtube_not_archived +
    "YouTube (not archived)" label; body never says "Archive.org".
  - Dup number 52 -> second occurrence (Virgins in Paradise?) renumbered to
    53 in display title; both entries kept; original title recorded.
  - Articles: found -> link local _posts (+ Wayback fallback);
    wayback_only -> Wayback link; lost (1) -> no button + honest note
    (reference capture kept as reference_url, never a button);
    feed-only null URL -> note, not a button.

Jekyll notes:
  - `page.url` is reserved (internal doc URL), so paper bodies/layouts must
    use `original_url` for the external publisher link. Builder writes BOTH
    `url` (spec literal) and `original_url` (rendered alias, same value).
  - `page.id` is reserved (path-based doc id), so videos carry `video_id`
    (+ filename itself is the search key). Builder writes BOTH `video_id`
    and `id` (same value; Liquid `page.id` still resolves to the doc path).
"""

import json
from urllib.parse import quote
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from transcribe import vtt_to_article_md  # noqa: E402

SCRIPT_DIR = pathlib.Path(__file__).parent
BASE = SCRIPT_DIR.parent  # andalusian-archive/

PAPERS_JSON = BASE / "_data" / "papers.json"
VIDEOS_JSON = BASE / "_data" / "videos.json"
CANON_JSON = BASE / "_data" / "canonical_works.json"
MDI_JSON = BASE / "_data" / "mdi_articles.json"
NOTICES_JSON = BASE / "_data" / "notices.json"
COVERAGE_JSON = BASE / "_data" / "transcript_coverage.json"
POSTS_DIR = BASE / "_posts"
# 2026-09-27 (task 8d): the published transcripts and the small index the
# video pages read them through.
TRANSCRIPTS_DIR = BASE / "_transcripts"
TRANSCRIPT_INDEX_JSON = BASE / "_data" / "transcript_index.json"
# The raw captures. READ ONLY, never written: build_transcripts() renders
# them into _transcripts/ and leaves the capture itself byte-identical.
CAPTURE_DIR = BASE / ".firecrawl" / "transcripts"

DISCLAIMER = (
    "*Transcript by machine ({source}) — accuracy isn't perfect, so it "
    "shouldn't be used in polemics or debate material as an authoritative "
    "source.*"
)

# 2026-09-27 (task 8d): the machine-transcript sentence on its own, without
# the markdown emphasis markers. `_layouts/transcript.html` prints it from the
# front-matter field this value is written into, `_layouts/video.html` prints
# the same bytes inside <em>, and test_transcripts.py compares both against
# this constant, so no copy can drift from another.
#
# Do not reword it and do not "tidy" the apostrophes into typographic ones: the
# apostrophes are U+0027 and the dash is U+2014, exactly as published, and a
# change here is a change to a term the archive has already published.
MACHINE_TRANSCRIPT_DISCLAIMER = (
    "Transcript by machine — accuracy isn't perfect, so it shouldn't be "
    "used in polemics or debate material as an authoritative source."
)

# --- Publication redaction list (2026-09-27) --------------------------------
# One personal identifier is withheld from the published machine transcripts at
# the site owner's decision (NOTICE.md 6.1): the birth name, the family name he
# discusses in his own account of his conversion. It is substituted for a
# visible marker at DOCUMENT BUILD time, so the marker is written into
# `_transcripts/*.md` itself rather than applied by a template at view time.
#
# WHY THE NAME IS NOT A LITERAL IN THIS FILE
# ------------------------------------------
# An earlier revision carried `BIRTH_NAME = "<the name>"` here. This script is
# part of the PUBLISHED repository, so that constant published the very
# identifier the redaction exists to withhold - the redaction defeated itself,
# and a reader grepping the source found the name. So the name is not written
# here, and it is not encoded, split or otherwise disguised here either:
# obfuscation would be theatre, and it would still be in the published tree.
#
# The list lives in a git-ignored local file, `.redaction.local.json` at the
# repo root, holding `{"names": [...], "marker": "..."}`. The marker is read
# from that file too, so this module contains no publication-facing redaction
# string at all. The file is untracked (see .gitignore) and exists only in the
# maintainers' working trees; see the report for the shape.
#
# The raw captures under `.firecrawl/transcripts/` are verbatim source evidence
# and are NOT edited: they are untracked from the published repository instead.
#
# The marker is visible, not a silent gap: a reader who meets it is told that
# something was withheld and why, and the page carries a `redaction_note`
# pointing at NOTICE.md. It replaces the name in place, so the surrounding
# sentence still reads as the speaker said it.
#
# `words` is recomputed from the REDACTED paragraphs (see
# transcript_documents()), so the front-matter count is the count of the text
# the reader actually gets, and test_transcripts.py's fidelity gate applies
# this same substitution to the stream it re-derives from the capture.
#
# If the local file is missing the build MUST still succeed, because a public
# clone has no capture files either and must not be broken by this. It then
# applies NO redaction and says so loudly, once, rather than silently
# publishing unredacted text.
REDACTION_LOCAL = BASE / ".redaction.local.json"

_REDACTION = {"loaded": False, "patterns": [], "marker": ""}


def _warn_redaction(problem):
    """One loud, self-locating warning. Never silent, never fatal.

    Written with f-strings rather than a `%` format over an implicitly
    concatenated block on purpose: `%` binds tighter than `+`, so a trailing
    `% (...)` on such a block applies only to its LAST literal and raises
    TypeError - which turns this warning into a crash, i.e. the exact opposite
    of degrading safely. The degraded-path test in the report is what caught it.
    """
    sys.stderr.write(
        f"\n{'!' * 74}\n"
        f"WARNING - PUBLICATION REDACTION NOT APPLIED\n"
        f"  {problem}\n"
        f"\n"
        f"  The redaction list is expected at:\n"
        f"      {REDACTION_LOCAL}\n"
        f"  Expected shape:\n"
        f"      {{\"names\": [\"<identifier to withhold>\", ...],\n"
        f"       \"marker\": \"<the visible marker substituted in its place>\"}}\n"
        f"\n"
        f"  The identifier itself is deliberately NOT a literal in any tracked\n"
        f"  file, so a clone that needs it must be given this file locally.\n"
        f"  Until it exists the build continues but NOTHING is redacted: any\n"
        f"  withheld identifier present in the sources is published verbatim.\n"
        f"{'!' * 74}\n\n"
    )
    sys.stderr.flush()


def load_redaction_list():
    """(patterns, marker) from the git-ignored local redaction list.

    Cached: the warning is emitted once per run, and the patterns are compiled
    once. Returns `([], "")` when no usable list is present, which every caller
    treats as "apply no reaction" rather than as an error.
    """
    if _REDACTION["loaded"]:
        return _REDACTION["patterns"], _REDACTION["marker"]
    _REDACTION["loaded"] = True

    if not REDACTION_LOCAL.is_file():
        _warn_redaction("the file does not exist.")
        return _REDACTION["patterns"], _REDACTION["marker"]

    try:
        data = json.loads(REDACTION_LOCAL.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        _warn_redaction("the file exists but could not be read as JSON: %s" % exc)
        return _REDACTION["patterns"], _REDACTION["marker"]

    names = [str(n).strip() for n in (data.get("names") or []) if str(n).strip()]
    marker = str(data.get("marker") or "").strip()
    if not names:
        _warn_redaction('the file parsed but its "names" list is empty.')
        return _REDACTION["patterns"], _REDACTION["marker"]
    if not marker:
        _warn_redaction('the file parsed but carries no "marker" string.')
        return _REDACTION["patterns"], _REDACTION["marker"]

    # Word-bounded and case-insensitive: the captures are lower-cased ASR
    # output, but a coincidental capitalised or plural use must be caught too.
    _REDACTION["patterns"] = [
        re.compile(r"\b%s\b" % re.escape(n), re.IGNORECASE) for n in names
    ]
    _REDACTION["marker"] = marker
    return _REDACTION["patterns"], _REDACTION["marker"]


def redaction_hits(text):
    """How many withheld identifiers `text` contains. 0 when the list is absent."""
    patterns, _ = load_redaction_list()
    return sum(len(p.findall(text)) for p in patterns)


def redact(text):
    """Substitute every withheld identifier with the visible marker.

    A no-op when the local redaction list is absent, so the build still runs.
    """
    patterns, marker = load_redaction_list()
    if not patterns:
        return text
    for p in patterns:
        text = p.sub(marker, text)
    return text


def redaction_note(hits):
    """The per-document `redaction_note`, stating what was withheld and why.

    `hits` is the number of occurrences found in this capture, so the note
    cannot claim a count the document does not carry. It names no identifier.
    """
    _, marker = load_redaction_list()
    return (
        "One personal identifier was withheld from this transcript at the "
        "site owner's request: his birth name, the family name he discusses "
        "in this account of his own conversion. It occurs %d time%s in the "
        "capture and each occurrence is shown here as %s. Every other word is "
        "the capture's own, unaltered. The raw capture file itself is "
        "withheld from this repository rather than edited - it is evidence, "
        "and editing evidence would destroy what makes it evidence - so the "
        "unredacted text is not published here either. See NOTICE.md, "
        "section 6." % (hits, "" if hits == 1 else "s", marker)
    )


# slug -> (video_id, human summary). Summaries describe the recording
# factually, written from transcript heads + video metadata 2026-09-07.
TRANSCRIPT_MAP = {
    "ijihad-pilot-and-first-2-episodes": (
        "RnkqSMTzvCg",
        "iJihad Ep. 1 answers Dutch YouTuber Gryffix's claims about Islamic "
        "fundamentalism — the opening episode of the Intellectual Jihad "
        "series dissecting popular anti-Islam arguments."),
    "ikhalifa-ep-1": (
        "rtViqNWY1Bk",
        "iKhalifa Ep. 1 opens with Qur'anic verses on humanity's role as "
        "khalifa (steward) of creation and introduces appreciating others."),
    "ikhalifa-ep-2": (
        "-BwP55UIg3c",
        "iKhalifa Ep. 2 continues the stewardship series on forgiving "
        "oneself, opening with Qur'anic recitation."),
    "a-muslims-guide-to-science-scientism": (
        "X36xEj0OSV4",
        "Part 1 of the Al-Balagh Academy series distinguishes science from "
        "scientism, beginning with definitions. Parts 2–5 are transcribed "
        "in the video archive."),
    "understanding-atheism-lecture-series": (
        "NyAVl7RsEOs",
        "Six-session Understanding Atheism lecture series hub. Session 1 "
        "transcript below; Sessions 2–6 transcripts linked as series parts.",
        ["CEzMdCn0Ims", "lZkv38vd7bw", "wVehdVlLdBI", "BRDaCqipcwM",
         "lS7h9SKKtVc"]),
    "understanding-atheism": (
        "lS7h9SKKtVc",
        "Repost of the Understanding Atheism series hub, pointing at Session 6. "
        "The transcript below is Session 6. The mirror that used to carry this "
        "card (bRTI6Z5gggE) was removed from the video catalogue in 2026-09-27 as "
        "a third-party re-upload of the same recording; its transcript was "
        "re-parented onto the surviving Session 6 entry rather than deleted."),
    "atheism-doubting-your-doubts": (
        "ZbcsxAoIVY0",
        "Yaqeen in New York lecture: doubting one's doubts about atheism."),
    "the-quran-science-a-forced-marriage": (
        "fJs5tuFw-UY",
        "MSA Ohio State halaqa: the Qur'an and science need not be forced "
        "into concordism — science as a tool, not a worldview."),
    "islam-science-and-history": (
        "0snGWjeqEeM",
        "Yaqeen podcast interview on the Structure of Scientific "
        "Productivity paper and the Orientalists' fables thesis."),
    "islam-terrorism": (
        "4VcPzhkP9bE",
        "IIUM Malaysia talk on Islam and terrorism (auto-captions, rough)."),
    "towards-litter-reduction-an-islamic-approach": (
        "7Rzu6BjvxjY",
        "IAIS talk: an Islamic approach to litter reduction."),
    "islam-and-litter-reduction": (
        "7Rzu6BjvxjY",
        "Repost of the litter-reduction talk page; same IAIS recording."),
    "understanding-aishas-age-an-interdisciplinary-approach": (
        "qBkiwqMucY0",
        "Talk version of the interdisciplinary Aisha's-age paper "
        "(auto-captions, rough)."),
    "hard-questions-answering-doubts-about-islam": (
        "1U6VfHosrqw",
        "Open Q&A answering doubts about Islam (auto-captions, rough)."),
    "of-context-and-confusion": (
        "biZFuWyB4lk",
        "Short dialogue answering out-of-context polemics."),
}

PAPERS_DIR = BASE / "_papers"
VIDEOS_DIR = BASE / "_videos"
ARTICLES_DIR = BASE / "_articles"

TALKS_URL = "https://independent.academia.edu/AsadullahAli/Talks"
YOUTUBE_WATCH = "youtube.com/watch"
CC_PAPER_ID = 4  # Between a Backbone And Ribs (CC-licensed; still link-out only)

# Second "52 - ..." occurrence gets renumbered to 53 (keep both titles).
DUP52_ID = "cDHrrbOKbl4"


def q(value):
    """YAML-safe double-quoted scalar (JSON quoting is valid YAML)."""
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def qlist(items):
    return json.dumps([str(x) for x in (items or [])], ensure_ascii=False)


def paper_slug(title):
    """Must match search.md:119 exactly (JS slugify)."""
    s = re.sub(r"[^a-z0-9]+", "-", str(title or "").lower())
    s = re.sub(r"^-|-$", "", s)
    return s


def is_youtube(url):
    return YOUTUBE_WATCH in str(url or "")


def clear_md(target):
    target.mkdir(parents=True, exist_ok=True)
    for old in sorted(target.glob("*.md")):
        old.unlink()


def write_md(target, name, front, body):
    lines = ["---"]
    lines.extend(front)
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    (target / name).write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------- transcripts ---
# 2026-09-27 (task 8d). Before this pass the transcript section on a video
# page was a status marker: the coverage row was rendered faithfully and the
# capture file name was printed, but the TEXT lived only in
# .firecrawl/transcripts/, which Jekyll excludes and cannot read. 56 of the 68
# catalogued videos had a machine transcript and a reader could not read one of
# them. This section turns each capture into a served document.

# A WebVTT cue header: `00:00:03.600 --> 00:00:06.150 align:start position:0%`
_CUE_TS = re.compile(
    r"^(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)\s+-->\s+"
    r"(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)")

# Characters that kramdown would otherwise read as markup. Escaping them
# changes the BYTES of the source, never the words a reader sees. The set is
# the intersection of what the captures actually contain (see the audit in the
# task-8d report) and what kramdown acts on, and it is exactly kramdown's own
# ESCAPED_CHARS list (kramdown/parser/kramdown/escaped_chars.rb) minus the
# characters these captures do not contain. `$` and `[]` matter because
# kramdown's default math_engine turns them into math and links.
#
# `'` is in the set for a different reason: kramdown's smart_quotes rewrites a
# straight apostrophe into U+2019, so an unescaped `they've` would reach the
# reader as `they’ve`. Same word, different byte - and a transcription page
# should be the machine's bytes. `\'` is a valid markdown escape, so the
# rendered character is exactly U+0027. Jekyll 4.4's kramdown parser reads its
# options from _config.yml only (see jekyll/converters/markdown/
# kramdown_parser.rb), so there is no per-page switch to turn this off; the
# escape is the way to say it in the source instead.
#
# `&` is deliberately NOT escaped: it is not in kramdown's ESCAPED_CHARS, so
# `\&` would leave a literal backslash on the page. kramdown escapes a bare `&`
# to `&amp;` by itself, which renders as `&`.
_MD_INLINE = re.compile(r"[\\`*_\[\]<|$']")
# kramdown rewrites `...` to U+2026 and `--`/`---` to U+2013/U+2014 whatever
# the options say (html.rb falls back to TYPOGRAPHIC_SYMS). Escaping the FIRST
# character of the run is enough to stop the match and still renders the run.
_MD_TYPO = re.compile(r"\.{3,}|--+")
# A paragraph that opens with a list marker would be read as a list. The
# punctuation forms are escaped with a backslash; the numbered form is escaped
# on its DOT, because a backslash only escapes ASCII punctuation in markdown -
# `\13. text` would render a visible backslash, `13\. text` renders `13. text`.
_MD_LINE_PUNCT = re.compile(r"^([#>+*\-])")
_MD_LINE_NUMBER = re.compile(r"^(\d+)\.")


def md_escape(text):
    """Escape markdown control characters in recovered text.

    The only transformation applied to a capture's words anywhere in this
    builder. No word is added, removed, reordered or respelled; this only
    stops kramdown from reading punctuation as markup.
    """
    text = _MD_INLINE.sub(lambda m: "\\" + m.group(0), text)
    text = _MD_TYPO.sub(lambda m: "\\" + m.group(0), text)
    text = _MD_LINE_PUNCT.sub(lambda m: "\\" + m.group(0), text)
    return _MD_LINE_NUMBER.sub(lambda m: m.group(1) + "\\.", text)


def _cue_seconds(h, m, s):
    return (int(h) * 3600 if h else 0) + int(m) * 60 + float(s)


def parse_capture(path):
    """Return [(start, end, text)] for one capture file, tags stripped.

    WebVTT: the `WEBVTT` header, the `Kind:` / `Language:` lines, the bare cue
    numbers, the `-->` timing lines and the inline `<00:00:03.840><c>` timing
    and `<v Name>` voice tags are removed. Nothing inside the caption text is
    touched.

    YouTube's own auto-captions arrive in a rolling window: each caption line
    is emitted twice - once as a long cue that repeats the previous line plus
    the new words, and once as a ~10 ms "settled" cue holding only the new
    words. Keeping both prints every line up to three times, which is what
    `transcribe.load_segments()` does and therefore what the 15 transcripts
    already embedded in `_articles/` look like. For a document meant to be
    read, the settled cue of each line is kept and the rolling echo dropped:
    the same words, once. A capture in any other caption format has no settled
    cues, and falls back to the plain parse rather than losing its text.
    """
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return [(float(s.get("start", 0.0)), float(s.get("end", 0.0)),
                 str(s.get("text", "")).strip()) for s in data.get("segments", [])]
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    cues, span, buf = [], None, []
    for line in raw:
        m = _CUE_TS.match(line.strip())
        if m:
            if buf and span is not None:
                cues.append((span[0], span[1], " ".join(buf)))
            h1, m1, s1, h2, m2, s2 = m.groups()
            span = (_cue_seconds(h1, m1, s1), _cue_seconds(h2, m2, s2))
            buf = []
            continue
        stripped = line.strip()
        if (not stripped or "WEBVTT" in stripped or stripped.isdigit()
                or stripped.startswith("Kind:") or stripped.startswith("Language:")
                or stripped.startswith("NOTE")):
            continue
        if "<" in stripped:
            stripped = re.sub(r"<[^>]+>", "", stripped)
        buf.append(stripped.strip())
    if buf and span is not None:
        cues.append((span[0], span[1], " ".join(buf)))
    settled = [c for c in cues if c[1] - c[0] <= 0.05]
    if settled:
        cues = settled
    # Consecutive identical lines are the auto-caption echo, not speech.
    out = []
    for start, end, text in cues:
        if not text:
            continue
        if out and out[-1][2] == text:
            continue
        out.append((start, end, text))
    return out


def capture_paragraphs(cues):
    """Group cues into paragraphs on a silence gap.

    A new paragraph starts when consecutive cue STARTS are more than 2.0 s
    apart - the same rule `transcribe.vtt_to_article_md()` uses, so the
    paragraph shape of a published transcript matches the transcript blocks
    already in `_articles/`.
    """
    paras, cur, last_start = [], [], None
    for start, _end, text in cues:
        if cur and last_start is not None and start - last_start > 2.0:
            paras.append(" ".join(cur))
            cur = []
        cur.append(text)
        last_start = start
    if cur:
        paras.append(" ".join(cur))
    return [p for p in (p.strip() for p in paras) if p]


def video_display_title(vid, title):
    """The title build_videos() writes, 52/53 de-duplication included.

    Shared so a transcript page and the video page it belongs to cannot print
    two different titles for the same recording.
    """
    title = str(title or "")
    if vid == DUP52_ID and title.startswith("52 -"):
        return "53 -" + title[4:]
    return title


def transcript_documents():
    """Every capture `_data/transcript_coverage.json` references, as document
    dicts, in file order.

    One document per CAPTURE, not per video: a top-level row that names a file
    and every `alternates` entry that names one. A superseded upload's
    transcript is therefore published as an additional transcript of the
    recording it duplicates - attributed to that upload, and filed under the
    surviving recording - which is the only way its text stays reachable once
    the upload left the catalogue.

    `transcript_id` is the document key and the URL segment. Alternates carry
    a `-duplicate-upload` suffix so a key can never collide with the primary
    capture of a video that happens to share the id.
    """
    cov = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    videos = {str(v.get("id")): v for v in
              json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))}
    docs, seen = [], set()

    def add(row, role, key):
        if key in seen:
            raise AssertionError("duplicate transcript id %r" % key)
        seen.add(key)
        name = row.get("file")
        assert name, "transcript %s has no capture file" % key
        path = CAPTURE_DIR / name
        assert path.is_file(), "capture file missing on disk: %s" % name
        vid = str(row.get("video_id", ""))
        recording = vid if role != "duplicate-upload" else str(
            row.get("reparented_onto", ""))
        assert recording, "alternate capture with no reparented_onto: %s" % vid
        v = videos.get(recording, {})
        title = video_display_title(recording, v.get("title")
                                    or row.get("title") or recording)
        if role == "duplicate-upload":
            title = "%s - transcript of a duplicate upload" % title
        cues = parse_capture(path)
        paras = capture_paragraphs(cues)
        assert paras, "capture %s yielded no text" % name
        # Publication redaction (2026-09-27): substitute the withheld birth
        # name BEFORE the paragraph count and word count are taken, so every
        # figure this document states describes the text the reader is given
        # rather than the text the capture holds. No other word is touched.
        hits = redaction_hits("\n".join(paras))
        if hits:
            paras = [redact(p) for p in paras]
        return {
            "transcript_id": key,
            "recording": recording,
            "capture_video_id": vid,
            "role": role,
            "title": title,
            "url": "/transcripts/%s/" % key,
            "file": name,
            "source": str(row.get("source", "")),
            "lang": str(row.get("lang", "")),
            "lines": int(row.get("lines") or 0),
            "words": sum(len(p.split()) for p in paras),
            "paragraphs": len(paras),
            "cues": len(cues),
            "recording_url": "/videos/%s/" % recording if recording in videos
                             else "",
            "reparented_at": str(row.get("reparented_at", "")),
            "superseded_reason": str(row.get("superseded_reason", "")),
            "note": str(row.get("note", "")),
            "redaction_note": redaction_note(hits) if hits else "",
            "paragraph_texts": paras,
        }

    for row in cov:
        if not row.get("captions") or not row.get("file"):
            # A row with captions false and no file is a recording the archive
            # could not caption (the Facebook-only debate). It has no text to
            # publish and the page that carries it says so in plain words.
            continue
        vid = str(row.get("video_id", ""))
        in_videos = vid in videos
        if row.get("attached_to_video_entry") is False:
            role = "preserved-not-attached"
        elif not in_videos:
            role = "superseded-upload"
        else:
            role = "own-capture"
        docs.append(add(row, role, vid))
        for alt in row.get("alternates") or []:
            if not alt.get("file"):
                continue
            assert alt.get("captions"), \
                "alternate %s has a file but captions is false" \
                % alt.get("video_id")
            docs.append(add(alt, "duplicate-upload",
                            "%s-duplicate-upload" % alt.get("video_id")))
    return docs


def transcript_filenames(cov):
    """The filenames build_transcripts() writes, for the collection_drift()
    leg. Derived from the coverage file, never from the directory, so a
    missing or extra page is drift."""
    names = set()
    for row in cov:
        if row.get("captions") and row.get("file"):
            names.add("transcript-%s.md" % row.get("video_id"))
        for alt in row.get("alternates") or []:
            if alt.get("file"):
                names.add("transcript-%s-duplicate-upload.md"
                          % alt.get("video_id"))
    return names


ROLE_NOTES = {
    "own-capture":
        "This is the capture taken from the catalogued recording itself.",
    "duplicate-upload":
        "This is an additional transcript of the same recording, taken from a "
        "duplicate upload that left the video catalogue under the "
        "count-once rule. It is not a separate recording, and it is not "
        "counted again.",
    "superseded-upload":
        "This capture belongs to an upload that is no longer a catalogued "
        "entry in its own right, so there is no recording page to file it "
        "under. Its text is preserved and published here rather than kept in "
        "a directory Jekyll does not serve, and the upload itself is recorded "
        "in the archive's superseded-video ledger.",
    "preserved-not-attached":
        "A machine transcript of this recording is preserved in the archive "
        "and is published here, but it is deliberately not attached to the "
        "catalogue entry, so that entry's page carries no transcript. The "
        "capture was made; nothing was deleted and nothing is promised.",
}

RENDERING_NOTES = {
    "youtube-auto-captions":
        "The source file is a YouTube auto-caption capture in the rolling "
        "window format, where every caption line is written twice: once "
        "prefixed with the previous line, and once on its own. The words are "
        "unchanged; the repeated window is dropped so each line is printed "
        "once. Cue numbers, `-->` timing lines and the inline `<00:00:03.840>` "
        "timing and `<v ...>` voice tags are removed, and a paragraph starts "
        "where the speaker pauses for more than two seconds. A handful of "
        "these files contain the literal text `&nbsp;` where the caption "
        "engine emitted an escaped non-breaking space; it is shown here as the "
        "space it stands for, and no word is affected.",
    "whisper":
        "The source file is a local Whisper transcription. The words are "
        "reproduced as Whisper wrote them, with no correction of any kind; a "
        "paragraph starts where the speaker pauses for more than two seconds.",
}


def archive_link(v: dict) -> str:
    """The preserved-file URL, safe to put in an href.

    The Internet Archive filenames carry spaces, a fullwidth colon and a
    fullwidth vertical bar. Emitted raw they are not requestable URLs: the href
    404s for anything that fetches it as written. A browser re-encodes on click,
    which is why 56 video pages shipped this way unnoticed. Only the path is
    escaped - the scheme and slashes have to survive.

    Two characters decide whether this is right or merely differently broken:

    `?` IS in SAFE, because twelve rows are `youtube_not_archived` and their
    `archive_url` *is* the YouTube watch URL. Escaping it turns
    `watch?v=TTGJPneVR_w` into `watch%3Fv=TTGJPneVR_w`, which is a 404 - the
    defect only appears when the collections are regenerated, so the suites stay
    green while twelve live links quietly break.

    `#` is deliberately NOT in SAFE. Six Internet Archive filenames contain a
    literal `#` ("Book Recommendations #1"). A fragment is never transmitted to
    the server, so a raw `#` 404s the file while `%23` returns it.

    `%` is in SAFE, so this is idempotent on already-encoded input.
    """
    url = (v.get("archive_url") or "").strip()
    if not url:
        return ""
    head, sep, tail = url.partition("://")
    if not sep:
        return url
    return head + sep + quote(tail, safe="/@:+$&~!*'()=%,;?")



def build_transcripts():
    """Publish the transcript TEXT as served documents, plus the index.

    Writes `_transcripts/<transcript_id>.md` (one per capture) and
    `_data/transcript_index.json`, which is what `_layouts/video.html` and
    `transcripts.md` read. The captures under `.firecrawl/transcripts/` are
    opened read-only and never rewritten.
    """
    docs = transcript_documents()
    clear_md(TRANSCRIPTS_DIR)
    by_recording, n_words, n_paras, n_alt = {}, 0, 0, 0
    n_redacted = []
    for d in docs:
        recording, tid = d["recording"], d["transcript_id"]
        if d["role"] == "duplicate-upload":
            n_alt += 1
        n_words += d["words"]
        n_paras += d["paragraphs"]

        rendering = RENDERING_NOTES.get(
            "youtube-auto-captions" if "youtube" in d["source"] else "whisper",
            "The source file's words are reproduced unchanged; only WebVTT "
            "cue numbering, timing lines and inline timing or voice tags are "
            "removed.")
        role_note = ROLE_NOTES[d["role"]]

        front = [
            "layout: transcript",
            "title: %s" % q(d["title"]),
            "transcript_id: %s" % q(tid),
            # `recording` is the catalogued video this page is a transcript
            # of; `capture_video_id` is the upload the capture was taken from.
            # They are the same for a normal capture and differ for a
            # re-parented one, which is the whole point of keeping both.
            "recording: %s" % q(recording),
            "capture_video_id: %s" % q(d["capture_video_id"]),
            "recording_url: %s" % q(d["recording_url"]),
            "permalink: %s" % q(d["url"]),
            "role: %s" % q(d["role"]),
            "source: %s" % q(d["source"]),
            "lang: %s" % q(d["lang"]),
            "lines: %d" % d["lines"],
            "cues: %d" % d["cues"],
            "paragraphs: %d" % d["paragraphs"],
            "words: %d" % d["words"],
            "capture_file: %s" % q(d["file"]),
            "disclaimer: %s" % q(MACHINE_TRANSCRIPT_DISCLAIMER),
        ]
        if d["reparented_at"]:
            front.append("reparented_at: %s" % q(d["reparented_at"]))
        if d["superseded_reason"]:
            front.append("superseded_reason: %s" % q(d["superseded_reason"]))
        if d["note"]:
            front.append("capture_note: %s" % q(d["note"]))
        if d["redaction_note"]:
            front.append("redaction_note: %s" % q(d["redaction_note"]))
            n_redacted.append("transcript-%s.md" % tid)

        body = [_h1(d["title"]), ""]
        if d["role"] == "duplicate-upload":
            body += [
                "> This is a transcript of the **same recording** as the page "
                "for `%s`. The upload it was captured from (`%s`) left the "
                "video catalogue as a duplicate; the transcript text was "
                "re-parented onto the surviving entry and kept, not deleted. "
                "It is published here, attributed, so that its text is "
                "readable." % (recording, d["capture_video_id"]),
                "",
            ]
        body += [role_note, ""]
        if d["recording_url"]:
            body += ["- The recording: [%s]({{ \"%s\" | relative_url }})"
                     % (recording, d["recording_url"]), ""]
        body += [
            "- Capture file held in the archive: `%s`" % d["file"],
            "- Produced by: %s" % (d["source"] or "unrecorded"),
            "- Language recorded for the capture: %s" % (d["lang"] or "unrecorded"),
            "- %d cue%s in the capture file, rendered as %d paragraph%s and "
            "%d word%s below" % (d["cues"], "" if d["cues"] == 1 else "s",
                                 d["paragraphs"],
                                 "" if d["paragraphs"] == 1 else "s",
                                 d["words"], "" if d["words"] == 1 else "s"),
            "",
            "How this text was rendered: %s" % rendering,
            "",
            "## Transcript text",
            "",
        ]
        body += [md_escape(p) for p in d["paragraph_texts"]]
        body.append("")

        write_md(TRANSCRIPTS_DIR, "transcript-%s.md" % tid, front,
                 "\n".join(body))

        by_recording.setdefault(recording, []).append({
            k: d[k] for k in ("transcript_id", "title", "role", "url",
                              "capture_video_id", "recording_url", "source",
                              "lang", "lines", "words", "paragraphs", "file")
        })

    # Gate: every capture on disk is published, and every capture named by the
    # coverage file exists. An unpublished capture is text the archive holds
    # and no reader can reach, which is the failure this pass exists to stop.
    on_disk = {p.name for p in CAPTURE_DIR.iterdir() if p.is_file()}
    named = {d["file"] for d in docs}
    dangling = sorted(named - on_disk)
    orphans = sorted(on_disk - named)
    assert not dangling, "coverage file names a capture that is not on disk: %s" \
        % dangling
    assert not orphans, ("capture(s) on disk that no coverage row references, "
                         "so no transcript publishes their text: %s - add a "
                         "coverage row or delete the file"
                         % orphans)

    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    attached = attached_transcript_ids()
    index = {
        "generated_by": "scripts/build_collections.py :: build_transcripts()",
        "generated_on": "2026-09-27",
        "reads": "_data/transcript_coverage.json and the capture files it "
                 "names under .firecrawl/transcripts/ (read-only)",
        "disclaimer": MACHINE_TRANSCRIPT_DISCLAIMER,
        "documents": len(docs),
        "words": n_words,
        "paragraphs": n_paras,
        "alternate_captures": n_alt,
        "recordings": len(by_recording),
        # 2026-09-27 (R25, task 8d): the catalogue split, read from the same
        # helper build_videos() gates on, so the index page and the gate cannot
        # disagree. 56 attached / 12 catalogue-only became 57 / 11 when R25
        # attached G47Stp3pLss's preserved capture to its restored entry.
        "catalogued_videos": len(videos),
        "videos_attached": len(attached),
        "videos_catalogue_only": len(videos) - len(attached),
        "role_notes": ROLE_NOTES,
        "by_recording": by_recording,
    }
    TRANSCRIPT_INDEX_JSON.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print("transcripts: wrote %d document(s) to _transcripts/ (%d words, "
          "%d paragraphs, %d additional transcript(s) of a recording from a "
          "duplicate upload, %d recording(s))"
          % (len(docs), n_words, n_paras, n_alt, len(by_recording)))
    print("transcripts: %d capture(s) on disk, all published, none orphaned"
          % len(on_disk))
    print("transcripts: %d of %d catalogued videos have an ATTACHED "
          "transcript, %d declare `transcripts: 0`"
          % (len(attached), len(videos), len(videos) - len(attached)))
    _, marker = load_redaction_list()
    if n_redacted:
        print("transcripts: withheld identifier(s) redacted at publication time "
              "from %d document(s), each occurrence shown as %r and each "
              "carrying a redaction_note: %s"
              % (len(n_redacted), marker, ", ".join(n_redacted)))
    else:
        print("transcripts: NO document was redacted - see the redaction "
              "warning above if one was printed")
    return len(docs)


# ---------------------------------------------------------------- papers ---
def build_papers():
    papers = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    assert len(papers) == 20, "expected 20 papers, got %d" % len(papers)
    clear_md(PAPERS_DIR)
    seen = set()
    n_profile_only = 0
    for p in papers:
        title = p.get("title", "")
        slug = paper_slug(title)
        assert slug, "empty slug for paper %r" % (p.get("id"),)
        assert slug not in seen, "duplicate paper slug: %s" % slug
        seen.add(slug)
        profile_only = (p.get("url") == TALKS_URL)
        if profile_only:
            n_profile_only += 1
        pub = p.get("publication_date")

        front = [
            "layout: paper",
            "title: %s" % q(title),
            # Explicit permalink: immune to :name slugify drift; matches
            # search.md `/papers/<slugified-title>/` exactly.
            "permalink: %s" % q("/papers/" + slug + "/"),
        ]
        # NOTE: Jekyll parses ONLY the `date` key as a Date (merge_date!).
        # Year-only ("2020") or year-month ("2015-04") values are fatal
        # (InvalidDateError), so emit `date` solely for full YYYY-MM-DD
        # values and keep the raw source string in `publication_date`.
        if pub and re.match(r"^\d{4}-\d{2}-\d{2}$", str(pub)):
            front.append("date: %s" % q(pub))
        if pub:
            front.append("publication_date: %s" % q(pub))
        # `url` = spec literal; `original_url` = rendered alias (page.url is
        # reserved for the internal Jekyll URL, see module docstring).
        if p.get("url"):
            front.append("url: %s" % q(p["url"]))
            front.append("original_url: %s" % q(p["url"]))
        if p.get("publisher_journal"):
            front.append("publisher_journal: %s" % q(p["publisher_journal"]))
        if p.get("type"):
            front.append("type: %s" % q(p["type"]))
        if p.get("status"):
            front.append("status: %s" % q(p["status"]))
        if p.get("volume_issue"):
            front.append("volume_issue: %s" % q(p["volume_issue"]))
        if p.get("doi"):
            front.append("doi: %s" % q(p["doi"]))
        if p.get("citation_count") is not None:
            front.append("citation_count: %s" % int(p["citation_count"]))
        front.append("co_authors: %s" % qlist(p.get("co_authors")))
        front.append("sources: %s" % qlist(p.get("sources")))
        if p.get("pdf_url"):
            front.append("pdf_url: %s" % q(p["pdf_url"]))
        if p.get("wayback_url"):
            front.append("wayback_url: %s" % q(p["wayback_url"]))
        if p.get("note"):
            front.append("note: %s" % q(p["note"]))
        if p.get("file"):
            front.append("file: %s" % q(p["file"]))
            front.append("file_source: %s" % q(p.get("file_source")))
            front.append("file_pages: %d" % int(p["file_pages"]))
            front.append("file_status: %s" % q(p.get("file_status", "held")))
            front.append("file_url: %s" % q(p.get("file_url")
                                            or "/papers/" + p["file"]))
            if p.get("file_licence"):
                front.append("file_licence: %s" % q(p["file_licence"]))
        if p.get("additional_files"):
            for extra in p["additional_files"]:
                front.append("additional_file: %s" % q("%s (%d pp.) - %s"
                                                        % (extra["file"],
                                                           extra["pages"],
                                                           extra["label"])))
                if extra.get("file_licence"):
                    front.append("additional_file_licence: %s"
                                 % q("%s: %s" % (extra["file"],
                                                extra["file_licence"])))
        if p.get("alternate_urls"):
            front.append(
                "alternate_urls: [%s]"
                % ", ".join(q(a) for a in p["alternate_urls"]))
        if profile_only:
            front.append("url_status: profile_page_only")

        is_yaqeen = "yaqeen" in str(p.get("publisher_journal", "")).lower()
        is_cc = (p.get("id") == CC_PAPER_ID)

        body = [_h1(title), ""]
        meta_bits = []
        if p.get("publisher_journal"):
            meta_bits.append(str(p["publisher_journal"]))
        if pub:
            meta_bits.append(str(pub))
        if p.get("type"):
            meta_bits.append(str(p["type"]))
        if meta_bits:
            body.append("*%s*" % " — ".join(meta_bits))
            body.append("")
        if p.get("co_authors"):
            body.append("Co-authors: %s" % ", ".join(p["co_authors"]))
            body.append("")
        if is_yaqeen:
            body.append(
                "Originally published by Yaqeen Institute for Islamic "
                "Research. Attribution preserved; this page links out and "
                "does not reproduce the full text."
            )
            body.append("")
        if p.get("file") or p.get("additional_files"):
            body.append("## Available sources")
        else:
            body.append("## Available sources (link-outs only)")
        body.append("")
        if profile_only:
            body.append(
                "**Availability: Unavailable** — the source data links this "
                "entry to a generic author profile page "
                "(independent.academia.edu/AsadullahAli/Talks), not a direct "
                "paper URL. No direct publisher page, PDF, or archived copy "
                "was located in the source data."
            )
            body.append("")
        if p.get("url") and not profile_only:
            body.append("- [View Original](%s)" % p["url"])
        elif p.get("url") and profile_only:
            body.append(
                "- [Author profile page (not a direct paper link)](%s)"
                % p["url"]
            )
        if p.get("pdf_url"):
            if is_cc and not p.get("file"):
                body.append(
                    "- [PDF via Internet Archive (CC-licensed, link-out; "
                    "nothing mirrored in this repo)](%s)" % p["pdf_url"]
                )
            elif p.get("file"):
                body.append(
                    "- [PDF via publisher (the copy in this repository was "
                    "obtained from the open source named below, not from this "
                    "page)](%s)" % p["pdf_url"]
                )
            else:
                body.append(
                    "- [PDF via publisher (link-out; not mirrored)](%s)"
                    % p["pdf_url"]
                )
        if p.get("wayback_url"):
            body.append("- [Wayback Machine](%s)" % p["wayback_url"])
        body.append("")
        held_files = ([p["file"]] if p.get("file") else []) + \
                     [e["file"] for e in (p.get("additional_files") or [])]
        if held_files:
            body.append("## Full text held in this repository")
            body.append("")
            for f in held_files:
                if p.get("file") == f:
                    pages, lic, src = p["file_pages"], p.get("file_licence"), \
                        p.get("file_source")
                else:
                    e = next(x for x in p["additional_files"] if x["file"] == f)
                    pages, lic = e["pages"], e.get("file_licence")
                    src = e.get("venue_url")
                body.append(
                    "- [%s]({{ \"/papers/%s\" | relative_url }}) - %d pp."
                    % (f, f, pages))
                body.append("")
                if src:
                    body.append("  - Obtained from: <%s>" % src)
                else:
                    body.append("  - Obtained from: **no verified public URL** "
                                "(see the licence note below)")
                body.append("  - Licence / provenance: %s" % (lic or "not recorded"))
                body.append("")
        else:
            body.append(
                "This archive links to the original publisher page. "
                "No PDF is mirrored in this repository."
            )
            body.append("")
            # A row can hold a file and still not publish it: `withheld_note` is
            # the plain-language reason, and it is data, not prose here, so the
            # page cannot drift from `_data/papers.json`. A row that never had a
            # file simply has no note and gets the sentence above alone.
            if p.get("withheld_note"):
                body.append(p["withheld_note"])
                body.append("")
        write_md(PAPERS_DIR, slug + ".md", front, "\n".join(body))
    print("papers: wrote %d (%d profile_page_only)" % (len(papers), n_profile_only))
    # Deliberately updated 2026-09-08: all 7 generic /Talks URLs replaced with
    # verified per-talk URLs (Task P) — expect 0 profile-only rows.
    assert n_profile_only == 0, "expected 0 /Talks rows, got %d" % n_profile_only
    # C2 (review-phase2): every PDF in _papers/pdfs/ must be named by a paper
    # row, or it is a held file that appears on no page - the exact failure the
    # files_extra/additional_files key mismatch produced.
    named = set()
    for p in papers:
        if p.get("file"):
            named.add(p["file"])
        for extra in p.get("additional_files") or []:
            named.add(extra["file"])
    on_disk = {f.name for f in PAPERS_DIR.glob("pdfs/*.pdf")}
    orphan_files = on_disk - named
    assert not orphan_files, \
        "PDF(s) in _papers/pdfs/ named by no paper row: %s" % sorted(orphan_files)
    missing_files = {f for f in named
                     if not (PAPERS_DIR / "pdfs" / f).is_file()}
    assert not missing_files, \
        "paper row names a PDF that is not in _papers/pdfs/: %s" % sorted(missing_files)
    # Jekyll copies a collection's static files to the COLLECTION ROOT, not into
    # a subdirectory, so the served URL is /papers/<file>.pdf. Verified against
    # _site by scripts/test_canonical_57.py's collection_drift() companion and by
    # the integration report; a /papers/pdfs/... link 404s.
    bad_link = [paper_slug(p["title"]) for p in papers if p.get("file")
                and "/papers/pdfs/" in (PAPERS_DIR / (paper_slug(p["title"]) + ".md"))
                .read_text(encoding="utf-8")]
    assert not bad_link, \
        "paper page(s) link into /papers/pdfs/, which Jekyll does not serve: %s" \
        % bad_link
    print("papers: %d held PDF(s) in _papers/pdfs/, all named by a paper row, "
          "linked at /papers/<file>.pdf" % len(on_disk))


def collection_drift():
    """C1 (review-phase2): every generated collection must hold exactly one page
    per data row, by NAME not just by count.

    Returns a list of human-readable failure strings; empty means no drift. The
    commit reviewed here shipped a 67-row video catalogue against 68 `_videos/`
    pages, so 11 search results 404'd and 12 uncounted videos stayed public,
    with nothing catching it. This is the gate that class of drift needs.

    The one documented exception is `_posts/`, which is not 1:1 with found
    works - see UNCLAIMED_POSTS below.
    """
    problems = []

    def cmp_names(label, expected, on_disk):
        missing, extra = sorted(expected - on_disk), sorted(on_disk - expected)
        if missing or extra:
            problems.append(
                "%s drift: %d page(s) missing %s; %d unexpected %s"
                % (label, len(missing), missing[:6], len(extra), extra[:6]))

    works = json.loads(CANON_JSON.read_text(encoding="utf-8"))
    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    papers = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    mdi = json.loads(MDI_JSON.read_text(encoding="utf-8")) if MDI_JSON.is_file() else []
    notices = (json.loads(NOTICES_JSON.read_text(encoding="utf-8"))
               if NOTICES_JSON.is_file() else [])

    # 1:1, name for name
    cmp_names("_videos", video_filenames(videos),
              {p.name for p in VIDEOS_DIR.glob("*.md")})
    cmp_names("_papers", {"%s.md" % paper_slug(p.get("title", ""))
                          for p in papers},
              {p.name for p in PAPERS_DIR.glob("*.md")})
    cmp_names("_articles",
              ({"%s.md" % w["slug"] for w in works}
               | {"mdi-%s.md" % r["slug"] for r in mdi}
               | {"notice-%s.md" % n["slug"] for n in notices}),
              {p.name for p in ARTICLES_DIR.glob("*.md")})
    # 2026-09-27 (task 8d): one page per CAPTURE the coverage file names, not
    # one per video, so the alternates and the preserved-but-unattached
    # captures are gated too. A coverage row that names a file with no page is
    # transcript text the archive holds and no reader can reach.
    cov = json.loads(COVERAGE_JSON.read_text(encoding="utf-8")) \
        if COVERAGE_JSON.is_file() else []
    cmp_names("_transcripts", transcript_filenames(cov),
              {p.name for p in TRANSCRIPTS_DIR.glob("*.md")})

    # _posts is NOT 1:1 with found works: a wayback_only work may still have a
    # partial local file. The gate is therefore: every found work resolves to
    # exactly one file, no file is claimed twice, and the unclaimed files are
    # exactly the documented set.
    #
    # N2 (re-review, 2026-09-27): resolution is by SLUG, not by date. The
    # previous version globbed "<date>-*.md", so any file sharing a date with a
    # found work was silently attributed to it. That mis-filed
    # _posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md
    # (a wayback_only work's partial text) under
    # extraordinary-claims-require-extraordinary-evidence-says-ordinary-intellect
    # (a found work) merely because both files carry the date 2015-05-12 - which
    # also hid a genuine unclaimed file from the exception list below.
    found = [w for w in works if w.get("status") == "found"]
    by_fm = posts_by_front_matter_slug()
    pointers = articles_local_post_pointers()
    claimed = {}
    for w in found:
        got = resolve_work_post(w, by_fm, pointers)
        if got:
            claimed.setdefault(got, []).append(w["slug"])
    unresolved = [w["slug"] for w in found
                  if not any(w["slug"] in v for v in claimed.values())]
    if unresolved:
        problems.append("_posts: found work(s) with no local file: %s" % unresolved)
    twice = sorted(f for f, v in claimed.items() if len(v) > 1)
    if twice:
        problems.append("_posts: file(s) claimed by 2 found works: %s" % twice)
    on_disk = {p.name for p in POSTS_DIR.glob("*.md")}
    stray = sorted(on_disk - set(claimed))
    if stray != sorted(UNCLAIMED_POSTS):
        problems.append(
            "_posts: unclaimed local file(s) %s differ from the documented "
            "exception list %s - update UNCLAIMED_POSTS in build_collections.py "
            "with the reason for each" % (stray, sorted(UNCLAIMED_POSTS)))
    return problems


# A YouTube video id is exactly 11 characters of [A-Za-z0-9_-]. Two ids in this
# archive are not YouTube ids and are longer: they are Facebook's numeric
# post/video ids, and they are kept verbatim because they are what the platform
# published. Both are gated by the rule below rather than by a hardcoded list, so
# a third platform id does not need a code change to be accepted.
#
# The shape test exists because the failure this guard exists for is a
# TRANSPOSED PAIR: `7KBCENktOUU` for `7KBCENktOOU` - same length, same
# characters, one adjacent swap. A transposed id passes every "is it 11 chars"
# test and every "is it a known id" test, and only 404s on the live site. That
# exact typo did ship once, as a `.gitignore` rule naming a capture file that
# does not exist, which meant the capture that really held the withheld name was
# not ignored and `git add -A` would have published it. A count gate cannot see
# that class of bug at all.
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
PLATFORM_ID_RE = re.compile(r"^[0-9]{12,}$")
# A coverage row's `file` is the transcript SOURCE it was built from, and this
# archive holds two kinds: a verbatim WebVTT caption capture
# (`cap-<id>.<lang>.vtt`, 29 of them) and a machine-transcription JSON
# (`whisper-<id>.json`, 39 of them). Both are named after the recording, so both
# carry the id and both are reconciled. A row with neither is a recorded
# negative result - a probe that found no captions - and is left alone.
CAPTURE_FILE_RE = re.compile(
    r"^(?:cap-([A-Za-z0-9_-]+)\.[A-Za-z0-9-]+\.vtt|whisper-([A-Za-z0-9_-]+)\.json)$")


def _fm_str(fm, key):
    m = re.search(r'^%s:\s*"?([^"\n]*)"?\s*$' % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else None


def _plausible_id(vid):
    return bool(vid) and bool(YOUTUBE_ID_RE.match(vid)
                              or PLATFORM_ID_RE.match(vid))


def _is_transposition(a, b):
    """True when `a` and `b` are the same characters in a different order.

    Same length and same multiset, but not equal, means a pair was reordered -
    and for an 11-character id that is almost always a single adjacent swap.
    Sharper and far cheaper than an edit distance, and it does not fire on an id
    that merely looks similar.
    """
    return len(a) == len(b) and a != b and sorted(a) == sorted(b)


def video_id_agreement():
    """A recording's id must be the SAME STRING in every place that names it.

    One recording's id is written in six independent places: the catalogue row,
    the coverage row, the capture file's own name, the published transcript
    document, the video page, and the ignore rules that keep a withheld capture
    unpublished. Nothing forces those to agree, and a disagreement is invisible
    in review because every place still looks like a plausible id. The symptom
    is a 404 on the live site or a silently published capture, never a build
    error.

    Two id-shaped things in the tree are NOT the video id, and are reconciled
    rather than flagged, because they are deliberate:

      * a transcript document for a re-upload carries the disambiguating
        `-duplicate-upload` suffix in `transcript_id` and in its permalink, so
        two documents for one recording get distinct URLs. The id of the
        recording is in `capture_video_id`, which is what this checks.
      * a video page whose id begins with `_` is written `video-<id>.md`, so the
        filename is a valid, non-hidden Jekyll document name. The id of the
        recording is in the `video_id` front matter, which is what this checks.

    Returns a list of human-readable failure strings; empty means agreement.
    """
    problems = []
    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    cov = json.loads(COVERAGE_JSON.read_text(encoding="utf-8")) \
        if COVERAGE_JSON.is_file() else []

    catalogue = {}
    for v in videos:
        vid = str(v.get("id") or "")
        if not _plausible_id(vid):
            problems.append("videos.json: id %r is neither an 11-character "
                            "YouTube id nor a platform id" % vid)
        if vid in catalogue:
            problems.append("videos.json: id %s appears on two rows" % vid)
        catalogue[vid] = v

    known = set(catalogue)
    for row in cov:
        for vid in [row.get("video_id")] + [a.get("video_id")
                                            for a in row.get("alternates") or []]:
            if vid:
                known.add(str(vid))

    # place -> the id it asserts. One entry per place, so a place that asserts
    # two different things is a failure rather than a silent overwrite.
    asserted = {}

    def assert_same(place, vid, why):
        if not vid:
            return
        prev = asserted.get(place)
        if prev is not None and prev != vid:
            problems.append("%s asserts id %s and also %s (%s)"
                            % (place, prev, vid, why))
        else:
            asserted[place] = vid
        if not _plausible_id(vid):
            problems.append("%s: %r is neither an 11-character YouTube id nor "
                            "a platform id" % (place, vid))

    # 1. the coverage rows and the capture file each one names. An ALTERNATE
    #    names a capture file too, and those are load-bearing in exactly the
    #    same way - three of them are the withheld captures of 6.2, and the
    #    published transcript for a re-upload is built from one - so they are
    #    reconciled here too rather than skipped.
    def check_capture(cap, owner, where):
        if not cap:
            return
        m = CAPTURE_FILE_RE.match(cap)
        if not m:
            problems.append("%s: %r is not a transcript source of the form "
                            "cap-<id>.<lang>.vtt or whisper-<id>.json"
                            % (where, cap))
            return
        from_name = m.group(1) or m.group(2)
        assert_same("transcript source %s" % cap, from_name, "source filename")
        if owner and from_name != owner:
            problems.append("transcript source %s names id %s but %s is for %s"
                            % (cap, from_name, where, owner))
        if not (CAPTURE_DIR / cap).is_file():
            problems.append("transcript source named by %s does not exist on "
                            "disk: %s" % (where, cap))

    for row in cov:
        rid = str(row.get("video_id") or "")
        place = "transcript_coverage.json video_id %s" % rid
        assert_same(place, rid, "coverage row")
        check_capture(str(row.get("file") or ""), rid, "its coverage row")
        for alt in row.get("alternates") or []:
            aid = str(alt.get("video_id") or "")
            assert_same("transcript_coverage.json alternate video_id %s" % aid,
                        aid, "coverage alternate")
            if aid and alt.get("reparented_onto") == aid:
                problems.append("transcript_coverage.json: capture %s is "
                                "reparented onto itself" % aid)
            check_capture(str(alt.get("file") or ""), aid,
                          "coverage alternate %s" % aid)

    # 2. the published transcript documents
    for p in sorted(TRANSCRIPTS_DIR.glob("*.md")):
        fm = front_matter_of(p.read_text(encoding="utf-8"))
        vid = _fm_str(fm, "capture_video_id")
        assert_same("_transcripts/%s capture_video_id" % p.name, vid,
                    "transcript front matter")
        cap = _fm_str(fm, "capture_file") or ""
        m = CAPTURE_FILE_RE.match(cap)
        if m:
            from_name = m.group(1) or m.group(2)
            assert_same("transcript source %s" % cap, from_name,
                        "source filename")
            if vid and from_name != vid:
                problems.append(
                    "_transcripts/%s: capture_file %s names id %s but "
                    "capture_video_id is %s"
                    % (p.name, cap, from_name, vid))
        tid = _fm_str(fm, "transcript_id")
        if vid and tid and not str(tid).startswith(vid):
            problems.append("_transcripts/%s: transcript_id %r does not carry "
                            "the recording id %s" % (p.name, tid, vid))
        permalink = _fm_str(fm, "permalink") or ""
        if vid and ("/transcripts/%s" % vid) not in permalink:
            problems.append("_transcripts/%s: permalink %r does not carry the "
                            "recording id %s" % (p.name, permalink, vid))

    # 3. the video pages
    for p in sorted(VIDEOS_DIR.glob("*.md")):
        stem = p.name[:-3]
        fm = front_matter_of(p.read_text(encoding="utf-8"))
        vid = _fm_str(fm, "video_id")
        assert_same("_videos/%s video_id" % p.name, vid, "video front matter")
        if vid:
            other = _fm_str(fm, "id")
            if other != vid:
                problems.append("_videos/%s: id is %r but video_id is %r"
                                % (p.name, other, vid))
            if stem != vid and stem != "video-" + vid:
                problems.append("_videos/%s: filename stem %r is neither the "
                                "recording id %s nor video-%s"
                                % (p.name, stem, vid, vid))
            if vid not in catalogue:
                problems.append("_videos/%s: video_id %s is not a row in "
                                "videos.json" % (p.name, vid))

    # 4. the transposition sweep. Every id any place asserts, against every id
    #    the data knows. A neighbour that is a permutation of a real id is the
    #    typo this guard was written for, and it is the one a shape test misses.
    for place, vid in sorted(asserted.items()):
        if vid in known:
            continue
        twins = sorted(k for k in known if _is_transposition(vid, k))
        if twins:
            problems.append(
                "%s asserts %r, which is a transposition of %s - a transposed "
                "id is a 404 on the live site, and a mis-spelled .gitignore "
                "capture rule publishes a withheld capture"
                % (place, vid, " and ".join(twins)))
        else:
            problems.append("%s asserts %r, which no data file names"
                            % (place, vid))

    # 5. one source, one recording. Two ids claiming the same capture is a
    #    split identity: the transcript would be served under the wrong URL.
    by_cap = {}
    for place, vid in asserted.items():
        m = re.match(r"^transcript source (\S+)$", place)
        if m:
            by_cap.setdefault(m.group(1), set()).add(vid)
    for cap, ids in sorted(by_cap.items()):
        if len(ids) > 1:
            problems.append("transcript source %s is claimed by more than one "
                            "id: %s" % (cap, ", ".join(sorted(ids))))

    # 6. every `cap-<id>` ignore rule must name a file that exists. A rule for
    #    a capture that is not there ignores nothing, and the real capture goes
    #    in on the next `git add -A`.
    gi = BASE / ".gitignore"
    if gi.is_file():
        for n, raw in enumerate(gi.read_text(encoding="utf-8")
                                .splitlines(), 1):
            name = raw.strip().rsplit("/", 1)[-1]
            if not raw.strip().startswith(".firecrawl/transcripts/cap-") \
                    or not CAPTURE_FILE_RE.match(name):
                continue
            if not (CAPTURE_DIR / name).is_file():
                problems.append(
                    ".gitignore:%d ignores %s, which is not a file that exists "
                    "- the capture that rule was written to protect is not "
                    "ignored, and `git add -A` would publish it"
                    % (n, name))
    return problems


def front_matter_of(text):
    """Return the front-matter block of a Jekyll markdown file (or "" if the
    file has none). Same `split("---", 2)` convention the fetch and test
    scripts already use."""
    return text.split("---", 2)[1] if text.count("---") >= 2 else ""
def posts_by_front_matter_slug():
    """Map each `_posts` front-matter `slug:` to its filename."""
    out = {}
    for path in sorted(POSTS_DIR.glob("*.md")):
        m = re.search(r"^slug:\s*(.+?)\s*$", front_matter_of(
            path.read_text(encoding="utf-8")), re.M)
        if m:
            out.setdefault(m.group(1).strip().strip("\"'"), path.name)
    return out


def articles_local_post_pointers():
    """Map each `_articles` `local_post:` value to its `_posts` filename.

    47 `_articles` rows carry a `local_post:` pointer; it is the authoritative
    link from a found work to the file holding its recovered text, and it does
    not depend on the date at all.
    """
    out = {}
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        m = re.search(r"^local_post:\s*(.+?)\s*$", front_matter_of(
            path.read_text(encoding="utf-8")), re.M)
        if m:
            out.setdefault(path.stem, m.group(1).strip().strip("\"'"))
    return out


def resolve_work_post(work, by_fm, pointers):
    """Return the single `_posts` filename that holds this work's local text.

    Tried in order of how explicit the link is:
      1. `<date>-<slug>.md`               exact filename, no inference at all
      2. `_articles` `local_post:`        an authored pointer for this slug
      3. front-matter `slug:`            a date-independent declared identity
    A date match on its own is never sufficient, which is the N2 fix.
    """
    slug, date = work["slug"], work["date"]
    exact = "%s-%s.md" % (date, slug)
    if (POSTS_DIR / exact).is_file():
        return exact
    target = pointers.get(slug)
    if target and (POSTS_DIR / path_basename(target)).is_file():
        return path_basename(target)
    got = by_fm.get(slug)
    if got and (POSTS_DIR / got).is_file():
        return got
    return None


def path_basename(p):
    return p.replace("\\", "/").rsplit("/", 1)[-1]


# DOCUMENTED EXCEPTION for the _posts leg of collection_drift(). These 7 files
# hold partial local text for works the archive classifies wayback_only, so they
# are not the "full text" of a counted work and are not claimed by one. They are
# kept because deleting them would lose recovered prose, and they are the local
# target of transcript joins in TRANSCRIPT_MAP.
#
# Word counts are `len(body_after_front_matter.split())`, the same measure
# build_articles() and the transcript suites use, so the figures below match
# `words:` in the generated pages. Counting the whole file including front
# matter would give a different range, which is the trap the re-review caught:
# the old comment said "91-184 w" and omitted the 76-word file, because the
# date-based join had hidden it.
#
# 2015-05-12-still-colonized-liberalism-in-muslim-thought.md  76 w
#   Partial text of a wayback_only work. Added 2026-09-27 (fix round 2, N2):
#   the date-only join attributed it to the found work
#   extraordinary-claims-require-extraordinary-evidence-says-ordinary-intellect,
#   so it never appeared as unclaimed. Its filename slug is exactly the work
#   slug, so resolve_work_post() step 1 does not match it either - it is not a
#   found work and must not be claimed. It is also the source file that proves
#   the MDI row still-colonised-liberalism-in-muslim-thought is a duplicate
#   (5-gram containment 1.0000); see _data/mdi_articles.json.
# 2017-12-22-the-atheistic-worldview-vs-the-quranic-worldview.md  91 w
# 2017-12-22-understanding-atheism.md                            161 w
# 2018-05-09-islam-science-and-history.md                          93 w
# 2018-06-20-atheism-doubting-your-doubts.md                     165 w
# 2018-10-02-understanding-aishas-age-an-interdisciplinary-approach.md
#                                                                184 w
# 2018-11-14-hard-questions-answering-doubts-about-islam.md       96 w
UNCLAIMED_POSTS = {
    "2015-05-12-still-colonized-liberalism-in-muslim-thought.md",
    "2017-12-22-the-atheistic-worldview-vs-the-quranic-worldview.md",
    "2017-12-22-understanding-atheism.md",
    "2018-05-09-islam-science-and-history.md",
    "2018-06-20-atheism-doubting-your-doubts.md",
    "2018-10-02-understanding-aishas-age-an-interdisciplinary-approach.md",
    "2018-11-14-hard-questions-answering-doubts-about-islam.md",
}


def video_filenames(videos):
    """The filename build_videos() gives each entry (Jekyll skips files that
    start with _ or ., so those get a readable prefix; the permalink still
    comes from the explicit `permalink:` front matter)."""
    return {("%s.md" % (v["id"] if str(v["id"])[:1] not in ("_", ".")
                         else "video-" + str(v["id"]))) for v in videos}


# ---------------------------------------------------------------- videos ---
# Characters that terminate an href attribute and make Liquid escape the rest
# of the tag. A video URL must never contain one.
_HREF_BREAK = re.compile(r'["<>`]')

# 2026-09-27 (on-page SEO pass): bidirectional isolation for a mixed-script
# title.
#
# `_data/videos.json` has exactly one title written in a right-to-left script
# (`s_BnmOrVaTg`: an Arabic-script title followed by a Latin transliteration,
# separated by neutral characters). Rendered inside this site's `lang="en"`
# LTR document, the Unicode Bidi Algorithm may reorder the neutrals at the
# boundary, so the title can appear scrambled in a browser and, worse, in a
# search result.
#
# Liquid cannot detect a script, and `<bdi>` cannot be emitted from a layout
# without knowing where the non-Latin run starts and ends. So the run is
# detected here, where the string is, and the two outputs a page needs are
# written into front matter:
#
#   title_runs  - a list of {text, lang, dir}, so the layout can print the
#                 <span lang dir> per run and the reader sees correct shaping
#                 and correct screen-reader pronunciation.
#   title_iso   - the same string with U+2066 LEFT-TO-RIGHT ISOLATE /
#                 U+2069 POP DIRECTIONAL ISOLATE wrapped around each non-Latin
#                 run, for the places that cannot carry markup: <title>,
#                 og:title, twitter:title and the JSON-LD `name`.
#
# A title with no non-Latin character gets neither field, so 67 of the 68 video
# pages are byte-identical to what they were before this. Nothing is guessed:
# the script ranges below are checked, not inferred, and an unrecognised
# non-Latin run still gets isolated, just without a language tag.
# Characters that are typographically CORRECT in the recorded title but paint
# far outside the line box, so they have to be rendered at a different size than
# the text around them.
#
# U+29F8 BIG SOLIDUS is the one that occurs. The author used it as an ordinary
# slash ("w⧸" for "with"), which is what the Unicode Consortium's own definition
# covers: it is a "big" slash, a slash intended to span a full em, and that is
# exactly why it is wrong at text size. Measured with canvas
# `actualBoundingBoxAscent/Descent` at the 41.6px h1:
#
#     U+29F8 in Lato / Source Sans Pro / Segoe UI / Georgia / Merriweather /
#            Noto Sans Symbols 2 / Apple Symbols / sans-serif / serif
#            -> ascent 52, descent 28, total 80px, against a 30px cap height
#               and a 47.84px line box. It inks 2.67x the cap and overflows its
#               own line by 32px, which is the reported visual break.
#     the same glyph in 'Segoe UI Symbol' -> 40px total, which fits.
#
# The other fullwidth characters were measured in the same pass and are FINE, so
# they are deliberately not listed here: U+FF5C ｜ (207 titles) inks 1.53x cap,
# U+FF1A ： (52) 0.83x, U+FF02 ＂ (34) 0.37x, U+FF1F ？ (15) 1.13x, U+300C 「 1.37x,
# U+FF08 （ 1.33x, and Arabic ALEF 1.03x. Only the big solidus breaks the line.
_TALL_GLYPHS = {
    "⧸": 0.55,   # U+29F8 BIG SOLIDUS
    "⧵": 0.55,   # U+29F5 REVERSE SOLIDUS OPERATOR
    "⫽": 0.55,   # U+2AFD DOUBLE SOLIDUS OPERATION
}


def _h1(title) -> str:
    """A generated body heading, with any oversized glyph wrapped for rendering.

    The heading itself must NOT be deleted. Every one of these folders is read by
    line number - the 501 verified topic quotations cite `_posts`,
    `_transcripts`, `_articles` and `_papers` at a specific line - and removing
    the leading heading shifts every citation below it by one. Measured: removing
    it broke 60 transcript citations and 7 paper citations outright. A cited line
    is recorded provenance, and rewriting 501 of them to suit a heading is
    exactly the silent alteration this archive does not make.

    What can be fixed is the rendering. Wrapping the glyph here is inline HTML
    on the SAME line, so no citation moves, and lets `.tall-glyph` size it. The
    character in the data is unchanged; only the markup around it is.
    """
    text = str(title or "")
    for ch in _TALL_GLYPHS:
        text = text.replace(ch, '<span class="tall-glyph">%s</span>' % ch)
    return "# %s" % text


_BIDI_RANGES = (
    ("ar", 0x0600, 0x06FF, "rtl"),   # Arabic
    ("he", 0x0590, 0x05FF, "rtl"),   # Hebrew
    ("fa", 0xFB50, 0xFDFF, "rtl"),   # Arabic Presentation Forms-A
    ("ur", 0x08A0, 0x08FF, "rtl"),   # Arabic Extended-A
)
_BIDI_CJK_RANGES = (
    ("ja", 0x3000, 0x30FF, None),    # CJK punctuation, Hiragana, Katakana
    ("ja", 0x3400, 0x4DBF, None),    # CJK Extension A
    ("zh", 0x4E00, 0x9FFF, None),    # CJK Unified Ideographs
)
_LRI = "⁦"   # LEFT-TO-RIGHT ISOLATE
_RLI = "⁧"   # RIGHT-TO-LEFT ISOLATE
_PDI = "⁩"   # POP DIRECTIONAL ISOLATE


def _bidi_script(ch):
    """(lang, dir) for a character, or None when it is not a non-Latin script."""
    cp = ord(ch)
    for lang, lo, hi, direction in _BIDI_RANGES:
        if lo <= cp <= hi:
            return lang, direction
    for lang, lo, hi, _direction in _BIDI_CJK_RANGES:
        if lo <= cp <= hi:
            return lang, None
    return None


def title_bidi(title):
    """Split a title into script runs. Returns [] when the title is plain.

    Whitespace is NEUTRAL, so it is absorbed into the run before it rather than
    treated as a script change of its own. Without that, an Arabic title
    separated by single spaces would come back as one run per WORD
    ("مناظره" | " " | "عبدالله" | ...), which is both unusable as markup and
    useless for isolation, because the space is exactly the neutral character
    that needs protecting. A leading space, having no run before it, joins the
    first real run.
    """
    runs = []
    for ch in str(title or ""):
        if ch.isspace() and runs:
            runs[-1][1] += ch
            continue
        script = _bidi_script(ch)
        key = ("ltr", None) if script is None else script
        if runs and tuple(runs[-1][0]) == key:
            runs[-1][1] += ch
        else:
            runs.append([list(key), ch])
    if not runs or (len(runs) == 1 and tuple(runs[0][0]) == ("ltr", None)):
        return []
    return [(r[0][0], r[0][1], r[1]) for r in runs]


def front_matter_bidi(title):
    """The two front-matter keys _layouts/video.html reads, or [] for a title
    that needs no isolation at all.

    `title_iso` wraps each non-Latin run in the matching directional isolate
    pair (RLI...PDI for a right-to-left script, LRI...PDI otherwise) and leaves
    the Latin runs alone, so the neutral characters at a boundary sit inside an
    isolate and the Bidi Algorithm cannot move them across it.
    """
    runs = title_bidi(title)
    if not runs:
        return []
    out = ["title_runs: [%s]" % ", ".join(
        '{"text": %s, "lang": %s, "dir": %s}' % (
            q(text), q(lang) if lang else "null",
            q(direction) if direction else "null")
        for lang, direction, text in runs
    )]
    iso = []
    for lang, direction, text in runs:
        if direction == "rtl":
            iso.append(_RLI + text + _PDI)
        elif direction is None and lang:
            iso.append(_LRI + text + _PDI)
        else:
            iso.append(text)
    out.append("title_iso: %s" % q("".join(iso)))
    return out


def build_videos():
    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    # The absolute video count belongs to _data/videos.json (I2 owns that file
    # and test_search_sync.py asserts data/videos.json against it). What this
    # builder must guarantee is the shape, not the snapshot size: non-empty,
    # unique, case-unique ids and a mirror_urls list on every row.
    yt_only = [v for v in videos if is_youtube(v.get("archive_url", ""))]
    ids = [str(v.get("id", "")) for v in videos]
    assert videos, "videos.json is empty"
    assert all(ids), "video with empty id"
    assert len(set(ids)) == len(ids), "duplicate video ids"
    lowered = [i.lower() for i in ids]
    assert len(set(lowered)) == len(ids), "case-colliding video ids (win fs risk)"
    for v in videos:
        assert isinstance(v.get("mirror_urls", []), list), \
            "video %s has a non-list mirror_urls" % v.get("id")
        # A raw " < > or ` in a URL terminates the href attribute and Liquid
        # escapes the rest of the tag, silently breaking the link. One entry
        # (Dr5IgXCHRIE) shipped that way; this gate stops it recurring.
        for key in ("archive_url", "youtube_url"):
            u = v.get(key)
            assert not (u and _HREF_BREAK.search(u)), \
                "video %s %s contains a character that breaks an href: %r" \
                % (v.get("id"), key, u)
        for u in v.get("mirror_urls") or []:
            assert not _HREF_BREAK.search(u), \
                "video %s mirror_urls contains a character that breaks an " \
                "href: %r" % (v.get("id"), u)
    # I5 (review-phase2): the `youtube_not_archived` branch that videos.md and
    # _layouts/video.html key off has no other gate. Pin its population: an entry
    # is rendered as YouTube-only exactly when its archive_url is a YouTube URL,
    # and exactly those entries are the ones F6/I2 declared with an explicit
    # `kind`. Assert the two sets are identical in both directions.
    kind_ids = {str(v.get("id")) for v in videos if v.get("kind")}
    yt_ids = {str(v.get("id")) for v in yt_only}
    assert yt_ids == kind_ids, (
        "youtube_not_archived population drifted: only-YouTube=%s, "
        "kind-declared=%s, symmetric difference=%s"
        % (sorted(yt_ids), sorted(kind_ids), sorted(yt_ids ^ kind_ids)))
    for v in yt_only:
        assert "source" in v, \
            "catalogue-only YouTube video %s must record its source" % v["id"]

    # 2026-09-27 (R25, task 8d): the `transcripts` field, cross-checked against
    # the coverage file in BOTH directions, for EVERY entry and not only the
    # YouTube-only ones.
    #
    # The gate this replaces was `transcripts == 0` for every YouTube-only
    # entry. That was true while all 12 of them were caption-less, and R25
    # attached a preserved capture to G47Stp3pLss, so it is no longer true of
    # all of them. Deleting it would have left the field ungated, which is how
    # G47Stp3pLss came to say "Transcript not yet available" while its
    # transcript sat published one click away. The invariant worth pinning is
    # the one the page actually renders, and it is checked in both directions
    # so neither mistake can hide:
    #
    #   `transcripts: 0` present  <=>  no transcript is attached to the entry
    #   `transcripts` absent      <=>  a transcript IS attached
    #
    # "Attached" is read from _data/transcript_coverage.json - an active row
    # (not `superseded`) that names a capture file, not flagged
    # `attached_to_video_entry: false`, and whose id is in videos.json.
    attached = attached_transcript_ids()
    for v in videos:
        vid = str(v.get("id"))
        declared = v.get("transcripts")
        if vid in attached:
            assert declared is None, (
                "video %s has an attached transcript in "
                "transcript_coverage.json but still declares `transcripts: %r` "
                "- its page would say 'Transcript not yet available' while the "
                "text is published" % (vid, declared))
        else:
            assert declared == 0, (
                "video %s has no attached transcript in "
                "transcript_coverage.json but does not declare "
                "`transcripts: 0` (found %r)" % (vid, declared))
    n_attached = sum(1 for v in videos if str(v.get("id")) in attached)
    print("videos: %d attached transcript(s), %d catalogue-only entry/entries "
          "declaring `transcripts: 0`; the field agrees with "
          "transcript_coverage.json in both directions"
          % (n_attached, len(videos) - n_attached))
    clear_md(VIDEOS_DIR)
    n_yt = 0
    for v in videos:
        vid = str(v["id"])
        title = video_display_title(vid, v.get("title", ""))
        original_title = str(v.get("title", ""))
        if vid == DUP52_ID and title.startswith("52 -"):
            title = "53 -" + title[4:]
        youtube_only = is_youtube(v.get("archive_url", ""))
        if youtube_only:
            n_yt += 1
        front = [
            "layout: video",
            "title: %s" % q(title),
            "video_id: %s" % q(vid),
            "id: %s" % q(vid),
            # Explicit permalink preserves the exact-case YouTube id.
            # The collection template `/videos/:name/` slugifies (lowercases,
            # `_`->`-`, strips leading `-`), which would 404 every
            # search.md `/videos/<id>/` link on case-sensitive hosts.
            "permalink: %s" % q("/videos/" + vid + "/"),
            "archive_url: %s" % q(v.get("archive_url", "")),
        ]
        if youtube_only:
            front.append("source: youtube_not_archived")
            front.append("youtube_url: %s" % q(v.get("archive_url", "")))
        else:
            front.append("source: archive_org")
        if v.get("format"):
            front.append("format: %s" % q(v["format"]))
        if v.get("duration"):
            front.append("duration: %s" % q(v["duration"]))
        if v.get("tone"):
            front.append("tone: %s" % q(v["tone"]))
        front.append("themes: %s" % qlist(v.get("themes")))
        front.append("topics: %s" % qlist(v.get("topics")))
        # 2026-09-27 (amendment A): carry the counting-constraint fields
        # through to the collection pages so the page and the data agree.
        # Without these the attached mirror_urls were machine-readable in
        # _data/videos.json but invisible on the rendered page. _layouts/ is
        # not this builder's to change, so the values are exposed as front
        # matter for the layout to pick up (Task 8).
        front.append("mirror_urls: [%s]"
                     % ", ".join(q(u) for u in (v.get("mirror_urls") or [])))
        if v.get("kind"):
            front.append("kind: %s" % q(v["kind"]))
        if v.get("transcripts") is not None:
            front.append("transcripts: %d" % int(v["transcripts"]))
        if v.get("source") and v["source"] != "YouTube mirror":
            front.append("catalogue_source: %s" % q(v["source"]))
        if v.get("note"):
            front.append("note: %s" % q(v["note"]))
        # 2026-09-27 (on-page SEO pass): bidirectional isolation for a title
        # written in, or mixing, a non-Latin script. Emitted only for the one
        # title that needs it; the other 67 pages get no new key at all.
        front.extend(front_matter_bidi(title))

        body = [_h1(title), ""]
        if vid == DUP52_ID:
            body.append(
                "Numbering note: the source data lists this entry as "
                '"%s"; it is renumbered here to 53 to resolve the duplicate '
                '"52" numbering (the other 52 is Book Recommendations #2). '
                "Both videos are kept." % original_title
            )
            body.append("")
        if youtube_only:
            body.append("**Source: YouTube (not archived)**")
            body.append("")
            body.append(
                "This video has no Internet Archive copy in the source data. "
                "The link below goes to YouTube."
            )
            body.append("")
            body.append("- [Watch on YouTube](%s)" % archive_link(v))
            body.append("")
        else:
            body.append(
                "Preserved on the Internet Archive as part of the "
                "andalusian-project collection."
            )
            body.append("")
            body.append(
                "- [Download from Archive.org](%s)" % archive_link(v)
            )
            body.append("")
            body.append(
                "Theme descriptions use neutral academic language for "
                "research purposes."
            )
            body.append("")
        if v.get("themes"):
            body.append(
                "Themes: %s" % "; ".join(str(t) for t in v["themes"])
            )
            body.append("")
        mirrors = [u for u in (v.get("mirror_urls") or []) if u]
        if mirrors:
            body.append("**Mirrors of this same recording** (%d) - counted "
                        "once, under this entry:" % len(mirrors))
            body.append("")
            for u in mirrors:
                body.append("- <%s>" % u)
            body.append("")
        if v.get("kind"):
            body.append("Kind: %s" % v["kind"])
            body.append("")
        if v.get("note"):
            body.append(str(v["note"]))
            body.append("")
        # Jekyll skips collection files starting with `_`/`.`, so the
        # `_C5ox2zZl0U` video needs a readable filename; its URL still comes
        # from the explicit permalink above, so the search link is unaffected.
        fname = vid if not vid[:1] in ("_", ".") else "video-" + vid
        write_md(VIDEOS_DIR, fname + ".md", front, "\n".join(body))
    print("videos: wrote %d (%d youtube_not_archived)" % (len(videos), n_yt))


# --------------------------------------------------------------- articles ---
def post_index():
    """Map post date -> [(filename, post_slug, categories)] for _posts/*.md."""
    index = {}
    if not POSTS_DIR.is_dir():
        return index
    for path in sorted(POSTS_DIR.glob("*.md")):
        name = path.name
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$", name)
        if not m:
            continue
        date, post_slug = m.group(1), m.group(2)
        text = path.read_text(encoding="utf-8")
        parts = text.split("---")
        fm = parts[1] if len(parts) >= 3 else ""
        cats = []
        cm = re.search(
            r"^\s*categor(?:y|ies)\s*:\s*\[(.*)\]\s*$",
            fm,
            re.MULTILINE | re.IGNORECASE,
        )
        if cm:
            cats = [c.strip() for c in cm.group(1).split(",") if c.strip()]
        index.setdefault(date, []).append((name, post_slug, cats))
    return index


def match_post(work, index):
    """Match a canonical work to a local _posts file (date first)."""
    cands = index.get(str(work.get("date", "")), [])
    if len(cands) == 1:
        return cands[0]
    if len(cands) > 1:
        # Only 2015-05-12 collides; pick best slug token overlap.
        wtokens = set(str(work.get("slug", "")).split("-"))
        best, best_n = cands[0], -1
        for cand in cands:
            n = len(wtokens & set(cand[1].split("-")))
            if n > best_n:
                best, best_n = cand, n
        return best
    return None


def video_index():
    """Map video id -> row from _data/videos.json."""
    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    return {str(v.get("id", "")): v for v in videos}


def coverage_index():
    try:
        cov = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    return {r.get("video_id", ""): r for r in cov}


def attached_transcript_ids():
    """Video ids whose transcript is ATTACHED to their catalogue entry.

    2026-09-27 (R25, task 8d). One definition, used by the gate in
    build_videos(), by build_transcripts(), and by the /transcripts/ index, so
    "attached" cannot mean one thing in the data check and another in the
    rendering.

    A capture is attached when its coverage row is active (not `superseded`),
    names a capture file, is not explicitly flagged
    `attached_to_video_entry: false`, and belongs to an id that is in
    _data/videos.json. A capture belonging to a superseded upload that is not
    re-parented is therefore NOT attached - its text is published, but no
    catalogue entry claims it.
    """
    cov = json.loads(COVERAGE_JSON.read_text(encoding="utf-8")) \
        if COVERAGE_JSON.is_file() else []
    live = {str(v.get("id")) for v in
            json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))}
    return {str(r.get("video_id")) for r in cov
            if r.get("captions") and r.get("file")
            and r.get("superseded") is not True
            and r.get("attached_to_video_entry") is not False
            and str(r.get("video_id")) in live}


def transcript_section(slug, videos, coverage):
    """Render disclaimer + summary + collapsible transcript, or ''."""
    if slug not in TRANSCRIPT_MAP:
        return "", False
    entry = TRANSCRIPT_MAP[slug]
    vid, summary = entry[0], entry[1]
    parts = entry[2] if len(entry) > 2 else []
    row = coverage.get(vid, {})
    if not row.get("captions"):
        return "", False
    v = videos.get(vid, {})
    src = row.get("source", "")
    provenance = ("Whisper local transcription" if src.startswith("whisper")
                  else "YouTube auto-captions")
    try:
        dur = float(v.get("duration") or 0)
        duration = f"{int(dur // 60)} min" if dur else ""
    except (TypeError, ValueError):
        duration = ""
    archive_url = str(v.get("archive_url", "") or "")
    if "youtube.com/watch" in archive_url or "youtu.be" in archive_url:
        watch = archive_url
    elif vid and not v.get("preserved_in_repo"):
        watch = f"https://www.youtube.com/watch?v={vid}"
    else:
        watch = (f"https://www.youtube.com/watch?v={vid}" if vid else "")
    title = str(v.get("title", "") or slug).split("[")[0].strip() or slug
    # 2026-09-27 (R25 pass, task 8d): read the cues through parse_capture(),
    # the SAME reader the published transcript pages use, instead of
    # transcribe.load_segments(). Two readers of one capture file produced two
    # different texts for the same recording: load_segments() keeps YouTube's
    # rolling caption window, so every caption line was printed up to three
    # times in the article while the published transcript printed it once.
    # parse_capture() keeps the settled cue of each line and drops the window,
    # so the article and /transcripts/<id>/ now carry the same words in the
    # same order. Nothing is corrected, re-spelled or re-ordered: only the
    # repeated window and the byte-identical adjacent repeats go, and no word
    # is removed, because a repeat of the same words is still those words.
    capture = CAPTURE_DIR / str(row.get("file", ""))
    if not capture.is_file():
        return "", False
    segments = [(start, text) for start, _end, text in parse_capture(capture)]
    if not segments:
        return "", False
    body = vtt_to_article_md(title, "", slug, watch or archive_url,
                             duration, segments, provenance)
    lines = [
        "## About this recording",
        "",
        summary,
        "",
        DISCLAIMER.format(source=provenance),
        "",
    ]
    if parts:
        live = [p for p in parts if coverage.get(p, {}).get("captions")]
        if live:
            lines.append("Series parts with transcripts:")
            lines.append("")
            for n, p in enumerate(live, 2):
                lines.append(
                    "- [Session %d transcript]"
                    "({{ \"/videos/\" | relative_url }}%s/)" % (n, p))
            lines.append("")
    # 2026-09-27 (Task 7 / I1): transcript text from a video that left the
    # catalogue as a duplicate was re-parented onto its surviving twin rather
    # than deleted. Name the alternate captures so nothing looks lost.
    alts = [a for a in (row.get("alternates") or []) if a.get("file")]
    if alts:
        lines.append("This recording was also transcribed from %d superseded "
                     "duplicate upload(s), preserved rather than deleted:"
                     % len(alts))
        lines.append("")
        for a in alts:
            lines.append("- `%s` — %s (%s lines, %s)"
                         % (a.get("video_id"), a.get("title", ""),
                            a.get("lines", "?"), a.get("file")))
        lines.append("")
    lines += [
        "<details>",
        "<summary>Full transcript "
        f"({len(segments)} segments — click to expand)</summary>",
        "",
        body,
        "</details>",
        "",
    ]
    return "\n".join(lines), True


def post_url_for(filename, post_slug, cats):
    if cats:
        return "/" + "/".join([c.lower() for c in cats] + [post_slug]) + "/"
    return "/" + post_slug + "/"


def build_articles():
    works = json.loads(CANON_JSON.read_text(encoding="utf-8"))
    assert len(works) == 72, "expected 72 works, got %d" % len(works)
    index = post_index()
    videos = video_index()
    coverage = coverage_index()
    clear_md(ARTICLES_DIR)
    counts = {"found": 0, "wayback_only": 0, "lost": 0}
    n_transcripts = 0
    for w in works:
        slug = str(w.get("slug", "")).strip()
        title = str(w.get("title", "")).strip()
        date = str(w.get("date", "")).strip()
        status = str(w.get("status", "")).strip()
        wayback = w.get("wayback_url")
        assert slug and title and date, "bad canonical row: %r" % (w,)
        assert status in ("found", "wayback_only", "lost"), status
        counts[status] += 1

        front = [
            "layout: article",
            "title: %s" % q(title),
            "slug: %s" % q(slug),
            # Explicit permalink: matches search.md `/articles/<slug>/`.
            "permalink: %s" % q("/articles/" + slug + "/"),
            "date: %s" % q(date),
            "status: %s" % q(status),
        ]
        # Lost rows keep their capture only as reference_url (never a
        # button: article.html renders a button only for wayback_url).
        if status != "lost" and wayback:
            front.append("wayback_url: %s" % q(wayback))
        elif status == "lost" and wayback:
            front.append("reference_url: %s" % q(wayback))

        alternates = [a for a in (w.get("alternate_urls") or []) if a]
        alt_note = str(w.get("alternate_note", "") or "").strip()
        if alternates:
            front.append(
                "alternate_urls: [%s]"
                % ", ".join(q(a) for a in alternates)
            )
            if alt_note:
                front.append("alternate_note: %s" % q(alt_note))

        match = match_post(w, index) if status == "found" else None
        if match:
            fname, pslug, cats = match
            front.append("local_post: %s" % q("_posts/" + fname))
            front.append(
                "local_post_url: %s" % q(post_url_for(fname, pslug, cats))
            )

        body = [_h1(title), "", "*%s — status: %s*" % (date, status), ""]
        # I3 (review-phase2): the "Wayback Machine" label and the hardcoded
        # "Original site: asadullahali.com" line are both wrong for a work whose
        # text came from some other live site. Both are now data-driven.
        wb_label = str(w.get("wayback_label") or "Wayback Machine")
        site_note = str(w.get("source_site") or
                        "Original site: asadullahali.com (no longer online).")
        if status == "found" and match:
            fname, pslug, cats = match
            url = post_url_for(fname, pslug, cats)
            body.append("Full text preserved in this repository:")
            body.append("")
            body.append(
                "- [Read full text in this archive]({{ %s | relative_url }})"
                % q(url)
            )
            if wayback:
                body.append("- [%s](%s)" % (wb_label, wayback))
            body.append("")
            body.append(site_note)
            body.append("")
        elif status == "found":
            body.append("Full text preserved in this repository.")
            body.append("")
            if wayback:
                body.append("- [%s](%s)" % (wb_label, wayback))
                body.append("")
            body.append(site_note)
            body.append("")
        elif status == "wayback_only" and wayback:
            body.append("Wayback-only — no full text in this repository.")
            body.append("")
            body.append("- [Read on Wayback Machine](%s)" % wayback)
            body.append("")
        elif status == "wayback_only":
            # Feed-only row (library-take-down-notice): null URL.
            body.append(
                "Feed-only entry — no Wayback capture URL was recorded and "
                "no full text is preserved in this repository. Title and "
                "date kept for reference; this page intentionally provides "
                "no link button rather than a dead link."
            )
            body.append("")
        else:  # lost
            body.append(
                "Lost — no archived copy located. Title and date are "
                "preserved for reference. This page intentionally provides "
                "no link button rather than imply readable content exists."
            )
            body.append("")
        if alternates:
            body.append("Also available (related sources, not verbatim copies "
                        "unless stated):")
            body.append("")
            if alt_note:
                body.append("_%s_" % alt_note)
                body.append("")
            for alt in alternates:
                # A same-site link must be legible: label it with its slug,
                # otherwise the reader sees a bare URL. (I3)
                if alt.startswith("/"):
                    body.append("- [Archive page: %s]({{ \"%s\" | relative_url }})"
                                 % (alt.strip("/").replace("/articles/", ""),
                                    alt))
                else:
                    body.append("- [Alternate source](%s)" % alt)
            body.append("")
        tsection, has_transcript = transcript_section(slug, videos,
                                                     coverage)
        if has_transcript:
            front.append("transcript: true")
            body.append(tsection)
            n_transcripts += 1
        write_md(ARTICLES_DIR, slug + ".md", front, "\n".join(body))
    print(
        "articles: wrote %d (found=%d wayback_only=%d lost=%d transcripts=%d)"
        % (len(works), counts["found"], counts["wayback_only"],
           counts["lost"], n_transcripts)
    )
    # Statuses change only on >=200w local-file evidence, never by
    # grandfathering. Updated 2026-09-27 (Task 7 / I1): the WordPress-mirror
    # and IDI recoveries added 15 works and filled 2 stubs, so
    # found 30 -> 47, wayback_only 25 -> 24, lost 2 -> 1.
    assert counts == {"found": 47, "wayback_only": 24, "lost": 1}, counts
    assert sum(counts.values()) == len(works)

    n_mdi = build_mdi_pages()
    n_notices = build_notice_pages()
    print("articles: + %d mdi text pages, + %d notice records" % (n_mdi, n_notices))


def build_mdi_pages():
    """Item 5: store the 17 staged MDI texts as local pages.

    _data/mdi_articles.json stays at 17 rows; the recovered prose now lives in
    this repository instead of being a bare URL. Seven of the seventeen are
    <100-word captions for an embedded video and are kept as they are.
    """
    if not MDI_JSON.is_file():
        return 0
    rows = json.loads(MDI_JSON.read_text(encoding="utf-8"))
    assert len(rows) == 17, "expected 17 mdi rows, got %d" % len(rows)
    n = 0
    for row in rows:
        slug = str(row.get("slug") or "").strip()
        assert slug, "mdi row without slug: %r" % (row,)
        text = str(row.get("text") or "").replace("\r\n", "\n").strip("\n")
        assert text, "mdi row %s has no stored text" % slug
        words = len(text.split())
        assert words == int(row.get("words", words)), \
            "mdi row %s: stored text is %d w, metadata says %s" % (
                slug, words, row.get("words"))
        front = [
            "layout: article",
            "title: %s" % q(str(row.get("title", slug))),
            "slug: %s" % q("mdi-" + slug),
            "permalink: %s" % q("/articles/mdi/%s/" % slug),
            "status: %s" % q("mdi_text"),
            "collection: %s" % q("Muslim Debate Initiative"),
            "author: %s" % q(str(row.get("author", ""))),
            "publication_date: %s" % q(str(row.get("date", ""))),
            "original_url: %s" % q(str(row.get("url", ""))),
            "wayback_url: %s" % q(str(row.get("url", ""))),
            "words: %d" % words,
        ]
        counted = row.get("counted_as_work", True) is not False
        dup = row.get("duplicate_of")
        # N1 (re-review): the sentence must match the row's EVIDENCE CLASS.
        # A text-proven row may say "it is the same text"; a work-row-only row
        # may not, because its evidence says the identity is inferred. The
        # previous wording asserted identity unconditionally and contradicted the
        # evidence printed directly beneath it.
        klass = row.get("evidence_class") or (
            "counted" if counted else "text_proven")
        cont = row.get("containment")
        if counted:
            counting_line = (
                "This post is a distinct item of content: it is counted once, "
                "here. The measurement behind that verdict is printed below.")
        elif klass == "text_proven":
            counting_line = (
                "**This essay is also catalogued as a work and is not counted "
                "again.** It is the same text as the work `%s`, proved by "
                "comparison rather than by title: %.4f of this post's 5-grams "
                "are present in that work's local text." % (dup, cont))
        else:
            counting_line = (
                "**The work `%s` is catalogued, and this post is not counted "
                "again, because it is an announcement for the same piece of "
                "work.** That link is INFERRED, NOT PROVEN: the archive holds "
                "no local text for the work, so the two texts could not be "
                "compared. The text below is the only preserved copy of this "
                "announcement." % dup)
        body = [
            _h1(str(row.get("title", slug))),
            "",
            "*Muslim Debate Initiative - %s*" % str(row.get("date", "")),
            "",
            "Full text recovered from the Muslim Debate Initiative author archive "
            "on 2026-09-27 and preserved here verbatim (author id 16585639, "
            "byline verified as `Asadullah Ali`). Before this recovery the archive "
            "held only the URL and a summary.",
            "",
            counting_line,
            "",
        ]
        if dup:
            body += [
                "- [The counted work page]({{ \"/articles/%s/\" | relative_url }})"
                % dup,
                "",
            ]
        if not counted and row.get("duplicate_evidence"):
            body += ["> %s" % str(row["duplicate_evidence"]), ""]
        if counted and row.get("counted_as_work_evidence"):
            body += ["> %s" % str(row["counted_as_work_evidence"]), ""]
        if words < 100:
            body += [
                "> This post is shorter than 100 words: its substance is the embedded "
                "video, and the prose is the caption. It is kept exactly as published.",
                "",
            ]
        body += ["## Text", "", text, ""]
        write_md(ARTICLES_DIR, "mdi-%s.md" % slug, front, "\n".join(body))
        n += 1
    return n


def build_notice_pages():
    """Item 3 / R12: the 3 announcements. Recorded, never counted as works."""
    if not NOTICES_JSON.is_file():
        return 0
    rows = json.loads(NOTICES_JSON.read_text(encoding="utf-8"))
    n = 0
    for row in rows:
        slug = str(row.get("slug", "")).strip()
        title = str(row.get("title", slug))
        text = str(row.get("text", "")).strip()
        front = [
            "layout: article",
            "title: %s" % q(title),
            "slug: %s" % q("notice-" + slug),
            "permalink: %s" % q("/articles/notice/%s/" % slug),
            "date: %s" % q(str(row.get("date", ""))),
            "status: %s" % q("notice"),
            "counted_as_work: false",
            "words: %d" % int(row.get("words", 0)),
            "wayback_url: %s" % q(str(row.get("wayback_url", ""))),
            "original_url: %s" % q(str(row.get("original_url", ""))),
        ]
        body = [
            "# %s" % title,
            "",
            "*%s - status: notice*" % str(row.get("date", "")),
            "",
            "**This is an announcement, not a work.** It is recorded in "
            "`_data/notices.json` with `counted_as_work: false` and is deliberately "
            "excluded from the works count.",
            "",
            str(row.get("note", "")),
            "",
        ]
        if text:
            body += ["## Text", "", text, ""]
        write_md(ARTICLES_DIR, "notice-%s.md" % slug, front, "\n".join(body))
        n += 1
    return n


def main():
    build_papers()
    build_videos()
    build_articles()
    build_transcripts()
    print("done: _papers=20 _videos=%d _articles=%d(+17 mdi +3 notices)"
          % (len(json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))),
             len(json.loads(CANON_JSON.read_text(encoding="utf-8")))))
    drift = collection_drift()
    assert not drift, "collection/data drift:\n  " + "\n  ".join(drift)
    print("collection_drift: none (_videos, _papers, _articles, _transcripts, "
          "_posts all agree)")
    ids = video_id_agreement()
    assert not ids, "video-id disagreement:\n  " + "\n  ".join(ids)
    print("video_id_agreement: none (catalogue, coverage, captures, "
          "_videos/ and _transcripts/ all name the same id for each recording)")


if __name__ == "__main__":
    main()
