---
layout: default
title: Timeline
---

<h1 class="page-title">Timeline</h1>
<p class="page-subtitle">Key milestones in the work of Asadullah Ali Al-Andalusi and The Andalusian Project.</p>
{%- comment -%}
  2026-09-27 (task 8f, Phase-3 review I6): this page used to say "Original
  YouTube channel deleted/privatized", which `rejected_claims[1]` in
  `_data/channel_facts.json` refines and the videos page and README already
  state: the videos were removed around October 2022; the channel id continued
  to exist, was captured through 2026-08-19, showed different items under a
  different handle in 2023, and reads "not available" at the 2026-09-27 check.
  The row now says that, and links the record that carries the captures. No
  figure on this page is typed, so no count changed.
{%- endcomment -%}

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
      <div class="timeline-title">Archive.org collection created (56+ videos)</div>
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