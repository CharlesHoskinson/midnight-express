I'll read the charter first and then the local evidence it requires, and write the Round 1 proposal from that alone.The charter fixes the ten decisions and the evidence rules. Next I read the Midnight stack notes, the graph overview, and the Bitmessage starting point.The baseline is Midnight’s existing events and indexer. I’ll check the code and the papers that would justify anything beyond that.Version 1 is a sealed-payload convention on one ledger contract, not a new network. Publishers pay a normal Midnight transaction to `emit` one fixed-size ciphertext; every subscriber downloads that contract’s whole `contractEvents` stream and trial-decrypts locally, the way a shielded wallet already scans `zswapLedgerEvents`. That buys content confidentiality and hides the topic from relays and from the indexer. It does not buy forward secrecy, volume privacy, or anonymity against a global observer, and those gaps are not filled in v1. Gossip overlays, mixnets, PIR, oblivious retrieval, fuzzy detection, MLS, ratchets, proof-of-work, Dandelion, and on-chain subscriptions are cut until a measurement in D10 fails.

Facts below are from the local ledger-9-generation tree (node runtime `spec_version` 003_000_000 at `midnight-node/runtime/src/lib.rs:276`, Compact `Misc` in tree). The docs’ mainnet matrix still lists node `node-1.0.300` and Compact toolchain `toolchain-0.31.1` (`midnight-docs/docs/relnotes/support-matrix.json:14`, `:38`) and on-chain runtime `onchain-runtime-3.0.0` (`:82`). `emit` is a later generation. v1 has nowhere to run until that generation is the one a target network actually executes.

## D1 — Event format

One Compact event, always the same size. `Misc` is tag 10, 288 bytes: `name: Bytes<32>`, `payload: Bytes<256>` (`minokawa-compact/compiler/midnight-events.ss:71-74`). `emit` accepts only standard event structs, requires disclosed fields, and is forbidden in the constructor (`minokawa-compact/doc/compact-reference.mdx:3497-3507`). CoIP-0003, which is Draft, already refuses to put encryption, topic filters, or recipient keys inside the VM (`minokawa-compact/coips/coip-0003.md:107-109`). v1 follows that cut: the chain stores ciphertext, and clients do the cryptography.

The bus contract exports one circuit, `publish(name, payload)`, which emits and writes no ledger cell. The call sits in the guaranteed segment, one emit per transaction, so a failed fallible segment cannot drop it (`midnight-network-stack.md` §3.2). There is no second entry point.

**Visible to every relay, validator, indexer, and chain observer:** contract address, entry point `publish`, event type `Misc`, block time, transaction hash, indexer `id`, the 32-byte `name`, and the 256-byte payload as opaque bytes. `name` does not carry a topic. It is constant for version 1:

| Offset | Length | Value |
|---|---|---|
| 0 | 4 | ASCII `MPE1` |
| 4 | 1 | `0x01` |
| 5 | 27 | zero |

A subscriber discards any other `name`. Two topics are indistinguishable in public fields. That is testable: encrypt the same-length body under two keys and compare `name`.

**Sealed payload**, ChaCha20-Poly1305 (12-byte nonce, 16-byte tag). The same AEAD is what a Zcash wallet trial-decrypts on every note (`2018-hopwood-zcashprotocol`). Associated data is the ledger’s canonical contract-address bytes followed by the 32-byte `name`, so a ciphertext cannot be replayed into another contract. Layout of the 256 bytes:

| Offset | Length | Content |
|---|---|---|
| 0 | 12 | nonce, random |
| 12 | 228 | ciphertext of the plaintext below |
| 240 | 16 | tag |

Plaintext is exactly 228 bytes, big-endian, canonical padding:

| Offset | Length | Content |
|---|---|---|
| 0 | 1 | `0x01` |
| 1 | 1 | flags, must be `0` |
| 2 | 4 | `seq` |
| 6 | 16 | `msg_id`, random |
| 22 | 1 | `body_len` ≤ 205 |
| 23 | `body_len` | body |
| rest | | zeros; non-zero padding is a reject |

Maximum body is 205 bytes. A longer message is an application problem: send another event. v1 does not depend on multipart `Misc` (MIP-0019 is Proposed). The VM’s 512 KiB `log` ceiling and the 1 KiB silent drop (`L9:onchain-vm/src/vm.rs`, as read in `midnight-network-stack.md` §3.2) are both above 288 bytes, so a well-formed v1 event is in the region the VM keeps. Do not emit anything larger “because the VM allows it.”

`seq` is a hint from one writer who holds the topic key. It is not a chain counter. Many writers who share a key will collide; consumers then use chain order and `msg_id`. The indexer `id` (`schema-v4.graphql` `ContractEvent.id`) is the only cursor.

**Lifetime.** No expiry field and no rebroadcast. Bitmessage stored objects for two days and rebroadcast when no acknowledgement arrived (`2012-warren-bitmessage-whitepaper`, §6). An acknowledgement is also how an eavesdropper localises the receiver (same paper, §7). v1 keeps neither. Retention is an indexer policy of 14 days, matching mainnet `global_ttl` of 1,209,600 seconds (`midnight-node/res/mainnet/ledger-parameters-config.json:176`). After that the event is gone. Block-body retention on full nodes is **unknown**; consumers use the indexer, or their own indexer, not a full node’s state (the node drops ledger events: `midnight-node/ledger/src/ledger_9/mod.rs:460-470` returns roots, hashes, addresses, and UTXO deltas, not logs).

**Cut from the envelope:** streams, `getpubkey`, embedded acknowledgements, proof-of-work nonce, Dandelion stem flag, per-recipient tag, content topic, size classes, JSON/CBOR/protobuf. One encoding, one size.

## D2 — Definition of “private”

v1 claims four properties and no others.

| Property | Holds against | Because |
|---|---|---|
| Content confidentiality | relay, indexer, chain observer, subscribers who lack the key | AEAD under a 32-byte topic key |
| Topic privacy | the same parties | topic is not on the chain; the subscription is the whole contract |
| Payload integrity under that key | the same parties | AEAD tag, plus associated data bound to the contract |
| Chain-level publisher unlinkability | a chain observer who does not see the submitter’s IP | a Midnight transaction has no Substrate signer; the DUST spend shows `v_fee`, a nullifier, and a commitment (`midnight-network-stack.md` §3.1, §3.4) |

**Leakage.**

| Observer | Learns | Does not learn |
|---|---|---|
| Relay, full node, validator | contract, `publish`, constant `name`, ciphertext, `v_fee`, block time, block author, tx hash | topic, body, DUST payer |
| Indexer the client chose | the above, plus client IP, the fact of a subscription to this one contract, and the cursor | which ciphertexts opened, the topic key |
| Chain observer | the public columns, historically | topic, body, payer |
| Colluding minority of the 10 permissioned authors | whatever those authors’ slots reveal, and the ability to omit a tx from a slot they produce | plaintext |
| Global network observer | ingress IPs at the RPC and the indexer, plus everything on the chain | topic, unless an endpoint is compromised |
| Another subscriber | bus volume and timing, and any topic whose key they hold | other topics’ bodies |

Mainnet’s D-parameter is 10 permissioned seats and 0 registered (`midnight-node/res/mainnet/system-parameters-config.json:6-9`). “Minority” means a set of those authors that does not by itself finalise the chain. The exact GRANDPA vote threshold was not re-derived here.

**Out of scope, on purpose.**

- Forward secrecy and post-compromise security. HPKE itself does not give forward secrecy against recipient-key compromise (`2022-barnes-rfc9180`, §9, “HPKE does not provide forward secrecy with respect to recipient compromise”). A Double Ratchet is a pairwise session with continuous key agreement (`2018-alwen-double-ratchet`). MLS gets group forward secrecy and post-compromise security from Update and Remove (`2023-barnes-rfc9420`). A shared topic key has neither, and v1 does not pretend.
- Strong anonymity against a global passive adversary. The anonymity trilemma says strong anonymity, low bandwidth, and low latency cannot all three hold (`2017-das-trilemma`, abstract). v1 spends bandwidth on one stream so the indexer cannot see the topic. It does not spend mix delay or cover traffic, and it does not claim the strong corner.
- Volume and timing privacy. Publication time is the block time. A mix in front of an RPC cannot erase a ciphertext once it is in a block. Loopix’s order-of-seconds mix delay and cover traffic (`2017-piotrowska-loopix`, abstract) would hide the path to the RPC, which is an IP problem, and would leave the chain record intact.
- Hiding “this client uses the bus” from the indexer it talks to. The API requires a contract address (`schema-v4.graphql:548-552`).
- Endpoint compromise, governance pause, and quantum adversaries.

At low volume the statistical anonymity set is small: a block with one bus transaction has one publisher. Shielding removes the signer; it does not invent extra publishers. Cover transactions are rejected. They cost DUST, they are visible as volume, and they would be empty events subscribers must download. The Zcash anonymity literature is the place to look before anyone adds cover (`2018-kappos-zcash-anonymity` is in the catalog; it was not used as a numeric source here).

## D3 — Publish and subscribe

A topic is a uniform 32-byte key, distributed out of band. It is not a passphrase. Bitmessage chans are a shared passphrase turned into an address (`2012-bitmessage-wiki-faq`, “What are chans?”). Low-entropy keys are the setting where one ciphertext can open under many keys (`2021-len-partitioningoracle`: AES-GCM and, more narrowly, ChaCha20-Poly1305 are not key-committing). v1 forbids passphrase topics. Residual for a public topic whose key is already known to the attacker: one crafted ciphertext might open under two such keys. That is confusion, not a confidentiality break. A committing AEAD is cut until that residual is observed.

There is no subscribe message, no on-chain topic registry, and no DHT lookup. A registry would be a public list of interests. A filter subscription would hand the topic to a peer: Waku’s own threat text defines receiver anonymity as subscriber-topic unlinkability, and names subscribing to a content topic as the action that breaks it (`2024-vac-adversarial-models`, “Receiver Anonymity”; the filter protocol exists so a light node receives only the content topics it names, `2020-vac-waku2-filter-spec`). GossipSub mesh peers learn topics through `JOIN` and `GRAFT` (`2020-vyzovitis-gossipsub`). The indexer cannot filter `Misc` by field prefix anyway: prefixes apply to standard events only (`schema-v4.graphql:557-560`).

**Publish.** Hold the key and enough DUST. Build one payload. Submit `publish` through an ordinary node RPC. **Subscribe.** Open `contractEvents` for the single bus address, type `MISC`, resume from `id` (`contract_event.rs:14-22`). Ignore foreign `name`s. Try each topic key. Deliver on AEAD success. Deduplicate by indexer `id` (the stream is at-least-once; midnight-js already tells consumers to dedup by `id`) and, for a second submission of the same body, by `msg_id`. Order by indexer `id`, which follows block order and in-transaction emission order.

**Back-fill** is the same query, paged. The query limit defaults to 100 and is clamped to 1–500 (`midnight-network-stack.md` §4.7). Then switch to the live subscription. There is no exactly-once promise and no causal order beyond the chain.

**Smart contracts do not consume events.** Nothing in the VM reads a log back (`midnight-network-stack.md` §5.4, §8). An agent that decrypted an event may later submit a normal transaction. That transaction is public in the ordinary way (address, entry point, transcript). The bus does not hide it, and v1 adds no relayer role.

**Wallets and agents** use the same local scan. The shielded wallet already takes the global `zswapLedgerEvents` stream and decrypts locally (`midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:220-229`). Copy that shape. Do not call `connect(viewingKey)`: that path stores the viewing key for the indexer operator (`midnight-network-stack.md` §4.4). The DApp connector has no event API (`midnight-dapp-connector-api`); a DApp opens the indexer URI the wallet already reports. No new wallet RPC.

A public broadcast is the same format with the key published beside the contract address. Content confidentiality is then void for anyone who reads the key. There is no second message type.

## D4 — Sustainable model

The publisher pays DUST. Carrying and ordering are the block the validators already produce. Storing for readers is the indexer those readers already run or already trust. v1 adds no relay market, no indexer invoice, and no proof-of-work.

The read-out’s inference, which this proposal does not re-prove from `dust.rs`, is that `v_fee` is burned rather than credited to a validator or a treasury (`midnight-network-stack.md` §2.3). Block rewards are stranded at launch (`mps-0019`, Proposed, as cited there). Paying “event relays” would invent a payroll the chain does not have. Indexer and proof-server operators have no on-chain fee path either (same section). That is acceptable only because v1 gives them no new duty: a chain indexer already materialises contract events.

**Spam.** The price is the fee market. There is no per-sender limit at the Substrate layer for ordinary Midnight transactions (`midnight-network-stack.md` §1.6). Bitmessage charges proof-of-work to every object; the one peer-reviewed pass at that formula finds that legitimate users and spammers face the same work, and the author’s own improvement only halves the harm (`2015-schaub-bitmessage-antispam`). Stacking Hashcash on top of a ZK proof and a DUST fee charges the legitimate publisher twice. Rate-limiting nullifiers, as in Waku RLN (`2022-taheri-waku-rln-relay`), need a membership set, a gossip network, and slashing. An on-chain epoch nullifier would add another proof and persistent set writes. Both are cut until the fee market is observed to fail.

**Arithmetic at genesis parameters, inference, to be replaced by a measurement.** The read-out gives overall price 10 and unit factors, and about 0.01 DUST per KB of block usage (`midnight-network-stack.md` §7.3; parameters at `ledger-parameters-config.json:169-175`). A transaction whose size is the sum of a 2,912-byte DUST-spend proof and a 4,832-byte call-proof estimate is about 8 KiB and about 0.08 DUST, with the log’s churn term negligible beside that (churn limit 50,000,000 bytes, `:160`). The design cap in D5 is 4 events per block: 0.32 DUST per block, about 4,600 DUST per day if the cap is full for 14,400 blocks. The read-out’s cap is 5 DUST per NIGHT, so filling the cap all day is on the order of 900 NIGHT of generation capacity, not a free flood and not a cryptographic puzzle. Prices move each block toward 50% fullness (`midnight-network-stack.md` §7.2). A sustained flood raises the price for every Midnight transaction, which is the brake already shipping.

**Low load.** Empty blocks cost the bus nothing. The anonymity set shrinks as in D2. v1 does not generate decoys. **High load.** The publisher’s transaction competes in the ordinary pool (upstream default 8,192 entries and 20 MiB, not overridden by Midnight; longevity 600 blocks, about one hour, `pallets/midnight/src/lib.rs:592`). What does not fit is not stored by the bus. The publisher resubmits. There is no side mempool.

## D5 — Performance requirements

No percentile below is a forecast. Prove time for this circuit is **unknown**. The Zswap figure of about 190 ms on a 32-core server and 5–30 s on a laptop is a Proposed MPS about a different proof (`mps-0004`). Finality is “usually about 3 blocks / 18 s” in a proposal, not a constant (`mps-0028`). The indexer’s 400-block constant is not a delivery delay: blocks within one GRANDPA session of the tip are fetched by hash, older blocks by height (`midnight-indexer/chain-indexer/src/infra/subxt_node.rs:83-86`, `:423-429`). Live events move when the finalized block is indexed. Sustained `contractEvents` throughput is **not found** in the repos.

**Design cap.** 4 events per block on the one bus contract, and never more than 5% of the 1,000,000-byte `blockUsage` limit. With measured transaction size `S`:

`cap = min(4, floor(0.05 × 1_000_000 / S))`

At the 8 KiB inference, 4 × 8 KiB = 32 KiB, which is 3.3% of `blockUsage` and 3.1% of the 1 MiB dispatch length (`runtime/src/lib.rs:312-313`). Slot time is 6,000 ms (`runtime/src/lib.rs:292`), so 4 per block is 40 per minute. That is a budget so the bus cannot become the block.

**Subscriber bandwidth, assumption until Phase 0.** Count 1,024 bytes on the wire per event, GraphQL included. 40 per minute × 1,440 minutes = 57,600 events/day × 1,024 = 56 MiB/day for a subscriber who takes the whole stream. The Bitmessage guide’s illustrative flood, which it labels as not a measurement, is about 28 MiB/day at 10 objects/min of 2 KiB and about 281 MiB/day at 100 objects/min (`design/evidence/bitmessage-guide.md`, scalability table). v1 at its cap sits near the low scenario, and only bus subscribers pay it. Other full nodes pay only the block bytes.

A 14-day catch-up is about 790 MiB at that assumption. Paging at 500 rows is about 1,600 queries. The wallet’s shielded sync buffer is 10,000 events (`Sync.ts`, as cited in the read-out); catch-up uses the query, then the socket.

**Fan-out.** Validators do the work once. One thousand always-on subscribers at 56 MiB/day are about 55 GiB/day of indexer egress, about 5 Mbit/s average. That is an indexer capacity question, not a consensus question. One hundred thousand such subscribers are about 500 Mbit/s, which is the point at which those subscribers run their own indexer against a node, an option that already exists (standalone indexer). v1 does not add a mesh to spread that read.

**CPU.** Validators and indexers do not trial-decrypt. A subscriber at 40 events/min and 256 topic keys performs about 170 AEAD opens per second of a 228-byte body. The opens-per-second figure is **unknown** and is a Phase 0 measurement. The acceptance bar is under 5% of one laptop core at 256 keys. A 1-byte view tag, the Monero scan shortcut (`2021-monero-mrl73-viewtags`), leaks a public hint. It is cut until that CPU bar fails.

**Latency gate, not a claim.** End-to-end, from the submit call returning to a remote subscriber decrypting the event, on an unloaded preview network: p50 ≤ 60 s or the product does not fit v1 (trigger T1). The floor is finality, on the order of 18 s if the doc holds, plus prove time, plus indexing. Anything that needs less than one 6-second slot is a different system.

| Class | Duty | v1 budget |
|---|---|---|
| Publisher with a proof server | one tx per event | fee and size measured in Phase 0; cap above |
| Always-on agent | full stream, ≤ 256 keys | 56 MiB/day at the cap, assumption |
| Wallet, periodic | same bytes, catch-up | ≤ 14 days, then query |
| Public or self-run indexer | store and serve | ~28 MiB/day row-storage assumption (D6) |
| Validator / full node | ordinary block | ≤ 5% of `blockUsage`; no decrypt |

Concurrent subscribers have no protocol cap. The indexer config caps subscriptions per socket at 20 (`midnight-network-stack.md` §4.7). A global client cap is **unknown**.

## D6 — Storage

On the ledger, the ciphertext lives in the transaction log, not in contract state. Logs are churn, not persistent writes (`midnight-network-stack.md` §3.2, §7.3). No rent was found. Persistent state is not pruned, so the contract is forbidden to store the message, a counter, or a topic list. A persistent byte is on the order of 20 times a transmitted byte at genesis weights (same section). That ratio is the whole argument against an on-chain mailbox.

Indexer row size is **unknown**. Planning assumption: 512 bytes per event including the MIP-0002 sidecar’s “about 150 bytes,” which that MIP treats as a loose bound (`midnight-network-stack.md` §4.6). At the cap, 57,600 × 512 ≈ 28 MiB/day, about 390 MiB for 14 days. The same read-out records a preprod indexer anecdote of on the order of 300 GB, mostly contract state. Bus rows at this cap are noise beside that. Archive beyond 14 days is an operator choice, outside the protocol. There is no availability promise past the retention window, and no second archive network.

What a full node keeps is blocks and pruned state (default state prune 256 blocks, `midnight-docs` full-node page, via the read-out). It does not keep a queryable event log. Availability of v1 for a late subscriber is “an indexer that retained the window,” not “the ledger remembers.”

## D7 — Infrastructure actors

No new role.

| Actor | Admission | Trusted with | Paid by |
|---|---|---|---|
| Publisher | holds NIGHT that generates DUST, and can get a proof | the topic key it holds | itself, in DUST |
| Subscriber agent or wallet | chooses an indexer URL | its own keys | itself |
| Validator set | today’s rule: 10 permissioned seats, registered SPO seats later | inclusion and ordering, not plaintext | existing block production; event fees are not a new reward |
| Indexer operator | anyone can run standalone; the public deployment is whoever runs it now | availability and completeness, not content | no protocol fee |
| Proof server | the publisher’s choice | sees the witness of `publish`, which is the already-public name and payload | off-protocol, as today |
| Wallet provider | unchanged | must not receive topic keys | unchanged |

Governance can pause user transactions, including `send_mn_transaction` (`midnight-network-stack.md` §2.2). That is a real censor. v1 does not route around it with a side network, because a side network would be the product.

**Launch** is one immutable contract per network, only `publish`, address written down after deploy. The deploy transaction reveals the deployer. It does not reveal later publishers. **End state** is many self-run indexers over the same chain, which is the end state Midnight already has for wallets. A relay market is not the destination.

## D8 — Network tether

Use the ledger and the indexer. Nothing else.

The node’s network worker is `sc_network::NetworkWorker`; the litep2p alternative is commented out (`midnight-node/node/src/command.rs:326-327`). A search of `midnight-node/Cargo.lock` finds no `libp2p-gossipsub`. Substrate gossip is present for GRANDPA and BEEFY only. Adding a notification protocol means a forked binary on every operator (`midnight-network-stack.md` §8). Peer slots are shared with consensus. Yamux’s patched window is 256 KiB. None of that is needed to carry 32 KiB of bus transactions per block.

A separate libp2p overlay, a hybrid “hash on chain, body on gossip,” and a node-protocol fork are rejected. The hybrid still needs a spam regime, a retention story, and a privacy story for the gossip topic, and it loses the property the chain actually gives: one finalized order, paid for by DUST, with no new Sybil set. Waku’s relay is that hybrid’s cousin (GossipSub shards plus a store, and a filter that learns interests). Its scoring and mesh machinery is what the Least Authority audit and the later ACL2s work spent their pages on (`2020-leastauthority-gossipsub-audit`, `2022-kumar-gossipsub-formal`). v1 has no peers to score.

**Fallback,** if a public indexer is unacceptable: run the existing standalone indexer against a node you trust. Still no overlay.

**Changes.** No node change, no runtime upgrade, no indexer schema change, no Compact language change. The wallet may grow a scanner; the protocol does not require it. Do not build a temporary overlay while waiting for the ledger-9 event hard fork. That overlay would become the protocol.

## D9 — Threats and open risks

| Attack | Defense in v1 | Residual |
|---|---|---|
| Spam flood | DUST fee market and the 5% block cap | A wealthy holder can fill the cap and raise everyone’s price. Accepted. PoW and RLN stay cut. |
| Replay of a transaction | intent replay set, TTL ≤ `global_ttl` | A new transaction with the same body is a new event. Dedup `msg_id`. |
| Replay into another contract | AEAD associated data | |
| Deanonymisation of the publisher’s IP | none in the protocol | The RPC that accepts the transaction sees the IP. Substrate transaction gossip has no stem phase. Dandelion++ is a peer-gossip change with a defined spy-fraction adversary (`2018-fanti-dandelionpp`). Putting it only on bus traffic is a node fork; putting it on all traffic is a chain-wide project. Users who care pick the RPC, or a transport they already have. |
| Subscriber deanonymisation | full-stream download, constant `name` | The indexer learns IP and “uses the bus.” A topic filter would leak more (`2024-vac-adversarial-models`). |
| Indexer omission or invention | ciphertext does not depend on the indexer; a second indexer, or your own, is the check | A client of one indexer cannot cheaply prove inclusion. An inclusion SNARK is cut until an indexer is shown equivocating. Running a second indexer is the whole defense. |
| Indexer key theft | topic keys never go to the indexer | `connect(viewingKey)` remains a foot-gun for shielded sync and is unused here. |
| Censorship by authors or by safe mode | none beyond “submit to more than one RPC” | Permissioned authors can omit transactions from their slots. Governance can pause user calls. v1 does not route around the chain. |
| Eclipse / Sybil of a bus peer set | there is no bus peer set | The chain’s admission is the validator set. A private overlay would reintroduce this (`2002-douceur-sybil` is the classical statement; not re-argued here). |
| Key compromise | out-of-band rotation of the topic key | Past messages under that key stay readable. Future messages stay readable until rotation. This is the Bitmessage static-key fact, restated so nobody calls it forward secrecy (`2012-warren-bitmessage-whitepaper` construction; `2022-barnes-rfc9180`). |
| Malicious ciphertext opening under several keys | topic keys are uniform 32 bytes, not passphrases | Public, widely known keys remain in the Len setting. Accepted for v1. |
| Scan denial of service | fixed 256-byte body, one AEAD per key, fee-bounded event rate | Senders cannot inflate per-event work. The BIP-352 class of sender-chosen scan cost (`midnight-network-stack.md` points at this via the PB3 notes) does not apply. |
| Traffic confirmation | fixed size, single stream | Volume of the bus is public. Correlation of a publisher IP with a later block is in the IP residual above. |

Oblivious message retrieval is not a defense in v1. UnifOMR shows that OMR with strong detection-key unlinkability is at least as hard as PIR, and reports about 25 seconds and 4 MB for 2^19 messages of 612 bytes (`2026-fisch-unifomr`). Chor’s bound is the reason a single server, for perfect query privacy, sends the whole database (`1998-chor-pir`, opening). Pung’s own evaluation says that for multi-retrieval and small tuples, downloading the collection can beat PIR (`2016-angel-pung-1`, the k>1 paragraph: 4.5–36 MB per message, and sometimes the full download wins). Our record is 256 bytes and a subscriber often has several topics. Full download is the simpler side of that comparison until the board is large (T2).

## D10 — Build and verification plan

Build the convention. Do not build a network. The plan stops at Phase 2. A later mechanism is a new design, opened only by a trigger, and only the cheapest mechanism that answers that trigger.

**Phase 0, one contract, test vectors, measurements.** Circuit is `publish` and nothing else. No ledger writes. Vectors, all required to pass before any agent is written:

- I1. `name` is a function of the version only. Two keys, one body length, identical `name`.
- I2. Wrong key, flipped ciphertext bit, and wrong contract address in the associated data all fail closed.
- I3. Non-canonical padding and `body_len` > 205 fail.
- I4. The deployed contract’s ledger state is unchanged by `publish`.

Measure and write down, replacing every inference in D4 and D5: encoded transaction size, DUST fee at that network’s live `ledgerParameters`, prove time on the proof server that will actually be used, delay from submit to `contractEvents` on a finalized block, standalone-indexer catch-up in events per second, and AEAD opens per second at 1, 16, and 256 keys. There is no formal model of GossipSub, a mix, or a peer sampler, because those systems are not in the build. A Quint model of this payload is optional and small; the vectors are the gate.

**Phase 1, two processes.** One private topic, a private indexer, disconnect and resume from `id`, 24 hours at one event per block. Pass: zero false opens, delivery order equal to indexer `id`, the gap after a disconnect filled up to retention, duplicate `id` delivered once.

**Phase 2, stop.** A wallet-side scanner that never calls `connect(viewingKey)`, and a one-page threat note that matches D2, including the properties v1 does not claim. No node fork, no mainnet until the target network’s runtime is one that actually emits `Misc` and an indexer serves `contractEvents`.

**Triggers that open a new design, not a patch.**

- **T1.** Measured p50 end-to-end above 60 s on an unloaded preview, or a written product requirement for latency under one slot. Response: say v1 does not fit that product. An overlay proposal starts as its own design. It is not added here.
- **T2.** More than the D5 cap, sustained for 14 days, and measured subscriber ingress above 100 MiB/day. Response, in order: a second contract (splits the anonymity set; say so), then a detection tag whose false-positive rate is published. PIR or OMR only after those two are measured and still short. The UnifOMR 4 MB versus an ~800 MB catch-up is the comparison that would justify that work, together with a server-CPU number for the subscriber count we actually have.
- **T3.** A break of a property D2 claims, with the adversary named in D2. A break of forward secrecy, of global relationship unobservability, or of IP hiding does not count. Those were never claimed.
- **T4.** Measured bus storage above 2 GB in a month. Response: shorten retention. Do not add a DHT or a mailserver. Whisper-style mailservers are how a store learns who asked for what (`2018-status-whisper-mailserver-spec` is the pattern; v1’s indexer already has that trust boundary and does not need a second one).

**Course change I will accept.** A measured transaction size that blows the 5% rule at one event per block. A Phase 0 prove time that makes even the proof-server path miss 60 s by a wide margin, if the consumers truly need that bound. Evidence that DUST fees do not move under a flood that fills the cap. Evidence that the target network will not ship `emit` on any schedule an application can wait for. I will not add a mechanism because a paper exists, or because Bitmessage, Waku, or MLS has the feature.

## Decision table

| Decision | Choice | Rejected | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Format | One `Misc`: constant 32-byte `name`, 256-byte ChaCha20-Poly1305 payload, 205-byte body, 14-day indexer life | Multipart, size classes, topics in the clear, PoW nonce, acks, protobuf | `midnight-events.ss:71-74`; `compact-reference.mdx:3497-3507`; `coip-0003.md:107-109`; `2012-warren-bitmessage-whitepaper` §6–7; `2018-hopwood-zcashprotocol` | High | A measured need for bodies above 205 bytes at a rate the fee market can pay, with MIP-0019 actually shipped |
| D2 Privacy | Confidentiality and topic privacy against relays and the indexer; no signer on chain. No FS, no volume privacy, no global anonymity | Mixnet, cover traffic, ratchets, MLS, “untraceable” claims | `2017-das-trilemma`; `2017-piotrowska-loopix`; `2022-barnes-rfc9180`; `2018-alwen-double-ratchet`; `2023-barnes-rfc9420`; ledger has no tx signer (`midnight-network-stack.md` §3.4) | Medium | A consumer requirement for a property D2 lists as out of scope, plus a measured design that buys it cheaper than leaving the chain |
| D3 Pub/sub | One contract, out-of-band 32-byte topic key, full-stream trial decrypt, chain order, no on-chain consumer | Content-topic filters, DHT, registry, per-topic contracts, subscribe messages, contract wakeup | `schema-v4.graphql:548-560`; `2020-vac-waku2-filter-spec`; `2024-vac-adversarial-models`; `2020-vyzovitis-gossipsub`; `2021-len-partitioningoracle`; node discards logs at `ledger_9/mod.rs:460-470` | High | Indexer API gains a privacy-preserving filter that is cheaper than the full stream at the measured rate |
| D4 Cost | Publisher pays DUST; no new payroll; no PoW; no RLN | Relay fees, Hashcash, on-chain nullifier quota, decoy events | `ledger-parameters-config.json:151-176`; `2015-schaub-bitmessage-antispam`; fee-burn is an **inference** in `midnight-network-stack.md` §2.3 | Medium | A flood that fills the cap without moving the fee, or a measured fee far above the 0.08 DUST inference |
| D5 Performance | Cap `min(4, 5% of blockUsage)`; 60 s p50 gate; 56 MiB/day subscriber assumption | Sub-slot latency, view tags, gossip fan-out | `runtime/src/lib.rs:292,312-313`; `subxt_node.rs:83-86,423-429`; Bitmessage guide’s illustrative table; prove time **unknown** | Low | Phase 0 measurements. The cap formula is already written to absorb a different transaction size |
| D6 Storage | Ciphertext in the log (churn); indexer keeps 14 days; contract state stays empty | On-chain mailbox, mailserver, infinite retention | Churn vs persistent cost in `midnight-network-stack.md` §7.3–7.5; row size is an **assumption** | Medium | Measured rows above 2 GB/month (T4), which shortens retention and still does not add a store network |
| D7 Actors | Publishers, existing validators, existing indexers, local scanners. No new role | Dedicated relays, paid indexers, bus-specific admission | `system-parameters-config.json:6-9`; no indexer fee path in the read-out §2.3 | High | A legal or operational fact that the public indexer cannot be used and self-running one is infeasible |
| D8 Tether | Ledger plus indexer only. Wait for the `emit` generation. Fallback is a private indexer | Overlay, hybrid gossip, node fork, temporary side net | No `libp2p-gossipsub` in `midnight-node/Cargo.lock`; `command.rs:326-327`; `support-matrix.json:14,38,82` | High | T1, but only as a new design. Or evidence `emit` will not ship on a schedule the application can wait for |
| D9 Threats | Fee market, full-stream download, second indexer, out-of-band key rotation | Dandelion fork, inclusion SNARKs, OMR, FMD, peer scoring | `2018-fanti-dandelionpp`; `1998-chor-pir`; `2016-angel-pung-1`; `2026-fisch-unifomr`; `2021-len-partitioningoracle` | Medium | A demonstrated break of a property D2 actually claims (T3), or a measured indexer equivocation |
| D10 Plan | Phase 0 vectors and measurements, Phase 1 two-process soak, Phase 2 scanner, then stop. T1–T4 reopen | A network model of protocols we are not building; a Phase 3 inside v1 | This proposal’s D1–D9; CoIP-0003’s own decision to defer private events | High | Any of T1–T4, or a Phase 0 number that makes the 5% rule or the 60 s gate impossible for the proof-server path |
