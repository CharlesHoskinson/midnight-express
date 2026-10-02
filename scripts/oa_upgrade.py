#!/usr/bin/env python3
"""Upgrade metadata_only catalog records to downloaded when a legal open copy exists.

For each record with status metadata_only in the named slices:
  1. arXiv id            -> https://arxiv.org/pdf/<id>
  2. DOI                 -> OpenAlex single-work lookup (best_oa_location, then other locations)
  3. a known pdf_url     -> tried as is
Each candidate goes through pe_fetch's PDF check (status 200 and a %PDF- header), so landing
pages and paywall HTML are rejected. No email is sent; no login or bot wall is bypassed.

    ~/.local/share/uv/tools/scrapling/bin/python scripts/oa_upgrade.py SLICE [SLICE ...]
"""
import json
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = Path.home() / ".local/share/uv/tools/scrapling/bin/python"
FETCH = ROOT / "scripts/pe_fetch.py"


def run(*args):
    res = subprocess.run([str(PY), str(FETCH), *args], capture_output=True, text=True)
    lines = [l for l in res.stdout.splitlines() if l.startswith("{") or l.startswith("[")]
    return json.loads(lines[-1]) if lines else {}


def candidates(rec):
    seen = []

    def add(u):
        if u and u not in seen and u.startswith("http"):
            seen.append(u)

    if rec.get("arxiv"):
        add(f"https://arxiv.org/pdf/{rec['arxiv']}")
    doi = (rec.get("doi") or "").replace("https://doi.org/", "").strip()
    if doi:
        q = urllib.parse.quote(f"https://doi.org/{doi}", safe="")
        w = run("json", "https://api.openalex.org/works/" + q +
                "?select=best_oa_location,locations,open_access")
        if isinstance(w, dict) and "locations" in w:
            add((w.get("best_oa_location") or {}).get("pdf_url"))
            for loc in w.get("locations") or []:
                add(loc.get("pdf_url"))
            add((w.get("open_access") or {}).get("oa_url"))
    add(rec.get("pdf_url"))
    return seen


def main():
    total = got = 0
    for sl in sys.argv[1:]:
        path = ROOT / "catalog" / f"{sl}.jsonl"
        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        for r in rows:
            if r.get("status") != "metadata_only" or not r.get("slug"):
                continue
            total += 1
            for url in candidates(r):
                if "dl.acm.org" in url or "ieeexplore" in url or "doi.org/10." in url:
                    continue  # publisher walls: never attempted
                res = run("pdf", url, r["slug"])
                if res.get("ok"):
                    r.update(status="downloaded", pdf_path=res["path"], sha256=res["sha256"],
                             pdf_url=url, upgraded_via="oa_upgrade")
                    got += 1
                    print(f"UP   {sl}: {r['title'][:70]}", flush=True)
                    break
            else:
                print(f"keep {sl}: {r['title'][:70]}", flush=True)
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"upgraded {got} of {total}")


if __name__ == "__main__":
    main()
