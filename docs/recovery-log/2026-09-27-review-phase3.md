# Independent review — Phase 3 (Task 8), `db16e2c..8eaa65f`

**Reviewer:** independent reviewer (did not write any of this)
**Date:** 2026-09-27 · **Base:** `db16e2c` · **Head:** `8eaa65f` (2 commits, 145 files)
**Spec:** `docs/superpowers/plans/2026-09-27-full-recovery-v6.md` — Task 8 + Global Constraints
**Method:** read the diff, read all four implementer reports, then verified against the working tree: 4 suites run, `bundle exec jekyll build` run, `_site/` inspected, `_data/*.json` re-derived, captures re-parsed. No file was modified.

---

## 1. Spec compliance

| # | Requirement | | Evidence |
|---|---|---|---|
| 1 | Four approved categories exist | ✅ | `_data/taxonomy.json:1-70` — 4 categories with inclusion/exclusion rules, `ordering_rule`, per-data-file rationale. Labels come from the data file; `_includes/category_badge.html:11-13` looks them up, no template types a label. |
| 1 | Categories **computed at build time**, not typed literals | ❌ partial | Liquid loops over `_data/*.json` throughout (`index.md:38-59`, `videos.md:12-32`, `papers.md:10-15`, `articles.md:11-22`, `transcripts.md:32-39`). But two typed numerals survive inside that prose — `index.md:69` ("The **13** MDI rows") and `articles.md:91` ("**Seven of the seventeen**"). See I3. |
| 1 | Authorship-not-format rule actually applied | ✅ | 57 videos he produced → A, 11 he appeared in → C, per each row's own `kind`/`source`. A debate he produced (`A3dbBCBSFKk`), an interview he conducted (`a1e0BMRLlr0`, `OTcAF8T-gD4`) and talks at others' halls (`ZbcsxAoIVY0` Yaqeen NY, `IhE3ka7SQQs` i3 Canada) are all A. The 11 C rows are 5 MDI debates + 1 MDI-archive radio + 1 MDI clip + 2 Fakir Ilmu clips + 1 MSA Ohio State GBM + 1 Persian upload + 1 short-form clip. Verified row by row. |
| 1 | Every countable item carries exactly one category | ✅ | 164 counted rows total (72 works + 68 videos + 20 papers + 4 MDI) = A 150 + B 3 + C 11. No row carries two letters; the 13 uncounted MDI rows all name `duplicate_of`; the 4 counted MDI rows name none. |
| 1 | No double-counting | ✅ | 13 MDI republishes held `counted: false`; co-authored papers counted once under B and not again under A; 3 papers with `co_authors` are the only B rows. |
| 1 | `secondary_sources` (69), notices (3), link-outs (10) catalogued, never counted | ✅ | All 69 `category: "C"`, `counted: false`; all 3 notices `D`/`false`; all 10 link-outs `D`/`false`. Rendered on `articles.md` under "None of them is counted" / "not counted". |
| 2 | **No published count changed without owner approval** | ❌ | **C1.** `articles.md` published totals 57→72, 30/15→47, 40→24, 2→1; `papers.md:18` 18→20. Task 9 has not happened. |
| 2 | `index.md` headline grid untouched | ✅ | `index.md:14,18,22,26,30` and the table at `:174-210` are byte-identical to `db16e2c`. |
| 2 | `videos.md` 68/56 untouched | ✅ | Still renders 68 total, 56 on Archive.org, 12 YouTube-only. `56→57` / `12→11` follow ruling R25 (new computed counts). |
| 2 | `README.md` count literals untouched | ✅ | 87/68/18/17/9/36/52/261 all preserved; only 3 Status cells and 1 paragraph changed. |
| 2 | `timeline.md` untouched | ✅ | Zero diff — but see I6. |
| 2 | New computed counts disclosed by the report | ✅ | 8d §9.3 discloses the `transcripts.md` numbers (68/58/540,947/10 + 57/10/1) and offers a one-span deletion. |
| 3 | Disclaimer **verbatim** on transcript pages and wherever shown | ✅ | `MACHINE_TRANSCRIPT_DISCLAIMER` = U+2014 + U+0027, byte-identical to the spec sentence. Present on **69/69** built `/transcripts/` pages, in all 68 `_transcripts/*.md` front matter, in `_data/transcript_index.json`, and in `_layouts/video.html:…`. `transcripts.md:25` and `_layouts/transcript.html:19` print it *from* the data, so no layout holds its own copy to drift. |
| 3 | `transcripts: 0` → neutral note, no dead link | ✅ | 11/11 pages show "Transcript not yet available for this entry." and **0** `/transcripts/<id>/` href (only the site-wide nav/footer). Verified by parsing the built HTML. |
| 3 | 10 re-parented `alternates` attributed to the right recording | ✅ | All 10 have `role: duplicate-upload`, `capture_video_id != recording`, and each is filed under the correct `by_recording` key. `NyAVl7RsEOs` correctly carries both `2tsI80MDUOI` and `EK5oppX6C2U`. |
| 3 | ≥5 published `_transcripts/` docs spot-checked vs `.vtt`/`.json` | ✅ | 6 sampled (4 VTT incl. 2 alternates, 2 whisper). **Every** paragraph of the capture appears in the built page: 806/806, 916/916, 936/936, 456/456, 67/67, 238/238. Only residual ≥3× repeats are genuine interjections (`so`, `um`, `[Music]`), not caption echo. |
| 4 | De-echo: article transcript == published transcript | ✅ | All 3 files now **identical** to `capture_paragraphs(parse_capture(...))`: 806 / 936 / 55 paragraphs, 11,322 / 9,502 / 739 words. |
| 4 | De-echo: no AUTHOR prose lost | ✅ | The text outside `<details>` is **byte-identical** to `db16e2c` in all 3 files (82 / 89 / 97 words before, 0 after). The new word stream is an **ordered subsequence** of the old in all 3 — no word invented, none dropped that was not echo. `_data/transcript_coverage.json` `lines` (16560 / 15216 / 1032) untouched. The 12 whisper-backed article transcripts are byte-identical to before. |
| 5 | BOM incident: homepage and blog index render | ✅ | `_site/index.html` and `_site/articles/index.html` both exist; `_site/index.md` and `_site/articles.md` are gone. |
| 5 | No OTHER tracked file has a BOM | ✅ | Byte-level scan of all **451** tracked files: **0** UTF-8/UTF-16 BOMs. |
| 6 | `docs/` (and no other non-site path) must not reach `_site` | ✅ | 0 paths for `docs`, `_staging`, `.superpowers`, `.firecrawl`, `node_modules`, `scripts`, `.ua`, `vendor`; 0 `/docs/` URLs in `sitemap.xml` (317 URLs). `.env`/`Gemfile`/`package.json` absent. |
| 7 | 2023 identity stated without asserting authorship either way | ✅ | `is_his: null` printed with the R19 reason ("a Wayback capture records a channel's *state*, not its *operator*"); explicit *can show* / *cannot show* pair. |
| 7 | Rejected "585 K subscribers" visible as rejected | ✅ | Rendered as a REJECTED card; closing sentence names 585K, 329K and 1.01 million; series "tops out at 15.7K". |
| 7 | No `youtube.com/channel/` in file, page or build | ✅ | 0 in `_data/channel_facts.json`, `channel.md`, `README.md`, `videos.md`, `_site/channel/index.html` — and **0 across the entire `_site`**. |
| 7 | Do-not-link rule stated | ✅ | `channel.md:154-176` → rendered 3-row table: live page never linked, id as text only, 2023 handle never linked as his, with the reason each time. |
| 8 | Honesty sweep — no sentence asserting what the evidence does not support | ❌ | C1, I1, I3, I6, I7. |
| 8 | Reports checked against reality | ❌ | I4 (8b), I5 (8a). |
| 9 | No leak into `_site` | ✅ | As row 6. |
| 9 | `_transcripts/` tracked, not ignored | ✅ | `git check-ignore` returns nothing; **68** files tracked; `.gitignore` unchanged. |
| 9 | No gate got weaker | ✅ | `test_canonical_57.py`: **0 lines changed**. `test_transcripts.py`: purely additive — the only edits to existing lines are the import block, 2 constants (56→57, 12→11, justified by R25) and docstring prose. No assert edited, renumbered, deleted or relaxed; the `unattached`-capture assert (line 163-171) is intact and would fire again on a re-detach. 5 new strict gates added. **4/4 suites PASS**, build green, `collection_drift: none`. |

---

## 2. Findings

### CRITICAL

#### C1 — The Task 9 count gate was bypassed on two published collection pages; the site now contradicts its own homepage

`articles.md:24`, `articles.md:25`, `articles.md:165` and `papers.md:18`

Published count numbers on **existing** pages changed, before the recount approval gate:

| Page / line | Published before (`db16e2c`) | Publishes now |
|---|---|---|
| `articles.md:24` subtitle | "57 works (2011-2020) from asadullahali.com" | **72** works |
| `articles.md:25` page-note | "15 works are preserved full-text …; 40 are available via the Wayback Machine only; 2 are lost … 87 CDX captures are preserved as metadata." | **47** full-text; **24** Wayback-only; **1** lost (the 87-capture sentence dropped) |
| `articles.md:165` Preservation Method | "57 canonical works identified from 87 Wayback Machine CDX captures. Full text of 30 works …; 40 are Wayback-only; 2 are lost." | "for **47** of the **72** works; **24** … Wayback-only and **1** is lost" |
| `papers.md:18` subtitle | "18 research papers and articles from Yaqeen Institute and academic journals." | **20** research papers |

Rendered, `_site/articles/index.html` reads: *"72 works from his own sites… 47 works are preserved full-text in this repository; 24 are available via the Wayback Machine only; 1 is lost with no archived copy located."*

**Why this is Critical.** This is not a new computed count for a structure that did not exist before — it replaces the pre-existing published totals of two existing pages. The checklist for this review makes any such change Critical, and the plan routes recounts through Task 9 with an explicit STOP. The numbers themselves are *correct* per the data (`works=72 found=47 wayback_only=24 lost=1`, `papers=20`); the violation is that they were published without approval.

The concrete harm is reader-visible self-contradiction. The homepage still says the opposite in four places:

- `index.md:30` — "57 works — 30 full-text in repo, 2 lost, 25 Wayback-only."
- `index.md:123` — "57 works — 30 full-text in repo, 2 lost, 25 Wayback-only"
- `index.md:141` — "Search across all 143 preserved items"
- `index.md:174-175` — table row "57" / "30 full-text in repo; 25 Wayback-only; 2 lost"

So `/` publishes 57 works / 30 full-text / 25 Wayback-only / 2 lost and `/articles/` publishes 72 / 47 / 24 / 1, at the same time, for the same collection.

**The process went the wrong way, and the ledger shows it.** 8c found precisely this class on `index.md` and correctly *declined* to fix it: "It is a count literal in another agent's file, so it waits for T9. I would not ship the site with it" (`task-8c-report.md:411-414`). 8a then rewrote `articles.md` and resolved the same contradiction from the other direction — by publishing the recount — and did not flag it. 8a's report §6 is headed *"Published headline numbers — untouched"* and only ever addresses `index.md`; §1 lists `articles.md` as "lost-works and about blocks re-pointed at computed counts" with no mention that this changes published totals. That is precisely the R24 failure mode the ledger adopted a rule against.

Note also that `index.md:30` still prints the arithmetically false identity `Total 203 = 57 + 68 + 18 + 17 + 9 + 36 + 1` — those seven terms sum to **206**, and `index.md:11`'s own comment uses 33, which makes the sum exactly 203. 8c filed that as its #1 defect. It is pre-existing and correctly parked, but see I-list ordering: it is now adjacent to a new block claiming 150 countable items in category A alone.

**Fix.** Restore the pre-`db16e2c` published figures on `articles.md:24`, `:25`, `:165` and `papers.md:18`, and keep only the genuinely new material: the MDI / notices / link-outs sections, the per-card category badges, and the per-category counts. The 72/47/24/1 and 20 figures are right and belong at Task 9, where they can be applied in one pass together with the homepage, `README.md` and the `36`-vs-`33` Al Balagh conflict.

---

### IMPORTANT

#### I1 — `videos.md:99` misdescribes its own category-C bucket and contradicts `index.md:69`

> "The remaining {{ c_videos }} are recordings of his appearances on other people's channels - debates organised by the Muslim Debate Initiative, **a lecture at another organisation**, and translated or clipped excerpts of those appearances…"

No category-C row is a lecture at another organisation. The two such recordings are `ZbcsxAoIVY0` ("Atheism: Doubting Your Doubts | Yaqeen in New York") and `IhE3ka7SQQs` ("Two Andalusians, One Conference"), and `_data/videos.json` puts **both in category A** — because 8a ruled he made those recordings, exactly as the taxonomy's own `ordering_rule` says. `index.md:69` states that rule on the homepage ("a talk he gave at someone else's hall [is] A").

So the sentence simultaneously (a) attributes to C a category of item that is not in C, and (b) contradicts the taxonomy rule published 30 lines above it on the same site. On a page whose stated purpose is honest provenance, that is not acceptable.

**Fix.** Delete "a lecture at another organisation," from the C description, or move it and say plainly that the two talks given at other organisations' halls are in A because he made them. The 11 C rows are: 5 MDI debates, 1 MDI-archive radio, 1 MDI clip, 2 Fakir Ilmu clips, 1 MSA Ohio State GBM event, 1 Persian upload, 1 short-form clip.

#### I2 — Ruling R25 is not in the ledger, so the durable evidence trail omits the one ruling in this phase that moved published numbers

`progress.md` ends at **R24** (`.superpowers/sdd/2026-09-27-full-recovery-v6/progress.md:103`); `grep R25 progress.md` → 0 hits. `docs/recovery-log/README.md:40` advertises the export as carrying "rulings **R0-R24**".

R25 changed: `_data/videos.json` (−1 line: the `transcripts: 0` key on `G47Stp3pLss`), `_data/transcript_coverage.json` (+3/−2: `attached_to_video_entry` → true, `attached_at`, note), two suite constants (`scripts/test_transcripts.py:60,62`: 56→57, 12→11), `_videos/G47Stp3pLss.md`, and the **published** 56→57 / 12→11 split on `videos.md` and `transcripts.md`.

R23 exists precisely so the evidence trail is durable in git rather than living only in the gitignored SDD workspace. The one Phase-3 ruling that changed published numbers is the one missing from it. The four `task-8*` reports are likewise still only in the SDD workspace.

**Fix.** Append R25 to `progress.md` (it is a real ruling: the user restored `G47Stp3pLss` as a counted work, which is what retired the "deliberately not attached" decision). Update `docs/recovery-log/README.md:40` to R0–R25, and export the four Task 8 reports at Task 9 per R23.

#### I3 — Typed numerals inside blocks that claim no number is typed

`index.md:69`, `articles.md:91`

`index.md:31-37` (8a's own comment) asserts: *"Every figure below is COUNTED FROM THE DATA at build time (Liquid loops over `_data/*.json`); **no number is typed here**."* Then `index.md:69` says "The **13** MDI rows that republish a work already in this list are catalogued but not counted again."

13 is `17 − 4`, and `articles.md:18` already computes exactly that as `mdi_republished`. So the literal is both stale-able and a false self-description of the block. Same class at `articles.md:91`: "**Seven of the seventeen** are under 100 words" — correct today (ledger Task 3: 7/17), typed, and it will not move if the data does. `taxonomy.json:71` has the same shape: `"secondary_sources (69), notices (3) and linkouts (10)"` as prose numbers.

**Fix.** `{{ mdi_total | minus: mdi_counted }}` at `index.md:69`; a computed loop at `articles.md:91`; derive or drop the numbers in `taxonomy.json:71`.

#### I4 — Report says the channel page cites timestamps "not files"; the built page prints 32 `_staging/` paths

`task-8b-report.md:85` — "the note that `_staging/` is temporary so the page cites timestamps, not files." The rendered `_site/channel/index.html` prints **32** `_staging/…` paths in its evidence column, e.g. `_staging/videos/discovery/pages/20180524110846.raw` and, in the rejected-claims cards, `_staging/videos/discovery/pages/20210904223751.raw`.

This is 8c defect-class 8 (dangling `_staging/` provenance, scheduled for deletion at Task 9.5) landing on a **published** page, and it contradicts the report's own claim about it. 8b's concern 5 acknowledges the class for `oembed_results.json` but not for the page's evidence column.

**Fix.** Either drop the path from the rendered table and keep the capture timestamp, or print the path together with its scheduled deletion date so a reader is not sent to a file that will not exist.

#### I5 — 8a's self-verification reports a page count that does not exist, and misses a URL collision

`task-8a-report.md:205` — "**146 post pages: 139 badged, 7 not.**"

Only **34** post pages build. `_posts/` holds 54 files; the site has 310 HTML pages total. Of the 34, 28 carry a badge and 6 do not.

8a's *substantive* claim does hold and I confirmed it: the post pages without a badge are exactly `build_collections.py`'s documented `UNCLAIMED_POSTS` set of 7 (`2015-05-12-still-colonized…`, `2017-12-22-the-atheistic-worldview…`, `2017-12-22-understanding-atheism`, `2018-05-09-islam-science-and-history`, `2018-06-20-atheism-doubting-your-doubts`, `2018-10-02-understanding-aishas-age…`, `2018-11-14-hard-questions…`), and rendering no badge there is the honest result. The seventh hides from a naive scan because it builds to `_site/articles/current issues/islamophobia/understanding-aishas-age-an-interdisciplinary-approach/index.html` — **inside the `/articles/` collection namespace**, because the post's `categories: [Articles, Current Issues, Islamophobia]` slugify to `articles/…`.

Also unreported: all 7 of those post pages are reachable **only by self-link**. Nothing in the site links to them (site-wide orphan count is 0 only because each page links to itself). 8a's "0 broken links" check cannot see this, because it tests href→target and never target←href.

Pre-existing, not a Phase-3 regression — but 8a offered this check as the evidence for the badge work, and it is wrong on the total and silent on two real defects.

**Fix.** Correct the report figure. Open a Task 9 item for (a) the `/articles/` namespace collision and (b) the 7 unlinked partial-capture post pages.

#### I6 — `timeline.md:31` still publishes the claim `rejected_claims[1]` refines

> `timeline.md:31` — `<div class="timeline-title">Original YouTube channel deleted/privatized</div>`

8d corrected exactly this claim in two other files in this diff — `videos.md:100` and `README.md:7` — and reported `timeline.md` as out of its ownership (`task-8d-report.md:244`, `§R9.4`). The site now states both: the videos page and the README say the channel was not deleted, the timeline says it was deleted/privatized.

Pre-existing and correctly reported rather than silently edited. But a known-false provenance claim must not survive to sign-off in an archive whose core value is honest provenance.

**Fix.** One-line change at Task 9, using the `README.md:7` wording.

#### I7 — `taxonomy.json:4` attributes the approval to an agent task

> `"approved_by": "site owner, 2026-09-27 (Task 8a)"`

The four categories were specified in the plan (Task 8a line: "A Works by Asadullah Ali / B Contributions & Collaborations / C Interviews, Reception & Mentions About Him / D Other Materials"), and the plan header records it as "Approved via grilling rounds 1–3 (2026-09-27)". Task 8a is an agent task, not an approval event, and the specific page renderings were never put to the owner. In a file whose job is provenance, the approval field points at the wrong artifact.

**Fix.** `"approved_by": "plan docs/superpowers/plans/2026-09-27-full-recovery-v6.md Task 8a (the four section names); plan approved via grilling rounds 1-3, 2026-09-27. Page renderings not yet put to the owner."`

---

### MINOR

- **M1** — `videos.md:98` publishes the flat claim "{{ a_videos }} of the {{ total }} videos were produced by The Andalusian Project" (57), which includes `G47Stp3pLss` — the one entry whose own `note` records the byline as **unverified** and the host as a third party. The `category_basis` disclosure exists in `_data/videos.json` and renders on that entry's own page, but not on the index. Consider a one-clause caveat on `videos.md`/`index.md`, or holding `G47Stp3pLss` out of the flat production claim until Checkpoint 2 settles R17.
- **M2** — `ROLE_NOTES["preserved-not-attached"]`, the `transcript_documents()` branch and the card tag at `transcripts.md:75` are unreachable in data after R25. 8d kept them deliberately and documented why (`§R9.3`) — correct. Recorded here only so a later agent does not "clean up" the mechanism a re-detach would need.
- **M3** — `_data/transcript_index.json` is generated but sits in the otherwise hand-maintained `_data/`. Its `generated_by` field is the only guard (`task-8d-report.md:§9.6`).
- **M4** — Capture-vs-published fidelity (37,381/37,388) is verified only by an ad-hoc script, not by a committed gate. The committed check (`scripts/test_transcripts.py:340-378`) is a **consistency** check — the article block and the published page are compared, but both derive from the same `parse_capture`, so a parser bug passes. The 7 documented `&nbsp;` paragraphs are the precedent for silent divergence.
- **M5** — `_layouts/paper.html:38` now prints the raw `publication_date` string, so paper pages show `2020` / `2020-03` where the rest of the site shows `March 12, 2020`. This removes a genuinely false "January 1970" (a real fix), at the cost of a visible format inconsistency. A `date:` filter guarded on the string's shape would restore consistency without reintroducing the bug.
- **M6** — The `category` / `counted` stamps on 189 rows were applied by an ad-hoc script that is **not in the repository** (`scripts/` was single-writer I1 and 8a did not edit it). The assignment is therefore not reproducible from the repo; `taxonomy.json → data_files` records the rationale per file, not the rule as executable code. Worth committing the stamping script, or a `make`-able equivalent, before Task 9 touches the numbers.
- **M7** — `_config.yml` sets `transcripts: permalink: /transcripts/:name/` while all 68 documents also carry an explicit `permalink:` front-matter key. The collection default is dead configuration for these pages. Harmless (it would protect a hand-added page) but it implies the `:name` slug is live when it is not.
- **M8** — `articles.md` also dropped the date range "(2011-2020)" from the subtitle. 8c had explicitly verified that range as correct (`task-8c-report.md:287-288`); its loss is an unremarked content regression in the same edit that produced C1.

---

## 3. ⚠️ Cannot verify from the diff / from the working tree

1. **The Wayback payloads behind `_data/channel_facts.json`'s 14 new capture rows.** The captures live in `_staging/videos/discovery/**`, which is scheduled for deletion and is not part of the reviewable state. I verified internal consistency (26 timeline rows, 29 UC-id mentions, 22 handle mentions, 0 forbidden URLs, subscriber series 7→18, rejected_claims 2→5, `do_not_link` intact) but **not** that each subscriber figure is the channel's own button and not a sidebar neighbour. 8b's §1.1 reasoning about `yt-subscription-button-subscriber-count-branded-horizontal` and `data-channel-external-id` is exactly the right check, but I could not re-run it. Same for the correctness of rejecting 585K / 329K / 1.01 million — I verified only that they are **rendered as rejected** and that the series tops out at 15.7K.
2. **Whether the 68 published transcripts are the *right* 68.** I verified 68/68 coverage-file captures are published, 0 orphans, 0 dangling, and that the 35 deleted `whisper-*.part<N>.json` intermediates are byte-recoverable from `db16e2c`. I did not re-derive the 10 merged whisper files from their parts to confirm element-wise identity (8c's proof), nor re-check that no capture was dropped upstream in Phase 1/2.
3. **Fidelity at scale for the whisper branch.** I spot-checked 2 of 39 whisper captures (67/67 and 238/238 paragraphs exact) plus 4 VTT files. 8d's corpus-wide figure (37,381/37,388) comes from an ad-hoc script that is not in the repo and I did not re-run it.
4. **The deployed site.** 8a asked whether the BOM bug is live in production. That needs the real host, which `scripts/deploy.sh` still placeholders — 8d hit the same wall (`§R3`) and correctly refused to invent a URL in `README.md`.
5. **Whether `G47Stp3pLss`'s recording is in fact his.** Open identity question (R17 / Checkpoint 2), not a Phase-3 matter. 8a's `A` assignment with a `category_basis` disclosure and 8d's attachment both preserve the ambiguity rather than resolving it, which is the right handling.

---

## 4. Verdict

**Is Phase 3 safe to keep? No — not as it stands. But the blocker is one localised, mechanical fix, and the substance underneath it is strong.**

This is a good phase. The taxonomy is real and computed, the authorship rule was genuinely applied rather than pattern-matched on the word "debate", the double-count audit comes out exact (164 = 150 + 3 + 11), the machine-transcript disclaimer is byte-verbatim on 69/69 built pages, `docs/` and every other non-site path are verifiably out of `_site`, no tracked file anywhere in the repo has a BOM, `_transcripts/` is tracked and gated, and **no gate got weaker** — `test_canonical_57.py` is untouched and `test_transcripts.py` is purely additive. The de-echo is provably safe: I confirmed the new word stream is an ordered subsequence of the old and that the author prose outside the transcript block is byte-identical to `db16e2c` in all three files. 4/4 suites and the build are green on my own run.

What stops it is that a *process* boundary was crossed. C1 is not a wrong number — it is the right numbers, published on the wrong side of an approval gate, in a way that leaves the homepage and the blog index stating incompatible totals for the same collection. This project exists to publish honest counts; shipping a site whose two count pages disagree is the one outcome the whole Task 9 gate was built to prevent.

**Must be fixed before this is kept:**
1. **C1** — restore the pre-`db16e2c` published figures on `articles.md:24`, `:25`, `:165` and `papers.md:18`; keep only the new sections. (Also restore "(2011-2020)", M8.) The 72/47/24/1 and 20 figures are correct and belong at Task 9.
2. **I1** — fix the C-bucket description at `videos.md:99`; it currently misfiles two category-A talks and contradicts the taxonomy rule on the homepage.
3. **I2** — add R25 to `progress.md` and bump `docs/recovery-log/README.md:40` to R0–R25; export the four Task 8 reports per R23.
4. **I3** — replace the typed numerals at `index.md:69` and `articles.md:91` with the values already computed, so the blocks' own "no number is typed here" claim becomes true.

**Can ride into Task 9** (all reported, none hidden): I4 (`_staging/` paths on the channel page), I5 (146→34 page count; `/articles/` namespace collision; 7 unlinked post pages), I6 (`timeline.md:31`), I7 (`approved_by`), and M1–M8. Task 9 should also close the parked `index.md:30` false arithmetic (`203 = …` sums to 206) that 8c filed and that C1 now compounds, and reconcile the homepage grid with the taxonomy block in the same pass rather than leaving two count systems to drift.
