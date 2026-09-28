# Reading-first redesign — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle `andalusian-archive` from a Tailwind dashboard into a
reading-first archive with SEP's red accent, serif body at a 680px measure, and
one warm surface.

**Architecture:** One rewritten `assets/css/style.css` (tokens + dark block +
component rules) plus class-only edits to 6 layouts and 2 includes. No markup
renames, so the 335 generated pages need no regeneration and no `_data/` file
changes. Two new pure gates in `scripts/test_quotes.py` lock the palette and the
measure so neither can regress.

**Tech Stack:** Jekyll 4, Liquid, plain CSS custom properties, Python 3 stdlib
(no new dependencies — the site loads no webfonts and must keep loading none).

**Spec:** `docs/superpowers/specs/2026-09-28-reading-first-redesign-design.md`

## Global Constraints

- **Accent is SEP's red**: `--accent` `#8c1515` light / `#e08a8a` dark. Never
  `#0a5167` or `#00635d` (IEP/Goodreads teal) — those were measured but rejected.
- **No webfonts.** `--font-serif` starts `'Merriweather'` (used only if locally
  installed) and falls back through `'Iowan Old Style', Charter, Georgia` to
  `serif`. No `@font-face`, no `@import`, no CDN request. The site loads none
  today and must keep loading none.
- **Tracked files carry no UTF-8 BOM.** Check after every write.
- **`--color-primary: #2563eb` and `--color-accent: #7c3aed` are removed**, not
  aliased. Grep must return zero hits for `#2563eb` and `#7c3aed` in
  `assets/css/style.css` at the end.
- **A shadow only on a raised thing.** Overlays only.
- **`--measure: 680px`** for prose; `860px` for index list rows; nav/footer
  content stays at `--max-width` `1200px`.
- Every existing gate must stay green: `sync_search_data.py`,
  `test_search_sync.py`, `test_canonical_57.py`, `test_no_junk.py`,
  `test_quotes.py`, and `test_transcripts.py` (local-only).
- Run `python -B` with `PYTHONDONTWRITEBYTECODE=1` so no `__pycache__` lands in
  the repo.
- Build is `bundle exec jekyll build --quiet`; exit 0 required.
- PowerShell 5.1: never `Set-Content -Encoding UTF8` on a tracked file (adds a
  BOM, which makes Jekyll skip front matter). Use the `edit` tool or byte-level
  Python.

---

### Task 1: The design tokens and both themes

**Files:**
- Modify: `assets/css/style.css:1-100` (the `:root` block and the
  `prefers-color-scheme` block)
- Test: `scripts/test_quotes.py` (new `check_palette()` gate)

**Interfaces:**
- Consumes: nothing.
- Produces: the token names later tasks read. `check_palette()` — no arguments,
  returns `list[str]` of failures, called from `check()` alongside
  `check_pages()` and `check_secondary_sources()`.

- [ ] **Step 1: Read the current token block so the replacement is exact**

Read `assets/css/style.css` lines 1-100. Confirm the current values are the
stock Tailwind set (`--color-primary: #2563eb`, `--color-accent: #7c3aed`,
`--font-sans` with no serif, `--max-width: 1200px`) before replacing them.

- [ ] **Step 2: Write the failing gate**

Append to `scripts/test_quotes.py`:

```python
# The token pairs the redesign declares. Kept as literal data in the gate, not
# parsed out of the stylesheet, so a careless token edit fails the build instead
# of quietly lowering the contrast floor.
PALETTE_TEXT_PAIRS = [
    ("--text", "--bg"), ("--text", "--surface"),
    ("--text", "--surface-sunken"), ("--text", "--accent-subtle"),
    ("--text-secondary", "--bg"), ("--text-secondary", "--surface"),
    ("--text-secondary", "--surface-sunken"),
    ("--text-secondary", "--accent-subtle"),
    ("--accent", "--bg"), ("--accent", "--surface"),
    ("--accent", "--surface-sunken"), ("--accent", "--accent-subtle"),
    ("--accent-hover", "--bg"), ("--accent-hover", "--surface"),
    ("--success", "--bg"), ("--success", "--surface"),
    ("--success", "--surface-sunken"),
    ("--warning", "--bg"), ("--warning", "--surface"),
    ("--warning", "--surface-sunken"),
    ("--danger", "--bg"), ("--danger", "--surface"),
    ("--danger", "--surface-sunken"),
]
# Hairline rules are decorative dividers, so they take a visibility floor rather
# than the 3:1 of WCAG 1.4.11. 3:1 would force a divider to be visually heavy,
# which is the opposite of the design.
PALETTE_RULE_PAIRS = [("--rule", "--bg"), ("--rule-strong", "--bg")]
TEXT_MIN = 4.5
RULE_MIN = 1.4


def _srgb_lum(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        ch.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _contrast(a: str, b: str) -> float:
    la, lb = _srgb_lum(a), _srgb_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def check_palette() -> list[str]:
    """Every declared token pair must clear its floor, in BOTH themes."""
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    failures: list[str] = []

    def read_vars(block: str) -> dict[str, str]:
        out: dict[str, str] = {}
        for m in re.finditer(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", block):
            out[m.group(1)] = m.group(2)
        return out

    root = css.split(":root", 1)[-1]
    root = root[: root.find("}") + 1]
    light = read_vars(root)

    dm = re.search(r"prefers-color-scheme:\s*dark\s*\{(.*?)\n\}", css, re.S)
    if not dm:
        return ["style.css: no prefers-color-scheme dark block found"]
    dark = read_vars(dm.group(1))
    for k, v in light.items():
        dark.setdefault(k, v)

    required = {n for n, _ in PALETTE_TEXT_PAIRS} | {n for n, _ in PALETTE_RULE_PAIRS}
    missing = sorted(required - set(light) - set(dark))
    if missing:
        failures.append(f"style.css: tokens not declared: {missing}")

    for theme_name, T in (("light", light), ("dark", dark)):
        for fg, bgn in PALETTE_TEXT_PAIRS:
            if fg not in T or bgn not in T:
                continue
            r = _contrast(T[fg], T[bgn])
            if r < TEXT_MIN:
                failures.append(
                    f"contrast {theme_name}: {fg} on {bgn} = {r:.2f} "
                    f"(< {TEXT_MIN})")
        for fg, bgn in PALETTE_RULE_PAIRS:
            if fg not in T or bgn not in T:
                continue
            r = _contrast(T[fg], T[bgn])
            if r < RULE_MIN:
                failures.append(
                    f"contrast {theme_name}: {fg} on {bgn} = {r:.2f} "
                    f"(< {RULE_MIN})")

    # The accent must actually be SEP's red, so a later edit back to the teal
    # the measurement surfaced first is caught.
    for theme_name, T, want in (("light", light, "#8c1515"),
                                ("dark", dark, "#e08a8a")):
        got = (T.get("--accent") or "").lower()
        if got and got != want:
            failures.append(
                f"style.css {theme_name}: --accent is {got}, expected {want} "
                f"(SEP's red)")

    print(f"palette pairs checked: {len(PALETTE_TEXT_PAIRS)} text, "
          f"{len(PALETTE_RULE_PAIRS)} rule, in 2 themes")
    return failures
```

Then add `failures.extend(check_palette())` to `check()`, immediately after the
existing `failures.extend(check_pages(total_queries))` line.

- [ ] **Step 3: Run the gate and watch it fail**

Run: `python -B scripts/test_quotes.py`
Expected: FAIL listing every old Tailwind pair — `--text` on `--bg` will pass but
`--accent` on `--bg` will be reported as `#2563eb`, and the `--accent is ...
expected #8c1515` line will fire.

- [ ] **Step 4: Replace the `:root` token block**

Replace the whole `:root { ... }` block with:

```css
:root {
  /* --- surfaces: SEP's warm paper, content sitting directly on it --------- */
  --bg: #f4efe9;
  --surface: #fdfbf8;
  --surface-sunken: #efe8de;

  /* --- ink ------------------------------------------------------------- */
  --text: #1c1a17;
  --text-secondary: #5c5750;
  --text-tertiary: #8a8378;

  /* --- rules: hairlines, not boxes -------------------------------------- */
  --rule: #ded5c7;
  --rule-strong: #cfc5b6;

  /* --- one accent: SEP's red, measured rgb(140,21,21) -------------------- */
  --accent: #8c1515;
  --accent-hover: #6e1010;
  --accent-subtle: #f2e3e1;

  /* --- status ----------------------------------------------------------- */
  --success: #2f6b45;
  --success-subtle: #eaf1ec;
  --warning: #8a5a12;
  --warning-subtle: #f6efe0;
  --danger: #9b2c22;
  --danger-subtle: #f6e9e7;

  /* --- spacing ---------------------------------------------------------- */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* --- type ------------------------------------------------------------- */
  /* Merriweather first because Goodreads uses it and it is drawn for screens,
     but it is only used when locally installed: the site loads no webfont and
     acquires no third-party request. Georgia is the floor and is universal. */
  --font-serif: 'Merriweather', 'Iowan Old Style', Charter, Georgia,
                'Times New Roman', serif;
  --font-sans: Lato, 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
               'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', SFMono-Regular, ui-monospace, Menlo, monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.8125rem;
  --text-base: 1rem;
  --text-body: 1.125rem;   /* 18px serif prose */
  --text-lead: 1.25rem;
  --text-lg: 1.15rem;
  --text-xl: 1.6rem;      /* h2 */
  --text-2xl: 2rem;
  --text-3xl: 2.6rem;     /* h1 */

  --line-height: 1.7;
  --measure: 680px;
  --measure-wide: 860px;
  --max-width: 1200px;
  --nav-height: 60px;

  --radius-sm: 3px;
  --radius-md: 4px;
  --radius-lg: 6px;
  --radius-full: 9999px;

  /* Shadows are for raised things only: overlays and the sticky nav. */
  --shadow-overlay: 0 8px 32px rgba(28, 26, 23, 0.14);
  --shadow-sticky: 0 1px 0 var(--rule);

  --transition-fast: 120ms ease;
  --transition-base: 180ms ease;
}
```

- [ ] **Step 5: Replace the dark block**

Find the `@media (prefers-color-scheme: dark)` block and replace its `:root`
(or `html`) body with exactly these values, overriding only what changes:

```css
    :root {
      --bg: #1a1917;
      --surface: #232120;
      --surface-sunken: #141312;
      --text: #e9e5de;
      --text-secondary: #a8a29a;
      --text-tertiary: #7d766c;
      --rule: #3b3833;
      --rule-strong: #4d4941;
      --accent: #e08a8a;
      --accent-hover: #eda3a3;
      --accent-subtle: #2a1d1d;
      --success: #7fbf95;
      --success-subtle: #1c2a20;
      --warning: #d9a441;
      --warning-subtle: #2a2318;
      --danger: #e08b80;
      --danger-subtle: #2b1c1a;
      --shadow-overlay: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
```

- [ ] **Step 6: Run the gate and the suite**

Run: `python -B scripts/test_quotes.py`
Expected: `palette pairs checked: 23 text, 2 rule, in 2 themes` and
`TEST_PASS`.

Run: `bundle exec jekyll build --quiet`
Expected: exit 0. The site is now unstyled-looking but structurally intact.

- [ ] **Step 7: Commit**

```bash
git add assets/css/style.css scripts/test_quotes.py
git commit -m "style: SEP-red tokens, warm paper surfaces, serif stack

Replaces the stock Tailwind palette with the values measured off SEP, IEP and
Goodreads. The accent is SEP's red, rgb(140,21,21) = #8c1515, which is what its
section headings and sidebar links use; the teal that IEP and Goodreads share
was measured and rejected.

Adds check_palette(), which computes the WCAG ratio for 23 text pairs and 2 rule
pairs in both themes and fails the build below the floor, so a later colour edit
cannot quietly ship an unreadable pair. It also pins --accent to SEP's red
specifically, because the first measurement to surface was the teal."
```

---

### Task 2: Typography and the measure

**Files:**
- Modify: `assets/css/style.css` (the `body`, `h1`-`h4`, `.page-content`,
  `.lead`, `blockquote` rules)
- Modify: `_layouts/paper.html`, `_layouts/transcript.html` (add the
  `.prose-reading` class to the body wrapper)
- Test: `scripts/test_quotes.py` (new `check_measure()` gate)

**Interfaces:**
- Consumes: `--font-serif`, `--measure`, `--text-body` from Task 1.
- Produces: `check_measure() -> list[str]`. Adds the class `prose-reading`.

- [ ] **Step 1: Write the failing measure gate**

Append to `scripts/test_quotes.py`:

```python
# 680px at an 18px serif lands near 66 characters, the midpoint of the three
# references (Goodreads 625, IEP 700, SEP 707). Assert the range rather than
# the pixel value so a later --max-width edit cannot quietly re-widen every
# paragraph, which is what an 860px measure did before this redesign.
MEASURE_MIN_CH = 60
MEASURE_MAX_CH = 80


def check_measure() -> list[str]:
    """The prose column must stay at a readable line length.

    Skipped when there is no build, because the CI gates run before
    `jekyll build`. This is a local gate, deliberately: the static half of the
    measurement is that `--measure` exists and is used, and that is checked
    unconditionally just below.
    """
    failures: list[str] = []
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")

    if "--measure:" not in css:
        return ["style.css: --measure is not declared"]
    m = re.search(r"--measure:\s*(\d+)px", css)
    if m and not (620 <= int(m.group(1)) <= 720):
        failures.append(
            f"style.css: --measure is {m.group(1)}px, outside the 620-720px band "
            f"the references use")

    built = ROOT / "_site"
    if not built.is_dir():
        print("measure: token checked, render skipped (no _site)")
        return failures

    # Approximate the character count the way a browser would: the measure in px
    # divided by the advance width of the body serif at 18px. Georgia's average
    # advance is ~0.5em, so 18px gives ~9px per character.
    measure_px = int(m.group(1)) if m else 680
    approx_ch = measure_px / 9.0
    if not (MEASURE_MIN_CH <= approx_ch <= MEASURE_MAX_CH):
        failures.append(
            f"measure: {measure_px}px at 18px serif is about {approx_ch:.0f}ch, "
            f"outside {MEASURE_MIN_CH}-{MEASURE_MAX_CH}ch")

    print(f"measure: {measure_px}px, about {approx_ch:.0f}ch "
          f"(target {MEASURE_MIN_CH}-{MEASURE_MAX_CH}ch)")
    return failures
```

Add `failures.extend(check_measure())` to `check()`.

- [ ] **Step 2: Run it and watch it fail**

Run: `python -B scripts/test_quotes.py`
Expected: FAIL — `style.css: --measure is not declared`.

- [ ] **Step 3: Set the base type rules**

In `assets/css/style.css`, replace the `body` rule and add after it:

```css
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--line-height);
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* Prose is serif. This is a reading archive: 68 machine transcripts and a body
   of recovered prose held verbatim. */
.page-content,
.prose-reading {
  font-family: var(--font-serif);
  font-size: var(--text-body);
  line-height: var(--line-height);
  color: var(--text);
}

.page-content { max-width: var(--measure); }
.prose-reading { max-width: var(--measure); }

/* Index pages hold a row of title + metadata, which needs more width than a
   paragraph does. */
.page-content-wide { max-width: var(--measure-wide); }

.page-content p { margin: 0 0 1.15em; }

.page-content .lead,
p.lead {
  font-size: var(--text-lead);
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 1.6em;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-sans);
  color: var(--text);
  text-wrap: balance;
}

/* Weight 300 is where SEP's headings come from; it resolves to Segoe UI Light
   on Windows and SF Pro Light on macOS. */
h1 {
  font-size: var(--text-3xl);
  font-weight: 300;
  line-height: 1.15;
  letter-spacing: -0.015em;
  margin: 0 0 0.5em;
}

h2 {
  font-size: var(--text-xl);
  font-weight: 400;
  line-height: 1.3;
  letter-spacing: -0.01em;
  margin: 2.2rem 0 0.7rem;
}

h3 {
  font-size: var(--text-lg);
  font-weight: 600;
  line-height: 1.4;
  margin: 1.8rem 0 0.6rem;
}

h4 {
  font-size: var(--text-base);
  font-weight: 600;
  line-height: 1.4;
  margin: 1.4rem 0 0.5rem;
}

/* The eyebrow is the small-caps label the references use above a section. */
.eyebrow,
.page-content h2 + .meta {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.page-content blockquote {
  font-family: var(--font-serif);
  font-size: 1.1875rem;
  line-height: 1.65;
  color: var(--text-secondary);
  border-left: 2px solid var(--rule-strong);
  padding-left: 1.25rem;
  margin: 1.6rem 0;
  background: none;
}

.page-content code,
.page-content pre {
  font-family: var(--font-mono);
  font-size: 0.875em;
}

.page-content pre {
  background: var(--surface-sunken);
  border: 1px solid var(--rule);
  border-radius: var(--radius-md);
  padding: 1rem 1.15rem;
  overflow-x: auto;
}

.page-content a {
  color: var(--accent);
  text-decoration: none;
  text-underline-offset: 3px;
}

.page-content a:hover,
.page-content a:focus-visible {
  text-decoration: underline;
  color: var(--accent-hover);
}
```

- [ ] **Step 4: Give the reading-heavy layouts the class**

In `_layouts/paper.html` and `_layouts/transcript.html`, find the element that
carries the body prose and add `prose-reading` to its `class` attribute. Do not
change any other attribute. If the class attribute does not exist, add
`class="prose-reading"` to the block-level wrapper that directly contains the
article body.

- [ ] **Step 5: Run the gates**

Run: `python -B scripts/test_quotes.py`
Expected: `measure: 680px, about 76ch (target 60-80ch)` and `TEST_PASS`.

Note 76ch is inside the range but near the top. If a future serif has a narrower
advance this is fine; the band exists to catch a return to 860px+, not to
micro-tune.

Run: `bundle exec jekyll build --quiet`
Expected: exit 0.

- [ ] **Step 6: Commit**

```bash
git add assets/css/style.css _layouts/paper.html _layouts/transcript.html scripts/test_quotes.py
git commit -m "style: serif prose at a 680px measure, weight-300 headings

The site is a reading archive, so body text is serif at 18px/1.7 and headings
switch to the sans at weight 300, which is where SEP's headings come from.

--measure is 680px, the midpoint of the three references (Goodreads 625, IEP
700, SEP 707). Index pages get --measure-wide because a row of title plus
metadata needs more width than a paragraph.

Adds check_measure(), which fails the build if --measure leaves the 620-720px
band or implies a line length outside 60-80ch."
```

---

### Task 3: Links, buttons, badges, tags

**Files:**
- Modify: `assets/css/style.css` (`.btn*`, `.badge`, `.tag`, `.tag-status`,
  global `a`)

**Interfaces:**
- Consumes: `--accent`, `--rule`, `--text-secondary` from Task 1.
- Produces: no new symbols. The existing class names are kept, so no page needs
  regenerating.

- [ ] **Step 1: Replace the interactive-element rules**

Delete the existing `.btn`, `.btn-primary`, `.btn-outline`, `.btn-sm`,
`.badge`, `.tag`, `.tag-status` rules and replace with:

```css
/* --- links --------------------------------------------------------------- */

a {
  color: var(--accent);
  text-decoration: none;
  text-underline-offset: 3px;
}

a:hover,
a:focus-visible {
  color: var(--accent-hover);
  text-decoration: underline;
}

/* --- buttons are links ---------------------------------------------------
   A filled rectangle per action is the loudest thing on a reading page, and
   there are 72 works. Every button on the site becomes an underlined text
   link, and the one accent is spent on the link colour rather than on a fill. */

.btn,
.btn-primary,
.btn-outline,
.btn-sm,
.btn-secondary {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--accent);
  background: none;
  border: 0;
  border-radius: 0;
  padding: 0;
  margin: 0 0.35rem 0.35rem 0;
  text-decoration: none;
  text-underline-offset: 3px;
  cursor: pointer;
}

.btn:hover,
.btn-primary:hover,
.btn-outline:hover,
.btn-sm:hover,
.btn-secondary:hover,
.btn:focus-visible,
.btn-primary:focus-visible,
.btn-outline:focus-visible,
.btn-sm:focus-visible {
  color: var(--accent-hover);
  text-decoration: underline;
  background: none;
}

.btn-primary {
  font-weight: 600;
  color: var(--accent);
}

/* --- badges and tags are text --------------------------------------------
   A filled pill is the single loudest element on the current index pages and
   there is one per item. The status that .tag-status carries is kept, but it is
   carried by colour and a leading rule instead of a fill. */

.badge,
.tag,
.tag-status {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-secondary);
  background: none;
  border: 0;
  border-radius: 0;
  padding: 0;
  margin: 0 0.4rem 0.3rem 0;
  white-space: nowrap;
}

.tag a,
.badge a {
  color: inherit;
}

/* Status is colour plus a rule, never a fill. The three states are the
   catalogue's found / wayback-only / lost verdicts. */
.tag-status::before {
  content: "";
  display: inline-block;
  width: 2px;
  height: 0.85em;
  margin-right: 0.4em;
  vertical-align: -0.08em;
  background: var(--text-tertiary);
}

.tag-status-found::before,
.status-found::before { background: var(--success); }
.tag-status-wayback::before,
.status-wayback::before { background: var(--warning); }
.tag-status-lost::before,
.status-lost::before { background: var(--danger); }

/* --- focus -------------------------------------------------------------- */

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```

- [ ] **Step 2: Build and check nothing lost its affordance**

Run: `bundle exec jekyll build --quiet`
Expected: exit 0. Then in a browser, open `/articles/` and confirm every title
link is visible, the buttons read as links, and the status tags are legible
without a fill.

- [ ] **Step 3: Commit**

```bash
git add assets/css/style.css
git commit -m "style: buttons become links, badges become small-caps text

A filled pill is the loudest element on an index page and there is one per
item, 72 of them on /articles/. Buttons lose their fill and border and become
underlined text links, so the single accent is spent on link colour rather than
on rectangles. The status that .tag-status carried is kept, carried by colour
and a 2px leading rule instead of a background."
```

---

### Task 4: Cards become list rows, and the three backlink blocks

**Files:**
- Modify: `assets/css/style.css` (`.card*`, `.topic-backlinks`,
  `.recording-links`, `.secondary-backlinks`, `.info-block`, `.page-note`,
  `.alternate-note`, `.detail-section`)

**Interfaces:**
- Consumes: `--measure`, `--rule`, `--rule-strong`, `--accent` from Tasks 1-2.
- Produces: no new symbols.

- [ ] **Step 1: Turn cards into rows**

Delete the existing `.card`, `.card-header`, `.card-body`, `.card-title`,
`.card-meta`, `.card-actions`, `.card-grid` rules and replace with:

```css
/* --- list rows, not card grids -------------------------------------------
   Goodreads' list and SEP's contents are both a title, a quiet metadata line
   and a hairline between rows. That is also what makes 68 videos scannable in
   a way a card grid is not. A card becomes a row by losing its fill, its radius
   and its shadow, and gaining a bottom rule. The class names are unchanged, so
   the 335 generated pages need no regeneration. */

.card-grid {
  display: block;
  margin: 0;
  padding: 0;
}

.card {
  background: none;
  border: 0;
  border-bottom: 1px solid var(--rule);
  border-radius: 0;
  box-shadow: none;
  padding: 1.1rem 0;
  margin: 0;
  max-width: var(--measure-wide);
}

.card:last-child { border-bottom: 0; }

.card-header,
.card-body,
.card-actions {
  background: none;
  border: 0;
  padding: 0;
  margin: 0;
}

.card-title,
.card h3,
.card h2 {
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  font-weight: 600;
  line-height: 1.4;
  margin: 0 0 0.3rem;
  letter-spacing: 0;
}

.card-title a,
.card a { color: var(--accent); }

.card p,
.card-meta,
.card .meta {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0 0 0.35rem;
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem 0.9rem;
  margin-top: 0.45rem;
}

.card-actions .btn { margin: 0; }
```

- [ ] **Step 2: Turn the three backlink blocks into rule-left indents**

Replace the `.topic-backlinks`, `.recording-links` and `.secondary-backlinks`
rules with one shared block, keeping each class in the selector list so the
existing markup keeps working:

```css
/* --- "elsewhere this appears" blocks --------------------------------------
   These are reference matter, not alerts. They currently carry a tinted fill,
   a border and a radius, which makes them the second-loudest thing on an item
   page after the pill badges. They become rule-left indents. */

.topic-backlinks,
.recording-links,
.secondary-backlinks {
  margin: 2rem 0;
  padding: 0.1rem 0 0.1rem 1.25rem;
  background: none;
  border: 0;
  border-left: 2px solid var(--rule-strong);
  border-radius: 0;
  box-shadow: none;
  max-width: var(--measure);
}

.topic-backlinks h2,
.recording-links h2,
.secondary-backlinks h2 {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin: 0 0 0.5rem;
}

.topic-backlinks p.meta,
.recording-links p.meta,
.secondary-backlinks p.meta {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0 0 0.7rem;
}

.topic-backlinks ul,
.recording-links ul,
.secondary-backlinks ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.topic-backlinks li,
.recording-links li,
.secondary-backlinks li {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: 1.55;
  color: var(--text-secondary);
  margin: 0 0 0.4rem;
}

.topic-backlinks li:last-child,
.recording-links li:last-child,
.secondary-backlinks li:last-child { margin-bottom: 0; }

.topic-backlinks li a,
.recording-links li a,
.secondary-backlinks li a {
  color: var(--accent);
  font-weight: 600;
}

.topic-backlinks .topic-q,
.recording-links .rel-how,
.secondary-backlinks .rel-how,
.secondary-backlinks .src-type {
  color: var(--text-tertiary);
  font-weight: 400;
  font-size: var(--text-xs);
  letter-spacing: 0.02em;
}

.secondary-backlinks .rel-none { font-style: italic; }

.recording-links .rec-direct {
  display: inline-block;
  margin-left: 0.5rem;
  font-size: var(--text-xs);
  color: var(--accent);
  border-bottom: 1px solid var(--rule-strong);
  padding-bottom: 1px;
}

.recording-links .rec-dl { color: var(--text-tertiary); font-weight: 400; }
```

- [ ] **Step 3: Flatten the prose furniture**

Replace `.info-block`, `.page-note`, `.prose-note`, `.alternate-note` and
`.detail-section`:

```css
.info-block,
.page-note,
.prose-note,
.alternate-note,
.detail-section {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: 1.6;
  color: var(--text-secondary);
  background: none;
  border: 0;
  border-left: 2px solid var(--rule);
  border-radius: 0;
  box-shadow: none;
  padding: 0.15rem 0 0.15rem 1.15rem;
  margin: 1.5rem 0;
  max-width: var(--measure);
}

.info-block strong,
.page-note strong { color: var(--text); font-weight: 600; }
```

- [ ] **Step 4: Build and verify**

Run: `bundle exec jekyll build --quiet` → exit 0.
Run: `python -B scripts/test_quotes.py` → `TEST_PASS`.

Open `/articles/`, `/topics/`, `/papers/the-qur-an-and-science-a-forced-marriage/`
and `/sources/`. Confirm rows read as a list, and that the three backlink blocks
read as indented references rather than boxes.

- [ ] **Step 5: Commit**

```bash
git add assets/css/style.css
git commit -m "style: cards become list rows, backlink blocks become indents

A card keeps its class names and loses its fill, radius and shadow, gaining a
bottom rule. That is the Goodreads list pattern and the SEP contents pattern,
and it is what makes 68 videos scannable rather than tiled.

The three 'elsewhere this appears' blocks lose their tinted fill and become
rule-left indents: they are reference matter, not alerts."
```

---

### Task 5: Tables, nav, footer, hero, timeline

**Files:**
- Modify: `assets/css/style.css` (`.data-table`, `.site-nav`, `.site-footer`,
  `.hero`, `.timeline*`, `.stat*`, `.quick-link`, `.page-header`)

**Interfaces:**
- Consumes: every token from Task 1.
- Produces: no new symbols.

- [ ] **Step 1: Tables**

Replace the table rules:

```css
.data-table,
.page-content table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  margin: 1.5rem 0;
  background: none;
}

.data-table th,
.page-content table th {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-secondary);
  text-align: left;
  padding: 0.5rem 0.75rem 0.5rem 0;
  border-bottom: 1px solid var(--rule-strong);
  background: none;
}

.data-table td,
.page-content table td {
  padding: 0.6rem 0.75rem 0.6rem 0;
  border-bottom: 1px solid var(--rule);
  color: var(--text);
  vertical-align: top;
}

.data-table tbody tr:hover td { background: var(--accent-subtle); }

/* Stripes go: a sunken fill on a warm cream page reads as noise. Row separation
   is a hairline. */
.data-table tbody tr:nth-child(even) td,
.page-content table tbody tr:nth-child(even) td {
  background: none;
}
```

Note this selector is `.page-content table`, not only `.data-table`: the home
page's "Preservation Status" table is class-less and is what overflows by 96px
at a 375px viewport today.

- [ ] **Step 2: Nav**

Replace the `.site-nav` rules:

```css
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg);
  border-bottom: 1px solid var(--rule);
  box-shadow: none;
}

.site-nav .nav-inner,
.site-nav > .container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--space-6);
  min-height: var(--nav-height);
  display: flex;
  align-items: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.site-nav a,
.site-nav .nav-link {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.35rem 0;
  border-bottom: 2px solid transparent;
}

.site-nav a:hover,
.site-nav .nav-link:hover {
  color: var(--accent);
  text-decoration: none;
  border-bottom-color: var(--accent);
}

.site-nav a.active,
.site-nav .nav-link.active {
  color: var(--text);
  font-weight: 600;
  border-bottom-color: var(--accent);
}
```

- [ ] **Step 3: Footer**

Replace the `.site-footer` rules:

```css
.site-footer {
  margin-top: 4rem;
  padding: 2.5rem 0 3rem;
  background: none;
  border-top: 1px solid var(--rule);
  color: var(--text-secondary);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
}

.site-footer .container,
.site-footer > .footer-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.site-footer h4 {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin: 0 0 0.7rem;
}

.site-footer a {
  color: var(--text-secondary);
  text-decoration: none;
}

.site-footer a:hover { color: var(--accent); text-decoration: underline; }

.site-footer ul { list-style: none; padding: 0; margin: 0; }
.site-footer li { margin: 0 0 0.3rem; }
.site-footer .footer-flag { color: var(--text-tertiary); }
```

- [ ] **Step 4: Hero, page header, timeline, stats, quick links**

Replace those rules:

```css
.hero,
.page-header {
  max-width: var(--measure);
  margin: 0 0 2.5rem;
  padding: 0;
  background: none;
  border: 0;
  box-shadow: none;
}

.hero h1,
.page-header h1 { margin-bottom: 0.4em; }

.hero p,
.page-header .lead,
.page-header p {
  font-family: var(--font-serif);
  font-size: var(--text-lead);
  line-height: 1.6;
  color: var(--text-secondary);
}

/* --- timeline ------------------------------------------------------------ */

.timeline { list-style: none; padding: 0; margin: 2rem 0; max-width: var(--measure); }

.timeline-item {
  position: relative;
  padding: 0 0 1.6rem 1.4rem;
  border-left: 1px solid var(--rule);
  margin: 0;
}

.timeline-item:last-child { border-left-color: transparent; padding-bottom: 0; }

.timeline-date {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  display: block;
  margin-bottom: 0.2rem;
}

.timeline-title {
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  font-weight: 600;
  line-height: 1.4;
  margin: 0 0 0.25rem;
}

.timeline-item p {
  font-family: var(--font-serif);
  font-size: var(--text-sm);
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
}

/* --- stats --------------------------------------------------------------- */

.stat-row,
.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1.75rem 2.5rem;
  margin: 1.75rem 0;
  padding: 0;
  background: none;
  border: 0;
  box-shadow: none;
}

.stat {
  background: none;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  padding: 0;
  margin: 0;
  min-width: 0;
}

.stat-value,
.stat .value {
  display: block;
  font-family: var(--font-sans);
  font-size: 1.75rem;
  font-weight: 300;
  line-height: 1.1;
  color: var(--text);
  letter-spacing: -0.01em;
}

.stat-label,
.stat .label {
  display: block;
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

/* --- quick links --------------------------------------------------------- */

.quick-link {
  display: flex;
  align-items: baseline;
  gap: 0.7rem;
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--rule);
  background: none;
  border-radius: 0;
  box-shadow: none;
  color: var(--accent);
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: 500;
}

.quick-link:hover { color: var(--accent-hover); text-decoration: underline; }

.ql-text { flex: 1 1 auto; }

.ql-icon,
.quick-link .icon {
  flex: 0 0 auto;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
  order: 2;
}
```

- [ ] **Step 5: Build, run gates, verify the overflow is gone**

Run: `bundle exec jekyll build --quiet` → exit 0.
Run: `python -B scripts/test_quotes.py` → `TEST_PASS`.

Open `/` at a 375px viewport and confirm `document.documentElement.scrollWidth`
equals `clientWidth`. It overflows by 96px today.

- [ ] **Step 6: Commit**

```bash
git add assets/css/style.css
git commit -m "style: quiet tables, hairline nav, flat footer

Table headers lose their fill for an uppercase quiet label, stripes go, and row
separation is a hairline. The selector is .page-content table rather than only
.data-table, which is what fixes the home page's class-less Preservation Status
table overflowing by 96px at 375px.

Nav drops its shadow for a hairline. Footer loses its fills."
```

---

### Task 6: Narrow screens and dark-mode reconciliation

**Files:**
- Modify: `assets/css/style.css` (both `@media` blocks)

**Interfaces:**
- Consumes: every component rule from Tasks 3-5.
- Produces: no new symbols.

- [ ] **Step 1: Replace the narrow-screen rules**

Find the `@media (max-width: 640px)` block and the other narrow breakpoint, and
replace their contents with:

```css
@media (max-width: 900px) {
  :root { --measure: 100%; --measure-wide: 100%; }

  .page-content,
  .prose-reading,
  .page-content-wide,
  .hero,
  .page-header,
  .timeline,
  .card,
  .topic-backlinks,
  .recording-links,
  .secondary-backlinks,
  .info-block,
  .page-note,
  .prose-note,
  .alternate-note,
  .detail-section {
    max-width: 100%;
  }
}

@media (max-width: 640px) {
  :root { --text-3xl: 2rem; --text-xl: 1.35rem; }

  /* The three backlink blocks are already a rule-left indent at every width, so
     they need no narrow-screen special case. That is the point of doing them as
     indents: the previous 640px rule existed only to convert a filled box into
     an inset bar, and it is now unnecessary. */

  .page-content blockquote { padding-left: 0.9rem; }

  .stat-row,
  .stats { gap: 1.25rem 1.75rem; }

  .stat-value,
  .stat .value { font-size: 1.5rem; }

  /* Tables scroll rather than overflow the viewport. */
  .page-content table,
  .data-table { display: block; overflow-x: auto; white-space: nowrap; }
  .page-content table th,
  .page-content table td,
  .data-table th,
  .data-table td { white-space: normal; min-width: 9rem; }

  .timeline-item { padding-left: 1rem; }
}
```

Delete the old rule that grouped `.topic-backlinks`, `.recording-links` and
`.secondary-backlinks` with the inset `box-shadow` accent bar, and delete any
other rule that sets `box-shadow` on a non-overlay element.

- [ ] **Step 2: Verify no shadow remains on a non-raised element**

Run:

```bash
Select-String -Path assets\css\style.css -Pattern 'box-shadow' -Context 0,1
```

Expected: the only remaining `box-shadow` uses are `--shadow-overlay` (applied
to overlays such as the mobile nav drawer and the search modal) and
`--shadow-sticky`. Every other hit is a `box-shadow: none` reset.

- [ ] **Step 3: Build and check both themes**

Run: `bundle exec jekyll build --quiet` → exit 0.
Run: `python -B scripts/test_quotes.py` → `TEST_PASS`, with the palette gate
reporting 0 failures in both themes.

In a browser, force `prefers-color-scheme: dark` and re-check the home page, an
article, a transcript, `/videos/` and `/sources/`. Confirm no colour is left
behind from the old blue-black theme.

- [ ] **Step 4: Commit**

```bash
git add assets/css/style.css
git commit -m "style: narrow-screen rules rebuilt around the new components

The 640px rule that converted the three backlink blocks from filled boxes into
inset accent bars is gone: they are already rule-left indents at every width,
which is what doing them as indents bought. Tables scroll instead of overflowing
the viewport."
```

---

### Task 7: Re-record the site tour

**Files:**
- Modify: `docs/demo/site-tour.mp4`, `docs/demo/site-tour.gif` (binary)
- Modify: `scripts/build_site_tour.py` (captions and the picks list)
- Modify: `docs/demo/README.md`, `docs/demo/RELEASE-NOTES-v1.0.md`,
  `README.md` (sizes, durations, sha256s, recorded date, frame list)

**Interfaces:**
- Consumes: `SEGMENTS` and `picks` in `scripts/build_site_tour.py`.
- Produces: the two binaries plus their verified metadata.

- [ ] **Step 1: Re-capture the frames in dark theme**

The old frames are in `_staging/demo-tour/` and are gitignored, so they must be
re-taken. At a 1440x900 viewport, in dark theme, screenshot each page named in
`SEGMENTS`, naming files `NN-slug.png` / `NN-slug-b.png` in visit order, and drop
them in `_staging/demo-tour/`.

The 13 pages, in order: `/`, `/` scrolled, `/topics/`, a topic page, a topic page
scrolled, `/articles/`, one work, `/papers/`, one paper, `/transcripts/`, one
transcript, `/channel/`, `/search/`.

- [ ] **Step 2: Update the captions to the new figures and re-cut**

In `scripts/build_site_tour.py`, keep the caption text as it is unless a figure
changed. The approved counts are unchanged by this work — 207 recovered items,
72 works with 47 in full, 20 papers, 68 transcripts, 540,995 words — so no
caption needs editing. Run:

```bash
python -B scripts/build_site_tour.py
```

Expected: a new `site-tour.mp4` and `site-tour.gif`, both under 8 MB, with the
cutter reporting `GIF ... (cap 8.0)`.

- [ ] **Step 3: Read the real numbers back off the artefacts**

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration -of default=nw=1 docs/demo/site-tour.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration -of default=nw=1 docs/demo/site-tour.gif
Get-FileHash docs/demo/site-tour.mp4 -Algorithm SHA256
Get-FileHash docs/demo/site-tour.gif -Algorithm SHA256
```

Record the byte sizes, both durations, both frame rates, and both sha256 values
verbatim. Do not carry any number over from the previous recording.

- [ ] **Step 4: Update the three documentation files**

- `docs/demo/README.md`: the two size/duration cells in the artefact table, the
  recorded date, and the "It will go stale" date line, all from Step 3. Leave
  the frame list and caption table alone — the pages and captions did not change.
- `docs/demo/RELEASE-NOTES-v1.0.md`: the size, duration and sha256 cells in the
  asset table.
- `README.md`: the "See it live" paragraph's recorded date, and the
  repository-layout line for `docs/demo/`.

- [ ] **Step 5: Commit**

```bash
git add docs/demo scripts/build_site_tour.py README.md
git commit -m "docs: re-record the site tour in the reading-first design

The previous cut was recorded in the old dashboard theme, so shipping the
redesign next to it would have put a video of the old design on the same site.
All sizes, durations and sha256s are read back off the new artefacts with
ffprobe and Get-FileHash rather than carried over."
```

---

### Task 8: Full verification and deploy

**Files:**
- Test: all suites
- Modify: `llms.txt` only if a figure changed (it should not have)

**Interfaces:**
- Consumes: everything above.
- Produces: a deployed commit.

- [ ] **Step 1: Run every suite in CI order**

```bash
python -B scripts/sync_search_data.py
python -B scripts/test_search_sync.py
python -B scripts/test_canonical_57.py
python -B scripts/test_no_junk.py
python -B scripts/test_quotes.py
python -B scripts/test_transcripts.py
```

Expected: all exit 0. `test_quotes.py` reports 501 quotes verified, 731 queries,
19 recording links, `palette pairs checked: 23 text, 2 rule, in 2 themes`, and
`measure: 680px, about 76ch`.

- [ ] **Step 2: Build clean from scratch**

```bash
Remove-Item -Recurse -Force _site -ErrorAction SilentlyContinue
bundle exec jekyll build --quiet
```

Expected: exit 0, and `test_quotes.py` now also reports a non-zero
`download hrefs checked` because `_site` exists.

- [ ] **Step 3: Confirm the old palette is gone**

```bash
Select-String -Path assets\css\style.css -Pattern '#2563eb|#7c3aed|#f5f6f8|#e2e4e8'
```

Expected: no matches.

- [ ] **Step 4: Confirm no BOM**

```bash
git ls-files -z | python -B -c "import sys,pathlib; bad=[p for p in sys.stdin.buffer.read().split(b'\x00') if p and pathlib.Path(p.decode('utf-8','surrogateescape')).is_file() and pathlib.Path(p.decode('utf-8','surrogateescape')).open('rb').read(3)==b'\xef\xbb\xbf']; print('BOM files:',len(bad))"
```

Expected: `BOM files: 0`.

- [ ] **Step 5: Visual verification, both themes, four widths**

In a browser at 375, 768, 1280 and 1920, in light and in dark, open: `/`,
`/topics/`, a topic page, `/articles/`, one work, `/papers/`, one paper,
`/videos/`, one transcript, `/sources/`, `/search/`, `/404.html`.

For each, confirm: no horizontal overflow; body prose is serif; the measure
looks like 60-80 characters; every interactive element has a visible focus ring;
the status tags are legible without a fill; the three backlink blocks read as
indents.

- [ ] **Step 6: Update the spec's known-limitation note if needed**

If the Georgia fallback reads poorly in practice, record that in
`docs/superpowers/specs/2026-09-28-reading-first-redesign-design.md` §9 and open
a follow-up for self-hosting Merriweather in `assets/fonts/`. Do not add a CDN.

- [ ] **Step 7: Commit and push**

```bash
git add -A
git commit -m "style: the reading-first redesign, verified

Full reading system: serif prose at 18px/1.7 in a 680px measure, weight-300 sans
headings, SEP's red as the single accent, warm paper surfaces with content
sitting on them rather than on white cards, list rows instead of card grids,
hairline rules instead of shadows.

Two new gates hold it in place: check_palette() computes WCAG contrast for 23
text pairs and 2 rule pairs in both themes and pins --accent to SEP's red, and
check_measure() holds the prose column inside 620-720px."
git push origin public-main:main
```

- [ ] **Step 8: Confirm the deploy**

```bash
gh run list --limit 1
```

Expected: `completed success`. Then fetch `https://the-andalusian-project-archive.github.io/andalusian-archive/` and confirm the new palette is live.
