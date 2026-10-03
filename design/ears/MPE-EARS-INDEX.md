# MPE requirements index

544 drafted requirements in 12 area files (`design/rounds/r5/`), 28 gap records, 137 in the prototype core.

| ID | Title | Pattern | Scope | Priority | Status | Flags |
|---|---|---|---|---|---|---|
| MPE-CON-001 | Local recognition | ubiquitous | POC | MUST | settled | dup of MPE-PUB-010 |
| MPE-CON-002 | Whole-Shard retrieval by default | state | POC | MUST | open (DEC-CON-1) | dup of MPE-PUB-011 |
| MPE-CON-003 | Recognition-independent requests | ubiquitous | POC | MUST | settled | dup of MPE-PUB-012 |
| MPE-CON-004 | Opt-in for selective profiles | optional | PROD | MUST | open (DEC-CON-1) | dup of MPE-PUB-016 |
| MPE-CON-005 | No silent reception downgrade | unwanted | POC | MUST | settled | dup of MPE-PRV-013; fixed as MPE-CON-005b |
| MPE-CON-006 | Keys only by invitation | ubiquitous | POC | MUST | open (DEC-CON-8) | dup of MPE-PUB-008 |
| MPE-CON-007 | Tag lookahead window | ubiquitous | POC | MUST | open (DEC-CON-2) |  |
| MPE-CON-008 | Recognition-window gap | unwanted | POC | MUST | open (DEC-CON-2) |  |
| MPE-CON-009 | Recognition key cap | unwanted | POC | MUST | settled | dup of MPE-CRY-016 |
| MPE-CON-010 | Generated codecs only | ubiquitous | POC | MUST | settled | dup of MPE-FMT-027 |
| MPE-CON-011 | Undecodable Events delivered | event | POC | SHOULD | settled | dup of MPE-PUB-049 |
| MPE-CON-012 | At-least-once within retention | state | POC | MUST | settled | dup of MPE-PUB-035 |
| MPE-CON-013 | Deduplication by Envelope identifier | ubiquitous | POC | MUST | settled | dup of MPE-PUB-036 |
| MPE-CON-014 | Logical deduplication of retries | ubiquitous | POC | MUST | settled | dup of MPE-PUB-037 |
| MPE-CON-015 | Delivery label on every Event | ubiquitous | POC | MUST | settled | fixed as MPE-CON-015; POC-CORE |
| MPE-CON-016 | Meaning of `final` | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-CON-017 | Upgrade notice from gossip to final | event | POC | MUST | settled |  |
| MPE-CON-018 | Unanchored notice | unwanted | POC | MUST | settled |  |
| MPE-CON-019 | One interface for both labels | ubiquitous | POC | SHOULD | settled |  |
| MPE-CON-020 | Suspected gap | event | POC | MUST | settled | dup of MPE-PUB-039 |
| MPE-CON-021 | Late fill | event | POC | MUST | settled | dup of MPE-PUB-040 |
| MPE-CON-022 | No hidden reordering | ubiquitous | POC | SHOULD | open (DEC-CON-4) | dup of MPE-PUB-038 |
| MPE-CON-023 | Bounded gap state | unwanted | POC | MUST | settled |  |
| MPE-CON-024 | Caught-up marker | event | POC | MUST | settled | dup of MPE-PUB-042 |
| MPE-CON-025 | Transport failures are typed | unwanted | POC | MUST | settled | fixed as MPE-CON-025b |
| MPE-CON-026 | Closed publish result set | event | POC | MUST | settled |  |
| MPE-CON-027 | Portable cursor | ubiquitous | POC | MUST | settled | dup of MPE-PUB-043 |
| MPE-CON-028 | Inclusive resume | event | POC | MUST | settled |  |
| MPE-CON-029 | Back-fill by complete window | ubiquitous | POC | MUST | settled | dup of MPE-STO-017 |
| MPE-CON-030 | Back-fill window reported | ubiquitous | POC | SHOULD | settled |  |
| MPE-CON-031 | Key-erased gap | unwanted | POC | MUST | settled | dup of MPE-PUB-046 |
| MPE-CON-032 | Retention gap | unwanted | POC | MUST | settled | dup of MPE-PUB-045 |
| MPE-CON-033 | Atomic processOnce | ubiquitous | POC | MUST | settled |  |
| MPE-CON-034 | Chaos acceptance | ubiquitous | POC | MUST | settled | dup of MPE-VER-023 |
| MPE-CON-035 | Delivery model check | ubiquitous | POC | SHOULD | settled | dup of MPE-VER-008 |
| MPE-CON-036 | Independent sources by default | ubiquitous | PROD | SHOULD | open (DEC-CON-5) |  |
| MPE-CON-037 | Inventory repair | state | POC | MUST | open (DEC-CON-5) | dup of MPE-PUB-014 |
| MPE-CON-038 | Anchor count check | event | PROD | SHOULD | settled |  |
| MPE-CON-039 | No automatic network action | ubiquitous | POC | MUST | settled |  |
| MPE-CON-040 | Reaction delay | optional | PROD | SHOULD | open (DEC-CON-7) |  |
| MPE-CON-041 | Off-chain blob fetch is explicit | ubiquitous | PROD | SHOULD | settled | dup of MPE-FMT-038 |
| MPE-CON-042 | Contract reaction by later transaction | ubiquitous | PROD | MUST | settled |  |
| MPE-CON-043 | Publisher authorisation in circuit | ubiquitous | PROD | MUST | open (DEC-CON-3) |  |
| MPE-CON-044 | Exactly-once contract effect | ubiquitous | PROD | MUST | settled | fixed as MPE-CON-044b |
| MPE-CON-045 | Secret-derived nullifier | ubiquitous | PROD | MUST | settled | dup of MPE-CRY-025 |
| MPE-CON-046 | Expiry enforced | ubiquitous | PROD | MUST | settled |  |
| MPE-CON-047 | Optional publication proof | optional | PROD | MAY | open (DEC-CON-3) |  |
| MPE-CON-048 | No infrastructure output as authority | ubiquitous | PROD | MUST | settled |  |
| MPE-CON-049 | Reactor race test | ubiquitous | POC | MUST | settled | dup of MPE-VER-032 |
| MPE-CON-050 | Ledger paused | unwanted | POC | MUST | settled |  |
| MPE-CON-051 | Gossip continues while ledger unavailable | state | POC | MUST | settled |  |
| MPE-CON-052 | Wallet grants | optional | PROD | SHOULD | open (DEC-CON-6) |  |
| MPE-CON-053 | Fallback path read | state | POC | MUST | settled | POC-CORE |
| MPE-CON-054 | Consumer bandwidth metering | ubiquitous | POC | SHOULD | settled |  |
| MPE-CON-055 | Afternoon test | ubiquitous | PROD | SHOULD | settled | dup of MPE-VER-036 |
| MPE-CRY-001 | Default cryptographic profile | ubiquitous | POC | MUST | open (DEC-CRY-1) | POC-CORE |
| MPE-CRY-002 | Sealed application metadata | ubiquitous | POC | MUST | settled |  |
| MPE-CRY-003 | Authenticated padding | ubiquitous | POC | MUST | settled | dup of MPE-FMT-016 |
| MPE-CRY-004 | Public-context authentication | ubiquitous | POC | MUST | settled | fixed as MPE-CRY-004; POC-CORE |
| MPE-CRY-005 | Acyclic Envelope construction | ubiquitous | POC | MUST | settled | dup of MPE-FMT-020 |
| MPE-CRY-006 | Domain separation | ubiquitous | POC | MUST | settled |  |
| MPE-CRY-007 | Purpose-specific derivation | ubiquitous | POC | MUST | open (DEC-CRY-2) |  |
| MPE-CRY-008 | Random stream secrets | event | POC | MUST | settled | fixed as MPE-CRY-008; POC-CORE |
| MPE-CRY-009 | Randomness failure | unwanted | POC | MUST | settled |  |
| MPE-CRY-010 | Nonce uniqueness | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-CRY-011 | Unsafe restored state | unwanted | POC | MUST | settled |  |
| MPE-CRY-012 | Exact retransmission | event | POC | MUST | settled | dup of MPE-PUB-023 |
| MPE-CRY-013 | Salted private Tags | event | POC | MUST | open (DEC-CRY-2) | POC-CORE |
| MPE-CRY-014 | Recognition is provisional | event | POC | MUST | settled | POC-CORE |
| MPE-CRY-015 | Local Tag recognition | ubiquitous | POC | MUST | settled | dup of MPE-PUB-010 |
| MPE-CRY-016 | Recognition-key bound | event | POC | MUST | open (DEC-CRY-2) | POC-CORE |
| MPE-CRY-017 | Ambiguous opening | unwanted | POC | MUST | settled |  |
| MPE-CRY-018 | Authenticated invitations | event | POC | MUST | open (DEC-CRY-3) |  |
| MPE-CRY-019 | Revocation rekeying | event | POC | MUST | settled |  |
| MPE-CRY-020 | Publisher signature profile | ubiquitous | POC | MUST | open (DEC-CRY-6) |  |
| MPE-CRY-021 | Signed statement binding | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-CRY-022 | Authenticated delivery | event | POC | MUST | settled | POC-CORE |
| MPE-CRY-023 | Failure-atomic cryptographic state | event | POC | MUST | settled |  |
| MPE-CRY-024 | Authenticated logical replay | unwanted | POC | MUST | settled | dup of MPE-PUB-037 |
| MPE-CRY-025 | Secret-bearing consumption nullifiers | optional | POC | MUST | settled | POC-CORE |
| MPE-CRY-026 | Explicit security posture | ubiquitous | POC | MUST | settled |  |
| MPE-CRY-027 | Seed-restoration boundary | optional | PROD | MUST | open (DEC-CRY-1) |  |
| MPE-CRY-028 | Encrypted-header session profile | optional | PROD | SHOULD | open (DEC-CRY-1) |  |
| MPE-CRY-029 | Ratchet-key erasure | event | PROD | MUST | open (DEC-CRY-1) |  |
| MPE-CRY-030 | Bounded skipped-key retention | state | PROD | MUST | open (DEC-CRY-1) |  |
| MPE-CRY-031 | Explicit cryptographic gaps | unwanted | PROD | MUST | open (DEC-CRY-1) |  |
| MPE-CRY-032 | Hybrid session establishment | optional | PROD | SHOULD | open (DEC-CRY-4) |  |
| MPE-CRY-033 | Wrapped bootstrap metadata | optional | PROD | MUST | open (DEC-CRY-4) |  |
| MPE-CRY-034 | One-time prekey consumption | event | PROD | MUST | settled |  |
| MPE-CRY-035 | Establishment failure | unwanted | PROD | MUST | open (DEC-CRY-4) |  |
| MPE-CRY-036 | Cryptographic size and cost report | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-CRY-037 | Fuzzy-detection activation | event | POC | MUST | open (DEC-CRY-5) |  |
| MPE-CRY-038 | Restricted detection delegation | optional | PROD | MUST | open (DEC-CRY-5) |  |
| MPE-CRY-039 | FMD construction measurement | optional | POC | MUST | open (DEC-CRY-5) |  |
| MPE-CRY-040 | Production composition gate | ubiquitous | PROD | MUST | settled | dup of MPE-VER-037 |
| MPE-ECO-001 | No proof-of-work admission | ubiquitous | POC | MUST | settled |  |
| MPE-ECO-002 | DUST is not operator payment | ubiquitous | POC | MUST | settled |  |
| MPE-ECO-003 | No Midnight transaction per overlay Event | ubiquitous | POC | MUST | open (DEC-ECO-1) | dup of MPE-NET-002 |
| MPE-ECO-004 | DUST-paid membership registration | event | PROD | MUST | open (DEC-ECO-1) |  |
| MPE-ECO-005 | Sponsored registration | ubiquitous | PROD | SHOULD | settled |  |
| MPE-ECO-006 | Dedicated admission secret | ubiquitous | POC | MUST | settled |  |
| MPE-ECO-007 | Shielded fee payment | ubiquitous | PROD | MUST | settled |  |
| MPE-ECO-008 | Live fee quotes | event | PROD | MUST | settled |  |
| MPE-ECO-009 | Insufficient DUST reported before proving | unwanted | PROD | SHOULD | settled |  |
| MPE-ECO-010 | Client back-off under chain congestion | state | PROD | SHOULD | settled |  |
| MPE-ECO-011 | Chain-share budget | ubiquitous | PROD | SHOULD | open (DEC-ECO-6) |  |
| MPE-ECO-012 | Admission Proof required | unwanted | POC | MUST | settled | POC-CORE |
| MPE-ECO-013 | Cheap checks before proof verification | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-ECO-014 | Epoch freshness | unwanted | POC | MUST | settled | POC-CORE |
| MPE-ECO-015 | Root window | unwanted | POC | MUST | settled | fixed as MPE-ECO-015; POC-CORE |
| MPE-ECO-016 | Committed rate limit | ubiquitous | POC | MUST | open (DEC-ECO-1) | fixed as MPE-ECO-016; POC-CORE |
| MPE-ECO-017 | Size-class credit weight | ubiquitous | POC | MUST | open (DEC-ECO-4) | fixed as MPE-ECO-017; POC-CORE |
| MPE-ECO-018 | Content-bound Admission Proof | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-ECO-019 | Duplicate nullifier, same Envelope | unwanted | POC | MUST | settled | dup of MPE-PUB-028 |
| MPE-ECO-020 | Equivocation detected | unwanted | POC | MUST | settled | fixed as MPE-ECO-020; POC-CORE |
| MPE-ECO-021 | Nullifier retention | ubiquitous | POC | MUST | settled |  |
| MPE-ECO-022 | Aggregate admission bound | state | POC | MUST | settled | POC-CORE |
| MPE-ECO-023 | Per-peer pre-verification limit | unwanted | POC | MUST | settled | dup of MPE-NET-023 |
| MPE-ECO-024 | Stale Registry view | unwanted | POC | MUST | settled | dup of MPE-NET-018 |
| MPE-ECO-025 | Continuity when Registry calls are paused | state | PROD | MUST | settled | dup of MPE-NET-038 |
| MPE-ECO-026 | Membership expiry | event | PROD | MUST | open (DEC-ECO-5) |  |
| MPE-ECO-027 | Root publication time recorded | ubiquitous | PROD | MUST | settled |  |
| MPE-ECO-028 | Revocation on evidence | event | PROD | MUST | open (DEC-ECO-2) |  |
| MPE-ECO-029 | Revocation takes effect | event | PROD | MUST | settled |  |
| MPE-ECO-030 | No per-Envelope ledger state | ubiquitous | PROD | MUST | settled |  |
| MPE-ECO-031 | Equivocation evidence retention | ubiquitous | PROD | SHOULD | settled |  |
| MPE-ECO-032 | Bond custody | optional | PROD | MAY | open (DEC-ECO-2) |  |
| MPE-ECO-033 | Slash split | complex | PROD | MAY | open (DEC-ECO-2) |  |
| MPE-ECO-034 | Registry funds invariant | optional | PROD | MUST | settled |  |
| MPE-ECO-035 | Maintainer cannot move bonds | ubiquitous | PROD | MUST | settled |  |
| MPE-ECO-036 | Registration publicity disclosed | optional | PROD | MUST | settled |  |
| MPE-ECO-037 | No protocol pay for relaying | ubiquitous | PROD | MUST | open (DEC-ECO-3) |  |
| MPE-ECO-038 | No performance-score payouts | ubiquitous | PROD | SHOULD | open (DEC-ECO-3) |  |
| MPE-ECO-039 | Treasury runway cap | optional | PROD | MUST | open (DEC-ECO-3) |  |
| MPE-ECO-040 | Per-key saturation cap | optional | PROD | SHOULD | open (DEC-ECO-3) |  |
| MPE-ECO-041 | Store Node retention challenge | complex | PROD | MAY | open (DEC-ECO-3) |  |
| MPE-ECO-042 | Missed challenge forfeits bond | complex | PROD | MAY | open (DEC-ECO-3) |  |
| MPE-ECO-043 | Unlinkable paid back-fill | optional | PROD | MAY | open (DEC-ECO-3) |  |
| MPE-ECO-044 | Overload refuses new Envelopes | unwanted | POC | MUST | settled | dup of MPE-PRF-034 |
| MPE-ECO-045 | Shed the largest class first | state | PROD | SHOULD | settled |  |
| MPE-ECO-046 | Cover Envelopes are admitted normally | optional | PROD | MAY | open (DEC-ECO-7) |  |
| MPE-ECO-047 | Prototype admission over a mocked ledger | ubiquitous | POC | MUST | settled | dup of MPE-NET-035 |
| MPE-ECO-048 | Admission-proof measurement gate | ubiquitous | POC | MUST | settled |  |
| MPE-ECO-049 | Registration-cost gate | ubiquitous | PROD | MUST | settled |  |
| MPE-ECO-050 | Flood-cost analysis published | ubiquitous | PROD | SHOULD | settled |  |
| MPE-FMT-001 | Fixed-width visible layout | ubiquitous | POC | MUST | settled | fixed as MPE-FMT-001b |
| MPE-FMT-002 | Byte order | ubiquitous | POC | MUST | open (DEC-FMT-7) |  |
| MPE-FMT-003 | Visible fields | ubiquitous | POC | MUST | open (DEC-FMT-2) | POC-CORE |
| MPE-FMT-004 | No identity-derived visible values | ubiquitous | POC | MUST | open (DEC-FMT-2) | POC-CORE |
| MPE-FMT-005 | Admission Slot unlinkability | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-FMT-006 | Reserved bytes | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-007 | Exact length | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-008 | Unknown size class | unwanted | POC | MUST | settled |  |
| MPE-FMT-009 | Structural checks first | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-FMT-010 | Transmit size bound | ubiquitous | POC | MUST | settled | dup of MPE-NET-014 |
| MPE-FMT-011 | Body-blind validation | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-FMT-012 | GossipSub carriage | ubiquitous | POC | MUST | settled | dup of MPE-NET-009 |
| MPE-FMT-013 | Sealed Body length | ubiquitous | POC | MUST | open (DEC-FMT-1) | POC-CORE |
| MPE-FMT-014 | Smallest fitting class | event | POC | MUST | settled | POC-CORE |
| MPE-FMT-015 | Oversize payload | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-016 | Sealed padding | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-FMT-017 | Padding check | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-018 | Envelope Identifier | ubiquitous | POC | MUST | open (DEC-FMT-3) | POC-CORE |
| MPE-FMT-019 | GossipSub message id | ubiquitous | POC | MUST | settled | dup of MPE-NET-010 |
| MPE-FMT-020 | Acyclic construction | ubiquitous | POC | MUST | settled |  |
| MPE-FMT-021 | Network binding | unwanted | POC | MUST | settled |  |
| MPE-FMT-022 | Logical Event Identifier | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-FMT-023 | Version bound to topic | unwanted | POC | MUST | open (DEC-FMT-4) | POC-CORE |
| MPE-FMT-024 | Version overlap | optional | PROD | SHOULD | open (DEC-FMT-4) | fixed as MPE-FMT-024 |
| MPE-FMT-025 | Unsupported sealed format | unwanted | POC | MUST | settled |  |
| MPE-FMT-026 | Unknown schema | event | POC | MUST | settled | dup of MPE-PUB-049 |
| MPE-FMT-027 | Static decoder dispatch | ubiquitous | POC | MUST | settled |  |
| MPE-FMT-028 | Expiry field | ubiquitous | POC | MUST | open (DEC-FMT-5) | POC-CORE |
| MPE-FMT-029 | Expiry too far ahead | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-030 | Expired on arrival | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-031 | Unsafe clock | state | POC | SHOULD | settled | fixed as MPE-FMT-031; POC-CORE |
| MPE-FMT-032 | No forwarding after expiry | event | POC | MUST | settled |  |
| MPE-FMT-033 | Lifetime ceiling | ubiquitous | PROD | MUST | settled |  |
| MPE-FMT-034 | Sealed Prefix | ubiquitous | POC | MUST | open (DEC-FMT-7) |  |
| MPE-FMT-035 | Sealed control packets | ubiquitous | PROD | MUST | settled |  |
| MPE-FMT-036 | No receipt kind | ubiquitous | POC | MUST | open (DEC-FMT-6) |  |
| MPE-FMT-037 | Carrier-independent body | ubiquitous | POC | MUST | open (DEC-FMT-8) | POC-CORE |
| MPE-FMT-038 | Explicit external fetch | ubiquitous | POC | MUST | settled |  |
| MPE-FMT-039 | Optional fragmentation | optional | PROD | MAY | open (DEC-FMT-6) |  |
| MPE-FMT-040 | Constant `Misc` name | ubiquitous | POC | MUST | open (DEC-FMT-8) | POC-CORE |
| MPE-FMT-041 | Part split | ubiquitous | POC | MUST | open (DEC-FMT-1) | POC-CORE |
| MPE-FMT-042 | One phase | ubiquitous | PROD | MUST | settled |  |
| MPE-FMT-043 | One `Misc` per emit | ubiquitous | POC | MUST | settled |  |
| MPE-FMT-044 | Ledger part limit | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-045 | Ledger reassembly | event | POC | MUST | settled | POC-CORE |
| MPE-FMT-046 | Malformed ledger group | unwanted | POC | MUST | settled | POC-CORE |
| MPE-FMT-047 | Anchor event | ubiquitous | PROD | MUST | settled |  |
| MPE-FMT-048 | Admission Slot measurement | ubiquitous | POC | MUST | open (DEC-FMT-1) | dup of MPE-ECO-048 |
| MPE-FMT-049 | Test vectors | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-001 | Sidecar process | ubiquitous | POC | MUST | settled | fixed as MPE-NET-001b |
| MPE-NET-002 | Overlay at launch | ubiquitous | POC | MUST | open (DEC-NET-1) |  |
| MPE-NET-003 | No node change | ubiquitous | PROD | MUST | settled |  |
| MPE-NET-004 | Validators not required | ubiquitous | PROD | MUST | settled | dup of MPE-OPS-001 |
| MPE-NET-005 | Distinct peer identity | ubiquitous | POC | MUST | settled |  |
| MPE-NET-006 | Network-scoped names | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-007 | Transport baseline | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-008 | GossipSub v1.1 with scoring | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-009 | StrictNoSign policy | ubiquitous | POC | MUST | settled | fixed as MPE-NET-009b |
| MPE-NET-010 | Content-addressed message id | ubiquitous | POC | MUST | settled | fixed as MPE-NET-010; POC-CORE |
| MPE-NET-011 | Mesh degree | ubiquitous | POC | MUST | open (DEC-NET-3) | POC-CORE |
| MPE-NET-012 | Timing parameters | ubiquitous | POC | SHOULD | open (DEC-NET-3) |  |
| MPE-NET-013 | Flood publishing off | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-014 | RPC size cap | unwanted | POC | MUST | settled | POC-CORE |
| MPE-NET-015 | Validate before forwarding | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-016 | Reject outcome | unwanted | POC | MUST | settled | POC-CORE |
| MPE-NET-017 | Ignore outcome | unwanted | POC | MUST | settled | dup of MPE-PUB-028; fixed as MPE-NET-017 |
| MPE-NET-018 | Stale chain view yields Ignore | state | POC | MUST | settled | fixed as MPE-NET-018; POC-CORE |
| MPE-NET-019 | Clock and stall detection | unwanted | POC | MUST | settled |  |
| MPE-NET-020 | Source disagreement | unwanted | PROD | MUST | settled |  |
| MPE-NET-021 | Score penalty signs | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-022 | Eviction of misbehaving peers | event | POC | MUST | settled | fixed as MPE-NET-022; POC-CORE |
| MPE-NET-023 | Per-peer rate limit | unwanted | POC | MUST | settled | fixed as MPE-NET-023; POC-CORE |
| MPE-NET-024 | Bootstrapper mode | optional | POC | SHOULD | settled |  |
| MPE-NET-025 | Bootstrapper set | ubiquitous | PROD | MUST | settled |  |
| MPE-NET-026 | Bootstrap list authenticity | event | PROD | SHOULD | settled |  |
| MPE-NET-027 | Peer Exchange acceptance | ubiquitous | PROD | MUST | settled |  |
| MPE-NET-028 | Outbound quota sources | ubiquitous | POC | MUST | settled |  |
| MPE-NET-029 | No local-network discovery | state | POC | MUST | settled |  |
| MPE-NET-030 | Warm-up before injection | state | PROD | SHOULD | settled |  |
| MPE-NET-031 | Shard topics from the Registry | ubiquitous | POC | MUST | open (DEC-NET-4) | POC-CORE |
| MPE-NET-032 | Shard-count transition | event | PROD | SHOULD | settled | dup of MPE-PUB-003 |
| MPE-NET-033 | Publish ingress hop | event | POC | SHOULD | open (DEC-NET-6) | POC-CORE |
| MPE-NET-034 | Relay allow-list | optional | POC | SHOULD | open (DEC-NET-7) | dup of MPE-OPS-007 |
| MPE-NET-035 | Ledger Adapter interface | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-036 | Finalized state only | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-NET-037 | Contract-state read path | ubiquitous | POC | MUST | open (DEC-NET-5) |  |
| MPE-NET-038 | Relaying during a governance pause | state | PROD | MUST | settled |  |
| MPE-NET-039 | Registry fields | ubiquitous | POC | MUST | settled |  |
| MPE-NET-040 | Fixed `Misc` names | ubiquitous | PROD | MUST | settled |  |
| MPE-NET-041 | Anchor cadence | optional | PROD | SHOULD | settled | fixed as MPE-NET-041 |
| MPE-NET-042 | Explicit fallback label | event | POC | MUST | settled |  |
| MPE-NET-043 | Gateway fallback | optional | PROD | SHOULD | open (DEC-NET-2) | fixed as MPE-NET-043b |
| MPE-NET-044 | Ledger fallback | optional | PROD | MAY | open (DEC-NET-2) |  |
| MPE-NET-045 | Unmodified Indexer | ubiquitous | POC | MUST | settled |  |
| MPE-NET-046 | Unmodified Compact toolchain | ubiquitous | POC | MUST | settled |  |
| MPE-NET-047 | IDONTWANT measurement | ubiquitous | POC | SHOULD | settled | POC-CORE |
| MPE-OPS-001 | No validator duty | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-002 | Separate network identity | ubiquitous | POC | MUST | settled | dup of MPE-NET-005 |
| MPE-OPS-003 | Separate bootstrap set | ubiquitous | POC | MUST | settled | dup of MPE-NET-025 |
| MPE-OPS-004 | Bootstrapper profile | optional | POC | SHOULD | settled | dup of MPE-NET-024 |
| MPE-OPS-005 | Role trust disclosure | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-006 | Content-blind roles | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-007 | Allow-listed mesh at launch | state | POC | MUST | open (DEC-OPS-1) | POC-CORE |
| MPE-OPS-008 | Allow-list removal gate | ubiquitous | PROD | MUST | open (DEC-OPS-1) |  |
| MPE-OPS-009 | Launch operator count | state | PROD | MUST | open (DEC-OPS-6) |  |
| MPE-OPS-010 | Concentration cap | ubiquitous | PROD | MUST | open (DEC-OPS-6) |  |
| MPE-OPS-011 | Gates counted per organization | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-012 | Parameter time-lock | event | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-013 | Emergency expiry | unwanted | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-014 | Exits survive a bus pause | complex | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-015 | No revocation by fiat | ubiquitous | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-016 | Maintenance notice | event | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-017 | Measure maintenance constraints | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-018 | Public governance events | event | PROD | MUST | settled |  |
| MPE-OPS-019 | Steward diversity | optional | PROD | MUST | open (DEC-OPS-2) |  |
| MPE-OPS-020 | Governance end state | ubiquitous | PROD | SHOULD | open (DEC-OPS-2) | fixed as MPE-OPS-020 |
| MPE-OPS-021 | Overlay survives a chain pause | state | POC | MUST | settled | dup of MPE-NET-038 |
| MPE-OPS-022 | Stale view gives Ignore | unwanted | POC | MUST | settled | dup of MPE-NET-018 |
| MPE-OPS-023 | Ejection takes effect | event | POC | MUST | settled |  |
| MPE-OPS-024 | Evidence-only ejection when open | state | PROD | MUST | open (DEC-OPS-2) | fixed as MPE-OPS-024 |
| MPE-OPS-025 | Tombstone deletion | complex | PROD | SHOULD | open (DEC-OPS-5) | dup of MPE-STO-036 |
| MPE-OPS-026 | Tombstoned Envelope not relayed | event | POC | SHOULD | open (DEC-OPS-5) | fixed as MPE-OPS-026 |
| MPE-OPS-027 | Transparency report | ubiquitous | PROD | SHOULD | open (DEC-OPS-5) |  |
| MPE-OPS-028 | Abuse report on explicit action only | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-029 | No IP persistence | ubiquitous | POC | MUST | settled | dup of MPE-SEC-027 |
| MPE-OPS-030 | Debug logging expires | unwanted | POC | SHOULD | settled |  |
| MPE-OPS-031 | Canary probes | ubiquitous | PROD | SHOULD | open (DEC-OPS-4) |  |
| MPE-OPS-032 | Canaries look ordinary | ubiquitous | PROD | SHOULD | open (DEC-OPS-4) |  |
| MPE-OPS-033 | Aggregated counters only | optional | PROD | SHOULD | open (DEC-OPS-4) | fixed as MPE-OPS-033b |
| MPE-OPS-034 | Multi-monitor decisions | ubiquitous | PROD | MUST | open (DEC-OPS-4) |  |
| MPE-OPS-035 | Version overlap | event | POC | MUST | settled | dup of MPE-FMT-024 |
| MPE-OPS-036 | Version deny-list | event | POC | SHOULD | open (DEC-OPS-2) |  |
| MPE-OPS-037 | Relay key handover | ubiquitous | PROD | SHOULD | settled |  |
| MPE-OPS-038 | Signed reproducible releases | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-039 | Sev1 mitigation time | event | PROD | SHOULD | settled | fixed as MPE-OPS-039 |
| MPE-OPS-040 | Post-mortem | event | PROD | SHOULD | settled |  |
| MPE-OPS-041 | Pause drill | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-042 | Gated phases | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-043 | Evidence freeze | event | PROD | MUST | settled | fixed as MPE-OPS-043 |
| MPE-OPS-044 | Ledger-generation gate | state | PROD | MUST | settled |  |
| MPE-OPS-045 | Prototype on a mock adapter | ubiquitous | POC | MUST | settled | dup of MPE-NET-035 |
| MPE-OPS-046 | Measured Registry costs | event | PROD | MUST | settled | dup of MPE-VER-030; fixed as MPE-OPS-046 |
| MPE-OPS-047 | Scoring-CVE gate | event | POC | MUST | settled | dup of MPE-VER-026; fixed as MPE-OPS-047 |
| MPE-OPS-048 | Audit gate | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-049 | Permissioned-phase exit | ubiquitous | PROD | MUST | settled | dup of MPE-VER-038 |
| MPE-OPS-050 | Counsel-memo gate | ubiquitous | PROD | SHOULD | open (DEC-OPS-5) |  |
| MPE-OPS-051 | Funding gate | ubiquitous | PROD | MUST | open (DEC-OPS-3) |  |
| MPE-OPS-052 | Anonymity-claim gate | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-053 | Course-change register | ubiquitous | PROD | MUST | settled |  |
| MPE-OPS-054 | Launch sequencing | state | PROD | SHOULD | open (DEC-OPS-7) |  |
| MPE-PRF-001 | Complete traffic accounting | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-002 | Reproducible benchmark manifest | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-003 | Percentiles with delivery denominators | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PRF-004 | Separate latency stages | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-005 | Measured propagation amplification | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PRF-006 | Sustained Shard capacity | state | PROD | MUST | open (DEC-PRF-1) | fixed as MPE-PRF-006 |
| MPE-PRF-007 | Normal-load delivery | state | POC | MUST | open (DEC-PRF-3) | fixed as MPE-PRF-007 |
| MPE-PRF-008 | Median warm propagation | state | PROD | MUST | open (DEC-PRF-3) |  |
| MPE-PRF-009 | Tail warm propagation | state | PROD | MUST | open (DEC-PRF-3) |  |
| MPE-PRF-010 | Mesh profile comparison | ubiquitous | POC | MUST | open (DEC-PRF-2) | POC-CORE |
| MPE-PRF-011 | Gossip-factor retry | unwanted | POC | MUST | settled |  |
| MPE-PRF-012 | Degree-transient cost | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-013 | Edge bandwidth budget | state | PROD | MUST | open (DEC-PRF-4) | fixed as MPE-PRF-013 |
| MPE-PRF-014 | Full bandwidth budget | state | PROD | MUST | open (DEC-PRF-4) | fixed as MPE-PRF-014 |
| MPE-PRF-015 | Edge CPU budget | state | PROD | MUST | open (DEC-PRF-4) |  |
| MPE-PRF-016 | Full CPU budget | state | PROD | MUST | open (DEC-PRF-4) |  |
| MPE-PRF-017 | Admission validation benchmark | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-018 | Publication preparation benchmark | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-019 | Desktop recognition budget | state | POC | MUST | open (DEC-PRF-4) | POC-CORE |
| MPE-PRF-020 | Mobile recognition boundary | optional | POC | SHOULD | open (DEC-PRF-4) |  |
| MPE-PRF-021 | Subscriber download cost | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PRF-022 | Edge stream concurrency | ubiquitous | POC | MUST | open (DEC-PRF-5) |  |
| MPE-PRF-023 | Gateway Subscriber capacity | state | POC | SHOULD | open (DEC-PRF-5) | fixed as MPE-PRF-023 |
| MPE-PRF-024 | Gateway resource curve | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-025 | Fifty-per-second comparison | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-026 | Aggregate load ladder | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-027 | Burst workloads | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-028 | Shard concentration | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-029 | Recovery contention | state | POC | MUST | settled |  |
| MPE-PRF-030 | Epoch synchronization burst | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-031 | Invalid-ingress resource cost | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-032 | Attack delivery floor | state | POC | MUST | open (DEC-PRF-3) |  |
| MPE-PRF-033 | Attack propagation tail | state | POC | MUST | open (DEC-PRF-3) |  |
| MPE-PRF-034 | Queue overflow response | unwanted | POC | MUST | open (DEC-PRF-4) |  |
| MPE-PRF-035 | Explicit capacity failure | event | POC | MUST | settled |  |
| MPE-PRF-036 | Stream bandwidth refusal | unwanted | POC | MUST | open (DEC-PRF-5) |  |
| MPE-PRF-037 | Sustained soak | ubiquitous | POC | MUST | settled |  |
| MPE-PRF-038 | Performance stop classification | unwanted | POC | MUST | open (DEC-PRF-3) |  |
| MPE-PRF-039 | Indexer fan-out comparison | optional | POC | MUST | open (DEC-PRF-6) |  |
| MPE-PRF-040 | Measured ledger capacity comparison | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-001 | Claim register | ubiquitous | PROD | MUST | settled |  |
| MPE-PRV-002 | Content confidentiality | ubiquitous | PROD | MUST | settled |  |
| MPE-PRV-003 | Sealed logical labels | ubiquitous | POC | MUST | settled | dup of MPE-FMT-003 |
| MPE-PRV-004 | Recipient-key-hiding claim gate | ubiquitous | PROD | MUST | open (DEC-PRV-3) |  |
| MPE-PRV-005 | Length concealment within a class | ubiquitous | POC | MUST | settled | dup of MPE-FMT-013 |
| MPE-PRV-006 | Conditional subscriber-interest privacy | state | POC | MUST | open (DEC-PRV-1) |  |
| MPE-PRV-007 | Local recognition secrets | state | POC | MUST | open (DEC-PRV-1) |  |
| MPE-PRV-008 | No private selection predicates | state | POC | MUST | open (DEC-PRV-1) | dup of MPE-PUB-010 |
| MPE-PRV-009 | Recognition-independent transport | state | POC | MUST | settled | dup of MPE-PUB-012 |
| MPE-PRV-010 | No recognition acknowledgements | event | POC | MUST | settled | dup of MPE-CON-039 |
| MPE-PRV-011 | Explicit application reactions | event | POC | MUST | open (DEC-PRV-2) | dup of MPE-PUB-047 |
| MPE-PRV-012 | Overload preserves the privacy boundary | unwanted | POC | MUST | open (DEC-PRV-1) | dup of MPE-PRV-013 |
| MPE-PRV-013 | Explicit privacy-changing fallback | unwanted | POC | MUST | settled | POC-CORE |
| MPE-PRV-014 | Recognition-free remote diagnostics | state | POC | MUST | settled |  |
| MPE-PRV-015 | Explicit plaintext disclosure | event | POC | MUST | settled |  |
| MPE-PRV-016 | Bus Node leakage declaration | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-017 | Store Node leakage declaration | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-018 | Admission issuer leakage declaration | optional | POC | MUST | settled |  |
| MPE-PRV-019 | Indexer leakage declaration | optional | POC | MUST | settled |  |
| MPE-PRV-020 | Ledger leakage declaration | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PRV-021 | Collusion leakage declaration | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-022 | Global-observer leakage declaration | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-023 | Insider leakage declaration | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-024 | Launch metadata non-claims | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-025 | No anonymity from unsigned transactions | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-026 | Launch compromise-security posture | ubiquitous | POC | MUST | open (DEC-PRV-4) |  |
| MPE-PRV-027 | No launch post-quantum claim | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-028 | No adversarial archive-erasure claim | ubiquitous | POC | MUST | settled |  |
| MPE-PRV-029 | No inherited stem anonymity | optional | POC | MUST | settled |  |
| MPE-PRV-030 | Evidence before advertising a property | event | PROD | MUST | settled |  |
| MPE-PRV-031 | Paired selection verification | ubiquitous | POC | MUST | settled | dup of MPE-VER-028 |
| MPE-PRV-032 | Active selection verification | ubiquitous | POC | MUST | settled | dup of MPE-VER-028 |
| MPE-PRV-033 | Attribution measurements | ubiquitous | POC | MUST | settled | dup of MPE-VER-027 |
| MPE-PRV-034 | Bound applicability | event | PROD | MUST | settled |  |
| MPE-PRV-035 | Violated-claim withdrawal | unwanted | PROD | MUST | settled |  |
| MPE-PRV-036 | Unknown leakage inventory | event | POC | MUST | settled |  |
| MPE-PRV-037 | Separate stronger-profile evidence | optional | PROD | MUST | settled |  |
| MPE-PUB-001 | Topic identifiers sealed | ubiquitous | POC | MUST | settled | dup of MPE-FMT-003 |
| MPE-PUB-002 | Shard derivation | ubiquitous | POC | MUST | open (DEC-PUB-1) | fixed as MPE-PUB-002; POC-CORE |
| MPE-PUB-003 | Bus Node shard-count transition | event | PROD | MUST | settled |  |
| MPE-PUB-004 | Client shard-count transition | event | PROD | MUST | settled |  |
| MPE-PUB-005 | Per-Envelope Tag | ubiquitous | POC | MUST | open (DEC-PUB-2) | dup of MPE-CRY-013 |
| MPE-PUB-006 | Random private audience keys | ubiquitous | POC | MUST | settled | dup of MPE-CRY-008; fixed as MPE-PUB-006 |
| MPE-PUB-007 | Public topic key | optional | POC | SHOULD | settled |  |
| MPE-PUB-008 | Invitation-only private membership | ubiquitous | POC | MUST | open (DEC-PUB-3) |  |
| MPE-PUB-009 | No subscriber directory | ubiquitous | POC | MUST | settled |  |
| MPE-PUB-010 | Local recognition | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-011 | Full-Shard reception | state | POC | MUST | settled | POC-CORE |
| MPE-PUB-012 | Network behaviour independent of recognition | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-013 | Fixed pull cadence | state | POC | SHOULD | open (DEC-PUB-4) |  |
| MPE-PUB-014 | Second-source reconciliation | state | POC | SHOULD | open (DEC-PUB-4) | fixed as MPE-PUB-014; POC-CORE |
| MPE-PUB-015 | Repair every difference | event | POC | SHOULD | open (DEC-PUB-4) | fixed as MPE-PUB-015; POC-CORE |
| MPE-PUB-016 | Reduced-privacy mode opt-in | optional | PROD | MUST | open (DEC-PUB-5) |  |
| MPE-PUB-017 | Report disclosed Shards | ubiquitous | POC | SHOULD | settled |  |
| MPE-PUB-018 | Recognition key cap | unwanted | POC | MUST | settled | dup of MPE-CRY-016 |
| MPE-PUB-019 | Per-publisher sequence number | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-020 | Logical event identifier | ubiquitous | POC | MUST | settled | dup of MPE-FMT-022 |
| MPE-PUB-021 | Oversize refusal | unwanted | POC | MUST | settled | dup of MPE-FMT-015 |
| MPE-PUB-022 | Acceptance before success | event | POC | MUST | settled | POC-CORE |
| MPE-PUB-023 | Identical retransmission | complex | POC | MUST | settled | POC-CORE |
| MPE-PUB-024 | Publication failure | unwanted | POC | MUST | settled |  |
| MPE-PUB-025 | Closed error set | ubiquitous | POC | MUST | settled |  |
| MPE-PUB-026 | GossipSub message identifier | ubiquitous | POC | MUST | settled | dup of MPE-NET-010 |
| MPE-PUB-027 | Seen-set until expiry | ubiquitous | POC | MUST | settled | fixed as MPE-PUB-027; POC-CORE |
| MPE-PUB-028 | Duplicate is Ignore | event | POC | MUST | settled | POC-CORE |
| MPE-PUB-029 | Expired on arrival is Ignore | unwanted | POC | MUST | settled | dup of MPE-FMT-030 |
| MPE-PUB-030 | Back-fill selectors | ubiquitous | POC | MUST | open (DEC-PUB-5) | POC-CORE |
| MPE-PUB-031 | Back-fill completeness | event | POC | MUST | settled | POC-CORE |
| MPE-PUB-032 | Refusal is distinguishable | unwanted | POC | MUST | settled |  |
| MPE-PUB-033 | Pull capacity | unwanted | POC | MUST | settled | dup of MPE-PRF-022 |
| MPE-PUB-034 | Busy fail-over | event | POC | MUST | settled |  |
| MPE-PUB-035 | At-least-once delivery | state | POC | MUST | settled | fixed as MPE-PUB-035; POC-CORE |
| MPE-PUB-036 | Envelope deduplication | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-037 | Logical deduplication | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-038 | Arrival-order delivery | ubiquitous | POC | MUST | open (DEC-PUB-6) |  |
| MPE-PUB-039 | Gap report | unwanted | POC | MUST | settled | POC-CORE |
| MPE-PUB-040 | Late fill | event | POC | MUST | settled |  |
| MPE-PUB-041 | Gap becomes lost | unwanted | POC | MUST | settled |  |
| MPE-PUB-042 | Caught-up marker | event | POC | MUST | settled |  |
| MPE-PUB-043 | Portable inclusive cursor | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-PUB-044 | Atomic processing helper | optional | POC | MUST | settled | dup of MPE-CON-033 |
| MPE-PUB-045 | Retention exceeded | unwanted | POC | MUST | settled |  |
| MPE-PUB-046 | Key erased | unwanted | PROD | MUST | settled |  |
| MPE-PUB-047 | Reactions only on explicit call | ubiquitous | POC | MUST | settled |  |
| MPE-PUB-048 | External object fetch | optional | PROD | SHOULD | settled | dup of MPE-FMT-038 |
| MPE-PUB-049 | Unknown schema | unwanted | POC | MUST | settled |  |
| MPE-PUB-050 | Disconnected status | unwanted | POC | MUST | settled |  |
| MPE-PUB-051 | Validation before forwarding | ubiquitous | POC | MUST | settled | dup of MPE-NET-015 |
| MPE-PUB-052 | Subscriber bandwidth measurement | ubiquitous | POC | MUST | settled | dup of MPE-PRF-021 |
| MPE-SEC-001 | Launch relay admission | state | POC | MUST | open (DEC-SEC-1) | dup of MPE-OPS-007 |
| MPE-SEC-002 | Bootstrap source diversity | event | POC | MUST | settled | dup of MPE-NET-026 |
| MPE-SEC-003 | Outbound connection protection | event | POC | MUST | open (DEC-SEC-2) | dup of MPE-NET-011 |
| MPE-SEC-004 | Active peer scoring | ubiquitous | POC | MUST | settled | dup of MPE-NET-008 |
| MPE-SEC-005 | Admission before forwarding | ubiquitous | POC | MUST | settled |  |
| MPE-SEC-006 | Cheap framing checks | unwanted | POC | MUST | settled | dup of MPE-FMT-009 |
| MPE-SEC-007 | Rejection of proven invalidity | unwanted | POC | MUST | settled | dup of MPE-NET-016 |
| MPE-SEC-008 | Ignore local uncertainty | unwanted | POC | MUST | settled | dup of MPE-NET-018 |
| MPE-SEC-009 | Verification backlog bounds | ubiquitous | POC | MUST | open (DEC-SEC-3) | POC-CORE |
| MPE-SEC-010 | Verification scheduling fairness | state | POC | MUST | open (DEC-SEC-3) | POC-CORE |
| MPE-SEC-011 | Retrieval abuse limits | unwanted | POC | MUST | settled |  |
| MPE-SEC-012 | Storage exhaustion response | unwanted | POC | MUST | settled | dup of MPE-STO-009 |
| MPE-SEC-013 | Historical admission separation | event | POC | MUST | settled |  |
| MPE-SEC-014 | Proof-independent deduplication | ubiquitous | POC | MUST | settled |  |
| MPE-SEC-015 | Durable admission replay state | ubiquitous | POC | MUST | settled | fixed as MPE-SEC-015 |
| MPE-SEC-016 | Missing replay-state recovery | unwanted | POC | MUST | settled | dup of MPE-STO-015 |
| MPE-SEC-017 | Replay-state pruning boundary | ubiquitous | POC | MUST | settled | dup of MPE-ECO-021 |
| MPE-SEC-018 | Conflicting allowance use | unwanted | POC | MUST | open (DEC-SEC-4) |  |
| MPE-SEC-019 | Conflict alarm | event | POC | MUST | open (DEC-SEC-4) |  |
| MPE-SEC-020 | Authenticated key changes | unwanted | POC | MUST | settled |  |
| MPE-SEC-021 | Independent retrieval comparison | event | POC | MUST | settled | dup of MPE-PUB-014 |
| MPE-SEC-022 | Authenticate Registry read results | unwanted | POC | MUST | settled | fixed as MPE-SEC-022 |
| MPE-SEC-023 | Recognition-independent omission repair | event | POC | MUST | settled | dup of MPE-PUB-015 |
| MPE-SEC-024 | Report unresolved retrieval | unwanted | POC | MUST | settled |  |
| MPE-SEC-025 | Recognition-independent network behavior | ubiquitous | POC | MUST | settled | dup of MPE-PUB-012 |
| MPE-SEC-026 | Prevent silent privacy fallback | unwanted | POC | MUST | settled | dup of MPE-PRV-013 |
| MPE-SEC-027 | Persistent logging limits | ubiquitous | PROD | MUST | settled |  |
| MPE-SEC-028 | Compromised-key send suspension | unwanted | POC | MUST | settled |  |
| MPE-SEC-029 | Admission-key separation | ubiquitous | POC | MUST | settled | dup of MPE-ECO-006 |
| MPE-SEC-030 | Authentication before session mutation | optional | PROD | MUST | settled | dup of MPE-CRY-023 |
| MPE-SEC-031 | Missing session-update response | complex | PROD | MUST | settled |  |
| MPE-SEC-032 | Payload execution boundary | ubiquitous | POC | MUST | settled |  |
| MPE-SEC-033 | Unwanted-contact rejection | unwanted | POC | MUST | settled |  |
| MPE-SEC-034 | Authenticated tombstone deletion | optional | PROD | MUST | open (DEC-SEC-5) | dup of MPE-STO-036 |
| MPE-SEC-035 | Delivery during ledger interruption | state | POC | MUST | settled | dup of MPE-NET-038 |
| MPE-SEC-036 | Ledger-dependent failure reporting | unwanted | POC | MUST | settled | dup of MPE-CON-050 |
| MPE-SEC-037 | Contract authorization predicate | ubiquitous | POC | MUST | settled | dup of MPE-CON-043 |
| MPE-SEC-038 | Atomic contract replay protection | ubiquitous | POC | MUST | settled | dup of MPE-CON-044 |
| MPE-SEC-039 | Configuration-specific attack evidence | ubiquitous | POC | MUST | settled |  |
| MPE-SEC-040 | Scoring vulnerability release gate | ubiquitous | POC | MUST | open (DEC-SEC-6) | dup of MPE-VER-026 |
| MPE-STO-001 | Bodies remain off the ledger | ubiquitous | POC | MUST | settled | fixed as MPE-STO-001; POC-CORE |
| MPE-STO-002 | Shard-scoped commitments | ubiquitous | POC | MUST | open (DEC-STO-1) |  |
| MPE-STO-003 | Reject excessive ordinary retention | unwanted | POC | MUST | open (DEC-STO-1) | fixed as MPE-STO-003 |
| MPE-STO-004 | Retain accepted Envelopes | event | POC | MUST | open (DEC-STO-1) |  |
| MPE-STO-005 | Complete verification material | ubiquitous | POC | MUST | open (DEC-STO-2) |  |
| MPE-STO-006 | Retrieval does not refresh retention | event | POC | MUST | settled |  |
| MPE-STO-007 | Expiry pruning | event | POC | MUST | settled |  |
| MPE-STO-008 | Per-Shard disk bound | ubiquitous | POC | MUST | settled |  |
| MPE-STO-009 | Refuse storage overload | unwanted | POC | MUST | open (DEC-STO-3) |  |
| MPE-STO-010 | Refuse cache overload | unwanted | POC | MUST | settled |  |
| MPE-STO-011 | Receipt follows persistence | event | POC | MUST | open (DEC-STO-5) |  |
| MPE-STO-012 | Stored delivery label | ubiquitous | POC | MUST | open (DEC-STO-5) | fixed as MPE-STO-012; POC-CORE |
| MPE-STO-013 | Application identifier cache | ubiquitous | POC | MUST | settled | dup of MPE-PUB-027 |
| MPE-STO-014 | Admission replay retention | ubiquitous | POC | MUST | settled | dup of MPE-ECO-021 |
| MPE-STO-015 | Restart recovery barrier | state | POC | MUST | open (DEC-STO-7) | fixed as MPE-STO-015; POC-CORE |
| MPE-STO-016 | Historical admission context | event | POC | MUST | open (DEC-STO-2) |  |
| MPE-STO-017 | Recognition-independent requests | event | POC | MUST | settled |  |
| MPE-STO-018 | Complete retained interval | event | POC | MUST | settled | dup of MPE-PUB-031 |
| MPE-STO-019 | Explicit unavailable ranges | unwanted | POC | MUST | settled |  |
| MPE-STO-020 | Corrupt stored records | unwanted | POC | MUST | settled |  |
| MPE-STO-021 | Bounded optional archives | optional | PROD | MAY | open (DEC-STO-1) |  |
| MPE-STO-022 | Recoverable history capability | event | POC | MUST | settled |  |
| MPE-STO-023 | Client payload cache bound | ubiquitous | POC | MUST | settled |  |
| MPE-STO-024 | Discard unmatched Envelopes | event | POC | MUST | settled |  |
| MPE-STO-025 | Durable recovery checkpoint | event | POC | MUST | settled |  |
| MPE-STO-026 | Missing recovery keys | unwanted | POC | MUST | settled | dup of MPE-PUB-046 |
| MPE-STO-027 | Unknown Indexer retention | unwanted | POC | MUST | settled |  |
| MPE-STO-028 | Bounded Anchor record count | ubiquitous | POC | MUST | open (DEC-STO-4) |  |
| MPE-STO-029 | Anchor age pruning | event | POC | MUST | open (DEC-STO-4) |  |
| MPE-STO-030 | Measure Anchor storage | ubiquitous | POC | MUST | open (DEC-STO-4) |  |
| MPE-STO-031 | Per-Shard Operator replication | state | PROD | MUST | open (DEC-STO-5) |  |
| MPE-STO-032 | Measured retention availability | state | PROD | SHOULD | open (DEC-STO-5) |  |
| MPE-STO-033 | Storage failure experiments | ubiquitous | POC | MUST | settled |  |
| MPE-STO-034 | Measure storage by node class | ubiquitous | POC | MUST | settled |  |
| MPE-STO-035 | Auxiliary state pruning | event | POC | MUST | settled |  |
| MPE-STO-036 | Authorized tombstone deletion | optional | PROD | MUST | open (DEC-STO-6) |  |
| MPE-STO-037 | Reject unauthorized deletion | unwanted | POC | MUST | settled |  |
| MPE-STO-038 | Prevent tombstone reinsertion | optional | PROD | MUST | open (DEC-STO-6) |  |
| MPE-STO-039 | Separate inclusion and storage evidence | ubiquitous | POC | MUST | settled |  |
| MPE-STO-040 | Verification cache validity | unwanted | POC | MUST | settled |  |
| MPE-VER-001 | Reproducible acceptance profile | ubiquitous | POC | MUST | settled |  |
| MPE-VER-002 | Claim register | ubiquitous | PROD | MUST | settled | dup of MPE-PRV-001 |
| MPE-VER-003 | Failed phase gate | unwanted | POC | MUST | open (DEC-VER-1) |  |
| MPE-VER-004 | Wire conformance | ubiquitous | POC | MUST | settled |  |
| MPE-VER-005 | Decoder fuzzing | ubiquitous | POC | MUST | open (DEC-VER-3) |  |
| MPE-VER-006 | Actual cryptographic costs | ubiquitous | POC | MUST | settled | dup of MPE-CRY-036 |
| MPE-VER-007 | Admission model | ubiquitous | POC | MUST | open (DEC-VER-4) |  |
| MPE-VER-008 | Delivery-state model | ubiquitous | POC | MUST | settled |  |
| MPE-VER-009 | Contract-consumption model | ubiquitous | POC | MUST | settled |  |
| MPE-VER-010 | Governance model gate | optional | PROD | MUST | open (DEC-VER-4) |  |
| MPE-VER-011 | Local multi-node demonstration | ubiquitous | POC | MUST | open (DEC-VER-1) |  |
| MPE-VER-012 | Nominal soak | ubiquitous | POC | MUST | open (DEC-VER-2) |  |
| MPE-VER-013 | Nominal latency | state | POC | MUST | open (DEC-VER-2) | POC-CORE |
| MPE-VER-014 | Nominal delivery fraction | state | POC | MUST | open (DEC-VER-2) | POC-CORE |
| MPE-VER-015 | Resource acceptance | unwanted | POC | MUST | settled |  |
| MPE-VER-016 | Measurement report | event | POC | MUST | settled |  |
| MPE-VER-017 | Scale simulations | ubiquitous | POC | MUST | open (DEC-VER-2) |  |
| MPE-VER-018 | Adversarial dissemination gate | state | POC | MUST | open (DEC-VER-2) |  |
| MPE-VER-019 | Admission abuse gate | ubiquitous | POC | MUST | settled |  |
| MPE-VER-020 | Validation outcome conformance | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-VER-021 | Invalid-ingress bounds | state | POC | MUST | settled | POC-CORE |
| MPE-VER-022 | Burst recovery | event | POC | MUST | open (DEC-VER-2) |  |
| MPE-VER-023 | Recovery completeness | ubiquitous | POC | MUST | settled |  |
| MPE-VER-024 | Atomic consumer deduplication | optional | POC | MUST | settled |  |
| MPE-VER-025 | Store failure recovery | event | POC | MUST | settled | POC-CORE |
| MPE-VER-026 | Scoring attack regression | ubiquitous | POC | MUST | settled |  |
| MPE-VER-027 | First-spy measurement | ubiquitous | POC | MUST | open (DEC-VER-5) |  |
| MPE-VER-028 | Interest-swapped executions | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-VER-029 | Infrastructure log audit | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-VER-030 | Ledger integration measurements | ubiquitous | POC | MUST | settled |  |
| MPE-VER-031 | Concurrent Anchor validity | ubiquitous | POC | MUST | settled |  |
| MPE-VER-032 | Contract reaction race | ubiquitous | POC | MUST | settled | POC-CORE |
| MPE-VER-033 | Hostile bridge inputs | ubiquitous | POC | MUST | settled |  |
| MPE-VER-034 | Deployment capability gate | unwanted | PROD | MUST | settled |  |
| MPE-VER-035 | Ledger Adapter failure | event | POC | MUST | settled |  |
| MPE-VER-036 | Outside-developer usability | ubiquitous | POC | SHOULD | open (DEC-VER-3) |  |
| MPE-VER-037 | Independent review gate | ubiquitous | PROD | MUST | settled |  |
| MPE-VER-038 | Production canary gate | state | PROD | MUST | open (DEC-VER-6) |  |
| MPE-VER-039 | Pause and resume drill | optional | PROD | MUST | open (DEC-VER-6) | dup of MPE-OPS-041 |
| MPE-VER-040 | Open admission gate | unwanted | PROD | MUST | open (DEC-VER-6) | dup of MPE-OPS-008; fixed as MPE-VER-040 |
| MPE-FMT-050 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-FMT-051 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-FMT-052 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-FMT-053 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-CRY-041 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-ECO-051 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-ECO-052 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-ECO-053 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-SEC-041 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-SEC-042 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-STO-041 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-STO-042 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-048 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-049 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-050 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-051 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-052 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-053 | (gap record) | | | | | added by reconciliation |
| MPE-NET-054 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-055 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-NET-056 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-PRF-041 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-CON-056 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-CON-057 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-PUB-053 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-PRV-038 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-OPS-055 | (gap record) | | | | | added by reconciliation; POC-CORE |
| MPE-VER-041 | (gap record) | | | | | added by reconciliation; POC-CORE |
