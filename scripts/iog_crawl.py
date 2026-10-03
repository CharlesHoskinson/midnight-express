#!/usr/bin/env python3
"""Crawl the IOG research library (https://www.iog.io/papers) into catalog/iog-library.jsonl.

Step 1 walks /papers?type=research-paper&page=N until a page adds no new slugs.
Step 2 fetches each /papers/<slug> page and keeps title, tags, page text and outbound links.
The library's robots.txt allows /papers. Requests go through pe_fetch.get (shared rate limit).

    ~/.local/share/uv/tools/scrapling/bin/python scripts/iog_crawl.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pe_fetch import ROOT, get  # noqa: E402

BASE = "https://www.iog.io"
OUT = ROOT / "catalog" / "iog-library.jsonl"
SLUGS = ROOT / "catalog" / "iog-library-slugs.txt"


def list_slugs():
    slugs, page = [], 1
    while True:
        p = get(f"{BASE}/papers?type=research-paper&page={page}")
        if p.status != 200:
            print(f"page {page}: status {p.status}", file=sys.stderr)
            break
        found = []
        for a in p.css("a"):
            h = a.attrib.get("href", "")
            m = re.fullmatch(r"/papers/([a-z0-9][a-z0-9-]+)", h)
            if m and m.group(1) not in slugs and m.group(1) not in found:
                found.append(m.group(1))
        print(f"page {page}: {len(found)} new", file=sys.stderr)
        if not found:
            break
        slugs += found
        page += 1
    return slugs


def read_paper(slug):
    try:
        p = get(f"{BASE}/papers/{slug}")
    except Exception as exc:  # redirect loops and transient network errors
        return {"slug": slug, "status": "error", "error": str(exc)[:200]}
    if p.status != 200:
        return {"slug": slug, "status": p.status}
    title = ""
    h1 = p.css("h1")
    if h1:
        title = h1[0].get_all_text(strip=True)
    tags = sorted({
        a.attrib["href"].split("tags=")[-1]
        for a in p.css("a")
        if "tags=" in a.attrib.get("href", "")
    })
    out = [
        {"href": a.attrib["href"], "text": a.get_all_text(strip=True)[:80]}
        for a in p.css("a")
        if a.attrib.get("href", "").startswith("http")
        and "iog.io" not in a.attrib["href"]
        and not re.search(r"x\.com|linkedin|youtube|lace\.io|pogun|realfi|projectcatalyst|identus|blockfrost|docs\.cardano", a.attrib["href"])
    ]
    main = p.css("main")
    text = (main[0] if main else p).get_all_text(separator="\n", strip=True)
    return {"slug": slug, "url": f"{BASE}/papers/{slug}", "status": 200,
            "title": title, "tags": tags, "links": out, "text": text[:6000]}


def main():
    OUT.parent.mkdir(exist_ok=True)
    slugs = list_slugs()
    SLUGS.write_text("\n".join(slugs) + "\n")
    print(f"{len(slugs)} papers listed", file=sys.stderr)
    done = set()
    if OUT.exists():
        done = {json.loads(l)["slug"] for l in OUT.read_text().splitlines() if l.strip()}
    with OUT.open("a") as fh:
        for i, s in enumerate(slugs, 1):
            if s in done:
                continue
            fh.write(json.dumps(read_paper(s), ensure_ascii=False) + "\n")
            fh.flush()
            if i % 25 == 0:
                print(f"  {i}/{len(slugs)}", file=sys.stderr)


if __name__ == "__main__":
    main()
