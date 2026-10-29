#!/usr/bin/env python3
"""Validate the generated `llms-full.txt` against the built site.

`build_llms_full.py` writes one `- in this archive:` URL per document. Nothing
used to check those URLs, and 63 of them pointed at `/posts/...` - a path
Jekyll never emits for this site. This gate maps every emitted URL back to the
build and fails when a document links to a page that does not exist. It also
refuses the contact claim the policy gate explicitly says is false.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
DOC = ROOT / "llms-full.txt"
ORIGIN = "https://the-andalusian-project-archive.github.io"
BASE = "/andalusian-archive"


def local_path(url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "the-andalusian-project-archive.github.io":
        return None
    path = unquote(parsed.path)
    if not path.startswith(BASE + "/"):
        return None
    rel = path[len(BASE):].strip("/")
    target = SITE / rel
    if target.is_dir() or path.endswith("/") or not target.suffix:
        target = target / "index.html"
    return target


def main() -> int:
    if not DOC.exists():
        print(f"FAIL: {DOC.relative_to(ROOT)} is missing; run build_llms_full.py")
        return 1
    text = DOC.read_text(encoding="utf-8", errors="replace")
    problems = []

    if "has asked not to be contacted" in text:
        problems.append("contains the false 'has asked not to be contacted' claim")

    urls: list[str] = []
    for value in re.findall(r"^- in this archive: (.*)$", text, re.M):
        value = value.strip()
        if not re.match(r"^https?://\S+$", value):
            problems.append(f"malformed '- in this archive:' URL: {value!r}")
            continue
        urls.append(value)
    if not urls:
        problems.append("no '- in this archive:' URLs found")
    missing = []
    for url in urls:
        target = local_path(url)
        if target is None:
            missing.append((url, "outside the configured origin/baseurl"))
        elif not target.exists():
            missing.append((url, str(target.relative_to(ROOT))))
    for url, why in missing[:20]:
        problems.append(f"dead URL: {url} ({why})")
    if len(missing) > 20:
        problems.append(f"... and {len(missing) - 20} more dead URLs")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        print(f"check_llms_full: {len(problems)} problem(s)")
        return 1

    docs = len(re.findall(r"^## ", text, re.M))
    print(f"check_llms_full: {len(urls)} internal URLs checked, "
          f"{docs} document headings, all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
