#!/usr/bin/env python3
"""Second open-access pass that does not need OpenAlex.

For each metadata_only record, look for a legal open copy through:
  1. arXiv API title search (accept only a near-exact title match),
  2. HAL API by DOI, then by title,
  3. CORE API by DOI (anonymous; skipped if it refuses).
Every candidate goes through pe_fetch's PDF check (200 + %PDF-). No email, no login, no bot-wall bypass.

    ~/.local/share/uv/tools/scrapling/bin/python scripts/oa_upgrade2.py SLICE [SLICE ...]
"""
import json
import re
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = Path.home() / ".local/share/uv/tools/scrapling/bin/python"
FETCH = ROOT / "scripts/pe_fetch.py"
ATOM = "{http://www.w3.org/2005/Atom}"


def fetch(*args):
    res = subprocess.run([str(PY), str(FETCH), *args], capture_output=True, text=True)
    return res.stdout


def jget(url):
    out = fetch("json", url)
    lines = [l for l in out.splitlines() if l.startswith("{") or l.startswith("[")]
    try:
        return json.loads(lines[-1]) if lines else {}
    except Exception:
        return {}


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower().replace("-", " ")).split()


def same_title(a, b):
    x, y = norm(a), norm(b)
    if not x or not y:
        return False
    common = len(set(x) & set(y))
    return common / max(len(set(x)), len(set(y))) >= 0.92 and abs(len(x) - len(y)) <= 3


def cand_arxiv(title):
    q = urllib.parse.quote('ti:"%s"' % re.sub(r'["]', "", title)[:200])
    xml = fetch("json", f"https://export.arxiv.org/api/query?search_query={q}&max_results=3")
    if "<feed" not in xml:
        return []
    try:
        root = ET.fromstring(xml[xml.index("<?xml"):] if "<?xml" in xml else xml)
    except ET.ParseError:
        return []
    out = []
    for e in root.findall(ATOM + "entry"):
        t = " ".join((e.findtext(ATOM + "title") or "").split())
        if same_title(t, title):
            i = (e.findtext(ATOM + "id") or "").replace("http://", "https://")
            out.append(i.replace("/abs/", "/pdf/"))
    return out


def cand_hal(rec):
    out = []
    doi = (rec.get("doi") or "").strip()
    queries = []
    if doi:
        queries.append(f'doiId_s:"{doi}"')
    queries.append('title_t:"%s"' % re.sub(r'["]', "", rec["title"])[:160])
    for q in queries:
        d = jget("https://api.archives-ouvertes.fr/search/?wt=json&rows=3&fl=title_s,fileMain_s&q=" + urllib.parse.quote(q))
        for x in (d.get("response") or {}).get("docs", []):
            t = (x.get("title_s") or [""])[0]
            if x.get("fileMain_s") and (doi or same_title(t, rec["title"])):
                out.append(x["fileMain_s"])
    return out


def cand_core(rec):
    doi = (rec.get("doi") or "").strip()
    if not doi:
        return []
    d = jget("https://api.core.ac.uk/v3/search/works?limit=1&q=" + urllib.parse.quote(f'doi:"{doi}"'))
    return [r["downloadUrl"] for r in d.get("results", []) if r.get("downloadUrl")]


def main():
    got = total = 0
    for sl in sys.argv[1:]:
        path = ROOT / "catalog" / f"{sl}.jsonl"
        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        for r in rows:
            if r.get("status") != "metadata_only" or not r.get("slug") or not r.get("title"):
                continue
            total += 1
            urls = cand_arxiv(r["title"]) + cand_hal(r) + cand_core(r)
            ok = False
            for u in dict.fromkeys(urls):
                out = fetch("pdf", u, r["slug"])
                lines = [l for l in out.splitlines() if l.startswith("{")]
                res = json.loads(lines[-1]) if lines else {}
                if res.get("ok"):
                    r.update(status="downloaded", pdf_path=res["path"], sha256=res["sha256"], pdf_url=u,
                             upgraded_via="oa_upgrade2")
                    got += 1
                    ok = True
                    print(f"UP   {sl}: {r['title'][:70]}", flush=True)
                    break
            if not ok:
                print(f"keep {sl}: {r['title'][:70]}", flush=True)
            if total % 20 == 0:  # checkpoint
                path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    print(f"upgraded {got} of {total}")


if __name__ == "__main__":
    main()
