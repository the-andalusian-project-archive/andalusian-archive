# 57-List Honest Counts + Full Ethical Collections Implementation Plan
> **Superseded.** This plan is kept as the historical record of the
> 2026-09-06 recovery. `canonical_57.json` was renamed
> `_data/canonical_works.json` on 2026-09-27; see
> `docs/superpowers/plans/2026-09-27-full-recovery-v6.md` (Task 7, item 12)
> for the rename and the recount that followed. The references below are
> left as written.


> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix Critical 9, make 57 the honest blog truth, implement full collections ethically.

**Architecture:** Split works (57 manual list) vs captures (87 CDX rows); `_data/` single source of truth copied to `data/` at build; detail layouts inherit `default.html`; full `_papers/_videos/_articles` collections with link-outs for institutional content.

**Tech Stack:** Jekyll 4.4.1, Ruby 3.2, GitHub Pages Actions (deploy-pages@v4), Python 3.11 asserts, Liquid, vanilla JS search.

**Spec:** `D:\The Andalusian Project\session_context.md` (57 list lines 120-193) + `D:\The Andalusian Project\issues.md` (33 issues, 9 Critical C-01…C-09)

## Global Constraints

- Canonical blog truth = 57 manual list (56 Wayback URLs + 1 feed-only: Library Take Down Notice 2014-03-17), not 87 CDX rows.
- Ethical scraping: DO NOT scrape Reddit (robots.txt blocked) or Medium (AI bots restricted); SAFE: Yaqeen Institute (with attribution), muslimdebate.org, traversingtradition.com, wordpress; USE existing archives for Archive.org/Wayback.
- Search priority: normal websearch + Exa first via parallel agents (max 2-3 concurrent implementers); Firecrawl search/scrape only where normal fails (~934 credits remaining, always `-o .firecrawl/` + `search-feedback` for refund).
- No git repo per prior user constraint — reviews use file diffs, not SHAs; do not `git init` without explicit approval.
- Every task ends with `bundle exec jekyll build` PASS + python JSON asserts + task review (spec + quality).
- Counts: `total == sum(collections)`; works vs captures vs files-preserved kept distinct.

---

### Task 0: Reconcile 57 works vs 87 captures

**Files:**
- Modify: `andalusian-archive/scripts/build_content_index.py:14` (remove hardcoded `D:\` path → relative)
- Modify: `andalusian-archive/_data/content_index.json:6-18,106-114`
- Create: `andalusian-archive/_data/canonical_57.json`

**Interfaces:**
- Consumes: `session_context.md:120-193` (57 list), `wayback_posts.json` (56 rows), `_data/blog_posts.json` (87 rows)
- Produces: `canonical_57.json` — array of 57 `{slug, title, date, wayback_url|null, status: found|wayback_only|lost}`; `total_works=57`, `total_captures=87` used by Tasks 3-4.

- [ ] **Step 1: Write the failing test**

```python
# scripts/test_canonical_57.py
import json, pathlib
base = pathlib.Path(__file__).parent.parent
canon = json.loads((base / "_data/canonical_57.json").read_text(encoding="utf-8"))
caps = json.loads((base / "_data/blog_posts.json").read_text(encoding="utf-8"))
assert len(canon) == 57, f"works={len(canon)} != 57"
assert len(caps) == 87, f"captures={len(caps)} != 87"
assert sum(1 for w in canon if w["status"]=="lost") == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python andalusian-archive/scripts/test_canonical_57.py`
Expected: FAIL with "canonical_57.json not found" (file does not exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/build_canonical_57.py — parse session_context.md 57 list + wayback_posts.json (56) + feed-only entry
# Library Take Down Notice 2014-03-17 → status wayback_only/feed_only, wayback_url null
# 2 lost: Inhumanity 2012-02-26, Making 2014-10-21 → status lost
# remaining 54 → found or wayback_only by content_file resolution
```

Regenerate `content_index.json` statistics from source lengths; fix `preservation_notes` (remove "All 87…Full text stored", "All 59 videos…", "5 articles scraped").

- [ ] **Step 4: Run test to verify it passes**

Run: `python andalusian-archive/scripts/test_canonical_57.py && bundle exec jekyll build`
Expected: PASS, `_site/index.html` generated

- [ ] **Step 5: Task review**

Dispatch single task reviewer (requesting-code-review, file-diff mode, no SHAs): spec = 57 = 56+1, 2 lost listed separately. Fix Critical/Important before proceeding.

### Task 1: Build safety (C-09 + C-08)

**Files:**
- Modify: `andalusian-archive/_config.yml:1-39` (add exclude)
- Modify: `andalusian-archive/.gitignore:11` (remove Gemfile.lock line — keep file, do not git-commit per no-git constraint)
- Modify: `andalusian-archive/Gemfile.lock` — NOT by hand; run `bundle lock --add-platform ruby --add-platform x86_64-linux` on Linux CI only; on Windows leave as-is + document

**Interfaces:**
- Consumes: Task 0 counts
- Produces: `_site/` contains no `scripts/`, `package.json`, `README.md`, `data/` raw copies

- [ ] **Step 1: Write the failing test**

```bash
bundle exec jekyll build && test ! -e _site/scripts/fetch_wayback.py && echo NO_LEAK || echo LEAK
```

- [ ] **Step 2: Run test to verify it fails**

Run: above in `andalusian-archive/`
Expected: LEAK (`_site/scripts/` exists today)

- [ ] **Step 3: Write minimal implementation**

```yaml
# _config.yml append:
exclude:
  - scripts/
  - data/
  - README.md
  - package.json
  - package-lock.json
  - Gemfile
  - Gemfile.lock
  - node_modules/
  - vendor/
  - .env
  - .env.example
  - .github/
  - .firecrawl/
  - .jekyll-cache/
  - .sass-cache/
keep_files: [.nojekyll]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `bundle exec jekyll build` + leak test → NO_LEAK
Expected: PASS

- [ ] **Step 5: Task review** (build/method focus)

### Task 2: Layout inheritance (C-01 + C-02 + M-01)

**Files:**
- Modify: `andalusian-archive/_layouts/post.html:1-64`, `article.html:1-59`, `paper.html:1-112`, `video.html:1-66`
- Modify: `andalusian-archive/_config.yml:20-35` (add posts default)

**Interfaces:**
- Consumes: `default.html:12-30` nav (`.site-nav`, `.nav-inner`, active states), `style.css:142-225`
- Produces: detail pages inherit nav/footer/SEO; video nav includes Search link

- [ ] **Step 1: Write the failing test**

```bash
# no standalone html shells in detail layouts:
grep -L "<!DOCTYPE html>" andalusian-archive/_layouts/post.html andalusian-archive/_layouts/article.html andalusian-archive/_layouts/paper.html andalusian-archive/_layouts/video.html
```

Expected now: all 4 contain DOCTYPE (fail = bug present).

- [ ] **Step 2: Run test to verify it fails** (confirms duplication)
- [ ] **Step 3: Write minimal implementation**

```html
---
layout: default
---
<article class="post-detail">{{ content }}</article>
```

Same shape for article/paper/video (keep inner meta/source-links, delete head/nav/footer dupes). Add to `_config.yml` defaults: `- scope: {path: "", type: "posts"}, values: {layout: "post"}` (fixes I-01: 13/15 posts missing layout).

- [ ] **Step 4: Run test + build** — grep shows no DOCTYPE in 4 files; `bundle exec jekyll build` PASS
- [ ] **Step 5: Task review** (frontend/method)

### Task 3: Honest counts + articles filter (C-03 + C-04 + C-05, I-07/I-08/I-09)

**Files:**
- Modify: `andalusian-archive/index.md:13-14,25-26,60,78,111`, `articles.md:7-8,11-24`, `search.md:8,56`

**Interfaces:**
- Consumes: Task 0 `canonical_57.json`
- Produces: headline "57 works — 15 full-text in repo, 2 lost, 40 Wayback-only"

- [ ] **Step 1: Write failing test** — assert `index.md` contains "57" not "87 posts … Full text preserved"; `articles.md` loops `canonical_57` not raw `blog_posts`
- [ ] **Step 2: Run, expect FAIL**
- [ ] **Step 3: Implement** — `{% assign works = site.data.canonical_57 %}` + filter; lost section lists 2 lost works separately; fix `total_content` to `sum(collections)` (173 baseline, recomputed)
- [ ] **Step 4: Build PASS**
- [ ] **Step 5: Task review**

### Task 4: Search single source (C-06 + I-13)

**Files:**
- Modify: `andalusian-archive/search.md:40-42,60-71,75-81,96-131,144-171`, build sync step

**Interfaces:**
- Consumes: `_data/*.json` (truth: blog 57 works, videos 68, papers 18)
- Produces: `data/*.json` synced at build; zero empty titles; https-allowlisted hrefs

- [ ] **Step 1: Failing test** `python -c "assert len(data/videos)==68 and len(data/papers)==18"` → FAIL (59/11 today)
- [ ] **Step 2-4:** copy `_data/` → `data/` in pre-build (npm `prebuild` or Jekyll hook), strip `?…` slugs (M-09), prebuild excerpt index for posts, attribute-escape URLs
- [ ] **Step 5: Task review**

### Task 5: Full ethical collections (C-07)

**Files:**
- Create: `andalusian-archive/_papers/*.md` (18), `_videos/*.md` (68), `_articles/*.md` (57) generated from JSON — link-outs only for institutional content, full text only for CC-licensed/at-risk
- Modify: `search.md:90,107,128` → `/papers/<slug>/` etc. (now real)

- [ ] **Step 1: Failing test** — `bundle exec jekyll build && test -f _site/papers/<sample>/index.html` → FAIL today
- [ ] **Step 2-4:** generator script (relative paths) + detail layouts from Task 2; video `status/source` field (I-04: 12 YouTube-only labeled "YouTube (not archived)"); papers generic `/Talks` URL marked `profile_page_only` (I-05)
- [ ] **Step 5: Task review** (ethics check: no Reddit/Medium inlining, Yaqeen attribution present)

### Task 6: Limited search wave (max 2 concurrent agents)

- S1 (websearch/Exa, general subagent): 40 Wayback-only 2016-2020 recoveries + 39 YouTube-only archiving assessment; output JSON rows
- S2 (method review, general subagent): I-14 toolchain (`package.json:11-13` firecrawl→devDeps, `bundle exec` prefix, relative paths, pagination for `fetch_wayback.py:18,54`)
- Firecrawl search/scrape only on S1 gaps (Yaqeen/MDI/AlBalagh/TT, AI-friendly only), `.firecrawl/` + feedback
- Integrate S1 rows into `canonical_57.json`; do not exceed credit shyness rule

### Task 7-8: Important I-01…I-14 then Minor M-01…M-10 (batched same-shape, one dispatch per batch)

### Task 9: Final verification (verification-before-completion gate)

Run fresh: `bundle exec jekyll build`, `python scripts/test_canonical_57.py`, leak test, link spot-check, counts cross-check (57/68/18). Broad file-diff review (requesting-code-review, most-capable). One fix wave max, scoped re-review, adjudicate residuals in ledger.
