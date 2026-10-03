#!/usr/bin/env python3
"""Build design/ears/MPE-EARS-INDEX.md from the twelve area files, reconcile.json and POC_CORE.md.

    python3 design/ears/build_index.py
One table row per requirement (area files are the authoritative text). Applies: fixes (replaced IDs), gap records,
duplicate marks (canonical owner) and PoC-core membership.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint import records  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
R5 = ROOT / "design/rounds/r5"
E = ROOT / "design/ears"

rec = {}
for f in sorted(R5.glob("*.md")):
    for r in records(f.read_text()):
        rec[r["id"]] = dict(r, file=f.name, sentence=" ".join(r["sentence"]))
rj = json.loads((E / "reconcile.json").read_text()) if (E / "reconcile.json").exists() else {}
dup = {o: d["canonical"] for d in rj.get("duplicates", []) for o in d.get("others", [])}
fixed = {x["replaces"]: x["id"] for x in rj.get("fixes", []) if x.get("replaces")}
gaps = {g["id"]: g for g in rj.get("gaps", [])}
core = set(re.findall(r"MPE-[A-Z]{3}-\d{3}[a-z]?", (E / "POC_CORE.md").read_text())) if (E / "POC_CORE.md").exists() else set()
rows = []
for i, r in sorted(rec.items()):
    a = r["attrs"]
    flags = []
    if i in dup: flags.append("dup of " + dup[i])
    if i in fixed: flags.append("fixed as " + fixed[i])
    if i in core: flags.append("POC-CORE")
    rows.append(f"| {i} | {r['title'][:60]} | {(a.get('Pattern') or '').split()[0] if a.get('Pattern') else ''} | {(a.get('Scope') or '').split()[0] if a.get('Scope') else ''} | {(a.get('Priority') or '').split()[0] if a.get('Priority') else ''} | {(a.get('Status') or '')[:22]} | {'; '.join(flags)} |")
for gid, g in gaps.items():
    rows.append(f"| {gid} | (gap record) | | | | | added by reconciliation{'; POC-CORE' if gid in core else ''} |")
out = ["# MPE requirements index", "",
       f"{len(rec)} drafted requirements in 12 area files (`design/rounds/r5/`), {len(gaps)} gap records, {len(core)} in the prototype core.", "",
       "| ID | Title | Pattern | Scope | Priority | Status | Flags |", "|---|---|---|---|---|---|---|"] + rows
(E / "MPE-EARS-INDEX.md").write_text("\n".join(out) + "\n")
print(f"index: {len(rec)} requirements, {len(gaps)} gaps, {len(core)} core, {len(dup)} duplicates marked")
