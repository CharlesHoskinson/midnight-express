# Model fidelity review: Lean v0.2 semantics against the Python reference

Reviewer: independent Claude Opus 5.5 reviewer (data model and economics). Baseline commit `0dfee26`. Review only: no repository source, generated example or `.lake` file was changed.

## Scope

I compared `formal/lean/MidnightExpress/Model.lean` and `Validation.lean` against `model/validator.py`, `model/bundles.py`, the three installed schemas (`model/schemas/*.v0.2.json`), `model/profiles/{lock,installed,rules}.json`, the five model examples, `model/conformance/trusted-context.json`, `formal/lean/check.py`, the generated `Examples.lean`, `docs/product-requirements/unified-data-model.md`, `model/README.md` and the website specification page. I read the earlier Astra notes (`astra-model.md`, `astra-validation.md`) as evidence. I did not read other reviewers' reports.

The question was whether, after JSON decoding, the Lean acceptance predicate admits or rejects the same decoded semantic values as the Python validator, and whether the claimed economic and identity properties hold within their stated scope. Raw JSON grammar, lexical identifier patterns, calendar parsing, JCS, SHA-256, signatures and context provenance are acknowledged boundaries. I treat them as roadmap items, not defects.

## Evidence and commands run

All scratch files are under `/tmp/mpe-lean-opus-review/model-fidelity/`.

- `lake env lean Audit.lean` (cwd `formal/lean`). All 16 audited theorems depend only on `propext`, plus `Quot.sound` for `accepted_quote_rational_cash`. No project axioms.
- `lake env lean /tmp/mpe-lean-opus-review/model-fidelity/Scratch.lean`, exit 0. The file imports the compiled `MidnightExpress.Examples` and contains reproducers A and D and the proofs E and B described below. All are checked with `decide` or ordinary tactics; there is no `native_decide` or `sorry`.
- `/tmp/mpe-data-model-validation-env/bin/python repro.py` exercises the real `Harness` on fixture mutations. Output:
  ```
  quoteId-conflict offchain-quote-valid offchain-quote-valid
  payment-double final-payment-evidence-only final-payment-evidence-only
  cumulative-overpay final-payment-evidence-only final-payment-evidence-only
  final-then-reversed final-payment-evidence-only payment-evidence-pending-or-reversed
  budget-window ['sandbox-candidate-only', 'sandbox-candidate-only', 'sandbox-candidate-only']
  reissued-same-key sandbox-candidate-only reject:action-identity-conflict
  examples-current True
  ```
  `examples-current True` means `check.generate(check.collect())` matches the checked-in `Examples.lean` byte for byte. I compared in-process and did not run `check.py`, because that script invokes `lake build`.
- `lockdiv.py` runs against a scratch copy of `model/{profiles,bundles,examples,conformance}` with `validator.ROOT` pointed at the copy. It publishes a second `rfq.v0.2` conformance bundle there and validates the RFQ example under both contracts. Both return `offchain-quote-valid`, and `lock.json` still names only the original contract.

## Field-level fidelity summary

Every non-constant wire field of the three `data` objects has a Lean counterpart. Fixed tags (`kind`, `quoteKind`, `settlement`, `fees`, `environment`, `operation`, the currency, and the `Share`/`Step` units) are encoded by single-constructor types or restricted enums. That is a legitimate decoding boundary.

The semantic gates match Python conjunct for conjunct:

- RFQ: the RFQ is open, the six terms match, buyer and seller follow from the requester side and differ, the price basis matches, time is half-open, and cash equals the coefficient product within the 18-digit bound.
- Invoice: the invoice terms match, the payment evidence equals the complete observation, `effectiveAt ≤ observedAt ≤ occurred`, and `amount ≤ payable`.
- Approval: domain, scope and window match, the proposal digest matches, the proposal and policy match, the human is permitted and the action is not revoked, `occurred ≤ validFrom ≤ now < validUntil ≤ expires`, and the target and Step budget are permitted.

Lean also re-checks several values that Python leaves to schema constants: `baseQuantity = 1`, `maxEffects = 1`, the authority domain and budget window constants, `rail`, and the scales. Lean is no weaker on any of them. The check order differs: Python checks role and principal before semantics, and its proposal hash before lookup. This changes only Python's error codes, which Lean does not model, not the accepted set.

## Strengths worth retaining

- Every executable gate has a separate `Prop` specification with a proved `_iff` lemma, and `validation_sound`/`validation_complete` connect them. This is the right shape for later refinement work.
- The arithmetic is exact. `accepted_quote_exact_decimal_product` and `accepted_quote_rational_cash` state economic correctness as an equality of values rather than merely of coefficients. `product_valid_iff_within_bound` isolates overflow as the only extra failure mode.
- The model compares the complete payment observation (`lookup i.paymentId c.paymentEvidence = some i`), so a source cannot turn Pending into Final or inflate an amount. `final_verdict_requires_final_record` is a useful theorem.
- `check` always calls `validate` first, and `invalid_now_cannot_replay` makes that explicit, so replay memory cannot reauthorize stale input.
- The model never executes: `acceptance_never_executes` and `stateful_check_never_executes` hold over all paths.
- The generated examples were current at review time. Decidable `Context`/`Event` values make conformance cases cheap to add.

## Confirmed findings

### Replay conflict properties are not connected to the structural business intent

Severity: medium. This is a gap between a stated claim and what is proved, inside the claimed scope.

References:
- `Validation.lean:29-42` (`replay`) and `Validation.lean:277-284` (`check`): `eventDigest` and `intentDigest` are free `String` parameters that the caller supplies.
- `Model.lean:268-270` (`Event.intent`) and `Model.lean:364-373` (`changed_target_changes_intent`).
- `formal/lean/README.md`, Economic meaning: "These properties explain why a delivery retry cannot renew an action and why altered terms must conflict under its old key."
- `astra-model.md:7`: "Business intent is retained structurally so replay arguments do not need an axiom that SHA-256 is injective."

No theorem links `Event.intent` to the token passed to `check`. `changed_target_changes_intent` shows that the structural intents differ. `action_conflict_rejected` shows that different tokens conflict. The step "different intents yield different tokens" is neither assumed nor proved, so the end-to-end claim does not hold for `check` as defined.

Reproducer (Scratch.lean, checked by `decide`): `ctxR` re-issues `action:demo` with target `sandbox:reports/other`. `reissued` is the fixture approval with that proposal under a new event id.

```lean
example : validate ctxR reissued = some (observation .candidate) := by decide
example : reissued.intent ≠ event1.intent := by decide
example : (match check context1 {} event1 "e1" "intent" with
  | some (_, s1) => (check ctxR s1 reissued "e2" "intent").map (·.1.verdict)
  | none => none) = some .duplicateAction := by decide
```

On the same scenario Python returns `reject:action-identity-conflict`, because it computes the intent digest itself (`validator.py:117,125`). The website already words this carefully ("when its supplied intent token matches"); the Lean README and the Astra note do not.

Proposed change: make replay structural, with no hash assumption. Store `Event` for occurrences and `BusinessIntent` for actions, or generalise `ReplayState` over a digest type `δ` with `[DecidableEq δ]` and instantiate it with `δ := BusinessIntent`. Scratch.lean defines `scheck` this way in about 20 lines and proves the following in three lines:

```lean
theorem scheck_changed_intent_conflicts (c : Context) (s : SReplay) (e : Event) (k : ActionKey)
    (old : BusinessIntent) (fresh : lookup e.occurrenceKey s.events = none)
    (hk : e.actionKey? = some k) (known : lookup k s.actions = some old)
    (changed : old ≠ e.intent) : scheck c s e = none
```

`decide` confirms that the reissued trace returns `none` under `scheck`. To keep the string-digest form as a refinement target, add `check_with (H : BusinessIntent → String)` and prove the conflict theorem under the explicit premise `Function.Injective H` (or injectivity on the stored keys). That makes the hash assumption visible instead of implicit.

Acceptance test: an end-to-end theorem that, for any `c₁ c₂ s e₁ e₂` with `check c₁ s e₁ = some (r, s₁)`, the same action key, a fresh occurrence, and `e₁.intent ≠ e₂.intent`, gives `check c₂ s₁ e₂ = none`. Also add a generated example mirroring the Python `reissued-same-key` case.

Tradeoff: structural tables carry whole events in the model state. That costs nothing for proofs and better matches the README's no-injectivity stance. The cost is that the string-digest form becomes a separate refinement obligation.

### Dispatch is pinned to the lock, but the Python validator dispatches on the installed set

Severity: low. The divergence is latent today and confirmed in a scratch copy.

References:
- `Model.lean:31-34` (`Profile.contract`) and `Model.lean:236-247` (`Envelope.Matches`, `dispatch`).
- `validator.py:94`: `load_profile(e.get('mpeprofile'), e.get('mpecontract'))`.
- `bundles.py:51-58`: when a contract is supplied, `load_bundle` consults only `installed.json`, and any entry in `conformance` mode dispatches.
- `bundles.py:30-44`: `publish_bundle` adds to `installed.json` and never updates `lock.json`.
- `model/README.md:55` describes `installed.json` as the allowlist and `lock.json` as "the current alias set".

Reproducer: `lockdiv.py`. After publishing a second `rfq.v0.2` bundle with altered rules, Python accepts the RFQ example under both `sha256:8b5c6b89…` and `sha256:17aab732…`. Lean `dispatch` accepts only the first. Today `installed.json` has exactly one conformance entry per profile, so the two accepted sets coincide on the current tree.

Proposed change: choose one rule and model it. Either add `installed : List (String × Profile)` to the context and have `dispatch` require `lookup e.contract installed = some p`, or make Python reject any contract that differs from `lock.json[profile]`. Given the docs ("Negotiate the intersection of installed exact contract commitments… Active workflows pin their contract"), the likely intent is: dispatch on the installed set, then require a per-workflow pin from context.

Acceptance test: a `dispatch_iff` theorem against the chosen table, plus a check.py case using a second installed contract.

Tradeoff: an installed-set model makes `Profile.contract` an example value rather than a definition. The `lock.json` copy in Lean becomes a fixture.

## Proposed coverage: economic gaps outside the current identity scope

In each case below Python and Lean agree, so these are not fidelity bugs. `rules.json` defines identity only for occurrences and agent actions. `unified-data-model.md:47` asks to "keep five concepts separate", including "source object and revision", but the v0.2 model does not implement that concept. These gaps are where an economically meaningful misuse is accepted.

### Quote identity and revision

Severity: medium for the product claim; roadmap for v0.2.

A dealer can send two different Firm prices under the same `quoteId` and `rfqId`, each with a new event id, and both are accepted as `offchain-quote-valid` (`quoteId-conflict` above: prices 123.45 and 120.00). `RFQ.quoteId` (`Model.lean:139`) is never used by any gate or by replay.

Proposed change: a quote key `(source, rfqId, quoteId)` handled like an action key. The same intent is a duplicate. A changed intent is a conflict, or an explicit revision once revisions are typed.

Acceptance theorem: `quote_key_conflict` mirroring `scheck_changed_intent_conflicts` for `.rfq`.

Tradeoff: legitimate re-quotes need either new quote ids or a revision field. The latter is a profile change.

### Payment observation identity, status transitions and cumulative amounts

Severity: medium for any consumer that aggregates verdicts.

Three behaviours, all confirmed against Python (`payment-double`, `final-then-reversed`, `cumulative-overpay`):

- The same Final observation under new event ids yields a fresh `paymentFinal` each time.
- A Final observation followed, after a context refresh, by a Reversed observation for the same `paymentId` is accepted with no transition rule.
- Two Final payments of 250.00 and 300.00 against a 500.00 invoice are each accepted, though together they exceed payable.

`InvoiceValid` (`Validation.lean:141-146`) checks only per-observation `amount ≤ payable`. `rules.json` says "partial allowed" and "no posting, allocation", so these behaviours sit inside the documented scope. A `paymentFinal` count is still not a safe economic signal.

Proposed changes:
- Add an observation key `(rail, paymentId)`. The same complete observation is a duplicate.
- Add an explicit status-transition relation, for example Pending→Final, Pending→Reversed and Final→Reversed, all recorded with no regression.
- Optionally add a per-invoice ledger invariant.

Acceptance theorems:
- `payment_observation_at_most_once_fresh`.
- `status_transition_monotone`.
- For the ledger: `∀ trace, Σ amount of accepted Final, non-reversed observations for invoiceId ≤ payable`, or an explicit `overpaid` verdict.

Tradeoff: the model gains stateful accounting that the README currently disclaims. It could be scoped as a separate `Ledger` module so `Validation` stays an observation checker.

### Budget window is carried but never accumulated

Severity: low to medium. This is a design question.

`Approval.budgetWindow` is compared only for equality (`Validation.lean:162,170`). `maxSteps` bounds each proposal, not the window. Three distinct actions of 5 Steps each with `maxSteps = 10` are all accepted (`budget-window` above). `rules.json` reserves the full declared budget "at effect boundary", which the model deliberately omits. Still, a field named `budgetWindow` invites the reading that a window-level cap exists.

Proposed change: either document that `maxSteps` is a per-action cap, or add `windowReserved : Nat` to the replay state and the theorem `Σ budget of fresh candidates in window ≤ maxSteps`.

Tradeoff: reservation semantics belong at the effect boundary, which is out of scope. A per-candidate model would over-count candidates that are never executed.

## Proposed coverage: theorems that are cheap and missing

- At-most-once fresh verdict per action key. This is the theorem that actually backs `maxEffects = 1` at the classification layer. Scratch.lean proves both halves for the existing string-digest `replay`:
  - `replay_records_action`: after any successful call with `some key`, either `key` is recorded or the call was an occurrence duplicate.
  - `known_action_never_fresh`: a recorded key never yields the fresh verdict again.

  Lift these to a trace lemma over `List.foldl` of `check`, and add both to `Audit.lean`.
- Projection theorems for accepted invoices:
  - `accepted_invoice_clock_order`: `effectiveAt ≤ observedAt ≤ occurred ≤ now`.
  - `accepted_invoice_terms`: `lookup invoiceId c.invoices = some i.terms`.
  - `accepted_invoice_not_overpaid`, stated as a cross-multiplied value comparison and not by coefficients alone.
- `accepted_quote_open_rfq`: `lookup q.rfqId c.rfqs = some (true, q.terms)`.
- `payload_profile_mismatch_rejected`: if `dispatch e.envelope ≠ some e.payload.profile` then `validate = none`. This holds today through `CommonValid` but is not stated.
- Round-trip and rejection lemmas for `decodeCurrency`, `decodeUnit` and `decodePaymentStatus`, matching the two that exist for profile and operation.
- `Decimal` equality: under the pinned scales, structural equality coincides with value equality (`a.ValidAt s → b.ValidAt s → (a = b ↔ a.coefficient * b.denominator = b.coefficient * a.denominator)`). The context term matches (`Validation.lean:117,142`) compare representations, so this lemma states when that is economically sound.

## Lower-severity observations

- `cash_unique` (`Model.lean:350-352`) is a tautology about natural numbers and mentions no model type. Remove it, or restate it as uniqueness of an admitted cash `Decimal` for given quote terms.
- `InvoiceValid` compares `amount.coefficient ≤ payable.coefficient` (`Validation.lean:145`). That is sound only because both scales are pinned to 2 in the same conjunction. A `Decimal.le` defined by cross-multiplication would survive a future scale change.
- `Context.proposalDigest` is a total `Proposal → String → String`. The generated contexts return `""` for any proposal other than the fixture's (`check.py`, function `context`). An approval carrying `proposalDigest := ""` therefore passes the digest conjunct in those contexts and is rejected only by the proposal lookup. This is harmless now because the lookup forces the proposal, but the digest gate is not independent evidence in the examples. A return type of `Option String`, with no match on `none`, would make it independent.
- Rejections carry no reason. Python's error codes (`action-identity-conflict`, `quote-validity` and so on) cannot be cross-checked. An `Except Reason Result` variant would let check.py compare rejection reasons as well as acceptance, which would surface ordering divergences.

## Deliberate boundaries (not findings)

These are correctly disclaimed in `formal/lean/README.md`:

- raw byte, depth, string and array limits, duplicate keys and integer-token grammar
- identifier and digest regexes, closed objects, and calendar validity of the `.000Z` instants
- JCS, SHA-256 and the proposal-digest computation
- bundle integrity and manifest closure, source authentication and context provenance
- durable atomic replay, Step reservation at the effect boundary, and actual execution

The Int-instant abstraction is faithful for the translator: whole seconds, UTC, and no leap seconds per `rules.json`.

## Unresolved questions

- Should dispatch follow `installed.json` (Python) or `lock.json` (Lean)? The answer decides which side of the first two findings changes.
- Is quote revision under a stable `quoteId` intended to be a conflict, a duplicate or a typed revision in the next profile version?
- Should `paymentFinal` remain a per-observation fact, or should the model expose invoice-level paid and overpaid status, with Reversed after Final as an explicit transition?
- Does `budgetWindow` denote a cumulative cap? If not, should it be renamed or documented as a pure scope label?
- Hypothesis, not confirmed: running the Rust and TypeScript RFQ interpreters on the `quoteId-conflict` pair should give the same double acceptance, because none of the three models quote identity. I did not run them.

## Key proposals, in priority order

1. Make the replay classification structural, or injective-parameterised, and prove end-to-end changed-intent conflict. Correct the README sentence until then.
2. Add the at-most-once fresh-candidate trace theorem (the core lemmas are already proved in scratch) and add it to `Audit.lean`.
3. Resolve the lock versus installed dispatch rule and make Lean and Python agree.
4. Decide the scope for quote and payment-observation identity and for cumulative payment and Step accounting. Then either document each explicitly as non-goals or add the keyed-replay and ledger theorems listed above.
5. Add the cheap projection and decoder lemmas, and replace `cash_unique`.
