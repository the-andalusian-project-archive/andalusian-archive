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
