#!/usr/bin/env python3
"""Print the compile-results table of RESULTS.md from out/*.measure.jsonl."""
import json
import sys

def fmt(v):
    return "not generated" if v is None else f"{v:,}"

print("| Contract | Circuit | k | Rows | Proof B | Proving key B | Verifying key B | ZKIR B (.zkir / .bzkir) | PI |")
print("|---|---|---|---|---|---|---|---|---|")
for path in sys.argv[1:]:
    contract = path.split("/")[-1].split("-")[0]
    for line in open(path):
        r = json.loads(line)
        print(f"| {contract} | `{r['circuit']}` | {fmt(r['k'])} | {fmt(r['rows'])} | {fmt(r['size'])} | "
              f"{fmt(r['prover_B'])} | {fmt(r['verifier_B'])} | {fmt(r['zkir_json_B'])} / {fmt(r['bzkir_B'])} | "
              f"{r.get('pi', '')} |")
