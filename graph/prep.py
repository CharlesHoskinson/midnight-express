#!/usr/bin/env python3
"""Prepare corpus text for LLM extraction.

pdfs/* (PDF or Markdown) -> unique files by sha256 -> graph/text/<doc>.txt -> page-aligned chunks
in graph/chunks/<doc>__NN.txt plus graph/chunks.jsonl (one line per chunk).

Doc id = file stem. The title comes from the first non-duplicate catalog record whose pdf_path
names the file. Bibliographies are cut so the model reads claims, not reference lists.
Idempotent: chunks already written are kept; new files are added.

    python3 graph/prep.py [--chunk-bytes 20000]
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G = ROOT / "graph"
TEXT, CHUNKS = G / "text", G / "chunks"
REF = re.compile(r"^\s*(?:\d+\.?\s*)?(references|bibliography|literature cited)\s*$", re.I | re.M)


def catalog_index():
    idx = {}
    for f in sorted((ROOT / "catalog").glob("*.jsonl")):
        if f.name.startswith("iog-library"):
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            p = r.get("pdf_path")
            if p and r.get("status") != "duplicate":
                idx.setdefault(Path(p).name, r)
    return idx


def to_text(path):
    if path.suffix.lower() == ".pdf":
        res = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True)
        raw = res.stdout.decode("utf-8", "replace")
        pages = raw.split("\f")
        out = [f"[p.{i}]\n{p.strip()}" for i, p in enumerate(pages, 1) if p.strip()]
        return "\n\n".join(out)
    return path.read_text(errors="replace")


def cut_refs(text):
    hits = [m for m in REF.finditer(text)]
    for m in reversed(hits):
        if m.start() > 0.45 * len(text):
            tail = len(text) - m.start()
            if tail < 0.4 * len(text):
                return text[: m.start()]
    return text


def chunk(text, limit):
    parts, cur, size = [], [], 0
    for para in re.split(r"\n{2,}", text):
        if size + len(para) > limit and cur:
            parts.append("\n\n".join(cur))
            cur, size = [], 0
        while len(para) > limit:  # one huge paragraph
            parts.append(para[:limit])
            para = para[limit:]
        cur.append(para)
        size += len(para) + 2
    if cur:
        parts.append("\n\n".join(cur))
    return parts


def work(args):
    path, limit = args
    doc = path.stem
    text = cut_refs(to_text(path))
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    (TEXT / f"{doc}.txt").write_text(text)
    if len(text) < 2500:
        return doc, 0, len(text), "short"
    pieces = chunk(text, limit)
    for i, p in enumerate(pieces, 1):
        (CHUNKS / f"{doc}__{i:02d}.txt").write_text(p)
    return doc, len(pieces), len(text), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk-bytes", type=int, default=20000)
    a = ap.parse_args()
    TEXT.mkdir(exist_ok=True)
    CHUNKS.mkdir(exist_ok=True)
    idx = catalog_index()
    seen, todo = {}, []
    for p in sorted((ROOT / "pdfs").iterdir()):
        if p.suffix.lower() not in (".pdf", ".md"):
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h in seen:
            continue
        seen[h] = p.name
        if not (CHUNKS / f"{p.stem}__01.txt").exists() and not (TEXT / f"{p.stem}.txt").exists():
            todo.append((p, a.chunk_bytes))
    print(f"unique files {len(seen)}; to process {len(todo)}")
    with cf.ProcessPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(work, todo))
    short = [r for r in results if r[3] == "short"]
    print(f"processed {len(results)}; short/scanned {len(short)}")
    with (G / "short.txt").open("a") as fh:
        for d, _, n, _ in short:
            fh.write(f"{d}\t{n}\n")
    rows = []
    for p in sorted(CHUNKS.glob("*__*.txt")):
        doc, n = p.stem.rsplit("__", 1)
        rec = idx.get(doc + ".pdf") or idx.get(doc + ".md") or {}
        rows.append({"chunk": p.name, "doc": doc, "n": int(n), "bytes": p.stat().st_size,
                     "title": rec.get("title"), "year": rec.get("year"), "cluster": rec.get("cluster"),
                     "slug": rec.get("slug")})
    with (G / "chunks.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    docs = {r["doc"] for r in rows}
    print(f"chunks {len(rows)} across {len(docs)} docs; avg {sum(r['bytes'] for r in rows)//max(1,len(rows))} bytes")


if __name__ == "__main__":
    main()
