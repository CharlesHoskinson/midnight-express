## Scope of this area

PRF defines D5 capacity limits, latency targets, node resource budgets and Prototype measurement workloads.
Rates count Envelopes; logical Event throughput depends on fragmentation and recipient fan-out.
The recommended default is 10 Envelopes/s plus 64 KiB/s per Shard, whichever binds first; g1’s 50/s proposal remains a required comparison.
All proposed performance numbers are targets or arithmetic on assumptions, not measured MPE capabilities.
Admission, client recognition, retrieval and chain latency are measured separately from relay propagation.
Overlay configuration, admission correctness, retention and privacy guarantees remain dependencies on the other areas.

## Parameters table

Units: KiB = 1,024 bytes; Mbit/s = 1,000,000 bits/s; GB = 1,000,000,000 bytes. CPU consumption is CPU-seconds per elapsed second, expressed in cores. Bandwidth budgets below include transport and control traffic. “Aggregate” means receive plus transmit.

Proposal references identify files under `design/rounds/r1/` or `design/rounds/r2/`, using the role IDs in the brief. Repository citations are relative to `/home/charl/libp2p/` or `/home/charl/midnight/`.

Allowed ranges define benchmark choices, not authorization to raise deployed capacity. Changes to recommended operating limits remain subject to the Decisions below.

| Parameter | Meaning and recommended default | Allowed range or alternatives | Source |
|---|---|---|---|
| P-PRF-1 | Sustained capacity: 10 unique Envelopes/s/Shard | Positive rates through 50/s for comparison; higher rates are overload experiments | g3 R1/R2 §D5; g1 R1 §D5; open DEC-PRF-1 |
| P-PRF-2 | Unique Envelope byte ceiling: 64 KiB/s/Shard, including Admission Proofs and padding | Positive ceilings ≤64 KiB/s under the recommended profile | g3 R1/R2 §D5; s2 R2 §D5 |
| P-PRF-3 | Benchmark Shard count: 8 | 1, 8 or 16; privacy implications require PUB/PRV review | g1, g3, o2 R1 §D5; **assumption** about the selected topology |
| P-PRF-4 | Mesh tuple `(D, D_low, D_high, D_out)`: `(6,5,12,2)` | Compare `(8,6,12,4)`; enforce `D_low≤D≤D_high`, `D_out<D_low`, `D_out≤D/2` | g1/g3 versus g2; `rust-libp2p/protocols/gossipsub/src/config.rs:83`; `specs/pubsub/gossipsub/gossipsub-v1.1.md:192`; open DEC-PRF-2 |
| P-PRF-5 | Gossip factor: 0.25 | 0.25 or 0.4 in the comparison suite | g2 R1 §D5; `specs/pubsub/gossipsub/gossipsub-v1.1.md:550` |
| P-PRF-6 | Heartbeat interval: 1 s | 1 s for these comparisons | g2 R1 §D5; `rust-libp2p/protocols/gossipsub/src/config.rs:521` |
| P-PRF-7 | Flood publishing: disabled | Disabled for the default; enabled only in a separately identified comparison | g1/g2 R1 §D5; specification default is enabled at `specs/pubsub/gossipsub/gossipsub-v1.1.md:549` |
| P-PRF-8 | Sidecar connection planning limit: 50 peers | Positive finite limits compatible with the mesh tuple; alternatives reported separately | g3 R1 §D5; independent of consensus-network peer limits |
| P-PRF-9 | Reference conditions: 32 Bus Nodes/Shard; warm admission; 50 Mbit/s links; 100 ms edge latency; established connections; no induced failures | Compare 16, 50, 200 and 1,000 Bus Nodes; impairment profiles reported separately | g3 R1 §D5; g1/g2 R1 §D5; **assumption** combining their fixtures |
| P-PRF-10 | Warm relay propagation p50 limit: 1.5 s | Compare 1 s and 2 s targets | g3 versus g2/g1 R1 §D5; open DEC-PRF-3 |
| P-PRF-11 | Warm relay propagation p99 limit: 3 s | Compare 2 s, 5 s, 10 s, 15 s and 35 s targets | g3, g2, o4, g1, s1/s2, s3 R1 §D5; open DEC-PRF-3 |
| P-PRF-12 | Edge Bus Node bandwidth: ≤4 Mbit/s aggregate for one Shard | Default is an aggregate budget; a directional interpretation requires DEC-PRF-4 resolution | g3 R1 §D5; **assumption** resolving its unspecified direction |
| P-PRF-13 | Full Bus Node bandwidth: ≤16 Mbit/s aggregate | Default budget; revisions require measured amplification | g3 R1 §D5; same directional assumption |
| P-PRF-14 | Edge Bus Node CPU: ≤0.30 core | Compare g1’s 0.20-core target under its own workload | g3/g1 R1 §D5; open DEC-PRF-4 |
| P-PRF-15 | Full Bus Node CPU: ≤2 cores | Default target; hardware-specific revisions require measurements | g3 R1 §D5 |
| P-PRF-16 | Full Bus Node Shard allocation: at most 4 Shards | Compare 1, 2, 4 and 8 | g3, o4, g2 R1 §D5 |
| P-PRF-17 | Edge Bus Node concurrent full-Shard streams: at most 4 | Compare 8; always subject to the node bandwidth budget | g1 versus g2 R1 §D5; open DEC-PRF-5 |
| P-PRF-18 | Gateway topology: 20 gateways, 500 Subscribers each, 10,000 Subscribers total; each gateway has 8 vCPU, 16 GiB RAM and 1 Gbit/s networking | Compare the 1,000-Subscriber topology; baseline Subscribers receive one complete Shard | s3/s4 R1 §D5; **assumption** adapting their full-feed topology to Shards |
| P-PRF-19 | Desktop recognition profile: 100 Envelopes/s, 32 recognition keys, 4 KiB complete Envelopes | Also measure the normal operating rate and the actual selected format | s1 R1 §D5 |
| P-PRF-20 | Desktop recognition CPU: ≤0.5 core under P-PRF-19 | Default target on declared reference hardware | s1 R1 §D5 |
| P-PRF-21 | Mobile recognition CPU: ≤50 ms CPU/s at 10 Envelopes/s with one recognition key | More keys require separate measurements | g3 R1 §D10; one-key fixture is an **assumption** |
| P-PRF-22 | Attack fraction: 20% adversarial peers during cold start | Additional fractions are separate SEC experiments | g2 R1 §D5 |
| P-PRF-23 | Attack delivery floor: 99% | Default target | g2 R1 §D5 |
| P-PRF-24 | Attack propagation p99 ceiling: 6 s | Default target | g2 R1 §D5 |
| P-PRF-25 | Sustained soak duration: 48 h | Longer runs may supplement this test | s1 R1 §D10; g3 R1 §D10 |
| P-PRF-26 | Burst duration: 60 s | Default duration | s4 R1 §D5; o1 R1 §D5 |
| P-PRF-27 | Validation/publication queue capacities | **Unknown** defaults; positive finite Envelope-count and byte bounds must be selected and recorded before a run | s2/s3/s4 R1 §D5; measure capacity before selecting deployment defaults |
| P-PRF-28 | g1 comparison: 50 Envelopes/s on one Shard with 16 Bus Nodes; weights 70/25/5/0.1 for 448/1,216/4,288/16,576-byte Envelopes, normalized to sum to one | Original arithmetic retained alongside corrected arithmetic | g1 R1 §D5; s1/s4 R2 §D5 |
| P-PRF-29 | Burst suite: 100 Envelopes/s on one Shard; 250/s network-wide; 500/s network-wide | Offered overload, not guaranteed admitted throughput | s4, o1, o4 R1 §D5 |
| P-PRF-30 | Aggregate load suite: 2, 20 and 200 Envelopes/s network-wide, uniform over eight Shards; 4 KiB complete-Envelope fixture | Repeat with actual serialized sizes | g3 R1 §D5 |
| P-PRF-31 | Recovery workload: 20 unique Envelopes/s total live-plus-back-fill service | Live/back-fill split recorded for each run | s3 R1 §D5; split is **unknown** |
| P-PRF-32 | Synchronized epoch burst: 300 Publishers | Default stress fixture | s3 R1 §D5 |
| P-PRF-33 | Indexer comparison: 1 Event/s average, 10/s peak, 10,000 Subscribers; 8 vCPU and 100 Mbit/s; fan-out p99 target 2 s after `BlockIndexed` | Use measured transaction and response sizes | o3 R1 §D5; open DEC-PRF-6 |

Comparison fixtures do not define Envelope formats. If the selected FMT/CRY/ECO design cannot encode a fixture at its stated complete size, the result records “format does not fit” and repeats the experiment with actual sizes. Admission bytes must remain present.

## Requirements

### MPE-PRF-001 Complete traffic accounting

The Prototype shall report traffic accounting that distinguishes logical Events, unique Envelopes, recipient copies, fragments, admission traffic, duplicates, overlay control traffic, back-fill traffic and transport overhead.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s2/s3/s4 R1 §D5; s2 R2 §D5.
- Rationale: Event counts alone conceal amplification and admission costs.
- Verify: inspection, reconcile accounting categories with generated traffic and captured bytes.
- Status: settled

### MPE-PRF-002 Reproducible benchmark manifest

The Prototype shall produce a manifest for each performance run specifying software revisions, hardware, Envelope sizes, admission mechanism, topology, mesh settings, workload, connection state, impairments, measurement interval and random seed.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g2/g3 R1 §D5; s4 R1 §D5 and §D10.
- Rationale: Performance results require reproducible conditions.
- Verify: inspection, reproduce a run from its manifest.
- Status: settled

### MPE-PRF-003 Percentiles with delivery denominators

The Prototype shall report p50, p95 and p99 latency distributions with their eligible-delivery counts, completed-delivery counts, losses, timeouts and observation deadlines.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s1/s2/s3/s4 R1 §D5.
- Rationale: Percentiles calculated only from successful deliveries can conceal failure.
- Verify: test, inject omissions and confirm they remain visible alongside the percentile results.
- Status: settled

### MPE-PRF-004 Separate latency stages

The Prototype shall report separate latency distributions for authorization, publication preparation, relay propagation, Subscriber delivery, recognition, back-fill, Anchor submission, transaction inclusion, finality, indexing and contract reaction.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g3/o1/s4 R1 §D5; o1/s2 R2 §D5.
- Rationale: A relay latency target does not establish first-publication or contract latency.
- Verify: inspection, reconcile stage timestamps with end-to-end samples and identify mocked stages.
- Status: settled

### MPE-PRF-005 Measured propagation amplification

The Prototype shall report per-node receive and transmit amplification as measured wire bytes divided by unique accepted Envelope bytes.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g2/g3 R1 §D5; `2024-revuelta-waku-latency` §3.3.
- Rationale: Degree and assumed overhead factors are planning models.
- Verify: analysis, reconcile directional amplification with packet captures and unique-byte counters.
- Status: settled

### MPE-PRF-006 Sustained Shard capacity

While Reference conditions hold, MPE shall sustain a per-Shard throughput equal to the lower of P-PRF-1 and P-PRF-2 divided by the measured mean complete Envelope size.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1/R2 §D5; o2/s2 R2 §D5.
- Rationale: Both count and byte limits constrain capacity.
- Verify: test, sustain the calculated rate using count-bound and byte-bound valid workloads.
- Status: open (DEC-PRF-1)

### MPE-PRF-007 Normal-load delivery

While Reference conditions hold at the sustained Shard capacity, MPE shall deliver every accepted Envelope to every continuously connected eligible honest Subscriber before the run’s declared observation deadline.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D5 and §D10; g1 R1 §D10.
- Rationale: Normal-load latency must accompany an explicit delivery criterion.
- Verify: test, compare accepted identifiers against each eligible Subscriber’s received identifiers.
- Status: open (DEC-PRF-3)

### MPE-PRF-008 Median warm propagation

While Reference conditions hold at the sustained Shard capacity, MPE shall keep warm relay propagation p50 at or below P-PRF-10.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 §D5; o2 R2 §D5; `2024-revuelta-waku-latency` §§3–5.
- Rationale: The median target includes preparation after warm authorization.
- Verify: test, calculate p50 using the warm propagation clock defined below.
- Status: open (DEC-PRF-3)

### MPE-PRF-009 Tail warm propagation

While Reference conditions hold at the sustained Shard capacity, MPE shall keep warm relay propagation p99 at or below P-PRF-11.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 §D5; o2 R2 §D5; `2024-revuelta-waku-latency` §§3–5.
- Rationale: A median target alone does not bound agent delivery tails.
- Verify: test, calculate p99 alongside the delivery denominator.
- Status: open (DEC-PRF-3)

### MPE-PRF-010 Mesh profile comparison

The Prototype shall benchmark GossipSub v1.1 using each P-PRF-4 mesh tuple with P-PRF-5, P-PRF-6, P-PRF-7 and P-PRF-8 explicitly configured.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g2/g3 R1 §D5; `rust-libp2p/protocols/gossipsub/src/config.rs:83`; `2020-vyzovitis-gossipsub` §4.
- Rationale: Degree-six and degree-eight proposals require comparable measurements.
- Verify: simulation, compare delivery, percentiles, amplification and CPU under identical workloads.
- Status: open (DEC-PRF-2)

### MPE-PRF-011 Gossip-factor retry

If the default mesh misses the warm propagation p99 target, then the Prototype shall repeat the failing workload with the alternative P-PRF-5 gossip factor.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D5 and §D10.
- Rationale: The proposed first tuning step is measurable before changing topology.
- Verify: simulation, reproduce the failure and compare the repeated run.
- Status: settled

### MPE-PRF-012 Degree-transient cost

The Prototype shall measure resource consumption during mesh oversubscription and pruning at the configured P-PRF-4 high-water degree.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D5; g2 R2 §D5; `2020-vyzovitis-gossipsub` §4.2.
- Rationale: Target degree is not the maximum forwarding degree.
- Verify: simulation, correlate observed mesh degree with traffic, CPU and queue peaks.
- Status: settled

### MPE-PRF-013 Edge bandwidth budget

While Reference conditions hold at the sustained Shard capacity, the Bus Node operating as an Edge Bus Node shall consume no more than P-PRF-12 aggregate bus bandwidth.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1/R2 §D5; `2024-revuelta-waku-latency` §3.3.
- Rationale: A one-Shard Operator needs a bounded network bill.
- Verify: test, measure receive plus transmit over the declared steady interval.
- Status: open (DEC-PRF-4)

### MPE-PRF-014 Full bandwidth budget

While Reference conditions hold with P-PRF-16 Shards at their sustained capacity, the Bus Node operating as a Full Bus Node shall consume no more than P-PRF-13 aggregate bus bandwidth.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 §D5.
- Rationale: Additional Shards consume the same node’s finite bandwidth.
- Verify: test, measure aggregate traffic with all allocated Shards active.
- Status: open (DEC-PRF-4)

### MPE-PRF-015 Edge CPU budget

While Reference conditions hold at the sustained Shard capacity, the Bus Node operating as an Edge Bus Node shall consume no more than P-PRF-14 cores for bus processing.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 §D5; s2 R2 §D5; `2024-revuelta-waku-latency` Table 1.
- Rationale: The budget covers actual admission, parsing, deduplication and forwarding.
- Verify: test, measure process CPU on declared reference hardware.
- Status: open (DEC-PRF-4)

### MPE-PRF-016 Full CPU budget

While Reference conditions hold with P-PRF-16 Shards at their sustained capacity, the Bus Node operating as a Full Bus Node shall consume no more than P-PRF-15 cores for bus processing.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D5; g3 R1 §D5.
- Rationale: Multi-Shard admission and forwarding require a separate CPU budget.
- Verify: test, measure process CPU with all allocated Shards active.
- Status: open (DEC-PRF-4)

### MPE-PRF-017 Admission validation benchmark

The Prototype shall report wall-clock Admission Proof validation costs for valid, invalid, duplicate, cached and uncached inputs on each tested Bus Node hardware class.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g3/s3 R1 §D5; s2 R2 §D5; `midnight-node/res/mainnet/ledger-parameters-config.json:124`.
- Rationale: Ledger pricing weights and nwaku timings do not establish sidecar validation costs.
- Verify: test, report distributions, CPU consumption and cache-hit rates for the selected admission implementation.
- Status: settled

### MPE-PRF-018 Publication preparation benchmark

The Prototype shall report publication preparation costs on server, laptop and mobile hardware for the selected Admission Proof mechanism.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g3/o2/o4 R1 §D5; `2024-revuelta-waku-latency` Table 1.
- Rationale: Batching or precomputation cannot substitute for measured preparation costs.
- Verify: test, measure generation latency, CPU and serialized bytes, marking unavailable implementations unknown.
- Status: settled

### MPE-PRF-019 Desktop recognition budget

While the desktop recognition profile P-PRF-19 is active, the MPE client library shall consume no more than P-PRF-20 cores for recognition.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; s1 R1 §D5; s2 R2 §D5.
- Rationale: Recognition scales with both Envelope rate and key count.
- Verify: test, measure matching and nonmatching traffic with the declared recognition keys.
- Status: open (DEC-PRF-4)

### MPE-PRF-020 Mobile recognition boundary

Where whole-Shard recognition on mobile hardware is present, the MPE client library shall satisfy the P-PRF-21 recognition CPU budget.

- Pattern: optional
- Scope: POC
- Priority: SHOULD
- Source: D5; g3 R1 §D5 and §D10.
- Rationale: Mobile support requires a measured boundary.
- Verify: test, measure recognition CPU on a named device using the declared one-key fixture.
- Status: open (DEC-PRF-4)

### MPE-PRF-021 Subscriber download cost

The Prototype shall report measured Subscriber download bytes per delivered Envelope and the resulting daily volume for every supported subscription profile.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g3/s4 R1 §D5; o3/o4/s1 R2 §D5.
- Rationale: Low relay bandwidth does not imply low Subscriber download volume.
- Verify: analysis, reconcile captures with daily extrapolations and disclose the extrapolation workload.
- Status: settled

### MPE-PRF-022 Edge stream concurrency

The Bus Node operating as an Edge Bus Node shall limit active full-Shard streams to P-PRF-17.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g2 R1 §D5.
- Rationale: Direct streams add unicast egress outside mesh propagation.
- Verify: test, request one stream beyond the limit and confirm refusal.
- Status: open (DEC-PRF-5)

### MPE-PRF-023 Gateway Subscriber capacity

While Reference conditions hold on one Shard at its sustained capacity, MPE shall deliver its complete Envelope stream to the concurrently connected Subscribers in P-PRF-18.

- Pattern: state
- Scope: POC
- Priority: SHOULD
- Source: D5; s3/s4 R1 §D5; o4 R1 §D5; s2 R2 §D5.
- Rationale: Gateway concurrency is a separate capacity target from mesh membership.
- Verify: demonstration, exercise the gateway topology and reconcile delivery per Subscriber.
- Status: open (DEC-PRF-5)

### MPE-PRF-024 Gateway resource curve

The Prototype shall report gateway CPU, memory, egress and delivery latency as Subscriber concurrency rises through the P-PRF-18 topology.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s3/s4/o4 R1 §D5.
- Rationale: A socket count alone does not establish usable fan-out capacity.
- Verify: test, identify the first saturated resource and associated delivery degradation.
- Status: settled

### MPE-PRF-025 Fifty-per-second comparison

The Prototype shall execute P-PRF-28 as a separately reported comparison workload.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1 R1 §D5 and §D10; s1/s4 R2 §D5.
- Rationale: The 50/s proposal must remain visible beside the 10/s default.
- Verify: test, compare measured bandwidth, CPU and latency with g1’s corrected estimates and stated gates.
- Status: settled

### MPE-PRF-026 Aggregate load ladder

The Prototype shall execute every P-PRF-30 aggregate load on the P-PRF-3 Shard topology.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g3 R1 §D5.
- Rationale: Low demand, operating demand and network overload expose different constraints.
- Verify: simulation, report offered rate, accepted rate and delivered rate per Shard.
- Status: settled

### MPE-PRF-027 Burst workloads

The Prototype shall execute every P-PRF-29 burst for P-PRF-26.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s4/o1/o4 R1 §D5.
- Rationale: A sustained capacity limit does not establish burst handling.
- Verify: test, report rejection, queue peaks, delivery tails and post-burst drain behavior.
- Status: settled

### MPE-PRF-028 Shard concentration

The Prototype shall repeat each aggregate load with all offered publications concentrated on one Shard.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g3 R1 §D5; s2 R2 §D5; concentration fixture is an **assumption**.
- Rationale: Uniform assignment can conceal a hot Shard.
- Verify: simulation, compare the concentrated run against its uniform counterpart.
- Status: settled

### MPE-PRF-029 Recovery contention

While live delivery shares resources with Store Node back-fill, the Prototype shall measure performance under P-PRF-31.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; s3 R1 §D5; s4 R2 §D10.
- Rationale: Recovery traffic must enter the same resource accounting as live traffic.
- Verify: test, record the live/back-fill split and its effects on live delivery.
- Status: settled

### MPE-PRF-030 Epoch synchronization burst

The Prototype shall measure performance when P-PRF-32 Publishers submit valid publications at the same admission epoch boundary.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s3 R1 §D5.
- Rationale: Epoch synchronization can overload verification despite acceptable averages.
- Verify: test, compare queue growth and latency against an evenly distributed publication schedule.
- Status: settled

### MPE-PRF-031 Invalid-ingress resource cost

The Prototype shall report invalid-ingress resource consumption separately from accepted-Envelope resource consumption during the SEC-defined abuse workloads.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s3 R1 §D5; g2 R1 §D9; s4 R2 §D10.
- Rationale: Valid-message throughput does not establish resistance to verification exhaustion.
- Verify: test, attribute CPU, ingress bytes and queue occupancy to invalid input categories.
- Status: settled

### MPE-PRF-032 Attack delivery floor

While the P-PRF-22 cold-start attack is active at the nominal offered load, MPE shall deliver at least P-PRF-23 of eligible honest Envelope deliveries.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D5; o2 R2 §D5.
- Rationale: Attack latency requires a delivery denominator.
- Verify: simulation, measure delivery among continuously connected honest recipients at each tested network size.
- Status: open (DEC-PRF-3)

### MPE-PRF-033 Attack propagation tail

While the P-PRF-22 cold-start attack is active at the nominal offered load, MPE shall keep completed honest relay propagation p99 at or below P-PRF-24.

- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D5; o2 R2 §D5.
- Rationale: Attack-induced delays have a separate acceptance boundary.
- Verify: simulation, calculate p99 with the losses reported under MPE-PRF-032.
- Status: open (DEC-PRF-3)

### MPE-PRF-034 Queue overflow response

If admitting another publication would exceed a P-PRF-27 queue bound, then the Bus Node shall refuse that publication.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D5; s2/s3/s4 R1 §D5.
- Rationale: Overload must remain bounded.
- Verify: test, fill each declared count or byte bound and confirm additional work is refused.
- Status: open (DEC-PRF-4)

### MPE-PRF-035 Explicit capacity failure

When a Publisher publication is refused because of capacity exhaustion, the Bus Node shall return an explicit capacity-exhausted result to the Publisher.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D5; s2/s4 R1 §D5.
- Rationale: Local capacity refusal must be distinguishable from accepted publication.
- Verify: test, exhaust capacity and inspect the Publisher-facing result.
- Status: settled

### MPE-PRF-036 Stream bandwidth refusal

If serving another full-Shard stream would exceed its class bandwidth budget, then the Bus Node shall refuse the additional stream.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D5; g1/g2 R1 §D5.
- Rationale: A concurrency ceiling does not reserve bandwidth for every possible stream.
- Verify: test, exhaust the measured stream budget before the socket limit.
- Status: open (DEC-PRF-5)

### MPE-PRF-037 Sustained soak

The Prototype shall run the recommended operating workload continuously for P-PRF-25.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; s1 R1 §D10; g3 R1 §D10.
- Rationale: Short runs can conceal accumulating queues, caches and memory consumption.
- Verify: test, inspect resource time series and delivery outcomes throughout the soak.
- Status: settled

### MPE-PRF-038 Performance stop classification

If delivery falls below P-PRF-23 or relay propagation p99 exceeds P-PRF-24 with 200 Bus Nodes, then the Prototype shall classify that configuration as failing the overlay performance gate.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D5; g2 R1 §D10; g2 R2 §D5.
- Rationale: A failed gate must remain visible to VER and OPS.
- Verify: test, feed each failing result into the acceptance report and confirm failure classification.
- Status: open (DEC-PRF-3)

### MPE-PRF-039 Indexer fan-out comparison

Where an Indexer fallback is present, the Prototype shall benchmark the P-PRF-33 workload.

- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D5; o3 R1 §D5; `midnight-indexer/indexer-api/src/infra/api/v4/subscription/contract_event.rs:125`; `midnight-indexer/indexer-api/config.yaml:30`.
- Rationale: Existing per-subscription queries make fallback fan-out an independent unknown.
- Verify: test, measure query rate, CPU, response bytes and fan-out latency after indexing.
- Status: open (DEC-PRF-6)

### MPE-PRF-040 Measured ledger capacity comparison

The Prototype shall report the byte-only ledger throughput ceiling using measured serialized transaction sizes and the applicable ledger and runtime byte limits.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D5; g1/g2/g3/s4 R1 §D5; `midnight-node/runtime/src/lib.rs:300`; `midnight-node/res/mainnet/ledger-parameters-config.json:158`.
- Rationale: Byte ceilings cannot establish throughput after computation and competing traffic.
- Verify: analysis, show both limit calculations and identify the binding applicable limit.
- Status: settled

## Decisions

### DEC-PRF-1 — Operating rate and counting unit

| Proposal | Proposed workload and principal limits |
|---|---|
| g1 | 50 objects/s/Shard; 100/s burst; approximately 848.6 bytes/object; approximately 2.21 Mbit/s aggregate mesh traffic; 16-relay test |
| g2 | Worked load of 10 small messages/s/Shard across eight Shards; approximately 104/s aggregate relay egress ceiling before header/control/client corrections |
| g3 | 10 Events/s plus 64 KiB/s/Shard; eight Shards; aggregate workloads 2/20/200 Events/s |
| g4 | `min(4, floor(5% × blockUsage / measured transaction size))` Events/block; about 0.67/s at four Events per six-second block |
| s1 | 10 cells/s planning load; 100/s sustained capacity experiment; 1,000 whole-feed Consumers |
| s2 | 10 cells/s normal; 100/s stress; 10,000 Subscribers across 50 gateways |
| s3 | 10 real cells/s launch; 20 unique cells/s recovery; 10,000 Subscribers |
| s4 | 10 records/s baseline; 100/s for 60 s; 10,000 complete-stream Consumers |
| o1 | 50 Envelopes/s network-wide; 250/s for 60 s; approximately 5.2 KiB/Envelope |
| o2 | 100 Events/s network-wide; 1,000/s peak with Shard splitting; ≤10/s/Shard across 16 Shards |
| o3 | Ledger lane: 1 Event/s average, 10/s peak; overlay lane later |
| o4 | 50 Events/s network-wide sustained; 500/s peak; approximately 2,400 bytes/Envelope |

Sources: each role’s R1 §D5 and `r1_positions.json`. Some R2 summaries misattribute proposal positions; this table follows the original proposals.

**Recommended default:** g3’s dual per-Shard ceiling, counting complete Envelopes. Eight Shards imply at most 80 Envelopes/s and 512 KiB/s unique traffic when every Shard is saturated. These are separate ceilings; their simultaneous attainment depends on size.

**Reason:** It bounds each Shard’s cost while preserving g1’s higher count-rate experiment. The proposals’ “10/s” and “50/s” are not comparable without sizes: g1’s corrected 50/s stream is approximately 41.39 KiB/s, below g3’s byte ceiling but above its count ceiling.

**Settling check:** Run both profiles with the chosen format and sound admission implementation. Measure CPU, amplification, Subscriber bytes and attainable throughput. Raise the count limit only if the higher-rate profile satisfies the selected resource and latency gates.

### DEC-PRF-2 — Degree-six versus degree-eight mesh

**Options:** g1/g3 use degree six; g2 uses `(8,6,12,4)`, gossip factor 0.25 and a one-second heartbeat. g2’s R2 recommendation adopts 10/s as launch load.

**Recommended default:** `(6,5,12,2)`, gossip factor 0.25, one-second heartbeat and flood publishing disabled. The local Rust defaults resolve g1’s unknown low/high degrees; the Go defaults also show 6/5/12/2 (`rust-libp2p/protocols/gossipsub/src/config.rs:83`; `go-libp2p-pubsub/gossipsub.go:53`). GossipSub v1.1 does not mandate degree six.

**Reason:** This is consistent with g3’s starting bandwidth model. Flood publishing is an explicit departure from the specification default and carries an eclipse-resilience trade-off (`specs/pubsub/gossipsub/gossipsub-v1.1.md:145`).

**Settling check:** Compare both tuples at identical rates, sizes, churn and attack conditions. NET must verify the selected implementation’s parameter validation: the local Go check uses strict `<D/2`, whereas the specification permits equality (`go-libp2p-pubsub/gossipsub.go:274`; specification `:192`).

### DEC-PRF-3 — Latency boundary and acceptance strictness

**Options:** g2 proposes p50≤1 s/p99≤2 s for small messages at up to 1,000 relays; g3 proposes p50<1.5 s/p99<3 s; o4 proposes 1 s/5 s; g1 proposes 2 s/10 s; s1/s2 propose 2 s/15 s; s3 proposes 5 s/35 s. s4 proposes relay p50≤1 s/p95≤3 s/p99≤10 s nominal and p99≤30 s during bursts.

**Recommended default:** Warm propagation p50≤1.5 s/p99≤3 s, with preparation after warm authorization included. Record relay-receipt, Subscriber-callback and recognition-completion clocks separately. Normal reference runs require complete delivery; attack runs require ≥99% delivery and completed-delivery p99≤6 s.

**Reason:** This retains g3’s agent-facing target and g2’s failure boundary without claiming cold or contract latency. The selected non-strict limits are a **drafting assumption** at the threshold of g3’s strict targets.

**Settling check:** Test 16/32/50/200/1,000-node topologies with actual preparation and validation costs. A failure at 200 nodes invokes MPE-PRF-038. VER/OPS own the resulting release or fallback decision.

### DEC-PRF-4 — Bandwidth, CPU and unresolved queue defaults

**Options:** g3 budgets 4 Mbit/s per one-Shard relay, 16 Mbit/s for four Shards, 0.30 core and two cores respectively. g1 budgets Relay-A at 20 Mbit/s aggregate, with a 12 Mbit/s refusal threshold and 0.20 core at its 50/s mix. g2 budgets 3,000,000 bytes/s egress. o1 proposes 0.30 core sustained from an unmeasured proof-cost estimate.

**Recommended default:** Test g3’s bandwidth numbers as aggregate receive-plus-transmit budgets. Keep its CPU targets as hardware-specific hypotheses. Queue defaults remain **unknown** until measured; every test must nevertheless use finite declared bounds.

**Arithmetic and evidence corrections:**

- g3’s model gives `1.25 × 6 × 65,536 = 491,520 bytes/s`, or 3.93216 Mbit/s. It does not prove actual aggregate traffic stays below 4 Mbit/s.
- g1’s weights sum to 1.001. Normalization gives 847.728 bytes/Envelope, approximately 2.204 Mbit/s mesh traffic and 3.662 GB/day per full Subscriber under its forwarding assumptions.
- g2’s body-only ceiling is `3,000,000 / (7 × 4,096) ≈ 104.6/s`. Including its 211-byte header reduces this to approximately 99.5/s before other traffic.
- nwaku verification measurements are 2.7/4.5/18.7 ms on M1/4-vCPU cloud/Pi hardware; generation is 85.7/276.3/766.8 ms (`2024-revuelta-waku-latency`, Table 1). These are not Midnight-native admission benchmarks.
- The ledger’s signature and proof constants are pricing inputs (`midnight-node/res/mainnet/ledger-parameters-config.json:124`, `:128`).
- At the byte ceiling, a single-copy Subscriber receives 5.662 GB/day before additional overhead.

**Settling check:** Capture both traffic directions and benchmark the complete admission path. If aggregate budgets fail, explicitly revise direction, capacity or node class; do not reinterpret the budget silently.

### DEC-PRF-5 — Subscriber fan-out topology

**Options:** g1 permits four direct streams on Relay-A and sixteen on Relay-B; g2 permits eight full-Shard pulls; s1 tests 1,000 Consumers; s2/s3/s4/o4 describe 10,000-Subscriber configurations with substantially larger gateway resources.

**Recommended default:** Four direct streams on the Edge Bus Node, admitted only from remaining bandwidth. Test 10,000 Subscribers separately across twenty gateways, initially receiving one complete Shard each.

**Reason:** Mesh traffic depends on overlay membership; gateway unicast traffic scales with Subscriber count. Under a 4 KiB complete-Envelope fixture:

- 500 Subscribers at 10/s require 163.84 Mbit/s payload egress per gateway.
- At 100/s, they require 1.6384 Gbit/s before overhead.
- Adding s4’s assumed 30% allowance yields 2.12992 Gbit/s, beyond a 1 Gbit/s gateway.

The one-Shard topology is an **assumption** requiring PUB/PRV agreement. It does not establish capacity for 10,000 Subscribers downloading all eight saturated Shards.

**Settling check:** Measure concurrency curves and repeat with whole-network download. Determine the gateway count, links and Operator funding necessary for the chosen subscription model.

### DEC-PRF-6 — Admission optimization and ledger comparison

**Options:** g3 proposes batches of at most 32 messages or 32 KiB, flushed within 200 ms; g1 uses prepaid tickets; g2 caches membership admission; o2 proposes proof precomputation. g4/o3 favor lower-rate ledger delivery.

**Recommended default:** Benchmark the admission mechanism chosen by ECO/CRY without assigning it borrowed proof timings. Include any batch wait in publication latency. Keep batching and precomputation conditional on sound message and byte-debit binding; s2 R2 §D4 identifies missing binding in g3’s batch and conflicting-body problems in o2’s precomputation.

For the ledger comparison, the checked node configuration uses six-second slots, 1,000,000 ledger block-usage bytes and 75% of a 1 MiB runtime block-length limit for Normal dispatch. At an assumed 8 KiB transaction, these give approximately 20.35/s and 16/s byte-only ceilings respectively, before competing traffic and compute limits (`midnight-node/runtime/src/lib.rs:292`, `:300`, `:312`; parameter JSON `:158`). The node pins ledger 9.1.0.0-rc.5 (`midnight-node/Cargo.toml:480`).

**Reason:** Neither overlay proof estimates nor ledger byte arithmetic establish service capacity.

**Settling check:** Serialize and benchmark the selected admission and fallback transactions. Measure the Indexer fan-out target after indexing. Its current subscription loop queries storage per `BlockIndexed`, with a configured pool of 25 connections and 20 subscriptions per connection (`contract_event.rs:125`; `config.yaml:30`, `:83`).

## Cross-area dependencies

These are expected merge allocations, not assertions that another author has already assigned these numbers.

| Expected requirement IDs | Required dependency |
|---|---|
| MPE-FMT-001, MPE-FMT-002 | Canonical complete Envelope sizes, padding, fragmentation and serialization overhead |
| MPE-CRY-001, MPE-CRY-002 | Recognition mechanism and sound binding for any batch or precomputed admission optimization |
| MPE-ECO-001, MPE-ECO-002 | Admission quotas, byte debit, Registry transaction costs and ledger resource reservation |
| MPE-NET-001, MPE-NET-002 | GossipSub v1.1 negotiation, pinned implementation, validated mesh settings, scoring and discovery |
| MPE-PUB-001, MPE-PUB-002 | Shard assignment, eligible Subscriber definition and acceptance/delivery semantics |
| MPE-PRV-001 | Whether one-Shard subscription and any retrieval optimization preserve the selected interest-hiding claim |
| MPE-CON-001, MPE-CON-002 | Publisher-facing capacity errors, callback timestamps and later contract-reaction flow |
| MPE-SEC-001, MPE-SEC-002 | Malicious-ingress fixtures, queue enforcement, attack topology and overload handling |
| MPE-STO-001, MPE-STO-002 | Retention, cache bounds and reproducible back-fill workload |
| MPE-VER-001, MPE-VER-002 | Statistical reporting, observation deadlines and release-gate aggregation |
| MPE-OPS-001 | Hardware profiles, gateway provisioning, monitoring and response to failed performance gates |

## Glossary additions

| Term | Meaning |
|---|---|
| Complete Envelope size | Serialized Envelope bytes including its Admission Proof, visible fields, seal and padding; transport bytes are accounted separately |
| Unique Envelope bytes | Complete Envelope bytes counted once per accepted identifier |
| Reference conditions | P-PRF-9 conditions at the capacity defined by MPE-PRF-006, using valid admission and a declared supported size mix |
| Warm admission | Authorization and required ledger finality completed before the measured publication request |
| Warm relay propagation | Time from a publication request with warm admission to validated receipt at an eligible remote Bus Node; includes subsequent preparation, batch wait and any configured stem |
| Subscriber delivery | Receipt at the client library’s declared callback boundary; recognition completion is separately timestamped |
| Eligible delivery | One accepted Envelope paired with one continuously connected intended test recipient in the applicable Shard |
| Edge Bus Node | One-Shard Bus Node subject to P-PRF-12, P-PRF-14 and P-PRF-17 |
| Full Bus Node | Bus Node carrying up to P-PRF-16 Shards under P-PRF-13 and P-PRF-15 |
| Gateway | Bus Node class provisioned for Subscriber unicast fan-out under P-PRF-18 |
| Recognition key | One key or capability tested by local Envelope recognition |
| Byte-only ceiling | Arithmetic limit from serialized bytes and applicable byte budgets, excluding other bottlenecks |

## Gaps

- **Attainable capacity is unknown.** No supplied result measures this MPE format, admission mechanism and Subscriber topology together. Requirements above demand those measurements.
- **Production hardware is unknown.** CPU budgets require named processors, virtualization limits and software revisions. vCPU counts alone cannot establish cryptographic throughput.
- **Queue defaults are unknown.** The proposals require bounded queues but do not supply defensible common count and byte capacities. Their measurement and SEC-owned enforcement remain prerequisites.
- **Mobile low-bandwidth service is unresolved.** Whole-Shard download can reach gigabytes per day. o1’s 13–15 MB/day estimate depends on a shortened index, fetch policy and retrieval design; it cannot become a universal mobile requirement.
- **Contract-visible percentile guarantees are unresolved.** Proposals range from 90 s to 180 s, or minutes. Approximately 18 s finality is prose in a Proposed MPS, not a percentile guarantee (`midnight-improvement-proposals/mps/mps-0028-pre-finality-state-visibility.md:5`, `:37`).
- **Imported latency results do not establish sustained MPE capacity.** Revuelta’s simulation publishes a small set of messages and introduces benchmarked CPU delays; it does not reproduce these sustained workloads (`2024-revuelta-waku-latency` §4.1).
- **Farooq’s printed example remains disputed.** g2 flags the 5,520 ms calculation; o1/o2 explain it through sequential transmission of degree-many copies. Queueing and shared-link serialization require measurement; neither interpretation establishes a percentile (`2025-farooq-staggering` §IV).
- **Large-message fetch capacity is unresolved.** g2’s 256 KiB external-body p99≤5 s target depends on a retrieval protocol, storage availability and concurrent demand outside the selected Envelope design.
- **s3’s Round 2 review is unavailable at the supplied path.** Its Round 1 proposal supplies its authoritative performance position.
- **Graph summaries are discovery aids.** `graph-overview.md` and `graph-digest.md` identify relevant GossipSub and RLN evidence, but their extracted relationships do not establish numeric acceptance limits.