#!/usr/bin/env python3
"""Mechanical prose checks from WRITING_LESSONS.md section 4.

    python3 lint_prose.py DIR_OR_FILES... [--json out.json] [--samples 3]

Reports per file the checks that fail or exceed their threshold, with sample sentences. A failure is a prompt to read, not an auto-edit.
"""
import json, re, statistics, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
LES = (D / "WRITING_LESSONS.md").read_text()
sec4 = LES.split("## 4. Mechanical checks")[1].split("## 5. Sources")[0]
PAT = {}
for m in re.finditer(r"^(C\d+)\.[^\n]*\n(.*?)(?=^C\d+\.|\Z)", sec4, re.S | re.M):
    cid, body = m.group(1), m.group(2)
    blk = re.search(r"```\n(.*?)```", body, re.S)
    if not blk:
        continue
    pats = {}
    for line in blk.group(1).strip().splitlines():
        mm = re.match(r"^(abstract|any|self|question|reveal|run-in|bold|announce|role-of|stock|item):\s*(.*)$", line)
        if mm:
            pats[mm.group(1)] = mm.group(2)
        else:
            pats.setdefault("main", line)
    PAT[cid] = pats


def comp(p, flags=0):
    return re.compile(p, flags)


def prose(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    out = []
    for l in text.splitlines():
        if l.startswith("|") or l.startswith("![") or l.startswith("\\partpage") or l.startswith(":::") or l.startswith("<"):
            continue
        out.append(l)
    t = "\n".join(out)
    t = re.sub(r"\[@[^\]]*\]", "", t)
    t = re.sub(r"\^\[[^\]]*\]", "", t)
    t = re.sub(r"`[^`]*`", "X", t)
    return t


def sentences(par):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\x60(])", par) if s.strip()]


def check(path):
    raw = path.read_text()
    t = prose(raw)
    heads = [l for l in raw.splitlines() if re.match(r"#{1,6} ", l)]
    nw = max(1, len(re.sub(r"[#*_>]", " ", t).split()))
    pars = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip() and not p.startswith("#")]
    pars_prose = [p for p in pars if not re.match(r"^\s*([-*+]|\d+\.)\s", p)]
    per = lambda n: round(n * 1000 / nw, 2)  # noqa: E731
    res = {}

    def hits(cid, key="main", flags=re.I, text=None):
        p = PAT.get(cid, {}).get(key)
        if not p:
            return []
        out = []
        for m in re.finditer(p, text if text is not None else t, flags):
            a = max(0, m.start() - 50); b = min(len(t), m.end() + 50)
            out.append((text if text is not None else t)[a:b].replace("\n", " "))
        return out

    def add(cid, name, hs, limit=0, rate=False):
        n = len(hs)
        val = per(n) if rate else n
        if val > limit:
            res[cid] = {"name": name, "count": n, "per1000": per(n), "limit": limit, "samples": hs[:4]}

    add("C1", "em dash", re.findall(r".{0,40}—.{0,40}", t))
    add("C3", "banned vocabulary", hits("C3"))
    add("C4", "watch vocabulary", hits("C4"), 2, True)
    add("C5", "banned phrases", hits("C5"))
    add("C6", "negative parallelism", hits("C6"), 1)
    add("C7", "rather than", hits("C7"), 0.5, True)
    add("C8", "copula avoidance", [h for h in hits("C8") if not re.search(r"acts? as|functions? as", h)])
    add("C9", "participial tails", hits("C9"), 1, True)
    add("C10", "abstract triads", hits("C10", "abstract"))
    add("C11", "stacked hedges", hits("C11"))
    c12 = [h for h in hits("C12") if not re.search(r"honest (node|relay|peer|majority|party)", h, re.I)]
    add("C12", "intensifiers", c12, 1, True)
    add("C13", "unquantified comparatives", [h for h in hits("C13") if not re.search(r"\d", h)])
    add("C14", "vague attribution", hits("C14"))
    add("C15", "transition openers", hits("C15", flags=0), 1, True)
    ends = [sentences(p)[-1] for p in pars_prose if len(sentences(p)) >= 2]
    c19 = [e for e in ends if re.match(PAT["C19"]["main"], e, re.I)]
    add("C19", "summary-ending paragraphs", c19)
    c20 = [e for e in ends if re.match(PAT["C20"]["main"], e, re.I)]
    add("C20", "demonstrative closers", c20, 1)
    add("C21a", "signposting", hits("C21"), 0)
    add("C21b", "self-reference", hits("C21", "self"), 2)
    add("C22a", "rhetorical question", hits("C22", "question", flags=re.M))
    add("C22b", "colon reveal", hits("C22", "reveal", flags=0))
    add("C24", "bold run-in", hits("C24", "run-in", flags=re.M), 0)
    # sentence rhythm
    lens = []
    firsts = []
    for p in pars_prose:
        ss = sentences(p)
        for s in ss:
            w = len(s.split())
            if w >= 3:
                lens.append(w)
        firsts += [" ".join(s.split()[:2]).lower() for s in ss]
    if len(lens) > 10:
        cv = statistics.pstdev(lens) / statistics.mean(lens)
        if cv < 0.5:
            res["C17"] = {"name": "sentence-length variation too low", "count": 1, "cv": round(cv, 2), "limit": 0.5, "samples": []}
    run = 0
    rep = []
    for i in range(2, len(firsts)):
        if firsts[i] == firsts[i - 1] == firsts[i - 2]:
            rep.append(firsts[i])
    add("C16", "three sentences opening alike", rep)
    pl = [len(p.split()) for p in pars_prose]
    if len(pl) > 8:
        cv = statistics.pstdev(pl) / statistics.mean(pl)
        if cv < 0.6:
            res["C18"] = {"name": "paragraph-length variation too low", "count": 1, "cv": round(cv, 2), "limit": 0.6, "samples": []}
    items = len(re.findall(PAT["C23"]["item"], t)) if "C23" in PAT else 0
    if pars_prose and items / max(1, len(pars_prose)) > 0.35:
        res["C23"] = {"name": "bullets-to-prose ratio", "count": items, "ratio": round(items / len(pars_prose), 2), "limit": 0.35, "samples": []}
    hs = [h for h in heads if not re.search(r"MIP|MPS|Abstract|Motivation|Specification|Rationale|Versioning|Copyright|License|Path to|Acceptance|Backwards|Security|Reference|Open Questions|Use Cases|Problem|Goals|Non-Goals|Requirements|Implementation|Test|Appendix|Introduction|Conclusion", h)]
    bad_heads = []
    for h in hs:
        for k in ("announce", "role-of", "stock"):
            if re.search(PAT["C26"][k], h + "\n", re.I | re.M):
                bad_heads.append(h)
        if re.search(PAT["C25"]["main"], h):
            bad_heads.append(h + "   [case]")
    if bad_heads:
        res["C25/26"] = {"name": "headings", "count": len(bad_heads), "samples": bad_heads[:8], "limit": 0}
    return {"file": path.name, "words": nw, "fails": res}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    jout = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    if jout:
        args.remove(jout)
    files = []
    for a in args:
        p = Path(a)
        files += sorted(p.glob("*.md")) if p.is_dir() else [p]
    out = [check(f) for f in files]
    tot = 0
    for r in out:
        print(f"{r['file']}  ({r['words']} words)  {len(r['fails'])} checks flagged")
        for cid, v in sorted(r["fails"].items()):
            tot += v["count"]
            extra = f" cv={v.get('cv', v.get('ratio'))}" if "cv" in v or "ratio" in v else f" n={v['count']} ({v.get('per1000', '')}/1000)"
            print(f"   {cid} {v['name']}{extra}")
            for s in v["samples"][:2]:
                print(f"        ...{s.strip()[:110]}")
    print("TOTAL flags:", tot)
    if jout:
        Path(jout).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
