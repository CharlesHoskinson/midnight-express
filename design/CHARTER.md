# Midnight Private Events: design charter

## Goal

Design a **private event bus for the Midnight network**, inspired by Bitmessage and the decentralized
publish/subscribe literature. Events are published by some parties and consumed by **agents, smart
contracts, wallets and other roles**. The output of this exercise is a protocol specification that an
engineering team can build, test and ship in phases.

Bitmessage's idea: hide who talks to whom by letting every node carry opaque objects, with
proof-of-work admission and recipient-side recognition. Its costs are known: replicated bandwidth and
storage, weak source anonymity, static-key encryption without forward secrecy, shared-identity groups.
Later work (mixnets, private information retrieval, fuzzy detection, oblivious message retrieval,
Dandelion, GossipSub, Signal and MLS sessions) improves parts of the problem. The design must say
which of those ideas to use, which to leave out, and why.

## Decisions the protocol must settle

Every proposal answers all ten, in this order.

- **D1 Event format.** Envelope layout, which fields are visible to relays and which are sealed,
  payload types and schemas, versioning, identifiers, size classes, encoding, how long events live.
- **D2 Definition of "private".** Named properties (for example content confidentiality, publisher
  unlinkability, subscriber-interest privacy, topic privacy, timing and volume privacy,
  relationship privacy), the adversary classes each property holds against, and an explicit leakage
  table: what a relay, an indexer, a chain observer, a colluding minority and a global observer learn.
  State what is out of scope.
- **D3 Publish and subscribe model.** How topics, tags or addresses work; discovery; how a consumer
  subscribes without revealing its interest; delivery semantics (ordering, duplicates, replay,
  back-fill); how a smart contract consumes an event; how a wallet and an agent consume one.
- **D4 Sustainable model.** Who pays for publishing, carrying and storing events; spam and abuse
  resistance; operator incentives; how the model survives low and high load. Use Midnight's real fee
  and DUST mechanics where they apply.
- **D5 Performance requirements.** Throughput, latency percentiles, fan-out, concurrent subscribers,
  per-node bandwidth and CPU, for named node classes. Give numbers and show the arithmetic.
- **D6 Storage requirements.** Retention windows, per-node storage by node class, pruning,
  archival, availability guarantees, and what lives on the ledger versus off it.
- **D7 Infrastructure actors.** Who runs the network (validators, full nodes, dedicated relays,
  indexers, wallet providers, agents, third parties), how they are admitted, what they are trusted
  with, how they are paid, and the path from a launch phase to a decentralized end state.
- **D8 Network tether.** Whether the bus rides Midnight's existing node network stack, a separate
  libp2p overlay, a hybrid (ledger for anchoring and ordering, off-chain gossip for bulk), or the
  ledger and indexer alone. Recommend one, name the fallback, and say what changes in Midnight's
  node, indexer, wallet or Compact if anything.
- **D9 Threats and open risks.** The attacks that matter (eclipse, Sybil, spam, deanonymization,
  replay, censorship, key compromise, indexer abuse) and what defends each, with residual risk.
- **D10 Build and verification plan.** Phases, what to simulate or formally check before building,
  measurable acceptance criteria, and what evidence would make the team change course.

## Evidence rules

- The evidence base is local. Literature: `catalog/*.jsonl` lists every paper (field `slug`,
  `title`, `note`, `bitmessage_link`); full texts are in `pdfs/` (field `pdf_path`); slice digests
  are in `notes/`. The knowledge graph is `graphify-out/graph.json` with `GRAPH_REPORT.md`; query it
  with `graphify query "question" --graph graphify-out/graph.json`. Midnight facts:
  `notes/midnight-network-stack.md` and the code under `/home/charl/midnight/`. The Bitmessage
  analysis the project started from is `design/evidence/bitmessage-guide.md` and its review in
  `reviews/bitmessage-technical-guide-review.md`.
- **Cite every non-trivial claim.** Literature: the catalog slug (for example `2012-voulgaris-poldercast`)
  and the section or page. Midnight: `repo/path:line`. If you assert something without a source, label
  it **assumption** or **inference**. Never invent a citation, a number or a file path. If a fact is not
  in the evidence, write **unknown** and say how to find out.
- Read before you decide. Open the papers and code behind the claims you rely on; a title is not evidence.
- Midnight's documentation and code differ in places (docs describe the ledger-8 generation, the
  node code pins ledger 9). State which generation each fact comes from.

## What a good answer looks like

A decision is useful when a builder can act on it. Prefer the smallest design that meets the stated
privacy properties. Say what you reject and why. Give numbers. Say what would change your mind.
Disagreement is valuable; a vague compromise is not.

## Process

1. **Round 1, independent proposals.** Each of twelve designers writes a full proposal from the lens
   of their role, without seeing others.
2. **Round 2, cross-review.** Each designer reviews four other proposals (reviewers from other model
   vendors where possible) and records objections and votes decision by decision.
3. **Round 3, amendments and votes.** Designers see the position matrix and the objections, amend, and
   vote on each decision: **agree**, **agree with reservation** (state it), or **block** (state the
   condition that would lift it).
4. **Consensus** on a decision means no blocks and at least nine of twelve agree. Any decision without
   consensus after Round 3 goes to a short Round 4 on that decision alone. Dissent that remains is
   recorded in the specification.
5. **Specification.** One writer drafts the protocol from the settled decisions; all twelve sign off or
   state objections.

## Output format

Write Markdown. Start with a one-paragraph summary of your position. Then sections D1 to D10. End with
a table: decision, choice, rejected alternatives, evidence, confidence (low, medium or high), and what
would change your mind. Keep each section tight. Length limit for Round 1: 6,000 words.
