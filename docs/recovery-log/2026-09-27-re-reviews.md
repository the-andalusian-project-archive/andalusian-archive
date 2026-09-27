# Independent re-review — Phase 2 fix wave (`9b431ef` → `f0ba4e7`)

**Reviewer:** independent reviewer (did not write any of the fix wave)
**Scope:** the fix diff only. Findings are verdicted ADDRESSED / PARTIALLY ADDRESSED / NOT ADDRESSED;
new breakage introduced by the fix diff is listed separately. Nothing outside the fix diff was
re-reviewed, and nothing was fixed.
**Method:** read the committed blobs at `f0ba4e7` and at `9b431ef` via `git show`/`git diff`; inspected
the current working files; re-ran the 4 read-only suites; recomputed every number independently
(5-gram containment, disk line counts, set comparison of every generated collection, the content-index
arithmetic, all 68 rendered video cards, all 7 PDF links); mutation-tested the new transcript guard.
No file in the workspace was modified; no state-changing git command was run.

## Suite re-run (read-only), working tree at `f0ba4e7`

```
test_no_junk:      ALL PASS (54 files clean)
test_canonical_57: TEST_PASS works=72 captures=87 notices=3 found=47 wayback_only=24 lost=1
                   (all found have >=200w local files, 1 audited exception(s); 0 collection/data drift)
test_search_sync:  ALL PASS  (videos 68 / papers 20 / works 72, 3 sync checks, blog_posts 87, excerpt/keyword)
test_transcripts:  ALL PASS  (56/68 transcribed, 12 catalogue-only, 1 capture deliberately not attached,
                   12 ledger rows accounted for: 10 re-parented / 1 kept / 1 restored,
                   10 re-parented alternates verified on disk, 15 transcript joins)
git status --short: (empty) — 0 dirty paths
```

I did not run `bundle exec jekyll build` (it rewrites `_site/`); the fixer's build claim is
unverified by me. Every `_site/` artefact I did inspect matched its data.

---

## Verdict table

| id | finding | verdict | evidence |
|---|---|---|---|
| **C1** | `_videos/` never regenerated (67 catalogue vs 68 pages); no gate | **ADDRESSED** | `build_collections.py:398-462` `collection_drift()`, called from the builder and from `test_canonical_57.py:11,83-84` (`assert not drift`). Compares **filenames, not counts**: `_videos` via `video_filenames()` (`:427-428`), `_papers` via `paper_slug` (`:429-431`), `_articles` by slug (`:432-436`). My own set comparison: `_videos` 68 rows ↔ 68 pages, **0 missing / 0 extra**; `_papers` 20/20; `_articles` 92/92. The C1 defect itself (11 dead `/videos/<id>/` search links, 12 removed videos still public) is gone. See N2 for the `_posts` leg. |
| **C2** | `files_extra` vs `additional_files`; held Japanese PDF silently dropped | **ADDRESSED** | `_data/papers.json` id 7: `files_extra` present in **0** rows, `additional_files` on 1. Reader-facing `note` no longer names a data key (`_papers/gender-equality-islam-and-law.md:9`). Builder asserts at `build_collections.py:367-395`: every `_papers/pdfs/*.pdf` named by a row **and** present on disk, plus no `/papers/pdfs/` link. Japanese PDF now linked at `/papers/gender-equality-islam-and-law-japanese.pdf` and present in `_site/papers/`. |
| **I1** | anti-vanishing guard checks row presence, never the text | **ADDRESSED** | `test_transcripts.py:61-107` `disk_line_count()` + `assert_text_intact()`, wired at `:175` (all 12 ledger rows, any disposition) and `:197` (all 10 alternates). It genuinely reads disk: `path.is_file()` (`:98`) then `disk_line_count()` (`:102`), and asserts non-null `file`/`lines`/`captions` first (`:90-92`), so the size check cannot be skipped. I recomputed all 22 entries myself: **0 mismatches** (e.g. `cap-D2t0idkAqjA.en-orig.vtt` rec 15048 / disk 15048; `cap-xhnU-1dNi3I` 23168/23168; `cap-G47Stp3pLss` 15048/15048). Mutation tests against the same logic: nulling the 3 fields → **CAUGHT**; truncating a `.vtt` to 1 line → **CAUGHT** (`size`); deleting a capture → **CAUGHT** (`missing`). The reviewer's original simulation (null the fields, suite stays green) now fails. |
| **I2** | MDI double count; `total_content: 219`; false "not counted again" on 17 pages | **ADDRESSED** | 13 rows carry `counted_as_work: false` + `duplicate_of` + evidence; 4 counted. **My own 5-gram containment** of each MDI text against each local work text reproduces the fixer on all 9 text-proven rows: `religion-vs-paedophilia-part-1` 1.0000, `still-colonised-…` 1.0000, `extraordinary-claims-…` 0.9849, `boko-haram…` 0.9810, `religion-vs-paedophilia-part-3` 0.9761, `-part-2` 0.9738, `withoutevidence2` 0.9643, `naked-kings…` 0.9399, `whataboutery…` 0.9387 — all ≥0.93, none a false positive. The 4 rows still counted are **not** duplicates: `refuting-the-masked-arab-2` (0.0000, no work shares the title), `when-facts-become-fiction-ijihad-ep-1` (0.0000, no title match; correctly flagged as a judgement call), `an-antidote-for-extremism` (0.0194 = noise, no title match). The 4th, `criminal-minds…`, is counted at 0.0000 but carries a false evidence sentence — see **N1**. Total: `statistics.total_content` = **207**; formula string `72 works + 68 videos + 20 papers + 4 MDI (of 17 rows; 13 are second publications of a work already counted) + 9 Yaqeen (link-outs, sizes not stored) + 33 AlBalagh (link-outs) + 1 interview = 207`; I re-added the terms: **207 ✓**. Sentence is data-driven (`build_collections.py:976,982-983`) and I checked **all 17 rendered pages** against their rows: **17/17 match** (13 show the duplicate wording, 4 the distinct-content wording, 0 still carry the old blanket claim). |
| **I3** | apostasy page: mislabelled Wayback link, false "Original site", no `original_url`/`alternate_urls`, false report claim | **ADDRESSED** | `_data/canonical_works.json` apostasy row now has `original_url` (live IDI URL), `wayback_capture_staged: false`, `wayback_label: "Original (live; no Wayback capture was staged)"`, `source_site: "Original site: islamicdiscourseinitiative.com (live; captured 2026-09-27). This text was never published on asadullahali.com"`. `alternate_urls` on **both** rows: IDI URL + the other's permalink. Rendered page shows the corrected label and source line; `"Original site: asadullahali.com"` is **absent**. The false report claim is corrected in `task-7-I1-report.md:901-908`. |
| **I4** | `channel_facts.json` `is_his: null` vs the brief's "NOT his" | **ADDRESSED** (by the remedy the finding itself prescribed — a ledger line) | `progress.md:98` **R19** records the deviation, the reasoning (a capture records a channel's state, not its operator), that the operational never-link rule is fully encoded, and the cost if wrong. `is_his: null` is intentionally unchanged, which is what R19 authorises. |
| **I5** | deleted video-shape assert; `videos.md` labels every card "Archive.org" | **ADDRESSED** | Gate restored and pinned to the data, not a magic number: `build_collections.py:528-539` asserts `youtube_not_archived` ≡ entries carrying `kind` **in both directions**, each declaring `transcripts: 0` and a `source`. My count: 12 rows with `kind`, 12 with `transcripts: 0`, 12 youtube-watch `archive_url`s → **12 == 12**. `videos.md` now branches on the actual `archive_url`; I parsed all **68** cards out of `_site/videos/index.html`: **12 `YouTube (kind)`, 56 `Archive.org`, 0 mismatches**, and no `&gt;Archive.org&lt;` escaped-attribute breakage. The `Dr5IgXCHRIE` raw `"` is percent-encoded in `archive_url` (`%22`) with the archive's own spelling kept in `filename`, and a new `_HREF_BREAK` gate (`build_collections.py:493,517,521`) rejects `"`, `<`, `>`, backtick in any video URL — **0 hits** repo-wide. |
| **I6** | commit is stale: 87 dirty paths | **ADDRESSED** | `git status --short` at `f0ba4e7` returns **empty** — 0 dirty paths, 0 untracked. The drift is committed; repository state and the ledger agree. |
| **I7** | `linkouts.json` `words_source` points into `_staging/`; 6 of 9 rows have no size | **ADDRESSED** (as scoped to `linkouts.json`) | `words_source` removed from **all 10** rows; **0** `_staging` references remain in `linkouts.json`; every row now carries a durable `provenance` object (`url`, `retrieved_at`, `wayback_capture_count`, `recorded_by`) and a `words_status` string (2 "known", 7 "unknown: … Its size is NOT counted in `total_content`", 1 "not measurable by design"). Formula term now reads `9 Yaqeen (link-outs, sizes not stored)`; `collections.yaqeen_papers` gained `sizes_known: 2` + a `storage` note saying it is a row count. |
| **M1** | `sync_search_data.py` docstring says 68/18/57 | **ADDRESSED** | `scripts/sync_search_data.py:9-20`: `_data/videos.json (68)`, `(20)`, `(72 works)`, "Search defaults to the works list (72)", and the stale "may still 404" note replaced with a pointer to `collection_drift()`. |
| **M2** | `README.md` says `(68/18/57 asserts)` | **ADDRESSED** | `README.md:108` now `python scripts/test_search_sync.py (68/20/72 asserts)`. |
| **M3** | "the 57 honest works" in `search.md` / `README.md` | **ADDRESSED** | **0** occurrences of "honest works" remain in either file (both now say "the works list"); the number itself correctly left to Task 9. |
| **M4** | report said the 2 stub-fills "extend the existing stubs" | **ADDRESSED** | `task-7-I1-report.md:985-989` appends the correction (two **new** `_posts` files; outcome unchanged). |
| **M5** | 5 new video entries carry `duration: ""` | **ADDRESSED** | `En8F38ChvvE`, `TTGJPneVR_w`, `dsMWdlzzfMk`, `s_BnmOrVaTg`, `vI3Jz-OSH54` are all `null` in `_data/videos.json` **and** in `data/videos.json` (synced); **0** empty-string `duration` remain in the file. |
| **M6** | adopted captures lost `>` blockquote markup | **ADDRESSED — deferred by ruling R20** | Not code-fixed, and correctly so: the finding's own remedy was "re-add `>`, **or note it**", and re-adding markup would mean hand-editing recovered essay text. Recorded at `progress.md:99` (R20) and in the report's §M6 with the 4 affected files named. `_posts/` is byte-unchanged by this commit, so no prose was touched. |
| **M7** | 2026-09-06 plan still names `canonical_57.json` | **ADDRESSED** | `docs/superpowers/plans/2026-09-06-57-list-honest-counts.md:2-8` gains a one-line "Superseded" pointer naming the rename and the 2026-09-27 plan; the plan's own historical references are left as written. |
| **M8** | evidence trail is untracked (`.superpowers/sdd/.gitignore` = `*`) | **ADDRESSED — deferred by ruling R23** | `progress.md:102` (R23) schedules the export of manifests/reports/log to `docs/recovery-log/` at Task 9, i.e. in the phase the finding named. `.gitignore` itself deliberately untouched. |
| **M9** | 52 rows keep `origin: "derived_52"` | **ADDRESSED** | `secondary_sources.json` 69 rows; `origin` values are now only `derived` / `lane_extension`; **0** rows still say `derived_52`. |
| **M10** | `recovered_text_words` absent from the 9 adopted `canonical_works.json` rows | **ADDRESSED** | All 9 adopted rows now carry **both** `recovered_text_words` and `word_count`, and the values match the report and the `_posts` front matter: 68903, 20037, 2167, 4534, 5646, 5939, 3826, 3661, 1601 (differing from `word_count` only for the 4 works with a retained appendix). |
| **M11** | report internally inconsistent on rename scope (13 vs 14) | **ADDRESSED** | `task-7-I1-report.md:990-994` appends the correction: the true number is 14, with the 2 renames and 12 reference-updated files enumerated. |
| **R16** (pulled forward) | 7 held PDFs unlinked; "not mirrored" prose wrong; no per-file licence line | **ADDRESSED** | All 7 PDFs are real links at `/papers/<file>.pdf` on their paper page and **all 7 are present in `_site/papers/`** (verified file-by-file), each with an `Obtained from:` line **and** a `Licence / provenance:` line. 6 paper pages carry the block (`gender-equality-islam-and-law` carries 2 files = 7 PDFs). Per-file provenance is real: archive.org CC via its item URL, TOTETU open copy, IIUM bitstream + sha256, AMJA programme URL, and the Japanese translation labelled a commercial out-of-print issue with public provenance **NOT verified**. `architects-of-civilisation-…` keeps `file_source: null` and its "SOURCE URL UNVERIFIED" warning on the page. The false prose is gone: **0** held-PDF pages say "No PDF is mirrored"/"not mirrored", while the **14** genuine link-out-only papers (incl. the 403 academia.edu item) still do. No `/papers/pdfs/` link anywhere. |

**Totals: 21 ADDRESSED · 0 PARTIALLY ADDRESSED · 0 NOT ADDRESSED** (2 of the 21 are deferrals
recorded as ledger rulings, R20 and R23, both of which match the remedy the finding itself proposed).

---

## R16 work pulled forward — verified

| # | PDF | linked | served | licence line |
|---|---|---|---|---|
| 1 | `between-a-backbone-and-ribs.pdf` | ✅ | ✅ | ✅ |
| 2 | `the-rise-and-decline-of-scientific-productivity.pdf` | ✅ | ✅ | ✅ |
| 3 | `islamic-intuitionism-thesis.pdf` | ✅ | ✅ | ✅ |
| 4 | `deconstructing-contemporary-atheist-thought.pdf` | ✅ | ✅ | ✅ |
| 5 | `gender-equality-islam-and-law.pdf` | ✅ | ✅ | ✅ |
| 6 | `gender-equality-islam-and-law-japanese.pdf` | ✅ | ✅ | ✅ (NOT-verified provenance stated) |
| 7 | `architects-of-civilisation-sallahuddin-ayubi.pdf` | ✅ | ✅ | ✅ (SOURCE URL UNVERIFIED kept) |

---

## New breakage introduced by the fix diff

### N1 — Important — the new MDI `counted_as_work` evidence fields assert falsehoods, and the generated page contradicts itself

This is the R24 failure mode (a self-review that checks presence, not semantics) recurring **inside**
the fix wave. No count is wrong and no text was altered, but false statements about the archive's own
holdings are now rendered on public pages, and no gate catches them.

1. **A provably false "no local text" claim.** `_data/mdi_articles.json:216`
   (`still-colonised-liberalism-in-muslim-thought`) states the work *"is wayback_only and has **NO
   local text**, so no text comparison was possible and the two may or may not be the same
   document."* That is false. `_posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md`
   exists and holds the essay's text (102 w, "On May 9th, 2015 I gave a lecture on Liberalism in
   Muslim Thought at IMEC 2015 in Kuala Lumpur…"). I computed the 5-gram containment of the MDI row
   against that file myself: **1.0000** — every 5-gram of the MDI caption is present in it. The
   comparison was possible and the answer was exact. The claim is rendered verbatim on
   `_articles/mdi-still-colonised-liberalism-in-muslim-thought.md`.
   The other 3 conservative rows (`islam-terrorism` L78, `do-muslim-women-need-feminism` L117,
   `towards-litter-reduction-…` L176) I checked against all 54 `_posts` files and all 493 staging
   files: for those, "no local text" is **true**, so the misstatement is confined to the one row above.

2. **The page contradicts itself on all 4 conservative rows.** `build_collections.py:982-983`
   emits, unconditionally for every duplicate row, *"**This essay is also catalogued as a work and is
   not counted again.** It is the same text as the work `X`"* and then quotes the evidence
   immediately below it — which for those 4 rows says *"may or may not be the same document."*
   A reader gets both assertions on one page.

3. **An unflagged judgement call in the inflating direction, with a false premise.**
   `_data/mdi_articles.json:156` (`criminal-minds-liberalism-in-muslim-thought`,
   `counted_as_work: true`) opens *"No work shares this title"* — but the work
   `liberalism-in-muslim-thought` exists (title "Liberalism in Muslim Thought", `wayback_only`). The
   row's later sentence does distinguish this MDI post from two *other* works, and the announcement
   is arguably a distinct document from the lecture, so the counted verdict is defensible. But this is
   the same class of unprovable call the report **did** flag for
   `when-facts-become-fiction-ijihad-ep-1`; here it is neither flagged nor surfaced in the report's
   Concerns, and it is worth 1 in `total_content` if reversed.

Count impact: **none** — the 207 arithmetic is correct and the 13/4 split is defensible. The defect is
that the evidence, which exists precisely to make the decision auditable, is not true in at least two
places, and one of them is a row where certainty was available and was discarded as "AMBIGUOUS".

### N2 — Minor — the `_posts` leg of `collection_drift()` joins by date, so a 7th unclaimed file is invisible

`collection_drift()` matches a found work to its file by **date prefix**
(`build_collections.py:446`, `POSTS_DIR.glob("%s-*.md" % w["date"])`), not by name, and a glob by
date absorbs every file sharing that date. `2015-05-12` carries two files, so
`_posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md` (102 w — the local text of the
`wayback_only` work of the same name) is counted as "claimed" by the unrelated found work
`extraordinary-claims-…` and never reaches the `stray` comparison at `:456-457`. Consequences:
`UNCLAIMED_POSTS` (`:472-479`) documents **6** files, but the true number of unclaimed partial-local-text
files for `wayback_only` works is **7**; and the comment's stated range "91–184 w" is wrong — 3 of the
6 documented files are 205, 212 and 225 words. No data is lost and no essay is at risk; the gate is
simply weaker for `_posts` than the report's "comparing **filenames**" phrasing implies. (It is
nonetheless non-vacuous: I confirmed the three 1:1 legs and the `stray != UNCLAIMED_POSTS` comparison
all produce failures on a set mismatch, and `test_canonical_57.py:84` asserts the result.)

---

## Regression check on the fix diff — none found

| check | result |
|---|---|
| `_posts/` touched by the fix wave | **`git diff --stat 9b431ef f0ba4e7 -- _posts/` is empty** — no essay altered |
| `.firecrawl/transcripts/` touched | **empty** — no transcript lost; 29 `.vtt` captures on disk, all 22 referenced sizes still match |
| MDI essay text | **17/17 `text` values byte-identical** between `9b431ef` and `f0ba4e7`; **0** pre-existing MDI key values changed; only 4 new keys added (`counted_as_work`, `counted_as_work_evidence`, `duplicate_of`, `duplicate_evidence`) |
| `canonical_works.json` | 72 → 72, **0** slugs added/removed, **0** changes to `title`/`status`/`date`/`wayback_url`; the only 3 edits are the intended `alternate_note`/`alternate_urls` on apostasy + naked-kings |
| `_articles/` | 19 files, 92+/22−; every changed line is the new MDI sentence/evidence or the 2 I3 pages — **no body text** |
| `_papers/` | 20 pages, prose/link/licence additions only |
| Task 9 approval gate | `index.md` still shows 57 / 68 / 18 / 203 and does **not** contain 207 — the count-approval gate is intact |
| collection sizes | 54 `_posts` · 92 `_articles` (72 + 17 MDI + 3 notices) · 20 `_papers` · 68 `_videos` — all match their data files exactly |
| new broken links | none found; the two the fixer found and fixed (`Dr5IgXCHRIE` raw `"`, `/papers/pdfs/` → `/papers/`) are both closed and both now gated |

## Out of scope, noted in one line each

- `_staging/` pointers — the class of dangling provenance I7 fixed in `linkouts.json` still exists in
  `_data/bibliography.json` (10), `channel_facts.json` (15), `mdi_articles.json` (17) and
  `superseded_videos.json` (12); they will dangle when `_staging/` is deleted at Phase 4. Outside I7's
  scope, not introduced by the fix wave.
- `channel_facts.json` was amended in this same commit (R22 merged the checkpoint-2 decisions with the
  fix wave), so 15 of its `_staging` `source_file` refs are new in `f0ba4e7` — but they belong to I2's
  lane, not the fix wave.

---

## Verdict

**21/21 findings ADDRESSED** (2 of them as recorded deferrals R20/R23 that match the remedy the
finding itself proposed), **0 PARTIALLY ADDRESSED**, **0 NOT ADDRESSED**, with one new Important
defect (**N1** — false `counted_as_work` evidence strings rendered on public pages, and a page that
contradicts itself) and one new Minor defect (**N2** — the date-based `_posts` leg of the new drift
gate hides a 7th unclaimed file). Both new findings are data-accuracy defects, not lost data: no
transcript was deleted, no essay was altered, and `total_content: 207` is arithmetically correct.

---

<!-- ==================== END OF DOCUMENT 1 of 2 ==================== -->
<!-- The remainder of this file is a second, separate review document, -->
<!-- reproduced verbatim below. Nothing between the two documents has  -->
<!-- been edited, summarised or merged.                             -->

---

# Independent re-review, round 2 — N1 and N2 (`f0ba4e7` → working tree)

**Reviewer:** independent reviewer (did not write any of the fix wave, round 1 or round 2)
**Scope:** N1 and N2 only, plus breakage introduced by the round-2 diff itself. Nothing else was
re-reviewed and nothing was fixed.
**Round-2 diff:** 21 files, +308/−77 — 17 `_articles/mdi-*.md` (each exactly **+2/−2 lines**),
`_data/mdi_articles.json`, `_data/content_index.json` (1 line: `last_updated`), `scripts/build_collections.py`,
`scripts/test_canonical_57.py`. `_posts/` is not in the diff.
**Method:** read the working-tree code and data; recomputed 5-gram containment myself over an
independently built corpus (54 `_posts` bodies + 351 `_staging` text files from the `mirror`,
`best_capture` and `deleted` lanes = **405 sources**; the `mdi` lane excluded, since it is each row's
own source and would trivially return 1.0000); re-ran the 4 suites; re-derived the slug join, the
unclaimed set and the word counts; checked every rendered MDI page against its row; diffed
`mdi_articles.json` against the `f0ba4e7` blob. No file was modified; no state-changing git command
was run.

## Suites (working tree)

```
test_no_junk:      ALL PASS (54 files clean)
test_canonical_57: TEST_PASS works=72 captures=87 notices=3 found=47 wayback_only=24 lost=1
                   (all found have >=200w local files, 1 audited exception(s); 0 collection/data drift)
test_search_sync:  ALL PASS   (videos 68 / papers 20 / works 72, 3 sync checks, blog_posts 87, excerpt/keyword)
test_transcripts:  ALL PASS   (56/68, 12 catalogue-only, 12 ledger rows, 10 alternates verified on disk, 15 joins)
```

---

## Verdicts

### N1a — ADDRESSED. The 4 "conservative" rows re-derived against sources that exist

`_data/mdi_articles.json` now carries a machine-readable `evidence_class`, `containment` and
`measured_against` on every row: **10 `text_proven`**, **3 `work_row_only`**, **4 `counted`**
(`scripts/test_canonical_57.py:118-152` gates the agreement between class and `counted_as_work`).

**My own recomputed containment (405 sources), against the fixer's claims:**

| row | class now | claimed | **my measured peak** | my top match |
|---|---|---|---|---|
| `still-colonised-liberalism-in-muslim-thought` | `text_proven` | 1.0000 | **1.0000** | `_posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md` |
| `islam-terrorism` | `work_row_only` | 0.0566 | **0.0556** | `mirror/islam-and-terrorism.json` |
| `do-muslim-women-need-feminism` | `work_row_only` | 0.0357 | **0.0357** | `mirror/islam-and-terrorism.json` |
| `towards-litter-reduction-an-islamic-approach` | `work_row_only` | 0.0000 | **<0.004 (none)** | — |

- **`still-colonised` is now genuinely text-proven.** My containment of the MDI row against
  `_posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md` is **1.0000** — the file the
  round-1 report identified, which the old evidence claimed did not exist. The row's
  `measured_against` names that exact `.md` file and `counted_as_work: false` is kept, so the count
  is unchanged for the right reason now. The old "has NO local text" string is **gone from this row**.
- **The other three have no comparable text anywhere, as claimed.** I searched all 54 `_posts`
  bodies and all 351 non-MDI staging text files: peak 0.0556 / 0.0357 / <0.004 — noise, no shared
  5-gram run worth calling identity. Their `measured_against` now says *"no local text file exists for
  this work; the full 405-source index was searched"* rather than implying a comparison.
- **No row still asserts "no local text" for a work whose file exists.** 5 evidence strings still
  contain the phrase "no local text" (`islam-terrorism`, `do-muslim-women-need-feminism`,
  `towards-litter-reduction-…`, `criminal-minds`, `when-facts-become-fiction-ijihad-ep-1`); for all
  five the named work genuinely has no `_posts` file, so every one of the five is now **true**. The
  single row that made the claim falsely is the one that was corrected.

### N1b — ADDRESSED. The page sentence is driven by the row's evidence class

Generator: `scripts/build_collections.py:1065-1093`. `counted` → neutral ("it is counted once, here.
The measurement behind that verdict is printed below"); `text_proven` → "**It is the same text as the
work `X`, proved by comparison rather than by title: %.4f of this post's 5-grams are present in that
work's local text**"; `work_row_only` → "**That link is INFERRED, NOT PROVEN: the archive holds no
local text for the work, so the two texts could not be compared.**"

I checked **all 17** rendered pages against their row, not a sample: **17/17 correct** — 10 say
"proved by comparison" and never "INFERRED"; 3 say "INFERRED, NOT PROVEN" + "could not be compared"
and never "It is the same text"; 4 say "distinct item of content" and neither of the others. The
round-1 self-contradiction (bold "It is the same text" printed directly above "may or may not be the
same document") is structurally impossible now: the unconditional `same text` clause is reachable only
in the `text_proven` branch.

Spot-checked verbatim (1 text-proven + 2 inferred + 1 counted):
- `_articles/mdi-still-colonised-liberalism-in-muslim-thought.md` — "It is the same text as the work
  `still-colonized-liberalism-in-muslim-thought`, proved by comparison rather than by title: **1.0000**
  of this post's 5-grams are present in that work's local text", evidence naming the `_posts` file.
- `_articles/mdi-islam-terrorism.md` — "the archive holds no local text for the work, so the two
  texts could not be compared. **The text below is the only preserved copy of this announcement.**"
- `_articles/mdi-do-muslim-women-need-feminism.md` — same INFERRED wording, naming
  `do-muslim-women-need-feminism-debate`.
- `_articles/mdi-criminal-minds-…md` — "distinct item of content: it is counted once, here."

All 13 "counted work page" links across the 17 pages resolve to an existing `_articles/<slug>.md`
whose `permalink:` matches the linked URL: **13/13, 0 bad**.

### N1c — ADDRESSED. `criminal-minds` claim replaced with measured figures

| row | claimed | **my measured** | my top match |
|---|---|---|---|
| `criminal-minds-liberalism-in-muslim-thought` | 0.0536 / 0.0179 | **0.0536 / 0.0179** | `_posts/2015-05-12-still-colonized-liberalism-in-muslim-thought.md`, then `mirror/liberalism-in-the-muslim-world.txt` |
| `an-antidote-for-extremism` | 0.0291 | **0.0291** | `mirror/islam-and-terrorism.json` |
| `when-facts-become-fiction-ijihad-ep-1` | 0.0000 | **<0.004 (none)** | — |
| `refuting-the-masked-arab-2` | 0.0000 | **<0.004 (none)** | — |

Both of the fixer's headline figures for `criminal-minds` reproduce **exactly**. The false premise is
gone: the string now opens "CORRECTED 2026-09-27 … The previous string opened 'No work shares this
title', which was false: the work `liberalism-in-muslim-thought` exists (title 'Liberalism in Muslim
Thought', 2017-12-22, wayback_only)" and rests on the three documents it actually distinguishes. I
re-ran the title-overlap test: the only counted row whose title overlaps a work is `criminal-minds`
→ `liberalism-in-muslim-thought`, and it is now the one row that **discloses** that overlap rather
than denying it. The other two rows that still assert "no work shares its title"
(`refuting-the-masked-arab-2`, `an-antidote-for-extremism`) are **true** — I confirmed zero title
overlap for both. `counted_as_work: true` stands for all four, and `when-facts-become-fiction-ijihad-ep-1`
remains explicitly flagged as a judgement call.

### N1d — ADDRESSED. Total stays 207, composition changed, nothing contradicts

`_data/content_index.json` `statistics.total_content` = **207**; the only line the round-2 diff
changed in that file is `last_updated`. The formula string is
`72 works + 68 videos + 20 papers + 4 MDI (of 17 rows; 13 are second publications of a work already
counted) + 9 Yaqeen (link-outs, sizes not stored) + 33 AlBalagh (link-outs) + 1 interview = 207`.
I parsed the terms and re-added them: **72+68+20+4+9+33+1 = 207 ✓**. MDI term **4** == the 4 rows
with `counted_as_work` not false; `total_mdi_duplicate_of_a_work: 13` == 10 `text_proven` + 3
`work_row_only`; `total_mdi_rows: 17`. Still computed, not hardcoded: `build_content_index.py:32-43`
`counted_mdi()` reads `counted_as_work`, `:76-85` builds the formula, `:185` sums. No other published
number contradicts 207: the only site-page total in the repo is `index.md`'s 203, which is Task 9's
deliberately untouched gate, and 219 appears nowhere.

**Why the total is provably unchanged:** against the `f0ba4e7` blob, **0 rows** flipped
`counted_as_work`, **0** changed `duplicate_of`, **0** rows added or removed. The composition moved
from 9 text-proven + 4 inferred to 10 + 3; the arithmetic is untouched because
`still-colonised` was always `counted_as_work: false` and is still so.

### N2 — ADDRESSED. The `_posts` leg resolves by slug; the 7th file is now reported

`scripts/build_collections.py:476-530`. `resolve_work_post()` tries `<date>-<slug>.md` (exact
filename) → `_articles` `local_post:` pointer → front-matter `slug:`, and **a bare date match is
never sufficient**; the old `POSTS_DIR.glob("%s-*.md")` is gone from `collection_drift()`.

My independent re-derivation using those three functions:
- 47/47 found works resolve; **0 unresolved**. Path actually used: **43 exact filename, 4
  `_articles` `local_post:` pointer, 0 front-matter slug**. (The 4 pointer cases are the pre-existing
  slug/filename divergences — `charlie-hebdo`, `for-good-men-to-do-evil`, `the-archetype-of-beauty-…`,
  `the-narrative-of-happymuslims-…` — which a filename-only join would have missed.)
- **0** files claimed by more than one found work; 0 duplicate front-matter slugs, so the
  `setdefault` in `posts_by_front_matter_slug()` cannot pick the wrong file.
- Unclaimed set is **7** files and equals `UNCLAIMED_POSTS` **exactly** — no documented-but-absent
  entry. **The 7th is the file round 1 named: `2015-05-12-still-colonized-liberalism-in-muslim-thought.md`**,
  now correctly surfaced instead of being absorbed by the same-date found work
  `extraordinary-claims-…`.
- The comment now names the measure it uses (`len(body_after_front_matter.split())`) and tabulates
  both readings. I recomputed all 14 figures and **all 14 match**:
  body 76 / 91 / 161 / 93 / 165 / 184 / 96, whole-file 102 / 139 / 205 / 133 / 212 / 225 / 136.
  Under the body measure the old "91–184 w" claim is now accurate (91–184) and the 76-word file is
  inside the set; the round-1 "205 / 212 / 225" figures are correctly identified in the comment as
  whole-file counts including front matter. Both readings are now unambiguous.
- `collection_drift()` returns **clean**, and `test_canonical_57.py:78-84` asserts it.
- The test suite had the **same** date-join defect (`glob(date + "-*.md")[0]`, i.e. it read whichever
  same-date file sorted first) and is now fixed too: `test_canonical_57.py:56-64` uses
  `resolve_work_post`, with a new same-date regression at `:83-97`. That regression is not vacuous —
  2015-05-12 carries 2 works and 2 files, the exact collision that broke the old join.

---

## New breakage introduced by the round-2 diff: **none**

| check | result |
|---|---|
| recovered prose | `_posts/` is **not in the diff**; all 17 `mdi_articles.json` `text` values are byte-identical to the `f0ba4e7` blob (**17/17**) |
| data rows | 0 rows added/removed, 0 `counted_as_work` flips, 0 `duplicate_of` changes — the total cannot have moved |
| scope discipline | `_data/canonical_works.json`, `papers.json`, `videos.json`, `transcript_coverage.json`, `linkouts.json`, `secondary_sources.json`, `superseded_videos.json`, `channel_facts.json`, `videos.md`, `index.md`, `README.md`, `search.md` are all **byte-identical to `f0ba4e7`** |
| `_articles` pages | 17 changed, each exactly **+2/−2** lines (the counting line and the evidence string); no body text |
| links | 13/13 "counted work page" links resolve to an existing file with a matching `permalink:` |
| did a gate get weaker? | **No.** `collection_drift()`'s `_posts` leg got strictly stronger (slug join + a 7th file exposed); `test_canonical_57.py`'s post resolution got strictly stronger; **no assertion was removed, relaxed or replaced by a weaker one** — the only edited assertion is the `matches[0]` → `resolve_work_post` line, which is the fix |
| new gates | N1: `evidence_class` present and consistent with `counted_as_work`; a work row that really exists; non-empty evidence; `containment` numeric and **≥ 0.90** for `text_proven` with a named `.md`; `INFERRED, NOT PROVEN` + "could not be compared" + numeric figure for `work_row_only`; dedup chains rejected (`test_canonical_57.py:118-152`). N2: same-date resolution regression (`:83-97`) |
| private/secret data | nothing added; `channel_facts.json` untouched (byte-identical) |

### Observations, not findings (no defect exists today)

1. The 4 `counted` rows record their headline figures (0.0000 / 0.0000 / 0.0291 / 0.0536) **in prose
   only** — `containment` is `None` on them, and the new gate requires a numeric `containment` only
   for `text_proven` and `work_row_only` rows. All four figures are correct as far as I measured, so
   nothing is false; but a future edit could overstate a counted row's figure without any gate
   objecting. Closing that would mean requiring a numeric `containment` on all 17 rows.
2. The new same-date regression asserts each file resolves to *a* work dated that date, not to *the
   correct* work; the complementary `collection_drift()` `twice` check is what catches two works
   claiming one file. Between them the collision is covered, but neither check alone is complete.
3. The formula's parenthetical still reads "13 are second publications of a work already counted"
   without marking that 3 of those 13 rest on an inferred link. The inference is disclosed on each of
   the 3 pages and in each row, so this is a summary line, not a claim of proof.
4. I did not run `bundle exec jekyll build` (it rewrites the gitignored `_site/`), so the fixer's
   "built site checked" claim is unverified by me. `_site/` is gitignored (`.gitignore:1`) and
   untracked, so its staleness is not committed breakage; every artefact I did inspect in `_articles/`
   matched the data.

---

## Verdict

N1 AND N2 ADDRESSED — 0 new-breakage findings.
