# UmbraDB: product and integration review

Reviewed checkout: `/home/hoskinson/Projects/UmbraDB`, commit `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca`. Read `AGENTS.md`; no repository edits, dependency installation, or test executions performed. Findings concern source and recorded evidence, not a newly qualified deployment.

**PASS, conditional adoption recommendation:** replace the generic SQLite recommendation for the **trusted backend workflow recovery tier** with a pinned UmbraDB/PostgreSQL integration experiment. Retain SQLite for the minimal bus/client tier. **BLOCK production cutover and any assertion of completed Midnight Express integration** until the checks below pass. No finding establishes a defect requiring UmbraDB code changes before this scoped experiment.

## What is actually available

The package is Apache-2.0, version **0.9.5**, ESM-only, root-export-only, and requires Node **24+** (`package.json:2`, `package.json:5`, `package.json:9`, `package.json:31`). PostgreSQL **17** is the documented tested platform; 15/16 are not equivalently validated. It is a TypeScript library over postgres.js owning a PostgreSQL schema, not an embedded SQL engine or Rust storage crate (`README.md:8`, `README.md:45`). It is not yet published to npm and has no 0.x compatibility guarantee (`README.md:14`, `README.md:49`). Pinning the reviewed commit/packaged artifact avoids treating a mutable branch as a supported release.

The public surface provides temporal KV/CAS, checkpoint snapshots with deduplicated chunks, watermarks, transaction/lease operations, wallet transaction history, wallet-state envelopes, and `saveAndAdvance` (`src/index.ts`, `README.md:67`). The last operation opens one transaction and passes its handle to checkpoint save and watermark set (`src/postgres/save-and-advance.ts:58`). This prevents the sync cursor committing ahead of its snapshot. It does **not** automatically commit a business effect, message-dedup record, or external ERP/payment/agent operation.

The documented 1.0 release is **not released, blocked** on the complete self-operated Midnight wallet-sync stack and final release gates (`docs/releases/v1.0.0.md:3`). That scope is distinct from this backend workflow experiment; requiring a 1.0 tag for every reversible pilot would overstate the dependency. Likewise, documents describing the frozen future 1.0 surface do not override the current 0.9.5 compatibility disclaimer.

## Fit and boundaries

Use one authoritative trusted writer process per supported database deployment. The session advisory lease is not a fencing token and the contract explicitly prohibits two writer processes (`docs/CONTRACT.md:101`). A scalable, failover-capable multiwriter service cannot be inferred from PostgreSQL's capabilities or from the lease API. The library supplies recovery primitives, not a tenant API, an authorization service, chain finality, or a managed database.

UmbraDB provides **no at-rest encryption or built-in encryption hook**; encrypt the substrate, backups and replicas. A schema is not a security boundary and global content dedup operates within one trust domain (`SECURITY.md:3`, `SECURITY.md:107`, `docs/CONTRACT.md:137`). Untrusted agents/participants must not receive database credentials. Persisting old business records or crypto state also requires an explicit retention policy; temporal history must not inadvertently retain secrets intended for deletion.

Durability requires `fsync=on`, `full_page_writes=on`, an acknowledged durable commit mode, and direct/session-mode connections rather than transaction pooling (`docs/CONTRACT.md:20`). Startup rejects some violations but **only warns** for `synchronous_commit=off` (`docs/CONTRACT.md:30`). The MPE backend should promote that warning to an admission failure for its durable receipt/recovery profile; start the experiment with `synchronous_commit=on`. Receipt timing must follow the actual transaction commit. Forward-only migrations require a tested consistent backup/restore plan (`docs/CONTRACT.md:39`, `docs/CONTRACT.md:114`).

The recommended main bus implementation does not already establish a Node runtime. Evaluate either an explicit Node workflow service consuming the bus SDK or an independently specified process boundary. Do not call UmbraDB a drop-in replacement for Rust-local SQLite. Keep business state in a separately owned namespace/schema and use documented root exports; wallet transaction-history APIs are not automatically an invoice ledger.

## Three commercial pilot checks

| Pilot | Benefit to evaluate | Required adapter behavior and meaningful check |
|---|---|---|
| Private RFQ coordination | Less manual reconstruction after interruption; one recoverable quote/approval state | Persist RFQ state, expiry, message ID dedup, durable cursor and queued outbound acknowledgement atomically. Kill before and after commit, redeliver the quote and restore: no lost acknowledged transition, no duplicate accepted quote, no expired quote accepted. Trade/settlement authorization remains separate. |
| Invoice and payment approval | Recoverable matching/approval history and fewer duplicate reconciliation tasks | Model invoice identity and approval version explicitly with CAS/dedup. Commit state, cursor and payment/ERP outbox intention together; recheck uncertain commit outcomes. Simulate ERP success followed by lost reply: stable external idempotency identity yields one effective business operation. UmbraDB alone cannot prove exactly-once external payment. |
| Bounded agent coordination | Recover human approval, budget and execution status without authorizing duplicate actions | Persist signed policy/proposal identity, authorized state transition and outbox intention together. Crash at each authorization/dispatch boundary; after replay the action executes only with current approval and budget, with external idempotency or reconciliation. Writer leases coordinate storage; they do not grant agent authority. |

Business evaluation metrics should be observed rather than claimed targets: operator minutes spent reconstructing workflows, acknowledged transitions recovered, duplicate effective external operations, measured restore time and replay volume, integration/operations effort. Demand and throughput remain unvalidated.

## Validation evidence and adoption gates

The release record describes pack/install validation, 25 enforced required test IDs, process and PostgreSQL crash injection, negative controls, soak/load-under-prune, and differential fault-schedule versus fault-free **in-repo** replay (`docs/releases/v0.9.5.md:41`, `docs/releases/v0.9.5.md:60`). The direct checkpoint/cursor test kills the actual combinator between its two writes and includes an un-killed control (`test/integration/crash/saveandadvance-cotx.crash.test.ts:128`). This is useful primitive-level evidence, not an MPE workflow cutover test.

Recorded live Preprod validation was **2 passed** at RC `8a684fca261ef0581a1b7b5e4c4ac6517c779561`; its cold start rebuilds a fresh object graph, not a host reboot (`docs/recovery/EVIDENCE.md:17`, `docs/recovery/EVIDENCE.md:65`). The record says subsequent 0.9.5 recutting retained code, but it is not fresh execution evidence for our reviewed SHA. Release-record tag/date placeholders and missing fresh CI links must not be presented as new exact-commit qualification (`docs/releases/v0.9.5.md:25`). Abstract Lean proofs do not mechanize the SQL/TypeScript refinement; GC liveness is not proved, and numeric performance is not a release gate (`README.md:252`, `README.md:279`, `README.md:301`).

Before production cutover: (1) package/root-import smoke and required conformance checks at the pinned artifact; (2) the three workflow crash/duplicate/uncertain-commit scenarios above; (3) application effect, dedup, cursor and outbox atomicity on the same supported transaction handle; (4) production durability/pooling configuration, bounded retry handling and consistent restore drill; (5) retention/encryption and trust-boundary review; (6) measured representative workload and restart recovery with the actual MPE consumer. Check `history()` after uncertain checkpoint commits rather than blindly retrying, and bound retryable authentication/configuration failures (`docs/CONTRACT.md:72`). Existing save idempotency-key support must not be claimed: it is deferred (`docs/CONTRACT.md:87`).

**Recommended wording:** “UmbraDB is our proposed PostgreSQL recovery library for trusted backend workflows, subject to a pinned integration pilot. SQLite remains the local minimal tier.”
