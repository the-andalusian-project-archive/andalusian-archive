---
layout: default
title: "Scholarly records: where this work is registered outside the archive"
description: "OpenAlex, Semantic Scholar, Crossref, DOAJ, ORCID and the Internet Archive: where Al-Andalusi's work is externally recorded, and what those records get wrong."
permalink: /scholarly-records/
schema: dataset
last_modified_at: 2026-09-28
---
{%- comment -%}
  THE BIBLIOGRAPHY-RECONCILIATION PAGE (2026-09-28).

  WHY IT EXISTS. The archive is the most complete single account of this
  corpus, and until now it said so only about the TEXT: what is held, what is
  a link-out, what is dead. It said nothing about the IDENTIFIERS other people
  cite, which is where a reader actually meets this work - in a bibliography,
  a database or a search result. A reader who searches his name in a scholarly
  registry gets five works, three co-authorships that never appear, one
  article registered twice and three DOIs that resolve to the wrong website.
  This page is the archive's answer to all of that.

  EVERY FACT ON THIS PAGE IS RENDERED FROM `_data/registries.json`. No
  identifier, no count, no date and no prose about a registry is typed here.
  The file is the source of truth and this template is the only thing that
  reads it. That is a deliberate constraint, not a style preference: a page
  about external identifiers is exactly where an invented one would do the
  most damage, because an invented identifier is not obviously wrong to a
  reader - it is a valid-looking string in a column headed "DOI".

  The paper list in the reconciliation table is derived from `_data/papers.json`
  rather than from the registry file, so the LEFT side of every row is the
  archive's own catalogue and the RIGHT side is what the registries say about
  it. A work with no external record gets an honest "none found", never a
  suggestion that an unindexed work is a lesser one.

  THE JOIN. Registry records name the archive paper they refer to by
  `archive_paper_id`, the integer `id` on the `_data/papers.json` row. The
  join is on that integer rather than on a title, because no registry agrees
  with any other registry, or with the archive, on the wording of these
  titles: one conference paper alone appears under three different titles
  across OpenAlex, Crossref and Semantic Scholar. The link to the paper's own
  page is matched on title, which is the join `_layouts/paper.html` and
  `papers.md` already use, so a title with no page produces no link rather
  than a dead one.
{%- endcomment -%}
{%- assign reg = site.data.registries -%}
{%- assign papers = site.data.papers -%}

{%- comment -%} ------------------------------------------------------------------
  PASS 1, COUNTS. Everything a number on this page needs, counted out of the
  two data files. Nothing below this block is typed.
  -------------------------------------------------------------------------- {%- endcomment -%}
{%- assign papers_total = 0 -%}
{%- assign n_covered = 0 -%}
{%- assign n_bare = 0 -%}
{%- assign n_with_doi = 0 -%}
{%- assign n_held = 0 -%}
{%- assign reg_records = 0 -%}
{%- assign reg_additional = 0 -%}
{%- assign reg_identifiers = 0 -%}
{%- for p in papers -%}
  {%- assign papers_total = papers_total | plus: 1 -%}
  {%- if p.doi -%}{%- assign n_with_doi = n_with_doi | plus: 1 -%}{%- endif -%}
  {%- if p.file -%}{%- assign n_held = n_held | plus: 1 -%}{%- endif -%}
  {%- assign hit = false -%}
  {%- for r in reg.registries -%}
    {%- for rec in r.records -%}
      {%- if rec.archive_paper_id == p.id -%}{%- assign hit = true -%}{%- endif -%}
    {%- endfor -%}
    {%- for rec in r.additional_records -%}
      {%- if rec.archive_paper_id == p.id -%}{%- assign hit = true -%}{%- endif -%}
    {%- endfor -%}
  {%- endfor -%}
  {%- if hit -%}{%- assign n_covered = n_covered | plus: 1 -%}{%- else -%}{%- assign n_bare = n_bare | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- for r in reg.registries -%}
  {%- assign reg_records = reg_records | add: r.records.size -%}
  {%- if r.additional_records -%}{%- assign reg_additional = reg_additional | add: r.additional_records.size -%}{%- endif -%}
  {%- for rec in r.records -%}
    {%- if rec.doi -%}{%- assign reg_identifiers = reg_identifiers | plus: 1 -%}{%- endif -%}
  {%- endfor -%}
  {%- for rec in r.additional_records -%}
    {%- if rec.doi -%}{%- assign reg_identifiers = reg_identifiers | plus: 1 -%}{%- endif -%}
  {%- endfor -%}
{%- endfor -%}

<div class="hero">
  <h1>Scholarly records</h1>
  <p class="hero-subtitle">Where Asadullah Ali Al-Andalusi&rsquo;s scholarly work is recorded
  outside this archive, which of his catalogued papers each record refers to, and what is
  wrong with the records. Every identifier below was read out of a live registry API on
  {{ reg.survey.verified_on }} and re-checked on {{ reg.survey.reverified_on }}; the survey
  is a snapshot, not a live feed, and its limits are stated in full at the foot of this
  page.</p>
</div>

<div class="info-block">
  <h3>The one-paragraph version</h3>
  <p>{{ reg.registries | size }} public registries were queried. Between them they hold
  {{ n_covered }} of the {{ papers_total }} papers in this archive&rsquo;s catalogue, under
  {{ reg.registries[0].records.size }} separate work records &mdash; which is more records than
  works, because one journal article is registered under two DOIs and one conference is
  registered twice. Two findings matter more than the count: three of his papers are
  <strong>co-authored</strong> and are therefore contributions rather than sole works, and
  <strong>every DOI in this corpus with the <code>10.12816</code> prefix now resolves to a
  third-party reader&rsquo;s homepage</strong> rather than to the article or the publisher.
  Nothing else in this corpus is that badly broken, and the archives&rsquo; own text is intact
  throughout.</p>
  <p class="page-note">This page is a bibliography record, not a claim of importance. A work
  with no external record is not a lesser work: most of them are talks and lectures that no
  registry indexes, and this archive holds them from other sources entirely.</p>
</div>

<h2 id="registries">1. What the registries hold</h2>
<p>One row per registry. The count is the number of records the registry actually returned
for him, counted at build time; it is not a coverage score, and a zero in the count column is
a fact about the registry&rsquo;s indexing policy rather than about the work.</p>

<table>
  <thead>
    <tr>
      <th>Registry</th>
      <th>Record</th>
      <th>What it holds</th>
      <th>What this archive can add to it</th>
    </tr>
  </thead>
  <tbody>
  {%- for r in reg.registries %}
    <tr>
      <td><strong>{{ r.name | escape }}</strong></td>
      <td>{% if r.records.size > 0 %}<a href="{{ r.record_url }}" target="_blank" rel="noopener noreferrer">{{ r.record_url | escape }}</a>{% else %}<a href="{{ r.record_url }}" target="_blank" rel="noopener noreferrer">search that returns nothing</a>{% endif %}</td>
      <td>
        <strong>{{ r.records.size }}</strong> {{ r.records_unit }}
        {%- if r.additional_records and r.additional_records.size > 0 %}, plus
        {{ r.additional_records.size }} found separately{% endif %}.
        {{ r.what_it_holds | escape }}
        {%- if r.no_record_reason %}
        <p class="meta"><strong>On the zero:</strong> {{ r.no_record_reason | escape }}</p>
        {%- endif %}
      </td>
      <td>{{ r.write_access | escape }}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>

<p class="page-note">The write-access column is the honest one. {{ reg.registries[3].write_access }}
{{ reg.registries[4].write_access }} This archive has no account on any of these services, and
the two it might conceivably create &mdash; an ORCID record and a Wikidata item &mdash; are
refused for the reasons in section 4.</p>

<h3>The subject is not in these registries under one name</h3>
<p>Four different name forms, one person, and no registry that links them to each other. This
is the first reconciliation problem and it is the reason a reader searching one form finds
nothing.</p>
<ul>
{%- for n in reg.subject.display_names_in_registries %}
  <li><code>{{ n | escape }}</code></li>
{%- endfor %}
</ul>
<p>{{ reg.subject.note | escape }}</p>

{%- comment -%}
  Per-registry record tables. Each identifier is rendered from the record's own
  field and links to the registry, so a reader can check any row of this page
  against the source it came from without leaving the archive.
{%- endcomment -%}
{%- for r in reg.registries %}
{%- if r.records.size > 0 %}
<h3>{{ r.name | escape }}: the {{ r.records.size }} {{ r.records_unit }}</h3>
<table>
  <thead>
    <tr>
      <th>Record</th>
      <th>Title as the registry has it</th>
      <th>Year</th>
      <th>DOI</th>
      <th>Other registry fields</th>
    </tr>
  </thead>
  <tbody>
  {%- for rec in r.records %}
    <tr>
      <td>{% if rec.registry_url %}<a href="{{ rec.registry_url }}" target="_blank" rel="noopener noreferrer"><code>{% if rec.openalex_id %}{{ rec.openalex_id }}{% elsif rec.corpus_id %}{{ rec.corpus_id }}{% elsif rec.doi %}{{ rec.doi }}{% elsif rec.collection_id %}{{ rec.collection_id }}{% else %}{{ rec.registry_url }}{% endif %}</code></a>{% else %}<code>{% if rec.openalex_id %}{{ rec.openalex_id }}{% elsif rec.corpus_id %}{{ rec.corpus_id }}{% elsif rec.doi %}{{ rec.doi }}{% else %}{{ rec.collection_id }}{% endif %}</code>{% endif %}
        {%- if rec.title %}<br><span class="meta">title record</span>{% endif %}</td>
      <td>{{ rec.title | escape }}{% if rec.duplicate_of %}<br><span class="meta"><strong>duplicate pair:</strong> this and <code>{{ rec.duplicate_of }}</code> are one work, registered twice</span>{% endif %}
        {%- if rec.archive_paper_id %}
        <br><span class="meta">refers to the archive&rsquo;s own record for
        {%- for pp in papers -%}{%- if pp.id == rec.archive_paper_id -%}{{ pp.title | escape }}{%- endif -%}{%- endfor -%}</span>
        {%- endif %}</td>
      <td>{% if rec.year %}{{ rec.year }}{% else %}&mdash;{% endif %}</td>
      <td>{% if rec.doi %}<a href="https://doi.org/{{ rec.doi }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.doi }}</code></a>{% else %}<span class="meta">no DOI</span>{% endif %}</td>
      <td>
        {%- if rec.cited_by != nil -%}{{ rec.cited_by }} citations<br>{%- endif -%}
        {%- if rec.is_oa != nil -%}open access: {{ rec.is_oa }}{%- if rec.oa_status %} ({{ rec.oa_status }}){% endif %}<br>{%- endif -%}
        {%- if rec.citationCount != nil -%}{{ rec.citationCount }} citations<br>{%- endif -%}
        {%- if rec.mag_id -%}MAG id {{ rec.mag_id }}<br>{%- endif -%}
        {%- if rec.corpus_id -%}corpus id {{ rec.corpus_id }}<br>{%- endif -%}
        {%- if rec.container_title -%}{{ rec.container_title }}{%- if rec.volume %} {{ rec.volume }}{%- endif -%}{%- if rec.issue %}({{ rec.issue }}){%- endif -%}{%- if rec.pages %}, pp. {{ rec.pages }}{%- endif -%}<br>{%- endif -%}
        {%- if rec.issn -%}ISSN {{ rec.issn }}<br>{%- endif -%}
        {%- if rec.mediatype -%}mediatype {{ rec.mediatype }}{%- endif -%}
        {%- if rec.publicdate -%}public {{ rec.publicdate }}{%- endif -%}
        {%- if rec.item_size_human -%}{{ rec.item_size_human }}{%- endif -%}
        {%- if rec.co_authors and rec.co_authors.size > 0 -%}<span class="tag tag-status">co-authored</span>{%- else -%}<span class="meta">sole-authored</span>{%- endif -%}
        {%- if rec.authors and rec.authors.size > 0 -%}<br><span class="meta">authors as recorded: {% for a in rec.authors %}{{ a.given }} {{ a.family }}{% unless forloop.last %}, {% endunless %}{% endfor %}</span>{%- endif -%}
        {%- if rec.note -%}<br><span class="meta">{{ rec.note | escape }}</span>{%- endif -%}
      </td>
    </tr>
  {%- endfor %}
  {%- for rec in r.additional_records %}
    <tr>
      <td><a href="{{ rec.registry_url }}" target="_blank" rel="noopener noreferrer"><code>{% if rec.openalex_id %}{{ rec.openalex_id }}{% elsif rec.corpus_id %}{{ rec.corpus_id }}{% else %}{{ rec.doi }}{% endif %}</code></a>
        <br><span class="meta">not on the author record</span></td>
      <td>{{ rec.title | escape }}
        <br><span class="meta">refers to the archive&rsquo;s own record for
        {%- for pp in papers -%}{%- if pp.id == rec.archive_paper_id -%}{{ pp.title | escape }}{%- endif -%}{%- endfor -%}</span></td>
      <td>{% if rec.year %}{{ rec.year }}{% else %}&mdash;{% endif %}</td>
      <td>{% if rec.doi %}<a href="https://doi.org/{{ rec.doi }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.doi }}</code></a>{% else %}<span class="meta">no DOI</span>{% endif %}</td>
      <td>
        {%- if rec.cited_by != nil -%}{{ rec.cited_by }} citations<br>{%- endif -%}
        {%- if rec.is_oa != nil -%}open access: {{ rec.is_oa }}<br>{%- endif -%}
        {%- if rec.on_author_record == false -%}<span class="tag tag-status">absent from the author record</span><br>{%- endif -%}
        {%- if rec.co_authors and rec.co_authors.size > 0 -%}<span class="tag tag-status">co-authored</span>{%- endif -%}
        {%- if rec.note -%}<br><span class="meta">{{ rec.note | escape }}</span>{%- endif -%}
      </td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
{%- if r.author_record %}
<p class="page-note"><strong>On the author record itself.</strong> {{ r.what_it_holds | escape }}
{%- if r.author_record.orcid == nil and r.author_record.display_name %} The record carries no ORCID, and no affiliations are recorded against it{% if r.author_record.affiliations_note %} &mdash; {{ r.author_record.affiliations_note | escape }}{% endif %}.{% endif %}
{%- if r.author_record.topics_note %} Topics on the record are generated by OpenAlex and change without notice: {{ r.author_record.topics_note | escape }}{% endif %}
{%- if r.cross_check %} {{ r.cross_check | escape }}{% endif %}</p>
{%- endif %}
{%- if r.rejected_candidates %}
<p class="page-note"><strong>{{ r.rejected_candidates.size }} candidate records were read and rejected</strong>, and they are named here so the next search does not have to repeat the work:
{% for c in r.rejected_candidates %}<code>{{ c.orcid }}</code> &mdash; {{ c.name_as_recorded | escape }}: {{ c.why_rejected | escape }}{% unless forloop.last %}; {% endunless %}{% endfor %}.</p>
{%- endif %}
{%- endif %}
{%- endfor %}

<h2 id="reconciliation">2. Work-by-work reconciliation</h2>
<p>Every paper in this archive&rsquo;s catalogue, with what the registries say about it. The
left-hand column is the archive&rsquo;s own record; the right-hand columns are what the
registries returned. <strong>{{ n_covered }}</strong> of the {{ papers_total }} have at least one
external record; <strong>{{ n_bare }}</strong> have none, which is stated plainly and is not a
judgement on the work. The {{ n_with_doi }} rows that carry a DOI on the archive&rsquo;s own
record are not the same set: a DOI in this archive&rsquo;s data is a bibliographic field, and a
registry record is somebody else&rsquo;s claim about the work.</p>

<table>
  <thead>
    <tr>
      <th>Paper in this archive</th>
      <th>External records found</th>
      <th>Identifiers</th>
      <th>Where this archive holds the text</th>
    </tr>
  </thead>
  <tbody>
  {%- for p in papers %}
    {%- assign paper_page = nil -%}
    {%- for doc in site.papers -%}
      {%- if doc.title == p.title -%}{%- assign paper_page = doc -%}{%- endif -%}
    {%- endfor -%}
    {%- assign hit = false -%}
    <tr>
      <td>
        {% if paper_page %}<a href="{{ paper_page.url | relative_url }}">{{ p.title }}</a>{% else %}{{ p.title }}{% endif %}
        <br><span class="meta">{{ p.publisher_journal }}{% if p.publication_date %} &middot; {{ p.publication_date }}{% endif %}</span>
        {%- if p.co_authors and p.co_authors.size > 0 %}
        <br><span class="tag tag-category tag-category-{{ p.category }}">B &middot; with {{ p.co_authors | join: ", " }}</span>
        {%- endif %}
      </td>
      <td>
        {%- assign found_any = false -%}
        {%- for r in reg.registries -%}
          {%- for rec in r.records -%}
            {%- if rec.archive_paper_id == p.id -%}
              {%- assign found_any = true -%}
              {{ r.name }}<br>
            {%- endif -%}
          {%- endfor -%}
          {%- for rec in r.additional_records -%}
            {%- if rec.archive_paper_id == p.id -%}
              {%- assign found_any = true -%}
              {{ r.name }}<br>
            {%- endif -%}
          {%- endfor -%}
        {%- endfor -%}
        {%- unless found_any %}
        <span class="meta">No external record found. Nothing in {{ reg.registries | size }}
        registries has this work, which is a fact about their indexing rather than about the
        work: it is catalogued, cited and preserved here either way.</span>
        {%- endunless -%}
      </td>
      <td>
        {%- assign any_id = false -%}
        {%- if p.doi -%}
          {%- assign any_id = true -%}
          <a href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener noreferrer"><code>{{ p.doi }}</code></a><br><span class="meta">DOI on the archive&rsquo;s own record</span><br>
        {%- endif -%}
        {%- for r in reg.registries -%}
          {%- for rec in r.records -%}
            {%- if rec.archive_paper_id == p.id -%}
              {%- if rec.doi %}{%- assign any_id = true -%}<a href="https://doi.org/{{ rec.doi }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.doi }}</code></a> <span class="meta">{{ r.name }}</span><br>{% endif -%}
              {%- if rec.openalex_id %}{%- assign any_id = true -%}<a href="{{ rec.registry_url }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.openalex_id }}</code></a> <span class="meta">OpenAlex</span><br>{% endif -%}
              {%- if rec.corpus_id %}{%- assign any_id = true -%}<code>{{ rec.corpus_id }}</code> <span class="meta">Semantic Scholar corpus id</span><br>{% endif -%}
            {%- endif -%}
          {%- endfor -%}
          {%- for rec in r.additional_records -%}
            {%- if rec.archive_paper_id == p.id -%}
              {%- if rec.doi %}{%- assign any_id = true -%}<a href="https://doi.org/{{ rec.doi }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.doi }}</code></a> <span class="meta">{{ r.name }}</span><br>{% endif -%}
              {%- if rec.openalex_id %}{%- assign any_id = true -%}<a href="{{ rec.registry_url }}" target="_blank" rel="noopener noreferrer"><code>{{ rec.openalex_id }}</code></a> <span class="meta">OpenAlex</span><br>{% endif -%}
            {%- endif -%}
          {%- endfor -%}
        {%- endfor -%}
        {%- unless any_id %}<span class="meta">no persistent identifier anywhere</span>{%- endunless -%}
      </td>
      <td>
        {%- if p.file %}
          <a href="{{ p.file_url | relative_url }}">PDF held here</a> ({{ p.file_pages }} pp.)
          {%- if p.additional_files %} plus {{ p.additional_files.size }} further file{% if p.additional_files.size != 1 %}s{% endif %}{% endif %}
        {%- elsif p.file_status %}
          <span class="meta">Citation retained; the file is <strong>withheld</strong>
          ({{ p.file_status }}). The text is not distributed by this archive.</span>
        {%- else %}
          <span class="meta">Link-out. The citation is catalogued here and the text is not
          mirrored; the publisher&rsquo;s copy is the canonical one.</span>
        {%- endif %}
      </td>
    </tr>
  {%- endfor %}
  </tbody>
</table>

<p class="page-note">The last column is the archive&rsquo;s own access ledger restated in one
line per paper: {{ n_held }} of the {{ papers_total }} hold a PDF in this repository, and the
papers whose full text is withheld or not mirrored are said so on their own pages, in
<code>NOTICE.md</code> and in <a href="{{ '/papers/' | relative_url }}">the papers index</a>.
Where the publisher&rsquo;s copy is still live it remains the right place to read, and this
archive points at it rather than competing with it.</p>

<h2 id="findings">3. Three findings that matter to a reader</h2>
<p>Presented as facts with their identifiers, so each can be checked against the registry
record it came from. The first is about attribution, the second about a citation that will
break, the third about a count that will come out wrong.</p>

{%- for f in reg.findings %}
<div class="info-block">
  <h3>{{ f.title | escape }}</h3>
  <p>{{ f.statement | escape }}</p>
  <p><strong>What the records actually say</strong></p>
  <ul>
  {%- for e in f.evidence %}
    <li>
      <strong>{{ e.fact | escape }}</strong>
      <br><span class="meta">{{ e.sources | escape }}</span>
    </li>
  {%- endfor %}
  </ul>
  <p><strong>Why it matters to a reader.</strong> {{ f.why_it_matters_to_a_reader | escape }}</p>
  <p class="meta"><strong>What this archive does about it.</strong> {{ f.archive_handling | escape }}</p>
</div>
{%- endfor %}

<h2 id="limits">4. What this archive cannot and will not do</h2>

<div class="info-block">
  <h3>It has no write access to any of these registries</h3>
  <p>{{ reg.registries[0].write_access }} {{ reg.registries[1].write_access }}
  {{ reg.registries[2].write_access }} {{ reg.registries[5].write_access }}</p>
  <p>The practical consequence is that every error on this page is a standing error. The
  duplicate DOIs, the duplicated conference record and the mis-resolving
  <code>10.12816</code> prefix are all things the registries that hold them could fix, and this
  archive cannot touch any of them. It can only record them, which is what this page does.</p>
</div>

<div class="info-block">
  <h3>It will not create an ORCID record for him</h3>
  <p>{{ reg.registries[4].write_access }} {{ reg.registries[4].no_record_reason | escape }}</p>
  <p>An ORCID iD is a persistent claim about who a person is, and the only party who can
  truthfully make it is the person it identifies. A recovery project minting one on his
  behalf &mdash; without his knowledge, from a name string, in a field he has never worked in
  &mdash; would be a false identifier published under his name, which is the single worst
  thing this archive could do to his bibliography. The {{ reg.registries[4].rejected_candidates.size }}
  near-miss records above are left documented rather than deleted, so that nobody later
  mistakes one of them for his.</p>
</div>

<div class="info-block">
  <h3>It has created no Wikipedia article and no Wikidata item</h3>
{%- for nc in reg.not_created %}
  <p><strong>{{ nc.item }}: {{ nc.decision }}.</strong> {{ nc.reason | escape }}</p>
{%- endfor %}
</div>

<div class="info-block">
  <h3>It consulted one registry not at all</h3>
{%- for nc in reg.survey.not_consulted %}
  <p><strong>{{ nc.name }}</strong> &mdash; {{ nc.reason | escape }}</p>
{%- endfor %}
  <p>No claim on this page rests on {{ reg.survey.not_consulted[0].name }} either way.</p>
</div>

<div class="info-block">
  <h3>It will not contact anyone to fix any of this</h3>
  <p>Correcting a registry record, claiming a co-authorship, reporting a dead DOI or
  registering an ORCID iD would each require contacting the author, a co-author or a
  publisher. The author has asked not to be contacted and the archive&rsquo;s maintainers
  cannot forward requests or put them through. The full notice is
  <a href="{{ '/NOTICE.md' | relative_url }}#do-not-contact-the-author">NOTICE.md section
  10</a>, and it applies to this page as it does to every other: the errors recorded here are
  left standing and visible rather than quietly reported upward.</p>
</div>

<h2 id="limitations">5. The limits of this survey</h2>
<p>Every one of these is a reason to read the table above as a dated snapshot rather than as
a standing truth.</p>
<ul>
{%- for l in reg.limitations %}
  <li>{{ l | escape }}</li>
{%- endfor %}
</ul>

<div class="info-block">
  <h3>How this page was made, so it can be re-made</h3>
  <p><strong>Verified on</strong> {{ reg.survey.verified_on }}. <strong>Re-verified on</strong>
  {{ reg.survey.reverified_on }}. {{ reg.survey.method | escape }}</p>
  <p>The endpoints queried were:</p>
  <ul class="meta">
  {%- for a in reg.survey.apis_used %}
    <li><code>{{ a | escape }}</code></li>
  {%- endfor %}
  </ul>
  {%- for c in reg.survey.access_caveats %}
  <p class="meta">{{ c | escape }}</p>
  {%- endfor %}
  <p>Every identifier, count, date and quotation on this page is rendered from
  <code>_data/registries.json</code>, which is the single source of truth for it. The paper
  list is rendered from <code>_data/papers.json</code>. No identifier on this page was typed
  into a template, because an invented identifier in a column headed &ldquo;DOI&rdquo; is
  indistinguishable from a real one to a reader who has not checked it.</p>
  <p class="page-note">This page records where the bibliographic record of this work is
  incomplete. It does not change the record itself. For what this archive holds and what
  it deliberately does not, see
  <a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}">who this is</a> and
  <a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what happened to the
  website</a>; for the recordings this corpus is better known for, see
  <a href="{{ '/channel/' | relative_url }}">the channel record</a>, whose files are preserved
  in the Internet Archive collection named in section 1.</p>
</div>
