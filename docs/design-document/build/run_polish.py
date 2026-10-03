#!/usr/bin/env python3
"""Humanizer and lessons pass over every file: draft-r3 -> draft-r4. Resume-safe.

    python3 run_polish.py [--only a.md,b.md] [--workers 6] [--src draft-r3] [--out draft-r4]

Each file gets the humanizer skill, WRITING_LESSONS.md sections 1-3 and the mechanical lint findings for that file. Headings may be repaired
but their {#anchors} and count must stay; numbers, citations, identifiers, tables, footnotes and normative keywords are checked before and after.
Length must stay within -3% / +4% of the input.
"""
import argparse, concurrent.futures as cf, json, re, subprocess, sys
from pathlib import Path
import run_inkwell as R
D, ROOT = R.D, R.ROOT
HUM = Path("/home/charl/.claude/skills/humanizer/SKILL.md")


def lint_report(path):
    r = subprocess.run([sys.executable, str(D / "build/lint_prose.py"), str(path)], capture_output=True, text=True)
    return r.stdout.strip()


def anchors(t):
    return sorted(re.findall(r"\{#[A-Za-z0-9_:.\-]+\}", t))


def polish(f, src, out, force):
    o = out / f
    if o.exists() and o.stat().st_size > 800 and not force:
        return f, "skip"
    t0 = (src / f).read_text()
    a = R.inv(t0)
    nw = R.words(t0)
    lo, hi = int(nw * 0.97), int(nw * 1.04)
    kind = R.kind(f)
    rep = lint_report(src / f)
    prompt = f"""You are the final prose editor of a long technical design document, "Midnight Express: Private Events for Midnight". Your task is to make the file read as written by a careful human expert, not by a language model, without changing what it says.

Read first and obey:
1. {HUM}: the humanizer skill. Run its detect, rewrite, audit loop silently; your output is the final version only. Voice calibration: the sample is the file itself; match its register (plain, exact, technical). Do not add personality, opinions, first person or invented facts. The "PERSONALITY AND SOUL" section does not apply to this register.
2. {D}/WRITING_LESSONS.md sections 1 to 3 (pattern catalogue, headings, paragraph and section shape) as hard rules. Section 4 lists the mechanical checks; the lint findings for this file are below. Fix each real hit by rewriting the sentence; if a hit is a legitimate technical use, leave it.
3. {D}/STYLE.md (including Vocabulary) and {D}/FACTS.md (wins on any number or name).
4. Voice: the text was written in an adaptation of the Grothendieck English profile ({R.GUIDE}). Keep its structure of motivated definitions, worked consequences and exact status of claims; the polish must not flatten it or remove the added explanatory prose for new readers. Do not mention any style or author.

Rules:
- Preserve every number, unit, requirement identifier, citation key [@slug], footnote, figure marker {{{{fig:N-M}}}}, table (all rows and cells), normative keyword and the status of every claim (measured, derived, assumed, proposed, unknown). Do not delete content to fix a pattern; rewrite it. Keep length within {lo} to {hi} words (the input has {nw}).
- Headings: repair headings that match the bad patterns by the rules of section 2 (state the thing or the finding, sentence case, no announcing). Keep every {{#anchor}} and keep the heading count and nesting exactly. {"This is a proposal file: the Foundation's template headings are fixed; do not change any heading." if kind == "mip" else ""}{" This is a reading-list section: keep each `@slug ::` line start and order; edit only annotation text." if kind == "reading" else ""}
- Remove signposting and recap paragraphs endings except where section 3 allows them. End sections on a fact, decision or consequence. Vary sentence and paragraph length. Replace stacked hedges by one exact qualification. Replace unquantified comparatives by the number, or by nothing.
- No em dashes. No placeholders. No mention of this task, the guide, the lint, editors, drafts or any process.

LINT FINDINGS FOR THIS FILE (advisory):
{rep}

FILE ({f}):
<<<
{t0}
>>>

Your entire final message is the complete Markdown of the revised file and nothing else."""
    t = R.claude(prompt, adddirs=(ROOT, R.INK, Path("/home/charl/.claude/skills/humanizer")))
    for _ in range(2):
        b = R.inv(t) if t else None
        probs = []
        if not t:
            probs.append("empty output")
        else:
            probs = R.loss({**a, "headings": [], "refs": a["refs"]}, {**b, "headings": []})
            if len(a["headings"]) != len(b["headings"]):
                probs.append(f"heading count {len(a['headings'])} -> {len(b['headings'])}")
            if anchors(t0) != anchors(t):
                probs.append("heading anchors {#...} changed")
            w = R.words(t)
            if w < lo:
                probs.append(f"too short: {w}, need {lo} to {hi}")
            if w > hi:
                probs.append(f"too long: {w}, need {lo} to {hi}")
        if not probs:
            break
        fix = f"""Your revised file has defects against the original. Repair them and return the complete file only.\nDEFECTS:\n- """ + "\n- ".join(probs) + f"\n\nORIGINAL:\n<<<\n{t0}\n>>>\n\nYOUR REVISION:\n<<<\n{t}\n>>>"
        r2 = R.claude(fix, adddirs=(ROOT,))
        if r2:
            t = r2
    if not t:
        return f, "failed"
    t = re.split(r"\n+(?:TECHNICAL NOTE|NOTE TO EDITOR):", t)[0].rstrip() + "\n"
    out.mkdir(exist_ok=True)
    o.write_text(t)
    left = R.loss(a, R.inv(t))
    return f, f"ok {nw}->{R.words(t)} loss={len(left)}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--src", default="draft-r3"); ap.add_argument("--out", default="draft-r4"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    src, out = D / a.src, D / a.out
    fs = [f for f in R.FILES if (src / f).exists() and (not a.only or f in a.only.split(","))]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda f: polish(f, src, out, a.force), fs):
            print(*r, flush=True)
