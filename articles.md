---
layout: default
title: Blog Posts
---
{%- comment -%}
  2026-09-27 (task 8f, Phase-3 review C1): the four PUBLISHED figures on this
  page - the work total in the subtitle, the three status figures in the
  page-note, the Preservation Method paragraph - were RESTORED to the values
  published at db16e2c. The recount (works, full-text, Wayback-only, lost) is
  correct in `_data/canonical_works.json` and is computed below, but publishing
  it is Task 9's approval gate, and publishing it here made /articles/ contradict
  the homepage, which still publishes the pre-recount totals. They are restored
  as typed figures deliberately and are the only typed figures on this page.

  Every other figure on this page is computed from the data at build time, and
  the sections added in task 8a carry their own computed counts.
{%- endcomment -%}
{%- assign found = 0 -%}{%- for w in site.data.canonical_works -%}{%- if w.status == "found" -%}{%- assign found = found | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign wayback_only = 0 -%}{%- for w in site.data.canonical_works -%}{%- if w.status == "wayback_only" -%}{%- assign wayback_only = wayback_only | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign lost = 0 -%}{%- for w in site.data.canonical_works -%}{%- if w.status == "lost" -%}{%- assign lost = lost | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign works_total = 0 -%}{%- for w in site.data.canonical_works -%}{%- assign works_total = works_total | plus: 1 -%}{%- endfor -%}
{%- assign mdi_total = 0 -%}{%- for m in site.data.mdi_articles -%}{%- assign mdi_total = mdi_total | plus: 1 -%}{%- endfor -%}
{%- assign mdi_counted = 0 -%}{%- for m in site.data.mdi_articles -%}{%- if m.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign mdi_republished = mdi_total | minus: mdi_counted -%}
{%- assign notices_total = 0 -%}{%- for n in site.data.notices -%}{%- assign notices_total = notices_total | plus: 1 -%}{%- endfor -%}
{%- assign linkouts_total = 0 -%}{%- for l in site.data.linkouts -%}{%- assign linkouts_total = linkouts_total | plus: 1 -%}{%- endfor -%}
{%- assign linkouts_story = 0 -%}{%- for l in site.data.linkouts -%}{%- if l.type == "conversion_story" -%}{%- assign linkouts_story = linkouts_story | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign linkouts_yaqeen = 0 -%}{%- for l in site.data.linkouts -%}{%- if l.type == "yaqeen_paper" -%}{%- assign linkouts_yaqeen = linkouts_yaqeen | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- comment -%}
  The published date range in the subtitle is computed, not typed (task 8f, M8):
  a typed range stops being true the moment a work is added, and the recovered
  works do decide it. `date` is ISO, so the year is its first four characters.
{%- endcomment -%}
{%- assign year_first = 9999 -%}{%- assign year_last = 0 -%}
{%- for w in site.data.canonical_works -%}
  {%- assign y = w.date | slice: 0, 4 | plus: 0 -%}
  {%- if y < year_first -%}{%- assign year_first = y -%}{%- endif -%}
  {%- if y > year_last -%}{%- assign year_last = y -%}{%- endif -%}
{%- endfor -%}
{%- assign mdi_under_100 = 0 -%}{%- for m in site.data.mdi_articles -%}{%- assign mwords = m.words | default: 0 -%}{%- if mwords < 100 -%}{%- assign mdi_under_100 = mdi_under_100 | plus: 1 -%}{%- endif -%}{%- endfor -%}

<h1 class="page-title">Blog Posts</h1>
<p class="page-subtitle">57 works ({{ year_first }}-{{ year_last }}) from asadullahali.com, plus {{ mdi_total }} MDI pages, {{ notices_total }} announcements and {{ linkouts_total }} link-outs.</p>
<p class="page-note">15 works are preserved full-text in this repository; 40 are available via the Wayback Machine only; 2 are lost with no archived copy located. 87 CDX captures are preserved as metadata.</p>
<div class="card-grid">
{% for work in site.data.canonical_works %}
{% if work.status != "lost" %}
  <div class="card">
    <h3>{{ work.title }}</h3>
    <div class="card-meta">
      {{ work.date }} &mdash; {{ work.slug }}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=work.category %}
      {% if work.status == "found" %}
      <span class="tag tag-status">Full-text</span>
      {% elsif work.status == "wayback_only" %}
      <span class="tag tag-status">Wayback-only</span>
      {% endif %}
    </div>
    <div class="card-actions">
      {% if work.status == "found" %}
      <a href="{{ '/articles/' | relative_url }}{{ work.slug }}/" class="btn btn-primary btn-sm">Read full text</a>
      {% if work.wayback_url %}
      <a href="{{ work.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Wayback Machine</a>
      {% endif %}
      {% elsif work.status == "wayback_only" %}
      {% if work.wayback_url %}
      <a href="{{ work.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">Read on Wayback Machine</a>
      {% else %}
      <span class="card-note">No Wayback URL captured</span>
      {% endif %}
      {% endif %}
    </div>
  </div>
{% endif %}
{% endfor %}
</div>

<h2>Lost works</h2>
<p class="page-note">{{ lost }} work{% if lost != 1 %}s{% endif %} with no archived copy located. Titles and dates preserved for reference.</p>
<div class="card-grid">
{% for work in site.data.canonical_works %}
{% if work.status == "lost" %}
  <div class="card">
    <h3>{{ work.title }}</h3>
    <div class="card-meta">
      {{ work.date }} &mdash; {{ work.slug }}
    </div>
    <div class="card-tags">
      <span class="tag tag-status">Lost</span>
    </div>
    <div class="card-actions">
      <span class="card-note">No archived copy located</span>
    </div>
  </div>
{% endif %}
{% endfor %}
</div>

{%- comment -%}
  The MDI pages and the notice pages were built and reachable by direct URL but
  listed nowhere, so a reader browsing the archive could not find them. They are
  listed here now. MDI rows are filed by authorship: every one of them carries
  his byline, so all of them are category A, but only {{ mdi_counted }} are
  counted as distinct items - the other {{ mdi_republished }} republish a work
  already in the list above and name it on their own page.
{%- endcomment -%}
<h2>Muslim Debate Initiative pages</h2>
<p class="page-note">{{ mdi_total }} pages he wrote for the Muslim Debate Initiative, all recovered from the MDI author archive on 2026-09-27 and preserved here verbatim. {{ mdi_counted }} are distinct items of content and are counted once; the rest republish a work listed above and are counted there instead. {{ mdi_under_100 }} of the {{ mdi_total }} are under 100 words, because the substance of those posts is an embedded video and the prose is its caption. They are kept as published.</p>
<div class="card-grid">
{% for m in site.data.mdi_articles %}
  <div class="card">
    <h3>{{ m.title }}</h3>
    <div class="card-meta">
      {{ m.date }} &mdash; {{ m.author }}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=m.category %}
      {% if m.counted %}<span class="tag tag-status">Counted item</span>{% else %}<span class="tag tag-status">Republishes a listed work</span>{% endif %}
      {% if m.words %}<span class="tag tag-topic">{{ m.words }} words</span>{% endif %}
    </div>
    <div class="card-actions">
      <a href="{{ '/articles/mdi/' | relative_url }}{{ m.slug }}/" class="btn btn-primary btn-sm">Read the page</a>
      <a href="{{ m.url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Original on MDI</a>
    </div>
  </div>
{% endfor %}
</div>

<h2>Announcements</h2>
<p class="page-note">{{ notices_total }} posts that announce something rather than argue it. They are catalogued, their text is preserved, and none of them is counted as a work.</p>
<div class="card-grid">
{% for n in site.data.notices %}
  <div class="card">
    <h3>{{ n.title }}</h3>
    <div class="card-meta">
      {{ n.date }} &mdash; {{ n.slug }}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=n.category %}
      <span class="tag tag-status">Not counted</span>
    </div>
    <div class="card-actions">
      <a href="{{ '/articles/notice/' | relative_url }}{{ n.slug }}/" class="btn btn-primary btn-sm">Read the announcement</a>
      {% if n.wayback_url %}<a href="{{ n.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Wayback Machine</a>{% endif %}
    </div>
  </div>
{% endfor %}
</div>

{%- comment -%}
  Link-outs. These are entries, not recovered text: the archive records that
  the page exists and links to it. No local text is claimed for any of them,
  which is why they carry no "read" button.
{%- endcomment -%}
<h2>Link-outs</h2>
<p class="page-note">{{ linkouts_total }} entries: {{ linkouts_story }} conversion-story reprint and {{ linkouts_yaqeen }} Yaqeen Institute pages. These are links, not recovered text. This archive does not download their bodies, so it does not claim their words and does not add their size to any total.</p>
<div class="card-grid">
{% for l in site.data.linkouts %}
  <div class="card">
    <h3>{{ l.title }}</h3>
    <div class="card-meta">
      {% if l.type == "conversion_story" %}{{ l.published_by }}{% if l.published %} &middot; {{ l.published }}{% endif %}{% else %}Yaqeen Institute for Islamic Research{% endif %}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=l.category %}
      <span class="tag tag-status">Link-out, not counted</span>
    </div>
    <div class="card-body">{{ l.description }}</div>
    <div class="card-actions">
      <a href="{{ l.url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Open the page</a>
      {% if l.wayback_url %}<a href="{{ l.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Wayback Machine</a>{% endif %}
    </div>
  </div>
{% endfor %}
</div>

<div class="section">
  <div class="info-block">
    <h3>About This Collection</h3>
    <p>The original asadullahali.com website was the primary platform for The Andalusian Project's written content, covering Islamic philosophy, theology, and contemporary issues. Everything on this page is his own writing, published by him; the categories that hold other people's material are the video page and this page's link-out section.</p>
    <h3>Preservation Method</h3>
    <p>57 canonical works identified from 87 Wayback Machine CDX captures. Full text of 30 works is preserved in this repository; 40 are Wayback-only; 2 are lost.</p>
    <h3>Content Categories</h3>
    <ul>
      <li>Philosophy &mdash; Discussions on Islamic and Western philosophical traditions</li>
      <li>Theology &mdash; Islamic creed and theological discussions</li>
      <li>Current Affairs &mdash; Analysis of contemporary issues from an Islamic perspective</li>
      <li>Debates &mdash; Responses to critics and interfaith discussions</li>
    </ul>
  </div>
</div>
