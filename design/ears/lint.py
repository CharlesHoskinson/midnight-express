#!/usr/bin/env python3
"""Lint EARS requirement files.

    python3 design/ears/lint.py FILE [FILE ...]      (or a directory of .md files)

Checks each `### MPE-<AREA>-<NNN> title` record: one sentence containing "shall"; pattern keyword matches the
declared Pattern; <= 60 words; no weasel words or "and/or"; required attributes with allowed values.
Exit code 1 if any record fails.
"""
import re, sys, collections
from pathlib import Path

WEASEL = re.compile(r"\b(fast|quickly|secure|securely|appropriate|appropriately|as needed|user[- ]friendly|etc\.?|and/or|robust|reasonable|adequate|efficient|efficiently|easy|simple|flexible|state[- ]of[- ]the[- ]art)\b", re.I)
HEAD = re.compile(r"^### (MPE-([A-Z]{3})-(\d{3})[a-z]?)\s*(.*)$")
ATTR = re.compile(r"^- (Pattern|Scope|Priority|Source|Rationale|Verify|Status):\s*(.*)$")
PAT = {"ubiquitous": None, "state": r"^\s*While\b", "event": r"^\s*When\b", "optional": r"^\s*Where\b",
       "unwanted": r"^\s*If\b.*\bthen\b", "complex": r"^\s*(While|When|Where|If)\b"}
OK = {"Pattern": set(PAT), "Scope": {"POC", "PROD"}, "Priority": {"MUST", "SHOULD", "MAY"}}


def records(text):
    cur = None
    for line in text.splitlines():
        m = HEAD.match(line)
        if m:
            if cur: yield cur
            cur = {"id": m.group(1), "area": m.group(2), "title": m.group(4), "sentence": [], "attrs": {}}
            continue
        if cur is None: continue
        a = ATTR.match(line)
        if a: cur["attrs"][a.group(1)] = a.group(2).strip()
        elif line.startswith("## ") or line.startswith("# "):
            yield cur; cur = None
        elif line.strip() and not line.startswith("- ") and not cur["attrs"]:
            cur["sentence"].append(line.strip())
    if cur: yield cur


def check(r):
    errs = []
    s = " ".join(r["sentence"])
    n = len(s.split())
    if not s: errs.append("no EARS sentence")
    if s and not re.search(r"\bshall\b", s): errs.append('no "shall"')
    if len(re.findall(r"\bshall\b", s)) > 1: errs.append('more than one "shall" (not atomic)')
    if n > 60: errs.append(f"{n} words (>60)")
    w = WEASEL.findall(s)
    if w: errs.append("weasel: " + ", ".join(sorted({x.lower() for x in w})))
    for k in ("Pattern", "Scope", "Priority", "Source", "Rationale", "Verify", "Status"):
        if k not in r["attrs"]: errs.append(f"missing {k}")
    for k, allowed in OK.items():
        v = r["attrs"].get(k)
        if v and v.split()[0].strip("`").lower() not in {a.lower() for a in allowed}: errs.append(f"bad {k}: {v[:30]}")
    p = (r["attrs"].get("Pattern") or "").split()[0].lower() if r["attrs"].get("Pattern") else ""
    if p in PAT and PAT[p] and s and not re.search(PAT[p], s): errs.append(f"sentence does not match pattern '{p}'")
    if p == "ubiquitous" and re.match(r"^\s*(While|When|Where|If)\b", s): errs.append("ubiquitous sentence starts with a trigger keyword")
    st = r["attrs"].get("Status", "")
    if st and not re.match(r"^(settled|open \(DEC-[A-Z]{3}-\d+\))", st): errs.append(f"bad Status: {st[:30]}")
    return errs


def main():
    files = []
    for a in sys.argv[1:]:
        p = Path(a); files += sorted(p.glob("*.md")) if p.is_dir() else [p]
    bad = 0; tot = 0; stats = collections.Counter(); ids = collections.Counter()
    for f in files:
        for r in records(f.read_text()):
            tot += 1; ids[r["id"]] += 1
            e = check(r)
            for k in ("Pattern", "Scope", "Priority"): stats[(k, (r["attrs"].get(k) or "?").split()[0].lower())] += 1
            if e:
                bad += 1; print(f"{f.name}: {r['id']}: " + "; ".join(e))
    dup = [i for i, c in ids.items() if c > 1]
    print(f"\n{tot} requirements, {bad} with problems, {len(dup)} duplicate ids {dup[:5]}")
    for k in ("Pattern", "Scope", "Priority"):
        print(k + ":", {v: c for (kk, v), c in sorted(stats.items()) if kk == k})
    sys.exit(1 if bad or dup else 0)

if __name__ == "__main__":
    main()
