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
and therefore the state at `8eaa65f` and after the fix wave.

The site's own published totals (`README.md`, `index.md`, `articles.md`, `papers.md`) are a
separate matter and are still awaiting the site owner's approval at Task 9. Phase 3 briefly
published the recount on `articles.md` and `papers.md` before that gate; the review caught it as
**C1** and the fix wave restored the pre-recount figures, so the published counts are once again
the approved ones. The recount values themselves (72 works / 47 full-text / 24 Wayback-only /
1 lost; 20 papers) are correct in `_data/`, and belong to Task 9 applied in one pass with the
homepage and `README.md`.
