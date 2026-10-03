# MPE-FMT: Event and envelope format

## 1. Scope of this area

This area defines the bytes of an MPE Envelope. It covers which fields a Bus Node sees and which are sealed, size classes and padding, identifiers, version and extension rules, when an expiry is valid, the Sealed Prefix that every Event carries, and how an Envelope maps onto Midnight `Misc` events for the ledger carrier and for Anchors. It does not choose the sealing or recognition construction (CRY), the Admission Proof (ECO), shard derivation and mesh settings (PUB, NET), or retention (STO). It defines the slots those areas fill. Midnight facts come from the ledger-9 / Compact 0.33 generation unless marked otherwise. Whether ledger 9 is active on any public network is **unknown** (o3-R2; o1 generation caveat).

## 2. Parameters

| ID | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-FMT-1 | Sealed Body length of size classes 0, 1, 2, 3 | 256, 1,024, 4,096, 16,384 B | 1 to 4 classes; class c body = 256 × 4^c B; largest wire length ≤ P-FMT-6 | g1 D1 class table; o3 D1 S/M/L = 1/4/16 `Misc` parts; o1-R2 adopts g1's 256 B class; DEC-FMT-1 |
| P-FMT-2 | Admission Slot width A, fixed per version | **unknown**; set by MPE-FMT-048 | 0 to 4,096 B | o2 D1 4 KiB budget; 256 B Waku RLN proof object (g3-R2, `2021-vac-waku2-rln-relay-spec` RateLimitProof); 354 B Privacy Pass token (`2024-rfc9578-privacypass-issuance` §6.3, checked in g1-R2 and o2-R2); 1,152 B (s3) |
| P-FMT-3 | Maximum Envelope lifetime | 172,800 s (48 h) | 3,600 s to 1,209,600 s | g3, s1, s3, s4; ceiling `midnight-node/res/mainnet/ledger-parameters-config.json:176`; DEC-FMT-5 |
| P-FMT-4 | Expiry clock tolerance | 60 s | 20 s to 300 s | g3 D1 (60 s); o1 D1 (5 min); lower bound is an **assumption** |
| P-FMT-5 | Offset between the Bus Node clock and the latest Midnight block timestamp at which expiry validation pauses | 120 s | 30 s to 600 s | g1 D1; range is an **assumption** |
| P-FMT-6 | GossipSub `max_transmit_size` | 65,536 B | ≥ largest wire length plus measured GossipSub framing | `rust-libp2p/protocols/gossipsub/src/protocol.rs:100` |
| P-FMT-7 | Maximum fragments per Event, where fragmentation is enabled | 16 | 2 to 16 | s1, s4 D1 |
| P-FMT-8 | Maximum `Misc` parts per ledger-carried Envelope | 16 | 1 to 64 | o3 D1 class L |
| P-FMT-9 | Version overlap window | 2 × P-FMT-3 + 30 days | ≥ 2 × P-FMT-3 | o4 D1 |
| P-FMT-10 | `Misc` name constants (ASCII, zero-padded to 32 B) | `mpe/env/v1`, `mpe/anchor/v1` | one pair per version | o1 D1; g4 D1 constant name |
| P-FMT-11 | Envelope Identifier domain string | `midnight-pe/id/v1` | one per version | g1 D1 |

**Visible Header (recommended default, DEC-FMT-2):**

| Offset | Field | Value |
|---|---|---|
| 0 | `version` u8 | 1 |
| 1 | `size_class` u8 | |
| 2 | `shard` u8 | |
| 3 | `reserved` u8 | 0 |
| 4 | `expiry` u32 | |
| 8 | Admission Slot | A bytes |
| 8 + A | Sealed Body | |

Wire length = 8 + A + P-FMT-1[class].

## 3. Requirements

**Layout and encoding**

### MPE-FMT-001 Fixed-width visible layout
The MPE client library shall encode every Envelope as fixed-width fields at fixed per-version offsets. Outside the Sealed Body there shall be no optional fields, extension fields, length prefixes, variable-length integers or self-describing encodings.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, s2, s3, s4, o1-R2, o4-R2; `2012-bitmessage-protocol-specification` (varint object header); `2020-vac-waku2-message-spec` (protobuf is not canonical, so Waku needed a separate deterministic hash)
- Rationale: each Envelope has exactly one legal byte string, so parsing is unambiguous. A new field requires a new version.
- Verify: inspection of the wire specification; test: decode and re-encode every test vector and get identical bytes.
- Status: settled

### MPE-FMT-002 Byte order
The MPE client library shall encode every multi-byte integer in the Visible Header and the Sealed Prefix in big-endian byte order.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o1, s2, g2, g4 (big-endian); g1, o2 (little-endian)
- Rationale: the order must be chosen once (g1-R2). Network byte order has more support among the proposals.
- Verify: test: `expiry` = 0x01020304 encodes as bytes 01 02 03 04 at offset 4.
- Status: open (DEC-FMT-7)

### MPE-FMT-003 Visible fields
Outside the Sealed Body, the MPE client library shall place only `version`, `size_class`, `shard`, `reserved`, `expiry` and the Admission Slot, at the offsets in the Visible Header table.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, g3, s1, s3, s4, g1-R2. Dissent: o1 and o4 (visible tag and clue); g2 (visible `msg_id`, `member_pk`, clear content topic)
- Rationale: topic, publisher, recipient, schema and sequence stay sealed. Every proposal requires this.
- Verify: inspection; test: 10^4 Prototype Envelopes each have a header of 8 + P-FMT-2 bytes and no other plaintext.
- Status: open (DEC-FMT-2)

### MPE-FMT-004 No identity-derived visible values
Outside the Sealed Body, the MPE client library shall place no value derived from a topic identifier, a recipient key or a Publisher long-term key. The `shard` field is the only exception.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1-R2 ("no public tag, clue, topic shard"); s4; o3-R2 (withdrew PRF tags). Dissent: o1, o4
- Rationale: a stable visible tag gives every relay a recipient or topic identifier (g3 D1).
- Verify: test: compare 1,000 Envelopes from one Publisher and topic with 1,000 from distinct Publishers and topics. Outside `shard` and `expiry`, the byte distributions at each offset do not differ (chi-square, p > 0.01).
- Status: open (DEC-FMT-2)

### MPE-FMT-005 Admission Slot unlinkability
The MPE client library shall place no value in the Admission Slot that is constant across one Publisher's Envelopes and differs between Publishers.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o2-R2, s1-R2, s2-R2 (objections to g2's visible `member_pk`); g2-R2 (d)
- Rationale: a persistent admission key lets any relay link all Envelopes of one membership.
- Verify: test: two memberships send 100 Envelopes each in one epoch. No Admission Slot byte range is constant within one membership and different between the two.
- Status: settled

### MPE-FMT-006 Reserved bytes
If a received Envelope has a non-zero reserved byte, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1, s2, s3, s4; `libp2p/specs/pubsub/gossipsub/gossipsub-v1.1.md:532-536` (Reject applies the P₄ penalty)
- Rationale: reserved bytes are neither an extension point nor a covert channel.
- Verify: test: set each reserved bit of a valid vector in turn; each result is Reject.
- Status: settled

### MPE-FMT-007 Exact length
If a received Envelope's length differs from 8 + P-FMT-2 + the P-FMT-1 body length of its `size_class`, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1 ("body length is implied by `size_class` and must match exactly"); s3
- Rationale: the class fixes the length, so any other length is malformed.
- Verify: test: valid vectors shortened by 1 B or lengthened by 1 B are Rejected.
- Status: settled

### MPE-FMT-008 Unknown size class
If a received Envelope's `size_class` has no entry in P-FMT-1, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1, o1, o2, o4
- Rationale: undefined classes would split the anonymity set and bypass size accounting.
- Verify: test: `size_class` values 4 to 255 are Rejected.
- Status: settled

### MPE-FMT-009 Structural checks first
The Bus Node shall complete the version, reserved-byte, size-class, length and expiry checks on an Envelope before it runs any cryptographic verification on it.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 (order of admission checks); s2 ("reject unknown versions and suites before cryptographic work"); s3 (reject oversized proofs before allocating)
- Rationale: a malformed Envelope should cost a relay a few comparisons, not a proof verification.
- Verify: test: send 10^4 malformed Envelopes with well-formed Admission Slots; the verification counter stays at 0.
- Status: settled

### MPE-FMT-010 Transmit size bound
The Bus Node shall set GossipSub `max_transmit_size` to P-FMT-6 bytes.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g2 (refuses 1 MiB mesh messages); `rust-libp2p/protocols/gossipsub/src/protocol.rs:100` (default 65,536)
- Rationale: the codec drops oversized frames before validation. Class 3 plus an Admission Slot of a few KiB fits under the default.
- Verify: test: a frame of P-FMT-6 + 1 bytes never reaches the validator.
- Status: settled

### MPE-FMT-011 Body-blind validation
The Bus Node shall compute every validation outcome without decrypting or parsing the Sealed Body.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s1 ("relay validation never depends on the application schema"); g1, g2, g3
- Rationale: relays hold no keys. Validation that depended on the schema would leak information or break when new schemas appear.
- Verify: inspection: the validator links no AEAD or schema decoder. Test: Envelopes with random Sealed Bodies and valid admission get the same outcome as real ones.
- Status: settled

### MPE-FMT-012 GossipSub carriage
The Bus Node shall publish each Envelope as the whole GossipSub `data` field, with the `from`, `seqno`, `signature` and `key` fields absent.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 (message signing off), g2 (StrictNoSign); `libp2p/specs/pubsub/README.md:272-284`; `rust-libp2p/protocols/gossipsub/src/config.rs:46-48` (`ValidationMode::Anonymous`)
- Rationale: GossipSub author fields would attach a peer identity to every Envelope.
- Verify: test: captured RPC frames lack all four fields, and peers in Anonymous mode accept them.
- Status: settled

**Size classes and padding**

### MPE-FMT-013 Sealed Body length
The MPE client library shall produce a Sealed Body whose length equals the P-FMT-1 entry for the Envelope's `size_class`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, o1, o2, o4, g3, s2 (size classes); s1, s3, s4 (single cell)
- Rationale: fixed lengths hide the payload length within a class.
- Verify: test: every Prototype Envelope has a body length listed in P-FMT-1 that matches its class byte.
- Status: open (DEC-FMT-1)

### MPE-FMT-014 Smallest fitting class
When publishing an Event, the MPE client library shall select the smallest size class whose payload capacity holds the payload, unless the application names a larger class.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1; g1, g3 ("padding is the volume control"), o3
- Rationale: full-feed subscribers pay for every padded byte (o3-R2, g3-R2).
- Verify: test: payloads exactly at each class capacity, and 1 B over it, land in the expected classes.
- Status: settled

### MPE-FMT-015 Oversize payload
If an Event payload exceeds the payload capacity of the largest size class, then the MPE client library shall return a payload-too-large error and publish no Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g4 ("a longer message is an application problem"); g3; s2
- Rationale: silently truncating or splitting the payload would break consumers.
- Verify: test: a payload of capacity + 1 B returns the error, and no Envelope reaches the mesh.
- Status: settled

### MPE-FMT-016 Sealed padding
The MPE client library shall place all padding inside the authenticated encryption, so that Events of different payload lengths in one size class produce Envelopes of equal length.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, o1, o3, s3 (authenticated padding)
- Rationale: visible padding would reveal the payload length.
- Verify: test: in each class, a 1 B payload and a full-capacity payload give equal wire lengths.
- Status: settled

### MPE-FMT-017 Padding check
If the padding of an opened Event contains a non-zero byte, then the MPE client library shall discard the Event as malformed.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1 ("a non-zero pad byte is invalid"); g4 ("non-zero padding is a reject")
- Rationale: allowing exactly one plaintext per Event removes a way to alter Events without detection.
- Verify: test: a vector re-sealed with one pad byte set to 0x01 is discarded and counted.
- Status: settled

**Identifiers**

### MPE-FMT-018 Envelope Identifier
The MPE client library shall compute the Envelope Identifier as SHA-256 over P-FMT-11, the Network Identifier, Visible Header bytes 0 to 7 and the Sealed Body. The Admission Slot is excluded.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s1, s3, s4, o2-R2 (identifier independent of the proof). Dissent: g1, o4, o1 (hash all bytes). L9 `base-crypto/src/hash.rs:29,93` (SHA-256, 32 B; line numbers per g1-R2)
- Rationale: admitting the same Envelope more than once must not defeat deduplication (s3).
- Verify: test vectors; test: one body under two different Admission Slots yields one identifier.
- Status: open (DEC-FMT-3)

### MPE-FMT-019 GossipSub message id
The Bus Node shall use the Envelope Identifier, recomputed from the received bytes, as the GossipSub message id.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 ("not transmitted ... the GossipSub message id and the dedup key"); dissent: g2 transmits `msg_id`; `rust-libp2p/protocols/gossipsub/src/config.rs:842`; `libp2p/specs/pubsub/README.md:282-284`
- Rationale: a transmitted identifier is one more field that must be checked and could be forged.
- Verify: test: on every node, IHAVE ids equal the locally recomputed identifiers.
- Status: settled

### MPE-FMT-020 Acyclic construction
The MPE client library shall build an Envelope in this order: Sealed Body, then Envelope Identifier, then Admission Slot. No step takes input from a later step.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s1-R2 and s4-R2, which found circular dependencies in g1's AEAD / `relay_sig` and in o1's identifier / RLN signal
- Rationale: a circular definition has no way to generate an Envelope.
- Verify: inspection; test vectors rebuild each stage from earlier stages only.
- Status: settled

### MPE-FMT-021 Network binding
If a received Envelope was admitted under a different Network Identifier, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; s1 (network identifier), s3 (genesis hash), s4
- Rationale: binding the network into the identifier stops replay across networks without adding a transmitted field.
- Verify: test: an Envelope valid on a test network is Rejected by a Bus Node configured with a different genesis hash.
- Status: settled

### MPE-FMT-022 Logical Event Identifier
The MPE client library shall seal a random 16-byte Logical Event Identifier that is the same in every retransmission and every carrier of one Event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s2, s3, s4; g4 (`msg_id`, 16 B random); o3 (portable `eid` across lanes)
- Rationale: the Envelope Identifier changes on re-admission and between carriers. Deduplication across lanes needs a sealed value that stays constant.
- Verify: test: one Event sent on the overlay and on the mock ledger carrier opens with equal Logical Event Identifiers.
- Status: settled

**Versioning and extension**

### MPE-FMT-023 Version bound to topic
If a received Envelope's `version` differs from the version assigned to the GossipSub topic it arrived on, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1 (a new layout gets a new protocol id and mesh), o1-R2; s2, s3, g3, o2 (reject or drop unknown versions). Dissent: g2 (Ignore), o1 R1 (relay unknown versions)
- Rationale: a v1 mesh never legitimately carries v2 bytes. Returning Ignore would let a neighbour spam without penalty.
- Verify: test: `version` = 2 on a v1 topic is Rejected and lowers the sender's P₄ score.
- Status: open (DEC-FMT-4)

### MPE-FMT-024 Version overlap
Where two Envelope versions are active, the Bus Node shall relay the topics of both versions for at least P-FMT-9 after the newer version activates.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D1; o4 (accept N and N−1 for 2 × `T_max` + 30 days); g1 (run both protocols during a window declared by the contract)
- Rationale: Envelopes published just before an upgrade stay deliverable until they expire.
- Verify: simulation: upgrade half the nodes; no unexpired old-version Envelopes are lost during the window.
- Status: open (DEC-FMT-4)

### MPE-FMT-025 Unsupported sealed format
If an opened Sealed Prefix has an unknown `pt_version` or `kind`, then the MPE client library shall return a typed unsupported-format error to the application.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; o3 ("reject unknown `v` values explicitly and never guess"); s2; `design/evidence/bitmessage-guide.md:24-33` (separate version namespaces)
- Rationale: guessing a format turns a version mismatch into silent corruption.
- Verify: test: vectors with `pt_version` = 2 or with an undefined `kind` return the typed error.
- Status: settled

### MPE-FMT-026 Unknown schema
When the MPE client library opens an Event whose schema identifier has no registered decoder, the MPE client library shall deliver the Event to the application marked as undecodable.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1; o3 ("delivered as `undecodable`, never dropped"); o2 ("an unknown schema is delivered opaque")
- Rationale: dropping the Event would hide gaps from loss detection based on sequence numbers (PUB).
- Verify: test: an Event with an unregistered schema arrives flagged as undecodable, with its raw payload.
- Status: settled

### MPE-FMT-027 Static decoder dispatch
The MPE client library shall select a payload decoder only from a table that is keyed by schema identifier and fixed when the application registers.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o4 (no dynamic type dispatch); `design/evidence/bitmessage-guide.md:352-358` (CVE-2018-1000070, an `eval()` on message data)
- Rationale: decrypted bytes from an attacker must never choose which code runs.
- Verify: inspection: no eval, reflection or dynamic loading keyed by payload bytes; fuzz test of the decoder path.
- Status: settled

**Expiry**

### MPE-FMT-028 Expiry field
The MPE client library shall set `expiry` to an unsigned 32-bit Unix time in seconds, no later than its own clock plus P-FMT-3.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, g3, o4 (Unix seconds). Dissent on encoding: o1 (minute index), o2 (`ttl_class`), s4 (hourly bucket)
- Rationale: an absolute expiry lets any node check validity without keeping Publisher state.
- Verify: test: at creation, Prototype Envelopes satisfy `now < expiry ≤ now + P-FMT-3`.
- Status: open (DEC-FMT-5)

### MPE-FMT-029 Expiry too far ahead
If a received Envelope's `expiry` exceeds the Bus Node's clock plus P-FMT-3 plus P-FMT-4, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1; g3; o1; s2 ("relays refuse expiry extensions")
- Rationale: a lifetime longer than allowed takes storage that the admission did not pay for.
- Verify: test: `expiry` = now + P-FMT-3 + P-FMT-4 + 1 s is Rejected; one second less is not.
- Status: settled

### MPE-FMT-030 Expired on arrival
If a received Envelope's `expiry` is earlier than the Bus Node's clock minus P-FMT-4, then the Bus Node shall return Ignore.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; g1 ("merely expired on arrival is Ignore: not forwarded, not punished"); `gossipsub-v1.1.md:532-536`
- Rationale: late delivery is a network condition, not misbehaviour.
- Verify: test: an expired Envelope is not forwarded, and the sender's P₄ counter does not change.
- Status: settled

### MPE-FMT-031 Unsafe clock
While the Bus Node's clock differs by more than P-FMT-5 from the timestamp of the latest Midnight block it holds, the Bus Node shall return Ignore for every Envelope.
- Pattern: state
- Scope: POC
- Priority: SHOULD
- Source: D1; g1 ("the relay stops validating rather than punishing peers")
- Rationale: a node with a skewed clock would otherwise penalise honest peers. NET must raise an alarm in this state.
- Verify: test: shift the mock Ledger Adapter timestamp by P-FMT-5 + 1 s; every outcome is Ignore and no P₄ penalties are applied.
- Status: settled

### MPE-FMT-032 No forwarding after expiry
When an Envelope's `expiry` passes, the Bus Node shall stop sending that Envelope to peers, including in IWANT responses.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1; g1 (seen-set kept until expiry); s2 ("relays ... prune expired bodies")
- Rationale: expiry bounds relay work. Retention by Store Nodes belongs to STO.
- Verify: test: an IWANT for an expired identifier returns nothing.
- Status: settled

### MPE-FMT-033 Lifetime ceiling
The Registry shall reject any P-FMT-3 parameter value above 1,209,600 s.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D1; o1, o2, o4; `midnight-node/res/mainnet/ledger-parameters-config.json:176` (`global_ttl`)
- Rationale: this keeps replay and anchor windows aligned with Midnight's intent validity window. `global_ttl` is not event retention (g2-R2, g4-R2).
- Verify: test on the Registry model: a parameter change to 1,209,601 s fails.
- Status: settled

**Sealed content**

### MPE-FMT-034 Sealed Prefix
The MPE client library shall begin every Sealed Body plaintext with the Sealed Prefix fields `pt_version`, `kind`, `flags`, `payload_len`, `schema_version`, `seq`, Logical Event Identifier and schema identifier.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 (plaintext prefix), o1 (inner frame), o3 (sealed CBOR fields), s2, s3, g3
- Rationale: every consumer needs ordering, deduplication and schema routing without trusting relays.
- Verify: inspection; test vectors decode every field.
- Status: open (DEC-FMT-7)

### MPE-FMT-035 Sealed control packets
The MPE client library shall carry every session or group control packet, including any MLS framing, entirely inside a Sealed Body.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D1; s1, s2, s3, s4; `2023-barnes-rfc9420` §6.3 (`PrivateMessage` exposes `group_id` and `epoch`; checked in g1-R2, o1-R2, g2-R2)
- Rationale: unwrapped MLS would show a group label to every relay.
- Verify: inspection; test: no MLS header byte appears outside the Sealed Body.
- Status: settled

### MPE-FMT-036 No receipt kind
The MPE client library shall define no Envelope `kind` whose purpose is to acknowledge receipt to a Publisher.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, g4, o3; `2012-warren-bitmessage-whitepaper` §7 (acknowledgements let an eavesdropper locate the receiver, per g4). Dissent: o2 (`bus/ack` schema), s3 (acknowledgement payloads)
- Rationale: transport receipts help locate the receiver. Applications can still send ordinary Events.
- Verify: inspection of the `kind` table.
- Status: open (DEC-FMT-6)

### MPE-FMT-037 Carrier-independent body
The MPE client library shall open a Sealed Body using only its bytes, the `version`, the `size_class` and the recipient's key material.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o2 (the same sealed body is published with `emit(Misc)`); o3 (the same envelope on both lanes)
- Rationale: the ledger carrier has no Visible Header, so the cryptographic inputs for each Envelope must sit inside the body.
- Verify: test: a body taken from the mock ledger carrier opens exactly as its overlay copy does.
- Status: open (DEC-FMT-8)

### MPE-FMT-038 Explicit external fetch
The MPE client library shall not retrieve an object referenced inside an Event unless the application calls an explicit fetch operation.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s3 ("never ... automatically fetch attachments"); s2; s4 (fetch leakage must be declared)
- Rationale: a fetch reveals the subscriber's interest to whoever serves the object.
- Verify: test: receiving an Event that contains a reference produces no outbound request.
- Status: settled

### MPE-FMT-039 Optional fragmentation
Where sealed fragmentation is enabled, the MPE client library shall deliver a fragmented Event only after all of its fragments (at most P-FMT-7) have been opened.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D1; s1, s4 (at most 16 fragments; incomplete events never execute). Dissent: g1, s2, g4 (no fragmentation)
- Rationale: delivering part of a control message would corrupt session state.
- Verify: test: drop one of 16 fragments; nothing is delivered, and the partial set expires.
- Status: open (DEC-FMT-6)

**Ledger carrier and Anchors**

### MPE-FMT-040 Constant `Misc` name
The MPE client library shall set the `Misc` `name` of every part of a ledger-carried Envelope to the P-FMT-10 envelope name for its version.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g4 (constant name); o1 ("the topic must never go in `name`", `midnight-indexer/indexer-api/graphql/schema-v4.graphql:1125-1165`); o3-R2 (withdrew the tag in `name`). Dissent: o2 (`H(shard‖epoch)`)
- Rationale: the indexer exposes `name` in the clear.
- Verify: test: all parts from two different topics carry byte-identical `name` fields.
- Status: open (DEC-FMT-8)

### MPE-FMT-041 Part split
The MPE client library shall carry a class-c Sealed Body on the ledger as 4^c `Misc` events whose 256-byte payloads, concatenated in emission order, equal that body.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o3 (1/4/16 parts), o1 (MIP-0019 multipart); `minokawa-compact/compiler/midnight-events.ss:71-74`; `midnight-improvement-proposals/mips/mip-0019-multipart-event.md:64-66`
- Rationale: every P-FMT-1 body length is an exact multiple of the 256-byte `Misc` payload.
- Verify: test vectors for classes 0 to 2 against the mock Ledger Adapter.
- Status: open (DEC-FMT-1)

### MPE-FMT-042 One phase
The MPE client library shall emit all parts of one ledger-carried Envelope within one intent, in the guaranteed phase.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D1; o1, o3; `mip-0019-multipart-event.md:70-76`
- Rationale: parts split across phases can end up only partly applied.
- Verify: inspection of the built transactions; ledger-9 devnet test with a failing fallible segment.
- Status: settled

### MPE-FMT-043 One `Misc` per emit
The MPE client library shall emit each ledger part as exactly one 288-byte `Misc` event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o1, o3, g4; L9 `onchain-vm/src/vm.rs:41-43` (`MAX_LOG_EMITTED` = 1 KiB, silent drop; `notes/midnight-network-stack.md` §3.2). g1-R2 and g3-R2 confirmed it on the tag; o3-R2 could not confirm it at the pinned revision `54a4e013`.
- Rationale: Compact accepts logs of up to 512 KiB, but ledger 9 silently drops events over 1 KiB.
- Verify: inspection of the contract; test: every emitted log item is 288 bytes.
- Status: settled

### MPE-FMT-044 Ledger part limit
If an application asks for ledger carriage of an Envelope that needs more than P-FMT-8 parts, then the MPE client library shall return an error without building a transaction.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; o3 (largest on-chain class is 16 parts); g4 (ledger cost)
- Rationale: a class-3 Envelope on the ledger costs 64 parts per Event.
- Verify: test: a request for ledger carriage of a class-3 Envelope returns the error and submits nothing.
- Status: settled

### MPE-FMT-045 Ledger reassembly
When reading ledger-carried Envelopes, the MPE client library shall concatenate, in ledger emission order, the payloads of parts named P-FMT-10 that come from one transaction and one physical intent.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1; o3 (the SDK implements the reader rule itself); `mip-0019-multipart-event.md:64-66` (MIP-0019 status is Proposed, `:6`)
- Rationale: the library cannot wait for MIP-0019 to be activated.
- Verify: test: interleaved parts from two intents in one block reassemble into two bodies.
- Status: settled

### MPE-FMT-046 Malformed ledger group
If a reassembled ledger group has a part count that is not 4^c for a defined class c, then the MPE client library shall discard the group as malformed.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; inference from MPE-FMT-041; MIP-0019 has no part-count field (`mip-0019-multipart-event.md:33`)
- Rationale: MIP-0019 groups every event with the same name in an intent, so a wrong count is the only sign of a bad package.
- Verify: test: groups of 2, 3 and 5 parts are discarded and counted.
- Status: settled

### MPE-FMT-047 Anchor event
The Registry shall emit each Anchor as one `Misc` event with the P-FMT-10 anchor name and a payload of at most 256 bytes.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D1; o1 (`"mpe/anchor/v1"`), o4 (`Misc{"MPE/anchor/v1", window_id‖shard_bitmap‖root‖count‖relay_id}`); g2 ("an anchor is a hash, a shard id and a short commitment")
- Rationale: Anchors are read off-chain through `contractEvents`. NET defines the payload fields.
- Verify: ledger-9 devnet test: each anchor transaction produces exactly one `Misc` with that name.
- Status: settled

**Measurement and test vectors**

### MPE-FMT-048 Admission Slot measurement
The Prototype shall measure the serialised length of the chosen Admission Proof and record it as P-FMT-2 before any P-FMT-1 value is frozen.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; o1-R2, o2-R2, g3-R2, s2-R2 ("until P is measured, no class table is final")
- Rationale: the admission field sets the minimum Envelope size, and its length is **unknown**.
- Verify: demonstration: a benchmark report giving the measured length and the proof system used.
- Status: open (DEC-FMT-1)

### MPE-FMT-049 Test vectors
The Prototype shall publish byte-exact test vectors for each size class, the Sealed Prefix, the Envelope Identifier, the binding between Admission Slot and identifier, and the ledger part split.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s4-R2 ("exact construction ... and test vectors must precede adoption"); s2 D10; g4 D10 (Phase 0 vectors)
- Rationale: a second implementation must be able to reproduce every byte.
- Verify: test: an independent decoder reproduces every vector.
- Status: settled

## 4. Decisions

### DEC-FMT-1 Size-class table
- Options:
  - (a) A single 4,096 B cell: s1, s3, g2-R2, g3-R2. g3-R2 voted for the cell with the 1,152 B admission area, which that review labels s4.
  - (b) A single 2,048 B record: s4.
  - (c) Cells of 1,024 or 4,096 B: s2.
  - (d) Bodies of 256 B, 1 KiB, 4 KiB and 16 KiB: g1, o1-R2, o4-R2.
  - (e) Bodies of 1, 4, 16 and 64 KiB: o1 R1, o2 R1.
  - (f) Bodies of 512 B, 2 KiB, 8 KiB and 32 KiB: o4 R1.
  - (g) Wire sizes of 1, 4 and 32 KiB: g3 R1, o2-R2.
  - (h) 4 and 64 KiB, plus a 256 KiB class that is only announced: g2 R1.
  - (i) One 288 B `Misc`: g4, o3-R2.
- Recommended default: (d).
- Reason:
  - The class bodies equal 1, 4, 16 and 64 `Misc` parts, so one table serves both carriers (o3's S/M/L).
  - The 256 B class keeps full-feed cost low, and that cost is the binding one for consumers (o3-R2, g3-R2).
  - The largest class plus an Admission Slot of several KiB fits under rust-libp2p's 65,536 B default.
  - Four classes is o1's limit for splitting the anonymity set.
  - Single-cell designs give one uniform set, but they charge every short notification 2 to 4 KiB.
- Settling check: MPE-FMT-048; a simulation of the anonymity set per class at PRF's load; payload-size histograms from pilot applications. If A exceeds 1 KiB, class 0 is mostly admission overhead, and (a) or (b) should go back to a vote.

### DEC-FMT-2 Visible header contents
- Options:
  - (a) Version, class, shard, expiry and admission only: g1, g3, s1, s3, s4, g1-R2.
  - (b) Also a recognition tag and an FMD clue: o1, o4 (tag), o2 (clue).
  - (c) Also `msg_id`, a persistent `member_pk`, and clear content topics on open shards: g2.
  - (d) Also visible flags (anchor-requested, intro-inbox): o4.
- Recommended default: (a). If CRY adopts recognition material, it goes inside the Sealed Body as pseudorandom bytes.
- Reason: o3-R2 withdrew PRF tags, and g1-R2 rejects tags and clues on the relay path. s1-R2 notes that Beck's paper supports the 68 B clue construction, but not the claim that random filler is indistinguishable from real clues. Visible flags would split traffic into visible kinds.
- Settling check: CRY's recognition decision; PRV's leakage table. Shard derivation stays with PUB and NET (g1-R2 objects to a shard derived from the topic).

### DEC-FMT-3 Identifier scope
- Options:
  - (a) Hash every stored byte, admission included: g1, o4, o1 R1.
  - (b) Hash everything except the admission proof or signature: s1, s3, s4, o2-R2.
  - (c) A transmitted `msg_id` that relays check: g2.
- Recommended default: (b), computed by each node and never transmitted.
- Reason: an Envelope admitted again through another issuer still deduplicates, and the order body → identifier → admission has no cycles (s1-R2, s4-R2). g1 objects that two byte strings then share one identifier. The cost is at most one wasted admission, because both copies are valid and a Bus Node forwards the first one it sees.
- Settling check: a Prototype test admitting one body twice, which must give one delivery; ECO confirms the nullifier rule is unaffected.

### DEC-FMT-4 Version handling
- Options:
  - (a) Bind the version to the protocol id or topic, and treat unknown versions as invalid: g1, o1-R2. Rejecting before any cryptographic work: s2, s3, g3, o2.
  - (b) Return Ignore for unknown versions: g2.
  - (c) Relay unknown versions and let endpoints drop them: o1 R1.
  - (d) Accept versions N and N−1 in one mesh for 2 × `T_max` + 30 days: o4.
- Recommended default: (a) with Reject, plus (d)'s overlap window, implemented by running both versions' topics.
- Reason: Ignore would let a neighbour send junk without penalty. Relaying unknown versions repeats Bitmessage's relaying of unknown object types, which g1 rejects.
- Settling check: the upgrade simulation in MPE-FMT-024, with no loss.

### DEC-FMT-5 Lifetime and expiry encoding
- Options for lifetime:
  - 300 to 3,600 s depending on class: g1.
  - 24 h, or 7 d for class L: g2.
  - 48 h: g3, s1, s3, s4.
  - 7 d after the end of the admission hour: s2.
  - A `ttl_class` of 1 h, 24 h or 7 d: o2.
  - 7 d default, 14 d maximum: o1.
  - 24 h default, 7 d governance maximum, 14 d hard ceiling: o4.
  - No expiry field, 14-day indexer retention: g4.
- Options for encoding: Unix seconds (g1, g3, o4); minute index (o1); hourly bucket (s4).
- Recommended default: a 48 h maximum, `expiry` in Unix seconds, and a 14-day hard ceiling.
- Reason: four proposals converge on 48 h. It covers a wallet that is offline overnight, which was o4-R2's objection to g1's 1 h.
- Settling check: STO's storage arithmetic at 48 h; CON's requirement for the offline window.

### DEC-FMT-6 Payload kinds and large payloads
- Options:
  - Fragmentation: none (g1, s2, g4) or up to 16 sealed fragments (s1, s4).
  - Large objects as blobs referenced from the Event: g2, g3, o3.
  - Acknowledgements: no transport acks (g1, g4, o3), or ack schemas or payloads (o2, s3).
- Recommended default:
  - No fragmentation in the POC; fragmentation as an optional PROD feature for control packets.
  - Referenced objects are fetched only on an explicit call.
  - No receipt `kind`.
- Settling check: CRY's measured sizes for control packets (s1-R2: "control messages exceeding practical bounds").

### DEC-FMT-7 Encoding details
- Options:
  - Byte order: big-endian (o1, s2, g2, g4) or little-endian (g1, o2).
  - Sealed metadata: fixed binary (g1, g4), canonical CBOR (o1, o3, s1) or length-prefixed binary (o4).
  - Schema id: 32 B hash (o1, o2, o4), 8 B plus a u16 version (o3), 4 B (s2) or u16 (g2, g3).
  - `seq`: u32 (g1, g4, o3) or u64 (o1, g3, s2).
- Recommended default: big-endian, with a fixed binary Sealed Prefix of 40 B. The application payload encoding is defined by its schema; the library default is canonical CBOR.

| Field | Width | Notes |
|---|---|---|
| `pt_version` | u8 | |
| `kind` | u8 | 1 = application Event, 2 = control |
| `flags` | u16 | bit 0: a publisher authentication block is present; CRY fixes its width |
| `payload_len` | u16 | |
| `schema_version` | u16 | |
| `seq` | u64 | |
| Logical Event Identifier | 16 B | |
| schema id | 8 B | |

- Reason (**inference**, assuming 60 B of body overhead for an X25519 key, a 12 B nonce and a 16 B tag): this prefix leaves 156 B of unsigned payload in the 256 B class. g1's 136 B prefix would leave 60 B.
- Settling check: CRY's overhead figures; the afternoon usability test (o3 D10).

### DEC-FMT-8 Ledger carrier
- Options:
  - `name`: a constant (g4, o1, o3-R2), the recognition tag (o3 R1) or `H(shard‖epoch)` (o2).
  - Parts: a single part only (g4) or MIP-0019 multipart (o1, o3).
- Recommended default: a constant name, multipart up to 16 parts, and the Sealed Body carried unchanged (MPE-FMT-037).
- Reason: a name that varies with shard or epoch adds public structure. Using one body on both carriers allows deduplication across lanes through the Logical Event Identifier.
- Settling check: cost per part on a ledger-9 devnet; o3's comparison of indexer `id` values between instances (PUB/CON).

## 5. Cross-area dependencies

- **CRY:** the sealing construction; nonce and ephemeral-key placement inside the body; associated data; the width of the authentication block; recognition material; key commitment for trial decryption (`2021-len-partitioningoracle`).
- **ECO:** what the Admission Slot holds and its width (P-FMT-2); how admission binds to the Envelope Identifier; nullifier rules.
- **NET:** topic naming per version and shard; `message_id_fn`; Anonymous validation mode; P₄ weights; the duplicate cache; the Anchor payload layout; alarms on Ledger Adapter timestamps (MPE-FMT-031).
- **PUB:** shard derivation and shard count; `seq` semantics; deduplication on the Logical Event Identifier; ordering; back-fill frames.
- **CON:** typed errors; delivery of undecodable Events; the schema registration API; a portable ledger cursor.
- **STO:** retention relative to `expiry`; what Store Nodes do after expiry.
- **PRV:** leakage-table entries for `size_class`, `shard`, `expiry` and the permanence of ledger-carried data.
- **SEC:** fuzzing of the validator and decoders; metrics for malformed input.
- **PRF:** bandwidth per class; full-feed cost for consumers.
- **VER:** gates on MPE-FMT-048 and MPE-FMT-049.
- **OPS:** Registry parameter changes for P-FMT-3; version activation windows.

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Visible Header | The Envelope bytes outside the Sealed Body: `version`, `size_class`, `shard`, `reserved`, `expiry` and the Admission Slot |
| Admission Slot | Fixed-width region of the Visible Header that holds the Admission Proof |
| Sealed Body | Fixed-length ciphertext of one size class; opaque to Bus Nodes |
| Sealed Prefix | Fixed fields at the start of the Sealed Body plaintext |
| Size Class | One of the Sealed Body lengths in P-FMT-1 |
| Envelope Identifier | Domain-separated SHA-256 of an Envelope, excluding the Admission Slot; used as the GossipSub message id |
| Logical Event Identifier | Random 16-byte sealed identifier shared by every copy of one Event |
| Network Identifier | The Midnight genesis block hash, bound into the Envelope Identifier |
| Ledger Carrier | Carrying a Sealed Body as `Misc` events on Midnight |
| Part | The 256-byte payload of one `Misc` event in the Ledger Carrier |

## 7. Gaps

- **Expiry is not deletion.** Ledger-carried bodies stay public for as long as any archive keeps the blocks. This is o4-R2's inference from archive nodes running `--pruning archive` and from the indexer re-executing blocks. It is a disclosure for PRV, not a testable property of the format.
- **Payload capacity per class** cannot be stated until CRY fixes the body overhead and the width of the authentication block.
- **`MAX_LOG_EMITTED` at the pinned VM revision `54a4e013`** has not been verified (o3-R2). MPE-FMT-043 holds either way.
- **Ledger-9 activation** is **unknown**. MPE-FMT-042 and MPE-FMT-047 cannot be verified on a public network until it ships.
- **The anonymity cost of four classes versus one cell** has not been measured. DEC-FMT-1 names the simulation that would measure it.
