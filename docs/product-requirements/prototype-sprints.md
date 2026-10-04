# First three prototype sprints

This proposed plan tests whether participants can agree on a business event, recover its accepted outcome after failure and reuse that processing path in another workflow. Each sprint must supply the evidence needed for the next. Two weeks per sprint is a planning assumption; staffing and start dates are not established.

The [unified data model](unified-data-model.md) defines the proposed shared meaning. Its [reference conformance slice](../../model/README.md) already checks unsigned v0.2 events and independent RFQ interpretations, while a separate Umbra/PostgreSQL sandbox demonstrates fixture-authorized report-row recovery. These results give the sprints a starting point. The complete protocol sprints, including genuine admission and sealed transport, remain uncompleted.

## Sprint 1 — Agree on meaning. Exchange a quote.

Start with a quote because an unstated price convention can change the value of a trade. This sprint asks whether two independently specified participant formats preserve the same economics and complete intent when exchanged over the proposed transport.

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

Once participants agree on a quote, the next risk is losing or repeating its accepted outcome. This sprint tests whether duplicate delivery, crashes and reconnect preserve both the agreed meaning and the committed processing progress.

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

If recovery holds, test whether invoices and human-approved agents can use the same processing core. Each workflow keeps its own meaning and authorization rules; reuse succeeds only if the shared mechanism preserves those differences.

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

Advance when the preceding sprint supports the next experiment. Revise the design if independent mappings disagree, transaction composition fails, a domain extension changes unrelated profiles or admission compatibility remains unresolved. Repair durability before adding Sprint 3 workflows. A demo may use explicitly mocked admission, but its genuine-proof gate stays unmet. Stop automatic execution whenever authority, expiry, finality or the destination outcome is uncertain.

Every run records commit, dependency lock, host/runtime, exact configs, fixture identities, seeds, commands, expected outcomes, full failures and trace inventory. Measure sample counts and missing/late events as well as percentiles. Synthetic turnaround and integration observations are not customer ROI. Obtain participant baselines and comprehension feedback when a partner is available.

## Present evidence and remaining work

The v0.2 reference covers unsigned quotes, payment observations and sandbox approvals. Python, Rust and TypeScript agree on the finite RFQ corpus; two source-format adapters preserve the same complete fixture intent. The separate PostgreSQL sandbox commits a report row with its inbox, action, budget, outbox, checkpoint and cursor, and reconciles uncertain acknowledgement against a destination fixture. See [implementation evidence](data-format-implementation.md) for exact scope and reproduction commands. Production cryptography, real authority and finality, transport integration and destination-specific reconciliation remain work. Exploratory transport/admission/ledger experiments are not a maintained production prototype.

The sandbox demonstrates composition through Umbra's public transaction handle. Keep the existing checkpoint/cursor helper outside the composed transaction: the helper alone cannot supply this behavior and must not open a nested transaction. One writer and a local opaque replay fixture leave HA fencing and replicated retention untested.

After these sprints: authoritative finalized Midnight Registry integration, exact wire/security review, replicated opaque availability with independent receipts, WAN/load/operator-cost evidence, hardened keys and restore, and operational/security audits. Settlement additionally requires signed authority, atomic replay and CON-060 anchored-message binding. OpenMLS, mobile discovery and broad chain/ERP adapters remain separately gated. Ethereum/Solana application-domain coverage is a contract inventory first, not a promise of full RPC execution or indexer correctness.

## Design reviews

The [design reviews](../../reviews/prototype-sprints/README.md) explain the sequencing, transport, admission, recovery, SDK/model, privacy, RFQ value, workflow reuse and evidence decisions behind this plan. Proposed sprint tasks and gates are recorded in the [machine-readable plan](prototype-sprints.json).
