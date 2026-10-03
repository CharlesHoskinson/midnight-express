I favor a small, separately funded overlay with complete-stream retrieval and optional Midnight commitments, while keeping publisher anonymity and private mobile retrieval outside the launch claims. The ledger-only proposal deserves a comparative prototype, but its retention, rate-cap and sustained-cost assumptions are unsupported. The overlay proposals contain useful components, yet none is ready to become a specification: two contain circular cryptographic dependencies, and several extend security results beyond their proved models. I checked the proposals against local papers and code; graph communities and catalog summaries served as navigation aids. Code citations below are relative to `/home/charl/midnight/`. Ledger-9 checks use the node’s pinned revisions: ledger `6abe9b16`, VM `54a4e013`, and base-crypto `dc87cc8f`; the read-out’s aggregate ledger tag resolves elsewhere. Mainnet activation remains **unknown**. [`midnight-node/Cargo.lock:7894`, `:8460`, `:7609`; `midnight-docs/docs/relnotes/support-matrix.json:38`.]

## D1 — Event format

- **g4-skeptic-minimalist:** One public `Misc`, constant name, 256-byte ciphertext, 205-byte application body.
- **g1-protocol-architect:** A 192-byte header, four body classes, single-use ticket, outer and inner signatures.
- **o4-governance-operations:** Four padded classes, visible rotating tags, RLN proof and mandatory franking slot.
- **o1-midnight-integrator:** Four classes, visible tag and FMD clue, Compact-RLN proof, multipart ledger fallback.

**Evidence check.** g4 correctly cites `Misc` as 32-byte name plus 256-byte payload. Its AEAD overhead and 205-byte body arithmetic are consistent. Zcash supports the scanning analogy and cipher choice, but uses derived one-time keys; it does not validate g4’s complete shared-key protocol. [`minokawa-compact/compiler/midnight-events.ss:71`; `2018-hopwood-zcashprotocol`, §§4.20.2, 5.4.3.]

g1 has a construction error: AEAD associated data includes `relay_sig`, while that signature covers the ciphertext being produced. The inner signature also covers the header. **Inference:** the specified dependencies are circular; no generation procedure is supplied. Its Yamux and transaction-size citations do not establish limits for an independent sidecar. [`privateEvents/design/rounds/r1/g1-protocol-architect.md`, D1.]

o4’s listed header fields sum to **296 bytes**, not 304; eight bytes remain unspecified. The Waku spec supports a 128-byte compressed proof for its construction. Grubbs supports committing encryption, and Hecate Table 4 reports **380 bytes sent, 484 received, 380 reported**; neither proves that reserving a slot implements franking. [`2021-vac-waku2-rln-relay-spec`, “RateLimitProof”; `2017-grubbs-franking`, §2; `2021-issa-hecate`, Table 4.]

o1’s 68-byte FMD clue is supported for the named construction. However, its ID includes RLN fields and proof, while the proof’s share input is `H(id)`: another circular dependency. Multipart is **Proposed**, not confirmed deployed. [`2021-beck-fmd`, §1; `privateEvents/design/rounds/r1/o1-midnight-integrator.md:13`, `:157`; `midnight-improvement-proposals/mips/mip-0019-multipart-event.md:6`.]

**Vote:** My alternative: fixed 2 KiB records, sealed application metadata, bounded fragmentation, and an explicitly acyclic order for commitments, encryption, admission and signatures. These sizes remain **engineering assumptions**.

**Strongest objection:** My recognition wrapper is also unproved. Exact construction, control-message sizing and test vectors must precede adoption.

## D2 — Definition of “private”

- **g4:** Confidentiality, topic privacy, shared-stream scanning and chain-level publisher unlinkability; no forward secrecy or global anonymity.
- **g1:** Confidential content and parties, full-shard interest privacy, ticket binding; no forward secrecy or anonymity theorem.
- **o4:** RLN membership privacy, rotating-tag topic privacy, conditional relationship privacy and recipient-controlled reporting.
- **o1:** Topic and membership unlinkability, bucket-level interest privacy, Dandelion++ source privacy and session security.

**Evidence check.** g4’s unsigned transaction citation establishes absence of a Substrate signer. It does **not** establish general transaction unlinkability: public transcripts, unshielded offers and network observations remain relevant. [`midnight-node/pallets/midnight/src/lib.rs:575`; `midnight-node/runtime/src/check_call_filter.rs:86`; `midnight-ledger@6abe9b16/ledger/src/dust.rs:469`.]

g1 incorrectly says knowing a candidate recipient **public** key permits trial decryption. Its X25519 KDF requires either the ephemeral secret or recipient secret. Public-key knowledge alone is insufficient. Whether its custom encryption provides recipient key privacy is **unknown**; confidentiality alone does not prove that property. [`privateEvents/design/rounds/r1/g1-protocol-architect.md`, D1–D2; `2022-barnes-rfc9180`, §4.1.]

o4’s RLN citation supports hiding the membership witness, not “unlinkability against everyone.” Network observations and registration timing fall outside that statement. Repeated hourly tags visibly link records. Its recipient-only disclosure claim also exceeds franking: the sender knows the message and opening material. [`2022-taheri-waku-rln-relay`, §§II–IV; `2017-grubbs-franking`, Figure 3.]

o1’s source-privacy claim lacks a specified Dandelion++ configuration matching the analysis. Its tag privacy depends on rotation details. MLS security requires processed commits and deletion of old keys; merely carrying MLS is insufficient. [`2018-fanti-dandelionpp`, §§3.1, 4; `2023-barnes-rfc9420`, §16.6.]

**Vote:** **g4’s restrained confidentiality and full-stream selection-privacy position**, with general publisher unlinkability removed and authenticated application behavior specified.

I amend my own Round 1 wording: a mandatory contract-address filter does not defeat privacy *among sealed topics inside one commonly downloaded bus contract*.

**Strongest objection:** Selection privacy disappears if acknowledgements, fetches, connection schedules or contract effects depend observably on recognized events. This is an **inference** requiring whole-client testing.

## D3 — Publish and subscribe model

- **g4:** Secret topic keys, one contract stream, local decryption, indexer ordering; agents submit subsequent transactions.
- **g1:** One-shard flooding, secret invitations, local trial opening, unordered delivery and later commitment calls.
- **o4:** Eight shards, hourly or per-message tags, introductory inbox, selective light retrieval and authenticated contract consumption.
- **o1:** Sixteen buckets, tags and first-contact FMD, decoy retrieval, private witnesses and historic-root checks.

**Evidence check.** g4’s stream mechanism is supported: the resolver drains existing records and follows indexed blocks using IDs. Its local-scanning analogy is supported by the wallet. These establish conditional replay and delivery behavior, not indexer completeness. [`midnight-indexer/indexer-api/src/infra/api/v4/subscription/contract_event.rs:98`; `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:220`.]

g1’s full-shard retrieval plausibly hides topic selection, but its at-least-once promise needs reachable storage and acceptance conditions. A later `note(commitment)` records an assertion; it does not authenticate publisher authority or event truth. **Inference from its interface.**

o4 appropriately distinguishes anchoring from authorization. Its decoy queries remain an **unquantified mitigation**, not private retrieval. The original OMR paper does not support “server-cheap” as an unconditional characterization: the reported roughly 0.065 seconds per scanned message is detector work for a recipient. [`2021-liu-omr`, §§1.1, 10.]

o1’s historic-root mechanism has real support: `checkRoot` checks membership in the past-root map, and a witness-free callee fits current cross-contract restrictions. But its public nullifier `hash(ev.id ‖ domain)` is enumerable if `ev.id` is the public envelope ID. **Inference:** observers can identify the consumed event. Its pseudocode also needs explicit constraints binding plaintext, envelope ID and both inclusion paths. [`minokawa-compact/compiler/midnight-ledger.ss:1260`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:101`; `privateEvents/design/rounds/r1/o1-midnight-integrator.md:129`.]

**Vote:** My alternative: secret invitations, complete-stream retrieval and authenticated local dispatch; adopt o1’s historic-root consumption pattern only after repairing binding and using a secret-derived consumption nullifier.

**Strongest objection:** Full-stream delivery creates substantial mobile cost. None of the selective alternatives yet preserves equivalent selection privacy at demonstrated cost.

## D4 — Sustainable model

- **g4:** Publishers pay DUST; existing validators and indexers absorb delivery costs.
- **g1:** DUST-paid batches of tickets; relay funding remains off-protocol.
- **o4:** RLN memberships with deposit, non-refundable fee, slashing and a service-payment pool.
- **o1:** DUST-paid, time-bounded RLN memberships; launch subsidies and later anonymous service payments.

**Evidence check.** DUST is gas capacity, not transferable relay compensation. Spending subtracts the public fee. The checked fee function includes utilization, persistent-write and churn terms. Claims that fees are burned remain an **inference**; the subtraction alone does not prove their entire accounting destination. [`midnight-docs/docs/concepts/dust-architecture.mdx:23`; `midnight-ledger@6abe9b16/ledger/src/dust.rs:1765`; `midnight-ledger@dc87cc8f/base-crypto/src/cost_model.rs:408`.]

g4’s sustained NIGHT estimate confuses capacity with generation. Its assumed 4,608 DUST/day requires approximately **6,451 NIGHT** at the checked generation rate, rather than approximately 900 NIGHT; approximately 922 NIGHT supplies one full-cap inventory. **Arithmetic inference:** `8267 × 10⁶ × 86400 / 10¹⁵ = 0.7142688 DUST/NIGHT/day`. Filling only its small bus budget does not establish whole-chain fullness sufficient to raise prices. [`midnight-ledger@6abe9b16/ledger/src/dust.rs:294`, `:1364`; `midnight-ledger@6abe9b16/ledger/src/structure.rs:3362`; `midnight-node/res/mainnet/ledger-parameters-config.json:166`.]

g1’s 60-ticket/s ceiling assumes an unmeasured batched transaction and unenforced 10% allocation. Membership alone does not provide Sybil resistance without a quantified registration cost.

o4’s RLN economics have the strongest literature match: the paper explicitly identifies multiple registrations and withdrawal escape as open problems. Its fee/deposit policy is a proposed response, not a proved solution. [`2022-taheri-waku-rln-relay`, §V.B.]

o1 correctly labels off-chain Compact proof verification unknown. Its 7 KB anchor estimate is below its own `2912 + 4832 = 7744` proof estimates before transcript overhead; o4’s 6 KB estimate has the same problem. Actual transaction sizes remain **unknown**. [`midnight-ledger@6abe9b16/ledger/src/dust.rs:2158`; `midnight-ledger@6abe9b16/ledger/src/structure.rs:1908`.]

**Vote:** My alternative: purchased, bounded publication and storage capacity with explicit operator funding; DUST pays chain operations. Benchmark anonymous admission separately.

**Strongest objection:** Issuer-funded admission introduces censorship and customer-to-event linkage. That trust cost must be declared.

## D5 — Performance requirements

- **g4:** Four events per block, 5% byte budget, approximately 56 MiB/day/client and a 60-second p50 gate.
- **g1:** 50 objects/s, approximately 2.21 Mbit/s mesh traffic/relay, p99 ≤10 seconds.
- **o4:** 50 events/s sustained, 500 peak, eight shards, p99 ≤5 seconds.
- **o1:** 50 envelopes/s sustained, 250 burst, mobile ≤15 MB/day and anchored p50 approximately 60 seconds.

**Evidence check.** g4’s bandwidth arithmetic is sound under its assumed 1,024-byte response size. Its four-event cap is not implemented by the stateless `publish` circuit; therefore it cannot bound hostile scanning or indexer load. **Inference from the proposed contract.**

g1’s bandwidth calculation is conditional on assumed replication factors; its traffic percentages total 100.1%, a small inconsistency. The 97 μs ledger signature price is not a benchmark of sidecar Ed25519 verification.

o4 accurately reproduces Waku’s approximately 0.5-second iPhone proof generation and 30 ms verification figures. Those concern the referenced implementation, not the proposed RLN-v2/Compact integration or batched verifier. [`2022-taheri-waku-rln-relay`, §IV.]

o1 acknowledges that ledger cost weights are not benchmarks, but then uses them for a CPU budget. Its detection-server estimate assumes only 10% of envelopes need FMD testing although every envelope carries an indistinguishable clue. The tested candidate stream needs definition. Its mobile arithmetic is approximately **12.96 MB of index plus 1.13 MB of fetches/day**, before transport overhead—not 13 MB total. **Arithmetic inference from D5’s assumptions.**

The six-second slot and block limits are checked; 18-second finality is proposal prose, not a percentile. GossipSub’s 5,000-container experiments establish results for their configurations, not these deployment SLOs. [`midnight-node/runtime/src/lib.rs:292`, `:313`; `midnight-improvement-proposals/mps/mps-0028-pre-finality-state-visibility.md:36`; `2020-vyzovitis-gossipsub`, §§1, 7.]

**Vote:** My proposed **10 records/s, 100/s burst** baseline, with separately measured propagation, retrieval, proving, inclusion, finality and indexing.

**Strongest objection:** That workload is a conservative **assumption**, not evidence of product adequacy.

## D6 — Storage requirements

- **g4:** Indexer retention of 14 days; no contract-state mailbox.
- **g1:** Class-dependent expiry of 5–60 minutes, approximately 100 MB retained, optional archive.
- **o4:** Default 24 hours, maximum seven days, approximately 72.6 GB network-stream retention.
- **o1:** Default seven days, maximum fourteen, proof-stripped stores and bounded anchor histories.

**Evidence check.** g4’s `global_ttl` citation concerns intent validity and replay protection—not event-row retention or deletion. The indexer’s 1,000-block setting preserves loadable ledger states. Neither supports “after fourteen days the event is gone.” [`midnight-ledger/spec/intents-transactions.md:131`; `midnight-indexer/chain-indexer/config.yaml:14`.]

g1’s class-based storage estimate follows its workload assumptions, but D1 additionally restricts expiry to the end of the ticket’s two-epoch window. **Inference:** its advertised one-hour class lifetime and corresponding storage model conflict with its acceptance predicate.

o4’s `50 × 2400 × 604800 = 72.576 GB` arithmetic is correct before database overhead. Three operators and canary completeness are proposed operating conditions, not guarantees derived from Waku.

o1’s stripped-storage arithmetic is approximately correct. However, hashing the original proof into an ID does not recover that proof or prove its validity. Offline verification needs retained proof material or an explicit trusted-verification model. Anchor existence also does not establish availability. **Inference.**

Both g4 and o1 lean on MIP-0002 storage estimates. Its approximately 703 MB/day upper bound assumes events consume persistent writes; the pinned VM instead charges logs as churn. Its 150-byte estimate concerns indexed-field sidecar rows, not a measured complete `Misc` record. [`midnight-improvement-proposals/mips/mip-0002-public-contract-log-emission.md:520`, `:531`; `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:595`.]

**Vote:** My **48-hour** retention proposal: complete verifiable records, three independent retention receipts, explicit pruning and separately funded archives. At 10/s and 2 KiB, raw storage is **3.539 GB/relay**.

**Strongest objection:** Receipts attest obligations; they do not prove future availability. The service promise remains conditional on reachable honest storage.

## D7 — Infrastructure actors

- **g4:** Existing validators, indexers and local scanners; no additional operator market.
- **g1:** Eight to sixteen permissioned sidecar operators; off-protocol funding.
- **o4:** Stewards, relays, stores, anchorers, monitors and application moderators, with time-limited governance.
- **o1:** Permissionless relays and anchorers, registered stores, optional detection services and subsidized seeds.

**Evidence check.** g4 correctly identifies existing roles, but “no new duty” is contradicted by serving additional event rows and subscriber egress. MIP-0002 explicitly identifies downstream costs not covered by gas. [`midnight-improvement-proposals/mips/mip-0002-public-contract-log-emission.md:510`.]

g1’s validator-isolation rationale has code support: snapshot serving is disabled by default for validators because its CPU work competes with authoring/finality. Its relay count and governance arrangement remain **assumptions**. [`midnight-node/node/src/service.rs:614`.]

o4 correctly cites a seven-day Root safe-mode duration. That does not enforce its separate steward contract. “Withdrawals never pausable” can hold against a bus-local flag, but not against Midnight’s chain-wide user-transaction filter. Maintenance-authority control must also be included in any claim that powers are excluded “by construction.” [`midnight-node/runtime/src/lib.rs:758`; `midnight-node/runtime/src/check_call_filter.rs:44`; `midnight-ledger/spec/contracts.md:20`.]

o1’s permissionless start is not justified by citing scoring: formal analysis finds configurations where continuous withholding retains positive scores. [`2022-kumar-gossipsub-formal`, §§1, 3–5.]

**Vote:** **o4’s accountable operator and bounded-governance structure**, reduced for launch: paid relays/stores, independent monitors, explicit local-versus-chain pause powers; franking belongs to applications.

**Strongest objection:** A steward-controlled registry and maintenance authority remain a concentrated censorship and upgrade trust boundary.

## D8 — Network tether

- **g4:** Ledger/indexer only; wait for events activation; self-run indexer fallback.
- **g1:** Sidecar plus ledger tickets; native non-validator protocol fallback.
- **o4:** Sidecar plus registry/anchors; small ledger-only fallback.
- **o1:** Sidecar plus memberships/anchors; multipart ledger fallback and upstream change register.

**Evidence check.** All four correctly avoid assuming an existing application GossipSub service. The node explicitly registers consensus and ledger-sync protocols; the lockfile lacks `libp2p-gossipsub`. A supported sidecar is an **architectural inference**, not a shipped Midnight feature. [`midnight-node/node/src/service.rs:586`, `:607`, `:644`; `midnight-node/Cargo.lock`.]

g4 has the clearest deployment caveat. Local Compact 0.33 release notes establish events and cross-contract calls; the support matrix lists mainnet toolchain 0.31.1. Actual activation cannot be inferred from either. [`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`; `midnight-docs/docs/relnotes/support-matrix.json:38`.]

g1’s native fallback requires participating operators to run modified binaries; “every operator” is broader than necessary.

o4’s fallback exposes stable-within-period tags and therefore changes its leakage profile.

o1’s “only mandatory upstream item U0” conflicts with U1 being required for its selected Compact-RLN path. A dedicated-circuit fallback is additional implementation work. Multipart “works today” is unsupported as a deployment claim. [`privateEvents/design/rounds/r1/o1-midnight-integrator.md`, U0–U3.]

**Vote:** **o1’s sidecar/hybrid tether**, with explicit proof-verification and activation gates. Use complete-stream gateways as the initial transport fallback; ledger fallback requires separate capacity and leakage acceptance.

**Strongest objection:** Off-chain delivery can survive a chain outage, but chain-dependent admission, revocation and consumption cannot simply inherit that liveness.

## D9 — Threats and open risks

- **g4:** Fees, full-stream retrieval, multiple indexers and manual key rotation; accepts substantial residual risk.
- **g1:** Tickets, permissioned mesh, two-hop heuristic stem and strict parser.
- **o4:** RLN/slashing, monitored operators, franking, tombstones and emergency governance.
- **o1:** RLN, Dandelion++, FMD, ratchets, scoring and competing anchorers.

**Evidence check.** g4 correctly rejects forward secrecy for static keys. Its fee and scanning defenses nevertheless depend on the unenforced cap. Multiple indexers can expose disagreement; they do not automatically authenticate inclusion.

g1’s claim that conflicting bodies cannot both have valid signatures is false. A ticket owner can sign both. Distinct IDs do not resolve which partition accepted the ticket first. **Inference:** equivocation requires a protocol rule and model.

o4’s invalid-proof rejection limits propagation, not expensive work on the receiving connection. Waku’s 30 ms figure makes ingress exhaustion an explicit risk. Tombstones and operator agreements establish cooperative deletion obligations, not deletion from adversarial archives or legal immunity. [`2022-taheri-waku-rln-relay`, §IV; legal consequences **unknown**.]

o1 appropriately acknowledges Seres-type leakage, but its decoy bound `1/(k+1)` assumes indistinguishable candidate choices and priors; it is not established. FMD ambiguity is defined for honestly generated ciphertexts and keys, and relationship recovery is demonstrated under specified sender knowledge. MLS recovery requires applied commits and key deletion. [`2021-beck-fmd`, §4; `2021-seres-fmdfalsepositives`, §§3–6; `2023-barnes-rfc9420`, §16.6.]

**Vote:** My alternative: threat-specific defenses with declared residuals, configuration-specific scoring checks, admission equivocation handling, authenticated replay state and independently checked anchors.

**Strongest objection:** Composing components introduces attacks absent from their individual models. No reviewed proposal supplies a combined security argument.

## D10 — Build and verification plan

- **g4:** Parser vectors, measured ledger prototype, two-process soak, scanner; upgrades only after explicit triggers.
- **g1:** Parser/admission model, sixteen-relay experiment, spy test and gated removal of permissioning.
- **o4:** Governance/envelope models, staged operations, audits, canaries and jurisdiction-specific legal gates.
- **o1:** Compact-RLN and anchor spikes, models, thousand-node simulation, FMD evaluation and phased integration.

**Evidence check.** g4’s measurement-first plan is sound, but must test hostile publication, actual retention and enforceability of the claimed cap.

g1’s reuse of ACL2s is useful; it is not a reason to omit checking application-specific scoring. Its spy gate uses `2p²` as though the lower bound were an attainable benchmark. Dandelion++ Theorem 1 instead bounds optimal precision using first-spy precision on an unknown random four-regular graph. A two-hop stem does not inherit that theorem. [`2023-kumar-gossipsub-acl2s`, §§1, 3–5; `2018-fanti-dandelionpp`, §§3.2, 4.1, Theorem 1.]

o4’s governance invariants are valuable, but low observed invalid ingress does not prove resilience to arbitrary invalid-proof flooding. Its one-anchor-per-window rule needs a failed-anchorer takeover model. Traffic thresholds are **operational assumptions**, not anonymity theorems.

o1’s proof/API and concurrent-anchor spikes are the strongest integration work. Its “zero over-quota” test must distinguish per-membership quota from aggregate Sybil traffic. Its Dandelion precision gate needs the same model correction as g1. “Every valid call succeeds” also requires stated chain, availability and concurrency conditions.

**Vote:** My claim-based plan, incorporating g4’s comparative ledger prototype, o1’s integration spikes and o4’s governance invariants:

1. Freeze revisions and deployment generation; register every claim and its assumptions.
2. Repair both circular formats; model ticket equivocation, expiry, revocation, consumption binding and pruning.
3. Benchmark ledger-only and overlay delivery on identical payloads, demand and fan-out.
4. Run nominal, burst, partition, invalid-ingress and recovery workloads; measure percentiles and costs separately.
5. Compare full download, FMD, PIR and OMR under identical boards and workloads. OMR’s privacy tolerates malicious collusion; its basic correctness conditions differ. The catalog’s non-colluding-server summary must not replace the paper. [`2021-liu-omr`, §§4.1–4.3.]

**Strongest objection:** Simulation and bounded models provide conditional evidence. They cannot certify global anonymity or unrestricted deployment resilience.

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Own fixed-record alternative | Circular layouts; mandatory FMD/franking | `2021-beck-fmd` §1; compiler `midnight-events.ss:71` | Medium | Reviewed wire construction and sizing |
| D2 | g4, narrowed | General unlinkability claims | `2022-barnes-rfc9180` §9; pallet `lib.rs:575` | High | Combined stronger privacy argument |
| D3 | Full stream; repaired historic-root consumption | Unproved decoy privacy | compiler `midnight-ledger.ss:1260`; OMR §4 | Medium | Private retrieval beats measured scan cost |
| D4 | Funded capacity; separate admission trial | DUST as relay payment; cap-based sustainability | cost-model `:408`; Waku §V.B | Medium | Sustainable anonymous admission |
| D5 | Own measured baseline | Imported benchmarks | runtime `lib.rs:292`; Waku §IV | Low | Representative product measurements |
| D6 | Own 48-hour service window | TTL as deletion; unverifiable stripped records | VM `vm.rs:595`; intent spec `:131` | Medium | Recovery or cost evidence |
| D7 | o4, reduced | Unfunded duties; universal pause exemptions | service `:614`; filter `:44` | Medium | Operator and governance evidence |
| D8 | o1, gated | Native launch fork; unchecked ledger fallback | service `:644`; release notes `:22` | High | Supported isolated native extension |
| D9 | Own explicit residuals | Component-level guarantees applied globally | GossipSub formal §§3–5; MLS §16.6 | High | Combined-protocol analysis |
| D10 | Own claim-based gates | Feature completion as assurance | Dandelion++ Theorem 1; OMR §4 | High | Reproduced evidence satisfies gates |

The three likely disagreements are **D8**, whether ledger-only simplicity outweighs overlay capacity and isolation; **D4**, whether admission should use ledger tickets, RLN deposits or funded permits; and **D2**, whether launch privacy means full-stream selection privacy or accepts tag/FMD leakage for mobile efficiency.

The **one unknown fact with the greatest settling power** is the measured resource cost of a ledger-only `publish(Misc)` service on the target generation: serialized bytes and DUST per accepted event, proving and finalized-delivery latency, and indexer cost at agreed fan-out. Run that comparative prototype first. It would most directly settle whether an overlay is necessary and how admission and operator funding must work; it would not settle the security-model objections.