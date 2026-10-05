# Authority and replay review of the Midnight Express Lean specification

Reviewer: independent Claude Opus 5.5, security and replay principal engineer role. Baseline commit `0dfee26`. Only this report and scratch files under `/tmp/mpe-lean-opus-review/authority-replay/` were written. I did not read the other reviewers' current reports.

## Scope

In scope: source principal binding, policy freshness and revocation, human approval, the `proposalDigest` assumption, occurrence conflicts, action retries and effect authority in `formal/lean/MidnightExpress/Model.lean` and `Validation.lean`. I compared them with the Python reference (`model/validator.py`) and the Umbra recovery host (`model/recovery/umbradb-host.mjs`, `test-postgres.mjs`), which hold the runtime evidence for effects. Raw JSON, JCS, SHA-256, signatures, authenticated context provenance, durability and concurrency are acknowledged boundaries (README "Proof boundary"). They are listed separately below and are not counted as defects.

## Evidence and commands actually run

- Read `formal/lean/README.md`, `Model.lean`, `Validation.lean`, `Audit.lean`, `check.py`, and the head of the generated `Examples.lean`. Also read `model/validator.py` (lines 50–200), `model/README.md`, the installed profile schema constants, `umbradb-host.mjs`, and the relevant lines of `test-postgres.mjs`, `docs/product-requirements/unified-data-model.md` and `website/dist/specification.html`. I skimmed the prior Astra reports and treated them as evidence only.
- Printed schema `const`/`enum` constraints with `/tmp/mpe-data-model-validation-env/bin/python` via `validator.load_profile`. Result: `maxEffects=1`, `authorityDomain=urn:mpe:sandbox:local`, `budgetWindow=window:fixture`, Step scale 0 and `rail=fixture-bank-v1` are enforced in Python by the schema. They agree with the literal checks in Lean's `ApprovalValid`/`InvoiceValid`.
- Scratch Lean, compiled against the existing modules with `lake env lean <file>` from `formal/lean` (toolchain v4.34.1). Both files compiled with no errors, no warnings and no `sorry`:
  - `/tmp/mpe-lean-opus-review/authority-replay/Probe.lean`: kernel-checked (`by decide`) counterexamples A, C and D below, plus `replay_preserves_action_binding` and `replay_fresh_requires_unbound`.
  - `/tmp/mpe-lean-opus-review/authority-replay/Probe2.lean`: `check_preserves_action_binding`, `replay_candidate_binds` and the two-step theorem `no_second_candidate`.
- Python harness reproductions with `Harness` on `model/examples/{rfq,agent}.json` and `model/conformance/trusted-context.json`. Observed outputs:
  - quote, then same `quoteId` with new occurrence and price+1¢ → `offchain-quote-valid` both times
  - approval → `sandbox-candidate-only`; identical retry at `now = validUntil` → `reject:approval-validity`; identical retry with action revoked → `reject:human-or-revocation`; identical retry with context restored → `duplicate-event`
  - new occurrence with honest later time `11:30` (validFrom `11:00`) → `reject:approval-validity`
  - same action key, `validUntil` shortened by 1 s → `reject:action-identity-conflict`
  - second authorized human (`bob`, own source) approving same action → `reject:action-identity-conflict`
- I did not run `check.py` (in either mode) or `lake build`. The existing `.lake` build artifacts were imported unchanged.

## Strengths worth retaining

- **The source principal is bound to the payload, not just the role.** `CommonValid` requires `lookup source c.sources = some ⟨profile.role, payload.principal⟩`, where the principal is the RFQ dealer taken from the trusted terms, the approving human, or the payment rail. For RFQs the dealer is fixed by `lookup q.rfqId c.rfqs = some (true, q.terms)`, so only the named dealer's source can quote that RFQ. `accepted_source_role_principal` states this directly.
- **Proposal integrity rests on structural equality.** `lookup a.actionId c.proposals = some a.proposal` compares the whole proposal record, so the authority binding does not depend on the digest oracle. No theorem relies on `proposalDigest`, and none assumes hash injectivity.
- **Current-context revalidation comes before replay classification.** `check` runs `validate` before `replay`, and `invalid_now_cannot_replay` proves it. This matches Python (`_semantic` before the `events`/`actions` lookups) and the Umbra host, which calls `verify()` again inside the transaction (line 26). Revocation, policy rotation and expiry therefore apply to retries, and nothing stale is ever reclassified.
- **The two identities are cleanly separated.** Occurrence identity is `(source, id)`. Action identity is `(authorityDomain, executionScope, actionId)`. Business intent excludes occurrence metadata (`occurrence_metadata_does_not_refresh_intent`). Lean, Python and Umbra use the same precedence: occurrence first, then action.
- **The model fails closed.** Changing any approval term (window, human, policy digest, source) under an existing action key is a conflict, not a renewal. Python confirms this.
- **The ordering of approval time windows is the same in all three implementations.** Lean, Python and Umbra all enforce `occurred ≤ validFrom ≤ now < validUntil ≤ expires`.

## Prioritized improvements: formal data-model findings

### Replay is not connected to event content, so "altered terms conflict" is not a theorem (Medium, confirmed)

`replay` and `check` (`Validation.lean:29–42`, `277–284`) take `eventDigest` and `intentDigest` as free `String` parameters. Nothing relates them to `e` or `e.intent`. `Model.lean` proves `changed_target_changes_intent` (lines 364–373) about the structural `BusinessIntent`, and `Validation.lean` proves `action_conflict_rejected` (56–61) about unequal strings. The bridge between the two is never stated. The README sentence at line 30 ("altered terms must conflict under its old key") is therefore an informal composition. The website's FAQ does already say that the replay model does not compute the digests (specification.html, "What does the replay proof assume?"); the gap is acknowledged there but not closed.

Kernel-checked reproducer (`Probe.lean`):

1. Accept `event1` under `context1` with tokens `"occ1"` and `"intentTok"`. Result: `.candidate`.
2. `e1'` is the same approval with a new occurrence id and target `sandbox:reports/other`. `e1'.intent ≠ event1.intent` holds by `decide`.
3. Under a context whose registry holds the altered proposal, `validate ctxAltered e1' = some (observation .candidate)`.
4. `check ctxAltered s1 e1' "occ2" "intentTok"` yields `.duplicateAction`, not a conflict.

This conforms to the current contract, but the contract leaves digest fidelity to the caller.

Proposed change: no cryptography is needed. Make the journal store structural values: `ReplayState.events : List ((String × String) × Event)` and `actions : List (ActionKey × BusinessIntent)`. Have `check` derive both values from `e` itself. A digest-backed refinement can keep the string form, parameterised by `H : BusinessIntent → String` with hypothesis `Function.Injective H` scoped to that refinement theorem.

Acceptance theorem: `check c s e = some (r, s₁) → agentKey e = some k → agentKey e' = some k → e'.occurrenceKey ∉ keys s₁.events → e'.intent ≠ e.intent → check c' s₁ e' = none`. Also a twin for occurrence conflict: same occurrence key, `e' ≠ e` → `none`.

Tradeoff: the stored state gets larger, which does not matter for a specification. The string-token theorems remain valid as the implementation-facing form.

### Journal invariants are single-step only; there is no reachable-state or trace theorem (Medium, confirmed gap, cheaply closable)

Every replay theorem quantifies over an arbitrary `ReplayState`. None states that bindings persist, that keys stay unique, or that at most one fresh candidate exists per action key across a trace. The type also admits states that the system cannot reach. Example: an agent occurrence recorded in `events` with no binding in `actions`. `identical_occurrence_duplicate` would classify a retry of such an event as `.duplicateEvent` without the action ever having been bound.

I proved the step lemmas in scratch against the unchanged definitions:

- `replay_preserves_action_binding` and `check_preserves_action_binding`: an existing `lookup k s.actions = some old` survives any successful step.
- `replay_candidate_binds`: a fresh verdict for key `k` requires `lookup k s.actions = none` and leaves `lookup k s'.actions = some i`.
- `no_second_candidate`: after a `.candidate` for key `k`, a threaded second `check` (under any context) cannot return `.candidate` for an event with the same key.

Proposed change: add `inductive Reachable : ReplayState → Prop` (start from `{}`, close under successful `check`). Add `run : ReplayState → List Input → List (Option Result) × ReplayState`.

Acceptance theorems:

- `candidate_at_most_once`: in any `run` trace, the number of `.candidate` results whose `agentKey = some k` is at most 1.
- `occurrence_binding_immutable` and the matching action-binding theorem.
- `reachable_keys_nodup`.
- `reachable_agent_occurrence_has_action`: every recorded agent occurrence has its action bound to its intent. This needs the structural journal from the previous finding.

Tradeoff: this costs a few hundred lines of list lemmas. The proofs in `Probe2.lean` show the shape is routine.

### RFQ quote identity is not a replay identity (Medium, confirmed behaviour; whether it is intended is an open question)

`check` passes `action := none` for `.rfq`, so `quoteId` takes part in no identity check. `validate` never reads `q.quoteId`, and `price.value` is not fixed by the trusted context, only by `ValidAt 2` and the cash equation. Kernel-checked in `Probe.lean`: after accepting `event0`, a new occurrence `event:rfq-2` with the same `rfqId`/`quoteId` and price +1¢ (cash recomputed) is accepted as a second fresh `.quote`. Python behaves identically. Two "Firm" quotes with one identifier and different cash obligations both validate. A downstream consumer cannot tell which one binds.

Proposed change: give RFQ a logical key `(source, rfqId, quoteId)` and route it through the same action-key path, so a changed price under a reused `quoteId` conflicts. If requotes under one id are intentional, state that in the README and the profile meaning instead.

Acceptance theorem: `quote_identity_conflict`, the RFQ analogue of `action_conflict_rejected`. Add a corpus case `same-quoteId-repriced → reject` to `check.py`.

Tradeoff: dealers must mint a new `quoteId` for every revision. This changes v0.2 semantics, so it needs a profile version change, not an in-place edit.

### Retries of stored occurrences become rejections after expiry or revocation (Low–Medium, confirmed; design question)

`check` returns `none` for a byte-identical redelivery once `now ≥ validUntil` or once the action is revoked, even though the occurrence is in the journal. This holds in Lean (`Probe.lean`, kernel-checked), in Python (`reject:approval-validity`, `reject:human-or-revocation`), and in Umbra, where the pre-transaction `verify()` throws. A sender cannot distinguish "never accepted" from "already accepted, now stale". Separately, an honest new occurrence stamped after `validFrom` is rejected (Python: `reject:approval-validity`), because `ApprovalValid` requires `e.occurred ≤ a.validFrom`. So the `same_action_new_occurrence_duplicate` branch is reachable for approvals only when the event is backdated.

Proposed change: keep "validate before replay" for anything fresh. Add a read-only verdict for exact stored occurrences, e.g. `.knownOccurrence` with `executes = false`, returned without revalidation. Alternatively, document that the transport layer must answer such retries. Also document that approval retries must be byte-identical.

Acceptance theorem: `known_identical_occurrence_classified`, stating that `lookup key s.events = some (exact e)` implies `check c s e = some (observation .knownOccurrence, s)` for every `c`. Pair it with a theorem that this verdict never binds or executes.

Tradeoff: an observer of stale contexts learns that the occurrence existed. The current design deliberately avoids this, as the docstring at `Validation.lean:27–28` shows.

### Candidate binding in the spec differs from effect binding in the runtime (Low–Medium, confirmed divergence; needs a transition system)

Lean and Python bind the action key when validation produces a candidate (`replay`, line 42; `validator.py:129`). Umbra binds `mpe-actions` only on effect commit (`umbradb-host.mjs:41`), after checking the aggregate budget. The intent includes `validFrom`, `validUntil`, `human`, `policyDigest` and `source`, so in the Lean/Python model a candidate that is never executed permanently burns its action key. Python confirms that a shortened window and a second human both give `action-identity-conflict`. Neither `maxEffects = 1` nor `budgetWindow` is consumed anywhere in Lean, and `acceptance_never_executes`/`replay_never_executes` hold by construction because `observation` hard-codes `false`. They are useful regression guards, but they make no claim about effect authority.

Proposed change: add a two-phase transition system. `Deliver` binds `ActionKey ↦ (intent, Bound)`. `Commit k` requires current revalidation at commit time, phase `Bound`, and the budget, and moves the key to `Committed`.

Acceptance theorems:

- `commit_at_most_once` (per key, any trace)
- `commit_requires_current_validation` (no commit if revoked or expired at commit time)
- `commit_intent_matches_bound_intent`
- `window_spent_le_max`

Tradeoff: this is new modelling, not a repair. It is what "effect authority" actually needs, and the Umbra test cases (race, revoked-at-boundary, aggregate) map onto it directly.

### Aggregate budget semantics are not specified in Lean, and the runtime keys them by human (Low, question)

`accepted_approval_bounded` proves only `proposal.budget ≤ c.maxSteps` for each proposal. Umbra reserves against the key `domain|human|budgetWindow` (`umbradb-host.mjs:33–36`), so each additional authorized human adds another `maxSteps` of capacity in the same window and scope. Whether the window budget is meant per approver or per scope is not stated anywhere I read.

Proposed change: decide the intended key and state it in the transition system above. If the budget is per scope, remove `human` from the runtime key.

Acceptance theorem: `window_spent_le_max` over the chosen key.

Tradeoff: per-scope budgets serialize all approvers on one CAS key.

### Key representation and well-formedness gaps (Low, confirmed)

- `Model.lean` defines `ActionKey` and `Approval.actionKey`, and `changed_target_keeps_action_key` is stated over it. `check` builds a separate tuple, `(a.authorityDomain, a.executionScope, a.actionId)` (`Validation.lean:283`), so the Model theorem does not formally touch the replay key. Fix: have `check` use `a.actionKey`, and type `ReplayState.actions` as `List (ActionKey × _)`.
- `revokedActions : List String` and `proposals` are keyed by `actionId` alone. This is sound only because a `Context` carries a single domain and scope, while the journal is keyed by the full triple. Fix: key revocations by `ActionKey`, or document that a single context holds one scope.
- `Context` lists admit duplicate keys, and `lookup` resolves them first-match. JSON objects in Python cannot express duplicates, and `check.py` never generates them. Fix: add `Context.WellFormed` (`NoDup` on keys) as a hypothesis on the cross-language examples, or use a map type.

### `proposalDigest` is not load-bearing (Low, informational)

`ApprovalValid` checks `a.proposalDigest = c.proposalDigest a.proposal e.contract`. The oracle is arbitrary: `check.py` uses a point function that returns `""` everywhere else. All authority comes from the structural registry lookup. This is the right design, but nothing says so. Fix: one README sentence, plus a theorem that `ApprovalValid` under any two oracles that agree on `(a.proposal, e.contract)` is equivalent.

Also unconfirmed and outside Lean scope: the Python proposal digest domain `{domain, contract, proposal}` does not include `actionId`, scope or policy. If a production signature ever covered only `proposalDigest`, it could be transplanted between action ids that share an identical proposal. A registry holding two action ids with equal proposals already yields two candidates under one human approval, each with `maxEffects = 1`. Fix in production: sign the whole approval, or include the action key in the proposal commitment.

## Deliberately deferred production boundaries

These are roadmap items, not defects:

- Authentication of `source` and the human signature.
- SHA-256/JCS correctness and collision resistance.
- Provenance of `Context` (`trusted : Bool` is a flag).
- Freshness of policy distribution, rollback protection and policy epochs (`policyDigest` is a single current-equality check).
- Clock monotonicity across calls. `now` is supplied per call, and a rolled-back clock is a context-provenance issue. Even so, replay still prevents a second candidate, as `no_second_candidate` shows.
- Durable atomic journaling, crash recovery, concurrent workers, the outbox, and remote exactly-once effects. Umbra and PostgreSQL provide runtime test evidence for these, not proofs.

## Proof boundary as it stands

Proved (kernel):

- Gate soundness and completeness for each profile.
- Principal and role binding and current policy, revocation and expiry for accepted inputs.
- Single-step replay classification over abstract tokens.
- Structural intent laws.
- Non-execution of every returned result, by construction.

Not proved:

- That the tokens are derived from the event.
- Any multi-step or trace invariant.
- Any effect or commit semantics, budget consumption, or quote identity.
- Any refinement relation to Python or Umbra beyond the 36 finite translated cases (as `check.py` itself says).

The single-step lemmas I proved in scratch show that the trace invariants are within reach with the current definitions. Linking to content needs the structural journal change.

## Unresolved questions

- Should a reused `quoteId` with different economics be a conflict, or are requotes under one id intended?
- Is the aggregate step budget per human (runtime today) or per execution scope or window?
- Should a known, byte-identical occurrence be answered without revalidation (status) or always rejected when stale (today)?
- Should an action key be bound at candidate time (Lean/Python) or at commit time (Umbra), and which one does the specification claim?
- Is permanently burning an action key after an unexecuted, expired approval acceptable, or should a re-approval be allowed while the key is still `Bound` and never committed?
