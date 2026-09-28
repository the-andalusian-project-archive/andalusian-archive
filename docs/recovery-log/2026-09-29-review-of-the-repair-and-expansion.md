# Review of the repair and the expansion (2026-09-29)

Independent review of `a7b30d2..HEAD` (7 commits: `c383564`, `9443fd9`, `1d7dcce`,
`6ca6b29`, `013c20a`, `3c07fa8`, `9129a46`). I did not write any of this and have no
interest in it being right. Everything below was checked against the working tree, the
built site and the raw captures in `_staging/`.

All five suites and `bundle exec jekyll build` were run and pass:

```
test_search_sync.py    ALL PASS  (exit 0 — but see F3: it prints FAIL and still exits 0)
test_canonical_57.py   TEST_PASS works=72 captures=87 ... total_content=220
test_transcripts.py    ALL PASS  79 transcripts, 937738 words, 67720 paragraphs
test_quotes.py         TEST_PASS 500 quotes verified, 388 links named, 272 display titles
bundle exec jekyll build  done in 9.339 seconds (exit 0)
```

---

## Verdict — is the author's prose intact?

**No. Three posts lost sentences the author wrote himself, and he is not named in
anything that records the loss.** The `comment-thread` rule in
`scripts/fetch_damage.py:259` deletes whole lines, and WordPress flattens a comment
thread onto one line per commenter-group. The author replied in three of those threads.
Commit `9129a46` deleted those three lines, and with them his own words:

- `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` — deleted:
  `Asadullah Ali11 Aug 2018This article (nor any of my other articles) make any claim
  that the Qur'an is a "scientific book".So I have no idea why you're making such an
  irrelevant point.Reply`
- `_posts/2020-03-24-lost-in-time-translation.md` — deleted:
  `Asadullah Ali11 Apr 2020Let me know how that would go. Come on, give an argument.Loading...Reply`
- `_posts/2018-08-18-yolo-a-motto-of-ignorance.md` — deleted:
  `Asadullah Ali24 Sep 2018Yes, that was the entire point of my article. Everything written
  can easily be summed up in your mindless meme.Note the sarcasm.Reply`

All three survive in `_staging/best_capture/pages/asadullahali.com_2018-08-01-gods-mercy-without-eternal-punishment.html`
and the two sibling captures, so nothing is permanently lost — but the archive no longer
holds it, and the recovery log describes the removal as "77 hits of somebody else's
commentary" (`scripts/fetch_damage.py:230`) and "33 lines of third-party commentary"
(commit `9129a46`). Both statements are false. A reader of this repository is told those
lines were somebody else's. He was not somebody else.

Separately, and worse for the reader: the committed `topics/quran-hermeneutics.md` was
never regenerated after the repair, so the **served site still publishes that comment
thread** — under a heading reading "how do I answer when someone says scripture could
have been clearer", attributed to the author, cited to `_posts/2020-03-24-lost-in-time-translation.md:76`,
a line that does not exist in a file that is now 43 lines long. So the archive both
destroyed the passage in the post and is still serving it, mislabelled, on a topic page.
No gate can see this, because every quote gate in the repository reads
`_data/topics/*.json` and none of them reads the generated `topics/*.md` or `_site/`.

## Verdict — is the archive honest about what it holds?

**Mostly, and its self-checks are unusually good, but three published claims are not
currently true and one gate is structurally incapable of failing.** Specifically:

- The served `/search/` page correctly says "all 173 preserved items" — good. But
  `scripts/test_search_sync.py:160` still asserts `searchable != 160`, which is stale
  (173), and that assertion sits *after* the `return 1` on line 153, so it can never fail
  the build. It is currently firing, printing `FAIL: searchable total is 173, not the
  published 160`, and the script then prints `test_search_sync: ALL PASS` and exits 0.
- `scripts/display_titles.py:16-18` and `_includes/title.html:18-19` both state that the
  stored title is provenance and "stays byte for byte what the catalogue holds". Commit
  `6ca6b29` rewrote the stored `title:` and body `H1` of 68 video/transcript files to
  strip the bracketed video ID, and collapsed a 4-space run to 1 in the bidirectional
  title of `_videos/s_BnmOrVaTg.md`.
- `.gitignore:79-80` says the reader-facing transcript text "passes through the
  redaction list", in a section about audience members who gave their names. The
  redaction list holds exactly one identifier — his birth name. Audience self-
  identification is published verbatim; I confirmed it on the served page.
- Against that: 220 is derived and not hardcoded, 500 quotes verify verbatim, 937,738
  words is re-derived from the 79 published pages, the 10 withheld caption captures are
  genuinely untracked and genuinely covered by `.gitignore`, and the 11 new transcripts
  each render a disclaimer. Those are real and I could not break them.

---

## Findings

### F1 — critical — `scripts/fetch_damage.py:252-297` — the `comment-thread` rule deletes the author's own replies

`_is_comment_body` fires on any line that starts `-`/`*`/`+` and contains a
`\d{1,2} <Month> 20\d\d` run anywhere. `_comment_thread_lines` then applies it
**standalone, with no heading required** (`fetch_damage.py:294-297`), and
`REPAIR_MODE["comment-thread"] = "lines"` (`fetch_damage.py:651`) deletes the whole line.

A WordPress thread where the author replied therefore has his reply deleted along with
the commenters. `git log -S "Let me know how that would go" --all` shows the text was
present at `4458e56` "Initial public release" and removed at `9129a46`.

The three lost passages are quoted in the Verdict above. I confirmed each against the
raw HTML captures under `_staging/best_capture/pages/`, so this is recoverable, but the
archive itself no longer records that it was his.

There is a second, narrower instance of the same class in the same commit: the repair
removes the thread but `_data/topics/quran-hermeneutics.json` had cited a line inside
one, and the fix was to delete the *citation* — leaving the author's own reply as the
one thing nobody put back.

**What I would do.** Before any future `repair_fetch_damage.py --apply`, split
`comment-thread` at the `Reply` boundaries and keep every span attributed to
`Asadullah Ali`, either restored to the post or written to a
`_data/held_comment_replies.json` the site can serve with its own byline. The discriminator
is already in the data — the thread is a flattened run of `<name><day><month><year>` and
the author's name is a known constant. Failing that, the honest minimum is to stop
describing these lines as "somebody else's commentary" and to name what was taken.

### F2 — critical — `topics/quran-hermeneutics.md:245` — the served site still publishes the deleted comment thread, misattributed

`git show 9129a46` removed the `wdqdqwd` claim from
`_data/topics/quran-hermeneutics.json`; I confirmed the spec no longer contains it and
that the three surviving claims for that post were re-anchored to lines 20, 28 and 68.
The generated page was not rebuilt. `_site/topics/quran-hermeneutics/index.html` contains:

> how do I answer when someone says scripture could have been clearer
> `- wdqdqwd10 Apr 2020This is a weak argument. An omniscient God would know how to explain
> future technology in a non-confusing way.Loading...ReplyAsadullah Ali11 Apr 2020Let me
> know how that would go. Come on, give an argument.Loading...Reply...`
> — **Lost in Time-Translation** (work), cited at
> `_posts/2020-03-24-lost-in-time-translation.md:76` — excerpt of about 127 words from a
> 976-word text. The argument around it is not on this page.

Three separate falsehoods in one rendered block: a stranger's objection presented as the
author's answer, the author's own reply buried inside it, and a citation to a line 33
lines past the end of the file. It also contradicts the commit message, which says "That
claim is removed, the underlying question is still served by three quotes from his own
text."

**Why no gate caught it.** `check_no_citation_into_damage` (`scripts/test_quotes.py:1055`)
and the whole of `check()` read `_data/topics/*.json`. `check_pages` compares only the
shelf block, the `<tr>` count, the byline gate and the llms.txt question count against
`topics/*.md` — it never compares the rendered quote blocks. I confirmed the gate reports
`citations into damage: 0` and `TEST_PASS` on this state.

**What I would do.** Add a check that every `key_claims` quote in every spec is either
absent from or present in `topics/<cid>.md`, and a check that every `cite-ref` line number
in `topics/*.md` is `<= len(lines)` of the file it names. Both are cheap and both would
have gone red here. Then rebuild and commit the pages.

### F3 — major — `scripts/test_search_sync.py:151-164` — a gate that cannot fail, asserting a stale number

```python
    if failures:
        print("test_search_sync: %d FAILURE(S)" % len(failures))
        return 1                      # <-- line 153
    searchable = 72 + 81 + 20         # = 173
    if searchable != 160:
        fail("searchable total is %d, not the published 160" % searchable)
    else:
        print("PASS: searchable total = %d (72 works + 81 videos + 20 papers)" % searchable)
    print("test_search_sync: ALL PASS")
    return 0
```

`fail()` records into `failures` that is never re-tested after line 153. The check is
unreachable as a failure. It is firing right now — 72+81+20 = **173**, not 160 — and
prints `FAIL: searchable total is 173, not the published 160` immediately before
`test_search_sync: ALL PASS` and `exit 0`.

The good news, which I checked: the *site* is right. `_site/search/index.html` reads
"Search across all 173 preserved items: 72 works, 81 videos and 20 papers." So the defect
is a stale constant in a dead gate, not a wrong published figure. Commit `6ca6b29`
edited the `PASS:` message to say "72 works + 81 videos + 20 papers" and left the `!= 160`
comparison beside it.

**What I would do.** Move the check above the `return 1`, and either compute the expected
total from the same files the builder reads or delete the comparison. As it stands, a
future change to any of the three counts is invisible to CI.

### F4 — major — `scripts/build_topic_pages.py:616` — re-anchoring silently does nothing for 125 of 500 citations

```python
hits = [i for i, l in enumerate(flat, 1) if l and quote in l]
```

`flat` is one entry per **line**. The test is single-line containment. But markdown
hard-wraps, and most quotes in this corpus span many lines. I ran the re-anchorer twice
over the live specs:

```
pass 1: 125 note(s), 0 ref(s) moved
pass 2: 125 note(s), 0 ref(s) moved
IDEMPOTENT: True
```

All 125 notes are `quote no longer found in <file> - left for a human`. Example:
`_posts/2020-01-23-backbone-ribs.md:692` — a 2,065-character quote spanning lines
692-698. Single-line hits: `[]`. `test_quotes.py`'s window search finds it. So
`test_quotes.py` passes it, `reanchor_spec_refs` cannot move it, and it is frozen at
whatever line it currently sits on.

That is precisely the failure the function exists to prevent. Its own docstring says
"the specs are corrected here, in the one place that holds both sides", and for a
quarter of the corpus it corrects nothing.

The reporting compounds it. `main()` (line 648) prints `refs re-anchored by content:
{len(moved)}` where `moved` is *all notes*, including the "left for a human" ones. A run
that moved nothing and failed on 125 prints "refs re-anchored by content: 125".

**What I would do.** Join a sliding window of `window_for(quote)` lines — reuse
`test_quotes.window_for`/`norm` — instead of testing one line, and report
"moved N, unresolved M" separately. Note that `test_quotes.py` is the real backstop here
and *would* catch a broken ref, so this is a robustness gap rather than a live corruption.

### F5 — major — 68 files: stored `title:` rewritten, against the module's own stated invariant

`scripts/display_titles.py:16-19`:

> Nothing is deleted from the archive. The video ID stays in front matter as
> `video_id`, the slug stays in the filename, and **the raw title is preserved
> verbatim. This function changes DISPLAY text only.**

`_includes/title.html:18-19`:

> The character in the DATA is never altered. It is provenance and stays byte for byte
> what the catalogue holds; only the markup around it changes.

Commit `6ca6b29` did exactly what both say it does not. 68 files, e.g.
`_videos/0snGWjeqEeM.md:3`:

```diff
-title: "23 - Islam, Science and History (Reupload from Andalusian Project) [0snGWjeqEeM]"
+title: "23 - Islam, Science and History (Reupload from Andalusian Project)"
```

and the same in the body `# ` H1. Separately `_videos/s_BnmOrVaTg.md:3` had a
**bidirectional Arabic/Latin title** rewritten:

```diff
-title: "مناظره عبدالله اندلسی با عارف احمد    abdullah andalusi vs arif ahmad"
+title: "مناظره عبدالله اندلسی با عارف احمد abdullah andalusi vs arif ahmad"
```

with `title_runs` and `title_iso` rewritten identically. In a mixed-direction title that
4-space run is the visual gutter between the scripts; collapsing it to one space changes
the rendered result, and `title_runs`/`title_iso` are precisely the fields that exist to
record script boundaries.

The ID is not lost — it is in `video_id:` and the permalink — so this is recoverable.
But it is a rewrite of recovered material presented by two files as forbidden, and
`build_collections.py:517` already calls `clean_display_title` at build time, so the
front-matter edit was not needed to achieve the display goal.

**What I would do.** Restore the raw `title:`/`title_runs`/`title_iso`/`H1` from
`6ca6b29^` and let `build_collections.py` clean at render, which is what the code was
designed to do. If the front-matter edit is wanted for a reason, change the two docstrings
instead of leaving them to lie.

### F6 — major — `scripts/fetch_damage.py:252-256, 386-389` — two rules that eat author-written prose, demonstrated

I constructed prose from this corpus's own register and ran it through `repair_text`.
Every one of these was deleted:

| input | rule that ate it |
|---|---|
| `- He resigned on 4 Jan 2013 after the scandal broke.` | `comment-thread` |
| `- See p. 12, 3 Jun 2019 edition, for the full table.` | `comment-thread` |
| `- "We met on 9 Nov 2001," he said. "That was the day."` | `comment-thread` |
| `- Yusuf al-Qarawi 12 Aug 2018 is the reference I mean.` | `comment-thread` |
| `Category: how the author himself uses the word in this essay.` | `category-tags-runon` |

`repair_text` output for the first: `'My point here is simple.\n\n- Another item entirely.'`

`category-tags-runon`'s only `allow` is `^\s*(?:I|We)\s`, so a sentence of the author's
prose beginning `Category:` is unrecoverable.

**Scope — and this is the mitigating fact:** I scanned all five collections
(`_posts`, `_articles`, `_papers`, `_transcripts`, `_videos`) and 1,149 files under
`_staging/` for lines matching either shape. **Zero** author-written list items carry a
date-run, and zero prose lines begin `Category:`. So on this corpus the rules did not eat
prose — the realised damage in F1 is the author's replies inside comment threads, not
these patterns. The risk is armed for the next repair pass, and the corpus does contain
dated material: the author quotes and cites dated sources constantly.

**What I would do.** Require the date-run to be *followed* by text and *preceded* by a
name-like token in the same flattened shape a WordPress comment produces (no space
between the name and the day), and drop the standalone orphan scan or require the
`Reply`/`Loading...` furniture that every real comment thread carries. For
`category-tags-runon`, require the line to look like a taxonomy list (a comma-separated
run of short words) or to be followed by a `Tags:` line.

### F7 — major — `.gitignore:79-80` — implies a privacy protection the served site does not have

```
#    Withheld, not edited, for the same reason as category 1: the bytes are
#    evidence that the recording says what it says, so the working tree keeps them
#    and only the git index drops them. The reader-facing text built from them is
#    served under /_transcripts/ and passes through the redaction list.
```

The redaction list holds **one** identifier, with marker `‖ birth name withheld ‖`. It is
his birth name, not an audience member's. The 10 withheld captures' text is published.

Verified on the served page for `0biKKRHO_Tk`, in the section `.gitignore:84-85` calls
sharp:

> `...and my brother was like man i'm like uh my name is man but you're probably looking
> for somebody else they're like no we we came from jeddah we're just looking for you...`

ASR mangled the name, which lowers but does not eliminate identifiability — the city, the
companion and the context remain. `test_transcripts.py` confirms the mechanism: "3
published transcript(s) carry the site owner's redaction ... and the other 76 are
word-for-word the capture", and all 3 redacted files are the pre-existing conversion-story
captures, none of the 11 new ones.

I want to be clear this is a defensible editorial call, and the commit discloses it
("published as spoken, on the owner's explicit decision after being told what is in
them"). The defect is that the tracked file that documents the privacy posture overstates
what the mechanism does, and `.gitignore` is the file a future maintainer will trust.

**What I would do.** Rewrite those four lines to say what is true: the raw bytes are
withheld; the served text is published as spoken and is not name-redacted; the ASR
happens to have mangled some of the names. If the intent was to redact third-party names,
put them in the redaction list — which is the only mechanism here that would do it.

### F8 — minor — `scripts/fetch_damage.py:194-221` — `injected-script-run` absorbs prose between two code-shaped lines

`_script_run_lines` clusters any two script-shaped lines within `_SCRIPT_RUN_GAP = 12`
and then takes `range(cluster[0], cluster[-1] + 1)` — every line between them, not just
the shaped ones. In a paper containing an unfenced code sample, two `System.out.println(...)`
lines six lines apart would delete the five lines of prose between them.

Fenced code is blanked first (`_strip_fenced_code`, line 524) and I verified there is
**no unfenced code in any of the five collections**, so this has not fired. `_papers` is
the collection where it would. Line-only removal of the shaped lines, with a separate
report for absorbed non-shaped lines, would be safe.

### F9 — minor — `scripts/fetch_damage.py:641-659` — gate and repair drift on two rules

`comment-prompt` (line 409) and `embed-tag` (line 353) are class `residue`/`chrome`, so
`Rule.automatic` is `True` and `check_fetch_damage` **fails the build** on them. Neither
appears in `REPAIR_MODE`, so `repair_fetch_damage.py` can never remove them. The module
docstring's claim that "both the repair pass and the build gate import the table below so
they cannot drift apart" is not true for these two. Today neither fires (residue is 0
corpus-wide), so this is latent. Either add them to `REPAIR_MODE` or mark them
report-only.

### F10 — minor — `scripts/display_titles.py:43, 141` — `_UPLOADER_CLAUSE` over-trims real titles

`_UPLOADER_CLAUSE` drops any 2-60 character run after a `｜` or `|`, vetoed only by
`_PART_MARKER`. It removed real words from two works:

- `_videos/IhE3ka7SQQs.md` — `43 - Two Andalusians, One Conference ｜ ＂Fortifying the
  Muslim Mind＂` shown as `43 - Two Andalusians, One Conference`. The subtitle is gone,
  and it is gone on the served topic pages.
- `_videos/cDHrrbOKbl4.md` — `53 - Virgins in Paradise？ ｜ Answered` shown as
  `53 - Virgins in Paradise？`. The item's own page and the transcripts/videos indexes
  still show the full `53 - Virgins in Paradise? | Answered`, so the same work is named
  two different ways on the same site.

The module docstring says "It does NOT touch the author's punctuation, spelling or
wording." 24 of 272 titles are altered; 8 of those are `｜ <clause>` trims, of which 4
are the duplicate-upload note (fine) and 4 are the two works above (not fine).

### F11 — nit — `scripts/display_titles.py:141` — `TITLE_EDITS` collapses raws

`TITLE_EDITS` is keyed on the *shown* string and filled with `setdefault`, so when two
raw titles clean to the same string only the first raw is retained. `check_display_titles`
and `check_no_collisions` then see one raw where there were two. 24 titles are altered
but the suite reports "16 cleaned for display".

### F12 — nit — `scripts/fetch_damage.py:230` says "77 hits", commit `9129a46` says "33 lines across 9 files, plus 4 orphans"

Both are in the tree describing the same removal. I counted 42 removed body lines in
`git show 9129a46 -- _posts _articles _papers`. Whichever is right, the two disagree.

---

## Could not verify

- **Whether the author consented to publishing the audience self-identification.** The
  commit says it was "on the owner's explicit decision after being told what is in them".
  I have no way to check that from the repository.
- **Whether the author's comment replies should be held content.** This is a policy call
  and `CONTRIBUTING.md`/`NOTICE.md` do not address it. I am confident they are *his words*
  and that describing them as "somebody else's commentary" is false; whether the archive
  should publish them is yours to decide.
- **That `cap-MCR3xh8wccQ` "screened clean."** `.gitignore:90-91` asserts it and the file
  is tracked. I scanned it for the self-identification patterns that flagged the other
  ten and found none, which is consistent, but I cannot reproduce whatever screening was
  done. It is 43,760 lines of unlabelled ASR of a live audience and was tracked on the
  strength of a claim in a comment.
- **The provenance of the 13 new videos** beyond what `test_transcripts.py` checks. I did
  not re-run the playlist sweep or the absence-by-id check.
- **The 9 paragraph-break differences** `test_transcripts.py` reports as a float-tie on
  exactly 2.0 s. No word differs; I did not confirm the tie is the only cause.

---

## Claims I checked and found true

- **220 = 72 + 81 + 20 + 4 + 9 + 33 + 1.** `scripts/build_content_index.py:101` computes
  it as a sum; `test_canonical_57.py:279-292` recomputes from `_data/`, compares against
  `content_index.json`'s stored total *and* its stored terms, and parses the formula
  string back out. Not hardcoded to match itself.
- **81 videos, 79 transcripts, 937,738 words, 67,720 paragraphs.** Re-derived from the 79
  published pages and from the 79 capture files by an independent reader — same words, same
  order, cue counts agree.
- **500 citations verify verbatim.** `test_quotes.py` locates each quote in the
  normalised whole-file string and asserts the cited line is one the quote actually
  occupies. The window check and the `flat` check are built separately, which is the right
  way round.
- **388 links named, 0 unnamed.** `check_link_labels` clears `LABEL_FALLBACKS`, re-runs
  `title_for` over every material row and every corpus item, and fails the build on any
  slug-like or unnamed result. `title_for` records every last-resort path it takes.
- **272 display titles checked, 0 collisions.** `check_no_collisions` reduces each raw by
  only the boilerplate the cleaner may drop and fails if the reductions still differ — the
  right test, and the part-marker veto in `_drop` is per-step.
- **10 withheld caption captures are untracked and correctly ignored.** I verified all
  13 sensitive `.vtt` files (the 3 birth-name ones plus the 10 new) are absent from
  `git ls-files`, appear in `git status --ignored` as `!!`, and are matched by
  `git check-ignore` against named `.gitignore` rules. `git status --porcelain` is clean,
  so a later `git add -A` cannot leak them. No blanket `.firecrawl/` ignore, so the 26
  load-bearing captures and 39 whisper JSONs stay tracked. No `.mp4`/`.webm`/`.m4a` present.
- **The 11 new transcripts each render a machine-transcript disclaimer on the served
  page** — 4 mentions each across all 11 built pages.
- **`sameAs` survives.** Not in `_papers/*.md` front matter, but served in the built
  pages' JSON-LD from `_data/registries.json`, which is the documented design.
- **The iKhalifa YouTube link restored at `9129a46` is verbatim from the capture.**
  `_staging/mirror/posts/ikhalifa-ep-2.txt` contains
  `https://www.youtube.com/watch?v=-BwP55UIg3c` and nothing else; the post body now
  carries exactly that. Honest restoration.
- **Fenced code is protected.** `var x = 1;` / `});` / `foo.bar();` inside a fence
  produces no gate hit.
- **`_JS_STATEMENT_LINE` is anchored**, so a sentence containing "return" mid-line is
  not matched, and lowercase-starting prose ("for example we must ask;") does not fire.
- **No third-party comment names leak into the served transcripts**, apart from
  `wdqdqwd` in the stale topic page (F2). I grepped the built site for 24 commenter
  handles; the only other hit was `Dr. Naved Bakali`, a published academic the author
  cites in a paper.

## Gates I tried to defeat

| gate | attack | result |
|---|---|---|
| `comment-thread` | author-written list item with a date (`- He resigned on 4 Jan 2013…`) | **Defeated it.** Repair deletes the line. Nothing in this corpus trips it. |
| `category-tags-runon` | prose line beginning `Category:` | **Defeated it.** Deletes the sentence. No allow pattern covers it. |
| `injected-script-run` | unfenced code sample, two `System.out.println(…)` lines | **Defeated it.** Absorbs the prose between them. No unfenced code in the corpus. |
| `comment-thread` in situ | a real thread where the author replied | **Defeated it, for real.** Three of his replies are gone (F1). |
| `markup-tag` allow | `<span class="tall-glyph">` | Held. `strip_deliberate` runs first; 0 residue. |
| `_strip_fenced_code` | `});` inside a fence | Held. |
| `test_search_sync` searchable total | let the stale `160` assertion fire | **Defeated the gate**, not the data. It fires, prints FAIL, and the build stays green. |
| `check_no_citation_into_damage` | leave a live comment-thread citation in a spec | Held for *live* damage — but the whole class of already-removed damage is invisible to it, and the stale rendered page (F2) is entirely outside its reach. |
| `check_pages` (generated pages) | delete a claim from a spec, leave the page | **Defeated it.** It compares shelf, `<tr>` count, byline and llms.txt only. Never the quote blocks. |
| `test_transcripts` re-derivation | trust stored word counts | Held. 76 word-for-word, 3 with exactly one marker per birth-name occurrence. |
| redaction marker count | swap one name for another | Held. `one '‖ birth name withheld ‖' marker per occurrence`, `redaction_note` present. |
| `reanchor_spec_refs` idempotency | run twice | Held. Byte-identical, 0 moves on the second pass. |
| `reanchor_spec_refs` wrong-line move | force an ambiguous match | Held — it requires a *unique* single-line hit and reports otherwise. But it cannot see multi-line quotes at all (F4). |
| `check_no_collisions` | drop a part number | Held. The part-marker veto rejected the rewrite and the collision count stayed 0. |
| `.gitignore` coverage | `git add -A` | Held. Working tree clean; all 13 sensitive captures ignored by name. |
