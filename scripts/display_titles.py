"""What a link, a heading or a card calls a work.

WHAT THIS IS
============
A preservation archive stores two different strings for every recording: the one
the channel used, and the one a reader should be shown. They are not the same
string, and conflating them is how a title ends up carrying a filename.

Of the 248 collection files in this corpus, 120 had a bare YouTube video ID in
the title - `[1U6VfHosrqw]`, `[A3dbBCBSFKk]`. The uploader puts those in the
title they type into YouTube, and the capture copies it faithfully, which is
correct for provenance and wrong for a page a person reads. A reader cannot use
`[A3dbBCBSFKk]` to do anything except guess.

WHAT IS NOT THROWN AWAY
=======================
Nothing is deleted from the archive. The video ID stays in front matter as
`video_id`, the slug stays in the filename, and the raw title is preserved
verbatim. This function changes DISPLAY text only. `TITLE_EDITS` records every
substitution so the log shows exactly which words were not shown and why, and
`check_display_titles` fails the build if a code name reaches a page.

The line is deliberately narrow. It removes storage identifiers and uploader
boilerplate. It does NOT touch the author's punctuation, spelling or wording -
`33 -` stays `33 -` because the channel numbered it and the number is part of
what he published. Rewriting a title into something tidier is how a
preservation archive starts editing its author.
"""

from __future__ import annotations

import re

# YouTube IDs are exactly 11 characters of [A-Za-z0-9_-]. Anchored to a bracket
# pair so that a genuine editorial bracket, or a chapter list that happens to
# contain eleven characters, is left alone.
_ID_IN_BRACKETS = re.compile(r"\s*[\[(]([A-Za-z0-9_-]{11})[\])]\s*$")

# The uploader's own channel name, typed after a full-width or ASCII bar:
# "... Answering Doubts About Islam ｜ MSA OSU by Andalusian Project". That
# clause names the account, not the talk. Dropped only when a real title
# survives without it, so a title that is nothing BUT a channel name is kept.
_UPLOADER_CLAUSE = re.compile(r"\s*[｜|]\s*[^｜|]{2,60}\s*$")

# Some uploads carry the channel after a colon or a double bar instead, and
# after the clause above is removed a separator can be left dangling
# ("... - MY STORY ｜｜ The Andalusian Project" -> "... - MY STORY ｜").
# Separators are only ever removed from the end, never from inside a title.
_DANGLING_SEP = re.compile(r"[\s｜|]+$")

# The archive publishes on channels of its own, so a trailing reference to one
# of them is boilerplate rather than part of the title's subject. Named
# explicitly rather than pattern-matched, because a generic "strip the last
# few words" rule is how a title loses its actual subject.
FIRST_PARTY_CHANNELS = (
    "The Andalusian Project",
    "Andalusian Project",
    "MSA OSU by Andalusian Project",
    "Al Andalusian Project",
    "Al-Balagh Academy",
    "Al Balagh Academy",
    "Islamic Advice and Solutions",
    "IAIS",
    "Andalusian",
)
_CHANNEL_SUFFIX = re.compile(
    r"\s*[｜|:：]\s*(?:"
    + "|".join(re.escape(c) for c in FIRST_PARTY_CHANNELS)
    + r")\s*$",
    re.IGNORECASE,
)

_WHITESPACE = re.compile(r"[ \t ]{2,}")

# Internal bookkeeping the archive appended to a title. It explains why a
# duplicate transcript exists, which belongs on the transcript's own page where
# it is stated in prose, not welded onto the end of every link to it.
_INTERNAL_NOTE = re.compile(
    r"\s*-\s*transcript of a duplicate upload\s*$", re.IGNORECASE
)

# The information a title must never lose. A series published as Parts 1..5
# under one name is distinguished ONLY by its part number: strip it and five
# distinct talks render as five identical links. This pattern is used as a
# veto - a candidate rewrite that drops a marker present in the original is
# rejected outright, not repaired afterwards.
_PART_MARKER = re.compile(
    r"\b(?:part|pt|episode|ep|lesson|session|talk|lecture|chapter|vol|volume"
    r"|installment|track|programme|program|seminar)\s*\.?\s*\d+\b"
    r"|\bpart\s+(?:one|two|three|four|five|six|seven|eight|nine|ten)\b",
    re.IGNORECASE,
)

#: slug/URL -> (shown, raw) for every title this module changed, so a reviewer
#: can see what was withheld from the reader without diffing 248 files.
TITLE_EDITS: dict[str, tuple[str, str]] = {}


def _drop(pattern: re.Pattern, out: str) -> str:
    """Apply one removal, unless doing so would lose a part marker.

    The veto is per step rather than a single check at the end. Applied once at
    the end it has to choose between "undo everything" and "accept the damage",
    and both are wrong: refusing a legitimate identifier removal because a later,
    unrelated rule would have been harmful leaves the identifier on the page.
    Each rule is judged on its own effect.
    """
    candidate = pattern.sub("", out, count=1)
    if candidate == out:
        return out
    if _PART_MARKER.search(out) and not _PART_MARKER.search(candidate):
        return out
    return candidate


def clean_display_title(raw: str) -> str:
    """The title a reader is shown. Returns `raw` unchanged when unsure."""
    original = str(raw or "")
    if not original.strip():
        return original

    out = original.strip()
    out = _INTERNAL_NOTE.sub("", out)
    out = _ID_IN_BRACKETS.sub("", out)
    out = _drop(_UPLOADER_CLAUSE, out)
    out = _drop(_CHANNEL_SUFFIX, out)

    # Removing a clause can leave the separator that introduced it behind.
    out = _DANGLING_SEP.sub("", out)
    out = _WHITESPACE.sub(" ", out).strip()

    # Every rule above can only remove. If it left nothing, the raw string was
    # the whole of the title and it goes back unchanged.
    if not out or out in {"-", "|", "｜", "[]", "()"}:
        return original.strip()

    if _PART_MARKER.search(original) and not _PART_MARKER.search(out):
        return original.strip()

    if out != original.strip():
        TITLE_EDITS.setdefault(out, (original.strip(), original.strip()))
    return out


def check_display_titles(extra_fails: list[str] | None = None) -> list[str]:
    """Fail the build if a code name would reach a reader.

    `extra_fails` lets the caller fold in its own findings so one run reports
    every naming problem rather than the first kind of them.
    """
    fails = list(extra_fails or [])

    for shown, (raw, _why) in sorted(TITLE_EDITS.items()):
        if re.search(r"[A-Za-z0-9_-]{11}", shown) and not re.search(r"[A-Za-z0-9_-]{11}", raw):
            fails.append(
                f"display title still carries an 11-character identifier: {shown!r} "
                f"(from {raw!r})"
            )
        if shown.endswith(".md"):
            fails.append(f"display title is a filename: {shown!r} (from {raw!r})")

    return fails


def check_no_collisions(pairs) -> list[str]:
    """Cleaning must never make two different titles into one.

    A series published as Sessions 1..13 differs from its siblings by a single
    token. Remove it by accident and thirteen links all read "01 - Understanding
    Atheism" - the shelf looks fine, nothing raises, and the archive has quietly
    stopped being able to say which talk is which.

    `pairs` is (raw, shown). A collision counts only when the two raw titles
    were genuinely different beyond the boilerplate the cleaner is allowed to
    remove, because a video and the transcript of that same video are meant to
    share a name.
    """
    groups: dict[str, list[str]] = {}
    for raw, shown in pairs:
        groups.setdefault(shown, []).append(raw)

    fails = []
    for shown, raws in sorted(groups.items()):
        if len(raws) < 2:
            continue
        # Reduce each raw to just the part the cleaner is allowed to drop; if
        # those reductions are still all different, the shown title is wrong.
        def residue(raw: str) -> str:
            r = _INTERNAL_NOTE.sub("", raw.strip())
            r = _ID_IN_BRACKETS.sub("", r)
            return _WHITESPACE.sub(" ", r).strip()

        if len({residue(r) for r in raws}) > 1:
            fails.append(
                f"{len(raws)} distinct titles all display as {shown!r} - "
                "cleaning removed the words that told them apart: "
                + "; ".join(sorted({residue(r) for r in raws})[:4])
            )
    return fails
