## Scope of this area

PRV owns D2: named privacy properties, adversary definitions, permitted leakage, explicit non-claims, and the evidence required for each claim.
Launch claims are conditional content confidentiality, sealed topic-label confidentiality, and subscriber-interest privacy within a completely received Shard.
Shard membership, participation, ingress identity, timing, volume, admission metadata, and public application effects remain observable.
Launch provides no general publisher anonymity, timing privacy, volume privacy, or relationship privacy.
Cryptographic content protection can hold against a global observer without providing global-observer anonymity.

## Parameters

| Parameter | Meaning and unit | Default | Allowed range | Source |
|---|---|---|---|---|
| P-PRV-1 | Relay-identity fractions used in attribution experiments; dimensionless fractions | Sweep `{0.01, 0.03, 0.05}` | Each fraction in `[0, 1]`; additional cases permitted; actual controlled-node counts and fractions reported | s3 R1 §D10; proposed experimental settings, **assumption**, not a security threshold |

Envelope sizes, Shard counts, retention periods, admission quotas, and traffic budgets belong to their respective areas.

## Requirements

Sources identified as `R1` or `R2` refer to the named author's corresponding file under `design/rounds/`. Midnight ledger citations use the locally available node-pinned ledger revision `6abe9b16`, identified by `midnight-node/Cargo.lock:7894`; they do not refer to the ledger-8 working tree. Deployment activation remains unknown.

### Adversary definitions

| Class | Capabilities |
|---|---|
| R — Local infrastructure observer | Observes its connections, requests, Envelopes, operational state, and service records; includes a Bus Node, Store Node, admission issuer, Indexer, or wallet provider. |
| C — Colluding infrastructure | Combines observations from infrastructure parties, including enrollment and ingress records. A numerical minority supplies no independent privacy guarantee. |
| G — Global passive observer | Observes endpoint and infrastructure traffic timing, sizes, counts, online intervals, and public ledger activity; may obtain infrastructure records. |
| A — Active network adversary | Injects valid or malformed traffic, replays, delays, drops, probes, partitions, eclipses, and creates identities; may also exercise C's observations. |
| I — Insider or compromised endpoint | Holds an authorized recognition capability, receives plaintext, controls application behavior, or obtains endpoint secrets. |

These definitions follow s1 R1/R2 §D2 and s3 R1 §D2. Content claims exclude challenge-key compromise and intended recipients. A public recipient key is not a recipient secret.

### Privacy games and claim boundaries

**Content Game.** Compare executions differing only in equal-length Event plaintexts, with identical declared public leakage. Challenge endpoints and authenticated key establishment remain uncompromised. Computationally bounded R, C, G, or A adversaries receive the observations allowed by their class. The selected construction must bound distinguishing advantage as stated in its reviewed security analysis.

**Selection Game.** Compare executions differing only in a Subscriber's private interest or recognition-key set within the same received Shard set. Hold incoming traffic, online schedule, transport policy, public application actions, and external responses fixed. Recognition must not change requests, request sizes, cursors, retries, errors, repair choices, or scheduled transmissions. This is conditional selection privacy, including against active probes under these conditions; it does not hide Shard choice or application reactions.

These games implement s1 R1/R2 §D2, s3 R1 §D2, and s4 R1/R2 §D2. Their scenario-based formulation follows `2019-kuhn-privacynotions`, §§2–3.

### MPE-PRV-001 Claim register

The MPE shall maintain a claim register assigning each privacy claim its game, adversary classes, assumptions, permitted leakage, supporting evidence, verification procedure, and applicable profile.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D2; s1 R1 §D2; s4 R1 §D10.
- Rationale: A property name alone does not define a security promise.
- Verify: inspection, check every advertised claim against the required register fields.
- Status: settled

### MPE-PRV-002 Content confidentiality

The MPE shall provide computational indistinguishability in the Content Game against R, C, G, and A adversaries lacking challenge decryption secrets.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D2; s1 R1/R2 §D2; s2 R1 §D2; s3 R1 §D2.
- Rationale: Observable activity does not imply disclosure of sealed plaintext.
- Verify: analysis, review the selected construction's reduction and its implementation assumptions against the complete Content Game.
- Status: settled

### MPE-PRV-003 Sealed logical labels

The MPE shall exclude logical topic names, recipient addresses, and session or group identifiers from cleartext Envelope fields.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D2; s2 R1 §D2; s4 R1 §D2.
- Rationale: Sealed labels provide a narrower property than general topic unlinkability.
- Verify: inspection, enumerate serialized fields and check representative data and control Envelopes for exposed logical labels.
- Status: settled

### MPE-PRV-004 Recipient-key-hiding claim gate

The MPE shall withhold a recipient-key-hiding claim until reviewed analysis establishes the selected wrapper's key privacy against adversaries knowing candidate recipient public keys.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D2; s1 R2 §§D1–D2; s4 R2 §D2; `2001-bellare-keyprivacy`, §1.1.
- Rationale: Content confidentiality and omission of an address do not establish key privacy.
- Verify: analysis, inspect the wrapper's key-privacy game, reduction, public fields, and recognition interfaces.
- Status: open (DEC-PRV-3)

### MPE-PRV-005 Length concealment within a class

The MPE shall give Envelopes in the same configured size class identical serialized lengths regardless of their contained Event lengths.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; o1 R1 §D2, P7; s1 R1 §D2; s3 R1 §D2.
- Rationale: Padding conceals length within a class while leaving class and Envelope count visible.
- Verify: test, serialize boundary-length Events within each supported class and compare complete Envelope lengths.
- Status: settled

### MPE-PRV-006 Conditional subscriber-interest privacy

While the Subscriber uses the private reception profile, the MPE client library shall satisfy the Selection Game within its received Shard set.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1/R2 §D2; s3 R1 §D2; s4 R2 §D2; g1 R1 §D2.
- Rationale: Whole-Shard reception hides local selection while exposing Shard membership.
- Verify: test, compare paired executions with different interests under identical transport inputs and schedules.
- Status: open (DEC-PRV-1)

### MPE-PRV-007 Local recognition secrets

While the Subscriber uses the private reception profile, the MPE client library shall retain its Event decryption, topic, recognition, and wallet viewing secrets within the Subscriber's trusted endpoint boundary.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D3; s3 R1 §D2; g4 R1 §D10; `midnight-indexer/docs/architecture.md:22`.
- Rationale: A provider receiving these secrets becomes a trusted content or interest observer.
- Verify: inspection, trace secret-bearing values through outbound requests, provider APIs, configuration, and remote diagnostics.
- Status: open (DEC-PRV-1)

### MPE-PRV-008 No private selection predicates

While the Subscriber uses the private reception profile, the MPE client library shall omit topic, Tag, recipient, detection-key, and recognized-Envelope selectors from infrastructure requests.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D3; s3 R1 §D2; s4 R1 §D2; g4 R1 §§D2–D3.
- Rationale: Server-side selection reveals information that local recognition is intended to conceal.
- Verify: test, capture live and back-fill requests for Subscribers with different private interests and inspect all selectors.
- Status: open (DEC-PRV-1)

### MPE-PRV-009 Recognition-independent transport

While the Subscriber uses the private reception profile, the MPE client library shall make transport actions independent of local recognition outcomes.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §§D2–D3; s3 R1 §D2; s4 R2 §D2.
- Rationale: Errors, retries, disconnects, and repair choices can disclose selection without an explicit filter.
- Verify: test, compare requests, cursors, sizes, retry decisions, repair selections, and transmission schedules after matched, unmatched, malformed, and replayed Envelopes.
- Status: settled

### MPE-PRV-010 No recognition acknowledgements

When an Envelope is recognized, the MPE client library shall emit no automatic network acknowledgement of recognition.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D2; g2 R1 §D2; o3 R1 §D2; s1 R1 §D3.
- Rationale: Recognition acknowledgements create an observable recipient signal.
- Verify: test, capture traffic after recognition and distinguish any publication or storage receipt from recipient recognition.
- Status: settled

### MPE-PRV-011 Explicit application reactions

When an Event is recognized, the MPE client library shall require explicit application authorization before initiating an Event-dependent external action.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D2; o3 R2 §D2; s3 R1 §D10; s4 R1 §D2.
- Rationale: Replies, attachment fetches, reports, and contract transactions can correlate a Consumer with an Event.
- Verify: test, recognize Events containing external-action instructions and confirm that recognition alone initiates no external action.
- Status: open (DEC-PRV-2)

### MPE-PRV-012 Overload preserves the privacy boundary

If whole-Shard reception exceeds a configured resource limit, then the MPE client library shall report reception failure without substituting interest-dependent retrieval.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §§D9–D10; s1 R1 §D10; g3 R2 §D2.
- Rationale: Resource exhaustion cannot silently convert private reception into a filtered service.
- Verify: test, exhaust reception limits and inspect subsequent requests for introduced selection predicates.
- Status: open (DEC-PRV-1)

### MPE-PRV-013 Explicit privacy-changing fallback

If a fallback changes the applicable leakage contract, then the MPE client library shall block its activation until the application explicitly selects the changed profile.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §D9, block 4; s1 R2 §D8.
- Rationale: Transport failure does not authorize an undisclosed privacy downgrade.
- Verify: test, disable the primary path and confirm that a path with different leakage remains inactive without profile selection.
- Status: settled

### MPE-PRV-014 Recognition-free remote diagnostics

While the Subscriber uses the private reception profile, the MPE client library shall exclude private interest sets and recognition outcomes from remotely exported diagnostics.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D2; s4 R1 §D10, Phase 1; s1 R1 §D2.
- Rationale: Remote logs and metrics are infrastructure observations in the Selection Game.
- Verify: test, inspect exported diagnostics across paired interest sets, including malformed matched Events and local errors.
- Status: settled

### MPE-PRV-015 Explicit plaintext disclosure

When an application requests disclosure of Event plaintext outside its authorized audience, the MPE client library shall require explicit application authorization for that disclosure.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §D2; s4 R1 §D2; o4 R1 §D2, report disclosure.
- Rationale: Public contract effects and application reports are outside the sealed-content guarantee.
- Verify: test, exercise ledger submission and reporting paths and confirm that recognition does not authorize plaintext export.
- Status: settled

### Leakage contract

The following rows describe information available at protocol interfaces. They are **architectural inferences** from the proposed interfaces, except where checked code establishes a field. They are not bounds on deductions using auxiliary information.

A row's reference to a field applies only when the selected format or admission mechanism contains that field. Unknown fields must be resolved through MPE-PRV-036. Observations of application-authorized disclosures remain permitted.

| Row | Observer | Permitted observations and residual inference | Protected boundary |
|---|---|---|---|
| L-R | Bus Node | Adjacent peer identities and IPs; Shard subscriptions; Envelope bytes and identifiers; class, expiry, Tag equality if visible; Admission Proof metadata; arrival times, forwarding decisions, and traffic counts. Direct ingress identifies the submitting connection, including a stem predecessor. | Sealed plaintext and logical labels under the cryptographic assumptions; private reception recognition outcomes. |
| L-S | Store Node | L-R plus client connection, service account if used, online intervals, received Shards, requested windows, cursors, catch-up volume, and repair requests. Selective profiles additionally expose their selectors. | Plaintext without secrets; within-Shard selection only in the private reception profile. |
| L-U | Admission issuer | Customer or funding relationship where available, allowance, issuance time, credential identifiers, and submitted Envelope identifiers when issuance binds to them. Joining these records to publication may identify a Publisher. | Plaintext and Subscriber recognition secrets not supplied to the issuer. |
| L-X | Indexer | Public ledger data; queried contract addresses and filters; client connection, cursors, and request schedule. Assisted wallet detection additionally exposes the supplied viewing key to its service boundary. | Off-chain Event plaintext without keys; sealed-topic selection within a commonly downloaded complete stream, subject to the Selection Game. |
| L-L | Chain observer | Registry changes and registrations; transaction times and hashes; contract addresses, entry points, public transcripts, declared effects, public fees, DUST nullifiers and commitments; Anchors, their cadence, and counts if disclosed; public funding information and contract reactions. | Sealed off-chain plaintext and undisclosed witnesses under their cryptographic assumptions. No general payer or reaction unlinkability claim. |
| L-C | Colluding infrastructure | Union of its local observations; enrollment/issuance/ingress joins, repeated-Tag grouping, first-seen estimates, intersection observations, and targeted probing or omission opportunities. | Content under uncompromised-key assumptions; selection only under the complete Selection Game. No minority-based anonymity bound. |
| L-G | Global passive observer | Endpoint participation; uploads, downloads, online intervals, timing, sizes, counts, catch-up patterns, public ledger activity, and application reactions; resulting source and relationship correlations. | Content under uncompromised-key assumptions. Conditional selection privacy supplies no general global anonymity. |
| L-I | Insider or compromised endpoint | Authorized plaintext, recognition capabilities, recognizable traffic, group information supplied by the application, and compromised endpoint state. These can be copied or disclosed. | No protection for information already authorized or compromised; unrelated secrets remain subject to their own boundaries. |

Sources: s1 R1/R2 §D2; s3 R1 §D2; s4 R1/R2 §D2; g1 and g4 R1 §D2; o2 and o4 R2 §D2. Checked interface facts are cited in the requirements below.

### MPE-PRV-016 Bus Node leakage declaration

The MPE shall include L-R in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D2; g1 R1 §D2; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:578`.
- Rationale: GossipSub announces Shard subscriptions to connected peers.
- Verify: inspection, reconcile L-R with serialized fields and instrumented ingress, subscription, and forwarding observations.
- Status: settled

### MPE-PRV-017 Store Node leakage declaration

The MPE shall include L-S in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §D2; s4 R1 §D2.
- Rationale: Complete retrieval conceals selection while exposing access patterns.
- Verify: inspection, reconcile L-S with live, reconnect, back-fill, and repair request traces.
- Status: settled

### MPE-PRV-018 Admission issuer leakage declaration

Where admission issuance is present, the MPE shall include L-U in the applicable privacy profile's leakage declaration.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D2; s4 R1 §D2; o2 R2 §D2.
- Rationale: Admission privacy depends on issuance records and the selected credential construction.
- Verify: inspection, inventory issuer inputs and linkable records for the selected admission mechanism.
- Status: settled

### MPE-PRV-019 Indexer leakage declaration

Where an Indexer read path is present, the MPE shall include L-X in the applicable privacy profile's leakage declaration.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D2; s4 R2 §D2; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`; `midnight-indexer/docs/architecture.md:26`.
- Rationale: A common contract filter reveals bus participation without necessarily revealing the sealed topic.
- Verify: inspection, enumerate GraphQL arguments and supplied secrets for each enabled Indexer path.
- Status: settled

### MPE-PRV-020 Ledger leakage declaration

The MPE shall include L-L in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §D2; s4 R2 §D2; `midnight-ledger@6abe9b16/ledger/src/structure.rs:2646`; `midnight-ledger@6abe9b16/ledger/src/dust.rs:469`.
- Rationale: Addresses, entry points, transcripts, and fee fields are public despite private witnesses.
- Verify: inspection, enumerate public fields of registration, admission, Anchor, fallback, and consumption transactions.
- Status: settled

### MPE-PRV-021 Collusion leakage declaration

The MPE shall include L-C in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1/R2 §D2; s3 R1 §D2; s4 R1 §D2.
- Rationale: Collusion combines service observations without a generic honest-majority privacy threshold.
- Verify: analysis, join issuer, ingress, retrieval, and ledger records and document available correlations.
- Status: settled

### MPE-PRV-022 Global-observer leakage declaration

The MPE shall include L-G in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D2; s3 R1 §D2; g4 R1 §D2.
- Rationale: Payload encryption leaves network-wide activity available for correlation.
- Verify: inspection, compare the declaration with a simulated global observer's traffic and public-action records.
- Status: settled

### MPE-PRV-023 Insider leakage declaration

The MPE shall include L-I in every applicable privacy profile's leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D2; s3 R1 §D2; s4 R1/R2 §D2.
- Rationale: Authorized recipients and compromised endpoints can disclose their information.
- Verify: demonstration, show authorized recognition and plaintext export without treating either as a confidentiality violation.
- Status: settled

### MPE-PRV-024 Launch metadata non-claims

The MPE shall label publisher-message unlinkability, general recipient-message unlinkability, relationship privacy, timing privacy, volume privacy, and hidden participation as unclaimed by the launch profile.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1/R2 §D2; s3 R1 §D2; s4 R1 §D2; g4 R1 §D2.
- Rationale: Conditional local selection privacy does not establish these broader properties.
- Verify: inspection, check profile descriptions, API privacy labels, demonstrations, and claim-register entries for these explicit exclusions.
- Status: settled

### MPE-PRV-025 No anonymity from unsigned transactions

The MPE shall describe the absence of a Substrate signer as a ledger-interface fact without presenting it as proof of publisher or payer unlinkability.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; g4 R1 §D2; s4 R2 §D2; g4 R2 §D2; `midnight-node/pallets/midnight/src/lib.rs:575`.
- Rationale: Public transcripts, funding information, ingress observations, and sparse activity remain relevant.
- Verify: inspection, check ledger privacy descriptions against L-L and their supporting code facts.
- Status: settled

### MPE-PRV-026 Launch compromise-security posture

The MPE shall label content forward secrecy, metadata forward secrecy, and post-compromise security as unclaimed by the launch bus profile.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; g1, g2, g4 R1 §D2; s1 R1 §D2; s2 R2 §D2; `2022-barnes-rfc9180`, §9.1.
- Rationale: A static-key seal does not inherit ratchet erasure or recovery properties.
- Verify: inspection, confirm that profile labels expose the consequences of later key compromise and retained historical keys.
- Status: open (DEC-PRV-4)

### MPE-PRV-027 No launch post-quantum claim

The MPE shall label post-quantum confidentiality as unclaimed by the launch profile.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1, s3, s4 R1 §D2; s2 R1 §D2; `midnight-zk/README.md:12`.
- Rationale: A future hybrid payload mechanism would not establish post-quantum security for the complete bus.
- Verify: inspection, check claim-register exclusions against the selected payload and ledger cryptographic dependencies.
- Status: settled

### MPE-PRV-028 No adversarial archive-erasure claim

The MPE shall describe Envelope expiry as an honest-service retention rule without claiming deletion from adversarial archives.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; g1 R1 §D2; s3 R1 §D2; s4 R1 §D2.
- Rationale: An observer can retain ciphertext after honest services prune it.
- Verify: demonstration, retain a captured Envelope beyond expiry and verify that privacy documentation acknowledges the remaining copy.
- Status: settled

### MPE-PRV-029 No inherited stem anonymity

Where stem forwarding is present, the MPE shall label its source-attribution effect as an unproved heuristic unless analysis covers the implemented construction and adversary.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D2; g1 R1 §D2; s1 R2 §D2; s4 R1 §D2; `2018-fanti-dandelionpp`, §§3.1, 4.1, Theorem 1.
- Rationale: A short stem on GossipSub does not inherit Dandelion++'s model-specific bounds.
- Verify: inspection, check every stem claim against the actual routing graph, adversary, traffic policy, and cited theorem.
- Status: settled

### MPE-PRV-030 Evidence before advertising a property

When a privacy property is advertised as provided, the MPE shall supply reviewed evidence establishing that property's registered game for the implemented profile.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D2; s1 R1 §D10; s3 R1 §D10; s4 R1 §D10.
- Rationale: Component names and successful benchmarks do not prove composed privacy.
- Verify: analysis, audit the claim-to-construction mapping and reject evidence that omits an interface or adversary capability.
- Status: settled

### MPE-PRV-031 Paired selection verification

The Prototype shall produce a paired-execution report comparing complete infrastructure-observable transcripts for Subscribers with different private interests under identical Selection Game inputs.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D10, step 4; s4 R1 §D10, Phase 1.
- Rationale: Whole-client behavior must preserve the transport invariant.
- Verify: test, control clocks and randomness; compare request bytes, sizes, cursors, scheduling decisions, and exported diagnostics; report every difference.
- Status: settled

### MPE-PRV-032 Active selection verification

The Prototype shall exercise the Selection Game under selective omissions, replay, malformed matched traffic, reconnects, and queue pressure.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s1 R1 §D10; s3 R1 §§D9–D10; s4 R2 §D2.
- Rationale: Active probes can expose recognition through recovery or failure handling.
- Verify: test, require unchanged transport policy across paired interests for every enumerated attack; treat any recognition-dependent difference as failure.
- Status: settled

### MPE-PRV-033 Attribution measurements

The Prototype shall report source-attribution precision and recall for random and targeted adversary placements using P-PRV-1.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; s3 R1 §D10; s1 R1 §D10; `2018-fanti-dandelionpp`, §3.2.
- Rationale: Attribution measurements characterize residual leakage rather than establish anonymity.
- Verify: simulation, record topology, actual node counts, controlled connections, bandwidth, operator concentration, admission share, estimator, and results for each placement.
- Status: settled

### MPE-PRV-034 Bound applicability

When literature supplies a quantitative privacy bound, the MPE shall document the mapping from that bound's assumptions and variables to the implemented profile before using it as an MPE guarantee.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D2; s1 R2 §D2; s3 R1 §D2; `2017-das-trilemma`, §V; `2023-guerraoui-inherent-anonymity-gossiping`, §4.2.
- Rationale: Necessary theoretical conditions are not deployment guarantees.
- Verify: analysis, inspect model, graph, observation, traffic, and variable mappings; reject unsupported substitutions.
- Status: settled

### MPE-PRV-035 Violated-claim withdrawal

If verification demonstrates a violation of an advertised privacy game, then the MPE shall mark that profile's affected claim as unsupported.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D2; g4 R1 §D10, T3; s1 R1 §D10; s3 R1 §D10.
- Rationale: A failing property cannot retain its provided label.
- Verify: demonstration, introduce a known recognition leak and confirm that the affected claim fails the release evidence check.
- Status: settled

### MPE-PRV-036 Unknown leakage inventory

When a proposed interface has unresolved privacy-relevant fields, the Prototype shall produce an observation inventory from that interface before the associated profile is accepted.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D2; s4 R1 §D10, Phase 0; s1 R1 §D10, step 1.
- Rationale: Open format and admission choices must not become undocumented leakage.
- Verify: inspection, reconcile packet captures, API arguments, public ledger fields, and remote diagnostics with the profile's leakage declaration.
- Status: settled

### MPE-PRV-037 Separate stronger-profile evidence

Where a stronger privacy profile is present, the MPE shall maintain a separate claim register for its implemented composition.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D2; s3 R1 §§D9–D10; s4 R1 §D2; s1 R1 §D10.
- Rationale: Mix transport, private retrieval, or session security introduces different assumptions and verification obligations.
- Verify: inspection, confirm that experimental results and component guarantees are confined to the separately analyzed profile.
- Status: settled

## Decisions

“Settled” records alignment with the brief's required boundaries or an uncontested verification obligation. It does not assert that a Round 3 consensus vote occurred.

### DEC-PRV-1 — Reception granularity and delegated selection

- **Options and proponents:** Complete shared-feed reception: s1, s3, s4, g4. Complete-Shard reception: g1, g2, g3 and the full-subscriber paths of o1, o2, o4. Selective bucket, Tag, or delegated detection: o1, o2, o3, o4; g3 includes a light-client filter path.
- **Recommended default:** Complete reception of each selected Shard, local recognition, and no delegated secrets or selection predicates in the private reception profile. Declare the complete received Shard set as leakage.
- **Reason:** The brief fixes sharding. Full reception can conceal selection inside that partition; it cannot conceal choosing the partition. Delegated selection receives a separate reduced-privacy label.
- **Settling check:** Run paired Selection Game tests and measure full-Shard reception cost on the intended Consumer classes. If a public Shard mapping identifies an application, record that deduction explicitly. If clients cannot sustain reception, resolve capacity or define another reviewed profile before extending the claim.

### DEC-PRV-2 — Recognition and useful application reactions

- **Options and proponents:** Recognition-independent fetching and fixed public reactions in the privacy game: s1, s3, s4. Normative SDK controls, including no automatic reaction and proposed batching or jitter: o3 R2. Applications issuing later contract transactions: g1, g4, o1, o3.
- **Recommended default:** Recognition alone produces no external action. An application explicitly authorizes a reply, fetch, report, or contract reaction. The resulting activity is declared leakage outside the restricted Selection Game.
- **Reason:** Useful reactions may remain observable. Batching or jitter alone does not establish relationship or timing privacy.
- **Settling check:** Exercise every Consumer callback and external-action path. Accept the default when reception remains recognition-independent and authorized reaction traces are documented. Stronger reaction privacy requires a separate game and composition analysis.

### DEC-PRV-3 — Topic labels, Tags, and recipient-key hiding

- **Options and proponents:** Sealed labels with reviewed wrapper security: s1, s2, s3, s4. Strong Tag/topic unlinkability: o1, o3, o4. g1 asserts that a candidate recipient public key permits trial opening; s1 and s4 R2 reject that assertion.
- **Recommended default:** Require sealed logical labels. Withhold general recipient-key hiding and cross-Envelope topic unlinkability until the chosen wrapper and Tag lifecycle have reviewed evidence. Public Tag equality remains leakage when Tags repeat.
- **Reason:** `2001-bellare-keyprivacy`, §1.1 defines privacy even with known candidate public keys. DH decapsulation requires a secret key (`2022-barnes-rfc9180`, §4.1). A symmetric recognition secret does permit recognition. None of these facts proves the eventual custom wrapper's key privacy.
- **Settling check:** Review the exact wrapper, known-public-key challenge, Tag reuse, dictionary-testable Shard mappings, and secret-compromise cases. Promote only the property supported by that analysis.

### DEC-PRV-4 — Forward secrecy and recovery

- **Options and proponents:** No launch bus forward secrecy or recovery claim: g1, g2, g3, g4. Conditional session-layer guarantees: s1, s2, s3, o1; s4 requires erasure and processed updates. Per-epoch stream forward secrecy: o3.
- **Recommended default:** No launch bus claim for content forward secrecy, metadata forward secrecy, or post-compromise security. Independently reviewed session profiles may state narrower guarantees.
- **Reason:** Static-key encryption lacks recipient-compromise forward secrecy (`2022-barnes-rfc9180`, §9.1). Retained historical, skipped, or invitation keys can defeat stronger claims.
- **Settling check:** CRY specifies the exact compromise, retention, erasure, restart, and update model. Review archived-content exposure and suppressed-update cases before adding a session claim.

### Interpretation of the cited bounds

The anonymity trilemma's synchronized-user Theorem 2 assumes model latency \(\ell<N\) rounds and dummy rate \(\beta\) messages per user per round with \(\beta N\ge1\). It excludes strong anonymity when \(2\ell\beta<1-\epsilon(\eta)\) under its other hypotheses. These are necessary conditions, not a sufficient construction. Gossip replication bytes are not automatically dummy traffic; model rounds are not seconds. Zero-cover cases require the applicable earlier bound rather than substitution outside Theorem 2's premises. Sources: `2017-das-trilemma`, §V, Theorems 1–2; s1 R2 §D2.

For an undirected connected graph and \(f>1\) curious nodes, gossip source \(\epsilon\)-DP requires \(\epsilon\ge\ln(f-1)\). If vertex connectivity \(\kappa(G)\le f\), no finite worst-case \(\epsilon\) exists under that model. Here \(f\) counts nodes, not their fraction. A changing GossipSub mesh requires an explicit model mapping. Source: `2023-guerraoui-inherent-anonymity-gossiping`, §4.2, Theorem 5.

Dandelion++'s cited first-spy comparison assumes a random four-regular anonymity graph unknown to the adversary. Its principal scope distinguishes mass deanonymization from targeted attacks and excludes ISP/AS adversaries. A short stem does not inherit those results. Source: `2018-fanti-dandelionpp`, §§3.1, 4.1, Theorem 1.

## Cross-area dependencies

The following are **provisional expected requirement IDs**, not assertions that other authors have assigned these numbers. The merge must resolve them to actual IDs.

| Expected IDs | Dependency required by PRV |
|---|---|
| MPE-CRY-001, MPE-CRY-002 | Content-sealing construction, authenticated key establishment, recognition security, and wrapper key-privacy analysis. |
| MPE-CRY-003 | Explicit session compromise, erasure, retention, and recovery posture for DEC-PRV-4. |
| MPE-FMT-001, MPE-FMT-002 | Complete public/sealed field inventory and fixed serialized length per configured class. |
| MPE-PUB-001, MPE-PUB-002 | Complete-Shard reception and recognition-independent live, back-fill, reconnect, and repair behavior. |
| MPE-CON-001, MPE-CON-002 | Explicit application reactions and inventory of contract-consumption disclosures. |
| MPE-NET-001, MPE-NET-002 | GossipSub origin-field policy and privacy-profile handling of fallback. `StrictNoSign` omits origin fields but does not provide source anonymity; see `specs/pubsub/README.md:271`. |
| MPE-ECO-001 | Admission credential visibility, issuance linkability, repeated identifiers, and exceptional identity disclosure. |
| MPE-SEC-001, MPE-SEC-002 | Active probing scenarios and bounded failure handling that preserves private reception. |
| MPE-STO-001 | Retention and catch-up interfaces whose access patterns are included in L-S. |
| MPE-PRF-001 | Measured full-Shard costs for supported Consumer classes; no privacy-preserving mobile feasibility assumption. |
| MPE-VER-001, MPE-VER-002 | Paired transcript checks, adversarial experiments, and claim-specific acceptance evidence. |
| MPE-OPS-001 | Operator trust boundaries and remotely exported diagnostics included in the leakage inventory. |

## Glossary additions

| Term | Meaning |
|---|---|
| Logical topic | Application-level audience or stream label, distinct from a Shard. |
| Privacy profile | Named combination of interfaces, behavior, assumptions, claims, and declared leakage. |
| Private reception profile | Complete-Shard reception with local recognition and recognition-independent transport. |
| Recognition outcome | Local determination that an Envelope belongs to the Subscriber's interests or can be opened. |
| Recognition capability | Secret material enabling recognition of selected Envelopes. |
| Trusted endpoint boundary | Devices or processes the Subscriber authorizes to hold its recognition or decryption secrets. |
| Claim register | Profile-specific record defined by MPE-PRV-001. |
| Leakage contract | Declared protocol observations and residual inference opportunities; not a bound on auxiliary knowledge. |
| Admission issuer | Party issuing a credential or authorization used by an Admission Proof, where that mechanism exists. |
| Key privacy | Cryptographic concealment of which candidate public key was used for encryption. |
| Content forward secrecy | Protection of past content after a specified later compromise, subject to explicit erasure conditions. |
| Post-compromise security | Recovery of specified confidentiality after compromise through an uncompromised update. |
| First-spy estimator | Source-attribution estimator using the first observed propagation into an adversary's controlled set. |

## Gaps

- **Exact wrapper and Tag behavior are unknown.** The proposals differ on static recognition, fresh Tags, repeated epoch Tags, and encrypted session headers. PRV can require label concealment and evidence gates; it cannot presently assign a recipient-anonymity or topic-unlinkability bound.

- **Admission unlinkability is unresolved.** RLN membership-witness hiding, one-time tickets, blind issuance, and visible membership keys expose different information. None alone establishes ingress anonymity or relationship privacy. ECO and CRY must instantiate L-U and the Admission Proof portion of L-R.

- **No numerical selection-privacy advantage is supported for the composed client.** Transcript equality checks provide concrete acceptance evidence for the specified cases. They do not prove absence of all runtime timing channels or unrestricted application correlations.

- **No launch anonymity-set floor is established.** Low traffic and publicly identifiable Shards can sharply narrow attribution. Proposed cover floors and decoy-fetch uncertainty lack a reviewed bound for this deployment.

- **Operator content-blindness has a technical boundary.** Operators lacking secrets cannot read sealed content under the stated assumptions. “Cannot classify anything” and “cannot be compelled” exceed that property because metadata, insiders, endpoint compromise, and legal behavior remain outside the cryptographic claim.

- **Recipient-only disclosure is unsupported.** A Publisher already knows its Event; an authorized recipient can copy plaintext. Reporting mechanisms can authenticate particular disclosures but cannot make recipients the only parties capable of revealing content.

- **Midnight deployment generation is unknown.** The checked local ledger-9 and Indexer interfaces establish available code behavior, not activation on the intended deployment. Privacy declarations for the `Misc` fallback must be checked against the actual target generation.

- **Evidence index discrepancy:** The local text `graph/text/2021-seres-fmdfalsepositives.txt` exists, but its cited slug was not found in the supplied `papers.tsv`. Delegated-detection requirements therefore trace to the proposal/review objections without treating that slug as a verified catalog entry.

- **The supplied s3 Round 2 Markdown file is absent.** Its available incomplete log supplies no review position for this area; s3 evidence here comes from its Round 1 proposal.

- **Graph summaries are navigation evidence.** Their communities and digests do not establish the privacy properties or override the checked papers' hypotheses.