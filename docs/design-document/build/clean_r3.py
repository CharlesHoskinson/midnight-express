#!/usr/bin/env python3
"""Strip model chatter around the content of each ../draft-r3 file: text before the file's first line (as found in its base) and after any trailing note.

    python3 clean_r3.py [dir]   (default draft-r3). Writes in place; reports every file changed and what was cut.
"""
import re, sys
from pathlib import Path
D = Path(__file__).resolve().parents[1]
dirn = D / (sys.argv[1] if len(sys.argv) > 1 else "draft-r3")
for p in sorted(dirn.glob("*.md")):
    base = D / "draft-r2" / p.name
    if not base.exists():
        base = D / "draft" / p.name
    if not base.exists():
        continue
    b = [l for l in base.read_text().splitlines() if l.strip()]
    first = b[0].strip()
    t = p.read_text()
    lines = t.splitlines()
    idx = next((i for i, l in enumerate(lines) if l.strip() == first or (first.startswith("#") and l.strip().startswith(first[:25]))), None)
    cut_head = ""
    if idx:
        cut_head = "\n".join(lines[:idx])
        lines = lines[idx:]
    t2 = "\n".join(lines)
    t2 = re.split(r"\n+(?:TECHNICAL NOTE|NOTE TO EDITOR|Technical note)[:\s]", t2)[0].rstrip() + "\n"
    # trailing chatter such as "Word count: ..." or "The full text above ..."
    t2 = re.sub(r"\n+(?:\*?\(?(?:Word count|Length|The file above|This revision)[^\n]*)\s*$", "\n", t2)
    if t2 != t:
        p.write_text(t2)
        print(p.name, "cut head:", repr(cut_head[:120]), "| tail trimmed:", len(t) - len(t2) - len(cut_head))
