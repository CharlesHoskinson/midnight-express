#!/usr/bin/env python3
"""Tabulate compile outputs of a Compact contract.

Usage: measure.py <compiler-output-dir> <zkir-binary>

For every circuit under <dir>/zkir it prints the ZKIR sizes (.zkir JSON and
.bzkir binary), the proving- and verifying-key sizes under <dir>/keys, and the
circuit model reported by `zkir mock-compile -v` (k, rows, table rows, and the
model `size` field, which is the proof size in bytes), and the number of
declared public inputs. Output is one JSON object per line. MOCK_TIMEOUT
(seconds, default 300) bounds each mock compile; a circuit that exceeds it
is reported with null model fields.
"""
import json
import os
import re
import subprocess
import sys

out, zkir = sys.argv[1], sys.argv[2]
zdir = os.path.join(out, "zkir")
kdir = os.path.join(out, "keys")


def size(p):
    return os.path.getsize(p) if os.path.exists(p) else None


for f in sorted(os.listdir(zdir)):
    if not f.endswith(".zkir"):
        continue
    name = f[:-5]
    row = {
        "circuit": name,
        "zkir_json_B": size(os.path.join(zdir, f)),
        "bzkir_B": size(os.path.join(zdir, name + ".bzkir")),
        "prover_B": size(os.path.join(kdir, name + ".prover")),
        "verifier_B": size(os.path.join(kdir, name + ".verifier")),
    }
    src = os.path.join(zdir, name + ".bzkir")
    if not os.path.exists(src):
        src = os.path.join(zdir, f)
    try:
        ir = json.load(open(os.path.join(zdir, f)))
        row["pi"] = sum(1 for i in ir.get("instructions", []) if i.get("op") == "declare_pub_input")
    except (OSError, ValueError):
        row["pi"] = None
    try:
        r = subprocess.run([zkir, "mock-compile", "-v", src], capture_output=True, text=True,
                           timeout=int(os.environ.get("MOCK_TIMEOUT", "300")))
        text = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        text = ""
    for key in ("k", "rows", "table_rows", "advice_columns", "lookups", "size"):
        m = re.search(r"\b" + key + r": (\d+)", text)
        row[key] = int(m.group(1)) if m else None
    print(json.dumps(row))
