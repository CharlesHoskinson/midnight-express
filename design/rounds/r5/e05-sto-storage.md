## Scope of this area

STO owns D6: Envelope retention, storage by node class, pruning, back-fill storage, availability commitments, caches and deduplication state.
The recommended Prototype uses per-Shard Store Nodes with a bounded ordinary retention window; Bus Nodes without storage duties retain transport and admission state.
Event bodies remain off the ledger, including the `Misc` fallback; the Registry retains bounded metadata and Anchor records.
Retention promises are conditional on surviving reachable holders and recoverable client keys; expiry does not guarantee deletion of other parties’ copies.
Envelope encoding, admission rules, cryptographic recovery, delivery semantics, Operator funding and transport configuration belong to the dependent areas identified below.

## Parameters

These are proposed defaults, not measured capacities. **Assumption** marks a new engineering choice or an unsupported range. Changing a retention parameter does not extend existing signed commitments or application execution deadlines.

| Parameter | Meaning | Default | Allowed range | Source |
|---|---|---:|---|---|
| P-STO-1 | Maximum ordinary Envelope retention lifetime, measured from authenticated creation time | 172,800 seconds (48 hours) | 3,600–604,800 seconds; **assumption** for range | g3, s3 R1 §D6; g3 R2 §D6; DEC-STO-1 |
| P-STO-2 | Maximum delay for removing an expired record from managed live storage | 60 seconds | 1–600 seconds; **assumption** | s3, s4 R1 §D6 require bounded pruning; numeric default is **assumption** |
| P-STO-3 | Store Node disk allocation per retained Shard, including indexes, journals and temporary database files | 32 GiB | 1 GiB–1 TiB; **assumption** | g3 R1 §D6 per-Shard accounting; s3 R1 §D6 provisioning approach; per-Shard default is **assumption** |
| P-STO-4 | Bus Node allocation for application storage caches, including deduplication, replay and verification-cache metadata | 1 GiB | 64 MiB–8 GiB; **assumption** | o4 R1 §D6 estimates relay caches below 1 GB; exact allocation is **assumption** |
| P-STO-5 | Number of distinct Operators required for the `stored` label and per-Shard storage deployment | 3 Operators | 3–12 Operators; upper bound is **assumption** | g3, o4, s2, s3 R1 §D6 |
| P-STO-6 | Additional Envelope identifier retention after its retention deadline | 3,600 seconds | 0–86,400 seconds; **assumption** for range | g1 R1 §D6 proposes one additional hour |
| P-STO-7 | Optional archive agreement duration, measured from authenticated creation time | 604,800 seconds (7 days) | Greater than P-STO-1, up to 2,592,000 seconds (30 days); range is a proposed service policy | s3 R1 §D6: 7 days; g3: 14 days; s4: 30 days |
| P-STO-8 | Client Event payload cache allocation | 200 MB | 0–1,000 MB; **assumption** | g3 R1 §D6 explicitly labels 200 MB an assumption |
| P-STO-9 | Maximum age of live Registry Anchor records | 604,800 seconds (7 days) | 172,800–1,209,600 seconds; **assumption** for range | o4 R1 §D6: 7 days; o2: 14 days; DEC-STO-4 |
| P-STO-10 | Maximum live Registry Anchor records, including records retained by an Anchor-history representation | 10,080 records | 1–20,160 records; capacity must cover the NET anchoring schedule within P-STO-9 | o4 R1 §D6: 10,080 windows; o2: 20,160 slots |
| P-STO-11 | Interval between scheduled per-Shard availability probes | 60 seconds | 1–3,600 seconds; **assumption** for range | o4 R1 §D7 canaries |
| P-STO-12 | Successful within-retention canary retrieval target | 99.9% | 99.9–100%; **assumption** for range | o4 R1 §D6 proposed completeness target |
| P-STO-13 | Availability assessment interval | 86,400 seconds (24 hours) | 3,600–604,800 seconds; **assumption** | o4 R1 §D6 monitoring direction; interval is **assumption** |
| P-STO-14 | Maximum deletion delay after an authorized tombstone, where that feature is enabled | 172,800 seconds (48 hours) | 0–172,800 seconds; **assumption** for range | o4 R1 §D7 Operator Agreement |

MB means 1,000,000 bytes; GiB means 1,073,741,824 bytes; TiB means 1,099,511,627,776 bytes.

Storage planning uses complete Envelope bytes, not plaintext or proof-stripped body sizes:

`raw bytes per replica = accepted Envelopes/second × mean Envelope bytes × retention seconds`.

The following are arithmetic fixtures from g3’s proposals, not additional performance requirements:

| Fixture | Raw storage per Shard over the default window | With an assumed 2× storage multiplier |
|---|---:|---:|
| g3 R1 L1: 2.5 Envelopes/second, 4,096 bytes/Envelope | 1,769,472,000 bytes; 1.648 GiB | 3.296 GiB |
| g3 R2 example: 6.25 Envelopes/second, 2,400 bytes/Envelope | 2,592,000,000 bytes; 2.414 GiB | 4.828 GiB |
| g3 R1 byte cap: 65,536 Envelope bytes/second | 11,324,620,800 bytes; 10.547 GiB | 21.094 GiB |

The 2× multiplier is **assumption**. At the last fixture, eight Shards require 84.375 GiB raw per complete replica. P-STO-3 provides provisional headroom per Shard; actual database amplification, compaction space and admission metadata sizes are **unknown** until MPE-STO-034 is demonstrated.

## Requirements

Source conventions: `R1` and `R2` identify the supplied proposal and review directories; role IDs identify their corresponding files. Midnight paths are relative to `/home/charl/midnight/`; libp2p paths are relative to `/home/charl/libp2p/`. Revision-qualified ledger citations identify the node-pinned ledger-9 generation. `settled` denotes consistency with the fixed brief or an uncontested storage invariant, not a claimed Round 3 consensus vote.

### MPE-STO-001 Bodies remain off the ledger
The MPE shall exclude Event bodies from all ledger writes, including the `Misc` fallback.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3, s2, s3 R1 §D6; BRIEF system definition; midnight-ledger@54a4e013/onchain-vm/src/vm.rs:268
- Rationale: The fixed architecture reserves the ledger for metadata and commitments.
- Verify: inspection, inspect Registry state and captured ledger-write arguments for Event body bytes.
- Status: settled

### MPE-STO-002 Shard-scoped commitments
The Store Node shall scope each retention commitment to a named Shard.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D6; g3 R2 §D6; o4 R1 §D6
- Rationale: Storage responsibility follows the Shards an Operator has undertaken to retain.
- Verify: test, commit retention for one Shard without creating retention obligations for another.
- Status: open (DEC-STO-1)

### MPE-STO-003 Reject excessive ordinary retention
If an ordinary Envelope’s authenticated retention deadline exceeds its authenticated creation time by more than P-STO-1, then the Store Node shall reject its storage admission.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D6 and §D10; s3 R1 §D6
- Rationale: Publisher-selected deadlines cannot create unbounded ordinary storage obligations.
- Verify: test, check admission immediately below, at and above the configured lifetime limit.
- Status: open (DEC-STO-1)

### MPE-STO-004 Retain accepted Envelopes
When an ordinary Envelope is accepted for storage, the Store Node shall retain it until its authenticated retention deadline unless an authorized tombstone applies.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; g3, s3 R1 §D6; o4 R1 §D7
- Rationale: A storage commitment covers accepted data through its stated deadline, subject to the explicitly selected deletion policy.
- Verify: test, retrieve committed Envelopes throughout their window across process restarts.
- Status: open (DEC-STO-1)

### MPE-STO-005 Complete verification material
The Store Node shall retain the complete Envelope verification material throughout its retention commitment.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; s2, s4 R2 §D6 objections to o1 and o2 proof stripping; s3 R1 §D6
- Rationale: An Anchor or proof hash does not replace the Admission Proof needed for independent historical verification.
- Verify: demonstration, verify a retrieved Envelope with a fresh client lacking the Store Node’s verification cache.
- Status: open (DEC-STO-2)

### MPE-STO-006 Retrieval does not refresh retention
When an Envelope is retrieved or received again, the Store Node shall preserve its existing retention deadline.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; s3 R1 §D6; s2 R1 §D1
- Rationale: Access time and retransmission do not authorize a new storage window.
- Verify: test, repeatedly retrieve and replay an Envelope near its deadline without extending retention.
- Status: settled

### MPE-STO-007 Expiry pruning
When an Envelope’s retention commitment expires, the Store Node shall remove its record from managed live storage within P-STO-2.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; g3, s3, s4 R1 §D6; P-STO-2 is assumption
- Rationale: Logical pruning bounds ordinary storage without claiming physical erasure of every historical copy.
- Verify: test, advance the clock beyond expiry and inspect live records after the pruning allowance.
- Status: settled

### MPE-STO-008 Per-Shard disk bound
The Store Node shall keep its allocated storage for each retained Shard at or below P-STO-3.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D6 and §D9; s3 R1 §D6; allocation is assumption
- Rationale: The allocation includes Envelope records, indexes, journals and temporary database files.
- Verify: test, measure allocated files during sustained ingest, pruning and compaction at the configured limit.
- Status: settled

### MPE-STO-009 Refuse storage overload
If accepting an Envelope would exceed its Shard’s P-STO-3 allocation, then the Store Node shall reject that storage admission with `STORAGE_FULL`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; g1 R1 §D6 refusal policy; g3 R1 §D9; g2 R1 §D6 competing eviction policy
- Rationale: Refusal preserves existing commitments instead of silently sacrificing retained data.
- Verify: test, fill the allocation and confirm explicit refusal while previously committed Envelopes remain retrievable.
- Status: open (DEC-STO-3)

### MPE-STO-010 Refuse cache overload
If live admission would exceed P-STO-4 for application storage caches, then the Bus Node shall reject that admission with `RESOURCE_EXHAUSTED`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; o4 R1 §D6; g3 R1 §D9; exact allocation is assumption
- Rationale: Capacity exhaustion cannot justify discarding still-required replay protection.
- Verify: test, exhaust cache allocation and confirm rejection without eviction of unexpired protection records.
- Status: settled

### MPE-STO-011 Receipt follows persistence
When the Store Node issues a retention receipt, the Store Node shall sign it only after committing the identified Envelope to storage recoverable after process restart.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; s2, s3 R1 §D6; s4 R2 §D6
- Rationale: The receipt attributes a persistence obligation to its Operator; it does not prove future availability.
- Verify: test, interrupt the process around receipt issuance and recover every Envelope covered by an issued receipt.
- Status: open (DEC-STO-5)

### MPE-STO-012 Stored delivery label
The MPE client library shall assign the `stored` label only after validating compatible retention receipts from at least P-STO-5 distinct Operators.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; s1, s2, s3 R1 §D6
- Rationale: Distinct peer identities alone do not establish distinct Operators.
- Verify: test, reject duplicate-Operator receipts and receipts naming different Envelopes or commitment deadlines.
- Status: open (DEC-STO-5)

### MPE-STO-013 Application identifier cache
The Bus Node shall retain each accepted Envelope identifier in its application deduplication cache until the Envelope’s retention deadline plus P-STO-6.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g1 R1 §D6; o1 R1 §D3; rust-libp2p/protocols/gossipsub/src/config.rs:524
- Rationale: GossipSub’s short duplicate cache is independent of the application replay horizon.
- Verify: test, replay an Envelope after transport-cache eviction but before application-cache expiry and confirm duplicate recognition.
- Status: settled

### MPE-STO-014 Admission replay retention
The Bus Node shall retain each consumed admission replay identifier until the latest time at which its authorization can pass the live-admission predicate.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D3 and §D9; s3 R1 §D6; s2 R2 §D9
- Rationale: Replay-state expiry follows admission eligibility, including the admission area’s clock tolerance.
- Verify: test, attempt reuse across every accepted epoch boundary and after the authorization becomes permanently ineligible.
- Status: settled

### MPE-STO-015 Restart recovery barrier
While required admission replay state has not been recovered after restart, the Bus Node shall refuse live admission.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D9; s2 R2 §D9
- Rationale: A restart cannot silently restore consumed publication allowances.
- Verify: test, restart with missing or stale replay state and confirm refusal until reconstruction completes or affected authorizations expire.
- Status: open (DEC-STO-7)

### MPE-STO-016 Historical admission context
When serving back-fill, the Store Node shall provide the retained context needed to validate the Envelope’s Admission Proof against its historical Registry state.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; s3 R1 §D6; s2 R2 §D6
- Rationale: Historical retrieval uses the original authorization context rather than a current membership assumption.
- Verify: demonstration, retrieve after Registry membership rotation and independently validate the original admission.
- Status: open (DEC-STO-2)

### MPE-STO-017 Recognition-independent requests
When requesting back-fill, the MPE client library shall request complete intervals of its selected Shards without selecting Envelopes by recognition results.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D3; s2, s3 R1 §D3; 2020-vac-waku2-store-spec, “Security Consideration”
- Rationale: Matching Tags, object identifiers and content filters would reveal interests to the storage provider.
- Verify: test, compare requests from clients with different recognition keys but identical Shard and interval selections.
- Status: settled

### MPE-STO-018 Complete retained interval
When an authorized back-fill request covers an available interval, the Store Node shall return every retained Envelope in that interval across its paginated response.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D3; s2, s3 R1 §D3; 2020-vac-waku2-store-spec, “Content filtered queries”
- Rationale: Completeness is relative to this Store Node’s retained inventory, not the global publication stream.
- Verify: test, compare all returned pages with a seeded inventory using inclusive start and exclusive end boundaries.
- Status: settled

### MPE-STO-019 Explicit unavailable ranges
If a back-fill request includes a known unavailable interval, then the Store Node shall identify that interval in a `RETENTION_GAP` response.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; s2, s3 R1 §D6; o3 R1 §D6
- Rationale: Expiry, deletion and known loss must not appear as a successfully empty history.
- Verify: test, request across expired, deleted and known lost intervals and inspect the reported boundaries.
- Status: settled

### MPE-STO-020 Corrupt stored records
If a stored Envelope fails its identifier or retained verification checks, then the Store Node shall return `CORRUPT_RECORD` for the affected record.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; s3 R1 §D6 historical validation; s2, s4 R2 §D6 complete verifiable records; response code is assumption
- Rationale: Corrupt bytes cannot count as successful recovery.
- Verify: test, mutate retained body and Admission Proof bytes and confirm a failure response instead of valid Envelope delivery.
- Status: settled

### MPE-STO-021 Bounded optional archives
Where an archive service is present, the Store Node shall retain archived Envelopes only through their separately agreed deadlines within P-STO-7.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D6; g3, s2, s3 R1 §D6; s4 R1 §D6
- Rationale: Longer retention is a separately funded service rather than an ordinary protocol duty.
- Verify: inspection, inspect archive agreements and demonstrate removal from managed archive storage after their deadlines.
- Status: open (DEC-STO-1)

### MPE-STO-022 Recoverable history capability
When a Subscriber queries recovery capabilities, the MPE client library shall report recoverable history as the intersection of advertised remote retention coverage and locally available decryption-state coverage.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; o3 R1 §D6; s2 R1 §D3 and R2 §D6
- Rationale: A stored ciphertext window can exceed the client’s decryptable history.
- Verify: test, independently shorten remote retention and local key coverage and check the reported intersection.
- Status: settled

### MPE-STO-023 Client payload cache bound
The MPE client library shall limit its local Event payload cache to P-STO-8.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D6; default and range are assumption
- Rationale: Application payload history is bounded independently of keys, cursors and replay state.
- Verify: test, exceed the configured payload allocation, including a zero allocation, and measure retained payload bytes.
- Status: settled

### MPE-STO-024 Discard unmatched Envelopes
When local recognition of an unmatched Envelope completes, the MPE client library shall discard its Envelope bytes from the recognition buffer.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; s1 R1 §D6; s2 R1 §D3
- Rationale: Whole-Shard fetching does not require retaining unrelated ciphertext indefinitely.
- Verify: test, process an unmatched interval and inspect recognition-buffer contents after completion.
- Status: settled

### MPE-STO-025 Durable recovery checkpoint
When committing a recovery checkpoint, the MPE client library shall persist its cursor and corresponding logical deduplication state as one atomic checkpoint.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; s2 R1 §D3 and §D6; s2 R2 §D3
- Rationale: A crash must not restore a cursor without the state needed to suppress repeated logical Events.
- Verify: test, inject failures during checkpoint persistence and recover either the preceding or completed checkpoint.
- Status: settled

### MPE-STO-026 Missing recovery keys
If retained ciphertext requires decryption state that is unavailable, then the MPE client library shall report `KEY_GAP` for the affected recovery range.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; s2 R1 §D3; s2 R2 §D6
- Rationale: Ciphertext availability does not establish decryptability after arbitrary session gaps.
- Verify: test, remove required recovery keys while preserving remote Envelopes and confirm an explicit key-gap result.
- Status: settled

### MPE-STO-027 Unknown Indexer retention
If contract-event retention coverage has not been established for an Indexer, then the Indexer adapter shall report that coverage as `unknown`.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; g2 R1 §D6; s2, s4 R2 §D6; midnight-indexer/chain-indexer/config.yaml:14
- Rationale: Ledger-state retention is not evidence of contract-event row retention.
- Verify: test, configure only ledger-state retention and confirm that no contract-event retention guarantee is inferred.
- Status: settled

### MPE-STO-028 Bounded Anchor record count
The Registry shall retain no more than P-STO-10 live Anchor records.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; o2, o4 R1 §D6; g1 R2 §D6
- Rationale: The bound includes Anchor records hidden in an underlying history representation.
- Verify: test, insert beyond the configured capacity and inspect the complete reachable live Anchor state.
- Status: open (DEC-STO-4)

### MPE-STO-029 Anchor age pruning
When an Anchor record becomes older than P-STO-9, the Registry shall remove that record from its live Anchor state on the next successful Anchor-maintenance transaction.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; o4 R1 §D6; o2 R1 §D6; s4 R1 §D6
- Rationale: Custom Anchor history requires explicit maintenance; ledger TTL does not prune it.
- Verify: test, advance ledger time through a maintenance outage and confirm removal when maintenance resumes.
- Status: open (DEC-STO-4)

### MPE-STO-030 Measure Anchor storage
The Prototype shall report reachable live Anchor-state bytes after each insertion, replacement and pruning operation during a run exceeding P-STO-10 insertions.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; o2 R1 §D6; g1, s4 R2 §D6; minokawa-compact/doc/ledger-adt.mdx:603
- Rationale: Slot counts alone do not establish bounded tree history or actual ledger write cost.
- Verify: demonstration, publish a revision-qualified ledger-9 measurement showing state growth before and after capacity is reached.
- Status: open (DEC-STO-4)

### MPE-STO-031 Per-Shard Operator replication
While a Shard advertises ordinary back-fill service, the MPE shall maintain storage commitments for that Shard from at least P-STO-5 distinct Operators.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D6; g3, o4 R1 §D6; s2, s3 R1 §D6
- Rationale: Operator diversity is an operational condition, not proof of independent failure probabilities.
- Verify: inspection, audit Operator ownership and active Shard retention commitments.
- Status: open (DEC-STO-5)

### MPE-STO-032 Measured retention availability
While a Shard advertises ordinary back-fill service, the MPE shall achieve at least P-STO-12 successful scheduled canary retrievals at P-STO-11 intervals during each P-STO-13 assessment interval.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: D6; o4 R1 §D6 and §D7; assessment interval is assumption
- Rationale: The denominator includes missed probes for canaries previously labeled stored and still within retention; PRF defines retrieval timeouts.
- Verify: analysis, calculate success from scheduled probes, counting unavailable Envelopes, corrupt results and timeouts as failures.
- Status: open (DEC-STO-5)

### MPE-STO-033 Storage failure experiments
The Prototype shall report within-retention retrieval outcomes for experiments covering individual Store Node loss, correlated Operator loss and partitions extending beyond retention.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; s2 R1 §D10; s3 R1 §D6; g3 R1 §D6
- Rationale: Receipts, Anchors and replica counts do not establish unconditional delivery.
- Verify: simulation, compare retained inventories with recovered inventories under each named failure condition.
- Status: settled

### MPE-STO-034 Measure storage by node class
The Prototype shall report peak storage allocations by node class under the PRF workload profiles, separately accounting for Envelope bytes, indexes, caches, replay state and database temporary files.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; g3, o2, o4, s2, s3 R1 §D6; g3 R2 §D6
- Rationale: Proposal sizing uses incompatible Envelope layouts and unmeasured database multipliers.
- Verify: demonstration, reconcile measured totals for Bus Nodes, Store Nodes and clients with their configured allocations.
- Status: settled

### MPE-STO-035 Auxiliary state pruning
When an application cache record’s protection or verification lifetime ends, the Bus Node shall remove that record within P-STO-2.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D6; g3, o4, s4 R1 §D6
- Rationale: Deduplication, replay and verification metadata need explicit expiry independent of body pruning.
- Verify: test, expire each cache class and inspect its records after the pruning allowance.
- Status: settled

### MPE-STO-036 Authorized tombstone deletion
Where the authorized tombstone feature is enabled, the Store Node shall remove the identified Envelope from managed live storage within P-STO-14 after validating the tombstone.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D6; o4 R1 §D7; o4 R2 §D6
- Rationale: Deletion authority is supplied by OPS; deletion can create a reported retention gap.
- Verify: test, apply a valid OPS-authorized tombstone and inspect storage after its deadline.
- Status: open (DEC-STO-6)

### MPE-STO-037 Reject unauthorized deletion
If an Envelope deletion request fails the configured authorization policy, then the Store Node shall reject that request.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; s3 R1 §D6; o4 R1 §D7
- Rationale: Sender requests and unauthenticated identifiers cannot terminate retention commitments.
- Verify: test, submit forged, malformed and unauthorized deletion requests and confirm retained records remain intact.
- Status: settled

### MPE-STO-038 Prevent tombstone reinsertion
Where the authorized tombstone feature is enabled, the Store Node shall reject reinsertion of a tombstoned Envelope until its latest otherwise-authorized retention deadline has passed.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D6; o4 R1 §D7 tombstones; s3 R1 §D6 replay constraints; reinsertion rule is assumption
- Rationale: Replayed bytes cannot immediately undo an authorized deletion.
- Verify: test, replay deleted Envelopes through live ingress and archive ingestion before the applicable deadline.
- Status: open (DEC-STO-6)

### MPE-STO-039 Separate inclusion and storage evidence
The MPE client library shall expose Anchor inclusion evidence separately from retention commitment evidence.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D6; s2 R1 §D6; s1, s2, s4 R2 §D6
- Rationale: A root opening establishes inclusion in a committed batch, not continuing availability or global completeness.
- Verify: test, supply an Anchor opening without retention receipts and confirm that inclusion does not imply the `stored` label.
- Status: settled

### MPE-STO-040 Verification cache validity
If an Admission Proof verification-cache entry no longer matches the applicable proof bytes, verifier version or Registry context, then the Bus Node shall invalidate that entry.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D6; g3 R1 §D5 and §D9 verification caching; s3 R1 §D6 historical context; cache-binding rule is assumption
- Rationale: A cached result is reusable only within the verification context that produced it.
- Verify: test, independently change proof bytes, verifier version and Registry context and confirm fresh validation is required.
- Status: settled

## Decisions

### DEC-STO-1 Ordinary retention, replication scope and archives

**Options and proponents**

- Short relay storage through expiry: g1; ten-minute relay cache with optional daily stores: g2.
- Forty-eight-hour retention: g3, s1, s3 and s4. g3 R2 specifically recommends per-Shard Store Nodes.
- Seven-day complete-stream replication: s2 and o1.
- Lifetime classes: o2; daily default with a seven-day maximum: o4.
- Indexer-based longer recovery: g4 and o3, under their competing ledger-oriented architectures.
- Optional longer archives: g3, s1, s2, s3 and s4, with different durations.

**Recommended default:** ordinary retention bounded by P-STO-1 on per-Shard Store Nodes; archive service disabled in the Prototype. Bus Nodes without storage duties do not inherit multi-day Envelope retention.

**Reason:** this combines g3’s storage accounting with the widely proposed forty-eight-hour bound. It avoids replicating every Shard on every Bus Node. It remains a proposed compromise, not consensus. A Subscriber offline beyond that window can lose Events.

**Settling check:** measure realistic Subscriber offline intervals, complete-Envelope disk costs and catch-up costs under the merged FMT/PRF profiles. Select seven-day ordinary retention only if the longer recovery benefit has funded storage and usable client recovery. Archive duration is independent of ledger `global_ttl`.

### DEC-STO-2 Complete records versus proof stripping

**Options and proponents**

- Remove Admission Proofs after anchoring: o1 and o2 R1.
- Retain complete independently verifiable records: s2 and s4 R2; s3 R1 requires historical admission validation.
- Introduce a replacement verification representation or explicit trusted-verification model: identified as necessary by s1 R2.

**Recommended default:** preserve complete Envelope verification material and the historical admission context needed for back-fill.

**Reason:** a proof hash cannot reconstruct a discarded proof. An Anchor does not establish admission validity by itself.

**Settling check:** demonstrate independent verification from archived bytes using a fresh client after membership and verifier rotation. Any compact replacement needs a specified verification statement and reviewed trust model before adoption.

### DEC-STO-3 Capacity refusal versus eviction

**Options and proponents**

- Reject new storage admission at the hard cap: g1.
- Evict the oldest unanchored object at the cap: g2.
- Use per-Shard quotas and authenticated expiry: g3 and s3.

**Recommended default:** reject new commitments when capacity is exhausted; preserve existing commitments until deadline or authorized deletion.

**Reason:** anchoring status is not a storage entitlement. Eviction would silently weaken an already issued retention receipt.

**Settling check:** saturate ingest while pruning and compaction run. Verify that committed data remains retrievable within the allocation. An eviction alternative requires explicit revocable service semantics and client-visible revocation.

### DEC-STO-4 Bounded Anchor history

**Options and proponents**

- Fourteen-day, 20,160-slot ring: o2.
- Seven-day, 10,080-window map: o4.
- Root cells with bounded rotation: g3.
- Historic tree with resets: o1; reviews question whether hidden history remains bounded.

**Recommended default:** enforce both P-STO-9 age and P-STO-10 record bounds, using the seven-day proposal. Keep the representation open.

**Reason:** bounding logical slots does not prove bounded reachable history. The Compact documentation describes historical-root checking and history reset, but does not establish measured storage reclamation. Sources: `minokawa-compact/doc/ledger-adt.mdx:613`, `:673`.

**Settling check:** execute insertion, replacement and pruning on the selected ledger-9 generation; measure reachable state bytes and charged writes/deletes. Verify stale-root eligibility separately in CON. A mock can exercise lifecycle rules but cannot settle ledger storage cost or reclamation.

### DEC-STO-5 Storage receipts, funding and availability

**Options and proponents**

- Self-use or voluntary storage: g3 and g2.
- Separately funded storage with three retention receipts: s2, s3 and s4.
- Bonded storage challenges and treasury rewards: o2.
- Operator diversity with canary monitoring: o4.

**Recommended default:** three distinct Operator commitments, receipts issued after persistence, conditional availability and measured retrieval. Fund the service through the ECO/OPS mechanism selected at merge; do not require an on-ledger challenge game in the Prototype.

**Reason:** commitments attribute obligations. Challenges can penalize failure but cannot recover absent bytes or prove continuous storage. Operator independence remains an operational assumption.

**Settling check:** test receipt issuance during crashes, retrieval under correlated failures, measured operating cost and independent Operator participation. A challenge mechanism additionally needs reviewed soundness, challenge-time borrowing analysis and payment feasibility.

### DEC-STO-6 Authorized deletion versus expiry-only storage

**Options and proponents**

- Prune by authenticated expiry rather than sender request: s3.
- Signed delete-by-identifier tombstones under a legal-desk policy: o4 R1 and R2.
- Reject protocol-level discretionary bans: o4’s broader governance position.

**Recommended default:** expiry-only storage in the Prototype. Keep authorized tombstones as an explicit production option, with authorization defined by OPS and reinsertion suppression bounded by remaining retention eligibility.

**Reason:** deletion changes the availability promise and introduces a censorship authority. The policy cannot be inferred from an identifier or a Publisher’s request.

**Settling check:** agree on authorization, receipt exceptions, appeal handling and audit evidence; demonstrate invalid-request rejection, valid deletion and replay resistance. Compliance checks establish local behavior, not erasure from adversarial copies.

### DEC-STO-7 Restart replay state

**Options and proponents**

- Relay-memory nullifier caches with an accepted restart replay window: g3 R1 describes the residual risk.
- Persist or reconstruct protection before live admission: g3’s stated alternative; s2 R2 objects to unspecified persisted-cache semantics.
- Prune only after old authorizations become permanently ineligible: s3 R1.

**Recommended default:** recover protection state before accepting live publications, or wait until affected authorizations expire.

**Reason:** deleting local state does not consume the underlying authorization.

**Settling check:** inject crashes and restore stale backups at admission epoch boundaries. No still-valid consumed authorization may be accepted again after recovery.

## Cross-area dependencies

The following are **expected requirement IDs**, proposed for merge coordination. Their allocation is not established by this STO file.

| Expected ID | Needed contract with STO |
|---|---|
| MPE-FMT-001 | Canonical Envelope identifier and complete serialized verification material. |
| MPE-FMT-002 | Authenticated creation time and retention deadline; ordinary lifetime aligned with P-STO-1. |
| MPE-CRY-001 | Historical proof verification, verifier versioning and required retained context. |
| MPE-CRY-002 | Key-retention coverage and explicit recovery limits; optional ratchets cannot silently change launch claims. |
| MPE-PRV-001 | Recognition-independent retrieval and disclosure of Shard, interval and access-time leakage. |
| MPE-PUB-001 | Complete-range pagination, cursor boundaries and duplicate delivery semantics. |
| MPE-CON-001 | Consumer recovery capabilities, `stored`, `RETENTION_GAP` and `KEY_GAP` API behavior. |
| MPE-CON-002 | Application execution expiry and replay-state pruning; archives cannot renew execution eligibility. |
| MPE-ECO-001 | Admission replay identifier, last admissible time and clock tolerance. |
| MPE-ECO-002 | Explicit funding for retention and retrieval; storage receipts do not imply a funded enforcement mechanism. |
| MPE-OPS-001 | Operator identity and ownership diversity, including receipt signing-key mapping. |
| MPE-OPS-002 | Any tombstone authority, policy, audit path and retention-agreement exceptions. |
| MPE-NET-001 | GossipSub cache configuration distinct from application storage and replay caches. |
| MPE-NET-002 | Anchor schedule, maintenance transaction path and generation-qualified Ledger Adapter behavior. |
| MPE-PRF-001 | Complete-Envelope workload profiles and per-node-class resource budgets. |
| MPE-PRF-002 | Back-fill throughput, timeout and separate retrieval/live-ingress budgets. |
| MPE-SEC-001 | Bounded unvalidated queues, malformed-record handling and recovery from corrupted local state. |
| MPE-VER-001 | Accelerated retention tests, restart injection, correlated failures and storage measurements. |

## Glossary additions

| Term | Meaning |
|---|---|
| Retention deadline | Authenticated time at which an ordinary Envelope’s storage commitment ends; distinct from an application’s execution deadline. |
| Retention commitment | An Operator’s obligation to retain a specified Envelope in a specified Shard through a stated deadline, subject to declared authorized-deletion exceptions. |
| Retention receipt | Signed evidence identifying the Envelope, Shard, deadline and committing Operator. It attributes an obligation rather than proving continued availability. |
| Complete Envelope verification material | Original Envelope bytes and referenced proof material sufficient for the selected independent verification procedure. |
| Historical admission context | Registry snapshot, authenticated root or other generation-qualified context needed to verify admission at publication time. |
| Managed live storage | Store Node records currently retained for ordinary back-fill, including their live indexes; excludes physical remnants and separately agreed archives. |
| Archive service | Optional Store Node service with a separately funded, bounded retention agreement. |
| Application deduplication cache | Bus Node Envelope identifier state whose lifetime is independent of GossipSub’s duplicate cache. |
| Admission replay identifier | Admission-scheme identifier whose reuse would spend an already consumed publication allowance. |
| Recovery checkpoint | Atomically persisted cursor and corresponding logical deduplication state. |
| Tombstone | OPS-authorized deletion record naming an Envelope identifier. |
| `stored` | Client label supported by compatible retention receipts from the required number of distinct Operators. |
| `STORAGE_FULL` | Refusal to undertake a storage commitment because the Shard allocation would be exceeded. |
| `RESOURCE_EXHAUSTED` | Refusal of live admission because required application cache state would exceed its allocation. |
| `RETENTION_GAP` | Identified interval with known unavailable retained history. |
| `CORRUPT_RECORD` | Stored bytes that fail the required identifier or verification checks. |
| `KEY_GAP` | Recovery range for which required client decryption state is unavailable. |

## Gaps

- **Consensus is unestablished.** The inputs contain proposals and cross-review votes, not a completed Round 3 decision. Recommended defaults remain open where those inputs disagree.
- **The supplied s3 Round 2 path is absent.** Its Round 1 proposal supplies the red-team storage position.
- **Actual storage amplification is unknown.** Proposal database multipliers, identifier sizes and provisioning figures are assumptions for different layouts. MPE-STO-034 measures the merged design.
- **Historical Registry-context encoding is unspecified.** MPE-STO-016 defines the required result; FMT, CRY and NET must select a verifiable representation.
- **Indexer contract-event retention is unknown.** `midnight-indexer/chain-indexer/config.yaml:14` describes loadable ledger states. It supplies no contract-event row retention promise.
- **Ledger-9 deployment activation is unknown.** Local source verification is not deployment evidence. Registry and Indexer demonstrations need a revision-qualified devnet or mock, with actual ledger storage measurements before production reliance.
- **State rent was not found, rather than proved impossible.** The read-out §7.5 reports that finding. No requirement assumes automatic rent, expiry or deletion of custom Registry state. The checked ledger update at `midnight-ledger@6abe9b16/ledger/src/semantics.rs:1715` updates replay protection, not arbitrary bus retention.
- **Permanent reconstructability is unsupported.** Indexer re-execution is supported by `midnight-indexer/docs/architecture.md:15`; indefinite recovery additionally requires historical blocks and compatible execution software.
- **Ledger log churn is not deletion.** The pinned VM charges logs as written and deleted bytes at `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:595`. That accounting does not erase block history or independently retained copies.
- **Global completeness cannot be derived from an Anchor.** Range completeness is tested against a Store Node inventory; canary completeness is sampled service evidence. Neither establishes receipt of every publication.
- **Universal deletion and unconditional availability are unsupported.** Expiry, receipts, bonds and replica counts cannot force adversarial erasure or delivery across partitions longer than retention.
- **Storage challenge enforcement is unfinished.** o2’s challenge game lacks a demonstrated storage soundness and economic result in these inputs. It remains an ECO/OPS option.
- **Legal effects are unknown.** No liability or jurisdictional protection is inferred from short ciphertext retention. OPS owns the policy decision; STO supplies testable local deletion behavior.
- **Client plaintext eviction order remains unspecified.** g3 suggests oldest-first eviction. The cache bound is testable now; application-specific archival and eviction preferences require the CON API contract.