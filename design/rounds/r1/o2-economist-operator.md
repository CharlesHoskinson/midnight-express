# Midnight Private Events: Round 1 proposal from the economist and operator

## Summary of position

The bus should be a **hybrid**. Encrypted events move on a separate GossipSub overlay run as sidecars next to Midnight nodes. A small Compact contract on Midnight (the **Bus Registry**) holds four things: publisher memberships, the bonds behind them, a treasury, and a bounded ring of batch anchors.

- **Spam control.** Senders do not pay per event and do no proof-of-work. Every event carries a **rate-limiting-nullifier (RLN-Diff) proof** tied to a NIGHT-bonded membership. Publishing twice in the same slot reveals the publisher's secret, and anyone can then slash the bond on-chain.
- **Why DUST cannot be the currency.** DUST is non-transferable and fees appear to be burned, so DUST can price on-chain use but can never pay an operator. Operator income therefore has three sources: non-refundable registration fees in NIGHT, slashed bonds, and a declining launch grant.
- **What gets paid.** The treasury pays only for work a contract or client can check: anchors that were posted, storage that passes on-chain availability challenges, and retrieval that clients buy directly with anonymous credit tokens. Relaying is not paid by the protocol, because relay "quality" scores have been gamed in deployed systems (`2026-cao-nymreputation`).
- **Operator path.** Launch is foundation-run behind a timelocked maintenance key. There are measured gates to open bonded participation. A payout saturation cap means no single operator can earn more than a fixed share.

Every number below is either cited or shown as arithmetic. Parameter values are labelled **assumption**.

---

## D1 Event format

**Envelope v1.** The layout is binary, fixed-offset and little-endian. Midnight's persistent hash is SHA-256 (`L9:base-crypto/src/hash.rs:23`), and the event ID is `SHA-256` of the envelope without `rln.proof`.

| Field | Size | Visible to relays | Purpose |
|---|---|---|---|
| `version` | 1 B | yes | format version (start at 1) |
| `size_class` | 1 B | yes | body padded to 1, 4, 16 or 64 KiB |
| `ttl_class` | 1 B | yes | 0 = 1 h, 1 = 24 h, 2 = 7 d; nothing longer than 14 d |
| `shard` | 2 B | yes | coarse routing bucket, `H(topic_id) mod 2^k`; k = 4 at launch |
| `epoch` | 4 B | yes | `floor(unix_time / 60)` |
| `rln.root` | 32 B | yes | Registry membership root (must be inside the root window) |
| `rln.nullifier`, `rln.x`, `rln.y` | 3 × 32 B | yes | RLN-v2 internal nullifier and Shamir share (`2024-vac-rln-v2-spec`, "RLN-Diff flow") |
| `rln.ephemeral_pk` + `sig` | 32 + 64 B | yes | `x = H(ephemeral_pk)`; the body is signed with the ephemeral key (allows proofs to be computed ahead of time, see D5) |
| `rln.proof` | **unknown**, budget 4 KiB | yes | PLONK/KZG on BLS12-381; dropped by store nodes after anchoring |
| `clue` | ~68 B (**assumption**) | yes | S-FMD detection clue for the topic's detection key (`2022-penumbra-fmd`) |
| `body` | the class size | sealed | KEM header + AEAD ciphertext + padding |

**Sealed inside the body:** topic ID, schema ID, publisher pseudonym and signature (if the topic needs authorship), per-publisher sequence number, publisher timestamp, payload and padding. Relays see nothing that identifies the topic, the schema or the publisher.

- **Payload types.** Schema IDs are 32-byte hashes of a schema document. Two schemas are standard: `bus/ack` and `bus/key-update`.
- **Versioning.** An unknown `version` is dropped; an unknown schema is delivered opaque.
- **Lifetime.** `ttl_class` sets how long store nodes must keep the event. Relays drop an envelope whose `epoch` is more than 20 s from their clock, the gap Waku uses (`2024-revuelta-waku-latency` §2.5.1).
- **Why 14 days at most.** It matches Midnight's `global_ttl` of 1,209,600 s (`midnight-node/res/mainnet/ledger-parameters-config.json:176`), so the anchor ring and replay windows line up with the ledger.

**On-chain class.** For events that must sit on the ledger, the same sealed body is published with `emit(Misc{name, payload})`. The `name` is `H(shard‖epoch)` and the body is at most 256 B (`minokawa-compact/compiler/midnight-events.ss:17-74`). Larger bodies need MIP-0019 multipart events, which are still Proposed (`mip-0019-multipart-event.md:6`). This class needs ledger 9 (read-out §0.3).

---

## D2 Definition of "private"

| Property | Holds against | Mechanism |
|---|---|---|
| **P1 Content confidentiality** | everyone except key holders | AEAD under a topic key or a per-recipient KEM |
| **P2 Publisher anonymity** (event ↔ membership) | relays, store nodes, the indexer, chain observers | RLN zero-knowledge membership proof; anonymity set = members whose leaf is in a root still inside the window (`2022-vac-rln-v1-spec`, "Signaling") |
| **P3 Event-to-event unlinkability** for one publisher | same | a fresh nullifier per (epoch, message_id); holds unless the publisher double-signals, which reveals the secret by design |
| **P4 Subscriber-interest privacy** | relays and store nodes: interest hidden to shard level. Detection servers: they see a candidate set of size about p·N | full-shard download, or S-FMD with a protocol floor on p |
| **P5 Topic privacy** | relays, store nodes, chain observers | topic only inside the body; the visible shard is 1 of 2^k |
| **P6 Timing and volume privacy** | **partial**: a per-shard anonymity floor (D4) hides low-volume topics from relays | cover events from treasury-funded memberships |
| **P7 Relationship privacy** | follows from P2 and P4 | |

**Leakage table**

| Observer | Learns |
|---|---|
| Relay | shard, size class, TTL class, epoch, the IP of its direct peer, the timing of first sight. A Dandelion-style stem hides the publisher's IP from all but the first stem hop (`2018-fanti-dandelionpp`). |
| Store or detection node | everything a relay sees, plus which client fetched which shard. A detection server also sees the set of events matching a detection key, inflated by false-positive rate p, and can link sessions that reuse the same detection key. |
| Indexer | Registry state (membership commitments, bonds, anchors), which address registered and when, and which contract a client watches (`contractEvents` requires an address, read-out §4.3) |
| Chain observer | registration events with the NIGHT owner address that funded each bond (unshielded outputs are public, read-out §3.4), slash events, anchor roots, and the public `v_fee` of each transaction |
| Colluding minority (≤ 1/3 of relays plus one detection server) | stem-origin guesses for publishers whose first hop it controls; FMD candidate sets; who is online in each shard |
| Global passive observer | per-IP send and receive volume and timing. **P2 against a global observer is out of scope for v1.** Breaking the anonymity trilemma needs cover traffic and latency beyond this budget (`2017-das-trilemma`). |

**Out of scope:** endpoint compromise; whether an address registered at all (registration is public; use sponsored memberships to hide it); unlinkability against a global passive observer at the IP level; post-quantum confidentiality (the KEM can be a hybrid, but it is not required in v1); coercion.

---

## D3 Publish and subscribe model

**Topics.**
- A topic is a 32-byte `topic_id` plus a topic key and an FMD detection key pair, shared out of band (invite, contract metadata or wallet QR).
- Public-but-sealed topics, such as "events of contract C", derive `topic_id = H("bus-topic"‖contract_address‖label)`. Anyone who knows C can subscribe, but relays still cannot see the topic.
- Discovery is out of band, by design. The bus has no directory of topics.

**Publishing.**
1. The publisher picks a precomputed RLN proof for the current epoch.
2. It encrypts and pads the body, and signs it with the proof's ephemeral key.
3. It sends the envelope along a 2–4-hop stem of relays, after which it is flooded into the shard mesh (Dandelion++, `2018-fanti-dandelionpp`).

**Relays** check, in order:
1. The epoch is within ±20 s of the relay's clock.
2. The root is in the Registry root window.
3. The RLN proof verifies.
4. The nullifier has not been seen for this (epoch, message_id).
5. The event ID has not been seen.

Peers that forward invalid messages lose GossipSub P₄ score (`2020-gossipsub-v11-spec`, "P₄: Invalid Messages"). Two different `x` values under the same nullifier reconstruct the publisher's secret, and the relay that sees this files a slash (D4).

**Three ways to subscribe** (the protocol does not pick one):

| Mode | Who | Interest privacy | Cost to the subscriber |
|---|---|---|---|
| **S1 Shard relay** | agents and services | interest hidden to shard level | about 1.7 GB/day per shard (D5) |
| **S2 Shard download from a store node** (paid, anonymous credit tokens) | desktop wallets, intermittently connected agents | interest hidden to shard level; the store node sees the shard and the IP | same volume, pulled in batches |
| **S3 S-FMD detection** from a detection server, scoped to one shard | mobile wallets | the server sees about p·N candidates; protocol floor p ≥ 1/64 | about 27 MB/day at p = 1/64 (D5) |

The floor on p is enforced by the clue format (sender-side S-FMD with a consensus-set rate, `2022-penumbra-fmd`). The subscriber cannot choose it, because selfish users pick low false-positive rates and break FMD privacy for everyone (`2024-frank-anonymous-messaging-altruism`, abstract).

**Delivery semantics.**
- **Duplicates and replay.** Delivery is at-least-once; subscribers deduplicate by event ID, the same rule midnight-js gives for indexer streams (`midnight-js/packages/types/src/public-data-provider.ts:507-509`). Replay outside ±20 s is rejected; replay inside the window is deduplicated by nullifier.
- **Ordering.** There is no global order. Each publisher's order comes from the sealed sequence number. A cross-publisher partial order comes from anchors: (anchor index, leaf index).
- **Back-fill.** Events can be fetched from store nodes within the TTL class. After expiry they are gone unless a subscriber archived them.

**Contract consumption.** Contracts cannot read events or subscribe (read-out §5.4, constraint 12).
- Every 60 s an **anchorer** writes `R_t`, a Merkle root over all events it saw in epoch t across all shards, into the Registry's anchor ring. This is contract state, not an event, so contracts can check it on ledger 8 as well.
- A consuming contract exposes a circuit that takes `(event bytes, Merkle path, t)` as arguments. It checks the path against the anchor ring through a witness-free cross-contract call (Compact 0.33; the callee-has-no-witnesses restriction is satisfied: `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:98-104`) and then acts.
- Someone has to submit that transaction. The consuming contract sets a bounty, or the interested party pays its own DUST.

**Wallets** use S3, or S2 on desktop. The DApp connector has no event method (`midnight-dapp-connector-api/src/api.ts:70-203`); D8 proposes one.

**Agents** use S1 for low latency, or the indexer's `contractEvents` for the on-chain class (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:1971`).

---

## D4 Sustainable model (the decision I lead)

### D4.1 Facts that constrain any Midnight fee design

1. **DUST is shielded, non-transferable and only usable as gas** (`midnight-docs/docs/concepts/dust-architecture.mdx`, "DUST and network usage"). A user cannot pay a relay in DUST.
2. **Fees appear to be burned.** No path credits `v_fee` to any pool (`L9:ledger/src/dust.rs:469-474`; `L9:ledger/src/semantics.rs:583-1013`; this is the read-out's **inference**). Validators earn nothing from bus transactions, so they have no bus incentive and need none.
3. **DUST regeneration per NIGHT:** 8,267 Specks/Star/s × 10⁶ Stars/NIGHT = 8.267 × 10⁹ Specks/s = 8.27 × 10⁻⁶ DUST/s ≈ **0.714 DUST/day per NIGHT**, with a cap of 5 DUST per NIGHT (`ledger-parameters-config.json:164-168`). This agrees with the docs' 71 DUST/day for 100 NIGHT.
4. **Cost of a typical transaction at genesis prices (inference):** about 6 KB on the wire gives a block-usage term of 10 × 6,000 / 1,000,000 = **0.06 DUST**. Compute is about 0.001 normalised, which is below block usage, so block usage sets the fee (`L9:base-crypto/src/cost_model.rs:408-417`; read-out §7.3). Live prices move by up to about 4.6% per block.
5. **Contracts can hold and pay out unshielded tokens** (`sendUnshielded`, `receiveUnshielded`, `unshieldedBalanceGte`: `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1196-1244`). They can also mint shielded tokens (`mintShieldedToken`, `exports.md:1055`). So a Registry can hold bonds and a treasury.
6. **No rent exists** (read-out §7.5). Anything the bus writes into persistent state is a permanent cost for every node, so bus state must be bounded.

These facts give one rule: **DUST prices on-chain use; NIGHT, bonded or paid, prices off-chain use.**

### D4.2 Who pays and who earns

| Actor | Pays | Earns |
|---|---|---|
| **Publisher** | (a) a registration transaction (~0.06–0.3 DUST); (b) a refundable **bond** in NIGHT that sets its tier; (c) a **non-refundable registration fee** in NIGHT per 30-day term; (d) for the on-chain class, ~0.06 DUST per event | nothing |
| **Sponsor** (dApp, wallet vendor, agent operator) | the bond and fee for memberships whose commitments its users generate | the users it brings in (a business reason, not a protocol payment) |
| **Subscriber** | anonymous credit tokens for store downloads and detection, bought from each provider (`2026-draft-act`: partial spends with unlinkable change); S1 is free | nothing |
| **Relay** | bandwidth and CPU | **no protocol payment**; it relays because it publishes or subscribes. Relaying is the price of using the network, as in Waku (`2024-cornelius-waku-network-dapps` §III-E). |
| **Store node** | disk, egress, a bond, DUST for challenge responses | retrieval credits (market price) plus **audit-gated treasury rewards** |
| **Detection server** | CPU | credits (market price) |
| **Anchorer** | DUST for one transaction per minute, plus a bond | a flat **per-anchor reward** from the treasury |
| **Challenger** (anyone) | a small challenge bond plus DUST | a share of a slashed store or anchorer bond |
| **Validators** | include the bus's transactions | ordinary block-production economics only; the bus adds about 0.06% of chain transaction capacity (D5) |

**Treasury inflows:** registration fees; 50% of slashed bonds (the other 50% goes to the reporter); the launch grant.

**Treasury outflows:** anchor rewards, store rewards, audit bounties, and cover-traffic memberships.

**Rule:** the daily payout is `min(budget_d, balance / 365)`, so the treasury always shows at least one year of runway on-chain. This is checkable by anyone reading contract state.

### D4.3 Spam and abuse: the RLN-Diff membership

The parameters below are launch **assumptions**, to be set by governance.

| Tier | Events per 60 s epoch | Largest size class | Bond | Fee per 30 days |
|---|---|---|---|---|
| T1 | 10 | 4 KiB | 50 NIGHT | 2 NIGHT |
| T2 | 100 | 16 KiB | 500 NIGHT | 20 NIGHT |
| T3 | 1,000 | 64 KiB | 5,000 NIGHT | 200 NIGHT |

**How a membership works.**
- **Registration.** One Registry call that runs `receiveUnshielded(NIGHT, bond + fee)`. It inserts `transientHash(identity_secret)` and the tier into a `HistoricMerkleTree` (`minokawa-compact/doc/ledger-adt.mdx:603-`). This is the anonymous-membership pattern from `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:105-232`, extended with an epoch-scoped nullifier (**inference**). RLN-Diff hides the member's tier inside the proof (`2024-vac-rln-v2-spec`, RLN-Diff).
- **Slashing.** A double-signal reveals `a₀ = identity_secret` (`2022-vac-rln-v1-spec`, "Verification and slashing"). Anyone calls `slash(sk)`, which proves in zero knowledge that the leaf for `transientHash(sk)` is present, sends 50% of the bond to the caller and 50% to the treasury, and removes the leaf with `insertIndexDefault` (`ledger-adt.mdx:537-544`, "emulate a removal").
- **Withdrawal.** A delay of 7 days (**assumption**), longer than the 1 h root window plus a slashing-evidence window, so a double-signal found late can still be slashed.
- **The circuit must hash with Midnight's Poseidon** (`L9:transient-crypto/src/hash.rs:23,76`) so the contract can recompute commitments.

**Why RLN and not the alternatives.**
- **Not proof-of-work.** The cost falls on honest phones while spammers use stolen compute. Laurie and Clayton's arithmetic already needed at least 5.8 s of work per email to make spam unprofitable (`2004-laurie-proofofwork`). A mobile wallet cannot carry that, and Bitmessage's formula charges spammer and honest sender the same (`2015-schaub-bitmessage-antispam`).
- **Not per-event DUST.** Each event would then be a full ZK transaction: about 6 KB, seconds of proving, and a chain-wide ceiling of about 28 tx/s (D5).
- **Not Privacy Pass, ARC or ACT for publishing.** Those are keyed-verification schemes in which the issuer is the verifier, so every relay would need the issuer's key (`2025-draft-arc`; `2018-davidson-privacypass`). They are the right tool for paid services (store and detection), where issuer and verifier are the same operator.

**Capital comparison.** A T1 bond of 50 NIGHT forgoes up to 50 × 0.714 = 35.7 DUST/day of fee capacity. Bonded NIGHT held by a contract presumably generates no DUST for its owner (**inference**: generation needs a registered NIGHT key, `dust-architecture.mdx`, "Registration Table"). That DUST would pay for 35.7 / 0.06 ≈ 595 on-chain events per day. The same 50 NIGHT as a T1 bond allows 10 × 1,440 = 14,400 off-chain events per day. **The off-chain bus is about 24 times more capital-efficient per event**, which is why on-chain publishing is a premium class.

**Cost to flood the network** (launch target 100 events/s = 6,000 per epoch): 600 T1 memberships = 30,000 NIGHT locked, plus 1,200 NIGHT per 30 days in fees, and the publisher gets nothing extra for the spend. Bond price also adjusts dynamically: once a day, the bond per unit of rate is multiplied by `1 + (u − 0.5)/8`, where `u` = registered rate ÷ (κ × provisioned capacity) and κ = 10 is an overbooking factor (**assumption**). This copies the ledger's own rule of steering prices toward 50% fullness (`L9:base-crypto/src/cost_model.rs:354-405`).

**Spam on the retrieval side** is limited by credits: each request spends credit with the provider (`2026-draft-act`). The free tier is one ARC credential per membership, good for N presentations per day (`2025-draft-arc`).

### D4.4 What the treasury pays for, and how a payout is checked

| Work | Check | Payout rule |
|---|---|---|
| **Anchor** for epoch t | the Registry accepts the first anchor per epoch from a bonded anchorer chosen by stake-weighted round-robin for that slot; others are rejected | flat `A` NIGHT per anchor, set to cover 0.06 DUST × the price of NIGHT plus a margin |
| **Retention** | anyone may call `challenge(t, leaf_index)` with a 1-NIGHT challenge bond (**assumption**). The store node must answer with the leaf and its Merkle path before a block-time deadline (`blockTimeLt`, `exports.md:1261`); Compact checks the path. | Missed answer: the challenger gets 50% of the store bond. Answered: the challenger loses the challenge bond. Daily pool shared ∝ `capacity_i × pass_rate_i⁴`, **capped at 1/k of the pool per bond key** (k = 10 in phase O). |
| **Anonymity floor** | the treasury holds T2 memberships and publishes cover events so each shard carries at least λ_min = 1 event/s (**assumption**) | treasury cost = bandwidth only; no payout |

**What the treasury does not pay for:** relay forwarding and "uptime". Measured-performance rewards invite framing: in Nym, a few low-stake nodes dropping probe packets cut the cost of dominating the active set by more than 99% (`2026-cao-nymreputation`, §1). HOPR's per-hop payments also leak routing information (as `2021-diaz-nym` §2 argues).

**Operator funding shape.** This follows Nym's: a subsidy pool that falls over time plus a fee pool that grows (`2021-diaz-nym` §6, "mixmining rewards ... fees will overtake"). Here the launch grant pays out on a straight-line schedule over 36 months (**assumption**).

**Payment privacy.** Paying providers directly in NIGHT would link payer and provider on-chain. So the Registry mints a shielded **bus credit token (BCT)** 1:1 against NIGHT deposits and redeems it for NIGHT. Users pay providers in BCT through Zswap shielded transfers and receive ACT credits in return. Feasibility is an **inference** from `mintShieldedToken` and `receiveShielded` (`exports.md:1055-1102`); it has to be prototyped.

### D4.5 Behaviour at low and high load

- **Low load.** Fixed costs dominate: the foundation's relays and store nodes plus the anonymity floor. The cost is bounded: λ_min × 6 KiB × 16 shards ≈ 96 KiB/s per full relay. Fee income can be near zero, and the launch grant covers it. The treasury rule keeps the runway visible on-chain.
- **High load.**
  - Each member's rate is fixed by RLN, so total load can never exceed the registered rate.
  - Shards split by raising k once per-shard λ stays above 10 events/s for 24 h.
  - Bond prices rise with registered rate.
  - Under overload, relays shed the 64 KiB class first.
  - The on-chain class is protected by Midnight's own fee curve.

---

## D5 Performance requirements

**Assumptions:** mean body 2 KiB; RLN proof plus envelope header 4 KiB (proof size **unknown**); wire size S ≈ 6 KiB; GossipSub D = 8, D_low = 6, D_high = 12 (`2020-vyzovitis-gossipsub`, evaluation); per-node duplication upper bound ≈ D.

| Quantity | Launch target | Arithmetic |
|---|---|---|
| Network throughput | 100 events/s sustained, 1,000/s peak (with shard split) | |
| Per-shard rate | ≤ 10 events/s | k = 4, so 16 shards |
| **Shard relay** bandwidth (1 shard) | ≤ 4 Mbit/s each way | 10 × 6 KiB = 60 KiB/s = 0.49 Mbit/s, × 8 ≈ 3.9 Mbit/s |
| **Full relay** bandwidth (all shards, 100 events/s) | ≤ 40 Mbit/s each way | 100 × 6 KiB × 8 bit × 8 ≈ 39 Mbit/s |
| Full-relay CPU for RLN verification | 1–2 cores at 100 events/s | 2.7–18.7 ms per verification (`2024-revuelta-waku-latency` Table 1); Midnight's cost model gives about 3.3 ms + 4.6 µs per public input per proof (`ledger-parameters-config.json:124-133`) |
| Publish latency p50 / p99, relay subscriber | ≤ 1 s / ≤ 3 s | Waku measured ≤ 1 s for ≤ 25 KB with RLN (`2024-revuelta-waku-latency` §8); stem adds 2–4 hops. **Precomputed proofs take proving off the critical path.** |
| Latency to contract-consumable | ≤ 120 s at p99 | 60 s anchor interval + 6 s block + about 18 s finality (`mps-0028:36-38`) + indexer |
| On-chain class | ≥ proof time + 30 s | proving takes 5–30 s on a laptop for a Zswap spend (`mps-0004:33`) |
| S1 subscriber, one shard | 1.7 GB/day | stored body 2 KiB × 10 events/s × 86,400 s |
| S3 subscriber, one shard, p = 1/64 | 27 MB/day | 1.73 GB / 64 |
| Concurrent S3 subscribers per detection server | **unknown**; measure in phase 0 | FMD test cost per clue per key |
| Anchor load on the chain | 1,440 tx/day ≈ 0.06% of capacity | chain ≈ 10⁶ B / 6 KB ≈ 166 tx per block ≈ 27.8 tx/s ≈ 2.4 M tx/day |
| Anchorer's NIGHT for DUST | ~121 NIGHT | 1,440 × 0.06 = 86.4 DUST/day ÷ 0.714 |

**Precomputing proofs.** The RLN signal is `x = H(ephemeral_pk)`, not a hash of the message. The publisher's client therefore proves future (epoch, message_id) slots in the background, up to the 1 h root window. At publish time it only signs. Two distinct ephemeral keys in the same slot still reconstruct the secret, so slashing is unchanged (**inference**; this needs review by the cryptographers).

**OMR rejected as the default on cost.** OMR costs about USD 1.02 per million messages scanned **per recipient** (`2021-liu-omr`, cost section). At 100 events/s that is 8.64 M messages/day, about USD 8.8 per recipient per day. Even scoped to one shard it is about USD 0.88. OMR with strong unlinkability cannot cost less than PIR (`2026-fisch-unifomr`).

---

## D6 Storage requirements

| Node class | Retention | Storage | Arithmetic |
|---|---|---|---|
| Relay | ±20 s epoch window plus 24 h ID dedup | < 2 GB | nullifiers 32 B × 6,000 per epoch × 2; event IDs 32 B × 8.64 M/day = 276 MB |
| **Store node** (all shards) | by `ttl_class` | **≈ 28 GB** at 100 events/s, ≈ 283 GB at 1,000 events/s | 100 × 2 KiB × 86,400 = 17.7 GB/day. Assuming 90% at 24 h and 10% at 7 d: 15.9 + 12.4 = 28.3 GB. Proofs are dropped after anchoring because the anchor and the challenge game attest to admission (**inference**). |
| Detection server | 24 h of clues | < 1 GB | about 68 B × 8.64 M |
| Registry contract (persistent, unprunable) | permanent membership tree; **anchor ring of 20,160 slots** (14 days × 1,440) overwritten in place | ≈ 1.3 MB ring + tree | 20,160 × about 64 B. Overwrites count as churn, not net writes (**inference** from `ledger-parameters-config.json:159-160`). Bounded because there is no rent. |
| Indexer | anchor events (on ledger 9), Registry actions | negligible | 1,440 small events/day |

- **Availability guarantee:** within its TTL class, an event in an anchored root is retrievable from at least one bonded store node, or that node loses its bond. This is enforced by challenges, not promised.
- **Archival** past the TTL class is not a protocol duty. Publishers or subscribers keep their own copies.
- **On the ledger:** memberships, bonds, treasury, anchor ring and on-chain-class events. **Off the ledger:** everything else.

---

## D7 Infrastructure actors (the decision I lead)

| Actor | Admission | Trusted with | Paid by |
|---|---|---|---|
| Relay | permissionless; any node with the bus sidecar | forwarding only; it cannot forge membership | nobody (it relays because it uses the bus) |
| Store node | bond ≥ 2,000 NIGHT (**assumption**) with the Registry | availability within the TTL | credits + audited treasury share, saturation-capped |
| Detection server | permissionless; a reputation list kept off-chain | the FMD candidate set (sees about p·N of matching events) | credits |
| Anchorer | bond with the Registry; round-robin slots | inclusion and ordering claims; it can **omit** events, not forge them | per-anchor reward |
| Indexer (existing) | unchanged | sees which contracts clients watch | today, nothing (read-out §2.3) |
| Validators | unchanged | including Registry and anchor transactions | unchanged |
| Wallet providers | none | the S3 client and sponsoring members | their own business model |
| Registry maintainer | contract maintenance authority (`Maintain`, `L9:ledger/src/structure.rs:2987`) | parameters only. It **cannot move bonds** except by the coded slash and withdraw rules. | — |

**The path from launch to open participation.** Each gate is checkable from on-chain state plus a published measurement.

| Phase | Who operates | Moves to the next phase when |
|---|---|---|
| **L (launch, about 6 months)** | Foundation: ≥ 6 full relays in ≥ 3 regions, 2 store nodes, 1 anchorer, 1 detection server. Relaying is open to anyone from day 1. Maintenance key = foundation multisig with a 7-day timelock. | Phase-0 benchmarks pass (D10); ≥ 3 months without a Registry incident; ≥ 1,000 memberships |
| **O (open services)** | Bonded store nodes and anchorers admitted without permission; foundation nodes are capped by the same 1/k saturation rule as everyone else | ≥ 7 independent bond keys hold ≥ 75% of paid store capacity; no key > 1/k for 30 days; treasury runway ≥ 12 months with no grant draw for 90 days |
| **D (decentralised)** | Parameter control moves to on-chain governance (Midnight's Council and Technical Committee, `midnight-node/res/mainnet/federated-authority-config.json`, or a bus-specific vote); foundation nodes ≤ 10% of capacity | — |

**Saturation caps per bond key, not per real-world operator.** One operator can split across keys, a pattern the Nym measurements also found (`2026-cao-nymreputation`, Appendix D). This is a **residual risk**. Phase O publishes off-chain ASN and IP diversity reports. Stake-backed peer discovery (`2026-alpturer-aetherweave`) is the phase-D candidate for raising the cost of Sybil relays.

**My lean, made concrete.** Without paid store and anchor roles, the foundation's nodes would be the only store nodes forever. With them, an outside operator's revenue is `credits + capacity share × daily pool` and its cost is `disk + egress + bond opportunity`. Both sides can be read from published numbers before the operator joins.

---

## D8 Network tether

**Recommendation: hybrid sidecar.**
- A separate libp2p GossipSub process sits next to any Midnight node (or alone).
- It reads the Registry through the indexer or node RPC and submits Registry, anchor and slash transactions through the normal `send_mn_transaction` path.
- The read-out confirms a sidecar can attach with nothing in the node helping or forbidding it (read-out §8).

**Why not inside the node.** Midnight has no gossipsub (read-out §1.5). Adding a notification protocol needs a node fork that every operator runs, shares peer slots with consensus traffic (`midnight-node/node/src/service.rs:641`), and needs governance approval. A permissioned 10-validator set (read-out §2.2) should not be the bus's relays.

**Rejected:** off-chain workers and inherents (validator-only and not private; read-out §8); ledger-and-indexer-only as the primary design, which tops out at about 28 tx/s chain-wide, needs seconds of proving and ~0.06 DUST per event, and is public by construction.

**Fallback:** ledger plus indexer, using `emit(Misc)` ciphertext events with DUST as the stamp, at low volume. It needs ledger 9; on ledger 8 the fallback is contract-state writes at 0.2 DUST/KB (read-out §7.3).

**Changes to Midnight:**

| Component | Change | Needed for |
|---|---|---|
| Node | none | — |
| Ledger and runtime | none. Request: governance confirms that the BCT shielded-token pattern and contract-held NIGHT bonds are supported uses. | L |
| Indexer | none. Optional: a `Misc` name-prefix filter (`Misc` has no indexed fields today: `schema-v4.graphql:558-562`). | O |
| Compact | none. The RLN circuit is built with midnight-zk, and its Poseidon must match `transientHash`. | L |
| Wallet SDK | a bus client (S2/S3, proof precomputation, BCT and ACT credits) | L |
| DApp connector | add `subscribeBusTopic` / `publishBusEvent` (no event method exists today: `api.ts:70-203`) | O |

---

## D9 Threats and open risks

| Threat | Defence | Residual risk |
|---|---|---|
| **Spam within limits** | bonded rate, dynamic bond price, shard split, shedding the largest class | a well-funded attacker buys capacity; the cost is visible and rises with use |
| **Spam beyond limits** | RLN nullifier + slashing; P₄ peer scoring | slashing pays out only if a relay sees both signals; a split mesh can let some double-signals through |
| **Sybil relays and eclipse** | RLN-protected content, GossipSub v1.1 scoring and opportunistic grafting (`2020-gossipsub-v11-spec`), diverse bootstrap | eclipse of a lone subscriber is possible; S2 and S3 users depend on their provider |
| **Publisher deanonymisation** | ZK membership, Dandelion stem, precomputed proofs (no timing tell from proving) | first-hop observer plus timing; a global observer; a registration funded from an identifiable NIGHT address |
| **Subscriber deanonymisation** | shard-level download; S-FMD floor p ≥ 1/64 | the detection server learns candidates and can link sessions of one key; intersection attacks across days |
| **Replay** | ±20 s epoch window, nullifier set, event-ID dedup | none within the stated model |
| **Censorship by anchorers** | round-robin slots, several anchorers; contracts accept any root in the ring | a single-anchorer phase L can omit events; the 10 permissioned validators can censor Registry transactions; governance can pause `send_mn_transaction` (`midnight-node/runtime/src/check_call_filter.rs:40-45`) |
| **Store node lying** | challenges with bond slashing | an under-challenged node keeps its reward; foundation-funded random challenges in phase L |
| **Reward gaming** | pay only for anchors and passed challenges; no performance scoring | operators split across bond keys (D7) |
| **Key compromise** | topic-key ratchet per epoch (other designers decide the details); membership secrets kept in an encrypted local store | a stolen membership secret lets the thief spend or slash that member's bond; loss is limited to one bond |
| **Indexer abuse** | run your own indexer (standalone mode); the Registry is readable by node RPC too | public indexers see which contracts a client watches |
| **Governance and parameter abuse** | 7-day timelock; bonds movable only by coded rules | the foundation controls parameters in phase L |
| **DUST price spike** | anchorers hold buffer NIGHT; anchoring can stretch to 5 min under stress | contract-consumable latency grows |

---

## D10 Build and verification plan

**Phase 0 (8 weeks): measure before committing.**
1. RLN circuit in midnight-zk: proof size, proving time on a laptop and on a phone, verification time. **Acceptance:** proof ≤ 4 KiB, verification ≤ 10 ms on 1 core, background proving keeps up with 10 events/epoch on a laptop.
2. Agent-based economic simulation: memberships, flooding attackers, dynamic bond price, treasury runway at low and high load, store-node returns. **Acceptance:** a flood that costs < 30,000 NIGHT locked does not push p99 latency above 3 s; treasury runway stays ≥ 12 months under the grant schedule.
3. GossipSub simulation with 1,000 nodes, 16 shards and RLN validation delays, reproducing the method of `2024-revuelta-waku-latency`. **Acceptance:** the latency targets in D5.
4. **Quint model of the Registry**: bond, slash, withdraw, challenge, anchor ring, payout cap. **Invariants:**
   - total contract NIGHT = bonds + treasury + challenge escrow;
   - no withdrawal before the delay;
   - a slash is always possible inside the evidence window;
   - payout per key ≤ pool/k;
   - daily payout ≤ balance/365.

**Phase 1 (L):** Registry on testnet, then mainnet; foundation-run nodes; S1 and S2; BCT and ACT credits; public dashboard of every D7 gate metric.
**Phase 2 (O):** bonded store nodes and anchorers, challenge game, S3 detection, connector methods.
**Phase 3 (D):** governance hand-off; optional mixnet ingress.

**What would change course:**

| Evidence | Change |
|---|---|
| Midnight-native RLN proof > 8 KiB, or verification > 20 ms | use a Groth16 RLN verified off-chain (as Waku does); the Registry keeps commitments in a hash both systems support |
| Background proving cannot keep 10 events/epoch on a laptop | lower the T1 rate, or let a sponsor prove on the user's behalf (it learns membership timing, not content) |
| Treasury runway < 12 months in phase O with no grant draw | raise registration fees or cut λ_min; do not add a relay subsidy |
| Any bond key > 1/k of capacity for > 2 reward epochs, or the Nym-style cluster analysis shows > 33% under one operator | tighten bond minimums; consider stake-backed discovery |
| On-chain class demand > 1% of chain capacity | price it separately, or push it to anchors only |
| OMR cost < USD 0.01 per recipient per day per shard | offer OMR as S4 |

---

## Decision table

| Decision | Choice | Rejected | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Fixed binary envelope; 4 size classes; TTL ≤ 14 d; visible: shard, epoch, RLN fields, S-FMD clue; everything else sealed; on-chain class via `Misc` | variable sizes; visible topic; TTL > `global_ttl` | `ledger-parameters-config.json:176`; `midnight-events.ss:17-74`; `2022-penumbra-fmd` | medium | measured RLN proof size much above 4 KiB |
| D2 | P1–P7 as defined; not protected against a global observer; registration fact public | claiming unlinkability against a global observer | `2017-das-trilemma`; read-out §3.4 | medium | a cheap cover-traffic design within the bandwidth budget |
| D3 | Shard gossip; S1/S2/S3 subscription; contracts consume via the anchor ring plus a submitted call | OMR by default; contracts reading events; subscriber-chosen p | `2021-liu-omr`; `2024-frank-anonymous-messaging-altruism`; `toolchain-0.33.0.md:98-104` | medium | OMR cost falls ≥ 100× |
| **D4** | NIGHT-bonded RLN-Diff memberships with slashing; non-refundable fees + slashes + declining grant into a contract treasury; pay only for checkable anchors and retention; credits for services; DUST only for on-chain use | proof-of-work; per-event DUST; paying relays for performance; ACT/ARC for publishing | `dust-architecture.mdx`; `L9:ledger/src/dust.rs:469-474`; `2022-vac-rln-v1-spec`; `2024-vac-rln-v2-spec`; `2004-laurie-proofofwork`; `2026-cao-nymreputation`; `2021-diaz-nym` §6; `2026-draft-act` | medium | simulation shows bonded capacity cannot be priced against floods; contract-held NIGHT or the BCT pattern infeasible |
| D5 | ≤ 10 events/s per shard; 100 events/s network; p50 ≤ 1 s, p99 ≤ 3 s; proofs precomputed | per-event on-chain publishing | `2024-revuelta-waku-latency`; `2020-vyzovitis-gossipsub`; `mps-0004:33` | medium-low (proof costs unknown) | phase-0 benchmarks |
| D6 | Store node ≈ 28 GB at launch; bounded 20,160-slot anchor ring; proofs dropped after anchoring | unbounded anchor history in state; protocol archival | read-out §7.5; `bitmessage-guide.md:420-457` | medium | consumers need inclusion proofs older than 14 d |
| **D7** | Paid roles: store nodes, anchorers (bonded, audited, saturation-capped); relays unpaid; foundation launch → measured gates → governance | volunteer-only operation; validators as relays; reputation-scored rewards | `2021-diaz-nym`; `2024-cornelius-waku-network-dapps` §III-E; `2026-cao-nymreputation`; read-out §2.2 | medium | operators cannot cover costs at simulated prices; evidence that bond-key splitting defeats the caps |
| D8 | Hybrid sidecar overlay + Registry contract; fallback ledger/indexer `Misc` | node fork; off-chain workers or inherents; ledger-only | read-out §1.5, §8, constraint 10 | high | Midnight adds a generic gossip extension point |
| D9 | Threat table above; main residual risks: global observer, phase-L anchorer censorship, bond-key splitting | — | as cited | medium | red-team results |
| D10 | Phase 0 measurement + economic simulation + Quint Registry model, before mainnet | building before measuring proof costs | `2024-revuelta-waku-latency` method | high | — |
