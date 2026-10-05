# Proof strength review of the Midnight Express Lean specification

Reviewer: Claude Opus 5.5 (independent, Lean formal methods role). Baseline commit `0dfee26`. Review only: no repository source, generated example or `.lake` file was edited. Scratch work lives under `/tmp/mpe-lean-opus-review/proof-strength/`, and the important scratch statements are reproduced below because that directory is temporary.

## Scope

In scope: every theorem in `formal/lean/MidnightExpress/Model.lean` and `Validation.lean`, `Audit.lean`, `check.py`, the generated `Examples.lean`, the README proof-boundary claims, and the Python reference `model/validator.py` as the runtime counterpart. I looked for vacuous, circular, tautological or overly weak claims, the Bool/Prop bridge, axiom dependencies, and missing rejection, monotonicity, context-change and identity properties.

Deliberately out of scope, following the stated boundary: the raw JSON grammar, JCS, SHA-256, signatures, provenance of the trusted context, durable or atomic replay, and the chain vocabulary. Those appear below only where a gap can be closed inside the model without crossing that boundary.

The Astra reports in `wiki-llm/specification/` were read as evidence. I did not read the other Opus reviewers' reports.

## Evidence and commands actually run

All Lean commands were run from `formal/lean` using `/home/hoskinson/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lake env lean …`, against the existing compiled modules.

- `lake env lean Audit.lean` succeeded. Fifteen of the sixteen audited theorems depend on `[propext]`. `accepted_quote_rational_cash` depends on `[propext, Quot.sound]`.
- `Probe1.lean` exited 0. It contains kernel-checked (`by decide`) reproducers A–D, described below.
- `Probe2.lean` exited 0. It proves `validate_eq_some_iff`, `validate_eq_none_iff`, `accepted_payload_matches_envelope`, `decodeProfile_sound`, `expired_approval_rejected`, `revocation_monotone`, `replay_records_event`, `replay_preserves_events`, `replay_binds_action`, `bound_action_never_fresh` and `replay_preserves_actions`. It also prints the axioms for several theorems that `Audit.lean` omits. `expired_quote_rejected` depends on `[propext, Quot.sound]`, which comes from `omega` and not from rational arithmetic. `changed_target_changes_intent` depends on no axioms.
- `Probe3.lean` exited 0. It proves `accepted_same_intent_only_occurrence_differs`, which depends on `[propext]`.
- `SorryProbe.lean`, which imports `MidnightExpress` and proves `1 = 2` by `sorry`, gave only a warning, exit code 0, and the axioms `[sorryAx]`.
- `lake --help` lists `--wfail  fail build if warnings are logged`. `check.py` calls plain `lake build`, so it does not use this flag.
- A Python script listed the field names of the `model/examples/{invoice-final,agent,rfq}.json` payloads. Every payload field is represented in the Lean structures or is fixed by a constructor.

I did not run `check.py`, because it rebuilds the shared project and the Astra verification record already covers it. I also did not run `lake build` on a project containing `sorry`, because that would require editing sources. The `--wfail` conclusion is therefore inferred from Lake's documented flag together with the `lake env lean` exit code.

## Strengths worth retaining

- **Clean axiom footprint.** There is no `sorry`, `axiom`, `unsafe` or `native_decide` in the project. Every example is a kernel `by decide`. Dependencies are limited to `propext`, with `Quot.sound` in a few places.
- **Explicit Bool/Prop reflection.** `commonCheck_iff`, `rfqCheck_iff`, `invoiceCheck_iff`, `approvalCheck_iff` and `semanticCheck_iff` give a sound bridge. Because `validation_sound` and `validation_complete` are stated against the `Prop` side, the downstream corollaries are about propositions, not Bool artefacts.
- **Strong dispatch result.** `dispatch_iff_exact_envelope` is a genuine iff. Combined with `CommonValid` requiring `dispatch e.envelope = some e.payload.profile`, it ties the payload constructor to all six envelope commitments.
- **Exact decimal arithmetic.** `accepted_quote_exact_decimal_product` and `accepted_quote_rational_cash` derive a structural decimal equality and a cross-multiplied rational equality from several separate conjuncts (scales and coefficient). This is real content, not a projection. `product_valid_iff_within_bound` correctly isolates overflow as the only failure mode.
- **Validation before replay.** `check` revalidates against the current context before consulting replay memory, and `invalid_now_cannot_replay` states this directly.
- **Non-vacuous hypotheses.** The generated examples show acceptance for all three profiles, for both requester sides and at the `validFrom` boundary. The acceptance-conditioned theorems therefore have satisfiable hypotheses.
- **Honest README boundaries.** The README boundary text is accurate in nearly every respect. The two exceptions are noted under the lower-priority findings.

## Prioritized improvements

### Replay identity is not connected to the event or to `Event.intent`

**Status:** confirmed. **Severity:** medium. This is the most consequential gap that lies inside the claimed scope.

**Where.** `Validation.lean:277-284` (`check`) accepts `eventDigest intentDigest : String` as free parameters. `replay` (`:29-42`) compares only these strings. `Event.intent` and `Approval.actionKey` (`Model.lean:255-270`) are never referenced by `Validation.lean`. `check` also rebuilds the action tuple inline at `:283` instead of using `Approval.actionKey`.

**Why it matters.** The README (paragraph "An approval carries…") says that `occurrence_metadata_does_not_refresh_intent`, `changed_target_keeps_action_key` and `changed_target_changes_intent` "explain why a delivery retry cannot renew an action and why altered terms must conflict under its old key". No theorem links those Model facts to the behaviour of `check`. The Astra validation report treats the tokens as acknowledged parameters, which is reasonable for SHA-256. Here, however, the structural intent already exists and has `DecidableEq`, so the link can be closed without any hash assumption.

**Reproducer (Probe A, kernel-checked).**
- `eventAlt` is `event1` with a new occurrence ID and `validUntil := 1791118000`. It is still valid under `context1`, and `eventAlt.intent ≠ event1.intent` is proved by `decide`.
- After `check context1 {} event1 "evt-1" "intent-token"`, the call `check context1 afterFirst eventAlt "evt-2" "intent-token"` returns `duplicateAction`. A changed approval term is therefore classified as a duplicate.
- Conversely, `eventRetry` has an identical intent (proved), but supplying a different token returns `none`. A genuine retry is therefore rejected.

The model's verdict on action identity is entirely determined by the caller's token.

**Proposed change.** Give `check` the identities itself:
- Either store structural values, `events : List ((String × String) × Event)` and `actions : List (ActionKey × BusinessIntent)`, and key with `e.occurrenceKey`, `a.actionKey` and `e.intent`.
- Or parametrize by `H : BusinessIntent → String` and `G : Event → String`, and carry `Function.Injective H` as an explicit theorem hypothesis, never as an axiom.

The structural option needs no assumption and matches the README's claim that "no theorem assumes a collision-free hash".

**Acceptance theorems.**
- `check_retry_is_duplicate`: if `check c s e₁ = some (r, s')`, `e₂.intent = e₁.intent`, `e₂.occurrenceKey ≠ e₁.occurrenceKey`, `e₁.payload = .agent a` and `validate c e₂ ≠ none`, then the verdict of `check c s' e₂` is `duplicateAction`.
- `check_changed_intent_conflicts`: under the same setup with `e₂.intent ≠ e₁.intent` and the same `actionKey`, `check c s' e₂ = none`.
- `changed_target_changes_intent` can then be used directly, because `Probe3.accepted_same_intent_only_occurrence_differs` (below) is already proven.

**Tradeoff.** Structural storage diverges from the Python `Harness`, which stores digests. That gap remains the cryptographic boundary, which is the honest place for it. The four hand-written replay examples in `check.py` would need regenerating.

### The proof gate does not fail on `sorry` or new axioms

**Status:** confirmed in part. **Severity:** medium (process soundness).

**Where.** `check.py:224` runs `lake build` without `--wfail`. `Audit.lean` is not a build target (`lakefile.lean` declares only `lean_lib MidnightExpress`), `check.py` does not run it, and it only prints axioms without asserting them.

**Evidence.** `SorryProbe.lean` compiles with exit 0 and `[sorryAx]`. A future `sorry` in `Validation.lean` would surface only as a warning, and `check.py` would still print `PASS`. This is inferred from the flag semantics, not reproduced on the project. `verification.json` records `auditedDependencies` from a human-read printout.

**Proposed change.**
1. Run `lake build --wfail` in `check.py`.
2. Turn `Audit.lean` into an asserting file, using one `#guard_msgs in #print axioms X` per theorem with the expected text pinned in a doc comment.
3. Run it from `check.py`, or add it as a `lean_lib`.
4. Audit every theorem, not 16 of about 50. `Audit.lean` currently omits all `Model.lean` theorems and also `expired_quote_rejected`, `revoked_approval_rejected`, `accepted_quote_units_and_roles`, `accepted_quote_exact_decimal_product`, `accepted_approval_unexpired`, `replay_never_executes` and the `*_iff` bridges.

**Acceptance test.** Temporarily inserting a `sorry` into any theorem makes `check.py` exit non-zero.

**Tradeoff.** Pinned output must be updated when Lean changes how it prints axioms.

### `CommonValid` and `SemanticValid` restate the Boolean gates, so soundness and completeness are reflection lemmas

**Status:** confirmed. **Severity:** medium (assurance inflation, not a defect).

**Where.** `Validation.lean:99` says "Explicit semantic specification, separate from executable Boolean gates". Each `Prop` predicate has the same conjuncts in the same order as its Boolean gate: 4 for common, 16 for RFQ, 8 for invoice and 19 for approval. `validation_sound` and `validation_complete` (`:216-228`) therefore prove that `decide` is correct, not that the gate meets an independent business property. Most `accepted_*` theorems (`:238-274`, `:291-296`, `:320-326`, `:353-360`) are projections of a single conjunct.

**What is genuinely derived:**
- `accepted_quote_exact_decimal_product`, `accepted_quote_rational_cash` and `final_verdict_requires_final_record`, which use `payloadVerdict`.
- `expired_quote_rejected` and `revoked_approval_rejected`.
- The two dispatch theorems.

**Proposed change.** Add a small, independently written business-level specification and prove refinement into it. The aim is properties that combine conjuncts across modules, not a third copy of the conjunct list. Proven or proposed examples:
- `accepted_payload_matches_envelope` (proven in Probe2) and `accepted_same_intent_only_occurrence_differs` (proven in Probe3): two accepted events with equal intent differ only in envelope `id` and `occurred`. This holds because `Matches` fixes `specversion`, `contentType` and `dataSchema` from the payload's profile.
- `accepted_quote_source_is_counterparty` (proposed): the authenticated source principal of an accepted quote is the dealer, and `{buyer, seller} = {requester, dealer}`. This combines `CommonValid` with `RFQValid` and `requester_side_determines_distinct_roles`, which no current theorem uses.
- `accepted_invoice_payload_is_evidence` (proposed): an accepted invoice payload equals the trusted evidence record, `amount ≤ payable` at a common scale of two, and `principal = rail = "fixture-bank-v1"`.

The longer-term alternative is to restate `RFQValid` and the other predicates as `structure … : Prop` with named fields. That removes the `.2.2.2…` projection chains, which reach 17 deep (`accepted_quote_cash`), and makes the "separate specification" comment true in form as well as content.

**Tradeoff.** More theorems to maintain. The value is that a reviewer can check a few readable statements instead of a 19-way conjunction.

### No single-effect property over a sequence of checks

**Status:** confirmed missing. **Severity:** medium.

**Where.** `maxEffects = 1` is only a conjunct of `ApprovalValid` (`:169`). No theorem says that an action key yields at most one fresh `candidate` across a run of `check` calls, which is the business meaning of a one-effect approval.

**Proven building blocks (Probe2).**
- `replay_binds_action`: a non-`duplicateEvent` success with key `ak` leaves `lookup ak s'.actions = some i`.
- `bound_action_never_fresh`: if `ak` is already bound, any success is `duplicateEvent` or `duplicateAction`.
- `replay_preserves_actions` and `replay_preserves_events`: memory only grows.
- `replay_records_event`.

**Proposed acceptance theorem.** Define `run` as in Probe3, folding `check` over a list. Then prove that for every `ak`, at most one index in `run c s xs` is `some .candidate` produced by an agent event with `actionKey = ak`, starting from `s` with `ak` unbound. The proof is a direct induction using the four lemmas above. I did not complete it within this review, so this part is unconfirmed.

**Tradeoff.** None significant. Sequential, in-memory semantics only, with durability still outside the boundary.

### Missing rejection characterizations and context-change theorems

**Status:** confirmed missing. **Severity:** low to medium.

The current rejection theorems cover only expired quotes, revoked approvals and unknown profiles. All of the following were proven in Probe2 and can be adopted as written:
- `validate_eq_none_iff : validate c e = none ↔ ¬(CommonValid c e ∧ SemanticValid c e)`.
- `validate_eq_some_iff`, which also pins `r = observation (payloadVerdict e.payload)`. No current theorem fixes the verdict on acceptance; `acceptance_never_executes` fixes only the Boolean field.
- `expired_approval_rejected`. Only the RFQ analogue exists.
- `decodeProfile_sound : decodeProfile s = some p → s = p.name`. Only the roundtrip and the negative case exist.
- `revocation_monotone`: if `validate {c with revokedActions := x :: c.revokedActions} e = some r`, then `validate c e = some r`. Adding a revocation never creates an acceptance. The proof shows that the RFQ and invoice cases are definitionally independent of `revokedActions`.

Proposed, not yet attempted:
- Context monotonicity for `humans`, `sandboxTargets` and `maxSteps`, in the direction of shrinking authority.
- Policy change rejects: `c.policyDigest ≠ a.policyDigest → validate c ⟨e, .agent a⟩ = none`.
- Cross-profile non-interference: changing approval-only context fields leaves `validate` unchanged on RFQ and invoice events.
- Time convexity: if an event is accepted at `now₁` and at `now₂`, it is accepted at every `now` in between.
- Validation-before-replay for duplicates: if `check c s e = some (duplicateEvent, _)`, then `validate c e ≠ none`. This follows from the definition, but it is the property a reader actually cares about.

### Context well-formedness is unstated; `lookup` is first-match

**Status:** confirmed behaviour. **Severity:** low.

**Where.** `lookup` (`Validation.lean:23-25`) is used for `sources`, `rfqs`, `invoices`, `paymentEvidence` and `proposals`. The Python contexts are JSON objects, and `raw_json` rejects duplicate keys.

**Reproducer (Probe C).** Prepending a second `"urn:mpe:source:dealer"` entry with the wrong role makes `validate` reject `event0`. Prepending a stale `"action:demo"` proposal makes it reject `event1`. Both outcomes are safe (rejection), but a shadowing entry can also turn a stale record into the effective one. Theorems quantify over all `Context` values, so they also cover contexts the runtime can never form.

**Proposed change.** Add `Context.WellFormed` with `(c.sources.map Prod.fst).Nodup` and the same for the other tables, and an `Inhabited`-free `lookup_eq_some_iff_mem` lemma under `Nodup`. Use it in any future "update a record" context-change theorem.

**Tradeoff.** It is an extra hypothesis. The current theorems need not change.

### Tautological or by-construction claims are presented alongside safety properties

**Status:** confirmed. **Severity:** low (presentation).

- `cash_unique` (`Model.lean:350`) is `a = x → b = x → a = b`.
- `positive_product` is `Nat.mul_pos`.
- `occurrence_metadata_does_not_refresh_intent` and `changed_target_keeps_action_key` are `rfl`.
- `acceptance_never_executes`, `replay_never_executes` and `stateful_check_never_executes` hold because `observation` hard-codes `executes := false` and nothing else builds a `Result`.

These are useful sanity lemmas, but they should not be counted as evidence of non-execution or replay safety. Proposed change: label them as definitional, drop `cash_unique`, and either remove `executes` from `Result` or document that non-execution is a property of the type (no effectful operation exists), not a proved behavioural property.

### The proposal digest carries no assurance in the model

**Status:** confirmed; this is an acknowledged boundary. **Severity:** low.

`ApprovalValid` requires `a.proposalDigest = c.proposalDigest a.proposal e.contract` with an arbitrary function. Probe D sets `proposalDigest := fun _ _ => "anything"` and an event whose digest field is `"anything"`, and the approval is accepted. The structural conjunct `lookup a.actionId c.proposals = some a.proposal` already pins the proposal, so the digest conjunct is redundant in Lean. Generated non-agent contexts also use `fun _ _ => ""`.

Proposed change: state in the README that the digest conjunct is a placeholder that the structural lookup subsumes, or add an explicit `Function.Injective (fun p => c.proposalDigest p contract)` hypothesis to whichever theorem relies on it. No current theorem does.

### Documentation accuracy

**Status:** confirmed. **Severity:** low.

- The README says `Quot.sound` arises "for rational arithmetic". There is no rational type. `Quot.sound` also appears in `expired_quote_rejected` (via `omega`), which `Audit.lean` omits. Reword to say that `Quot.sound` enters through standard tactics (`omega`, `simp` and function extensionality).
- `check.py`'s four replay examples are Lean-only and are not compared with `Harness`. The README's "agreement covers this finite slice" should say that the slice is `validate` only.

## Deliberate deferred boundaries (not counted as defects)

These are acknowledged in the README and consistent with the code:
- JSON decoding, lexical bounds, calendar parsing, JCS and SHA-256.
- Signature and source authentication.
- Provenance of the trusted context and clock.
- Durable, atomic or distributed replay.
- Refinement of the Python, Rust and TypeScript implementations.

The translator in `check.py` is a trusted test component. Its asserts (for example `quoteKind == 'Firm'`) take the place of constructor restriction, which is consistent with the README.

## Conjectures and unresolved questions

- **Logical identity for quotes and invoices.** Quotes and invoices have no logical-action identity. Probe B, kernel-checked, shows the same quote re-sent with a new occurrence ID receives a second fresh `.quote`. Python behaves the same. Is that intended, for example because quotes are idempotent observations, or should `(rfqId, quoteId)` and `paymentId` act as logical keys?
- **Duplicate actions after a context change.** After a duplicate-action verdict, replay memory still holds the old intent. If the trusted `proposals` table is legitimately updated for the same `actionId`, every later approval conflicts permanently. That is consistent with "altered terms must conflict", but the intended recovery path (a new `actionId` or a new scope) should be stated.
- **Ordering of the invoice amount check.** `InvoiceValid` compares `amount.coefficient ≤ payable.coefficient` before the conjuncts that fix both scales to two. It is correct as a conjunction. I recommend a derived lemma stating the comparison as a rational-value inequality, so a future scale change cannot silently break it. This is unconfirmed as a risk; it is only a robustness suggestion.
- **Lake and `sorry`.** I did not run `lake build` on a project containing `sorry`. The claim that `check.py` would pass rests on Lake's documented `--wfail` default together with the `lake env lean` exit code.

## Recommended order of work

1. Make `check.py` fail on warnings and on any axiom drift (`--wfail` plus an asserting audit over all theorems).
2. Connect replay to `Event.occurrenceKey`, `Approval.actionKey` and `Event.intent` structurally, and prove `check_retry_is_duplicate` and `check_changed_intent_conflicts`.
3. Adopt the proven Probe2 and Probe3 lemmas, then prove the run-level single-candidate theorem.
4. Add the business-level corollaries that combine conjuncts across modules, and the context-change and non-interference theorems.
5. Relabel the tautological lemmas and correct the two README statements.
