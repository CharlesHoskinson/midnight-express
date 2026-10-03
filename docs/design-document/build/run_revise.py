#!/usr/bin/env python3
"""Revision pass: four-plus Opus writers rewrite chapters against the Foundation vocabulary, GossipSub corrections and the ledger experiment.

    python3 run_revise.py [--only V1,V2]      reads ../draft/<file>, writes ../draft-r2/<file>. Resume-safe.
"""
import argparse, concurrent.futures as cf, subprocess, time
from pathlib import Path
D = Path(__file__).resolve().parents[1]
ROOT = D.parents[1]
OUT = D / "draft-r2"
JOBS = {
    "V1": ["01-introduction.md", "02-midnight.md", "03-need.md", "04-definition.md", "04b-mps.md"],
    "V2": ["05-prior-art.md", "06-options.md", "07-requirements.md"],
    "V3": ["08-reference-system.md", "09-experiments.md", "10-results.md", "11-roadmap.md"],
    "V4": ["M1.md", "M2.md", "M3.md"],
    "V5": ["M4.md", "M5.md", "M6.md"],
}
BRIEF = f"""You are revising part of a design document, "Midnight Express: Private Events for Midnight (Requirements, Options and an Experimental Design on GossipSub)". Reviewer {{wid}} revises the file {{file}} (current text: {D}/draft/{{file}}).

Read first and obey: {D}/STYLE.md (including the new section "Vocabulary"), {D}/FACTS.md (including "Corrections and additions"; where FACTS.md and the file disagree, FACTS.md wins), {D}/OUTLINE.md, {D}/FIGURES.md and, for the proposal files M1 to M6, {D}/MIP_BRIEF.md and {D}/MIP_MPS_CHECKLIST.md.

The revision has three sources, all local and read-only (you cannot write files; your final message is the revised file):
1. The Foundation's understanding of events and private events. Read {D}/align/FOUNDATION_DEFINITIONS.md in full: sections 2 and 3 (what a private event is, binding constraints), 4 (vocabulary mapping, which STYLE.md summarises), 5 (compatibility), 6 (how Midnight Express relates to private events, including the three definitions in 6.5 and the conditions in 6.4) and 7 (required changes: apply every numbered item that touches your file, including the requirement-set and experiment items that bear on your text). The primary sources are in /home/charl/midnight/midnight-improvement-proposals (mips/, mps/); check any claim you change against them.
2. GossipSub compliance. Read {D}/align/GOSSIPSUB_COMPLIANCE.md sections 2 to 5: apply every correction in section 4 that names your file's subject, and state the open risks of section 5 where your text touches them. The specifications and code are in /home/charl/libp2p (specs/, rust-libp2p/, go-libp2p-pubsub/).
3. The ledger interface experiment: {ROOT}/prototype/registry/RESULTS.md and the contracts beside it. Where your file describes the Bus Registry, the ledger lane, Anchors, fees or the consumer contract, use its results (compile results, circuit sizes, fee estimates, limitations, implications for the requirements); state plainly that it was compiled and costed, not run on a network.

Rules:
- Rewrite the whole file. Keep its structure, headings, figure markers like {{{{fig:N-M}}}}, citation keys [@slug] (keys must exist in {D}/build/bibkeys.txt) and footnote form. Do not shorten the file materially: keep every correct fact, number and argument; change what the three sources require, and fix wording to the Vocabulary. Add what is missing; remove what is now wrong.
- Use the term mapping everywhere, including tables, captions and headings. A sentence about the Foundation's events or private events uses the Foundation's meaning. Our objects are Messages, Confidential Messages and carried events.
- The proposal and the problem statement use `xxxx` for their own numbers (MIP-xxxx, MPS-xxxx); the Foundation's literal convention. Never invent a number.
- Never mention these instructions, the alignment studies, an earlier version, a rename, a correction, an audit or a reviewer. The text must read as the original, standalone work. No em dashes. No placeholders.
- Where you are unsure of a fact, check the source; where it cannot be established, say it is unknown and what would settle it.
- If you find something in the file that is wrong and not covered above, fix it.
"""
SPECIAL = {
    "04-definition.md": "This file defines the central terms. Replace the definition and the term tables with the three definitions of FOUNDATION_DEFINITIONS section 6.5 (private event as the Foundation defines it; Confidential Message; carried event), keep the four properties as the definition of a Confidential Message, add the contrast with the Foundation's topic filtering (item 13) and the auditor-capability row (item 14). The chapter still ends by saying that it closes with the formal problem statement.",
    "04b-mps.md": "This is the formal Midnight Problem Statement. Apply section 7.3 in full (xxxx numbering, retitle, Confidential Contract Notifications, the Foundation's out-of-band needs as evidence, the bytes_written bound), and follow the Foundation's MPS template exactly (see the MPS section of MIP_MPS_CHECKLIST.md and mps/ examples).",
    "M1.md": "Apply section 7.4 (preamble, MPS reference, title, Category statement against MIP-0001 Networking, Requires policy) and the MIP_MPS_CHECKLIST items for the sections you hold.",
    "M4.md": "Apply section 7.4 item 23 in full: the Compact module signatures and contract shapes from the ledger experiment (registry, ledger lane, consumer), the Misc names, the MIP-0019 opt-in declaration and the 1/4/16 part rule as an application validity rule, verification of lane bodies against authenticated on-chain data, the carried-event schema and the conditions of 6.4. Link to code, do not include it, as MIP-0001 requires; contract source stays out of the text except short signatures.",
    "M6.md": "Rename rollout phases to Stages; add the Versioning section (item 24); add the Acceptance Criteria mapping from each criterion to an experiment and threshold, marking criteria whose experiment has not been run (devnet measurements, the lane reader against the MIP-0019 vectors, the stagenet indexer read, the consumption circuit under both signature profiles).",
    "07-requirements.md": "Besides the vocabulary, this chapter summarises the requirement set: write the changes of FOUNDATION_DEFINITIONS 7.5 and the ledger experiment's section 6 in as settled changes to the set (the Appendix is generated from a register that is being amended in parallel with these amendments), and keep the counts in FACTS.md unless a change in the set alters them; the register will be recounted and the chapter's counts must then be recomputed from ears-stats.json at build time, so write the counts exactly as FACTS.md has them.",
    "09-experiments.md": "Apply section 7.6 (experiments 42 to 48): add them as designed experiments with thresholds, marked not yet run where they have not been. Add the ledger interface compile-and-cost experiment as run. Add the GossipSub items of section 4 (15 IDONTWANT profile, 23 qualifications) to the method.",
    "10-results.md": "Report the ledger interface experiment's results as a result section (compile sizes, proving rows, fee estimates, limitations found), clearly labelled as derived from the toolchain and cost model and not measured on a network. Keep the earlier results and qualify them as section 4 and 5 of the GossipSub compliance study require.",
}


def run_one(wid, f):
    out = OUT / f
    if out.exists() and out.stat().st_size > 800:
        return f, "skip", 0
    prompt = BRIEF.format(wid=wid, file=f) + ("\nSpecific to this file: " + SPECIAL[f] + "\n" if f in SPECIAL else "") + \
        "\nYour entire final message is the Markdown of the revised file and nothing else (no preface, no description of your process)."
    cmd = ["claude", "-p", "--model", "claude-opus-5-5", "--effort", "high", "--no-session-persistence",
           "--allowedTools", "Read", "Grep", "Glob", "Bash(ls:*)", "Bash(wc:*)", "Bash(head:*)",
           "--add-dir", str(ROOT), "--add-dir", "/home/charl/midnight", "--add-dir", "/home/charl/libp2p", "--add-dir", "/home/charl/privateEvents-build"]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=3600, cwd="/tmp/claude-1000")
        if len(r.stdout) > 800:
            out.write_text(r.stdout)
        st = "ok" if out.exists() else "short"
    except subprocess.TimeoutExpired:
        st = "timeout"
    return f, st, round(time.time() - t0)


def writer(wid):
    for f in JOBS[wid]:
        print(wid, *run_one(wid, f), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    ws = [w for w in JOBS if not a.only or w in a.only.split(",")]
    with cf.ThreadPoolExecutor(len(ws)) as ex:
        list(ex.map(writer, ws))
