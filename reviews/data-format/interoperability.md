# SDK interoperability and adoption review

Review date: 2026-10-03. Role: principal engineer, SDK interoperability and practical adoption; fifth reviewer. This report proposes work only. No runtime, schema, manifest, catalog or product document was changed.

## Decision

Ship a corrected, RFQ-focused **conformance release** next: one immutable private core, the existing three narrow profile contracts, independently implemented Rust and TypeScript interpretation, and two explicitly specified RFQ source adapters. Make only RFQ the integration pilot; keep invoice and agent acceptance informational. Add complete workflow types only when needed for the coordination demo. Do not turn the 267 vocabulary records into an SDK event union or a universal transaction model.

An integration release that actually performs local workflow effects must additionally pass durable recovery and current authority gates. Calling the next artifact a production SDK would exceed the evidence. The proposed sprint sequence remains appropriate: shared meaning, recovery, then demonstrated reuse.

## Inspected evidence and current limits

Read the unified-model, prototype-sprint, recommended-stack and UmbraDB-recovery documents; model README, validator, example RFQ and manifest; domain README, metadata schema, catalog and tests; and [semantic-science](semantic-science.md) and [contract-engineering](contract-engineering.md) reviews. Examined catalog entries by chain/evidence category and the RPC, finality, rollback, gaps and backfill records. No external research or partner integration was performed.

Executed from the repository root:

```text
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
PASS 51 checks; 3 schema self-checks; pinned local resources verified
/tmp/mpe-data-model-validation-env/bin/python model/domains/test_catalog.py
267 proposed entries; 12 tests pass
```

The unsigned examples occupy 964–1252 raw bytes. Those measurements establish neither sealed-envelope fit nor available room for future signatures, provenance or evidence references. Current validation is Python-only, fixture-authorized, unsigned and nonexecuting. No deterministic adapters, private capability negotiation, authenticated installer, historical contract coexistence or durable effects are demonstrated. These are declared implementation limits, not hidden defects.

The outer MPE wire/security profile, private event core and domain profile need separate lifecycles. Retain the existing outer wire unchanged for the conformance release. Keep all ten current core fields inside encryption and retain exact cross-checks among type, schema, profile and contract commitment. Share identity, time, bounded parsing and commitment construction; price bases, payment statuses, Step accounting and chain commitment remain domain-owned. CloudEvents compatibility does not mean arbitrary CloudEvents inputs become actionable.

## Correct the reference before copying its behavior

The companion reviews distinguish reproducible defects from future capabilities. Treat their counterexamples as release-blocking input vectors:

| Current issue | Interoperability consequence | Required decision |
| --- | --- | --- |
| Terminal newline accepted in IDs/coefficients | One runtime trims or parses what another rejects; identical economics acquires different commitment bytes | Require exact portable lexical grammars before conversion; never trim |
| Fractional/exponent JSON tokens round into numeric constants | Python/JavaScript number parsing can erase a noninteger input before validation | Pilot numeric JSON fields use lexical integer tokens; reject floating tokens before lossy parsing |
| Duplicate-action return omits its new occurrence record | Subsequent conflicting bytes under that occurrence escape conflict classification | Record the validated occurrence atomically with the existing action decision; specify replay precedence |
| Pending/reversed overpayment accepted although README excludes overpayment | Status changes alter arithmetic admissibility unexpectedly | Domain owner chooses a consistent three-status boundary and publishes vectors |
| Invoice occurrence/observation clock relationship unspecified | Independent freshness and latency calculations disagree | Define clock meanings before adding an ordering check |

These findings are reproduced in the linked reviews; this review inspected their code paths and reran the baseline suites, rather than independently rerunning every counterexample. The catalog's compute-budget classification and response/nonce ambiguities should be resolved before promoting those particular entries. They do not justify expanding next-release scope.

Whole Python-source hashing is currently fail-closed but couples all profiles to every validator edit. Replace that mechanism through an explicit reviewed contract revision: normative per-profile rules, primitive/canonicalization specifications and immutable vectors define the semantic contract; implementation hashes, dependencies and build provenance identify approved releases. Do not silently discard today's executable-authority commitment. Preserve historical bundles. Meaning changes require new commitments; a label such as `v0.1` cannot authorize reinterpretation.

## Two adapters must prove the same economics

Use separate source contracts rather than a configurable adapter guessing units. Illustrative input records below are proposed source fixtures, not accepted MPE payloads. Each source contract also requires stable source-object revision, parties, asset, validity, quote kind and fees.

```json
{"format":"dealer-a.usd-share.v1","quantity":"100","price":"123.45","currency":"USD","basisShares":"1","perspective":"RequesterBuy","fees":"None"}
{"format":"dealer-b.cents-lot.v1","quantity":"100","priceCents":"1234500","currency":"USD","basisShares":"100","perspective":"DealerSell","fees":"None"}
```

Both deterministically produce the existing RFQ economics: quantity `{coefficient:"100",scale:0,unit:"Share"}`, price `{coefficient:"12345",scale:2}` per one matching asset Share, cash `{coefficient:"1234500",scale:2}`, requester buyer and dealer seller. A parses decimal text exactly. B divides the integer cents amount by its declared denominator and requires exact representability at target scale. B value `1234501` per 100 shares rejects rather than rounds. Missing basis, perspective, fee policy, currency or asset mapping rejects; familiar price magnitude supplies no default.

Equal economics alone does **not** imply equal current intent digests. `business_digest` also includes source, contract and every typed data field, including IDs and validity. The equivalence fixture must represent the same attesting source and same complete quote through two encodings. Quotes from genuinely different dealers retain different source identities and digests; compare their economic projection separately. Never forge source equality just to pass a digest test.

Each mapping produces a separately bounded, private adapter receipt. Its proposed logical contents are source-byte digest, source format/revision, adapter commitment, target contract, target intent digest, identity-map version, transformations and classified loss. For B record `minor-unit-conversion`, `basis-normalization(100→1)` and `perspective-resolution`; all are exact. Label a dropped UI caption as omitted nonsemantic information only if the reviewed source contract says so. Unknown fields that might carry fees, tax, authority or validity require refusal or a new source contract. Retain original evidence/signature and verify it under its own rules; authenticate the transformed claim independently. A signature over source bytes cannot be copied onto target bytes.

Receipts are new contracts, not extensions smuggled into today's closed schemas. Keep receipt digest separate from the present business-intent construction until a reviewed provenance/signing rule explicitly binds it. Loss that prevents establishing target economics or evidence blocks action; retaining raw bytes does not repair that loss.

## Independent interpretation and SDK behavior

Use Rust and TypeScript/Node as the two release implementations, matching the proposed Rust sidecar and Node >=24 workflow host. Python remains a reference diagnostic. A TypeScript wrapper calling Rust, shared generated validator implementation, or a second Python test suite is not independent interpretation. Generate public types from schemas if useful, but implement parsing, semantic checks and commitment construction independently from the normative specification.

Keep real decimal magnitudes in strings with bounded integer arithmetic. TypeScript uses `bigint` internally and serializes coefficient strings; Rust uses bounded integer arithmetic after lexical checks. No JavaScript `Number`, binary float, UI amount or implicit currency exponent enters amount conversion. Scale/maxEffects are small lexical integers in the pilot. Publish exact JCS UTF-8 bytes and SHA-256 values for event, intent, proposal and manifest separately; ordinary sorted-key JSON is insufficient. Include non-ASCII/escaped keys, duplicate decoded names, Unicode/surrogates, integer-token bounds, whitespace, calendar boundaries and raw-byte/depth/array limits.

Expose typed accepted observations/candidates and stable rejection categories, plus duplicate, conflict, unsupported-contract, expired and recovery-gap outcomes. Specify precedence where several checks fail; do not require identical human error strings. Listener cancellation stays local; bounded queues/backpressure and isolated handler failures must not create upstream business selectors. `once` describes callback delivery, never business exactly-once behavior. An AsyncAPI/type catalog documents private operations; it is not permission or an RPC dispatcher.

## Manifest evolution and provider capabilities

Install immutable, content-addressed contract bundles under a reviewed local allowlist. Validate metadata and offline closure, read verified bytes once, and preserve active workflow references during retirement. Test old/new simultaneous installation, unsupported new input, restart under an old workflow and explicit authorized migration. Migration cannot renew approval validity or logical action IDs. Separate wire/security, private core, domain/workflow and adapter versions; negotiate exact commitments, not matching version strings.

Proposed private capability record, schematic rather than a current event:

```json
{"contracts":["sha256:<installed-rfq-contract>"],"adapters":["sha256:<approved-source-mapping>"],"maxBodyBytes":3926,"network":"<exact-network-identity>","methods":["<explicit-supported-method>"],"history":{"availability":"bounded","from":"<source-cursor>"},"observedAt":"<instant>","expires":"<instant>"}
```

Capabilities need authenticated issuer/session binding, bounds and freshness. Scope each advertisement to its service; do not require RFQ partners to advertise chain RPC methods. Absence means unsupported/unknown, not a default. Distinguish method versions, transaction-version support, provider limits, evidence formats, native finality and history availability. Claimed support does not prove complete history or source truth. Recheck actual responses and invalidation on endpoint/network/session changes.

Exchange only the authorized compatibility surface privately. Publishing installed profiles, interested contracts or provider queries to a relay leaks business interests. No intersection means typed refusal, never automatic schema download or fallback to a weaker contract. Local application observation of unsupported inputs does not trigger recognition acknowledgements upstream.

## Bounded evidence and recovery

Do not inline a block, receipt bundle, ERP document or account blob into the 3926-byte pilot body. A later evidence-reference profile must specify digest, encoding, length/maximum size, bounded projection, omissions, snapshot identity, authorized retrieval and retention policy. A schematic private reference is `{digest,byteLength,mediaType,projectionContract,omittedFields,retainedUntil,locator}`. A locator is an untrusted address, not authorization: prohibit arbitrary sender-selected fetches, enforce an approved service and access capability, bound/decompress safely, authenticate response bytes and verify the digest before interpreting them.

Private metadata alone does not make retrieval private. Fetch timing and requested object can expose recognition. For the next pilot keep evidence local or fetch only through an explicitly authorized, declared weaker retrieval profile. A stronger claim requires paired traffic evidence or a separately tested private retrieval mechanism. Catalog research URLs never become runtime locators.

Align evidence availability, schema/adapter bundle retention, dedup horizon and replay policy. Evidence missing, key erased, history pruned, decoder unavailable and stale freshness yield distinct gaps. Retention expiry cannot imply erasure; historical secret snapshots can defeat ratchet erasure. A record received before expiry does not permit an expired action after restore.

For the Node host compose inbox/dedup, supported local effect, outbox, checkpoint and cursor using one public UmbraDB transaction handle; current `saveAndAdvance` only covers checkpoint/cursor and must not be nested. Store exact contract/adapter commitments, action key, intent, source evidence identity and recovery context with durable progress. Test actual transaction durability and restore authentication; single-writer operation does not establish HA fencing. External completion needs destination idempotency and reconciliation; an unknown response cannot trigger blind retry. Rust/SQLite clients need the same acceptance semantics, not the same database dependency.

## Minimal delivery order and acceptance

Effort below is engineering effort for bounded artifacts, not elapsed promises or a production estimate; security/admission and partner availability are separate dependencies.

| Order / priority | Deliverable | Effort assumption | Exit evidence |
| --- | --- | --- | --- |
| 1 / P1 | Repair current lexical/replay defects; resolve invoice boundaries; publish corrected immutable contracts and corpus | 3–5 engineer-days | Reviewed commitment changes; counterexamples reject or receive explicitly revised expected meaning |
| 2 / P1 | Independent Rust and TypeScript parsers/interpreters plus A/B adapters | 2–4 engineer-weeks | Same raw-input decisions, canonical bytes, arithmetic and digests across runtimes; zero accepted disagreements; exact refusals retained |
| 3 / P1 | Local immutable bundle installation/coexistence and private compatibility experiment | 1–2 engineer-weeks | No schema fetch; no downgrade; old workflow replay; issuer/session/freshness and incompatible-intersection negatives |
| 4 / P1 before effects | RFQ workflow/recovery integration, separately reviewed request/accept types if needed | 2–4 engineer-weeks, excluding unfinished admission | Real crash matrix; no progress past uncommitted effects; resealed action dedups; paired privacy traces and actual sealed wire measurements |
| 5 / P2 | Invoice and agent reuse with explicit evidence and sandbox metering | Scope after gate 4 | Pending/partial/final/reversed evidence matrix; four separate agent workflow types; changed/revoked/expired input and uncertain-outcome tests |
| 6 / P3 | Customer-selected bounded chain observation experiment | Estimate after provider selection | One chain first; exact network/decoder/native commitment; zero/max integers, null/error/omission, rollback/gap and failed-execution evidence |

Conformance corpus entries should carry immutable case ID, raw source/event bytes, installed bundle set, adapter receipt/evidence bytes, trusted fixture provenance, expected decision/category, canonical target bytes and digests, plus ordered replay/crash operations where relevant. Capture runtime/compiler/dependency locks, commit, commands and full failures. Require all positive and rejection cases on both implementations; a missing fixture is a failed release check. Include altered source perspective, cents-per-lot ambiguity, nonrepresentable division, overflow, absent fees, unknown meaningful source fields, endpoint capability changes, old-contract migration and evidence expiry. Synthetic context remains explicitly synthetic.

Do not implement Ethereum and Solana simultaneously to demonstrate breadth. The catalog is 127 Ethereum plus 140 Solana proposed entries with no payloads or authority; its 12 metadata tests are not an adoption denominator. Promote a record only with a closed payload, exact deployment/network/decoder and source/evidence policy, two source mappings and independent interpreter vectors. Never merge Ethereum safe/finalized with Solana processed/confirmed/finalized into one `confirmed` flag, or force uint256/u64 zero-inclusive values through the pilot positive 18-digit primitive.

## Partner cost is an acceptance input

Run the RFQ exercise with two independently owned source conventions and, when available, a real buyer/dealer integration. Capture engineer-hours to first independently verified exchange, semantic-review hours, adapter code/config volume, exceptions, mapping refusals, manual corrections, deployment/upgrade/replay effort and support time. Compare to each partner's current integration and manual reconciliation baseline. Separate reusable core work, profile-specific work and partner-specific identity/convention mapping.

Report attempts, accepted agreements, safe refusals and accepted disagreements by convention, with sample counts and reasons. Require zero accepted disagreements in the finite adversarial corpus; report live uncertainty rather than extrapolating that result. Ask partners to explain quantity, price basis, roles, evidence and expiry from sample records; successful schema validation does not establish comprehension. Predeclare an acceptable partner-hour budget with participants before observing results, since no customer baseline exists here. If the second adapter requires another broad model redesign or upgrade churn overwhelms the baseline, revise the contract/adoption proposition before adding families. This is the practical test of whether a small shared core reduces integration cost.
