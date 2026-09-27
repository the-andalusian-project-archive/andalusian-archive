# `docs/demo/` — the site tour

A short screen recording of the live site, so a reader can see the archive working
before reading anything about it. Two artefacts, cut from the same 19 captured
frames of the deployed site.

| File | What it is | Size |
|---|---|---:|
| [`site-tour.mp4`](site-tour.mp4) | The full tour. 1440x900, 30 fps, 55.7 s. | 12,544,496 B (11.96 MiB) |
| [`site-tour.gif`](site-tour.gif) | A size-capped preview for inline display, one frame per section. 800x500, 8 fps, 12.63 s. | 7,117,088 B (6.79 MiB) |

The repository README embeds the **GIF**, not the MP4: GitHub strips `<video>`
tags from README markdown, so a `<video>` embed renders as nothing. The GIF is
linked alongside the MP4 and the live site.

**This is a screen recording of the live site, not a rendering of the repository.**
It was captured on **2026-09-27** from
<https://the-andalusian-project-archive.github.io/andalusian-archive/> at a
1440x900 viewport, using a real browser, with the site's own navigation and CSS
in place. Every frame is a screenshot of a page a visitor can open.

## It will go stale

**Recorded 2026-09-27. Re-record when the site's pages change.** This is a
picture of one moment, not a live feed. It will disagree with the site as soon as
a caption, a layout, a count or a page changes — and the captions carry figures,
so an approved recount will make them wrong. If you find a caption that no longer
matches the page it sits on, the caption is the thing to fix, and the number to
re-read from `_data/` first.

## What the MP4 shows

Nineteen frames, in this order, plus an opening title card and a closing card
carrying the live URL. Each frame gets a slow Ken Burns move and its own caption;
consecutive frames dissolve over 0.55 s, so there is no hard cut anywhere in the
video.

| # | Frame | Page | Caption burned in |
|---:|---|---|---|
| — | *(generated)* | title card | The Andalusian Project Archive / a screen tour of the live site |
| 1 | `01-home.png` | `/` | Home - the four collections, and the honest count |
| 2 | `01-home-b.png` | `/` scrolled | Home - preservation status, collection by collection |
| 3 | `02-articles.png` | `/articles/` | Works - every post, and what was recovered of each |
| 4 | `02-articles-b.png` | `/articles/` scrolled | Works - the rest of the recovered writing |
| 5 | `03-work-detail.png` | one work | One work, with its provenance and its recovery verdict |
| 6 | `03-work-detail-b.png` | one work, scrolled | Works - the related writing, the talk, and the transcript |
| 7 | `04-papers.png` | `/papers/` | Papers - records, with the PDFs this archive may hold |
| 8 | `04-papers-b.png` | `/papers/` scrolled | Papers - the co-authored work is listed separately |
| 9 | `05-videos.png` | `/videos/` | Videos - 68 catalogued recordings |
| 10 | `05-videos-b.png` | `/videos/` scrolled | Videos - every record carries its themes and its tone |
| 11 | `06-transcripts.png` | `/transcripts/` | Transcripts - 68 machine transcripts, 540,995 words |
| 12 | `06-transcripts-b.png` | `/transcripts/` scrolled | Transcripts - one document per capture, listed together |
| 13 | `07-transcript-detail.png` | one transcript | One transcript, with the machine-transcript disclaimer |
| 14 | `07-transcript-detail-b.png` | one transcript, scrolled | Transcript text - the machine words, uncorrected |
| 15 | `08-channel.png` | `/channel/` | Channel history - what the channel was, and why it is gone |
| 16 | `08-channel-b.png` | `/channel/` scrolled | Channel history - the subscriber series, from its own header |
| 17 | `09-timeline.png` | `/timeline/` | Timeline - the work in date order |
| 18 | `09-timeline-b.png` | `/timeline/` scrolled | Timeline - each item with the status of its capture |
| 19 | `10-search-results.png` | `/search/` | Search - the client-side index, nothing leaves the browser |
| — | *(generated)* | end card | The archive is live at / the-andalusian-project-archive.github.io/andalusian-archive |

Frames 13 and 14 are a re-capture. The frames originally taken for that segment
were screenshots of the site's 404 page, not of a transcript; they were replaced
by a real transcript page (`/transcripts/1962338957360877/`) before the encode.

## What the GIF shows

One frame per section — the ten sections above, first frame of each, dropping the
scrolled second beat — because the 8 MB cap cannot hold nineteen frames of this UI
text (see *Why the GIF is not the MP4* below). Its captions are the section captions
above, with two wordings shortened to fit the shorter hold:

| # | Frame | Caption burned in |
|---:|---|---|
| — | title card | The Andalusian Project Archive / a screen tour of the live site |
| 1 | `01-home.png` | Home - the four collections, and the honest count |
| 2 | `02-articles.png` | Works - every post, and what was recovered of each |
| 3 | `03-work-detail.png` | A single work, with its provenance and its recovery verdict |
| 4 | `04-papers.png` | Papers - records, with the PDFs this archive may hold |
| 5 | `05-videos.png` | Videos - 68 catalogued recordings |
| 6 | `06-transcripts.png` | Transcripts - 68 machine transcripts, 540,995 words |
| 7 | `07-transcript-detail.png` | One transcript, with the machine-transcript disclaimer |
| 8 | `08-channel.png` | Channel history - what the channel was, and why it is gone |
| 9 | `09-timeline.png` | Timeline - the work in date order |
| 10 | `10-search-results.png` | Search - the client-side index, nothing leaves the browser |
| — | end card | The archive is live at / the-andalusian-project-archive.github.io/andalusian-archive |

## The figures in the captions

Every number in a caption was read out of `_data/`, not typed from memory, and
two captions deliberately carry **no** number at all:

* **Works** and **Papers** carry no count. `_data/canonical_works.json` holds 72
  counted works and `_data/papers.json` holds 20 counted papers, but the site's
  published headline totals are still frozen at 57 and 18 pending the site
  owner's approval of the recount (see *Note on the published totals* in the
  repository README). A caption asserting either figure would contradict the page
  it is printed over, so it names the collection instead.
* **Videos** (68) and **Transcripts** (68 documents, 540,995 words) carry figures
  because `_data/videos.json` and `_data/transcript_index.json` agree with what
  the pages render, so nothing on screen contradicts them.

No count anywhere in the repository was changed to make a caption work.

## Encode settings

Both files are produced by one script, `scripts`-external, driven by ffmpeg
`N-125875-g5d4d3bdc61`. The exact commands are in the media report and can be
re-run verbatim.

**MP4** — `-c:v libx264 -preset slow -crf 23 -profile:v high -level 4.0
-pix_fmt yuv420p -r 30 -movflags +faststart -an`. Each frame is scaled to
2880x1800, driven through `zoompan` (slow zoom out from `z=1.28` to `z=1.05`
with a +-0.02 pan), scaled back to 1440x900, captioned with `drawtext` in
Segoe UI, then chained with `xfade` (0.55 s dissolves) and encoded. `moov` is
written before `mdat`, so the file starts playing before it has finished
downloading.

**GIF** — `fps=8, scale=800:-1:flags=area`, then a two-pass palette:
`palettegen=stats_mode=diff:max_colors=256` and `paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle`.
`stats_mode=diff` weights the palette towards the colours that actually change
between frames, which reads better on UI screenshots than a whole-clip
histogram; `diff_mode=rectangle` stores only the rectangle that changed.

**Why the GIF is not the MP4.** The GIF is capped at 8 MB, and this is dense UI
text: 19 frames at 800x500 and 8 fps costs roughly 1,000 KB per second of
animation, so a frame-for-frame copy of the MP4 would need about 55 MB. The GIF
therefore carries **one frame per section** — the ten captions the tour is
specified with — so each caption gets real screen time instead of flashing past.
At 800x500, 8 fps and 12.63 s it is 6.79 MiB, inside the cap with 15% to spare,
and page headings, card titles and the captions are all readable at 1:1.

## Re-recording

1. Open the live site in a browser at a 1440x900 viewport and screenshot each
   page you want in the tour, top of page and one scroll down, naming them
   `NN-slug.png` / `NN-slug-b.png` in visit order.
2. Drop them in `_staging/demo-tour/`. That tree is gitignored, so captures never
   reach the repository.
3. Edit `SEGMENTS` in the build script: one entry per frame, with its caption and
   its Ken Burns move. Check every figure in a caption against `_data/` first,
   and leave the number out where the recount would make it contested.
4. Re-run the build for both cuts and re-encode the GIF.
5. Update the frame list, the caption table and the recorded date in this file,
   and the numbers in the repository README's "See it live" block if the length
   changed.

Nothing in `docs/demo/` is referenced by the site build, so a stale or missing
tour cannot break `jekyll build` or the test suites.
