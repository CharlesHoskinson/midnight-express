# Lean specification: architecture, reproducibility and documentation review

Reviewer: Claude Opus 5.5, specification architecture and documentation role. Baseline commit `0dfee26`. No existing file was edited. Scratch work is under `/tmp/mpe-lean-opus-review/maintainability-reader/`.

## Scope

I reviewed the Lean project in `formal/lean` (`README.md`, `lakefile.lean`, `lean-toolchain`, `lake-manifest.json`, `MidnightExpress.lean`, `MidnightExpress/Model.lean`, `MidnightExpress/Validation.lean`, the generated `MidnightExpress/Examples.lean`, `Audit.lean`, `check.py`). I compared them with the Python reference (`model/validator.py`), the public copy in `website/dist/formal/lean` and its `source-manifest.json`, the public page `website/dist/specification.html`, its browser test `website/tests/specification.cjs`, the publishing note in `website/README.md`, and the earlier Astra records in `wiki-llm/specification`. I treated those records as claims to check. I did not read other Opus reviewers' reports.

The project deliberately excludes JSON decoding, JCS, hashing, provenance, runtime refinement and durable storage. I list those exclusions as roadmap items, not defects. The findings below concern what the model and its documentation claim inside that boundary.

## Evidence and commands run

All Lean commands used the pinned binary `/home/hoskinson/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lake`. Unless stated otherwise, they ran from `formal/lean`.

- `lake env lean Audit.lean`: printed 16 lines. `accepted_quote_rational_cash` depends on `[propext, Quot.sound]`; every other audited theorem depends on `[propext]`.
- I used `grep` to search for `sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|opaque`. The only match is the word "opaque" in a doc comment (`Validation.lean:17`).
- `lake env lean MidnightExpress/{Model,Validation,Examples}.lean`: all exited with code 0 and printed no warnings. They took about 1.0 s, 0.7 s and 6.0 s.
- Scratch `regen_compare.py`: loads `check.py`, calls `collect()`/`generate()` in memory and compares the result with the checked-in `Examples.lean`. Result: 36 cases, identical. I did not run `check.py` itself, because it would invoke `lake build` in the shared tree. I did not use `--update`.
- Scratch `AuditAll.lean`: walks every imported theorem under `MidnightExpress` and fails on any axiom outside `{propext, Quot.sound, Classical.choice}`. Result: `theorems scanned: 165; outside allowed set: []`.
- Scratch `Shadow.lean`: shows that `MidnightExpress.Unit` shadows Lean's `Unit` (see the maintainability findings).
- Scratch `StructuralReplay.lean`: a replay/check variant that stores complete events and structural intents. Three theorems compile with no warnings (see the replay finding).
- Scratch `Conjuncts.lean`: evaluates every named conjunct of `CommonValid`, `RFQValid`, `InvoiceValid` and `ApprovalValid` on the 36 generated cases and lists which ones fail. Output is in `conjuncts.out`.
- I copied the public tree `website/dist/formal/lean` to scratch and ran `lake build` there from a clean state. It built in 7.5 s and its `Audit.lean` ran. Its `check.py` fails with `ModuleNotFoundError: No module named 'validator'`.
- `sha256sum` over `formal/lean` matched every hash in `website/dist/formal/lean/source-manifest.json`, and `cmp` showed the public copy is byte-identical to the source.

## Strengths worth retaining

- The scope statement is disciplined. `formal/lean/README.md` ("Proof boundary") and the page's "What still needs external evidence" list name each excluded layer explicitly. The theorems I checked against the page claims do not overreach. The exceptions are the wording points below.
- Each validity rule has a separate `Prop` predicate and executable `Bool` check, linked by an `_iff` theorem (`commonCheck_iff`, `rfqCheck_iff`, `invoiceCheck_iff`, `approvalCheck_iff`, `semanticCheck_iff`). On top of these, `validation_sound` and `validation_complete` give an exact characterisation of acceptance. This is the right architecture and should stay.
- Dispatch is an iff (`dispatch_iff_exact_envelope`, `Model.lean:310`). It pins all six envelope selectors, including the contract hash.
- Arithmetic stays as exact `Nat` coefficient/scale arithmetic with no rounding. `product_valid_iff_within_bound` states precisely which condition is left once both inputs are admitted.
- The project is small and self-contained: core `Std` only, no Mathlib, an empty manifest and a pinned toolchain. A clean build of the public copy takes under 10 s. That makes CI cheap.
- The generated examples are three-way checked. `check.py:185-188` asserts that the Python verdict equals the expected label, and the Lean `by decide` example asserts that the Lean verdict equals the same label. No `native_decide`.
- Lean's replay precedence matches Python's. Occurrence identity is checked first; a duplicate action records the event; a conflict records nothing; validation runs before replay. Compare `Validation.lean:29-42,277-284` with `validator.py:114-131`.

## Prioritized improvements

### Medium: replay theorems are about caller-supplied tokens, not about the structural intent the documentation explains

Status: confirmed. The proposed fix is prototyped and compiles.

References: `Validation.lean:18-21` (`ReplayState` stores `String` digests), `Validation.lean:29-42` (`replay`) and `Validation.lean:277-284` (`check` takes `eventDigest intentDigest : String` as free parameters). In `Model.lean`, the structural results are `Model.lean:258-270` (`BusinessIntent`, `Event.intent`) and `Model.lean:354-379` (`occurrence_metadata_does_not_refresh_intent`, `changed_target_changes_intent`).

Reasoning: the structural-identity theorems and the replay theorems are never connected. `check` does not compute anything from `e` for replay except the occurrence key and action tuple. A caller can pass the same `intentDigest` for two approvals with different targets, and `same_action_new_occurrence_duplicate` will classify the second as `duplicateAction`. The page says this honestly in "What does the replay proof assume?". However, `formal/lean/README.md:30` says "These properties explain why a delivery retry cannot renew an action and why altered terms must conflict under its old key". `astra-model.md:13` says "The validation module can therefore classify same-key altered intent as a conflict". Neither claim is proved by any theorem: the step from "intent differs" to "replay refuses" goes through an unconstrained string.

This gap is not a cryptographic boundary. Lean has `DecidableEq` on `Event` and `BusinessIntent`, so replay memory can store the structural values directly with no hash assumption.

Proposed change: add a structural replay module, or replace the token form. In the prototype (`/tmp/mpe-lean-opus-review/maintainability-reader/StructuralReplay.lean`):

- `IntentReplay` holds `events : List ((String × String) × Event)` and `actions : List (ActionKey × BusinessIntent)`.
- `Event.actionKey?` reuses `Approval.actionKey`.
- `replayS` and `checkS` mirror `replay` and `check`, comparing `old = e` and `old = e.intent`.

Keep the token version only if a later refinement step to digests needs it. In that case, state the condition it relies on as an explicit hypothesis on the digest function (for example, injectivity on intents), not as an axiom.

Acceptance theorems (all three compile against the existing build):

- `changed_intent_conflicts`: if `e.payload = .agent a`, the occurrence is new, `lookup a.actionKey s.actions = some I` and `I ≠ e.intent`, then `checkS c s e = none`.
- `retargeted_approval_conflicts`: an approval recorded under envelope `env`, then re-presented with a different target under any envelope `env'` that has the same source, type, profile and contract and a fresh occurrence key, is refused. This connects `changed_target_changes_intent` to replay.
- `identical_retry_duplicate`: an exact retry of an accepted event yields `duplicateEvent` with unchanged state.

Tradeoff: replay memory now stores whole events. That is fine in a specification but no longer mirrors the Python data layout (digest dictionaries). The link between the two becomes "Python stores `SHA256(JCS(x))` where Lean stores `x`", which is exactly the documented hash boundary.

### Medium: the generated differential cases leave many semantic conjuncts unexercised, and the overflow case is mislabelled

Status: confirmed from `conjuncts.out`.

References: `check.py:133-173`, `check.py:159-161` (`cash_overflow`), `Validation.lean:116-124, 141-146, 160-170`, `astra-model.md:9` ("This covers an actual overflow boundary in the Python validator") and `astra-validation.md:35` ("arithmetic overflow").

Reasoning: `conjuncts.out` lists the Lean conjuncts that are false in each generated reject case. The conjuncts that are never false in any of the 36 cases are:

- RFQ: `distinct` (buyer ≠ seller), `priceUnit`, `priceCurrency`, `baseQty`, `shareUnit`, `qtyValid`, `priceValid`, `cashValid`, and `fromNow` (a quote that is not yet valid). `occBeforeFrom` fails only together with `notFuture`.
- Invoice: `invoiceTerms`, `effBeforeObs`, `amountValid`, `payableValid`, `rail`.
- Approval: `domain`, `scope`, `window` (context mismatch), `occBeforeFrom`, `fromNow`, `untilExpires`, `budgetValid`, `stepUnit`, `maxEffects`, `domainConst`, `windowConst`.

Several of these mirror explicit Python semantic branches, not schema constants:

- `side-mismatch` when buyer equals seller (`validator.py:149`)
- `quote-validity` and `approval-validity` lower bounds (`validator.py:153,185`)
- `authority-domain` context comparison (`validator.py:175`)
- `invoice-mismatch` (`validator.py:162`)
- `evidence-time` for `effectiveAt > observedAt` (`validator.py:164`)

A Python/Lean disagreement in any of those branches would go undetected.

The case named `cash_overflow` fails only `cashProduct`, not `cashValid`. The event keeps its original cash while the quantity is inflated, so it shows "cash ≠ product", not "product exceeds the bound". The Python `cash > 999…` branch (`validator.py:157`) is not the deciding check here either: both disjuncts raise the same code. The prior claim that the slice "covers an actual overflow boundary" is therefore overstated.

The `check.py:133` comment excludes "lexical/schema-only failures that typed decoding cannot represent". Values such as `maxEffects = 2`, `rail = "other"`, a `Step` quantity unit or a 19-digit cash coefficient are representable in the Lean types and are rejected by the Python schema. The differential comparison checks only accept versus reject, so it can include them.

Proposed change: add one mutation per conjunct in which that conjunct is the only failing one where possible. `priceCurrency` is the exception: `Currency` has a single constructor, so it can never fail. Rename `cash_overflow` to `cash_not_product_large_quantity`. Add `cash_bound_only`, in which cash equals a product above `maxCoefficient`. Lean then fails only `cashValid`, and Python rejects at the schema.

Acceptance test: generate a Lean file like `Conjuncts.lean` from `check.py` and assert two things. First, every conjunct name that is not uninhabitable by type is the only failing conjunct in at least one case. Second, each case's failing set equals a label recorded in `check.py`. Fail the run if either assertion breaks.

Tradeoff: about 20 more cases, adding a few seconds to elaboration of `Examples.lean`. Agreement still holds only at verdict level, because Lean has no rejection reasons. See the implementer-guidance section.

### Medium: nothing runs the gates automatically; the audit and public copy are checked by hand

Status: confirmed.

References: there is no `.github` directory or other CI. `wiki-llm/specification/verification.json` records commands and a timestamp written by hand. `Audit.lean:2-17` lists 16 names and prints output that someone has to read. `website/README.md:61` says "verify byte equality before publishing", but no script does this, and `source-manifest.json` has no generator. `website/tests/specification.cjs:42` checks only free-text fragments and that links resolve. It never checks that the theorem names on the page exist.

Reasoning: the source and public copies agree today; I verified the hashes and byte equality. Nothing keeps them aligned. `Audit.lean` covers 16 of the many theorems the page and README cite. For example, `dispatch_iff_exact_envelope`, `accepted_quote_exact_decimal_product`, `changed_target_changes_intent` and `replay_never_executes` are not audited. Its output is never compared with an expected value. `Examples.lean:5` sets `maxHeartbeats 0`, so if a future `decide` regresses, the build hangs instead of failing.

Proposed change: add one script, for example `formal/lean/ci.sh`, or a CI job with these steps:

1. Install the pinned toolchain.
2. Build with warnings as errors (`leanOptions := #[⟨`warningAsError, true⟩]` on the `lean_lib`, or the equivalent lake flag).
3. Run `check.py` (read-only).
4. Run a self-checking audit modelled on the scratch `AuditAll.lean`, using `logError` instead of `logInfo` so a violation fails the run. It scans the whole namespace instead of a fixed list.
5. Generate `website/dist/formal/lean` and `source-manifest.json` from `formal/lean` and fail on any diff.
6. Run `specification.cjs`, extended to collect every theorem name cited on the page and assert that `theorem <name>` exists in the copied Lean sources.

Replace `maxHeartbeats 0` with a measured bound; the current examples finish in about 6 s.

Acceptance test: in a scratch branch, rename a cited theorem, edit one byte of the public `Model.lean`, or add `axiom foo : False`. Each change must make the script fail.

Tradeoff: one more job to maintain. The project builds in under 10 s, so the runtime cost is negligible.

### Low to medium: page and README wording that goes slightly beyond the theorems

Status: confirmed, except where marked.

- `specification.html:91` says "A consumed action cannot be renewed by a fresh occurrence". The model never consumes anything. `replay` records an action key the first time a candidate is accepted (`Validation.lean:42`), and every result has `executes = false`. Suggested wording: "Once an action key is recorded, a later occurrence with the same intent is a duplicate and a different intent is a conflict." Unresolved: whether the product means recording at candidate time or at effect time. See the unresolved questions.
- `specification.html:115` says "Unknown profile and operation strings are rejected by the supplied tag decoders" and cites `unknown_operation_rejected`. `decodeOperation`, `decodeCurrency`, `decodeUnit` and `decodePaymentStatus` (`Model.lean:75-92`) are never called by `validate` or by `check.py`. `check.py:41,55,67` maps tags with Python dicts. The theorem is true but concerns an isolated function. Either route the generated examples through these decoders (emit `decodeUnit "Share"` and add `decodeX "<corpus tag>" = none` examples), or describe them as reference decoders for implementers.
- `specification.html:30,120` present `executes:false` as a property of validation. In the model it is true by construction: `observation` is the only way a `Result` is built (`Validation.lean:15`). The more informative statement is that the model has no execution branch at all. Consider removing the `executes` field and stating that the result type carries no capability. Alternatively, keep the field and say plainly that the property holds by construction.
- `formal/lean/README.md:50` attributes `Quot.sound` to "rational arithmetic". The model has no rational type. `accepted_quote_rational_cash` is a `Nat` cross-multiplication identity, and `Quot.sound` comes from the proof automation (hypothesis, not traced). Suggested wording: "`Quot.sound` appears through standard library lemmas used by `simp`/`omega`."
- The public `website/dist/formal/lean/check.py` cannot run in the published layout, because `ROOT` resolves to `website/dist`, which has no `model/`. The page only promises `lake build`, which works. Add a one-line note that `check.py` needs the full repository.

### Low: maintainability of the Lean sources

Status: confirmed unless marked.

- **`Unit` shadowing** (`Model.lean:59-61`). Inside `namespace MidnightExpress`, `Unit` refers to the share/step enum. Scratch `Shadow.lean` fails with "`()` has type `_root_.Unit` but is expected to have type `Unit`". Any later helper returning `Unit` in this namespace will hit a confusing error. Rename it to `QuantityUnit`. `Fee.none` (`Model.lean:63-65`) has the same collision risk with `Option.none`; `Fee.noFee` or `Fee.zero` avoids it. Acceptance test: the `Shadow.lean` probe compiles after the rename.
- **Two representations of the action key.** `ActionKey` (`Model.lean:249-256`) is what `changed_target_keeps_action_key` is about. Replay, however, uses `String × String × String` and rebuilds the tuple by hand (`Validation.lean:283`), and no lemma links the two. Use `ActionKey` in `ReplayState` and `a.actionKey` in `check`, as the structural-replay prototype does.
- **Positional projection chains.** `hs.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2` and similar appear at `Validation.lean:252, 268, 274, 295-296, 302-304, 325-326, 359-360`. Because the theorem statements are fixed, reordering conjuncts breaks proofs loudly rather than silently, so this is a cost, not a soundness risk. Destructure once with named hypotheses (`obtain ⟨hTerms, hBuyer, hSeller, …⟩ := hs`), or define each validity predicate as a `structure … : Prop` with named fields and a `Decidable` instance. Acceptance test: reordering two conjuncts in `RFQValid` requires changes only in `RFQValid`, `rfqCheck` and the destructuring line.
- **Hand-duplicated Bool checks.** `rfqCheck`, `invoiceCheck` and `approvalCheck` copy each predicate by hand. The `_iff` theorems catch any drift, so this is safe. Defining `rfqCheck c e q := decide (RFQValid c e q)` with an `inferInstanceAs` instance would remove the duplication. This is unconfirmed: I did not test whether the `by decide` kernel reduction in `Examples.lean` stays as fast.
- **Fixture constants inside predicates.** `"fixture-bank-v1"` (`Validation.lean:146`), `"urn:mpe:sandbox:local"` and `"window:fixture"` (`Validation.lean:170`) are schema `const`s of the installed bundles (`model/bundles/*/schema.json`). Moving them next to `Profile.contract` as named profile constants means a contract revision touches one place.
- **Low-value lemmas.** `cash_unique` (`Model.lean:350-352`) proves that two values both equal to `shares * cents` are equal. `positive_product` and `whole_shares_times_cents` are used nowhere else. They are harmless, but grouping them as "sanity lemmas" would keep the coverage list from looking larger than it is.
- **Module split.** `Model.lean` mixes profile pins, decoders, types, arithmetic and identity. `Validation.lean` places replay (`:17-71`) before `Context`, with a stray blank block at `:72-74`. A light split would make the change surface for a new contract a single file:
  - `Profile.lean`: names, contract pins, constants, dispatch
  - `Decimal.lean`
  - `Types.lean`
  - `Identity.lean`
  - `Validation.lean`
  - `Replay.lean`

  Tradeoff: more files for about 770 lines. A split into only `Profile.lean` and `Replay.lean` would get most of the benefit.

## Does the specification guide implementers?

It explains the rules clearly. It is not yet precise enough to be conformance material for another implementation.

- **No rejection reasons.** The Lean model returns `Option Result`. Python returns specific codes (`side-mismatch`, `quote-validity`, `authority-domain`, …). An implementer has no mapping from a Lean conjunct to the expected error code. The cheapest fix is a README table listing each conjunct, the Python code that covers it, and whether the check happens at the schema or semantic layer; `conjuncts.out` already provides the left column. A stronger option is a `Reason` type with `validate : … → Except Reason Result`. That makes check order part of the specification, which is a product decision.
- **No language-neutral vectors.** `check.py` already builds the cases. It could also write a JSON vector file containing the event, the context, the expected verdict and the Lean-computed failing conjuncts, gated by the same staleness check as `Examples.lean`. The Rust and TypeScript interpreters mentioned on the page could then run the same vectors. Tradeoff: another generated artifact to keep in sync.
- **Replay sequences are not differentially tested.** The four replay examples (`check.py:193-202`) are written by hand. Every Python case runs in a fresh `Harness` (`check.py:185`), so the Python replay path is never compared with Lean. Add short sequences generated from one `Harness`: accept, exact retry, new id with the same action, and changed intent after a context change. Compare them with `checkS` from the structural-replay finding.

## Proposed staged roadmap

Each stage keeps the current claims unchanged until its own evidence exists.

- **Hygiene.** No change to the claims.
  - Add the CI script, self-checking namespace audit, public copy generator and theorem-name test.
  - Set a heartbeat bound.
  - Rename `Unit`.
  - Use `ActionKey` in replay and named destructuring in proofs.
  - Make the wording fixes above.
- **In-scope strengthening.** These claims become provable inside the current boundary.
  - Add structural replay and `checkS` with the three prototype theorems.
  - Add one mutation per conjunct and the `cash_bound_only` case.
  - Add Python sequences compared with Lean replay.
  - Add the conjunct-to-reason table and the vector export.
- **Boundary narrowing.** Each step gets its own scoped claim.
  - A Lean decoder from a JSON value tree (core `Lean.Json`, no external dependency) into `Event`, with theorems that unsupported tags and extra fields are rejected and that decoding round-trips on well-formed values. This still says nothing about bytes, Unicode, JCS or SHA-256.
  - Optionally, property-based differential testing that generates typed values from the Lean types and compares them with Python. This is evidence, not refinement.
- **Separate models, kept separate.** Subscriptions, watch cursors and recovery need their own state models with their own scope statements, for example a Quint or Lean state machine. Do not extend this three-profile model into a universal one.

## Proof boundary, as I understand it after review

Kernel-checked: the typed definitions, exact acceptance (soundness and completeness relative to the stated predicates), dispatch pinning, exact decimal arithmetic, structural intent laws, and token-based sequential replay classification. Dependencies are limited to `propext` and `Quot.sound`, confirmed across all 165 theorems in the namespace.

Finite evidence only: agreement with the Python validator on 36 typed cases. For more than half of the semantic conjuncts, no case makes that conjunct the reason for rejection.

Outside the model, as acknowledged: wire decoding, canonical serialization, hashes, provenance of the trusted context, durable and concurrent replay, and execution. One item currently sits outside the proofs but does not need to: the step from "intent differs" to "replay refuses", which the structural replay prototype closes without any cryptographic assumption.

## Unresolved questions

- Should an action key be recorded when a candidate is accepted (current Lean and Python behaviour) or only when an effect boundary consumes it? The page's word "consumed" suggests the latter. Changing this would alter both implementations.
- Should rejection reasons and their order become part of the specification, or remain implementation detail with only a mapping table?
- Should `Profile.contract` and the profile constants be generated from `model/profiles/lock.json` and the bundle schemas, or remain hand-copied with a test asserting equality? Today the link is only indirect: fixtures carrying `mpecontract` would fail dispatch if the values drifted.
- Should the public site carry `check.py` at all, given that it cannot run there?
- Is the `executes` field meant to stay as a reader-facing marker, or can the result type drop it?
