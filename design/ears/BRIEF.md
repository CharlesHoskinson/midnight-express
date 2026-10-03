# EARS requirements brief: Midnight Private Events (MPE)

You are drafting the requirements for one area of the Midnight Private Events bus, in EARS syntax
(Easy Approach to Requirements Syntax). Twelve authors each own one area; a merge step combines them,
so use the shared names below and stay inside your area (note cross-area dependencies instead of
writing the other area's requirements).

## The system in one paragraph

MPE is a private event bus for Midnight. Publishers send sealed, fixed-size envelopes into sharded
GossipSub v1.1 meshes run by sidecar Bus Nodes (separate from `midnight-node`). Midnight's ledger carries
membership, rate-limit roots, batch anchors and a fallback `Misc` path; event bodies never live on the
ledger. Consumers (agents, smart contracts, wallets, apps) subscribe through a client library, recognise
their events locally, and contracts react through a later transaction that proves the event. The twelve
Round 1 proposals and Round 2 reviews under `design/rounds/` record the design and its open disagreements.

## Glossary (use these terms exactly)

| Term | Meaning |
|---|---|
| MPE | Midnight Private Events, the bus as a whole |
| Event | The application message a publisher wants delivered |
| Envelope | The fixed-size sealed wire object that carries one Event across the overlay |
| Shard | One GossipSub topic partition of the overlay |
| Tag | Keyed pseudorandom value in an Envelope that lets a Subscriber recognise its Events |
| Bus Node | Sidecar process that joins the GossipSub overlay and relays Envelopes |
| Store Node | Bus Node that also retains Envelopes for back-fill |
| Publisher, Subscriber | Client roles using the MPE client library |
| Consumer | An agent, smart contract, wallet or application that receives Events |
| Admission Proof | Proof or ticket that authorises one publication and enforces a rate limit |
| Registry | Midnight contract holding memberships, parameters, relay list and anchors |
| Anchor | Batch root of recent Envelope identifiers posted to the Registry |
| Ledger Adapter | The client or Bus Node interface to Midnight, mockable for the prototype |
| Indexer | Midnight indexer (`contractEvents` subscription) used as read path or fallback |
| Operator | A party that runs a Bus Node, Store Node, anchorer or indexer |
| Prototype | The Rust proof of concept built on rust-libp2p GossipSub |

Add terms if you need them; list them in your "Glossary additions" section.

## EARS sentence patterns (every requirement uses exactly one)

| Pattern | Template |
|---|---|
| Ubiquitous | The `<system>` shall `<response>`. |
| State-driven | While `<state>`, the `<system>` shall `<response>`. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. |
| Optional feature | Where `<feature is present>`, the `<system>` shall `<response>`. |
| Unwanted behaviour | If `<unwanted condition>`, then the `<system>` shall `<response>`. |
| Complex | A combination such as `While <state>, when <trigger>, the <system> shall <response>.` |

`<system>` is one of: the MPE client library, the Bus Node, the Store Node, the Registry, the Indexer
adapter, the Prototype, or MPE (for properties of the whole bus). Use "shall" in the sentence; priority
goes in an attribute.

## Quality rules

- **Atomic.** One obligation per requirement. No "and/or". If a sentence needs "and" between two
  obligations, split it.
- **Testable.** A third party could write a pass/fail check from the sentence. Numbers carry units. Where a
  number is a tunable parameter, write it as `P-<AREA>-<n>` in the sentence, and define it in a Parameters
  table with default, allowed range, and source.
- **No weasel words.** Avoid "fast", "secure", "appropriate", "as needed", "user-friendly", "etc.".
- **Solution-neutral where the design is open; specific where it is decided.** GossipSub v1.1 is decided.
  Do not prescribe an implementation detail that the design leaves open.
- **60 words or fewer per requirement.** Put reasoning in the rationale line.
- **Honest scope.** The privacy claims are the limited ones the proposals agree on: content confidentiality,
  interest-hiding from infrastructure, no claim against a global observer, no timing or relationship
  privacy at launch. Do not write a requirement that promises more.

## Requirement record (exact format)

```
### MPE-<AREA>-<NNN> <short title>
<one EARS sentence>
- Pattern: ubiquitous | state | event | optional | unwanted | complex
- Scope: POC | PROD            (POC = the Rust prototype must demonstrate it; PROD = production target)
- Priority: MUST | SHOULD | MAY
- Source: D<n>; proposal ids (g1, s2, ...); evidence (catalog slug, section; or repo/path:line)
- Rationale: one line
- Verify: test | simulation | inspection | analysis | demonstration, plus the concrete check
- Status: settled | open (DEC-<AREA>-<n>)
```

Numbering starts at 001 in your area. Aim for 20 to 40 requirements; completeness beats count. Cover the
negative cases (what the system shall do on failure, abuse and overload) as well as normal operation.

## Open decisions

Where the proposals disagree, do not hide it. Write the requirement for the **recommended default** with
`Status: open (DEC-<AREA>-<n>)`, and add a Decisions section: for each DEC, list the options, who proposed
each (role ids), the recommended default, the reason, and the check that would settle it. A Round 3 vote
may follow; the merge step uses your recommended default for the Prototype.

## Evidence rules

Read before writing. Every requirement must trace to a proposal or review in `design/rounds/` or to a fact
in `notes/midnight-network-stack.md`, and where it relies on a number, a paper or code, cite the catalog
slug (`design/evidence/papers.tsv`) or `repo/path:line`. Mark anything unsupported as **assumption**.
Never invent a citation, number or path. If a needed fact is unknown, say **unknown** and write a
requirement to measure it. The libp2p source repositories are local under `/home/charl/libp2p/`
(rust-libp2p, specs, go-libp2p and others); cite `repo/path:line` there for GossipSub behaviour.

## Output

One Markdown file, in this order: (1) "Scope of this area" (3 to 6 lines); (2) Parameters table;
(3) Requirements; (4) Decisions; (5) Cross-area dependencies (requirement IDs you expect from other areas);
(6) Glossary additions; (7) Gaps: design statements you could not turn into a testable requirement, and why.
No process narration. Your final message is the file content.
