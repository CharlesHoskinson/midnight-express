#!/usr/bin/env python3
"""Write the executive summary and the conclusion. Reads finished chapters (draft-r4 where present, else draft-r3, else draft-r2). Writes ../draft-r4/00-executive-summary.md and 12-conclusion.md."""
import re, sys
from pathlib import Path
import run_inkwell as R
D, ROOT = R.D, R.ROOT
OUT = D / "draft-r4"; OUT.mkdir(exist_ok=True)

def src(f):
    for d in ("draft-r4", "draft-r3", "draft-r2"):
        if (D / d / f).exists():
            return D / d / f
JOBS = {
 "00-executive-summary.md": "Write the Executive summary (about 900 words, 6 to 9 paragraphs, no bullets). Open with the problem in Midnight's terms, give the Foundation's meaning of private event and how Midnight Express relates to it (complement and, under conditions, transport), state the definition of a Confidential Message, the options considered and the recommended design in three or four sentences, what the ledger interface experiment and the prototype showed (with the headline measured and derived numbers, each labelled measured, derived or assumed), what remains unknown, and what the Foundation is asked to decide (the proposal and the problem statement, numbers left as xxxx). The first line of the file is exactly `# Executive summary`.",
 "12-conclusion.md": "Write Chapter 12, the Conclusion (about 900 to 1,200 words, no bullets). The first line is exactly `# Conclusion {#ch12}`. State what the document established and with what evidence, what it did not establish (the stand-in admission proof, no network run, derived fees, simulator limits, interop gaps), the order in which the open questions should be settled by logical dependence (not by calendar), and the conditions that would change the recommendation. End on the next concrete obligation, not on a summary. No recap list of chapters.",
}
for f, task in JOBS.items():
    if (OUT / f).exists():
        continue
    chapters = [f"{c}: {src(c)}" for c in R.FILES if not c.startswith("B") and src(c) and c not in ("M3.md", "M5.md", "M6.md")]
    prompt = f"""You are writing one part of the design document "Midnight Express: Private Events for Midnight". {R.COMMON}

{task}

Read the finished chapters from these files (all of them, in order; use Read): {chr(10).join(chapters)}
Also read {D}/FACTS.md and {D}/WRITING_LESSONS.md (sections 1 to 3). Every number, name and claim you write must agree with the chapters; check each against the chapter text. Do not add a claim the chapters do not support. No em dashes, no placeholders, no process words.

Your entire final message is the Markdown of the file and nothing else."""
    t = R.claude(prompt, adddirs=(ROOT, R.INK, D), timeout=3300)
    if t:
        lines = t.splitlines()
        i = next((k for k, l in enumerate(lines) if l.startswith("# ")), 0)
        (OUT / f).write_text("\n".join(lines[i:]).rstrip() + "\n")
        print("wrote", f, len(t.split()), flush=True)
    else:
        print("failed", f, flush=True)
