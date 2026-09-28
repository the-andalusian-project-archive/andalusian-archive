# Query Discoverability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the archive findable by the questions the author already answered, not only by his name and exact work titles.

**Architecture:** Eight parallel research agents read the ACTUAL material (`_posts/`, `_papers/`, `_transcripts/`) and return per-cluster specs built from verbatim quotes carrying `file:line` references. A new `scripts/test_quotes.py` mechanically verifies every quote resolves to real text, so no agent can invent a claim. `scripts/apply_topics.py` mirrors the existing `apply_taxonomy.py` pattern to stamp topics and emit cross-links. Result: a `/topics/` index, 8 substantive cluster pages, and topical cross-links on ~160 items.

**Tech Stack:** Jekyll (existing), Python 3 for data/build scripts, JSON for topic data, Bash/PowerShell for verification. No new dependencies.

**Spec:** This document. Approved by the site owner 2026-09-28.

## Global Constraints

- **No thin pages, no doorway pages.** One page per query is spam and would risk the domain. 8 substantive cluster pages cover the query space in real prose because the material genuinely answers it.
- **No fabrication.** Every `key_claims` entry must be a verbatim quote with `file:line`. `scripts/test_quotes.py` fails the build otherwise.
- **Attribution discipline.** The author's prose is quoted and attributed. The archive's own framing is labelled as the archive's. Never present synthesis as his claim.
- **No contact with the author.** The no-contact notice stands. Any published address is the ARCHIVE MAINTAINER, explicitly labelled as such.
- **PowerShell safety.** Never use `Set-Content -Encoding UTF8` on tracked files: on Windows PowerShell 5.1 it writes a BOM, which makes Jekyll skip front matter. Use a bytes-level Python rewrite and re-run the BOM check.
- **Counts are computed, never typed.** No page may hardcode a number; compute it from `_data` at build time.
- **Preserve the copyright posture.** Author's prose is openly readable, NOT relicensed. Archive-owned data/scripts are CC BY-NC 4.0.

---

## File Structure

**Created:**
- `docs/superpowers/plans/2026-09-28-query-discoverability.md` — this plan
- `_data/topics.json` — merged topic taxonomy and per-cluster query map (build-time source of truth)
- `scripts/apply_topics.py` — stamps `topics` onto data rows, emits cross-link data. Mirrors `apply_taxonomy.py`.
- `scripts/test_quotes.py` — verifies every `key_claims` quote exists verbatim at its cited `file:line`
- `topics.md` — `/topics/` index page
- `topics/<cluster>.md` — 8 cluster pages, one per cluster
- `scripts/test_topics.py` — coverage/orphan checks for the topic layer

**Modified:**
- `.github/workflows/deploy.yml` — IndexNow failure warning; derive host from `base_path`
- `README.md` — plain-language rewrite, contribution address
- `_layouts/default.html` — UI/UX improvements
- `llms.txt` — expanded for AI engines
- `.superpowers/sdd/2026-09-27-full-recovery-v6/outreach-drafts.md` — (gitignored) fix overstatement and stale slugs

**Deleted:**
- `scripts/deploy.sh` — vestigial, referenced nowhere, its `YOUR_USERNAME` placeholder actively blocked two earlier recovery-log tasks. Repairing dead code preserves the trap.

---

## The 8 clusters

| ID | Cluster | Seed material |
|---|---|---|
| `atheism-doubt` | Atheism, doubt, evidence | Understanding Atheism, Doubting Your Doubts, 3 Isms, Rationality of Believing in God Without Evidence, Hard Questions |
| `science-scientism` | Science, faith, scientism | From Science to Scientism, Qur'an and Science: A Forced Marriage, Rise and Decline of Scientific Productivity, Orientalists' Fables |
| `gender-feminism` | Feminism, gender, Aisha | Do Muslim Women Need Feminism?, How Feminism Undermines Islam, Marina Mahathir, Understanding Aisha's Age |
| `terrorism-extremism` | Terrorism, extremism | Islam and Terrorism, Who Justifies Terrorism?, Extremism in Muslim Thought, Boko Haram, Prophets vs Pedophiles |
| `liberalism-orientalism` | Liberalism, orientalism, human rights | Still Colonized, Decoding Contemporary Liberalism, Inhumanity of Human Rights, War on Islam, Naked Kings |
| `apostasy-hell` | Apostasy, hell, divine justice | Apostasy: Beyond the Rhetoric, Punishment for Apostasy, God's Mercy Without Eternal Punishment, For Good Men to Do Evil |
| `aqeedah-basics` | Aqeedah basics | How to know "No-thing", Nothing, Adam is No Myth |
| `quran-hermeneutics` | Quran and hermeneutics | Illogical Critiques of the Quran, Backbone Ribs, Lost in Time Translation |

---

## Phase 0 — Fix known issues (inline, before anything new ships)

- [ ] Task 0a: Correct the outreach draft that asserts a role "is no longer current". The archive's own entity page explicitly disclaims that claim. Replace with the defensible one: the bio is unverifiable on those institutions' current pages. Re-measure word count.
- [ ] Task 0b: Fix the two stale `/asadullah-ali-al-andalususi/` slugs in the drafts and the false "confirmed by explicit `permalink:`" claim.
- [ ] Task 0c: `deploy.yml` — add a `::warning::` on IndexNow failure so the step can never again read green while doing nothing.
- [ ] Task 0d: `deploy.yml` — derive the host from `steps.pages.outputs.base_path`; remove the three hardcoded occurrences and the duplicated inline Python in favour of `scripts/ping_indexnow.py`.
- [ ] Task 0e: Delete `scripts/deploy.sh`.

## Phase 1 — Parallel research (8 agents, one dispatch)

- [ ] Task 1a–1h: One agent per cluster. Each reads real material, writes `_data/topics/<id>.json`, touches no other file.

## Phase 2 — Integration and quote verification

- [ ] Task 2a: Merge the 8 specs into `_data/topics.json`.
- [ ] Task 2b: Write `scripts/test_quotes.py`; run it; every quote must resolve.
- [ ] Task 2c: Report per-cluster counts; flag any thin cluster rather than inflating it.

## Phase 3 — Build the layer

- [ ] Task 3a: `scripts/apply_topics.py` stamps topics and emits cross-links.
- [ ] Task 3b: `/topics/` index and 8 cluster pages.
- [ ] Task 3c: Cross-links on works, papers, transcripts, videos.
- [ ] Task 3d: `scripts/test_topics.py` — coverage and orphan checks.

## Phase 4 — AI surfaces (no Wikipedia, per decision)

- [ ] Task 4a: Expand `llms.txt`.
- [ ] Task 4b: Note the Wikipedia option as deferred, not done.

## Phase 5 — Plain language, contribution route, UI/UX

- [ ] Task 5a: README plain-language rewrite.
- [ ] Task 5b: Publish the archive maintainer address, clearly labelled as NOT the author's.
- [ ] Task 5c: UI/UX improvements in `_layouts/default.html`.

## Phase 6 — Backlinks worth having

- [ ] Task 6a: Assess each legitimate backlink route; implement only the ones that are legitimate and worth the time. No link schemes, no reciprocal-link padding.

## Phase 7 — Verify and deploy

- [ ] Task 7a: 5 suites green, build green, BOM check, wrong-slug check.
- [ ] Task 7b: Single commit, push, confirm live.

## Phase 8 — Two review agents, then fixes

- [ ] Task 8a: Dispatch 2 independent review agents.
- [ ] Task 8b: Fix what they find; re-verify.

## Phase 9 — Next indexing batch

- [ ] Task 9a: Emit the batch with the full Backbone and Ribs PAPER page replacing the 245-word stub, respecting the ~10/day URL Inspection quota.
