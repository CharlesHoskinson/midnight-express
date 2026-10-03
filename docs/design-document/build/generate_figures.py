#!/usr/bin/env python3
"""Generate the document's artwork and diagrams with GPT image generation (via `codex exec`), in the Midnight City style.

    python3 generate_figures.py [--only fig-8-1,cover] [--parallel 4]
Output PNGs go to ../figures/<id>.png (copied from Codex's generated_images folder). Resume-safe: existing files are kept.
"""
import argparse, concurrent.futures as cf, json, re, shutil, subprocess, time
from pathlib import Path
D = Path(__file__).resolve().parents[1]
OUT = D / "figures"; OUT.mkdir(exist_ok=True)
FIG = {f["id"]: f for f in json.loads((D / "figures.json").read_text())}

ART = ("Pixel art in the style of a modern 16-bit-inspired indie game. Deep navy-to-black night palette (#000000, #03050d, #19344d, #2f5477), "
       "sky blue (#6cb7ff) highlights and warm orange (#e85d2c) lit windows and glows, pale blue-white (#e0f0ff) stars and light. Crisp square pixels, "
       "no anti-aliasing blur, soft vignette fading to pure black at the edges. No text, no logos, no watermark, no people's faces.")
DIAG = ("A clean technical diagram drawn in pixel-art/blueprint style on a pure black (#000000) background, like a game interface: panels with thin hairline "
        "borders (#292f39) and small notched chevron corners, thin signal-blue (#6cb7ff) lines, the key path highlighted in orange (#e85d2c), pale blue-white (#e0f0ff) "
        "text in a condensed uppercase monospace type, small diamond marks. Wide 16:9 landscape. Generous spacing, no clutter. Use ONLY the exact label texts listed, spelled exactly as given, "
        "uppercase; add no other words, no numbers beyond those listed, no logos, no watermark. Every label must be fully legible and not overlap any line.")

ART_ITEMS = {
 "cover": ("Portrait 2:3 book-cover artwork. A pixel-art night express train with warm orange lit windows speeding along a long viaduct bridge over dark water toward a city skyline "
           "of dark towers with a few orange lit windows, under a deep blue star-filled sky with a pale moon at upper right. Thin glowing blue and orange lines rise from the towers and join "
           "into a loose network of nodes across the sky, suggesting sealed messages travelling between windows. Foreground black cliffs and trees. Large empty dark area in the upper "
           "third for a title. No text."),
 "part-1": ("Landscape 16:9 artwork for 'Part I'. A pixel-art city gate and skyline at midnight with a single glowing orange doorway and a quiet street, deep blue sky, one small signal tower. No text."),
 "part-2": ("Landscape 16:9 artwork for 'Part II'. A pixel-art crossroads at night with five distinct lit paths branching toward different districts of a distant city, one path glowing orange, lanterns, deep blue sky. No text."),
 "part-3": ("Landscape 16:9 artwork for 'Part III'. A pixel-art night test field: a ring of small lit relay towers connected by thin blue light lines over dark hills, a distant city skyline, an orange beacon, stars. No text."),
 "part-4": ("Landscape 16:9 artwork for the final section, a proposal. A pixel-art night scene of a bridge under construction reaching toward a lit city across dark water, orange work lights, blue sky. No text."),
 "appendix-a": ("Landscape 16:9 artwork for an appendix of requirements. A pixel-art night archive hall with endless glowing ledger shelves and orange lamps, deep blue shadows. No text."),
 "appendix-b": ("Landscape 16:9 artwork for a reading list. A pixel-art night library with tall bookshelves, a reading desk with an orange lamp, a window onto a skyline, deep blue shadows. No text."),
}
LAYOUT = {
 "2-1": "Layout: a tall vertical stack of five full-width horizontal panels, top to bottom: WALLETS AND DAPPS; INDEXER (CONTRACT EVENTS, WALLET SYNC); MIDNIGHT NODE: LEDGER, COMPACT CONTRACTS, ZERO-KNOWLEDGE PROOFS; CONSENSUS AND CARDANO PARTNER CHAIN; LIBP2P NETWORK: CONSENSUS GOSSIP ONLY. Left of the stack, a dashed empty blue slot with the label NO PRIVATE EVENT PATH. Right of the stack, an orange arrow rising from the node panel to a glowing open envelope labelled PUBLIC EVENT (EMIT): 32 B NAME + 256 B PAYLOAD.",
 "3-1": "Layout: two equal panels side by side. Left panel title PUBLIC EVENT: an open envelope with lines showing NAME, PAYLOAD, CONTRACT and BLOCK TIME, a large eye looking at it, caption OBSERVER SEES: WHO REACTED, WHEN, TO WHAT. Right panel title CONFIDENTIAL MESSAGE: a closed uniform envelope with a lock and a small label SIZE CLASS, SHARD, TIME, a small eye, caption OBSERVER SEES: SIZE CLASS, SHARD, TIME.",
 "4-1": "Layout: a left-to-right path: PUBLISHER, then BUS NODE (RELAY), then a second BUS NODE (RELAY), then SUBSCRIBER, joined by an orange line. Above the middle, a cluster of three nodes highlighted in orange labelled COLLUDING INFRASTRUCTURE. Between the two relays, a small figure with a pair of scissors over the link, labelled ACTIVE NETWORK ADVERSARY. Below the middle left, a cylinder labelled INDEXER; below the middle right, a block labelled CHAIN OBSERVER. At the top a very large eye with faint rays over everything labelled GLOBAL PASSIVE OBSERVER. Each adversary has a small eye icon.",
 "5-1": "Layout: a two-axis map. Horizontal axis labelled COSTS MORE with an arrow to the right; vertical axis labelled HIDES MORE with an arrow upward. Place small pixel icons with labels: TOPIC GOSSIP (GOSSIPSUB) low-left; FEDERATED RELAYS low-left; LEDGER LOG WITH STEALTH ADDRESSES lower-middle; FUZZY DETECTION AND OBLIVIOUS RETRIEVAL middle; FLOOD AND TRIAL-DECRYPT (BITMESSAGE) middle-right; PRIVATE INFORMATION RETRIEVAL right-middle; MIXNETS upper-right; DC-NETS top-right.",
 "6-1": "Layout: five panels in a row, each a small schematic with a title: OPTION 1: LEDGER AND INDEXER ONLY (publisher to ledger to indexer to subscriber, badge LEDGER LANE); OPTION 2: HYBRID, GOSSIPSUB SIDECAR OVERLAY WITH LEDGER ANCHORING (publisher to a mesh of nodes to subscriber, with a dotted line to a ledger block, orange border, badge RECOMMENDED); OPTION 3: IN-NODE PROTOCOL (a ledger node with gossip inside); OPTION 4: MIX NETWORK OR PIR DELIVERY (layers of mix nodes); OPTION 5: EXTERNAL PUB/SUB SERVICE (a cloud server with clients).",
 "7-1": "Layout: a left-to-right funnel of five connected blocks: 10 DECISION AREAS (D1 TO D10); 12 REQUIREMENT AREAS; 625 REQUIREMENT ENTRIES; 510 LIVE REQUIREMENTS; 137-REQUIREMENT PROTOTYPE CORE (orange). Two smaller blocks feed into the funnel from below: 28 DECISIONS RECORDED and 53 RECONCILED PARAMETERS.",
 "8-1": "Layout: centre, a cluster of hexagonal nodes labelled BUS NODE inside a rounded region labelled GOSSIPSUB MESH (SHARD). Left, PUBLISHER with an orange arrow into the mesh. Right, two SUBSCRIBER boxes and one box CONSUMER: AGENT, CONTRACT, WALLET. Below the mesh, STORE NODE attached to it. Top, a box ANCHORER sending an arrow up to a wide bar BUS REGISTRY CONTRACT (MIDNIGHT). Bottom right, a box INDEXER with a dotted orange path from a box LEDGER LANE: MISC EVENTS ON THE LEDGER.",
 "8-2": "Layout: four horizontal bars stacked, one per class. Each bar has three segments left to right: FIXED HEADER 8 B (small), ADMISSION SLOT 512 B (medium), SEALED BODY (long, orange). Row labels at left and total at right: CLASS 0, body 256 B, 776 B ON THE WIRE; CLASS 1, body 1,024 B, 1,544 B; CLASS 2, body 4,096 B, 4,616 B; CLASS 3, body 16,384 B, 16,904 B. Small note NOT TO SCALE.",
 "8-3": "Layout: six connected stations left to right along an orange line, each with a pixel icon and a number: 1 SEAL (padlock), 2 ADMIT (ticket gate), 3 GOSSIP (mesh of nodes), 4 RECOGNISE (magnifier over an envelope), 5 ANCHOR (chain block), 6 REACT (gear).",
 "9-1": "Layout: a left-to-right pipeline of six panels joined by arrows: SEEDED SCHEDULE; SWARM OF 50 NODES (small cluster of dots); TEN SCENARIOS (ten small squares); INSTRUMENTATION; RESULT FILE; CHECKER AND THRESHOLDS ending in a green pass light and a red fail light.",
 "11-1": "Layout: a horizontal winding path from left to right with five gates, each a numbered milestone: STAGE 0: MODELS, SIMULATION AND PROOF OF CONCEPT; STAGE 1: PERMISSIONED PILOT; STAGE 2: PERMISSIONED PRODUCTION; STAGE 3: OPEN ADMISSION; STAGE 4: HANDOVER AND STRONGER PRIVACY. A pixel city skyline grows taller and brighter behind the gates from left to right.",
}
def prompt(i):
    if i in ART_ITEMS: return ART + "\n\n" + ART_ITEMS[i]
    f = FIG[i.replace("fig-", "")]
    return DIAG + "\n\nExact label texts (uppercase): " + "; ".join(l.upper() for l in f["labels"]) + ".\n\n" + LAYOUT[f["id"]]

def newest_png(since):
    cands = [p for p in (Path.home() / ".codex" / "generated_images").glob("*/*.png") if p.stat().st_mtime >= since]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None

def make(i):
    dst = OUT / f"{i}.png"
    if dst.exists(): return i, "have"
    t0 = time.time()
    p = ("Use your image generation tool to create exactly ONE image from the brief below. Do not write any files yourself and do not run commands. "
         "When the image is made, reply with only the absolute file path of the generated image.\n\nBRIEF:\n" + prompt(i))
    out = Path(f"/tmp/claude-1000/figgen/{i}.txt"); out.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["codex", "exec", "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="low"', "--ephemeral", "--ignore-user-config", "-s", "read-only",
                        "--skip-git-repo-check", "-C", "/tmp/claude-1000/figgen", "-o", str(out), p], capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return i, "timeout"
    m = re.search(r"(/[^\s'\"`]+\.png)", out.read_text() if out.exists() else "")
    src = Path(m.group(1)) if m and Path(m.group(1)).exists() else newest_png(t0)
    if not src: return i, "no image"
    shutil.copy(src, dst)
    return i, f"ok {round(time.time()-t0)}s"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--parallel", type=int, default=4); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    ids = list(ART_ITEMS) + [f"fig-{f['id']}" for f in FIG.values() if f["kind"] == "diagram"]
    if a.only: ids = [x for x in ids if x in a.only.split(",")]
    if a.force:
        for x in ids: (OUT / f"{x}.png").unlink(missing_ok=True)
    with cf.ThreadPoolExecutor(a.parallel) as ex:
        for r in ex.map(make, ids): print(*r, flush=True)

if __name__ == "__main__":
    main()
