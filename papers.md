---
layout: default
title: Academic Papers
description: The archive's academic papers by venue and date, with the full text where the archive holds it, a link-out where it does not, and a page per paper.
---
{%- comment -%}
  Counts are computed, with one exception: the subtitle's paper total is the
  figure published before the 2026-09-27 recount and is restored as a typed
  number on purpose. 2026-09-27 (task 8f, Phase-3 review C1): the recount put
  `_data/papers.json` at 20 rows and publishing that on this existing page went
  past the Task 9 approval gate. The 20 is correct and waits for the owner
  there, applied together with the homepage and README in one approved pass.

  build_collections.py already writes the local PDF link and the per-file
  licence/provenance line into each paper's own page; this index repeats the
  same two facts on the card so a reader can see which papers are held locally
  before opening one, and flags the co-authored ones with the existing
  co_authors field.
{%- endcomment -%}
{%- assign total = 0 -%}{%- for p in site.data.papers -%}{%- assign total = total | plus: 1 -%}{%- endfor -%}
{%- assign coauthored = 0 -%}{%- for p in site.data.papers -%}{%- if p.co_authors and p.co_authors.size > 0 -%}{%- assign coauthored = coauthored | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign sole = total | minus: coauthored -%}
{%- assign held = 0 -%}{%- assign held_files = 0 -%}{%- for p in site.data.papers -%}{%- if p.file -%}{%- assign held = held | plus: 1 -%}{%- assign held_files = held_files | plus: 1 -%}{%- endif -%}{%- if p.additional_files -%}{%- assign held_files = held_files | plus: p.additional_files.size -%}{%- endif -%}{%- endfor -%}

<h1 class="page-title">Academic Papers</h1>
<p class="page-subtitle">18 research papers, articles, talks and book chapters, listed by publication venue.</p>
<p class="page-note">{{ sole }} are his alone and {{ coauthored }} co-authored with a named co-author; a co-authored paper is counted once, under category B, and not again among his sole-authored work. {{ held }} of the {{ total }} hold a PDF in this repository ({{ held_files }} files in total, including translations); the rest are link-outs, because this project does not download a paper body it cannot obtain openly.</p>

<h2>Sole-authored</h2>
{%- comment -%}
  2026-09-27 (on-page SEO pass): every paper card now links to that paper's own
  page under /papers/<slug>/. Before this, all 20 paper pages - the whole
  academic-papers collection - had ZERO inbound internal links: this index
  linked only to PDFs and to external hosts, so the entire scholarly output of
  the archive was reachable only from the sitemap, and the sitemap is not
  reliably fetched for a github.io host (audit B10). This is the single largest
  discoverability defect in the corpus and it was one missing link per card.

  The join is on the row's `title`, which build_papers.py writes verbatim into
  each page's front matter, so the index cannot drift from the pages it links
  to: a title with no matching page simply produces no link rather than a dead
  one. Nothing else about the card changed, and no figure on this page changed.
{%- endcomment -%}
<div class="card-grid">
{% for paper in site.data.papers %}
{% if paper.co_authors.size == 0 %}
  {%- assign paper_page = nil -%}
  {%- for doc in site.papers -%}
    {%- if doc.title == paper.title -%}{%- assign paper_page = doc -%}{%- endif -%}
  {%- endfor -%}
  <div class="card">
    <h3>{% if paper_page %}<a href="{{ paper_page.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ paper.title }}{% endif %}</h3>
    <div class="card-meta">
      {{ paper.publisher_journal }}
      {% if paper.publication_date %} &middot; {{ paper.publication_date }}{% endif %}
      {% if paper.citation_count %} &middot; {{ paper.citation_count }} citations{% endif %}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=paper.category %}
      {% if paper.file %}<span class="tag tag-status">PDF held here</span>{% else %}<span class="tag tag-status">Link-out only</span>{% endif %}
    </div>
    <div class="card-actions">
      {%- if paper_page -%}<a href="{{ paper_page.url | relative_url }}" class="btn btn-primary btn-sm">Read the page</a>{%- endif -%}
      <a href="{{ paper.url }}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">View Original</a>
      {% if paper.pdf_url %}<a href="{{ paper.pdf_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">PDF</a>{% endif %}
      {% if paper.wayback_url %}<a href="{{ paper.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Wayback Machine</a>{% endif %}
    </div>
    {% if paper.file %}
    <div class="card-body">
      <a href="{{ '/papers/' | relative_url }}{{ paper.file }}">Local PDF: {{ paper.file }}</a> ({{ paper.file_pages }} pp.)<br>
      Licence / provenance: {{ paper.file_licence }}
    </div>
    {% endif %}
    {% if paper.additional_files %}
    {% for extra in paper.additional_files %}
    <div class="card-body">
      <a href="{{ '/papers/' | relative_url }}{{ extra.file }}">Local PDF: {{ extra.file }}</a> ({{ extra.pages }} pp.) &mdash; {% include bidi.html text=extra.label %}<br>
      Licence / provenance: {{ extra.file_licence }}
    </div>
    {% endfor %}
    {% endif %}
  </div>
{% endif %}
{% endfor %}
</div>

<h2>Co-authored</h2>
<p class="page-note">{{ coauthored }} paper{% if coauthored != 1 %}s{% endif %} written with a named co-author. Category B: the count is not the same as it would be if he had written it alone, and it is not counted a second time under category A.</p>
<div class="card-grid">
{% for paper in site.data.papers %}
{% if paper.co_authors.size > 0 %}
  {%- assign paper_page = nil -%}
  {%- for doc in site.papers -%}
    {%- if doc.title == paper.title -%}{%- assign paper_page = doc -%}{%- endif -%}
  {%- endfor -%}
  <div class="card">
    <h3>{% if paper_page %}<a href="{{ paper_page.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ paper.title }}{% endif %}</h3>
    <div class="card-meta">
      {{ paper.publisher_journal }}
      {% if paper.publication_date %} &middot; {{ paper.publication_date }}{% endif %}
    </div>
    <div class="card-tags">
      {% include category_badge.html category=paper.category %}
      <span class="tag tag-status">Co-authored</span>
      {% if paper.file %}<span class="tag tag-status">PDF held here</span>{% else %}<span class="tag tag-status">Link-out only</span>{% endif %}
    </div>
    <div class="card-body">Co-authors: {{ paper.co_authors | join: ", " }}</div>
    {% if paper.file %}
    <div class="card-body">
      <a href="{{ '/papers/' | relative_url }}{{ paper.file }}">Local PDF: {{ paper.file }}</a> ({{ paper.file_pages }} pp.)<br>
      Licence / provenance: {{ paper.file_licence }}
    </div>
    {% endif %}
    {% if paper.additional_files %}
    {% for extra in paper.additional_files %}
    <div class="card-body">
      <a href="{{ '/papers/' | relative_url }}{{ extra.file }}">Local PDF: {{ extra.file }}</a> ({{ extra.pages }} pp.) &mdash; {% include bidi.html text=extra.label %}<br>
      Licence / provenance: {{ extra.file_licence }}
    </div>
    {% endfor %}
    {% endif %}
    <div class="card-actions">
      {%- if paper_page -%}<a href="{{ paper_page.url | relative_url }}" class="btn btn-primary btn-sm">Read the page</a>{%- endif -%}
      <a href="{{ paper.url }}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">View Original</a>
      {% if paper.pdf_url %}<a href="{{ paper.pdf_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">PDF</a>{% endif %}
      {% if paper.wayback_url %}<a href="{{ paper.wayback_url }}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Wayback Machine</a>{% endif %}
    </div>
  </div>
{% endif %}
{% endfor %}
</div>
