# Recovery and storage copy review

Sources: `umbradb-recovery.md`, `recommended-stack-and-use-cases.md`, and the current `dist/index.html`. The recovery section already distinguishes today's checkpoint/cursor API from future atomic MPE processing and the separate replicated store. Preserve that distinction throughout component detail and journey copy.

## Suggested component copy

### Endpoint workflow recovery — UmbraDB + PostgreSQL / SQLite

**Role:** Recover application state inside each endpoint's trust domain. Trusted Node backend hosts use UmbraDB with PostgreSQL; standalone Rust nodes and clients can use SQLite. The Rust sidecar handles transport, proof validation and local recognition.

**Available foundation:** UmbraDB supplies temporal records, checkpoints and watermarks. Its current `saveAndAdvance` API atomically saves a checkpoint and advances a cursor. It does not commit business effects, deduplication or an outbox.

**Proposed MPE capability:** An additive future release would atomically commit local effects, deduplication, outbox records, an optional checkpoint and cursors, with strict durability, protected restore and writer ownership enforced at commit. Release timing is unset; integration acceptance remains ahead.

**Boundary:** Remote effects require stable destination idempotency keys and reconciliation. Checkpoint byte integrity does not establish trusted origin or freshness. Secret state needs protection before storage; historical snapshots must respect the selected erasure policy.

### MPE store — custom replicated envelope protocol

**Role:** Retain and replicate opaque encrypted envelopes, supply signed persistence receipts and support backfill under the selected privacy profile.

**Custom work:** Retention rules, replication, receipts and private retrieval belong to the MPE store protocol. Choosing UmbraDB, PostgreSQL or SQLite does not implement them.

**Boundary:** A persistence receipt is separate from admission, anchor/finality evidence, endpoint processing and a signed business acknowledgement. Transport operators do not inherit endpoint plaintext or keys.

## Targeted page corrections

- Recovery node subtitle currently reads “Durable inbox · local commit.” Prefer “Endpoint state · proposed atomic commit” or clearly mark the node as a target integration; the existing map caption does provide a design-stage qualifier.
- Keep “Today: checkpoint + cursor,” but expand detail to “Current saveAndAdvance: checkpoint + cursor only.” Current temporal records/CAS can support broader explicitly verified caller composition; the tag should not imply those are unavailable.
- Future-release paragraph: change “checkpoints” to “an optional checkpoint” and “lease-bound ownership” to “writer ownership enforced at commit.” Current lease and transaction connections are separate and do not provide stale-writer fencing.
- Principle “Recovery before action”: use “Endpoint recovery is designed to make interrupted workflows recoverable through durable state and bounded replay. External effects require destination idempotency and reconciliation.” Existing phrasing can otherwise read as accepted recovery behavior.
- Production phase: replace “Validate the future Umbra capability” with “Validate the proposed Umbra MPE capability or equivalently verified caller composition.” The recommended stack allows either route.
- Do not describe UmbraDB as an in-process Rust database, a shared plaintext recovery service, an encrypted store by default, or an HA/fenced writer system. Node >=24 and a trusted writer/domain are the inspected baseline.

## Implementation notes for component detail

A bounded current prototype may compose supported temporal/CAS operations, checkpoint save and watermark set under one public transaction handle. Do not nest `saveAndAdvance`: it opens its own transaction. Watermarks are last-write-wins; callers enforce monotonicity, finality and gap handling. Current migration durability warning callbacks cannot enforce strict durability simply by throwing; production policy must cover actual pooled transaction connections.

Before stronger recovery claims, validate duplicate/conflicting actions, crashes, unclean PostgreSQL recovery, lease loss, unsafe durability, expiry and wrong-key/domain/stale restore. No MPE workload benchmark or integration acceptance was established in the inspected evidence.
