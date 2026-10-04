# ORIGINAL MIDNIGHT EXPRESS REQUIREMENTS: GOSSIPSUB + SIGNAL FIT
Independent privacy/security review, 3 October 2026. Original PDF extraction, consolidated ears-consolidated.json and Appendix A re-examined. Libraries are candidates, not inherited conformance. No repository edits, deployed results, performance or audit claims.

ANSWER
GossipSub supplies transport and Signal supplies client cryptographic sessions. Their combination covers useful portions of Midnight Express, but no complete requirement family is automatically satisfied. The strongest mandatory missing cryptographic component is production anonymous, content-bound membership/quota admission: RLN is a plausible third-protocol candidate, not a completed solution. Additional protocols depend on product goals: MLS for efficient groups, private retrieval for mobile privacy/bandwidth, and Tor for a first-hop anonymity profile. Persistent storage and Midnight ledger/contracts remain required application subsystems, even though they are not one more universal messaging protocol.

The original PDF explicitly leaves admission proof selection open and says prototype relays know its stand-in admission secrets. Its proof target is 4,096 bytes and 10 ms verification, not measured performance. The original explains why publisher signatures differ from deniable shared-secret authentication. The consolidated baseline makes signed reaction/anchor binding explicit, so report an implementation/decision gap rather than inventing a missing normative requirement.

## TWELVE REQUIREMENT AREAS
Classification is of GossipSub+Signal WITHOUT the MPE application implementation: PARTIAL means useful mechanisms, OUTSIDE means additional subsystem, FULL denotes a narrow individual mechanism only. None of the 12 complete families is FULL.

FMT — PARTIAL. MPE-NET-009a StrictNoSign is a directly available router policy with configuration/evidence; MPE-NET-009b rejects even empty identity/signature protobuf fields and must be checked against the pinned decoder. MPE-FMT-003/004 define permitted visible fields and forbid identity-derived values. MPE-FMT-051 has a CLEAR salt/nonce/Recognition Tag prefix INSIDE the structurally named Sealed Body, before ciphertext: do not assert every byte of that body is encrypted. Salted tags are visible but not stable identity labels. Signal clear ratchet/group/device identifiers must remain in the protected inner representation. MPE-FMT-018 envelope ID excludes admission slot; MPE-NET-010 wire-message ID includes it; confusing them breaks admission/commitment behavior. Fixed layout, classes, padding and canonical codecs need MPE implementation.

CRY — PARTIAL. Signal helps ratcheting, erasure and asynchronous session setup corresponding to MPE-CRY-028/029/030, but does not implement suite 0x01 specified by MPE-CRY-001 or MPE-CRY-013/014/015 salted local recognition. MPE-CRY-021/022 require canonical publisher signatures and authorized authenticated delivery. Pairwise Signal MACs cannot replace public-verifiable business authority; group sender-key ciphertext signatures are not automatically the MPE signature profile. Current Signal includes PQXDH and SPQR/Triple Ratchet; exact encrypted-header/API fit must be demonstrated. Static recognition secrets compromise past and future envelope matching in that generation even if inner ratchet content remains forward-secret.

PUB — PARTIAL. GossipSub propagates envelopes but MPE-PUB-015 requires whole differing-window repair independent of recognition, MPE-PUB-016 requires explicit reduced-privacy opt-in, MPE-PUB-022/023 require named ingress acceptance and identical retries, and MPE-PUB-027 retains application seen-set until expiry. Router caching does not fulfill these semantics; Signal cryptographic duplicate handling is not transport retention or application logical replay state.

CON — MOSTLY OUTSIDE. Local decryption assists receipt, but MPE-CON-039 prohibits automatic recognition-triggered network action. Signal automatic handshake/session responses need explicit handling under this boundary. MPE-CON-043, MPE-CON-044a/b, MPE-CON-045/046 and MPE-CON-060 require authorized signed effect inputs, atomic consumption replay protection, expiry and anchored-sealed-body-to-statement binding. Midnight circuits/ledger integration are necessary. An outer signature over opaque Signal ciphertext does not authenticate its plaintext business action; an inner canonical signature is needed. Nesting also adds opening/binding proof cost and does not automatically satisfy CON-060. MPE-CON-016 final means commitment/ledger confirmation, not issuer correctness or recipient processing.

ECO — OUTSIDE. MPE-ECO-012/013 require verified admission with cheap checks first; MPE-ECO-016/017 require membership-committed class allowance and network/registry/window/class/index-bound nullifiers; MPE-ECO-018 binds rate-limit shares to envelope ID; MPE-ECO-021 persists accepted allowances. Signal identity/session keys and GossipSub scores prove none of this. Separate admission secret from encryption/business identity under MPE-SEC-029. Quota/economic governance and operator funding also remain MPE work.

NET — PARTIAL, STRONGEST REUSE. MPE-NET-008's scoring plus v1.2 IDONTWANT is available in suitable routers; MPE-NET-009a's anonymous wrapper is configurable. MPE-NET-009b/010/014 require exact decoding/message-ID/RPC-bound checks. MPE-NET-020/068 require finalized ledger-source trust, beyond GossipSub. Cross-implementation conformance is not automatic; standard v1.2 IDONTWANT behavior is optional and implementation thresholds vary.

PRF — OUTSIDE AS EVIDENCE. MPE-PRF-001/002/004 require complete accounting and reproducible stage-separated measurements; MPE-PRF-017/018 benchmark actual production admission costs; MPE-PRF-020/021 measure mobile CPU and daily download. Neither library's independent benchmark establishes composed throughput/latency/battery/size budgets. Count recipient/device copies, PQ/bootstrap overhead, fragments, proof bytes and recovery. No inherited p99 promise.

STO — OUTSIDE. Signal mailbox concepts and GossipSub cache are not retention contracts. MPE-STO-004/005 require complete verification-material retention; MPE-STO-007 pruning; MPE-STO-011 signed receipts AFTER durable persistence; MPE-STO-012 compatible independent-operator receipts; MPE-STO-014 admission replay retention. RocksDB/SQLite can implement parts, but signatures, replication, deadlines, repair and outage policies remain MPE. Retained ciphertext without retained keys may be intentionally unreadable.

OPS — OUTSIDE. MPE-OPS-006 content-blind operators, MPE-OPS-028 explicit-action abuse reports, MPE-OPS-029 no persistent IP logs, MPE-OPS-033a/b threshold aggregation/DP budget, MPE-OPS-038 reproducible releases and MPE-OPS-051 funding are deployment/governance obligations. Native library debug logging, persistent key-state diagnostics and telemetry can violate them. Disable sensitive debug features; evaluate backup/key-state exposure and role separation.

PRV — PARTIAL, COMPOSITION GATE. Signal gives content confidentiality and ratchet properties; GossipSub flooding can help local recipient recognition. Neither proves MPE-PRV-006 Selection Game, MPE-PRV-007 trusted-local secrets, MPE-PRV-008 no private selection predicates, MPE-PRV-009/010 recognition-independent traffic/no ack, or MPE-PRV-012/013 no silent privacy fallback. First-contact lookup, session replies, prekey refresh, multi-device recovery, attachment fetch, indexer confirmation and private-error telemetry must be reviewed together. Tor does not hide topic selectors at the destination; PIR alone does not hide variable query count/timing.

SEC — PARTIAL. Borrow validated crypto and transport parsing, but enforce MPE-SEC-015/016/017 durable allowances/restart fail-closed rules; MPE-SEC-020 authenticated key changes; MPE-SEC-029 separated keys; MPE-SEC-032 explicit payload execution/download authorization; MPE-SEC-037 contract-authority predicate. Session authentication must not authorize arbitrary downloaded commands. Test key-directory substitution and revoked-device recovery.

VER — OUTSIDE AS CONFORMANCE. Upstream crypto tests help engineering but do not satisfy MPE-VER-002 claim evidence, MPE-VER-007 admission model, MPE-VER-008 cursor/dedup model, MPE-VER-009 unauthorized/duplicate-effect model or MPE-VER-030 actual ledger measurements. Complete composition invariants and mismatch tests under failure/replay/restore/adversarial selectors.

## INDIVIDUAL OPEN-SOURCE CANDIDATE STUDIES

## WAKU RLN RELAY / JS-RLN
Useful: anonymous quota verification, signal-bound double-publication evidence and membership-root management already developed around GossipSub. js-rln is browser/WASM-oriented and provides Waku encoder/decoder interfaces; package license MIT OR Apache-2.0. Its wrapper should not be confused with a generic drop-in MPE circuit. Current RFC redirect/source and precise RLN version need pinning.
Gap: Waku registration/epoch/fee/identity assumptions and proof public inputs differ from MPE class/window/root/context requirements. Its economic slashing/conflict semantics cannot be inherited without deciding how MPE governance handles exposed secret evidence. Observe privacy linkability of protocol nullifiers within their defined scope.
Gate: demonstrate MPE-ECO-016/017/018 exactly, conflicting share extraction, replay restart behavior, proof encoding in P-FMT-2 and actual MPE-PRF-017/018 hardware costs; never imply a small RLN proof establishes total-slot and <=10ms conformance.
Sources: https://rfc.vac.dev/spec/17/ (resolved to https://lip.logos.co/spec/17/) ; https://github.com/waku-org/js-rln ; https://github.com/waku-org/js-rln/blob/master/package.json

## ZEROKIT / RLN
Useful: Rust RLNv2, Circom/Groth16/arkworks, FFI and WASM primitives; current repository also supports multi-message-ID burn. License MIT OR Apache-2.0, verified rln/Cargo.toml. Suitable first admission implementation experiment, not the complete ledger-integrated admission protocol.
Gap: selected circuit artifact/proving parameters/public-input relation require independent inspection; domain-separated MPE statement binding and nullifier slopes must match the exact circuit. Dependencies, setup/proving artifacts and versioned serialization are security boundaries.
Gate: pin code and circuit hashes; test foreign genesis/registry/class/index/root and envelope substitutions, malformed encodings, conflict extraction, restart behavior, proof size and invalid-proof CPU. Relay never sees admission secret.
Sources: https://github.com/vacp2p/zerokit ; https://github.com/vacp2p/zerokit/blob/master/rln/Cargo.toml

## OPENMLS
Useful: Rust RFC9420 groups with provider traits and storage adapters; MIT license. Maintained by Phoenix R&D and CE Labs. Supported crypto suites/provider choices and platform testing are documented.
Gap: not a routing/private-discovery system, does not promise MPE recipient-key hiding, unknown-member admission or private group selection; group credentials and commits have visibility depending on wrapper. Group rotation needs honest fresh updates, erasure and epoch-order/fork handling. Public MLS messages/group IDs must not leak through MPE wrapper.
Gate: fixed-size sealed commits/welcome/traffic, private membership discovery, simultaneous commits/removal and offline restore; use patched pinned release and inspect current security advisories. Sensitive content-debug/crypto-debug features remain disabled. Business instruction signatures and CON-060 stay independent.
Sources: https://github.com/openmls/openmls ; https://github.com/openmls/openmls/blob/main/LICENSE ; https://github.com/openmls/openmls/security

MLS-RS
Useful: Rust RFC9420 implementation with multi-identity/group client, pluggable crypto/storage and async-friendly integration; Apache-2.0 OR MIT verified project documentation. Alternative to OpenMLS, not another required group protocol in addition to it.
Gap: backend/provider selection, feature combinations, credential binding and commit ordering are application responsibilities; library support does not establish mobile profile or recipient-interest privacy. It is a different implementation/runtime/storage API, requiring independent persistence/failure tests.
Gate: same group/private-wrapper/authority gates as OpenMLS plus interop vectors with chosen peer implementation and compatible persisted-state schema across upgrades.
Sources: https://github.com/awslabs/mls-rs ; https://awslabs.github.io/mls-rs/

## MICROSOFT SEAL
Useful: C++ homomorphic-encryption primitives, MIT license. Possible foundation for computational PIR and encrypted-query processing.
Gap: SEAL is not a PIR protocol or MPE authentication/retention service. Choose security parameters, evaluator bounds and explicit row database construction; malicious reply integrity is not guaranteed merely by computing on encrypted queries.
Gate: selected PIR implementation has independent reviewed privacy/correctness assumptions and authenticated result opening to an expected commitment/envelope. Include serialization, key material, CPU/memory and parameter-version costs.
Sources: https://github.com/microsoft/SEAL ; https://www.microsoft.com/en-us/research/project/microsoft-seal/

## SEALPIR
Useful: computational single-server PIR example built atop SEAL, MIT license. Direct candidate for retrieval benchmark.
Gap: README explicitly says research library and not for production; pinned dependency described as SEAL4.0.0. Index privacy alone does not hide query cadence, count, record/bucket class, IP or initial desired-row discovery. Dynamic retention windows need database/version consistency and authenticity.
Gate: prototype only; padded/fixed cadence and row budgets, snapshot/epoch indexing, failed-answer authentication, denial-of-service bounds, measured hints/keys/query/reply bytes and continuous update costs.
Sources: https://github.com/microsoft/SealPIR ; https://github.com/microsoft/SealPIR/blob/master/LICENSE

## GOOGLE PRIVATE-RETRIEVAL
Useful: C++/Bazel PIR implementation with cryptographic and serialization dependencies, Apache-2.0 license.
Gap: repository archived 18 April2026; README says not officially supported Google product. Distinguish it from separate google/hintless_pir and google/private-membership projects. No implied current maintained production service or MPE suitability.
Gate: benchmark/reference only unless maintenance is explicitly owned. Review cryptographic parameter support, malicious-response integrity, dependency age and dynamically updated/padded MPE database profile.
Sources: https://github.com/google/private-retrieval ; https://github.com/google/private-retrieval/blob/main/LICENSE

## SIMPLEPIR / DOUBLEPIR
Useful: single-server LWE-based reference implementations and batch/long-record extensions, MIT license; efficient scan architecture worth benchmarking.
Gap: README calls code a research prototype. Preprocessing/hint movement, dynamic snapshot updates, row sizes and server scanning dominate application costs; paper numbers are not MPE phone/node performance. PIR does not supply discovery, proof admission, replay authority or data integrity.
Gate: bounded epoch/window database with authenticated snapshot, real mobile preprocessing/updates, constant observable queries/dummy rows and measured useful-to-total-byte ratio. Do not classify an encrypted index as a complete interest-privacy proof.
Sources: https://github.com/ahenzinger/simplepir ; https://github.com/ahenzinger/simplepir/blob/main/LICENSE

## TOR / ARTI
Useful: Tor client routing can reduce direct ingress/source IP exposure; Arti has Rust async streams and SOCKS/onion-service integration. Arti license MIT OR Apache-2.0 verified crate manifest. Tor C source uses a distinct implementation/license and must be pinned separately rather than treating Arti license as Tor universal license.
Gap: Tor does not suppress server-visible stream/device selectors, query timing/volume, traffic correlation or authenticated identity credentials. It does not provide global-observer immunity or MPE bandwidth reductions. TCP-stream integration differs from ordinary libp2p QUIC/UDP transport; avoid bypass via DNS or auxiliary direct sockets. Arti current APIs are pre1.x and require upgrades as Tor network changes.
Gate: explicit ingress threat profile, stream isolation, no DNS/side-channel leaks, all intended connections proxy-routed with fail-closed behavior; measure startup/latency/reconnect and node resource costs. Read request traffic remains recognition-independent.
Sources: https://arti.torproject.org/ ; https://arti.torproject.org/contributing/ ; https://docs.rs/crate/arti-client/latest ; https://docs.rs/crate/arti-client/latest/source/Cargo.toml

## ROCKSDB
Useful: embedded persistent key-value engine, WAL/batched writes for replay/cursor/store material; dual Apache-2.0 OR GPLv2 per current README, so select/document Apache option. Good node storage candidate.
Gap: durability settings and write-batch semantics must be selected; a storage API does not establish receipt-before-persistence, cross-node quorum, encrypted key storage, erasure, expiry or application effect atomicity. Plaintext secret state can persist in WAL/backups despite logical deletion.
Gate: process/host crash injection around admission acceptance, receipt and ratchet commit; correct sync/WAL choices; backup/compaction/key-material inventory; deterministic retention scans and typed disk-full behavior.
Sources: https://github.com/facebook/rocksdb ; https://github.com/facebook/rocksdb/blob/main/LICENSE.Apache ; https://github.com/facebook/rocksdb/blob/main/COPYING

SQLITE
Useful: public-domain core with local ACID transactions/WAL; reasonable SDK state and small reference-node implementation. WAL files/readers/checkpoints require correct lifecycle handling.
Gap: default SQLite is not encrypted; public-domain core does not mean every extension/provider is equally licensed. ACID local DB transactions cannot atomically commit arbitrary remote service/chain effects; deleting a row does not ensure filesystem/backups lose secret keys.
Gate: combine replay/effect/checkpoint locally where possible, use destination idempotency elsewhere; test power/process failure, long-lived readers, disk-full and WAL checkpoint cleanup. Client-state encryption and real key erasure policy are explicit.
Sources: https://www.sqlite.org/copyright.html ; https://www.sqlite.org/wal.html

## RUST-LIBP2P
Useful: MIT-licensed Rust networking stack with router/transport/validation settings; directly relevant to existing implementation direction.
Gap: pinned decoder policy and v1.2 negotiation behavior matter. Baseline notes 0.50.0 missing StrictNoSign key-presence validation later added in0.51.0; upgrade evidence is required. Connection encryption/PeerID authentication is transport security, not publisher anonymity or business signature authority.
Gate: packet-level anonymous-wrapper conformance, foreign shard/version rejection, encoded RPC limit, IDONTWANT compatibility, validation-cache timeout and cross-Go/Rust router parameters; all application validation occurs before forwarding.
Sources: https://github.com/libp2p/rust-libp2p ; https://docs.rs/crate/libp2p/latest/source/Cargo.toml

## LIBSIGNAL
Useful: Rust-based Signal crypto with Java/Swift/TypeScript bridges; AGPLv3, outsideSignal use explicitly unsupported, APIs can change without notice. Current Signal protocol research includes PQXDH/SPQR; group sender keys are separately implemented.
Gap: no MPE salted recognition/admission/authority/anchor API. Pairwise deniable MAC authentication is not an authorized business signature. Stable outer MPE secret can preserve discovery while sacrificing historical/future metadata privacy; ratchet encryption does not fix that. Opaque nesting preserves current suite only by retaining outer encryption/authentication; inner canonical business signature and CON-060 opening remain separate.
Gate: pinned supported API/profile test, offline prekey/device bootstrap, state rollback/erasure, size/fanout/fragment budget, no automatic recognition-response leakage, license/upgrade ownership, and independent cryptographic composition review.
Sources: https://github.com/signalapp/libsignal ; https://signal.org/docs/specifications/pqxdh/ ; https://signal.org/docs/specifications/doubleratchet/ ; https://signal.org/docs/specifications/sesame/

## THIRD-PROTOCOL DECISION
Mandatory production gap: anonymous membership/quota proof scheme under DEC-007, with RLN/Zerokit as leading reuse experiment. Signal identity or gossip scores cannot fill it.
Optional group architecture: choose MLS/OpenMLS or mls-rs if efficient large groups justify another protocol; pairwise Signal/device fanout can pilot first. Do not import group IDs or assume sender-key groups inherit pairwise compromise recovery.
Conditional mobile gap: PIR/oblivious retrieval if both bandwidth and recipient-interest goals require it; whole-shard backend receipt remains valid baseline. PIR needs discovery, fixed budgets, dummy queries, authenticated epoch snapshots and declared leakage. The exact current whole-window repair/whole-shard API is not automatically satisfied by a selective PIR API; approve a distinct reviewed profile with explicit requirement reconciliation. Encrypted index privacy does not hide whether/when/how much a client requests.
Optional ingress profile: Tor/Arti reduces direct origin exposure if required by adversary scope. It neither changes global-observer limits nor replaces private retrieval.
Outside all of those: Midnight membership/Anchor/governance circuits, signed authority/replay/binding, durable retention/repair, operations/funding and composed evidence. These are essential application work rather than a missing universal third protocol.

## RESEARCH OPTION: THIN DISCOVERY INVENTORY PLUS PIR
A whole-shard schedule could distribute salts/tags to every subscriber for local recognition and retrieve ciphertext bodies with padded fixed-budget PIR. This potentially separates discovery from payload bandwidth, but it is not a selected compliant profile. At 10 envelopes/s, 16-byte salt plus 16-byte tag alone is 27,648,000 bytes/day (27.65 decimal MB); adding a 32-byte envelope ID reaches 55,296,000 bytes/day before authenticated inventory structure, headers, transport, hints, query/reply cover and payload. The 56–60MB mobile target is therefore tight; no fits-budget claim is warranted.

The existing Anchor commits envelope IDs, not independently advertised discovery fields. A server could misstate salt/tag or omit entries unless a reviewed inventory structure proves their correct binding and completeness against the actual anchored envelopes. Hashing EID alone does not let a lightweight client verify an isolated advertised prefix without an opening/proof. Fixed row sizes, scheduled counts/epochs, dummy queries and fail-closed integrity checks must prevent matching-message workload or server response manipulation from exposing recognition. Evaluate mobile CPU/bandwidth and malicious-store behavior before deciding whether it satisfies the Selection Game and requires changes to whole-window repair.

## FIRST EXPERIMENTS
1. Anonymous quota proof: exact MPE statement and slot/verification/preparation benchmark, including malformed and replayed inputs.
2. Pairwise opaque Signal inside existing MPE suite: preserve local recognition, fixedclasses, signedinstruction and failure-atomic state; measure overhead.
3. Contract consumed statement: mismatched valid inclusion/inner instruction must fail; demonstrate actual Compact proof and cost before settlement.
4. Private mobile retrieval comparative prototypes: static/dynamic epochs, hint churn, fixed budgets and server/client adversary traces.
5. Durable store/replay integration: receipts issued only after crash-recoverable commit; recognition-independent repair and key-retention gaps explicit.

Every requirement citation above was checked against consolidated IDs. Classification is an engineering assessment, not an assertion of upstream conformance or a percentage of work completed.

## GROUP-FIRST PRODUCT CHOICE: MLS INSTEAD OF SIGNAL
For a business product whose core workflows are groups, roles and changing counterparties, choose MLS as the first session/group cryptographic architecture and treat Signal as an alternative profile rather than stacking both by default. MLS groups can have two members, so the same machinery can cover direct conversations and larger committees. This reduces duplicate identity, prekey, state-recovery and upgrade surfaces; it does not imply a two-member MLS group has the exact same operational/PQ guarantees as the currently documented Signal Triple Ratchet. Choose an exact ciphersuite and implementation version; the OpenMLS advertised default suites are classical, so no inherited post-quantum claim.

Mandatory MLS gates: seal group IDs, epoch counters, credentials, commit/welcome metadata and plaintext/application headers inside the MPE protected representation; separately evaluate unavoidable packet-class/timing leakage. Bind MLS credentials to independently authorized wallet/device/business identities with authenticated rotation. Freeze epoch/commit ordering, concurrent-commit fork resolution, member-removal/send boundary and offline state-recovery rules. Retained old epoch keys and backups limit erasure/forward-secrecy claims. Re-establishment after lost state must be explicit and cannot silently rebuild intentionally erased secrets. Private local recognition remains separate from MLS group routing, and a stable outer recognition secret retains its own compromise exposure.

MLS message authentication/signatures are not automatically the canonical authorized business-effect signature accepted by the Midnight contract. Retain and verify the separately scoped signed instruction, expiry, replay nullifier and MPE-CON-060 anchored-body opening. MLS encryption does not supply this circuit implementation or solve proving costs. Experiment with off-chain group coordination first; complete the contract gate before actual settlement.

## GOSSIPSUB CACHE EXPIRY ENFORCEMENT
Application validation at initial receive does not alone prove every later relay path respects MPE expiry. Stock GossipSub can satisfy IWANT from its message cache after initial validation, so the selected MPE expiry predicate must cover cached response/queued-send paths as well as new publication and receipt. A cached envelope can cross its deadline even within a short router cache lifetime. Specify whether cache eviction/response filtering/queue cancellation is implemented through a supported hook or a narrowly scoped pinned router patch; do not claim a generic wrapper automatically intercepts every internal send. Test an envelope just before expiry, advance time, request it by IWANT and drain delayed outbound queues; expired data must not be served/forwarded contrary to the frozen predicate and any explicit clock tolerance. This work belongs to MPE transport integration, not the choice between MLS and Signal.
