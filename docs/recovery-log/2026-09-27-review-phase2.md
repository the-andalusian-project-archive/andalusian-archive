# Independent review — Phase 2 integration commit `7e32c28` → `9b431ef`

**Reviewer:** independent reviewer (did not write any of this)
**Scope:** 127 files, 3.2 MB diff. Spec = `.superpowers/sdd/2026-09-27-full-recovery-v6/task-7-brief.md`
(+ plan `docs/superpowers/plans/2026-09-27-full-recovery-v6.md` Global Constraints, ledger
`.superpowers/sdd/2026-09-27-full-recovery-v6/progress.md` rulings R0–R18).
**Method:** read the diff file-group by file-group; verified the *committed blobs* (not the
working tree) with `git show`/`git ls-tree`; re-ran the 4 suites; diffed every recovered text
against its staged original in `_staging/{mirror,deleted,mdi,best_capture,secondary}`; simulated
the new transcript gate against mutated data. No file in the workspace was modified; no
state-changing git command was run.

---

## Spec compliance

### I1 — text-data integrator (brief items 1–14)

| # | Item | | Evidence |
|---|---|---|---|
| 1 | 9 named fuller-version adoptions, diffed, never summed | ✅ | All 9 `_posts` files carry `provenance` + `recovered_text_words`; each equals **exactly one** candidate, never a sum: `reviewing-haqiqatjou` 68903 = mirror, `backbone-ribs` 20037 = mirror, `archetype` 2167 = F4, `narrative` 4534 = mirror, `rationality-p1` 5646 = F4, `rationality-p2-2` 5939 = mirror, `malaysias-tiger` 3826 = F4, `pvp-part-1` 3661 = MDI, `rise-and-decline` 1601 = F4. Token-diff of each file against its winning capture: body identical, only the staged `TITLE:/SLUG:/DATE:/MODIFIED:` header replaced by an `# Title` heading. Winners: mirror 5 · wayback 3 · mdi 1. |
| 2 | `adam-is-no-myth`: no merge, 6 token welds repaired | ✅ | `_posts/2020-08-07-adam-is-no-myth.md` — 0 of 7 welded tokens remain (`hispaperfound`, `fromThe`, `Delusionno`, `torefute`, `theOxford`, `well.Nidhal`, `Jalajel’spodcast`); the 7th (`Jalajel's podcast`) is a real 7th site, reported not hidden. Word delta 2050→2058 = 8 inserted spaces, no word changed. |
| 3 | 15 net-new works, `status: found`, `wayback_url` + provenance | ✅ | 15 rows in `_data/canonical_works.json` carry `provenance`+`local_post`+`recovered_text_words`; all 72 rows carry `wayback_url`; all 47 found works resolve 1:1 to a distinct `_posts` file (verified, no date collision among found works). 15/15 texts byte-identical to `_staging/deleted/posts/*.txt` after whitespace normalisation. |
| 4 | 2 stub-fills, `the-inhumanity-of-human-rights` lost→found | ✅ | `_data/lost_works.json` 2→1; `the-inhumanity-of-human-rights` is `found` (635 w file / 629 w recovered) and `library-take-down-notice` `wayback_only`→`found` (221 w / 216 w). Both texts byte-identical to staging. *Wording note — see Minor M4.* |
| 5 | MDI: 17 staged texts stored, row count stays 17 | ✅ | `_data/mdi_articles.json` = 17 rows, 17/17 with non-empty `text`, **byte-identical** to `_staging/mdi/posts/*.txt`; `words` metadata matches the stored text exactly on all 17; 17 `_articles/mdi-*.md` pages generated; 7 sub-100-word captions kept with an on-page note. |
| 6 | F4: 0 new works, 8 alternates, 22 recorded-not-churned | ✅ | 0 new slugs added. All 8 named alternates present with capture id + word count in `alternate_note` (`illogical-critques`, `narrative`, `supporting-happymuslims`, `boko-haram`, `whataboutery`, `rationality-p2-2`, `structure-of-scientific-productivity`, `reviewing-haqiqatjou`). The 22 no-churn cases are ⚠️ unverifiable from the diff. |
| 7 | `bibliography.json` FIRST, then papers 18→20 | ✅ | `_data/bibliography.json` = 24 papers rows (8 oa / 15 restricted / 1 dead) + 2 conference reports + 5 DOIs = 29 records, all `papers.csv` rows present, restricted/dead never counted as held texts. `_data/papers.json` 18→20 with 6 rows holding a real file. All 7 PDFs verified `%PDF-` header + `%%EOF` trailer + page count matching metadata, and byte-identical (sha256) to `_staging/secondary/papers/`. |
| 8 | `linkouts.json`: conversion story metadata-only + 9 Yaqeen link-outs | ✅ | `_data/linkouts.json` = 10 rows. The `conversion_story` row has `metadata_only: true`, `words: null` **on purpose**, a single neutral sentence, Wayback URL + 22 captures + 1 alternate reprint — **no body text anywhere in the repo** (grep-verified). 9 `yaqeen_paper` rows, link-out only. |
| 9 | `secondary_sources.json` 52→69, mojibake repaired | ✅ | 69 rows, all `counted_as_content: false`, no duplicate URLs, no missing URLs. All 7 named mojibake titles verified repaired (`[Video] Refuting The Masked Arab (2)`, `Lecture: 'Islam & Terrorism' […]`, the Arabic `بناء الإنتاج العلمي…`, the Turkish `İSLAM MEDENİYETİNDE…`, `The Fiqh of Ḥalāl and Ḥarām`, `Clinical Applications of Islāmic…`, `Al Balāgh Online ʿĀlimiyyah…`). |
| 10 | `lost_works.json` 2→1 | ✅ | 1 row, with a `reason` naming every lane that failed. |
| 11 | IDI "Apostasy: Beyond the Rhetoric" as a work, not a paper (R4) | ⚠️ | Filed as `_posts/2018-05-22-apostasy-beyond-the-rhetoric.md`, work row present, correctly **excluded** from `papers.json`. *But* the cross-reference and the rendered page have defects — Important I3. |
| 12 | Rename `canonical_57.json` → `canonical_works.json` across all reference sites | ⚠️ | Done in `_data/` and `data/` (git records the rename, sha256-verified copy→delete). All **live** code updated: 6 scripts, `articles.md` (2), `timeline.md` (1), `index.md` (1 comment), `README.md`, `search.md` (2, including the client-side `fetch`). `git grep canonical_57 9b431ef` returns hits **only** in `docs/superpowers/plans/*` (19), `.superpowers/sdd/*` (29, gitignored) and `scripts/test_canonical_57.py:1` (the filename, which the brief permits). *Brief listed "plan docs" as a site to update; 2 plan files left unchanged by design — see Minor M6.* |
| 13 | Transcript preservation, 0 deletions, honest gate restated | ⚠️ | 0 deletions — verified. `transcript_coverage.json` 69→59; 10 re-parented onto surviving twins' `alternates` with `file`+`lines`+`title`+`captions`+`source`+`lang` all intact; 2 (`xhnU-1dNi3I`, `G47Stp3pLss`) kept in place flagged `superseded: true` (23,168 and 15,048 lines). Gate restated 68/68 → 56/56 + 11 catalogue-only, old→new numbers stated in the report. *But the new anti-vanishing guard is ineffective — Important I1.* |
| 14 | Test expectations updated, no unrelated assert weakened | ⚠️ | 21 changes across 6 files, all listed with before/after in I1 §12. Verified independently: 4 suites pass. Two shape asserts were *generalised* rather than renumbered (`len(set(ids)) == 68` → `== len(ids)`, same for case-colliding, plus `mirror_urls` list check) and `assert len(yt_only) == 12` was **deleted with nothing replacing it** — Important I5. The anti-vanishing guard is added but weak — Important I1. |

### I2 — media-data integrator (brief items 1–8)

| # | Item | | Evidence |
|---|---|---|---|
| 1 | `superseded_videos.json` written FIRST, 12 rows, full record + twin + reason | ✅ | 12 rows in F6 order; every row has `id`, `title`, `source`, `youtube_url`, `live{}`, `duplicate_of_baseline_id`, `duplicate_of_archive_url`, `match_basis`, `duration_evidence`, `reason`, `disposition` and a complete `superseded_record` (7 keys each). All 12 titles preserved. The 2 no-twin rows carry `candidate_twin` + `candidate_twin_evidence` + `candidate_twin_confidence` and were **not** merged on title similarity. |
| 2 | Remove the 12, attach as `mirror_urls` on the twin, 68→56 | ✅ | Commit `videos.json` = 67 rows; 0 of the 12 superseded ids remain; 10 of the 12 URLs attached to their twin (10 URLs on 9 entries, `NyAVl7RsEOs` takes two). The one non-obvious move — F6's `DctcuGidoUI`, mapped to the removed `D2t0idkAqjA`, re-homed to `7KBCENktOOU` — is documented and count-neutral. |
| 3 | Append F6's 11 new entries with `kind` + `transcripts: 0` → 67 | ✅ | 11 entries, all `kind` ∈ {appearance 7, clip 4}, all `transcripts: 0`, all `mirror_urls` present. No `kind` invented for any other entry. F6's field order preserved. |
| 4 | Promote the 12 parked mirrors, re-verified, evidence recorded | ✅ | All 12 promoted on Δ<1 s duration evidence re-derived from F6's own on-disk data; 3 pairings F6 never surfaced are recorded as I2 re-verification with their deltas; the loosest is `-19Fq0e4y8M` at Δ0.99 s and is flagged as the first to reverse. `unmapped_mirrors.json` = `[]` (verified). |
| 5 | `mirror_urls: []` on every entry, schema grows only | ✅ | 67/67 carry the key, always last, as a list of URL strings; 35 URLs across 30 entries; no duplicate URL; no URL equals its own id. The 56 archive.org rows keep their original 12 keys in the original order. |
| 6 | `channel_facts.json` timeline + do-not-link + rejected 585 K claim | ⚠️ | 12 capture-dated timeline rows, every one traceable to a `_staging` file; subscriber series 190 → 6.97 K → 11.2 K → 14.4 K → 15.7 K; live check attributed to `fetched_by: "controller"`; the 585 K figure is **rejected with its proof** (sidebar `navigationEndpoint` → `UC3vHW2h22WE-…`) instead of being written; `do_not_link_uc_id: true` and **no `youtube.com/channel/…` URL anywhere in the file** (grep-verified). *The handle is labelled `is_his: null`, not "NOT his" — Important I4.* |
| 7 | Do not touch `scripts/`, `transcript_coverage.json`, or any transcript file | ✅ | `git diff 7e32c28 9b431ef -- scripts/ transcript_coverage.json` shows changes only from I1's lane; `.firecrawl/transcripts/*.vtt` untouched (all 12 `cap-<id>.en-orig.vtt` still on disk). I2 reported the exact one-line `test_search_sync.py` fix instead of applying it, as instructed. |
| 8 | Sync `data/videos.json` | ✅ | Byte-equal in content to `_data/videos.json`; `test_search_sync` confirms. |

### Both

| Item | | Evidence |
|---|---|---|
| Integration log written | ✅ | `.superpowers/sdd/…/integration_log.md`, 190 lines, one line per work `slug → source lane → verdict → destination`. **But it is untracked** — `.superpowers/sdd/.gitignore` contains `*` (Minor M7). |
| No git commands / no subagents | ✅ | Consistent with the file list and the reports. |
| 4 suites + `bundle exec jekyll build` green | ⚠️ | All 4 suites pass. Build is green. **But no suite or gate checks `_videos/`, and `_videos/` was never regenerated for this commit — Critical C1.** |
| Site pages: no count text silently updated | ✅ | `git diff 7e32c28 9b431ef -- index.md articles.md timeline.md search.md README.md` contains **8 changed lines, all of them the `canonical_57` → `canonical_works` rename**. `index.md` still shows 57 / 68 / 18 / 203 and the `= 203` comment. The Task 9 approval gate is intact. |
| Privacy: conversion-story body text absent | ✅ | Grep for the birth name (redacted at publication time as `‖ birth name withheld ‖`) over 1,907 text files: 0 hits in any `_posts`/`_articles`/`_data`/`data` file. The only hits are pre-existing in `.firecrawl/transcripts/cap-7KBCENktOOU.en-orig.vtt` — his own public "My Story" video, committed before this work. This finding was accurate as written; the three transcript pages built from these captures have since had the name substituted at document-build time, at the site owner's request — see NOTICE.md §6.2. |
| Privacy: no API keys | ✅ | `.env` is gitignored (`.gitignore:9`) and is not in the diff. No `fc-`/`sk-`/`AIza` secret appears in any tracked file. |

### Suite re-run (read-only)

```
test_no_junk: ALL PASS (54 files clean)
TEST_PASS works=72 captures=87 notices=3 found=47 wayback_only=24 lost=1 (1 audited exception)
test_search_sync: ALL PASS   (videos 67, papers 20, works 72, 3 sync checks, blog_posts 87, excerpt/keyword)
test_transcripts: ALL PASS  (56/67 + 11 catalogue-only + 10/12 re-parented + 15 joins)
```

All 4 counts asserted by the suites are true of the committed data (I re-derived every one from
the commit's blobs, not from the suites).

---

## Data integrity findings

### Critical

**C1 — `_videos/` was never regenerated: the commit ships a 67-video catalogue against 56 video pages.**
`_data/videos.json` in `9b431ef` has 67 rows, but `git ls-tree -r 9b431ef -- _videos` returns the
same **68** files as the base `7e32c28`. All 12 superseded ids still have a page
(`_videos/2tsI80MDUOI.md`, `_videos/G47Stp3pLss.md`, `_videos/xhnU-1dNi3I.md`, …) and the 11 new
entries have **none** (`_videos/vLkE81ZCMVs.md`, `_videos/EJLSAA_w4PY.md`,
`_videos/s_BnmOrVaTg.md`, … are MISSING).
Why it matters: `search.md:138` builds `/videos/<id>/` links from `data/videos.json`, so **11 of
the 67 video search results are dead links** at this commit; conversely 12 videos that were
removed from the catalogue remain publicly openable at their old URLs. Nothing catches it:
`test_no_junk.py` globs `_posts` only, `test_transcripts.py` checks `_articles` page existence
only, and `videos.md` iterates `site.data.videos` so its own cards look right.
I2 predicted this in its report §8 and correctly noted `clear_md(VIDEOS_DIR)` prunes it on the
next run — but nobody ran it before the commit, and the ledger's controller verification
("site pages changed rename-only", "PDFs are served") never looked at `_videos/`.
Fix I would make: `python -B scripts/build_collections.py`, `bundle exec jekyll build`,
`git add _videos/`, and add `assert len(list((base/"_videos").glob("*.md"))) == len(videos)` to
`test_transcripts.py` so a catalogue/collection divergence can never be committed again.

**C2 — `files_extra` vs `additional_files`: a held PDF is silently dropped and the page's own note points at a key that does not exist.**
`_data/papers.json` id 7 stores the Japanese translation under **`files_extra`**
(`_data/papers.json:141`), while the new builder code reads
`p.get("additional_files")` (`scripts/build_collections.py`, `build_papers()` — the
`for extra in p.get("additional_files") or []` loop and the `additional_file:` front-matter
emitter). The branch never fires: `any("additional_files" in p for p in papers)` is `False`.
Consequence: `gender-equality-islam-and-law-japanese.pdf` is in `_papers/pdfs/`, is committed,
and is served at `/papers/gender-equality-islam-and-law-japanese.pdf` — but appears in no page
front matter, no page body and no link anywhere on the site. `_papers/gender-equality-islam-and-law.md:15`
even says *"A Japanese translation is held alongside it (see additional_files)"*, pointing the
reader at a field that does not exist.
Fix I would make: rename the key to `additional_files` in `papers.json` (one edit) and re-run
`build_collections.py`; or accept both names in the builder. Either way, add a builder assert
that every `*.pdf` in `_papers/pdfs/` is named by some paper row.

### Important

**I1 — the new "transcript text never vanishes" guard does not actually check the text.**
`scripts/test_transcripts.py:78-92` builds `reparented` from `alt.get("video_id")` only, and the
per-superseded branch tests *row presence* and the `superseded` flag — never `file`, `lines` or
`captions`. I simulated the exact check against a mutated copy of the committed
`transcript_coverage.json` in which `file`, `lines`, `captions` and `title` were nulled on all 10
re-parented `alternates` entries **and** both kept-in-place rows: **the check still returns 0
failures.** All 12 superseded transcripts could be emptied and the suite would stay green, while
the brief's item 13 requirement is literally "**Never delete transcript text**" and the test's own
docstring claims to enforce it.
Fix I would make: after the reachability loop, assert for every `alternates` entry
`a["file"] and a["lines"] and a["captions"]`, that `base/".firecrawl/transcripts"/a["file"]`
exists, and that its line count equals `a["lines"]`; same for the `superseded` top-level rows.

**I2 — `total_content: 219` double-counts MDI rows that are also Category-A works, and the commit's own generated page claims the opposite.**
`_data/content_index.json` publishes
`"72 works + 67 videos + 20 papers + 17 MDI + 9 Yaqeen + 33 AlBalagh + 1 interview = 219"`, and
`scripts/build_content_index.py` now *computes* that string so it can never drift. But
`build_mdi_pages()` writes into every one of the 17 generated pages:
*"Where the same essay is also catalogued as a Category-A work (the `prophets-vs-pedophiles`
series) it is not counted again."* At least **9 of the 17** MDI rows are the same essay as a
counted work — `naked-kings-in-the-information-age`, `islam-terrorism`,
`do-muslim-women-need-feminism-debate`, `withoutevidence2`→`…part-1`,
`the-rationality-…-part-1`, `towards-litter-reduction-…`, `still-colonised-…`,
`extraordinary-claims-…`, `boko-haram-…` — and by ruling R9 the three
`religion-vs-paedophilia-*` rows are the `prophets-vs-pedophiles` parts, so up to **12 of 17**.
Six of those essays are now published at two URLs (`/articles/<work>/` and `/articles/mdi/<slug>/`).
The double count predates this commit, but this commit is what made the MDI text local (so the
duplication became material), blessed the number in a computed formula, and added an explicit
sentence asserting the opposite.
Fix I would make: add `counted_as_work: false` + `duplicate_of: <work-slug>` to the overlapping
`mdi_articles.json` rows, subtract them from the formula in `build_content_index.py`, and settle
it **before** Task 9's recount so 219 is not carried forward.

**I3 — `apostasy-beyond-the-rhetoric`: a live third-party URL behind a "Wayback Machine" label, a false "Original site" line, and a one-directional cross-reference.**
`_articles/apostasy-beyond-the-rhetoric.md:20-22` renders
`- [Wayback Machine](https://www.islamicdiscourseinitiative.com/apologetics/apostasy-beyond-the-rhetoric/)`
— a live IDI page, not a Wayback capture — followed by *"Original site: asadullahali.com (no
longer online)"*, which is wrong: this text was never on asadullahali.com. The canonical row's
`alternate_note` claims *"the live URL is recorded in both `wayback_url` and `original_url`"*
but the row has **no `original_url` key**, and it has **no `alternate_urls` at all**, while
`naked-kings-in-the-information-age` does carry the IDI URL. I1's report §9 states "Both rows now
carry the other's URL in `alternate_urls`" — that is false.
Fix I would make: relabel the link "Original (live; no Wayback capture was staged)", correct the
"Original site" line to the Islamic Discourse Initiative, add `original_url` to the row, and add
`naked-kings-in-the-information-age` + its permalink to apostasy's `alternate_urls`.

**I4 — `channel_facts.json` records `is_his: null` where the brief says "Mark the handle as NOT his".**
`_data/channel_facts.json` `do_not_link[0]` carries `"is_his": null` and
`"is_his_meaning": "unknown - deliberately not asserted in either direction"`. The *operational*
rule the brief wanted is fully encoded (`marker: "DO NOT LINK - never link this handle"`,
`channel.do_not_link_uc_id: true`, and no `youtube.com/channel/…` URL anywhere in the file), and
I2's epistemics are more defensible than the brief's letter — a capture records a channel's
state, not its operator. But the brief's literal instruction is unmet, and it was met silently
rather than by a recorded ruling.
Fix I would make: one ledger line (R19) recording the deliberate deviation and why, so the next
reviewer does not re-litigate it.

**I5 — a video-shape assert was deleted with nothing replacing it.**
`scripts/build_collections.py` previously asserted `len(yt_only) == 12`; the commit deletes it
and adds no replacement, while keeping only generic uniqueness checks. Consequence: the
`youtube_not_archived` label branch that `videos.md:31` drives ("Archive.org" vs YouTube) now has
no gate at all, and `videos.md:31` still labels **every** card "Archive.org" from
`video.archive_url` — which is a YouTube URL for all 11 new entries. I2 flagged the label; nobody
acted, because no test covers the branch.
Fix I would make: assert `len(yt_only) == sum(1 for v in videos if v.get("kind"))` (or an
explicit expected value) so the branch's population is pinned.

**I6 — the commit is already stale: 87 dirty paths, 4 data files and 3 scripts modified but uncommitted.**
`git status` after `9b431ef` shows `_data/videos.json` (**68** rows), `data/videos.json`,
`_data/superseded_videos.json`, `_data/transcript_coverage.json`, `_data/channel_facts.json`,
`scripts/build_collections.py`, `scripts/test_search_sync.py`, `scripts/test_transcripts.py`
modified, plus 11 untracked `_videos/*.md` and 12 uncommitted `_videos/*.md` deletions. The drift
is a documented post-Checkpoint-2 **user decision**: `G47Stp3pLss` "My Conversion Story"
restored as a distinct counted video (with a machine-readable `duplicate_pairing_rejected`
block), and `xhnU-1dNi3I` attached as a `mirror_urls` entry on `vJRfL4Kal20`.
Why it matters for this review: the commit's headline number (67) and the ledger's "controller
verification" are no longer the repository's state, and the suite output above reflects the
drift rather than the commit. I verified the commit's own blobs separately (§Spec compliance) and
they are internally consistent — but nothing should be built on 67 until this is committed.

**I7 — `linkouts.json` records provenance that will dangle, and counts 9 rows of which 6 have no size.**
`_data/linkouts.json:36,49,62,75,88,101,114,127` set `words_source` to
`"_staging/mirror/posts/…"` or `"not staged yet; word count is owned by the F1 mirror lane"`.
`_staging/` is deleted after Phase 4 (plan Task 9.5), so 8 of the 9 Yaqeen rows will point at
nothing. `_data/yaqeen_papers.json` has **no** `words` field on any of its 9 rows, so
`linkouts.json` can only supply 2 of 9 — yet `build_content_index.py` adds `yaqeen = 9` to the
published total.
Fix I would make: replace `words_source` with durable provenance (`url`, `wayback_capture_count`)
or drop the key, and state in the formula that Yaqeen is a row count with unknown sizes.

### Minor

- **M1** `scripts/sync_search_data.py:9-11` docstring still says `_data/videos.json (68)`,
  `_data/papers.json (18)` and "Search defaults to works (57)" — the same class of stale literal
  I1 removed from `build_content_index.py`. Fix: 68→67, 18→20, 57→72.
- **M2** `README.md:110` still reads `python scripts/test_search_sync.py (68/18/57 asserts)`; the
  asserts are now 67/20/72. Fix: one line.
- **M3** `search.md:37` and `README.md:114` still say "the 57 honest works" in files this commit
  already touched. The number itself is Task 9's; the stale mention is not.
- **M4** Brief item 4 says "extend the existing stubs", but neither `the-inhumanity-of-human-rights`
  nor `library-take-down-notice` had an existing `_posts` file at `7e32c28` (both were
  `lost`/`wayback_only` with no local text), so these are **new** files, not extensions. The
  outcome is right; I1's report wording ("extend the existing stubs") is not.
- **M5** 5 of the 11 new video entries carry `duration: ""` (empty string) rather than `null`
  (`En8F38ChvvE`, `TTGJPneVR_w`, `dsMWdlzzfMk`, `s_BnmOrVaTg`, `vI3Jz-OSH54`); every other row
  uses a numeric string or omits the key. `duration_source` says "unknown (no Wayback capture)",
  which is honest, but the empty string is a schema smell that any duration formatter will trip on.
- **M6** The adopted captures lose the `>` blockquote markup present in the previous local
  captures (visible in `_posts/2014-04-30-the-narrative-behind-happymuslims.md`,
  `_posts/2020-01-23-backbone-ribs.md`), so quotations now render as plain paragraphs. Words are
  unchanged — this is the source extractor's plain-text output, not a prose alteration — but it is
  a visible formatting regression on 4 files. Fix: re-add `>` on the affected runs, or note it.
- **M7** `docs/superpowers/plans/2026-09-06-57-list-honest-counts.md` still names
  `canonical_57.json` in 9 places. Leaving the 2026-09-27 plan alone is right (rewriting it would
  destroy the spec), but the 2026-09-06 plan could take a one-line forward pointer. Brief item 12's
  "plan docs" is therefore only partially met.
- **M8** `.superpowers/sdd/.gitignore` contains `*`, so `integration_log.md` (190 lines), both
  integrator reports, the brief and the ledger are all **untracked**. Deliberate, but it means the
  entire evidence trail for a 3.2 MB integration commit lives on one disk with no history. Consider
  a `docs/recovery-log/` export at Phase 4.
- **M9** 52 of the 69 `secondary_sources.json` rows keep `origin: "derived_52"`, a marker that now
  describes a 69-row file. Fix: `derived_52` → `derived` or `f5_csv`.
- **M10** `recovered_text_words` is absent from all 9 adopted rows in `canonical_works.json`
  (it lives in the `_posts` front matter, where all 9 values are correct and match the staged
  source exactly). Not a data problem, but the canonical list — the thing the site counts from —
  carries no adopted-from evidence, so the brief's item-1 diff record is only in the reports.
- **M11** I1's report is internally inconsistent about its own rename scope: §1 row 12 says
  "13 files touched", §10 numbers 14. Cosmetic, but the brief's report contract asks for
  "files touched".

---

## ⚠️ Cannot verify from the diff

1. **Whether each of the 9 adopted texts is genuinely the same work as the local copy it replaced.**
   The token evidence is strong (body identical modulo whitespace and token welds; only 2 labelled
   appendices added; 5/5 image references retained; the one superseded sentence in
   `reviewing-haqiqatjou` preserved verbatim in an appendix) — but "same work, later revision" is
   an editorial judgment that needs a human read of the 14,607-word delta.
2. **The 12 duration-based mirror promotions.** `-19Fq0e4y8M` (Δ0.99 s), `6BpJxBdJtY4` (Δ0.63 s)
   and `ZnNAaPy-mN0` (Δ0.58 s) were re-derived by I2 itself, not by F6, and rest on duration plus a
   title judgement rather than the strict title rule. I cannot confirm from the diff that they are
   the same recording.
3. **F4's "22 of 30 reproduce the recorded capture exactly (recorded, not churned)".** I verified
   the 8 alternates exist with capture ids and word counts; confirming the 22 no-churn cases
   requires re-running F4's `selection.csv` join.
4. **Whether `xhnU-1dNi3I` and `G47Stp3pLss` are duplicates of `vJRfL4Kal20` / `7KBCENktOOU`.** No
   duration evidence exists for either in any capture. The commit's choice (remove, count nowhere,
   preserve the record, surface to a human) is the conservative one; the working tree has since
   reversed it by user decision, which is exactly the right process.
5. **Licence/attribution for the 7 now-published PDFs.** R16 defers the per-file licence line to
   Task 8a, but the files are already in `_site/papers/`. `architects-of-civilisation-…` is
   published with `file_source: null` and a "SOURCE URL UNVERIFIED" note — correct and honest, but
   it is a PDF of unknown provenance now publicly served.
6. **Whether the 2023 channel re-registration was by him.** `channel_facts.json` correctly declines
   to say, and its reasoning (a UC id is not transferable between accounts, so same account ≠ same
   person) is sound. Nothing in the captures can settle it.
7. **`total_content: 219` as a number.** Beyond the MDI/works overlap (Important I2), the 9 Yaqeen
   rows have no sizes and `secondary_sources`/`talks`/`translations` are excluded by rule. The
   figure is arithmetically consistent with the formula but not a content count in any meaningful
   sense. This is Task 9's problem; I flag it so the recount does not inherit it unexamined.
8. **Whether any of the 15 recovered works was already counted under another slug.** No duplicate
   slugs, no duplicate titles, no date collisions among found works, and all 22 of F2's recovered
   posts are accounted for (15 works + 3 notices + 2 stub-fills + 3 pre-existing/adopted). But
   "is this essay distinct from `islam-and-terrorism` vs `islam-terrorism`" style near-duplicates
   across the 2017-12-22 MDI-as-work cluster needs an editorial pass, not a slug join.

---

## Verdict

**Yes — this commit is safe to keep as the basis for the remaining phases, with two fixes applied
before anything is built on top of it.**

The substance of the work is sound and, unusually, verifiable: every one of the 15 recovered works,
2 stub-fills, 9 adopted texts, 17 MDI texts and 3 notices is byte-identical to its staged original
after whitespace normalisation; nothing was summarised, reworded or summed; all 7 PDFs are real,
page-count-correct and byte-identical to staging; the 12 superseded videos are preserved with full
records; all 12 transcripts survive with their line counts; the rename is complete across every
live reference; the five site pages are provably rename-only, so the Task 9 approval gate is
untouched; and there is no privacy leak. The counting discipline the brief cared most about —
mirrors never counted as works, announcements catalogued but never counted, restricted and dead
papers recorded before any count moved — holds.

Two things must be fixed first, both mechanical:

1. **C1** — run `python -B scripts/build_collections.py`, rebuild, and `git add _videos/`, so the
   67-video catalogue and the 56 video pages agree. Add a suite assert so it cannot drift again.
2. **C2** — rename `files_extra` → `additional_files` in `_data/papers.json` and rebuild, so the
   held Japanese PDF appears on its page instead of being silently dropped.

Then, before Task 9's recount: settle **I2** (the ≥9 MDI/works double count and the false
"not counted again" sentence the commit prints on 17 pages), because the recount is exactly where
it would otherwise be blessed; and land **I6** (commit the 87 dirty paths) so the repository state
and the ledger agree. **I1** (the ineffective anti-vanishing guard) should be tightened in the same
edit as C1, since both are in `test_transcripts.py`.

Everything else is Important-but-deferrable (I3–I5, I7) or Minor, and none of it blocks Phase 3.

One process note for the controller: this commit is the right shape, but two of its three headline
verifications (the `_videos/` page set and the site-page "rename-only" check) were run against a
narrower file set than the change touched, and both reports' strongest self-review claims — I1's
"byte-identical, PASS 9/9" and "both rows carry each other's `alternate_urls`" — are stated more
strongly than the data supports. The self-reviews were automated and checked presence, not
semantics. For the remaining phases, add one gate that compares every generated collection's file
count to its data file's row count, and one that greps generated pages for keys the data does not
contain.
