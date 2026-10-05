# Verification bridge review: Python validator ↔ Lean semantic model

Reviewer: independent Claude Opus 5.5 instance, cross-language validation and verification role.
Baseline: commit `0dfee26`. No repository files were edited. All experiments live in `/tmp/mpe-lean-opus-review/verification-bridge/`. I did not read the other reviewers' reports or the Astra reports before writing this.

## Scope

I read `formal/lean/README.md`, `MidnightExpress/Model.lean`, `MidnightExpress/Validation.lean`, the generated `MidnightExpress/Examples.lean`, `Audit.lean`, `check.py`, `model/validator.py`, `model/test_conformance.py`, the conformance corpus, the three installed v0.2 schemas (via `load_profile`) and `model/bundles.py:load_bundle`. The questions were:

- Does the translator in `check.py` carry the JSON values into Lean faithfully?
- Do the generated cases actually exercise the Lean gates?
- Does replay behaviour agree across the two languages?
- Does the build gate detect proof regressions?
- What is the next verified boundary that is practical to build?

## Evidence and commands actually run

Everything ran from `formal/lean`, using `/home/hoskinson/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lake` and `/tmp/mpe-data-model-validation-env/bin/python`.

| Check | Command (abridged) | Result |
| --- | --- | --- |
| Generated examples are current | `stale.py` imports `check.collect/generate` and compares with `Examples.lean` (no `--update`) | Identical. 36 cases: 28 reject, 8 accept |
| Build is current, without writing | `lake build --no-build` | `All targets up-to-date (6 jobs)` |
| Named axiom audit | `lake env lean Audit.lean` | 16 theorems. Only `propext`, plus `Quot.sound` for `accepted_quote_rational_cash` |
| Whole-namespace axiom audit | `lake env lean audit_all.lean` (metaprogram over every `MidnightExpress.*` constant) | 884 declarations, none outside `propext`/`Quot.sound` |
| Per-condition coverage of the 36 cases | `conjuncts.lean` imports `MidnightExpress.Examples` and evaluates each atomic gate condition on `context{i}`/`event{i}` | See the coverage finding below |
| New targeted cases, kernel-checked | `diff.py targeted`, then `lake env lean targeted.lean` (37 `by decide` examples) | Exit 0. Python and Lean agree on all 37 |
| Randomized differential | `diff.py fuzz N seed` with N=400 (seed 20261005) and N=1500 (seeds 1, 2, 3), then `#eval` in Lean | 4,900 cases, 0 mismatches, 0 untranslatable |
| Stateful replay differential | `stateful.py 400 7` and `stateful.py 400 8`: Python `Harness` sequences against a Lean `check` fold with the Python digests | 800 sequences, 3,185 steps, 0 mismatches |
| Bridge theorems (feasibility) | `lake env lean bridge_theorems.lean` | Compiles. Axioms `[propext]` and `[propext, Quot.sound]` |
| `sorry` behaviour | `lake env lean sorry_only.lean` | Warning only, exit 0 |
| Escape fidelity | `#eval "x\by"` | Lean rejects the `\b` escape (`invalid escape sequence`) |

One harness mistake is worth recording. My first stateful run reported 70 mismatching sequences. The cause was a stale loop variable in my scratch generator, which gave every step the same digests. After the fix there were 0 mismatches. It was not a model defect.

The randomized and stateful runs use `#eval`, which is compiled evaluation, not kernel checking. The 37 targeted cases use `by decide`, the same as `Examples.lean`.

## Strengths worth retaining

- Each gate has two forms: an executable Bool gate (`rfqCheck`, `invoiceCheck`, `approvalCheck`, `commonCheck`) and a separate Prop specification, linked by `_iff` theorems (`Validation.lean:112,137,156,186,211`). `validation_sound` and `validation_complete` then give an exact characterisation of `validate`. This is the right structure for a reference oracle.
- `check.py` asserts the Python verdict against the expected label before it emits each Lean example (`check.py:184-188`). Lean is then kernel-checked against the same label. A divergence therefore fails loudly in one direction or the other. The script uses `by decide` throughout and never `native_decide`. It also refuses to run when `Examples.lean` is stale.
- The fixtures are real `model/examples` and conformance JSON, not hand-written Lean values.
- The `Profile.contract` strings are guarded transitively. Each profile has an accepting fixture that carries the `lock.json` commitment, so a contract change breaks a `decide`.
- The replay control flow agrees with `Harness.check`, including two cases: occurrence precedes action, and a duplicate action still records the new occurrence. The stateful differential found no divergence.
- The project has no axioms beyond `propext`/`Quot.sound` across all 884 constants, not just the 16 that `Audit.lean` lists.

## Confirmed findings, prioritized

### The cross-language slice tests only 16 of 54 gate conditions in isolation

Severity: medium-high. Location: `check.py:collect` (lines 122-174), against `Validation.lean:100-188`.

I split the gates into 54 atomic conditions: 11 common, 16 RFQ, 8 invoice and 19 approval. For each of the 36 generated cases I recorded which conditions are false. Deleting a condition from `validate` changes an example's outcome only if that condition is the sole failure in some case. Results:

- 16 conditions fail alone in some case, so their deletion would be caught.
- 9 conditions fail only together with others: `c.sourceKnown`, `c.sourceRole`, `c.contract`, `c.notFuture`, `q.buyer`, `q.seller`, `q.occurred≤validFrom`, `a.digest` and `a.human`.
- 29 conditions are never false in any case. These include semantically material checks that `validator.py` also performs:
  - quote not yet valid (`q.validFrom ≤ now`)
  - approval `occurred ≤ validFrom`, `validFrom ≤ now` and `validUntil ≤ proposal.expires`
  - `executionScope`, and the context `budgetWindow`/`authorityDomain`
  - invoice terms against the trusted invoice (`i.terms`)
  - invoice `effectiveAt ≤ observedAt`
  - `buyer ≠ seller`
  - envelope `specversion`, `datacontenttype`, `type` and `dataschema`
  - every `ValidAt` scale and bound condition, and the `rail`, `maxEffects`, `baseQuantity`, share-unit, step-unit and literal-domain/window conditions

So 38 single-condition deletion mutants of `validate` survive the generated suite. Some would happen to break a positional projection in a theorem (see the brittleness finding below), but nothing makes that reliable.

The comment at `check.py:133` ("omits lexical/schema-only failures that typed decoding cannot represent") is broader than the facts. Of my 37 targeted cases, 20 are rejected by Python at the schema or bundle level, yet their fields are fully representable in Lean and Lean rejects them through its own condition. Examples: price scale 3, a cash coefficient above 10^18-1, baseQuantity 2, a zero amount, rail `other-bank-v1`, maxEffects 2, a Share-unit budget, a wrong `dataschema`, specversion `1.1`, and an uninstalled contract. Only wire tags outside a singleton type (EUR, `Token`, an unknown operation or fee) are unrepresentable.

Proposed change: add the 37 mutations in `/tmp/mpe-lean-opus-review/verification-bridge/diff.py` (the `MUT` list) to `collect()`. Then add a generated isolation check: for each condition name, at least one case has that condition as its only failure. Two conditions would be declared exempt:

- `c.sourceKnown`, because an absent source necessarily fails role and principal too.
- `q.price.currency = q.terms.currency`, which can never be false because `Currency` has the single constructor `usd`.

Acceptance test: with the targeted cases added, my scratch run isolates 52 of 54 conditions, and only the two exempt ones remain. The guard would make `check.py` fail if a future gate condition has no isolating case. Tradeoff: 37 more `decide` examples. My `targeted.lean` checks in about 6.6 s wall-clock. The isolation check needs a condition list that mirrors the gates. Keeping it as a Lean `List (String × Bool)` next to each gate is the cleanest option.

### Replay is not tested across languages, and `check` is detached from the structural intent

Severity: medium. Location: `Validation.lean:277-284` (`check` takes free `eventDigest`/`intentDigest : String`), `check.py:193-201` (four hand-written token examples), `Model.lean:260-273` (`BusinessIntent`, `Event.intent`).

The four replay examples in `Examples.lean` use the abstract strings `"whole1"` and `"intent"`. Python never runs them. `test_conformance.py` contains replay sequences, but they are not translated: duplicate-event, duplicate-action, a conflict after a changed `validFrom`, and stale time after a duplicate.

Separately, nothing in Lean links the `intentDigest` argument of `check` to `Event.intent`. The Model theorems `occurrence_metadata_does_not_refresh_intent` and `changed_target_changes_intent` therefore never reach the replay machine, and the README's explanation of why a delivery retry cannot renew an action is only informal. My stateful differential (3,185 steps, 0 mismatches) shows that the behaviour agrees today. The gap is in coverage and in proof, not a known defect.

Proposed change:

1. Have `check.py` replay the `test_conformance.py` sequences, plus seeded random sequences, through `Harness`. Emit Lean `decide` examples over a `check` fold, passing the real `digest(e)` and `business_digest(e)` strings. `stateful.py` is a working prototype.
2. Add theorems that take digest functions `H₁ : Event → String` and `H₂ : BusinessIntent → String`. I compiled these in `bridge_theorems.lean`:
   - `same_intent_new_occurrence_duplicate`: a validated agent event whose intent equals a remembered intent, on a fresh occurrence key, is classified `.duplicateAction`.
   - `redelivery_duplicate_action`: the corollary for any id/time change, via `occurrence_metadata_does_not_refresh_intent`.
   - `changed_intent_same_key_conflicts`: with `Function.Injective H₂`, the same action key with a different intent gives `check = none`.
   - `changed_target_conflicts`: the corollary using `changed_target_keeps_action_key` and `changed_target_changes_intent`.

Acceptance test: these four theorems in `Validation.lean` (or a new `Replay.lean`), listed in `Audit.lean`. The generated sequence examples must agree with `Harness` statuses. Tradeoff: injectivity of `H₂` is an explicit hypothesis, which is honest for SHA-256. Nothing is assumed globally.

### The build gate accepts `sorry`, and the audit only reports

Severity: medium. Location: `check.py:224` (`subprocess.run([lake, 'build'], ..., check=True)`), `Audit.lean`.

A `sorry` produces a warning and exit status 0. I confirmed this with `lake env lean sorry_only.lean`; `lake build` relays the same warning. `Audit.lean` prints axioms for 16 named theorems but asserts nothing, and it does not cover other theorems such as `dispatch_iff_exact_envelope`, `product_valid_iff_within_bound`, `accepted_quote_exact_decimal_product` or `revoked_approval_rejected`. The `example`s in `Examples.lean` are anonymous. They are not in the environment, so no axiom audit can reach them, and only warnings would reveal a `sorry` there. The README states that the project uses no `sorry`. Today that holds (884 declarations audited), but nothing enforces it.

Proposed change: run `lake build --wfail` (the pinned Lake lists that option). Turn `Audit.lean` into a failing check: iterate all `MidnightExpress.*` constants with `collectAxioms` and `throwError` on anything outside `{propext, Quot.sound}`. `audit_all.lean` is a 15-line working version. Have `check.py` run it.

Acceptance test: adding `theorem t : False := sorry` anywhere, or a `sorry` inside a generated example, makes `check.py` exit non-zero. Tradeoff: `--wfail` also fails on linter warnings, so any existing ones must be cleared first. I could not see the current warning set without rebuilding, which I avoided.

### The translator is lossy and has no fidelity check

Severity: low-medium. Location: `check.py:36-37` (`decimal`, `int(d['coefficient'])`), `check.py:72-102` (`event` reads a fixed key list), `check.py:23-24` (`string` via `json.dumps`).

- Python's `int()` accepts `"0100"`, `" 7 "`, `"1_000"` and non-ASCII decimal digits, and maps each to a canonical `Nat`.
- `event()` silently ignores any data key it does not read.
- `json.dumps` can emit `\b` and `\f`, which Lean string literals reject. I confirmed that this fails closed, as a compile error.

Today this is safe. Only cases whose label Python confirms are emitted, and a lossy translation of a Python-rejected lexical case would make Lean accept it, so `decide` would fail. The translation is still not shown to be injective, and schema evolution could drift silently. If v0.3 adds a compared data field, Python would check it and Lean would never see it.

Proposed change:

- `fullmatch` every coefficient against `[1-9][0-9]{0,17}|0` before `int()`, with `0` admitted deliberately so representable negative cases stay possible.
- Track which keys were consumed, and raise if the event or data contains an unread key.
- Add an inverse renderer: convert the emitted Lean value back to JSON, re-inserting the constructor-fixed tags, and assert equality with the input.

Acceptance test: a fixture with an extra `data.memo`, or a coefficient `"0100"`, makes the translator raise. All 36 current and 37 proposed cases still round-trip. Tradeoff: about 40 lines of Python. Pure-lexical negatives stay out of the bridge until a Lean decoder exists.

### Some named cases do not isolate what their names say

Severity: low. Location: `check.py:158-161` (`cash_overflow`), `check.py:170-171` (`future_occurrence`), corpus `profile-hash`.

- `cash_overflow` changes the quantity but not the cash, so it fails only `q.cashProduct`. The 18-digit cash bound (`q.cash.ValidAt 2`) is never falsified in the existing suite.
- `future_occurrence` uses an RFQ. There, `occurred > now` also violates `occurred ≤ validFrom ≤ now`. For RFQ and approval events the common not-future check follows from the profile conditions, so only invoice events exercise it, and the suite has no invoice future case.
- `profile-hash` fails both `c.contract` and `a.digest`.

Proposed change: add `q_cash_product_above_bound`, `i_future_occurrence` and `env_contract_alone`, which are already in the targeted set, and rename or annotate the existing ones. Optionally prove `SemanticValid c e → e.payload ≠ .invoice _ → e.envelope.occurred ≤ c.now` to document the redundancy. Acceptance test: the isolation check from the first finding.

### Positional projections make the theorems brittle

Severity: low (maintainability). Location: `Validation.lean:252` (`hs.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2`), `268`, `274`, `295-296`, `302-304`, `325-326`.

Inserting a condition into `RFQValid` or `ApprovalValid` silently shifts these indices. The result either breaks unrelated proofs or, if the types happen to line up, makes a theorem project a different condition.

Proposed change: declare `RFQValid`, `InvoiceValid` and `ApprovalValid` as `structure ... : Prop` with named fields (`openTerms`, `fromLeNow`, `untilLeExpires`, ...). Keep the Bool gates and the `_iff` theorems, using anonymous-constructor proofs. Acceptance test: all current theorems restated with field access, and `Audit.lean` unchanged. Tradeoff: somewhat longer `_iff` proofs. The isolation check from the first finding could then reuse the field names.

### The profile fingerprint guard is only transitive

Severity: low. Location: `Model.lean:15-34,46-49,99`, `Validation.lean:146,169-170`, against the installed schemas.

Only the contract strings are tied to `lock.json`, and only through accepting fixtures. The following are not compared with the bundle anywhere:

- `eventType`, `dataSchema` and the role mapping
- `maxCoefficient`, which the pattern `[1-9][0-9]{0,17}` implies
- the `rail`, `authorityDomain` and `budgetWindow` literals
- the `maxEffects` and `baseQuantity` constants and the decimal scales

A contract change forces someone to edit Lean, but nothing checks that they updated these literals. I checked them all against the schema dump: they currently match.

Proposed change: have `check.py` emit generated `example : Profile.rfq.eventType = "<schema const>" := rfl` lines, plus one for each literal, extracted from `load_profile(...)['schemaObject']` and `lock.json`. Acceptance test: changing any one schema constant in a scratch copy of a bundle makes the guard fail and name the field. Tradeoff: the extraction code depends on the schema layout. If the layout changes, the guard should fail rather than silently skip.

### The commitment oracle is derived from the event under test

Severity: low. Location: `check.py:107-112`.

Each generated context sets `proposalDigest := fun p contract => if p = <this event's proposal> ∧ contract = <this event's contract> then <python digest> else ""`. At that point this matches `validator.py:178` exactly. However, the "trusted" commitment function changes from case to case, and it returns the sentinel `""` everywhere else. No current case can exploit this, because the schema forbids an empty digest. Still, Lean never checks a context whose commitment is fixed independently of the input.

Proposed change: build one finite commitment table per run, covering every proposal that appears in the context or in any event, and reuse it across cases. Keep injectivity as an explicit theorem hypothesis, as in the replay finding. Acceptance test: the 36+37 cases pass with the shared table.

### README wording on `Quot.sound`

Severity: informational. Location: README, "Recheck fixtures and proof assumptions".

The README attributes `Quot.sound` to "rational arithmetic", but the model has no rational type. `accepted_quote_rational_cash` is a `Nat` cross-multiplication, and `Quot.sound` comes from standard-library lemmas that `rw`/`simp` use. Suggested wording: "Some proofs depend on `Quot.sound` through standard library lemmas."

## Proposed coverage and next verified boundaries

These are ordered by value for effort.

1. Add the targeted cases and the isolation check (first finding), plus `--wfail` and the failing whole-namespace audit (third finding). Both are cheap and close concrete gaps.
2. Generate replay sequences from Python and add the four bridge theorems (second finding).
3. Make the translator strict, add the round-trip check, and generate the profile fingerprint guard (lossy-translator and fingerprint findings).
4. Run the seeded differential in CI. `diff.py` with a fixed seed and N around 1,000 takes a few seconds per side. Report any mismatch as a minimized case and promote it to a `decide` example. The mutation menu should grow beyond my 37 targeted mutations and time shifts. In particular, add string-identity swaps across fields, context-list membership edits and coefficient boundary values (1, max, max+1).
5. Next verified parsing boundary, in increasing cost:
   - `parseCoefficient : String → Option Nat` for `[1-9][0-9]{0,17}`, with round-trip (`parse (render n) = some n` for valid `n`) and canonicality (`parse s = some n → s = render n`) theorems. This removes the trusted `int()` from the semantic bridge.
   - `parseInstant` for the fixed `YYYY-MM-DDTHH:MM:SS.000Z` grammar, with calendar validity and an order-preservation theorem: for canonical strings, lexicographic order equals `Int` order. This replaces the `strptime` in `check.py:instant`.
   - A closed-object decoder from a minimal JSON value type to `Event`, with a theorem that decoding success implies every key was consumed and every tag decoder succeeded. The existing `decodeProfile`/`decodeOperation`/`decodeUnit`/`decodePaymentStatus` slot in directly. Lean core's `Lean.Json` would conflict with the README's Std-only stance, so a 60-line local AST is probably simpler. Once this exists, the Python translator is no longer trusted for semantic fields. Parse the raw fixture bytes on both sides and differential-test the lexical corpus too (duplicate-key, decimal-exponent, timestamp-offset, non-ascii-id, calendar), with only the JSON tokenizer remaining outside the proof.

## Deliberate deferred boundaries (not defects)

The following are outside the claimed scope, and the README states so:

- raw JSON/UTF-8 handling, duplicate keys and the depth/length/array bounds (`validator.py:16-49`)
- JCS and SHA-256 (`validator.py:51-52`)
- bundle integrity (`bundles.py:51-76`)
- calendar validity
- authenticity and provenance of the trusted context
- durable or atomic replay storage
- the Rust and TypeScript interpreters

The context passed to `Harness` is itself unschematized. For example, `c['humans']` as a string would give substring membership at `validator.py:183`. That is acceptable for a trusted test fixture, but a context schema would be a cheap hardening step on the Python side.

## Conjecture and unconfirmed items

- I believe `lake build --wfail` will pass on the current tree, but I did not confirm it, because that requires a rebuild.
- I expect the differential mutation menu to find no mismatch in the remaining unexplored dimensions (string swaps between fields, list-valued context edits). That is untested.
- Moving `RFQValid` and the other predicates to named `Prop` structures should not break `decide` on the examples, because the Bool gates stay unchanged. I have not tried it.

## Proof boundary, restated for the bridge

What is proved: the kernel-checked `_iff`, soundness, completeness, non-execution and replay-conflict properties about the Lean definitions, plus 36 finite examples. My scratch work adds 37 more examples and the four replay-to-intent theorems.

What is tested but not proved: Python/Lean agreement on 36 (and in scratch 37 + 4,900 + 3,185-step) translated cases.

What is trusted: `check.py`'s translator, Python's `int`/`strptime`, the per-case commitment oracle, and the Lean kernel and compiler. `#eval` results are additionally trusted to the compiler.

What is not addressed: refinement of `validator.py`, which no finite suite gives.

## Unresolved questions

1. Should the bridge's job be stated as "conjunct-complete" (every Lean gate condition has an isolating cross-language case), so that `check.py` can enforce it, or does the maintainer prefer a smaller representative slice?
2. Should representable schema-level failures (scale, bound, singleton literal and envelope constants) count as part of the semantic model's claimed scope? The Lean gates already enforce them, which suggests yes. The `check.py:133` comment suggests no.
3. Is the Std-only constraint firm? If `Lean.Json` were acceptable, the verified decoder in item 5 of the coverage plan becomes considerably cheaper.
4. For replay, should the Lean model store structural `Event`/`BusinessIntent` values and treat the hashed Python store as a refinement under injectivity, or keep string digests with explicit `H₁`/`H₂` parameters as in my scratch theorems?
