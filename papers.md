---
layout: default
title: Academic Papers
description: The archive's academic papers by venue and date, with the full text where the archive holds it, a link-out where it does not, and a page per paper.
last_modified_at: 2026-09-28
---
{%- comment -%}
  Every figure on this page is computed from `_data/papers.json` at build time,
  including the subtitle's paper total.

  2026-09-27 (task 8f, Phase-3 review C1): the subtitle used to carry a typed
  `18` - the figure published before the recount - on the grounds that
  publishing 20 would go past the Task 9 approval gate while the homepage still
  published the pre-recount totals. That gate is now satisfied and the recount
  is applied across every page in one pass, so the total is computed like the
  rest.

  `held` counts paper ROWS that carry a local PDF; `held_files` counts the PDF
  FILES, which is one higher because one of those rows also carries a
  translation under `additional_files`. The two are printed separately rather
  than collapsed, because "6 PDFs" and "6 papers" are different claims and only
  one of them is true.

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
{%- comment -%}
  2026-09-28: papers that have at least one external registry record, counted
  for the cross-link to /scholarly-records/ below. The join is
  `_data/papers.json` row id -> `archive_paper_id` on every registry record in
  `_data/registries.json`, including each registry's `additional_records`. A
  paper is counted ONCE however many registries hold it, so a work registered
  under two DOIs does not inflate this figure. Nothing is typed.
{%- endcomment -%}
{%- assign n_covered = 0 -%}{%- assign n_bare = 0 -%}
{%- for p in site.data.papers -%}
  {%- assign hit = false -%}
  {%- for r in site.data.registries.registries -%}
    {%- for rec in r.records -%}{%- if rec.archive_paper_id == p.id -%}{%- assign hit = true -%}{%- endif -%}{%- endfor -%}
    {%- for rec in r.additional_records -%}{%- if rec.archive_paper_id == p.id -%}{%- assign hit = true -%}{%- endif -%}{%- endfor -%}
  {%- endfor -%}
  {%- if hit -%}{%- assign n_covered = n_covered | plus: 1 -%}{%- else -%}{%- assign n_bare = n_bare | plus: 1 -%}{%- endif -%}
{%- endfor -%}

<h1 class="page-title">Academic Papers</h1>
<p class="page-subtitle">{{ total }} research papers, articles, talks and book chapters, listed by publication venue.</p>
<p class="page-note">{{ sole }} are his alone and {{ coauthored }} co-authored with a named co-author; a co-authored paper is counted once, under category B, and not again among his sole-authored work. {{ held }} of the {{ total }} hold a PDF in this repository &mdash; {{ held_files }} PDF files in total, one of them a translation of a paper already counted, so the file count is one higher than the paper count. The rest are link-outs, because this project does not download a paper body it cannot obtain openly.</p>
{%- comment -%}
  2026-09-28. The point of this cross-link is the access ledger, not the author.
  Two of the twenty papers have a dead or restricted primary source - the 2015 ICR
  paper, whose publisher domain no longer resolves and whose DOI is dead, and the
  2014 IIUM thesis, whose full text the university restricts. Both are on this page
  with their corrected citation, which is the one thing a reader with a broken
  reference actually needs. The entity page carries who he is; the lost-and-found
  page carries why a dead publisher is not the end of a citation.
{%- endcomment -%}
<p class="page-note">Every row below states its own access status, which is the part of a
bibliography that goes out of date: {{ total }} rows, and for two of them the publisher or
the DOI no longer resolves. If you are here because a citation you were given does not work,
the corrected citation is printed on the paper&rsquo;s own page. For who wrote them, see
<a href="{{ '/asadullah-ali-al-andalusi/' | relative_url }}">the entity page</a>; for
what became of the sites these papers were announced on, see
<a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what happened to the
Andalusian Project&rsquo;s web presence</a>.</p>

{%- comment -%}
  2026-09-28: the cross-link to the bibliography-reconciliation page, placed here
  because this index is the page a reader lands on when they are checking a
  citation. The link answers the question the access ledger below cannot: not
  "is the publisher reachable" but "what do other people&rsquo;s bibliographies
  say about this paper, and what is wrong with those records". The sentence
  states the real figure rather than gesturing at the page, and that figure is
  counted from the two data files at build time - {{ n_covered }} of {{ total }}
  papers have an external record, computed by joining _data/papers.json to the
  archive_paper_id on each _data/registries.json record. A hand-typed number
  here would be the one thing on this page that could go stale silently.
{%- endcomment -%}
<p class="page-note">For the other half of a bibliography &mdash; where these papers are
recorded in OpenAlex, Semantic Scholar, Crossref, DOAJ, ORCID and the Internet Archive,
which of them are co-authored, and which DOIs no longer resolve to the article &mdash; see
<a href="{{ '/scholarly-records/' | relative_url }}">scholarly records</a>. That page
reconciles all {{ total }} of these papers against every registry surveyed, and
{{ n_covered }} of them have at least one external record; the remaining {{ n_bare }} have
none, which is a fact about what registries index and not a judgement on the work.</p>

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
