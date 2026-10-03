#!/usr/bin/env python3
"""Rewrite the files that depend on several builds so the document describes one specification and one implementation.
    python3 run_single.py [--only W1,W2]    reads ../draft-r4, writes ../draft-r5. Resume-safe."""
import argparse, concurrent.futures as cf, re
from pathlib import Path
import run_inkwell as R
D, ROOT = R.D, R.ROOT
IN, OUT = D / "draft-r4", D / "draft-r5"
GROUPS = {"W1": ["10-results.md"], "W2": ["09-experiments.md"], "W3": ["08-reference-system.md", "01-introduction.md", "11-roadmap.md"],
          "W4": ["06-options.md", "04-definition.md", "00-executive-summary.md", "12-conclusion.md"], "W5": ["M1.md", "M4.md", "M5.md", "M6.md"],
          "W6": ["07-requirements.md"], "W7": ["M2.md", "M3.md"], "W8": ["05-prior-art.md", "03-need.md", "04b-mps.md", "02-midnight.md"]}
BAD = re.compile(r"(?i)\b(three|3) (independent |separate )?(implementations|builds|builders)\b|\ball three (implementations|builds)\b|\bthe other two\b|\bimplementations? [ABC]\b|\bbuild [ABC]\b|\b(in|of|from) (A|B|C)(,|\.| and|'s)\b|\bthe winning\b|\bjudge[sd]?\b|\bbuilders?\b|\bindependent implementations\b")
BRIEF = """You are revising one file of the design document "Midnight Express: Private Events for Midnight". The file is {f}; its current text is {src}.

THE CHANGE. This document proposes a design and the plan for a proof of concept. It must not borrow credibility from experiments or from code that does not exist as a proof of concept. What happened: a series of throwaway exploratory runs (three separate Rust builds, compared and judged, with variant runs) was used to understand the design better and to decide what the proof of concept should be. Those runs may be mentioned as exploration that guided the design, and the document may say what they suggested, but nothing may rest on them. The proof of concept, a single reference implementation with a deterministic simulator, is the next step and has not been built.
1. Remove every statement that several implementations exist, were built, compared, judged or selected: no "independent implementations", "all three", "the other two", "implementation A/B/C", "builds", "builders", "the winner", "pilot results", "measured on the prototype", "the reference implementation exists/was run". Where the text says "the reference implementation" as something that exists, say "the proof of concept" as something to be built, or "the specified system" when describing the design.
2. Figures from the exploratory runs (delivery rates, latencies, amplification, bandwidth, CPU, restart or eclipse outcomes, leakage counts and so on) are not evidence. They may appear only in Chapter 10 and in one-sentence pointers elsewhere, each labelled an unreplicated exploratory observation that informed the design, never as support for a claim, a threshold, a choice, or a recommendation. In the executive summary, introduction, conclusion, problem statement and proposal, do not quote them at all; say in one plain sentence that exploratory runs guided the design and that a proof of concept is the next step. Where a design choice is justified by arithmetic from the specification, the Foundation's published limits, the rust-libp2p source or a cited paper, keep that justification and show the derivation. Where a choice was prompted only by the exploration, state it as a hypothesis that the proof of concept must test, with the test and its threshold, in Chapter 9 or Chapter 11.
3. Chapter 10 becomes short and honest: what the exploration suggested (a few paragraphs, with the figures labelled as in point 2), the compile-and-cost study of the ledger interface contracts (compiled with the stated toolchain; circuit sizes and fees derived from the cost model; nothing run on a network; the contracts are exploratory code and the design does not depend on them being final), and then what the proof of concept must establish first and in what order. It is not a results chapter and must not read like one.
4. Part III (Chapters 8 to 11) is the specification of the system under test and the experimental design for the proof of concept: scenarios, metrics, thresholds, controls, what each outcome would change, and a deterministic simulator plus a runnable single-implementation harness as deliverables of the first milestone. Write it in the future or conditional tense where it describes what will be built or run.
5. Established facts the text may state without hedging: arithmetic and derivations; facts read from Midnight's and libp2p's code and specifications (with the citation form of the style guide); what the design requires.

Keep: structure, headings and their {{#anchors}}, the Foundation vocabulary (STYLE.md Vocabulary section), citations, footnotes, every number that comes from arithmetic, specifications, code or the compile-and-cost study, normative keywords in the proposal files, and the honest limits (stand-in admission proof, nothing run on a Midnight network). Read {D}/STYLE.md, {D}/FACTS.md (which still mentions three implementations in places: FACTS.md is being corrected; this brief wins), and {D}/WRITING_LESSONS.md sections 1 to 3. No em dashes; no placeholders; no process words (drafts, passes, studies, reviewers, builds). Do not build authority by pointing at the number of checks, reviews, tests or implementations: state the evidence and its limit. Where a file is shorter after the change, that is fine; do not pad.
{extra}
Your entire final message is the complete Markdown of the revised file and nothing else."""
EXTRA = {"07-requirements.md": "The requirement register is generated separately; this chapter describes it. Where it says the prototype \"confirmed\" or \"the pilot found\" a decision, restate the decision as settled by argument or open pending the proof of concept. Keep the counts exactly as written.",
         "10-results.md": "This is the chapter most affected. Rewrite it as described in point 3, retitle it to match (keep the {#ch10} anchor, and the file name), and remove the figures that plot exploratory runs (take out their {{fig:...}} markers). It may stay a modest length.",
         "00-executive-summary.md": "Keep it to about 900 words and at most six paragraphs; replace the bullet lists by sentences except the list of options if you keep it short.", "12-conclusion.md": "Keep it to about 800 words, no bullet lists."}

def run(f, wid):
    out = OUT / f
    if out.exists() and out.stat().st_size > 800:
        return f, "skip"
    src = IN / f
    prompt = BRIEF.format(f=f, src=src, ROOT=ROOT, D=D, extra=EXTRA.get(f, ""))
    for attempt in range(2):
        t = R.claude(prompt, adddirs=(ROOT, "/home/charl/privateEvents-build", "/home/charl/libp2p", "/home/charl/midnight"), timeout=3300)
        if not t:
            continue
        L = t.splitlines(); i = next((k for k, l in enumerate(L) if l.startswith("#")), 0)
        t = "\n".join(L[i:])
        t = re.split(r"\n+(?:FIGURE NOTE|TECHNICAL NOTE):", t)
        note = t[1] if len(t) > 1 else ""
        t = t[0].rstrip() + "\n"
        bad = BAD.findall(t)
        if bad and attempt == 0:
            prompt += f"\n\nYour previous attempt still contained multi-build language ({len(bad)} hits, for example {BAD.search(t).group(0)!r}). Remove all of it."
            continue
        OUT.mkdir(exist_ok=True)
        out.write_text(t)
        if note:
            (D / "inkwell-notes" / (f + ".figure-note.txt")).write_text(note)
        return f, f"ok {len(t.split())} words, residual hits {len(bad)}"
    return f, "failed"

def work(wid):
    return [run(f, wid) for f in GROUPS[wid]]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="")
    a = ap.parse_args()
    ws = [w for w in GROUPS if not a.only or w in a.only.split(",")]
    with cf.ThreadPoolExecutor(len(ws)) as ex:
        for rs in ex.map(work, ws):
            for r in rs: print(*r, flush=True)
