# First three prototype sprints

Status: proposed validation plan, synthesized from ten independent design reviews. Two weeks per sprint is a planning assumption; staffing and start dates are not established. These are dependency gates, not a six-week launch promise.

Shared meaning is the first hypothesis. See [unified data model](unified-data-model.md) and [reference conformance slice](../../model/README.md).

## Sprint 1 — Agree on meaning. Exchange a quote.

Hypothesis: Two independently specified participant formats can mean exactly the same trade, without guessed defaults.

Build:

- Closed RFQ contract and two deterministic source adapters; independent Rust/TypeScript interpretation.
- A buyer and two dealers on actual whole-shard GossipSub, with typed requests, offers and off-chain acceptance.
- Start genuine admission and finalized Registry feasibility immediately; label any mock boundary.

Demo: 100 shares at 123.45 USD per share maps identically from two declared price conventions. An expired offer, wrong role or missing price basis fails.

Required evidence:

- Equal canonical economics and intent commitments across implementations; ambiguous mappings reject.
- Independent wire vectors; trace inspection finds no RFQ topics or upstream business selectors.
- Candidate proof compatibility and actual encoded size/verification report, or a named blocking mismatch.

## Sprint 2 — Recover without changing the outcome.

Hypothesis: The same accepted meaning and durable progress survive duplicate delivery, crashes and reconnect.

Build:

- Compose authenticated inbox, dedup, local effect, outbox, checkpoint and cursor in one UmbraDB/PostgreSQL transaction.
- Persistent opaque replay fixture, bounded retries, encrypted quarantine and explicit gap handling.
- Carry pinned semantic contracts through restart and replay; continue proof, root and privacy checks.

Demo: Kill the host before commit, after commit before acknowledgement and during outbox delivery. Replay and restore one accepted record, with no cursor beyond an uncommitted effect.

Required evidence:

- Real process/crash fault matrix; same business action with a new EID cannot duplicate the effect.
- Expired redrive, wrong restore context and unsupported contract cannot become actionable.
- Paired recognition traces show no subscription-dependent acknowledgements or schema fetches.

## Sprint 3 — Reuse the core. Test the investment case.

Hypothesis: Invoices and human-approved agents can reuse the core without a universal business schema or unsafe inferred authority.

Build:

- Restricted invoice/payment observations with pending, partial, final and reversed evidence; no payment execution.
- Separate proposal, approval, execution request and result contracts for one human-approved sandbox action.
- Reuse fault harness and measure adapter effort; evaluate chain-domain profiles without treating indexer observations as authority.

Demo: A payment fixture cannot become paid by changing its status. A changed target, expired approval, excess budget or repeated action is rejected. Uncertain remote completion goes to reconciliation.

Required evidence:

- Both workflows retain their domain rules through the same durable core.
- Destination idempotency or explicit reconciliation prevents unsafe automatic retries.
- Reproducible decision pack: observed results, integration cost, proof status and unresolved production gates.

## Cross-sprint admission gate

Start this work in Sprint 1. A genuine membership/class-credit/EID-bound abuse proof must use compatible identity commitment, field/hash, tree, scope and codec. Scope excludes EID and current root so a reseal or root change cannot renew quota. One proof combines the required claims; a separate per-event Semaphore proof is not the recommendation.

MPE-ECO-048 is a **prototype measurement gate**: encoded slot `roundUp64(104 + proofBytes) <= 4096`; benchmark 10,000 genuine proofs on one core of a 4-vCPU VM and report median/p99. Predeclare p99 <= 10 ms as conservative project acceptance policy. The original requirement does not specify that percentile. A stock library benchmark is not the candidate relation benchmark. A <=4096 ceiling does not establish fit in the existing fixture's fixed 512-byte slot. Changed wire profiles require explicit revision and independent vectors. Finalized Registry roots, revocation and witness update need actual environment evidence; compilation or a mock is insufficient.

## Decision protocol

Continue only the claims supported by evidence. Revise when independently mapped meanings differ, atomic transaction composition fails, domain extensions contaminate unrelated profiles, or admission compatibility is unresolved. Stop automatic execution where authority, expiry, finality or destination outcome is uncertain. Blocked durability is repaired before Sprint 3 breadth; a functional mocked demo may proceed while its genuine admission verdict remains red.

Every run records commit, dependency lock, host/runtime, exact configs, fixture identities, seeds, commands, expected outcomes, full failures and trace inventory. Measure sample counts and missing/late events as well as percentiles. Synthetic turnaround and integration observations are not customer ROI. Obtain participant baselines and comprehension feedback when a partner is available.

## Present evidence and remaining work

The repository has a Python-only unsigned three-event reference conformance slice. It does not have the three completed sprints. Adapters, Rust/TypeScript agreement, cryptography, real permissions/finality, durable processing and destination reconciliation remain work. Current exploratory transport/admission/ledger experiments are not a maintained production prototype.

Umbra's existing checkpoint/cursor helper alone does not provide the proposed atomic composition: test public transaction-handle composition, with no nested transaction. One writer and a local opaque replay fixture do not establish HA fencing or replicated retention.

After these sprints: authoritative finalized Midnight Registry integration, exact wire/security review, replicated opaque availability with independent receipts, WAN/load/operator-cost evidence, hardened keys and restore, and operational/security audits. Settlement additionally requires signed authority, atomic replay and CON-060 anchored-message binding. OpenMLS, mobile discovery and broad chain/ERP adapters remain separately gated. Ethereum/Solana application-domain coverage is a contract inventory first, not a promise of full RPC execution or indexer correctness.

## Design reviews

Ten reviewers covered sequencing, transport, admission, recovery, SDK/model, privacy, RFQ product value, workflow reuse, evidence decisions and page experience. Their original reviews are in [reviews/prototype-sprints](../../reviews/prototype-sprints/README.md). Machine-readable plan: [prototype-sprints.json](prototype-sprints.json).
