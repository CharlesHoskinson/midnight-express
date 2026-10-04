# MIDNIGHT EXPRESS: GOSSIPSUB + SIGNAL PROTOCOL — PRODUCT/INTEGRATION REVIEW
Independent reviewer: design_review_product. Evidence checked 2026-10-03 America/Denver.
Status: Feasibility assessment and experimental gates, not adoption or implementation claim.

## RECOMMENDATION
Go for a narrow backend, single-device, one-to-one messaging experiment combining GossipSub transport with a reviewed Signal-derived session profile inside MPE. No-go for describing these dependencies alone as a complete production private coordination service. They solve different layers and leave discovery, interest-private reception, persistent session state, retention, admission proofs, business authority, mobile cost and operator economics to Midnight Express.

'Use Signal' should mean its cryptographic specifications or an explicitly selected implementation, not using the Signal app or relying on Signal Messenger's service. Parties can generate their own identities and exchange authenticated invitations/prekey material. A prototype need not create Signal accounts, use phone numbers, or connect to Signal servers. This is an architectural proposal, not a promise of interoperability with the Signal app.

## PRIMARY SOURCES
GossipSub1.2: https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.2.md
Signal Double Ratchet: https://signal.org/docs/specifications/doubleratchet/
Signal PQXDH: https://signal.org/docs/specifications/pqxdh/
Signal Sesame: https://signal.org/docs/specifications/sesame/
libsignal implementation/support/bindings: https://github.com/signalapp/libsignal
libsignal license: https://github.com/signalapp/libsignal/blob/main/LICENSE
Concrete API: https://github.com/signalapp/libsignal/blob/main/node/ts/index.ts
Rust protocol API: https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/lib.rs
Group primitives: https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/sender_keys.rs
Local baseline: docs/design-document/build/ears-consolidated.json and repo LICENSE.
Primary sources verified through web and concrete libsignal APIs additionally fetched through Scrapling. No new source repository copied into Midnight Express.

## GOSSIPSUB DESIGN ASSESSMENT
The1.2 extension adds IDONTWANT duplicate suppression for received message IDs and negotiates /meshsub/1.2.0. Threshold/pruning policy is implementation-specific; small-message traffic may get worse and flood limits need agreement. This does not supply encryption, durable offline storage, private subscription discovery or business authorization.

Adopt the transport, but make duplicate signaling depend on receipt/inventory, never whether a recipient recognizes/decrypts a message. Use the existing shard topic and anonymous GossipSub payload profile MPE-FMT-012: data carries the envelope while from/seqno/signature/key are absent. A private conversation must not become its own public topic. Transport-peer authentication and observable IP paths remain separate from sealed publisher authentication.

Product implication: a stable listener API and store-backfill layer are still necessary. Publishing to a mesh is not a success receipt from another business. Measure1.2 behavior and selected implementation interoperability; no source-specific performance number is inherited.

## SIGNAL DESIGN ASSESSMENT
Double Ratchet supplies per-message keys, bounded handling of skipped/out-of-order messages and compromise recovery under its assumptions. Header encryption is a specified variant, not evidence every library exports it. Current spec revision4, dated2025-11-04, also defines sparse post-quantum and Triple Ratchet extensions. Choosing classical Double Ratchet is distinct from adopting that full current profile.

PQXDH bootstraps asynchronous sessions using identity/prekey material and hybrid key agreement. Authenticated invitation pinning is still needed to establish whose identity keys these are; a valid prekey signature alone does not identify a dealer. A PQ bootstrap plus classical ratchet is not ongoing post-quantum compromise recovery. Specify exact KEM representation and algorithm rather than equating any library symbol called Kyber with required ML-KEM-768.

Sesame addresses asynchronous multi-device session management, but its presented model includes user/device directories, device mailboxes, recipient selectors and retry/receipt paths. Copying that infrastructure model directly would change MPE's privacy properties. Borrow local device/session lifecycle ideas while independently reviewing directory reads, retry emission and device fanout leakage. Single-device pilot avoids making this a first-release dependency.

## SESSION AUTHENTICATION IS NOT BUSINESS AUTHORITY
Signal's deniable authenticated communication is not a publicly verifiable signed instruction for a Midnight contract. Retain the separate inner application-signature layer binding genesis, target contract, action, logical identity, expiry and payload digest. Validate authorized publisher set, atomic consumption replay protection and actual anchored-body binding where required. 'Ratchet decrypted it' cannot authorize a settlement. Adding explicit business signatures means the resulting workflow should not be advertised as fully deniable.

## CONCRETE IMPLEMENTATION AND LICENSING CHOICE
Current libsignal uses Rust implementations with Java, Swift and TypeScript wrappers. README explicitly says use outside Signal is unsupported and APIs/bridges may change without notice. The TypeScript source exports processPreKeyBundle, signalEncrypt/signalDecryptPreKey and application-supplied SessionStore, IdentityKeyStore and prekey stores; Rust exports analogous protocol/state APIs. These make a backend integration experiment plausible, not a supported vendor SDK commitment.

The repository's license is GNU AGPLv3; Midnight Express's repo currently uses Apache2. Do not assume libsignal code can be relicensed Apache2, and do not assume wrapping it in a process erases any applicable obligations. Record dependency/code-copying boundaries and obtain a distribution/hosting license assessment before selecting a released dependency strategy. This observation is based on the actual licenses, not a final legal conclusion about a hypothetical combined product.

Three reasonable options to evaluate:
## 1. An isolated, explicitly AGPL-compatible libsignal experiment, pinned revision and adapter API, to measure concrete formats and state behavior.
## 2. A license-compatible maintained implementation of the required Signal-derived profile, independently verified before adoption. No such alternative has been selected or claimed audited by this review.
## 3. Implement from public specifications if necessary, accepting a significantly larger cryptographic engineering/review burden. Double Ratchet's specification declares itself public domain; specification availability does not automatically resolve rights for every included component or copied implementation.

Do not patch cryptography merely to make packet sizes or existing APIs convenient. No current generic libsignal header-encryption API was identified in the reviewed exports; explicitly verify or select another implementation. Outer MPE sealing hides the serialized packet on the wire, but that is not evidence of satisfying the exact encrypted-header session profile's semantics. A compatibility experiment must declare any deviation instead of claiming conformance.

## COMPOSITION OPTIONS AND CONTRACT BOUNDARY
Incremental option: keep the existing MPE envelope/profile and register a payload schema whose body is serialized Signal ciphertext. The MPE outer publisher signature then authenticates those payload bytes; a separate transferable business signature inside the ratcheted payload binds the actionable instruction. This is an application-layer experiment, not an assertion that the optional encrypted-header cryptographic suite is complete.

A contract effect needs to verify the exact authorized instruction and bind it through whichever nested encryption/serialization is committed by the anchored MPE body. libsignal decryption off-chain does not automatically become a Compact in-circuit proof. If the selected consumption circuit cannot prove the required inner-business-payload/outer-envelope relation, restrict the pilot to off-chain coordination and defer anchored contract consumption. Changing the MPE cryptographic suite instead requires explicit version, codec and API decisions; do not quietly replace the default profile.

An inner ratchet can protect content after old message-key erasure while a static outer recognition secret remains able to recognize historical envelopes after compromise. Keep content secrecy, recognition secrecy and outer-key exposure as separate advertised properties. Inner ratcheting does not repair recognition-secret compromise or traffic-analysis leakage.

## FEASIBLE FIRST PROTOTYPE
- Two backend participants, one device each, pinned identities obtained by authenticated invitation.
- Existing permissioned single-shard GossipSub overlay, durable stores and default whole-shard local recognition.
- A separately selected/pinned session implementation behind a small local adapter; no Signal service dependency.
- Signed RFQ/offer messages encoded inside ratcheted ciphertext, complete setup/session control protected by MPE rather than public addressing.
- Durable transactional session/key-store writes, bounded skipped keys, no auto business receipt/fetch or re-establishment triggered by recognition in default mode.
- First exercise coordination only. Settlement enabled only after signature/replay/binding proof checks pass.

MPE currently specifies these optional components already: CRY-028 encrypted-header pairwise packet; CRY-032 exact X25519/ML-KEM-768 PQXDH profile; CRY-033 wrapped bootstrap metadata; CRY-035 no weaker fallback; CRY-040 independent production composition review; FMT-035 sealed session control. This proposal is completion/validation of those targets, not an entirely new architecture. A libsignal experiment that differs from them must be labeled experimental and must not silently change normative suites.

## GROUPS ARE A SECOND PROJECT
libsignal exposes SenderKey distribution/group encryption primitives, but these are not a ready-made MPE group lifecycle or an MLS equivalence. Each group needs authenticated membership, sender-key distribution, removal/rekey boundary, history policy, compromise recovery and multi-device semantics. Pairwise fanout is a feasible small-group experiment with traffic scaling by recipients; it can expose group size/changes through volume. No guarantee of scalable groups follows from pairwise success. Evaluate sender-key/MLS approaches after the two-party composition and product needs are clear.

## GO/NO-GO GATES
## 1. Exact profile/API: serialize actual bootstrap/session packets including signatures, envelope overhead and padding. Every required message fits a permitted class or an explicitly authorized fragmentation path; unsupported profiles fail closed. Verify actual header-encryption and KEM compatibility, not library naming.
## 2. State safety: reorder/drop/replay messages; crash before/after state commit; restore old backup. No nonce/session reuse, unauthenticated state mutation or unbounded skipped-key derivation. Lost key state produces typed resynchronization/gap, not weaker encryption.
## 3. Metadata: hold public workload fixed while changing recipient interests. IDONTWANT, retries, prekey-directory reads, error paths and confirmation traffic must match the declared privacy policy. Do not inherit Signal-service metadata claims or global anonymity.
## 4. Recovery/secrecy: verify specified key-erasure and compromise-recovery scenarios, then test archival/backup tradeoff. Restoring an archive must not secretly restore erased ratchet secrets while claiming unchanged forward secrecy.
## 5. Authority: valid ratchet packet containing unauthorized, altered, expired or replayed signed instruction cannot effect target action; authorized instruction commits once; anchored commitment proves the same signed statement only when required binding passes.
## 6. Operations: bounded memory/storage, full-shard bandwidth, admission-verification cost and failure behavior measured on named backend/phone profiles. Private mobile retrieval remains unresolved by adding Signal cryptography.
## 7. Dependency/product: recorded license/distribution decision, pinned builds, API migration owner, upstream maintenance monitoring, no unsupported integration marketed as supported by Signal. Confirm onboarding and workflow requirements with prospective users.

## EFFORT BOUNDARIES
A crypto adapter experiment is smaller than a messaging product. Main work is state/recovery and envelope composition, then identities/prekeys, store reliability, proof authorization, mobile privacy and groups. Do not invent a calendar estimate before measuring format compatibility and deciding implementation/license ownership. A reusable session cryptographic component can reduce cryptographic implementation work; it does not remove independent composition review or the operational/product work.
