# Data format review — recommendations from five roles

Status: review and recommended backlog, not an implemented format revision. Two data scientists and three principal engineers studied the actual unified model, three pinned reference profiles and 267-entry Ethereum/Solana catalog. Their independent reports are in [reviews/data-format](../../reviews/data-format/README.md).

## Decision

Keep the small shared core and closed domain profiles. Do not freeze the present reference as the interoperable contract yet. Correct the reproducible parsing and identity defects, then prove independent agreement on a complete RFQ slice. Promote narrow chain observation slices with replay and explicit evidence before turning the broad vocabulary into supported runtime contracts.

The chain catalog is useful discovery coverage, not 267 validated event payloads. It contains 127 Ethereum and 140 Solana entries, with 67 native, 94 decoded, 27 derived and 79 intent classifications. All 40 chain/family cells are populated, but that does not establish complete request/result/failure lifecycles. Existing reference and catalog checks pass while additional adversarial examples contradict some stated rules.

## Reproduced reference defects

The [independent counterexample script](../../reviews/data-format/reproduce-findings.py) runs against unchanged pinned artifacts and records [actual outcomes](../../reviews/data-format/observed-counterexamples.json). It returns observations, not a security acceptance result; no effect executes.

| Input/sequence | Intended rule | Observed result |
| --- | --- | --- |
| RFQ occurrence ID ending in LF | Exact bounded identifier grammar | Accepted as `offchain-quote-valid` |
| Price coefficient ending in LF | Canonical integer string; no whitespace repair | Accepted as `offchain-quote-valid`; Python integer conversion discards whitespace |
| New occurrence of an already-known action, followed by changed occurrence time under that same new ID | Record immutable `(source,id)` even when action is duplicate | Both returns are `duplicate-action`; new occurrence never enters the occurrence map |
| Raw `maxEffects:1.0000000000000001` | No fractional coercion into the permitted constant | Binary float parsing rounds to 1.0; accepted as `sandbox-candidate-only` |

These are defects in a simulated, unsigned reference that always returns `executes:false`, not evidence of unauthorized production execution. The current 51 checks do not contain these complete counterexamples. The parser/identity accepted language changes when corrected, so review new commitments and preserve historic bundles rather than silently replacing meanings.

Two additional specification decisions matter. Overpayment is rejected only for Final payment observations, despite the README's general exclusion; matching trusted Pending evidence above payable remains accepted. The event occurrence time has no declared relationship to payment observation time. Decide the intended representation and clock semantics before enforcing an arbitrary restriction or calculating latency.

## Prioritized recommendations

Priority A means before freezing the next conformance reference; B means before admitting the affected prototype slice; C means later extension. Effort is relative, not a staffing/calendar commitment.

| ID / priority | Recommendation | Effort | Acceptance evidence |
| --- | --- | --- | --- |
| DFR-01 / A | Enforce exact full-string primitives and an explicit raw numeric-token policy. Reject whitespace and fractional/exponent coercion before numeric conversion. | Small | LF/CR/CRLF, exponent, overflow, rounded fractional constant and escaped-key corpus; two implementations agree on raw acceptance and canonical bytes. No silent trimming. |
| DFR-02 / A | Record valid occurrence identity even when its logical action already exists; define duplicate-event/action/conflict precedence. | Small | Original → new occurrence duplicate-action → exact occurrence duplicate-event → changed same occurrence conflict. Invalid input consumes no action. |
| DFR-03 / A | Specify occurrence/effective/observed/ingested clocks and the exact Pending/Final/Reversed amount boundary. | Small | Three-status below/equal/above-payable matrix, delayed reporting and explicit ordering/freshness cases. Context matching is not an arithmetic substitute. |
| DFR-04 / A | Correct catalog taxonomy and add a bounded lifecycle support matrix. Distinguish instruction proposals from RPC requests, submission results from normalized observations and raw nonce account bytes from decoded nonce state. | Small–medium | Record-level source mapping and request/result/error/rejection/unknown-outcome coverage. Token-2022 configuration cannot be counted as an actual withheld fee or hook execution. Label raw/generic-only and out-of-scope surfaces. |
| DFR-05 / B | Publish a corrected RFQ conformance slice with two separately specified adapters and independent Rust/TypeScript interpretation. | Medium | Dollars per share and cents per hundred, opposite role perspective, unsupported basis, precision, expiry and replay produce identical economics or explicit refusal. Equal intent digests require the same attesting source and complete quote data; different dealers remain distinct. Neither implementation imports the other's interpretation engine. |
| DFR-06 / B | Install immutable content-addressed contract bundles; separate normative meaning from implementation release attestation. Support historic contracts and explicit private negotiation. | Medium | Old/new contracts coexist; active old workflow replays unchanged; unsupported contract refuses. Invoice-only implementation changes have a reviewed cross-profile impact. Verify and use the same immutable bytes; offline closure, manifest consistency and dependency release evidence are tested. |
| DFR-07 / B | Define physical facts, logical operations, observer deliveries and derived projections separately, with append-only evidence/invalidation lineage. | Medium | Poll/subscription/backfill cannot triple-count one fact; repeated CPI transfers remain distinct; re-inclusion retains branch identity; decoder revision does not invent another transfer. Historical “known as of” views retain their observation cutoff. |
| DFR-08 / B | Promote one read-only token-transfer slice per chain before expanding protocol breadth. | Medium–large | Ethereum ERC-20 and Solana base Token Program slices pass zero/max raw integers, duplicates, failed execution, reorg/rollback, gaps and versioned metadata. Unsupported extensions stay unresolved or refuse. No signing/broadcast capability is included. |
| DFR-09 / B | Before effects, define authority-domain, policy, budget and stable effect state contracts, then prove the durable transaction and uncertain-destination path. | Medium–large | Permission/clock/revocation rechecked at effect boundary; explicit Step charging and aggregate reservations; inbox/dedup/effect/outbox/checkpoint/cursor atomicity; remote timeout goes to reconciliation rather than unsafe retry. Define retargeting and contract-upgrade action identity explicitly; candidate validation alone never consumes a production approval. |
| DFR-10 / B | Measure semantic agreement, evidence quality, scoped completeness and partner integration cost instead of vocabulary size. | Small to start | Publish attempted mappings, safe refusals, accepted disagreements, missingness categories, rollback/recovery results and engineering hours. Zero accepted disagreements in the declared adversarial corpus; live sample limitations and uncertainty remain explicit. |

## What to preserve

Keep explicit unitful price and quantity, exact buyer/seller perspective, closed fields/enums, domain-separated intent construction, source/role/policy boundaries and rejection of unknown semantics. Preserve Ethereum safe/finalized and Solana processed/confirmed/finalized as distinct native evidence profiles. Retain local listener cancellation, private schema negotiation and no runtime schema fetching.

Equal economic projections do not establish equal authenticated intent. The existing intent digest includes source, contract and complete typed business data. Test identical source intent through two encodings for digest agreement; genuine quotes from different dealers must keep their identities and distinct commitments. Do not forge source equality to pass a conformance test.

Do not expand the shared core with every field requested by a chain or finance adapter. Source surface, decode/derivation level, authenticity, execution outcome and native commitment are independent properties; define their relevant subset in each closed profile rather than multiplying a universal object. Missing, null, zero, omitted projection, unsupported, unavailable and decode-failed values must stay distinguishable.

## Proposed next release and experiment order

1. **Corrected reference:** resolve DFR-01–04, publish reviewed new commitments, retain the old model for explicit historical fixtures and add adversarial raw-byte/sequence vectors. Do not rebuild the existing version in place as a migration mechanism.
2. **Shared-meaning gate:** use RFQ as the first interoperable release. Independent Rust/TypeScript interpreters and two participant adapters must agree or refuse. Ship a small, offline contract bundle and precise acceptance/digest vectors.
3. **Durable reuse:** carry pinned contract and stable action state through real UmbraDB/PostgreSQL crash/replay tests before invoice and sandbox-approval breadth. Test destination reconciliation separately from local transactions.
4. **Read-only chain promotion:** choose one customer-relevant chain first, then implement the other as a separate gated slice. The target is one complete Ethereum and one complete Solana transfer observation/recovery slice. Define physical identity, native evidence, projection loss and invalidation. Keep signing, transaction submission and broader program-specific economics separately gated.

The five reviewers agree on the bounded design direction and the need for independent evidence. They emphasize different priorities: chain science proposes complete read-only datasets, while interoperability proposes RFQ as the first conformance release. This synthesis keeps RFQ as the primary product path and chain observations as narrowly scoped subsequent or separately staffed work; it does not add both full tracks to an unchanged sprint budget.

## Evidence and limits

The existing Python suite reports 51 reference checks plus three schema self-checks; the catalog suite reports 12 metadata tests. Reviewers inspected actual records, ran local checks and added counterexamples. No real partner corpus, live chain adapter, authenticated capability service, finality verifier, cross-language interpreter or durable effect executor was tested. Dependency hashes and file commitments do not alone prove implementation semantics or trusted installation. Catalog metadata checks cannot establish native chain truth or prevent all semantic reclassification by a maintainer.

Full role-specific reasoning, source links, effort estimates and adversarial chain sequences are retained in the five reports. These recommendations are saved for implementation consideration; pinned format artifacts and the published website remain unchanged by this review.
