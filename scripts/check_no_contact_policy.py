#!/usr/bin/env python3
"""The no-contact policy must say the same thing everywhere a reader meets it.

WHY THIS FILE EXISTS
--------------------
On 2026-10-02 the policy was rewritten in ten places. Nothing checked them. The
rewrite had to be applied by hand, twice, because the first pass silently missed
four files whose HTML is indented with two spaces - and a script that reports four
missing files for what is really one whitespace bug is a script that gets ignored.

This checks three things a reader cannot:

  1. EVERY reader-facing surface carries the rule. A page that drops it is a page
     where someone reads about the archive and never learns they must not contact
     the author.
  2. EVERY surface states BOTH grounds. The explicit request AND the inference
     from his leaving online dawah. The second is the load-bearing one: it closes
     the reading in which someone rejects the request and concludes contact is
     therefore permitted.
  3. NO surface tells anyone to contact him. Including the things that look
     helpful - the maintainer address is below the rule on every page, and a
     reader who reads "do not contact" followed by a mailto can reasonably take
     the whole block as an invitation.

DELIBERATELY NOT CHECKED
------------------------
The exact wording, on any surface. These ten places are written for different
audiences - a footer line, a machine-readable index, an issue-template link
label - and forcing them character-identical would produce one awkward sentence
repeated ten times. What is checked is that they agree in substance, because
substance is what a reader is bound by and prose is not.

`llms-full.txt` is generated and gitignored, and `docs/recovery-log/` is a dated
log; neither is edited by hand and neither is checked here.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: (path, human label). Every place a reader meets this policy.
SURFACES = [
    ("NOTICE.md", "the notice, section 10"),
    ("README.md", "the readme"),
    ("CONTRIBUTING.md", "the contributing guide"),
    ("llms.txt", "the machine-readable index"),
    ("_layouts/default.html", "the footer of every page"),
    ("index.md", "the home page"),
    ("asadullah-ali-al-andalusi.md", "the identity page"),
    ("asadullahali-com-what-happened.md", "the domain-history page"),
    ("scholarly-records.md", "the bibliographic-records page"),
    (".github/ISSUE_TEMPLATE/config.yml", "the issue template"),
]

#: Surfaces that contain an AUTHORITATIVE BLOCK, which must carry the rule itself
#: rather than merely the file carrying it somewhere.
#:
#: NOTICE.md states the policy twice - once in section 10, which is the
#: authoritative statement, and once in passing in section 4.1. Without this, the
#: first version of this gate passed a NOTICE.md whose section 10 had been gutted,
#: because section 4.1 still contained the words. Demonstrated, not theorised:
#: deleting "asked not to be contacted" from section 10 left the gate green.
AUTHORITATIVE = {
    "NOTICE.md": ("## 10. DO NOT CONTACT THE AUTHOR", "## 11."),
}

#: Both grounds must appear. Normalised so line wrapping and HTML entities do not
#: decide whether a surface passes.
def normalise(text: str) -> str:
    t = text.lower()
    t = t.replace("&mdash;", "-").replace("&rsquo;", "'").replace("&#8217;", "'")
    t = t.replace("&nbsp;", " ").replace("’", "'")
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t


#: Ground one: the explicit request. Stronger evidence than the inference, and
#: dropping it loses a true claim about what he actually said.
GROUND_EXPLICIT = re.compile(r"asked not to be contacted")

#: Ground two: the inference from his leaving. Checked as TWO conditions rather
#: than one alternation, and the earlier version got this wrong.
#:
#: The first version matched `would not want to be found|left online dawah`, so
#: merely MENTIONING that he left satisfied it. Deleting the inference from
#: NOTICE.md section 10, from README.md, and from scholarly-records.md all left
#: the gate green - three of six mutations missed, and each was a real erosion of
#: the rule.
#:
#: The point of this ground is the reasoning, not the fact. He has left: that is
#: stated on all ten surfaces already and it grounds nothing by itself. What
#: grounds the rule is the step from leaving to "would not want to be found".
MENTIONS_LEAVING = re.compile(r"left online dawah|leaving online dawah")
STATES_INFERENCE = re.compile(
    r"would not want to be (?:found|contacted|approached|troubled|pursued)"
    r"|would not want anyone to (?:find|contact|reach)"
    r"|would not want to be tracked down")

#: An INVITATION, narrowly. Imperative, sentence-initial, no negation.
#:
#: Three attempts at catching invitations by pattern, all recorded because the
#: failure modes are the point:
#:
#:   1. A +/-70 character window around the phrase. Missed a real invitation two
#:      clauses after "never said a word about it" - negation was nearby and the
#:      window could not tell whose clause it belonged to.
#:   2. The 48 characters before the phrase. FIFTEEN false positives on correct
#:      policy text, including "requests to contact him ... will not be
#:      answered" and "nothing on this page is an invitation to reach him".
#:      A gate that cries wolf on correct text is worse than no gate.
#:   3. The sentence. Better - down to two false positives - but still wrong on
#:      "the request most often arrives as an issue that asks how to reach him",
#:      which describes a request rather than making one.
#:
#: What survives is the shape an invitation actually takes when written FOR a
#: reader: imperative mood, at the start of a sentence or list item. Descriptive
#: mentions - "asks how to reach him", "requests to contact him will not be
#: answered" - are mid-sentence and so do not match.
#:
#: KNOWN LIMITATION: a mid-sentence invitation ("if you need to reach him, email
#: the author") is not caught. That shape is rarer in policy prose, and chasing
#: it is what produced the fifteen false positives. The two grounds checks are
#: what protect the policy; this is a backstop against a stray instruction.
CONTRADICTIONS = [
    r"contact (?:the |him|author)",
    r"reach (?:the )?(?:author|him)",
    r"email (?:the )?(?:author|him)",
    r"get in touch with (?:the )?(?:author|him)",
    r"write to (?:the )?(?:author|him)",
    r"message (?:the )?(?:author|him)",
    r"track (?:him|the author) down",
]

#: Where an imperative invitation can legally sit: start of text, start of a
#: sentence, or the start of a list item / heading.
INVITATION_POSITION = re.compile(
    r"(?:^|[.!?;:]\s+|\s-\s|^\s*[-*>]\s*|^#+\s+)\s*$")

#: Negation that marks a phrase as PROHIBITION rather than invitation.
NEGATION_IN_SENTENCE = re.compile(
    r"\b(?:not|no|none|nothing|nobody|never|cannot|can't|won't|wouldn't|"
    r"should\s+not|must\s+not|do\s+not|does\s+not|did\s+not|n't|without|"
    r"refuse|refuses|refused|declines|declined|instead)\b", re.I)

SENTENCE_BREAK = re.compile(r"(?:[.!?;]\s|\s-\s|\n)")


def sentence_around(text: str, start: int, end: int) -> str:
    """The sentence containing text[start:end], with a little slack either side.

    Slack matters because the negation and the invitation phrase are often in
    the same sentence but not adjacent: "requests to contact him, requests for
    his personal details, and invitations to events WILL NOT BE ANSWERED" is one
    prohibition spread over twenty words.
    """
    lo = 0
    for mm in SENTENCE_BREAK.finditer(text, max(0, start - 400), start):
        lo = mm.end()
    hi = len(text)
    mm = SENTENCE_BREAK.search(text, end, min(len(text), end + 400))
    if mm:
        hi = mm.start()
    return text[lo:hi]


def main() -> int:
    problems: list[str] = []
    checked = 0

    for rel, label in SURFACES:
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing ({label})")
            continue
        raw = p.read_text(encoding="utf-8")

        # If this file has an authoritative block, the rule must be IN that block.
        # Checking only the whole file is how a gutted section 10 passes: NOTICE.md
        # states the policy in section 10 AND in passing in section 4.1, so
        # deleting it from section 10 left the earlier version of this gate green.
        # Demonstrated, not theorised.
        scope_name, scope_text = "the file", normalise(raw)
        if rel in AUTHORITATIVE:
            start_mark, end_mark = AUTHORITATIVE[rel]
            a = raw.find(start_mark)
            b = raw.find(end_mark, a + len(start_mark)) if a >= 0 else -1
            if a < 0:
                problems.append(
                    f"{rel}: no authoritative block found (expected the heading "
                    f"{start_mark!r}). If section 10 was renamed, rename it here "
                    f"rather than deleting the entry.")
                continue
            block = raw[a:] if b < 0 else raw[a:b]
            scope_text = normalise(block)
            scope_name = "its authoritative block"

        body = normalise(raw)
        checked += 1

        if "do not contact" not in scope_text and "not be contacted" not in scope_text:
            problems.append(
                f"{rel} ({label}): {scope_name} carries no no-contact rule at all")

        if not GROUND_EXPLICIT.search(scope_text):
            problems.append(
                f"{rel} ({label}): {scope_name} does not state that he asked not "
                "to be contacted. That is the stronger of the two grounds and "
                "dropping it loses a true claim.")

        if not MENTIONS_LEAVING.search(scope_text):
            problems.append(
                f"{rel} ({label}): {scope_name} does not record that he left "
                "online dawah, which is the fact the second ground rests on.")

        if not STATES_INFERENCE.search(scope_text):
            problems.append(
                f"{rel} ({label}): {scope_name} records that he left online "
                "dawah but never draws the conclusion from it. Mentioning the "
                "leaving grounds nothing; the rule needs the step to 'would not "
                "want to be found', so it binds readers who reject the explicit "
                "request as a request.")

        # The contradiction scan stays file-wide: an invitation to contact him is
        # a problem wherever it appears, even outside the authoritative block.
        for pat in CONTRADICTIONS:
            for m in re.finditer(pat, body):
                # Only an IMPERATIVE, sentence-initial phrase is an invitation.
                if not INVITATION_POSITION.search(body[:m.start()]):
                    continue
                sentence = sentence_around(body, m.start(), m.end())
                if NEGATION_IN_SENTENCE.search(sentence):
                    continue  # "requests to contact him ... will not be answered"
                problems.append(
                    f"{rel} ({label}): appears to INVITE contact with the "
                    f"author: ...{sentence.strip()[:150]}...")

    print(f"  surfaces checked          : {checked}/{len(SURFACES)}")

    if problems:
        for p_ in problems:
            print(f"FAIL: {p_}")
        print(f"check_no_contact_policy: {len(problems)} problem(s)")
        return 1

    print("  both grounds on all surfaces: yes (authoritative blocks scoped)")
    print("  invitations to contact him : 0")
    print("check_no_contact_policy: 0 problem(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())