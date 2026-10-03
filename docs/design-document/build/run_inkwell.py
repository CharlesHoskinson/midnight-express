#!/usr/bin/env python3
"""Inkwell pass over every prose file: Zinsser draft, Gottlieb edit, apply, Le Guin revise, target-reader gate (max 3 fix cycles).

    python3 run_inkwell.py [--only 02-midnight.md,M1.md] [--workers 8]

Input: ../draft-r2/<file> (falls back to ../draft/<file>). Output: ../draft-r3/<file>; per-file notes in ../inkwell-notes/<file>.json.
Profile: the live `grothendieck` profile (diagnostic mode) with its English guide. Mechanical invariants (citations, numbers, identifiers, headings,
table rows, figure markers, footnotes) are compared before and after every rewriting stage; losses are sent back for repair.
Length: the finished file must be 10 to 20 percent longer than its input (5 to 20 for the proposal files, whose normative text does not grow).
"""
import argparse, concurrent.futures as cf, collections, json, re, subprocess, sys, time
from pathlib import Path

D = Path(__file__).resolve().parents[1]
ROOT = D.parents[1]
INK = Path("/home/charl/inkwell")
IN2, IN1, OUT, NOTES = D / "draft-r2", D / "draft", D / "draft-r3", D / "inkwell-notes"
FILES = ["01-introduction.md", "02-midnight.md", "03-need.md", "04-definition.md", "04b-mps.md", "05-prior-art.md", "06-options.md", "07-requirements.md",
         "08-reference-system.md", "09-experiments.md", "10-results.md", "11-roadmap.md", "B1-reading-W1.md", "B2-reading-W2.md", "B3-reading-W3.md",
         "B4-reading-W4.md", "M1.md", "M2.md", "M3.md", "M4.md", "M5.md", "M6.md"]
PROFILE = INK / "skills/voiceprint/profiles/grothendieck.md"
SIDECAR = INK / "skills/voiceprint/profiles/grothendieck.metrics.json"
GUIDE = INK / "skills/voiceprint/references/grothendieck-english.md"
SCORER = INK / "skills/voiceprint/scripts/conformance.py"
AUDIENCE = ("An engineer or protocol designer who builds on blockchains or distributed systems and reads this document from the front. They have not met "
            "GossipSub, the anonymity literature, Compact or Midnight's internals, and they have no access to the authors. They read this chapter in order, after the ones before it.")
MIP_AUDIENCE = ("A Midnight Improvement Proposal editor or reviewer and an implementer who will build to this proposal. They know blockchains, have read MIP-0001 and the other proposals, "
                "and have not read the rest of this document except where this text points to it.")


def persona(name):
    t = (INK / "agents" / f"{name}.md").read_text()
    return re.sub(r"^---.*?---\n", "", t, count=1, flags=re.S)


def claude(prompt, effort="high", tools=("Read", "Grep", "Glob"), adddirs=(), timeout=3300, cwd="/tmp/claude-1000"):
    cmd = ["claude", "-p", "--model", "claude-opus-5-5", "--effort", effort, "--no-session-persistence"]
    if tools:
        cmd += ["--allowedTools", *tools]
    for a in adddirs:
        cmd += ["--add-dir", str(a)]
    Path(cwd).mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=cwd)
            if len(r.stdout.strip()) > 300:
                return r.stdout.strip() + "\n"
        except subprocess.TimeoutExpired:
            pass
        time.sleep(20)
    return ""


# ---- mechanical invariants -------------------------------------------------
def inv(t):
    cites = set()
    for m in re.findall(r"\[@([^\]]+)\]", t):
        cites |= set(re.findall(r"[A-Za-z0-9_][A-Za-z0-9_:.\-]*", m.replace("@", " ")))
    return {
        "cites": cites,
        "figs": set(re.findall(r"\{\{fig:[0-9]+-[0-9]+\}\}", t)),
        "ids": set(re.findall(r"\b(?:MPE-[A-Z]{3}-\d+[a-z]?|DEC-\d+|P-[A-Z]{3}-\d+|MIP-(?:\d{4}|xxxx)|MPS-(?:\d{4}|xxxx)|CoIP-\d{4})\b", t)),
        "nums": collections.Counter(re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])", t)),
        "headings": [re.sub(r"\s*\{[^}]*\}\s*$", "", h).strip() for h in re.findall(r"^#{1,6} .*$", t, flags=re.M)],
        "rows": sum(1 for l in t.splitlines() if l.startswith("|")),
        "notes": t.count("^["),
        "refs": [l.split("::")[0].strip() for l in t.splitlines() if l.startswith("@") and "::" in l],
        "musts": collections.Counter(re.findall(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|MAY)\b", t)),
    }


def loss(a, b):
    out = []
    for k in ("cites", "figs", "ids"):
        miss = sorted(a[k] - b[k])
        if miss:
            out.append(f"{k} missing: {miss[:40]}")
    nm = [n for n, c in a["nums"].items() if b["nums"][n] < c]
    if nm:
        out.append(f"numbers missing or reduced: {nm[:60]}")
    if a["headings"] != b["headings"]:
        out.append(f"headings changed: before {[h for h in a['headings'] if h not in b['headings']][:10]}, after {[h for h in b['headings'] if h not in a['headings']][:10]}")
    if b["rows"] < a["rows"]:
        out.append(f"table rows {a['rows']} -> {b['rows']}")
    if b["notes"] < a["notes"]:
        out.append(f"footnotes {a['notes']} -> {b['notes']}")
    if a["refs"] and a["refs"] != b["refs"]:
        out.append("reading-list entry lines (the `@slug ::` lines) changed or reordered")
    for k, c in a["musts"].items():
        if b["musts"][k] < c:
            out.append(f"normative keyword {k}: {c} -> {b['musts'][k]}")
    return out


def words(t):
    return len(re.sub(r"[|#*`]", " ", t).split())


# ---- stages ----------------------------------------------------------------
COMMON = f"""Voice: the live `grothendieck` profile of Inkwell, used as an adaptation for English scientific exposition. Read {PROFILE}, its sidecar {SIDECAR} and the guide {GUIDE}. Follow its structural habits (a motivated setting before a definition; a definition followed by a consequence or example that tests it; the common obligation stated before the cases; reductions shown; theorem, result proved elsewhere, conditional result, conjecture, heuristic and goal kept apart; return from the framework to a concrete instance; close a section with the question that remains). Its measured rates are observations, not targets. Do not import algebraic geometry or any subject vocabulary of the historical author, do not mention him or any style, and do not quote his texts.

House rules that still bind: {D}/STYLE.md (including the Vocabulary section; no em dashes; the banned filler list; citation keys [@slug]; footnote form), {D}/FACTS.md (wins over the text on any number or name) and {D}/FIGURES.md. The text must read as original standalone work: no mention of drafts, reviewers, passes, studies, agents or this process; no placeholders.

If the file {D}/WRITING_LESSONS.md exists, read it and obey its sections 1 to 3 (patterns, headings, paragraph shape) as hard rules; headings of the Foundation's proposal template are exempt.

Scientific integrity outranks voice. Preserve every definition, number, unit, requirement identifier, citation, figure marker, heading, table, footnote, normative keyword (MUST, SHOULD, MAY and their negatives), quantifier order, assumption, caveat and the status of each claim (measured, derived, assumed, proposed, unknown). Do not turn an obligation into a result or a hypothesis into a fact. Do not drop a qualification as a hedge. If something looks technically wrong, leave it and list it under a final line `TECHNICAL NOTE:` after the file (the harness removes it). Evidence for any new claim is local and read-only: {ROOT} (literature in design/evidence/papers.tsv with text paths; prototype and results; align/ for the Foundation and GossipSub facts), /home/charl/midnight, /home/charl/libp2p. Check a fact before you add it."""

INTRO = """Introductory lens, and length. The reader meets these ideas for the first time. Add roughly 15 percent more prose (between 10 and 20 percent of the words of the file you were given; the figure counts words of text, tables included in the base) by explaining, in the places where understanding would otherwise fail: what a technical term is in plain words at its first use, why the mechanism exists, what problem it removes, a small concrete example worked through (one message, one relay, one block, one subscriber) before the general statement, why a requirement or parameter has the value it has, and what each section lets the reader do next. Put the added prose where it is needed, not in one block. Do not add recaps, signposting, summaries, cheering, generic background, or anything the argument does not use. Added prose must be true and checkable; derive any new number and show the arithmetic."""
MIP_INTRO = """Length. This file belongs to a Midnight Improvement Proposal. Its normative text (anything stating what an implementation MUST, SHOULD or MAY do, any table of values, format or interface) keeps its exact content and does not grow. Add 5 to 15 percent more words, only in the non-normative parts (Motivation, Rationale, Background, explanatory paragraphs), explaining concepts for a reader meeting them for the first time, with an example where it helps. Keep the Foundation's template headings exactly."""


def kind(f):
    return "mip" if f.startswith("M") and f[1].isdigit() or f == "04b-mps.md" else ("reading" if f.startswith("B") else "chapter")


def special(f):
    k = kind(f)
    if k == "reading":
        return "This is a reading-list section. Keep every line that starts with `@slug ::` as the first part of its entry and in the same order; rewrite only the annotation text after `::`, in the same line (an annotation may run to several sentences on that line). Keep the `## ` theme headings. Annotations say what the work is, what it shows and how it bears on the design; add, where the work is technical, a plain sentence on what the reader needs to know to approach it."
    if k == "mip":
        return MIP_INTRO + (" This is the formal problem statement; keep the Foundation's MPS template headings." if f == "04b-mps.md" else "")
    return INTRO


def stage_draft(f, text, p):
    prompt = f"""You are the `zinsser-writer` of Inkwell's writing pipeline. Persona (follow it): {INK}/agents/zinsser-writer.md.

{COMMON}

{special(f)}

Task: rewrite the file below in the selected voice and add the introductory prose. Keep its structure and everything protected above. File: {f}. Audience: {AUDIENCE if kind(f) != 'mip' else MIP_AUDIENCE}

THE FILE:
<<<
{text}
>>>

Your entire final message is the complete Markdown of the revised file and nothing else."""
    return claude(prompt, adddirs=(ROOT, INK, "/home/charl/midnight", "/home/charl/libp2p"))


def stage_edit(f, text):
    prompt = f"""You are the `gottlieb-editor` of Inkwell's writing pipeline. Persona (follow it): {INK}/agents/gottlieb-editor.md. Voice profile in force (read it, with its guide): {PROFILE} and {GUIDE}. House rules: {D}/STYLE.md. Run the five-family tell audit. Scientific integrity outranks everything: report suspected technical defects separately and never as a cut. Do not suggest removing numbers, identifiers, citations, tables or necessary qualifications. The draft has been lengthened on purpose for a reader new to the subject: do not call that lengthening a fault; cut only what does not serve the argument or the beginner's understanding, and name where an explanation is still missing. Cite by paragraph number. Return the review in your format.

DRAFT ({f}):
<<<
{text}
>>>"""
    return claude(prompt, tools=("Read", "Grep", "Glob"), adddirs=(INK, ROOT))


def stage_apply(f, text, findings, why="Apply the editor's findings"):
    prompt = f"""You are the `zinsser-writer` of Inkwell's writing pipeline applying an edit. {COMMON}

{why}: cut what the findings say to cut, fix what they name, keep what they say works. Where a finding asks for a cut that would remove a protected item, keep the item and fix the sentence. Keep the file's length within the range required (the file must stay 10 to 20 percent above the base word count of {{BASE}} words for ordinary chapters, 5 to 15 percent for proposal files: the target for this file is {{LOW}} to {{HIGH}} words). Do not mention the findings.

FINDINGS:
<<<
{findings}
>>>

CURRENT FILE ({f}):
<<<
{text}
>>>

Your entire final message is the complete Markdown of the revised file and nothing else."""
    return prompt


def stage_cadence(f, text):
    prompt = f"""You are the `leguin-reviser` of Inkwell's writing pipeline. Persona (follow it): {INK}/agents/leguin-reviser.md. Voice profile in force: {PROFILE} and {GUIDE}. {COMMON}

Revise for rhythm, sound and momentum without changing the claim inventory or removing protected items. Do not shorten the file by more than 2 percent. File: {f}.

DRAFT:
<<<
{text}
>>>

Your entire final message is the complete Markdown of the revised file and nothing else."""
    return claude(prompt, adddirs=(INK, ROOT))


def stage_read(f, text):
    body = persona("target-reader")
    aud = MIP_AUDIENCE if kind(f) == "mip" else AUDIENCE
    prompt = f"""{body}

AUDIENCE DESCRIPTION:
{aud}

DRAFT ({f}):
<<<
{text}
>>>"""
    return claude(prompt, tools=(), effort="medium", cwd="/tmp/claude-1000/empty")


def job(f, force=False):
    out, note = OUT / f, NOTES / (f + ".json")
    if out.exists() and out.stat().st_size > 800 and not force:
        return f, "skip"
    src = (IN2 / f) if (IN2 / f).exists() else (IN1 / f)
    base = src.read_text()
    base = re.split(r"\n+NOTE TO EDITOR:", base)[0]
    a = inv(base)
    nw = words(base)
    lo, hi = (nw * (1.06 if kind(f) == "mip" else 1.11), nw * (1.19 if kind(f) == "mip" else 1.19))
    lo, hi = int(lo), int(hi)
    log = {"file": f, "base_words": nw, "target": [lo, hi], "stages": []}

    def repair(t, label):
        for _ in range(2):
            problems = loss(a, inv(t))
            w = words(t)
            if w < lo * 0.97:
                problems.append(f"too short: {w} words, need {lo} to {hi}; add explanatory prose for a first-time reader where understanding needs it")
            if w > hi * 1.04:
                problems.append(f"too long: {w} words, need {lo} to {hi}; cut what does not serve the argument or the beginner")
            if not problems:
                return t
            log["stages"].append({label + "-repair": problems})
            p = stage_apply(f, t, "\n".join(problems), "Repair these defects against the original (the protected items below are in the BASE FILE; restore any that are missing, and fix the length)").replace("{BASE}", str(nw)).replace("{LOW}", str(lo)).replace("{HIGH}", str(hi))
            p = p.replace("CURRENT FILE", "BASE FILE (what the protected items must match):\n<<<\n" + base + "\n>>>\n\nCURRENT FILE")
            r = claude(p, adddirs=(ROOT, INK))
            if r:
                t = r
        return t

    t = stage_draft(f, base, None)
    if not t:
        return f, "draft failed"
    t = repair(t, "draft")
    findings = stage_edit(f, t)
    log["stages"].append({"edit": findings[:6000]})
    if findings:
        p = stage_apply(f, t, findings).replace("{BASE}", str(nw)).replace("{LOW}", str(lo)).replace("{HIGH}", str(hi))
        r = claude(p, adddirs=(ROOT, INK))
        if r:
            t = repair(r, "apply")
    r = stage_cadence(f, t)
    if r:
        t = repair(r, "cadence")
    for cycle in range(3):
        verdict = stage_read(f, t)
        log["stages"].append({f"read{cycle}": verdict[:4000]})
        if "Verdict: CLEAR" in verdict or "Verdict:CLEAR" in verdict or not verdict:
            break
        p = stage_apply(f, t, verdict, "Fix the reader's flags by changing what is communicated (order, grounding, a missing step), never by flattening the voice; each flag is a place where a first-time reader lost the thread").replace("{BASE}", str(nw)).replace("{LOW}", str(lo)).replace("{HIGH}", str(hi))
        r = claude(p, adddirs=(ROOT, INK))
        if r:
            t = repair(r, f"fix{cycle}")
    t = re.split(r"\n+(?:TECHNICAL NOTE|NOTE TO EDITOR):", t)[0].rstrip() + "\n"
    log["final_words"] = words(t)
    log["final_loss"] = loss(a, inv(t))
    OUT.mkdir(exist_ok=True); NOTES.mkdir(exist_ok=True)
    out.write_text(t)
    tmp = NOTES / (f + ".txt")
    tmp.write_text(t)
    try:
        s = subprocess.run([sys.executable, str(SCORER), str(SIDECAR), str(tmp)], capture_output=True, text=True, timeout=120)
        log["voice"] = (s.stdout.strip() or s.stderr.strip())[-600:]
    except Exception as e:  # noqa: BLE001
        log["voice"] = f"NOT SCORED: {e}"
    tmp.unlink(missing_ok=True)
    note.write_text(json.dumps(log, indent=1))
    return f, f"ok {nw}->{log['final_words']} loss={len(log['final_loss'])}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--workers", type=int, default=8); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    fs = [f for f in FILES if not a.only or f in a.only.split(",")]
    OUT.mkdir(exist_ok=True); NOTES.mkdir(exist_ok=True)
    Path("/tmp/claude-1000/empty").mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda f: job(f, a.force), fs):
            print(*r, flush=True)
