# Ledger interface in Compact: compile results and findings

This experiment wrote the ledger interface of the private event bus in Compact, compiled it with Midnight's toolchain, and measured the circuits. It covers the Registry (PROTOTYPE.md sections 7.2 and 9), the ledger-only fallback (section 10) and a contract consumer (section 9, DEC-022 option (b)). Nothing ran on a Midnight network. The fee figures are derived from the ledger cost model, not measured.

## 1. Toolchain

| Item | Value |
|---|---|
| Compact CLI | 0.5.2 |
| Compiler used | 0.35.0 (debb05f94, 2026-09-29), language 0.27.0, `ledger-9.1.0.0-rc.3`, compact-runtime 0.20.0 |
| Compiler for comparison | 0.31.1, language 0.23.0 (the ledger-8 toolchain that the Midnight docs list for mainnet) |
| Proof backend | ZKIR v2 (the default; no `--feature-zkir-v3` was needed) |
| Key generation | `zkir compile-many`, bundled with the compiler; it downloads KZG parameters `bls_midnight_2p<k>` into `~/.cache/midnight/zk-params` on first use (2^20: 201 MB) |
| Simulator | `@midnight-ntwrk/compact-runtime` 0.20.0, Node.js 24.21.0 |
| Host | 6 cores, 47 GB RAM, WSL2 |

Events (`emit`) arrived with toolchain 0.33.0 (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:26`). Toolchain 0.35.0 is the newest release and states that it targets ledger 9, "not yet deployed on Midnight Mainnet" (`toolchain-0.35.0.md:10`).

## 2. Contracts

### 2.1 registry.compact

Ledger state:

| Field | Type | Requirement |
|---|---|---|
| `members` | `Map<Uint<32>, HistoricMerkleTree<20, Bytes<32>>>`, one tree per membership period | MPE-ECO-004, MPE-ECO-026 |
| `revoked` | `Set<Bytes<32>>` of identity commitments | MPE-ECO-028, MPE-ECO-029 |
| `params` | epoch length, membership period, root window, per-class quota (64, 16, 4, 1), Anchor window, Anchor history, Shard count, activation height, maximum version, bootstrap-list hash | MPE-NET-039, DEC-016 |
| `pending`, `paramsDelay` | proposed parameters and their activation time; time-lock fixed at deployment | MPE-OPS-012 |
| `relays` | `Map<Bytes<32>, RelayEntry>`: Operator id, five role flags, anchorer key commitment | MPE-NET-054, MPE-NET-053 |
| `paused`, `steward` | pause flag; hash of the steward secret | DEC-019 prototype default |
| `anchors` | `Map<Uint<16>, AnchorRecord>`: slot `window mod 2940` to window, root, 8 Shard counts | MPE-NET-050, MPE-STO-028 |
| `anchorTree` | `HistoricMerkleTree<12, Bytes<32>>`: leaf `SHA-256(domain, window, root)` at the same slot | MPE-CON-047, MPE-VER-031 |
| `networkId` | sealed 32-byte Network Identifier | |

Circuits: `register`, `revoke`, `prunePeriod`, `addRelay`, `removeRelay`, `proposeParams`, `activateParams`, `pause`, `unpause`, `setSteward`, `postAnchor`, `pruneAnchor`, `anchorRootValid`. Pure helpers (`memberLeafOf`, `idcOf`, `rlnA1`, `rlnX`, `anchorLeafOf`, `stewardKeyOf`, `relayKeyOf`) are exported for off-chain tools and produce no keys.

Behaviour, with the choices made where the requirements are silent:

- **Registration.** The caller passes an identity commitment and the current membership period. The circuit checks the period against the block time, refuses revoked commitments, creates the period's tree on first use and inserts the leaf `SHA-256(domain, idc, quota)`. The circuit computes the leaf from the current `params.quota`, so a registrant cannot choose its own limits (DEC-016). The period trees replace the "exclude expired memberships from later roots" rule of MPE-ECO-026: a new period starts an empty tree, and `prunePeriod` (callable by anyone) removes a tree one root window after its period ends.
- **Revocation.** The evidence is private: the recovered secret `a0`, epoch, class, credit index, the member's committed quota, two shares `(EID, y)`, and the member's Merkle path. The circuit computes `a1 = H(a0, epoch, class, credit)`, `x_i = H(EID_i)` and checks `y_i = a0 + a1 * x_i` for both shares and `EID_1 != EID_2`. It then checks the path against a historic root, sets the leaf at the path's index to the default value (`insertIndexDefault`) and adds the commitment to `revoked`. The RLN relation uses the native field and `transientHash` (Poseidon), which is what an in-circuit admission proof on Midnight would use; the prototype stand-in uses SHA-256 and curve25519 scalars (PROTOTYPE.md 6.1). Disclosed: period, the root the path proves against, the leaf index, the identity commitment and a reason code. No steward action is involved (MPE-OPS-015).
- **Relay list.** Steward only. Each change emits `Misc { name: "mpe/gov/v1", payload: action u8 ‖ reason u16 ‖ subject 32 B ‖ zero fill }` (MPE-OPS-018). The peer key is SHA-256 of the libp2p peer id, because a libp2p Ed25519 peer id is a 38-byte multihash.
- **Parameters.** `proposeParams` (steward) stores the new values with `effectiveAt = clock + paramsDelay`; `activateParams` (anyone) applies them once the block time passes `effectiveAt`. This puts the MPE-OPS-012 time-lock in the contract; the prototype deploys with a delay of 0 (DEC-019).
- **Pause.** The flag blocks `register` and `postAnchor`. Revocation and pruning stay open (by analogy with MPE-OPS-014: exits and evidence survive a pause).
- **Anchors.** `postAnchor(peer, window, q, slot, root, counts)`: the peer must be listed with the anchorer role and the caller must know the preimage of its key commitment (MPE-NET-053); `window = q * 2940 + slot`; the window closed at least 20 s ago and less than 176,400 s ago; at least one count is non-zero (empty windows produce no Anchor); counts of Shards at or above `shardCount` are zero; a slot that holds the same or a newer window refuses the post (at most one Anchor per window, MPE-NET-041). The record replaces the record 2,940 windows older in the same slot, the Anchor-tree leaf is written at the slot, and one `Misc { name: "mpe/anchor/v1", payload: window u64 BE ‖ root ‖ 8 × count u32 BE ‖ zero fill }` is emitted (MPE-FMT-047, MPE-NET-050). `pruneAnchor` (anyone) removes a record older than P-STO-9 (MPE-STO-029). The slot rule bounds the live records at 2,940 by construction (MPE-STO-028).
- **Consumer read.** `anchorRootValid(root)` is a witness-free circuit, so another contract can call it. It is a historic-root check over the Anchor tree.

### 2.2 fallback.compact

`publishPart(name, payload)` emits one `Misc` and accepts only the name `"mpe/env/v1"` (MPE-FMT-040, MPE-NET-040); several calls in one intent form one MIP-0019 package. `publishClass0(Bytes<256>)`, `publishClass1(Vector<4, Bytes<256>>)` and `publishClass2(Vector<16, Bytes<256>>)` emit a whole Envelope in one call, in order, which keeps every part in one intent and one contract call (MPE-FMT-041, MPE-FMT-042). Class 3 has no circuit (MPE-FMT-044). A transcript without `checkpoint` is one section, which the transaction builder places either wholly in the guaranteed segment or wholly in the fallible one (section 4, item 16); either way the parts share one phase.

### 2.3 consume.compact

`react(notAfter, action)` takes a private witness: EID, window, a 12-step RFC 6962 path to the Shard batch root, a 3-step path from the batch root to the window root (both SHA-256 with `0x00`/`0x01` prefixes and a per-step skip flag for trees whose size is not a power of two), the Anchor-tree path, and the event secret. It checks the chain EID to Anchor-tree root, calls `registry.anchorRootValid(root)` (cross-contract), checks `window * 60 + 172,800 >= notAfter` privately and `blockTime < notAfter` publicly (CON-046 through the anchored creation minute), derives the nullifier `SHA-256("mpe/v1/consume" ‖ N ‖ contract ‖ event secret)` (MPE-CRY-025, MPE-CON-045), refuses a known nullifier and records nullifier and action in the same transition (MPE-CON-044a, MPE-CON-044b). Disclosed: Anchor-tree root, `notAfter`, nullifier, action. Not disclosed: EID, window, Shard, paths, secret.

## 3. Compile results

All three contracts compile with 0.35.0 without changes to their requirements. With 0.31.1, `registry.compact` and `fallback.compact` fail with `unbound identifier emit`; the Registry with its two `emit` statements removed compiles with 0.31.1, so `emit` is the only ledger-9 dependency of the Registry. `consume.compact` fails with 0.31.1 because the ledger-8 cross-contract model needs the callee's compiled `contract-info.json`.

Columns: `k` and rows from `zkir mock-compile -v` (the circuit model of `midnight-zk/proofs/src/dev/cost_model.rs`); proof bytes is that model's `size` field; ZKIR is the JSON `.zkir` file and the binary `.bzkir` file; PI is the number of `declare_pub_input` instructions.

| Contract | Circuit | k | Rows | Proof B | Proving key B | Verifying key B | ZKIR B (.zkir / .bzkir) | PI |
|---|---|---|---|---|---|---|---|---|
| registry | `activateParams` | 8 | 77 | 2,800 | 73,186 | 1,351 | 14,938 / 751 | 229 |
| registry | `addRelay` | 17 | 67,862 | 4,368 | 38,418,022 | 2,119 | 19,058 / 1,272 | 65 |
| registry | `anchorRootValid` | 6 | 46 | 2,800 | 22,669 | 1,351 | 1,708 / 143 | 19 |
| registry | `pause` | 15 | 26,902 | 4,368 | 9,965,323 | 2,119 | 8,793 / 563 | 45 |
| registry | `postAnchor` | 18 | 152,138 | 4,368 | 76,393,028 | 2,119 | 77,676 / 4,964 | 585 |
| registry | `proposeParams` | 15 | 27,842 | 4,368 | 9,966,760 | 2,119 | 14,133 / 868 | 113 |
| registry | `pruneAnchor` | 13 | 2,143 | 4,368 | 2,814,558 | 2,119 | 15,026 / 820 | 197 |
| registry | `prunePeriod` | 7 | 94 | 2,800 | 40,942 | 1,351 | 8,414 / 445 | 109 |
| registry | `register` | 13 | 6,305 | 4,368 | 2,824,152 | 2,119 | 18,133 / 1,031 | 225 |
| registry | `removeRelay` | 17 | 67,236 | 4,368 | 38,417,418 | 2,119 | 18,689 / 1,253 | 62 |
| registry | `revoke` | 17 | 77,971 | 4,368 | 38,458,495 | 2,119 | 36,894 / 2,684 | 134 |
| registry | `setSteward` | 17 | 67,234 | 4,368 | 38,417,267 | 2,119 | 17,426 / 1,179 | 46 |
| registry | `unpause` | 15 | 26,902 | 4,368 | 9,965,324 | 2,119 | 8,794 / 563 | 45 |
| consume | `react` | 17 | 77,905 | 4,368 | 38,492,629 | 2,119 | 32,490 / 2,331 | 128 |
| fallback | `publishClass0` | 18 | 166,241 | 2,800 | 67,427,594 | 1,351 | 36,754 / 2,577 | 24 |
| fallback | `publishClass1` | 20 | 663,950 | 2,800 | 269,585,955 | 1,351 | 148,099 / 10,365 | 96 |
| fallback | `publishClass2` | 22 | 2,651,779 | 2,800 | not generated | not generated | 596,647 / 41,757 | 384 |
| fallback | `publishPart` | 18 | 186,418 | 2,800 | 67,442,022 | 1,351 | 41,256 / 2,901 | 24 |

Compile time (wall clock, `time compact compile`, keys included):

| Contract | Run 1 | Run 2 | Front end only (`--skip-zk`), two runs | Conditions |
|---|---|---|---|---|
| registry (13 circuits) | 7 min 21 s | 10 min 50 s | 0.76 s, 0.76 s | run 1 alone on the host; run 2 beside two other key generations |
| consume (1 circuit, struct preimages) | 55.5 s | 48.2 s | 0.51 s, 0.53 s | both beside the fallback key generation |
| consume, byte-spread preimages (superseded) | stopped after 25 min without a key | | | k = 20, beside two other key generations |
| fallback (4 circuits) | stopped after 22 min without a key | per circuit: `publishPart` 264 s, `publishClass0` 195 s, `publishClass1` 1,105 s (7.1 GB of memory) | 0.55 s, 0.58 s | `zkir compile` per circuit; maximum resident memory 1.8 GB at k = 18 |

Repeated compiles produce identical verifying keys and identical key sizes. Key generation time is dominated by k: about 4 minutes at k = 18 on this host, against well under a minute for the k = 13 to 17 Registry circuits.

The simulator test (`test/registry.test.mjs`, 33 checks, all passed; log in `test/registry.test.log`) ran register, relay management, Anchor posting with five refusal cases, the historic Anchor-root check across a later Anchor, revocation with two refusal cases and the re-registration refusal, pause and unpause, the 16-part fallback call with emission order, the refusal of a foreign `Misc` name, and the hash-encoding checks of section 4, item 13. Simulator transcript gas (VM operations plus the contract state update, `CostModel.initialCostModel()`):

| Call | Compute | Read | Bytes written | Bytes deleted |
|---|---|---|---|---|
| `register` (first in its period, creates the tree) | 16.36 ms | 4.25 ms | 2,982 | 2,702 |
| `postAnchor` | 26.08 ms | 4.68 ms | 2,781 | 3,463 |
| `publishClass0` (1 part) | 1.08 ms | 0 | 414 | 414 |
| `publishClass2` (16 parts) | 17.41 ms | 0 | 10,809 | 10,809 |
| marginal `Misc` inside one call | 1.09 ms | 0 | 693 | 693 |

## 4. Limitations found

Each item names what the design needs, what Compact 0.35.0 offers, and what the contracts do instead.

1. **`emit` needs ledger 9.** Toolchain 0.31.1 rejects `emit` (`unbound identifier emit`). Everything else in the Registry compiles with 0.31.1. Anchors and the fallback therefore depend on a ledger generation that mainnet does not run (MPE-OPS-044).
2. **Turning circuit values into bytes dominates the proving cost, and `emit` needs bytes.** Compact packs a `Bytes<n>` value into field elements; every operation that needs individual bytes (a `Bytes[...]` spread, an index `b[i]`, a `Uint` to `Bytes` cast, and the encoding of an `emit` payload that is not a constant) adds `div_mod_power_of_two` instructions, about 670 rows each. A probe contract (`probe/probe.compact`, compiled with `--skip-zk` and measured with `zkir mock-compile`) isolates the effect: emitting a constant 256-byte payload costs 23 rows (k = 6); emitting a 256-byte circuit argument costs 166,241 rows (k = 18); three chained SHA-256 node hashes cost 133,922 rows (k = 18) when the preimage is built with `Bytes[1, ...l, ...r]` and 12,674 rows (k = 14) when it is a struct of `Bytes` fields, with identical digests. Consequences: one ledger-carried part is a k = 18 proof (`publishPart`, 186,418 rows; `publishClass0`, 166,241 rows); four parts in one call are k = 20 (663,950 rows); sixteen parts need 2,651,779 rows, k = 22 (section 3; the model alone took 18 minutes to compute). `postAnchor` (k = 18, 152,138 rows) spends most of its rows on the payload bytes of its single `emit`. The verifier side does not grow: every proof in the model is 4,368 bytes or less and every verifying key 2,119 bytes or less. The prover side does: the k = 18 proving keys are 67-76 MB, and key generation for `publishPart` took 264 s and 1.8 GB of memory. An Anchor every 60 s means one k = 18 proof per minute per anchorer.
3. **No signer, so authority is a hash preimage proved in circuit.** A Midnight transaction has no sender (notes section 3.4), and `kernel.caller()` returns `none` off chain for a top-level call, so a top-level read fails on chain (`toolchain-0.35.0.md`, "The caller of a circuit"). The steward and the anchorer therefore prove knowledge of a secret whose SHA-256 is in state. The hash itself is cheap (`register` computes two SHA-256 in 6,305 rows); the steward circuits are large (`pause` k = 15, `addRelay`, `removeRelay`, `setSteward` k = 17) because of the byte work of their governance `Misc` payloads and `Bytes<32>` arguments, not because of the key check.
4. **Block time can be compared, not read.** `blockTimeLt` and `blockTimeGte` are the only clock (`ledger-adt.mdx`, Kernel). The contract cannot store "the block time of publication" (MPE-ECO-027). Every time-stamped write takes a caller-supplied clock value and checks it against the block time within a tolerance (900 s here). A transaction that waits in the pool longer than that fails. Publication times must come from the timestamp of the including block, read from the chain.
5. **Every time comparison discloses its operand.** The value passed to `blockTimeLt` appears in the public transcript. A consumer that checks expiry against block time would publish the expiry, which fixes the creation second. `consume.compact` therefore discloses only a coarse `notAfter` that the prover chooses and checks the real bound privately.
6. **A circuit cannot read its own Merkle root.** `root()`, `firstFree()` and `pathForLeaf()` are TypeScript-only (`ledger-adt.mdx`, MerkleTree). The Registry cannot keep a map from root to publication or supersession time (MPE-ECO-027, MPE-NET-055). Readers reconstruct roots from the transaction history.
7. **Root validity cannot be time-bounded.** `HistoricMerkleTree.checkRoot` accepts every past root until `resetHistory`. The 3,600 s root window (P-ECO-5) cannot be enforced by the contract; Bus Nodes enforce it off chain. For the Anchor tree, the consumer's expiry check bounds the useful age instead.
8. **No division, modulo or bitwise operators.** The Anchor slot `window mod 2940` is supplied by the caller with its quotient and checked by multiplication. Role flags are five Booleans instead of a bit mask. Big-endian fields in `Misc` payloads need explicit byte reversal, because `Uint` to `Bytes` casts are little-endian.
9. **No iteration over ledger collections.** Pruning needs an explicit key: `pruneAnchor(slot)` and `prunePeriod(period)` are callable by anyone with the right argument. The ring of 2,940 slots makes the record bound of MPE-STO-028 structural.
10. **Static sizes.** One circuit per size class; the Anchor payload always carries 8 count slots (zero for unused Shards); the RFC 6962 paths are fixed at 12 + 3 steps with a skip flag per step.
11. **DUST cannot be paid to a contract.** DUST is non-transferable and only pays transaction fees (notes section 7.4). A contract cannot require or observe a registration price, so the cost of a membership is the network fee of the registration transaction. A price set by the Registry would need NIGHT or another token, received shielded or unshielded (MPE-ECO-036 applies to the unshielded case).
12. **Inclusion is not authority.** `react` proves that some anchored EID exists and derives a nullifier from a private event secret, but nothing in the circuit binds that secret to that EID. A subscriber holding the inclusion proof could react several times with different secrets. Binding needs either the publisher signature of MPE-CON-043 (DEC-022 option (a); `ed25519Verify` exists but needs `--feature-zkir-v3`) or the sealed body in circuit to recompute the EID and Tag. This was not compiled.
13. **SHA-256 inside circuits is affordable only with struct preimages.** `persistentHash` of a `Bytes<k>` value, and of a struct of `Bytes` fields, is plain SHA-256 of the concatenated bytes (checked in the simulator against Node's SHA-256), so the RFC 6962 batch roots of MPE-NET-051 can be verified in a contract. Written with byte spreads, the 19 SHA-256 evaluations of `react` needed 703,378 rows (k = 20, key generation not finished after 25 minutes); written with struct preimages, as committed, they need 77,905 rows (k = 17).
14. **Cross-contract historic-root check costs a second call.** `react` calls `registry.anchorRootValid`, so a reaction transaction carries two contract calls and two proofs (the Registry side is k = 6). Toolchain 0.31.1 cannot compile the consumer at all (its cross-contract model needs the callee's compiled `contract-info.json`).
15. **`transientHash` is not guaranteed stable across upgrades** (`exports.md`, transientHash). The RLN relation in `revoke` uses it because an in-circuit admission proof would; a protocol hash pinned by the MIP should be one that Midnight commits to keeping.
16. **Large transcripts leave the guaranteed segment.** A transcript with no `checkpoint` goes into the guaranteed segment only if its modelled cost fits the time-to-dismiss budget, `max(2 µs × transaction bytes, 15 ms)` minus the per-transaction reserve; otherwise all of it goes into the fallible segment (`midnight-ledger` 9.1 `ledger/src/construct.rs:1104-1166`). Derived from the measured gas: the 16-part fallback call (27.6 ms against 25.8 ms), `register` and `postAnchor` all exceed it, so their whole transcripts, events included, land in the fallible segment; the fee is paid even when such a call fails. This is still one phase, which MIP-0019 accepts, but it contradicts MPE-FMT-042 ("in the guaranteed phase").
17. **Key generation fetches parameters.** `zkir` downloads `bls_midnight_2p<k>` on first use (2^20 is 201 MB; 2^22 is four times larger), and key generation took 195-264 s at k = 18 (1.8 GB of memory) and 1,105 s at k = 20 (7.1 GB of memory, a 270 MB proving key) on this host.

## 5. Fee estimates (derived, not measured)

**Source tree.** `/home/charl/midnight/midnight-ledger` is ledger 8.2.0-rc.1. The ledger-9 cost code was read from the checkout that the node build uses, `~/.cargo/git/checkouts/midnight-ledger-b2f9c59d942dfdca/9a8777c` (9.1.0.0-rc.4; the node pins rc.5 at `midnight-node/Cargo.toml:480`). It is cited below as L9. CFG is `midnight-node/res/mainnet/ledger-parameters-config.json`.

**Formula.** Each of the five cost dimensions is divided by its block limit; a transaction above any limit is invalid. The fee is

```
fee_DUST = overall_price × ( max(rf·read/R, cf·compute/C, bf·block/B) + wf·written/W + wf·churned/W_churn )
```

(L9 `base-crypto/src/cost_model.rs:277-297, 408-417`). Specks = ceil(fee × 10^15) (L9 `ledger/src/structure.rs:1943-1953, 3363`). The contract-call part of `compute`, `read`, `written` and `churned` is the transcript gas, which the transaction builder declares as one re-run of the program × 1.2 (L9 `ledger/src/construct.rs:783-802, 863`; charged at `structure.rs:2233`). Wallets pay `fees_with_margin` with 5 blocks of margin, a factor of 1.2519 (`structure.rs:1929-1941`).

**Inputs.**

| Input | Value | Source |
|---|---|---|
| Block limits R, C, B, W, W_churn | 2 s read, 2 s compute, 1,000,000 B, 50,000 B, 50,000,000 B | CFG:155-160 |
| `overall_price`; rf, cf, bf, wf | 10.0 DUST (raw 184467440737095516160 / 2^64); 1.0 each | CFG:169-175 |
| Unit prices that follow | 0.005 DUST per ms of compute or read; 1e-5 DUST per block byte; 2e-4 DUST per net written byte; 2e-7 DUST per churned byte | derived |
| Per-transaction baseline compute | 100 µs, in validation and in application | CFG:146 |
| Validation discount | × 1/4 on validation compute only | CFG:143 |
| Proof verification; verifier-key load | 3.27 ms + 4.56 µs per public input; 1.53 ms | CFG:127-129 |
| DUST spend proof | 2,912 B, 138 public inputs | L9 `ledger/src/dust.rs:2153-2154` |
| `log` on an array value | 1,315,830 ps per byte, size counted as written and deleted (churn) | CFG:32-33; L9 `onchain-vm/src/vm.rs:556-604` |
| Time-to-dismiss | max(2 µs per byte, 15 ms) | CFG:153-154 |
| Contract proof | 4,368 B for every circuit used here | measured model, section 3 |
| Verifying key | 2,119 B | measured, section 3 |
| Transcript gas per call | simulator values of section 3 × 1.2 | measured in simulator |
| Block bytes other than proofs | about 700-900 B per transaction, 306 B per `Misc` | estimated |

The simulator gas already includes the state-update cost (compact-runtime 0.20.0 `circuit-context.js:204-214`; L9 `onchain-runtime/src/context.rs:946-964`) but charges it once per ledger-operation group, where the chain charges it once per transcript; the compute figures are therefore upper bounds by up to about 1.3 ms per extra group.

**Results at genesis prices** (fee / fee with wallet margin):

| Transaction | Block bytes | Compute | Read | Net written | Churn | Dominant term | Fee DUST |
|---|---|---|---|---|---|---|---|
| One registration (`register`) | about 8,670 | 26.2 ms | 8.7 ms | 560 B | 17,203 B | compute | 0.246 / 0.308 |
| One Anchor post (`postAnchor`) | about 10,340 | 38.2 ms | 9.2 ms | about 0 B (see note) | 17,522 B | compute | 0.195 / 0.244 |
| One 256-byte `Misc`, marginal inside a call | +306 | +1.33 ms | 0 | 0 | +832 B | | +0.0032 / +0.0040 (block dominant) to +0.0068 / +0.0085 (compute dominant) |
| One `Misc` alone (`publishClass0`) | | | | | | | 0.129 / 0.161 |
| Fallback, 16 parts in one call (`publishClass2`) | about 12,920 | 27.6 ms | 3.6 ms | 224 B | 26,931 B | compute | 0.188 / 0.236 |
| Fallback, 16 `publishPart` calls in one intent | about 80,260 | 64.0 ms | 15.0 ms | 224 B | 91,992 B | block | 0.866 / 1.084 |

Note on the Anchor row: the simulator reports more bytes deleted than written for `postAnchor` (the slot record replacement), so net written saturates at zero; each 100 B of real net growth adds 0.02 DUST.

Against the gates: one registration is about 8.7 KB and 0.25 DUST (0.31 with margin), inside P-ECO-13 (16 KiB and 0.5 DUST). An Anchor every 60 s costs about 280 DUST per day at genesis prices (1,440 × 0.195). Sixteen separate part calls cost 4.6 times one 16-part call; one call per Envelope is the cheaper shape for fees, and the more expensive one to prove (section 4, item 2). Live prices move each block by up to about 4.6% per dimension and never fall below `min_block_price` in ledger-9 configurations; mainnet still runs the ledger-8 parameter schema.

## 6. Implications for the requirement set and the MIP

Requirements to change:

- **MPE-ECO-004.** "A paid DUST fee" cannot be checked by a contract. Change to "a registration transaction" and state that the network fee is the only price unless a token price is added (see the new requirement below).
- **MPE-ECO-026.** Specify the membership set as one tree per membership period, removed by a permissionless prune one root window after the period ends; this is what the Registry can express.
- **MPE-ECO-027 and MPE-NET-055.** Publication and supersession times come from the timestamps of the blocks that include root-changing transactions, read by the Ledger Adapter; the Registry cannot record them (section 4, items 4 and 6).
- **MPE-ECO-028.** Specify the evidence check: two shares under one `(epoch, class, credit)` that lie on the member's line with distinct EIDs, plus the member's Merkle path; state that the leaf index and the identity commitment become public.
- **MPE-ECO-015 and P-ECO-5.** State that the root window is enforced by Bus Nodes, because the Registry's historic-root check has no time bound.
- **MPE-NET-050.** Fix the payload as window u64 BE, root, 8 × u32 BE counts, zero fill, so that its length does not depend on the Shard count.
- **MPE-NET-053 and MPE-NET-054.** "Submitter key" means a key commitment stored in the relay entry, proved in circuit; add the commitment field to the relay entry, and define the peer key as SHA-256 of the libp2p peer id.
- **MPE-STO-028 and MPE-STO-029.** Define the live Anchor store as 2,940 slots indexed by `window mod 2940`, so the bound holds by construction and pruning is permissionless.
- **MPE-FMT-042.** Replace "in the guaranteed phase" with "in one phase of one intent", as MIP-0019 allows: the 16-part call, registrations and Anchors exceed the guaranteed-segment budget and land in the fallible segment (section 4, item 16).
- **MPE-FMT-044 and P-FMT-8.** Keep 16 parts as the fee limit, and add the proving cost: one 16-part call is a k = 22 circuit. Consider lowering the in-contract limit to 4 parts (k = 20) unless a cheaper `Misc` encoding appears.
- **MPE-CON-046.** Add that the expiry comparison discloses only a coarse bound chosen by the prover, and that the check may use the anchored creation minute instead of the sealed expiry.
- **MPE-CON-047.** Specify the Anchor tree: leaf `SHA-256(domain, window, window root)` at slot `window mod 2940` in a `HistoricMerkleTree<12>`, read through a witness-free Registry circuit; state that a reaction then contains two contract calls.
- **DEC-022.** The inclusion-only path (option (b)) gives no authority and no binding between nullifier and Event (section 4, item 12). Keep option (a) as the production default and require the signature check whenever option (b) is used for authority.
- **MPE-OPS-044.** Confirmed by compilation: the Registry needs toolchain 0.33 or later only for `emit`; without Anchors and governance events it compiles with 0.31.1.
- **MPE-NET-040 and MPE-OPS-018.** The standard `Paused` and `Unpaused` events exist, but MPE-NET-040 allows only `Misc`; the Registry uses a `Misc` named `mpe/gov/v1`. Decide which applies and define the governance payload (action u8, reason u16, subject 32 B).
- **MPE-ECO-049, MPE-OPS-046 and MPE-VER-030.** Replace the 8,192-byte transaction assumption with the measured inputs of this experiment (4,368-byte proofs, 2,119-byte verifying keys, the simulator gas) until devnet measurements exist.

Requirements to add:

- **Registry toolchain.** The Registry shall compile with a Compact toolchain that supports `emit` and witness-free cross-contract reads (0.33 or later), and its MIP version shall name the toolchain and ledger versions.
- **Proving budget.** The MIP shall state the proving circuit size of each Registry and consumer circuit (k and rows) and a gate on Anchor proving time per window, since every Anchor needs a k = 18 proof.
- **Clock tolerance.** Every Registry write that depends on time shall take a caller clock value checked against the block time within a stated tolerance (900 s in this prototype).
- **Registration price instrument.** If a registration price beyond the network fee is wanted, the MIP shall name the token and the receive path (shielded NIGHT preferred, MPE-ECO-036 for unshielded).
- **Protocol hash for in-circuit RLN.** The admission relation shall use a hash that Midnight commits to keeping stable; `transientHash` carries no such guarantee.
- **Circuit encoding rule.** Protocol hashes that a circuit computes shall take struct preimages of fixed-width fields, never byte-level concatenation, and the MIP shall keep the number of non-constant bytes that a circuit emits as small as the protocol allows (Anchor payload 72 B of fields; governance payload 35 B).
- **Consumer authority.** A consumption circuit that uses Anchor inclusion shall also bind the nullifier to the Event through a publisher signature over a statement that contains the EID or LEI.

For the MIP's Specification, Ledger interface section: the contract shapes in section 2 are implementable today on ledger 9 with the listed costs, and nothing in the Midnight node needs to change. The two capability requests that would make the interface cheaper belong in the MIP's Rationale or a follow-up: a cheaper `Misc` emission path for public byte payloads (the dominant prover cost), and a way to read the block time or a contract's own Merkle root inside a circuit.

## 7. What remains unverified

- Nothing ran on a Midnight network, devnet or local node. No transaction was built, proved, balanced or submitted; no proof was generated or verified.
- Fees are derived from the cost model at genesis mainnet prices with estimated block bytes; live prices, real transaction sizes and the state-update charge of a single on-chain transcript are not measured.
- The guaranteed-segment placement in section 4, item 16, is derived from the measured gas and the partitioning code, not observed.
- The simulator test exercises the generated JavaScript, not the circuits: it does not prove that the ZKIR constraints accept the same executions, and it does not run the cross-contract call of `react`.
- `consume.compact` was compiled and its circuit measured, but not executed.
- Proving time and prover memory for the k = 18, 20 and 22 circuits were not measured.
- No keys were generated for the k = 22 circuit `publishClass2`; its model comes from `zkir mock-compile` alone (1,071 s, 2.5 GB of memory). Key generation at k = 22 would also download the 2^22 parameter file.
- Toolchain 0.35.0 and ledger 9.1 are release candidates of a ledger generation that mainnet does not run; the numbers can change before ledger 9 is deployed.
- The DEC-022 option (a) circuit (in-circuit Ed25519 or JubJub Schnorr signature) was not written or compiled.
