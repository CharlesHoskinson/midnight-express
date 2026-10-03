#!/usr/bin/env python3
"""Shared fetch helper for the privateEvents corpus.

Run with scrapling's own interpreter:
    ~/.local/share/uv/tools/scrapling/bin/python scripts/pe_fetch.py <command> ...

Commands:
    json  URL                 print the JSON body of an API endpoint
    text  URL                 print the visible text of an HTML page (first 20000 chars)
    pdf   URL SLUG [--src S]  download a PDF to pdfs/SLUG.pdf, verify %PDF-, print sha256

The helper sends a generic User-Agent and never any email address. It sleeps
between calls so that callers can loop without hammering a host.
"""
import argparse
import fcntl
import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from scrapling.fetchers import Fetcher

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pdfs"
UA = "privateEventsResearch/1.0"
DELAY = 1.5


HOST_GAP = {  # minimum seconds between requests to one host, shared by all processes
    "export.arxiv.org": 3.5,
    "arxiv.org": 3.5,
    "api.openalex.org": 0.3,
    "api.crossref.org": 0.3,
    "eprint.iacr.org": 8.0,
    "dl.acm.org": 8.0,
}
STATE_DIR = Path.home() / ".cache" / "pe_fetch"


def wait_for_host(url):
    """Block until this process may call the host, using a lock and timestamp file
    shared across all pe_fetch processes on the machine."""
    host = urlparse(url).hostname or "unknown"
    gap = HOST_GAP.get(host, DELAY)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_DIR / f"{host}.ts", "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        try:
            last = float(fh.read().strip() or 0)
        except ValueError:
            last = 0.0
        pause = last + gap - time.time()
        if pause > 0:
            time.sleep(pause)
        fh.seek(0)
        fh.truncate()
        fh.write(str(time.time()))
        fh.flush()
        fcntl.flock(fh, fcntl.LOCK_UN)


def get(url, timeout=60):
    wait_for_host(url)
    return Fetcher.get(
        url,
        timeout=timeout,
        impersonate="chrome",
        headers={"User-Agent": UA},
        follow_redirects=True,
    )


def cmd_json(url):
    page = get(url)
    if page.status != 200:
        print(json.dumps({"error": page.status, "url": url}))
        return 1
    try:
        print(json.dumps(page.json()))
    except Exception:
        print(page.body.decode("utf-8", "replace"))
    return 0


def cmd_text(url):
    page = get(url)
    if page.status != 200:
        print(json.dumps({"error": page.status, "url": url}))
        return 1
    print(page.get_all_text(separator="\n", strip=True)[:20000])
    return 0


def cmd_pdf(url, slug):
    page = get(url, timeout=120)
    for pause in (30, 60, 120):  # back off on rate limiting, then give up
        if page.status != 429:
            break
        time.sleep(pause)
        page = get(url, timeout=120)
    body = bytes(page.body)
    if page.status != 200 or not body.startswith(b"%PDF-"):
        print(json.dumps({"ok": False, "status": page.status, "url": url,
                          "reason": "not a PDF (paywall, landing page or error)"}))
        return 1
    PDF_DIR.mkdir(exist_ok=True)
    path = PDF_DIR / f"{slug}.pdf"
    path.write_bytes(body)
    print(json.dumps({"ok": True, "path": str(path.relative_to(ROOT)),
                      "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                      "url": url}))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("json").add_argument("url")
    sub.add_parser("text").add_argument("url")
    p = sub.add_parser("pdf")
    p.add_argument("url")
    p.add_argument("slug")
    a = ap.parse_args()
    if a.cmd == "json":
        return cmd_json(a.url)
    if a.cmd == "text":
        return cmd_text(a.url)
    return cmd_pdf(a.url, a.slug)


if __name__ == "__main__":
    sys.exit(main())
