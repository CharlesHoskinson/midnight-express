#!/usr/bin/env python3
"""Assemble the design document from the drafts.

    python3 assemble.py [--src draft] [--out document.md] [--body-only]

Order: front matter (written by the build), Part I (chapters 1-4 + MPS), Part II (5-7), Part III (8-11), conclusion (12),
References (citeproc), Appendix A (generated), Appendix B (reading list expanded from the writers' @slug :: annotation lines), then the MIP.
Replaces {{fig:N-M}} markers by images with the captions of figures.json (a missing image is dropped and reported).
--body-only writes the text without Appendix A (for readers)."""
import argparse, json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
B = D / "build"
FIGS = {f["id"]: f for f in json.loads((D / "figures.json").read_text())}
REFS = {r["id"]: r for r in json.loads((B / "references.json").read_text())}


def fig(m):
    i = m.group(1)
    f = FIGS.get(i)
    path = D / "figures" / f"fig-{i}.png"
    if not f or not path.exists():
        print(f"missing figure {i}", file=sys.stderr)
        return ""
    return f"\n![**Figure {i.replace('-', '.')}.** {f['caption']}](figures/fig-{i}.png){{width=100%}}\n"


def read(src, name):
    p = src / name
    return p.read_text() if p.exists() else ""


def strip_note(t):
    return re.split(r"\n+NOTE TO EDITOR:", t)[0].rstrip() + "\n"


def refline(slug):
    r = REFS.get(slug)
    if not r:
        return None
    au = r.get("author") or []
    names = ", ".join((a.get("given", "") + " " + a.get("family", a.get("literal", ""))).strip() for a in au[:4]) + (", et al." if len(au) > 4 else "")
    yr = (r.get("issued") or {}).get("date-parts", [[""]])[0][0]
    venue = r.get("container-title", "")
    url = r.get("DOI") and "https://doi.org/" + r["DOI"] or r.get("URL", "")
    return f"{names + '. ' if names else ''}**{r['title']}**{'. ' + venue if venue else ''}{' (' + str(yr) + ')' if yr else ''}.{' <' + url + '>' if url else ''}"


def reading_list(src):
    out = ["# Appendix B. Annotated reading list {.unnumbered #appendix-b}", "",
           "The works below are grouped by theme and listed in date order within each theme. Each entry says what the work is, what it shows and how it bears on this design."]
    bad = 0
    for name in ("B1-reading-W1.md", "B2-reading-W2.md", "B3-reading-W3.md", "B4-reading-W4.md"):
        for line in read(src, name).splitlines():
            if line.startswith("## "):
                out += ["", "## " + line[3:].strip() + " {.unnumbered}", ""]
            elif line.startswith("@") and "::" in line:
                slug, ann = [x.strip() for x in line.split("::", 1)]
                slug = slug.lstrip("@")
                ref = refline(slug)
                if not ref:
                    bad += 1
                    print("reading list: unknown key", slug, file=sys.stderr)
                    continue
                out += [f"**{ref}**  ", ann, ""]
    return "\n".join(out) + "\n", bad


def unnumber(text):
    return re.sub(r"^(#{1,4} .*?)(?<!\})$", lambda m: m.group(1) + " {.unnumbered}" if "{" not in m.group(1) else m.group(1), text, flags=re.M)


def mip(src):
    pre = ("MIP: xxxx\n\nTitle: Midnight Express: Confidential Message and Private Event Delivery over a GossipSub Overlay with Ledger Anchoring\n")
    head = ["# Midnight Improvement Proposal {.unnumbered #mip}", "",
            "| | |", "|---|---|",
            "| MIP | xxxx |", "| Title | Midnight Express: Confidential Message and Private Event Delivery over a GossipSub Overlay with Ledger Anchoring |",
            "| Authors | Charles Hoskinson (@CharlesHoskinson) |", "| Status | Draft |", "| Category | Standards |", "| Created | 2026-10-02 |",
            "| Requires | MIP-0019 |", "| Replaces | none |", "| MPS | MPS-xxxx (Confidential Message and Private Event Delivery for Contracts, Agents and Wallets) |",
            "| License | Apache-2.0 |", ""]
    parts = [strip_note(read(src, f"M{i}.md")).strip() for i in range(1, 7)]
    body = "\n\n".join(p for p in parts if p)
    body = re.sub(r"^## ", "## ", body, flags=re.M)
    return "\n".join(head) + "\n" + unnumber(body) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="draft")
    ap.add_argument("--out", default="document.md")
    ap.add_argument("--body-only", action="store_true")
    a = ap.parse_args()
    src = D / a.src
    ch = lambda f: strip_note(read(src, f))  # noqa: E731
    parts = []
    exec_sum = read(src, "00-executive-summary.md")
    if exec_sum:
        parts.append("# Executive summary {.unnumbered #exec}\n\n" + re.sub(r"^# .*\n+", "", strip_note(exec_sum)))
    def part(label, title, img, files):
        t = [f"\n\\partpage{{{label}}}{{{title}}}{{figures/{img}.png}}\n"]
        t += [ch(f) for f in files if (src / f).exists()]
        return "\n\n".join(t)
    parts.append(part("Part I", "Midnight and the case for private events", "part-1", ["01-introduction.md", "02-midnight.md", "03-need.md", "04-definition.md", "04b-mps.md"]))
    parts.append(part("Part II", "Options and requirements", "part-2", ["05-prior-art.md", "06-options.md", "07-requirements.md"]))
    parts.append(part("Part III", "Experimental design for Confidential Messages over GossipSub", "part-3", ["08-reference-system.md", "09-experiments.md", "10-results.md", "11-roadmap.md", "12-conclusion.md"]))
    text = "\n\n".join(parts)
    text = re.sub(r"\{\{fig:([0-9]+-[0-9]+)\}\}", fig, text)
    out = [text, "\n# References {.unnumbered #references}\n\n::: {#refs}\n:::\n"]
    if not a.body_only:
        out.append("\n\\partpage{Appendix A}{Requirements in EARS form}{figures/appendix-a.png}\n")
        out.append("\n\\begingroup\\appendixsize\n")
        out.append(unnumber((B / "appendix-a.md").read_text()))
        out.append("\n\\endgroup\n")
        rl, bad = reading_list(src)
        out.append("\n\\partpage{Appendix B}{Annotated reading list}{figures/appendix-b.png}\n")
        out.append(rl)
    if (src / "M1.md").exists():
        out.append("\n\\partpage{Proposal}{Midnight Improvement Proposal}{figures/part-4.png}\n")
        out.append(mip(src))
    doc = "\n".join(out)
    for old, new in (("MPS-0044", "MPS-xxxx"), ("MIP-0020", "MIP-xxxx"), ('MPS: "0044"', 'MPS: "xxxx"'), ('MIP: "0020"', 'MIP: "xxxx"')):
        doc = doc.replace(old, new)
    (B / a.out).write_text(doc)
    print(f"wrote {B / a.out}: {len((B / a.out).read_text().split())} words")


if __name__ == "__main__":
    main()
