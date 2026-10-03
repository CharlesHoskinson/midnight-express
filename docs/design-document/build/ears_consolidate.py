#!/usr/bin/env python3
"""Consolidate the twelve EARS area files + reconciliation into Appendix A (Markdown) and a JSON register.

    python3 ears_consolidate.py            -> writes appendix-a.md, ears-consolidated.json, ears-stats.json next to this script

Rules (from design/ears/reconcile.json):
  fixes      replace the record named in `replaces`; splits (a/b) replace one record by several
  gaps       new records added to their area
  duplicates every `others` ID becomes a one-line cross-reference to the canonical ID
  withdrawn  MPE-CON-007 and MPE-CON-008 (recorded as withdrawn)

Then (this directory):
  ears_revisions.json  list of operations applied after fixes and gaps:
                       {"op": "replace", "id", fields...}  overwrites the given fields of an existing record
                       {"op": "add", "id", fields...}      creates a new record
                       {"op": "param", "id": "P-...", "meaning"}  overrides a parameter's meaning text
                       optional "note" is printed under the verification line; "source" is not printed
  vocabulary pass      final pass over title, sentence, verify and note of every record, the parameter tables and the
                       area scope texts (STYLE.md, "Vocabulary")
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "design/ears"))
from lint import records  # noqa: E402

R5 = ROOT / "design/rounds/r5"
rj = json.loads((ROOT / "design/ears/reconcile.json").read_text())

AREAS = [  # (code, chapter title, file)
    ("FMT", "Message and MPE Envelope format", "e07-fmt-format.md"),
    ("CRY", "Cryptography and key management", "e02-cry-crypto.md"),
    ("PUB", "Publish and subscribe model and delivery", "e08-pub-model.md"),
    ("CON", "Consumers: agents, contracts and wallets", "e09-con-consumers.md"),
    ("ECO", "Admission, economics and spam cost", "e10-eco-economics.md"),
    ("NET", "GossipSub overlay and Midnight tether", "e12-net-overlay.md"),
    ("PRF", "Performance and capacity", "e04-prf-performance.md"),
    ("STO", "Storage and retention", "e05-sto-storage.md"),
    ("OPS", "Infrastructure actors, governance and operations", "e11-ops-actors.md"),
    ("PRV", "Privacy properties and leakage", "e01-prv-privacy.md"),
    ("SEC", "Threats, abuse resistance and failure handling", "e03-sec-threats.md"),
    ("VER", "Verification and prototype acceptance", "e06-ver-verification.md"),
]
WITHDRAWN = {"MPE-CON-007": "DEC-003 (salted per-Envelope Tags replace the earlier tag rule)",
             "MPE-CON-008": "DEC-003 (salted per-Envelope Tags replace the earlier tag rule)"}


def key(i):
    m = re.match(r"MPE-([A-Z]{3})-(\d+)([a-z]?)", i)
    return (m.group(1), int(m.group(2)), m.group(3))


def rec_from(r, origin):
    a = r["attrs"]
    first = lambda k: (a.get(k) or "").split()[0].strip(".,;").strip("`") if a.get(k) else ""  # noqa: E731
    st = a.get("Status", "")
    return {"id": r["id"], "title": r["title"].strip(), "sentence": " ".join(r["sentence"]).strip(),
            "pattern": first("Pattern").lower(), "scope": first("Scope").upper(), "priority": first("Priority").upper(),
            "status": "open" if st.startswith("open") else "settled", "decision": (re.search(r"DEC-[A-Z]{3}-\d+", st) or [None])[0],
            "verify": (a.get("Verify") or "").strip(), "origin": origin}


def area_text(path, heading):
    t = path.read_text()
    m = re.search(rf"^## {heading}[^\n]*\n(.*?)(?=^## )", t, re.S | re.M)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- revisions
REV_FIELDS = ("title", "sentence", "pattern", "scope", "priority", "status", "decision", "verify", "note")


def apply_revisions(reg, area_params):
    path = HERE / "ears_revisions.json"
    n = {"replaced": 0, "added": 0, "params": 0}
    if not path.exists():
        return n
    for op in json.loads(path.read_text()):
        i, kind = op["id"], op["op"]
        if kind == "param":
            if i in area_params:
                area_params[i]["meaning"] = op["meaning"]
                n["params"] += 1
            else:
                print(f"warning: parameter {i} not in the area tables", file=sys.stderr)
            continue
        if kind == "replace":
            if i not in reg:
                raise SystemExit(f"replace of unknown record {i}")
            rec, n["replaced"] = reg[i], n["replaced"] + 1
            origin = "revised"
        elif kind == "add":
            if i in reg:
                raise SystemExit(f"add of existing record {i}")
            rec, n["added"] = {"id": i, "title": "", "sentence": "", "pattern": "", "scope": "", "priority": "",
                               "status": "settled", "decision": None, "verify": ""}, n["added"] + 1
            reg[i] = rec
            origin = "added"
        else:
            raise SystemExit(f"unknown operation {kind} for {i}")
        for f in REV_FIELDS:
            if f in op:
                rec[f] = op[f]
        rec["origin"] = origin
    return n


# ---------------------------------------------------------------- vocabulary (STYLE.md, "Vocabulary")
# Phase A: fixed phrases on the raw text (they may contain code spans). Phase B: word rules on text whose code
# spans, quotations and identifiers are protected. Phase C: articles.
PHRASES = [
    # Message (the bus's object) and the Logical Message Identifier
    (r"\bLogical Event Identifier", "Logical Message Identifier"),
    (r"\b([Ll])ogical [Ee]vent identifier", r"\1ogical message identifier"),
    (r"\bsealing a private Event\b", "sealing a Message"),
    # ledger lane
    (r"\bthe fallback `Misc` path\b", "the ledger lane"),
    (r"\bfallback `Misc` event\b", "ledger-lane `Misc` event"),
    (r"\bfallback-publish calls\b", "ledger-lane publish calls"),
    (r"\bFallback path read\b", "Ledger lane read"),
    (r"\bfallback Envelopes\b", "ledger-lane Envelopes"),
    (r"\bagainst the fallback path\b", "against the ledger lane"),
    (r"\bLedger fallback\b", "Ledger lane"),
    (r"\bthe ledger fallback\b", "the ledger lane"),
    (r"\bfallback Event\b", "ledger-lane Message"),
    (r"\bfallback publications\b", "ledger-lane publications"),
    (r"\bAnchor, fallback, and consumption\b", "Anchor, ledger-lane, and consumption"),
    (r"\bback-fill and fallback\b", "back-fill and the ledger lane"),
    (r"\bover a fallback path\b", "over a path other than the overlay"),
    (r"\bthe fallback mode it used\b", "the carrier it used"),
    (r"\bExplicit fallback label\b", "Explicit carrier label"),
    # admission window; key periods are not admission windows
    (r"\bAfter erasing epoch-1 keys, back-filling epoch 1 yields", "After erasing the keys of key period 1, back-filling period 1 yields"),
    (r"\bErase epoch keys, back-fill that epoch\b", "Erase the keys of one key period, back-fill that period"),
    (r"\bmid-epoch\b", "in the middle of an admission window"),
    (r"\bper-epoch\b", "per-admission-window"),
    (r"\b([Aa])dmission epoch\b", r"\1dmission window"),
    # admission nullifier
    (r"\bAdmission Proof nullifier\b", "admission nullifier"),
    (r"\bnullifier-duplicate\b", "admission-nullifier duplicate"),
    (r"\ba multi-nullifier circuit\b", "a circuit spending several admission nullifiers"),
    (r"\bMessage bodies remain off the ledger, including the `Misc` fallback;", "Message bodies never enter Bus Registry contract state, even on the ledger lane;"),
    (r"\bEvent bodies remain off the ledger, including the `Misc` fallback;", "Message bodies never enter Bus Registry contract state, even on the ledger lane;"),
    # Bus Operator
    (r"\bduplicate-Operator\b", "duplicate Bus Operator"),
    # rollout stages (MPS-0005 owns "Phase")
    (r"\bPhase ([0-4])\b", r"Stage \1"),
    (r"\b(launch|release|preceding|open-admission|permissioned-overlay|permissioned|open|mandatory) phase\b", r"\1 stage"),
    (r"\bGated phases\b", "Gated stages"),
    (r"\bPermissioned-phase exit\b", "Permissioned-stage exit"),
    (r"\bphase (gates?|transition|check)\b", r"stage \1"),
    (r"\bFailed phase gate\b", "Failed stage gate"),
    # Shard topics are GossipSub topics; application topics are streams
    (r"\bon a v1 topic\b", "on a v1 GossipSub topic"),
    (r"\bthe topics of both versions\b", "the GossipSub topics of both versions"),
    (r"\bevery MPE topic\b", "every MPE GossipSub topic"),
    (r"\b[Ss]hard topics\b", "Shard GossipSub topics"),
    (r"\bsubscribed topic set\b", "subscribed GossipSub topic set"),
    (r"(?<!GossipSub )\btopic it arrived on\b", "GossipSub topic it arrived on"),
    (r"\bShard-0 topic\b", "Shard-0 GossipSub topic"),
    (r"\bfield matches topic\b", "field matches GossipSub topic"),
    (r"\bbound to topic\b", "bound to GossipSub topic"),
    (r"\btopic IDs found in captured\b", "GossipSub topic IDs found in captured"),
    (r"\bcarries a topic, Tag or identifier filter\b", "carries a filter on streams, Recognition Tags or identifiers"),
    (r"\blogical topic\b", "stream"),
    (r"\bapplication topic identifier\b", "stream identifier"),
    # Recognition Tag
    (r"\b(?:private )?Tag recognition\b", "Recognition Tag matching"),
    (r"\bprivate Tag(s?)\b", r"Recognition Tag\1"),
    (r"\bTag-(match|filter)\b", r"Recognition Tag \1"),
    # Ledger Adapter is never a bridge
    (r"\bhostile bridge-input suite\b", "hostile ledger-input suite"),
    (r"\bHostile bridge inputs\b", "Hostile ledger inputs"),
    (r"\bbridge authorization\b", "ledger-interface authorization"),
]
SENTENCE_PHRASES = [  # only in the normative sentence
    (r"\bthe serving node\b", "the serving Store Node"),
    (r"\bper-node\b", "per-Bus-Node"),
]
PROTECT = re.compile(r"`[^`]*`|\"[^\"]*\"|“[^”]*”|\b(?:MPE|DEC|P)-[A-Z]{3}-\d+[a-z]?\b|\bDEC-\d{3}\b|\b(?:MIP|MPS|CoIP)-\d{4}\b")


def _nullifier(kind):
    def f(m):
        q = kind if m.group(1) == "n" else kind.capitalize()
        return f"{q} nullifier{m.group(2)}"
    return f


def _cap(word):
    return lambda m: (word[0].upper() + word[1:]) if m.group(1).isupper() else word


def vocab(text, kind="other", rid="", nullifier="admission"):
    """kind: 'sentence' (normative text), 'other' (title, verification, note, tables)."""
    if not text:
        return text
    for pat, rep in PHRASES + (SENTENCE_PHRASES if kind == "sentence" else []):
        text = re.sub(pat, rep, text)
    held = []

    def hold(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"
    t = PROTECT.sub(hold, text)
    rules = [
        (r"\b([Aa])n Event\b", lambda m: m.group(1) + " Message"),
        (r"\bEvent(s?)\b", r"Message\1"),
        (r"(?<!Recognition )\bTag(s?)\b", r"Recognition Tag\1"),
        (r"(?<!Bus )\bRegistry\b", "Bus Registry"),
        (r"\b([Aa])n Operator\b", lambda m: m.group(1) + " Bus Operator"),
        (r"(?<!Bus )\bOperator(s?)\b", r"Bus Operator\1"),
        (r"(?<!node )(?<!pool )(?<!Indexer )(?<!proof-server )\boperator(s?)\b", r"Bus Operator\1"),
        (r"(?<!admission )\b([Ee])poch(s?)\b", lambda m: ("Admission window" if m.group(1) == "E" else "admission window") + ("s" if m.group(2) else "")),
        (r"(?<![-\w])(?<!admission )(?<!consumption )(?<!Admission )(?<!Consumption )\b([Nn])ullifier(s?)\b", _nullifier(nullifier)),
        (r"(?<!GossipSub )(?<!per-)\b([Tt])opic(s?)\b(?!\s+(?:score|contribution|cap|weight))",
         lambda m: ("Stream" if m.group(1) == "T" else "stream") + m.group(2)),
    ]
    if kind == "sentence":
        rules.append((r"(?<![-\w])(?<!MPE )Envelope(s?)\b", r"MPE Envelope\1"))
    for pat, rep in rules:
        t = re.sub(pat, rep, t)
    # articles
    t = re.sub(r"\b([Aa])n (Bus|Recognition|Message|Ledger|Logical|Stage|ledger-lane|ledger|stream|Store)\b", r"\1 \2", t)
    t = re.sub(r"\b([Aa]) (MPE|admission|Admission)\b", r"\1n \2", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], t)


def nullifier_kind(r):
    text = " ".join(r.get(f) or "" for f in ("title", "sentence", "verify"))
    return "consumption" if r["id"].startswith("MPE-CON-") or "consum" in text.lower() else "admission"


def vocab_record(r):
    nk = nullifier_kind(r)
    for f in ("title", "verify", "note"):
        if r.get(f):
            r[f] = vocab(r[f], "other", r["id"], nk)
    r["sentence"] = vocab(r["sentence"], "sentence", r["id"], nk)


# ---------------------------------------------------------------- glossary (Appendix A.0)
GLOSSARY = [
    ("event", "A contract event: a typed record that a Compact circuit emits with `emit` during transaction execution, recorded in the transaction and served by the Indexer.",
     "The Foundation's term (MIP-0002, CoIP-0003), used with that meaning only."),
    ("private event", "A contract event some of whose fields are encrypted for chosen recipients and bound to the transaction by a commitment that the proof checks.",
     "The Foundation's term, planned for Phase 2 of MPS-0005 and defined by Midnight. Midnight Express can carry private events but does not define or replace them."),
    ("Message", "The application message that a Publisher seals into an MPE Envelope and delivers through Midnight Express.",
     "Not a contract event. A Message is authenticated by its Publisher's signature and committed by an Anchor, not by contract execution."),
    ("Confidential Message", "A Message for which content confidentiality, sealed labels, conditional interest privacy and no silent change hold, as defined in Chapter 4.",
     "No Foundation counterpart. It complements on-chain private events."),
    ("carried event", "A Message whose payload is the unchanged bytes of a contract event, public or private, with the hash of the recording transaction and the event's position in it.",
     "The event keeps the authority and the binding of its transaction. Carriage adds early, private delivery and is confirmed against the chain."),
    ("MPE Envelope", "The fixed-size sealed wire object that carries one Message: an 8-byte visible header, the Admission Slot and the Sealed Body.",
     "Distinct from the ledger's `VersionedLogItem`, which the Foundation's documents call a versioned envelope and which this document never calls an envelope."),
    ("Shard", "One GossipSub topic partition of the overlay.",
     "No Foundation counterpart. In MPS-0005 \"topic\" means an event filter value, so this document uses \"topic\" only as \"GossipSub topic\"."),
    ("stream", "A sealed application channel between Publishers and their audience, named only inside the Sealed Body.",
     "Unrelated to the `@topic` annotation that MPS-0005 plans for private events."),
    ("Recognition Tag", "A salted 16-byte keyed value in each MPE Envelope that lets a Subscriber recognise its Messages locally.",
     "Serves the purpose of MPS-0005 topic-based filtering by other means: it is fresh per MPE Envelope, unlinkable, and evaluated only by the Subscriber. Unrelated to domain-separation tags and to the event tag of `Misc`."),
    ("Bus Node", "A sidecar process, beside and not inside the Midnight node, that joins the GossipSub overlay and relays MPE Envelopes.",
     "Not a Midnight node: in the Foundation's documents \"node\" means `midnight-node`."),
    ("Store Node", "A Bus Node that also retains MPE Envelopes for back-fill.",
     "Stores no chain history, unlike the archival and pruned nodes of the Foundation's documents."),
    ("Publisher", "A client that seals and submits Messages.",
     "On the ledger lane, also a publisher in the sense of MIP-0019."),
    ("Subscriber", "A client that receives a Shard and recognises its own Messages.",
     "On the ledger lane, it acts as a MIP-0019 reader."),
    ("Consumer", "An agent, contract, wallet or application that acts on a Message.",
     "Narrower than the Foundation's consumer of events, which includes indexers and explorers. A contract consumes a Message only through a later transaction."),
    ("Admission Proof", "The proof in the Admission Slot that authorises one publication and enforces a rate limit.",
     "Not a transaction proof; \"proof\" alone in the Foundation's documents means the zero-knowledge proof of a transaction."),
    ("Bus Registry", "The Compact contract that holds memberships, parameters, the relay list and Anchors.",
     "Distinct from the domain-separation, name-service, token and proof-server registries of the Foundation's documents."),
    ("Anchor", "A Bus Registry state record holding the root over the MPE Envelope Identifiers of one 60-second window. A `Misc` copy is emitted as a notification.",
     "No Foundation counterpart. Verification uses the state record, because events are not consensus state."),
    ("Ledger Adapter", "The client or Bus Node interface that reads Midnight state and submits transactions.",
     "Not the node-internal ledger bridge of MPS-0007."),
    ("Indexer", "A service that reads chain data and serves it to wallets and DApps.",
     "The Foundation's definition (MPS-0028), used unchanged."),
    ("Bus Operator", "A party that runs a Bus Node, Store Node, bootstrapper, gateway or anchorer.",
     "Narrower than the Foundation's operators of nodes, stake pools and proof servers. An Indexer operator is not a Bus Operator."),
    ("ledger lane", "The explicitly selected ledger-only path that carries an MPE Envelope's Sealed Body as 1, 4 or 16 `Misc` parts.",
     "Uses the multipart transport of MIP-0019. Unrelated to the fallible phase of a transaction."),
    ("admission window", "The 60-second period over which admission quotas are counted.",
     "Unrelated to Midnight consensus and staking epochs."),
    ("admission nullifier", "The value an Admission Proof reveals when it spends one publication allowance.",
     "Unrelated to Zswap and other ledger nullifiers."),
    ("consumption nullifier", "The value a contract records when it acts on a Message, so that it acts at most once.",
     "Unrelated to Zswap and other ledger nullifiers."),
    ("Stage 0 to Stage 4", "The rollout stages of Midnight Express: models, simulation and the Prototype; permissioned pilot; permissioned production; open admission; handover.",
     "Distinct from the Phase 1 and Phase 2 of MPS-0005, which denote public and private contract events."),
    ("bond", "An optional balance held by the Bus Registry contract against misbehaviour.",
     "Unrelated to NIGHT staking, which locks nothing and carries no consensus weight."),
    ("`gossip`, `final`", "Delivery labels: `gossip` for a delivered Message not yet confirmed by the chain, `final` for a Message covered by a Bus Registry Anchor in a finalized block or verified on the ledger lane.",
     "`final` builds on the Foundation's finalization, usually about 3 blocks (about 18 s) after inclusion."),
]


def glossary_section():
    esc = lambda s: s.replace("|", "\\|")  # noqa: E731
    out = ["## A.0 Glossary {#a0-glossary}", "",
           "The table defines the terms that the requirements use and states how each relates to the usage of the Midnight Foundation's "
           "proposals. The terms \"event\" and \"private event\" keep the Foundation's meaning.", "",
           "| Term | Meaning | Relation to the Foundation's usage |", "|---|---|---|"]
    for term, meaning, rel in GLOSSARY:
        out.append(f"| {esc(term)} | {esc(meaning)} | {esc(rel)} |")
    return out + [""]


def main():
    reg = {}
    for code, _, fn in AREAS:
        for r in records((R5 / fn).read_text()):
            reg[r["id"]] = rec_from(r, "draft")
    n_draft = len(reg)
    for fx in rj["fixes"]:
        old = fx["replaces"]
        for r in records(fx["text"]):
            if fx["id"] != old and old in reg:
                reg.pop(old, None)
            reg[r["id"]] = rec_from(r, "fix")
    for g in rj["gaps"]:
        for r in records(g["text"]):
            reg[r["id"]] = rec_from(r, "gap")
    # parameters
    area_params = {}
    for code, _, fn in AREAS:
        for line in (R5 / fn).read_text().splitlines():
            m = re.match(r"^\|\s*(P-[A-Z]{3}-\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$", line)
            if m:
                area_params[m.group(1)] = {"meaning": m.group(2), "range": m.group(3)}
    covered = set()
    for p in rj["params"]:
        covered |= set(re.findall(r"P-[A-Z]{3}-\d+", p["name"]))
    n_rev = apply_revisions(reg, area_params)
    dup = {o: d["canonical"] for d in rj["duplicates"] for o in d["others"]}
    for i, c in dup.items():
        if i in reg:
            reg[i]["duplicate_of"] = c
    for i, why in WITHDRAWN.items():
        if i in reg:
            reg[i]["withdrawn"] = why
    for r in reg.values():
        vocab_record(r)
    # emit appendix
    out = ["# Appendix A. Requirements in EARS form {#appendix-a}", "",
           "This appendix lists every requirement of Midnight Express, written in EARS syntax (Easy Approach to Requirements Syntax). "
           "Each entry gives the requirement identifier, a short title, the sentence, its scope (POC for the prototype, PROD for production), its priority, "
           "whether the decision behind it is settled or open, and how it is verified; some entries add a note. "
           "Entries marked *same obligation* restate a requirement listed elsewhere; they point to the entry that owns it. "
           "The prefix MPE marks requirement identifiers and the MPE Envelope. Terms follow the Glossary in A.0.", ""]
    out += glossary_section()
    out += ["## A.1 Parameters {#a1-parameters}", "",
            "Requirements refer to tunable parameters by identifier (`P-AREA-n`). The first table gives the values chosen for the prototype and for production. "
            "The second table lists the remaining parameters with the default each requirement area assumes.", "",
            "| Parameter | Prototype value | Production value |", "|---|---|---|"]
    esc = lambda s: s.replace("|", "\\|").replace("\n", " ")  # noqa: E731
    for p in rj["params"]:
        out.append(f"| {esc(vocab(p['name']))} | {esc(vocab(p['prototype']))} | {esc(vocab(p['production']))} |")
    out += ["", "| Parameter | Meaning and default |", "|---|---|"]
    for pid in sorted(area_params, key=lambda x: (x.split("-")[1], int(x.split("-")[2]))):
        if pid not in covered:
            out.append(f"| {pid} | {esc(vocab(area_params[pid]['meaning']))} |")
    n_stat = {"total": 0, "dup": 0, "withdrawn": 0, "poc": 0, "prod": 0, "open": 0, "must": 0, "should": 0, "may": 0}
    by_area = {}
    for k, (code, title, fn) in enumerate(AREAS, 2):
        ids = sorted([i for i in reg if i.startswith(f"MPE-{code}-")], key=key)
        by_area[code] = len(ids)
        out += ["", f"## A.{k} {title} (MPE-{code}) {{#a{k}-{code.lower()}}}", ""]
        scope = area_text(R5 / fn, "Scope of this area")
        if scope:
            out += [vocab(scope), ""]
        for i in ids:
            r = reg[i]
            n_stat["total"] += 1
            if r.get("withdrawn"):
                n_stat["withdrawn"] += 1
                out += [f"**{i}** {r['title']}. *Withdrawn: {vocab(r['withdrawn'])}.*", ""]
                continue
            if r.get("duplicate_of"):
                n_stat["dup"] += 1
                owner = r['duplicate_of']
                if owner not in reg and owner + "a" in reg:
                    parts = sorted(k for k in reg if re.fullmatch(re.escape(owner) + "[a-z]", k))
                    owner = " and ".join(parts)
                    out += [f"**{i}** {r['title']}. *Same obligation as {owner}, which own it together.*", ""]
                    continue
                out += [f"**{i}** {r['title']}. *Same obligation as {owner}, which owns it.*", ""]
                continue
            n_stat["poc" if r["scope"] == "POC" else "prod"] += 1
            n_stat["open"] += r["status"] == "open"
            n_stat[r["priority"].lower()] = n_stat.get(r["priority"].lower(), 0) + 1
            tag = f"{r['scope']}, {r['priority']}, {'open: ' + r['decision'] if r['status'] == 'open' and r['decision'] else r['status']}"
            out += [f"**{i}** {r['title']}. *({tag})*  ", r["sentence"] + "  ", f"*Verification.* {r['verify']}" + ("  " if r.get("note") else "")]
            out += ([f"*Note.* {r['note']}"] if r.get("note") else []) + [""]
    (HERE / "appendix-a.md").write_text("\n".join(out) + "\n")
    (HERE / "ears-consolidated.json").write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    stats = dict(n_stat, drafted=n_draft, fixes=len(rj["fixes"]), gaps=len(rj["gaps"]), by_area=by_area,
                 params_reconciled=len(rj["params"]), params_other=len([p for p in area_params if p not in covered]),
                 decisions=len(rj["decisions"]), duplicate_groups=len(rj["duplicates"]),
                 revised=n_rev["replaced"], added=n_rev["added"], params_revised=n_rev["params"])
    (HERE / "ears-stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
