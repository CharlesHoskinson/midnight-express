# Midnight Express: original requirement fit and additional open-source components
Independent architecture reviewer, 2026-10-03 America/Denver. Re-examined original PDF extraction, especially architecture/recognition, prior-art PIR/OMR and Waku/RLN passages, against repo docs/design-document/build/appendix-a.md and ears-consolidated.json. Current register is normative; PDF prose can lag it. Research does not establish implemented compliance.

Verdict
GossipSub + Signal is a useful transport/session-encryption combination, not the complete Midnight Express protocol. No entire requirement area is demonstrated complete merely by selecting those libraries. Full-Shard backend operation does NOT logically require a universal third named protocol. It DOES require additional protocol roles and implementation components. Best next additional protocol candidate is RLN-style anonymous rate-limited admission; mobile private delivery is a separate discovery/retrieval research track, not something RLN or Signal solves.

The original PDF already identifies Waku/RLN, private retrieval/OMR, onion-routing limits, retention and ledger anchoring. These are not newly missing ideas. The work is choosing measured components and implementing the existing obligations. Signed authority and anchored-statement binding already exist normatively (MPE-CON-043, MPE-CON-044a/b/060); exploratory circuits have not demonstrated them. PDF passages saying binding is unspecified require reconciliation.

Coverage vocabulary: partial = provides mechanisms supporting a subset after integration; outside scope = neither library supplies the area; complete = would require passed acceptance evidence, and is not assigned here. Requirement IDs below are concrete traceability samples, not an exhaustive per-requirement compliance certification.

All 12 areas
FMT — PARTIAL. GossipSub transports bytes; Signal serializes session ciphertext. Neither supplies fixed MPE envelope classes, visible-field restrictions, canonical construction or admission layout. MPE-FMT-003, MPE-FMT-004 and MPE-CRY-036 require MPE wrapping and measured size accounting. Gate: codec round-trip/vectors and packet captures show only permitted outer fields; bootstrap and ratchet updates fit agreed classes without silent fragmentation/version changes.

CRY — PARTIAL. Signal can supply session establishment and ratchet primitives, but not MPE salted recognition, wallet publisher signatures, invitation policy or outer sealing profile. MPE-CRY-001, MPE-CRY-013, MPE-CRY-018, MPE-CRY-020, MPE-CRY-028, MPE-CRY-029, MPE-CRY-030, MPE-CRY-032, MPE-CRY-034 and DEC-CRY-1/2/3/4 remain integration choices. Gate: exact negotiated suites, key lifecycle/revocation, identity binding, restore rollback and skipped-key bounds. Existing suite0x01 is invitation-based symmetric MPE, not automatically replaced by Signal. Nested ciphertext is an experiment with its own versioned payload schema.

PUB — PARTIAL. GossipSub dissemination supports publication; Signal secrecy supports protected payloads. MPE-PUB-010, MPE-PUB-012, MPE-PUB-015, MPE-PUB-044, MPE-PUB-045 require local recognition, recognition-independent behavior, complete-window repair, transactional effects and explicit retention gaps. Gate: compare interest-swapped traces and crash/recovery workloads. Neither generic topic subscription nor Signal destination-addressed service provides those guarantees automatically.

CON — PARTIAL. Signal authenticates its session peer under its identity model; MPE consumers need authorized signed business effects, finality, replay protection and anchor binding. MPE-CON-012, MPE-CON-033, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-045, MPE-CON-047, MPE-CON-060. Gate: wrong signer/target/expiry, mismatched anchor versus instruction, duplicated effects and failed/retracted source events are rejected. Pairwise deniable authentication is not a portable wallet signature. Nested Signal payload decryption can materially complicate proof circuits; begin off-chain one-to-one.

ECO — OUTSIDE SCOPE. Need real anonymous admission, class/credit quotas, replay/equivocation handling, membership economics and fee/funding rules. MPE-ECO-012, MPE-ECO-013, MPE-ECO-017, MPE-ECO-018, MPE-ECO-022, MPE-ECO-048, MPE-ECO-049, MPE-ECO-054; DEC-007 and DEC-ECO-1/4. Gate: secret remains client-side, proofs bind the proof-independent envelope identifier, stale roots/reused credits behave correctly, and proof bytes/verification/mobile generation meet measured limits. Admission is per-node allowance with distributed races/evidence, not a magical globally atomic bandwidth cap. DUST is not operator pay (MPE-ECO-002).

NET — PARTIAL, strongest library fit. GossipSub directly supplies mesh/scoring/control behavior; MPE-NET-008, MPE-NET-009a, MPE-NET-010, MPE-NET-015, MPE-NET-035, MPE-NET-036, MPE-NET-041, MPE-NET-051, MPE-NET-058, MPE-NET-062 still require StrictNoSign, correct IDs, application validation, authenticated Registry reads, anchors and version policy. Gate: Rust/custom-identifier v1.2 caveat, cross-implementation interoperability, finalized-only state and peer-abuse tests. Signal has no mesh-delivery role.

PRF — OUTSIDE SCOPE AS A GUARANTEE. Both impose costs but neither demonstrates the declared deployment performance. MPE-PRF-002, MPE-PRF-017, MPE-PRF-018, MPE-PRF-021, MPE-PRF-038, MPE-PRF-040. Gate: named hardware/software/workload manifests and actual dissemination, proof, ciphertext overhead, subscriber daily bytes and ledger costs. Original full-Shard design's mobile burden remains regardless of improved session encryption.

STO — OUTSIDE SCOPE. GossipSub caches are not the 48h ordinary retention service; Signal storage traits preserve local keys, not distributed envelope availability. MPE-STO-001, MPE-STO-006, MPE-STO-011, MPE-STO-017, MPE-STO-022, MPE-STO-032, MPE-STO-042. Gate: receipts follow restart-recoverable persistence; expiry is not refreshed by fetch; replicated coverage/canaries and full-window replay work; recoverable ciphertext AND decryptable state coverage are reported. A database engine alone does not implement these network semantics.

OPS — OUTSIDE SCOPE. Governance, operator diversity, concentration, bootstrap authentication, upgrades, incident response and written funding remain. MPE-OPS-007, MPE-OPS-010, MPE-OPS-018, MPE-OPS-038, MPE-OPS-044, MPE-OPS-048, MPE-OPS-051, MPE-OPS-052. Gate: governance/upgrade/drill evidence and operator commitments. Neither library supplies a sustainable network/operator business model.

PRV — PARTIAL. Signal adds content protection; whole-Shard local recognition can protect recipient interests conditionally. MPE-PRV-007, MPE-PRV-009, MPE-PRV-010, MPE-PRV-013, MPE-PRV-014, MPE-PRV-028. Gate: no recognition-dependent acknowledgements, key-directory queries, source verification, attachment fetches or diagnostics; weaker fallbacks require explicit selection. Ingress IP/timing and coarse shard membership remain exposed; no adversarial archive erasure or global-observer anonymity claim.

SEC — PARTIAL. GossipSub scoring and Signal cryptography support attack resistance, but admission, proof-independent dedup, current Registry trust and omission repair remain MPE concerns. MPE-SEC-001, MPE-SEC-014, MPE-SEC-023, MPE-SEC-025, MPE-SEC-038. Gate: hostile admission/root/state inputs, replay, omission, verification-DoS and privacy traces. Open membership is a separate gate, not inherited Sybil resistance.

VER — OUTSIDE SCOPE. MPE-VER-004, MPE-VER-006, MPE-VER-007, MPE-VER-009, MPE-VER-024, MPE-VER-025, MPE-VER-028, MPE-VER-034, MPE-VER-037 require conformance, cryptographic measurement, admission/consumption models, chaos tests, trace checks, demonstrated ledger capability and independent composition review. Existing library tests do not certify the MPE composition.

Smallest architecture satisfying the selected backend profile
Application / SDK authority, finality, processOnce
 -> existing versioned MPE signing, sealing, padding and salted local-recognition
 -> optional Signal pairwise ciphertext payload inside that MPE message
 -> class-bound anonymous admission proof + replay/equivocation state
 -> GossipSub1.2 full-Shard propagation and authenticated operator/Registry view
 -> MPE Store service: durable receipts, fixed retention, inventory/replay/repair
 -> periodic batch commitments / Midnight Registry Anchors / LedgerAdapter
Receiver obtains full-Shard windows independently of interest, recognizes locally, opens and authenticates, decrypts session payload, verifies business authority/finality and atomically commits allowed local effects.

Persist local sessions/credits/cursors using transactional storage; persist opaque retained envelopes using an engine under an explicitly defined MPE store protocol. Add operator funding, governance and validation evidence across all layers. Optional Tor/Arti changes ingress privacy; optional MLS changes group cryptography; optional private retrieval changes mobile reception. None is required to call the whole-Shard experimental backend complete without its applicable gates.

Open-source candidates: independent study of every named option

1. Waku RLN / Zerokit rln
Sources: https://github.com/vacp2p/zerokit ; https://lip.logos.co/spec/17/ ; https://github.com/vacp2p/zerokit/blob/master/rln/README.md
Mechanism/fit: membership proof and rate-limiting nullifiers/shares; current Zerokit documents RLNv2 and multi-message-ID burn, Circom/arkworks Groth16, FFI/WASM. Strong admission candidate for MPE-ECO-012, MPE-ECO-017, MPE-ECO-018.
Bounds: no subscription or publisher-network anonymity; multiple purchased memberships amplify quota. Root/hash/circuit relation, per-class allowance, content binding, setup/proving artifacts and Compact Registry integration need a chosen design; importing an Ethereum Waku membership contract does not implement Midnight Registry. Current root badges specify MIT/Apache2.0. Pin exact rln/circuit artifacts and audit dependencies. Gate: proof size/time, client-held secrets, equivocation test and live Registry-root compatibility.

2. OpenMLS
Sources: https://github.com/openmls/openmls ; https://github.com/openmls/openmls/blob/main/LICENSE
Mechanism/fit: RFC9420 group epochs and membership updates, transport-independent secure group library; MIT. Candidate for group cryptography where pairwise fanout becomes costly.
Bounds: not Signal Sender Keys and not a third transport/privacy layer. Requires credentials, delivery/commit handling, state persistence and reviewed provider choices. Group identifiers/headers must stay inside MPE protection. Does not hide recipient queries or network relationships. Gate: revoked-member new-epoch rejection, fork/lost-commit recovery and actual welcome/commit size against MPE classes. Do not enable debug secret logging in deployment.

3. mls-rs
Sources: https://github.com/awslabs/mls-rs ; https://github.com/awslabs/mls-rs/blob/main/README.md
Mechanism/fit: alternative RFC9420 group implementation with configurable crypto/credential/storage providers; MIT OR Apache2.0. Evaluate alongside OpenMLS, choose one for a declared group profile rather than stacking both.
Bounds: README says no full third-party security audit yet; provider stability varies. MLS confidentiality does not solve metadata. Gate: same membership/epoch/recovery interoperability tests, audited provider selection and application credential binding.

4. Microsoft SEAL
Sources: https://github.com/microsoft/SEAL ; https://github.com/microsoft/SEAL/blob/main/LICENSE
Mechanism/fit: homomorphic-encryption primitives, MIT. A building block for private computation/retrieval research, not itself a PIR inbox protocol or message bus.
Bounds: app chooses scheme/parameters and integrity/authentication; FHE does not discover recipient records by itself. Gate: approved security parameters, actual wire/CPU cost and end-to-end retrieval correctness. Do not recommend SEAL alone as mobile interest-privacy solution.

5. SealPIR
Sources: https://github.com/microsoft/SealPIR ; https://github.com/microsoft/SealPIR/blob/master/LICENSE
Mechanism/fit: computational single-server indexed retrieval atop SEAL; MIT. Useful experimental hidden-index back-fill primitive.
Bounds: repository explicitly warns against production use. A hidden known index is not hidden inbox discovery or dynamic message matching. Timing/count, database choice, class choice, malicious omissions and freshness remain outside its basic guarantee. Gate: separately authenticated indexing/discovery and fixed/batched access schedule; dynamic updates and complete-window availability; mobile all-in cost.

6. Google private-retrieval
Sources: https://github.com/google/private-retrieval ; https://github.com/google/private-retrieval/blob/master/LICENSE
Mechanism/fit: C++ library retrieves a database element without exposing index, using dependencies including SHELL encryption; Apache2.0. Another research comparison for indexed retrieval.
Bounds: not an officially supported Google product; no MPE discovery, session keys, quota, availability or traffic-correlation solution. Gate: confirm actual selected API threat model, malicious-server handling, mobile build/latency and authenticated updated data before selecting it.

7. SimplePIR / DoublePIR
Sources: https://github.com/ahenzinger/simplepir ; https://github.com/ahenzinger/simplepir/blob/main/LICENSE
Mechanism/fit: single-server LWE-based PIR with preprocessing hints; MIT, explicitly research prototype. Good measurable comparison for bandwidth/server cost.
Bounds: published static database throughput is not mobile dynamic-inbox throughput; hints/preprocessing and refresh are real costs. Indexed PIR does not privately identify new recipient messages as OMR would. Gate: account for hints, updates, padded request schedule, signed snapshots and all device/server costs using realistic retention windows.

8. Tor / Arti
Sources: https://arti.torproject.org/about/ ; https://arti.torproject.org/contributing/ ; https://gitlab.com/torproject/tor/-/blob/main/CONTRIBUTING?ref_type=heads
Mechanism/fit: onion-routed ingress can obscure client IP from bus endpoint under a declared adversary. Arti offers embeddable Rust client functionality, MIT OR Apache2.0; classic Tor's contribution terms name BSD3-Clause (inventory bundled dependencies separately).
Bounds: no global-observer/timing-correlation guarantee, no private selection/index queries by itself. TCP ingress over Tor requires an adapter; libp2p QUIC/UDP is not transparently carried. Persistent node keys/account login can relink clients. Gate: no direct-connection fallback, latency/first-spy measurement, circuit/isolation policy and endpoint identifier audit. Optional for original full-Shard profile, mandatory only for a newly selected stronger source-privacy claim.

9. RocksDB
Sources: https://github.com/facebook/rocksdb ; https://github.com/facebook/rocksdb/blob/main/LICENSE.Apache ; https://github.com/facebook/rocksdb/blob/main/LICENSE.leveldb
Mechanism/fit: embedded persistent key-value engine for store envelope/index/replay state. README specifies GPLv2 OR Apache2.0, with separate inherited LevelDB BSD notices; do not call the entire project BSD licensed.
Bounds: engine is not a distributed store protocol, no implicit retention receipts, replication or privacy; ordinary deletion may leave copies/backups. Gate: chosen sync/WAL settings actually survive crash, atomic batch invariants, bounded capacity/expiry and encrypted local secret storage where needed.

10. SQLite
Sources: https://www.sqlite.org/copyright.html ; https://www.sqlite.org/atomiccommit.html
Mechanism/fit: public-domain embedded transactional database; useful client session/cursor/dedup/outbox and small-node store engine.
Bounds: public-domain status can require jurisdiction/procurement handling, optional commercial warranty exists. No default key encryption, distributed availability or remote-side-effect atomicity. Gate: synchronous/journal/transaction settings withstand crash at each session/effect boundary; secrets encrypted under endpoint key and backup/rollback policy explicit. RocksDB/SQLite are alternative engines chosen by role, not two extra network protocols.

11. libp2p / rust-libp2p
Sources: https://github.com/libp2p/rust-libp2p ; https://github.com/libp2p/rust-libp2p/blob/master/LICENSE ; earlier GossipSub study source manifest
Mechanism/fit: MIT transport/library implementation; retain pinned GossipSub1.2 behavior and application validation. Supports the existing sidecar decision.
Bounds: custom protocol-ID APIs in inspected Rust source have version1.0/1.1 choices even though defaults negotiate1.2. Do not inherit anonymity, global order or long retention. Gate: strict unsigned outer frames, agreed profile, cross-implementation tests and MPE recovery integration.

12. Signal / libsignal
Sources: https://github.com/signalapp/libsignal ; https://signal.org/docs/specifications/pqxdh/ ; https://signal.org/docs/specifications/doubleratchet/ ; https://signal.org/docs/specifications/sesame/
Mechanism/fit: maintained Signal primitives and per-device session APIs; current source AGPL3-only, third-party use unsupported and APIs can change. Current specifications include SPQR/TripleRatchet alongside classical DoubleRatchet; pin actual implemented suite, not marketing label.
Bounds: not a pubsub registry, local recognition protocol, prekey directory privacy service or contract-signature authority. Signature and anchor binding stay MPE obligations. Static outer-key exposure may reveal stream linkage while erased inner keys protect plaintext; session compromise recovery does not heal recognition secrets. Gate: pinned adapter/version/license inventory, encrypted transactional key state, actual payload sizes and off-chain one-to-one vectors before contract or group claims. Do not reimplement crypto to sidestep library restrictions.

Third-protocol decision
If the question is 'what next protocol improves the launch backend most?', choose RLN admission evaluation, because anonymity-preserving quotas remain unsolved by the proposed pair. If the question is 'what enables usable private mobile subscriptions?', require private message discovery plus retrieval and timing/size policy; none of the listed indexed PIR libraries is a plug-in complete OMR substitute. If the question is 'what enables multi-party secrecy with scalable rekey?', evaluate MLS separately from Signal pairwise/Sender Keys. If the question is 'what hides source IP?', use a declared onion ingress profile and its costs/limits. These solve different requirements and cannot substitute for one another.

NATS/Kafka can support internal enterprise integration/local app processing, but visible topic filters, consumer offsets and per-recognition acknowledgements conflict with MPE-PUB-010, MPE-PUB-012 and MPE-PRV-009, MPE-PRV-010. Their durability does not prove confidential interest privacy. Likewise RocksDB/SQLite supply persistence mechanisms; the MPE Store network API, admission, receipts, full-window inventory/replay, retention and authenticity rules remain to be implemented.

Thin-inventory plus PIR: worthwhile bounded research experiment, not selected production protocol
A client could download every salt/tag discovery entry in a Shard, recognize locally, and privately retrieve matching envelope positions. At the original 10-envelope/s ceiling, 864,000 entries/day times salt16+tag16 costs27.648MB/day before authentication or retrieval. Adding a32-byte envelope identifier yields55.296MB/day; nonce, framing, inventory proofs, PIR hints/responses, retries and dummy queries add costs. This is already close to the cited56–60MB/day mobile ambition. It reduces bulk scanning potential but does not establish a working budget.
Gate: authenticated inventory-to-PIR-database snapshot binding, fixed padded query volume independent of match count, update/hint refresh cost, source diversity/omission detection, replay and window gaps. A valid commitment authenticates its included inventory; it does not prove every admitted message was included. PIR must not expose discovery tags or per-interest plain filters. Benchmark changing real versus dummy indices at constant observable schedule. This is a separate DEC-021 experiment alongside OMR; failure must not silently activate a less-private profile.
