# Unified data model — bounded contracts, shared meaning

Status: proposed design, with a narrow executable Python reference slice in [model/](../../model/README.md). This supplements the product requirements; it does not rewrite the original protocol requirements or demonstrate a deployed protocol.

## Recommendation

Unify the **contract mechanism and a few primitives**, then define closed, independently owned workflow profiles. Do not attempt a universal model of every market instrument or organization. Participants agree to the same immutable semantic contract before an event becomes actionable. Unsupported messages may remain encrypted or be recorded as undecodable; they must never become actions through guessed meanings.

The common private event core carries event identity, source, occurrence time, exact event type, schema identifier and semantic-contract commitment. Each domain profile defines its own terms, roles, units, state transitions and authority requirements. RFQ terms do not belong in invoice or agent schemas. All of this remains inside the MPE encrypted body: no public topics, schema lookups or routing selectors reveal business subscriptions.

The initial reference implements three exact types: `mpe.rfq.quote.v0.1`, `mpe.invoice.payment-observed.v0.1`, and `mpe.agent.approval.v0.1`. These are conformance slices, not complete request/offer/accept, invoice-accounting or proposal/approval/execution/result protocols. The remaining typed events and state machines are prototype work.

## Literature we can use

| Source | Adopt selectively | Boundary |
| --- | --- | --- |
| [Eric Evans, Domain-Driven Design reference](https://www.domainlanguage.com/ddd/reference/) | Bounded contexts, explicit ubiquitous language and translation between contexts | No universal Customer, Price or Status object |
| [Enterprise Integration Patterns: Canonical Data Model](https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html) | A small canonical contract reduces pairwise adapter growth | Canonical syntax alone does not unify economics |
| [CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) | Private event wrapper and occurrence identity `(source,id)` | No authorization, workflow state or business truth implied |
| [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core) | Closed structural contracts, exact enums and bounded data | Explicit semantic checks and asserted calendar validation are still required |
| [FINOS Common Domain Model](https://cdm.finos.org/docs/product-model/) | Unitful price/quantity, party roles and economic lineage | Reuse concepts; do not import its entire runtime or claim CDM conformance |
| [OASIS UBL 2.3 Invoice](https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html) | Invoice parties, document identity and payable amounts | Restricted original JSON profile, not UBL XML conformance |
| [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785) | Deterministic bytes for explicit business-intent commitments | Does not define currency, units, rounding or signature authority |
| [W3C SHACL](https://www.w3.org/TR/shacl/) | Closed-shape thinking and explicit semantic constraints | Optional offline semantic export; no RDF reasoner in the execution path |
| [CaMeL](https://arxiv.org/abs/2503.18813) | Separate untrusted content from capability-controlled execution | Research precedent, not proof our authorization system is secure |

Five role-specific studies and Scrapling archives are indexed in [catalog/data-model](../../catalog/data-model/README.md). Financial code sources were pinned where available; historical FpML and candidate SBE documents are labeled as such. Some fetches failed or required a documented TLS-verification exception; failed records are not evidence. Concepts above are adapted into original narrow definitions, not copied full schemas. Any future imported/generated standard artifacts need artifact-specific license review.

## What agreement actually means

A locally installed, reviewed contract manifest pins schema bytes, dictionaries, rules and validator semantics. Version names alone are insufficient. The reference pins schemas, rules and its Python validator, then commits the complete manifest using JCS and SHA-256. The graph is acyclic: resources → manifest → trusted lock → event. Production implementations must add protocol signing rules, workflow state-machine specifications and approved adapter definitions to their reviewed contract distribution.

Never fetch a schema from a sender-supplied URL during handling. Negotiate the intersection of installed exact contract commitments privately; no compatible intersection means no automatic action. Trust comes from authenticated installation and policy, not from a hash supplied by the sender. Keep wire/security, common core, domain contracts, and workflow/policy versions separate. Active workflows pin their contract; explicit authorized migration or continued old-contract interpretation is required for replay.

The validator pipeline is: bounded raw parse → duplicate-key rejection → exact installed profile → closed structural validation → semantic invariants → authenticated source and role → freshness and current policy → state/replay checks → atomic effect boundary. The current reference implements the parse/contract/semantic stages and simulated context checks only. Its return values always say `executes:false`.

## Prevent the dangerous price mismatch

Consider 100 shares at 123.45 USD per share, total 12,345.00 USD. Participant A declares a dollar unit price `123.45`. Participant B declares `1234500` cents **per 100 shares**. They mean the same trade only when each adapter's pinned convention explicitly establishes currency, minor-unit conversion, denominator and role perspective. Missing basis, currency or perspective must reject. A value that merely looks familiar is not sufficient.

Our pilot uses positive canonical integer coefficients and a declared scale: `value = coefficient × 10^-scale`. Quantity is whole Shares; USD price and cash use scale 2. Price states the numerator currency, denominator asset/unit and base quantity. Requester BuyAsset/SellAsset fixes buyer and seller roles. Fees are explicitly None. A precise cash equality check prevents plausible-but-inconsistent totals. This profile intentionally excludes fractional shares, derivatives, multi-currency and negotiated fee structures. Broader instruments require new reviewed profiles, not optional fields with guessed defaults.

Sprint 1 must implement two independently specified source adapters and an independent Rust/TypeScript interpreter. They must produce equal canonical economics and intent commitments, or refuse the mapping. Python-only reference tests do not establish that agreement. Preserve source bytes/digest, adapter contract, transformations and loss information. A transformed event needs a new attestation; it cannot reuse a signature over the original bytes.

## Identity, authority and truth

Keep five concepts separate: occurrence `(source,id)`; workflow/correlation; source object and revision; stable logical business action/destination key; and outer envelope EID. Re-emitting or resealing with a new EID must not renew an approved action. The reference excludes occurrence id/time from its unsigned business-intent candidate and includes source, exact profile commitment and all typed business data. MPE wire bytes, admission commitments and signature/AAD inputs remain distinct protocol constructions.

An authenticated payment observation is a source claim. Pending, Final and Reversed must remain distinct. Even a matching Final fixture is neither bank-finality proof nor automatic invoice allocation or payment authority. An approval binds the complete sandbox proposal, target, input, budget, expiry, policy and named human. Current authorization and revocation must be checked again immediately before an effect. Separate typed proposal, approval, execution request and result contracts are required in the full workflow. No arbitrary tool dictionary, script or LLM interpretation belongs in the executor.

Atomic local transaction composition covers inbox, dedup, effect, outbox, checkpoint and cursor. External destinations still need stable idempotency keys and reconciliation. An uncertain remote outcome stops automatic retry until resolved. The reference's in-memory duplicate detection does not establish durable exactly-once behavior.

## Avoid death by committee

Domain owners can publish experimental private profiles without expanding the global core. Core promotion requires demonstrated reuse in at least two independent profiles and a bounded maintenance cost; this is a proposed governance rule. Meaning-changing changes produce new commitments even if structural changes look compatible. Trusted profiles classify extensions; sender declarations cannot turn an unknown effect-bearing field into an inert annotation. The initial reference admits no extensions at all.

Measure partner adapter effort, rejected convention mismatches, unsupported-profile rates and domain-specific comprehension. An expanding adapter/configuration burden can falsify the value proposition even when all schemas validate. AI can draft proposed mappings and requests, but deterministic reviewed adapters and contracts govern actionable messages.

## Validation and next decision

The executable slice contains three closed schemas, pinned local manifests, five unsigned examples and a negative corpus. See [model/README.md](../../model/README.md) for exact restrictions and reproducible commands. Passing it demonstrates reference rejection behavior; it does not establish cryptography, authenticated finality, protocol wire fit, deployed adapters or cross-language agreement. Extend only after the [three prototype sprints](prototype-sprints.md) establish shared interpretation, durable recovery and reuse without unsafe inference.

## Ethereum and Solana application domain

Extend the domain vocabulary through separate chain profiles, not a generic Transaction or Confirmed enum. Full inventories: [Ethereum](ethereum-application-domain.md), [Solana](solana-application-domain.md), and [machine-readable domain catalog](../../model/domains/README.md). The machine catalog contains 267 proposed vocabulary entries across 20 families per chain; its 12 checks validate catalog metadata, not chain payloads. These are proposed contracts; the executable v0.1 validator still accepts only the three financial/approval reference events.

| Application surface | Required messages and events |
| --- | --- |
| RPC and endpoint | Typed request/result/error, endpoint capability/network identity, bounded batch correlation, read/query, simulation, fees and compute/gas estimates |
| Chain progress | Block/header/slot/root observations, native finality/commitment views, canonical ancestry, rollback/reorg/removal, gap and backfill reconciliation |
| Transaction lifecycle | Proposal, exact signing request/result, broadcast request/result/unknown outcome, pending or signature observation, inclusion and execution errors, expiry and policy-labeled replacement/drop inferences |
| State | ETH/SOL balances, nonces/storage/code, Solana account/program data and owner, token balances and metadata, explicit state block/slot and source context |
| Contract/program | Ethereum raw logs and pinned ABI decoding; Solana instructions, inner instructions/CPI and program logs with pinned decoder/program identity |
| Tokens and NFTs | ERC-20/721/1155 transfers, mint/burn derivations, approvals/operator permissions; SPL and Token-2022 transfer/mint/burn/delegate/revoke/authority/freeze/thaw, associated token accounts and extension-specific effects |
| Wallet and permissions | Connection/accounts/network changes, errors, permissions, exact message/typed-data/transaction signing requests and results, revocation and chain-switch invalidation |
| Application protocols | Versioned swap/liquidity/lending/liquidation/staking/reward/governance/oracle/NFT/bridge observations, with protocol-specific economics and origin/destination identity |
| Listener lifecycle | Subscribe/unsubscribe request/result, endpoint-local subscription identity, reconnect, error, cancellation and explicit coverage gaps; MPE private cancellation remains local |

Each event preserves source authenticity status, raw evidence digest, exact network identity, block/slot location, native commitment, adapter/decoder commitment and observed time. Native, decoded and derived claims remain distinct. A sender's decoded Swap or Final label cannot elevate evidence or permission. DeFi and bridge contracts require separate program/ABI, amount/fee/direction and finality policies; initiation is not completion.

Ethereum quantities use minimal RPC hex at the boundary and canonical unsigned decimal strings with uint256 bounds internally; byte DATA, addresses and hashes have distinct encodings. Solana uses exact decoded base58 public-key/signature lengths, canonical unsigned lamport/token amounts with field-specific bounds, cluster/genesis identity and mint decimals. Zero values are valid in these domains. Do **not** reuse the pilot's positive-only 18-digit decimal or whole-Share vocabulary. Full blocks/receipts/accounts/ABI objects need bounded projections, pages and explicitly authorized evidence retrieval; they do not automatically fit the selected MPE body class.

Acceptance work includes duplicate/out-of-order feeds, reconnect gaps, contradictory finality, reorg/rollback, failed execution with emitted diagnostic logs, changing token metadata/proxy programs, wallet rejection/chain switch, transaction version support and source projection loss. Observations are informational until a separate reviewed action contract satisfies current authenticated capability, freshness, evidence, state and durable replay policy. No chain RPC or signing call becomes executable merely by being in the catalog.
