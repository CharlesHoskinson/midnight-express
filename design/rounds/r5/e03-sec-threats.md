## Scope of this area

SEC specifies defenses against network capture, resource exhaustion, replay, censorship, hostile infrastructure, compromised keys and malicious inputs.
It covers attack responses in the Prototype and production targets, including failures that must not penalize honest peers.
Contract invariants apply to MPE’s supplied consumption integration; arbitrary application contracts remain outside MPE’s enforceable boundary.
Launch claims remain content confidentiality and interest-hiding from infrastructure, with visible Shard membership; global-observer resistance, timing privacy and relationship privacy are not promised.
Admission economics, cryptographic constructions, retention periods, governance authority and delivery SLOs belong to the corresponding areas.

## Parameters

Defaults are proposed settings, not measured security guarantees. Sources use `R1` and `R2` for the corresponding files under `design/rounds/`. Midnight paths refer to `/home/charl/midnight/`; libp2p paths refer to `/home/charl/libp2p/`.

| Parameter | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-SEC-1 | Minimum outbound mesh connections per Shard | 4 connections, assuming NET selects `D=8`, `D_low=6` | Positive integer; strictly below `D_low`; at most `D/2` | g2 R1 D5/D9, R2 D5; `specs/pubsub/gossipsub/gossipsub-v1.1.md:192`; open DEC-SEC-2 |
| P-SEC-2 | Independent Operators supplying bootstrap or comparison sources | 2 Operators | Integer ≥2, bounded by the available roster | o1 R1 D9; o3 R1 D9, R2 D9; s1 R1 D9; independence assessment is an **assumption** |
| P-SEC-3 | Per-peer outstanding verification jobs, including queued and executing jobs | 8 jobs | Positive integer ≤ P-SEC-4 | s3 R1 D9; g3 R1 D9; numerical default is an **assumption**, open DEC-SEC-3 |
| P-SEC-4 | Bus Node total outstanding verification jobs | 128 jobs | Integer ≥ P-SEC-3, subject to the PRF memory budget | s3 R1 D9; s4 R1 D9; numerical default is an **assumption**, open DEC-SEC-3 |
| P-SEC-5 | Maximum delay before deleting a body named by an authenticated tombstone | 48 hours after successful authorization | Positive duration ≤48 hours; ordinary expiry may delete sooner | o4 R1 D7; open DEC-SEC-5 |
| P-SEC-6 | Adversarial relay-identity fractions exercised in targeted security experiments | 1%, 3%, 5% | Each fraction greater than 0% and less than 100%; additional cases permitted | s3 R1 D10; g2 R2 D10; experimental fractions, not resilience bounds |

Resource limits owned by PRF and STO must be finite, configured values. SEC does not introduce competing defaults for their byte, connection, retention or retrieval budgets.

## Requirements

### MPE-SEC-001 Launch relay admission

While launch relay admission is permissioned, the Bus Node shall admit only relay identities authorized by its authenticated Registry snapshot.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D9; o4 R1 D9; s3 R1 D7/D9.
- Rationale: A launch allow-list limits relay identity flooding without claiming permissionless Sybil resistance.
- Verify: test, attempt relay admission with authorized, unauthorized, revoked and substituted identities against a mock Ledger Adapter.
- Status: open (DEC-SEC-1)

### MPE-SEC-002 Bootstrap source diversity

When forming its initial peer set, the Bus Node shall use authenticated bootstrap records supplied by P-SEC-2 independent Operators.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9; s1 R1 D9; s3 R1 D9; s4 R1 D9.
- Rationale: Authentication prevents list substitution; multiple Operators reduce dependence on a single discovery service.
- Verify: test, poison one bootstrap source and confirm that unauthenticated records cannot replace the independently authenticated source.
- Status: settled

### MPE-SEC-003 Outbound connection protection

When maintaining a Shard mesh with sufficient eligible outbound peers, the Bus Node shall retain at least P-SEC-1 outbound mesh connections.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9; s1 R2 D9; `specs/pubsub/gossipsub/gossipsub-v1.1.md:192`; `rust-libp2p/protocols/gossipsub/src/config.rs:376`.
- Rationale: The outbound quota constrains coordinated inbound takeover; poisoned outbound selection remains possible.
- Verify: simulation, saturate inbound connections and inspect mesh membership after grafting, oversubscription pruning and heartbeat maintenance.
- Status: open (DEC-SEC-2)

### MPE-SEC-004 Active peer scoring

The Bus Node shall apply the selected GossipSub v1.1 scoring profile to mesh peer selection.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9; s4 R1/R2 D9; `specs/pubsub/gossipsub/gossipsub-v1.1.md:205`.
- Rationale: Scoring must affect peer selection rather than exist only as telemetry.
- Verify: test, drive peers across the selected pruning, graylisting and opportunistic-grafting thresholds and check the corresponding v1.1 behavior.
- Status: settled

### MPE-SEC-005 Admission before forwarding

The Bus Node shall forward an Envelope only after validating its Admission Proof against the authorized network, epoch, Shard, size class, expiry, proof-independent Envelope identifier and publication allowance.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D1/D9; s1 R2 D9; s2 R2 D9; `rust-libp2p/protocols/gossipsub/src/config.rs:280`.
- Rationale: Admission must authorize the particular Envelope rather than possession of an unrelated credential.
- Verify: test, mutate each bound field independently and confirm no forwarding; inspect that application validation precedes GossipSub acceptance.
- Status: settled

### MPE-SEC-006 Cheap framing checks

If an Envelope violates the supported framing rules, then the Bus Node shall discard it before admission cryptography or allocation based on its declared variable lengths.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D9; s3 R1 D1/D9; s4 R1 D9.
- Rationale: Fixed framing and early length checks limit parser and proof-verification amplification.
- Verify: test, submit truncated records, excessive lengths, invalid size classes, noncanonical encodings and invalid reserved fields; instrument verifier calls and allocations.
- Status: settled

### MPE-SEC-007 Rejection of proven invalidity

If validation establishes that an Envelope violates supported framing or cryptographic admission rules, then the Bus Node shall classify it as GossipSub Reject.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9; g1 R2 D9; `specs/pubsub/gossipsub/gossipsub-v1.1.md:535`; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:939`.
- Rationale: Reject suppresses dissemination and applies the invalid-message penalty to forwarding peers.
- Verify: test, inject a malformed supported Envelope and an invalid proof; confirm no forwarding and the configured P₄ score change.
- Status: settled

### MPE-SEC-008 Ignore local uncertainty

If validation cannot determine validity because of unavailable admission state, a stale chain view, an unsupported version or local overload, then the Bus Node shall classify the Envelope as GossipSub Ignore.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9; o1 R2 D9; `specs/pubsub/gossipsub/gossipsub-v1.1.md:524`; `rust-libp2p/protocols/gossipsub/src/peer_score.rs:750`.
- Rationale: Local uncertainty must not become an invalid-message accusation against an honest forwarder.
- Verify: test, exercise each condition with valid traffic and confirm no forwarding and no P₄ increment.
- Status: settled

### MPE-SEC-009 Verification backlog bounds

The Bus Node shall limit outstanding verification work to P-SEC-3 jobs per peer within a total of P-SEC-4 jobs.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; g3 R1 D9; s4 R1 D9; numerical defaults are **assumptions**.
- Rationale: Per-peer limits contain a single sender; the total limit contains distributed connection floods.
- Verify: test, flood through existing and newly created connections and confirm both bounds include executing jobs.
- Status: open (DEC-SEC-3)

### MPE-SEC-010 Verification scheduling fairness

While multiple peer verification queues remain nonempty, the Bus Node shall dispatch jobs by round-robin peer selection.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; specific scheduling policy is an **assumption** implementing its fair-scheduling defense.
- Rationale: A continuously replenished attacker queue must not monopolize dispatch ahead of already queued honest work.
- Verify: test, keep attacker queues saturated and confirm each continuously nonempty peer queue receives a dispatch opportunity in every scheduling round.
- Status: open (DEC-SEC-3)

### MPE-SEC-011 Retrieval abuse limits

If a retrieval request would exceed a configured retrieval byte, request or concurrency budget, then the Store Node shall refuse that request with ResourceExhausted.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D6/D9; g3 R1 D9; s4 R1 D9.
- Rationale: Historical retrieval requires its own limits rather than unrestricted access to live-path resources.
- Verify: test, exceed each STO/PRF retrieval budget using oversized intervals, parallel requests and repeated requests; confirm refusal before excess resource commitment.
- Status: settled

### MPE-SEC-012 Storage exhaustion response

If accepting a retention request would exceed its configured storage cap, then the Store Node shall refuse that request with StorageExhausted.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D4/D5/D9; g3 R1 D9; s3 R1 D9.
- Rationale: Valid paid traffic can exhaust storage; admission cannot guarantee free capacity.
- Verify: test, fill the configured cap with unexpired Envelopes and confirm refusal leaves existing unexpired bodies intact.
- Status: settled

### MPE-SEC-013 Historical admission separation

When serving retained Envelopes through back-fill, the Store Node shall validate admission using the historical Registry snapshot applicable to each Envelope.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D6/D9; s2 R1 D9.
- Rationale: Back-fill must not renew expired publication allowances or treat historical delivery as fresh admission.
- Verify: test, retrieve an historically valid Envelope after its admission epoch closes and confirm historical validation consumes no new allowance.
- Status: settled

### MPE-SEC-014 Proof-independent deduplication

The Bus Node shall treat alternative valid Admission Proof serializations for the same proof-independent Envelope identifier as duplicate publication.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D1/D9; s4 R1 D9.
- Rationale: Proof variability must not create additional delivery identities; identifier construction belongs to FMT.
- Verify: test, supply alternative valid proof representations for an identical authenticated Envelope representation and confirm only the initial publication is accepted.
- Status: settled

### MPE-SEC-015 Durable admission replay state

The Bus Node shall durably commit consumed publication allowances before forwarding their admitted Envelopes.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; g3 R1 D9; s3 R1 D9; s2 R2 D9.
- Rationale: A crash between forwarding and persistence must not restore an already spent allowance.
- Verify: test, interrupt execution at persistence and forwarding boundaries, restart, and replay the admitted Envelope.
- Status: settled

### MPE-SEC-016 Missing replay-state recovery

If replay state for still-usable publication allowances is missing or cannot be validated after recovery, then the Bus Node shall refuse live admission under those allowances.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g3 R1 D9; s3 R1 D9; s2 R1/R2 D9.
- Rationale: Restart or backup recovery must not silently reset admission quotas.
- Verify: test, restore absent, corrupt and detectably stale replay state and confirm affected admission remains unavailable until recovery establishes the required history or permanent expiry.
- Status: settled

### MPE-SEC-017 Replay-state pruning boundary

The Bus Node shall retain a consumed allowance record until every accepted authorization using that allowance is permanently ineligible for live publication.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D6/D9; s2 R2 D9; g1 R1 D6/D9.
- Rationale: Payload expiry alone may precede the end of the authorization’s replay window.
- Verify: test, exercise epoch boundaries, accepted historical roots, clock tolerance and restart recovery; attempt reuse immediately before and after the pruning boundary.
- Status: settled

### MPE-SEC-018 Conflicting allowance use

If a valid Envelope conflicts with an already consumed publication allowance, then the Bus Node shall classify that later Envelope as GossipSub Ignore.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g3 R1 D9; s1 R2 D9; s4 R2 D9; Ignore for partition conflicts is a recommended **assumption**.
- Rationale: Locally observed conflicts require suppression without accusing a forwarder whose partition accepted a different Envelope.
- Verify: simulation, spend an allowance on distinct signed Envelopes in separate partitions, reconnect, and confirm each node refuses subsequent conflicting acceptance without P₄ framing.
- Status: open (DEC-SEC-4)

### MPE-SEC-019 Conflict alarm

When it verifies conflicting Envelopes authorized by the same publication allowance, the Bus Node shall emit an AdmissionConflict diagnostic containing their identifiers and the applicable authorization reference.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; s4 R2 D9; g1 R2 D9.
- Rationale: A malicious credential holder can authorize conflicting bodies; signatures do not establish a globally unique winner.
- Verify: test, distinguish valid equivocation from invalid proofs and confirm diagnostics use bounded records containing no plaintext or secret keys.
- Status: open (DEC-SEC-4)

### MPE-SEC-020 Authenticated key changes

If a discovery service presents a replacement for a pinned Publisher key without an authenticated change authorization, then the MPE client library shall reject that replacement.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; s2 R1 D9.
- Rationale: Service control must not suffice to substitute an Event authentication or encryption identity.
- Verify: test, replace invitation and discovery keys through a hostile service and confirm the pinned identity remains authoritative.
- Status: settled

### MPE-SEC-021 Independent retrieval comparison

When completing a Shard retrieval interval, the MPE client library shall compare its Envelope inventory against inventories supplied by P-SEC-2 independent Operators.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; s1 R1 D9; s3 R1 D9; o3 R2 D9.
- Rationale: Independent observations can reveal selective omission and victim-specific feed tagging.
- Verify: test, omit different Envelopes from different providers and confirm comparison covers the entire requested interval, including unrecognized Envelopes.
- Status: settled

### MPE-SEC-022 Authenticate Registry read results

If an Indexer result lacks independently verified provenance from the authorized Registry at finalized state, then the Indexer adapter shall exclude it from admission and Anchor authorization.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D9; s1 R1 D9; s4 R2 D9; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`.
- Rationale: An Indexer query response supplies data, not authority; verification transport belongs to NET.
- Verify: test, substitute contract addresses, invent Anchors, alter Registry data and supply malformed logs; confirm no authorization derives from these results.
- Status: settled

### MPE-SEC-023 Recognition-independent omission repair

When compared inventories differ, the MPE client library shall request repair of every missing Envelope identifier in their union, subject to configured retrieval budgets.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D9; s1 R1 D9; s3 R1 D9; g1 R2 D9.
- Rationale: Repairing only recognized Events would expose interests to a selectively withholding provider.
- Verify: test, vary Subscriber keys over identical inventories and compare the requested repair identifiers; budget refusal must leave the interval unresolved.
- Status: settled

### MPE-SEC-024 Report unresolved retrieval

If inventory comparison is unavailable, an authenticated sequence gap remains or requested repair fails, then the MPE client library shall report the affected retrieval interval as Unresolved.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; o3 R1/R2 D9; s2 R2 D9; s3 R1 D9; s4 R1 D9.
- Rationale: Roots, counts and signatures do not prove global completeness; an omitted first contact or suffix may remain undetectable.
- Verify: test, remove a comparison source, withhold an interior sequence item and fail a repair request; confirm no complete-delivery assertion appears.
- Status: settled

### MPE-SEC-025 Recognition-independent network behavior

The MPE client library shall keep infrastructure-facing retrieval, retry, error and receipt behavior independent of whether an Envelope’s Tag matches a Subscriber.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s1 R1/R2 D9; s2 R1/R2 D9; g2 R1 D9; s3 R1 D9.
- Rationale: Active probing can reveal interests even when encrypted content remains confidential.
- Verify: test, replay identical feeds and failures with matching and nonmatching Subscriber keys; compare library-generated network transcripts before application actions.
- Status: settled

### MPE-SEC-026 Prevent silent privacy fallback

If recovery would change the selected privacy profile or replace whole-Shard retrieval with recognition-based filtering, then the MPE client library shall refuse the change until the caller explicitly selects that replacement profile.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; s1 R1 D9; s4 R1 D9; o3 R2 D9.
- Rationale: An attacker-induced outage must not silently weaken the caller’s selected interest-hiding behavior.
- Verify: test, disable the selected transport or retrieval source and confirm no filtered or weaker-profile request precedes explicit caller selection.
- Status: settled

### MPE-SEC-027 Persistent logging limits

The Bus Node shall exclude client IP addresses, Tags and per-client activity histories from persistent logs.

- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D9; o4 R1 D7/D9, R2 D9.
- Rationale: Content-blind operation does not prevent relationship disclosure through infrastructure logs.
- Verify: inspection, exercise normal operation, malformed traffic, admission conflicts and overload; inspect persisted application logs for prohibited fields.
- Status: settled

### MPE-SEC-028 Compromised-key send suspension

If a caller marks an active publishing or session key as compromised, then the MPE client library shall refuse publications using that key until authenticated replacement state is installed.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g4 R1 D9; s3 R1 D9; s2 R1 D9; o4 R1 D7/D9.
- Rationale: Continued use prolongs impersonation or disclosure; replacement does not erase previously exposed ciphertext.
- Verify: test, mark each active key compromised, attempt publication, and confirm an unauthenticated service-supplied replacement cannot lift suspension.
- Status: settled

### MPE-SEC-029 Admission-key separation

The MPE client library shall use distinct secret keys for admission authorization, Event encryption and application identity authentication.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D9; s3 R1 D9; s1 R2 D9.
- Rationale: Admission compromise or RLN secret extraction must not directly expose encryption or application identity secrets.
- Verify: inspection, trace key generation, derivation domains and API use; confirm no secret is reused across the named roles.
- Status: settled

### MPE-SEC-030 Authentication before session mutation

Where ratcheted sessions are present, the MPE client library shall commit received session-state changes only after message authentication succeeds.

- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D9; s2 R1/R2 D9; s3 R1 D9.
- Rationale: Malformed or forged traffic must not advance counters, consume keys or corrupt recovery state.
- Verify: test, submit forged messages, malformed keys and replayed initialization inputs; compare persisted session state before and after failure.
- Status: settled

### MPE-SEC-031 Missing session-update response

Where ratcheted sessions are present, if authenticated session state identifies a required key update as missing, then the MPE client library shall refuse sensitive publications dependent on that update with SessionUpdateRequired.

- Pattern: complex
- Scope: PROD
- Priority: MUST
- Source: D9; s3 R1 D9; s2 R2 D9; `2023-barnes-rfc9420`, §16.9.
- Rationale: Suppressed updates can prolong compromise; CRY defines update requirements and detection limits.
- Verify: test, suppress required updates while delivering application traffic and confirm affected sends remain suspended until the authenticated update is applied.
- Status: settled

### MPE-SEC-032 Payload execution boundary

The MPE client library shall require explicit Consumer authorization before initiating any download or executing any command requested by Event payload data.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D1/D10; g1 R1 D9; o1 R1 D9.
- Rationale: Authentication of a Publisher does not authorize executable content or unbounded external retrieval.
- Verify: test, deliver authenticated payloads containing executable expressions, command strings and external references; confirm decoding alone produces no corresponding side effect.
- Status: settled

### MPE-SEC-033 Unwanted-contact rejection

If an authenticated Publisher is denied by the Subscriber’s configured contact policy, then the MPE client library shall suppress delivery of that Publisher’s Event to the Consumer.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; o4 R1 D7, R2 D9; s3 R1 D9.
- Rationale: Unwanted contact is handled locally; bus admission alone cannot distinguish useful traffic from harassment.
- Verify: test, apply allow and deny policies to authenticated Events and confirm denied Events cause no Consumer callback or recognition-dependent infrastructure response.
- Status: settled

### MPE-SEC-034 Authenticated tombstone deletion

Where authenticated tombstones are enabled, the Store Node shall delete the named Envelope body within P-SEC-5 of successful tombstone authorization.

- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D9; o4 R1 D7/D9; s4 R2 D9.
- Rationale: Cooperative deletion is attributable; it cannot erase adversarial archives or establish legal immunity.
- Verify: test, authorize a tombstone using the OPS policy and confirm timely body deletion preserves admission replay records; forged tombstones must authorize no deletion.
- Status: open (DEC-SEC-5)

### MPE-SEC-035 Delivery during ledger interruption

While ledger-dependent registration or anchoring is unavailable, the Bus Node shall continue forwarding Envelopes valid under still-eligible authenticated cached Registry state.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D9; g3 R1 D9; s4 R1 D9; o4 R1 D7/D9; `midnight-node/runtime/src/check_call_filter.rs:44`.
- Rationale: A ledger interruption does not invalidate existing off-chain authorization or extend its validity.
- Verify: demonstration, disable the Ledger Adapter during active traffic; confirm eligible cached authorizations continue and expired or unknown authorizations do not.
- Status: settled

### MPE-SEC-036 Ledger-dependent failure reporting

If a ledger interruption or observed pause prevents registration, anchoring or contract consumption, then the MPE client library shall return a typed LedgerUnavailable or BusPaused outcome for the affected operation.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; o3 R1 D9; g2 R1 D9; o4 R1 D9; `midnight-node/runtime/src/check_call_filter.rs:44`.
- Rationale: Overlay delivery must not be mistaken for successful ledger authorization or a completed contract effect.
- Verify: test, separately fail each ledger-dependent operation and distinguish unavailable transport from an authenticated pause indication.
- Status: settled

### MPE-SEC-037 Contract authorization predicate

MPE shall permit an Event-triggered effect through its supplied contract-consumption integration only after in-circuit verification of an authorized Publisher’s signature binding the network genesis, target contract, action, payload commitment, logical Event identifier and expiry.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; o2 R2 D3; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1004`; `minokawa-compact/doc/compact-reference.mdx:3493`.
- Rationale: An unchecked witness, valid Admission Proof or Anchor inclusion does not establish application authorization.
- Verify: test, alter every bound field, substitute an unauthorized signer, omit signature assertions and use forged Indexer output; require zero unauthorized effects.
- Status: settled

### MPE-SEC-038 Atomic contract replay protection

MPE shall consume an authenticated logical Event’s replay identifier in the same atomic transaction as its supplied contract-consumption integration’s corresponding effect.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9; s1 R1/R2 D9; s2 R1/R2 D9; `minokawa-compact/doc/compact-reference.mdx:3777`.
- Rationale: Transport deduplication cannot prevent repeated effects after rewrapping, reconnects or application crashes.
- Verify: test, repeat consumption through distinct transactions and Envelope wrappers, including failure boundaries; require at most one committed effect for each authenticated Event, target and action.
- Status: settled

### MPE-SEC-039 Configuration-specific attack evidence

The Prototype shall produce an attack report for every SEC test-matrix case, recording configuration, attacker placement, controlled resources, delivery ratio, latency percentiles, eclipse duration, peak resource use and unauthorized or duplicate effects.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; s3 R1 D9/D10; g2 R2 D9/D10; s4 R1/R2 D9; `2023-kumar-gossipsub-acl2s`, §§3–5.
- Rationale: Peer fractions, Operator control, bandwidth and purchased allowances are different adversarial resources.
- Verify: inspection, check that every matrix case has reproducible inputs and measured results; absent measurements must be recorded as unknown.
- Status: settled

### MPE-SEC-040 Scoring vulnerability release gate

The Prototype shall report public-overlay release as blocked until its pinned GossipSub implementation has a documented resolution of CVE-2022-47547 for the selected scoring configuration.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; g2 R1 D9, R2 D10; o2 R2 D9; s4 R2 D9; `2023-kumar-gossipsub-acl2s`, §1.
- Rationale: Protocol adoption, an old audit or a crate version number does not establish closure of configuration-sensitive scoring attacks.
- Verify: inspection, review implementation provenance and applicability analysis, then run the corresponding attack regression against the pinned implementation and configuration.
- Status: open (DEC-SEC-6)

## Decisions

### DEC-SEC-1 Launch relay admission

- **Options:** Permissioned launch relays, proposed by g1 and o4; open relaying with scoring and paid publication admission, proposed by g2 and g3; accountable staged enrollment, proposed by s3.
- **Recommended default:** Permissioned launch relay admission with an authenticated roster and disclosed administrator censorship power.
- **Reason:** Paid publication admission does not constrain relay identities. The launch threat boundary is easier to test with an explicit roster.
- **Settling check:** Targeted bootstrap and mesh-capture experiments using the proposed open-admission mechanism, independently varying identity, Operator and bandwidth control. OPS and ECO must supply a concrete replacement admission policy before removing the roster.

### DEC-SEC-2 Outbound quota

- **Options:** `D=6`, outbound quota 2, proposed by g1; `D=8`, outbound quota 4, proposed by g2.
- **Recommended default:** P-SEC-1 under g2’s mesh profile, subject to PRF/NET adoption.
- **Reason:** The higher outbound quota constrains inbound capture while satisfying the v1.1 parameter conditions. It does not authenticate discovery or prevent malicious outbound selection.
- **Settling check:** Compare both profiles under churn, poisoned discovery, inbound saturation and targeted outbound capture. Select using measured delivery, resource budgets and honest-peer score behavior.

### DEC-SEC-3 Verification resource policy

- **Options:** Bounded queues and fair scheduling, proposed by s3; bounded concurrent unverified proofs per peer, proposed by g3; early rejection and ingress budgets, proposed by s2 and s4. Exact queue sizes remain unspecified.
- **Recommended default:** P-SEC-3 and P-SEC-4 with round-robin peer dispatch. These numerical defaults and the exact scheduler are **assumptions**.
- **Reason:** Invalid proofs consume work before their invalidity is established. Global limits remain necessary when attackers open many connections.
- **Settling check:** Measure valid and invalid verification costs on the reference Bus Node; flood connections while honest queues remain active. Retune before exceeding PRF memory, CPU or latency budgets.

### DEC-SEC-4 Conflicting allowance use

- **Options:** Deduplication and single-use caches without a partition-resolution rule, proposed by g1 and g2; RLN conflict evidence and slashing, proposed by o2 and o4; explicit conflict alarms and evidence-based action, proposed by s3 and s4.
- **Recommended default:** Retain the locally accepted binding, Ignore later conflicting publications, and emit AdmissionConflict. Economic penalties remain ECO’s responsibility.
- **Reason:** Credential holders can sign conflicting bodies. Honest partitions may select different initial Envelopes; forwarding either does not prove forwarder misconduct.
- **Settling check:** Model partition, root-transition, restart and conflicting-proof cases. Establish whether a proposed global winner rule is implementable without adding consensus to the overlay.
- **Residual:** Different partitions can accept different Envelopes before observing the conflict. Local first acceptance is not global ordering.

### DEC-SEC-5 Tombstones

- **Options:** Authenticated protocol tombstones and cooperative deletion, proposed by o4; ordinary expiry and infrastructure ejection without a specified tombstone feature in g1 and g2. Their omission is not an explicit rejection. s4 questions deletion and legal claims.
- **Recommended default:** Disable tombstones in the Prototype; retain MPE-SEC-034 as a conditional production target.
- **Reason:** Content reports, authorization authority and deletion appeals remain undefined. A forged or captured deletion authority becomes a censorship mechanism.
- **Settling check:** OPS must specify authenticated issuance, scope, auditability and recovery from unauthorized issuance. Test selective body deletion without premature removal of replay state.
- **Residual:** Cooperative deletion cannot remove copies retained by adversaries.

### DEC-SEC-6 CVE closure evidence

- **Options:** A pinned crate changelog explicitly naming the fix, required by g2; configuration-specific analysis and attack checks, emphasized by s4 and s2.
- **Recommended default:** Require documented resolution for the actual pinned implementation and configuration, supported by an attack regression. A reviewed non-applicability argument may count as resolution; this acceptance route is an **assumption**, not a recorded consensus.
- **Reason:** The published counterexample depends on scoring configuration. Neither an unrelated crate fix nor a changelog’s silence establishes safety.
- **Settling check:** Determine applicability, identify the relevant remediation or non-applicability evidence, and reproduce the scoring attack against the selected profile.
- **Current evidence:** The locally inspected Rust GossipSub changelog contains no explicit `CVE-2022-47547` entry; closure is **unknown**.

## Cross-area dependencies

These are expected merge slots, not assertions that the other authors have already assigned these numbers. The merge must replace provisional references with their actual requirement IDs.

| Expected requirement IDs | Required interface or invariant |
|---|---|
| MPE-FMT-001, MPE-FMT-002, MPE-FMT-003 | Canonical fixed framing, supported versions, size-class limits, proof-independent identifiers and authenticated expiry fields |
| MPE-CRY-001, MPE-CRY-002, MPE-CRY-003 | Authentication and key separation; authenticated invitations and rotation; optional session mutation, update-age and skipped-key limits |
| MPE-PRV-001, MPE-PRV-002 | Named adversaries, leakage boundary, recognition-independent behavior and explicit global-observer non-claims |
| MPE-ECO-001, MPE-ECO-002, MPE-ECO-003 | Message-bound Admission Proof predicate, publication allowances, eligibility across root transitions and economic response to conflicts |
| MPE-NET-001, MPE-NET-002, MPE-NET-003 | Separate overlay peer table; pinned GossipSub profile; authenticated finalized Registry reads and bounded cache eligibility |
| MPE-PRF-001, MPE-PRF-002 | Finite ingress, egress, connection and CPU budgets; delivery acceptance thresholds under named attacks |
| MPE-STO-001, MPE-STO-002, MPE-STO-003 | Storage and retrieval budgets; historical snapshots; durable replay records, expiry and pruning boundaries |
| MPE-PUB-001, MPE-PUB-002 | Authenticated inventories, logical identifiers, sequence-gap semantics and whole-Shard repair |
| MPE-CON-001, MPE-CON-002, MPE-CON-003 | Typed failure outcomes; application authorization in the supplied consumption circuit; atomic effect and replay-state updates |
| MPE-OPS-001, MPE-OPS-002, MPE-OPS-003 | Operator roster and declared affiliation; compromise response and optional tombstone authority; incident response and logging policy |
| MPE-VER-001, MPE-VER-002, MPE-VER-003 | SEC matrix execution, model checks, parser fuzzing, release thresholds and independent review |

The ledger-interruption requirements rely on the inspected local node generation, whose safe-mode filter deliberately excludes ordinary `send_mn_transaction` calls (`midnight-node/runtime/src/check_call_filter.rs:44`). Compact signature assertions were checked in the local Compact documentation (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1004`). Neither check establishes production activation of the ledger-9 event path.

## Glossary additions

| Term | Meaning |
|---|---|
| Independent Operators | Operators declared to have separate administrative control, assessed using the OPS roster and affiliations. Distinct peer IDs, addresses or signatures alone do not establish independence. |
| Publication allowance | A single-use ticket or rate-limit slot defined by ECO and consumed by live publication. |
| Proof-independent Envelope identifier | The FMT identifier derived from the authenticated Envelope representation without Admission Proof serialization. |
| Logical Event identifier | An authenticated application identifier used to recognize repeat delivery or execution despite transport rewrapping. |
| Inventory | A bounded list or manifest of Envelope identifiers for a specified Shard interval. Authentication establishes its source, not global completeness. |
| Authenticated cached Registry state | Previously verified Registry state whose admission eligibility remains valid under NET/ECO rules. Cached state cannot extend expiry. |
| Tombstone | An authenticated instruction naming an Envelope body for cooperative removal under the OPS policy. It does not authorize premature replay-state pruning. |
| Typed outcomes | Distinguishable machine-readable results: ResourceExhausted, StorageExhausted, AdmissionConflict, Unresolved, SessionUpdateRequired, LedgerUnavailable and BusPaused. CON owns their API encoding. |
| Supplied contract-consumption integration | MPE’s specified circuit and follow-up transaction path, implemented with CON. It excludes arbitrary contracts that deliberately omit its checks. |

The **SEC test matrix** comprises:

- Random and targeted attacker placements at P-SEC-6, recording identity, Operator, bandwidth and allowance control separately.
- Poisoned bootstrap lists, inbound saturation, malicious outbound candidates, cold boot, churn and cross-Shard score manipulation.
- Invalid-proof floods, malformed framing, connection floods, paid-capacity saturation, storage exhaustion and retrieval amplification.
- Partitioned allowance conflicts, alternative proofs, epoch/root transitions, replay after restart and detectable backup rollback.
- Indexer invention, stale chain views, selective inventories, first-contact omission, withheld suffixes and failure of comparison sources.
- Key substitution, caller-declared compromise, optional session-update suppression, recipient probing and attempted silent fallback.
- Contract authorization mutations, malicious witnesses, repeated logical Events and crash boundaries around effect commitment.
- Ledger interruption, authenticated pause indications, conditional tombstone forgery and logging inspection.

These cases specify coverage. VER and PRF own release thresholds; passing them does not prove resilience against every attacker.

## Gaps

- **Permissionless Sybil resistance:** No reviewed launch mechanism establishes independent relay ownership or prevents targeted routing capture. Scoring and paid publishing cannot substitute for that missing argument.
- **Complete delivery:** Matching inventories and Anchors do not prove that every Event was included. Coordinated omission, suppressed first contact and withheld suffixes can remain indistinguishable from silence.
- **Rollback detection:** Durable records prevent ordinary restart loss; detecting an internally consistent old backup requires an independently monotonic reference or reconstruction mechanism. That mechanism is **unknown** and belongs to STO/CON.
- **Combined security argument:** Individual component analyses do not establish security of admission, recognition, sessions, storage and contract consumption together. No supplied proposal closes that composition.
- **Traffic analysis:** Padding, encrypted transport and heuristic stems do not establish launch resistance to global correlation, repeated observation or revealing application effects. No stronger requirement is supported.
- **Key recovery:** Static-key rotation leaves retained history exposed. Ratchet recovery additionally depends on authenticated update delivery and deletion; CRY must select the profile before stronger claims become testable.
- **Governance and issuer capture:** Administrators or a compromised admission issuer can censor or authorize capacity. Authority thresholds, issuance caps and emergency powers require OPS/ECO requirements; SEC cannot infer honest governance.
- **Economic attacks:** Self-slash refunds, bond-key splitting, challenge griefing and DUST price spikes are identified in o2 R2 D9. Their settlement and treasury invariants belong to ECO; no reviewed design closes every case.
- **Institutional abuse response:** Jurisdictional liability, compelled logging and shutdown exposure are **unknown**. Tombstones, agreements and retention limits are technical controls, not legal conclusions.
- **Supply chain and incident commitments:** o4 proposes signed reproducible builds, independent audit and response deadlines. OPS/VER must define verifiable release artifacts and accountable response procedures.
- **Scoring closure and resource defaults:** CVE applicability, selected scoring weights and reference-machine verification costs remain **unknown**. Queue defaults are assumptions pending measurement.