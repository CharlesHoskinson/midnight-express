# MPE bounded model v0.1

This is an experimental **data model and Python reference harness**, not an MPE runtime protocol, SDK implementation, standards implementation, authorization service or payment executor. Three closed profiles share a private structured CloudEvents-compatible core. Every example is unsigned. Production cryptography, authenticated source/role binding, finalized evidence, trusted clocks, permissions, durable atomic effect/replay state, and Rust/TypeScript agreement remain pending.

All event fields belong inside the existing MPE encrypted body. This model does not change outer transport fields, admission, EID or wire encoding. `application/cloudevents+json` identifies the structured event representation; its required `datacontenttype` is `application/json`. This stricter application profile deliberately rejects otherwise permissible CloudEvents extensions and representations.

## Artifacts and execution

- `schemas/{rfq,invoice,agent}.v0.1.json`: standalone JSON Schema 2020-12 resources, closed at every object, with no `$ref` or runtime fetch.
- `profiles/{rfq,invoice,agent}.v0.1.json`: local manifests pin raw schema bytes, shared normative `profiles/rules.json`, and the exact reference `validator.py` bytes. `profiles/lock.json` pins the JCS digest of each complete manifest. Treat the installed lock and artifacts as locally trusted, reviewed distribution inputs.
- `examples/`: five complete unsigned events (quote; final, pending and reversed payment observations; sandbox approval).
- `conformance/cases.json`: expected outcomes for 34 raw JSON corpus files, including examples. Duplicate-key cases deliberately contain invalid raw JSON object semantics.
- `conformance/trusted-context.json`: clearly labeled **trusted test fixture**, supplied separately from sender event bytes. It simulates clock, source role/principal bindings, RFQ state, exact invoice/payment records, proposed action, policy and human capability. It does not prove any of these facts.
- `test_conformance.py`: raw corpus plus state/context counterexamples; `validator.py`: local validation CLI/library; `build.py`: maintainer-only deterministic artifact builder.

From the repository root:

```bash
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
/tmp/mpe-data-model-validation-env/bin/python model/validator.py model/examples/agent.json --context model/conformance/trusted-context.json
```

A fresh environment can install `model/requirements.txt`. Normal validation never runs `build.py`. After an authorized model edit, rebuilding deliberately changes contract digests and regenerates examples; review those changes before distribution. Rebuilding is not a migration, authenticated installation or approval.

## Exact core and primitives

Each profile requires exactly `specversion`, `id`, `source`, `type`, `time`, `datacontenttype`, `dataschema`, `mpeprofile`, `mpecontract`, `data`. `specversion` is `1.0`; `mpecontract` is the locally pinned manifest SHA-256 digest; `dataschema` must be the exact installed profile URN. Unknown fields, schemas, profiles, digest mismatches and enum values reject, with no fallback or default insertion.

`source` has the closed ASCII grammar `urn:mpe:source:` plus 1–32 lowercase letters/digits/hyphens, beginning with a letter or digit. Business IDs use a named scope plus `:` and 1–64 lowercase ASCII letters/digits/dot/underscore/slash/hyphen, beginning with a letter or digit. Equality is exact string equality. These pilot IDs do not establish legal identity, wallet ownership or production asset registration.

An instant is exactly `YYYY-MM-DDTHH:mm:ss.000Z`, with a real Gregorian calendar parse and UTC timezone. Leap seconds, offsets, fractional alternatives, invalid dates and future occurrence times reject. Only whole seconds are supported in v0.1. The fixture clock is explicit, not trusted merely because a timestamp parses.

Decimals are `{coefficient,scale}`, sometimes with mandatory `unit`. Coefficients are positive canonical integer strings with 1–18 digits; no zeros, signs, leading zeros, exponent syntax, floating point amounts or silent rounding. Value is `coefficient × 10^-scale`. Scale is fixed by the field, so equivalent alternative precision is rejected. Quantity and Step budget have scale 0; USD price/cash/payable/payment amount have scale 2. This intentionally excludes fractional shares, zero-value invoices, multi-currency, fees, taxes, derivatives and arbitrary assets or tools.

The parser rejects duplicate decoded property names before normal object parsing, invalid UTF-8/surrogates, non-JSON NaN/Infinity, depth above 12, strings above 512 characters and arrays above 16 entries. The event body is bounded to 3926 raw UTF-8 bytes. This is a selected body constraint only: no sealing, signature overhead or class-2 wire acceptance is asserted.

## Three typed profiles

| Profile / exact event type | Required meaning | Successful result |
| --- | --- | --- |
| `rfq.v0.1` / `mpe.rfq.quote.v0.1` | An open trusted RFQ's single pilot asset for USD, whole Share quantity, requester side, distinct resolved buyer/seller, Firm absolute price per one matching asset Share, fees `None`, cash, validity, off-chain coordination marker | `offchain-quote-valid` |
| `invoice.v0.1` / `mpe.invoice.payment-observed.v0.1` | Exact trusted invoice parties/document/payable/currency plus a complete matching payment-evidence record, fixture rail, amount, effective/observed instants and `Pending`, `Final` or `Reversed` source status | `final-payment-evidence-only` or `payment-evidence-pending-or-reversed` |
| `agent.v0.1` / `mpe.agent.approval.v0.1` | Logical action ID, complete sandbox `WriteReport` proposal with target/input digest/Step budget/expiry, proposal digest, policy digest, named human, approval validity and `maxEffects:1` | `sandbox-candidate-only` |

RFQ roles are fixed from requester perspective. `BuyAsset` means requester is buyer; `SellAsset` means dealer is buyer. Price numerator is `iso4217:USD`; denominator is exactly one matching asset `Share`. Cash coefficient equals quantity coefficient times price cents coefficient, bounded to 18 digits. The sample is 100 Shares × 123.45 USD = 12,345.00 USD. No acceptance event, settlement policy or trade execution is implemented; `Firm` is an off-chain fixture description.

Invoice evidence must match the separately trusted complete source record; a sender cannot relabel pending evidence Final. Final remains a source assertion, not proof of settlement. Partial payment is supported; overpayment is outside this profile. No matching allocation, journal posting, reversal accounting, refund, tax calculation or payment execution occurs.

Approval checks exact proposal and policy, source principal/human binding, allowed human and sandbox target, Step budget and revocation. Changed target or input requires a different proposal; recomputing a proposal hash cannot bypass exact trusted proposal matching. Quote and approval validity use an exclusive upper bound: `validFrom <= now < validUntil`; approval expiry must not exceed proposal expiry. No action dispatch occurs after validation. Every returned result has `executes:false`.

## Commitments and identities

The reference computes `sha256:` plus lowercase hex SHA-256 over RFC 8785 JCS UTF-8 bytes of the following **unsigned intent candidate**:

```json
{"domain":"mpe.model.intent.v0.1","source":"<event source>","type":"<event type>","profile":"<mpeprofile>","contract":"<mpecontract>","data":"<complete typed data object>"}
```

The shown placeholders describe construction; actual hash input contains the complete object, never a serialized `data` string. `business_digest(event)` is authoritative executable construction. Occurrence `id` and `time` are excluded deliberately: resealing or emitting another occurrence cannot renew an action. Source, complete profile commitment and complete business intent are included. Narrative fields are absent. There is no signature field, signing algorithm, key binding or proof verifier; calling this candidate a verified signature would be incorrect.

`proposal_digest` hashes JCS of `{domain:"mpe.model.proposal.v0.1",contract:<mpecontract>,proposal:<complete proposal>}`. The manifest has no self digest; its resources have no manifest digest. Thus schema/rules/validator → manifest → local lock → event/intent is an acyclic commitment graph. Examples and corpus reference manifests but are outside the pinned manifest to avoid hash cycles. Test code and builder are not the semantic validation authority; `validator.py` and `rules.json` are pinned.

CloudEvents `(source,id)` identifies an occurrence. Same occurrence and same complete canonical event is a duplicate; changed content is a conflict. Logical approval action `(proposal.target,actionId)` identifies an at-most-one candidate in fixture memory. Same intent with a new event ID is `duplicate-action`; changed intent with the same action is a conflict. EID is an optional opaque harness argument kept separate, with no model interpretation or hash derivation. RFQ/payment observations never acquire effect IDs or execute effects.

The memory harness records only after checks; it is neither durable nor atomic and cannot supply production exactly-once effects. A production executor must recheck authenticated permission, revocation, trusted clock, input, target, budget, evidence and required ledger proof/finality immediately before committing a capability-bounded effect with durable replay state.

## Standards reuse and limits

Original narrow definitions adapt concepts from [CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core), [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), [FINOS CDM product concepts](https://cdm.finos.org/docs/product-model/) (units, price denominator, buyer/seller), and [OASIS UBL 2.3 Invoice concepts](https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html) (parties and payable amount). Source URLs and adaptation labels are also in pinned rules. This is original MPE application vocabulary, not copied full CDM/UBL schemas or a CDM, UBL, ISO 20022, FIX or FpML conformance claim. Distribution licensing review of any future imported/generated artifacts remains pending; no full standard is imported here.

Design evidence is the completed [event contracts](../reviews/data-model/event-contracts.md), [domain modelling](../reviews/data-model/domain-modelling.md), [financial semantics](../reviews/data-model/financial-semantics.md), [semantic constraints](../reviews/data-model/semantic-constraints.md), and [selected stack](../docs/product-requirements/recommended-stack-and-use-cases.md) reviews. No live schema lookup, RDF reasoner or LLM interpretation participates in validation. Python-only tests establish reference behavior; cross-language canonicalization, production cryptographic/finality/permission checks, adapters and MPE wire compatibility are pending.
