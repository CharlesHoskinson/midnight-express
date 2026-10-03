#!/usr/bin/env python3
"""Final audit: five Opus 5.5 (medium) readers with different personas. Output ../audit/final/<P>.md. Resume-safe.

    python3 run_personas.py [--doc build/document.md] [--round final]
"""
import argparse, concurrent.futures as cf, subprocess
from pathlib import Path
D = Path(__file__).resolve().parents[1]
ROOT = D.parents[1]
P = {
 "P1-concepts": "a protocol architect who checks CONCEPTS: every definition is introduced before use and used the same way everywhere; the privacy properties, adversaries and non-claims are consistent between chapters, the requirements, the experiments and the proposal; the logic from need to definition to options to requirements to experiments to proposal has no gap; claims are marked measured, derived, assumed, proposed or unknown correctly; the Foundation's meanings of event and private event are respected; the numbers agree across chapters (check against FACTS.md and the tables).",
 "P2-research": "a research reviewer who checks the RESEARCH: whether each claim about a paper, system or specification matches what that source says (open the source text through design/evidence/papers.tsv text_path, or the code under /home/charl/midnight and /home/charl/libp2p), whether the prior-art taxonomy is fair and complete for the question, whether important work is missing, whether limits from the literature are stated accurately, and whether the experiments' conclusions follow from the data and their stated limits.",
 "P3-citations": "a bibliographic auditor who checks the CITATIONS: every [@key] resolves in build/bibkeys.txt and supports the sentence it is attached to (spot-check at least 60 spread over all parts, more where a claim is strong), no claim that needs a citation lacks one, footnotes for code and documents give repository, path, symbol and branch or tag with access date, the reading list annotations match their works and its grouping makes sense, the References list has no placeholders or malformed entries, and the figures and tables are cited and numbered consistently.",
 "P4-flow": "an editor who checks FLOW: the order of chapters and sections, whether each chapter opens by connecting to the previous one and ends on a consequence, forward and backward cross-references that are wrong or missing, repetition across chapters, sections that are too long or too thin, whether a newcomer to Midnight, GossipSub and privacy engineering can follow in order, whether the executive summary and conclusion match the body, and whether the proposal reads as a coherent standalone document that follows the Foundation's template.",
 "P5-prose": "a prose stylist who checks ELEGANCE and AI-sounding patterns: apply /home/charl/privateEvents/docs/design-document/WRITING_LESSONS.md in full (patterns, headings, paragraph shape) and the humanizer catalogue at /home/charl/.claude/skills/humanizer/SKILL.md; find the passages that still sound machine-written (name the pattern), weak or announcing headings, uniform rhythm, summary-ending paragraphs, inflated or hedged sentences, jargon not taught, and repeated phrases; also praise nothing. Specifically hunt credibility-by-process: any sentence that builds authority by pointing to the number of checks, reviews, audits, agents, implementations or tests rather than to the evidence itself ("independent", "thoroughly verified", "cross-checked", "three separate builds"), badges of rigour, and repeated reminders of what was tested; each such sentence must be cut or replaced by the evidence or the limit. Give the repair text for every finding.",
}
BRIEF = """You are {persona}

Document: "Midnight Express: Private Events for Midnight", full text at {doc} (Markdown; the proposal at the end uses the Foundation's template). Read all of it in order (use the Read tool in sections; do not skip parts). Reference material, read-only: {D}/FACTS.md, {D}/STYLE.md, {D}/MIP_MPS_CHECKLIST.md, {D}/align/FOUNDATION_DEFINITIONS.md, {D}/align/GOSSIPSUB_COMPLIANCE.md, {ROOT}/design/evidence/papers.tsv, /home/charl/midnight, /home/charl/libp2p. No web access.

Report as your final message, no preface: findings ranked blocker, major, minor. For each: location (chapter, section heading and a quoted phrase of at least six words so it can be found by text search), what is wrong and the evidence you checked, and the exact replacement text or the exact change. Be specific and verifiable; do not report a preference without a reason. Then a list of at most ten things you checked and found sound. Do not describe your process. The document must read as standalone work: also report any trace of how it was made (mentions of drafts, reviewers, passes, studies, agents, placeholders), with the quoted text."""

def run(pid, doc, rnd):
    out = D / "audit" / rnd / f"{pid}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 1500:
        return pid, "skip"
    cmd = ["claude", "-p", "--model", "claude-opus-5-5", "--effort", "medium", "--no-session-persistence", "--allowedTools", "Read", "Grep", "Glob",
           "--add-dir", str(ROOT), "--add-dir", "/home/charl/midnight", "--add-dir", "/home/charl/libp2p", "--add-dir", "/home/charl/.claude/skills/humanizer"]
    r = subprocess.run(cmd, input=BRIEF.format(persona=P[pid], doc=doc, D=D, ROOT=ROOT), capture_output=True, text=True, timeout=7000, cwd="/tmp/claude-1000")
    if len(r.stdout) > 1500:
        out.write_text(r.stdout)
    return pid, "ok" if out.exists() else "short"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--doc", default=str(D / "build/document.md")); ap.add_argument("--round", default="final")
    a = ap.parse_args()
    with cf.ThreadPoolExecutor(5) as ex:
        for r in ex.map(lambda p: run(p, a.doc, a.round), P):
            print(*r, flush=True)
