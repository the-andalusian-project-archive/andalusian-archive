# NOTICE

**The Andalusian Project Archive** — a preservation record of the written and
spoken work of Asadullah Ali Al-Andalusi ("The Andalusian Project"), assembled
by the site owner as an act of archival recovery.

Read this file before you reuse, quote, mirror or redistribute anything here.
It is not boilerplate: it states what this archive is, what it does **not**
have the right to license, what has been deliberately withheld, and what will
mislead you.


## 1. What this archive is

A preservation record. The original sites were taken down, mirrored, or
otherwise lost; this repository holds what could be recovered before it
disappeared, with a record of where each piece came from.

It currently holds, as of 2026-09-27:

| | |
|---|---|
| Written works | **72** catalogued — 47 with full text recovered in this repository, 24 held only as Wayback captures, 1 lost entirely |
| Capture records | **87** Wayback/CDX capture records preserved as metadata |
| Videos | **68** catalogued, with **68** machine-transcript documents |
| Academic papers | **20** catalogued, of which **6** PDFs are held in this repository |
| Third-party source records | **70** rows |

Where a work was recovered, the reproduction is **verbatim**. This archive does
not edit his prose, does not summarise it in place of it, and does not correct
it. Where a work could not be recovered, it is recorded as missing rather than
quietly dropped.


## 2. OPENLY AVAILABLE IS NOT OPEN SOURCE

This is the single most important distinction in this file.

His essays were published on websites that anyone could read without paying.
**That is availability, not permission.** Copyright in that prose was never
surrendered, no open licence was ever applied to it, and no Creative Commons
grant was ever made by its author over it. Nothing in this repository changes
that, and nothing in this repository should be read as though it did.

So:

* The archive reproduces his prose **as a preservation and attribution record**.
* The archive **does not license** that prose, and cannot. The rights are his
  (or, for the journal and conference papers, his and his co-authors' and the
  publishers').
* Reuse of his prose is governed by the rights holder's terms, not by this
  repository's. What the repository grants you is scoped in `LICENSE` to the
  archive's *own* material only.
* "You can read it" was never a licence, and the disappearance of the original
  site did not convert one into the other. Reproducing a text that has gone
  offline, with attribution and provenance, is the narrow case this archive is
  built for. It is not a claim over the text.

Anyone who tells you this material is "open source" or "free to republish" is
wrong, and `LICENSE` will show you exactly where the grant stops.


## 3. Provenance, and how to check it

Every recovered item carries where it came from:

* **Written works** — the original URL as published, plus the Wayback capture
  timestamp it was recovered from (for example capture `20120717030040` of
  `asadullahali.wordpress.com`). The `wayback_url` on each work is the
  timestamped capture, not a live link, and the capture ID is the identity of
  the copy. The full trail is in `_data/canonical_works.json` and
  `_data/recovery_log.json`.
* **Videos** — the recording, the channel or mirror it came from, and the
  caption/transcript capture. See `_data/videos.json` and
  `_data/transcript_coverage.json`.
* **Papers** — publisher, DOI where one exists, and the repository or journal
  copy. `_data/bibliography.json` is the full ledger, including everything
  restricted, dead or unobtainable, so the gaps are visible rather than
  hidden. The per-file licence and provenance for each held PDF is the
  `file_licence` field of its row in `_data/papers.json`, and is printed on
  the paper's page.

Where a page names an original URL, that URL is a **citation**: it records
where the work was published, not an endorsement of the destination as it
stands today. See section 7.

Nothing here was obtained by circumventing a paywall, a robots rule or an
access control. Where a source was inaccessible, that is recorded as
inaccessible. Where a challenge was not fought, the notes say so.


## 4. Attribution is required, and crediting this archive is not enough

If you quote or reproduce any of his work, cite **the author, the work, and the
capture**:

> Asadullah Ali Al-Andalusi, "*Title of the work*," *original URL*, capture
> recorded in The Andalusian Project Archive (capture ID / Wayback timestamp
> as given on the page).

Crediting "The Andalusian Project Archive" **alone does not satisfy this**.
The archive is the record, not the author. If you reuse the archive's own data,
scripts or site, credit the archive and link to the licence.


## 5. The machine transcripts carry this disclaimer

Every transcript in `_transcripts/`, and every transcript block on an article or
video page, is machine-generated. The disclaimer is printed on each of them and
is reproduced here verbatim:

> *Transcript by machine — accuracy isn't perfect, so it shouldn't be used in
> polemics or debate material as an authoritative source.*

This is not a formality. These transcripts are the output of automatic speech
recognition over video captions. They mishear names, mis-split sentences, lose
negations and flatten argument. They are a **finding aid** — a way to search
the corpus and find the moment worth going back to the video for. They are not
an authorised edition of what was said, and quoting one as though it were
settles nothing.


## 6. WITHHELD / NOT PUBLISHED

The following is deliberately absent. This list is public on purpose: a
withheld item that is not disclosed is a silent gap, and a silent gap is how an
archive becomes unreliable.

### 6.1 Two personal names

At the site owner's decision, **two of his personal names appear nowhere in the
published material**:

* his **legal / real name** — the name printed in the author line of his
  published academic work; and
* his **birth name** — the name he discusses himself in his own conversion
  account.

In the data files and on the paper page where an institutional author line
carried the legal name, the name is replaced with `[real name withheld]`, the
row is flagged `author_name_redacted: true`, and a `redaction_note` on the same
row says why. The **citation is left factually intact** — source URL, DOI,
issuing institution and every other bibliographic field are unchanged, so the
reference still resolves at the institution that published it. That
institution's own public record is not this archive's to alter, and was not
altered.

The kunya **Abu Isabel** is *not* withheld. It appears only inside verbatim
quotations of live YouTube video titles, which are public metadata and are
part of the evidence. Those occurrences are left intact on purpose.

### 6.2 Withheld raw captures

Three raw capture files are **not tracked in this published repository**:

| File | Why |
|---|---|
| `.firecrawl/transcripts/cap-7KBCENktOOU.en-orig.vtt` | verbatim caption capture of his conversion-story recording; **contains the birth name** |
| `.firecrawl/transcripts/cap-D2t0idkAqjA.en-orig.vtt` | same recording, second capture; **contains the birth name** |
| `.firecrawl/transcripts/cap-G47Stp3pLss.en-orig.vtt` | third-party re-upload of the same recording; **contains the birth name** |

They are **withheld, not edited**: they are verbatim source evidence, so the
bytes are preserved unaltered in the private working tree and only the
published repository's copy is dropped. Editing an evidence file to remove a
name would destroy the thing that makes it evidence.

The reader-facing text is served separately, under `/_transcripts/`, built from
these captures and carrying the machine-transcript disclaimer of section 5.

> **Redaction applied to the published transcripts (2026-09-27).** The birth
> name also occurred in the body text of the three published machine-transcript
> pages built from these captures — 4 occurrences in each, 12 in total, in his
> own words describing the origin of his family name. Untracking the raw
> captures did not redact them, and this notice previously recorded that gap as
> open. It is now closed: `scripts/build_collections.py` substitutes the name
> for a visible marker, **‖ birth name withheld ‖**, at document-build time, so
> the marker is written into `_transcripts/*.md` itself rather than applied by
> the template at view time. The three affected pages are
> `/_transcripts/7KBCENktOOU/`,
> `/_transcripts/D2t0idkAqjA-duplicate-upload/` and
> `/_transcripts/G47Stp3pLss/`; each carries a `redaction_note` in its front
> matter saying what was withheld, how many times, and why, and the layout
> prints that note to the reader. No other word in those documents is altered,
> and `scripts/test_transcripts.py` fails if the name reappears, if the marker
> count does not equal the occurrence count, or if any other transcript drifts
> from its capture.
>
> This is the one place where the archive's usual "reproduced verbatim" rule
> yields to a redaction, and it is recorded here rather than left for a reader
> to infer from a gap. The unredacted text is still not published: the raw
> captures remain withheld from this repository, so the withheld words are
> available to no reader of the published archive at all.
>
> All three captures **must remain on disk** in the maintainers' working tree
> and must be load-bearing to the build. `cap-7KBCENktOOU.en-orig.vtt` is the
> capture named by the coverage row for video `7KBCENktOOU`;
> `cap-D2t0idkAqjA.en-orig.vtt` is named by that row's `alternates`;
> `cap-G47Stp3pLss.en-orig.vtt` is the sole capture named for video
> `G47Stp3pLss` (15,048 lines). All three are read by
> `scripts/test_transcripts.py`, which re-derives all 68 published transcripts
> from the files the coverage data names. Removing one from disk breaks the
> suite and orphans a served page; only the *index* copy is dropped.

### 6.2a Files redacted in place, at publication time

| File | What was redacted |
|---|---|
| `_transcripts/transcript-7KBCENktOOU.md` | birth name, 4 occurrences → `‖ birth name withheld ‖` (generated; see 6.2) |
| `_transcripts/transcript-D2t0idkAqjA-duplicate-upload.md` | birth name, 4 occurrences → `‖ birth name withheld ‖` (generated; see 6.2) |
| `_transcripts/transcript-G47Stp3pLss.md` | birth name, 4 occurrences → `‖ birth name withheld ‖` (generated; see 6.2) |
| `docs/recovery-log/2026-09-27-review-phase2.md` | birth name, 1 occurrence → `‖ birth name withheld ‖` |
| `docs/superpowers/plans/2026-09-27-full-recovery-v6.md` | birth name, 1 occurrence → `‖ birth name withheld ‖` |

The two `docs/` files are the committed evidence trail and the plan this
recovery was executed against. They are redacted rather than removed because
removing a review finding would destroy the audit record; the redaction is
marked in place so the change is visible rather than silent.

`README.md` previously published his legal name in an "Also published as"
section. That section has been removed, and the two places in the README that
referred to the name now state that it is withheld and point here, so nothing
dangles. `docs/profile-readme.md` and the working notes under `.superpowers/`
still carry the name and are recorded as known residues in the publication
report; they are the maintainers' own records, not published site content.


### 6.3 A PDF withheld for unverified provenance

`_papers/pdfs/architects-of-civilisation-sallahuddin-ayubi.pdf`
("Architects of Civilisation: Sallahuddin Ayubi", IAIS Malaysia book chapter,
5 pp.) is **not published**.

The file was held and is genuine, but it came from a prior-research pool and
**no confirmed public source URL could be established** for that exact file:
the Academia.edu listing that would attribute it sits behind a managed
Cloudflare challenge, which this archive did not attempt to bypass. Third-party
full-text mirrors of the chapter exist; they were deliberately not used as a
source, and no unattributed URL is asserted in their place.

An archive that states a provenance it cannot support is not an archive. The
**citation is retained in full** — author, title, publisher, and the listing
URL, which is recorded as a link-out, not a mirror. The remaining **6** held
PDFs keep their existing licences and links, recorded per paper in
`_data/papers.json`.


## 7. WARNING: THE ORIGINAL DOMAIN IS NO LONGER HIS

The site this corpus was published on is gone, and **the domain itself has been
taken over**. It now resolves to an unrelated, commercially operated site.

**Do not visit it. Do not link to it. Do not treat anything served there as his
work, his statement, or his archive.**

This matters because third-party pages still point at it. Institutional
profiles, course listings and academic faculty pages — including pages this
archive itself catalogues under `_data/albalagh_courses.json` — continue to
present that domain as his official site, because those pages were written
before the takeover and nobody updated them. **If you arrive here from one of
those links, you are arriving from an outdated reference, not from him.**

If you are following a citation to a work, follow the **Wayback capture**
recorded on the page, or the archive's own copy — not the live domain. The
capture timestamp in the provenance block is what makes the citation resolve to
what he actually wrote.

The archive deliberately does not reproduce the domain as a live hyperlink in
this notice. Naming it here is necessary to warn you; making it clickable would
defeat the warning.


## 8. What this corpus is, and what it is not

**This is a dated polemical archive.**

The material is argument, not reference. It is apologia, critique and rebuttal —
written by a Muslim apologist responding to what he took to be misrepresentations
of Islam, of Muslim practice, and of the people he disagreed with. It is
preserved here because it was published and then lost, not because it is
settled, balanced, current, or endorsed.

* **The claims are his.** They were his claims, argued in his voice, on the
  dates shown. Reproducing them records what he argued. It does not adopt them.
* **This archive does not endorse any of it**, and neither does the archive
  owner. Nothing here should be read as a position of the archive on any
  religious, political or scholarly question raised in the corpus.
* **Named individuals are described in the author's words, as of the dates
  shown.** Real people — living and dead — are discussed, characterised,
  criticised and sometimes accused. Those descriptions are his, timestamped,
  and frequently polemical. Do not treat them as verified fact, as the archive's
  own assessment, or as fair characterisation. Several of the people discussed
  are identifiable academics, public figures and activists who did not consent
  to being discussed in an archive.
* **Positions have moved.** A 2011 text on a 2026 question is a historical
  document. Read it as one. Where a statement has been overtaken by events, this
  archive does not update it, because updating it would falsify the record.

Read this corpus as evidence of a particular writer's arguments at particular
times. That is the only claim it makes, and the only one it can support.


## 9. Provenance of the corrections in this file

Redactions, the withheld-PDF decision and the licence scope were made by the
site owner on 2026-09-27 and applied to the data files, the paper pages, this
notice, and the repository's ignore rules. The reasoning for each is recorded in
`_data/bibliography.json` (policy), `_data/papers.json` (`redaction_note`,
`file_licence`) and the `.gitignore` comments at the point of application.

The same day, the owner's decision on the **birth name** was carried through to
the three published transcript pages that still carried it, and the decision on
the **hijacked live domain** was enforced in the layouts:

* the birth name is substituted at document-build time by
  `scripts/build_collections.py` (`BIRTH_NAME`, `BIRTH_NAME_MARKER`,
  `redact_birth_name()`), which writes both the marker and a per-document
  `redaction_note`; the raw captures are untouched, and
  `scripts/test_transcripts.py` gates the result;
* the live domain is never emitted as an `href`. `_includes/source_link.html`
  prints such a URL as plain text and leaves the Wayback capture as the
  clickable source; `scripts/build_collections.py` and the four layouts that
  render provenance all route their source URLs through it;
* his **legal name** is no longer published in `README.md`, and the two evidence
  documents listed in 6.2a carry the birth name as a marker rather than as text.

Each of these is a departure from a rule stated elsewhere in this file, which is
why each is recorded here rather than left as an unremarked difference.
