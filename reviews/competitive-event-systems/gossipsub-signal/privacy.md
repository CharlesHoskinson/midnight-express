# GOSSIPSUB + SIGNAL FOR MIDNIGHT EXPRESS — PRIVACY/SECURITY REVIEW
Independent review, 3 October 2026. Primary-source study; no repository edits or implementation/security claim. Fresh Scrapling snapshots and SHA-256 manifest are in gossipsub-signal-privacy-sources/source-manifest.json alongside this report.

## RECOMMENDATION
Yes: use GossipSub as the ciphertext dissemination transport and Signal-protocol mechanisms as a client cryptographic session layer. This is meaningful layering, not a dependency on the Signal messaging service. GossipSub is already the transport direction in Midnight Express; the consolidated requirements already contemplate encrypted-header ratcheted sessions under DEC-CRY-1. The real work is composing these components with recognition, invitations, offline devices, admission, retention and Midnight-verifiable publisher authority.

Do not claim that integrating libsignal alone implements MPE interest privacy, durable delivery, anonymous admission, group permissions, transferable signed business instructions or anchored contract reaction. Each remains a separate property and integration gate.

## 1. GOSSIPSUB 1.2: WHAT IT CONTRIBUTES
GossipSub propagates topic messages through a mesh and gossip control traffic; 1.1 adds attack-resilience/peer-scoring mechanisms. Version 1.2 adds optional IDONTWANT duplicate suppression. It does not natively provide MPE message expiry, application-level retention, store receipts, whole-shard recovery, recognition, admission proofs or business replay protection. Its control messages and mesh topic membership remain observable to peers.

Preserve StrictNoSign/anonymous outer publication and content-based application message IDs as specified by the chosen MPE profile rather than leaking sender PeerID/sequence through signed pubsub fields. This does not hide ingress connection identity. StrictNoSign refers to the pubsub wrapper; sealed publisher signatures remain necessary inside MPE.

The v1.2 spec allows IDONTWANT to be sent on first receipt even before application validation, and peers may ignore it without penalty. MPE must keep duplicate suppression tied to receipt of opaque envelopes, never successful recipient recognition. Implementation thresholds, control-message limits and cache lifetimes are not uniformly fixed by the spec; cross-implementation testing is required. A pubsub acknowledgement or successful publish call cannot mean recipient processing or persistent storage.
Sources:
https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.0.md
https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md
https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.2.md

## 2. SIGNAL KEY AGREEMENT AND CONTINUOUS RATCHETING
PQXDH supports asynchronous first contact using recipient prekey material and hybrid post-quantum secret establishment. Its current documented mutual authentication remains elliptic-curve based, so it must not be described as fully post-quantum authentication. Identity-to-wallet/device association, key changes, directory equivocation and identity misbinding remain application concerns; prekey signatures do not establish permission for a business action. Validate identity bindings with pinned/verified wallet-device credentials and explicit replacement policy.
Source: https://signal.org/docs/specifications/pqxdh/

The current Double Ratchet specification includes classical Double Ratchet, an encrypted-header variant, Sparse Post-Quantum Ratchet, and hybrid Triple Ratchet. Classical symmetric key progression plus fresh DH input provides different guarantees from SPQR's continuing post-quantum refresh. Triple Ratchet combines classical and post-quantum outputs. Signal announced SPQR rollout in 2025; do not stop architectural planning at PQXDH plus a classical ratchet. Pin an exact algorithm/version and measured implementation profile.

Header encryption also requires session association, explicitly outside that specification's scope. It does not itself give private pubsub message discovery. Bounded skipped-key retention and erasure make out-of-order processing possible with a finite exposure window; authenticated state changes must be failure-atomic. Recovery requires fresh uncompromised entropy, honest updates and correct erasure, not merely calling a session "recovered".
Sources: https://signal.org/docs/specifications/doubleratchet/ ; https://signal.org/blog/spqr/ ; https://signal.org/docs/specifications/mlkembraid/

## 3. SALTED RECOGNITION COMPOSITION IS AN EXPLICIT GATE
A Signal pairwise packet normally relies on session/device addressing. Midnight Express instead needs local classification of fixed-size opaque envelopes received for a whole shard. Keep sender/device/session identifiers, ratchet headers and counters inside the protected representation. Do not derive a public topic from a Signal identity, distribution ID or group.

The simplest incremental prototype carries serialized Signal ciphertext as an opaque application payload inside the EXISTING MPE envelope/suite, retaining salted recognition, outer encryption and padding. This preserves the outer format, subject to size/fragmentation limits. Its outer publisher signature authenticates the ciphertext payload, not the decrypted business instruction: a separate inner canonical signed instruction is required for that authority claim. An alternative that replaces the MPE seal with Signal-derived per-message sealing requires a NEW cryptographic profile, versioning, key/API design and independent review. Neither option is a security proof. An enduring recognition/outer-routing secret can enable matching BOTH historical and future envelopes in that secret generation when stolen, even if ratchet-erased inner content remains protected. Explicitly distinguish content forward secrecy from metadata forward secrecy.

If recognition itself rotates, offline peers need a bounded way to recognize future packets without missing the very key update they need to read. Deriving recognition solely from the next per-message key risks a discovery/key-update circular dependency. Reusing stable secrets solves discovery at a different compromise cost. Enumerate candidate current/next/skipped recognition windows, cap derivation work and bound retained state; measure collision/miss behavior, CPU and offline gaps. Do not extract arbitrary libsignal internal ratchet secrets through an unsupported API or hand-roll a new ratchet unnoticed.

The current MPE encrypted-header Double Ratchet target is not proof that libsignal exposes that exact variant. Assess actual supported API and wrapping semantics before claiming conformance. Ordinary opaque-packet embedding may retain different header/key exposures than native encrypted-header operation.

## 4. OFFLINE BOOTSTRAP AND MULTI-DEVICE
Sesame describes asynchronous multi-device session management, including device lists, active/inactive sessions and copies for a sender's other devices. Borrow those lifecycle ideas rather than Signal service mailbox addressing. MPE needs its own authenticated prekey/device directory, atomic one-time-prekey allocation, expired/revoked-device policy and replay-safe initialization. Wallet identity can authorize device keys without phone-number identities or Signal accounts.

Directory lookups and selective device mailboxes can reveal first-contact recipient interest. Classify them in the privacy model; strongest whole-shard receipt must not become selective server fetch when a session recognizes a message. First contact and postrecognition auto replies can reveal relationships even when all message bodies remain encrypted.

Fanout encrypts separate copies for multiple devices/recipients unless a separate group mechanism is used. Those copies consume envelope/admission/storage budgets; deduplication must preserve one business effect across device sessions. Loss of a device must not reconstruct deliberately erased session keys from a wallet seed. Durable state commit before publishing avoids key reuse; reject rollback/restored-state nonce or ratchet reuse. Archive ciphertext retention and skipped-key lifetime jointly bound readable recovery history.
Source: https://signal.org/docs/specifications/sesame/

## 5. GROUP SENDER KEYS ARE NOT PAIRWISE TRIPLE RATCHET
Current libsignal has sender-key group support: per-sender chain state, distribution messages and ciphertext signatures. Therefore it would be inaccurate to say Signal uses no signatures anywhere. A group sender-key signature authenticates that cryptographic sender-key context; it is not automatically a Midnight-verifiable business-role authorization over canonical effect inputs.

A shared sender-chain compromise can derive subsequent messages in that generation; the symmetric progression alone cannot provide pairwise-style fresh-secret recovery. Group removal needs fresh key distribution to remaining authorized devices, and epoch transition/race rules. Do not inherit pairwise SPQR/Triple Ratchet guarantees for sender-key groups without a specified composition. Key distribution and recovery must not reveal private member identifiers in public gossip. Initially test pairwise sessions and bounded recipient/device fanout; consider group design separately, including the already reviewed MLS alternative.
Sources: https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/sender_keys.rs ; https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/group_cipher.rs

## 6. SIGNAL AUTHENTICATION CANNOT REPLACE MPE BUSINESS SIGNATURES
Pairwise authenticated encryption/MAC verification proves session authenticity to its participants, but is not a transferable public proof that a named publisher authorized a canonical instruction. PQXDH explicitly pursues cryptographic deniability; signed prekeys attest key material, not invoice/payment/action semantics. A Midnight circuit receiving a MAC and shared secret cannot conclude that only the publisher created it.

Retain a distinct canonical authorized publisher signature, sealed in the encrypted application representation, with the existing MPE-CRY-021 domain/context/effect bindings. Existing MPE-CON-043, MPE-CON-044a/b and MPE-CON-060 govern authorization, atomic replay handling and signed-statement-to-anchored-Sealed-Body binding. Signal session identity and business authority must be separately mapped, scoped and revocable. A signature-valid packet from a session peer without the relevant business role cannot authorize settlement.

Adding deliberate publisher signatures means those business statements no longer have the same deniability goal as ordinary Signal conversation content. State this intentional tradeoff. Keep unrelated conversational messages distinct from executable signed statements.

Nesting ciphertext also affects the circuit binding obligation: anchoring an outer ciphertext and verifying an unrelated valid inner instruction is insufficient. Demonstrate that the particular anchored sealed representation opens to the exact authorized statement under the selected composition. Do not assume Compact can afford full Signal/PQ ratchet verification/decryption. Measure witness construction, signature verification and required opening/commitment checks, with cryptographic review.

## 7. ADMISSION, PRIVACY AND DURABILITY STAY SEPARATE
Signal keys do not prove a publisher's current Bus Registry membership or enforce anonymous publication quotas. Retain dedicated proof/admission nullifiers and production unlinkability work; neither prekeys nor GossipSub scores replace them. Retain anchored commitments, replicated stores, receipts and whole-shard recovery independently of Signal crypto state.

Neither component hides IP addresses, gossip topics, packet sizes, timing, fanout or recognition-triggered responses. MPE's fixed classes and whole-shard local processing remain necessary. No default delivery/read receipt, reactive selective retry, attachment fetch or per-message source-confirmation query follows recognition. Explicit authorized business actions can still reveal correlation; strongest transport interest privacy is not global traffic-analysis immunity.

## 8. IMPLEMENTATION AND MAINTENANCE
libsignal is AGPLv3; its README explicitly states use outside Signal is unsupported and APIs/bridge layers may change without notice. It offers Rust implementation with Java/Swift/TypeScript wrappers, not a supported commercial general-purpose messaging SDK. Pin dependencies, own upgrade/interoperability work and decide distribution/licensing compatibility before production adoption. Using protocol specifications is a different decision from linking libsignal code. Do not pretend protocol reuse automatically gives Signal service infrastructure or upstream support.
Source: https://github.com/signalapp/libsignal

## PROOF-OF-CONCEPT ACCEPTANCE GATES
## 1. Envelope captures expose no recipient, session, device, group ID or ratchet counter beyond approved outer fields; gossip wrapper has no publisher identity fields.
## 2. Matching/nonmatching local recognition keys generate identical strongest-profile retrieval/control/diagnostic traces; IDONTWANT depends on envelope receipt, never recognition.
## 3. Offline first contact, exhausted one-time prekeys, directory tampering, device revocation and identity replacement have explicit authenticated outcomes.
## 4. Loss/reordering and large counter gaps respect skipped-key/CPU limits; corrupt packets never advance durable state; restart cannot reuse send keys.
## 5. Current-state compromise cannot open erased historical content outside retained windows; fresh honest update restores the advertised security; recognition metadata exposure is separately tested.
## 6. Concurrent group removal/send is epoch-defined; removed members cannot derive subsequent fresh keys; sender-key groups have no untested pairwise recovery claim.
## 7. Valid session message with forged/unauthorized business signature is rejected; changing network/destination/action/expiry fails; repeated logical instruction executes at most once.
## 8. Inclusion proof for another envelope cannot authorize a signed instruction; actual circuit proof and cost evidence satisfy MPE-CON-060 when anchored publication is claimed.
## 9. Classical/PQ first-contact and ratchet packets fit selected fixed-size classes or the existing reviewed fragmentation profile; measure fanout, bytes/day, CPU and key-state growth.
## 10. Compare a minimal pinned libsignal adapter against the exact MPE encrypted-header requirement; approve licensing, upgrade ownership and compatibility boundaries before production.

Proceed with a pairwise OFF-CHAIN backend messaging proof of concept retaining the complete MPE policy layer. Treat on-chain signed consumption through nested ciphertext as a separate experiment; existing outer signatures and commitments do not establish that binding automatically. Keep group sender-key integration, private mobile retrieval and post-quantum wire/circuit composition behind explicit decisions until those experiments pass. This reuses mature transport and cryptographic ideas while leaving the novel composition visible and reviewable.
