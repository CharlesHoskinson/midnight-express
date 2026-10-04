# Midnight Express: GossipSub + Signal architecture review (independent reviewer 1 of 3)
Evidence verified 2026-10-03 America/Denver through official web documentation and Scrapling source snapshots in review-gossipsub-signal-architecture-sources/manifest.json. Research recommendation only; no integration, proofs or network benchmarks performed.

Verdict
The composition is technically plausible and useful: GossipSub carries opaque ciphertext; Signal-family libraries protect conversations; Midnight Express supplies sealed routing/recognition, admission, retention and ledger commitment. Neither component replaces the existing product contract. Adopt an explicitly versioned Signal payload profile first for one-to-one/device sessions. Keep group mode a separate decision and integration gate. This is not interoperability with Signal's hosted application/service, and does not inherit its complete metadata/privacy system.

## 1. GossipSub design study
Primary sources:
https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md
https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.2.md
https://github.com/libp2p/rust-libp2p/blob/master/protocols/gossipsub/src/config.rs
https://github.com/libp2p/rust-libp2p/blob/master/protocols/gossipsub/src/protocol.rs

Mechanism: mesh forwarding plus gossip repair, peer scoring and duplicate suppression. Version1.2 adds IDONTWANT to reduce repeated delivery, not durability or message authority. Its spec is currently an active working draft, with implementation-specific policies. Nodes advertise /meshsub/1.2.0. Peer scoring and limits need a shared network profile.

Current Rust source's default protocol list includes1.2; ConfigBuilder custom protocol_id/prefix paths still only select1.0/1.1 behavior. Do not call a custom string ending1.2 while selecting1.1 and claim interoperability. Pin the actual crate/commit, use the existing standard identifier plus network-specific topics, or deliberately maintain/test a reviewed upstream patch. The design already identifies this issue.

Adaptation: admission validation precedes propagation; fixed wire bounds and verification work quotas remain. Message identity must follow existing MPE canonical identity, not mutable peer/source sequence fields. Duplicate controls concern opaque envelope reception, never successful private recognition. GossipSub provides no global order, delivery completeness, retained history or publisher anonymity; stores and client recovery remain separate subsystems.

Acceptance: cross-implementation1.2 negotiation and IDONTWANT conformance; agreed peer scoring and abuse limits; malformed/over-budget proof rejection with bounded verification work; dedup/repair under loss; disconnected catch-up through retained stores. Changing local recognized interests must not alter mesh control messages. Ingress can still see publisher IP/connection and first-hop timing.

## 2. Signal design study
Primary sources:
https://signal.org/docs/specifications/pqxdh/
https://signal.org/docs/specifications/doubleratchet/
https://signal.org/docs/specifications/sesame/
https://github.com/signalapp/libsignal
https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/lib.rs
https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/session_management.rs
https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/group_cipher.rs
https://github.com/signalapp/libsignal/blob/main/rust/protocol/src/storage/traits.rs

PQXDH supports asynchronous first contact using authenticated identity/signed prekeys and one-time/KEM prekeys. It needs a key directory and verified identity binding. A malicious directory can withhold material; use a verified wallet-to-installation binding, explicit identity-change handling, and resource-limited prekey access. Directory lookup itself can disclose recipient interests; Signal cryptography does not make lookup private.

Double Ratchet advances message keys, supports bounded skipped-message keys for reordering, and relies on key erasure and fresh key exchanges for recovery. Current official specification also includes Sparse Post-Quantum Ratchet and hybrid Triple Ratchet. PQXDH plus a classic elliptic-curve ratchet alone is not a blanket claim of ongoing post-quantum compromise recovery. Pin the exact libsignal version and suite actually exercised; benchmark its full serialized initial/update messages against the existing Envelope classes. Do not invent a smaller incompatible variant.

Sesame addresses asynchronous multi-device session management: identity/device records, session selection and stale-session recovery. Implementing a codec alone does not implement that lifecycle. Encrypt to each authorized recipient device and any required sender-linked device; directory revocation and atomic session state updates are product responsibilities. Never use one shared pairwise ratchet concurrently across independently advancing devices.

Current libsignal source exports process_prekey_bundle, message_encrypt, message_decrypt and storage traits for identity, session, prekey, signed/KEM prekey and sender-key records. Wrap these through a pinned adapter with transactional encrypted storage, not copied cryptographic code. Runtime session state, outgoing ciphertext/outbox and consumed one-time prekeys need crash-safe persistence and rollback handling.

Business authority is separate: pairwise session authentication is not a transferable wallet signature or contract authorization proof. Keep the existing signed workflow payload with recipient/target/action/expiry/domain binding inside session encryption, and satisfy MPE-CON-043/044a/b/060 before any effect. Proving a decrypt-and-signature relation against nested ciphertext may change circuit cost; this is a measured experiment, not an inherited property of libsignal.

## 3. Concrete composition

Publisher application
  signed/versioned workflow payload
       |
  Signal session encryption (per-device pairwise initially)
       |
  versioned Signal ciphertext container
       |
  EXISTING MPE sealing/padding + salted Recognition Tag
       |
  bounded MPE Envelope + admission evidence
       |
  Bus ingress validates admission/format/expiry
       |
  GossipSub1.2 full-Shard opaque propagation
       |                          |
  recipient receives wholeShard   Store Nodes retain same Envelope bytes
       |                          |       |
  local recognition -> MPE open   replay/repair   ciphertext commitment -> Anchor
       |
  select verified local Signal session -> libsignal decrypt
       |
  verify schema/signed workflow/finality/replay policy -> handler/effect

Directory/control lane: authenticated installation and prekey bundles -> Signal session setup. Its lookup/distribution privacy is an explicit separate dependency, not a visible recipient topic in the relay mesh. Initial discovery needs an existing consent/invitation/bootstrap key or a reviewed introduction mechanism; Signal prekeys do not by themselves supply MPE recognition secrets.

Proposed conservative wire choice: retain existing MPE outer framing and AEAD; set the MPE Message payload schema to a versioned container of serialized Signal ciphertext, then apply the existing MPE signed statement/sealing to that ciphertext payload. The outer MPE signature authenticates the ciphertext container; an inner signed business instruction independently authenticates plaintext effect inputs. This adds encryption/size overhead but avoids silently replacing current normative sealing and recognition semantics. Any future single-layer merge, including a Signal-derived per-message key replacing the MPE encryption suite, is a separately reviewed protocol revision needing library API work, version negotiation, binding and interoperability evidence. Put Signal headers, installation/session identifiers, business labels, group distribution identifiers and message types inside the encrypted MPE body, not public GossipSub fields. Existing transport size classes and admission slots remain fixed unless explicitly revised.

Recognition-state separation: stable recognition/invitation secrets help locate ciphertext but must not be reused as Signal message keys. Compromise of static MPE outer keys/recognition secrets can expose inner ciphertext and stream linkage, while Signal session plaintext can remain protected by erased ratchet keys. Conversely Signal compromise recovery does not automatically heal these outer metadata/recognition secrets. State the separate history-linkage and plaintext-forward-secrecy properties honestly.

## 4. One-to-one, multicast and groups
One-to-one: one device session ciphertext per authorized device, separately sealed; account-level delivery tracks device coverage privately. Extra linked-device copies increase bytes and admission spend, so benchmark bounded devices/fanout.

Multicast: a pairwise ratchet ciphertext is not decryptable by all members simply because GossipSub broadcasts it. Initial group prototype may use pairwise fanout, with cost proportional to recipient devices and an explicit group membership/version commitment in the signed inner payload. Avoid assuming all recipients saw identical transcripts: overlays may omit or reorder messages.

Sender Keys: current group_cipher exposes group_encrypt/group_decrypt and sender-key distribution creation/processing. Each sender's distribution material is delivered through authenticated pairwise sessions; group messages advance that sender chain and carry its signing information. This is a real separate Signal group primitive, not MLS. Membership and distribution state require application-level policy. Rotate affected sender distributions at removals before accepted subsequent group sends; old access cannot be revoked. A compromised sender chain permits future-key derivation until fresh secret distribution; do not inherit pairwise DH-ratchet post-compromise security for group mode. Enforce independent sender authorization before accepting new distribution material. Hold this mode behind group-specific state, revocation and audit gates.

## 5. Offline, archival and privacy boundaries
Offline recovery: stores keep ciphertext, not Signal private keys. Recover/replay original bytes; do not re-encrypt a network retry as a fresh Signal message unless intentionally creating a new application send. Skipped-key bounds, store retention and prekey lifetime are distinct clocks. Large out-of-order gaps or deleted sessions must produce an explicit recovery failure, not unlimited skipped-key storage or silent insecure fallback.

Archival: retaining encrypted transport transcripts can coexist with key erasure; recovering all old plaintext on a new device requires retained/exported decryptable history or secrets and therefore changes compromise exposure. Archive decrypted history under a separate user-approved recovery key if required; clearly separate that profile from strong ratchet erasure. Never silently resurrect deliberately erased ratchet keys from backups.

Privacy: GossipSub ingress still sees IP/timing; wholeShard reception hides local recognition conditionally; neither Signal ratchets nor sealed headers hide global traffic correlation. Signal's separate sealed-sender feature has certificates/service/delivery-token assumptions (https://signal.org/blog/sealed-sender/); importing its names alone supplies neither anonymous ingress nor private MPE admission. Keep acknowledgements, directory access, source confirmation and attachment fetches recognition-independent in strongest mode or explicitly declare a weaker mode.

## 6. Dependency and adoption gate
libsignal README says use outside Signal is unsupported and APIs may change. The current project is GNU AGPLv3, with protocol source SPDX AGPL-3.0-only. Record a pinned commit/release, full license inventory, integration ownership and planned source/compliance disposition before implementation; obtain license review for actual distribution/service composition rather than inferring obligations from the name. Reuse maintained crypto through an adapter; do not reimplement ratchets to avoid integration or licensing constraints.

Approval recommendation: approve an architecture experiment, not a production security claim. Start with an off-chain one-to-one pairwise-device pilot: codec, authenticated directory and crash-safe session stores with existing MPE envelopes. Claim no contract-consumption binding from that pilot. CON-060 proof over nested ciphertext and plaintext instructions is a separate circuit-design/cost gate. Gate on valid/tampered prekey tests, identity substitution, device removal, crash after encryption before publish, duplicate replay, bounded reorder gaps, retention exhaustion, packet-trace interest independence, group old-key rejection, suite size budgets, cross-implementation GossipSub conformance and license/dependency support plan. Preserve all existing authorization, replay, anchor binding and privacy requirements.
