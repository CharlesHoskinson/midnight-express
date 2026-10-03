#!/usr/bin/env python3
"""Run document jobs for the design document, one writer per vendor lane, chapters sequential per writer.

    python3 run_docs.py draft            # four Opus 5.5 (medium) writers draft chapters + reading-list sections
    python3 run_docs.py draft --only W1
Outputs to ../draft/<chapter>.md ; the writer's final message is the file content. Resume-safe.
"""
import argparse, concurrent.futures as cf, json, subprocess, time
from pathlib import Path
D = Path(__file__).resolve().parents[1]
ROOT = D.parents[1]
import sys
PHASE = sys.argv[1] if len(sys.argv) > 1 else "draft"
jobs = json.loads((D / "build" / {"draft": "jobs.json", "mip": "mip_jobs.json", "align": "align_jobs.json"}[PHASE]).read_text())
STYLE = (D / "STYLE.md").read_text(); FACTS = (D / "FACTS.md").read_text(); OUTLINE = (D / "OUTLINE.md").read_text(); FIG = (D / "FIGURES.md").read_text()

def header(job):
    extra = f" Also read {D}/MIP_BRIEF.md (the brief for the Midnight Improvement Proposal) and the Foundation's template and examples in /home/charl/midnight/midnight-improvement-proposals (mips/, mps/)." if job["writer"][0] in "MS" else ""
    return f"""You are writing part of a design document, "Midnight Express: Private Events for Midnight (Requirements, Options and an Experimental Design on GossipSub)". Writer {job['writer']}.{extra}

Read these three files first and obey them exactly: {D}/STYLE.md, {D}/OUTLINE.md, {D}/FACTS.md, and {D}/FIGURES.md. They define the voice, the chapter plan, the shared numbers and names, and the figures. If a source you read disagrees with FACTS.md, FACTS.md wins unless you can show from the code or the cited work that it is wrong, in which case say so in a short note after the chapter, under a line "NOTE TO EDITOR:".

All evidence is local and read-only (you cannot write files and must not try): {ROOT}. Literature: {ROOT}/design/evidence/papers.tsv (slug is the citation key; text_path is the plain text of each work) and {ROOT}/graph/text/. Midnight and libp2p code: /home/charl/midnight and /home/charl/libp2p. Requirements and decisions: {ROOT}/design/ears/RECONCILE.md, {ROOT}/design/rounds/r5/, {ROOT}/design/ears/POC_CORE.md. Prototype and results: {ROOT}/design/PROTOTYPE.md, {ROOT}/design/LEARNINGS.md, {ROOT}/design/prototype/, {ROOT}/prototype/, and the three implementations' RESULTS.md under /home/charl/privateEvents-build/{{a,b,c}}/. Midnight code facts: {ROOT}/notes/midnight-network-stack.md. The earlier design proposals and reviews: {ROOT}/design/rounds/r1/ and r2/ (use them for substance; never mention them). Brand and public context about Midnight City: {D}/brand/midnight-city/pages/.

Check every factual claim you write against the cited work or code; open the paper text rather than relying on a title. Cite with pandoc keys that exist in {D}/build/bibkeys.txt.
"""

def run_job(job):
    out = D / "draft" / job["file"]
    if out.exists() and out.stat().st_size > 800:
        return job["id"], "skip", 0
    prompt = (job["task"] if job.get("raw") else header(job) + "\n" + job["task"]) + "\n\nYour entire final message is the Markdown of this file and nothing else (no preface, no description of your process)."
    t0 = time.time()
    if job.get("vendor") == "codex":
        cmd = ["codex", "exec", "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="high"', "--ephemeral", "--ignore-user-config", "-s", "read-only",
               "--skip-git-repo-check", "-C", "/tmp/claude-1000/doc-work", "-o", str(out), prompt]
        Path("/tmp/claude-1000/doc-work").mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=3600, stdin=subprocess.DEVNULL)
            st = "ok" if out.exists() and out.stat().st_size > 800 else "short"
        except subprocess.TimeoutExpired:
            st = "timeout"
        return job["id"], st, round(time.time() - t0)
    cmd = ["claude", "-p", "--model", "claude-opus-5-5", "--effort", job.get("effort", "medium"), "--no-session-persistence",
           "--allowedTools", "Read", "Grep", "Glob", "Bash(ls:*)", "Bash(wc:*)", "Bash(head:*)", "Bash(pdftotext:*)",
           "--add-dir", str(ROOT), "--add-dir", "/home/charl/midnight", "--add-dir", "/home/charl/libp2p", "--add-dir", "/home/charl/privateEvents-build", "--add-dir", "/home/charl/midnight/midnight-improvement-proposals"]
    try:
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=3000)
        if len(r.stdout) > 800:
            out.write_text(r.stdout)
        st = "ok" if out.exists() else "short"
    except subprocess.TimeoutExpired:
        st = "timeout"
    return job["id"], st, round(time.time() - t0)

def writer(wid):
    for job in [j for j in jobs if j["writer"] == wid]:
        print(*run_job(job), flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("phase"); ap.add_argument("--only", default="")
    a = ap.parse_args()
    (D / "draft").mkdir(exist_ok=True)
    ws = sorted({j["writer"] for j in jobs if not a.only or j["writer"] in a.only.split(",")})
    with cf.ThreadPoolExecutor(len(ws)) as ex:
        list(ex.map(writer, ws))

if __name__ == "__main__":
    main()
