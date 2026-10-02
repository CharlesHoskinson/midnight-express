# Round 2 cross-review: o1, Midnight protocol integrator

Reviewed: g1-protocol-architect, g2-network-engineer, s1-privacy-theorist and s2-cryptographer, with my own Round 1 proposal (o1) as reference.

**How I checked.** I opened the node, indexer, Compact, wallet, docs and MIP files in the working trees under `/home/charl/midnight/`. A helper read the 18 paper claims the proposals depend on most, in `graph/text/`. I could not reopen the `ledger-9.1.0.0-rc.5` tag in this session because `git show` was not permitted. Every `L9:` line number below therefore rests on the read-out (`notes/midnight-network-stack.md`) and on my Round 1 reading. I did not re-verify those lines.

**Integrator findings that cut across all four proposals:**

1. **The node discards contract logs.** `TransactionAppliedStateRoot` carries a state root, the tx hash, addresses and UTXO deltas, and no logs (`midnight-node/ledger/src/ledger_9/mod.rs:460-470`). Any relay that checks admission against `Misc` events must read them through the indexer's `contractEvents`, which is still `@beta` (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:1971`), or re-execute blocks itself the way the chain-indexer does (`midnight-indexer/docs/architecture.md:15-19`). A plain full node is not enough.
2. **`HistoricMerkleTree.checkRoot` accepts any past root** (`minokawa-compact/doc/ledger-adt.mdx:603-613`). The docs warn the tree "is not suitable if items are frequently removed or replaced" (`midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:170-174`). Membership designs that rely on `checkRoot` cannot enforce expiry or revocation on their own. That covers g1's buy call, s2's later membership plan and my own RLN.
3. **Compact can check both signature families in-circuit.** It ships `jubjubSchnorrVerify` (`exports.md:921`) and plain `ed25519Verify`, which hashes the message with SHA-512 in-circuit (`exports.md:993-998`). Ed25519 publisher signatures (g1, s2) are therefore checkable by a contract. The circuit cost is **unknown**.
4. **Safe mode deliberately filters `send_mn_transaction`** (`midnight-node/runtime/src/check_call_filter.rs:40-45`). Any admission scheme that needs a chain transaction every epoch stops when governance pauses.
5. **Ledger-9 activation is unknown for every proposal.** The mainnet support matrix lists toolchain 0.31.1 (`midnight-docs/docs/relnotes/support-matrix.json:38`).

---

## D1 Event format

**(a) Positions**
- **g1:** a fixed 192-byte little-endian header, four classes (256 B, 1 KiB, 4 KiB, 16 KiB body) with TTL from 1 h down to 5 min, static X25519 plus ChaCha20-Poly1305, and a one-time Ed25519 `pub_pk` plus a ticket on the header. Versions change only by protocol id.
- **g2:** a StrictNoSign envelope. The 32-byte shard, `msg_id`, `epoch`, `seq`, nullifier, `member_pk` and `member_sig` are all visible. Classes are 4 KiB and 64 KiB, plus a 256 KiB class that is announced only. TTL is up to 1 day (7 days for L). Open shards may carry content topics in clear.
- **s1:** one 4,096 B cell (128 header + 128 issuer admission + 3,840 sealed), a 48 h life, up to 16 cells per event, and the whole MLS packet sealed.
- **s2:** 1,024 B or 4,096 B cells, a 56 B encrypted Double-Ratchet header, a 354 B Privacy Pass token, and a 7-day life.

**(b) Evidence**
- `Misc` is 32 + 256 bytes (`minokawa-compact/compiler/midnight-events.ss:71-74`). Confirmed.
- Yamux `DEFAULT_CREDIT` is 256 KiB with a 16 KiB split (`rust-yamux/yamux/src/lib.rs:45,68`; first-frame check at `connection.rs:626`). Confirmed. It binds only a node-linked Yamux, which g2 notes; a sidecar has its own.
- Waku's content topic is cleartext and its hash is deterministic (`2020-vac-waku2-message-spec` L172-183). Supported.
- The Privacy Pass token is 2+32+32+32+256 = 354 B (`2024-rfc9578-privacypass-issuance` L734-740, Nk = 256 at L882). Supported as a sum of field sizes. The RFC never prints 354.
- MLS `PrivateMessage` exposes `group_id`, `epoch`, content type and authenticated data (`2023-barnes-rfc9420` L2045-2055). This supports s1 and s2 sealing the whole MLS packet.
- s2's appeal to Double-Ratchet §7.2 is only partly right. The SIV advice there is for message `ENCRYPT`, not for headers. The header nonce rule is in §4.2 (`2016-signal-double-ratchet-spec` L1356-1358, L1895-1897).
- g2's `nullifier = SHA-256(domain‖member_pk‖epoch‖seq)` is a public counter, not a privacy nullifier. Anyone can compute it.

**(c) Vote:** my own o1 envelope, rebuilt on **g1's encoding discipline**: one legal layout, reserved bytes must be zero, length implied by class, Ignore versus Reject, version only by protocol id. I also adopt g1's 256 B class and s1's rule that the whole session packet is sealed. My TTL stays: 7 days by default, 14 at most (`ledger-parameters-config.json:176` `global_ttl`). Of the four proposals reviewed, g1 is best.

**(d) Strongest objection to the leading position (fixed classes with sealed topics, which all five share):** the admission field sets the size floor and nobody has measured it. My envelope carries a Compact proof of planned size 3 KiB. s2's token takes 34.6% of a 1 KiB cell. g1 needs only 96 B, but only by pushing every ticket on chain. Until the admission proof size P is measured, no class table is final.

## D2 Definition of "private"

**(a) Positions**
- **g1:** content confidentiality; topic hidden from relays; a one-time ticket key per object. No forward secrecy, no global-observer claim. Known `enc_pk` values can be tested.
- **g2:** content confidentiality only. Shard interest, timing and relationships are explicitly not protected. Uses Pfitzmann's vocabulary and the Guerraoui bound.
- **s1:** game-based definitions over five adversary classes. Content confidentiality, plus subscriber-interest privacy conditional on identical fetching behaviour. Publisher unlinkability is not provided.
- **s2:** content confidentiality plus recipient and topic concealment, and ratchet forward secrecy. Notes the system is not post-quantum because the proofs are PLONK/KZG.

**(b) Evidence**
- Trilemma: strong anonymity is impossible if 2ℓβ < 1 − ε(η) (`2017-das-trilemma` §V-B Thm 2, L1093-1098). Supported for all four.
- Guerraoui Theorem 5: ε ≥ ln(f−1), and no finite ε if κ(G) ≤ f, against a worst-case adversary (L589-594). Supported.
- Seres's graph recovery holds "when the server knows the senders' identity" (L74). s1 states this condition and g1 omits it.
- Dandelion++: p² is a lower bound on precision. The ISP/AS adversary is out of scope (L273-275). s1's use is correct. g1 calls p² the 4-regular result, which is a little loose: that result is the bound D ≤ 8D_FS + 6p² + O(p³) (L631-633).
- g2 writes "DUST fees are burned" as fact. The read-out marks it **inference** (§2.3).

**(c) Vote: s1's framework.** Name each property as a game with an explicit adversary class and a leakage function. Then add one property s1 drops: **credential-level publisher unlinkability against relays.** Two envelopes must not be linkable to one admission identity. RLN gives this, and so do g1's one-time tickets and s2's blind tokens. g2's visible `member_pk` breaks it for an hour at a time. s1's issuer model gives it up to the issuer.

**(d) Strongest objection to s1:** "subscriber-interest privacy conditional on identical fetching" holds only for whole-feed clients. On s1's own arithmetic that is 3.5 GB/day at 10 cells/s. Most Midnight end users will sit in browser-extension or mobile wallets (**assumption**), and for them the definition guarantees nothing. That leaves a privacy definition with no adversary model for the users the product is for.

## D3 Publish and subscribe model

**(a) Positions**
- **g1:** a single flooded shard. Every object is trial-opened by AEAD, with no tags. A contract consumes an event when someone later calls `note(commitment)`. Wallets go through a local agent, with no connector change.
- **g2:** a mesh per shard, at most 8 shards. Open shards carry clear content topics. Contracts consume through a later transaction. Mobile wallets stay on the indexer and are not on the bus.
- **s1:** capability topics and one common feed, fetched every second. A second operator's inventory is used to repair omissions. Contracts consume through an explicit transaction with commitment and nullifier.
- **s2:** one transport topic and 56 B encrypted-header trials. At most 32 recipient devices per publication, as independent ciphertexts. A contract checks the Ed25519 publisher signature as a witness, plus a nullifier scoped to the destination.

**(b) Evidence**
- `contractEvents` requires `contractAddress`, and `fieldPrefixes` works on standard events only (`schema-v4.graphql:548-562`). Confirmed.
- The shielded wallet streams global Zswap events and applies them with local secret keys (`midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:238-266,295`). This supports the precedent s1 and s2 cite.
- `ed25519Verify` exists in Compact (`exports.md:993`). This supports s2's contract path.
- Encrypted-header trial order (skipped keys, then HKr, then NHKr) is in Double-Ratchet §4.6 (L1443-1456). Supported.
- OMR costs about 0.065 s per message per recipient (`2021-liu-omr` L315). That is p.6, not p.2 as my own Round 1 said: **I correct my citation.** g1's catalog-note figure is consistent with it.
- The DApp connector has no event method (`midnight-dapp-connector-api/src/api.ts`, grep). Confirmed.

**(c) Vote: s1's reception model plus s2's contract path.**
- **Reception:** whole-feed download with local recognition is the default.
- **Contract path:** the witness carries the event and the publisher signature, and a nullifier scoped to the destination contract is checked. This works with no cross-contract call, so it is simpler than my anchor-plus-`checkRoot` pattern.
- **Anchors become optional.** My anchor proof should be kept only for applications that need "published by time T" or batch order.
- **Mobile profile:** my bucket and tag-index profile stays, but only as a separately labelled reduced-privacy profile, as s1 requires for FMD.

**(d) Strongest objection to the leading position (one feed with local recognition):** s2's fan-out (32 independent ciphertexts per publication) and g1's/s1's whole-feed scan both price a broadcast to N subscribers at N ciphertexts, or a full-feed download for each subscriber. The 10,000-subscriber price feed or contract announcement that motivates an "event bus" is unaffordable in s2. It has no mobile reader in g1, g2 or s1. Symmetric topic keys (g1) or MLS exporters (o1) are needed for one-to-many, and the leading proposals treat them as later work.

## D4 Sustainable model

**(a) Positions**
- **g1:** single-use tickets bought with DUST through an admit contract. Each buy proves membership and emits one `Misc` per ticket. Budget 30 per member per 600 s. Relays are unpaid.
- **g2:** an hourly DUST membership with a visible Ed25519 `member_pk`, 60 class-S credits, and a per-peer token bucket. No slashing; relays unpaid.
- **s1:** prepaid admission slots signed by an issuer, settled in fiat or a transferable asset. RLN later.
- **s2:** Privacy Pass blind-RSA stamps bound to the object, with off-chain billing. A Compact membership-and-nullifier scheme later.

**(b) Evidence**
- **NIGHT and DUST arithmetic.** All four agree on 5 DUST per NIGHT and about 604,800 s to cap (`ledger-parameters-config.json:164-166`; `dust-architecture.mdx:96-111`, "≈ 604,800 seconds"). Confirmed. g2's "about twenty messages an hour per NIGHT" follows: 0.714 DUST/day ÷ 0.08 ≈ 9 memberships × 60 credits.
- **Block reward hook.** The hook is at `midnight-node/runtime/src/lib.rs:681-698`. Confirmed (s1, s2).
- **RLN verification time.** About 30 ms is in §IV of `2022-taheri-waku-rln-relay` (L430), but it is drawn from the RLN library, not measured on the prototype. Partly supported (s1).
- **My own citation error.** RLN-v2 does not say `message_id < limit`. It says the range is 1 to `limit`, inclusive (`2024-vac-rln-v2-spec` L188-190). **I correct this.**
- **g1's Schaub reading.** "At best halves the harm" is wrong. Schaub says the gain grows with network delay (L553-556).
- **g1's internal inconsistency.** The fee of 0.0027 DUST per object assumes 30 tickets per transaction. g1's own D2 says tickets in one transaction are linkable to each other. One ticket per transaction costs 0.08 DUST, and at g1's 10% block budget it mints about 2 tickets/s, against a 50 objects/s target.
- **g1's governance claim.** g1 says the allow-list in the admit contract is changed by "Root via Council". A Compact contract's state changes only through its circuits or its maintenance authority (the read-out says `Maintain` carries committee signatures, §3). Root governance would need a design of its own (**inference**).

**(c) Vote: o1 (an RLN statement written as a Compact circuit, membership bought with DUST), gated on Phase 0.** I add two amendments. First, epoch-scoped membership trees or a `Map<root, epoch>`, so expiry is enforceable despite finding 2. Second, s2's blind stamps as the named fallback if P exceeds 1 KiB.

Among the four reviewed, s2 is the best. It is the only one that is unlinkable, keeps per-object data off the chain, and leaves relays a constant-time check. The cost is an issuer who learns timing.

**(d) Strongest objection to the leading position (DUST membership with nullifier quotas: g1, g2, o1):** liveness depends on Midnight. Safe mode stops `send_mn_transaction` (`check_call_filter.rs:40-45`), and with it new memberships. g1 needs a transaction every 10 minutes and g2 every hour, so a governance pause silences publishers within an epoch. s1 and s2 issuers keep running. My 14-day membership degrades more slowly, but it degrades.

## D5 Performance requirements

**(a) Positions**
- **g1:** 50 objects/s per shard, mean 848.6 B on the wire, about 2.21 Mbit/s mesh traffic per relay, D = 6, p99 ≤ 10 s.
- **g2:** D = 8/6/12, heartbeat 1 s, amplification m = 7, a relay cap of about 104 class-S messages/s, p99 ≤ 2 s at N = 1,000.
- **s1:** 10 cells/s normal and 100 stress, 1,000 whole-feed consumers, 1 Gbit/s relays, p99 ≤ 15 s.
- **s2:** 10 cells/s normal and 100 stress, mean 1,054.72 B, 50 gateways serving 10,000 subscribers, p99 ≤ 15 s.

**(b) Evidence: the arithmetic checks out.**
- g1: 5 × 848.6 + 1.5 × 848.6 = 5,516 B = 44.1 kbit per object. ✓
- g2: 7 × 10 × 4,096 = 286,720 B/s. The cap 3·10⁶ / 28,672 = 104.6. ✓
- s1: 69 × 409,600 B/s = 226.1 Mbit/s. ✓
- s2: 0.75 × 1,048,576 / (8,192 × 6) = 16 tx/s. ✓ This uses the runtime `BlockLength` (`runtime/src/lib.rs:312`), which is tighter than the ledger's `blockUsage` of 1,000,000.
- g2's GossipSub profile (D = 8/6/12, heartbeat 1 s, p99 205 ms, recovery in 90 heartbeats) matches `2020-vyzovitis-gossipsub` (L577-579, L532, L1210, L1236).
- g2 dismisses Farooq's 5,520 ms figure for 1 MB. The figure is consistent with *sequential sends to all 8 peers* (8 × 160 ms ≈ 1,280 ms per hop), so g2's single-send latency model understates large classes. That is negligible at 4 KiB and about +0.3 s at 64 KiB.
- g1's 97 µs signature check is the ledger's *native* `signature_verify_constant` (`ledger-parameters-config.json:124`), not an in-circuit verify as g1 calls it.
- My own 5.2 KiB mean envelope is 5–6× heavier than the others' because of the proof.

**(c) Vote: g2's method.** Name the amplification m explicitly, take mesh parameters from the published evaluation, and give no credit for IDONTWANT until the crate implements it. Use s1's and s2's 10/100 cells-per-second operating points as the normal and stress loads.

**(d) Strongest objection to g2:** a 2 s p99 counts only the mesh. Every design here admits through Midnight: a ticket, a membership or a proof. The cold path adds about 18 s to finality (`mps-0028`, via the read-out §1.7) plus proving time, from seconds to over a minute (`zk-loan/cli.mdx:302`). A latency requirement that leaves out admission sets the wrong expectation for first-time publishers.

## D6 Storage requirements

**(a) Positions**
- **g1:** a body is kept until expiry (at most 1 h), about 100 MB per relay, a 2 GiB cap. Archives are optional.
- **g2:** a 10-minute relay cache. Stores keep 24 h, or 7 days if the object is anchored, with a 100 GiB cap.
- **s1:** relays keep 48 h, archives 7 days. An object counts as stored after three receipts.
- **s2:** storage relays keep the complete stream for 7 days, 6.4 GB per week at normal load. Three receipts.

**(b) Evidence**
- Persistent `bytesWritten` is 50,000 per block and churn is 50,000,000 (`ledger-parameters-config.json:158-160`). Confirmed.
- MIP-0002 assumes events consume the 50 KB write budget (`mip-0002...md:520-521`). The read-out says the VM counts logs as written = deleted, i.e. churn. These disagree.
- This matters most for g1. At 50 tickets/s, the `Misc` data is about 86 KB per block, which **would exceed** `bytesWritten` under MIP-0002's reading. The question is **unknown** until it is measured on a ledger-9 devnet.
- s2's arithmetic: 10 × 1,054.72 × 604,800 = 6.379 GB. ✓

**(c) Vote: s2 (7-day complete-stream retention).** It matches my 7-day default and Midnight wallet behaviour: wallets resync after long offline periods. g1's 1 h maximum TTL means a phone offline overnight loses every event.

**(d) Strongest objection to s2:** three storage receipts are contractual statements, not proof of retrievability. No proposal, mine included, gives a cheap audit, and the chain cannot enforce availability.

## D7 Infrastructure actors

**(a) Positions**
- **g1:** 8 to 16 relays on a permissioned allow-list. Each runs a full node. Validators are excluded.
- **g2:** open relays kept in the mesh by score, four bootstrappers separate from the chain bootnodes, validators excluded.
- **s1:** dedicated relays, issuers who know publishers, 16 relays across 8 organisations.
- **s2:** relays, gateways and at least 3 issuers across at least 5 organisations.

**(b) Evidence**
- Ledger-sync is not served on authorities by default (`service.rs:609-618`). Confirmed for all four.
- Genesis has 10 permissioned and 0 registered committee candidates (`system-parameters-config.json:6-9`). Confirmed.
- Heimbach locates more than 15% of Ethereum validators (L49-50). Supported.
- GossipSub's advice for bootstrappers is broader than "degree 0": `D = D_lo = D_hi = D_out = 0` plus a high application score (`2020-gossipsub-v11-spec` L658-661). g2 is substantively right.
- g1's statement that the relay's full node is how it sees admit events is **contradicted** by finding 1.

**(c) Vote: g2.** Exclude validators, keep the event bootstrappers separate from chain bootnodes, and optionally commit the bootstrap list's hash on chain.

**(d) Strongest objection to g2:** relays are open from Phase 2 with no stake and no red-team gate. g1's rule is better: keep admission gated until a Sybil red-team fails to capture the mesh under the chosen scoring parameters. The Least Authority audit asked for more simulation before parameters are frozen (`2020-leastauthority-gossipsub-audit`, as g2 itself notes).

## D8 Network tether (my lead decision)

**(a) Positions.** All four choose a hybrid sidecar libp2p overlay, with no node change.
- **g1:** fallback is a Substrate notification protocol on non-validators.
- **g2:** fallback is `Misc` events read through the indexer.
- **s1:** fallback is replicated feed servers.
- **s2:** fallback is replicated gateways. Anchors are optional.

**(b) Evidence**
- `Cargo.lock` has `sc-network-gossip` (line 14548) and no `gossipsub` or `floodsub`. Confirmed.
- The node runs `NetworkWorker` (`command.rs:326`) and registers GRANDPA, BEEFY, BEEFY justifications and ledger-sync (`service.rs:574-644`). Confirmed.
- The ledger-sync handler takes its size from `default_peers_set_num_full` (`service.rs:641`). Confirmed.
- CVE-2022-47547 is real and was unfixed when the ACL2s paper was written (`2023-kumar-gossipsub-acl2s` L25, L73). This supports g2's gate on the crate version.
- Every proposal's claim of "indexer: none" is incomplete. Admission (g1, g2, o1) and anchors (all of us) depend on the `@beta` `contractEvents` subscription, or on each operator re-executing blocks.

**(c) Vote: the hybrid sidecar** (o1, g2 and all four reviewed proposals). I amend my fallback order from Round 1:
1. **First fallback:** s1's and s2's replicated feed servers with identical framing. They keep the same privacy contract.
2. **Last resort only:** ledger `Misc` for rendezvous and censorship escape, which is a different, public product.

The upstream changes are now:
- **U0, ledger-9 activation.** Owner: node release team and governance.
- **U7, `contractEvents` out of beta, plus a capacity benchmark.** Owner: indexer team. Now **required**, not merely desirable.
- **New: package a standalone re-executing indexer for relay operators.** Owner: indexer team. Alternatively MPS-0007, node-side event visibility, owned by the node team.
- **U2, aligning the log size limits.** Owners: Compact and ledger teams.

**(d) Strongest objection to the leading position:** "no Midnight change" is true for the node binary and false for operations. Every relay's admission view depends on an indexer interface that is beta, has no published capacity figure (read-out §4.7), and runs on a ledger generation whose mainnet activation is **unknown**. An indexer that withholds events censors publishers, as g1 notes. If ledger 9 slips, g1 and g2 have no admission at all. I and s2 lose anchors and on-chain membership. s1 alone keeps running.

## D9 Threats and open risks

**(a) Positions**
- **g1:** tickets, a permissioned mesh, the stem as an unclaimed heuristic, strict parser rejection rules.
- **g2:** v1.1 scoring, a separate peer table, `D_out` = 4, a CVE gate, no receipts.
- **s1:** omission repair from a second source, no probing that depends on recognition, issuer equivocation evidence.
- **s2:** composition risk ranked first (the three Double-Ratchet attacks in `2026-cheval-dr-automated`), recipient probing, rollback.

**(b) Evidence**
- `D_out` must be "less than `D_lo` and at most `D/2`" (`2020-gossipsub-v11-spec` L553), so g2's legal range of 1 to 4 for D = 8 is correct.
- The Dandelion++ scope (L273-275) supports s1's refusal to make global claims.
- g1's attribution of the Bitmessage RCE to CVE-2018-1000070 and `eval` dispatch is consistent with the guide's account.

**(c) Vote: g2's table, merged with s1's omission and probing rows.**

**(d) Strongest objection:** none of the four lists *the chain view as an attack surface on admission*. An eclipsed or lagging indexer makes honest relays Reject valid envelopes. Under GossipSub P4 that graylists honest forwarders, turning a chain-read failure into self-inflicted network partition. Admission failures caused by a stale chain view must be Ignore, not Reject. g1 half-addresses this with its "stop validating if the clock drifts" rule.

## D10 Build and verification plan

**(a) Positions**
- **g1:** parser and admit circuit first on a ledger-9 devnet, a 16-relay mesh with a numeric spy gate, the allow-list removed only after a red-team fails.
- **g2:** simulation at 50, 200 and 1,000 relays, explicit stop conditions, the CVE gate, a model of admission only.
- **s1:** the privacy games instantiated before code, paired-execution tests, a funded pilot.
- **s2:** a frozen crypto profile with test vectors and an audit, reproduction of the ratchet attacks, a separate gate on Midnight integration.

**(b) Evidence.** The gates are design choices and are labelled as such. The cited methods (Vyzovitis, Farooq, ACL2s) support them.

**(c) Vote: g1's ordering** (measure the admission transaction or proof on a ledger-9 devnet before writing a relay), **with g2's stop conditions and s2's crypto gates appended.**

**(d) Strongest objection:** every plan starts on a ledger-9 devnet but none has a branch for "mainnet stays on ledger 8 for a year". The plan needs an explicit ledger-8 profile: s1-style issuer admission, no anchors, s2's contract path, assuming `ed25519Verify` exists in 0.31.1, which is **unknown**. Without it the schedule depends on U0.

---

## Where the group will disagree most

1. **D4, the admission instrument.** The options are on-chain tickets (g1), a visible member key (g2), issuer slots (s1), blind stamps (s2) and RLN in Compact (o1). Each trades a different party's knowledge (chain, relays, issuers) against chain dependence and per-object bytes.
2. **D3, reception for constrained wallets and one-to-many fan-out.** Positions run from whole-feed only (g1, s1) to wallets off the bus entirely (g2), per-recipient ciphertexts (s2), and tag index with decoys (o1).
3. **D1/D2, session security in v1.** g1 and g2 ship static keys with no forward secrecy. s1 and s2 require ratchets or MLS from launch, which forces larger cells and composition audits.

## The one fact that would settle the most

**The measured size and verification time of a membership-plus-epoch-nullifier proof written in Compact and proven by the standard proof server, and whether the ledger API can verify it outside a transaction (my U1).**
- If P ≤ about 1 KiB and verification takes ≤ 10 ms, then:
  - **D4:** RLN in Compact dominates. There are no per-ticket chain events (g1), no linkable member key (g2), and no trusted issuer (s1, s2).
  - **D1:** the header size is fixed.
  - **D5:** the bandwidth arithmetic converges near g1's 0.85–1 KiB mean.
  - **D8:** the dependence on the indexer narrows to membership roots.
- If P is about 3 KiB or more, s2's blind stamps become the launch instrument and RLN moves to Phase 3.

The measurement is a Phase-0 spike of a few weeks on a ledger-9 devnet.
