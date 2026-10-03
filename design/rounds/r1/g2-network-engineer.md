I'll read the charter first, then the Midnight network evidence and the graph overview it requires.The charter sets the ten decisions and the evidence rules. Next I’ll read the Midnight stack note, the graph overview, and the Bitmessage starting documents.The stack note says GossipSub is absent and only Substrate gossip is wired for consensus. I’ll check that in the node code and pull the overlay papers the tether decision depends on.The event bus should be a separate libp2p swarm running GossipSub v1.1, with Midnight used only as the admission and anchor ledger. The Midnight node binary, as pinned today, cannot host that mesh: it has no GossipSub crate, its gossip engine is the consensus gadgets, and its peer slots and validator CPU budget are already spoken for. Payloads stay off the ledger. A relay-visible envelope carries a shard id, an admission nullifier and a sealed body; relays do not learn the recipient. The mesh is sized from the GossipSub evaluation profile (degree 8, heartbeat 1 s). Planning numbers, not measurements, put a dedicated relay at about 100 class-S messages per second aggregate before it spends half of a 50 Mbit/s link, and put end-to-end latency for a 4 KiB message on a 1,000-relay mesh on the order of a second. Strong anonymity against a global observer is out of scope: this design spends its budget on latency and bandwidth. The fallback, if the overlay cannot be operated, is ledger-9 `Misc` anchors read through the indexer, which is a different and much smaller bus.

Facts below are from the ledger-9 generation the node pins (`midnight-node` `887348f9`, ledger tag `ledger-9.1.0.0-rc.5`). The docs’ mainnet support matrix is an older generation, on which contract events are not yet available. Upstream Substrate defaults cited from the network-stack read-out are a nearby SDK, not the pinned `stable2609` fork.

## D1. Event format

Relays see an envelope. They do not see a recipient, a sender peer id, or a payload schema.

The swarm uses GossipSub’s StrictNoSign policy, as Waku relay specifies it: the pubsub `from`, `seqno`, `signature` and `key` fields are absent, not empty (`2020-vac-waku2-relay-spec`, Signature Policy). The pubsub topic is a 32-byte shard id. The GossipSub `data` field is the envelope.

Envelope version 1, fixed binary layout, big-endian:

| Field | Visible to relays | Size |
|---|---|---|
| `version` | yes | 1 |
| `shard` | yes | 32 |
| `msg_id` | yes | 32 |
| `created_unix_ms` | yes | 8 |
| `ttl_s` | yes | 4 |
| `epoch` | yes | 4 |
| `seq` | yes | 2 |
| `nullifier` | yes | 32 |
| `member_pk` | yes | 32 |
| `member_sig` | yes | 64 |
| `body` | opaque | class cap |

`msg_id` is SHA-256 over the canonical concatenation of `version`, `shard`, `epoch`, `seq`, `nullifier` and `body`, the same role as Waku’s deterministic message hash (`2020-vac-waku2-message-spec`, Deterministic message hashing). `member_sig` is an Ed25519 signature by `member_pk` over `msg_id`. The nullifier is `SHA-256(domain || member_pk || epoch || seq)`. A relay drops the message unless the id matches, the signature verifies, `seq` is inside the epoch budget, and the nullifier is new. Unknown `version` is GossipSub **Ignore**, so it does not trip the invalid-message penalty. A bad signature or a replay is **Reject** (`2020-gossipsub-v11-spec`, Extended Validators).

The body is ciphertext. The seal is an application concern: key-private IND-CCA public-key encryption, or a symmetric key distributed out of band (`2001-bellare-keyprivacy`; `2013-kohlweiss-anonymitypke`). Relays never trial-decrypt. Inside the seal, a `u16` schema id distinguishes agent events, wallet hints and anchor pointers. Coin data does not travel here. Wallet coin sync already has a path.

Three size classes:

- **S.** Body ≤ 4,096 bytes. Full-message mesh.
- **M.** Body ≤ 65,536 bytes. Full-message mesh, counted as sixteen class-S credits.
- **L.** Body ≤ 262,144 bytes (Bitmessage’s `MAX_OBJECT_PAYLOAD_SIZE` of `2**18`, from the protocol guide). The mesh carries only a class-S announcement: content hash and length. The body moves on a separate request-response protocol.

The 4 KiB and 64 KiB cuts are design choices. The 256 KiB cap matches both Bitmessage and the patched Yamux rule that the first frame of a stream must be at most `DEFAULT_CREDIT` = 256 KiB (`rust-yamux` `yamux/src/lib.rs:45`, `yamux/src/connection.rs:626`). Mesh messages are also split by Yamux’s 16 KiB send size (`yamux/src/lib.rs:68`). A 1 MiB mesh message is refused. Farooq’s own estimate for 1 MiB on a degree-8 mesh of 1,000 peers is already in the multi-second range, and cold TCP windows make the first copies slower (`2025-farooq-staggering`).

Time to live. Class S and M: `ttl_s` ≤ 86,400. Class L: ≤ 604,800. The mesh cache is only long enough to satisfy gossip retries, on the order of seconds (`2019-vyzovitis-gossipsub-v01`, gossip of ids seen in the last few seconds). Relay memory keeps bodies for 10 minutes. That 10-minute figure is a design choice. Optional store nodes keep a shard for 24 hours, or 7 days if the publisher also posted a chain anchor. This is not Bitmessage’s two-day global retention (`2012-warren-bitmessage-whitepaper`).

Open shards may also carry a 32-byte content topic in the clear, so a subscriber can filter without trial decryption. Private shards must not. Mixing the two in one shard would tag private traffic with clear topics.

On-chain anchors, when used, are Compact `emit` of a standard event. The only custom-data event is `Misc` (`name` 32 bytes, `payload` 256 bytes). Ledger 9 silently drops a log whose data exceeds `MAX_LOG_EMITTED` = 1 KiB, while the VM accepts a log argument up to `MAX_LOG_SIZE` = 512 KiB (`L9:onchain-vm/src/vm.rs`, constants verified on tag `ledger-9.1.0.0-rc.5`). An anchor is a hash, a shard id and a short commitment. It is not the body.

## D2. Definition of private

Vocabulary follows Pfitzmann (`2010-pfitzmann-terminology`): anonymity is non-identifiability inside a set; unlinkability is the inability to decide that two items are related; unobservability requires both, plus indistinguishability from noise. This bus does not claim unobservability.

| Property | One mesh neighbour | Colluding minority of relays | Global passive observer | Chain observer | Indexer operator |
|---|---|---|---|---|---|
| Content confidentiality | Holds, if the seal is key-private IND-CCA and the relay lacks the key | Same | Same for overlay bytes | Holds for overlay bodies. Fails for anything in `emit` or ledger state | Same as the chain for anchors. No overlay bytes |
| Publisher unlinkability to an IP | Holds against neighbours who are not the chosen stem peer. Fails against that stem peer | Partial. Outbound stem-then-fluff only. Not a Dandelion++ bound | Fails. Timing recovers topology (`2016-neudecker-timing`) and a first-spy estimator works on a fluff flood (`2017-fanti-anonymitybitcoin`) | The overlay publish is not a transaction. An anchor has no Substrate signer. `v_fee` is public; the payer is not | Sees the anchor transaction, not the publisher’s IP, unless the publisher submitted through that operator |
| Subscriber-interest privacy | Fails for the shard. GossipSub `SubOpts` send the topic id to direct peers (`2020-vac-waku2-relay-spec`, SubOpts) | Fails for shards they sit in | Fails | No overlay interest. An anchor is public | `contractEvents` requires a contract address, so the operator learns that filter |
| Topic privacy | Shard id is visible. A human name is not, if ids are hashes. Open content topics are visible | Same | Same | Anchor `name` is public | Same |
| Timing and volume | Fails | Fails | Fails | Block time is 6 s (`midnight-node/runtime/src/lib.rs:292`) | Same as the chain |
| Relationship privacy | The seal hides who the body is for. Same-shard membership is not a pairwise relationship. No acknowledgements on the mesh | Long-term intersection still works (`2014-oya-dummies`) | Fails | Two anchors can be correlated by time | Two clients that filter the same contract are linkable by the operator |

Waku relay lists publisher-message unlinkability and subscriber-topic unlinkability as goals, and then defines an adversary who does not see the global graph and who does learn subscriptions of direct peers (`2020-vac-waku2-relay-spec`, Adversarial Model). Those goals are not properties of the wire format. This design does not adopt them as claims.

The anonymity trilemma is the reason. Against a global passive adversary, strong anonymity is impossible when `2βℓ` is negligibly below 1, even if every party is honest (`2017-das-trilemma`, the synchronised-user bound). Here the latency overhead `ℓ` is a handful of gossip rounds and the cover fraction `β` is about 0. The design chooses low latency and a bounded mesh degree. It therefore refuses strong sender or recipient anonymity against that adversary. Guerraoui’s bound points the same way: any gossip protocol has differential-privacy ε at least `ln(f−1)` against `f` curious nodes, and no finite ε if those nodes can cut the graph (`2023-guerraoui-inherent-anonymity-gossiping`, Theorem 5).

Out of scope for version 1: global-observer anonymity, cover traffic, mixnet latency, traffic-analysis resistance, forward secrecy, post-compromise security, and hiding that a shard exists. A static recipient key recorded today is readable later by whoever later holds that key (`2015-mosca-quantum-ready` states the record-now problem; the Bitmessage review records the same static-key failure). Pairwise sessions can add a ratchet in a later phase. The bus default stays sealed envelopes without a ratchet. Version 1 also sends no delivery receipts. Receipts are a metadata channel (`2024-gegenhuber-careless-whisper`).

A private-shard subscriber who will not reveal a content topic downloads the shard and recognises locally. That is the trivial single-server PIR result: perfect privacy against one holder of the database costs a full download (`1998-chor-pir`). Sublinear PIR and oblivious message retrieval are not in this version.

## D3. Publish and subscribe

A **shard** is the GossipSub mesh topic. A **content topic** is an application tag. Meshes are per shard, never per content topic. A relay joins at most eight shards. Eight times the mesh high-water mark of 12 is 96 full-message links, which is already more peering than a consensus node should share with block and finality traffic.

Open shards put the content topic in the header. Private shards leave recognition to the seal. Shard ids for open feeds are published as chain data (a public ledger field or a `Misc` name). Private shard ids are distributed out of band. There is no global directory of subscribers.

Publish path. The publisher sends the envelope to one **outbound** peer (the stem), chosen from peers it dialed. That peer validates admission and then publishes into the shard mesh (the fluff). Flood-publish is off on private shards and on for open shards. The spec’s default is flood-publish on (`2020-gossipsub-v11-spec`, parameter table). Turning it off on private shards is a deliberate departure: flooding the source to every peer above the publish threshold hands the origin to every neighbour, which is the estimator Fanti analyses (`2017-fanti-anonymitybitcoin`). Censorship resistance on a private shard comes from having several honest outbound peers, not from showing the source to all of them.

This one-hop stem is not Dandelion++. Dandelion++ uses an approximately 4-regular anonymity graph, fresh relays per epoch on the order of ten minutes, and a formal bound against a spy fraction that may drop and inject (`2018-fanti-dandelionpp`). One hop only hides the source from peers other than the stem. If that stem is adversarial, the source is known. Full Dandelion++ is a later phase, and only if measurement shows the one hop is the dominant leak. It adds path length before the mesh clock even starts, so it needs its own latency budget.

Subscribe path.

- A desktop agent that can pay the shard bandwidth joins the mesh.
- A desktop agent that must hide which content topic it wants, inside a private shard, pulls the whole shard from two relays and filters locally.
- A light filter pushed to a relay (“send me only these topics”) is a supported debugging mode and a privacy downgrade. Bloom filters given to an untrusted peer leak the interest (`2014-gervais-bloomfilters`). Waku’s own threat note is that a peer in the topic learns the subscription (`2024-vac-adversarial-models`).

Delivery is at-least-once. Consumers deduplicate on `msg_id`. There is no total order and no causal order on the overlay. Per-publisher order is `epoch` plus `seq` inside one membership. Consumers who need a total order use chain-anchor order from the indexer’s monotonic id. Replay inside the TTL is rejected by the nullifier cache. Backfill is “give me the shard between two times,” served by a store, not a per-recipient mailbox. A mailbox index would tell the store who wants which body.

Smart contracts do not subscribe. No on-chain event read exists, and `emit` results are not ledger state. A contract consumes an event only when some off-chain relayer submits a later transaction whose public inputs are the hash, the nullifier, or whatever the circuit discloses. Wallets do not have to change. Shielded sync stays on `zswapLedgerEvents` with local trial decryption. A wallet joins this overlay only as an explicit desktop subscription. Mobile wallets stay on the indexer.

## D4. Sustainable model

Publishers pay. Relays, in version 1, are not paid by the protocol. That is a hole, and it is acceptable at launch because the mesh does not need thousands of anonymous relays to function. It needs a diverse operator set.

Admission is a Midnight membership, not proof of work and not a rate-limiting nullifier with slashing.

Flat proof of work prices honest weak senders and botnet senders the same (`2004-laurie-proofofwork`). Bitmessage’s own reviewed analysis reaches the same economic conclusion (`2015-schaub-bitmessage-antispam`). Waku’s RLN construction is the right shape: one signal per external nullifier per epoch, membership in a Merkle tree, and a double-signal that reveals a key and slashes a deposit (`2022-taheri-waku-rln-relay`). Midnight cannot slash. DUST fees are burned; the read-out finds no credit of `v_fee` to a validator or a treasury. DUST is shielded and non-transferable. Block-reward withdrawal is stranded in the problem statement of MPS-0019, and NIGHT staking is still a draft MIP. Until a seizable asset exists, RLN’s financial punishment has nothing to seize. What Midnight already has is the documented pattern: a historic Merkle tree of commitments and a nullifier set, checked in a circuit. Scope the nullifier by epoch and the same pattern is a rate cap.

Concrete cap, design choice. One membership covers one epoch of 600 blocks, which is one hour at the 6 s slot (`runtime/src/lib.rs:292`). The transaction pool already uses a 600-block longevity. A membership may publish at most `K_s` = 60 class-S credits in that hour. Class M costs 16 credits. Class L announcements cost 1 credit; the body is not extra credits, but stores may refuse an unanchored body. Relays enforce the cap. Over-cap messages are Reject.

Cost at genesis parameters, inference, not a live quote. The read-out’s worked example at factor 1 and overall price 10 is 0.01 DUST per KB of block usage. A membership transaction includes a DUST spend proof of 2,912 bytes and a call proof the ledger estimates at 4,832 bytes, so a lower bound near 8 KB is about 0.08 DUST if block usage dominates. One NIGHT generates at most 5 DUST, filling over about a week. A full tank buys on the order of 60 membership-hours. Spent as a burst, 60 memberships times 60 messages is a few thousand class-S messages and then a dry week. Spent smoothly, it is on the order of twenty messages an hour per NIGHT. Live prices are not in the repos. They move by up to about 4.6% per block when a dimension is full, so a crowded chain makes the next membership more expensive by itself. The overlay cap `K_s` does not move with price.

Relay incentives. No on-chain payment to an indexer, an RPC operator, or a relay was found. Version 1 does not invent one. Operators are the same parties who already run wallet backends and application relays, plus anyone who chooses to run a sidecar. High load is handled by splitting shards and by the DUST price of new memberships, not by paying relays more. Low load does not collapse the mesh: GossipSub maintains degree with whatever honest peers exist, and bootstrappers are configured with degree 0 so they only hand out peer records (`2020-gossipsub-v11-spec`, Recommendations for Network Operators).

Per-peer token bucket before signature checks: 20 messages per second per peer. That stops one neighbour filling the relay’s budget. The figure is a design choice.

## D5. Performance requirements

These are acceptance targets plus the arithmetic a builder can recompute. They are not measurements of a Midnight network. Link assumptions are taken from Farooq’s shadow configuration: 100 ms edge latency and 50 Mbit/s, labelled as planning assumptions (`2025-farooq-staggering`).

Mesh profile, taken from the GossipSub evaluation and the v1.1 spec, not retuned:

- Target degree `D` = 8, low 6, high 12. Heartbeat 1 s (`2020-vyzovitis-gossipsub`, the setting used in that evaluation).
- Gossip factor 0.25, prune backoff 1 minute, flood-publish as in D3 (`2020-gossipsub-v11-spec`).
- Outbound mesh quota `D_out` = 4. The spec requires `D_out` < `D_low` and at most `D/2`, and its only numeric example is 2 when `D` is 6. For `D` = 8 the legal range is 1 to 4. The choice 4 is the top of that range, because an eclipse succeeds by owning every outbound connection (`2015-heilman-eclipse`). If scoring becomes unstable, drop to 2 before touching `D`.

Hop count uses Farooq’s formula `H = ceil(log N / log D)` and `L ≈ (τ_p + τ_tx) · H`. Transmit time is `8 · bytes / 50e6` seconds.

| Relays N | H at D=8 | Body | Transmit | Theoretical L at 100 ms |
|---:|---:|---:|---:|---:|
| 200 | 3 | 4 KiB | 0.66 ms | 0.30 s |
| 1,000 | 4 | 4 KiB | 0.66 ms | 0.40 s |
| 200 | 3 | 64 KiB | 10.5 ms | 0.33 s |
| 1,000 | 4 | 64 KiB | 10.5 ms | 0.44 s |

One stem hop adds about one `τ_p`, so about 0.1 s, before this clock starts. The paper prints 5,520 ms for a 1 MiB message at N=1,000, D=8, 100 ms, 50 Mbit/s. Recomputing `(0.100 + 8·10^6/50·10^6)·4` gives about 1.04 s. The printed 5,520 ms is therefore not used as a checked input. Either figure, plus the cold-window penalty the same paper reports, keeps 1 MiB off the mesh.

The evaluation’s own attack runs are evidence that this profile can be fast, not a substitute for our measurement. With scoring, opportunistic graft and gossip factor 0.25, a cold-boot Sybil case in that paper still delivered every message, with some delays up to 1.2 s and a reported p99 of 205 ms on that figure; raising the gossip factor to 0.4 shortened the tail they plotted (`2020-vyzovitis-gossipsub`). Their Filecoin and ETH2.0 deadline was 6 s. Ours is tighter, and it is a target.

**Node classes and budgets**

| Class | Role on the overlay | Budget |
|---|---|---|
| Chain validator | Does not run it | 0 event bytes, 0 event CPU |
| Event relay | Meshes up to 8 shards, degree 8 | Planning link 50 Mbit/s. Half reserved. Event egress cap 3.0·10^6 bytes/s |
| Desktop agent | Mesh member of one shard, or full-shard pull | Same per-shard cost as one relay’s ingress for that shard |
| Mobile wallet | Not on the overlay in v1 | Indexer only |
| Store | Disk for one or more shards | Not on the hot mesh path |

Pessimistic amplification, without assuming IDONTWANT savings: a node holding a new message pushes it to every mesh neighbour except the sender. At the target degree that multiplier is `m` = 7. At the high-water mark it is 11. Capacity planning uses 7. Farooq reports that IDONTWANT cuts bandwidth in proportion to message size and barely cuts latency. Until the chosen crate implements it, the SLO uses `m` = 7 with no credit for the saving.

Egress is `m · λ · S`.

- One shard, 10 messages/s, 4 KiB, `m` = 7: 286,720 bytes/s, about 23.1 GiB/day.
- Eight shards at that rate: 2.29·10^6 bytes/s, about 18.4 Mbit/s, under the 3.0·10^6 byte/s cap.
- Aggregate cap at `m` = 7 and 4 KiB: `λ` ≈ 104 class-S messages/s per relay, across all of its shards.
- One class-M message/s on one shard: about 4.6·10^5 bytes/s. A relay that carries class M must spend credits, not add it free on top of a full class-S load.

Fan-out. Every mesh member of a shard receives every message. Concurrent mesh subscribers scale with the number of relays in the shard, not with a broker’s socket table. Light clients are different. Serving 200 clients a full copy of a 10 message/s, 4 KiB shard is 200 · 40 KiB/s = 8·10^6 bytes/s, which exceeds the relay cap. So a relay does not fan the shard out to a crowd of pullers. Pull is limited to a small count per relay. The design cap is 8 simultaneous full-shard pulls. That cap is a design choice. Past it, the client joins the mesh or uses a store.

CPU. Ed25519 verification at 104/s is noise next to the link. A per-message Midnight proof is not. Genesis verification is about 3.27 ms plus a per-input term, and a call proof is estimated at 4,832 bytes. At 100 messages/s that is a third of a core before amplification, and the proofs dominate the byte budget. Admission proofs are verified when a membership is accepted and then cached for the epoch. Per message, the relay checks a signature and a nullifier.

Latency SLOs, to be measured before mainnet, not claimed as already met:

- Class S, N ≤ 1,000, no attack: p50 ≤ 1 s, p99 ≤ 2 s.
- Class M, N ≤ 200: p99 ≤ 3 s.
- Class L: announcement meets the class-S SLO; body fetch from at least three peers who store the hash, p99 ≤ 5 s.
- Under a 20% Sybil cold start: delivery ≥ 99%, p99 ≤ 6 s. If the 2 s target fails and the 6 s target holds, the first knob is gossip factor 0.4, which the evaluation already tried.

Chain comparison, so the overlay is not sized against a fantasy. Block usage limit is 1,000,000 bytes per 6 s slot, about 1.7·10^5 bytes/s for the entire chain. An 8 KB transaction at that cap is on the order of twenty transactions a second if the block were nothing but those transactions. Finality is documented at about three blocks, about 18 s, and the indexer serves finalized blocks only. The overlay exists because those two numbers cannot carry this bus.

## D6. Storage requirements

Hot state is small. Durable state is opt-in. Ledger state is not the log.

A relay’s body cache is 10 minutes. At 10 messages/s, 4 KiB, 8 shards: `10 · 4096 · 600 · 8` ≈ 188 MiB. A 24-hour seen-id table at 32 bytes per id for the same load is about 211 MiB. Both are design points tied to the TTL in D1.

A store that keeps those eight shards for 24 hours holds `10 · 4096 · 86400 · 8` ≈ 26.4 GiB, plus class-L bodies. Design cap for a store: 100 GiB, then drop the oldest object that has no chain anchor. Availability of an unanchored body is “some honest cache or store still has it.” That is hours, not consensus availability. After the last copy expires, the message is gone. Publishers who need a durable receipt anchor a hash on chain and keep the body in a store they operate.

The ledger stores membership roots and optional anchors. It does not store bodies. Persistent contract bytes are paid once, are not rented, and are not pruned; the write budget is 50,000 net bytes per block. Logs are churn, which is the cheap dimension, and they are dropped by the node after verification. The indexer reconstructs them by re-execution. Indexer ledger-state retention of 1,000 blocks is not a proven retention rule for contract-event rows. Whether those rows are pruned is **unknown**. Treat anchors as public durable data until an indexer GC policy is measured.

Full nodes and validators store none of this. Substrate pruning (256 blocks by default for a non-archive node) is unrelated to the overlay cache.

## D7. Infrastructure actors

| Actor | Admission | Trusted with | Paid by |
|---|---|---|---|
| Validator (10 permissioned seats at mainnet genesis) | Cardano-side registration and the D-parameter, later | Consensus only. Must not run the event mesh | Not by this protocol. Block rewards are not load-bearing yet |
| Midnight full node, RPC node | Anyone who syncs | Chain data. Event sidecar off by default | Their operator |
| Event bootstrapper | Published list, at least four, distinct networks. Degree 0, peer exchange only, signed peer records | The first introduction. Not trusted with payloads | The operator who publishes the list |
| Event relay | Open after phase 1. Kept in the mesh by score, not by stake | Liveness of the shards it serves. Not trusted to forget metadata or to stay honest | Not in v1 |
| Store | Open. Announces retention | Availability inside its advertised window. Sees shard bytes, not seal plaintext | The operator. A publisher who needs 7-day class L can run their own |
| Indexer | Unchanged | Chain queries. Learns `contractEvents` filters. Not on the overlay path | Unchanged. No on-chain indexer fee exists |
| Wallet provider | Unchanged | If the wallet dials only that provider, the provider sees the wallet IP and its shard subscriptions | Unchanged |
| Agent | A membership if it publishes | Its own keys | DUST for membership and for any anchor |
| Proof server | Unchanged | Witnesses it is given for membership transactions | Unchanged |

Bootstrappers are not the four Midnight DNS bootnodes. Coupling the two peer sets would let one eclipse or one seizure hit consensus and events together, and it would tie event peer ids to chain peer ids. A governance transaction may commit the hash of the bootstrap list so a substituted list is detectable. The list itself stays off chain. mDNS is off on this swarm. Private-address dialing is off except in a dev profile. The chain node already documents `--no-private-ip` for operators; the sidecar copies that posture.

Path. Phase 0 is a lab mesh run by one operator. Phase 1 is four bootstrappers and open peer exchange, still no token. Phase 2 lets any scored peer relay. Phase 3 pays relays only if a real payment path exists. The bus ships at phase 1. Waiting for phase 3 repeats the stranded-reward problem.

A wallet that wants publisher unlinkability dials at least two outbound relays itself. A wallet that uses only its provider as stem has delegated the stem to that provider. That is an honest trust point, not a hidden one.

## D8. Network tether

**Choice: a hybrid sidecar.** Bulk events ride a new libp2p swarm. The ledger anchors membership and, when a contract must see that something happened, a hash. The indexer is how clients read those anchors. It is not the bus.

**Fallback:** ledger-9 `Misc` anchors plus `contractEvents`, and no overlay. That fallback is a low-rate public commitment channel. It becomes the product only if the overlay fails the phase-0 tests in D10.

What the node can host without a fork: an external process. Nothing inside the consensus swarm.

Checked in the tree:

- `midnight-node/Cargo.lock` contains `sc-network-gossip` 0.34.0 (line 14548) and does not contain `libp2p-gossipsub` or `libp2p-floodsub`.
- The node registers three Midnight-added protocols: GRANDPA notifications, BEEFY notifications, BEEFY justifications request-response, and `midnight-ledger-sync/2` (`midnight-node/node/src/service.rs:586-644`). Everything else comes from `build_network`. There is no application pub/sub.
- `sc-network-gossip` is a dependency of the GRANDPA and BEEFY crates, not a general bus. The read-out describes its topics as 32-byte tags decided by a per-protocol validator. That matches a consensus gadget. It does not match a multi-shard event mesh with peer scoring, graft, prune, and peer exchange.
- Ledger-sync serving is refused on validators by default because snapshot CPU must not compete with authoring and finality (`service.rs:614-625`). Event validation on that same process is the same mistake.
- The ledger-sync handler is dimensioned with `default_peers_set_num_full` (`service.rs:641`). Event peers would share that set. The read-out’s upstream defaults are 8 outbound and 32 inbound full peers. Those numbers are from a nearby SDK, not re-verified on the pinned fork. They are small next to eight shards at degree 12 even if the pinned fork raises them.
- QUIC is not on the node’s libp2p feature list, by the same upstream read-out. The sidecar is a different binary and may use TCP and QUIC. Noise and Yamux on TCP. The node’s patched Yamux stays on the node.

Putting the mesh in-process would also repeat a measured validator leak. Heimbach mapped more than 15% of Ethereum validators to peer IPs by watching attestation gossip (`2024-heimbach-deanon`). Midnight’s author set is smaller and, while Aura is the producer, the slot leader is a deterministic round-robin. Event gossip on that peer set would hand an observer both graphs at once.

Discovery. Bootstrappers with degree 0 and signed peer records, as the v1.1 spec tells operators to deploy. Kademlia may supply candidates. It must not supply the outbound quota. Kademlia peer tables have been eclipsed with cheap identities on Ethereum and on IPFS (`2018-marcus-ethereumeclipse`, `2019-henningsen-falsefriends`, `2022-prunster-ipfseclipse`, `2026-shi-ethereum-eclipse`). A single DNS seeder is enough of a lever that the Ethereum work poisoned the official DNS list; this overlay does not create that lever.

What changes in existing software: nothing in the node, the indexer, the wallet, or the Compact compiler. A new contract uses the existing Merkle-membership pattern. A new sidecar binary links a libp2p that actually ships GossipSub. It does not link the node’s libp2p, and it does not require operators to replace `midnight-node`.

Rejected:

- **Consensus-swarm protocol.** No GossipSub in the lock, shared peers, validator CPU, and a mandatory binary upgrade before a single event can cross the network.
- **Ledger and indexer alone.** Public 256-byte payloads, a finality floor around 18 s, a chain-wide budget of order 10^5 bytes/s, and no contract subscription.
- **A Bitmessage-style global flood.** The guide’s illustrative 2 KiB objects at 1,000 per minute are already about 2.75 GiB/day per node before amplification, inventory, or duplicates. A mesh multiplier of 7 makes a global flood worse, and the flood still fails the trilemma.
- **A mixnet as the default tether.** Loopix-style delay is how low-latency systems buy strong anonymity. It misses the latency SLO on purpose. A mix hop may later wrap the stem for publishers who ask for it. It is not the mesh.
- **A new topic overlay** (PolderCast rings and the topic-connected constructions in the corpus). GossipSub already has a spec, a large testbed, a third-party audit (`2020-leastauthority-gossipsub-audit`), and a machine-checked model that found a real bug (`2023-kumar-gossipsub-acl2s`, CVE-2022-47547). Inventing a mesh would throw that away.

I would move the sidecar in-process only if a future node shipped GossipSub on its **own** peer set, disabled on authorities, with a connection budget separate from GRANDPA, BEEFY and transactions, and operators accepted the upgrade. I would abandon the mesh as the privacy story if the product required strong anonymity against a global observer. The replacement would be a mix or a PIR mailbox, and the latency SLO would have to be rewritten first.

## D9. Threats and open risks

| Attack | Defence in this design | Residual |
|---|---|---|
| Eclipse of a relay | Separate swarm; `D_out` = 4 from outbound dials only; IP-colocation penalty P6; bootstrappers not in the mesh; DHT excluded from the outbound quota | A patient AS-level adversary who sits on most honest paths. Encrypted transport does not fix that (`2026-ndolo-bitcoinv2transport` on length and eclipse under Bitcoin’s encrypted transport) |
| Eclipse of a Midnight full node | Does not eclipse the event view, and the reverse is also true, because the peer tables differ | An operator who runs both under one name and one /24 still concentrates fate. Operational rule, not a protocol proof |
| Sybil relays | v1.1 scoring, opportunistic graft, prune backoff. Publish still requires a paid membership | Relay identities are cheap until phase 3 (`2002-douceur-sybil`). Scoring weights are application-specific and the spec’s tuning section is still marked TBD |
| Cold-boot and covert flash | Refuse public publish until an honest bootstrap set has been serving for at least 10 minutes. The evaluation recovered a poisoned mesh in about 90 heartbeats, roughly 1.5 min, and plain GossipSub without the v1.1 defences lost messages | A sustained majority of Sybil mesh links still censors. Scoring raises the cost. It does not create honest peers |
| Spam | Epoch cap, DUST membership, per-peer bucket, Reject drives P4 graylisting | A large NIGHT holder can burst until the tank is empty. Relays that skip checks are faulty peers; honest relays graylist whoever forwards invalid messages to them |
| Score manipulation (CVE-2022-47547) | Pin a crate whose changelog records the fix found by the ACL2s work | **Unknown** until that changelog is checked. Phase 0 blocks on it |
| Deanonymization of publishers | StrictNoSign, one outbound stem hop, no receipts, validators off the mesh | The stem peer, a global observer, and long-term intersection. One hop is a weak stem |
| Deanonymization of subscribers | Private shards have no clear content topic. Local filtering | Shard membership is visible to neighbours. A global observer sees it all |
| Replay | `msg_id` and nullifier cache for the TTL. Chain intents have their own TTL replay set | A store that ignores the cache is a faulty store. Clients still deduplicate |
| Censorship by one relay | Publisher has four outbound choices; open shards also flood-publish | An AS can drop the swarm (`2024-vac-adversarial-models`). Governance safe mode can pause chain anchors and `send_mn_transaction`. The overlay keeps moving |
| Key compromise | Epoch memberships expire hourly. Losing a key exposes future publishes under that key | Version 1 has no forward secrecy and no post-compromise healing (`2016-cohngordon-pcs`) |
| Indexer abuse | Indexer is off the payload path. No viewing keys are sent for this protocol | Anchor queries still reveal which contract a client watches |
| Large-message DoS | Class caps. Ignore is not Reject for unknown versions | Without IDONTWANT, duplicates cost `m` = 7. The cap is what keeps that affordable |
| Malicious bootstrap list | Signed records, multi-operator list, optional on-chain hash of the list | The first connection is only as honest as the list the user got |

Audit residue worth naming. Least Authority’s review of GossipSub v1.1 concluded the v1.1 changes help and that peer scoring is not a complete defence; they also showed ways to inflate or depress scores, and they asked for more simulation before parameters are frozen (`2020-leastauthority-gossipsub-audit`). This design inherits that homework. It does not claim the audit closed the protocol.

## D10. Build and verification plan

Phase 0, before any public relay. Simulate the mesh at 50, 200 and 1,000 relays with the D5 profile. Tooling is whatever the team already runs; Farooq used shadow, the GossipSub authors used a container testbed. Acceptance:

- Class S, no attack, N=1,000: p99 ≤ 2 s, no loss.
- Twenty percent Sybil, cold start, honest peers joining into a Sybil-heavy graph: delivery ≥ 99%, p99 ≤ 6 s.
- If p99 is between 2 s and 6 s, rerun with gossip factor 0.4 before changing the overlay.
- If delivery falls below 99%, or class-S p99 exceeds 6 s at N=200, stop. The product is the anchor fallback. Do not design a replacement mesh in that same effort.
- Admission tests: over-cap and bad signatures are Reject; unknown versions are Ignore; replays do not multiply egress.
- The crate changelog names a fix for CVE-2022-47547. If it does not, stop.
- A test that fills the DHT with attacker ids still leaves `D_out` occupied by dialed, non-DHT peers.

Formal work. Do not re-prove GossipSub. The ACL2s model is the scoring spec of record (`2023-kumar-gossipsub-acl2s`). The piece worth a small model is the admission state machine: epoch boundary, credit cap, nullifier uniqueness, Ignore versus Reject. A failed invariant there is a spam or penalty bug, and it is small enough to check before the sidecar is feature-complete.

Phase 1. Sidecar on a test chain, four bootstrappers, one membership contract, agents publishing and subscribing. No wallet release. Measure p99 and bytes on the real binary. A validator’s tcpdump on the consensus port shows no event protocol. Stopping every event relay does not move GRANDPA off its ordinary finality behaviour. A relay at eight shards and 10 class-S messages/s per shard stays under 3.0·10^6 bytes/s egress.

Phase 2. Desktop agent library, store protocol, private shards, and only then a Dandelion++ stem if phase-1 traces show the one-hop stem is the main publisher leak. Contract anchors demonstrated on ledger 9: a 256-byte `Misc` visible through the indexer, overlay body not visible there.

Phase 3. Only after phase 1 meets the SLOs: a membership proof small enough and fast enough to replace the per-message signature (target, design choice: under 200 bytes and under 1 ms to verify, or it stays off the hot path), an optional mix-wrapped stem, and relay payment if a seizable fee path exists.

Evidence that changes the design:

- A product requirement for strong anonymity against a global observer. D8’s privacy claims would be withdrawn and the tether reopened.
- A node release that hosts GossipSub on a separate, authority-off peer set. The sidecar can move in-process.
- Live DUST prices that make one class-S message cost more than the application will bear, measured from `Block.ledgerParameters`, not from the genesis inference. Raise `K` only together with a higher membership fee, so the weekly NIGHT budget in messages stays on the order of a few thousand.
- A simulation in which `D_out` = 4 collapses scoring. Drop to 2.
- Confirmation that contract-event rows are pruned on a short horizon. Anchors would need an explicit durability plan before anyone treats them as receipts.

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Event format | StrictNoSign envelope: 32-byte shard, Ed25519 admission, nullifier, sealed body. Classes 4 KiB, 64 KiB, and 256 KiB announce-only. Anchors are `Misc` hashes | Clear sender ids; per-message Midnight proofs; 1 MiB mesh messages; Bitmessage global object header | `2020-vac-waku2-relay-spec`; `2020-vac-waku2-message-spec`; `2020-gossipsub-v11-spec`; `L9:onchain-vm/src/vm.rs` `MAX_LOG_EMITTED`; Yamux `connection.rs:626` | Medium | A measured proof under 200 bytes and 1 ms, or a product need for relay-visible topics inside private shards |
| D2 Private | Content confidentiality against relays. No claim of unobservability, subscriber unlinkability, or global-observer anonymity. No receipts, no forward secrecy in v1 | Waku’s stated unlinkability goals treated as theorems; cover traffic; “Bitmessage is untraceable” | `2017-das-trilemma`; `2023-guerraoui-inherent-anonymity-gossiping` Thm 5; `2010-pfitzmann-terminology`; `2017-fanti-anonymitybitcoin`; `2016-neudecker-timing` | High on the refusals. Medium on the one-hop stem | An explicit requirement for strong global anonymity, which forces a different tether and different SLOs |
| D3 Pub/sub | Mesh per shard, ≤8 shards. Open topics in the header; private topics only inside the seal. At-least-once, dedup by `msg_id`. Contracts only via a later transaction | Per-topic meshes; Bloom push to a peer; on-chain subscription; total order on the overlay | `2020-vac-waku2-relay-spec` SubOpts; `2014-gervais-bloomfilters`; indexer `contractEvents` requires an address; no contract event-read in the node | Medium | Users refuse whole-shard download and accept the filter leak. Then a filter mode can be the default for open shards only |
| D4 Sustainable model | DUST-paid hourly membership, 60 class-S credits, relays unpaid in v1, no slash | Flat PoW; RLN slash; a new relay fee market | `2004-laurie-proofofwork`; `2022-taheri-waku-rln-relay`; burned `v_fee` and non-transferable DUST in the network-stack read-out; genesis price inference 0.01 DUST/KB | Medium | A seizable stake ships, or live prices make the membership useless. Then adopt RLN-style slashing or retune `K` against measured prices |
| D5 Performance | D=8, D_low=6, D_high=12, D_out=4, gossip factor 0.25, heartbeat 1 s. Relay cap ~104 class-S msg/s at m=7. SLO p99 ≤ 2 s class S at N=1,000. Validators at 0 | Untuned degree; 1 MiB full-message mesh; sizing from chain throughput | `2020-vyzovitis-gossipsub`; `2020-gossipsub-v11-spec`; `2025-farooq-staggering` formula. Link 100 ms / 50 Mbit/s is that paper’s sim setup, not a Midnight measurement | Medium | Phase-0 p99 misses 6 s at N=200, or `D_out`=4 breaks scoring. First knobs: gossip factor 0.4, then D_out=2 |
| D6 Storage | 10 min relay cache, 24 h optional store, 7 days only if anchored. No bodies in contract state. ~188 MiB hot for the worked load; ~26 GiB per store-day for eight busy shards | Two-day full replication; payloads in ledger state | Bitmessage 2-day TTL (`2012-warren-bitmessage-whitepaper`); 50,000 write-byte block budget; node discards events; `MAX_LOG_EMITTED` | Medium | Indexer event rows turn out to be short-lived. Anchors then need a durability design before they count as receipts |
| D7 Actors | Validators excluded. New relay and bootstrapper roles. Indexer unchanged. Wallets unchanged unless they opt in. Four bootstrappers, not the chain bootnodes | Event duty on the committee; one DNS seeder; hiding wallet-provider trust | Genesis 10 permissioned seats; `service.rs:614-625`; `2024-heimbach-deanon`; no relay payment found | Medium | Operators will not run relays without pay, and a payment asset exists. Then phase 3 moves forward and v1’s volunteer assumption is dropped |
| D8 Network tether | Hybrid sidecar: GossipSub v1.1 data plane, ledger for membership and hash anchors. Fallback is `Misc` plus the indexer | In-process Substrate gossip; ledger-only bus; global flood; mixnet default; a new overlay | No `libp2p-gossipsub` in `Cargo.lock`; protocols at `service.rs:586-644`; `sc-network-gossip` 0.34.0 only via consensus; eclipse papers on Kademlia; trilemma | High | Node ships GossipSub on a separate, authority-off peer set. Or the privacy requirement becomes global-observer anonymity |
| D9 Threats | v1.1 scoring, separate peer table, outbound quota, epoch caps, no receipts, CVE gate | “Scoring is enough”; “encryption hides the graph”; Dandelion++ claimed for a one-hop stem | `2020-leastauthority-gossipsub-audit`; `2023-kumar-gossipsub-acl2s`; `2015-heilman-eclipse`; `2022-prunster-ipfseclipse`; `2018-fanti-dandelionpp` | Medium | The chosen crate has no CVE fix, or a sim shows a minority eclipse that `D_out` does not stop. Then the overlay does not ship |
| D10 Build plan | Sim at 50/200/1,000 before mainnet. Small model of admission only. Sidecar testnet. Anchors on ledger 9. Stop and fall back if delivery or the CVE gate fails | Proving GossipSub again; building a new mesh after a failed sim; blocking the bus on relay payments | Evaluation method in `2020-vyzovitis-gossipsub` and `2025-farooq-staggering`; CVE from `2023-kumar-gossipsub-acl2s` | High | Phase-0 numbers miss the stop condition in D5. The decision then flips to the anchor fallback rather than to another overlay |
