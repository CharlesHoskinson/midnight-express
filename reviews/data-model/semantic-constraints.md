# Semantic constraints, vocabulary, units, and bounded interoperability

Research date: 2026-10-03, America/Denver. This review extends the selected [stack and use cases](../../docs/product-requirements/recommended-stack-and-use-cases.md) and [event-contract review](event-contracts.md). Seven primary specification pages were fetched as full HTML and extracted full text with Scrapling `Fetcher.get(..., timeout=25)`; the [catalog manifest](../../catalog/data-model/semantic-constraints/manifest.json) records source URLs, UTC retrieval timestamps, HTTP statuses, and separate SHA-256 hashes. UTC retrieval crossed into October 4. This is a design recommendation and illustrative schema, not implemented MPE conformance.

## Decision

Use a small shared vocabulary and reusable value types beneath closed, versioned domain profiles. The first release should understand a few exact RFQ, invoice/status, and bounded-agent-action contracts. It should refuse ambiguous executable intent rather than ask an LLM to reconcile synonyms, missing units, reversed trade direction, or unfamiliar conditions. A universal ontology covering all enterprise activities would add governance and implementation cost without ensuring safe execution.

The useful unification is **shared identity, exact values, units, time, provenance, and authority conventions**, not one universal business record. A market request requires instrument identity and price direction; an invoice requires issuer, payee, tax/payment-reference semantics; an approval requires operation, destination, maximum resources, validity, and approver authority. The common event spine remains the private CloudEvents-compatible wrapper already selected. Semantic fields and contract lookup remain inside authenticated encryption, without business routing topics or upstream content selectors.

Build the semantic contract as an immutable manifest binding: closed JSON Schema; field dictionary with normative definitions; allowlisted codes and asset/unit registry snapshot; deterministic cross-field rules; workflow transitions; authority/signature profile; named adapter mappings; and positive/negative conformance examples. Its digest binds rules beyond structural validation. A registry indexes installed contracts, not arbitrary sender-selected meanings. No live ontology resolution or LLM guessing belongs on the effect path.

## What the primary sources establish

| Primary source, inspected full text | Relevant result | MPE consequence |
|---|---|---|
| [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/), §§1.5, 3.4, 4.2, 4.8.1, 4.8.3 | Shapes support cardinality, allowed-value lists, and explicit property closure. Closure does not itself require properties. Entailment is optional, with failure required for unsupported requested regimes; recursive-shape validation is left to implementations. | SHACL can validate an RDF integration view. Specify closure, cardinality, target selection, graph boundary, entailment and recursion policy explicitly. It is unnecessary for native pilot JSON commands. |
| [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/), §4 and open-world discussion | Missing facts do not establish falsity; distinct names are not automatically distinct individuals. Cardinality axioms can imply identity or existence instead of functioning like record-validation errors. | Ontological consistency or inferred membership cannot prove that a command contains all required fields or that a principal has explicit permission. |
| [W3C JSON-LD 1.1](https://www.w3.org/TR/json-ld11/), contexts, protected terms, scoped contexts and imports | Contexts map terms to identifiers/types; protected terms restrict redefinition with specified exceptions. Context processing supports remote references, imports, scopes and base/vocabulary rules. | A context is a meaning map, not an executable authorization schema. Pin the whole context closure and processing mode; disallow sender context overrides in the authoritative profile. |
| [W3C JSON-LD 1.1 Processing Algorithms and API](https://www.w3.org/TR/json-ld11-api/), Context Processing and document loader | Loading and expanding remote contexts is part of processing; document loading is configurable. Expansion and compaction depend on the active context and algorithm options. | If JSON-LD is needed, use a loader that resolves only installed digest-pinned resources and rejects everything else. No runtime remote fetch or mutable latest context. |
| [UCUM specification](https://ucum.org/ucum), §§4–7 and annotations | Defines machine-readable unit expressions with separate case-sensitive/case-insensitive representations, compositional units, and special conversions. Annotations carry no unit semantics. | Use a small case-sensitive UCUM allowlist for actual physical measurements. Do not treat `kg{assetABC}` as a secure asset identifier or make arbitrary compositional expressions actionable. |
| [QUDT schema, January 2025](https://www.qudt.org/doc/2025/01/DOC_SCHEMA-QUDT.html), QuantityValue, QuantityKind, units, conversion and currency properties | Distinguishes magnitude, unit, quantity kind and dimensions; exposes conversion multiplier/offset and currency exponent metadata. | Reuse quantity-kind/unit concepts in offline mappings. Currency metadata is not a live exchange-rate oracle, and equal dimensions do not establish economic interchangeability. |
| [JSON Schema 2020-12 validation](https://json-schema.org/draft/2020-12/json-schema-validation), §§6, 7, 9 | Supports type, required, enum/const, patterns and bounds. `format` assertion support is optional; defaults are annotations. | Structural checks are deterministic when implementation behavior is pinned. Application checks still establish calendar validity, registries, economics, authorization and current state. |

The recommendations below are MPE design judgments derived from these distinctions, not claims that these specifications mandate one system architecture.

## Minimal semantic kernel

| Primitive | Required meaning and boundary |
|---|---|
| Identity | Namespace plus bounded identifier, with authority domain and registry snapshot. Asset identity includes network/issuer/contract where relevant. `USD`, `ABC`, ticker symbols, display labels and filenames alone are insufficient. |
| Exact amount | Canonical nonnegative decimal string and scale fixed by the profile or explicit and checked against registry terms. Bound coefficient size. Reject exponent notation, whitespace, leading-zero variants and unsupported precision. Signed quantity uses a separate deliberate type; avoid negative zero and inferring debit/credit from sign. |
| Physical measurement | Exact value, allowed unit code, and quantity kind. Define allowed conversions, offsets, precision, rounding and uncertainty when relevant. A UCUM expression's validity alone is insufficient. |
| Price | Numerator asset, denominator asset, denominator quantity, exact value/scale, price basis, fee/tax treatment and validity. Fix direction explicitly, such as quote currency per one base unit. Basis-point spreads, yields, percentages and clean/dirty bond prices require distinct profiles. |
| Money | Asset/currency identity and representation scale. Currency minor-unit exponent and ledger token precision can differ from negotiated price precision. No automatic currency conversion; any conversion requires an authorized rate/source/time/rounding policy. |
| Time | One fixed UTC representation and precision, verified by an actual instant parser. Distinguish occurrence time, quote expiry, source observation time, settlement deadline, approval expiry and transport expiry. |
| Reference | Typed request/offer/order/invoice/action identifier, scoped issuer/tenant/destination, and where needed immutable content digest/revision. References must resolve to authenticated expected objects, not merely well-formed strings. |
| Workflow state | Closed state/event vocabulary, predecessor revision or sequence, transition rules, gap/finality status and responsible authority. Delivery ordering does not determine business validity. |
| Role/capability | Explicit issuer, subject, role/operation scope, destination, bounds, validity and policy version, checked against trusted authority. A claimed `role` string is not permission. |

Avoid unbounded `attributes`, `terms`, `parameters` or freeform unit strings in executable profiles. Optional narrative can live in a separately bounded annotation area only when the signed profile explicitly classifies it as non-authoritative. An unknown new restriction must fail closed; software may not strip it and then execute. Descriptions must never carry omitted restrictions such as “subject to manager approval.”

Use stable ASCII code values and localized display labels separately. Introduce new synonyms through reviewed ingress adapters, producing an explicit normalized proposal and provenance before fresh authorization when signed intent changes. No global `owl:sameAs`, fuzzy asset match, latest vocabulary fetch, or model-generated enum translation can grant authority.

## Implementable narrow RFQ profile

The catalog includes a complete illustrative [JSON Schema 2020-12 payload](../../catalog/data-model/semantic-constraints/rfq-request.schema.json) and [example request](../../catalog/data-model/semantic-constraints/rfq-request.example.json). It closes every nested object and pins a fictitious `pilot:asset:ABC`/`pilot:fiat:USD` pair. The all-zero example terms digest is a placeholder; production must reject it unless it identifies a genuinely installed contract, which it is not intended to do. The payload sits inside the existing closed private event wrapper; this example does not replace its identity or signature rules.

The example means: requester buys exactly `10.000000` ABC, with limit `12.5000` USD per `1.000000` ABC, excluding fees, all-or-none fill, expiring at a specific UTC instant. Its maximum base purchase consideration is `125.00` USD before separately authorized fees. It is coordination only and grants no settlement authority. Different instrument types, partial fills, taxes, accrued interest, lot sizes, and execution venues need explicit named profiles rather than hidden optional semantics.

After schema acceptance, a deterministic handler must check:

1. The exact installed contract/terms digest and authenticated requester/instrument identities match the private wrapper and authority domain.
2. Quantity and limit are positive, within issuer/market bounds, satisfy the allowed lot/tick rules, and match registry scale. Schema deliberately permits lexical zero; the domain gate rejects economically invalid zero requests.
3. `createdAt < expiresAt`, valid calendar instants, current freshness and allowed lifetime hold under the configured clock policy. A regex cannot validate February 30 or establish a trusted time source.
4. Buy/sell is always from the named requester's perspective, and offers reference the authenticated request/revision. Base/quote orientation and denominator quantity must match exactly.
5. Exact coefficient arithmetic computes totals and applies the declared rounding policy only at the defined posting boundary. With scales 6 and 4, the product has scale 10 before USD total rounding to 2. Validate bounds before multiplication; do not use JavaScript `Number` or floating-point intermediates.
6. Fees are excluded by this request; the acceptance contract separately binds any permitted fee amount, total spend ceiling, payee and destination. Rounding, slippage and extra fees cannot expand a signed budget silently.
7. Duplicate/revised/cancelled/expired requests and unsupported conditions enter the prescribed state machine. A quote acceptance binds offer digest, request digest, destination, action ID and authority; it cannot rely on “latest offer” or freeform order references.

Rust and TypeScript should receive generated closed types only after lexical and domain validation, with exact-value arithmetic backed by integers or an audited decimal library. Generated types help callers but do not replace runtime hostile-input validation. No missing approval, unit or side is filled by a schema default.

## Optional RDF and JSON-LD boundary

Use RDF/JSON-LD when a customer integration genuinely needs stable term identifiers, knowledge-graph search or cross-domain discovery. Keep it as a derived, provenance-bearing view of the signed JSON event, with an explicitly installed mapping version. A semantic graph projection is not a replacement signature preimage: expansion, compaction, graph merges or dropped JSON terms cannot redefine the originally authorized bytes.

For JSON-LD exports, pin processing mode `json-ld-1.1`, complete context bytes and imports, base IRI and mapping options. Configure an offline document loader with a finite URI-to-digest map; reject unknown URLs and prevent network fallback. Prefer exporting an installed context rather than accepting sender-supplied inline/scoped context definitions. Protected terms help vocabulary discipline but are not an access-control mechanism or cryptographic pin.

If an RDF consumer accepts commands, require a separate installed closed SHACL profile: explicit targets or focus-node checks, `sh:minCount 1` and `sh:maxCount 1` for required scalar fields, `sh:in`/`sh:hasValue` for allowed codes, `sh:closed true` on each relevant nested shape, and a defined finite graph boundary. A valid empty graph or a node that was never targeted must not become a valid command. Reject recursive shapes and non-installed SPARQL/custom constraints for the pilot; specify any entailment policy and graph-size/query resource limits. RDF graph closure differs from global knowledge completeness.

Do not deploy a live OWL reasoner, unrestricted SPARQL rules, triplestore, full QUDT corpus or whole UCUM expression engine in the executable pilot solely to claim “semantic interoperability.” Offline tooling may check vocabularies and generate audited mappings. The trusted runtime can be a finite dictionary, closed schema, exact arithmetic and a small state machine.

## Bad-to-good counterexamples

| Bad input or assumption | Safer explicit contract and outcome |
|---|---|
| `"buy 10 ABC at 12.5"` | Exact asset identities, requester perspective, quantity scale, price orientation/basis and expiry. Narrative becomes a proposed request requiring typed confirmation. |
| `amount: 100`, consumer assumes dollars, producer intended cents | `value: "1.00"`, USD identity, scale 2 under an installed profile. A change to minor-unit integer representation creates a new contract digest. |
| `price: "0.08"` with base/quote reversed | Separate numerator/denominator identities and pinned `QUOTE_PER_ONE_BASE` basis; reversed pair rejects rather than reciprocates automatically. |
| `unit: "m"` interpreted as metres by one consumer and millions by another | Physical metre has an allowlisted UCUM identity; million currency units must be converted by an explicit finance adapter, never a unit guess. |
| `rate: 5`, mixing percentage, fraction and basis points | Separate closed types, such as integer basis-point count or fixed fractional rate; conversions are named and checked. |
| `kg` amount treated as interchangeable with token units or a nominal invoice amount | Quantity kind and asset identity remain separate; dimensional equality is insufficient for economic equivalence. |
| OWL cardinality says exactly one payee; payload omits payee | Closed schema/SHACL presence gate rejects. An inferred existential payee does not supply an authorized destination. |
| Sender context maps `price` or `approver` differently | Authoritative JSON profile refuses context substitution; optional exporter uses the installed pinned mapping and no network fetch. |
| SHACL report passes because no node matched target class | Require the designated command focus node, its expected class/profile and cardinality before acceptance. |
| New offer adds `approvalRequired` or “subject to approval” in a note | Unknown authority field/contract rejects; a new profile makes the condition explicit and tests its enforcement. Notes never downgrade restrictions. |
| Quote schema validates but offer has wrong request revision, expired terms or untrusted signer | Cross-field/state/authority gates reject before any effect. Structural validity is not economic or permission validity. |
| AI substitutes USDC for USD, reciprocal price, or a newer quote | Executor rejects mismatched exact assets/offer digest and limits. Model may propose a new typed action; it cannot approve its own substitution. |

## Governance and acceptance

Assign one owner to the shared kernel and a domain owner to each profile. Require a normative dictionary entry for each executable field: exact meaning, units, perspective, authority, presence/null rules, valid bounds, arithmetic/rounding, and change classification. Standardize only fields that truly share meaning; reuse names without shared definitions is false consistency.

Release a small offline contract bundle with immutable digests and named adapters. New executable enums, fields, units, fee semantics, rounding or state transitions require a new semantic contract and explicit adoption. Test adapters with reversed orientation, scaled amounts, suppressed approval, wrong issuer/network and stale revisions. Do not label a structurally accepted but lossy adapter semantically compatible.

The illustrative JSON artifacts were serialized and parsed successfully; no JSON Schema validator was available in the inspected Python environments, so runtime/meta-schema validation is not claimed. Before a pilot, validate both implementations against nested extra properties, zero/bounds, decimal syntax/overflow, tick/lot rules, total rounding ties, currency/token scale differences, wrong numerator/denominator, invalid calendars, expiry, wrong-role signatures, unresolved/conflicting references and unsupported contract digests. For any JSON-LD/SHACL integration add remote-context refusal, context substitution, untargeted nodes, missing cardinality and inference/recursion mismatch vectors.

The pilot can reduce ambiguous AI inputs without a universal semantic platform. Its assurance comes from explicit installed meanings, deterministic economics and current authorization at the effect boundary; vocabulary reuse alone cannot provide those guarantees.
