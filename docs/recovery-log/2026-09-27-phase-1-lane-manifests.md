# Phase 1 lane manifests — counts and provenance

**Exported:** 2026-09-27 · **Plan:** [`docs/superpowers/plans/2026-09-27-full-recovery-v6.md`](../superpowers/plans/2026-09-27-full-recovery-v6.md) (Tasks 1–6) · **Ledger:** `.superpowers/sdd/2026-09-27-full-recovery-v6/progress.md` (rulings R9–R14)

This file records what each of the six Phase 1 recovery lanes fetched and staged, so the
integration commit has a durable provenance trail in git. It is a **summary, not a copy**.
The raw artefacts each lane produced — staged HTML, PDFs, images, capture files — are
multi-megabyte binaries and intermediates that are **not** committed here; they lived in
the gitignored `_staging/` tree and are scheduled for deletion at Task 9.5. What follows
is the per-lane count of every artefact class, the lane's own totals where it published
them, and the path where the full manifest and report can be found.

**Date range covered:** all six lanes ran on **2026-09-27** (manifest generation stamps
range from `09:05:36Z` to `14:33:13+05:30`). Lane sources span the archive's own history:
the WordPress mirror (2010–2021 posts), Wayback captures (2007–2021 enumeration, 2026
retrievals), the live `muslimdebate.org` author archive, and the live YouTube channel as
of 2026-09-27.

**How to read the counts.** `pages` = distinct URLs whose prose was extracted and kept.
`images`/`pdfs` = binary artefacts downloaded. A lane's *deliverable* count is not the same
as its *evidence* count: most lanes kept non-chosen captures as proof that the best
capture really was the best, and those are counted separately below.

## Summary table

| Lane | Staging dir | Report | posts | images | pages | pdfs | videos | Lane files | Lane size |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| F1 mirror | `_staging/mirror/` | [`task-1-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-1-report.md) | 38 | 334 | — | 1 | — | 447 | 72.1 MB |
| F2 deleted | `_staging/deleted/` | [`task-2-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-2-report.md) | 22 | 0 | 22 | 0 | 0 | 180 | 7.1 MB |
| F3 MDI | `_staging/mdi/` | [`task-3-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-3-report.md) | 17 | 0 | 17 | 0 | 0 | 83 | 2.4 MB |
| F4 best-capture | `_staging/best_capture/` | [`task-4-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-4-report.md) | 30 works / 48 pages | 0 | 48 | 0 | 0 | 138 | 11.1 MB |
| F5 secondary | `_staging/secondary/` | [`task-5-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-5-report.md) | 1 IDI text | 0 | 1 | 7 (+4 working copies) | 0 | 98 | 14.4 MB |
| F6 videos | `_staging/videos/` | [`task-6-report.md`](../../.superpowers/sdd/2026-09-27-full-recovery-v6/task-6-report.md) | — | 0 | — | 0 | 239 checked / 11 new | 172 | 37.0 MB |

Every lane manifest is at `_staging/<dir>/MANIFEST.md` with a machine-readable
`_staging/<dir>/manifest.json` beside it. Both were gitignored and are **not** preserved
after Task 9.5; the counts above are the surviving record.

---

## F1 — WordPress mirror (`_staging/mirror/`)

Source: the WordPress.com public API for `asadullahali.wordpress.com` plus the mirror's own
image/PDF CDN. Plain HTTP only; no Firecrawl, no Exa, no live `asadullahali.com`, no
Wayback. Generated `2026-09-27T14:33:13+05:30`.

Lane totals as published by `_staging/mirror/MANIFEST.md`:

| Item | Count | Bytes |
|---|---:|---:|
| Posts — raw API records (`posts/*.json`) | 38 | 1,448,258 |
| Posts — extracted text (`posts/*.txt`) | 38 | 809,178 |
| Images referenced by posts — retrieved | 334 | 68,284,370 |
| Images referenced by posts — NOT retrieved | 3 | 0 |
| &nbsp;&nbsp;of which ijihad comic slides | 22 | — |
| &nbsp;&nbsp;of which ijihad comic cover | 1 | — |
| Mirror-hosted PDFs | 1 | 2,534,058 |
| Evidence files (`evidence/`) | 3 | 37,132 |
| Tooling / intermediates (`_work/`) | 30 | 2,194,372 |
| **Lane total (all files on disk)** | **447** | **75,574,105** |

- **posts 38** — every post the mirror API returned, each with a raw JSON record and an
  extracted `.txt`. Verdicts against the archive's existing local copies: `MIRROR_FULLER` 6,
  `LOCAL_FULLER` 23, `EQUAL` 9, 0 stubs. 14 of the 38 are under 40 words (WordPress stubs).
- **images 334 retrieved, 3 not** — the 3 failures are third-party Photon-CDN URLs, recorded
  in the manifest as unrecoverable. Of the 334, only **285** are distinct image *content*
  (md5); the other 49 are byte-identical duplicates reachable at two URLs each (the CoBlocks
  gallery `src` re-upload and its `data-orig-file` original). Both URLs are kept so every URL
  referenced by a post resolves to a file.
- **pdfs 1** — the mirror's own hosted PDF.
- **The 22 ijihad comic slides + 1 cover** are the entire body of the `ijihad-1` post. See
  "Provenance that is about to be deleted" below.
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`.

## F2 — Deleted mirror posts + stub-fills (`_staging/deleted/`)

Source: Wayback Machine only (`id_` capture form, original bytes, no toolbar). Strictly
serial, ≥1.0 s apart, real browser User-Agent, 4 attempts with exponential backoff. The only
non-Wayback host contacted was `muslimdebate.org` (3 pages), which the brief directed.

| Metric | Value |
|---|---|
| CDX rows, fresh enumeration (`statuscode:200&collapse=digest`) | 1,024 |
| CDX rows, all status codes (control query) | 2,352 |
| unique post permalinks with a 200 capture | 42 |
| — of which still present in the WordPress API (Lane F1's set) | 20 |
| — **absent from the API = deleted** | **22** |
| 200-captures held by those 22 deleted permalinks | 110 |
| recovered — new untracked works | 17 |
| stub-fills | 2 / 2 |
| verifications of already-tracked works | 5 / 5 |
| candidate duplicates staged (muslimdebate.org) | 3 / 3 |
| not found | 0 |
| recovered prose, all 22 posts | 31,631 words |
| non-chosen captures kept as evidence | 47 captures (94 files) |
| extra captures fetched to prove the best-capture choice | 45 |
| total Wayback page fetches, all HTTP 200, 0 failures | 78 |
| `manifest.json` entries | 180 |

- **posts 22** (`_staging/deleted/posts/*.txt`, 22 matching `.html` raw captures).
- **pages 22** plus **47 non-chosen captures** kept as evidence in `cdx/alt_captures/`
  (47 `.txt` + 47 `.html`), plus **3 candidate duplicates** staged from `muslimdebate.org`
  and **2 stub** records in `stubs/`. That is 74 `.txt` and 72 `.html` on disk.
- **images 0, pdfs 0, videos 0.**
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`. Known limitation: the CDX
  brief-mismatch — `who-justifies-terrorism-part-1` and `-2` are one permalink, and
  `the-inhumanity-of-human-rights` is Part 1 only (629 w; no Part 2 exists).

## F3 — Muslim Debate Initiative (`_staging/mdi/`)

Source: **live `https://muslimdebate.org`**, 17/17 pages HTTP 200, retrieved 2026-09-27.
Wayback used only to corroborate author-archive pagination, never as a text source. No
Firecrawl/Exa spend; no request to `asadullahali.com`.

- **pages 17**, each held three ways: `posts/<slug>.txt` (extracted prose),
  `posts/<slug>.json` (crosscheck record, `mdi_json_match=exact`), and
  `posts/html/<slug>.html` (raw fetched source, marked *do not publish*).
- **24,081 words** total. All 17 matched `_data/mdi_articles.json` exactly; 0 byline
  mismatches. 7 of the 17 are under 100 words (captions, not essays).
- **posts/images/pdfs/videos:** 17 prose files, 0, 0, 0. 83 files / 2.4 MB on disk.
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`.

## F4 — `asadullahali.com` best-capture re-fetch (`_staging/best_capture/`)

Source: Wayback Machine only — the live `asadullahali.com` is domain-hijacked (since July
2024, 15 spam captures in the pool) and was never contacted.

| metric | value |
|---|---|
| CDX rows enumerated (status 200, matchType=domain) | 4,723 |
| unique original URLs | 1,094 |
| unique normalised URLs (scheme/`:80`/trailing-slash merged) | 1,009 |
| distinct-digest captures (collapse=digest) | 3,872 |
| evolution candidates (>1 distinct capture) | 619 |
| canonical content URLs taken to fetch | 346 |
| distinct captures fetched (serial, ≥0.55 s apart) | 2,403 |
| HTTP failures / rate-limits during fetch | 0 / 0 |
| **pages selected (≥100-word prose capture)** | **48** |
| — of which distinct works (`is_work`) | 30 |
| — AMP duplicates of a selected work | 9 |
| — WordPress comment-feed pages (not works) | 4 |
| — site boilerplate / course shell / homepage | 1 / 1 / 1 |
| — index listing + REST API dump (not prose) | 1 / 1 |
| **URLs skipped (no capture reached 100 words)** | **298** |
| selected words recovered (all pages) | 218,881 |
| selected words in distinct works | 120,938 |
| works whose fullest Wayback capture beats the archive's current copy | 8 |
| works that look NEW vs `_data/canonical_57.json` | 0 |
| fetch wall-clock | 58.6 min for the 2,403-request fetch |

- **pages 48** (`pages/*.txt` + 48 raw `.html`), of which **30 are distinct authored works**.
- **The bimodal skip pattern** the lane recorded: of the 298 skipped URLs, 298 sat at 0 words
  and 0 sat in the 1–99 band — they are prose-free WordPress attachment pages, not thin
  essays. The brief's expectation of ≈180 pages was 6× off; the lane's max-bytes rule would
  otherwise have pulled the hijacker's casino spam.
- **0 new works.** The lane's whole value was 8 fuller versions of works already held
  (+16…+282 w) plus 22 that reproduce the already-recorded capture exactly.
- **images/pdfs/videos:** 0, 0, 0. 138 files / 11.1 MB on disk.
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`.

## F5 — Secondary sources, academic texts, link-outs (`_staging/secondary/`)

Built `2026-09-27T09:08:22Z`. Every row below carries a `sha256` in the lane manifest.

- **pdfs 7** in `papers/`: `iium-thesis-islamic-intuitionism.pdf` (24 pp),
  `gender-equality-islam-and-law.pdf` (17 pp), `gender-equality-islam-and-law-japanese.pdf`
  (20 pp), `the-rise-and-decline-of-scientific-productivity.pdf` (18 pp),
  `architects-of-civilisation-sallahuddin-ayubi.pdf` (5 pp, **SOURCE URL UNVERIFIED**),
  `between-a-backbone-and-ribs.pdf` (63 pp, archive.org CC), and
  `deconstructing-contemporary-atheist-thought.pdf` (31 pp, AMJA). Four further working
  copies sit in `_work/` (11 PDF files on disk in total) — they are the download-side twins
  the sha256 comparison ran against.
- **pages 1** text article: `idi_apostasy.txt`, 2,272 w, live
  `islamicdiscourseinitiative.com` capture. Filed as a **Category-A work, not a paper**
  (ledger ruling R4).
- **Register files:** `papers.csv` 24 rows (8 oa / 15 restricted / 1 dead),
  `linkouts.json` 10 rows (1 conversion-story **metadata only, body never fetched**;
  9 Yaqeen link-outs), `secondary_sources.csv` 69 rows, `dois.csv` 5 DOIs.
- **images/videos:** 0, 0. 98 files / 14.4 MB on disk.
- **Known restrictions recorded, not worked around:** Academia.edu is Cloudflare-blocked
  (403 on every attachment endpoint — the probe is kept as evidence), so 0 of 13
  Academia items were downloaded; `10.52282/icr.v6i2.333` is dead (DNS); three `10.12816`
  DOIs land on Kezana with `IsOpenAccess=false`.
- **A provenance correction worth keeping:** `iium_thesis.pdf` was mis-titled in prior
  research — it is *Islamic Intuitionism*, not an "IIUM thesis" on some other subject. The
  sha256 in this lane's manifest is the proof.
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`.

## F6 — Video catalogue + mirror mapping (`_staging/videos/`)

Generated `2026-09-27T09:45:42Z`.

| Deliverable | Rows | Purpose |
|---|---:|---|
| `verify.csv` | 239 | every candidate id: `alive`/`dead`, live title, `author_name`, `source_of_discovery` |
| `videos_new.json` | 11 | new catalogue entries, `transcripts: 0`, `kind` set on each |
| `mirrors.json` | 13 | live re-uploads mapped to a baseline video (strict rule: normalised-exact title **and** duration within 60 s) |
| `unmapped_mirrors.json` | 12 | live Andalusian candidates NOT mapped, each with a reason |
| `excluded_unrelated.json` | 72 | live candidates with no evidence of Andalusian authorship (counted nowhere) |
| `baseline_status.json` | 29 / 102 | liveness of all 68 baseline videos + the full dead list |
| `baseline_duplicates.json` | 12 | pre-existing double count inside the 68-entry baseline (not created here) |

- **videos 239 candidate ids checked** via YouTube oEmbed (serial, 0.4 s apart, **0 errors**):
  **137 alive, 102 dead**. Sources: 49 Wayback raw captures of channel/playlist/mirror pages,
  10 raw captures of YouTube watch pages (duration only), 6 CDX enumerations.
- **11 new entries**, not the ~53 the brief expected: 7 `appearance`, 4 `clip`, all
  `transcripts: 0`.
- **13 mirrors mapped, 12 left unmapped.** I2 later re-verified and **promoted all 12** on
  Δ<1 s duration evidence (ledger ruling R14) — including 3 pairings F6 never surfaced.
- **The 12 baseline double-counts are flagged, not fixed here** — removing a double-counted
  entry is a counting decision, and it was made at Checkpoint 1 by the site owner, not by
  the lane.
- **The impostor channel** `@andalusianproject6093` holds the same UC id with 0 videos.
  `_data/channel_facts.json` records `do_not_link_uc_id: true` and carries no
  `youtube.com/channel/…` URL at all. Never link it.
- **posts/images/pdfs:** 0, 0, 0. 172 files / 37.0 MB on disk.
- **Verdict class recorded in the ledger:** `DONE_WITH_CONCERNS`.

---

## Controller verification of all six lanes

Every lane manifest row resolves to a real file. `deleted` and `mdi` use repo-root-relative
paths in their manifests, which is a valid convention, not a broken link. The 21 rows of
`secondary` all resolve. The 5 missing items in the `videos` manifest are non-deliverable
discovery `.raw` captures. An empty nested `_staging/_staging/mdi` directory was removed. No
lane wrote outside `_staging/`, verified two ways: by mtime containment per lane, and
git-independently — only `_staging/` and `.superpowers/` were ever untracked or ignored.

## Provenance that is about to be deleted

`_staging/` is scheduled for deletion at Task 9.5. Three things recorded above exist **only**
there, and this file is their surviving trace:

1. **The `ijihad-1` NO-MATCH evidence.** The `mapping_note` on the `ijihad-1` work row says
   the post *"is a 22-slide comic reboot (wordpress comments verify)"*. The F1 capture
   `_staging/mirror/posts/ijihad-1.json` proves it directly and more strongly than the note
   claims: `content.rendered` is 28,245 characters of markup that yields **zero characters of
   prose** after tag-stripping — the entire post body is one `wp-block-coblocks-gallery-stacked`
   element holding `slide1.png` … `slide22.png` (each repeated 9× for the responsive `srcset`),
   plus a `comiccover1.png` featured image. A post with no text cannot be matched to the
   iJihad Ep. 3 "Sargonic Suicide" video (4,606 s) by text, so the mapping stays unresolved
   and the work stays `wayback_only` with a stub. **After Task 9.5 the only surviving evidence
   for that verdict is this paragraph plus the `mapping_note` in `_data/canonical_works.json`.**
2. **The 47 non-chosen F2 captures** kept specifically to prove each chosen capture was the
   best of its 110 candidates.
3. **The per-capture rejection reasoning in `_staging/best_capture/selection.csv`** (2,403
   fetches) and `skips.csv`. This is what makes the bimodal 298-skip pattern auditable.

## What is deliberately NOT here

- The multi-megabyte raw artefacts: staged HTML (F2, F3, F4), 334 images (F1), 11 PDFs (F5),
  67 `.raw` Wayback captures (F6). **~144 MB across the six lanes.** Counts and provenance are
  recorded instead; the bytes are not in git.
- The lane `MANIFEST.md` / `manifest.json` files themselves, and the lane reports under
  `.superpowers/sdd/2026-09-27-full-recovery-v6/task-{1..6}-report.md` — that tree is
  gitignored (`.superpowers/sdd/.gitignore` contains `*`). See
  [`README.md`](README.md) in this directory for what *was* exported and why.
- The two 3.2 MB / 909 KB review diffs (`review-7e32c28..9b431ef.diff`,
  `review-9b431ef..f0ba4e7.diff`) and the 226 KB working-tree diff.
