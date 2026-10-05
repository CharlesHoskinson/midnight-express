# Midnight Express semantic specification

This Lean 4 project gives executable definitions and machine-checked theorems for the three installed v0.2 data profiles. It models quotes, payment observations, sandbox approval candidates and replay decisions. Its inputs are decoded semantic values and an explicitly supplied trusted fixture context. Passing validation supplies evidence about those values; it does not execute a trade, payment or report write.

The pinned toolchain is `leanprover/lean4:v4.34.1`. Only Lean's bundled `Std` library is used; no external theorem library is downloaded.

```bash
cd formal/lean
lake build
```

The build imports all three source modules through [MidnightExpress.lean](MidnightExpress.lean):

| Source | Purpose |
| --- | --- |
| [Model.lean](MidnightExpress/Model.lean) | Profile commitments, envelope, typed payloads, exact decimal arithmetic, occurrence/action identities and structural business intent |
| [Validation.lean](MidnightExpress/Validation.lean) | Trusted-context acceptance rules and their safety properties |
| [Examples.lean](MidnightExpress/Examples.lean) | Executable examples and adversarial boundary checks |

The contracts in `Profile.contract` are copied exactly from [the installed profile lock](../../model/profiles/lock.json). Dispatch requires the profile, contract, event type, data schema, spec version and content type to agree. An unknown profile has no dispatch branch. `Operation` has only `writeReport`; its small wire-tag decoder returns `none` for every other string. Extension requires an explicit source change and new verification.

## Economic meaning

`Decimal` stores a natural-number coefficient and a scale. Its exact interpretation is coefficient divided by `10 ^ scale`. A field's acceptance rule requires a positive coefficient no greater than `999999999999999999` and the prescribed scale. Whole Share quantities have scale zero; USD amounts have scale two; Step budgets have scale zero. Scale and unit remain separate values so invalid combinations can be rejected.

`product_denominator` proves that coefficient multiplication and scale addition preserve the exact denominator. `whole_shares_times_cents` proves the result remains cents. `product_valid_iff_within_bound` proves that, once quantity and price are individually admitted, the precise product bound is the remaining condition for an admitted cash amount. No approximation or rounding is introduced. `requester_side_determines_distinct_roles` checks both BuyAsset and SellAsset perspectives.

An invoice observation carries all invoice terms, payment ID, amount, status, evidence clocks and rail. Pending, Final and Reversed are separate constructors. Matching trusted evidence concerns the complete observation, including status and amount. Even a Final result describes fixture evidence; it establishes no banking finality, accounting allocation or payment execution.

An approval carries the complete proposal, target, input digest, Step budget and expiry, plus the human, policy, authority domain, execution scope and budget window. Its stable action key is `(authorityDomain, executionScope, actionId)`. The business intent contains the source, event type, profile, contract and complete payload. Changing an occurrence ID/time leaves this intent unchanged. Changing a target preserves the action key while changing intent; changing a contract changes intent. These properties explain why a delivery retry cannot renew an action and why altered terms must conflict under its old key.

## Proof boundary

The model starts after JSON decoding. It does not implement or prove UTF-8 handling, duplicate-key rejection, exact coefficient-string grammar, identifier grammar, closed-object validation, calendar parsing, raw byte/depth/array/string limits, JCS serialization or SHA-256. The corresponding Python parser and JSON schemas remain necessary at the wire boundary. Integers model already checked UTC instants; they do not prove that any timestamp string denotes a valid calendar date.

Fixed wire tags such as Firm, AbsolutePerUnit, OffchainCoordinationOnly, Sandbox, USD and WriteReport are represented by restricted constructors or the type itself. The real decoder must reject every unsupported tag before constructing these values. Only the explicitly supplied small tag decoders are implemented here; a complete verified JSON-to-Lean decoder is future work.

The Lean intent is a complete structural value. The Python implementation uses JCS/SHA-256 fingerprints. No theorem assumes a collision-free hash or equates those implementations. Proposal digest comparisons rely on a supplied computation/evidence boundary; this project does not verify a cryptographic hash implementation, signatures, source authentication or trusted-context provenance.

The trusted fixture assumptions also include the clock, source roles/principals, RFQ state and terms, invoice/payment evidence, proposal and policy records, permitted humans/targets and revocations. Lean can prove consequences of the checked predicates; it cannot establish that these records describe the outside world. Authentication, fresh policy distribution, durable atomic replay, database recovery, remote effects and blockchain consensus require separate implementation and evidence.

Kernel-checked theorems apply to these Lean definitions. Concrete cross-language examples, where provided, are finite regression evidence. They do not constitute a general refinement proof of [the Python validator](../../model/validator.py), the Rust/TypeScript interpreters, subscriptions, chain observations or the Umbra recovery host. The 291-entry chain vocabulary is outside this three-profile model.

There are no project declarations using `sorry`, `admit`, `axiom`, `unsafe`, or an external proof oracle. Ordinary Lean kernel checking and the pinned compiler/standard library remain the trusted computing base.

## Recheck fixtures and proof assumptions

Run `python formal/lean/check.py` from the repository root in an environment with the model dependencies installed. It compares actual JSON examples and semantic mutations with the Python validator, checks that the generated Lean examples are current, then builds the full project. The translator and its external commitment computation are trusted test components; agreement covers this finite slice.

From this directory, `lake env lean Audit.lean` prints the kernel dependencies of the principal properties. The audit uses the standard Lean principles `propext` and, for rational arithmetic, `Quot.sound`. It introduces no project axioms.

## Extending the specification

The module interface is `namespace MidnightExpress`. `Model` owns data types and arithmetic/identity laws. `Validation` owns fixture context, executable gates and acceptance theorems. `Examples` exercises the public definitions. Preserve that dependency direction so the type model does not depend on its acceptance implementation.

When a reviewed contract changes, add or update its explicit profile definition and tests, explain the new assumptions, and rerun `lake build`. Keep historical released bundles immutable. A new operation, asset unit or payment status needs a defined semantic branch and corresponding rejection/acceptance properties; widening a decoder alone is insufficient. Supply synthetic contexts for checks. The build needs no credentials, secret imports, network service or external account.
