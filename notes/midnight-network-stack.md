# Midnight network stack: code-grounded read-out for a private event bus

## 0. Scope, sources and conventions

All paths are relative to `/home/charl/midnight/` unless stated. Line numbers refer to the files as synced on 2026-10-01. Nothing was fetched from the web. The `*.upstream-2026-09-13` snapshot folders were not used.

### 0.1 Source baseline

| Repo | State read | Notes |
|---|---|---|
| `midnight-node` | `887348f9`, 2026-10-01, "upgrade of polkadot-sdk to stable2609 equivalent" | runtime `spec_version: 003_000_000` (`midnight-node/runtime/src/lib.rs:276`); ledger 9 (`midnight-node/Cargo.toml:101-107`) |
| `midnight-ledger` | working tree is branch `ledger-8`, `9f9842eb`, version 8.2.0-rc.1 (`midnight-ledger/Cargo.toml:4`) | The node pins ledger 9.1.0.0-rc.5 (`midnight-node/Cargo.toml:472-477`). Ledger-9 facts below were read from `git archive ledger-9.1.0.0-rc.5` (read-only archive of the tag) and are cited as `L9:<path>:<line>`. Ledger-8 working-tree facts are cited as `L8:<path>:<line>`; the only one used is that the ledger-8 branch has the same `log` op and `MAX_LOG_SIZE` (`L8:onchain-vm/src/vm.rs:38`) but no `MAX_LOG_EMITTED` and no `VersionedLogItem` (its `ContractLog` carries a raw `StateValue`, `L8:ledger/src/events.rs:102-106`). A tag `ledger-10.1.0.0-alpha.1` also exists; it was not examined. |
| `midnight-indexer` | `7842950e`, 2026-10-01, workspace version 4.4.0-rc.5 (`midnight-indexer/Cargo.toml:14`) | |
| `midnight-js` | `8edbd949`, 5.0.0-rc.3 (`midnight-js/package.json:4`) | |
| `midnight-wallet` | `4628d984`, 2026-09-30 | |
| `minokawa-compact` (Compact compiler, std lib, docs) | `3eb9758`, 2026-09-30 | The folder `compact/` holds only a README and a prerelease note; the compiler source is in `minokawa-compact/`. |
| `midnight-dapp-connector-api` | `612db2b`, 2026-09-29 | |
| `midnight-docs`, `midnight-architecture`, `midnight-improvement-proposals` | `eabbedf` (architecture), `078a5a7` (MIPs/MPSs) | |
| `midnight-zk` | `bc0d161`, 2026-10-01 | |
| `rust-yamux` | branch `origin/yamux-v0.12.2`, `8ed778c` | The node patches yamux to this branch (`midnight-node/Cargo.toml:470`). |
| polkadot-sdk (Parity SDK fork) | **Pinned source not on disk.** `midnight-node/Cargo.lock:14461-14463` pins tag `stable2609-rpc-fix-10-oct` at `84fbde24`; that commit is not in `~/.cargo/git/db/polkadot-sdk-dee0edd6eefa0594`. | The only polkadot-sdk source on disk is commit `660acefe` (stable2606, 2026-07-03) in that bare repo. It is cited as `SDK-ref:<path>:<line>` and used only to read upstream defaults and protocol names. Every `SDK-ref` fact is **upstream behaviour at a nearby version, not verified against the pinned fork**. |

Cargo features, defaults and constants that Midnight does not override are therefore marked "upstream default" where used.

### 0.2 Labels

- **[code]** read in a source file. **[doc]** stated in prose/docs/proposals, not enforced by code read here. **Inference** is my deduction from cited code. **not found** means I searched and the item is absent from the local repos.

### 0.3 Generation caveat that affects the whole read-out

The local repos are ahead of the deployment generation that the docs list for mainnet. `midnight-docs/docs/relnotes/support-matrix.json` lists for mainnet: node `node-1.0.300` (line 14), Compact toolchain `toolchain-0.31.1` (line 38), on-chain runtime `onchain-runtime-3.0.0` (line 82), midnight-js `4.1.1` (line 104), indexer `4.3.302` (line 137). The local node/ledger/indexer/Compact code is the ledger-9 generation: ledger v8 to v9 state translation is wired into the runtime migrations (`midnight-node/runtime/src/lib.rs:1239-1249`; `midnight-node/pallets/midnight/src/lib.rs:104-106`). Compact contract events (`emit`) and the indexer `contractEvents` API belong to this ledger-9/Compact-0.33 generation (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:26`; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:1971`). **Inference:** on the generation the docs call current for mainnet, contract events are not yet available; they arrive with the ledger-9 hard fork. Confirm the activation date before relying on them.

---

## 1. Node networking

### 1.1 P2P library, versions, transports

| Item | Finding | Source |
|---|---|---|
| Network backend | `sc_network::NetworkWorker` (the libp2p backend) is hard-wired. A comment shows the litep2p alternative is not selected. | `midnight-node/node/src/command.rs:326-327` |
| libp2p | 0.54.1 (umbrella), libp2p-core 0.42.0, libp2p-kad 0.46.2, libp2p-mdns 0.46.0, libp2p-noise 0.45.0, libp2p-tcp 0.42.0, libp2p-websocket 0.44.0, libp2p-request-response 0.27.0, libp2p-identify 0.45.0, libp2p-swarm 0.45.1 | `midnight-node/Cargo.lock:6685-6686, 6744, 6829, 6858, 6897, 6985, 7021, 6965, 6788, 7073` |
| litep2p | 0.15.3 is in the lockfile as an `sc-network` dependency but unused at runtime | `midnight-node/Cargo.lock:7242-7243`; `command.rs:326` |
| sc-network | 0.34.0, fork `shieldedtech/polkadot-sdk` tag `stable2609-rpc-fix-10-oct` | `midnight-node/Cargo.lock:14461-14463`; `midnight-node/Cargo.toml:269` |
| Transports | TCP, WebSocket, DNS names. Mainnet bootnodes are `/dns4/.../tcp/30333/ws/p2p/...`. | `midnight-docs/docs/concepts/network-architecture/p2p-networking.mdx:36-40`; `midnight-node/res/mainnet/bootnodes-config.json:3-6` |
| QUIC | `libp2p-quic` appears in the lock as a dependency of the umbrella crate (`midnight-node/Cargo.lock:6941`) but the SDK-ref `sc-network` feature list is `dns identify kad macros mdns noise ping request-response tcp tokio websocket yamux` (`SDK-ref:substrate/client/network/Cargo.toml:40`). **Inference:** QUIC is not enabled on the libp2p backend. | `Cargo.lock:6941`; `SDK-ref:substrate/client/network/Cargo.toml:40` |
| Encryption / mux | Noise; Yamux. | `p2p-networking.mdx:42-49` |
| Yamux | Patched to `midnightntwrk/rust-yamux` branch `yamux-v0.12.2` (version 0.12.2). The patch rejects a first stream frame whose body exceeds `DEFAULT_CREDIT` (256 KiB). Defaults in the patched crate: `max_num_streams` 8192, `max_buffer_size` 1 MiB, per-stream receive window 256 KiB. | `midnight-node/Cargo.toml:470`; `midnight-node/Cargo.lock:21334-21336`; `rust-yamux@origin/yamux-v0.12.2:yamux/src/connection.rs:643-650` (commit `8ed778c`); `rust-yamux@origin/yamux-v0.12.2:yamux/src/lib.rs:41,108-111` |
| Peer identity | ed25519 key, separate from consensus keys | `p2p-networking.mdx:61` |

### 1.2 Notification and request-response protocols registered

Registered explicitly by Midnight in `new_full`:

| Protocol | Kind | Registered at | Notes |
|---|---|---|---|
| GRANDPA | notification | `midnight-node/node/src/service.rs:574-586` | name from `sc_consensus_grandpa::protocol_standard_name(genesis, chain_spec)` |
| BEEFY gossip | notification | `service.rs:589-607` | name from `sc_consensus_beefy::gossip_protocol_name(genesis, fork_id)`; SDK-ref names are `/{genesis}/beefy/2` (`SDK-ref:substrate/client/consensus/beefy/src/communication/mod.rs:32,137`) |
| BEEFY justifications | request-response | `service.rs:593-608` | SDK-ref `/{genesis}/beefy/justifications/1` (`.../beefy/src/communication/mod.rs:34,141`) |
| Midnight ledger-sync | request-response, custom | `service.rs:610-644` | name `/{genesis}[/{fork}]/midnight-ledger-sync/2`; chunk max 1 MiB, raw max 1 GiB. Non-validators serve by default; validators serve only with `--serve-warp-ledger-sync` (`service.rs:619`, `cli.rs:58`). Purpose: recover the ledger arena after warp+state sync. |
| Everything else | created inside `sc_service::build_network` | `service.rs:652-665` | warp sync is configured as `WarpSyncConfig::WithProvider(grandpa NetworkProvider)` (`service.rs:646-651, 660`) |

Constants of the custom protocol: `PROTOCOL_NAME_SUFFIX = "midnight-ledger-sync/2"` (`midnight-node/node/src/warp_ledger_sync/protocol.rs:31`), `MAX_LEDGER_SYNC_CHUNK = 1 MiB` (`:36`), `MAX_LEDGER_SYNC_RAW_BYTES = 1 GiB` (`:43`).

Created by `build_network` (names from SDK-ref, upstream defaults): block announces `/{genesis}/block-announces/1` (`SDK-ref:substrate/client/network/sync/src/engine.rs:1102`), block sync `/{genesis}/sync/2` (`.../block_request_handler.rs:104`), state `/{genesis}/state/2` (`.../state_request_handler.rs:85`), warp `/{genesis}/sync/warp` (`.../warp_request_handler.rs:68`), light `/{genesis}/light/2` (`SDK-ref:substrate/client/network/light/src/light_client_requests.rs:37`), transactions `/{genesis}/transactions/1` (`SDK-ref:substrate/client/network/transactions/src/lib.rs:149`). Every Substrate protocol name embeds the genesis hash, so peer sets are chain-scoped. Midnight's own `RunMidnight` CLI adds only `--filter-deploy-txs`, `--rpc-max-finality-subscriptions` (default 512) and `--serve-warp-ledger-sync` on top of `sc_cli::RunCmd` (`midnight-node/node/src/cli.rs:41-58`).

### 1.3 Peer discovery

- **Bootnodes [code/config]:** four DNS bootnodes in the mainnet chain spec (`midnight-node/res/mainnet/chain-spec.json:5-10`; same in `res/mainnet/bootnodes-config.json:3-6`). Additional nodes via `--bootnodes` (`midnight-node/README.md:297`). Preview/preprod bootnodes are listed in `midnight-docs/docs/nodes/boot-node.mdx:37-48,63-73`.
- **Reserved nodes** are used in the local-environment networks (`midnight-node/local-environment/src/networks/well-known/mainnet/mainnet.network.yaml:43-52`).
- **Kademlia random walk and mDNS [doc + lock]:** described in `midnight-docs/docs/concepts/network-architecture/p2p-networking.mdx:22-28`; libp2p-kad 0.46.2 and libp2p-mdns 0.46.0 are in the lock (see 1.1). Upstream mDNS is on unless `--dev` or `--no-mdns` (`SDK-ref:substrate/client/cli/src/params/network_params.rs:114,279`). Midnight's own code and config set neither flag; the only occurrence in the node repo is a sync-test script (`midnight-node/scripts/sync-test/run-sync.sh:161`, `--no-mdns`). Kademlia replication factor upstream default is 20 (`network_params.rs:149`).
- `--no-private-ip` is what the operator docs use (`midnight-docs/docs/nodes/full-node.mdx:123,134`).
- Peer reputation inspection and unban RPCs are custom (`midnight-node/docs/openrpc.json:279`; `midnight-node/node/src/peer_info_rpc.rs`).

### 1.4 How transactions and blocks propagate

Transactions:
- User transactions are Substrate extrinsics that call `Midnight::send_mn_transaction(midnight_tx: Vec<u8>)`, submitted as **bare (unsigned) extrinsics** and validated by `ValidateUnsigned` (`midnight-node/pallets/midnight/src/lib.rs:378, 450-468, 575-598`). Only governance calls may carry signed-extrinsic extensions (`midnight-node/runtime/src/check_call_filter.rs:86-87`). The wallet submits through polkadot.js `midnight.sendMnTransaction` (`midnight-wallet/packages/node-client/src/effect/PolkadotNodeClient.ts:171`).
- Pool: `sc_transaction_pool` wrapped by `FilteringTransactionPool` (`midnight-node/node/src/service.rs:405-417`). With `--filter-deploy-txs` the pool rejects transactions containing `Deploy` or `Maintain` operations (`midnight-node/node/src/filtering_pool.rs:30-44,72-95`, `cli.rs:44`).
- Propagation uses the standard Substrate transactions notification protocol (upstream): each transaction is sent as its own notification (RFC 56), per-peer known-hash LRU of 10,240, at most 8,192 pending validations, flush interval 2,900 ms, max notification size `MAX_RESPONSE_SIZE` = 16 MiB (`SDK-ref:substrate/client/network/transactions/src/config.rs:28,33,36,39`; `.../transactions/src/lib.rs:499-505`; `SDK-ref:substrate/client/network/src/lib.rs:314`). Peers that send transactions lose reputation first (`-16` per tx, `+128` for a good one, `-4096` for a bad one; `transactions/src/lib.rs:77-83`).
- Tag `provides = tx_hash` and `longevity = 600` blocks (about 1 hour at 6 s) so identical transactions deduplicate and stale ones are revalidated (`pallets/midnight/src/lib.rs:590-594`). No `priority` is set there. **Inference:** no fee-based ordering exists in the pool.

Blocks:
- Authoring by Aura (`service.rs:868-899`); blocks announced via `block-announces/1` and fetched via `sync/2`; imports go through GRANDPA/BEEFY block import wrappers and the Partner Chains verifier (`service.rs:419-500`).

### 1.5 Gossipsub / pubsub

- **libp2p gossipsub: not found.** `midnight-node/Cargo.lock` has no `libp2p-gossipsub` or `libp2p-floodsub` package (list of libp2p crates at lines 6720-7094).
- **Substrate gossip engine: present.** `sc-network-gossip` 0.34.0 (`Cargo.lock:14548-14549`) is a dependency of `sc-consensus-grandpa` (`:14273`) and `sc-consensus-beefy` (`:14197`). It provides topic-tagged gossip with a per-protocol validator that decides rebroadcast; topics are single 32-byte tags (`SDK-ref:substrate/client/network-gossip/src/lib.rs:20-27`). It is used only by the consensus gadgets. Midnight registers no gossip protocol of its own.
- No application-level pub/sub is exposed by the node. The nearest services are RPC subscriptions: `chain_subscribeFinalizedHeads`, `author_submitAndWatchExtrinsic`, `state_subscribeStorage`, `grandpa_subscribeJustifications`, `beefy_subscribeJustifications` (`midnight-node/docs/openrpc.json:757, 695, 900, 942, 983`).

### 1.6 Mempool limits

| Limit | Value | Source |
|---|---|---|
| Max pool entries / bytes | upstream defaults `--pool-limit` 8192, `--pool-kbytes` 20480 (20 MiB), pool type `ForkAware`. Midnight does not override. The operator docs show `--pool-limit 35`. | `SDK-ref:substrate/client/cli/src/params/transaction_pool_params.rs:47,51,61`; `midnight-node/node/src/service.rs:410`; `midnight-docs/docs/nodes/full-node.mdx:121` |
| Per-tx byte limit (ledger) | 1,048,576 bytes | `midnight-node/res/mainnet/ledger-parameters-config.json:152`; `L9:ledger/src/structure.rs:1270-1273` |
| Longevity | 600 blocks | `pallets/midnight/src/lib.rs:592` |
| Time-to-dismiss (DoS price for invalid txs) | `max(2,000,000 ps x est_size, 15,000,000,000 ps)` | `ledger-parameters-config.json:153-154`; `L9:ledger/src/structure.rs:2371-2378` |
| Per-account throttle | 100 txs and 10 MiB per window of `HOURS` blocks (600 blocks = 1 hour; the source comment says "1 day" but the constant is `HOURS`). Applies only to signed extrinsics, which are limited to governance calls. | `midnight-node/runtime/src/lib.rs:962-968`; `runtime/src/constants.rs:18-23`; `pallets/throttle/src/check_throttle.rs:72-115`; `midnight-docs/docs/nodes/index.mdx:111` |
| Transaction pre-checks | weight check before ledger validation; early reject if it cannot fit the block | `pallets/midnight/src/lib.rs:470-490, 542-571` |

Not found: a per-sender rate limit for ordinary Midnight transactions (they have no signer at the Substrate layer).

### 1.7 Consensus components and message rates

| Component | Status | Parameters | Source |
|---|---|---|---|
| Aura (block production) | active | slot = 6,000 ms; one block author per slot, round-robin on the committee; proposal budget 2/3 of the slot | `runtime/src/lib.rs:292`; `service.rs:868-899` (`block_proposal_slot_portion`, `:894`) |
| BABE | code present, **not active**. `pallet-consensus-engine` drives AURA -> BABE: "arm", "schedule flip", flip at an epoch boundary; from arming every block must carry a BABE `SecondaryPlain` digest. MIP-0010 is Proposed. | `c = 1/4` genesis epoch config | `midnight-node/pallets/consensus-engine/src/lib.rs:14-52`; `runtime/src/lib.rs:294-298` (the `BABE_GENESIS_EPOCH_CONFIG` constant); `service.rs:849-856`; `midnight-improvement-proposals/mips/mip-0010-aura-to-babe-migration.md:6,34` |
| GRANDPA (finality) | active, every full node runs the voter (observer disabled) | `gossip_duration` 333 ms; justification period 512 blocks; round duration = 5 x gossip duration; keeps 3 recent rounds | `service.rs:244, 1002-1038` (`:1004,:1007`); `SDK-ref:substrate/client/consensus/grandpa/src/communication/gossip.rs:121,261,1250` |
| BEEFY + MMR | active, `min_block_delta: 8` (a justification target at most every 8 blocks, so at least 48 s apart). ECDSA keys; MMR hashed with Keccak-256. | | `service.rs:957-1000` (`:973`); `runtime/src/lib.rs:456-464, 470`; `midnight-docs/docs/nodes/index.mdx:118` |
| Partner-chain committee | active. Ariadne v2 selection each sidechain epoch; the epoch length on mainnet is 300 slots (30 min at 6 s: **inference**, arithmetic on a code constant). Committee changes take effect after a delay (test comments say 2 epochs). | max authorities 10,000 | `res/mainnet/chain-spec.json:36`; `runtime/src/lib.rs:578, 589-611, 2008-2016`; `partner-chains/toolkit/committee-selection/authority-selection-inherents/src/select_authorities.rs:53-60` |
| Mainchain (Cardano) follower | inherent data per block: Cardano block hash (`mc_hash`), cNIGHT observations, federated-authority observation, bridge transfers | | `service.rs:473-500` (`PartnerChainsVerifier`, `VerifierCIDP`); `runtime/src/check_call_filter.rs:46-62`; `pallets/cnight-observation/src/lib.rs:68-77` |

Authoring backoff: `unfinalized_slack: 15_600` blocks (the code comment says "around 1 day plus 1 session"; 15,600 x 6 s = 26 h) (`service.rs:734-739`).

Finality time: **no constant found.** [doc] "Finalization usually happens within about 3 blocks (around 18 seconds at a 6-second block time), and can take longer if the network is under stress" (`midnight-improvement-proposals/mps/mps-0028-pre-finality-state-visibility.md:36-38`). The indexer consumes finalized blocks only (section 4).

Documentation inconsistency: `midnight-docs/docs/nodes/index.mdx:89-90` lists "Session length 1200 slots (2 hours)" and "Epoch length 300 blocks". The code constant is `slotsPerEpoch: 300` in the Sidechain pallet (`res/mainnet/chain-spec.json:36`); no 1,200-slot constant was found.

### 1.8 Quoted constants (block, finality, size, peers)

| Quantity | Value | Source |
|---|---|---|
| Block time / slot duration | 6,000 ms (`pub const SLOT_DURATION: u64 = 6 * 1000;`) | `midnight-node/runtime/src/lib.rs:292` |
| Timestamp minimum period | 3,000 ms (`SLOT_DURATION / 2`) | `runtime/src/lib.rs:525` |
| Max block length | 1 MiB for all dispatch classes; Normal class = 75% (`max_with_normal_ratio(1024 * 1024, NORMAL_DISPATCH_RATIO)`). Normal = 786,432 bytes by the SDK-ref formula (**inference**; pinned fork not read). Midnight txs use the default Normal class. | `runtime/src/lib.rs:300, 312-313`; `SDK-ref:substrate/frame/system/src/limits.rs:78-89` |
| Max block weight | 2 s of ref time ("We allow for 2 seconds of compute with a 6 second average block time") | `runtime/src/lib.rs:305-311` |
| Max tx size | 1,048,576 bytes (ledger) | `res/mainnet/ledger-parameters-config.json:152` |
| Ledger block limits | readTime 2e12 ps, computeTime 2e12 ps, blockUsage 1,000,000 bytes, bytesWritten 50,000, bytesChurned 50,000,000 | `ledger-parameters-config.json:156-160` |
| Block hash history | 2,400 blocks | `runtime/src/lib.rs:304` |
| Peer limits | **not found in Midnight code or config.** Upstream defaults: `--out-peers 8`, `--in-peers 32`, `--in-peers-light 100`; `--max-parallel-downloads 5`; `--max-blocks-per-request 64` | `SDK-ref:substrate/client/cli/src/params/network_params.rs:98,102,106,120,175` |
| Default P2P / RPC ports | 30333 / 9944 | `midnight-node/README.md` (configuration table); `midnight-docs/docs/nodes/index.mdx:93-94` |
| RPC subscription cap | `--rpc-max-finality-subscriptions` default 512 (GRANDPA + BEEFY combined) | `node/src/cli.rs:46-49` |
| Finality time | not found as a constant; [doc] about 3 blocks / 18 s | see 1.7 |

---

## 2. Node roles and operators

### 2.1 Roles

| Role | How it is defined | Source |
|---|---|---|
| Validator / block producer | Node with `--validator`; runs Aura authoring, GRANDPA voter, BEEFY. Needs a PostgreSQL Cardano db-sync instance. | `midnight-docs/docs/nodes/_run-a-validator/index.mdx:8`; `midnight-docs/docs/nodes/full-node.mdx:19-22`; `service.rs:840-899` |
| Full node | Prunes states older than 256 blocks by default | `full-node.mdx:160` |
| Archive node | `--pruning archive`; needed for explorers, historical queries | `full-node.mdx:163-175` |
| Boot node | Normal node with a public `--listen-addr` | `boot-node.mdx:26-53` |
| RPC node | Default RPC bound to `127.0.0.1`, `--rpc-methods Safe`; docs recommend a hardened reverse proxy for rate limiting | `midnight-docs/docs/nodes/rpc-node.mdx:28-76` |
| Indexer | Separate services: chain-indexer (single writer), wallet-indexer, indexer-api, spo-indexer; cloud mode (PostgreSQL + NATS) or standalone (SQLite + in-memory pub/sub). Production environments run two instances behind `indexer.<env>.midnight.network`. | `midnight-indexer/docs/architecture.md:7-52`; `midnight-indexer/docs/re-indexing.md` ("Every deployed environment runs two indexer instances behind `indexer.<env>.midnight.network`") |
| Proof server | Stand-alone service; wallet SDK posts to `/prove` and `/check` | `midnight-wallet/packages/prover-client/src/effect/HttpProverClient.ts:25-26`; `midnight-ledger/proof-server/` (present, not read in detail) |
| Cardano side | cardano-node, Ogmios (registration tx submission) and db-sync | `midnight-docs/docs/nodes/_run-a-validator/index.mdx:51-76` |
| Telemetry | `substrate-telemetry` repo exists; mainnet chain spec has `"telemetryEndpoints": null`; Midnight also pushes Prometheus remote-write metrics when configured | `midnight-node/res/mainnet/chain-spec.json:11`; `midnight-node/README.md` (configuration table); `node/src/metrics_push.rs` |

Who actually runs each role today (names): **not found** in the local repos. Operator identities do not appear; only keys do.

### 2.2 Validator admission

- Committee = permissioned candidates plus Cardano-registered candidates, in proportions fixed by the **D-parameter**, selected each sidechain epoch by `ariadne_v2` (ChaCha20 with seed from Cardano epoch nonce and sidechain epoch). Registered candidates carry a weight equal to their stake delegation; permissioned candidates weigh 1. Guarantee: a candidate with expected `P + Q` seats gets at least `P`. If one class is absent, its seats go to the other. (`partner-chains/toolkit/committee-selection/selection/src/ariadne_v2.rs:10-48`; `.../authority-selection-inherents/src/select_authorities.rs:40-60`; `.../filter_invalid_candidates.rs:106-121`)
- The D-parameter is read from the on-chain `SystemParameters` pallet, not from Cardano (`runtime/src/lib.rs:589-597`). It is changed by Root, which governance reaches through the Council/Technical Committee (`pallets/system-parameters/src/lib.rs`; `runtime/src/lib.rs:957-960`).
- Mainnet genesis: `num_permissioned_candidates: 10`, `num_registered_candidates: 0` (`midnight-node/res/mainnet/system-parameters-config.json:6-9`), with exactly 10 permissioned key sets (`midnight-node/res/mainnet/permissioned-candidates-config.json:3-`; each carries `aura_pub_key`, `grandpa_pub_key`, `sidechain_pub_key`, `beefy_pub_key`). The permissioned list lives under a Cardano policy id (`permissioned-candidates-config.json:2`). Preview and qanet have 6; preprod lists 13 permissioned keys with `num_permissioned_candidates: 130` (as read from `res/preprod/*.json`).
- Registered path (SPO): the operator must already run a Cardano stake pool; three-step `midnight-node wizards register1/2/3` submits a registration to the Committee smart contract on Cardano via Ogmios; eligibility after "n+2 epochs" (`midnight-docs/docs/nodes/_run-a-validator/index.mdx:62-78`; `step-3.mdx:289-352`). Registrations are validated by `filter_trustless_candidates_registrations` (`filter_invalid_candidates.rs:106`).
- [doc] "At mainnet launch, blocks are produced by permissioned validators" (`midnight-improvement-proposals/mps/mps-0019-block-production-rewards-night.md:25`); "Initial validator set: Permissioned nodes operated by Federated Node Operators (FNOs). Stake Pool Operators (SPOs) supported at a later date." (`midnight-docs/docs/nodes/index.mdx:98`). [doc] "There is no slashing if one is offline" (`_run-a-validator/index.mdx:41`).
- Governance bodies: Council (6 members) and Technical Committee (9 members) on mainnet, with membership observed from Cardano policy ids (`midnight-node/res/mainnet/federated-authority-config.json:2-25`; `pallets/federated-authority-observation/src/lib.rs`). Runtime upgrades pass through `apply_authorized_upgrade` (`runtime/src/check_call_filter.rs:35-37`).
- Safe mode and tx-pause exist and can block `send_mn_transaction` (user traffic is deliberately not whitelisted in safe mode) (`runtime/src/lib.rs:321, 741-800`; `runtime/src/check_call_filter.rs:40-45`).

### 2.3 Fees, rewards and incentives in code

| Mechanism | What the code shows | Source |
|---|---|---|
| User fees | Paid in DUST by a `DustSpend { v_fee, old_nullifier, new_commitment, proof }` inside the transaction. `v_fee` is public. The DUST value is spent down by `v_fee`; a search of `L9:ledger/src/dust.rs` and `L9:ledger/src/semantics.rs` found **no path that credits `v_fee` to a validator, treasury or pool**; `treasury`, `block_reward_pool` and `reserve_pool` change in the `SystemTransaction` handlers and in claims. **Inference:** fees are burned. | `L9:ledger/src/dust.rs:469-474, 1041-1050`; `L9:ledger/src/structure.rs:3337-3352, 738-770`; `L9:ledger/src/semantics.rs:583-1013` |
| Block rewards | Ledger has `block_reward_pool` and `unclaimed_block_rewards` and a claim transaction (`ClaimRewardsTransaction`). The node-side hook returns `(0, None)` in both feature configurations and the `pallet_block_rewards` wiring is commented out. System transactions are Root-only; the C2M bridge pallet may only build `UnlockToTreasury`, `DistributeReserve`, `DistributeNight(ClaimKind::CardanoBridge, _)`. | `L9:ledger/src/structure.rs:1845`; `midnight-node/runtime/src/lib.rs:681-698, 1137`; `pallets/midnight-system/src/lib.rs:187-199`; `primitives/midnight/src/lib.rs:61-65` |
| Reward payout status | [doc] "At mainnet launch, blocks are produced by permissioned validators. Reward mechanics become load-bearing only as the network decentralizes" and "No withdrawal path exists, so rewards are stranded" (the problem statement of a Proposed MPS) | `mps-0019-block-production-rewards-night.md:25, 33` |
| Staking | MIP-0016 (Draft): rewards through producing pools funded from the Reserve | `midnight-improvement-proposals/mips/mip-0016-night-staking.md:6, 34, 100` |
| DUST generation | Holding NIGHT (as cNIGHT on Cardano) generates DUST: cap `night_dust_ratio` = 5,000,000,000 Specks per Star (= 5 DUST per NIGHT), `generation_decay_rate` = 8,267 Specks per Star per second, `dust_grace_period` = 10,800 s | `midnight-node/res/mainnet/ledger-parameters-config.json:164-168`; `midnight-docs/docs/concepts/dust-architecture.mdx:102-111`; `midnight-indexer/docs/api/v4/api-documentation.md:354-358` |
| Slashing | none (see above) | |
| Indexer / RPC / proof-server operators | **No on-chain payment or incentive mechanism found.** Proof serving is discussed as a trust problem in an MPS (Proposed). | `mps-0004-trusted-proof-serving.md:34-50` |
| Throttle | per-account byte/tx window on signed (governance) extrinsics only | 1.6 |

---

## 3. Ledger and events

### 3.1 What the ledger records for a transaction (ledger 9)

`Transaction` is `Standard(StandardTransaction)` or `ClaimRewards` (`L9:ledger/src/structure.rs:1385-1390`). A standard transaction contains (`L9:structure.rs:1667-1674`):

| Field | Content | Source |
|---|---|---|
| `network_id` | string | |
| `intents: HashMap<Segment, Intent>` | per segment: `guaranteed_unshielded_offer`, `fallible_unshielded_offer` (UTXO inputs and outputs with signatures), `actions` (contract Call / Deploy / Maintain), `dust_actions`, `ttl`, `binding_commitment` | `L9:structure.rs:873-882, 773-782, 3027` |
| `guaranteed_coins: Option<ZswapOffer>`, `fallible_coins: HashMap<Segment, ZswapOffer>` | Zswap shielded offers | `L9:zswap/src/structure.rs:485-497` |
| `binding_randomness` | Pedersen binding | |

Details:
- **Zswap input:** `nullifier`, Pedersen `value_commitment`, optional `contract_address`, `merkle_tree_root`, `proof`. **Output:** `coin_com` (commitment), `value_commitment`, optional `contract_address`, optional `ciphertext` (`CoinCiphertext` = one embedded-curve point plus 6 field elements), `proof` (`L9:zswap/src/structure.rs:214-220, 305-311, 90-96`). Offers also carry `deltas: (shielded token type, i128)`: the net per-type imbalance (`:469-473`).
- **Unshielded:** `UtxoOutput { value: u128, owner: UserAddress, type_ }` in the clear (`L9:structure.rs:3220-3224`); the indexer exposes `owner, value, tokenType, intentHash, outputIndex` (`midnight-indexer/docs/api/v4/api-documentation.md:558-567`).
- **Contract call:** `address`, `entry_point`, `guaranteed_transcript`, `fallible_transcript` (Impact VM operations plus effects), `communication_commitment`, `proof` (`L9:structure.rs:2646-2655`). **Deploy** includes the initial `ContractState`; **Maintain** carries committee signatures (`:2763, 2987`).
- **DUST:** `DustActions { spends, registrations }`. A `DustSpend` is `(v_fee, old_nullifier, new_commitment, proof)`; a `DustRegistration` is `(night_key, dust_address, allow_fee_payment, signature)` (`L9:ledger/src/dust.rs:469-474, 679-685`). DUST state is a commitment tree plus a nullifier set; spends are shielded.
- **Ledger state:** `network_id`, parameters, `locked_pool`, `bridge_receiving`, `reserve_pool`, `block_reward_pool`, `unclaimed_block_rewards`, `treasury`, `zswap` state (commitment tree + nullifier set), `contract` map (address -> `ContractState`), `utxo` state, `replay_protection`, `dust` state (`L9:structure.rs:3337-3352`).
- **Replay protection:** an intent hash set kept by TTL. The intent `ttl` must satisfy `tblock <= ttl <= tblock + global_ttl` (`midnight-ledger/spec/intents-transactions.md:131`; mainnet `global_ttl` = 1,209,600 s = 14 days: `ledger-parameters-config.json:176`).
- **Segments and fallibility:** the guaranteed segment (id 0) pays fees and cannot fail; fallible segments can fail individually, giving `Success`, `PartialSuccess`, or `Failure` (`L9:structure.rs:1661`; node events `TxApplied` vs `TxPartialSuccess`, `pallets/midnight/src/lib.rs:426-431`).

### 3.2 Events that already exist, and where they stop

Three layers:

**(a) Substrate (FRAME) events from `pallet-midnight`** (`midnight-node/pallets/midnight/src/lib.rs:246-263`): `ContractCall{tx_hash, contract_address}`, `ContractDeploy`, `TxApplied`, `ContractMaintain`, `PayoutMinted`, `ClaimRewards{tx_hash, value}`, `UnshieldedTokens{spent, created}`, `TxPartialSuccess`. Emission code: `pallets/midnight/src/lib.rs:378-432`. They contain tx hash and contract addresses only; no contract-emitted payload.

**(b) Ledger events** (`EventDetails`, `L9:ledger/src/events.rs:88-127`): `ZswapInput`, `ZswapOutput` (with `ZswapPreimageEvidence::{Ciphertext, PublicPreimage, None}`, and `try_with_keys` for trial decryption, `:60-80`), `ContractDeploy`, `ContractLog { address, entry_point, logged_item: VersionedLogItem }`, `ParamChange`, `DustInitialUtxo`, `DustGenerationDtimeUpdate`, `DustSpendProcessed`. They are produced while applying a transaction; contract logs are pushed in `L9:ledger/src/semantics.rs:1491-1498`. **The node discards them**: `apply_transaction` returns only state root, tx hash, `all_applied`, call/deploy/maintain addresses, claim values and UTXO deltas (`midnight-node/ledger/src/ledger_9/mod.rs:460-470`). The proposals say the same: "Events are not consensus state ... the node discards them after verification" (`mips/mip-0002-public-contract-log-emission.md:154-162`); "events discarded at the ledger-bridge boundary" (`mps-0007-node-event-visibility.md:31`, Proposed). The **indexer re-executes every transaction against its own ledger copy** to recover them (`midnight-indexer/docs/architecture.md:15-19`; `mps-0007-node-event-visibility.md:31`). There is no node-side event store; `midnight-architecture/apis-and-common-types/event-log/Readme.md` (Draft) describes one that was never built ("Transport API: Undefined", lines 93-96).

**(c) Compact `emit` and `VersionedLogItem`** (ledger 9 / Compact 0.33; see the generation caveat 0.3):
- Impact VM op `log` (`L9:onchain-vm/src/ops.rs:172` `Log`, opcode byte `0x09` at `:481`). The argument may be at most `MAX_LOG_SIZE = 1 << 19` (512 KiB), else the program fails (`L9:onchain-vm/src/vm.rs:39, 561-568`). The log charges gas and counts the whole size as both bytes written and bytes deleted (churn) (`L9:onchain-vm/src/vm.rs:596-604`).
- The emitted value is decoded as `VersionedLogItem { version: u32, event_type: LogEventType, data }` (`L9:onchain-vm/src/ops.rs:83-143`, `vm.rs:248-276`). A malformed value degrades to `version 0, Misc`. **Events whose `data` exceeds `MAX_LOG_EMITTED = 1 << 10` (1 KiB, counting 32 bytes of hash per storage node plus the node data) are silently dropped**: the source comment reads "The size limit over which `log` events are silently swallowed" (`vm.rs:41-43, 268-276`; accounting at `storage-core/src/arena.rs:1736-1737`).
- Compact exposes this as `emit(e)` where `e` must be an instance of one of the **standard event structs**; any other struct is a compile error ("is not a declared event type"). `emit` is a disclosure site (all fields must already be `disclose`d) and is not allowed in the constructor (`minokawa-compact/doc/compact-reference.mdx:3495-3540`; `minokawa-compact/compiler/analysis-passes/lower-emit.ss:17-40`; `minokawa-compact/coips/coip-0003.md:57-85`).
- Standard events (tag, serialized size): ShieldedSpend 0/32, ShieldedReceive 1/578, ShieldedMint 2/81, ShieldedBurn 3/49, UnshieldedSpend 4/145, UnshieldedReceive 5/145, UnshieldedMint 6/80, UnshieldedBurn 7/113, Paused 8/0, Unpaused 9/0, **Misc 10/288 = `{ name: Bytes<32>, payload: Bytes<256> }`** (`minokawa-compact/compiler/midnight-events.ss:17-74`; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:265-420`). `Misc` is the only custom-data event. Event format version is 1 (`minokawa-compact/compiler/events.ss:31`).
- Size limits disagree across layers: Compact's `max-emit-size` is 512 KiB ("Must match MAX_LOG_SIZE", `events.ss:33-37`); the ledger silently drops events over 1 KiB (`vm.rs:43`); MIP-0002 and CoIP-0003 say "capped at 1 KB serialized" (`mip-0002:46, 129`; `coip-0003.md:85`). With the fixed standard structs the largest event is 578 bytes, so the practical ceiling is the 256-byte `Misc.payload`.
- Events are readable from TypeScript through `CircuitContext.events` during local execution (`minokawa-compact/runtime/src/circuit-context.ts:185, 499-505`).
- MIP-0002 status is **Accepted**; CoIP-0003 is **Draft**; MIP-0019 (multipart `Misc` events) is **Proposed** (`mip-0002...md:6`; `coips/coip-0003.md:6`; `mip-0019-multipart-event.md:6`).
- Phase semantics: events in a fallible segment are discarded if that segment fails; MIP-0019 therefore tells publishers to keep all parts of a message in one phase of one intent (`mip-0019-multipart-event.md:64-78`).

Events seen by consumers are ordered by an indexer-assigned monotonic `id`, and within a transaction by ledger emission order (`indexer-api/graphql/schema-v4.graphql:1971`; `mip-0019:64`).

### 3.3 How a contract can publish or expose data

| Way | Visibility | Limit / cost | Source |
|---|---|---|---|
| `export ledger` fields written with `disclose`d values (cells, counters, `Set`, `Map`, `List`, Merkle trees) | Public. Everything passed to a ledger operation and every ledger read/write is public; the exception is `MerkleTree`/`HistoricMerkleTree` inserts, which hide the value from observers (though a guesser can verify a guess). | persistent bytes cost write price, 50,000 net bytes per block | `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:12-30`; ADT list `minokawa-compact/doc/ledger-adt.mdx:153-317`; `midnight-node/res/mainnet/ledger-parameters-config.json:156-160` |
| `emit(Misc{name, payload})` or standard events | Public to anyone reading the chain; indexed by indexer | 256-byte payload, 32-byte name | 3.2 |
| Circuit return values and exported circuit arguments | Public if the circuit is exported and the transcript includes them (disclosure rules apply) | | `minokawa-compact/doc/compact-reference.mdx:3551-3560` |
| Shielded outputs with a ciphertext to a recipient key | Commitment public; plaintext only to the viewing-key holder | a `CoinCiphertext` (1 point + 6 field elements) | `L9:zswap/src/structure.rs:90-96`; `L9:ledger/src/events.rs:60-80` |
| Contract state read | `midnight_contractState` RPC; indexer `ContractAction.state` (around 1 MB for large states) | | `midnight-node/docs/openrpc.json:10`; `api-documentation.md:479-484` |
| Example | `example-bboard` stores `message: Maybe<Opaque<"string">>`, `state`, `sequence: Counter`, `owner: Bytes<32>` as public ledger fields; `owner` is a hash of a local secret key and a sequence number | | `example-bboard/contract/src/bboard.compact:25-60` |

### 3.4 Public versus private, and exactly what a chain observer learns

Compact model: **witnesses** are TypeScript callbacks that run locally and feed the circuit; their values stay private unless `disclose()` appears on the path to a ledger write, an exported-circuit return, or a conditional that affects either (`minokawa-compact/doc/compact-reference.mdx:3551-3600`). Private state is stored locally by the `PrivateStateProvider`; the LevelDB provider encrypts at rest with a PBKDF2-derived key (`midnight-js/packages/level-private-state-provider/src/storage-encryption.ts:46-89`). The compiler rejects undeclared disclosure ("potential witness-value disclosure must be declared but is not").

| Artifact | Observer learns | Observer does not learn |
|---|---|---|
| Contract call | contract address, entry-point name, the public transcript (ledger operations with values), declared effects (claimed nullifiers, receives, mints, unshielded in/out), the proof, segment, success/failure | witness values, private state, which user called (no signer at the Substrate layer) |
| `emit` | `version`, event type, all field values (public by construction), emitting contract, entry point, transaction | who emitted it, unless a field or the DUST/unshielded inputs reveal it |
| Shielded offer | nullifiers, output commitments, Pedersen value commitments, tree root, optional contract address, ciphertext, proof, per-token-type net `deltas` (i128, in the clear) | coin owner, value, token type of individual coins, which output a nullifier spends |
| Unshielded offer | owner address, value, token type, intent hash for every input and output | |
| DUST fee | `v_fee` (public number), a DUST nullifier and new commitment, proof, plus registration pairs `(night_key, dust_address)` when registering | which DUST UTXO paid; the payer |
| Block | author, timestamp, state roots, fee-price state, transaction hashes, paid fees per tx | |
| Network | the IP of whoever submits to a node and the first-seen node of a gossiped tx (**inference**: standard Substrate gossip, no mixnet, no onion routing; neither was found) | |
| Indexer queries | which address, contract or nullifier prefix a client subscribes to | |

---

## 4. Indexer

### 4.1 Components and data flow

`node --subxt--> chain-indexer --writes--> DB <--> indexer-api --GraphQL--> clients`; NATS (or in-memory pub/sub in standalone) carries ID-only `BlockIndexed`, `UnshieldedUtxoIndexed`, `WalletIndexed` signals (`midnight-indexer/docs/architecture.md:9-42`). The chain-indexer is the single writer, consumes **finalized blocks only** (`midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128-181`; the "safety margin" for recent blocks is one GRANDPA session, 400 blocks, `:83-86`), applies each block to its own `LedgerState` and checks Merkle roots against the node's (`docs/architecture.md:15-19`). Pre-finality data is not available through the indexer (`mps-0028-pre-finality-state-visibility.md:53-57, 83-86`, Proposed).

### 4.2 GraphQL API (v4)

- HTTP queries/mutations: `POST /api/v4/graphql`; subscriptions: WebSocket at `/api/v4/graphql/ws`, subprotocol `graphql-transport-ws`, plus an opt-in zlib-compressed `graphql-transport-ws` variant (`midnight-indexer/docs/api/v4/api-documentation.md:48-58`; `indexer-api/src/infra/api/v4.rs:431-467`; `.../v4/ws_deflate.rs`). Introspection is supported (`api-documentation.md:60-80`). Schema SDL: `indexer-api/graphql/schema-v4.graphql`.
- Queries: `block`, `transactions`, `contractAction`, `contractEvents(filter, limit, offset)` (@beta, `schema-v4.graphql:1302`), merkle-tree collapsed updates, DUST, governance history, SPO analytics (`api-documentation.md:25-30`).
- Mutations: `connect(viewingKey, options)` returns a session id; `disconnect(sessionId)` (`schema-v4.graphql` `type Mutation`; `api-documentation.md:594-637`).

### 4.3 Subscription endpoints

| Subscription | Arguments | Resume / cursor | Notes | Source |
|---|---|---|---|---|
| `blocks` | `offset: {hash or height}` | block offset | each finalized block | `schema-v4.graphql:1940`; `api-documentation.md:643-661` |
| `contractActions` | `address`, `offset` | block offset | Deploy/Call/Update with `state`, `zswapState`, `unshieldedBalances` | `:1965`; `api-documentation.md:663-679` |
| **`contractEvents`** (@beta) | `filter { contractAddress (required), types[], fieldPrefixes[], fromBlock, toBlock, transactionHash }`, `id` | `id` inclusive, monotonic; `max(id, fromBlock cursor)`; completes at `toBlock` | replay then live in one stream; event types include `MISC` | `schema-v4.graphql:1971, 548-580`; `indexer-api/src/infra/api/v4/subscription/contract_event.rs:14-22, 56-140` |
| `zswapLedgerEvents` | `id` | `id` inclusive | global stream of all Zswap ledger events; wallets decrypt locally | `schema-v4.graphql:2012`; `.../subscription/zswap_ledger_events.rs:47-70` |
| `dustLedgerEvents` | `id` | `id` | | `schema-v4.graphql:1985` |
| `shieldedTransactions` | `sessionId`, `index` | zswap index | server-side filtered by viewing key; progress events | `schema-v4.graphql:2003`; `api-documentation.md:681-717` |
| `unshieldedTransactions` | `address`, `transactionId` | transaction id | per-address UTXO events, progress events | `schema-v4.graphql:2008`; `api-documentation.md:719-754` |
| `shieldedNullifierTransactions`, `dustNullifierTransactions` | nullifier **prefixes**, `fromBlock`, `toBlock` | block range | returns tx references; prefix length chosen by the client | `schema-v4.graphql:1998, 1992`; `api-documentation.md:815-825` |
| `dustGenerations` (@beta) | `dustAddress`, `blockHash`, `dtimeCutoffHeight` | snapshot at a block | | `schema-v4.graphql:1981` |
| `bridgeEvents`, `bridgePoolUpdates`, `bridgeBalance` (@beta) | | `from` id | cNIGHT bridge | `schema-v4.graphql:1947-1960` |

Event types on `contractEvents`: `ShieldedSpend/Receive/Mint/Burn`, `UnshieldedSpend/Receive/Mint/Burn`, `Paused`, `Unpaused`, `Misc` (`schema-v4.graphql:582-625`). `MiscContractEvent` exposes `name` (32 bytes) and `payload` (up to 256 bytes) (`:1125-1165`). Indexed-field prefix filters work on **standard events only**, not `Misc`; `Misc` indexing is "entirely on the end user" (`schema-v4.graphql:558-562`; `mip-0002...md:506`; `midnight-js/packages/types/src/public-data-provider.ts:480-482`). Each `ContractCall` also exposes nested `contractEvents` (events are attributed by address and entry point; ambiguous cases are only reachable via the top-level query) (`schema-v4.graphql:491-498`).

### 4.4 Wallets, viewing keys and sessions

- **Legacy/server-assisted path:** `connect(viewingKey)` stores the (encrypted) viewing key, a fresh `session_id` and a start index; wallet-indexer then **trial-decrypts every new transaction against each active wallet's viewing key** and materialises relevant transactions; `shieldedTransactions(sessionId, index)` streams them. A heartbeat every 10 minutes keeps the wallet "active"; wallet-indexer expires inactive wallets after 30 minutes (`docs/architecture.md:20-31`; `wallet-indexer/src/application.rs:248-345`; `indexer-common/src/domain/ledger/transaction.rs:195-223`; `indexer-api/config.yaml:72`; `wallet-indexer/config.yaml:3`). **The viewing key is disclosed to the indexer operator.**
- **Current wallet SDK path:** the shielded wallet does **not** use `connect`. It subscribes to `zswapLedgerEvents` from `appliedIndex - 1` (inclusive cursor, boundary event re-delivered and filtered), receives every Zswap ledger event, and replays them locally with the wallet's `ZswapSecretKeys` (`midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:200-320`; `CoreWallet.ts:167-172`). The indexer therefore learns nothing about which coins belong to the wallet. The DUST wallet uses `dustLedgerEvents` (`dust-wallet/src/v1/Sync.ts:295`), the unshielded wallet uses `unshieldedTransactions(address, transactionId)` (`unshielded-wallet/src/v1/Sync.ts:84`). A grep for `contractEvents`/`ContractEvent` in `midnight-wallet/packages` found nothing.

### 4.5 Resume and ordering

- Event streams (`contractEvents`, `zswapLedgerEvents`, `dustLedgerEvents`) are replayed from the supplied cursor in monotonic id order, then follow `BlockIndexed` signals; each wake-up re-queries from the last seen id in batches (`contract_event.rs:98-140`). Delivery to a client across reconnects is **at-least-once**; midnight-js says persisting consumers should dedup by `id` (`public-data-provider.ts:507-509`).
- Because the indexer reads finalized blocks only, there are no reorg-induced retractions in these streams. **Inference.**
- A missed pub/sub signal only delays delivery to the next `BlockIndexed` (the loop is signal-driven but each drain queries by id). **Inference.**

### 4.6 Storage backend and sizes

- PostgreSQL (cloud) or SQLite (standalone). The ledger arena (a content-addressed node store) is held in the same PostgreSQL (`ledger_db_nodes`, `ledger_db_roots`) or a separate SQLite file (`midnight-indexer/docs/re-indexing.md:30-31`; `README.md:70`).
- Measured sizes quoted in the repo: a previous schema stored full contract state per action, "on preprod 301 GB of a 292 GB database, with individual states reported at around 860 KB" (sic; the figures are as written, `docs/re-indexing.md:49-53`). Current schema stores arena keys and shares structure; on stagenet 14 actions on one contract shrank from 257,530 bytes to 18,956 bytes (`re-indexing.md:55-60`).
- Retention: `ledger_state_retention: 1000` recent blocks stay loadable; GC runs every 25 blocks with a 200 ms budget per block (`chain-indexer/config.yaml:8-16`).
- Contract-event storage projections (MIP-0002 Appendix B): "~703 MB/day / ~250 GB/year" raw upper bound with sidecar index rows of about 150 bytes each (`mip-0002...md:508-540`). The appendix assumes events consume the 50 KB persistent `bytes_written` budget, while the same MIP's fee section and the code count log bytes as churn (3.2, `mip-0002...md:144`), so treat these numbers as a loose bound.
- Ledger-event table gets `contract_address` and `contract_action_id` columns and a `contract_event_indexed_fields` sidecar table (`indexer-common/migrations/postgres/006_contract_events.sql`).

### 4.7 Throughput and pagination limits (indexer-api defaults)

In this table `:N` alone means `midnight-indexer/indexer-api/config.yaml:N`.

| Limit | Value | Source |
|---|---|---|
| Request body | 1 MiB | `indexer-api/config.yaml:45` |
| Query complexity / depth | 200 / 15 | `:46-47` |
| Subscription batch size (all stream types) | 20 rows per drain | `:49-77` |
| Progress updates (shielded, unshielded) | every 30 s | `:68, 75` |
| Subscriptions per WebSocket connection | 20 | `:83` |
| New `shieldedTransactions` subscriptions per session id | 10 per minute | `:84` |
| `contractEvents` query | default `limit` 100, clamped to 1-500; `offset` is only stable within a fixed `toBlock` window | `indexer-api/src/infra/api/v4/query.rs:478`; `public-data-provider.ts:476-478` |
| DB pool | 25 connections | `:30` |
| Concurrent ledger-backed queries | `ledger_query_concurrency` default = half of pool minus 6 | `indexer-api/config.yaml:9-16` |
| Contract-state cache | 512 MiB, idle 10 min, 6 concurrent loads | `:88-96` |
| DUST generations snapshot age | 500 blocks | `:59` |
| Wallet client sync defaults | buffer 10,000 events, resume threshold 100, batch 10, spacing 4 ms | `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:232-236` |

Sustained events-per-second capacity: **not found** (no benchmark in the repo for `contractEvents`).

---

## 5. Client side

### 5.1 midnight-js

Provider bundle `MidnightProviders`: `privateStateProvider`, `publicDataProvider`, `zkConfigProvider`, `proofProvider`, `walletProvider`, `midnightProvider` (`midnight-js/packages/types/src/providers.ts:39-73`). Responsibilities:
- `PublicDataProvider` (indexer-backed): queries and observables for block, contract state, unshielded balances, `watchForTxData`, and the event API `queryContractEvents(filter, page)` and `contractEventsObservable(filter, { startAt: { fromId | fromBlock } })` (`public-data-provider.ts:305-518`). The `ContractEvent` union covers the 11 event types; `Misc` has `name` and `payload` (`:111-240`). The underlying GraphQL is `CONTRACT_EVENTS_QUERY` and `CONTRACT_EVENTS_SUB` (`indexer-public-data-provider/src/query-definitions.ts:430-473`). Default page size 100 (`config.ts:34`); polling interval for `watchQuery` paths 1,000 ms (`config.ts:27`).
- Event streaming from the indexer is a real WebSocket subscription; other watchers (`watchForTxData`, contract-state watchers) poll or subscribe through the same client (`observables.ts:156-198, 259-274`).
- `PrivateStateProvider`: encrypted LevelDB (3.4).
- `WalletProvider`/`ProofProvider`: balancing and proving; proving is delegated to a proof server over HTTP.
- midnight-js does no trial decryption itself; it relies on the wallet.

### 5.2 Wallet SDK: sync and decryption

Covered in 4.4. Summary: the shielded wallet receives the global `zswapLedgerEvents` stream and **trial-decrypts locally** (`ZswapPreimageEvidence::try_with_keys` in the ledger crate, `L9:ledger/src/events.rs:60-80`; `try_decrypt` at `L9:zswap/src/keys.rs:140`). The encryption is Diffie-Hellman on the embedded curve with Poseidon in CTR mode (`midnight-ledger/spec/zswap.md:15-22`). Transactions are submitted with the Polkadot client (`PolkadotNodeClient.ts:171`). Proving uses the proof server's `/prove` (`HttpProverClient.ts:25`).

### 5.3 DApp connector API (v4)

`InitialAPI.connect(networkId)` returns `ConnectedAPI` (`midnight-dapp-connector-api/src/api.ts:21-58`). Methods: `getShieldedBalances`, `getUnshieldedBalances`, `getDustBalance`, `getShieldedAddresses`, `getUnshieldedAddress`, `getDustAddress`, `getTxHistory(page, size)`, `balanceUnsealedTransaction`, `balanceSealedTransaction`, `signData`, `submitTransaction`, `getProvingProvider`, `getConfiguration`, `getConnectionStatus`, `hintUsage` (`api.ts:70-203`). `getConfiguration` returns `indexerUri`, `indexerWsUri`, `substrateNodeUri`, `networkId` (`api.ts:206-220`). **There is no event or subscription method.** A DApp reads events by opening its own connection to the indexer URI the wallet reports.

### 5.4 Where an agent, a contract and a wallet each consume events today

| Consumer | Mechanism today | Source |
|---|---|---|
| Off-chain agent / service | `contractEventsObservable` (or raw `contractEvents` subscription) against an indexer; resume with `fromId`; filter by contract address (required), event type, and for standard events by indexed-field prefix. Alternative without events: poll `midnight_contractState` or `contractActions` and diff state (the pre-events method MIP-0002 describes). | 5.1; `mip-0002...md:55-62` |
| Smart contract | **No on-chain subscription or event-read primitive found.** Events are not stored in contract or ledger state (MIP-0002:154-162). Contracts can call other contracts synchronously (Compact 0.33 cross-contract calls) and read their own ledger fields; callee must have no private state/witnesses at present (`toolchain-0.33.0.md:98-104` restrictions list). A contract can only be "pushed to" by a call. | `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:24, 88-104` |
| Wallet | Shielded coins: global `zswapLedgerEvents` + local decrypt; DUST: `dustLedgerEvents`; unshielded: `unshieldedTransactions(address)`. No contract-event consumption in the wallet SDK. | 4.4 |

---

## 6. Cryptography on chain

### 6.1 Primitives

| Area | What the code uses | Source |
|---|---|---|
| Proof system | PLONK-style (halo2 lineage) with **KZG** commitments over **BLS12-381**; ledger links `midnight-proofs`, `midnight-circuits`, `midnight-zk-stdlib` | `midnight-zk/README.md:9-17`; `L9:transient-crypto/Cargo.toml:30-33`; `L9:transient-crypto/src/proofs.rs:25` |
| Curves | BLS12-381 (outer) and **JubJub** (embedded), implemented in `midnight-curves`; Compact also types secp256k1, secp256r1, Curve25519 points | `midnight-zk/README.md:9`; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:565-860` |
| Verifier parameters | `bls_midnight_2p14`: KZG verifier params up to degree 2^14 (`VERIFIER_MAX_DEGREE = 14`), embedded in the binary | `L9:transient-crypto/src/proofs.rs:108-128` |
| Transient hash | Poseidon over the BLS12-381 scalar field (in-circuit friendly) | `L9:transient-crypto/src/hash.rs:23,76` |
| Persistent hash | SHA-256 (`PERSISTENT_HASH_BYTES` = 32) | `L9:base-crypto/src/hash.rs:23,94` |
| Other hashes in Compact | `keccak256`, `sha512` (ZKIR v3 for Keccak-256, secp256k1 and ECDSA) | `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:547-565`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:30` |
| Signatures (ledger) | Schnorr over secp256k1 (BIP340) for unshielded offers; ECDSA over secp256k1 | `L9:base-crypto/src/schnorr.rs:14`; `L9:base-crypto/src/ecdsa.rs:14` |
| Signatures in Compact circuits | `jubjubSchnorrVerify`, `secp256k1EcdsaVerify`, `secp256r1EcdsaVerify`, `ed25519Verify` | `exports.md:921-1010` |
| Coin keys | 256-bit secret key; public key = SHA-256 of it; encryption key is a JubJub point | `midnight-ledger/spec/zswap.md:10-31` |
| Commitments | Pedersen (value commitments, binding commitment per intent); coin commitments are hashes; Merkle trees with transient hashes | `L9:zswap/src/structure.rs:306`; `L9:structure.rs:873-882` |
| Nullifiers | `coin.nullifier(sk)` in a global set; DUST nullifiers in a separate set | `midnight-ledger/spec/zswap.md:117-127,205-207`; `L9:ledger/src/dust.rs:471` |
| Node consensus keys | sr25519 (Aura), Ed25519 (GRANDPA), ECDSA (Partner Chains, BEEFY); runtime hashing Blake2-256, MMR Keccak-256 | `midnight-docs/docs/nodes/index.mdx:118-120`; `midnight-docs/docs/concepts/network-architecture/cryptography.mdx:16-24`; `runtime/src/lib.rs:339, 470` |

### 6.2 Proof sizes and timing

| Quantity | Value | Source |
|---|---|---|
| Zswap input proof | 4,832 bytes, 68 public inputs | `L9:zswap/src/structure.rs:633-634` |
| Zswap output proof | 4,832 bytes, 77 public inputs | `:635-636` |
| DUST spend proof | 2,912 bytes, 138 public inputs | `L9:ledger/src/dust.rs:2158-2159` |
| Contract call proof | **no fixed size found**; the ledger estimates unproven calls at `PROOF_SIZE` = 4,832 bytes each. Verifier key estimate 2,875 bytes. | `L9:structure.rs:619, 1908, 1911` |
| Proof verification (cost-model, genesis) | constant 3,273,586,253 ps (3.27 ms) + 4,555,132 ps per public input; verifier-key load 1,529,923,104 ps; Pedersen check 277,513,481 ps; signature verify 97,304,512 ps; `ec_mul` 127,815,559 ps; Poseidon `transient_hash` 86,465,888 ps | `ledger-parameters-config.json:124-133`; `L9:structure.rs:1129-1133` |
| Validation discount | compute time of validation multiplied by `validation_factor` = 1/4 (`parallelism_factor: 4`) | `ledger-parameters-config.json:143`; `L9:structure.rs:1244` |
| Proving time (doc claim) | "A single ZSwap spend proof requires ~190ms on a 32-core server but can take 5-30 seconds on a consumer laptop and is infeasible in WASM on mobile browsers"; "~50 MB of RAM per proof" | `mps-0004-trusted-proof-serving.md:33, 49` (Proposed MPS, [doc]) |
| Proving time (docs) | "Midnight transactions can take over a minute to finalize while the proof server generates ZK proofs" | `midnight-docs/docs/tutorials/zk-loan/cli.mdx:302` |
| Circuit sizes (docs output) | tutorial linter output shows `k=11` to `k=13` circuits | `midnight-docs/docs/tutorials/bship/smart-contract.mdx:570-598` |
| Proof aggregation/recursion | `midnight-zk/aggregation` implements IVC with constant proof size; **the ledger does not depend on it** (no `aggregat` in any ledger Cargo.toml) | `midnight-zk/aggregation/src/ivc/mod.rs:1-20` |

The tutorial linter prints "proof payload: ~96KB" for `k=11` and "~192KB" for `k=12`; no local source defines that field, so I do not use it as a proof size.

### 6.3 What is usable for tags, rate limiting, anonymous credentials

All patterns below are Compact-contract patterns on existing primitives; the ledger itself provides no credential or rate-limit primitive.

- **Anonymous membership in a group, once-only use.** The documented pattern: a `HistoricMerkleTree<N, Bytes<32>>` of authorised commitments `H("commitment-domain", sk)`, a `Set` of nullifiers `H("nullifier-domain", sk)`; the circuit proves (in ZK) a Merkle path to the commitment, asserts `authPath.leaf == publicKey(sk)`, and checks and inserts the nullifier. This gives anonymous authorisation with single-use per key, which an event bus can turn into per-epoch rate limiting by scoping the nullifier with an epoch value (**inference**; the doc example is single-use only). Source: `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:105-232`.
- **Domain-separated tags/topics:** `persistentHash<Vector<n, Bytes<32>>>` with a padded domain string is the documented idiom (`keeping-data-private.mdx:218-225`), and `transientHash`/`transientCommit` are available (`exports.md:455-495`).
- **Time gating in circuits:** `blockTimeLt/Gte/Gt/Lte` (`exports.md:1261-1285`).
- **Signature verification inside circuits:** ECDSA/Schnorr/Ed25519 (6.1) lets a contract accept messages authorised by off-chain keys without revealing the key on-chain **only if** the signature is checked in-circuit and not disclosed (**inference**).
- **Shielded token primitives:** nullifiers and Pedersen-committed values; `createZswapInput/Output`, `sendShielded`, `receiveShielded` (`exports.md:1092-1180`).
- **Verifiable credentials / DID repos** exist in the workspace (`midnight-did`, `midnight-verifiable-credentials`, `midnight-trust-registry`); they were not examined.
- **Rate limiting at protocol level:** only by price (DUST) and block budgets; no per-identity limiter exists (section 7).

---

## 7. Cost model

### 7.1 Structure

Five cost dimensions: read time (ps), compute time (ps, single-threaded), block usage (bytes), bytes written (persistent net), bytes churned (temporary) (`midnight-ledger/spec/cost-model.md:32-39, 56-76`). A transaction's `SyntheticCost` is normalised by the block limits (a transaction exceeding any block limit is invalid) and priced:

```
fee = overall_price * ( max(read_factor*read, compute_factor*compute, block_usage_factor*block_usage)
                        + write_factor*bytes_written + write_factor*bytes_churned )
```
(`L9:base-crypto/src/cost_model.rs:408-417`; fees returned in Specks, 1 DUST = 10^15 Specks: `L9:structure.rs:1943-1953`, `SPECKS_PER_DUST` at `L9:structure.rs:3363`.) Mainnet block limits are in 1.8.

### 7.2 Price dynamics

- Prices adjust each block toward 50% fullness. Each dimension factor and the overall price are multiplied by `1 + f(fullness)`, with `f(x) = -ln(1/x - 1) / a`, clamped to `[0.01, 0.99]`; mainnet `a` = 100, so the maximum change is about 4.6% per block (**inference**: table maximum 4.59512 divided by 100). Dimension factors have a floor of `min_ratio` (= 0.25) times the highest factor; `overall_price` has a floor (`MIN_COST` 100 raw fixed-point units, or `min_block_price`). (`L9:base-crypto/src/cost_model.rs:354-405, 825-948`; `ledger-parameters-config.json:169-178`; `cost-model.md:163-211`.)
- Genesis values: `overallPrice` = 184467440737095516160 / 2^64 = 10.0; all four factors = 1.0 (`ledger-parameters-config.json:169-175`). The current live prices are in each block's `ledgerParameters` (indexer `Block.ledgerParameters`, `api-documentation.md:518`); **current live prices were not found in the repos.**

### 7.3 Per-byte and per-compute costs (genesis parameters)

| Cost | Value | Source |
|---|---|---|
| Block usage | `block_usage = est_size(tx)` in bytes against 1,000,000 | `L9:structure.rs:2034`; `ledger-parameters-config.json:158` |
| Persistent writes | against 50,000 bytes per block | `:159` |
| Churn | against 50,000,000 bytes per block | `:160` |
| Compute | proof verify 3.27 ms + 4.56 us per public input; vk load 1.53 ms; signature 97 us; each at 1/4 for validation | 6.2 |
| `log` instruction | `log_array_coeff_value_size` 1,315,830 ps/byte (array payload), `log_cell_constant` 3,054,417 ps + 505 ps/byte (cell payload); bytes_written = bytes_deleted = size, so a log is pure churn | `ledger-parameters-config.json:26-33`; `L9:onchain-vm/src/vm.rs:564-604` |
| Per-tx baseline compute | 100,000,000 ps | `ledger-parameters-config.json:146` |

Worked example, **inference from genesis parameters, assuming all factors are 1.0 and price is unchanged**: the block-usage term is `10 x bytes / 1,000,000` DUST, i.e. 0.01 DUST per KB; a persistent byte costs `10 / 50,000` = 0.0002 DUST, i.e. 0.2 DUST per KB, which is 20 times a transmitted byte. A typical contract call (about 5 KB, compute about 1 ms) is dominated by the block-usage term (0.005 normalised vs about 0.0006 for compute). One NIGHT generates at most 5 DUST (api-documentation:356), which is about 500 KB of transaction bytes at these prices. Live prices will differ.

### 7.4 DUST mechanics

- DUST is shielded, non-transferable, generated from NIGHT UTXOs, and decays to zero after the backing NIGHT is spent (`dust-architecture.mdx:23-25, 52-72, 124-126`). Capacity `N x night_dust_ratio`, time to cap about 604,800 s (one week) (`:109-111`).
- Grace period: 10,800 s. A transaction is accepted if its declared DUST time is within the grace window of block time (`dust-architecture.mdx:138-140`; `ledger-parameters-config.json:167`).
- A DUST wallet balance cannot be read from the indexer after fee payments because spends are shielded (`api-documentation.md:360-366`).
- Registration links a Cardano reward address and a DUST public key; registration on Cardano takes about 12 hours to reach Midnight (`midnight-docs/docs/tokens/overview.mdx:41`).
- The ledger transaction check "OutOfDustValidityWindow" is why the pool simulates the next block time plus `MaxSkippedSlots` x slot duration (default 1) when validating (`pallets/midnight/src/lib.rs:181-183, 450-468`).

### 7.5 Storage costs, rent and retention

- **State rent: not found** (no occurrence of "rent" or storage deposit in `midnight-ledger/spec` or `L9:ledger/src`). Persistent bytes are paid once at write time through the `bytes_written` dimension; contract state persists indefinitely.
- **Retention rules found:** (i) intent/replay history is dropped after `ttl` (`L9:semantics.rs:1715` `replay_protection.post_block_update`, `time_filter_map`; max `ttl` is `global_ttl`, 14 days on mainnet); (ii) the history of past Zswap Merkle roots (`past_roots`) is filtered to `global_ttl` each block (`L9:zswap/src/ledger.rs:241-253`; `apply_post_block_update` passes `global_ttl` to both the Zswap and DUST updates, `L9:ledger/src/semantics.rs:1717-1725`); a coin proof must reference a root still in that history (`midnight-ledger/spec/zswap.md:205`); (iii) Substrate state pruning default 256 blocks for non-archive nodes (`full-node.mdx:160`); (iv) indexer `ledger_state_retention` 1000 blocks (4.6).
- History growth is an acknowledged open problem: MPS-0032 "History Management" (Proposed) (`mps-0032-storage-management.md:30-70`).

---

## 8. Extension points

For each point, whether a new off-chain event network could attach.

| Extension point | Where | Can an off-chain event network attach? |
|---|---|---|
| **P2P protocol registry** | `net_config.add_notification_protocol` / `add_request_response_protocol` in `service.rs:586, 607-608, 644`; the Midnight ledger-sync protocol is a worked example (`warp_ledger_sync/protocol.rs`, `server.rs`). Protocol names embed the genesis hash. | **Only with a custom node binary.** There is no plugin mechanism; every operator must run the fork for the network to span nodes. A gossip-topic protocol could reuse `sc-network-gossip` (32-byte topics) as GRANDPA/BEEFY do. Peer-set slots are shared with the node (`default_peers_set_num_full`, `service.rs:641`). |
| **Independent P2P sidecar** (own libp2p/gossipsub process next to a node) | none in node | **Yes**, fully decoupled: the sidecar uses node RPC and the indexer for chain reads and submits transactions through the normal path. Nothing in the node assists or forbids it. |
| **Pallets / runtime upgrade** | `construct_runtime` list `runtime/src/lib.rs:1100-1200`; upgrades via governance `apply_authorized_upgrade` | Possible only through a governance-approved runtime upgrade. User-callable surface is deliberately narrow: signed extrinsics are filtered to governance calls (`check_call_filter.rs:25-37, 86-124`), user traffic is `send_mn_transaction` (bare). A new user-facing pallet call would be another bare call with its own `ValidateUnsigned`. |
| **Precompiles / chain extensions / EVM** | none | **not found** |
| **Off-chain workers** | enabled by the config flag (upstream default `WhenAuthority`) with `enable_http_requests: true` and the node's `network_provider`; runtime exposes `OffchainWorkerApi` (`service.rs:710-730`; `runtime/src/lib.rs:1516-1519`; `SDK-ref:substrate/client/cli/src/params/offchain_worker_params.rs:41`) | No pallet implements `offchain_worker` (search in `pallets/`, `runtime/`, `partner-chains/toolkit` found only the generic runtime plumbing), and OCWs run only on validators. An OCW could in principle talk to an external network over HTTP and submit extrinsics, but it needs a new pallet via runtime upgrade, and any extrinsic must pass the governance-only signed filter or be a full proven Midnight transaction. **Inference:** poor fit. |
| **Inherent data** | existing inherents: timestamp, committee (`SessionCommitteeManagement::set`), cNIGHT `process_tokens`, bridge `handle_transfers`, federated-authority `reset_members` (`check_call_filter.rs:46-62`); data providers in `node/src/inherent_data.rs` and `service.rs:482-490, 875-889` | A block producer could carry data from an external network (e.g. a batch root) as an inherent, but this needs a runtime change plus a node change, is limited to the permissioned committee, and puts bytes in every block. **Inference:** possible, restrictive, and not private. |
| **Custom RPC** | `midnight_*`, `systemParameters_*`, `sidechain_*`, `network_*` modules merged in `node/src/rpc.rs:177-257` | Adding a method needs a node build. An RPC node operator could expose a pub/sub RPC if they run a fork; as a public service it is better built as an indexer-style sidecar. |
| **Runtime APIs** | `MidnightRuntimeApi`, `ConsensusEngineApi`, session/committee APIs | read-side only |
| **Indexer GraphQL** | `contractEvents` subscription, filters, `Misc` events | **Yes, the supported read path** for on-chain events. A bus can run its own indexer deployment (standalone mode exists) and add filters/indices; `Misc` has no indexed fields. |
| **Compact: `emit(Misc)`** | 3.2 | Yes, as a public announcement / anchor channel: 32-byte topic name + 256-byte payload, via MIP-0019 up to multiples of 256 bytes. |
| **Compact: calling out** | Witnesses are TypeScript callbacks running on the prover's machine (`compact-reference.mdx:1153,1504`); Impact VM `Op` enum has stack, map, arithmetic, `log` and checkpoint operations and no I/O (`L9:onchain-vm/src/ops.rs:156-`); cross-contract calls exist since Compact 0.33 (`toolchain-0.33.0.md:24`) | Contracts cannot call out to a network. Off-chain data enters only through witnesses and is then proven or disclosed. |
| **Cardano inbound** | Main-chain follower, cNIGHT observation, bridge pallets read Cardano via db-sync/Postgres | One-directional and specific to those pallets (`pallets/cnight-observation/src/lib.rs`); not a generic feed. |
| **Transaction filtering** | `--filter-deploy-txs`; pallet-tx-pause; safe mode | Governance can pause calls or block `send_mn_transaction` (`runtime/src/lib.rs:321`; `check_call_filter.rs:40-46`). This is a risk to any design that depends on on-chain posting. |

---

## 9. Constraints a private event bus must respect

1. **Contract events do not exist on the mainnet generation the docs list; they arrive with ledger 9 / Compact 0.33.** Docs list toolchain 0.31.1 and onchain-runtime 3.0.0 for mainnet; MIP-0002 is Accepted but its Compact front end (CoIP-0003) is Draft (0.3, 3.2).
2. **Custom event payload is 32 + 256 bytes.** `emit` accepts only the standard event structs; `Misc` carries `Bytes<32>` name + `Bytes<256>` payload; events over 1 KiB are silently dropped by the VM; longer messages need MIP-0019 (Proposed) multipart concatenation within one intent and one execution phase (3.2).
3. **Everything emitted is public.** `emit` requires `disclose`d fields; there is no encrypted-event primitive, so a private bus must encrypt payloads itself and publish ciphertext in `Misc`; every reader can enumerate ciphertexts for a contract and subscribers must trial-decrypt (3.2, 3.4; CoIP-0003:107-108 defers private events).
4. **Event latency is finality plus indexing.** The indexer serves finalized blocks only; finality is about 3 blocks / 18 s ([doc]); block time 6 s. There is no pre-finality event stream (4.1; MPS-0028).
5. **Events exist only through the indexer.** The node discards them; readers depend on an indexer (public deployment or self-run) that re-executes the chain. `contractEvents` is `@beta`; at-least-once delivery; dedup by `id` (3.2, 4.3, 4.5).
6. **Posting a message is a full Midnight transaction.** It needs a contract call with a ZK proof, a DUST spend (2,912-byte proof, public `v_fee`), and, **inference**, at least roughly 5-8 KB on the wire (a 2,912-byte DUST proof, a call proof estimated at 4,832 bytes, plus transcript); proving takes seconds on a laptop ([doc]). Block budgets: 1,000,000 bytes of block usage and 1 MiB block length per 6 s block, tx limit 1,048,576 bytes; at genesis prices about 0.01 DUST per KB (6.2, 7.3).
7. **Publish rate is bounded by price, not by identity.** Midnight transactions have no signer; the only limiters are DUST, per-block budgets, intent TTL and replay protection. Per-sender rate limits must be built in contract logic (e.g. epoch-scoped nullifiers from the group-membership pattern) (1.6, 6.3).
8. **Persistent state is expensive and unrefundable; events are cheap churn.** Writing a message into ledger state costs about 20 times a transmitted byte at genesis weights and is capped at 50,000 net bytes per block; no rent was found and nothing prunes contract state. Logs count as churn (7.3, 7.5).
9. **Who sees what.** Observers see contract address, circuit name, transcript, event fields, `v_fee`, unshielded owners and values, shielded deltas; they do not see witnesses, the payer, or coin owners. Reader privacy depends on the indexer operator: `contractEvents` requires a contract address, and `unshieldedTransactions` requires an address; `connect(viewingKey)` gives the operator the viewing key. Only the nullifier-prefix subscriptions and the global `zswapLedgerEvents` stream are designed to leak little (4.3, 4.4, 3.4).
10. **The p2p layer is closed to new protocols without a node fork.** No gossipsub; only Substrate notification/request-response protocols keyed by genesis hash; Yamux limits; peer slots are shared with consensus traffic. A separate overlay needs its own network and may use the chain only for anchoring or authorisation (1.2, 1.5, 8).
11. **Validators are a small, known, permissioned set.** Mainnet: 10 committee seats, Aura round-robin (predictable leaders), D-parameter 10/0; governance can pause user calls. Censorship and liveness assumptions follow from this; BABE migration is planned but not active (1.7, 2.2; MPS-0026).
12. **Contracts cannot read events or call out.** On-chain consumers cannot subscribe; consumption is off-chain. A bus that must trigger on-chain logic needs an explicit follow-up transaction from an off-chain relayer (5.4, 8).
13. **Fees and live limits are dynamic.** Prices move up to about 4.6% per block; block limits and cost model are governance-adjustable parameters; check each block's `ledgerParameters` rather than hard-coding (7.2).
14. **Event delivery follows transaction semantics.** Events from a failed fallible segment never appear; within a transaction they keep emission order; a malformed or oversized log degrades to `version 0 / Misc` or disappears silently. A bus protocol needs its own framing, sequence numbers and integrity checks on top (3.2; `mip-0019-multipart-event.md:64-78`).
