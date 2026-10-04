# Evidence and investment decisions for three prototype sprints

Status: proposed acceptance protocol, 2026-10-03. No prototype run, customer result or proof benchmark is reported here. Read alongside [sequence](sequence.md), [RFQ product validation](rfq-product.md), [recovery](recovery.md), [privacy](privacy.md) and [event contracts](../data-model/event-contracts.md). Three two-week timeboxes are planning assumptions.

The decision is whether to fund the next bounded experiment. Keep separate verdicts for shared meaning/product, transport/privacy, durable processing and genuine admission/platform feasibility. A green RFQ demonstration cannot cancel a red proof gate. Before each sprint, name an owner and independent reviewer for each verdict, freeze its scope and thresholds, and identify which failures prohibit the next claim.

## A repeatable evidence packet

Each sprint produces a private run bundle and a redacted index. The index links gate IDs to expected outcomes, observed outcomes, commands, artifact hashes, failures and limitations. Raw keys and plaintext ground truth belong only in protected local artifacts; never include production credentials. Record:

- Exact repository commits and dirty diff, dependency locks, compiler/runtime/validator versions, build flags, OS/kernel, CPU/VM, memory, affinity, database and transport configuration. Pin circuit/proving material and its provenance, Registry/network context, schema closure, semantic manifest, reference data, adapter and signing-policy digests.
- Fixture generator version, explicit seeds, immutable input bytes/hashes, actor/role configuration, equal-key-count interest configurations, clock/expiry policy, publication order, concurrency, fault schedule and run count. Seeds make fixtures reproducible; they do not make OS scheduling deterministic. Use synthetic test keys and preserve recorded schedules for replay.
- Executable clean-setup, run and inspection commands, required permissions, actual exit status and capture coverage. Missing prerequisites and skipped checks are **blocked**, never passed. A clean checkout replay by the independent reviewer must reproduce the same semantic verdicts, wire vectors and durable invariants; timing distributions may vary within the declared experiment.
- Per-test provenance: synthetic or customer source, mock or real transport/storage, stand-in or genuine proof, simulator or authoritative network. Distinguish proposed, executed-pass, executed-fail and blocked from these implementation labels. Retain failed and abandoned runs; changes to acceptance policy create a new protocol revision rather than retroactively passing old runs.

Use four distinct commitments: original envelope bytes/EID, full-envelope GossipSub message ID, canonical business assertion and exact contract-bundle digest. Event `(source,id)`, business `actionId` and destination idempotency keys have separate scopes. Preserve these mappings in the evidence oracle instead of treating one transport hash as proof of every identity.

## Sprint 1 — establish meaning and expose proof risk

**Required packet:** one buyer/two-dealer RFQ scenario; two independently authored source conventions and field-level mappings; independently calculated expected asset/cash obligations; Rust/TypeScript wire and canonical-assertion vectors; actual sidecar/topic/log traces; semantic rejection results; a genuine-proof compatibility report or explicit failed attempt.

Buyer-side purchase/shares/USD-per-share and dealer-side sell/lots/USD-per-lot are useful distinct fixtures. Separate owners specify expected obligations before comparing outputs. Two generated serializers of one canonical struct do not count. Compare exact units, buyer/seller perspective, denominator, fees, validity, reference data and signed offer revision across source mappings, trusted displays and executors. A terms hash match without obligation equivalence fails.

Run independent Rust and TypeScript checks on original wire/EID/message-ID vectors and JCS signed assertions, with a separately reviewed oracle. Cross-implementation agreement alone cannot exclude a shared specification mistake. Include escaped duplicate keys, unsafe numbers, invalid Unicode, UTF-16 property sorting, timestamp variants, nested unknown fields, unsupported vocabularies, default insertion, unknown contracts and remote-reference traps. Require typed rejection, no effect and protected quarantine where applicable. Domain negatives include reversed side, wrong asset/currency/scale, missing lot multiplier or fee, changed revision, indicative offer, unauthorized signer, expiry and competing acceptance.

Privacy evidence requires complete controlled-endpoint captures plus canaries and intentional leak detection. A scanner must detect an injected schema fetch and match-triggered receipt before its clean result is credible. Plain encrypted packet capture or static code review alone is preliminary. Observe actual whole-shard carriage; private operation/profile names must not become topics, selectors or diagnostics.

**Go:** the supported synthetic obligations agree, negative cases fail safely, wording clearly states off-chain acceptance, and real carriage/privacy evidence supports only its declared boundary. Continue local recovery work with any admission mock visible.

**Revise:** mapping/display errors, incomplete cross-language vectors or blocked capture coverage require a smaller slice and rerun before broader product/privacy claims. An unresolved genuine-proof path gets a named compatibility experiment and budget before workflow breadth grows.

**Stop the affected claim:** a lossy economic conversion authorizes an effect, infrastructure sees a private selector, or the required proof relation has no credible compatible path within agreed constraints. Preserve the negative evidence; do not replace anonymous admission with a secret-readable verifier.

## Sprint 2 — require durable and privacy oracles

**Required packet:** the [recovery fault matrix](recovery.md#crash-and-fault-matrix), public transaction-call map, actual PostgreSQL durability/session settings, protected inbox/outbox records, receiver result ledger and paired recognition traces. Inspect the complete durable vector, not only restored checkpoint bytes.

Inject failures after every participant write before commit, during uncertain COMMIT, after commit before dispatch and after receiver success before local confirmation. Include abrupt database termination, unsafe durability on pooled/reconnected sessions, concurrent duplicates/competing offers, conflicts, expiry between validation and commit, source gaps, poisoned handlers and explicit redrive. Every recovered transaction must be wholly old or wholly new; processing progress cannot pass an uncommitted effect. An acknowledgement must describe committed terms, and remote completion must remain uncertain until reconciled.

Replay the same action under a new event and resealed EID, across profile upgrades and an older checkpoint against newer guards. Require one local result with stable replay scope; changed action digest conflicts. Full database rollback without trusted freshness remains blocked for secure restore. Enforce the one-writer boundary; cooperative leases do not prove fenced failover. Verify SQLite separately if used.

For privacy, swap only local interests with application publications disabled; retain A/A baselines, fixed-schedule comparisons and at least five live pairs per selected scenario. Capture decoded control/HTTP fields, logs and caches. Report omissions, timing residuals and documented normalization. A recognition-dependent request, control decision or repeatable unexplained difference fails or blocks the gate. Admission stays a separate verdict.

**Go:** required transaction/duplicate/durability cases pass without skips, gaps and uncertain remote outcomes remain explicit, and the tested privacy boundary passes. Authorize reuse only within the authoritative single-host scope.

**Revise:** missing fault coverage, unsupported public transaction composition or unexplained privacy differences take priority over Sprint 3 breadth. Blocked anti-rollback evidence constrains the restore claim rather than inventing a pass.

**Stop automatic effects:** a cursor skips a lost effect, a consumed action executes again, unsafe durability is accepted, or ambiguous destination success is blindly retried without idempotency/query support. Repair and rerun before resuming automatic execution.

## Sprint 3 — test reuse, then decide the next investment

**Required packet:** one invoice-status fixture and one human-approved sandbox action through the same core, named domain policies, added adapter/code/engineering effort, the reused crash harness, explicit-action privacy captures and an admission disposition.

Invoice evidence must reject wrong issuer/invoice/amount/currency, stale versions and untrusted/provisional payment claims. A signed synthetic notice proves source assertion only. Inject destination success followed by lost local confirmation: durable destination idempotency/query returns the prior result, or automatic retry stops for manual reconciliation. No payment executes.

Approval evidence binds exact proposal/action, destination, budget/units, expiry and application/network domain. Reject changed target, excess budget, replay, denied/revoked/expired approval and narrative instructions to bypass policy; recheck authority at execution after restart. A deterministic proposer suffices. Reuse does not mean inventing a universal economic/authority object.

Backfill privacy evidence must include unrecognized pages, expiry gaps, crashes and failover without narrowing inventories or stopping pagination at no-match pages. Keep deliberate signed business acknowledgements in a separate authorized-action scenario: captures must link each publication to independent authorization and durable action consumption. Its observable timing/volume remains a stated limit.

**Go to a constrained partner evaluation:** the reuse and safety gates pass, supported product/trust boundaries and remaining blockers are explicit, and a customer owner or plan exists. Compare task comprehension, handling time and integration effort with a declared baseline; synthetic observations cannot establish savings, demand or ROI. An admission-red evaluation remains visibly mock-based and cannot claim anonymous admission.

**Revise:** repeat failed core work, reduce destination/adapter scope or commission circuit/platform work. Record owner, next experiment, cost assumption and stopping condition for every unresolved gate.

**Stop the proposed pilot claim:** no feasible way preserves its required privacy, business authority, durable outcome or genuine admission assurance within the agreed constraints. This stops that scope; a narrower internal experiment requires a separately stated decision.

## MPE-ECO048: predeclared prototype feasibility gate

Start in Sprint 1 and disposition by Sprint 3. Use an actual content-bound membership/quota proof with the selected field/hash/tree/Registry relation and canonical network/window/class/index scopes. Test substitution, excess credit, stale/revoked roots, root-change quota non-renewal and restart-safe duplicate/conflict handling. A stand-in, unrelated membership proof, circuit compilation or mock ledger cannot pass this gate. Finalized-root/witness integration must name its actual network evidence or remain blocked.

Measure the actual encoded Admission Slot, including 104 bytes of fixed fields and padding: **`roundUp64(104 + proof_length) <= 4096`**. This allows at most 3,992 proof bytes under this layout. Preserve the exact selected wire profile; the ceiling does not permit enlargement of another fixed field or omission of required statement inputs.

Before measurement, freeze a conservative policy: **10,000 genuine valid proofs, one core of a 4-vCPU VM, median and p99 reported, p99 <= 10 ms required**. Define p99 as the nearest-rank 9,900th sorted observation, timed around the pinned adapter decode/verification path; disclose warmup, cold results, corpus diversity, CPU affinity, VM contention, failures and raw observations. Do not discard failures or slow samples to improve the percentile. Measure malformed/invalid-input cost separately. Report proof generation, witness updates, memory and load behavior separately from verification. A different host or incomplete relation gives candidate evidence only. No current measured performance is asserted here.

Passing this prototype gate is necessary for the selected feasibility claim, not sufficient for production. Independent cryptographic review, authoritative finalized-root integration, hardened key/restore controls, replicated opaque retention/operator receipts, WAN/load/economics and operations remain separate gates. These sprints establish neither ingress/timing anonymity, forward secrecy, mobile private retrieval, settlement/CON-060 readiness nor unrestricted agent execution.
