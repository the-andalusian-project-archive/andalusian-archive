# Contributing

This is a preservation archive, not a writing project. The useful contributions
are corrections to the record, not changes to the recovered material.

## Do not contact the author

The author has asked not to be contacted, and he keeps a private life. This is
stated here so that nobody has to guess.

Requests to contact him, requests for his personal details, and invitations to
events will not be answered and should not be sent. The maintainers cannot
forward them and cannot put them through.

This section exists because the request most often arrives as an issue that
asks how to reach him. It cannot be fulfilled, and filing it does not create a
channel. Everything this archive can act on has a template, and all of them are
about the record rather than the person:

* a **provenance error** — a work attributed to the wrong person, a stated
  source that is not where the text came from, a wrong date or capture
  timestamp, a self-contradictory field, or a withheld item that is not
  disclosed — goes on the **Provenance correction or dead capture** template;
* a **dead capture** — a Wayback or Internet Archive link in a provenance block
  that no longer resolves, a page that 404s, a PDF that will not open — goes on
  the same template;
* a **rights, licensing or takedown request** goes on the **Rights, licensing
  or takedown request** template. If you want something removed rather than
  clarified, say so there and give the reason.

Do not include his legal or birth name, or any contact detail you have found
for him, in an issue or a pull request. See `NOTICE.md` section 6.1.

## What is worth reporting

Almost all of it, and none of it needs code.

**A broken capture.** A Wayback or Internet Archive link in a provenance block
that no longer resolves, a page 404, a PDF that will not open, a sitemap entry
pointing at a file that is not published. This is the common case and the easiest
to fix.

**A provenance error.** A work attributed to the wrong person, a stated source
that is not where the text actually came from, a wrong date or capture
timestamp, a field that contradicts itself, or a withheld item that is not
disclosed. The archive's whole value is that a reader can check where each item
came from, so a wrong provenance field is a real defect.

**A figure that disagrees with the data.** If a number on a page does not match
the file it is counted from, say which page and which value. Check
`docs/recovery-log/` first - the counts there are the evidence for the counts on
the site, and there are known figures that are deliberately frozen pending the
owner's approval, which are recorded rather than wrong.

File these on the **Provenance correction or dead capture** template. One item per
report, so each can be verified independently.

## What is not accepted

**Edits to recovered prose.** The texts are reproduced verbatim. Wording changes
to his essays, papers or talks are not a contribution, however well argued -
including corrections of spelling, tone or factual error. If a work is
mislabelled or a paragraph is out of order, that is a provenance problem and
should be reported as one.

**Reuploads or mirrors of the recovered text elsewhere.** This repository and
the site it builds are the canonical location. A copy somewhere else adds a
second thing to keep in sync, not a second citation.

**Bulk or generated data.** Do not submit a scrape, a dump, or a machine-written
catalogue. Every row here has a retrieval method and a capture behind it, and a
generated row is precisely the thing that cannot be checked.

**The author's withheld names.** Two personal names of his are withheld at the
site owner's decision, and both are disclosed in `NOTICE.md` section 6.1
rather than left as a silent gap. Do not include either in an issue, a pull
request or a commit. Section 6.1 also records the one place a withheld name
survives inside a held file, and section 6.4 the personal identifier that was
cleared from a PDF's embedded metadata.

**Long pasted passages.** Link the page. Recovered text stays in its page, where
it has provenance attached to it.

## Rights and takedown requests

Use the **Rights, licensing or takedown request** template. A person reads those.
Include a working email address and state your relationship to the material -
author, co-author, publisher, representative, or reader with a concern.

The licence position is settled and recorded in `NOTICE.md` and `LICENSE`, and it
is worth reading before writing: the author's prose is reproduced with
attribution and is **not** relicensed, because it was openly readable but never
openly licensed; the archive's own data, scripts and documentation are
CC BY-NC 4.0. If you want something removed rather than clarified, say so
directly in the issue and give the reason.

## Working on the repository

Requires Ruby with Bundler (Jekyll 4.3+), Python 3, and Node.

```
npm install
npm run test:search-sync     # asserts _data/ and data/ are in sync
npm run build                # syncs search data, then runs jekyll build
```

Four Python test suites gate the build and are worth running after any change:
`scripts/test_search_sync.py`, `scripts/test_transcripts.py`,
`scripts/test_canonical_57.py` and `scripts/test_no_junk.py`. They enforce the
prose-fidelity rule, the redaction rules, and the collections' shape; a change
that breaks one of them is almost always a change that should not be made.

**Never hand-edit** anything in `data/` - it is generated from `_data/` on every
build. The catalogue lives in `_data/`, and a number on a page is counted from
there rather than typed.

`_staging/` holds raw captures and binaries. It is gitignored and is not
published. Raw captures are evidence: they are withheld, never edited, so a
capture file that contains something withheld stays intact and stays untracked
rather than being cleaned up.

## Verifying a claim about the archive

Every count on the site and in the README is counted from `_data/` at build time,
and the derivation of each is in `docs/recovery-log/` - per-lane manifests, the
append-only integration log, and two independent review rounds. If a figure
looks wrong, the fastest check is to count the corresponding collection file
yourself before opening an issue.

## Security

There is no `SECURITY.md`, deliberately. The site is static, the build has no
runtime, no database and no user input, `.env` is gitignored and `.env.example`
carries placeholders only, and the three Actions permissions are already scoped
to `contents: read`, `pages: write`, `id-token: write`. There is no vulnerability
surface to document. If you find something that looks like one, open a blank
issue and say so - do not assume it is out of scope.
