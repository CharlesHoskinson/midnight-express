# MPE prototype core requirements

137 requirements the Rust prototype implements, in build order by milestone (M0 to M5 of `design/PROTOTYPE.md`). Requirement text is in `design/rounds/r5/e*.md`; where `design/ears/RECONCILE.md` corrected or split a requirement, the corrected record and its ID apply, and gap records come from RECONCILE.md section 5.4. A duplicate appears only under its canonical ID. Parameter values are the Prototype column of the RECONCILE.md parameter table.

"Proof" names the unit test (crate and test name) or the simulator scenario (`mpe-sim run --scenario <name>`) whose failure would show the requirement unmet. "Stand-in" names the mock component the proof depends on; "no" means the proof exercises production code paths only.

## M0 Envelope, sealing and recognition (`mpe-core`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-FMT-001a | Fixed-width visible layout | `wire::vectors_roundtrip`: decode and re-encode every vector, bytes equal | no |
| MPE-FMT-003 | Visible fields | `wire::header_is_520_bytes` over 10,000 Envelopes; `leakage` scenario, `plaintext_leaks` = 0 | no |
| MPE-FMT-004 | No identity-derived visible values | `wire::header_bytes_chi_square`: 1,000 Envelopes of one publisher and stream against 1,000 of distinct ones, every offset outside `shard` and `expiry`, p > 0.01 | admission stand-in (slot bytes) |
| MPE-FMT-013 | Sealed Body length | `seal::body_length_per_class` for classes 0-3 | no |
| MPE-FMT-014 | Smallest fitting class | `seal::class_edges`: payloads of 86, 87, 854, 855, 3,926, 3,927 and 16,214 B land in classes 0, 1, 1, 2, 2, 3, 3 | no |
| MPE-FMT-015 | Oversize payload | `seal::too_large`: 16,215 B returns `TooLarge`; publisher test shows no request sent | no |
| MPE-FMT-016 | Sealed padding | `seal::equal_wire_length`: 1 B and full-capacity payloads give equal wire length per class | no |
| MPE-FMT-017 | Padding check | `seal::nonzero_pad_discarded`: resealed vector with one pad byte 0x01 is discarded and counted | no |
| MPE-FMT-018 | Envelope Identifier | `wire::eid_vectors`; `wire::eid_ignores_slot`: one body under two slots gives one EID | no |
| MPE-FMT-022 | Logical Event Identifier | `seal::lei_stable_on_retransmit`; M4 `fallback::same_lei_both_carriers` | MockLedger (second half) |
| MPE-FMT-028 | Expiry field | `seal::expiry_is_creation_plus_lmax`: `now < expiry = creation + 172,800` | no |
| MPE-FMT-049 | Test vectors | `tests/independent_decoder.rs` parses every vector in `vectors/*.json` by fixed offsets without `mpe-core` code | no |
| MPE-FMT-051 | Sealed Body clear prefix | `seal::clear_prefix_offsets` (salt 520, nonce 536, Tag 548); `fallback::ledger_copy_opens` | MockLedger (second half) |
| MPE-FMT-053 | One cryptographic profile per version | `seal::foreign_profile_fails`: opening under another profile id fails authentication | no |
| MPE-CRY-001 | Default cryptographic profile | `keys::primitive_vectors` (RFC 5869, RFC 4231, RFC 8439, RFC 8032 vectors) and MPE derivation vectors | no |
| MPE-CRY-004 | Public-context authentication | `seal::aad_tamper`: flipping any AAD byte (network id, header bytes 0-3, salt, nonce, Tag) prevents opening; header bytes 4-7 are bound by the EID test of M1 and the signed-expiry check (finding F1 of PROTOTYPE.md) | no |
| MPE-CRY-008 | Random stream secrets | inspection: stream creation reads exactly 32 B from `OsRng`; `keys::rng_failure` injects an RNG error and gets a local failure with no key | no |
| MPE-CRY-010 | Nonce uniqueness | `seal::no_key_nonce_reuse`: 100,000 seals, no repeated (`k_enc`, nonce); `publisher::retransmit_is_identical_bytes` | no |
| MPE-CRY-013 | Salted private Tags | `tag::vectors`; `tag::recognition_survives_seq_gaps` (sequence numbers 1, 7, 1,000 all recognised) | no |
| MPE-CRY-014 | Recognition is provisional | `subscriber::tag_match_bad_ciphertext_not_delivered` | no |
| MPE-CRY-016 | Recognition-key bound | `subscriber::key_cap`: 256th key installs, 257th returns `KeyLimit`, existing subscriptions unchanged | no |
| MPE-CRY-021 | Signed statement binding | `seal::statement_field_substitution`: changing each statement field breaks signature verification | no |
| MPE-CRY-022 | Authenticated delivery | `subscriber::rejects_malformed_expired_unauthorized_badsig`; `malformed` scenario `rejected.bad_signature` equals injected count | no |
| MPE-CRY-041 | Publisher authentication block | `seal::auth_block_layout`; `seal::capacity_is_body_minus_170` | no |
| MPE-PUB-002 | Shard derivation | `keys::shard_vectors` for 1,000 keys at 1 and 8 Shards | no |
| MPE-PUB-019 | Per-publisher sequence number | `publisher::seq_monotonic`: 1,000 Events seal n to n+999 | no |

## M1 Admission stand-in and validator (`mpe-core`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-ECO-052 | Admission Slot field layout | `admission::slot_vectors` (epoch 8, root 16, nullifier 48, share 80, proof 112) | admission stand-in |
| MPE-ECO-053 | Epoch number | `admission::epoch_boundaries` at 59, 60 and 61 s | no |
| MPE-ECO-017 | Class-bound nullifier | `admission::nullifier_vectors`; equal index in two classes gives two nullifiers | admission stand-in |
| MPE-ECO-018 | Content-bound Admission Proof | `admission::secret_recovery`: two EIDs under one nullifier recover the admission secret | admission stand-in |
| MPE-ECO-016 | Committed per-class rate limit | `validator::class2_limit`: indices 0-3 Accept, 4 Reject; `spam` scenario | admission stand-in |
| MPE-FMT-005 | Admission Slot unlinkability | `admission::slot_unlinkable`: two memberships, 100 Envelopes each, no byte range constant within one and different between them | admission stand-in |
| MPE-FMT-050 | Admission Slot zero fill | `validator::filler_byte_reject` for each of bytes 360-511 of the slot | no |
| MPE-ECO-012 | Admission Proof required | `validator::mutated_proof_reject`; M2 `node::p4_rises_on_bad_proof` | admission stand-in |
| MPE-ECO-013 | Cheap checks before proof verification | `validator::stale_epoch_never_verified` (verifier call counter stays 0) | no |
| MPE-ECO-014 | Epoch freshness | `validator::epoch_tolerance`: −19 s Accept, −21 s Ignore, no P4 change | no |
| MPE-ECO-015 | Root window from supersession | `validator::root_window`: current root valid after 2 h without update; root superseded 3,601 s ago Ignored | mock Registry |
| MPE-ECO-051 | Stale-root bound | `validator::stale_root_bound`: frozen adapter, Envelopes under the last root Ignored 25 h after its period began | mock Registry |
| MPE-ECO-020 | Equivocation recorded without penalty | `validator::equivocation_ignore_and_evidence`; `spam` scenario phase B evidence count | admission stand-in |
| MPE-ECO-022 | Aggregate admission bound | `node::aggregate_bound`: 16 Bus Nodes, 50 memberships each offering 2 class-3 Envelopes per epoch for 3 epochs through different ingress nodes; Accepted ≤ 50 per epoch | admission stand-in |
| MPE-FMT-006 | Reserved bytes | `validator::reserved_bits`: each bit set in turn, Reject | no |
| MPE-FMT-007 | Exact length | `validator::length_off_by_one`: ±1 B, Reject | no |
| MPE-FMT-009 | Structural checks first | `validator::structural_before_crypto`: 10,000 malformed Envelopes with well-formed slots, verifier counter 0 | no |
| MPE-FMT-011 | Body-blind validation | inspection: `validator.rs` links no AEAD or decoder; `validator::random_body_same_outcome` | no |
| MPE-FMT-023 | Version bound to topic | `validator::version_mismatch_reject`; M2 `node::p4_rises_on_version` | no |
| MPE-FMT-029 | Expiry too far ahead | `validator::expiry_upper_bound`: now + 172,861 s Reject, now + 172,860 s Accept | no |
| MPE-FMT-030 | Expired on arrival | `validator::expired_ignore`; `replay` scenario `rejected.expired` | no |
| MPE-FMT-031 | Unsafe clock | `validator::stale_view_far_future_ignore`: mock time shifted 61 s, far-future expiry gives Ignore, valid Envelopes Accept | mock Registry |
| MPE-FMT-052 | Shard field matches topic | `validator::shard_mismatch_reject`; M2 `node::p4_rises_on_shard_mismatch` | no |
| MPE-NET-016 | Reject outcome | `validator::outcome_table`: every structural and admission mutation of the FMT list gets Reject | no |
| MPE-NET-018 | Stale chain view never penalises | `node::frozen_adapter`: adapter frozen 120 s, cached-valid Envelopes still delivered, no peer's P4 changes | MockLedger |
| MPE-PUB-027 | Seen-set until expiry | `validator::seen_set_retention`: replays at 61 s and at expiry − 1 s are not forwarded | no |
| MPE-PUB-028 | Duplicate is Ignore | `node::hundred_duplicates_no_score_change`; `replay` scenario `rejected.replay` | no |
| MPE-SEC-041 | Seen-set entry after Accept | `validator::rejected_copy_does_not_block_valid_copy` | admission stand-in |
| MPE-SEC-009 | Verification backlog bounds | `validator::queue_bounds`: per-peer 8 and total 128 jobs including running ones | no |
| MPE-SEC-010 | Verification scheduling fairness | `node::round_robin_dispatch`: two saturating peers cannot starve a third peer's queue | no |
| MPE-NET-023 | Per-peer per-Shard rate limit | `node::per_peer_rate`: 100/s from one peer on one Shard, verifier calls for that peer ≤ 20/s | no |
| MPE-STO-015 | Restart barrier | `node::restart_barrier`: restart mid-epoch, replay a pre-restart Envelope at 1 s and 141 s, neither Accepted live; genesis exemption tested separately | no |

## M2 Bus Node and overlay (`mpe-node`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-NET-001a | Sidecar process | inspection: `mpe-node` is its own binary with no Midnight node dependency | no |
| MPE-NET-006 | Network-scoped names | `node::genesis_isolation`: two networks sharing a bootstrapper exchange no Envelope | no |
| MPE-NET-007 | Transport baseline | `node::tcp_noise_yamux_pair`: two nodes built with only TCP, Noise and Yamux exchange Envelopes | no |
| MPE-NET-008 | GossipSub v1.1 with scoring | inspection of `config.rs`; `node::scores_visible` reads `peer_score` for every peer | no |
| MPE-NET-009a | StrictNoSign publication | `node::captured_frames_unsigned`: no `from`, `seqno`, `signature` or `key` in captured RPCs | no |
| MPE-NET-009b | Signed-field rejection | `node::signed_message_dropped`: a message carrying any of the four fields is not delivered and the sender's score falls | no |
| MPE-NET-010 | Wire-byte message id | `node::msgid_distinct_for_slot_change`; identical bytes give one id | no |
| MPE-NET-011 | Mesh degree | config dump shows (8, 6, 12, 4); `node::reject_dout_ge_dlo` fails start-up | no |
| MPE-NET-013 | Flood publishing off | `node::first_hop_fanout`: a node with 30 peers sends a fresh Envelope to at most 12 | no |
| MPE-NET-014 | RPC size cap | `node::oversize_rpc_dropped`: 65,537 B is neither delivered nor forwarded | no |
| MPE-NET-015 | Validate before forwarding | `node::held_until_accept`: an Envelope held in validation is seen by no downstream peer until Accept | no |
| MPE-NET-021 | Score penalty signs | `node::p6_colocation` on TCP with 12 peers on one loopback address: all get negative P6; P4 weight negative in config | no |
| MPE-NET-022 | Eviction of misbehaving peers | `node::evict_withholder`: withholding and invalid-only peers pruned within 90 loaded heartbeats at 10/s; no prune in an idle Shard over 300 s | no |
| MPE-NET-031 | Shard topics from the Registry | `node::shard_count_change`: mock Registry 1 to 8 changes the subscribed topic set | mock Registry |
| MPE-NET-033 | Publish ingress hop | `publisher::one_ingress_of_two`: 1,000 publications each reach exactly one first Bus Node, choices span both | no |
| MPE-NET-048 | Shard stream service | `node::feed_complete`: a client pulling one Shard receives every Accepted EID for 10 min | no |
| MPE-NET-049 | Publish acceptance message | `node::ack_only_on_accept`: `Accepted{eid}` for Accepted Envelopes, nothing for Rejected or Ignored | no |
| MPE-NET-054 | Relay list entries | `ledger::relay_entry_fields`: adapter reads peer id, Operator id and the five role flags | mock Registry |
| MPE-OPS-007 | Allow-listed mesh at launch | `node::unlisted_graft_refused`: an unlisted peer's GRAFT is pruned while its published Envelope is still validated | mock Registry |
| MPE-OPS-055 | Mock Operator roster | inspection of the simulator fixture: Bus Nodes and Store Nodes under 3 Operator ids; used by the `stored` and reconciliation tests | mock Registry |

## M3 Client library and Store Node (`mpe-client`, `mpe-node`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-PUB-010 | Local recognition | `leakage` scenario: no recognition key, stream secret or Tag filter in any captured client frame | no |
| MPE-PUB-011 | Full-Shard reception | `baseline` scenario: every Subscriber's received EID count equals the Shard's Accepted count | no |
| MPE-PUB-012 | Network behaviour independent of recognition | `subscriber::paired_traces`: clients with 0 and 256 keys over the same feed send identical request sequences and sizes; KS test on timing, α = 0.01 | no |
| MPE-PUB-014 | Second-source reconciliation | `client::reconcile_repairs_omission`: one source drops 5%, every dropped Envelope arrives from the other Operator within 120 s | no |
| MPE-PUB-015 | Repair every difference | `client::repair_independent_of_keys`: every missing EID's window is back-filled with 0 and with 32 keys | no |
| MPE-PUB-022 | Acceptance before success | `publisher::silent_node_never_accepted` | no |
| MPE-PUB-023 | Identical retransmission | `publisher::retry_to_second_node`: first node blackholed, second receives byte-identical bytes after 5 s | no |
| MPE-PUB-053 | Retransmission stops at epoch end | `publisher::retry_stops_after_epoch_tolerance`: all nodes blackholed across an epoch boundary, retries stop 20 s after the epoch, result `NotAccepted` | no |
| MPE-PUB-030 | Back-fill selectors | inspection of the `/backfill` request type: Shard, time bound and cursor only | no |
| MPE-PUB-031 | Back-fill completeness | `store::backfill_pages`: N held Envelopes return exactly N distinct EIDs in pages of ≤ 64; `backfill` scenario | no |
| MPE-PUB-035 | At-least-once delivery | `churn` scenario after drain; `client::sixteen_nodes_20pct_churn`: 1,000 Envelopes reach every Subscriber | no |
| MPE-PUB-036 | Envelope deduplication | `subscriber::three_paths_one_delivery` (feed, back-fill, repair) | no |
| MPE-PUB-037 | Logical deduplication | `subscriber::same_lei_one_delivery`, overlay and ledger copies | MockLedger |
| MPE-PUB-039 | Gap report | `subscriber::gap_after_120s`: withheld seq 5 gives `gap{5..5}` at 120 ± 1 s | no |
| MPE-PUB-043 | Portable inclusive cursor | `client::switch_store_mid_backfill`: two Store Nodes with different ingest orders, no Envelope skipped | no |
| MPE-CON-015 | Finality label on every Event | `subscriber::exactly_one_finality_label` over all scenarios' deliveries | no |
| MPE-CON-056 | Closed outcome set | inspection of `outcome.rs`; `client::fault_injection_maps_once`: each injected fault yields exactly one of the 19 outcomes | no |
| MPE-CON-057 | Carrier attribute | `client::carrier_attribute`: one Event over overlay, gateway feed and ledger each carries one matching attribute | MockLedger |
| MPE-PRV-013 | Explicit privacy-changing fallback | `client::no_silent_fallback`: overlay disabled, the ledger path stays inactive until the application selects the fallback profile | MockLedger |
| MPE-STO-012 | Stored attribute | `client::stored_needs_three_operators`: duplicate-Operator receipts and receipts naming another EID or deadline are refused | mock Registry (Operator keys) |
| MPE-STO-041 | Inventory listing | `store::inventory_pages`: N seeded EIDs return exactly N across pages | no |
| MPE-STO-042 | Retention receipt request | `store::receipts_by_window`: receipts from 3 Store Nodes validate under the `stored` rule | mock Registry (Operator keys) |
| MPE-NET-056 | Historic root lookup | `store::backfill_after_two_rotations` validates against the historic root and consumes no allowance | mock Registry |

## M4 Ledger, Anchors, contract consumer and fallback (`mpe-core`, `mpe-node`, `mpe-client`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-NET-035 | Ledger Adapter interface | the whole test suite runs against `MockLedger` through the `LedgerAdapter` trait | MockLedger |
| MPE-NET-055 | Ledger Adapter read set | `ledger::reads`: roots with publication and supersession times, relay list, parameters, Anchors, pause flag, `ledgerParameters` | MockLedger |
| MPE-NET-036 | Finalized state only | `ledger::unfinalized_invisible`: a Registry write included but not 3 blocks deep is not returned | MockLedger |
| MPE-STO-001 | No bodies in ledger state | inspection of the mock Registry state type; `ledger::state_writes_have_no_body` | mock Registry |
| MPE-NET-050 | Anchor payload | `anchor::payload_vectors` (44 B at 1 Shard, 72 B at 8); mock Registry decodes every field | mock Registry |
| MPE-NET-051 | Batch root construction | `anchor::rfc6962_vectors`; an independent Merkle implementation in the test reproduces the roots | no |
| MPE-NET-052 | Inclusion path service | `anchor::paths_verify`; a path request for an unanchored EID is refused; `anchor` scenario | MockLedger |
| MPE-CON-016 | Meaning of `final` | `client::final_only_after_finalized_anchor`: forged path and unfinalized Anchor both leave `gossip`; `anchor` scenario | MockLedger |
| MPE-CRY-025 | Secret-bearing consumption nullifiers | `consumer::nullifier_vectors`: same event secret reproduces the nullifier; another contract changes it | mock contract |
| MPE-VER-032 | Contract reaction race | `consumer::hundred_reactors_one_effect` | mock contract |
| MPE-FMT-037 | Carrier-independent body | `fallback::ledger_copy_opens`: body from the `Misc` parts opens as its overlay copy | MockLedger |
| MPE-FMT-040 | Constant `Misc` name | `fallback::constant_name`: parts from two streams carry identical `name` | MockLedger |
| MPE-FMT-041 | Part split | `fallback::part_vectors` for classes 0-2 | MockLedger |
| MPE-FMT-044 | Ledger part limit | `fallback::class3_refused`: error, no transaction built | no |
| MPE-FMT-045 | Ledger reassembly | `fallback::interleaved_intents`: parts of two intents in one block reassemble into two bodies | MockLedger |
| MPE-FMT-046 | Malformed ledger group | `fallback::bad_part_counts`: groups of 2, 3 and 5 parts discarded and counted | MockLedger |
| MPE-CON-053 | Fallback path read | `fallback::indexer_queries`: every MockIndexer call carries only the bus contract address | MockIndexer |

## M5 Simulator, measurement and declarations (`mpe-sim`)

| ID | Title | Proof | Stand-in |
|---|---|---|---|
| MPE-VER-041 | End-to-end Prototype scenario | `mpe-sim e2e`: registration, publication, overlay delivery, recognition, client crash with back-fill resume, `final` label and one mock contract reaction, each logged with EID and LEI | MockLedger, mock contract |
| MPE-SEC-042 | Corrupted-slot front-running test | `node::corrupted_slot_front_run` on 32 in-process Bus Nodes with the adversary adjacent to the ingress node: the honest Envelope reaches every eligible Subscriber within 10 s; repeated at 50 nodes as the `replay` scenario sub-case | admission stand-in |
| MPE-VER-013 | Nominal latency | `baseline` scenario `latency_ms.p99` ≤ 10,000 | admission stand-in |
| MPE-VER-014 | Nominal delivery fraction | `baseline` scenario `delivered.ratio` ≥ 0.999 with the denominator of PROTOTYPE.md 11.4 | admission stand-in |
| MPE-VER-020 | Validation outcome conformance | `validator::outcome_table` plus `malformed` scenario: forwarding and score effects per outcome match the policy | no |
| MPE-VER-021 | Invalid-ingress bounds | `malformed` scenario: sampled queue and cache sizes stay within 8 per peer, 128 per node and the cache caps | no |
| MPE-VER-025 | Store failure recovery | `backfill` scenario: first Store Node stopped, back-fill completes from another Operator's Store Node | no |
| MPE-VER-028 | Interest-swapped executions | `leakage` scenario paired Subscribers with swapped keys produce identical request traces | no |
| MPE-VER-029 | Infrastructure log audit | `leakage` scenario scanner over all logs: zero canaries | no |
| MPE-PRF-003 | Percentiles with delivery denominators | every result JSON: p50, p95, p99 with expected, received and missing counts in `notes` | no |
| MPE-PRF-005 | Measured propagation amplification | `baseline` `notes`: per-node receive and transmit bytes divided by unique Accepted Envelope bytes | no |
| MPE-PRF-010 | Mesh profile comparison | `baseline --mesh 8,6,12,4` and `--mesh 6,5,12,2` at 50 nodes, same seed | no |
| MPE-PRF-019 | Desktop recognition budget | `criterion` bench `recognition`: 100 Envelopes/s, 32 keys, class 2, CPU ≤ 0.5 core | no |
| MPE-PRF-021 | Subscriber download cost | `baseline` `notes`: bytes per delivered Envelope per Subscriber and the daily extrapolation | no |
| MPE-PRF-041 | Bus Node memory ceiling | process resident memory sampled every 10 s in `baseline` at 50 nodes, divided by Bus Node count, plus per-node cache bytes; ≤ 2 GiB | no |
| MPE-CRY-036 | Cryptographic size and cost report | `mpe-sim report-crypto`: byte accounting of every wire field and `criterion` times for seal, open, Tag, sign, verify | no |
| MPE-NET-047 | IDONTWANT measurement | `baseline --idontwant on` and `off`, egress difference per size class | no |
| MPE-PRV-020 | Ledger leakage declaration | `LEAKAGE.md` L-L entry: Registry, Anchor, fallback and reaction transaction fields | MockLedger |
| MPE-PRV-038 | Anchor count leakage | `LEAKAGE.md` L-L names the per-Shard counts and the 60 s window | no |

## Deferred PoC-scope requirements

Listed by area and number.

| Requirement | Reason |
|---|---|
| ECO-048, PRF-017, PRF-018 | Need a real admission prover and verifier; the stand-in's size and time are synthetic |
| VER-005 | 10^9 fuzz iterations do not fit the build budget; `proptest` no-panic properties run instead and are not claimed as this requirement |
| VER-007, VER-008, VER-009 | Bounded state-machine models belong to the Quint work, not the Rust prototype |
| VER-012, PRF-037 | 72 h soak |
| VER-017, VER-018, PRF-032, PRF-033, PRF-038 | Need 200- and 1,000-node adversarial runs with 20% cold-start Sybil attackers; one 6-core host runs 200 nodes only for baseline and churn |
| VER-026 | The CVE-2022-47547 attack trace is not in the local evidence; the eclipse scenario measures a different attack |
| VER-011 | 16 separate local processes; the simulator runs swarms in one process, and a multi-process script follows M5 |
| STO-004, STO-011 | Restart durability of retained Envelopes and receipts; the prototype store is in memory and its receipts say so |
| FMT-032 | rust-libp2p serves IWANT from its message cache without an application hook; exposure is bounded by 5 heartbeats |
| CRY-020 | Needs a compiled Compact fixture |
| NET-037, NET-045, NET-046, VER-030, STO-030, PRF-040 | Need a ledger-8 or ledger-9 devnet, the real Indexer or the Compact toolchain |
| SEC-022 | Only one mock chain source exists, so source agreement cannot be tested |
| VER-019 | 1,000 admission identities; the spam scenario uses one attacker membership and the aggregate-bound test 50 |
| PRF-012, PRF-023, PRF-024 to PRF-031 | Workload suites longer than one scenario or the 10,000-Subscriber gateway topology |
| VER-027 | First-spy instrumentation and estimator are outside the ten scenarios |
| VER-036 | Outside-developer trial |
