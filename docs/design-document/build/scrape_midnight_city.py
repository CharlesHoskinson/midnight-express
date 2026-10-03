#!/usr/bin/env python3
"""Scrape https://midnight.city with scrapling for brand reference.

    ~/.local/share/uv/tools/scrapling/bin/python scrape_midnight_city.py

Polite breadth-first crawl: same host only, robots.txt Disallow paths skipped, 2.5 s between pages, at most 40 pages.
For each page saves the rendered HTML, the visible text and a screenshot. Then downloads the stylesheets, images and font files the
pages reference. Output under ../brand/midnight-city/ (kept out of git: third-party material).
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

from scrapling.fetchers import DynamicFetcher, Fetcher

BASE = "https://midnight.city"
OUT = Path(__file__).resolve().parent.parent / "brand" / "midnight-city"
PAGES, ASSETS, SHOTS = OUT / "pages", OUT / "assets", OUT / "screens"
for d in (PAGES, ASSETS, SHOTS):
    d.mkdir(parents=True, exist_ok=True)
DISALLOW = ("/api/", "/observer/", "/coordinator/", "/admin/")
UA = {"User-Agent": "privateEventsResearch/1.0"}
MAX_PAGES, DELAY = 40, 2.5


def slug(url):
    p = urlparse(url)
    s = (p.path.strip("/") or "home").replace("/", "_")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)[:80]


def allowed(url):
    p = urlparse(url)
    return p.netloc in ("midnight.city", "www.midnight.city") and not p.path.startswith(DISALLOW) \
        and not re.search(r"\.(png|jpe?g|gif|webp|svg|ico|css|js|woff2?|ttf|otf|mp4|webm|pdf|zip)$", p.path, re.I)


def main():
    queue, seen, pages = [BASE + "/"], set(), []
    assets = {}
    while queue and len(pages) < MAX_PAGES:
        url = urldefrag(queue.pop(0))[0].rstrip("/") or BASE
        if url in seen or not allowed(url + "/"):
            continue
        seen.add(url)
        name = slug(url)
        shot = SHOTS / f"{name}.png"

        def action(page, _shot=shot):
            page.wait_for_timeout(2500)
            page.screenshot(path=str(_shot), full_page=True)
            return page

        try:
            r = DynamicFetcher.fetch(url, headless=True, network_idle=True, timeout=60000, page_action=action)
        except Exception as exc:  # noqa: BLE001
            print("FAIL", url, str(exc)[:120])
            continue
        if r.status != 200:
            print("status", r.status, url)
            continue
        html = bytes(r.body).decode("utf8", "replace")
        (PAGES / f"{name}.html").write_text(html)
        text = r.get_all_text(separator="\n", strip=True)
        (PAGES / f"{name}.txt").write_text(text)
        pages.append({"url": url, "file": name, "chars": len(text), "title": (r.css("title::text").get() or "").strip()})
        print(f"ok {url} ({len(text)} chars)")
        for a in r.css("a"):
            h = a.attrib.get("href")
            if h:
                u = urldefrag(urljoin(url + "/", h))[0]
                if allowed(u) and u.rstrip("/") not in seen and u not in queue:
                    queue.append(u)
        for sel, attr in (("link[rel=stylesheet]", "href"), ("link[rel=icon]", "href"), ("link[rel=preload]", "href"),
                          ("img", "src"), ("source", "src"), ("meta[property='og:image']", "content"), ("script[src]", "src")):
            for e in r.css(sel):
                v = e.attrib.get(attr)
                if v:
                    assets[urljoin(url + "/", v)] = sel
        time.sleep(DELAY)
    # stylesheets first, then the url() references inside them
    todo = dict(assets)
    done = {}
    css_seen = set()
    while todo:
        u, why = todo.popitem()
        if u in done:
            continue
        p = urlparse(u)
        ext = Path(p.path).suffix.lower()
        if "fonts.googleapis.com" in p.netloc:
            ext = ".css"
        if ext not in (".css", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".js") and "fonts.googleapis.com" not in p.netloc:
            done[u] = "skipped"
            continue
        if ext == ".js" and "midnight.city" not in p.netloc:
            done[u] = "skipped"
            continue
        try:
            time.sleep(0.6)
            resp = Fetcher.get(u, impersonate="chrome", timeout=60, headers=UA)
        except Exception as exc:  # noqa: BLE001
            done[u] = f"error {str(exc)[:60]}"
            continue
        if resp.status != 200:
            done[u] = f"status {resp.status}"
            continue
        body = bytes(resp.body)
        fname = re.sub(r"[^A-Za-z0-9_.-]+", "_", (p.netloc + p.path + ("_" + p.query if p.query else "")))[-120:]
        if not Path(fname).suffix:
            fname += ext or ".bin"
        (ASSETS / fname).write_bytes(body)
        done[u] = fname
        if ext == ".css":
            css = body.decode("utf8", "replace")
            css_seen.add(fname)
            for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css):
                if not ref.startswith("data:"):
                    nu = urljoin(u, ref)
                    if nu not in done and nu not in todo:
                        todo[nu] = "css-url"
    (OUT / "manifest.json").write_text(json.dumps({"pages": pages, "assets": done}, indent=1))
    print(f"{len(pages)} pages, {sum(1 for v in done.values() if not str(v).startswith(('skipped', 'error', 'status')))} assets saved to {OUT}")


if __name__ == "__main__":
    main()
