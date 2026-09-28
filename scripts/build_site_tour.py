#!/usr/bin/env python3
"""Cut the site tour from captured frames. Dark mode, 2026-09-28.

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

INPUT   _staging/demo-tour/NN-name.png   1440x900, captured in dark mode
OUTPUT  docs/demo/site-tour.mp4          1440x900, 30 fps
        docs/demo/site-tour.gif          800x500, 8 fps, under 8 MB

Usage: python scripts/build_site_tour.py [--mp4-only] [--gif-only]
Requires: ffmpeg on PATH, Pillow.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMES = ROOT / "_staging" / "demo-tour"
OUT = ROOT / "docs" / "demo"
WORK = ROOT / "_staging" / "demo-tour-work"

# Every caption is checked against _data/ before it is burned in. The figures
# here are the ones the site computes; nothing is typed that the site derives.
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

HOLD = 3.0          # seconds each frame is held
XFADE = 0.55        # dissolve between frames
FPS = 30
GIF_FPS = 8
GIF_MAX_MB = 8.0

# Dark-theme ink. The frames are dark, so the caption plate has to be a light
# text on a dark scrim, and the title/end cards are built on the same surface
# as the site rather than as white slides.
FG = "0xE5E7EB"
DIM = "0x9CA3AF"
ACCENT = "0x60A5FA"

# drawtext parses its own options, so a Windows drive colon has to be escaped
# AND the whole path quoted, or C: is read as a filter name.
FONT = "'C\\:/Windows/Fonts/segoeui.ttf'"
FONT_BOLD = "'C\\:/Windows/Fonts/segoeuib.ttf'"


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-2500:] + "\n")
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:4])}...")


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


def title_card(text: str, sub: str, out: pathlib.Path) -> None:
    """A title or end card, drawn on the site's own dark surface."""
    vf = (
        f"drawbox=x=0:y=0:w=iw:h=ih:color=0x0F1117:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:text='{text}':fontcolor={FG}"
        f":fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2-40,"
        f"drawtext=fontfile={FONT}:text='{sub}':fontcolor={DIM}"
        f":fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2+50"
    )
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F1117:s=1440x900:d=3.2",
        "-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out),
    ])


def frame_clip(src: pathlib.Path, caption: str, z_out: float, z_in: float,
               dur: float, out: pathlib.Path) -> None:
    """One frame: scale up, Ken Burns, caption plate, output a silent clip."""
    frames = int(dur * FPS)
    # 2880x1800 then down to 1440x900 gives zoompan the headroom it needs to pan
    # without resampling artefacts.
    vf = (
        f"scale=2880:1800:flags=lanczos,"
        f"zoompan=z='if(eq(on,0),{z_out},{z_in})'"
        f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={frames}:s=1440x900:fps={FPS},"
        f"drawbox=x=0:y=h-150:w=iw:h=150:color=0x0F1117@0.92:t=fill,"
        f"drawbox=x=0:y=h-6:w=iw:h=6:color={ACCENT}:t=fill,"
        f"drawtext=fontfile={FONT}:text='{re.sub(chr(39), '', caption)}'"
        f":fontcolor={FG}:fontsize=34:x=70:y=h-98"
    )
    run([
        "ffmpeg", "-y", "-loop", "1", "-t", f"{dur}", "-i", str(src),
        "-vf", vf, "-r", str(FPS), "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", str(out),
    ])


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

    WORK.mkdir(parents=True, exist_ok=True)
    clips: list[pathlib.Path] = []

    if not args.gif_only:
        head = WORK / "00-title.mp4"
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
        inputs: list[str] = []
        for c in clips:
            inputs += ["-i", str(c)]
        chains = []
        prev = "[0:v]"
        for i in range(1, len(clips)):
            label = f"[v{i}]"
            offset = HOLD - XFADE * i
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
        print(f"\nMP4  {mp4.name}  {mp4.stat().st_size / 1e6:.2f} MB")

    # ---- GIF: one frame per section, two-pass palette, under the cap ------
    gif_src = WORK / "gif.mp4"
    run([
        "ffmpeg", "-y", *sum([["-i", str(c)] for c in clips], []),
        "-filter_complex",
        "[0:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[a];"
        "[3:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[b];"
        "[5:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[c];"
        "[6:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[d];"
        "[7:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[e];"
        "[9:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[f];"
        "[11:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[g];"
        "[12:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[h];"
        "[13:v]trim=start=1.2:end=1.2+0.6,setpts=PTS-STARTPTS[i];"
        "[14:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[j];"
        "[15:v]trim=start=1.2:end=1.8,setpts=PTS-STARTPTS[k];"
        "[a][b][c][d][e][f][g][h][i][j][k]concat=n=11:v=1:a=0[out]",
        "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", str(gif_src),
    ])
    gif = OUT / "site-tour.gif"
    run([
        "ffmpeg", "-y", "-i", str(gif_src),
        "-vf", f"fps={GIF_FPS},scale=800:-1:flags=area,split[a][b];"
               f"[a]palettegen=stats_mode=diff:max_colors=256[p];"
               f"[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
        str(gif),
    ])
    mb = gif.stat().st_size / 1e6
    print(f"GIF  {gif.name}  {mb:.2f} MB  (cap {GIF_MAX_MB})")
    if mb > GIF_MAX_MB:
        print("  OVER CAP - lower GIF_FPS or drop a segment", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
