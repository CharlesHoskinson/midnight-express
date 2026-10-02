# Round 2 cross-review: o4 (governance, compliance and operations)

**Reviewed:** g4-skeptic-minimalist, g1-protocol-architect, s4-evidence-auditor, s1-privacy-theorist. I also re-read my own Round 1 proposal (o4).

**How I checked evidence.** I opened the cited code under `/home/charl/midnight/` and the plain texts under `graph/text/`.
- "Supported" means I read the cited lines and they say what the proposal claims.
- "Not opened" means I did not check that citation.

**Generation note that affects every proposal.** The local `midnight-ledger` working tree does not contain the 1 KiB silent-drop constant.
- Its `onchain-vm/src/vm.rs:37-38` has only `MAX_LOG_SIZE = 1 << 19`.
- Its `process_log` (`result_mode.rs:60-62`) keeps every log.
- The 1 KiB drop that g1, s4 and s1 cite comes from the tag `ledger-9.1.0.0-rc.5` / rev `54a4e013`. I could not open that tag here; the readout (`notes/midnight-network-stack.md:218`) records it.
- No design depends on this limit, because `Misc` is 288 bytes in every proposal. Still, any statement about it must name the tag.

---

## D1 Event format

**(a) Positions**
- **g4:** one ledger `Misc` event: a constant 32-byte `name` plus a 256-byte ChaCha20-Poly1305 payload (205-byte body). No expiry field. 14-day indexer retention.
- **g1:** one `EVENT` object with a fixed 192-byte little-endian header and 4 size classes (448–16,576 B on the wire). Lifetime is capped per class, from 3,600 s down to 300 s. Ticket nullifier and one-time Ed25519 `pub_pk` are visible. No extension bits; a new version means a new protocol id.
- **s4:** a fixed 2,048-byte record: 128-byte header, 128-byte issuer permit, sealed body. 48 h retention. Up to 16 fragments.
- **s1:** a fixed 4,096-byte cell with up to 2,048 application bytes. 16 cells per event at most. The whole MLS packet is sealed. 48 h expiry.

**(b) Evidence**
- **g4.** These citations are supported:
  - `Misc` is 32 + 256 bytes (`minokawa-compact/compiler/midnight-events.ss:71-74`).
  - `emit` accepts only standard event types and is forbidden in the constructor (`compact-reference.mdx:3497-3507`).
  - CoIP-0003 defers private events (`coip-0003.md:107-109`).
  - `global_ttl = 1209600` (`ledger-parameters-config.json:176`).
  - The node's `TransactionAppliedStateRoot` carries no logs (`ledger/src/ledger_9/mod.rs:460-470`).

  **Not supported:** "After that [14 days] the event is gone." The payload is part of the transaction transcript. Archive nodes run `--pruning archive` and serve explorers (`notes/midnight-network-stack.md:148`, citing `full-node.mdx:163-175`). Anyone can re-derive the events by re-executing those blocks. The indexer re-executes in exactly this way (`midnight-indexer/docs/architecture.md:15-17`). So the ciphertext is permanent public data. That is **inference** from those two facts, and it is the operational fact that matters most for D1.
- **g1.** Supported:
  - The yamux default credit is 256 KiB (`rust-yamux/yamux/src/lib.rs:45`).
  - `transaction_byte_limit` is 1,048,576 (`ledger-parameters-config.json:152`).

  Not opened: `hash.rs` at the ledger-9 tag. The vm.rs line numbers at the tag cannot be checked locally (see the generation note).
- **s4 / s1.** The `Misc` size and the MLS header-exposure citations match the Compact source. I did not open RFC 9420, `2001-bellare-keyprivacy` or `2022-grubbs-anonrobustpq`.

**(c) Vote: g1's layout, with two amendments.**
1. Add a 32-byte franking commitment inside the sealed prefix. Relays never see it. It is what makes recipient-initiated abuse reports verifiable (`2017-grubbs-franking`; o4 D1).
2. Raise the class-0 and class-1 `TTL_MAX` to at least 24 h, so that a wallet offline overnight can back-fill.

g1 has the strictest parser rules: one legal layout, reject on non-zero reserved fields, and no type dispatch. That is the right answer to the Bitmessage CVE-2018-1000070 lesson (`bitmessage-guide.md:352-358`).

**(d) Strongest objection to g1.** A maximum lifetime of 3,600 s on the smallest class makes "at-least-once" an empty promise for any consumer that is not always online. It pushes users to always-on hosted agents, and those agents see interests. g1 itself concedes that "a phone ... does not get topic privacy" (D3).

---

## D2 Definition of "private"

**(a) Positions**
- **g4:** content confidentiality, topic privacy, payload integrity, and chain-level publisher unlinkability. No forward secrecy (FS), no volume privacy, no GPA (global passive adversary) protection.
- **g1:** content confidentiality, sealed parties against relays, interest privacy at topic granularity, and ticket binding. Explicit non-claims: no FS, no GPA protection, no stem theorem, and known `enc_pk` values can be tested.
- **s4:** content confidentiality, complete-stream interest privacy, topic-label confidentiality, and limited record unlinkability. No publisher, timing or relationship privacy.
- **s1:** game-based definitions over adversaries R, C, G, A and I. Content and conditional interest privacy are claimed. Publisher unlinkability and timing privacy are explicitly not provided.

**(b) Evidence**
- **s1.** Guerraoui Theorem 5, ε ≥ ln(f−1) for any gossip protocol, is supported (`2023-guerraoui-inherent-anonymity-gossiping` txt L589-592, L611-614). This is the strongest citation in the four proposals. It shows that no mesh claim in any of them can be worst-case anonymous.
- **g1.** The Dandelion++ claim is supported with a nuance. Theorem 1 gives D_OPT ≤ 8·D_FS + 6p² + O(p³), and p² is a lower bound for any scheme (`2018-fanti-dandelionpp` txt L631-637). g1's Phase 1 gate of 2·p² is its own threshold, as it says. The paper's bound depends on an unknown random 4-regular graph, which g1 does not build. So the gate is a measurement target, not a theorem, and g1 says so.
- **g4.** The "chain-level publisher unlinkability" claim is only partly supported. The DUST spend hides the note. However, a public Registration Table links NIGHT keys to DUST keys (`midnight-docs/docs/concepts/dust-architecture.mdx:136, 203`). The payer's anonymity set is therefore the set of registered DUST holders. At low volume it is "one bus transaction per block", which g4 concedes.

**(c) Vote: s1's game-based definitions as the specification text**, with these additions:
- g1's extra leakage rows: stem predecessor, and holder of a candidate key.
- My P7 (report-only disclosure) and P8 (operator content-blindness) as named properties. The governance model depends on them: an operator who cannot read content cannot be compelled to scan it.

**(d) Strongest objection to s1.** Subscriber-interest privacy holds only while "fetching/error behavior remains independent of recognition". Every useful action depends on recognition: an abuse report, an application reply, a contract `note`. So for any user who acts, the property collapses. The leakage contract must list those actions explicitly, or the claim will be read as broader than it is.

---

## D3 Publish and subscribe

**(a) Positions**
- **g4:** one bus contract. Subscribers stream that contract's `contractEvents` and trial-decrypt everything. Contracts do not consume events.
- **g1:** a single-shard flood with trial-open. Contracts consume through a later `note(commitment)` call. The wallet gets events from a local agent over localhost.
- **s4:** secret invitations, complete-stream retrieval, local dispatch, and a follow-up transaction for contracts. MLS groups of up to 100.
- **s1:** capability invitations and a fixed 1-second fetch cadence. Every minute, a full inventory repair against a second operator. Explicit transaction for contracts. MLS groups of up to 32. No unsolicited first contact.

**(b) Evidence**
- `contractEvents` requires `contractAddress`, and `fieldPrefixes` apply to standard events only (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:548-562`). The subscription is inclusive and `@beta` (`:1967-1971`). Supported for g4, s4 and s1.
- The shielded wallet's global-stream-plus-local-decrypt pattern is supported:
  - g4's citation `Sync.ts:220-229` is the inclusive resume cursor.
  - s1's citations `:243, :266, :295` are backpressure, `WalletSyncUpdate.create(data, secretKeys)` and apply.
- g1's statement that "the indexer serves finalized blocks only" agrees with `architecture.md:15`.

**(c) Vote: g1, plus s1's fixed fetch cadence and second-source inventory repair.** All five proposals, mine included, already agree on the core: no topic filter at infrastructure, local trial decryption, and contracts consume only through a follow-up transaction.

**(d) Strongest objection to g1.** Anyone who knows an `enc_pk` can send a unicast object for the price of a ticket. Nothing on the recipient side gates first contact. That is the harassment vector that gets a messaging system shut down. g1 needs one of the following:
- an intro tier with a stricter rate limit plus recipient consent lists (`2023-xmtp-xip42-consent`; o4 D3, D7); or
- s1's rule: no unsolicited contact in v1.

---

## D4 Sustainable model

**(a) Positions**
- **g4:** the publisher pays a DUST fee per event. No relay payment, no PoW, no RLN. A "design cap" of min(4 events, 5% of blockUsage) per block.
- **g1:** a DUST-paid admit transaction mints up to 30 single-use tickets per member per 10-minute epoch. Relays are unpaid. Admit calls are budgeted at 10% of block usage. No slashing.
- **s4:** issuer-signed single-use permits, sold commercially. Publisher anonymity toward the issuer is given up on purpose. Operators are paid under contract.
- **s1:** the same as s4, plus sponsor-funded idle capacity and subscriber egress plans.

**(b) Evidence**
- DUST is non-transferable (`dust-architecture.mdx:23`). Supported.
- s1's block reward `(0, None)` is supported (`midnight-node/runtime/src/lib.rs:680-695`, both feature arms).
- s4's arithmetic of 5 DUST/NIGHT and 8,267 per second is supported (`ledger-parameters-config.json:165-166`).
- Schaub "halves the harm" is supported (`2015-schaub-bitmessage-antispam` txt L33, L103, L570-571), as g4 and g1 report it.
- RLN verification ≈ 30 ms and proving ≈ 0.5 s on an iPhone 8 are supported (`2022-taheri-waku-rln-relay` txt L429-430).
- **g1's "Slashing does not fit DUST"** is correct for DUST only. Compact contracts can hold tokens through `receiveUnshielded` and `receiveShielded` (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:1046, 1092`). So a slashable NIGHT deposit, as in my RLN design, is not ruled out by this fact.
- **g4's cap is not a mechanism.** Its `publish` circuit "writes no ledger cell" (D1), so no contract state can count events per block. The "4 per block / 5%" figure is a budget, not an enforced limit. The only brake is the chain-wide fee update.

**(c) Vote: g1's DUST-bought single-use tickets for launch admission**, combined with my operator-funding path: grants first, then a pool funded by a non-refundable membership fee and the slash remainder, paid on multi-monitor probe scores. Tickets are anonymous toward any issuer and use the nullifier pattern that Midnight already has. s4 and s1 make the issuer a party that can link customers to events, and so a party that can be subpoenaed. From the compliance side, that is the worst place to put an identity map.

**(d) Strongest objection to g1.** "Relays are not paid by the protocol" makes availability depend on goodwill. It also leaves no money for the actors who carry legal exposure. Admission is per `admit_sk`, so a flooder who registers k keys gets 30·k tickets per epoch. The quota limits only how fast tickets are bought, not who buys them.

---

## D5 Performance

**(a) Positions**
- **g4:** at most 4 events per block (40/min). 56 MiB/day per subscriber. p50 ≤ 60 s as a gate.
- **g1:** 50 objects/s per shard, mean 848.6 B. Relay mesh ≈ 2.2 Mbit/s. Hot-path p99 ≤ 10 s.
- **s4:** 10/s sustained, 100/s burst, 10,000 consumers. 82.9 Mbit/s out per relay. 1.769 GB/day per consumer.
- **s1:** 10 cells/s planning load, 100/s capacity, 1,000 consumers. 3.54 GB/day per consumer.

**(b) Evidence**
- s4's Loopix setup (6 mixes, 4 providers, 500 clients, mean latency 1.93 s) is supported (`2017-piotrowska-loopix` txt L1029-1033, L1142-1144).
- OMR at 0.065 s/msg, about $1 per million messages *per recipient served*, is supported (`2021-liu-omr` txt L315, L3601). g1 and s4 both read it correctly.
- UnifOMR at about 25 s and 4 MB for 2¹⁹ messages of 612 B is supported (`2026-fisch-unifomr` txt L38-39).
- **g1 misapplies one number.** It uses `signature_verify_constant: 97304512` (`ledger-parameters-config.json:124`) as relay CPU time. That number is a ledger cost-model weight for in-VM verification, not a native Ed25519 benchmark. The relay CPU budget therefore remains **unknown**.
- The slot of 6,000 ms and the 1 MiB block length at a 75% normal ratio are supported (`runtime/src/lib.rs:292, 300, 312-313`).

**Arithmetic nobody stated.** g1's full-shard edge stream is 50 × 848.6 B ≈ 42.4 kB/s, which is about **3.67 GB/day** per full subscriber. That is in the same range as s1 (3.54 GB/day) and s4 (1.77 GB/day). Every overlay design costs a full subscriber gigabytes per day. g4 costs 56 MiB/day only because its throughput is about 0.67 events/s. The real trade-off is privacy-preserving full download against throughput, not ledger against overlay.

**(c) Vote: g1's mesh sizing and s4's consumer-egress accounting**, which s4 states honestly as the binding cost.

**(d) Strongest objection.** At about 3.7 GB/day, no phone receives the full stream. "Private wallet" then means "a user-hosted agent" or "a provider that sees interests". The second option creates a regulated intermediary with interest logs. No overlay proposal states that consequence.

---

## D6 Storage

**(a) Positions**
- **g4:** ciphertext stays in transaction logs (churn), with a 14-day indexer policy. Contract state stays empty.
- **g1:** each relay keeps objects until expiry (≤ 1 h) with a 2 GiB cap and refuses new objects past the cap. Optional 7-day archive.
- **s4:** every relay keeps 48 h (3.3 GiB at 10/s). Three retention receipts are required before an event counts as durably accepted. Archive is bought separately.
- **s1:** every relay keeps 48 h (70.8 GB at 100/s). 7-day archive. Three receipts.

**(b) Evidence**
- Log churn is supported in the local tree: `vm.rs:553-561` charges `bytes_written` and `bytes_deleted` equally ("count the entire log as churn"). This backs s4's correction of MIP-0002's 703 MB/day bound. I did not open MIP-0002:520.
- The indexer's `ledger_state_retention: 1000` concerns loadable ledger states (`chain-indexer/config.yaml:14-16`). Supported, as s4 says.
- g4's "14-day indexer policy" proposes a new policy. No current pruning of `contractEvents` rows was found, and archive nodes keep the blocks anyway (see D1).

**(c) Vote: s4.** It keeps 48 h, needs three independent receipts, and states that archives give no deletion guarantee. That is close to my own position (24 h by default, 7 days at most) and gives a clear upper limit on legal exposure.

**(d) Strongest objection to s4.** Every relay holds all ciphertext, so every operator in every jurisdiction faces the same takedown demand for the same object. The design needs a defined, auditable delete-by-ID path: o4's signed tombstone, a 48 h SLA, and canary-measured compliance. Without it, a court order goes to all 20 operators at once and no one can show they complied.

---

## D7 Infrastructure actors (I lead)

**(a) Positions**
- **g4:** no new role. Validators, existing indexers and local scanners only.
- **g1:** 8–16 permissioned relay operators on an allow-list in the admit contract. The allow-list changes through Root via Council and Technical Committee (TC). Relays are unpaid. The allow-list is removed only after a failed Phase 3 red-team.
- **s4:** paid independent relays, gateways, issuers and anchor submitters. 20 relays from at least 5 operators. Decentralization by conformance suites.
- **s1:** 16 relays from at least 8 organizations, several issuers and 2 archives. Ledger-governed issuer admission as the end state.

**(b) Evidence**
- g1's claim that validators do not serve ledger-sync by default because it competes with authoring is supported (`midnight-node/node/src/service.rs:610-620`).
- g1's "block author is predictable under Aura" depends on the generation. The tree contains `pallet_aura`, `pallet_babe` and an Aura→BABE migration (`runtime/src/lib.rs:380, 393-396`; `node/src/service.rs:16`).
- Safe mode and tx-pause gate all calls (`BaseCallFilter = InsideBoth<SafeMode, TxPause>`, `runtime/src/lib.rs:321`). Forced safe mode lasts 7 days (`:758`). Supported. g4 and g1 both note this pause risk.
- s1's genesis D-parameter citation agrees with the others.

**What none of the four has.** None defines any of the following:
- who receives abuse reports or legal process;
- who can eject a misbehaving relay, and how fast;
- what an operator must log or must not log;
- how keys and circuits are rotated;
- how incidents are classified and handled.

g1 puts the allow-list under Root through Council and TC. Federated governance motions take days (`runtime/src/lib.rs:907-943`, as cited in o4). A relay found injecting malformed objects, or under a court order, cannot be removed in hours.

**(c) Vote: my own alternative (o4 D7), amended.**
- Keep a bus-specific steward set. Every power is time-locked. Emergency actions expire after 7 days unless ratified, mirroring `SafeModeForceDuration`.
- Some powers are excluded by construction: no content access, no de-anonymization, no membership revocation by fiat, no blocking of withdrawals.
- Adopt g1's rule that the allow-list is removed only after a failed red-team, in place of my calendar phase.
- Adopt s1's minimum operator diversity (at least 8 organizations).
- The end state hands the maintenance authority to Council and TC, which is g1's governance path, or ossifies the contract.

**(d) Strongest objection, aimed at my own position.** A 7-seat steward multisig is a new, identifiable body, and courts and regulators can compel it. The tombstone desk makes the stewards the obvious target of every takedown request. The amendment I accept: tombstones bind only operators who signed the Operator Agreement, and stewards publish every tombstone in the transparency report. g4's rival answer is "no new role, so nobody to compel". It holds only because g4 puts permanent, undeletable ciphertext on a public ledger.

---

## D8 Network tether

**(a) Positions**
- **g4:** ledger and indexer only; fallback is a private indexer. No overlay, ever, in v1.
- **g1:** a sidecar libp2p GossipSub mesh, with the ledger used for admission tickets and commitments. Fallback is a non-validator Substrate notification protocol.
- **s4:** a hybrid of an independent overlay and optional Midnight anchoring. Fallback is replicated feed gateways.
- **s1:** a hybrid of a separate overlay and the ledger for authorization and commitments. Fallback is replicated feed servers.

**(b) Evidence**
- `midnight-node/Cargo.lock` has 0 matches for `gossipsub`. It does contain `libp2p-kad`, `libp2p-identify` and others (`Cargo.lock:6685-6703`). g4's and g1's claim is supported.
- `NetworkWorker` is selected and litep2p is commented out (`node/src/command.rs:326-327`). Supported.
- The mainnet matrix lists `node-1.0.300`, `toolchain-0.31.1` and `onchain-runtime-3.0.0` (`midnight-docs/docs/relnotes/support-matrix.json:14, 38, 82`). Supported, so every ledger-dependent part of every proposal (g4's whole bus, g1's tickets, my anchors) is still blocked on activation.

**(c) Vote: hybrid, in g1's form, with g4's ledger-only mode as a deliberate first phase and permanent fallback** (o4 D8). The governance reason is blast-radius separation. A bus incident must not need a chain lever, and a chain pause should not delete the bus.

**(d) Strongest objection to the hybrid (from g4).** The overlay brings a new Sybil set, a new unpaid operator class and new legal exposure, and still cannot get around the chain. Admission is a Midnight transaction, so tx-pause stops new tickets anyway (g1 D7 admits this). If the hybrid's censorship resistance is bounded by the chain, its benefit is throughput and short retention, and the group must decide whether that is worth the operational cost.

---

## D9 Threats

**(a) Positions**
- **g4:** fee market, full-stream download and a second indexer. Publisher IP exposure is accepted.
- **g1:** tickets, permissioned mesh, stem as an unclaimed heuristic, parser reject rules, and a quantum record-now risk.
- **s4:** configuration-specific defenses. Kumar's formal work warns that GossipSub scoring guarantees depend on the configuration.
- **s1:** adds active recipient probing, group forks and downgrade.

**(b) Evidence**
- The parser lesson is supported (`bitmessage-guide.md:352-358`).
- The OMR and UnifOMR figures used to reject private retrieval at launch are supported (see D5).
- Seres FMD and Kumar GossipSub: not opened by me.
- From my own proposal: Nym's single monitor allowed framing attacks that cut the cost of dominating the active set by more than 99% (`2026-cao-nymreputation` txt L148-150). That matters for any proposal that will later score relays.

**(c) Vote: s1's table as the base**, plus g1's parser and malformed-log rows, plus my rows for:
- regulatory shutdown;
- compelled operator disclosure;
- steward capture;
- moderator abuse;
- reputation framing.

**(d) Strongest objection to the leading position.** None of the four lists abuse of the bus by its users, such as harassment, illegal content or unsolicited contact, as a threat. Nor does any list the institutional response to it: compelled logging, or a shutdown order to validators who can pause all user transactions (`runtime/src/lib.rs:321`). In practice that is the most likely way the bus ends, and none of their mitigations addresses it.

---

## D10 Build and verification (I lead)

**(a) Positions**
- **g4:** Phase 0 test vectors and measurements, Phase 1 two-process soak, Phase 2 wallet scanner, then stop. Triggers T1–T4 open a new design.
- **g1:** parser and circuit first. A 16-relay simulation with a spy-precision gate of 0.02. Wallet and contract `note`. Allow-list removed only after a failed red-team.
- **s4:** freeze the evidence (lockfile revisions and a claim register), bounded models, a 72 h measured test, upgrades trialled separately.
- **s1:** property games and reductions, simulation, a 48 h capacity run, observational interest tests, a funded pilot.

**(b) Evidence**
- s4's lockfile-pinned revisions (`Cargo.lock:7894, 8460, 7609`): not opened. My generation note above confirms its point: the local tag and working tree disagree on the 1 KiB constant.
- g1's 0.02 gate is derived correctly from p = 0.1, and it labels the 2× multiplier as its own.

**(c) Vote: my phased plan (o4 D10), extended with three pieces from the others.**
- From s4: the claim register and evidence freeze as the Phase 0 exit gate.
- From g1: the numeric spy-precision gate.
- From g4: triggers T1–T4 as named reasons to change course.

The other plans have no legal or operational gates. Mine requires:
- a counsel memo for each operator jurisdiction;
- an independent audit with no open critical findings;
- a pause→resume drill in ≤ 1 h;
- canary-measured tombstone compliance ≥ 99% within 48 h;
- no anonymity claim before at least 1,000 memberships and at least 20 events/s of organic traffic.

**(d) Strongest objection to my plan.** Five gated phases with legal memos may never reach Phase 3. A bus that ships late into an empty network has no anonymity set at all. g4's "build the convention, measure, stop" ships sooner and claims less.

---

## Where the group will disagree most

1. **D8 tether (ledger-only against hybrid).** g4 stands alone against three hybrids. The underlying question is whether a separate operator network is worth having when the chain can censor admission anyway.
2. **D4 admission and payment.** The four options are the fee market only (g4), anonymous DUST tickets (g1), identified issuer permits (s4, s1) and RLN with slashable NIGHT deposits (o4). Each places the identity map and the Sybil cost somewhere different, and the payment options for relays (none, contracts, or a pool) do not line up with the admission options.
3. **D6/D1 retention.** Lifetimes are 1 h (g1), 48 h (s4, s1), 24 h to 7 d (o4), and effectively permanent public ciphertext (g4). Retention sets wallet usability, legal exposure and harvest-now-decrypt-later risk all at once.

## The one fact to check

**Is ledger 9 (`emit`/`Misc` plus `contractEvents`) active on the target network, and if not, when will it be?**

The docs' matrix pins mainnet to `node-1.0.300`, `toolchain-0.31.1` and `onchain-runtime-3.0.0` (`support-matrix.json:14, 38, 82`). The local node tree pins ledger 9 at `spec_version 003_000_000` (`runtime/src/lib.rs:276`).

- **If ledger 9 is not active and not scheduled:** g4's design has nowhere to run, and g1's tickets and my anchors cannot work either. s4/s1-style off-ledger permits win D4, and the hybrid wins D8 by default.
- **If it is active:** measuring one real `publish` or admit transaction (bytes and DUST) on it settles g4 against g1 on D4 and D5.

**How to check:** read the `midnight-ledger` dependency in `midnight-node` at tag `node-1.0.300` (`Cargo.toml`/`Cargo.lock`), and query the live runtime's `spec_version` on mainnet and preprod.
