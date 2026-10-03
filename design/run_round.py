#!/usr/bin/env python3
"""Run one round of the twelve-designer protocol exercise in parallel.

    python3 design/run_round.py 1                 # independent proposals
    python3 design/run_round.py 2                 # cross-review (needs round 1 outputs)
    python3 design/run_round.py 3 --prompt-dir D  # amendments and votes (prompts prepared in D)
    options: --only ROLE_ID[,ROLE_ID]  --timeout SECONDS

Vendors (all read-only):
  grok   grok-4.7, reasoning xhigh, write tools removed, no web
  codex  gpt-6.1-sol, reasoning high, read-only sandbox
  claude claude-opus-5-5, effort high, Read/Grep/Glob plus a few read-only shell commands
Outputs: design/rounds/r<N>/<role>.md, logs in the same folder. Resume-safe: finished roles are skipped.
"""
import argparse
import concurrent.futures as cf
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "design"
ROLES = json.loads((D / "roles.json").read_text())
WORK = Path("/tmp/claude-1000/design-work")
# Grok cannot be sandboxed on this machine, so it is read-only by construction: no shell, no writers.
GROK_DENY = ("write,search_replace,run_terminal_command,spawn_subagent,image_gen,image_edit,"
             "image_to_video,reference_to_video,x_user_search,x_semantic_search,x_keyword_search,x_thread_fetch,"
             "web_search,open_page,open_page_with_find,web_fetch")
CLAUDE_TOOLS = ["Read", "Grep", "Glob", "Bash(graphify:*)", "Bash(ls:*)", "Bash(wc:*)", "Bash(head:*)",
                "Bash(pdftotext:*)", "Bash(cat:*)", "Bash(sed:*)"]


def common_header(role):
    return f"""You are one of twelve designers of the Midnight Private Events protocol. Your role: **{role['title']}** (you lead decisions {', '.join(role['leads'])}, but you answer all ten).

Role lens: {role['lens']}
Your lean: {role['lean']}

Read /home/charl/privateEvents/design/CHARTER.md first and follow it exactly. It defines the ten decisions, the evidence rules and the output format.

Evidence you must use (all local, read-only; you have no web access and must not try to write or modify any file):
- Midnight read-out: /home/charl/privateEvents/notes/midnight-network-stack.md (then open the code it cites under /home/charl/midnight/ to check what you rely on)
- Knowledge graph: /home/charl/privateEvents/graphify-out/GRAPH_REPORT.md and graph.json, start with /home/charl/privateEvents/design/evidence/graph-overview.md (the 90 largest topic communities), then search the flat digest /home/charl/privateEvents/design/evidence/graph-digest.md and the paper index /home/charl/privateEvents/design/evidence/papers.tsv with grep. If you have a shell: graphify query "your question" --graph /home/charl/privateEvents/graphify-out/graph.json
- Literature catalog: /home/charl/privateEvents/catalog/*.jsonl (fields slug, title, note, bitmessage_link, pdf_path); full texts in /home/charl/privateEvents/pdfs/; plain text of every paper is in /home/charl/privateEvents/graph/text/<file-stem>.txt (the stem is the pdf_path file name without extension; use this if you cannot read PDFs); slice digests in /home/charl/privateEvents/notes/*.md
- Project start: /home/charl/privateEvents/design/evidence/bitmessage-guide.md and /home/charl/privateEvents/reviews/bitmessage-technical-guide-review.md

Cite catalog slugs and repo/path:line. Label unsupported statements assumption, inference or unknown. Do not invent sources, numbers or paths.
"""


def prompt_round1(role, _):
    return common_header(role) + """
ROUND 1. Write your independent proposal now. You have not seen anyone else's. Cover D1 to D10, then end with the decision table. Maximum 6,000 words. Your entire final message is the proposal (Markdown); do not describe your process.
"""


def assignments():
    """Each designer reviews four proposals: two from each other vendor, so every proposal gets four reviews."""
    by_v = {}
    for r in ROLES:
        by_v.setdefault(r["vendor"], []).append(r["id"])
    out = {}
    vendors = list(by_v)
    for v, ids in by_v.items():
        for k, rid in enumerate(ids):
            t = []
            for w in vendors:
                if w == v:
                    continue
                t += [by_v[w][k % 4], by_v[w][(k + 1) % 4]]
            out[rid] = t
    return out


def prompt_round2(role, _):
    targets = assignments()[role["id"]]
    paths = "\n".join(f"- {t}: /home/charl/privateEvents/design/rounds/r1/{t}.md" for t in targets)
    return common_header(role) + f"""
ROUND 2, cross-review. Read these four Round 1 proposals written by other designers (you have not seen them before):
{paths}

Also read your own Round 1 proposal: /home/charl/privateEvents/design/rounds/r1/{role['id']}.md

For each of D1 to D10, in order: (a) list the positions of the four reviewed proposals in one line each; (b) check their evidence: open the cited papers and code and say whether the citation supports the claim; (c) state your vote on the position you consider best (name the proposal), or your own alternative if none works; (d) state the single strongest objection to the leading position. Finish with: the three decisions on which the group is most likely to disagree, and the one fact that, if checked, would settle the most disagreement. Maximum 4,500 words. Your entire final message is the review (Markdown).
"""


def ears_agents():
    return json.loads((D / "ears" / "agents.json").read_text())


def prompt_ears(role, _):
    r1 = "\n".join(f"- {r['id']}: /home/charl/privateEvents/design/rounds/r1/{r['id']}.md" for r in ROLES)
    r2 = "\n".join(f"- {r['id']}: /home/charl/privateEvents/design/rounds/r2/{r['id']}.md" for r in ROLES)
    return f"""You are one of twelve EARS requirements authors for the Midnight Private Events (MPE) bus. Your area is **{role['area']}: {role['title']}** (requirement IDs MPE-{role['area']}-NNN). Decisions in your area: {', '.join(role['decisions'])}.

Area focus: {role['focus']}

Read /home/charl/privateEvents/design/ears/BRIEF.md first and follow it exactly: it defines the EARS patterns, the glossary, the requirement record format, the quality rules and the output structure.

Inputs (all local, read-only; no web access; do not write or modify any file):
- Charter: /home/charl/privateEvents/design/CHARTER.md
- Decision matrix of all twelve proposals: /home/charl/privateEvents/design/rounds/r1_positions.json (start here)
- Round 1 proposals (read, in full, the sections for your decisions in every one):
{r1}
- Round 2 cross-reviews (objections, citation checks and votes; s3-red-team's review is incomplete, so rely on its Round 1 proposal):
{r2}
- Midnight code read-out: /home/charl/privateEvents/notes/midnight-network-stack.md (verify what you rely on in /home/charl/midnight/)
- libp2p source (GossipSub v1.1 behaviour, mesh parameters, validation, scoring): /home/charl/libp2p/rust-libp2p, /home/charl/libp2p/specs, /home/charl/libp2p/go-libp2p-pubsub
- Evidence: /home/charl/privateEvents/design/evidence/papers.tsv (paper index with text paths), graph-overview.md, graph-digest.md

Write the complete area file now, in the structure the brief requires. Maximum 7,000 words. Your entire final message is the file content (Markdown); do not describe your process.
"""


BUILDERS = {1: prompt_round1, 2: prompt_round2, 5: prompt_ears}


def command(role, prompt, outfile):
    v = role["vendor"]
    if v == "grok":
        return (["grok", "--model", "grok-4.7", "--reasoning-effort", "xhigh", "--disable-web-search",
                 "--disallowed-tools", GROK_DENY, "--always-approve", "--cwd", str(WORK / role["id"]), "-p", prompt],
                None, "stdout")
    if v == "codex":
        return (["codex", "exec", "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="high"', "--ephemeral",
                 "--ignore-user-config", "-s", "read-only", "--skip-git-repo-check", "-C", str(WORK / role["id"]),
                 "-o", str(outfile), prompt], None, "file")
    return (["claude", "-p", "--model", "claude-opus-5-5", "--effort", "high", "--no-session-persistence",
             "--allowedTools", *CLAUDE_TOOLS, "--add-dir", "/home/charl/privateEvents", "--add-dir",
             "/home/charl/midnight"], prompt, "stdout")


def run_role(role, rnd, prompt, timeout):
    out = D / "rounds" / f"r{rnd}" / f"{role['id']}.md"
    if out.exists() and out.stat().st_size > 2000:
        return role["id"], "skip", 0
    (WORK / role["id"]).mkdir(parents=True, exist_ok=True)
    cmd, stdin, mode = command(role, prompt, out)
    t0 = time.time()
    log = out.with_suffix(".log")
    try:
        res = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=timeout,
                             cwd=str(WORK / role["id"]))
        log.write_text(f"rc={res.returncode}\n--- stderr ---\n{res.stderr[-4000:]}\n")
        if mode == "stdout":
            out.write_text(res.stdout)
        status = "ok" if out.exists() and out.stat().st_size > 2000 else "short"
    except subprocess.TimeoutExpired:
        status = "timeout"
    return role["id"], status, round(time.time() - t0)


GUARD = str(D / "guard.sh")
MIDNIGHT_CHECK = ["midnight-node", "midnight-ledger", "midnight-js", "midnight-wallet", "midnight-indexer",
                  "midnight-docs", "midnight-architecture", "compact", "minokawa-compact", "midnight-zk",
                  "midnight-improvement-proposals"]


def guard(cmd):
    return subprocess.run([GUARD, cmd], capture_output=True, text=True).stdout.strip()


def midnight_state():
    out = {}
    for r in MIDNIGHT_CHECK:
        g = Path("/home/charl/midnight") / r
        if (g / ".git").exists() or (g / ".git").is_file():
            h = subprocess.run(["git", "-C", str(g), "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True).stdout
            out[r] = (subprocess.run(["git", "-C", str(g), "rev-parse", "HEAD"], capture_output=True,
                                     text=True).stdout.strip(), h)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("round", type=int)
    ap.add_argument("--only", default="")
    ap.add_argument("--timeout", type=int, default=3000)
    ap.add_argument("--prompt-dir", default="")
    a = ap.parse_args()
    (D / "rounds" / f"r{a.round}").mkdir(parents=True, exist_ok=True)
    pool = ears_agents() if a.round == 5 else ROLES
    roles = [r for r in pool if not a.only or r["id"] in a.only.split(",")]
    jobs = []
    for r in roles:
        if a.prompt_dir:
            p = (Path(a.prompt_dir) / f"{r['id']}.txt").read_text()
        else:
            p = BUILDERS[a.round](r, None)
        jobs.append((r, p))
    print(f"round {a.round}: {len(jobs)} designers", flush=True)
    before = guard("snapshot")
    mid_before = midnight_state()
    print("evidence locked:", guard("lock"), "| snapshot", before.replace("\n", " files:"), flush=True)
    try:
        with cf.ThreadPoolExecutor(max_workers=len(jobs)) as ex:
            futs = [ex.submit(run_role, r, a.round, p, a.timeout) for r, p in jobs]
            for f in cf.as_completed(futs):
                print(*f.result(), flush=True)
    finally:
        print("evidence", guard("unlock"), flush=True)
        after = guard("snapshot")
        print("evidence unchanged" if after == before else f"!! EVIDENCE CHANGED: {before!r} -> {after!r}", flush=True)
        mid_after = midnight_state()
        for k in mid_before:
            if mid_before[k] != mid_after.get(k):
                print(f"!! midnight repo changed: {k}", flush=True)


if __name__ == "__main__":
    main()
