# Reading-first redesign — design spec

**Date:** 2026-09-28
**Status:** approved in conversation, pending written review
**Scope:** the visual system of `andalusian-archive` — typography, colour, measure,
and the presentation of every component across 335 pages and 6 layouts.

---

## 1. The problem

The site is a **long-form reading archive**: 68 machine transcripts, recovered
prose held verbatim, quoted passages cited to a line. It is currently presented
as a **dashboard**.

`_data`-driven evidence — the token block in `assets/css/style.css` is the
stock Tailwind palette, unaltered:

```
--color-primary: #2563eb      (Tailwind blue-600)
--color-accent:  #7c3aed      (Tailwind violet-600)
--radius-sm/md/lg/xl: 6/10/14/20px
--space-1..16: 4/8/12/16/20/24/32/40/48/64px
--shadow-sm/md/lg/xl: 4 steps
--max-width: 1200px
--font-sans: -apple-system, ... sans-serif     (no serif anywhere)
```

The consequence is not that the site is ugly. It is that it is **hard to read and
hard to navigate**: cool blue-grey surfaces, tinted card fills, pill badges,
drop shadows on things that are not raised, and a body measure of 860px. A
reader opening a 4,000-word transcript gets a dashboard.

## 2. The references, measured

Not from memory. Values below were read off the live sites with
`getComputedStyle`.

| | body | UI chrome | measure | background | text | accent |
|---|---|---|---|---|---|---|
| **SEP** | serif `16.5px / 1.5` | Source Sans Pro, **h1 weight 300** | `707px` | `#f3ede9` warm cream | `#1a1a1a` | black in-body links |
| **IEP** | Georgia `18px / 1.6` | — (all serif) | `700px` | `#ffffff` | `#444444` | `#0a5167` deep teal |
| **Goodreads** | **Merriweather** | Lato | `625px` | `#ffffff` | `#181818` / `#333` | `#00635d` deep teal |

Three findings that shaped the design:

1. **Two of the three chose the same accent.** Goodreads' is not the orange its
   old logo suggests; its nav, links and genre tags are all `rgb(0,99,93)` =
   `#00635d`, the same deep teal family as IEP's `#0a5167`. A single teal accent
   is what these sites converge on, so the design uses one.
2. **SEP inverts the surface relationship.** The page is warm cream and content
   sits directly on it. This site does the opposite: grey page, white cards.
3. **All three are quiet.** No drop shadows on non-raised things, no pill badges,
   one accent, hairline rules. The elegance the brief asks for is mostly
   *subtraction*.

## 3. Typography

### 3.1 Families

```css
--font-serif: 'Merriweather', 'Iowan Old Style', Charter, Georgia,
              'Times New Roman', serif;
--font-sans:  Lato, 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
              'Segoe UI', Roboto, sans-serif;
```

**No webfonts are loaded, deliberately.** The site loads no `@font-face` and no
third-party stylesheet today, and a preservation archive that claims to be
self-contained should not acquire a render-blocking request to a font CDN.
Merriweather is first in the stack so a reader who has it installed gets it;
Georgia — IEP's actual face — is the fallback and is on every platform in scope.
This is a real trade: without a webfont the design is at the mercy of the local
serif, and Georgia is the floor rather than the intention. Recorded as a known
limitation, not an oversight.

`font-weight: 300` is used for `h1`. It resolves to Segoe UI Light on Windows
and SF Pro Light on macOS, which is where SEP's light-weight headings come from.

### 3.2 Scale

| role | family | size / line-height | weight |
|---|---|---|---|
| body prose | serif | `1.125rem / 1.7` (18px) | 400 |
| lead / intro | serif | `1.25rem / 1.7` | 400 |
| `h1` | sans | `2.6rem / 1.15` | **300** |
| `h2` | sans | `1.6rem / 1.3` | 400 |
| `h3` | sans | `1.15rem / 1.4` | 600 |
| `h4` | sans | `1rem / 1.4` | 600 |
| eyebrow | sans | `0.75rem / 1.4` | 600, `letter-spacing: .08em`, uppercase |
| meta / caption | sans | `0.8125rem / 1.5` | 400, `--text-secondary` |
| code / mono | mono | `0.875em` | 400 |

Body prose goes to `1.1875rem` (19px) on `/papers/*` and `/transcripts/*`, which
are the two reading-heavy page kinds.

### 3.3 Measure

`--measure: 680px` — the midpoint of the three references (625 / 700 / 707).
Applied to `.page-content` and to the article/paper/transcript prose column.
`--max-width` stays `1200px` for the nav and footer only.

## 4. Colour

| token | light | dark | source |
|---|---|---|---|
| `--bg` | `#f4efe9` | `#1a1917` | SEP cream; dark is warm, **not** blue-black |
| `--surface` | `#fdfbf8` | `#232120` | raised things only |
| `--surface-sunken` | `#efe8de` | `#141312` | code blocks, table stripes |
| `--text` | `#1c1a17` | `#e9e5de` | SEP `#1a1a1a` / Goodreads `#181818` |
| `--text-secondary` | `#5c5750` | `#a8a29a` | Goodreads `#999` |
| `--text-tertiary` | `#8a8378` | `#7d766c` | Goodreads `#aaa` |
| `--rule` | `#ded5c7` | `#3b3833` | hairline dividers; 1.40:1 on light bg, see §7 |
| `--rule-strong` | `#cfc5b6` | `#4d4941` | table headers, input borders |
| `--accent` | `#0a5167` | `#7fb3c8` | **IEP** |
| `--accent-hover` | `#00635d` | `#9cc9d8` | **Goodreads** |
| `--accent-subtle` | `#e8eef1` | `#1e2a2f` | link underline tint, hover fills |
| `--success` | `#2f6b45` | `#7fbf95` | Goodreads green `#409d69`, darkened for AA |
| `--warning` | `#8a5a12` | `#d9a441` | |
| `--danger` | `#9b2c22` | `#e08b80` | Goodreads red `#e1534e`, darkened |

`--color-primary: #2563eb` and `--color-accent: #7c3aed` are **removed**. The
cool grey family (`#f5f6f8`, `#e2e4e8`, `#6b7280`, `#9ca3af`) is removed.

`--success` is darkened from Goodreads' `#409d69` because `#409d69` on `#fdfbf8`
is 2.6:1 and fails AA for text. It is used for text only at `--success` and for
the dot/rule in "found" states.

### 4.1 Dark mode

Kept, because a reading archive is used at night and dropping it is a
regression. Restyled to the same warm family: the hue is shifted off blue-black
(`#0f1117` today) to `#1a1917`, and every accent is lightened for contrast on a
dark ground. Light and dark are designed as one system with two values per
token, not as one theme plus an afterthought.

## 5. Components

The rule for every component below: **if it is not raised, it does not have a
shadow.** Currently 4 shadow steps are defined and used on cards, badges and
nav.

### 5.1 Cards → list rows

The primary form on every index page (`/articles/`, `/papers/`, `/videos/`,
`/transcripts/`, `/topics/`) becomes a **list row**: title, quiet metadata line,
hairline rule between rows. This is Goodreads' list pattern and SEP's contents
pattern. It is also what makes 68 videos scannable in a way a card grid is not.

Existing markup classes (`.card`, `.card-body`, `.card-actions`, `.card-title`)
are **kept** so the 335 generated pages need no markup changes; only their CSS
changes. A card becomes a row by losing its fill, its radius and its shadow, and
gaining a bottom rule. Index pages get `--measure` widened to `860px` because a
row of title + metadata needs more width than a paragraph does.

### 5.2 Badges and tags → small-caps text

`.badge`, `.tag`, `.tag-status` lose their background fill and border-radius and
become uppercase, letterspaced, `--text-secondary` at `0.75rem`. The status
distinction that `.tag-status` carries (found / wayback-only / lost) is carried
by **colour and a leading rule**, not by a filled pill — a filled pill is the
single loudest element on the current pages, and there are 72 of them.

### 5.3 Buttons → underlined text links

`.btn`, `.btn-primary`, `.btn-outline`, `.btn-sm` all become text links: accent
colour, `text-underline-offset: 3px`, underline on hover/focus. `.btn-primary`
gains nothing extra — there is one accent and it is used for links, not for
filled rectangles. Buttons that lead off-site keep `→`.

### 5.4 The three "elsewhere this appears" blocks

`.topic-backlinks`, `.recording-links`, `.secondary-backlinks` currently have a
tinted fill, a border, a radius and are grouped in the narrow-screen rule with
an inset accent bar. They become **rule-left indents**: a `2px` `--rule-strong`
left border, `--measure` padding, no fill, no radius, no shadow. They are
reference matter, not alerts, and they should read that way.

### 5.5 Prose furniture

`.info-block`, `.page-note`, `.alternate-note`, `.detail-section` lose their
fills and become indented blocks with a left rule in `--rule`. `blockquote` in
prose becomes a serif blockquote at `1.1875rem`, `--text-secondary`, with a
`2px` `--rule` left border and no fill.

Tables: header row gets a `--rule-strong` bottom border and uppercase
`0.75rem` `--text-secondary` text instead of a filled header. Stripes go, since
`--surface-sunken` stripes on a cream page read as noise; row separation is a
hairline.

### 5.6 Nav and footer

Nav: `--bg` background, `1px` `--rule` bottom border, **no shadow**, `--measure`
for its inner container at wide viewports (nav content stays centred, not
stretched to 1200px). Footer: 3 columns, `--text-secondary`, `0.8125rem`,
hairline rule above, no fills.

## 6. Files

**Rewritten:**
- `assets/css/style.css` — the `:root` token block, the dark block, and the
  component rules in §5. Target: shorter than the current 2,370 lines, because
  removing 4 shadow steps, ~10 pill/badge rules and the card-grid rules deletes
  more than the redesign adds.

**Edited (structure only, no content):**
- `_layouts/default.html`, `article.html`, `paper.html`, `video.html`,
  `transcript.html`, `post.html` — add a `.page-content` prose wrapper class
  where a measure needs applying; nav/footer markup gains no new chrome.
- `_includes/secondary_links.html`, `recording_links.html` — class names only,
  no behaviour change.

**Unchanged:** every `_data/` file, every generated page, `llms.txt`, `sitemap`
generation, SEO/JSON-LD tags, `README.md`, `NOTICE.md`, the no-contact copy, the
licence split, and the transcription disclaimer.

**Not changed:** all five test gates, except for the two added in §7.

## 7. New gates

Both live in `scripts/test_quotes.py`, both fail the build, both are pure and
offline.

1. **Contrast.** For every declared foreground/background token pair, compute
   the WCAG 2.1 contrast ratio. Text pairs (`--text`, `--text-secondary`,
   `--accent`, `--accent-hover`, `--success`, `--warning`, `--danger` on `--bg`,
   `--surface`, `--surface-sunken`, `--accent-subtle`) require **≥ 4.5:1** in
   **both** themes. Hairline rules (`--rule`, `--rule-strong`) require
   **≥ 1.4:1** on `--bg` — deliberately not the 3:1 of WCAG 1.4.11, because a
   rule between two list rows is a decorative divider and 3:1 would force it to
   be visually heavy, which is the opposite of the intent. The measured values
   are `--rule` 1.27 light / 1.51 dark and `--rule-strong` 1.49 light / 1.96
   dark, so `--rule` in the light theme is **darkened from `#e3dcd1` to
   `#ded5c7`** in §4 to clear the 1.4 floor. Verified: all 8 text tokens clear
   4.5:1 on all 4 backgrounds in both themes; the lowest is `--warning` on
   `--surface-sunken` at 4.86.

   This is what stops a future colour edit from shipping an unreadable pair —
   the reason the current dark theme needed a manual correction pass earlier.
2. **Measure.** Parse the built `.page-content` and assert the prose column is
   between `60ch` and `80ch` at the 1280px viewport. Guards §3.3 against a later
   `--max-width` edit quietly widening every paragraph again.

Both skip cleanly when `_site` is absent, because the CI gates run before
`jekyll build` — the mistake recorded in `25107c4`/`1c977ba`, where a
build-output check passed vacuously.

## 8. Testing

- Existing 5 suites must stay green: `test_search_sync`, `test_canonical_57`,
  `test_no_junk`, `test_quotes`, `test_transcripts` (local-only).
- Contrast and measure gates from §7.
- Manual verification with a real browser, both themes, at `375px`, `768px`,
  `1280px`, `1920px`:
  - home, a topic page, an article, a paper, a transcript, `/videos/`,
    `/sources/`, `/search/`, 404.
  - Confirm no horizontal overflow at 375px. The home page currently overflows
    by 96px because the class-less "Preservation Status" table is 440px wide and
    misses the `table.data-table` rule; that is fixed here, not deferred.
  - Keyboard focus visible on every interactive element.
- `bundle exec jekyll build` exit 0; zero tracked files with a BOM.

## 9. Consequences, stated

- **The site tour goes stale.** `docs/demo/site-tour.mp4` and `.gif` are recorded
  in the current dark theme. After this change its colours, type and layout are
  wrong. Re-record with `scripts/build_site_tour.py` and update
  `docs/demo/README.md`, `RELEASE-NOTES-v1.0.md` and the root `README.md` sizes,
  durations and sha256s — the same three files that were left inconsistent
  earlier. **This is in scope**, not deferred: shipping a redesign next to a
  video of the old design is the same class of error as the stale counts.
- **The palette is local-font dependent.** See §3.1. If the reader-facing result
  is not good enough with Georgia, the fix is to self-host Merriweather in
  `assets/fonts/` with `@font-face` and a `font-display: swap`, not to add a CDN.
- **Print is not addressed.** A reading archive is plausibly printed. Out of
  scope here; noted as a follow-up.
- Search, `/topics/`, and every count are untouched. This is presentation only.

## 10. Out of scope

Content, provenance, licensing, the recording-link layer, the third-party source
layer, outreach, and the two deferred CSS-consolidation items from earlier work.
