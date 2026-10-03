#!/usr/bin/env python3
"""Draw the data charts of Chapter 10 in the Midnight City style. Values are those of the pilot result tables.
    ~/.local/share/uv/tools/graphifyy/bin/python make_charts.py"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

D = Path(__file__).resolve().parents[1]
for f in (D / "fonts").glob("IosevkaCharon-*.ttf"):
    fm.fontManager.addfont(str(f))
BG, PANEL, GRID, TXT, MUTED, BLUE, ORANGE, RED = "#000000", "#000f1e", "#292f39", "#e0f0ff", "#8fa8c4", "#6cb7ff", "#e85d2c", "#ff5a4d"
plt.rcParams.update({"font.family": "Iosevka Charon", "text.color": TXT, "axes.labelcolor": TXT, "xtick.color": TXT, "ytick.color": TXT,
                     "axes.edgecolor": GRID, "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG, "font.size": 13})

def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)

def label(ax, bars, fmt, dy=0.0):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + dy, fmt(b.get_height()), ha="center", va="bottom", color=TXT, fontsize=14)

# 10-1 IDONTWANT
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=168)
groups = ["NOMINAL LOAD\n(IMPLEMENTATION B)", "CLASS 3 AT THE BYTE CAP\n(IMPLEMENTATION A)"]
on, off = [2.26, 1.41], [5.12, 4.68]
x = range(2); w = 0.34
b1 = ax.bar([i - w / 2 for i in x], on, w, color=ORANGE, label="IDONTWANT ON")
b2 = ax.bar([i + w / 2 for i in x], off, w, color=BLUE, label="IDONTWANT OFF")
label(ax, b1, lambda v: f"{v:.2f}×", 0.08); label(ax, b2, lambda v: f"{v:.2f}×", 0.08)
ax.set_xticks(list(x)); ax.set_xticklabels(groups); ax.set_ylim(0, 6.2)
ax.set_ylabel("MEDIAN INGRESS AMPLIFICATION (×)"); style(ax)
ax.legend(frameon=False, loc="upper right", labelcolor=TXT)
fig.tight_layout(); fig.savefig(D / "figures/fig-10-1.png"); plt.close(fig)

# 10-2 churn
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5.6), dpi=168, gridspec_kw={"wspace": 0.28})
names = ["A\nIGNORE,\nNO ADDRESS\nDISCOVERY", "B\nSILENT,\nREPAIR\nEVERY 60 s", "C\nBUSY REPLY,\nREPAIR\nEVERY 5 s"]
deliv, p99 = [0.816, 1.0, 1.0], [26.5, 42.7, 1.10]
cols = [RED, BLUE, ORANGE]
bs = a1.bar(range(3), deliv, 0.55, color=cols); label(a1, bs, lambda v: f"{v:.3f}", 0.012)
a1.set_ylim(0, 1.12); a1.set_xticks(range(3)); a1.set_xticklabels(names, fontsize=10.5); a1.set_title("DELIVERY OF ELIGIBLE PAIRS", color=MUTED, fontsize=12); style(a1)
bs = a2.bar(range(3), p99, 0.55, color=cols); label(a2, bs, lambda v: f"{v:.1f} s", 0.8)
a2.set_ylim(0, 52); a2.set_xticks(range(3)); a2.set_xticklabels(names, fontsize=10.5); a2.set_title("P99 LATENCY (s)", color=MUTED, fontsize=12); style(a2)
fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.30); fig.savefig(D / "figures/fig-10-2.png"); plt.close(fig)

# 10-3 overhead
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=168)
cls = ["CLASS 0", "CLASS 1", "CLASS 2", "CLASS 3"]; wire = [776, 1544, 4616, 16904]; over = 690; pay = [w_ - over for w_ in wire]
ov = [over / w_ * 100 for w_ in wire]; pl = [100 - o for o in ov]
y = range(4)
ax.barh(y, ov, 0.55, color=ORANGE, label="FIXED OVERHEAD, 690 B"); ax.barh(y, pl, 0.55, left=ov, color=BLUE, label="PAYLOAD CAPACITY")
for i in y:
    ax.text(ov[i] / 2 if ov[i] > 12 else ov[i] + 1.2, i, f"{ov[i]:.1f}%" if ov[i] > 12 else f"{ov[i]:.1f}%", va="center", ha="center" if ov[i] > 12 else "left", color=BG if ov[i] > 12 else TXT, fontsize=13)
    txt = f"{pay[i]:,} B payload of {wire[i]:,} B"
    if pl[i] >= 25:
        ax.text(ov[i] + pl[i] / 2, i, txt, va="center", ha="center", color=BG, fontsize=13)
    else:
        ax.text(101.5, i, txt, va="center", ha="left", color=TXT, fontsize=13)
ax.set_yticks(list(y)); ax.set_yticklabels(cls); ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("SHARE OF THE WIRE LENGTH (%)"); ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, labelcolor=TXT)
fig.subplots_adjust(left=0.12, right=0.80, top=0.96, bottom=0.26); fig.savefig(D / "figures/fig-10-3.png"); plt.close(fig)
print("charts written")
