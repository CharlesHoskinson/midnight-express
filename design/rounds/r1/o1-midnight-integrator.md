# Midnight Private Events (MPE): Round 1 proposal from the Midnight protocol integrator

## Summary of position

Build MPE as a **hybrid**. Bulk traffic travels on a dedicated libp2p overlay. Midnight is used only for what a ledger does well: membership, rate-limit roots, ordering and anchoring, plus a censorship fallback. The bus software is a sidecar ("bus node") that runs next to, not inside, `midnight-node`. It uses GossipSub v1.1 with Dandelion++ stems, fixed-size sealed envelopes, and recognition by keyed pseudorandom tags, with fuzzy-detection clues for first contact. Spam control is a rate-limiting nullifier (RLN). Its statement is written **as a Compact circuit** in a membership contract and proven with Midnight's own proof stack, so membership is paid in DUST and checked against a ledger Merkle root. An anchor contract records one batch root per window in a `HistoricMerkleTree` and emits one `Misc` event. That lets any Midnight contract consume a private event **privately**: the event stays a witness, and a cross-contract `checkRoot` reveals only a recent anchor root. The design runs on the ledger-9 / Compact 0.33 generation with **no mandatory change to the node, ledger, indexer or wallet**. Every upstream change I list is additive, and each has an owner. The fallback is ledger-plus-indexer only: multipart `Misc` events, which work today but are public metadata, expensive and slow. I reject putting the bus inside the node's network stack.

**Generation caveat.** Contract events, `emit`, cross-contract calls and the `contractEvents` subscription belong to ledger 9 / Compact 0.33. The node pins ledger 9.1.0.0-rc.5, but the support matrix lists `onchain-runtime-3.0.0` and toolchain 0.31.1 for mainnet (`notes/midnight-network-stack.md` §0.3; `midnight-docs/docs/relnotes/support-matrix.json:14,38,82`). Every on-chain part of this proposal therefore depends on ledger-9 activation. Its date is **unknown**; the node release team must confirm it.

---

## D1 Event format

**Envelope v1.** All fields are fixed-width big-endian. The envelope id is `id = SHA-256(header ‖ rln ‖ body)`, matching Midnight's persistent hash (`L9:base-crypto/src/hash.rs:23`).

| Field | Bytes | Visible to relays? | Purpose |
|---|---|---|---|
| `ver` | 1 | yes | Envelope version (1). Unknown versions are relayed if valid per the outer rules and dropped by endpoints. |
| `size_class` | 1 | yes | 0 = 1 KiB, 1 = 4 KiB, 2 = 16 KiB, 3 = 64 KiB body |
| `bucket` | 2 | yes | Shard, 0 to B−1 (B = 16 at launch) |
| `expiry` | 4 | yes | Minute index since bus genesis. Maximum lifetime is 14 days, the same as Midnight `global_ttl` = 1,209,600 s (`midnight-node/res/mainnet/ledger-parameters-config.json:176`). |
| `tag` | 16 | yes, pseudorandom | Keyed recognition tag (D3). Random bytes when unused. |
| `clue` | 68 | yes, pseudorandom | FMD2 flag ciphertext; 68 bytes for p = 2^-n up to n = 24 (`2021-beck-fmd` §1, p.3). Random bytes when unused, as Penumbra does with dummy clues (`2022-penumbra-fmd`). |
| `rln` | 4 + 32 + 32 + 32 + 4 + P | yes | Epoch, nullifier, share (x, y), membership-root index, proof (D4) |
| `body` | class size | sealed | HPKE (`2022-barnes-rfc9180`) or session ciphertext, padded to the class size |

Every envelope carries both a tag and a clue. A relay therefore cannot tell inbox traffic from topic traffic from cover traffic. The only visible distinctions are size class, bucket and expiry.

**Sealed inner frame** (after decryption): `kind` (topic-message, inbox-first-contact, session, ack-free receipt, cover), `topic_id` (32 bytes, never on the wire), `seq` (u64 per publisher per topic), `sent_at`, `schema` (32-byte hash of the schema), `publisher_auth`, `payload`, and the length of the zero padding.

`publisher_auth` comes in three variants:
- a JubJub Schnorr signature, which a Compact consumer contract can verify in-circuit (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:921-1010`);
- an MLS sender (`2023-barnes-rfc9420`);
- none, for anonymous publication, where authority comes from RLN membership alone.

Payload encoding is canonical CBOR with deterministic map ordering. This is an **assumption** chosen for its tooling; any canonical encoding works.

**Schemas.** A schema is identified by `SHA-256(schema text)`. Public schemas are registered in the on-chain registry contract (D3). Private schemas are agreed inside a topic.

**On-chain projection.** When an event goes to the ledger (anchor or fallback), it is a Compact `Misc { name: Bytes<32>, payload: Bytes<256> }`. `Misc` is the only custom event (`minokawa-compact/compiler/midnight-events.ss:71`). Bodies longer than 256 bytes use MIP-0019 multipart: one intent and one phase, preferably the guaranteed phase (`midnight-improvement-proposals/mips/mip-0019-multipart-event.md:64-76`). The `name` is a fixed protocol string such as `"mpe/anchor/v1"` or `"mpe/env/v1"`. The topic must never go in `name`, because the indexer exposes it in the clear (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:1125-1165`). I keep every on-chain event at 288 bytes or less. The ledger silently drops log data over 1 KiB (`MAX_LOG_EMITTED`, `L9:onchain-vm/src/vm.rs:41-43,268-276`), while Compact allows up to 512 KiB (`minokawa-compact/compiler/events.ss:33-37`). That mismatch is a hazard any design must avoid.

**Lifetimes.** The default is 7 days and the maximum is 14. Relays drop envelopes whose expiry is more than 14 days ahead or more than 5 minutes past.

**Rejected:**
- Bitmessage's variable-length objects up to 2^18 bytes (`design/evidence/bitmessage-guide.md`, protocol reference). Variable length leaks size.
- More than four size classes, because each class splits the anonymity set.
- Topic names in the clear.

## D2 Definition of "private"

**Properties:**
- **P1 Content confidentiality**: only key holders read the body.
- **P2 Topic privacy**: relays, store nodes, indexers and the chain do not learn which topic an envelope belongs to, or whether two envelopes share a topic.
- **P3 Subscriber-interest privacy**: an infrastructure party learns at most a bucket (1/B of traffic), plus the fuzzy set in delegated mode.
- **P4 Publisher unlinkability**: an envelope proves only "some current member, within quota". Two envelopes from one member in different epochs are unlinkable.
- **P5 Network-source privacy**: against a colluding fraction of relays, using Dandelion++ (`2018-fanti-dandelionpp` §3, which gives precision/recall bounds against a colluding fraction p).
- **P6 Session forward secrecy and post-compromise security**: X3DH/PQXDH followed by Double Ratchet for pairs (`2016-signal-x3dh-spec`, `2023-signal-pqxdh-spec`, `2016-signal-double-ratchet-spec`), and MLS for groups (`2023-barnes-rfc9420`).
- **P7 Size uniformity** within a class.

**Not provided at launch** (stated plainly):
- Timing and volume privacy against a global passive observer (GPA).
- Relationship anonymity against a GPA.
- Strong anonymity at low bandwidth and low latency at the same time. The trilemma says you get at most two (`2017-das-trilemma`).

A mixnet transport is Phase 3 (D10).

**Leakage table:**

| Observer | Learns | Does not learn |
|---|---|---|
| Single relay | Neighbour IPs; per-envelope arrival times, size class, bucket, expiry; RLN epoch and nullifier (one per member per epoch per slot); whether a neighbour was the first to send (weakened by the stem) | Content, topic, publisher identity, recipient, whether an envelope is cover |
| Store node | Above, plus which bucket a client reads, which envelope ids it fetches (hidden by k decoys, D3), and when | Topic, which fetches are real (up to 1/(k+1)) |
| Detection server (delegated FMD) | For each delegated client, the set of inbox envelopes whose clues match: true positives mixed with false positives at the client's rate p | Which matches are true. But Seres et al. show the server can recover much of the social graph when sender identities are known and p is small (`2021-seres-fmdfalsepositives` §1, contributions; p.3). FMD is therefore weak privacy and is used only for first contact. |
| Midnight indexer | Who subscribes to the anchor contract (every bus node, so this says nothing); membership registrations as commitments | Any per-topic interest. The contract address is the only required filter (`schema-v4.graphql:548-576`), and it is the same for everyone. |
| Chain observer | Anchor batch roots, per-batch counts, anchor timing; a membership commitment and the DUST `v_fee` per registration (`notes/midnight-network-stack.md` §3.4); for fallback-published envelopes, the ciphertext, size and time | The payer of the DUST, or which member is which. For contract consumption: which event, which batch, or which publisher, because only a recent anchor-tree root is revealed (D3). |
| Colluding minority of relays (fraction f) | First-spy source estimates, bounded by Dandelion++; partial eclipse of victims (D9) | Content or topic |
| Global passive observer | Who sends when, and how much, by correlating flows. Publisher-to-recipient links by timing unless cover traffic is high. | Content or topic, without endpoint compromise |
| A topic member | The plaintext. Other members by MLS sender identity if MLS-authenticated. | Non-members' traffic |

**Out of scope:** endpoint compromise; deniability; coercion; legal identity; censorship by the 10 permissioned validators beyond the fallback (D9); hiding the existence of bus software on a host.

## D3 Publish and subscribe model

**Addressing.** There are three recognition modes, and all of them use the one envelope type.

1. **Keyed topic** (one-to-many or group). Members share an epoch secret `k_e`, taken from the MLS epoch's exporter for groups, or from a topic key for broadcast topics.
   - Tag: `tag = HMAC-SHA-256(k_e, "tag" ‖ publisher_slot ‖ seq)[0..16]`.
   - Bucket: `bucket = H(k_e ‖ day) mod B`.
   - Subscribers precompute a window of the next W expected tags per publisher slot (W = 64), so recognition is one hash-table lookup per envelope. That replaces Bitmessage's trial decryption of every object (`design/evidence/bitmessage-guide.md`, "Recipient processing").
   - Tags are unlinkable without `k_e` (an **inference** from PRF security).
2. **Inbox** (first contact). The recipient publishes an inbox address: HPKE key, FMD public key, home bucket, and short-lived prekeys (X3DH/PQXDH). The sender fills `clue`. The recipient either scans its home bucket or delegates its FMD detection key. After first contact, both sides move to a keyed session (mode 1). FMD therefore covers only a small share of traffic, which limits Seres-style leakage.
3. **Public topic**. `tag = H("pub" ‖ topic_name ‖ day)[0..16]`. It is linkable by design, signed by the publisher, and suited to contract announcements and price feeds. It can be mirrored on chain.

**Discovery.** Public topics, schema hashes, bus bootstrap multiaddrs and inbox addresses that their owners chose to publish are recorded in a **Registry contract**. Its ledger `Map`s are public on purpose. Private topics are discovered only by invitation, delivered through an inbox.

**Subscribing without revealing interest.**
- A full node reads all buckets.
- A desktop light client downloads full buckets.
- A mobile light client downloads its buckets' **tag index**: `(id_prefix 8 bytes, tag 16 bytes)` per envelope. It then fetches the matched bodies with k = 4 decoy ids per real id.
- PIR retrieval, for example SimplePIR (`2022-henzinger-simplepir`), replaces decoys in Phase 3.
- I reject OMR at launch. Its detector cost is about 0.065 s per message *per recipient* (`2021-liu-omr`, p.2, "~$1.02 per million messages"). At 50 envelopes per second that is 3.25 core-seconds per second for each recipient.

**Delivery semantics.**
- Delivery is at-least-once. Endpoints deduplicate by `id`, mirroring the Midnight indexer's at-least-once streams, where consumers deduplicate by `id` (`midnight-js/packages/types/src/public-data-provider.ts:507-509`).
- There is no global order on the overlay. Per-publisher order comes from `seq` inside the sealed frame, and gaps are visible to subscribers.
- **Anchored order** is the batch order on chain: window W_a = 60 s, ordered by envelope id inside a batch.
- Replay defences: expiry, a seen-id cache for the expiry period, the RLN nullifier per epoch, and per-consumer nullifiers on chain.
- Back-fill: store nodes serve `(bucket, from_minute)` ranges for the retention window. Anchors let a client check completeness against the on-chain count.

**How a smart contract consumes an event.** Contracts cannot read events or subscribe (`notes/midnight-network-stack.md` §5.4, §9 item 12). An off-chain party, usually the beneficiary or an agent, submits a call. The pattern works on ledger 9 today:

```
// Anchor contract (deployed once, public)
export ledger anchors: HistoricMerkleTree<24, Bytes<32>>;   // leaves = batch roots
export circuit anchor(batchRoot: Bytes<32>, meta: Bytes<256>): [] {
  anchors.insertHash(disclose(batchRoot));
  emit(Misc { name: pad(32, "mpe/anchor/v1"), payload: disclose(meta) });
}
export circuit isAnchoredRoot(rt: MerkleTreeDigest): Boolean { return anchors.checkRoot(rt); }

// Consumer contract
witness eventBody(): EventFrame;           // decrypted inner frame, private
witness batchPath(): MerkleTreePath<16, Bytes<32>>;   // event id -> batch root
witness anchorPath(): MerkleTreePath<24, Bytes<32>>;  // batch root -> anchor-tree root
export circuit consume(anchorC: Anchor): [] {
  const ev = eventBody();
  assert(jubjubSchnorrVerify(trustedPublisherKey, hash(ev), ev.sig), "bad publisher");
  const rt = merkleTreePathRoot(anchorPath());   // also checks the batch-root leaf
  assert(anchorC.isAnchoredRoot(disclose(rt)), "not anchored");
  assert(!consumed.member(disclose(hash(ev.id ‖ domain))), "replay");
  consumed.insert(disclose(hash(ev.id ‖ domain)));
  ... act on ev, disclosing only what the business logic needs ...
}
```

The pseudocode illustrates the pattern. Exact Compact syntax and the hash used by `merkleTreePathRoot` must be matched in Phase 0. Why it fits Midnight:

- `checkRoot` on a `HistoricMerkleTree` accepts past roots (`minokawa-compact/doc/ledger-adt.mdx:603-615`). A proof built against a slightly stale anchor state stays valid after new anchors land. That is an **inference** from the ADT semantics; it must be tested against transcript replay.
- The callee `isAnchoredRoot` reads only ledger state and calls no witness, so it satisfies the 0.33 cross-contract restriction that callees have no private state (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:96-104`).
- Only `rt` and the consumer nullifier become public. The event, the publisher and the batch stay private. Using a `Set` of batch roots would reveal the batch, so I reject it.

The consumer nullifier reveals "some event was consumed now". Linkability across consumers is avoided by using a domain-separated hash.

**Wallet consumption.** The wallet SDK gains a bus light-client package. Bus keys (HPKE, FMD, RLN identity, MLS) are derived from the wallet seed on a new derivation path, so restoring a seed restores subscriptions. Wallets subscribe to their inbox bucket and their topics' buckets. The DApp connector currently has **no** event or subscription method (`midnight-dapp-connector-api/src/api.ts:70-203`). It needs an additive `bus` capability (D8, change U5).

**Agent consumption.** An agent runs a bus node, or a light client against store nodes. It reads anchors through `contractEventsObservable` on the anchor address, resuming with `fromId` (`notes/midnight-network-stack.md` §5.1). It submits consumer-contract calls through the normal wallet path.

## D4 Sustainable model

**Who pays for publishing.** Members register an RLN identity commitment in the **Membership contract** by calling `register(commitment, tier)`. The call pays an ordinary DUST fee and inserts the commitment into a `HistoricMerkleTree`.
- The fee is spent from shielded DUST, so the payer is hidden (`L9:ledger/src/dust.rs:469-474`).
- DUST cannot be transferred and is generated from NIGHT (`midnight-docs/docs/concepts/dust-architecture.mdx:23-25`). The real price of publishing is therefore holding NIGHT. That fits Midnight's model and needs no new token.
- Membership lasts one **membership period** of 14 days, which matches `global_ttl`. After that a new commitment is needed, which also bounds the size of the tree history.

**Rate limit.** RLN-v2 per-epoch limits apply (`2024-vac-rln-v2-spec` lines 111-130: `message_id` < `user_message_limit`). The epoch is 60 s. Tier 0 allows 10 envelopes per epoch; higher tiers need proportionally higher registration fees, set as a contract parameter. The RLN statement covers four things:
1. Membership against a membership root the relay accepts (the current root or the last 60 anchored roots).
2. `nullifier = H(a1)`, with `a1 = H(sk, epoch, message_id)`.
3. The share `y = sk + a1·x`, with `x = H(id)`.
4. `message_id` < limit.

Double-signalling reveals `sk` (`2022-taheri-waku-rln-relay` §III). Anyone holding the two shares can call `revoke(sk)`, which proves knowledge of the key and adds it to a revoked set that relays honour. At launch the cost of spam is one membership registration per exhausted identity. Slashing a locked stake is Phase 3. It needs the contract to custody NIGHT; whether Compact 0.33 supports that for unshielded NIGHT is **unknown**, so check the standard library before committing.

**Proof system choice (integrator decision).** Write the RLN statement as an exported Compact circuit of the Membership contract. Prove it with the standard proof server (`midnight-wallet/packages/prover-client/src/effect/HttpProverClient.ts:25`). **Never submit it as a transaction.** Relays verify the proof off chain with the ledger's verifier, against the verifier key stored in contract state. Benefits:
- No new trusted setup; it reuses the universal KZG SRS (`L9:transient-crypto/src/proofs.rs:108-128`).
- The same Poseidon and Merkle hashing as the ledger tree.
- Wallets, proof servers and tooling already exist.

Costs:
- The proof size P is **unknown**. A comparable membership-plus-nullifier proof, the DUST spend, is 2,912 bytes (`L9:ledger/src/dust.rs:2158`). The ledger estimates an unproven contract call at 4,832 bytes (`L9:ledger/src/structure.rs:619`). I plan with P = 3 KiB.
- Whether a contract-call proof can be verified outside a transaction through the public ledger API is **unknown**. This is the first Phase 0 spike.

Fallback: a dedicated RLN circuit in `midnight-zk` over BLS12-381 with Midnight's Poseidon. If that is still too large, use Groth16 over BLS12-381. Its proof is about 192 bytes (**inference**: two G1 points and one G2 point, compressed), at the price of a per-circuit ceremony.

**Who pays for carrying and storing.**
- **Launch:** operators carry traffic out of self-interest. Wallet providers need it for their users; dapps and agents need it for their own events. The Midnight Foundation (or an equivalent) funds seed relays and two store nodes. This mirrors the indexer today, which has no payment mechanism (`notes/midnight-network-stack.md` §2.3).
- **Phase 3:** store and detection services are paid with anonymous tokens bought with shielded tokens, on the Privacy Pass architecture (`2024-rfc9576-privacypass-arch`). The token, not the payment, authorises service, so payment cannot be linked to interest.

**Anchoring cost.** This is an **inference** at genesis prices, assuming all factors are 1.0 (`notes/midnight-network-stack.md` §7.3).
- An anchor transaction is about 7 KB: a call-proof estimate of 4.8 KB, a DUST proof of 2.9 KB, and the transcript. The block-usage term is 7,000 / 1,000,000 × 10 = 0.07 DUST.
- The persistent bytes of a `HistoricMerkleTree` insert are **unknown**. Planning with 1 KB gives 1,000 / 50,000 × 10 = 0.2 DUST.
- That is about 0.27 DUST per anchor. At 1,440 anchors a day it is about 390 DUST a day.
- One NIGHT generates up to 8,267 × 10^6 Specks per second, which is 0.714 DUST a day (`dust-architecture.mdx:91-111`; this assumes spending keeps the holder below the cap). About **550 NIGHT** therefore sustains anchoring.
- The `Misc` log is churn and costs almost nothing (`L9:onchain-vm/src/vm.rs:596-604`).

**Low load.** The anonymity set is small, and selfish users will not generate cover traffic (`2024-frank-anonymous-messaging-altruism`). Store and seed operators therefore emit cover envelopes so that each bucket carries at least 0.5 envelopes per second. That costs 16 × 0.5 × 5 KiB = 40 KiB/s for the whole network. Cover envelopes need valid RLN proofs, so operators hold memberships.

**High load.**
- Raise B from 16 to 64; nodes may then carry subsets.
- The registry contract can lower the tier-0 quota.
- DUST prices already rise automatically with block fullness, which affects registrations and anchors (`L9:base-crypto/src/cost_model.rs:354-405`).

## D5 Performance requirements

**Planning workload for Phase 1** (an **assumption** to validate): a sustained λ = 50 envelopes per second network-wide, with bursts of 250 per second for 60 s. The mean padded body is 2 KiB (classes 0 and 1 dominate). The mean wire size is 2 KiB + P (3 KiB) + about 220 B of header and RLN fields, roughly **5.2 KiB**.

| Node class | Requirement | Arithmetic |
|---|---|---|
| Bus relay (server) | Ingress ≥ 4.2 Mbit/s sustained, 21 Mbit/s burst; egress ≤ 6× unique ingress | Unique traffic is 50 × 5.2 KiB = 260 KiB/s = 2.1 Mbit/s. A duplication factor of 2× from mesh redundancy is an **assumption**; measure it, since GossipSub v1.2 IDONTWANT targets this (`2023-libp2p-gossipsub-v12`). Mesh degree D = 6 (`2020-gossipsub-v11-spec`, parameter table) bounds egress at about 12.5 Mbit/s. |
| Bus relay CPU | ≤ 0.3 core sustained, ≤ 1.5 cores burst, for RLN verification | Verification is about 3.27 ms + 4.56 µs per public input (genesis cost model, `ledger-parameters-config.json:124-133`). With about 20 inputs that is ~3.4 ms; with a cached verifier key, ~5 ms. 50 × 5 ms = 0.25 core. **Inference**: the cost model is a pricing model, not a benchmark. |
| Store node | Sustained ingest of 2.1 Mbit/s; serves 10,000 light clients | See D6 for storage. Egress: 10,000 clients × 13 MB/day (below) = 130 GB/day ≈ 12 Mbit/s. |
| Mobile light client | ≤ 15 MB/day; ≤ 1 s CPU per minute | The tag index is 24 B per envelope. 4 buckets × 50/16 envelopes per second × 24 B × 86,400 s ≈ 26 MB/day, so the tag index must be shortened to 12 B (an 8-byte tag plus a 4-byte index) for **13 MB/day**. Fetches: 100 real messages/day × 5 (with decoys) × 2.2 KiB ≈ 1.1 MB. |
| Desktop light client | One full bucket ≈ 1.3 GiB/day with proofs, 0.56 GiB/day stripped | 50/16 × 5.2 KiB × 86,400 s; stripped is 2.2 KiB. |
| Detection server (FMD) | 1 core per about 365 always-online delegated clients | If inbox clues are 10 % of traffic, that is 5 envelopes per second × 0.548 ms per test (`2021-beck-fmd` p.3) = 2.7 ms of CPU per second per client. |
| Anchor aggregator | 1 transaction per 60 s; one proof per minute | Proof times run from seconds to over a minute on consumer hardware (`midnight-docs/docs/tutorials/zk-loan/cli.mdx:302`), so it needs a server-class proof server. |

**Latency targets** (to be confirmed in simulation; these are targets, not measurements):
- Publish to 95 % of relays: p50 ≤ 2 s, p99 ≤ 10 s. This includes the Dandelion++ stem.
- Publish to a light client: p50 ≤ 5 s, p99 ≤ 30 s at a 5 s poll.
- Publish to anchored-and-visible in the Midnight indexer: p50 ≈ 30 s (half a window) + 12 s (inclusion) + 18 s (finality, [doc] `mps-0028-pre-finality-state-visibility.md:36-38`) ≈ **60 s**; p99 ≤ 180 s. The indexer serves finalized blocks only (`midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128-181`).
- Contract consumption end to end: p50 ≤ 3 min. It is dominated by proving, plus a second inclusion and finality.

**Fan-out.** Topics are not on the wire, so fan-out per topic costs nothing extra in the overlay. A topic with 10,000 subscribers costs the same as one with 1, except for MLS commit sizes (O(log n), `2023-barnes-rfc9420`).

**On-chain ceiling** for the fallback path: 1,000,000 bytes of block usage per 6 s block, shared with all traffic (`ledger-parameters-config.json:158`). At 0.01 DUST per KB, a 4 KiB fallback envelope costs about 0.04 DUST plus the call's proofs, about 0.1 DUST in total (**inference**). Ten such envelopes per block would use about 10 % of block bytes.

## D6 Storage requirements

| Location | What | Retention | Size |
|---|---|---|---|
| Relay | Seen-id cache and the GossipSub message cache | Expiry-bounded ids (16 B each) | 50/s × 14 d × 16 B ≈ 970 MB worst case; with a 7-day default, ≈ 480 MB |
| Store node | Bucket envelopes; proofs stripped after verification and anchoring (the anchor commits to `id`, which includes the proof hash, so a later reader can still check the proof against an archive) | Default 7 days, maximum 14 | Stripped: 50 × 2.2 KiB × 604,800 s ≈ **63 GiB** for 7 days, 127 GiB for 14. Unstripped: 150 / 300 GiB. |
| Archive (optional) | Full envelopes of anchored batches | Indefinite, by choice of the archive operator | 21 GiB/day unstripped |
| Midnight ledger | Membership commitments; anchor-tree leaves; revoked set; registry `Map`s | Contract state persists indefinitely with no rent (`notes/midnight-network-stack.md` §7.5). The design bounds it with periodic resets of the tree history. | Unknown bytes per insert; at a planning 1 KB, 1,440 anchors/day is ~1.4 MB/day, plus registrations |
| Midnight indexer | 1,440 `Misc` events/day | Indexer policy | About 1,440 × (288 + ~150 index bytes) ≈ 0.6 MB/day (the index-row size is from `mip-0002...md:508-540`). Negligible next to MIP-0002's upper bound of 703 MB/day. |
| Light client | Keys, MLS and ratchet state, tag windows, the last 14 days of its own messages | Device policy | < 50 MB (**assumption**) |

**Availability guarantee.** An anchor proves an envelope *existed* at a minute. It does not prove the envelope is *available*. Availability is best effort: at least two independent store nodes per bucket in Phase 1, measured by a public probe. A publisher that needs the message to survive can self-archive, or can republish through the fallback (on chain, so as available as the chain).

**What lives on the ledger:** membership, quotas, revocations, anchors, registry entries, fallback envelopes. Bodies are never on the ledger except in the fallback.

## D7 Infrastructure actors

| Actor | Admission | Trusted with | Paid by | Launch → end state |
|---|---|---|---|---|
| Bus relay | Permissionless. Peers are scored with GossipSub v1.1 (`2020-gossipsub-v11-spec`). Bootstrap comes from Registry entries signed by operators. | Availability only | Self-interest; Phase 3 tokens | Foundation and FNO-run seeds, then an open set with diversity rules |
| Store node | Registry entry | Availability; sees bucket and fetch patterns | Foundation and wallet providers; Phase 3 Privacy Pass tokens | 2 nodes, then ≥ 5 independent operators per bucket |
| Detection server | The client chooses it | FMD detection keys (fuzzy interest) | Wallet providers | Phase 3: multi-server FMD (`2025-goes-multiserverfmd`), so no single server holds a usable key |
| Anchor aggregator | Permissionless. Anyone can anchor, so "anchored" means only "existed by then"; authenticity is checked by consumers. | Nothing except timeliness. Withholding is detectable, and publishers can self-anchor. | Its own NIGHT-backed DUST (~550 NIGHT) | Foundation, then several competing aggregators |
| Midnight validators | Unchanged (10 permissioned at genesis, `midnight-node/res/mainnet/system-parameters-config.json:6-9`) | Ordering anchor and registration transactions; can censor them | Existing | Unchanged; benefits from SPO decentralization |
| Midnight indexer operators | Unchanged | They see that a client follows the anchor contract, which everyone does | Existing | Unchanged |
| Wallet providers | — | They run light clients locally. A provider-run store or detection service is optional. | — | — |
| Agents | Run a bus node or light client | Their own keys | Their own business | — |

The bus node **may co-locate** with a Midnight full node, indexer or RPC node. It uses the node's RPC or the indexer for chain reads, and normal transaction submission for writes (`notes/midnight-network-stack.md` §8, "Independent P2P sidecar").

## D8 Network tether (lead decision)

**Recommendation: Hybrid with a sidecar overlay.** A separate libp2p overlay carries the bulk traffic. The Midnight ledger handles membership, rate-limit roots, anchoring, ordering and the fallback. The Midnight indexer is the read path for anchors.

**Why not inside the node's network stack:**
1. There is no plugin mechanism. A new notification protocol needs a custom node binary that every operator runs (`midnight-node/node/src/service.rs:586,607-608,644`).
2. Peer slots are shared with consensus traffic (`service.rs:641`).
3. The stack has no gossipsub; `sc-network-gossip` is used only by GRANDPA and BEEFY and has single 32-byte topics (`midnight-node/Cargo.lock:14548`; `notes/midnight-network-stack.md` §1.5).
4. Bulk private traffic on validator links mixes consensus liveness with a spam surface.
5. A mesh of 10 permissioned validators plus the full nodes is a small, known topology, which is poor for anonymity.

Adding a node protocol later gains nothing the sidecar lacks.

**Why not ledger and indexer alone:**
- Every byte is public metadata: contract, size, time and frequency (MIP-0019 security considerations, lines 126-128).
- Capacity is capped by 1 MB blocks.
- Each post costs a fee and a proof.
- Latency is at least one block plus finality.
- Governance can pause `send_mn_transaction` (`midnight-node/runtime/src/lib.rs:321`; `check_call_filter.rs:40-45`).

It remains the **fallback**: publication and rendezvous that survive a broken overlay.

**Why not overlay alone:** it would lose a fee-backed Sybil cost (DUST), a common clock and order, and above all contract consumption. None of these can be faked off chain.

**Upstream change register.** Nothing below is required for Phase 1 except U0.

| # | Change | Required? | Owner |
|---|---|---|---|
| U0 | Activate ledger 9 / Compact 0.33 on mainnet (`emit`, `contractEvents`, cross-contract calls) | **Yes** for anchors through `emit` and for contract consumption | Midnight node and ledger release team; governance |
| U1 | A public, supported API in `midnight-ledger` to verify a contract-circuit proof outside a transaction, given a verifier key and public inputs | Required for Compact-RLN; otherwise use the `midnight-zk` fallback | Ledger team |
| U2 | Make the event size limits agree: the Compact `max-emit-size` of 512 KiB against the VM's silent drop above 1 KiB. Make the compiler reject events over 1 KiB, or make the VM fail loudly. | Safety; MPE stays at ≤ 288 B | Compact compiler team and ledger team |
| U3 | Accept MIP-0019 (multipart `Misc`) | Fallback bodies over 256 B; otherwise MPE defines its own framing | MIP editors; the author |
| U4 | Indexer: an exact-match filter on `Misc.name` (`miscNames: [HexEncoded]`) | Nice to have. Today a dedicated contract address suffices, since `fieldPrefixes` works on standard events only (`schema-v4.graphql:558-562`). | Indexer team |
| U5 | DApp connector: an optional `bus` capability (`getBusInbox`, `subscribeTopic`, `publish`, `exportTopicInvite`), with keys held by the wallet | Phase 2 | DApp connector API maintainers; wallet team |
| U6 | Wallet SDK: a bus key derivation path and a light-client package | Phase 2 | Wallet team |
| U7 | Promote `contractEvents` out of `@beta`, and publish a capacity benchmark (none exists, `notes/midnight-network-stack.md` §4.7) | Before mainnet GA of MPE | Indexer team |
| U8 | Compact: lift the cross-contract restriction on callee witnesses | Not needed (`checkRoot` uses no witness) | — |
| U9 | Node-side event visibility (MPS-0007, Proposed) | Not needed. It would let light consumers avoid the indexer for anchors. | Node team |
| — | Node networking, pallets, inherents, off-chain workers | **No change.** I reject them (`notes/midnight-network-stack.md` §8). | — |

## D9 Threats and open risks

| Threat | Defence | Residual risk |
|---|---|---|
| Eclipse of a relay or light client | GossipSub v1.1 scoring with `D_out` outbound quotas (`2020-gossipsub-v11-spec` §"Outbound Mesh Quotas"); bootstrap diversity from the Registry; light clients use ≥ 2 store nodes from different operators; on-chain anchor counts reveal withheld traffic | A low-resource eclipse remains possible against weakly connected nodes (`2018-marcus-ethereumeclipse`); detection depends on anchors, not prevention |
| Sybil relays | Scoring; IP-group diversity; relays have no special authority | Many Sybils raise first-spy precision |
| Spam / flooding | RLN with a DUST-priced membership; tags and clues cost nothing to relays; proofs are verified before forwarding | The cost of spam equals the registration fee. If DUST prices fall, spam gets cheaper. Governance can raise the tier price. |
| Publisher deanonymization (network) | Dandelion++ stem (`2018-fanti-dandelionpp`); fixed size classes; cover floor | A GPA defeats it. Mixnet transport is Phase 3 (`2017-piotrowska-loopix`, `2021-diaz-nym`). |
| Publisher deanonymization (registration) | Fees are paid in shielded DUST; anonymity set is the whole membership tree | Timing between registration and first use; mitigated by recommending a delay. Small trees at launch. |
| Recipient deanonymization via a detection server | FMD only for first contact; p ≥ 2^-4 recommended | Seres-type graph recovery (`2021-seres-fmdfalsepositives`); delegation has a privacy price (`2026-cinal-viewingkeycompromise`) |
| Statistical disclosure over time | Ack-free receipts by default; no automatic delivery receipts | Repeated patterns still leak, as with sealed sender (`2021-martiny-sealed-sender`: about 5 messages with receipts on) |
| Replay | Expiry; id cache; RLN epoch nullifier; consumer-contract nullifiers; Midnight's own intent replay protection for transactions (`midnight-ledger/spec/intents-transactions.md:131`) | None material |
| Censorship by validators | Overlay traffic does not touch validators; anchors can be resubmitted by any aggregator | Ten permissioned validators with predictable Aura leaders (`midnight-node/runtime/src/lib.rs:292`) can censor anchors and registrations. Governance pause can stop all of them. |
| Aggregator withholding or equivocation | Permissionless anchoring; publisher self-anchoring; anchors carry counts | Delays of up to one window per honest aggregator |
| Key compromise | Ratchets and MLS give forward secrecy and post-compromise security; short-lived inbox prekeys; PQ hybrid in Phase 3 (`2023-signal-pqxdh-spec`, `2026-bao-anonymity-xwing`) | First-contact messages to a compromised long-term inbox key, as in Bitmessage's static-key problem (`design/evidence/bitmessage-guide.md`, "Cryptography") |
| RLN secret leak from a buggy client | Revocation | Loss of membership; the published messages stay unlinkable to identity unless `sk` links to registration timing |
| Indexer abuse | The only indexer dependency is the anchor contract stream, which every node follows | The indexer can withhold anchors; mitigated by ≥ 2 indexers or a self-run standalone indexer |
| Parser and endpoint RCE | Memory-safe parsers; a closed schema registry; no dynamic dispatch on decrypted content (the Bitmessage `eval()` lesson, `design/evidence/bitmessage-guide.md`, "Security incident") | General software risk |
| Dependence on unshipped upstream work | Phase gates (D10) | Ledger-9 slip blocks contract consumption |

## D10 Build and verification plan

**Phase 0, about 8 weeks: spikes and models.**
1. **Compact-RLN spike.** Write the circuit, then measure the proof size P, proving time on the proof server and on a laptop, and verification time. Prove that U1 is achievable.
2. **Anchor and consumer spike on a ledger-9 devnet.** Measure the bytes written by a `HistoricMerkleTree<24>` insert, the anchor fee and the transaction size. Show that `checkRoot` still passes after new inserts between proving and inclusion.
3. **Quint model** of the anchor, membership, revocation and consumer-nullifier logic. Invariants: no double consumption; no consumption of an unanchored event; revocation is monotone.
4. **Network simulation** with 1,000 nodes (GossipSub + Dandelion++ + RLN validation delay). Report latency percentiles, the duplication factor and first-spy precision at colluding fractions of 5, 10 and 20 %.
5. **FMD privacy simulation** in the style of Seres et al., on synthetic first-contact graphs.

**Phase 1: overlay MVP on testnet.** Bus node, store node, tags, inbox with HPKE + X3DH, RLN, anchors, Registry, a TypeScript client library.

**Phase 2: integration.** Consumer-contract SDK and templates, DApp connector `bus` capability (U5), wallet integration (U6), MLS groups, detection servers, mainnet beta after U0 and U7.

**Phase 3: hardening.** Privacy Pass-paid services, multi-server FMD, PIR retrieval, an optional mixnet transport, PQ hybrid sessions, stake slashing.

**Acceptance criteria for Phase 1 exit:**
- At 50 envelopes per second for 24 h on 200 testnet relays: p99 delivery to 95 % of relays ≤ 10 s; relay CPU ≤ 0.3 core; ingress ≤ 5 Mbit/s.
- Zero accepted envelopes beyond quota in an adversarial spam test with 1,000 Sybil identities.
- Anchored visibility p50 ≤ 60 s.
- 100 % of 10,000 consumer-contract calls succeed against anchors up to 1 hour old.
- A light client stays under 15 MB/day.
- The first-spy precision of a 10 % colluding set is within 1.5× of the Dandelion++ analytical bound.

**Evidence that would change course:**
- **P > 6 KiB, or verification > 10 ms.** Switch to the dedicated `midnight-zk` or Groth16 RLN circuit.
- **An anchor costs > 2 DUST** (a `HistoricMerkleTree` insert writes too many bytes). Anchor every 5 minutes, or keep a rolling `Map<epoch, root>` with a privacy cost.
- **Ledger 9 not active on mainnet by Phase 2.** Keep the overlay and drop contract consumption.
- **`checkRoot` transcripts fail under concurrent anchoring.** A Compact or ledger change is needed (escalate to the Compact team).
- **The FMD simulation shows > 30 % edge recovery at p = 2^-4.** Drop delegated FMD and require full-bucket inbox scanning.
- **The duplication factor > 4×.** Adopt GossipSub v1.2 IDONTWANT or switch topology.

---

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Format | One fixed envelope: visible version, size class (1/4/16/64 KiB), bucket, expiry, 16 B tag, 68 B clue, RLN fields; HPKE- or session-sealed body; 7-day default and 14-day maximum life; on-chain projection as ≤ 288 B `Misc`, multipart per MIP-0019 | Variable sizes (Bitmessage); topics in the clear; >4 classes; on-chain events >1 KiB | `2021-beck-fmd` p.3; `2022-penumbra-fmd`; `L9:onchain-vm/src/vm.rs:41-43`; `midnight-events.ss:71`; `mip-0019:64-76` | Medium | A measured P that makes the 1 KiB class pointless |
| D2 Privacy | P1–P7 as defined; no protection against a GPA or for timing at launch; explicit leakage table | Claiming "untraceable"; relying on FMD for all recipient privacy | `2017-das-trilemma`; `2021-seres-fmdfalsepositives`; `2018-fanti-dandelionpp`; `notes/midnight-network-stack.md` §3.4 | High | A cheap cover/mix design that meets the D5 budgets |
| D3 Pub/sub | Keyed PRF tags for topics, FMD clues only for first contact, public tags for public topics; buckets; tag-index plus decoy retrieval; contract consumption by witness + Merkle paths + cross-contract `checkRoot` + consumer nullifier | Trial decryption of everything; OMR at launch; a `Set` of batch roots; on-chain subscription | `ledger-adt.mdx:603-615`; `toolchain-0.33.0.md:96-104`; `2021-liu-omr` p.2; `api.ts:70-203` | Medium | `checkRoot` transcript instability; PIR becoming cheaper than decoys at mobile scale |
| D4 Sustainability | DUST-priced RLN membership (Compact circuit, proven off chain); revocation on double-signal; Foundation-funded seeds at launch; Privacy Pass-paid services later; operator cover floor | Bitmessage-style PoW; a new token; per-envelope on-chain fees | `2022-taheri-waku-rln-relay`; `2024-vac-rln-v2-spec`; `dust-architecture.mdx:91-111`; `2024-frank-anonymous-messaging-altruism`; `2024-rfc9576-privacypass-arch` | Medium | A Phase 0 P or verification cost far above plan; DUST prices too low to deter spam |
| D5 Performance | 50/s sustained, 250/s burst; relay ~2.1 Mbit/s unique, ≤ 0.3 core; mobile ≤ 13–15 MB/day; anchored p50 ≈ 60 s; overlay p99 ≤ 10 s | Full-flood mobile clients; OMR detection | Arithmetic in D5; `ledger-parameters-config.json:124-133`; `2020-gossipsub-v11-spec` | Low–medium (P and the duplication factor are unmeasured) | Phase 0 measurements |
| D6 Storage | Store nodes keep 7 days by default (14 maximum), stripping proofs after anchoring (~63 GiB); ledger holds only membership, anchors, registry and fallback; indexer load ~0.6 MB/day | Bodies on the ledger; indefinite relay retention | `notes/midnight-network-stack.md` §7.5; `mip-0002:508-540`; `ledger-parameters-config.json:176` | Medium | Bytes per `HistoricMerkleTree` insert; a demand for long archives |
| D7 Actors | Permissionless relays and aggregators; registry-listed store nodes; client-chosen detection servers; validators and indexers unchanged; Foundation-seeded launch moving to independent operators | New validator duties; a permissioned relay set as the end state | `notes/midnight-network-stack.md` §2, §8 | Medium | Operators unwilling to run store nodes without payment before Phase 3 |
| D8 Tether | **Hybrid with a sidecar overlay** (libp2p GossipSub + Dandelion++) plus Midnight ledger anchoring and membership, with the indexer as read path; fallback: ledger + indexer only. Only mandatory upstream item: ledger-9 activation (U0); U1–U7 additive, each with an owner. | Inside midnight-node (fork, shared peer slots, consensus risk); ledger only (public, costly, capped); overlay only (no Sybil cost, no contract consumption) | `service.rs:586-644`; `Cargo.lock:14548`; `check_call_filter.rs:40-45`; `schema-v4.graphql:548-576`; `notes/midnight-network-stack.md` §8–9 | High | Midnight shipping a node plugin system with separate peer sets, or MPS-0007 plus pre-finality visibility making a node-native read path cheap |
| D9 Threats | Scoring and diversity against eclipse and Sybil; RLN against spam; Dandelion++ and padding against deanonymization; layered replay defences; fallback and multiple aggregators against censorship; ratchets and MLS against key compromise | Claiming defence against a GPA; trusting one detection server | Table in D9 and the cited slugs | Medium | Simulation showing first-spy precision far above the bounds |
| D10 Plan | Phase 0 spikes (Compact-RLN, anchor costs, Quint model, 1,000-node simulation, FMD simulation), then MVP, then integration, then hardening; numeric exit criteria and pivot triggers | Building before measuring P and insert costs | D10 | High | — |
