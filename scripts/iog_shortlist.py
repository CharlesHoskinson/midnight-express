#!/usr/bin/env python3
"""Download the IOG-library papers chosen for the private event bus corpus (slice H-iog)."""
import json, re, subprocess, sys, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PY = Path.home() / ".local/share/uv/tools/scrapling/bin/python"
SHORT = {  # title prefix -> (role, tags)
 "CougaR": ("core", ["dissemination", "eclipse"]),
 "SCRamble": ("core", ["overlay", "dissemination"]),
 "SecureCyclon": ("core", ["peer-sampling", "gossip"]),
 "The Generals": ("core", ["gossip", "byzantine"]),
 "Introduction to the design of the Data Diffusion": ("core", ["cardano-network"]),
 "Correctness of Broadcast via Multicast": ("core", ["multicast"]),
 "Are continuous stop-and-go mixnets": ("core", ["mixnet"]),
 "Proofs about Network Communication": ("adjacent", ["network-model"]),
 "Message-passing in the Extended UTxO": ("adjacent", ["ledger-messaging"]),
 "MARS: Monetized": ("adjacent", ["routing", "incentives"]),
 "Incentivizing Geographic Diversity": ("adjacent", ["network", "incentives"]),
 "Ouroboros Leios": ("adjacent", ["cardano-network", "throughput"]),
 "High-Throughput Permissionless Blockchain Consensus": ("adjacent", ["network-model"]),
 "Full Analysis of Nakamoto Consensus": ("adjacent", ["network-delay"]),
 "What Did Come Out of It": ("core", ["didcomm", "messaging", "privacy"]),
 "Modular Design of Secure Group Messaging": ("adjacent", ["mls", "group-messaging"]),
 "Security Analysis and Improvements for the IETF MLS": ("adjacent", ["mls"]),
 "Continuous Group Key Agreement": ("adjacent", ["mls", "cgka"]),
 "Kachina": ("core", ["midnight", "private-smart-contracts"]),
 "Zswap": ("core", ["midnight", "shielded"]),
 "Ouroboros Crypsinous": ("adjacent", ["privacy"]),
 "Uncontrolled Randomness in Blockchains": ("core", ["bulletin-board", "covert"]),
 "Turn-Based Communication Channels": ("adjacent", ["channels"]),
 "Setchain": ("adjacent", ["set-broadcast"]),
 "State Machine Replication Among Strangers": ("adjacent", ["gossip", "smr"]),
 "SyRA": ("adjacent", ["sybil-resistance", "anonymous-credentials"]),
 "SoK: Communication Across Distributed Ledgers": ("adjacent", ["cross-chain-messaging"]),
}
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
rows = [json.loads(l) for l in (ROOT/"catalog/iog-library.jsonl").read_text().splitlines()]
out = ROOT/"catalog/H-iog.jsonl"
done = {json.loads(l)["slug"] for l in out.read_text().splitlines()} if out.exists() else set()
for r in rows:
    if r.get("status") != 200: continue
    key = next((k for k in SHORT if r["title"].startswith(k)), None)
    if not key: continue
    sl = "iog-" + slug(r["title"])[:60]
    if sl in done: continue
    pdf = next((l["href"] for l in r["links"]), None)
    rec = {"slug": sl, "title": r["title"], "year": None, "venue": None, "doi": None, "arxiv": None,
           "landing_url": r["url"], "pdf_url": pdf, "status": "metadata_only", "pdf_path": None,
           "sha256": None, "relevance": SHORT[key][0], "tags": SHORT[key][1], "kind": "paper",
           "cluster": "H-iog", "found_via": "iog.io/papers",
           "note": "IOG research library; listing text: " + re.sub(r"\s+", " ", r["text"])[:220]}
    if pdf:
        res = subprocess.run([str(PY), str(ROOT/"scripts/pe_fetch.py"), "pdf", pdf, sl], capture_output=True, text=True)
        try:
            j = json.loads([l for l in res.stdout.splitlines() if l.startswith("{")][-1])
        except Exception:
            j = {"ok": False}
        if j.get("ok"):
            rec.update(status="downloaded", pdf_path=j["path"], sha256=j["sha256"])
    print(rec["status"], "|", r["title"][:70], "|", pdf)
    with out.open("a") as fh: fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
