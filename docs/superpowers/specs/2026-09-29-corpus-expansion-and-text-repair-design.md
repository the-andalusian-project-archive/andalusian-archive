# Corpus expansion and text repair — design

**Date:** 2026-09-29
**Status:** approved

## Why this is four plans and not one

The request was to transcribe missing videos, repair formatting damage, and pull
more from the Wayback Machine. Those are three independent subsystems, and a
fourth was added: link labels. The writing-plans scope check requires each plan
to produce working, testable software on its own, so this design is four specs'
worth of scope delivered as four plans:

| Plan | Subsystem | Depends on |
|---|---|---|
| 1 | Fetch-damage cleaner | — |
| 2 | Transcripts for 13 absent works | 1 |
| 3 | Fresh Wayback survey | 1 |
| 4 | Display-title resolver | 2 |

Plan 3 is report-only. It recovers nothing, so it cannot contaminate anything.

## The line every repair has to hold

`CONTRIBUTING.md` says contributions are "corrections to the record, not changes to
the recovered material". That sentence is the whole design constraint, and it
splits cleanly in two:

- **Fetch damage** — something the *fetcher* did. An ad-injection script left in
  the body, WordPress chrome, a space destroyed when an inline tag was removed.
  The author never wrote these. Removing them restores his text.
- **His text** — his punctuation, his typos, his quote style. Stays, even where it
  reads as an error. `2017;` is not ours to fix.

`scripts/fetch_damage.py` is the single place that distinction is encoded, and
both the repair pass and the build gate import it, so they cannot disagree.

**"Don't make up anything" is a hard constraint, not a preference.** No invented
punctuation, no inferred text, no synthesised data. Every hit is triaged to
*repair* / *author's text, leave* / *false positive*, with the reason recorded.
Ambiguous cases are left unchanged and logged as "reviewed, unchanged" rather
than guessed at.

## What was measured, before anything was designed

| Collection | Files | ad/script residue | WP chrome | join candidates |
|---|---:|---:|---:|---:|
| `_posts` | 54 | 10 | 17 (45 hits) | 417 |
| `_articles` | 92 | 2 | 0 | 56 |
| `_papers` | 20 | 0 | 0 | 19 |
| `_transcripts` | 68 | 6 | 0 | 186 |
| `_videos` | 68 | 0 | — | — |

The user's premise was that papers and articles were broadly damaged. They are
not — papers are the cleanest collection. The damage is concentrated in `_posts`,
which is the WordPress blog pull, because that is the only lane whose fetcher
passes an ad-injection payload through into the body.

Join candidates are a **detector count, not a defect count**: the patterns
legitimately match camelCase, verse references and abbreviations, and each hit
needs a decision.

## Plan 1 — fetch-damage cleaner

`scripts/fetch_damage.py` holds a `Rule` table. Each rule carries a class, a
pattern, an optional automatic repair, and an `allow` pattern for legitimate
lookalikes it must not fire on — every rule has at least one, because a rule that
fires on the author's own text is worse than no rule.

Classes split by whether a repair can be mechanical:

- `residue`, `chrome` — unambiguous fetch damage. A gate **fails** on these.
- `join`, `space`, `encoding` — judgement. **Reported for triage, never
  auto-rewritten**, never gate-failing.

The repair lands in `fetch_blog_content.py::clean_content_element` and
`scrub_ad_junk_lines`, not in the corpus files. Fixing the files alone is
pointless: the next recovery run re-contaminates them.

Only the affected files are re-derived, with verbatim before/after retained in
`docs/recovery-log/`.

**The exhaustive triage is the honest cost centre.** A per-hit decision across
678 join candidates and every other class resists pattern-matching. That is the
price of "don't make up anything", and it is stated up front rather than
discovered late.

## Plan 2 — transcripts for 13 absent works

A playlist of 88 videos by a third-party re-upload channel was found and never
incorporated. Against the 68 catalogued videos, three works are verified absent
by grep over the whole repository:

- **The Arena — Challenge Islam — Defend your Beliefs**, 11 episodes
- **"Yes, I'm leaving"** (`kRCzZW3rg4U`), his last video
- **Episode 93 — The Akh-Right, LGBTQ & Liberalism** (`M3nB154Mkuk`)

All 13 have a caption track: 10 human-authored subtitles, 3 automatic. **No media
download is required for any of them**, which is what makes this consistent with
YouTube's terms of service — the objection that stopped the obvious approach.

Transcript provenance follows the existing practice at `NOTICE.md:234`
(`cap-*.en-orig.vtt` verbatim caption captures). Raw caption files containing
personal identifiers are **withheld, not edited**: preserved unaltered in the
private tree, dropped from the published repository, because editing evidence
destroys what makes it evidence.

The 13 are counted, so the published total moves **207 → 220**. That is a wide
blast radius: `content_index.json`, the search index, JSON-LD, every document
that prints the number, and the site-tour caption. It moves atomically or
`test_canonical_57.py` breaks.

## Plan 3 — fresh Wayback survey

The known gap is already closed. `README.md:203` records the 22-permalink lane as
"18 recovered, 0 not found". This is therefore a **fresh survey, not a reopened
lane** — CDX enumeration across known URL patterns that reports what is new and
recovers nothing. New lanes are built from the survey's findings, each a
separate reviewable task.

## Plan 4 — display-title resolver

A single resolver supplies every visible link label, so labels cannot drift apart
again. It fixes, on the current build:

- **501** `cite-ref` links showing `_posts/2015-08-16-….md`
- **179** links whose text is a PDF filename
- **149** whose text is a bare opaque id (`W2166612418`, `W2279455005`)
- **53** other slugs
- video titles of the form `"33 - (Reupload - Read Desc) Hard Questions…"`

It runs **after** Plan 2, so the 13 new works are labelled correctly from birth
instead of adding 13×N more bad labels to fix afterwards.

`check_link_labels` fails the build when any visible link text matches a slug, a
path or a bare id — the detector promoted to CI.

## Verification

Every plan leaves the five suites green and `_site` building. Specifically:

- `test_quotes.py` — all 501 quotations verbatim at their cited lines
- `test_canonical_57.py` — the content total (207, then 220)
- `check_fetch_damage`, `check_link_labels`, `check_captions` — new
- the 152-combination browser sweep — unchanged at 0 errors, 0 overflow

## Global constraints

1. Never alter the author's prose; only remove damage the fetch introduced.
2. No invented punctuation, no inferred text, no synthesised data.
3. Caption tracks only for transcripts. No media download.
4. Caption files with personal identifiers are withheld, not edited.
5. Windows: `python -B`, no `Set-Content -Encoding UTF8`, no BOM.
6. Push only `git push origin public-main:main`.
