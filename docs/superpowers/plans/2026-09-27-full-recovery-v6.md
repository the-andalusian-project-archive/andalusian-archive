# Full Recovery v6 — Andalusian Archive

Approved via grilling rounds 1–3 (2026-09-27). Execution: Phases 0–4, user checkpoint after each of Phases 1, 2, 3, and a recount approval gate inside Phase 4.

## Context

The archive at `D:\The Andalusian Project\andalusian-archive` (Jekyll) currently reports 57 works / 68 videos / 18 papers / 203 total_content from a 2026-09-06 recovery. Research proved far more recoverable text exists: a WordPress mirror API (38 posts), 22 deleted mirror posts (17 untracked + 2 stub-fills), 17 MDI posts, ~452 evolving-snapshot candidates on the dead asadullahali.com, academic OA papers (5 already downloaded to temp), and 121 live YouTube videos (53 new). This plan recovers all of it legally, integrates it, adds UI/taxonomy, then recounts honestly (diff shown to the user before anything applies).

## Global Constraints

1. **Repo writes**: only `_staging/<lane>/` during Phase 1; `_data/`, `_posts/`, `_papers/`, `_articles/`, `data/`, `scripts/`, layouts only during Phase 2/3 (single-writer per file).
2. **Git**: controller (lead) runs all `git commit` — never a worker (index-lock race). Commit messages `task-N: <what moved>`. No `git push`, ever, until the user explicitly orders one. `.env`, `_site/`, `.jekyll-cache/`, `vendor/`, `node_modules/`, `scripts/__pycache__/`, `_staging/` are gitignored.
3. **Network**: polite serial Wayback (≥0.5 s between bulk requests). Never fetch live `asadullahali.com` (hijacked → gambling spam); Wayback only. ≤2022 snapshots for YouTube channel captures. YouTube oEmbed/id checks are fine. **Firecrawl/Exa only if ordinary web fetch fails**, hard cap 200 credits total, log any spend; prefer retries with plain HTTP first.
4. **Legal/ethical**: no paywall/robots circumvention. Yaqeen papers = link-outs only (never download PDFs). Conversion story = link-out metadata entry ONLY, no local text copy (user decision Q5=b). Facebook = login-walled, record as unrecovered. IIUM full thesis 401 → record `restricted`. Byline gate: any page authored by "Abdullah Al-Andalusi"/MDI-London (different person) must NOT enter the corpus.
5. **Counts stay meaning-preserving**: buckets never merge; videos never double-counted (mirrors attach as `mirror_urls`); `secondary_sources` derived and uncounted; new videos catalogue-only (`transcripts: 0`) — baseline gate 68/68 transcripts untouched.
6. **Disclaimer** (transcripts page + video pages, verbatim): "*Transcript by machine — accuracy isn't perfect, so it shouldn't be used in polemics or debate material as an authoritative source.*"
7. **Environment**: Windows PowerShell; `python` not `python3`; avoid nested quotes/f-strings in `python -c`; workers never dispatch subagents; worker reports go to report files, not long chat dumps.
8. **Staging**: every lane writes `MANIFEST.md` + `manifest.json` (`[{path, source_url, retrieved_at, http_status, notes}]`) + `REPORT.md` in its lane dir. `_staging/` is deleted after Phase 4 (manifests/reports preserved in `.superpowers/sdd/`).
9. **Concurrency**: ≤6 agents at once; lanes are disjoint single-writer directories.

## Task 0: Phase 0 — baseline (controller, inline)

- Suites baseline: `python -B scripts/test_no_junk.py`, `test_canonical_57.py`, `test_search_sync.py`, `test_transcripts.py` (all green pre-flight).
- `bundle exec jekyll build` green.
- `git init -b main` (+ local identity if unset), `.gitignore` per Global Constraint 2.
- Open SDD ledger, run conflict scan, **Commit 0** = baseline snapshot.

## Task 1: Lane F1 — WordPress mirror posts + images

**Goal:** stage all 38 mirror posts as text, full evidence for the 4 mirror-fuller works, all post images, and the comic assets.

**Inputs:** API `https://public-api.wordpress.com/wp/v2/sites/asadullahali.wordpress.com/posts?per_page=100` (fresh pull; sanity-diff against `%TEMP%\opencode\mirror_posts.json` 1.7 MB if present — report any drift). Known quality audit: 4 MIRROR_FULLER = `reviewing-haqiqatjou` (+14,366 w), `backbone-ribs` (+643), `archetype` (+51), `narrative` (+53); 1 LOCAL_FULLER = `adam-is-no-myth` (keep local, record +53 w merge paragraph as `evidence/local_fuller_adam-is-no-myth.txt`).

**Deliverables (`_staging/mirror/`):**
- `posts/<slug>.json` (raw API record) + `posts/<slug>.txt` (extracted plain text) for all 38.
- `evidence/wordcounts.csv`: slug, local_w, mirror_w, verdict (MIRROR_FULLER / LOCAL_FULLER / EQUAL / STUB).
- `images/`: every image URL referenced by the 38 posts (mirror CDN `i0.wp.com`…), named `NNN_<basename>`; record original URL in manifest. Plus `backboneribspdf-2.pdf` and the 23 ijihad comic slide images if referenced.
- `MANIFEST.md`, `manifest.json`, `REPORT.md`.

**Rules:** serial polite fetch; if an image 404s, note and continue (no retries beyond 2); API pagination until exhausted; expected ≈38 posts, ≈334 images.

**Report contract:** DONE + counts line (posts/images/pdf) + concerns.

## Task 2: Lane F2 — deleted mirror posts + stub-fills

**Goal:** recover text for the 22 deleted posts of `asadullahali.wordpress.com` (17 untracked + verification of the 5 already-tracked) and fill 2 stubs.

**Inputs:** fresh CDX enumeration `https://web.archive.org/cdx/search/cdx?url=asadullahali.wordpress.com/*&output=json&filter=statuscode:200&collapse=digest` (re-derive; do not trust memory). Known untracked set (ts): `happymuslim-inferioritycomplex` 20140718192323 (460 w), `contra-contemporary-atheism-lecture` 20141015041328 (156 w stub, Farizmi embeds), `prophets-vs-pedophiles-part-2/-3`, `who-justifies-terrorism-part-1/-2`, `the-fraud-of-islamic-mint-nusantara`, `qatar-timbuktu-and-an-arab-rescue`, `the-sword-of-ibn-nasir`, `hitchslapping-*`, `against-atheist-aesthetics`, `how-to-know-no-thing`, `the-collaborative-couple`, `a-quick-response`, `more-additions`, `nothing`, `islam` (2012), `quran` (2010). Stub-fills: `the-inhumanity-of-human-rights` ts 20120313034043 (lost→found), `library-take-down-notice` ts 20140507224757.
Also stage `religion-vs-paedophilia-part-1/2/3` from muslimdebate.org (author id `16585639`, 3,685/1,466/2,095 w) into `candidate_duplicates/` — possible duplicates of prophets-vs-pedophiles; flag in REPORT, integrator decides.

**Deliverables (`_staging/deleted/`):** `posts/<slug>.html` + `.txt` per recovered post, `stubs/` for the 2 fills (record old vs new word count), `candidate_duplicates/`, manifest trio, REPORT.

**Rules:** Wayback serial ≥0.5 s; pick highest-quality capture ≤ snapshot of deletion era; never live domain.

**Report contract:** DONE + counts (recovered/stub-fills/candidates) + per-post status table in REPORT + concerns.

## Task 3: Lane F3 — MDI posts (17)

**Goal:** full text of the 17 Asadullah posts on muslimdebate.org (author `16585639`) to verify they are his and match/extend `_data/mdi_articles.json`.

**Inputs:** CDX or live fetch of `muslimdebate.org/?author=16585639` listings + per-post pages (site is not him — read-only fetch fine). Compare title/date/slug against `_data/mdi_articles.json` (17 entries).

**Deliverables (`_staging/mdi/`):** `posts/<slug>.txt` + `.json` ({title, date, url, words, mdi_json_match: exact|differs|missing}), `crosscheck.md` (any title/date mismatches vs mirror-deleted posts — esp. prophets-vs-pedophiles vs religion-vs-paedophilia), manifest trio, REPORT.

**Report contract:** DONE + counts (17 fetched / matches / diffs) + concerns.

## Task 4: Lane F4 — asadullahali.com best-capture re-fetch

**Goal:** re-fetch the best Wayback capture for every evolving content URL on his dead personal site.

**Inputs:** existing CDX artifacts in `%TEMP%\opencode\` (`cdx.json`, `cdx_raw.json`, `aw_domain.json`, `norm.json`, `buckets.json`, `datearch.json`, `extras_final.json` — reuse if consistent with a fresh CDX query; else re-enumerate). Known: 4,723 CDX rows → 1,031 URLs → 452 evolution candidates.

**Target:** content pages only — after filtering out images/CSS/JS/404s/empties, expect ≈180 pages (REPORT must state actual vs expected and why).

**Deliverables (`_staging/best_capture/`):** `pages/<host>_<path-slug>.txt` (+ `.html`), `selection.csv` (url, chosen_capture, bytes, words, reason for rejected candidates), manifest trio, REPORT. Prefer capture with max words; tie-break earlier date.

**Rules:** Wayback serial ≥0.5 s (this is the largest lane — throttle, no parallel inside lane); never live domain; skip any URL whose capture content is login/placeholder (<100 w) — record as skipped.

**Report contract:** DONE + counts (candidates → selected → skipped) + concerns.

## Task 5: Lane F5 — academic papers, secondary sources, link-outs

**Goal:** legally obtain every OA academic text; record restricted/dead ones honestly; build link-out entries.

**Inputs:**
- Reuse `%TEMP%\opencode\`: `gender_equality.pdf`, `gender_equality_jp.pdf`, `iium_thesis.pdf`, `rise_decline_icr.pdf`, `sallahuddin_ayubi_iais.pdf` (copy into staging; verify each opens / page count > 0).
- Academia.edu open PDFs (independent): IDs `37974215, 32865802, 19782374, 18640397, 12984545, 13215503` (+ 7 talk PDFs if listed on the profile page).
- AMJA 31 pp "Deconstructing Contemporary Atheist Thought" (search amja.org / web if direct URL fails).
- DOI resolve checks (HEAD/GET): `10.12816/0019168`, `10.12816/0019212`, `10.12816/0009888`, `10.52282/icr.v6i2.333`, `10.65061/hdxb1161` → landing URL, OA status, download if OA.
- IDI "Apostasy: Beyond the Rhetoric" (~2,500 w article) → full text page capture (his authored work → countable).
- Conversion story (~1,100 w, birth name, redacted at publication time as `‖ birth name withheld ‖`) → **metadata only** (title, URL, Wayback URL, word count if visible in snippet, author note) in `linkouts.json`. No body text.
- Yaqeen 9 → **link-outs only** in `linkouts.json`.
- `secondary_sources`: verify/extend the derived 52-list with URLs (reprints, critiques, bios) — records only, no full-text capture of third-party criticism beyond brief metadata.

**Deliverables (`_staging/secondary/`):** `papers/*.pdf` + `papers.csv` (title, source_url, pages, oa|restricted|dead), `linkouts.json`, `secondary_sources.csv`, `dois.csv`, manifest trio, REPORT.

**Report contract:** DONE + counts (pdfs obtained / link-outs / doi statuses / restricted) + concerns.

## Task 6: Lane F6 — video catalogue (121) + mirror mapping

**Goal:** verify all 121 candidate video IDs are live; draft the 53 new entries; map the 65 live mirrors to baseline with the strict rule; prepare transcripts:0 entries.

**Inputs:** prior sweep results (in session): `@archivedandalusianproject` (33 v), Arena 11 episodes (~48 h), Shirkuh re-uploads (10–23), "Abduallah amin" 88-video playlist, Wayback playlist capture 20201007152603 (57 titles+IDs), 68 baseline IDs from `_data/videos.json`, 65 live mirrors of baseline. Note: `ap_*.json` temp lists are GONE — re-derive from Wayback playlist captures + channel `videos` tab captures (≤2022) + oEmbed discovery; do not trust memory, verify each ID.

**Method:** for each candidate ID: `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<id>&format=json` (serial, ~0.3 s) → alive (title, author, duration unavailable) or dead. Wayback `av` for duration when needed for mapping.

**Mirror rule (strict):** attach to baseline entry only on normalized-exact title match AND (duration within 60 s OR same-uploader playlist context); everything else → `_staging/videos/unmapped_mirrors.json`, counted nowhere.

**Deliverables (`_staging/videos/`):**
- `videos_new.json` — 53 (±) new entries, schema mirror of `_data/videos.json` entries + `kind` (lecture|interview|appearance|clip|series-episode) + `transcripts: 0` + `source` note.
- `mirrors.json` — [{baseline_id, live_url, match_basis}] for mapped; `unmapped_mirrors.json` for parked.
- `verify.csv` — all 121 candidate IDs: alive/dead/title.
- manifest trio, REPORT.

**Rules:** catalogue-only — **no transcript work**; if >5% of oEmbed calls error, pause and report BLOCKED (possible rate-limit) rather than hammering.

**Report contract:** DONE + counts (alive/dead, new entries, mapped/unmapped mirrors) + concerns.

## Task 7: Phase 2 — integration (two integrators, parallel, single-writer)

Spec revised 2026-09-27 after Checkpoint 1 (user decisions folded in; Phase-1 evidence supersedes the earlier estimates). Inputs: staged lane artifacts under `_staging/{mirror,deleted,mdi,best_capture,secondary,videos}/`; lane reports in the SDD workspace; F6's `baseline_duplicates.json`, `videos_new.json`, `mirrors.json`, `unmapped_mirrors.json`, `verify.csv`; F5's `papers.csv`, `linkouts.json`, `secondary_sources.csv`, `dois.csv`; F2's `posts/*.txt`, `stubs/`, `candidate_duplicates/`; F1's `evidence/wordcounts.csv` + `wordcounts_detail.csv`; F4's `fuller_than_local.json`.

**I1 — text-data integrator** — owns `_data/canonical_57.json`→`_data/canonical_works.json`, `_posts/`, `_articles/`, `_papers/`, `_data/papers.json`, `_data/lost_works.json`, `_data/mdi_articles.json`, `_data/secondary_sources.json`, `_data/bibliography.json`, `_data/linkouts.json`, `data/` search copies, and **ALL of `scripts/`** (per R2 — I2 must not touch `scripts/`):
1. **Nine named fuller-version adoptions** (per-work diff; mirror and wayback candidates diffed, **never summed**; adopt the single best text): `reviewing-haqiqatjou` +14,607 (mirror) · `backbone-ribs` +366/+282 · `the-archetype-of-beauty-in-islam` +106/+82 · `the-narrative-of-happymuslims` +57/+35 · `the-rationality-…-part-1` +62/+79 · `the-rationality-…-part-2-2` +105/+27 · `malaysias-tiger-in-waiting` +39 (wayback) · `prophets-vs-pedophiles-part-1` +22 · `the-rise-and-decline-of-scientific-productivity-…` +16.
2. `adam-is-no-myth`: **no merge** (the +53 w "paragraph" was a method artifact; mirror residue is 19 w). Repair only the 6 token-welded artifacts (`hispaperfound`, `theOxford`, …) in the local file.
3. **15 net-new works** from F2's 17 untracked (R9: `prophets-vs-pedophiles-part-1` ≡ `religion-vs-paedophilia-1` ≡ MDI part 3 = ONE work carrying three provenance records; R12: 3 announcements recorded as notices, never counted). Follow the existing slug-named `_posts/`/`_articles/` convention, `status: found`, with `wayback_url` + provenance note.
4. **2 stub-fills**: extend the existing stubs with staged text. `the-inhumanity-of-human-rights` moves lost→found (629 w; record that no Part 2 exists in any capture).
5. **MDI**: store the 17 staged texts in the corpus (previously URL-only). `_data/mdi_articles.json` stays at 17 (F3 found 0 new candidates, 0 byline mismatches). 7 of 17 are <100-word captions — keep as they are; the text is now local.
6. **F4**: 0 new works. Its 30 selected works become `wayback_url` alternates where better than the archive's existing capture; 22 reproduce the existing timestamp exactly (record, do not churn).
7. **`bibliography.json` FIRST, before any count edit**: all 24 `papers.csv` rows (title, source_url, status `oa|restricted|dead`, notes) + the 2 conference reports + the 5 DOIs. Then `_data/papers.json` grows only by legitimately obtained texts (18 → ~20–22; exact figure comes from the Phase-4 recount).
8. **`linkouts.json`**: conversion story = metadata only (title, URL, Wayback URL, word count, one neutral sentence — **never its body text**, user decision) + the 9 Yaqeen papers (link-outs only, license).
9. **`secondary_sources.json`**: replace the mojibake titles with F5's 69 clean rows.
10. **`lost_works.json`**: 2 → 1 (only the still-unrecovered work remains).
11. **IDI "Apostasy: Beyond the Rhetoric"** (2,272 w staged) files as a Category-A **work, not a paper** (R4). Log that it is a near-duplicate of the mirror's "Naked Kings in the Information Age" — do not double-count.
12. **Rename `_data/canonical_57.json` → `_data/canonical_works.json`** atomically: grep every `canonical_57` reference (the `data/` copy, `scripts/test_canonical_57.py`, `scripts/test_search_sync.py`, `scripts/build_collections.py`, `scripts/build_canonical_57.py`, `scripts/build_content_index.py`, `timeline.md`, plan docs) and update. Script filenames may stay; the data file must be renamed.
13. **Transcript preservation** (after I2's video set lands — the controller sequences this step): for each of the 12 superseded videos, re-parent its transcript row/text onto the surviving twin (as the twin's transcript, or an `alternates` list if the twin has its own). **Never delete transcript text.** Then set the honest gate in `test_transcripts.py` to survivor-count/survivor-count (56/56 baseline + 11 catalogue-only with `transcripts: 0`) and state old→new gate numbers explicitly in the report.
14. Update every test expectation to the new honest numbers so all 4 suites pass. Never weaken an assert unrelated to a count change; list every changed expectation in the report.

**I2 — media-data integrator** — owns `_data/videos.json`, `data/videos.json`, `_data/superseded_videos.json`, `_data/unmapped_mirrors.json`, `_data/channel_facts.json`:
1. **FIRST write `_data/superseded_videos.json`** (user decision: their titles must be preserved): the 12 `"source": "YouTube mirror"` duplicates — `EK5oppX6C2U`, `fq1WejCHgXs`, `4maSZMzhmuI`, `kDH1BOyhhYk`, `eQ-frTAlcJc`, `hURJIIm0tSY`, `D2t0idkAqjA`, `YjGHZwdM7XU`, `xhnU-1dNi3I`, `G47Stp3pLss`, `bRTI6Z5gggE`, `2tsI80MDUOI` — each with its full record, the archive.org twin it duplicates (F6's `baseline_duplicates.json`), and the reason.
2. Remove those 12 from `_data/videos.json`, attaching each as `mirror_urls` on its twin → 68 → 56.
3. Append F6's **11** new entries from `videos_new.json` with `kind` + `transcripts: 0` → **67**.
4. Promote F6's 12 parked mirrors into `mirror_urls` on their baseline entries — re-verify each pairing against F6's duration data first (Δ<1 s is the evidence); any pairing without duration evidence stays parked in `unmapped_mirrors.json`.
5. Add `mirror_urls: []` to every entry (schema grows; never remove a field).
6. **`channel_facts.json`**: the verified timeline — his own header shows 14.4 K subs in the 2021 capture, and the subscriber series runs 190 → 6.97 K → 11.2 K → 14.4 K → 15.7 K; emptied Oct 2022 · re-registered 2023 as `@andalusianproject6093` with 84 videos / 15.4 K subs (2023 captures; canonical link = his UC id) · captures `20250820` and `20260819` show 0 videos · **live check 2026-09-27 → "This channel is not available."** Mark the handle as NOT his: never link it, never link the live UC id. **Rejected claim**: the widely-repeated "585 K subscribers" figure belongs to a *different* channel (that capture block's `navigationEndpoint` points at `UC3vHW2h22WE-…`); it is recorded in `channel_facts.json → rejected_claims` and must never appear in the archive.
7. **Do NOT touch `scripts/`, `transcript_coverage.json`, or any transcript file** (I1 owns that reconciliation). If a suite run fails only on a video-count or transcript-row assert, report the exact one-line change needed instead of editing it.
8. Sync `data/videos.json`.

**Both:**
- Log every adoption/removal to the SDD workspace `integration_log.md`: slug/id → source → verdict → destination path.
- No git commands (the controller commits). No subagents.
- After both streams land: all 4 suites + `bundle exec jekyll build` green (the build may write `_site/`).
- Report contract: status `DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT`, files touched, counts in→out, suite results, transcript gate old→new, concerns. Full report to `task-7-I1-report.md` and `task-7-I2-report.md` in the SDD workspace.

**Report contract:** each integrator: DONE + (files touched, counts in/out, suites run + result) + concerns.

## Task 8: Phase 3 — code & UI (two agents, parallel, single-writer)

**8a — layouts/UI:** category taxonomy + homepage: `index.md` restructured into 4 sections (A Works by Asadullah Ali / B Contributions & Collaborations / C Interviews, Reception & Mentions About Him / D Other Materials), category badges on detail pages (`_layouts/work`, `video`, `paper`, `article` as applicable), co-authored flags on papers page; collection pages keep chronological lists. Video page gains transcript display when a transcript exists (respect disclaimer verbatim), `transcripts: 0` renders "transcript not yet available" — gate 68/68 untouched.
**8b — channel backfill:** add channel facts (21 ≤2022 Wayback captures: about 20220320030541, playlists 20201007152603, videos 20191030013134, community 20201111194329) into the channel page; 65 mirrors already in videos via I2.
**8c — closes & hygiene:** `Closes-Section-*` additions for newly closed items (incl. ijihad-1 NO-MATCH finalization if evidence landed), delete leftover `part-*.json` whisper files in `.firecrawl/transcripts/`, README/index stale counts (36-vs-33, 261) deferred to Task 9 recount — but structural contradictions fixed now if trivial.

Suites + build green at end. Controller commits `task-7: …` etc. as reports land (one commit per sub-task).

## Task 9: Phase 4 — recount, gates, reviewers

1. **Recount diff (controller):** run `scripts/build_collections.py`-style audit + hand recount → table: field, old, new (works 57→?, videos 68→121, papers 18→23, lost 2→1, external_interviews 1→?, total_content →?). **STOP — user approval required before applying count changes.**
2. Apply approved numbers everywhere (script outputs, `index.md`, `README.md`, `timeline.md`, test expectations) — honest counts only, formula documented.
3. Gates: 4 suites + `bundle exec jekyll build` + `_site` leak check (no `_staging` in `_site`) + grep for stale numbers + transcript gate ≥68 + disclaimer verbatim.
4. Two final reviewers (spec compliance vs this plan; report deferred/parked findings).
5. Ledger: confusion report (agent failures, retries, demotions), spend log (credits), `_staging` deletion after sign-off (preserve manifests/reports in `.superpowers/sdd/`), ruling roll-up for the user. No push.
