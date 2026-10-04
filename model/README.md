# Midnight Express model v0.2

Use this local reference to check how applications interpret quotes, payment observations and approvals to write a report. Each workflow has a strict profile defining its fields and rules. RFQ adapters translate two declared quote formats, while independent interpreters compare their meaning across Python, Rust and TypeScript. Reviewed definitions are stored in immutable offline bundles. Separate prototypes exercise read-only chain observations and recovery of a database report write.

The source and permission evidence is supplied by test fixtures. Production use still requires protocol signing/sealing, genuine admission, authenticated contract distribution, a current permission service and live partner evidence. This release does not deploy the MPE protocol, verify consensus or execute financial transactions.

## Rules enforced by v0.2

- Raw parsing rejects duplicate decoded keys, floats/exponents, negative/unsafe integer tokens, invalid UTF-8/surrogates and oversized/deep input. IDs and coefficients use exact portable grammar checks; whitespace is never trimmed.
- Every valid occurrence is recorded, including duplicate actions. Reusing an occurrence identity with changed content creates a conflict. A new occurrence/EID cannot renew an action.
- A payment observation’s amount cannot exceed the invoice payable for Pending, Final or Reversed. `effectiveAt <= observedAt <= event.time <= trustedNow`; event time is observation-record creation. No payment allocation or execution is implied.
- Approval commits authority domain, execution scope, budget window and full proposal. Stable action identity is `(authorityDomain, executionScope, actionId)`; target/contract changes conflict rather than silently re-keying a consumed action.
- Per-profile schema/rules + common primitive/canonicalization definition determine immutable semantic commitments. Python implementation bytes no longer determine every domain's contract. Implementation/dependency evidence is recorded separately.
- The chain vocabulary proposes 291 entries and records lifecycle support in a matrix. A reviewed semantic index checks for reclassification under an existing released ID. Runtime payload contracts still need to be defined for these entries.

## Run the checks

Use an isolated Python environment; dependencies and transitive distribution hashes are pinned in `requirements.lock.txt`.

```bash
uv venv /tmp/mpe-data-model-validation-env
uv pip sync --python /tmp/mpe-data-model-validation-env/bin/python --require-hashes model/requirements.lock.txt
cargo build --locked --manifest-path model/interpreters/rust/Cargo.toml
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
/tmp/mpe-data-model-validation-env/bin/python model/test_bundles.py
/tmp/mpe-data-model-validation-env/bin/python model/domains/test_catalog.py
/tmp/mpe-data-model-validation-env/bin/python model/test_interoperability.py
/tmp/mpe-data-model-validation-env/bin/python model/test_chain_observations.py
```

TypeScript runs directly on Node >=24 with type stripping. For strict type checking, `npm ci --prefix model/interpreters` then `npm run typecheck --prefix model/interpreters`. This compiler and its types are pinned independently of the semantic contract.

The RFQ campaign compares independently implemented Python, Rust and TypeScript parsing, schema checks, semantics, canonical bytes and intent digests. The Rust cents-per-hundred adapter and TypeScript dollars-per-share adapter represent the same complete attested fixture intent; price-basis, perspective and unknown-field negatives refuse. Different genuine dealers retain distinct source-bound intent hashes even when economics match.

The files in [evidence/](evidence/) record outcomes for finite synthetic cases. Operational error rates and customer savings remain unmeasured. `test_interoperability.py` deliberately regenerates local evidence after executing all interpreters; it never silently replaces an immutable bundle.

## Exact profiles and primitives

All ten event fields (`specversion`, `id`, `source`, `type`, `time`, `datacontenttype`, `dataschema`, `mpeprofile`, `mpecontract`, `data`) stay inside the proposed MPE encrypted body. The outer transport/EID/admission format is unchanged. Each schema closes every object and pins exact type/schema/profile. No sender URL triggers a fetch.

IDs are bounded scoped ASCII strings with exact equality. Instants are real Gregorian UTC `YYYY-MM-DDTHH:mm:ss.000Z`, years 0001–9999, seconds precision, no leap seconds or offsets. JSON numeric tokens are nonnegative lexical integers <=9007199254740991; money and quantities use bounded decimal strings. Parsing is limited to 3926 raw UTF-8 bytes, depth 12, 512-character strings and 16-item arrays. This raw event limit does not establish sealed wire fit or signature overhead.

| Profile | Exact type | Meaning |
| --- | --- | --- |
| `rfq.v0.2` | `mpe.rfq.quote.v0.2` | Whole pilot Shares, USD cents, absolute price per one Share, explicit requester perspective, fees None, exact cash and exclusive expiry; off-chain observation only |
| `invoice.v0.2` | `mpe.invoice.payment-observed.v0.2` | Matching complete trusted fixture evidence, positive partial/full amounts, distinct Pending/Final/Reversed and explicit clocks; Final remains a source assertion |
| `agent.v0.2` | `mpe.agent.approval.v0.2` | Exact sandbox WriteReport proposal, authority domain/scope/window, input/target/policy/budget/expiry and named human; validation produces a candidate only |

Decimals are `coefficient × 10^-scale`: positive canonical coefficient strings of 1–18 digits; quantity/Step scale 0 and USD scale 2. Zero/fractional Shares, multi-currency, arbitrary fees/assets/tools and broad invoice accounting are outside these pilot profiles. Chain uint256/u64 zero-inclusive quantities use their own primitives.

An intent candidate is an unsigned fingerprint of the source and complete business terms, allowing implementations to compare their interpretation. It is SHA-256 of JCS `{domain:"mpe.model.intent.v0.2",source,type,profile,contract,data}`. Proposal candidate uses `{domain:"mpe.model.proposal.v0.2",contract,proposal}`. No occurrence ID/time or outer EID enters the business intent. These are unsigned commitments; origin authentication and permission are not inferred from a digest. Every Python/Rust/TypeScript validation success has `executes:false`.

## Install exact rules and preserve history

A bundle packages one contract’s exact definitions for offline use. `bundles/<manifest-sha256>/` contains `manifest.json`, `schema.json`, `core.json`, `rules.json`. The manifest commits raw resource bytes; the contract commits its JCS manifest. Schema and rule resources never contain their own contract digest, avoiding cycles. The offline `profiles/installed.json` allowlist selects exact installed contracts; `profiles/lock.json` is the current alias set. Unknown contracts refuse, with no downgrade/default insertion.

The loader closes manifest metadata, bounds reads, rejects symlink/path escape and every reference keyword, verifies resource bytes once and validates from that same snapshot. The pure `negotiate` helper finds exact commitments installed on both sides. Authentication and a network handshake require separate mechanisms. Operator-reviewed allowlists are a fixture trust assumption; authenticated atomic installation and live workflow migration are not demonstrated.

The original [v0.1 release](releases/v0.1/README.md) preserves exact schemas, validator, manifests, fixtures and known defects. Its archived interpreter retains historical behavior:

```bash
/tmp/mpe-data-model-validation-env/bin/python model/releases/v0.1/test_conformance.py
/tmp/mpe-data-model-validation-env/bin/python reviews/data-format/reproduce-findings.py
/tmp/mpe-data-model-validation-env/bin/python reviews/data-format/reproduce-findings.py --current
```

The default counterexample command reproduces the reviewed v0.1 faults; `--current` checks v0.2 corrections. v0.1 is registered **historical-read-only** and the current loader refuses to dispatch it. An archived test pass is not permission to reactivate an unsafe historical contract. No live workflow has been cut over. `build.py` creates reviewed current artifacts and refuses to overwrite different bytes under an existing content hash; it is not an installer or a migration service.

## Read-only chain slices

[chains/observations.py](chains/observations.py) and its closed [transfer schema](chains/transfer.schema.json) implement bounded Ethereum ERC-20 receipt/log projection and Solana legacy base Token Program TransferChecked projection. They preserve zero/max exact amounts, approved network/genesis, physical inclusion/instruction identity, source/fragment/context digests and decoder identity. ERC-721-shaped logs refuse; Token-2022/unknown instructions or transaction versions are outside the admitted base slice. Diagnostic failed transactions yield no ordinary transfer effects; this does not assert their fees or durable nonce changes vanish.

The Solana branch hash is separately supplied fixture evidence, never inferred from the transaction's recent blockhash. Source payloads are bounded dictionary fixtures; `sourceDigest` identifies their deterministic JSON serialization, not authenticated original RPC wire bytes. Full live RPC parsing, provider authentication and independent program decoders remain required before promotion. No signing/broadcasting or effect capability is exposed.

The SQLite journal keeps observer deliveries, physical facts, native commitment assertions, invalidations and gaps append-only. A supplied known-at clock is trusted local intake context and must not regress; it is not sender event time. Duplicates from polling/subscription/backfill aggregate once, repeated CPI transfers stay distinct, re-inclusion has a new physical location, historical cutoff views remain separate, and conflicting commitment assertions expose a gap instead of a total. Finality assertions are explicitly source fixtures, not consensus proofs.

## Recover a report write with Umbra

[recovery/umbradb-host.mjs](recovery/umbradb-host.mjs) uses only Umbra's public root API and one `withTransaction` handle for inbox, action/dedup, sandbox report row, Step accounting, outbox, checkpoint and cursor. It does not nest `saveAndAdvance`. The host prepares the write by cloning intent, checking scope and verifying current fixture permission. It checks that permission again inside the transaction, reserves the declared maximum budget, charges one Step for the report-row write and releases unused capacity. Stable action/occurrence conflicts, aggregate budget, revocation, concurrent replay and cursor behavior are tested.

Run against an isolated PostgreSQL 17 database and the built reviewed Umbra checkout. The measured checkout is `f662822765247f0da553347c9819f958a1992d28` (package metadata 0.9.5); the original research's earlier checkout is not silently substituted.

```bash
UMBRA_DIST=/path/to/UmbraDB/dist \
UMBRA_COMMIT=f662822765247f0da553347c9819f958a1992d28 \
MPE_TEST_DATABASE_URL=postgres://postgres@127.0.0.1:55437/postgres \
node model/recovery/test-postgres.mjs
```

The test creates a fresh `mpe_format_<pid>` schema. It kills four actual worker processes: after effect writes, before commit, after commit before acknowledgement, and after a separate destination-fixture commit. Recovery produces one local report write; uncertain delivery exposes OutcomeUnknown and reconciles the original idempotency key. Destination delivery is a separate-transaction acknowledgement fixture, not a live external payment/tool service. Neither PostgreSQL nor a local transaction supplies global exactly-once effects, HA fencing, consensus finality, checkpoint encryption or production authority.

## Literature and implementation status

Original narrow concepts draw from [CloudEvents](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core), [JCS](https://www.rfc-editor.org/rfc/rfc8785), [FINOS CDM](https://cdm.finos.org/docs/product-model/) and [UBL](https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html). These are selectively adapted concepts; full CDM/UBL/ISO/FIX conformance is not claimed. The repository retains the research sources and five independent reviews.

See [recommendation implementation status](../docs/product-requirements/data-format-implementation.md) for artifact-by-artifact evidence and remaining deployment/customer gates. The three website sprints remain a proposed protocol-validation plan; these components do not establish their entire completion.
