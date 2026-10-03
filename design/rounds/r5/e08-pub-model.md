# MPE-PUB: Publish and subscribe model and delivery semantics (D3)

## 1. Scope of this area

This area covers how Publishers address Events and how Subscribers recognise them: Shards, Tags, audience keys, invitations and discovery. It also covers how a Subscriber receives a Shard without revealing which topics it follows, the delivery contract the MPE client library gives applications (at-least-once delivery, duplicates, ordering, gaps, replay, back-fill and cursors), and what Publishers, Subscribers, Bus Nodes and Store Nodes do on failure and overload. It does not cover the Envelope byte layout, admission and rate limits, the mesh parameters, retention windows, contract-side verification or the privacy claims themselves. Those belong to other areas and are listed in section 5.

## 2. Parameters

| ID | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-PUB-1 | Shard count, a Registry parameter | 1 | 1–16 | g1 D3 (1 at launch); g2, g3 and o4 (8); o2 (16); DEC-PUB-1 |
| P-PUB-2 | Pull cadence while retrieving a Shard by pull | 1 s | 1–10 s | s1 D3 |
| P-PUB-3 | Interval for reconciling against a second source | 60 s | 30–600 s | s1 D3; o3 R2 D7 and D9 |
| P-PUB-4 | Maximum recognition keys per Subscriber | 256 | 16–4,096 | s2 D3 |
| P-PUB-5 | Time a Publisher waits for Bus Node acceptance before retrying | 5 s | 1–30 s | **assumption** (2.5 × g2's class-S p99 target of 2 s) |
| P-PUB-6 | Distinct Bus Nodes tried per publication | 3 | 1–8 | **assumption**; g2 D3 ("several honest outbound peers") |
| P-PUB-7 | Wait before a missing sequence number is reported as a gap | 120 s | 10–600 s | o3 D3.3 (`T_gap` = 20 blocks ≈ 2 min) |
| P-PUB-8 | Clock-skew allowance | 120 s | 10–300 s | g1 D1 (a relay's clock stays within 120 s of the latest block time) |
| P-PUB-9 | Back-fill page size | 64 Envelopes | 1–500 | g1 D1 (1–64); indexer clamp of 1–500 cited by g4 (`midnight-network-stack.md` §4.7) |
| P-PUB-10 | Concurrent full-Shard pulls served by one Bus Node | 8 | 1–64 | g2 D5 |
| P-PUB-11 | Silence before the client reports `disconnected` | 30 s | 5–300 s | **assumption** |

`L_max` is the maximum Envelope lifetime. The format and storage areas define it (see section 6). The proposals range from 300 s (g1, class 3) to 14 days (g4, o2).

## 3. Requirements

### Topics, Shards, Tags and discovery

### MPE-PUB-001 Topic identifiers sealed
The MPE client library shall place every application topic identifier, session identifier and recipient identifier only inside the sealed body of an Envelope.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, s1, s2, s3, s4, g4, o3; `2020-vac-waku2-filter-spec` lines 298-300 (a filter node learns content topics)
- Rationale: A topic that relays can read is the interest leak this design exists to avoid. g2's clear topics on open Shards are not adopted; see MPE-PUB-007.
- Verify: test. Publish 10,000 Envelopes on 100 topics. Bus Node captures contain none of the topic, session or recipient identifiers as byte strings.
- Status: settled

### MPE-PUB-002 Shard derivation
The MPE client library shall set an Envelope's Shard to a domain-separated SHA-256 hash of the audience key, reduced modulo P-PUB-1 as read from the Registry.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1 (computed, `shard_count` = 1), g3, o4 (`H(K) mod 8`), o2 (`H(topic_id) mod 16`); g1 R2 objection that a shard derived from a label can be guessed
- Rationale: A computed placement keeps each topic on one Shard. Using a secret key as input stops anyone testing which Shard a guessed label lands on.
- Verify: test. Vectors for 1,000 keys at P-PUB-1 ∈ {1, 8, 16} match a reference implementation.
- Status: open (DEC-PUB-1)

### MPE-PUB-003 Bus Node shard-count transition
When the Registry changes P-PUB-1, the Bus Node shall accept Envelopes placed under either the previous or the new value until `L_max` plus P-PUB-8 has elapsed after the change takes effect.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D3; g1 D3 ("in-flight objects keep the old mapping until they expire")
- Rationale: Without this, Envelopes that are valid but already in flight would be rejected as invalid at the cut-over.
- Verify: simulation. Change from 1 to 8 Shards under load. No Envelope is rejected for a shard mismatch during the transition.
- Status: settled

### MPE-PUB-004 Client shard-count transition
When the Registry changes P-PUB-1, the MPE client library shall follow each audience key's Shards under both the previous and the new value until `L_max` plus P-PUB-8 has elapsed after the change takes effect.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D3; g1 D3 ("subscribers follow the new mapping")
- Rationale: The receiving side of MPE-PUB-003. Without it, Events published just before the change would be lost.
- Verify: simulation. No Event is lost across a change from 1 to 8 Shards.
- Status: settled

### MPE-PUB-005 Per-Envelope Tag
The MPE client library shall compute each Envelope's Tag as a keyed pseudorandom function of the audience key and a fresh random salt carried in that Envelope.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s4 D1 (salted, truncated PRF hint); o1, o4 and o3 R1 (keyed PRF tags); o3 R2 (withdrew the 32-tag lookahead window); s4 R2 (bucket arithmetic)
- Rationale: Tags cannot be linked without the key, recognition costs one PRF evaluation per key, and there is no sequence window that can fall out of step.
- Verify: test. Across 10⁶ Envelopes under one key, no Tag repeats and a chi-square test does not reject uniform Tag bytes at α = 0.01. Inspection: a cryptographic review of the construction.
- Status: open (DEC-PUB-2)

### MPE-PUB-006 Random private audience keys
The MPE client library shall generate every private audience key as 32 bytes drawn from the operating system's cryptographically secure random source.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g4 D3 (forbids passphrase topics and Bitmessage-style chans); `2021-len-partitioningoracle` (ChaCha20-Poly1305 is not key-committing)
- Rationale: Low-entropy keys make it possible to guess and test topics. They are also the setting in which one ciphertext can open under several keys.
- Verify: inspection. The API offers no passphrase input for private topics. Test: generated keys pass NIST SP 800-22 frequency tests (**assumption**: the test suite choice is this author's).
- Status: settled

### MPE-PUB-007 Public topic key
Where a topic is public, the MPE client library shall derive its audience key as a domain-separated hash of the published topic name.
- Pattern: optional
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D3.1 (`k_s = H("public" ‖ name)`), o1 (public topics), o2 (sealed contract topics that anyone can derive), g4 (key published beside the contract)
- Rationale: One mechanism serves both kinds of topic, so relays cannot tell a public Envelope from a private one.
- Verify: test. Known-answer vectors. Public and private Envelopes cannot be told apart by any header field.
- Status: settled

### MPE-PUB-008 Invitation-only private membership
The MPE client library shall add a private topic to a Subscriber only by importing an invitation received outside the bus.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1, s2, s4 (no unsolicited first contact in v1); g1, g4 (out-of-band keys); o4 R2 (harassment vector); o1, o3, o4 (inbox alternatives)
- Rationale: An open inbox lets anyone who knows a key reach its holder for the price of an Admission Proof.
- Verify: inspection. The API exposes no other way in. Test: an Envelope sent under an unregistered recipient key is never surfaced.
- Status: open (DEC-PUB-3)

### MPE-PUB-009 No subscriber directory
MPE shall provide no Bus Node, Store Node or Registry operation that returns which Subscribers follow a topic, Tag or audience key.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g4, s3, s4, o2, o4 (no directory, because a directory would leak interest)
- Rationale: Any lookup service would become a public list of interests.
- Verify: inspection of the protocol identifiers and Registry entry points.
- Status: settled

### Subscribing without revealing interest

### MPE-PUB-010 Local recognition
The MPE client library shall not send any audience key, recognition key or Tag filter to a Bus Node, Store Node or Indexer.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g4, s1, s2, s3, s4; `2014-gervais-bloomfilters` lines 69-71; `2021-seres-fmdfalsepositives` lines 95-96; `midnight-indexer/docs/architecture.md:20` (the indexer stores wallet viewing keys, cited by s1 and checked by g1 R2)
- Rationale: Handing a filter or detection key to a server reveals interest. Bloom-filter and FMD studies show how much.
- Verify: test. Capture all client egress for 24 h. No key or Tag-filter material appears.
- Status: settled

### MPE-PUB-011 Full-Shard reception
While in the default reception mode, the MPE client library shall retrieve every unexpired Envelope of each Shard it follows.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g4, s1, s2, s3, s4, o3 R2; `1998-chor-pir` (with a single server, perfect privacy costs a full download, per g2 D2)
- Rationale: Fetching everything is the only reception mode whose interest privacy needs no new cryptography.
- Verify: simulation. The count received equals the Shard's publication count minus expired Envelopes.
- Status: settled

### MPE-PUB-012 Network behaviour independent of recognition
The MPE client library shall send network messages whose content, size and timing do not depend on which Envelopes match the Subscriber's keys.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1 D2 (interest game) and D3; g1 R2 objection on retries; o3 R2 D2; `2024-gegenhuber-careless-whisper` (receipts are a metadata channel, per g2 D2)
- Rationale: The interest claim holds only if the fetch transcript is fixed. This rules out acknowledgements and retries triggered by a match.
- Verify: test. Two clients follow the same Shards for 1 h with 0 and 256 keys. Their request counts and sizes are identical, and a KS test at α = 0.01 does not distinguish their timing.
- Status: settled

### MPE-PUB-013 Fixed pull cadence
While retrieving a Shard by pull, the MPE client library shall request new Envelopes every P-PUB-2 seconds.
- Pattern: state
- Scope: POC
- Priority: SHOULD
- Source: D3; s1 D3; o4 R2 (vote)
- Rationale: A fixed schedule removes any timing signal that adaptive polling would carry.
- Verify: test. The standard deviation of inter-request intervals over 1 h is at most 50 ms.
- Status: open (DEC-PUB-4)

### MPE-PUB-014 Second-source reconciliation
While following a Shard, the MPE client library shall reconcile its received Envelope identifiers against a second, independently operated Bus Node or Store Node every P-PUB-3 seconds.
- Pattern: state
- Scope: POC
- Priority: SHOULD
- Source: D3; s1 D3; o3 R2 (D7 and D9: cross-checking is the default defence against omission); o4 R2
- Rationale: Sequence gaps cannot reveal omission of whole publishers or of first contacts. A second source can.
- Verify: simulation. One serving Bus Node silently drops 5% of Envelopes. The client obtains every dropped Envelope that the second source holds within 2 × P-PUB-3.
- Status: open (DEC-PUB-4)

### MPE-PUB-015 Repair every difference
When reconciliation finds an Envelope identifier that the client has not received, the MPE client library shall fetch that Envelope.
- Pattern: event
- Scope: POC
- Priority: SHOULD
- Source: D3; s1 D3 ("repair all differences, independent of private matches")
- Rationale: Repairing only matched Envelopes would reveal which Envelopes matched.
- Verify: test. Every missing identifier is fetched, whatever the client's key set.
- Status: open (DEC-PUB-4)

### MPE-PUB-016 Reduced-privacy mode opt-in
Where a reduced-privacy retrieval mode is present, the MPE client library shall enable it only after an explicit opt-in by the application for each subscription.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D3; o1 R2 (bucket and tag-index profile kept only with a label); o3 R1 (bucket opt-in); g2 (filter push as a "privacy downgrade"); g3 (filter node); o2 (S-FMD)
- Rationale: Bandwidth-saving modes leak a selector, so the leak must be a deliberate choice and never a default.
- Verify: inspection and test. The default configuration never sends a selector. Opting in for one subscription does not change any other subscription.
- Status: open (DEC-PUB-5)

### MPE-PUB-017 Report disclosed Shards
The MPE client library shall report, for each subscription, the Shard identifiers it has announced to connected peers.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; g2 D2 (GossipSub `SubOpts` give the Shard to direct peers); `libp2p/specs/pubsub/README.md:95-100` (`SubOpts.topicid`)
- Rationale: Shard membership is visible to peers. The library states this leak instead of implying topic-level privacy at the mesh.
- Verify: test. The reported set equals the topic IDs found in captured `SubOpts`.
- Status: settled

### MPE-PUB-018 Recognition key cap
If adding a recognition key would raise the Subscriber's key set above P-PUB-4 keys, then the MPE client library shall refuse the addition with a typed `KeyLimit` error.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s2 D3 (256-key cap including all categories)
- Rationale: The cap bounds the recognition work per Envelope at P-PUB-4 PRF evaluations.
- Verify: test. Adding key P-PUB-4 + 1 returns `KeyLimit`, and the key set is unchanged.
- Status: settled

### Publisher behaviour

### MPE-PUB-019 Per-publisher sequence number
The MPE client library shall seal in each Event a sequence number one greater than the same publisher's previous Event on the same topic.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g3, o1, o2, o3, o4, s1, s3, s4
- Rationale: This gives per-publisher order and gap detection without revealing either to relays.
- Verify: test. 1,000 Events produce sealed sequence numbers n…n+999.
- Status: settled

### MPE-PUB-020 Logical event identifier
The MPE client library shall seal in each Event a logical event identifier that stays the same across every republication of that Event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1, s3, s4 (retries keep the original logical identifier)
- Rationale: A republication that needs a new Admission Proof has a new Envelope identifier. The logical identifier still lets Subscribers remove the duplicate.
- Verify: test. Republishing after a failure yields two Envelope identifiers with one logical identifier.
- Status: settled

### MPE-PUB-021 Oversize refusal
If an Event exceeds the largest size-class body, then the MPE client library shall refuse the publication with a `TooLarge` error before requesting an Admission Proof.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D1 and D3.4 (no silent drop); g1 D1
- Rationale: Failing early spends no admission credit and never truncates silently.
- Verify: test. A body one byte over the limit returns `TooLarge`, and the admission counter is unchanged.
- Status: settled

### MPE-PUB-022 Acceptance before success
When the MPE client library submits an Envelope, the MPE client library shall report it `accepted` only after a Bus Node returns the GossipSub validation result Accept for that Envelope identifier.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g1 D3 (return when a mesh peer holds it); s1 D3 (an acknowledgement means storage acceptance, never recognition); o3 D3.4; `midnight-js/packages/types/src/public-data-provider.ts:507-508`
- Rationale: A transport failure must never surface as a completed publication.
- Verify: test. Against a Bus Node that drops input silently, the client never reports `accepted`.
- Status: settled

### MPE-PUB-023 Identical retransmission
While an Envelope is unexpired, if no acceptance arrives within P-PUB-5 seconds, then the MPE client library shall resubmit the identical Envelope bytes to a different Bus Node, up to P-PUB-6 Bus Nodes in total.
- Pattern: complex
- Scope: POC
- Priority: MUST
- Source: D3; s3 D3 (exact-cell retransmission during the admission window); g2 D3 (censorship resistance comes from several outbound peers)
- Rationale: Identical bytes keep one identifier, so a retry costs no new admission and is removed as a duplicate.
- Verify: test. With the first Bus Node blackholed, the second receives byte-identical bytes, and retransmission stops at expiry.
- Status: settled

### MPE-PUB-024 Publication failure
If all P-PUB-6 attempts end without acceptance, then the MPE client library shall report the publication as failed with the error `NotAccepted`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4 (typed, closed errors)
- Rationale: The application decides whether to republish under the same logical identifier (MPE-PUB-020).
- Verify: test. With all Bus Nodes blackholed, the result is `NotAccepted` after P-PUB-6 × P-PUB-5 seconds.
- Status: settled

### MPE-PUB-025 Closed error set
The MPE client library shall return every publish and subscribe failure as one member of a closed, versioned, typed error set.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4
- Rationale: Applications can only handle exhaustively the failures they are able to name.
- Verify: inspection of the API. Fault injection maps each of 20 injected faults to exactly one documented error.
- Status: settled

### Bus Node and Store Node delivery behaviour

### MPE-PUB-026 GossipSub message identifier
The Bus Node shall configure GossipSub to use the Envelope identifier, a domain-separated hash of every Envelope byte, as the message identifier.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1 R2 D1 (every forwarded byte in the identifier); `rust-libp2p/protocols/gossipsub/src/config.rs:526-539` (default identifier is source plus seqno); `behaviour.rs:121-125` (anonymous mode needs a custom identifier); `libp2p/specs/pubsub/README.md:174-192`
- Rationale: With no author and no seqno, the default identifier makes every message from a peer collide.
- Verify: test. Envelopes differing in one byte get distinct identifiers. Identical Envelopes get the same identifier.
- Status: settled

### MPE-PUB-027 Seen-set until expiry
The Bus Node shall keep each accepted Envelope identifier in a seen-set until that Envelope's expiry plus P-PUB-8.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1 (seen-set held until expiry); o1, o4 (seen cache plus expiry); `rust-libp2p/protocols/gossipsub/src/config.rs:524` (`duplicate_cache_time` is 60 s)
- Rationale: GossipSub's 60 s duplicate cache is shorter than an Envelope's lifetime, so an Envelope replayed later would flood the mesh again.
- Verify: test. Replays at 61 s and at expiry − 1 s are not forwarded.
- Status: settled

### MPE-PUB-028 Duplicate is Ignore
When the Bus Node receives an Envelope whose identifier is in its seen-set, the Bus Node shall return the GossipSub validation result Ignore.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1; `rust-libp2p/protocols/gossipsub/src/types.rs:51-58`; `libp2p/specs/pubsub/gossipsub/gossipsub-v1.1.md:536`
- Rationale: Duplicates are normal at-least-once traffic and must not cost an honest peer its P₄ score.
- Verify: test. The forwarding peer's score is unchanged after 100 duplicates.
- Status: settled

### MPE-PUB-029 Expired on arrival is Ignore
If an Envelope's expiry is earlier than the Bus Node's clock minus P-PUB-8, then the Bus Node shall return Ignore without storing the Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1 ("merely expired on arrival is Ignore")
- Rationale: Expiry bounds the replay window. A late copy is not misbehaviour by the peer that forwarded it.
- Verify: test. An expired Envelope is neither stored nor forwarded, and the sender's score is unchanged.
- Status: settled

### MPE-PUB-030 Back-fill selectors
The Store Node shall select back-fill responses only by Shard, time window and continuation cursor.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g3, s1, s2, s3, s4; `2020-vac-waku2-store-spec` lines 366-367 (the store learns content filters, confirmed in o3 R2)
- Rationale: A topic-based or Tag-based query would tell the store who wants which Envelope.
- Verify: inspection of the back-fill request format. It has no Tag, topic or identifier-list field.
- Status: open (DEC-PUB-5)

### MPE-PUB-031 Back-fill completeness
When the Store Node answers a back-fill request, the Store Node shall return every Envelope it holds for the requested Shard and window, in pages of at most P-PUB-9 Envelopes, each page ending with a continuation cursor.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1 (bounded pages); s4 D3 (complete windows)
- Rationale: Partial windows would hide omission behind pagination.
- Verify: test. A store holding N Envelopes in the window returns exactly N distinct identifiers across all pages.
- Status: settled

### MPE-PUB-032 Refusal is distinguishable
If the Store Node does not serve a back-fill request in full, then the Store Node shall return a typed refusal distinct from an empty result.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; g1 D3 ("a relay may refuse backfill"); o3 D3.4 (no silent completion)
- Rationale: An empty page that really means "refused" is silent omission.
- Verify: test. A store over its rate limit returns `Refused`, never an empty page.
- Status: settled

### MPE-PUB-033 Pull capacity
If a Bus Node already serves P-PUB-10 concurrent full-Shard pulls, then the Bus Node shall refuse a further pull with a typed `Busy` response.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; g2 D5 (serving 200 pullers at 40 KiB/s each, 8 × 10⁶ B/s, exceeds the relay cap)
- Rationale: Fan-out to pullers must not starve the mesh.
- Verify: test. Pull number P-PUB-10 + 1 gets `Busy`, and the existing pulls are unaffected.
- Status: settled

### MPE-PUB-034 Busy fail-over
When a Bus Node refuses a pull as `Busy`, the MPE client library shall request the pull from another Bus Node in the Registry relay list.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g2 D5; g3 D3
- Rationale: Refusal under load should move the client to another node, not leave it without a feed.
- Verify: test. The client is receiving from a second Bus Node within 2 × P-PUB-2.
- Status: settled

### Delivery contract to the application

### MPE-PUB-035 At-least-once delivery
While an Envelope is unexpired and held by a correctly operating Bus Node or Store Node that the Subscriber can reach, MPE shall deliver that Envelope to the Subscriber's client library at least once.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g3, o1, o2, o3, o4, s1, s3, s4 (all at-least-once within retention)
- Rationale: This is the strongest guarantee a store-bounded overlay can give. s4 conditions it on a reachable copy.
- Verify: simulation. 16 Bus Nodes, 20% churn, 1,000 Envelopes. Every continuously connected Subscriber receives every Envelope.
- Status: settled

### MPE-PUB-036 Envelope deduplication
The MPE client library shall pass each Envelope identifier to the application at most once per subscription store.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; all proposals; `midnight-js/packages/types/src/public-data-provider.ts:507-508`
- Rationale: The mesh, back-fill and reconciliation each produce duplicates by design.
- Verify: test. Each Envelope is injected three times across the three paths, and the application sees it once.
- Status: settled

### MPE-PUB-037 Logical deduplication
The MPE client library shall pass each authenticated pair of publisher and logical event identifier to the application at most once per subscription store.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1, s3, s4
- Rationale: Republications have new Envelope identifiers (MPE-PUB-020).
- Verify: test. Two Envelopes carrying one logical identifier produce one delivery.
- Status: settled

### MPE-PUB-038 Arrival-order delivery
The MPE client library shall deliver Events in the order it authenticates them, holding no Event back to restore sequence order.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3(2) (no hidden reorder buffer); s3 (bounded reordering); o1, o2 (anchor order)
- Rationale: Hidden buffering is how consumers lose Events when they crash. Gaps are reported instead.
- Verify: test. Events with sequence numbers 3 then 2 are delivered as 3, then 2 marked `late`.
- Status: open (DEC-PUB-6)

### MPE-PUB-039 Gap report
If a missing sequence number has not arrived P-PUB-7 seconds after a later number from the same publisher and topic, then the MPE client library shall emit a `gap` item naming the publisher and the missing range.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3(7); s3, s4, o1 (explicit gaps)
- Rationale: Omission inside a known stream becomes visible instead of silent.
- Verify: test. Withholding sequence number 5 produces `gap{5..5}` at P-PUB-7 ± 1 s.
- Status: settled

### MPE-PUB-040 Late fill
When an Event arrives whose sequence number lies inside an open gap, the MPE client library shall deliver it as a `late` item.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3(2) and D3.4
- Rationale: The application learns that an earlier gap has been filled.
- Verify: test. Releasing the withheld Event yields `late` with sequence number 5.
- Status: settled

### MPE-PUB-041 Gap becomes lost
If a gap is still open `L_max` plus P-PUB-8 after it was emitted, then the MPE client library shall mark that gap `lost`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; g1 D3 ("after expiry it is loss")
- Rationale: No valid copy can still exist, so waiting longer has no purpose.
- Verify: test. A `lost` item is emitted at `L_max` + P-PUB-8 ± 1 s.
- Status: settled

### MPE-PUB-042 Caught-up marker
When back-fill reaches the newest Envelope the serving node holds, the MPE client library shall emit a `head` item carrying the current cursor.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3(6); `nostr-nip-01` lines 153, 161 (`EOSE`)
- Rationale: Consumers need to know when the replay is complete and live delivery begins.
- Verify: test. Exactly one `head` per back-fill, emitted after the last stored Envelope.
- Status: settled

### MPE-PUB-043 Portable inclusive cursor
The MPE client library shall resume a subscription from an inclusive cursor defined only by Envelope header fields and wall-clock time, never by a row number local to one node.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D1 and R2; `midnight-indexer/docs/re-indexing.md:78-92` (two instances, secondary re-indexed from empty); s1 (inclusive cursors); g1 D1 (back-fill keyed by expiry)
- Rationale: Row numbers differ between nodes, so a fail-over can skip Events.
- Verify: test. Switching mid-back-fill between two Store Nodes with different ingest orders skips no Envelope.
- Status: settled

### MPE-PUB-044 Atomic processing helper
Where the application uses the library's idempotent processing helper, the MPE client library shall commit the cursor, the deduplication record and the application's effect in one atomic write.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4 (`processOnce`); s2, s3 (cursor and processing committed atomically)
- Rationale: This gives an exactly-once effect on top of at-least-once delivery.
- Verify: test. Kill the process at 1,000 random points (o3 D10 zero-loss chaos test). Each Event's effect occurs exactly once.
- Status: settled

### MPE-PUB-045 Retention exceeded
If a subscription resumes from a cursor older than the earliest Envelope any reachable Store Node holds, then the MPE client library shall emit a `gap` item with reason `retention-exceeded` for the unreachable interval.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 R2 D6 (offline beyond retention must be visible)
- Rationale: Otherwise "at least once within retention" silently becomes "at most once" for clients that are often offline.
- Verify: test. A client offline for longer than retention receives this `gap` before any Event.
- Status: settled

### MPE-PUB-046 Key erased
If a back-fill interval predates the oldest recognition key the Subscriber retains for a topic, then the MPE client library shall emit a `gap` item with reason `key-erased` for that topic and interval.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D3; o3 D3.3(5); s2 D3 ("storage availability does not imply decryptability")
- Rationale: A ratcheted key that has been deleted makes stored Events unreadable, and the client must say so.
- Verify: test. After erasing epoch-1 keys, back-filling epoch 1 yields `key-erased`.
- Status: settled

### MPE-PUB-047 Reactions only on explicit call
The MPE client library shall submit a transaction or publication that reacts to an Event only when the application explicitly calls a reaction operation.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 R2 D2 (no automatic reaction); s4 D2 (reactions re-correlate); s1 D3
- Rationale: An automatic reaction links the reactor to the Event through timing.
- Verify: inspection. No code path in the library sends a reaction except a reaction call.
- Status: settled

### MPE-PUB-048 External object fetch
Where an Event references an external object, the MPE client library shall fetch that object only through a separate operation that the API marks as interest-revealing.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 R2 D2 (blob fetches flagged in the type system); s4 D1 (declared fetch leakage)
- Rationale: A fetch reveals interest. Exposing it as its own call keeps the leak deliberate.
- Verify: inspection. Delivering an Event never triggers a fetch, and the fetch operation's type carries the marker.
- Status: settled

### MPE-PUB-049 Unknown schema
If an authenticated Event carries a schema identifier the application has not registered, then the MPE client library shall deliver it as an `undecodable` item.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D1 (deliver unknown schemas, never drop them); `design/evidence/bitmessage-guide.md:354-358` (`eval` on decrypted data, cited by o3)
- Rationale: Dropping Events silently breaks the gap accounting, and dynamic decoding is an attack surface.
- Verify: test. An Event with an unregistered schema arrives as `undecodable` with its sequence number.
- Status: settled

### MPE-PUB-050 Disconnected status
If the MPE client library has received no response from any Bus Node or Store Node for P-PUB-11 seconds, then the MPE client library shall emit a `disconnected` status item.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4 (no silent transport failure)
- Rationale: A stalled feed must not look like a quiet one.
- Verify: test. Partitioning the client yields `disconnected` at P-PUB-11 ± 1 s.
- Status: settled

### Prototype obligations

### MPE-PUB-051 Validation before forwarding
The Prototype shall run every Bus Node with GossipSub application validation enabled, so that no Envelope is forwarded before its validation result.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1, g2 D1 (Accept, Reject and Ignore validators); `rust-libp2p/protocols/gossipsub/src/config.rs:525` (`validate_messages` defaults to false)
- Rationale: With the library default, Envelopes are forwarded before the seen-set and expiry checks run.
- Verify: test. An Envelope held in validation for 2 s reaches no peer during those 2 s.
- Status: settled

### MPE-PUB-052 Subscriber bandwidth measurement
The Prototype shall measure bytes received per Subscriber per day in full-Shard mode at P-PUB-1 = 1 and P-PUB-1 = 8, under the performance area's reference load.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 R2 D3 and D5 (the per-consumer cost is never gated); s1 R2 and s4 R2 (mobile cost of full-feed reception)
- Rationale: This is the number that settles DEC-PUB-1 and DEC-PUB-5. Today it is computed, not measured.
- Verify: demonstration. A 24-hour run, with the measured bytes reported against the arithmetic in DEC-PUB-1.
- Status: settled

## 4. Decisions

### DEC-PUB-1 Shard count and assignment
- **Options.** (a) One feed (P-PUB-1 = 1) with the Shard field kept for growth: g1, and the one-feed designs of s1, s2, s3 and s4. (b) Eight Shards: g2 (at most 8 per relay), g3 (`H(contract) mod 8`), o4 (`H(K) mod 8`). (c) Sixteen: o2, and o1's sixteen buckets.
- **Round 2.** Votes for one feed or full-stream reception: g1, g2, g4, o1, o3, o4, s1, s2 and s4. Votes for Shards: g3 and o2. s3's review is incomplete.
- **Recommended default.** (a): a computed assignment (MPE-PUB-002), P-PUB-1 = 1 at launch, raised by the Registry only after measurement.
- **Reason.** Each extra Shard divides the anonymity set and reveals per-Shard volume (o2 R2 objection). Sharding also does not by itself bring a mobile client within budget. At s4's planning load (10 Envelopes/s × 2 KiB), one feed costs 1.77 GB/day per Subscriber (checked in o3 R2), and one of eight uniform Shards costs about 221 MB/day. Both are far above the 56–60 MB/day consumer budgets of g4 and o3.
- **Settling check.** MPE-PUB-052, plus the performance area's consumer budget. Raise P-PUB-1 when one Shard exceeds the relay or Subscriber budget and the projected per-Shard anonymity set stays above the privacy area's floor.

### DEC-PUB-2 Recognition mechanism and Tag
- **Options.** (a) No public Tag; trial AEAD on every Envelope: g1, g3, g4, and o3 in R2. (b) PRF Tags indexed by sequence with a lookahead window: o1, o3 R1, o4 (direct channels). (c) Time-rotated topic Tags: o4 (hourly broadcast) and o1 (public topics). These are linkable within each period. (d) A salted PRF hint per Envelope: s4. (e) A trial on an encrypted header: s2 and s3.
- **Recommended default.** (d).
- **Reason.** It is as unlinkable as (a) and (e) and matches the glossary's Tag. It costs one PRF per key per Envelope: at P-PUB-4 = 256 keys and 10 Envelopes/s, that is 2,560 evaluations/s. It also avoids the lookahead desynchronisation that o3 withdrew in R2, and the bucket inconsistency s4 R2 computed (32 lookahead tags cover about 13.97 of 16 buckets).
- **Unknowns.** The per-evaluation cost on phone hardware.
- **Settling check.** A Prototype benchmark at 256 keys on reference desktop and phone hardware, plus the cryptographic review that s4 makes a condition.

### DEC-PUB-3 First contact
- **Options.** (a) Out-of-band invitations only at launch: s1, s2, s4, with o4 R2 accepting it as one remedy. (b) An ECDH inbox to a published key: g1, o3. (c) An inbox with an FMD clue: o1, and o2's S-FMD. (d) A dedicated intro inbox with a stricter rate tier: o4.
- **Recommended default.** (a) for the Prototype and launch. (d) can be a later PROD profile.
- **Reason.** An open inbox is a harassment vector (o4 R2). A clue on every Envelope adds visible structure (g1 R2). FMD leaks the social graph to the detection server (`2021-seres-fmdfalsepositives` lines 95-96).
- **Settling check.** A stated product requirement for unsolicited contact, plus a red-team pass on the intro-tier rate limit.

### DEC-PUB-4 Fetch cadence and second-source reconciliation
- **Options.** (a) A fixed pull cadence plus reconciliation against an independent second source: s1, with o3 R2 and o4 R2 in support. (b) A single source, with sequence-gap detection only: g1, g4, o1, o2.
- **Recommended default.** (a).
- **Reason.** Gaps cannot reveal the suppression of a whole publisher or of first contacts (o3 R2 D9). Reconciliation is cheap: at 10 Envelopes/s, a 60 s inventory is 600 × 32 B = 19,200 B, or about 27.6 MB/day. That is about 1.6% of the 1.77 GB/day feed.
- **Settling check.** An omission-attack simulation (MPE-PUB-014 verification), plus a measured overhead below 2% of feed bytes.

### DEC-PUB-5 Light and mobile retrieval
- **Options.** (a) Full Shard only; mobile is not served privately in v1: g1, g2, g4, s1, s2, s3, s4, and o3 in R2. (b) A unicast push of one Shard from a filter node: g3. (c) A tag index or tag queries with decoys: o1, o4. (d) S-FMD with a floor of p ≥ 1/64: o2. (e) Bucket prefixes: o3 R1.
- **Recommended default.** (a). Any of (b) to (e) is allowed only as a labelled, opt-in reduced-privacy profile (MPE-PUB-016), following o1 R2.
- **Reason.** No selective mode yet keeps selection privacy at a demonstrated cost (s4 R2). S-FMD's rate is chosen by the sender, so o2's floor is not enforced (`2022-penumbra-fmd`, g2 R2).
- **Settling check.** MPE-PUB-052 against the mobile budget, then a measured OMR or PIR profile.

### DEC-PUB-6 Ordering presented to applications
- **Options.** (a) Arrival order with `gap`, `late` and `lost` items and no buffer: o3. (b) A bounded reorder buffer: s3. (c) A total order taken from anchors: o1 (batch order), o2 (anchor index, leaf index), and g4/o3 Lane A (chain order).
- **Recommended default.** (a). An anchored order is offered by the anchor area as an annotation, not as a delivery gate.
- **Reason.** A hidden buffer loses Events on a crash (o3 D3.3). Anchors are optional in o1 R2 and o3 R2.
- **Settling check.** A Quint model of the client delivery state machine, including Store Node fail-over (o3 D10), proving no loss and no duplicate effect under MPE-PUB-044.

## 5. Cross-area dependencies

IDs are assigned by the owning areas.

- **Format area:** a Shard field wide enough for P-PUB-1 ≤ 16, a Tag field and salt width (DEC-PUB-2), and a header expiry field. It must define the Envelope identifier as a hash of every byte (MPE-PUB-026), the sealed sequence number, the logical identifier and the schema identifier (MPE-PUB-019, -020, -049), the size classes (MPE-PUB-021), and `L_max`.
- **Admission and economics area:** one Admission Proof per Envelope, a retransmission of identical bytes needing no new proof (MPE-PUB-023), nullifier replay rules, and a stricter tier if DEC-PUB-3 changes.
- **Network area:** StrictNoSign or Anonymous GossipSub mode, a stem or flood-publish policy for Publishers' own Envelopes (g2 sets flood-publish off; the libp2p default is on, `gossipsub-v1.1.md:549`), `D_out` and scoring, and a Registry relay list that carries operator identity for MPE-PUB-014.
- **Storage area:** Store Node retention and the back-fill horizon (MPE-PUB-045), and how pruning interacts with `L_max`.
- **Anchor and Registry area:** the Registry P-PUB-1 parameter with an activation epoch (MPE-PUB-003 and -004), and an optional anchored order (DEC-PUB-6).
- **Contract consumption area:** in-circuit checks of publisher signature, destination, expiry and replay nullifier. The library's reaction call (MPE-PUB-047) feeds them.
- **Privacy area:** the leakage table rows for Shard disclosure (MPE-PUB-017) and for reactions.
- **Performance area:** the reference load and the per-Subscriber byte budget (MPE-PUB-052), and the latency target that bounds P-PUB-5 and P-PUB-7.

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Audience key | 32-byte secret (private topic) or derived value (public topic) from which the Tag key, the Shard and the seal key derive |
| Invitation | Out-of-band object carrying the network identifier, audience key, authorised publisher keys and schema identifiers |
| Recognition key | A key the client library tests Tags against. The Subscriber holds at most P-PUB-4 of them |
| Envelope identifier | Domain-separated hash of all Envelope bytes; the GossipSub message identifier |
| Logical event identifier | Sealed identifier, stable across republications of one Event |
| Cursor | Inclusive resume point defined by Envelope header fields and wall-clock time |
| Delivery item | One of `event`, `late`, `gap`, `lost`, `head`, `undecodable`, `disconnected` |
| Reconciliation | Comparing received Envelope identifiers with a second, independently operated source |
| Reduced-privacy mode | A retrieval mode that sends a selector to a serving node; only on opt-in |
| `L_max` | Maximum Envelope lifetime, defined by the format and storage areas |

## 7. Gaps

- **Completeness against an unknown publisher.** Neither sequence gaps nor reconciliation can prove that no Event was withheld from a publisher the Subscriber does not know, or from all sources at once (o3 R2 D9; s1 "mitigates omission; it does not prove completeness"). The design has no testable completeness guarantee, only the mitigations in MPE-PUB-014.
- **Timing linkage of reactions.** o3 R2 asks for reactions to be batched or jittered by default. No proposal gives a delay distribution or a measured gain against the privacy area's adversary, so no number can be written. MPE-PUB-047 covers only the "no automatic reaction" part.
- **Interest privacy for applications whose behaviour depends on recognition.** s1's game holds the application's actions fixed (g1 R2 objection). The library can control its own traffic (MPE-PUB-012) but not what the application does outside it.
- **Private mobile reception.** No proposal offers a private, affordable mobile path in v1 (DEC-PUB-5). Its cost is **unknown** until MPE-PUB-052 and an OMR or PIR benchmark exist.
- **Group ordering and fan-out.** s4's single MLS commit coordinator and s2's limit of 32 device ciphertexts belong to the session layer. s2's figure of 0.3125 logical publications/s at 10 cells/s is noted but not turned into a requirement here.
- **Skip markers.** o3's sealed `prev_skip`, which closes gaps a publisher has abandoned, has only one proponent and no format slot yet. It is deferred to the format area.
