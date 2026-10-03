#!/usr/bin/env python3
"""Apply audit/FIX_PLAN.md file by file: draft-r5 (else draft-r4) -> draft-r6. Resume-safe.
    python3 run_fix.py [--only a.md,b.md] [--workers 10]"""
import argparse, concurrent.futures as cf, re
from pathlib import Path
import run_inkwell as R
import run_single as S
D, ROOT = R.D, R.ROOT
PLAN = (D / "audit/FIX_PLAN.md").read_text()
OUT = D / "draft-r6"
L = PLAN.splitlines()
def idx(pred, start=0):
    return next(i for i in range(start, len(L)) if pred(L[i]))
s1 = idx(lambda l: l.startswith("## 1."))
s2 = idx(lambda l: l.startswith("## 2."))
s3 = idx(lambda l: l.startswith("## 3."))
CANON = "\n".join(L[s1:s2])
SEC3 = "\n".join(L[s3:])
def file_section(f):
    try:
        a = idx(lambda l: l.strip() == f"### {f}", s2)
    except StopIteration:
        return ""
    b = idx(lambda l: l.startswith("### ") or l.startswith("## 3."), a + 1)
    return "\n".join(L[a:b])
def cur(f):
    return (D / "draft-r5" / f) if (D / "draft-r5" / f).exists() else (D / "draft-r4" / f)
FILES = [f for f in R.FILES] + ["00-executive-summary.md", "12-conclusion.md"]
PROMPT = """You are the editor of one file of the design document "Midnight Express: Private Events for Midnight". Apply a fix plan to the file {f} (current text: {src}) and return the corrected file.

Read {D}/STYLE.md and {D}/FACTS.md (FACTS.md is partly superseded by the canonical decisions below: they win). Then apply, completely and exactly:
(1) every item for {f} in the PER-FILE FIXES below (each gives a quoted anchor that occurs once in the file; make the change at that anchor);
(2) every item of SECTION 3 (process traces and AI patterns) that concerns {f};
(3) the CANONICAL DECISIONS wherever the file states or implies the matter they decide, even where no fix item names the place.
Rules: change nothing else except what a fix requires for consistency; keep every other word, number, table row, citation key, footnote, heading and {{#anchor}}; keep the Foundation vocabulary and the single-specification, no-proof-of-concept-yet framing (exploratory runs guided the design and support nothing); never mention this plan, fixes, audits or editing; no em dashes; no placeholders; do not add statements that point at the number of checks, reviews or tests as authority. If a fix item cannot be applied because its anchor is not found, apply the intent at the right place. If a canonical table must appear in this file (the plan says which file carries it), copy it exactly.

=== CANONICAL DECISIONS ===
{canon}

=== PER-FILE FIXES FOR {f} ===
{mine}

=== SECTION 3 ===
{sec3}

Your entire final message is the complete Markdown of the corrected file and nothing else."""

def run(f):
    out = OUT / f
    if out.exists() and out.stat().st_size > 800:
        return f, "skip"
    src = cur(f)
    mine = file_section(f)
    if not mine and f not in ("00-executive-summary.md",):
        pass
    base = src.read_text()
    prompt = PROMPT.format(f=f, src=src, D=D, canon=CANON, mine=mine or "(no fix items for this file; apply canonical decisions and section 3 only)", sec3=SEC3)
    for attempt in range(2):
        t = R.claude(prompt, adddirs=(ROOT, "/home/charl/midnight", "/home/charl/libp2p"), timeout=3500, cwd="/tmp/claude-1000/fixwork")
        if not t:
            continue
        lines = t.splitlines(); i = next((k for k, l in enumerate(lines) if l.startswith("#")), 0)
        t = "\n".join(lines[i:]).rstrip() + "\n"
        probs = []
        if len(re.findall(r"^#{1,6} ", t, flags=re.M)) < 0.9 * len(re.findall(r"^#{1,6} ", base, flags=re.M)):
            probs.append("headings lost")
        if R.words(t) < 0.8 * R.words(base):
            probs.append("file lost more than 20 percent of its words")
        if S.BAD.search(t):
            probs.append("multi-build language present")
        if probs and attempt == 0:
            prompt += "\n\nYour previous attempt failed a check: " + "; ".join(probs) + ". Return the complete corrected file."
            continue
        OUT.mkdir(exist_ok=True)
        out.write_text(t)
        return f, f"ok {R.words(base)}->{R.words(t)} {','.join(probs)}"
    return f, "failed"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    fs = [f for f in FILES if (cur(f)).exists() and (not a.only or f in a.only.split(","))]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(run, fs):
            print(*r, flush=True)
