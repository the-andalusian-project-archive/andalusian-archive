# Indexing log

Dated measurements from `scripts/measure_indexing.py`. One row per
run. The baseline is the 2026-09-29 audit, which found no crawler
footprint of any kind. Read `UNREACHABLE` as *not measured*, never
as *absent* - a timeout and an absence of indexing are different
findings and this log refuses to merge them.

Common Crawl is the weakest of the four: its API answers an empty
body for a malformed query exactly as it does for an uncrawled
domain, so a 0 from it cannot self-verify. The other three can.

| Date | Wayback | Common Crawl | urlscan | sitemap live |
|---|---|---|---|---|
| 2026-09-30 | 0 | 0 | 0 | 12/12 |

## Search Console coverage snapshots

`measure_indexing.py` asks third-party crawlers; it cannot see Google's
index. These readings come from the Search Console URL Inspection API and
are recorded here because they answer the same question from the crawler
that matters most. A URL counts as indexed only when the verdict is `PASS`
and the coverage state is `Submitted and indexed`.

The 2026-10-29 sample is the ten URLs inspected by hand: `/`, `/papers/`,
`/transcripts/`, `/channel/`, `/asadullah-ali-al-andalusi/`, `/videos/`,
`/articles/`, the Backbone paper, `/notice/` and `/contributing/`.

| Date | Indexed | Unknown to Google | Crawled, not indexed | Note |
|---|---:|---:|---:|---|
| 2026-10-29 | 5 | 4 | 1 | Sitemap resubmitted 15:08. `/articles/` had been crawled but not indexed. |
| 2026-10-31 | 9 | 1 | 0 | The 3f7ba25 deploy moved `/articles/`, the Backbone paper, `/notice/` and `/contributing/` into the index. Only `/videos/` is still unknown. |

The sitemap itself remained `pending` with `last_downloaded: null` on
2026-10-31, despite 0 errors and 0 warnings. The four new entries above
are therefore crawl-by-link or manual-request results, not a sitemap
download; the file has not been fetched yet.

The 2026-10-31 inspection also covered `/scholarly-records/`: indexed,
crawled 2026-10-30, but its rich result failed. Six `isBasedOn` entries
were typed `Dataset` with only `name` and `url`, so Google reported all
six missing `description` (error), `creator` and `license` (warnings).
`e8afccd` cuts that duplicate list; the six registries remain once in the
`CollectionPage` ItemList. `check_rendered_seo.py` now rejects any
`Dataset` node missing one of those four fields, so the same defect fails
the build rather than waiting for an email.
