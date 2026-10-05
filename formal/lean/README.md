# Midnight Express semantic specification

This Lean project describes the installed v0.2 quote, payment-observation and sandbox-approval profiles. It checks decoded typed values against supplied context and models a sequential journal of accepted occurrences and action intents. Its results are observations and candidates; they carry `executes:false` by construction, and the model has no effect operation.

The pinned toolchain is `leanprover/lean4:v4.34.1`. Semantic modules use bundled `Std`. The audit imports Lean's bundled inspection library to examine proof dependencies; no external theorem library is downloaded.

```bash
cd formal/lean
lake --wfail build
```

For the integrated checks, run these from the repository root in a Python environment containing `model/requirements.lock.txt` dependencies:

```bash
python formal/lean/check.py
python formal/lean/publish.py --check
```

The Python bridge needs the full repository. The source downloads on the website form an independently buildable Lean project; they do not include the model's Python fixtures and dependencies.

## Reading the source

| Source | Responsibility |
| --- | --- |
| [Model.lean](MidnightExpress/Model.lean) | Profile commitments, typed values, exact decimals, occurrence identity, action keys and structural intent |
| [Validation.lean](MidnightExpress/Validation.lean) | Named validity predicates, executable gates and acceptance/rejection properties |
| [Replay.lean](MidnightExpress/Replay.lean) | Structural journal, content conflicts, current validation, reachable states and trace invariants |
| [ProfilePins.lean](MidnightExpress/ProfilePins.lean) | Generated kernel checks against the verified installed bundle constants |
| [Bridge.lean](MidnightExpress/Bridge.lean) | Condition diagnostics used to check isolation coverage |
| [Examples.lean](MidnightExpress/Examples.lean) | Generated kernel-checked fixture and stateful sequence comparisons |
| [Audit.lean](Audit.lean) | Asserting dependency inspection for project-owned declarations |

The contracts are exact release pins. Python supports its reviewed installed-contract allowlist, which can grow beyond this release. A newly installed contract requires an explicit semantic model and checks before these proofs can describe it. Unknown commitments have no branch in this modeled release. Tag decoders are small reference functions; they are not a verified JSON decoder.

## Economic meaning

A `Decimal` records a natural coefficient and a scale, interpreted as coefficient divided by `10 ^ scale`. Accepted fields require positive coefficients bounded by `999999999999999999` and the declared scale. Whole Shares and Step budgets use scale zero; USD values use scale two. Unit and scale remain separate so invalid combinations can be tested and rejected.

Quote cash equals quantity multiplied by price, with no rounding. The arithmetic proofs connect coefficient multiplication to exact decimal values and isolate the product bound. Requester perspective determines buyer and seller. Validation also requires an open RFQ with matching complete terms and the half-open interval `occurred ≤ validFrom ≤ now < validUntil`.

An invoice payload contains complete invoice terms, payment identity, amount, status, clocks and rail. It must equal the supplied payment evidence and obey `effectiveAt ≤ observedAt ≤ occurred ≤ now`. Pending, Final and Reversed remain distinct source observations. A Final result establishes neither bank settlement nor allocation to an accounting ledger.

An approval records the complete proposal, target, input digest, Step budget and expiry, together with the human, policy, authority domain, execution scope and budget window. Its action key is `(authorityDomain, executionScope, actionId)`. Acceptance checks current context and permitted scope. Narrowing authority cannot reauthorize an event; changing the current policy or reaching expiry rejects the approval.

## Replay and journal behavior

Use `structuralCheck context journal event`. `Journal.events` stores complete typed events by `(source,id)`; `Journal.actions` stores complete `BusinessIntent` values by `ActionKey`. The function derives identity and intent from the event itself. It accepts no independent digest arguments.

An unchanged occurrence is a duplicate. Changed content under the same occurrence key conflicts. A new occurrence for the same action and intent is a duplicate action. Changed terms under a bound action key conflict in a well-formed or reachable journal. Occurrence ID and record time are excluded from intent, while source, event type, profile, contract and the complete payload remain included.

Current validation runs before replay classification. A remembered occurrence cannot restore an expired or revoked approval. `Reachable` starts with an empty journal and follows successful checks. Reachable journals have unique keys and coherent occurrence/action bindings; successful steps and runs preserve those bindings. `run_at_most_one_fresh_candidate` limits an action key to one fresh candidate across a sequential trace with varying contexts and rejected steps.

That property describes candidate classification. Effect commitment, budget reservation and crash-safe atomicity require their own transition model. The older `ReplayState` and token-based `check` remain as explicitly limited historical reference definitions in `Validation.lean`; the new journal and fixture sequences use structural replay.

## Verification and release checks

The fixture bridge compares the actual Python validator with generated Lean `by decide` examples. It includes isolated negative conditions, exact bound cases and stateful sequences. [vectors.json](vectors.json) exports the event/context cases for other implementations; [coverage.json](coverage.json) records condition isolation and explicit exemptions. Unknown source necessarily also fails role and principal checks. Currency disagreement is impossible within the singleton USD type. Lexical failures that cannot enter the typed model remain wire-decoder evidence.

The translator checks consumed fields, canonical representations, fixed tags and reconstruction. It preserves deliberately invalid numeric bounds and scales so Lean can reject those values rather than removing them from the test slice. These checks are finite evidence. The translator, proposal commitment calculation and parsing pipeline remain trusted test components.

The proof gate checks the actual pinned compiler, builds with warnings as errors and audits project-owned declarations, including declarations outside the public namespace. It rejects proof placeholders and unexpected axiom dependencies. Standard Lean principles such as `propext` and `Quot.sound` arise through library lemmas and proof automation. Isolated negative tests verify that unsafe proof additions make the gate fail.

`publish.py --check` verifies generated profile pins, theorem references on the Specification page, public source bytes and their hash manifest. After intentional reviewed source or fixture changes, regenerate the bridge with `check.py --update` and the public source copy with `publish.py --update`, then run both read-only checks. The CI workflow enforces these checks on repository changes.

## Proof boundary

The model starts after JSON decoding. It does not prove UTF-8 handling, duplicate-key rejection, identifier grammar, closed-object parsing, calendar conversion, raw byte/depth/array/string limits, JCS or SHA-256. Integer instants represent already interpreted UTC seconds. Fixed tags and singleton constructors require a real decoder to reject unsupported wire values.

Proposal digest equality uses a supplied commitment function. Structural proposal lookup and structural replay bind the actual modeled terms, without assuming a hash is injective. The digest-based Python journal remains a separate representation boundary; these proofs do not establish hash collision resistance or a general refinement of that implementation.

The clock, source roles and principals, RFQ records, invoice/payment evidence, proposals, policy, allowed humans and targets, and revocations come from supplied context. `Context.WellFormed` describes unique map keys. Neither it nor the trusted flag establishes authenticity, freshness or provenance in the outside world.

Wire acceptance, source authentication, fresh policy distribution, durable replay, concurrent workers, database recovery, remote effects and blockchain finality require separate evidence. Subscription selectors, cursors, retention and permission transitions are outside this event-profile journal. The Ethereum/Solana vocabulary is also outside the installed profile model.

## Extending the specification

Preserve the dependency direction: typed definitions, validity rules, then the structural journal. Use named predicate fields for derived business properties and keep context assumptions explicit. A new operation, payment status or unit needs a semantic branch and corresponding acceptance and rejection checks. A meaning-changing contract edit belongs in a reviewed immutable release, with new pins and vectors.

Quote revisions, payment-observation identity and cumulative accounting are product decisions for later profiles or separate projections. The current per-observation checker provides no invoice ledger or aggregate budget guarantee. Candidate binding and effect commitment must remain explicit in any later effect model.

## CI template

[lean-specification.yml](ci/lean-specification.yml) contains the checked pipeline commands. GitHub rejected creation of an active Actions workflow because the configured OAuth login lacks `workflow` scope. The template is retained here for installation after that permission is available. The same pipeline passed locally; CI is not enabled by the template alone.
