#!/usr/bin/env python3
"""Name graph communities with gpt-6-luna in parallel.

    python3 graph/label.py [--min-size 30] [--workers 44]
Writes graph/labels/<cid>.json and graph/labels.json (cid -> name). Communities below --min-size, or
that fail, get "<top member label> cluster".
"""
import argparse, concurrent.futures as cf, json, subprocess, tempfile, time
from pathlib import Path
G = Path(__file__).resolve().parent
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["name", "summary"],
          "properties": {"name": {"type": "string"}, "summary": {"type": "string"}}}
PROMPT = """You name clusters in a knowledge graph about decentralized publish/subscribe, gossip and overlay networks, private and metadata-private messaging, anonymity and related cryptography.
Below are the members of one cluster (label | type | description), most connected first. Answer with JSON: `name` = a specific topic name of 2 to 6 words (not generic words like "Cluster" or "Group"), `summary` = one sentence on what the cluster is about. Use only the members shown. No commands, no files.

MEMBERS:
@@M@@
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--min-size", type=int, default=30); ap.add_argument("--workers", type=int, default=44)
    a = ap.parse_args()
    an = json.loads((G / "analysis.json").read_text())
    ex = json.loads((G / "extract.json").read_text())
    nodes = {n["id"]: n for n in ex["nodes"]}
    deg = {}
    for e in ex["edges"]:
        deg[e["source"]] = deg.get(e["source"], 0) + 1; deg[e["target"]] = deg.get(e["target"], 0) + 1
    (G / "labels").mkdir(exist_ok=True)
    (G / "label_schema.json").write_text(json.dumps(SCHEMA))
    comm = an["communities"]
    jobs = []
    for cid, mem in comm.items():
        top = sorted(mem, key=lambda m: -deg.get(m, 0))[:14]
        text = "\n".join(f"{nodes[m]['label'][:70]} | {nodes[m]['entity_type']} | {nodes[m]['description'][:130]}" for m in top if m in nodes)
        jobs.append((cid, len(mem), text, nodes[top[0]]["label"] if top and top[0] in nodes else f"Community {cid}"))
    todo = [j for j in jobs if j[1] >= a.min_size and not (G / "labels" / f"{j[0]}.json").exists()]
    print(f"{len(todo)} communities to name", flush=True)
    def one(j):
        cid, n, text, top = j
        for attempt in range(3):
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    subprocess.run(["codex", "exec", "-m", "gpt-6-luna", "-c", 'model_reasoning_effort="low"', "--ephemeral", "--ignore-user-config",
                                    "-s", "read-only", "--skip-git-repo-check", "-C", tmp, "--output-schema", str(G / "label_schema.json"),
                                    "-o", f"{tmp}/o.json", PROMPT.replace("@@M@@", text)], capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
                    so = json.loads(Path(f"{tmp}/o.json").read_text())
                    if so.get("name"):
                        (G / "labels" / f"{cid}.json").write_text(json.dumps(so)); return True
                except Exception:
                    time.sleep(5)
        return False
    done = 0; t0 = time.time()
    with cf.ThreadPoolExecutor(a.workers) as ex2:
        for ok in ex2.map(one, todo):
            done += 1
            if done % 50 == 0: print(f"{done}/{len(todo)} wall={time.time()-t0:.0f}s", flush=True)
    names = {}
    for cid, n, text, top in jobs:
        p = G / "labels" / f"{cid}.json"
        names[cid] = json.loads(p.read_text())["name"] if p.exists() else f"{top[:40]} cluster"
    (G / "labels.json").write_text(json.dumps(names))
    print("labels.json written;", sum(1 for j in jobs if (G / 'labels' / f'{j[0]}.json').exists()), "named by Luna")

if __name__ == "__main__":
    main()
