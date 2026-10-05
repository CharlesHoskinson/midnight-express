# Lean specification review synthesis

The independent Claude Opus 5.5 reviews are complete. Baseline: `0dfee26`. This review proposes changes; it does not modify the canonical specification, runtime or published page.

The current model is a useful semantic specification for quotes, payment observations and sandbox approval candidates. Its exact arithmetic, complete evidence matching, source-principal checks and current-context validation should be retained. The highest-value improvement is to connect the replay rules to the business content they are meant to protect. The next assurance step is a build gate that rejects proof placeholders and unexpected axioms automatically.

## Connect replay to business content

`check` accepts opaque event and intent tokens supplied by its caller. Changing an approval's expiry changes its structural business intent, but reusing the old token makes the Lean model classify it as a duplicate action. The actual Python validator computes the changed intent and rejects it. This is a confirmed formalization gap, not evidence of that bug in the Python runtime.

Use structural `Event` values for occurrence bindings and `BusinessIntent` values for action bindings, deriving them inside `check`. Reuse `ActionKey` throughout. Keep digest-backed runtime storage as a separate representation/refinement boundary; avoid introducing an axiom of SHA-256 injectivity to make the model appear complete.

Prove that altered terms under a bound action key conflict, identical terms under a fresh occurrence are duplicates while current validation succeeds, and altered content under an existing occurrence key conflicts. Both sides must refer to actual event content.

## Make proof failures stop the build

Use the pinned toolchain and `lake --wfail build`, then an asserting audit covering all project theorem dependencies. Include an explicit check for project axioms and placeholders, including declarations outside the expected namespace, and make the fixture bridge, public-source synchronization and profile commitments required CI checks.

Parent verification confirmed the current ordinary build accepts an isolated `sorry` canary. Warnings as errors reject that canary, but a separate unaudited axiom still passes both the warning gate and the selective printing audit. The existing canonical project has neither declaration. The negative tests are preserved under [evidence](evidence/README.md). The reviewers' scratch namespace scans also only log findings; they must be made asserting checks before adoption.

## Prove journal behavior across a run

Add reachable-state and well-formedness definitions, with unique table keys and immutable occurrence/action bindings. Prove that a fresh candidate binds its action, later checks preserve the binding, and at most one fresh candidate per key occurs across a sequential trace, including changes to time, policy and revocation context.

A first successful check alone is an insufficient premise for a retry theorem: an arbitrary state can contain an occurrence without its action binding, making the first result a duplicate occurrence and the later result a fresh candidate. Use a fresh-candidate premise or prove coherence for states reachable from the empty journal. The parent checked this case in [retry-premises.lean](evidence/retry-premises.lean).

These properties concern classification. A limit on fresh candidates proves neither effect execution nor durable at-most-once commit.

## State business guarantees in readable terms

Keep the Bool/Prop reflection lemmas, but explain that they establish agreement between the Lean predicate and its executable gate. Add business corollaries combining the gates: source and counterparty agreement, exact cash obligations, complete payment evidence and clock order, and approval intent binding. Use named fields in proposition structures instead of long conjunction projections.

Add explicit rejection and context-change properties: expiry, policy mismatch, revoked approval, narrowed human/target sets and reduced budget cannot create an approval acceptance. Distinguish definitional facts, finite regression evidence and derived safety properties in the reader guide.

## Strengthen the finite bridge and release checks

Add named mutations for each representable semantic gate, preserving all other gates where possible. The current large-quantity cash case also violates the cash equation, so it would still reject if the product-bound check regressed. Add an exact product above the admitted coefficient bound and record which gates fail. Include lower validity bounds, source-role/principal changes, invoice evidence clocks, scope/window/domain comparisons, positive values, units and maximum effects.

The verification reviewer ran targeted kernel-checked examples, seeded compiled differential cases and stateful sequences with the real Python digests; those checks reported no mismatches. Preserve the distinction: `by decide` is kernel evidence, while the larger `#eval` runs are compiled test evidence. Neither is a general refinement proof.

Make the translator strict about consumed keys, fixed tags and canonical string syntax, with a reconstruction check for representable inputs. Keep syntax validity distinct from profile value bounds: typed negative cases must still preserve an out-of-bound coefficient or wrong scale so the Lean gate can reject it. A translator rule that rejects every such value would erase that coverage.

Export language-neutral vectors and compare stateful Python and Lean sequences: fresh acceptance, exact retry, a new occurrence for the same action, changed terms, expiry, revocation and policy rotation. Fresh `Harness` instances for individual events cannot exercise replay. Keep lexical failures and single-constructor tag restrictions listed separately from representable semantic cases.

Use a single checked source for profile commitments, theorem coverage and public downloads. Verify every cited declaration exists, every downloaded file matches the canonical source, and the compiler actually matches the pinned toolchain. Give builds a measured timeout or heartbeat limit. The public standalone Lean build works; the Python bridge needs the full repository and its model dependencies.

## Preserve the current safety boundary

Keep validation before normal replay classification. A known stale occurrence must not regain validity because the journal remembers it. If users need delivery history, define a separate, permission-checked, non-authoritative journal inspection operation rather than changing the acceptance path to ignore current validation.

Keep candidate classification distinct from effect commitment. A later effect model should describe current validation at commit, intent binding, atomic reservation, spent budgets and recovery explicitly. It must align with the Umbra host's actual transitions; the observation checker should not acquire accounting or execution claims by implication.

## Decide product semantics before changing profiles

Quote and payment observations currently use occurrence identity, while approvals also use an action key. Reusing a quote or payment identifier under a new occurrence is therefore not automatically a duplicate or conflict. Decide immutable quote identity versus explicit revision, payment-observation identity and correction transitions, and the key for aggregate budget accounting before adding new gates. Any changed business meaning needs a reviewed profile release and migration plan.

The Lean dispatch model pins the current release commitments; Python dispatches on reviewed installed contracts. They agree for today's modeled release, but a later installed contract can be accepted by Python and remain outside the Lean model. Document that release boundary and model installed-contract selection separately when supporting multiple bundles. Do not silently narrow the runtime to the alias lock or accept arbitrary contract strings in Lean.

## Recommended work sequence

| Work | Completion evidence |
| --- | --- |
| Enforce proof and release checks | A placeholder, unexpected axiom, stale public source or mismatched profile constant makes CI fail |
| Introduce structural replay | Changed terms conflict; exact and same-action retries classify correctly while current validation succeeds |
| Establish reachable journal invariants | Unique keys and immutable bindings survive a trace; one action yields at most one fresh candidate |
| Expand the verification bridge | Representable gates have documented isolated negative cases; stateful vectors and translator round-trips pass |
| Improve implementer guidance | Named predicates, accurate proof classifications, rejection-layer mapping and reproducible source commands |
| Scope later protocol models | Requirements specify quote/payment revisions and budget keys before separate effect, recovery or subscription proofs |

These are proposals. No canonical Lean, validator, subscription implementation or public page was changed by this review. The [independent reports](README.md), [parent verification](verification.json) and [reproductions](evidence/README.md) preserve the supporting evidence and unresolved questions.
