# UmbraDB recovery foundation and future release

**Recommend CharlesHoskinson/UmbraDB as the backend workflow recovery foundation.** It already models Midnight temporal state, content-addressed snapshots, transaction history and sync cursors. Extend it for Midnight Express in a future additive release; use SQLite for minimal standalone Rust nodes/clients. This is the [Midnight UmbraDB library](https://github.com/CharlesHoskinson/UmbraDB), not the unrelated TUM research database.

## Inspected baseline and evidence

Pulled `/home/hoskinson/Projects/UmbraDB`, commit `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca`, package **0.9.5**, Apache-2.0, Node >=24, PostgreSQL 17 tested. Three independent source studies: [architecture](../../reviews/competitive-event-systems/umbradb/architecture.md), [privacy](../../reviews/competitive-event-systems/umbradb/privacy.md), [product](../../reviews/competitive-event-systems/umbradb/product.md). Eight commit-pinned source snapshots were retrieved with Scrapling into the [catalog](../../catalog/event-systems/README.md).

Local `npm run build`, `npm run typecheck` and **38 API-surface tests across eight files passed**. Runtime-only npm audit reported zero findings; this is a dependency advisory check, not a security audit. The exact baseline [conformance CI run](https://github.com/CharlesHoskinson/UmbraDB/actions/runs/30213426351) succeeded. Its existing PostgreSQL crash tests were reviewed but **not rerun locally**: the current user cannot access the Docker socket. No MPE integration or workload benchmark ran.

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

The Rust sidecar still handles MPE transport, proof validation and local recognition. Each trusted Node workflow host uses UmbraDB/Postgres for its own application state. No public shared plaintext recovery service is implied. Backend endpoints can reuse Midnight-aware records for RFQ, invoice and bounded agent workflows; Rust-native/client deployment may retain SQLite rather than requiring Node/Postgres everywhere.

Network retention, replicated stores, signed persistence receipts, ledger finality and contract proof binding remain MPE work. A database or checkpoint does not implement them.

## Future release requirements

The [UmbraDB future-release draft PR](https://github.com/CharlesHoskinson/UmbraDB/pull/5) contains the audited requirements. The requested UmbraDB proposal is on branch `design/midnight-express-recovery`: [integration summary](https://github.com/CharlesHoskinson/UmbraDB/blob/design/midnight-express-recovery/docs/integrations/midnight-express-recovery.md) and [OpenSpec requirement set](https://github.com/CharlesHoskinson/UmbraDB/blob/design/midnight-express-recovery/openspec/changes/midnight-express-recovery/specs/mpe-recovery/spec.md). Exact release version/schedule is unset; the work coordinates with post-1.0/1.1 tracks without modifying current API/package behavior.

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

**Important current detail:** `runMigrations` intentionally swallows exceptions from `onDurabilityWarning`. Throwing inside that callback cannot reject `synchronous_commit=off`. A supported current adapter can capture warnings synchronously, await migrations, then fail before use; production enforcement also needs actual pooled-session/transaction policy. The future strict profile addresses that gap.

UmbraDB has no built-in at-rest encryption and assumes one trusted writer/domain. Encrypt secret-bearing bytes before the raw checkpoint store or use a reviewed cipher decorator; protect database metadata, WAL, backups and replicas as the threat model requires. Retaining obsolete session secrets in historical snapshots defeats erasure. Wrong-domain/key/corrupt/stale restore must fail explicitly; trusted freshness/anti-rollback evidence remains a design decision. Do not infer tenant isolation from schemas or secure erasure from expiry.

## Consumer acceptance

Before production adoption run MPE fixtures for RFQ local acceptance, invoice reconciliation and human-approved agent actions through duplicate, conflicting intent, mid-batch process death, unclean Postgres recovery, lease loss, unsafe durability, stale/expired state and wrong-key/domain restore. Test the complete state vector, not merely checkpoint round-trip. Keep contract settlement gated on MPE authority/replay/anchored-message proof and mobile delivery gated on private retrieval.

The recommendation is to **evolve UmbraDB into this role**, preserving its Midnight data model and public boundaries. It is not a claim that current 0.9.5 already satisfies all MPE recovery requirements.
