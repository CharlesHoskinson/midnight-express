# Builder A measured results

Repair round: **9/10 scenarios pass the supplied checker** at 50 nodes, seed 1 and a 60-second publishing window. Release build, fmt, Clippy and 100 workspace tests pass. Coverage: 109/137 qualified Done rows; 28 partial/not-done rows remain unmet. No git commands were used.

## Repair round

| Fix item | Change and evidence |
|---|---|
| 1 | Shard bounds checked before rate-map allocation; anchor leaf insertion bounds checked. Correctly admitted out-of-range publish is refused without an anchorer panic. Red and green regression evidence retained. |
| 2 | Each publication has an independent retry task. Actual schedule elapsed is measured before retry completion. README no longer promises an unconditional five-minute runtime. Churn wall time is reported below. |
| 3 (partial) | Seeded shuffled churn includes indices 0–9 serving ingress/subscribers; every joiner is added to live allow-lists. Feed failover chooses an existing source with history, avoiding a fresh empty restart-barrier source. Registry membership remains a simulation fixture. |
| 4 | Backfill EIDs are collected from /backfill pages only. Late live feed starts at the join head and runs concurrently with historical recovery; live and historical measurements are separate below. |
| 5 | Eviction deadline keeps application score -20 throughout 60-second prune backoff. Real eight-node withholding test verifies mesh removal; policy test verifies 300 useful heartbeats and deadline reset. This policy is tested for one Shard. |
| 6 | Network-scoped GossipSub 1.2 with a small vendored custom-Version API patch; serial IDONTWANT on/off comparison and successful-flush per-class payload counters below. |
| 7 | Reaction carries signed statement, signature, consumption nullifier and optional inclusion proof. No stream/event secret or Sealed Body. Mock uses an off-transaction trusted relation registry; wrong signature/nullifier fail and 100 reactions have one effect. |
| 8 | Per-Shard Accepted rings: 64MiB/50000 rows, expiry pruning and absolute cursors. Validation traces use a capped 200000-entry ring only under explicit simulation diagnostics. Normal library builds omit tag-match EID diagnostics; simulator enables that test feature. Plaintext/received/gap state expires at ten minutes, with separate bounded expiry dedup. |
| 9 (partial) | Queue-full publish returns Busy; completion guard releases every job on semaphore failure, blocking-task failure or abort. Simulated clients now use second-Operator inventory reconciliation every 60 seconds. Gate-close, queue saturation/recovery and completion-abort tests pass. Short observation windows can still miss late omissions before the next reconciliation. |
| 10 | ECO-053 calls production epoch(); STO-012 uses correctly signed duplicate-Operator receipts and an independent deadline mismatch; PUB-031 reads and verifies every returned envelope. Receipt filtering/paging now precedes signing. |
| 11 | Node select arms delegate to named Runtime methods for commands, completion, heartbeat, gossip, RPC and services. |

Items 1, 2, 4–8, 10 and 11 are fixed. Items 3 and 9 are partially fixed: subscriber/ingress churn and allow-list refresh are implemented, but client address discovery for replacement and alternate peers remains incomplete. Churn records 168 first-ingress dial failures, eight subscriber failovers and zero successful reconciliation calls; 904/1108 pairs arrive (81.59%). All three original stores are churned, and replacement stores are empty during their restart barriers. The five-minute timing defect is fixed (200.93 seconds), but churn delivery is not. The 50-minute repair budget leaves no time for another implementation/verification cycle; these failures are retained rather than hidden. Remaining limitations: the mock trusted reaction relation is not a real ZK proof; eviction has no eight-Shard policy test; CBOR vectors still encode as integer arrays; production finalized Registry roster subscription, WAN tests, exhaustive cache/RSS soak and timing/log privacy audits remain absent. These need protocol/backend work or longer experiments and remain qualified in COVERAGE.md. The network-wide allowance counterexample remains unfixed because independent admission validators do not serialize a shared allowance.

The initial repair baseline suffered scanner-induced load (69.5% delivery). A cached Aho–Corasick matcher replaced per-canary frame scans, and instrumentation now uses atomic counters without extra router events. Final baseline delivered 100%. An initial malformed run overlapped replay and verification commands and delivered 91.13%; its raw record is retained as `evidence/repair/malformed-overlap.json`. The rerun overlaps leakage after verification finishes; its result below is reported without excluding missing pairs.

## Scenario measurements

Delivery counts are eligible subscriber-event pairs, including scheduled publications that failed ingress. PASS describes only the supplied checker gates. p99 excludes missing pairs; missing counts remain visible in delivery ratios. All fresh runs use the normal synthetic proof-cost setting (4500 microseconds), real localhost TCP/Noise/Yamux and no WAN model. Baseline on/off ran serially; malformed/replay and churn/anchor overlapped to fit the budget. The final malformed rerun overlaps leakage; other measurements are serial. CPU and wall times for overlapping runs are subject to host contention.

| Scenario | Published | Delivered pairs | Min subscriber | p99 ms | Wall s | Checker |
|---|---:|---:|---:|---:|---:|---|
| baseline | 554 | 1108/1108 (100.0000%) | 100.0000% | 2463.6 | 85.51 | PASS |
| spam | 554 | 1108/1108 (100.0000%) | 100.0000% | 4146.9 | 86.78 | PASS |
| malformed | 547 | 1094/1094 (100.0000%) | 100.0000% | 2856.1 | 85.75 | PASS |
| replay | 246 | 1033/1108 (93.2310%) | 89.0909% | 23825.6 | 125.61 | PASS |
| eclipse | 554 | 1108/1108 (100.0000%) | 100.0000% | 2536.6 | 85.58 | PASS |
| churn | 554 | 904/1108 (81.5884%) | 45.3704% | 26592.7 | 200.93 | FAIL |
| backfill | 549 | 1208/1208 (100.0000%) | 100.0000% | 52242.6 | 103.83 | PASS |
| anchor | 554 | 1108/1108 (100.0000%) | 100.0000% | 2480.9 | 161.43 | PASS |
| leakage | 554 | 1108/1108 (100.0000%) | 100.0000% | 3860.4 | 86.61 | PASS |
| fallback | 319 | 957/957 (100.0000%) | 100.0000% | 31079.4 | 110.27 | PASS |

Replay published counts attack injections; its delivery denominator counts honest subscriber-event pairs. All final runs report 0 panics and 0 duplicates.

## Backfill and churn

Backfill-page recovery: **261/261** pre-join EIDs. Late live delivery: **63/63 (100.0000%)**. Overall backfill-scenario delivery is in the table. The old 0.427 minimum was the late subscriber: historical pagination blocked its feed, then the feed restarted from zero. Current live reading runs alongside pagination from the join head, and feed reads cannot raise the recovery count.

churn:
- publish_window=60s; actual_publish_elapsed=60.005s; drain=125s; churn replacements=25
- Subscriber source failovers=8; reconciliation calls=0; repaired observations=0

backfill:
- publish_window=60s; actual_publish_elapsed=60.000s; drain=30s; churn replacements=0
- Subscriber source failovers=2; reconciliation calls=10; repaired observations=272
- Late subscriber store failovers=1; backfill-only recovery=261/261

## IDONTWANT measurement

Paired serial baseline runs, 50 nodes, seed 1, 60 seconds, identical 554-envelope schedule. Per-class values are medians per node of envelope payload bytes successfully flushed by GossipSub handlers. They exclude protobuf, control, Noise and client RPC overhead; transport totals include those costs.

| IDONTWANT | Node ingress median B | Node egress median B | Class 0 B | Class 1 B | Class 2 B | Class 3 B |
|---|---:|---:|---:|---:|---:|---:|
| on | 2945320 | 2799282 | 1174088 | 222336 | 281576 | 490216 |
| off | 6222918 | 5720113 | 1203576 | 861552 | 1130920 | 2062288 |

## Verification and artifacts

```sh
python3 scripts/verify_repair.py
python3 scripts/run_repair.py
python3 /home/charl/privateEvents/design/prototype/check_sim.py results/repair
python3 scripts/write_repair_results.py
```

Tests: 100 passed, zero failed. Exit codes: build=0, fmt=0, clippy=0, tests=0.

The exact commands, exit codes and wall times are in `evidence/repair/hygiene.json`, `evidence/repair/runs.json` and `evidence/repair/malformed-rerun.json`. Compiler/test output and scenario logs are alongside them. Complete metrics: `results/repair/*.50.json`; off control: `results/repair-idontwant/baseline.50.json`. Checker output: `evidence/repair/check.txt`. Previous seed-42/short-window RESULTS.md is archived under `evidence/repair/RESULTS-before-repair.md`; its benchmarks and 200-node runs were not repeated this round.

```text
[PASS] baseline (baseline.50.json): 7/7 checks
[PASS] spam (spam.50.json): 2/2 checks
[PASS] malformed (malformed.50.json): 2/2 checks
[PASS] replay (replay.50.json): 2/2 checks
[PASS] eclipse (eclipse.50.json): 2/2 checks
[FAIL] churn (churn.50.json): 1/2 checks
        - delivery_ratio: got 0.8158844765342961, want >= 0.99
[PASS] backfill (backfill.50.json): 1/1 checks
[PASS] anchor (anchor.50.json): 2/2 checks
[PASS] leakage (leakage.50.json): 2/2 checks
[PASS] fallback (fallback.50.json): 2/2 checks

9/10 scenarios pass
```

