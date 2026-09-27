---
layout: default
title: Timeline
description: How The Andalusian Project archive was recovered, in dated order from the first honest count to the final totals, followed by the recovered works in the order they were published.
---

{%- comment -%}
  This page has two dated sections and every figure in both is computed from
  `_data/`.

  The first is the recovery narrative - what the archive knew at each date and
  what changed it. Its dates are the dates the repository itself records: the
  2026-09-06 honest-counts plan, the 2026-09-07 canonical Wayback fetch, the
  2026-09-08 junk purge, the 2026-09-27 recovery run, and the 2026-09-28
  recount. None is invented. The counts on the earlier entries are the counts
  that were true on that date, which is why some of them are smaller than the
  ones below; the last entry is the present state.

  The second section is the recovered corpus by the author's own publication
  dates, which is what this page carried before the recovery narrative was added
  and is unchanged by it.

  2026-09-27 (task 8f, Phase-3 review I6): this page used to say "Original
  YouTube channel deleted/privatized", which `rejected_claims[1]` in
  `_data/channel_facts.json` refines and the videos page and README already
  state: the videos were removed around October 2022; the channel id continued
  to exist, was captured through 2026-08-19, showed different items under a
  different handle in 2023, and reads "not available" at the 2026-09-27 check.
  That row still says that, and still links the record that carries the
  captures.
{%- endcomment -%}

{%- assign works_total = 0 -%}{%- assign found = 0 -%}{%- assign wayback_only = 0 -%}{%- assign lost = 0 -%}
{%- for w in site.data.canonical_works -%}
  {%- assign works_total = works_total | plus: 1 -%}
  {%- if w.status == "found" -%}{%- assign found = found | plus: 1 -%}
  {%- elsif w.status == "wayback_only" -%}{%- assign wayback_only = wayback_only | plus: 1 -%}
  {%- elsif w.status == "lost" -%}{%- assign lost = lost | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign videos_total = 0 -%}{%- assign archive_files = 0 -%}{%- for v in site.data.videos -%}
  {%- assign videos_total = videos_total | plus: 1 -%}
  {%- if v.archive_org_id -%}{%- assign archive_files = archive_files | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign papers_total = 0 -%}{%- assign pdf_files = 0 -%}{%- for p in site.data.papers -%}
  {%- assign papers_total = papers_total | plus: 1 -%}
  {%- if p.file -%}{%- assign pdf_files = pdf_files | plus: 1 -%}{%- endif -%}
  {%- if p.additional_files -%}{%- assign pdf_files = pdf_files | plus: p.additional_files.size -%}{%- endif -%}
{%- endfor -%}
{%- assign mdi_total = 0 -%}{%- assign mdi_counted = 0 -%}{%- assign mdi_words = 0 -%}
{%- for m in site.data.mdi_articles -%}
  {%- assign mdi_total = mdi_total | plus: 1 -%}
  {%- if m.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}
  {%- assign mdi_words = mdi_words | plus: m.words | default: 0 -%}
{%- endfor -%}
{%- assign mdi_republished = mdi_total | minus: mdi_counted -%}
{%- assign notices_total = 0 -%}{%- for n in site.data.notices -%}{%- assign notices_total = notices_total | plus: 1 -%}{%- endfor -%}
{%- assign linkouts_total = 0 -%}{%- for l in site.data.linkouts -%}{%- assign linkouts_total = linkouts_total | plus: 1 -%}{%- endfor -%}
{%- assign yaqeen_total = 0 -%}{%- for y in site.data.yaqeen_papers -%}{%- assign yaqeen_total = yaqeen_total | plus: 1 -%}{%- endfor -%}
{%- assign albalagh_total = 0 -%}{%- for ab in site.data.albalagh_courses -%}{%- assign albalagh_total = albalagh_total | plus: 1 -%}{%- endfor -%}
{%- assign interviews_total = 0 -%}{%- for ei in site.data.external_interviews -%}{%- assign interviews_total = interviews_total | plus: 1 -%}{%- endfor -%}
{%- assign captures_total = 0 -%}{%- for b in site.data.blog_posts -%}{%- assign captures_total = captures_total | plus: 1 -%}{%- endfor -%}
{%- assign superseded_total = 0 -%}{%- for s in site.data.superseded_videos -%}{%- assign superseded_total = superseded_total | plus: 1 -%}{%- endfor -%}
{%- assign secondary_total = 0 -%}{%- for s in site.data.secondary_sources -%}{%- assign secondary_total = secondary_total | plus: 1 -%}{%- endfor -%}
{%- assign recovery_rows = 0 -%}{%- for r in site.data.recovery_log -%}{%- assign recovery_rows = recovery_rows | plus: 1 -%}{%- endfor -%}
{%- assign ix = site.data.transcript_index -%}
{%- assign total_content = works_total | plus: videos_total | plus: papers_total | plus: mdi_counted | plus: yaqeen_total | plus: albalagh_total | plus: interviews_total -%}

<h1 class="page-title">Timeline</h1>
<p class="page-subtitle">Two histories: how this archive was recovered, and the works it recovered, in the order they were published.</p>

<h2 id="recovery">How the archive was recovered</h2>
<p class="page-note">Each entry states the counts as they stood on that date. Some of them are smaller than the ones below, and that is the point: the earlier figures are what the archive actually held when they were true, not a second opinion about the present. The last entry is the current state, and every figure in it is counted from <code>_data/</code> when this page is built.</p>

<div class="timeline">

  <div class="timeline-group">
    <h2>2026-09-06 &mdash; the first honest count</h2>
    <div class="timeline-item">
      <div class="timeline-date">September 6</div>
      <div class="timeline-title">The archive stops counting Wayback captures and starts counting works. The baseline this date produced is the one every later entry is measured against: <strong>57 works</strong> (30 full-text, 25 Wayback-only, 2 lost), <strong>68 videos</strong>, <strong>18 papers</strong>, and a published total of <strong>203</strong> &mdash; read from 87 CDX capture records, which are metadata and were never counted as works. <a href="{{ '/channel/' | relative_url }}">The channel record</a> and the <a href="{{ '/articles/' | relative_url }}">works index</a> were built on that basis.</div>
    </div>
  </div>

  <div class="timeline-group">
    <h2>2026-09-07 &mdash; the canonical fetch</h2>
    <div class="timeline-item">
      <div class="timeline-date">September 7</div>
      <div class="timeline-title">The works held at that date &mdash; the 57 of the previous entry &mdash; are re-fetched one canonical URL at a time, and the Al Balagh course list is de-duplicated by canonical URL to {{ albalagh_total }} rows. This is the date the recovered text in this archive is from; the works themselves are dated 2011&ndash;2020.</div>
    </div>
  </div>

  <div class="timeline-group">
    <h2>2026-09-08 &mdash; the junk purge</h2>
    <div class="timeline-item">
      <div class="timeline-date">September 8</div>
      <div class="timeline-title">Navigation shells, tag pages and other non-post captures are removed from the corpus and kept as the {{ captures_total }} capture records they are. The distinction between a <em>work</em> and a <em>capture</em> is what makes the 57 figure meaningful, and it is why the capture count is quoted separately everywhere on this site.</div>
    </div>
  </div>

  <div class="timeline-group">
    <h2>2026-09-27 &mdash; the full recovery</h2>
    <div class="timeline-item">
      <div class="timeline-date">September 27, morning</div>
      <div class="timeline-title"><strong>Six recovery lanes run in parallel</strong>, between 09:05:36Z and 14:33:13+05:30: the WordPress mirror, deleted mirror posts and stub-fills, the Muslim Debate Initiative, best-capture re-fetches, academic texts and secondary sources, and the video catalogue. Each lane writes to its own staging tree and is verified against the manifest before anything is accepted.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, mirror</div>
      <div class="timeline-title">A fresh CDX enumeration of the WordPress mirror finds 42 post permalinks with a 200 capture: 20 still in the mirror&rsquo;s API and 22 gone, holding 110 available captures between them. The lane recovers <strong>18 items the archive did not have &mdash; 15 works plus {{ notices_total }} announcements</strong>, and fills 2 more stubs on works already held, with {{ recovery_rows }} per-work verdicts recorded in the recovery log. Three of the eighteen are announcements rather than works and are catalogued, never counted. One work that three different lanes each found separately is recognised as one work carrying three provenance records, which is why the item count and the work count differ.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, best-capture re-fetch</div>
      <div class="timeline-title"><strong>9 works already held adopt a fuller version</strong> found in a better capture &mdash; the largest being <em>Reviewing HaqiqatJou</em>, 54,296 &rarr; 68,903 words. Each is diffed, adopted as one text and never summed with the copy it replaces; the other 8 gain between 50 and 366 words each. All nine are listed work by work, with their word deltas, in the integration log committed with this repository.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, Muslim Debate Initiative</div>
      <div class="timeline-title">All {{ mdi_total }} author-archive pages are fetched live and their full text, {{ mdi_words }} words, is held here for the first time instead of being a link. {{ mdi_counted }} are distinct items of content; the other {{ mdi_republished }} republish a work already counted above, decided by a 5-gram text comparison rather than by title similarity, and are catalogued without being counted twice.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, papers</div>
      <div class="timeline-title">Every name is saved before any count moves: a {{ site.data.bibliography.counts.paper_rows }}-row access ledger records what is open, restricted or dead, alongside {{ site.data.bibliography.counts.doi_rows }} DOIs. The paper list then grows from 18 to <strong>{{ papers_total }}</strong> on legitimately obtained texts alone, and <strong>{{ pdf_files }} PDF files</strong> are held here. No paywall, robots rule or access control was bypassed to get them; the Academia.edu challenge was not fought.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, videos</div>
      <div class="timeline-title">{{ videos_total }} catalogued videos, {{ archive_files }} of them preserved as files in the Internet Archive and the rest catalogued as live re-uploads with a named uploader. <strong>{{ superseded_total }} entries that double-counted an existing recording</strong> are removed from the count and preserved in full in a superseded-video ledger rather than deleted, and mirror URLs attach to the recording they duplicate instead of adding to the total. The catalogue is now {{ videos_total }} videos, not a larger number that counted the same talk twice.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, afternoon &mdash; integration</div>
      <div class="timeline-title">An integration pass moves every verified item into the repository and records each one in an append-only log. <strong>An independent review finds 2 Critical, 7 Important and 11 Minor findings</strong>, including that the MDI pages and the works list were counting the same text twice; a fix wave settles it, and the computed total falls from a double-counted 219 to <strong>{{ total_content }}</strong>. Two further review rounds re-run the suites and confirm the fixes.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">September 27, evening &mdash; publication</div>
      <div class="timeline-title"><strong>{{ ix.documents }} machine transcripts, {{ ix.words }} words</strong>, are published one document per capture, each with its capture file, cue count, language and producing model. {{ ix.videos_attached }} of the {{ ix.catalogued_videos }} catalogued videos carry a transcript attached; {{ ix.videos_catalogue_only }} do not, and their pages say so rather than implying one is coming. The archive is published, and the per-lane evidence trail &mdash; the lane manifests, the append-only integration log, both independent review rounds and the Phase 3 reports &mdash; is committed with the repository, in the recovery log a reader can reach from the project&rsquo;s GitHub page.</div>
    </div>
  </div>

  <div class="timeline-group">
    <h2>2026-09-28 &mdash; the recount, applied</h2>
    <div class="timeline-item">
      <div class="timeline-date">September 28</div>
      <div class="timeline-title">The site owner approves the recount and it is applied in one pass, so that the site and the repository finally tell one story. The pre-recount figures above stop being the published ones. <strong>Every page that shows a count now counts it from <code>_data/</code> at build time</strong> rather than typing it, and the total is a sum whose terms are printed in the order they are added: <strong>{{ total_content }} = {{ works_total }} works + {{ videos_total }} videos + {{ papers_total }} papers + {{ mdi_counted }} MDI items + {{ yaqeen_total }} Yaqeen link-outs + {{ albalagh_total }} Al Balagh link-outs + {{ interviews_total }} interview</strong>. The {{ mdi_republished }} MDI rows that republish an already-counted work, the {{ secondary_total }} third-party source records, the {{ notices_total }} announcements and the {{ linkouts_total }} link-outs are catalogued and deliberately outside that sum; each is counted, and labelled, on its own.</div>
    </div>
  </div>

</div>

<h2 id="works">The recovered works, by publication date</h2>
<p class="page-note">{{ works_total }} works, each with the state of its own capture: full text preserved in this repository, catalogued Wayback-only, or lost with no archived copy located.</p>

<div class="timeline">
{% assign works = site.data.canonical_works | sort: "date" %}
{% assign current_year = "" %}
{% for work in works %}
  {% assign year = work.date | slice: 0, 4 %}
  {% if year != current_year %}
    {% unless forloop.first %}</div>{% endunless %}
  <div class="timeline-group">
    <h2>{{ year }}</h2>
    {% assign current_year = year %}
  {% endif %}
    <div class="timeline-item">
      <div class="timeline-date">{{ work.date | date: "%B %-d" }}</div>
      <div class="timeline-title"><a href="{{ "/articles/" | relative_url }}{{ work.slug }}/">{{ work.title }}</a> <span class="tag tag-status">{{ work.status }}</span></div>
    </div>
  {% if forloop.last %}</div>{% endif %}
{% endfor %}

  <div class="timeline-group">
    <h2>2022</h2>
    <div class="timeline-item">
      <div class="timeline-date">October 5</div>
      <div class="timeline-title">Videos removed from the original YouTube channel; the channel itself was not deleted &mdash; see the <a href="{{ '/channel/' | relative_url }}">channel history</a></div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">October 6</div>
      <div class="timeline-title">Archive.org collection created</div>
    </div>
  </div>

  <div class="timeline-group">
    <h2>2023</h2>
    <div class="timeline-item">
      <div class="timeline-date">July 13</div>
      <div class="timeline-title">"Between a Backbone and Ribs" PDF archived on Archive.org</div>
    </div>
  </div>

</div>

{%- comment -%}
  2026-09-28: this page is the archive's account of how the recovery went, so it is
  the right place to say what the 2026-09-28 searchability pass added - and the
  wrong place to bury it. Two entry points were added to the site on that date
  because two questions had no answer anywhere on it: who the subject is, and
  what became of the site he published on. A third surface groups the transcripts
  into the series the channel numbered. No count on this page changed; the figures
  above are the same figures, still counted from `_data/`.
{%- endcomment -%}
<p class="page-note"><strong>2026-09-28 &mdash; the searchability pass.</strong> Two pages
were added to the site because the queries people actually type about this corpus had no
honest answer anywhere on the web. <a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}">Who
this is</a> is the archive&rsquo;s single answer to the subject&rsquo;s name and his work:
every attested form of it, the distinction from the different man also called Abdullah
al-Andalusi, his four recorded roles and a linked index into the collections.
<a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">What happened to the
website</a> is the account of the lost properties &mdash; the site, the WordPress mirror,
the channel and the dead publisher domain &mdash; and it carries a safety warning, because
the domain he published on is now an unrelated gambling site. A third surface,
<a href="{{ '/transcripts/by-series/' | relative_url }}">the transcripts by series</a>,
groups the transcript corpus into the multi-part series the channel itself numbered. The
channel&rsquo;s own history is still on
<a href="{{ '/channel/' | relative_url }}">the channel record</a>.</p>
