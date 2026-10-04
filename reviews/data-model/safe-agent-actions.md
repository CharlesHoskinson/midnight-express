# Safe agent actions: a closed contract and independent authority boundary

Research date: 2026-10-03. This is a proposed architecture and acceptance plan, not implemented security or a claim that an AI model is trustworthy. It applies to UC-05 and the RFQ/invoice workflows in the [selected stack](../../docs/product-requirements/recommended-stack-and-use-cases.md), extending the [event-contract review](event-contracts.md). Nine primary source documents were archived through Scrapling, with complete PDF extraction for LangSec and CaMeL. The [manifest](../../catalog/data-model/safe-agent-actions/manifest.json) records URLs, retrieval times, bytes/text hashes, and extraction methods. One additional Hardy source failed TLS verification and is not relied on. The LangSec public mirror has an incomplete certificate chain; its archival fetch explicitly disabled certificate verification and records that provenance limitation. Research hashes identify retrieved evidence; they do not establish publisher authenticity.

## Decision

Adopt a closed, typed command interface for effectful consumers. AI may interpret narrative to draft a proposal. A deterministic executor must never use an LLM, RAG retrieval, prose interpretation, model confidence, or a sender-supplied schema to determine the meaning or authority of an executable action. Unknown contracts, unknown command tags, unrecognized restriction fields, and unsupported versions produce no effect. Keep narrative and references as evidence for review; they cannot supply executable instructions or missing permissions.

The danger is broader than invalid JSON. A perfectly well-formed message can change a unit, currency, destination, profile, or condition while preserving shape. A legitimate signature can authenticate a proposal from someone without permission to execute it. An approved request can arrive after expiry, revocation, or a state change. Safe formats must therefore bind **shape, meaning, values, authority, freshness, destination, and replay scope**, with separate checks for each.

Use separate contracts for `ActionProposal`, `ActionApproval`, `ExecutionRequest`, and `ActionResult`. Sharing a correlation ID does not make them interchangeable. For the first pilot, authorize one exact action, rather than arbitrary scripts, shell commands, HTTP requests, natural-language tasks, or generic tool-name/parameter dictionaries.

## Primary evidence and its limits

| Primary source | What it establishes | Design consequence |
|---|---|---|
| Sassaman et al., [Security Applications of Formal Language Theory](https://langsec.org/papers/langsec-tr.pdf), §§5–6 and 9–10 | Input recognition and agreement between interpreters are security concerns; parse-tree differences can be exploited. Some overly powerful input languages make complete recognition intractable or undecidable. | Put bounded recognition before dispatch, minimize command expressiveness, and test Rust/TypeScript interpretation agreement. This does not prove that JSON Schema alone establishes safe business meaning. |
| Saltzer and Schroeder, [Basic Principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html), I.A.3 | Permission-based defaults, complete mediation, small mechanisms, privilege separation, and least privilege guide protection design; cached authority must track changes. | A proposal signer, approver, and executor have separate rights. Recheck policy at the effect boundary, including retry and recovery. |
| Saltzer and Schroeder, [Descriptor-Based Protection](https://web.mit.edu/Saltzer/www/publications/protection/Descriptors.html), II.A–B | Object designation and permission are distinct; capabilities must be protected against forgery. Dynamic sharing requires a trustworthy path for identifying intended principals. | A resource name or capability ID in JSON is merely a claim/reference. Resolve it under the authenticated principal and issue an enforced, narrowly scoped execution grant. |
| [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725), §§3.1, 3.8–3.12 | JWT validation must constrain algorithms, bind keys to issuers, validate audience, and prevent token substitution through mutually exclusive profiles. Token-supplied lookup URLs can cause SSRF. | Apply analogous type/domain/key/purpose checks to MPE authority assertions. This recommends principles, **not adopting JWT** or pretending its normative rules govern arbitrary MPE signatures. |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), §§3.1–3.2 and appendices D/E | JCS gives a specific canonical JSON encoding, rejects duplicate properties, restricts numeric representation, and preserves strings without Unicode normalization. | Canonical signatures need an agreed parser and value grammar. Canonicalization cannot resolve money units, identity meaning, or authority. |
| [RFC 7493](https://www.rfc-editor.org/rfc/rfc7493), §§2.1–2.3 | I-JSON constrains encoding/numbers and forbids duplicate names after escape decoding. | Reject ambiguous input before object parsing discards evidence. Use constrained strings for exact large values. Its general must-ignore recommendation is deliberately not used for actionable fields. |
| [JSON Schema 2020-12 core](https://json-schema.org/draft/2020-12/json-schema-core), §§6.5, 8.1.2, 11.3 | Unknown schema keywords normally annotate rather than enforce; required vocabularies matter; object closure must account for composition. | Install a reviewed schema closure with required dialect/vocabularies. Close nested objects and disjoint command variants. |
| [JSON Schema validation](https://json-schema.org/draft/2020-12/json-schema-validation), §§7.2, 9.2 | Format assertion is not generally enabled by default, and defaults are annotations. | Pin validator behavior; validate instants independently; prohibit coercion, default insertion, and unknown-field stripping in authority verification. |
| Debenedetti et al., [Defeating Prompt Injections by Design / CaMeL](https://arxiv.org/pdf/2503.18813v1), §§3–4, 6, 8 | A separate control/data-flow interpreter and capability policies can constrain an agent despite model susceptibility. The work states trusted-query assumptions and discusses misleading text, adoption, policy usability, and side channels. | Place enforcement outside the model and constrain disclosure as well as mutations. This narrower MPE command design does not implement CaMeL or inherit its benchmark/proof claims. |

The recommendations below are an MPE synthesis from this evidence, not requirements imposed by these papers on all systems.

## Concrete contract family

Preserve the existing encrypted CloudEvents-compatible event wrapper, semantic manifest binding, MPE EID, and whole-shard/local-recognition transport. Source/type/profile/roles/action IDs and approval references stay inside encryption. Admission proves admissible publication; decryption, group membership, persistence, and anchoring each remain insufficient authority for a business effect.

Every command profile is an installed immutable bundle: JSON Schema 2020-12 and transitive references, operation meanings, exact value/identity grammars, signature profile, state machine, adapter mapping, and negative vectors. Its manifest digest is the semantic contract identity. A version label or schema URL alone is insufficient. There is no runtime `$ref` fetch, sender-selected plugin, or dynamically evaluated policy language.

Define the following four disjoint event types with literal tags and closed nested objects:

| Type | Required role and contents | Permitted behavior |
|---|---|---|
| `ActionProposal/v1` | Proposer assertion; `proposalId`, typed action, evidence digests, requested validity, exact contract digest | Store, display, or reject. It cannot trigger the effect. |
| `ActionApproval/v1` | Approver assertion; exact proposal/action digests, `approvalId`, authorized actor, destination authority domain, policy digest/epoch, validity, consumption scope | Record a scoped authorization. It does not itself send a payment or acknowledge completion. |
| `ExecutionRequest/v1` | Authenticated requesting actor; exact immutable proposal and approval references/digests, action ID, destination domain | Ask the policy gate to execute the approved typed action after current checks. |
| `ActionResult/v1` | Executor assertion; action/request/approval digests, executor identity, destination evidence, bounded status, state/finality | Report an outcome. A result is neither a grant nor permission to compensate/retry. |

For a bounded coordination pilot, an illustrative action sum is:

```text
Action = AcceptQuoteV1 {
  quoteId, quoteIssuer, quoteDigest, termsDigest,
  buyerAccountId, executorId, destinationSystemId,
  baseAssetId, quantityCoefficient, quantityScale,
  quoteAssetId, maximumDebitCoefficient, debitScale,
  acceptanceDeadline, expectedQuoteRevision
}
       | PostInvoiceMatchV1 {
  invoiceIssuer, invoiceId, invoiceDigest,
  paymentEvidenceDigest, evidenceFinality,
  ledgerId, invoiceRevision, executorId, destinationSystemId,
  assetId, amountCoefficient, amountScale
}
```

These are proposed profile fields, not an existing wire standard. Every alternative has a fixed literal `operation` and exact contract digest. Coefficients are bounded unsigned decimal strings with no whitespace, exponent, leading zeros, or negative zero; scale is a small bounded integer under the profile's fixed asset conventions. Asset IDs include the issuer/network identity domain where needed. `AcceptQuoteV1` means off-chain acceptance in the initial pilot; settlement requires a separate operation and its ledger proof gates. `PostInvoiceMatchV1` records a match under ERP policy; it does not mean initiating payment.

Use `oneOf` branches whose literal operation tags are distinct, `required` fields, bounded arrays/strings, and closure at every level. Generate SDK types, but do not treat TypeScript compile-time types or Rust deserialization as runtime authorization. Unknown enum/command values never fall through to a generic handler. A documentation-only string may be permitted under an explicitly defined field; no open extension map is interpreted by execution. Adding a restriction to an older action changes the semantic contract and requires reviewed adoption, rather than silent ignore or a model-chosen migration.

## Bind exactly what is approved

Define an `ActionIntent` containing the action plus action ID, contract digest, deployment/network/tenant authority domain, authenticated actor, target/executor identity, resource version, and validity. Commit all authority-relevant external terms through immutable content digests; an action cannot mean “whatever this URL currently says.” Restriction and budget fields must live in this signed intent or in an exact digest-bound approval scope, never in prose that the executor searches for.

One implementable proposed digest grammar is `SHA-256(label || uint64_be(byte_length) || JCS_UTF8(intent))`, where the label is a fixed published ASCII protocol/purpose constant and the length measures bytes. Approval assertions independently bind this action digest, exact proposal digest, policy identity, approving principal/role, authorized actor, intended executor and destination, validity, and single-use scope. Signature fields are outside their own preimages. Separate purpose constants and validation rules prevent a proposal, receipt, approval, or different tenant's authorization from being substituted. Select keys/algorithms from a local allowlisted authority profile; a message cannot enable a weaker algorithm or nominate a trusted key server.

Use one fixed UTC representation and a real instant parser; JCS does not normalize timestamps. Display money with explicit asset, scale, direction, maximum total debit, and separately defined fees. If total debit includes fees, enforce that definition at the adapter; if fees cannot be bounded, the operation is unavailable. No conversion or default manufactures missing intent. The trusted approval UI renders the verified typed intent and exact terms, escapes all narrative, and distinguishes signed fields from model summaries. Editing amount, destination, unit, or terms produces a new action digest and fresh approval. A hidden field must not silently change the effect shown to the approver.

An approval signature proves who asserted a grant. Independently verify signer-to-role membership, whether that role may approve this operation/resource/budget, delegation limits, current revocation/freshness, separation-of-duty rules, and intended audience. Pin the approved policy digest, then require it to be currently accepted and apply current stricter restrictions; never silently reinterpret an old approval under changed policy. A policy change may force reapproval.

## Executor and capability boundary

1. Authenticate/decrypt and bounded-parse once. Reject duplicate decoded keys, invalid Unicode, prohibited number forms, overlong data, and excessive nesting before normal map deserialization. Enforce the pinned closed schema and deterministic semantic checks without coercion or stripping.
2. Verify the exact proposal and approval assertions, contract bundle, operation, actor, purpose, domain, target, terms, and digest equality. Check current capability and approval policy separately from signature validity. Quarantine unsupported or conflicting authority without any effect.
3. Resolve target/resource IDs through the installed adapter under the authenticated tenant/domain. Do not turn an ID into a generic URL, path, SQL expression, or shell string. Bind object revision or compare-and-swap preconditions to prevent target remapping and stale quote/invoice execution. Treat document/RAG results as untrusted data even when delivered by an authenticated connector.
4. Atomically reserve the approved budget and single-use approval/action identity, subject to current validity and revocation. Budget scope is `(tenant, actor, policy, asset, period)` or an equally explicit profile key; concurrent individually valid proposals cannot overspend an aggregate limit. Use integers with checked arithmetic. Refuse unknown asset conversion and enforce data-disclosure destinations too.
5. Pass an opaque local execution grant to a dedicated adapter holding only the necessary credentials. A serialized capability reference is not itself authority: the broker checks the authenticated caller, action digest, target, expiry, and consumption. The model never receives bearer credentials or unrestricted executor access. The adapter permits only its installed typed operation, with filesystem/network/process isolation appropriate to that operation.
6. Recheck validity/revocation at the declared effect linearization point. Queueing or approval arrival before expiry does not authorize a later send. Cancellation races must have an explicit outcome: accepted cancellation prevents a new effect; already committed effects require separately authorized compensation. Model narrative cannot cancel, revoke, or alter a grant.

For local effects, atomically commit effect, action-digest deduplication, budget consumption, result/outbox, and recovery progress in the destination database. For remote effects, a local transaction alone cannot establish once-only execution. Use destination idempotency bound to the same authority-domain/action ID and digest, and reconcile unknown outcomes before retry. If a destination lacks trustworthy idempotency/status reconciliation, do not enable automatic effectful execution there. Never release a reserved budget on timeout while the remote effect may have happened. A recovered worker must recheck authority before a genuinely new effect; querying the outcome of an already committed effect is a distinct bounded operation.

Keep statuses such as `accepted`, `rejected`, `dispatched`, `outcomeUnknown`, `committed`, and `finalized` distinct. An agent's “done” string or an MPE persistence acknowledgement cannot replace authenticated destination evidence. PostgreSQL/UmbraDB requires the proposed atomic effect/dedup/outbox capability or a verified caller composition; SQLite applies to standalone Rust clients. Neither storage choice automatically makes external APIs atomic.

On-chain effects retain the selected stack's finalized membership/authority policy, replay/nullifier consumption, exact carried-event/applied-phase checks when applicable, and CON-060 anchored-message binding. This contract proposal cannot replace those proofs. Event identity `(source,id)` and envelope EID are evidence identities; replay defense keys the business action at the destination authority domain.

## Adversarial acceptance matrix

Run these integration vectors in the actual Rust recognizer, TypeScript SDK, approval renderer, policy gate, and destination adapter. Passing model-output schema tests alone is insufficient.

| Mutation or race | Required outcome |
|---|---|
| Change coefficient, scale, asset/currency, debit direction, or fee convention after approval | Digest/signature or semantic-policy failure; zero effect. Test shape-valid mutations as well as malformed ones. |
| Replace destination, tenant, executor, authorized actor, account, network, or resource revision | Independent domain/target policy failure even for a syntactically valid, otherwise signed request. |
| Keep action bytes but change profile/version/schema manifest | Contract binding fails; no “closest supported” fallback. |
| Change `termsDigest`, invoice/quote/evidence digest, or content behind a reference | Exact commitments/preconditions fail; no model summary supplies equivalent meaning. |
| Expired approval arrives late; approval valid at receipt but expires in queue; revocation occurs before effect | Current effect-boundary checks refuse. Test controlled clocks, skew policy, and expiry boundary equality. |
| Reuse action ID with new event ID and newly sealed EID | Return prior authenticated outcome or reconcile pending outcome; never a second effect. Different digest under the same destination-domain/action ID is a conflict. |
| Duplicate keys, including `amount` and escaped `am\u006funt`; parser-dependent number/Unicode behavior | Reject before map parsing. Cross-language canonical bytes and UI values agree. |
| Add `requiresSecondApproval`, unknown `operation`, nested extension, absent required approval, or unasserted format | Refuse; no stripping, default insertion, command discovery, or generic handler. |
| Substitute signed proposal/result for approval; wrong-purpose or wrong-audience signature | Mutually exclusive authority validation rejects. |
| Valid approval signed by a role without spending rights; delegation widens target/budget | Independent role/capability and attenuation checks reject. |
| Many concurrent actions individually fit budget but collectively exceed it | Atomic reservation permits only the approved aggregate; crash recovery preserves reservations/consumption. |
| Prompt injection in quote text, invoice attachment, RAG excerpt, result narrative, or tool documentation | It may influence a draft but cannot widen operations, budgets, targets, disclosure recipients, or approval scope. Executor never interprets the narrative. |
| Target identity remaps or invoice changes after approval | Revision-bound conditional execution fails; refresh requires a new exact intent where semantics change. |
| Crash after remote effect but before result; timeout during dispatch; replay after restore | Destination idempotency/reconciliation governs; no blind resend or released budget. Protected restore preserves replay state. |
| Unknown result or premature/provisional payment evidence | No completion/finality inference, invoice posting, or compensation grant. |
| Cancel/revoke while dispatching; stale policy cached during redrive | Defined linearization outcome and current mediation; no new unauthorized effect. |

Property-based tests should generate one-field mutations of approved fixtures and parser-differential inputs. State-machine tests should explore duplicate delivery, concurrent approvals, retries, revocation, cancellation, and crashes around each persistence/effect boundary. Record exact preimages, validated values, decisions, and destination evidence privately without exposing credentials or creating plaintext business-routing headers.

## Scope and remaining risk

A closed grammar makes automated meaning and authority checks reviewable; it does not prove the proposal is wise, an invoice genuine, an approver attentive, a source honest, a sandbox perfect, or an adapter free of bugs. Schema-valid malicious proposals remain possible. Authentication only makes them attributable. Deliberately misleading summaries can still persuade a human, and authorized recipients can disclose received information. Information-flow controls require explicit policies and do not remove all timing/traffic side channels.

Keep the initial UC-05 pilot to a small installed operation set with trustworthy target identity, bounded total cost/disclosure, exact human approvals, and destination idempotency. Measure denial/ambiguity rate, approval comprehension, replay/expiry rejection, budget races, and recovery reconciliation. General tool ecosystems, arbitrary code, policy interpreters, automatic schema migration, and broad autonomous delegation need separate security designs; they are not implied by this pilot.
