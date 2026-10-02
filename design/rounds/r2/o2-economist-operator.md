# Round 2 cross-review: economist and operator (o2)

Reviewed: g2-network-engineer, g3-performance-storage, s2-cryptographer, s3-red-team. I also re-read my own Round 1 proposal, and I correct two of my own errors below. I opened the code under `/home/charl/midnight/` and the paper texts under `graph/text/` for each citation I judge. "L8" means the ledger-8 working tree. "L9" means the ledger-9 tag, read through the read-out.

**Summary.** All five proposals agree on D8 (hybrid sidecar) and roughly on D2, D6 and D10. The real split is economic:
- **Who pays for admission:**
  - DUST burned for a membership (g2, g3)
  - prepaid off-chain service contracts (s2, s3)
  - a NIGHT bond held by a contract, which can be slashed (mine)
- **Whether any operator role is paid by the protocol at all.**

One claim behind the "no slashing" camp is wrong in the code. g2 says "Midnight cannot slash… until a seizable asset exists." The ledger's own tests deposit NIGHT into a contract and pay it back out. Slashing is buildable. The open question is whether it is worth building.

---

## D1 Event format

**(a) Positions**
- **g2:** StrictNoSign GossipSub envelope with a 32 B shard id; the relay sees `member_pk`, an Ed25519 signature and a nullifier; classes 4 KiB / 64 KiB / 256 KiB (the last as announce-only); TTL 24 h, or 7 d if anchored.
- **g3:** padded classes of 1 / 4 / 32 KiB; a fixed-length admission proof with a chunk nullifier; a quota day; expiry of 48 h or less; sequence and schema sealed.
- **s2:** fixed cells of 1,024 or 4,096 B; a 354 B Privacy Pass token; a 56 B encrypted Double Ratchet header; PQXDH with ML-KEM-768; 7-day expiry.
- **s3:** a single 4,096 B cell; a 1,152 B admission area (root, nullifier, RLN share, proof); header-encrypted Double Ratchet; 48 h retention.

**(b) Evidence**
- g2's Yamux citation is accurate: `rust-yamux/yamux/src/lib.rs:45` sets `DEFAULT_CREDIT = 256 KiB`, and `connection.rs:626` rejects a first body larger than that. But g2 itself says the sidecar does not link the node's Yamux, so this only supports the 256 KiB cap by analogy.
- g2's `MAX_LOG_EMITTED = 1 KiB` is not in the L8 tree. Only `MAX_LOG_SIZE = 1<<19` is (`midnight-ledger/onchain-vm/src/vm.rs:38`). The 1 KiB figure rests on the read-out's L9 extract (read-out line 215). I accept it as L9-sourced.
- s2's token size checks out against RFC 9578: `nonce[32]`, `challenge_digest[32]`, `token_key_id[32]`, `authenticator[Nk]` (`graph/text/2024-rfc9578-privacypass-issuance.txt:522-525`). With a 2-byte type and Nk = 256, that is 354 B.
- s2's Ed25519 support is real: `exports.md:100` defines `Ed25519Signature`.
- s3's proof-independent identifier is labelled inference and is sound.

**(c) Vote: g3.** Three padded classes, a byte-denominated debit, and sequence and schema sealed. It is the only format that ties volume privacy (padding) to billing (bytes). Two amendments:
- Leave the admission slot length open until it is measured.
- Adopt s3's rule that the identifier is computed without the proof.

g2's visible `member_pk` makes every event in one membership-hour linkable by relays (up to 60 class-S events). That is a privacy regression none of the others accept.

**(d) Strongest objection.** Every format freezes the length of an admission field nobody has measured: 0 B extra (g2's Ed25519), 354 B (s2's RSA), 1,152 B (s3) and my 4 KiB budget. Until a Midnight-native RLN proof is benchmarked, the class sizes are guesses. At 1 KiB (g3's S class), any proof over a few hundred bytes leaves little room for payload.

---

## D2 Definition of "private"

**(a) Positions**
- **g2:** content confidentiality only. Explicitly refuses publisher, subscriber and relationship unlinkability against a global observer, citing the trilemma and Guerraoui's Theorem 5. No forward secrecy, no receipts.
- **g3:** content confidentiality, interest privacy at shard level, and weak one-hop stem unlinkability. Cover traffic is refused until priced.
- **s2:** content confidentiality plus cryptographic hiding of recipient and topic from infrastructure. Forward secrecy is bounded. The system is explicitly not post-quantum, because the proofs are PLONK/KZG.
- **s3:** separates confidentiality, interest privacy, topic privacy and publisher unlinkability, each with its own conditions. Global-observer privacy is a separate experimental mix profile.

**(b) Evidence**
- g2's and s2's trilemma citations support the refusal they make. s3 correctly warns against using the trilemma as a numeric proof for an asynchronous overlay.
- s2's statement that the proof system is not post-quantum matches the read-out: PLONK/KZG on BLS12-381 (`midnight-zk/README.md:9-17`, read-out line 359).
- s3's indexer leakage claim is accurate: `contractEvents` needs an address. I did not reopen `schema-v4.graphql:548`; the read-out confirms it.

**(c) Vote: s3's structure (separate, conditional claims), with g2's explicit refusals.** One amendment: make "registration is public" a named leak. Every model that admits publishers on chain leaks who enrolled and when:
- my NIGHT bond (an unshielded deposit)
- g2's and g3's DUST memberships (contract call and timing are visible)
- s2's issuer purchases

**(d) Strongest objection.** s2 and s3 buy subscriber-interest privacy with whole-feed download. s3's own figure is 7.078 GB/day per client at 20 cells/s. The claim holds only for clients who can pay that bill, and nobody in s2 or s3 says who pays it. The property should be stated as "interest privacy at stream level, for clients who pull the whole stream", not as a general guarantee.

---

## D3 Publish and subscribe model

**(a) Positions**
- **g2:** one mesh per shard, at most 8 shards per relay. Open shards carry clear content topics; private shards do not. A one-hop outbound stem, and flood-publish off on private shards. Mobile wallets use the indexer only.
- **g3:** 8 pinned shards: `H(contract) mod 8` for contract events, `H(secret) mod 8` for private events. Light clients use unicast filter nodes. A one-hop stem.
- **s2:** one network-wide transport topic. Invitations only (no public first contact). Local trial of encrypted headers, capped at 256 keys. At most 32 recipient devices per publication.
- **s3:** one common feed, whole-feed retrieval, out-of-band invitations. Contracts consume through a signed statement plus a replay nullifier.

**(b) Evidence**
- g3's "eight shards, like Waku" is supported: "sharding messaging traffic from all applications into eight pub/sub topics" (`2024-cornelius-waku-network-dapps.txt:54`).
- s2's FMD figures are exact: 68 B flags, 1.927 ms to generate, 0.548 ms to test (`2021-beck-fmd.txt:123-124`). The extrapolation of 10 cells/s × 10,000 clients × 0.548 ms = 54.8 CPU-s/s is correct arithmetic.
- s2's citation that header keys are tried during recognition is supported by the HKr/NHKr state in `2016-signal-double-ratchet-spec.txt:1368-1414`.
- My own S-FMD floor citation holds: in S-FMD "the false positive rate is set by the sender" (`2022-penumbra-fmd.txt:603`). So does "FMD is not viable with selfish users" (`2024-frank-anonymous-messaging-altruism.txt:24`).

**(c) Vote: g3's pinned shards, plus s3's rule for contract consumption** (signature, target, expiry and replay nullifier checked atomically). Sharding is what lets one node class's cost stay bounded at all. A single global stream (s2, s3) makes every subscriber's bandwidth scale with total bus volume. Someone then has to pay for that bandwidth, and the volume cannot grow without raising every subscriber's cost.

**(d) Strongest objection.** `H(contract) mod 8` cuts each publisher's anonymity set to one-eighth and publishes which shard each contract uses. Anyone who knows a low-volume contract can watch its shard's volume. g2's further point stands: GossipSub `SubOpts` tell direct peers which shard a node joined. Also, g2's "mobile wallets stay on the indexer" means mobile wallets get no private events in v1 at all, because the indexer carries only public on-chain events.

---

## D4 Sustainable model (the decision I lead)

**(a) Positions**
- **g2:** a DUST-paid hourly membership with 60 class-S credits per hour; Ed25519 plus a nullifier per message; no slashing; relays unpaid in v1.
- **g3:** a DUST-paid daily membership with a byte budget; at most 10% of block usage reserved for the bus, enforced only by clients; burned fees; relays and stores unpaid.
- **s2:** publicly verifiable Privacy Pass blind-RSA stamps from issuers; publishers buy prepaid capacity through "ordinary billing"; a service pool pays contracted relays and gateways; prices unknown.
- **s3:** RLN-style anonymous admission; 300 credentials at 1 cell per 30 s; prepaid leases; equivocators are revoked, not slashed; a launch subsidy pays for cover traffic.

**(b) Evidence**

*The slashing question (g2, s3).* g2: "Midnight cannot slash … Until a seizable asset exists, RLN's financial punishment has nothing to seize." **The code contradicts this.**
- `midnight-ledger/ledger/tests/token_vault_unshielded.rs:70` is the test "User deposits unshielded NIGHT tokens to contract", using `TokenType::Unshielded(NIGHT)` (`:211`).
- `:364` is the test "Contract withdraws unshielded NIGHT tokens to user."
- The standard library exposes `receiveUnshielded`, `sendUnshielded` and `unshieldedBalanceGte` (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1196-1241`).

So a contract can hold a NIGHT bond and release it to a reporter. The test is in the L8 working tree, with the same file in the upstream snapshot; whether it is active on mainnet is not checked. g2 is right that DUST cannot be seized and that fees are burned: the read-out finds no `v_fee` credit (read-out line 172), and the block-reward hook returns `(0, None)` in both builds (`midnight-node/runtime/src/lib.rs:691,695`, confirmed). s3's narrower claim is accurate: "not already supplied by Midnight." The nullifier construction is new work, and Taheri uses Groth16 on Ethereum (`2022-taheri-waku-rln-relay.txt:199`).

*Waku.* The Waku Network itself removed deposit slashing: "In the original RLN proposal, registration also involves putting down a deposit that is slashed" (`2024-revuelta-waku-latency.txt:178`). Deployed Waku relies on registration cost alone. This is real evidence for g2, g3 and s3: slashing is not necessary for a working network. It is not evidence that slashing is impossible.

*DUST arithmetic.* All of it checks:
- g3's "100 saturated blocks ≈ 90×" is 1.046¹⁰⁰ ≈ e^4.5.
- g2's "~20 messages/hour per NIGHT" is 0.714/24 ÷ 0.08 × 60 ≈ 22.
- g3's "one shard-day flood ≈ 770 NIGHT" is 5,530 memberships × 0.1 ÷ 0.714.

*My own transaction-size error.* My figure of ~6 KB per transaction was too low. The DUST spend proof alone is 2,912 B (`midnight-ledger/ledger/src/dust.rs:2106`, `DUST_SPEND_PROOF_SIZE`), and the call-proof estimate is 4,832 B (read-out line 379). g2's and g3's 8–10 KB, about 0.08–0.1 DUST, is the better planning number. My anchorer budget rises from ~121 to ~170–200 NIGHT.

*s2's evidence for the stamp.* It supports the stamp as specified. The economics are labelled unknown, which is honest but leaves D4 unanswered.

*Waku sustainability.* Waku's own sustainability section supports unpaid relaying: relaying "has inherent value for participants". It also proposes a paid service marketplace for Store and Filter (`2024-cornelius-waku-network-dapps.txt:130-148`). That is my split: relays unpaid, services paid.

**(c) Vote: my own position (o2), with three amendments drawn from this review.**

1. **Close the self-slash refund.** In my R1 design, a spammer who double-signals can call `slash(sk)` on themselves and recover the 50% reporter share. Change the split:
   - the reporter receives at most 10%, paid from the treasury after the 7-day window;
   - 90% of the bond is burned or goes to the treasury.

   Taheri's two RLN risks are handled as follows. The early-withdrawal escape (`2022-taheri-waku-rln-relay.txt:498-503`) is already covered by my withdrawal delay. The copy-and-claim race (`:372-383`) does not apply, because `sk` is a private witness in a Compact proof.
2. **Adopt g3's byte-denominated budget** instead of per-event counts, so size classes are billed honestly.
3. **Adopt s3's revocation from future snapshots** as the launch fallback if the slash contract misses phase 1. The bond then still costs capital, and the registration fee is still non-refundable.

Why not the DUST-only models (g2, g3)?
- **Nobody is paid.** Burned DUST funds no operator, so stores and relays are run only by parties paid elsewhere. In practice that is the foundation and wallet vendors.
- **The attacker's capital is never at risk.** DUST regenerates from held NIGHT (`midnight-docs/docs/concepts/dust-architecture.mdx:109-111`), so the attacker pays only a regenerating opportunity cost. By g3's own arithmetic, 6,200 NIGHT held, never spent, floods all 8 shards every day. My model costs 30,000 NIGHT locked plus 1,200 NIGHT of fees per 30 days at a higher network capacity. The fees go to a treasury that pays for storage.

Why not s2's stamps?
- **Privacy.** Stamps are bound to the object and issued after encryption, so the issuer sees the timing of every publication against a billing account. s2 says this.
- **Concentration.** Three issuers hold the power to mint capacity.

**(d) Strongest objection to the leading position.** The leading position, by count, is "paid membership plus a nullifier rate cap, no slashing, relays unpaid" (g2, g3, s3). Its weakness is that no actor in it has a protocol income, so the "open participation" end state has no mechanism behind it.

The strongest objection to my position is different. **A bond that must stay locked forgoes DUST generation:** spending NIGHT into a contract starts decay, per `dust-architecture.mdx:25,125`. Honest small publishers pay that capital cost too. The case for my model then rests on whether sponsors (dApps, wallets) will post bonds for their users. That is an unmeasured market assumption.

---

## D5 Performance requirements

**(a) Positions**
- **g2:** D = 8, D_out = 4, heartbeat 1 s. Relay cap ~104 class-S messages/s at m = 7. Class S p50 ≤ 1 s and p99 ≤ 2 s at N = 1,000; p99 ≤ 6 s under a 20% Sybil cold start.
- **g3:** D = 6. Shard cap of 10 events/s and 64 KiB/s (80 events/s across the network). Light-shard p50 < 1.5 s, p99 < 3 s. One proof per burst of at most 32 messages.
- **s2:** 10 cells/s normal, 100 stress, as one stream. p50 ≤ 2 s, p95 ≤ 5 s, p99 ≤ 15 s. A mobile profile of 1 cell/s.
- **s3:** 10 cells/s, 20 for recovery. p50 ≤ 5 s, p95 ≤ 20 s, p99 ≤ 35 s. A gateway at 409.6 Mbit/s for 500 subscribers.

**(b) Evidence**
- g3's RLN timings are exact: generation 85.7 / 276.3 / 766.8 ms and verification 2.7 / 4.5 / 18.7 ms on M1 / DO 4-CPU / Pi 4 (`2024-revuelta-waku-latency.txt:251-270`). These are nwaku Groth16 numbers. g3 correctly labels them as transferred, not Midnight measurements.
- **g2's correction of Farooq is itself wrong.** g2 recomputes (0.1 + 8·10⁶/50·10⁶) × 4 = 1.04 s and discards the paper's printed 5,520 ms (`2025-farooq-staggering.txt:538-543`). But 5,520 ms is what you get when τ_tx is the time to upload D = 8 copies over one 50 Mbit/s link: (0.1 + 8 × 0.16) × 4 = 5.52 s. The paper's figure is consistent, and g2's per-hop transmit times are 8× too low.
  - For 4 KiB this changes nothing material: ~5 ms per hop.
  - For 64 KiB it adds ~84 ms per hop, roughly 0.3 s at H = 4, which pushes class M toward g2's own 3 s bound under load.
- s2's and s3's bandwidth arithmetic checks: 10 × 1,054.72 × 1.25 × 86,400 = 1.139 GB/day, and 20 × 4,096 × 86,400 = 7.078 GB/day.

**(c) Vote: g3's per-shard cap (10 events/s and 64 KiB/s), with g2's attack SLO (≥ 99% delivery and p99 ≤ 6 s at 20% Sybils) and g3's latency targets (p50 < 1.5 s, p99 < 3 s).** A per-shard cap gives each node class a bounded bill, and that bound is what you need to price a store operator. s3's p99 of 35 s is too loose to serve agents.

**(d) Strongest objection.** Every latency and CPU target in all five proposals depends on an admission-proof cost that has not been measured on Midnight's proof system. The only Midnight figures are the ledger cost model (3.27 ms plus a per-input term) and laptop proving of 5–30 s for a Zswap spend. Neither is an RLN circuit.

---

## D6 Storage requirements

**(a) Positions**
- **g2:** a 10-minute relay cache; optional stores keep 24 h, or 7 d if anchored; ~26.4 GiB per store-day across 8 busy shards; unpaid.
- **g3:** 48 h stores; an optional 14-day archive (about 0.9 TiB at L2); one root cell on the ledger; nullifiers held in relay memory; durability means three stores per shard.
- **s2:** every storage relay keeps the complete stream for 7 days (12 GB provisioned at normal load); three storage receipts; receipts are "contractual, not proof".
- **s3:** 48 h; 32 GB per relay; three signed receipts; replay buckets rotated only when old events can no longer be used.

**(b) Evidence**
- g3's `global_ttl` of 1,209,600 s is confirmed (`ledger-parameters-config.json:176`), as is `bytesWritten` of 50,000 (`:159`).
- g3's figure of ~1.7 GB/year for an on-chain nullifier set is correct arithmetic, and a good argument against per-message nullifiers on chain. My design keeps only memberships and a bounded anchor ring on chain.
- s2's and s3's receipts have no enforcement path. Both say so.

**(c) Vote: g3's 48 h default and the rule that only roots go on chain, plus my bonded challenge game and bounded anchor ring.** The challenge game is what turns s2's and s3's receipts into something a contract can enforce. A store that signed a receipt and holds a bond either answers `challenge(t, leaf)` before a `blockTimeLt` deadline or loses the bond.

**(d) Strongest objection.** The leading position is unpaid stores (g2, g3), with s3's unenforced receipts. It promises 48 h availability and gives no store operator a reason to keep data it does not itself need. g3's own exit test ("relay payment only if volunteer stores miss the 48 h SLO") will be passed in phase 1 while the foundation runs the stores, and missed later.

---

## D7 Infrastructure actors (the decision I lead)

**(a) Positions**
- **g2:** validators excluded; volunteer relays and stores; at least 4 bootstrappers separate from the chain bootnodes; relays paid in phase 3 "only if a real payment path exists".
- **g3:** sidecar relays, stores and filter nodes, all unpaid; wallet providers carry the filter fan-out bill; validators excluded.
- **s2:** contracted dedicated relays, gateways and issuers; at least 5 independent organizations and 3 issuers at launch; permissionless admission without issuers is a later milestone.
- **s3:** a published operator roster; registry administrators whose power to censor is explicit; "decentralization means removing administrator discretion".

**(b) Evidence**
- `system-parameters-config.json:6-8` confirms 10 permissioned and 0 registered validator seats (s2, s3).
- `service.rs:614-625` confirms that validators do not serve ledger-sync because of CPU contention (g2).
- `2024-heimbach-deanon` (validator IP mapping) is cited plausibly by g2; I did not open it.
- `2002-douceur-sybil` (s3) correctly limits what peer counts prove.

**(c) Vote: my own position (o2), amended with s2's launch gate** (at least 5 independent operator organizations) **and s3's disclosure rule** (state the administrator's censorship power).

Paid, bonded, audited roles go only where the work is checkable: stores (challenges) and anchorers (one per slot). Relays stay unpaid, as in all five proposals and in Waku §III-E. Each phase gate (launch L → open O → decentralized D) is a number anyone can read from contract state.

**(d) Strongest objection.** My per-bond-key saturation cap (1/k) can be split across Sybil keys. I conceded this in R1, citing `2026-cao-nymreputation` Appendix D. So "no operator above 1/k" can be checked per key but not per real-world entity. g2's and g3's volunteer model avoids this problem only by paying nobody.

---

## D8 Network tether

**(a) Positions**
- **g2:** a hybrid sidecar running GossipSub v1.1; the ledger holds memberships and hash anchors. Fallback: ledger-9 `Misc` plus `contractEvents`.
- **g3:** the same hybrid. Fallback: a default-off notification protocol inside the node, which is a fork.
- **s2:** a separate libp2p overlay with optional anchoring. Fallback: replicated gateways serving the same opaque stream.
- **s3:** the same hybrid. Fallback: a common ledger announcement contract.

**(b) Evidence.** All of it checks:
- `midnight-node/Cargo.lock:14548` has `sc-network-gossip` and no `gossipsub` or `floodsub`.
- `command.rs:326` selects `NetworkWorker`.
- `check_call_filter.rs:44-45` deliberately leaves `send_mn_transaction` out of the safe-mode whitelist, as s2 and s3 say.

**(c) Vote: the hybrid sidecar (all five agree), with g2's fallback** (`Misc` plus the indexer). That is also my R1 fallback. It is the only fallback that needs no new operators and no node fork. It is limited to ledger 9 and is public; label it so.

**(d) Strongest objection.** Each fallback brings its own funding problem. g3's node fork has to be run by operators who are paid nothing for it. s2's gateways are a small set of companies, which is the outcome my lean warns about.

---

## D9 Threats and open risks

**(a) Positions**
- **g2:** eclipse defence through the outbound quota and separate peer tables. Phase 0 blocks unless the GossipSub crate fixes CVE-2022-47547. Least Authority's audit findings are listed as open work.
- **g3:** caps, scoring and expiry. Names a split-view double-spend of nullifiers and a replay window after a relay restart.
- **s2:** composition is the leading risk. The three forward-secrecy attacks in `2026-cheval-dr-automated` must be reproduced. A compromised issuer can mint capacity.
- **s3:** 15 ranked threats, led by a contract accepting forged data. Five blocks, including any claim of global-observer privacy and any unbounded state.

**(b) Evidence**
- s3's citations to Dandelion++ §3.1 (AS-level adversaries out of scope) and to Katzenpost replay protection on restart are used in the scope the papers give them. I did not reopen them.
- g2's CVE gate is tied correctly to `2023-kumar-gossipsub-acl2s`.

**(c) Vote: s3's ranking and blocks, plus g2's CVE gate**, plus the economic threats none of the four list:
- the self-slash refund (fixed in my D4 amendment)
- splitting stakes across bond keys
- a treasury drain through challenge griefing
- a DUST price spike that stalls anchoring
- issuer capture (s2)

**(d) Strongest objection.** s3's list has no economic attacks at all. It also treats the registry administrator as a permanent, disclosed censor, with no measurable path to removing them.

---

## D10 Build and verification plan

**(a) Positions**
- **g2:** simulations at 50, 200 and 1,000 relays; hard stop conditions (delivery < 99%, or no CVE fix) that fall back to anchors only; a small model of admission only.
- **g3:** a Shadow or testnet run with 32 and 100 sidecars; **a devnet registration transaction must be ≤ 16 KiB and ≤ 0.5 DUST**; measure ECDH on phones; a Quint or TLA+ model of the quota set.
- **s2:** freeze the crypto profile and run an audit gate, then a bounded prototype, then 10,000-subscriber simulations; check activation on the actual ledger generation.
- **s3:** model authorization and allowance resets; simulate targeted adversaries at 1%, 3% and 5%; a 7-day pilot; a later mix profile with classifier advantage ≤ 0.05.

**(b) Evidence.** All plans cite method papers as templates, not results. Each one says so.

**(c) Vote: my phase 0, plus g3's devnet fee gate and g2's stop conditions.** Mine is the only plan with an economic simulation and invariants on contract funds: total NIGHT equals bonds plus treasury plus escrow; payouts are capped. g3's measured gate replaces everyone's inferred DUST price with a real one.

**(d) Strongest objection.** None of the plans, mine included, has an exit test for the funding model that a third party can run before mainnet. A simulated treasury runway is still a simulation. The first real evidence is phase-O operator entry, and by then the foundation has run everything for six months.

---

## Where the group will disagree

1. **D4 Sustainable model.** There are four incompatible mechanisms: burned DUST membership, issuer stamps, administered leases, and bonded RLN with a treasury. The split is not just about evidence: it is whether the protocol should pay anyone.
2. **D3 Pub/sub model.** Pinned shards (g2, g3, mine) or one global stream with whole-feed download (s2, s3). That trades the size of the anonymity set against a per-subscriber bandwidth bill of 1–7 GB/day, and it decides whether mobile wallets are in v1.
3. **D7 Infrastructure actors.** Volunteer operators (g2, g3), contracted operators and issuers (s2), an administered roster (s3), or bonded paid roles with measured gates (mine). It follows from D4, and the decentralization end state is framed differently in each.

**The one fact that would settle the most disagreement:** the **proof size and verification time of an RLN-style membership proof built with midnight-zk (PLONK/KZG on BLS12-381, Poseidon matching `transientHash`), measured on a 4-vCPU relay and on a laptop prover.**
- It decides the admission field in D1: 0 B, 354 B, 1,152 B or 4 KiB.
- It decides between per-message ZK (g3, s3, mine), Ed25519 with a cached membership (g2), and RSA stamps (s2) in D4.
- It decides relay CPU and publisher latency in D5.

g2 already states the threshold: under 200 bytes and under 1 ms to verify, or the proof stays off the hot path. The other big factual dispute is whether a contract can seize NIGHT. I checked it for this review: a contract can hold and release NIGHT (`midnight-ledger/ledger/tests/token_vault_unshielded.rs:70,364`). Whether that is enabled on mainnet still needs checking.
