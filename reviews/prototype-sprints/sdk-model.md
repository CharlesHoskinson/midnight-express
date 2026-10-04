# Sprint 5: private SDK contracts and bounded model v0.1

Status: design plus executable Python **model** fixtures, 2026-10-03. This sprint owns `model/` and this review only. It does not implement the MPE runtime, cryptography, Rust/TypeScript SDK, adapter authentication, application capabilities or ledger effects. The selected [stack](../../docs/product-requirements/recommended-stack-and-use-cases.md) supplies the architecture; completed [event contracts](../data-model/event-contracts.md), [domain modelling](../data-model/domain-modelling.md), [financial semantics](../data-model/financial-semantics.md) and [semantic constraints](../data-model/semantic-constraints.md) reviews supply the design basis.

## Decision and concrete artifacts

Use a small private structured CloudEvents-compatible core with three separately pinned closed profiles. The implemented model provides one complete typed event per profile: single-asset/USD off-chain quote, invoice payment-status observation, and bounded sandbox human approval. Pending/reversed payment samples are separate observations of the same typed profile. Broader lifecycle events stay out until their guards have complete fixtures; no universal nine-message workflow is implied.

The [model README](../../model/README.md) defines every field, limit, outcome and commitment. [Schemas](../../model/schemas/), [local manifests and lock](../../model/profiles/), [unsigned examples](../../model/examples/), [raw conformance corpus](../../model/conformance/), [reference validator](../../model/validator.py) and [test harness](../../model/test_conformance.py) are real artifacts. `model/build.py` reproducibly generates schemas/manifests/fixtures for maintainer review; validation never generates or installs contracts.

The exact profiles are `rfq.v0.1`, `invoice.v0.1`, `agent.v0.1`; event types are `mpe.rfq.quote.v0.1`, `mpe.invoice.payment-observed.v0.1`, `mpe.agent.approval.v0.1`. Schema URNs and manifest hashes are mandatory and match local dispatch. Every object is closed, schemas have no external references, and runtime does not fetch, reason over RDF or ask an LLM to invent fields.

Manifests bind schema bytes, normative semantic rules and the exact Python validator. JCS/SHA-256 of each complete manifest is pinned in a local reviewed lock. The graph has no hash cycles: normative resources → manifest → lock → unsigned events/intents. Proposal commitments bind complete proposal plus profile contract; business intent binds source, exact type/profile/contract and complete typed data. No signature or proof exists here.

## SDK design boundary

The eventual Rust core/TypeScript-facing SDK should decode and locally dispatch exactly installed profiles after existing MPE recognition/decryption, then return a tagged typed value only after structural and deterministic semantic checks. Preserve raw original authenticated bytes separately from typed projection and envelope/EID evidence. Unknown/uninstalled contracts yield bounded unsupported/quarantine outcomes, without attempting coercion or supplying defaults.

Listener registration and event dispatch should expose `on`, `off`, `once` and cancellable bounded async iteration, while keeping application subscriptions local. Listener cancellation stops local delivery demand; it does not send a business selector to relays, undo a committed action or revoke approval. `once` selects one listener invocation, not at-most-once execution. One handler failure must not authorize automatic redrive, acknowledge another handler's business completion or erase another handler's cursor. These remain SDK design obligations, not Python harness tests or implemented APIs.

Distinguish event `(source,id)`, destination-scoped logical action, and opaque transport EID. A handler/AI may render evidence or propose a next action. An effect executor independently rechecks typed proposal, current authority, trusted evidence and replay state. Transport recognition, persistence, anchoring and validation do not create a business permission.

In this harness, the only approval outcome is `sandbox-candidate-only`. RFQ results are off-chain quote observations; invoice results preserve pending, reversed or final-source-evidence distinctions. All successful/duplicate results explicitly include `executes:false`. Reference context is labeled `trusted-test-fixture-only` and passed by the operator, never read from the event body. Missing evidence rejects. The in-memory dedup state is a test instrument, without production atomic/durable guarantees.

## Verification performed

Actual commands from the repository root:

```bash
/tmp/mpe-data-model-validation-env/bin/python model/build.py
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
/tmp/mpe-data-model-validation-env/bin/python model/validator.py model/examples/agent.json --context model/conformance/trusted-context.json
```

Build result: 3 complete JSON Schema 2020-12 resources, 3 pinned manifests, 5 unsigned examples, 34 raw corpus cases. Test result: **51 checks pass**, plus 3 JSON Schema self-checks and verification of locally pinned resource bytes. Example raw UTF-8 file sizes are RFQ 1252 B; invoice final 964 B; invoice pending 971 B; invoice reversed 974 B; approval 1116 B. Each is below the selected 3926 B body budget. This measurement includes the checked-in unsigned JSON only; it proves neither sealed class-2 wire fit nor signature/admission overhead acceptance.

Checks include price asset/unit mismatch, side reversal consistency, fixed precision, currency mismatch, unknown fee field/enum, cash mismatch and overflow, expiry at exclusive boundary, noncanonical decimals, invalid calendar/offset and ASCII identifiers, unknown schema/profile and bad profile hash, raw duplicate keys (including escaped equivalent keys), changed proposal target/input/policy, changed target with a recomputed valid proposal digest, missing trusted context, source principal/role mismatch, absent proposal/payment evidence, revoked approval, target/budget capabilities, pending-to-Final invention, identical event retry, conflicting occurrence, and same logical action with new event identity/EID. SellAsset also has a complete positive fixture transformation with matching trusted RFQ roles.

Dependencies used: Python 3 in the provided virtual environment, `jsonschema==4.26.0`, `rfc8785==0.1.4`, pinned in `model/requirements.txt`. Canonicalization uses the actual RFC 8785 package, rather than generic sorted JSON.

## Acceptance limits and next gates

The model demonstrates small complete deterministic fixtures across the three pilot domains. It does not inherit full CDM/UBL libraries or claim their compliance; original field/rule definitions adapt their unit, price denominator, party and payable concepts with source attribution in the README and pinned rules.

Remaining gates are independent Rust/TypeScript structural/semantic/JCS agreement; real authenticated source and human-role/capability bindings; production clock uncertainty and offline policy; payment adapter provenance and finality/reversal evidence; durable transactional replay/effect state; cryptographic signing/verifying and message/anchor/applied-phase binding; actual MPE sealing/admission wire measurement; listener isolation/cancellation/recovery behavior; governance and signed distribution of reviewed profile locks. No result in this sprint should be presented as satisfying those gates.
