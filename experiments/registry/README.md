# Registry, fallback and consumer contracts in Compact

This folder holds the ledger interface of the private event bus written in Compact, and the commands that rebuild and measure it. RESULTS.md records what was measured and what the measurements mean for the requirement set and the MIP.

## Files

| File | Content |
|---|---|
| `registry.compact` | Registry: membership trees per period, revocation on equivocation evidence, relay list, parameters with a time-lock, pause, steward, Anchors with a bounded history and an Anchor tree |
| `fallback.compact` | Ledger-only carrier: one `Misc` part per call, or one whole class-0, class-1 or class-2 Envelope per call |
| `consume.compact` | Contract consumer: reaction with a private RFC 6962 inclusion proof, a cross-contract historic-root check against the Registry, and a consumption nullifier |
| `probe/probe.compact` | Probe that isolates the cost of byte spreads and of `emit` payloads (compile with `--skip-zk`, measure with `zkir mock-compile`) |
| `table.py` | Prints the compile-results table of RESULTS.md from `out/*.measure.jsonl` |
| `measure.py` | Tabulates ZKIR sizes, key sizes and the circuit model (`k`, rows, proof size) of one compiler output folder |
| `test/registry.test.mjs`, `test/run.sh` | Simulator test of the Registry and the fallback (no proofs) |
| `test/registry.test.log` | Output of the last test run |
| `out/*.log`, `out/*.measure.jsonl` | Compile logs with timings, and the measurement tables |

## Toolchain

The contracts need Compact toolchain 0.35.0 (language 0.27.0, ledger 9, compact-runtime 0.20.0). Toolchain 0.31.1 (ledger 8) does not know `emit`.

```sh
compact update 0.35.0 --no-set-default     # installs 0.35.0 beside 0.31.1
compact compile +0.35.0 --version          # 0.35.0
```

## Compile

Key generation is slow and the keys are large (one k=20 proving key is several hundred MB). Compile outside tmpfs.

```sh
cd prototype/registry
mkdir -p out
for c in registry fallback consume; do
  ( time compact compile +0.35.0 $c.compact out/$c-0.35.0 ) > out/$c-0.35.0.log 2>&1
done
```

For type checking and JavaScript only, add `--skip-zk` (about one second per contract).

The 0.31.1 comparison:

```sh
sed 's/>= 0.25;/>= 0.23;/' registry.compact > /tmp/claude-1000/registry-031.compact
compact compile +0.31.1 --skip-zk /tmp/claude-1000/registry-031.compact /tmp/claude-1000/reg031
# Exception: ... unbound identifier emit
```

## Measure

```sh
ZKIR=~/.compact/versions/0.35.0/x86_64-unknown-linux-musl/zkir
python3 measure.py out/registry-0.35.0 $ZKIR > out/registry-0.35.0.measure.jsonl
python3 measure.py out/fallback-0.35.0 $ZKIR > out/fallback-0.35.0.measure.jsonl
python3 measure.py out/consume-0.35.0  $ZKIR > out/consume-0.35.0.measure.jsonl
```

`zkir mock-compile -v <circuit>.bzkir` prints the circuit model alone in well under a second for small circuits, without generating keys. Its `size` field is the proof size in bytes (`midnight-zk/proofs/src/dev/cost_model.rs:197-198, 300`).

## Test

```sh
RUNTIME_MODULES=/path/to/node_modules test/run.sh
```

`RUNTIME_MODULES` must contain `@midnight-ntwrk/compact-runtime` 0.20.0. The script compiles with `--skip-zk` into `/tmp/claude-1000/regtest`, links the modules there and runs the test with Node.js 24.

## Cleaning up

The proving keys are not needed after measurement. In this folder they were deleted (`rm out/*/keys/*.prover`) after `out/*.measure.jsonl` recorded their sizes; the verifying keys, ZKIR files and generated JavaScript are kept. `measure.py` reports `null` for deleted keys, so measure first. The `publishClass1` and `publishClass2` rows of `out/fallback-0.35.0.measure.jsonl` were completed by hand from separate `zkir compile` and `zkir mock-compile` runs (`out/fallback-keygen.log`, `out/fallback-class2-mock.log`), because the full fallback compile was stopped.
