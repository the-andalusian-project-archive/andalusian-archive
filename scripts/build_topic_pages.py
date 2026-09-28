#!/usr/bin/env python3
"""Build the /topics/ layer from the verified cluster specs.

Reads `_data/topics/*.json` (whose every quote has been machine-verified by
scripts/test_quotes.py) and writes:

    _data/topics.json          the merged taxonomy, for anything that needs it whole
    _data/material_topics.json  material URL -> [topic id], so every page can
                                cross-link back to the questions it answers
    topics.md                  the /topics/ index
    topics/<id>.md             one page per cluster

DESIGN RULE - THE PAGE IS THE MATERIAL, NOT A SUMMARY OF IT. The substance of
each page is the author's own words, quoted and attributed, each tied to the
question it answers. The archive does not paraphrase him, and this generator
writes no prose of its own beyond structural labels. Anything the research
flagged as thin, contested, or unsafe to quote bare is carried through verbatim
from the agent's `notes` rather than being smoothed away.

Usage: python scripts/build_topic_pages.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from display_titles import clean_display_title, check_display_titles  # noqa: E402
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOPIC_DIR = ROOT / "_data" / "topics"
TODAY = date.today().isoformat()

BUCKETS = (
    ("head", "The broad questions"),
    ("mid", "Mid-tail questions"),
    ("long_tail", "Specific questions"),
    ("question_forms", "How people actually ask"),
    ("ai_phrased", "How people ask an assistant"),
)


def load_specs() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(TOPIC_DIR.glob("*.json"))]


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def slug_of(url: str) -> str:
    return url.strip("/").split("/")[-1] or "index"


def permalink_index() -> tuple[set[str], dict[str, str]]:
    """Every real permalink in the repository, and a last-segment -> permalink map.

    Built from source front matter rather than from `_site/`, so this script does
    not depend on a prior build having happened.

    It exists because the research agents transcribed URLs with `%20` for spaces,
    while the corpus permalinks carry literal spaces (`/articles/atheism/existence
    of god/...`). Left alone, those material rows point at pages that do not
    exist, the reverse index is keyed wrongly, and every back-link for the item
    silently disappears. Several rows also named a long historical path where the
    live page is a short one; the slug fallback below resolves those to the page
    that is actually built.
    """
    perma: set[str] = set()
    by_last: dict[str, list[str]] = {}
    for pattern in ("*.md", "*/*.md", "_articles/*.md", "_papers/*.md",
                    "_transcripts/*.md", "_videos/*.md", "series/*.md"):
        for md in sorted(ROOT.glob(pattern)):
            if "topics" in md.parts:
                continue
            try:
                head = md.read_text(encoding="utf-8", errors="replace")[:1200]
            except OSError:
                continue
            m = re.search(r"^permalink:\s*(\S+)\s*$", head, re.M)
            if not m:
                continue
            p = m.group(1).strip().strip('"\'')
            if not p.startswith("/"):
                continue
            perma.add(p)
            # A LIST, not a single winner. Seventy last-segments collide -
            # `understanding-atheism` is an article, a paper and a series page -
            # and the previous version kept whichever the filesystem returned
            # first, so the same spec row could resolve to a different page on a
            # different machine. resolve_url() picks from the list, by kind.
            by_last.setdefault(p.strip("/").split("/")[-1], []).append(p)
    return perma, by_last


# Which collection a resolved permalink should come from, given what the
# research agent said the item was. A `paper` must not land on the blog page of
# the same name.
KIND_PREFIX = {
    "work": ("/articles/",),
    "paper": ("/papers/",),
    "transcript": ("/transcripts/",),
    "video": ("/videos/",),
}


def resolve_url(url: str, perma: set[str], by_last: dict[str, list[str]],
                kind: str = "") -> tuple[str, str]:
    """Map a researched material URL onto a real permalink.

    Returns (permalink, how). `how` is exact | decoded | slug | missing, so the
    report can say how much of the index was guessed.
    """
    if url in perma:
        return url, "exact"
    decoded = urllib.parse.unquote(url)
    if decoded in perma:
        return decoded, "decoded"
    last = url.rstrip("/").split("/")[-1]
    options = by_last.get(last)
    if options:
        wanted = KIND_PREFIX.get(kind, ())
        for prefix in wanted:
            for opt in options:
                if opt.startswith(prefix):
                    return opt, "slug"
        # Deterministic: sorted, so the same input always yields the same page.
        return sorted(options)[0], "slug"
    return url, "missing"


def corpus_vocabulary() -> list[dict]:
    """Every addressable item in the corpus, with the text to match clusters against.

    The eight cluster specs are narrow by construction: each research agent read
    one subject and catalogued what they read. That is the right way to build the
    evidence on a page and the wrong way to build its shelf. A reader who arrives
    with a question about atheism wants every argument on atheism, including the
    ones no agent chose to quote from.

    Walked from the collection markdown rather than the JSON, because the JSON
    does not carry page URLs: `papers.json` has no `slug` and no permalink, and
    `videos.json` carries neither. The collection files are where the built route
    actually lives. Video `topics` and `themes` are joined in from `videos.json`
    by `video_id`, because that is the only place the corpus's own vocabulary
    lives and it is the reason this function can match on subject at all.
    """
    items: list[dict] = []
    seen: set[str] = set()

    videos_by_id: dict[str, dict] = {}
    for v in load("_data/videos.json"):
        videos_by_id[str(v.get("id", ""))] = v

    collections = (
        ("_articles", "work"),
        ("_papers", "paper"),
        ("_transcripts", "transcript"),
        ("_videos", "video"),
    )

    for directory, kind in collections:
        for md in sorted((ROOT / directory).glob("*.md")):
            head = md.read_text(encoding="utf-8", errors="replace")[:4000]
            fm = parse_front_matter(head)

            url = str(fm.get("permalink") or "").strip()
            if not url:
                continue
            title = str(fm.get("title") or md.stem)
            extra = [str(fm.get("slug") or "")]

            if kind == "video":
                vid = str(fm.get("video_id") or md.stem)
                row = videos_by_id.get(vid, {})
                extra += list(row.get("topics") or []) + list(row.get("themes") or [])

            if url in seen:
                continue
            seen.add(url)
            # The URL is deliberately NOT part of the haystack. It is a
            # path-encoded slug of the original WordPress hierarchy, so matching
            # terms against it produced false positives that no human would
            # predict: "west" matched a video whose URL contained "northwest".
            hay = " ".join([title] + [e for e in extra if e]).lower()
            items.append({"url": url, "kind": kind, "label": title, "hay": hay})

    return items


def parse_front_matter(head: str) -> dict:
    """Front matter as a dict, via PyYAML where possible.

    The previous implementation was a regex - `title:\\s*["']?([^"'\\n]+)` - and
    it broke on any title containing an escaped quote. Three titles in this
    corpus do, and the result was worse than a mangled string: one of them
    yielded a single backslash, so a shelf link rendered with the text `\\` where
    a work's title should be. `yaml.safe_load` handles the escaping because it
    is a YAML parser. The regex stays as a fallback so the generator still runs
    without PyYAML installed.
    """
    m = re.match(r"^---\r?\n(.*?)\r?\n---", head, re.S)
    if not m:
        return {}
    block = m.group(1)
    try:
        import yaml

        data = yaml.safe_load(block)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    out: dict = {}
    for line in block.splitlines():
        fm = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if not fm:
            continue
        key, val = fm.group(1), fm.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
        else:
            out[key] = val.strip("\"'")
    return out


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


# Why a link's words are a title and not a filename
# =============================================
# Every link on a topic page pointed at its target by the target's own storage
# name. `2017-12-22-the-atheistic-worldview-vs-the-quranic-worldview.md` is a
# filename, not a title, and a reader cannot tell from it which work they are
# about to read.
#
# The fix is not a lookup table. Both kinds of row that reach the renderer can
# name their target's own file, and the file's front matter carries the title
# the author or the channel gave it. So the resolver asks the source document
# rather than guessing from a slug.
#
# The failure mode that matters here is not an ugly label, it is a SILENT one.
# The original code was `item.get("slug", "source")`, and `corpus_vocabulary()`
# sets no `slug` key - so it rendered the literal word "source" for all 501
# citations, every one of them a link whose destination was correct and whose
# text was interchangeable. No test noticed, because the output was valid HTML
# and nothing was missing. `LABEL_FALLBACKS` records every row that has to
# reach a last resort, and `check_link_labels` fails the build on it, so this
# cannot recur quietly.
LABEL_FALLBACKS: list[str] = []
_TITLE_MAP: dict[str, str] | None = None


def title_map() -> dict[str, str]:
    """permalink -> title, from the corpus. Built once, lazily.

    Keyed on the permalink a row carries, so a cluster-spec row that was never
    in `corpus_vocabulary()` can still be named from the document itself.
    """
    global _TITLE_MAP
    if _TITLE_MAP is None:
        _TITLE_MAP = {}
        try:
            for it in corpus_vocabulary():
                url, lab = str(it.get("url") or ""), str(it.get("label") or "")
                if url and lab:
                    _TITLE_MAP[url] = lab
        except Exception:
            pass
    return _TITLE_MAP


def title_for(row: dict, by_url: dict[str, str] | None = None) -> str:
    """The human title for a link target, or the last resort, recorded."""
    for key in ("label", "title"):
        val = str(row.get(key) or "").strip()
        if val:
            return clean_display_title(val)

    # The row names the document it came from; that document knows its own
    # title. Prefer this over any slug-derived guess because it is the title as
    # published rather than as inferred.
    path = str(row.get("path") or "").strip()
    if path:
        md = ROOT / path
        if md.is_file():
            fm = parse_front_matter(md.read_text(encoding="utf-8", errors="replace")[:4000])
            val = str(fm.get("title") or "").strip()
            if val:
                return clean_display_title(val)

    url = str(row.get("url") or "").strip()
    table = by_url if by_url is not None else title_map()
    val = table.get(url, "").strip()
    if val:
        return clean_display_title(val)

    # A slug is still better than nothing, but it is a filename and the page
    # should say so rather than pretend. Recording it is what makes the gate
    # able to fail.
    slug = str(row.get("slug") or "").strip()
    who = slug or url or "?"
    LABEL_FALLBACKS.append(who)
    return slug or "source"


def check_link_labels() -> list[str]:
    """Every link must be named by something a reader can read."""
    fails = []
    for who in sorted(set(LABEL_FALLBACKS)):
        slugy = "-" in who or "_" in who or "/" in who or who.endswith(".md")
        fails.append(
            f"{'slug-like' if slugy else 'unnamed'} link label for {who!r}: "
            "no title on the row, in its file's front matter, or in the "
            "corpus title map"
        )
    return fails


def _term_pattern(term: str) -> re.Pattern:
    """Match a term from a word start, as a prefix.

    Plain substring matching put "Charlie Hebdo, Coexistence and Crocodile Tears"
    on the Foundational Questions page, because `existence` occurs inside
    `coexistence`. Adding a lookahead as well as a lookbehind fixed that and
    broke the corpus: the term `atheis` is a deliberate stem, and a trailing
    boundary means it no longer matches "Atheism" - 70 plainly relevant items,
    including the whole Understanding Atheism series, fell out of their subject
    pages and into miscellany.

    A lookbehind alone is the right rule. It refuses to start mid-word, so
    `existence` cannot match `coexistence` and `west` cannot match `northwest`,
    while `atheis` still matches `Atheism`, `atheist` and `atheistic` because
    nothing constrains where it stops. Suffix `!` demands a full-word match.
    """
    full = term.endswith("!")
    core = term.rstrip("!").rstrip("*")
    left = r"(?<![a-z0-9])"
    right = r"(?![a-z0-9])" if full else ""
    return re.compile(left + re.escape(core) + right, re.I)


def match_clusters(vocab: list[dict], relations: dict) -> dict[str, list[dict]]:
    """Assign every corpus item to every cluster it matches.

    `/topics/miscellany/` is then whatever no specific cluster claimed, so the
    nine pages partition the corpus without dropping or double-counting
    anything.
    """
    clusters = {cid: [] for cid in relations["clusters"]}
    claimed: set[str] = set()

    for cid, spec in relations["clusters"].items():
        if spec.get("is_fallback"):
            continue
        patterns = [_term_pattern(t) for t in (spec.get("terms") or []) if t]
        if not patterns:
            continue
        for item in vocab:
            if any(p.search(item["hay"]) for p in patterns):
                clusters[cid].append(item)
                claimed.add(item["url"])

    clusters["miscellany"] = [
        item for item in vocab if item["url"] not in claimed
    ]
    return clusters


_TIMESTAMP = re.compile(r"\[\d{1,2}:\d{2}\]")


def looks_transcribed(path: str) -> bool:
    """Does this source hold machine-captioned speech, whatever page type it is?

    The disclaimer used to be gated on `kind == "transcript"`, which is a PAGE
    type and not a CONTENT type. Four items quote embedded Whisper caption text
    while being typed `work` or `article` - 18 passages site-wide, 16 of them on
    the science cluster - and were published as clean quotations with no
    disclaimer, which made llms.txt's claim that transcripts are marked inline
    false. Two or more timestamp markers in the cited region is the signal.
    """
    target = ROOT / path
    if not target.exists():
        return False
    try:
        head = target.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return False
    return len(_TIMESTAMP.findall(head)) >= 2


def _labels() -> dict[str, str]:
    """Cluster id -> reader label, for the "also filed under" column."""
    out: dict[str, str] = {}
    for spec_path in sorted((ROOT / "_data" / "topics").glob("*.json")):
        try:
            s = json.loads(spec_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out[s.get("id", spec_path.stem)] = s.get("label", spec_path.stem)
    return out


LABEL_BY_ID = _labels()

KIND_NAMES = {
    "work": "Written works",
    "paper": "Papers",
    "video": "Recordings",
    "transcript": "Transcripts",
}


def render_shelf(shelf_out: list[dict]) -> str:
    """The "everything else on this subject" block, grouped by kind.

    A function, not inline code, because it is built once per cluster in the
    taxonomy loop and once per cluster in the page loop. Inlined it was computed
    in the first and consumed in the second, so every page got the shelf of
    whichever cluster happened to run last.
    """
    if not shelf_out:
        return ""
    by_kind: dict[str, list[dict]] = {}
    for m in shelf_out:
        by_kind.setdefault(m["kind"], []).append(m)
    sections = []
    for kind, rows in by_kind.items():
        lis = "\n".join(
            f'      <li><a href="{{{{ site.baseurl }}}}{r["url"]}">'
            f'{esc(r["title"])}</a></li>'
            for r in sorted(rows, key=lambda x: x["title"].lower())
        )
        sections.append(
            f"""<h3 class="shelf-kind">{esc(KIND_NAMES.get(kind, kind))} ({len(rows)})</h3>
<ul class="shelf-list">
{lis}
</ul>"""
        )
    # NOTE the indentation: this `return` sits AFTER the loop, not inside it.
    # Indented one level too deep it returned after the first kind group, so
    # every page showed one kind and the rest of the shelf silently vanished -
    # with the taxonomy still correct, which is what made it hard to see. The
    # page/taxonomy check in scripts/test_quotes.py is what caught it.
    return f"""
<h2>Everything else on this subject</h2>
<p>More from the archive on the same subject. A work can appear on more than one
of these pages.</p>
{''.join(sections)}
"""


SUBJECT = "Asadullah Ali Al-Andalusi"
# The other man. One word away from the subject, which is the whole reason the
# entity page exists, and the reason a quote from him must never be presented in
# this archive's quotation format as though the subject had said it.
CONFUSABLE = "abdullah al-andalusi"
THIRD_PARTY_MARKERS = (
    "this is a response by",
    "guest contributor",
)


def byline_of(path: str) -> str:
    """The byline a source post records, or "" if none is found.

    Read from the post body rather than the `author:` front-matter key, because
    three of these posts carry `author: "Asadullah Ali Al-Andalusi"` in front
    matter while the body byline says someone else entirely. The archive's own
    written rule is the opposite: a row counts as his on the strength of the
    BYLINE the publishing site records, never on the strength of a name in a
    title - and, as those three files show, never on the strength of a front
    matter key either.
    """
    target = ROOT / path
    if not target.exists():
        return ""
    try:
        head = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    # front matter is not evidence of authorship, so start looking after it
    body = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", head, count=1, flags=re.S)
    for line in body.splitlines()[:40]:
        s = line.strip()
        low = s.lower()
        if re.match(r"^(by|written by)\s+\S", s, re.I):
            return s
        for marker in THIRD_PARTY_MARKERS:
            if marker in low:
                return s
    return ""


def is_subject_authored(path: str) -> tuple[bool, str]:
    """(may this item be quoted as the subject's words?, why not)"""
    line = byline_of(path)
    if not line:
        return True, ""
    low = line.lower()
    if CONFUSABLE in low:
        return False, f"Not by the subject - the post is bylined '{line}'"
    if "as-sufi" in low or "as sufi" in low:
        return False, f"Not by the subject - bylined '{line}'"
    for marker in THIRD_PARTY_MARKERS:
        if marker in low:
            return False, f"Not the subject's own argument - the post says '{line}'"
    if "asadullah" in low:
        return True, ""
    return True, ""


def is_answer_quote(quote: str) -> bool:
    """Is this passage substantial enough to sit under a question heading?

    The brief was to stop the pages showing oversimplifications, and the earlier
    version of this filter failed at exactly that. It excluded bylines and quotes
    under 60 characters, and let through lines like "A two day lecture on the
    subject of atheism, atheists' beliefs, and common arguments and responses" -
    a page DESCRIPTION, hung under the heading "arguments against atheism", where
    it read as the answer. It is not an answer; it is a caption.

    A passage earns a question heading only if it is long enough to carry an
    argument. Short lines are not discarded - the corpus has real aphorisms in it
    - but a 35-character sentence cannot answer "why do atheists believe
    evolution disproves god", and presenting it as though it could is the failure
    this function exists to prevent. Those passages stay in the material table
    below, where they are legible and not mistaken for a reply.
    """
    q = quote.strip()
    if re.match(r"^(by |By )[A-Z]", q) and len(q) < 120:
        return False
    if re.match(r"^co-authors?\s*:", q, re.I):
        return False
    if re.match(r"^by\s", q, re.I) and "shaykh" in q.lower():
        return False
    if len(q) < 200:
        return False
    return True


_SOURCE_WORDS: dict[str, int] = {}


def source_words(path: str) -> int:
    """Word count of a source file, cached.

    Used to tell the reader how much of a work a quotation actually is. A
    passage presented without that number invites the reader to treat the
    excerpt as the argument; with it, they know they are reading a fragment of
    something three times longer, and the link to the whole is one click away.
    """
    if path not in _SOURCE_WORDS:
        target = ROOT / path
        try:
            _SOURCE_WORDS[path] = len(target.read_text(encoding="utf-8", errors="replace").split())
        except OSError:
            _SOURCE_WORDS[path] = 0
    return _SOURCE_WORDS[path]


def main() -> int:
    specs = load_specs()
    if not specs:
        print("no cluster specs found", flush=True)
        return 1

    perma, by_last = permalink_index()
    how_counts: dict[str, int] = {}

    # Broad, corpus-wide shelf per cluster, matched on the corpus's own metadata.
    relations = load("_data/topic_relations.json")
    vocab = corpus_vocabulary()
    matched = match_clusters(vocab, relations)

    # ---- merge + reverse index -------------------------------------------
    merged = {
        "title": "What this archive answers",
        "built": TODAY,
        "built_by": "scripts/build_topic_pages.py from _data/topics/*.json",
        "rule": (
            "A cluster is a body of questions the recovered material already "
            "answers. Clusters are not the archive's categories: the four A/B/C/D "
            "categories in taxonomy.json are about authorship, and this file is "
            "about subject matter. A work may appear in several clusters."
        ),
        "queries_counted": (
            "Query counts are computed from the buckets below at build time. No "
            "page may type a number."
        ),
        "clusters": [],
    }
    material_topics: dict[str, list[str]] = {}
    label_by_id: dict[str, str] = {}

    for spec in specs:
        cid = spec["id"]
        buckets = spec.get("queries") or {}
        n_queries = sum(len(buckets.get(b) or []) for b, _ in BUCKETS)
        n_claims = sum(
            len(item.get("key_claims") or []) for item in spec.get("material") or []
        )
        for item in spec.get("material") or []:
            raw_url = item.get("url")
            if not raw_url:
                continue
            url, how = resolve_url(raw_url, perma, by_last, item.get("kind", ""))
            how_counts[how] = how_counts.get(how, 0) + 1
            item["url"] = url
            material_topics.setdefault(url, [])
            if cid not in material_topics[url]:
                material_topics[url].append(cid)

        # Everything about this subject, from the corpus's own tags, not only
        # what the research agent happened to quote. Recorded separately so the
        # page can distinguish evidence it can prove from a shelf it is
        # asserting, and so the counts cannot be confused with one another.
        shelf = [m for m in matched.get(cid, []) if m["url"] not in
                 {i.get("url") for i in spec.get("material") or []}]
        shelf_out = [
            {"url": m["url"], "kind": m["kind"], "title": m["label"]} for m in shelf
        ]
        for m in shelf:
            material_topics.setdefault(m["url"], [])
            if cid not in material_topics[m["url"]]:
                material_topics[m["url"]].append(cid)

        shelf_md = render_shelf(shelf_out)

        merged["clusters"].append(
            {
                "id": cid,
                "label": spec.get("label", cid),
                "reader_question": spec.get("reader_question", ""),
                "one_line": spec.get("one_line", ""),
                "url": f"/topics/{cid}/",
                "material_count": len(spec.get("material") or []),
                "quote_count": n_claims,
                "shown_quote": sum(
                    1
                    for it in spec.get("material") or []
                    for c in it.get("key_claims") or []
                    if is_subject_authored(it.get("path", ""))[0]
                    and is_answer_quote(c.get("quote", ""))
                ),
                "query_count": n_queries,
                "shelf_count": len(shelf_out),
                "shelf": shelf_out,
                "bucket_counts": {b: len(buckets.get(b) or []) for b, _ in BUCKETS},
            }
        )

    # _data/topics.json is named topic_taxonomy.json on purpose. Jekyll keys
    # `site.data` on basename, so a FILE named topics.json and a DIRECTORY named
    # topics/ collide; the directory wins and `site.data.topics.clusters` is
    # silently undefined, which renders every back-link empty rather than failing.
    (ROOT / "_data" / "topic_taxonomy.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "_data" / "material_topics.json").write_text(
        json.dumps(material_topics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for spec in specs:
        label_by_id[spec["id"]] = spec.get("label", spec["id"])
    (ROOT / "_data" / "topic_labels.json").write_text(
        json.dumps(label_by_id, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("  material URL resolution: " + ", ".join(
        f"{k}={v}" for k, v in sorted(how_counts.items())))

    # ---- /topics/ index ---------------------------------------------------
    rows = "\n".join(
            f"""    <li class="topic-card">
      <h3><a href="{{{{ site.baseurl }}}}/topics/{c['id']}/">{esc(c['label'])}</a></h3>
      <p class="topic-q">{esc(c['reader_question'])}</p>
      <p class="topic-meta">{c['material_count']} items &middot; {c['shown_quote']} passages shown
        &middot; {c['shelf_count']} more on the subject &middot; {c['query_count']} questions</p>
    </li>"""
            for c in merged["clusters"]
        )
    total_q = sum(c["query_count"] for c in merged["clusters"])
    total_m = sum(c["material_count"] for c in merged["clusters"])

    index = f"""---
layout: default
title: Questions this archive answers
description: "The questions the recovered work of Asadullah Ali Al-Andalusi addresses, grouped by subject, with the passages that bear on each one and links to the full text."
permalink: /topics/
last_modified_at: {TODAY}
---

<h1>What this archive answers</h1>

<p class="lead">Most people arrive with a question, not a name. These are the
questions the recovered work addresses.</p>

<p>Each subject page puts a question in ordinary words, then gives the passages
that bear on it &mdash; quoted, attributed, and linked to the full text, paper,
transcript or recording. The archive records this work; it does not endorse it.</p>

<ul class="topic-list">
{rows}
</ul>

<h2>If a question is not here</h2>
<p>Search covers every item:
<a href="{{{{ site.baseurl }}}}/search/">search the archive</a>. Recovered items
that fit none of these subjects are still listed under
<a href="{{{{ site.baseurl }}}}/topics/miscellany/">other materials</a>, so
nothing recovered here is unreachable.</p>
"""
    (ROOT / "topics.md").write_text(index, encoding="utf-8")

    # ---- one page per cluster --------------------------------------------
    for spec in specs:
        cid = spec["id"]
        buckets = spec.get("queries") or {}
        material = spec.get("material") or []

        # The shelf must be recomputed HERE, in the loop that writes the page.
        # It is also computed in the loop above, which builds the taxonomy; that
        # copy is left over from whichever cluster ran last, so reusing the name
        # across the two loops silently put one subject's shelf on all eight
        # pages. Same variable, two loops - so it is recomputed, not shared.
        shelf = [m for m in matched.get(cid, []) if m["url"] not in
                 {i.get("url") for i in material}]
        shelf_out = [
            {"url": m["url"], "kind": m["kind"], "title": m["label"]} for m in shelf
        ]
        shelf_md = render_shelf(shelf_out)

        by_query: dict[str, list[tuple[dict, dict]]] = {}
        demoted = 0
        gated = 0
        for item in material:
            # The byline gate runs FIRST and is not satisfied by length. Three
            # posts in this corpus are bylined to other people while their front
            # matter claims the subject, and the 200-character floor below would
            # happily publish any of them at 250 characters.
            subject_ok, why = is_subject_authored(item.get("path", ""))
            item["not_by_subject"] = why or None
            if not subject_ok:
                gated += 1
                continue
            for claim in item.get("key_claims") or []:
                q = claim.get("supports", "").strip()
                if not q:
                    continue
                if not is_answer_quote(claim.get("quote", "")):
                    # Kept in the cluster and still machine-verified - it is
                    # provenance, not an answer - but not presented as a reply
                    # to a question. See is_answer_quote().
                    demoted += 1
                    continue
                by_query.setdefault(q, []).append((item, claim))

        # Two different numbers, because they are two different things. `n_claims`
        # is every machine-verified quotation in the cluster; `shown_quotes` is
        # how many actually appear on the page after the byline gate and the
        # substance floor. Publishing only the first overstated the evidence on
        # the index by 1.9x - a reader counting blockquotes got a different
        # answer from the one the page stated.
        shown_quotes = sum(len(v) for v in by_query.values())
        n_claims = sum(len(it.get("key_claims") or []) for it in material)

        query_order: list[str] = []
        for bucket, _ in BUCKETS:
            for q in buckets.get(bucket) or []:
                if q not in query_order:
                    query_order.append(q)

        # The question section: each query that has a passage, with that passage.
        blocks: list[str] = []
        rendered = 0
        for q in query_order:
            pairs = by_query.get(q)
            if not pairs:
                continue
            rendered += 1
            rows_md = []
            for item, claim in pairs[:3]:
                src = f"{item.get('kind', 'item')}"
                link = f"{{{{ site.baseurl }}}}{item.get('url', '')}"
                ref = claim.get("ref", "")
                whole = source_words(item.get("path", ""))
                shown = len(claim.get("quote", "").split())
                # Say out loud how big the thing we did not show you is. Without
                # this the excerpt reads as the argument, which is the one way a
                # faithful quotation can still mislead.
                if whole and whole > shown * 3:
                    size = (
                        f' &mdash; <span class="cite-size">excerpt of about {shown:,} '
                        f'words from a {whole:,}-word text. The argument around it is '
                        f'not on this page.</span>'
                    )
                else:
                    size = ""
                cite = f'<span class="cite-ref">{esc(ref)}</span>'
                rows_md.append(
                    f"""> {esc(claim['quote'])}
>
> &mdash; <a href="{link}">{esc(title_for(item))}</a> ({esc(src)}), cited at {cite}{size}"""
                )
                if item.get("kind") == "transcript" or looks_transcribed(item.get("path", "")):
                    rows_md.append(
                        ">\n> *This is a machine transcript. Accuracy is not "
                        "guaranteed and it should not be used in polemics or debate "
                        "material as an authoritative source.*"
                    )
            blocks.append(
                f"""<h3 class="question">{esc(q)}</h3>

{''.join(r + chr(10) + chr(10) for r in rows_md)}"""
            )

        unrendered = [q for q in query_order if q not in by_query]

        # A query with no substantial passage is not a gap to paper over. It goes
        # in the plain list below, where nothing promises it an answer, rather
        # than under a heading with a caption hung under it.
        unrendered_md = ""
        if unrendered:
            items_li = "\n".join(f"      <li>{esc(q)}</li>" for q in unrendered)
            unrendered_md = f"""
<h2>Related questions with nothing to quote here</h2>
<p>The archive holds material that bears on these, but not a long enough passage
to be worth putting under a question. They are listed so the gap is visible
rather than papered over; the reading list above is the place to go.</p>
<ul class="query-list">
{items_li}
</ul>
"""

        # HTML rows, not markdown pipe rows. Kramdown does not parse markdown
        # inside a raw HTML block, so the previous pipe rows shipped as literal
        # text that the browser then foster-parented OUT of the tbody - leaving
        # a header-only table and a run-on line of raw markdown above it, on all
        # eight subject pages.
        item_lines = []
        for it in material:
            others = [t for t in material_topics.get(it.get("url", ""), []) if t != cid]
            also = (
                " ".join(
                    f'<a href="{{{{ site.baseurl }}}}/topics/{t}/">'
                    f"{esc(LABEL_BY_ID.get(t, t))}</a>"
                    for t in others
                )
                if others
                else "&mdash;"
            )
            flag = it.get("not_by_subject")
            if flag:
                name_cell = f"{esc(it.get('kind',''))} &middot; <strong>not by the subject</strong>"
            else:
                name_cell = esc(it.get("kind", ""))
            item_lines.append(
                f'<tr><td><a href="{{{{ site.baseurl }}}}{it.get("url", "")}">'
                f'{esc(title_for(it))}</a></td>'
                f"<td>{name_cell}</td>"
                f"<td>{len(it.get('key_claims') or [])}</td>"
                f"<td>{also}</td></tr>"
            )
        item_rows = "\n".join(item_lines)
        gated_md = ""
        if gated:
            gated_md = f"""
<p class="note">This cluster also holds <strong>{gated}</strong> item(s) bylined to
other people &mdash; a guest contributor, or the other man also called
Al-Andalusi. Those are listed in the table for completeness and are
<strong>not quoted on this page</strong>: a quotation in this archive&rsquo;s format
reads as the subject&rsquo;s words, and for a byline one word away from his own that
is the most likely misattribution on the site. Follow the link to read them
with their own byline intact.</p>
"""

        # Reader-facing cautions, not the agents' research notes. The notes were
        # handoff memos to a maintainer - internal file paths, grep commands,
        # ALL-CAPS headings - and in three clusters they published the reason a
        # file was withheld together with the repository URL it was withheld
        # from, which is a pointer to the withheld document printed in the
        # document that withholds it. The full notes are kept at
        # docs/topic-research-notes.md. What a reader needs is here.
        rc = (load("_data/reader_cautions.json") or {}).get(cid) or {}
        caveat_items = rc.get("caveats") or []
        notes_md = ""
        if caveat_items:
            lis = "".join(f"<li>{esc(c)}</li>" for c in caveat_items)
            notes_md = (
                "\n<h2>What to know before you rely on this page</h2>\n"
                f'<ul class="caution-list">\n{lis}\n</ul>\n'
            )

        page = f"""---
layout: default
title: "{esc(spec.get('label', cid))}: the questions this material answers"
description: "{esc(spec.get('reader_question', ''))} The recovered work of Asadullah Ali Al-Andalusi that addresses it, quoted and linked."
permalink: /topics/{cid}/
last_modified_at: {TODAY}
---

<p class="crumb"><a href="{{{{ site.baseurl }}}}/topics/">What this archive answers</a> &rsaquo; {esc(spec.get('label', cid))}</p>

<h1>{esc(spec.get('label', cid))}</h1>

<p class="lead">{esc(spec.get('reader_question', ''))}</p>

<p>{esc(spec.get('one_line', ''))}</p>

<p class="note">The archive records this work. It does not endorse it, and it is not
a religious authority.</p>

<h2>Reading the passages below</h2>

<p><strong>None of these is the whole argument.</strong> Each passage is a
quotation from a longer work, and the link under it takes you to the whole thing
&mdash; the context, the qualifications and the objections, none of which fit in
an excerpt. Where a passage is a small part of a long work, the size of the whole
is given: a few sentences out of several thousand can make a position look
settled when the writer never settled it. If you intend to disagree with him, or
to cite him, read the full work first.</p>

<p>You do not have to arrive agreeing with him, or with anyone else. Where a
reading is contested, a position is his alone, or the evidence is thin, that is
said at the foot of the page.</p>

<h2>Where he addresses the question</h2>

{chr(10).join(blocks) if blocks else '<p>No quoted passage in this cluster yet.</p>'}
{unrendered_md}
{shelf_md}
<h2>Everything in this cluster</h2>

<table class="data-table">
<thead><tr><th>Item</th><th>Kind</th><th>Quoted passages</th><th>Also filed under</th></tr></thead>
<tbody>
{item_rows}
</tbody>
</table>

<p class="meta">{len(material)} items &middot; {rendered} of {len(query_order)} mapped questions carry a quoted passage
&middot; {shown_quotes} of {n_claims} verified passages shown
&middot; {gated} bylined to other people and not quoted here.</p>
{gated_md}{notes_md}"""
        (ROOT / "topics").mkdir(exist_ok=True)
        (ROOT / "topics" / f"{cid}.md").write_text(page, encoding="utf-8")

        # (shown_quotes is computed just above, next to the byline gate)
        print(
            f"  {cid:24s} material={len(material):3d} "
            f"questions={len(query_order):4d} rendered={rendered:4d} "
            f"unrendered={len(unrendered):3d} shelf={len(shelf_out):3d} "
            f"quotes={shown_quotes:3d}/{n_claims:3d} demoted={demoted:2d} "
            f"bylined-elsewhere={gated}"
        )

    # ---- /topics/miscellany/ ---------------------------------------------
    # The remainder. A page of leftovers is honest; an invisible orphan is not.
    # A work that fits no cluster still has to be findable, or the eight subject
    # pages are quietly lossy and the archive is lying about its own coverage.
    leftovers = matched.get("miscellany", [])
    kind_names = {
        "work": "Written works", "paper": "Papers",
        "video": "Recordings", "transcript": "Transcripts",
    }
    by_kind: dict[str, list[dict]] = {}
    for m in leftovers:
        by_kind.setdefault(m["kind"], []).append(m)

    sections = []
    for kind, rows in sorted(by_kind.items()):
        lis = "\n".join(
            f'      <li><a href="{{{{ site.baseurl }}}}{r["url"]}">'
            f'{esc(r["label"])}</a></li>'
            for r in sorted(rows, key=lambda x: x["label"].lower())
        )
        sections.append(
            f"""<h2>{esc(kind_names.get(kind, kind))} ({len(rows)})</h2>
<ul class="shelf-list">
{lis}
</ul>"""
        )

    misc = f"""---
layout: default
title: "Other materials: everything not yet filed under a subject"
description: "Recovered works in this archive that do not fit the eight subject pages, listed so that nothing recovered here becomes unreachable."
permalink: /topics/miscellany/
last_modified_at: {TODAY}
---

<p class="crumb"><a href="{{{{ site.baseurl }}}}/topics/">What this archive answers</a> &rsaquo; Other materials</p>

<h1>Other materials</h1>

<p class="lead">Everything recovered here that does not yet fit one of the eight
subjects.</p>

<p>This page exists so the other eight do not have to pretend to be complete. A
recovered work that belongs to no subject is still a recovered work, and leaving
it off the subject pages would mean they quietly did not hold everything they
claim to.</p>

<p>Some of this is a limit of the original site's own tagging, which is thin and
uneven, rather than a gap in the recovery. Where a work plainly belongs to a
subject it may still appear on that page.</p>

{''.join(sections) if sections else '<p>Nothing is left over: every recovered item is filed under at least one subject.</p>'}
"""
    (ROOT / "topics" / "miscellany.md").write_text(misc, encoding="utf-8")
    print(f"  {'miscellany':24s} leftover items={len(leftovers)}")

    print("\nwrote _data/topic_taxonomy.json, _data/material_topics.json, "
          "topics.md, topics/*.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
