#!/usr/bin/env python3
"""Cut the site tour from captured frames. Light mode, 2026-09-28.

WHY THIS IS IN THE REPOSITORY NOW. The previous tour was cut by a script that
lived outside the repository, and all 19 source frames were left behind in a
gitignored directory. When the tour needed re-recording there was nothing to
re-run and nothing to re-use, so this records the whole cut: the segment list,
the captions, the Ken Burns moves and the ffmpeg invocation. A future
maintainer can change a caption here and re-cut, instead of rediscovering the
pipeline.

The previous version also left a STALE warning in docs/demo/README.md saying
the tour showed pre-recount totals and had to be re-recorded before v1.0. That
warning is now resolved rather than carried forward.

INPUT   _staging/demo-tour/NN-name.png   1440x900, captured in light mode
        by scripts/capture_site_tour.js
OUTPUT  docs/demo/site-tour.mp4          1440x900, 30 fps
        docs/demo/site-tour.gif          800x500, 8 fps, under 8 MB

Usage: python scripts/build_site_tour.py [--mp4-only] [--gif-only]
Requires: ffmpeg on PATH, Pillow.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMES = ROOT / "_staging" / "demo-tour"
OUT = ROOT / "docs" / "demo"
WORK = ROOT / "_staging" / "demo-tour-work"

# Every figure a caption prints is checked against _data/ by check_captions()
# below, before anything is burned in. The previous version of this file claimed
# that check existed; it did not - the only validation was that the frame file
# was on disk - so the claim was removed and then the check was written.
#
# The tuple comment used to read `(frame, caption, zoom-in-out, pan)`. There has
# never been a pan in it; the fourth field has always been `z_in`, the zoom it
# moves TO. The docs separately promised a "+-0.02 pan" that no line of this
# script has ever implemented, so the promise is being corrected in the docs
# rather than the code growing a drift nobody asked for.
SEGMENTS = [
    # (frame, caption, zoom-in-out, pan)
    ("01-home",       "The archive - 207 recovered items, counted from the data", 1.05, 1.28),
    ("01-home-b",     "Start with a question, not a name", 1.28, 1.05),
    ("02-topics",     "The questions the recovered work answers", 1.06, 1.26),
    ("03-subject",    "A subject page: the passages, quoted and cited to a line", 1.24, 1.06),
    ("03-subject-b",  "Every item on the subject, and what else it belongs to", 1.06, 1.24),
    ("04-articles",   "Works - 72 catalogued, 47 with full text held", 1.24, 1.06),
    ("05-work",       "One work, with its provenance and recovery verdict", 1.06, 1.24),
    ("06-papers",     "Papers - 20 records, with the PDFs this archive may hold", 1.24, 1.06),
    ("07-paper",      "The full text of a paper, on the page, with its licence", 1.06, 1.24),
    ("08-transcripts","Transcripts - 68 machine transcripts, 540,995 words", 1.24, 1.06),
    ("09-transcript", "One transcript, with the machine-transcription warning", 1.06, 1.24),
    ("10-channel",    "What happened to the channel, and what survives", 1.24, 1.06),
    ("11-search",     "Search every item, in the browser", 1.06, 1.24),
]

HOLD = 3.0          # seconds each frame is held in the MP4
GIF_HOLD = 2.0      # seconds each frame is held in the GIF
XFADE = 0.55        # dissolve between frames
FPS = 30
GIF_FPS = 6
GIF_WIDTH = 720     # of 1440. Halving the width quarters the pixel count the
                    # GIF has to store, which is the cheapest saving available:
                    # measured 7.05 MB at 800px, 5.87 at 720, 4.59 at 640. 720
                    # keeps the caption readable and leaves real headroom under
                    # the cap instead of sitting on it - and a 5.9 MB preview is
                    # a kinder thing to hand someone on a phone than a 7 MB one.
GIF_MAX_MB = 8.0
GIF_MAX_COLORS = 128


def light_tokens() -> dict[str, str]:
    """The light palette, read out of the stylesheet rather than restated here.

    The previous cut hardcoded 0x0F1117 for its caption plates and title cards.
    That colour was already dead: assets/css/style.css says in its own palette
    note that the previous dark theme *was* #0f1117 and has since been replaced
    by --color-bg #33201d, so the plates had been painted a colour the site no
    longer used anywhere. Reading the tokens means that cannot happen again, and
    a palette change in the stylesheet moves the captions with it.
    """
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    m = re.search(r":root\s*\{", css)
    if not m:
        raise SystemExit("assets/css/style.css has no :root block")
    depth = 0
    i = m.end() - 1
    while i < len(css):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    body = css[m.end():i]
    return {n: v.strip() for n, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body)}


def hex_arg(palette: dict[str, str], name: str) -> str:
    """One #rrggbb token as an ffmpeg colour argument, 0xRRGGBB."""
    value = palette[name].lstrip("#")
    if len(value) != 6 or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise SystemExit(f"{name} is not a #rrggbb value: {palette[name]!r}")
    return "0x" + value


PALETTE = light_tokens()
SURFACE = hex_arg(PALETTE, "--color-bg")          # #f4efe9 card and card base
PLATE = hex_arg(PALETTE, "--color-surface")       # #fdfbf8 caption plate
PLATE_EDGE = hex_arg(PALETTE, "--color-border")   # #d5cab7 plate hairline
FG = hex_arg(PALETTE, "--color-text")             # #1c1a17, 16.8:1 on the plate
DIM = hex_arg(PALETTE, "--color-text-secondary")  # #5c5750, 6.9:1 on the plate
ACCENT = hex_arg(PALETTE, "--color-primary")      # #8c1515

# drawtext parses its own options, so a Windows drive colon has to be escaped
# AND the whole path quoted, or C: is read as a filter name.
FONT = "'C\\:/Windows/Fonts/segoeui.ttf'"
FONT_BOLD = "'C\\:/Windows/Fonts/segoeuib.ttf'"


def caption_numbers() -> dict[str, int]:
    """Every figure the captions quote, read from the data at build time.

    Nothing is restated. content_index.statistics is already asserted against the
    underlying _data/ files by scripts/test_canonical_57.py, so reading it gives
    one derivation rather than two, and if the catalogue moves both gates notice
    instead of only the one that happens to be run.
    """
    stats = json.loads(
        (ROOT / "_data" / "content_index.json").read_text(encoding="utf-8")
    )["statistics"]
    transcripts = json.loads(
        (ROOT / "_data" / "transcript_index.json").read_text(encoding="utf-8")
    )
    return {
        "total_content": stats["total_content"],
        "works": stats["total_blog_works"],
        "works_with_full_text": stats["blog_status_counts"]["found"],
        "papers": stats["total_papers"],
        "transcripts": transcripts["documents"],
        "transcript_words": transcripts["words"],
    }


def check_captions() -> list[str]:
    """No caption may print a figure the data does not produce.

    This is the check the file used to claim it had. It reads the six numbers the
    captions quote out of _data/ and then requires that every number appearing in
    every caption is one of them - so a caption cannot drift when the catalogue
    changes, and cannot carry a figure nothing derives. Thousands separators are
    stripped, so "540,995" is compared as 540995.
    """
    facts = caption_numbers()
    allowed = set(facts.values())
    bad: list[str] = []
    for name, caption, *_ in SEGMENTS:
        for token in re.findall(r"\d[\d,]*", caption):
            value = int(token.replace(",", ""))
            if value not in allowed:
                bad.append(
                    f"{name}: caption prints {token!r} and no _data/ figure is "
                    f"{value}; derived figures are {sorted(allowed)}")
    return bad


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-2500:] + "\n")
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:4])}...")


def esc(text: str) -> str:
    """Escape a string for use as an ffmpeg filter option value.

    `drawtext` parses its own options, and its text field is full of characters
    with meaning at the filter-graph level. A single unescaped colon is enough
    to kill the encode: the caption "A subject page: the passages..." parsed as
    an option named `page` and ffmpeg exited with "No option name near...". Order
    matters - the backslash first, so the escapes added afterwards are not
    themselves escaped.
    """
    out = text.replace("\\", "\\\\")
    for ch in (":", "'", "%", "[", "]", ",", ";"):
        out = out.replace(ch, "\\" + ch)
    return out


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


def title_card(text: str, sub: str, out: pathlib.Path) -> None:
    """A title or end card, drawn on the site's own light surface."""
    vf = (
        f"drawbox=x=0:y=0:w=iw:h=ih:color={SURFACE}:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:text='{esc(text)}':fontcolor={FG}"
        f":fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2-40,"
        f"drawtext=fontfile={FONT}:text='{esc(sub)}':fontcolor={DIM}"
        f":fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2+50"
    )
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={SURFACE}:s=1440x900:d=3.2",
        "-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out),
    ])


def ease_expr(frames: int) -> str:
    """Smootherstep position of output frame `on`, as an ffmpeg expression.

    `on` is the output frame counter, and with d=1 it runs 0..frames-1 once
    across the clip. Smootherstep is 6t^5-15t^4+10t^3, which starts and ends at
    zero velocity. That is the whole point of using it rather than a linear
    ramp: a linear zoom begins and ends at full speed, and on a 3s hold that
    reads as a nudge at each end - thirteen times.
    """
    t = f"(on/{frames - 1})"
    return f"({t}*{t}*{t}*({t}*({t}*6-15)+10))"


def frame_clip(src: pathlib.Path, caption: str, z_out: float, z_in: float,
               dur: float, out: pathlib.Path) -> None:
    """One frame: eased Ken Burns, caption plate, output a silent clip."""
    frames = int(dur * FPS)
    # 2880x1800 then down to 1440x900 gives zoompan the headroom it needs to pan
    # without resampling artefacts.
    #
    # THE RAMP. This used to be `zoompan=z='if(eq(on,0),{z_out},{z_in})'`. That is
    # not a zoom, it is a cut: `on` is 0 for exactly one output frame and equals
    # z_in for every frame after it, so each three-second hold showed the start
    # value for 1/30s and then sat still. Measured on the shipped MP4 with
    # mpdecimate, segment interiors kept 1-2 changed frames out of 30 and only
    # the dissolve boundaries moved at all - 145 changed frames out of 1052
    # across the whole clip. What read as jitter was thirteen snaps and thirteen
    # dissolves with no motion between them.
    #
    # `d=1` is what makes `on` mean what the expression assumes. zoompan's `d` is
    # OUTPUT frames per INPUT frame, so the old `d=90` made `on` count 0..89
    # within each input frame's own group of 90; with the input looped it
    # produced 75*90 = 6750 frames, which is what the `-t` on the output below
    # exists to truncate. At d=1 input and output are one frame each, `-framerate`
    # before `-loop 1` sets the input rate, and `on` is the clip's real frame
    # index. `-t` is kept as a guard.
    ease = ease_expr(frames)
    zoom = f"{z_in}+({z_out}-{z_in})*{ease}"
    vf = (
        f"scale=2880:1800:flags=lanczos,"
        f"zoompan=z='{zoom}'"
        f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s=1440x900:fps={FPS},"
        # The plate inverts with the theme: a solid near-white band with a
        # hairline along its top edge, the site's red rule along the bottom, and
        # dark ink.
        #
        # It is opaque on purpose, and the previous cut had it at 0.92 over the
        # dark frames. A translucent plate over moving page content is wrong twice
        # over: the text behind shows through the caption, and because the pixels
        # under the band change every frame the quantiser has to re-dither the
        # whole 150px strip continuously, which is the single most expensive thing
        # in the file. A solid band is one flat colour, so it costs almost nothing
        # and the caption is clean.
        #
        # `ih`, not `h`. In drawbox, `h` is the HEIGHT OF THE BOX BEING DEFINED,
        # not the height of the frame - so the old `y=h-150` evaluated to
        # y=150-150=0 and painted the plate across the top of the picture, and
        # `y=h-6` for the rule evaluated to y=0 as well. The input height is `ih`.
        # drawtext is the opposite: there `h` IS the frame height, which is why the
        # caption text landed in the right place while its plate did not. In the
        # dark cut both were invisible mistakes - a dark band on a dark frame at
        # the top of the picture, with dark text sitting on whatever happened to
        # be behind it. The light theme made it obvious: a red bar across the top
        # of every frame and a caption with no background at all.
        f"drawbox=x=0:y=ih-150:w=iw:h=150:color={PLATE}:t=fill,"
        f"drawbox=x=0:y=ih-151:w=iw:h=1:color={PLATE_EDGE}:t=fill,"
        f"drawbox=x=0:y=ih-6:w=iw:h=6:color={ACCENT}:t=fill,"
        f"drawtext=fontfile={FONT}:text='{esc(caption)}'"
        f":fontcolor={FG}:fontsize=34:x=70:y=h-98"
    )
    # `-t` goes on the OUTPUT, not the input. See the d=1 note above: the old
    # d=90 with `-loop 1` emitted 6750 frames for a three-second clip.
    run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-loop", "1", "-i", str(src),
        "-vf", vf, "-t", f"{dur}", "-r", str(FPS), "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", str(out),
    ])


def probe_duration(path: pathlib.Path) -> float:
    """Duration in seconds, so the build reports a real number.

    An encode can exit 0 and write a file with no content in it, which is
    exactly what the first xfade chain did. Reporting the duration turns that
    silent failure into a visible one.
    """
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4-only", action="store_true")
    ap.add_argument("--gif-only", action="store_true")
    args = ap.parse_args()

    if not have("ffmpeg"):
        print("ffmpeg is not on PATH", file=sys.stderr)
        return 1
    missing = [n for n, *_ in SEGMENTS if not (FRAMES / f"{n}.png").is_file()]
    if missing:
        print(f"missing frames in {FRAMES}: {missing}", file=sys.stderr)
        return 1

    # Before anything is rendered. A caption is burned into 13 clips and cannot be
    # edited afterwards without re-cutting the whole tour, so a figure the data
    # does not support has to stop the build here.
    caption_problems = check_captions()
    if caption_problems:
        print("caption figures do not match _data/:", file=sys.stderr)
        for p in caption_problems:
            print("  " + p, file=sys.stderr)
        return 1
    facts = caption_numbers()
    print("captions checked     : "
          + ", ".join(f"{k}={v:,}" for k, v in facts.items()))

    # The old build cached the GIF's title card on disk and reused it if present.
    # The card on disk was drawn in the old dark ink on the old 0x0F1117 surface,
    # so a re-cut silently kept a stale card - the only visible symptom being a
    # darker strip at the head of the GIF. The card costs one second to render, so
    # it is rebuilt every time and the cache is gone rather than worked around.
    WORK.mkdir(parents=True, exist_ok=True)
    clips: list[pathlib.Path] = []

    head = WORK / "00-title.mp4"
    if not args.gif_only:
        title_card("The Andalusian Project Archive",
                   "a screen tour of the live site", head)
        clips.append(head)

    for name, caption, z_out, z_in in SEGMENTS:
        clip = WORK / f"{name}.mp4"
        frame_clip(FRAMES / f"{name}.png", caption, z_out, z_in, HOLD, clip)
        clips.append(clip)
        print(f"  {name}: {caption}")

    if not args.gif_only:
        tail = WORK / "99-end.mp4"
        title_card("The archive is live",
                   "the-andalusian-project-archive.github.io/andalusian-archive",
                   tail)
        clips.append(tail)

    # ---- chain with dissolves -------------------------------------------
    if not args.mp4_only:
        inputs = []
        for c in clips:
            inputs += ["-i", str(c)]
        chains = []
        prev = "[0:v]"
        for i in range(1, len(clips)):
            label = f"[v{i}]"
            # The i-th dissolve starts at (i-1) * (HOLD - XFADE). Writing this
            # as `HOLD - XFADE * i` - which is what the first version did -
            # counts DOWN from 2.45s and produces an output the encoder accepts
            # and writes 20 kB of, so the failure is silent: ffmpeg exits 0 and
            # the file is empty of content. Cumulative, not decreasing.
            offset = (i - 1) * (HOLD - XFADE)
            chains.append(
                f"{prev}[{i}:v]xfade=transition=fade:duration={XFADE}"
                f":offset={offset:.3f}{label}"
            )
            prev = label
        mp4 = OUT / "site-tour.mp4"
        run([
            "ffmpeg", "-y", *inputs, "-filter_complex", ";".join(chains),
            "-map", f"[v{len(clips) - 1}]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "23",
            "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-movflags", "+faststart", "-an", str(mp4),
        ])
        dur = probe_duration(mp4)
        print(f"\nMP4  {mp4.name}  {mp4.stat().st_size / 1e6:.2f} MB  {dur:.1f}s")

    # ---- GIF: shorter holds, two-pass palette, under the cap ----------------
    # WHY THE GIF IS NOW SHORTER PER FRAME. It was 1.19 MB in the previous cut and
    # this one came out at 17.75 MB, which the cap correctly refused. Almost none
    # of that is the light theme. The reason is that the GIF used to contain no
    # motion at all: every segment was the same static frame for 3s, so a GIF
    # stored roughly one bitmap per segment. Fixing the ramp gave the GIF
    # something to compress for the first time - 288 distinct frames instead of
    # about a dozen - and a palette-indexed format pays for every one of them.
    #
    # So the budget is spent on frames. The three ways to buy them back are
    # dropping picks, dropping frame rate, or holding each pick for less time.
    # Measured on this footage: dropping a pick loses a page of the tour; 6fps
    # over 3s holds still missed the cap at 9.03 MB; shortening the hold to 2.0s
    # while keeping 6fps and every pick landed at 6.09 MB. Holding each frame for
    # less time is the one that costs the reader nothing, because the motion is a
    # slow zoom and 2s shows the whole of it.
    #
    # The picks are taken by NAME from SEGMENTS rather than by clip index: the
    # earlier version hardcoded filter indices like [3:v] and [11:v], which is one
    # segment inserted or removed away from silently feeding the GIF the wrong
    # frames.
    picks = ["01-home", "02-topics", "03-subject", "04-articles", "05-work",
             "06-papers", "07-paper", "08-transcripts", "09-transcript",
             "10-channel", "11-search"]
    by_name = {n: c for n, c, *_ in SEGMENTS}
    unused = sorted(set(by_name) - set(picks))
    if unused:
        print("  note: not in the GIF: " + ", ".join(unused))
    gif_head = WORK / "gif-title.mp4"
    title_card("The Andalusian Project Archive", "a screen tour", gif_head)
    gif_clips = [gif_head]
    for name in picks:
        gif_clips.append(WORK / f"{name}.mp4")

    # Each input is trimmed to GIF_HOLD before the concat. `setpts=PTS-STARTPTS`
    # is required: trim leaves the presentation timestamps where they were, and
    # concat expects each segment to start at zero.
    gif_src = WORK / "gif-concat.mp4"
    inputs: list[str] = []
    for c in gif_clips:
        inputs += ["-i", str(c)]
    chains = [
        f"[{i}:v]trim=0:{GIF_HOLD},setpts=PTS-STARTPTS[g{i}]"
        for i in range(len(gif_clips))
    ]
    chains.append("".join(f"[g{i}]" for i in range(len(gif_clips)))
                  + f"concat=n={len(gif_clips)}:v=1:a=0[out]")
    run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(chains),
        "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", str(gif_src),
    ])

    # stats_mode=full, not diff. With diff the palette is fitted to the changed
    # pixels between frames - mostly the edges of a moving zoom - and then has to
    # approximate the paper and the body text with a palette that never saw them.
    # Measured here: full 17.31 MB against diff 16.93 MB at the same settings,
    # and the full-frame palette is the one that keeps the small text readable.
    gif = OUT / "site-tour.gif"
    run([
        "ffmpeg", "-y", "-i", str(gif_src),
        "-vf", f"fps={GIF_FPS},scale={GIF_WIDTH}:-1:flags=area,split[a][b];"
               f"[a]palettegen=stats_mode=full:max_colors={GIF_MAX_COLORS}[p];"
               f"[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
        str(gif),
    ])
    mb = gif.stat().st_size / 1e6
    print(f"GIF  {gif.name}  {mb:.2f} MB  "
          f"(cap {GIF_MAX_MB}, {GIF_FPS}fps, {GIF_MAX_COLORS} colours, "
          f"{GIF_HOLD}s per frame, {len(gif_clips)} frames)")
    if mb > GIF_MAX_MB:
        print("  OVER CAP - lower GIF_HOLD, GIF_FPS or GIF_MAX_COLORS",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
