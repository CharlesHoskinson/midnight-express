# Midnight Private Events: Round 1 proposal (consumer and developer experience; lead for D3)

## Position summary

I propose one envelope format, one consumer API and one set of delivery rules, released in phases. **Phase 1 uses only the Midnight ledger and the indexer** (the "anchored lane"). Sealed envelopes are published as `Misc` contract events on a few shared bus contracts and read through the indexer's `contractEvents` stream. Recipients recognise their events by 32-byte pseudorandom tags derived from per-stream keys, so matching is a hash-table lookup and not trial decryption. Phase 2 adds an off-chain **fast lane**: a separate libp2p/GossipSub sidecar with RLN rate limiting that carries the same envelope. The consumer API stays the same and each event is labelled `final` or `gossip`. Every consumer gets the same contract:

- events arrive **finalised and at least once**;
- they are **totally ordered by chain position**;
- they are **numbered per stream**, so gaps can be detected;
- a consumer can **resume from a portable, chain-anchored cursor**;
- a stored-events boundary marker says when the consumer has caught up, as Nostr's `EOSE` does.

Smart contracts cannot read events. They react through a **relayed proof of publication**: the recipient submits the plaintext as a private witness, the contract checks a Merkle anchor kept by the bus contract, and a consumed-nullifier gives an exactly-once effect. I reject Bloom filters, fuzzy message detection and PIR/OMR for Phase 1. They are clever, but they fail my test: a developer cannot use them correctly in an afternoon, and two of them leak more than they appear to. The default subscriber mode downloads the whole bus stream. At the Phase-1 target load I estimate about 50 MB per day for one subscriber, which agents and servers can afford. Mobile clients use an explicit, documented bucket mode that leaks a small, stated amount.

---

## D1 Event format

**Lane A carrier (Phase 1).** Each event is published as one `Misc` contract event, or as several. The 32-byte `name` field holds the routing **tag** and the 256-byte `payload` field holds one **part**.

- `Misc` is the only custom-data event type. Its size is fixed at `{name: Bytes<32>, payload: Bytes<256>}` (`minokawa-compact/compiler/midnight-events.ss:71-74`).
- Multi-part events follow MIP-0019. The reader groups events by transaction and physical intent and concatenates them in ledger emission order (`midnight-improvement-proposals/mips/mip-0019-multipart-event.md:64`). The publisher must keep all parts in one execution phase, and the SDK uses the guaranteed phase (`mip-0019:70-76`). MIP-0019 is still *Proposed*, so the SDK implements the reader rule itself and does not depend on activation.
- The SDK never emits more than one 256-byte part per `emit`. The ledger-9 VM **silently drops** log items over `MAX_LOG_EMITTED` = 1 KiB (`notes/midnight-network-stack.md` §3.2, citing `L9:onchain-vm/src/vm.rs:41-43, 268-276`; I did not re-read the L9 archive myself). That silent drop is the most dangerous failure for consumers, and fixed-size parts rule it out.

**Size classes.** Fixed sizes hide the true length and keep circuits fixed.

| Class | Parts | Bytes on chain (name + parts) | Usable sealed body |
|---|---|---|---|
| S | 1 | 32 + 256 | 256 − 49 (header and tag) = **207 B** |
| M | 4 | 32 + 1,024 | **975 B** |
| L | 16 | 32 + 4,096 | **4,047 B** |

Anything larger travels as an off-chain blob, referenced inside the sealed body by `(sha256, key, locator)`. In Phase 1 the blob store is the application's choice and is out of scope.

**Public layout (visible to nodes, indexers and chain observers):**

```
name[32]    = tag                     (pseudorandom; see D3)
part0[0]    = v (protocol version, 0x01)
part0[1]    = vt (1-byte view tag; only meaningful for first-contact; random otherwise)
part0[2..34]= ek (32 B: Elligator2-encoded X25519 ephemeral key for first-contact, random nonce otherwise)
part0[34..] ‖ part1.. = AEAD ciphertext ‖ 16-byte tag, padded to class
```

Ordinary stream events and first-contact events have the same layout, so an observer cannot tell them apart. The one exception is the bucket byte described in D3.

**Sealed body.** It is encoded as deterministic CBOR (a design choice; no evidence needed):

| Field | Purpose for consumers |
|---|---|
| `stream_seq: u32` | Per-publisher sequence number. Gives per-stream order, gap detection and dedup. |
| `prev_skip: u32?` | Publisher's statement that sequence numbers up to `prev_skip` were abandoned. Lets consumers close a gap and stop waiting. |
| `schema: (id: 8 B, ver: u16)` | `id` is a truncated hash of the application schema definition. Unknown schemas are delivered as `undecodable`, never dropped. |
| `expires_at: u32?` (block height) | Advisory logical expiry. The SDK hides expired events by default and counts them. |
| `binding: 32 B?` | Commitment for contract consumption (see D3): `persistentHash(event_secret ‖ action_digest)`. |
| `sig: 64 B?` | Publisher signature (Jubjub Schnorr so contracts can verify it in-circuit; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:921-1010` per the read-out §6.1). Required on authenticated multi-publisher streams. |
| `body` | Application data. |

**Identifiers.**

- `eid = SHA-256(tag ‖ parts)` is a **portable** envelope ID. It is the same on both lanes and on every indexer, and it is the dedup key.
- `cursor = (height, tx_index, log_index)` is a **portable** position.
- I do **not** expose the indexer's `id` as the cursor. That `id` is assigned by each indexer deployment (`schema-v4.graphql:1127-1129`). Production runs two instances behind one hostname and re-indexes the secondary from empty (`midnight-indexer/docs/re-indexing.md:78-95`). Whether `id` values match across instances is **unknown**. The test is to diff `contractEvents` IDs between primary and secondary. If they differ, an `id` resume through a load balancer can skip or repeat events. The SDK translates a portable cursor into `fromBlock` and then skips forward locally.

**Lifetime.** Lane A events live as long as the chain's block history, because the indexer can rebuild them by re-execution (`midnight-indexer/docs/architecture.md:15-19`). The guarantee that matters to consumers is about *keys*, not storage (see D6). Lane B events have a 24-hour store TTL (Phase 2).

**Versioning.** The public `v` byte selects the envelope and cipher suite: v1 is X25519, HKDF-SHA-256 and ChaCha20-Poly1305, and v2 (reserved) is a hybrid post-quantum KEM. The sealed `schema.ver` versions the application data. The SDK must reject unknown `v` values explicitly and never guess. That rule follows the Bitmessage lesson that version namespaces must not be conflated (`design/evidence/bitmessage-guide.md:24-33`).

---

## D2 Definition of "private"

**Properties.**

| ID | Property | Holds against |
|---|---|---|
| C | Content confidentiality | All network parties without the stream key |
| T | Topic privacy: a tag cannot be linked to a stream, or two tags to each other | Chain observers, nodes, indexers (PRF tags) |
| S | Subscriber-interest privacy | The indexer in **full mode** (it learns only that the client reads the bus). In bucket mode it is weakened to *b*-bit buckets. |
| P | Publisher unlinkability on chain | Chain observers: DUST spends are shielded and Midnight transactions have no signer (read-out §3.4, §1.4) |
| R | Relationship privacy | Chain observers and indexers, except through timing |
| FS | Forward secrecy per epoch on streams | A later compromise of the current stream key (symmetric hash ratchet per epoch). No post-compromise security in Phase 1. |
| X | Unlinkable contract reaction: a reaction does not reveal which event it consumes | Chain observers (ZK Merkle membership), except through timing and anchor-root epoch |

**Leakage table.**

| Party | Learns | Does not learn |
|---|---|---|
| Submission node / RPC | Publisher IP plus the transaction, hence a link between IP and a publication. The node gossips without Dandelion or mixing (read-out §3.4 "Network", inference). | Stream, content |
| Indexer (full mode) | Subscriber IP, online times, that the client uses the bus, cursor positions | Which streams the client follows |
| Indexer (bucket mode, *b* bits) | All of the above, plus the bucket set requested per session. Intersection across sessions narrows which streams the client follows over time (the same effect Seres et al. show for FMD, `2021-seres-fmdfalsepositives` lines 72-96). | Exact tags, content |
| Chain observer | Bus contract, entry point (so the size class), tag, publish time, `v_fee`, DUST nullifier, anchor flag. For first contact: the recipient's 8-bit inbox bucket. For a reaction: target contract, anchor root, consumed-nullifier and disclosed effects. | Topic, publisher identity, recipient identity, content, which event a reaction consumed |
| Colluding minority (indexers and nodes) | The union of the above. Can **omit** events. | Omission within a stream is detected by `stream_seq` gaps |
| Global passive observer | Timing correlation from a publisher's submission to a recipient's reaction or reply | Not defended. Strong anonymity costs bandwidth or latency overhead (`2017-das-trilemma`, abstract). |

**Out of scope in Phase 1:** compromised endpoints; global timing analysis; hiding *that* a party uses the bus; post-compromise security and membership privacy for groups (MLS in Phase 3, `2022-hashimoto-mls-metadata`); read receipts. Bitmessage acknowledgements leak location and are not read receipts (`bitmessage-guide.md:265-267`), so the protocol defines no acknowledgement. An application that wants one sends a normal event and takes on that leak.

---

## D3 Publish and subscribe model (my lead decision)

### D3.1 Three kinds of stream, one mechanism

Everything is a **stream** with a symmetric key `k_s` that ratchets once per epoch (`k_{e+1} = H("ratchet" ‖ k_e)`; epoch = 14,400 blocks ≈ 1 day at 6 s, `midnight-node/runtime/src/lib.rs:292`).

- **Public stream:** `k_s = H("public" ‖ name)`. There is no confidentiality, but the API is the same. Used for announcements.
- **Shared stream:** random `k_s`, distributed in an **invite** `{bus_id, k_s, epoch, publisher_pubkeys, schema_ids}` by QR code, URL or inbox.
- **Inbox:** a **contact card** `{X25519 inbox key, bucket byte, card version}`. A first-contact event uses ECDH to deliver an invite to a pairwise shared stream, and all later traffic uses that stream. This is Bitmessage's first-contact flow (`bitmessage-guide.md:160-190`), with forward-secret streams after the first message.

There is no public topic discovery. A topic is discoverable only as far as its invite is shared, and that is the topic-privacy property.

**Tags.** A publisher with index *j* in stream *s* sends sequence number *n* under:

`tag = PRF(k_s,e, "tag" ‖ j ‖ n)`, which is 32 bytes.

Each publisher has its own sub-stream, so concurrent publishers never collide. Each stream member has its own signing key inside the sealed body. That avoids the Bitmessage chan problem, where a shared key is also a shared identity (`bitmessage-guide.md:289-291`).

**Recipient matching.** The recipient keeps a hash set of the next W = 32 expected tags per (stream, publisher). An event whose tag is in the set is decrypted with a known key, with no trial decryption. An event whose tag is not in the set costs one X25519 operation plus the 1-byte view-tag check, which skips the AEAD on 255 of 256 events. Monero adopted the same view-tag idea to cut scanning time (`2022-monero-pr8061-viewtags`, line 220). At 86,400 events per day and about 50 µs per X25519 operation (**assumption**; benchmark it), that is about 4.3 s of CPU per day.

### D3.2 How a consumer subscribes without revealing interest

| Mode | What the client fetches | Leak | Who uses it |
|---|---|---|---|
| **Full** (default) | Every `Misc` event on the bus contracts | That the client reads the bus | Agents, servers, desktop wallets |
| **Bucket(b)**, b ≤ 8, explicit opt-in | Events whose tag starts with one of the client's *b*-bit prefixes, plus the client's inbox bucket | Bucket set, which accumulates over sessions (D2) | Mobile |
| **Self-hosted** | Run the standalone indexer (SQLite plus in-memory pub/sub, `midnight-indexer/docs/architecture.md:7-52`) | Nothing to third parties | High-risk users, operators |

Bucket mode reuses a pattern Midnight already ships, client-chosen prefix lengths on nullifier subscriptions (`schema-v4.graphql:1992, 1998`). It needs an **indexer change**: today `fieldPrefixes` works on standard events only, and indexing `Misc` is left to the user (`schema-v4.graphql:558-562`). In the first-contact tag, byte 0 is the recipient's bucket and the other 31 bytes are random, so bucket clients still see their first-contact events.

**Rejected for Phase 1:**

- **Bloom-filter subscriptions.** Clients with fewer than 20 addresses leak nearly all of them (`2014-gervais-bloomfilters`, lines 66-71).
- **Server-side topic filters, as in Waku Filter.** They disclose topic interest to the full node (`2020-vac-waku2-filter-spec`, lines 298-300).
- **Fuzzy message detection.** The server can recover much of the social graph when senders are known (`2021-seres-fmdfalsepositives`, lines 95-96). The rate has to adapt to global traffic, which pushed Penumbra to a sender-chosen variant (`2022-penumbra-fmd-spec`, lines 78-94). Selfish users break FMD without altruists (`2024-frank-anonymous-messaging-altruism`, via `notes/PB3-receiver-privacy.md`). That is too many parameters to tune for a developer's first afternoon.
- **OMR / PIR.** OMR costs about $1 per million messages scanned and its digests decode in about 20 ms (`2021-liu-omr`, lines 28-29). Recipient-hiding retrieval costs at least as much as PIR (`notes/PB3-receiver-privacy.md`, findings 2). I keep it as the Phase-3 option for when full-mode volume exceeds mobile budgets (see D10 triggers).

### D3.3 Delivery semantics (normative)

1. **Finality.** Lane A delivers only finalised events. The indexer consumes finalised blocks only (`midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128-181`, per the read-out §4.1). Inference: there are no retractions.
2. **Order.** Lane A order is total, by `(height, tx_index, log_index)`. Within a stream, order is by `stream_seq` per publisher. The SDK delivers in chain order, and a later `stream_seq` can therefore arrive before an earlier one that was finalised later. In that case the SDK emits `gap` and then a `late` fill. There is no reordering buffer by default, because hidden buffering is how consumers lose events when they crash.
3. **Duplicates.** Delivery is at least once. midnight-js already says so and tells persisting consumers to dedup (`midnight-js/packages/types/src/public-data-provider.ts:507-508`). The SDK's dedup key is `eid`, the portable ID, not the indexer `id`.
4. **Replay.** Replaying a public envelope reproduces the same `eid`, so it is deduplicated. A *new* publication with equal bytes is impossible, because the tag includes `n`. Contract-level replay is handled by the consumed-nullifier (D3.5).
5. **Back-fill.** `subscribe(stream, {from: cursor | 'earliest' | 'now'})` replays and then follows live, as one stream. The indexer already does replay-then-live from an inclusive cursor (`midnight-indexer/indexer-api/src/infra/api/v4/subscription/contract_event.rs:98-152`). Back-fill is possible only for epochs whose keys the consumer still holds. Otherwise the SDK emits `gap{reason:"key-erased"}` and does not fail silently.
6. **Caught up.** The SDK emits `head{cursor}` when the replay reaches the indexer's tip. Today the client can see this only by comparing an event's `id` with its `maxId` (`schema-v4.graphql:1135-1137`). I ask the indexer for an explicit boundary marker, following Nostr's `EOSE` (`nostr-nip-01`, lines 153, 161).
7. **Gaps.** A missing `stream_seq` is reported as `gap{suspected}` after `T_gap` = 20 blocks (2 min). It becomes `late` if the event arrives later, or `closed` once `prev_skip` covers it.

### D3.4 SDK surface (TypeScript; a new `@midnight-ntwrk/private-events` package next to `PublicDataProvider`)

```ts
const bus = await PrivateEvents.connect({
  indexerWsUri, busAddresses,            // from wallet getConfiguration() (dapp-connector api.ts:206-220)
  keyStore,                              // reuses encrypted PrivateStateProvider storage
  mode: 'full',                          // or { bucketBits: 4 }  (explicit opt-in, documented leak)
});

const { stream, invite } = await bus.createStream({ kind: 'shared', schema: OrderFilled });
const card = await bus.openInbox();      // shareable contact card
await bus.join(inviteFromSomeone);

for await (const item of bus.subscribe(stream, { from: await store.cursor() ?? 'earliest' })) {
  switch (item.type) {
    case 'event':  /* { eid, stream, publisher, seq, cursor, finality:'final', blockTime, body } */ break;
    case 'gap':    /* { publisher, seqRange, reason:'suspected'|'key-erased'|'closed' } */ break;
    case 'late':   /* event that fills an earlier gap */ break;
    case 'head':   /* caught up */ break;
  }
  await store.commit(item.cursor);       // consumer-owned ack
}

await bus.processOnce(stream, handler, store); // idempotent wrapper: dedup by eid + atomic cursor commit

const r = await bus.publish(stream, body, { size: 'S', anchor: false });
// r.status: 'submitted' | 'final' | { failed: 'InsufficientDust'|'BusPaused'|'TooLarge'|'TxFailed' }
```

Errors are typed and closed. The SDK must never turn a transport failure into a silent completion. midnight-js already follows that rule (`public-data-provider.ts:509-510`). Sealed bodies are decoded only by generated codecs and never by dynamic dispatch. PyBitmessage's remote-code-execution bug came from `eval` on decrypted attacker data (`bitmessage-guide.md:354-358`).

### D3.5 How each consumer class consumes an event

- **Agent or service:** `subscribe` plus `processOnce`. Effects are exactly once given an atomic cursor-and-effect store.
- **Wallet:** in Phase 1 the SDK runs inside the wallet process. In Phase 2 the wallet holds the stream keys and the DApp connector gains `subscribeEvents(grant, cursor)`. Today the connector has **no event or subscription method** (read-out §5.3, `midnight-dapp-connector-api/src/api.ts:70-203`). Under this design dapps never hold keys for streams they were not granted.
- **Smart contract.** A contract **cannot read events or call out** (read-out §5.4 and §8). The node discards events after verification (`mips/mip-0002-public-contract-log-emission.md:154-162`). The pattern has five steps:
  1. The publisher sets `anchor = true`. The bus contract inserts `persistentHash(envelope)` into a `HistoricMerkleTree<32, Bytes<32>>` in its ledger state. Inserts into `HistoricMerkleTree` hide the value from observers (`midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:12-30`).
  2. Any recipient (the "reactor") calls the target contract's circuit, for example `onEvent(root)`, with the envelope, the Merkle path, `event_secret` and `action` as **private witnesses**.
  3. The circuit asserts `bus.isAnchorRoot(root)` through a cross-contract call. This is allowed because the callee uses no witnesses, and restriction 4 of toolchain 0.33 forbids only witness-using callees (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:96-104`). The circuit also checks the path, `binding == H(event_secret ‖ action_digest)`, and the publisher's signature against the contract's authorised-publisher set, without disclosing the publisher's key.
  4. It inserts `nf = H("consumed" ‖ event_secret)` into its own `Set` and rejects if `nf` is already there. The effect is **exactly once**, and the reaction **is not linkable** to the specific envelope (property X). The documented anonymous-authorisation pattern uses the same mechanism (`keeping-data-private.mdx:105-232`).
  5. Liveness rule: **no event triggers a contract by itself.** If no reactor submits, nothing happens. Applications that need liveness pay a bounty from the target contract (optional pattern).

  Feasibility is an **inference** that Phase 0 must prove: specifically the cross-contract `checkRoot` read and the circuit size for a depth-32 path. Fallback: the target contract keeps the anchor tree itself. That works, but anchored events lose the shared anonymity set.

---

## D4 Sustainable model

**Publishers pay DUST on Lane A, and readers pay nothing on chain.** There is no proof of work. It burdens weak devices and does not stop well-resourced spammers (`2004-laurie-proofofwork`; `bitmessage-guide.md:416`). Midnight's fee is already a non-transferable, generated resource.

**Cost per publish**, as an **inference** from genesis parameters with all factors at 1.0 and `overall_price` = 10 (read-out §7.1-7.3, `midnight-node/res/mainnet/ledger-parameters-config.json:156-175`):

- Transaction size is about 6 KB: a DUST spend proof of 2,912 B, a call proof estimate of 4,832 B, the transcript and a 288 B part (read-out §9.6).
- Block-usage term: 6,000 / 1,000,000 = 0.006 (normalised).
- Compute: about 2 proofs × (3.27 ms + inputs) ≈ 8 ms, × ¼ validation factor = 2 ms, / 2,000 ms block budget = 0.001. The `max(...)` therefore picks block usage.
- Churn for a 288 B log: 288 / 50,000,000 ≈ 6×10⁻⁶.
- **Fee ≈ 10 × 0.006 ≈ 0.06 DUST per S-class publish.** An L-class publish adds 4 KB, so about 0.10 DUST.

**What that costs in NIGHT.** `generation_decay_rate` is 8,267 Specks per Star per second. 1 NIGHT is 10⁶ Stars, derived from the 5 DUST per NIGHT cap (`ledger-parameters-config.json:164-168`). So 1 NIGHT generates 8.267×10⁻⁶ DUST per second, or **0.714 DUST per day**, which is **about 12 S-publishes per day per NIGHT**.

- An agent that publishes 1,000 events per day needs about 84 NIGHT.
- The whole Phase-1 target of 86,400 events per day needs about 7,260 NIGHT across all publishers.

Live prices move by up to about 4.6% per block toward 50% block fullness (read-out §7.2). The SDK reads `ledgerParameters` from each block and does not hard-code prices.

**Spam and abuse.** On Lane A spam is limited by price alone, because Midnight transactions have no signer (read-out §1.6). Open publishing to a shared bus is acceptable because spam costs DUST and consumers drop it at almost no cost: an unmatched tag costs one X25519. Scan-DoS is real when senders choose what recipients process (`notes/PB3-receiver-privacy.md`, finding 6). Here the cost is bounded by block capacity: at most about 167 publishes per block at 6 KB each, so a spammer spending the entire block budget forces at most 167 × 50 µs ≈ 8 ms of CPU per block onto each full-mode client. That is acceptable.

**Anchoring** (`anchor = true`) adds a persistent write of about 32 B per leaf plus Merkle nodes, against the 50,000-byte-per-block `bytesWritten` budget. The exact cost is **unknown** and is measured in Phase 0. Only publishers that need contract consumption pay it.

**Lane B (Phase 2).** Each sender holds an RLN membership with a stake in a Compact contract, a per-epoch message limit and secret-share slashing (`2024-vac-rln-v2-spec`, lines 36-54, 107-125; `2022-taheri-waku-rln-relay`).

**Read side.** No on-chain payment exists for indexer operators (read-out §2.3). Phase 1 relies on public indexers run by the Foundation, plus self-hosting. Paid access through anonymous prepaid tokens is a Phase-3 **open question**. I do not invent a mechanism here.

**Low load.** A small anonymity set is the real risk (`bitmessage-guide.md:350`). Shared bus contracts pool every application into one set. Per-application bus contracts are discouraged in the SDK and flagged in its documentation.

**High load.** See the D10 triggers: above 5 events per second sustained, bulk traffic moves to Lane B and Lane A keeps anchors.

---

## D5 Performance requirements

**Lane A capacity.**

- Target: 1 event/s average and 10 events/s peak.
- At 6 KB per publish, 1/s is 6 tx per block = 36 KB, which is **3.6%** of the 1,000,000-byte block-usage limit (`ledger-parameters-config.json:158`). The 10/s peak is **36%**.
- Absolute ceiling (the bus fills every block): about 167 publishes per block, about 28 per second.

**Latency from publish to delivery**, excluding proving (an inference from documented figures):

- Inclusion: 0-6 s, mean 3 s (`runtime/src/lib.rs:292`).
- Finality: about 18 s, which is about 3 blocks (`mps-0028-pre-finality-state-visibility.md:35-38`).
- Indexing and fan-out: about 1-2 s (**assumption**).
- **p50 ≈ 23 s. Target p99 ≤ 60 s.**
- Proving adds seconds on servers and 5-30 s on laptops for comparable proofs (`mps-0004-trusted-proof-serving.md:33`, [doc], about Zswap proofs; contract-call proving time is **unknown**).
- Lane A does not suit sub-second needs. That is why Lane B exists.

**Lane B latency (Phase 2).** Waku with RLN delivers messages of 25 KB or less in under 1 s, in simulation and on multiple hosts (`2024-revuelta-waku-latency`, lines 652-654). **Target p50 ≤ 1 s, p99 ≤ 3 s.**

**Full-mode subscriber bandwidth** at 1 event/s:

- Average 1.5 parts × 288 B = 432 B raw. Hex encoding in GraphQL doubles it to 864 B, plus about 300 B of JSON framing, which gives about 1.2 KB.
- With the deflate WebSocket variant (`midnight-indexer/indexer-api/src/infra/api/v4/ws_deflate.rs`), about 0.6 KB (**assumption**: about 2× compression on hex).
- Total: 86,400 × 0.6 KB ≈ **52 MB per day**.
- Bucket(4) cuts it to about 3.3 MB per day.

**CPU per subscriber.** Hash lookups plus one X25519 per unmatched event, about 4.3 s per day (D3.1).

**Indexer fan-out, the real bottleneck.** Today each subscription re-queries the database on every `BlockIndexed` signal (`contract_event.rs:125-146`). The configuration has a pool of 25 connections, a batch of 20 rows and 20 subscriptions per WebSocket (`midnight-indexer/indexer-api/config.yaml:30, 49-77, 83`).

- 10,000 full-mode subscribers produce 10,000 queries per 6 s, or 1,667 queries per second. On 25 connections each query must finish within 15 ms.
- I require a **shared per-block broadcast** for bus contracts: one query per block, fanned out from memory.
- Outbound bandwidth: 10,000 × 52 MB per day = 520 GB per day ≈ **48 Mbit/s** per instance.
- **Node-class targets:** a *bus indexer* serves 10,000 concurrent full-mode subscribers on 8 vCPU with 100 Mbit/s and p99 fan-out under 2 s after `BlockIndexed`; a *client* uses ≤ 60 MB per day and ≤ 10 s of CPU per day.
- Sustained events-per-second capacity of the current indexer is **not known** (no benchmark, read-out §4.7). Phase 0 measures it.

---

## D6 Storage requirements

**On the ledger.**

- Events are not stored in ledger state. Logs are churn (read-out §3.2 and §7.3).
- Only anchored envelopes add persistent state: one Merkle leaf each, permanently, because state rent does not exist (read-out §7.5).
- At a 10% anchoring rate that is 8,640 leaves per day, 276 KB per day of leaf data plus tree nodes (the node overhead is **unknown**). That amounts to 0.6 inserts per block, well inside the 50,000-byte-per-block `bytesWritten` budget, subject to Phase-0 measurement.

**Bus indexer.**

- Each event takes about 432 B raw plus about 150 B of sidecar index row (MIP-0002 Appendix B, `mip-0002:508-540`, which the read-out says to treat as a loose bound). Call it about 600 B.
- 86,400 × 600 B = **52 MB per day, 19 GB per year**.
- Hot retention is ≥ 30 days. Archival is indefinite and optional, because events can be rebuilt from block history by re-execution.

**Client.**

- The client stores stream keys per epoch, the cursor and the `eid` dedup set.
- The dedup set can be pruned below the committed cursor minus one finality window. The client keeps only `eid`s at or after `cursor − 1 block`, because finalised order is stable.
- That is a few kilobytes per stream. Clients store no events unless the application wants them.

**Availability rule that consumers see:**

`back-fill window = min(indexer hot retention (≥ 30 d), consumer key retention (default 30 d))`.

Both numbers come back from `bus.capabilities()`, so a developer never discovers them by surprise.

**Lane B (Phase 2).** Store nodes keep 24 h. At a 10/s peak with 1 KB events that is 864 MB per day per store node.

---

## D7 Infrastructure actors

| Actor | Admission | Trusted with | Paid by |
|---|---|---|---|
| Validators | Unchanged: 10 permissioned seats on mainnet (`midnight-node/res/mainnet/system-parameters-config.json:6-9`) | Inclusion and censorship. Governance can pause `send_mn_transaction` (read-out §2.2). | Unchanged. Fees appear to be burned (inference, read-out §2.3). |
| Bus indexer operators | Permissionless; anyone runs the indexer with the bus extensions | Availability and completeness. Omission can be detected within a stream; content is never exposed. | Phase 1: Foundation or self-hosted. Later: open question. |
| Publishers | Anyone with DUST | Nothing | Themselves (D4) |
| Reactors | Any recipient of the event | The plaintext they already hold | Themselves, or a bounty in the target contract |
| Lane B relays (Phase 2) | Permissionless libp2p peers; senders hold RLN membership | Forwarding only | Unpaid relay (Waku model); store nodes may charge |
| Wallet providers (Phase 2) | User's choice | Stream keys; they enforce dapp grants | The user's wallet |

**Path.** Phase 1 runs on Foundation indexers plus self-hosting, and the SDK supports a list of indexers with cross-checking. Phase 2 adds independent Lane B relays and wallet custody. By the end state every serious consumer either self-hosts or cross-checks two independent indexers, and the shared bus contracts are immutable (no `Maintain` authority) so governance cannot repoint them.

---

## D8 Network tether

**Recommendation: hybrid, built in phases.**

- **Phase 1 uses the ledger and indexer alone.** The anchoring lane is the only one that gives total order, durability, finality and something a contract can verify, without new peer-to-peer infrastructure. It also gives consumers the simplest semantics.
- **Phase 2 adds a separate libp2p GossipSub sidecar** as the fast lane, carrying the same envelope.
- I reject a node fork. Midnight has no gossipsub, a new protocol needs a custom node binary that every operator must run, and peer slots are shared with consensus traffic (read-out §1.5 and §8).
- **Fallback:** if ledger-9 contract events are not on mainnet in time, or the Lane A cost is too high, run Lane B first and anchor batch roots on chain with one `Misc` event per batch. The consumer API stays the same; only the `finality` labels change.

**Generation caveat.** Contract events and `contractEvents` belong to ledger 9 and Compact 0.33. The support matrix lists older versions for mainnet (`midnight-docs/docs/relnotes/support-matrix.json:14, 38, 82`, per read-out §0.3). Phase 1 depends on the ledger-9 hard fork, and its activation date is **unknown**.

**Changes required:**

- **Node:** none.
- **Ledger:** none.
- **Compact:** no compiler change. The Phase-1 bus contract and the `PrivateEventProof` library are plain Compact. I ask the compiler team to make `emit` of an item over `MAX_LOG_EMITTED` a compile error and not a silent drop. Today `max-emit-size` is 512 KiB while the VM drops above 1 KiB (read-out §3.2).
- **Indexer:**
  1. `Misc` name-prefix filter;
  2. shared per-block fan-out;
  3. `head` boundary marker;
  4. portable position fields `(height, txIndex, logIndex)` on `ContractEvent`;
  5. a documented retention policy.
- **midnight-js:** the new private-events package.
- **Wallet / DApp connector (Phase 2):** `subscribeEvents` with grants.

---

## D9 Threats and open risks

| Threat | Defence | Residual |
|---|---|---|
| Indexer omission or censorship | Per-stream `stream_seq` gaps, cross-checking two indexers, self-hosting | Omission of a *first-contact* event cannot be detected. Mitigation: the sender retries through its inbox stream. |
| Indexer reordering or forged events | Monotonic cursor check; AEAD; signatures; the anchor root is checked on chain for contract consumption | A forged *public* stream event is possible only if the stream lacks signatures. Signatures are mandatory on multi-publisher streams. |
| Cursor drift across indexer instances | Portable cursors; dedup by `eid` | None if the SDK is used |
| Silent event loss (> 1 KiB, failed fallible phase) | Fixed 256 B parts; guaranteed phase only (MIP-0019) | None known |
| Spam, scan-DoS | DUST price; O(1) tag matching; capacity bound (D4) | A well-funded spammer can raise fees for everyone |
| Subscriber deanonymisation through bucket queries | Full mode by default; bucket mode is opt-in, with *b* ≤ 8 and a leakage notice | Accumulates over sessions (`2021-seres-fmdfalsepositives`) |
| Linking a publisher's IP | SDK option to submit through Tor or a rotating RPC | Not defended by default; no Dandelion in the node. Lane B may add Dandelion-style stems (`2018-fanti-dandelionpp`). |
| Key compromise | Per-epoch ratchet (FS); rekey through inboxes on member removal | No post-compromise security until MLS (Phase 3) |
| Replay against contracts | Consumed-nullifier set | None |
| Governance pause / safe mode | Typed `BusPaused`; Lane B fallback in Phase 2 | Lane A stops entirely during a pause (`runtime/src/check_call_filter.rs:40-45`, per read-out) |
| Sybil / eclipse on Lane B | GossipSub peer scoring (`2020-vyzovitis-gossipsub`); RLN | Standard GossipSub residuals |
| `contractEvents` is `@beta` | Pin the API version; conformance tests in CI | Breaking changes upstream |

---

## D10 Build and verification plan

**Phase 0 (6-8 weeks): measure and model.**

- (a) Publish cost on preprod for the S, M and L classes, anchored and not.
- (b) Merkle anchor write cost, and the size of the cross-contract `isAnchorRoot` and depth-32 path circuit.
- (c) Indexer fan-out benchmark with 1k, 10k and 50k subscribers, before and after the shared broadcast.
- (d) Whether indexer `id` values match across primary and secondary.
- (e) A **Quint model of the SDK delivery state machine** (cursor, dedup, gap, late, head, reconnect, indexer failover). Invariants: no committed cursor skips an undelivered finalised event; each `eid` reaches the handler at most once under `processOnce`; every gap is eventually resolved as `late` or `closed`, or stays `suspected` with a reason.

**Phase 1: Lane A.** Bus contracts, the Compact `PrivateEventProof` library, the TypeScript SDK and the indexer extensions 1-4.

**Phase 2: wallet custody and Lane B.** DApp connector grants, GossipSub plus RLN sidecar, dual-lane dedup.

**Phase 3: scale and groups.** An OMR/PIR detection service, MLS-based groups and paid indexer access.

**Acceptance criteria for Phase 1.**

1. **Afternoon test:** five developers outside the team each build a subscriber that resumes after a crash and a publisher, using only the docs. At least 4 of 5 finish in 4 hours or less.
2. Chaos test with 10⁶ events: random indexer restarts, primary/secondary failover and client crashes. **Zero events lost, zero duplicates passed to `processOnce` handlers.**
3. Preprod latency p50 ≤ 30 s and p99 ≤ 90 s, excluding proving.
4. Full-mode client ≤ 60 MB per day at 1 event/s.
5. Contract reaction demo: exactly-once effect under 100 concurrent reactors racing on the same event.
6. Fuzzing of the envelope and CBOR decoders: no crash in 10⁹ iterations.

**Evidence that would change course.**

- Live publish cost above 0.2 DUST, or above about 3.5 publishes per NIGHT per day. Then move bulk traffic to Lane B in Phase 1.
- The indexer cannot serve 1,000 or more full-mode subscribers per instance even with broadcast. Then make self-hosting the default, or bring Phase 3 detection forward.
- Bus volume sustained above 5 events/s (more than 260 MB per day per full-mode client). Then bring OMR/PIR or bucket-by-default forward.
- The cross-contract root check is infeasible. Then use per-contract anchoring and accept the smaller anonymity set.
- Ledger-9 events are not on mainnet by the Phase-1 date. Then use the D8 fallback.

---

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Event format | `Misc` carrier: 32 B tag plus fixed 256 B parts; S/M/L classes (207 / 975 / 4,047 B usable); public `v`, view tag, `ek`; sealed CBOR with `stream_seq`, schema, binding, signature; portable `eid` and chain-position cursor | Variable-length emits (silent drop over 1 KiB); indexer `id` as cursor; data in ledger state (about 20× cost) | `midnight-events.ss:71-74`; read-out §3.2 (`L9:vm.rs:41-43`); `mip-0019:64-76`; `re-indexing.md:78-95`; `schema-v4.graphql:1127` | High | MIP-0019 rejected, or larger native events shipped (ledger 10) |
| D2 Private | C, T, S (full mode), P, R, FS per epoch, X; explicit leakage table; global observer and post-compromise security out of scope | Claiming global-observer anonymity; acknowledgements as receipts | `2017-das-trilemma`; `bitmessage-guide.md:265-267, 328`; `2021-seres-fmdfalsepositives` | Medium | Measured anonymity-set data showing the bus set is too small |
| D3 Pub/sub (lead) | Three stream kinds on one PRF-tag mechanism; full-stream default, opt-in bucket(b ≤ 8), self-host; finalised, at least once, chain-ordered, per-stream seq, gap/late/head, portable resume; contracts react through relayed ZK proof of an anchored envelope plus consumed-nullifier | Bloom filters; server topic filters; FMD; OMR/PIR in Phase 1; reorder buffering in the SDK; on-chain push to contracts | `2014-gervais-bloomfilters:66-71`; `2020-vac-waku2-filter-spec:298-300`; `2022-penumbra-fmd-spec:78-94`; `2021-liu-omr:28-29`; `contract_event.rs:98-152`; `public-data-provider.ts:507-510`; `nostr-nip-01:153-161`; `toolchain-0.33.0.md:96-104`; `2022-monero-pr8061-viewtags:220` | Medium-high (contract path: medium) | Phase-0 circuit/root-check infeasible; full-mode bandwidth over the mobile budget at real load |
| D4 Sustainable | Publisher pays DUST (≈ 0.06 DUST per S event; ≈ 12 per NIGHT per day); no proof of work; RLN on Lane B; reads free and the read-side incentive open | Proof of work; per-identity limits on Lane A; inventing indexer payments now | `ledger-parameters-config.json:156-175`; read-out §7; `2004-laurie-proofofwork`; `2024-vac-rln-v2-spec` | Medium | Live prices about 3× genesis or worse |
| D5 Performance | Lane A 1/s average, 10/s peak (3.6% / 36% of a block); p50 ≈ 23 s, p99 ≤ 60 s; client ≤ 52 MB/day; indexer 10k subscribers with shared broadcast; Lane B p50 ≤ 1 s | Sub-second on Lane A; a query per subscriber per block | `runtime/src/lib.rs:292`; `mps-0028:35-38`; `config.yaml:30, 49-83`; `2024-revuelta-waku-latency:652-654` | Medium | Phase-0 benchmarks |
| D6 Storage | No events in ledger state; anchors only when asked; indexer 52 MB/day (19 GB/year), ≥ 30 d hot; back-fill = min(indexer, key retention) | Storing messages in contract state; unlimited client back-fill promises | read-out §7.5; `mip-0002:508-540` | Medium | Anchor-tree write cost far above estimate |
| D7 Actors | Unchanged validators; permissionless bus indexers; reactors; Lane B relays; wallet key custody (Phase 2) | A dedicated permissioned relay set; dapps holding all keys | read-out §2; `api.ts:70-220` | Medium | Nobody runs indexers without pay, which moves paid access forward |
| D8 Tether | Hybrid in phases: Phase 1 ledger plus indexer only; Phase 2 GossipSub/RLN sidecar; fallback Lane B with on-chain batch anchors; no node change; indexer changes 1-5 | Node fork with a gossip protocol; off-chain workers; inherents | read-out §1.5, §8; `support-matrix.json` (read-out §0.3) | High (Phase 1), medium (Phase 2) | Ledger-9 activation slipping past Phase 1 |
| D9 Threats | Seq-based omission detection, cross-checked indexers, fixed parts, consumed-nullifiers, typed pause errors | Trusting one indexer silently | `contract_event.rs`; `check_call_filter.rs:40-45` (read-out) | Medium | Evidence that a first-contact omission attack is practical at scale |
| D10 Plan | Phase 0 measurement plus a Quint model of SDK delivery; Phase 1 Lane A; Phase 2 wallet and Lane B; Phase 3 OMR/MLS; afternoon test and a zero-loss chaos test as gates | Building Lane B first; shipping without a delivery-model check | — | High | Afternoon test failing twice, which means the API is redesigned before any lane is added |
