# Original requirements: GossipSub, Signal and the remaining stack

**GossipSub and Signal can supply transport and optional session security. They cannot, by themselves, satisfy the complete Midnight Express requirements.** The most important additional cryptographic component for production is anonymous membership/quota admission. RLN is a promising candidate. Durable storage, private recognition, ledger integration, business authority and operations remain separate work; no universal third messaging protocol supplies them all.

Three independent agents re-read the original design and assessed every requirement area and each open-source component: [architecture](../../reviews/competitive-event-systems/requirements-fit/architecture.md), [privacy](../../reviews/competitive-event-systems/requirements-fit/privacy.md), [product](../../reviews/competitive-event-systems/requirements-fit/product.md), and [component coverage](../../reviews/competitive-event-systems/requirements-fit/coverage.json). This is a documentary feasibility assessment. No integration, benchmark or cryptographic acceptance check has run.

## What the original PDF actually requires

The Downloads PDF and repository PDF are byte-identical: SHA-256 `5ce38c65b5bbfd1409d61cac0e3a294f2ba16370fd8a857e1d5d4fb6c573e0ed`, 464 pages. The consolidated register contains 625 records: **510 live obligations**, 113 same-obligation references and two withdrawn tag-lookahead records. [Complete inventory and alias resolution](../../reviews/competitive-event-systems/requirements-fit/requirements-inventory.json).

The launch cryptographic profile is already defined: symmetric stream secrets, salted local recognition, ChaCha20-Poly1305 sealing and signed publisher statements. The PDF explicitly makes ratcheting an **optional pairwise profile**, with no forward-secrecy claim for launch broadcast streams. Signal is therefore an extension to that scope rather than a prerequisite for all messages. See printed pages 64–65, 87–89 and 134, DEC-002/020/021, and `MPE-CRY-001/026` in [the PDF](../design-document/Midnight-Express-Design-Document.pdf).

The salt, nonce and Recognition Tag are a clear prefix structurally **inside the Sealed Body**. “Inside the body” must not be mistaken for encrypted. Infrastructure can read those values, while matching is local and keyed. Existing requirements, not Signal, define their privacy behavior (`MPE-FMT-051`, `MPE-CRY-013/015`).

## Fit across all twelve requirement areas

“Partial” means useful supporting mechanisms, not demonstrated satisfaction. No complete area can be certified by selecting these dependencies. The [inventory](../../reviews/competitive-event-systems/requirements-fit/requirements-inventory.json) assigns every record to an area, preserves withdrawal/alias metadata and records that implementation satisfaction remains unproven.

| Area | Live obligations | GossipSub + Signal fit | Remaining responsibility |
|---|---:|---|---|
| FMT: format | 55 | Partial | Fixed classes, sealed semantic metadata, canonical IDs, codecs and carried-event identity |
| CRY: cryptography | 40 | Partial | Exact MPE suites, recognition, wallet/device binding, erasure, recovery and independent business signatures |
| PUB: publishing | 40 | Partial | Invitations, retries, whole-shard reception, reconciliation, cursors and explicit gaps |
| CON: consumers | 38 | Partial | Finality states, atomic local effects, action authorization, replay and anchored-message binding |
| ECO: admission/economics | 51 | Outside | Genuine anonymous quotas, membership roots, allowance abuse evidence and funding |
| NET: networking | 69 | Partial | MPE profile configuration, expiry-aware sends, Registry bootstrap, store/gateway/ledger adapters |
| PRF: performance | 43 | Outside guarantees | Measured composed throughput, latency, resource use and mobile budgets |
| STO: storage | 38 | Outside | Durable retention, replica receipts, recovery, pruning and available key history |
| OPS: operations | 45 | Outside | Operators, governance, payment, rollout, release and incident processes |
| PRV: privacy | 34 | Partial | Recognition-invariant traffic, leakage profiles, private retrieval and selective disclosure |
| SEC: security | 20 | Partial | Admission/parser/state abuse defenses and business-policy enforcement |
| VER: verification | 37 | Outside | Actual interoperability, proof, workload, adversarial and deployment evidence |

Sources: [Appendix A](../design-document/build/appendix-a.md), [consolidated register](../design-document/build/ears-consolidated.json), and the three independent fit reviews above.

## The missing pieces and useful open-source options

### 1. Anonymous admission is the first additional protocol candidate

Neither Signal session authentication nor GossipSub peer scoring proves that an anonymous publisher holds a valid membership and remaining allowance under a finalized Midnight root. Evaluate **Waku RLN with Zerokit** as a proof engine. Zerokit implements RLNv2 in Rust with Circom/Groth16 support, FFI/WASM and multi-message-ID allowance consumption. [Zerokit](https://github.com/vacp2p/zerokit), [Waku protocols](https://docs.waku.org/learn/concepts/protocols).

It is not a drop-in proof for the MPE statement. Bind the network/genesis, Registry, membership root, admission window, size class, credit and envelope identity; reconcile hash/field/circuit choices with Midnight. Measure the actual serialized proof package and verification time against the PDF's **4,096-byte encoded Admission Slot and 10-ms verification prototype measurement gates** (`MPE-ECO-048`); the slot is `roundUp64(104 + proof_length)`, not just the raw proof. Implement replay retention, root freshness, equivocation evidence and Registry revocation. An Ethereum-backed Waku registration path is not automatically a Midnight adapter.

RLN detects repeated allowance use when conflicting publications meet; it does not guarantee a globally serialized admission count before propagation. Several ingress nodes can initially accept conflicts. Preserve the PDF's explicit measurement of that exposure and domain-separate the relation to prevent cross-network accidental secret disclosure. See printed page 88 and `MPE-ECO-017/018/019/021/022/048`.

### 2. Durable recovery needs storage and an MPE protocol

GossipSub's duplicate cache is not the required 48-hour store. Signal session persistence is not replicated message availability. Use **SQLite** for a modest pilot/client store or **RocksDB** where measured node workloads justify it, then implement MPE's whole-window backfill, signed persistence receipts, replica selection, pruning and gap reporting. A database engine does not supply that network protocol. [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html), [RocksDB](https://github.com/facebook/rocksdb).

Test receipt-after-persistence and crash recovery, including atomic cursor/effect/dedup updates and ratchet/outbox state (`MPE-STO-004/011/017/025/039/042`, `MPE-CON-033`). Core SQLite and ordinary RocksDB are not a complete encrypted key-storage solution; application keys/index metadata need a selected protection scheme. RocksDB offers an Apache-2.0 or GPLv2 license choice with retained third-party notices; core SQLite is public domain. Record the chosen integration and bindings rather than treating a storage brand as replication or confidentiality.

### 3. Private mobile reception remains an unsolved integration target

Signal encrypts content but does not reduce whole-shard bandwidth. At the PDF's byte ceiling, full reception is approximately **5.7 GB/day**; its baseline mix is about **1.86 GB/day**, compared with a **56–60 MB/day** mobile budget. The original document explicitly does not claim private mobile reception at launch. See printed pages 64 and 134, DEC-021 and `MPE-PRF-021`.

Evaluate **PIR/OMR private discovery and retrieval**, not merely encrypted HTTP downloads. Useful research tools include [SimplePIR/DoublePIR](https://github.com/ahenzinger/simplepir), [SealPIR](https://github.com/microsoft/SealPIR), [Microsoft SEAL](https://github.com/microsoft/SEAL), and [Google private-retrieval](https://github.com/google/private-retrieval). PIR hides a chosen database index; it does not tell a receiver privately which indices contain its messages or hide query counts, timing, tenant choices, update traffic or selective failures.

These have material adoption limits: SealPIR explicitly says not to use it in production and documents an older SEAL dependency; SimplePIR is a research implementation; Google's repository was archived on 18 April 2026 and is not a supported Google product. SEAL is a homomorphic-encryption substrate, not a complete delivery protocol. Its current upgrade guidance must be reconciled with any old PIR dependency pin. Measure preprocessing, hints, dynamic database updates, server work, mobile energy and malicious-server behavior before selecting a construction.

An exploratory thin salt/tag inventory plus PIR could reduce discovery bytes, but it is **not a selected or proven design**. At 10 envelopes/s, a 32-byte salt/tag entry costs 27.648 decimal MB/day; adding a 32-byte envelope ID reaches 55.296 MB/day before framing, proof/authenticity, hints, updates, payload retrieval or cover queries. Existing envelope commitments do not alone prove that an isolated advertised salt/tag inventory is correct and complete. Private discovery, authenticated inventory/data binding and recognition-independent query schedules need a separate experiment.

### 4. Group-first messaging may favor MLS instead of Signal

For pairwise conversations, the Signal-derived experiment is plausible. For business groups with frequent membership changes, compare **MLS** using [OpenMLS](https://github.com/openmls/openmls) or [mls-rs](https://github.com/awslabs/mls-rs). MLS defines authenticated group epochs and membership updates, with conditional forward secrecy and compromise recovery. The standard is transport-independent and supports groups with two members as well as larger groups. [RFC 9420](https://www.rfc-editor.org/rfc/rfc9420.html).

This suggests a genuine alternative: a group-first product may use **GossipSub + MLS + anonymous admission**, instead of adopting Signal and MLS together by default. Compare that option against a pairwise Signal profile before taking on two independent session-state, codec, recovery and maintenance systems. Neither architecture supplies private discovery or contract authority automatically.

Hide group/epoch/credential/Welcome metadata under the MPE profile; verify wallet/device credentials; define concurrent commit/fork, removal/rekey and offline recovery behavior. Ordinary MLS credentials/signatures do not automatically authorize a business effect. OpenMLS is MIT licensed; mls-rs offers MIT/Apache-2.0 and currently states it has not received a full third-party security audit. Current library/provider/version review is still required. Default classical MLS suites are not a post-quantum security claim. [OpenMLS security scope](https://github.com/openmls/openmls/security), [mls-rs README](https://github.com/awslabs/mls-rs/blob/main/mls-rs/README.md).

### 5. Origin privacy is an optional, separate transport profile

If hiding the client's direct address from ingress is a requirement for a selected profile, investigate **Tor/Arti** for eligible connections. That does not give global timing/volume privacy, anonymous GossipSub participation or general UDP/QUIC anonymization. Handle circuit isolation, DNS, failures and direct fallback explicitly; do not silently downgrade a chosen privacy profile. The original launch design claims no ingress anonymity. [Arti](https://arti.torproject.org/about/), [arti-client](https://docs.rs/arti-client/latest/arti_client/), `MPE-PRV-024` and DEC-023.

### 6. Midnight authority and ledger integration remain custom work

Complete Registry/Anchor/finalized-ledger adapters, carried-event exact-byte and applied-phase checks, independent signed instructions, stable consumption nullifiers and effect binding. Stock Signal authentication cannot discharge `MPE-CON-043/044a/044b/060`. In the nested Signal payload option, the outer MPE signature authenticates ciphertext; proving that the authorized plaintext is inside the anchored envelope is additional circuit work. An off-chain decryption or a valid inclusion path does not prove that relation. [Composition assessment](gossipsub-signal-option.md), [Appendix A](../design-document/build/appendix-a.md).

### 7. Some gaps require a patch, not another protocol

`MPE-FMT-032` forbids forwarding expired envelopes, including queued sends and IWANT responses. Initial ingress validation does not guarantee that stock GossipSub's internal cached response or delayed queue drain rechecks application expiry. Identify supported hooks or a scoped router patch and test deadline crossings on all send paths; a generic wrapper cannot be assumed to intercept them. Also verify the pinned version's anonymous message fields, custom protocol negotiation and peer-score/mesh constraints. These are concrete implementation/conformance gaps already discussed by the PDF, not reasons to add another messaging protocol.

## Recommended build sequence

1. **Backend coordination pilot:** configured Rust libp2p/GossipSub, existing MPE envelopes and local recognition, authenticated invitations, one durable state engine, whole-shard recovery and a workflow SDK. The original symmetric profile can establish business value before adding ratchets. Mock ledger/stand-in admission is acceptable only with the prototype's explicit limitations.
2. **Production admission and Midnight integration:** real anonymous proofs, stable domains and root lifecycle, replay/abuse handling, actual Registry and consumer proofs, persistence receipts and measured recovery. This is the first protocol investment beyond transport/session encryption.
3. **Choose one session architecture:** pairwise Signal-derived integration or group-first MLS; test exact wire fit, identities, erasure, crash/backup recovery and independent business signatures.
4. **Private mobile experiment:** jointly solve discovery, query scheduling, authenticated mutable inventories and private retrieval, measuring the complete client/server budget.
5. **Production gates:** deploy measured workload/security tests, independent review, funded operators, costed service targets and profile-specific privacy evidence. Neither open-source availability nor documentation conformance proves these gates.

The missing pieces are mostly acknowledged by the original PDF. New composition-specific questions are nested proof binding, exact library/profile compatibility, session-state persistence and whether stable recognition keys preserve metadata exposure after inner ratchet recovery. The practical decision is which narrow profile to deliver first, with its remaining requirements made explicit.

## Semaphore extraction into the working stack

The subsequent three-agent Semaphore study adopts its identity/group/witness lifecycle patterns while retaining the original RLN-style publication relation. Actual library reuse requires compatible commitment, hash, field and tree semantics; no second membership proof is added per message. See [working stack](proposed-stack.md) and [membership assessment](semaphore-membership-option.md).
