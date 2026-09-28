# Caption capture — 13 videos (2026-09-29)

Recovery of 13 videos verified absent from the archive (not in `_data/videos.json`,
68 rows; not in `.firecrawl/transcripts/`). Captions only. No media was downloaded.

**Outcome: 11 of 13 captured. 0 human-authored tracks — all 11 are auto-generated.
2 not captured (no caption track of any kind exists on YouTube for them).**

The raw captures are untracked working-tree files. Nothing was committed, nothing
in `_data/`, `_videos/`, `_transcripts/`, `_articles/`, `_papers/` or any `.md` file
was modified. Integration is the site owner's decision.

## 1. Method

One command, the pattern already in use in this repo, run once per video id:

```
yt-dlp --skip-download --write-sub --write-auto-sub --sub-langs "en.*,en" --sub-format vtt --no-warnings -o ".firecrawl/transcripts/cap-%(id)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEOID"
```

yt-dlp 2026.07.04 on Windows PowerShell 5.1.

Metadata (title, uploader, duration, `subtitles` / `automatic_captions` keys) was read
first with `yt-dlp --dump-json --skip-download` for all 13, so the human/auto question
was answered before any file was written. No variation of the capture command was
needed for the 11 successes. Two probes were run against the two failures
(`--list-subs`, and `--list-subs --extractor-args "youtube:player_client=web"`); see
section 3.

`--skip-download` held throughout. A recursive baseline of every `.mp4`, `.webm`,
`.m4a`, `.part`, `.mkv`, `.opus` file in the tree was taken before the first run (18
files) and re-taken after the last (18 files, zero new). Nothing to delete. yt-dlp
prints `Downloading 1 format(s): 136+251` on these subtitle-only runs; that is
format *selection* for the skipped media, not a transfer, and the file census
confirms no bytes landed.

One cleanup: `--sub-langs "en.*,en"` makes yt-dlp write two files per video when both
an `en-orig` and an `en` track exist. The 11 pairs were byte-identical (SHA-256
verified per file), so the 11 `cap-<id>.en.vtt` duplicates were deleted and the
`en-orig` originals kept. The repo convention is `.en-orig.vtt` and only that remains.

## 2. Per-video

Captions are **auto-generated in every successful case**. No human-authored English
track was found on any of the 13. The repo convention
`.firecrawl/transcripts/cap-<VIDEOID>.en-orig.vtt` was followed throughout.

| id | title (as YouTube gives it) | uploader | duration | caption kind | file | bytes | identifier screening |
|---|---|---|---|---|---|---|---|
| ywhiqBkoveA | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 8 | Hamza's Den | 05:02:32 | **none** | not written | 0 | not applicable |
| QoU02Om_wiQ | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 12 | Hamza's Den | 05:07:55 | auto | cap-QoU02Om_wiQ.en-orig.vtt | 2,635,686 | **yes** — see 2a |
| n3vhs1mcmVM | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 32 | Hamza's Den | 04:54:39 | auto | cap-n3vhs1mcmVM.en-orig.vtt | 2,333,511 | **yes** — see 2a |
| OHNMeqGMdPc | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 28 | Hamza's Den | 04:53:10 | auto | cap-OHNMeqGMdPc.en-orig.vtt | 2,425,010 | **yes** — see 2a |
| lE690yapgTA | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 22 | Hamza's Den | 04:38:13 | auto | cap-lE690yapgTA.en-orig.vtt | 2,342,899 | **yes** — see 2a |
| 3vXG_nXFWwM | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 18 | Hamza's Den | 04:20:05 | **none** | not written | 0 | not applicable |
| idz29r5LHig | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 14 | Hamza's Den | 03:47:53 | auto | cap-idz29r5LHig.en-orig.vtt | 1,913,236 | **yes** — see 2a |
| 7EqMJJuUKr8 | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 20 | Hamza's Den | 03:44:18 | auto | cap-7EqMJJuUKr8.en-orig.vtt | 1,911,751 | **yes** — see 2a |
| MCR3xh8wccQ | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 16 | Hamza's Den | 03:09:44 | auto | cap-MCR3xh8wccQ.en-orig.vtt | 1,664,926 | no (see 2b) |
| 0biKKRHO_Tk | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 24 | Hamza's Den | 03:07:30 | auto | cap-0biKKRHO_Tk.en-orig.vtt | 1,624,264 | **yes** — see 2a |
| 3vqVYfs5mCk | The Arena \| Challenge Islam \| Defend your Beliefs - Episode 29 | Hamza's Den | 05:40:45 | auto | cap-3vqVYfs5mCk.en-orig.vtt | 2,635,263 | **yes** — see 2a |
| kRCzZW3rg4U | "Yes, I'm leaving" Last Video of Asadullah Andalusi \|\| The Andalusian Project | Deen e Haq [Portal] | 00:18:18 | auto | cap-kRCzZW3rg4U.en-orig.vtt | 126,587 | **yes** — see 2a |
| M3nB154Mkuk | [VIDEO] Episode 93 - The Akh-Right, LGBTQ & Liberalism \| Asadullah Ali | Boys In The Cave | 02:18:09 | auto | cap-M3nB154Mkuk.en-orig.vtt | 1,330,900 | **yes** — see 2a |

### 2a. Correction to the brief's expectations

Two assumptions in the task did not survive checking, and both were confirmed
rather than assumed:

- **`ywhiqBkoveA` and `3vXG_nXFWwM` do not have human captions.** The brief expected
  human captions and no auto track. `--dump-json` shows `subtitles: {live_chat}` and
  `automatic_captions: {}` (empty) for both, and `--list-subs` prints `has no
  automatic captions` with `live_chat json` as the only entry. These are the two
  videos that produced no file. Live chat replay is a chat log, not a speech caption
  track, and is not a transcript.
- **`OHNMeqGMdPc` is auto-only, as expected.** It also has no `live_chat` entry, and
  its auto track is the only English one.

The human/auto split across the 13 is therefore 0 human, 11 auto, 2 none. Nothing here
changes the "prefer the human track" rule for future work; it simply never applied.

### 2b. Identifier screening

Screened all 11 captures for: the withheld birth name (via the repo's own
`build_collections.load_redaction_list` / `redaction_hits`, not a reimplementation),
given names, family-member names, places of residence, employers, phone numbers,
email addresses, and social handles.

**The withheld birth name does not appear in any of the 11 captures.** `redaction_hits`
returned 0 for every file. The three gitignored conversion-story captures remain the
only ones that carry it; these 13 do not join them on that ground.

Ten of the eleven do carry third-party personal identifiers. **Kinds only, as
requested — no identifier is reproduced here.** The captures are unedited.

| id | kinds found | representative lines |
|---|---|---|
| QoU02Om_wiQ | given name / nickname, relative's given name, place of residence (city-level) | 26383, 25919, 23439, 49271, 49295 |
| n3vhs1mcmVM | given name, given name of a child, third party's given name | 26519, 26535, 40191, 58271 |
| OHNMeqGMdPc | given name (repeated, a recurring speaker), place of residence (country-level), employer/sector, relative's given name, place of residence (city-level) | 3671, 10311, 17655, 20015, 33639, 37487 |
| lE690yapgTA | two given names, one a surname; relative's given name | 42287, 41383 |
| idz29r5LHig | given name, place of residence (US state and state-pair) | 23183, 43543, 43551 |
| 7EqMJJuUKr8 | a **full legal name** plus a self-chosen religious/street name, and a given name; references to posting an email address (no address itself captured) | 1679, 1687, 24983, 39351 |
| MCR3xh8wccQ | none beyond kinship terms ("my wife", "my son") with no names | — |
| 0biKKRHO_Tk | a **full personal name**, employer sector, place of residence (country) | 2527, 7703, 40463 |
| 3vqVYfs5mCk | a chosen handle/abbreviation, place of residence (two countries) | 40255, 58231, 59007 |
| kRCzZW3rg4U | **a full personal name of a named third party singled out and criticised by name**, plus a moderator's full name, plus public figures named critically | 00:10:45, 00:16:48 |
| M3nB154Mkuk | the speaker's own chosen name change (stated on the record), kinship terms with no names | 9183, 9194, 9407, 9415 |

Notes on the sharpest cases:

- **`7EqMJJuUKr8`** (L1679/L1687) — a participant states a religious name on air and
  then explicitly says which is their legal name. Both are spoken, so both are in the
  capture. This is the single clearest full-legal-name disclosure in the set.
- **`0biKKRHO_Tk`** (L2527) — a participant gives a full personal name on air, and at
  L7703 states their employer sector. L40463 gives a country of origin.
- **`kRCzZW3rg4U`** (00:10:45) — the site owner names a specific individual in the
  community and criticises him by full name, at length, in the closing third of the
  video. A chat moderator is thanked by full name at 00:16:48. Public figures are also
  named critically. This is the highest-sensitivity capture in the set and the closest
  in character to the conversion-story videos already withheld under `.gitignore`,
  though it is a different kind of material: the names here are people he is criticising,
  not his own family or birth name.
- **`M3nB154Mkuk`** (L9183–L9415) — the speaker announces a name change on air. No
  previous or legal name is spoken, so the capture does not defeat the birth-name
  withholding. Flagged because it is adjacent to that question.
- **`3vqVYfs5mCk`** (L40255) — a participant gives a two-letter handle, and two
  countries of origin are stated (L58231, L59007).

Screening method and its limits are in section 4. The short video
(`kRCzZW3rg4U`, 1,344 distinct cues) was additionally read in full rather than only
pattern-matched.

No email address, phone number or social-media handle was captured in any of the 11.
Email *addresses* are discussed at `idz29r5LHig` (L18503–L18607) and `7EqMJJuUKr8`
(L39351) but the addresses themselves are not spoken into the captions. A loose
phone-number regex produced 33 hits across 5 files; every one was inspected by hand
and all 33 are false positives — population figures, verse references, year ranges and
ASR artefacts (e.g. "200 000", "1698-100", "369 369"). Not reported as identifiers.

## 3. Failures

Two videos could not be captured. Neither failure is a bot-detection block, a rate
limit, or a permissions problem — **no access control was encountered or worked
around.** Both videos have no caption track published on YouTube, so there is nothing
to fetch.

### ywhiqBkoveA — The Arena, Episode 8 — NOT CAPTURED

Exact output:

```
[youtube] ywhiqBkoveA: Downloading webpage
[youtube] ywhiqBkoveA: Downloading android vr player API JSON
[info] ywhiqBkoveA: Downloading 1 format(s): 136+251
[info] There are no subtitles for the requested languages
```

yt-dlp exits 0. It is a soft failure: the run "succeeds" and writes nothing.

What I tried:
1. `--dump-json --skip-download` — metadata read fine, so the video is live and public.
   `subtitles: {live_chat}`, `automatic_captions: {}`.
2. The standard capture command — "There are no subtitles for the requested languages".
3. `--list-subs` — "ywhiqBkoveA has no automatic captions"; the only row is
   `live_chat  json`.
4. `--list-subs --extractor-args "youtube:player_client=web"` — identical result via a
   second extractor client, ruling out a client-specific gap.

Conclusion: no English caption track exists, human or auto. `live_chat` is a chat
replay log in JSON, not a speech transcript, so it is not a substitute and I did not
capture it. A transcript of this episode would have to come from audio, which is out
of scope here and would mean downloading media.

### 3vXG_nXFWwM — The Arena, Episode 18 — NOT CAPTURED

Identical failure and identical diagnosis. Exit 0, "There are no subtitles for the
requested languages". `subtitles: {live_chat}`, `automatic_captions: {}`; `--list-subs`
on both the android-vr and web clients reports no automatic captions and lists only
`live_chat  json`.

## 4. Honest limits

- **All 11 captures are auto-generated ASR, and they read like it.** Lower-cased
  throughout, heavy false starts, no punctuation, rolling repeated cues. `OHNMeqGMdPc`
  is the outlier: it preserves capitalisation and is markedly cleaner. Treat these as
  rough evidence, not publishable prose; the same treatment the existing whisper
  transcripts in this directory receive would apply.
- **Speaker attribution is absent.** These are unlabelled speech tracks. I inferred
  who was speaking from context for screening purposes only, and those inferences are
  not reliable enough to publish. Several rows in 2b mix the site owner with
  participants because the captions do not distinguish them. If you need to know
  *who* said a given name, that requires a diarisation pass this capture did not do.
- **Identifier screening is pattern-based plus targeted reading, not exhaustive.** I
  checked the withheld birth name through the repo's own `redaction_hits`, then swept
  for name/kinship/residence/employer/email/phone/handle patterns and read the context
  around every hit. That reliably catches the classes listed and will not reliably
  catch, for example, a surname spoken without a given name, or a place named
  obliquely. Auto-ASR mangles names into near-homophones, so a name can be present in
  the audio and unrecognisable in the text — and equally, a garbled string can look
  like a name when it is not. Treat 2b as a floor, not a ceiling.
- **Two videos are simply not recoverable this way.** Episodes 8 and 18 have no
  caption track. If those episodes matter, the options are a different transcript
  source, or audio transcription — and the latter is a media download, which this task
  excluded and which the author's wishes point away from.
- **No transcript derivation was attempted.** Per the brief, the raw `.vtt` files are
  the whole deliverable. Integration into `_data/videos.json` and `_transcripts/` is
  yours, and the gitignore decision for any of the 10 files carrying third-party
  identifiers is yours too.
- **Nothing is committed.** The 11 files are untracked (`??`) in the working tree. A
  blanket `git add -A` would publish all ten identifier-bearing captures. The
  `.gitignore` rules for the three existing withheld captures do not cover any of
  these.
- **The two probe runs on the failures were not attempts to defeat access control.**
  `--extractor-args "youtube:player_client=web"` is yt-dlp's ordinary way of asking a
  second official API surface the same public question, to rule out a client-specific
  gap. It returned the same answer, and I stopped there. No proxy, no account
  rotation, no challenge bypass.

## Files written

Captures (11, untracked, unedited):
`.firecrawl/transcripts/cap-{QoU02Om_wiQ,n3vhs1mcmVM,OHNMeqGMdPc,lE690yapgTA,idz29r5LHig,7EqMJJuUKr8,MCR3xh8wccQ,0biKKRHO_Tk,3vqVYfs5mCk,kRCzZW3rg4U,M3nB154Mkuk}.en-orig.vtt`

This report (1): `docs/recovery-log/2026-09-29-caption-capture.md`

No other file was created, modified or deleted. No media on disk.
