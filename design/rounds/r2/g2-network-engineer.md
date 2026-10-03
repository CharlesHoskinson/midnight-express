I'll follow the charter and review the four Round 1 proposals against the network evidence, starting with the charter and the cited sources.The charter and my Round 1 position are in hand. Next I’ll read the four proposals and check the citations they rely on.The four proposals split on whether the bus is a GossipSub sidecar or the ledger first. I’ll check the citations those positions rest on, starting with the Midnight node and the gossip papers.The bus should be a separate GossipSub sidecar. Validators stay off it, contracts cannot subscribe, DUST cannot pay a relay, and none of the four proposals earns a claim of strong anonymity against a global observer. Those points are held in common and the citations behind them check out. What does not check out is a mesh a builder can configure. s3-red-team has the privacy claims and the threat list. s2-cryptographer has the only admission object whose size I could recompute from the cited RFC. o2-economist-operator has the only operator path with a checkable payout, and a slash story the cited RLN spec does not support. o3-consumer-experience has the only consumer API, and it makes the indexer the bus. Per-message zero-knowledge proofs stay off the relay hot path until one measurement says they fit.

## D1. Event format

**(a)**
- **s2-cryptographer:** Fixed 1,024- or 4,096-byte cells; sealed Double Ratchet header; 354-byte public Privacy Pass stamp; seven-day expiry.
- **s3-red-team:** One 4,096-byte cell; 1,152-byte RLN admission area; sealed session header; 48-hour retention; no relay-visible topic.
- **o2-economist-operator:** Classes 1/4/16/64 KiB; visible shard, epoch, RLN fields and an S-FMD clue; TTL up to 14 days; on-chain class is `Misc`.
- **o3-consumer-experience:** Phase 1 carrier is `Misc` (32-byte tag + 256-byte parts); usable bodies 207 / 975 / 4,047 bytes; Lane B later reuses the same envelope.

**(b)** s2’s stamp layout matches RFC 9578 §6.3 and §8.2.2: token type 2 + nonce 32 + challenge digest 32 + key id 32 + authenticator `Nk`, and §8.2.2 sets `Nk` to 256 for Blind RSA-2048, so 354 bytes is right. The Double Ratchet spec §7.2 recommends an AEAD “based on either SIV or a composition of CBC with HMAC,” and §4.2 requires a header nonce that is non-repeating or random with at least 128 bits. SIV is one recommended family. MLS `PrivateMessage` really does carry `group_id` and `epoch` in the clear (`2023-barnes-rfc9420` §6.3), and §16.4.1 says MLS provides no mechanism to hide them from the delivery service. The PQXDH spec I opened exemplifies Kyber-1024 and says authentication stays classical; s2’s move to ML-KEM-768 is what they labelled an integration assumption. I did not open FIPS 203, so those byte counts are unverified here.

s3’s 1,152-byte admission area is an assumption. The RLN paper they cite uses Groth16 on Ethereum (`2022-taheri-waku-rln-relay`), not a Midnight proof of that size. The 48-hour bound is their requirement, not a cited constant.

o2’s `global_ttl` of 1,209,600 s is in `midnight-node/res/mainnet/ledger-parameters-config.json:176`. The ledger spec defines it as the intent validity window (`tblock <= ttl <= tblock + global_ttl`), not as event retention. Waku’s 20 s figure is the maximum gap `g` between a node’s clock and the epoch a proof was made for (`2024-revuelta-waku-latency`, before the analytical model, and restated as a conclusion in §8). It is not a rule that a 60-second epoch id must lie within 20 s of the clock. The RLN-v2 text they cite for the share implements the circuit in Groth16; the envelope’s “PLONK/KZG” is a different proof system. The ~68-byte clue is marked assumption; Beck’s 68-byte flag (`2021-beck-fmd`) is not a Penumbra clue size I found in `2022-penumbra-fmd`.

o3’s `Misc` layout is in the working compiler: `minokawa-compact/compiler/midnight-events.ss:71-74` is `{name: Bytes 32, payload: Bytes 256}`. MIP-0019 is still `Status: Proposed`. `MAX_LOG_EMITTED` is not in the working trees I searched. The network-stack read-out quotes it from the `ledger-9.1.0.0-rc.5` archive as 1 KiB with a silent drop. o3 says they did not re-read that archive. The working `onchain-vm/src/vm.rs:38` only has `MAX_LOG_SIZE = 1 << 19`. The silent-drop claim stands on the read-out, not on a file I opened.

**(c)** None of the four is a relay frame I would ship. The alternative keeps s3’s single padded 4,096-byte cell and sealed topic, puts s2’s 354-byte public stamp in the admission area, and keeps s3’s 48-hour cap. A per-hop Groth16 or PLONK proof is not part of version 1.

**(d)** The strongest objection to that cell is s2’s and s3’s: a visible shard or nullifier lets a mesh neighbour link one publisher’s messages, and a single padded feed avoids that only by making every client read every cell.

## D2. Definition of private

**(a)**
- **s2:** Content confidentiality and recipient concealment from infrastructure; metadata and global unlinkability are not claimed.
- **s3:** Separate claims for confidentiality, interest privacy, and anonymity; no release guarantee for timing, volume, or relationship privacy; the trilemma is not a numerical proof for this overlay.
- **o2:** P1–P7, including publisher anonymity via RLN and a Dandelion stem; global-observer unlinkability is out of scope.
- **o3:** Confidentiality, PRF topic privacy, full-mode interest privacy, and chain-level publisher unlinkability; global timing is out of scope.

**(b)** The trilemma abstract and the synchronised-user bound are about a synchronous-round model with bandwidth overhead `β` and latency overhead `ℓ` (`2017-das-trilemma`). s3’s refusal to treat `2βℓ` as a number for this asynchronous bus matches the paper’s hypotheses. s2’s and o3’s abstract-level citations, and o2’s “cover or latency” reading, are fair. They are not a calculation for these parameters.

Dandelion++ §3.1 says an ISP or AS adversary, modelled as corrupted edges, is outside the paper’s scope. o2’s leakage row says a stem hides the publisher’s IP from all but the first hop, while the publish path is 2–4 hops of Dandelion++. The paper’s bound is a spy fraction on an approximately 4-regular graph, not that sentence. s3’s use of §3.1 is the one that matches the text.

o2’s “a double-signal reveals `a0 = identity_secret`” does not match `2022-vac-rln-v1-spec`: `a_0 = identity_secret_hash`, and the spec says a double signal lets anyone derive that hash. Publisher anonymity against relays still follows from the zero-knowledge membership proof if the proof is the one in the spec. The slash identity does not.

o3’s chain-observer row depends on shielded DUST and the absence of a Substrate signer. The read-out states both; I confirmed `DustSpend.v_fee` is a public field in the upstream `dust.rs` and that the docs call DUST shielded and non-transferable (`dust-architecture.mdx:23`). The submission node still sees IP plus transaction, which o3’s own table says. Relationship privacy “except through timing” is their inference.

Indexer `contractEvents` requires `contractAddress` (`schema-v4.graphql:548-552`). That supports every proposal’s claim that a contract filter tells the indexer which contract is watched. The wallet path stores an encrypted viewing key and trial-decrypts (`midnight-indexer/docs/architecture.md:20-28`). s3’s “server-assisted wallet can disclose its viewing key” is supported for that path.

**(c)** Vote **s3-red-team**. The claims are separated, the leakage table is labelled as a design description, and the trilemma and Dandelion citations are the ones that match the papers.

**(d)** The strongest objection is inside s3’s own later phases: an experimental mix is still on the roadmap, and a reader can take that phase as the global-observer property their D9 block says not to claim.

## D3. Publish and subscribe

**(a)**
- **s2:** One transport topic; invitation-only sessions; local trial of a 56-byte header; at most 32 recipient ciphertexts; contracts via a later transaction.
- **s3:** One common feed; local recognition; whole-interval backfill; no directory; contracts via an asserted signature and a replay nullifier.
- **o2:** 16 shards; S1 mesh, S2 store download, or S3 S-FMD; contracts check an anchor ring.
- **o3:** PRF tags on a shared bus contract; full download by default; opt-in bucket mode; chain order and a portable cursor; contracts via a relayed Merkle proof.

**(b)** Encrypted-header trial decryption with current, next, and skipped header keys is Double Ratchet §4.6, as s2 says. Waku filter’s security note says light clients must disclose content topics to the full node (`2020-vac-waku2-filter-spec`, Security Considerations). o3’s rejection of that pattern is supported. Gervais shows SPV clients with fewer than 20 addresses can leak essentially all of them through one Bloom filter (`2014-gervais-bloomfilters`). Seres shows an FMD server that knows senders can recover much of the social graph, and that selfish users drop cover (`2021-seres-fmdfalsepositives`). Frank’s abstract says FMD is not viable with selfish users and needs altruists. o2’s claim that a clue-format floor stops the subscriber choosing `p` does not match Penumbra: S-FMD lets the sender choose the false-positive rate (`2022-penumbra-fmd`). A floor of `1/64` is o2’s parameter. A sender can still pick a tiny rate.

`ed25519Verify` exists and must be asserted (`exports.md:993-1005`). Historic-Merkle membership is the documented pattern. o2’s and o3’s cross-contract root check cites Compact 0.33’s witness restriction (`toolchain-0.33.0.md` introduces cross-contract calls). I did not re-open the restriction lines; treat feasibility as the inference they already labelled. The indexer subscription really does replay from an id and then follow `BlockIndexed` (`contract_event.rs:98-152`). o3’s “at least once” citation matches `public-data-provider.ts:507-508`. Monero’s view-tag note at the cited line is the 1/256 skip, so o3’s “255 of 256” is that PR’s expectation. The 50 µs figure is their assumption.

**(c)** Vote **s3-red-team**. One feed, local recognition, no remote topic filter, and a contract path that treats the witness as untrusted. That is the subscribe model a gossip mesh can carry without teaching a relay the application topic.

**(d)** The strongest objection is fan-out. s3’s own arithmetic at 10,000 subscribers is 6.554 Gbit/s of payload before overhead. A gateway that serves the whole feed is a new trusted interceptor, which their leakage table already records and their design does not replace.

## D4. Sustainable model

**(a)**
- **s2:** Public blind-RSA stamps; a service pool pays contracted relays; DUST pays only Midnight transactions.
- **s3:** Prepaid leases; RLN-style cap of 300 credentials at one cell per 30 s; revoke equivocators; do not promise slashing yet.
- **o2:** NIGHT-bonded RLN-Diff memberships, slashing, a treasury that pays anchors and challenged storage; relays unpaid.
- **o3:** Publishers pay about 0.06 DUST per Lane A event; readers pay nothing; RLN only on Lane B.

**(b)** DUST is documented as shielded and non-transferable gas (`dust-architecture.mdx:23`). Generation at `generation_decay_rate` 8,267 and `night_dust_ratio` 5,000,000,000 yields 0.714 DUST per NIGHT per day, and the same page’s 71 DUST/day for 100 NIGHT matches. The reward hook returns `(0, None)` at `runtime/src/lib.rs:691` and `:695` (line 681 is the struct). s2’s “no relay reward in this hook” is right. The read-out’s fee-burn statement is still an inference; o2 labels it that way.

Laurie and Clayton’s 5.8 s is their 2004 arithmetic so a spammer’s PC cannot profit at the prices they assumed (`2004-laurie-proofofwork` §3.1). It supports “flat PoW prices the honest sender and the stolen-compute sender alike.” It is not a modern cost.

Privacy Pass public verification uses the issuer public key (RFC 9578 §6.4). o2’s rejection of Privacy Pass, because “the issuer is the verifier,” fits the 2018 private VOPRF, not the public token s2 specified. s2 still needs every relay to have the issuer public key. That is not the issuer’s secret.

RLN slashing in the cited v1 spec reveals `identity_secret_hash`, and v2 says verification stays as in v1 while the circuit is Groth16. o2’s `slash(sk)` with a Midnight PLONK proof over `transientHash(sk)` is a new circuit. Midnight’s proof system is PLONK with KZG over BLS12-381 (`midnight-zk/README.md:12`). Nothing I opened shows that circuit verifying inside a Compact contract at relay rate. s3’s “do not promise automatic slashing” matches that gap. Nym’s paper does show a packet-dropping attack that cuts the cost of dominating the active set by over 99% (`2026-cao-nymreputation`). That supports o2’s refusal to pay relays for a performance score. It does not show that unpaid relays will exist.

o3’s 0.06 DUST figure is the read-out’s genesis inference (fixed-point `overallPrice` in the JSON is `10 * 2^64`, factors are `1 * 2^64`). Live prices are not that file’s raw integers. Per-event DUST means every event is a transaction. The block-usage limit of 1,000,000 bytes (`ledger-parameters-config.json:158`) is what caps that lane.

**(c)** Vote **s2-cryptographer** for version 1. The stamp size is checked, verification is public, and relay payment is a contract rather than a score. Keep s3’s refusal to promise a slash the chain cannot yet run.

**(d)** The strongest objection is the issuer. Issuance time is visible to them, a bad issuer mints capacity, and object-binding means stamps cannot be stockpiled independently of the ciphertext. s2 states this and does not remove it.

## D5. Performance requirements

**(a)**
- **s2:** 10 cells/s normal, 100 stress; p50 ≤ 2 s, p95 ≤ 5 s, p99 ≤ 15 s; a six-peer planning mesh.
- **s3:** 10 real cells/s, 20 during recovery; p50 ≤ 5 s, p95 ≤ 20 s, p99 ≤ 35 s; client 7.078 GB/day.
- **o2:** 100 events/s, p50 ≤ 1 s, p99 ≤ 3 s; D = 8; full relay about 39 Mbit/s.
- **o3:** Lane A at 1/s average and 10/s peak, p50 about 23 s, p99 ≤ 60 s; Lane B borrows Waku’s under-1 s result.

**(b)** GossipSub v1.1’s parameter table defaults `FloodPublish` to true and `D_out` to 2 when `D` is 6, with `D_out < D_lo` and `D_out ≤ D/2`. The evaluation that used D = 8, D_low = 6, D_high = 12 and gossip factor 0.25 is `2020-vyzovitis-gossipsub`, as o2 says. None of the four sets `D_out`, the heartbeat, or the gossip factor.

Revuelta’s conclusion (§8) and the results text say messages of 25 KB or smaller were always delivered in under 1 s, in a 1,000-node Shadow run at D = 6 and in their multi-host path. Table 1’s verification column runs from 2.7 ms on an M1 to 18.7 ms on a Raspberry Pi 4. o2’s “≤ 1 s for ≤ 25 KB” is in that paper. Their design adds a 2–4 hop stem and a Midnight proof the experiment did not run. The 2.7–18.7 ms range is nwaku’s Groth16 RLN, not Midnight’s `proof_verify_constant` of 3,273,586,253 (about 3.27 ms if that field is picoseconds) at `ledger-parameters-config.json:128`. Using both numbers as the same verify cost is not supported.

s2’s and s3’s byte arithmetic checks: s3’s 20 × 4,096 = 81,920 bytes/s, and 10,000 × that is 819.2 MB/s. s2’s `0.75 × 1,048,576 / (8,192 × 6) = 16` matches `NORMAL_DISPATCH_RATIO` of 75% and `SLOT_DURATION` of 6 s (`runtime/src/lib.rs:292`, `:300`, `:312`) under their 8 KiB assumption. o2’s `100 × 6 KiB × 8` is about 39 Mbit/s of copies at degree 8. D_high in the same evaluation is 12, so 8 is the target, not the mesh high-water mark. Farooq’s Shadow setup is 50 Mbps and 100 ms edges (`2025-farooq-staggering`). o2’s full-relay target sits on most of that planning link. The paper’s printed 5,520 ms for a 1 MB message does not match recomputing `(100 ms + transmit) × 4` in one unit system; I do not use 5,520 ms.

o3’s indexer bottleneck is real in the code: each `contractEvents` subscription queries on `BlockIndexed` (`contract_event.rs:125-146`), the pool is 25 (`config.yaml:30`), and the batch is 20. `max_concurrent_per_connection: 20` is the quota key they read as “20 subscriptions.” The 52 MB/day figure uses an assumed deflate factor. The 18 s finality is `mps-0028`, which I did not open; the 6 s slot is in the runtime.

**(c)** None of the four is an acceptance target. The alternative is the v1.1 profile the evaluation actually ran: D = 8, D_low = 6, D_high = 12, D_out = 4 (top of the legal range for D = 8), gossip factor 0.25, heartbeat 1 s, flood-publish off on this feed, and a 4 KiB full-message cap. Launch rate is s3’s 10 cells/s, not o2’s 100/s. Targets to measure, not claimed results: class-S p99 ≤ 2 s at N = 1,000 with no attack; stop if p99 > 6 s or delivery < 99% at N = 200. Egress planning uses multiplier 7 (degree minus the sender) and the 50 Mbps / 100 ms link as Farooq’s simulator setup.

**(d)** The strongest objection to that profile is that the 2 s target is a planning extrapolation under those link assumptions. Revuelta already measured a 1,000-node mesh, and their under-1 s result includes RLN verify that this profile deliberately does not have. A product that accepts s3’s 35 s would keep a mesh this stop would reject.

## D6. Storage requirements

**(a)**
- **s2:** Seven-day complete replication; about 6.38 GB of raw cells at 10/s, provision 12 GB.
- **s3:** 48 hours at the 20 cell/s budget is 14.156 GB; provision 32 GB per relay; optional paid archive.
- **o2:** Store nodes about 28 GB at 100 events/s of 2 KiB bodies; a 14-day anchor ring in contract state.
- **o3:** No events in ledger state; indexer about 52 MB/day; anchors only when requested; Lane B stores 24 hours.

**(b)** s2’s `10 × 1054.72 × 86400 × 7` and s3’s `20 × 172800 × 4096` both recompute to the gigabytes they print. o2’s 17.7 GB/day at 100 × 2 KiB, then 90% at 24 h and 10% at 7 d, also recomputes to about 28 GB. Dropping proofs after anchoring is their inference. The anchor ring is permanent contract state: the read-out’s no-rent claim is the constraint, and `bytesWritten` is 50,000 per block. o2’s “overwrites are churn” is an inference I did not re-prove. o3 is right that ordinary logs are not ledger state. The node’s applied-transaction event at `ledger/src/ledger_9/mod.rs:460-470` carries roots, addresses, and UTXO deltas, not contract log payloads. The indexer rebuilds logs by re-execution (`architecture.md:15-19`). Whether contract-event rows are pruned is still unknown.

**(c)** Vote **s3-red-team**. Bounded 48-hour relay storage, archives paid separately, ledger holds commitments and replay state only.

**(d)** The strongest objection is availability. Three signed receipts attribute a promise. They do not prove the bytes are still there, which s3 already calls an inference, and a partition longer than 48 hours deletes the message.

## D7. Infrastructure actors

**(a)**
- **s2:** Relays, gateways, and issuers; at least five organisations; validators do not relay.
- **s3:** A published launch roster, explicit trust, outbound quotas, exploratory connections; peer count is not decentralisation.
- **o2:** Unpaid relays; bonded stores and anchorers; treasury; phases L, O, and D with on-chain gates.
- **o3:** Foundation indexers plus self-hosting; Lane B relays later; wallet custody in phase 2.

**(b)** Mainnet config has `num_permissioned_candidates: 10` and `num_registered_candidates: 0` (`system-parameters-config.json:6-8`). Safe mode omits `send_mn_transaction` on purpose (`check_call_filter.rs:44-45`). Both support every proposal that says ledger enrolment can be paused by the permissioned set. Least Authority records issues A–D and says peer scoring is not a complete defence (`2020-leastauthority-gossipsub-audit`). The v1.1 spec’s outbound-mesh section is real. I did not re-open `2002-douceur-sybil` this round; s3’s paraphrase is the paper’s standard thesis, not a section I re-checked. Cao’s Appendix D is cited by o2 for operators splitting across keys; I confirmed the paper’s cluster analysis exists and did not re-read that appendix line by line. `Maintain` exists as a contract action in the upstream ledger (`structure.rs:2757` in the tree I opened). o2’s line 2987 was not that line. The DApp connector’s connected API, from `api.ts:70` onward, has balances, transactions, and signing, and no subscribe method.

**(c)** Vote **o2-economist-operator** for the actor split and the gates: validators unchanged, stores and anchorers bonded, payout only for work a contract can check, foundation share capped by a published measurement. Do not take the unpaid-relay rule. Relay payment stays s2’s contracted service pool until a slashable asset exists.

**(d)** The strongest objection to o2’s table as written is the unpaid relay. Filecoin and ETH relays forward because they already need the topic. A read-heavy event bus does not give a forwarder that reason, and bond-key splitting, which o2 cites, defeats a cap enforced per key.

## D8. Network tether

**(a)**
- **s2:** Separate libp2p GossipSub overlay, one topic, optional anchors; fallback is replicated gateways, not chain bulk.
- **s3:** Independent overlay for bulk, contracts for authorisation; clients must not flood-publish; ledger fallback is small announcements.
- **o2:** GossipSub sidecar plus a Registry contract; fallback is `Misc` or, on ledger 8, state writes.
- **o3:** Phase 1 is ledger and indexer only; phase 2 adds the sidecar; fallback if events are late is Lane B plus batch anchors.

**(b)** `midnight-node/Cargo.lock` contains `sc-network-gossip` 0.34.0 and does not contain `libp2p-gossipsub` or `libp2p-floodsub`. `service.rs` registers GRANDPA notifications (`:586`), BEEFY notifications (`:607`), BEEFY justifications (`:608`), and ledger sync (`:644`). `command.rs:327` selects `sc_network::NetworkWorker`. s2’s pins at `command.rs:326` and `service.rs:574` are a line early; `:574` is the GRANDPA protocol name, and `:610` is the ledger-sync comment. The claim “only consensus protocols and ledger sync are registered” is true of that region. Ledger sync on authorities is refused by default because snapshot CPU competes with authoring (`service.rs:614-625`). `service.rs:641` passes `default_peers_set_num_full` into the ledger-sync handler. That supports “this handler uses the default full set.” It does not say every new notification protocol must share GRANDPA’s peer slots; GRANDPA builds its own set. The read-out’s sidecar row matches what the lock file shows: an external process is not helped or blocked by the node. Coupling that process to the consensus swarm would be the fork.

`Cargo.toml:472-480` pins ledger 9.1.0.0-rc.5. The support matrix lists Compact toolchain 0.31.1 for mainnet (`support-matrix.json:38`). Compact 0.33’s notes introduce ledger 9 and events (`toolchain-0.33.0.md:22-26`). Activation on the deployed network is unknown, as s2, s3, and o3 say.

Flood-publish’s default is on. s3 is the only proposal that forbids clients from bypassing the ingress profile by flooding. s2 says to suppress author fields and cites scoring and outbound degree, not the flood-publish flag. A builder who implements “the spec they named” turns flood-publish on.

**(c)** None of the four names the crate constraint, the mesh profile, and the bootstrap rule together. The alternative is a hybrid sidecar: its own libp2p swarm, GossipSub v1.1 with the D5 profile, flood-publish off, bootstrappers at degree 0 (the spec’s operator note) and not the chain bootnodes, DHT candidates excluded from the outbound quota, validators not on the mesh. The ledger holds membership commitments and hash anchors. The indexer is how clients read anchors. If the phase-0 stop in D5 fails, the fallback is `Misc` anchors, not the bulk stream. s3 is the closest direction. s2’s gateway fallback is the right failure mode if the cryptographic framing must keep working without the chain. o3’s ledger-first phase is a different product: public logs, finality on the order of the 6 s slot plus whatever `mps-0028` sets, and a chain-wide block-usage budget of 1,000,000 bytes per slot.

**(d)** The strongest objection to the sidecar is o3’s: if ledger-9 events are actually live and the product accepts about one event per second and delivery on the order of a minute, the indexer lane ships with no second network. Building the mesh before that product choice is confirmed spends the first milestone on a network the application may not need.

## D9. Threats and open risks

**(a)**
- **s2:** Composition of the ratchet, the stamp, and the contract bridge is the leading risk; Cheval’s three forward-secrecy attacks must be reproduced.
- **s3:** Ranked list, with blocks on unanalysed global-observer claims, peer-count Sybil arguments, unchecked witnesses, silent fallback, and unbounded queues.
- **o2:** RLN slashing, GossipSub scoring, Dandelion, challenges; residual global observer and phase-L anchorer censorship.
- **o3:** Gap detection, two indexers, DUST price, GossipSub scoring on Lane B; first-contact omission is undetectable.

**(b)** Cheval’s abstract reports three forward-secrecy attacks and partial results for encrypted headers and PQXDH composition. I did not find the phrase “resource limitation.” The prover-guidance section says ProVerif cannot finish these proofs without guidance. s2’s “partial proof is not an attack” is a fair reading. It is their wording.

Heilman shows address-table poisoning that monopolises a Bitcoin node’s connections (`2015-heilman-eclipse` is the paper s3 cites; I confirmed the catalog note and did not re-walk §§3–6 this round). That supports “random peer fraction is the wrong eclipse model” as an analogy. It is not a GossipSub experiment. Loopix’s own adversary section is what s3 points at for “do not inherit the theorem”; I did not re-open that paper this round. The Dandelion++ scope sentence I did re-open, and it supports s3’s block on a global-observer claim built from a stem. CVE-2022-47547 is the scoring bug the ACL2s paper says was confirmed (`2023-kumar-gossipsub-acl2s`). None of the four gates the crate on a fix. o2’s “replay: none within the stated model” is stronger than a ±20 s window plus a cache. A store that skips the cache is outside the model by definition.

**(c)** Vote **s3-red-team**. The blocks match the papers that were checked: no strong global-observer claim from encryption, flooding, or Dandelion++; no “few percent of peer IDs” independence; no contract effect from an unchecked witness.

**(d)** The strongest objection is priority. Global timing is ranked third, and the defence named for it is a mix that phase 3 has not analysed. Until that profile exists, the mitigated risks a launch can actually test are eclipse, proof floods, and allowance exhaustion, which they rank lower.

## D10. Build and verification plan

**(a)**
- **s2:** Freeze and audit the cryptographic profile, then a bounded prototype, then a 10,000-subscriber simulation.
- **s3:** Model admission and replay first; simulate targeted 1%, 3%, and 5% adversaries; pilot; audit; mix only after that.
- **o2:** Measure the RLN proof, simulate the treasury, simulate 1,000 GossipSub nodes, model the Registry in Quint.
- **o3:** Measure publish cost and indexer fan-out, model the SDK cursor, then ship Lane A. An afternoon usability test is an acceptance gate.

**(b)** o2’s first gate is the right experiment if a Midnight proof is on the hot path: size and verify time, with an explicit retreat to off-chain Groth16. Revuelta’s method (analytic model, 1,000-node Shadow, multi-host) is a real method. It does not transfer to a stem plus a different prover. s3’s targeted fractions match Heilman’s point that a random fraction is the wrong test, provided the sim can place the adversary on the victim’s outbound edges. o3’s cursor invariants are testable and do not tell you whether a mesh delivers. The CVE paper says the developers confirmed CVE-2022-47547. A changelog check is a gate nobody listed.

**(c)** Vote the following alternative. Phase 0 has two measurements before any public relay. First, if anyone still wants a per-message Midnight proof, record its bytes and its single-core verify time; above 4 KiB or above 10 ms, it stays off the mesh. Second, run the D5 profile at 50, 200, and 1,000 relays, including s3’s targeted 1/3/5% placements and a DHT full of attacker identities that must not occupy `D_out`. Require a crate changelog that names a fix for CVE-2022-47547. If class-S p99 exceeds 6 s at N = 200, or honest delivery falls below 99%, stop and ship only `Misc` anchors. Do not design a replacement overlay in that same effort. A small model of the admission state machine (epoch, credit, nullifier, Ignore versus Reject) is worth checking. Re-proving GossipSub is not.

**(d)** The strongest objection is the 6 s kill line. It is a chosen threshold. A product owner who signs s3’s 35 s budget, or o3’s minute-scale indexer, would be right to call that stop a preference rather than a failed bus.

## Where the group will split

The three decisions most likely to stay in dispute are **D8**, **D4**, and **D5**. D8 is whether version 1 is the indexer (o3) or a sidecar (s2, s3, o2, and this review). D4 is whether admission is a public stamp (s2), a capped lease with no slash yet (s3), a NIGHT bond that is supposed to slash (o2), or a DUST transaction per event (o3). D5 is whether “fast” means under a second (o2, citing Waku), a few seconds (s2), half a minute (s3), or a minute on the chain (o3). D1 and D3 follow those three. D2’s refusal of global-observer anonymity, D7’s exclusion of validators, and the ban on DUST as a relay wage are not where the argument is.

The one fact that would settle the most of this is the **wire size and single-core verify time of one Midnight PLONK membership proof**, measured on the reference relay the way Revuelta’s Table 1 measured nwaku RLN. If that proof is small and fast, o2’s slashable membership can sit on the hot path and the stamp-versus-signature argument shrinks to economics. If it is a multi-kilobyte, multi-millisecond object, per-message Midnight proofs leave the mesh, D1’s admission area collapses to s2’s stamp or a cached signature, and D5 becomes a bandwidth and degree question rather than a proving question. Ledger-9 event activation would decide only whether o3’s phase 1 can start; it would not choose the admission mechanism or the mesh.
