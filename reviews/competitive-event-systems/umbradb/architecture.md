# UmbraDB architecture adoption review

Reviewed local checkout `/home/hoskinson/Projects/UmbraDB`, commit `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca`. Read-only source review; no adapter execution or UmbraDB edits performed.

**PASS: a deliberately scoped, single-writer backend application/SDK recovery experiment. BLOCK: general production admission, multiple writer processes, writer fencing, arbitrary external SQL effects within the supported transaction API, or remote exactly-once claims.** UmbraDB supplies useful local recovery primitives; it is not an existing Midnight Express adapter or a distributed bus store.

## Supported boundary and runtime

UmbraDB is Apache-2.0, ESM, Node >=24, with PostgreSQL 17 the tested supported version. The actual package is **0.9.5**; comments describing a frozen 1.0 API do not establish a released SemVer compatibility guarantee. Pin the inspected commit/package artifact. Source: `package.json:3`, `package.json:5`, `package.json:9`, `package.json:31`; `README.md:42`, `README.md:45`, `README.md:49`.

Keep Rust/libp2p as the bus/client transport implementation. An optional trusted Node backend SDK worker can own this PostgreSQL recovery domain. Define an authenticated, versioned local IPC/application handoff if these are separate processes, and send only endpoint-authorized application data. The TypeScript package cannot simply become a Rust storage trait implementation. SQLite remains the standalone bus/client fallback; UmbraDB does not supply mesh retention, archive replication, private discovery, anonymous admission, or Midnight execution proofs.

## Atomic cursor, effects, dedup and outbox

`PgTransactionLeaseLayer.withTransaction` opens a real PostgreSQL transaction, registering a short-lived opaque handle that each primitive resolves to that same connection. The handle is unregistered when the callback exits. Source: `src/postgres/transaction-lease.ts:207`, `src/postgres/transaction-lease.ts:223`, `src/postgres/transaction-lease.ts:246`.

Public TemporalKV reads/writes, checkpoint `save`, and watermark reads/writes accept `{tx}`. Therefore a candidate `processOnce` can co-commit an inbox dedup record, a **TemporalKV application effect**, pending outbox records, recovery checkpoint and application cursor. `put(...,{expectedVersion:0n,tx})` is atomic create-only; an unconditional put is an upsert and is insufficient for dedup. A specific nonzero version supports compare-and-set. Source: `src/postgres/temporal-kv.ts:91`, `src/postgres/temporal-kv.ts:113`, `src/postgres/temporal-kv.ts:128`, `src/postgres/temporal-kv.ts:147`, `src/postgres/temporal-kv.ts:170`; `src/interfaces/checkpoint-store.ts:193`; `src/interfaces/watermarks.ts:63`.

**Important API limit:** the public package exports an opaque transaction handle, not its SQL connection. `resolveTransaction` lives in an internal module and is not re-exported by `src/index.ts`; the export map supports only the package root. A business mutation issued on the general `createClient` pool does not automatically join an Umbra transaction. The initial experiment must express effects through public TemporalKV primitives. Arbitrary ERP/application SQL tables require an explicitly supported transaction adapter extension or another transaction ownership design; do not bypass the root export contract with deep imports.

`saveAndAdvance` already co-commits checkpoint bytes and a cursor, but nothing else. It neither deduplicates MPE messages nor supplies an outbox. For the broader transaction, call the constituent APIs with one shared handle rather than nesting this helper. Source: `src/postgres/save-and-advance.ts:58`.

Persist protocol event identity and payload digest alongside the dedup record; distinguish business operation identity from envelope identity when republishing is allowed. Reject conflicting content for the same immutable identity. Outbox dispatch occurs after commit, with a stable destination idempotency key. A lost acknowledgement may cause redelivery; an idempotent destination or reconciliation is necessary. Atomic PostgreSQL state does not make an external effect exactly once.

## Checkpoint resume and cursor correctness

Checkpoint load verifies chunks before returning. Save joins the caller transaction, while load/history/prune use their own transactions. The adapter must take a coherent startup view under a quiescent single writer, validate application cursor/checkpoint compatibility, and resume according to the application's ordered stream profile. Watermarks are last-write-wins, not monotonic or compare-and-set: explicitly reject regression and mismatched network/stream/profile identities. Large integer positions require decimal strings; runtime schemas only validate generic JSON, not an MPE cursor shape. Source: `src/interfaces/checkpoint-store.ts:198`, `src/interfaces/checkpoint-store.ts:214`, `src/interfaces/watermarks.ts:38`, `src/interfaces/watermarks.ts:54`, `src/interfaces/watermarks.ts:68`.

If cryptographic ratchet/session state is persisted here, advance it only after complete message authentication, and atomically persist outgoing ciphertext/outbox state with its ratchet transition. This is an adapter obligation, not an Umbra cryptographic guarantee. Likewise, checkpoint chunk deduplication is unrelated to application message deduplication.

## Writer fencing and durability gates

The writer lease is a session advisory lock, not a fencing token. Its connection can die while application work continues on a different pool connection. Two writer processes are explicitly unsupported. Use one externally enforced writer process with no automatic overlapping takeover; do not infer HA safety from `withLease`. Source: `docs/CONTRACT.md:101`.

Run migrations/startup durability checks against a direct PostgreSQL primary or a configured session pool, never transaction pooling. `fsync` and normally `full_page_writes` are enforced, but `synchronous_commit=off` merely warns and can lose acknowledged commits. Any adapter emitting a recoverable-persistence acknowledgement must enforce durable commit settings itself. These settings establish local-primary durability, not replication failover guarantees. Source: `docs/durability-contract.md:20`, `docs/durability-contract.md:47`, `docs/durability-contract.md:72`.

UmbraDB has no built-in at-rest encryption. Its global checkpoint chunk pool has a cross-wallet deduplication side channel and is one trust domain. A schema is not a security boundary. Use separate stores for mutually distrusting principals and an explicit encryption/key/backup policy for confidential application or ratchet material. Source: `docs/CONTRACT.md:135`; `src/interfaces/checkpoint-store.ts:182`.

## Minimum concrete adapter experiment

Use actual PostgreSQL 17 and Node 24 with only package-root imports. Serialize one writer. Implement a versioned JSON application cursor plus TemporalKV inbox/effect/outbox namespaces, and optional opaque checkpoint bytes. Tests should establish:

1. One shared transaction applies one effect, one dedup record, a pending outbox entry and its cursor; an injected failure between any writes rolls all of them back.
2. A duplicate replay does not repeat the effect or regress the cursor; identity/content mismatch is rejected. Exercise create-only `expectedVersion:0n` and conflicting-version paths.
3. Reopening a fresh adapter after commit resumes from consistent state. Before-commit interruption leaves no advanced cursor. A subprocess kill distinguishes actual recovery from an ordinary thrown exception.
4. Commit followed by failure before dispatch leaves a recoverable outbox record. Dispatch success followed by acknowledgement loss redelivers with the same destination idempotency key.
5. Unsupported stale transaction handles fail; watermark shape/profile and integer encodings are validated by the adapter. Misconfigured non-durable acknowledgements are refused.

This test scope supports a **backend recovery prototype**, not full MPE requirement compliance. Separate future gates cover arbitrary SQL effect composition, fencing/failover, security/key retention, remote idempotency and transport acknowledgement/retention semantics.
