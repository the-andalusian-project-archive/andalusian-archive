#!/usr/bin/env python3
"""Transcript pipeline for video-stub articles (Plan B).

Part 1 -- sweep_captions(): yt-dlp --write-auto-subs --skip-download per
  YouTube id -> _data/transcript_coverage.json (FAST, minutes, no media).
Part 2 -- whisper_transcribe(): faster-whisper local transcription of gaps
  from Archive_org_videos/*.mp4 (SLOW, serial overnight; checkpointed).
Part 3 -- vtt_to_article_md(): caption/segment -> formatted markdown with
  provenance header, [mm:ss] paragraphs, ## section headings.

Usage:
  python scripts/transcribe.py --sweep
  python scripts/transcribe.py --whisper [--only ID1,ID2] [--model base]
  python scripts/transcribe.py --format [--only ID1,ID2]
"""

import csv
import json
import os
import pathlib
import re
import subprocess
import sys

BASE = pathlib.Path(__file__).parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VIDEOS_JSON = BASE / "_data" / "videos.json"
COVERAGE_JSON = BASE / "_data" / "transcript_coverage.json"
LOCAL_VIDEOS = BASE.parent / "Archive_org_videos"
TRANSCRIPTS_DIR = BASE / ".firecrawl" / "transcripts"

YTDLP = "yt-dlp"


def load_videos():
    return json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))


def sweep_captions():
    """Fetch auto-caption availability for all 68 ids (no media)."""
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    videos = load_videos()
    coverage = []
    for i, v in enumerate(videos):
        vid = v.get("id", "")
        row = {"video_id": vid, "title": v.get("title", ""),
               "captions": False, "lang": None, "lines": 0,
               "source": "none"}
        if not vid:
            coverage.append(row)
            continue
        print(f"[{i + 1}/{len(videos)}] {vid}")
        try:
            r = subprocess.run(
                [YTDLP, "--write-auto-subs", "--write-subs",
                 "--sub-langs", "en.*", "--skip-download",
                 "--sub-format", "vtt", "-o",
                 str(TRANSCRIPTS_DIR / f"cap-{vid}.%(ext)s"),
                 f"https://www.youtube.com/watch?v={vid}"],
                capture_output=True, text=True, timeout=120)
            vtts = sorted(TRANSCRIPTS_DIR.glob(f"cap-{vid}*.vtt"))
            if vtts:
                lines = sum(1 for _ in vtts[0].read_text(
                    encoding="utf-8", errors="replace").splitlines())
                row.update(captions=True, lang="en", lines=lines,
                           source="youtube-auto-captions",
                           file=vtts[0].name)
                for extra in vtts[1:]:
                    extra.unlink()
            else:
                for stale in TRANSCRIPTS_DIR.glob(f"cap-{vid}*"):
                    stale.unlink()
        except Exception as e:  # noqa: BLE001 - logged per-row
            row["error"] = f"{type(e).__name__}: {e}"
        coverage.append(row)
    COVERAGE_JSON.write_text(json.dumps(coverage, indent=2,
                                       ensure_ascii=False) + "\n",
                             encoding="utf-8")
    n = sum(1 for r in coverage if r["captions"])
    print(f"sweep: {n}/{len(coverage)} captioned -> {COVERAGE_JSON.name}")
    return 0


def whisper_transcribe(model="base", only=None, chunk_minutes=30):
    """Transcribe local MP4s lacking captions (serial, checkpointed).

    Long audio is split into chunk_minutes parts via ffmpeg; each part
    checkpoints independently (whisper-{id}.part{i}.json) so a kill loses
    at most one part. Parts merge into whisper-{id}.json on completion.
    """
    from faster_whisper import WhisperModel  # lazy: heavy import
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        coverage = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Run --sweep first.")
        return 1
    by_id = {r["video_id"]: r for r in coverage}
    videos = load_videos()
    if only:
        videos = [v for v in videos if v.get("id") in set(only)]
    print(f"Loading whisper model '{model}' (one-time download)...")
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    for i, v in enumerate(videos):
        vid, title = v.get("id", ""), v.get("title", "")
        if by_id.get(vid, {}).get("captions"):
            continue
        mp4 = LOCAL_VIDEOS / (v.get("filename", "") or "")
        if not mp4.exists():
            cands = sorted(LOCAL_VIDEOS.glob(f"*{vid}*.mp4"))
            mp4 = cands[0] if cands else None
        if mp4 is None or not mp4.exists():
            by_id.setdefault(vid, {}).update(
                whisper="missing_local_file")
            continue
        out = TRANSCRIPTS_DIR / f"whisper-{vid}.json"
        if out.exists():
            continue
        print(f"[{i + 1}/{len(videos)}] {title[:60]} "
              f"({mp4.stat().st_size / 1e9:.1f}GB)")
        parts = split_audio(mp4, vid, chunk_minutes)
        all_segs, lang = [], None
        for pi, (part_path, offset) in enumerate(parts):
            part_json = TRANSCRIPTS_DIR / f"whisper-{vid}.part{pi}.json"
            if part_json.exists():
                psegs = json.loads(part_json.read_text(
                    encoding="utf-8"))["segments"]
                print(f"  part {pi + 1}/{len(parts)} cached "
                      f"({len(psegs)} segs)")
            else:
                print(f"  part {pi + 1}/{len(parts)} transcribing...")
                segments, info = wm.transcribe(str(part_path), beam_size=5,
                                               vad_filter=True)
                psegs = [{"start": s.start + offset, "end": s.end + offset,
                          "text": s.text.strip()} for s in segments
                         if s.text.strip()]
                part_json.write_text(json.dumps(
                    {"video_id": vid, "part": pi, "segments": psegs},
                    ensure_ascii=False) + "\n", encoding="utf-8")
                lang = lang or info.language
            all_segs.extend(psegs)
        if lang is None:
            lang = "en"
        out.write_text(json.dumps(
            {"video_id": vid, "model": model, "chunked": len(parts) > 1,
             "language": lang, "segments": all_segs},
            ensure_ascii=False) + "\n", encoding="utf-8")
        by_id.setdefault(vid, {}).update(
            captions=True, lang=lang,
            lines=len(all_segs), source=f"whisper-{model}-local",
            file=out.name)
        COVERAGE_JSON.write_text(json.dumps(list(by_id.values()), indent=2,
                                           ensure_ascii=False) + "\n",
                                 encoding="utf-8")
        print(f"  -> {len(all_segs)} segments ({lang})")
    print("whisper pass done.")
    return 0


def split_audio(mp4, vid, chunk_minutes=30):
    """Split mp4 into chunk_minutes parts; returns [(path, offset_sec)]."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(mp4)], capture_output=True, text=True,
        timeout=60)
    try:
        duration = float(probe.stdout.strip())
    except ValueError:
        return [(mp4, 0.0)]
    chunk = chunk_minutes * 60
    if duration <= chunk * 1.2:
        return [(mp4, 0.0)]
    parts = []
    idx, offset = 0, 0.0
    while offset < duration:
        part = TRANSCRIPTS_DIR / f"chunk-{vid}.{idx}.mp4"
        if not part.exists():
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-ss", str(offset),
                 "-i", str(mp4), "-t", str(chunk), "-c", "copy",
                 str(part)], check=True, timeout=300)
        parts.append((part, offset))
        offset += chunk
        idx += 1
    return parts


def mmss(seconds):
    m, s = divmod(int(float(seconds)), 60)
    return f"{m:02d}:{s:02d}"


def load_segments(row):
    """Return [(start, text)] from a captions VTT or whisper JSON file."""
    path = TRANSCRIPTS_DIR / row.get("file", "")
    if not path.exists() or row.get("source", "").startswith("whisper"):
        if path.suffix == ".json" and path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return [(s["start"], s["text"]) for s in data["segments"]]
        return []
    # Minimal VTT parse: timestamp lines "-->", cue text follows.
    segs, cur_start, buf = [], None, []
    ts = re.compile(r"(\d+:)?(\d+):(\d+\.\d+)\s+-->")
    for line in path.read_text(encoding="utf-8",
                               errors="replace").splitlines():
        m = ts.search(line)
        if m:
            if buf and cur_start is not None:
                segs.append((cur_start, " ".join(buf)))
            h, mi, sec = m.group(1), m.group(2), m.group(3)
            cur_start = (int(h[:-1]) if h else 0) * 3600 + int(mi) * 60 \
                + float(sec)
            buf = []
        elif line.strip() and "WEBVTT" not in line \
                and not line.strip().isdigit() \
                and not line.startswith("Kind:") \
                and not line.startswith("Language:"):
            if "<" in line:
                line = re.sub(r"<[^>]+>", "", line)
            buf.append(line.strip())
    if buf and cur_start is not None:
        segs.append((cur_start, " ".join(buf)))
    # Dedupe consecutive repeats (auto-caption echo).
    out = []
    for start, text in segs:
        if not out or out[-1][1] != text:
            out.append((start, text))
    return out


def vtt_to_article_md(title, date, slug, video_url, duration, segments,
                      provenance):
    """Format segments as an honest machine-transcript article section."""
    paras, cur, cur_start, last_end = [], [], None, 0.0
    for start, text in segments:
        if cur_start is None:
            cur_start = start
        if start - last_end > 2.0 and cur:
            paras.append((cur_start, " ".join(cur)))
            cur, cur_start = [], start
        cur.append(text)
        last_end = start
    if cur:
        paras.append((cur_start, " ".join(cur)))
    lines = [
        f"> Transcript of [{title}]({video_url})"
        + (f" ({duration})" if duration else "")
        + ". Machine-generated "
        f"({provenance}) — errors likely; the summary above is human-written.",
        "",
    ]
    for k, (start, text) in enumerate(paras):
        if k % 12 == 0 and k:
            head = " ".join(text.split()[:6])
            lines.append(f"## {head}…")
            lines.append("")
        lines.append(f"[{mmss(start)}] {text}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    if "--sweep" in sys.argv:
        sys.exit(sweep_captions())
    if "--whisper" in sys.argv:
        only = None
        model = "base"
        for a in sys.argv:
            if a.startswith("--only="):
                only = a.split("=", 1)[1].split(",")
            if a.startswith("--model="):
                model = a.split("=", 1)[1]
        sys.exit(whisper_transcribe(model, only))
    print(__doc__)
