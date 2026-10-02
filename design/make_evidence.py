#!/usr/bin/env python3
"""Build greppable evidence files for the design round.

    python3 design/make_evidence.py papers   -> design/evidence/papers.tsv
    python3 design/make_evidence.py graph    -> design/evidence/graph-digest.md  (needs graph/extract.json + analysis)

papers.tsv: one line per downloaded paper (slug, year, cluster, role, title, text path, pdf path, relevance
to Bitmessage, catalog note). Duplicate slugs resolve to the record that owns the file.
graph-digest.md: the named systems and attacks with their descriptions, the papers that discuss them, and the
strongest edges; then one block per community.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "design/evidence"


def papers():
    rows, seen = [], set()
    for f in sorted((ROOT / "catalog").glob("*.jsonl")):
        if f.name.startswith("iog-library"):
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            p = r.get("pdf_path")
            if r.get("status") != "downloaded" or not p or p in seen:
                continue
            seen.add(p)
            stem = Path(p).stem
            txt = ROOT / "graph/text" / f"{stem}.txt"
            note = " ".join((r.get("note") or "").split())[:420]
            link = " ".join((r.get("bitmessage_link") or "").split())[:240]
            rows.append("\t".join([
                r.get("slug") or stem, str(r.get("year") or ""), r.get("cluster") or "", r.get("role") or "",
                (r.get("title") or "").replace("\t", " "), f"graph/text/{stem}.txt" if txt.exists() else "",
                p, link, note]))
    header = "slug\tyear\tcluster\trole\ttitle\ttext_path\tpdf_path\tbitmessage_link\tnote"
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "papers.tsv").write_text(header + "\n" + "\n".join(sorted(rows)) + "\n")
    print(f"papers.tsv: {len(rows)} papers")


def graph():
    import collections
    ex = json.loads((ROOT / "graph/extract.json").read_text())
    nodes = {n["id"]: n for n in ex["nodes"]}
    deg = collections.Counter()
    out = collections.defaultdict(list)
    docs = collections.defaultdict(set)
    for e in ex["edges"]:
        deg[e["source"]] += 1
        deg[e["target"]] += 1
        if e["relation"] == "discusses":
            docs[e["target"]].add(e["source"].removeprefix("paper_"))
        else:
            out[e["source"]].append(e)
    named = [n for n in nodes.values() if n["id"].startswith("concept_")]
    named.sort(key=lambda n: -(len(docs[n["id"]]) * 3 + deg[n["id"]]))
    lines = ["# Graph digest", "",
             "Named systems, mechanisms, attacks and bounds extracted from the corpus, ordered by how many papers "
             "discuss them. Paper keys are file stems; look them up in papers.tsv.", ""]
    for n in named[:400]:
        lines.append(f"## {n['label']}  [{n['id']}]  ({n['entity_type']}; {len(docs[n['id']])} papers)")
        lines.append(n["description"].strip())
        ds = sorted(docs[n["id"]])[:8]
        if ds:
            lines.append("Papers: " + ", ".join(ds))
        rel = collections.defaultdict(list)
        for e in out[n["id"]][:60]:
            t = nodes.get(e["target"])
            if t:
                rel[e["relation"]].append(t["label"])
        for r, ts in sorted(rel.items()):
            lines.append(f"- {r}: " + "; ".join(sorted(set(ts))[:10]))
        lines.append("")
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "graph-digest.md").write_text("\n".join(lines))
    print(f"graph-digest.md: {min(400, len(named))} concepts of {len(named)} named nodes")


if __name__ == "__main__":
    {"papers": papers, "graph": graph}[sys.argv[1]]()
