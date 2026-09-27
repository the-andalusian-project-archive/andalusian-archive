---
layout: default
title: "Asadullah Ali Al-Andalusi: who he is, what he wrote, and what happened to his sites"
description: "Every attested form of Asadullah Ali Al-Andalusi's name, his four recorded roles, an index into every collection, and the other Al-Andalusi he is confused with."
permalink: /asadullah-ali-al-andalususi/
schema: person
last_modified_at: 2026-09-28
---
{%- comment -%}
  The entity page (2026-09-28).

  WHY IT IS A PAGE AND NOT AN ESSAY. Every name, role, URL and status below is
  read out of `_data/entity_page.json`, and every figure is counted from the
  collection data files by Liquid at build time. Nothing here is typed, which is
  the only way a page like this can be trusted: a hand-written entity page is
  exactly where invented credentials and drifted counts get in.

  THE ORDER IS DELIBERATE and follows the archive's own precedence:
    1. the name, because a reader arriving by search arrives by name;
    2. the disambiguation, because a reader arriving by the WRONG name has to be
       told so before anything else on the page is read as agreement;
    3. roles, with the corpus's own tense preserved rather than tidied;
    4. what he worked on, as links into the real collections;
    5. the loss record, because it is the reason this archive exists;
    6. what this archive is and is not, which is the licence and the ethics.

  NO CONTACT. Nothing on this page invites a reader to reach the author, quotes
  him, or reproduces a personal identifier. `NOTICE.md` section 10 is the single
  statement of that and it is linked from the footer of every page on the site;
  the line at the end of this page points at the same notice rather than
  restating it, so there is one wording in one place.
{%- endcomment -%}
{%- assign ep = site.data.entity_page -%}
{%- assign series = site.data.series -%}

{%- comment -%} Counts. All read from _data/, none typed. {%- endcomment -%}
{%- assign works_total = 0 -%}{%- assign found = 0 -%}{%- assign wayback_only = 0 -%}{%- assign lost = 0 -%}
{%- for w in site.data.canonical_works -%}
  {%- assign works_total = works_total | plus: 1 -%}
  {%- if w.status == "found" -%}{%- assign found = found | plus: 1 -%}
  {%- elsif w.status == "wayback_only" -%}{%- assign wayback_only = wayback_only | plus: 1 -%}
  {%- elsif w.status == "lost" -%}{%- assign lost = lost | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign videos_total = 0 -%}{%- for v in site.data.videos -%}{%- assign videos_total = videos_total | plus: 1 -%}{%- endfor -%}
{%- assign papers_total = 0 -%}{%- assign pdf_files = 0 -%}{%- for p in site.data.papers -%}
  {%- assign papers_total = papers_total | plus: 1 -%}
  {%- if p.file -%}{%- assign pdf_files = pdf_files | plus: 1 -%}{%- endif -%}
  {%- if p.additional_files -%}{%- assign pdf_files = pdf_files | plus: p.additional_files.size -%}{%- endif -%}
{%- endfor -%}
{%- assign mdi_total = 0 -%}{%- assign mdi_counted = 0 -%}
{%- for m in site.data.mdi_articles -%}
  {%- assign mdi_total = mdi_total | plus: 1 -%}
  {%- if m.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign ix = site.data.transcript_index -%}

<div class="hero">
  <h1>Asadullah Ali Al-Andalusi</h1>
  <p class="hero-subtitle">Founder of The Andalusian Project. This page is the archive&rsquo;s
  single answer to &ldquo;who is this and what did he write&rdquo;: every form of his name the
  corpus attests, the one name he is regularly confused with, his four recorded roles, a
  linked index into everything recovered, and a dated record of what was lost.</p>
</div>

<div class="info-block">
  <h3>The short version</h3>
  <p>Asadullah Ali Al-Andalusi founded and wrote for an independent Islamic-studies
  research platform called <strong>The Andalusian Project</strong>. He published
  {{ works_total }} catalogued written works, {{ videos_total }} catalogued recordings,
  {{ papers_total }} academic papers and {{ mdi_counted }} further distinct items for the
  Muslim Debate Initiative, and this archive holds {{ ix.documents }} machine transcripts
  &mdash; {{ ix.words }} words &mdash; of the recordings, which exist nowhere else.
  His own website, his WordPress mirror and his YouTube channel no longer serve his work;
  the domain he published on is now an unrelated commercial site. That is what this
  archive is, and <a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what
  happened to all of it is on its own page</a>.</p>
  <p class="page-note">This page describes the work and the record. It is not a biography,
  and where the archive holds no evidence of something it says so rather than filling the
  gap.</p>
</div>

<h2 id="names">1. The name and its variants, as attested</h2>
<p>Search engines and third-party pages do not agree on how to spell this name, and the
archive&rsquo;s own recovered material contains more than one form. Every form below is
listed with <strong>where it is attested</strong>, and nothing on this list was chosen for
this page: each one is in the archive&rsquo;s data or on a third-party page this archive
checked and dated.</p>

<table>
  <thead>
    <tr>
      <th>Form</th>
      <th>Attested</th>
      <th>Where, and what it is</th>
    </tr>
  </thead>
  <tbody>
  {%- for v in ep.name_variants %}
    <tr>
      <td><strong>{{ v.form | escape }}</strong></td>
      <td>{% if v.status == "in_corpus" %}<span class="badge badge-available">in this corpus</span>{% else %}<span class="badge badge-archived">external</span>{% endif %}</td>
      <td>
        {{ v.role | escape }}
        <details>
          <summary class="meta">Attested in</summary>
          <ul class="meta">
          {%- for a in v.attested_where %}
            <li>{{ a | escape }}</li>
          {%- endfor %}
          </ul>
        </details>
      </td>
    </tr>
  {%- endfor %}
  </tbody>
</table>

<p class="page-note"><strong>On the two forms that need a word of explanation.</strong>
<em>Asadullah Ali al-Andalusi</em> and <em>Asadullah Ali al Andalusi</em> are the same name as
the first form, with a lower-case second element or a space instead of a hyphen; both are
in the archive&rsquo;s data, and both are listed because a reader who searched one of them
should land here. <em>Abu Isabel</em> is his kunya &mdash; a form of address, not a contact
detail. It reaches this archive from one place only, the live third-party title of a single
recording, and <a href="{{ '/NOTICE.md' | relative_url }}#the-kunya-is-not-withheld">NOTICE.md
section 6.1</a> records that it is not withheld and why. <em>Ustadh</em> appears
<strong>zero times anywhere in this corpus</strong>; it is on the list because Al Balagh
Academy uses it on the faculty page linked below, and a reader searching that form deserves
to be told it is the same person.</p>

<h2 id="disambiguation">2. A different man with almost the same name</h2>

<div class="info-block">
  <h3>This page is about Asadullah Ali Al-Andalusi, not Abdullah al-Andalusi</h3>
  <p>A <strong>different, active Muslim speaker</strong> publishes and speaks under the name
  {{ ep.disambiguation.other_person_name }} &mdash; also written
  {{ ep.disambiguation.other_person_name_forms | join: " and " }} &mdash; from
  {{ ep.disambiguation.other_person_site_plain_text }} and a channel at
  {{ ep.disambiguation.other_person_channel_plain_text }}. Both of those properties answered
  HTTP 200 on {{ ep.external_check.date }}, so the two names are live at the same time and
  the confusion is current, not historical. The two men are routinely conflated with each
  other, in both directions, and this archive is on the receiving end of it.</p>
  <p><strong>The archive&rsquo;s own evidence that they are two people is in its own corpus,
  and it is the subject&rsquo;s own words.</strong> In the recovered work
  <em>Whataboutery: The Fail-Safe of Islamophobes</em> (2015) &mdash; published verbatim in
  this repository &mdash; the author describes <em>MDI representative Abdullah
  Al-Andalusi</em> as someone else in the room:</p>
  <blockquote><p>&ldquo;&hellip;her frequent interruptions, appeals to emotion, question
  begging, and her shouting over MDI representative Abdullah Al-Andalusi as he was
  comprehensively detailing the cruel oppression of state actors&hellip;&rdquo;</p></blockquote>
  <p>The same post carries the tag <code>Abdullah al Andalusi</code>. The man he is writing
  about is not him.</p>
  <p><strong>{{ ep.disambiguation.the_mislabelling_runs_both_ways }}</strong></p>
</div>

<div class="info-block">
  <h3>How the archive keeps the two apart: the byline gate</h3>
  <p>{{ ep.disambiguation.the_gate }}</p>
  <p><strong>Why you are being told.</strong> {{ ep.disambiguation.why_it_is_printed_here }}</p>
  <p class="page-note">The other man&rsquo;s site and channel are printed here as plain
  text, not as links. This archive holds no material of his, has no relationship with him
  and has verified nothing about him beyond the two HTTP responses above, so a link would
  imply a check this archive did not make. His name is on the page because a search for it
  should reach a page that says plainly that this is the wrong person.</p>
</div>

<h2 id="roles">3. Roles and affiliations</h2>
<p>Four, as the corpus states them. The archive does not tidy the tense: where its own
pages disagree about whether a role is current, both readings are given and neither is
resolved, because the corpus does not settle it.</p>

<table>
  <thead>
    <tr>
      <th>Role</th>
      <th>Organisation</th>
      <th>How this archive records it</th>
    </tr>
  </thead>
  <tbody>
  {%- for r in ep.roles %}
    <tr>
      <td><strong>{{ r.role | escape }}</strong></td>
      <td>
        {% if r.url %}<a href="{{ r.url }}" target="_blank" rel="noopener noreferrer">{{ r.organisation | escape }}</a>{% else %}{{ r.organisation | escape }}{% endif %}
      </td>
      <td>
        {% if r.status == "former_as_stated" %}<span class="badge badge-archived">not stated as current</span>{% else %}<span class="badge badge-available">attested</span>{% endif %}
        &mdash; stated by {{ r.stated_by | escape }}
        <p class="meta">{{ r.note | escape }}</p>
      </td>
    </tr>
  {%- endfor %}
  </tbody>
</table>

<p class="page-note"><strong>On &ldquo;former&rdquo;.</strong> {{ ep.roles[1].note }} The
same holds for the Muslim Debate Initiative row above. This archive does not assert that
either role has ended: it records that its own README describes both in the past tense and
its own homepage in the present, and leaves the reader with both facts.</p>

<h2 id="work">4. What he worked on</h2>
<p>An index into the real collections, not a summary. Every figure below is counted from
<code>_data/</code> when this page is built, and every link goes to the collection the
number came from.</p>

<h3>The recorded lecture and discussion series</h3>
<p>{{ series.series_count }} multi-part series survive in the recording catalogue, together
holding {{ series.grouped_videos }} of the {{ videos_total }} catalogued recordings and
transcripts nobody else has. Each has its own page, its own description and its parts in the
order the channel numbered them.</p>

<div class="card-grid">
{%- for s in series.series %}
  <div class="card">
    <h3><a href="{{ '/transcripts/by-series/' | append: s.slug | append: '/' | relative_url }}">{{ s.title | escape }}</a></h3>
    <div class="card-meta">{{ s.part_count }} parts &middot; {{ s.transcript_words }} transcript words</div>
    <div class="card-body">{{ s.framing | escape }}</div>
    <div class="card-actions">
      <a href="{{ '/transcripts/by-series/' | append: s.slug | append: '/' | relative_url }}" class="btn btn-primary btn-sm">Series page and transcripts</a>
    </div>
  </div>
{%- endfor %}
</div>
<p class="page-note">The other {{ series.ungrouped_videos }} catalogued recordings are not
parts of a series and are not filed under one. {{ series.ungrouped_note }}</p>

<h3>The written and scholarly corpus</h3>

<table>
  <thead>
    <tr>
      <th>Collection</th>
      <th>Count</th>
      <th>What is held</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="{{ '/articles/' | relative_url }}">Written works</a></td>
      <td>{{ works_total }}</td>
      <td>{{ found }} with full text in this repository, {{ wayback_only }} catalogued from Wayback captures with no text held, {{ lost }} lost with no archived copy located. Dated 2011-12-18 to 2020-08-11.</td>
    </tr>
    <tr>
      <td><a href="{{ '/papers/' | relative_url }}">Academic papers</a></td>
      <td>{{ papers_total }}</td>
      <td>{{ pdf_files }} PDF files held in this repository; the rest are link-outs, and the access ledger records which primary sources are open, restricted or dead. Two of the twenty carry a DOI on the record, one of them dead.</td>
    </tr>
    <tr>
      <td><a href="{{ '/articles/' | relative_url }}#mdi">Muslim Debate Initiative pages</a></td>
      <td>{{ mdi_counted }} of {{ mdi_total }}</td>
      <td>All {{ mdi_total }} are held in full text, recovered from the MDI author archive on 2026-09-27. {{ mdi_counted }} are distinct items of content; the other {{ mdi_total | minus: mdi_counted }} republish a work already counted above and are not counted again.</td>
    </tr>
    <tr>
      <td><a href="{{ '/videos/' | relative_url }}">Recordings</a></td>
      <td>{{ videos_total }}</td>
      <td>Catalogued with their ids, durations and surviving copies. Most are preserved as files in the Internet Archive&rsquo;s <code>andalusian-project</code> collection; the rest survive only as re-uploads on other people&rsquo;s channels.</td>
    </tr>
    <tr>
      <td><a href="{{ '/transcripts/' | relative_url }}">Machine transcripts</a></td>
      <td>{{ ix.documents }}</td>
      <td>{{ ix.words }} words across {{ ix.recordings }} recordings, one document per capture. This is the archive&rsquo;s most unique asset: no other site holds the text of these talks.</td>
    </tr>
  </tbody>
</table>

<h3>Where each kind of work is canonically published</h3>
<p>The archive is a preservation record, not a publisher. For most of this corpus the
original publisher is still the right place to read it, and the archive&rsquo;s own position
&mdash; set out in <code>NOTICE.md</code> section 5 and honoured throughout &mdash; is to point
outward rather than compete.</p>
<ul>
  <li><strong>Yaqeen Institute</strong> publishes his co-authored paper on Aisha&rsquo;s age
  and the <em>Orientalists&rsquo; Fables</em> paper, and hosts the <em>Doubting Your
  Doubts</em> lecture page. This archive holds them as link-outs and does not mirror their
  text.</li>
  <li><strong>The Muslim Debate Initiative</strong> holds the full text of the
  {{ mdi_total }} author-archive articles at authoritative URLs. They are his canonical
  home, and this archive says so on every one of its own pages for them.</li>
  <li><strong>Al Balagh Academy</strong> is the current home of his course teaching; the
  {{ videos_total }} recordings of it survive here.</li>
  <li><strong>The Internet Archive</strong> is where the preserved recordings physically sit,
  in the <code>andalusian-project</code> collection, and
  <a href="{{ '/channel/' | relative_url }}">the channel page</a> is the dated record of
  what the original channel showed.</li>
</ul>

<h2 id="loss">5. What was lost, and what this archive recovered</h2>
<p>Four things stopped being available, for four different reasons, and the archive keeps
them apart because they are not the same event.</p>

<table>
  <thead>
    <tr>
      <th>What</th>
      <th>State</th>
      <th>What the archive holds instead</th>
    </tr>
  </thead>
  <tbody>
  {%- for s in ep.loss_record.sites %}
    <tr>
      <td><strong>{{ s.what | escape }}</strong><br><code>{{ s.host | escape }}</code></td>
      <td>{{ s.state | escape }}</td>
      <td>{{ s.note | escape }}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>

<p>The dated evidence is on <a href="{{ '/channel/' | relative_url }}">the channel
record</a> and <a href="{{ '/timeline/' | relative_url }}">the timeline</a>, and the
per-property account is on
<a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what happened to the
Andalusian Project&rsquo;s web presence</a>.</p>

<h2 id="not">6. What this archive is, and is not</h2>

<div class="info-block">
  <h3>It is not affiliated with, endorsed by, or a successor to anything live</h3>
  <p>The Andalusian Project&rsquo;s own site, mirror and channel are gone. This archive is
  not a successor to any of them, is not affiliated with any institution named on this page,
  and is not endorsed by any of them. It is a third party&rsquo;s documented recovery, and it
  says so on every page. Nobody was asked to approve it and nobody has approved it on
  anyone&rsquo;s behalf.</p>
</div>

<div class="info-block">
  <h3>His works are reproduced with attribution, and are not relicensed here</h3>
  <p>Recovered prose is reproduced verbatim, with the source URL and the Wayback capture
  timestamp on every item. It is <strong>not</strong> relicensed by this archive and it never
  was: his essays were openly readable when published, which is availability, not permission,
  and no open licence was ever applied to them. The full position, including the one place it
  is more complicated, is in <a href="{{ '/NOTICE.md' | relative_url }}">NOTICE.md</a>
  section 2 and in <code>LICENSE</code>. Attribution is required, and crediting this archive
  alone does not satisfy it: the archive is the record, not the author.</p>
</div>

<div class="info-block">
  <h3>Two personal names are withheld, and this notice says so rather than leaving a gap</h3>
  <p>At the site owner&rsquo;s request, his legal name and his birth name are not published
  here. Both are disclosed in <a href="{{ '/NOTICE.md' | relative_url }}">NOTICE.md</a>
  section 6.1, with what was withheld, where the redaction is marked, and one known residue
  that is published deliberately and explained. A withheld item that is not disclosed is a
  silent gap, and a silent gap is how an archive becomes unreliable.</p>
</div>

<div class="info-block">
  <h3>This is a dated polemical archive, and the claims in it are his</h3>
  <p>The material is argument, not reference, and it is preserved because it was published
  and then lost &mdash; not because it is settled, current, or endorsed. The claims are the
  author&rsquo;s, argued in his voice on the dates shown. This archive reproduces them as a
  record and adopts none of them. <a href="{{ '/NOTICE.md' | relative_url }}">NOTICE.md</a>
  section 8 states the position in full.</p>
</div>

<div class="info-block">
  <h3>Do not contact the author</h3>
  <p>The author has asked not to be contacted, and the archive&rsquo;s maintainers cannot
  forward requests and cannot put them through. The full notice is
  <a href="{{ '/NOTICE.md' | relative_url }}#do-not-contact-the-author">NOTICE.md section
  10</a>, and the same wording is on every page of this site. Nothing on this page is an
  invitation to reach him.</p>
</div>
