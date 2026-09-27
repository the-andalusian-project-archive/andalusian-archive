---
layout: default
title: "asadullahali.com and the Andalusian Project website: what happened, and where the work is now"
description: "The Andalusian Project's site is gone and its domain is now a gambling site - do not visit. What happened to the site, the mirror, the channel, and how to cite it."
permalink: /asadullahali-com-what-happened/
schema: faq
last_modified_at: 2026-09-28
---
{%- comment -%}
  The lost-and-found page (2026-09-28).

  WHY THIS PAGE IS THE ARCHIVE'S MOST VALUABLE SINGLE ASSET. A search for this
  man's name, or for his site, or for what happened to his project, currently
  returns a live page on a hijacked domain that serves slot gambling, and nothing
  else that answers the question. The gambling page ranks because it is on the
  exact-match domain, not because anyone vouched for it. Nobody on the web is
  publishing a factual account of what happened, which means this page competes
  with nothing and is the only honest answer available.

  THE DOMAIN IS PLAIN TEXT AND MUST STAY THAT WAY. It is written in this comment
  and in the body below as a bare string, never inside an `href`. The rule is
  `NOTICE.md` section 7 and it is implemented in `_includes/source_link.html`,
  which prints a URL on that host as text with the reason attached and leaves the
  Wayback capture as the clickable source. A link here would send a reader who
  searched his name to a gambling site, and the warning is the entire value of
  this page. Do not add one.

  NO CONTACT. Nothing here invites a reader to reach the author or reproduces a
  personal identifier. The archive is the destination for citations, not for
  messages, and the notice at the end says so.

  THE FAQ BLOCK. The questions below are read from `_data/entity_page.json` ->
  `queries`, and the same file supplies the `short` answer that the FAQPage
  structured data in `_includes/jsonld.html` publishes. One list, two surfaces,
  word for word identical - which is the only way an FAQPage stays honest.
{%- endcomment -%}
{%- assign ep = site.data.entity_page -%}
{%- assign ix = site.data.transcript_index -%}

{%- comment -%} Counts, all read from _data/. {%- endcomment -%}
{%- assign works_total = 0 -%}{%- assign found = 0 -%}{%- assign wayback_only = 0 -%}{%- assign lost = 0 -%}
{%- for w in site.data.canonical_works -%}
  {%- assign works_total = works_total | plus: 1 -%}
  {%- if w.status == "found" -%}{%- assign found = found | plus: 1 -%}
  {%- elsif w.status == "wayback_only" -%}{%- assign wayback_only = wayback_only | plus: 1 -%}
  {%- elsif w.status == "lost" -%}{%- assign lost = lost | plus: 1 -%}{%- endif -%}
{%- endfor -%}
{%- assign videos_total = 0 -%}{%- for v in site.data.videos -%}{%- assign videos_total = videos_total | plus: 1 -%}{%- endfor -%}
{%- assign papers_total = 0 -%}{%- for p in site.data.papers -%}{%- assign papers_total = papers_total | plus: 1 -%}{%- endfor -%}
{%- assign mdi_total = 0 -%}{%- assign mdi_counted = 0 -%}
{%- for m in site.data.mdi_articles -%}
  {%- assign mdi_total = mdi_total | plus: 1 -%}
  {%- if m.counted -%}{%- assign mdi_counted = mdi_counted | plus: 1 -%}{%- endif -%}
{%- endfor -%}

<div class="hero">
  <h1>What happened to the Andalusian Project&rsquo;s website</h1>
  <p class="hero-subtitle">The short answer, in one paragraph, because this is the page people
  land on after searching a name and finding something they did not expect.</p>
</div>

<div class="info-block">
  <h3>The one-paragraph answer</h3>
  <p><code>asadullahali.com</code> was Asadullah Ali Al-Andalusi&rsquo;s own website, the
  original home of The Andalusian Project&rsquo;s writing, and <strong>it is defunct: the
  domain no longer belongs to him and now serves an unrelated, commercially operated
  gambling site. Do not visit it and do not follow a link to it</strong> &mdash; the archive
  prints the domain as plain text for exactly that reason. His WordPress mirror at
  <code>asadullahali.wordpress.com</code> is still up but its post bodies have been removed,
  so it is navigable and empty. His YouTube channel is no longer available; the videos are
  gone and the channel reads &ldquo;not available&rdquo;, though {{ videos_total }} of his
  recordings are catalogued here, most preserved as files in the Internet Archive, and
  {{ ix.documents }} of them have machine transcripts published on this site &mdash;
  {{ ix.words }} words of text that exists nowhere else. The written work was not lost so
  much as scattered, and it is gathered here with per-item provenance:
  {{ works_total }} works ({{ found }} full-text in this repository, {{ wayback_only }}
  Wayback-only, {{ lost }} unrecoverable), {{ papers_total }} academic papers,
  {{ mdi_counted }} further distinct items among {{ mdi_total }} Muslim Debate Initiative
  pages. Where the work was republished by an institution that is still live, that
  institution remains the canonical place to read it, and this archive says which one rather
  than competing with it. To cite anything recovered here, cite the work, the original URL
  and the Wayback capture timestamp, exactly as in
  <a href="{{ '/NOTICE.md' | relative_url }}#3-provenance-and-how-to-check-it">NOTICE.md
  section 3</a>. This archive is a third party&rsquo;s documented recovery; it is not
  affiliated with, endorsed by, or a successor to anything that is still running.</p>
</div>

<div class="info-block">
  <h3>Safety warning, stated plainly</h3>
  <p><strong>The domain <code>asadullahali.com</code> now serves an unrelated gambling
  operation and should not be visited.</strong> It is not a parked page and it is not an
  archive of anything: it is a commercially operated site running under the founder&rsquo;s
  byline. Nothing served there is his work, his statement, or his archive. This matters
  because third-party pages still send readers there &mdash; institutional profiles, course
  listings and faculty pages, including pages this archive itself catalogues, still present
  that domain as his official site because they were written before the takeover and nobody
  updated them. <strong>If you arrived here from one of those links, you arrived from an
  outdated reference, not from him.</strong> The archive deliberately prints the domain as
  text rather than as a link, and asks that you do the same.</p>
</div>

<h2 id="site">What each of the three properties was, and what happened to it</h2>

<h3>The main site</h3>
<p>The Andalusian Project published on <code>asadullahali.com</code>. This archive holds
{{ works_total }} catalogued works from it, of which {{ found }} were recovered in full text
&mdash; verbatim, never summarised or reworded &mdash; and {{ wayback_only }} are catalogued
from Wayback Machine captures that were never fetched again, so only their titles and dates
are held. {{ lost }} work could not be recovered from any capture at all and is recorded as
missing rather than quietly dropped. Every recovered item carries the capture timestamp it
came from, which is what makes a citation resolve to what he actually wrote rather than to
whatever a host serves today.</p>

<h3>The WordPress mirror</h3>
<p><code>asadullahali.wordpress.com</code> is a mirror of the same site on WordPress.com
hosting. It is <strong>partly removed, and partly the reason the recovery worked</strong>. The
site chrome and his bio paragraph are still served and the post list is still navigable, but
the post bodies are gone &mdash; an orphaned shell. That shell turned out to be the single
most useful recovery source in the project: its own API still returned the post list, which
is how a fresh Wayback enumeration found {{ works_total }} post permalinks, how
{{ lost }} unrecoverable work and 3 announcements were identified as missing, and how the
fullest text of the largest work in the archive was adopted. Where a body was gone from the
mirror it was recovered from a Wayback capture instead, and where two copies disagreed the
archive kept the longer one, kept the other as a recorded alternate, and never added them
together.</p>

<h3>The YouTube channel</h3>
<p>The channel existed continuously under a single id from at least June 2015 until its
videos were removed around October 2022. The channel id continued to exist and was captured
by the Wayback Machine repeatedly, so the archive holds a
<strong>dated record of what the channel actually showed at each capture</strong> &mdash;
subscriber counts, item counts and handles, each tied to its capture timestamp &mdash; on
<a href="{{ '/channel/' | relative_url }}">the channel record</a>. The videos themselves are
gone. What survives is catalogued rather than assumed:
{{ videos_total }} recordings with their ids, durations and current locations, most preserved
as files in the Internet Archive&rsquo;s <code>andalusian-project</code> collection, the rest
as re-uploads on other people&rsquo;s channels with the uploader named, plus a ledger of
removed duplicates preserved in full and counted nowhere. {{ ix.documents }} of the recordings
have machine transcripts published here.</p>
<p class="page-note">The channel record also lists the claims this archive
<strong>refuses</strong> to make &mdash; subscriber figures that belong to other channels,
and any statement about who was operating the account in a later re-upload period. A capture
records what a channel showed on a date; it does not record who was holding the account, and
the archive says so instead of guessing.</p>

<h3>One publisher that vanished too</h3>
<p>The journal that published <em>The Rise and Decline of Scientific Productivity in the
Muslim World</em> (2015) no longer resolves at all: <code>icrjournal.org</code> is NXDOMAIN
and the paper&rsquo;s DOI is dead. A web search still returns what looks like a live article
page for it; that is a stale index snippet, not a live page. The archive holds a copy of that
paper taken from the Internet Archive&rsquo;s capture of the publisher&rsquo;s own file and
sha256 byte-verified against it, which is the only reason that citation still resolves
anywhere. The access ledger on the <a href="{{ '/papers/' | relative_url }}">papers
page</a> records which of the {{ papers_total }} primary sources are open, restricted or
dead.</p>

<h2 id="where">Where the material lives now</h2>

<table>
  <thead>
    <tr>
      <th>What you are looking for</th>
      <th>Where it is</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>The full text of a recovered work</td>
      <td><a href="{{ '/articles/' | relative_url }}">The works index</a>, one page per work, each with its original URL, its Wayback capture and its recovery provenance. {{ found }} of {{ works_total }} are in full text here.</td>
    </tr>
    <tr>
      <td>An academic paper</td>
      <td><a href="{{ '/papers/' | relative_url }}">The papers index</a>, one page per paper, with a per-item access status. The archive holds the texts it could obtain openly and link-outs the rest; it does not mirror a paper it could not obtain openly.</td>
    </tr>
    <tr>
      <td>The text of a talk</td>
      <td><a href="{{ '/transcripts/' | relative_url }}">{{ ix.documents }} machine transcripts</a> ({{ ix.words }} words), and <a href="{{ '/transcripts/by-series/' | relative_url }}">the same transcripts grouped by series</a>. These exist nowhere else on the web.</td>
    </tr>
    <tr>
      <td>A recording</td>
      <td><a href="{{ '/videos/' | relative_url }}">The video catalogue</a>, and the <a href="https://archive.org/details/andalusian-project" target="_blank" rel="noopener noreferrer">Internet Archive&rsquo;s <code>andalusian-project</code> collection</a> for the files themselves.</td>
    </tr>
    <tr>
      <td>What the channel showed, and when</td>
      <td><a href="{{ '/channel/' | relative_url }}">The channel record</a> &mdash; capture by capture, with three claims this archive rejects and the evidence that rejects them.</td>
    </tr>
    <tr>
      <td>Who he is, and every form of his name</td>
      <td><a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}">The entity page</a>, including the distinction from the different man also called Abdullah al-Andalusi.</td>
    </tr>
  </tbody>
</table>

<h3>Still live at the original publishers</h3>
<p>Most of this corpus was republished by institutions that are still running, and for those
the original publisher remains the right place to read it. This archive points outward rather
than competing:</p>
<ul>
  <li><strong>Yaqeen Institute</strong> &mdash; the co-authored paper on Aisha&rsquo;s age
  with Dr Jonathan Brown, the <em>Orientalists&rsquo; Fables</em> paper, and the
  <em>Doubting Your Doubts</em> lecture page. This archive holds all three as link-outs and
  mirrors none of them. <a href="https://yaqeeninstitute.org/team/asadullah" target="_blank" rel="noopener noreferrer">Yaqeen&rsquo;s profile page</a>.</li>
  <li><strong>The Muslim Debate Initiative</strong> &mdash; the full text of the
  {{ mdi_total }} author-archive articles, at authoritative URLs, still live. Those are his
  canonical home and this archive says so on each of its own pages for them.
  <a href="https://muslimdebate.org/author/asadullahali/" target="_blank" rel="noopener noreferrer">MDI&rsquo;s author archive</a>.</li>
  <li><strong>Al Balagh Academy</strong> &mdash; the current home of his course teaching, and
  the body of the five-part <em>A Muslim&rsquo;s Guide to Science and Scientism</em> series
  that this archive holds as
  <a href="{{ '/transcripts/by-series/a-muslims-guide-to-science-and-scientism/' | relative_url }}">transcripts</a>.</li>
  <li><strong>Traversing Tradition</strong> &mdash; a dated nine-question Q&A on science,
  history and atheism, 19 November 2020, the most recent third-party item in this corpus.
  <a href="https://traversingtradition.com/2020/11/19/science-history-and-athiesm-qa-with-asadullah-ali/" target="_blank" rel="noopener noreferrer">The interview</a>.</li>
  <li><strong>The Internet Archive</strong> &mdash; the archived recordings, and the Wayback
  Machine for every capture the archive cites.</li>
</ul>

<h2 id="cite">How to cite what you found here</h2>
<p>Cite the work, not this repository. Crediting &ldquo;The Andalusian Project
Archive&rdquo; on its own does not satisfy attribution: the archive is the record, not the
author. The capture timestamp is what makes the citation resolve to what he actually wrote.</p>

<div class="info-block">
  <h3>A recovered work</h3>
  <p><code>Asadullah Ali Al-Andalusi, &ldquo;&lt;title&gt;&rdquo;, &lt;date&gt;. The
  Andalusian Project. Preserved in The Andalusian Project Archive,
  https://the-andalusian-project-archive.github.io/andalusian-archive/articles/&lt;slug&gt;/;
  original capture: &lt;wayback_url&gt;.</code></p>
</div>

<div class="info-block">
  <h3>An academic paper</h3>
  <p>Cite the publication first and treat the archive as the surviving copy, which is what
  makes it useful when a publisher has gone:
  <code>Asadullah Ali Al-Andalusi. &ldquo;&lt;title&gt;.&rdquo; &lt;journal&gt;
  &lt;volume/issue&gt; (&lt;year&gt;). DOI &lt;doi&gt;. Preserved copy:
  &lt;archive url&gt;.</code> The papers page prints the corrected citation for every paper,
  including the one whose DOI is dead.</p>
</div>

<div class="info-block">
  <h3>A transcript &mdash; always with the disclaimer</h3>
  <p>Every transcript in this archive is machine-made, and the same sentence is printed on
  every one of them and reproduced in
  <a href="{{ '/NOTICE.md' | relative_url }}#5-the-machine-transcripts-carry-this-disclaimer">NOTICE.md
  section 5</a>:</p>
  <p class="transcript-disclaimer"><em>{{ ix.disclaimer }}</em></p>
  <p>They are a finding aid &mdash; a way to search {{ ix.words }} words of recovered speech
  and find the moment worth going back to the recording for. They are not an authorised
  edition of what was said, and quoting one as though it were settles nothing.</p>
</div>

<h2 id="questions">The questions people actually search for</h2>
<p>These are the searches this page exists to answer. Each answer below is the whole answer,
and each is repeated in the page&rsquo;s structured data word for word, so nothing is
marked-up that a reader cannot read here.</p>

{%- for qa in ep.queries %}
<div class="info-block">
  <h3>{{ qa.q | escape }}</h3>
  <p><strong>{{ qa.short | escape }}</strong></p>
  <p>{{ qa.a | escape }}</p>
</div>
{%- endfor %}

<h2 id="not">What this archive is not</h2>
<ul>
  <li><strong>Not affiliated with, endorsed by, or a successor to anything that is still
  running.</strong> The Andalusian Project&rsquo;s site, mirror and channel are gone. This is
  a third party&rsquo;s documented recovery, and nobody asked to approve it and nobody has
  approved it on anyone&rsquo;s behalf.</li>
  <li><strong>Not a claim over the domain.</strong> The archive does not control
  <code>asadullahali.com</code>, does not represent it, and does not assert any right over it.
  It records the state of the site, dated.</li>
  <li><strong>Not a re-licensing of his work.</strong> His prose is reproduced verbatim with
  attribution. It was openly readable when published, which is availability and not
  permission, and no open licence was ever applied to it. Reuse is governed by the rights
  holder&rsquo;s terms. <a href="{{ '/NOTICE.md' | relative_url }}#2-openly-available-is-not-open-source">NOTICE.md
  section 2</a>.</li>
  <li><strong>Not an endorsement of the arguments it preserves.</strong> This is a dated
  polemical archive. The claims are the author&rsquo;s, on the dates shown, and the archive
  adopts none of them. <a href="{{ '/NOTICE.md' | relative_url }}#8-what-this-corpus-is-and-what-it-is-not">NOTICE.md
  section 8</a>.</li>
  <li><strong>Not a route to the author.</strong> He has asked not to be contacted, and the
  maintainers cannot forward requests and cannot put them through.
  <a href="{{ '/NOTICE.md' | relative_url }}#do-not-contact-the-author">NOTICE.md section
  10</a>.</li>
</ul>
