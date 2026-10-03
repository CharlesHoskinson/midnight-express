I'll start with the charter and the five Round 1 proposals, then check the citations they rely on against the local Midnight code and the literature.The five proposals disagree on layout, admission, and what a relay may see. I am checking the Midnight lines and paper passages those disagreements rest on.The wire should be one opaque fixed-size object whose every byte is in the identifier. Relays see admission and length, not a tag, a clue, or a topic-derived shard. Of the four proposals, s1 is the only outer layout that is actually fixed, and it is also the only privacy section that refuses to treat gossip, fuzzy detection, or a rate-limiting nullifier as anonymity. o1 and o2 put a variable PLONK proof, a recognition tag or clue, and a shard byte on the relay path. s2 is fixed, then spends 354 of 1,024 bytes on a public token and trial-decrypts session headers the Double Ratchet specification does not associate across sessions. Ledger facts below were checked on tag `ledger-9.1.0.0-rc.5` (`67f9f972`). The `midnight-ledger` working tree is `ledger-8` and does not contain `MAX_LOG_EMITTED`. The node pins the ledger-9 tag (`midnight-node/Cargo.toml` patch table). The support matrix still lists mainnet Compact `toolchain-0.31.1` and `onchain-runtime-3.0.0` (`midnight-docs/docs/relnotes/support-matrix.json:38`, `:82`).

## D1 Event format

(a) Positions

- **s1:** One 4,096-byte cell: 128-byte header, 128-byte admission record, 3,840-byte sealed body; canonical CBOR and at most 16 fragments inside the seal; unknown versions and nonzero reserved bytes rejected; the identifier hashes the header and body and omits the admission signature.
- **s2:** Fixed 1,024-byte or 4,096-byte cells; 64-byte public header; 56-byte encrypted ratchet header; 354-byte public token; no fragments; unknown versions rejected before cryptography.
- **o1:** Body classes 1, 4, 16 and 64 KiB; public 16-byte tag and 68-byte clue; RLN (rate-limiting nullifier) proof planned at 3 KiB and still unknown; unknown versions relayed.
- **o2:** The same four body classes; public shard `H(topic_id) mod 16`; public RLN fields, ephemeral signature and an S-FMD clue; proof budget 4 KiB; unknown versions dropped.

(b) Evidence

s2’s token width matches RFC 9578. The Blind RSA token is `token_type` (2) plus nonce, challenge digest and key id (32 each) plus authenticator `Nk` (`2024-rfc9578-privacypass-issuance`, §6.3). Section 8.2.2 sets `Nk = 256`. The sum is 354 bytes. That is 34.6% of the small cell, as s2 says.

The 68-byte clue is real for the cited scheme. Beck’s CCA construction uses 68-byte flags for `p = 2^{-n}` up to `n = 24`, and the 0.548 ms test is at a 3% false-positive rate (`2021-beck-fmd`, the microbenchmark paragraph). o1’s “random bytes when unused, as Penumbra does” only half-matches. Penumbra adds dummy clues until clue count equals output count (`2022-penumbra-fmd`, the clue-count paragraph). That is padding of a count, not a permanent random clue slot.

o1 and o2 cite `L9:base-crypto/src/hash.rs:23` for the persistent hash. On the tag, line 23 is `use sha2::{Digest, Sha256}`. `persistent_hash` is SHA-256 at line 93, and `PERSISTENT_HASH_BYTES` is 32 at line 29. The hash family is right. The line is wrong.

o1’s 4,832-byte “unproven contract call” is `INPUT_PROOF_SIZE` at `zswap/src/structure.rs:634` on the tag, not a literal at `ledger/src/structure.rs:619`. `estimated_tx_size` adds one such proof per call on top of the serialized transaction. A DUST spend proof is 2,912 bytes at `ledger/src/dust.rs:2158`. Neither number is an RLN proof. o1 already marks `P` unknown. Until `P` is a fixed width, o1 and o2 do not have an envelope.

`global_ttl` is 1,209,600 seconds, exactly 14 days (`ledger-parameters-config.json:176`). `Misc` is a 32-byte name and a 256-byte payload, declared size 288 (`minokawa-compact/compiler/midnight-events.ss:71-74`). On the ledger-9 tag, `MAX_LOG_EMITTED` is `1 << 10` at `onchain-vm/src/vm.rs:43`, and the silent bound is applied at line 274. s2’s `:41` and `:268` are the neighbouring comment and a few lines off. The 1 KiB drop is real. Compact’s `max-emit-size` remains `2^19` (`compiler/events.ss`). MLS `PrivateMessage` carries `group_id` and `epoch` outside `ciphertext` (`2023-barnes-rfc9420`, the `PrivateMessage` struct in §6.3). s1’s reason to seal all of MLS holds. I did not re-open §16.4.

(c) Vote: **my alternative.** None of the four is a layout I would freeze. s1 is the only fully fixed object. Its identifier omits the admission signature, so two byte strings share one id.

The layout I will defend: one version, unknown versions invalid, reserved bytes required zero, big-endian or little-endian chosen once, a size class that selects an exact body length, and `object_id` equal to a domain-separated SHA-256 of every byte that is stored or forwarded. No public tag, clue, topic shard, or variable proof. A new layout is a new protocol id.

(d) Strongest objection to s1, the best of the four: an id that excludes the admission signature makes the forwarded bytes not a function of the id. A dedup cache can keep one issuer’s signature and forward another’s.

## D2 Definition of private

(a) Positions

- **s1:** Content confidentiality, and subscriber-interest privacy only when the fetch transcript is independent of what the client recognizes. Publisher unlinkability and timing privacy are explicitly not claimed. Adversaries R, C, G, A and I are named as games.
- **s2:** Content confidentiality and recipient concealment from infrastructure, plus session forward secrecy. Publisher unlinkability against a global observer is not claimed. Hybrid establishment is for harvest-now-decrypt-later only.
- **o1:** Claims P1–P7, including RLN publisher unlinkability and Dandelion++ source privacy against a colluding fraction. Global passive anonymity is excluded. FMD is limited to first contact.
- **o2:** Claims publisher anonymity against relays via RLN, topic privacy against relays, and relationship privacy as a consequence of those two. Global passive anonymity is excluded. The registration fact is public.

(b) Evidence

s1’s impossibility inequality is in the trilemma paper: no strong anonymity when `2ℓβ < 1 − ε(η)` (informal Lemma 1 in the text I opened). `2 × 10 × 0.01 = 0.2` is correct arithmetic, and s1 is right that it is not a ten-second engineering bound. I did not re-check every hypothesis s1 attaches to “Theorem 2.”

Guerraoui Theorem 5 matches s1’s quotation: for an undirected connected graph and `f > 1` curious nodes, any gossip protocol with ε-differential privacy needs `ε ≥ ln(f − 1)`, and if vertex connectivity is at most `f` then no finite worst-case ε (`2023-guerraoui-inherent-anonymity-gossiping`, Theorem 5). Curious nodes in that paper follow the protocol. Applying it to a GossipSub mesh is an inference. It does kill a “minority of relays, therefore anonymous” sentence.

Dandelion++ models a botnet fraction `p` and says an ISP or AS adversary is outside the paper (`2018-fanti-dandelionpp`, the adversary paragraphs). The precision floor “not below on the order of `p²`” is a bound stated there, for that graph. o1’s P5 cites those bounds for a stem on a GossipSub mesh. The paper’s construction is an approximately 4-regular anonymity graph. A two-hop stem does not inherit the bound. s1’s refusal of that claim is the citation that matches the text.

Seres shows a detection server can recover much of the social graph when it knows senders (`2021-seres-fmdfalsepositives`, the contributions paragraph). o1 and o2 cite that limitation and still ship a clue. Frank’s abstract says prior work found FMD unviable with selfish users (`2024-frank-anonymous-messaging-altruism`). That supports o2’s floor on `p`. It does not make a clue private.

s1’s indexer citations hold. `ContractEventFilter.contractAddress` is required (`schema-v4.graphql`, the filter input). `architecture.md:20` starts the wallet-indexer bullet; lines 22–23 say it trial-decrypts with the wallet’s viewing key. s2’s PLONK-with-KZG claim matches `midnight-zk/README.md` (“Plonk proof system using KZG commitments”). The conclusion that the system is not post-quantum is an inference from pairing-based KZG. I accept it.

o2’s “relationship privacy follows from P2 and P4” is the composition the Kuhn paper exists to forbid. s1 cites that paper for defining games. I did not re-open Kuhn §2. The catalog note describes a hierarchy of notions, which is the use s1 makes of it.

(c) Vote: **s1.**

(d) Strongest objection: the interest-privacy game holds the fetch schedule fixed. A client whose retry, error, or later contract call depends on which cell opened is outside the claim, and s1’s own leakage table already gives the relay the cursor, the online period, and the catch-up range.

## D3 Publish and subscribe

(a) Positions

- **s1:** One transport feed. Clients fetch every cell on a fixed cadence and repair the whole inventory from a second operator. Topics are capabilities distributed out of band. Contracts consume only by a later transaction.
- **s2:** The same single feed, plus publisher-specific sessions, a cap of 32 device ciphertexts per publication, and trial decryption of a 56-byte header under at most 256 keys.
- **o1:** One envelope, three modes: keyed PRF tags and day buckets, FMD inbox for first contact, and public tags. Mobile clients fetch a tag index and then bodies with four decoys. Consumption is a witness plus `HistoricMerkleTree.checkRoot`.
- **o2:** Sixteen shards with `shard = H(topic_id) mod 16`. Subscribers pick full-shard relay, paid shard download, or S-FMD at `p ≥ 1/64`. Contracts check an anchor ring.

(b) Evidence

The shielded wallet replays a global Zswap stream with local secret keys (`midnight-wallet/.../Sync.ts`, `replayEventsWithChanges` on `wrappedUpdate.secretKeys`). s1 and s2 cite this region fairly. It is a pattern for local recognition, not an existing bus API. `api.ts` is 385 lines. A search of that file finds no event or subscribe method. The slice `:70-203` is not the whole file; the conclusion is still true.

`checkRoot` on a `HistoricMerkleTree` tests past roots (`minokawa-compact/doc/ledger-adt.mdx`, HistoricMerkleTree `checkRoot`). Compact 0.33 rejects a cross-contract callee that invokes a witness (`toolchain-0.33.0.md:101`). o1’s witness-free `isAnchoredRoot` matches that restriction. The pseudocode is not the compiler’s syntax. `jubjubSchnorrVerify` exists (`exports.md`, the circuit at the `jubjubSchnorrVerify` heading). Ed25519 in Compact is a 32-byte key and a 64-byte signature (`exports.md`, `Ed25519Signature`).

s1 cites `onchain-vm/src/ops.rs:156` for `Log`. On the tag the `Log` opcode is at line 172. There is no network-subscribe opcode in the opcode list I searched. The “consumption is a transaction” conclusion matches the VM. The line does not.

The Double Ratchet header-encryption section says how a recipient associates a message with a session is outside the specification, then tries current, next, and skipped header keys inside the chosen session (`2016-signal-double-ratchet-spec`, §4.1). s2 cites §4.6 as if the specification defined cross-session trial recognition. It defines trial inside a session after association. `MAX_SKIP` is an implementer constant. s2’s value 1,000 is s2’s parameter.

RLN-v2’s internal nullifier is `poseidonHash([a_1])` with `a_1 = poseidonHash([a0, external_nullifier, message_id])` (`2024-vac-rln-v2-spec`, the formula block). o1’s nullifier shape matches. The recommended registration publishes `user_message_limit` and stores `poseidonHash(identity_secret_hash, userMessageLimit)` (same spec, method 2). o2’s “the proof hides the tier” is not that registration.

o2’s shard function is computed from `topic_id`. A relay sees the shard. Anyone who can guess the label can test which shard a topic occupies. That is a smaller leak than a clear topic, and it is not “topic only inside the body.”

(c) Vote: **s1**, for one feed and no relay-visible selector. Contract inclusion, if required, is o1’s `checkRoot` pattern added later, on a fixed commitment, not on a tag.

(d) Strongest objection: s1’s circuit authenticates a signature and a nullifier. It does not check that the ciphertext was disseminated. A party who can produce the witness can drive the contract without the bus having carried the event.

## D4 Sustainable model

(a) Positions

- **s1:** Publishers buy fixed admission records from issuers who see the buyer. Subscribers pay egress. Sponsors buy an idle floor. DUST pays ledger transactions only. Relays are not paid by the protocol. Prices are unknown until bids exist.
- **s2:** Publicly verifiable Privacy Pass stamps, object-bound, bought after encryption. Same split: DUST for ledger work, ordinary billing for relays. RLN is deferred because a revealed admission secret must not be a session secret.
- **o1:** DUST-priced RLN membership in a Compact circuit, proved off chain, verified by relays against a ledger root. Launch relays are unpaid. Operators emit cover. Privacy Pass pays services in a later phase.
- **o2:** NIGHT bonds and non-refundable fees fund a contract treasury. Double-signalling slashes the bond. The treasury pays anchors and challenged storage only. Relays are unpaid. DUST cannot pay them.

(b) Evidence

DUST is shielded and non-transferable (`dust-architecture.mdx:23`). A spend stores public `v_fee` (`ledger/src/dust.rs:469`) and sets the new note’s `initial_value` to `v_new - v_fee` (line 1765; s1’s `:1763` is two lines early). `LedgerBlockReward` returns `(0, None)` in both feature configurations (`midnight-node/runtime/src/lib.rs`, `LedgerBlockReward`). o2’s citation `dust.rs:469-474` for “fees are burned” is the struct and its debug field. The subtraction shows the fee leaves the note. I found no credit of `v_fee` to a relay. Treasury payout code in `semantics.rs` is commented out pending governance. “Burned” remains an inference, which o2 labels.

`overall_cost` at `base-crypto/src/cost_model.rs:408` takes the max of the normalized read, compute, and block-usage terms, then adds write and churn, then multiplies by `overall_price`. s1’s description matches. `STARS_PER_NIGHT` is `1_000_000` at `structure.rs:3362` and `SPECKS_PER_DUST` is `10^15` at line 3363. Cap arithmetic `5×10^9 × 10^6 / 10^15 = 5` DUST per NIGHT matches the dust document. `generation_decay_rate` is 8,267 (`ledger-parameters-config.json:166`). Time to cap `5×10^9 / 8267 ≈ 604,814` seconds matches the document’s “about one week.” One NIGHT at that rate is about 0.714 DUST per day, and the document’s 71 DUST per day for 100 NIGHT is the same quantity. The fee-price factors in the genesis file are `1 × 2^64` and `10 × 2^64`, not 1.0 in integer DUST. Any “0.06 DUST” figure is an inference through the readout’s scaling.

`receiveUnshielded`, `sendUnshielded`, and `unshieldedBalanceGte` exist (`exports.md:1203`, `:1211`, `:1241`). `mintShieldedToken` exists (`:1055`). A contract-held NIGHT bond is therefore an API possibility. `insertIndexDefault` “can be used to emulate a removal” (`ledger-adt.mdx`, that heading). The private-data guide says a `HistoricMerkleTree` is the wrong tree when items are removed, because `checkRoot` still accepts proofs against prior roots. o2’s slash-by-overwrite does not invalidate a proof against a root still inside the window.

Taheri reports RLN verification around 30 ms and Shamir shares of the identity secret (`2022-taheri-waku-rln-relay`, the verification sentence and §II-B). s1’s `100 × 30 ms = 3` CPU-seconds per second is arithmetic on that figure. Laurie and Clayton state a calculation of at least 5.8 seconds in the spam analysis (`2004-laurie-proofofwork`). o2’s “per email” is the surrounding argument. The cost-model proof price is `proof_verify_constant = 3,273,586,253` ps, about 3.27 ms, plus `4,555,132` ps per public input (`ledger-parameters-config.json:128-129`). Line 124 is the signature price, 97,304,512 ps, about 97 µs. o1’s range `:124-133` contains both. The 3.27 ms figure is a fee weight, and o1 says so.

o1’s `proofs.rs:108-128` is the embedded KZG verifier parameters, `VERIFIER_MAX_DEGREE = 14`, and the `bls_midnight_2p14` bytes. That is a degree-bounded parameter set. The wallet prover client posts transactions to `/prove` and imports `ledger-v8` (`HttpProverClient.ts`). It is not a verifier for a free-standing contract proof. o1 already marks that API unknown.

Nym’s paper says performance-score attacks cut the cost of dominating the active set by over 99% (`2026-cao-nymreputation`). That supports o2’s refusal to pay relays for a quality score. It does not test o2’s challenge game.

The spec’s signal input is `x: signal_hash` (`2024-vac-rln-v2-spec`, the signalling input list). o2’s `x = H(ephemeral_pk)`, computed before the body exists, is not in the spec. o2 marks it as needing cryptographic review. One nullifier then admits whichever body signed by that key arrives first. That is a different binding than RLN-on-the-message.

(c) Vote: **my alternative.** Use s1’s fixed-width admission record on the object. Use o2’s payment rule beside it: DUST prices ledger transactions, relays are unpaid, and any protocol payment is for storage a contract can check. Do not put an RLN proof on the object.

(d) Strongest objection to o2, the proposal that actually tries to pay operators: a slash that overwrites a `HistoricMerkleTree` leaf leaves every earlier root valid, so a double-signaller keeps producing accepts for the whole root window. The bond does not enforce the rate the envelope claims.

## D5 Performance requirements

(a) Positions

- **s1:** Plan at 10 cells/s, test at 100. One thousand whole-feed consumers. At 100 cells/s and 16 relays with 63 consumers each, outbound is about 226 Mbit/s before a 50% overhead allowance. p50 ≤ 2 s, p99 ≤ 15 s after admission.
- **s2:** Plan at 10 cells/s, stress at 100, mean wire size 1,055 bytes. A six-peer relay budget is about 1.6 MB/s at stress. Ten thousand subscribers imply about 131 MB/s of aggregate egress at the normal rate. Phones are outside the privacy budget.
- **o1:** Fifty envelopes/s, mean wire about 5.2 KiB including a 3 KiB proof. Relay ingress about 2.1 Mbit/s unique. CPU at 0.3 core from the 3.27 ms price. Mobile at 13–15 MB/day after shortening the tag index.
- **o2:** One hundred events/s across 16 shards, at most 10 per shard, wire about 6 KiB. Full-relay budget about 39 Mbit/s at degree 8. Hot-path p99 ≤ 3 s with precomputed proofs.

(b) Evidence

s1’s fan-out arithmetic holds: `(63 + 6) × 100 × 4096 = 28,262,400` bytes/s, which is 226.1 Mbit/s. The 48-hour store `100 × 4096 × 172,800` is 70.78 GB in decimal units. s2’s `0.99×1024 + 0.01×4096 = 1,054.72` holds, and twelve copies plus 25% overhead is the 1.58 MB/s they print. o2’s `100 × 6 KiB × 8` is about 39 Mbit/s. These are arithmetics on assumptions, which each author labels.

The v1.1 parameter table sets `FloodPublish` default true and `D_out` default 2 “for a D of 6” (`2020-gossipsub-v11-spec`, parameter table). It does not make `D = 6` mandatory. o2’s `D = 8`, `D_low = 6`, `D_high = 12` is cited to the Vyzovitis evaluation paper. I did not open that paper. It is not the v1.1 default table.

Revuelta sets the RLN epoch gap `g` to 20 s (`2024-revuelta-waku-latency`, the epoch-gap paragraph). That supports o2’s ±20 s epoch check. The same paper says messages of 25 KB or smaller were delivered in under 1 s in its experiment. That experiment is not o2’s stem plus precomputed proof. The 2.7 and 18.7 figures sit on Table 1; o2 reads them as verification milliseconds.

o1’s mobile tag-index arithmetic, `4 × (50/16) × 24 × 86,400 ≈ 26 MB/day`, is right, and the drop to 13 MB/day is a shorter index that is not in the envelope. The 0.3 core figure multiplies the fee weight by 50. Taheri’s measured verify is about 30 ms, which at 50 proofs per second is 1.5 cores before GossipSub. o1’s CPU gate is a price, not a measurement.

(c) Vote: **s1**, because it counts the subscriber copies the whole-feed claim requires. Phase 1 should gate the 10 cells/s row. The 100 cells/s, 1,000-consumer case is a capacity test, not a launch promise.

(d) Strongest objection: s1’s relay class is a 1 Gbit machine doing 339 Mbit/s at the stress point. That excludes the operator set Midnight has today, and the proposal has no second topology once that budget is missed other than “reduce admitted capacity.”

## D6 Storage requirements

(a) Positions

- **s1:** Relays keep every cell for 48 hours. At the stress rate that is about 71 GB of ciphertext plus about 2.2 GB of index. Three storage receipts define “stored.” Archives are a separate seven-day product.
- **s2:** Seven days of the whole stream. At 10 cells/s, about 6.4 GB of bodies, provision 12 GB. Stress provision is 120 GB. Clients keep bounded skipped keys.
- **o1:** Store nodes keep 7 days by default and 14 at most, proofs stripped after anchoring, about 63 GiB stripped at 50 envelopes/s. An anchor proves existence, not availability.
- **o2:** Store nodes keep the TTL class, about 28 GB at 100 events/s under a 90/10 mix of 24-hour and 7-day objects. A 20,160-slot anchor ring is overwritten in place. Availability is a bond challenge.

(b) Evidence

s2’s week at 10 cells/s, `10 × 1,054.72 × 86,400 × 7 ≈ 6.38 GB`, matches the text. o1’s `50 × 2.2 KiB × 604,800 s ≈ 63 GiB` matches if 2.2 KiB is the stripped size. o2’s `100 × 2,048 × 86,400 = 17.7 GB/day`, then `0.9 × 17.7 + 0.1 × 17.7 × 7 = 28.3 GB`, matches. All three are inferences from their own rates.

There is no state rent (`notes/midnight-network-stack.md` §7.5, as cited; I am not re-deriving it). Persistent `bytesWritten` per block is 50,000 and churn is 50,000,000 (`ledger-parameters-config.json:159-160`). A 20,160-slot ring left forever in state is the right thing to fear. Whether an in-place overwrite is churn rather than net growth is an inference, which o2 labels. I did not find a ledger rule that a `HistoricMerkleTree` overwrite of a past root deletes the history `checkRoot` needs. If the history remains, the ring is not a bounded 1.3 MB.

Bodies on the ledger hit the 1 KiB silent drop and the public `Misc` name. All four keep ordinary ciphertext off the ledger. That part is consistent with the VM.

(c) Vote: **s1.** Forty-eight hours, bodies off the ledger, and an explicit statement that a receipt is not a proof of continued storage.

(d) Strongest objection: 48 hours of a 4 KiB cell at the stress rate is already a 71 GB hot store, and a wallet that is offline for a weekend has missed the feed. The retention is expensive for relays and short for the consumers the charter names.

## D7 Infrastructure actors

(a) Positions

- **s1:** Sixteen relay instances across at least eight organizations, several admission issuers, two archives. Validators stay on the ledger. Open relay service is allowed. Issuer admission stays gated.
- **s2:** Dedicated relays, gateways, and issuers. At least five organizations, three issuers, three storage receipts. Anyone may relay. Issuer-free admission is a later milestone.
- **o1:** Permissionless relays and anchor aggregators from the start, foundation-seeded stores, client-chosen detection servers. Validators unchanged.
- **o2:** Unpaid permissionless relays. Bonded store nodes and anchorers. A foundation phase with a seven-day timelock, then measured gates, then governance. Saturation cap per bond key.

(b) Evidence

Genesis sets `num_permissioned_candidates` to 10 and `num_registered_candidates` to 0 (`system-parameters-config.json`, the `d_parameter` object). That is the committee’s launch shape, not a count of live operators. s1 says this. The node registers GRANDPA, BEEFY, and ledger-sync in `new_full`. `command.rs:327` instantiates `sc_network::NetworkWorker`. s1 and s2 cite 326. Validators do not serve ledger-sync snapshots by default (`service.rs`, the comment above `serve_ledger_sync`). `Cargo.lock` has `sc-network-gossip` at line 14548 and no `gossipsub` package in the search I ran. o2’s `service.rs:641` is `default_peers_set_num_full` passed into the ledger-sync handler. Shared peer slots with consensus are an inference from one `NetworkWorker`, not a fact at that line.

`ContractAction::Maintain` is at `structure.rs:3030` on the tag, not 2987. A maintenance update exists. o2’s claim that the maintainer cannot move bonds except through coded slash and withdraw rules is a property of a contract they have not written.

(c) Vote: **o2** for who is paid: relays unpaid, store and anchor roles bonded, foundation phase with a public gate. Admission credentials stay s1’s issuers until a fixed-width anonymous quota exists.

(d) Strongest objection: phase L has one foundation anchorer, and every contract that trusts the ring trusts that operator’s omissions. The saturation cap is per bond key, and o2 already reports that Nym operators split keys (`2026-cao-nymreputation`, Appendix D, as o2 cites). I did not re-open Appendix D.

## D8 Network tether

(a) Positions

- **s1:** A separate libp2p overlay carries ciphertext. Midnight does authorization, settlement, and application commitments. Fallback is replicated whole-feed servers. No node change.
- **s2:** The same split, with gateway fallback and optional anchors. No node change. Ledger-9 activation for log anchors is unknown.
- **o1:** Sidecar plus ledger membership, anchors, and a ledger fallback of multipart `Misc`. Lists nine upstream changes and says only ledger-9 activation is mandatory.
- **o2:** Sidecar plus a Registry contract. Fallback is `Misc` ciphertext, or contract-state writes on ledger 8. Asks governance to confirm contract-held NIGHT and a shielded credit token.

(b) Evidence

All four read the same node: application pubsub is not registered, and a new notification protocol is a node change (`service.rs`, the protocol registrations; `command.rs:327`). The indexer subscription follows finalized blocks (`chain-indexer/.../subxt_node.rs`, `subscribe_finalized_blocks`). `contractEvents` is `@beta`. `Misc.name` is a clear GraphQL field on `MiscContractEvent`. o1’s summary says no mandatory change to node, ledger, indexer, or wallet. The same proposal’s U0 says ledger-9 activation is required for anchors and contract consumption, and the support matrix still lists the older toolchain and runtime. Both sentences are in o1. They cannot both be the launch requirement.

Safe mode’s call filter is `InsideBoth<SafeMode, TxPause>` (`runtime/src/lib.rs`, `BaseCallFilter`). `check_call_filter.rs` says `send_mn_transaction` is deliberately not an inherent, so safe mode stops user transactions. o1’s `lib.rs:321` is the filter type. The explicit exclusion is in the filter file. The pause claim holds.

(c) Vote: **s1.** Sidecar for bytes, ledger for commitments and whatever fixed admission needs, no new peer protocol, fallback that keeps the whole-feed rule.

(d) Strongest objection: the feed-server fallback concentrates ingress on a few operators. s1 records that. It is still a single observation point for every publisher who uploads there, and the proposal has no second fallback if those servers are also the issuers.

## D9 Threats and open risks

(a) Positions

- **s1:** Names ingress attribution, omission, probing, and issuer equivocation as residuals. Rejects Dandelion++ as a global-observer defence and FMD as equivalent to whole-feed privacy.
- **s2:** Same residuals, plus Double Ratchet composition. Requires the cited forward-secrecy attacks to be reproduced before launch. No post-quantum post-compromise security.
- **o1:** GossipSub scoring, RLN, Dandelion++, padding, and a cover floor. Residuals are a global passive adversary, Seres-style detection, and a small launch anonymity set.
- **o2:** Bonds, slashing, challenges, and a stem. Residuals are a global observer, a single phase-L anchorer, and bond-key splitting.

(b) Evidence

s1’s Dandelion and FMD rejections match the papers checked under D2. GossipSub P₄ is the invalid-message penalty (`2020-gossipsub-v11-spec`, “P₄: Invalid Messages”), and extended validators distinguish Accept, Reject, and Ignore. o2’s use of P₄ for invalid proofs matches the spec. Scoring is a dissemination defence. s1 is right that it is not an anonymity theorem.

Cheval reports three forward-secrecy attacks on the Double Ratchet, including encrypted-header and PQXDH composition (`2026-cheval-dr-automated`, abstract and §3). s2’s further sentence, that the missing encrypted-header proof was only a resource limit, was not in the lines I opened. The three attacks are enough to refuse “the specification composes, therefore the bus composes.”

o1’s replay row says “none material.” A partitioned relay set can accept two bodies under rules that only meet when the partition heals. That residual is missing. o2 states the split-mesh double-signal case. That one is the better threat row.

(c) Vote: **s1.**

(d) Strongest objection: the second-source repair is specified as “repair all differences,” and the privacy game forbids the difference set from depending on recognition. Nothing in the protocol makes that a checkable function of the two inventories. A client bug that repairs only the cells it opened breaks D2 without failing admission.

## D10 Build and verification plan

(a) Positions

- **s1:** Write the games first. Prove or obtain a review of the wrapper. Simulate omission and equivocation. Run 100 cells/s and 1,000 consumers for 48 hours. Paired executions must show no interest-dependent requests. Fund the pilot before production. Mix and PIR stay separate.
- **s2:** Freeze encodings and vectors. Reproduce the three ratchet attacks. Benchmark the full topology, including 10,000 subscribers. Compile the Midnight circuits separately. Change course if recognition CPU or the composition audit fails.
- **o1:** Eight-week spikes for proof size, anchor bytes, a Quint model, a 1,000-node simulation, and an FMD graph simulation, then an overlay MVP. Numeric pivots if the proof exceeds 6 KiB or verify exceeds 10 ms.
- **o2:** Measure the RLN circuit, simulate the treasury, simulate GossipSub, and model the Registry in Quint before mainnet. Pivot if the proof exceeds 8 KiB or verify exceeds 20 ms.

(b) Evidence

The phase gates that depend on ledger-9 `emit` are blocked until the deployed runtime is identified. The node pin and the support matrix disagree, and every proposal that anchors through `Misc` says this. o1’s pivot “if the proof is over 6 KiB, use Groth16 at about 192 bytes” is an inference from three group elements. I did not verify a 192-byte encoding. UnifOMR’s “about 25 seconds and 4 MB for `2^19` messages of 612 bytes” is in the abstract and the implementation paragraph (`2026-fisch-unifomr`). Theorem 5.1 is the reduction from strongly unlinkable OMR to PIR. Using those figures as a reason to defer OMR is fair. Using them as this bus’s budget is not, and s1 says so.

Quint is appropriate for the accept predicate and for o2’s bond invariants. It will not discharge s1’s cryptographic games. s1 is right to put those games in a review rather than in a model checker.

(c) Vote: **s1**, with one added spike from o1 and o2: if anyone still proposes an on-object ZK admission proof, measure its bytes and its verify time before the envelope is frozen. I do not adopt that proof.

(d) Strongest objection: the 48-hour run at 100 cells/s and 1,000 consumers is a data-center test. A failure there does not tell the team whether a wallet on the 10 cells/s feed can keep the fixed-fetch invariant. The first gate should be that wallet, on the planning load, with the paired-execution test.

## Where the group will disagree

The three decisions most likely to stay open are **D1**, **D3**, and **D4**.

D1 and D3 are the same split seen twice. s1 and s2 disseminate one opaque feed. o1 and o2 give relays a tag, a clue, or a shard derived from the topic so that a phone can avoid the feed. That choice decides whether subscriber-interest privacy is a fetch invariant or a probabilistic filter. D5 and D6 move with it, because the byte budgets are the price of the choice. D4 is the other split: a fixed admission signature or token, versus an RLN proof bound to a NIGHT bond. s2 is with s1 on the object and with nobody on Privacy Pass. o1 and o2 share RLN and disagree on slashing.

The fact that settles the most of this is the **byte length, on Midnight’s ledger-9 PLONK verifier, of one membership-and-rate proof, together with whether that proof verifies outside a transaction against the embedded degree-14 KZG parameters**. If the proof is wider than a fixed field the envelope can spare, or if verification only exists inside `send_mn_transaction`, then o1’s envelope, o1’s 0.3-core budget, and o2’s precomputed on-object proof are unspecified. The group is then left with a fixed admission record and a whole-feed object, which is s1’s wire, and D3’s phone path has to be argued on its own privacy evidence rather than as a consequence of RLN. The `HistoricMerkleTree` half of o2’s slash is already answered by the ADT documentation: past roots stay valid after a leaf is overwritten.
