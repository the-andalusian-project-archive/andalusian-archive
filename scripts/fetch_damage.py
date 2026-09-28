"""Damage introduced by fetching, as distinct from the author's own prose.

THE LINE THIS MODULE HOLDS
==========================
A recovery pipeline can damage text two ways, and only one is this module's
business.

  fetch damage  Something the FETCHER did. An ad-injection payload left in the
                body, WordPress chrome, a space destroyed when an inline tag was
                stripped. The author never wrote any of it. Removing it restores
                his text; it does not alter it.

  his text      His punctuation, his typos, his quote style. This stays, even
                where it reads as an error. `2017;` is not ours to fix.

`CONTRIBUTING.md` puts it as "corrections to the record, not changes to the
recovered material", and this file is that sentence in executable form. The
repair pass and the build gate both import the table below so they cannot drift
apart.

WHY THE RULES ARE STRUCTURAL, NOT KEYWORDS
===========================================
The first version of this matched ad payload by keyword and reported six
transcripts and two articles as contaminated. Every one was a false positive,
and every one was the author's own speech:

    "function you know I have to take a lot of things in order for me to"
    "document this is this is what you believe so"
    "even sponsored some of her videos on his own channel"

A rule that fires on what a man said while lecturing is worse than no rule at
all. So the residue rules below match SHAPE - a contiguous run of `key: value`
lines terminated by `});` - which is what an injected ad configuration actually
is, and which prose does not have. Every rule also carries an `allow` pattern
for a legitimate lookalike, because a rule with no lookalike exemption has not
been thought about.

CLASSES
=======
  residue, chrome   Unambiguous fetch damage. A gate FAILS on these.
  join, space,      Judgement calls. REPORTED for per-hit triage, never
  encoding           auto-rewritten and never gate-failing. Rewriting these
                    mechanically is how a preservation archive starts editing its
                    author.
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Collections of recovered material that a fetcher wrote.
RECOVERED_DIRS = ("_posts", "_articles", "_papers", "_transcripts", "_videos")

#: Classes where a mechanical repair is safe: the text was never the author's.
AUTOMATIC = frozenset({"residue", "chrome"})


@dataclass(frozen=True)
class Rule:
    """One damage pattern, and what may be done about it."""

    name: str
    cls: str
    pattern: re.Pattern[str]
    #: A legitimate lookalike that must NOT fire. No rule ships without one.
    allow: re.Pattern[str] | None = None
    #: A second pattern that must ALSO match the SAME span. A lookahead cannot
    #: express "this run contains an ad key" when the key may be on the first
    #: line of the run rather than after it, and getting that wrong makes the
    #: LAST ad block in every file invisible - to the repair and to the gate
    #: alike, which is the worst kind of bug: the two agree, and both are wrong.
    requires: re.Pattern[str] | None = None
    note: str = ""

    @property
    def automatic(self) -> bool:
        return self.cls in AUTOMATIC

    def find_all(self, text: str) -> list[re.Match[str]]:
        """Every match that also satisfies `requires` and clears `allow`."""
        out: list[re.Match[str]] = []
        for m in self.pattern.finditer(text):
            if self.requires and not self.requires.search(m.group(0)):
                continue
            if self.allow and self.allow.search(m.group(0)):
                continue
            out.append(m)
        return out


@dataclass
class Hit:
    rule: str
    cls: str
    line: int
    text: str
    automatic: bool


# --------------------------------------------------------------------------
# residue - injected script and markup. Structural, never keyword.
# --------------------------------------------------------------------------

#: One line of injected ad configuration: the whole line is `key: value`, plus
#: indentation. Prose is not shaped like this. Earlier rules tried to capture
#: multi-line runs with a single regex and had to be widened three times: a
#: 2-line run, a blank line between terminators, and a multi-word category in
#: the taxonomy block each defeated it. Classifying one line at a time removes
#: the run-shape problem entirely - a config line is either that or it is not.
_AD_CONFIG_LINE = re.compile(
    r"^[ \t]*[A-Za-z_$][\w$]*[ \t]*:[ \t]*(?:'[^']*'|\"[^\"]*\"|\d+)[ \t]*,?[ \t]*$")
#: An orphaned JavaScript terminator, alone on its line.
_JS_TERMINATOR = re.compile(r"^[ \t]*\}[ \t]*\)*[ \t]*;?[ \t]*$")
_AD_KEYS = ("collapseEmpty", "sectionId", "insertAt", "adUnit", "writeAd", "adSlot")

#: How far either side of a terminator a config line still counts as part of the
#: same injected block. The real files put blank lines between the blocks.
_TERMINATOR_NEIGHBOURHOOD = 3


def _config_run_lines(lines: list[str]) -> set[int]:
    """0-based indexes of lines that are injected ad configuration.

    A line qualifies when it is config-shaped AND either
      (a) a config line within two lines of another config line, or
      (b) a config line within _TERMINATOR_NEIGHBOURHOOD of a `});` line.

    Requiring company is what keeps this safe: a lone `width: 300,` in prose is
    not damage, and prose does not come with a `});` on the next line either.
    """
    config = {i for i, ln in enumerate(lines) if _AD_CONFIG_LINE.match(ln)}
    terms = {i for i, ln in enumerate(lines) if _JS_TERMINATOR.match(ln)}
    out: set[int] = set()
    for i in config:
        near_config = any(
            j in config and abs(i - j) <= 2 for j in config if j != i)
        near_term = any(abs(i - t) <= _TERMINATOR_NEIGHBOURHOOD for t in terms)
        if near_config or near_term:
            out.add(i)
    return out


def _terminator_lines(lines: list[str]) -> set[int]:
    """0-based indexes of orphaned `});` lines. In the body of a recovered
    article these only ever come from an injected script; nothing this archive
    writes emits one, and a code block is blanked before this runs."""
    return {i for i, ln in enumerate(lines) if _JS_TERMINATOR.match(ln)}


# --------------------------------------------------------------------------
# A rule that cannot see the damage it exists to find
# ========================================================================
# The 2026-09-29 repair pass removed the `});` terminators from the Orientalists
# Fables post. `ad-payload-block` qualified a config line partly by its
# proximity to a terminator, so the repair deleted the evidence the rule keys on
# and the nine surviving lines of the injected `wpmrec2x` stylesheet became
# permanently invisible. The gate reported 0 on a file that still carried a
# stylesheet and a truncated script.
#
# The lesson generalises: a detector must not depend on a token that the repair
# is going to delete. So these two classifiers key on the CONTENT of a line
# instead, and neither mentions a terminator.
#
# The block they catch, for the record, is not a `key: value` config run at all.
# It is CSS (`div.wpmrec2x{max-width:610px;}`) and JavaScript
# (`p.style.setProperty('display', 'none', 'important');`), which is why
# _AD_CONFIG_LINE never matched any of it.

#: A whole-line CSS rule: a selector, a brace, declarations, a closing brace.
_CSS_RULE_LINE = re.compile(
    r"^[ \t]*[.#]?[A-Za-z][\w.#\s,>+~*\[\]=\"'-]*\{[^{}]*:[^{}]*;?[ \t]*\}[ \t]*$")
#: A whole-line JavaScript statement. Anchored at the start so that a sentence
#: containing the word "return" mid-line is not a match.
_JS_STATEMENT_LINE = re.compile(
    r"^[ \t]*(?:var|let|const|if|else|for|while|return|function|window|document)\b"
    r".*[;{][ \t]*$")
#: A method call that only ever appears in script: `x.setProperty(...)`, `y.f(...)`.
_JS_CALL_LINE = re.compile(r"^[ \t]*[\w.]+\.[A-Za-z_$][\w$]*\([^()]*\)[ \t]*;?[ \t]*$")
#: A bare JS block opener left over from a truncated paste: `} else {`, `}) {`.
_JS_BLOCK_OPENER = re.compile(r"^[ \t]*\}[ \t]*(?:else[ \t]*)?\{[ \t]*$")

#: Two script-shaped lines close together are an injected script. One on its own
#: is not enough to act on: a single `var x = 1;` line could be someone's
#: example. Prose is never shaped like this either way, but the run requirement
#: is what makes the rule safe to make automatic.
_SCRIPT_RUN_MIN = 2
_SCRIPT_RUN_GAP = 12


def _script_run_lines(lines: list[str]) -> set[int]:
    """0-based indexes of an injected CSS/JavaScript block."""
    def shaped(ln: str) -> bool:
        return bool(
            _CSS_RULE_LINE.match(ln)
            or _JS_STATEMENT_LINE.match(ln)
            or _JS_CALL_LINE.match(ln)
            or _JS_BLOCK_OPENER.match(ln)
        )

    shaped_idx = [i for i, ln in enumerate(lines) if shaped(ln)]
    if not shaped_idx:
        return set()
    out: set[int] = set()
    # Any cluster of >=2 shaped lines within _SCRIPT_RUN_GAP is one injected
    # block; absorb the un-shaped lines that sit between them so the whole
    # fragment goes rather than leaving `var p = o.parentNode;` behind.
    cluster: list[int] = [shaped_idx[0]]
    for i in shaped_idx[1:]:
        if i - cluster[-1] <= _SCRIPT_RUN_GAP:
            cluster.append(i)
        else:
            if len(cluster) >= _SCRIPT_RUN_MIN:
                out.update(range(cluster[0], cluster[-1] + 1))
            cluster = [i]
    if len(cluster) >= _SCRIPT_RUN_MIN:
        out.update(range(cluster[0], cluster[-1] + 1))
    return {i for i in out if i < len(lines) and lines[i].strip()}


# --------------------------------------------------------------------------
# Comment threads: third-party blog commentary inside his essay
# --------------------------------------------------------------------------
# The 2026-09-29 pass removed the `1 Comment` count and the
# `### One Comment on "..."` heading. It did not remove the comment BODIES,
# because no rule matched them, and the recovery log then said the threads had
# been "removed in full". They had not. 77 hits of somebody else's commentary
# were still sitting inside eleven posts.
#
# A WordPress comment list arrives flattened: the name, the date and the text
# are run together with no markup between them, so a comment reads
#   - GameBotX12 Aug 2018Great article, you explained it in a clear way.Reply...
# The date-run and the glued `Reply` are what make that distinguishable from a
# list item the author wrote, and requiring BOTH the bullet and a date-run
# keeps the rule off ordinary prose lists.

_MONTHS = ("Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February"
           "|March|April|June|July|August|September|October|November|December")
#: `<name><day><month><year>` - the name is not matched, only the date glued to
#: text on both sides, which is what a flattened comment list looks like.
_COMMENT_DATE_RUN = re.compile(rf"\d{{1,2}}\s+(?:{_MONTHS})\s+20\d\d")
#: The heading WordPress puts above the thread.
_COMMENT_HEADING = re.compile(
    r"^[ \t]{0,3}#{2,6}[ \t]*(?:(?:\d+|One|No|Be the first)[ \t]+)?"
    r"Comments?(?:[ \t]+on\b|[ \t]*$)",
    re.IGNORECASE)


def _is_comment_body(ln: str) -> bool:
    """A flattened WordPress comment: a bullet with a name-date-text run."""
    return bool(
        re.match(r"^[ \t]*[-*+][ \t]+", ln) and _COMMENT_DATE_RUN.search(ln)
    )


def _comment_thread_lines(lines: list[str]) -> set[int]:
    """0-based indexes of a comment heading and the flattened comment bodies.

    Two entry points, because the 2026-09-29 pass removed the `1 Comment` count
    and the `### One Comment on "..."` heading from some posts and left the
    bodies behind: four comment lists are now orphaned, with no heading above
    them, and a heading-led scan misses all four.

    Heading-led scanning still stops at the first non-blank line that is neither
    a bullet nor continued comment text, so a heading followed by ordinary prose
    is left alone and only a real thread is taken. The standalone case is the
    date-run bullet on its own, which is specific enough to act on: a list item
    the author wrote does not have a person's name welded to `10 Mar 2012` and
    continue straight into a sentence.
    """
    out: set[int] = set()
    for i, ln in enumerate(lines):
        if not _COMMENT_HEADING.match(ln):
            continue
        out.add(i)
        j = i + 1
        blanks = 0
        while j < len(lines):
            body = lines[j]
            if not body.strip():
                blanks += 1
                if blanks > 1:
                    break
                j += 1
                continue
            if _COMMENT_HEADING.match(body) or _is_comment_body(body):
                out.add(j)
                j += 1
                continue
            break
    # Orphaned bodies: the heading was removed by an earlier pass.
    for i, ln in enumerate(lines):
        if i not in out and _is_comment_body(ln):
            out.add(i)
    return out


RESIDUE_RULES = (
    Rule(
        name="ad-payload-block",
        cls="residue",
        # Filled in by scan_text / repair_text from the line classifier, because
        # a multi-line regex is what made this rule wrong three times.
        pattern=re.compile(r"(?!)"),
        note="injected ad configuration left in the body",
    ),
    Rule(
        name="js-terminator-run",
        cls="residue",
        pattern=re.compile(r"(?!)"),
        note="orphaned JavaScript terminators",
    ),
    Rule(
        name="injected-script-run",
        cls="residue",
        pattern=re.compile(r"(?!)"),
        note="injected CSS/JavaScript: an ad widget's stylesheet and script, "
             "which is not `key: value` config and was invisible to "
             "ad-payload-block",
    ),
    Rule(
        name="comment-thread",
        cls="residue",
        pattern=re.compile(r"(?!)"),
        note="a WordPress comment thread: third-party commentary, not his essay",
    ),
    Rule(
        name="html-comment",
        cls="residue",
        pattern=re.compile(r"<!--.*?-->", re.S),
        note="HTML comment surviving into prose",
    ),
    Rule(
        name="markup-tag",
        cls="residue",
        pattern=re.compile(
            r"</?(?:p|br|div|span|strong|em|ul|ol|li|blockquote|script|style)\b[^>]*>",
            re.I,
        ),
        # Deliberate markup is not damage. `<span class="tall-glyph">` is
        # written by this archive to size U+29F8, and the first version of this
        # rule flagged all twelve of them as residue - six in _videos and six in
        # _transcripts, which is how two clean collections acquired a
        # contamination report. A tag carrying a class is one this repository
        # chose to write; an unclassed <p> or <br> is markup that fell through
        # from the source page.
        allow=re.compile(r'<(?:span|a|em|strong)\b[^>]*\bclass\s*=', re.I),
        note="inline tag surviving into prose",
    ),
    Rule(
        name="embed-tag",
        cls="residue",
        pattern=re.compile(r"<\s*(?:iframe|embed|object)\b", re.I),
        note="iframe/embed surviving into prose",
    ),
)

# --------------------------------------------------------------------------
# chrome - WordPress furniture. Removed, because the post body is not the post.
# --------------------------------------------------------------------------

CHROME_RULES = (
    Rule(
        name="posted-on-byline",
        cls="chrome",
        # `Posted on December 22, 2017ByAsadullah Ali` - a byline whose date and
        # author were joined when the span tags between them were stripped.
        pattern=re.compile(r"Posted on \w+ \d{1,2}, \d{4}By[A-Z]"),
        note="byline with the tag-strip join still in it",
    ),
    Rule(
        name="category-tags-runon",
        cls="chrome",
        # Matched to the end of the line, not to a list of single words: the real
        # line is `Category:Atheism,Current Issues,existence of god,fitrah,...`
        # and an earlier version that allowed one word per category stopped at the
        # space in "Current Issues" and left the whole block in place.
        #
        # `Tags:` is optional because a post with exactly one category and no
        # tags prints `Category:iKhalifa` on its own, which is the same block
        # with less in it. Requiring both left that one in a post body, and the
        # line is furniture either way.
        pattern=re.compile(
            r"(?m)^[ \t]*Category:[^\n]*?(?:Tags:[^\n]*)?$\n?"),
        allow=re.compile(r"^\s*(?:I|We)\s", re.I),
        note="taxonomy block in the body",
    ),
    Rule(
        name="comment-count",
        cls="chrome",
        pattern=re.compile(r"^\s*\d+\s+Comments?\s*$", re.M),
        note="comment count in the body",
    ),
    Rule(
        name="one-comment-on",
        cls="chrome",
        pattern=re.compile(r"^#{1,6}\s*One Comment on\b.*$", re.M),
        note="comment-thread heading in the body",
    ),
    Rule(
        name="pingback-line",
        cls="chrome",
        pattern=re.compile(r"^-\s*Pingback:.*$", re.M),
        note="pingback list in the body",
    ),
    Rule(
        name="comment-prompt",
        cls="chrome",
        pattern=re.compile(
            r"(?m)^[ \t]*(?:Share this|Related Posts|Leave a comment|"
            r"Posted in|Tags:|Categories:)\b.*$"
        ),
        note="theme comment/share furniture",
    ),
)

# --------------------------------------------------------------------------
# judgement classes - reported, never rewritten, never gate-failing
# --------------------------------------------------------------------------

JUDGEMENT_RULES = (
    Rule(
        name="tag-strip-join-lower-upper",
        cls="join",
        # `2017ByAsadullah`: two words that shared an inline element. Genuine
        # when it is a year, a number or a known name; not when it is camelCase.
        pattern=re.compile(r"\b(?:\d{4}|[a-z]{2,})[A-Z][a-z]{2,}"),
        allow=re.compile(
            r"(?:eBay|iPhone|YouTube|WhatsApp|Islamic|JavaScript|LinkedIn|"
            r"GitHub|WordPress|iJihad|MacBook|WebArchive|Internet)", re.I),
        note="a space may have been destroyed by tag-stripping",
    ),
    Rule(
        name="tag-strip-join-full-stop",
        cls="join",
        pattern=re.compile(r"\b[a-z]{3}\.[A-Z][a-z]{2,}"),
        allow=re.compile(r"(?:U\.S|U\.K|etc)\b"),
        note="sentence boundary may have lost its space",
    ),
    Rule(
        name="space-before-punctuation",
        cls="space",
        pattern=re.compile(r"[ \t]+[,.;:!?]"),
        note="space before punctuation",
    ),
    Rule(
        name="no-space-after-stop",
        cls="space",
        pattern=re.compile(r"(?<=[a-z]{3})\.(?=[A-Z][a-z])"),
        allow=re.compile(r"(?:U\.S|U\.K|No\.|vs\.)"),
        note="missing space after a full stop",
    ),
    Rule(
        name="tab-character",
        cls="space",
        pattern=re.compile(r"\t"),
        note="tab left by the fetcher",
    ),
    Rule(
        name="trailing-space",
        cls="space",
        pattern=re.compile(r"(?m)[ \t]+$"),
        note="trailing whitespace",
    ),
    Rule(
        name="html-entity",
        cls="encoding",
        pattern=re.compile(
            r"&(?:amp|lt|gt|quot|apos|nbsp|rsquo|lsquo|ldquo|rdquo|mdash|ndash|"
            r"hellip|#[0-9]{2,5});"
        ),
        note="undecoded HTML entity",
    ),
    Rule(
        name="mojibake",
        cls="encoding",
        pattern=re.compile(r"(?:\u00c3[\u0080-\u00bf]|\u00e2\u0080|\u00c2\u00a0)"),
        note="double-decoded UTF-8",
    ),
)

ALL_RULES = RESIDUE_RULES + CHROME_RULES + JUDGEMENT_RULES


# --------------------------------------------------------------------------
# scanning
# --------------------------------------------------------------------------

#: Markup this repository writes itself, removed before scanning.
#:
#: Damage is what the FETCHER left behind. Anything this archive deliberately
#: emits is not damage, and the cheapest way to stop a rule firing on it is to
#: take it out of the text first - per-rule allowlists handle an opening tag and
#: miss its closing partner, which is how six `<span class="tall-glyph">` and
#: six `</span>` were reported as residue across _videos and _transcripts, two
#: collections that are in fact clean. The inner text is preserved; only the
#: tag is removed, so line and word counts do not move.
#:
#: `tall-glyph` sizes U+29F8, the author's "w/" for "with", which inks 2.67x cap
#: height and overflows its line unless it is scaled.
DELIBERATE_MARKUP = (
    re.compile(r'<span\b[^>]*\bclass\s*=\s*["\'][^"\']*tall-glyph["\'][^>]*>'
               r'(.*?)</span>', re.S),
)


def strip_deliberate(text: str) -> str:
    """Remove markup this archive authored, keeping the text it wraps."""
    for pattern in DELIBERATE_MARKUP:
        text = pattern.sub(r"\1", text)
    return text


def _strip_fenced_code(text: str) -> str:
    """Blank out fenced code so its contents are never read as prose.

    A transcript that discusses code legitimately contains `});`. So does an
    injected script. The difference is the fence, and the fence is the only
    reliable signal that a human meant it.
    """
    return re.sub(r"(?ms)^(```|~~~).*?^\1[ \t]*$", lambda m: "\n" * m.group(0).count("\n"), text)


def _front_matter_end(text: str) -> int:
    """Offset just past the closing `---` of front matter, or 0."""
    if not text.startswith("---"):
        return 0
    close = text.find("\n---", 3)
    return close + 4 if close != -1 else 0


def scan_text(text: str, *, judgement: bool = True) -> list[Hit]:
    """Every rule hit in `text`, in line order."""
    body_start = _front_matter_end(text)
    head, body = text[:body_start], text[body_start:]
    scannable = _strip_fenced_code(strip_deliberate(body))
    lines = scannable.split("\n")
    offset = head.count("\n")

    hits: list[Hit] = []
    for rule in ALL_RULES:
        if rule.pattern.pattern == "(?!)":
            # A rule whose pattern is supplied by the line classifier.
            if rule.name == "ad-payload-block":
                indexes = sorted(_config_run_lines(lines))
                snippet_of = lambda i: lines[i].strip()
            elif rule.name == "js-terminator-run":
                indexes = sorted(_terminator_lines(lines))
                snippet_of = lambda i: lines[i].strip()
            elif rule.name == "injected-script-run":
                indexes = sorted(_script_run_lines(lines))
                snippet_of = lambda i: lines[i].strip()
            elif rule.name == "comment-thread":
                indexes = sorted(_comment_thread_lines(lines))
                snippet_of = lambda i: lines[i].strip()
            else:  # pragma: no cover - guards a new classifier-less rule
                indexes, snippet_of = [], (lambda i: "")
            for i in indexes:
                hits.append(
                    Hit(rule=rule.name, cls=rule.cls, line=offset + i + 1,
                        text=snippet_of(i)[:120], automatic=rule.automatic)
                )
            continue
        # find_all applies the rule's `requires` and `allow` together, so the
        # scanner and the repair below can never disagree about what is a hit.
        for m in rule.find_all(scannable):
            snippet = m.group(0).strip()
            if not snippet:
                continue
            hits.append(
                Hit(
                    rule=rule.name,
                    cls=rule.cls,
                    line=offset + scannable.count("\n", 0, m.start()) + 1,
                    text=snippet.replace("\n", " ")[:120],
                    automatic=rule.automatic,
                )
            )
    hits.sort(key=lambda h: (h.line, h.rule))
    return hits


def scan_file(path: pathlib.Path, *, judgement: bool = True) -> list[Hit]:
    return scan_text(path.read_text(encoding="utf-8", errors="replace"),
                     judgement=judgement)


def scan_collections(dirs=RECOVERED_DIRS, *, judgement: bool = True):
    """Yield (path, hits) for every recovered file that has any hit."""
    for d in dirs:
        base = ROOT / d
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            hits = scan_file(path, judgement=judgement)
            if hits:
                yield path, hits


def summary(paths_and_hits) -> tuple[dict[str, int], dict[str, int]]:
    """(counts by class, counts by rule) for a scan."""
    by_class: dict[str, int] = {}
    by_rule: dict[str, int] = {}
    for _, hits in paths_and_hits:
        for h in hits:
            by_class[h.cls] = by_class.get(h.cls, 0) + 1
            by_rule[h.rule] = by_rule.get(h.rule, 0) + 1
    return by_class, by_rule


# --------------------------------------------------------------------------
# repair
# --------------------------------------------------------------------------

#: What each repair removes, and why it is not the author's text.
#:
#: Every entry has to be defensible as "the fetcher did this", never as "this
#: reads badly". Two decisions are recorded here rather than left implicit:
#:
#: - The byline and the Category/Tags block are removed because the same values
#:   are already in front matter, so nothing is lost. The byline also carries the
#:   tag-strip join ("2017ByAsadullah"), which is the damage this whole exercise
#:   is about.
#:
#: - WordPress comment threads are removed, heading and body alike. They are
#:   third-party blog comments: not the author's work, and not sources this
#:   archive claims to hold. The archive keeps third-party *sources* in
#:   /sources/; a comment under a post is neither. This is a decision, not a
#: repair, so it is in the log for every file it touches.
#:
#: How each automatic rule is removed. The PATTERN is not repeated here - it
#: comes from the Rule itself, so the repair and the detector cannot drift apart.
#: An earlier version of this table carried its own copy of the ad pattern while
#: the Rule had been fixed, so the repair kept removing what the gate had
#: stopped seeing, and the two agreed about a file that was still damaged.
#:
#:   lines  the match covers whole lines; remove them
#:   line   remove the line the match starts on (furniture, always alone)
#:   inline remove just the matched span, keeping the line
#:
#: "inline" is the one that protects his prose: `<!--more-->` and a stray `<br>`
#: sit inside lines that also contain sentences, and a line-mode removal would
#: take the sentences with them.
REPAIR_MODE = {
    "ad-payload-block": "lines",
    "js-terminator-run": "lines",
    "injected-script-run": "lines",
    "comment-thread": "lines",
    "markup-tag": "inline",
    "html-comment": "inline",
    "posted-on-byline": "line",
    "comment-count": "line",
    "category-tags-runon": "line",
    "one-comment-on": "line",
    "pingback-line": "line",
}

#: Applied only when asked for explicitly, never by the gate.
ENCODING_REPAIRS: tuple[tuple[str, str, re.Pattern[str], str | None], ...] = (
    ("html-entity", "encoding", re.compile(r"&nbsp;", re.I), " "),
    ("html-entity-others", "encoding",
     re.compile(r"&(?:amp|lt|gt|quot|rsquo|lsquo|ldquo|rdquo|mdash|ndash|hellip);"),
     None),  # decoded through the html entity table
)

_RULE_BY_NAME = {r.name: r for r in ALL_RULES}


def _cut(lines: list[str], start: int, end: int) -> None:
    del lines[start:end]


def repair_text(text: str, *, encoding: bool = False) -> tuple[str, list[tuple[str, str]]]:
    """Remove fetch damage from `text`, leaving the author's prose alone.

    Returns (repaired text, [(rule, text removed)]). Front matter is never
    touched: `word_count`, `title` and the identifiers are the catalogue's, not
    the fetcher's.
    """
    start = _front_matter_end(text)
    head, body = text[:start], text[start:]
    lines = body.split("\n")
    removed: list[tuple[str, str]] = []

    for name, mode in REPAIR_MODE.items():
        rule = _RULE_BY_NAME.get(name)
        if rule is None:
            raise SystemExit(f"REPAIR_MODE names an unknown rule: {name}")
        while True:
            scannable = _strip_fenced_code(strip_deliberate("\n".join(lines)))
            if rule.pattern.pattern == "(?!)":
                # Classifier-supplied: remove every qualifying line, highest
                # first so the remaining indexes stay valid.
                if name == "ad-payload-block":
                    targets = sorted(_config_run_lines(scannable.split("\n")),
                                     reverse=True)
                elif name == "js-terminator-run":
                    targets = sorted(_terminator_lines(scannable.split("\n")),
                                     reverse=True)
                elif name == "injected-script-run":
                    targets = sorted(_script_run_lines(scannable.split("\n")),
                                     reverse=True)
                elif name == "comment-thread":
                    targets = sorted(_comment_thread_lines(scannable.split("\n")),
                                     reverse=True)
                else:  # pragma: no cover
                    targets = []
                if not targets:
                    break
                for i in targets:
                    removed.append((name, scannable.split("\n")[i].strip()[:100]))
                    _cut(lines, i, i + 1)
                continue
            matches = rule.find_all(scannable)
            if not matches:
                break
            m = matches[0]
            # Map the offset in the scanned text back to a line index. The scan
            # only deletes characters, never whole lines, so counting newlines up
            # to the match is exact.
            line_no = scannable.count("\n", 0, m.start())
            if mode == "lines":
                block = m.group(0).count("\n")
                _cut(lines, line_no, line_no + block)
            elif mode == "line":
                _cut(lines, line_no, line_no + 1)
            else:  # inline
                a, b = m.start(), m.end()
                head_off = scannable.rfind("\n", 0, a) + 1
                tail_off = scannable.find("\n", b)
                tail_off = len(scannable) if tail_off == -1 else tail_off
                lines[line_no] = (scannable[head_off:a] + scannable[b:tail_off])
            removed.append((name, m.group(0).strip()[:100]))

    body = "\n".join(lines)

    if encoding:
        from html import unescape

        for name, _cls, pattern, literal in ENCODING_REPAIRS:
            while True:
                m = pattern.search(body)
                if not m:
                    break
                removed.append((name, m.group(0)))
                body = body[:m.start()] + (
                    literal if literal is not None else unescape(m.group(0))
                ) + body[m.end():]

    # Collapse the runs of blank lines the removals leave behind, and any
    # trailing space they strand at the end of a line.
    body = re.sub(r"[ \t]+$", "", body, flags=re.M)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return head + body, removed


def main() -> int:
    import sys

    auto_only = "--auto-only" in sys.argv
    pairs = list(scan_collections(judgement=not auto_only))
    by_class, by_rule = summary(pairs)
    print(f"scanned {len(RECOVERED_DIRS)} collections, "
          f"{len(pairs)} file(s) with hits")
    print("  by class: " + (", ".join(f"{k}={v}" for k, v in sorted(by_class.items()))
                            or "clean"))
    print("  by rule:")
    for rule, n in sorted(by_rule.items(), key=lambda kv: -kv[1]):
        r = next(r for r in ALL_RULES if r.name == rule)
        mark = "GATE " if r.automatic else "triage"
        print(f"    [{mark}] {rule:<32} {n:5d}  {r.note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
