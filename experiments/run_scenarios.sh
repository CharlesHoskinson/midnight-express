#!/usr/bin/env bash
# Build the workspace and run the ten simulator scenarios. Usage: ./run_scenarios.sh [nodes] [duration-secs] [out-dir]
set -euo pipefail
cd "$(dirname "$0")"
NODES=${1:-50}; DUR=${2:-60}; OUT=${3:-results}
mkdir -p "$OUT"
cargo build --workspace --release
for s in baseline spam malformed replay eclipse churn backfill anchor leakage fallback; do
  cargo run -q -p mpe-sim --release -- run --scenario "$s" --nodes "$NODES" --seed 1 --duration-secs "$DUR" --out "$OUT/$s.$NODES.json"
  echo "done $s"
done
