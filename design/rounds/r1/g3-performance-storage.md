I'll start from the charter and the Midnight read-out, then build the load model from the cited code and the local evidence set.The charter and the Midnight stack are in hand. Next I pull Bitmessage costs and the papers that bound fan-out, detection CPU, and retention.A private event bus has to keep every ordinary node’s cost proportional to the traffic on the shards that node actually carries. Bitmessage-style flood-and-trial-decrypt, and any design that writes each event into a Midnight block, both fail that test as soon as the network leaves launch rate. The data plane is a sidecar GossipSub mesh of eight public shards, admitted by a batched membership proof, retained for 48 hours by store nodes, and anchored on the ledger only as a quota root and as optional batch commitments. Validators, the chain indexer, and contract state do not carry payloads.

Figures below are either taken from the cited Midnight files and papers or computed from them. Loads L0, L1, and L2, the 2× index factor, the 25% gossip-control factor, and wall-clock trial-decrypt times are labelled **assumption**. The node pins ledger 9 (`notes/midnight-network-stack.md` §0.1). Constants I re-opened in the ledger-8 working tree are marked L8; they match the ledger-9 read-out where cited.

## D1 Event format

Relay-visible envelope, version 1, fixed fields so a relay can admit, deduplicate, and drop without parsing the payload:

| Field | Size | Visible to relays |
|---|---:|---|
| version | 2 | yes |
| shard | 1 | yes |
| expiry (unix seconds) | 4 | yes |
| class | 1 | yes |
| quota day | 4 | yes |
| membership root | 32 | yes |
| chunk nullifier | 32 | yes |
| admission proof | fixed, length frozen after measurement | yes |
| ciphertext | exactly the class length | opaque |

Class lengths are padded wire sizes: **S = 1 KiB**, **M = 4 KiB**, **L = 32 KiB**. A publisher may not send a variable length. Padding is the volume control. Class L is at most one object in flight per peer, because the patched Yamux receive window is 256 KiB (`notes/midnight-network-stack.md` §1.1). An object above 32 KiB is rejected on this mesh; the payload is stored as a content-addressed blob and the event carries the 32-byte name.

Inside the ciphertext: ephemeral sender public key, AEAD nonce, publisher sequence (`u64`), content schema id (`u16`), and the body. Relays never see publisher, recipient, topic, or schema. Event id = SHA-256(shard ‖ nullifier ‖ ciphertext). Unknown envelope versions are dropped.

One-shot events use a fresh ECDH to the recipient’s long-term key. That construction has no forward secrecy, as in Bitmessage (`2012-warren-bitmessage-whitepaper`, via `design/evidence/bitmessage-guide.md`). Established agent and wallet channels put a double-ratchet or Noise session inside the same ciphertext (`2016-signal-double-ratchet-spec`, `2024-vac-noise-x3dh-double-ratchet-spec`). The relay path is identical either way.

Lifetime is the envelope expiry, at most **48 hours** ahead and at most 60 seconds behind the relay clock. Bitmessage’s protocol text allows 28 days + 3 hours (`2012-bitmessage-protocol-specification`); that horizon is an archive product, not the default object. No view tag in version 1. A precise public tag is a recipient identifier, and a fuzzy clue waits until a phone measurement says trial decryption of one shard is too slow (D5).

## D2 Definition of “private”

Properties this design actually buys:

| Property | Against | Holds? |
|---|---|---|
| Content confidentiality | relay, indexer, chain observer, global passive observer | Yes, while the recipient key and any ratchet state hold. One-shot ECDH does not survive later compromise of the long-term key. |
| Publisher unlinkability to an IP, vs one honest first hop | single relay | Weakly, by a one-hop stem before the shard mesh (`2018-fanti-dandelionpp`). Not against a global observer. |
| Subscriber-interest privacy | mesh peers | Only at shard granularity. Peers learn the shard, not the contract, agent, or topic. |
| Topic privacy | relay | Yes for topics inside the ciphertext. A public contract’s shard is `H(contract address) mod 8`, so the contract’s existence on that shard is public by construction. |
| Volume privacy | global observer | Only up to the three size classes. Rates are visible. |
| Relationship privacy | global observer | No. |

Leakage table:

| Observer | Learns | Does not learn from this protocol |
|---|---|---|
| Shard relay | shard, class, expiry, quota day, membership root, nullifier, proof, ciphertext bytes, peer IPs on its links | plaintext, sender key, recipient, schema |
| Filter or store node serving a light client | the client IP, the shard, and the time range requested | which contract or key inside the shard |
| Chain observer | quota-registration transactions and any optional batch root: contract address, `v_fee`, public transcript (`notes/midnight-network-stack.md` §3.4) | event payloads, who holds the membership secret |
| Chain indexer | the same public chain data it already re-executes | private-bus payloads, if operators do not co-locate a store |
| Colluding minority of relays | first-hop stem traffic they touch; nullifiers they see | a delivery guarantee they can selectively break (D9) |
| Global observer | all of the above, plus timing and which peers mesh which shards | plaintext |

Out of scope, on purpose: global anonymity, traffic-analysis resistance, cover traffic, and metadata-private retrieval. Das et al. show strong anonymity forces a large latency overhead or a large bandwidth overhead (`2017-das-trilemma`). Cover traffic would put a cost that grows with the cover rate on every mesh node. That is the cost shape this design refuses unless a later measurement prices it.

## D3 Publish and subscribe model

Eight public shards, the same count The Waku Network uses to keep every message on one pubsub topic (`2024-cornelius-waku-network-dapps`). A publisher pins a shard: `H(contract address) mod 8` for contract-scoped events, or `H(shared secret) mod 8` for a private conversation. Shards are not chosen at random per event. Random placement would force every subscriber to carry every shard, which returns flood cost to the client.

Publish path: stem one hop to a random sidecar peer, then eager-push on the shard mesh (GossipSub, target degree D = 6). Admission is a proof that the sender knows a secret committed in the day’s membership root and that this chunk nullifier is bound to a byte budget (D4). Relays verify, then forward.

Subscribe path: a full participant grafts the shard mesh. A light wallet or phone does not join the mesh. It takes a unicast push of that one shard from a filter node it chooses (`2020-vac-waku2-filter-spec` is the pattern; the leak is in D2). There is no Bloom filter over topics. Whisper’s topic bloom is exactly the interest leak we decline (`2017-eip-627-whisper`).

Delivery is at-least-once. Duplicates are dropped by event id. There is no global order. Each publisher’s sequence lives inside the ciphertext; a gap is repaired by a store query for that shard and time range, which is the same information the client already revealed by subscribing. Store queries are not content-topic queries (`2020-vac-waku2-store-spec` does expose content topics; this bus must not). Replay dies by expiry and by a seen nullifier cache held for the quota day plus one hour.

Back-fill horizon is the 48-hour store, not the chain. A client offline for one hour on an L1 shard pulls `2.5 × 4096 × 3600 = 36.9 MB`. A client that waits the full window pulls the whole shard disk figure in D6.

Smart contracts cannot subscribe. No on-chain event read exists, and `emit` is public (`notes/midnight-network-stack.md` §5.4, §3.2). A contract consumes an event only when a later transaction writes a batch root into contract state and a follow-up call presents an inclusion path. The contract acts on what that call discloses. Wallets and agents run the same shard client locally. They do not call indexer `connect(viewingKey)`, which hands the operator the key (`notes/midnight-network-stack.md` §4.4).

## D4 Sustainable model

Publishers pay DUST for a daily membership. Relays and stores are unpaid by the protocol in v1, the same way full nodes and indexers are unpaid today (`notes/midnight-network-stack.md` §2.3). Fees are burned: the ledger-9 read-out found no credit of `v_fee` to a validator or treasury. This design does not add a fee destination.

Genesis price is `overallPrice / 2^64 = 10`, and each factor is 1 (`midnight-node/res/mainnet/ledger-parameters-config.json:169-175`). The cost function is `overall_price × (max(read, compute, block_usage) + write + churn)` (L8 `midnight-ledger/base-crypto/src/cost_model.rs:392-400`). Block usage is normalised by 1,000,000 bytes (`ledger-parameters-config.json:158`), so a transmitted byte at these factors costs `10 / 10^6 = 0.01` DUST per KiB. A persistent byte costs `10 / 50,000 = 0.2` DUST per KiB, twenty times more, and the persistent cap is 50,000 bytes per block. That is why payloads stay off the ledger.

**Assumption:** a quota-registration transaction is 10 KiB (DUST spend proof is 2,912 bytes and a call proof is estimated at 4,832 bytes in the ledger-9 read-out, §6.2, plus a short transcript). At genesis factors the block-usage term is `10 × 10,000 / 10^6 = 0.1` DUST. A write of a 32-byte root adds `10 × 32 / 50,000 = 0.0064` DUST. Live prices move with fullness, up to about 4.6% per block when a dimension sits at the 0.99 clamp (`a = 100` from the same JSON; the 4.6% figure is the read-out’s evaluation of `−ln(1/x − 1) / a`). One hundred consecutive saturated blocks compound to about 90×. Clients must price from the block’s `ledgerParameters`, not from 0.1 DUST.

One NIGHT caps at 5 DUST and generates about 0.714 DUST/day. The docs work 100 NIGHT as ~71 DUST/day and a one-week cap (`midnight-docs/docs/concepts/dust-architecture.mdx:109-116`); per NIGHT that is 0.71 DUST/day. I use 0.714 from `5 / 7`. A publisher who registers once a day spends 0.1 DUST, which is about 0.14 NIGHT of generation. Hourly registration would be 2.4 DUST/day and about 3.4 NIGHT. Daily is the sustainable choice; the intra-day byte budget is enforced off chain.

Chain budget reserved for this bus: **10% of block usage**, 100,000 bytes per 6-second block (`midnight-node/runtime/src/lib.rs:292`). At 10 KiB per registration that is 10 transactions per block, 1.67 per second, about 6,000 new or renewed memberships per hour if the reservation is full, or about 144,000 per day. Launch will be far under that. The client stops buying quota when the last block’s Midnight byte usage exceeds 50% fullness, so this bus does not itself shove the price up the log curve.

Spam price, genesis factors, shard cap 64 KiB/s (D5): filling one shard for a day moves `64 × 1024 × 86,400 ≈ 5.53 GB`. If one membership buys a 1 MB/day byte budget, the spammer needs about 5,500 memberships, about 550 DUST, about 770 NIGHT of generation. Congestion multiplies that by the same factor honest users pay. Proof-of-work is not the admission mechanism. Bitmessage’s minimum is 1,000 trials per byte and does not pay relays (`design/evidence/bitmessage-guide.md`; `2015-schaub-bitmessage-antispam`). RLN’s economic idea is the one we keep: a paid membership plus a nullifier, verified by relays (`2022-taheri-waku-rln-relay`). The circuit may be RLN v2’s per-epoch budget (`2024-vac-rln-v2-spec`) or a Midnight anonymous-membership proof (`midnight-docs` group-membership pattern in the read-out §6.3). The performance constraint is the verify budget in D5, not the circuit brand.

Low load: relays still mesh D = 6, store 48 hours of nearly empty shards, and the chain sees registrations only. Empty shards are not anchored. High load: shard cap, class weights (an L chunk debits 32× an S chunk), and the 10% chain reservation are the brakes. There is no per-sender Substrate throttle on Midnight transactions (`notes/midnight-network-stack.md` §1.6), so the contract nullifier and the relay nullifier cache are the rate limit.

## D5 Performance requirements

**Hard chain ceiling.** Block usage 1,000,000 bytes / 6 s = 166.7 KiB/s for the entire Midnight block (`ledger-parameters-config.json:158`, `runtime/src/lib.rs:292`). Persistent writes are 50,000 / 6 = 8.3 KiB/s. Compute weight is 2 s per block (`runtime/src/lib.rs:306-311`); authors may spend 2/3 of the slot proposing (`midnight-node/node/src/service.rs:894`).

An on-chain event is a full transaction. At the 10 KiB assumption, L1 (20 events/s) is 200 KiB/s, which is more than the whole block. L0 (2 events/s) is 20 KiB/s, about 12% of the block, and every byte is public. The chain can carry launch-rate public notices. It cannot carry product-rate private events. `Misc` adds a 256-byte public payload on top of that transaction (`notes/midnight-network-stack.md` §3.2). It is not a bus.

**Mesh arithmetic.** GossipSub’s per-node amplification is about the mesh degree D, independent of network size (`2024-revuelta-waku-latency` §3.3). The v1.1 spec’s defaults are written for D = 6 (`2020-gossipsub-v11-spec`, `D_out` “2 for a D of 6”). Waku keeps D between 4 and 12. Planning bandwidth is `1.25 × D × λ_shard × S`. The 1.25 is an **assumption** for IHAVE/IWANT control traffic; the Bitmessage scalability note omitted `inv`/`getdata` and so will not be repeated blind (`design/evidence/bitmessage-guide.md`).

Mean object size for the tables is 4 KiB. A mix of 70% S, 25% M, 5% L has mean `0.7×1024 + 0.25×4096 + 0.05×32768 = 3379` bytes, so 4 KiB is a fair centre. If class L rises to 20% of objects the mean becomes 8.3 KiB and every line below scales by 2.45. Quota is therefore denominated in bytes, and class L is capped by debit, not only by count.

Loads are **assumptions**: L0 = 2 events/s network-wide, L1 = 20/s, L2 = 200/s, eight shards, uniform, D = 6, S = 4096.

| Load | λ per shard | Unique payload | Relay bandwidth (×6 ×1.25) | Flood-all bandwidth, same relay carrying every shard |
|---|---:|---:|---:|---:|
| L0 | 0.25/s | 1.0 KiB/s | 7.5 KiB/s (0.06 Mbit/s) | 0.48 Mbit/s |
| L1 | 2.5/s | 10 KiB/s | 75 KiB/s (0.60 Mbit/s) | 4.8 Mbit/s |
| L2 | 25/s | 100 KiB/s | 750 KiB/s (6.0 Mbit/s) | 48 Mbit/s |

Disk does not multiply by D; bandwidth does. Flood-all at L2 is a home-link and a validator-link problem. Shard scope keeps L2 inside a small relay.

**Shard cap, which is the SLO.** A light-capable shard stays at or below **10 events/s and 64 KiB/s unique**, whichever binds first. Eight shards give a network cap of 80 events/s or 512 KiB/s before a generation adds shards. At the byte cap a relay spends `1.25 × 6 × 64 KiB/s = 480 KiB/s ≈ 3.9 Mbit/s`. A light client on the filter path pays one copy, 64 KiB/s = 0.5 Mbit/s, not the mesh multiple. Crossing the cap marks the shard heavy: light clients stop, or they accept a filter node and the D2 leak. Adding shards cuts per-node bytes and cuts the anonymity set by the same factor. Do not add shards until a shard holds the cap.

**CPU, admission.** Waku’s nwaku RLN measurements (`2024-revuelta-waku-latency` Table 1): verify 2.7 ms on an M1, 4.5 ms on a 4-vCPU cloud VM, 18.7 ms on a Raspberry Pi 4; generate 85.7 ms, 276 ms, and 767 ms on those machines. Per-message verify at the shard cap is `10 × 4.5 ms = 45 ms` of core per second on the cloud VM, and 187 ms/s on the Pi. Both fit an edge relay. Flood-all at L2 is `200 × 4.5 ms = 900 ms/s`, most of a core, before consensus work. That is the number that keeps this mesh off validators.

Generating a proof per event caps an M1 publisher at about 10 events/s and a Pi at about 1/s. The bus therefore batches: one proof covers a burst of at most 32 messages or 32 KiB, flushed at least every 200 ms while the burst is non-empty. Relays cache the verify on the proof id and still enforce each chunk nullifier. Publisher cost becomes one proof per burst. A laptop that is not a firehose spends that 86 ms occasionally. A phone is a subscriber, not a publisher, until a measured prove time on that phone is under 200 ms.

A full Midnight PLONK proof per event is the wrong tool. Verification is priced at 3.27 ms plus 4.56 µs per public input in the ledger cost model, but proving a Zswap spend is documented at ~190 ms on a 32-core server and 5–30 s on a laptop (`notes/midnight-network-stack.md` §6.2). The daily membership transaction is the only Midnight proof on the publish path.

**CPU, detection.** Ledger prices `ec_mul` at 127,815,559 ps ≈ 0.128 ms (`ledger-parameters-config.json:132`). That is a cost-model unit, not a wall clock. **Unknown:** JubJub ECDH wall time on a phone and a laptop; measure it before phase 1 ships. Sensitivity: at 1 ms per trial decrypt, a light client on one L1 shard (2.5/s) spends 2.5 ms/s; on a shard at the 10/s cap, 10 ms/s; on all eight shards at the cap, 80 ms/s. The radio, not the scalar multiply, is the light-client limit. Monero’s 1-byte view tag does not remove the shared-secret multiply; the proposer still spends scalar multiplies and hopes for a 50–70% cut in the rest of the scan (`2021-monero-mrl73-viewtags`). It is not a 256× CPU win, and an exact tag would identify the recipient. Version 1 omits it.

Oblivious message retrieval is about $1.02 per million messages scanned **for each recipient** (`2021-liu-omr`). At L1, 20 events/s is 1.73 million messages/day, about $1.8 per recipient per day. Five thousand recipients is on the order of $9,000/day. Digests decode in ~20 ms, which is not the problem. The linear scan per recipient is. Pung’s multi-retrieval costs the client 4.5–36 MB per message (`2016-angel-pung-1`). Both are mailbox tools. They are not the bus.

**Fan-out.** Mesh fan-out is D = 6 and does not grow with subscriber count. Unicast filter fan-out does. One filter node serving 1,000 light clients on one L1 shard sends `1000 × 10 KiB/s = 10 MB/s ≈ 80 Mbit/s`. Serving all eight shards to those clients is about 640 Mbit/s. Wallet providers who proxy users must count this; the mesh will not hide it. Concurrent mesh members have no protocol cap. The sidecar’s own peer cap is a design parameter: 50 peers, with mesh target 6, in the same range as Waku’s 6 mesh plus 25 gossip peers. The consensus node’s upstream defaults of 8 outbound and 32 inbound (`notes/midnight-network-stack.md` §1.8, SDK-ref) belong to the block network and are not reused.

**Latency targets** (design targets, not Midnight measurements). Waku’s model and a 1,000-node simulation delivered 25 KiB messages within 1 second at D = 6, with four hops enough in that sim and a link latency of 150 ms (`2024-revuelta-waku-latency`). Our objects are smaller and our relay count at launch is smaller. For N = 32 and D = 6 their hop formula gives on the order of 3 hops. Target for a light-capable shard: p50 under 1.5 s and p99 under 3 s, including a 200 ms batch wait and a one-hop stem. Anchored events add finality. The docs say finality is usually about 3 blocks, about 18 s (`notes/midnight-network-stack.md` §1.7). A contract reaction also waits on proving (seconds to tens of seconds) and two transactions. Budget a contract-visible event at **tens of seconds on a proof server, and minutes from a laptop**. Gossip latency is not chain latency.

Node classes, sustained, excluding the 2× disk factor (that is D6):

| Class | Carries | Bandwidth SLO | CPU SLO | At L1 |
|---|---|---|---|---|
| Light client | 1 shard, filter push, no mesh | ≤ 0.5 Mbit/s (the cap) | trial decrypt of that shard only | 10 KiB/s, ~0.08 Mbit/s |
| Edge relay | 1 shard mesh | ≤ 4 Mbit/s | ≤ 30% of one core at 4.5 ms verify | 0.60 Mbit/s |
| Full relay | up to 4 shards | ≤ 16 Mbit/s | ≤ 2 cores | 2.4 Mbit/s |
| Filter node | unicast copies | provision `n × λ_shard × S` | same verify as a relay | 80 Mbit/s per 1,000 clients per shard |
| Validator | nothing on this bus | 0 | 0 | 0 |
| Indexer | chain only | unchanged | unchanged | unchanged |

What would break the SLO first: class-L fraction, then filter-node fan-out, then proof generation on the publisher, then disk at the cap. Raw bandwidth of an edge relay at L1 is not the binding constraint.

## D6 Storage requirements

Steady-state unique bytes on a store are `λ_shard × S × R`, the Bitmessage relation `D_node ≈ λ S R` (`design/evidence/bitmessage-guide.md`), with λ replaced by the shard rate. Replication across stores is an operator choice, not a flood. **Assumption:** budget 2× the raw figure for indexes and metadata. The guide did not measure that factor.

R = 48 × 3600 = 172,800 s.

| Load | Raw bytes, one shard, 48 h | With 2× | Raw, all 8 shards, 48 h |
|---|---:|---:|---:|
| L0 | 177 MB (0.16 GiB) | 0.33 GiB | 1.32 GiB |
| L1 | 1.77 GB (1.65 GiB) | 3.3 GiB | 13.2 GiB |
| L2 | 17.7 GB (16.5 GiB) | 33 GiB | 132 GiB |
| Shard at the 64 KiB/s cap | 11.3 GB (10.5 GiB) | 21 GiB | 84 GiB if every shard is at the cap |

Check: L1 shard `2.5 × 4096 × 172800 = 1,769,472,000` bytes. Flood-all L2 is 141.6 GB raw per node per 48 h (131.8 GiB). That is the figure that disqualifies “every full node stores the bus.” Bitmessage’s illustrative 1,000 objects/min of 2 KiB already projects ~77 GiB over 28 days; our L2 flood is that problem on a shorter clock.

Retention and pruning:

- Mesh cache: seconds to a few heartbeats. GossipSub’s heartbeat in the 2020 report is 1 s (`2020-vyzovitis-gossipsub`). The mesh is not a store.
- Edge and full relays that elect to store: expiry, hard cap 48 h, delete on expiry. No indefinite object table.
- Archive role, optional: 14 days, matching mainnet `global_ttl` of 1,209,600 s (`ledger-parameters-config.json:176`), so an intent can still name an anchored root while replay protection remembers the intent. Fourteen days is 7× the 48-hour column. An archive of all shards at L2 is about 0.9 TiB raw. That is a paid machine, not a default node.
- Light clients: local decrypted cache, user cap. Suggest 200 MB as a wallet default (**assumption**), oldest plaintext dropped first. Lossy by consent; the store still has the ciphertext until expiry.
- Ledger: the day’s membership root (32 bytes, overwritten) and optional batch roots for events that paid for anchoring. Not payloads, not per-message nullifiers. Midnight has no state rent (`notes/midnight-network-stack.md` §7.5). A nullifier set that grows by 6,000 × 32 bytes per hour and is never deleted becomes ~1.7 GB/year of consensus state at the 10% registration ceiling, and full nodes only prune historical state (default 256 blocks, `full-node.mdx` via the read-out), not live contract state. Nullifiers live in relay memory with a one-day TTL. If the membership contract cannot overwrite a single cell and drop yesterday’s tree, the contract rotates and the old tree must be removed in the same transaction. Until that removal is demonstrated on ledger 9, the on-chain object is one root cell and nothing else.
- Indexer: no private-bus tables. Indexer ledger-state retention is 1,000 blocks (`notes/midnight-network-stack.md` §4.6). Contract-event storage projections in MIP-0002 (~250 GB/year upper bound) describe public `emit` traffic, and the read-out already flags that appendix as a loose bound. This bus must not add a second copy there. Preprod’s old schema reached hundreds of gigabytes by storing full contract state per action; that is a warning against putting event bodies in contract state.

Availability: durability is three store nodes per shard (**assumption**, an operator target), any one answering. The mesh provides fast at-least-once delivery and then forgets. If all stores of a shard lose the object, it is gone. No erasure coding in v1. Anchored batch roots remain on the chain for `global_ttl` as commitments; they are not a payload backup.

Availability is not a total order and not exactly-once. A contract that needs inclusion uses the batch root. Everyone else uses the 48-hour store.

## D7 Infrastructure actors

| Actor | Admission | Trusted with | Paid by |
|---|---|---|---|
| Edge and full relay (sidecar) | open, GossipSub scoring, `D_out` so inbound Sybils cannot fill the mesh (`2020-gossipsub-v11-spec`) | forwarding and, if they store, 48 h of ciphertext | nobody in v1; run it if you need the shard |
| Store | same binary, disk enabled | time-range queries for a shard | the operator who needs back-fill (wallet provider, agent host) |
| Archive | opt-in flag, 14-day disk | the same, longer | a commercial deal outside the protocol |
| Filter node | open | the client’s shard choice and IP | same as the store |
| Validator | **excluded** | block production only | existing (and currently unpaid) block-reward path |
| Indexer | unchanged | public chain, not this payload | unchanged; no on-chain indexer payment exists |
| Publisher | DUST membership | their own key | their NIGHT generation |
| Wallet provider, agent host | run a sidecar or a filter node | whatever their users already trust them with | their users, off protocol |

Launch path. Phase 0: the engineering team runs eight sidecars on a devnet, one store each. Phase 1: anyone runs the sidecar; bootstrapping is a published peer list, as Waku does with a signed list plus discovery (`2024-cornelius-waku-network-dapps`). Phase 2: shard split only after a shard sits on the D5 cap for a week. Phase 3: a relay payment market only if volunteer stores miss the 48-hour SLO. Do not design that market before the measurement. At L1 an edge relay is 0.6 Mbit/s and about 3 GiB of disk with the index factor. That is small next to a validator, which already runs a Cardano db-sync Postgres (`notes/midnight-network-stack.md` §2.1). **Inference:** self-use carries L1. It will not carry a filter node with thousands of unicast clients; those operators are the wallet providers, and D5 gives them the bandwidth bill.

Validators stay out because the peer set is small and permissioned (mainnet genesis 10 of 10 permissioned, read-out §2.2), proposal time is already budgeted, and there is no gossipsub in `midnight-node`’s `Cargo.lock` (searched; no match). Putting the mesh in the consensus process would spend the 2 s block weight and the 32 inbound slots on event traffic.

## D8 Network tether

**Recommendation: hybrid sidecar.** Ledger for the daily membership root and for optional batch anchors. A separate libp2p GossipSub overlay, genesis-scoped by the Midnight chain id in the protocol name, for bulk. The sidecar reads roots through the existing indexer or node RPC and submits quota transactions with `send_mn_transaction`.

**Fallback:** a notification protocol registered beside the Midnight ledger-sync protocol (`midnight-node/node/src/service.rs`, read-out §8), still default-off on validators, shipped only if sidecar deployment fails in phase 0. That fallback is a node fork. Every operator who wants to relay must run it. It is not the launch path.

Rejected:

- Ledger and indexer alone. L1 does not fit in 166.7 KiB/s, and what would fit is public.
- Riding the existing consensus swarm. No gossipsub crate is linked, Yamux and peer slots are shared with GRANDPA and BEEFY, and a custom protocol requires the fork above.
- Mixnet data plane. Loopix relays can move hundreds of messages per second, with end-to-end latency in seconds plus cover (`2017-piotrowska-loopix`). That is a different product, and cover is a cost that scales for every mix.
- On-chain `emit` as the private channel. Public, 256-byte `Misc`, finality-bound, indexer-mediated.

Changes to Midnight components in v1: one Compact contract that overwrites a membership root; no compiler change; no node change; no indexer schema change. midnight-js grows a bus client beside `PublicDataProvider`. The wallet syncs a shard locally and does not extend `zswapLedgerEvents`. The dapp connector has no event method today (`notes/midnight-network-stack.md` §5.3); phase 1 does not block on one. Agents open the sidecar directly. Contract authors who need inclusion write the batch root themselves in a follow-up transaction.

## D9 Threats and open risks

| Attack | Defence | Residual |
|---|---|---|
| Spam flood | daily DUST membership, byte-denominated chunk nullifiers, shard cap, GossipSub P4 invalid-message score | A publisher who pays can still fill their budget. A split view can double-spend a nullifier until gossip converges. Waku’s write-up notes economic slashing of the publisher was not in the nwaku they measured (`2024-revuelta-waku-latency`). Same gap here. |
| Disk fill | 48 h expiry, class padding so size is predictable, store quota per shard | A store that disables expiry is its own problem. Clients must cap downloads. |
| Bandwidth exhaustion of light clients | shard cap, filter path is one copy, class L debit | A heavy shard pushes phones off. That is the SLO, not a bug. |
| Verify DoS | fixed proof length, verify cache, score peers who send bad proofs | First proof of a burst still costs 3–19 ms. Cap concurrent unverified proofs per peer. |
| Eclipse of a shard | `D_out`, peer scoring, bootstrap list with application scores (`2020-gossipsub-v11-spec`) | A shard with few honest relays is eclipseable. Phase 0 must not open a shard with fewer than D_high honest relays. |
| Deanonymisation by filter or store | documented leak; self-run sidecar is the alternative | Users who use a hosted filter give that host their shard and IP. |
| Global traffic analysis | size classes only | Not defended. Cover is rejected until priced. |
| Replay | expiry + nullifier cache | Cache loss on restart replays until expiry. Persist the nullifier set or accept a restart window. |
| Censorship | mesh diversity, publisher can pin a different shard only by losing subscribers | A colluding majority of one shard can drop a nullifier. Eight shards do not route around a targeted shard if the recipient is pinned to it. |
| Key compromise | ratchet inside established channels | One-shot events are readable after long-term key theft. Say so in the wallet UI. |
| Indexer abuse | indexer never receives the payload | An indexer run by the same operator as a filter node combines chain identity with shard interest. Operators who want the privacy claim separate the processes. |
| Chain pause | quota registration stops; already-issued roots keep working until the day ends | Safe mode can block `send_mn_transaction` (read-out §2.2). The bus then cannot enrol new publishers. Existing ciphertext still flows. |
| Sybil relays | scoring and paid membership for publishing; relaying itself is open | Free relays can still Sybil. Scoring raises the cost of staying in the mesh; it does not make Sybils impossible (`2002-douceur-sybil`, as the limit, not as a solved control). |

The performance-relevant open risk is the unmeasured wall-clock ECDH and the unmeasured registration transaction size. Every CPU and DUST figure that depends on them is provisional.

## D10 Build and verification plan

Phase 0, before any mainnet contract. A Shadow-style or testnet run of 32 and of 100 sidecars, eight shards, D = 6, object mix 70/25/5, offered load at L1 and at the 64 KiB/s cap. Record per-node goodput, p50 and p99 latency, CPU, and bytes on disk after a simulated 48 h (accelerated clock is fine if expiry is tested separately). Waku’s 1,000-node result is evidence that this shape of mesh can be fast (`2024-revuelta-waku-latency`). It is not evidence about our proof or our object layout.

Also in phase 0: measure JubJub ECDH and AEAD on one phone and one laptop; measure admission prove and verify on the M1-class, 4-vCPU, and Pi-class machines already used as reference points; submit one real quota transaction to a devnet and record its byte length and DUST at that block’s prices.

Formal check, small, before the contract is deployed: a model of the quota root and the chunk-nullifier set. Invariants: a nullifier is accepted once per day; accepted bytes for a membership never exceed the purchased budget; expiry is monotone; an object whose expiry is more than 48 h ahead is rejected. Quint or TLA+ is enough. Do not model GossipSub again; that protocol already has an ACL2s line (`2023-kumar-gossipsub-acl2s`) and we are not modifying it.

Acceptance for leaving phase 0:

- At L1, no edge relay exceeds 2 Mbit/s or 30% of one core. The arithmetic predicts 0.6 Mbit/s; 2 Mbit/s is the fail line.
- p99 latency on a light-capable shard under 3 s at L1, stem included.
- After 48 h, store bytes ≤ 2× raw `λ S R`.
- Devnet registration transaction ≤ 16 KiB and ≤ 0.5 DUST at genesis-like factors. Above either number, the 10% chain reservation and the 0.1 DUST planning figure are wrong and D4 is redesigned before phase 1.
- Trial decrypt of a shard at 10 events/s ≤ 50 ms/s on the measured phone. If it misses, phase 1 stays “full relays and desktops” and phones wait for a detection clue.

Phase 1: public sidecar, eight shards, 48 h stores, no view tag, no archive, no relay payments, validators untouched. Phase 2 only if a measured SLO misses: fuzzy detection if phone CPU misses, a ninth shard if a shard holds the cap, a node-fork fallback if operators will not run a sidecar. Phase 3: OMR or PIR only for a narrow mailbox whose recipient count keeps Liu’s cost under a budget the operator will pay, never for the shard mesh.

Change course if any of these is true: the devnet transaction is far above 16 KiB; phone decrypt is far above 50 ms/s and detection cannot be made cheap; honest shard occupancy stays under a few tens of relays so the anonymity set is the operator list; or governance will not accept a contract that stores even a single root. In that last case the private bus waits, and public `contractEvents` remains the only supported channel, with the capacity limit in D5 stated on the tin.

## Decision table

| Decision | Choice | Rejected | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Format | Versioned envelope; classes 1 / 4 / 32 KiB; 48 h expiry; sealed sequence and schema; fixed-length admission proof | Bitmessage variable objects up to 2^18 and 28-day TTL; public `Misc` as the private body; per-event view tag in v1 | `2012-bitmessage-protocol-specification`; Yamux 256 KiB window in the read-out §1.1; Compact `Misc` 256 B in §3.2 | high | A measured MTU or proof length that does not fit the 32 KiB class |
| D2 Privacy | Content confidentiality; shard-level interest privacy; no global anonymity; one-shot without forward secrecy | Flood-for-ambiguity; cover traffic; mixnet as the default | `2017-das-trilemma`; `2018-fanti-dandelionpp`; Bitmessage guide on static ECDH | medium | A deployment where shard subscription alone identifies users, and a priced cover design that stays inside the D5 cap |
| D3 Pub/sub | Eight pinned shards; mesh for relays; unicast filter for light clients; at-least-once; contract via a later inclusion transaction | Random per-event shard; topic Bloom filters; on-chain subscription | `2024-cornelius-waku-network-dapps`; `2017-eip-627-whisper`; read-out §5.4 | high | Subscribers who must hear every shard, which collapses the cost model |
| D4 Payment | Daily DUST membership, burned fee, ≤10% of block usage; byte budget; relays unpaid in v1 | Per-event Midnight transactions; proof-of-work; a new fee sink | `cost_model.rs:392-400` (L8); `ledger-parameters-config.json`; `dust-architecture.mdx:109-116`; `2022-taheri-waku-rln-relay` | medium | Devnet registration above 16 KiB or 0.5 DUST, or a decision that relays will not run without protocol payment |
| D5 Performance | Shard SLO 10 events/s and 64 KiB/s; relay ≤4 Mbit/s per shard; batched proofs; light clients off the mesh | Every node pays `Θ(total traffic)`; OMR or Pung as the data plane; per-event PLONK | Waku latency paper Table 1 and §3.3; `2021-liu-omr`; `2016-angel-pung-1`; block usage 10^6 / 6 s | high on the arithmetic, medium on transferred RLN timings | Measured verify ≫ 10 ms, or a mean object size ≫ 8 KiB |
| D6 Storage | 48 h shard stores; 14-day archive optional; chain holds a root only; nullifiers in relay memory | 28-day flood; payload in contract state; indexer as the bus disk | `D_node ≈ λSR` in the Bitmessage guide; `global_ttl` 1,209,600 s; no rent in read-out §7.5 | high | A requirement for guaranteed payload retention beyond 48 h without a funded archive role |
| D7 Actors | Sidecar relays and stores; validators excluded; wallet providers own filter fan-out | Validators as relays; a new paid role in v1 | Read-out §2.1–2.3; GossipSub v1.1 scoring | medium | Evidence that voluntary stores miss the 48 h SLO at L1 |
| D8 Tether | Hybrid: ledger for roots, sidecar GossipSub for bulk. Fallback is a default-off node protocol | Consensus-swarm gossip; ledger-only; mixnet | No `libp2p-gossipsub` in `midnight-node/Cargo.lock`; read-out §1.5 and §8 | high | Operators refuse a second process and also refuse a fork, which leaves only public `contractEvents` |
| D9 Threats | Cap, score, expiry, and an explicit non-claim on global adversaries | Treating RLN slashing or cover traffic as already deployed | `2024-revuelta-waku-latency`; `2020-gossipsub-v11-spec` | medium | A measured eclipse or nullifier-split attack that scoring does not contain |
| D10 Plan | Phase 0 simulation and a devnet fee measurement gate phase 1; Quint/TLA only for the quota set | Building the contract before the byte and DUST measurement | Waku evaluation method as the template, not as our result | high | A phase-0 miss on the 16 KiB / 0.5 DUST gate or the 3 s p99 gate |
