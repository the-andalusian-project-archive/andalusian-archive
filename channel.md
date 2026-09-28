---
layout: default
title: The YouTube Channel Record
description: What the captures of The Andalusian Project's YouTube channel show, what they cannot show, and what this archive preserves instead.
---

{% assign f = site.data.channel_facts %}

<h1 class="page-title">The YouTube Channel Record</h1>
<p class="page-subtitle">What the captures of The Andalusian Project&rsquo;s YouTube channel show, what they cannot show, and what this archive preserves instead.</p>

<p class="page-note">This page is a preservation record, not a fan page. Every claim below is dated to a specific Wayback capture of the channel, and the capture timestamps are given so each one can be re-checked. Nothing here is a statement about a person&rsquo;s conduct; where a capture cannot settle a question, this page says so rather than guessing.</p>

<div class="info-block">
  <h3>The channel in one paragraph</h3>
  <p>The channel existed continuously under the id <code>{{ f.channel.uc_id }}</code> from at least June 2015 until it was reported unavailable. Its subscriber count ran 190 &rarr; 2,526 &rarr; 3,130 &rarr; 5,559 &rarr; 6.97K &rarr; 11.2K &rarr; 11.3K &rarr; 11.5K &rarr; 14.4K &rarr; 15.7K, read from the channel&rsquo;s own header in each capture. The videos were gone by October 2022. The same channel id was re-populated in 2023 with 81 &rarr; 84 &rarr; 85 items under a new handle, then emptied again; by August 2025 it showed 0 videos, and a live check on {{ f.live_check.date }} returned &ldquo;{{ f.live_check.result }}&rdquo; Today it is terminal: <strong>{{ f.channel.current_state }}</strong>.</p>
</div>

<h2>1. The verified timeline</h2>
<p>Every row is one Wayback capture, dated by its capture timestamp. Subscriber counts are the channel&rsquo;s own, never a neighbouring channel&rsquo;s &mdash; that distinction is the subject of section 2. Capture timestamps are the citation: each can be pasted into the Wayback Machine to re-read the header. Where the archived URL is a dead channel path, the capture is cited by timestamp and archived path rather than by link, so that no link on this page leads a reader to an unavailable channel.</p>

<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>Capture</th>
      <th>Subscribers</th>
      <th>Videos</th>
      <th>What the capture shows</th>
    </tr>
  </thead>
  <tbody>
    {% for row in f.timeline %}
    <tr>
      <td>{{ row.date }}</td>
      <td>
        {% if row.wayback_url %}
        <a href="{{ row.wayback_url }}" target="_blank" rel="noopener noreferrer"><code>{{ row.capture }}</code></a>
        {% else %}
        <code>{{ row.capture }}</code>
        {% endif %}
        <br><span class="meta">{{ row.page | escape }}</span>
      </td>
      <td>{% if row.subscribers %}{{ row.subscribers }}{% else %}&mdash;{% endif %}</td>
      <td>{% if row.videos %}{{ row.videos }}{% elsif row.videos_on_page %}{{ row.videos_on_page }} on page{% else %}&mdash;{% endif %}</td>
      <td>
        {{ row.evidence | escape }}
        {% if row.note %}<br><em>{{ row.note | escape }}</em>{% endif %}
        {%- comment -%}
          I4 (Phase-3 review, 2026-09-27): this cell used to print
          `row.source_file`, which is a path under the gitignored staging tree
          that is deleted after the final phase - so the published channel page
          pointed a reader at a file that will not exist. The capture timestamp
          in the row above is the citation and is durable; the local payload
          filename stays in _data/channel_facts.json, and the payload SIZE is
          kept here because it is what distinguishes a head-only capture, an
          empty capture and a full one.
        {%- endcomment -%}
        {% if row.source_bytes %}<br><span class="meta">archived payload: {{ row.source_bytes }} bytes</span>{% endif %}
      </td>
    </tr>
    {% endfor %}
    <tr>
      <td>{{ f.live_check.date }}</td>
      <td><em>live check, not a capture</em></td>
      <td>&mdash;</td>
      <td>0</td>
      <td>{{ f.live_check.result }} <span class="meta">({{ f.live_check.how | escape }})</span></td>
    </tr>
  </tbody>
</table>

<p><strong>Continuity of the id.</strong> {{ f.identity_continuity.statement | escape }}</p>
<ul>
  {% for item in f.identity_continuity.how_the_continuity_is_evidenced %}
  <li>{{ item | escape }}</li>
  {% endfor %}
</ul>

<p><strong>Reading the counts.</strong> {{ f.subscriber_series_note | escape }}</p>

<p class="page-note">The captures live in a temporary staging area during the recovery work and are deleted when it finishes. This page therefore carries the capture timestamps and, where the archived URL is not a dead channel path, a Wayback link &mdash; it does not depend on any local file continuing to exist. The archived path and payload filename for each row are recorded in the site&rsquo;s channel-facts data file so any claim can be re-verified against the Wayback Machine by timestamp.</p>

<h2>2. Claims this archive rejects</h2>
<p>{{ f.page_section_order[1].lead | escape }}</p>

{% for c in f.rejected_claims %}
<div class="info-block">
  <h3>{{ c.claim | escape }}</h3>
  <p><strong>{{ c.verdict | escape }}</strong></p>
  <p>{{ c.evidence | escape }}</p>
  {% if c.recorded_from %}<p class="meta">recorded from: {{ c.recorded_from | escape }}</p>{% endif %}
</div>
{% endfor %}

<p><strong>The archive does not publish 585K, 329K, or 1.01 million subscribers for this channel.</strong> The channel&rsquo;s own series is the one in the table above, and it tops out at 15.7K. The three large numbers are real numbers from real captures &mdash; they simply belong to other channels that YouTube rendered on the same page.</p>

<h2>3. The 2023 uploads: what is known, and what cannot be</h2>
<p>{{ f.account_control.statement | escape }}</p>

<p>That is the limit of what the captures support, and it is worth being precise about why. A Wayback capture records a channel&rsquo;s state on a date &mdash; how many videos, how many subscribers, what the handle is called. It does not record who was holding the account. So the captures establish that the 2023 material went through the original account, and they cannot establish whether the person himself or a third party with access to that account was operating it.</p>

<div class="info-block">
  <h3>What the captures can show</h3>
  <p>{{ f.account_control.what_the_2023_items_are_consistent_with | remove_first: "a re-upload or a return of material to the existing account. " | prepend: "The captures are consistent with a re-upload, or with a return of material to the existing account. " | escape }}</p>
  <h3>What the captures cannot show</h3>
  <p>{{ f.account_control.what_cannot_be_determined_from_captures | remove_first: "who operated that account in 2023. " | prepend: "What they cannot show is who operated that account in 2023. " | escape }}</p>
</div>

<p>On the byline question, the field is deliberately empty rather than filled in: <code>is_his: {% if f.do_not_link[0].is_his == nil %}null{% else %}{{ f.do_not_link[0].is_his }}{% endif %}</code> &mdash; {{ f.do_not_link[0].is_his_meaning | escape }}. The captures were asked a direct question and returned nothing either way, so this archive records a null.</p>
<p><em>{{ f.do_not_link[0].not_established | escape }}</em></p>

<h2>4. What this archive preserves instead</h2>
<p>{{ f.preservation_record.headline | escape }}</p>

<div class="info-block">
  <h3>{{ f.preservation_record.catalogued_videos }} catalogued videos</h3>
  <ul>
    <li><strong>{{ f.preservation_record.archive_org_files }} archive.org files</strong> &mdash; {{ f.preservation_record.how_split | escape }}</li>
    <li><strong>{{ f.preservation_record.catalogue_only_live_reuploads }} live re-upload entries</strong> &mdash; recordings whose only surviving copy sits on someone else&rsquo;s channel. They are catalogued once, in their own right, and labelled as appearances or clips rather than as his uploads.</li>
  </ul>
  <h3>Transcripts</h3>
  <p>{{ f.preservation_record.transcripts | escape }}</p>
  <p>{{ f.preservation_record.transcripts_reparented | escape }}</p>
  <h3>Live mirror URLs</h3>
  <p>{{ f.preservation_record.mirror_urls | escape }}</p>
  <h3>Superseded duplicates</h3>
  <p>{{ f.preservation_record.superseded_duplicates | escape }}</p>
  {%- comment -%}
    2026-09-28: a broken link, found while adding the Internet Archive link this
    section is supposed to carry - the link was already here and did not work.

    `preservation_record.archive_org_collection` is the PAGE-FACING statement
    of the collection and it reads

        andalusian-project (https://archive.org/details/andalusian-project)

    i.e. a sentence with the URL in it, not an identifier. Interpolating it into
    an href produced, in the built site:

        href="https://archive.org/details/andalusian-project (https://archive.org/details/andalusian-project)"

    which is a dead href with a space and a pair of parentheses in it. The
    sibling key `preservation.archive_org_collection` holds the bare identifier
    and is what belongs in a URL, so that is what is read here. No literal is
    typed and `_data/channel_facts.json` is not edited - the taxonomy records
    that file as owned by another agent and read-only here. The one link this
    section prints for the collection is now the one that resolves.
  {%- endcomment -%}
  <p><a href="https://archive.org/details/{{ f.preservation.archive_org_collection }}" target="_blank" rel="noopener noreferrer">The {{ f.preservation.archive_org_collection }} collection on the Internet Archive</a> is where the {{ f.preservation_record.archive_org_files }} files live. This collection is the live third-party preservation of the channel, and it is also the first entry on <a href="{{ '/scholarly-records/' | relative_url }}">the scholarly-records page</a>, which is this archive&rsquo;s account of where this work is registered in scholarly registries and what is wrong with those registrations.</p>
  <p class="meta">{{ f.preservation_record.caveat | escape }}</p>
</div>

<h2>5. Standing re-uploads on third-party channels</h2>
<p>{{ f.standing_reuploads.what_this_is | escape }}</p>

<table>
  <thead>
    <tr>
      <th>Channel</th>
      <th>What it is</th>
      <th>Attached as mirror URLs</th>
      <th>Superseded rows</th>
      <th>Counted entries</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    {% for c in f.standing_reuploads.channels %}
    <tr>
      <td><a href="{{ c.channel_url }}" target="_blank" rel="noopener noreferrer">{{ c.name | escape }}</a></td>
      <td>{{ c.what_it_is | escape }}<br><span class="meta">{{ c.status | escape }}</span></td>
      <td>{{ c.attached_as_mirror_urls }}</td>
      <td>{{ c.superseded_rows }}</td>
      <td>{{ c.counted_entries }}</td>
      <td>{{ c.total }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<p><strong>{{ f.standing_reuploads.counting_rule | escape }}</strong> Across the {{ f.standing_reuploads.totals.channels }} channels there are {{ f.standing_reuploads.totals.recorded_re_upload_placements }} recorded re-upload placements covering {{ f.standing_reuploads.totals.distinct_re_upload_recordings }} distinct recordings &mdash; {{ f.standing_reuploads.totals.breakdown | escape }}.</p>
<p>These channels are re-uploads of the archived recordings. None of them is the original channel, none is operated by this archive, and linking one is a statement about where a recording currently sits &mdash; not about who made it. The uploader names and channel handles were resolved from the oEmbed sweep recorded during the recovery work, and are held in the site&rsquo;s channel-facts data file so this list survives the deletion of the working files.</p>

<h2>6. The do-not-link rule</h2>
<p>{{ f.do_not_link_rule.statement | escape }}</p>

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Rule</th>
      <th>Why</th>
    </tr>
  </thead>
  <tbody>
    {% for r in f.do_not_link_rule.rules %}
    <tr>
      <td><code>{{ r.item | escape }}</code></td>
      <td><strong>{{ r.rule | escape }}</strong></td>
      <td>{{ r.why | escape }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<p>{{ f.do_not_link_rule.what_is_not_being_claimed | escape }}</p>

<h2>7. Where these claims come from</h2>
<p>{{ f.evidence_files.how_to_recheck_a_row | escape }}</p>
<p>{{ f.evidence_files.staging_is_temporary | escape }}</p>
<p>The channel id <code>{{ f.channel.uc_id }}</code> is recorded on this page as text, as provenance. It is not a link, and it is not a claim that the page behind it is his, alive, or available.</p>

{%- comment -%}
  2026-09-28: two cross-links, placed here because this page is where a reader
  arrives having just discovered the channel is gone. The first is the account of
  what happened to the channel's own properties, which is the question this page
  provokes; the second is the series index, because a good number of the
  recordings catalogued here are parts of a numbered series and their transcripts
  are now grouped by those series rather than only by recording.
{%- endcomment -%}
<p class="page-note">The recordings catalogued here are also grouped by series on
<a href="{{ '/transcripts/by-series/' | relative_url }}">the transcripts-by-series index</a>,
which links each part of <em>Understanding Atheism</em>, <em>iJihad</em>, <em>A Muslim&rsquo;s
Guide to Science and Scientism</em> and the other recorded series straight to its transcript.
For what became of the site this channel belonged to, see
<a href="{{ '/asadullahali-com-what-happened/' | relative_url }}">what happened to the
Andalusian Project&rsquo;s web presence</a>; for who the author is, see
<a href="{{ '/asadullah-ali-al-andalususi/' | relative_url }}">the entity page</a>.</p>
