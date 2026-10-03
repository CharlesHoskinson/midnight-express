#!/usr/bin/env bash
# Run the simulator test of registry.compact and fallback.compact.
#
# Needs: the compact CLI with toolchain 0.35.0 installed, Node.js 24, and a
# node_modules directory that contains @midnight-ntwrk/compact-runtime 0.20.0
# (the runtime version that toolchain 0.35.0 generates code for). Point
# RUNTIME_MODULES at it, or let the script use the default below.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
src="$(cd "$here/.." && pwd)"
work="${WORK:-/tmp/claude-1000/regtest}"
modules="${RUNTIME_MODULES:-/home/charl/research/moriarty-signed-intent-2026-10-01/compiler-probe/runtime/node_modules}"

mkdir -p "$work"
ln -sfn "$modules" "$work/node_modules"
compact compile +0.35.0 --skip-zk "$src/registry.compact" "$work/reg"
compact compile +0.35.0 --skip-zk "$src/fallback.compact" "$work/fb"
compact compile +0.35.0 --skip-zk "$src/consume.compact" "$work/co"
cp "$here/registry.test.mjs" "$work/"
cd "$work"
REG="$work/reg/contract/index.js" FB="$work/fb/contract/index.js" CO="$work/co/contract/index.js" node registry.test.mjs
