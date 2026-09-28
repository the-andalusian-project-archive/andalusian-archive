# The Andalusian Project Archive — v1.0.0

**Prepared 2026-09-28. Not published.** This file is the release note for the
GitHub release of the archive at
<https://the-andalusian-project-archive.github.io/andalusian-archive/>. The
maintainer creates the release and uploads the assets; nothing here has been
tagged, uploaded or published.

**Repository:** `the-andalusian-project-archive/andalusian-archive`
**Version:** 1.0.0 (matches `package.json`)
**Live site:** <https://the-andalusian-project-archive.github.io/andalusian-archive/>

---

## Read this before you tag

Nothing is blocking v1.0. The site tour that used to be a blocker has been
re-recorded three times over: after the recount was approved and applied, after
the reading-first redesign, and again on 2026-09-28 in the design's own **light**
theme — which is now also the site's default — with the SEP-red accent and a
Ken Burns move that actually moves. Their captions carry the current figures
(220 recovered items, 72 works with 47 in full, 20 papers, 79 transcripts of
937,738 words) and their screenshots show the `/topics/` layer, which the
previous cut did not include at all. The assets below can be attached as they
stand.

The tour is still a picture of one moment rather than a live feed. If a later
approved recount changes a figure after v1.0 is tagged, re-cut it then; see
[`README.md`](README.md) § *Re-recording*.

---

## What v1.0 contains

Every figure below is counted from `_data/` at build time or read out of a
`_data/` file. None is typed into a page.

### The corpus

| | Count | What is actually held |
|---|---:|---|
| Written works | **72** | 47 with full text in the repository, 24 catalogued Wayback-only with no text held, 1 unrecovered. Dated 2011-12-18 to 2020-08-11. |
| Video records | **68** | 56 preserved as files in the Internet Archive's `andalusian-project` collection; 25 catalogued as live re-uploads. 36 mirror URLs attached to the 30 entries they duplicate; 12 superseded duplicates preserved in full in a ledger rather than deleted. |
| Machine transcripts | **79 documents** | 937,738 words, 67,720 paragraphs, one document per capture. 57 attached to a video record, 11 preserved but deliberately not attached. 58 distinct recordings behind the 68 documents. |
| Academic papers | **20** | **5 PDF files across 4 of the 20 paper records**; one of the five is a Japanese translation of a paper already counted. 2 further PDFs withheld in full. A 24-row access ledger records 8 open-access, 15 restricted and 1 dead item, so the gap is visible rather than implied. |
| MDI author-archive pages | **17 rows / 4 items** | All 17 held verbatim, 24,081 words. The 13 that republish an already-counted work are decided by 5-gram text comparison, not title similarity. |
| Announcements | **3** | Catalogued and held with their text, never counted as works. |
| Link-outs | **10** | 1 conversion-story reprint held as metadata only (its body was never fetched) + 9 Yaqeen pages, which are link-outs by policy. |
| Third-party source records | **70** | Catalogued and never counted. Derived from this archive's own catalogue, so counting them would count the archive against itself. |
| Wayback capture records | **87** | One record per CDX capture, preserved as metadata. |
| Recovery-log rows | **74** | Per-work verdicts with the method and word count for each. |

**Total counted content: 220**, and it is a sum rather than a figure anyone
typed. The site prints the arithmetic it performed:

```
Total 220 = 72 works + 81 videos + 20 papers + 4 MDI items + 9 Yaqeen link-outs + 33 Al Balagh link-outs + 1 interview
```

Every count on every page — the homepage, the works index, the papers index,
the video index, the transcript index, search, the timeline and the channel page
— is read out of `_data/` in a Liquid loop or counted by a build script. No page
types a number that is not counted from there, and
`scripts/test_canonical_57.py` recomputes the same total from the same files.

### The recovery method

The original sites are gone. `asadullahali.com` resolves and serves an
unrelated gambling operation; the WordPress mirror at
`asadullahali.wordpress.com` is still up with its post bodies removed; the
YouTube channel returns "This channel is not available." The corpus was
recovered on **2026-09-27** by **six parallel lanes** — the WordPress mirror,
deleted mirror posts and stub-fills, the Muslim Debate Initiative, a
best-capture re-fetch of `asadullahali.com`, secondary sources and academic
texts, and the video catalogue — then an integration pass moved every verified
item into the repository.

The governing rules, all recorded in the repository rather than asserted here:

* **Verbatim, never summarised.** Recovered prose is reproduced as published.
  Where two copies of a work disagree, the archive keeps the longer one, keeps
  the other as a recorded alternate, and **never adds them together**.
* **Every item records where it came from.** Original URL, the Wayback capture
  timestamp it was recovered from, and the byte-identity proof where one was
  claimed. A capture ID is the identity of a copy.
* **Nothing was obtained by circumventing a paywall, a robots rule or an access
  control.** Where a source was inaccessible, that is recorded as inaccessible.
  The Cloudflare challenge on Academia.edu was not fought. The live
  `asadullahali.com` was contacted **zero times**.
* **What could not be recovered is recorded as missing**, not quietly dropped.

### The review trail

Not a single pass. The work was independently reviewed in three rounds, and each
review's findings and the fix wave that answered them are committed, not just
summarised:

| Round | What it found | Where the record is |
|---|---|---|
| Phase 2 review of the integration commit | 2 Critical, 7 Important, 11 Minor | [`../recovery-log/2026-09-27-review-phase2.md`](../recovery-log/2026-09-27-review-phase2.md) |
| Fix-wave re-reviews, rounds 1 and 2 | 21 findings, all ADDRESSED; then N1 and N2 | [`../recovery-log/2026-09-27-re-reviews.md`](../recovery-log/2026-09-27-re-reviews.md) |
| Phase 3 review of the taxonomy/channel/transcript work | 1 Critical, 7 Important, 8 Minor | [`../recovery-log/2026-09-27-review-phase3.md`](../recovery-log/2026-09-27-review-phase3.md) |

The **C1** finding is the one worth naming in a release note: Phase 3 published
the recount on the works and papers pages while the homepage still published the
old figures, so the site spent a day contradicting itself rather than
contradicting the data. The fix wave reversed it, and the gate was then closed
the only way that keeps working — by making the numbers impossible to type.

The full trail, including the append-only integration log and the per-lane
manifests, is committed at [`../recovery-log/`](../recovery-log/README.md). It
lives in the repository rather than in a scratch directory because an earlier
review raised exactly that as a finding: a 3.2 MB integration commit whose only
provenance was one untracked disk.

### The licence split

Stated once here and in full in [`LICENSE`](../../LICENSE) and
[`NOTICE.md`](../../NOTICE.md):

* **The author's works are not relicensed.** They were openly readable when
  published, which is *availability, not permission*. No open licence was ever
  applied to them by their author and none is applied here. Copyright is his —
  or, for the journal and conference papers, his and his co-authors' and the
  publishers'. Reuse of that prose is governed by the rights holder's terms.
* **The archive's own material is CC BY-NC 4.0.** The `_data/` files, the
  `scripts/`, the Jekyll layouts, includes and stylesheet, the `docs/` research
  trail, and the editorial prose this archive wrote about the material. That is
  the only grant in the repository.
* **One held PDF is genuinely licensable** and is called out as such: *Between a
  Backbone and Ribs* is the author's own CC-licensed deposit on the Internet
  Archive. It is the one paper this archive is permitted to mirror.

Attribution is required, and **crediting this archive alone does not satisfy
it** — the archive is the record, not the author. A citation names the author,
the work, and the capture.

### The no-contact notice

The author has asked not to be contacted, and he keeps a private life. It is
stated in the same words in every place a reader meets it: this file's
`NOTICE.md` §10, linked from the footer of **every** built page; `README.md`
above the contents table; `CONTRIBUTING.md` as its first section; `llms.txt` for
machine readers; and the first entry in
`.github/ISSUE_TEMPLATE/config.yml`, so someone arriving intending to ask how to
reach him is redirected to templates that can be acted on. Requests to contact
him, requests for his details, and invitations to events are not answered and
are not forwarded — the maintainers have no way to put them through. No contact
detail appears anywhere in the repository.

### What is withheld, and disclosed rather than left as a silent gap

A withheld item that is not disclosed is a silent gap, and a silent gap is how
an archive becomes unreliable. Every one is listed in `NOTICE.md` §6:

* **Two personal names** — his legal name and his birth name — withheld at the
  site owner's request. The citations themselves are left intact so they still
  resolve at the publishing institutions. On the three transcript pages that
  carried the birth name, the name is replaced at build time with a visible
  `‖ birth name withheld ‖` marker and the page says how many were replaced and
  why; the raw captures are withheld unedited rather than altered.
* **Three raw caption captures** containing the birth name: untracked,
  withheld unedited, retained on disk because the build and the test suite read
  them.
* **Two PDFs withheld in full**, each keeping its full citation and a link to
  where the text remains available: an IAIS Malaysia book chapter whose public
  provenance could not be verified against any source, and the 24-page IIUM MA
  thesis excerpt, whose page text reproduces personal identifiers of the author
  and of third parties.
* **One held PDF's embedded metadata** cleared field by field, leaving its 63
  pages byte-identical and its page count unchanged.
* **Recovered images are staged but not published.** They sit in the gitignored
  staging tree; the count is an inventory of what was recovered, not a claim
  about what the site serves, and the README says so.

**Do not visit the original domain.** `asadullahali.com` no longer belongs to
him. It is named in `NOTICE.md` §7 as plain text and is never emitted as a
link — making it clickable would defeat the warning. Institutional profiles and
course listings still present it as his official site; if you arrive from one of
those, you are arriving from an outdated reference.

---

## Assets to attach

Two files, both already in the repository, both cut from the same 13 captured
frames of a local `_site/` build. **These are the two to attach** — verified present,
of the right type, and referenced by `README.md` (the GIF is the inline embed)
and by `docs/demo/README.md`.

| File | What it is | Size | sha256 |
|---|---|---:|---|
| `docs/demo/site-tour.mp4` | The full tour. 1440x900, 30 fps, 35.07 s. | 5,517,745 B (5.26 MiB) | `822ba1d6d24c9d3df7db4b80239ea54e7759e1ba5a7b938b8ef22d93eb1da3f2` |
| `docs/demo/site-tour.gif` | A size-capped preview for inline display. 720x450, 6 fps, 24.00 s. | 6,169,014 B (5.88 MiB) | `8845a3277d46e2c0da79b24456f6e9eb552db987eddaf1916123104fa921acb0` |

Verified on 2026-09-28: the MP4 begins with a valid ISO-BMFF `ftyp` box and the
GIF with a `GIF89a` header, so both are intact and neither is a Git LFS pointer
or a truncated upload.

No other binary is a release asset. The five PDFs in `_papers/pdfs/` are already
served from the site at `/papers/<file>.pdf` and do not need attaching.

---

## Suggested release body

Tag: `v1.0.0` · Title: `The Andalusian Project Archive v1.0.0`

> The first tagged release of the archive of the published work of Asadullah Ali
> Al-Andalusi. 72 catalogued written works, 68 video records, 68 published
> machine transcripts, 20 academic papers, 3 announcements, 10 link-outs and 70
> third-party source records; 220 counted items, counted from `_data/` at build
> time rather than typed into any page.
>
> The original sites are gone — one domain has been taken over by an unrelated
> commercial operation and must not be visited or linked. The corpus was
> recovered on 2026-09-27 by six parallel lanes, integrated, and then reviewed in
> three independent rounds whose findings and fix waves are committed under
> `docs/recovery-log/`.
>
> The author's works are reproduced verbatim and are **not** relicensed. The
> archive's own material — the data, the scripts, the site source and the
> documentation — is CC BY-NC 4.0. See `LICENSE` and `NOTICE.md`.
>
> **The author has asked not to be contacted.** See `NOTICE.md` §10.
>
> Attached: the site tour (`site-tour.mp4`, `site-tour.gif`), recorded
> 2026-09-28 in the light theme from a local build of the current commit, after
> the recount. Its captions carry the current figures.
