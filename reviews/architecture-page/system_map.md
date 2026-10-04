# Midnight Express architecture page: system map

The repository is at the design/exploratory stage. The selections below name existing libraries and documented protocol responsibilities; they do not establish a running or accepted Midnight Express integration.

## Component inventory

| Component | Role and connection | Existing primitive versus proposed integration |
|---|---|---|
| Applications and adapters | ERP, agent, wallet and Midnight applications issue signed business intent through a typed event/workflow SDK. Adapters declare source identity, versions, snapshot/delta and finality. | Application-owned adapters and SDK behavior remain custom work. CloudEvents-compatible payloads and AsyncAPI supply contract conventions, inside encryption. |
| Rust MPE core and GossipSub sidecar | Seal fixed-class envelopes; publish through rust-libp2p GossipSub v1.2 with anonymous message fields, validation and peer scoring. Receive whole shards; enforce application expiry on cached/queued sends. | Rust/libp2p exists. MPE profile, envelope integration and expiry acceptance remain implementation obligations. Default private profile has no business topics or content-aware routing. |
| MPE sealing and local recognition | AEAD, signatures and salted local recognition protect semantic headers and let recipients recognize locally after whole-shard reception. Source/type/correlation/role stay encrypted. | Original MPE symmetric profile is retained for launch. Static streams do not establish forward secrecy or ingress anonymity. |
| Semaphore-derived membership module | Independent admission identity → profile commitment → registration → finalized Registry snapshot → private insertion/removal witness. Owns disciplined scoped nullifiers and versioned parameters. | Semaphore provides reusable lifecycle/API patterns. Runtime library reuse requires exact commitment/hash/field/tree compatibility; no automatic compatibility with RLN or Midnight. |
| Midnight Registry | Authoritative finalized membership roots, committed member limits, revocation and bounded root grace. Feeds witness/admission policy. | Custom Registry and finalized-ledger adapters remain required. Root changes must not renew spent credits. |
| One RLN-style admission proof | Envelope plus membership witness → one proof of membership, committed per-class credits and envelope-bound abuse shares. Bus nodes verify and durably record duplicate/equivocation state. | Zerokit is the preferred evaluation engine, pending adaptation and measurement. No second Semaphore membership proof per event, no per-envelope Registry write and no global quota serialization claim. |
| Opaque retained-envelope stores | GossipSub traffic → custom replicated MPE store protocol → opaque retained envelopes and signed persistence receipts → receiver recovery. | Custom protocol, replication, retention and receipts remain unfinished requirements. A database does not implement them. Store/relay operators receive neither plaintext nor application keys. |
| Endpoint inbox and recovery | Receiver/local recognition → durable inbox → authenticated handler/application policy → atomic local effect, dedup, outbox, checkpoint and cursor → explicit signed business acknowledgement. | SQLite is the standalone Rust/client option. UmbraDB + PostgreSQL is selected for a trusted Node >=24 backend host with one writer; the required MPE atomic recovery capability is a future release. Existing `saveAndAdvance` covers checkpoint/cursor only. |
| Optional OpenMLS security | Session/group security inside MPE composition, connected to identities and durable epoch/rekey recovery. | Existing OpenMLS implementation; proposed optional integration. First pilot keeps symmetric launch profile. Credential, metadata, wire-fit, rekey and crash/erasure gates must pass before deployment. Signal is a deferred alternative, not a parallel required dependency. |
| Midnight Anchor and consumer adapters | Bus windows → Midnight commitments. Authenticated workflow + anchor evidence → authorized reaction proof → contract verifies and atomically commits an effect. | Custom Anchor, authority/binding circuits and consumer adapters remain required. Signed authority, replay nullifiers and anchored-message binding are separate from transport protection/inclusion. |
| Operations and SDK outcomes | Bounded listeners, failures/gaps/expiry/recovery, privacy-preserving metrics, encrypted quarantine and authorized redrive. | Custom product semantics; distinguish admission, persistence, anchor finality, processing and business completion. `once` means listener behavior, not exactly-once business execution. |

## Diagram connections

1. Application → SDK → signed intent/application policy → MPE seal → one RLN admission proof → GossipSub overlay.
2. Independent admission identity and Semaphore-derived witness lifecycle → finalized Midnight Registry roots → the same RLN admission proof.
3. GossipSub → whole-shard receiver/local recognition; GossipSub → opaque replicated stores → receiver recovery.
4. Receiver → endpoint durable inbox → authenticated handler/policy → atomic local commit → explicit signed acknowledgement.
5. GossipSub windows → Midnight Anchor; handler/policy + anchor → authorized reaction proof → contract effect.
6. Optional OpenMLS sits within the MPE security composition. UmbraDB/Postgres or SQLite sits inside the endpoint trust boundary, separate from replicated opaque stores.

## Inaccuracies to avoid

- Presenting the selected stack as already built, production-ready or integration-accepted.
- Drawing Semaphore as a second per-message proof or as an independent authoritative membership tree alongside RLN.
- Treating Semaphore v4 identity/tree semantics as automatically compatible with Midnight/RLN.
- Describing Zerokit as an accepted plug-in solution: proof relation, adaptation, slot-size and verification performance remain gates.
- Claiming UmbraDB currently provides atomic MPE effects/dedup/outbox/checkpoint/cursor; its MPE capability is proposed future work.
- Embedding UmbraDB in Rust or using it as the replicated retained-envelope protocol; it runs in a trusted Node backend host.
- Making OpenMLS mandatory for the first pilot, claiming it replaces recognition or grants contract authority, or installing Signal alongside it by default.
- Equating admission, retention receipt, anchor inclusion, handler execution and business acknowledgement.
- Implying every message requires a ledger transaction or contract effect.
- Claiming launch forward secrecy, ingress anonymity, guaranteed private mobile reception, exactly-once business execution or automatic settlement.
- Treating inclusion/encryption as business authorization; contract effects need signed authority, atomic replay protection and anchored-message binding.
