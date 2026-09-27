# Repository metadata — the-andalusian-project-archive / andalusian-archive

Plain text to pass to the GitHub API. Every value below is a literal; nothing needs editing
before use.

---

## 1. Repository name

```
andalusian-archive
```

**Confirmed.** This is the recommendation in `seo-research-technical.md` §B11 (Option A) and
`seo-research-keywords.md` §6(a), and it is also the name the local working directory already
uses, so local and remote names agree.

The reason it is not `the-andalusian-project-archive`: **GitHub forbids a repository whose name
is exactly its owner's login.** `the-andalusian-project-archive` is therefore the *account* and
the name of the *profile README* repository (a profile README only renders if the repository
name matches the username exactly, case-sensitive). The archive repository must carry a
different name, and `andalusian-archive` is the zero-migration choice: `_config.yml:5` hardcodes
`baseurl: "/andalusian-archive"`, which is load-bearing across 311 built pages, 6 published PDFs
and 309 sitemap entries.

> **Counted from the build, 2026-09-28.** 311 is the number of rendered `.html` files in
> `_site/`, 6 is the number of PDFs it serves, and 309 is the number of `<loc>` values in
> `sitemap.xml`. The two pages that are built but deliberately absent from the sitemap are
> `404.html` and `search/` (the latter is `noindex`, because it is an application surface). All
> 309 `<loc>` values are absolute and resolve to a file on disk. These three numbers are the ones
> `README.md` quotes, so they are the numbers to change together if the corpus moves.

Two repositories, two names:

| Repository | Name | Purpose |
|---|---|---|
| Archive + site source | `andalusian-archive` | Everything. This repository. Builds the GitHub Pages site. |
| Profile README | `the-andalusian-project-archive` | Renders on the profile page. Content is `docs/profile-readme.md`. |

Do not rename `andalusian-archive` during or immediately after publication. If a rename is ever
wanted, add the 301s first (`jekyll-redirect-from` is already in the `Gemfile` and enabled) and
do it in one pass, because the name is currently load-bearing in `_config.yml:5` and in the
Pages URL.

---

## 2. Owner-visible title

```
The Andalusian Project — Asadullah Ali Al-Andalusi: Recovered Works, Papers and Transcripts
```

> **Corrected 2026-09-28.** This was written as `Complete Recovered Works…`. 24 of the 72 works
> hold no text and 1 is unrecovered, so "Complete" overclaims; the repository H1 was corrected on
> 2026-09-27 for that reason. The title here is quoted, not recommended, and now matches.

100 characters. This is the site's H1, the `<title>` on the Pages build, and the first line of
`README.md`.

**One precision note:** a GitHub repository has no separate "title" field. The About area renders
the **description** as its visible line. So this string lives in the README H1 and on the site;
the About line is the description in §3. If the owner wants a longer human label on the repo page
itself, the only place it can go is the first line of the README, which is what §2 is.

---

## 3. Description (hard limit 350 characters)

Both are 350 or fewer, both use the "openly available material, archive and lost-and-found"
framing, and both name the person, the project, the three content classes and the method.

### Option A — **PREFERRED** (329 characters)

```
Openly available material, archive and lost-and-found: the complete recovered works of Asadullah Ali Al-Andalusi, founder of The Andalusian Project — 72 works, 20 papers, 68 videos, 68 transcripts — recovered from the Wayback Machine and his own surviving sites after the original web presence was lost, with per-item provenance.
```

Why this one: it states the framing the site owner asked for in the first eleven words, then
names the entity, the organisation, the four content classes with their real counts, the method,
the loss, and the provenance discipline. It is the more informative string, and on GitHub the
description is the About line on the repo page, the snippet in GitHub search results, and the
`description` field in the API payload — so the counts earn their place there in a way they
would not in a paragraph of prose.

### Option B (294 characters)

```
Openly available material, archive and lost-and-found for Asadullah Ali Al-Andalusi and The Andalusian Project: recovered works, papers and machine transcripts with per-item Wayback provenance. asadullahali.com is gone and its YouTube channel unavailable; this repository is the surviving copy.
```

Why it is the alternative: it spends its last two sentences on the *hazard* — that
`asadullahali.com` now serves an unrelated gambling operation and the channel is unavailable —
which is the correction the SEO research identifies as the archive's most urgent and most
uniquely useful contribution. It trades the counts for that. Choose it if the priority is
reputation repair over inventory; choose Option A if the priority is a reader landing on the
page and finding out what is in it.

**Do not** enumerate keyword variants in either. The research is explicit that there is no
documented penalty for a keyword-stuffed repository description, but the realistic exposure is a
`keyword stuffing` manual action on the Pages site, and the variants belong in the README's
"Also published as" block, which is real prose on a real page.

---

## 4. Topics — exactly 20, in recommended order

GitHub's limits, all satisfied below: lowercase letters, numbers and hyphens only; 50 characters
maximum each; 20 topics maximum.

Order is entity-first, then subject, then archival. That is deliberate: the SEO research's
single highest-value finding is that **no page anywhere assembles this person**, and that a
complete, sourced, entity-first landing page is winnable precisely because every incumbent is a
fragment or boilerplate. Topics put the entity terms where they will be found first.

| # | Topic | Why it is here |
|---:|---|---|
| 1 | `the-andalusian-project` | The exact brand and the organisation he actually founded. The research's naming argument rests on this being his real masthead, and it is the token that distinguishes the archive from the unrelated European "Andalusian" research industry. First because the *project* is the entity; the person is its output. |
| 2 | `asadullah-ali` | The navigational entity query. Five institutional hosts — Yaqeen, Al Balagh, MDI, academia.edu, Traversing Tradition — each hold a different slice, and no single canonical page exists. This topic is how the repo surfaces against the fragmented name SERP. |
| 3 | `al-andalusi` | The surname form, and the disambiguator. Al Balagh Academy itself lists a *different, active* Muslim speaker, "Abdullah al Andalusi", as separate faculty, so the conflation is already costing him. Carrying the surname as a topic puts the archive on the correct side of that collision. |
| 4 | `islam-and-atheism` | The corpus's densest subject — the *Understanding Atheism* series, the 2021 AMJA paper, the P1–P5 argument, 68 transcripts. Fourth because the paired phrase is winnable at the long tail while the bare heads (`atheism`, `islam`) are owned by institutional incumbents and should not be chased. |
| 5 | `apologetics` | The corpus's genre, and the highest-traffic already-existing topic that is genuinely on-topic. Fifth because it is the bridge term a librarian, a student or an academic librarian-type reader would actually type. |
| 6 | `atheism` | |
| 7 | `quran` | |
| 8 | `hadith` | |
| 9 | `islamic-studies` | |
| 10 | `islamic-philosophy` | |
| 11 | `philosophy-of-science` | |
| 12 | `library-science` | |
| 13 | `islam` | The highest-traffic already-existing topic that is unambiguously on-topic. See the note below: this is the one term I added, because the brief's list contained 19 and GitHub's cap is 20. |
| 14 | `digital-preservation` | |
| 15 | `wayback-machine` | |
| 16 | `internet-archive` | |
| 17 | `transcripts` | |
| 18 | `oral-history` | |
| 19 | `archive` | |
| 20 | `lost-and-found` | |

**One term I added, and why.** The topic list in the brief contains **19** terms, not 20, so one
slot was mine to fill. Row 13, `islam`, is it: the highest-traffic already-existing topic in the
research's Tier 1, unambiguously on-topic, and topic competition works nothing like SERP
competition — appearing under a broad bucket costs nothing and reaches readers who never type a
long tail. If you would rather spend that slot differently, the two runners-up are:

- **`islamophobia`.** The corpus genuinely covers it (*Whataboutery*, *Confronting
  Islamophobia*, *Still Colonized*), and the research's Tier 2 rates it as differentiating the
  repo from a generic `islam` bucket. The tradeoff is a polemical topic on a repository whose
  value proposition is neutral provenance.
- **`science-and-islam`.** The archive's strongest *scholarly* thread (the ICR paper,
  *Orientalists' Fables*, Qur'an 86:5-7). The research's Tier 2. Narrower, and it positions the
  repo as academic rather than polemical.

Either swap is a one-line change in the payload in §6. What I would **not** add: `dawah`
(research Tier 1, but contested terminology the archive does not assert about itself),
`jekyll` / `github-pages` / `static-site-generator` (no topical value; GitHub's auto-suggestion
engine proposes them anyway), `web-archive` (duplicates `wayback-machine`), or `arabic` /
`turkish` — those last two would be **inaccurate**, because the HTML corpus is English-only and
those two titles exist only as external links and one PDF.

**Apply the topics.** GitHub auto-generates suggested topics for public repos from content
analysis; set them explicitly and reject the suggestions, or the classifier's output will sit
alongside yours.

---

## 5. Homepage

```
https://the-andalusian-project-archive.github.io/andalusian-archive/
```

This is the single most valuable field in the About area: it passes a link from every GitHub
page for the repository to the site. It is **fixed**: `_config.yml` now sets an absolute `url:`,
so every `<link rel="canonical">`, every `og:url` and all 309 `<loc>` values in `sitemap.xml` are
absolute. The `url: ""` P0 this section was written against is closed, and the live check on
2026-09-27 returned absolute canonical and `og:url` with a 200.

---

## 6. About section — the API payload

GitHub's repository object has no separate About title. The About area is rendered from exactly
three fields: `description`, `homepage` and `topics`. Apply all of them in one call.

### Option A (preferred description) — apply this

```http
PATCH /repos/the-andalusian-project-archive/andalusian-archive
Authorization: Bearer <token>
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```

```json
{
  "name": "andalusian-archive",
  "description": "Openly available material, archive and lost-and-found: the complete recovered works of Asadullah Ali Al-Andalusi, founder of The Andalusian Project — 72 works, 20 papers, 68 videos, 68 transcripts — recovered from the Wayback Machine and his own surviving sites after the original web presence was lost, with per-item provenance.",
  "homepage": "https://the-andalusian-project-archive.github.io/andalusian-archive/",
  "topics": [
    "the-andalusian-project",
    "asadullah-ali",
    "al-andalusi",
    "islam-and-atheism",
    "apologetics",
    "atheism",
    "quran",
    "hadith",
    "islamic-studies",
    "islamic-philosophy",
    "philosophy-of-science",
    "library-science",
    "islam",
    "digital-preservation",
    "wayback-machine",
    "internet-archive",
    "transcripts",
    "oral-history",
    "archive",
    "lost-and-found"
  ],
  "has_issues": true,
  "has_projects": false,
  "has_wiki": false,
  "has_discussions": false,
  "is_template": false
}
```

Note: `has_wiki` and `has_discussions` default to `true` on a new repository, so both must be
sent explicitly as `false` to disable them. `has_projects` is sent `false` deliberately — see §7.

### As `curl`

```bash
curl -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/the-andalusian-project-archive/andalusian-archive \
  -d '{
    "name": "andalusian-archive",
    "description": "Openly available material, archive and lost-and-found: the complete recovered works of Asadullah Ali Al-Andalusi, founder of The Andalusian Project — 72 works, 20 papers, 68 videos, 68 transcripts — recovered from the Wayback Machine and his own surviving sites after the original web presence was lost, with per-item provenance.",
    "homepage": "https://the-andalusian-project-archive.github.io/andalusian-archive/",
    "topics": ["the-andalusian-project","asadullah-ali","al-andalusi","islam-and-atheism","apologetics","atheism","quran","hadith","islamic-studies","islamic-philosophy","philosophy-of-science","library-science","islam","digital-preservation","wayback-machine","internet-archive","transcripts","oral-history","archive","lost-and-found"],
    "has_issues": true,
    "has_wiki": false,
    "has_discussions": false
  }'
```

`description` above is 329 characters. The limit is 350 and GitHub rejects longer values with
`422 Validation Failed`, so do not add a clause without re-counting.

### Profile README repository

The second repository, whose `README.md` is the content of `docs/profile-readme.md`:

```
POST /repos/the-andalusian-project-archive/the-andalusian-project-archive
```

```json
{
  "name": "the-andalusian-project-archive",
  "description": "Profile of The Andalusian Project Archive — the account that maintains github.com/the-andalusian-project-archive/andalusian-archive.",
  "homepage": "https://the-andalusian-project-archive.github.io/andalusian-archive/",
  "public": true
}
```

The repository must be **public**, must contain a `README.md` at its root, and that file must
have content, or the profile README does not render at all. Repositories matching the username
and created **after July 2020** attach automatically; this one will be created now, so it will.

---

## 7. Repository settings

| Setting | Recommendation | Why |
|---|---|---|
| **Pages** | **Already correct — no change.** Source: **GitHub Actions**. | `.github/workflows/deploy.yml` already uses `actions/configure-pages` → `bundle exec jekyll build --baseurl …` → `actions/upload-pages-artifact` → `actions/deploy-pages`, with permissions correctly scoped to `contents: read`, `pages: write`, `id-token: write`. Under an Actions deploy no `CNAME` file is needed and no `.nojekyll` is required. Do not switch to "Deploy from a branch": that would run Jekyll over `_site/` with `--safe` and break the four plugins the site depends on. |
| **Issues** | **YES — enable.** | This is the single most likely and most valuable use of the surface. The realistic inbound is provenance, not feature requests: *"this transcript's opening is wrong"*, *"this source URL is dead as of today"*, *"this work exists and I have a copy"*, *"this DOI now resolves"*. Each one becomes a public, dated, per-item, linkable record — which is exactly the artefact an archive should generate, and exactly what a Discussions thread cannot do. Ship four issue templates: **provenance report**, **transcript correction**, **dead or changed source**, **new material I can supply**. Say in the README that privacy and takedown requests go to the contact in `NOTICE.md` and not to Issues. |
| **Discussions** | **NO — disable.** | Three reasons, in order. (1) Function: the only substantive conversation this archive will have is a provenance dispute, and an Issue is per-item, closable, searchable, and referenceable from the commit or the data row that answers it; a Discussion is none of those. (2) Surface: a general public comment area on a deliberately neutral, polemical-content archive creates a moderation obligation the project has not staffed, and the failure mode is visible. (3) Precedent: the research found an active GitHub community complaint that over-long metadata "causes pollution in search results" — GitHub treats an open comment surface as a cost, not an asset. If it is wanted later, `has_discussions` is a one-line PATCH. |
| **Wiki** | **OFF — leave disabled.** | A 311-page site *is* the archive; a wiki would duplicate it. The research is explicit that a wiki is not a reliable index surface for search. And it is a specific failure mode this project cannot afford: a second place where a number can be typed and go stale, when the whole count-approval pass exists to stop exactly that. `has_wiki` defaults to `true` — it must be sent `false` explicitly. |
| **Projects** | **OFF.** | Nothing here is roadmapped as work. Set `has_projects: false` to keep the repo tab strip to Issues, Pull requests, Actions and Security. |
| **Archive flag** | **YES — but only after the first re-check cycle. See the caveat.** | The flag marks the repository read-only, adds a banner, and removes it from language and framework search and code-navigation affordances. It is the correct signal here: the recovery is complete, the evidence trail is committed, the reviews are done, and the remaining work is publication and outreach rather than development. It also sets the right expectation for readers and for contributors whose work is in it — *cite this, don't send it a pull request.* **Caveat: the flag is effectively one-way, and this archive has a live re-check obligation.** `_data/lost_works.json` records one work as unrecovered with the note "re-check if a new capture appears", and the `channel_facts.json` timeline ends at a 2026-08-19 capture with a 2026-09-27 live check. Do not set the flag until at least one re-check cycle has run and been recorded. If the owner expects to keep recovering, do not set it at all; instead say so in the README and leave the repo writable. |
| **Releases** | **Recommended, one release: `v1.0.0`.** | Not asked for, but it is the cheapest way to give the preservation claim a dated, citable artefact, and a `latest` download for people who want the corpus without cloning. Attach the archive manifest (the 21 `_data/*.json` files, or a generated manifest) as the release asset. The SEO research rates this medium-low but cheap and specifically notes it is the kind of artefact academics and archives actually cite. |
| **Branch protection on `main`** | **Recommended — after one workflow edit.** | Four test suites exist and encode the counting discipline: `test_canonical_57.py`, `test_transcripts.py`, `test_search_sync.py`, `test_no_junk.py`. **Only `test_search_sync.py` is currently wired into CI** (`deploy.yml:37-38`, via `npm run test:search-sync`); the other three are run by hand. So this is two steps, in order: add the three missing suites as steps in `deploy.yml` before `bundle exec jekyll build`, *then* protect `main` with all four as required status checks. Doing only the second step would set required checks on suites that never run. This is the control that stops the exact class of failure the Phase 3 review caught: correct numbers published on the wrong side of an approval gate. |

---

## 8. Order of operations

1. Set `url:` in `_config.yml:4` to `https://the-andalusian-project-archive.github.io` — **one
   line, and the site is not announceable until it is done.** Un-exclude `data/` in the same
   pass or the search page ships saying "Failed to load search data" to every visitor.
2. Create both repositories; push `andalusian-archive` to `main`.
3. `docs/profile-readme.md` → `README.md` at the root of `the-andalusian-project-archive`.
4. Apply the §6 PATCH. Apply the §7 toggles.
5. Enable Pages with source **GitHub Actions** and confirm the first deploy is green.
6. Publish `v1.0.0`; pin `andalusian-archive` as the first pinned repository on the profile.
7. Only then begin outreach. Every ask points at a live site with absolute canonicals; the SEO
   research's clearest finding is that links from Yaqeen and the Muslim Debate Initiative are
   worth more than every on-page decision combined, and that they are far likelier to be granted
   to an archive that visibly credits them.
8. Do **not** set the archive flag until a re-check cycle has run and been recorded.

---

*Numbers in the description and topics are as of 2026-09-27 and are counted from `_data/`. If
the Task 9 recount changes one, this file changes with it.*
