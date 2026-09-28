---
layout: default
title: Transcripts
permalink: /transcripts/
description: Every machine transcript this archive holds, one page per capture, each naming the recording it transcribes, the capture file it came from and its word count.
last_modified_at: 2026-09-28
---
{%- comment -%}
  The transcript index (task 8d).

  Every number on this page is read out of _data/transcript_index.json, which
  scripts/build_collections.py :: build_transcripts() writes from the capture
  files it reads. Nothing here is typed, so the page cannot claim a count the
  data does not support.

  Grouping is by RECORDING, not by capture. A recording that was transcribed
  twice - once from its own upload and once from a duplicate upload that left
  the catalogue - appears once, with both of its transcripts listed. Two
  captures that have no surviving recording to belong to are listed at the
  end, under their own heading, with the reason.
{%- endcomment -%}
{%- assign ix = site.data.transcript_index -%}

<h1 class="page-title">Transcripts</h1>
<p class="page-subtitle">{{ ix.documents }} published transcripts of {{ ix.recordings }} recordings, {{ ix.words }} words of machine transcription.</p>
<p class="page-note">Every transcript on this site is machine-made. {{ ix.documents }} of them: one per capture file the archive holds, including {{ ix.alternate_captures }} that were taken from duplicate uploads which left the video catalogue and were re-parented onto the recording they duplicate, rather than being deleted. The capture files themselves are read, never rewritten &mdash; what is published here is a rendering of them, and the raw capture stays in the archive.</p>
<p class="transcript-disclaimer"><em>{{ ix.disclaimer }}</em></p>

{%- comment -%}
  Three buckets, decided from each document's `role`, never from position:
  a capture of a catalogued recording, a capture re-parented onto one, and a
  capture with no catalogued recording to belong to.
{%- endcomment -%}
{%- assign attached = 0 -%}{%- assign alternates = 0 -%}{%- assign orphans = 0 -%}
{%- for pair in ix.by_recording -%}
  {%- for d in pair[1] -%}
    {%- if d.role == "duplicate-upload" -%}{%- assign alternates = alternates | plus: 1 -%}
    {%- elsif d.recording_url == "" -%}{%- assign orphans = orphans | plus: 1 -%}
    {%- else -%}{%- assign attached = attached | plus: 1 -%}{%- endif -%}
  {%- endfor -%}
{%- endfor -%}

<div class="section">
  <div class="info-block">
    <h3>How to read these</h3>
    <ul>
      <li><strong>Transcripts of catalogued recordings</strong> &mdash; {{ attached }} capture{% if attached != 1 %}s{% endif %}. Each links to the recording it transcribes.</li>
      <li><strong>Additional transcripts of the same recording</strong> &mdash; {{ alternates }} capture{% if alternates != 1 %}s{% endif %} from uploads that left the catalogue as duplicates. Listed under the recording they duplicate, and never counted as separate recordings.</li>
      <li><strong>Preserved captures with no catalogued recording</strong> &mdash; {{ orphans }} capture{% if orphans != 1 %}s{% endif %}. The text is published rather than held in a file the site does not serve.</li>
    </ul>
    <p>Of the {{ ix.catalogued_videos }} videos in the catalogue,
    <strong>{{ ix.videos_attached }} carry an attached transcript</strong> and their pages link the text;
    {{ ix.videos_catalogue_only }} declare no transcript attached, and their pages say so in plain words and
    link nothing. Both figures are read from the archive's own transcript coverage data at build time.</p>
  </div>
</div>

{%- comment -%}
  2026-09-28. This list is grouped by RECORDING, which is the archive's counting
  unit and the right unit for a catalogue. It is the wrong unit for a reader who
  wants one session of one series, so the multi-part series the channel itself
  numbered now have pages of their own. The link sits at the top of the list,
  because a reader who arrives from a search for `understanding atheism session 3
  transcript` should not have to know this page exists first.
{%- endcomment -%}
<div class="info-block">
  <h3>Looking for one part of a series?</h3>
  <p>These {{ ix.documents }} documents are listed by recording, which is how the archive
  counts them. The {{ site.data.series.series_count }} multi-part series the channel
  numbered &mdash; <em>Understanding Atheism</em>, <em>iJihad</em>,
  <em>A Muslim&rsquo;s Guide to Science and Scientism</em>, <em>iKhalifa</em> and three more
  &mdash; have pages of their own, each listing its parts in the channel&rsquo;s order and
  linking straight to the transcript:
  <a href="{{ '/transcripts/by-series/' | relative_url }}">transcripts by series</a>.</p>
</div>

<h2>Transcripts of catalogued recordings</h2>
<p class="page-note">{{ attached }} capture{% if attached != 1 %}s{% endif %}, one per recording. Where a recording has more than one published transcript, they are listed together.</p>
<div class="card-grid">
{%- for pair in ix.by_recording -%}
{%- assign docs = pair[1] -%}
{%- assign own = nil -%}
{%- assign alts = 0 -%}
{%- for d in docs -%}
  {%- if d.role == "duplicate-upload" -%}{%- assign alts = alts | plus: 1 -%}
  {%- else -%}{%- assign own = d -%}{%- endif -%}
{%- endfor -%}
{%- if own and own.recording_url != "" -%}
  <div class="card">
    <h3><a href="{{ own.recording_url | relative_url }}">{{ own.title }}</a></h3>
    <div class="card-meta">
      upload <code>{{ own.capture_video_id }}</code> &middot; {{ own.source }} &middot; {{ own.lang }} &middot; {{ own.words }} words
    </div>
    <div class="card-tags">
      <span class="tag tag-topic">{{ own.paragraphs }} paragraphs</span>
      {% if own.role == "preserved-not-attached" %}<span class="tag tag-status">preserved capture, deliberately not attached to this entry</span>{% endif %}
      {% if alts > 0 %}<span class="tag tag-topic">+{{ alts }} further transcript{% if alts != 1 %}s{% endif %} of this recording</span>{% endif %}
    </div>
    <div class="card-actions">
      <a href="{{ own.url | relative_url }}" class="btn btn-primary btn-sm">Read the transcript</a>
      <a href="{{ own.recording_url | relative_url }}" class="btn btn-outline btn-sm">Recording page</a>
    </div>
  </div>
{%- endif -%}
{%- endfor -%}
</div>

<h2>Additional transcripts of the same recording</h2>
<p class="page-note">{{ alternates }} capture{% if alternates != 1 %}s{% endif %} taken from duplicate uploads. Each is an additional transcript of a recording already listed above &mdash; a different upload of the same talk &mdash; not a separate recording, and nothing is counted twice.</p>
<ul class="source-list">
{%- for pair in ix.by_recording -%}
{%- for d in pair[1] -%}
{%- if d.role == "duplicate-upload" -%}
  <li><a href="{{ d.url | relative_url }}">{{ d.title }}</a> &mdash; captured from upload
  <code>{{ d.capture_video_id }}</code>, {{ d.source }}, {{ d.lang }}, {{ d.words }} words.
  The recording it duplicates is
  {% if d.recording_url %}<a href="{{ d.recording_url | relative_url }}">{{ d.recording }}</a>{% else %}<code>{{ d.recording }}</code>{% endif %}.</li>
{%- endif -%}
{%- endfor -%}
{%- endfor -%}
</ul>

<h2>Preserved captures with no catalogued recording</h2>
<p class="page-note">These captures belong to uploads that are no longer catalogued entries in their own right. Their text is published here rather than left in a file the site does not serve. Nothing was deleted, and the uploads themselves remain in the archive's superseded-video ledger.</p>
<ul class="source-list">
{%- for pair in ix.by_recording -%}
{%- for d in pair[1] -%}
{%- if d.recording_url == "" and d.role != "duplicate-upload" -%}
  <li><a href="{{ d.url | relative_url }}">{{ d.title }}</a> &mdash; upload
  <code>{{ d.capture_video_id }}</code>, {{ d.source }}, {{ d.lang }}, {{ d.words }} words.
  {{ ix.role_notes[d.role] }}</li>
{%- endif -%}
{%- endfor -%}
{%- endfor -%}
</ul>

<div class="section">
  <div class="info-block">
    <h3>What a machine transcript is, and is not</h3>
    <p>Each capture is either a local Whisper transcription of the archived audio or a YouTube auto-caption file, and the page for each one names which. The text is published exactly as the machine wrote it, with no correction, no spell-checking and no smoothing: what is here is what was produced. Reading it as a record of what was said is legitimate; quoting it as an authority on what was said is not, which is why the same sentence appears above every transcript on this site.</p>
    <p>Paragraphs are the machine's own segmentation, taken from pauses of more than two seconds. There are no speaker labels, because neither capture source supplied reliable ones. Where a capture file is a YouTube rolling-window caption, the repeated window is dropped so each line is printed once; the words themselves are untouched, and the page for each transcript says exactly how its text was rendered.</p>
  </div>
</div>
