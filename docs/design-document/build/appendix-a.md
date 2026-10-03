# Appendix A. Requirements in EARS form {#appendix-a}

This appendix lists every requirement of Midnight Express, written in EARS syntax (Easy Approach to Requirements Syntax). Each entry gives the requirement identifier, a short title, the sentence, its scope (POC for the prototype, PROD for production), its priority, whether the decision behind it is settled or open, and how it is verified; some entries add a note. Entries marked *same obligation* restate a requirement listed elsewhere; they point to the entry that owns it. The prefix MPE marks requirement identifiers and the MPE Envelope. Terms follow the Glossary in A.0.

## A.0 Glossary {#a0-glossary}

The table defines the terms that the requirements use and states how each relates to the usage of the Midnight Foundation's proposals. The terms "event" and "private event" keep the Foundation's meaning.

| Term | Meaning | Relation to the Foundation's usage |
|---|---|---|
| event | A contract event: a typed record that a Compact circuit emits with `emit` during transaction execution, recorded in the transaction and served by the Indexer. | The Foundation's term (MIP-0002, CoIP-0003), used with that meaning only. |
| private event | A contract event some of whose fields are encrypted for chosen recipients and bound to the transaction by a commitment that the proof checks. | The Foundation's term, planned for Phase 2 of MPS-0005 and defined by Midnight. Midnight Express can carry private events but does not define or replace them. |
| Message | The application message that a Publisher seals into an MPE Envelope and delivers through Midnight Express. | Not a contract event. A Message is authenticated by its Publisher's signature and committed by an Anchor, not by contract execution. |
| Confidential Message | A Message for which content confidentiality, sealed labels, conditional interest privacy and no silent change hold, as defined in Chapter 4. | No Foundation counterpart. It complements on-chain private events. |
| carried event | A Message whose payload is the unchanged bytes of a contract event, public or private, with the hash of the recording transaction and the event's position in it. | The event keeps the authority and the binding of its transaction. Carriage adds early, private delivery and is confirmed against the chain. |
| MPE Envelope | The fixed-size sealed wire object that carries one Message: an 8-byte visible header, the Admission Slot and the Sealed Body. | Distinct from the ledger's `VersionedLogItem`, which the Foundation's documents call a versioned envelope and which this document never calls an envelope. |
| Shard | One GossipSub topic partition of the overlay. | No Foundation counterpart. In MPS-0005 "topic" means an event filter value, so this document uses "topic" only as "GossipSub topic". |
| stream | A sealed application channel between Publishers and their audience, named only inside the Sealed Body. | Unrelated to the `@topic` annotation that MPS-0005 plans for private events. |
| Recognition Tag | A salted 16-byte keyed value in each MPE Envelope that lets a Subscriber recognise its Messages locally. | Serves the purpose of MPS-0005 topic-based filtering by other means: it is fresh per MPE Envelope, unlinkable, and evaluated only by the Subscriber. Unrelated to domain-separation tags and to the event tag of `Misc`. |
| Bus Node | A sidecar process, beside and not inside the Midnight node, that joins the GossipSub overlay and relays MPE Envelopes. | Not a Midnight node: in the Foundation's documents "node" means `midnight-node`. |
| Store Node | A Bus Node that also retains MPE Envelopes for back-fill. | Stores no chain history, unlike the archival and pruned nodes of the Foundation's documents. |
| Publisher | A client that seals and submits Messages. | On the ledger lane, also a publisher in the sense of MIP-0019. |
| Subscriber | A client that receives a Shard and recognises its own Messages. | On the ledger lane, it acts as a MIP-0019 reader. |
| Consumer | An agent, contract, wallet or application that acts on a Message. | Narrower than the Foundation's consumer of events, which includes indexers and explorers. A contract consumes a Message only through a later transaction. |
| Admission Proof | The proof in the Admission Slot that authorises one publication and enforces a rate limit. | Not a transaction proof; "proof" alone in the Foundation's documents means the zero-knowledge proof of a transaction. |
| Bus Registry | The Compact contract that holds memberships, parameters, the relay list and Anchors. | Distinct from the domain-separation, name-service, token and proof-server registries of the Foundation's documents. |
| Anchor | A Bus Registry state record holding the root over the MPE Envelope Identifiers of one 60-second window. A `Misc` copy is emitted as a notification. | No Foundation counterpart. Verification uses the state record, because events are not consensus state. |
| Ledger Adapter | The client or Bus Node interface that reads Midnight state and submits transactions. | Not the node-internal ledger bridge of MPS-0007. |
| Indexer | A service that reads chain data and serves it to wallets and DApps. | The Foundation's definition (MPS-0028), used unchanged. |
| Bus Operator | A party that runs a Bus Node, Store Node, bootstrapper, gateway or anchorer. | Narrower than the Foundation's operators of nodes, stake pools and proof servers. An Indexer operator is not a Bus Operator. |
| ledger lane | The explicitly selected ledger-only path that carries an MPE Envelope's Sealed Body as 1, 4 or 16 `Misc` parts. | Uses the multipart transport of MIP-0019. Unrelated to the fallible phase of a transaction. |
| admission window | The 60-second period over which admission quotas are counted. | Unrelated to Midnight consensus and staking epochs. |
| admission nullifier | The value an Admission Proof reveals when it spends one publication allowance. | Unrelated to Zswap and other ledger nullifiers. |
| consumption nullifier | The value a contract records when it acts on a Message, so that it acts at most once. | Unrelated to Zswap and other ledger nullifiers. |
| Stage 0 to Stage 4 | The rollout stages of Midnight Express: models, simulation and the Prototype; permissioned pilot; permissioned production; open admission; handover. | Distinct from the Phase 1 and Phase 2 of MPS-0005, which denote public and private contract events. |
| bond | An optional balance held by the Bus Registry contract against misbehaviour. | Unrelated to NIGHT staking, which locks nothing and carries no consensus weight. |
| `gossip`, `final` | Delivery labels: `gossip` for a delivered Message not yet confirmed by the chain, `final` for a Message covered by a Bus Registry Anchor in a finalized block or verified on the ledger lane. | `final` builds on the Foundation's finalization, usually about 3 blocks (about 18 s) after inclusion. |

## A.1 Parameters {#a1-parameters}

Requirements refer to tunable parameters by identifier (`P-AREA-n`). The first table gives the values chosen for the prototype and for production. The second table lists the remaining parameters with the default each requirement area assumes.

| Parameter | Prototype value | Production value |
|---|---|---|
| Size-class Sealed Body lengths (P-FMT-1) | 256, 1,024, 4,096, 16,384 B (classes 0-3) | Same table if the measured Admission Slot A is at most 1,024 B; if A exceeds 1,024 B, classes 1-3 only (1,024, 4,096, 16,384 B) |
| Admission Slot width A (P-FMT-2) | 512 B: admission window 8 B, membership root 32 B, admission nullifier 32 B, share y 32 B, proof 256 B (360 B), then zero fill | Measured length of the selected proof fields rounded up to a multiple of 64 B, at most 4,096 B (P-ECO-11), fixed per version |
| Visible Header and wire length | 8 B fixed fields + 512 B Admission Slot = 520 B; wire 776, 1,544, 4,616, 16,904 B | 8 B + A; wire = 8 + A + class body |
| Payload capacity per class (default cryptographic profile) | 86, 854, 3,926, 16,214 B | Class body minus 170 B for the default profile; recomputed from MPE-CRY-036 for any other profile |
| GossipSub maximum transmit size (P-FMT-6, P-NET-8) | 65,536 B | 65,536 B |
| Maximum Envelope lifetime L_max (P-FMT-3) | 172,800 s (48 h) | 172,800 s; hard ceiling 1,209,600 s (MPE-FMT-033) |
| Ordinary retention (P-STO-1) and retention deadline | Retention deadline = visible expiry, at most P-FMT-3 + P-FMT-4 after arrival | Same; optional paid archive up to 604,800 s (P-STO-7) |
| Expiry clock tolerance (P-FMT-4; replaces P-PUB-8 in delivery rules) | 60 s | 60 s |
| Chain-view staleness threshold (P-NET-13; absorbs P-FMT-5 and P-OPS-10) | 60 s | 60 s |
| Membership-root acceptance window (P-ECO-5) | 3,600 s counted from the root's supersession; the current root is always eligible | Same |
| Stale-root bound (P-ECO-4 + P-ECO-5) | 25 h | 25 h |
| Admission window and tolerance (P-ECO-1, P-ECO-6) | 60 s; 20 s | 60 s; 20 s |
| Admission nullifier retention and restart barrier (P-ECO-7) | 140 s | 140 s |
| Membership period (P-ECO-4) | 86,400 s (mock Bus Registry) | 86,400 s |
| Lowest-tier publication quota (P-ECO-2, P-ECO-3) | Per-class limits (64, 16, 4, 1) Envelopes per admission window for classes 0-3, committed in the membership leaf; one admission nullifier per Envelope | Same vector; an exact 64-credit byte debit (credit = 256 B of body) only if a circuit spending several admission nullifiers passes P-ECO-11 and P-ECO-12 |
| Per-Shard capacity (P-PRF-1, P-PRF-2, P-VER-2) | 10 Envelopes/s and 64 KiB/s per Shard, whichever binds first | Same |
| Comparison and burst loads (P-PRF-28, P-PRF-29, P-VER-4, P-VER-5, P-VER-9, P-VER-10) | 50 Envelopes/s for 24 h as a comparison; 100 Envelopes/s per Shard for 60 s as a burst | Not capacity targets |
| Shard count (P-PUB-1, P-NET-9) | 1 operating; 8 in the benchmark topology (P-PRF-3) | 1 at launch; allowed range 1-8 |
| Mesh tuple D, D_lo, D_hi, D_out (P-NET-1..4, P-PRF-4, P-SEC-1) | (8, 6, 12, 4); (6, 5, 12, 2) as mandatory comparison | (8, 6, 12, 4) |
| Heartbeat, gossip factor, prune backoff, flood publishing | 1 s, 0.25, 60 s, off | 1 s, 0.25, 60 s, off |
| Edge Bus Node bandwidth (P-PRF-12) | At most 6 Mbit/s egress and 6 Mbit/s ingress at one Shard's byte cap | Same |
| Full Bus Node bandwidth (P-PRF-13) | At most 24 Mbit/s per direction with 4 Shards at their byte caps | Same |
| Bus Node CPU (P-PRF-14, P-PRF-15) | 0.30 core edge; 2 cores full | Same |
| Bus Node memory ceiling (new P-PRF-34) | 2 GiB resident | 2 GiB resident |
| Bus Node application seen-set retention (MPE-PUB-027, P-STO-6) | Expiry + P-FMT-4 (60 s) | Same |
| Client deduplication retention (P-CON-2) | Expiry + 3,600 s | Same |
| Recognition key cap (P-CRY-4, P-PUB-4, P-CON-7) | 256 keys; allowed range 1-256 | Same |
| Recognition Tag and salt (P-CRY-2, P-CRY-3; withdraws P-CON-5, P-CON-6) | 16 B Recognition Tag and 16 B salt in the Sealed Body clear prefix | Same |
| Sequence-gap wait (P-PUB-7; withdraws P-CON-1) | 120 s | 120 s |
| Reconciliation interval and independent sources (P-PUB-3, P-CON-4, P-CON-3, P-SEC-2) | 60 s; 2 sources from distinct mock Bus Operators | 60 s; 2 sources from distinct Bus Operators |
| Full-Shard streams per Bus Node (P-PUB-10, P-PRF-17) | 4 per Bus Node; 500 per gateway (P-PRF-18) | Same |
| Per-peer pre-verification rate (P-ECO-10, P-NET-10) | 20 Envelopes/s per peer per Shard | Same |
| Verification queues (P-SEC-3, P-SEC-4) | 8 jobs per peer; 128 total | Same |
| Publisher retry (P-PUB-5, P-PUB-6) | 5 s; 3 Bus Nodes | Same |
| Latency gates (P-PRF-10, P-PRF-11, P-VER-6, P-VER-7, P-VER-21..23) | Post-admission delivery p99 at most 10 s and at least 99.9% of eligible pairs within 10 s; warm propagation p50 1.5 s and p99 3 s recorded, a miss triggers MPE-PRF-011 | Warm propagation p50 at most 1.5 s and p99 at most 3 s; canary delivery at least 99.9% within 5 s for 30 consecutive days |
| Attack thresholds (P-PRF-22..24, P-VER-25, P-OPS-5) | 20% cold-start Sybil: at least 99% delivery and completed p99 at most 6 s; failure at 200 nodes triggers MPE-PRF-038 | Open-admission red team at 1:1 Sybil identities: canary delivery at least 99.9% (P-OPS-5) |
| Adversarial fractions (P-SEC-6, P-PRV-1, P-VER-11, P-VER-12, P-PRF-22) | Placements 1, 3, 5, 20%; first-spy coalitions 1, 3, 5, 10, 20% | Same sets for the red team |
| Soak duration (P-PRF-25, P-VER-3) | 72 h at 10 Envelopes/s per Shard | Replaced by the 30-day canary window |
| Topology sizes (P-VER-1, P-PRF-9, P-VER-8) | 32 local Bus Node processes for reference runs (at least 16 for MPE-VER-011); simulations at 50, 200 and 1,000 | Not applicable |
| Store Node allocation (P-STO-3) and Bus Node caches (P-STO-4) | 32 GiB per retained Shard; 1 GiB | Same |
| Distinct Bus Operators for 'stored' (P-STO-5) | 3 mock Bus Operators (new MPE-OPS-055) | 3 |
| Anchor window and granularity (P-NET-17) | 60 s; one Anchor per non-empty window covering every Shard | Same |
| Live Anchor history (P-STO-9, P-STO-10) | 176,400 s (49 h); 2,940 records | Same |
| Unanchored wait (P-CON-8) | 300 s | 300 s |
| Tombstone deadline (P-SEC-5, P-STO-14, P-OPS-13) | Feature disabled | 24 h |
| Version overlap (P-FMT-9, P-OPS-19) | Not applicable (single version) | 2 x 172,800 s + 30 days = 34 days |
| Bootstrappers (P-OPS-3, P-NET-11, P-SEC-2) | 2 local bootstrappers from 2 mock Bus Operators | 4, each run by a distinct Bus Operator |
| Launch relay roster (P-OPS-1, P-OPS-2) | Mock roster of at least 3 organizations | At least 8 organizations; at most 20% of listed relays each |
| Chain-share budget (P-ECO-8) | Not applicable (mock ledger) | 10% of blockUsage, 24 h mean, enforced by client back-off |
| Skipped-key retention (P-CRY-7) | Not applicable (no ratchet) | 172,800 s; 604,800 s only where an archive profile is enabled |
| Bond and deposit amounts (P-ECO-14..17) | None | None at launch; if enabled, amount set from the MPE-ECO-050 flood cost, withdrawal delay 7 days, reporter share at most 10% |
| Admission gates (P-ECO-11, P-ECO-12, P-ECO-13) | Encoded Admission Slot at most 4,096 B (a proof of at most 3,992 B); verification at most 10 ms on one core of a 4-vCPU VM | Same, plus registration at most 16 KiB and 0.5 DUST |
| Chaos, race and usability fixtures (P-VER-13/P-CON-10, P-VER-17/P-CON-12, P-VER-18..20/P-CON-13) | 1,000,000 Messages; 100 reactors; 4 of 5 developers within 4 h | Same |

| Parameter | Meaning and default |
|---|---|
| P-CON-9 | Pending-gap state per publisher, in sequence numbers |
| P-CON-11 | Upper bound of the random delay on helper-submitted reactions |
| P-CRY-1 | Symmetric stream-secret length |
| P-CRY-5 | Maximum skipped-message derivations for one ratcheted session transition |
| P-CRY-6 | Maximum retained skipped-message keys per Subscriber device |
| P-CRY-8 | Experimental FMD2 false-positive probability for unrelated valid clues |
| P-ECO-9 | Client back-off threshold (last block's `blockUsage` fullness) |
| P-ECO-15 | Reporter share of a slashed bond |
| P-ECO-16 | Treasury runway divisor (daily payout ≤ balance ÷ P-ECO-16) |
| P-ECO-17 | Payout saturation divisor k (per-bond-key share ≤ pool ÷ k) |
| P-ECO-18 | Retention-challenge response deadline |
| P-FMT-7 | Maximum fragments per Message, where fragmentation is enabled |
| P-FMT-8 | Maximum `Misc` parts per ledger-lane MPE Envelope: 16, set by the fee limit; one 16-part call is a k = 22 circuit, against k = 20 for 4 parts |
| P-FMT-10 | `Misc` name constants `mip-xxxx:anchor[v1]`, `mip-xxxx:envelope[v1]` and `mip-xxxx:governance[v1]` (ASCII, NUL-padded to 32 B; `xxxx` becomes the assigned MIP number; a new layout takes a new name) |
| P-FMT-11 | Envelope Identifier domain string: `midnight-pe/id/v1` |
| P-NET-2 | `D_lo` |
| P-NET-3 | `D_hi` |
| P-NET-4 | `D_out` (outbound mesh quota) |
| P-NET-5 | Heartbeat interval |
| P-NET-6 | Gossip factor |
| P-NET-7 | Prune backoff |
| P-NET-12 | Warm-up before local injection |
| P-NET-14 | Independent chain sources per Ledger Adapter |
| P-NET-15 | IP-colocation (P6) threshold |
| P-NET-16 | Heartbeats within which a continuously misbehaving mesh peer is pruned |
| P-NET-18 | IDONTWANT message-size threshold |
| P-OPS-4 | Sybil peer identities held by the allow-list red-team |
| P-OPS-6 | Delay before an approved parameter change takes effect |
| P-OPS-7 | Expiry of an emergency action that has not been ratified |
| P-OPS-8 | Public notice period before a Bus Registry maintenance update |
| P-OPS-9 | Maximum steward seats held by one organization |
| P-OPS-11 | Time from relay removal to the end of meshing by every Bus Node |
| P-OPS-12 | Evidence window for ejection in the open stage |
| P-OPS-14 | Transparency-report period |
| P-OPS-15 | Time after which debug logging switches itself off |
| P-OPS-16 | Minimum number of independent monitor organizations and share keepers |
| P-OPS-17 | Canary publication interval per Shard |
| P-OPS-18 | Differential-privacy ε for published relay counters |
| P-OPS-20 | Independent signers per release |
| P-OPS-21 | Time to deploy a Sev1 mitigation (Sev2: 12 h; Sev3: 72 h) |
| P-OPS-22 | Maximum duration of a pause→resume drill |
| P-OPS-23 | Consecutive days at the canary gate needed to exit the permissioned stage |
| P-OPS-24 | Horizon of written Bus Operator funding commitments |
| P-OPS-25 | Organic load below which no anonymity-set claim is published |
| P-OPS-26 | Distinct active publisher admissions below which no anonymity-set claim is published |
| P-OPS-27 | Deadline for publishing a post-mortem |
| P-PRF-3 | Benchmark Shard count: 8 |
| P-PRF-5 | Gossip factor: 0.25 |
| P-PRF-6 | Heartbeat interval: 1 s |
| P-PRF-7 | Flood publishing: disabled |
| P-PRF-8 | Sidecar connection planning limit: 50 peers |
| P-PRF-16 | Full Bus Node Shard allocation: at most 4 Shards |
| P-PRF-18 | Gateway topology: 20 gateways, 500 Subscribers each, 10,000 Subscribers total; each gateway has 8 vCPU, 16 GiB RAM and 1 Gbit/s networking |
| P-PRF-19 | Desktop recognition profile: 100 Envelopes/s, 32 recognition keys, 4 KiB complete Envelopes |
| P-PRF-20 | Desktop recognition CPU: ≤0.5 core under P-PRF-19 |
| P-PRF-21 | Mobile recognition CPU: ≤50 ms CPU/s at 10 Envelopes/s with one recognition key |
| P-PRF-23 | Attack delivery floor: 99% |
| P-PRF-24 | Attack propagation p99 ceiling: 6 s |
| P-PRF-26 | Burst duration: 60 s |
| P-PRF-27 | Validation/publication queue capacities |
| P-PRF-30 | Aggregate load suite: 2, 20 and 200 Envelopes/s network-wide, uniform over eight Shards; 4 KiB complete-Envelope fixture |
| P-PRF-31 | Recovery workload: 20 unique Envelopes/s total live-plus-back-fill service |
| P-PRF-32 | Synchronized admission window burst: 300 Publishers |
| P-PRF-33 | Indexer comparison: 1 Message/s average, 10/s peak, 10,000 Subscribers; 8 vCPU and 100 Mbit/s; fan-out p99 target 2 s after `BlockIndexed` |
| P-PUB-2 | Pull cadence while retrieving a Shard by pull |
| P-PUB-9 | Back-fill page size |
| P-PUB-11 | Silence before the client reports `disconnected` |
| P-STO-2 | Maximum delay for removing an expired record from managed live storage |
| P-STO-7 | Optional archive agreement duration, measured from authenticated creation time |
| P-STO-8 | Client Message payload cache allocation |
| P-STO-11 | Interval between scheduled per-Shard availability probes |
| P-STO-12 | Successful within-retention canary retrieval target |
| P-STO-13 | Availability assessment interval |
| P-VER-14 | Decoder fuzz campaign size |
| P-VER-15 | Post-burst queue recovery deadline |
| P-VER-16 | Admission attack identity count |
| P-VER-19 | Successful usability completions |
| P-VER-20 | Usability completion deadline |
| P-VER-22 | Production canary timely delivery fraction |
| P-VER-23 | Production canary delivery deadline |
| P-VER-24 | Pause-to-resume drill deadline |

## A.2 Message and MPE Envelope format (MPE-FMT) {#a2-fmt}

**MPE-FMT-001a** Fixed-width visible layout. *(POC, MUST, settled)*  
The MPE client library shall encode every MPE Envelope field outside the Sealed Body as a fixed-width field at a fixed per-version offset.  
*Verification.* test, decode and re-encode every MPE-FMT-049 vector and compare the bytes for equality.

**MPE-FMT-001b** No variable encodings outside the Sealed Body. *(POC, MUST, settled)*  
The MPE client library shall emit no optional field, extension field, length prefix, variable-length integer or self-describing encoding outside the Sealed Body.  
*Verification.* inspection, review the wire specification; test, every fuzzed Envelope that carries such a construct fails MPE-FMT-006 or MPE-FMT-007.

**MPE-FMT-002** Byte order. *(POC, MUST, open: DEC-FMT-7)*  
The MPE client library shall encode every multi-byte integer in the Visible Header and the Sealed Prefix in big-endian byte order.  
*Verification.* test: `expiry` = 0x01020304 encodes as bytes 01 02 03 04 at offset 4.

**MPE-FMT-003** Visible fields. *(POC, MUST, open: DEC-FMT-2)*  
Outside the Sealed Body, the MPE client library shall place only `version`, `size_class`, `shard`, `reserved`, `expiry` and the Admission Slot, at the offsets in the Visible Header table.  
*Verification.* inspection; test: 10^4 Prototype Envelopes each have a header of 8 + P-FMT-2 bytes, and no plaintext outside the header, the Admission Slot, the Sealed Body's `MPE-FMT-051` clear prefix (salt, nonce, Recognition Tag) and the authenticator.

**MPE-FMT-004** No identity-derived visible values. *(POC, MUST, open: DEC-FMT-2)*  
Outside the Sealed Body, the MPE client library shall place no value derived from a stream identifier, a recipient key or a Publisher long-term key. The `shard` field is the only exception.  
*Verification.* test: within each size class, compare 1,000 Envelopes from one Publisher and stream with 1,000 from distinct Publishers and streams; outside `shard` and `expiry`, the largest per-offset chi-square statistic, with its p-value from 1,000 random relabellings of the two samples, stays above the 1 percent family-wise level, and a planted constant byte at one offset of the single-Publisher sample is flagged.

**MPE-FMT-005** Admission Slot unlinkability. *(POC, MUST, settled)*  
The MPE client library shall place no value in the Admission Slot that is constant across one Publisher's MPE Envelopes and differs between Publishers.  
*Verification.* test: two memberships send 100 Envelopes each in one admission window. No Admission Slot byte range is constant within one membership and different between the two.

**MPE-FMT-006** Reserved bytes. *(POC, MUST, settled)*  
If a received MPE Envelope has a non-zero reserved byte, then the Bus Node shall return Reject.  
*Verification.* test: set each reserved bit of a valid vector in turn; each result is Reject.

**MPE-FMT-007** Exact length. *(POC, MUST, settled)*  
If a received MPE Envelope's length differs from 8 + P-FMT-2 + the P-FMT-1 body length of its `size_class`, then the Bus Node shall return Reject.  
*Verification.* test: valid vectors shortened by 1 B or lengthened by 1 B are Rejected.

**MPE-FMT-008** Unknown size class. *(POC, MUST, settled)*  
If a received MPE Envelope's `size_class` has no entry in P-FMT-1, then the Bus Node shall return Reject.  
*Verification.* test: `size_class` values 4 to 255 are Rejected.

**MPE-FMT-009** Structural checks first. *(POC, MUST, settled)*  
The Bus Node shall complete the version, reserved-byte, size-class, length and expiry checks on an MPE Envelope before it runs any cryptographic verification on it.  
*Verification.* test: send 10^4 malformed Envelopes with well-formed Admission Slots; the verification counter stays at 0.

**MPE-FMT-010** Transmit size bound. *Same obligation as MPE-NET-014, which owns it.*

**MPE-FMT-011** Body-blind validation. *(POC, MUST, settled)*  
The Bus Node shall compute every validation outcome without decrypting or parsing the Sealed Body.  
*Verification.* inspection: the validator links no AEAD or schema decoder. Test: Envelopes with random Sealed Bodies and valid admission get the same outcome as real ones.

**MPE-FMT-012** GossipSub carriage. *Same obligation as MPE-NET-009a and MPE-NET-009b, which own it together.*

**MPE-FMT-013** Sealed Body length. *(POC, MUST, open: DEC-FMT-1)*  
The MPE client library shall produce a Sealed Body whose length equals the P-FMT-1 entry for the MPE Envelope's `size_class`.  
*Verification.* test: every Prototype Envelope has a body length listed in P-FMT-1 that matches its class byte.

**MPE-FMT-014** Smallest fitting class. *(POC, MUST, settled)*  
When publishing a Message, the MPE client library shall select the smallest size class whose payload capacity holds the payload, unless the application names a larger class.  
*Verification.* test: payloads exactly at each class capacity, and 1 B over it, land in the expected classes.

**MPE-FMT-015** Oversize payload. *(POC, MUST, settled)*  
If a Message payload exceeds the payload capacity of the largest size class, then the MPE client library shall return a payload-too-large error and publish no MPE Envelope.  
*Verification.* test: a payload of capacity + 1 B returns the error, and no Envelope reaches the mesh.

**MPE-FMT-016** Sealed padding. *(POC, MUST, settled)*  
The MPE client library shall place all padding inside the authenticated encryption, so that Messages of different payload lengths in one size class produce MPE Envelopes of equal length.  
*Verification.* test: in each class, a 1 B payload and a full-capacity payload give equal wire lengths.

**MPE-FMT-017** Padding check. *(POC, MUST, settled)*  
If the padding of an opened Message contains a non-zero byte, then the MPE client library shall discard the Message as malformed.  
*Verification.* test: a vector re-sealed with one pad byte set to 0x01 is discarded and counted.

**MPE-FMT-018** Envelope Identifier. *(POC, MUST, open: DEC-FMT-3)*  
The MPE client library shall compute the MPE Envelope Identifier as SHA-256 over the P-FMT-11 domain string, the Network Identifier, Visible Header bytes 0 to 7 and the Sealed Body, excluding the Admission Slot.  
*Verification.* test vectors; test: one body under two different Admission Slots yields one identifier.

**MPE-FMT-019** GossipSub message id. *Same obligation as MPE-NET-010, which owns it.*

**MPE-FMT-020** Acyclic construction. *(POC, MUST, settled)*  
The MPE client library shall build an MPE Envelope in this order: Sealed Body, then MPE Envelope Identifier, then Admission Slot. No step takes input from a later step.  
*Verification.* inspection; test vectors rebuild each stage from earlier stages only.

**MPE-FMT-021** Network binding. *(POC, MUST, settled)*  
If a received MPE Envelope was admitted under a different Network Identifier, then the Bus Node shall return Reject.  
*Verification.* test: an Envelope valid on a test network is Rejected by a Bus Node configured with a different genesis hash.

**MPE-FMT-022** Logical Message Identifier. *(POC, MUST, settled)*  
The MPE client library shall seal a random 16-byte Logical Message Identifier that is the same in every retransmission and every carrier of one Message.  
*Verification.* test: one Message sent on the overlay and on the mock ledger carrier opens with equal Logical Message Identifiers.

**MPE-FMT-023** Version bound to GossipSub topic. *(POC, MUST, open: DEC-FMT-4)*  
If a received MPE Envelope's `version` differs from the supported version assigned to the GossipSub topic it arrived on, then the Bus Node shall return Reject.  
*Verification.* test: `version` = 2 on a supported v1 GossipSub topic is Rejected and lowers the forwarding peer's P₄ score; validity that cannot be determined for lack of protocol support follows MPE-SEC-008 (Ignore).

**MPE-FMT-024** Version overlap. *(PROD, MUST, open: DEC-FMT-4)*  
Where two MPE Envelope versions are active, the Bus Node shall relay the GossipSub topics of both versions for at least P-FMT-9 after the newer version activates.  
*Verification.* simulation, upgrade half the nodes; no unexpired old-version Envelope is lost during the window.

**MPE-FMT-025** Unsupported sealed format. *(POC, MUST, settled)*  
If an opened Sealed Prefix has an unknown `pt_version` or `kind`, then the MPE client library shall return a typed unsupported-format error to the application.  
*Verification.* test: vectors with `pt_version` = 2 or with an undefined `kind` return the typed error.

**MPE-FMT-026** Unknown schema. *Same obligation as MPE-PUB-049, which owns it.*

**MPE-FMT-027** Static decoder dispatch. *(POC, MUST, settled)*  
The MPE client library shall select a payload decoder only from a table that is keyed by schema identifier and fixed when the application registers.  
*Verification.* inspection: no eval, reflection or dynamic loading keyed by payload bytes; fuzz test of the decoder path.

**MPE-FMT-028** Expiry field. *(POC, MUST, open: DEC-FMT-5)*  
The MPE client library shall set `expiry` to an unsigned 32-bit Unix time in seconds, no later than its own clock plus P-FMT-3.  
*Verification.* test: at creation, Prototype Envelopes satisfy `now < expiry ≤ now + P-FMT-3`.

**MPE-FMT-029** Expiry too far ahead. *(POC, MUST, settled)*  
If a received MPE Envelope's `expiry` exceeds the Bus Node's clock plus P-FMT-3 plus P-FMT-4, then the Bus Node shall return Reject.  
*Verification.* test: `expiry` = now + P-FMT-3 + P-FMT-4 + 1 s is Rejected; one second less is not.

**MPE-FMT-030** Expired on arrival. *(POC, MUST, settled)*  
If a received MPE Envelope's `expiry` is earlier than the Bus Node's clock minus P-FMT-4, then the Bus Node shall return Ignore.  
*Verification.* test: an expired Envelope is not forwarded, and the sender's P₄ counter does not change.

**MPE-FMT-031** Unsafe clock. *(POC, MUST, settled)*  
While the Ledger Adapter view is stale under MPE-NET-019, the Bus Node shall return Ignore instead of Reject for an MPE Envelope that fails the expiry check of MPE-FMT-029.  
*Verification.* test, shift the mock adapter timestamp by P-NET-13 + 1 s; far-future expiry yields Ignore and valid Envelopes are still accepted.

**MPE-FMT-032** No forwarding after expiry. *(POC, MUST, settled)*  
When an MPE Envelope's `expiry` passes, the Bus Node shall stop sending that MPE Envelope to peers, including IWANT responses and sends already queued.  
*Verification.* test: an IWANT for an expired identifier and a send queued before expiry both transmit nothing; a conformance test is recorded for each transport implementation, because stock GossipSub message caches do not read the MPE expiry field.

**MPE-FMT-033** Lifetime ceiling. *(PROD, MUST, settled)*  
The Bus Registry shall reject any P-FMT-3 parameter value above 1,209,600 s.  
*Verification.* test on the Bus Registry model: a parameter change to 1,209,601 s fails.

**MPE-FMT-034** Sealed Prefix. *(POC, MUST, open: DEC-FMT-7)*  
The MPE client library shall begin every Sealed Body plaintext with the Sealed Prefix fields `pt_version`, `kind`, `flags`, `payload_len`, `schema_version`, `seq`, Logical Message Identifier and schema identifier.  
*Verification.* inspection; test vectors decode every field.

**MPE-FMT-035** Sealed control packets. *(PROD, MUST, settled)*  
The MPE client library shall carry every session or group control packet, including any MLS framing, entirely inside a Sealed Body.  
*Verification.* inspection; test: no MLS header byte appears outside the Sealed Body.

**MPE-FMT-036** No receipt kind. *(POC, MUST, open: DEC-FMT-6)*  
The MPE client library shall define no MPE Envelope `kind` whose purpose is to acknowledge receipt to a Publisher.  
*Verification.* inspection of the `kind` table.

**MPE-FMT-037** Carrier-independent body. *(POC, MUST, open: DEC-FMT-8)*  
The MPE client library shall open a Sealed Body using only its bytes, the `version`, the `size_class` and the recipient's key material.  
*Verification.* test: a body taken from the mock ledger carrier opens exactly as its overlay copy does.

**MPE-FMT-038** Explicit external fetch. *(POC, MUST, settled)*  
The MPE client library shall not retrieve an object referenced inside a Message unless the application calls an explicit fetch operation.  
*Verification.* test: receiving a Message that contains a reference produces no outbound request.

**MPE-FMT-039** Optional fragmentation. *(PROD, MAY, open: DEC-FMT-6)*  
Where sealed fragmentation is enabled, the MPE client library shall deliver a fragmented Message only after all of its fragments (at most P-FMT-7) have been opened.  
*Verification.* test: drop one of 16 fragments; nothing is delivered, and the partial set expires.

**MPE-FMT-040** Constant `Misc` name for ledger-lane parts. *(POC, MUST, settled)*  
The MPE client library shall set the `Misc` `name` of every part of a ledger-lane MPE Envelope to the P-FMT-10 envelope name `mip-xxxx:envelope[v1]`, NUL-padded to 32 bytes.  
*Verification.* test: all parts from two different streams carry byte-identical 32-byte `name` fields equal to `mip-xxxx:envelope[v1]` followed by NUL bytes.

**MPE-FMT-041** Part split. *(POC, MUST, open: DEC-FMT-1)*  
The MPE client library shall carry a class-c Sealed Body on the ledger as 4^c `Misc` events whose 256-byte payloads, concatenated in emission order, equal that body.  
*Verification.* test vectors for classes 0 to 2 against the mock Ledger Adapter.

**MPE-FMT-042** One phase of one intent. *(PROD, MUST, settled)*  
The MPE client library shall emit all parts of one ledger-lane MPE Envelope within one execution phase of one intent.  
*Verification.* inspection of the built transactions: all parts of an Envelope sit in one segment, guaranteed or fallible (a 16-part call exceeds the guaranteed-segment budget); ledger-9 devnet test with a failing fallible segment shows that no part of that Envelope is applied.

**MPE-FMT-043** One `Misc` per part. *(POC, MUST, settled)*  
The MPE client library shall emit each ledger part as one `Misc` event whose struct data is 288 bytes: a 32-byte name and a 256-byte payload.  
*Verification.* inspection of the contract; test: every emitted `Misc` carries 288 bytes of struct data; the serialized size, about 40 bytes larger by MIP-0002's estimate, is measured under MPE-PRF-040.

**MPE-FMT-044** Ledger part limit. *(POC, MUST, settled)*  
If an application asks for ledger carriage of an MPE Envelope that needs more than P-FMT-8 parts, then the MPE client library shall return an error without building a transaction.  
*Verification.* test: a request for ledger-lane carriage of a class-3 Envelope returns the error and submits nothing; analysis: the proving circuit size of the largest permitted call is stated (16 parts in one call is k = 22 with 2,651,779 rows; 4 parts is k = 20) under MPE-PRF-043.

**MPE-FMT-045** Ledger reassembly. *(POC, MUST, settled)*  
When reading ledger-carried MPE Envelopes, the MPE client library shall concatenate, in ledger emission order, the payloads of parts named P-FMT-10 that come from one transaction and one physical intent.  
*Verification.* test: interleaved parts from two intents in one block reassemble into two bodies.

**MPE-FMT-046** Malformed ledger group. *(POC, MUST, settled)*  
If a reassembled ledger group has a part count that is not 4^c for a defined class c, then the MPE client library shall discard the group as malformed.  
*Verification.* test: groups of 2, 3 and 5 parts are discarded and counted.

**MPE-FMT-047** Anchor notification event. *(PROD, MUST, settled)*  
The Bus Registry shall emit each Anchor as one `Misc` event named `mip-xxxx:anchor[v1]`, NUL-padded to 32 bytes, whose payload is the MPE-NET-050 Anchor payload.  
*Verification.* ledger-9 devnet test: each Anchor transaction produces exactly one `Misc` with that name and a 256-byte payload; consumers verify Anchors against Bus Registry state (MPE-CON-016), not against this event.

**MPE-FMT-048** Admission Slot measurement. *Same obligation as MPE-ECO-048, which owns it.*

**MPE-FMT-049** Test vectors. *(POC, MUST, settled)*  
The Prototype shall publish byte-exact test vectors for each size class, the Sealed Prefix, the MPE Envelope Identifier, the binding between Admission Slot and identifier, and the ledger part split.  
*Verification.* test: an independent decoder reproduces every vector.

**MPE-FMT-050** Admission Slot zero fill. *(POC, MUST, settled)*  
If any Admission Slot byte after the selected proof fields is non-zero, then the Bus Node shall return Reject.  
*Verification.* test, set each filler byte of a valid vector in turn; each result is Reject.

**MPE-FMT-051** Sealed Body clear prefix. *(POC, MUST, open: DEC-CRY-2)*  
The MPE client library shall place the P-CRY-3-byte salt, the 12-byte AEAD nonce and the P-CRY-2-byte Recognition Tag, in that order, at the start of the Sealed Body before the ciphertext.  
*Verification.* test vectors; a body copied from the mock ledger carrier opens exactly as its overlay copy.

**MPE-FMT-052** Shard field matches GossipSub topic. *(POC, MUST, settled)*  
If a received MPE Envelope's `shard` value differs from the Shard index of the GossipSub topic it arrived on, then the Bus Node shall return Reject.  
*Verification.* test, an Envelope with `shard` = 1 published on the Shard-0 GossipSub topic is Rejected and lowers the sender's P4 score.

**MPE-FMT-053** One cryptographic profile per version and suite. *(POC, MUST, open)*  
The MPE client library shall bind each MPE Envelope version to exactly one cryptographic profile, identified by the `version` value; the profile's one-byte suite identifier names it in invitations and in the label table and is not a wire field.  
*Verification.* inspection, the profile table maps each `version` to one suite and profile, and a new suite takes a new version; test, an Envelope opened under another profile fails authentication.

**MPE-FMT-054** Carried-event schema. *(PROD, MUST, settled)*  
The MPE client library shall reserve one schema identifier for carried events, whose payload holds a contract event, the hash of the transaction that recorded it and its position within that transaction.  
*Verification.* inspection of the schema table; test vectors encode and decode a carried public event with its transaction hash and position.

**MPE-FMT-055** Carried-event bytes unchanged. *(PROD, MUST, settled)*  
When sealing a carried event, the MPE client library shall place the contract event's `VersionedLogItem` bytes in the payload exactly as the transaction records them.  
*Verification.* test: for events captured during local circuit execution, the carried bytes equal the bytes the Indexer later serves for the same transaction and position; no field is re-typed, re-ordered or truncated.

**MPE-FMT-056** Carried-event transaction reference. *(PROD, MUST, settled)*  
The MPE client library shall include in every carried event the hash of the recording transaction and the event's position among that transaction's contract events.  
*Verification.* test: a Consumer locates the event in the finalized transaction from the carried hash and position alone.

**MPE-FMT-057** Midnight decoder for carried events. *(PROD, MUST, settled)*  
The MPE client library shall decode a carried event only with the decoder Midnight defines for its `LogEventType` and schema `version`, never with an application payload decoder.  
*Verification.* inspection of decoder dispatch; test: a carried event whose bytes also parse under a registered application schema is decoded only by the Midnight decoder.

**MPE-FMT-058** Carried `@topic` values sealed. *(PROD, MUST, open)*  
Where a carried private event contains `@topic` values, the MPE client library shall carry those values only inside the Sealed Body.  
*Verification.* inspection and test: visible header, Admission Slot and Recognition Tag of a carried private event are independent of its `@topic` values.

**MPE-FMT-059** Few non-constant emitted bytes. *(PROD, SHOULD, settled)*  
The Bus Registry shall emit no more than 72 non-constant payload bytes per Anchor event and 35 per governance event.  
*Verification.* inspection of every `emit` site; analysis: circuit rows per emitted event, since each non-constant emitted byte adds byte-decomposition rows (a 256-byte circuit argument costs 166,241 rows, k = 18).


## A.3 Cryptography and key management (MPE-CRY) {#a3-cry}

CRY owns Message sealing, cryptographic recognition, key derivation, rotation, publisher authentication, nonce safety and cryptographic replay protection.
The recommended Prototype default uses authenticated invitations, symmetric stream secrets, locally tested salted Recognition Tags and sealed publisher signatures.
That default makes no forward-secrecy claim; an optional production session profile targets hybrid establishment with encrypted-header Double Ratchet.
Fuzzy detection is not part of the design (`DEC-020`); `MPE-CRY-038` and `MPE-CRY-039` apply only if a separately specified future profile adds it.
Shard selection, transport admission, storage availability and contract execution belong to other areas; cryptography supplies their required bindings.

**MPE-CRY-001** Default cryptographic profile. *(POC, MUST, open: DEC-CRY-1)*  
The MPE client library shall implement, as suite 0x01, an invitation-based symmetric profile using HKDF-SHA-256 key derivation, HMAC-SHA-256 recognition, ChaCha20-Poly1305 sealing and plain Ed25519 publisher authentication.  
*Verification.* test, independent implementations agree on derivation, sealing, recognition and signature vectors, and every Envelope of this profile carries suite identifier 0x01.

**MPE-CRY-002** Sealed application metadata. *(POC, MUST, settled)*  
The MPE client library shall encrypt the Message’s private stream identifier, publisher identity, schema, logical identifier, sequence, application timestamps, payload and publisher signature inside the MPE Envelope.  
*Verification.* inspection, the wire-field inventory contains these fields only within authenticated ciphertext.

**MPE-CRY-003** Authenticated padding. *Same obligation as MPE-FMT-016, which owns it.*

**MPE-CRY-004** Public-context authentication. *(POC, MUST, settled)*  
The MPE client library shall authenticate the Network Identifier, Visible Header bytes 0 to 3 and the Sealed Body's salt, nonce and Recognition Tag as AEAD associated data, and bind Visible Header bytes 4 to 7 by fixing `expiry` at creation plus 172,800 s and covering creation and expiry in the signed statement.  
*Verification.* test, changing any associated byte prevents opening; changing `expiry` changes the MPE Envelope Identifier and fails the Subscriber's comparison with the signed expiry.

**MPE-CRY-005** Acyclic Envelope construction. *Same obligation as MPE-FMT-020, which owns it.*

**MPE-CRY-006** Domain separation. *(POC, MUST, settled)*  
The MPE client library shall separate Recognition Tags, encryption keys, associated data, publisher signatures, MPE Envelope identifiers, receipts, admission values and consumption nullifiers with the distinct version-1 labels of the MPE-CRY-042 table, binding the Network Identifier and the cryptographic profile where that table's construction includes them.  
*Verification.* test, cross-purpose, cross-network and cross-profile substitution vectors fail; inspection, every label in the code appears in the MPE-CRY-042 table.

**MPE-CRY-007** Purpose-specific derivation. *(POC, MUST, open: DEC-CRY-2)*  
The MPE client library shall derive separate recognition and encryption keys from a stream secret using distinct HKDF-SHA-256 purpose labels, with the MPE Envelope salt included in per-Envelope encryption derivation.  
*Verification.* test, derivation vectors distinguish purposes, salts, networks and profiles.

**MPE-CRY-008** Random stream secrets. *(POC, MUST, settled)*  
When a private stream is created, the MPE client library shall obtain its P-CRY-1-byte stream secret from the operating-system cryptographic random-number interface.  
*Verification.* inspection, stream creation requests exactly P-CRY-1 bytes from the configured interface (getrandom on Linux); test, an injected interface failure produces the MPE-CRY-009 result.

**MPE-CRY-009** Randomness failure. *(POC, MUST, settled)*  
If required cryptographic randomness cannot be obtained, then the MPE client library shall refuse the affected cryptographic operation with a local failure result.  
*Verification.* test, injected entropy failure produces no key, ciphertext or bootstrap publication.

**MPE-CRY-010** Nonce uniqueness. *(POC, MUST, settled)*  
The MPE client library shall use each AEAD key–nonce pair for at most one encryption operation.  
*Verification.* test, forced nonce repetition, concurrent publication and crash recovery cannot produce a second encryption under the same pair.

**MPE-CRY-011** Unsafe restored state. *(POC, MUST, settled)*  
If restored client state cannot establish nonce uniqueness or ratchet-state freshness, then the MPE client library shall refuse publication under the affected key generation until authenticated re-establishment.  
*Verification.* test, restoring a pre-publication snapshot prevents subsequent publication under its obsolete generation.

**MPE-CRY-012** Exact retransmission. *Same obligation as MPE-PUB-023, which owns it.*

**MPE-CRY-013** Salted Recognition Tags. *(POC, MUST, open: DEC-CRY-2)*  
When sealing a Message, the MPE client library shall generate a P-CRY-2-byte Recognition Tag by truncating HMAC-SHA-256 over the canonical Recognition Tag domain and a fresh P-CRY-3-byte MPE Envelope salt under the stream’s recognition key.  
*Verification.* test, independent vectors agree; arbitrary publisher-sequence gaps do not prevent recognition under a retained stream key.

**MPE-CRY-014** Recognition is provisional. *(POC, MUST, settled)*  
When a Recognition Tag or fuzzy clue matches, the MPE client library shall treat the MPE Envelope only as a candidate for complete Message authentication.  
*Verification.* test, matching hints paired with invalid ciphertext or signatures produce no Message delivery.

**MPE-CRY-015** Local Recognition Tag matching. *Same obligation as MPE-PUB-010, which owns it.*

**MPE-CRY-016** Recognition-key bound. *(POC, MUST, open: DEC-CRY-2)*  
When installing subscription state would exceed P-CRY-4 distinct recognition keys, the MPE client library shall reject that installation with a local capacity result.  
*Verification.* test, installation at the limit succeeds; installation beyond the limit leaves existing subscriptions unchanged.

**MPE-CRY-017** Ambiguous opening. *(POC, MUST, settled)*  
If one MPE Envelope authenticates as belonging to distinct private streams, then the MPE client library shall reject its delivery with a local ambiguity result.  
*Verification.* test, injected multiple-opening vectors produce no delivery to either stream.

**MPE-CRY-018** Authenticated invitations. *(POC, MUST, open: DEC-CRY-3)*  
When installing a private subscription, the MPE client library shall validate an invitation binding the network, cryptographic profile, stream secret or setup material, and authorized publisher keys through the configured authenticated invitation channel.  
*Verification.* test, modified, unauthenticated, foreign-network and unsupported-profile invitations cannot install subscriptions.

**MPE-CRY-019** Revocation rekeying. *(POC, MUST, settled)*  
When an authorized membership change removes a Subscriber from a symmetric private stream, the MPE client library shall generate the replacement stream secret independently of the previous stream secret.  
*Verification.* test, possession of the old secret does not derive the replacement secret or open Messages sealed under it.

**MPE-CRY-020** Publisher signature profile. *(POC, MUST, open: DEC-022)*  
The MPE client library shall authenticate publisher statements with plain Ed25519 in the default cryptographic profile.  
*Verification.* test, library signatures verify over identical statement bytes in a compiled Compact fixture; analysis, consumption-circuit rows, proving time and prover-key size under Ed25519 and JubJub Schnorr (MPE-CRY-043) decide the production profile.

**MPE-CRY-021** Signed statement binding. *(POC, MUST, settled)*  
The MPE client library shall sign a canonical statement binding the signature domain, pre-seal-header digest, private stream identifier, logical identifier, publisher sequence, schema, creation time, expiry, payload digest and applicable destination contract and action.  
*Verification.* test, substituting each signed field causes publisher-signature verification failure.

**MPE-CRY-022** Authenticated delivery. *(POC, MUST, settled)*  
When an MPE Envelope is opened, the MPE client library shall deliver its Message only after validation of the seal, canonical inner encoding, signed context, authorized publisher key and application expiry.  
*Verification.* test, malformed, expired, unauthorized and signature-invalid Messages produce no delivery.

**MPE-CRY-023** Failure-atomic cryptographic state. *(POC, MUST, settled)*  
When processing an incoming MPE Envelope, the MPE client library shall commit cryptographic state changes only after complete Message authentication succeeds.  
*Verification.* test, invalid bodies following valid-looking headers leave persistent cryptographic state unchanged.

**MPE-CRY-024** Authenticated logical replay. *Same obligation as MPE-PUB-037, which owns it.*

**MPE-CRY-025** Secret-bearing consumption nullifiers. *(POC, MUST, settled)*  
Where contract-consumption nullifier derivation is supported, the MPE client library shall derive the consumption nullifier from a Message-specific secret using a canonical domain containing the network and destination contract.  
*Verification.* test, the same Message secret reproduces the destination’s consumption nullifier; changing destination changes it.

**MPE-CRY-026** Explicit security posture. *(POC, MUST, settled)*  
The MPE client library shall expose each profile’s capability record specifying content forward secrecy, key-retention exposure, post-compromise recovery conditions, passive quantum protection, authentication algorithm and metadata-forward-secrecy limitations.  
*Verification.* inspection, capability records distinguish the default from ratcheted profiles and state all retained-key exposure.

**MPE-CRY-027** Wallet-derived admission and invitation keys. *(PROD, MUST, open: DEC-CRY-1)*  
Where wallet-seed derivation is supported, the MPE client library shall derive only the admission secret and invitation identity keys from the seed, through `deriveSecret` with domains `mpe:admission:v1` and `mpe:invitation:v1` and the Network Identifier, the Bus Registry contract address and the membership period as context.  
*Verification.* inspection, derivation paths cannot reconstruct erasable session state from the wallet seed; test with a `deriveSecret` stub: a restored wallet recovers the same admission secret and membership, no derived value equals a spending or encryption key, and a wallet without `deriveSecret` falls back to MPE-ECO-006 generation.

**MPE-CRY-028** Encrypted-header session profile. *(PROD, SHOULD, open: DEC-CRY-1)*  
Where ratcheted pairwise sessions are supported, the MPE client library shall seal the complete encrypted-header Double Ratchet packet within the MPE Envelope’s protected representation.  
*Verification.* inspection, packet captures contain no clear ratchet header or stable session identifier.

**MPE-CRY-029** Ratchet-key erasure. *(PROD, MUST, open: DEC-CRY-1)*  
When a ratcheted session transition becomes durable, the MPE client library shall erase superseded secret state outside the declared skipped-key retention policy.  
*Verification.* inspection, post-transition memory and persistent-state inventories exclude used message keys and obsolete ratchet secrets.

**MPE-CRY-030** Bounded skipped-key retention. *(PROD, MUST, open: DEC-CRY-1)*  
While a ratcheted session is active, the MPE client library shall retain skipped-message keys only within P-CRY-5 derivations per transition, P-CRY-6 stored keys per device and P-CRY-7 seconds after derivation.  
*Verification.* test, boundary gaps and clock advancement enforce every limit without retaining excess keys.

**MPE-CRY-031** Explicit cryptographic gaps. *(PROD, MUST, open: DEC-CRY-1)*  
If opening a Message requires erased keys or would exceed a cryptographic key budget, then the MPE client library shall return a local resynchronization-required result.  
*Verification.* test, over-limit and erased-key back-fill produces an explicit result without reconstructing obsolete state.

**MPE-CRY-032** Hybrid session establishment. *(PROD, SHOULD, open: DEC-CRY-4)*  
Where the hybrid pairwise profile is supported, the MPE client library shall establish sessions using PQXDH instantiated with X25519 and ML-KEM-768, with network, profile, identities and actual KEM public key bound to the bootstrap transcript.  
*Verification.* test, independent bootstrap vectors agree; identity, KEM-key, network and profile substitutions fail.

**MPE-CRY-033** Wrapped bootstrap metadata. *(PROD, MUST, open: DEC-CRY-4)*  
Where invitation-based hybrid establishment is supported, the MPE client library shall protect bootstrap identity keys, prekey identifiers and initialization material with invitation-derived wrapping keys.  
*Verification.* inspection, bootstrap captures reveal no identity key or prekey identifier outside the protected representation.

**MPE-CRY-034** One-time prekey consumption. *(PROD, MUST, settled)*  
When a bootstrap authenticates successfully, the MPE client library shall erase its used one-time prekey private material after durably recording that bootstrap’s identity.  
*Verification.* test, concurrent duplicate bootstraps and restart yield at most one initialization and no remaining consumed private prekey.

**MPE-CRY-035** Establishment failure. *(PROD, MUST, open: DEC-CRY-4)*  
If required one-time prekeys are exhausted, bootstrap authentication fails or selected-profile input validation fails, then the MPE client library shall refuse establishment without selecting a weaker profile.  
*Verification.* test, exhausted, corrupted and downgrade vectors create no session under any alternative profile.

**MPE-CRY-036** Cryptographic size and cost report. *(POC, MUST, settled)*  
The Prototype shall report serialized cryptographic component sizes, complete MPE Envelope sizes, usable payload capacity, operation-time distributions and peak cryptographic-state bytes for every implemented profile at its configured key limits.  
*Verification.* demonstration, a reproducible report accounts for every serialized byte and gives operation times in microseconds and state sizes in bytes.

**MPE-CRY-037** Fuzzy-detection activation. *(POC, MUST, open: DEC-CRY-5)*  
When initializing a client configuration without explicit first-contact FMD opt-in, the MPE client library shall leave fuzzy detection disabled.  
*Verification.* test, default configurations generate no fuzzy clue or delegated detection registration.

**MPE-CRY-038** Restricted detection delegation. *(PROD, MUST, open: DEC-CRY-5)*  
Where first-contact FMD delegation is enabled, the MPE client library shall export only the selected construction’s first-contact detection capability to the detector.  
*Verification.* inspection, detector registration contains only construction-defined first-contact detection material.

**MPE-CRY-039** FMD construction measurement. *(POC, MUST, open: DEC-CRY-5)*  
Where experimental FMD2 is implemented, the Prototype shall report clue size, generation time, testing time, true-match failures and observed unrelated-clue match frequency at P-CRY-8.  
*Verification.* demonstration, a labeled-corpus report states sample counts, configuration, hardware and frequency uncertainty.

**MPE-CRY-040** Production composition gate. *Same obligation as MPE-VER-037, which owns it.*

**MPE-CRY-041** Publisher authentication block. *(POC, MUST, open: DEC-CRY-6)*  
The MPE client library shall encode the sealed publisher authentication block as a 2-byte authorized-key index, a 4-byte creation time and the suite's publisher signature, 64 bytes for Ed25519.  
*Verification.* test vectors; for suite 0x01 the payload capacity per class equals body minus 170 B; any other suite states its signature length and recomputes capacity under MPE-CRY-036.

**MPE-CRY-042** Published label table. *(PROD, MUST, settled)*  
MPE shall publish, in the MIP, the complete table of its domain-separation labels and `Misc` event names, in a form ready for registration under the domain-separation registry that MPS-0027 recommends.  
*Verification.* inspection: every label and `Misc` name used by the code appears in the MIP table; hash, MAC, KDF and signature labels have the form `mpe/v1/<purpose>` or are `midnight-pe/id/v1`, and `Misc` names have the form `mip-xxxx:<name>[v1]`.

**MPE-CRY-043** JubJub Schnorr publisher profile. *(PROD, MAY, open: DEC-022)*  
Where the JubJub publisher profile is enabled, the MPE client library shall sign publisher statements with Schnorr signatures over JubJub that Compact's `jubjubSchnorrVerify` accepts.  
*Verification.* test: library signatures verify in a compiled Compact fixture; analysis: rows, proving time and prover-key size of the consumption circuit compared with the Ed25519 profile.

**MPE-CRY-044** Shielded-key profile deferred. *(PROD, MUST, settled)*  
MPE shall not freeze a suite identifier for a profile that encrypts to Midnight shielded encryption public keys until the `encrypt_for` construct of MPS-0005 Part 2 is published.  
*Verification.* inspection of the suite table and the MIP: the shielded-key profile is listed as deferred with a reserved, unfrozen suite value.

**MPE-CRY-045** Shielded-key first-contact profile. *(PROD, MAY, open: DEC-020)*  
Where the deferred shielded-key profile is enabled, the MPE client library shall encrypt first-contact Messages to the recipient's Midnight shielded encryption public key, resolved through MIP-0007.  
*Verification.* test on a devnet: a recipient resolved through MIP-0007 opens the Message with its shielded encryption key; the profile is disabled by default (DEC-020).

**MPE-CRY-046** Circuit-friendly hash preimages. *(PROD, MUST, settled)*  
MPE shall define every protocol hash that a circuit computes over a struct preimage of fixed-width fields, never over a byte-level concatenation.  
*Verification.* inspection of the hash definitions; test: struct and concatenated preimages give identical SHA-256 digests in the simulator, and the circuit row counts of both forms are reported (12,674 against 133,922 rows for three chained node hashes).


## A.4 Publish and subscribe model and delivery (MPE-PUB) {#a4-pub}

**MPE-PUB-001** Stream identifiers sealed. *Same obligation as MPE-FMT-003, which owns it.*

**MPE-PUB-002** Shard derivation. *(POC, MUST, open: DEC-PUB-1)*  
The MPE client library shall set an MPE Envelope's Shard to a domain-separated SHA-256 hash of the audience key reduced modulo P-PUB-1 as read from the Bus Registry.  
*Verification.* test, vectors for 1,000 keys at P-PUB-1 of 1 and 8 match a reference implementation.

**MPE-PUB-003** Bus Node shard-count transition. *(PROD, MUST, settled)*  
When the Bus Registry changes P-PUB-1, the Bus Node shall accept MPE Envelopes placed under either the previous or the new value until `L_max` plus P-PUB-8 has elapsed after the change takes effect.  
*Verification.* simulation. Change from 1 to 8 Shards under load. No Envelope is rejected for a shard mismatch during the transition.

**MPE-PUB-004** Client shard-count transition. *(PROD, MUST, settled)*  
When the Bus Registry changes P-PUB-1, the MPE client library shall follow each audience key's Shards under both the previous and the new value until `L_max` plus P-PUB-8 has elapsed after the change takes effect.  
*Verification.* simulation. No Message is lost across a change from 1 to 8 Shards.

**MPE-PUB-005** Per-Envelope Recognition Tag. *Same obligation as MPE-CRY-013, which owns it.*

**MPE-PUB-006** Random private audience keys. *Same obligation as MPE-CRY-008, which owns it.*

**MPE-PUB-007** Public stream key. *(POC, SHOULD, settled)*  
Where a stream is public, the MPE client library shall derive its audience key as a domain-separated hash of the published stream name.  
*Verification.* test. Known-answer vectors. Public and private Envelopes cannot be told apart by any header field.

**MPE-PUB-008** Invitation-only private membership. *(POC, MUST, open: DEC-PUB-3)*  
The MPE client library shall add a private stream to a Subscriber only by importing an invitation received outside the bus.  
*Verification.* inspection. The API exposes no other way in. Test: an Envelope sent under an unregistered recipient key is never surfaced.

**MPE-PUB-009** No subscriber directory. *(POC, MUST, settled)*  
MPE shall provide no Bus Node, Store Node or Bus Registry operation that returns which Subscribers follow a stream, Recognition Tag or audience key.  
*Verification.* inspection of the protocol identifiers and Bus Registry entry points.  
*Note.* This excludes, by design, the indexer-side relevance model that MPS-0005 plans for private events: per-wallet relevance tables and wallet-session decryption at the Indexer.

**MPE-PUB-010** Local recognition. *(POC, MUST, settled)*  
The MPE client library shall not send any audience key, recognition key or Recognition Tag filter to a Bus Node, Store Node or Indexer.  
*Verification.* test. Capture all client egress for 24 h. No key or Recognition Tag filter material appears.  
*Note.* This excludes, by design, the per-wallet relevance and session-decryption model that MPS-0005 plans for the Indexer.

**MPE-PUB-011** Full-Shard reception. *(POC, MUST, settled)*  
While in the default reception mode, the MPE client library shall retrieve every unexpired MPE Envelope of each Shard it follows.  
*Verification.* simulation. The count received equals the Shard's publication count minus expired Envelopes.

**MPE-PUB-012** Network behaviour independent of recognition. *(POC, MUST, settled)*  
The MPE client library shall send network messages whose content, size and timing do not depend on which MPE Envelopes match the Subscriber's keys.  
*Verification.* test. Two clients follow the same Shards for 1 h with 0 and 256 keys. Their request counts and sizes are identical, and a KS test at α = 0.01 does not distinguish their timing.

**MPE-PUB-013** Fixed pull cadence. *(POC, SHOULD, open: DEC-PUB-4)*  
While retrieving a Shard by pull, the MPE client library shall request new MPE Envelopes every P-PUB-2 seconds.  
*Verification.* test. The standard deviation of inter-request intervals over 1 h is at most 50 ms.

**MPE-PUB-014** Second-source reconciliation. *(POC, MUST, open: DEC-PUB-4)*  
While following a Shard, the MPE client library shall reconcile its received MPE Envelope Identifiers against a second source run by a different Bus Operator every P-PUB-3.  
*Verification.* simulation, one source drops 5% of Envelopes; the client obtains every dropped Envelope the second source holds within 2 x P-PUB-3.

**MPE-PUB-015** Repair every differing window. *(POC, MUST, open: DEC-PUB-4)*  
When reconciliation finds that a Shard window differs from a second source, the MPE client library shall retrieve that complete window, independently of recognition.  
*Verification.* test, every differing window is fetched in full whatever the key set; request captures contain no per-identifier selection of recognized or missing Messages.

**MPE-PUB-016** Reduced-privacy mode opt-in. *(PROD, MUST, open: DEC-PUB-5)*  
Where a reduced-privacy retrieval mode is present, the MPE client library shall enable it only after an explicit opt-in by the application for each subscription.  
*Verification.* inspection and test. The default configuration never sends a selector. Opting in for one subscription does not change any other subscription.

**MPE-PUB-017** Report disclosed Shards. *(POC, SHOULD, settled)*  
The MPE client library shall report, for each subscription, the Shard identifiers it has announced to connected peers.  
*Verification.* test. The reported set equals the GossipSub topic IDs found in captured `SubOpts`.

**MPE-PUB-018** Recognition key cap. *Same obligation as MPE-CRY-016, which owns it.*

**MPE-PUB-019** Per-publisher sequence number. *(POC, MUST, settled)*  
The MPE client library shall seal in each Message a sequence number one greater than the same publisher's previous Message on the same stream.  
*Verification.* test. 1,000 Messages produce sealed sequence numbers n…n+999.

**MPE-PUB-020** Logical message identifier. *Same obligation as MPE-FMT-022, which owns it.*

**MPE-PUB-021** Oversize refusal. *Same obligation as MPE-FMT-015, which owns it.*

**MPE-PUB-022** Acceptance before success. *(POC, MUST, settled)*  
When the MPE client library submits an MPE Envelope, the MPE client library shall report it `accepted` only after the ingress Bus Node's `Accepted` reply (MPE-NET-049) names that MPE Envelope Identifier.  
*Verification.* test. Against a Bus Node that drops input silently, and against one that answers `PublishFailed{eid}`, the client never reports `accepted`; inspection, `accepted` is documented as ingress application acceptance and queueing, not mesh receipt, storage or finality.

**MPE-PUB-023** Identical retransmission. *(POC, MUST, settled)*  
While an MPE Envelope is unexpired, if no acceptance arrives within P-PUB-5 seconds, then the MPE client library shall resubmit the identical MPE Envelope bytes to a different Bus Node, up to P-PUB-6 Bus Nodes in total.  
*Verification.* test. With the first Bus Node blackholed, the second receives byte-identical bytes, and retransmission stops at expiry.

**MPE-PUB-024** Publication failure. *(POC, MUST, settled)*  
If all P-PUB-6 attempts end without acceptance, then the MPE client library shall report the publication as failed with the error `NotAccepted`.  
*Verification.* test. With all Bus Nodes blackholed, the result is `NotAccepted` after P-PUB-6 × P-PUB-5 seconds.

**MPE-PUB-025** Closed error set. *(POC, MUST, settled)*  
The MPE client library shall return every publish and subscribe failure as one member of a closed, versioned, typed error set.  
*Verification.* inspection of the API. Fault injection maps each of 20 injected faults to exactly one documented error.

**MPE-PUB-026** GossipSub message identifier. *Same obligation as MPE-NET-010, which owns it.*

**MPE-PUB-027** Seen-set until expiry. *(POC, MUST, settled)*  
The Bus Node shall keep each accepted MPE Envelope Identifier in its application seen-set until that MPE Envelope's expiry plus P-FMT-4.  
*Verification.* test, replays at 61 s and at expiry - 1 s are not forwarded.

**MPE-PUB-028** Duplicate is Ignore. *(POC, MUST, settled)*  
When the Bus Node receives an MPE Envelope whose identifier is in its seen-set, the Bus Node shall return the GossipSub validation result Ignore.  
*Verification.* test. The forwarding peer's score is unchanged after 100 duplicates.

**MPE-PUB-029** Expired on arrival is Ignore. *Same obligation as MPE-FMT-030, which owns it.*

**MPE-PUB-030** Back-fill selectors. *(POC, MUST, open: DEC-PUB-5)*  
The Store Node shall select back-fill responses only by Shard, time window and continuation cursor.  
*Verification.* inspection of the back-fill request format. It has no Recognition Tag, stream or identifier-list field.

**MPE-PUB-031** Back-fill completeness. *(POC, MUST, settled)*  
When the Store Node answers a back-fill request, the Store Node shall return every MPE Envelope it holds for the requested Shard and window, in pages of at most P-PUB-9 MPE Envelopes, each page ending with a continuation cursor.  
*Verification.* test. A store holding N Envelopes in the window returns exactly N distinct identifiers across all pages.

**MPE-PUB-032** Refusal is distinguishable. *(POC, MUST, settled)*  
If the Store Node does not serve a back-fill request in full, then the Store Node shall return a typed refusal distinct from an empty result.  
*Verification.* test. A store over its rate limit returns `Refused`, never an empty page.

**MPE-PUB-033** Pull capacity. *Same obligation as MPE-PRF-022, which owns it.*

**MPE-PUB-034** Busy fail-over. *(POC, MUST, settled)*  
When a Bus Node refuses a pull as `Busy`, the MPE client library shall request the pull from another Bus Node in the Bus Registry relay list.  
*Verification.* test. The client is receiving from a second Bus Node within 2 × P-PUB-2.

**MPE-PUB-035** At-least-once delivery. *(POC, MUST, settled)*  
While an unexpired MPE Envelope is retained by at least one configured source that answers the Subscriber's requests, MPE shall deliver that MPE Envelope to the Subscriber's client library at least once.  
*Verification.* simulation, 16 Bus Nodes, 20% churn, 1,000 Envelopes, one answering source per interval; every Envelope reaches every Subscriber.

**MPE-PUB-036** Envelope deduplication. *(POC, MUST, settled)*  
The MPE client library shall pass each MPE Envelope identifier to the application at most once per subscription store.  
*Verification.* test. Each Envelope is injected three times across the three paths, and the application sees it once.

**MPE-PUB-037** Logical deduplication. *(POC, MUST, settled)*  
The MPE client library shall pass each authenticated pair of publisher and logical message identifier to the application at most once per subscription store.  
*Verification.* test. Two Envelopes carrying one logical identifier produce one delivery.

**MPE-PUB-038** Arrival-order delivery. *(POC, MUST, open: DEC-PUB-6)*  
The MPE client library shall deliver Messages in the order it authenticates them, holding no Message back to restore sequence order.  
*Verification.* test. Messages with sequence numbers 3 then 2 are delivered as 3, then 2 marked `late`.

**MPE-PUB-039** Gap report. *(POC, MUST, settled)*  
If a missing sequence number has not arrived P-PUB-7 seconds after a later number from the same publisher and stream, then the MPE client library shall emit a `gap` item naming the publisher and the missing range.  
*Verification.* test. Withholding sequence number 5 produces `gap{5..5}` at P-PUB-7 ± 1 s.

**MPE-PUB-040** Late fill. *(POC, MUST, settled)*  
When a Message arrives whose sequence number lies inside an open gap, the MPE client library shall deliver it as a `late` item.  
*Verification.* test. Releasing the withheld Message yields `late` with sequence number 5.

**MPE-PUB-041** Gap becomes lost. *(POC, MUST, settled)*  
If a gap is still open `L_max` plus P-PUB-8 after it was emitted, then the MPE client library shall mark that gap `lost`.  
*Verification.* test. A `lost` item is emitted at `L_max` + P-PUB-8 ± 1 s.

**MPE-PUB-042** Caught-up marker. *(POC, MUST, settled)*  
When back-fill reaches the newest MPE Envelope the serving Store Node holds, the MPE client library shall emit a `head` item carrying the current cursor.  
*Verification.* test. Exactly one `head` per back-fill, emitted after the last stored Envelope.

**MPE-PUB-043** Portable inclusive cursor. *(POC, MUST, settled)*  
The MPE client library shall resume a subscription from an inclusive cursor defined only by MPE Envelope header fields and wall-clock time, never by a row number or Indexer event `id` local to one source.  
*Verification.* test. Switching mid-back-fill between two Store Nodes with different ingest orders skips no Envelope; on the ledger lane, a resume against a second Indexer, with `id` values translated by the Ledger Adapter (MPE-CON-053), skips no Envelope.

**MPE-PUB-044** Atomic processing helper. *Same obligation as MPE-CON-033, which owns it.*

**MPE-PUB-045** Retention exceeded. *(POC, MUST, settled)*  
If a subscription resumes from a cursor older than the earliest MPE Envelope any reachable Store Node holds, then the MPE client library shall emit a `gap` item with reason `retention-exceeded` for the unreachable interval.  
*Verification.* test. A client offline for longer than retention receives this `gap` before any Message.

**MPE-PUB-046** Key erased. *(PROD, MUST, settled)*  
If a back-fill interval predates the oldest recognition key the Subscriber retains for a stream, then the MPE client library shall emit a `gap` item with reason `key-erased` for that stream and interval.  
*Verification.* test. After erasing the keys of key period 1, back-filling period 1 yields `key-erased`.

**MPE-PUB-047** Reactions only on explicit call. *(POC, MUST, settled)*  
The MPE client library shall submit a transaction or publication that reacts to a Message only when the application explicitly calls a reaction operation.  
*Verification.* inspection. No code path in the library sends a reaction except a reaction call.

**MPE-PUB-048** External object fetch. *Same obligation as MPE-FMT-038, which owns it.*

**MPE-PUB-049** Unknown schema. *(POC, MUST, settled)*  
If an authenticated Message carries a schema identifier the application has not registered, then the MPE client library shall deliver it as an `undecodable` item.  
*Verification.* test. A Message with an unregistered schema arrives as `undecodable` with its sequence number.

**MPE-PUB-050** Disconnected status. *(POC, MUST, settled)*  
If the MPE client library has received no response from any Bus Node or Store Node for P-PUB-11 seconds, then the MPE client library shall emit a `disconnected` status item.  
*Verification.* test. Partitioning the client yields `disconnected` at P-PUB-11 ± 1 s.

**MPE-PUB-051** Validation before forwarding. *Same obligation as MPE-NET-015, which owns it.*

**MPE-PUB-052** Subscriber bandwidth measurement. *Same obligation as MPE-PRF-021, which owns it.*

**MPE-PUB-053** Retransmission stops at admission window end. *(POC, MUST, settled)*  
If an unaccepted MPE Envelope's admission window ended more than P-ECO-6 earlier, then the MPE client library shall stop retransmitting it and report `NotAccepted`.  
*Verification.* test, with all Bus Nodes blackholed across an admission window boundary, retries stop P-ECO-6 after the admission window ends.


## A.5 Consumers: agents, contracts and wallets (MPE-CON) {#a5-con}

**MPE-CON-001** Local recognition. *Same obligation as MPE-PUB-010, which owns it.*

**MPE-CON-002** Whole-Shard retrieval by default. *Same obligation as MPE-PUB-011, which owns it.*

**MPE-CON-003** Recognition-independent requests. *Same obligation as MPE-PUB-012, which owns it.*

**MPE-CON-004** Opt-in for selective profiles. *Same obligation as MPE-PUB-016, which owns it.*

**MPE-CON-005a** Typed degraded outcome. *(POC, MUST, settled)*  
If the active reception mode cannot be sustained, then the MPE client library shall return the typed `Degraded` outcome to the subscription.  
*Verification.* test, make every source unreachable and assert one `Degraded` outcome.

**MPE-CON-005b** Reception mode unchanged after degradation. *(POC, MUST, settled)*  
If the active reception mode cannot be sustained, then the MPE client library shall keep the reception mode unchanged until the application selects another profile.  
*Verification.* test, after `Degraded`, capture requests and confirm no selector or filtered request precedes an explicit profile selection.

**MPE-CON-006** Keys only by invitation. *Same obligation as MPE-PUB-008, which owns it.*

**MPE-CON-007** Recognition Tag lookahead window. *Withdrawn: DEC-003 (salted per-Envelope Recognition Tags replace the earlier tag rule).*

**MPE-CON-008** Recognition-window gap. *Withdrawn: DEC-003 (salted per-Envelope Recognition Tags replace the earlier tag rule).*

**MPE-CON-009** Recognition key cap. *Same obligation as MPE-CRY-016, which owns it.*

**MPE-CON-010** Generated codecs only. *Same obligation as MPE-FMT-027, which owns it.*

**MPE-CON-011** Undecodable Messages delivered. *Same obligation as MPE-PUB-049, which owns it.*

**MPE-CON-012** At-least-once within retention. *Same obligation as MPE-PUB-035, which owns it.*

**MPE-CON-013** Deduplication by Envelope identifier. *Same obligation as MPE-PUB-036, which owns it.*

**MPE-CON-014** Logical deduplication of retries. *Same obligation as MPE-PUB-037, which owns it.*

**MPE-CON-015** Finality label on every Message. *(POC, MUST, settled)*  
The MPE client library shall label every delivered Message with exactly one finality label, `gossip` or `final`.  
*Verification.* test, every delivered item has exactly one finality label.

**MPE-CON-016** Meaning of `final`. *(POC, MUST, settled)*  
The MPE client library shall label a Message `final` only after verifying its MPE Envelope Identifier under an Anchor in Bus Registry state at a finalized block, or its ledger-lane parts against finalized on-chain data confirmed by P-NET-14 independent sources or by block replay.  
*Verification.* test with the mock Ledger Adapter: a forged inclusion path, an unfinalized Anchor, an Anchor present only as a `Misc` notification and ledger-lane parts reported by one source only each leave the label at `gossip`.

**MPE-CON-017** Upgrade notice from gossip to final. *(POC, MUST, settled)*  
When a Message already delivered as `gossip` becomes covered by a verified finalised Anchor, and for a carried event `MPE-CON-058` and `MPE-CON-059` are also satisfied, the MPE client library shall emit a `finalised{eid}` notice.  
*Verification.* test. Publish, observe `gossip`, anchor, and assert one `finalised` notice; an anchored carried event whose transaction is unfinalized, whose fallible segment failed or whose transcript holds different bytes gets no notice.

**MPE-CON-018** Unanchored notice. *(POC, MUST, settled)*  
If a Message delivered as `gossip` is not covered by a verified finalised Anchor within P-CON-8, then the MPE client library shall emit an `unanchored{eid}` notice.  
*Verification.* test. Suppress the anchorer and assert the notice after P-CON-8.

**MPE-CON-019** One interface for both labels. *(POC, SHOULD, settled)*  
The MPE client library shall deliver `gossip`-labelled and `final`-labelled Messages through the same subscription call and the same item type.  
*Verification.* inspection of the API, plus a test that runs the same consumer against the overlay and against the ledger lane.

**MPE-CON-020** Suspected gap. *Same obligation as MPE-PUB-039, which owns it.*

**MPE-CON-021** Late fill. *Same obligation as MPE-PUB-040, which owns it.*

**MPE-CON-022** No hidden reordering. *Same obligation as MPE-PUB-038, which owns it.*

**MPE-CON-023** Bounded gap state. *(POC, MUST, settled)*  
If a publisher's pending-gap state would exceed P-CON-9 sequence numbers, then the MPE client library shall emit `gap{reason:"overflow"}` and discard the oldest pending range.  
*Verification.* test. Inject a sequence jump of 10 × P-CON-9 and assert bounded memory plus the overflow item.

**MPE-CON-024** Caught-up marker. *Same obligation as MPE-PUB-042, which owns it.*

**MPE-CON-025a** Typed source failure. *(POC, MUST, settled)*  
If a source connection fails, then the MPE client library shall return the typed `SourceFailed` outcome to the subscription.  
*Verification.* test, kill the source mid-stream and assert one `SourceFailed` outcome.

**MPE-CON-025b** No completion on source failure. *(POC, MUST, settled)*  
If a source connection fails, then the MPE client library shall keep the subscription open instead of ending it as complete.  
*Verification.* test, kill the source mid-stream and assert the subscription never emits completion.

**MPE-CON-026** Closed publish result set. *(POC, MUST, settled)*  
When a publish call returns, the MPE client library shall report exactly one of `accepted` (the ingress Bus Node completed application acceptance), `final`, or `failed{reason}` from a closed reason set.  
*Verification.* test of each failure cause, asserting the matching reason; inspection, `accepted` is not described as remote receipt, storage or finality.

**MPE-CON-027** Portable cursor. *Same obligation as MPE-PUB-043, which owns it.*

**MPE-CON-028** Inclusive resume. *(POC, MUST, settled)*  
When the application subscribes from a committed cursor, the MPE client library shall deliver every retained recognised Message at or after that cursor that is absent from the committed deduplication state.  
*Verification.* test. Crash at random points and assert that the union of deliveries equals the set of published Messages.

**MPE-CON-029** Back-fill by complete window. *Same obligation as MPE-STO-017, which owns it.*

**MPE-CON-030** Back-fill window reported. *(POC, SHOULD, settled)*  
The MPE client library shall report, through a capabilities call, the back-fill window as the minimum of source retention and local key retention.  
*Verification.* test. Set retention to 48 h and key retention to 24 h, and assert a reported window of 24 h.

**MPE-CON-031** Key-erased gap. *Same obligation as MPE-PUB-046, which owns it.*

**MPE-CON-032** Retention gap. *Same obligation as MPE-PUB-045, which owns it.*

**MPE-CON-033** Atomic processOnce. *(POC, MUST, settled)*  
The MPE client library shall provide a `processOnce` call that commits the application effect, the cursor and the deduplication state in one atomic write to an application-supplied store.  
*Verification.* test. Kill the process between effect and commit and assert one effect after restart.

**MPE-CON-034** Chaos acceptance. *Same obligation as MPE-VER-023, which owns it.*

**MPE-CON-035** Delivery model check. *Same obligation as MPE-VER-008, which owns it.*

**MPE-CON-036** Independent sources by default. *(PROD, SHOULD, open: DEC-CON-5)*  
The MPE client library shall, by default, retrieve each subscribed Shard from at least P-CON-3 sources run by different Bus Operators.  
*Verification.* test. With default configuration, assert connections to P-CON-3 distinct Bus Operators per Shard.

**MPE-CON-037** Inventory repair. *Same obligation as MPE-PUB-014, which owns it.*

**MPE-CON-038** Anchor count check. *(PROD, SHOULD, settled)*  
When a verified finalised Anchor covers a subscribed Shard window, the MPE client library shall emit `incomplete{window}` if its inventory for that window lacks any anchored MPE Envelope identifier.  
*Verification.* test. Withhold one anchored Envelope from all sources and assert the item.

**MPE-CON-039** No automatic network action. *(POC, MUST, settled)*  
The MPE client library shall send no network message, acknowledgement or transaction as a consequence of recognising a Message.  
*Verification.* test. Compare egress with and without matching keys; it must be identical.

**MPE-CON-040** Reaction delay. *(PROD, SHOULD, open: DEC-CON-7)*  
Where the application submits a reaction through the library's reaction helper, the MPE client library shall delay submission by a uniformly random interval in [0, P-CON-11].  
*Verification.* test. Over 1,000 reactions, the delays fit uniform [0, P-CON-11] (KS test, p > 0.01).

**MPE-CON-041** Off-chain blob fetch is explicit. *Same obligation as MPE-FMT-038, which owns it.*

**MPE-CON-042** Contract reaction by later transaction. *(PROD, MUST, settled)*  
The MPE client library shall provide a reaction builder that produces a Midnight transaction calling a target contract circuit, with the Message supplied as private witness data.  
*Verification.* demonstration on a local ledger-9 network, or test against the mock Ledger Adapter.

**MPE-CON-043** Publisher authorisation in circuit. *(PROD, MUST, open: DEC-022)*  
The MPE client library's consumption circuit shall assert a publisher signature, under the suite's signature algorithm, over genesis, target contract, action, logical identifier, expiry and payload digest, against a publisher set committed in the target contract's state, and recompute that payload digest from the payload bytes from which it derives every effect input.  
*Verification.* test. Wrong key, wrong target, wrong action, wrong genesis, and a valid signature with a changed amount, recipient or other consumed field each fail proof generation, under Ed25519 and, where enabled, JubJub Schnorr; analysis reports rows, proving time and prover-key size of both.

**MPE-CON-044a** Replayed consumption rejected. *(PROD, MUST, settled)*  
If a reaction's consumption nullifier is already in the target contract's consumption nullifier set, then the MPE client library's consumption circuit shall reject the reaction.  
*Verification.* test, submit the same reaction twice and assert the second transaction fails.

**MPE-CON-044b** Atomic consumption nullifier insertion. *(PROD, MUST, settled)*  
The MPE client library's consumption circuit shall insert the consumption nullifier in the same transaction as the contract effect it authorizes.  
*Verification.* test, inject failure in the fallible segment and confirm neither the effect nor the consumption nullifier is committed.

**MPE-CON-045** Secret-derived consumption nullifier. *Same obligation as MPE-CRY-025, which owns it.*

**MPE-CON-046** Expiry enforced. *(PROD, MUST, settled)*  
The MPE client library's consumption circuit shall reject a Message whose expiry, taken from its signed expiry or from its anchored creation minute plus P-FMT-3, is earlier than the block time of the reacting transaction.  
*Verification.* test. React after expiry under both expiry sources and assert the rejection.

**MPE-CON-047** Optional publication proof. *(PROD, MAY, open: DEC-CON-3)*  
Where an application requires proof of publication before a time, the MPE client library's consumption circuit shall verify that the MPE Envelope Identifier is included under a window root whose Anchor-tree leaf passes the Bus Registry's witness-free historic-root check.  
*Verification.* test on a local ledger-9 network: the Anchor tree is a `HistoricMerkleTree<12>` with leaf `SHA-256(domain, window, window root)` at slot `window mod 2940`; a forged path fails, a stale accepted root passes, and the reaction carries two contract calls.

**MPE-CON-048** No infrastructure output as authority. *(PROD, MUST, settled)*  
The MPE client library shall offer no contract-consumption API that accepts output from a Bus Node, Store Node or Indexer as evidence of publisher authorisation.  
*Verification.* inspection of the API surface.

**MPE-CON-049** Reactor race test. *Same obligation as MPE-VER-032, which owns it.*

**MPE-CON-050** Ledger paused. *(POC, MUST, settled)*  
If the Ledger Adapter reports that Midnight rejects user transactions, then the MPE client library shall return a typed `LedgerPaused` error to reaction and ledger-lane publish calls.  
*Verification.* test. Set the mock adapter to paused and assert the error.

**MPE-CON-051** Gossip continues while ledger unavailable. *(POC, MUST, settled)*  
While the Ledger Adapter reports Midnight unavailable, the MPE client library shall continue delivering recognised Messages labelled `gossip`.  
*Verification.* test. Pause the mock ledger and assert continued `gossip` delivery with no `final` labels.

**MPE-CON-052** Wallet grants. *(PROD, SHOULD, open: DEC-CON-6)*  
Where a wallet hosts the MPE client library, the client library shall release a stream's Messages to a DApp only under a grant for that stream issued by the wallet user.  
*Verification.* test. A DApp without a grant receives nothing; a DApp with a grant receives only that stream.

**MPE-CON-053** Ledger lane read. *(POC, MUST, settled)*  
While the ledger lane is active, the MPE client library shall read ledger-lane MPE Envelopes through the Indexer adapter, filtering by the bus contract address only and resuming from the Indexer's monotonic event `id` as translated by the Ledger Adapter.  
*Verification.* test. Inspect Indexer adapter queries; only the address and the `MISC` type appear, and the stored resume point maps to the MPE-PUB-043 cursor.

**MPE-CON-054** Consumer bandwidth metering. *(POC, SHOULD, settled)*  
The MPE client library shall report to the application the bytes received per subscribed Shard per UTC day.  
*Verification.* test. The reported count matches captured traffic within 1%.

**MPE-CON-055** Afternoon test. *Same obligation as MPE-VER-036, which owns it.*

**MPE-CON-056** Closed outcome set. *(POC, MUST, settled)*  
The MPE client library shall report every refusal or failure as one of TooLarge, NotReady, NotAccepted, Busy, Refused, ResourceExhausted, StorageExhausted, KeyLimit, Degraded, SourceFailed, Unresolved, RetentionGap, KeyGap, CorruptRecord, LedgerUnavailable, LedgerPaused, BusPaused, InsufficientDust or SessionUpdateRequired.  
*Verification.* inspection of the API; fault injection maps each injected fault to exactly one outcome.

**MPE-CON-057** Carrier attribute. *(POC, MUST, settled)*  
The MPE client library shall mark every delivered Message with exactly one carrier attribute: `overlay`, `gateway` or `ledger`.  
*Verification.* test, deliver one Message over each carrier and check its attribute.

**MPE-CON-058** Carried event unconfirmed until matched. *(PROD, MUST, settled)*  
The MPE client library shall label a carried event `gossip` until the recording transaction is finalized and its transcript holds the carried bytes at the stated position.  
*Verification.* test with the mock Ledger Adapter: a carried event whose bytes differ from the finalized transcript, or whose transaction is not finalized, stays `gossip`.

**MPE-CON-059** Carried event from a failed fallible phase. *(PROD, MUST, settled)*  
If a carried event was emitted in a fallible segment that did not succeed, then the MPE client library shall never label that carried event `final`.  
*Verification.* test on a ledger-9 devnet: a transaction whose fallible segment fails yields a carried event that never becomes `final`.

**MPE-CON-060** Anchor inclusion bound to the Message. *(PROD, MUST, open: DEC-022)*  
Where the consumption circuit uses Anchor inclusion to prove publication, it shall prove that the anchored MPE Envelope Identifier commits to a Sealed Body that opens to the signed publisher statement the circuit verifies.  
*Verification.* test: a valid signed statement for one Message combined with a valid inclusion path for another Envelope, and a holder of a valid inclusion path who supplies a different Message secret or no publisher signature, each fail to produce an accepted reaction.

**MPE-CON-061** Coarse expiry disclosure. *(PROD, MUST, settled)*  
The MPE client library's consumption circuit shall disclose, for its expiry check, only a coarse upper time bound chosen by the prover, never the signed expiry.  
*Verification.* inspection of the public transcript of a reaction: the only time value is the prover-chosen bound, because every block-time comparison discloses its operand.

**MPE-CON-062** Deferred `in-block` label. *(PROD, MAY, open)*  
Where a best-chain Indexer view is enabled, the MPE client library shall label a Message `in-block` while its Anchor or ledger-lane parts sit only in blocks that are not finalized.  
*Verification.* test with a mock best-chain view: a Message anchored in an unfinalized block is labelled `in-block`, never `final`.

**MPE-CON-063** Rollback of `in-block`. *(PROD, MAY, open)*  
If a reorganization removes the block behind an `in-block` label, then the MPE client library shall withdraw that label and emit a `rolled-back{eid}` notice.  
*Verification.* test with a mock reorganization: the label is withdrawn and exactly one notice is emitted.


## A.6 Admission, economics and spam cost (MPE-ECO) {#a6-eco}

**MPE-ECO-001** No proof-of-work admission. *(POC, MUST, settled)*  
The Bus Node shall not use proof-of-work as an admission criterion for an MPE Envelope.  
*Verification.* inspection of the Bus Node validator code path; a test that an Envelope with no work field is accepted when all other checks pass.

**MPE-ECO-002** DUST is not Bus Operator payment. *(POC, MUST, settled)*  
MPE shall not require any party to transfer DUST to a Bus Operator.  
*Verification.* inspection of the client library and Bus Node payment interfaces; no DUST-transfer call exists.

**MPE-ECO-003** No Midnight transaction per overlay Message. *Same obligation as MPE-NET-002, which owns it.*

**MPE-ECO-004** Membership registration. *(PROD, MUST, open: DEC-ECO-1)*  
When the Bus Registry receives a registration transaction carrying a membership commitment, the Bus Registry shall insert that commitment into the membership tree of the current membership period.  
*Verification.* test on a ledger-9 devnet: register, then confirm that the next root contains the leaf; inspection: the only price is the network fee of the registration transaction unless MPE-ECO-056 adds a token price, since a contract cannot receive or observe DUST.

**MPE-ECO-005** Sponsored registration. *(PROD, SHOULD, settled)*  
The Bus Registry shall accept a membership commitment from any caller that pays the registration fee, without requiring that caller to know the admission secret.  
*Verification.* test: a sponsor registers a commitment generated by a separate client, and that client then publishes successfully.

**MPE-ECO-006** Dedicated admission secret. *(POC, MUST, settled)*  
The MPE client library shall generate the admission secret independently of every wallet spending, encryption, signing and session key, either from the operating-system generator or through the `deriveSecret` derivation of MPE-CRY-027.  
*Verification.* inspection of key derivation; a test that the admission secret has no derivation path from any spending, encryption, signing or session key.

**MPE-ECO-007** Shielded fee payment. *(PROD, MUST, settled)*  
The MPE client library shall pay Bus Registry registration fees from shielded DUST without attaching unshielded inputs or outputs to that transaction.  
*Verification.* inspection of three devnet registration transactions built by the client: no unshielded offer is present.

**MPE-ECO-008** Live fee quotes. *(PROD, MUST, settled)*  
When the MPE client library quotes the DUST cost of a Bus Registry transaction, it shall compute the quote from the `ledgerParameters` of the latest finalized block.  
*Verification.* test with a mocked block whose parameters double the price: the quote doubles.

**MPE-ECO-009** Insufficient DUST reported before proving. *(PROD, SHOULD, settled)*  
If the available DUST is less than the quoted fee, then the MPE client library shall return an insufficient-DUST error before generating any proof.  
*Verification.* test with a balance below the quote: the error is returned and the prover is never called.

**MPE-ECO-010** Client back-off under chain congestion. *(PROD, SHOULD, settled)*  
While the last finalized block's `blockUsage` fullness exceeds P-ECO-9, the MPE client library shall defer membership renewals that are not due within the current membership period.  
*Verification.* test with a mocked block fullness of 60%: renewals due in the next period are not submitted until fullness drops.

**MPE-ECO-011** Chain-share budget. *(PROD, SHOULD, open: DEC-ECO-6)*  
MPE shall consume no more than P-ECO-8 of either the `block_usage` or the `bytes_written` block limit, averaged over 24 h, for Bus Registry registrations, Anchors and ledger-lane parts combined.  
*Verification.* analysis of 7 days of testnet blocks: sum the block bytes and the `bytes_written` of MPE transactions, including ledger-lane parts, and divide each sum by its limit (`bytes_written` is 50,000 B per block).

**MPE-ECO-012** Admission Proof required. *(POC, MUST, settled)*  
If an MPE Envelope lacks an Admission Proof, or its Admission Proof fails verification, then the Bus Node shall return GossipSub `Reject` for that MPE Envelope.  
*Verification.* test: inject a mutated proof; the receiver reports `Reject` and the sender's P₄ counter increases.

**MPE-ECO-013** Cheap checks before proof verification. *(POC, MUST, settled)*  
The Bus Node shall complete the length, admission window, root-window and admission-nullifier duplicate checks on an MPE Envelope before verifying its Admission Proof.  
*Verification.* test with instrumentation: an Envelope with a stale admission window never reaches the verifier.

**MPE-ECO-014** Admission window freshness. *(POC, MUST, settled)*  
If an MPE Envelope's admission window differs from the Bus Node's current admission window by more than P-ECO-6 beyond the admission window boundary, then the Bus Node shall return GossipSub `Ignore` for that MPE Envelope.  
*Verification.* test at offsets of P-ECO-6 − 1 s (accepted) and P-ECO-6 + 1 s (Ignore, no P₄ change).

**MPE-ECO-015** Root window from supersession. *(POC, MUST, settled)*  
If an MPE Envelope's Admission Proof references a membership root that is neither the current root nor superseded less than P-ECO-5 earlier, then the Bus Node shall return Ignore for that MPE Envelope.  
*Verification.* test, with no root update for 2 h the current root still validates; a root superseded P-ECO-5 + 1 s earlier yields Ignore; inspection: the Bus Registry's historic-root check has no time bound, so this Bus Node check alone enforces P-ECO-5.

**MPE-ECO-016** Committed per-class rate limit. *(POC, MUST, open: DEC-ECO-4)*  
The Bus Node shall return Reject for an MPE Envelope of size class c unless its Admission Proof shows a credit index below the class-c per-admission-window limit committed in the membership leaf.  
*Verification.* test, with class-2 limit 4, credit indices 0-3 are accepted and index 4 is Rejected.

**MPE-ECO-017** Class-bound admission nullifier. *(POC, MUST, open: DEC-ECO-4)*  
The MPE client library shall derive each admission nullifier from the admission secret, the Network Identifier, the Bus Registry contract address, the admission window number, the size class and the credit index under the domain-separated hash of the admission proof profile.  
*Verification.* test vectors; two Envelopes of different classes with equal index yield different admission nullifiers, and the same secret, window, class and index under another Network Identifier or another Bus Registry yield a different slope and admission nullifier.

**MPE-ECO-018** Content-bound Admission Proof. *(POC, MUST, settled)*  
The Admission Proof shall bind its rate-limit share to the MPE Envelope identifier, so that two MPE Envelopes with different identifiers under one admission nullifier yield two distinct shares.  
*Verification.* test: produce two Envelopes under one admission nullifier and recover the admission secret from their shares.

**MPE-ECO-019** Duplicate admission nullifier, same Envelope. *Same obligation as MPE-PUB-028, which owns it.*

**MPE-ECO-020** Equivocation recorded without penalty. *(POC, MUST, open: DEC-SEC-4)*  
If an MPE Envelope carries an admission nullifier already accepted with a different MPE Envelope Identifier, then the Bus Node shall return Ignore and record both MPE Envelopes as equivocation evidence.  
*Verification.* test, send two conflicting Envelopes from two peers; no P4 change and the evidence store holds both.

**MPE-ECO-021** Admission nullifier retention. *(POC, MUST, settled)*  
The Bus Node shall retain each accepted admission nullifier for at least P-ECO-7 after acceptance.  
*Verification.* test: restart a Bus Node in the middle of an admission window, then replay a conflicting Envelope; the result is Ignore with the evidence retained, never Accept.

**MPE-ECO-022** Per-Bus-Node allowance bound. *(POC, MUST, settled)*  
The Bus Node shall accept at most one MPE Envelope Identifier per live publication allowance under its local acceptance state.  
*Verification.* simulation with 16 Bus Nodes and conflicting first uses injected at separate nodes: each node accepts at most one identifier per allowance and retains the conflict evidence (MPE-ECO-020); the report states that no network-wide admission count follows from mesh connectivity alone.

**MPE-ECO-023** Per-peer pre-verification limit. *Same obligation as MPE-NET-023, which owns it.*

**MPE-ECO-024** Stale Bus Registry view. *Same obligation as MPE-NET-018, which owns it.*

**MPE-ECO-025** Continuity when Bus Registry calls are paused. *Same obligation as MPE-NET-038, which owns it.*

**MPE-ECO-026** One membership tree per period. *(PROD, MUST, open: DEC-ECO-5)*  
The Bus Registry shall hold the memberships of each membership period of P-ECO-4 in a separate membership tree.  
*Verification.* test on a devnet: after the period ends, a proof against the next period's root fails for a member registered only in the ended period.

**MPE-ECO-027** Root times from block timestamps. *(PROD, MUST, settled)*  
The Ledger Adapter shall derive each membership root's publication and supersession times from the timestamps of the finalized blocks that include the root-changing transactions.  
*Verification.* test on a devnet after 3 root updates: each root maps to the timestamp of its including block; inspection: the Bus Registry stores no publication time, because a circuit can compare block time but not read it.

**MPE-ECO-028** Revocation on evidence. *(PROD, MUST, open: DEC-ECO-2)*  
When the Bus Registry receives two shares under one admission window, class and credit index that lie on one member's line with distinct MPE Envelope Identifiers, together with that member's Merkle path, the Bus Registry shall mark the membership revoked.  
*Verification.* test: submit the two shares of a double use; the member's leaf is reset and its identity commitment enters the revoked set; inspection: the leaf index and the identity commitment become public.

**MPE-ECO-029** Revocation takes effect. *(PROD, MUST, settled)*  
When a membership is revoked, the Bus Registry shall exclude it from every membership root published after the revocation.  
*Verification.* test: after revocation plus P-ECO-5, an Envelope from the revoked member gets `Ignore` at every Bus Node.

**MPE-ECO-030** No per-Envelope ledger state. *(PROD, MUST, settled)*  
The Bus Registry shall not write any per-Envelope admission nullifier or per-Envelope identifier into ledger state.  
*Verification.* inspection of the Bus Registry contract's state declarations.

**MPE-ECO-031** Equivocation evidence retention. *(PROD, SHOULD, settled)*  
The Bus Node shall retain each recorded equivocation evidence pair for at least P-ECO-14.  
*Verification.* test: evidence remains retrievable through the Bus Node interface after P-ECO-14 − 1 s.

**MPE-ECO-032** Bond custody. *(PROD, MAY, open: DEC-ECO-2)*  
Where membership bonds are enabled, the Bus Registry shall hold each bond in NIGHT until P-ECO-14 after its holder requests withdrawal.  
*Verification.* Quint model invariant "no withdrawal before the delay"; devnet test of a withdrawal at delay − 1 block (fails) and + 1 block (succeeds).  
*Note.* Bonds in MPE-ECO-032 to MPE-ECO-042 are balances of the Bus Registry contract. They have no relation to NIGHT staking, which locks nothing and "carries no consensus weight".

**MPE-ECO-033** Slash split. *(PROD, MAY, open: DEC-ECO-2)*  
Where membership bonds are enabled, when the Bus Registry accepts slash evidence for a bonded membership, the Bus Registry shall pay at most P-ECO-15 of the bond to the reporter.  
*Verification.* test: an equivocator self-reports and recovers ≤ P-ECO-15 of the bond.

**MPE-ECO-034** Bus Registry funds invariant. *(PROD, MUST, settled)*  
Where membership bonds or a treasury are enabled, the Bus Registry shall hold NIGHT equal to outstanding bonds plus the treasury balance plus challenge escrow.  
*Verification.* Quint model check over bond, slash, withdraw, challenge and payout actions; balance comparison on devnet after each action.

**MPE-ECO-035** Maintainer cannot move bonds. *(PROD, MUST, settled)*  
The Bus Registry shall move bonded NIGHT only through its coded slash, withdraw and payout circuits.  
*Verification.* inspection of every Bus Registry circuit that calls `sendUnshielded`; a test that a maintenance-authority call cannot transfer funds.

**MPE-ECO-036** Registration publicity disclosed. *(PROD, MUST, settled)*  
Where a membership requires an unshielded NIGHT deposit, the MPE client library shall tell the user, before submission, that the funding address becomes publicly linked to a membership registration.  
*Verification.* demonstration: the registration flow shows the notice and requires confirmation.

**MPE-ECO-037** No protocol pay for relaying. *(PROD, MUST, open: DEC-ECO-3)*  
The Bus Registry shall not pay any Bus Operator for forwarding MPE Envelopes.  
*Verification.* inspection of Bus Registry payout circuits.

**MPE-ECO-038** No performance-score payouts. *(PROD, SHOULD, open: DEC-ECO-3)*  
The Bus Registry shall not base any payout on a measured relay or uptime performance score.  
*Verification.* inspection of payout circuit inputs; none is a score.

**MPE-ECO-039** Treasury runway cap. *(PROD, MUST, open: DEC-ECO-3)*  
Where a Bus Registry treasury is enabled, the Bus Registry shall pay out no more per day than the treasury balance divided by P-ECO-16.  
*Verification.* Quint invariant; devnet test that a payout above the cap fails.

**MPE-ECO-040** Per-key saturation cap. *(PROD, SHOULD, open: DEC-ECO-3)*  
Where a Bus Registry treasury is enabled, the Bus Registry shall pay any single bond key no more than the reward pool for that period divided by P-ECO-17.  
*Verification.* Quint invariant "payout per key ≤ pool ÷ k".

**MPE-ECO-041** Store Node retention challenge. *(PROD, MAY, open: DEC-ECO-3)*  
Where Store Node bonding is enabled, when the Bus Registry records a challenge for an anchored MPE Envelope inside its retention window, the Store Node shall submit that MPE Envelope and its Merkle path within P-ECO-18.  
*Verification.* devnet test: a challenge is issued and answered before the deadline.

**MPE-ECO-042** Missed challenge forfeits bond. *(PROD, MAY, open: DEC-ECO-3)*  
Where Store Node bonding is enabled, if a challenged Store Node misses the P-ECO-18 deadline, then the Bus Registry shall transfer the forfeited bond share to the challenger and the treasury.  
*Verification.* devnet test: an unanswered challenge produces the transfer after the deadline.

**MPE-ECO-043** Unlinkable paid back-fill. *(PROD, MAY, open: DEC-ECO-3)*  
Where a Store Node charges for back-fill, the Store Node shall accept payment tokens that carry no Subscriber account identifier.  
*Verification.* inspection of the redemption message format: no persistent client identifier is present.

**MPE-ECO-044** Overload refuses new Envelopes. *Same obligation as MPE-PRF-034, which owns it.*

**MPE-ECO-045** Shed the largest class first. *(PROD, SHOULD, settled)*  
While the Bus Node's ingress exceeds its configured cap, the Bus Node shall refuse MPE Envelopes of the largest size class before refusing any smaller class.  
*Verification.* simulation at 2× the cap with a mixed class load: the refusal ratio for the largest class is ≥ that of every smaller class.

**MPE-ECO-046** Cover Envelopes are admitted normally. *(PROD, MAY, open: DEC-ECO-7)*  
Where a Bus Operator emits cover MPE Envelopes, the Bus Node shall apply the same Admission Proof and credit checks to them as to any other MPE Envelope.  
*Verification.* test: a cover Envelope without credits gets `Reject`.

**MPE-ECO-047** Prototype admission over a mocked ledger. *Same obligation as MPE-NET-035, which owns it.*

**MPE-ECO-048** Admission-proof measurement gate. *(POC, MUST, settled)*  
The Prototype shall report the Admission Proof size in bytes, the encoded Admission Slot width `roundUp64(104 + proof length)` and the verification time on one core of a 4-vCPU VM, and fail its gate if the slot width exceeds P-ECO-11 or the verification time exceeds P-ECO-12.  
*Verification.* test: a benchmark harness over 10,000 proofs reports median and p99 verify time and the proof length.

**MPE-ECO-049** Registration-cost gate. *(PROD, MUST, settled)*  
MPE shall not enter production until a measured devnet registration transaction is within P-ECO-13.  
*Verification.* demonstration: submit 10 registrations on devnet and record bytes and DUST from the block's `ledgerParameters`; until then, the estimate uses the measured model inputs (proofs of at most 4,368 bytes, verifying keys of at most 2,119 bytes, simulator transcript gas), about 8.7 KB and 0.246 DUST.

**MPE-ECO-050** Flood-cost analysis published. *(PROD, SHOULD, settled)*  
MPE shall publish, before production, the NIGHT holding needed to fill one Shard at its D5 cap for 24 h, computed from the ECO-049 measurement.  
*Verification.* analysis: an independent reviewer recomputes it from the published inputs using 0.714 DUST/NIGHT/day.

**MPE-ECO-051** Stale-root bound. *(POC, MUST, settled)*  
If the membership period served by an Admission Proof's referenced root ended more than P-ECO-5 before the Bus Node's clock, then the Bus Node shall return Ignore for that MPE Envelope.  
*Verification.* test, freeze the mock adapter and confirm Envelopes under the last root are Ignored 25 h after its period began.

**MPE-ECO-052** Admission Slot field layout. *(POC, MUST, open: DEC-ECO-1)*  
The MPE client library shall fill the Admission Slot with the 8-byte admission window number, the 32-byte referenced membership root, the 32-byte admission nullifier, the 32-byte share y-coordinate and the proof, in that order.  
*Verification.* test vectors; a Bus Node rejects a stale admission window without invoking the verifier.

**MPE-ECO-053** Admission window number. *(POC, MUST, settled)*  
The MPE client library shall compute the admission window number as the Unix time in seconds divided by P-ECO-1, rounded down.  
*Verification.* test vectors at boundary times.

**MPE-ECO-054** Admission secret stays with the client. *(PROD, MUST, settled)*  
The MPE client library shall not send the admission secret, or a witness derived from it, to a prover outside the client's trust boundary unless that prover is attested.  
*Verification.* inspection of the proving path; test: configuring an unattested remote prover fails before any admission witness leaves the client.

**MPE-ECO-055** Permissionless period pruning. *(PROD, MUST, settled)*  
When any caller requests removal of a membership tree whose period ended more than P-ECO-5 earlier, the Bus Registry shall remove that tree.  
*Verification.* test on the mock Bus Registry and a devnet: an unprivileged caller prunes an ended period after P-ECO-5; a request before then fails.

**MPE-ECO-056** Registration price instrument. *(PROD, MAY, open)*  
Where a registration price beyond the network fee is enabled, MPE shall state in the MIP the token and receive path of that price, with shielded NIGHT as the default token.  
*Verification.* inspection of the MIP; an unshielded price also applies MPE-ECO-036.

**MPE-ECO-057** Stable hash for the admission relation. *(PROD, MUST, settled)*  
MPE shall build the in-circuit admission relation only from hash functions that Midnight documents as stable across upgrades, never from `transientHash`.  
*Verification.* inspection of the relation against the Compact standard library documentation (`persistentHash` is guaranteed to persist between upgrades; `transientHash` is not).

**MPE-ECO-058** Durable credit reservation. *(POC, MUST, settled)*  
The MPE client library shall durably reserve each credit (admission window, class, index) before sending any share computed under it, use disjoint credit ranges on devices sharing one membership, and, after a restore with uncertain credit state, not publish under that membership until every admission window it might have used has ended plus P-ECO-6, unless it registers a fresh membership.  
*Verification.* test: crash after reservation and before sending, roll back client state, and run two devices on one membership; in no case do two different MPE Envelope Identifiers carry shares under one admission nullifier.


## A.7 GossipSub overlay and Midnight tether (MPE-NET) {#a7-net}

**MPE-NET-001a** Sidecar process. *(POC, MUST, settled)*  
The Bus Node shall run as an operating-system process separate from `midnight-node`.  
*Verification.* inspection, the Prototype is its own binary and runs beside an unmodified node.

**MPE-NET-001b** No MPE code in the node binary. *(POC, MUST, settled)*  
MPE shall add no code to the `midnight-node` binary.  
*Verification.* inspection, the `midnight-node` dependency tree is unchanged by the MPE build.

**MPE-NET-002** Overlay at launch. *(POC, MUST, open: DEC-NET-1)*  
MPE shall carry MPE Envelopes over the GossipSub overlay from the first release stage.  
*Verification.* demonstration. The Prototype delivers Envelopes with no Midnight transaction per Envelope.

**MPE-NET-003** No node change. *(PROD, MUST, settled)*  
MPE shall operate with an unmodified `midnight-node` binary, runtime and pallet set.  
*Verification.* inspection. The Prototype runs against a stock local devnet node.

**MPE-NET-004** Validators not required. *Same obligation as MPE-OPS-001, which owns it.*

**MPE-NET-005** Distinct peer identity. *(POC, MUST, settled)*  
The Bus Node shall use a libp2p identity key distinct from the network key of any Midnight node on the same host.  
*Verification.* test. The Prototype refuses to start when given the co-located node's network key file.

**MPE-NET-006** Network-scoped names. *(POC, MUST, settled)*  
The Bus Node shall derive every MPE GossipSub topic name and request-response protocol identifier from the prefix `/mpe/<g>/1`, where `g` is the first eight bytes of the Midnight genesis hash in lowercase hexadecimal.  
*Verification.* test. Two swarms with different genesis hashes share a bootstrapper, and no Envelope crosses between them; inspection: admission binds the full genesis hash, because the eight-byte prefix is a routing label, not an authenticated network identifier.

**MPE-NET-007** Transport baseline. *(POC, MUST, settled)*  
The Bus Node shall support TCP with Noise encryption and Yamux multiplexing as its mandatory transport stack.  
*Verification.* test. Two Prototype nodes built with only TCP, Noise and Yamux exchange Envelopes.

**MPE-NET-008** GossipSub v1.2 profile with scoring. *(POC, MUST, settled)*  
The Bus Node shall relay MPE Envelopes using a GossipSub router with v1.1 peer scoring, extended application validation and the v1.2 IDONTWANT capability enabled.  
*Verification.* inspection of the configuration and of the negotiated identifier `/meshsub/1.2.0`; test, per-peer scores appear in metrics and IDONTWANT is exchanged on v1.2 links but not on v1.1 links.  
*Note.* The v1.2 specification is not final (revision r2, 30 August 2026). Compatibility with a v1.1 peer does not provide IDONTWANT on that connection.

**MPE-NET-009a** StrictNoSign publication. *(POC, MUST, settled)*  
The Bus Node shall publish every MPE Envelope under the GossipSub StrictNoSign policy, with the `from`, `seqno`, `signature` and `key` fields absent.  
*Verification.* test, captured RPC frames lack all four fields.

**MPE-NET-009b** Signed-field rejection. *(POC, MUST, settled)*  
If a received GossipSub message carries a `from`, `seqno`, `signature` or `key` protobuf field, including an explicitly empty one, then the Bus Node shall drop it and apply the invalid-message penalty to the forwarding peer.  
*Verification.* test, an injected message carrying any one of the four fields, present or empty, is not delivered and the forwarding peer's P4 score falls; inspection, the pinned decoder enforces the `key` check, which the vendored gossipsub 0.50.0 decoder lacks and the 0.51.0 source adds.

**MPE-NET-010** Wire-byte message id. *(POC, MUST, open: DEC-FMT-3)*  
The Bus Node shall set the GossipSub message identifier to SHA-256 over the domain string `mpe/v1/msgid` and the complete MPE Envelope bytes carried as `Message.data`, including the Admission Slot and excluding all protobuf, RPC and transport framing.  
*Verification.* test, two Envelopes differing only in the Admission Slot get distinct ids and one Envelope Identifier; identical bytes get one id; all implementations agree on test vectors and no data transform is configured.

**MPE-NET-011** Mesh degree. *(POC, MUST, open: DEC-NET-3)*  
The Bus Node shall set `D`, `D_lo`, `D_hi` and `D_out` to P-NET-1, P-NET-2, P-NET-3 and P-NET-4, satisfying `D_lo` ≤ `D` ≤ `D_hi`, `D_out` < `D_lo` and `D_out` ≤ `D`/2.  
*Verification.* inspection of the configuration dump, plus a test that a configuration violating any of the three constraints fails at startup; interoperability with the inspected Go implementation, whose validator requires `D_out` < `D`/2 and rejects (8, 6, 12, 4), is recorded as not established until tested.  
*Note.* These are mesh maintenance targets. They guarantee neither a minimum degree nor a bound on all recipients: gossip, explicit peers, publication replenishment and opportunistic grafting add neighbours.

**MPE-NET-012** Timing parameters. *(POC, SHOULD, open: DEC-NET-3)*  
The Bus Node shall set the heartbeat interval, gossip factor and prune backoff to P-NET-5, P-NET-6 and P-NET-7.  
*Verification.* inspection of the configuration dump.

**MPE-NET-013** Flood publishing off. *(POC, MUST, settled)*  
The Bus Node shall disable GossipSub flood publishing on every MPE GossipSub topic.  
*Verification.* test. A node with 30 connected peers sends a fresh Envelope to at most P-NET-3 first-hop peers.

**MPE-NET-014** Encoded RPC size cap. *(POC, MUST, settled)*  
If an encoded GossipSub RPC, including batched messages and control fields, exceeds P-NET-8 bytes, then the Bus Node shall drop it without forwarding.  
*Verification.* test. An RPC of P-NET-8 + 1 bytes is neither delivered nor forwarded; inspection, Go peers set this limit explicitly instead of their 1 MiB default, and the application check of Envelope length is separate.

**MPE-NET-015** Validate before forwarding. *(POC, MUST, settled)*  
The Bus Node shall forward an MPE Envelope's payload only after its application validator has returned Accept.  
*Verification.* test. An Envelope held in validation is not seen by any downstream peer until Accept; inspection, identifier calculation, seen-cache entry, IDONTWANT and delivery bookkeeping may precede Accept and are documented as such.

**MPE-NET-016** Reject outcome. *(POC, MUST, settled)*  
If an MPE Envelope fails a layout or admission check that does not depend on chain state, then the Bus Node shall return Reject.  
*Verification.* test. Every entry of the FMT mutated-header list gets Reject, and the sender's P4 term falls.

**MPE-NET-017** Ignore outcome. *Same obligation as MPE-PUB-028, which owns it.*

**MPE-NET-018** Stale chain view never penalises. *(POC, MUST, settled)*  
While the Ledger Adapter view is stale, the Bus Node shall return Ignore instead of Reject for every MPE Envelope whose failed check depends on chain state or the local clock.  
*Verification.* test, freeze the mock adapter; cached-valid Envelopes still reach Subscribers and no peer's P4 term changes.

**MPE-NET-019** Clock and stall detection. *(POC, MUST, settled)*  
If the local clock and the latest finalized block timestamp differ by more than P-NET-13 seconds, then the Ledger Adapter shall mark its view stale.  
*Verification.* test. Pause the mock chain, or shift the local clock by P-NET-13 + 1 s; the view becomes stale.

**MPE-NET-020** Source disagreement. *(PROD, MUST, settled)*  
If two configured chain sources report different Bus Registry admission roots for the same finalized block, then the Ledger Adapter shall mark its view stale.  
*Verification.* test. Two mock sources diverge at one height; the view becomes stale and an alarm metric is raised.

**MPE-NET-021** Score penalty signs. *(POC, MUST, settled)*  
The Bus Node shall configure negative weights for the invalid-message (P4) and IP-colocation (P6) score terms, with P6 threshold P-NET-15.  
*Verification.* test. P-NET-15 + 2 peers on one IP all get a negative P6 contribution.

**MPE-NET-022** Eviction of misbehaving peers. *(POC, MUST, settled)*  
When a mesh peer has delivered only Rejected MPE Envelopes, or no MPE Envelope within the GossipSub mesh-delivery window, for P-NET-16 consecutive heartbeats in each of which the Shard carried an accepted MPE Envelope, the Bus Node shall prune that peer from its mesh.  
*Verification.* simulation with asymmetric latency and topology, slow honest peers, every supported Shard and at least 90 loaded heartbeats: withholding and invalid-only peers at 10 Envelopes/s are pruned within P-NET-16 heartbeats, no honest peer is pruned, and no peer is pruned in an idle Shard; the report states whether near-first deliveries were tracked or approximated by first deliveries.

**MPE-NET-023** Per-peer per-Shard rate limit. *(POC, MUST, settled)*  
If a peer sends more than P-NET-10 MPE Envelopes per second on one Shard, then the Bus Node shall drop the excess with Ignore before proof verification.  
*Verification.* test, at 5 x P-NET-10 from one peer on one Shard, verifier calls for that peer and Shard stay at or below P-NET-10 per second.

**MPE-NET-024** Bootstrapper mode. *(POC, SHOULD, settled)*  
Where a Bus Node runs as a bootstrapper, it shall set `D`, `D_lo`, `D_hi` and `D_out` to zero and return at least one Peer Exchange candidate on every PRUNE.  
*Verification.* test. A bootstrapper forwards no Envelopes and returns peer identifiers on PRUNE (`prune_peers` above zero); inspection, until this profile is demonstrated the reference bootstrappers relay and are reported as relaying.

**MPE-NET-025** Bootstrapper set. *(PROD, MUST, settled)*  
MPE shall publish at least P-NET-11 bootstrappers, each run by a distinct Bus Operator on a host that is not a Midnight chain bootnode.  
*Verification.* inspection of the published list against Bus Operator records and `res/mainnet/bootnodes-config.json`.

**MPE-NET-026** Bootstrap list authenticity. *(PROD, SHOULD, settled)*  
When the Bus Node loads a bootstrap list, it shall verify the list hash against the bootstrap-list hash in the Bus Registry.  
*Verification.* test. A list with one substituted address is refused and not dialed.

**MPE-NET-027** Peer Exchange acceptance. *(PROD, MUST, settled)*  
The Bus Node shall accept Peer Exchange suggestions only from peers whose score reaches `AcceptPXThreshold`, a value attainable only through the bootstrapper application score, and only for identities the Bus Registry authorizes.  
*Verification.* test. Peer Exchange from a high-scoring non-bootstrapper is ignored, and a bootstrapper's suggestion of an identity absent from the Bus Registry relay list is not dialed.

**MPE-NET-028** Outbound quota sources. *(POC, MUST, settled)*  
The Bus Node shall fill its `D_out` quota only with peers it dialed from the bootstrap list, bootstrapper Peer Exchange or the Bus Registry relay list, after the same authentication and address checks for every dial source.  
*Verification.* test. With a DHT full of attacker ids, every `D_out` slot holds a non-DHT peer, and a suggested private or unauthenticated address is not dialed.

**MPE-NET-029** No local-network discovery. *(POC, MUST, settled)*  
While running outside a development profile, the Bus Node shall not discover or dial peers on private, link-local or loopback addresses.  
*Verification.* test. Production profile: no mDNS traffic, and private-address dials are refused.

**MPE-NET-030** Warm-up before injection. *(PROD, SHOULD, settled)*  
While the Bus Node has not held at least `D_out` outbound mesh peers continuously for P-NET-12 seconds, it shall refuse local client publications with a not-ready error.  
*Verification.* test. A publication during warm-up returns not-ready and is not injected.

**MPE-NET-031** Shard GossipSub topics from the Bus Registry. *(POC, MUST, open: DEC-NET-4)*  
The Bus Node shall subscribe to the Shard GossipSub topics defined by the shard count P-NET-9 read from the Bus Registry.  
*Verification.* test. Changing the mock Bus Registry value changes the subscribed GossipSub topic set.

**MPE-NET-032** Shard-count transition. *Same obligation as MPE-PUB-003, which owns it.*

**MPE-NET-033** Publish ingress hop. *(POC, SHOULD, open: DEC-NET-6)*  
When the MPE client library publishes an MPE Envelope, it shall send it to exactly one Bus Node chosen at random from at least two Bus Nodes the client dialed itself.  
*Verification.* test. Across 1,000 publications, each one reaches exactly one first Bus Node, and the choice spans at least two nodes.

**MPE-NET-034** Relay allow-list. *Same obligation as MPE-OPS-007, which owns it.*

**MPE-NET-035** Ledger Adapter interface. *(POC, MUST, settled)*  
The Ledger Adapter shall expose finalized Bus Registry reads and Midnight transaction submission through one interface that has a mock implementation.  
*Verification.* test. The full Prototype suite passes against the mock adapter, and a subset passes against a devnet adapter.

**MPE-NET-036** Finalized state only. *(POC, MUST, settled)*  
The Ledger Adapter shall return Bus Registry state only from finalized blocks.  
*Verification.* test. A Bus Registry write that is included but not finalized is invisible to the adapter.

**MPE-NET-037** Contract-state read path. *(POC, MUST, open: DEC-NET-5)*  
The Ledger Adapter shall obtain admission roots and network parameters from Bus Registry contract state without depending on `contractEvents`.  
*Verification.* demonstration. The adapter reads a root via `midnight_contractState` on a ledger-8 devnet.

**MPE-NET-038** Relaying during a governance pause. *(PROD, MUST, settled)*  
While safe mode filters Midnight user transactions, the Bus Node shall keep relaying MPE Envelopes admitted under previously accepted Bus Registry roots until those admissions expire.  
*Verification.* test. With safe mode entered on a devnet, existing admissions deliver and new registrations fail.

**MPE-NET-039** Bus Registry fields. *(POC, MUST, settled)*  
The Bus Registry shall expose as public ledger state the shard count, its activation height, the maximum MPE protocol version, the current admission root and the bootstrap-list hash.  
*Verification.* inspection of the contract, plus a test that the adapter reads each field.

**MPE-NET-040** Fixed `Misc` names. *(PROD, MUST, settled)*  
The Bus Registry shall emit only `Misc` events, each named `mip-xxxx:anchor[v1]` or `mip-xxxx:governance[v1]` and NUL-padded to 32 bytes.  
*Verification.* inspection of every `emit` site, plus a test over 100 emits showing one distinct `name` per event kind and no `Paused` or `Unpaused` standard event.

**MPE-NET-041** Anchor cadence. *(PROD, SHOULD, settled)*  
Where a Bus Node acts as anchorer, the Bus Node shall submit at most one Anchor per non-empty P-NET-17 window, covering every Shard.  
*Verification.* test, ten windows with three empty ones produce seven Anchors, each listing all Shards' counts.

**MPE-NET-042** Explicit carrier label. *(POC, MUST, settled)*  
When the MPE client library carries a Message over a path other than the overlay, it shall label that Message with the carrier it used for the Consumer.  
*Verification.* test. With the overlay disabled, every delivered Message carries a non-overlay label.

**MPE-NET-043a** Complete-stream gateway. *(PROD, SHOULD, open: DEC-NET-2)*  
Where the gateway fallback is enabled, the Bus Node shall serve the complete MPE Envelope stream of a requested Shard in overlay framing.  
*Verification.* test, the byte streams from the overlay and from the gateway match for one Shard over 1 h.

**MPE-NET-043b** No filter on the gateway. *(PROD, SHOULD, open: DEC-NET-2)*  
Where the gateway fallback is enabled, if a stream request carries a filter on streams, Recognition Tags or identifiers, then the Bus Node shall refuse the request with `Refused`.  
*Verification.* test, each filter parameter is refused and no Envelope is sent.

**MPE-NET-044** Ledger lane. *(PROD, MAY, open: DEC-NET-2)*  
Where the ledger lane is enabled, the MPE client library shall publish each MPE Envelope on the ledger lane as the 4^c `Misc` parts of MPE-FMT-041, all named `mip-xxxx:envelope[v1]`.  
*Verification.* test on a ledger-9 devnet: ledger-lane publications of classes 0, 1 and 2 show 1, 4 and 16 parts with one `name` and 256-byte payloads.

**MPE-NET-045** Unmodified Indexer. *(POC, MUST, settled)*  
The Indexer adapter shall use only queries and subscriptions present in the unmodified Indexer `schema-v4` API.  
*Verification.* inspection. Every GraphQL operation in the adapter validates against `schema-v4.graphql`.

**MPE-NET-046** Unmodified Compact toolchain. *(POC, MUST, settled)*  
The Prototype shall build its Bus Registry contract with an unmodified released Compact toolchain.  
*Verification.* inspection. The build log names a released toolchain version with no patches.

**MPE-NET-047** IDONTWANT measurement. *(POC, SHOULD, settled)*  
The Prototype shall report per-Bus-Node bytes sent with GossipSub v1.2 IDONTWANT enabled at threshold P-NET-18 and with IDONTWANT disabled.  
*Verification.* test. Paired runs report the egress difference per size class and state which behaviour was disabled: a Rust emission threshold of 65,537 B suppresses emission only, not receipt or honouring of notices.

**MPE-NET-048** Shard stream service. *(POC, MUST, settled)*  
The Bus Node shall provide a stream protocol that sends a connected non-mesh client every MPE Envelope the Bus Node accepts on each Shard the client requests.  
*Verification.* test, a client streaming one Shard receives every accepted identifier over 1 h; inspection, the service is an MPE request-response protocol, not a GossipSub subscription.

**MPE-NET-049** Publish acceptance reply. *(POC, MUST, settled)*  
When the Bus Node has committed application acceptance of a client-submitted MPE Envelope and queued it for sending, the Bus Node shall send that client an `Accepted` reply carrying the MPE Envelope Identifier.  
*Verification.* test, a client receives `Accepted` for accepted and queued Envelopes, `PublishFailed` when the publish call fails, `Busy` for transient local unavailability and `Refused` for every other refusal, including Envelopes the Bus Node Rejects or Ignores; inspection, these are MPE service replies, not GossipSub validator outcomes.

**MPE-NET-050** Anchor payload. *(POC, MUST, settled)*  
Where a Bus Node acts as anchorer, the Bus Node shall encode each Anchor payload as an 8-byte big-endian window number, the 32-byte window root, eight 4-byte big-endian MPE Envelope counts and zero fill to 256 bytes.  
*Verification.* test vectors: field offsets and payload length do not depend on the Shard count (counts of unused Shards are zero); a mock Bus Registry decodes every field.

**MPE-NET-051** Batch root construction. *(POC, MUST, settled)*  
Where a Bus Node acts as anchorer, the Bus Node shall compute each per-Shard batch root as a SHA-256 Merkle root over the window's accepted MPE Envelope Identifiers in ascending byte order.  
*Verification.* test vectors; an independent implementation reproduces the roots.

**MPE-NET-052** Inclusion path service. *(POC, MUST, settled)*  
Where a Bus Node acts as anchorer, the Bus Node shall return, on request, the Merkle inclusion path of an anchored MPE Envelope Identifier for P-STO-9 after anchoring.  
*Verification.* test, paths verify against the Anchor root; a path for a non-anchored identifier is refused.

**MPE-NET-053** Anchorer authorization. *(PROD, MUST, open: DEC-OPS-2)*  
The Bus Registry shall accept an Anchor only from a caller that proves, in circuit, knowledge of the preimage of the anchorer key commitment stored in a relay entry with the anchorer role.  
*Verification.* test, an Anchor from an unlisted relay or without the preimage fails on a devnet and on the mock Bus Registry.

**MPE-NET-054** Relay list entries. *(POC, MUST, settled)*  
The Bus Registry shall expose a relay list keyed by SHA-256 of each relay's serialized libp2p PeerId, whose entries carry a Bus Operator organization identifier, role flags for relay, Store Node, bootstrapper, gateway and anchorer, and an anchorer key commitment.  
*Verification.* inspection of the contract; test, the adapter reads every field and recomputes each key from the relay's PeerId, never treating a 32-byte value as a serialized PeerId.

**MPE-NET-055** Ledger Adapter read set. *(POC, MUST, settled)*  
The Ledger Adapter shall expose finalized reads of membership roots with publication and supersession times taken from including block timestamps, the relay list, Bus Registry parameters, Anchors, the bus pause flag and the current `ledgerParameters`.  
*Verification.* test, the mock adapter answers each read and the full Prototype suite passes against it.

**MPE-NET-056** Historic root lookup. *(POC, MUST, settled)*  
When a Store Node validates a back-filled MPE Envelope, the Ledger Adapter shall return the referenced membership root with its period and supersession time if that root was eligible at the MPE Envelope's creation time (visible expiry minus 172,800 s), keeping each root for 172,860 s after the last moment it could authorize an admission, independently of live-tree pruning.  
*Verification.* test, a Message admitted late in a membership period under a root published at the period's start and back-filled shortly before its expiry validates; back-fill after two root rotations validates against the historical root.

**MPE-NET-057** Negotiated protocol recorded. *(POC, MUST, settled)*  
The Bus Node shall record the negotiated GossipSub protocol identifier and internal peer kind of every pubsub connection.  
*Verification.* test: connection metrics list the negotiated identifier and peer kind for v1.1, v1.2 and custom-identifier peers.

**MPE-NET-058** Version policy enforced. *(POC, MUST, settled)*  
If a peer's negotiated GossipSub protocol is not the selected v1.2 profile identifier, then the Bus Node shall refuse that peer a mesh slot.  
*Verification.* negotiation test with a v1.1-only peer and a peer that also offers v1.3: neither joins a mesh under another version; a default offer list is not accepted as proof of v1.2.

**MPE-NET-059** Local publication checks. *(POC, MUST, settled)*  
When a local client submits an MPE Envelope for publication, the Bus Node shall apply the same application validation as for a received MPE Envelope before calling GossipSub publish.  
*Verification.* test: a locally submitted Envelope that would be Rejected on receipt is never published.

**MPE-NET-060** Validation within cache lifetime. *(POC, MUST, settled)*  
If reporting a validation result fails because the message has left the GossipSub message cache, then the Bus Node shall record that MPE Envelope as not propagated.  
*Verification.* test: delay validation beyond the message-cache lifetime; the result report fails, the Envelope is counted as not propagated, and no metric reports it as delivered.

**MPE-NET-061** Publish failure reported. *(POC, MUST, settled)*  
If the GossipSub publish call fails for an MPE Envelope the Bus Node has accepted, then the Bus Node shall answer the publication request with a single `PublishFailed` reply naming that MPE Envelope Identifier, in place of `Accepted`.  
*Verification.* test: with no mesh or fanout peers and with a full publication queue, the client receives `PublishFailed{eid}` as the only reply to its request; with peers and queue space it receives `Accepted{eid}`.

**MPE-NET-062** IDONTWANT on capable links. *(POC, MUST, settled)*  
The Bus Node shall send and honour IDONTWANT on every link that negotiated GossipSub v1.2.  
*Verification.* test: on v1.2 links IDONTWANT is emitted for messages above the threshold and honoured on receipt; on v1.1 links none is sent.

**MPE-NET-063** IDONTWANT size predicate. *(POC, MUST, settled)*  
The Bus Node shall emit IDONTWANT only for messages whose serialized pubsub-message length exceeds P-NET-18 bytes.  
*Verification.* test at the boundary: a message of exactly P-NET-18 serialized bytes triggers no IDONTWANT; interoperability reports record each implementation's predicate (Go compares payload length, sends at equality and defaults to 1,024 B).

**MPE-NET-064** No penalty for sends after IDONTWANT. *(POC, MUST, settled)*  
If a peer sends a message after the Bus Node's IDONTWANT for it, then the Bus Node shall apply no score penalty for that send.  
*Verification.* test: a peer that sends a notified message is not penalised; suppression lifetime and queued-send cancellation are recorded separately from the seen-cache lifetime.

**MPE-NET-065** IDONTWANT excess limit. *(PROD, MUST, settled)*  
Where an excess-IDONTWANT penalty is configured, the Bus Node shall apply it only above a per-peer, per-heartbeat IDONTWANT limit stated in the release profile.  
*Verification.* inspection of the release profile; test: a peer within the stated limit is not penalised, one above it is.

**MPE-NET-066** Subscription name filter. *(POC, MUST, settled)*  
If a peer subscribes to a GossipSub topic outside the supported MPE major versions, the selected genesis prefix and the Bus Registry's current or transitional Shards, then the Bus Node shall refuse that subscription.  
*Verification.* test: subscriptions with a foreign genesis prefix, an unsupported major version or an unauthorized Shard index are refused; subscription-count limits still apply.

**MPE-NET-067** No unreviewed GossipSub extensions. *(POC, MUST, settled)*  
The Bus Node shall negotiate no GossipSub extension that changes message behaviour, including partial messages, unless the release profile specifies and reviews it for privacy.  
*Verification.* test: negotiation with a peer offering v1.3 extensions enables none of them; inspection of the release profile.

**MPE-NET-068** No action on unfinalized state. *(POC, MUST, settled)*  
The Ledger Adapter shall take no value from a block that is not finalized, whether Bus Registry state, an Anchor, a ledger-lane part or a carried-event transcript.  
*Verification.* test with the mock Ledger Adapter: values written in an included but unfinalized block are invisible to every read, so no rollback is needed.

**MPE-NET-069** Bus Registry clock tolerance. *(PROD, MUST, open)*  
When a Bus Registry circuit performs a time-dependent write, the Bus Registry shall accept the caller-supplied clock value only within 900 s of the block time.  
*Verification.* test on the mock Bus Registry and a devnet: values 901 s from block time fail; a transaction that waits in the pool beyond the tolerance fails.

**MPE-NET-070** Bus Registry toolchain floor. *(POC, MUST, settled)*  
The Prototype shall build the Bus Registry, ledger-lane and consumer contracts with a released Compact toolchain at version 0.33.0 or later, which provides `emit` and witness-free cross-contract reads.  
*Verification.* inspection: the build log names the toolchain and compiler versions (0.35.0, language 0.27.0 in the reference build).


## A.8 Performance and capacity (MPE-PRF) {#a8-prf}

PRF defines D5 capacity limits, latency targets, node resource budgets and Prototype measurement workloads.
Rates count Envelopes; logical Message throughput depends on fragmentation and recipient fan-out.
The recommended default is 10 Envelopes/s plus 64 KiB/s per Shard, whichever binds first; g1’s 50/s proposal remains a required comparison.
All proposed performance numbers are targets or arithmetic on assumptions, not measured MPE capabilities.
Admission, client recognition, retrieval and chain latency are measured separately from relay propagation.
Overlay configuration, admission correctness, retention and privacy guarantees remain dependencies on the other areas.

**MPE-PRF-001** Complete traffic accounting. *(POC, MUST, settled)*  
The Prototype shall report traffic accounting that distinguishes logical Messages, unique MPE Envelopes, recipient copies, fragments, admission traffic, duplicates, overlay control traffic, back-fill traffic and transport overhead.  
*Verification.* inspection, reconcile accounting categories with generated traffic and captured bytes.

**MPE-PRF-002** Reproducible benchmark manifest. *(POC, MUST, settled)*  
The Prototype shall produce a manifest for each performance run specifying software revisions, hardware, MPE Envelope sizes, admission mechanism, topology, mesh settings, workload, connection state, impairments, measurement interval and random seed.  
*Verification.* inspection, reproduce a run from its manifest.

**MPE-PRF-003** Percentiles with delivery denominators. *(POC, MUST, settled)*  
The Prototype shall report p50, p95 and p99 latency distributions with their eligible-delivery counts, completed-delivery counts, losses, timeouts and observation deadlines.  
*Verification.* test, inject omissions and confirm they remain visible alongside the percentile results.

**MPE-PRF-004** Separate latency stages. *(POC, MUST, settled)*  
The Prototype shall report separate latency distributions for authorization, publication preparation, relay propagation, Subscriber delivery, recognition, back-fill, Anchor submission, transaction inclusion, finality, indexing and contract reaction.  
*Verification.* inspection, reconcile stage timestamps with end-to-end samples and identify mocked stages.

**MPE-PRF-005** Measured propagation amplification. *(POC, MUST, settled)*  
The Prototype shall report per-Bus-Node receive and transmit amplification as measured wire bytes divided by unique accepted MPE Envelope bytes.  
*Verification.* analysis, reconcile directional amplification with packet captures and unique-byte counters.

**MPE-PRF-006** Sustained Shard capacity. *(POC, MUST, open: DEC-PRF-1)*  
While Reference conditions hold, MPE shall deliver at least P-VER-7 of eligible MPE Envelope-Subscriber pairs within P-VER-6 for an offered load of min(P-PRF-1, P-PRF-2 divided by mean complete MPE Envelope size) MPE Envelopes per second per Shard sustained for P-VER-3.  
*Verification.* test, run count-bound (class 0) and byte-bound (class 3) workloads and compute the delivery fraction per MPE-VER-014.

**MPE-PRF-007** Normal-load delivery. *(POC, MUST, open: DEC-PRF-3)*  
While Reference conditions hold at the sustained Shard capacity, MPE shall deliver every accepted MPE Envelope to every continuously connected eligible Subscriber within P-VER-6 after admission.  
*Verification.* test, compare accepted identifiers with each Subscriber's received identifiers and timestamps.

**MPE-PRF-008** Median warm propagation. *(PROD, MUST, open: DEC-PRF-3)*  
While Reference conditions hold at the sustained Shard capacity, MPE shall keep warm relay propagation p50 at or below P-PRF-10.  
*Verification.* test, calculate p50 using the warm propagation clock defined below.

**MPE-PRF-009** Tail warm propagation. *(PROD, MUST, open: DEC-PRF-3)*  
While Reference conditions hold at the sustained Shard capacity, MPE shall keep warm relay propagation p99 at or below P-PRF-11.  
*Verification.* test, calculate p99 alongside the delivery denominator.

**MPE-PRF-010** Mesh profile comparison. *(POC, MUST, open: DEC-PRF-2)*  
The Prototype shall benchmark the GossipSub v1.2 profile using each P-PRF-4 mesh tuple with P-PRF-5, P-PRF-6, P-PRF-7 and P-PRF-8 explicitly configured.  
*Verification.* simulation, compare delivery, percentiles, amplification and CPU under identical workloads; each tuple satisfies the mesh constraints of MPE-NET-011, and gossip and publication recipients are counted separately from mesh degree.

**MPE-PRF-011** Gossip-factor retry. *(POC, MUST, settled)*  
If the default mesh misses the warm propagation p99 target, then the Prototype shall repeat the failing workload with the alternative P-PRF-5 gossip factor.  
*Verification.* simulation, reproduce the failure and compare the repeated run.

**MPE-PRF-012** Degree-transient cost. *(POC, MUST, settled)*  
The Prototype shall measure resource consumption during mesh oversubscription and pruning at the configured P-PRF-4 high-water degree.  
*Verification.* simulation, correlate observed mesh degree with traffic, CPU and queue peaks.

**MPE-PRF-013** Edge bandwidth budget. *(PROD, MUST, open: DEC-PRF-4)*  
While Reference conditions hold at the sustained Shard capacity, the Bus Node operating as an Edge Bus Node shall consume no more than P-PRF-12 of bus bandwidth in each direction.  
*Verification.* test, capture receive and transmit separately over the steady interval.

**MPE-PRF-014** Full bandwidth budget. *(PROD, MUST, open: DEC-PRF-4)*  
While Reference conditions hold with P-PRF-16 Shards at their sustained capacity, the Bus Node operating as a Full Bus Node shall consume no more than P-PRF-13 of bus bandwidth in each direction.  
*Verification.* test, capture receive and transmit separately with all allocated Shards active.

**MPE-PRF-015** Edge CPU budget. *(PROD, MUST, open: DEC-PRF-4)*  
While Reference conditions hold at the sustained Shard capacity, the Bus Node operating as an Edge Bus Node shall consume no more than P-PRF-14 cores for bus processing.  
*Verification.* test, measure process CPU on declared reference hardware.

**MPE-PRF-016** Full CPU budget. *(PROD, MUST, open: DEC-PRF-4)*  
While Reference conditions hold with P-PRF-16 Shards at their sustained capacity, the Bus Node operating as a Full Bus Node shall consume no more than P-PRF-15 cores for bus processing.  
*Verification.* test, measure process CPU with all allocated Shards active.

**MPE-PRF-017** Admission validation benchmark. *(POC, MUST, settled)*  
The Prototype shall report wall-clock Admission Proof validation costs for valid, invalid, duplicate, cached and uncached inputs on each tested Bus Node hardware class.  
*Verification.* test, report distributions, CPU consumption and cache-hit rates for the selected admission implementation.

**MPE-PRF-018** Publication preparation benchmark. *(POC, MUST, settled)*  
The Prototype shall report publication preparation costs on server, laptop and mobile hardware for the selected Admission Proof mechanism.  
*Verification.* test, measure generation latency, CPU and serialized bytes, marking unavailable implementations unknown; state for each hardware class whether proof generation runs locally.

**MPE-PRF-019** Desktop recognition budget. *(POC, MUST, open: DEC-PRF-4)*  
While the desktop recognition profile P-PRF-19 is active, the MPE client library shall consume no more than P-PRF-20 cores for recognition.  
*Verification.* test, measure matching and nonmatching traffic with the declared recognition keys.

**MPE-PRF-020** Mobile recognition boundary. *(POC, SHOULD, open: DEC-PRF-4)*  
Where whole-Shard recognition on mobile hardware is present, the MPE client library shall satisfy the P-PRF-21 recognition CPU budget.  
*Verification.* test, measure recognition CPU on a named device using the declared one-key fixture.

**MPE-PRF-021** Subscriber download cost. *(POC, MUST, settled)*  
The Prototype shall report measured Subscriber download bytes per delivered MPE Envelope and the resulting daily volume for every supported subscription profile.  
*Verification.* analysis, reconcile captures with daily extrapolations and disclose the extrapolation workload.

**MPE-PRF-022** Edge stream concurrency. *(POC, MUST, open: DEC-PRF-5)*  
The Bus Node operating as an Edge Bus Node shall limit active full-Shard streams to P-PRF-17.  
*Verification.* test, request one stream beyond the limit and confirm refusal.

**MPE-PRF-023** Gateway Subscriber capacity. *(POC, SHOULD, open: DEC-PRF-5)*  
While Reference conditions hold on one Shard at its sustained capacity, MPE shall deliver at least P-VER-7 of that Shard's accepted MPE Envelopes within P-VER-6 to each of the P-PRF-18 concurrently connected Subscribers.  
*Verification.* demonstration, run the gateway topology and compute per-Subscriber delivery fractions.

**MPE-PRF-024** Gateway resource curve. *(POC, MUST, settled)*  
The Prototype shall report gateway CPU, memory, egress and delivery latency as Subscriber concurrency rises through the P-PRF-18 topology.  
*Verification.* test, identify the first saturated resource and associated delivery degradation.

**MPE-PRF-025** Fifty-per-second comparison. *(POC, MUST, settled)*  
The Prototype shall execute P-PRF-28 as a separately reported comparison workload.  
*Verification.* test, compare measured bandwidth, CPU and latency with g1’s corrected estimates and stated gates.

**MPE-PRF-026** Aggregate load ladder. *(POC, MUST, settled)*  
The Prototype shall execute every P-PRF-30 aggregate load on the P-PRF-3 Shard topology.  
*Verification.* simulation, report offered rate, accepted rate and delivered rate per Shard.

**MPE-PRF-027** Burst workloads. *(POC, MUST, settled)*  
The Prototype shall execute every P-PRF-29 burst for P-PRF-26.  
*Verification.* test, report rejection, queue peaks, delivery tails and post-burst drain behavior.

**MPE-PRF-028** Shard concentration. *(POC, MUST, settled)*  
The Prototype shall repeat each aggregate load with all offered publications concentrated on one Shard.  
*Verification.* simulation, compare the concentrated run against its uniform counterpart.

**MPE-PRF-029** Recovery contention. *(POC, MUST, settled)*  
While live delivery shares resources with Store Node back-fill, the Prototype shall measure performance under P-PRF-31.  
*Verification.* test, record the live/back-fill split and its effects on live delivery.

**MPE-PRF-030** Admission window synchronization burst. *(POC, MUST, settled)*  
The Prototype shall measure performance when P-PRF-32 Publishers submit valid publications at the same admission window boundary.  
*Verification.* test, compare queue growth and latency against an evenly distributed publication schedule.

**MPE-PRF-031** Invalid-ingress resource cost. *(POC, MUST, settled)*  
The Prototype shall report invalid-ingress resource consumption separately from accepted-Envelope resource consumption during the SEC-defined abuse workloads.  
*Verification.* test, attribute CPU, ingress bytes and queue occupancy to invalid input categories.

**MPE-PRF-032** Attack delivery floor. *(POC, MUST, open: DEC-PRF-3)*  
While the P-PRF-22 cold-start attack is active at the nominal offered load, MPE shall deliver at least P-PRF-23 of eligible honest MPE Envelope deliveries.  
*Verification.* simulation, measure delivery among continuously connected honest recipients at each tested network size.

**MPE-PRF-033** Attack propagation tail. *(POC, MUST, open: DEC-PRF-3)*  
While the P-PRF-22 cold-start attack is active at the nominal offered load, MPE shall keep completed honest relay propagation p99 at or below P-PRF-24.  
*Verification.* simulation, calculate p99 with the losses reported under MPE-PRF-032.

**MPE-PRF-034** Queue overflow response. *(POC, MUST, open: DEC-PRF-4)*  
If admitting another publication would exceed a P-PRF-27 queue bound, then the Bus Node shall refuse that publication.  
*Verification.* test, fill each declared count or byte bound and confirm additional work is refused.

**MPE-PRF-035** Explicit capacity failure. *(POC, MUST, settled)*  
When a Publisher publication is refused because of capacity exhaustion, the Bus Node shall return an explicit capacity-exhausted result to the Publisher.  
*Verification.* test, exhaust capacity and inspect the Publisher-facing result.

**MPE-PRF-036** Stream bandwidth refusal. *(POC, MUST, open: DEC-PRF-5)*  
If serving another full-Shard stream would exceed its class bandwidth budget, then the Bus Node shall refuse the additional stream.  
*Verification.* test, exhaust the measured stream budget before the socket limit.

**MPE-PRF-037** Sustained soak. *(POC, MUST, settled)*  
The Prototype shall run the recommended operating workload continuously for P-PRF-25.  
*Verification.* test, inspect resource time series and delivery outcomes throughout the soak.

**MPE-PRF-038** Performance stop classification. *(POC, MUST, open: DEC-PRF-3)*  
If delivery falls below P-PRF-23 or relay propagation p99 exceeds P-PRF-24 with 200 Bus Nodes, then the Prototype shall classify that configuration as failing the overlay performance gate.  
*Verification.* test, feed each failing result into the acceptance report and confirm failure classification.

**MPE-PRF-039** Indexer fan-out comparison. *(POC, MUST, open: DEC-PRF-6)*  
Where an Indexer fallback is present, the Prototype shall benchmark the P-PRF-33 workload.  
*Verification.* test, measure query rate, CPU, response bytes and fan-out latency after indexing.

**MPE-PRF-040** Measured ledger-lane capacity. *(POC, MUST, settled)*  
The Prototype shall report the ledger-lane throughput ceiling under both the `block_usage` and the `bytes_written` block limits, using the measured serialized size of one `Misc` event and of 1-, 4- and 16-part groups.  
*Verification.* analysis, show both limit calculations with MIP-0002's 40-byte overhead (about 6.3 class-1 and 1.5 class-2 Envelopes per second for the whole chain at 50,000 B of `bytes_written` per block), identify the binding limit and record which `block_usage` value (200,000 or 1,000,000) is live.

**MPE-PRF-041** Bus Node memory ceiling. *(POC, MUST, settled)*  
While Reference conditions hold at the sustained Shard capacity, the Bus Node shall keep its resident memory at or below P-PRF-34.  
*Verification.* test, sample resident memory every 10 s through the 72 h soak.

**MPE-PRF-042** Circuit sizes stated. *(PROD, MUST, settled)*  
MPE shall state in the MIP the circuit size, as k and rows, of every Bus Registry, ledger-lane and consumer circuit.  
*Verification.* inspection against `zkir mock-compile` output for each circuit (for example `postAnchor` k = 18, 152,138 rows).

**MPE-PRF-043** Anchor proving gate. *(POC, MUST, settled)*  
If proving one Anchor transaction on the anchorer reference host takes longer than one P-NET-17 window, then the Prototype shall mark Anchor acceptance as failed.  
*Verification.* test: measure proving time and prover memory of the k = 18 Anchor circuit over 100 Anchors on the reference host.


## A.9 Storage and retention (MPE-STO) {#a9-sto}

STO owns D6: Envelope retention, storage by node class, pruning, back-fill storage, availability commitments, caches and deduplication state.
The recommended Prototype uses per-Shard Store Nodes with a bounded ordinary retention window; Bus Nodes without storage duties retain transport and admission state.
Message bodies never enter Bus Registry contract state, even on the ledger lane; the Bus Registry retains bounded metadata and Anchor records.
Retention promises are conditional on surviving reachable holders and recoverable client keys; expiry does not guarantee deletion of other parties’ copies.
Envelope encoding, admission rules, cryptographic recovery, delivery semantics, Bus Operator funding and transport configuration belong to the dependent areas identified below.

**MPE-STO-001** No bodies in ledger state. *(POC, MUST, settled)*  
The Bus Registry shall store no Message body and no Sealed Body in contract state.  
*Verification.* inspection, review the Bus Registry's state declarations and captured state writes.

**MPE-STO-002** Shard-scoped commitments. *(POC, MUST, open: DEC-STO-1)*  
The Store Node shall scope each retention commitment to a named Shard.  
*Verification.* test, commit retention for one Shard without creating retention obligations for another.

**MPE-STO-003** Reject excessive ordinary retention. *(POC, MUST, open: DEC-STO-1)*  
If a received MPE Envelope's expiry exceeds the Store Node's clock plus P-FMT-3 plus P-FMT-4, then the Store Node shall reject its storage admission.  
*Verification.* test, admission just below, at and above the limit.

**MPE-STO-004** Retain accepted Envelopes. *(POC, MUST, open: DEC-STO-1)*  
When an ordinary MPE Envelope is accepted for storage, the Store Node shall retain it until its authenticated retention deadline unless an authorized tombstone applies.  
*Verification.* test, retrieve committed Envelopes throughout their window across process restarts.

**MPE-STO-005** Complete verification material. *(POC, MUST, open: DEC-STO-2)*  
The Store Node shall retain the complete MPE Envelope verification material throughout its retention commitment.  
*Verification.* demonstration, verify a retrieved Envelope with a fresh client lacking the Store Node’s verification cache.

**MPE-STO-006** Retrieval does not refresh retention. *(POC, MUST, settled)*  
When an MPE Envelope is retrieved or received again, the Store Node shall preserve its existing retention deadline.  
*Verification.* test, repeatedly retrieve and replay an Envelope near its deadline without extending retention.

**MPE-STO-007** Expiry pruning. *(POC, MUST, settled)*  
When an MPE Envelope’s retention commitment expires, the Store Node shall remove its record from managed live storage within P-STO-2.  
*Verification.* test, advance the clock beyond expiry and inspect live records after the pruning allowance.

**MPE-STO-008** Per-Shard disk bound. *(POC, MUST, settled)*  
The Store Node shall keep its allocated storage for each retained Shard at or below P-STO-3.  
*Verification.* test, measure allocated files during sustained ingest, pruning and compaction at the configured limit.

**MPE-STO-009** Refuse storage overload. *(POC, MUST, open: DEC-STO-3)*  
If accepting an MPE Envelope would exceed its Shard’s P-STO-3 allocation, then the Store Node shall reject that storage admission with `STORAGE_FULL`.  
*Verification.* test, fill the allocation and confirm explicit refusal while previously committed Envelopes remain retrievable.

**MPE-STO-010** Refuse cache overload. *(POC, MUST, settled)*  
If live admission would exceed P-STO-4 for application storage caches, then the Bus Node shall reject that admission with `RESOURCE_EXHAUSTED`.  
*Verification.* test, exhaust cache allocation and confirm rejection without eviction of unexpired protection records.

**MPE-STO-011** Receipt follows persistence. *(POC, MUST, open: DEC-STO-5)*  
When the Store Node issues a retention receipt, the Store Node shall sign it only after committing the identified MPE Envelope to storage recoverable after process restart.  
*Verification.* test, interrupt the process around receipt issuance and recover every Envelope covered by an issued receipt.

**MPE-STO-012** Stored attribute. *(POC, MUST, open: DEC-STO-5)*  
The MPE client library shall mark a delivered Message `stored` only after validating compatible retention receipts from at least P-STO-5 distinct Bus Operators.  
*Verification.* test, reject duplicate Bus Operator receipts and receipts naming different Envelopes or deadlines.

**MPE-STO-013** Application identifier cache. *Same obligation as MPE-PUB-027, which owns it.*

**MPE-STO-014** Admission replay retention. *Same obligation as MPE-ECO-021, which owns it.*

**MPE-STO-015** Restart barrier. *(POC, MUST, open: DEC-STO-7)*  
While less than P-ECO-7 has elapsed since the Bus Node process started, the Bus Node shall return Ignore for every MPE Envelope requiring live admission.  
*Verification.* test, restart in the middle of an admission window and replay a pre-restart Envelope at 1 s and at P-ECO-7 + 1 s; neither is accepted live.

**MPE-STO-016** Historical admission context. *(POC, MUST, open: DEC-STO-2)*  
When serving back-fill, the Store Node shall provide the retained context needed to validate the MPE Envelope’s Admission Proof against its historical Bus Registry state.  
*Verification.* demonstration, retrieve after Bus Registry membership rotation and independently validate the original admission.

**MPE-STO-017** Recognition-independent requests. *(POC, MUST, settled)*  
When requesting back-fill, the MPE client library shall request complete intervals of its selected Shards without selecting MPE Envelopes by recognition results.  
*Verification.* test, compare requests from clients with different recognition keys but identical Shard and interval selections.

**MPE-STO-018** Complete retained interval. *Same obligation as MPE-PUB-031, which owns it.*

**MPE-STO-019** Explicit unavailable ranges. *(POC, MUST, settled)*  
If a back-fill request includes a known unavailable interval, then the Store Node shall identify that interval in a `RETENTION_GAP` response.  
*Verification.* test, request across expired, deleted and known lost intervals and inspect the reported boundaries.

**MPE-STO-020** Corrupt stored records. *(POC, MUST, settled)*  
If a stored MPE Envelope fails its identifier or retained verification checks, then the Store Node shall return `CORRUPT_RECORD` for the affected record.  
*Verification.* test, mutate retained body and Admission Proof bytes and confirm a failure response instead of valid Envelope delivery.

**MPE-STO-021** Bounded optional archives. *(PROD, MAY, open: DEC-STO-1)*  
Where an archive service is present, the Store Node shall retain archived MPE Envelopes only through their separately agreed deadlines within P-STO-7.  
*Verification.* inspection, inspect archive agreements and demonstrate removal from managed archive storage after their deadlines.

**MPE-STO-022** Recoverable history capability. *(POC, MUST, settled)*  
When a Subscriber queries recovery capabilities, the MPE client library shall report recoverable history as the intersection of advertised remote retention coverage and locally available decryption-state coverage.  
*Verification.* test, independently shorten remote retention and local key coverage and check the reported intersection.

**MPE-STO-023** Client payload cache bound. *(POC, MUST, settled)*  
The MPE client library shall limit its local Message payload cache to P-STO-8.  
*Verification.* test, exceed the configured payload allocation, including a zero allocation, and measure retained payload bytes.

**MPE-STO-024** Discard unmatched Envelopes. *(POC, MUST, settled)*  
When local recognition of an unmatched MPE Envelope completes, the MPE client library shall discard its MPE Envelope bytes from the recognition buffer.  
*Verification.* test, process an unmatched interval and inspect recognition-buffer contents after completion.

**MPE-STO-025** Durable recovery checkpoint. *(POC, MUST, settled)*  
When committing a recovery checkpoint, the MPE client library shall persist its cursor and corresponding logical deduplication state as one atomic checkpoint.  
*Verification.* test, inject failures during checkpoint persistence and recover either the preceding or completed checkpoint.

**MPE-STO-026** Missing recovery keys. *Same obligation as MPE-PUB-046, which owns it.*

**MPE-STO-027** Unknown Indexer retention. *(POC, MUST, settled)*  
If contract-event retention coverage has not been established for an Indexer, then the Indexer adapter shall report that coverage as `unknown`.  
*Verification.* test, configure only ledger-state retention and confirm that no contract-event retention guarantee is inferred.

**MPE-STO-028** Anchor ring of fixed size. *(POC, MUST, open: DEC-STO-4)*  
The Bus Registry shall store live Anchor records in P-STO-10 slots indexed by window number modulo P-STO-10, each new record replacing the record P-STO-10 windows older.  
*Verification.* test, insert beyond 2,940 windows and confirm that the reachable live Anchor state never exceeds 2,940 records and that a slot holding the same or a newer window refuses the post.

**MPE-STO-029** Permissionless Anchor pruning. *(POC, MUST, open: DEC-STO-4)*  
When any caller requests removal of an Anchor record older than P-STO-9, the Bus Registry shall remove that record from its live Anchor state.  
*Verification.* test, advance ledger time, prune by slot from an unprivileged caller and confirm removal; a request for a younger record fails.

**MPE-STO-030** Measure Anchor storage. *(POC, MUST, open: DEC-STO-4)*  
The Prototype shall report reachable live Anchor-state bytes after each insertion, replacement and pruning operation during a run exceeding P-STO-10 insertions.  
*Verification.* demonstration, publish a revision-qualified ledger-9 measurement showing state growth before and after capacity is reached.

**MPE-STO-031** Per-Shard Bus Operator replication. *(PROD, MUST, open: DEC-STO-5)*  
While a Shard advertises ordinary back-fill service, the MPE shall maintain storage commitments for that Shard from at least P-STO-5 distinct Bus Operators.  
*Verification.* inspection, audit Bus Operator ownership and active Shard retention commitments.

**MPE-STO-032** Measured retention availability. *(PROD, SHOULD, open: DEC-STO-5)*  
While a Shard advertises ordinary back-fill service, the MPE shall achieve at least P-STO-12 successful scheduled canary retrievals at P-STO-11 intervals during each P-STO-13 assessment interval.  
*Verification.* analysis, calculate success from scheduled probes, counting unavailable Envelopes, corrupt results and timeouts as failures.

**MPE-STO-033** Storage failure experiments. *(POC, MUST, settled)*  
The Prototype shall report within-retention retrieval outcomes for experiments covering individual Store Node loss, correlated Bus Operator loss and partitions extending beyond retention.  
*Verification.* simulation, compare retained inventories with recovered inventories under each named failure condition.

**MPE-STO-034** Measure storage by node class. *(POC, MUST, settled)*  
The Prototype shall report peak storage allocations by node class under the PRF workload profiles, separately accounting for MPE Envelope bytes, indexes, caches, replay state and database temporary files.  
*Verification.* demonstration, reconcile measured totals for Bus Nodes, Store Nodes and clients with their configured allocations.

**MPE-STO-035** Auxiliary state pruning. *(POC, MUST, settled)*  
When an application cache record’s protection or verification lifetime ends, the Bus Node shall remove that record within P-STO-2.  
*Verification.* test, expire each cache class and inspect its records after the pruning allowance.

**MPE-STO-036** Authorized tombstone deletion. *(PROD, MUST, open: DEC-STO-6)*  
Where the authorized tombstone feature is enabled, the Store Node shall remove the identified MPE Envelope from managed live storage within P-STO-14 after validating the tombstone.  
*Verification.* test, apply a valid OPS-authorized tombstone and inspect storage after its deadline.

**MPE-STO-037** Reject unauthorized deletion. *(POC, MUST, settled)*  
If an MPE Envelope deletion request fails the configured authorization policy, then the Store Node shall reject that request.  
*Verification.* test, submit forged, malformed and unauthorized deletion requests and confirm retained records remain intact.

**MPE-STO-038** Prevent tombstone reinsertion. *(PROD, MUST, open: DEC-STO-6)*  
Where the authorized tombstone feature is enabled, the Store Node shall reject reinsertion of a tombstoned MPE Envelope until its latest otherwise-authorized retention deadline has passed.  
*Verification.* test, replay deleted Envelopes through live ingress and archive ingestion before the applicable deadline.

**MPE-STO-039** Separate inclusion and storage evidence. *(POC, MUST, settled)*  
The MPE client library shall expose Anchor inclusion evidence separately from retention commitment evidence.  
*Verification.* test, supply an Anchor opening without retention receipts and confirm that inclusion does not imply the `stored` label.

**MPE-STO-040** Verification cache validity. *(POC, MUST, settled)*  
If an Admission Proof verification-cache entry no longer matches the applicable proof bytes, verifier version or Bus Registry context, then the Bus Node shall invalidate that entry.  
*Verification.* test, independently change proof bytes, verifier version and Bus Registry context and confirm fresh validation is required.

**MPE-STO-041** Inventory listing. *(POC, MUST, settled)*  
When a client requests an inventory for a Shard and time window, the Store Node shall return every retained MPE Envelope Identifier in that window in pages of at most P-PUB-9 entries.  
*Verification.* test, a seeded store of N identifiers returns exactly N across pages.

**MPE-STO-042** Retention receipt request. *(POC, MUST, open: DEC-STO-5)*  
When a client requests the retention receipts of a Shard window, the Store Node shall return a receipt for every MPE Envelope Identifier it retains in that window, each signed with its Bus Operator key over the identifier, the Shard and the retention deadline.  
*Verification.* test, request receipts from three Store Nodes and validate them under MPE-STO-012.


## A.10 Infrastructure actors, governance and operations (MPE-OPS) {#a10-ops}

**MPE-OPS-001** No validator duty. *(PROD, MUST, settled)*  
MPE shall assign no relay, store, anchoring or bootstrapping duty to a Midnight block-authoring node.  
*Verification.* test. On a testnet validator, a packet capture on the consensus port shows no MPE protocol id, and stopping every Bus Node leaves GRANDPA finality time unchanged (g2 Stage 1).

**MPE-OPS-002** Separate network identity. *Same obligation as MPE-NET-005, which owns it.*

**MPE-OPS-003** Separate bootstrap set. *Same obligation as MPE-NET-025, which owns it.*

**MPE-OPS-004** Bootstrapper profile. *Same obligation as MPE-NET-024, which owns it.*

**MPE-OPS-005** Role trust disclosure. *(PROD, MUST, settled)*  
MPE shall publish, before the first Bus Operator is admitted, a statement for each Bus Operator role of what that role observes and what it can withhold, delay or forge.  
*Verification.* inspection. Every role in the Glossary has a published statement.

**MPE-OPS-006** Content-blind roles. *(PROD, MUST, settled)*  
MPE shall define no Bus Operator role or governance role that holds a key able to open an MPE Envelope body.  
*Verification.* inspection of the role definitions and key inventory; analysis of the Bus Registry operations.

**MPE-OPS-007** Allow-listed mesh at launch. *(POC, MUST, open: DEC-OPS-1)*  
While the relay allow-list is active, the Bus Node shall accept GRAFT only from peers whose identity is on the Bus Registry relay list.  
*Verification.* test. A non-listed Prototype peer that sends GRAFT is pruned, while it can still publish as a non-mesh peer.

**MPE-OPS-008** Allow-list removal gate. *(PROD, MUST, open: DEC-OPS-1)*  
MPE shall keep the relay allow-list active until a red-team holding P-OPS-4 peer identities fails to push honest delivery below P-OPS-5 under the production scoring parameters.  
*Verification.* simulation and demonstration. A red-team run on the Stage 1 network with targeted placement at 1, 3 and 5 % (s3 D10).

**MPE-OPS-009** Launch Bus Operator count. *(PROD, MUST, open: DEC-OPS-6)*  
While the relay allow-list is active, MPE shall list relays run by at least P-OPS-1 independent organizations.  
*Verification.* inspection of the roster against Bus Operator attestations.

**MPE-OPS-010** Concentration cap. *(PROD, MUST, open: DEC-OPS-6)*  
MPE shall keep the share of listed relays run by any one organization at or below P-OPS-2.  
*Verification.* inspection of the roster each time the Bus Registry relay list changes.

**MPE-OPS-011** Gates counted per organization. *(PROD, MUST, settled)*  
MPE shall compute every decentralization-gate metric per verified organization, not per peer identity or bond key.  
*Verification.* inspection of the gate report method.

**MPE-OPS-012** Parameter time-lock. *(PROD, MUST, open: DEC-OPS-2)*  
When a Bus Registry parameter change is approved, the Bus Registry shall defer its effect by at least P-OPS-6.  
*Verification.* analysis using the Quint invariant I1 "no parameter takes effect before its delay" (o4), plus a devnet test.

**MPE-OPS-013** Emergency expiry. *(PROD, MUST, open: DEC-OPS-2)*  
If an emergency action is not ratified within P-OPS-7, then the Bus Registry shall restore the value in force before that action.  
*Verification.* analysis using the Quint invariant I2 (o4), plus a devnet test with no ratification.

**MPE-OPS-014** Exits survive a bus pause. *(PROD, MUST, open: DEC-OPS-2)*  
Where the Bus Registry holds Publisher deposits, while the bus pause flag is set, the Bus Registry shall accept withdrawal and slashing calls.  
*Verification.* analysis using the Quint invariant I3, plus a devnet test with the bus paused.

**MPE-OPS-015** No revocation by fiat. *(PROD, MUST, open: DEC-OPS-2)*  
The Bus Registry shall provide no governance operation that revokes a Publisher admission credential without misuse evidence checked by the Bus Registry circuit.  
*Verification.* inspection of the Bus Registry entry points; analysis that every removal path checks evidence.

**MPE-OPS-016** Maintenance notice. *(PROD, MUST, open: DEC-OPS-2)*  
When a Bus Registry maintenance update is prepared, MPE shall publish its full content at least P-OPS-8 before submitting it.  
*Verification.* inspection. The publication time of the notice precedes the transaction's block time by P-OPS-8.

**MPE-OPS-017** Measure maintenance constraints. *(PROD, MUST, settled)*  
MPE shall determine on a ledger-9 network, before Stage 2, whether a `ContractMaintenanceAuthority` can enforce a delay on verifier-key replacement.  
*Verification.* test on a devnet. Attempt a delayed maintenance update and record the outcome.

**MPE-OPS-018** Public governance events. *(PROD, MUST, settled)*  
When the Bus Registry applies a parameter change, pause, emergency action or relay ejection, the Bus Registry shall emit one `mip-xxxx:governance[v1]` `Misc` event whose payload is an action byte, a 2-byte reason code and a 32-byte subject, zero-filled.  
*Verification.* test. Each action type on a devnet produces one matching `Misc` in the `contractEvents` output.

**MPE-OPS-019** Steward diversity. *(PROD, MUST, open: DEC-OPS-2)*  
Where a steward set governs the Bus Registry, MPE shall seat no more than P-OPS-9 stewards from any one organization.  
*Verification.* inspection of the steward roster at every steward-set change.

**MPE-OPS-020** Governance end state. *(PROD, SHOULD, open: DEC-OPS-2)*  
When the open-admission stage exit review starts, MPE shall show that the Bus Registry maintenance authority has been transferred to Midnight federated governance or removed.  
*Verification.* inspection, read the Bus Registry's maintenance authority from ledger state.

**MPE-OPS-021** Overlay survives a chain pause. *Same obligation as MPE-NET-038, which owns it.*

**MPE-OPS-022** Stale view gives Ignore. *Same obligation as MPE-NET-018, which owns it.*

**MPE-OPS-023** Ejection takes effect. *(POC, MUST, settled)*  
When a relay is removed from the Bus Registry relay list, the Bus Node shall stop meshing with that relay within P-OPS-11.  
*Verification.* test. Remove a peer in the mock Bus Registry, then measure the time until no Prototype has it in any mesh.

**MPE-OPS-024** Evidence-only ejection when open. *(PROD, MUST, open: DEC-OPS-2)*  
While the relay allow-list is inactive, MPE shall eject a relay only on published evidence that P-OPS-16 independent monitors measured its canary delivery below P-OPS-5 for P-OPS-12, or on a malformed Anchor it signed.  
*Verification.* inspection, every ejection event references the monitor records and the threshold computation.

**MPE-OPS-025** Tombstone deletion. *Same obligation as MPE-STO-036, which owns it.*

**MPE-OPS-026** Tombstoned Envelope not relayed. *(PROD, SHOULD, open: DEC-OPS-5)*  
Where tombstones are enabled, when the Bus Node holds a valid tombstone for an MPE Envelope Identifier, the Bus Node shall Ignore that MPE Envelope.  
*Verification.* test, a replayed tombstoned Envelope is not forwarded and the sender's P4 term is unchanged.

**MPE-OPS-027** Transparency report. *(PROD, SHOULD, open: DEC-OPS-5)*  
MPE shall publish, every P-OPS-14, a report of the counts of tombstones, ejections, emergency actions and slashes in that period.  
*Verification.* inspection. The report counts match the Bus Registry events for the period.

**MPE-OPS-028** Abuse report on explicit action only. *(PROD, MUST, settled)*  
The MPE client library shall send an abuse report only on an explicit request by the receiving user.  
*Verification.* test. Paired clients with different interests emit identical traffic when no report is requested.

**MPE-OPS-029** No IP persistence. *Same obligation as MPE-SEC-027, which owns it.*

**MPE-OPS-030** Debug logging expires. *(POC, SHOULD, settled)*  
If debug logging is enabled on a Bus Node, then the Bus Node shall disable it after P-OPS-15.  
*Verification.* test using a simulated clock.

**MPE-OPS-031** Canary probes. *(PROD, SHOULD, open: DEC-OPS-4)*  
MPE shall run canary Publishers in every Shard from at least P-OPS-16 monitor organizations, each publishing one MPE Envelope per P-OPS-17.  
*Verification.* inspection of the monitor roster; demonstration from canary logs.

**MPE-OPS-032** Canaries look ordinary. *(PROD, SHOULD, open: DEC-OPS-4)*  
The MPE client library shall send canary MPE Envelopes through the same size classes and admission path as other MPE Envelopes.  
*Verification.* analysis. A classifier trained on relay-visible fields does no better than chance at telling canaries from other Envelopes.

**MPE-OPS-033a** Aggregated counter release. *(PROD, SHOULD, open: DEC-OPS-4)*  
Where Bus Node counters are published, the Bus Node shall release them only as aggregates computed across at least P-OPS-16 share keepers, none of which receives an individual Bus Node's counter value.  
*Verification.* inspection, review the counter-export path; test, capture share-keeper inputs and confirm each is a blinded share.

**MPE-OPS-033b** Differential-privacy budget for counters. *(PROD, SHOULD, open: DEC-OPS-4)*  
Where Bus Node counters are published, the Bus Node shall add noise that gives each published counter a differential-privacy epsilon of at most P-OPS-18.  
*Verification.* analysis, compute epsilon from the configured noise distribution and sensitivity; test, the noise sampler matches that distribution (KS test, p > 0.01).

**MPE-OPS-034** Multi-monitor decisions. *(PROD, MUST, open: DEC-OPS-4)*  
MPE shall base each relay ejection or Bus Operator payout on measurements from at least P-OPS-16 independent monitors.  
*Verification.* inspection of each ejection and payout record.

**MPE-OPS-035** Version overlap. *Same obligation as MPE-FMT-024, which owns it.*

**MPE-OPS-036** Version deny-list. *(POC, SHOULD, open: DEC-OPS-2)*  
When the Bus Node receives a version deny-list entry signed by the governance threshold, the Bus Node shall Ignore MPE Envelopes of that version.  
*Verification.* test. Envelopes of the denied version are dropped, and no peer's P₄ count changes.

**MPE-OPS-037** Relay key handover. *(PROD, SHOULD, settled)*  
The Bus Node shall support replacing its identity key through a handover signed by the old key and recorded in the Bus Registry relay list.  
*Verification.* test on a devnet. After the handover the new key is grafted and the old key is not.

**MPE-OPS-038** Signed reproducible releases. *(PROD, MUST, settled)*  
MPE shall publish each Bus Node release as a reproducible build signed by at least P-OPS-20 independent signers.  
*Verification.* test. Two independent rebuilds match the release hash bit for bit.

**MPE-OPS-039** Sev1 mitigation time. *(PROD, SHOULD, settled)*  
When an incident is classified Sev1, MPE shall publish a signed release or configuration change that removes the classified trigger within P-OPS-21.  
*Verification.* demonstration, timed drills at least twice per year; the drill's trigger no longer reproduces on the published artifact.

**MPE-OPS-040** Post-mortem. *(PROD, SHOULD, settled)*  
When a Sev1 or Sev2 incident is closed, MPE shall publish a post-mortem within P-OPS-27.  
*Verification.* inspection of the incident log against publication dates.

**MPE-OPS-041** Pause drill. *(PROD, MUST, settled)*  
MPE shall complete a bus pause-to-resume drill within P-OPS-22 before exiting Stage 1.  
*Verification.* demonstration on the Stage 1 network, with timestamps from the Bus Registry events.

**MPE-OPS-042** Gated stages. *(PROD, MUST, settled)*  
MPE shall not start a launch stage until every exit gate of the preceding stage has passed with published evidence.  
*Verification.* inspection of the gate record for each stage transition.

**MPE-OPS-043** Evidence freeze. *(PROD, MUST, settled)*  
When the Stage 0 exit review starts, MPE shall record the target network's ledger version, runtime `spec_version` and the pinned revision of every Midnight component the bus depends on.  
*Verification.* inspection, compare the claim register against a live RPC `spec_version` query.

**MPE-OPS-044** Ledger-generation gate. *(PROD, MUST, settled)*  
While the target network runs ledger 8, MPE shall make no production claim for a feature that needs ledger-9 contract events or cross-contract calls.  
*Verification.* inspection of the published feature claims against the network's ledger version; compilation confirms that the Bus Registry needs toolchain 0.33.0 or later only for `emit` and compiles with 0.31.1 without Anchors and governance events.

**MPE-OPS-045** Prototype on a mock adapter. *Same obligation as MPE-NET-035, which owns it.*

**MPE-OPS-046** Measured Bus Registry costs. *Same obligation as MPE-VER-030, which owns it.*

**MPE-OPS-047** Scoring-CVE release gate. *Same obligation as MPE-VER-026, which owns it.*

**MPE-OPS-048** Audit gate. *(PROD, MUST, settled)*  
MPE shall not deactivate the relay allow-list while an independent audit of the Bus Node parser, admission check or Bus Registry has an open critical or high finding.  
*Verification.* inspection of the audit report status.

**MPE-OPS-049** Permissioned-stage exit. *Same obligation as MPE-VER-038, which owns it.*

**MPE-OPS-050** Counsel-memo gate. *(PROD, SHOULD, open: DEC-OPS-5)*  
MPE shall not admit a Bus Operator in a jurisdiction without a counsel memo on the liability of relaying ciphertext in that jurisdiction.  
*Verification.* inspection. One memo on file for each roster jurisdiction.

**MPE-OPS-051** Funding gate. *(PROD, MUST, open: DEC-OPS-3)*  
MPE shall not leave the permissioned-overlay stage without written funding commitments covering every launch Bus Operator role for P-OPS-24.  
*Verification.* inspection of the signed commitments against the roster.

**MPE-OPS-052** Anonymity-claim gate. *(PROD, MUST, settled)*  
MPE shall publish no broadcast anonymity-set claim while organic load is below P-OPS-25 or distinct active publisher admissions number fewer than P-OPS-26.  
*Verification.* inspection of published claims against aggregated load (MPE-OPS-033) and Bus Registry counts.

**MPE-OPS-053** Course-change register. *(PROD, MUST, settled)*  
MPE shall maintain a register in which each course-change trigger has a measurable threshold and a named response.  
*Verification.* inspection. Every trigger has a numeric threshold and a response.

**MPE-OPS-054** Launch sequencing. *(PROD, SHOULD, open: DEC-OPS-7)*  
While no ledger-9 mainnet activation date precedes the Stage 1 start date, MPE shall run Stage 1 as a permissioned overlay whose Ledger Adapter targets a ledger-9 devnet.  
*Verification.* inspection of the Stage 1 deployment against the network's ledger version.

**MPE-OPS-055** Mock Bus Operator roster. *(POC, MUST, settled)*  
The Prototype shall register its local Bus Nodes and Store Nodes in the mock Bus Registry relay list under at least P-STO-5 distinct Bus Operator organization identifiers.  
*Verification.* inspection of the fixture; test, the `stored` attribute and reconciliation run on it.

**MPE-OPS-056** Toolchain and ledger versions named. *(PROD, MUST, settled)*  
MPE shall state, in each MIP version, the Compact toolchain, language, runtime and ledger versions used to build the Bus Registry, ledger-lane and consumer circuits.  
*Verification.* inspection of the MIP against the build logs.


## A.11 Privacy properties and leakage (MPE-PRV) {#a11-prv}

PRV owns D2: named privacy properties, adversary definitions, permitted leakage, explicit non-claims, and the evidence required for each claim.
Launch claims are conditional content confidentiality, sealed stream-label confidentiality, and subscriber-interest privacy within a completely received Shard.
Shard membership, participation, ingress identity, timing, volume, admission metadata, and public application effects remain observable.
Launch provides no general publisher anonymity, timing privacy, volume privacy, or relationship privacy.
Cryptographic content protection can hold against a global observer without providing global-observer anonymity.

**MPE-PRV-001** Claim register. *(PROD, MUST, settled)*  
The MPE shall maintain a claim register assigning each privacy claim its game, adversary classes, assumptions, permitted leakage, supporting evidence, verification procedure, and applicable profile.  
*Verification.* inspection, check every advertised claim against the required register fields.

**MPE-PRV-002** Content confidentiality. *(PROD, MUST, settled)*  
The MPE shall provide computational indistinguishability in the Content Game against R, C, G, and A adversaries lacking challenge decryption secrets.  
*Verification.* analysis, review the selected construction's reduction and its implementation assumptions against the complete Content Game.

**MPE-PRV-003** Sealed logical labels. *Same obligation as MPE-FMT-003, which owns it.*

**MPE-PRV-004** Recipient-key-hiding claim gate. *(PROD, MUST, open: DEC-PRV-3)*  
The MPE shall withhold a recipient-key-hiding claim until reviewed analysis establishes the selected wrapper's key privacy against adversaries knowing candidate recipient public keys.  
*Verification.* analysis, inspect the wrapper's key-privacy game, reduction, public fields, and recognition interfaces.

**MPE-PRV-005** Length concealment within a class. *Same obligation as MPE-FMT-013, which owns it.*

**MPE-PRV-006** Conditional subscriber-interest privacy. *(POC, MUST, open: DEC-PRV-1)*  
While the Subscriber uses the private reception profile, the MPE client library shall satisfy the Selection Game within its received Shard set.  
*Verification.* test, compare paired executions with different interests under identical transport inputs and schedules.

**MPE-PRV-007** Local recognition secrets. *(POC, MUST, open: DEC-PRV-1)*  
While the Subscriber uses the private reception profile, the MPE client library shall retain its Message decryption, stream, recognition, and wallet viewing secrets within the Subscriber's trusted endpoint boundary.  
*Verification.* inspection, trace secret-bearing values through outbound requests, provider APIs, configuration, and remote diagnostics.  
*Note.* This excludes, by design, the per-wallet relevance and session-decryption model that MPS-0005 plans for the Indexer.

**MPE-PRV-008** No private selection predicates. *Same obligation as MPE-PUB-010, which owns it.*

**MPE-PRV-009** Recognition-independent transport. *Same obligation as MPE-PUB-012, which owns it.*

**MPE-PRV-010** No recognition acknowledgements. *Same obligation as MPE-CON-039, which owns it.*

**MPE-PRV-011** Explicit application reactions. *Same obligation as MPE-PUB-047, which owns it.*

**MPE-PRV-012** Overload preserves the privacy boundary. *Same obligation as MPE-PRV-013, which owns it.*

**MPE-PRV-013** Explicit privacy-changing fallback. *(POC, MUST, settled)*  
If a fallback changes the applicable leakage contract, then the MPE client library shall block its activation until the application explicitly selects the changed profile.  
*Verification.* test, disable the primary path and confirm that a path with different leakage remains inactive without profile selection.

**MPE-PRV-014** Recognition-free remote diagnostics. *(POC, MUST, settled)*  
While the Subscriber uses the private reception profile, the MPE client library shall exclude private interest sets and recognition outcomes from remotely exported diagnostics.  
*Verification.* test, inspect exported diagnostics across paired interest sets, including malformed matched Messages and local errors.

**MPE-PRV-015** Explicit plaintext disclosure. *(POC, MUST, settled)*  
When an application requests disclosure of Message plaintext outside its authorized audience, the MPE client library shall require explicit application authorization for that disclosure.  
*Verification.* test, exercise ledger submission and reporting paths and confirm that recognition does not authorize plaintext export.

**MPE-PRV-016** Bus Node leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-R in every applicable privacy profile's leakage declaration.  
*Verification.* inspection, reconcile L-R with serialized fields and instrumented ingress, subscription, and forwarding observations.

**MPE-PRV-017** Store Node leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-S in every applicable privacy profile's leakage declaration.  
*Verification.* inspection, reconcile L-S with live, reconnect, back-fill, and repair request traces.

**MPE-PRV-018** Admission issuer leakage declaration. *(POC, MUST, settled)*  
Where admission issuance is present, the MPE shall include L-U in the applicable privacy profile's leakage declaration.  
*Verification.* inspection, inventory issuer inputs and linkable records for the selected admission mechanism.

**MPE-PRV-019** Indexer leakage declaration. *(POC, MUST, settled)*  
Where an Indexer read path is present, the MPE shall include L-X in the applicable privacy profile's leakage declaration.  
*Verification.* inspection, enumerate GraphQL arguments and supplied secrets for each enabled Indexer path.

**MPE-PRV-020** Ledger leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-L in every applicable privacy profile's leakage declaration.  
*Verification.* inspection, enumerate public fields of registration, admission, Anchor, ledger-lane, and consumption transactions.

**MPE-PRV-021** Collusion leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-C in every applicable privacy profile's leakage declaration.  
*Verification.* analysis, join issuer, ingress, retrieval, and ledger records and document available correlations.

**MPE-PRV-022** Global-observer leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-G in every applicable privacy profile's leakage declaration.  
*Verification.* inspection, compare the declaration with a simulated global observer's traffic and public-action records.

**MPE-PRV-023** Insider leakage declaration. *(POC, MUST, settled)*  
The MPE shall include L-I in every applicable privacy profile's leakage declaration.  
*Verification.* demonstration, show authorized recognition and plaintext export without treating either as a confidentiality violation.

**MPE-PRV-024** Launch metadata non-claims. *(POC, MUST, settled)*  
The MPE shall label publisher-message unlinkability, general recipient-message unlinkability, relationship privacy, timing privacy, volume privacy, and hidden participation as unclaimed by the launch profile.  
*Verification.* inspection, check profile descriptions, API privacy labels, demonstrations, and claim-register entries for these explicit exclusions.

**MPE-PRV-025** No anonymity from unsigned transactions. *(POC, MUST, settled)*  
The MPE shall describe the absence of a Substrate signer as a ledger-interface fact without presenting it as proof of publisher or payer unlinkability.  
*Verification.* inspection, check ledger privacy descriptions against L-L and their supporting code facts.

**MPE-PRV-026** Launch compromise-security posture. *(POC, MUST, open: DEC-PRV-4)*  
The MPE shall label content forward secrecy, metadata forward secrecy, and post-compromise security as unclaimed by the launch bus profile.  
*Verification.* inspection, confirm that profile labels expose the consequences of later key compromise and retained historical keys.

**MPE-PRV-027** No launch post-quantum claim. *(POC, MUST, settled)*  
The MPE shall label post-quantum confidentiality as unclaimed by the launch profile.  
*Verification.* inspection, check claim-register exclusions against the selected payload and ledger cryptographic dependencies.

**MPE-PRV-028** No adversarial archive-erasure claim. *(POC, MUST, settled)*  
The MPE shall describe MPE Envelope expiry as an honest-service retention rule without claiming deletion from adversarial archives.  
*Verification.* demonstration, retain a captured Envelope beyond expiry and verify that privacy documentation acknowledges the remaining copy.

**MPE-PRV-029** No inherited stem anonymity. *(POC, MUST, settled)*  
Where stem forwarding is present, the MPE shall label its source-attribution effect as an unproved heuristic unless analysis covers the implemented construction and adversary.  
*Verification.* inspection, check every stem claim against the actual routing graph, adversary, traffic policy, and cited theorem.

**MPE-PRV-030** Evidence before advertising a property. *(PROD, MUST, settled)*  
When a privacy property is advertised as provided, the MPE shall supply reviewed evidence establishing that property's registered game for the implemented profile.  
*Verification.* analysis, audit the claim-to-construction mapping and reject evidence that omits an interface or adversary capability.

**MPE-PRV-031** Paired selection verification. *Same obligation as MPE-VER-028, which owns it.*

**MPE-PRV-032** Active selection verification. *Same obligation as MPE-VER-028, which owns it.*

**MPE-PRV-033** Attribution measurements. *Same obligation as MPE-VER-027, which owns it.*

**MPE-PRV-034** Bound applicability. *(PROD, MUST, settled)*  
When literature supplies a quantitative privacy bound, the MPE shall document the mapping from that bound's assumptions and variables to the implemented profile before using it as an MPE guarantee.  
*Verification.* analysis, inspect model, graph, observation, traffic, and variable mappings; reject unsupported substitutions.

**MPE-PRV-035** Violated-claim withdrawal. *(PROD, MUST, settled)*  
If verification demonstrates a violation of an advertised privacy game, then the MPE shall mark that profile's affected claim as unsupported.  
*Verification.* demonstration, introduce a known recognition leak and confirm that the affected claim fails the release evidence check.

**MPE-PRV-036** Unknown leakage inventory. *(POC, MUST, settled)*  
When a proposed interface has unresolved privacy-relevant fields, the Prototype shall produce an observation inventory from that interface before the associated profile is accepted.  
*Verification.* inspection, reconcile packet captures, API arguments, public ledger fields, and remote diagnostics with the profile's leakage declaration.

**MPE-PRV-037** Separate stronger-profile evidence. *(PROD, MUST, settled)*  
Where a stronger privacy profile is present, the MPE shall maintain a separate claim register for its implemented composition.  
*Verification.* inspection, confirm that experimental results and component guarantees are confined to the separately analyzed profile.

**MPE-PRV-038** Anchor count leakage. *(POC, MUST, settled)*  
The MPE shall include the per-Shard MPE Envelope counts published in Anchors in the L-L leakage declaration.  
*Verification.* inspection, L-L names the count fields and their window granularity.

**MPE-PRV-039** Per-Message disclosure object. *(PROD, MUST, open)*  
When an application discloses one Message to a named reader, the MPE client library shall produce a disclosure object holding the MPE Envelope, its per-Envelope encryption key, the Publisher's verifying key, the Anchor inclusion path and the discloser's signature over the object.  
*Verification.* test: the reader opens exactly the disclosed Envelope, checks the Publisher's signature, recomputes its MPE Envelope Identifier against the Anchor and learns who disclosed it; the key opens no other Envelope of the stream.

**MPE-PRV-040** Per-period disclosure object. *(PROD, MUST, open)*  
When an application discloses one stream for a stated period to a named reader, the MPE client library shall produce a signed disclosure object that opens only that stream's Messages within that period.  
*Verification.* test: Messages of the stream before and after the period, and of other streams, do not open.

**MPE-PRV-041** Disclosures verified against Anchors. *(PROD, MUST, open)*  
When a reader verifies a disclosure object, the MPE client library shall accept a disclosed Message only if its MPE Envelope Identifier verifies under an Anchor in Bus Registry state at a finalized block.  
*Verification.* test: a disclosure object with a forged inclusion path or an unanchored Message is refused.

**MPE-PRV-042** Disclosure lifetime. *(PROD, MUST, open)*  
The MPE client library shall include in every disclosure object an expiry time after which its verification fails.  
*Verification.* test: verification succeeds before and fails after the stated expiry.

**MPE-PRV-043** Selective-disclosure goals mapped. *(PROD, MUST, settled)*  
MPE shall publish a mapping of each MPS-0043 selective-disclosure goal, 1 to 5, to a requirement or to an explicit non-claim.  
*Verification.* inspection: every goal has a row; the leakage declaration states that handing over a stream secret is a coarse, irrevocable viewing capability.

**MPE-PRV-044** Identify leakage declared. *(PROD, MUST, settled)*  
Where a Bus Node enables the libp2p Identify protocol, MPE shall list Identify's public key, addresses, supported protocols and implementation metadata as permitted leakage.  
*Verification.* inspection of the deployment configuration against the leakage declaration.


## A.12 Threats, abuse resistance and failure handling (MPE-SEC) {#a12-sec}

SEC specifies defenses against network capture, resource exhaustion, replay, censorship, hostile infrastructure, compromised keys and malicious inputs.
It covers attack responses in the Prototype and production targets, including failures that must not penalize honest peers.
Contract invariants apply to MPE’s supplied consumption integration; arbitrary application contracts remain outside MPE’s enforceable boundary.
Launch claims remain content confidentiality and interest-hiding from infrastructure, with visible Shard membership; global-observer resistance, timing privacy and relationship privacy are not promised.
Admission economics, cryptographic constructions, retention periods, governance authority and delivery SLOs belong to the corresponding areas.

**MPE-SEC-001** Launch relay admission. *Same obligation as MPE-OPS-007, which owns it.*

**MPE-SEC-002** Bootstrap source diversity. *Same obligation as MPE-NET-026, which owns it.*

**MPE-SEC-003** Outbound connection protection. *Same obligation as MPE-NET-011, which owns it.*

**MPE-SEC-004** Active peer scoring. *Same obligation as MPE-NET-008, which owns it.*

**MPE-SEC-005** Admission before forwarding. *(POC, MUST, settled)*  
The Bus Node shall forward an MPE Envelope's payload only after validating its Admission Proof against the authorized network, admission window, Shard, size class, expiry, proof-independent MPE Envelope Identifier and publication allowance.  
*Verification.* test, mutate each bound field independently and confirm no forwarding; inspect that application validation precedes GossipSub acceptance.

**MPE-SEC-006** Cheap framing checks. *Same obligation as MPE-FMT-009, which owns it.*

**MPE-SEC-007** Rejection of proven invalidity. *Same obligation as MPE-NET-016, which owns it.*

**MPE-SEC-008** Ignore local uncertainty. *Same obligation as MPE-NET-018, which owns it.*

**MPE-SEC-009** Verification backlog bounds. *(POC, MUST, open: DEC-SEC-3)*  
The Bus Node shall limit outstanding verification work to P-SEC-3 jobs per peer within a total of P-SEC-4 jobs.  
*Verification.* test, flood through existing and newly created connections and confirm both bounds include executing jobs.

**MPE-SEC-010** Verification scheduling fairness. *(POC, MUST, open: DEC-SEC-3)*  
While multiple peer verification queues remain nonempty, the Bus Node shall dispatch jobs by round-robin peer selection.  
*Verification.* test, keep attacker queues saturated and confirm each continuously nonempty peer queue receives a dispatch opportunity in every scheduling round.

**MPE-SEC-011** Retrieval abuse limits. *(POC, MUST, settled)*  
If a retrieval request would exceed a configured retrieval byte, request or concurrency budget, then the Store Node shall refuse that request with ResourceExhausted.  
*Verification.* test, exceed each STO/PRF retrieval budget using oversized intervals, parallel requests and repeated requests; confirm refusal before excess resource commitment.

**MPE-SEC-012** Storage exhaustion response. *Same obligation as MPE-STO-009, which owns it.*

**MPE-SEC-013** Historical admission separation. *(POC, MUST, settled)*  
When serving retained MPE Envelopes through back-fill, the Store Node shall validate admission using the historical Bus Registry snapshot applicable to each MPE Envelope.  
*Verification.* test, retrieve an historically valid Envelope after its admission window closes and confirm historical validation consumes no new allowance.

**MPE-SEC-014** Proof-independent deduplication. *(POC, MUST, settled)*  
The Bus Node shall treat alternative valid Admission Proof serializations for the same proof-independent MPE Envelope identifier as duplicate publication.  
*Verification.* test, supply alternative valid proof representations for an identical authenticated Envelope representation and confirm only the initial publication is accepted.

**MPE-SEC-015** Optional durable admission replay state. *(PROD, MAY, settled)*  
Where durable replay state is configured, the Bus Node shall commit each consumed publication allowance to durable storage before forwarding its MPE Envelope.  
*Verification.* test, interrupt at the persistence and forwarding boundaries, restart, and replay the admitted Envelope.

**MPE-SEC-016** Missing replay-state recovery. *Same obligation as MPE-STO-015, which owns it.*

**MPE-SEC-017** Replay-state pruning boundary. *Same obligation as MPE-ECO-021, which owns it.*

**MPE-SEC-018** Conflicting allowance use. *(POC, MUST, open: DEC-SEC-4)*  
If a valid MPE Envelope conflicts with an already consumed publication allowance, then the Bus Node shall classify that later MPE Envelope as GossipSub Ignore.  
*Verification.* simulation, spend an allowance on distinct signed Envelopes in separate partitions, reconnect, and confirm each node refuses subsequent conflicting acceptance without P₄ framing.

**MPE-SEC-019** Conflict alarm. *(POC, MUST, open: DEC-SEC-4)*  
When it verifies conflicting MPE Envelopes authorized by the same publication allowance, the Bus Node shall emit an AdmissionConflict diagnostic containing their identifiers and the applicable authorization reference.  
*Verification.* test, distinguish valid equivocation from invalid proofs and confirm diagnostics use bounded records containing no plaintext or secret keys.

**MPE-SEC-020** Authenticated key changes. *(POC, MUST, settled)*  
If a discovery service presents a replacement for a pinned Publisher key without an authenticated change authorization, then the MPE client library shall reject that replacement.  
*Verification.* test, replace invitation and discovery keys through a hostile service and confirm the pinned identity remains authoritative.

**MPE-SEC-021** Independent retrieval comparison. *Same obligation as MPE-PUB-014, which owns it.*

**MPE-SEC-022** Authenticate Bus Registry read results. *(POC, MUST, settled)*  
If an Indexer result is not confirmed by Bus Registry state read from P-NET-14 independent chain sources at a finalized block, then the Indexer adapter shall exclude it from admission, Anchor verification and `final` labelling.  
*Verification.* test, substitute contract addresses, invent Anchors, emit a `Misc` Anchor notification without matching Bus Registry state and alter Bus Registry data at one source; no authorization or `final` label derives from them.

**MPE-SEC-023** Recognition-independent omission repair. *Same obligation as MPE-PUB-015, which owns it.*

**MPE-SEC-024** Report unresolved retrieval. *(POC, MUST, settled)*  
If inventory comparison is unavailable, an authenticated sequence gap remains or requested repair fails, then the MPE client library shall report the affected retrieval interval as Unresolved.  
*Verification.* test, remove a comparison source, withhold an interior sequence item and fail a repair request; confirm no complete-delivery assertion appears.

**MPE-SEC-025** Recognition-independent network behavior. *Same obligation as MPE-PUB-012, which owns it.*

**MPE-SEC-026** Prevent silent privacy fallback. *Same obligation as MPE-PRV-013, which owns it.*

**MPE-SEC-027** Persistent logging limits. *(PROD, MUST, settled)*  
The Bus Node shall exclude client IP addresses, Recognition Tags and per-client activity histories from persistent logs.  
*Verification.* inspection, exercise normal operation, malformed traffic, admission conflicts and overload; inspect persisted application logs for prohibited fields.

**MPE-SEC-028** Compromised-key send suspension. *(POC, MUST, settled)*  
If a caller marks an active publishing or session key as compromised, then the MPE client library shall refuse publications using that key until authenticated replacement state is installed.  
*Verification.* test, mark each active key compromised, attempt publication, and confirm an unauthenticated service-supplied replacement cannot lift suspension.

**MPE-SEC-029** Admission-key separation. *Same obligation as MPE-ECO-006, which owns it.*

**MPE-SEC-030** Authentication before session mutation. *Same obligation as MPE-CRY-023, which owns it.*

**MPE-SEC-031** Missing session-update response. *(PROD, MUST, settled)*  
Where ratcheted sessions are present, if authenticated session state identifies a required key update as missing, then the MPE client library shall refuse sensitive publications dependent on that update with SessionUpdateRequired.  
*Verification.* test, suppress required updates while delivering application traffic and confirm affected sends remain suspended until the authenticated update is applied.

**MPE-SEC-032** Payload execution boundary. *(POC, MUST, settled)*  
The MPE client library shall require explicit Consumer authorization before initiating any download or executing any command requested by Message payload data.  
*Verification.* test, deliver authenticated payloads containing executable expressions, command strings and external references; confirm decoding alone produces no corresponding side effect.

**MPE-SEC-033** Unwanted-contact rejection. *(POC, MUST, settled)*  
If an authenticated Publisher is denied by the Subscriber’s configured contact policy, then the MPE client library shall suppress delivery of that Publisher’s Message to the Consumer.  
*Verification.* test, apply allow and deny policies to authenticated Messages and confirm denied Messages cause no Consumer callback or recognition-dependent infrastructure response.

**MPE-SEC-034** Authenticated tombstone deletion. *Same obligation as MPE-STO-036, which owns it.*

**MPE-SEC-035** Delivery during ledger interruption. *Same obligation as MPE-NET-038, which owns it.*

**MPE-SEC-036** Ledger-dependent failure reporting. *Same obligation as MPE-CON-050, which owns it.*

**MPE-SEC-037** Contract authorization predicate. *Same obligation as MPE-CON-043, which owns it.*

**MPE-SEC-038** Atomic contract replay protection. *Same obligation as MPE-CON-044a and MPE-CON-044b, which own it together.*

**MPE-SEC-039** Configuration-specific attack evidence. *(POC, MUST, settled)*  
The Prototype shall produce an attack report for every SEC test-matrix case, recording configuration, attacker placement, controlled resources, delivery ratio, latency percentiles, eclipse duration, peak resource use and unauthorized or duplicate effects.  
*Verification.* inspection, check that every matrix case has reproducible inputs and measured results; absent measurements must be recorded as unknown.

**MPE-SEC-040** Scoring vulnerability release gate. *Same obligation as MPE-VER-026, which owns it.*

**MPE-SEC-041** Seen-set entry after Accept. *(POC, MUST, settled)*  
The Bus Node shall insert an MPE Envelope Identifier into its application seen-set only after its validator returns Accept for an MPE Envelope carrying that identifier.  
*Verification.* test, a Rejected corrupted-slot copy followed by the valid copy: the valid copy is accepted.

**MPE-SEC-042** Corrupted-slot front-running test. *(POC, MUST, settled)*  
The Prototype shall deliver an honest MPE Envelope to every eligible Subscriber within P-VER-6 when an adversarial peer injects copies of its Sealed Body with corrupted Admission Slots ahead of it.  
*Verification.* test, on the 32-node topology with the adversary adjacent to the publisher's ingress Bus Node.


## A.13 Verification and prototype acceptance (MPE-VER) {#a13-ver}

VER defines the evidence, test suites, stage gates and acceptance reports required for the Rust Prototype and subsequent MPE releases.
It covers local multi-node demonstrations, bounded models, simulations, adversarial workloads, Midnight integration and production acceptance.
It verifies the behavior specified by other areas without selecting their cryptographic, admission, storage or mesh designs.
A passing experiment supports only its recorded configuration, workload and adversary model.
D10 remains open where proposals disagree; the recommended defaults below govern Prototype acceptance pending review.

**MPE-VER-001** Reproducible acceptance profile. *(POC, MUST, settled)*  
The Prototype shall attach a reproducible acceptance profile to every acceptance run.  
*Verification.* inspection, check source revisions, dependency lock, build flags, hardware, topology, transport, mesh/scoring configuration, workload, parameter values, random seeds, clock policy, commands and fixture hashes.

**MPE-VER-002** Claim register. *Same obligation as MPE-PRV-001, which owns it.*

**MPE-VER-003** Failed stage gate. *(POC, MUST, open: DEC-VER-1)*  
If a mandatory stage check fails or lacks evidence, then the Prototype shall mark that stage gate as failed.  
*Verification.* test, inject failed, skipped, missing and timed-out mandatory checks; confirm none produces a passing gate.

**MPE-VER-004** Wire conformance. *(POC, MUST, settled)*  
The Prototype shall pass the frozen MPE Envelope conformance suite before multi-node acceptance.  
*Verification.* test, compare exact expected outcomes for valid vectors, incorrect lengths, unsupported versions, non-canonical encodings, malformed fields and applicable padding violations; include cross-implementation vectors supplied by FMT and CRY.

**MPE-VER-005** Decoder fuzzing. *(POC, MUST, open: DEC-VER-3)*  
The Prototype shall complete P-VER-14 fuzz iterations without a crash in the MPE Envelope and application-payload decoders.  
*Verification.* test, retain campaign configuration, iteration counts, sanitizer results and regression corpus; count only executions reaching a decoder, with coverage reported separately.

**MPE-VER-006** Actual cryptographic costs. *Same obligation as MPE-CRY-036, which owns it.*

**MPE-VER-007** Admission model. *(POC, MUST, open: DEC-VER-4)*  
The Prototype shall pass bounded exploration of the selected admission state machine without a violation of its frozen safety invariants.  
*Verification.* analysis, explore allowance boundaries, root replacement, expiry, revocation, restart, rollback and conflicting bodies; check message binding, scoped replay rules and absence of allowance resets.

**MPE-VER-008** Delivery-state model. *(POC, MUST, settled)*  
The Prototype shall pass bounded exploration of the client delivery state machine without a violation of its frozen cursor and deduplication invariants.  
*Verification.* analysis, explore inclusive cursors, crash points, reconnect, failover, withheld suffixes and gap closure; check that committed progress never skips an undelivered recoverable Message.

**MPE-VER-009** Contract-consumption model. *(POC, MUST, settled)*  
The Prototype shall pass bounded exploration of the contract-consumption model without an unauthorized or duplicate contract effect.  
*Verification.* analysis, explore incorrect leaves, destinations, networks, expiry, missing Anchors, replay-state pruning and concurrent consumption; model the CON authorization predicate explicitly.

**MPE-VER-010** Governance model gate. *(PROD, MUST, open: DEC-VER-4)*  
Where Bus Registry governance features are present, MPE shall pass bounded exploration of their frozen governance invariants before production acceptance.  
*Verification.* analysis, check applicable delayed changes, emergency expiry, threshold transitions, pause states, Anchor takeover and fund-conservation rules; record disabled features explicitly.

**MPE-VER-011** Local multi-node demonstration. *(POC, MUST, open: DEC-VER-1)*  
The Prototype shall demonstrate Publisher-to-Subscriber Message delivery through P-VER-1 separate local Bus Node processes using rust-libp2p GossipSub under the v1.2 profile.  
*Verification.* demonstration, publish every selected Envelope class across tested Shards; confirm matching Subscribers recover exact Messages and nonmatching Subscribers produce no false opens; use a declared mock Ledger Adapter.

**MPE-VER-012** Nominal soak. *(POC, MUST, open: DEC-VER-2)*  
The Prototype shall complete a nominal acceptance run at P-VER-2 for P-VER-3 without an unplanned process termination.  
*Verification.* test, use the local multi-node topology, real elapsed time and frozen Envelope mix; report offered, admitted and rejected rates separately.

**MPE-VER-013** Nominal latency. *(POC, MUST, open: DEC-VER-2)*  
While the nominal acceptance workload is running, the Prototype shall achieve a post-admission delivery p99 no greater than P-VER-6.  
*Verification.* test, measure first valid delivery for each expected Subscriber; publish the completion percentile and missing-delivery count under the measurement convention below.

**MPE-VER-014** Nominal delivery fraction. *(POC, MUST, open: DEC-VER-2)*  
While the nominal acceptance workload is running, the Prototype shall deliver at least P-VER-7 of eligible MPE Envelope–Subscriber pairs within P-VER-6 after admission.  
*Verification.* test, derive the denominator from generated accepted Envelopes and scheduled honest Subscribers; count each pair once, including pairs that never complete.

**MPE-VER-015** Resource acceptance. *(POC, MUST, settled)*  
If a measured resource exceeds its frozen PRF or STO acceptance ceiling, then the Prototype shall fail resource acceptance.  
*Verification.* test, check CPU, memory, ingress, egress, queue/cache occupancy, retained bytes, storage amplification and recognition cost against declared ceilings; an undefined ceiling yields an incomplete gate.

**MPE-VER-016** Measurement report. *(POC, MUST, settled)*  
When an acceptance run ends, the Prototype shall produce a measurement report using the measurement convention below.  
*Verification.* inspection, check latency distributions, admission outcomes, delivery coverage, transport amplification, resource time series, recovery results and raw artifact references.

**MPE-VER-017** Scale simulations. *(POC, MUST, open: DEC-VER-2)*  
The Prototype shall produce scale-evaluation results at every Bus Node count in P-VER-8.  
*Verification.* simulation, exercise nominal load, P-VER-9 for P-VER-10, bursts, cold starts and overload; incorporate measured validation delay and the NET topology; disclose simulator limitations and compare overlapping cases with the real binary.

**MPE-VER-018** Adversarial dissemination gate. *(POC, MUST, open: DEC-VER-2)*  
While a non-partitioned adversarial acceptance run is active, the Prototype shall achieve a timely honest delivery fraction of at least P-VER-25 within P-VER-6.  
*Verification.* simulation, use P-VER-11 shares at each P-VER-8 size; test targeted outbound placement, poisoned discovery, Sybil-heavy joining, selective dropping, concentrated bandwidth and synchronized Publishers; report every case separately.

**MPE-VER-019** Admission abuse gate. *(POC, MUST, settled)*  
The Prototype shall accept zero publications violating the selected admission policy during an attack using P-VER-16 admission identities.  
*Verification.* test, submit over-quota, forged, expired, wrong-network, revoked and conflicting-body publications across admission window boundaries and restarts; account for valid aggregate allowances separately.

**MPE-VER-020** Validation outcome conformance. *(POC, MUST, settled)*  
The Prototype shall pass the validation outcome suite for the frozen Accept, Reject and Ignore policy.  
*Verification.* test, compare forwarding and score effects with the selected policy; include validation timeout and cache eviction; verify application validation is enabled because the inspected configuration defaults to automatic forwarding.

**MPE-VER-021** Invalid-ingress bounds. *(POC, MUST, settled)*  
While invalid-ingress saturation is active, the Prototype shall keep each queue and cache within its declared capacity.  
*Verification.* test, saturate malformed frames, invalid Admission Proofs, repeated identifiers and control traffic; sample capacities and memory through overload and recovery; report verification CPU separately.

**MPE-VER-022** Burst recovery. *(POC, MUST, open: DEC-VER-2)*  
When a P-VER-4 burst lasting P-VER-5 ends, the Prototype shall restore every monitored queue to its pre-burst nominal bound within P-VER-15.  
*Verification.* test, establish bounds during a stable nominal interval before the burst; continue nominal load afterward and measure the first sustained return within those bounds.

**MPE-VER-023** Recovery completeness. *(POC, MUST, settled)*  
The Prototype shall recover every eligible Message in the P-VER-13 recovery chaos workload.  
*Verification.* test, inject client crashes, Bus Node and Store Node restarts, partitions and Indexer failover where present; compare the recovered Message set after recovery with the authoritative fixture set.

**MPE-VER-024** Atomic consumer deduplication. *(POC, MUST, settled)*  
Where an atomic effect store is present, the Prototype shall produce at most one committed handler effect per Message in the recovery chaos workload.  
*Verification.* test, crash between receive, effect commit and cursor commit; inject replay through overlay, back-fill and the ledger lane; count committed effects independently of callback attempts.

**MPE-VER-025** Store failure recovery. *(POC, MUST, settled)*  
When one Store Node fails while another honest holder remains reachable, the Prototype shall recover all requested eligible MPE Envelopes within the selected retention window.  
*Verification.* test, fail the initially selected Store Node, back-fill from another holder and compare identifiers and bytes; repeat near expiry and report unavailable expired ranges.

**MPE-VER-026** Scoring attack regression. *(POC, MUST, settled)*  
The Prototype shall fail network acceptance if the selected GossipSub scoring configuration reproduces a registered scoring safety violation.  
*Verification.* test, register the relevant CVE-2022-47547 attack traces and MPE-specific score counterexamples; exercise multi-Shard reward/penalty interactions, targeted dropping and the NET outbound-quota policy.

**MPE-VER-027** First-spy measurement. *(POC, MUST, open: DEC-VER-5)*  
The Prototype shall report first-spy precision and recall for every coalition share in P-VER-12.  
*Verification.* simulation, compare direct publication with any selected ingress mechanism on identical workloads; report topology, placement, load, estimator, sample counts and uncertainty, including idle and targeted cases.

**MPE-VER-028** Interest-swapped executions. *(POC, MUST, settled)*  
The Prototype shall produce identical infrastructure-visible retrieval traces for paired executions differing only in Subscriber interests under identical connection and retrieval schedules.  
*Verification.* test, compare requests, cursors, requested ranges, volumes and scheduled timing; include malformed matching Envelopes, withheld suffixes, reconnect, repair, acknowledgements and backpressure.

**MPE-VER-029** Infrastructure log audit. *(POC, MUST, settled)*  
The Prototype shall pass a log audit with zero occurrences of fixture Message plaintext in Bus Node or Store Node logs.  
*Verification.* test, publish unique plaintext canaries, trigger parsing, validation and storage errors, then scan logs and diagnostic exports; CRY and PRV separately define secret-field exclusions.

**MPE-VER-030** Ledger integration measurements. *(POC, MUST, settled)*  
The Prototype shall report measured transaction costs and timing for each selected ledger operation on the integration test network.  
*Verification.* test, record serialized bytes, applicable cost dimensions, live ledger parameters, DUST charge, proving, submission, inclusion, finality and indexing times; distinguish registration, Anchor and consumption operations; until devnet figures exist, use the measured model inputs (proofs of at most 4,368 bytes, verifying keys of at most 2,119 bytes, simulator transcript gas).

**MPE-VER-031** Concurrent Anchor validity. *(POC, MUST, settled)*  
The Prototype shall demonstrate that a reaction whose inclusion path ends at an eligible Anchor root is still accepted despite intervening Anchor insertions.  
*Verification.* test, prepare a reaction proof against an eligible root, insert later Anchors, then submit the original proof within the CON acceptance window; separately reject roots outside that window; the test shows root eligibility only, not that the anchored Envelope is the signed one.

**MPE-VER-032** Contract reaction race. *(POC, MUST, settled)*  
The Prototype shall demonstrate exactly one authorized contract effect when P-VER-17 concurrent reactors submit valid consumption transactions for the same Message.  
*Verification.* demonstration, under a functioning integration ledger with an eligible Anchor, include the racing transactions and inspect finalized contract state independently.

**MPE-VER-033** Hostile ledger inputs. *(POC, MUST, settled)*  
The Prototype shall produce zero unauthorized contract effects in the hostile ledger-input suite.  
*Verification.* test, inject fabricated Indexer results, incorrect Merkle leaves, misbound authorization, wrong destinations, expired statements, replays and failed fallible execution; inspect finalized effects and public disclosures.

**MPE-VER-034** Deployment capability gate. *(PROD, MUST, settled)*  
If the target network lacks a demonstrated capability required by the selected integration profile, then MPE shall fail production integration acceptance.  
*Verification.* demonstration, execute the exact selected Bus Registry, Anchor and consumer operations against the target runtime and Indexer schema; require finalized results and generation evidence.

**MPE-VER-035** Ledger Adapter failure. *(POC, MUST, settled)*  
When the Ledger Adapter is unavailable or returns stale state, the Prototype shall produce the NET-defined degraded-mode result for the affected operation.  
*Verification.* test, disconnect the adapter, withhold finality, return old membership roots and delay Anchor reads; check result labels against NET and CON, then exercise recovery.

**MPE-VER-036** Outside-developer usability. *(POC, SHOULD, open: DEC-VER-3)*  
The Prototype shall enable at least P-VER-19 of P-VER-18 outside developers to complete the publisher and crash-resuming subscriber exercise within P-VER-20.  
*Verification.* demonstration, provide only released documentation, examples and a prepared local environment; count success only after publication, crash, resume and correct Message recovery without team coaching.

**MPE-VER-037** Independent review gate. *(PROD, MUST, settled)*  
MPE shall enter production acceptance only with zero unresolved critical or high-severity findings from independent review of the selected construction.  
*Verification.* inspection, review admission binding, cryptography, encodings, parsing, persistent state, ledger-interface authorization and privacy claims; require reproducible closure evidence for each blocking finding.

**MPE-VER-038** Production canary gate. *(PROD, MUST, open: DEC-VER-6)*  
While the production pilot runs for P-VER-21, MPE shall achieve canary timely delivery of at least P-VER-22 within P-VER-23.  
*Verification.* test, derive expected deliveries from scheduled accepted canaries; retain failures, outages, Bus Operator distribution and per-day results throughout the consecutive window.

**MPE-VER-039** Pause and resume drill. *Same obligation as MPE-OPS-041, which owns it.*

**MPE-VER-040** Open admission gate. *Same obligation as MPE-OPS-008, which owns it.*

**MPE-VER-041** End-to-end Prototype scenario. *(POC, MUST, settled)*  
The Prototype shall demonstrate, in one scripted run against the mock Ledger Adapter, membership registration, publication, overlay delivery, local recognition, a client crash with back-fill resume, Anchor-based `final` labelling and one mock contract reaction.  
*Verification.* demonstration, the run log shows each stage with Envelope and logical identifiers and the final contract state.

