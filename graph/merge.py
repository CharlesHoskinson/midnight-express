#!/usr/bin/env python3
"""Merge Luna chunk extractions + catalog metadata into one graphify extraction.

    python3 graph/merge.py [--out DIR]    (default DIR = graph/out, result graph/extract.json)

Rules
- Named nodes (id starts with concept_) merge across papers. Spelling variants fold onto the most
  frequent spelling: trailing plural s and suffixes _protocol/_system/_scheme/_attack are ignored
  when grouping.
- Paper-local nodes keep the id "<doc>__<label>"; a wrong prefix from the model is repaired.
- Placeholder nodes ("not discussed") and edges to unknown ids are dropped.
- Every document gets a paper node (catalog metadata) with `discusses` edges to the named nodes
  it contributed.
"""
import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G = ROOT / "graph"


def slug(s):
    s = s.lower().replace("++", "pp").replace("+", "plus")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def fix_id(raw, doc):
    raw = (raw or "").strip()
    if raw.lower().startswith("concept_"):
        return "concept_" + slug(raw[8:])
    tail = raw.split("__", 1)[1] if "__" in raw else raw
    return f"{doc}__{slug(tail)[:70]}"


def fold_key(cid):
    k = re.sub(r"_(protocol|system|scheme|attack|attacks|mechanism)$", "", cid)
    return re.sub(r"(?<=[a-z]{3})s$", "", k)


META = ("the chunk", "this chunk", "the excerpt", "the document", "not discussed", "not mentioned")


def is_meta(d):
    d = (d or "").strip().lower()
    return d.startswith(META) or len(d) < 25


def better_desc(new, old):
    """Prefer a substantive description over a meta remark, then the longer one (capped)."""
    if is_meta(new):
        return False
    if is_meta(old):
        return True
    return len(new) > len(old) and len(new) <= 420


def load_catalog():
    by_file = {}
    for f in sorted((ROOT / "catalog").glob("*.jsonl")):
        if f.name.startswith("iog-library"):
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            p = r.get("pdf_path")
            if not p:
                continue
            name = Path(p).stem
            cur = by_file.setdefault(name, dict(r, clusters=[r.get("cluster")]))
            if r.get("cluster") not in cur["clusters"]:
                cur["clusters"].append(r.get("cluster"))
    return by_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(G / "out"))
    ap.add_argument("--dest", default=str(G / "extract.json"))
    a = ap.parse_args()
    vocab = {}
    for line in (G / "vocab.txt").read_text().splitlines():
        if " = " in line:
            i, n = line.split(" = ", 1)
            vocab[i] = n
    cat = load_catalog()
    raw_nodes, raw_edges, usage = [], [], collections.Counter()
    for f in sorted(Path(a.out).glob("*.json")):
        env = json.loads(f.read_text())
        if env.get("status") != "SUCCESS":
            usage["error"] += 1
            continue
        usage["ok"] += 1
        doc, chunk = env["doc"], env["chunk"]
        so = env["structured_output"]
        idmap = {}
        for n in so["nodes"]:
            d = (n.get("description") or "").lower()
            if "not discussed" in d or "not mentioned" in d or "not stated in this chunk" in d:
                continue
            nid = fix_id(n["id"], doc)
            idmap[n["id"]] = nid
            raw_nodes.append(dict(n, id=nid, doc=doc, chunk=chunk))
        for e in so["edges"]:
            s = idmap.get(e["source"], fix_id(e["source"], doc))
            t = idmap.get(e["target"], fix_id(e["target"], doc))
            raw_edges.append(dict(e, source=s, target=t, doc=doc, chunk=chunk))
    freq = collections.Counter(n["id"] for n in raw_nodes if n["id"].startswith("concept_"))
    groups = collections.defaultdict(list)
    for cid in freq:
        groups[fold_key(cid)].append(cid)
    canon = {c: max(v, key=lambda x: (freq[x], -len(x))) for v in groups.values() for c in v}
    for i in vocab:  # a vocabulary id always wins as the canonical spelling of its group
        for c in groups.get(fold_key(i), []):
            canon[c] = i
    canon_id = lambda i: canon.get(i, i)  # noqa: E731

    nodes = {}
    for n in raw_nodes:
        cid = canon_id(n["id"])
        doc = n["doc"]
        pdf = next((p for p in ("pdfs/%s.pdf" % doc, "pdfs/%s.md" % doc) if (ROOT / p).exists()), f"pdfs/{doc}")
        if cid in nodes:
            old = nodes[cid]
            old["mentions"] = old.get("mentions", 1) + 1
            old.setdefault("docs", set()).add(doc)
            if better_desc(n["description"], old["description"]):
                old["description"] = n["description"]
            continue
        nodes[cid] = {"id": cid, "label": n["label"].strip()[:120], "file_type": "concept",
                      "entity_type": n["entity_type"], "named": bool(n["named"]),
                      "description": n["description"], "evidence": n["evidence"],
                      "source_file": pdf, "source_location": n["source_location"],
                      "mentions": 1, "docs": {doc}, "_origin": "llm"}
    # named nodes seen in several papers get the vocabulary label when available
    for cid, n in nodes.items():
        if cid in vocab:
            n["label"] = vocab[cid]
    edges, seen = [], set()
    dropped = 0
    for e in raw_edges:
        s, t = canon_id(e["source"]), canon_id(e["target"])
        for end in (s, t):
            if end not in nodes and end in vocab:
                nodes[end] = {"id": end, "label": vocab[end], "file_type": "concept", "entity_type": "concept",
                              "named": True, "description": f"{vocab[end]} (referenced; no description extracted)",
                              "evidence": "", "source_file": "", "source_location": "", "mentions": 0,
                              "docs": set(), "_origin": "vocab"}
        if s == t or s not in nodes or t not in nodes:
            dropped += 1
            continue
        key = (s, t, e["relation"])
        if key in seen:
            continue
        seen.add(key)
        edges.append({"source": s, "target": t, "relation": e["relation"], "confidence": "EXTRACTED",
                      "confidence_score": 1.0, "weight": 1.0, "evidence": e["evidence"],
                      "source_file": f"pdfs/{e['doc']}", "source_location": "", "_origin": "llm"})
    # paper nodes and discusses edges
    docs = {n["doc"] for n in raw_nodes}
    papers = 0
    for doc in sorted(docs):
        r = cat.get(doc, {})
        pdf = next((p for p in ("pdfs/%s.pdf" % doc, "pdfs/%s.md" % doc) if (ROOT / p).exists()), f"pdfs/{doc}")
        pid = f"paper_{slug(doc)}"
        nodes[pid] = {"id": pid, "label": (r.get("title") or doc)[:160], "file_type": "paper",
                      "entity_type": "paper", "named": False,
                      "description": (r.get("note") or "")[:400], "evidence": "",
                      "source_file": pdf, "source_location": "title page",
                      "year": r.get("year"), "venue": r.get("venue"), "doi": r.get("doi"),
                      "clusters": [c for c in r.get("clusters", []) if c], "role": r.get("role"),
                      "bitmessage_link": r.get("bitmessage_link"), "mentions": 0, "docs": {doc}, "_origin": "catalog"}
        papers += 1
    per_doc = collections.defaultdict(set)
    for n in raw_nodes:
        if n["id"].startswith("concept_"):
            per_doc[n["doc"]].add(canon_id(n["id"]))
    for doc, ids in per_doc.items():
        for cid in ids:
            if cid in nodes:
                edges.append({"source": f"paper_{slug(doc)}", "target": cid, "relation": "discusses",
                              "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 0.5, "evidence": "",
                              "source_file": f"pdfs/{doc}", "source_location": "", "_origin": "catalog"})
    for n in nodes.values():
        n["docs"] = sorted(n.get("docs", []))
    out = {"nodes": list(nodes.values()), "edges": edges, "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
    Path(a.dest).write_text(json.dumps(out, ensure_ascii=False))
    named = sum(1 for n in nodes.values() if n["id"].startswith("concept_"))
    multi = sum(1 for n in nodes.values() if n["id"].startswith("concept_") and len(n["docs"]) >= 2)
    print(f"chunks ok {usage['ok']} err {usage['error']} | nodes {len(nodes)} (papers {papers}, named {named}, "
          f"named in >=2 papers {multi}) | edges {len(edges)} (dropped {dropped}) | folded {sum(1 for k, v in canon.items() if k != v)} ids")


if __name__ == "__main__":
    main()
