# Recovery log

A committed record of the **2026-09-27 full recovery** of The Andalusian Project archive:
what was recovered, what was decided, and what was independently checked. This directory
exists so that the evidence trail for the Phase 2 integration commit has a durable home in
git rather than living only in a gitignored scratch workspace on one disk.

## Why this directory exists

The recovery ran under a superpowers SDD ledger at
`.superpowers/sdd/2026-09-27-full-recovery-v6/`. That tree's `.gitignore` contains `*`, so
every brief, lane report, integrator report, manifest, review and the integration log are
**untracked by design** — the ledger is scratch space. The independent Phase 2 review
raised this as finding **M8**: the entire evidence trail for a **3.2 MB, 127-file
integration commit** lived on a single disk with no history and would be lost with it.

Ledger ruling **R23** scheduled the remedy: export a curated record to `docs/recovery-log/`
so the commit has provenance a reader can find without access to the scratch tree. This
directory is that export. `.gitignore` itself was deliberately left untouched.

The Phase 3 review repeated the finding as **I2**, one step sharper: R23 had been satisfied for
Phase 2 while the *one ruling in Phase 3 that moved published numbers* — R25, which attached
`G47Stp3pLss`'s transcript and moved the published 56/12 split to 57/11 — and all four Phase 3
implementer reports stayed in the scratch tree. Both are here now, so the rule is applied to
every phase rather than the first one that needed it.

## What is in here

| File | What it is | Source in the ledger |
|---|---|---|
| [`2026-09-27-integration-log.md`](2026-09-27-integration-log.md) | Every item Phase 2 moved, one line each: `slug → source lane → verdict → destination`. 190 lines, append-only by both integrators. | `integration_log.md`, copied byte-identical |
| [`2026-09-27-review-phase2.md`](2026-09-27-review-phase2.md) | The independent review of commit `7e32c28` → `9b431ef`: 2 Critical, 7 Important, 11 Minor findings, plus 8 items it could not verify from the diff. | `review-phase2.md`, copied byte-identical |
| [`2026-09-27-re-reviews.md`](2026-09-27-re-reviews.md) | Two further independent reviews, verbatim: round 1 of the fix wave (`9b431ef` → `f0ba4e7`, 21 findings, 21 ADDRESSED), and round 2 of the follow-up fixes (findings N1 and N2, both ADDRESSED). | `re-review-phase2-fixes.md` + `re-review-round2.md`, concatenated with a marked separator; neither document edited |
| [`2026-09-27-phase-1-lane-manifests.md`](2026-09-27-phase-1-lane-manifests.md) | Per-lane counts and provenance for the six Phase 1 recovery lanes (posts / images / pages / pdfs / videos), each with its report path. | Authored from the six `_staging/*/MANIFEST.md` files; counts only, no raw artefacts |
| [`2026-09-27-review-phase3.md`](2026-09-27-review-phase3.md) | The independent review of Phase 3 / Task 8, `db16e2c` → `8eaa65f`: 1 Critical (C1, the Task 9 count gate bypassed on two published collection pages), 7 Important, 8 Minor, plus 5 items it could not verify. | `review-phase3.md`, copied byte-identical |
| [`2026-09-27-phase-3-lane-reports.md`](2026-09-27-phase-3-lane-reports.md) | The four Phase 3 implementer reports, verbatim: 8a (the four-category taxonomy), 8b (the channel record), 8c (transcript inventory and hygiene), 8d (68 published transcript documents). ~130 KB. | `task-8a-report.md` + `task-8b-report.md` + `task-8c-report.md` + `task-8d-report.md`, concatenated with a marked separator; no document edited |

The copied files are byte-identical to their sources; each concatenation preserves every
source document exactly, separated by an HTML comment that marks the join.

## How this relates to the plan and the ledger

- **Plan:** [`docs/superpowers/plans/2026-09-27-full-recovery-v6.md`](../superpowers/plans/2026-09-27-full-recovery-v6.md)
  — the spec. Tasks 0–6 are Phase 0–1, Task 7 is the Phase 2 integration, Tasks 8–9 are
  Phase 3–4. **This directory is not part of the plan**; it is the R23 export of the plan's
  own working papers.
- **Ledger:** `.superpowers/sdd/2026-09-27-full-recovery-v6/progress.md` — the running record
  with rulings **R0–R25**, the conflict scan, the Phase 1/2 lane summaries, the Phase 3 rulings
  (R25–R29, which is where the transcript attachment, the BOM, the `docs/` leak and the C1
  reversal are recorded), the user's Checkpoint 1 and Checkpoint 2 decisions, and the
  controller's own verification notes. It remains untracked; the rulings that matter are cited
  by number in the files above.
- **Commit trail.** The integration landed as three commits: `9b431ef` (the 127-file, 3.2 MB
  integration), `f0ba4e7` (checkpoint-2 decisions + the Phase 2 fix wave) and `db16e2c` (the
  round-2 fix). Phase 3 landed as `b92499a` (8a/8b/8c) and `8eaa65f` (8d + residue pass), and
  the Phase-3 review fix wave followed it. Rulings R15 and R22 record why the Phase 2 work was
  committed coarsely rather than split further.

## Date range

- **Recovery work:** 2026-09-27. Phase 1 lane manifests were generated between
  `09:05:36Z` and `14:33:13+05:30`; integration and both review rounds followed the same day.
- **Content covered by the recovery:** 2010-09-20 (earliest recovered post, `quran`) to
  2026-09-27 (the live-channel check and the IDI capture). Wayback enumeration reached back
  to 2007 captures; the recovered works themselves span 2011-12-18 to 2020-08-11.
- **Files dated `2026-09-27-`:** the date the recovery ran, not the date of the content.

## What is deliberately absent

- **Raw artefacts.** The six Phase 1 lanes staged ~144 MB of HTML, images, PDFs and raw
  captures under the gitignored `_staging/`, which is scheduled for deletion at Task 9.5.
  Counts and provenance are recorded instead.
- **The lane briefs, lane reports and integrator reports** (`task-1`…`task-7-I2`). They stay
  in the scratch tree. Where a lane's numbers matter to a published claim, they are restated
  in [`2026-09-27-phase-1-lane-manifests.md`](2026-09-27-phase-1-lane-manifests.md). The four
  **Phase 3** implementer reports are the exception and are now exported, because Phase 3 is
  where the taxonomy, the channel record and the published transcripts were decided.
- **The raw review diffs** (3.2 MB, 909 KB, 5.8 MB). The review documents that interpret them are
  here; the diffs themselves are reproducible with `git diff`.
- **The Phase 3 implementer briefs** (`task-8a`…`task-8d-brief.md`) and the fix-wave brief and
  report for the Phase 3 review. They stay in the scratch tree; the reviews that ordered the
  work are here, which is what makes the work auditable.
- **The Phase 4 material** (Task 9), which does not exist yet.

## Reading order

1. [`2026-09-27-integration-log.md`](2026-09-27-integration-log.md) — what actually changed.
2. [`2026-09-27-review-phase2.md`](2026-09-27-review-phase2.md) — what was wrong with it.
3. [`2026-09-27-re-reviews.md`](2026-09-27-re-reviews.md) — proof the findings were fixed.
4. [`2026-09-27-phase-1-lane-manifests.md`](2026-09-27-phase-1-lane-manifests.md) — where the
   material came from.
5. [`2026-09-27-phase-3-lane-reports.md`](2026-09-27-phase-3-lane-reports.md) — what Phase 3
   decided and built.
6. [`2026-09-27-review-phase3.md`](2026-09-27-review-phase3.md) — what was wrong with that, and
   in particular the C1 count-gate breach that the fix wave reversed.

## Counts in this directory

These files describe the recovery, so they are not subject to the site's count-approval gate.
Where they state a number it is the number as of **2026-09-27 at `db16e2c`**, except in
[`2026-09-27-review-phase3.md`](2026-09-27-review-phase3.md) and
[`2026-09-27-phase-3-lane-reports.md`](2026-09-27-phase-3-lane-reports.md), which describe Phase 3
and therefore the state at `8eaa65f` and after the fix wave. **None of them has been edited by the
2026-09-28 recount**, and none should be: a review record is evidence of what was true when it was
written, and rewriting it would destroy the only reason to keep it.

The count-approval gate is now **closed**. The site owner approved the recount and it was applied
on 2026-09-28 in one pass, so `README.md`, `index.md`, `articles.md`, `papers.md`, `search.md` and
`timeline.md` publish the recount values (72 works / 47 full-text / 24 Wayback-only / 1 lost;
20 papers; a computed total of 207) and every count on those pages is now read from `_data/` at
build time instead of being typed. The history of the gate itself — Phase 3 publishing the recount
ahead of approval on `articles.md` and `papers.md`, the review catching it as **C1**, and the fix
wave restoring the pre-recount figures — is recorded in
[`2026-09-27-review-phase3.md`](2026-09-27-review-phase3.md) and in the ledger ruling **R29**, and
is left exactly as it was written.

## The `checked` dates in `_data/recovery_log.json` (2026-09-28)

`recovery_log.json` carries 74 rows, each with a `checked` date. **54 of them read
`2026-09-11` and 20 read `2026-09-27`**, which looks like a stale field on the first block: every
one of the 19 rows dated 2026-09-27 is a Phase 1 lane row, and the Phase 1 manifests are all dated
2026-09-27. The 2026-09-27 recount flagged it (finding 6.5) as unresolvable from the repository and
deliberately kept the date off the public timeline. It is resolvable, and the answer is that
**2026-09-11 is a genuine historical record, not a stale field**, so those 54 dates were left alone:

* The 2026-09-11 rows are written by `scripts/fetch_blog_content.py`, which stamps
  `method: "wayback-refetch"` and this exact row shape. That script dates its own refetch work to
  2026-09-11 in two places — `Task R (2026-09-11): hardened ad/JS junk stripping for the article
  track` and `Task R (2026-09-11): keep-better guardrail + all-37 refetch support`.
* The dispatch that ran it is on the record: `.superpowers/sdd/2026-09-06-57-list-honest-counts/`
  holds `fix-wave-report.md` ("Fix-wave report (2026-09-11, single dispatch, no subagents)") and
  `task-R-report.md` ("Date: 2026-09-11. Implementer: Task R (article track)."). So the pass is in
  the ledger after all, just in the *earlier* ledger, not the 2026-09-27 one.
* The Phase 1 lane that re-checked the same 30 works on 2026-09-27 — F4, the `asadullahali.com`
  best-capture re-fetch — **did not write this file at all**. Its own report closes with "Writes
  confined to `_staging\best_capture\`". F4 could not and did not re-date a row it never wrote.
* The row shapes agree. The 2026-09-11 rows carry `words` / `fetched_title` / `categories` / `tags` /
  `comments` and no `content_file` / `fetched_words` / `guardrail`; the 2026-09-27 rows carry all
  three of those. Two different passes, two different shapes, and the dates distinguish them
  correctly.

One row in that block **was** factually wrong and was corrected on 2026-09-28:
`library-take-down-notice` read `checked: 2026-09-11` with `words: 0`, `source_url: null` and
`verdict: skipped_no_url` — the record of the 2026-09-11 pass, which found nothing — and was never
updated when lane F2 recovered the work on 2026-09-27. It now reads `2026-09-27`, 216 words, the
capture it came from, and `stub_fill`. That is the whole 55 → 54 difference. `checked` therefore
means *the date this row's own pass ran*, not *the date the work was last looked at by anybody*.

What is **not** settled, and is left visible rather than papered over: F4's 8 adopted "fuller
versions" (in `_staging/best_capture/fuller_than_local.json`) were fetched on 2026-09-27, but their
rows still read `checked: 2026-09-11`. Their `words` figures are not directly comparable to F4's
either — the log counts fetched text and F4 counts the archive's own file, so `backbone-ribs` reads
19,671 in the log against F4's `local_words` of 19,716. Nothing was rewritten, because a correction
here would have to be a judgement about which word count is right, and that is a decision for the
ledger's owner, not a cleanup.
