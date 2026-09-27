---
layout: default
title: "Transcripts by series"
permalink: /transcripts/by-series/
description: "The archive's machine transcripts grouped into the multi-part lecture and discussion series the channel itself numbered: Understanding Atheism, iJihad, A Muslim's Guide to Science and Scientism, iKhalifa, and three more, each with its parts and full transcripts."
last_modified_at: 2026-09-28
---
{%- comment -%}
  The series index (2026-09-28).

  This page exists because the archive's most unique asset - {{ ix.words }} words
  of transcript text that exist nowhere else - was a flat list of 68 documents,
  so a reader searching for the third session of a series had nothing to land on.
  Each series now has a page of its own with its parts in the channel's order.

  THE GROUPING IS NOT THE `themes` FIELD, and saying why on the page is part of
  the page. `_data/videos.json` carries `themes`, `topics` and `tone` on every
  row and they look like a topic taxonomy, but
  `scripts/generate_video_themes.py` produced them with a first-match-wins
  substring test over ten keywords: the single largest theme bucket on those rows is
  the classifier's own `default` branch, which is not a subject, and all six sessions
  of Understanding Atheism land in it alongside unrelated short talks. Grouping on it
  would have produced a topical index that was an artefact of a keyword list.
  Neither `_data/transcript_index.json` nor `_data/transcript_coverage.json`
  carries a topic or series key at all.

  What does support grouping is the channel's own title shape - `NN - <series
  name>` - which is preserved verbatim in the recording titles and is recovered
  evidence rather than an editorial label. `scripts/build_series_index.py` holds
  the rules and re-derives the result with `--check`.

  The recordings that match no series rule are NOT filed under an invented one.
  Saying so, with the count, is the honest version of this page.
{%- endcomment -%}
{%- assign sx = site.data.series -%}
{%- assign ix = site.data.transcript_index -%}
{%- assign videos_total = 0 -%}{%- for v in site.data.videos -%}{%- assign videos_total = videos_total | plus: 1 -%}{%- endfor -%}

<h1 class="page-title">Transcripts by series</h1>
<p class="page-subtitle">{{ ix.documents }} published transcripts, {{ ix.words }} words, in {{ sx.series_count }} recorded series covering {{ sx.grouped_videos }} of the {{ ix.recordings }} recordings.</p>
<p class="transcript-disclaimer"><em>{{ ix.disclaimer }}</em></p>

<div class="info-block">
  <h3>Why this page exists</h3>
  <p>These transcripts are the one part of this corpus that exists nowhere else. His channel
  reads &ldquo;not available&rdquo;; the institutions that republished some of his work host
  descriptions and embeds, not text. Until this page, the only way in was a flat list of
  {{ ix.documents }} documents, which is useless to a reader who wants session three of
  something and does not know the archive has it. The series below are the channel&rsquo;s
  own multi-part runs, with each part&rsquo;s transcript linked directly.</p>
  <p class="page-note">A series is a <strong>view</strong> over recordings that are already
  catalogued once each in <a href="{{ '/videos/' | relative_url }}">the video
  archive</a>. Nothing here is counted twice and nothing here adds to the archive&rsquo;s
  published total.</p>
</div>

<h2>The {{ sx.series_count }} series</h2>

<div class="card-grid">
{%- for s in sx.series %}
  {%- assign with_tr = 0 -%}{%- for p in s.parts -%}{%- if p.transcript_url != "" -%}{%- assign with_tr = with_tr | plus: 1 -%}{%- endif -%}{%- endfor %}
  <div class="card">
    <h3><a href="{{ '/transcripts/by-series/' | append: s.slug | append: '/' | relative_url }}">{{ s.title | escape }}</a></h3>
    <div class="card-meta">{{ s.part_count }} parts &middot; {{ with_tr }} with published transcripts &middot; {{ s.transcript_words }} words</div>
    <div class="card-body">{{ s.framing | escape }}</div>
    <div class="card-actions">
      <a href="{{ '/transcripts/by-series/' | append: s.slug | append: '/' | relative_url }}" class="btn btn-primary btn-sm">Parts and transcripts</a>
    </div>
  </div>
{%- endfor %}
</div>

<h2>What is not in a series</h2>
<p><strong>{{ sx.ungrouped_videos }} of the {{ videos_total }} catalogued recordings are
not parts of a series</strong>, and this archive does not file them under an invented one.
They are single talks, one-off debates, appearances on other people&rsquo;s channels,
translated excerpts and re-uploads. Every one of them is catalogued, and
{{ ix.videos_attached }} of the {{ videos_total }} catalogued entries carry an attached
transcript &mdash; all of them are on
<a href="{{ '/transcripts/' | relative_url }}">the full transcript list</a> and in
<a href="{{ '/videos/' | relative_url }}">the video catalogue</a>.</p>
<p class="page-note">{{ sx.ungrouped_note }}</p>

<div class="section">
  <div class="info-block">
    <h3>How the grouping was decided, and what it is not</h3>
    <p>{{ sx.grouping_signal | escape }}</p>
    <p>Two consequences are worth stating plainly. First, a series needs two or more parts:
    a rule that matched a single recording is rejected by the script rather than
    published as a series of one. Second, where the channel skipped a number or closed a
    title with a different label, that is what the series page prints &mdash; this archive
    does not renumber anything to make a series look tidier than it was.</p>
    <p class="meta">Rule and provenance: <code>_data/series.json</code>, generated by
    <code>scripts/build_series_index.py</code> and re-checkable with
    <code>python scripts/build_series_index.py --check</code>.</p>
  </div>
</div>

<p class="page-note">For who the author is and every form of his name, see
<a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}">the entity page</a>. For what
happened to the channel these recordings came from, see
<a href="{{ '/channel/' | relative_url }}">the channel record</a> and
<a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what happened to the
Andalusian Project&rsquo;s web presence</a>.</p>
