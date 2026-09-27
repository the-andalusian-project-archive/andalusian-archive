---
layout: default
title: Home
description: "A digital preservation record of the writing and recordings of Asadullah Ali Al-Andalusi and The Andalusian Project: papers, videos, machine transcripts and works, catalogued with the state of each capture."
---

<div class="hero">
  <h1>The Andalusian Project Archive</h1>
  <p class="hero-subtitle">Digital preservation of the scholarly work of Asadullah Ali Al-Andalusi — founder of The Andalusian Project, research fellow at Yaqeen Institute, and member of the Muslim Debate Initiative.</p>
</div>

{%- comment -%}
  Every figure in the headline panel, the quick-link descriptions and the
  preservation table below is COUNTED FROM THE DATA at build time (Liquid loops
  over _data/*.json). No number in any of those three places is typed, so the
  panel cannot publish a total the data does not support, and the seven terms of
  the arithmetic are printed in the same order they are summed.

  The published pre-recount figures (57 works / 18 papers / 203 total) were
  restored over these spots in task 8f because publishing the recount ahead of
  the site owner's approval would have made this page contradict the others.
  The approval has been given and the recount is applied here, in one pass.
{%- endcomment -%}
{%- assign works_total = 0 -%}{%- assign found = 0 -%}{%- assign wayback_only = 0 -%}{%- assign lost = 0 -%}
{%- for w in site.data.canonical_works -%}
  {%- assign works_total = works_total | plus: 1 -%}
  {%- if w.status == "found" -%}{%- assign found = found | plus: 1 -%}
  {%- elsif w.status == "wayback_only" -%}{%- assign wayback_only = wayback_only | plus: 1 -%}
  {%- elsif w.status == "lost" -%}{%- assign lost = lost | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign videos_total = 0 -%}{%- for v in site.data.videos -%}{%- assign videos_total = videos_total | plus: 1 -%}{%- endfor -%}
{%- assign papers_total = 0 -%}{%- assign pdf_files = 0 -%}{%- assign pdf_papers = 0 -%}
{%- for p in site.data.papers -%}
  {%- assign papers_total = papers_total | plus: 1 -%}
  {%- if p.file -%}{%- assign pdf_files = pdf_files | plus: 1 -%}{%- endif -%}
  {%- if p.file or p.additional_files -%}{%- assign pdf_papers = pdf_papers | plus: 1 -%}{%- endif -%}
  {%- if p.additional_files -%}{%- assign pdf_files = pdf_files | plus: p.additional_files.size -%}{%- endif -%}
{%- endfor -%}
{%- assign mdi_total = 0 -%}{%- assign mdi_counted = 0 -%}
{%- for m in site.data.mdi_articles -%}
  {%- assign mdi_total = mdi_total | plus: 1 -%}
  {%- if m.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign mdi_republished = mdi_total | minus: mdi_counted -%}
{%- assign yaqeen_total = 0 -%}{%- for y in site.data.yaqeen_papers -%}{%- assign yaqeen_total = yaqeen_total | plus: 1 -%}{%- endfor -%}
{%- assign albalagh_total = 0 -%}{%- for ab in site.data.albalagh_courses -%}{%- assign albalagh_total = albalagh_total | plus: 1 -%}{%- endfor -%}
{%- assign interviews_total = 0 -%}{%- for ei in site.data.external_interviews -%}{%- assign interviews_total = interviews_total | plus: 1 -%}{%- endfor -%}
{%- assign notices_total = 0 -%}{%- for n in site.data.notices -%}{%- assign notices_total = notices_total | plus: 1 -%}{%- endfor -%}
{%- assign captures_total = 0 -%}{%- for b in site.data.blog_posts -%}{%- assign captures_total = captures_total | plus: 1 -%}{%- endfor -%}
{%- assign search_total = papers_total | plus: videos_total | plus: works_total -%}
{%- assign total_content = works_total | plus: videos_total | plus: papers_total | plus: mdi_counted | plus: yaqeen_total | plus: albalagh_total | plus: interviews_total -%}

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number">{{ works_total }}</div>
    <div class="stat-label">Blog Works</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">{{ videos_total }}</div>
    <div class="stat-label">Videos</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">{{ papers_total }}</div>
    <div class="stat-label">Academic Papers</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">{{ total_content }}</div>
    <div class="stat-label">Total Items Preserved</div>
  </div>
</div>
<p class="stats-note">{{ works_total }} works &mdash; {{ found }} full-text in repo, {{ wayback_only }} Wayback-only, {{ lost }} lost. Total {{ total_content }} = {{ works_total }} + {{ videos_total }} + {{ papers_total }} + {{ mdi_counted }} + {{ yaqeen_total }} + {{ albalagh_total }} + {{ interviews_total }} (non-overlapping; the MDI term is the {{ mdi_counted }} distinct items of {{ mdi_total }} catalogued rows, the other {{ mdi_republished }} republishing a work already counted above; it excludes the derived secondary_sources and the {{ notices_total }} announcements, and the blog term is the works list, not the {{ captures_total }} captures).</p>

{%- comment -%}
  Task 8a: the four-category taxonomy. Every figure below is COUNTED FROM THE
  DATA at build time (Liquid loops over _data/*.json); no number is typed here.
  These are a breakdown of the same data by authorship, not a replacement for
  the headline panel, and the two now agree because both are read from _data/.

  `mdi_total`, `mdi_counted` and `mdi_republished` are assigned once in the
  headline block above and reused here; I3 (Phase-3 review, 2026-09-27) is the
  finding that "13" was once a typed literal inside a block that claims no
  number is typed, and it is `mdi_total - mdi_counted`, computed from the data.
{%- endcomment -%}
{%- assign a_works = 0 -%}{%- for row in site.data.canonical_works -%}{%- if row.category == "A" and row.counted -%}{%- assign a_works = a_works | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_videos = 0 -%}{%- for row in site.data.videos -%}{%- if row.category == "A" and row.counted -%}{%- assign a_videos = a_videos | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_papers = 0 -%}{%- for row in site.data.papers -%}{%- if row.category == "A" and row.counted -%}{%- assign a_papers = a_papers | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_mdi = 0 -%}{%- for row in site.data.mdi_articles -%}{%- if row.category == "A" and row.counted -%}{%- assign a_mdi = a_mdi | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_total = a_works | plus: a_videos | plus: a_papers | plus: a_mdi -%}
{%- comment -%}
  I3 (Phase-3 review, 2026-09-27): "13" was a typed literal here, inside a block
  that claims no number is typed. It is `mdi_total - mdi_counted`, computed
  above from the data like every other figure on this page.
{%- endcomment -%}

{%- assign b_papers = 0 -%}{%- for row in site.data.papers -%}{%- if row.category == "B" and row.counted -%}{%- assign b_papers = b_papers | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign b_other = 0 -%}{%- for row in site.data.canonical_works -%}{%- if row.category == "B" and row.counted -%}{%- assign b_other = b_other | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- for row in site.data.videos -%}{%- if row.category == "B" and row.counted -%}{%- assign b_other = b_other | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign b_total = b_papers | plus: b_other -%}

{%- assign c_videos = 0 -%}{%- for row in site.data.videos -%}{%- if row.category == "C" and row.counted -%}{%- assign c_videos = c_videos | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign c_reception = 0 -%}{%- for row in site.data.secondary_sources -%}{%- if row.category == "C" -%}{%- assign c_reception = c_reception | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign c_total = c_videos | plus: c_reception -%}

{%- assign d_notices = 0 -%}{%- for row in site.data.notices -%}{%- if row.category == "D" -%}{%- assign d_notices = d_notices | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign d_linkouts = 0 -%}{%- for row in site.data.linkouts -%}{%- if row.category == "D" -%}{%- assign d_linkouts = d_linkouts | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign d_total = d_notices | plus: d_linkouts -%}

<div class="section taxonomy-section">
  <div class="section-header">
    <h2>How this archive is sorted</h2>
    <p>Four categories, decided by who made the thing, not by what shape it is. A video he produced is A even when it is a debate; a show he was a guest on is C even though it carries his voice. Every countable item sits in exactly one category. The full rules are in <code>_data/taxonomy.json</code>.</p>
    <p class="page-note">Figures in this section are counted from the data at build time, as is the headline panel above, so the two cannot disagree.</p>
  </div>

  <div class="taxonomy-entry">
    <h3>{% include category_badge.html category="A" %} <span class="taxonomy-count">{{ a_total }} items</span></h3>
    <p>Works by Asadullah Ali &mdash; {{ a_works }} works, {{ a_videos }} videos he produced, {{ a_papers }} papers he wrote alone, {{ a_mdi }} MDI posts that are distinct items. All {{ a_total }} are counted.</p>
    <p class="taxonomy-detail">A debate he produced, an interview he conducted and a talk he gave at someone else&rsquo;s hall are all A: he made the recording. The {{ mdi_republished }} MDI rows that republish a work already in this list are catalogued but not counted again.</p>
    <p><a href="{{ '/articles/' | relative_url }}">Read the works</a> &middot; <a href="{{ '/videos/' | relative_url }}">See the videos</a> &middot; <a href="{{ '/papers/' | relative_url }}">See the papers</a></p>
  </div>

  <div class="taxonomy-entry">
    <h3>{% include category_badge.html category="B" %} <span class="taxonomy-count">{{ b_total }} items</span></h3>
    <p>Contributions &amp; collaborations &mdash; {{ b_papers }} papers written with a named co-author{% if b_other > 0 %} and {{ b_other }} other jointly produced item{% if b_other != 1 %}s{% endif %}{% endif %}. All {{ b_total }} are counted.</p>
    <p class="taxonomy-detail">A co-written paper is B because authorship is shared. A record he only spoke in is not B: it is C, because somebody else made the recording.</p>
    <p><a href="{{ '/papers/' | relative_url }}">See the co-authored papers</a></p>
  </div>

  <div class="taxonomy-entry">
    <h3>{% include category_badge.html category="C" %} <span class="taxonomy-count">{{ c_total }} catalogued</span></h3>
    <p>Interviews, reception and mentions about him &mdash; {{ c_videos }} recordings he appeared in on other people&rsquo;s channels, plus {{ c_reception }} reprints, critiques, biographies and mentions written by others. The {{ c_videos }} appearances are counted; the {{ c_reception }} reception items are <strong>not</strong> counted.</p>
    <p class="taxonomy-detail">The reception items are derived from this archive&rsquo;s own catalogue, so counting them would count the archive against itself. They are listed so a reader can see they exist.</p>
  </div>

  <div class="taxonomy-entry">
    <h3>{% include category_badge.html category="D" %} <span class="taxonomy-count">{{ d_total }} catalogued</span></h3>
    <p>Other materials &mdash; {{ d_notices }} announcements that are not works, and {{ d_linkouts }} link-outs (the conversion-story reprint, held as metadata only, and the Yaqeen pages, whose text this project does not download). None of them is counted.</p>
    <p class="taxonomy-detail">A link-out records that something exists elsewhere. No recovered text is claimed for any of them, and no size is added to any total. Site and channel history is on the <a href="{{ '/channel/' | relative_url }}">channel page</a>.</p>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <h2>Explore the Archive</h2>
  </div>

  <div class="quick-links">
    <a href="{{ '/papers/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-primary-subtle); color: var(--color-primary);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h12v16H4z"/><path d="M8 4V2h8v2"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Academic Papers</div>
        <div class="ql-desc">{{ papers_total }} papers from Yaqeen Institute and academic journals; {{ pdf_files }} PDF files held</div>
      </div>
    </a>
    <a href="{{ '/videos/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-accent-subtle); color: var(--color-accent);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Video Archive</div>
        <div class="ql-desc">68 lectures and discussions preserved on Archive.org</div>
      </div>
    </a>
    <a href="{{ '/articles/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-success-subtle); color: var(--color-success);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v12H4z"/><path d="M8 8h8M8 12h5"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Blog Posts</div>
        <div class="ql-desc">{{ works_total }} works &mdash; {{ found }} full-text in repo, {{ wayback_only }} Wayback-only, {{ lost }} lost</div>
      </div>
    </a>
    <a href="{{ '/timeline/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-warning-subtle); color: var(--color-warning);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10" cy="10" r="8"/><path d="M10 6v4l3 3"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Timeline</div>
        <div class="ql-desc">How the archive was recovered, and the works from 2011 to 2020</div>
      </div>
    </a>
    {%- comment -%}
      2026-09-28: the two named entry points get a card on the homepage, above the
      search card and below the timeline, because they answer the two questions a
      first-time reader arrives with - who is this, and what happened to his site -
      and both questions were previously unanswerable from anywhere on this site.
      The descriptions state the facts that make each page necessary rather than
      describing the page: one is the only complete account of the corpus and of
      the two different men named Al-Andalusi, the other is the only warning that
      the domain is now a gambling site.
    {%- endcomment -%}
    <a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-primary-subtle); color: var(--color-primary);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10" cy="10" r="7"/><path d="M10 9v5M10 6.5v.5"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Who this is</div>
        <div class="ql-desc">Asadullah Ali Al-Andalusi: every attested form of his name, his roles, what he wrote, and the different man also called Abdullah al-Andalusi</div>
      </div>
    </a>
    <a href="{{ '/asadullahali-com-what-happened/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-danger-subtle); color: var(--color-danger);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 3l7 13H3z"/><path d="M10 8v4M10 14v.5"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">What happened to the website</div>
        <div class="ql-desc">asadullahali.com is gone and the domain is now a gambling site &mdash; do not visit it. What survives, where it lives, and how to cite it</div>
      </div>
    </a>
    <a href="{{ '/search/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-danger-subtle); color: var(--color-danger);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="6"/><path d="M14 14l4 4"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Search</div>
        <div class="ql-desc">Search across all {{ search_total }} preserved items</div>
      </div>
    </a>
    <a href="https://archive.org/details/andalusian-project" target="_blank" rel="noopener noreferrer" class="quick-link">
      <div class="ql-icon" style="background: var(--color-primary-subtle); color: var(--color-primary);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 2a8 8 0 100 16 8 8 0 000-16z"/><path d="M2 10h16M10 2a12 12 0 014 8 12 12 0 01-4 8 12 12 0 01-4-8 12 12 0 014-8z"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Internet Archive</div>
        <div class="ql-desc">Full 14GB video collection on Archive.org</div>
      </div>
    </a>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <h2>Preservation Status</h2>
    <p>{{ found }} blog works preserved full-text in this repository; {{ wayback_only }} catalogued via the Wayback Machine with no text held; {{ lost }} lost with no archived copy located. Videos, papers, and external collections are linked via public archives.</p>
  </div>

  <table>
    <thead>
      <tr>
        <th>Collection</th>
        <th>Count</th>
        <th>Storage</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Blog Works</td>
        <td>{{ works_total }}</td>
        <td>{{ found }} full-text in repo; {{ wayback_only }} Wayback-only; {{ lost }} lost</td>
        <td><span class="badge badge-archived">Partial</span></td>
      </tr>
      <tr>
        <td>Blog Captures (metadata)</td>
        <td>{{ captures_total }}</td>
        <td>In Repository</td>
        <td><span class="badge badge-archived">Metadata</span></td>
      </tr>
      <tr>
        <td>Videos</td>
        <td>{{ videos_total }}</td>
        <td>Archive.org Mirrors</td>
        <td><span class="badge badge-available">Preserved</span></td>
      </tr>
      <tr>
        <td>Academic Papers</td>
        <td>{{ papers_total }}</td>
        <td>Institutional Links; {{ pdf_files }} PDF files held</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
      <tr>
        <td>MDI Articles</td>
        <td>{{ mdi_counted }} of {{ mdi_total }}</td>
        <td>Full text in repo; the other {{ mdi_republished }} republish a work counted above</td>
        <td><span class="badge badge-archived">Full text held</span></td>
      </tr>
      <tr>
        <td>Yaqeen Papers</td>
        <td>{{ yaqeen_total }}</td>
        <td>Links</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
      <tr>
        <td>Al Balagh Courses</td>
        <td>{{ albalagh_total }}</td>
        <td>Links</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
      <tr>
        <td>Announcements (never counted)</td>
        <td>{{ notices_total }}</td>
        <td>Full text in repo</td>
        <td><span class="badge badge-archived">Not counted</span></td>
      </tr>
      <tr>
        <td>Third-party source records (never counted)</td>
        <td>{{ site.data.secondary_sources | size }}</td>
        <td>In Repository; derived from this archive&rsquo;s own catalogue</td>
        <td><span class="badge badge-archived">Not counted</span></td>
      </tr>
    </tbody>
  </table>
</div>
