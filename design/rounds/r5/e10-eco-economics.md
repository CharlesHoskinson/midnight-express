# MPE-ECO: Admission, economics and spam cost

## 1. Scope of this area

This area covers who pays for publishing, carrying and storing Events. It covers how an Envelope earns admission to the overlay and how the per-epoch rate limit is enforced. It covers what DUST, NIGHT and fees can and cannot do in the Midnight code, the optional bond, slashing and treasury mechanics, and how Bus Nodes behave at low load and in overload. It does not cover the Envelope byte layout (D1), mesh parameters and latency SLOs (D5), retention windows (D6), or operator admission and governance (D7). Where this area depends on those, section 5 records the dependency. Decision coverage: D4.

## 2. Parameters

| ID | Name | Default | Allowed range | Source |
|---|---|---|---|---|
| P-ECO-1 | Admission epoch length | 60 s | 30–3,600 s | o1, o2, o4 (60 s); s3 (30 s); g2 (3,600 s); DEC-ECO-5 |
| P-ECO-2 | Lowest-tier per-epoch credit limit | 10 credits | 1–1,000 | o1 tier 0; o2 tier T1; o4 uses 20 |
| P-ECO-3(c) | Credit weight of size class c | ⌈body bytes of c ÷ body bytes of the smallest class⌉ | 1–64 | g3 (an L chunk debits 32× an S chunk); g2 (M = 16 S credits); o2 R2 amendment 2; DEC-ECO-4 |
| P-ECO-4 | Membership period | 86,400 s | 3,600–1,209,600 s | g3 (daily); g2 (hourly); o1 (14 d). The upper bound is `global_ttl`, `midnight-node/res/mainnet/ledger-parameters-config.json:176`; DEC-ECO-5 |
| P-ECO-5 | Membership-root acceptance window | 3,600 s | P-ECO-1 to P-ECO-4 | o2 (1 h root window); o1 (last 60 anchored roots) |
| P-ECO-6 | Epoch clock tolerance | 20 s | 0 to P-ECO-1 ÷ 2 | o2, citing `2024-revuelta-waku-latency` §2.5.1 |
| P-ECO-7 | Bus Node nullifier retention | 2 × P-ECO-1 + P-ECO-6 | ≥ P-ECO-1 + P-ECO-6 | s3 (accept only the current or the immediately previous epoch) |
| P-ECO-8 | MPE share of `blockUsage` (registrations plus anchors), 24 h mean | 10% | 1–10% | g1, g3 (10%); g4 (5%); `ledger-parameters-config.json:158`; DEC-ECO-6 |
| P-ECO-9 | Client back-off threshold (last block's `blockUsage` fullness) | 50% | 25–90% | g3 |
| P-ECO-10 | Per-peer Envelope rate before proof verification | 20 Envelopes/s | 1–1,000 Envelopes/s | g2 (design choice) |
| P-ECO-11 | Admission-proof size gate | 4,096 B | 192–8,192 B | o2 Phase 0 acceptance (4 KiB) and change trigger (8 KiB); o1 R2 (stamp fallback above 1 KiB); g2 (<200 B to keep on the hot path) |
| P-ECO-12 | Admission-proof verification gate | 10 ms on one core of a 4-vCPU VM | 1–20 ms | o2 Phase 0; measured comparator 4.5 ms Groth16 in `2024-revuelta-waku-latency` Table 1 |
| P-ECO-13 | Registration-transaction gate | ≤ 16 KiB and ≤ 0.5 DUST at genesis-like price factors | fixed gate | g3 D10 |
| P-ECO-14 | Bond withdrawal delay, and how long equivocation evidence is kept | 604,800 s | ≥ P-ECO-5 + 86,400 s | o2, o4; escape-by-withdrawal risk in `2022-taheri-waku-rln-relay` txt L498-503 |
| P-ECO-15 | Reporter share of a slashed bond | 10% | 0–10% | o2 R2 amendment 1 (closes the self-slash refund) |
| P-ECO-16 | Treasury runway divisor (daily payout ≤ balance ÷ P-ECO-16) | 365 days | 180–730 days | o2 D4.2 |
| P-ECO-17 | Payout saturation divisor k (per-bond-key share ≤ pool ÷ k) | 10 | 3–100 | o2 (k = 10 in phase O); o4 (1/k, from `2021-diaz-nym`) |
| P-ECO-18 | Retention-challenge response deadline | **assumption** 3,600 s | 600–86,400 s | o2 gives a `blockTimeLt` deadline but no number; set by simulation |

## 3. Requirements

### MPE-ECO-001 No proof-of-work admission
The Bus Node shall not use proof-of-work as an admission criterion for an Envelope.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; all twelve proposals reject PoW; `2004-laurie-proofofwork` §§3–4; `2015-schaub-bitmessage-antispam`
- Rationale: PoW costs honest phones as much as it costs stolen compute, and it pays no operator.
- Verify: inspection of the Bus Node validator code path; a test that an Envelope with no work field is accepted when all other checks pass.
- Status: settled

### MPE-ECO-002 DUST is not operator payment
MPE shall not require any party to transfer DUST to an Operator.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; g1, g2, g3, o2, s1, s2, s4; `midnight-docs/docs/concepts/dust-architecture.mdx:23`; `midnight-node/runtime/src/lib.rs:691,695` (reward hook returns `(0, None)`)
- Rationale: DUST is shielded, non-transferable gas, and no code path credits `v_fee` to anyone (notes §2.3, an **inference** that fees are burned).
- Verify: inspection of the client library and Bus Node payment interfaces; no DUST-transfer call exists.
- Status: settled

### MPE-ECO-003 No Midnight transaction per overlay Event
The MPE client library shall publish an Event on the overlay without submitting a Midnight transaction for that Event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; g1, g2, g3, o1, o2, s1–s4; notes §9 item 6; `ledger-parameters-config.json:158`
- Rationale: a transaction of about 8 KB costs about 0.08 DUST at genesis prices (**inference**), and the block-usage limit caps the chain at roughly 21 such calls per second.
- Verify: test: publish 1,000 Events through the Prototype and count zero Ledger Adapter submissions.
- Status: open (DEC-ECO-1)

### MPE-ECO-004 DUST-paid membership registration
When the Registry receives a registration call carrying a membership commitment and a paid DUST fee, the Registry shall insert that commitment into the membership set for the current membership period.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D4; o1, g3, g2, o2; `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:105-232` (membership plus nullifier pattern, notes §6.3)
- Rationale: holding NIGHT, through the DUST it generates, becomes the price of publishing, and no new token is needed.
- Verify: test on a ledger-9 devnet: register, then confirm that the next published root contains the leaf.
- Status: open (DEC-ECO-1)

### MPE-ECO-005 Sponsored registration
The Registry shall accept a membership commitment from any caller that pays the registration fee, without requiring that caller to know the admission secret.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D4; o2 (sponsor role), s1 (sponsors buy idle capacity), s4
- Rationale: wallets and dApps can onboard users who hold no NIGHT. A sponsor learns that it registered a user, not which Events that user publishes.
- Verify: test: a sponsor registers a commitment generated by a separate client, and that client then publishes successfully.
- Status: settled

### MPE-ECO-006 Dedicated admission secret
The MPE client library shall generate the admission secret independently of every wallet, encryption, signing and session key.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; s1, s3, g1 (separate `admit_sk`); `2022-taheri-waku-rln-relay` §II-B (misuse reveals the secret)
- Rationale: equivocation reveals the admission secret by design, so it must expose nothing else.
- Verify: inspection of key derivation; a test that the admission secret has no derivation path from any other key.
- Status: settled

### MPE-ECO-007 Shielded fee payment
The MPE client library shall pay Registry registration fees from shielded DUST without attaching unshielded inputs or outputs to that transaction.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; g1 D4; o1 D4; notes §3.4; `midnight-ledger` L9 `ledger/src/dust.rs:469` (public `v_fee`, hidden payer)
- Rationale: unshielded inputs publish the owner and would link the funding address to the membership.
- Verify: inspection of three devnet registration transactions built by the client: no unshielded offer is present.
- Status: settled

### MPE-ECO-008 Live fee quotes
When the MPE client library quotes the DUST cost of a Registry transaction, it shall compute the quote from the `ledgerParameters` of the latest finalized block.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D4; o3, g3, s3, s4; notes §7.2 (prices move up to about 4.6% per block); `base-crypto/src/cost_model.rs:354-405,408`
- Rationale: genesis prices are not live prices; 100 saturated blocks compound to about 90× (g3, checked by o2 R2).
- Verify: test with a mocked block whose parameters double the price: the quote doubles.
- Status: settled

### MPE-ECO-009 Insufficient DUST reported before proving
If the available DUST is less than the quoted fee, then the MPE client library shall return an insufficient-DUST error before generating any proof.
- Pattern: unwanted
- Scope: PROD
- Priority: SHOULD
- Source: D4; o3 R2 (`InsufficientDust`)
- Rationale: proving takes seconds on a laptop (notes §6.2), so failing late wastes that time.
- Verify: test with a balance below the quote: the error is returned and the prover is never called.
- Status: settled

### MPE-ECO-010 Client back-off under chain congestion
While the last finalized block's `blockUsage` fullness exceeds P-ECO-9, the MPE client library shall defer membership renewals that are not due within the current membership period.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: D4; g3 D4
- Rationale: the bus should not push Midnight's fee curve upward by itself.
- Verify: test with a mocked block fullness of 60%: renewals due in the next period are not submitted until fullness drops.
- Status: settled

### MPE-ECO-011 Chain-share budget
MPE shall consume no more than P-ECO-8 of `blockUsage`, averaged over 24 h, for Registry registrations and Anchors combined.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D4; g1, g3 (10%); g4 (5%); `ledger-parameters-config.json:158`
- Rationale: this is a budget, not a mechanism; no contract can enforce a chain-wide share (o4 R2, s4 R2).
- Verify: analysis of 7 days of testnet blocks: sum the bytes of MPE transactions and divide by the total block-usage limit.
- Status: open (DEC-ECO-6)

### MPE-ECO-012 Admission Proof required
If an Envelope lacks an Admission Proof, or its Admission Proof fails verification, then the Bus Node shall return GossipSub `Reject` for that Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2, o1, g1, g3; `rust-libp2p/protocols/gossipsub/src/types.rs:51-58` (`Reject` triggers the P₄ penalty)
- Rationale: an invalid proof is the forwarding peer's fault, so the P₄ penalty should apply.
- Verify: test: inject a mutated proof; the receiver reports `Reject` and the sender's P₄ counter increases.
- Status: settled

### MPE-ECO-013 Cheap checks before proof verification
The Bus Node shall complete the length, epoch, root-window and nullifier-duplicate checks on an Envelope before verifying its Admission Proof.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; o2 D3 (check order); g1 D1; s3 D4 ("valid proofs do not protect against a flood of invalid proofs")
- Rationale: proof verification is the most expensive check, so it runs last.
- Verify: test with instrumentation: an Envelope with a stale epoch never reaches the verifier.
- Status: settled

### MPE-ECO-014 Epoch freshness
If an Envelope's admission epoch differs from the Bus Node's current epoch by more than P-ECO-6 beyond the epoch boundary, then the Bus Node shall return GossipSub `Ignore` for that Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2 (±20 s); g1 (an expired object is Ignore, not Reject); `types.rs:56-58`
- Rationale: late arrival can be honest propagation delay, so it should not be penalised.
- Verify: test at offsets of P-ECO-6 − 1 s (accepted) and P-ECO-6 + 1 s (Ignore, no P₄ change).
- Status: settled

### MPE-ECO-015 Root window
If an Envelope's Admission Proof references a membership root published more than P-ECO-5 before the Bus Node's current time, then the Bus Node shall return GossipSub `Ignore` for that Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2, o1; g1 R2 (`HistoricMerkleTree` accepts prior roots)
- Rationale: membership expiry and revocation only take effect if old roots stop being accepted.
- Verify: test with a mocked root aged P-ECO-5 + 1 s: Ignore.
- Status: settled

### MPE-ECO-016 Committed rate limit
The Bus Node shall reject an Envelope unless its Admission Proof shows that every credit index used is below the per-epoch limit committed in the membership leaf.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; `2024-vac-rln-v2-spec` ("RLN-Diff flow", `rate_commitment`); o1, o2, o4; s1 R2 (the rate binding must survive the port to Midnight)
- Rationale: binding the limit into the leaf supports tiers without revealing a member's tier to relays.
- Verify: test with a membership whose limit is 10: credit index 9 is accepted and index 10 gets `Reject`.
- Status: open (DEC-ECO-1)

### MPE-ECO-017 Size-class credit weight
The Bus Node shall reject an Envelope of size class c unless its Admission Proof authorises P-ECO-3(c) distinct credit indices in that epoch.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; g3 (byte-denominated quota); g2 (class M = 16 credits); o2 R2 amendment 2
- Rationale: billing by bytes stops large classes from getting an unfair share of relay bandwidth and store capacity.
- Verify: test: a largest-class Envelope carrying one credit gets `Reject`; with P-ECO-3(c) credits it is accepted.
- Status: open (DEC-ECO-4)

### MPE-ECO-018 Content-bound Admission Proof
The Admission Proof shall bind its rate-limit share to the Envelope identifier, so that two Envelopes with different identifiers under one nullifier yield two distinct shares.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; g1 R2, s1 R2, s2 R2 (o2's `x = H(ephemeral_pk)` precomputation breaks accountability); `2022-vac-rln-v1-spec` ("Verification and slashing")
- Rationale: without content binding, an equivocator cannot be identified, so neither revocation nor slashing works.
- Verify: test: produce two Envelopes under one nullifier and recover the admission secret from their shares.
- Status: settled

### MPE-ECO-019 Duplicate nullifier, same Envelope
If an Envelope carries a nullifier already accepted with the same Envelope identifier, then the Bus Node shall return GossipSub `Ignore`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2 D3; g1 D1 (a duplicate is Ignore)
- Rationale: duplicates are normal in gossip and should not be penalised.
- Verify: test: deliver the same Envelope twice from two peers; neither peer's P₄ counter changes.
- Status: settled

### MPE-ECO-020 Equivocation detected
If an Envelope carries a nullifier already accepted with a different Envelope identifier, then the Bus Node shall return GossipSub `Reject` and record both Envelopes as equivocation evidence.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2, o1, o4; `2022-taheri-waku-rln-relay` §III
- Rationale: this is the double-signal that reveals the admission secret.
- Verify: test: send two conflicting Envelopes; the second gets `Reject` and the evidence store holds both.
- Status: settled

### MPE-ECO-021 Nullifier retention
The Bus Node shall retain each accepted nullifier for at least P-ECO-7 after acceptance.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; g3 D9 (a restart can replay until expiry); s3
- Rationale: a shorter cache lets a credit be spent twice inside the epoch tolerance.
- Verify: test: restart a Bus Node mid-epoch, then replay a conflicting Envelope; `Reject` is still returned.
- Status: settled

### MPE-ECO-022 Aggregate admission bound
While the Shard mesh is connected, MPE shall admit no more than M × L credits per epoch from M memberships with per-epoch limit L.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D4; o2 D4.5; g3 D9 (a split view can double-spend until convergence)
- Rationale: total load can never exceed the registered rate, which is the core spam bound.
- Verify: simulation with 16 Bus Nodes and 50 memberships each publishing 2L credits per epoch: delivered credits ≤ 50L per epoch.
- Status: settled

### MPE-ECO-023 Per-peer pre-verification limit
If a peer sends more than P-ECO-10 Envelopes per second, then the Bus Node shall drop the excess with GossipSub `Ignore` without verifying their Admission Proofs.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; g2 D4 (token bucket); g3 D9 (cap concurrent unverified proofs); s3 D4
- Rationale: this bounds the verification CPU any one neighbour can consume.
- Verify: test: a peer sends 2 × P-ECO-10 Envelopes/s; verifier invocations from that peer stay ≤ P-ECO-10 per second.
- Status: settled

### MPE-ECO-024 Stale Registry view
If the Bus Node's newest Registry membership root is older than P-ECO-5, then the Bus Node shall return `Ignore`, never `Reject`, for Envelopes it cannot validate against a known root.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; g1 D1 (stop validating rather than punish peers when the local view is stale)
- Rationale: a lagging Ledger Adapter must not cause honest peers to be penalised.
- Verify: test: freeze the mocked Ledger Adapter for P-ECO-5 + 60 s; no peer's P₄ counter increases.
- Status: settled

### MPE-ECO-025 Continuity when Registry calls are paused
While Midnight rejects `send_mn_transaction` calls, the Bus Node shall continue to accept Envelopes whose membership roots remain inside P-ECO-5.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D4; o1 R2 (safe mode stops new memberships); g1 D7; `midnight-node/runtime/src/check_call_filter.rs:40-45`
- Rationale: a governance pause should stop enrolment, not delivery from members already admitted.
- Verify: test with a mocked Ledger Adapter that rejects submissions: existing members still publish until their roots age out.
- Status: settled

### MPE-ECO-026 Membership expiry
When a membership period of P-ECO-4 ends, the Registry shall exclude memberships registered for that period from every subsequently published root.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D4; o1 (14-day period bounds tree history); g3 (daily); notes §7.5 (no rent)
- Rationale: expiry bounds both the anonymity-set churn and the Registry state that has to be kept live.
- Verify: test on a devnet: after the period ends, a proof against the new root fails for an expired member.
- Status: open (DEC-ECO-5)

### MPE-ECO-027 Root publication time recorded
The Registry shall record, for each membership root it publishes, the block time of publication.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; o1 R2 amendment (`Map<root, epoch>`); g1 R2
- Rationale: `HistoricMerkleTree.checkRoot` accepts any prior root, so Bus Nodes need the publication time to enforce P-ECO-5.
- Verify: inspection of Registry state after 3 root updates; each root maps to a block time.
- Status: settled

### MPE-ECO-028 Revocation on evidence
When the Registry receives a proof of knowledge of an admission secret whose commitment is a current member, the Registry shall mark that membership revoked.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D4; o1 (`revoke(sk)`); s3 (revoke equivocators from future snapshots); o2 R2 amendment 3
- Rationale: revocation makes equivocation cost a membership even where no bond exists.
- Verify: test: submit a recovered secret; the membership's revoked flag is set in Registry state.
- Status: open (DEC-ECO-2)

### MPE-ECO-029 Revocation takes effect
When a membership is revoked, the Registry shall exclude it from every membership root published after the revocation.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D4; o1, s3; g1 R2
- Rationale: together with ECO-015, revocation takes effect at every Bus Node within P-ECO-5.
- Verify: test: after revocation plus P-ECO-5, an Envelope from the revoked member gets `Ignore` at every Bus Node.
- Status: settled

### MPE-ECO-030 No per-Envelope ledger state
The Registry shall not write any per-Envelope nullifier or per-Envelope identifier into ledger state.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; g3 D6 (an on-chain nullifier set grows about 1.7 GB/year); o2 R2; notes §7.5 (no rent; persistent bytes cost 20× transmitted bytes)
- Rationale: persistent ledger state is permanent and unrefundable, so it must stay bounded.
- Verify: inspection of the Registry contract's state declarations.
- Status: settled

### MPE-ECO-031 Equivocation evidence retention
The Bus Node shall retain each recorded equivocation evidence pair for at least P-ECO-14.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D4; o2 (withdrawal delay longer than the evidence window); o4
- Rationale: revocation or slashing filed late still needs the evidence.
- Verify: test: evidence remains retrievable through the Bus Node interface after P-ECO-14 − 1 s.
- Status: settled

### MPE-ECO-032 Bond custody
Where membership bonds are enabled, the Registry shall hold each bond in NIGHT until P-ECO-14 after its holder requests withdrawal.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D4; o2, o4; `midnight-ledger/ledger/tests/token_vault_unshielded.rs:70,364`; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1203,1211,1241`
- Rationale: the delay blocks Taheri's escape-by-withdrawal (`2022-taheri-waku-rln-relay` txt L498-503).
- Verify: Quint model invariant "no withdrawal before the delay"; devnet test of a withdrawal at delay − 1 block (fails) and + 1 block (succeeds).
- Status: open (DEC-ECO-2)

### MPE-ECO-033 Slash split
Where membership bonds are enabled, when the Registry accepts slash evidence for a bonded membership, the Registry shall pay at most P-ECO-15 of the bond to the reporter.
- Pattern: complex
- Scope: PROD
- Priority: MAY
- Source: D4; o2 R2 amendment 1; o4 (remainder to the pool)
- Rationale: a 50% reporter share let the equivocator self-report and recover half its bond.
- Verify: test: an equivocator self-reports and recovers ≤ P-ECO-15 of the bond.
- Status: open (DEC-ECO-2)

### MPE-ECO-034 Registry funds invariant
Where membership bonds or a treasury are enabled, the Registry shall hold NIGHT equal to outstanding bonds plus the treasury balance plus challenge escrow.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D4; o2 D10 (Quint invariants)
- Rationale: it is the solvency check anyone can read from contract state.
- Verify: Quint model check over bond, slash, withdraw, challenge and payout actions; balance comparison on devnet after each action.
- Status: settled

### MPE-ECO-035 Maintainer cannot move bonds
The Registry shall move bonded NIGHT only through its coded slash, withdraw and payout circuits.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; o2 D7 (the maintainer sets parameters only); o4 (powers excluded by construction)
- Rationale: limits what a compromised maintenance key can take.
- Verify: inspection of every Registry circuit that calls `sendUnshielded`; a test that a maintenance-authority call cannot transfer funds.
- Status: settled

### MPE-ECO-036 Registration publicity disclosed
Where a membership requires an unshielded NIGHT deposit, the MPE client library shall tell the user, before submission, that the funding address becomes publicly linked to a membership registration.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D4; o4 D4 (the depositing address is public); o2 R2 (name "registration is public" as a leak); notes §3.4
- Rationale: honest scope: the registration is visible even though Envelopes are not linked to it.
- Verify: demonstration: the registration flow shows the notice and requires confirmation.
- Status: settled

### MPE-ECO-037 No protocol pay for relaying
The Registry shall not pay any Operator for forwarding Envelopes.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; g1, g2, g3, o1, o2 (relays unpaid); `2024-cornelius-waku-network-dapps` txt L134 (relaying has inherent value); s1, s2, s4 (pay relays off-protocol by contract); o4 dissents (relay pool)
- Rationale: relay quality cannot be checked by a contract, and paid relay scores have been gamed.
- Verify: inspection of Registry payout circuits.
- Status: open (DEC-ECO-3)

### MPE-ECO-038 No performance-score payouts
The Registry shall not base any payout on a measured relay or uptime performance score.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D4; o2 D4.4; `2026-cao-nymreputation` txt L150 (score attacks cut the cost of dominating the active set by over 99%); o4 proposes multi-monitor probe scores
- Rationale: only work a contract can check is paid.
- Verify: inspection of payout circuit inputs; none is a score.
- Status: open (DEC-ECO-3)

### MPE-ECO-039 Treasury runway cap
Where a Registry treasury is enabled, the Registry shall pay out no more per day than the treasury balance divided by P-ECO-16.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D4; o2 D4.2
- Rationale: at least one year of runway stays visible on chain at all times.
- Verify: Quint invariant; devnet test that a payout above the cap fails.
- Status: open (DEC-ECO-3)

### MPE-ECO-040 Per-key saturation cap
Where a Registry treasury is enabled, the Registry shall pay any single bond key no more than the reward pool for that period divided by P-ECO-17.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D4; o2, o4; `2021-diaz-nym`; key splitting is a residual risk (`2026-cao-nymreputation` Appendix D)
- Rationale: limits how far one bond key can concentrate rewards. It does not limit concentration by one real-world entity.
- Verify: Quint invariant "payout per key ≤ pool ÷ k".
- Status: open (DEC-ECO-3)

### MPE-ECO-041 Store Node retention challenge
Where Store Node bonding is enabled, when the Registry records a challenge for an anchored Envelope inside its retention window, the Store Node shall submit that Envelope and its Merkle path within P-ECO-18.
- Pattern: complex
- Scope: PROD
- Priority: MAY
- Source: D4; o2 D4.4, R2 D6; `exports.md:1266` (`blockTimeLt`)
- Rationale: this is the only proposed mechanism that turns a storage promise into something a contract can enforce.
- Verify: devnet test: a challenge is issued and answered before the deadline.
- Status: open (DEC-ECO-3)

### MPE-ECO-042 Missed challenge forfeits bond
Where Store Node bonding is enabled, if a challenged Store Node misses the P-ECO-18 deadline, then the Registry shall transfer the forfeited bond share to the challenger and the treasury.
- Pattern: complex
- Scope: PROD
- Priority: MAY
- Source: D4; o2 D4.4
- Rationale: without a penalty a store has no reason to keep data it does not need itself (o2 R2 D6).
- Verify: devnet test: an unanswered challenge produces the transfer after the deadline.
- Status: open (DEC-ECO-3)

### MPE-ECO-043 Unlinkable paid back-fill
Where a Store Node charges for back-fill, the Store Node shall accept payment tokens that carry no Subscriber account identifier.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D4; o2 (ACT credits, `2026-draft-act`); o1 (Privacy Pass, `2024-rfc9576-privacypass-arch`); s4 (accounts disclose participation)
- Rationale: payment must not link a Subscriber's identity to the Shard it reads.
- Verify: inspection of the redemption message format: no persistent client identifier is present.
- Status: open (DEC-ECO-3)

### MPE-ECO-044 Overload refuses new Envelopes
If accepting an Envelope would exceed the Bus Node's configured ingress or storage cap, then the Bus Node shall refuse that Envelope with GossipSub `Ignore` instead of evicting an unexpired accepted Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; g1 D4 (refusal is visible; silent early pruning is not allowed); s2 (reject excess explicitly)
- Rationale: overload should show up as refusals, not as silent loss of Envelopes already admitted.
- Verify: test: fill the store cap, then inject one more; the stored set is unchanged and the new Envelope gets `Ignore`.
- Status: settled

### MPE-ECO-045 Shed the largest class first
While the Bus Node's ingress exceeds its configured cap, the Bus Node shall refuse Envelopes of the largest size class before refusing any smaller class.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: D4; o2 D4.5
- Rationale: refusing large Envelopes first keeps the most messages flowing for each byte refused.
- Verify: simulation at 2× the cap with a mixed class load: the refusal ratio for the largest class is ≥ that of every smaller class.
- Status: settled

### MPE-ECO-046 Cover Envelopes are admitted normally
Where an Operator emits cover Envelopes, the Bus Node shall apply the same Admission Proof and credit checks to them as to any other Envelope.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D4; o1 (cover needs valid RLN proofs), o2 (treasury-held memberships), s3 (subsidised cover); g3, g4 (no cover until priced)
- Rationale: cover must not open a free admission path. No timing-privacy claim follows from it.
- Verify: test: a cover Envelope without credits gets `Reject`.
- Status: open (DEC-ECO-7)

### MPE-ECO-047 Prototype admission over a mocked ledger
The Prototype shall run ECO-012 through ECO-024 against a mocked Ledger Adapter that supplies membership roots, root publication times and revocations.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; BRIEF glossary (Ledger Adapter, mockable); o2 D10; g1 D10
- Rationale: the admission logic can be tested before any Registry exists on ledger 9.
- Verify: demonstration: the conformance suite passes with the mock adapter.
- Status: settled

### MPE-ECO-048 Admission-proof measurement gate
The Prototype shall report the Admission Proof size in bytes and its verification time on one core of a 4-vCPU VM, and fail its gate if either exceeds P-ECO-11 or P-ECO-12.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; o2 R2 ("the one fact"); o1 (proof size P **unknown**); g2 (threshold)
- Rationale: this one number decides between DEC-ECO-1 options and sets relay CPU.
- Verify: test: a benchmark harness over 10,000 proofs reports median and p99 verify time and the proof length.
- Status: settled

### MPE-ECO-049 Registration-cost gate
MPE shall not enter production until a measured devnet registration transaction is within P-ECO-13.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D4; g3 D10; o2 R2 (6 KB was an underestimate; 2,912 B + 4,832 B = 7,744 B of proofs alone); notes §6.2
- Rationale: every DUST figure in the proposals is a genesis-price inference.
- Verify: demonstration: submit 10 registrations on devnet and record bytes and DUST from the block's `ledgerParameters`.
- Status: settled

### MPE-ECO-050 Flood-cost analysis published
MPE shall publish, before production, the NIGHT holding needed to fill one Shard at its D5 cap for 24 h, computed from the ECO-049 measurement.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D4; g3 (about 770 NIGHT at genesis prices, an **inference**); o3 R2 and s4 R2 (g4's figure was off by about 7× because it used capacity instead of generation)
- Rationale: the spam price has to be stated as a number, not assumed adequate.
- Verify: analysis: an independent reviewer recomputes it from the published inputs using 0.714 DUST/NIGHT/day.
- Status: settled

## 4. Decisions

**DEC-ECO-1: Admission instrument.**
- Options:
  - (a) A DUST-paid Registry membership plus a per-Envelope anonymous proof of a per-epoch nullifier quota, RLN-style (o1, g3, s3, o2, o4).
  - (b) DUST-bought single-use on-chain tickets (g1; o4's R2 vote).
  - (c) A visible member key with a signature and credit counter (g2).
  - (d) Issuer-signed permits or publicly verifiable blind-RSA stamps (s1, s4; s2; g2's R2 vote).
  - (e) A DUST fee per Event on the ledger (g4; o3 Lane A; o3's R2 vote).
- **Recommended default: (a).** It needs no issuer holding a customer-to-Event map (o4 R2), writes nothing per Envelope to the chain, and puts no linkable key on each Envelope (o2 R2 on g2). Option (b) is unlinkable only at one ticket per transaction, which is about 2 tickets/s at a 10% block share (o1 R2). Option (e) caps the whole chain at roughly 21 calls/s.
- **Fallback:** option (d) with s2's 354-byte object-bound stamp, if ECO-048 fails (o1 R2 amendment).
- **Settling check:** ECO-048. In addition, an off-chain verifier for a Compact-circuit proof must be shown to work. o1 marks that as **unknown**.

**DEC-ECO-2: Deterrent beyond registration cost.**
- Options:
  - (a) None (g2, g3).
  - (b) Revocation from future roots (o1, s3).
  - (c) A NIGHT bond with slashing (o2, o4; o3 Lane B).
- **Recommended default: (b) for the Prototype and launch, with (c) as an optional PROD feature.** Deployed Waku dropped the deposit (`2024-revuelta-waku-latency` txt L178, L218). A contract can hold and release NIGHT (`token_vault_unshielded.rs:70,364`), but mainnet enablement is **unknown**.
- **Settling check for (c):**
  - mainnet support for NIGHT held by a contract;
  - ECO-018 demonstrated;
  - the Quint invariants of ECO-032 to ECO-034;
  - a sponsor-market test (o2 R2: a locked bond forgoes DUST generation).

**DEC-ECO-3: Operator funding.**
- Options:
  - (a) Nobody is paid by the protocol (g1, g2, g3, g4, o3).
  - (b) Off-protocol contracts for relays, gateways and issuers (s1, s2, s3, s4).
  - (c) A Registry treasury fed by non-refundable fees and slashes that pays only for checkable work: anchors and passed retention challenges (o2).
  - (d) A pool paid on multi-monitor probe scores (o4).
- **Recommended default:** relays are never paid by the protocol. Launch operators are grant-funded outside the protocol (o1, o2, o4). PROD adds (c).
- **Reason:** only (c) gives the "open participation" end state an income mechanism (o2 R2). Option (d) pays scores, and scores have been gamed (`2026-cao-nymreputation`).
- **Settling check:** the o2 economic simulation (treasury runway ≥ 12 months with no grant draw), plus operator cost bids (s1).

**DEC-ECO-4: Quota unit.**
- Options:
  - (a) Envelope count (o1, o4, s3).
  - (b) Bytes, through size-class weights (g3, g2, o2 amended).
- **Recommended default: (b).** Padded classes make bytes a known quantity per class, and that is what both relay bandwidth and storage are priced in.
- **Settling check:** a simulation of the class mix at P-ECO-2. Weight (b) should keep per-membership bandwidth within 2× across class mixes.

**DEC-ECO-5: Epoch and membership period.**
- Options for the epoch: 30 s (s3), 60 s (o1, o2, o4), 600 s (g1), 3,600 s (g2).
- Options for the membership period: 1 h (g2), 24 h (g3), 14 d (o1), 30 d (o2).
- **Recommended default: a 60 s epoch and a 24 h period.**
- **Trade-off:**
  - Hourly renewal costs about 2.4 DUST/day, against 0.1 DUST/day for daily renewal (g3).
  - A longer period survives a safe-mode pause longer (o1 R2) but slows expiry.
- **Settling check:** ECO-049 cost, plus a measured safe-mode duration distribution (**unknown**).

**DEC-ECO-6: Chain-share budget.**
- Options: 10% (g1, g3) or 5% (g4).
- **Recommended default:** 10%, enforced only through client behaviour (ECO-010).
- **Settling check:** ECO-011 measured on testnet at the D5 load.

**DEC-ECO-7: Low-load cover.**
- Options:
  - (a) An operator-funded floor: 0.5 Envelopes/s per bucket (o1), 1 Event/s per Shard (o2), or a subsidy (s3).
  - (b) None (g1, g3, g4).
- **Recommended default: (b) for the Prototype.** Cover is an optional PROD feature (ECO-046) with no privacy claim attached.
- **Settling check:** a priced cover design inside the D5 bandwidth budget (g3, o2's change trigger).

## 5. Cross-area dependencies

| Area | Requirement I expect (ID assigned at merge) |
|---|---|
| D1 format | An Envelope field set carrying an epoch, a root reference, nullifier(s), a share and an Admission Proof of fixed length ≤ P-ECO-11. The Envelope identifier is computed without the proof (s3, o2 R2). |
| D2 privacy | A leakage table entry: "registration is public"; issuer timing leaks if DEC-ECO-1 falls back to (d). |
| D5 performance | A per-Shard cap (events/s and bytes/s) that ECO-050 prices. Bus Node ingress and CPU caps referenced by ECO-044 and ECO-045. The p99 target under flood. |
| D6 storage | Retention windows that bound ECO-041. Anchor cadence and ring size (an anchor costs about 0.08 DUST at genesis prices). |
| D7 actors | The launch operator set and its funding source. Who holds the Registry maintenance key, and the timelock on changes to P-ECO-2, P-ECO-8 and P-ECO-15 to P-ECO-17. |
| D8 tether | A Ledger Adapter interface exposing roots, root times, revocations, `ledgerParameters` and submission status (ECO-008, ECO-024, ECO-025, ECO-047). |
| D9 threats | Threat entries for split-view double-spend, multi-registration Sybil, bond-key splitting, challenge griefing and DUST price spikes (o2 R2). |
| D10 plan | Phase gates that consume ECO-048, ECO-049 and the DEC-ECO-3 simulation. |

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Membership | A Registry entry, holding a commitment to an admission secret and a committed per-epoch limit, that authorises publishing for one membership period |
| Admission secret | A dedicated secret behind a Membership; revealed by equivocation |
| Epoch | An admission time slot of P-ECO-1 |
| Credit | One unit of per-epoch quota; an Envelope consumes P-ECO-3(c) credits |
| Nullifier | A per-(membership, epoch, credit index) value that is public on the Envelope and unlinkable to the Membership |
| Equivocation | Two Envelopes with different identifiers under one nullifier |
| Membership root | A Registry root over current Memberships, with its publication time |
| Bond | Optional NIGHT held by the Registry against a Membership or Store Node |
| Treasury | Optional Registry-held NIGHT balance that pays for checkable work |
| Sponsor | A party that pays registration for someone else's Membership |

## 7. Gaps

- **Operators' willingness to run unpaid relays** cannot be tested before launch. Every proposal assumes it, and o2 R2 notes that no pre-mainnet exit test exists for any funding model.
- **Multi-registration Sybil.** A funded attacker can buy M memberships. This is priced (ECO-050), not prevented (`2022-taheri-waku-rln-relay` txt L488).
- **Live DUST prices** are not in the repositories (notes §7.2). Every per-Event and per-anchor DUST figure is a genesis-price **inference**. That fees are burned is also an **inference** (notes §2.3).
- **Mainnet enablement of contract-held NIGHT** is **unknown**. It is shown only in a ledger test.
- **Off-chain verification of a Compact-circuit proof by relays** is **unknown** (o1).
- **Read-side funding.** No mechanism pays indexer or gateway egress, which grows with the number of Subscribers (o3 R2, s4). I could not write a testable requirement for it.
- **Cross-partition equivocation** is detected only if some Bus Node sees both Envelopes (o2 D9). ECO-022 holds only while the mesh is connected.
- **Bond-key splitting** defeats ECO-040 for real-world entities (`2026-cao-nymreputation` Appendix D). No per-entity check is possible.
