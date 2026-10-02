I support the shared sidecar architecture, but would narrow the launch guarantee to **content confidentiality and subscriber-interest privacy under recognition-independent fetching**. None of the reviewed proposals establishes general relationship privacy or global-observer anonymity. The main corrections concern cryptographic binding, decoy retrieval, admission economics and availability guarantees. Below, **G1** is `g1-protocol-architect`, **G2** is `g2-network-engineer`, **O1** is `o1-midnight-integrator`, and **O2** is `o2-economist-operator`. **L9** denotes `midnight-ledger@ledger-9.1.0.0-rc.5`; other Midnight paths are relative to `/home/charl/midnight/`. Positions are summarized from each proposal’s corresponding decision. New requirements and acceptance thresholds are **design assumptions**; deductions are labeled **inference**.

## D1 — Event format

- **G1:** Fixed 192-byte header, four body classes, static unicast/topic encryption, single-use ledger ticket and outer signature.
- **G2:** StrictNoSign GossipSub envelope with visible membership key, three body classes and separate large-body retrieval.
- **O1:** Four padded classes carrying recognition tags, FMD clues and Compact-RLN proofs; seven-day default lifetime.
- **O2:** Four padded classes, S-FMD clues and NIGHT-backed RLN-Diff proofs; ephemeral signing keys permit proof precomputation.

**Evidence check.** Waku supports G2’s StrictNoSign policy, but removes only GossipSub identity fields: G2 reintroduces a linkable `member_pk` in its envelope (`2020-vac-waku2-relay-spec`, “Signature Policy”). Waku’s message specification supports deterministic hashing and visible content topics; it does not validate any proposed custom encoding (`2020-vac-waku2-message-spec`, “Wire Format,” “Deterministic Message Hashing”).

Three bindings need repair:

- **G1:** Encryption authenticates the entire header, including `relay_sig`, while that signature covers the resulting ciphertext. The inner signature also covers the header. **Inference:** this creates circular construction dependencies as written (`design/rounds/r1/g1-protocol-architect.md:26`, `:41`, `:60`).
- **G2:** `created_unix_ms` and `ttl_s` are outside the signed hash. **Inference:** an intermediary can alter lifetime metadata without invalidating the signature (`design/rounds/r1/g2-network-engineer.md:27`).
- **O1:** The identifier includes the RLN record/proof, while the proof’s signal is `H(id)`. **Inference:** this is another circular dependency unless the identifier excludes proof-dependent fields (`design/rounds/r1/o1-midnight-integrator.md:13`, `:157`).

Beck supports O1’s **68-byte FMD construction**, not indistinguishability of arbitrary random filler from valid clues (`2021-beck-fmd`, §1, p.3). HPKE provides content protection; recipient anonymity requires separate analysis (`2022-barnes-rfc9180`, §9; `2001-bellare-keyprivacy`, §1.1).

**Vote:** **Own alternative**, retaining my Round 1 fixed 4,096-byte cells. Define an acyclic construction: immutable public header → inner authentication and encryption → cell identifier → admission endorsement. Seal complete session/control packets; MLS otherwise exposes group and epoch headers (`2023-barnes-rfc9420`, §§6.3,16.4). Require reviewed key hiding before claiming private recognition.

**Strongest objection:** Fixed cells and fragmentation impose substantial overhead on small events.

## D2 — Definition of “private”

- **G1:** Confidentiality and whole-shard interest hiding; explicitly excludes forward secrecy and global anonymity.
- **G2:** Confidentiality with disclosed shard, timing and volume leakage; a limited source-hiding stem.
- **O1:** Topic privacy, epoch unlinkability, Dandelion++ source privacy and session security; delegated FMD is weaker.
- **O2:** Anonymous membership, event unlinkability, shard/FMD interest privacy and partial cover-based privacy; relationship privacy follows from these.

**Evidence check.**

**G1:** Its rejection of static-key forward secrecy is supported by the Bitmessage starting analysis and review. Its assertion that knowing `enc_pk` permits trial decryption is incorrect: DH decapsulation needs the recipient **private** key. Public candidate keys are precisely what the key-privacy game permits the adversary to know (`2001-bellare-keyprivacy`, §1.1; `2022-barnes-rfc9180`, §§4,5). Knowing a symmetric topic secret does permit recognition.

**G2:** Its main refusals are supported, but “publisher unlinkability holds against non-stem neighbours” is too categorical. A neighbour may combine propagation observations and auxiliary information; the one-hop construction has no cited reduction. Waku itself excludes global observation and acknowledges direct-peer subscription leakage (`2020-vac-waku2-relay-spec`, “Adversarial Model”).

**O1:** Dandelion++ supplies model-specific mass-deanonymization results, not an unconditional minority-collusion guarantee. Its principal model excludes ISP/AS attacks and targeted deanonymization protection (`2018-fanti-dandelionpp`, §§3.1–3.3). The asserted `1/(k+1)` decoy-fetch uncertainty lacks a supporting theorem; it requires exchangeable candidates and priors, which repeated observations need not preserve. These are **unsupported assumptions**.

**O2:** RLN membership privacy does not hide ingress identity, online schedules or detection-server correlations. Therefore P7 does not follow from P2 and P4. Seres explicitly demonstrates relationship leakage when senders are known (`2021-seres-fmdfalsepositives`, §§1,4). Treasury-originated cover cannot, by itself, hide a user’s publication activity: **inference**.

**Vote:** **Own alternative**, with these adversaries and games:

| Class | Capabilities |
|---|---|
| Local observer | Relay, store, issuer or indexer sees its connections and records |
| Colluding infrastructure | Combines arbitrary infrastructure observations; “minority” alone supplies no guarantee |
| Global passive observer | Observes all endpoint/network timing, sizes and volumes |
| Active adversary | Injects, drops, replays, probes, partitions, eclipses and creates identities |
| Insider/endpoint adversary | Possesses capabilities, plaintext or compromised endpoint state |

Content confidentiality compares equal-length payload substitutions under identical public leakage. Subscriber-interest privacy compares different interest sets while keeping fetching, online schedules, retries, errors and public application reactions identical. Both require uncompromised challenge keys and reviewed cryptography. Publisher unlinkability, hidden participation and general relationship privacy are **not launch claims**. Session forward secrecy requires erasure; recovery requires appropriate uncompromised updates (`2019-kuhn-privacynotions`, §§3–5; `2016-signal-double-ratchet-spec`, §§8.1–8.4).

**Proposed leakage contract — architectural inferences:**

| Observer | Learns |
|---|---|
| Relay | Peer/client IPs, participation, cell IDs, admission metadata, arrival timing, aggregate volume; direct ingress can identify publishers |
| Indexer | Public contract activity, queried contracts, client connections and cursors |
| Chain observer | Public transcripts, commitments, fees, timing and unshielded funding information |
| Colluding minority | Union of observations, registration/ingress correlations and opportunities for targeted probing |
| Global observer | Endpoint activity, uploads, downloads and catch-up patterns; public reactions permit correlation |
| Capability holder | Its authorized plaintext and recognizable channel traffic |

Whole-feed reception protects **which cells are recognized**, conditional on the game above. It does not protect all facts in this table.

The bounds require precision:

1. For synchronized users, Theorem 2 excludes strong anonymity when \(2\ell\beta<1-\epsilon(\eta)\), under its conditions including \(\ell<N\) and \(\beta N\ge1\). These are model rounds and dummy rates, not seconds and ordinary replication bandwidth. Zero-cover cases require the appropriate earlier bound, not substitution outside Theorem 2’s conditions (`2017-das-trilemma`, §V, Theorems 1–2).
2. Coordination also has necessary costs: the broader model excludes strong anonymity when \(\hat\ell(B+1)<N-\epsilon(\eta)\), subject to its stated conditions (`2020-das-comprehensivetrilemma`, §5.2, Theorem 2).
3. Gossip source \(\epsilon\)-DP requires \(\epsilon\ge\ln(f-1)\) for \(f>1\); no finite worst-case \(\epsilon\) exists when vertex connectivity is at most \(f\). Here \(f\) is a **node count**, not a fraction (`2023-guerraoui-inherent-anonymity-gossiping`, §4.2, Theorem 5).
4. Classical information-theoretic single-server PIR requires linear communication; computational PIR escapes that particular bound. Strong detection-key-unlinkable OMR implies PIR with corresponding costs, not universal linear server computation (`1998-chor-pir`, §§1.3,5.1; `2026-fisch-unifomr`, Theorem 5.1).

**Strongest objection:** Useful agents often react publicly; those reactions lie outside the restricted reception guarantee.

## D3 — Publish and subscribe

- **G1:** Out-of-band capabilities, whole-shard trial decryption, no acknowledgments; contracts receive later commitment transactions.
- **G2:** Open/private shards, local filtering and explicitly weaker filtering services; contracts consume later transactions.
- **O1:** PRF tags, FMD first contact, mobile tag indexes with four decoys, and private anchored witness consumption.
- **O2:** Whole-shard or S-FMD reception; contracts consume against an anchor ring through a submitted call.

**Evidence check.** G1 and G2 correctly separate off-chain reception from contract execution. The checked VM has a `Log` operation; Compact’s cross-contract capability does not introduce network subscriptions (`L9:onchain-vm/src/ops.rs:156`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:24`). Waku Filter explicitly receives content-topic interests (`2020-vac-waku2-filter-spec`, “Subscribe,” “Security Considerations”).

O1’s `HistoricMerkleTree.checkRoot` and witness-free callee claims are supported (`minokawa-compact/doc/ledger-adt.mdx:607`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:101`). Its pseudocode does not establish the complete event → batch → anchor binding: `batchPath` is declared but not checked. Furthermore, public `H(ev.id || domain)` is recognizable to anyone knowing candidate event IDs; domain separation prevents identical outputs across domains, not candidate testing. These are **inferences**.

O2’s exported event-byte arguments require explicit disclosure analysis; calling them private is unsupported. Both anchored designs also need publisher authorization independently of membership in an aggregator-selected batch.

**Vote:** **Own alternative**, borrowing O1’s nested witness concept after correcting the circuit. Launch with authenticated invitations and complete-feed fetching. Separate recognition from transport; repair all inventory differences, never only matched events. Contracts verify event authorization, binding, application conditions and replay protection through an explicit transaction. Use a secret-bearing nullifier construction, rather than a publicly testable event-ID hash.

The existing local wallet scan is a useful implementation pattern, not an existing bus capability (`midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:243`, `:266`).

**Strongest objection:** Complete-feed reception excludes many mobile users unless a separately proved private retrieval profile is added.

## D4 — Sustainable model

- **G1:** DUST-funded single-use tickets, bounded chain share; relay funding remains external.
- **G2:** DUST-funded hourly membership and signature-enforced credits; relays initially unpaid.
- **O1:** Compact-RLN memberships with revocation, subsidized operators and later anonymous service payments.
- **O2:** NIGHT bonds and registration fees fund a treasury; RLN slashing, storage challenges and paid retrieval support operators.

**Evidence check.** All correctly distinguish DUST fees from relay revenue. DUST is non-transferable gas capacity; checked spends subtract public `v_fee`. That supports the distinction, not a complete proof of every claimed burn/no-credit path (`midnight-docs/docs/concepts/dust-architecture.mdx:23`; `L9:ledger/src/dust.rs:469`, `:1765`).

G1/G2’s categorical “Midnight cannot slash” is too broad. Compact has actual unshielded receipt and transfer circuits, supporting O2’s bond direction, while leaving the full NIGHT custody/slashing application **unknown until tested** (`minokawa-compact/compiler/standard-library.compact:313`, `:322`).

RLN literature supports double-signal accountability, not solvency or sufficient spam pricing. RLN-v2 also binds the user’s rate into the membership commitment; that binding must survive translation to Midnight (`2022-taheri-waku-rln-relay`, §II-B; `2024-vac-rln-v2-spec`, “RLN-Diff flow”).

O2’s precomputation changes the signal to `H(ephemeral_pk)`. **Inference:** one key can sign multiple bodies under the same proof/share without yielding two distinct RLN share coordinates. Local first-seen rejection does not restore slashing accountability across partitions. O1’s native off-chain verifier remains explicitly unknown.

**Vote:** **O2, with reservation**, for its transferable funding and paid storage/retrieval direction. Block adoption of its exact admission construction until body equivocation is provably punishable. Launch funding must also cover relay egress explicitly; slashes are incidental income, not a dependable operating budget. My signed-capacity admission remains the fallback.

**Strongest objection:** O2’s economic guarantees depend on an admission mechanism whose accountability fails as presently specified.

## D5 — Performance requirements

- **G1:** 50 objects/s, degree six, roughly 2.2 Mbit/s mesh traffic and p99 ≤10 seconds.
- **G2:** Degree eight, roughly 104 class-S messages/s per relay and p99 ≤2 seconds at 1,000 relays.
- **O1:** 50 envelopes/s, 250/s bursts, small mobile downloads and relay verification below 0.3 core.
- **O2:** 100 events/s, 1,000/s peaks, precomputed proofs and p99 ≤3 seconds.

**Evidence check.**

- **G1:** The size mix totals 100.1%; its signature-cost constant is a ledger pricing parameter, not a relay benchmark (`midnight-node/res/mainnet/ledger-parameters-config.json:124`). Normalize the mix and measure actual verification.
- **G2:** Farooq supports its planning topology and link assumptions, not a percentile guarantee. G2 correctly notices the paper’s inconsistent 5,520-ms example (`2025-farooq-staggering`, §IV). Its 211-byte envelope changes the nominal \(3,000,000/[7(4096+211)]\) capacity to approximately **99.5/s**, before control traffic and client egress: **arithmetic inference**.
- **O1:** Beck’s 0.548-ms benchmark supports the selected detector measurement. But every envelope carries a clue and first-contact traffic is supposed to be indistinguishable. Testing 50 clues/s costs 0.0274 CPU-seconds/s per delegated key: approximately **36 clients/core**, not 365, absent a justified skip mechanism (`2021-beck-fmd`, §1, p.3). Store egress also includes body fetches.
- **O2:** Waku measures 2.7–18.7-ms verification on named platforms; those measurements do not transfer to Midnight-native RLN or establish latency with the proposed stems (`2024-revuelta-waku-latency`, Table 1, §§3,5).

**Vote:** **G2’s budgeting method**, with corrected byte counts and my privacy workload. Count cells, fragments, control traffic, proof checks and subscriber egress separately. My proposed capacity experiment remains 100 cells/s and 1,000 whole-feed consumers. At 4,096 bytes/cell, each consumer receives **35.389 GB/day**; this is arithmetic, not measured capacity.

The chain comparison must respect both ledger limits and runtime block limits; the runtime reserves only 75% of its 1-MiB length for Normal dispatch (`midnight-node/runtime/src/lib.rs:300`, `:312`; `midnight-node/res/mainnet/ledger-parameters-config.json:158`).

**Strongest objection:** A relay-capacity result can conceal an economically or physically unusable subscriber download budget.

## D6 — Storage requirements

- **G1:** Retain through expiry, approximately 100 MB at its workload; hard store caps and optional archives.
- **G2:** Ten-minute relay cache, optional 24-hour stores and seven-day anchored storage.
- **O1:** Seven-day stores, fourteen-day maximum, proofs stripped after anchoring; availability is best effort.
- **O2:** TTL-based bonded stores, bounded anchor ring and challenge-enforced retrieval.

**Evidence check.** G1’s apparent one-hour lifetime conflicts with its requirement `expiry ≤ (ticket_epoch + 2)*600`: **inference**, actual ticket-relative lifetime is shorter. G2’s 24-hour envelope lifetime does not imply 24-hour availability from its ten-minute cache.

O1 correctly distinguishes existence commitments from availability. However, its ID hashes the complete RLN record; stripping proofs requires retaining a checkable commitment representation and specifying what later clients verify. O2’s statement that challenges enforce retrievability overstates their effect. **Inference:** punishment after failed retrieval cannot supply missing bytes, prove continuous availability, or prevent challenge-time borrowing.

The fourteen-day ledger TTL governs ledger replay/history mechanisms; it does not impose an off-chain retention requirement (`midnight-node/res/mainnet/ledger-parameters-config.json:176`; `/home/charl/privateEvents/notes/midnight-network-stack.md`, §7.5).

**Vote:** **Own alternative:** 48-hour mandatory relay retention and optional seven-day archives. At 100 fixed cells/s, raw replica storage is **70.779 GB/48 hours** and **247.726 GB/seven days**, excluding indexes: arithmetic inference. Promise delivery only if a surviving honest holder is reachable before expiry and the client can catch up. Keep application commitments/nullifiers on chain; treat challenges as incentives.

**Strongest objection:** Uniform retention forces every replica to pay for unrelated traffic.

## D7 — Infrastructure actors

- **G1:** Permissioned launch relays, separate from validators; open membership only after red-team testing.
- **G2:** Separate bootstrappers, open scored relays and optional stores; payment comes later.
- **O1:** Permissionless relays/aggregators, subsidized stores and client-selected detection services.
- **O2:** Open relaying, bonded paid stores/anchorers, foundation launch and measured governance transition.

**Evidence check.** Validator exclusion has direct support: Midnight deliberately avoids serving expensive ledger snapshots on authorities by default (`midnight-node/node/src/service.rs:614`). Genesis specifies ten permissioned candidates and zero registered candidates, not the live operator population (`midnight-node/res/mainnet/system-parameters-config.json:7`).

G1’s allow-list makes operator control explicit, but a failed red-team attack does not prove permissionless safety. G2/O1’s scoring does not create independent operators or sustainable supply (`2020-leastauthority-gossipsub-audit`, “General Comments,” “Recommendations”). O2’s concern about reputation gaming is supported by Nym framing and operator-concentration findings; its per-key saturation cap does not enforce per-operator independence (`2026-cao-nymreputation`, §4.2, Appendix D).

**Vote:** **O2’s phased operator plan, with reservation.** Fund independent stores and feed service, keep relay operation open, and disclose launch concentration. Governance-transition gates must measure organizations and correlated infrastructure rather than merely bond keys. Admission issuers/providers remain explicitly trusted within their respective roles.

**Strongest objection:** Pseudonymous keys cannot establish the independent-operator counts required by decentralization gates.

## D8 — Network tether

- **G1:** Sidecar overlay plus ledger tickets; fallback is a new non-validator node notification protocol.
- **G2:** Sidecar overlay plus memberships/anchors; fallback is a public commitment channel.
- **O1:** Sidecar overlay plus membership and anchors, detailed upstream register; multipart-ledger fallback.
- **O2:** Sidecar plus Registry; low-volume ledger/indexer fallback and wallet/connector additions.

**Evidence check.** The shared primary choice is supported. I checked the lockfile: GossipSub/FloodSub packages are absent. Node registrations are GRANDPA, BEEFY and ledger-sync; adding a bus there requires implementation work (`midnight-node/Cargo.lock:14548`; `midnight-node/node/src/service.rs:574`).

O1’s generation caveat is correct: local node dependencies identify ledger 9, Compact 0.33 introduces events/cross-contract calls, and the documentation matrix still lists mainnet 0.31.1 (`midnight-node/Cargo.toml:472`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`; `midnight-docs/docs/relnotes/support-matrix.json:38`). Actual activation remains **unknown**.

Multipart is **Proposed**, not an already accepted transport standard (`midnight-improvement-proposals/mips/mip-0019-multipart-event.md:6`). `Misc` exposes a public name and payload, and indexer queries require a contract address (`minokawa-compact/compiler/midnight-events.ss:71`; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`, `:1157`).

**Vote:** **O1’s primary architecture and dependency register**, replacing its fallback with independently operated complete-feed servers preserving the same reception interface. A ledger commitment channel may serve applications separately, with explicitly different leakage.

**Strongest objection:** A fallback that changes fetching or exposes contract-specific interest cannot inherit the overlay’s privacy label.

## D9 — Threats and open risks

- **G1:** Tickets, allow-list, heuristic stems and strict parsing; accepts static-key compromise.
- **G2:** Scoring, outbound quotas, epoch caps and a GossipSub CVE gate; admits first-hop/global leakage.
- **O1:** RLN, Dandelion++, cover floor, ratchets, anchors and delegated-FMD limits.
- **O2:** Bonds, slashing, challenges and treasury controls; accepts provider dependence and key splitting.

**Evidence check.** G2’s outbound-quota mechanism is supported against coordinated **inbound** takeover, not malicious outbound selection generally (`2020-gossipsub-v11-spec`, “Outbound Mesh Quotas”). Its CVE concern is supported; the ACL2s paper found counterexamples and did not certify arbitrary application parameters (`2023-kumar-gossipsub-acl2s`, §§1,5).

G1’s signature proves authorization by a ticket key, not that its malicious holder signs only one body: **inference**. O2 has the same problem after precomputation, without distinct-share slashing evidence.

O1’s “no material replay residual” and O2’s “none” omit partitions, rollback, downstream duplicate effects and equivocation. Ratchets/MLS also require update delivery and erasure; malicious delivery can suppress PCS recovery (`2016-signal-double-ratchet-spec`, §§8.1–8.4; `2023-barnes-rfc9420`, §16.9).

**Vote:** **Own alternative**, with these mandatory residuals:

| Threat | Required defense and residual |
|---|---|
| Eclipse/Sybil | Diverse bootstrap/outbound sources and inventory comparison; full eclipse still defeats availability |
| Spam | Message-bound admission, byte/retention quotas and bounded verification queues; wealthy valid publishers can saturate capacity |
| Recipient probing | Fetching, errors, retries and acknowledgments independent of recognition; application responses can reveal receipt |
| Replay | Transport deduplication plus authenticated logical IDs and transactional application nullifiers; rollback remains relevant |
| Key compromise | Separate admission/discovery/session secrets, ratchets and erasure; persistent compromise defeats recovery |
| Censorship/indexer abuse | Independent holders and chain verification; roots/counts do not prove global completeness |

FMD remains a distinct weaker profile. Expected returned messages are \(t+p(M-t)\), not merely \(pM\); repeated observations can recover relationships (`2021-seres-fmdfalsepositives`, §§2,4). A future mix profile must specify schedules, cover, compromised placement and enrollment assumptions; importing a hop does not import Loopix’s security (`2017-piotrowska-loopix`, §2.2).

**Strongest objection:** Ordinary application replies can defeat transport privacy even when the transport satisfies its restricted game.

## D10 — Build and verification plan

- **G1:** Parser/admission circuit first, numeric mesh gates, then an allow-list removal experiment.
- **G2:** Mesh simulation and CVE checks, sidecar testnet, later privacy/payment features.
- **O1:** Native-RLN and anchor spikes, state-machine models, network/FMD simulation, integration and advanced profiles.
- **O2:** Proof/economic measurements and Registry invariants before funded rollout.

**Evidence check.** O1’s native-verifier and concurrent-root spikes directly address unknown integration facts. O2’s accounting invariants are useful, but their validity does not establish privacy, retention or market sufficiency.

G1/O1’s first-spy thresholds cannot be derived by multiplying Dandelion++’s \(p^2\) floor. That is a lower bound on achievable expected precision in a specified model, not a universal upper-bound acceptance test for these meshes (`2018-fanti-dandelionpp`, §§3.2–3.3). G2 overstates the existing ACL2s model as a scoring “specification of record”; new applications require tailored counterexample generators (`2023-kumar-gossipsub-acl2s`, §5).

Old OMR costs justify measuring alternatives, not excluding the entire class. UnifOMR’s reported approximately 25-second/4-MB result uses \(2^{19}\) messages with 612-byte payloads; it is neither a bus benchmark nor an impossibility result (`2021-liu-omr`, “Implementation and Evaluation”; `2026-fisch-unifomr`, Abstract, §8).

**Vote:** **O1’s spike-first plan, amended** to put these gates before deployment:

1. Eliminate circular dependencies and prove message/admission/anchor bindings.
2. Compare interest-swapped executions under active omissions, malformed matches, reconnects and backpressure.
3. Test equivocation across partitions, old roots, revocation and crashes.
4. Measure complete feed, retrieval, proof and replication costs on named hardware.
5. Verify bridge authorization and replay protection against a false indexer.
6. Obtain funded operator commitments before claiming sustainability.

First-spy experiments quantify leakage; they do not prove anonymity.

**Strongest objection:** Successful finite experiments cannot establish universal privacy guarantees.

## Decision record

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Own fixed-cell alternative | Current circular/unbound formats | RFC9180; RFC9420; D1 checks | Medium | Reviewed efficient alternative |
| D2 | Own restricted games | General relationship/source claims | Trilemma; gossip Thm.5; PIR/OMR bounds | High | Applicable composition proof |
| D3 | Own complete-feed model | Decoys/FMD as equivalent privacy | Seres §4; wallet `Sync.ts:243` | Medium | Verified private thin-client retrieval |
| D4 | O2, conditional | DUST as operator revenue; unsafe precomputation | RLN-v2; standard library `:313` | Medium | Safe admission and funded bids |
| D5 | G2 method, corrected | Imported percentiles/CPU estimates | Waku Table 1; explicit arithmetic | Medium | End-to-end measurements |
| D6 | Own bounded replication | Anchors/challenges as availability | D6 arithmetic; MIP-0019 `:78` | Medium | Different offline requirements |
| D7 | O2, conditional | Key counts as independence | Nym §4.2/Appendix D | Medium | Independent operator evidence |
| D8 | O1 primary; feed fallback | Silent privacy-changing fallback | Node `service.rs:574`; Compact `:22` | High | Isolated native transport |
| D9 | Own threat contract | “No residual”; component-name guarantees | Dandelion++; Seres; MLS §16.9 | High | Stronger reviewed defenses |
| D10 | O1, amended | Classifier/benchmark as proof | ACL2s §5; UnifOMR §8 | High | Failed binding/privacy/resource gates |

The three likely disagreements are **D2**, over the meaning of subscriber and relationship privacy; **D3**, over complete-feed reception versus mobile FMD/decoy retrieval; and **D4**, over ledger tickets, native RLN and funded admission.

The single fact most likely to settle disagreement is: **can a correctly message-bound, revocable Midnight-native RLN admission implementation sustain 100 cells/s off chain on the proposed relay hardware?** A checked implementation result would resolve much of the dispute over format, admission, performance, operator costs and build dependencies. It would not establish network anonymity.