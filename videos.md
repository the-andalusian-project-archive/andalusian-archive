---
layout: default
title: Video Archive
description: Every recording of the Andalusian Project that this archive has catalogued, with the archived file where one exists, the source it survives at where one does not, and its themes and topics.
last_modified_at: 2026-09-28
---
{%- comment -%}
  Counts are computed from _data/videos.json and _data/transcript_coverage.json
  at build time. The source label follows the entry's real source, not a
  snapshot: I5 (review-phase2) found that 12 catalogue-only entries carry a
  YouTube URL in `archive_url`, so a card labelled "Archive.org" was sending
  readers to YouTube.
{%- endcomment -%}
{%- assign total = 0 -%}{%- assign on_archive = 0 -%}{%- assign youtube_only = 0 -%}
{%- assign a_videos = 0 -%}{%- assign c_videos = 0 -%}
{%- assign transcribed = 0 -%}{%- assign no_transcript = 0 -%}{%- assign with_alternates = 0 -%}
{%- comment -%}
  a_produced_certain is the M1 count: category A minus the one entry whose own
  byline evidence is recorded as unverified (G47Stp3pLss, category_basis on its
  row and on its own page). It is only used for the caveat clause, never for a
  total, so the count a reader reads is still the whole category.
{%- endcomment -%}
{%- assign a_unverified = 0 -%}
{%- for v in site.data.videos -%}
  {%- assign total = total | plus: 1 -%}
  {%- if v.archive_url contains "youtube.com" or v.archive_url contains "youtu.be" -%}
    {%- assign youtube_only = youtube_only | plus: 1 -%}
  {%- else -%}
    {%- assign on_archive = on_archive | plus: 1 -%}
  {%- endif -%}
  {%- if v.category == "A" -%}{%- assign a_videos = a_videos | plus: 1 -%}{%- endif -%}
  {%- if v.category == "C" -%}{%- assign c_videos = c_videos | plus: 1 -%}{%- endif -%}
  {%- if v.category_basis -%}{%- assign a_unverified = a_unverified | plus: 1 -%}{%- endif -%}
  {%- assign cov = site.data.transcript_coverage | where: "video_id", v.id | first -%}
  {%- if v.transcripts == 0 -%}
    {%- assign no_transcript = no_transcript | plus: 1 -%}
  {%- elsif cov and cov.captions -%}
    {%- assign transcribed = transcribed | plus: 1 -%}
  {%- endif -%}
  {%- if cov and cov.alternates -%}{%- assign with_alternates = with_alternates | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign a_produced_certain = a_videos | minus: a_unverified -%}

<h1 class="page-title">Video Archive</h1>
<p class="page-subtitle">{{ total }} videos: {{ a_videos }} he produced, {{ c_videos }} he appeared in on other people's channels.</p>
<p class="page-note">{{ on_archive }} are archived on the <a href="https://archive.org/details/andalusian-project" rel="noopener noreferrer">Internet Archive</a>; {{ youtube_only }} survive only as YouTube uploads and are labelled YouTube below, because that is where they are. {{ transcribed }} carry a machine transcript; {{ no_transcript }} do not have one attached. Mirrors of the same recording are counted once, under the entry you are reading. Theme descriptions use neutral academic language for research purposes.</p>

<div class="card-grid">
{% for video in site.data.videos %}
{%- assign cov = site.data.transcript_coverage | where: "video_id", video.id | first -%}
  <div class="card">
    <h3>{{ video.title }}</h3>
    <div class="card-meta">
      {% if video.format %}{{ video.format }}{% endif %}
      {% if video.size_bytes %} &middot; {{ video.size_bytes | divided_by: 1048576.0 | round: 1 }} MB{% endif %}
      {% if video.source %} &middot; {{ video.source }}{% endif %}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=video.category %}
      {% if video.kind %}<span class="tag tag-format">{{ video.kind }}</span>{% endif %}
      {% if video.transcripts == 0 %}
        {%- comment -%} Neutral, and it promises nothing. {%- endcomment -%}
        <span class="tag tag-status">Transcript not yet available</span>
      {% elsif cov and cov.captions %}
        <span class="tag tag-topic">Transcript &middot; {{ cov.lines }} lines, {{ cov.lang }}</span>
        {%- if cov.alternates %}<span class="tag tag-topic">+{{ cov.alternates.size }} further transcript{% if cov.alternates.size != 1 %}s{% endif %} of this recording</span>{% endif %}
      {% else %}
        <span class="tag tag-status">No transcript in the archive</span>
      {% endif %}
      {% for theme in video.themes %}
        <span class="tag tag-theme">{{ theme }}</span>
      {% endfor %}
      {% for topic in video.topics %}
        <span class="tag tag-topic">{{ topic }}</span>
      {% endfor %}
    </div>
    <div class="card-body">
      Tone: {{ video.tone }}
    </div>
    <div class="card-actions">
      {%- comment -%}
        I5 (review-phase2): this button used to be labelled "Archive.org" for
        every card, but for the catalogue-only entries archive_url is a YouTube
        watch URL, so 12 cards sent a reader to YouTube under an Archive.org
        label. The label now follows the actual source. build_collections.py
        pins the population of the non-archive branch (it is exactly the set of
        entries carrying `kind`).
      {%- endcomment -%}
      {% assign is_youtube = false %}
      {% if video.archive_url contains "youtube.com" or video.archive_url contains "youtu.be" %}
        {% assign is_youtube = true %}
      {% endif %}
      {% if is_youtube %}
        <a href="{{ video.archive_url | uri_escape | replace: '#', '%23' }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">YouTube{% if video.kind %} ({{ video.kind }}, not archived){% endif %}</a>
      {% else %}
        <a href="{{ video.archive_url | uri_escape | replace: '#', '%23' }}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">Archive.org</a>
      {% endif %}
      {% if video.youtube_url %}
        <a href="{{ video.youtube_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">YouTube</a>
      {% endif %}
      <a href="{{ '/videos/' | relative_url }}{{ video.id }}/" class="btn btn-outline btn-sm">Page</a>
    </div>
  </div>
{% endfor %}
</div>

<div class="section">
  <div class="info-block">
    <h3>About This Collection</h3>
    <p>{{ a_videos }} of the {{ total }} videos were produced by The Andalusian Project. One of those {{ a_videos }} rests on an unverified byline and is counted with them only because the evidence does not settle it either way, so the number that rests on a settled byline is {{ a_produced_certain }}; that entry&rsquo;s own page carries the evidence and the reason. The remaining {{ c_videos }} are recordings of his appearances on other people&rsquo;s channels &mdash; debates organised by the Muslim Debate Initiative, and translated or clipped excerpts of those appearances &mdash; catalogued so they are findable, and kept out of the count of what he produced. A talk he gave at another organisation&rsquo;s hall is one of the {{ a_videos }}, not one of the {{ c_videos }}: the test is who made the recording, and he made that one. A debate he produced is here for the same reason, whatever format it took.</p>
    <p>The original channel held lectures, debates and discussions on Islamic philosophy, theology and contemporary issues. Its videos were removed around October 2022 &mdash; the channel itself was not deleted: the same channel id continued to exist afterwards, showed a different set of items under a different handle in 2023, and is reported as unavailable by the last live check, so it is not linked from here. The full record, with the capture dates behind every step of it and the claims this archive refuses to make about it, is on the <a href="{{ '/channel/' | relative_url }}">channel history page</a>.</p>
    <h3>Transcripts</h3>
    <p>{{ transcribed }} recordings carry a machine transcript; every transcript on this site carries the same caveat: it is machine-generated, its accuracy is imperfect, and it should not be used in polemics or debate material as an authoritative source. The transcript text is published, not just marked: every capture the archive holds has its own page under <a href="{{ '/transcripts/' | relative_url }}">Transcripts</a>, and each video page links its own. {{ with_alternates }} recordings carry further transcripts taken from duplicate uploads that left the catalogue: those transcripts were re-parented onto the surviving recording and kept, not deleted, and each is published as an additional transcript of that recording. {{ no_transcript }} entries have no transcript attached, and the archive does not say when one will arrive.</p>
    <h3>Theme Description Policy</h3>
    <p>To prevent misinterpretation and prejudice, video descriptions use neutral academic language:</p>
    <ul>
      <li>Themes describe subject areas without revealing specific arguments</li>
      <li>Topics use standard academic categorizations</li>
      <li>Tone indicates presentation format (lecture, dialogue, etc.)</li>
    </ul>
  </div>
</div>
