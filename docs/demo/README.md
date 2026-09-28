# `docs/demo/` — the site tour

A short screen recording of the site, so a reader can see the archive working
before reading anything about it. Two artefacts, cut from the same 13 captured
frames by `scripts/build_site_tour.py`.

| File | What it is | Size |
|---|---|---:|
| [`site-tour.mp4`](site-tour.mp4) | The full tour. 1440x900, 30 fps, 35.07 s. | 5,517,745 B (5.26 MiB) |
| [`site-tour.gif`](site-tour.gif) | A size-capped preview for inline display. 720x450, 6 fps, 24.00 s. | 6,169,014 B (5.88 MiB) |

The repository README embeds the **GIF**, not the MP4: GitHub strips `<video>`
tags from README markdown, so a `<video>` embed renders as nothing. The GIF is
linked alongside the MP4 and the live site.

**This is a screen recording of the site, not a rendering of the repository.**
It was captured on **2026-09-28**, after the reading-first redesign, at a
1440x900 viewport, using a real browser, with the site's own navigation and CSS
in place. Every frame is a screenshot of a page a visitor can open.

Captured from a **local build served on `127.0.0.1`**, not from the deployed
github.io site, by `scripts/capture_site_tour.js`. An earlier version of this
file said the frames came from the live site; that was not true of the cut it
described, and the deployed site was several commits behind anyway, so it could
not have been the source for a "latest version" recording. The frames are the
same pages and the same CSS, served from `_site/`.

**The tour is recorded in the site's light theme**, which is also the site's
default as of this recording. Two earlier cuts existed: the first was light, the
second dark on the reasoning that dark was the default. That reasoning was never
sound — a tour that shows a theme a reader will not see is a worse advert than a
slightly heavier file, and a dark-OS reader is not the majority. The theme the
site hands someone who has chosen nothing is light, so that is what the tour
shows.

## It will go stale

**Recorded 2026-09-28, in the current design. Re-record when the site's
pages change.** This is a
picture of one moment, not a live feed. It will disagree with the site as soon as
a caption, a layout, a count or a page changes — and the captions carry figures,
so an approved recount will make them wrong. If you find a caption that no longer
matches the page it sits on, the caption is the thing to fix, and the number to
re-read from `_data/` first — which is what `check_captions()` in
`build_site_tour.py` does, so the build refuses to cut a tour whose captions
quote a figure no data file produces.

## What the MP4 shows

Thirteen frames, in this order, plus an opening title card and a closing card
carrying the live URL. Each frame gets a slow Ken Burns move and its own caption;
consecutive frames dissolve over 0.55 s, so there is no hard cut anywhere in the
video. Each frame is held for 3.0 s.

| # | Frame | Page | Caption burned in |
|---:|---|---|---|
| — | *(generated)* | title card | The Andalusian Project Archive / a screen tour of the live site |
| 1 | `01-home` | `/` | The archive - 220 recovered items, counted from the data |
| 2 | `01-home-b` | `/` scrolled | Start with a question, not a name |
| 3 | `02-topics` | `/topics/` | The questions the recovered work answers |
| 4 | `03-subject` | one topic page | A subject page: the passages, quoted and cited to a line |
| 5 | `03-subject-b` | one topic page, scrolled | Every item on the subject, and what else it belongs to |
| 6 | `04-articles` | `/articles/` | Works - 72 catalogued, 47 with full text held |
| 7 | `05-work` | one work | One work, with its provenance and recovery verdict |
| 8 | `06-papers` | `/papers/` | Papers - 20 records, with the PDFs this archive may hold |
| 9 | `07-paper` | one paper | The full text of a paper, on the page, with its licence |
| 10 | `08-transcripts` | `/transcripts/` | Transcripts - 79 machine transcripts, 937,738 words |
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
| 1 | `01-home` | The archive - 220 recovered items, counted from the data |
| 2 | `02-topics` | The questions the recovered work answers |
| 3 | `03-subject` | A subject page: the passages, quoted and cited to a line |
| 4 | `04-articles` | Works - 72 catalogued, 47 with full text held |
| 5 | `05-work` | One work, with its provenance and recovery verdict |
| 6 | `06-papers` | Papers - 20 records, with the PDFs this archive may hold |
| 7 | `07-paper` | The full text of a paper, on the page, with its licence |
| 8 | `08-transcripts` | Transcripts - 79 machine transcripts, 937,738 words |
| 9 | `09-transcript` | One transcript, with the machine-transcription warning |
| 10 | `10-channel` | What happened to the channel, and what survives |
| 11 | `11-search` | Search every item, in the browser |

The picks are taken **by name** from `SEGMENTS`, not by clip index. The earlier
build hardcoded filter indices like `[3:v]`, which is one inserted or removed
segment away from silently feeding the GIF the wrong frames with no error.

## The figures in the captions

Every number in a caption was read out of `_data/`, not typed from memory:

* **220 recovered items** is the site's own computed `total_content` — 72 works
  plus 81 videos plus 20 papers — and is asserted by `scripts/test_canonical_57.py`.
* **72 catalogued, 47 with full text held** is the works row, matching
  `/articles/` as rendered.
* **20 papers** is the counted paper total. The caption does not claim a PDF
  count, because that figure is a licensing decision rather than a catalogue
  one: 5 PDF files across 4 of the 20 records, with the IIUM MA thesis excerpt
  withheld in full (`NOTICE.md` §6.1a). A caption asserting a PDF count would
  need re-cutting every time that decision changed.
* **79 transcripts, 937,738 words** matches `_data/transcript_index.json` and what
  `/transcripts/` renders.

No count anywhere in the repository was changed to make a caption work.

## Re-recording

1. Build the site and serve `_site/` on `127.0.0.1:8899`:
   `npm run build`, then `npx live-server _site -p 8899`.
2. Run `scripts/capture_site_tour.js` — it is a function to hand to a browser
   tool, not a `node` script, because the repository has no Playwright
   dependency. It captures all 13 frames in the light theme, waits for
   `document.fonts.ready` before each shot, and fails loudly if the stored theme
   is not the one being recorded.
3. Frames land in `_staging/demo-tour/`, which is gitignored, so captures never
   reach the repository.
4. Edit `SEGMENTS` in `scripts/build_site_tour.py`: one entry per frame, with its
   caption and its zoom move. Every figure in a caption is checked against
   `_data/` at build time, so leave the number out where a recount would make it
   contested.
5. `python -B scripts/build_site_tour.py` — cuts both files and fails if the GIF
   is over `GIF_MAX_MB`.
6. Update the frame list, the caption table, the recorded date, the file sizes and
   the SHA-256s in this file and in `RELEASE-NOTES-v1.0.md`.

## Encode settings

Both files are produced by one script, `scripts/build_site_tour.py`, driven by
ffmpeg. The script is committed, so the cut is reproducible; the captured frames
are not, because `_staging/` is gitignored — step 3 above is the only manual part
of the process.

**MP4** — `-c:v libx264 -preset slow -crf 23 -profile:v high -level 4.0
-pix_fmt yuv420p -r 30 -movflags +faststart -an`. Each frame is scaled to
2880x1800, driven through `zoompan`, scaled back to 1440x900, captioned with
`drawtext` in Segoe UI, then chained with `xfade` (0.55 s dissolves) and encoded.
`moov` is written before `mdat`, so the file starts playing before it has finished
downloading.

**The zoom move.** `zoompan` is given `d=1`, an input frame rate of 30, and an
eased expression that interpolates between the two zoom values in `SEGMENTS`:
`z = z_in + (z_out - z_in) * smootherstep(on / (frames - 1))`. Smootherstep is
`6t^5 - 15t^4 + 10t^3`, so the move starts and ends at zero velocity; a linear
ramp begins and ends at full speed and reads as a nudge at each end of every hold.

`d=1` is load-bearing. `zoompan`'s `d` is *output* frames per *input* frame, so
the value that was there before, `d=90`, made `on` count `0..89` within each input
frame's own group of 90 and produced 75 × 90 = 6750 frames for a three-second
clip. That is what the `-t` on the output truncates. At `d=1` the two are one to
one and `on` is the clip's real frame index.

An earlier cut used `z='if(eq(on,0),{z_out},{z_in})'`, which is not a zoom but a
cut: `on` is 0 for exactly one frame and `z_in` for every frame after it, so each
hold showed one frame at the start value and then sat still. Measured with
`mpdecimate`, the shipped MP4 kept 145 changed frames out of 1052, all of them in
the dissolve boundaries, and segment interiors kept 1–2 changed frames out of 30.
The current cut keeps 966 of 1052, and 30 of 30 in the interiors. This file
previously described the move as a "slow zoom out from z=1.28 to z=1.05 with a
±0.02 pan". There has never been a pan in the script, and the direction was
backwards; both claims are removed rather than implemented.

**The caption plate** is an opaque `--color-surface` band across the bottom 150 px,
with a `--color-border` hairline along its top edge and a `--color-primary` rule
along the bottom, and the caption in `--color-text`. The plate is opaque on
purpose: translucent, the page behind shows through the text, and because those
pixels change every frame the quantiser re-dithers the whole band continuously,
which is the single most expensive thing in the GIF. All four colours are read
out of `assets/css/style.css` at build time rather than restated, because the
previous cut hardcoded `0x0F1117` — a colour the redesign had already retired.

**GIF** — `fps=6, scale=720:-1:flags=area`, then a two-pass palette:
`palettegen=stats_mode=full:max_colors=128` and
`paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle`. `stats_mode=full`
fits the palette to the whole frame rather than to the changed pixels, which
matters here because the changed pixels are the edges of a slow zoom and a
palette fitted only to those has to approximate the paper and the body text.

**Why the GIF is not the MP4.** The GIF is capped at 8 MB and this is dense UI
text. Two things make the difference. Each pick is held for 2.0 s rather than the
MP4's 3.0 s, and each input is trimmed in the filter graph before the concat.
Shortening the hold is the cheapest saving available, because the motion is a slow
zoom and two seconds still shows all of it. The alternative, dropping a frame
rate or a pick, costs the reader something visible.

This is also why the GIF is 5.87 MiB where the previous dark cut was 1.13 MiB,
which is not a regression to be tuned away: **the previous GIF contained no
motion at all.** Every segment was one static frame held for three seconds, so a
GIF stored roughly one bitmap per segment. Fixing the ramp gave the GIF something
to compress for the first time — 144 distinct frames instead of about a dozen —
and a palette-indexed format pays for every one of them. `GIF_WIDTH` is the
other lever: halving the width quarters the pixel count, and 720 px was chosen
over 640 px to keep the captions readable, landing at 77% of the cap with real
headroom rather than sitting on it.

Nothing in `docs/demo/` is referenced by the site build, so a stale or missing
tour cannot break `jekyll build` or the test suites.
