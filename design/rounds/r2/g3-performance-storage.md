I'll start with the charter and the five Round 1 proposals, then check the citations they rely on before I vote.The charter and my Round 1 numbers are in hand. Next I read the four proposals and check the claims they hang on.The four proposals disagree hardest on who pays for fan-out and whether every node must see every event. I am checking the fee formula, the RLN timings, and the block budget those claims rest on.The bus has to keep an ordinary node’s cost proportional to the shard it actually carries. Three of the four proposals show that arithmetic honestly, and it rules their own full-feed and on-chain operating points out as a default. Fixed-size cells, eight shards, a hard publish cap, 48-hour per-shard retention, and a sidecar are the pieces that survive the citations. The chain can hold a membership root and an occasional batch root. It cannot hold the payloads. Figures below were recomputed from the cited files. Loads, the 1.25 control factor, and the 2× disk factor are assumptions.

## D1 Event format

- **s3-red-team:** one 2,048-byte record (128-byte header, 128-byte issuer permit, 1,792-byte body), 48-hour retention, sealed topic, salted recognition hint.
- **s4-evidence-auditor:** one 4,096-byte cell (128-byte header, 1,152-byte admission area, 2,816-byte body), 48 hours, header-encrypted Double Ratchet inside.
- **o3-consumer-experience:** `Misc` parts of 32+256 bytes, classes with 207 / 975 / 4,047 bytes usable, public view tag and ephemeral key, life of the chain.
- **o4-governance-operations:** four padded classes, 512 B to 32 KiB, claimed 304-byte header with RLN fields and a franking slot, expiry default 24 h and ceiling 14 d.

**Evidence.** Compact `Misc` is `Bytes<32>` plus `Bytes<256>` (`minokawa-compact/compiler/midnight-events.ss:71-74`). On the pinned ledger-9 VM (`54a4e013`), `MAX_LOG_SIZE` is 512 KiB and `MAX_LOG_EMITTED` is 1 KiB, and an event over that bound is omitted (`onchain-vm/src/vm.rs:39-43` and `decode_event` in the same file). The ledger-8 working tree has the 512 KiB log cap and charges a log as churn (`midnight-ledger/onchain-vm/src/vm.rs:38`, `:553-562`) and does not define `MAX_LOG_EMITTED`. That supports s3, s4, and o3 on why bulk ciphertext cannot be an emitted event. The RLN proof blob is a 128-byte compressed proof plus four 32-byte fields, 256 bytes (`2021-vac-waku2-rln-relay-spec`, RateLimitProof table). s3’s 128-byte permit can hold an issuer signature. It cannot hold that proof. s4’s 1,152-byte area can, with about 900 bytes spare. o4’s listed header fields sum to 296 bytes, not 304. o4’s “7-day withdrawal” is not in the lines it cites for the format’s sibling fee design (see D4). GossipSub’s worked example uses `D` of 6 only as the setting for which `D_out` defaults to 2 (`2020-gossipsub-v11-spec`, parameter table at the `D_out` row). That does not fix an object size.

**Vote:** s4. Freeze a single cell only after the admission proof is measured, and shrink the 1,152-byte area to the measured proof. A 4 KiB cell at s4’s recovery rate is `20 × 4096 = 81,920` bytes/s per full-feed client, 7.08 GB/day. Cutting unused admission bytes is a direct cut in that number.

**Objection:** every subscriber downloads the slack in the admission area. At 10 cells/s, 900 spare bytes is 0.78 GB/day on a full feed before any payload.

## D2 Definition of “private”

- **s3:** content confidentiality and selection privacy against infrastructure; no publisher, timing, volume, or relationship privacy against a global observer.
- **s4:** the same split, and an explicit block on strong relationship privacy from encryption, flooding, Dandelion++, or relay diversity.
- **o3:** also claims chain publisher unlinkability, relationship privacy except timing, per-epoch forward secrecy, and unlinkable contract reactions.
- **o4:** RLN unlinkability of event to membership, shard-level interest privacy, report-only disclosure; global observer out of scope.

**Evidence.** Dandelion++ Theorem 1 is a first-spy result on an unknown random 4-regular graph and puts ISP/AS adversaries outside its scope (`2018-fanti-dandelionpp`, the paper’s own threat section; s3 and s4 cite this and the text matches). Loopix excludes unrestricted client Sybils and limits corrupt providers (`2017-piotrowska-loopix`, evaluation is six mixes and 500 client processes on AWS, mean latency 1.93 s). The anonymity trilemma is a model bound, not a parameter recipe (`2017-das-trilemma`). Those citations support s3 and s4’s refusals. o4’s RLN membership anonymity matches Taheri’s security claim for the registration-and-messaging game (`2022-taheri-waku-rln-relay`, security paragraphs). It does not hide an unshielded NIGHT deposit, which o4 states separately. o3’s Monero citation (below, D5) does not support a cheap private scan. Indexer `contractEvents` requires a contract address (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`). DUST spends expose `v_fee` (ledger-8 `midnight-ledger/ledger/src/dust.rs:464`; s4’s ledger-9 line 469 is the same field).

**Vote:** s4. The leakage table matches what the overlay actually reveals, and it refuses inherited theorems.

**Objection:** whole-feed “interest privacy” costs 7.08 GB/day per client at s4’s own recovery budget. Clients will ask for a filter, and the property dies at the first filter.

## D3 Publish and subscribe model

- **s3:** one shared stream, local recognition, no topic subscription, contract consumption only by a later transaction.
- **s4:** the same whole feed, authenticated invites, witness data checked in-circuit, no global order.
- **o3:** PRF tags on a shared bus contract, full-stream default, opt-in bucket, chain order and a portable cursor; contracts check a Merkle anchor.
- **o4:** eight shards, hourly or per-message PRF tags visible to relays, light clients query stores by tag, intro-inbox trial decryption on shard 0.

**Evidence.** Waku’s deployed network puts every message on one of eight pubsub topics (`2024-cornelius-waku-network-dapps`, sharding paragraphs). That supports o4’s shard count as a precedent, not as a measurement of this bus. Bitmessage’s flood-and-scan is what s3 and s4 adapt; they label the adaptation as inference, which is accurate. `fieldPrefixes` applies to standard events only (`schema-v4.graphql:558-561`), so o3’s bucket mode is an indexer change, as o3 says. The subscription path re-queries storage on every `BlockIndexed` (`contract_event.rs:125-133`). Contracts have no network read; that is the read-out’s ledger-9 conclusion and o3/o4/s3 agree. o4’s OMR sizes match the paper: clue 956 bytes, detection key about 129 MB, detector about 0.065 s per message (`2021-liu-omr`, evaluation summary and the clue-embedding paragraph). The 956-byte figure is not in the two early lines o4 groups with it. The claim is still in the paper.

**Vote:** o4, for the shard split. A node’s unique bytes are then one-eighth of the network under a uniform-shard assumption, which is the only shape here whose relay cost stays flat as other shards grow.

**Objection:** the tag is relay-visible, and the light-client path queries by that tag. At o4’s sustained load one shard is `6.25 × 2,400 × 86,400 ≈ 1.30 GB/day`. A phone that will not pay that will take the leaky path. The intro inbox also piles every first contact onto shard 0, so the uniform-shard assumption fails for the traffic that is most sensitive.

## D4 Sustainable model

- **s3:** sponsors reserve relay, egress, and retention; launch admission is an issuer permit; DUST pays only chain execution.
- **s4:** prepaid leases, 300 credentials at one cell per 30 s (`300/30 = 10` cells/s), no promised slashing, DUST is gas only.
- **o3:** about 0.06 DUST per S-class publish, about 12 publishes per NIGHT per day, readers free, RLN only on a later lane.
- **o4:** RLN-v2 deposit plus a non-refundable fee into a relay pool, 20 messages per 60 s epoch, one anchor per minute at about 86 DUST/day.

**Evidence.** DUST is shielded and non-transferable (`midnight-docs/docs/concepts/dust-architecture.mdx:23`). It cannot be the relay payroll. That supports s3, s4, and o4’s split between gas and operator pay. Genesis `overallPrice / 2^64 = 10`, factors 1, block usage 1,000,000 bytes, writes 50,000, churn 50,000,000 (`midnight-node/res/mainnet/ledger-parameters-config.json:155-175`). The pinned fee function is `overall_price × (max(read, compute, block_usage) + write + churn)` (`dc87cc8f` `base-crypto/src/cost_model.rs`, `overall_cost`). Generation is 8,267 Specks per Star per second, `10^6` Stars per NIGHT, `10^15` Specks per DUST (`dust.rs` initial parameters; `structure.rs` `STARS_PER_NIGHT` and `SPECKS_PER_DUST`). Per NIGHT that is `8267 × 10^6 / 10^15 × 86400 = 0.714` DUST/day. s3’s 8,192-byte illustration, `10 × 8192/10^6 = 0.08192` DUST, and 165 NIGHT of generation for one anchor per minute, matches that formula. o3 and o4’s 6 KB does not. The constants they name already sum to `2912 + 4832 = 7744` bytes (`DUST_SPEND_PROOF_SIZE` in the pinned dust module; ledger-8 `zswap/src/structure.rs:634` `INPUT_PROOF_SIZE = 4832`), before a transcript. At 8 KB the block-usage term is 0.08 DUST, not 0.06, and o3’s “12 publishes per NIGHT-day” falls to about 9. Block usage can still dominate compute: validation multiplies compute by 1/4 (`ledger-parameters-config.json` `parallelism_factor`; read-out §7.3). Laurie and Clayton argue that puzzle cost does not separate botnet senders from honest users (`2004-laurie-proofofwork`). s3’s reading of that paper matches the text. Taheri lists multiple registrations and early withdrawal as open problems (`2022-taheri-waku-rln-relay`, open-problems paragraphs). o4’s citation of those lines for a 7-day withdrawal delay is not in the text. RLN-v2 does define `rate_commitment` and RLN-Diff (`2024-vac-rln-v2-spec`, abstract and flow). “20 messages per epoch” is o4’s parameter.

**Vote:** s4. A protocol cap of 10 cells/s is a number a capacity plan can sit on. Issuer permits (s3) and open DUST publishing (o3) both let a buyer push the network past the relay budget.

**Objection:** the same proposal then budgets recovery and cover at 20 cells/s. Cover is a cost every full-feed client pays, and no operator price is known. The 10/s cap and the 20/s download are not one budget.

## D5 Performance requirements

- **s3:** 10 records/s sustained, 100/s for 60 s, 10,000 full-stream consumers; a relay with 500 clients at about 83 Mbit/s nominal and 829 Mbit/s in the burst; validators carry nothing.
- **s4:** 10 real cells/s, 20 padded cells/s, same 10,000 consumers; 7.08 GB/day per client; a 500-subscriber gateway at about 410 Mbit/s; proof target 5 ms.
- **o3:** 1 event/s average and 10/s peak on the chain (claimed 3.6% and 36% of block usage); client about 52 MB/day; indexer about 48 Mbit/s at 10,000 subscribers; lane B later.
- **o4:** 50 events/s sustained and 500/s peak, mean 2,400 bytes, `D = 6`; all-shard relay about 5.8 Mbit/s each way sustained; verify at 30 ms so a 500/s relay needs 15 cores; phones prove in 0.5 s.

**Evidence.** Slot time is 6 s and the runtime block weight is 2 s with a 75% normal ratio and a 1 MiB length (`midnight-node/runtime/src/lib.rs:292`, `:300-313`). Ledger block usage is 1,000,000 bytes per block, so the chain ceiling is `10^6 / 6 ≈ 167 KB/s`. That supports every proposal’s refusal to treat the block as a 50–200 event/s bus. s3’s egress arithmetic checks: `10 × 2048 = 20,480` bytes/s per client; `500 × 20,480 + 6 × 20,480 = 10.36 MB/s = 82.9 Mbit/s`; the burst is 10×. s4’s checks: `20 × 4096 = 81,920` bytes/s; `10,000 × 81,920 = 6.55 Gbit/s` of subscriber payload; gateway `500 × 81,920 × 1.25 = 51.2 MB/s`. o4’s sustained relay line checks: `50 × 2,400 × 6 = 720,000` bytes/s ≈ 5.8 Mbit/s one way. o3’s indexer line checks only after the 0.6 KB assumption: `10,000 × 52 MB/day ≈ 48 Mbit/s`, and `10,000 / 6 / 25 = 67` queries per connection per second, so 15 ms is the saturation bound on a pool of 25 (`indexer-api/config.yaml:30`). The re-query itself is in the code cited above.

The CPU citations do not all say what the proposals use them for. Taheri says a membership proof for a group of `2^32` takes about 0.5 s on an iPhone 8, and that verification in that library takes about 30 ms (`2022-taheri-waku-rln-relay`, performance paragraph). o4 drops the group size. Revuelta’s nwaku table is the later measurement: verify 2.7 ms on an M1, 4.5 ms on a 4-vCPU cloud VM, 18.7 ms on a Pi 4; generate 85.7 ms, 276 ms, and 767 ms on those machines (`2024-revuelta-waku-latency`, Table 1). Messages of 25 KB or smaller were delivered in under 1 s in that paper’s simulation (`2024-revuelta-waku-latency`, simulation results). That supports a latency hope for a similar mesh. It is not this bus’s p99. Monero’s view tag skips the elliptic-curve step on about 99.6% of outputs (`2022-monero-pr8061-viewtags`, the 99.6% paragraph). o3 still does an X25519 on every unmatched event and only skips AEAD. The 50 µs figure is o3’s assumption. At 1 event/s it is `86,400 × 50 µs = 4.3 s/day`. At o4’s 50/s the same assumption is 215 s/day per full-feed client.

**Vote:** none of the four. The SLO I would adopt is per shard, not per network.

Assumption set: eight shards, uniform, GossipSub `D = 6`, control factor 1.25, mean object 4 KiB until the proof length is measured. Shard cap, whichever binds first: 10 events/s or 64 KiB/s unique. Relay bytes on one shard: `1.25 × 6 × unique`. At the cap that is 480 KiB/s ≈ 3.9 Mbit/s. A client that takes one copy of one shard pays at most 64 KiB/s (0.5 Mbit/s), not `D` copies and not the other seven shards. Verify budget uses Revuelta’s Table 1, not Taheri’s 30 ms: 10 proofs/s is 45 ms of core per second on the 4-vCPU VM and 187 ms/s on the Pi. Both fit an edge relay that holds one shard. A publisher proves once per burst of at most 32 KiB, not once per cell, because generate time on the Pi is 767 ms. Validators and the chain indexer carry none of this. Chain reservation for roots and registrations stays at or below 10% of block usage, 100,000 bytes per 6 s block, and only after the devnet transaction is measured.

s3 is the closest on honesty: it shows 829 Mbit/s and tells the team to benchmark a 1 Gbit/s relay. That benchmark is the reason not to adopt the full feed. o4 is the closest on shape, once 30 ms and 0.5 s are replaced.

**Objection to the leading overlay numbers:** s3 and s4 make every consumer’s download equal to the whole network. At 10,000 clients that is 205 MB/s (s3 nominal) or 6.55 Gbit/s (s4 padded). o4’s 15-core peak is an arithmetic consequence of the wrong verify constant: at 4.5 ms, 500 proofs/s is 2.25 cores on that cloud VM, and a single shard at a uniform 500/s peak is about 0.3 core.

## D6 Storage requirements

- **s3:** every launch relay keeps the full stream for 48 h: `10 × 2048 × 172800 = 3.296 GiB`, plus a 1.5× database factor; 30-day archive about 49 GiB; three retention receipts.
- **s4:** provision at 20 cells/s: 14.16 GB raw for 48 h, 32 GB reserved; 7-day archive about 50 GB; receipts from three operators.
- **o3:** no event bodies in ledger state; indexer about 52 MB/day and 19 GB/year; hot window at least 30 days; anchors accumulate because there is no state rent.
- **o4:** store nodes keep at most 7 days: `120,000 × 604,800 ≈ 72.6 GB` for all shards at 50/s, about 9.1 GB per shard, “at peak ×10”; anchor map pruned after 7 days.

**Evidence.** s3 and s4’s products match the formula `λ × S × R`. o4’s 72.6 GB matches `50 × 2,400 × 7 × 86400`. Ledger-9 logs are churn: written and deleted bytes are both charged (pinned `vm.rs` log arm; ledger-8 has the same comment at `vm.rs:553-562`). A log is not a payload store. `global_ttl` is 1,209,600 s, 14 days (`ledger-parameters-config.json:176`). That is a replay horizon for intents, not a reason to keep every ciphertext that long. o3’s “no state rent” matches the read-out §7.5; I did not re-derive rent from a rent module. MIP-0002’s event-storage appendix is a loose bound, which o3 says. s4 is right that receipts attest a promise. They do not prove the disk still holds the bytes tomorrow.

**Vote:** none of the four as written. Keep s3’s 48-hour window and o4’s per-shard split. Steady-state unique bytes on a store are `λ_shard × S × 172800`. At o4’s sustained 6.25 events/s and 2,400 bytes that is 2.6 GB raw per shard, not 9.1 GB, and not 72.6 GB. Assumption: budget 2× for indexes. Three stores per shard, operator-replicated, not flooded to every relay. The chain stores the day’s membership root and optional batch roots. Nullifiers live in relay memory for the quota day. Ledger-9 has no demonstrated deletion of an ever-growing nullifier set; until a contract overwrites one cell, the on-chain object is that root and nothing else.

**Objection to the leading 48-hour full-stream figure:** s3’s 3.3 GiB is cheap only because every relay stores the world at 10 records/s. The same formula at s4’s 20 cells/s is 14 GB, and at an unsharded o4 rate for 7 days it is 73 GB on every store. Disk, like bandwidth, has to be per shard.

## D7 Infrastructure actors

- **s3:** about 20 dedicated relays across at least five operators, paid by service contract; validators unchanged; anonymous admission is a later requirement.
- **s4:** published launch roster, explicit trust, validators only for registry transactions, open relay IDs are not independent operators.
- **o3:** Foundation indexers plus self-hosting in phase 1; lane-B relays unpaid; no reader payment.
- **o4:** seven stewards, permissioned relays then bonds, probe-paid pool, canaries, PrivCount, franking moderators, tombstones.

**Evidence.** Mainnet genesis lists 10 permissioned seats and 0 registered candidates (`midnight-node/res/mainnet/system-parameters-config.json:6-9`). There is no on-chain indexer payment in the read-out §2.3; o3 and o4 both say so. Douceur’s result is that locally created identities are not independent without a resource assumption (`2002-douceur-sybil`). s4’s use of that limit matches the paper’s claim. GossipSub outbound quotas are a resilience tool in the v1.1 spec, and the formal model found punishment-property violations in an Ethereum configuration (`2022-kumar-gossipsub-formal`, attack-generation summary). s3 and s4 are right not to treat scoring as a Sybil proof. o4’s “over 99%” Nym framing result is in that paper’s summary (`2026-cao-nymreputation`). I did not re-check every line number in o4’s Nym cluster. Canary load at one message per shard per minute is `8/60 ≈ 0.13` events/s, negligible next to 10–50/s. The governance machinery is not the bandwidth problem. The unpaid gateway is.

**Vote:** s4. Validators stay out, and decentralization is not declared from peer count.

**Objection:** s4’s own gateway is about 410 Mbit/s at 500 subscribers before overhead is finished. A roster with no bound contract for that port will not meet the 48-hour SLO. Wallet providers who terminate light clients have to be the ones who pay that bill, in the service contract s3 describes.

## D8 Network tether

- **s3:** independent libp2p overlay for bulk, Midnight for optional commitments; fallback is gateways serving the same stream.
- **s4:** the same hybrid; fallback is a small ledger announcement contract.
- **o3:** phase 1 is ledger and indexer only; phase 2 adds a GossipSub sidecar; fallback is the sidecar if ledger-9 events slip.
- **o4:** sidecar plus a Bus Registry; fallback is `Misc` ciphertext of at most 256 bytes, kept permanently.

**Evidence.** The node registers GRANDPA, BEEFY, and ledger-sync in `midnight-node/node/src/service.rs` (grandpa around `:580-586`, beefy notification at `:607`, ledger-sync at `:610-644`). The ledger-sync comment says arena serialization must not compete with authoring on validators. That supports every proposal’s refusal to put event payloads on the consensus swarm. I did not find a gossipsub crate reference while reading that function. o3’s phase-1 lane needs ledger-9 events. The support-matrix caveat in the read-out §0.3 still stands: mainnet docs list an older toolchain, and activation is unknown from these files. A 256-byte `Misc` fallback is `1/6` of an event per second if the chain is full of them at one part each, before proof bytes. It is a notice channel.

**Vote:** s3. Same tether as s4 and o4, and the fallback does not write payload bytes into chain history.

**Objection:** GossipSub amplification is still unmeasured on this object. Flood-publish defaults to true in the v1.1 parameter table, so a publisher’s own send is to all peers, not to `D`. The mesh factor `D` is the forward path only. Phase 0 has to measure both.

## D9 Threats and open risks

- **s3:** permits, bounded parsing, and configuration-specific GossipSub scoring; residuals include issuer linkage, receipt lies, and no global-observer defense.
- **s4:** ranked list that blocks strong anonymity, few-percent attacker claims from peer count, unchecked witnesses, silent fallback from whole-feed, and unbounded queues.
- **o3:** sequence gaps, two indexers, fixed parts, consumed-nullifiers; spam CPU bounded by block capacity.
- **o4:** RLN slashing, graylisting, multi-monitor scoring, tombstones; high residual on timing and on light-client tags.

**Evidence.** Safe mode’s inherent filter deliberately omits `Midnight::send_mn_transaction` (`midnight-node/runtime/src/check_call_filter.rs:39-45`). `SafeModeForceDuration` is `7 * DAYS` (`runtime/src/lib.rs:758`). A chain pause stops new registrations and anchors and leaves already-issued overlay traffic running. s3, s4, and o4 all say that; the code supports it. o3’s scan-DoS bound of `167 × 50 µs ≈ 8 ms` per block is arithmetic on the 6 KB size and the 50 µs assumption. At 8 KB the block holds about 125 such transactions, so the CPU story is the same order. It is still an assumption until X25519 is timed. Invalid-proof floods are limited to direct peers in Taheri’s analysis only after verification fails and the message is not forwarded. The first verify still costs 3–19 ms on the 2024 machines, or 30 ms on the 2022 library. s4’s bounded verify queue is the control that matches that cost.

**Vote:** s4. The blocks match the evidence: no global-observer claim, no peer-count anonymity, no contract effect from an unchecked witness.

**Objection:** the launch subsidy for cover traffic is a bandwidth tax on every full-feed node. Leave cover out until its bytes sit inside the shard cap. A padded mix at s4’s illustrative `53 × 5 × 8192 ≈ 2.2 MB/s` is a different product and is not a defense that is already paid for.

## D10 Build and verification plan

- **s3:** evidence freeze, then a model, then a 20-relay / 10,000-consumer measurement, with OMR and PIR tried only as separate experiments. Includes the per-recipient detector extrapolation.
- **s4:** adversary simulations at 1%, 3%, and 5%, then a seven-day pilot, then a mix experiment, then mobile retrieval.
- **o3:** phase 0 measures real publish cost, anchor writes, indexer fan-out at 1k/10k/50k, and a Quint model of the cursor state machine.
- **o4:** governance Quint invariants, then a ledger-only phase, then a permissioned overlay with a 500 event/s red-team day.

**Evidence.** s3’s OMR arithmetic matches the paper’s `∼0.065 s/msg`: at 10 new records/s that is 0.65 detector-seconds per second per recipient, and 6,500 at 10,000 recipients, if each recipient is scanned independently. The paper’s cost is per scan under that recipient’s key (`2021-liu-omr`, the 0.065 s/msg sentence). PerfOMR and SimplePIR are different workloads; s3 says so, and the abstracts support not importing 10 GB/s/core as a messaging throughput (`2022-henzinger-simplepir`). Cargo.lock pins ledger `6abe9b16`, VM `54a4e013`, and base-crypto `dc87cc8f` (lines 7894, 8460, 7609 in the lockfile region I opened). s3 is right that a tag name is weaker than those pins. o3’s phase-0 list is the right Midnight measurement set. o4’s 500 event/s gate is a peak test, not a disk-sizing test.

**Vote:** s3, with o3’s devnet fee measurement added as a hard gate. Acceptance I would actually ship against: at the shard cap, an edge relay stays under 4 Mbit/s and under 30% of one core on the 4-vCPU reference; store bytes after 48 h stay within 2× raw `λ S R`; the devnet registration or anchor transaction is at most 16 KiB and at most 0.5 DUST at genesis-like factors; a phone trial-decrypt or tag-match of one shard at 10 events/s stays under 50 ms of core per second. Miss the fee gate and the chain budget is redesigned. Miss the phone gate and phones stay off the mesh.

**Objection:** s3’s headline trial is the 10,000-consumer full stream. A pass certifies the data-center shape. The trial needs a one-shard arm at 64 KiB/s unique, or the acceptance line will ratify the cost this review is trying to avoid.

## Where the group will split

The three decisions most likely to stay in dispute are **D3**, **D4**, and **D5**. D3 is full feed versus shards versus the chain. D4 is issuer permits versus an RLN cap versus per-event DUST versus a deposit pool. D5 is the numeric SLO: 1 event/s on a block, 10 records/s to every client, or a per-shard cap near 64 KiB/s. D8 looks agreed (sidecar, validators out) until o3’s phase 1 puts the chain back in front.

The one fact that would settle the most of that is a ledger-9 devnet measurement of a single contract transaction that writes a 32-byte root and emits one `Misc`: serialized bytes, each of the five cost dimensions, and DUST at that block’s prices. o3’s 6 KB, 0.06 DUST, 3.6% of the block, and 12 publishes per NIGHT-day, and o4’s 86 DUST/day anchor, are all scaled from an unmeasured size. The two proof constants already named sum to 7,744 bytes before the transcript. If the real transaction is near 8–16 KB, the chain lane is a notice channel at about one event per second, phase 1 cannot be the bus, and the remaining argument is full feed versus shards at a stated rate. Those two client-download products are already in s3 (1.77 GB/day at 10×2 KiB) and s4 (7.08 GB/day at 20×4 KiB). They do not need another paper. They need that fee measurement so the chain option is either in or out.
