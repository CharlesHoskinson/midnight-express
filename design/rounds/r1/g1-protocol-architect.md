I will read the charter first, then the Midnight readout, the graph overview, and the Bitmessage evidence the ten decisions depend on.The charter fixes the ten decisions and the citation rules. Next I will read the Midnight stack, the Bitmessage start, and the graph overview before choosing a wire format.The stack readout and the Bitmessage guide are in. I am checking the review, the paper index, and the formats I would actually put on the wire.Midnight Private Events v1 is one fixed 192-byte object, `EVENT`, flooded inside a single shard by a sidecar GossipSub mesh. Relays see admission and size, not topics or parties. Payloads are sealed with an ephemeral X25519 key and ChaCha20-Poly1305. Publishing is authorized by a one-time key bought with a shielded DUST transaction on a ledger-9 contract. The ledger is not the data plane, and the Midnight node does not gain a new peer protocol. Version 1 has no extension bits: a new layout is a new protocol id.

## D1 Event format

One disseminated object. Point-to-point frames exist for stem forwarding, a full-shard stream, and backfill. They are not objects and they are not stored. There is no `getpubkey`, `ack`, or `broadcast` type. Bitmessage's four propagating types, its varints, and its rule that unknown types still relay are the behaviour this layout is built to avoid (`2012-bitmessage-protocol-specification`, object header: 8-byte nonce, 8-byte `expiresTime`, 4-byte `objectType`, a varint version, a varint stream, then a typed payload; unknown types are relayed). Waku's protobuf, with optional `content_topic`, `meta`, `timestamp`, and `rate_limit_proof`, is the other behaviour to avoid: protobuf v3 is not a stable canonical encoding, and the content topic is cleartext (`2020-vac-waku2-message-spec`, wire format and hash sections). Whisper's clear 4-byte topic is the same leak in a smaller header (`2017-eip-627-whisper`, envelope `[Expiry, TTL, Topic, Data, Nonce]`).

Encoding is little-endian, fixed width, one legal layout. No SCALE, no protobuf, no varints, no trailing bytes. `header_len` must be 192. Both reserved fields must be zero. A non-zero reserved field is invalid, not a place for an extension. Integers use their full width. The body length is implied by `size_class` and must match exactly.

`EVENT` header, version 1, kind 1:

| Offset | Width | Field | Relay rule |
|---:|---:|---|---|
| 0 | u8 | `version` | Must be 1. Any other value is invalid. |
| 1 | u8 | `kind` | Must be 1. |
| 2 | u16 | `header_len` | Must be 192. |
| 4 | u8 | `size_class` | 0, 1, 2, or 3. |
| 5 | u8 | `shard` | Must equal `SHA-256("midnight-pe/shard/v1" \|\| audience_key)[0] mod shard_count`. Launch `shard_count` is 1, so this byte is 0. |
| 6 | u16 | `reserved` | Must be 0. |
| 8 | u32 | `expiry` | Unix seconds. `now + 60 ≤ expiry ≤ now + TTL_MAX[class]`. |
| 12 | u32 | `ticket_epoch` | `floor(unix / 600)` of the finalized admit event. |
| 16 | 32 | `eph_pk` | X25519 public key. Reject the all-zero encoding and any key the X25519 library rejects. |
| 48 | 32 | `ticket` | Nullifier from the admit contract. |
| 80 | 12 | `nonce` | AEAD nonce, random per object. |
| 92 | u32 | `reserved2` | Must be 0. |
| 96 | 32 | `pub_pk` | One-time Ed25519 key, equal to the key in the admit event. |
| 128 | 64 | `relay_sig` | Ed25519 over `header[0:128] \|\| body` by `pub_pk`. |

The body is `SIZE[size_class]` bytes and nothing follows it. `object_id = SHA-256("midnight-pe/id/v1" \|\| header \|\| body)`. It is not transmitted. It is the GossipSub message id and the dedup key.

Size classes and maximum lifetime:

| Class | Body | Wire | `TTL_MAX` | Cleartext payload max |
|---:|---:|---:|---:|---:|
| 0 | 256 | 448 | 3600 s | 104 |
| 1 | 1024 | 1216 | 1800 s | 872 |
| 2 | 4096 | 4288 | 900 s | 3944 |
| 3 | 16384 | 16576 | 300 s | 16232 |

Payload max is `body − 16` (Poly1305 tag) `− 136` (plaintext prefix). The largest wire object is 16,576 bytes. That is far under the patched Yamux default credit of 256 KiB (`rust-yamux/yamux/src/lib.rs:45`) and under the 1,048,576-byte Midnight transaction limit (`midnight-node/res/mainnet/ledger-parameters-config.json:152`). Class 3 exists so a proof-carrying blob does not pretend to be a 256-byte signal. Longer TTL on larger classes is refused so one object cannot dominate the store.

AEAD is ChaCha20-Poly1305. The nonce is `header[80:92]`. Associated data is the 192-byte header. Keying:

- Unicast: `shared = X25519(eph_sk, recipient_enc_pk)`, then HKDF-SHA256 with salt `midnight-pe/v1` and info `midnight-pe/aead/unicast/v1 || ticket`.
- Topic: HKDF-SHA256 with ikm the 32-byte topic key and info `midnight-pe/aead/topic/v1 || ticket || eph_pk`. The publisher still puts a fresh `eph_pk` on the header so the two audiences are the same width.

SHA-256 is Midnight's persistent hash on ledger 9 (`ledger-9.1.0.0-rc.5:base-crypto/src/hash.rs:29,93-94`, `PERSISTENT_HASH_BYTES = 32`). One hash family for object ids, topic ids, and contract commitments.

Plaintext prefix, then application bytes, then `0x00` pad to `body − 16`. A non-zero pad byte is invalid.

| Offset | Width | Field |
|---:|---:|---|
| 0 | u8 | `pt_version` = 1 |
| 1 | u8 | `audience` = 1 unicast, 2 topic |
| 2 | u16 | `payload_len` |
| 4 | u32 | `seq` |
| 8 | 32 | `topic_id`, or 32 zero bytes for unicast |
| 40 | 32 | long-term Ed25519 `sender_pk`, or zeros |
| 72 | 64 | Ed25519 signature, or zeros |

The inner signature covers the ASCII domain `midnight-pe/sig/v1`, the clear header, prefix bytes `[0:72]`, and the payload. It does not cover the pad. Topic objects must be signed. Unicast may be unsigned; an unsigned unicast object is unauthenticated. The inner key is the publisher's long-term identity. The outer `pub_pk` is a one-time admission key. They are different keys on purpose.

`topic_id = SHA-256("midnight-pe/topic/v1" || utf8(label))`. It sits inside the seal. `audience_key` for the shard byte is the recipient encryption key (unicast) or the `topic_id` (topic).

Identity, off the wire: `0x01 || enc_pk[32] || sig_pk[32] || SHA-256(SHA-256(those bytes))[0:4]`, text form `mpe1` plus base32. A third secret, `admit_sk`, is used only to buy tickets and is not in the identity string. RIPEMD-160 is not a Midnight hash, so Bitmessage's address digest is not reused.

What a relay is given: every header field, the ciphertext body, the peer that handed it the bytes, and the time it arrived. What a relay is not given: topic, sender, recipient, `seq`, payload, or inner signature.

Admission check, in order, before forward: version and widths; reserved zeros; size class and body length; expiry window; local clock within 120 seconds of the latest Midnight block timestamp the relay has, otherwise the relay stops validating rather than punishing peers; `shard` legal for the current `shard_count`; `relay_sig` verifies; `ticket` equals a finalized admit event for `(ticket, pub_pk, ticket_epoch)` and has not been used; `expiry ≤ (ticket_epoch + 2) * 600`. Failure of the signature or the ticket is a GossipSub Reject and counts as an invalid message. A duplicate `object_id`, or an object that is merely expired on arrival, is Ignore: not forwarded, not punished (`2020-gossipsub-v11-spec`, extended validator Accept / Reject / Ignore).

Seen-sets: `object_id` until `expiry`; `ticket` until `(ticket_epoch + 2) * 600`, which is longer than object expiry, so one ticket cannot buy a second object.

Version negotiation is the libp2p protocol string plus the version byte, checked against `pe_version_max` on the admit contract. v1 speaks only `/midnight-pe/1`. A second layout is `/midnight-pe/2` with its own mesh. Nodes may run both during a contract-declared window. They do not negotiate features inside v1. GossipSub's own protobuf is an implementation detail of the sidecar: message signing off, peer-id `from` not part of the id. Waku already had to define a deterministic hash because protobuf is not canonical (`2020-vac-waku2-message-spec`). Ours is stricter: the id is a hash of the fixed object only.

Stem, stream, and backfill are fixed frames on their own protocol ids (`/midnight-pe/stem/1`, `/midnight-pe/stream/1`, `/midnight-pe/backfill/1`). The stem frame is 8 bytes (`version = 1`, `hops_remaining`, six zero bytes) plus one `EVENT`. The publisher sets `hops_remaining = 2`. Each stem decrements it and forwards to one outbound peer, or fluffs if it has nowhere to send. A frame that arrives with 0 is injected into the mesh. `hops_remaining` is not part of `object_id`. The backfill request is 12 bytes: version, shard, size-class bitmask, a zero, `from_expiry` u32, `limit` u16 from 1 to 64, and a zero u16. The response is a count and raw objects. No topic field.

## D2 Definition of private

v1 claims four properties, each against a named adversary.

**Content confidentiality.** A relay, an indexer, a chain observer, a colluding minority of relays, or a wiretap that does not hold the audience key learns nothing about the plaintext from the body, assuming ChaCha20-Poly1305 and X25519 hold. A party who holds the topic key or the recipient key reads the body. This is not forward secret. The ephemeral key is on the header; the recipient key is static. Later compromise of `enc_sk` opens the archive. That is the same shape as Bitmessage's ECIES construction (`design/evidence/bitmessage-guide.md`, encryption section). `admit_sk` does not decrypt.

**Sealed-party confidentiality against relays that lack candidate keys.** Topic id, long-term sender key, and recipient key are inside the AEAD. With `shard_count = 1` the shard byte does not partition audiences.

**Subscriber-interest privacy at topic granularity.** Mesh membership is "this peer wants shard 0", not "this peer wants topic T". Waku Filter does the opposite: the client sends a non-empty content-topic set and the server forwards matches (`2020-vac-waku2-filter-spec`). The indexer `contractEvents` filter requires `contractAddress` (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:548-552`). Neither is the subscribe path.

**Ticket binding.** A finalized admit event names `(ticket, pub_pk)`. Only the holder of that one-time key can publish one object under that ticket. A chain observer who copies the ticket cannot substitute a body.

Explicit non-claims:

- **No forward secrecy and no post-compromise security.** A session ratchet would be a new object version. v1 does not carry one.
- **No global-passive anonymity.** Against a global passive adversary, strong anonymity requires high bandwidth or high latency (`2017-das-trilemma`). v1 spends bandwidth on one-shard flood and does not add cover traffic or mix delay. Relationship privacy and publisher unlinkability are not claimed against that adversary.
- **No source-anonymity theorem.** The 2-hop stem is a heuristic. Dandelion++'s near-optimal regime is a different mechanism: an approximately 4-regular anonymity graph, with expected precision no better than on the order of `p²` for a spy fraction `p`, and the older line stem only reaching `O(p² log(1/p))` under weaker assumptions (`2018-fanti-dandelionpp`). v1 does not implement that graph and does not claim that bound.
- **A known candidate encryption key can be tested.** `eph_pk` is public, so anyone who already knows `enc_pk` can try the unicast KDF. Unlisted keys are not testable. Listed keys are. Fuzzy detection is not in v1: a detection key handed to a server weakens the guarantee the flood was bought to get (`2021-beck-fmd`, flag ciphertext 68 bytes, test about 0.548 ms at `p ≈ 3%`; `2021-seres-fmdfalsepositives`, relationship anonymity fails for many users once the server sees real traffic).

Leakage table:

| Observer | Learns | Does not learn from the protocol |
|---|---|---|
| One honest relay | Header fields, ciphertext, neighbour addrs, arrival time, size class | Topic, parties, payload, inner signature |
| Stem predecessor of the publisher | Publisher IP and the moment of injection, plus the header | Payload |
| Indexer used for admit events | Contract address of the admit contract, each `Misc` ticket event, block time, `v_fee` of the buy transaction | Audience, payload. Payer of a shielded DUST spend is hidden; `v_fee` is not (`notes/midnight-network-stack.md` §3.4; `ledger-9.1.0.0-rc.5:ledger/src/dust.rs:1765` subtracts `v_fee` from the note) |
| Chain observer | Same as the indexer for anything the buy or `note` transaction discloses. Unshielded inputs and outputs are clear if the client attaches them | Sealed body, unless the follow-up call discloses fields |
| Colluding minority of relays | Union of the above, plus a better first-seen estimate of who injected the fluff | A proof of the author |
| Global passive observer | Sizes, times, and the ticket-to-purchase link (the ticket is on chain before it is on the mesh) | Payload. Sender-recipient relationship is out of scope, not protected |
| Holder of a candidate `enc_pk` | Whether each object opens under that key | Other people's plaintext |

Out of scope: endpoint compromise, malware, a malicious local agent, traffic confirmation by an ISP against a user who is the only speaker on an otherwise idle host, quantum decryption of recorded X25519, and deletion from a relay that ignores `expiry`. Expiry obliges honest relays to stop serving the object. It is not a promise that copies are gone. Bitmessage's own expiry has the same limit (`design/evidence/bitmessage-guide.md`).

Co-purchase is a leak the user chooses. Several tickets emitted by one Midnight transaction are linkable to each other. One ticket per transaction avoids that and costs a proof per ticket.

## D3 Publish and subscribe

Addresses are not routes. A unicast audience is an encryption public key. A topic audience is a 32-byte symmetric key plus a `topic_id` derived from a label. Discovery of those keys is out of band (a wallet QR, a contract field the application chooses to publish, a prior object). The mesh does not look up keys. There is no `getpubkey` object. A public directory of encryption keys makes those keys testable; applications that need the test to fail keep keys off the chain and off public websites.

Shard assignment is computed, not chosen. Launch parameter `shard_count = 1`. The byte is in the header so a later parameter change does not need a new object version. Raising `shard_count` is a contract write, one epoch before it takes effect, and only after a shard has sat over its bandwidth budget (D5) for seven days. Subscribers follow the new mapping. In-flight objects keep the old mapping until they expire, which is at most one hour.

Subscribe means: hold the audience keys, join shard 0 as a relay or open one full-shard stream, trial-open every object. A relay tries its unicast keys and then its topic keys. A miss is an AEAD failure. No view tag and no Bloom interest are in the header. At the operating point below, a full trial is cheap relative to the link; a tag would spend anonymity to save work we have not measured as scarce.

Delivery:

- At-least-once for a peer that is on the mesh, or on a stream to an honest relay, during the object's life.
- Duplicates are normal. Consumers dedup on `object_id`.
- There is no cross-publisher order. `seq` is advisory and visible only after open, and only for one signing key. A gap is "not arrived" until `expiry`; after `expiry` it is loss.
- Replay of the same bytes is a duplicate. Replay with a new body needs a new ticket. A ticket cannot be spent twice inside the two-epoch window.
- Backfill returns objects the relay still holds, by `expiry` and size class, never by topic. A relay may refuse backfill. Refusal is not a validity failure.
- No acknowledgements. An ack is a second object that traces the recipient, which the Bitmessage paper already flagged (`design/evidence/bitmessage-guide.md`, acknowledgement timing).

Topic keys are symmetric. Anyone who has the key can read. They cannot publish as a named sender unless they hold that sender's long-term signing key. Rotating the topic key is the revocation action. Old objects stay readable to holders of the old key. This is not a chan: a chan derives a shared identity from a passphrase so every member can act as that identity (`2012-bitmessage-wiki-faq`, as summarised in `design/evidence/bitmessage-guide.md`). It is also not MLS. MLS state may sit inside the application payload later; relays will not parse it.

**Smart contract.** No contract reads the bus. The Impact VM has no network I/O, events are not ledger state, and the node drops them after verification (`notes/midnight-network-stack.md` §3.2, §5.4, §8). Consumption is a later Midnight transaction. The application defines `commitment = SHA-256("midnight-pe/commit/v1" || object_id || payload)`. An agent calls `note(commitment)` on a consuming contract. The contract stores or checks that 32-byte value. It learns the commitment and whatever else the call discloses. It does not learn the payload. Order is ledger order of finalized `note` calls. A second `note` of the same commitment is the same fact. A failed fallible segment emits nothing, so `note` belongs in the guaranteed segment. This path exists only after the ledger-9 fork: `emit` and `VersionedLogItem` are on tag `ledger-9.1.0.0-rc.5` (`onchain-vm/src/vm.rs:39,43`, `MAX_LOG_SIZE = 1 << 19`, `MAX_LOG_EMITTED = 1 << 10`), and the docs' mainnet matrix is an older generation (`notes/midnight-network-stack.md` §0.3).

**Wallet.** The shielded wallet today trial-decrypts the global Zswap stream locally and does not subscribe to contract events (`notes/midnight-network-stack.md` §4.4). The bus follows that pattern: a user-run agent holds `enc_sk`, scans shard 0, and hands opened objects to the wallet over localhost. The public indexer is not given wallet keys and is not given a topic filter. The dapp connector has no event method (`notes/midnight-network-stack.md` §5.3). v1 does not add one. A phone that will not run an agent does not get topic privacy: handing a detection key to a provider is the FMD trade, and it is deferred.

**Agent.** The agent is the consumer that can stay online. It keeps `object_id`s until `expiry`, persists the admit contract's last finalized height, and speaks either the mesh or a stream. It is the component a contract's `note` relayer and a wallet's scanner share.

Publish path, hot: tickets were bought in an earlier epoch; the agent builds the object, stem-forwards it, and returns when at least one honest mesh peer has it. Publish path, cold: the agent first lands an admit transaction and waits until that block is finalized. Relays must not accept a ticket from the mempool. The indexer serves finalized blocks only (`notes/midnight-network-stack.md` §4.1). Pre-finality visibility is a proposed MPS, not a mechanism.

## D4 Sustainable model

Publishers pay. Relays in v1 are not paid by the protocol. Carrying and storing are operator costs, the same shape as today's indexer and RPC hosts, for which no on-chain payment exists (`notes/midnight-network-stack.md` §2.3).

The payer's instrument is DUST. A `DustSpend` reduces the note by public `v_fee` (`ledger-9.1.0.0-rc.5:ledger/src/dust.rs:1765`). The network readout found no path that credits `v_fee` to a validator or treasury (inference, §2.3). This proposal does not depend on fees being burned, only on this fact: the fee does not arrive at a relay. Paying relays from `v_fee` would be new ledger semantics.

Admit contract, one Compact contract, no compiler change:

- Membership is a commitment `persistentHash("mpe-member-v1" || admit_sk)` in a `HistoricMerkleTree`. The encryption key is not an input. Registration does not publish a testable key.
- A buy call proves membership, takes a fresh one-time Ed25519 `pub_pk`, and emits one `Misc` per ticket. `Misc` is `name: Bytes<32>` plus `payload: Bytes<256>` (`minokawa-compact/compiler/midnight-events.ss:71-74`). `name` is the 32-byte domain hash. `payload` is `ticket_epoch || ticket || pub_pk` (68 bytes) and zeros after that. Each such event is far under the 1 KiB silent drop (`MAX_LOG_EMITTED`).
- Uniqueness is a `Set` of live tickets. The same call deletes tickets whose epoch is older than `current − 2`. Net persistent bytes stay near zero when one insert replaces one delete. The member tree still grows. Contract state has no rent (`notes/midnight-network-stack.md` §7.5). Member-tree growth is an accepted residual until a history mechanism exists (MPS-0032 is Proposed, not code).
- Budget **assumption:** 30 tickets per member per 600-second epoch. A hotter publisher registers another `admit_sk` and pays another transaction.
- Clients must not attach unshielded inputs to a buy. Relays cannot enforce that. A buy that spends unshielded tokens publishes the owner (`notes/midnight-network-stack.md` §3.4).

Why tickets instead of proof-of-work. Bitmessage's proof of work prices length and TTL and is checked with one hash (`2012-bitmessage-protocol-specification`, PoW minima in the guide's reading). Schaub's analysis of that formula: legitimate senders and spammers pay the same, and a redesign that separates them at best halves the harm (`2015-schaub-bitmessage-antispam`). Waku's rate-limiting nullifier is closer to the right idea and adds slashing via Shamir shares (`2022-taheri-waku-rln-relay`). Slashing does not fit DUST: DUST is non-transferable and the fee is not paid to a pool the protocol can seize. A prepaid single-use ticket is the primitive Midnight already has, the shielded nullifier (`notes/midnight-network-stack.md` §6.3, the Merkle-membership plus nullifier pattern).

Genesis price arithmetic, from parameters I read, not from live fees. `overallPrice` and the four factors in `ledger-parameters-config.json:169-175` are `10 * 2^64` and `1 * 2^64`. The readout's fee formula then charges the block-usage term `10 * bytes / 1_000_000` DUST when other terms are smaller (§7.3). Block usage limit is 1,000,000 bytes (`ledger-parameters-config.json:158`). **Assumption:** an admit transaction is about 8 KB, from the readout's proof sizes (DUST spend proof 2,912 bytes, unproven call estimated at 4,832). Fee at genesis ≈ `10 * 8000 / 1_000_000 = 0.08` DUST per buy. At 30 tickets, about 0.0027 DUST per object. Live prices move; the same file's adjustment parameter is not a promise, and current live prices are not in the repos (`notes/midnight-network-stack.md` §7.2). One NIGHT's DUST cap is 5 DUST on the readout's reading of `night_dust_ratio = 5_000_000_000` (`ledger-parameters-config.json:165` and §2.3). That cap buys on the order of 60 such transactions before regeneration. I did not re-derive the speck scale.

The chain, not the mesh, caps the publish rate. A full block of 8 KB transactions is `1_000_000 / 8000 = 125` calls, and blocks are every 6 seconds (`midnight-node/runtime/src/lib.rs:292`), so about 21 calls per second if the block were only admit calls. **Policy assumption:** admit calls are budgeted at 10% of `blockUsage`, about 2 calls per second. At 30 tickets each, the mint rate is about 60 tickets per second. The operating point in D5 is 50 objects per second per shard so the bus stays under that mint rate while `shard_count = 1`. If the real circuit is larger than 8 KB or heavier than the block's compute budget (2 seconds of ref time, `runtime/src/lib.rs:305-311`), the phase-0 build lowers the batch size and lowers the operating point with it. That measurement is a gate, not a guess to ship around.

Low load: a few relays hold a quiet shard; tickets are cheap; pre-bought tickets make publish a gossip send. High load: DUST price rises with Midnight's fee update, the 10% block budget queues buys, and relays refuse new objects past their local cap instead of dropping stored ones. Refusal is visible. Silent early prune is not allowed. An empty network does not require cover traffic to stay up; it also does not earn the anonymity of a busy shard. That is the trilemma showing up as an operations fact (`2017-das-trilemma`).

Spam without NIGHT cannot buy tickets. Spam with NIGHT can, up to the budget and the block cap. A replay of a captured object dies with `object_id` dedup and with expiry.

## D5 Performance requirements

These are requirements for the phase-1 simulation, not measurements of a running network. GossipSub's v1.1 text gives an example point of `D = 6` with `D_out = 2`, and it defaults `FloodPublish` to true (`2020-gossipsub-v11-spec`, parameter table). v1 sets `D = 6`, `D_out = 2`, `FloodPublish = false`. `D_lo` and `D_hi` are whatever the pinned GossipSub crate documents for `D = 6`; I did not find those two defaults in the v1.1 text, so they stay **unknown** until the crate is pinned. The mesh topic string is `/midnight-pe/1/shard/0`. There is one topic. Content topics are not created.

**Assumption** on the launch mix: 70% class 0, 25% class 1, 5% class 2, 0.1% class 3. Mean wire size:

`0.70*448 + 0.25*1216 + 0.05*4288 + 0.001*16576 = 848.6` bytes.

**Assumption** on forwarding: with flood-publish off, a relay sends each new object to `D − 1 = 5` mesh peers and receives it `1.5` times including duplicates and IHAVE/IWANT overhead. I have no measurement for the 1.5 factor.

Per object, per relay, at that assumption: send `5 * 848.6 = 4,243` bytes, receive `1,273` bytes, together about 44.1 kbit.

| Class | NIC (assumption) | Bus cap | Joins | Edge streams | Object-store cap |
|---|---:|---:|---|---:|---:|
| Edge | 10 Mbit/s up | one stream | none | consumes 1 | none |
| Relay-A | 50 Mbit/s | 20 Mbit/s | shards whose projected send+receive ≤ 12 Mbit/s | at most 4, only from budget left after the mesh | 2 GiB |
| Relay-B | 200 Mbit/s | 80 Mbit/s | all launch shards | at most 16 | 8 GiB |
| Archive | same as the relay it sits beside | same | read-only, not a mesh injector | 0 | class 0 and 1 for 7 days |

Operating point, one shard, `λ = 50` obj/s:

- Mesh send+receive per relay ≈ `50 * 44.1 kbit = 2.21 Mbit/s`.
- One edge stream ≈ `50 * 848.6 * 8 = 0.34 Mbit/s`. Four streams ≈ 1.36 Mbit/s.
- Relay-A total ≈ 3.6 Mbit/s, under the 20 Mbit/s cap.
- Resident objects, everyone at `TTL_MAX`: `35*3600 + 12.5*1800 + 2.5*900 + 0.05*300 = 126,000 + 22,500 + 2,250 + 15 = 150,765`.
- Store ≈ half of the λ=100 figure below, about 94 MB of bodies. A 2 GiB cap is about twenty times that.

Headroom check at `λ = 100`, which the chain mint rate does not sustain at a 10% block share, but the mesh must survive as a burst: mesh ≈ 4.4 Mbit/s, store ≈ `100 * 1.874e6` byte-seconds ≈ 179 MB. Hard local reject: a relay refuses new objects when its measured bus rate would exceed 12 Mbit/s or the store cap. It does not delete unexpired objects to make room.

CPU requirement: one Ed25519 verify per object. The ledger prices an in-circuit signature verify at `97,304,512` ps, which is 97 µs (`ledger-parameters-config.json:124`). At 50 obj/s that is about 5 ms of that equivalent per second of wall clock. Opening the AEAD is extra and is done only for keys the relay actually holds; a pure relay verifies the outer signature and does not trial-open. X25519 costs cited in the corpus are for a laptop pair at 160–233 ns (`2023-stainton-pqsphinx`, catalog note). I do not treat that as a server budget. The requirement is: a Relay-A at 50 obj/s stays under 20% of one core for validation plus forwarding. If the phase-1 run exceeds that, the cap drops before the format changes.

Latency requirements, hot path (ticket already finalized): relay-to-relay p50 ≤ 2 s and p99 ≤ 10 s at `λ = 50` with 16 relays and no artificial loss. Cold path adds finality. The docs say finality is usually about three blocks, about 18 s (`notes/midnight-network-stack.md` §1.7, citing MPS-0028). Proving a buy is seconds to a minute on the same readout's docs (§6.2). Contract `note` is that cold path again. The 2 s figure is not a claim about contract visibility.

Fan-out: every Relay that has joined the shard receives every object. Edge count does not multiply mesh traffic. It multiplies the stream sender's unicast fan-out, which is why the stream cap is 4 on Relay-A. Ten thousand phones cannot each pull the shard from public relays. They run an agent, or they wait for a later retrieval design.

Concurrent subscribers in the mesh: on the order of the relay count, not the user count. Launch mesh is the admitted relay set (D7). GossipSub degree stays 6; extra relays are reached by gossip, not by raising `D`.

## D6 Storage requirements

Honest relays keep each object until `expiry` and the ticket until the end of `ticket_epoch + 2`. They may keep the `object_id` for another hour to ignore late duplicates. They must not keep the body after `expiry`.

At the D5 operating point a Relay-A holds on the order of 100 MB of bodies and a few tens of megabytes of ids. The 2 GiB cap is the availability bound: past it the relay rejects new objects. Availability of an object is "any honest relay that accepted it will serve it until `expiry`" to mesh peers and to streams it has already admitted. There is no replication factor beyond the mesh itself. A partition can hide an object from the other side until expiry. That is loss, not a queue.

Archives are optional and outside the availability claim. Seven days for class 0 and class 1, on a node that asks for them. They are not required for a consumer who was online during the hour. A consumer who was not online has missed the object unless an archive it trusts still has it. Trusting an archive is the same trust as trusting a store node that learns the time of the request. The request still has no topic field.

What is on the ledger: the member tree, the live ticket set, the admit `Misc` events, `shard_count`, `pe_version_max`, and any `note` commitment an application submits. What is not on the ledger: bodies, headers, topic ids, encryption keys. Logs are churn, priced as bytes written and bytes deleted, against a 50,000,000-byte churn limit per block (`ledger-parameters-config.json:160`; the readout §3.2 describes the `log` opcode charging both). Persistent `bytesWritten` is 50,000 per block (`:159`). Ticket churn at 50 obj/s is a `Misc` of a few hundred bytes each, on the order of 6-second batches of a few hundred kilobytes, well under the churn limit. The persistent cost that does not churn away is the member tree.

Indexer retention of ordinary chain state (`ledger_state_retention: 1000` blocks in the readout §4.6) is irrelevant to bodies, because bodies are not chain state. A relay that learns tickets from an indexer must still check the block hash against a Midnight node. An indexer that omits a ticket censors that publisher until some relay sees the event another way. The defence is a relay that re-executes, which is what the chain-indexer already does for contract events (`notes/midnight-network-stack.md` §3.2).

Substrate pruning (full nodes default to 256 blocks in the docs, readout §2.1) does not prune the sidecar store. The sidecar has its own expiry.

## D7 Infrastructure actors

Launch set, phase 1: 8 to 16 relay operators, distinct networks as far as the operator list can make them. **Assumption** on the count. Admission is an allow-list of peer ids in the admit contract, changed by the same governance path that changes Midnight's permissioned committee: Root via Council and Technical Committee (`notes/midnight-network-stack.md` §2.2). Mainnet genesis has `num_permissioned_candidates: 10` and `num_registered_candidates: 0` (`midnight-node/res/mainnet/system-parameters-config.json:6-9`). The bus copies that launch shape and does not wait for open membership.

Validators are not relays. The committee is small and the block author is predictable under Aura. Putting the mesh on those nodes would share peer slots with GRANDPA and BEEFY and would offer a censorship point that already exists for transactions. The node registers protocols only in `new_full`; the ledger-sync comment says validators do not serve that protocol by default because snapshot work competes with authoring (`midnight-node/node/src/service.rs:610-644`). A private event mesh would compete the same way. `Cargo.lock` has no `libp2p-gossipsub` package (search of `midnight-node/Cargo.lock` returned no matches). Adding one is a node fork. v1 does not ask for that fork.

Each phase-1 relay runs a Midnight full node, or a private node it operates, plus the `pe-relay` process. The full node is how it sees finalized admit events. A relay that instead trusts the public indexer must document that trust. The indexer operator then sits in the ticket path.

Wallet providers and agent hosts are users' choices. A provider that holds `enc_sk` is inside the user's trust boundary and is not a protocol actor. A provider that is given only a stream of the whole shard is an Edge peer with an IP. It does not receive keys.

Payment: none on-chain in v1. Operators are paid by the same off-chain arrangements that fund RPC. A NIGHT staking path (MIP-0016, Draft, readout §2.3) could later pay relays. It is not a dependency.

End state: the allow-list is removed only after the D10 red-team fails to capture a mesh of scored peers. Until that run exists, the mesh stays permissioned. Open admission is Bitmessage's model; it is also the Sybil and eclipse setting Dandelion and GossipSub spend their mechanisms on. I will not put a date on it.

Safe mode and tx-pause can stop `send_mn_transaction` (`notes/midnight-network-stack.md` §2.2, §8). That stops new tickets and new `note` calls. Objects already ticketed can still move until their tickets age out. Governance pause is a liveness risk the bus inherits because admission is a Midnight transaction.

## D8 Network tether

Run the bulk path as a sidecar libp2p process. The ledger anchors admission and application commitments. Gossip carries bytes. The indexer is a way to read the admit contract, not a way to read private events.

Rejected as the primary path:

- The current node stack, as the place the bytes flow. No application pubsub exists; consensus gossip uses 32-byte topics for GRANDPA and BEEFY only (`notes/midnight-network-stack.md` §1.5). A new notification protocol requires every operator to run a forked binary (§8). Peer slots are the node's slots. Upstream defaults are 8 outbound and 32 inbound full peers; Midnight does not set them in its own code (readout §1.8, marked upstream and not verified against the pinned SDK). I am not putting event traffic in that budget.
- Ledger and indexer alone. `Misc` is 32 + 256 bytes. Events over 1 KiB are dropped silently (`ledger-9.1.0.0-rc.5:onchain-vm/src/vm.rs:43`). `emit` is public by construction (`minokawa-compact` disclosure rules, readout §3.2). Finality is on the order of 18 seconds before an indexer will show the event. Contracts still cannot subscribe. A 50 obj/s bus of 1 KB bodies is about 50 KB/s of public ciphertext, which the chain could physically carry and should not, because every byte is a public, permanent-until-prune log and the payer's transaction reveals `v_fee` and timing.
- A Sphinx mix overlay. Constant-size packets and per-hop group elements buy sender anonymity at mix latency (`2009-danezis-sphinx`, catalog note). That is a different product from a 2-second event bus. The trilemma says we do not get both for free (`2017-das-trilemma`).

Fallback, if a sidecar is operationally refused: one Substrate notification protocol, genesis-scoped name, carrying the same `EVENT` bytes, `sc-network-gossip` topic equal to the 32-byte shard id, enabled only on non-validators, behind a flag, after a measurement that GRANDPA round time and block propagation stay inside their current envelopes. The object layout does not change. I do not recommend starting there. The ledger-sync protocol is the pattern for how painful a custom protocol is (`service.rs:610-644`): it is already special-cased so validators do not serve it.

Changes required:

- Midnight node: none for the recommended path.
- Indexer: none, if `Misc` events on the admit contract are already returned by `contractEvents`. That subscription is `@beta` (`schema-v4.graphql:1971`). No new filter. Relays filter `name` locally. `Misc` has no indexed-field filter (readout §4.3); that is acceptable because the relay asks for one contract address and scans names itself.
- Wallet: a local agent API, not a connector change.
- Compact: one new contract. No new event struct. `Misc` is enough. No VM change.

The sidecar uses its own Ed25519 peer key, not the node's, so a node peer id is not an event-mesh id.

## D9 Threats and open risks

| Attack | Defence in v1 | Residual |
|---|---|---|
| Spam flood | Ticket, 30 per member per epoch, 10% block budget, relay rate cap | A rich NIGHT holder can fill the budget. That is the cost model, not a failure of it. |
| Ticket griefing | One-time `pub_pk` and `relay_sig` over header and body | The purchase transaction still reveals the ticket before use, so the buyer should publish soon after finality or accept a timing link. A leaked one-time signing key burns that one ticket. |
| Replay | `object_id` dedup, ticket single-use through `epoch + 2`, expiry | A partitioned minority can accept a second spend of a ticket it has not seen. The mesh heals by `object_id` once the partition ends; two conflicting bodies cannot both be valid under one signature. |
| Sybil relays | Permissioned allow-list at launch; GossipSub `D_out` so inbound peers cannot be the whole mesh (`2020-gossipsub-v11-spec`, outbound quotas); P4 on bad tickets | After the allow-list is removed, Sybil resistance is unproven for this mesh. |
| Eclipse | Allow-list plus operator diversity; stem will not forward to a peer in the same IPv4 /16 when the stem has another choice | A user whose only path is one relay is eclipsed by that relay. Edges should peer with two relays when they can. Two is a design choice, not a measured anonymity set. |
| Deanonymization of the author | Header has no long-term identity. Stem length 2, `FloodPublish` false. Fluff injector is the first mesh sender | The stem predecessor sees the author IP. A global observer is out of scope. A colluding stem defeats the hop. Simulation in D10 decides whether the stem is worth its code. |
| Subscriber deanonymization | Full-shard fetch, no content topic | The stream relay sees the edge IP and the fact of subscription to shard 0. Size and timing of which objects the edge trial-opens are local and do not cross the wire. |
| Indexer abuse | Tickets are checkable against a node. Bodies are not stored at the indexer. No viewing key is sent | An indexer that is the only ticket source can omit events. Run a node. |
| Censorship | Any honest relay that has the object can serve it. Tickets are public events, so a relay cannot pretend a finalized ticket does not exist if it has the block | Governance pause stops new tickets. A unanimous relay cartel can refuse a valid object. The allow-list makes that cartel small on purpose at launch. |
| Key compromise | Separate `admit_sk`, `enc_sk`, `sig_sk`. Rotate topic keys | `enc_sk` compromise opens history. No ratchet. |
| Parser attack | One layout, reject on mismatch, no `eval` of types, length taken from `size_class` not from the peer | Bitmessage's 2018 RCE came from dispatch on attacker-controlled message types (`design/evidence/bitmessage-guide.md`, CVE-2018-1000070). The residual is ordinary implementation bugs. Fuzz the parser before the mesh exists (D10). |
| Malformed Compact log | Ticket payload must match the 68-byte layout or relays ignore the event | A buggy admit contract can halt admission. The contract is in the phase-0 test set. |
| Quantum record-now | Nothing in v1 | A future `/midnight-pe/2` can swap in a hybrid KEM. Ciphertext growth has to fit a size class or force a new class. I am not reserving bytes for it in v1; reserved-zero means reserved-zero. |

Cover traffic, mix delay, oblivious retrieval, and PIR are omitted. Oblivious message retrieval removes trial-download and costs a homomorphic scan (`2021-liu-omr`, catalog note: on the order of a dollar per million messages scanned on the authors' figures). At 50 obj/s a single scanner is about 4.3 million objects a day. Ten thousand users each scanning that board is tens of billions of message-scans a day. I will not make every relay run that. Multi-server FMD (`2025-goes-multiserverfmd`) is a candidate for a later light-client proposal, not for this header.

## D10 Build and verification plan

Phase 0, no public mesh. Executable parser and admit circuit on a ledger-9 devnet. Gates: every mutated header in a conformance list is rejected; a non-zero reserved byte is rejected; a short body is rejected; a long body is rejected; pad bytes other than zero are rejected; one ticket cannot authorize two bodies; an admit call's measured byte size and compute time are published. If that call exceeds 8 KB or does not fit beside ordinary traffic inside 10% of `blockUsage` and the 2-second compute budget, the operating point and the batch size change before any relay is written. Formal check: a small model of the accept predicate (version, lengths, expiry, ticket unused, signature) in a tool the team already runs. Quint is a fit if the team uses it; a property-based test that enumerates the predicate is enough if the model stays this small. I am not asking to model GossipSub again; an ACL2s model of GossipSub v1.1 already exists (`2023-kumar-gossipsub-acl2s`) and does not know our header.

Phase 1, private mesh of 16 instrumented relays. Traffic at 50 obj/s with the mix in D5. Measure: per-relay send and receive against the 2.21 Mbit/s estimate; p50 and p99 relay-to-relay delay; CPU share; store size after six hours; fraction of objects that fail to reach at least 15 of 16 relays before expiry. Acceptance: within 2× of the bandwidth estimate, p99 ≤ 10 s, store under 1 GB, delivery fraction ≥ 0.99 for unexpired objects with no induced loss. Spy run: 10% of relays log first-seen peer. Report precision and recall. If precision is more than twice the `p²` floor from `2018-fanti-dandelionpp` at that spy fraction (`p = 0.1` gives `p² = 0.01`, so the gate is 0.02), the stem stays in the code only as a delay and the specification's privacy section drops any source-hiding sentence. The 2× multiplier is my gate, not a number from the paper.

Phase 2, wallets and one consuming contract. An agent opens a class-0 object and a class-1 object, calls `note`, and a second process sees the commitment only after finality. A wallet on localhost receives the opened payload and does not open an indexer subscription to do it. A phone build is not a gate. Parser fuzzing from phase 0 still runs in CI.

Phase 3, the allow-list decision. A red-team with a budget of peer ids equal to the honest set tries to occupy meshes under the phase-1 scoring parameters. Capture means honest publishers' objects fail the phase-1 delivery fraction. If they succeed, the allow-list stays. If they fail, a proposal can remove it. That proposal is a new decision, not an automatic flag day.

Change course if any of these is true:

- The admit circuit cannot be paid for inside the block budget at a rate the application actually needs. Then the bus is the wrong layer for that rate, and those events should be fewer, larger, class 3, or they should not exist.
- Phase-1 bandwidth is more than 2× the estimate. Then `D` or the size mix is wrong and the caps in D5 are rewritten from the measurement.
- The product requires anonymity against a global passive observer. v1 cannot be patched into that. The replacement is a mix or a cover-traffic design, with latency as a requirement rather than a 2 s p50 (`2017-das-trilemma`).
- Ledger 9 `emit` does not activate. Then there is no ticket event. Do not invent an off-chain CA. Wait, or run only a lab mesh with a file of tickets.
- A measured light-client retrieval, FMD or OMR, beats full-shard download on cost and has a written bound we can implement. Then add a protocol `/midnight-pe/retrieve/1`. Do not add a content topic to `EVENT`.

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Event format | One `EVENT`, 192-byte header, four size classes, exact lengths, version only by protocol id | Bitmessage varint objects and unknown-type relay; Waku protobuf with clear `content_topic`; Whisper 4-byte topic; SCALE or TLV extensions | `2012-bitmessage-protocol-specification` object header; `2020-vac-waku2-message-spec`; `2017-eip-627-whisper`; `ledger-9.1.0.0-rc.5:base-crypto/src/hash.rs:93-94`; `rust-yamux/yamux/src/lib.rs:45`; `ledger-parameters-config.json:152` | High on the layout; medium on TTL numbers | A phase-1 store or CPU measurement that cannot meet D5 inside these classes |
| D2 Private | Confidential payload; topic hidden from relays; no FS; no global-passive claim; known keys are testable | FMD tags; clear topics; ack objects; a claim of source anonymity | `2017-das-trilemma`; `2021-beck-fmd`; `2021-seres-fmdfalsepositives`; `2018-fanti-dandelionpp`; `design/evidence/bitmessage-guide.md`; `schema-v4.graphql:552` | High | A product requirement for global-passive anonymity, which selects a different system |
| D3 Pub/sub | Shard flood, trial open, `seq` inside the seal, contract consumes by a later `note` | Per-topic meshes; Waku Filter; indexer `contractEvents` as the private path; chans; MLS as the bus | `2020-vac-waku2-filter-spec`; `schema-v4.graphql:548-552,1971`; `notes/midnight-network-stack.md` §5.4; `2012-bitmessage-wiki-faq` via the guide; `vm.rs:43` on the ledger-9 tag | High | A contract primitive that can read off-chain bytes, which does not exist in the VM |
| D4 Sustainable | DUST-bought single-use tickets; relays unpaid; 10% block budget; PoW not used | Per-object PoW; RLN slashing; relay fees taken from `v_fee` | `2015-schaub-bitmessage-antispam`; `2022-taheri-waku-rln-relay`; `dust.rs:1765` on the ledger-9 tag; `ledger-parameters-config.json:158-175`; `runtime/src/lib.rs:292,305-311` | Medium, because admit tx size is still an assumption | Measured admit-call size or compute that blows the 10% budget at the needed rate |
| D5 Performance | 50 obj/s per shard, Relay-A about 2.2 Mbit/s mesh, p99 ≤ 10 s hot path, `D = 6`, flood-publish off | Sizing to gossip line-rate; phone clients on the mesh | Arithmetic above; `2020-gossipsub-v11-spec` parameter table; `ledger-parameters-config.json:124`; chain mint bound from D4 | Medium | Phase-1 numbers outside 2× on bandwidth or outside the latency gate |
| D6 Storage | Keep until expiry; about 100 MB at the operating point; 2 GiB hard cap; bodies off the ledger | 28-day flood retention; putting bodies in contract state | TTL table; `ledger-parameters-config.json:159-160`; Bitmessage expiry in `2012-bitmessage-protocol-specification`; readout §7.5 on rent | High on the split; medium on the 100 MB figure | A size mix much heavier than the 70/25/5/0.1 assumption |
| D7 Actors | Permissioned sidecar relays, not validators; wallets and agents local; no on-chain relay pay | Validators as the mesh; open membership at launch; `connect(viewingKey)` for private events | `system-parameters-config.json:6-9`; `service.rs:610-644`; readout §2.2–2.3 | High | A red-team in phase 3 that fails to capture the mesh, which is the condition for opening admission |
| D8 Tether | Sidecar GossipSub plus ledger tickets; node, indexer, and Compact unchanged except one contract | In-process Substrate gossip; ledger-only bus; mixnet | No `libp2p-gossipsub` in `midnight-node/Cargo.lock`; `MAX_LOG_EMITTED` on the ledger-9 tag; `Misc` in `midnight-events.ss:71-74`; readout §1.5 and §8 | High | An operator constraint that forbids a second process, which triggers the non-validator notification-protocol fallback |
| D9 Threats | Tickets, permissioned mesh, stem as an unclaimed heuristic, parser reject rules | Cover traffic; OMR on the hot path; security claims for the stem | `2018-fanti-dandelionpp`; `2021-liu-omr` catalog note; CVE narrative in the Bitmessage guide | Medium | Phase-1 spy precision inside the D10 gate, which would let the spec claim a measured stem property and nothing stronger |
| D10 Build | Parser and circuit first; 16-node sim with a numeric gate; allow-list removed only after a failed red-team | Shipping a public mesh before the admit call is measured | Block limits in `runtime/src/lib.rs` and `ledger-parameters-config.json`; `2023-kumar-gossipsub-acl2s` | High on the order of work; low on calendar time | Any phase gate failing in the way its own "change course" line describes |
