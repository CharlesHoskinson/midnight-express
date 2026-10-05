# Sol implementation: named acceptance predicates and enforced proof gates

This implements the reviewed readability and proof-enforcement work against baseline `5ee50a7`. Historical Opus and Astra verification reports and evidence remain archival evidence of their original runs. This note describes the new implementation, rather than changing those reports.

## Acceptance predicates and theorem API

`CommonValid`, `RFQValid`, `InvoiceValid`, and `ApprovalValid` in `formal/lean/MidnightExpress/Validation.lean` are now `Prop` structures with named fields. The executable Boolean gates, legacy digest-token replay API, and all existing theorem names remain intact. The `_iff` theorems reconstruct those named fields. Business corollaries use names such as `cashProduct`, `completeEvidence`, `currentPolicy`, `notRevoked`, `nowLtUntil`, and `permittedTarget` instead of long positional conjunction projections.

The additions are:

- `validation_rejected_iff`: exact rejection means the common and profile-specific predicates do not both hold.
- `expired_approval_rejected` and `stale_policy_approval_rejected`: explicit current-context expiry and policy mismatch rejection, complementing the retained quote-expiry and approval-revocation laws.
- `accepted_invoice_clocks_and_amount` and `accepted_approval_authority`: readable evidence-clock/amount and authority/scope/window/human consequences.
- `narrowAuthority`, `authority_narrowing_preserves_validity`, and `authority_narrowing_cannot_reauthorize`: at a fixed clock, policy and trusted-record snapshot, removing humans/targets, adding revocations, or reducing the step budget cannot turn rejection into acceptance. The premises explicitly require the permission subsets, revocation superset and reduced bound. This does not claim unrestricted monotonicity under arbitrary clock, policy or trusted-record changes.
- `Context.WellFormed`: unique keys for the source, RFQ, invoice, payment-evidence and proposal maps. This is an explicit fixture-quality predicate, not a new executable condition or a claim that external data satisfy it.
- `lookup_of_mem_unique`: under unique keys, map membership yields the same value as first-match executable lookup.

The structural journal is owned by `Replay.lean`; the older `ReplayState`, `replay`, and token-based `check` remain available for compatibility and their equality-token proof boundary is unchanged.

## Proof enforcement

`formal/lean/proof_gate.py` is the shared entry point. The CLI runs the gate; `run_proof_gate(root: Path)` returns audit metadata or raises `GateFailure`. `check.py` calls this gate after checking the finite bridge.

The gate requires the exact `leanprover/lean4:v4.34.1` pin and checks the compiler's reported version. It builds with `lake --wfail build`. Additional canonical modules outside the umbrella imports are compiled with `-DwarningAsError=true`, so an orphan source cannot quietly escape verification.

Source lint covers every canonical `.lean` file under `formal/lean`, excluding `.lake`, the Lake package file and the separate audit-tooling module. It masks string literals and nested comments and rejects proof placeholders, explicit axioms, unsafe declarations, `native_decide`, reduction oracles and externally implemented proof paths. It forbids canonical source from overriding `warningAsError` and admits imports only from bundled `Std` or another local project module. Historical review evidence lives outside this source set.

`Audit.lean` is an asserting metaprogram, not a list of selected `#print axioms` commands. It imports bundled `Lean` solely to inspect the environment. Direct use audits declarations owned by all imported `MidnightExpress` modules. The Python gate generates a temporary invocation importing every canonical project module and identifies ownership by exact module name. It therefore also reaches declarations outside the `MidnightExpress` declaration namespace and newly added modules with other names. It includes generated/internal declarations, rejects explicit project axioms and unsafe declarations, and fails if any transitive proof dependency falls outside `{propext, Quot.sound}`. A success marker and nonzero declaration count are required.

Anonymous `example` proofs do not persist as named environment declarations. Source lint rejects placeholders and forbidden proof mechanisms there; fatal compiler warnings independently reject anonymous placeholders. The negative tests exercise both enforcement layers rather than relying only on a clean-tree audit.

## Regression and CI checks

`formal/lean/test_proof_gate.py` works exclusively in a temporary copy and checks named and anonymous placeholders, an explicit axiom in an orphan module outside the public namespace, a `Classical.choice` dependency without an explicit axiom, unsafe/native-oracle/admit constructs, a changed compiler pin, and nested-comment/string masking. The axiom test bypasses source lint deliberately to prove the kernel-dependency audit itself catches the declaration. Placeholder tests independently exercise fatal compiler warnings.

`.github/workflows/lean-specification.yml` installs hash-locked Python dependencies and the pinned Lean compiler, then runs the finite fixture/replay bridge with the shared proof gate, the isolated proof-gate and translator tests, and `publish.py --check`. The publishing check owns source/schema-constant synchronization and checks named theorem claims on the public reader page. CI does not regenerate stale examples or silently refresh published source.

## Verified boundaries

The kernel proofs concern the Lean definitions and decoded semantic inputs. Finite Python/Lean vectors and replay sequences are regression evidence, not a universal Python refinement theorem. The parser, UTC calendar interpretation, fixture provenance, commitment computation, cryptographic collision assumptions, durable storage and remote effects retain the documented trust boundaries. Context uniqueness is available as a premise; executable lookup semantics remain deterministic first-match semantics for all contexts.

Verified on the integrated working tree:

- `python formal/lean/proof_gate.py` passed: **1,539 project declarations across seven canonical modules**, exact pinned compiler, fatal warnings, and only the allowed `propext` / `Quot.sound` dependencies.
- `python -m unittest discover -s formal/lean -p test_proof_gate.py -v` passed **all seven isolated tests** in 69.44 seconds. Named/anonymous placeholders fail independent compiler-warning checks; an orphan-module axiom and a `Classical.choice` dependency fail the asserting audit.
- The final constructor-only line wrapping in `Validation.lean` also passed `lake env lean MidnightExpress/Validation.lean` after the integrated audit. It changes formatting only.

The bridge agent separately verified the finite vectors, structural traces, diagnostic equivalence and strict translator regressions. The root integration run owns the final source synchronization and public mirror checks; this note does not replace those checks.
