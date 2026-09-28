#!/usr/bin/env python3
"""Ping IndexNow with this site's URLs. No account, no API key registration.

IndexNow (https://www.indexnow.org) is a push protocol: a site owner POSTs the
URLs that changed to participating engines (Bing, Yandex and others), and they
re-crawl those URLs instead of waiting for their next scheduled visit. It is the
only submission route available on a `github.io` subpath that requires no account
of any kind - Google Search Console and Bing Webmaster Tools both require one.

OWNERSHIP IS PROVED BY A KEY FILE, NOT AN ACCOUNT. The key must be served from the
site root; this repository commits it as `indexnow-<key>.txt`, which Jekyll copies
to the output root, and that URL is what the POST advertises as `keyLocation`.

WHAT THIS DOES AND DOES NOT DO. It tells participating engines that URLs changed.
It does not create an index entry, it does not verify anything with Google, and it
works only for engines that participate. Google does not accept IndexNow.

Usage
    python scripts/ping_indexnow.py                     # ping the sitemap
    python scripts/ping_indexnow.py --sitemap <path>    # ping a given sitemap
    python scripts/ping_indexnow.py --url <url> [...]    # ping specific URLs
    python scripts/ping_indexnow.py --dry-run           # print, do not send

Exit codes: 0 sent or nothing to do, 1 the POST failed or a named sitemap is
unreadable, 2 no key file.
"""

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY_GLOB = "indexnow-*.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
# The protocol allows up to 10,000 URLs per request. One site this size fits in a
# single call; the batching below exists so a much larger sitemap still works.
BATCH = 10000


def find_key() -> tuple[str, str] | tuple[None, str | None]:
    """Return (key, absolute key URL) from the committed key file, or (None, why)."""
    matches = sorted(ROOT.glob(KEY_GLOB))
    if not matches:
        return None, f"no {KEY_GLOB} at the repository root"
    key = matches[0].read_text(encoding="utf-8").strip()
    if not key:
        return None, f"{matches[0].name} is empty"
    site = ""
    for line in (ROOT / "_config.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r'^\s*url:\s*"?([^"\s]+)"?\s*$', line)
        if m:
            site = m.group(1)
            break
    if not site:
        return None, "could not read `url:` from _config.yml"
    baseurl = ""
    for line in (ROOT / "_config.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r'^\s*baseurl:\s*"?([^"\s]*)"?\s*$', line)
        if m:
            baseurl = m.group(1)
            break
    return key, f"{site.rstrip('/')}{baseurl.rstrip('/')}/{matches[0].name}"


def sitemap_urls(path: "pathlib.Path | None" = None) -> list[str]:
    """Read <loc> entries from a sitemap.

    Defaults to the local build's `_site/sitemap.xml`. CI passes the DEPLOYED
    sitemap instead, because that is the list of URLs that are actually live -
    the local `_site/` belongs to a build job whose output the deploy job cannot
    see, and could in principle be a build that never shipped.
    """
    sm = path or (ROOT / "_site" / "sitemap.xml")
    if not sm.exists():
        return []
    return re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))


def send(key: str, key_url: str, urls: list[str], dry_run: bool) -> int:
    host = re.match(r"https?://([^/]+)", key_url).group(1)
    for i in range(0, len(urls), BATCH):
        chunk = urls[i : i + BATCH]
        payload = {
            "host": host,
            "key": key,
            "keyLocation": key_url,
            "urlList": chunk,
        }
        body = json.dumps(payload).encode("utf-8")
        if dry_run:
            print(f"[dry-run] would POST {len(chunk)} URL(s) to {ENDPOINT}")
            print(json.dumps({**payload, "urlList": chunk[:2] + (["..."] if len(chunk) > 2 else [])}, indent=2))
            continue
        req = urllib.request.Request(
            ENDPOINT,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "andalusian-archive/1.0 (IndexNow protocol)",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                print(f"sent {len(chunk)} URL(s): HTTP {resp.status}")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            print(f"IndexNow returned HTTP {exc.code}: {detail}", file=sys.stderr)
            return 1
        except urllib.error.URLError as exc:
            print(f"IndexNow unreachable: {exc.reason}", file=sys.stderr)
            return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", action="append", default=[], help="a specific URL to ping (repeatable)")
    ap.add_argument("--sitemap", help="read URLs from this sitemap instead of _site/sitemap.xml")
    ap.add_argument("--dry-run", action="store_true", help="print the payload, do not send")
    args = ap.parse_args()

    key, key_url = find_key()
    if key is None:
        print(f"cannot ping: {key_url}", file=sys.stderr)
        return 2
    print(f"key     : {key[:8]}... (redacted)")
    print(f"keyUrl  : {key_url}")

    sitemap = pathlib.Path(args.sitemap) if args.sitemap else None
    if args.sitemap and not sitemap.exists():
        print(f"cannot ping: {args.sitemap} does not exist", file=sys.stderr)
        return 1
    urls = args.url or sitemap_urls(sitemap)
    if not urls:
        print("nothing to ping: no URLs given and no readable sitemap. Build the site first.")
        return 0
    print(f"urls    : {len(urls)}")
    return send(key, key_url, urls, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
