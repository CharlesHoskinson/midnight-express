# Chain data science review

Reviewed 2026-10-03 from the perspective of reproducible blockchain datasets and application event analytics. Scope: the unified model, both chain application requirements, `model/domains/README.md`, the actual catalog, metadata schema/tests, and retained Ethereum/Solana primary-source archives. This review does not infer deployed functionality from proposed vocabulary.

## Assessment

The design has the right boundaries: source reports, decoding, local inference, requested actions, execution outcome and finality are separate; neither an authenticated MPE sender nor a familiar event name proves chain truth or grants permission. The documents already describe most important hazards, including native integer precision, fork location, duplicate deliveries, failed Solana execution, durable nonces, changing decoders and uncertain submissions. These are unusually valuable requirements for an analytics interface.

The catalog is a broad discovery inventory, not yet a complete event dataset specification. Its 20 families per chain conceal uneven lifecycle coverage. The next investment should be two small, complete, read-only transfer datasets with deterministic replay, rather than more protocol event names. The lack of chain payload schemas is expressly deferred and is **not an implementation defect** in this proposed catalog. The recommendations below distinguish vocabulary corrections from runtime adoption gates.

## Audit of all 267 records

Counts were computed from `chain-event-catalog.json` with Python `collections.Counter`, rather than copied from the prose. Exact IDs and `(chain,family,semanticName)` keys have no duplicates. All 40 chain/family combinations are populated; every record is proposed and declares `effectAuthority:false`.

| Dimension | Ethereum | Solana | Total |
| --- | ---: | ---: | ---: |
| Entries | 127 | 140 | 267 |
| Native | 32 | 35 | 67 |
| Decoded | 41 | 53 | 94 |
| Derived | 14 | 13 | 27 |
| Intent | 40 | 39 | 79 |

Across both chains, message kinds are 182 observations, 62 application intents, 13 RPC requests, six RPC responses and four subscription controls. Thus 79 request/control records coexist with 188 observation/response records; row count is not a count of economic events or distinct supported RPC methods.

| Family | Ethereum | Solana |
| --- | ---: | ---: |
| blocks | 3 | 4 |
| finality | 2 | 3 |
| rollback | 3 | 2 |
| transactions | 9 | 12 |
| simulation | 5 | 6 |
| state | 5 | 6 |
| logs-instructions-cpi | 3 | 8 |
| token-nft | 12 | 20 |
| approvals-permissions | 12 | 9 |
| staking | 6 | 7 |
| governance | 8 | 7 |
| defi | 23 | 26 |
| oracle | 3 | 3 |
| bridge | 4 | 4 |
| account-abstraction-wallet | 10 | 4 |
| rpc | 4 | 4 |
| subscriptions | 7 | 7 |
| errors | 3 | 3 |
| gaps | 2 | 2 |
| backfill | 3 | 3 |

`/tmp/mpe-data-model-validation-env/bin/python model/domains/test_catalog.py` passes all 12 tests. That establishes closed catalog metadata, namespace consistency and coarse classification constraints. It does not establish coverage completeness, semantic independence, decoder correctness or finality. An in-memory experiment changing `mpe.ethereum.transactions.dropped-claim.v1` to `evidenceKind:native, scope:chain` still passes `validate_catalog` with 267 entries. The test named `test_derived_claim_is_not_native` only changes scope while retaining `derived`; it does not prevent this two-field promotion. This is a narrow metadata-test weakness, not evidence that a runtime accepts fabricated chain facts.

## Findings and recommendations

Effort estimates are relative: S is roughly 1–3 engineering days, M roughly 1–2 weeks, L a multiweek cross-adapter effort. P0 means required before admitting the affected runtime slice; P1 means the next catalog/design iteration; P2 means later expansion. Estimates include focused fixtures but exclude production infrastructure.

### 1. Preserve physical facts, logical operations and deliveries separately

**Priority P0; effort M; runtime adoption gate.** The documents already distinguish occurrence, workflow, source object, business action and envelope identity. Turn that requirement into executable identity examples before introducing chain profiles.

`mpe.ethereum.logs-instructions-cpi.raw-log-observed.v1`, `mpe.ethereum.token-nft.erc20-transfer.v1` and `mpe.ethereum.rollback.log-removed.v1` describe related evidence, not three independent transfers. Use a physical log key containing approved network identity, block hash, transaction hash and log index. Retain transaction index for order; track observer occurrence IDs and adapter/decoder attestations independently. Re-inclusion in another block is a new physical inclusion. A cross-inclusion logical operation link requires explicit evidence/policy, since different execution state can change logs or their indices. Do not globally deduplicate by transaction hash and log index across forks.

For `mpe.solana.logs-instructions-cpi.inner-instructions-observed.v1`, `mpe.solana.logs-instructions-cpi.cpi-invocation-decoded.v1` and `mpe.solana.token-nft.spl-transfer.v1`, keep approved genesis, branch/blockhash where established, signature, outer instruction index and inner invocation order/path. Signature alone collapses multiple transfers. Stack height alone is not a unique path; missing trace information must remain missing. Account notifications need their own state-revision/evidence identity: address plus context slot is not a proven causal transaction or necessarily a unique within-slot update.

**Acceptance:** fixtures replay one transfer from polling, subscription and backfill without inflating aggregates; preserve two identical CPI transfers in one transaction; preserve fork re-inclusions as distinct inclusions; and preserve a changed decoder interpretation without inventing another economic effect. No causal signature is assigned to an account update without supporting evidence.

### 2. Make finality and rollback an append-only dependency graph

**Priority P0; effort L; runtime adoption gate.** `mpe.ethereum.finality.safe-head-observed.v1`, `mpe.ethereum.finality.finalized-head-observed.v1`, `mpe.solana.finality.confirmed-observed.v1` and `mpe.solana.finality.finalized-observed.v1` correctly retain native labels. They need target-specific relationships rather than an object-level status overwritten by the last provider report. A root/head report must establish ancestry for the target inclusion; a numerically later root does not alone establish membership.

Record observation dependencies for `mpe.ethereum.rollback.observation-invalidated.v1` and `mpe.solana.rollback.observation-invalidated.v1`: exact prior inclusion/revision, invalidating evidence, verifier/policy commitment, affected derived facts and replacement evidence when known. Keep provider correction distinct from verified branch invalidation and contradictory finalized reports distinct from ordinary provisional rollback. Store immutable claims and rebuildable projections; do not delete history or silently reverse an external action.

**Acceptance:** replaying a fork swap retracts precisely the affected token/protocol aggregates and candidate actions while preserving their audit records. A removed notification arriving before the original log is remembered and applied when that log arrives. A provider disagreement never becomes settled merely through last-write-wins. Missing/pruned history, a skipped slot and a dead branch produce distinct unresolved states. Existing irreversible effects yield explicit reconciliation work.

Primary archived support: [Geth subscription behavior](../../catalog/data-model/ethereum/pubsub.txt), [Solana slot lifecycle](../../catalog/data-model/solana/slotsupdatessubscribe.txt) and [root notifications](../../catalog/data-model/solana/rootsubscribe.txt).

### 3. Specify temporal analytics and coverage truth

**Priority P0; effort M; runtime adoption gate.** The common occurrence time and chain timestamps are insufficient for reproducible historical analytics without an explicit query model. Keep source block time (possibly null), source notification time, observer receive time, normalization time and correction/finality-observation time separate. Also preserve chain order, since timestamps need not uniquely order events. Do not synthesize Solana block time or treat slot as block height.

`mpe.ethereum.backfill.backfill-completed-claim.v1`, `mpe.solana.backfill.backfill-completed-claim.v1` and both `gaps.coverage-gap-claim` entries should certify only a precisely stated network, branch/range, filter, endpoint capability/retention, commitment, page boundaries and omissions. Quiet subscriptions cannot prove a zero count. Completeness for one address/filter does not establish complete protocol volume.

Offer two explicit analytical views: canonical facts under a named evidence policy, and facts known to the observer at an observation-time cutoff. Version decimals, proxy/program identity, oracle revisions and adapters at the evidence location; replay must not use today's metadata to reinterpret yesterday's raw units. Preserve dependency IDs, source digests, transformation/loss flags and derivation commitments so features can be rebuilt without look-ahead leakage.

**Acceptance:** late backfill changes present canonical totals without changing an immutable historical “known as of” query; a reorg corrects branch-dependent features; stale/contradictory oracle data remains attributed; and volume reports label unresolved coverage rather than substituting zero. Each aggregate can enumerate its contributing physical facts and derivations.

### 4. Resolve catalog overlap and classification inconsistencies

**Priority P1; effort S; vocabulary correction.** Most classifications are defensible: removed Ethereum logs and dead-slot reports are native provider surfaces; branch replacement, expiry, dropping and coverage completion are local derived claims. Program/ABI interpretations are decoded. Generic action proposals are correctly intent/local rather than universal APIs.

Several entries need sharper relationships:

- `mpe.ethereum.blocks.block-observed.v1` and `mpe.ethereum.blocks.header-observed.v1` are separate projections of block retrieval; their cited Geth pubsub page directly supports `head-observed`, while block retrieval should point to the archived JSON-RPC/execution API material. Explicitly distinguish header projection from block transaction pages.
- `mpe.solana.state.account-observed.v1` and `mpe.solana.transactions.nonce-account-observed.v1` both cite `getAccountInfo`, but the nonce interpretation is typed account-state decoding. Clarify whether the latter is raw native account evidence or decoded nonce state. Conversely `mpe.solana.staking.stake-rewards-observed.v1` is `decoded` for the direct RPC `getInflationReward`, while Ethereum's `staking.rewards-observed` is native. Classify by actual transformation, not by family name.
- `mpe.solana.token-nft.token2022-transfer-fee-observed.v1` cites `TransferFeeConfig`: that is configuration observation, not evidence of a fee actually withheld by a transfer. Likewise hook configuration does not establish hook invocation. Clarify names/qualifications before economic analytics reuse.
- Both chains have `subscriptions.subscription-gap-claim` and `gaps.coverage-gap-claim`; define the former as session delivery discontinuity and the latter as bounded dataset coverage uncertainty, with links between them. Transport disconnect being locally derived is reasonable, but should not be treated as evidence about chain execution.

**Acceptance:** a source-to-vocabulary mapping table names raw fact, decoded interpretation, projection and logical-operation links; one input can produce several linked records without being counted several times. Native reward RPC, nonce-state decoding and Token-2022 configuration/effect boundaries have explicit, consistent classifications. Update the targeted negative test to reject semantic promotion of pinned local-claim IDs, or state accurately that it only enforces conditional metadata consistency; do not imply all native truth is machine-verified.

### 5. Close common lifecycle gaps before expanding the protocol list

**Priority P1; effort M; vocabulary coverage correction.** Family coverage is a weak proxy for application completeness. The following are absent as dedicated entries, although generic RPC envelopes or raw evidence can preserve their traffic and the prose already anticipates many of them:

- `mpe.ethereum.account-abstraction-wallet.sign-intent.v1` and all four Solana wallet rows are intents. Neither chain inventory has dedicated signed-byte/signature results, wallet rejection/cancel outcomes or an explicit unresolved broadcast outcome. Generic transport/RPC errors are not a complete wallet lifecycle. Solana also lacks wallet account/session/feature observations, unlike Ethereum's four EIP-1193 observations.
- `mpe.solana.token-nft.spl-transfer.v1` names only `TransferChecked`. Specify coverage or separate variants for unchecked Transfer and relevant checked mint/burn/approval forms. Native System transfer decoding, ATA creation, wrapped-SOL sync/close effects and native account lifecycle are documented but have no dedicated rows. Ethereum has native `transfer-intent` but no named native ETH movement observation; internal ETH movements need the separately deferred trace profile, never inferred from token logs.
- Ethereum mint/burn intents lack corresponding policy-qualified ERC mint/burn derivations. Zero-address conventions require implementation-specific interpretation; do not promote them to a universal consensus event. NFT marketplace/list/cancel/buy and compressed Solana assets are application inventory gaps, not interchangeable with metadata snapshots.
- `mpe.ethereum.bridge.wormhole-message-observed.v1` and its Solana counterpart cover source messages; VAA observations plus `destination-redeem-intent` still leave destination execution, failure/retry and refund observations unnamed. Do not claim a complete bridge workflow from these four rows per chain.
- `mpe.solana.defi.orca-swap.v1` and `mpe.ethereum.defi.uniswap-swap.v1` coexist with generic swap intents but no quote/route acceptance lifecycle. Orca position close/reward collection are missing dedicated candidates. Many Solana governance/NFT rows are account-state snapshots rather than event-complete histories. Label each protocol's selected projection honestly.

**Acceptance:** publish a bounded support matrix with “typed candidate,” “preserved only through raw/generic envelope,” and “out of scope” per method/operation/version. Every admitted write/sign flow has request, result, failure, cancellation and uncertainty variants with exact distinctions. Each omitted workflow is visibly partial. Count workflow coverage separately from vocabulary rows; avoid duplicating raw transfer records with inferred mint/burn facts in volume measures.

Archive basis: [SPL account and wrapped-SOL semantics](../../catalog/data-model/solana/tokens.txt), [ATA semantics](../../catalog/data-model/solana/associated-token.txt), [wallet signer interfaces](../../catalog/data-model/solana/wallet-signers.txt), [bridge source/verification interfaces](../../catalog/data-model/solana/wormhole-core-solana.txt) and [Uniswap pool events](../../catalog/data-model/ethereum/uniswap-v3-events.txt).

### 6. Bind economic interpretation to execution, units and deployment

**Priority P0; effort M; runtime adoption gate.** `mpe.solana.defi.drift-order-filled.v1` cites an instruction (`fill_perp_order`), not independently demonstrated fill economics; `mpe.solana.defi.kamino-supply.v1` similarly cites a deposit instruction. Attempt decoding, successful operation and protocol-specific economic result need separate claims. Failed transactions can contain logs/inner instruction evidence without successful transfers. Account snapshots such as `mpe.solana.governance.vote-record-observed.v1` cannot be backdated into a causal vote event from a latest-state read alone.

Amounts must preserve raw units and field-specific bounds. Do not use symbol/decimals as asset identity or assume ERC-20 decimals exist. Uniswap signed amounts, Pyth exponents/confidence, signed rewards and fees require distinct primitives. Unknown confidential quantity is not zero. A transfer fee configuration does not equal actual withheld fees; gross debit, net credit and fee require supported execution evidence. A successful Ethereum receipt is also insufficient to prove a reviewed application-level outcome.

**Acceptance:** failed Solana execution yields zero committed ordinary token-transfer effects while retaining diagnostic evidence and the correct fee/nonce effects; config observations do not masquerade as transfers; and unsupported decoder, program deployment, proxy revision, token extension or quantity cannot enter an economic aggregate through guessed values. Every derived price/amount declares its raw inputs and rounding policy.

Primary archive support: [transaction structures](../../catalog/data-model/solana/rpc-structures.txt), [durable nonce failure behavior](../../catalog/data-model/solana/nonce-runtime.txt), [ERC-20 zero-transfer requirements](../../catalog/data-model/ethereum/erc20.txt) and [Solidity ABI source](../../catalog/data-model/ethereum/abi-source.txt).

### 7. Implement two minimal complete vertical slices

**Priority P0; effort L; sequencing recommendation.** Start with observations and replay; keep signing/broadcast actions outside the first slices.

**Ethereum slice:** one approved network and deployed ERC-20, pinned decoder, raw logs → decoded Transfer → inclusion/receipt execution → ancestry/finality report → invalidation/reconciliation → bounded backfill → exact base-unit aggregate. Include zero transfer, failed receipt and re-inclusion. Resolve metadata at the observed block. Limit the admitted range/result size; disclose projection loss.

**Solana slice:** one approved genesis and Token Program deployment/version, transaction bytes/meta → outer/CPI instruction decoding → repeated TransferChecked operations → execution gating → signature status/branch commitment → invalidation → bounded reconciliation → exact raw token aggregate. Add unchecked Transfer only under an explicit mint/decimals-evidence rule. Initially refuse Token-2022 extensions rather than accidentally assign base-token economics. Keep unknown history distinct from transaction failure.

**Acceptance:** for each slice, two independently specified adapters and Rust/TypeScript interpretation produce identical fact identities, raw quantities, evidence links and canonical totals, or both refuse unsupported input. Snapshot restore plus replay produces byte-identical normalized facts and the same projections. Feed order and duplicate deliveries do not alter final results. Every gap/uncertain branch is visible. Promotion requires closed payload contracts and committed fixtures, not merely a larger catalog.

### 8. Build an adversarial corpus with analytical oracles

**Priority P0; effort M initially, then ongoing; conformance work.** Fixture success must mean more than “schema validated.” Each sequence should assert admitted facts, evidence strength, unresolved outcomes, aggregate deltas, invalidation targets and audit lineage. Include:

| Corpus sequence | Required analytical result |
| --- | --- |
| Duplicate live/poll/backfill, shuffled pages, reconnect and filter change | Stable physical counts; explicit scoped coverage; no false complete claim |
| Ethereum same-height competing heads; removal before addition; re-inclusion with changed logs | Correct branch-specific identities and aggregate retractions |
| Same sender/nonce competitors; pending timeout/null receipt; submit timeout | Unresolved/policy-qualified replacement; no global dropped or cancelled assertion |
| Solana repeated CPI transfers; missing inner trace; diagnostic event before later failure | Distinct attempts, bounded decoding confidence, no successful ordinary transfer on failure |
| Durable nonce accepted then execution fails; validation rejected | Respect retained nonce/fees in the first case and distinguish validation failure; no recent-blockhash expiry rule applied |
| Recent-blockhash expiry with skipped slots, stale RPC and status-cache null | Use block height/chain policy and history evidence; never a universal slot/time timer |
| Conflicting finalized providers; root without target ancestry; pruned history | Halt/reconcile evidence conflict; do not infer target finality or absence |
| uint256/u64 maxima, zero, overflow, JS unsafe integers, signed deltas, null/absent/empty | Exact cross-language values or deterministic rejection, no silent rounding/coercion |
| ERC-20/ERC-721 topic collision; anonymous/indexed-dynamic ABI; proxy/program upgrades | Version/deployment-aware decode or opaque evidence, no guessed semantic promotion |
| Wrong genesis; address-table resolution failure; unknown transaction version/extension | Explicit refusal of unsupported actionable/economic interpretation |
| Token fee/hook config versus actual execution; wrapped SOL; confidential amount | Separate config/effect and gross/net/fee; unknown quantity retained |
| Bridge source message and valid attestation without destination execution | Pending cross-chain relation, never destination settlement |
| Late correction, mutable decimals, revised decoder, oracle time/exponent changes | Rebuildable versioned analytics; historical “known as of” view avoids future information |
| Wallet returns changed bytes; chain/account switch; user rejection | Separate lifecycle outcome and invalidated proposal; no inherited capability |

**Acceptance:** freeze input digests, adapter/decoder/policy commitments and expected fact/projection outputs for both adapters/languages. At least one fixture per row must demonstrate the rejected or unresolved alternative as well as the valid path. Use property-based reorder/duplicate/replay tests around these independent oracle fixtures; metadata tests remain a separate suite.

## Limits of the review

Research archives are dated source captures, not deployed contract/program attestations. The retained Solidity 429 and initial Wormhole 404 are not normative evidence; moving repository branches need reviewed release/commit pins before implementation. No live RPC, cryptographic verifier, signing flow, chain payload validator or production analytics pipeline was exercised. Counts and metadata-test outcomes above are observed locally; runtime gates are proposed acceptance criteria, not claims that the explicitly deferred runtime already fails them.
