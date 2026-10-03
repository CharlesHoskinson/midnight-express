#!/usr/bin/env python3
"""Audit the assembled design document: four technical reviewers (GPT-6.1 Sol, high) and four reader agents (Grok 4.7, xhigh).

    python3 run_audit.py [--round 1] [--only T1,R2]

Inputs: build/document.md (full) and build/document-body.md (without Appendix A, for readers).
Outputs: ../audit/round<N>/<ID>.md (the reviewer's final message). Resume-safe. Grok runs read-only under design/guard.sh.
"""
import argparse, concurrent.futures as cf, subprocess, time
from pathlib import Path

D = Path(__file__).resolve().parents[1]
ROOT = D.parents[1]
GUARD = str(ROOT / "design" / "guard.sh")

COMMON_REFS = f"""Reference material (read-only, local; do not write or modify any file; no web access):
- The Foundation's proposals: /home/charl/midnight/midnight-improvement-proposals (mips/, mps/, index.md); the alignment study {D}/align/FOUNDATION_DEFINITIONS.md is the reference for the Foundation's definitions of events and private events, and the document must agree with it.
- The GossipSub specifications and code: /home/charl/libp2p/specs/pubsub, /home/charl/libp2p/rust-libp2p/protocols/gossipsub, /home/charl/libp2p/go-libp2p-pubsub; the study {D}/align/GOSSIPSUB_COMPLIANCE.md lists what the design must respect.
- Midnight code: /home/charl/midnight; notes {ROOT}/notes/midnight-network-stack.md.
- The conformance checklist for the proposals: {D}/MIP_MPS_CHECKLIST.md.
- Facts and names that must agree across chapters: {D}/FACTS.md. Requirements register: {D}/build/ears-consolidated.json.
- Literature: {ROOT}/design/evidence/papers.tsv (slug, text_path)."""

TECH = """You are a technical reviewer of a design document, "Midnight Express: Private Events for Midnight", read in full from {doc}. It ends with a Midnight Improvement Proposal and (in Chapter 4) a Midnight Problem Statement. You are reviewer {id}; your scope is: {scope}

Be adversarial and specific. For every finding give: severity (blocker, major, minor), the location (chapter, section, and a quoted phrase), what is wrong, the evidence you checked (file and line in the code, specification section, or paper), and the exact change you recommend. Check claims against the sources instead of trusting the text. Also check that: (a) the document uses the Foundation's understanding and definitions of events and private events and flags every divergence; (b) it respects the GossipSub specification and the rust-libp2p behaviour; (c) the design, the experiments and the results meet the needs the proposal and the problem statement state, and the acceptance criteria in the proposal map to experiments with thresholds; (d) the proposal and the problem statement follow the Foundation's templates and process (see the checklist). Rank findings most severe first. End with a short list of things you verified and found correct. Do not describe your own process.

{refs}"""

READER = """You are a reader agent for a design document, "Midnight Express: Private Events for Midnight", in {doc}. You are reader {id}: {persona}

Read the document in order. Then write, as your final message: (1) the questions you still have after reading, each with the place where you expected the answer (at least twelve, most important first); (2) the places where the prose is unclear, padded, repetitive, jargon-heavy, or where a term is used before it is defined, each with a quoted phrase and a suggested rewrite; (3) the claims you do not believe or could not follow, with why; (4) a verdict per chapter (keep, tighten, rewrite) with one sentence of reason; (5) the three changes that would most improve the document for your kind of reader. Be direct. Do not describe your own process. The document must read as a standalone piece of work: also report any trace of how it was made (mentions of drafts, panels, reviewers, agents, rounds, scoring, placeholders or editor notes) with the quoted text.

{refs}"""

JOBS = [
    {"id": "T1", "vendor": "codex", "scope": "protocol and cryptography: Chapter 4 definitions and properties, the Envelope format, Tags, keys, admission, the leakage table, threats and defences; check every cryptographic and privacy claim and the non-claims.", "kind": "tech"},
    {"id": "T2", "vendor": "codex", "scope": "GossipSub and performance: the overlay design, topics and Shards, the message identifier, scoring, mesh parameters, IDONTWANT, restart and churn handling, bandwidth and storage arithmetic, and the experiments and results in Chapters 8 to 11; recompute the numbers and check against the specification and rust-libp2p source.", "kind": "tech"},
    {"id": "T3", "vendor": "codex", "scope": "Midnight facts and the proposals: Chapters 2 and 3, the ledger and Compact facts, the Registry and anchoring, the fallback through emitted events, fees, and the proposal and problem statement against the MIP-0001 process and templates and against MIPs 2, 19 and MPS-0005 and 0007; every fact about Midnight must be checkable in the code or the Foundation's documents.", "kind": "tech"},
    {"id": "T4", "vendor": "codex", "scope": "requirements and traceability: Chapter 7, Appendix A and the acceptance criteria; counts, identifiers and cross-references; whether every requirement in the proposal exists in Appendix A and is covered by an experiment or marked as not tested; contradictions between chapters, and between FACTS.md and the text; the reading list entries against the sources.", "kind": "tech"},
    {"id": "R1", "vendor": "grok", "persona": "a Midnight protocol engineer who has built Compact contracts and wants to know what to build against and what changes for them. You know blockchains, not mix networks.", "kind": "reader"},
    {"id": "R2", "vendor": "grok", "persona": "a distributed-systems researcher who knows GossipSub and libp2p well and is sceptical of the experimental method and of claims drawn from an in-process simulator.", "kind": "reader"},
    {"id": "R3", "vendor": "grok", "persona": "a privacy and cryptography researcher who knows anonymity literature (mixnets, PIR, Bitmessage, anonymity of gossip) and tests every privacy claim against its stated adversary.", "kind": "reader"},
    {"id": "R4", "vendor": "grok", "persona": "a decision-maker at a foundation who funds work and will not read Appendix A: you want to know what is being proposed, what it costs, what is known, what is not, and what the Foundation should do next.", "kind": "reader"},
]


def run(job, rnd, doc_full, doc_body):
    out = D / "audit" / f"round{rnd}" / f"{job['id']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 1500:
        return job["id"], "skip", 0
    refs = COMMON_REFS
    if job["kind"] == "tech":
        prompt = TECH.format(doc=doc_full, id=job["id"], scope=job["scope"], refs=refs)
    else:
        prompt = READER.format(doc=doc_body, id=job["id"], persona=job["persona"], refs=refs)
    work = Path("/tmp/claude-1000/audit-work") / job["id"]
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    try:
        if job["vendor"] == "codex":
            subprocess.run(["codex", "exec", "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="high"', "--ephemeral", "--ignore-user-config",
                            "-s", "read-only", "--skip-git-repo-check", "-C", str(work), "-o", str(out), prompt],
                           capture_output=True, text=True, timeout=4800, stdin=subprocess.DEVNULL)
        else:
            r = subprocess.run(["grok", "--model", "grok-4.7", "--reasoning-effort", "xhigh", "--disable-web-search", "--always-approve",
                                "--cwd", str(work), "-p", prompt], capture_output=True, text=True, timeout=4800, stdin=subprocess.DEVNULL)
            if len(r.stdout) > 1500:
                out.write_text(r.stdout)
        st = "ok" if out.exists() and out.stat().st_size > 1500 else "short"
    except subprocess.TimeoutExpired:
        st = "timeout"
    return job["id"], st, round(time.time() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    jobs = [j for j in JOBS if not a.only or j["id"] in a.only.split(",")]
    doc_full, doc_body = D / "build" / "document.md", D / "build" / "document-body.md"
    subprocess.run([GUARD, "lock"], capture_output=True)
    try:
        with cf.ThreadPoolExecutor(len(jobs)) as ex:
            for res in ex.map(lambda j: run(j, a.round, doc_full, doc_body), jobs):
                print(*res, flush=True)
    finally:
        subprocess.run([GUARD, "unlock"], capture_output=True)


if __name__ == "__main__":
    main()
