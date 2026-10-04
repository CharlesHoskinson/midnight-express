# UmbraDB recovery foundation and future release

Use [CharlesHoskinson/UmbraDB](https://github.com/CharlesHoskinson/UmbraDB) to hold backend workflow progress. Its Midnight temporal state, content-addressed snapshots, transaction history and sync cursors provide the foundation for recovery after a host failure. A bounded MPE sandbox now demonstrates local transaction composition; complete recovery support still requires the additive release described below. Minimal standalone Rust nodes and clients can use SQLite. This assessment concerns the Midnight library, not the unrelated TUM research database.

## Original source assessment and later sandbox

The original assessment inspected `/home/hoskinson/Projects/UmbraDB` at commit `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca`, package **0.9.5**, Apache-2.0, Node >=24, with PostgreSQL 17 tested. Source studies cover [architecture](../../reviews/competitive-event-systems/umbradb/architecture.md), [privacy](../../reviews/competitive-event-systems/umbradb/privacy.md), [product](../../reviews/competitive-event-systems/umbradb/product.md). Commit-pinned source snapshots are retained in the [catalog](../../catalog/event-systems/README.md).

Local `npm run build`, `npm run typecheck` and API-surface tests passed at that baseline. Runtime-only npm audit reported zero findings; that was a dependency advisory check, not a security audit. The pinned [conformance CI run](https://github.com/CharlesHoskinson/UmbraDB/actions/runs/30213426351) succeeded. PostgreSQL crash tests were reviewed during the original assessment but were not rerun locally because Docker socket access was unavailable. It ran no MPE integration or workload benchmark.

The later [MPE sandbox](data-format-implementation.md) uses Umbra commit `f662822765247f0da553347c9819f958a1992d28` with PostgreSQL 17.11. It demonstrates atomic report-row processing and recovery after actual worker termination, including reconciliation with an acknowledgement fixture. Source and authority remain trusted fixtures; the result does not establish financial execution, production authorization or complete recovery support.

## What fits now

| Umbra primitive | MPE responsibility | Current boundary |
|---|---|---|
| TemporalKV with create-only/CAS | Workflow state, local action dedup and staged outbox | Only Umbra-backed local effects participate via supported handles; business authorization remains MPE/application-owned |
| CheckpointStore | Recoverable state snapshots | Byte integrity is not trusted provenance/freshness; plaintext by default, global dedup within one trust domain |
| Watermarks | Shard/window/source progress | Last-write-wins; caller enforces monotonicity, finality and gap semantics |
| `saveAndAdvance` | Checkpoint plus cursor atomicity | Correct public signature is `(deps, walletId, networkId, data, cursor, opts)`; not a local-effect/dedup/outbox helper |
| Transaction/Lease | Shared atomic composition and cooperative writer coordination | Lease connection and normal transaction connection are separate; no stale-writer fencing/HA claim |
| TransactionHistory/wallet envelope | Midnight wallet status/history | Not a generic event decoder, authority verifier or MPE store protocol |

For a bounded current prototype, compose `PgTemporalKV`, checkpoint `save` and watermark `set` under **one** public `withTransaction` handle. `expectedVersion: 0n` can create a dedup record once. Do not call `saveAndAdvance` inside that transaction: it opens its own transaction. Do not deep-import the private SQL resolver. Any remote effect requires a stable destination idempotency key and reconciliation.

## Integration placement

The proposed Rust sidecar handles MPE transport, proof validation and local recognition. Each trusted Node workflow host uses UmbraDB/Postgres for its own application state within its trust domain. Backend endpoints can reuse Midnight-aware records for RFQ, invoice and bounded agent workflows; Rust-native/client deployment may retain SQLite rather than requiring Node/Postgres everywhere.

MPE must separately implement network retention, replicated stores, signed persistence receipts, ledger finality and contract proof binding. Local recovery depends on those services when it needs missing messages or authoritative chain evidence.

## Future release requirements

The [UmbraDB future-release draft PR](https://github.com/CharlesHoskinson/UmbraDB/pull/5) contains the reviewed requirements. The proposal is on branch `design/midnight-express-recovery`: [integration summary](https://github.com/CharlesHoskinson/UmbraDB/blob/design/midnight-express-recovery/docs/integrations/midnight-express-recovery.md) and [OpenSpec requirement set](https://github.com/CharlesHoskinson/UmbraDB/blob/design/midnight-express-recovery/openspec/changes/midnight-express-recovery/specs/mpe-recovery/spec.md). Exact release version/schedule is unset; the work coordinates with post-1.0/1.1 tracks without modifying current API/package behavior.

The fourteen proposed requirements cover:

1. Atomic local effect, dedup, outbox, optional checkpoint and cursor commitment.
2. Matching duplicate replay returning the prior local result.
3. Conflicting action IDs rejected without progress.
4. Strict local WAL-flushing commit policy on actual transaction connections and reconnect.
5. Writer ownership bound to protected transaction commits.
6. Authenticated domain/profile/checkpoint/cursor restore with trusted freshness evidence.
7. Protected secret state and endpoint key custody.
8. Ratchet erasure/history compatibility.
9. Typed missing-history/key/freshness recovery gaps.
10. Live-manifest GC and full replay-horizon dedup retention.
11. Stable outbox idempotency/uncertain completion and expired-dispatch refusal.
12. Preservation of caller-verified source identity/finality.
13. No automatic recognition/processing acknowledgement in the strongest profile.
14. Supported APIs/errors and required non-skipping recovery tests.

`runMigrations` intentionally swallows exceptions from `onDurabilityWarning` in the inspected API. Throwing inside that callback cannot reject `synchronous_commit=off`. A supported current adapter can capture warnings synchronously, await migrations, then fail before use; production enforcement also needs actual pooled-session/transaction policy. The future strict profile addresses that gap.

UmbraDB has no built-in at-rest encryption and assumes one trusted writer/domain. Encrypt secret-bearing bytes before the raw checkpoint store or use a reviewed cipher decorator; protect database metadata, WAL, backups and replicas as the threat model requires. Retaining obsolete session secrets in historical snapshots defeats erasure. Wrong-domain/key/corrupt/stale restore must fail explicitly; trusted freshness/anti-rollback evidence remains a design decision. Do not infer tenant isolation from schemas or secure erasure from expiry.

## Consumer acceptance

Before production adoption run MPE fixtures for RFQ local acceptance, invoice reconciliation and human-approved agent actions through duplicate, conflicting intent, mid-batch process death, unclean Postgres recovery, lease loss, unsafe durability, stale/expired state and wrong-key/domain restore. Test the complete state vector, not merely checkpoint round-trip. Keep contract settlement gated on MPE authority/replay/anchored-message proof and mobile delivery gated on private retrieval.

Adoption depends on those recovery and authority checks. Preserve UmbraDB’s Midnight data model and public API boundaries while completing the proposed support; the inspected 0.9.5 release alone does not satisfy all MPE recovery requirements.
