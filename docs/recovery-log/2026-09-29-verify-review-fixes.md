# Verify-review-fixes — 2026-09-29

An independent re-check of the five defects found by the previous review of
commits `9129a46` and the fixes claimed in `bf6c47f`. Read-only except for five
deliberate fault injections, each reverted byte-for-byte and confirmed by
SHA256. **The working tree is clean and nothing was committed.**

## How this was checked

- All five suites run: `test_quotes.py`, `test_search_sync.py`,
  `test_canonical_57.py`, `test_no_junk.py`, `test_transcripts.py`. All exit 0.
- `bundle exec jekyll build` exits 0; `_site/` grepped for each restored reply
  and for the stale quotation.
- Every citation re-derived with an independent implementation of the gate's
  matcher, then cross-checked against the source line rather than the window.
- `comment-thread` re-run over the pre-damage tree `9129a46~1` and every one of
  the 33 lines it would remove inspected for author text.
- All 48 HTML captures parsed for comments attributed to the author, using the
  `bypostauthor` class, the display name, the site URL, and the gravatar hash
  `5553faa658e88b95aa8845f848084060` as four independent signals.

## Verdict on the five findings

### 1. The author's own comment replies were deleted — GENUINELY FIXED

The three replies are restored **character for character**. Each was extracted
from `_staging/best_capture/pages/` by pulling the author comment out of the
`byuser`/`bypostauthor` `<li>`, unescaping the HTML, and joining `</p><p>` into
one sentence, then compared to the shipped `> ` line with a first-difference
search. All three are exact whole-comment matches; no word changed, dropped,
added or re-punctuated.

| Post | Restored reply | Verdict |
|---|---|---|
| `2018-08-01-gods-mercy-without-eternal-punishment.md` | `This article (nor any of my other articles) make any claim that the Qur'an is a "scientific book". So I have no idea why you're making such an irrelevant point.` | exact |
| `2020-03-24-lost-in-time-translation.md` | `Let me know how that would go. Come on, give an argument.` | exact |
| `2018-08-18-yolo-a-motto-of-ignorance.md` | `Yes, that was the entire point of my article. Everything written can easily be summed up in your mindless meme. Note the sarcasm.` | exact |

`git log -S` on each sentence confirms all three were present at `9129a46~1`,
gone at `9129a46`, and back at `bf6c47f`. All three are **served**: each appears
in exactly one built page, and all three pages carry the heading.

Two exclusions are correct and should stay:

- `Loading...` is a Jetpack comment-likes widget placeholder
  (`<span class='loading'>Loading...</span>`), a fetch artefact, not his words.
- The destroyed space in `book".So` is an artefact of the flattening; the
  capture shows two `<p>` elements, so the space is the correct reading.

No reader comment text came back with them.

**Completeness — the `comment-thread` rule is clean.** Re-running
`_comment_thread_lines` over the 54 pre-damage posts reproduces the original 33
lines across 13 posts. All 33 are genuine WordPress comment furniture: 11
headings, 22 flattened bullets, every one carrying a third party's name welded
to a date. Exactly three contained author prose and all three are restored. No
author-authored HTML, list item or prose line was eaten by the date-run pattern.

**The one caveat, and it is not a regression.** Six *further* replies by him
exist in the HTML captures and are still not in the archive:

- `2014-05-04-supporting-happymuslims-...` — comments 1678, 1689, 1798
- `2015-07-30-whataboutery` — comment 2342
- `2020-01-23-backbone-ribs` — comments 3306, 3316

They carry the same four-signal authorship signature as the three that were
restored. But `git log --all -S` finds their text in **no commit, ever** — they
were never in `_posts/`, so `comment-thread` did not destroy them and this fix
did not miss them. They are absent because the flattened `.txt` captures that
feed `_posts/` never contained that comment thread; the text survives only in
the `.html`. Roughly 3,400 characters of his replies. Worth a separate lane;
it is a pre-existing gap, not a defect of `bf6c47f`.

### 2. A gate reported its failures as successes — GENUINELY FIXED

`reanchor_spec_refs` now returns `(moved, unresolved)`
(`scripts/build_topic_pages.py:582`), main() reports them separately, and the
matcher is the gate's matcher. The shared constants are asserted equal at
`scripts/test_quotes.py:969-973`.

The correctness point that matters: the gate does not merely ask whether the
quote is inside the forward window. It normalises the whole file once, records
where each line begins, and requires the cited line to be a line on which the
quote **starts** (`scripts/test_quotes.py:339-357`). I re-derived all 500
citations independently:

- cited line is not a genuine quote start: **0**
- passes only because the quote sits somewhere in the forward window: **0**
- quote occurs at more than one start line: **1**

The single ambiguous case is `_data/topics/gender-feminism.json`, slug
`do-muslim-women-need-feminism-debate`, ref `:10`, quote starting at lines
`[10, 23]`. It is the string `MDI event report + debate video embed (...)` — an
archive-authored availability record for a Wayback-only work, not his prose, so
a repeat of it is not a mis-citation.

On the specific worry that a forward window could admit a wrong line: it cannot,
because the window test is now backed by the stricter start-line test. The
re-anchor's max-of-contiguous-run rule is also safe, because it is reached only
for refs that *already fail* the gate, and it declines on any non-contiguous
match set (`build_topic_pages.py:672-677`) rather than guessing.

### 3. A generated page served stale content — GENUINELY FIXED

`check_generated_pages_in_sync` (`scripts/test_quotes.py:1000`) reads
`topics/*.md`, unescapes both sides, joins wrapped blockquote lines and requires
every printed quotation to be in a spec. It reports `158 quotation(s) printed,
0 not traceable to a spec`. The commenter's objection does not appear anywhere
in `_site/`.

### 4. A gate that could not fail — GENUINELY FIXED

`scripts/test_search_sync.py:161` checks against 173, and the failure block is
now last (`scripts/test_search_sync.py:172-174`) with `return 1`. Proved live:
forcing the total to 174 in-process produced `FAIL: searchable total is 174, not
the published 173` and **return code 1**. It can fail now.

### 5. Stored data was rewritten — GENUINELY FIXED, with one display defect

The data half is correct. `video_display_title` is back to the 52/53 dedup alone
(`scripts/build_collections.py:502`); `build_videos` writes the channel's own
string into `title:` (line 1790) and uses the cleaned form only for the body
heading (line 1837). Verified:

- `_data/videos.json` holds `24 - Asadullah Andalusi - MY STORY ｜｜ The
  Andalusian Project [7KBCENktOOU]`; the collection front matter matches it
  byte for byte.
- `clean_display_title` renders `24 - Asadullah Andalusi - MY STORY`.
- The Arabic/Latin gutter case is restored. `_videos/s_BnmOrVaTg.md` carries
  `مناظره عبدالله اندلسی با عارف احمد␣␣␣␣abdullah andalusi vs arif ahmad`
  and `title_runs` again records the boundary as two runs
  (`ar`/`rtl` then `ltr`), with the four-space gutter intact in the text.

But the rendered H1 is **not** cleaned, and this is a new problem — see New
finding 1.

## New findings, by severity

### 1. HIGH — the layout H1 shows the raw stored title, so 120 pages now print the YouTube ID

`_layouts/video.html:15` (and `post.html:23`, `article.html:5`, `paper.html:5`,
`transcript.html:17`) render the heading with
`{% include title.html title=page.title runs=page.title_runs %}`. The include
renders the string it is given and only adds `<bdi>`/tall-glyph markup
(`_includes/title.html:18-19` says so explicitly). It never calls
`clean_display_title`.

So restoring the full title to front matter — correct in itself — flowed straight
into the first `<h1>` of every collection page. Grepping `_site/`:

```
collection pages with an <h1>:            161
whose FIRST h1 carries an 11-char [id]:   120
```

`_site/videos/7KBCENktOOU/index.html` has two `<h1>` elements:

```
h1[0]: 24 - Asadullah Andalusi - MY STORY ｜｜ The Andalusian Project [7KBCENktOOU]
h1[1]: 24 - Asadullah Andalusi - MY STORY
```

The first — the one that is the page's real heading — carries the ID and the
uploader's channel clause. The second, from the Markdown body, is clean. Before
`bf6c47f` the front-matter title was itself stripped, so the layout printed the
clean string and the two headings agreed; that agreement is what the fix
removed.

This contradicts the commit's own stated outcome, "displays `# 24 - Asadullah
Andalusi - MY STORY`", and the rendering-only-path design in
`display_titles.py`. `check_display_titles` cannot see it: it inspects
`TITLE_EDITS`, a Python-side dict, never the built HTML.

### 2. HIGH — `check_no_citation_into_damage` is off by one and cannot catch the defect it was written for

`scripts/test_quotes.py:1180` computes `n = int(tail.lstrip("L")) - offset` and
tests `n in damaged`. `damaged` holds **0-based** indexes into `scannable`
(the post body after front matter), but `n` is a **1-based** file line minus the
front-matter line count — one greater than the 0-based body index. Proven by
calling the gate directly against a file with a comment thread appended:

| citation points at | gate result |
|---|---|
| the exact damaged line | **silent** |
| one line above the damaged line | fires |
| one line below the damaged line | silent |

The gate fires when the citation is one line *before* the damage, and stays
quiet when it rests *on* the damage. The original defect — a citation resting on
a WordPress comment — is precisely the case it misses. Its current `0` is
therefore not evidence that the corpus is clean.

Not currently harmful (no citation does point into damage), but it is a gate
that reports success for the wrong reason.

### 3. LOW — `check_generated_pages_in_sync` only sees quotations that end at a byline

The scan anchors on `_BYLINE` and walks upward, so a printed quotation with no
adjacent `— <a href=…>` byline is invisible to it, and so is one separated from
its byline by a blank line. My first injection attempt used a blank line and the
gate reported `158 … 0 not traceable` while the stale text sat in the page. The
real generator always emits the byline, so this is a narrow gap rather than a
live one, but the gate's reach is narrower than "reads the pages" implies.

### 4. INFO — six of his replies remain unheld

As set out under finding 1. Pre-existing, never in any commit, present only in
the HTML captures. Not a regression; a genuine incompleteness in what the
archive holds of his work.

## Gates defeated

None. Five faults were injected; four produced the expected failure and a clean
revert.

| # | Gate | Fault injected | Result |
|---|---|---|---|
| 1 | `check_generated_pages_in_sync` | stale quotation appended to `topics/quran-hermeneutics.md` | **caught** — `159 … 1 not traceable`, `TEST_FAIL: 1 problem(s)`, exit 1 |
| 2a | `check_refs_agree_with_gate` | a ref moved to line 1 | **caught** — `1 the re-anchor would move`, `QUOTE NOT FOUND`, exit 1 |
| 2b | same | `_CHARS_PER_LINE` 30 → 31 | **caught** — `AssertionError: re-anchor CHARS_PER_LINE 31 != gate 30`, exit 1 |
| 3 | `check_fetch_damage` | comment-thread line appended to a cited post | **caught** — `fetch damage: comment-thread in 1 place(s)`, exit 1 |
| 4 | `check_link_labels` | material row with no title anywhere | **caught** — `slug-like link label for 'some-unlabelled-row…'`, exit 1 |

The same injection run produced `citations into damage: 0` — that is the
off-by-one in New finding 2, not a gate that cannot fail.

Every injection was reverted from a byte copy and confirmed by SHA256. After the
last one, `test_quotes.py` returned to `TEST_PASS` and exit 0, all five suites
exit 0, and `git status --porcelain` is empty with no stashes.

## Claims verified as true

| Claim | Result |
|---|---|
| 3 replies restored verbatim | confirmed character-exact against the captures |
| `comment-thread` destroyed nothing else of his | 33 lines re-checked; 3 held author prose; all 3 restored |
| re-anchor returns a tuple, reports both counts | `scripts/build_topic_pages.py:582` |
| re-anchor and gate share one matcher | constants asserted equal; 500/500 agree, 0 unresolved, idempotent |
| 500 citations verify, none on a wrong line | 0 citations fail the stricter start-line test |
| generated page rebuilt | 158 quotations traceable; stale text absent from `_site/` |
| search-sync constant 173, failure block last | 174 → `FAIL` → return 1 |
| 220 items | `72 + 81 + 20 + 4 + 9 + 33 + 1 = 220`, matches `content_index.json` |
| 81 videos / 79 transcripts | `len(videos.json)` 81; 79 pages, coverage agrees |
| 937,738 transcript words | re-derived from the 79 capture files by an independent reader |
| 500 citations | 500 `key_claims` across the eight topic specs |
| 173 searchable | `72 + 81 + 20` |
| 388 links named | 0 unnamed |
| stored titles hold the channel's original | 68 files match `_data/videos.json` byte for byte |
| `title_runs` / `title_iso` not collapsed | the one bidi title has 2 runs and the 4-space gutter intact |
| restored section breaks nothing | suite green; replies appended at end of post, so no line number moved |

## Plainly

The three replies are back and they are right. The four gates the review called
out are real: each one fails when it should, and the arithmetic holds.

Two things are wrong. The stored-title fix went half a way — the data is
restored but the layout now prints the raw title, so **120 collection pages
show the YouTube ID in their heading**, which is a new regression this commit
introduced. And `check_no_citation_into_damage` is off by one: it cannot detect
a citation resting on a damaged line, which is the one thing it exists to
detect, so its `0` proves nothing. Both are small, localised fixes. Nothing in
this commit destroyed the author's prose.
