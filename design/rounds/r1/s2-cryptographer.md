I propose a bounded, recipient-oblivious event bus: one common off-chain stream, encrypted ratchet headers, local recipient recognition, hybrid asynchronous session establishment, and anonymous publication stamps. Midnight supplies contract authorization, commitments, replay protection, and optional checkpoints; dedicated relays carry ciphertext. Launch with small subscriptions and explicit bandwidth limits. Do not promise global-observer anonymity, unlimited fan-out, or post-quantum recovery after compromise. Preserve Bitmessage’s recipient ambiguity, replace static encryption and shared identities, and require evidence before introducing delegated detection or stronger anonymity.

## D1 — Event format

**Evidence convention.** All proposed layouts, limits, topology choices, and acceptance targets below are **design assumptions**, not measurements or existing Midnight features. Calculations from them are **inferences**. Repository citations are relative to `/home/charl/midnight/`. `L9:` identifies the inspected `midnight-ledger` tag `ledger-9.1.0.0-rc.5`, commit `67f9f972`.

The node pins ledger 9, while the ledger working tree is ledger 8. Compact 0.33 explicitly introduces ledger-9 events; the support matrix lists mainnet toolchain 0.31.1. Therefore, deployment support for event anchors is **unknown**, pending activation verification. Sources: `midnight-node/Cargo.toml:472`, `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`, `midnight-docs/docs/relnotes/support-matrix.json:38`.

### Envelope

Use fixed-size binary cells of **1,024 or 4,096 bytes**. Integers use network byte order; reserved bytes must be zero. Reject unknown versions and suites before cryptographic work.

| Component | Bytes | Visibility |
|---|---:|---|
| Common header | 64 | Public |
| Encrypted recognition/ratchet header | 56 | Opaque |
| Encrypted, padded body | 550 or 3,622 | Opaque |
| Publicly verifiable publication token | 354 | Public |
| **Total** | **1,024 or 4,096** | |

The common header contains magic 4, version 2, suite 2, size class 1, flags 1, reserved 2, admission epoch 4, expiry 4, random nonce 16, and reserved padding 28 bytes. Relays see version, cryptographic suite, size class, coarse time, expiry, token issuer, and ciphertext equality.

For established sessions, the recognition plaintext is the standard Double Ratchet header: X25519 public key 32, previous-chain counter 4, current-chain counter 4 bytes. AES-SIV adds a 16-byte authenticator. Use the common 128-bit random nonce as an SIV nonce input. Derive appropriately sized SIV keys from ratchet keys with distinct HKDF-SHA-512 labels. This is a **proposed adapter requiring audit**; the Double Ratchet specification recommends SIV and requires non-repeating header nonces, with at least 128 bits of entropy when random. Source: `2016-signal-double-ratchet-spec`, inspected revision 4, §§4.2, 7.2.

The body plaintext contains:

- Secret topic identifier 16 bytes; logical event identifier 16.
- Publisher sequence 8; schema identifier 4.
- Kind 2; flags 2; payload length 4; creation time 8.
- Publisher Ed25519 signature 64.
- Payload and zero padding.

Thus a normal cell holds **410 application bytes**; a large cell holds **3,482**, before bootstrap-specific material. Ed25519’s 32-byte public key and 64-byte signature are confirmed by `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:100`.

The signature covers a canonical, domain-separated statement binding network, topic, event identifier, sequence, schema, creation/expiry times, payload digest, and intended contract when applicable. The body AEAD additionally authenticates the common and encrypted headers. Signing keys remain sealed and are pinned during subscription establishment. These signatures deliberately permit recipients to prove publisher statements; **deniability is not a requirement**.

Use a computed SHA-256 hash of the complete cell as its transport identifier. The sealed logical identifier deduplicates the same application event across recipient-specific ciphertexts and retransmissions with new stamps.

Payload kinds are application event, subscription control, key update, and snapshot. Schemas define their own canonical bytes. No executable payloads, compression, fragmentation, or selective external blob retrieval in version 1. Larger applications send separately authenticated events and accept the resulting traffic leakage.

Expire cells seven days after the end of their admission hour. Relays refuse expiry extensions and prune expired bodies. Expiry is authenticated; it is not a promise that third parties erase archives.

### Cryptographic suites and costs

Recommend **PQXDH with X25519 and ML-KEM-768, followed by encrypted-header Double Ratchet**. Bind the exact suite, network, identities, and bootstrap transcript. Require one-time prekeys; do not silently fall back to last-resort keys or classical establishment.

PQXDH parameterizes its KEM, but the supplied revision predates standardized ML-KEM. Selecting ML-KEM-768 and initializing the additional header keys are **integration assumptions requiring independent review**, not an already-proved implementation. Sources: `2023-signal-pqxdh-spec`, §§2.1, 3, 4.12; `2016-signal-double-ratchet-spec`, §§4.4, 7.1.

| Choice | Bytes and operations |
|---|---|
| Established event | Two SIV encryptions; chain KDF; one publisher signature. Receiver tries short header decryptions, then one body decryption and signature verification for a match. |
| PQXDH establishment | Four DH computations per side with curve one-time prekey; one KEM encapsulation/decapsulation; initiator verifies two prekey signatures; key generation and KDF work additional. |
| ML-KEM-768 | Public key 1,184; expanded private key 2,400; ciphertext 1,088; shared secret 32 bytes. |
| X-Wing alternative | Public key 1,216; ciphertext 1,120 bytes. Encapsulation includes one ML-KEM encapsulation and two X25519 computations. |
| Future ML-DSA-65 authentication | Public key 1,952; signature 3,309 bytes, versus Ed25519’s 32/64. One signing/verification operation per signed event. |

Sources: `2023-signal-pqxdh-spec`, §3.3; `2024-nist-fips203`, Table 3; `2025-draft-xwing-kem`, §§5.1, 5.4; `2024-nist-fips204`, Table 2.

A normal event with ML-DSA-65 replacing Ed25519 would grow from 1,024 to **4,269 bytes**, exceeding even the large class. Do not add PQ signatures invisibly: introduce a new class/version and recost dissemination.

Hybrid establishment targets resistance to passive harvest-now-decrypt-later attacks. Classical ratcheting provides conditional classical recovery; it **does not supply post-quantum PCS**. Triple Ratchet/ML-KEM Braid is the upgrade candidate. One ML-KEM public-key/ciphertext exchange alone costs 2,272 bytes; “45.44 bytes per message over 50 messages” is merely arithmetic, excluding framing, coding, and retransmission. Source: `2025-dodis-triple-ratchet`, abstract and §1; `2016-signal-double-ratchet-spec`, §§5–6.

## D2 — Definition of “private”

The launch security boundary is **content confidentiality and cryptographic recipient/topic concealment from infrastructure**, with endpoint authentication and bounded forward secrecy. It is not traffic unobservability.

**Assumptions:** authenticated confidential invitation delivery; uncompromised endpoints and randomness; correct implementations; an honest reachable storage operator for availability. Metadata claims below are **inferences about this design**, conditional on these assumptions.

| Observer | Learns | Intended concealment and limits |
|---|---|---|
| Relay | Adjacent peers/IPs, first-seen traffic, size, timing, expiry, issuer, ciphertext identifiers | No plaintext, topic, publisher signing key, or recipient selector. Direct ingress exposes the submitting connection. |
| Retrieval gateway/indexer | Client connection, cursor, online intervals, complete-stream downloads; requested chain contracts | No matching events when clients download everything and never report matches. Contract-filtered chain queries reveal interest in that contract. |
| Chain observer | Authorization/checkpoint contract, transaction timing, public transcript, commitments, public DUST fee | No off-chain plaintext from a hiding commitment. Contract identity and resulting public state changes remain visible. |
| Colluding minority | Union of local observations; issuer purchase/issuance timing if included | No new content access without keys. Can correlate publishing, recovery traffic, and client activity; no numerical anonymity guarantee. |
| Global observer | Network-wide timing/volume, participation, ingress/egress correlations | Content protection remains conditional; publisher unlinkability and relationship unobservability are **not guaranteed**. |

Content forward secrecy requires deletion of used message keys and obsolete session state. Retained skipped keys expose their corresponding messages. Current header-key compromise may identify archived messages within its retained ratchet interval; **metadata forward secrecy is weaker than per-message content secrecy**. Sources: `2016-signal-double-ratchet-spec`, §§4, 8.1–8.4.

PQXDH authentication remains classical. Midnight’s inspected proof system is PLONK with KZG over pairing-friendly curves, so the overall system is **not post-quantum secure**, even with hybrid payload establishment. Sources: `2023-signal-pqxdh-spec`, §4.1; `midnight-zk/README.md:12`.

Out of scope: malicious authorized recipients, screenshots/plaintext export, endpoint malware, civil-identity authentication, hidden participation, precise volume/timing privacy, guaranteed censorship resistance, and deniable publisher statements.

Reject the inference that replicated encrypted objects imply source anonymity. Loopix explicitly combines mixing, delays, and cover traffic; the anonymity trilemma bounds strong anonymity against a global passive observer under its modeled conditions. Sources: `2017-piotrowska-loopix`, abstract; `2017-das-trilemma`, abstract.

## D3 — Publish and subscribe model

### Addressing and discovery

There is **one network-scoped transport topic**, independent of application topics. Never put a topic hash, recipient identifier, stable session tag, signing key, or application group identifier into relay routing.

A subscription is a publisher-authorized, device-specific session plus secret application topic identifier. Version 1 supports **at most 32 recipient devices per publication** through independent ciphertexts. A recipient cannot impersonate the publisher to other recipients because application statements carry the publisher’s signature.

Discovery uses authenticated invitations delivered through an existing trusted application channel or in person. Public unsolicited first contact is excluded from version 1.

Each invitation contains a one-time PQXDH bundle, pinned publisher signing key, network/version metadata, and a random 32-byte bootstrap wrapping secret. A proposed compact bundle with three curve keys, one ML-KEM key, two signatures, three 4-byte prekey identifiers, wrapping secret, publisher key, and 16 bytes of metadata totals:

`96 + 1,184 + 128 + 12 + 32 + 32 + 16 = 1,500 bytes`.

The initial PQXDH fields alone occupy **1,164 bytes**: two curve keys, ML-KEM ciphertext, and three identifiers. Send bootstrap as a large control cell, sealed under invitation-derived header/body keys; therefore exposed identity keys and prekey identifiers never become relay selectors. Ordinary traffic begins after a session confirmation. Retries retransmit identical bootstrap objects; receivers cache their hashes and confirmation responses rather than reusing consumed prekeys.

These invitation and wrapping mechanics are **proposed composition**, requiring verification. PQXDH’s own requirements include authenticated identity comparison, deletion of one-time prekeys, unambiguous encoding, replay precautions, and KEM key binding. Source: `2023-signal-pqxdh-spec`, §§3.3–3.4, 4.1–4.3, 4.12–4.13.

### Recognition

Clients receive every admitted cell and trial-decrypt only its **56-byte encrypted header**. Try current, next, and retained historical header keys, plus pending invitation keys. Deduplicate identical header keys in the trial set.

Cap the entire recognition set at **256 keys**, including all categories; cap established sessions at 100. Verify admission and deduplicate transport identifiers before recognition. Commit ratchet changes only after body authentication succeeds.

This avoids expensive public-key trial decryption of every object. It also avoids giving a gateway any detection key. Encrypted-header Double Ratchet specifies trial recognition using current/next and skipped-message header keys. Source: `2016-signal-double-ratchet-spec`, §4.6.

Set `MAX_SKIP=1,000` per session and 4,096 retained message keys per device, with expiration after seven days or earlier explicit eviction. Crossing either key budget produces an explicit resynchronization requirement. **Storage availability does not imply decryptability after arbitrary gaps.** Source for the underlying trade-off: `2016-signal-double-ratchet-spec`, §8.4.

One-way publication does not automatically heal compromised state. Classical PCS requires fresh uncompromised bidirectional ratchet contributions and cessation of active interference. Control responses consume ordinary publication capacity; there are no automatic per-event read receipts. Sources: `2016-signal-double-ratchet-spec`, §§2.3, 8.2.

### Why not delegated detection?

- **FMD:** not the default. The supplied construction reports 68-byte flags, 1.927 ms generation, and 0.548 ms testing at \(p=2^{-5}\). At 10 cells/s and 10,000 clients, direct per-client testing extrapolates to **54.8 CPU-seconds/second**, before retrieval. False positives reduce downloading but introduce a different privacy model and statistical attacks. Source: `2021-beck-fmd`, §7, Tables 1–3 and “Lewis’s Attacks.”
- **OMR:** benchmark as the preferred scaling experiment. The original paper’s constructions have approximately 16/129 MB detection keys; catalog summaries disagree on baseline costs, so do not combine their figures. Source: `2021-liu-omr`, §1 and Table 2.
- **UnifOMR:** reports roughly 25 seconds and 4 MB communication for \(2^{19}\) messages of 612 bytes. That is promising evidence, not a performance prediction for our cells or user count. Source: `2026-fisch-unifomr`, abstract.
- **PIR:** useful only after solving which indices to retrieve without exposing recognition. OMR supplies that missing functionality; plain PIR is not a complete subscription protocol. Source: `2026-fisch-unifomr`, §1, “Why PIR and OMR differ.”

Reject public X-Wing first-contact scanning for launch. Its anonymity evidence is valuable, but confidentiality’s hybrid “either component” intuition does not automatically apply to anonymity: the supplied analysis requires weak anonymity of both components. Secret invitation wrapping avoids needing that property at ingress. Source: `2026-bao-anonymity-xwing`, §1.

### Delivery and consumers

Delivery is **at least once**, with per-publisher sequences and logical identifiers. There is no global total order. Persist application processing and cursor advancement atomically; reject duplicate logical events and expired statements. Request complete time ranges for back-fill, not matching object hashes. New subscribers receive an explicitly authorized snapshot; historical key distribution is not automatic.

Wallets and agents use a separate event SDK with local keys. This resembles the existing shielded wallet’s global-event replay, but is **new functionality**. Sources: `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:230`, `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:295`.

A contract cannot subscribe directly. An authorized off-chain agent decrypts and submits a follow-up transaction. The receiving circuit checks the publisher signature, network/destination/expiry, application predicates, and a destination-scoped replay nullifier. The signature and payload can enter as witnesses; only required effects and replay state are disclosed. Plain Ed25519 verification, persistent hashes/commitments, and block-time predicates are available. Sources: `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:993`, `:495`, `:511`, `:1261`.

A publisher signature proves a publisher statement, **not execution by an originating contract**. Contract-origin claims require a commitment recorded by the actual source contract and verification of its opening and provenance. Do not treat an arbitrary bus checkpoint as that proof.

For larger groups, evaluate MLS in phase 3. Reject shared-identity chans. MLS `PrivateMessage` still exposes group identifier and epoch in its framing, so transporting it directly would violate this addressing policy; hiding its framing needs a separately reviewed wrapper. Source: `2023-barnes-rfc9420`, §6.3.

## D4 — Sustainable model

Use **Privacy Pass publicly verifiable blind-RSA stamps** for launch admission. Its token occupies:

`2 type + 32 nonce + 32 challenge digest + 32 key identifier + 256 authenticator = 354 bytes`.

That is **34.6% of a small cell**. It buys public verification without a per-object Midnight proof. Sources: `2024-rfc9578-privacypass-issuance`, §§6.1–6.4, 8.2.2.

**Proposed redemption profile:** bind the challenge to network, epoch, class, expiry, and the hash of the header/encrypted contents, excluding the token. Relays reconstruct it. A copied token consequently authorizes only the same object. Issuer keys are shared by large epoch/class cohorts; prohibit individualized keys. Charge four capacity units for a large-cell issuer key, one for a small-cell key.

Object binding means issuance happens **after encryption**. It cannot be honestly described as unlimited prefetching of object-independent stamps. Issuers learn issuance timing; batching and purchase/issuance separation mitigate correlation without eliminating it.

Each distinct cell requires one RSA verification per relay. Issuance requires client blinding/finalization and issuer blind signing; request/response payloads total **515 bytes**, excluding HTTP. The challenge profile and multi-relay redemption require audit beyond the issuance RFC.

Publishers purchase prepaid service capacity through ordinary billing or a separately specified transferable-asset settlement. The service pool pays contracted relays for carrying/storage and gateways for subscriber egress. Subscribers pay for bandwidth tiers. Launch grants cover low utilization; hard capacity quotas and published prices govern overload. **Actual monetary prices and settlement choice are unknown** until operator quotations and measurements exist.

DUST pays Midnight transaction fees, not off-chain relay invoices. It is shielded, non-transferable, generated from NIGHT, and decays after backing NIGHT is spent. Sources: `midnight-docs/docs/concepts/dust-architecture.mdx:23`, `:104`, `:125`.

At inspected genesis parameters, one NIGHT’s cap is **5 DUST**: \(10^6\) Stars × \(5×10^9\) Specks/Star ÷ \(10^{15}\). The byte-only fee contribution is approximately **0.01 DUST per decimal KB**, before writes, churn, or a dominating compute/read term. Live prices are unknown. Sources: `midnight-node/res/mainnet/ledger-parameters-config.json:165`, `:169`; `L9:midnight-ledger/ledger/src/structure.rs:3362`; `L9:midnight-ledger/base-crypto/src/cost_model.rs:408`.

Do not infer relay rewards from fee payment. The inspected node reward hook returns `(0, None)`. Source: `midnight-node/runtime/src/lib.rs:681`.

For decentralization, prototype Compact membership-and-nullifier authorization with epoch and budget-index domains. It must bind the witness secret to the Merkle leaf. This extends the documented single-use pattern; it is **not an existing Midnight rate-limiting primitive**. Source: `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:176`.

Reject per-object ledger proofs at launch: a DUST spend proof alone is 2,912 bytes, and contract proof sizes vary. Reject PoW as primary financing/spam control: it pays no operator and the supplied critique identifies stolen-compute and heterogeneous-device problems. Sources: `L9:midnight-ledger/ledger/src/dust.rs:2158`; `L9:midnight-ledger/ledger/src/structure.rs:1908`; `2004-laurie-proofofwork`, §§3–4.

## D5 — Performance requirements

All rates count **ciphertext cells**, including recipient fan-out, bootstrap, and control traffic.

Assume 99% small and 1% large cells:

\[
S=0.99(1024)+0.01(4096)=1054.72\text{ bytes}.
\]

Reserve 25% for framing, inventories, retransmissions, and transport. This is a **planning assumption to replace with measurements**.

| Class/scenario | Requirement and calculated load |
|---|---|
| Mobile launch, aggregate 1 cell/s | 113.9 MB/day downloading; at most 256 header trials/s. |
| Desktop wallet/agent, normal 10 cells/s | 13.18 KB/s; 1.139 GB/day; at most 2,560 header trials/s. |
| Desktop stress, 100 cells/s | 131.84 KB/s; 11.391 GB/day; at most 25,600 header trials/s. |
| Relay, six-peer planning mesh | Budget six incoming plus six outgoing copies: 158.2 KB/s at normal load; 1.582 MB/s at stress load. |
| Gateway, 200 complete-stream subscribers | 2.637 MB/s normal; 26.368 MB/s stress, plus overlay traffic. |
| 50 gateways, 10,000 concurrent subscribers | Aggregate normal subscriber egress 131.84 MB/s, or 11.391 TB/day. |

For 32-recipient fan-out, normal capacity permits at most **10/32 = 0.3125 logical publications/s** before controls. Ten thousand subscribers can be concurrently connected; that does not mean ten thousand independently active publishers.

Publisher-side traffic additionally includes issuance’s 515 bytes and three storage receipts. With proposed 132-byte receipts, those add **911 bytes per cell**, before transport and invitation exchange.

**Acceptance targets:** after a valid stamp is obtained, off-chain delivery p50 ≤2 s, p95 ≤5 s, p99 ≤15 s under normal load. Stamp issuance p95 ≤2 s must be measured separately; end-to-end publication targets include both stages. At stress load, p95 ≤15 s and bounded queues; excess admission is rejected explicitly.

Target desktop header trials ≤5 μs and mobile trials ≤20 μs. These imply normal recognition CPU of 12.8 and 51.2 ms/s respectively; **they are benchmark targets, not observed performance**. Relevant events add body AEAD, signature verification, and occasional ratchet DH work.

On-chain throughput is a separate budget. With an assumed 8 KiB transaction, the normal-class byte ceiling alone gives:

\[
0.75×1{,}048{,}576/(8192×6)=16\text{ transactions/s}.
\]

This excludes compute, state-write limits, and all competing activity. Sources: `midnight-node/runtime/src/lib.rs:292`, `:300`, `:312`. No fixed contract-call proof size or measured private-event throughput was found.

Do not claim the 10-cell/s full-stream profile is inexpensive mobile operation. Require Wi-Fi/background synchronization there, or change retrieval architecture after evaluation.

## D6 — Storage requirements

Every launch storage relay keeps the complete admitted stream for seven days plus the current hour.

At normal load, seven days of raw cells occupy:

`10 × 1054.72 × 86,400 × 7 = 6.379 GB`.

A proposed 64-byte identifier/expiry/pointer index adds **0.387 GB/week**. Allowing 50% database overhead gives about **10.15 GB**, excluding temporary queues; provision **12 GB**. Stress retention requires roughly ten times that; provision **120 GB**. Fifty normal replicas retain approximately 319 GB of raw bodies collectively.

Clients retain session state, cursors, duplicate identifiers, and bounded skipped keys. The 4,096 message-key limit accounts for **131,072 bytes of key material**, excluding maps and other state. Saving plaintext or old keys for archival changes the forward-secrecy boundary.

A publication is “stored” only after receipts from three distinct operators. **Assumption:** at least one remains honest, reachable, and retains the object. Receipts are contractual evidence, not cryptographic proof of continued storage. Independent audits sample retrievability.

Archives are optional, separately funded full-stream services. Do not silently query an archive only for matching objects. Beyond retention, availability is explicitly unsupported unless archival service was purchased.

The ledger stores authorization state, consumed replay identifiers where required, and optional batch roots. Bulk ciphertext stays off chain. Publish one checkpoint per minute when enabled; its root establishes inclusion in the committed batch, **not global completeness or availability**. Anchor provenance remains visible.

Compact `Misc` supports only a 32-byte name and 256-byte payload. Ledger-9 separately drops emitted data exceeding its 1 KiB bound, although the VM accepts larger `log` arguments. These are different limits. Sources: `minokawa-compact/compiler/midnight-events.ss:71`; `L9:midnight-ledger/onchain-vm/src/vm.rs:39`, `:43`, `:274`.

Do not interpret either limit as private storage capacity. Logged values are public and log accounting charges churn. Source: `L9:midnight-ledger/onchain-vm/src/vm.rs:595`.

## D7 — Infrastructure actors

**Proposed launch actors:**

- Dedicated relays: validate stamps, deduplicate, gossip, and retain opaque cells.
- Gateways: serve complete streams and historical ranges; hold no recognition or payload keys.
- Issuers: enforce purchased capacity and blind-sign stamps. Trusted for quota discipline and availability, not content.
- Wallets/agents: hold device-specific keys, recognize locally, validate schemas/signatures, and initiate contract calls.
- Checkpoint adapters: submit commitments and monitor finalized chain data.
- Midnight validators/full nodes: provide their existing ledger service; no mandatory event relay duties.

Launch with at least five independent operator organizations, three accepted issuers, and three independent storage receipts. Organization independence is an **operational assumption**, not something peer IDs prove.

Stage decentralization by publishing operator terms, common issuer-key cohorts, objective stamp validation rules, interoperability tests, and self-hosted gateway software. Allow anyone to run a relay; access to issuer acceptance/payment requires published criteria. Permissionless, issuer-free admission is a later cryptographic/economic milestone.

Do not equate validator decentralization with bus decentralization. The inspected mainnet configuration has ten permissioned and zero registered committee candidates. Source: `midnight-node/res/mainnet/system-parameters-config.json:6`.

Separate payload, signing, invitation, admission, and wallet keys. Never hand the gateway wallet viewing keys or event recognition keys. The existing shielded wallet’s local replay path supplies the appropriate integration precedent. Source: `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:295`.

## D8 — Network tether

Recommend a **separate libp2p overlay with GossipSub dissemination and optional Midnight anchoring**.

The current node selects `sc_network::NetworkWorker`; its explicit registrations are consensus protocols and ledger sync. Extending that registry requires a node implementation change. Sources: `midnight-node/node/src/command.rs:326`; `midnight-node/node/src/service.rs:574`, `:610`.

Use one fixed overlay transport topic, application-defined content identifiers, peer scoring, outbound diversity, bounded validation queues, and independently sourced peers. Suppress author-identifying message fields/signatures at the gossip envelope layer; sealed application signatures supply publisher authentication. Verify the selected library’s policy and compatibility before implementation.

GossipSub scoring and outbound-mesh protections support resilience, **not anonymity guarantees**. Source: `2020-gossipsub-v11-spec`, “Outbound Mesh Degree” and “Peer Scoring.”

Version 1 requires:

- **Node:** no change.
- **Compact:** application contracts for authorization/checkpoints/consumption; no compiler or ledger primitive changes.
- **Indexer:** existing finalized-event interface for anchors; a separate service for off-chain cells.
- **Wallet/agent SDK:** new invitation, recognition, ratchet-state, and complete-stream synchronization support.

Indexer subscriptions expose a required contract address and inclusive cursor, then emit in monotonic local ID order. They are suitable for anchors, not hidden application-topic subscriptions. Sources: `midnight-indexer/indexer-api/graphql/schema-v4.graphql:548`, `:1967`.

**Fallback:** replicated gateways serving the same opaque stream with identical cryptographic framing and local recognition, with explicit reduction in decentralized dissemination. If contract events are not activated, omit event-log checkpoints or use an explicitly costed public state commitment. Do not move bulk data onto the chain as an automatic fallback.

The node bridge does not expose contract log payloads in its returned transaction event structure; the indexer is a distinct finalized-block consumer. Sources: `midnight-node/ledger/src/ledger_9/mod.rs:460`; `midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128`.

## D9 — Threats and open risks

| Threat | Proposed defense | Residual risk |
|---|---|---|
| Eclipse/Sybil | Multiple discovery sources, outbound diversity, operator diversity, retained peer scores | Peer IDs do not establish independence; routing capture remains possible. |
| Spam/CPU exhaustion | Class-priced stamps, cheap rejection first, duplicate caches, issuer quotas, bounded queues | Compromised issuer can mint capacity; RSA admission is not PQ secure. |
| Source deanonymization | No application routing tags; optional independently evaluated anonymity transport | Direct ingress, issuer timing, and global correlation remain exposed. |
| Recipient probing | Complete-stream download; no match callbacks/read receipts | Application reactions, reconnects, and resynchronization can identify interests. |
| Replay/rollback | Cell hashes, logical identifiers, signed destination/expiry, contract nullifiers, atomic state updates | Restored backups can reintroduce keys/counters unless explicitly handled. |
| Key compromise | One-time prekeys, erasure, ratchets, device revocation and re-invitation | Active interference prevents healing; header/history exposure; no PQ PCS. |
| Gateway withholding | Multiple providers, storage receipts, checkpoint comparisons | Availability and completeness are not guaranteed by a root. |
| Ledger censorship | Off-chain delivery continues without fresh checkpoints | Required authorization or contract consumption can still be blocked. |

The safe-mode filter intentionally excludes ordinary user transaction submission. Source: `midnight-node/runtime/src/check_call_filter.rs:44`.

Treat composition as the leading cryptographic risk. The 2026 Double Ratchet analysis reports three forward-secrecy attacks and only partial proofs for encrypted headers and PQXDH composition. Its inability to prove full encrypted-header PCS was a resource limitation, not a proof of security or an attack. Source: `2026-cheval-dr-automated`, abstract, §§3, 5–6.

Reproduce those attacks against the chosen implementation. Test null receiving-chain handling, initial-state reuse, replay, malformed curve encodings, prekey exhaustion, and failure atomicity.

Reject “the standard parts make the composition standard.” Our invitation wrapping, header initialization, admission challenge, signing semantics, and contract bridge are new integration surfaces.

## D10 — Build and verification plan

1. **Freeze cryptographic profile.** Specify exact encodings, labels, signed bytes, key separation, prekey lifecycle, header-key initialization, and token challenge reconstruction. Produce deterministic vectors. Audit ML-KEM/PQXDH integration and the SIV adapter. Gate: no unresolved critical/high findings or successful reproduction of the three cited ratchet attacks.

2. **Build a bounded transport prototype.** Use memory-safe parsers, explicit limits, admission caching, complete-stream range retrieval, receipts, and atomic client state. Gate: interoperable implementations reject every malformed/version-downgrade vector and remain within declared memory/key budgets.

3. **Simulate and benchmark.** Exercise 10,000 subscribers, 50 gateways, normal/stress rates, recipient fan-out, offline back-fill, 20% operator outages, malicious peers, issuer failure, and correlated providers. Measure percentiles, actual transport overhead, signature/SIV/KEM costs, storage amplification, and retrieval failures. Gate: D5 targets and seven-day retention budgets hold; measured economics fund operators.

4. **Verify Midnight integration separately.** Compile circuits enforcing leaf binding, signature assertions, destination/expiry, and replay rules. Check hidden witnesses and actual transcripts. Gate: duplicate consumption fails, unauthorized or expired statements fail, and disclosed fields match the leakage table. Verify actual deployed ledger/toolchain activation before enabling log anchors.

5. **Evaluate scaling and stronger privacy.** Compare full download against FMD and UnifOMR on identical cells and workloads. Separately evaluate MLS groups and Triple Ratchet/header concealment. A mixnet profile needs its own cover-traffic, latency, operator, and adversary budget; Loopix’s paper results are not this system’s benchmarks.

**Change course** if recognition exceeds its CPU budget, full-stream mobile traffic is unacceptable, large fan-out dominates capacity, issuer correlation defeats the required threat model, or ratchet composition cannot be independently validated. A requirement for global-observer anonymity changes the transport architecture. A requirement for post-quantum PCS changes the session protocol. Neither is a wording change.

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Fixed padded cells; sealed signatures; hybrid setup and encrypted headers | Static recipient encryption; public session tags; uncosted PQ signatures | `2016-signal-double-ratchet-spec` §§4,7; FIPS 203/204 tables | Medium | Composition audit fails; measured cell utilization is unacceptable |
| D2 | Conditional content/recipient concealment; explicit metadata leakage | Global anonymity from flooding alone | `2017-das-trilemma`, abstract; PQXDH §4.1 | High | Stronger adversary requirements become mandatory |
| D3 | Invitations, local header trials, ≤32-device fan-out | Public first contact; default FMD; shared identities; bare PIR | DR §4.6; FMD §7; UnifOMR §1; MLS §6.3 | Medium | Retrieval or group alternatives meet the same privacy at lower measured cost |
| D4 | Paid blind stamps; DUST only for ledger operations | PoW financing; DUST relay payments; per-cell ledger proofs | RFC 9578 §6; `dust-architecture.mdx:23`; L9 `dust.rs:2158` | Medium | Issuer-free admission proves affordable and sustainable |
| D5 | 10 cells/s normal; 100 stress; explicit mobile boundary | Unlimited logical event rates or free fan-out | Proposed workload arithmetic; `runtime/src/lib.rs:292`, `:312` | Medium | Benchmarks or product demand invalidate budgets |
| D6 | Seven-day complete replication; roots offload no availability duty | Permanent ledger ciphertext storage; guaranteed archival | L9 `vm.rs:43`, `:595`; `midnight-events.ss:71` | High | Required offline window or operator costs differ materially |
| D7 | Independent dedicated relays/gateways/issuers | Mandatory validator relay service; keys held by providers | `system-parameters-config.json:6`; wallet `Sync.ts:295` | Medium | Funding or independently operated infrastructure cannot be secured |
| D8 | Separate overlay; optional ledger anchors; gateway fallback | Consensus-network modification; ledger-only bulk transport | `service.rs:574`, `:610`; indexer schema `:1967` | High | Midnight ships a suitable isolated application transport |
| D9 | Bounded defenses with explicit composition and correlation risks | Automatic PCS, anonymity, or completeness claims | `2026-cheval-dr-automated` §§3,5; DR §8 | High | New attacks or stronger assurance alter the threat boundary |
| D10 | Audit, vectors, simulations, deployment checks, measured gates | Shipping on literature microbenchmarks alone | Cited ratchet analysis; inspected Midnight generation differences | High | Independent evidence satisfies—or disproves—the gates |