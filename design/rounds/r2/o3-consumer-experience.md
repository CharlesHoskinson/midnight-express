# Round 2 cross-review: o3 (consumer and developer experience)

**Reviewer summary.** I read g3, g4, s3 and s4 against the code and papers they cite. Two verification passes checked 23 Midnight code claims and 21 literature claims, and I checked the arithmetic by hand. Most citations hold. Three findings change the debate:

1. **No public network can run any design that rides `emit`/`Misc` today.** That includes mine and g4's. The Compact 0.33 release notes say ledger 9 "will be, but is not yet, deployed on Midnight Mainnet" (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:10-12`). The docs say "Preview, Preprod, and Mainnet currently run ledger version 8" (`midnight-docs/docs/concepts/how-midnight-works/building-blocks.mdx:79-83`).
2. **The 1 KiB silent-drop constant that four of us cite cannot be confirmed in the pinned VM revision.** `MAX_LOG_EMITTED` appears only in a cargo checkout `9a8777c` (`~/.cargo/git/checkouts/midnight-ledger-…/9a8777c/onchain-vm/src/vm.rs:41-43, 274, 600`). The node pins onchain-vm `54a4e013` (`midnight-node/Cargo.lock:8460`), and that revision is not on disk.
3. **g4's spam-cost figure understates the sustained cost by about 7×** (details under D4).

I keep my D3 delivery semantics. I give up two of my own choices: the PRF-tag/bucket machinery, in favour of g4's simpler constant-name envelope, and the Merkle-anchor contract path, in favour of s3's signature-plus-nullifier path.

---

## D1 Event format

**(a) Positions**
- **g3:** Sidecar envelope. Relays can see shard, class, expiry, quota day, membership root, chunk nullifier and admission proof. Padded classes are 1, 4 and 32 KiB, expiry is 48 h, and there is no view tag.
- **g4:** One `Misc` event of 288 B. The `name` is the constant `MPE1`. The payload is a 256 B ChaCha20-Poly1305 ciphertext carrying a 205 B body. The indexer `id` is the only cursor, and indexer retention is 14 days.
- **s3:** Fixed 4,096 B cell: 128 B header, 1,152 B admission area, 2,816 B protected data. A header-encrypted Double Ratchet runs inside. Cells live 48 h.
- **s4:** Fixed 2,048 B record with a salted, truncated PRF recognition hint, a 128 B issuer permit, up to 1,024 B of application data and up to 16 fragments. Records live 48 h.

**(b) Evidence**
- `Misc` is `{name: Bytes<32>, payload: Bytes<256>}`, tag 10, 288 B (`minokawa-compact/compiler/midnight-events.ss:71-74`). **Confirmed.**
- The VM drops log items over 1 KiB without an error and caps the `log` argument at 512 KiB. The text is confirmed only in checkout `9a8777c` (`vm.rs:38-43, 274, 560, 600`).
  - s3 cites `ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:38,268,595`. s4 cites `midnight-ledger@54a4e013/vm.rs:39,43,268`. Neither path exists on disk: `54a4e013` is the pinned revision, but it is not checked out.
  - Logs counted as churn, as both written and deleted bytes, is confirmed (`9a8777c vm.rs:590-597`).
  - **Inference:** the constant probably exists at `54a4e013`, but nobody has shown it. My own proposal inherited the same unverified provenance from the read-out.
- g4 cites `compact-reference.mdx:3497-3507`. It supports "standard event types only" and "no emit in the constructor". It does not state "disclosed fields"; that appears only in the example at `:3528`.
- g4 says CoIP-0003 "refuses" encryption and topic filters. `coip-0003.md:107-109` actually *defers* them as "a different problem" and does not mention the VM.
- The node keeps no logs. The applied-transaction record has roots, hashes, addresses and UTXO deltas but no events field (`ledger/src/ledger_9/mod.rs:460-470`). **Confirmed.**
- s3's header encryption hides "which messages belong to which sessions, or the ordering" (`2016-signal-double-ratchet-spec` §4.1). **Confirmed.**
- s4 says MLS exposes group ID and epoch (`2023-barnes-rfc9420` §16.4). **Confirmed.** "Content type" comes from the `PrivateMessage` struct, not from the §16.4 prose.

**(c) Vote: g4**, with two amendments.
1. **Replace the indexer `id` with a portable cursor `(height, tx_index, log_index)` plus `eid = H(name‖payload)`.**
   - Production runs two indexer instances behind one hostname and re-indexes the secondary "empty" (`midnight-indexer/docs/re-indexing.md:78-95`).
   - The document never says whether `id` values survive across instances. That is still **unknown**.
   - g4's "the indexer `id` is the only cursor" is therefore a silent-skip risk on failover.
2. **Keep the version byte meaningful** so that MIP-0019 multipart can be added later as v2.

I withdraw my PRF tags with a 32-tag expected window. If a publisher abandons more than W sequence numbers, the recipient never recognises the later events, which is a consumer-correctness bug I introduced. At g4's cap, trial AEAD on 228 B against a few hundred keys is cheap, and the constant `name` hides more.

**(d) Strongest objection to the leading position.** The leading position is an off-chain fixed cell of 2–4 KiB (g3, s3, s4). Every full-stream subscriber pays for every byte of every cell. s3 puts 1,152 B of admission data, 28% of each cell, into the stream. A 4 KiB cell costs a consumer 14× more than a 288 B `Misc` per event, and in all three of these designs the consumer cost is the binding one (D5).

---

## D2 Definition of "private"

**(a) Positions**
- **g3:** Content confidentiality; subscriber-interest privacy at shard granularity only; weak protection of the publisher's IP through a one-hop stem; no relationship or timing privacy.
- **g4:** Exactly four claims: confidentiality, topic privacy, integrity, and chain-level publisher unlinkability. It explicitly claims no forward secrecy, no volume privacy and no global anonymity.
- **s3:** Separate, conditional claims. It declines to claim publisher unlinkability over gossip and blocks any strong global-observer claim.
- **s4:** Content and authenticity, subscriber-selection privacy, topic-label confidentiality and limited record unlinkability. It makes no publisher-unlinkability claim.

**(b) Evidence**
- `2017-das-trilemma`: strong anonymity, low bandwidth and low latency cannot all hold against a global passive adversary (lines 27-31). **Supports all four.**
- `2018-fanti-dandelionpp` §3.1 puts ISP- and AS-level adversaries "outside the scope", and Theorem 1 assumes a random 4-regular graph (lines 273-275, 631). **Supports s3 and s4.**
  - g3's "one-hop stem" is not the construction Dandelion++ analyses. **Inference:** g3's "weakly" has no evidence behind it.
- `2022-barnes-rfc9180`: "HPKE does not provide forward secrecy with respect to recipient compromise" (line 1525). **Supports g4 verbatim.**
- `2017-piotrowska-loopix` §2.2 excludes client Sybils. s4 is right that a *corrupt* provider is limited to honest-but-curious behaviour (lines 176-183). s3's "assumes conditions on providers" is acceptable.

**(c) Vote: s4.** It is the only proposal that says full-stream retrieval hides *selection*, not *participation*, and names reactions as the leak. Add two things:
- g4's chain-level publisher unlinkability for any ledger lane. Midnight transactions have no signer.
- My property X: an unlinkable contract reaction, which holds if the D3 contract path uses a hidden publisher-set membership proof.

**(d) Strongest objection to the leading position.** The leading position is "content plus selection privacy, no global-observer claim". It is undone by consumer behaviour, and no proposal puts the countermeasure in the SDK.
- An agent that reacts on a match, whether by contract call, acknowledgement, blob fetch or reply, links itself to the event through timing.
- s3 (#10, selective-feed tagging) and s4 ("interest-dependent disconnects…") name the leak but specify no API rule.

The property needs normative SDK rules:
- no automatic reaction;
- reactions batched or jittered by default;
- fetches of off-chain blobs flagged as a leak in the type system.

---

## D3 Publish and subscribe model (my lead)

**(a) Positions**
- **g3:** Eight pinned public shards (`H(contract) mod 8`). Relays join the mesh, light clients use a unicast filter node, and delivery is at least once with 48-h back-fill. Contracts consume an event through a later batch-root inclusion proof.
- **g4:** One bus contract, an out-of-band 32 B key, full-stream download and local trial decryption. Order follows the indexer `id`. Contracts do not consume events.
- **s3:** Subscriptions are local, the whole feed is retrieved, and per-publisher sequence numbers allow a bounded reorder with explicit gaps. A contract consumes an event through a signed witness plus a replay nullifier.
- **s4:** Invitations, a complete stream, per-publisher sequence gaps and complete-window back-fill. A contract consumes an event through a follow-up transaction, and s4 states explicitly that an anchor proves the bytes, not the truth.

**(b) Evidence**
- The indexer replays from an inclusive cursor and then follows live (`contract_event.rs:98-152`; `schema-v4.graphql:1967-1968`). Delivery is at least once, and consumers must dedup (`midnight-js/packages/types/src/public-data-provider.ts:507-510`). **Confirmed.** These support my semantics and g4's.
- Field-prefix filters are "standard events only" (`schema-v4.graphql:558-559`). **Confirmed.** g4 is right, and my bucket mode needs a new indexer feature. It is not a reuse of an existing one.
- g3's eight shards: "sharding messaging traffic from all applications into eight pub/sub topics" (`2024-cornelius-waku-network-dapps` line 54). **Confirmed.** The paper also says it "can be scaled beyond" eight.
- Waku store queries reveal content filters (`2020-vac-waku2-store-spec` lines 366-367), and so do filter subscriptions (`2020-vac-waku2-filter-spec` lines 298-300). **Confirmed.** g3 accepts that its filter node learns the client's shard.
- s3's witness claim: a witness is a callback (`compact-reference.mdx:1153`). **Confirmed.**
- My cross-contract root check is allowed if the callee uses no witness (`toolchain-0.33.0.md:96-104`, guard 4). **Confirmed.**
  - However, a caller cannot *read* another contract's tree. It can only call a circuit that the bus contract exports (`toolchain-0.33.0.md:88`).
  - Cross-contract calls "can't [be deployed] to those networks yet" (`building-blocks.mdx:79-83`).

**(c) Vote: my own position (o3), amended.** Keep:
- finalised, at-least-once delivery in chain order;
- per-publisher `stream_seq`, with `gap`, `late` and `head` markers;
- a portable cursor;
- `processOnce`.

Replace three things:
- **Use full stream only in Phase 1.** Drop bucket mode, adopting g4's position.
- **Make s3's path the default contract path:**
  1. The publisher signature is verified in-circuit against a publisher set committed in the *target* contract's own state, through a Merkle membership proof so that the publisher is not disclosed.
  2. The signature binds genesis, target, action, logical ID and expiry.
  3. A consumed-nullifier makes the effect happen exactly once.

  This needs no anchor and no cross-contract call, so it does not depend on ledger 9.
- **Make the anchor optional,** only for applications that must prove *on-chain publication*.

**(d) Strongest objection to the leading position.** The leading position is full-stream local recognition (g4, s3, s4 and mine: four of five). Client bandwidth grows linearly with total bus volume. At s3's and s4's own design loads, every subscriber downloads 7.08 GB/day and 1.77 GB/day. So the overlay proposals pick an overlay for throughput, then pick a retrieval mode no wallet can sustain at that throughput. Full-stream retrieval is only coherent with a volume cap of the kind g4 sets.

---

## D4 Sustainable model

**(a) Positions**
- **g3:** A daily DUST membership transaction plus an off-chain byte budget enforced by chunk nullifiers. 10% of block usage is reserved, and relays are unpaid in v1.
- **g4:** The publisher pays DUST for each event. There is no new payroll, no proof of work and no RLN.
- **s3:** Prepaid service leases, plus RLN-style anonymous admission with 300 credentials at one cell per 30 s. A launch subsidy pays for cover traffic.
- **s4:** Sponsors buy relay and retention capacity. Admission uses issuer-signed single-use permits, so the issuer sees which customer published which event.

**(b) Evidence**
- `ledger-parameters-config.json` is confirmed: `blockUsage` 1,000,000 at line 158, `bytesWritten` 50,000 at 159, `generation_decay_rate` 8,267 at 166, `global_ttl` 1,209,600 at 176.
- `dust-architecture.mdx:111-116` confirms "71 DUST per day" per 100 NIGHT and a cap of about one week.
- RLN timings (`2024-revuelta-waku-latency` Table 1, lines 251-270):

  | Machine | Verify | Generate |
  |---|---|---|
  | M1 | 2.7 ms | 85.7 ms |
  | 4-vCPU cloud VM | 4.5 ms | 276 ms |
  | Raspberry Pi 4 | 18.7 ms | 767 ms |

  The paper also says nwaku "does not yet support economic punishment" (lines 218-219). That supports g3's and s3's refusal to promise slashing.
- `2015-schaub-bitmessage-antispam`: legitimate users and spammers face the same work (lines 467-469), and the paper's fix halves the harm (lines 32-34). g4's word "only" is its own framing.
- **Arithmetic**
  - **g3:** 553 DUST ÷ 0.714 DUST per NIGHT per day ≈ 774 NIGHT. **Correct.**
  - **s3:** 300 credentials ÷ 30 s = 10 cells/s. **Correct.**
  - **s4:** 0.08192 DUST × 1,440 anchors/day = 117.96 DUST/day, or 165.2 NIGHT. **Correct.**
  - **g4 is wrong.** Its flood of 4 events per block costs 0.32 DUST × 14,400 blocks = 4,608 DUST/day. Dividing by the *stock* cap of 5 DUST per NIGHT gives about 922 NIGHT, which pays for only *one day* starting from full capacity. A sustained flood needs 4,608 ÷ 0.714 ≈ **6,450 NIGHT**. That is consistent with my figure of 7,260 NIGHT at 86,400 events/day.

**(c) Vote: g4** for Phase 1: DUST per event, with nothing added. It is the only model a developer can reason about in an afternoon. The SDK reports `InsufficientDust` before proving.

**(d) Strongest objection to the leading position.** No proposal funds the read side, and in a full-stream design the cost grows with consumers, not publishers (s4 makes this point).
- At 10,000 subscribers × about 55 MB/day, public indexers serve about 0.55 TB/day.
- No indexer payment path exists (read-out §2.3).
- Every proposal that leaves reads unpaid, mine included, assumes a free public indexer will keep serving. It is the most likely component to fail first.

---

## D5 Performance requirements

**(a) Positions**
- **g3:** A shard SLO of 10 events/s or 64 KiB/s, relays at most 4 Mbit/s per shard, p50 < 1.5 s and p99 < 3 s, and batched RLN proofs.
- **g4:** A cap of `min(4 per block, 5% of blockUsage)`, a p50 ≤ 60 s gate, and 56 MiB/day per subscriber.
- **s3:** 10 cells/s of 4 KiB, 7.078 GB/day per client, p50 ≤ 5 s and p99 ≤ 35 s.
- **s4:** 10 records/s of 2 KiB, 1.769 GB/day per client, and a 100/s burst. Relay propagation targets are p99 ≤ 10 s nominal and p99 ≤ 30 s under burst.

**(b) Evidence**
- I re-ran every product (g3's L1 shard, s3's daily feed, s4's relay egress, g4's daily volume) and found no arithmetic errors.
- GossipSub amplification is about D and independent of N (`revuelta` lines 320-321). A 1,000-node simulation at D = 6 delivered messages of 25 KB or less in under 1 s (lines 402-405 and 652). **Confirmed for g3.**
- g3 cites a 50–70% scan-time cut from view tags. That is MRL73's *estimate* (`2021-monero-mrl73-viewtags` line 180). The measured figure is 30–40% (`2022-monero-pr8061-viewtags` line 201). My own citation of PR 8061 line 220 should point to line 201.
- g3 is right that a view tag does not remove the shared-secret scalar multiplication (MRL73 line 179).
- The slot is 6 s, block length is 1 MiB, and normal dispatch is 75% (`runtime/src/lib.rs:292, 300, 313`). **Confirmed.**
- Not stated by g3: a "light" client on one shard at g3's load L1 still downloads 10 KiB/s, about **0.88 GB/day**.

**(c) Vote: g4.**
- The cap is written as a formula that absorbs the transaction size once it is measured.
- Its consumer budget (56 MiB/day) matches mine (≤ 60 MB/day). Both are numbers a phone on Wi-Fi can meet.
- Its latency figure is a gate, not a promise.

**(d) Strongest objection to the leading position.** The leading position is roughly 10 events/s over an overlay with relay latency in seconds (g3, s3, s4). The latency targets exclude what the consumer actually waits for: proof generation for admission (276–767 ms per proof on cloud and Pi hardware, `revuelta` Table 1) and, for contract consumers, proving plus finality. Above all, the bandwidth targets are per *relay*, while the per-*consumer* figure (0.9–7 GB/day) is never gated. A design whose relays pass and whose wallets cannot keep up has not met a consumer SLO.

---

## D6 Storage requirements

**(a) Positions**
- **g3:** 48-h shard stores, an optional 14-day archive, and only a root on the ledger. Nullifiers live in relay memory with a one-day TTL.
- **g4:** Ciphertext lives in the log as churn, indexers keep 14 days, and contract state stays empty.
- **s3:** 48 h with 32 GB per relay, an optional paid 7-day archive, and signed storage receipts from three operators.
- **s4:** Every relay keeps 48 h, publishers get three receipts, an archive keeps 30 days, and s4 corrects MIP-0002.

**(b) Evidence**
- **s4's correction holds.** MIP-0002 Appendix B derives its bound from the 50 KB `bytes_written` budget (`mip-0002:520, 529`), but the VM counts logs as churn (`vm.rs:590-597`, `9a8777c`). MIP-0002 also assumes a 1 MB churn limit (`:151`), while mainnet config sets 50,000,000 (`ledger-parameters-config.json:160`). My proposal's use of Appendix B as a row-size bound survives; using it as a ceiling would not.
- `global_ttl` = 1,209,600 s is confirmed and supports the 14-day figures in g3 and g4.
- g4's "retention is an indexer policy of 14 days": I found no indexer setting for contract-event retention. **Unknown.** It is a new operator requirement, not an existing property.

**(c) Vote: g4**, 14 days. I move down from my 30. The SDK exposes `back-fill window = min(indexer retention, key retention)` through `capabilities()`.

**(d) Strongest objection to the leading position.** The leading position is 48 h (g3, s3, s4), which was sized for relay disk, not for consumer behaviour.
- A wallet that is off over a long weekend comes back to a `gap` it can never fill.
- s4 itself computes 3.5 GB to recover a full 48-h window, so even recovery within retention costs a phone more than it can pay.
- Retention must exceed realistic offline periods. Otherwise "at least once within retention" means "at most once" for intermittent consumers.

---

## D7 Infrastructure actors

**(a) Positions**
- **g3:** Open sidecar relays, stores and filter nodes. Validators are excluded, wallet providers carry the filter fan-out, and nobody is paid in v1.
- **g4:** No new role.
- **s3:** A published launch roster of dedicated relay operators, gateways, registry administrators and later mix operators, with the trust each holds stated.
- **s4:** Paid relays (20 across at least five operators), gateways, admission issuers and anchor submitters.

**(b) Evidence**
- Mainnet has 10 permissioned candidates and 0 registered (`system-parameters-config.json:7-8`). **Confirmed.**
- Safe mode deliberately filters `send_mn_transaction` (`check_call_filter.rs:44-45`). **Confirmed.**
- GossipSub v1.1 sets `D_out` "2 for a D of 6" and adds outbound quotas (`2020-gossipsub-v11-spec` lines 553 and 191-192). **Confirmed.**
- s3 cites `2002-douceur-sybil` only as a limit, which is a correct use.

**(c) Vote: g4.** Adding no role is the honest Phase-1 answer.

**(d) Strongest objection to the leading position.** "No new role", whether in g4 or in the overlay variants, hides a concentration: the Foundation's two-instance indexer (`re-indexing.md:78`). It sees every subscriber's IP and schedule, can omit events, and is unpaid. g4's defence is "run a second indexer", which is not something a developer does in an afternoon. The SDK must cross-check two independent endpoints by default, or the claim of "no new trusted role" is false in practice.

---

## D8 Network tether

**(a) Positions**
- **g3:** Hybrid. A GossipSub sidecar carries bulk traffic and the ledger holds the daily membership root. The fallback is a default-off node protocol.
- **g4:** Ledger plus indexer only, waiting for the `emit` generation. The fallback is a private indexer.
- **s3:** Hybrid. An independent libp2p overlay plus ledger authorization. The fallback is one ledger announcement contract.
- **s4:** Hybrid. An independent overlay plus optional anchors. The fallback is independent gateways.

**(b) Evidence**
- `midnight-node/Cargo.lock` contains no `libp2p-gossipsub`. **Confirmed.**
- The support matrix lists mainnet at `node-1.0.300`, `toolchain-0.31.1` and `onchain-runtime-3.0.0` (`support-matrix.json:14, 38, 82`). **Confirmed.**
- **Decisive:** Preview, Preprod and Mainnet run ledger 8 (`building-blocks.mdx:79-83`), and ledger 9 is "not yet" deployed (`toolchain-0.33.0.md:12`). Consequences:
  - g4's design and my Phase 1 have no public network to run on today.
  - My plan to measure on preprod in Phase 0 is impossible. It must run on a local ledger-9 network.
  - g3's design needs only a root write, so it can deploy on ledger 8.
  - s3's ledger fallback also needs ledger 9 if it uses events.
- s4's lockfile pins are confirmed: the ledger crate `6abe9b16` (line 7894), onchain-vm `54a4e013` (8460) and base-crypto `dc87cc8f` (7609).

**(c) Vote: my own position (o3)**, a phased hybrid with an explicit switch:
- **If ledger 9 has a mainnet date before the Phase-1 date:** Lane A first (g4's envelope), then the overlay.
- **If not:** start with my fallback (the overlay with batch roots anchored on the ledger) under the *same* consumer API, with every event labelled `gossip`.

g4's refusal to build a "temporary overlay" is principled. But if the wait has no end date, there is no product at all.

**(d) Strongest objection to the leading position.** The leading position is an overlay first (g3, s3, s4). The overlay brings a new Sybil set, a new spam regime and an operator-funding problem, and no proposal has priced any of them (s4: market prices **unknown**; g3: relays unpaid). Its admission credential, RLN or a Midnight membership proof, is also unbuilt, and the measured RLN implementation has no slashing. The overlay trades one unshipped dependency, ledger 9, for three unbuilt ones.

---

## D9 Threats and open risks

**(a) Positions**
- **g3:** Caps, scoring and expiry. It names the residual risk that a nullifier can be spent twice during a split view.
- **g4:** The fee market, full-stream download, a second indexer and out-of-band key rotation. It does not claim forward secrecy.
- **s3:** 15 threats ranked; #1 is a contract that accepts forged data. Five red-team blocks.
- **s4:** Defences tied to specific configurations, with GossipSub's formal-verification failures and the FMD rejection explicit.

**(b) Evidence**
- FMD lets the server recover much of the social graph when it knows the senders (`2021-seres-fmdfalsepositives` lines 73-74 and 95-96). **Confirmed for s4 and me.**
- `2021-len-partitioningoracle` lists ChaCha20/Poly1305 as non-committing (lines 63-64) but calls those attacks "more limited" (lines 38-39). g4's residual-risk statement is fair.
- Bloom filters: users with fewer than 20 addresses "risk leaking all" of them (`2014-gervais-bloomfilters` lines 69-71). My word "nearly" overstated it.
- MLS PCS can be defeated by a delivery service that suppresses updates (`rfc9420` lines 5854-5856). **Confirmed for s3 and s4.**
- s3's `2015-heilman-eclipse` and s4's `2022-kumar-gossipsub-formal`: **not checked by me**.

**(c) Vote: s3.** Its ranking puts the consumer's worst failure first: a contract that acts on forged data. It blocks unverified witnesses and silent fallbacks, and those blocks belong in the specification whatever the transport.

**(d) Strongest objection to the leading position.** No threat table gives the consumer a test for *completeness*.
- s3 says manifests authenticate content, not completeness, and offers no check.
- Per-publisher sequence numbers (mine, s3, s4) detect omission only on streams whose publishers are known. They cannot detect a withheld first-contact message or a whole publisher being suppressed.
- That makes indexer and gateway omission (s3 #10) the threat most likely to succeed silently. The residual risk must be stated as such, with cross-checking two independent sources as the default defence, not an option.

---

## D10 Build and verification plan

**(a) Positions**
- **g3:** Phase 0 is a Shadow or testnet run of 32 and 100 sidecars, phone ECDH measurements and a devnet fee measurement, with a Quint model of the quota set only.
- **g4:** Test vectors I1–I4 plus measurements, then a two-process soak, then a scanner, then stop. Triggers T1–T4 reopen the design.
- **s3:** Model authorization and epochs first, then adversary simulations at 1–5%, a 7-day pilot, an audit, an experimental mix, and MLS later.
- **s4:** Freeze the evidence and keep a claim register, then bounded models, a 72-h service run, Midnight integration, and finally a comparison against PIR and OMR.

**(b) Evidence.** s4's warning about provenance, that the lockfile matters more than the tag name, is borne out by the `MAX_LOG_EMITTED` finding above. g4's indexer claim that blocks near the tip are fetched by hash, with `FINALIZATION_SAFETY_MARGIN` = 400 (`chain-indexer/src/infra/subxt_node.rs:84-86`), is confirmed.

**(c) Vote: g4**, with additions:
- s4's claim register as the Phase-0 exit gate;
- my Quint model of the SDK delivery state machine, including indexer failover;
- my "afternoon test": at least 4 of 5 outside developers build a publisher and a crash-resuming subscriber in 4 hours or less.

All measurements run on a local ledger-9 network until a public network upgrades.

**(d) Strongest objection to the leading position.** The leading position is model first, then a bounded pilot. No proposal except mine gates on whether consumers can use the API correctly. g4's Phase 1 tests two processes and one indexer, so it would pass while the cursor breaks on the first primary/secondary failover. s3's and s4's gates measure relays and attackers. A protocol whose consumers mishandle duplicates, gaps or cursors loses events in production, whatever the relays do.

---

## Where the group will disagree most

1. **D8 tether.** g4 and o3 (Phase 1) want ledger plus indexer; g3, s3 and s4 want an overlay first. This split drives D1 cell size, D4 admission and D7 actors.
2. **D4 payment and admission.** The options are DUST per event (g4, o3), a daily DUST membership with off-chain quota (g3), RLN leases with cover traffic (s3), and issuer permits that give up anonymity from the issuer (s4). They differ in who learns what at admission, not only in cost.
3. **D5 and D3 volume versus retrieval mode.** Four of five choose full-stream recognition, but the target loads they pair with it differ by about 100×, from 56 MiB/day to 7 GB/day per consumer. Until the group fixes one consumer bandwidth budget, the D3 votes do not mean the same thing.

## The one fact that settles the most

**The mainnet activation date for ledger 9**, which brings `emit`/`Misc`, `contractEvents` and cross-contract calls.
- The current documents say mainnet, preprod and preview run ledger 8 (`building-blocks.mdx:79-83`; `toolchain-0.33.0.md:10-12`).
- If ledger 9 has a near date, the ledger-first Phase 1 (g4, o3) is buildable, and the overlay proposals must justify their extra actors on load alone.
- If it has no date, even g4 concedes ("evidence the target network will not ship `emit`… on any schedule"), and the debate narrows to *which* overlay.
- **How to check:** ask the node and ledger team for the hard-fork schedule, and compare the runtime spec version that mainnet RPC reports with the version in the local node tree (g4 cites `runtime/src/lib.rs:276`; I did not verify that line).
