# Validation formalization notes

The source of behavioral requirements is `model/validator.py`, with the current v0.2 schemas, trusted context fixture, example JSON, and `model/test_conformance.py`. This document records implementation decisions and checked results, not private reasoning.

The formalization uses decoded, typed payloads and integer timestamps. It separates executable branch checks from semantic predicates and proves acceptance implications for the constraints actually checked. A successful validation result describes an observation or candidate; it never performs execution.

The Python validator compares complete invoice observation records against trusted evidence, including status and timestamps. A `Final` record does not establish payment finality cryptographically, does not mean the invoice is fully paid, and does not authorize execution. Agent replay checks occur after current context validation: an old duplicate cannot bypass expiry or revocation.

The intended conformance bridge translates checked-in JSON examples and selected semantic mutations into Lean terms, checks those terms using Lean's kernel, and compares finite outcomes with Python. It does not verify JSON parsing, schema decoding, canonicalization, hashing, trusted-context authenticity, durable atomic storage, chain finality, or runtime implementation refinement.

## Checked implementation

`MidnightExpress/Validation.lean` provides independent semantic predicates and executable Boolean checks, with equivalence proofs for the common envelope/context gate and all three business branches. The overall validator is proved sound and complete relative to these predicates. This is a typed specification, not a proof that Python implements it for every possible input.

The specific corollaries establish:

- Successful validation and sequential replay results have `executes = false`.
- Accepted occurrences are not in the future, and the exact source principal and required role are present in trusted fixture context.
- Quotes match open trusted RFQ terms, assign distinct buyer/seller roles by requester side, preserve the asset/unit/currency price basis, and use a half-open validity interval. Cash equals the exact decimal product; a separate cross-multiplication theorem states the rational equality without rounding. Expired quotes are rejected.
- Invoice observations match the complete trusted evidence record, including status and timestamps. A final verdict requires a final evidence record. The positive fixture is a partial payment, so final observation is intentionally distinct from complete invoice settlement.
- Approvals match the current proposal and policy, exclude revoked actions, stay within proposal expiry, permitted targets, step budget, and one modeled effect. Revoked approvals are rejected.
- Unknown profile strings are rejected. Same occurrence/same digest is a duplicate event; changed digest conflicts. A new occurrence with the same action/intent is a duplicate action; changed intent conflicts. Every stateful check validates current context before consulting replay memory, so an invalid current input cannot become accepted by replay.

## Validation evidence

Commands run from the repository root:

```sh
/tmp/mpe-data-model-validation-env/bin/python formal/lean/check.py --update
/tmp/mpe-data-model-validation-env/bin/python formal/lean/check.py
```

Both completed successfully with the pinned Lean 4.34.1 toolchain. The normal command checks that `Examples.lean` still exactly represents current fixtures and mutations, then runs `lake build`. The result was **36 Python/Lean semantic cases (8 accepted, 28 rejected), plus 4 kernel-checked replay examples**. Examples use `by decide`; there is no `sorry`, `admit`, `axiom`, `unsafe`, or `native_decide` proof shortcut in the formalization.

The finite slice reads all five actual example JSON files and twelve checked-in negative fixtures. Additional cases exercise no trust, revocation, insufficient budget, role/principal failures, absent proposal, target/policy changes, exact start/end validity boundaries, opposite requester side, arithmetic overflow, rehashed proposal substitution, observation ordering, complete-evidence overpayment, future occurrence, and closed RFQ state. Four separate replay examples exercise occurrence and action equality/conflict paths.

## Trust and scope limits

The Python bridge is trusted test infrastructure. It translates selected already representable JSON values into typed Lean expressions and uses the Python implementation's proposal commitment computation to supply finite commitment observations. Lean proves the resulting typed cases. This is not verified JSON parsing, complete schema conformance, canonicalization, or SHA-256 correctness. Lexical failures (duplicate keys, Unicode, decimal-token grammar, calendar parsing, byte/depth limits) are outside this slice. Fixed typed enums cannot represent unsupported operations/currencies; their decode boundary is stated explicitly.

`Context` represents locally trusted test state, not authenticated external authority. Commitment functions and replay digest strings are parameters; no collision resistance or digest injectivity is assumed or proved. Replay memory is sequential and in-process; the proofs do not establish atomic durable authorization, distributed exactly-once execution, chain finality, or real tool/payment execution. Watch-control transitions and transport routing are outside these Lean modules.
