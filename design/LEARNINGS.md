# What the MPE prototypes taught about the design

Three independent Rust builds (A, B, C) implemented the reconciled Prototype design of `design/PROTOTYPE.md` on rust-libp2p 0.57 and GossipSub 0.50. Each one includes:
- sealed fixed-size Envelopes;
- a stand-in admission proof;
- Store Nodes;
- a MockLedger with Anchors and a contract consumer;
- the ledger fallback carrier.

**Sources.** Unless a figure is labelled otherwise, it comes from the ten scenarios at 50 Bus Nodes, seed 1 and a 60 s publish window, in `/home/charl/privateEvents-build/judge/<build>/`.
- Variant runs (byte cap, IDONTWANT off, mesh (6, 5, 12, 2), poisoned eclipse, EID message id, 10 ms proofs, 50/s) are in `/home/charl/privateEvents-build/judge/experiments/`.
- Older figures (seed 42, round 1) come from the builders' RESULTS files and are labelled "round 1".
- The winning build (A) is in `/home/charl/privateEvents/prototype/`.

**Limits that apply to every number below:**
- **One machine.** All runs share one 6-core host and one process, with 50 to 61 swarms.
- **Localhost networking.** Transport is localhost TCP (A) or in-memory (B, C). There is no wide-area latency, loss or bandwidth cap, and no IP diversity.
- **Synthetic admission cost.** The admission proof is a stand-in that reveals member secrets to every Bus Node, and its cost is a 4.5 ms busy loop.
- **Mock ledger.** The ledger, Indexer and contract are mocks that copy Midnight's published limits.
- **Single, short runs.** Each scenario ran once per configuration, for 60 s.

Delivery and latency are therefore optimistic, CPU is contended, and nothing here supports a privacy claim about admission.

## Summary

1. **The core pipeline works end to end at the reconciled parameters:** 4 wire sizes, 0 plaintext leaks, 100% baseline delivery with p99 1.0 to 2.4 s, and ledger fallback p99 25 to 36 s.
2. **IDONTWANT (GossipSub 1.2) is the largest cost lever measured.** Baseline ingress amplification is 2.3 to 2.5× with it and 5.1× without. Class-3 egress falls by 70 to 76%. The requirement to run GossipSub "v1.1" is wrong.
3. **Stock rust-libp2p cannot negotiate 1.2 under a custom protocol id.** Network-scoped protocol names need a fork. The default `/meshsub/1.2.0` works unpatched.
4. **The planning bandwidth model (1.25 × D × unique bytes) overstates mesh egress about eightfold.** The busiest node is the one serving Subscriber feeds, not the mesh.
5. **Independent validators cannot enforce a network-wide admission quota.** 2 of 2 and 5 of 5 conflicting Envelopes were accepted under one class-3 credit. MPE-ECO-022 must change.
6. **The 140 s restart barrier is affordable only if a restarting Bus Node says so.** With an explicit Busy reply and 5 s repair, churn delivered 100% with p99 1.1 s. With silent Ignore and 60 s repair, p99 was 42.7 s. Without client re-discovery, delivery was 81.6%.
7. **A Busy Ignore is a permanent loss at that node**, because rust-libp2p caches the message id first. Second-source reconciliation is load-bearing, and its interval sets the latency tail.
8. **The Subscriber's cost is the whole-Shard download: about 1.7 GB/day at the baseline mix.** The gateway protocol can multiply that by 1.1 to 4.9 depending on the codec and the cursor overlap.
9. **The salted Tag is cheap: 0.2 to 0.5 µs per key.** The trial-decryption comparison was never built, so DEC-003 stays open.
10. **Untested:** the stale-chain rule in a running overlay, idle-Shard scoring, storage overhead, receipt cost, anchor latency, and any 50/s per-node ceiling. Each is listed under "Next experiments".

---

## Design decisions D1 to D10

### D1 Event format

**What was built.** All three builds implement:
- the 8 B visible header and a 512 B Admission Slot;
- four Sealed Body classes, giving wires of 776, 1,544, 4,616 and 16,904 B;
- a 44 B clear prefix: salt, nonce and Tag;
- a 70 B authentication block.

**Measured.**

| Measure | Result | Where |
|---|---|---|
| Distinct sizes on the wire | Exactly 4 in every honest scenario | `leakage`, all builds |
| Plaintext leaks | 0 over 26,600 to 42,500 captured frames | `leakage`, all builds |
| Class-0 overhead | 690 B of 776 B (89%) is header, slot, prefix and authentication; the 520 B header plus slot alone is 67% | arithmetic |
| Seal p50 | 17.5 to 32 µs | crypto reports, round 1 |
| Authenticated open p50 | 41 to 55 µs, of which the Ed25519 verify is 37 to 38 µs | crypto reports, round 1 |

Class-0 payload capacity is 86 B.

**What it confirms.** The fixed-size format composes with GossipSub, the stores and the ledger carrier. No path leaked a canary.

**What it refutes.** The literal MPE-CRY-004 (header bytes 0-7 in the AEAD associated data) cannot coexist with the ledger carrier. A body-only `Misc` copy cannot rebuild the visible expiry. All three builds therefore adopted the same profile:
- header bytes 0-3 go into the associated data;
- expiry is fixed at creation + 172,800 s;
- expiry is authenticated through the EID, the signature and admission.

A variable lifetime would need a sealed expiry field.

**Unknown.** The real Admission Slot width, which depends on the proof system (DEC-013).

### D2 Privacy

**What was built.** The relays are body-blind. The defences are:
- canary scanning of every relay and client frame;
- window-level `final` labelling, with no per-EID request from Subscribers;
- per-window receipts;
- a reaction transaction carrying only statement fields, signature, consumption nullifier and optional inclusion path. Round 1 had builds that put the stream or event secret on the transaction.

**Measured.** 0 leaks in `leakage` for all three builds.

The leak scanner only sees contiguous byte strings, and A encodes RPC byte fields as CBOR integer arrays. A key carried in an RPC field could therefore not be detected in A. In B, envelope fields and the scanner were fixed, but EIDs are still integer arrays. C uses byte strings throughout.

**What it confirms.**
- Finding F4: requesting receipts or inclusion paths per recognized Event leaks interest. All three builds converged on per-window requests.
- The reaction must carry public statement data only.

**What it refutes.** Nothing measured refutes the leakage table.

**Unknown.** Everything about admission privacy: the stand-in links every Envelope to its member at every Bus Node. Also unmeasured: timing and volume analysis, the global observer, and first-spy precision (DEC-023).

### D3 Publish and subscribe model

**What was built.**
- Whole-Shard reception.
- Local Tag recognition over 32 keys per Subscriber.
- A pull feed (1 s cadence) or an embedded Subscriber.
- Back-fill with portable `(expiry, EID)` cursors.
- Inventory reconciliation from a second Operator, every 2 to 60 s depending on the build.
- Fallback to another Bus Node.

**Measured.**
- Baseline delivery: 1108/1108 (A), 1198/1198 (B) and 1064/1064 (C). p50 is 142 to 211 ms and p99 1.05 to 2.39 s.
- Back-fill after a mid-pagination store failure:
  - A: 263/263, counted from `/backfill` pages only, with late live delivery of 63/63.
  - C: 60/61. The one Event in flight at the join instant was missed.
  - B: 323/323.
- Churn: see DEC-017.
- No build delivered a duplicate to an application.

**What it confirms.**
- At-least-once delivery holds only with reconciliation. A one-shot back-fill at join time misses Envelopes that are in flight, so a late Subscriber needs a reconciler from the first second.
- The portable cursor works across Operators.

**What it refutes.** "Fetch the missing Envelope" (MPE-PUB-015) cannot be met without an identifier request, which MPE-PUB-030 forbids. All builds repair by window (finding F5).

**Unknown.** Behaviour across a 48 h retention window and on mobile clients.

### D4 Sustainable model

**What was built.**
- Per-class quotas of (64, 16, 4, 1) per 60 s epoch, one nullifier per Envelope.
- Per-peer, per-Shard token buckets of 20/s.
- Queues of 8 per peer and 128 per node.
- Mock registration and revocation.

**Measured.**
- `spam` (100/s through one ingress during honest traffic):

  | Build | Accepted | Quota | Honest delivery |
  |---|---:|---:|---:|
  | A | 128 | 128 | 1.0 |
  | B | 128 | 128 | 1.0 |
  | C | 29 | 128 | 1.0 |

  In A, 103 of the honest observations were repaired.
- Phase B (one class-3 credit spent at several ingress nodes at once): 2 of 2 accepted (A) and 5 of 5 (C).

**What it confirms.** Local quota enforcement works.

**What it refutes.** MPE-ECO-022, the network-wide "at most one per allowance" bound (see DEC-014 and DEC-016).

**Unknown.** The real proof cost, and DUST costs for registration.

### D5 Performance

**What was built.** Synthetic 4.5 ms verification, behind per-node and global semaphores.

**Measured.**
- Bus Node CPU at baseline: 2.45 to 2.79 s per 60 s (0.041 to 0.046 core), almost all of it synthetic verification. With a 6 ms cost: 3.69 s (0.061 core), delivery 1.0, p99 1.12 s (B, `verify10000`).
- Bandwidth: see DEC-012 and DEC-027.
- At 50 Envelopes/s (B, `rate50`, 240 memberships):
  - 42.1% of pairs delivered, 15.5% within 10 s, p99 57.2 s;
  - 285 ingress timeouts;
  - the host needed 50 × 50 × 4.5 ms = 11.25 cores of proof work against 6 available.

**What it confirms.** CPU at 10/s is dominated by proof verification, and everything else is small.

**What it refutes.** Nothing. The 50/s result says nothing about one Bus Node, because 50 nodes share six cores.

**Unknown.** The per-node ceiling at 50/s, which needs one node per machine or a measured proof. Wide-area latency.

### D6 Storage

**What was built.**
- In-memory per-Shard stores, keyed by `(expiry, EID)`.
- Feed rings capped at 64 MiB.
- Paged back-fill, inventory and receipts.

**Measured.** `store.max_bytes` is, by construction, Envelope bytes plus 72 B per entry. Examples: 3,293,344 B for 194 class-3 Envelopes (B, `bytecap`) and 1.2 to 1.5 MB at baseline.

**What it confirms.** The interfaces work: inventory, paged receipts from three Operators, and the `stored` assignment in C.

**What it refutes.** A hard cap on the application seen-set is unsafe.
- B capped the seen-set at 65,536 identifiers and answered Busy to every Accept beyond it. At 10/s a Bus Node then goes silent after about 1.8 hours, for two days.
- The seen-set must hold 10/s × 172,860 s = 1.73 million identifiers per Shard (RECONCILE §1.1). That is a size requirement, not a cap.

**Unknown.** The real storage multiplier, durable stores and restart recovery (DEC-004).

### D7 Infrastructure actors

**What was built.**
- A mock roster of three Operators.
- An allow-listed relay set, with −20 for unlisted peers.
- Bootstrappers.
- An anchorer role on Bus Node 0.
- Store Nodes, one per Operator.

**Measured.**
- Churn that replaced all three original Store Nodes left their replacements empty during the 140 s barrier.
- In A, no client learned the replacements' addresses: 168 dial failures and 0 successful reconciliations, giving 0.816 delivery.

**What it confirms.** Clients need the relay list and its addresses from the Registry (MPE-NET-054), refreshed on change, not a static bootstrap.

**Unknown.** Operator economics and the end state of the Operator set.

### D8 Network tether

**What was built.**
- An overlay on rust-libp2p.
- Ledger for Registry, Anchors and the fallback carrier, all mocked.

**Measured.**
- GossipSub 1.2 needed a 3-line fork to keep a network-scoped protocol id (A, C), or the default id (B).
- Per-class egress needed a hook inside the connection handler.
- Fallback: see DEC-008.

**What it refutes.** The assumption that stock rust-libp2p meets MPE-NET-006 together with MPE-NET-047 (see DEC-012).

**Unknown.** Everything about real Midnight nodes and Indexers.

### D9 Threats and open risks

**Measured.**

| Attack | Scenario | Result |
|---|---|---|
| Malformed injection, 5 peers × 20/s | `malformed` | 0 panics, honest delivery 1.0 in all three builds |
| Spam | `spam` | Accepted ≤ quota |
| Replay, identical bytes at +62 s | `replay` | B: 250 replays + 20 expired, all classified. C: 220 + 10. A: classified only 24 of 48 same-EID re-admissions at the first honest node. Honest delivery was unaffected. |
| Eclipse, 20% withholding attackers around a victim | `eclipse` | Victim delivery 1.0 everywhere (see DEC-006) |
| Corrupted-slot front-run | `replay` (A) | See DEC-010 |
| Equivocation | `spam` phase B | Succeeds (DEC-014) |

**What it confirms.** Structural checks before cryptography stop junk cheaply. In A's `malformed` run, 107 of 6,002 injections reached classification; graylisting and rate limits dropped the rest.

**Unknown.** CVE-2022-47547 closure, cold-start Sybil at 20%, and open admission.

### D10 Build and verification plan

**What it showed about verification:**
- **Short runs hide time-dependent defects.** A 60 s run cannot show eviction (90 loaded heartbeats), seen-set growth, or store pruning.
- **One shared host makes delivery depend on contention.** B's own runs under contention lost 34% of honest pairs in `spam`. The same build, run alone, lost none.
- **The checker's gates can pass while a design property is untested:**
  - C's eclipse ratio counted Accepts injected by a 2 s store repair;
  - B's back-fill count accepted any Subscriber's back-fill pages.

**Requirement change.** MPE-VER-041 should specify run length, isolation, and seeds-per-result. See "Requirements to change".

---

## Open decisions in RECONCILE.md

### DEC-003 Recognition mechanism

**What was built.** Option (d), the salted HMAC Tag in the Sealed Body clear prefix. No build implemented `--recognition trial`.

**Measured.** The Tag scan:

| Build | 32 keys | 256 keys | Per key |
|---|---|---|---|
| C | 5.7 µs | 46.8 µs | 0.18 µs |
| B | 15.5 µs (thread CPU) | 128.3 µs | 0.50 µs |

At 100 Envelopes/s and 32 keys that is 0.06 to 0.16% of one core. At 256 keys it is 0.5 to 1.3%.

The trial-decryption cost was not measured. It can be estimated from the authenticated open minus the Ed25519 verify (C, `crypto.json`): about 3.5 µs at class 0, 7.5 µs at class 2 and 18.7 µs at class 3, per key and per Envelope. At 100/s, class 2:

| Keys | Trial (estimate) | Tag (measured) |
|---|---|---|
| 32 | about 2.4% of a core | 0.06 to 0.16% |
| 256 | about 19% of a core | 0.5 to 1.3% |

**What it confirms.** The Tag path is 15 to 40 times cheaper per key (estimated ratio).

**What it leaves open.** The Q1 settling rule pulls both ways:
- At 32 keys both paths are under 5% of a core, so the rule would move the default to trial decryption (a).
- At the 256-key cap trial decryption exceeds 5%, while the Tag stays near 1%.

**Recommendation.** Settle on the key cap, not the 32-key fixture. On that basis the Tag stays (d). Measure trial decryption directly before deciding, on phone hardware too.

### DEC-004 Envelope lifetime and retention

**Measured.** Stores are in memory. `store.max_bytes` is computed as Envelope bytes plus a fixed 72 B per entry. That gives a multiplier of 1.004 at class 3 and 1.09 at class 0 by definition; it is not a measured database footprint.

**Unknown.** The real multiplier, the 48 h fill, and the 7-day archive. The 48 h decision is untouched by these results.

### DEC-005 Operating rate (10 versus 50 per second)

**Measured.**
- At 10/s, every build delivers 100% with p99 at most 2.4 s and per-node CPU of 0.041 to 0.046 core.
- At 50/s (B, `rate50`): 42.1% delivered, p99 57.2 s. The host was 1.9 times oversubscribed on synthetic proofs alone.

**What it confirms.** 10/s is safe on this implementation.

**Unknown.** Whether one Bus Node can sustain 50/s. The arithmetic says 50 × 4.5 ms = 0.225 core, inside the 0.30-core edge budget, but no run isolated one node. The count ceiling stays at 10/s until a one-node-per-host run or a measured proof exists.

### DEC-006 Relay admission (allow-list or open)

**What was built.** The eclipse scenario has the allow-list off and 20% withholding attackers that dial the victim. Scoring is on with the reconciled parameters, and P3 is off.

**Measured.**

| Build | Variant | Victim delivery | Attacker / honest peers |
|---|---|---|---|
| A | inbound | 1.0 | 10 / 27 |
| B | inbound | 1.0 | 10 / 18 |
| B | inbound, mesh (6, 5, 12, 2) | 1.0 | 10 / 18 |
| B | poisoned | 1.0 | 10 / 12 |
| C | inbound | 1.0 | 5 / 6 |

In B's poisoned variant the victim dials 8 attackers, 2 honest relays and the 2 bootstrappers. C's figure is assisted by a 2 s store repair that feeds the victim's validator, so it does not measure mesh resistance.

No run lasted the 90 loaded heartbeats eviction needs, so no withholder was shown being evicted inside a scenario. A and B prove eviction in dedicated node tests with injected load.

**What it confirms.** With zero link latency, one honest mesh path is enough. A victim that keeps any honest dialled peer receives everything.

**What it refutes.** Nothing. These runs cannot refute the scoring caveats in the literature, because withholding costs an attacker nothing in a network where one honest link delivers instantly.

**Unknown.**
- A victim whose dial sources are entirely attacker-controlled.
- Forged IHAVE without IWANT answers.
- Wide-area delay, where withholding matters.

The allow-list default (a) stands.

### DEC-007 Admission instrument

**Measured.** Nothing about RLN. The stand-in gives every Bus Node the member secrets, so the admission privacy argument is untested. The pluggable `AdmissionProof` trait shape works in all three builds.

The decision stays where it is.

### DEC-008 Ledger fallback

**What was built.** Classes 0-2 as 1, 4 or 16 `Misc` parts of 256 B. Class 3 is refused. The mock block budget, finality and log limits are enforced.

**Measured (`fallback`).**

| Build | Delivered | Ledger bytes | Bytes per Event | p50 | p99 |
|---|---|---|---|---|---|
| A | 319/319 | 3,193,280 B | 10,010 B | 23.1 s | 31.1 s |
| B | 328/328 | 3,371,552 B | 10,279 B | 24.1 s | 36.2 s |
| C | 324/324 | 2,920,320 B | 9,013 B | 21.8 s | 25.0 s |

The arithmetic for the class mix is about 9,160 B per Event. No Event was dropped over a limit.

**What it confirms.**
- The lane works inside the limits as an emergency path.
- Latency is block time plus finality plus polling.

**What it refutes.**
- C's first version showed that all-or-nothing reassembly lets anyone block the lane with one malformed group. The "discard the group" rule of MPE-FMT-046 is load-bearing.
- Polling must drain every log entry, or a burst silently drops Events (B, round 1).

**Unknown.** Real Midnight fees, inclusion under contention, the 1,000-Event burst, and blocks-to-clear.

### DEC-009 Stale chain view

**What was built.** C drives the Registry view from the Ledger Adapter's finalized head. Its frozen-adapter node test shows a chain-dependent check returning Ignore(Clock) while stale and Reject when fresh.

**Not measured.** No build implements `--ledger freeze` in the simulator. Delivery during a freeze and P4 changes on honest peers are therefore unmeasured. The rule is correct at the unit level only.

### DEC-010 GossipSub message id

**What was built.** The message id is a hash of the wire bytes in all builds. A also has `--msgid eid`.

**Measured.**
- The corrupted-slot front-run node tests pass with the wire id: honest copy at all 8 nodes (A) and at all 32 swarms (C).
- In A's `replay` run, one corrupted-slot copy is sent ahead of the first honest Envelope:
  - with the wire id: 1108/1108 pairs;
  - with the EID as message id: 1107/1108. One Subscriber lost that Event, and the 60 s reconciliation did not repair it within the drain.

**What it confirms.** The attack exists with an EID message id, even from a single injection point. The wire-byte id closes it. DEC-010 (b) is confirmed: one run, one injection.

**Unknown.** The size of the attack with many injection points. Whether the pre-validation IDONTWANT opens a second suppression path under the wire id; no loss was seen.

### DEC-011 Shard count

**Not measured.** No build ran `--shards 8`. B's validator cap of 8,192 nullifiers would Busy-drop above about 58 Accepts/s per node, so an 8-Shard benchmark at 10/s per Shard would fail on B. That is an implementation limit, not a design result.

**Arithmetic, confirmed by the measured whole-Shard volume** (DEC-021): one of eight Shards is about 210 MB/day, still about 3.5 times the mobile budget.

### DEC-012 Mesh profile, and the GossipSub version

**Measured. Nominal load (B):**

| Mesh | Median ingress per node, 60 s | Median egress per node, 60 s |
|---|---:|---:|
| (8, 6, 12, 4) | 3.29 MB | 3.13 MB |
| (6, 5, 12, 2) | 2.28 MB (round 1) | 2.20 MB |

**Measured. Class-3 load (B, 194 class-3 Envelopes in 60 s = 83% of the byte cap):**

| Mesh | Median ingress / egress | Busiest egress | Ingress amplification |
|---|---|---|---|
| (8, 6, 12, 4) | 0.55 / 0.51 Mbit/s | 2.73 Mbit/s | 1.27× |
| (6, 5, 12, 2) | 0.52 / 0.47 Mbit/s | 3.23 Mbit/s | 1.18× |

Eclipse delivery was 1.0 under both profiles.

**IDONTWANT on and off (paired runs):**

| Build and load | On | Off |
|---|---|---|
| B, nominal: ingress amplification | 2.26× | 5.12× |
| B, nominal: median ingress | 3.29 MB | 7.44 MB |
| A, class 3 only: ingress amplification | 1.41× | 4.68× |
| A, class 3 only: class-3 payload egress per node | 1.72 MB | 5.85 MB (−70.5% with it on) |
| C, 10 s runs: class-3 payload egress | | −75% with it on |
| A, nominal (A's run): class-0 payload egress | 1.17 MB | 1.20 MB |

Class 0 is unchanged because 776 B is below the 1,000 B IDONTWANT threshold.

In round 1, A and C ran v1.1, where IDONTWANT is inert, and had 6.4 to 6.6× ingress amplification.

**What it confirms.**
- (8, 6, 12, 4) costs little more than (6, 5, 12, 2) once IDONTWANT is on: 7 to 13% more ingress.
- The profile choice can follow the Sybil cold-start result alone.

**What it refutes.**
- "GossipSub v1.1" in MPE-NET-008 and the brief. The design needs 1.2.
- The assumption that a network-scoped protocol id comes for free. rust-libp2p 0.50's public `Version` selector has no `V1_2`, so a custom id negotiates 1.1 and IDONTWANT is silently off. A and C each added a 3-line `Version::V1_2` arm in a vendored crate. B kept `/meshsub/1.2.0` unpatched.
- The assumption that per-class egress is observable. It needed a hook in the connection handler.

**Unknown.** Mesh behaviour under 20% cold-start Sybil at 200 and 1,000 nodes, which is the settling evidence for DEC-012.

### DEC-013 Size classes and Admission Slot width

**Measured.**
- Seed-1 baseline: 325, 119, 62 and 26 Envelopes per 60 s for classes 0 to 3 (C, `leakage` capture, 50 nodes).
- Class 0 spends 520 of 776 B (67%) on the header and slot.

**What it confirms.**
- Class 3 at 26 per minute is under the 30-per-minute floor of the Q12 rule at the baseline mix.
- At the 50/s weights it would be about 3 per minute (arithmetic).

**Recommendation.** Merge class 3's anonymity set concern into the DEC-013 decision. Either drop class 3 from the default table or raise its share by policy. The Slot-width trigger waits for a real proof.

### DEC-014 Equivocation outcome

**Measured.**
- A: two concurrent class-3 bodies under one nullifier were both accepted at two ingress nodes (`spam` phase B and the `distributed_equivocation_exposes_aggregate_gap` node test).
- C: five ingress nodes accepted five distinct EIDs against a class-3 quota of one.
- B: the same result, by regression test.
- Evidence appears only after the Envelopes have been forwarded.

**What it confirms.** Option (b), Ignore plus evidence plus revocation, is the only workable outcome. Rejecting the second copy would penalise honest forwarders. B notes that its Reject rule conflicted with honest forwarding.

**What it adds.** The per-class quota is not a delivery bound. Two requirements follow:
- Bus Nodes must gossip equivocation evidence.
- Clients must keep at most one Envelope per nullifier, which they can see in the visible Admission Slot.

**Unknown.** Time until every node holds evidence. The number of conflicting Envelopes delivered to Subscribers per nullifier was not counted separately from acceptance.

### DEC-015 Unknown or foreign version

**Measured.** In A's `malformed` run, 49 wrong-version Envelopes were Rejected, along with other structural rejects, with no honest loss. This is consistent with (a): the version is bound to the topic and a mismatch is Rejected.

### DEC-016 Quota accounting

**Measured.** Per-class limits worked locally: the epoch-derived quota of 128 was never exceeded in `spam`. Under C's rate limits, 29 of 6,000 attack Envelopes were accepted.

**Refuted.** The phase B result (DEC-014) refutes the network-wide reading of (c).

**Unknown.** The 2× byte-excess concern, which needs the class-mix simulation at the lowest tier.

### DEC-017 Durability of admission replay state (restart barrier)

**What was built.** In-memory nullifier state and a 140 s barrier on every start. Every churn joiner waits the full 140 s.

**Measured (`churn`: 10% of nodes replaced every 10 s, 60 s window, 125 s drain).**

| Build | Restart behaviour | Delivery | p99 | Within 10 s | Repair |
|---|---|---|---|---|---|
| A | Silent Ignore (6,066 Ignore:Restart decisions); clients never learn replacements | 904/1108 = 0.816 | 26.5 s | | none succeeded |
| B | Silent Ignore | 1198/1198 | 42.7 s | 1117 of 1198 (93.2%) | 60 s inventory repair |
| C | Busy reply from a barrier node, so the publisher retries elsewhere at once | 1136/1136 | 1.1 s | | 5 s per-Subscriber repair |

A's minimum per Subscriber was 0.454. The cost of C's approach is gateway traffic: 7.59 GB/day per client under churn, against 1.81 at baseline.

**What it confirms.** The waiting barrier itself is not the problem. The problem is that a Bus Node inside the barrier stays silent. An explicit refusal plus fast repair restores the 10 s target.

**What it refutes.** MPE-NET-049 ("nothing for Reject or Ignore") must allow a Busy or Refused reply for local, non-content reasons.

**Unknown.**
- Barrier occupancy over time.
- Behaviour with 240 s runs, where early joiners clear the barrier.
- The durable-commit option (a).

### DEC-021 Light and mobile reception

**Measured.** Whole-Shard raw download at the measured rate:
- 1.67 GB/day (C), at 532 Envelopes per 60 s, mean wire 2,184 B;
- 1.69 GB/day (A).

Actual gateway client traffic per Subscriber:

| Build | Gateway traffic | Ratio to raw | Main cause |
|---|---:|---:|---|
| C | 1.81 GB/day | 1.08× | byte strings, small repair cost |
| B | 8.27 GB/day | 4.9× | 2 s cursor overlap on every 1 s poll; integer-array EIDs |
| B, round 1 | 2.81 GB/day | 1.8× | |
| B, byte cap | 18.2 GB/day | | |

**What it confirms.**
- Whole-Shard reception at about 1.7 GB/day is 28 to 30 times a 56-60 MB/day mobile budget.
- Default (a) is a desktop or always-connected profile. Mobile needs one of the opt-in profiles.

**What it adds.** The feed protocol's overlap and codec can cost more than the payload. A requirement should bound gateway bytes per delivered Envelope.

### DEC-022 Contract consumption path

**What was built.** The reaction carries the signed statement, the Ed25519 signature, the consumption nullifier and an optional inclusion path. The mock checks the nullifier against an off-transaction witness.

**Measured.** 100 racing reactions gave 1 effect in all builds. Forged nullifiers and signatures had no effect.

**What it refutes.** Round-1 shapes that put the stream secret (A) or the event secret (B) on the transaction. Both would disclose secrets to the ledger.

**Unknown.** Compact circuit size and proving time for (e) against (f). The mock cannot bind the nullifier to the event secret without a circuit.

### DEC-023 Publish ingress

**Measured.** Not measured. No first-spy run exists. Publish ingress retry behaves as specified:
- 5 s per attempt, 3 Bus Nodes;
- concurrent publication tasks are needed. A's original sequential publisher stretched a 60 s schedule to 81 to 89 s.

### DEC-024 Anchors

**What was built.** One Anchor per 60 s window covering all Shards, submitted by an anchorer Bus Node. `/anchor-leaves` and `/inclusion` are served. Subscribers check `final` per window.

**Measured.** In `anchor`, every build finalized 2 batches:

| Build | Checks | What a check is |
|---|---|---|
| A | 5/5 | 4 window checks, 1 contract path |
| B | 120/120 | 20 Subscriber window checks, 100 contract checks |
| C | 21/21 | one window fetch reused for 10 Subscribers, plus 1 contract path |

**What it shows.** Every builder chose to download the anchorer's leaf list instead of first recomputing the root from the Subscriber's own inventory. In effect, all three voted for published leaf lists, and that adds no interest leak.

**Unknown.** The share of windows in which a local recomputation would match (Q15), and the time from publication to `final`.

### DEC-025 Second-source reconciliation

**Measured.**
- A Busy Ignore at a node puts the message id in rust-libp2p's duplicate cache first. A copy dropped for a full queue is therefore never re-accepted from another peer within 60 s.
- With reconciliation wired, A repaired 103 Subscriber observations in `spam` and 267 in `backfill`. In round 1, without it, A lost 8 honest pairs in `spam`.
- B's own repair runs under host contention lost 34% of honest pairs in `spam` with a 60 s single-pass repair.
- Interval trade-off: C's 5 s repair under churn gave p99 1.1 s at 4.2 times baseline gateway bytes. B's 60 s repair gave p99 42.7 s.
- Reconciliation overhead could not be isolated. C's total client overhead over raw envelope bytes at baseline is 8%, including feed framing and transport.

**What it confirms.** (a): reconciliation must be a MUST, and it must be in the client library, not the simulator. Only C put it there.

**Unknown.** The overhead fraction against the 2% bound.

### DEC-026 Delivery labels

**Measured.** C assigned `stored` to 1064 deliveries from paged receipts of three Operators, and `final` per window. A has the `stored()` predicate but no client calls it.

**What it confirms.** The three orthogonal attributes are implementable.

**Unknown.** Receipt cost (Q14).

### DEC-027 Direction of bandwidth budgets

**Measured.** Median per-node rates at the class-3 load (B, `bytecap`, scaled to the full 65,536 B/s cap):

| Profile | Ingress | Egress | Busiest egress |
|---|---:|---:|---:|
| (8, 6, 12, 4), IDONTWANT on | 0.66 Mbit/s | 0.61 Mbit/s | 3.3 Mbit/s |
| (6, 5, 12, 2) | 0.62 Mbit/s | 0.57 Mbit/s | 3.9 Mbit/s |

Without IDONTWANT, A's class-3 run scales to about 2.5 Mbit/s median per direction.

The busiest egress is the node that also serves Subscriber feeds. In C's `churn` run that node reached 43.0 MB in 60 s (5.7 Mbit/s) at nominal load, because of 5 s repair.

**What it confirms.** A per-direction budget is the right unit. 6 Mbit/s holds for mesh traffic with a wide margin.

**What it refutes.** The planning model 1.25 × D × 64 KiB/s = 5.24 Mbit/s for mesh egress. The measured median is about one eighth of that. Average egress equals average ingress, which is unique bytes times amplification, not D times unique bytes.

**What it adds.** Feed and repair service, not the mesh, is what approaches the budget. It needs its own budget (P-PUB-10 streams per node).

---

## Learning questions

Each answer names its source and compares the result with the prediction recorded beforehand in `PREDICTIONS.md`.

**Q1 Tag versus trial decryption.**
- **Answer:** the Tag costs 0.18 to 0.5 µs per key. Trial decryption was not built; the estimate is 3.5 to 18.7 µs per key by class. At 32 keys and 100/s both stay under 5% of a core. At 256 keys trial decryption is about 19%. (DEC-003.)
- **Prediction:** tag 8 to 15 times cheaper, both under 5%, rule moves the default to trial.
- **Verdict:** right on the 32-key arithmetic, and the estimated ratio is higher (15 to 40). The rule's 32-key reading is wrong at the key cap. Untested as a measurement.

**Q2 Validation ceiling.**
- **Answer:** non-proof CPU at 10/s is small. Total per-node CPU is 0.041 to 0.046 core, almost all proof. The 50/s run is host-bound (42.1% delivered), so the per-node ceiling is unanswered. A 6 ms proof gives 0.061 core at 10/s with no delivery loss.
- **Prediction:** non-proof under 0.1 core; ceiling stays at 10/s.
- **Verdict:** right on the first part. The second is untestable on one host.

**Q3 Eclipse.**
- **Answer:** inbound surround leaves the victim at 1.0 with D_out = 4 and with 2. The partially poisoned variant (8 of 12 dialled peers attackers) also leaves it at 1.0. (DEC-006.)
- **Prediction:** at least 0.99 for both inbound profiles; poisoned below 0.5.
- **Verdict:** right on inbound; wrong on poisoned as run. A victim that keeps even 2 honest outbound peers and 2 bootstrappers receives everything on a zero-latency network. A fully poisoned dial list was not tested.

**Q4 Bandwidth at the byte cap.**
- **Answer:** median egress is 0.61 Mbit/s and the busiest node 3.3 Mbit/s with D = 8. Both are inside 6 Mbit/s. The planning model overstates mesh egress about eightfold. (DEC-027.)
- **Prediction:** egress 3.5 to 4 Mbit/s, ingress 2 to 4 Mbit/s; the model overstates.
- **Verdict:** direction right, magnitude wrong. Measured egress is a sixth of the prediction. The prediction assumed every node forwards each message to D − 1 peers. With IDONTWANT most forwards are suppressed, and average egress equals average ingress.

**Q5 IDONTWANT.**
- **Answer:** class-3 egress falls by 70.5% (A) and 75% (C). Total ingress falls from 5.1 to 2.3× amplification (B). Class 0 sees no change, because it is below the 1,000 B threshold.
- **Prediction:** under 10% saving in the simulator.
- **Verdict:** **wrong, and the most useful miss.** Even at zero link delay, IDONTWANT arrives before most duplicates. In-process forwarding is not instantaneous: validation takes 4.5 ms per hop while IDONTWANT goes out before validation. The Q5 rule (at least 30%) makes IDONTWANT mandatory.

**Q6 Message id.**
- **Answer:** with the EID as message id, one corrupted-slot front-run cost 1 of 1108 pairs, unrepaired within the drain. With the wire id, 0. (DEC-010.)
- **Prediction:** the EID id suppresses the honest copy where the corrupted copy arrives first; the wire id keeps at least 0.999.
- **Verdict:** right. Evidence is one run with one injection point.

**Q7 Stale chain.**
- **Answer:** unit level only. A frozen adapter turns a chain-dependent Reject into Ignore(Clock). There is no overlay run.
- **Prediction:** delivery at least 0.999 and no penalties.
- **Verdict:** untestable this round.

**Q8 Restart barrier under churn.**
- **Answer:** depends on the reply. Silent Ignore gave 0.816 (A, without client re-discovery) or 1.0 with p99 42.7 s and 6.8% of pairs later than 10 s (B). Busy plus 5 s repair gave 1.0 with p99 1.1 s (C). (DEC-017.)
- **Prediction:** delivery below 0.99 and repair carrying more than 10%; the redesign rule triggers.
- **Verdict:** partly right. The silent barrier is expensive as predicted. C shows the redesign needed is a reply and a repair cadence, not durable commits.

**Q9 Equivocation.**
- **Answer:** 2 of 2 (A) and 5 of 5 (C) conflicting EIDs accepted under one class-3 credit. (DEC-014.)
- **Prediction:** 3 to 5 delivered per nullifier.
- **Verdict:** right on acceptance. Delivery per nullifier was not counted separately.

**Q10 Storage multiplier.**
- **Answer:** not answerable. The in-memory store reports bytes plus a fixed 72 B per entry, which is 1.004 to 1.09 by definition. No allocator or database overhead was measured.
- **Prediction:** 1.05 to 1.25.
- **Verdict:** untestable.

**Q11 Subscriber download.**
- **Answer:** raw whole-Shard volume is 1.67 to 1.69 GB/day at the measured rate (532 to 554 Envelopes per 60 s). That matches the arithmetic for that rate within 2%. Gateway transport is 1.81 (C) to 8.27 (B) GB/day. 8 Shards were not run.
- **Prediction:** within 5% of 1.86 GB/day; 230 MB/day at 8 Shards.
- **Verdict:** right on the payload arithmetic. It missed that the feed protocol can multiply the cost up to 4.9 times. The 8-Shard figure is arithmetic only.

**Q12 Size classes.**
- **Answer:** class 3 carries 26 Envelopes per minute at the baseline mix (seed 1). That is under the 30-per-minute floor. (DEC-013.)
- **Prediction:** about 30 per minute at baseline; about 3 at the 50/s mix.
- **Verdict:** right. The rule triggers for class 3 at baseline. The 50/s mix was not measured, because that run collapsed.

**Q13 Reconciliation cost.**
- **Answer:** not isolated. C's whole client overhead over raw envelope bytes is 8% at baseline, which is an upper bound that includes feed framing and transport. With a 5 s interval under churn it is 4.2 times.
- **Prediction:** 1.2 to 2%.
- **Verdict:** untestable as asked. The interval trade-off is now the open parameter.

**Q14 Receipt cost.**
- **Answer:** not measured. C fetched receipts after the publish window, outside the byte counters.
- **Prediction:** 12 to 18% of feed bytes.
- **Verdict:** untestable.

**Q15 Time to `final` and window agreement.**
- **Answer:** not measured. No build first recomputes the root from its own inventory; all three fetch leaf lists.
- **Prediction:** 90 to 130 s, with local recomputation failing in more than 5% of windows.
- **Verdict:** untestable. The builders' design choice is consistent with the prediction.

**Q16 Ledger fallback.**
- **Answer:** p50 21.8 to 24.1 s, p99 25.0 to 36.2 s, and 9.0 to 10.3 kB of ledger bytes per Event against an arithmetic 9.2 kB. Blocks-to-clear and the 1,000 burst were not run. (DEC-008.)
- **Prediction:** p95 25 to 40 s; throughput within 15%.
- **Verdict:** latency right. Throughput untested, though bytes per Event agree within 12%.

**Q17 Idle Shards and P3.**
- **Answer:** not run. All builds set P3 and P3b to weight 0, as specified.
- **Prediction:** no penalty without per-topic P3.
- **Verdict:** untestable.

### Predictions that were wrong

- **IDONTWANT (Q5)** saves 70 to 76% of class-3 egress even in-process. The prediction said under 10%.
- **Mesh egress at the byte cap (Q4)** is about 0.6 Mbit/s median. The prediction said 3.5 to 4.
- **The poisoned-dial eclipse (Q3)** did not drop the victim below 0.5. The variant left two honest relays and both bootstrappers in its dial set, so it was not a full test.

### Results that were not predicted

1. **A custom protocol id silently turns off IDONTWANT in stock rust-libp2p.**
2. **A Busy Ignore is a permanent loss at that node**, and a builder's own delivery figures move by 34 points under host contention.
3. **The feed protocol, not the mesh, dominates both Subscriber download and the busiest node's egress.**
4. **A hard cap on the seen-set kills a Bus Node after about 1.8 hours.**
5. **The restart barrier's cost comes from silence, not from waiting.**

---

## Requirements to change

| Requirement | Change |
|---|---|
| MPE-NET-008 (and BUILD_BRIEF) | Name GossipSub v1.2: v1.1 scoring plus IDONTWANT. |
| MPE-NET-047 | Make IDONTWANT mandatory, with a threshold below the class-0 wire size (see P-NET-18). Per-class egress becomes a test-build measurement, since the stock API exposes none. |
| MPE-NET-006, MPE-NET-031 | Either allow the standard `/meshsub/1.2.0` protocol id, with network scope carried by topic names and the allow-list, or record a maintained fork plus an upstream change (`Version::V1_2` for custom ids) as a dependency. |
| MPE-ECO-022 | Replace "at most one Envelope per allowance network-wide" with: a per-Bus-Node bound; equivocation evidence gossiped to all Bus Nodes; revocation; and client-side keeping of at most one Envelope per visible nullifier. |
| MPE-ECO-020, MPE-SEC-018 | Conflicting second Envelope: Ignore plus evidence plus `AdmissionConflict` (DEC-014 (b)), never Reject. |
| MPE-NET-049 | A Bus Node shall answer the publish protocol with `Busy` or `Refused` for local, non-content reasons: queue full, rate limit, restart barrier, stale view. Silence remains for Reject and content Ignore. |
| MPE-STO-015 | Keep the 140 s barrier, and require the explicit refusal above while it is active. |
| MPE-SEC-009, MPE-PUB-014 | State that a gossip copy Ignored as Busy is lost at that node for the duplicate-cache time. Reconciliation from a second Operator is a client-library MUST, running from the first second after join, with an interval bound tied to the delivery target (see P-PUB-3). |
| MPE-PUB-015 | Repair by whole window (finding F5); "fetch that Envelope" conflicts with MPE-PUB-030. |
| MPE-CRY-004, MPE-FMT-037, MPE-FMT-051 | Adopt one carrier-compatible profile: header bytes 0-3 in the AEAD associated data; expiry fixed at creation + 172,800 s and authenticated through the EID, signature and admission. A variable lifetime requires a sealed expiry field. |
| MPE-CON-016, MPE-STO-042 | `final` and `stored` are determined per window from the anchorer's published leaf list and per-window receipts. A Subscriber never requests a per-EID path. Per-EID inclusion is a reaction-only tool. |
| MPE-NET-052 / anchorer | The anchorer shall serve the full leaf list for each window and Shard (`/anchor-leaves`) for the Anchor history period. |
| MPE-PRV-020 (L-L row), MPE-CRY-025 | The reaction transaction carries only the statement fields, the signature, the consumption nullifier and an optional inclusion path. Never a stream secret, event secret or Sealed Body. |
| MPE-FMT-046 | Add a verification case: one malformed group among valid groups must not block the valid groups. |
| MPE-FMT-040..046 (reader) | The reader shall drain every log entry of a block before reassembly. |
| New, protocol codec | All byte fields in RPC messages are encoded as CBOR byte strings. |
| New, gateway cost | Gateway bytes per delivered Envelope at most 1.2 times the wire size at baseline, excluding repair. |
| MPE-PRF-013, MPE-PRF-014 | Replace the 1.25 × D planning model with unique bytes × measured amplification. Budget feed and repair service separately from mesh traffic. |
| MPE-PUB-027, MPE-PRF-041 | The application seen-set shall hold every Accepted identifier until expiry + 60 s: 1.73 million per Shard at 10/s. Refusing new Accepts because a fixed-size set is full is forbidden. Verify with a full-retention fill, not a 60 s run. |
| MPE-NET-054, MPE-PUB-013 | Clients obtain Bus Node and Store Node addresses from the finalized Registry relay list and refresh them on change, so replacements are reachable. |
| MPE-NET-022 | Keep the application eviction rule. State that its verification needs at least 90 loaded heartbeats, or injected load. Fix the evicted score at −20 (not a graylisting value). |
| MPE-VER-041, MPE-VER-011 | Each gated result needs: runs isolated on the host; at least 5 seeds; runs long enough for time-based rules (eviction, pruning, barrier exit); and a stated attribution for every metric, for example gossip-path delivery separated from repair-path delivery in eclipse. |
| MPE-SEC-042 | Keep it. One run reproduced a loss with the EID id and none with the wire id. |

## Parameters to change

| Parameter | Reconciled value | Measured | Recommendation |
|---|---|---|---|
| IDONTWANT size threshold (P-NET-18) | 1,000 B | Class 0 (776 B, 61% of Envelopes) gets no saving: 1.17 vs 1.20 MB egress | Test 700 B against the control overhead of IDONTWANT per message, then set it below 776 B if it pays |
| Edge bandwidth (P-PRF-12) | 6 Mbit/s per direction | Mesh median about 0.6 Mbit/s; busiest node 3.3 Mbit/s at the byte cap (scaled); 5.7 Mbit/s at nominal load for a feed and repair server under churn with 5 s repair | Keep 6 Mbit/s for mesh. Add a separate feed-service budget or lower P-PUB-10. |
| Mesh (P-NET-1..4) | (8, 6, 12, 4) | +7 to 13% ingress over (6, 5, 12, 2) with IDONTWANT on; same eclipse result | Keep (8, 6, 12, 4); the cost argument against it is gone |
| Reconciliation interval (P-PUB-3) | 60 s | 60 s: churn p99 42.7 s. 5 s: p99 1.1 s at 4.2× gateway bytes | 10 to 15 s, or adaptive (short after a Busy or a source change). Measure overhead at each value. |
| Restart barrier (P-ECO-7) | 140 s | Silent: 0.816 delivery or 42.7 s p99. With Busy reply: p99 1.1 s | Keep 140 s; add the Busy reply |
| Feed cursor overlap (gateway, B) | Not specified | 2 s overlap on 1 s polls: 4.9× gateway bytes | Specify an exclusive cursor plus inventory repair instead of overlap |
| Seen-set capacity | Expiry + 60 s (P-STO-6 retired) | A 65,536 cap fails after about 1.8 h at 10/s | Size from P-PRF-34 (2 GiB): 1.73 M entries per Shard |
| Class table (P-FMT-1) | 4 classes | Class 3: 26 per minute at the baseline mix | Drop class 3 from the default table, or set a minimum class-3 share; re-run at the 50/s mix |
| Verification cost (P-PRF-14 basis) | 4.5 ms | 0.045 core at 10/s; 6 ms gives 0.061 core with no loss | No change; settle with a measured proof |
| Count ceiling (P-PRF-1) | 10/s | 50/s collapses on one shared host (42.1%) | Keep 10/s until one node per host is measured |

## Next experiments

1. **Trial decryption against the Tag.** Implement `--recognition trial`. Benchmark 1, 32 and 256 keys at 10 and 100/s, classes 0-3, on desktop and phone hardware. Settle DEC-003 at the key cap.
2. **Fully poisoned eclipse.** A victim whose dial sources and bootstrappers are all attacker-controlled. Add forged IHAVE without IWANT answers, injected link latency of 50 to 200 ms, and runs of at least 180 s so eviction can fire. Report gossip-path delivery separately from repair.
3. **IDONTWANT threshold.** At 500, 700 and 1,000 B, with IDONTWANT control bytes counted, at nominal and byte-cap loads.
4. **Churn matrix.** Busy reply on or off, against reconciliation at 5, 15 and 60 s, with Registry-driven address refresh, at 50 and 200 nodes over 240 s. Measure delivery within 10 s, repair share and gateway bytes.
5. **Stale chain overlay run.** `--ledger freeze` from T0 + 10 s and `skew:90`. Count P4 on honest peers and delivery.
6. **Idle Shards.** 8 Shards with all load on one, 300 s, P3 off against the default.
7. **One node per host, or a CPU-pinned node.** Find the per-node validation ceiling at 10, 20 and 50/s with a measured RLN or Groth16 verifier.
8. **Full-retention soak.** A Bus Node and a Store Node filled to 48 h of identifiers (1.73 M) at the byte cap. Measure the resident and on-disk multiplier, and pruning cost.
9. **Receipts and reconciliation overhead.** Count inventory, receipt and repair bytes separately, inside the measurement window. Compare a signed window root per Operator against per-EID receipts.
10. **Anchor timing and window agreement.** Time from publish to `final`, and the share of windows whose local recomputation matches the Anchor without a leaf list. Run 300 s.
11. **Equivocation spread.** Time until every node holds evidence, and Envelopes delivered per nullifier with client nullifier dedupe on and off, at 50 and 200 nodes.
12. **Ledger lane capacity.** A 1,000-Event burst. Measure blocks to clear and Events per block by class, against the 10% chain share.
13. **Repeat every gated scenario with seeds 1 to 5** in isolation, and report median and range.
