I favor a separate event overlay, local recognition, authenticated invitations, ratcheted encryption and paid admission that binds authorization to the actual ciphertext. The reviewed proposals provide useful transport, accounting and delivery ideas, but none is ready to adopt unchanged: g2 exposes a persistent publisher key and leaves membership validation unspecified; g3’s proof batching lacks a defined binding to its message budget; o2’s proof precomputation permits same-key equivocation without RLN secret recovery; o3 understates transaction costs and its bucket savings do not follow from its tag construction. Below, proposed parameters are **design assumptions**, calculations are **inferences**, and unverified implementation properties are **unknown**. Repository paths are relative to `/home/charl/midnight/`; `L9:` means `midnight-ledger` at `ledger-9.1.0.0-rc.5`, rather than its ledger-8 working tree. I used the graph as an evidence locator and checked the underlying text and code.

## D1 — Event format

- **g2-network-engineer:** StrictNoSign transport; visible shard, membership key/signature and nullifier; sealed application body; 4/64 KiB mesh bodies and 256 KiB external bodies.
- **g3-performance-storage:** Padded 1/4/32 KiB classes, visible quota proof and shard, no recognition tag; static ECDH for first contact and optional ratcheted sessions.
- **o2-economist-operator:** Four padded body classes, visible RLN-Diff fields and S-FMD clue, approximately 4 KiB proof allowance; sealed topic and authorship.
- **o3-consumer-experience:** `Misc` carrier with a 32-byte recognition tag and 256-byte parts; X25519 first contact and symmetric streams.

**Evidence check.** g2 correctly cites StrictNoSign, but removing GossipSub’s author fields does not conceal its application-level `member_pk` (`2020-vac-waku2-relay-spec`, “Signature Policy”). Its 211-byte public header also remains outside the body caps. The Yamux citation establishes a first-frame receive limit, not an application-object limit (`rust-yamux@origin/yamux-v0.12.2:yamux/src/connection.rs:643`).

g3’s ratchet citation supports session encryption, but its “padded wire sizes” cannot be frozen while admission-proof length remains unknown. o2’s RLN citation supports the public share/nullifier structure; it specifies Groth16, not Midnight’s proposed PLONK implementation (`2024-vac-rln-v2-spec`, “ZK Circuits specification”).

o3 correctly cites `Misc`’s fixed fields (`minokawa-compact/compiler/midnight-events.ss:71`). **Inference:** each multipart event repeats its name, so four parts occupy 1,152 bytes and sixteen occupy 4,608, before surrounding serialization. Its public header plus AEAD tag costs 50 bytes, not 49; usable capacities become 206/974/4,046 bytes.

**Vote — own alternative, s2-cryptographer.** Keep fully costed 1,024/4,096-byte cells, sealed signatures and encrypted ratchet headers. Use hybrid establishment: ML-KEM-768 adds a 1,184-byte public key and 1,088-byte ciphertext; setup requires four DH computations per side when the curve one-time prekey is used, plus one encapsulation/decapsulation (`2024-nist-fips203`, Table 3; `2023-signal-pqxdh-spec`, §3.3). ML-DSA-65 signatures cost 3,309 bytes and require a revised class (`2024-nist-fips204`, Table 2).

**Strongest objection:** my invitation wrapping and header-key initialization are new composition. The ratchet specification does not prove this complete envelope.

## D2 — Definition of “private”

- **g2-network-engineer:** Conditional confidentiality; explicit shard/IP/timing leakage; no global anonymity, FS or PCS.
- **g3-performance-storage:** Confidentiality and shard-level interest concealment; one-hop source obfuscation; no relationship privacy.
- **o2-economist-operator:** Anonymous membership, publisher unlinkability, fuzzy interest privacy and a cover floor; excludes global source anonymity and mandatory PQ protection.
- **o3-consumer-experience:** Full-download interest privacy, PRF topic concealment, epoch FS and hidden contract reaction; buckets explicitly weaken privacy.

**Evidence check.** g2’s refusal of global anonymity is supported by `2017-das-trilemma`, abstract. Its encryption claim also needs the weak robustness identified by its cited `2013-kohlweiss-anonymitypke`, abstract, alongside IND-CCA and key privacy.

g3 correctly distinguishes shard interest from relationship privacy. However, a publicly derivable `H(contract address) mod 8` is dictionary-testable: sealing the topic does not hide its shard mapping (**inference from its routing rule**).

o2’s RLN citation supports anonymity within the accepted membership set, conditional on a sound implementation. Its statement that relationship privacy “follows” from publisher anonymity and fuzzy detection is unsupported. `2021-seres-fmdfalsepositives`, §§4–6, finds relationship and temporal attacks; a fixed false-positive floor supplies no general bound.

o3’s epoch-FS claim requires erasure. Retaining thirty days of keys exposes that retained window, while a recorded inbox invitation containing the initial stream key can defeat subsequent hash-ratchet secrecy if later decrypted (**inference**; underlying erasure requirement: `2016-signal-double-ratchet-spec`, §8.1).

**Vote — g2-network-engineer’s explicit leakage discipline, amended with s2’s session guarantees.** Relays learn adjacent IPs, timing, class and ciphertext equality; gateways learn full-stream cursors; chain observers learn contracts, transcripts and effects; colluders combine observations; global observers retain correlation opportunities. Require conditional content FS, but promise neither relationship unobservability nor PQ PCS. PQXDH authentication remains classical (`2023-signal-pqxdh-spec`, §4.1).

**Strongest objection:** a technically accurate leakage table can still describe privacy too weak for the intended applications; that requirement must be settled before launch.

## D3 — Publish and subscribe model

- **g2-network-engineer:** Private/open shards, local whole-shard recognition, at-least-once delivery; contracts consume through later transactions.
- **g3-performance-storage:** Eight pinned shards; whole-shard unicast for phones; sealed sequence numbers and 48-hour back-fill.
- **o2-economist-operator:** Shared topic keys; relay/download/FMD subscription choices; contracts verify inclusion against an anchor ring.
- **o3-consumer-experience:** Per-publisher PRF tags, 32-tag lookahead, full/bucket/self-hosted retrieval and explicit gap/late/head states.

**Evidence check.** g2’s shard-subscription leakage is supported by Waku’s `SubOpts`; g3’s eight-shard precedent is supported by `2024-cornelius-waku-network-dapps`, “Routing and Sharding.” Neither source establishes that eight shards are appropriate for this workload.

o2 correctly cites Penumbra’s sender-selected precision, but Penumbra calls for adaptation to global traffic; it does not validate a universal `p ≥ 1/64` privacy guarantee (`2022-penumbra-fmd-spec`, “Sender and Receiver FMD”).

o3 correctly cites replay-then-live and at-least-once behavior (`midnight-indexer/indexer-api/src/infra/api/v4/subscription/contract_event.rs:102`; `midnight-js/packages/types/src/public-data-provider.ts:507`). Its bucket arithmetic is inconsistent with fresh PRF tags. **Inference:** 32 uniformly distributed lookahead tags cover an expected `16[1−(15/16)^32] ≈ 13.97` four-bit buckets, not one. Losing more than the lookahead also needs an explicit recognition-resynchronization path.

The cross-contract citation supports witness-free callees, not the entire consumption circuit (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:96`).

**Vote — own alternative, incorporating o3’s explicit delivery states.** One transport topic; authenticated device invitations; local encrypted-header trials; complete-range back-fill; logical deduplication and atomic processing/cursor commits. Contracts assert publisher authorization, destination, expiry and replay protection in a submitted call. Source-contract provenance needs an actual source commitment, not merely a bus anchor.

I correct my Round 1 attribution: the ratchet specification supports trials **within an associated session**; it explicitly leaves session association outside scope (§§4.1, 4.6). Trying a bounded set across sessions is our extension.

**Strongest objection:** full download and independent recipient ciphertexts scale poorly. At ten cells/s, 32-device fan-out permits only 0.3125 logical publications/s before controls (**inference**).

## D4 — Sustainable model

- **g2-network-engineer:** DUST-paid hourly membership, sixty small-message credits, public-key enforcement and unpaid relays.
- **g3-performance-storage:** Daily DUST membership, byte budgets, batched proofs and unpaid relays/stores.
- **o2-economist-operator:** NIGHT bonds and registration fees; RLN slashing; funded storage/anchors and anonymous retrieval credits.
- **o3-consumer-experience:** Per-event DUST on the initial ledger lane; later bonded RLN overlay; initially subsidized reads.

**Evidence check.** All correctly reject treating DUST as transferable relay money (`midnight-docs/docs/concepts/dust-architecture.mdx:23`). The fee formula supports approximately 0.01 DUST per **decimal KB** at genesis factors, not a live quote (`L9:base-crypto/src/cost_model.rs:408`).

g2 specifies signature and sequence checks but no verifiable binding between `member_pk` and purchased membership. Its assertion that Midnight “cannot slash” is too broad: contract token receipt/payment primitives exist; the proposed NIGHT bond implementation remains **unknown** (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1196`).

g3’s batch proof needs an explicit commitment to its bounded messages and byte debit. RLN does not supply that batch automatically.

o2 incorrectly rejects all Privacy Pass as privately verifiable: RFC 9578 §6 explicitly provides public verification (`2024-rfc9578-privacypass-issuance`). Its precomputation also changes RLN’s signal binding. **Inference:** signing different bodies with the same ephemeral key preserves the same `x,y`; conflicting bodies therefore do not provide the two distinct shares needed to recover the secret. Deduplication can reject a second body locally, but the claimed slashing property does not follow.

o3’s cited proof estimates total 7,744 bytes before transcript/event data, contradicting its 6 KB derivation. Actual call-proof size is **unknown** (`L9:ledger/src/dust.rs:2158`; `L9:ledger/src/structure.rs:1908`).

**Vote — own alternative.** Launch with purchased, object-bound blind-RSA stamps: 354 bytes per cell, one public verification, and 515 issuance bytes before HTTP (RFC 9578 §§6.1–6.4, 8.2.2). Fund carrying, retention and egress explicitly. Prototype message-bound anonymous quota proofs separately.

**Strongest objection:** accepted issuers can censor or mint excess capacity; blind issuance does not eliminate timing correlation.

## D5 — Performance requirements

- **g2-network-engineer:** Degree-eight mesh; approximately 104 small messages/s within its relay budget; p99 ≤2 seconds target.
- **g3-performance-storage:** Per-shard event/byte caps; degree-six accounting; named relay/filter/client budgets and measured Waku proof costs.
- **o2-economist-operator:** 100 events/s sustained, 1,000 peak; proof precomputation; FMD phones; p99 ≤3 seconds.
- **o3-consumer-experience:** Ledger lane at 1 event/s average and 10 peak; approximately 52 MB/day per full client; 10,000 subscribers per optimized indexer.

**Evidence check.** g2 correctly treats its latency formula as a model and identifies Farooq’s inconsistent printed example (`2025-farooq-staggering`, §IV). Mesh degree and serialization time alone do not establish its percentile target.

g3 accurately reproduces Waku’s 2.7/4.5/18.7 ms verification measurements and 85.7/276.3/766.8 ms generation measurements (`2024-revuelta-waku-latency`, Table 1). These are nwaku results, not Midnight-native proof benchmarks. Its bandwidth tables also require admission overhead inside the mean wire size.

o2’s same timings are supported, but its precomputation benefit depends on the unsound slashing inference in D4. Its subscriber volume counts bodies rather than complete envelopes.

o3 correctly identifies per-subscription database drains (`contract_event.rs:125`) and the 25-connection pool (`midnight-indexer/indexer-api/config.yaml:30`). Its 28 tx/s ceiling overlooks the runtime’s Normal-dispatch byte allowance. **Inference:** at an assumed 8 KiB transaction, the configured 75% of 1 MiB per six seconds gives a byte-only ceiling of sixteen tx/s (`midnight-node/runtime/src/lib.rs:292`, `:300`, `:312`).

**Vote — g3-performance-storage’s accounting method, recosted for D1/D3.** Count ciphertext cells, fan-out, control traffic, proofs and subscriber egress. For the s2 normal workload, 10 × 1,054.72 × 1.25 gives 13,184 bytes/s, or 1.139 GB/day per full downloader (**inference; 25% overhead assumed**). Report latency from authorization request through delivery.

**Strongest objection:** without measured admission size and client recognition costs, the numerical budgets remain provisional.

## D6 — Storage requirements

- **g2-network-engineer:** Ten-minute relay cache; optional 24-hour stores; anchored bodies may receive seven-day storage.
- **g3-performance-storage:** Forty-eight-hour shard stores, optional fourteen-day archives; bounded chain roots.
- **o2-economist-operator:** TTL-priced bonded stores, approximately 28 GB of bodies at launch, fourteen-day anchor ring; proofs discarded after anchoring.
- **o3-consumer-experience:** Thirty-day hot indexer retention, optional indefinite reconstruction, and key-limited back-fill.

**Evidence check.** g2 correctly separates indexer state retention from event-row retention. An anchor alone does not entitle a body to storage; that needs a service agreement (**inference**).

g3’s `λSR` accounting is sound: its L1 shard holds 1,769,472,000 raw bytes over 48 hours. Its fourteen-day archive rationale does not follow from ledger `global_ttl`, which governs specified replay/root histories rather than custom bus archives (`L9:ledger/src/semantics.rs:1715`; `midnight-node/res/mainnet/ledger-parameters-config.json:176`).

o2’s arithmetic describes retained **bodies**, omitting remaining envelope metadata. A root opening proves inclusion, not continued retrievability. Discarding admission proofs also removes independent admission revalidation unless another verifiable mechanism replaces it (**inference**).

o3’s re-execution claim is supported (`midnight-indexer/docs/architecture.md:15`). Indefinite reconstructability additionally assumes available historical blocks and execution software; the cited architecture provides no indefinite availability guarantee.

**Vote — own alternative.** Seven-day paid retention, three independent storage receipts, complete-range retrieval and explicit key-gap limits. At the assumed normal load, raw retention is 6.379 GB; indexing/database allowance yields approximately 10.15 GB, so provision 12 GB (**inference from s2’s stated assumptions**). Receipts establish a contractual obligation, not cryptographic availability.

**Strongest objection:** seven days of ciphertext does not guarantee seven days of decryptable recovery when skipped-key limits are exceeded.

## D7 — Infrastructure actors

- **g2-network-engineer:** Separate bootstrappers, open relays and optional stores; validators excluded; volunteer operation initially.
- **g3-performance-storage:** Self-use relays/stores and wallet-funded filter services; payment market deferred.
- **o2-economist-operator:** Bonded, paid storage/anchor services; open relays; foundation launch followed by measured decentralization gates.
- **o3-consumer-experience:** Foundation/self-hosted indexers first; reactors and wallet custody; open overlay later.

**Evidence check.** g2’s exclusion of mandatory validator work is supported by the node’s explicit concern about serialization competing with consensus (`midnight-node/node/src/service.rs:614`). Its ten permissioned candidates are a genesis configuration fact, not a live census (`system-parameters-config.json:6`).

g3’s self-use incentives have a Waku precedent, but that paper distinguishes relay reciprocity from paid services for constrained clients (`2024-cornelius-waku-network-dapps`, §III-E).

o2 correctly cites reputation-framing risks (`2026-cao-nymreputation`, §1). Its saturation cap is per key, not independent organization. More seriously, `Maintain` can remove and insert verifier keys: “parameters only; cannot move bonds” is not established by the cited mechanism (`L9:ledger/src/structure.rs:2952`). A timelock does not itself restrict replacement circuit behavior (**inference**).

o3 accurately describes the existing connector boundary and proposes new wallet custody; the cited API has no event subscription method (`midnight-dapp-connector-api/src/api.ts:70`).

**Vote — own alternative, adopting o2’s funding discipline.** Dedicated contracted relays/gateways, multiple issuers, local wallet/agent keys and independent operator organizations. Use measured service-opening gates; defer the bespoke bond/treasury/challenge system until verified.

**Strongest objection:** independence and sustainable revenue are operational assumptions; distinct peer IDs or bond keys cannot establish them.

## D8 — Network tether

- **g2-network-engineer:** Separate GossipSub sidecar; ledger authorization/anchors; low-rate anchor/indexer fallback.
- **g3-performance-storage:** Separate sidecar; fallback is a default-off custom node protocol.
- **o2-economist-operator:** Sidecar plus Registry; ledger/indexer ciphertext fallback.
- **o3-consumer-experience:** Ledger/indexer first, sidecar second; reverse the order if activation or costs fail.

**Evidence check.** g2, g3 and o2 correctly identify the extension boundary: the node explicitly registers consensus and ledger-sync protocols, with no GossipSub package in its lockfile (`midnight-node/node/src/service.rs:574`, `:610`; `midnight-node/Cargo.lock`). A node fork is possible; a ready application plugin is not shown.

o3 correctly flags the deployment-generation mismatch: Compact 0.33 introduces ledger-9 events and cross-contract calls, whereas the mainnet support matrix lists toolchain 0.31.1 (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`; `midnight-docs/docs/relnotes/support-matrix.json:38`). Actual activation is **unknown** locally.

The ledger carries public ciphertext bytes, so “public by construction” does not mean plaintext must be public. Nevertheless, envelope metadata and publication transcripts are public; ledger bandwidth remains constrained.

**Vote — g2-network-engineer’s sidecar architecture.** Use a separate overlay and optional anchors. Require new client software, application contracts where needed, and a separate bulk-stream service. My fallback is replicated gateways serving the same encrypted stream; anchor/indexer-only fallback is explicitly reduced functionality.

**Strongest objection:** operating a second network introduces discovery, monitoring and availability obligations that the existing ledger/indexer service already handles.

## D9 — Threats and open risks

- **g2-network-engineer:** Diverse discovery, outbound mesh quotas, scoring/CVE gate, admission caps and explicit anonymity residuals.
- **g3-performance-storage:** Byte caps, expiry, verification caches and shard diversity; names split-view nullifier spending.
- **o2-economist-operator:** Bonded RLN, store challenges, FMD floor, governance timelock and saturation caps.
- **o3-consumer-experience:** Sequence gaps, cross-indexer checks, portable cursors, fixed parts and contract nullifiers.

**Evidence check.** g2’s scoring protections are supported, but not complete eclipse resistance (`2020-gossipsub-v11-spec`, “Outbound Mesh Quotas”). The ACL2s paper reports successful scoring attacks and CVE-2022-47547; it does not certify every implementation or parameter set (`2023-kumar-gossipsub-acl2s`, §1).

g3 correctly names split-view and restart-cache risks; its nullifier defense remains conditional on D4’s circuit binding.

o2’s “no replay residual” is unjustified without epoch-boundary and persisted-cache semantics. Its FMD floor and timelock also retain the D2/D7 weaknesses.

o3’s gap detection catches interior omissions once a later authenticated sequence arrives, not withheld suffixes. Replaying equal bytes is possible; deduplication suppresses repeated processing. “None” for contract replay residual additionally assumes correct nullifier derivation and atomic enforcement (**inference**).

**Vote — g2’s network defenses, with mandatory s2 key/rollback defenses and corrected admission.** Persist replay state; reject malformed keys and downgrades; commit ratchets only after authentication; test backup rollback and recipient probing. Treat encrypted-header/PQXDH composition as unresolved assurance work: the supplied analysis reports three FS attacks and partial results for these variants (`2026-cheval-dr-automated`, abstract, §§3, 5–6).

**Strongest objection:** authenticated application reactions can reveal recipients even when transport recognition leaks nothing.

## D10 — Build and verification plan

- **g2-network-engineer:** Mesh simulation, scoring-fix gate and admission model; fallback if delivery fails.
- **g3-performance-storage:** Fee/proof/client measurements and quota invariants before launch.
- **o2-economist-operator:** Native RLN benchmarks, economic simulation and Registry conservation/slash/withdraw models.
- **o3-consumer-experience:** Delivery-state model, crash/failover chaos tests, contract race tests and an outside-developer usability gate.

**Evidence check.** g2’s simulation method is reasonable, but a changelog entry is weaker evidence than reproducing the scoring attack and checking its failure. g3 correctly separates Waku measurements from this implementation’s results (`2024-revuelta-waku-latency`, §§4–5).

o2’s proposed Registry invariants are useful **design assumptions**, but omit same-ephemeral-key conflicting bodies and historic-root authorization after removal. The membership documentation explicitly warns that historic roots can retain authorization for replaced/removed entries (`midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:170`).

o3’s delivery model addresses real inclusive-cursor/reconnect behavior. Its “zero duplicates” guarantee requires an atomic effect store; external effects need their own idempotency contract. Nostr’s `EOSE` supports the boundary-marker pattern, not this bus’s completeness guarantee (`nostr-nip-01`, “From relay to client”).

**Vote — o3-consumer-experience’s delivery-verification plan, expanded with cryptographic gates.** Before launch: freeze encodings; test message-bound admission; reproduce the ratchet/scoring attacks; benchmark actual wire sizes and devices; test lookahead/key-gap recovery; verify hidden witnesses and disclosed effects; then run outage/load/economic tests. Add deliberate conflicting-body, rollback, withheld-suffix and membership-removal cases.

**Strongest objection:** successful finite tests cannot establish cryptographic composition security; independent review of the complete construction remains necessary.

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | s2: fully costed cells and hybrid ratcheted sessions | Visible stable keys; unspecified proof overhead | DR §4; FIPS 203/204 tables | Medium | Composition audit or size measurements fail |
| D2 | g2 leakage discipline, amended session guarantees | Derived relationship anonymity | Trilemma; Seres §§4–6 | High | Stronger privacy becomes mandatory |
| D3 | s2 recognition plus o3 delivery states | Unvalidated buckets; default delegated FMD | DR §§4.1/4.6; indexer stream code | Medium | Retrieval matches privacy at lower measured cost |
| D4 | s2 object-bound public stamps | Unbound batches; same-key RLN slashing claim | RFC 9578 §6; RLN-v2 flow | Medium | Sound native quotas are affordable |
| D5 | g3 accounting, recosted | Borrowed benchmarks as bus measurements | Waku Table 1; runtime byte limits | Medium | Actual wire/CPU costs invalidate budgets |
| D6 | s2 paid seven-day retention | Anchors as availability guarantees | `λSR`; indexer architecture | Medium | Offline requirements or funding differ |
| D7 | s2 actors with o2 funding discipline | Volunteer-only durability; unrestricted maintenance trust | Token APIs; maintenance updates | Medium | Independent operators cannot be funded |
| D8 | g2 sidecar; gateway fallback | Node fork first; ledger bulk first | Node protocol registrations | High | Suitable isolated native transport ships |
| D9 | g2 network defenses plus s2 key defenses | Absolute replay/completeness claims | ACL2s; ratchet analysis | Medium | Red-team attacks defeat the controls |
| D10 | o3 delivery plan plus crypto/economic gates | Shipping on component citations | Stream code; cited attack analyses | High | Independent evidence satisfies revised gates |

**Most likely disagreements:** **D3**, full-stream recognition versus shards/tags/FMD; **D4**, blind stamps versus bonded anonymous quotas and volunteer economics; **D8**, overlay-first versus ledger/indexer-first launch.

**One fact that would settle the most disagreement:** the measured serialized size of a **sound, ciphertext-bound, quota-enforcing admission proof produced by the intended Midnight toolchain**. That single measurement would resolve much of the disagreement over envelope classes, proof batching, admission architecture and bandwidth/storage costs. It is currently **unknown**; generate and serialize the exact proposed circuit’s proof, rather than substituting Zswap estimates or Waku proof sizes.