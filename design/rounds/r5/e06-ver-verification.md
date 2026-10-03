## Scope of this area

VER defines the evidence, test suites, phase gates and acceptance reports required for the Rust Prototype and subsequent MPE releases.
It covers local multi-node demonstrations, bounded models, simulations, adversarial workloads, Midnight integration and production acceptance.
It verifies the behavior specified by other areas without selecting their cryptographic, admission, storage or mesh designs.
A passing experiment supports only its recorded configuration, workload and adversary model.
D10 remains open where proposals disagree; the recommended defaults below govern Prototype acceptance pending review.

## Parameters

All numerical defaults below are proposed acceptance targets, **not measured MPE capabilities**. Sources identify their origin; adaptations are marked **assumption**. Changing a default creates a new acceptance profile and does not retrospectively pass a failed run.

| Parameter | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-VER-1 | Local Bus Node count | 16 Bus Nodes | Integer ≥ 16 Bus Nodes | g1 R1 D10 |
| P-VER-2 | Nominal offered load, per tested Shard | 10 Envelopes/s | Positive finite Envelopes/s | s4 R1 D5/D10; per-Shard application is an **assumption** |
| P-VER-3 | Nominal soak duration | 72 h | ≥ 72 h | s4 R1 D10 |
| P-VER-4 | Burst offered load, per tested Shard | 100 Envelopes/s | ≥ P-VER-2 | s4 R1 D5/D10; per-Shard application is an **assumption** |
| P-VER-5 | Burst duration | 60 s | ≥ 60 s | s4 R1 D10 |
| P-VER-6 | Nominal post-admission delivery deadline | 10 s | Positive finite seconds | g1, o1, s4 R1 D10/D5; recommended in DEC-VER-2 |
| P-VER-7 | Nominal timely delivery fraction | 0.999 | [0.999, 1] | s4 R1 D10; denominator defined below |
| P-VER-8 | Simulation sizes | 50, 200, 1,000 Bus Nodes | Finite integer set containing these sizes | g2 R1/R2 D10 |
| P-VER-9 | Additional sustained offered load | 50 Envelopes/s per tested Shard | ≥ P-VER-2 | g1 R1 D10; o1 R1 D10 |
| P-VER-10 | Additional sustained run duration | 24 h | ≥ 24 h | o1 R1 D10 |
| P-VER-11 | Adversarial Bus Node shares | 1%, 3%, 5%, 20% | Finite set containing these shares | s3 R1 D10; g2 R1/R2 D10 |
| P-VER-12 | First-spy coalition shares | 5%, 10%, 20% | Finite set containing these shares | o1, o4 R1 D10 |
| P-VER-13 | Recovery chaos workload | 1,000,000 Events | Integer ≥ 1,000,000 Events | o3 R1 D10 |
| P-VER-14 | Decoder fuzz campaign size | 1,000,000,000 iterations | Integer ≥ 1,000,000,000 iterations | o3 R1 D10 |
| P-VER-15 | Post-burst queue recovery deadline | 60 s | Positive finite seconds | **Assumption** making s4’s “queues recover” gate measurable |
| P-VER-16 | Admission attack identity count | 1,000 admission identities | Integer ≥ 1,000 identities | o1 R1 D10 |
| P-VER-17 | Contract-reaction concurrency | 100 concurrent reactors | Integer ≥ 100 reactors | o3 R1 D10 |
| P-VER-18 | Outside developers in usability trial | 5 developers | Integer ≥ 5 developers | o3 R1/R2 D10 |
| P-VER-19 | Successful usability completions | 4 developers | Integer from 4 to P-VER-18 | o3 R1/R2 D10 |
| P-VER-20 | Usability completion deadline | 4 h per developer | Positive finite hours | o3 R1/R2 D10 |
| P-VER-21 | Production canary observation window | 30 consecutive days | ≥ 30 days | o4 R1 D10 |
| P-VER-22 | Production canary timely delivery fraction | 0.999 | [0.999, 1] | o4 R1 D10 |
| P-VER-23 | Production canary delivery deadline | 5 s | Positive finite seconds | o4 R1 D10 |
| P-VER-24 | Pause-to-resume drill deadline | 1 h | Positive finite hours | o4 R1/R2 D10 |
| P-VER-25 | Non-partitioned adversarial timely delivery fraction | 0.99 | [0.99, 1] | g2 R1/R2 D10; using P-VER-6 as its deadline is an **assumption**, DEC-VER-2 |

Resource ceilings, Envelope classes, retention, Shard counts and GossipSub parameters come from the frozen PRF, FMT, STO and NET acceptance profile. Their numerical values are **unknown in this area** until those records are merged. Missing ceilings prevent resource acceptance.

## Requirements

### MPE-VER-001 Reproducible acceptance profile

The Prototype shall attach a reproducible acceptance profile to every acceptance run.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; s4 R1/R2; o3 R2; `midnight-node/Cargo.lock:7894`
- Rationale: Results require an identifiable implementation and workload.
- Verify: inspection, check source revisions, dependency lock, build flags, hardware, topology, transport, mesh/scoring configuration, workload, parameter values, random seeds, clock policy, commands and fixture hashes.
- Status: settled

### MPE-VER-002 Claim register

MPE shall maintain an evidence record for each advertised privacy or capacity claim.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; s4 R1/R2; o3, o4 R2
- Rationale: A component citation does not establish a claim about the assembled service.
- Verify: inspection, require claim wording, source revision, deployment generation, checked scope, assumptions, contradictory evidence, reproduction procedure and applicable acceptance results.
- Status: settled

### MPE-VER-003 Failed phase gate

If a mandatory phase check fails or lacks evidence, then the Prototype shall mark that phase gate as failed.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D10; g2, s4, o4 R1; o1 R2
- Rationale: Feature completion cannot substitute for acceptance evidence.
- Verify: test, inject failed, skipped, missing and timed-out mandatory checks; confirm none produces a passing gate.
- Status: open (DEC-VER-1)

### MPE-VER-004 Wire conformance

The Prototype shall pass the frozen Envelope conformance suite before multi-node acceptance.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g1, g4, s2 R1; s4 R2
- Rationale: Framing and binding defects precede transport evaluation.
- Verify: test, compare exact expected outcomes for valid vectors, incorrect lengths, unsupported versions, non-canonical encodings, malformed fields and applicable padding violations; include cross-implementation vectors supplied by FMT and CRY.
- Status: settled

### MPE-VER-005 Decoder fuzzing

The Prototype shall complete P-VER-14 fuzz iterations without a crash in the Envelope and application-payload decoders.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o3, s3 R1; g1 R1 D9/D10
- Rationale: Unauthenticated parsing remains an attack surface regardless of payload encryption.
- Verify: test, retain campaign configuration, iteration counts, sanitizer results and regression corpus; count only executions reaching a decoder, with coverage reported separately.
- Status: open (DEC-VER-3)

### MPE-VER-006 Actual cryptographic costs

The Prototype shall report measured wire size and execution-time distributions for every cryptographic operation on its selected publication path.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g3, o1, o2, s2 R1; g1, g2, s2 R2
- Rationale: Midnight cost weights and literature microbenchmarks are not Prototype measurements.
- Verify: test, benchmark sealing, recognition, Admission Proof generation and validation on named reference hardware; include serialization, caching conditions, batch sizes, p50, p95, p99 and sample counts.
- Status: settled

### MPE-VER-007 Admission model

The Prototype shall pass bounded exploration of the selected admission state machine without a violation of its frozen safety invariants.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g1, g2, g3, s3 R1; s1, s2, s4 R2
- Rationale: Admission safety includes transitions and recovery, not only proof verification.
- Verify: analysis, explore allowance boundaries, root replacement, expiry, revocation, restart, rollback and conflicting bodies; check message binding, scoped replay rules and absence of allowance resets.
- Status: open (DEC-VER-4)

### MPE-VER-008 Delivery-state model

The Prototype shall pass bounded exploration of the client delivery state machine without a violation of its frozen cursor and deduplication invariants.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o3 R1/R2; s4 R1; s2 R2
- Rationale: Correct mesh propagation does not establish correct consumer recovery.
- Verify: analysis, explore inclusive cursors, crash points, reconnect, failover, withheld suffixes and gap closure; check that committed progress never skips an undelivered recoverable Event.
- Status: settled

### MPE-VER-009 Contract-consumption model

The Prototype shall pass bounded exploration of the contract-consumption model without an unauthorized or duplicate contract effect.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o1, s1, s3, s4 R1; s1, s4 R2
- Rationale: An Anchor alone does not establish application authorization.
- Verify: analysis, explore incorrect leaves, destinations, networks, expiry, missing Anchors, replay-state pruning and concurrent consumption; model the CON authorization predicate explicitly.
- Status: settled

### MPE-VER-010 Governance model gate

Where Registry governance features are present, MPE shall pass bounded exploration of their frozen governance invariants before production acceptance.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D10; o4, o2 R1; s4 R2
- Rationale: Only selected governance features require corresponding models.
- Verify: analysis, check applicable delayed changes, emergency expiry, threshold transitions, pause states, Anchor takeover and fund-conservation rules; record disabled features explicitly.
- Status: open (DEC-VER-4)

### MPE-VER-011 Local multi-node demonstration

The Prototype shall demonstrate Publisher-to-Subscriber Event delivery through P-VER-1 separate local Bus Node processes using rust-libp2p GossipSub v1.1.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g1 R1; g2 R1; g4 R1; BRIEF system definition
- Rationale: A single-process callback demonstration does not exercise the overlay.
- Verify: demonstration, publish every selected Envelope class across tested Shards; confirm matching Subscribers recover exact Events and nonmatching Subscribers produce no false opens; use a declared mock Ledger Adapter.
- Status: open (DEC-VER-1)

### MPE-VER-012 Nominal soak

The Prototype shall complete a nominal acceptance run at P-VER-2 for P-VER-3 without an unplanned process termination.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; s4 R1; g4 R1; s3 R1
- Rationale: A continuous run exposes leaks and accumulating state.
- Verify: test, use the local multi-node topology, real elapsed time and frozen Envelope mix; report offered, admitted and rejected rates separately.
- Status: open (DEC-VER-2)

### MPE-VER-013 Nominal latency

While the nominal acceptance workload is running, the Prototype shall achieve a post-admission delivery p99 no greater than P-VER-6.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D10; g1, o1 R1; s4 R1 D5/D10
- Rationale: Hot-path latency must exclude separately measured admission and ledger delays.
- Verify: test, measure first valid delivery for each expected Subscriber; publish the completion percentile and missing-delivery count under the measurement convention below.
- Status: open (DEC-VER-2)

### MPE-VER-014 Nominal delivery fraction

While the nominal acceptance workload is running, the Prototype shall deliver at least P-VER-7 of eligible Envelope–Subscriber pairs within P-VER-6 after admission.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D10; s4 R1; o1 R1; s4 R2
- Rationale: A latency percentile over successful deliveries can conceal omissions.
- Verify: test, derive the denominator from generated accepted Envelopes and scheduled honest Subscribers; count each pair once, including pairs that never complete.
- Status: open (DEC-VER-2)

### MPE-VER-015 Resource acceptance

If a measured resource exceeds its frozen PRF or STO acceptance ceiling, then the Prototype shall fail resource acceptance.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D10; g1, g3, s1, s3, s4 R1; g3 R2
- Rationale: Resource budgets depend on node class, Envelope mix and retention.
- Verify: test, check CPU, memory, ingress, egress, queue/cache occupancy, retained bytes, storage amplification and recognition cost against declared ceilings; an undefined ceiling yields an incomplete gate.
- Status: settled

### MPE-VER-016 Measurement report

When an acceptance run ends, the Prototype shall produce a measurement report using the measurement convention below.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10; g1, g3, o1, s3, s4 R1; s4 R2
- Rationale: Comparisons require consistent denominators and complete failure accounting.
- Verify: inspection, check latency distributions, admission outcomes, delivery coverage, transport amplification, resource time series, recovery results and raw artifact references.
- Status: settled

### MPE-VER-017 Scale simulations

The Prototype shall produce scale-evaluation results at every Bus Node count in P-VER-8.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g2, o1 R1; g2 R2; `2024-revuelta-waku-latency`, §§4.1–4.2
- Rationale: Local success does not establish scale behavior.
- Verify: simulation, exercise nominal load, P-VER-9 for P-VER-10, bursts, cold starts and overload; incorporate measured validation delay and the NET topology; disclose simulator limitations and compare overlapping cases with the real binary.
- Status: open (DEC-VER-2)

### MPE-VER-018 Adversarial dissemination gate

While a non-partitioned adversarial acceptance run is active, the Prototype shall achieve a timely honest delivery fraction of at least P-VER-25 within P-VER-6.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D10; g2, s3 R1; g2 R2
- Rationale: Random peer fractions alone do not exercise targeted capture.
- Verify: simulation, use P-VER-11 shares at each P-VER-8 size; test targeted outbound placement, poisoned discovery, Sybil-heavy joining, selective dropping, concentrated bandwidth and synchronized Publishers; report every case separately.
- Status: open (DEC-VER-2)

### MPE-VER-019 Admission abuse gate

The Prototype shall accept zero publications violating the selected admission policy during an attack using P-VER-16 admission identities.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o1, s3 R1; s2, s4 R2
- Rationale: Per-identity correctness differs from aggregate Sybil capacity.
- Verify: test, submit over-quota, forged, expired, wrong-network, revoked and conflicting-body publications across epoch boundaries and restarts; account for valid aggregate allowances separately.
- Status: settled

### MPE-VER-020 Validation outcome conformance

The Prototype shall pass the validation outcome suite for the frozen Accept, Reject and Ignore policy.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g2 R1/R2; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:930`; `rust-libp2p/protocols/gossipsub/src/types.rs:51`
- Rationale: Invalid-content penalties differ from ignoring unsupported or indeterminate input.
- Verify: test, compare forwarding and score effects with the selected policy; include validation timeout and cache eviction; verify application validation is enabled because the inspected configuration defaults to automatic forwarding.
- Status: settled

### MPE-VER-021 Invalid-ingress bounds

While invalid-ingress saturation is active, the Prototype shall keep each queue and cache within its declared capacity.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D10; s3, s4 R1; s4 R2
- Rationale: A low invalid-ingress percentage is not proof of flood resistance.
- Verify: test, saturate malformed frames, invalid Admission Proofs, repeated identifiers and control traffic; sample capacities and memory through overload and recovery; report verification CPU separately.
- Status: settled

### MPE-VER-022 Burst recovery

When a P-VER-4 burst lasting P-VER-5 ends, the Prototype shall restore every monitored queue to its pre-burst nominal bound within P-VER-15.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10; s4 R1; recovery deadline is an **assumption**
- Rationale: Bounded instantaneous queues can still hide persistent backlog.
- Verify: test, establish bounds during a stable nominal interval before the burst; continue nominal load afterward and measure the first sustained return within those bounds.
- Status: open (DEC-VER-2)

### MPE-VER-023 Recovery completeness

The Prototype shall recover every eligible Event in the P-VER-13 recovery chaos workload.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o3 R1/R2; g4, s3, s4 R1
- Rationale: Recovery must cover client state and alternative read paths.
- Verify: test, inject client crashes, Bus Node and Store Node restarts, partitions and Indexer failover where present; compare the recovered Event set after recovery with the authoritative fixture set.
- Status: settled

### MPE-VER-024 Atomic consumer deduplication

Where an atomic effect store is present, the Prototype shall produce at most one committed handler effect per Event in the recovery chaos workload.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D10; o3 R1/R2; s2 R2
- Rationale: Deduplication alone cannot provide exactly-once external effects.
- Verify: test, crash between receive, effect commit and cursor commit; inject replay through overlay, back-fill and fallback; count committed effects independently of callback attempts.
- Status: settled

### MPE-VER-025 Store failure recovery

When one Store Node fails while another honest holder remains reachable, the Prototype shall recover all requested eligible Envelopes within the selected retention window.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10; s3, s4 R1; g4 R1; o1 R1 D6
- Rationale: Availability is conditional on surviving holders, not on an Anchor.
- Verify: test, fail the initially selected Store Node, back-fill from another holder and compare identifiers and bytes; repeat near expiry and report unavailable expired ranges.
- Status: settled

### MPE-VER-026 Scoring attack regression

The Prototype shall fail network acceptance if the selected GossipSub scoring configuration reproduces a registered scoring safety violation.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g2 R1/R2; s2, s4 R2; `2023-kumar-gossipsub-acl2s`, §§3–5
- Rationale: A changelog entry cannot establish safety of application-specific scoring.
- Verify: test, register the relevant CVE-2022-47547 attack traces and MPE-specific score counterexamples; exercise multi-Shard reward/penalty interactions, targeted dropping and the NET outbound-quota policy.
- Status: settled

### MPE-VER-027 First-spy measurement

The Prototype shall report first-spy precision and recall for every coalition share in P-VER-12.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o1, o4 R1; s1, s4 R2; `2018-fanti-dandelionpp`, §§3.2–3.3, Theorem 1
- Rationale: Attribution experiments quantify leakage under a stated model.
- Verify: simulation, compare direct publication with any selected ingress mechanism on identical workloads; report topology, placement, load, estimator, sample counts and uncertainty, including idle and targeted cases.
- Status: open (DEC-VER-5)

### MPE-VER-028 Interest-swapped executions

The Prototype shall produce identical infrastructure-visible retrieval traces for paired executions differing only in Subscriber interests under identical connection and retrieval schedules.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; s1, s4 R1; g4, s1 R2; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:548`
- Rationale: Local recognition must not create an interest-dependent retrieval action.
- Verify: test, compare requests, cursors, requested ranges, volumes and scheduled timing; include malformed matching Envelopes, withheld suffixes, reconnect, repair, acknowledgements and backpressure.
- Status: settled

### MPE-VER-029 Infrastructure log audit

The Prototype shall pass a log audit with zero occurrences of fixture Event plaintext in Bus Node or Store Node logs.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o4 R1; s1, s4 R1
- Rationale: Confidentiality tests must include diagnostics and failure paths.
- Verify: test, publish unique plaintext canaries, trigger parsing, validation and storage errors, then scan logs and diagnostic exports; CRY and PRV separately define secret-field exclusions.
- Status: settled

### MPE-VER-030 Ledger integration measurements

The Prototype shall report measured transaction costs and timing for each selected ledger operation on the integration test network.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; g1, g3, g4, o1, o3, s4 R1
- Rationale: Mock adapters cannot measure DUST, transaction serialization or finality.
- Verify: test, record serialized bytes, applicable cost dimensions, live ledger parameters, DUST charge, proving, submission, inclusion, finality and indexing times; distinguish registration, Anchor and consumption operations.
- Status: settled

### MPE-VER-031 Concurrent Anchor validity

The Prototype shall demonstrate successful valid consumption against an eligible Anchor despite intervening Anchor insertions.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o1 R1; o1 R2; `minokawa-compact/doc/ledger-adt.mdx:607`
- Rationale: Concurrent publication can invalidate a proof unless the selected root-history policy supports it.
- Verify: test, prepare a valid consumption proof, insert later Anchors, then submit the original proof within the CON acceptance window; separately reject roots outside that window.
- Status: settled

### MPE-VER-032 Contract reaction race

The Prototype shall demonstrate exactly one authorized contract effect when P-VER-17 concurrent reactors submit valid consumption transactions for the same Event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; o3 R1; o1, s3 R1
- Rationale: Concurrent valid submissions exercise the consumption nullifier boundary.
- Verify: demonstration, under a functioning integration ledger with an eligible Anchor, include the racing transactions and inspect finalized contract state independently.
- Status: settled

### MPE-VER-033 Hostile bridge inputs

The Prototype shall produce zero unauthorized contract effects in the hostile bridge-input suite.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; s1, s2, s3, s4 R1; s1, s4 R2
- Rationale: An Indexer response is not sufficient authentication of an Event or Anchor.
- Verify: test, inject fabricated Indexer results, incorrect Merkle leaves, misbound authorization, wrong destinations, expired statements, replays and failed fallible execution; inspect finalized effects and public disclosures.
- Status: settled

### MPE-VER-034 Deployment capability gate

If the target network lacks a demonstrated capability required by the selected integration profile, then MPE shall fail production integration acceptance.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D10; g1, g4, o1, s2, s4 R1; o1, o3 R2; `midnight-docs/docs/relnotes/support-matrix.json:38`
- Rationale: Local source and release documentation do not establish target-network activation.
- Verify: demonstration, execute the exact selected Registry, Anchor and consumer operations against the target runtime and Indexer schema; require finalized results and generation evidence.
- Status: settled

### MPE-VER-035 Ledger Adapter failure

When the Ledger Adapter is unavailable or returns stale state, the Prototype shall produce the NET-defined degraded-mode result for the affected operation.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10; g1, o1, s3, s4 R1; o1 R2
- Rationale: Missing ledger capability requires an explicit outcome rather than fabricated finality.
- Verify: test, disconnect the adapter, withhold finality, return old membership roots and delay Anchor reads; check result labels against NET and CON, then exercise recovery.
- Status: settled

### MPE-VER-036 Outside-developer usability

The Prototype shall enable at least P-VER-19 of P-VER-18 outside developers to complete the publisher and crash-resuming subscriber exercise within P-VER-20.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D10; o3 R1/R2
- Rationale: Documentation and API semantics affect correct adoption.
- Verify: demonstration, provide only released documentation, examples and a prepared local environment; count success only after publication, crash, resume and correct Event recovery without team coaching.
- Status: open (DEC-VER-3)

### MPE-VER-037 Independent review gate

MPE shall enter production acceptance only with zero unresolved critical or high-severity findings from independent review of the selected construction.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; s2, s3, s4, o4 R1; s2 R2
- Rationale: Finite tests cannot establish cryptographic composition security.
- Verify: inspection, review admission binding, cryptography, encodings, parsing, persistent state, bridge authorization and privacy claims; require reproducible closure evidence for each blocking finding.
- Status: settled

### MPE-VER-038 Production canary gate

While the production pilot runs for P-VER-21, MPE shall achieve canary timely delivery of at least P-VER-22 within P-VER-23.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D10; o4 R1
- Rationale: Operational acceptance requires sustained evidence beyond a laboratory run.
- Verify: test, derive expected deliveries from scheduled accepted canaries; retain failures, outages, Operator distribution and per-day results throughout the consecutive window.
- Status: open (DEC-VER-6)

### MPE-VER-039 Pause and resume drill

Where the selected Registry profile supports pause, MPE shall complete the pause-to-resume acceptance drill within P-VER-24.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D10; o4 R1/R2; `midnight-node/runtime/src/check_call_filter.rs:39`
- Rationale: Registry pause and ledger-wide transaction filtering are distinct failure conditions.
- Verify: demonstration, exercise OPS runbooks and defined availability labels; test Registry pause separately from ledger safe mode, without assuming MPE can resume the underlying ledger.
- Status: open (DEC-VER-6)

### MPE-VER-040 Open admission gate

If the open-admission red team reduces honest delivery below the frozen adversarial acceptance threshold, then MPE shall fail open-admission acceptance.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D10; g1 R1; o1 R2; s3 R1
- Rationale: Removing a launch restriction requires its own evidence and decision.
- Verify: simulation, give attackers as many peer identities as the honest set under the proposed open NET profile; test targeted capture and cold joining against P-VER-25, with publication allowances controlled independently.
- Status: open (DEC-VER-6)

### Acceptance suites and measurement convention

The following conventions define the checks referenced above; they do not add transport or privacy guarantees.

| Category | Required evidence |
|---|---|
| Conformance and cryptography | Exact valid/malformed vectors; object-bound admission; selected-domain separation; wrong-key and tamper cases; measured wire and cryptographic costs |
| Models | Executable transition rules, invariant definitions, explored bounds, tool versions, exhausted search results and preserved counterexample traces |
| Nominal and scale | Local multi-process demonstration, nominal soak, sustained scale evaluations and complete delivery/resource reports |
| Failure and recovery | Crash points, partitions, restart, retained-range recovery, failover, cursor replay and unavailable-range outcomes |
| Abuse and overload | Invalid ingress, quota exhaustion, equivocation, targeted discovery poisoning, scoring attacks and burst recovery |
| Privacy observations | Interest-swapped traces, plaintext-log canaries and scoped attribution experiments |
| Midnight integration | Actual costs, target capabilities, root concurrency, reaction races, hostile bridge inputs and adapter failure |
| Production | Independent review, operational pilot, pause drills and a separately approved open-admission gate |

**Eligibility.** An eligible Envelope–Subscriber pair consists of an accepted valid Envelope and a scheduled honest Subscriber authorized to recognize its Event. The fixture selects sufficient expiry and retention for its declared deadline. An admitted Envelope omitted by the implementation remains in the denominator.

Nominal and adversarial delivery fractions use the declared connected topology. Partition cases use separate recovery acceptance: the Event remains within retention, an honest holder is reachable after healing, and the Subscriber requests recovery. Permanent partitions or loss of all holders produce explicit unavailable outcomes; they cannot be silently removed from nominal statistics.

**Timing.** Post-admission timing starts when the Publisher’s selected submission path accepts the Envelope and ends at the first correct Subscriber delivery. Completion percentiles cover delivered pairs; deadline fractions include omissions. Reports identify the timestamp boundary and clock uncertainty. Admission, proving, Anchor inclusion, finality, indexing and contract effects have separate clocks.

**Accounting.** Reports include p50, p95, p99, sample counts, unique accepted Envelopes, expected pairs, delivered pairs, late pairs, missing pairs and duplicate attempts. CPU uses declared core units. Byte counts state whether they include transport, control traffic, retries and client fan-out. Amplification compares observed wire bytes with unique accepted Envelope bytes.

**Models.** Bounds cover at least allowance crossing, adjacent epochs, conflicting publications, old/current roots and crash/recovery transitions. Exact cardinalities and exploration depth are frozen before checking. A passing bounded exploration means no discovered counterexample within those bounds; it is not an unrestricted proof.

**Mocks.** Mock Ledger Adapter results carry explicit mock provenance. Mock success cannot satisfy real-ledger measurement or deployment-capability gates. Where a real capability is unavailable, local Prototype acceptance and production integration acceptance retain separate verdicts.

## Decisions

### DEC-VER-1 Phase order and Prototype boundary

- **Options:** g4’s ledger-only convention, two-process soak and stop; o3’s ledger-first then overlay; g1/g2’s parser/admission and simulation before sidecar release; o1’s integration spikes then overlay; s4’s evidence and models before measured service; o4’s operational stages.
- **Recommended default:** Phase 0 freezes evidence, selected encodings, vectors, bounded models and cryptographic microbenchmarks. Phase 1 runs the local Rust Prototype and scale evaluations. Phase 2 completes real Midnight integration and a bounded pilot. Phase 3 applies production operational gates. Optional retrieval or anonymity upgrades have separate profiles.
- **Reason:** The brief decides a sidecar GossipSub Prototype. Local mocks permit progress while deployment capabilities remain unknown; they do not discharge integration gates.
- **Settling check:** Review the completed gate artifacts against the intended product’s latency, payload, device and ledger dependencies. Reject any phase transition supported only by mock or imported benchmark results.

### DEC-VER-2 Workloads, deadlines and stop conditions

- **Options:** g1: 16 relays, 50/s, six-hour storage observation, p99 ≤ 10 s, ≥ 99% reaching 15 relays; g2: 50/200/1,000 relays, nominal p99 ≤ 2 s, stop above 6 s at 200 or below 99% delivery; g3: shard-specific caps and p99 ≤ 3 s; o1: 200 relays at 50/s for 24 h; s4: 10/s for 72 h, 100/s burst, 99.9% timely consumer delivery; s3: seven-day pilot and 35 s deadline.
- **Recommended default:** Apply the Parameters table: 16-process local run, 10/s for 72 h, 100/s burst, 10 s nominal deadline and 99.9% timely pair delivery. Evaluate 50/s for 24 h at the scale-simulation sizes. Require 99% timely honest delivery in declared non-partitioned attack cases.
- **Reason:** This combines a narrow endurance workload with a distinct higher-load evaluation. It does not equate Bus Node counts with Subscriber fan-out.
- **Settling check:** Run the selected FMT/NET/admission profile against PRF’s merged workloads and resource ceilings. PRF must resolve per-Shard versus network-wide rates and Subscriber counts before acceptance. A failure stops progression; it triggers a reviewed capacity or architecture change.
- **Residual disagreement:** g2’s automatic anchors-only fallback is not adopted. Anchors do not deliver unavailable bodies. NET must define a separately demonstrated fallback.

### DEC-VER-3 Fuzz campaign and consumer usability gates

- **Options:** g1/g4 emphasize deterministic vectors and continuous parser testing; o3 adds one billion fuzz iterations and a five-developer afternoon exercise; s3/s4 emphasize bounded hostile-input effects and independent review.
- **Recommended default:** Keep the billion-iteration decoder campaign as a Prototype MUST. Keep the outside-developer exercise as a Prototype SHOULD, reporting its outcome explicitly.
- **Reason:** The fuzz threshold is a proposed gate rather than a coverage guarantee. The usability trial requires independent participants and complements delivery correctness.
- **Settling check:** Review coverage, corpus diversity and execution cost before changing the fuzz profile. Promote usability to a release MUST when CON identifies the SDK as a shipped consumer interface. o3’s proposal treats it as mandatory.

### DEC-VER-4 Formal-model extent

- **Options:** g1 allows exhaustive property-based checking of a small accept predicate; g2/g3 limit formal work primarily to admission; o1/s3 add Anchors and consumption; o3 adds delivery state; o2/o4 add selected governance and economic invariants; s1/s2 require separate cryptographic construction review.
- **Recommended default:** Require executable bounded models for admission, delivery and consumption. Model governance features only when selected. Permit Quint, TLA+, ACL2s or equivalent exhaustive state exploration with recorded bounds.
- **Reason:** These models address MPE composition and recovery. Existing GossipSub work informs attack generation but does not certify MPE’s scoring configuration. Cryptographic claims require independent analysis.
- **Settling check:** Map each selected safety property to a model invariant and adversarial implementation fixture. Require new counterexample generators for application-specific scoring where existing ones omit MPE states. See `2023-kumar-gossipsub-acl2s`, §5.

### DEC-VER-5 Attribution experiment interpretation

- **Options:** g1/o4 propose a `2p²` precision gate; o1 proposes a multiplier of a Dandelion++ bound; s1/s4 reject these as transferable anonymity criteria.
- **Recommended default:** Require precision/recall measurements and uncertainty, without an anonymity pass threshold derived from `p²`.
- **Reason:** The paper’s lower bound and random four-regular-graph theorem do not establish an upper bound for the selected MPE ingress mechanism. Launch claims exclude global-observer, timing and relationship privacy.
- **Settling check:** A stronger claim needs a separately reviewed construction, adversary model and preregistered evaluation. Finite first-spy results alone do not settle it. See `2018-fanti-dandelionpp`, §§3.2–3.3 and Theorem 1.

### DEC-VER-6 Production and open-admission gates

- **Options:** g1 retains restricted admission until a failed capture attempt; o1 initially proposes permissionless relays but its review supports a red-team gate; o2 uses economic/operator milestones; o4 adds operational canaries, pause drills and jurisdictional review; s1/s3/s4 require funded capacity and independent assurance.
- **Recommended default:** Separate local Prototype completion from production acceptance. Require independent review, the canary window, applicable pause drills and a reviewed open-admission red-team result. Passing a red-team run does not automatically remove restrictions.
- **Reason:** Laboratory results do not establish Operator diversity, funding or sustained availability.
- **Settling check:** OPS and ECO provide the selected Operator, funding and governance criteria; verify them alongside VER results. Jurisdictional approvals remain OPS responsibilities.
- **Scope limit:** Membership counts or organic traffic thresholds are operational assumptions, not anonymity theorems.

## Cross-area dependencies

The IDs below are **provisional expected integration slots**. The merge must map them to the other authors’ final IDs; they do not assert that those records already exist.

| Expected requirement IDs | Required contract with VER |
|---|---|
| MPE-PRV-001, MPE-PRV-002 | Claimed properties, adversary classes, leakage contract and permitted observational differences |
| MPE-CRY-001, MPE-CRY-002 | Exact cryptographic profile, binding/domain rules, valid and hostile vectors, key lifecycle |
| MPE-SEC-001, MPE-SEC-002 | Attack fixtures, overload bounds, scoring safety properties and severity definitions |
| MPE-PRF-001, MPE-PRF-002 | Rates, Envelope mix, Shard counts, Subscriber fan-out, named hardware and numerical resource ceilings |
| MPE-STO-001, MPE-STO-002 | Retention, expiry, holder conditions, back-fill behavior, pruning and storage accounting |
| MPE-FMT-001, MPE-FMT-002 | Canonical Envelope classes, version policy, identifier derivation and decoder vectors |
| MPE-PUB-001, MPE-PUB-002 | Admission boundary, delivery eligibility, ordering, replay and gap semantics |
| MPE-CON-001, MPE-CON-002 | Result labels, cursor persistence, atomic handler semantics, contract authorization and replay rules |
| MPE-ECO-001, MPE-ECO-002 | Purchased allowance, admission identity scope, acceptable ledger costs and funded capacity |
| MPE-OPS-001, MPE-OPS-002 | Production phases, runbooks, Operator diversity, independent-review process and approval of admission changes |
| MPE-NET-001, MPE-NET-002 | Frozen GossipSub v1.1 configuration, discovery/outbound policy, Ledger Adapter interface and demonstrated fallback |

## Glossary additions

| Term | Meaning |
|---|---|
| Acceptance profile | Frozen configuration, workload, thresholds, fixtures and reproduction instructions for one acceptance evaluation |
| Phase gate | Verdict over all mandatory checks assigned to a phase |
| Eligible Envelope–Subscriber pair | Accepted valid Envelope and scheduled honest Subscriber expected to recognize its Event under the fixture’s authorization and availability conditions |
| Timely delivery fraction | Fraction of eligible pairs receiving their first correct delivery within the declared deadline |
| Atomic effect store | Store committing a handler effect and its deduplication record atomically |
| Reactor | Off-chain process submitting a transaction through the CON contract-consumption path |
| First-spy estimator | Attribution rule assigning a publication to the first honest peer observed forwarding it to a coalition |
| Canary | Controlled test Event with a known publication schedule and expected recipients |
| Recovery chaos workload | Fixture-generated Events combined with declared crashes, restarts, partitions, replay and failover |
| Phase 0–3 | Evidence/models; local Prototype and simulations; real integration/pilot; production acceptance, respectively |

## Gaps

- **Merged operating point is unknown.** Rates, Envelope classes, admission size, retention and fan-out conflict across proposals. VER defines candidate workloads; PRF/FMT/ECO/STO/NET must supply a coherent profile. g1’s illustrative size mix totals 100.1%; it cannot be copied unchanged into a fixture.
- **Resource ceilings are incomplete.** Proposed node classes and budgets differ materially. Without merged numerical ceilings, MPE-VER-015 cannot pass. Measuring an unspecified ceiling is not acceptance.
- **Deployed Midnight capabilities are unknown.** The checked lockfile pins ledger revision `6abe9b16`; the local support matrix lists Compact `0.31.1` for mainnet. Neither establishes live activation. Target-network demonstrations remain necessary.
- **Off-chain verification of the intended Midnight Admission Proof is unknown.** o1 explicitly identifies this spike. Proof bytes, verifier availability and measured costs must precede adoption; Waku figures are not substitutes.
- **Ledger-only comparison is not an accepted MPE architecture.** g4 and s4 motivate a comparative experiment. Any such experiment must be labeled separately because the brief keeps Event bodies off the ledger. The inspected `Misc` declaration provides a 256-byte payload, not an arbitrary bulk carrier: `minokawa-compact/compiler/midnight-events.ss:71`.
- **Unconditional zero-loss delivery is unsupported.** Permanent partitions, unavailable bodies and expiry prevent recovery. The zero-loss chaos gate therefore has explicit surviving-holder and retention conditions.
- **Exactly-once external side effects are unsupported.** o3’s handler guarantee requires atomic state or application idempotency, as s2’s review observes. VER confines its gate to committed effects in the declared atomic store.
- **A complete scoring fix cannot be inferred from a crate version.** The inspected rust-libp2p changelog does not establish that every selected MPE scoring configuration defeats CVE-2022-47547-style attacks. Regression evidence remains required.
- **Universal privacy cannot be converted into a finite test.** Paired traces, log audits and attribution measurements can find violations; they cannot prove the complete construction secure. Launch claims retain the brief’s limits.
- **Advanced profiles are not launch gates.** FMD, PIR/OMR, mix transports, MLS, ratchets, cover traffic and incentive upgrades require separate construction reviews and matched-workload evaluations if selected.
- **Funding and legal readiness are not established by simulation.** Economic models and counsel memoranda belong to ECO/OPS. Production acceptance needs the concrete commitments and approvals those areas select.
- **Calendar estimates are not acceptance criteria.** Proposed six-to-eight-week phases have no verified delivery basis and are omitted from the gates.