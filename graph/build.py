#!/usr/bin/env python3
"""Build the graphify graph from graph/extract.json.

    python3 graph/build.py build                 cluster, write graph/analysis.json, print communities
    python3 graph/build.py label labels.json     write graphify-out/{graph.json,GRAPH_REPORT.md,graph.html}

Env: EXTRACT (default graph/extract.json), OUT (default graphify-out).
"""
import collections
import json
import os
import sys
from pathlib import Path

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.export import to_json
from graphify.report import generate

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = Path(os.environ.get("EXTRACT", ROOT / "graph/extract.json"))
OUT = Path(os.environ.get("OUT", ROOT / "graphify-out"))
OUT.mkdir(exist_ok=True)
ex = json.loads(EXTRACT.read_text())
G = build_from_json(ex, root=str(ROOT), directed=False)
ANALYSIS = ROOT / "graph/analysis.json"


def members_summary(G, comm, k=12):
    rows = {}
    for cid, mem in comm.items():
        top = sorted(mem, key=lambda m: -G.degree(m))[:k]
        rows[str(cid)] = {
            "size": len(mem),
            "top": [{"id": m, "label": G.nodes[m].get("label"), "type": G.nodes[m].get("entity_type")} for m in top],
            "papers": collections.Counter(G.nodes[m].get("source_file", "") for m in mem).most_common(3),
        }
    return rows


if sys.argv[1] == "build":
    comm = cluster(G)
    coh = score_all(G, comm)
    ANALYSIS.write_text(json.dumps({
        "communities": {str(k): v for k, v in comm.items()},
        "cohesion": {str(k): v for k, v in coh.items()},
        "gods": god_nodes(G, top_n=25),
        "surprises": surprising_connections(G, comm, top_n=20),
        "summary": members_summary(G, comm),
    }, ensure_ascii=False))
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(comm)} communities")
    for cid, mem in sorted(comm.items(), key=lambda kv: -len(kv[1]))[:25]:
        top = sorted(mem, key=lambda m: -G.degree(m))[:6]
        print(cid, len(mem), "|", ", ".join(str(G.nodes[m].get("label"))[:28] for m in top))
else:
    an = json.loads(ANALYSIS.read_text())
    comm = {int(k): v for k, v in an["communities"].items()}
    coh = {int(k): v for k, v in an["cohesion"].items()}
    names = {int(k): v for k, v in json.loads(Path(sys.argv[2]).read_text()).items()}
    labels = {c: names.get(c, f"Community {c}") for c in comm}
    papers = sorted({n.get("source_file") for _, n in G.nodes(data=True) if n.get("file_type") == "paper"})
    det = {"files": {"paper": papers}, "total_files": len(papers), "total_words": 0, "needs_graph": False,
           "warning": "", "skipped_sensitive": [], "unclassified": [], "walk_errors": [], "ignored": [],
           "pruned_noise_dirs": [], "graphifyignore_patterns": 0, "scan_root": str(ROOT)}
    q = suggest_questions(G, comm, labels)
    (OUT / "GRAPH_REPORT.md").write_text(generate(G, comm, coh, labels, an["gods"], an["surprises"], det,
                                                  {"input": 0, "output": 0}, str(ROOT), suggested_questions=q))
    (OUT / ".graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()}))
    ok = to_json(G, comm, str(OUT / "graph.json"), force=True, community_labels=labels)
    print("graph.json written" if ok else "WRITE FAILED", f"-> {OUT}")
