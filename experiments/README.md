# Experiments

Exploratory code written to understand the Midnight Express design better. It is not the proof of concept, it is not maintained, and nothing in the design document relies on it.

The experiments guided the design in two ways. They exposed questions that arithmetic and reading specifications did not settle, and they shaped what the proof of concept should be. The proof of concept is the next step: one reference implementation with a deterministic simulator, specified in Part III of the design document.

## Contents

| Path | What it is |
|---|---|
| `mpe-core`, `mpe-client`, `mpe-node`, `mpe-sim`, `vendor` | A Rust workspace on rust-libp2p 0.57 and `libp2p-gossipsub` 0.50: sealed fixed-size envelopes, a stand-in admission proof (Bus Nodes can read every admission secret), in-memory stores, a mock ledger, and a simulator with ten scenarios. |
| `registry` | The ledger interface in Compact (Bus Registry, ledger lane, consumer), the compile results, circuit sizes and derived fee estimates in `registry/RESULTS.md`. Compiled with toolchain 0.35.0; nothing has run on a Midnight network. |
| `RESULTS.md`, `COVERAGE.md`, `LEAKAGE.md` | Notes from the exploratory runs. Single runs on one machine, localhost networking, synthetic costs. Treat the figures as unreplicated observations. |

## Running the Rust workspace

Stable Rust 1.98.1.

```sh
./run_scenarios.sh            # builds, then runs the ten scenarios at 50 nodes, 60 s, seed 1; JSON goes to results/
cargo test --workspace
```

The simulator runs real libp2p swarms in one process. It has no wide-area latency, loss or bandwidth cap.
