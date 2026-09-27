---
layout: default
title: Home
---

<div class="hero">
  <h1>The Andalusian Project Archive</h1>
  <p class="hero-subtitle">Digital preservation of the scholarly work of Asadullah Ali Al-Andalusi — founder of The Andalusian Project, research fellow at Yaqeen Institute, and member of the Muslim Debate Initiative.</p>
</div>

<!-- Task 3 honest counts (Task 0 ruling): total = 57 works + 68 videos + 18 papers + 17 MDI + 9 Yaqeen + 33 AlBalagh + 1 interview = 203. Excludes derived secondary_sources; blog uses the works list (canonical_works) not 87 CDX captures. -->
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number">57</div>
    <div class="stat-label">Blog Works</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">68</div>
    <div class="stat-label">Videos</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">18</div>
    <div class="stat-label">Academic Papers</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">203</div>
    <div class="stat-label">Total Items Preserved</div>
  </div>
</div>
<p class="stats-note">57 works &mdash; 30 full-text in repo, 2 lost, 25 Wayback-only. Total 203 = 57 + 68 + 18 + 17 + 9 + 36 + 1 (non-overlapping; excludes derived secondary_sources; blog counts works, not 87 captures).</p>

{%- comment -%}
  Task 8a: the four-category taxonomy. Every figure below is COUNTED FROM THE
  DATA at build time (Liquid loops over _data/*.json); no number is typed here.
  The published headline numbers in the stats grid above are deliberately
  UNCHANGED: the recount of the headline totals is Task 9's gate and the site
  owner has not approved new totals yet. The counts in this block are a
  breakdown of the same data by authorship, not a replacement for the headline.
{%- endcomment -%}
{%- assign a_works = 0 -%}{%- for row in site.data.canonical_works -%}{%- if row.category == "A" and row.counted -%}{%- assign a_works = a_works | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_videos = 0 -%}{%- for row in site.data.videos -%}{%- if row.category == "A" and row.counted -%}{%- assign a_videos = a_videos | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_papers = 0 -%}{%- for row in site.data.papers -%}{%- if row.category == "A" and row.counted -%}{%- assign a_papers = a_papers | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_mdi = 0 -%}{%- for row in site.data.mdi_articles -%}{%- if row.category == "A" and row.counted -%}{%- assign a_mdi = a_mdi | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign a_total = a_works | plus: a_videos | plus: a_papers | plus: a_mdi -%}
{%- comment -%}
  I3 (Phase-3 review, 2026-09-27): "13" was a typed literal here, inside a block
  that claims no number is typed. It is `mdi_total - mdi_counted`, so it is
  computed from the data like every other figure in this block.
{%- endcomment -%}
{%- assign mdi_total = 0 -%}{%- for row in site.data.mdi_articles -%}{%- assign mdi_total = mdi_total | plus: 1 -%}{%- endfor -%}
{%- assign mdi_counted = 0 -%}{%- for row in site.data.mdi_articles -%}{%- if row.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}{%- endfor -%}
{%- assign mdi_republished = mdi_total | minus: mdi_counted -%}

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
    <p class="page-note">Figures in this section are counted from the data at build time. The headline totals in the panel above are unchanged pending the site owner&rsquo;s approval of the recount.</p>
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
        <div class="ql-desc">18 papers from Yaqeen Institute and academic journals</div>
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
        <div class="ql-desc">57 works &mdash; 30 full-text in repo, 2 lost, 25 Wayback-only</div>
      </div>
    </a>
    <a href="{{ '/timeline/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-warning-subtle); color: var(--color-warning);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10" cy="10" r="8"/><path d="M10 6v4l3 3"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Timeline</div>
        <div class="ql-desc">Key milestones from 2011 to 2023</div>
      </div>
    </a>
    <a href="{{ '/search/' | relative_url }}" class="quick-link">
      <div class="ql-icon" style="background: var(--color-danger-subtle); color: var(--color-danger);">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="6"/><path d="M14 14l4 4"/></svg>
      </div>
      <div class="ql-text">
        <div class="ql-title">Search</div>
        <div class="ql-desc">Search across all 143 preserved items</div>
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
    <p>30 blog works preserved full-text in this repository; 25 available via the Wayback Machine only; 2 lost with no archived copy located. Videos, papers, and external collections are linked via public archives.</p>
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
        <td>57</td>
        <td>30 full-text in repo; 25 Wayback-only; 2 lost</td>
        <td><span class="badge badge-archived">Partial</span></td>
      </tr>
      <tr>
        <td>Blog Captures (metadata)</td>
        <td>87</td>
        <td>In Repository</td>
        <td><span class="badge badge-archived">Metadata</span></td>
      </tr>
      <tr>
        <td>Videos</td>
        <td>68</td>
        <td>Archive.org Mirrors</td>
        <td><span class="badge badge-available">Preserved</span></td>
      </tr>
      <tr>
        <td>Academic Papers</td>
        <td>18</td>
        <td>Institutional Links</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
      <tr>
        <td>MDI Articles</td>
        <td>17</td>
        <td>Links</td>
        <td><span class="badge badge-archived">Linked</span></td>
      </tr>
      <tr>
        <td>Yaqeen Papers</td>
        <td>9</td>
        <td>Links</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
      <tr>
        <td>Al Balagh Courses</td>
        <td>33</td>
        <td>Links</td>
        <td><span class="badge badge-available">Available</span></td>
      </tr>
    </tbody>
  </table>
</div>
