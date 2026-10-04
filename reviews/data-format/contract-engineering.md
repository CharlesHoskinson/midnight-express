# Contract engineering review

Reviewed 2026-10-03 from the principal engineer perspective for contracts and schema evolution. Scope: `docs/product-requirements/unified-data-model.md`, the actual `model/schemas/` and `model/profiles/` artifacts, `model/{README.md,validator.py,build.py,test_conformance.py,requirements.txt}`, and `model/domains/`. No pinned artifact was edited or rebuilt. Findings below describe current behavior; all remediation is proposed.

## Decision

The implemented slice is a useful, closed Python reference model. It is not ready to serve as an interoperable contract distribution or execution boundary. Three reproducible issues contradict its own primitive/identity guarantees: terminal newlines survive ID and coefficient validation, fractional JSON numbers round into permitted constants, and duplicate logical actions leave new occurrence identities unrecorded. Fix these before treating the corpus as a normative reference for another implementation.

The broader design correctly separates proposals, observations, authority and effects, and explicitly defers production authentication, finality, durable replay and execution. Those deferred capabilities are prerequisites for deployment, not hidden functionality inferred from passing tests. The 267 chain catalog entries are proposed vocabulary metadata, not implemented payload contracts.

## Evidence and existing strengths

Executed the requested commands in the existing environment:

```text
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
PASS 51 checks; 3 schema self-checks; pinned local resources verified
Unsigned JSON example byte sizes: agent=1116, invoice-final=964,
invoice-pending=971, invoice-reversed=974, rfq=1252

/tmp/mpe-data-model-validation-env/bin/python model/domains/test_catalog.py
Proposed catalog: 267 entries; metadata only, no runtime contracts.
Ran 12 tests ... OK
```

These results establish those checks in one Python environment. They do not establish independent implementation agreement, signing, authenticated installation, effects, chain proofs or sealed wire fit.

Implemented strengths:

- All three schemas are standalone and close every object. Exact type/profile/schema constants and local lock matching reject unknown profiles and schema URLs. The present schemas contain no references; there is no transitive schema dependency to resolve today.
- `validator.py:61–68` constructs explicit domain-separated proposal and intent candidates. Intent contains source, type, profile, contract and complete typed data, with occurrence ID/time excluded intentionally. The data is an object, not a JSON string. The manifest graph is acyclic; raw resource hashes and JCS manifest hashes serve different documented purposes.
- `validator.py:16–45` rejects duplicate decoded keys, including escaped aliases, and checks UTF-8/surrogates and post-parse bounds. `Harness.check` applies a 3926-byte event limit before decoding. Decimal coefficients are strings, keeping intended financial magnitudes outside binary floating-point arithmetic.
- Source role/principal, exact trusted proposal/evidence, expiry and policy checks precede replay state mutation. Every successful return explicitly has `executes:false`.
- The catalog distinguishes native, decoded, derived and intent entries. Its checked inventory has 127 Ethereum and 140 Solana entries; all remain proposed and have no effect authority. Its README explicitly refuses to reuse the positive 18-digit pilot primitive for uint256/u64 chain quantities.

## Reproduced implementation defects

### P1 — Terminal newlines bypass supposedly exact primitive grammars

Locations: `model/build.py:17–23,79`; generated `model/schemas/rfq.v0.1.json:9,85,115,161`; `model/schemas/agent.v0.1.json:9,67`; `model/validator.py:100,157–159`. The schema regexes end with `$`. The installed Python validation path accepts a final LF before that anchor. No subsequent full-string validation covers IDs or coefficients. Python `int()` also accepts the whitespace.

Using an otherwise unchanged example and unchanged trusted context:

```python
agent['id'] += '\n'
Harness(context).check(json.dumps(agent))
# status: sandbox-candidate-only

rfq['data']['price']['value']['coefficient'] += '\n'
Harness(context).check(json.dumps(rfq))
# status: offchain-quote-valid
```

The event ID contains a character outside the declared grammar. The price coefficient is no longer a canonical integer string, yet arithmetic silently removes the whitespace. Its business commitment changes even though the numerical price remains the same. A stricter independent interpreter can reject both, producing divergent acceptance and commitment behavior.

**Proposed fix:** enforce full-string primitive matches in the semantic boundary and generate portable end-of-input schema patterns, with negative cases for LF, CR, CRLF and other whitespace on every primitive family. Do not fix this by inserting Python-only `\Z` into JSON Schema; a future Rust/TypeScript implementation needs an agreed grammar. Numeric conversion must follow successful exact lexical validation.

**Effort/acceptance:** small, 1–2 engineer-days including contract regeneration review. Both examples above must reject; unchanged positive examples and independently implemented grammar vectors must agree. New pinned commitments are required because the accepted language changes.

### P1 — Binary float parsing accepts disallowed and rounded numeric constants

Locations: `model/validator.py:28`; `model/build.py:16,19,39`; actual `model/schemas/agent.v0.1.json:69–71,119–121`; `model/profiles/rules.json` decimal restriction. Numeric constants do not establish a lexical integer-only rule. Python parses fractional/exponent JSON numbers to floats, and JSON Schema numeric equality accepts `0.0 == 0` and `1.0 == 1`.

Reproduced with unchanged trusted context:

```python
agent['data']['proposal']['budget']['scale'] = 0.0
agent['data']['maxEffects'] = 1.0
# status: sandbox-candidate-only, even with original proposalDigest
```

More significantly, replacing the raw token `"maxEffects":1` with `"maxEffects":1.0000000000000001` also returns `sandbox-candidate-only`; `raw_json` decodes the latter as `1.0`. The original noninteger value disappears before structural validation or JCS hashing. This conflicts with the rules' no-floats/no-rounding claim. The same parser helper returns positive infinity for `raw_json('1e999')`; rejecting literal `Infinity` through `parse_constant` does not catch numeric overflow. This last example demonstrates a parser-helper gap, not an accepted complete event or an execution bypass.

**Proposed fix:** decide and document whether these pilot profiles permit only lexical integer JSON tokens for numeric fields. Given the existing no-floats claim and the absence of legitimate fractional JSON fields, reject `parse_float` tokens at the raw boundary, retain bounded integer parsing and reject nonfinite values explicitly. Merely adding `type:integer` is insufficient: JSON Schema treats integral numeric values as integers, and information has already been rounded. If future profiles need fractional JSON numbers, specify their parsing and JCS number domain separately.

**Effort/acceptance:** small, 1–2 days. Add raw-byte negatives for `0.0`, `1e0`, `1.0000000000000001`, overflow and oversized integer tokens; retain coefficient strings. Two independent interpreters must agree on acceptance and exact canonical bytes, not just resulting mathematical values.

### P1 — New occurrences returning duplicate-action escape occurrence conflict detection

Locations: `model/validator.py:117–131`; `model/README.md` occurrence identity guarantee; `model/test_conformance.py:29–39` tests the initial replay but not subsequent changes to that replay occurrence.

Reproduced sequence in one harness, with the same trusted context:

```text
original agent occurrence                      -> sandbox-candidate-only
same agent data, id=event:replay                 -> duplicate-action
same event:replay, time=10:59:59 instead of 11:00 -> duplicate-action
(source,event:replay) present in h.events?      -> False
```

Both timestamps satisfy current checks. The second return occurs at line 129 before line 131 records the new occurrence. Consequently its changed canonical event cannot be recognized as an occurrence conflict; even an exact retransmission of that occurrence continues to be classified as duplicate-action. This is a deterministic bug within the stated in-memory model, separate from the acknowledged lack of durable/atomic execution state.

**Proposed fix:** after all validation, record a nonconflicting occurrence even when its business action is already present. Define the return precedence and whether rejected/conflicting occurrences enter a separate inbox audit record. Preserve action consumption behavior.

**Effort/acceptance:** small, less than a day plus pinned validator rebuild review. Above sequence must return candidate, duplicate-action, then `event-identity-conflict`; an exact replay of the second occurrence must return the documented duplicate-event status. Assert rejected input never consumes a new action.

## Contract mechanism and evolution risks

### P2 — Whole-source validator hashing couples independent contracts to implementation churn

Locations: `model/build.py:86–92`; each profile's `resources` map; `model/validator.py:8–9,50–51,70–81`; `model/README.md` executable-authority description; unified model document `:31–33` version separation.

Every manifest pins the same complete Python validator and rules file. Changing an invoice branch, a comment, CLI help or code formatting changes the validator hash, all three manifests and all event contract commitments. A proposal digest includes the resulting agent contract (`validator.py:61–62`), so even an invoice-only implementation change invalidates approval proposal digests. This is fail-closed and honestly documented as exact matching, but defeats the intended independence of workflow ownership and makes maintenance/migration expensive.

Conversely, the manifest does not pin Python, `rfc8785`, `jsonschema`, their transitive dependencies or their loaded code. `requirements.txt` pins two versions but is outside the committed resources and has no package hashes. Hashing the current `validator.py` file attests disk bytes, not the already imported program or dependency implementation. There is no demonstrated commitment-to-semantics equivalence across interpreters. This is a distribution/attestation limitation, not a claim that a hostile local administrator can be resisted by hashing files.

**Proposed approach:** separate immutable normative semantic contract IDs from implementation release attestations. Pin a bounded per-profile semantic specification, common primitive specification, canonicalization construction and test vectors; distribute approved implementation digests/dependency lockfiles as release evidence. Intent commitments should change for meaning changes under an explicit policy. Do not simply remove executable hashes while leaving their current authority claim intact.

**Effort/acceptance:** medium, roughly 1–2 weeks for the pilot plus independent implementation work. An invoice-only implementation correction must have an explicitly reviewed impact on agent/RFQ contracts. A Rust/TypeScript implementation must validate the same contract and reproduce published digest vectors without requiring byte-identical Python source. Packaging must identify reproducible dependency artifacts.

### P2 — Rebuilding overwrites a version name; historic contracts cannot coexist

Locations: `model/build.py:75–92`; `model/validator.py:70–81,96–100`; generated schema `$id` values; `model/profiles/lock.json`; unified model document `:33,55`.

The builder writes `rfq.v0.1.json`/equivalent and the lock in place. It can change accepted meaning while keeping profile name, version, schema URN and event type unchanged. Exact digests prevent silent acceptance, but the loader has one current digest per name. After a rebuild, an old event has no installed historical interpretation unless the whole directory/environment is separately preserved. Authorized migration, private negotiation, coexistence and active-workflow pinning are proposed prose, not implemented mechanisms.

**Proposed approach:** immutable content-addressed bundles, a reviewed installation allowlist keyed by contract commitment, explicit support/retirement metadata and workflow binding to a precise contract. Reserve named version/type identifiers for documented identity rules; reject accidental reuse in release tooling. An adapter is another versioned contract with source/target commitments and declared transformations/loss, not a default-filled schema upgrade.

**Effort/acceptance:** medium, 1–2 weeks for install/replay design and pilot tooling. Install old and new contracts together, replay an active old workflow correctly, reject an unsupported new contract and prove migration cannot refresh or duplicate an action. Semantic changes require a reviewed new contract even when JSON Schema compatibility appears additive.

### P2 — Trusted lock and schema closure remain operational assumptions

Locations: `model/validator.py:70–81,99–100`; `model/test_conformance.py` schema checks; `model/build.py:84–87`; `model/README.md` trusted-distribution boundary.

Today the reviewed lock and resources are local inputs; that is a reasonable fixture assumption. There is no authenticated installer, signer trust policy, rollback protection or immutable bundle snapshot. The loader verifies one read of a schema and later reads it again for validation, leaving a verification/use race under concurrent installation. `Path.is_relative_to(ROOT)` is lexical and does not prevent `..` components or symlink escape in a future manifest. The present reviewed paths are ordinary safe relative paths, so this is not a current sender-controlled traversal exploit.

The current files have no `$ref`; however production loading does not enforce that closure rule or supply an explicit offline reference registry. The test only searches serialized schema text for `$ref`, missing other reference mechanisms such as `$dynamicRef`, and does not define future transitive dependency policy. A reviewed future schema with external references could change the no-runtime-fetch behavior. Manifest schema/role/profile metadata is also trusted without a closed manifest schema and consistency checks.

**Proposed approach:** validate bundle metadata on installation, resolve/reject paths against a concrete bundle root, reject symlinks or constrain their resolved targets, verify/read immutable bytes once and validate from those bytes. For this pilot, forbid all reference keywords. If references become necessary, commit the entire resolved closure and use an offline registry with no network retrieval. Authenticate atomic installation and rollback policy before production use.

**Effort/acceptance:** medium, several days for a hardened local loader; distribution trust design adds 1–2 weeks. Tests must reject escaping paths, missing resources, manifest/schema disagreement and remote/dynamic references without any network activity. A concurrent installation must never mix verified old bytes with new validation bytes.

## Core duplication and catalog semantics

The nine envelope fields, `data`, schema URN, event type, profile name and contract digest are intentionally redundant. They give explicit discrimination and detect inconsistent sender declarations. Current schemas enforce the first three names through constants, while the loader enforces the digest. Retain that validation advantage. The builder already generates common fields once (`build.py:78–83`), then emits standalone files, which usefully avoids runtime transitive references.

There is nevertheless no independently committed common-core artifact or version policy: `core` is a manifest string (`build.py:90`), and all rules reside in one file. Proposed improvement: maintain one normative core/primitive definition and generate standalone profile schema closure from it, pinning its commitment in manifests. Add installation/build checks proving generated cores match, profile/type/schema/role metadata agree and every manifest schema is a pinned resource. Avoid introducing a remote shared schema simply to reduce generated repetition. Acceptance should demonstrate two genuinely independent profile implementations using the same bounded primitives; do not promote domain-specific payment/price/status fields into the core.

The domain metadata schema and tests enforce identity uniqueness, namespace agreement, coverage, no authority escalation and local provenance for derived claims (`model/domains/test_catalog.py:17–45`). They do not freeze historical meaning: an existing entry's `qualification`, `sourceStandard` or provenance can change while its `.v1` ID still passes every check. The explicit README requirement to use a new identity/version for incompatible meaning is currently governance prose. Proposed improvement: publish reviewed immutable catalog releases with digests and a semantic-diff review process; distinguish stable vocabulary identity from a future executable payload profile identity and from a concrete deployment/decoder version. Effort is a few days for release checks. Acceptance should flag changed meaning under an existing stable ID without treating harmless editorial/source updates as runtime authorization.

## Next engineering gate

First repair the three reproduced P1 defects, deliberately rebuild and review changed commitments, and publish raw-input acceptance/canonical-byte/digest vectors covering both positive and negative cases. Then implement an independent interpreter and two independently specified adapters before broadening profiles. Include occurrence/action replay sequences, strict primitive boundaries, Unicode/duplicate decoded keys, schema closure, profile mismatch, contract upgrades and historical replay. A second test suite importing the same Python validator is not an independent semantic agreement test.

Production remains gated on authenticated reviewed distribution, source/key/role binding, workflow state machines, current capability and revocation checks, durable atomic inbox/effect/outbox state, external idempotency/unknown-outcome reconciliation, and explicit transport/sealing overhead validation. Chain catalog promotion additionally requires exact network/deployment/decoder commitments and chain-specific evidence/finality contracts. These are proposed prerequisites, not implemented results of the successful reference tests.
