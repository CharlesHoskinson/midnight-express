#!/usr/bin/env python3
"""Fan out graph extraction over chunks with gpt-6-luna via `codex exec`.

Each job is a pure function: chunk text inlined in the prompt, JSON out through --output-schema,
read-only sandbox, empty working dir. Outputs go to graph/out/<chunk>.json and are resumable.

    python3 graph/run_all.py --workers 32 [--limit N] [--effort low] [--only SUBSTR]
"""
import argparse
import concurrent.futures as cf
import json
import subprocess
import tempfile
import threading
import time
from pathlib import Path

G = Path(__file__).resolve().parent
OUT = G / "out"
PROMPT = (G / "prompt.txt").read_text()
VOCAB = (G / "vocab.txt").read_text().strip()
SCHEMA = G / "schema.json"
lock = threading.Lock()
stats = {"ok": 0, "fail": 0, "empty": 0, "retry": 0, "secs": 0.0}


def build_prompt(row):
    text = (G / "chunks" / row["chunk"]).read_text()
    return (PROMPT.replace("@@VOCAB@@", VOCAB).replace("@@DOC@@", row["doc"])
            .replace("@@TITLE@@", row.get("title") or row["doc"])
            .replace("@@CHUNKNO@@", str(row["n"])).replace("@@TEXT@@", text))


def is_done(dst, row):
    """A result counts as done when it succeeded and is non-empty (or the chunk is tiny,
    or an empty answer was already confirmed by retries)."""
    try:
        env = json.loads(dst.read_text())
    except Exception:
        return False
    if env.get("status") != "SUCCESS":
        return False
    return bool(env["structured_output"]["nodes"]) or row["bytes"] < 3000 or env.get("confirmed_empty", False)


def run_one(row, model, effort, timeout):
    dst = OUT / (row["chunk"] + ".json")
    if dst.exists() and is_done(dst, row):
        return "skip"
    prompt = build_prompt(row)
    last_err = ""
    for attempt in range(3):
        with tempfile.TemporaryDirectory() as tmp:
            t0 = time.time()
            try:
                res = subprocess.run(
                    ["codex", "exec", "-m", model, "-c", f'model_reasoning_effort="{effort}"',
                     "--ephemeral", "--ignore-user-config", "-s", "read-only", "--skip-git-repo-check", "-C", tmp,
                     "--output-schema", str(SCHEMA), "-o", f"{tmp}/last.json", prompt],
                    capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
                dt = time.time() - t0
                so = json.loads(Path(f"{tmp}/last.json").read_text())
                assert "nodes" in so and "edges" in so
                if not so["nodes"] and row["bytes"] >= 3000 and attempt < 2:
                    effort = "medium"  # Luna sometimes answers empty under load; ask again
                    with lock:
                        stats["retry"] += 1
                    time.sleep(3)
                    continue
                env = {"status": "SUCCESS", "engine": f"codex:{model}:{effort}", "seconds": round(dt, 1),
                       "chunk": row["chunk"], "doc": row["doc"], "structured_output": so,
                       "confirmed_empty": not so["nodes"]}
                dst.write_text(json.dumps(env, ensure_ascii=False))
                with lock:
                    stats["ok"] += 1
                    stats["secs"] += dt
                    if not so["nodes"]:
                        stats["empty"] += 1
                return "ok"
            except Exception as exc:  # noqa: BLE001
                last_err = f"{type(exc).__name__}: {exc}"[:300]
                tail = ""
                try:
                    tail = (res.stderr or "")[-300:]
                except Exception:
                    pass
                last_err += " | " + tail.replace("\n", " ")
                with lock:
                    stats["retry"] += 1
                time.sleep(10 * (attempt + 1))
    dst.write_text(json.dumps({"status": "ERROR", "chunk": row["chunk"], "error": last_err}))
    with lock:
        stats["fail"] += 1
    return "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only", default="")
    ap.add_argument("--seed", type=int, default=0, help="shuffle seed for samples (0 = file order)")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    rows = [json.loads(l) for l in (G / "chunks.jsonl").read_text().splitlines()]
    if a.only:
        rows = [r for r in rows if a.only in r["chunk"]]
    if a.seed:
        import random
        random.Random(a.seed).shuffle(rows)
    todo = []
    for r in rows:
        p = OUT / (r["chunk"] + ".json")
        if p.exists() and is_done(p, r):
            continue
        todo.append(r)
    if a.limit:
        todo = todo[: a.limit]
    print(f"{len(rows)} chunks; {len(todo)} to run with {a.workers} workers ({a.model}, {a.effort})", flush=True)
    t0 = time.time()
    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(run_one, r, a.model, a.effort, a.timeout) for r in todo]
        for f in cf.as_completed(futs):
            done += 1
            if done % 25 == 0 or done == len(futs):
                el = time.time() - t0
                with lock:
                    avg = stats["secs"] / max(1, stats["ok"])
                    print(f"{done}/{len(futs)} ok={stats['ok']} fail={stats['fail']} retries={stats['retry']} "
                          f"empty={stats['empty']} avg_call={avg:.0f}s wall={el:.0f}s "
                          f"rate={done / el * 60:.1f}/min", flush=True)


if __name__ == "__main__":
    main()
