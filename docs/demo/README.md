# `docs/demo/` — the site tour

A short screen recording of the live site, so a reader can see the archive working
before reading anything about it. Two artefacts, cut from the same 13 captured
frames of the deployed site.

| File | What it is | Size |
|---|---|---:|
| [`site-tour.mp4`](site-tour.mp4) | The full tour. 1440x900, 30 fps, 35.07 s. | 3,542,646 B (3.38 MiB) |
| [`site-tour.gif`](site-tour.gif) | A size-capped preview for inline display, one frame per section. 800x500, 8 fps, 36.26 s. | 1,188,014 B (1.13 MiB) |

The repository README embeds the **GIF**, not the MP4: GitHub strips `<video>`
tags from README markdown, so a `<video>` embed renders as nothing. The GIF is
linked alongside the MP4 and the live site.

**This is a screen recording of the live site, not a rendering of the repository.**
It was captured on **2026-09-28**, after the reading-first redesign, from
<https://the-andalusian-project-archive.github.io/andalusian-archive/> at a
1440x900 viewport, using a real browser, with the site's own navigation and CSS
in place. Every frame is a screenshot of a page a visitor can open.

**The tour is recorded in the site's dark theme.** The earlier cut was light. Dark
mode is what the archive now defaults to, and a tour that shows a theme a reader
will not see is a worse advert than a slightly heavier file.

## It will go stale

**Recorded 2026-09-28, in the current design. Re-record when the site's
pages change.** This is a
picture of one moment, not a live feed. It will disagree with the site as soon as
a caption, a layout, a count or a page changes — and the captions carry figures,
so an approved recount will make them wrong. If you find a caption that no longer
matches the page it sits on, the caption is the thing to fix, and the number to
re-read from `_data/` first.

## What the MP4 shows

Thirteen frames, in this order, plus an opening title card and a closing card
carrying the live URL. Each frame gets a slow Ken Burns move and its own caption;
consecutive frames dissolve over 0.55 s, so there is no hard cut anywhere in the
video. Each frame is held for 3.0 s.

| # | Frame | Page | Caption burned in |
|---:|---|---|---|
| — | *(generated)* | title card | The Andalusian Project Archive / a screen tour of the live site |
| 1 | `01-home` | `/` | The archive - 207 recovered items, counted from the data |
| 2 | `01-home-b` | `/` scrolled | Start with a question, not a name |
| 3 | `02-topics` | `/topics/` | The questions the recovered work answers |
| 4 | `03-subject` | one topic page | A subject page: the passages, quoted and cited to a line |
| 5 | `03-subject-b` | one topic page, scrolled | Every item on the subject, and what else it belongs to |
| 6 | `04-articles` | `/articles/` | Works - 72 catalogued, 47 with full text held |
| 7 | `05-work` | one work | One work, with its provenance and recovery verdict |
| 8 | `06-papers` | `/papers/` | Papers - 20 records, with the PDFs this archive may hold |
| 9 | `07-paper` | one paper | The full text of a paper, on the page, with its licence |
| 10 | `08-transcripts` | `/transcripts/` | Transcripts - 68 machine transcripts, 540,995 words |
| 11 | `09-transcript` | one transcript | One transcript, with the machine-transcription warning |
| 12 | `10-channel` | `/channel/` | What happened to the channel, and what survives |
| 13 | `11-search` | `/search/` | Search every item, in the browser |
| — | *(generated)* | end card | The archive is live at / the-andalusian-project-archive.github.io/andalusian-archive |

Frames 2–5 are the reason this cut exists: the `/topics/` layer is the part of
the archive most likely to be useful to a reader, and the previous tour did not
show it at all.

## What the GIF shows

One frame per section — the eleven `picks` in the build script, dropping the two
scrolled second beats (`01-home-b` and `03-subject-b`) — because the 8 MB cap
cannot hold thirteen frames of this UI text (see *Why the GIF is not the MP4*
below). The GIF is the same length as the MP4, 36.26 s, because each pick keeps
the same 3.0 s hold; it is cheaper in bytes, not in seconds. It has a title card
and **no end card**.

| # | Frame | Caption burned in |
|---:|---|---|
| — | title card | The Andalusian Project Archive / a screen tour of the live site |
| 1 | `01-home` | The archive - 207 recovered items, counted from the data |
| 2 | `02-topics` | The questions the recovered work answers |
| 3 | `03-subject` | A subject page: the passages, quoted and cited to a line |
| 4 | `04-articles` | Works - 72 catalogued, 47 with full text held |
| 5 | `05-work` | One work, with its provenance and recovery verdict |
| 6 | `06-papers` | Papers - 20 records, with the PDFs this archive may hold |
| 7 | `07-paper` | The full text of a paper, on the page, with its licence |
| 8 | `08-transcripts` | Transcripts - 68 machine transcripts, 540,995 words |
| 9 | `09-transcript` | One transcript, with the machine-transcription warning |
| 10 | `10-channel` | What happened to the channel, and what survives |
| 11 | `11-search` | Search every item, in the browser |

The picks are taken **by name** from `SEGMENTS`, not by clip index. The earlier
build hardcoded filter indices like `[3:v]`, which is one inserted or removed
segment away from silently feeding the GIF the wrong frames with no error.

## The figures in the captions

Every number in a caption was read out of `_data/`, not typed from memory:

* **207 recovered items** is the site's own computed `total_content` — 72 works
  plus 68 videos plus 20 papers — and is asserted by `scripts/test_canonical_57.py`.
* **72 catalogued, 47 with full text held** is the works row, matching
  `/articles/` as rendered.
* **20 papers** is the counted paper total. The caption does not claim a PDF
  count, because that figure is a licensing decision rather than a catalogue
  one: 5 PDF files across 4 of the 20 records, with the IIUM MA thesis excerpt
  withheld in full (`NOTICE.md` §6.1a). A caption asserting a PDF count would
  need re-cutting every time that decision changed.
* **68 transcripts, 540,995 words** matches `_data/transcript_index.json` and what
  `/transcripts/` renders.

No count anywhere in the repository was changed to make a caption work.

## Re-recording

1. Open the live site in a browser at a 1440x900 viewport **in dark theme** and
   screenshot each page you want in the tour, naming them `NN-slug.png` /
   `NN-slug-b.png` in visit order.
2. Drop them in `_staging/demo-tour/`. That tree is gitignored, so captures never
   reach the repository.
3. Edit `SEGMENTS` in `scripts/build_site_tour.py`: one entry per frame, with its
   caption and its Ken Burns move. Check every figure in a caption against
   `_data/` first, and leave the number out where the recount would make it
   contested.
4. Re-run the build for both cuts and re-encode the GIF.
5. Update the frame list, the caption table, the recorded date and the file sizes
   in this file, and the numbers in the repository README's "See it live" block if
   the length changed.

## Encode settings

Both files are produced by one script, `scripts/build_site_tour.py`, driven by
ffmpeg. The script is committed, so the cut is reproducible; the captured frames
are not, because `_staging/` is gitignored — step 2 above is the only manual part
of the process.

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
text: 13 frames at 800x500 and 8 fps costs roughly 1,000 KB per second of
animation, so a frame-for-frame copy of the MP4 would need about 35 MB. The GIF
therefore carries **one frame per section** — the eleven picks the build script
names — so each caption gets real screen time instead of flashing past. At
800x500 and 8 fps it is 1.13 MiB, well inside the cap, and page headings, card
titles and the captions are all readable at 1:1.

Nothing in `docs/demo/` is referenced by the site build, so a stale or missing
tour cannot break `jekyll build` or the test suites.
