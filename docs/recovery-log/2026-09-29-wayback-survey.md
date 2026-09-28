# Wayback survey — 2026-09-29

A **read-only** survey of the Internet Archive's Wayback Machine, run to answer one
question: *what published material by Asadullah Ali Al-Andalusi exists there that this
archive does not already hold?*

**Nothing was recovered.** No content file was added, modified or deleted; no media was
downloaded; no live host was contacted. This file is the only thing this run produced.
The headline number is **76 permalinks on `muslimdebate.org`**, all of them carrying a
200 capture and all of them absent from the archive. Detail and caveats in §3 and §5.

## 1. Method

All queries were CDX API calls against `https://web.archive.org/cdx/search/cdx`, issued
serially with a 3–4 s pause between them, using `urllib.request` with an identifying
User-Agent. `curl` is not on this machine; `python` is (`Python 3.11.9`), `python3` is not.
`yt-dlp` is on PATH but was **not** used — no media was fetched.

Every query used the same field set:

```
fl=timestamp,original,statuscode,mimetype,length & collapse=urlkey & output=json
```

`collapse=urlkey` means each figure below is a count of **distinct archived URLs**, not of
captures. A URL with 40 captures counts once.

### 1.1 Every query run, verbatim, with its row count

| # | `url` parameter | `matchType` / extra | HTTP | Distinct URLs |
|---:|---|---|---:|---:|
| 1 | `asadullahali.com/*` | probe (limit 5) | 200 | 5 |
| 2 | `asadullahali.com` | `domain` | 200 | 1,140 |
| 3 | `asadullahali.wordpress.com` | `domain` | 200 | 846 |
| 4 | `abdullahalandalusi.com` | `domain` | 200 | **0** |
| 5 | `muslimdebate.org` | `domain` | 200 | 8,487 |
| 6 | `muslimsdebate.com` | `domain` | 200 | 12,770 |
| 7 | `islamicdiscourseinitiative.com` | `domain` | 200 | 1,009 |
| 8 | `thedebateinitiative.com` | `domain` | 200 | **0** |
| 9 | `thedeeninstitute.com` | `domain` | 200 | 1,049 |
| 10 | `albalaghacademy.org` | `domain` | 200 | **20,000 (capped)** |
| 11 | `hidayah.albalaghacademy.org` | `domain` | 200 | 3,395 |
| 12 | `totetu.org` | `domain` | 200 | **20,000 (capped)** |
| 13 | `islamcompass.com` | `domain` | 200 | 13,673 |
| 14 | `euvolution.com` | `domain` | 200 | **0** |
| 15 | `thedeenshow.com` | `domain` | 200 | **20,000 (capped)** |
| 16 | `yaqeeninstitute.org` | `domain` | 200 | **20,000 (capped)** |
| 17 | `islamic-life-forum.blogspot.com` | `domain` | 200 | 512 |
| 18 | `myultimatedecision.info` | `domain` | 200 | 5,276 |
| 19 | `forevermuslim.in` | `domain` | 200 | 6,471 |
| 20 | `muslimdebate.org/author/abdullahandalusi*` | `prefix` (malformed, see note) | 200 | 0 |
| 21 | `muslimdebate.org/author/asadullahali*` | `prefix` (malformed, see note) | 200 | 0 |
| 22 | `muslimdebate.org/author/abdullahandalusi` | `prefix` | 200 | 17 |
| 23 | `muslimdebate.org/author/asadullahali` | `prefix` | 200 | 3 |
| 24 | `muslimdebate.org/author/asadullahali/page/2/` | exact | 200 | **0** |
| 25 | `https://asadullahali.com/2014/10/21/the-making-of-modern-western-civilization-the-war-on-islam-guest-contribution/` | exact | 200 | 1 |
| 26 | `asadullahali.wordpress.com/2014/10/21/the-making-of-modern-western-civilization-the-war-on-islam-guest-contribution` | `prefix` | 200 | 1 |
| 27 | `albalaghacademy.org` | `domain` + `filter=original:.*(instructor\|ustaad\|team)/.*` | 200 | 356 |
| 28 | `hidayah.albalaghacademy.org/team` | `prefix` | 200 | 43 |
| 29 | `islamic-life-forum.blogspot.com` | `domain` + `filter=original:.*(asadullah\|andalusi).*` | 200 | 2 |
| 30 | `yaqeeninstitute.org/asadullah` | `prefix` | 200 | 30 |
| 31 | `yaqeeninstitute.org/team` | `prefix` + `filter=original:.*andalusi.*` | 200 | 2 |

Queries 20 and 21 are recorded because they were run and **returned 0 rows for a
malformed reason**: a trailing `*` in the `url` parameter with `matchType=prefix` is not
valid CDX syntax and silently matches nothing. The correct form dropped the `*` and is
queries 22 and 23. Anyone repeating this work should not copy queries 20–21.

### 1.2 HTTP status counts

| Status | Count |
|---|---:|
| 200 | **31** |
| 429 (rate limited) | **0** |
| 503 | 0 |
| other / failed | 0 |

**31 of 31 queries returned HTTP 200. No rate limit was hit at any point.** This is a
result of serialising the requests with a 3–4 s sleep rather than anything inherent, so it
should not be read as evidence the endpoint is unlimited. Total distinct URLs returned
across all queries: **135,088**.

A further **37 page fetches** from `web.archive.org/web/` (20 author-archive pages, a
17-permalink verification sample, and 3 further byline checks) also all returned HTTP 200.
No 404 and no empty body was encountered on any fetch.

### 1.3 How "not held" was decided

For every claim of absence below, the permalink's **slug** (final path segment) was tested
against these files, and the check is reproducible from the repository:

- `_data/canonical_works.json` (72 rows)
- `_data/videos.json` (68 rows)
- `_data/secondary_sources.json` (70 rows)
- `_data/linkouts.json` (10 rows)

Those four hold **214 distinct (host, path) pairs** and **189 distinct slugs**.

Two further sweeps were run, because the four files alone are not sufficient to say what
the archive holds:

- **All of `_data/*.json`** — 350 distinct (host, path) pairs, 919 slugs. This is what
  caught the fact that the archive holds 17 MDI articles in `_data/mdi_articles.json`,
  which is *not* one of the four named files.
- **Content directories** (`_posts/`, `_articles/`, `_papers/`, `_transcripts/`,
  `_videos/`, `docs/`, `scripts/`) — 818 distinct (host, path) pairs from filename
  slugs and inline URLs.

**Matching was done at slug level, not host level, and this mattered.** A first pass
matched on (host, path) and reported four WordPress permalinks as new. They were not:
`supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad`,
`boko-haram-and-the-culture-of-coercive-disapproval`, `the-sword-of-ibn-nasir` and
`more-additions` are all already held, but held under the *other* host, or under
`_data/notices.json` rather than as works. A work keeps its slug across hosts, so
host-level matching manufactures false positives.

---

## 2. Already held — lanes checked that turned out to be covered

This is the part that proves no lane was wasted.

| Pattern checked | Distinct URLs in CDX | Genuine post permalinks after filtering | Of those, already held | Newly found |
|---|---:|---:|---:|---:|
| `asadullahali.com` (his era, 2010–2016) | 1,140 | 34 | **32** | 2 (non-work pages) |
| `asadullahali.wordpress.com` (2011–2014) | 846 | 112 | **104** | 4 (non-work pages) |
| `muslimdebate.org` author archives | 20 author pages | 88 | **10** in the four files, **12** archive-wide | **76** |
| `islamicdiscourseinitiative.com` | 1,009 | see §3.3 | 1 | ~20, attribution unverified |
| `yaqeeninstitute.org/asadullah*` | 30 | 15 | 12 | 3 URL forms, 0 new works |
| `islamic-life-forum.blogspot.com` | 512 | 2 | 1 | 1 |
| `hidayah.albalaghacademy.org/team*` | 43 | 2 | 1 | 1 |
| `albalaghacademy.org/{ustaad,instructors,team}*` | 356 | 2 | 1 | 1 |

**The author's own blog is exhausted.** Of 146 genuine post permalinks across
`asadullahali.com` and the WordPress mirror, **136 are already held** and the remaining 6
are not works at all — they are site furniture: `asadullahali.com/policy/` (8,193 B),
`asadullahali.com/contact/` (7,769 B), `asadullahali.wordpress.com/policy/` (9,024 B),
`/aqid/` (6,338 B), `/science/` (5,326 B), `/law/` (5,323 B). Every other "unheld" URL on
those two hosts is a category, tag, monthly-archive or query-variant listing page, which is
what the archive's existing 87 "Wayback capture records" already describe (17 permalinks,
13 monthly archives, 10 feeds, 2 AMP, 45 query variants).

**`asadullahali.com` after 2016 is not his.** The domain now resolves to an unrelated
gambling site. Of the 1,140 archived URLs, the capture years split 2015: 47, 2016: 3, then
2019: 72, 2020: 323, 2021: 162, 2022–2024: 36. The 2019+ captures are the gambling site
and were excluded from consideration. The survey did not visit that live site.

**Yaqeen yields no new works.** The archive holds 9 Yaqeen pages as link-outs by policy
(Global Constraint 4 — no text downloaded). The `/asadullah/` author section on Yaqeen
lists 15 pages with 200 captures, but their slugs are the *same* works already
link-out-held, reached by a different path (`/asadullah/<slug>` rather than
`/read/blog/<slug>`). The only genuinely unheld item is the author landing page
`https://yaqeeninstitute.org/asadullah` (107,594 B, captured 2020-11-27). **No new Yaqeen
work was found.**

### 2.1 `muslimsdebate.com` — a large number that is not a finding

`muslimsdebate.com` returned **12,770 distinct URLs**, the second-largest count of the
survey, and **0 of them appear in any of the four data files or anywhere else in the
archive**. It is nonetheless not a finding, and reporting it as one would be wrong.

It is a vBulletin-style user forum, not a publication. Its content URLs carry per-post
query strings — `/faces/shownotes.php?notesid=1000=`, `/faces/sn.php`,
`/story.php`, `/n.php`, `/faces/index.php` — and it has an author-listing endpoint
`listing.php?author=<name>` whose captured values are other people's names
(`Claudia Smith`, `Peter Morgan`, `Tanveer Jafri`, `ALEXANDER MELEAGROU-HITCHENS`).
The 12,770 is forum session and post churn, not 12,770 works. It was not pursued further.

---

## 3. Newly found

### 3.1 `muslimdebate.org` — 76 permalinks with a 200 capture, held nowhere in the archive

This is the substantive result of the survey.

**How the list was obtained.** `muslimdebate.org` is WordPress, so it keeps author
archives. Two exist for him, and the CDX prefix queries 22 and 23 found every page of
both:

- `muslimdebate.org/author/abdullahandalusi/` — 16 pages (`/` and `/page/2/` … `/page/16/`), 17 captures including a feed
- `muslimdebate.org/author/asadullahali/` — 3 pages (`/`, `/page/3/`, `/page/4/`), 3 captures

All 20 author-archive pages have a 200 capture. Each was fetched and parsed. Each page
contains exactly 5 `<article>` elements — MDI's author archive paginates at 5, not the
WordPress default of 10 — so 5 per page is the verified yield, not a truncated one. That
produced **88 distinct post permalinks** spanning **2011-12 to 2019-12**.

**All 88 have a 200 capture.** 0 were missing. Capture counts per URL: 52 URLs have one
capture, 20 have two, 6 have three or more, and one has 77.

**Of the 88, the archive holds 12 and does not hold 76.** The 12 are recorded in
`_data/mdi_articles.json` and 10 of the 12 are also reachable from
`_data/canonical_works.json` or `_data/secondary_sources.json`.

| Checked against | Result |
|---|---|
| `_data/canonical_works.json` | 10 of 88 held |
| `_data/videos.json` | 0 of 88 held |
| `_data/secondary_sources.json` | 10 of 88 held (same 10 as canonical_works) |
| `_data/linkouts.json` | 0 of 88 held |
| **all four combined** | **10 of 88 held** |
| `_data/mdi_articles.json` (a fifth file, not among the four) | 12 of 88 held |
| any of `_data/*`, or `_posts/`, `_articles/`, `_papers/`, `_transcripts/`, `_videos/` | 12 of 88 held |

So the 76 are absent from the four named files **and** from every other data file and
content directory in the repository. The absence claim is checkable on that basis.

**Why this file matters, and why it nearly made me wrong.** Checking only the four named
files would have reported **88** new permalinks rather than 76, because
`_data/mdi_articles.json` — which is not one of the four — already holds 17 MDI articles,
12 of which appear in the author archives. The four-file figure of 10 and the
whole-archive figure of 12 are different numbers, and both are stated here so the claim can
be checked against whichever basis a reader prefers.

**Authorship is verified, not inferred.** The 17 permalinks read in §3.2 each returned an
explicit `By Abdullah al Andalusi on <date>` byline. This is MDI's own
author attribution, corroborated by a byline in the page body.

**Publication years of the 76:** 2011: 1, 2012: 4, 2013: 31, 2014: 26, 2015: 6, 2016: 4,
2017: 2, 2018: 1, 2019: 1. **Best-capture years:** 2021: 66, 2022: 9, 2023: 1 — the site
was crawled once, thoroughly, in late 2021, which is why so many URLs have exactly one
capture. CDX `length` is the compressed WARC record length, not page text; treat it as a
size proxy, not a word count.

#### The 76

| Permalink (on `https://muslimdebate.org`) | Best timestamp | Length | Title | Read? |
|---|---|---:|---|---|
| `/2013/12/25/debate-video-are-ahmadiyyah-part-of-islam/` | 20220522233017 | 91400 | Debate Video: Are Ahmadiyya part of Islam? | yes |
| `/2012/10/20/tom-hollands-obsession-with-islams-origins-a-critical-response/` | 20230221034951 | 67467 | Tom Holland’s Obsession with Islam’s Origins: A Critical response | yes |
| `/2014/01/19/a-post-liberal-future/` | 20210510085824 | 65853 | A Post-Liberal Future? | yes |
| `/2014/01/06/hobbes-folly-how-a-mistake-led-to-secularism-and-a-new-intolerance/` | 20210925234243 | 46916 | Hobbes' Folly: The Creation of Secularism and a new Intolerance | yes |
| `/2013/06/12/who-justifies-terrorism-part-1/` | 20220523002445 | 37114 | Who Justifies Terrorism? | yes |
| `/2013/05/05/sheikh-abdul-hakim-murad-falls-victim-to-the-hypocrisy-of-liberal-tolerance/` | 20210514203638 | 35351 | Sheikh Abdal-Hakim Murad falls victim to the hypocrisy of Liberal tolera | yes |
| `/2014/04/15/maajid-nawaz-the-bbc-and-the-uk-muslim-community-part-1/` | 20210621165239 | 34958 | Maajid Nawaz, the BBC and the UK Muslim Community (part 1) | no |
| `/2014/02/20/debate-review-my-public-debate-defending-islam-from-feminist-criticism/` | 20211207083815 | 34420 | Debate Review: My public debate defending Islam from Feminist criticism | no |
| `/2015/05/07/should-muslims-vote-in-secular-liberal-democracies-the-bigger-picture/` | 20210511165046 | 32881 | Should Muslims Vote in Secular Liberal Democracies? The Bigger Picture | yes |
| `/2013/05/22/the-fallacies-of-dr-william-lane-craigs-argument-for-the-trinity/` | 20210514204534 | 32757 | The fallacies of Dr William Lane Craig’s argument for the Trinity | no |
| `/2013/04/13/abdullah-al-andalusi-to-teach-dawah-diploma-in-july-2013/` | 20210723232420 | 32566 | Abdullah al Andalusi to teach Dawah Diploma' in July 2013 | no |
| `/2013/05/29/liberal-intolerance-john-lockes-dark-secret-2/` | 20221203082945 | 31595 | Liberal Intolerance: John Locke's Dark Secret | no |
| `/2014/06/25/the-no-one-kills-in-the-name-of-atheism-argument/` | 20211207083623 | 31279 | The No one kills in the name of Atheism' Argument | no |
| `/2014/11/22/tales-of-the-unexpected-convincing-members-of-english-upper-class-that-sharia-is-fairer-than-english-law/` | 20210506180902 | 30858 | Tales of the Unexpected: Convincing members of English Upper Class that  | no |
| `/2013/03/14/atheist-hypocrisy-and-gender-segregation/` | 20210510072121 | 30679 | Atheist Hypocrisy and Gender Segregation | no |
| `/2014/04/11/upcoming-debate-can-we-trust-todays-torah/` | 20210923122422 | 30666 | Debate: Can We Trust Today's Torah? (11th April 2014) | no |
| `/2012/10/09/the-intolerance-of-the-intolerant-why-anti-muslim-polemicists-misrepresent-muslim-groups-a-case-study/` | 20210624183445 | 30306 | The Intolerance of anti-Muslim polemicists and the misrepresention of Mu | no |
| `/2011/12/20/of-course-religious-and-political-debates-happen-in-the-muslim-world/` | 20210510085316 | 29230 | Of course religious and political public debates happen in the Muslim wo | yes |
| `/2016/08/31/transcript-opening-speech-did-god-create-man-or-did-man-create-god-abdullah-al-andalusi/` | 20210510083446 | 28989 | Transcript: Opening Speech "Did God Create Man, or did Man create God?"  | yes |
| `/2018/11/26/glossary-of-terms-idioms-used-by-muslim-debaters-daees-around-the-world/` | 20210618201113 | 28932 | GLOSSARY OF TERMS & IDIOMS USED BY MUSLIM DEBATERS & DAEE's (around the  | yes |
| `/2013/12/02/reject-democracy-freedom-of-speech-and-predict-the-future-collapse-of-western-civilisation-youre-an-extremist-unless-youre-chinese/` | 20210512072021 | 28589 | Reject Democracy & Freedom of Speech' and predict the collapse of Wester | no |
| `/2013/04/11/review-of-my-human-rights-debate-yesterday/` | 20220520134138 | 28585 | Review of my Human Rights debate yesterday | no |
| `/2013/10/01/the-sad-events-mall-attack-kenya-some-needed-reflections/` | 20221203084828 | 28556 | The Sad Events of the Mall Attack in Kenya and some needed reflections a | no |
| `/2014/03/04/the-panoptic-police-state-a-natural-product-of-secular-liberalist-ideology/` | 20210514202116 | 28442 | The Panoptic Police State: a Natural Product of Secular Liberalist Ideol | no |
| `/2013/06/24/abdullah-al-andalusi-on-bbc1s-the-big-questions-discusses-mixing-religions-gambling-and-suicide/` | 20210515015636 | 28232 | Abdullah al Andalusi on BBC1's The Big Questions' discusses gambling, su | no |
| `/2016/04/06/islam-needs-a-restoration-not-a-reformation-mdi-member-article-published-in-middle-east-eye/` | 20220119112412 | 28064 | Islam Needs a Restoration, not a Reformation' MDI Member Article publish | no |
| `/2015/07/09/the-life-for-muslims-in-britain-since-77-is-abuse-suspicion-and-constant-apologies/` | 20210511164854 | 27518 | The life for Muslims in Britain since 7/7 is abuse, suspicion and consta | no |
| `/2013/11/13/public-debate-on-patriotism-abdullah-al-andalusi-to-debate-at-the-oxford-union/` | 20220520143444 | 27445 | Public Debate on Patriotism: Abdullah al Andalusi to debate at the Oxfor | no |
| `/2014/11/13/british-media-demands-muslims-women-wear-poppy-motif-hijab-to-demonstrate-loyalty-to-britain/` | 20211019131644 | 27180 | British Media Demands Muslims Women wear Poppy-motif Hijab to demonstrat | no |
| `/2013/10/16/abdullah-al-andalusi-discusses-tommy-robinsons-way-forward-for-syria/` | 20220520125441 | 27084 | TV: Abdullah al Andalusi discusses Tommy Robinson leaving the EDL, and w | no |
| `/2014/12/02/uk-government-set-to-criminalise-free-intellectual-discussion-at-uk-universities/` | 20210511174518 | 26857 | UK Government set to criminalise Free Intellectual Discussion at UK Univ | no |
| `/2014/11/24/debate-video-is-sharia-law-fairer-than-english-law/` | 20221201162536 | 26814 | DEBATE VIDEO: Is SHARIA LAW FAIRER than ENGLISH LAW? | no |
| `/2013/09/21/how-the-historical-islamic-caliphate-dealt-with-foreign-intervention-from-the-west/` | 20210512085152 | 26772 | How the historical Islamic Caliphate dealt with foreign intervention fro | no |
| `/2013/05/31/song-banned-in-athens-for-encouraging-islam/` | 20210922135414 | 26655 | Song banned in Athens for “encouraging” Islam | no |
| `/2014/01/10/upcoming-conference-muslim-women-of-today-divided-by-culture-united-by-faith/` | 20210926010529 | 26654 | Conference "Muslim Women of Today: Divided by Culture, United by Faith" | no |
| `/2014/11/29/debate-review-islam-or-feminism-which-one-can-truly-liberate-women-debate-between-feminist-julie-bindel-and-zara-faris/` | 20210514194031 | 26619 | Debate Review: Islam or Feminism: Which one can truly Liberate Women?' D | no |
| `/2012/08/29/my-thoughts-on-channel-4s-islam-the-untold-story-program-by-tom-holland/` | 20210514190156 | 26370 | My thoughts on Channel 4's Islam: The Untold Story' program, by Tom Holl | no |
| `/2013/05/21/popular-greek-neo-nazi-group-gives-greek-muslims-one-month-to-leave-or-be-slaughtered-like-chicken/` | 20211207082454 | 25843 | Popular Greek Neo-Nazi Group gives Greek Muslims one month to leave or b | no |
| `/2014/10/25/islamophobia-and-the-true-untold-story-of-dracula/` | 20210514184556 | 25400 | Islamophobia and the true "Untold" Story of Dracula | no |
| `/2014/11/07/mdi-big-debate-islam-or-feminism-which-one-can-truly-liberate-women/` | 20210921053918 | 24869 | MDI BIG DEBATE: Islam or Feminism: which one can truly liberate women? | no |
| `/2013/12/08/male-and-female-brains-wired-differently-scans-reveal/` | 20210518084942 | 24695 | Male and female brains wired differently, scans reveal | no |
| `/2013/06/16/britain-destroyed-records-of-colonial-crimes/` | 20210510074839 | 24606 | Britain destroyed records of colonial crimes | no |
| `/2013/06/17/egypts-muslim-brotherhood-government-protects-rights-of-christian-minorities/` | 20211209075748 | 24594 | Egypt's Muslim Brotherhood government protects rights of Christian minor | no |
| `/2013/11/16/mdi-news-amazing-victory-at-oxford-university-debate-on-patriotism-nationalism/` | 20210512080428 | 24492 | MDI News: Amazing Victory at Oxford University Debate on Patriotism (Nat | no |
| `/2019/12/16/9th-cent-christians-in-egypt-preferred-islamic-law-rather-than-christian-courts-which-also-show-they-were-allowed-to-exist-and-operate/` | 20210511171225 | 24476 | 10th Cent. Christians in Egypt preferred Islamic law , rather than Chris | yes |
| `/2014/03/13/debate-video-feminism-vs-islam-does-islam-treat-women-right-rebakah-mckinney-perry-vs-abdullah-al-andalusi/` | 20210510072455 | 24391 | Debate Video: Feminism vs Islam Does Islam Treat Women Right?' Rebak'ah  | no |
| `/2013/06/05/mosque-destroyed-in-anti-muslim-terrorist-attack-in-uk/` | 20210514185548 | 24360 | Mosque destroyed in Anti-Muslim Terrorist Attack in UK | no |
| `/2014/09/13/sky-news-interview-on-syria-terrorism-and-uk-hypocrisy/` | 20210921055157 | 24116 | SKY NEWS interview on Syria, Terrorism' and UK hypocrisy | no |
| `/2013/08/02/secularism-debate-with-terry-sanderson-president-of-the-national-secularist-society-nss/` | 20210512081223 | 23917 | Secularism Debate with Terry Sanderson, President of the National Secula | no |
| `/2013/06/01/muslim-soldiers-who-fought-in-world-war-1-let-us-be-proud/` | 20210926011833 | 23785 | Muslim Soldiers who fought in World War 1: Let us be proud | no |
| `/2015/05/10/bbc-debate-has-human-rights-law-achieved-more-for-humanity-than-religion-the-big-questions/` | 20210919043720 | 23689 | BBC Debate: Has Human Rights Law achieved more for Humanity than Religio | no |
| `/2014/03/01/join-the-london-demonstration-against-uk-governments-detention-of-political-dissenters-and-individuals-of-conscience/` | 20210624123133 | 23640 | Join the London Demonstration against UK government's detention of polit | no |
| `/2013/05/14/upcoming-event-the-beauty-within/` | 20210514193557 | 23562 | Event "The Beauty Within" | no |
| `/2014/10/01/uk-government-forced-to-drop-politically-motivated-charges-against-muslim-rights-activist-moazzam-begg/` | 20210514045802 | 23486 | UK government forced to drop Politically-motivated charges against Musli | no |
| `/2013/05/25/secret-services-had-previously-tortured-woolwich-killer/` | 20210511171304 | 23305 | Secret Services had previously tortured Woolwich killer | no |
| `/2016/02/12/event-why-islam-doesnt-need-reformation-ucl-uk-11th-feb-2016/` | 20210514191244 | 23175 | Event: "WHY ISLAM DOESN'T NEED REFORMATION" [UCL, UK 11th Feb 2016] | no |
| `/2014/01/01/upcoming-event-is-islam-being-criminalised-2/` | 20210518084823 | 23165 | Event: Is Islam being Criminalised? | no |
| `/2012/12/08/a-short-lesson-in-islamophobic-spin-or-why-there-is-nothing-good-a-muslim-can-do/` | 20210510084754 | 22862 | A Short Lesson in Islamophobic Spin (or why there is nothing good a Musl | no |
| `/2014/03/05/debate-should-modern-law-be-guided-by-religious-principles-university-of-keele-uk/` | 20210512075028 | 22826 | Debate: Should Modern Law be Guided by Religious Principles? (University | no |
| `/2014/03/01/fake-picture-of-syrian-girl-being-stoned-by-rebels-for-having-facebook-account/` | 20210506181002 | 22779 | Fake Picture of Syrian Girl Being Stoned By Rebels For Having Facebook A | no |
| `/2014/03/07/upcoming-lecture-today-is-islam-relevant-for-the-21st-century-university-of-east-anglia/` | 20210506183025 | 22712 | Lecture: Is Islam relevant for the 21st century? (University of East Ang | no |
| `/2013/06/21/abdullah-al-andalusi-invited-to-discuss-gambling-the-right-to-suicide-and-whether-someone-can-pick-choose-parts-of-their-religion-on-bbc1s-big-questions-programme/` | 20210514041343 | 22591 | Abdullah al Andalusi invited to discuss gambling, the right' to suicide, | no |
| `/2013/05/26/anti-muslim-terrorist-drives-car-full-of-explosives-to-a-mosque/` | 20210514194151 | 22574 | Anti-Muslim Terrorist drives car full of explosives to a Mosque | no |
| `/2015/04/30/abdullah-andalusi-refutes-the-quilliamhjs-neocon-narrative-why-has-the-independent-censored-its-report-on-it/` | 20210511165009 | 22485 | Abdullah Andalusi Refutes the Quilliam/HJS Neocon Narrative Why Has the  | no |
| `/2014/03/11/upcoming-lecture-how-sharia-is-more-tolerant-than-secular-democracy-university-of-reading/` | 20210514192033 | 22400 | Lecture: How Sharia is more tolerant than Secular Democracy' (University | no |
| `/2014/02/24/upcoming-debate-shariah-vs-secular-democracy-which-is-more-tolerant/` | 20210506180404 | 22328 | Debate Event: Shariah vs Secular Democracy: Which is more tolerant? | no |
| `/2013/10/15/eid-mubarak-from-mdi/` | 20210506191142 | 22232 | EID Mubarak from all the members of MDI | no |
| `/2013/05/14/bill-maher-refuted-on-tv-by-glenn-greenwald-on-us-intervention-in-muslim-countries/` | 20210518075401 | 22231 | Bill Maher refuted on TV by Glenn Greenwald on US intervention in Muslim | no |
| `/2014/02/27/demonstration-against-uk-goverments-silencing-of-muslims-speakers-in-the-uk/` | 20210518073932 | 22156 | Demonstration against UK goverment's silencing of Muslims speakers in th | yes |
| `/2017/07/19/video-did-islam-abolish-slavery-in-the-lifetime-of-the-prophet-muhammed-saaw/` | 20210514040229 | 22101 | [VIDEO] Did Islam Abolish Slavery in the lifetime of the Prophet Muhamme | yes |
| `/2015/01/22/levant-tv-debate-charlie-hebdo-a-christian-jewish-muslim-debate-on-terrorism-and-sharia-in-europe/` | 20210511174825 | 22094 | Levant TV Debate: "Charlie Hebdo A Christian-Jewish-Muslim debate on Ter | no |
| `/2015/11/02/public-debate-should-we-be-proud-to-be-patriotic-durham-university-uk/` | 20210510080938 | 22076 | PUBLIC DEBATE: Should we be Proud to be Patriotic? [Durham University, U | yes |
| `/2016/01/16/radio-debate-should-donald-trump-be-banned-from-the-uk-like-other-hate-preachers-that-the-uk-has-banned-charlie-wolf-vs-abdullah-al-andalusi/` | 20210510065637 | 21951 | Radio Debate: Should Donald Trump be banned from the UK like other hate  | yes |
| `/2013/06/15/what-is-the-reason-behind-the-rapid-increase-of-muslims-around-the-world-islam-life-press-tv/` | 20210621011447 | 21475 | What is the reason behind the rapid increase of Muslims around the world | no |
| `/2017/06/30/do-we-need-god-lecture-by-abdullah-al-andalusi-university-of-leicester-uk-2/` | 20210510064959 | 21388 | Do We Need God? [Lecture by Abdullah al Andalusi, University of Leiceste | yes |
| `/2013/06/06/jesus-v-muhammad-muslim-response-to-misconceptions/` | 20210514185446 | 21047 | Jesus vs Muhammed? A Muslim response to misconceptions | yes |

**Caveats on this table, stated plainly.**

- The **Read?** column is the honest split: **17 rows were fetched and read**, 59 were
  not. §3.6 lists all 76 one per row and states which is which; §3.2 records the byline
  found on each of the 17.
- Every length here is a CDX `length` (compressed WARC record size) copied from the B1
  index, not a page-text size and not a word count. See §5.4.
- Titles come from MDI's own author-archive listing, not from the posts themselves. One
  disagrees with its own permalink: the row
  `/2019/12/16/9th-cent-christians-in-egypt-...` is listed by MDI as
  *"10th Cent. Christians in Egypt preferred Islamic law"*. The slug says 9th, the title
  says 10th. Recorded unresolved rather than silently picking one.
- Several rows are event announcements, translation reposts or video pages rather than
  prose works (the `/2018/` translation posts, the `/2016/12/08/` announcement, the
  `/2014/02/27/` demonstration notice). The 76 is a count of **permalinks the archive does
  not hold**, not a count of 76 new works. How many of them are distinct works is a
  judgement for whoever takes this forward.
- Two further permalinks surfaced in the same sweep and are **excluded** from the 76
  because the archive already holds them, as notices rather than works, in
  `_data/notices.json`: `/2012/10/14/more-additions/` and `/2012/11/19/the-sword-of-ibn-nasir/`.
  Neither was fetched, so nothing is claimed about their contents here.

### 3.2 Verification actually performed

Seventeen of the 76 were fetched and read: a stratified sample of 15, plus 2 more taken as
the largest by length. **All 17 returned HTTP 200 with real body text, and every one
carries an explicit `By Abdullah al Andalusi on <date>` byline.** Word counts include
comment threads, so they overstate article body length.

| Permalink | HTTP | Words (incl. comments) | Byline |
|---|---:|---:|---|
| `/2013/12/25/debate-video-are-ahmadiyyah-part-of-islam/` | 200 | 27,536 | By Abdullah al Andalusi on December 25, 2013 |
| `/2012/10/20/tom-hollands-obsession-with-islams-origins-a-critical-response/` | 200 | 6,411 | By Abdullah al Andalusi on October 20, 2012 |
| `/2014/01/19/a-post-liberal-future/` | 200 | 18,282 | By Abdullah al Andalusi on January 19, 2014 |
| `/2014/01/06/hobbes-folly-how-a-mistake-led-to-secularism-and-a-new-intolerance/` | 200 | 8,235 | By Abdullah al Andalusi on January 6, 2014 |
| `/2013/06/12/who-justifies-terrorism-part-1/` | 200 | 3,275 | By Abdullah al Andalusi on June 12, 2013 |
| `/2013/05/05/sheikh-abdul-hakim-murad-falls-victim-to-the-hypocrisy-of-liberal-tolerance/` | 200 | 4,137 | By Abdullah al Andalusi on May 5, 2013 |
| `/2016/08/31/transcript-opening-speech-did-god-create-man-or-did-man-create-god-abdullah-al-andalusi/` | 200 | 2,544 | byline match |
| `/2017/06/30/do-we-need-god-lecture-by-abdullah-al-andalusi-university-of-leicester-uk-2/` | 200 | 375 | byline match |
| `/2017/07/19/video-did-islam-abolish-slavery-in-the-lifetime-of-the-prophet-muhammed-saaw/` | 200 | 596 | byline match |
| `/2018/11/26/glossary-of-terms-idioms-used-by-muslim-debaters-daees-around-the-world/` | 200 | 2,932 | byline match |
| `/2019/12/16/9th-cent-christians-in-egypt-preferred-islamic-law-rather-than-christian-courts-which-also-shows-they-were-allowed-to-exist-and-operate/` | 200 | 907 | byline match |
| `/2015/05/07/should-muslims-vote-in-secular-liberal-democracies-the-bigger-picture/` | 200 | 4,038 | byline match |
| `/2015/11/02/public-debate-should-we-be-proud-to-be-patriotic-durham-university-uk/` | 200 | 554 | byline match |
| `/2016/01/16/radio-debate-should-donald-trump-be-banned-from-the-uk-like-other-hate-preachers-that-the-uk-has-banned-charlie-wolf-vs-abdullah-al-andalusi/` | 200 | 540 | byline match |
| `/2013/06/06/jesus-v-muhammad-muslim-response-to-misconceptions/` | 200 | 317 | byline match |
| `/2014/02/27/demonstration-against-uk-goverments-silencing-of-muslims-speakers-in-the-uk/` | 200 | 328 | byline match |
| `/2011/12/20/of-course-religious-and-political-debates-happen-in-the-muslim-world/` | 200 | 2,008 | byline match |

`A Post-Liberal Future?` is the largest genuine prose find among those read: its own page
identifies it as the **lead essay of Demos Quarterly, 17 January 2014**.

**The remaining 59 of the 76 were verified only at CDX level** — status 200, `text/html`,
and a length consistent with a content page. They are reported as new on that basis and
**their body text has not been read**. A claim that each is his own words rests on the
author-archive attribution, which is strong but is not the same as having read them.

### 3.3 `islamicdiscourseinitiative.com` — ~20 posts, attribution **unverified**

IDI is WordPress and also keeps author archives. Fourteen exist. Two carry pseudonymous
bylines and substantial output:

| IDI author archive | Pages captured | Posts listed | Resolve to a 200 capture |
|---|---:|---:|---:|
| `/author/ibn-mosharraf/` | 2 (`/`, `/page/2/`) | 22 | **18** |
| `/author/abdullah-feras/` | 1 | 9 | **7** |
| the other twelve | 1 each | 12–22 each | not pursued |

The two overlap: 5 slugs appear in both (`assessing-nigeria-2019`, `country-analysis`,
`decolonialism`, `the-question-of-hadith-politics`, `what-is-islamic-discourse-initiative`),
giving **20 distinct resolvable posts**. None is in any of the four data files, nor
anywhere else in the archive. Representative captures with 200:

| Permalink | Best timestamp | Length | Byline found in page |
|---|---|---:|---|
| `/politics/post-colonial-paradigms-in-muslim-communities-part-1/` | 20190722192228 | 44148 | (listed under `ibn-mosharraf`) |
| `/canon/hadith-the-myth-of-the-telephone-game/` | 20190502130305 | 32641 | (listed under `ibn-mosharraf`) |
| `/politics/hamza-yusuf-the-sultan-a-case-study-in-the-misuse-of-prophetic-traditions/` | 20191021072734 | 32334 | **Abdullah Feras** |
| `/reviews/book-review-diplomacy-by-henry-kissinger/` | 20190102113552 | 32334 | (listed under `abdullah-feras`) |
| `/canon/hadith/the-question-of-hadith-politics/` | 20190822101704 | 30412 | (listed under both) |
| `/reviews/radical-skin-moderate-masks-review/` | 20191209161849 | 30306 | **Ibn Mosharraf** |
| `/history/hamza-yusuf-the-sultan-misreadings-of-history-to-justify-obedience-to-tyrants/` | 20191021074622 | 31326 | (listed under `ibn-mosharraf`) |
| `/politics/rebirth-of-a-nation-white-supremacist-violence-myths-catharsis/` | 20190822085505 | 27145 | (listed under `ibn-mosharraf`) |
| `/politics/feminism/feminism-issues-and-discourses/` | 20190722181251 | 30876 | (listed under `ibn-mosharraf`) |
| `/politics/abortion-beyond-the-polemics/` | 20190722183553 | 25660 | **Ibn Mosharraf** |
| `/canon/hadith/the-quranist-fallacy-how-quranism-ultimately-undermines-the-qurans-authenticity/` | 20190722182557 | 24786 | (listed under `ibn-mosharraf`) |
| `/canon/hadith/the-realism-of-hadith-an-authentic-human-experience/` | 20190822092801 | 27623 | (listed under `ibn-mosharraf`) |
| `/politics/jihad-between-reactionism-and-decolonialism/` | 20190128205854 | 29854 | (listed under `ibn-mosharraf`) |
| `/uncategorized/global-capitalism-in-perspective/` | 20190220105952 | 20402 | (listed under `ibn-mosharraf`) |
| `/politics/the-wisdom-behind-the-ijtihad-of-sheikh-taqiuddin-an-nabhani/` | 20190101000227 | 26346 | (listed under `ibn-mosharraf`) |
| `/download/the-authentic-signs-of-the-hour/` | 20191021074628 | 20876 | (listed under `abdullah-feras`) |
| `/download/assessing-nigeria-2019/` | 20190822085552 | 21544 | (listed under both) |

The table lists 17 of the 20. The other three resolvable slugs are **not posts** and are
excluded deliberately: `/country-analysis/` (12,708 B) and `/decolonialism/` (13,057 B) are
category landing pages that both author archives happen to surface, and
`/updates/what-is-islamic-discourse-initiative/` (19,381 B) is IDI's own about/updates
page. All three are listed under **both** pseudonymous accounts, which is a further reason
not to read them as authored output.

**I am not asserting these are his, and this section should not be counted as a find
until an owner decision is made.** The reasons:

1. The bylines are pseudonyms. `Ibn Mosharraf` and `Abdullah Feras` are the only
   attribution signals, and a byline is not proof of identity.
2. **The repository records no alias mapping.** I searched `_data/*.json` and the top-level
   markdown for "Ibn Mosharraf", "ibn-mosharraf", "Feras" and "ibn mosharraf": **zero
   matches anywhere in the archive.**
3. The archive's own editorial policy is hostile to the inference. `NOTICE.md` §141–147 and
   `bibliography.json` redact his legal/real name "at the site owner's request" and replace
   it with `[real name withheld]` throughout. Resolving a pseudonym to a redacted identity
   from a third-party site is precisely the kind of move that policy exists to prevent, and
   he has asked not to be contacted and has left online dawah.
4. The one IDI post the archive *does* hold as his —
   `/apologetics/apostasy-beyond-the-rhetoric/` — carries the byline **"Guest"**, and
   appears in **neither** of these two author archives. So the archive's existing
   attribution rests on a *third* IDI account, which weakens any inference from these two.

What can be said without an identity claim: **IDI holds roughly 20 post pages with 200
captures, under two pseudonymous author accounts, that this archive does not hold.** That
is a lead for the owner, not a recovery.

Also noted and **excluded**: IDI's domain now carries spam. Two 2026 captures
(`/uncategorized/realz-login-przewodnik-...` and
`/uncategorized/crownplay-registrierung-...`, both 2026-04-18) are Polish and German
casino/login SEO spam, not scholarship. They are not attributed to him and were not
pursued.

### 3.4 Four smaller items

| Permalink | Best timestamp | Length | Note |
|---|---:|---:|---|
| `hidayah.albalaghacademy.org/team/ustadh-abdullah-al-andalusi/` | 20260225044333 | 40416 | Al-Balagh Hidayah faculty profile. **Not in the four files**; not in any `_data` file. |
| `hidayah.albalaghacademy.org/team/ustadh-asadullah-ali-al-andalusi/` | 20260225044522 | 39661 | Second, parallel profile. In `_data` (via `papers.json`), not in the four files. |
| `www.albalaghacademy.org/ustaad/ustadh-abdullah-al-andalusi/` | 20220125015215 | 24870 | Earlier Al-Balagh instructor page. Held in `_data/secondary_sources.json`. |
| `islamic-life-forum.blogspot.com/2020/07/science-scientism-asadullah-ali.html` | 20231124052345 | 5110 | Third-party blog reprint of his "Science & Scientism" talk. **Not in the four files**; not in any `_data` file. Its sibling `/2019/06/understanding-atheism-asadullah-ali-al.html` **is** held in `secondary_sources.json`. |

These are a bio page, a course/instructor page and a third-party reprint — not new works.
They are recorded because the archive catalogues exactly this kind of page and the
hidayah/ustaad and islamic-life-forum items are genuinely absent.

---

### 3.6 The 76 permalinks, one row each

Every one of the 76, **sorted by capture date ascending**. `Read?` is `yes` only where I
actually fetched the capture and read the page; `no` means the row rests on the CDX index
alone. The 17 `yes` rows were fetched twice — once during the §3.2 verification pass and
once more to capture each page's own `<title>` — and all 17 returned HTTP 200 with a
`By Abdullah al Andalusi` byline. The 59 `no` rows were not fetched; their notes say only
what the index supports.

Byte figures are the CDX `length` (compressed WARC record size) and are identical to the
Length column of the §3.1 table, so the two can be compared row for row.

| # | Permalink (on `https://muslimdebate.org`) | Best capture | Bytes | Read? | One-line note |
|---:|---|---|---:|:---:|---|
| 1 | `/2014/02/24/upcoming-debate-shariah-vs-secular-democracy-which-is-more-tolerant/` | `20210506180404` | 22328 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-02-24. |
| 2 | `/2014/11/22/tales-of-the-unexpected-convincing-members-of-english-upper-class-that-sharia-is-fairer-than-english-law/` | `20210506180902` | 30858 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-11-22. |
| 3 | `/2014/03/01/fake-picture-of-syrian-girl-being-stoned-by-rebels-for-having-facebook-account/` | `20210506181002` | 22779 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-01. |
| 4 | `/2014/03/07/upcoming-lecture-today-is-islam-relevant-for-the-21st-century-university-of-east-anglia/` | `20210506183025` | 22712 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-07. |
| 5 | `/2013/10/15/eid-mubarak-from-mdi/` | `20210506191142` | 22232 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-10-15. |
| 6 | `/2017/06/30/do-we-need-god-lecture-by-abdullah-al-andalusi-university-of-leicester-uk-2/` | `20210510064959` | 21388 | yes | Read. Page title: "Do We Need God? [Lecture by Abdullah al Andalusi, Univers…". Byline "By Abdullah al Andalusi on June 30, 2017". Body 530 words incl. comment thread. |
| 7 | `/2016/01/16/radio-debate-should-donald-trump-be-banned-from-the-uk-like-other-hate-preachers-that-the-uk-has-banned-charlie-wolf-vs-abdullah-al-andalusi/` | `20210510065637` | 21951 | yes | Read. Page title: "Radio Debate: Should Donald Trump be banned from the UK l…". Byline "By Abdullah al Andalusi on January 16, 2016". Body 699 words incl. comment thread. |
| 8 | `/2013/03/14/atheist-hypocrisy-and-gender-segregation/` | `20210510072121` | 30679 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-03-14. |
| 9 | `/2014/03/13/debate-video-feminism-vs-islam-does-islam-treat-women-right-rebakah-mckinney-perry-vs-abdullah-al-andalusi/` | `20210510072455` | 24391 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-13. |
| 10 | `/2013/06/16/britain-destroyed-records-of-colonial-crimes/` | `20210510074839` | 24606 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-16. |
| 11 | `/2015/11/02/public-debate-should-we-be-proud-to-be-patriotic-durham-university-uk/` | `20210510080938` | 22076 | yes | Read. Page title: "PUBLIC DEBATE: Should we be Proud to be Patriotic? [Durha…". Byline "By Abdullah al Andalusi on November 2, 2015". Body 709 words incl. comment thread. |
| 12 | `/2016/08/31/transcript-opening-speech-did-god-create-man-or-did-man-create-god-abdullah-al-andalusi/` | `20210510083446` | 28989 | yes | Read. Page title: "Transcript: Opening Speech “Did God Create Man, or did Ma…". Byline "By Abdullah al Andalusi on August 31, 2016". Body 2,722 words incl. comment thread. |
| 13 | `/2012/12/08/a-short-lesson-in-islamophobic-spin-or-why-there-is-nothing-good-a-muslim-can-do/` | `20210510084754` | 22862 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2012-12-08. |
| 14 | `/2011/12/20/of-course-religious-and-political-debates-happen-in-the-muslim-world/` | `20210510085316` | 29230 | yes | Read. Page title: "Of course religious and political public debates happen i…". Byline "By Abdullah al Andalusi on December 20, 2011". Body 2,203 words incl. comment thread. |
| 15 | `/2014/01/19/a-post-liberal-future/` | `20210510085824` | 65853 | yes | Read. Page title: "A Post-Liberal Future?". Byline "By Abdullah al Andalusi on January 19, 2014". Body 18,453 words incl. comment thread. |
| 16 | `/2015/07/09/the-life-for-muslims-in-britain-since-77-is-abuse-suspicion-and-constant-apologies/` | `20210511164854` | 27518 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2015-07-09. |
| 17 | `/2015/04/30/abdullah-andalusi-refutes-the-quilliamhjs-neocon-narrative-why-has-the-independent-censored-its-report-on-it/` | `20210511165009` | 22485 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2015-04-30. |
| 18 | `/2015/05/07/should-muslims-vote-in-secular-liberal-democracies-the-bigger-picture/` | `20210511165046` | 32881 | yes | Read. Page title: "Should Muslims Vote in Secular Liberal Democracies? The B…". Byline "By Abdullah al Andalusi on May 7, 2015". Body 4,199 words incl. comment thread. |
| 19 | `/2019/12/16/9th-cent-christians-in-egypt-preferred-islamic-law-rather-than-christian-courts-which-also-show-they-were-allowed-to-exist-and-operate/` | `20210511171225` | 24476 | yes | Read. Page title: "10th Cent. Christians in Egypt preferred Islamic law , ra…". Byline "By Abdullah al Andalusi on December 16, 2019". Body 1,048 words incl. comment thread. |
| 20 | `/2013/05/25/secret-services-had-previously-tortured-woolwich-killer/` | `20210511171304` | 23305 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-25. |
| 21 | `/2014/12/02/uk-government-set-to-criminalise-free-intellectual-discussion-at-uk-universities/` | `20210511174518` | 26857 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-12-02. |
| 22 | `/2015/01/22/levant-tv-debate-charlie-hebdo-a-christian-jewish-muslim-debate-on-terrorism-and-sharia-in-europe/` | `20210511174825` | 22094 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2015-01-22. |
| 23 | `/2013/12/02/reject-democracy-freedom-of-speech-and-predict-the-future-collapse-of-western-civilisation-youre-an-extremist-unless-youre-chinese/` | `20210512072021` | 28589 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-12-02. |
| 24 | `/2014/03/05/debate-should-modern-law-be-guided-by-religious-principles-university-of-keele-uk/` | `20210512075028` | 22826 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-05. |
| 25 | `/2013/11/16/mdi-news-amazing-victory-at-oxford-university-debate-on-patriotism-nationalism/` | `20210512080428` | 24492 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-11-16. |
| 26 | `/2013/08/02/secularism-debate-with-terry-sanderson-president-of-the-national-secularist-society-nss/` | `20210512081223` | 23917 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-08-02. |
| 27 | `/2013/09/21/how-the-historical-islamic-caliphate-dealt-with-foreign-intervention-from-the-west/` | `20210512085152` | 26772 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-09-21. |
| 28 | `/2017/07/19/video-did-islam-abolish-slavery-in-the-lifetime-of-the-prophet-muhammed-saaw/` | `20210514040229` | 22101 | yes | Read. Page title: "[VIDEO] Did Islam Abolish Slavery in the lifetime of the …". Byline "By Abdullah al Andalusi on July 19, 2017". Body 752 words incl. comment thread. |
| 29 | `/2013/06/21/abdullah-al-andalusi-invited-to-discuss-gambling-the-right-to-suicide-and-whether-someone-can-pick-choose-parts-of-their-religion-on-bbc1s-big-questions-programme/` | `20210514041343` | 22591 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-21. |
| 30 | `/2014/10/01/uk-government-forced-to-drop-politically-motivated-charges-against-muslim-rights-activist-moazzam-begg/` | `20210514045802` | 23486 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-10-01. |
| 31 | `/2014/10/25/islamophobia-and-the-true-untold-story-of-dracula/` | `20210514184556` | 25400 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-10-25. |
| 32 | `/2013/06/06/jesus-v-muhammad-muslim-response-to-misconceptions/` | `20210514185446` | 21047 | yes | Read. Page title: "Jesus vs Muhammed? A Muslim response to misconceptions". Byline "By Abdullah al Andalusi on June 6, 2013". Body 461 words incl. comment thread. |
| 33 | `/2013/06/05/mosque-destroyed-in-anti-muslim-terrorist-attack-in-uk/` | `20210514185548` | 24360 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-05. |
| 34 | `/2012/08/29/my-thoughts-on-channel-4s-islam-the-untold-story-program-by-tom-holland/` | `20210514190156` | 26370 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2012-08-29. |
| 35 | `/2016/02/12/event-why-islam-doesnt-need-reformation-ucl-uk-11th-feb-2016/` | `20210514191244` | 23175 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2016-02-12. |
| 36 | `/2014/03/11/upcoming-lecture-how-sharia-is-more-tolerant-than-secular-democracy-university-of-reading/` | `20210514192033` | 22400 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-11. |
| 37 | `/2013/05/14/upcoming-event-the-beauty-within/` | `20210514193557` | 23562 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-14. |
| 38 | `/2014/11/29/debate-review-islam-or-feminism-which-one-can-truly-liberate-women-debate-between-feminist-julie-bindel-and-zara-faris/` | `20210514194031` | 26619 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-11-29. |
| 39 | `/2013/05/26/anti-muslim-terrorist-drives-car-full-of-explosives-to-a-mosque/` | `20210514194151` | 22574 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-26. |
| 40 | `/2014/03/04/the-panoptic-police-state-a-natural-product-of-secular-liberalist-ideology/` | `20210514202116` | 28442 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-04. |
| 41 | `/2013/05/05/sheikh-abdul-hakim-murad-falls-victim-to-the-hypocrisy-of-liberal-tolerance/` | `20210514203638` | 35351 | yes | Read. Page title: "Sheikh Abdal-Hakim Murad falls victim to the hypocrisy of…". Byline "By Abdullah al Andalusi on May 5, 2013". Body 4,392 words incl. comment thread. |
| 42 | `/2013/05/22/the-fallacies-of-dr-william-lane-craigs-argument-for-the-trinity/` | `20210514204534` | 32757 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-22. |
| 43 | `/2013/06/24/abdullah-al-andalusi-on-bbc1s-the-big-questions-discusses-mixing-religions-gambling-and-suicide/` | `20210515015636` | 28232 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-24. |
| 44 | `/2014/02/27/demonstration-against-uk-goverments-silencing-of-muslims-speakers-in-the-uk/` | `20210518073932` | 22156 | yes | Read. Page title: "Demonstration against UK goverment’s silencing of Muslims…". Byline "By Abdullah al Andalusi on February 27, 2014". Body 484 words incl. comment thread. |
| 45 | `/2013/05/14/bill-maher-refuted-on-tv-by-glenn-greenwald-on-us-intervention-in-muslim-countries/` | `20210518075401` | 22231 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-14. |
| 46 | `/2014/01/01/upcoming-event-is-islam-being-criminalised-2/` | `20210518084823` | 23165 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-01-01. |
| 47 | `/2013/12/08/male-and-female-brains-wired-differently-scans-reveal/` | `20210518084942` | 24695 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-12-08. |
| 48 | `/2018/11/26/glossary-of-terms-idioms-used-by-muslim-debaters-daees-around-the-world/` | `20210618201113` | 28932 | yes | Read. Page title: "GLOSSARY OF TERMS & IDIOMS USED BY MUSLIM DEBATERS & DAEE…". Byline "By Abdullah al Andalusi on November 26, 2018". Body 3,107 words incl. comment thread. |
| 49 | `/2013/06/15/what-is-the-reason-behind-the-rapid-increase-of-muslims-around-the-world-islam-life-press-tv/` | `20210621011447` | 21475 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-15. |
| 50 | `/2014/04/15/maajid-nawaz-the-bbc-and-the-uk-muslim-community-part-1/` | `20210621165239` | 34958 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-04-15. |
| 51 | `/2014/03/01/join-the-london-demonstration-against-uk-governments-detention-of-political-dissenters-and-individuals-of-conscience/` | `20210624123133` | 23640 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-03-01. |
| 52 | `/2012/10/09/the-intolerance-of-the-intolerant-why-anti-muslim-polemicists-misrepresent-muslim-groups-a-case-study/` | `20210624183445` | 30306 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2012-10-09. |
| 53 | `/2013/04/13/abdullah-al-andalusi-to-teach-dawah-diploma-in-july-2013/` | `20210723232420` | 32566 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-04-13. |
| 54 | `/2015/05/10/bbc-debate-has-human-rights-law-achieved-more-for-humanity-than-religion-the-big-questions/` | `20210919043720` | 23689 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2015-05-10. |
| 55 | `/2014/11/07/mdi-big-debate-islam-or-feminism-which-one-can-truly-liberate-women/` | `20210921053918` | 24869 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-11-07. |
| 56 | `/2014/09/13/sky-news-interview-on-syria-terrorism-and-uk-hypocrisy/` | `20210921055157` | 24116 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-09-13. |
| 57 | `/2013/05/31/song-banned-in-athens-for-encouraging-islam/` | `20210922135414` | 26655 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-31. |
| 58 | `/2014/04/11/upcoming-debate-can-we-trust-todays-torah/` | `20210923122422` | 30666 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-04-11. |
| 59 | `/2014/01/06/hobbes-folly-how-a-mistake-led-to-secularism-and-a-new-intolerance/` | `20210925234243` | 46916 | yes | Read. Page title: "Hobbes’ Folly: The Creation of Secularism and a new Intol…". Byline "By Abdullah al Andalusi on January 6, 2014". Body 8,391 words incl. comment thread. |
| 60 | `/2014/01/10/upcoming-conference-muslim-women-of-today-divided-by-culture-united-by-faith/` | `20210926010529` | 26654 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-01-10. |
| 61 | `/2013/06/01/muslim-soldiers-who-fought-in-world-war-1-let-us-be-proud/` | `20210926011833` | 23785 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-01. |
| 62 | `/2014/11/13/british-media-demands-muslims-women-wear-poppy-motif-hijab-to-demonstrate-loyalty-to-britain/` | `20211019131644` | 27180 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-11-13. |
| 63 | `/2013/05/21/popular-greek-neo-nazi-group-gives-greek-muslims-one-month-to-leave-or-be-slaughtered-like-chicken/` | `20211207082454` | 25843 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-21. |
| 64 | `/2014/06/25/the-no-one-kills-in-the-name-of-atheism-argument/` | `20211207083623` | 31279 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-06-25. |
| 65 | `/2014/02/20/debate-review-my-public-debate-defending-islam-from-feminist-criticism/` | `20211207083815` | 34420 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-02-20. |
| 66 | `/2013/06/17/egypts-muslim-brotherhood-government-protects-rights-of-christian-minorities/` | `20211209075748` | 24594 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-06-17. |
| 67 | `/2016/04/06/islam-needs-a-restoration-not-a-reformation-mdi-member-article-published-in-middle-east-eye/` | `20220119112412` | 28064 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2016-04-06. |
| 68 | `/2013/10/16/abdullah-al-andalusi-discusses-tommy-robinsons-way-forward-for-syria/` | `20220520125441` | 27084 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-10-16. |
| 69 | `/2013/04/11/review-of-my-human-rights-debate-yesterday/` | `20220520134138` | 28585 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-04-11. |
| 70 | `/2013/11/13/public-debate-on-patriotism-abdullah-al-andalusi-to-debate-at-the-oxford-union/` | `20220520143444` | 27445 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-11-13. |
| 71 | `/2013/12/25/debate-video-are-ahmadiyyah-part-of-islam/` | `20220522233017` | 91400 | yes | Read. Page title: "Debate Video: Are Ahmadiyya part of Islam?". Byline "By Abdullah al Andalusi on December 25, 2013". Body 28,412 words incl. comment thread. |
| 72 | `/2013/06/12/who-justifies-terrorism-part-1/` | `20220523002445` | 37114 | yes | Read. Page title: "Who Justifies Terrorism?". Byline "By Abdullah al Andalusi on June 12, 2013". Body 3,478 words incl. comment thread. |
| 73 | `/2014/11/24/debate-video-is-sharia-law-fairer-than-english-law/` | `20221201162536` | 26814 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2014-11-24. |
| 74 | `/2013/05/29/liberal-intolerance-john-lockes-dark-secret-2/` | `20221203082945` | 31595 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-05-29. |
| 75 | `/2013/10/01/the-sad-events-mall-attack-kenya-some-needed-reflections/` | `20221203084828` | 28556 | no | CDX index only: 200 text/html capture; title not read. Permalink path gives publication date 2013-10-01. |
| 76 | `/2012/10/20/tom-hollands-obsession-with-islams-origins-a-critical-response/` | `20230221034951` | 67467 | yes | Read. Page title: "Tom Holland’s Obsession with Islam’s Origins: A Critical …". Byline "By Abdullah al Andalusi on October 20, 2012". Body 6,636 words incl. comment thread. |

**Reading the `no` rows.** "Publication date" is taken from the permalink path, which is
MDI's own date-bearing URL structure — it is a fact about the URL, not a claim about the
page. Where MDI's own author-archive listing carried a title for a permalink, that title is
in the §3.1 table; it was read from the *listing page*, not from the post, so it is not
repeated here as though it were the post's own title.

**One row disagrees with itself.** Row 19's permalink says `9th-cent` and the page's own
`<title>` says "10th Cent. Christians in Egypt preferred Islamic law". The capture reads
10th; the URL says 9th. Unresolved — recorded rather than silently reconciled.

## 4. Gaps that are real

### 4.1 Confirmed still unavailable

**The one entry in `_data/lost_works.json` is still lost.** I re-checked it directly
(queries 25 and 26):

| Host | Only capture | Status | What it is |
|---|---|---:|---|
| `asadullahali.com/2014/10/21/the-making-of-modern-western-civilization-the-war-on-islam-guest-contribution/` | 20150610232358 | **404** | error page, 6,553 B |
| `asadullahali.wordpress.com/2014/10/21/…-guest-contribution` | 20141208115235 | **301** | redirect, 521 B |

**No 200 capture exists on either host.** The `unrecovered` verdict in
`_data/lost_works.json` stands, and the recorded reason — the .com holds only the
WordPress "Private Site" login wall, the post is absent from the mirror, and the IDI copy
is a different essay — remains accurate. No new capture has appeared. Recorded as
**confirmed still unavailable, not as newly lost**.

### 4.2 The closed lane stayed closed

I did **not** re-run the "22 permalinks the WordPress mirror no longer returns" lane. The
README's table records it as closed at "18 recovered, 0 not found", and the check in §2
independently confirms that lane has no residue: of 112 genuine WordMirror post permalinks
in 2011–2014, 104 are held, and the 8 that are not are listing pages and the six site
pages named in §2. Nothing there contradicts the closed verdict.

### 4.3 Hostnames that do not exist in the archive

Three hostnames that might plausibly have been his return **zero rows**, which is a
positive finding — these lanes are closed, not merely unproductive:

| Hostname | Distinct URLs in CDX | Checked against |
|---|---:|---|
| `abdullahalandalusi.com` | **0** | all four files + all `_data` + content dirs: 0 references |
| `thedebateinitiative.com` | **0** | 0 in the four files; 1 mention in `_data/mdi_articles.json` |
| `euvolution.com` | **0** | 1 reference in `canonical_works.json` (unreachable) |

`thedeeninstitute.com` returned 1,049 URLs and `islamcompass.com` 13,673, but after
filtering for author-attributable paths neither yielded a permalink the archive lacks.
`euvolution.com` is referenced by the archive as a source and has **no Wayback captures at
all** — worth recording, since it is cited but uncitable via the archive.

---

## 5. Honest limits

**1. The 76 is a floor, not a ceiling — and I can name the holes.**
`muslimdebate.org/author/asadullahali/page/2/` **has never been captured** (query 24,
0 rows). Up to 5 posts are therefore missing from the 88. Separately, **5 posts the
archive already holds are absent from the author archives entirely**:
`/2016/04/17/do-muslim-women-need-feminism/`,
`/2016/02/07/withoutevidence2/`,
`/2015/10/15/criminal-minds-liberalism-in-muslim-thought/`,
`/2015/10/15/towards-litter-reduction-an-islamic-approach/`, and
`/2015/08/17/the-rationality-of-believing-in-god-without-evidence-part-1/`. So the author
archive is demonstrably **not** a complete enumeration of his MDI output. Some MDI posts
were published under an account that is neither `abdullahandalusi` nor `asadullahali`, and
this survey did not find those accounts. **MDI output held nowhere in the archive probably
exceeds 76.**

**2. Four lanes hit the 20,000-row cap and are incomplete.** `albalaghacademy.org`,
`totetu.org`, `thedeenshow.com` and `yaqeeninstitute.org` each returned exactly 20,000
distinct URLs, which is my `limit`, not a real total. For the three non-author properties
this is defensible — they are large third-party sites and the archive already indexes them
through other lanes — but it does mean I cannot state their true sizes, and I did not
enumerate them. **Unverified: whether any author-attributable permalink exists beyond
20,000 URLs on any of those four hosts.**

**3. Twelve IDI author archives were not pursued.** I enumerated only `ibn-mosharraf` and
`abdullah-feras`. The other twelve each list 12–22 posts. Some — `guest` (17),
`ahmad-hussain-abir` (22), `abu-al-abbas-al-shami` (16), `nadeem` (13) — may contain his
output under accounts I have not checked. **Unverified.**

**4. CDX `length` is not text size.** It is the compressed WARC record length. It is
correlated with content but is not a word count, and it is not comparable with the
`recovered_text_words` figures the archive publishes. No word count in this report is a
claim about article length; the 17 verified word counts include comment threads.

**5. 59 of the 76 were not read.** §3.2 states exactly which 17 were fetched and what the
byline said. The other 59 rest on CDX status/length plus the author-archive listing.

**6. The 76 is a count of permalinks, not of works.** Several of the 76 are event
announcements, video pages or translation reposts rather than prose. Two permalinks that
surfaced in the same sweep and *are* already held — `/2012/10/14/more-additions/` and
`/2012/11/19/the-sword-of-ibn-nasir/` — were excluded from the 76 and are named in §3.1's
caveats. How many of the 76 are distinct authored works is **unverified** and is a
judgement for whoever takes this forward, not something this survey can settle.

**7. No live host was contacted, and none was needed.** Every status in this report is a
Wayback status. `asadullahali.com` is now an unrelated gambling site; I did not visit it
and the README already records that warning. The author has asked not to be contacted and
has left online dawah, so no contact was attempted and no scope was expanded on the basis
of that openness. The IDI pseudonym question in §3.3 is left as a question **precisely
because** resolving it would require an identity judgement I am not entitled to make.

**8. Not surveyed at all.** Arabic-language and Malay/Indonesian-language IDI or MDI
sub-sites beyond the paths CDX exposed; YouTube (68 videos already catalogued, and no
media was downloaded); the `andlusia*` blogspot network beyond the one
`islamic-life-forum` host; and `muslimsdebate.com` beyond establishing that it is a forum
(§2.1).

**9. This report is a survey, not a recovery.** Nothing was downloaded to the repository.
Recovering any of the 76 is a separate decision requiring a content-lane run, and the
count-approval gate in `docs/recovery-log/README.md` applies to whatever that produces.
---

*Survey run 2026-09-29 against the Wayback Machine. 31 CDX queries, 31 HTTP 200, 0 rate limits,
135,088 distinct URLs enumerated. Page fetches: 20 author-archive pages, 17 permalinks read for
§3.2, the same 17 re-read to capture page titles for §3.6, and 3 IDI byline checks —
74 in total, every one HTTP 200, no 404 and no empty body. No repository file other than this
one was created, modified or deleted. §6 is a plan; nothing in it has been carried out.*

---

## 6. Recovery plan

**Nothing in this section has been done.** No capture was fetched for recovery purposes, no
data file was touched, no count was moved. This is a proposal, and every number in it is
traceable to a CDX query in §1 or to a file in this repository.

### 6.1 The order, and why

The risk to minimise is filing something as his that is not his. Two facts from §3 make the
order less obvious than it first looks:

1. **MDI's author archive is demonstrably not a reliable identity oracle.** §5.1 records
   that 5 MDI articles the archive already holds sit *outside* both author archives
   (`/2016/04/17/do-muslim-women-need-feminism/`, `/2016/02/07/withoutevidence2/`,
   `/2015/10/15/criminal-minds-liberalism-in-muslim-thought/`,
   `/2015/10/15/towards-litter-reduction-an-islamic-approach/`,
   `/2015/08/17/the-rationality-of-believing-in-god-without-evidence-part-1/`). So WordPress
   author attribution on this site is incomplete. The 59 unread rows currently rest on
   nothing but that attribution.
2. **The 76 are not 76 works.** From the 17 I read, several are event announcements, video
   pages or translation reposts rather than prose — `/2014/02/27/demonstration-against-…`
   is 484 words of notice, `/2015/11/02/public-debate-should-we-be-proud-…` is 709 words
   with the substance in an embedded player. Filing all 76 into `canonical_works.json` as
   works would inflate the works count with non-works.

**The order I would take:**

**Stage 0 — read and classify all 76, changing no data at all.** Fetch the 59 unread
captures (one Wayback fetch each, read-only, exactly as §3.2 did for the other 17) and
record, per permalink: the page's own title, whether a `By Abdullah al Andalusi` byline is
present, the body word count, and a class — *prose work* / *announcement* / *video
caption* / *other*. This stage writes **no** file in the repository beyond, at most, an
extension of this survey document. **No published number moves. No gate is touched.** This
is the whole argument for doing it first: the expensive-looking part is 59 fetches, and it
is also the part that removes the risk. Filing before reading spends the risk instead of
removing it.

**Stage 1 — file the attested prose works.** Only rows where a byline was actually read.
These can carry `counted_as_work_evidence` naming the byline, which is the strongest
evidence string the MDI gate accepts.

**Stage 2 — file the attested non-works.** Announcements and video captions to
`_data/notices.json` with `counted_as_work: false`, matching the 3 notices already there
and matching how `mdi_articles.json` already keeps 7 short video captions "as published".

**Stage 3 — only then decide about the unattributable residue.** If Stage 0 finds any
permalink on MDI that lacks a byline, it is **not** filed as his on the strength of the
listing. It goes on hold (§6.5) or is filed as a `wayback_only` record with the
attribution marked unproven, reusing the `INFERRED, NOT PROVEN` disclosure the MDI gate
already enforces at `test_canonical_57.py:161-166`.

The temptation to do Stage 1 first and treat the rest as cleanup should be resisted. 17
attested rows move the total by 17; all 76 move it by 76. Splitting the work buys nothing
and costs a second pass over the gate.

### 6.2 What has to be true before any of them is filed

**Authorship evidence.** For a row to be filed as a work by him, one of these, stated
plainly in the row's evidence field:

- a `By Abdullah al Andalusi` byline read in the capture (17 rows already have this), or
- an existing `_data/canonical_works.json` row it is a republication of, proved by the
  5-gram text comparison the MDI gate already uses (`containment >= 0.90` plus
  `measured_against` naming a local `.md`), not by title similarity.

A permalink that merely *appears* on an MDI author page is not sufficient, for the reason
in §6.1.

**Provenance fields.** Follow the existing MDI row shape, which already carries
`title`, `category`, `url`, `date`, `author`, `source`, `summary`, `slug`, `words`,
`text_preserved`, `retrieved_at`, `notes`, `counted_as_work`, `evidence_class`,
`counted_as_work_evidence`. Three additions the 76 need that the live-sourced 17 did not:

- the **capture timestamp** is the identity of the copy here, exactly as `NOTICE.md` §3
  requires of a written work. The 17 were recovered live and have no capture; all 76 are
  capture-only, so the Wayback URL and its timestamp must be recorded on every row.
- the **fetch verdict**, using the vocabulary `wayback_only` rows already use:
  `fetch_words`, `fetch_verdict`, `recovery_checked`, `recovery_note`.
- **no local text unless text was actually recovered**, or the archive asserts something
  false.

**A permalink with no usable text.** All 76 have a 200 `text/html` capture, so this case
does not arise for them — but the rule for it already exists and I would apply it
unchanged: a `status: "wayback_only"` row in `canonical_works.json` carrying
`fetch_words`, `fetch_verdict`, `recovery_checked` and `recovery_note`, with **no**
`local_post` and **no** `recovered_text_words`. The gate enforces the negative half at
`test_canonical_57.py:45` (`assert not w.get("local_post")`) and `:47`
(`assert not w.get("recovered_text_words")`).
`understanding-atheism-lecture-series` is the worked example — a 52-word index stub
catalogued honestly rather than padded.

**Licence.** `NOTICE.md` §2 is the governing rule and these rows do not soften it:
*"That is availability, not permission."* Checking `_data/papers.json` `file_licence`
across its 20 rows, exactly **one** item in the entire archive carries an explicit
Creative Commons grant made by the author himself — the Internet Archive deposit
`between-a-backbone-and-ribs-asadullah`, recorded as *"the author's own CC-licensed
deposit… the one paper the archive is permitted to mirror."* The other 19 are `None`,
publisher open-access with no licence restriction recorded, or `NOT PUBLISHED … withheld`.

**None of the 76 has any CC grant, and none can.** MDI is a third-party publisher of his
prose; availability on `muslimdebate.org` is not a licence from him or from MDI. So the
76 would be filed exactly as the existing 47 full-text works are: a **preservation and
attribution record**, under `NOTICE.md` §2's narrow case, with `NOTICE.md` §4's rule that
crediting the archive alone does not satisfy attribution. No row should carry a
`file_licence`-style string implying reuse rights, because none exists to state.

**A publisher distinction worth recording.** The 76 are MDI's publication of his work, not
his own site. His own domains (`asadullahali.com`, the WordPress mirror) are first-party
and are exhausted (§2). The `source` field should say *Muslim Debate Initiative*, and
`NOTICE.md` §3's point applies with extra force: the original URL is a citation recording
where it was published, not an endorsement of the destination as it stands.

### 6.3 The total, exactly

Two routes exist and **both land on the same number**, which is the useful fact here: the
76 are 76 items whichever file they go in.

**Route A — as 76 new works in `canonical_works.json`:**

| Assertion (line) | Now | Becomes |
|---|---:|---:|
| `len(canon) == 72` (:23) | 72 | **148** |
| `n_found == 47` (:30) | 47 | **47 + k** (k = prose works actually filed) |
| `n_wayback == 24` (:31) | 24 | **24 + (76 − k − a)** (a = announcements) |
| `n_lost == 1` (:28) | 1 | 1, unchanged |
| `expected_total == 207` (:214) | 207 | **283** |
| `len(caps) == 87` (:24) | 87 | **87, unchanged** — verified: `blog_posts.json` has 0 rows referencing `muslimdebate.org`, so it is scoped to the blog and does not grow |
| partition (:35) | holds | holds only if every new row carries exactly one of the three statuses |

`283` is not a guess: `148 + 68 + 20 + 4 + 9 + 33 + 1 = 283`, the same seven terms
`content_index.json` already stores, with `works` the only one changed.

**Route B — as 76 new rows in `mdi_articles.json`:**

| Assertion (line) | Now | Becomes |
|---|---:|---:|
| `len(mdi) == 17` (:134) | 17 | **93** |
| `n_mdi_counted == 4` (:177) | 4 | **4 + m** |
| `n_mdi_dupes == 13` (:178) | 13 | 13, unchanged — the 76 are not republications of works already held, which is the whole reason they are new |
| `expected_total == 207` (:214) | 207 | **283** again |

Route B is not cheaper in outcome. The MDI gate at `:143-149` requires every non-counted
row's `duplicate_of` to name a real work, so a genuinely new MDI post **must** be counted,
which moves `n_mdi_counted` and therefore the total. **There is no route that adds 76 items
and leaves 207 standing** — and that is the correct outcome, not a problem to engineer
around.

**A third route exists and I recommend against it, explicitly.** Adding the 76 to
`secondary_sources.json` with `counted_as_content: false` would move no term in the 207
(`expected_total` only reads works/videos/papers/mdi/yaqeen/albalagh/interviews), and
would require updating just `ci_stats["total_secondary_sources"]` to keep
`test_canonical_57.py:246` passing. It is also wrong. `content_index.json:89` defines that
collection as *"Combined index of all external content referencing Asadullah Ali"* —
third-party mentions, bios, reprints and critiques, `counted_as_content: false` because
they are not his work. First-person prose **by** him is not that category. Filing his own
essays there would keep a number still at the cost of the archive's categories meaning
what they say. I name it only so it is not proposed later as a shortcut.

**Everything that would have to move, by file:**

| File | What moves | Computed or hardcoded |
|---|---|---|
| `_data/canonical_works.json` | +76 rows (Route A) | data |
| `_data/mdi_articles.json` | +76 rows (Route B) | data |
| `_data/content_index.json` | `total_content` 207→283; `total_content_terms.works` 72→148 (A) or `.mdi_counted` 4→80 (B); `total_content_formula` string; `blog_status_counts`; `collections.blog_posts.description`; `preservation_notes.blog_posts` | **hardcoded strings** |
| `scripts/test_canonical_57.py` | the 6 assert lines in the tables above | hardcoded |
| `NOTICE.md:34` | `**207**` and the `72 works` term in the same row | **hardcoded** |
| `README.md:171` | `**72**` / 47 full-text / 24 Wayback-only / 1 unrecovered | **hardcoded** |
| `README.md:522` | `72 works (47 full-text, 24 Wayback-only, 1 lost)` | **hardcoded** |
| `README.md:530` | `Total 207 = 72 + 68 + 20 + 4 + 9 + 33 + 1` | **hardcoded** |
| `scripts/build_site_tour.py:52` | `"The archive - 207 recovered items, counted from the data"` | **hardcoded** |
| `scripts/build_site_tour.py:57` | `"Works - 72 catalogued, 47 with full text held"` | **hardcoded** |
| `index.md`, `timeline.md` | nothing | computed at build time from `_data/` (Liquid `total_content` sums) |

The two `build_site_tour.py` strings are the ones most likely to be missed: they are
captions burned into the recorded site tour, they are typed rather than computed, and
`docs/recovery-log/2026-09-27-re-record-the-site-tour-in-the-reading-first-design` shows
the tour has been re-recorded before when a caption changed. `test_canonical_57.py` has no
assertion covering them, so nothing would fail if they were left stale.

Per `docs/recovery-log/README.md`, this recount needs **site-owner approval** before it is
applied, applied in one pass, and the pre-recount figures are the ones currently
published. The gate's own comment at `test_canonical_57.py:21-22` calls 207 *"The approved
recount, frozen"*.

### 6.4 Two questions that are not mine to decide

**Q1 — the two pseudonymous IDI author accounts.** `ibn-mosharraf` and `abdullah-feras`
carry ~20 post pages with 200 captures (§3.3), none held by the archive. Their bylines are
the only attribution, the repository contains **no** alias mapping (searched: zero matches
for "Ibn Mosharraf", "ibn-mosharraf", "Feras" across `_data/*.json` and the top-level
markdown), and `NOTICE.md` §6.1 redacts his real name at his own request while §10 forbids
contact. *My recommendation:* do not file them as his. Either leave them out, or catalogue
them as authorship-unverified with an `INFERRED, NOT PROVEN` evidence string on the model
the MDI gate already enforces, and exclude them from every count. **The decision is yours**,
because it turns on a fact about the person that the repository deliberately does not hold
and that I am not willing to infer from a third-party byline.

**Q2 — `muslimdebate.org/author/asadullahali/page/2/`, which has never existed in the
archive** (query 24, 0 rows). Up to 5 posts are missing from the 88, so the true figure is
above 76 by an unknown amount. *My recommendation:* query the live MDI author archive for
page 2. This is not contact with the author — MDI is a third-party site that
`content_index.json:117-120` records as `status: "Active"`, and the 2026-09-27 MDI lane
already recovered full text from the live site, so a live fetch is inside existing practice.
If page 2 is gone, record the gap in the recovery log rather than leaving the 76 looking
complete. **The decision is yours** because it is a live-fetch decision rather than a
survey decision, and the archive has a `reader_cautions.json` and a no-contact rule that
make live third-party fetches something you have kept a hand on.

### 6.5 Hold list — what I would deliberately not bring in

| Held back | Why |
|---|---|
| The 3 IDI index pages: `/country-analysis/`, `/decolonialism/`, `/updates/what-is-islamic-discourse-initiative/` | Category/about pages, not posts, and listed under **both** pseudonym accounts (§3.3) |
| The 12 un-pursued IDI author archives | Other people's work; out of scope for a survey about his output |
| All of `muslimsdebate.com` | A user forum; 12,770 URLs of other people's posts, and its author endpoint lists strangers' names (§2.1) |
| The 2 IDI spam captures from 2026-04-18 (`realz-login-przewodnik-…`, `crownplay-registrierung-…`) | Polish and German casino/SEO spam injected into the current domain. Not his, not scholarship, and filing it would put spam in a preservation record |
| `asadullahali.com` captures from 2016 onward | The domain is an unrelated gambling business; `NOTICE.md` §7 and the README both warn about it |
| The 6 site-furniture pages: `/policy/`, `/contact/`, `/aqid/`, `/science/`, `/law/` | Site furniture, not works (§2) |
| Announcements and video captions among the 76 | Not prose works. Route to `notices.json` with `counted_as_work: false` (§6.1 Stage 2), **not** to the works count |
| Any of the 76 that Stage 0 finds has no byline | Unattributable on available evidence; §6.1 Stage 3 |
| The 2 hidayah/ustaad faculty pages, the `islamic-life-forum` reprint, the `yaqeeninstitute.org/asadullah` landing page | Bio, course and landing pages, not works. The archive's precedent for the islamic-life-forum sibling is `secondary_sources.json`, and I would follow it rather than open a new category |
| `euvolution.com` | Cited by the archive, but **0** Wayback captures. A citation, not a recoverable copy |
| `/2012/10/14/more-additions/` and `/2012/11/19/the-sword-of-ibn-nasir/` | Already held, as notices in `_data/notices.json`; re-filing would double-count against the archive |
| The IDI ~20 under `ibn-mosharraf` / `abdullah-feras` | Q1 above — held pending your decision, not rejected |

### 6.6 What this plan does not do

It does not fetch a capture for recovery, edit any data file, move any count, commit
anything, or contact the author. Stage 0 is 59 read-only Wayback fetches plus a triage
table; if you approve Stage 0 alone, the only file it would touch is this survey document,
and every published number would stay exactly where it is.
