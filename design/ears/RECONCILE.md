# MPE requirements reconciliation

## Summary

- Input: 544 EARS requirements in twelve areas (CON 55, CRY 40, ECO 50, FMT 49, NET 47, OPS 54, PRF 40, PRV 37, PUB 52, SEC 40, STO 40, VER 40); 375 settled, 169 open; 13 fail `design/ears/lint.py`.
- Parameters: 53 reconciled parameter rows, each with one Prototype value and one production value.
- Duplicates: 89 groups; 114 requirements become "see canonical".
- Decisions: 28 register entries (DEC-001 to DEC-028); four of them (DEC-009, DEC-010, DEC-016, DEC-017) resolve contradictions that no single area recorded.
- Fixes: 56 corrected records: 21 replace the 13 lint failures, 9 rewrite untestable or vague requirements, 26 implement the parameter and decision choices. Two requirements are withdrawn (MPE-CON-007, MPE-CON-008).
- Gaps: 28 new records in 12 areas (CON, CRY, ECO, FMT, NET, OPS, PRF, PRV, PUB, SEC, STO, VER); 26 of them are needed for the Prototype to run end to end.
- All new and corrected records pass the `lint.py` checks (sentence, pattern, word count, weasel words, attributes).

Most consequential choices:

1. **GossipSub message id over all wire bytes (DEC-010).** The Envelope Identifier still excludes the Admission Slot for admission binding, deduplication and Anchors. rust-libp2p caches the message id before application validation and keeps it after Reject, so an id that excludes the slot lets one peer censor an honest Envelope by forwarding it with a corrupted slot first.
2. **Stale chain view (DEC-009).** The Bus Node keeps forwarding Envelopes valid under cached roots and never Rejects on chain- or clock-dependent checks. Staleness threshold 60 s; cached roots expire 25 h after their period starts.
3. **Wire format and load.** Bodies of 256 B, 1 KiB, 4 KiB and 16 KiB with a 512 B Admission Slot give wires of 776, 1,544, 4,616 and 16,904 B. The load is 10 Envelopes/s and 64 KiB/s per Shard on one launch Shard. The mesh is (8, 6, 12, 4), with an edge budget of 6 Mbit/s per direction.
4. **Admission quota (DEC-016, DEC-017).** Per-class limits (64, 16, 4, 1) per 60 s epoch with one nullifier per Envelope. Nullifier state stays in memory, and a 140 s restart barrier replaces durable commits.
5. **Lifetime and Anchors (DEC-004, DEC-024).** Lifetime equals ordinary retention at 48 h. Anchors are one per 60 s window covering all Shards. Live Anchor history is 49 h (2,940 records), because contracts reject expired Events.

Conventions. "See canonical X" means the requirement keeps its ID, its text is replaced by a pointer to X, and its parameters take X's values. Register decisions are DEC-001 onward; area decisions keep their own IDs (DEC-FMT-1 and so on) and are cited as proposers. Role IDs (g1-g4, o1-o4, s1-s4) refer to `design/rounds/r1` and `design/rounds/r2`. Midnight paths are relative to `/home/charl/midnight/`; libp2p paths to `/home/charl/libp2p/`.

## 1. Parameters

| Parameter | Prototype | Production | Reason | Requirement IDs to change |
|---|---|---|---|---|
| Size-class Sealed Body lengths (P-FMT-1) | 256, 1,024, 4,096, 16,384 B (classes 0-3) | Same table if the measured Admission Slot A is at most 1,024 B; if A exceeds 1,024 B, classes 1-3 only (1,024, 4,096, 16,384 B) | DEC-013. One table serves the overlay and the ledger carrier (1, 4, 16 and 64 Misc parts, MPE-FMT-041). The 256 B class keeps full-feed cost low (o3 R2, g3 R2). DEC-FMT-1's own trigger removes class 0 when admission overhead dominates it. PRF fixtures stated as '4 KiB complete Envelopes' map to class 2 (wire 4,616 B). | MPE-PRF-019, MPE-PRF-025, MPE-PRF-026, MPE-STO-034 |
| Admission Slot width A (P-FMT-2) | 512 B: epoch 8 B, membership root 32 B, nullifier 32 B, share y 32 B, proof 256 B (360 B), then zero fill | Measured length of the selected proof fields rounded up to a multiple of 64 B, at most 4,096 B (P-ECO-11), fixed per version | The Waku RateLimitProof carries a 256 B uncompressed (128 B compressed) proof and 32 B root, shares and nullifier (2021-vac-waku2-rln-relay-spec, RateLimitProof table); share x is recomputed from the Envelope Identifier (MPE-ECO-018), so it is not sent. s2's object-bound stamp is 354 B (2024-rfc9578-privacypass-issuance section 6.3, per P-FMT-2). 512 B fits both and leaves 152 B for a different proof encoding without changing the class table. Unused bytes must be zero (new MPE-FMT-050). | MPE-FMT-007, MPE-FMT-048, MPE-ECO-048 |
| Visible Header and wire length | 8 B fixed fields + 512 B Admission Slot = 520 B; wire 776, 1,544, 4,616, 16,904 B | 8 B + A; wire = 8 + A + class body | DEC-FMT-2 option (a). g1's 192 B, g2's 211 B and o4's 304 B headers are rejected with their visible tags, clues, member keys and msg_id. CRY's salt, nonce and Tag move to the clear prefix of the Sealed Body (new MPE-FMT-051), so the CRY-004 'pre-seal header' is the Network Identifier, header bytes 0-7 and that prefix. | MPE-CRY-004, MPE-CRY-005, MPE-CRY-013 |
| Payload capacity per class (default cryptographic profile) | 86, 854, 3,926, 16,214 B | Class body minus 170 B for the default profile; recomputed from MPE-CRY-036 for any other profile | Sealed Body = 44 B clear prefix (salt 16, nonce 12, Tag 16) + ciphertext. Plaintext = 40 B Sealed Prefix + 70 B authentication block (new MPE-CRY-041: key index 2, creation time 4, Ed25519 signature 64) + payload + zero padding; the AEAD adds 16 B. 256 - 44 - 16 - 40 - 70 = 86 B. DEC-FMT-7's 156 B figure assumed an X25519 key that the symmetric default does not carry and omitted the signature. | MPE-FMT-014, MPE-FMT-049 |
| GossipSub maximum transmit size (P-FMT-6, P-NET-8) | 65,536 B | 65,536 B | Largest wire is 16,904 B in the prototype and 20,488 B at A = 4,096 B. rust-libp2p default (rust-libp2p/protocols/gossipsub/src/protocol.rs:100). NET's allowed range up to 262,144 B serves only g2's 256 KiB class, which no area adopts. | MPE-NET-014, MPE-FMT-010 |
| Maximum Envelope lifetime L_max (P-FMT-3) | 172,800 s (48 h) | 172,800 s; hard ceiling 1,209,600 s (MPE-FMT-033) | DEC-004. g3, s1, s3 and s4 converge on 48 h; the ceiling is global_ttl (midnight-node/res/mainnet/ledger-parameters-config.json:176). PUB's L_max is this parameter. | MPE-PUB-003, MPE-PUB-004, MPE-PUB-041, MPE-NET-032 |
| Ordinary retention (P-STO-1) and retention deadline | Retention deadline = visible expiry, at most P-FMT-3 + P-FMT-4 after arrival | Same; optional paid archive up to 604,800 s (P-STO-7) | A Store Node sees no creation time: it is signed inside the seal (MPE-CRY-021) and the Visible Header carries only expiry (MPE-FMT-003). STO-003 as written cannot be evaluated by a Store Node. | MPE-STO-003, MPE-STO-004 |
| Expiry clock tolerance (P-FMT-4; replaces P-PUB-8 in delivery rules) | 60 s | 60 s | The same expired-on-arrival check carried 60 s (MPE-FMT-030) and 120 s (MPE-PUB-029). 60 s exceeds normal NTP error; chain-view staleness has its own threshold (P-NET-13). P-PUB-8 is retired. | MPE-PUB-003, MPE-PUB-004, MPE-PUB-027, MPE-PUB-029, MPE-PUB-041 |
| Chain-view staleness threshold (P-NET-13; absorbs P-FMT-5 and P-OPS-10) | 60 s | 60 s | Three definitions existed: clock against latest finalized block above 120 s (FMT-031, NET-019), Registry lag above 60 s (OPS-022) and 'newest root older than P-ECO-5 = 3,600 s' (ECO-024). After DEC-009 a stale view only turns chain-dependent Reject into Ignore and keeps cached-valid forwarding, so an early trigger costs little. 60 s is 10 slots of 6 s (midnight-node/runtime/src/lib.rs:292) and more than three times the 18 s finality (notes/midnight-network-stack.md section 1.7). | MPE-FMT-031, MPE-NET-019, MPE-OPS-022, MPE-ECO-024 |
| Membership-root acceptance window (P-ECO-5) | 3,600 s counted from the root's supersession; the current root is always eligible | Same | ECO-015 counts from publication, so a Registry with no registration for one hour would make every Envelope Ignore. Supersession time is recorded alongside publication time (MPE-ECO-027, new MPE-NET-055). | MPE-ECO-015 |
| Stale-root bound (P-ECO-4 + P-ECO-5) | 25 h | 25 h | Bounds forwarding under a cached root while the chain view is stale (DEC-009): a root becomes ineligible P-ECO-5 after the membership period it serves ends (new MPE-ECO-051). 86,400 s + 3,600 s = 90,000 s. | MPE-NET-038, MPE-SEC-035 |
| Admission epoch and tolerance (P-ECO-1, P-ECO-6) | 60 s; 20 s | 60 s; 20 s | DEC-ECO-5 (o1, o2, o4). The publish retry budget P-PUB-5 x P-PUB-6 = 5 s x 3 = 15 s stays inside the 20 s tolerance, so identical retransmissions started in an epoch's last second remain admissible; new MPE-PUB-053 stops retries beyond that. | none (values agree) |
| Nullifier retention and restart barrier (P-ECO-7) | 140 s | 140 s | 2 x 60 s + 20 s. An allowance is permanently ineligible 80 s after its epoch ends, at most 140 s after acceptance. Refusing live admission for 140 s after each start (DEC-017) restores the replay invariant without a disk write on the forwarding path. SEC-017 and STO-014 state the same bound without a number. | MPE-SEC-015, MPE-SEC-016, MPE-STO-014, MPE-STO-015 |
| Membership period (P-ECO-4) | 86,400 s (mock Registry) | 86,400 s | Daily renewal costs about 0.1 DUST/day against 2.4 for hourly renewal (g3). Ceiling: 10% of 1,000,000 blockUsage bytes per block (ledger-parameters-config.json:158) over 14,400 blocks/day is 1.44 GB/day; at the 16 KiB registration gate (P-ECO-13) that is 1,440,000,000 / 16,384 = 87,890 registrations per day before Anchors. | none (values agree) |
| Lowest-tier publication quota (P-ECO-2, P-ECO-3) | Per-class limits (64, 16, 4, 1) Envelopes per epoch for classes 0-3, committed in the membership leaf; one nullifier per Envelope | Same vector; an exact 64-credit byte debit (credit = 256 B of body) only if a multi-nullifier circuit passes P-ECO-11 and P-ECO-12 | DEC-016. P-ECO-2 = 10 credits is below the class-3 weight of 64 (P-ECO-3), so ECO-017 as written forbids class 3 to the lowest tier, and it needs up to 64 nullifier and share pairs per Envelope, which one fixed Admission Slot cannot hold. The vector gives 16,384 B of body per class per epoch (273 B/s): 240 single-class memberships, or 60 using all four classes, saturate one 64 KiB/s Shard. | MPE-ECO-016, MPE-ECO-017, MPE-ECO-022, MPE-ECO-050 |
| Per-Shard capacity (P-PRF-1, P-PRF-2, P-VER-2) | 10 Envelopes/s and 64 KiB/s per Shard, whichever binds first | Same | DEC-005. At 10/s the byte cap binds above a mean wire size of 6,553.6 B; with prototype wire sizes class 3 alone binds at 65,536 / 16,904 = 3.88 Envelopes/s. | MPE-PRF-006 |
| Comparison and burst loads (P-PRF-28, P-PRF-29, P-VER-4, P-VER-5, P-VER-9, P-VER-10) | 50 Envelopes/s for 24 h as a comparison; 100 Envelopes/s per Shard for 60 s as a burst | Not capacity targets | g1's normalized mix (847.7 B mean) at 50/s is 41.39 KiB/s, inside the byte cap and above the count cap; the run decides whether the count ceiling can rise (DEC-005). | none (values agree) |
| Shard count (P-PUB-1, P-NET-9) | 1 operating; 8 in the benchmark topology (P-PRF-3) | 1 at launch; allowed range 1-8 | DEC-011. Nine Round 2 votes favour one feed (DEC-PUB-1). P-PUB-1 allowed 1-16 and P-NET-9 1-8; no proponent of 16 Shards (o1, o2) remains after Round 2. | MPE-PUB-002 |
| Mesh tuple D, D_lo, D_hi, D_out (P-NET-1..4, P-PRF-4, P-SEC-1) | (8, 6, 12, 4); (6, 5, 12, 2) as mandatory comparison | (8, 6, 12, 4) | DEC-012. The prototype gates include a 20% cold-start Sybil attack (MPE-PRF-032, MPE-VER-018) and an outbound quota of 4 (MPE-SEC-003); (8, 6, 12, 4) is the profile evaluated under Sybil cold start (2020-vyzovitis-gossipsub). It satisfies D_out < D_lo and D_out <= D/2 (specs/pubsub/gossipsub/gossipsub-v1.1.md:192). | MPE-PRF-010, MPE-SEC-003 |
| Heartbeat, gossip factor, prune backoff, flood publishing | 1 s, 0.25, 60 s, off | 1 s, 0.25, 60 s, off | Consistent across NET, PRF and SEC. Flood publishing off departs from the specification default (specs/pubsub/gossipsub/gossipsub-v1.1.md:549; rust-libp2p/protocols/gossipsub/src/config.rs:548). | none (values agree) |
| Edge Bus Node bandwidth (P-PRF-12) | At most 6 Mbit/s egress and 6 Mbit/s ingress at one Shard's byte cap | Same | g3's planning model is egress: 1.25 x D x 64 KiB/s (g3 R1 D5: '1.25 x 6 x 64 KiB/s = 480 KiB/s, about 3.9 Mbit/s'). With D = 8: 1.25 x 8 x 65,536 B/s x 8 bit = 5.24 Mbit/s, which breaks the 4 Mbit/s figure. Ingress carries the same duplicates. A per-direction budget settles DEC-PRF-4's direction question. | MPE-PRF-013 |
| Full Bus Node bandwidth (P-PRF-13) | At most 24 Mbit/s per direction with 4 Shards at their byte caps | Same | 4 x 5.24 = 20.97 Mbit/s planning egress plus headroom; g3's 16 Mbit/s was its D = 6 egress model. | MPE-PRF-014 |
| Bus Node CPU (P-PRF-14, P-PRF-15) | 0.30 core edge; 2 cores full | Same | 10 Envelopes/s x 4.5 ms Groth16 verification on a 4-vCPU VM (2024-revuelta-waku-latency Table 1) is 0.045 core per Shard; at the P-ECO-12 gate of 10 ms it is 0.10 core, inside 0.30. | none (values agree) |
| Bus Node memory ceiling (new P-PRF-34) | 2 GiB resident | 2 GiB resident | MPE-VER-015 cannot pass without a ceiling. Application seen-set at one Shard: 10/s x 172,860 s = 1.73 million identifiers x about 72 B = 124 MB; 4 Shards about 0.5 GB, inside P-STO-4 = 1 GiB; plus 1 GiB for process, GossipSub caches and queues (P-SEC-4 x 16,904 B = 2.2 MB). New MPE-PRF-041. | MPE-VER-015 |
| Bus Node application seen-set retention (MPE-PUB-027, P-STO-6) | Expiry + P-FMT-4 (60 s) | Same | A Bus Node Ignores anything whose expiry is earlier than its clock minus P-FMT-4 (MPE-FMT-030), so longer retention protects nothing. P-STO-6 (+3,600 s) and P-PUB-8 (+120 s) disagreed; P-STO-6 is retired. | MPE-PUB-027, MPE-STO-013 |
| Client deduplication retention (P-CON-2) | Expiry + 3,600 s | Same | Clients receive back-fill pages up to P-STO-2 after expiry and apply no expiry gate before recognition; one hour covers client clock error. | none (values agree) |
| Recognition key cap (P-CRY-4, P-PUB-4, P-CON-7) | 256 keys; allowed range 1-256 | Same | Same default in three files; PUB and CON ranges up to 4,096 exceed CRY's bound. Cost at the cap: 256 keys x 10 Envelopes/s = 2,560 HMAC-SHA-256 evaluations per second. | MPE-PUB-018, MPE-CON-009 |
| Tag and salt (P-CRY-2, P-CRY-3; withdraws P-CON-5, P-CON-6) | 16 B Tag and 16 B salt in the Sealed Body clear prefix | Same | DEC-003. Salted per-Envelope Tags make the expected-Tag lookahead window and the recognition-window gap unnecessary. | MPE-CON-007, MPE-CON-008, MPE-PUB-005 |
| Sequence-gap wait (P-PUB-7; withdraws P-CON-1) | 120 s | 120 s | A missing Envelope is repaired by reconciliation every 60 s (P-PUB-3) plus delivery within 10 s (P-VER-6): 70 s. CON's 60 s would emit gap items that the next reconciliation fills. | MPE-CON-020 |
| Reconciliation interval and independent sources (P-PUB-3, P-CON-4, P-CON-3, P-SEC-2) | 60 s; 2 sources from distinct mock Operators | 60 s; 2 sources from distinct Operators | Inventory at 10/s: 600 identifiers x 32 B = 19,200 B per minute, 27.6 MB/day, 1.6% of a 1.77 GB/day feed (DEC-PUB-4). Priority conflict resolved by DEC-025. | MPE-PUB-014, MPE-CON-036, MPE-CON-037, MPE-SEC-021 |
| Full-Shard streams per Bus Node (P-PUB-10, P-PRF-17) | 4 per Bus Node; 500 per gateway (P-PRF-18) | Same | At the byte cap one stream is 0.524 Mbit/s; 8 streams need 4.19 Mbit/s on top of 5.24 Mbit/s mesh egress. MPE-PRF-036 still refuses streams beyond remaining bandwidth. | MPE-PUB-033 |
| Per-peer pre-verification rate (P-ECO-10, P-NET-10) | 20 Envelopes/s per peer per Shard | Same | A per-peer total starves Full Bus Nodes: a mesh peer on 4 Shards at capacity forwards up to 40 Envelopes/s. 20/s per Shard is twice the Shard cap. | MPE-NET-023, MPE-ECO-023 |
| Verification queues (P-SEC-3, P-SEC-4) | 8 jobs per peer; 128 total | Same | 128 x 16,904 B = 2.2 MB; at 4.5 ms per proof a full queue drains in 0.58 s, below the 3 s p99 target. | none (values agree) |
| Publisher retry (P-PUB-5, P-PUB-6) | 5 s; 3 Bus Nodes | Same | 15 s total, inside the 20 s epoch tolerance (P-ECO-6) and above the 3 s propagation p99. | none (values agree) |
| Latency gates (P-PRF-10, P-PRF-11, P-VER-6, P-VER-7, P-VER-21..23) | Post-admission delivery p99 at most 10 s and at least 99.9% of eligible pairs within 10 s; warm propagation p50 1.5 s and p99 3 s recorded, a miss triggers MPE-PRF-011 | Warm propagation p50 at most 1.5 s and p99 at most 3 s; canary delivery at least 99.9% within 5 s for 30 consecutive days | DEC-PRF-3 and DEC-VER-2. The prototype carries unmeasured admission costs, so g3's 3 s target is recorded rather than gated; production adopts it with o4's canary window. MPE-PRF-007 and MPE-PRF-023 receive the 10 s deadline they lacked. | MPE-PRF-007, MPE-PRF-023 |
| Attack thresholds (P-PRF-22..24, P-VER-25, P-OPS-5) | 20% cold-start Sybil: at least 99% delivery and completed p99 at most 6 s; failure at 200 nodes triggers MPE-PRF-038 | Open-admission red team at 1:1 Sybil identities: canary delivery at least 99.9% (P-OPS-5) | MPE-VER-040 used 99% and MPE-OPS-008 used 99.9% for the same gate. Removing a safety restriction takes the stricter value, which equals the canary SLO. | MPE-VER-040 |
| Adversarial fractions (P-SEC-6, P-PRV-1, P-VER-11, P-VER-12, P-PRF-22) | Placements 1, 3, 5, 20%; first-spy coalitions 1, 3, 5, 10, 20% | Same sets for the red team | Union of the five sets; DEC-NET-6 asks for a 10% spy run. | MPE-PRV-033 |
| Soak duration (P-PRF-25, P-VER-3) | 72 h at 10 Envelopes/s per Shard | Replaced by the 30-day canary window | A Store Node reaches steady-state storage only after one 48 h retention window; 72 h = 48 h fill + 24 h of pruning at steady state. P-PRF-25 said 48 h. | MPE-PRF-037 |
| Topology sizes (P-VER-1, P-PRF-9, P-VER-8) | 32 local Bus Node processes for reference runs (at least 16 for MPE-VER-011); simulations at 50, 200 and 1,000 | Not applicable | P-PRF-9 reference conditions use 32 Bus Nodes per Shard; 32 satisfies VER's minimum of 16. | MPE-VER-011 |
| Store Node allocation (P-STO-3) and Bus Node caches (P-STO-4) | 32 GiB per retained Shard; 1 GiB | Same | Byte cap x 48 h = 65,536 x 172,800 = 11,324,620,800 B = 10.55 GiB raw; 21.1 GiB at the assumed 2x database multiplier. | none (values agree) |
| Distinct Operators for 'stored' (P-STO-5) | 3 mock Operators (new MPE-OPS-055) | 3 | MPE-STO-012 is a POC MUST and cannot execute without Operator diversity in the mock roster. | none (values agree) |
| Anchor window and granularity (P-NET-17) | 60 s; one Anchor per non-empty window covering every Shard | Same | DEC-024. NET-041 (one per Shard per window) and STO's record bound (one per window) differ by the Shard count. A combined payload (8 B window, 32 B root, 4 B count per Shard = 72 B at 8 Shards) fits the 256 B Misc payload (MPE-FMT-047). Cost: 1,440 Anchors/day; at the 8 KiB transaction assumed in DEC-PRF-6, 11.8 MB/day = 0.08% of 14.4 GB/day blockUsage. | MPE-NET-041 |
| Live Anchor history (P-STO-9, P-STO-10) | 176,400 s (49 h); 2,940 records | Same | Consumption rejects expired Events (MPE-CON-046), so no contract needs a root older than L_max; 1 h margin. 49 h x 60 windows per hour = 2,940. o4's 7 days and o2's 14 days assumed 7- to 14-day lifetimes. | MPE-STO-028, MPE-STO-029 |
| Unanchored wait (P-CON-8) | 300 s | 300 s | 60 s window + 6 s inclusion + about 18 s finality + indexing, with margin. | none (values agree) |
| Tombstone deadline (P-SEC-5, P-STO-14, P-OPS-13) | Feature disabled | 24 h | DEC-018. With 48 h retention a 48 h deadline never removes a body before ordinary expiry; 24 h is inside all three allowed ranges. | MPE-SEC-034, MPE-STO-036, MPE-OPS-025, MPE-OPS-026 |
| Version overlap (P-FMT-9, P-OPS-19) | Not applicable (single version) | 2 x 172,800 s + 30 days = 34 days | Identical definitions; MPE-OPS-035 becomes see canonical MPE-FMT-024. | MPE-OPS-035 |
| Bootstrappers (P-OPS-3, P-NET-11, P-SEC-2) | 2 local bootstrappers from 2 mock Operators | 4, each run by a distinct Operator | NET-025 already requires distinct Operators; this satisfies SEC's minimum of 2. | MPE-OPS-003, MPE-SEC-002 |
| Launch relay roster (P-OPS-1, P-OPS-2) | Mock roster of at least 3 organizations | At least 8 organizations; at most 20% of listed relays each | DEC-OPS-6; s1 and o4 R2 back 8 organizations. | none (values agree) |
| Chain-share budget (P-ECO-8) | Not applicable (mock ledger) | 10% of blockUsage, 24 h mean, enforced by client back-off | Anchors at 60 s use 0.08%; the remainder bounds registrations (87,890 per day at 16 KiB). | none (values agree) |
| Skipped-key retention (P-CRY-7) | Not applicable (no ratchet) | 172,800 s; 604,800 s only where an archive profile is enabled | Keys need to outlive only the ciphertext the client can still fetch; shorter retention narrows compromise exposure (2016-signal-double-ratchet-spec section 8.4). | MPE-CRY-030 |
| Bond and deposit amounts (P-ECO-14..17) | None | None at launch; if enabled, amount set from the MPE-ECO-050 flood cost, withdrawal delay 7 days, reporter share at most 10% | DEC-007: revocation is the launch deterrent; contract-held NIGHT on mainnet is unknown. | MPE-OPS-014 |
| Admission gates (P-ECO-11, P-ECO-12, P-ECO-13) | Proof fields at most 4,096 B; verification at most 10 ms on one core of a 4-vCPU VM | Same, plus registration at most 16 KiB and 0.5 DUST | Consistent across ECO, FMT and OPS. | none (values agree) |
| Chaos, race and usability fixtures (P-VER-13/P-CON-10, P-VER-17/P-CON-12, P-VER-18..20/P-CON-13) | 1,000,000 Events; 100 reactors; 4 of 5 developers within 4 h | Same | Identical values; the CON copies become see canonical. | MPE-CON-034, MPE-CON-049, MPE-CON-055 |

### 1.1 Derived arithmetic

**Envelope sizes (Prototype, A = 512 B).** Wire = 8 + A + body. Payload = body - 44 (salt 16, nonce 12, Tag 16) - 16 (AEAD tag) - 40 (Sealed Prefix) - 70 (authentication block).

| Class | Body (B) | Wire (B) | Payload (B) | Misc parts | Envelopes/s at the 64 KiB/s cap |
|---|---|---|---|---|---|
| 0 | 256 | 776 | 86 | 1 | 10.00 |
| 1 | 1,024 | 1,544 | 854 | 4 | 10.00 |
| 2 | 4,096 | 4,616 | 3,926 | 16 | 10.00 |
| 3 | 16,384 | 16,904 | 16,214 | 64 | 3.88 |

At 10 Envelopes/s the byte cap binds once the mean wire size exceeds 65,536 / 10 = 6,553.6 B. At A = 4,096 B (the P-ECO-11 gate) class-0 wire would be 4,360 B, 94% admission overhead, which is the DEC-013 trigger to drop class 0.

**Mesh bandwidth (g3's planning model, egress = 1.25 x D x unique bytes/s).** At the byte cap (65,536 B/s): D = 6 gives 491,520 B/s = 3.93 Mbit/s; D = 8 gives 655,360 B/s = 5.24 Mbit/s. A lower bound counting D - 1 forwards with no control traffic is 7 x 65,536 x 8 = 3.67 Mbit/s for D = 8. Ingress carries the same duplicates. Full Bus Node with 4 Shards: 4 x 5.24 = 20.97 Mbit/s per direction. One full-Shard stream at the cap: 65,536 x 8 = 0.524 Mbit/s.

**Subscriber download.** One Shard at the byte cap: 65,536 x 86,400 = 5.66 GB/day. At 10 class-1 Envelopes/s: 10 x 1,544 x 86,400 = 1.33 GB/day. At s4's planning load (10 x 2 KiB): 1.77 GB/day. Reconciliation adds 600 x 32 B per minute = 27.6 MB/day.

**Storage.** Store Node raw bytes per Shard over 48 h at the byte cap: 65,536 x 172,800 = 11,324,620,800 B = 10.55 GiB; 21.1 GiB at a 2x multiplier, inside P-STO-3 = 32 GiB. Bus Node application seen-set: 10/s x (172,800 + 60) s = 1,728,600 identifiers per Shard, about 124 MB at 72 B each; about 0.5 GB for a 4-Shard Full Bus Node, inside P-STO-4 = 1 GiB. Nullifier cache: 10/s x 140 s = 1,400 entries per Shard.

**Chain budget.** blockUsage limit 1,000,000 B per 6 s block (`midnight-node/res/mainnet/ledger-parameters-config.json:158`, `midnight-node/runtime/src/lib.rs:292`) = 14.4 GB/day; a 10% MPE share is 1.44 GB/day. Anchors at 60 s: 1,440 per day x 8,192 B (DEC-PRF-6 assumption) = 11.8 MB/day = 0.08%. Registrations at the 16 KiB gate: 1.44 GB / 16,384 B = 87,890 per day. Anchor state at the live bound: 2,940 records.

**Admission quota.** Lowest tier: 16,384 B of body per class per 60 s epoch = 273 B/s per class. Single-class use: 65,536 / 273 = 240 memberships saturate one Shard; all four classes: 60. RLN fields in the slot: 8 + 32 + 32 + 32 + 256 = 360 B of 512 B.

**Timing chains.** Publish retries 3 x 5 s = 15 s, inside the 20 s epoch tolerance. Gap wait 120 s, above the 70 s repair path (60 s reconciliation + 10 s deadline). Restart barrier 140 s, below the 600 s warm-up before local injection. Unanchored wait 300 s, above 60 s window + 6 s inclusion + 18 s finality. Stale-root bound 86,400 + 3,600 = 90,000 s.

**Retired parameters.** P-PUB-8 (replaced by P-FMT-4), P-FMT-5 and P-OPS-10 (replaced by P-NET-13), P-STO-6 (seen-set retention is expiry + P-FMT-4), P-CON-1 (replaced by P-PUB-7), P-CON-5 and P-CON-6 (DEC-003). New: P-PRF-34 = 2 GiB.

## 2. Duplicates

| Obligation | Canonical | See canonical | Note |
|---|---|---|---|
| Sealed Body length fixed per size class | MPE-FMT-013 | MPE-PRV-005 |  |
| Padding inside the authenticated encryption | MPE-FMT-016 | MPE-CRY-003 |  |
| Only the Visible Header fields are cleartext; logical labels sealed | MPE-FMT-003 | MPE-PRV-003, MPE-PUB-001 | MPE-CRY-002 stays as the positive list of sealed fields. |
| StrictNoSign carriage without from, seqno, signature, key | MPE-NET-009 | MPE-FMT-012 | Canonical split into MPE-NET-009a/b. |
| GossipSub message identifier | MPE-NET-010 | MPE-FMT-019, MPE-PUB-026 | Rewritten per DEC-010. |
| GossipSub transmit-size cap | MPE-NET-014 | MPE-FMT-010 | P-FMT-6 = P-NET-8 = 65,536 B. |
| Application validation before forwarding | MPE-NET-015 | MPE-PUB-051 |  |
| Structural checks before cryptographic work | MPE-FMT-009 | MPE-SEC-006 | MPE-ECO-013 keeps the admission-specific order. |
| Reject on proven invalidity independent of chain state | MPE-NET-016 | MPE-SEC-007 |  |
| Ignore, never Reject, while the chain view is stale | MPE-NET-018 | MPE-SEC-008, MPE-ECO-024, MPE-OPS-022 | Rewritten per DEC-009. |
| Expired on arrival yields Ignore | MPE-FMT-030 | MPE-PUB-029 | Tolerance P-FMT-4. |
| Duplicate yields Ignore | MPE-PUB-028 | MPE-NET-017, MPE-ECO-019 | MPE-NET-017 rewritten to drop the unknown-version case (DEC-015). |
| Application seen-set retention | MPE-PUB-027 | MPE-STO-013 | Retention expiry + P-FMT-4. |
| Per-peer rate limit before verification | MPE-NET-023 | MPE-ECO-023 | Per peer per Shard. |
| Store Node refuses storage beyond its cap | MPE-STO-009 | MPE-SEC-012 | Outcome name StorageExhausted (MPE-CON-056). |
| Bus Node refuses work beyond its queue or ingress cap | MPE-PRF-034 | MPE-ECO-044 |  |
| No key, Tag filter or selector sent to infrastructure | MPE-PUB-010 | MPE-CON-001, MPE-CRY-015, MPE-PRV-008 | MPE-PRV-007 stays (wider secret boundary). |
| Whole-Shard reception by default | MPE-PUB-011 | MPE-CON-002 |  |
| Network behaviour independent of recognition | MPE-PUB-012 | MPE-PRV-009, MPE-CON-003, MPE-SEC-025 |  |
| No network action on recognition | MPE-CON-039 | MPE-PRV-010 | MPE-FMT-036 stays (no receipt kind). |
| Back-fill requested as complete Shard intervals | MPE-STO-017 | MPE-CON-029 |  |
| Back-fill returns every held Envelope of the window | MPE-PUB-031 | MPE-STO-018 |  |
| Second-source inventory reconciliation | MPE-PUB-014 | MPE-SEC-021, MPE-CON-037 | Priority raised to MUST (DEC-025). |
| Repair every missing identifier | MPE-PUB-015 | MPE-SEC-023 |  |
| Reduced-privacy profiles only on explicit opt-in | MPE-PUB-016 | MPE-CON-004 |  |
| No silent privacy-changing fallback | MPE-PRV-013 | MPE-SEC-026, MPE-CON-005, MPE-PRV-012 |  |
| Private membership only by invitation | MPE-PUB-008 | MPE-CON-006 | MPE-CRY-018 stays (invitation authentication). |
| Random private stream secrets | MPE-CRY-008 | MPE-PUB-006 | Audience key (PUB) and stream secret (CRY) are one object. |
| Recognition key cap | MPE-CRY-016 | MPE-PUB-018, MPE-CON-009 | Outcome KeyLimit. |
| Salted per-Envelope Tag | MPE-CRY-013 | MPE-PUB-005 | MPE-CON-007 and MPE-CON-008 withdrawn (DEC-003). |
| Logical Event Identifier stable across carriers and retries | MPE-FMT-022 | MPE-PUB-020 |  |
| At most one delivery per publisher and logical identifier | MPE-PUB-037 | MPE-CON-014, MPE-CRY-024 |  |
| At most one delivery per Envelope identifier | MPE-PUB-036 | MPE-CON-013 | Client retention expiry + P-CON-2. |
| At-least-once delivery within retention | MPE-PUB-035 | MPE-CON-012 | Canonical rewritten with a testable condition. |
| Arrival-order delivery without hidden buffering | MPE-PUB-038 | MPE-CON-022 |  |
| Sequence-gap item | MPE-PUB-039 | MPE-CON-020 | Wait P-PUB-7 = 120 s. |
| Late-fill item | MPE-PUB-040 | MPE-CON-021 |  |
| Caught-up head item | MPE-PUB-042 | MPE-CON-024 |  |
| Portable inclusive cursor | MPE-PUB-043 | MPE-CON-027 | MPE-CON-028 stays (resume behaviour). |
| Retention gap item | MPE-PUB-045 | MPE-CON-032 |  |
| Key-erased gap item | MPE-PUB-046 | MPE-CON-031, MPE-STO-026 | MPE-CON-031's forward-secrecy rationale is void under DEC-002. |
| Atomic processOnce helper | MPE-CON-033 | MPE-PUB-044 |  |
| Unknown schema delivered as undecodable | MPE-PUB-049 | MPE-FMT-026, MPE-CON-011 |  |
| Static schema-keyed decoder dispatch | MPE-FMT-027 | MPE-CON-010 |  |
| Reactions only on explicit application call | MPE-PUB-047 | MPE-PRV-011 |  |
| External object fetch only on explicit call | MPE-FMT-038 | MPE-PUB-048, MPE-CON-041 | MPE-SEC-032 stays (command execution). |
| Oversize payload refused before admission | MPE-FMT-015 | MPE-PUB-021 | Outcome TooLarge. |
| Identical-byte retransmission | MPE-PUB-023 | MPE-CRY-012 |  |
| Admission secret separate from other keys | MPE-ECO-006 | MPE-SEC-029 |  |
| Nullifier and replay-state retention | MPE-ECO-021 | MPE-SEC-017, MPE-STO-014 | P-ECO-7 = 140 s. |
| Refuse live admission until replay state is safe | MPE-STO-015 | MPE-SEC-016 | Rewritten per DEC-017; MPE-SEC-015 becomes optional. |
| Continue relaying during ledger interruption or pause | MPE-NET-038 | MPE-SEC-035, MPE-OPS-021, MPE-ECO-025 | MPE-CON-051 stays (client side). |
| Typed ledger-paused outcome | MPE-CON-050 | MPE-SEC-036 | BusPaused and LedgerPaused stay distinct (MPE-CON-056). |
| No MPE duty on block-authoring nodes | MPE-OPS-001 | MPE-NET-004 |  |
| Distinct Bus Node identity key | MPE-NET-005 | MPE-OPS-002 |  |
| Separate MPE bootstrap set | MPE-NET-025 | MPE-OPS-003 |  |
| Authenticated bootstrap list | MPE-NET-026 | MPE-SEC-002 |  |
| Bootstrapper profile | MPE-NET-024 | MPE-OPS-004 |  |
| Outbound mesh quota | MPE-NET-011 | MPE-SEC-003 |  |
| Peer scoring active | MPE-NET-008 | MPE-SEC-004 |  |
| Relay allow-list at launch | MPE-OPS-007 | MPE-SEC-001, MPE-NET-034 |  |
| Allow-list removal red team | MPE-OPS-008 | MPE-VER-040 | Threshold P-OPS-5 = 99.9%. |
| CVE-2022-47547 regression gate | MPE-VER-026 | MPE-SEC-040, MPE-OPS-047 | MPE-NET-022 stays (eviction property). |
| Version overlap window | MPE-FMT-024 | MPE-OPS-035 |  |
| Bus Node Shard-count transition | MPE-PUB-003 | MPE-NET-032 | MPE-PUB-004 stays (client side). |
| Tombstone deletion deadline | MPE-STO-036 | MPE-SEC-034, MPE-OPS-025 | Disabled in the Prototype (DEC-018). |
| No client IPs in persistent logs | MPE-SEC-027 | MPE-OPS-029 |  |
| Claim register | MPE-PRV-001 | MPE-VER-002 |  |
| Paired interest-swapped transcripts | MPE-VER-028 | MPE-PRV-031, MPE-PRV-032 |  |
| Source-attribution measurement | MPE-VER-027 | MPE-PRV-033 |  |
| Independent review before production | MPE-VER-037 | MPE-CRY-040 | MPE-OPS-048 stays (allow-list gate). |
| Cryptographic size and cost report | MPE-CRY-036 | MPE-VER-006 |  |
| Admission Proof size and verification measurement | MPE-ECO-048 | MPE-FMT-048 |  |
| Measured ledger transaction costs | MPE-VER-030 | MPE-OPS-046 | MPE-ECO-049 stays (production gate). |
| Mockable Ledger Adapter for the Prototype | MPE-NET-035 | MPE-OPS-045, MPE-ECO-047 |  |
| No Midnight transaction per overlay Event | MPE-NET-002 | MPE-ECO-003 |  |
| Recovery chaos workload | MPE-VER-023 | MPE-CON-034 |  |
| Concurrent reactor race | MPE-VER-032 | MPE-CON-049 |  |
| Outside-developer usability trial | MPE-VER-036 | MPE-CON-055 |  |
| Bounded model of client delivery | MPE-VER-008 | MPE-CON-035 |  |
| Pause-to-resume drill | MPE-OPS-041 | MPE-VER-039 |  |
| Production canary gate | MPE-VER-038 | MPE-OPS-049 |  |
| In-circuit publisher authorization | MPE-CON-043 | MPE-SEC-037 | MPE-CRY-021 stays (signed statement content). |
| Atomic contract replay protection | MPE-CON-044 | MPE-SEC-038 | Canonical split into MPE-CON-044a/b. |
| Secret-bearing consumption nullifier | MPE-CRY-025 | MPE-CON-045 |  |
| Session state changes only after authentication | MPE-CRY-023 | MPE-SEC-030 |  |
| Subscriber download measurement | MPE-PRF-021 | MPE-PUB-052 | MPE-CON-054 stays (runtime metering API). |
| Full-Shard stream concurrency | MPE-PRF-022 | MPE-PUB-033 |  |
| Acyclic Envelope construction order | MPE-FMT-020 | MPE-CRY-005 | CRY's 'admission content commitment' is the Envelope Identifier; its 'final wire identifier' is the GossipSub message id (DEC-010). |

## 3. Decision register

### DEC-001 Who pays relays and other Operators

- **Options and proponents:**
  - (a) No protocol payment to anyone - g1, g2, g3, g4, o3; DEC-ECO-3(a), DEC-OPS-3(a)
  - (b) Off-protocol contracts for relays, gateways and issuers - s1, s2, s3, s4; DEC-ECO-3(b), DEC-OPS-3(b)
  - (c) Registry treasury paying only contract-checkable work (Anchors, passed retention challenges) - o2; DEC-ECO-3(c), DEC-OPS-3(d), DEC-STO-5 (bonded challenges)
  - (d) Pool paid on multi-monitor probe scores - o4; DEC-ECO-3(d), DEC-OPS-3(c)
- **Prototype default:** (a): no payment code; MPE-ECO-037 and MPE-ECO-038 hold.
- **Production default:** Relays are never paid by the protocol. Launch Operators are funded by written off-protocol commitments covering 12 months (MPE-OPS-051). Option (c) is an optional later feature behind the MPE-ECO-034 invariants. Option (d) is rejected.
- **Reason:** DUST is shielded and non-transferable and no code path credits fees to anyone (midnight-node/runtime/src/lib.rs:691,695 return (0, None); MPE-ECO-002). Relay quality is not checkable by a contract, and score attacks cut the cost of dominating a paid active set by over 99% (2026-cao-nymreputation, as cited in MPE-ECO-038 and MPE-OPS-034).
- **Settled by:** o2's economic simulation showing at least 12 months of treasury runway with no grant draw; written Operator bids (s1 D4); procurement showing 8 organizations will sign (DEC-OPS-6).

### DEC-002 Forward secrecy posture

- **Options and proponents:**
  - (a) No forward-secrecy claim at launch; symmetric stream secrets - g1, g2, g3, g4; DEC-PRV-4, DEC-CRY-1 recommended
  - (b) Per-epoch hash progression of stream keys - o3 R1 (s2 R2 objects)
  - (c) Encrypted-header Double Ratchet sessions with hybrid PQXDH setup - s2, s3; s1 and s4 conditional on a reviewed wrapper; MPE-CRY-028..035
- **Prototype default:** (a): invitation-based symmetric profile (MPE-CRY-001), revocation rekey from fresh entropy (MPE-CRY-019), capability record stating no forward secrecy (MPE-CRY-026, MPE-PRV-026).
- **Production default:** (a) for the broadcast bus; (c) as an optional pairwise profile, each claim gated by MPE-CRY-040 and MPE-VER-037. Option (b) is rejected.
- **Reason:** Static or stream-key encryption has no recipient-compromise forward secrecy (2022-barnes-rfc9180 section 9.1). Hash progression does not revoke a removed holder (MPE-CRY-019) and retained keys over a 48 h retention window defeat its secrecy claim (s2 R2). Ratchet secrecy holds only with erasure (2016-signal-double-ratchet-spec sections 8.1-8.4).
- **Settled by:** DEC-CRY-1 check: run both profiles on identical workloads including broadcast fan-out, offline recovery, crash restore and retained-key compromise, and count KEY_GAP outcomes against the 48 h window.
- **Requirements affected:** MPE-CON-031 (rationale)

### DEC-003 Recognition mechanism

- **Options and proponents:**
  - (a) Trial decryption of every Envelope, no Tag - g1, g3, g4, o3 R2; DEC-CRY-2, DEC-PUB-2(a), DEC-CON-2(b)
  - (b) Per-publisher sequence PRF Tags with an expected-Tag lookahead window - o1, o3 R1, o4 (direct channels); DEC-CON-2(a) recommended
  - (c) Hourly broadcast Tags - o4 R1
  - (d) Salted per-Envelope PRF Tag - s4; DEC-CRY-2 and DEC-PUB-2 recommended
  - (e) Encrypted-header trial under a capped key set - s2, s3
  - (f) Visible recognition Tag or FMD clue in the Visible Header - o1, o2, o4; DEC-FMT-2(b)
- **Prototype default:** (d): 16 B salt and 16 B Tag in the clear prefix of the Sealed Body (new MPE-FMT-051), HMAC-SHA-256 under the recognition key, local test of every Envelope of the Shard, then authentication (MPE-CRY-013, MPE-CRY-014).
- **Production default:** (d), kept only if it measurably beats (a) on recognition cost; otherwise (a).
- **Reason:** (b) loses a publisher after more than W skipped numbers (o3 R2 withdrew it; MPE-CON-008 exists only to report that loss). (c) groups an hour of traffic. (f) gives relays a per-Envelope string and is rejected by DEC-FMT-2. (d) is unlinkable without the key and costs one HMAC per key per Envelope: 256 x 10 = 2,560 evaluations per second.
- **Settled by:** DEC-PUB-2 benchmark of (a) against (d) at 256 keys and 10 and 100 Envelopes/s on desktop and phone hardware; the MPE-PRV-004 key-privacy review of the exact construction.
- **Requirements affected:** MPE-CON-007 (withdrawn), MPE-CON-008 (withdrawn), MPE-CRY-004

### DEC-004 Envelope lifetime and ordinary retention (48 h versus 7 days)

- **Options and proponents:**
  - (a) 300-3,600 s by class - g1
  - (b) 10-minute relay cache, 24 h optional store, 7 days if anchored - g2
  - (c) 48 h - g3, s1, s3, s4; DEC-STO-1, DEC-FMT-5 recommended
  - (d) 7-day complete replication (7 d default, 14 d maximum for o1) - s2, o1
  - (e) TTL classes 1 h, 24 h, 7 d - o2
  - (f) 24 h default, 7 d maximum - o4
  - (g) 14-day Indexer retention - g4
- **Prototype default:** (c): L_max = ordinary retention = 172,800 s on per-Shard Store Nodes; archives off.
- **Production default:** (c), with an optional paid archive up to 7 days (MPE-STO-021) and the 14-day hard ceiling (MPE-FMT-033).
- **Reason:** Four proposals converge on 48 h, which covers a wallet offline overnight (o4 R2's objection to 1 h). At the byte cap one replica holds 65,536 x 172,800 = 11.3 GB per Shard; 7 days would hold 39.6 GB per Shard, tripled by the three Operators per Shard (P-STO-5). Offline periods longer than 48 h are reported as retention gaps (MPE-PUB-045), not hidden.
- **Settled by:** Pilot measurement of Subscriber offline intervals and the share of resumes that hit a retention gap, compared against a threshold recorded in the course-change register (MPE-OPS-053); Store Node cost bids at 48 h and 7 d.
- **Requirements affected:** MPE-STO-003, MPE-STO-004

### DEC-005 Operating rate (10 versus 50 per second)

- **Options and proponents:**
  - (a) 10 Envelopes/s and 64 KiB/s per Shard, whichever binds first - g3; g2 worked load; s1, s2, s3, s4; DEC-PRF-1 and DEC-VER-2 recommended
  - (b) 50 objects/s per Shard - g1
  - (c) 50 Events/s network-wide sustained, 250-500/s peak - o1, o4
  - (d) 100 Events/s network-wide at 10/s per Shard - o2
  - (e) Ledger-lane rates of 1/s average, 10/s peak, or about 0.67/s - o3, g4
- **Prototype default:** (a), with (b) run as the P-PRF-28 comparison for 24 h and 100/s bursts for 60 s.
- **Production default:** (a) per Shard; aggregate capacity grows only through the Shard count (DEC-011). The count ceiling rises to 50/s only on the settling evidence below.
- **Reason:** '10/s' and '50/s' are not comparable without sizes: g1's normalized 50/s mix is 41.39 KiB/s, inside the 64 KiB/s byte cap. The binding unknowns are per-Envelope verification and recognition CPU, which (a) caps.
- **Settled by:** MPE-PRF-025 run with the selected admission verifier: adopt 50/s if edge CPU stays within P-PRF-14, propagation p99 within P-PRF-11 and timely delivery at or above 99.9%.
- **Requirements affected:** MPE-PRF-006

### DEC-006 Relay admission: permissioned or permissionless

- **Options and proponents:**
  - (a) Registry allow-list, removed only after a failed capture red team - g1, o4 (amended), o1 R2, s3 (roster); DEC-OPS-1(a), DEC-NET-7(a), DEC-SEC-1
  - (b) Contracted dedicated Operators plus open relaying - s1, s2, s4; DEC-OPS-1(b)
  - (c) Open relaying controlled by peer scoring - g2, g3, o1 R1, o2; DEC-OPS-1(c), DEC-NET-7(b)
- **Prototype default:** Both modes implemented; (a) is the default against the mock Registry relay list (MPE-OPS-007); (c) runs only in red-team experiments.
- **Production default:** (a) at launch with at least 8 organizations and at most 20% each (MPE-OPS-009, MPE-OPS-010); removal only after the MPE-OPS-008 red team at 1:1 Sybil identities fails to push canary delivery below 99.9% and the MPE-OPS-048 audit gate passes.
- **Reason:** Scoring is not a Sybil defence (2020-leastauthority-gossipsub-audit); configurations exist where a withholding peer keeps a positive score (2022-kumar-gossipsub-formal). Paid publication does not constrain relay identities (DEC-SEC-1).
- **Settled by:** MPE-OPS-008 red team at 1, 3 and 5% targeted placement and at 1:1 identities under production scoring parameters.
- **Requirements affected:** MPE-VER-040

### DEC-007 Admission instrument (DUST ticket, RLN membership, NIGHT bond, blind stamps)

- **Options and proponents:**
  - (a) DUST-paid Registry membership with a per-Envelope anonymous nullifier proof (RLN-style) - o1, g3, s3, o2, o4; DEC-ECO-1(a) recommended
  - (b) DUST-bought single-use on-chain tickets - g1; o4 R2 vote; DEC-ECO-1(b)
  - (c) Visible member key with signature and credit counter - g2; DEC-ECO-1(c)
  - (d) Issuer-signed permits or publicly verifiable blind-RSA stamps - s1, s2, s4; g2 R2 vote; DEC-ECO-1(d) fallback
  - (e) DUST fee per Event on the ledger - g4, o3 Lane A; DEC-ECO-1(e)
  - (f) NIGHT-bonded membership with slashing - o2, o4, o3 Lane B; DEC-ECO-2(c)
- **Prototype default:** (a) against the mock Ledger Adapter: simulated registration fee, revocation on equivocation, no bond; 512 B Admission Slot; pluggable verifier.
- **Production default:** (a) with DUST registration paid from shielded DUST (MPE-ECO-007) and revocation (MPE-ECO-028); (f) disabled at launch; (d) with a 354 B object-bound stamp if (a) fails MPE-ECO-048.
- **Reason:** (b) is unlinkable only at one ticket per transaction, about 2 tickets/s at a 10% block share (o1 R2). (c) links every Envelope of a member (MPE-FMT-005). (d) gives the issuer a customer-to-Event map (o4 R2; leakage row L-U). (e) caps the whole chain at about 21 calls/s (MPE-ECO-003). (f): deployed Waku dropped its deposit (2024-revuelta-waku-latency) and contract-held NIGHT on mainnet is unknown.
- **Settled by:** MPE-ECO-048 (proof fields at most 4,096 B, verification at most 10 ms on a 4-vCPU core); a demonstrated off-chain verifier for the selected proof (o1 spike); MPE-ECO-049 registration at most 16 KiB and 0.5 DUST.

### DEC-008 Ledger-only operation, ledger fallback and bodies on the ledger

- **Options and proponents:**
  - (a) Overlay from the first phase; ledger for membership and Anchors - g1, g2, g3, o1, o2, o4, s1, s2, s3, s4; DEC-NET-1(a), DEC-OPS-7(b)
  - (b) Ledger and Indexer lane first, overlay later - o3; o4 R2; DEC-OPS-7(a)
  - (c) Ledger and Indexer only - g4; DEC-NET-1(c)
  - (d) Fallback by whole-feed gateways in overlay framing - s1, s2, s4, o1 R2; DEC-NET-2(a)
  - (e) Fallback by Misc events read through contractEvents - g2, o2, o4, s3; DEC-NET-2(b)
  - (f) Fallback by a default-off Substrate notification protocol - g1, g3; DEC-NET-2(c)
  - (g) Anchors-only fallback - g2; rejected in DEC-VER-2
- **Prototype default:** (a); gateway fallback as the Bus Node stream service (new MPE-NET-048); the ledger carrier (MPE-FMT-040..046) runs only against the mock adapter; no ledger-only mode.
- **Production default:** (a); fallback order (d) then (e) as a labelled last resort on ledger 9, never automatic (MPE-PRV-013); (f) and (g) rejected. Sealed Bodies may appear in Misc logs only through (e); Registry contract state never holds a body (MPE-STO-001 rewritten).
- **Reason:** Public networks run ledger 8 (midnight-docs/docs/concepts/how-midnight-works/building-blocks.mdx:79-83), so (b) and (c) have no public network. The ledger lane shares 1,000,000 blockUsage bytes per 6 s slot (ledger-parameters-config.json:158; runtime/src/lib.rs:292) and carries 256 B Misc payloads (minokawa-compact/compiler/midnight-events.ss:71-74). MPE-STO-001 ('no ledger writes, including the Misc fallback') contradicted MPE-FMT-040..046 and MPE-CON-053; the BRIEF keeps bodies out of ledger state while naming a Misc fallback path.
- **Settled by:** The ledger-9 mainnet date against the Phase 1 start; a written product need for latency under one slot or bodies over 205 B (g4 T1); Prototype delivery at least 99% with p99 at most 6 s at 200 nodes (g2).
- **Requirements affected:** MPE-STO-001, MPE-NET-044 (see canonical MPE-FMT-040/041)

### DEC-009 Bus Node behaviour under a stale chain view

- **Options and proponents:**
  - (a) Ignore every Envelope whose admission depends on chain state while the view is stale - MPE-NET-018, MPE-FMT-031; g1 D1, o1 R2 D9
  - (b) Keep forwarding Envelopes valid under cached eligible Registry state; never Reject on chain-dependent checks - MPE-SEC-035, MPE-OPS-021, MPE-NET-038, MPE-ECO-025; g1 D7, g3 D9, o4 R2 D8, s4 D9
- **Prototype default:** (b): Accept Envelopes that validate against a cached root that is current or superseded less than P-ECO-5 ago and whose membership period ended less than P-ECO-5 ago (new MPE-ECO-051); Ignore Envelopes that need state the node lacks; never Reject on a chain- or clock-dependent check while stale.
- **Production default:** Same as the Prototype.
- **Reason:** (a) turns any Ledger Adapter outage into a bus outage: MPE-NET-018's test (freeze the mock adapter, expect Ignore) and MPE-OPS-021's test (freeze the mock adapter, expect delivery) cannot both pass. (b) keeps o1 R2's rule that a lagging chain source must not graylist honest forwarders, and the stale-root bound limits forwarding under old state to 25 h.
- **Settled by:** One frozen-adapter test asserting both continued delivery of cached-valid Envelopes and zero P4 changes; a stale-root test at P-ECO-4 + P-ECO-5.
- **Requirements affected:** MPE-NET-018, MPE-FMT-031

### DEC-010 GossipSub message id versus Envelope Identifier

- **Options and proponents:**
  - (a) Message id = Envelope Identifier, which excludes the Admission Slot - MPE-FMT-019, MPE-NET-010; s1, s3, s4, o2 R2; DEC-FMT-3(b)
  - (b) Message id = hash of every wire byte; Envelope Identifier kept for admission binding, deduplication and Anchors - MPE-PUB-026; g1, o4, o1 R1; DEC-FMT-3(a); g1 R2 objection; MPE-CRY-005 'final wire identifier'
- **Prototype default:** (b): message id = SHA-256 over a domain string and the complete wire bytes; Envelope Identifier (MPE-FMT-018) binds admission, keys application deduplication, inventories and Anchor leaves; the application seen-set records an Envelope Identifier only after Accept (new MPE-SEC-041).
- **Production default:** Same as the Prototype.
- **Reason:** rust-libp2p inserts the message id into its duplicate cache before application validation (rust-libp2p/protocols/gossipsub/src/behaviour.rs:1983), sends IDONTWANT for it before validation (behaviour.rs:1950), and on Reject removes the message only from the message cache (behaviour.rs:991). Under (a) a peer that forwards an honest Sealed Body with a corrupted Admission Slot makes each receiver that sees the corrupted copy first drop the honest copy as a duplicate, and IDONTWANT extends the suppression one hop, for the price of one P4 penalty per receiver. Under (b) the corrupted copy has its own id. Alternative valid admissions of one body still resolve to one delivery through the seen-set (MPE-SEC-014).
- **Settled by:** New MPE-SEC-042: inject corrupted-slot copies ahead of the honest copy; the honest Envelope reaches every eligible Subscriber within P-VER-6.
- **Requirements affected:** MPE-NET-010, MPE-FMT-019, MPE-PUB-026

### DEC-011 Shard count

- **Options and proponents:**
  - (a) One feed with the shard field reserved - g1, s1, s2, s3, s4; DEC-PUB-1(a), DEC-NET-4(a)
  - (b) Up to 8 Shards - g2, g3, o4; DEC-NET-4(b)
  - (c) 16 Shards or buckets - o1, o2
- **Prototype default:** 1 operating Shard; the benchmark topology runs 8 (P-PRF-3).
- **Production default:** 1 at launch; raised by the Registry (at most 8) after one Shard exceeds the PRF cap for 7 days and the per-Shard anonymity floor holds.
- **Reason:** Round 2 has nine votes for one feed (DEC-PUB-1). Each split divides the anonymity set and exposes per-Shard volume (o2 R2). Sharding does not reach mobile budgets: at 10 x 2 KiB per second one feed is 1.77 GB/day and one of eight Shards 221 MB/day, against 56-60 MB/day (g4, o3).
- **Settled by:** MPE-PRF-021 measured Subscriber bytes at 1 and 8 Shards; PRV's anonymity floor (MPE-OPS-052 counts).
- **Requirements affected:** MPE-PUB-002

### DEC-012 Mesh profile

- **Options and proponents:**
  - (a) (D, D_lo, D_hi, D_out) = (6, 5, 12, 2) - g1, g3, o1 R1, s2; rust-libp2p default (config.rs:83-86); DEC-PRF-2 recommended
  - (b) (8, 6, 12, 4) - g2, o1 R2; DEC-NET-3 recommended; DEC-SEC-2
- **Prototype default:** (b), heartbeat 1 s, gossip factor 0.25, prune backoff 60 s, flood publishing off; (a) as the mandatory MPE-PRF-010 comparison.
- **Production default:** (b), unless the comparison shows (a) meets P-PRF-23 and P-PRF-24 at 200 nodes under a 20% cold-start Sybil attack; then (a).
- **Reason:** The Prototype gates include the 20% cold-start attack (MPE-PRF-032, MPE-VER-018) and an outbound quota of 4 (MPE-SEC-003); (b) is the profile evaluated under that attack (2020-vyzovitis-gossipsub). D_out = 4 forces an eclipse to own four dialled slots (2015-heilman-eclipse). The cost is planning egress of 5.24 against 3.93 Mbit/s at the byte cap, absorbed by the revised edge budget.
- **Settled by:** MPE-PRF-010 comparison at 50, 200 and 1,000 nodes with identical sizes, churn and 20% Sybil cold start.
- **Requirements affected:** MPE-PRF-010, MPE-PRF-013, MPE-PRF-014

### DEC-013 Size classes and Admission Slot width

- **Options and proponents:**
  - (a) Single 4,096 B cell - s1, s3, g2 R2, g3 R2
  - (b) Single 2,048 B record - s4
  - (c) 1,024 or 4,096 B cells - s2
  - (d) Bodies 256 B, 1 KiB, 4 KiB, 16 KiB - g1, o1 R2, o4 R2; DEC-FMT-1 recommended
  - (e) Bodies 1, 4, 16, 64 KiB - o1 R1, o2 R1
  - (f) 512 B to 32 KiB - o4 R1
  - (g) Wires 1, 4, 32 KiB - g3 R1, o2 R2
  - (h) 4 and 64 KiB plus announced 256 KiB - g2 R1
  - (i) One 288 B Misc - g4, o3 R2
- **Prototype default:** (d) with A = 512 B: wires 776, 1,544, 4,616 and 16,904 B.
- **Production default:** (d) if the measured A is at most 1,024 B; otherwise (d) without the 256 B class.
- **Reason:** One table serves both carriers (1, 4, 16, 64 Misc parts) and the 256 B class keeps full-feed cost low (o3 R2, g3 R2). If a Midnight-native proof runs to kilobytes (o2 R2 cites 2,912 B and 4,832 B transaction proofs), class 0 becomes mostly admission overhead, which is DEC-FMT-1's own reversal trigger.
- **Settled by:** MPE-ECO-048 measured proof length; per-class anonymity-set simulation at the PRF load (DEC-FMT-1); payload-size histograms from pilot applications.
- **Requirements affected:** MPE-FMT-048, MPE-PRF-019

### DEC-014 Outcome for conflicting use of one allowance (equivocation)

- **Options and proponents:**
  - (a) Reject the second Envelope and record evidence - MPE-ECO-020; o2, o1, o4
  - (b) Ignore the second Envelope, record evidence and emit AdmissionConflict - MPE-SEC-018, MPE-SEC-019; s3, s4; DEC-SEC-4 recommended
  - (c) Deduplicate without a partition rule - g1, g2
- **Prototype default:** (b); revocation through MPE-ECO-028.
- **Production default:** (b); bond slashing only where DEC-007 (f) is enabled.
- **Reason:** The peer forwarding the second Envelope may be honest: in another partition it accepted that Envelope first. Reject would graylist honest peers when partitions heal. The equivocator is punished by revocation, not by mesh score.
- **Settled by:** Partition simulation in MPE-SEC-018: spend one allowance on two bodies in two partitions, heal, and confirm no P4 change and an evidence record.
- **Requirements affected:** MPE-ECO-020

### DEC-015 Unknown or foreign Envelope version

- **Options and proponents:**
  - (a) Bind version to the topic; mismatch is Reject - g1, o1 R2, s2, s3, g3, o2; DEC-FMT-4 recommended; MPE-FMT-023
  - (b) Ignore unknown versions - g2; MPE-NET-017, MPE-SEC-008
  - (c) Relay unknown versions - o1 R1
  - (d) Accept N and N-1 in one mesh - o4; MPE-OPS-035
- **Prototype default:** (a); one version.
- **Production default:** (a) with both versions' topics relayed for P-FMT-9 = 34 days (MPE-FMT-024); a governance deny-list entry yields Ignore (MPE-OPS-036).
- **Reason:** Topic names carry the major version (MPE-NET-006), so a v1 topic never legitimately carries v2 bytes; Ignore would let a neighbour inject junk without penalty. Running both topics gives o4's overlap without mixing versions in one mesh.
- **Settled by:** MPE-FMT-024 upgrade simulation with no loss of unexpired old-version Envelopes.
- **Requirements affected:** MPE-NET-017, MPE-SEC-008, MPE-OPS-035

### DEC-016 Quota accounting inside one Admission Proof

- **Options and proponents:**
  - (a) Envelope count - o1, o4, s3; DEC-ECO-4(a)
  - (b) Byte weights: P-ECO-3(c) credit indices per Envelope - g3, g2, o2 R2; DEC-ECO-4(b) recommended; MPE-ECO-017
  - (c) Per-class limits committed in the membership leaf, one nullifier per Envelope - Reconciliation of MPE-ECO-017 with MPE-FMT-003 and MPE-FMT-007
- **Prototype default:** (c): limits (64, 16, 4, 1) per epoch for classes 0-3; size class bound into the nullifier domain.
- **Production default:** (c); (b) only with a reviewed multi-nullifier circuit that fits P-ECO-11.
- **Reason:** (b) needs up to 64 distinct credit indices for a class-3 Envelope: 64 nullifier and share pairs (at least 4 KiB of public outputs) or 64 proofs, which a single fixed Admission Slot cannot carry; and P-ECO-2 = 10 is below the class-3 weight, so the lowest tier could never send class 3. (c) bounds bytes per member per epoch at 4 x 16 KiB, which exceeds DEC-ECO-4's 2x target by a factor of 2; that excess is accepted for the Prototype.
- **Settled by:** DEC-ECO-4 class-mix simulation at the lowest tier; circuit size and verification time of a multi-nullifier variant against P-ECO-11 and P-ECO-12.
- **Requirements affected:** MPE-ECO-016, MPE-ECO-017

### DEC-017 Durability of admission replay state

- **Options and proponents:**
  - (a) Durably commit consumed allowances before forwarding - MPE-SEC-015; s3, s2 R2
  - (b) In-memory caches with an accepted restart replay window - g3 R1
  - (c) Recover protection, or wait until affected authorizations expire, before live admission - g3 alternative, s3 R1; MPE-STO-015, MPE-SEC-016; DEC-STO-7
- **Prototype default:** (c) by waiting: in-memory nullifier and seen-set state; after every process start the Bus Node returns Ignore for live admission for P-ECO-7 = 140 s.
- **Production default:** Same; (a) remains an optional configuration (MPE-SEC-015 rewritten as optional).
- **Reason:** Every allowance is permanently ineligible at most 140 s after acceptance (MPE-ECO-021), so waiting restores the invariant without a disk write on the forwarding path and without rollback detection, which SEC lists as unknown. A restarted node already waits 600 s before injecting local publications (MPE-NET-030).
- **Settled by:** DEC-STO-7 check: crash and stale-backup restore at epoch boundaries; no consumed allowance accepted twice.
- **Requirements affected:** MPE-SEC-015, MPE-STO-015

### DEC-018 Tombstones

- **Options and proponents:**
  - (a) Authenticated tombstones with a 48 h deadline - o4; DEC-OPS-5(a)
  - (b) No takedown path - g4; silent in g1, g2
  - (c) Cooperative deletion only - s4 R2; DEC-OPS-5(c), DEC-SEC-5, DEC-STO-6
- **Prototype default:** Disabled; MPE-OPS-025 and MPE-OPS-026 move to PROD scope.
- **Production default:** Optional, binding only Operators under the Operator Agreement; deletion within 24 h; every tombstone published; replay records untouched.
- **Reason:** With 48 h retention a 48 h deadline never deletes a body before ordinary expiry. A forged or captured deletion authority is a censorship mechanism, so the feature waits for OPS issuance rules.
- **Settled by:** Counsel memos for Phase 1 jurisdictions (MPE-OPS-050); DEC-SEC-5 forgery and replay tests.
- **Requirements affected:** MPE-OPS-026, MPE-SEC-034, MPE-STO-036

### DEC-019 Governance authority over the Registry

- **Options and proponents:**
  - (a) Bus steward set with time-locks and 7-day emergency expiry - o4; s4 R2 reduced form; DEC-OPS-2(a)
  - (b) Midnight Root through Council and TC - g1; DEC-OPS-2(b)
  - (c) Foundation multisig with 7-day timelock - o2; DEC-OPS-2(c)
  - (d) Immutable contracts - o3 end state, g4; DEC-OPS-2(d)
- **Prototype default:** Mock Registry with a single maintainer key; time-lock and expiry logic exercised in the Quint model only.
- **Production default:** (a), handed to Council and TC or removed before the open-admission phase ends (MPE-OPS-020).
- **Reason:** Federated motions take 5 days (midnight-node/runtime/src/lib.rs:789), too slow to eject a relay injecting malformed objects (o4 R2). (d) has no ejection or emergency path. MPE-ECO-035 limits any maintainer to parameter changes.
- **Settled by:** Quint invariants I1-I6 (o4); MPE-OPS-017 result on whether a maintenance authority can be time-locked on ledger 9.

### DEC-020 First contact and fuzzy detection

- **Options and proponents:**
  - (a) Authenticated invitations only - s1, s2, s3, s4, g4; DEC-CRY-3, DEC-PUB-3, DEC-CON-8 recommended
  - (b) Inbox to a published key - g1, g2, o1, o3 R1
  - (c) Inbox with an FMD clue - o1; o2 S-FMD; DEC-CRY-5
  - (d) Dedicated intro inbox with a stricter rate tier - o4
- **Prototype default:** (a); FMD disabled (MPE-CRY-037).
- **Production default:** (a); (d) only as a separately reviewed profile.
- **Reason:** An open inbox is a harassment vector (o4 R2); FMD detection keys expose candidate subsets to the detector (2021-seres-fmdfalsepositives sections 1, 4-6; listed in catalog/PB3-receiver-privacy.jsonl, absent from papers.tsv).
- **Settled by:** A written product requirement for unsolicited contact plus a red-team pass on the intro-tier rate limit.

### DEC-021 Light and mobile reception

- **Options and proponents:**
  - (a) Whole Shard only - g1, g2, g4, s1, s2, s3, s4, o3 R2; DEC-PUB-5, DEC-CON-1, DEC-PRV-1
  - (b) Unicast filter node - g3
  - (c) Tag index or queries with decoys - o1, o4
  - (d) S-FMD - o2
  - (e) Bucket prefixes - o3 R1
- **Prototype default:** (a) only.
- **Production default:** (a) by default; (b)-(e) only as labelled opt-in profiles (MPE-PUB-016) with their own claim register (MPE-PRV-037).
- **Reason:** No selective mode keeps selection privacy at a demonstrated cost (s4 R2); sender-chosen S-FMD rates do not enforce a floor (2022-penumbra-fmd-spec).
- **Settled by:** MPE-PRF-021 Subscriber bytes per day against the 56-60 MB/day mobile budgets, then a measured OMR or PIR profile.

### DEC-022 Contract consumption path and signature algorithm

- **Options and proponents:**
  - (a) In-circuit publisher signature with a secret-derived nullifier, no Anchor - s3, s2, s1, o3 R2, o1 R2, o2 R2; DEC-CON-3(a)
  - (b) Anchor inclusion through a historic-root check - o1 R1, o3 R1, o2, o4, g3; DEC-CON-3(b)
  - (c) note(commitment) - g1
  - (d) No contract consumption - g4
  - (e) Ed25519 statements - s2, g1; DEC-CRY-6
  - (f) JubJub Schnorr - o1, o3, o4
- **Prototype default:** (a) with (e), exercised against a mock contract with a nullifier set (MPE-VER-032).
- **Production default:** (a) with (e) unless (f) proves cheaper in the measured circuit; (b) optional (MPE-CON-047).
- **Reason:** (a) needs no cross-contract call and puts authority in the circuit (s3 #1, o4 D3). The Compact standard library exposes plain Ed25519 verification (minokawa-compact/doc/api/CompactStandardLibrary/exports.md:993); its circuit cost against JubJub is unknown.
- **Settled by:** Compile both authorization fixtures on a ledger-9 devnet; compare circuit size and proving time; zero unauthorized and duplicate effects in the MPE-VER-009 model.

### DEC-023 Publish ingress and stem

- **Options and proponents:**
  - (a) One-hop outbound stem - g2, g3; DEC-NET-6
  - (b) Two-hop stem - g1
  - (c) Dandelion++ - o1, o2
  - (d) Mix ingress later - s3
  - (e) No anonymity claim from any stem - s1, s4; MPE-PRV-029; DEC-VER-5
- **Prototype default:** (a) with (e): one Bus Node chosen at random from two dialled (MPE-NET-033).
- **Production default:** (a) kept only if the first-spy run shows lower precision than direct publication; no anonymity claim.
- **Reason:** The Dandelion++ bound assumes a random 4-regular anonymity graph unknown to the adversary (2018-fanti-dandelionpp sections 3.1, 4.1) and does not transfer to GossipSub meshes.
- **Settled by:** MPE-VER-027 first-spy precision and recall for (a), (b) and direct publication at coalitions 1-20%.

### DEC-024 Anchor granularity and history

- **Options and proponents:**
  - (a) One Anchor per Shard per window - MPE-NET-041; o1, o2
  - (b) One Anchor per window covering all Shards - o4 (window_id, shard_bitmap, root, count)
  - (c) 7-day history, 10,080 records - o4; DEC-STO-4 recommended
  - (d) 14-day, 20,160-slot ring - o2
  - (e) History bounded by L_max - Derived from MPE-CON-046
- **Prototype default:** (b) with (e): 60 s windows; payload of window number, root over per-Shard batch roots and per-Shard counts (new MPE-NET-050); 49 h, 2,940 records.
- **Production default:** Same as the Prototype.
- **Reason:** (a) multiplies records by the Shard count and breaks the STO record bound at 8 Shards (8 x 10,080). Contracts reject expired Events (MPE-CON-046), so no live root older than L_max serves a consumer; clients verify older Anchors from Misc history, not live state.
- **Settled by:** Ledger-9 measurement of reachable Anchor-state bytes (MPE-STO-030) and per-Anchor cost (MPE-VER-030).
- **Requirements affected:** MPE-NET-041, MPE-STO-028, MPE-STO-029

### DEC-025 Second-source reconciliation: MUST or SHOULD

- **Options and proponents:**
  - (a) Reconciliation against an independent second source is mandatory in the Prototype - s1, o3 R2, o4 R2; MPE-SEC-021 and MPE-CON-037 (MUST); DEC-PUB-4, DEC-CON-5
  - (b) Single source with sequence-gap detection; second source optional - g1, g4, o1, o2; MPE-PUB-014 and MPE-PUB-015 (SHOULD), MPE-CON-036 (PROD SHOULD)
- **Prototype default:** (a): MPE-PUB-014 and MPE-PUB-015 become POC MUST.
- **Production default:** (a).
- **Reason:** Sequence gaps cannot reveal suppression of a whole publisher or of first contact (o3 R2 D9); the inventory costs 1.6% of feed bytes (DEC-PUB-4).
- **Settled by:** Omission-injection simulation (MPE-PUB-014 verify) with measured overhead below 2% of feed bytes.
- **Requirements affected:** MPE-PUB-014, MPE-PUB-015

### DEC-026 Delivery labels and attributes

- **Options and proponents:**
  - (a) Exactly one label, gossip or final - MPE-CON-015; o3
  - (b) A stored label from retention receipts - MPE-STO-012; s1, s2, s3
  - (c) A fallback-mode label - MPE-NET-042; s1 R2, s3
- **Prototype default:** Three orthogonal attributes: finality (gossip or final, MPE-CON-015), carrier (overlay, gateway or ledger, new MPE-CON-057) and storage (stored when MPE-STO-012 holds).
- **Production default:** Same as the Prototype.
- **Reason:** MPE-CON-015 requires exactly one of two labels, which a third 'stored' label or a fallback label would violate; the three properties vary independently.
- **Settled by:** API inspection plus a test delivering one Event over each carrier, before and after anchoring, with and without three receipts.
- **Requirements affected:** MPE-STO-012, MPE-NET-042

### DEC-027 Direction of node bandwidth budgets

- **Options and proponents:**
  - (a) Aggregate receive plus transmit - DEC-PRF-4 drafting assumption
  - (b) Per direction - g3 R1 D5 planning model (egress); g2 egress budget
- **Prototype default:** (b): 6 Mbit/s per direction per Shard for an Edge Bus Node, 24 Mbit/s per direction for a Full Bus Node.
- **Production default:** (b).
- **Reason:** g3's 4 Mbit/s is its egress model (1.25 x 6 x 64 KiB/s); reading it as aggregate halves the budget. With D = 8 the same model gives 5.24 Mbit/s egress.
- **Settled by:** Two-direction packet capture at the byte cap under both mesh profiles (MPE-PRF-005).
- **Requirements affected:** MPE-PRF-013, MPE-PRF-014

### DEC-028 Phase numbering and the Prototype boundary

- **Options and proponents:**
  - (a) VER: Phase 0 evidence and models, 1 local Prototype and simulations, 2 integration and pilot, 3 production - DEC-VER-1; s4, g1, g2
  - (b) OPS: Phase 0 models, simulation and Prototype, 1 permissioned pilot, 2 permissioned production, 3 open admission, 4 handover - DEC-OPS-7; o4, o2
  - (c) Ledger-first phases - o3, g4
- **Prototype default:** (b) numbering: everything in the Prototype is Phase 0.
- **Production default:** (b): VER Phases 0 and 1 map to OPS Phase 0, VER Phase 2 to OPS Phase 1, VER Phase 3 to OPS Phase 2.
- **Reason:** MPE-OPS-017, -041, -043 and -046 already reference OPS numbering, and OPS adds the open-admission and handover phases VER lacks.
- **Settled by:** Gate record of each transition (MPE-OPS-042).
- **Requirements affected:** MPE-VER-003, MPE-VER-011

## 4. Fixes

### 4.1 Lint failures

| Requirement | Problem | Corrected records |
|---|---|---|
| MPE-CON-005 | Two "shall" (not atomic). | MPE-CON-005a, MPE-CON-005b |
| MPE-CON-025 | Two "shall" (not atomic). | MPE-CON-025a, MPE-CON-025b |
| MPE-CON-044 | Two "shall" (not atomic). | MPE-CON-044a, MPE-CON-044b |
| MPE-CRY-008 | Weasel word "secure". | MPE-CRY-008 |
| MPE-FMT-001 | Two "shall" (not atomic). | MPE-FMT-001a, MPE-FMT-001b |
| MPE-NET-001 | Two "shall" (not atomic). | MPE-NET-001a, MPE-NET-001b |
| MPE-NET-009 | Two "shall" (not atomic). | MPE-NET-009a, MPE-NET-009b |
| MPE-NET-043 | Two "shall" (not atomic). | MPE-NET-043a, MPE-NET-043b |
| MPE-OPS-033 | Weasel word "secure"; two obligations. | MPE-OPS-033a, MPE-OPS-033b |
| MPE-OPS-043 | Pattern event but sentence starts with "Before". | MPE-OPS-043 |
| MPE-OPS-046 | Pattern event but sentence starts with "Before". | MPE-OPS-046 |
| MPE-OPS-047 | Pattern event but sentence starts with "Before". | MPE-OPS-047 |
| MPE-PUB-006 | Weasel word "secure". | MPE-PUB-006 |

### MPE-FMT-001a Fixed-width visible layout
The MPE client library shall encode every Envelope field outside the Sealed Body as a fixed-width field at a fixed per-version offset.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, s2, s3, s4, o1-R2, o4-R2; `2012-bitmessage-protocol-specification` (varint object header)
- Rationale: Each Envelope has exactly one legal byte string, so parsing is unambiguous.
- Verify: test, decode and re-encode every MPE-FMT-049 vector and compare the bytes for equality.
- Status: settled

### MPE-FMT-001b No variable encodings outside the Sealed Body
The MPE client library shall emit no optional field, extension field, length prefix, variable-length integer or self-describing encoding outside the Sealed Body.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1, s3, s4; `2020-vac-waku2-message-spec` (protobuf is not canonical)
- Rationale: A new field requires a new version and topic (register DEC-015).
- Verify: inspection, review the wire specification; test, every fuzzed Envelope that carries such a construct fails MPE-FMT-006 or MPE-FMT-007.
- Status: settled

### MPE-CRY-008 Random stream secrets
When a private stream is created, the MPE client library shall obtain its P-CRY-1-byte stream secret from the operating-system cryptographic random-number interface.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g4 R1 D3; s2 R1 D3; o3 R1 D3; `2021-len-partitioningoracle`, section 1
- Rationale: Human-chosen passphrases face a guessing threat that random capabilities do not.
- Verify: inspection, stream creation requests exactly P-CRY-1 bytes from the configured interface (getrandom on Linux); test, an injected interface failure produces the MPE-CRY-009 result.
- Status: settled

### MPE-PUB-006 Random private audience keys
The MPE client library shall obtain every private audience key as 32 bytes from the operating-system cryptographic random-number interface.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g4 D3; `2021-len-partitioningoracle` (ChaCha20-Poly1305 is not key-committing); see canonical MPE-CRY-008
- Rationale: Low-entropy keys allow guessing topics and multi-key openings.
- Verify: inspection, the API offers no passphrase input for private topics and key generation calls the operating-system interface.
- Status: settled

### MPE-OPS-033a Aggregated counter release
Where Bus Node counters are published, the Bus Node shall release them only as aggregates computed across at least P-OPS-16 share keepers, none of which receives an individual Bus Node's counter value.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; `2016-jansen-safely-measuring-tor`
- Rationale: Load can be measured without exposing any single relay's activity.
- Verify: inspection, review the counter-export path; test, capture share-keeper inputs and confirm each is a blinded share.
- Status: open (DEC-OPS-4)

### MPE-OPS-033b Differential-privacy budget for counters
Where Bus Node counters are published, the Bus Node shall add noise that gives each published counter a differential-privacy epsilon of at most P-OPS-18.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; `2018-mani-tor-usage-privacy-preserving` txt L505
- Rationale: Aggregation alone does not bound what a published count reveals about one user.
- Verify: analysis, compute epsilon from the configured noise distribution and sensitivity; test, the noise sampler matches that distribution (KS test, p > 0.01).
- Status: open (DEC-OPS-4)

### MPE-OPS-043 Evidence freeze
When the Phase 0 exit review starts, MPE shall record the target network's ledger version, runtime `spec_version` and the pinned revision of every Midnight component the bus depends on.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D10; s4 D10; o4 R2; o3 R2; `midnight-node/Cargo.lock:7894`
- Rationale: The tag, the lockfile and the documentation disagree, for example on the 1 KiB log limit.
- Verify: inspection, compare the claim register against a live RPC `spec_version` query.
- Status: settled

### MPE-OPS-046 Measured Registry costs
When the Phase 1 exit review starts, MPE shall report the measured serialized bytes and DUST fee of one Registry admission transaction and one Anchor transaction on a ledger-9 network.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D10; g3 D10; o1, o2, o3, s4 R2; see canonical MPE-VER-030
- Rationale: Every DUST and anchoring budget in the proposals scales from an unmeasured transaction size.
- Verify: test, on a devnet with the recorded `ledgerParameters`.
- Status: settled

### MPE-OPS-047 Scoring-CVE release gate
When a Bus Node release is prepared for a network other than a test network, MPE shall attach a recorded run showing the CVE-2022-47547 score-manipulation attack failing against that release's pinned GossipSub implementation and scoring configuration.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10, D9; g2 D10; s2 R2; `2023-kumar-gossipsub-acl2s`; see canonical MPE-VER-026
- Rationale: A changelog does not establish closure of a configuration-dependent scoring attack.
- Verify: test, run the attack scenario against the release candidate and check that the attacker's score falls below the graylist threshold.
- Status: open (DEC-SEC-6)

### MPE-CON-005a Typed degraded outcome
If the active reception mode cannot be sustained, then the MPE client library shall return the typed `Degraded` outcome to the subscription.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s3 D9 block 4; see canonical MPE-PRV-013
- Rationale: A silent switch to a leakier mode breaks the privacy claim unnoticed.
- Verify: test, make every source unreachable and assert one `Degraded` outcome.
- Status: settled

### MPE-CON-005b Reception mode unchanged after degradation
If the active reception mode cannot be sustained, then the MPE client library shall keep the reception mode unchanged until the application selects another profile.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s3 D9 block 4; see canonical MPE-PRV-013
- Rationale: Only the application may accept a different leakage contract.
- Verify: test, after `Degraded`, capture requests and confirm no selector or filtered request precedes an explicit profile selection.
- Status: settled

### MPE-CON-025a Typed source failure
If a source connection fails, then the MPE client library shall return the typed `SourceFailed` outcome to the subscription.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4; `midnight-js/packages/types/src/public-data-provider.ts:509-510`
- Rationale: Applications must distinguish loss of a source from a quiet feed.
- Verify: test, kill the source mid-stream and assert one `SourceFailed` outcome.
- Status: settled

### MPE-CON-025b No completion on source failure
If a source connection fails, then the MPE client library shall keep the subscription open instead of ending it as complete.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4
- Rationale: A silent completion reads as 'no more Events', which is loss.
- Verify: test, kill the source mid-stream and assert the subscription never emits completion.
- Status: settled

### MPE-CON-044a Replayed consumption rejected
If a reaction's consumption nullifier is already in the target contract's nullifier set, then the MPE client library's consumption circuit shall reject the reaction.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D3; o3 D3.5 step 4; s3 D3; s2 D3; o1 D3
- Rationale: Replayed reactions produce no second effect.
- Verify: test, submit the same reaction twice and assert the second transaction fails.
- Status: settled

### MPE-CON-044b Atomic nullifier insertion
The MPE client library's consumption circuit shall insert the consumption nullifier in the same transaction as the contract effect it authorizes.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; s3 D9; `minokawa-compact/doc/compact-reference.mdx:3777`
- Rationale: Effect and replay state must not diverge across failures.
- Verify: test, inject failure in the fallible segment and confirm neither the effect nor the nullifier is committed.
- Status: settled

### MPE-NET-001a Sidecar process
The Bus Node shall run as an operating-system process separate from `midnight-node`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1, g2, g3, o1, o2, o4, s1, s2, s3, s4; notes section 8
- Rationale: The node has no GossipSub and no plugin slot.
- Verify: inspection, the Prototype is its own binary and runs beside an unmodified node.
- Status: settled

### MPE-NET-001b No MPE code in the node binary
MPE shall add no code to the `midnight-node` binary.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; `midnight-node/Cargo.lock` (no `libp2p-gossipsub`; `sc-network-gossip` at :14548)
- Rationale: A protocol inside the node would be a fork every relaying operator has to run.
- Verify: inspection, the `midnight-node` dependency tree is unchanged by the MPE build.
- Status: settled

### MPE-NET-009a StrictNoSign publication
The Bus Node shall publish every Envelope under the GossipSub StrictNoSign policy, with the `from`, `seqno`, `signature` and `key` fields absent.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D1; g2 D1; `specs/pubsub/README.md:272-321`; `rust-libp2p/protocols/gossipsub/src/config.rs:46` (`ValidationMode::Anonymous`)
- Rationale: Removes the peer-id author stamp from the gossip layer.
- Verify: test, captured RPC frames lack all four fields.
- Status: settled

### MPE-NET-009b Signed-field rejection
If a received GossipSub message carries a `from`, `seqno`, `signature` or `key` field, then the Bus Node shall drop it and apply the invalid-message penalty to the sender.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8; `rust-libp2p/protocols/gossipsub/src/protocol.rs:421-442`; `CHANGELOG.md:1-4`
- Rationale: Author fields would attach a peer identity to an Envelope.
- Verify: test, an injected message carrying any one of the four fields is not delivered and the sender's P4 score falls.
- Status: settled

### MPE-NET-043a Complete-stream gateway
Where the gateway fallback is enabled, the Bus Node shall serve the complete Envelope stream of a requested Shard in overlay framing.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D8; s1 D8; s2 D8; s4 D8; o1 R2 D8
- Rationale: Keeps the whole-feed interest property while concentrating ingress on fewer Operators.
- Verify: test, the byte streams from the overlay and from the gateway match for one Shard over 1 h.
- Status: open (DEC-NET-2)

### MPE-NET-043b No filter on the gateway
Where the gateway fallback is enabled, if a stream request carries a topic, Tag or identifier filter, then the Bus Node shall refuse the request with `Refused`.
- Pattern: complex
- Scope: PROD
- Priority: SHOULD
- Source: D8; s1 D8; MPE-PUB-030
- Rationale: A filter would reveal Subscriber interest to the gateway.
- Verify: test, each filter parameter is refused and no Envelope is sent.
- Status: open (DEC-NET-2)

### 4.2 Untestable or vague requirements

| Requirement | Problem |
|---|---|
| MPE-PRF-006 | "Sustain a throughput" has no pass criterion. |
| MPE-PRF-007 | Deadline left to each run. |
| MPE-PRF-023 | No deadline or fraction. |
| MPE-PUB-035 | "Correctly operating" is untestable. |
| MPE-NET-022 | Prunes honest peers in idle Shards. |
| MPE-OPS-024 | Threshold undefined. |
| MPE-OPS-039 | "Mitigation" not observable. |
| MPE-OPS-020 | Ubiquitous sentence opening with a time trigger. |
| MPE-SEC-022 | "Independently verified provenance" undefined. |

### MPE-PRF-006 Sustained Shard capacity
While Reference conditions hold, MPE shall deliver at least P-VER-7 of eligible Envelope-Subscriber pairs within P-VER-6 for an offered load of min(P-PRF-1, P-PRF-2 divided by mean complete Envelope size) Envelopes per second per Shard sustained for P-VER-3.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; g3 R1/R2 D5; s4 R1 D10; register DEC-005
- Rationale: "Sustain" had no pass condition; delivery fraction and deadline make it one.
- Verify: test, run count-bound (class 0) and byte-bound (class 3) workloads and compute the delivery fraction per MPE-VER-014.
- Status: open (DEC-PRF-1)

### MPE-PRF-007 Normal-load delivery
While Reference conditions hold at the sustained Shard capacity, MPE shall deliver every accepted Envelope to every continuously connected eligible Subscriber within P-VER-6 after admission.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 D5, D10; g1 R1 D10
- Rationale: Replaces a free 'declared observation deadline' with the frozen acceptance deadline.
- Verify: test, compare accepted identifiers with each Subscriber's received identifiers and timestamps.
- Status: open (DEC-PRF-3)

### MPE-PRF-023 Gateway Subscriber capacity
While Reference conditions hold on one Shard at its sustained capacity, MPE shall deliver at least P-VER-7 of that Shard's accepted Envelopes within P-VER-6 to each of the P-PRF-18 concurrently connected Subscribers.
- Pattern: state
- Scope: POC
- Priority: SHOULD
- Source: D5; s3/s4 R1 D5; o4 R1 D5
- Rationale: A socket count is not a capacity claim without a delivery bound.
- Verify: demonstration, run the gateway topology and compute per-Subscriber delivery fractions.
- Status: open (DEC-PRF-5)

### MPE-PUB-035 At-least-once delivery
While an unexpired Envelope is retained by at least one configured source that answers the Subscriber's requests, MPE shall deliver that Envelope to the Subscriber's client library at least once.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; all proposals; s4 D3; see MPE-CON-012
- Rationale: "Correctly operating" is not observable; a source that holds and answers is.
- Verify: simulation, 16 Bus Nodes, 20% churn, 1,000 Envelopes, one answering source per interval; every Envelope reaches every Subscriber.
- Status: settled

### MPE-NET-022 Eviction of misbehaving peers
When a mesh peer has delivered only Rejected Envelopes, or no Envelope within the GossipSub mesh-delivery window, for P-NET-16 consecutive heartbeats in each of which the Shard carried an accepted Envelope, the Bus Node shall prune that peer from its mesh.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D9; `2022-kumar-gossipsub-formal` sections 3-5; `2023-kumar-gossipsub-acl2s`
- Rationale: In an idle Shard no peer delivers anything; the original wording pruned every peer.
- Verify: simulation, withholding and invalid-only peers at 10 Envelopes/s are pruned within P-NET-16 heartbeats; no peer is pruned in an idle Shard.
- Status: settled

### MPE-OPS-024 Evidence-only ejection when open
While the relay allow-list is inactive, MPE shall eject a relay only on published evidence that P-OPS-16 independent monitors measured its canary delivery below P-OPS-5 for P-OPS-12, or on a malformed Anchor it signed.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7 (72 h evidence, 7-day appeal); `2026-cao-nymreputation` section 1
- Rationale: "Probe failure above threshold" named no threshold; the canary gate supplies one.
- Verify: inspection, every ejection event references the monitor records and the threshold computation.
- Status: open (DEC-OPS-2)

### MPE-OPS-039 Sev1 mitigation time
When an incident is classified Sev1, MPE shall publish a signed release or configuration change that removes the classified trigger within P-OPS-21.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7
- Rationale: "Deploy a mitigation" had no observable end point.
- Verify: demonstration, timed drills at least twice per year; the drill's trigger no longer reproduces on the published artifact.
- Status: settled

### MPE-OPS-020 Governance end state
When the open-admission phase exit review starts, MPE shall show that the Registry maintenance authority has been transferred to Midnight federated governance or removed.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; g1 D7; o3 D7; `midnight-node/runtime/src/lib.rs:789`
- Rationale: A bus-specific authority is a launch measure.
- Verify: inspection, read the Registry's maintenance authority from ledger state.
- Status: open (DEC-OPS-2)

### MPE-SEC-022 Authenticate Registry read results
If an Indexer result is not confirmed by Registry state read from P-NET-14 independent chain sources at a finalized block, then the Indexer adapter shall exclude it from admission and Anchor authorization.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D9; g1 R1 D9; s1 R1 D9; s4 R2 D9; MPE-NET-020; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`
- Rationale: "Independently verified provenance" named no procedure; source agreement does.
- Verify: test, substitute contract addresses, invent Anchors and alter Registry data at one source; no authorization derives from them.
- Status: settled

### 4.3 Consistency rewrites

These records implement the parameter table and the decision register. Each replaces the requirement with the same ID.

| Requirement | Conflict resolved |
|---|---|
| MPE-NET-010 | Conflicts with MPE-PUB-026; enables a duplicate-cache censorship attack. |
| MPE-NET-017 | Unknown version as Ignore contradicts MPE-FMT-023. |
| MPE-NET-018 | Contradicts MPE-OPS-021 and MPE-SEC-035 on the same frozen-adapter test. |
| MPE-FMT-031 | Ignore-everything stops the bus during adapter staleness. |
| MPE-ECO-015 | Window measured from publication time. |
| MPE-ECO-016 | Weights of up to 64 credits per Envelope cannot fit one fixed slot. |
| MPE-ECO-017 | Replaces the multi-credit debit. |
| MPE-ECO-020 | Reject contradicts MPE-SEC-018. |
| MPE-NET-023 | Per-peer total starves Full Bus Nodes. |
| MPE-STO-001 | Forbade the Misc fallback that FMT and CON specify. |
| MPE-STO-003 | Creation time is not visible to a Store Node. |
| MPE-STO-012 | A third label violated MPE-CON-015. |
| MPE-NET-041 | Per-Shard Anchors exceed the STO record bound. |
| MPE-PRF-013 | Aggregate reading halved g3's budget. |
| MPE-PRF-014 | Aggregate reading. |
| MPE-SEC-015 | Mandatory durability conflicted with the restart barrier. |
| MPE-STO-015 | Recovery condition left undefined. |
| MPE-CRY-004 | Listed fields that the Visible Header does not carry. |
| MPE-VER-040 | Threshold conflicted with MPE-OPS-008. |
| MPE-PUB-014 | SHOULD conflicted with MUST in SEC-021 and CON-037. |
| MPE-PUB-015 | Priority raised with MPE-PUB-014. |
| MPE-FMT-024 | SHOULD here, MUST in MPE-OPS-035. |
| MPE-OPS-026 | POC scope conflicted with tombstones disabled in the Prototype. |
| MPE-PUB-027 | Retention differed from MPE-STO-013. |
| MPE-PUB-002 | Range 1-16 conflicted with P-NET-9 (1-8). |
| MPE-CON-015 | Collided with the stored and fallback labels. |

### MPE-NET-010 Wire-byte message id
The Bus Node shall set the GossipSub message id to SHA-256 over a fixed MPE domain string and the complete received Envelope bytes.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D1; register DEC-010; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:1950,1983,991`; `config.rs:526-539`
- Rationale: A corrupted Admission Slot must not share the honest copy's id in the duplicate cache.
- Verify: test, two Envelopes differing only in the Admission Slot get distinct ids; identical bytes get one id.
- Status: open (DEC-FMT-3)

### MPE-NET-017 Ignore outcome
If an Envelope is a duplicate of an accepted Envelope Identifier or expired on arrival, then the Bus Node shall return Ignore.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8; g1 D1; `gossipsub-v1.1.md:536`; register DEC-015
- Rationale: A version mismatch on a version-bound topic is Reject (MPE-FMT-023).
- Verify: test, each case is neither forwarded nor penalised.
- Status: settled

### MPE-NET-018 Stale chain view never penalises
While the Ledger Adapter view is stale, the Bus Node shall return Ignore instead of Reject for every Envelope whose failed check depends on chain state or the local clock.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D8, D9; o1 R2 D9; g1 D1, D7; register DEC-009
- Rationale: Cached-valid Envelopes keep flowing (MPE-NET-038); only penalties are suspended.
- Verify: test, freeze the mock adapter; cached-valid Envelopes still reach Subscribers and no peer's P4 term changes.
- Status: settled

### MPE-FMT-031 Unsafe clock
While the Ledger Adapter view is stale under MPE-NET-019, the Bus Node shall return Ignore instead of Reject for an Envelope that fails the expiry check of MPE-FMT-029.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D1; g1 D1; register DEC-009
- Rationale: A skewed clock must not penalise honest peers or stop the bus.
- Verify: test, shift the mock adapter timestamp by P-NET-13 + 1 s; far-future expiry yields Ignore and valid Envelopes are still accepted.
- Status: settled

### MPE-ECO-015 Root window from supersession
If an Envelope's Admission Proof references a membership root that is neither the current root nor superseded less than P-ECO-5 earlier, then the Bus Node shall return Ignore for that Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2, o1; g1 R2; MPE-ECO-027
- Rationale: Counting from publication made every Envelope Ignore after an hour without registrations.
- Verify: test, with no root update for 2 h the current root still validates; a root superseded P-ECO-5 + 1 s earlier yields Ignore.
- Status: settled

### MPE-ECO-016 Committed per-class rate limit
The Bus Node shall return Reject for an Envelope of size class c unless its Admission Proof shows a credit index below the class-c per-epoch limit committed in the membership leaf.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; `2024-vac-rln-v2-spec` (RLN-Diff); o1, o2, o4; register DEC-016
- Rationale: One nullifier per Envelope fits one fixed Admission Slot.
- Verify: test, with class-2 limit 4, credit indices 0-3 are accepted and index 4 is Rejected.
- Status: open (DEC-ECO-4)

### MPE-ECO-017 Class-bound nullifier
The MPE client library shall derive each Admission Proof nullifier from the admission secret, epoch number, size class and credit index under one domain-separated hash.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; register DEC-016; `2022-vac-rln-v1-spec`
- Rationale: Separate index spaces per class prevent one credit index from serving two classes.
- Verify: test vectors; two Envelopes of different classes with equal index yield different nullifiers.
- Status: open (DEC-ECO-4)

### MPE-ECO-020 Equivocation recorded without penalty
If an Envelope carries a nullifier already accepted with a different Envelope Identifier, then the Bus Node shall return Ignore and record both Envelopes as equivocation evidence.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4; o2, o1, o4; s3, s4; `2022-taheri-waku-rln-relay` section III; register DEC-014
- Rationale: The forwarder of the second Envelope may be honest; the equivocator loses its membership through MPE-ECO-028.
- Verify: test, send two conflicting Envelopes from two peers; no P4 change and the evidence store holds both.
- Status: open (DEC-SEC-4)

### MPE-NET-023 Per-peer per-Shard rate limit
If a peer sends more than P-NET-10 Envelopes per second on one Shard, then the Bus Node shall drop the excess with Ignore before proof verification.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D4; s3 D9; register parameter table
- Rationale: A per-peer total would drop honest traffic on multi-Shard Full Bus Nodes.
- Verify: test, at 5 x P-NET-10 from one peer on one Shard, verifier calls for that peer and Shard stay at or below P-NET-10 per second.
- Status: settled

### MPE-STO-001 No bodies in ledger state
The Registry shall store no Event body and no Sealed Body in contract state.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; BRIEF system definition; g3, s2, s3 R1 D6; register DEC-008
- Rationale: Sealed Bodies reach the ledger only as Misc logs on the labelled ledger fallback (MPE-FMT-040..046).
- Verify: inspection, review the Registry's state declarations and captured state writes.
- Status: settled

### MPE-STO-003 Reject excessive ordinary retention
If a received Envelope's expiry exceeds the Store Node's clock plus P-FMT-3 plus P-FMT-4, then the Store Node shall reject its storage admission.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 D6; s3 R1 D6; MPE-FMT-029
- Rationale: The visible expiry is the retention deadline; creation time is sealed.
- Verify: test, admission just below, at and above the limit.
- Status: open (DEC-STO-1)

### MPE-STO-012 Stored attribute
The MPE client library shall mark a delivered Event `stored` only after validating compatible retention receipts from at least P-STO-5 distinct Operators.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; s1, s2, s3 R1 D6; register DEC-026
- Rationale: Storage is an attribute beside the gossip or final label.
- Verify: test, reject duplicate-Operator receipts and receipts naming different Envelopes or deadlines.
- Status: open (DEC-STO-5)

### MPE-NET-041 Anchor cadence
Where a Bus Node acts as anchorer, the Bus Node shall submit at most one Anchor per non-empty P-NET-17 window, covering every Shard.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D8, D6; o4 D4; g3 D4; register DEC-024
- Rationale: One record per window keeps the Anchor history inside P-STO-10.
- Verify: test, ten windows with three empty ones produce seven Anchors, each listing all Shards' counts.
- Status: settled

### MPE-PRF-013 Edge bandwidth budget
While Reference conditions hold at the sustained Shard capacity, the Bus Node operating as an Edge Bus Node shall consume no more than P-PRF-12 of bus bandwidth in each direction.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 D5; register DEC-027
- Rationale: g3's model is an egress budget; D = 8 needs 5.24 Mbit/s.
- Verify: test, capture receive and transmit separately over the steady interval.
- Status: open (DEC-PRF-4)

### MPE-PRF-014 Full bandwidth budget
While Reference conditions hold with P-PRF-16 Shards at their sustained capacity, the Bus Node operating as a Full Bus Node shall consume no more than P-PRF-13 of bus bandwidth in each direction.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 D5; register DEC-027
- Rationale: Same direction rule as the edge budget.
- Verify: test, capture receive and transmit separately with all allocated Shards active.
- Status: open (DEC-PRF-4)

### MPE-SEC-015 Optional durable admission replay state
Where durable replay state is configured, the Bus Node shall commit each consumed publication allowance to durable storage before forwarding its Envelope.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D9; s3 R1 D9; s2 R2 D9; register DEC-017
- Rationale: The default restart barrier (MPE-STO-015) already prevents reuse; durability shortens restart unavailability.
- Verify: test, interrupt at the persistence and forwarding boundaries, restart, and replay the admitted Envelope.
- Status: settled

### MPE-STO-015 Restart barrier
While less than P-ECO-7 has elapsed since the Bus Node process started, the Bus Node shall return Ignore for every Envelope requiring live admission.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D6, D9; g3 R1 D9; s3 R1 D6; s2 R2 D9; register DEC-017
- Rationale: Every allowance accepted before the restart is then permanently ineligible.
- Verify: test, restart mid-epoch and replay a pre-restart Envelope at 1 s and at P-ECO-7 + 1 s; neither is accepted live.
- Status: open (DEC-STO-7)

### MPE-CRY-004 Public-context authentication
The MPE client library shall authenticate the Network Identifier, Visible Header bytes 0 to 7, and the Sealed Body's salt, nonce and Tag as AEAD associated data.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 R1 D1; s2 R1 D1; s1, s4 R2 D1; MPE-FMT-051, MPE-FMT-053
- Rationale: The cryptographic profile is fixed by `version`; the Admission Slot is excluded to keep construction acyclic.
- Verify: test, changing each bound byte prevents opening under the original context.
- Status: settled

### MPE-VER-040 Open admission gate
If the open-admission red team reduces canary delivery below P-OPS-5, then MPE shall fail open-admission acceptance.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D10; g1 R1; o1 R2; s3 R1; see canonical MPE-OPS-008
- Rationale: The same gate carried 99% and 99.9%; the stricter value applies.
- Verify: simulation, attackers hold as many peer identities as the honest set; targeted capture and cold joining.
- Status: open (DEC-VER-6)

### MPE-PUB-014 Second-source reconciliation
While following a Shard, the MPE client library shall reconcile its received Envelope Identifiers against a second source run by a different Operator every P-PUB-3.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; s1 D3; o3 R2 D7, D9; o4 R2; register DEC-025
- Rationale: Sequence gaps cannot reveal omission of whole publishers or first contacts.
- Verify: simulation, one source drops 5% of Envelopes; the client obtains every dropped Envelope the second source holds within 2 x P-PUB-3.
- Status: open (DEC-PUB-4)

### MPE-PUB-015 Repair every difference
When reconciliation finds an Envelope Identifier that the client has not received, the MPE client library shall fetch that Envelope.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s1 D3; register DEC-025
- Rationale: Repairing only matched Envelopes would reveal which ones matched.
- Verify: test, every missing identifier is fetched, whatever the key set.
- Status: open (DEC-PUB-4)

### MPE-FMT-024 Version overlap
Where two Envelope versions are active, the Bus Node shall relay the topics of both versions for at least P-FMT-9 after the newer version activates.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D1; o4 D1; g1; register DEC-015
- Rationale: Unexpired Envelopes published before an upgrade stay deliverable.
- Verify: simulation, upgrade half the nodes; no unexpired old-version Envelope is lost during the window.
- Status: open (DEC-FMT-4)

### MPE-OPS-026 Tombstoned Envelope not relayed
Where tombstones are enabled, when the Bus Node holds a valid tombstone for an Envelope Identifier, the Bus Node shall Ignore that Envelope.
- Pattern: complex
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; register DEC-018
- Rationale: Tombstones are disabled in the Prototype.
- Verify: test, a replayed tombstoned Envelope is not forwarded and the sender's P4 term is unchanged.
- Status: open (DEC-OPS-5)

### MPE-PUB-027 Seen-set until expiry
The Bus Node shall keep each accepted Envelope Identifier in its application seen-set until that Envelope's expiry plus P-FMT-4.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1 D1; `rust-libp2p/protocols/gossipsub/src/config.rs:524` (60 s duplicate cache)
- Rationale: After that time MPE-FMT-030 Ignores the Envelope anyway.
- Verify: test, replays at 61 s and at expiry - 1 s are not forwarded.
- Status: settled

### MPE-PUB-002 Shard derivation
The MPE client library shall set an Envelope's Shard to a domain-separated SHA-256 hash of the audience key reduced modulo P-PUB-1 as read from the Registry.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g3, o4; g1 R2; register DEC-011
- Rationale: A secret input stops testing which Shard a guessed label lands on.
- Verify: test, vectors for 1,000 keys at P-PUB-1 of 1 and 8 match a reference implementation.
- Status: open (DEC-PUB-1)

### MPE-CON-015 Finality label on every Event
The MPE client library shall label every delivered Event with exactly one finality label, `gossip` or `final`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D8; register DEC-026
- Rationale: Carrier and storage are separate attributes (MPE-CON-057, MPE-STO-012).
- Verify: test, every delivered item has exactly one finality label.
- Status: settled

### 4.4 Withdrawn

- MPE-CON-007 (expected-Tag lookahead window) and MPE-CON-008 (recognition-window gap): withdrawn by DEC-003. Salted per-Envelope Tags have no sequence window to lose.
- The forward-secrecy rationale of MPE-CON-031 is void under DEC-002. The requirement itself becomes see canonical MPE-PUB-046 (PROD).

## 5. Gaps

### 5.1 Cross-area dependencies that no file provides

| Missing provision | New record |
|---|---|
| A 512 B slot holding 360 B of fields needs a filler rule; FMT-006 covers only the reserved header byte. | MPE-FMT-050 |
| CRY expects salt, nonce and Tag in a pre-seal header that FMT does not define. | MPE-FMT-051 |
| No area checks the visible shard byte against the topic. | MPE-FMT-052 |
| CRY authenticates a profile identifier that FMT does not carry. | MPE-FMT-053 |
| FMT left the authentication block width to CRY; CRY did not set it. | MPE-CRY-041 |
| DEC-009 keeps forwarding under cached roots; nothing bounded how long. | MPE-ECO-051 |
| ECO expects FMT to define epoch, root, nullifier and share fields; FMT left the slot opaque. | MPE-ECO-052 |
| Epoch freshness (ECO-014) has no defined epoch number. | MPE-ECO-053 |
| Needed by the DEC-010 message-id split. | MPE-SEC-041 |
| No SEC test covers identifier-based suppression. | MPE-SEC-042 |
| Reconciliation requires an inventory service that no area provides. | MPE-STO-041 |
| STO-011 signs receipts but no request path exists. | MPE-STO-042 |
| Whole-Shard reception has no transport for non-mesh clients. | MPE-NET-048 |
| PUB-022 relies on an acceptance signal that NET does not define. | MPE-NET-049 |
| FMT delegated the Anchor payload to NET; NET did not define it. | MPE-NET-050 |
| CON verifies inclusion under a root no area defines. | MPE-NET-051 |
| The `final` label needs inclusion paths that no area serves. | MPE-NET-052 |
| No area authorizes anchorers. | MPE-NET-053 |
| NET-039 lists Registry fields without the relay list. | MPE-NET-054 |
| NET-035 names only 'Registry reads'; other areas need specific reads. | MPE-NET-055 |
| STO lists the historical Registry context as unspecified. | MPE-NET-056 |
| VER-015 checks memory against a ceiling PRF never set. | MPE-PRF-041 |
| Outcome names conflict across SEC, STO, PUB, CON, FMT and ECO. | MPE-CON-056 |
| NET-042's fallback label had no slot in CON's label set. | MPE-CON-057 |
| PUB-023 retransmits until expiry (48 h) although admission lapses after one epoch. | MPE-PUB-053 |
| New public field introduced by MPE-NET-050. | MPE-PRV-038 |
| POC requirements depend on Operator diversity that no fixture provides. | MPE-OPS-055 |
| No requirement ties the stages into one run. | MPE-VER-041 |

### 5.2 Decision coverage

Counts are requirements whose Source cites the decision. A requirement citing two decisions counts under both.

| Decision | Requirements | POC | PROD | Thin coverage |
|---|---|---|---|---|
| D1 Event format | 109 | 92 | 17 | Admission Slot contents, Sealed Body clear prefix, authentication block width, profile identification and shard-topic check were delegated between FMT, CRY and ECO and never written (FMT-050..053, CRY-041, ECO-052). |
| D2 Private | 52 | 38 | 14 | Leakage of per-Shard Anchor counts (PRV-038). |
| D3 Pub/sub | 164 | 132 | 32 | Heavily duplicated across PUB, CON, PRV and SEC; missing an acceptance signal, a stream transport and a closed outcome set (NET-048, NET-049, CON-056). |
| D4 Sustainable | 57 | 24 | 33 | Prototype admission is under-specified: no epoch numbering, slot layout or stale-root bound (ECO-051..053). |
| D5 Performance | 51 | 44 | 7 | No memory ceiling (PRF-041); bandwidth direction unresolved (DEC-027). |
| D6 Storage | 52 | 43 | 9 | No inventory or receipt request path, and no historical root lookup (STO-041, STO-042, NET-056). |
| D7 Actors | 67 | 25 | 42 | Anchorer authorization and Operator identity in the relay list absent; no POC Operator fixture (NET-053, NET-054, OPS-055). |
| D8 Tether | 55 | 41 | 14 | Anchor payload, batch root, inclusion paths and Ledger Adapter read set undefined (NET-050..052, NET-055). |
| D9 Threats | 86 | 71 | 15 | Duplicate-cache censorship through a corrupted Admission Slot (SEC-041, SEC-042). |
| D10 Build plan | 100 | 69 | 31 | No single end-to-end Prototype run; phase numbering conflict (VER-041, DEC-028). |

### 5.3 Needed for an end-to-end Prototype

MPE-FMT-050, MPE-FMT-051, MPE-FMT-052, MPE-FMT-053, MPE-CRY-041, MPE-ECO-051, MPE-ECO-052, MPE-ECO-053, MPE-SEC-041, MPE-SEC-042, MPE-STO-041, MPE-STO-042, MPE-NET-048, MPE-NET-049, MPE-NET-050, MPE-NET-051, MPE-NET-052, MPE-NET-054, MPE-NET-055, MPE-NET-056, MPE-PRF-041, MPE-CON-056, MPE-CON-057, MPE-PUB-053, MPE-OPS-055, MPE-VER-041.

### 5.4 New records

### MPE-FMT-050 Admission Slot zero fill
If any Admission Slot byte after the selected proof fields is non-zero, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1; MPE-FMT-006 (reserved-byte rule); register parameter A = 512 B
- Rationale: Unused slot bytes would otherwise be a covert channel and a second encoding of one Envelope.
- Verify: test, set each filler byte of a valid vector in turn; each result is Reject.
- Status: settled

### MPE-FMT-051 Sealed Body clear prefix
The MPE client library shall place the P-CRY-3-byte salt, the 12-byte AEAD nonce and the P-CRY-2-byte Tag, in that order, at the start of the Sealed Body before the ciphertext.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; MPE-CRY-004, MPE-CRY-013; MPE-FMT-037; DEC-FMT-2 (recognition material inside the body); register DEC-003
- Rationale: The ledger carrier has no Visible Header, so recognition and nonce inputs must travel inside the body.
- Verify: test vectors; a body copied from the mock ledger carrier opens exactly as its overlay copy.
- Status: open (DEC-CRY-2)

### MPE-FMT-052 Shard field matches topic
If a received Envelope's `shard` value differs from the Shard index of the topic it arrived on, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1, D3; MPE-NET-006, MPE-NET-031; MPE-PUB-002
- Rationale: A mismatched field would let Envelopes cross Shards and distort per-Shard accounting.
- Verify: test, an Envelope with `shard` = 1 published on the Shard-0 topic is Rejected and lowers the sender's P4 score.
- Status: settled

### MPE-FMT-053 One cryptographic profile per version
The MPE client library shall bind exactly one cryptographic profile to each Envelope `version` value.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; CRY parameter note ('changing them requires a new profile identifier'); MPE-FMT-001b; MPE-CRY-004
- Rationale: The Visible Header has no profile field; the version selects the profile.
- Verify: inspection, the version table maps each value to one profile; test, an Envelope opened under another profile fails authentication.
- Status: settled

### MPE-CRY-041 Publisher authentication block
The MPE client library shall encode the sealed publisher authentication block as a 2-byte authorized-key index, a 4-byte creation time and a 64-byte Ed25519 signature.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; DEC-FMT-7 (flags bit 0: 'CRY fixes its width'); MPE-CRY-018, MPE-CRY-020, MPE-CRY-021; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:106`
- Rationale: The key index points into the invitation's authorized publisher keys, so no key travels in each Envelope.
- Verify: test vectors; payload capacity per class equals body minus 170 B.
- Status: open (DEC-CRY-6)

### MPE-ECO-051 Stale-root bound
If the membership period served by an Admission Proof's referenced root ended more than P-ECO-5 before the Bus Node's clock, then the Bus Node shall return Ignore for that Envelope.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D4, D9; register DEC-009; MPE-ECO-026, MPE-ECO-027
- Rationale: Bounds forwarding under cached state to P-ECO-4 + P-ECO-5 when the chain view is stale.
- Verify: test, freeze the mock adapter and confirm Envelopes under the last root are Ignored 25 h after its period began.
- Status: settled

### MPE-ECO-052 Admission Slot field layout
The MPE client library shall fill the Admission Slot with the 8-byte epoch number, the 32-byte referenced membership root, the 32-byte nullifier, the 32-byte share y-coordinate and the proof, in that order.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D4; `2021-vac-waku2-rln-relay-spec` (RateLimitProof); MPE-ECO-018; ECO dependency row D1
- Rationale: Fixed offsets let a Bus Node run the cheap checks of MPE-ECO-013 before verification; share x is a hash of the Envelope Identifier.
- Verify: test vectors; a Bus Node rejects a stale epoch without invoking the verifier.
- Status: open (DEC-ECO-1)

### MPE-ECO-053 Epoch number
The MPE client library shall compute the admission epoch number as the Unix time in seconds divided by P-ECO-1, rounded down.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D4; o2 D3; MPE-ECO-014
- Rationale: Bus Nodes and clients must agree on epoch boundaries without coordination.
- Verify: test vectors at boundary times.
- Status: settled

### MPE-SEC-041 Seen-set entry after Accept
The Bus Node shall insert an Envelope Identifier into its application seen-set only after its validator returns Accept for an Envelope carrying that identifier.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9; register DEC-010; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:1983`; MPE-SEC-014
- Rationale: An invalid copy must not suppress the valid copy of the same Sealed Body.
- Verify: test, a Rejected corrupted-slot copy followed by the valid copy: the valid copy is accepted.
- Status: settled

### MPE-SEC-042 Corrupted-slot front-running test
The Prototype shall deliver an honest Envelope to every eligible Subscriber within P-VER-6 when an adversarial peer injects copies of its Sealed Body with corrupted Admission Slots ahead of it.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D9, D10; register DEC-010
- Rationale: Regression test for the duplicate-cache censorship path.
- Verify: test, on the 32-node topology with the adversary adjacent to the publisher's ingress Bus Node.
- Status: settled

### MPE-STO-041 Inventory listing
When a client requests an inventory for a Shard and time window, the Store Node shall return every retained Envelope Identifier in that window in pages of at most P-PUB-9 entries.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6, D3; MPE-PUB-014, MPE-SEC-021, MPE-CON-037 (expected from STO)
- Rationale: Reconciliation needs an identifier list from an independent source.
- Verify: test, a seeded store of N identifiers returns exactly N across pages.
- Status: settled

### MPE-STO-042 Retention receipt request
When a client requests a retention receipt for a retained Envelope Identifier, the Store Node shall return a receipt signed with its Operator key naming that identifier, the Shard and the retention deadline.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; MPE-STO-011, MPE-STO-012; s2, s3 R1 D6
- Rationale: The `stored` attribute needs a way to obtain receipts.
- Verify: test, request receipts from three Store Nodes and validate them under MPE-STO-012.
- Status: open (DEC-STO-5)

### MPE-NET-048 Shard stream service
The Bus Node shall provide a stream protocol that sends a connected non-mesh client every Envelope the Bus Node accepts on each Shard the client requests.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D3; CON dependency ('Bus Node interface for a non-mesh client'); MPE-PRF-022, MPE-PUB-033; MPE-OPS-007 (non-listed peers cannot GRAFT)
- Rationale: Under the allow-list, Subscribers are not mesh members and need a full-Shard feed.
- Verify: test, a client streaming one Shard receives every accepted identifier over 1 h.
- Status: settled

### MPE-NET-049 Publish acceptance message
When the Bus Node's validator returns Accept for an Envelope submitted by a client, the Bus Node shall send that client an acceptance message carrying the Envelope Identifier.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D8, D3; MPE-PUB-022, MPE-CON-026
- Rationale: The client reports `accepted` only on this message.
- Verify: test, a client receives the message for accepted Envelopes and none for Rejected or Ignored ones.
- Status: settled

### MPE-NET-050 Anchor payload
Where a Bus Node acts as anchorer, the Bus Node shall encode each Anchor payload as an 8-byte window number, a 32-byte root over the window's per-Shard batch roots and one 4-byte Envelope count per Shard.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D8, D6; MPE-FMT-047 ('NET defines the payload fields'); o4 D1; register DEC-024
- Rationale: At 8 Shards the payload is 72 B, inside the 256 B Misc payload.
- Verify: test vectors; a mock Registry decodes every field.
- Status: settled

### MPE-NET-051 Batch root construction
Where a Bus Node acts as anchorer, the Bus Node shall compute each per-Shard batch root as a SHA-256 Merkle root over the window's accepted Envelope Identifiers in ascending byte order.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D8; MPE-CON-016, MPE-CON-038
- Rationale: A canonical leaf order lets any holder of the leaf list reproduce the root.
- Verify: test vectors; an independent implementation reproduces the roots.
- Status: settled

### MPE-NET-052 Inclusion path service
Where a Bus Node acts as anchorer, the Bus Node shall return, on request, the Merkle inclusion path of an anchored Envelope Identifier for P-STO-9 after anchoring.
- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D8, D6; MPE-CON-016, MPE-CON-047
- Rationale: Only the anchorer knows each window's exact leaf set.
- Verify: test, paths verify against the Anchor root; a path for a non-anchored identifier is refused.
- Status: settled

### MPE-NET-053 Anchorer authorization
The Registry shall accept an Anchor only from a submitter key listed with the anchorer role in the Registry relay list.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7, D8; MPE-STO-028 (bounded records); OPS glossary 'Anchorer'
- Rationale: Unauthenticated Anchors could evict genuine records from the bounded history and forge counts.
- Verify: test, an Anchor from an unlisted key fails on a devnet and on the mock Registry.
- Status: open (DEC-OPS-2)

### MPE-NET-054 Relay list entries
The Registry shall expose a relay list whose entries each carry a peer identity, an Operator organization identifier and role flags for relay, Store Node, bootstrapper, gateway and anchorer.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D7, D8; MPE-OPS-007, MPE-OPS-011, MPE-PUB-014, MPE-PUB-034, MPE-STO-012; MPE-NET-039
- Rationale: Independence checks and fail-over need the Operator and role of each peer.
- Verify: inspection of the contract; test, the adapter reads every field.
- Status: settled

### MPE-NET-055 Ledger Adapter read set
The Ledger Adapter shall expose finalized reads of membership roots with publication and supersession times, the relay list, Registry parameters, Anchors, the bus pause flag and the current `ledgerParameters`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; MPE-NET-035; MPE-ECO-008, MPE-ECO-015, MPE-CON-016, MPE-CON-050, MPE-SEC-013
- Rationale: One interface lets the mock and the devnet adapters serve every area.
- Verify: test, the mock adapter answers each read and the full Prototype suite passes against it.
- Status: settled

### MPE-NET-056 Historic root lookup
When a Store Node validates a back-filled Envelope, the Ledger Adapter shall return the referenced membership root with its period if it was published within the last P-FMT-3 plus P-ECO-5.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6, D8; MPE-SEC-013, MPE-STO-016 (STO gap: historical context encoding)
- Rationale: Back-fill validation needs the root in force at publication, not the current one.
- Verify: test, back-fill after two root rotations validates against the historical root.
- Status: settled

### MPE-PRF-041 Bus Node memory ceiling
While Reference conditions hold at the sustained Shard capacity, the Bus Node shall keep its resident memory at or below P-PRF-34.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; MPE-VER-015; register parameter P-PRF-34 = 2 GiB (assumption derived from P-STO-4)
- Rationale: Resource acceptance cannot pass without a memory ceiling.
- Verify: test, sample resident memory every 10 s through the 72 h soak.
- Status: settled

### MPE-CON-056 Closed outcome set
The MPE client library shall report every refusal or failure as one of TooLarge, NotReady, NotAccepted, Busy, Refused, ResourceExhausted, StorageExhausted, KeyLimit, Degraded, SourceFailed, Unresolved, RetentionGap, KeyGap, CorruptRecord, LedgerUnavailable, LedgerPaused, BusPaused, InsufficientDust or SessionUpdateRequired.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; MPE-PUB-025; SEC glossary ('CON owns their API encoding'); STO glossary; o3 D3.4
- Rationale: Areas named the same outcomes differently (StorageExhausted and STORAGE_FULL, ResourceExhausted and RESOURCE_EXHAUSTED).
- Verify: inspection of the API; fault injection maps each injected fault to exactly one outcome.
- Status: settled

### MPE-CON-057 Carrier attribute
The MPE client library shall mark every delivered Event with exactly one carrier attribute: `overlay`, `gateway` or `ledger`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3, D8; MPE-NET-042; register DEC-026
- Rationale: Fallback leakage differs by carrier and must be visible beside the finality label.
- Verify: test, deliver one Event over each carrier and check its attribute.
- Status: settled

### MPE-PUB-053 Retransmission stops at epoch end
If an unaccepted Envelope's admission epoch ended more than P-ECO-6 earlier, then the MPE client library shall stop retransmitting it and report `NotAccepted`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3, D4; MPE-PUB-023; MPE-ECO-014
- Rationale: Bus Nodes Ignore such bytes, so further retries only waste bandwidth.
- Verify: test, with all Bus Nodes blackholed across an epoch boundary, retries stop P-ECO-6 after the epoch ends.
- Status: settled

### MPE-PRV-038 Anchor count leakage
The MPE shall include the per-Shard Envelope counts published in Anchors in the L-L leakage declaration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D2; MPE-PRV-020; MPE-NET-050
- Rationale: Per-window counts reveal per-Shard volume to any chain observer.
- Verify: inspection, L-L names the count fields and their window granularity.
- Status: settled

### MPE-OPS-055 Mock Operator roster
The Prototype shall register its local Bus Nodes and Store Nodes in the mock Registry relay list under at least P-STO-5 distinct Operator organization identifiers.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D7, D10; MPE-STO-012, MPE-SEC-021, MPE-PUB-014
- Rationale: Operator-diversity requirements cannot execute against a single-Operator fixture.
- Verify: inspection of the fixture; test, the `stored` attribute and reconciliation run on it.
- Status: settled

### MPE-VER-041 End-to-end Prototype scenario
The Prototype shall demonstrate, in one scripted run against the mock Ledger Adapter, membership registration, publication, overlay delivery, local recognition, a client crash with back-fill resume, Anchor-based `final` labelling and one mock contract reaction.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; DEC-VER-1; MPE-VER-011; MPE-CON-042
- Rationale: Component tests can pass while the end-to-end path is broken.
- Verify: demonstration, the run log shows each stage with Envelope and logical identifiers and the final contract state.
- Status: settled

### 5.5 Residual gaps without a testable requirement

- Permissionless Sybil resistance and global completeness of delivery have no reviewed mechanism (SEC and PUB gaps). The allow-list gate (MPE-OPS-008) and reconciliation (MPE-PUB-014) are mitigations, not proofs.
- Closure of CVE-2022-47547 in the pinned rust-libp2p is unknown: the local CHANGELOG has no entry naming it. Evidence comes only from MPE-VER-026.
- Ledger-9 activation on public networks is unknown (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:12`). Anchors, contract consumption and the ledger fallback stay behind MPE-OPS-044.
- Off-chain verification of a Midnight-native admission proof is unknown. DEC-007's fallback to stamps covers a failed MPE-ECO-048.
- `2021-beck-fmd` and `2021-seres-fmdfalsepositives` are cited by CRY, PUB and PRV. They appear in `catalog/PB1-bitmessage-heirs.jsonl` and `catalog/PB3-receiver-privacy.jsonl` and in `graph/text/`, but not in `design/evidence/papers.tsv`.

