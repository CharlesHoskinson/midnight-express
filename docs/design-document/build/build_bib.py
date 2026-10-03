#!/usr/bin/env python3
"""Build references.json (CSL JSON) from the catalog so that [@slug] citations resolve through pandoc-citeproc.

    python3 build_bib.py  -> references.json, bibkeys.txt   (downloaded papers only: every cited work was read)
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2].parent if False else Path(__file__).resolve().parents[3]
out, seen = [], set()
def person(s):
    s = s.strip()
    if not s: return None
    if "," in s:
        fam, giv = [x.strip() for x in s.split(",", 1)]
    else:
        parts = s.split()
        fam, giv = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (s, "")
    return {"family": fam, "given": giv}
for f in sorted((ROOT / "catalog").glob("*.jsonl")):
    if f.name.startswith("iog-library"): continue
    for line in f.read_text().splitlines():
        if not line.strip(): continue
        r = json.loads(line)
        slug, st = r.get("slug"), r.get("status")
        if not slug or st != "downloaded" or r.get("duplicate_of") or slug in seen: continue
        seen.add(slug)
        venue = (r.get("venue") or "").strip()
        kind = r.get("kind") or "paper"
        typ = {"rfc": "report", "spec": "webpage", "whitepaper": "report", "thesis": "thesis", "audit": "report", "report": "report"}.get(kind)
        if not typ:
            typ = "paper-conference" if re.search(r"conference|symposium|workshop|proceedings|ccs|ndss|usenix|eurocrypt|crypto|\bsp\b|icdcs|middleware|infocom|sosp|osdi|nsdi|eurosys|debs|podc|disc\b", venue, re.I) else ("article-journal" if venue and not re.search(r"arxiv|eprint|iacr", venue, re.I) else "article")
        e = {"id": slug, "type": typ, "title": (r.get("title") or slug).strip()}
        au = [p for p in (person(a) for a in (r.get("authors") or [])) if p]
        if au: e["author"] = au[:6] + ([{"literal": "et al."}] if len(au) > 6 else [])
        if r.get("year"): e["issued"] = {"date-parts": [[int(r["year"])]]}
        if venue: e["container-title"] = venue
        if r.get("doi"): e["DOI"] = r["doi"]
        url = r.get("landing_url") or r.get("pdf_url")
        if url: e["URL"] = url
        out.append(e)
(Path(__file__).parent / "references.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
(Path(__file__).parent / "bibkeys.txt").write_text("\n".join(sorted(seen)) + "\n")
print(len(out), "references;", sum(1 for e in out if "author" in e), "with authors;", sum(1 for e in out if "issued" in e), "with year")
