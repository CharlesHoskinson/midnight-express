# Lean review implementation

The user requested GPT 6.1 Sol agents at high reasoning to implement the archived Opus review recommendations. Distinct reviewers implemented [structural replay](sol-implementation-replay.md), [named predicates and proof gates](sol-implementation-gates.md), and the [finite validation bridge](sol-implementation-bridge.md). Each agent used the requested model through the collaboration tool. Root integrated publication checks and reader guidance; the original review archive remains unchanged.

The canonical journal now compares complete typed events and business intents. Reachability establishes coherent bindings, unique keys and at most one fresh approval candidate per action over a sequential run. Named acceptance predicates expose the validation conditions. The proof gate builds with pinned Lean and fatal warnings, then audits declarations by owning module, including declarations outside the project namespace.

The bridge compares genuine reference validation with typed Lean interpretation, includes refusal cases and isolates gate conditions with explicit exemptions. Shared structural traces exercise identity conflict, renewed occurrences and changing authority. These finite checks do not establish general Python refinement. Wire parsing, serialization, hashes, authenticated context, concurrent durability and effects remain separate boundaries.

Generated profile pins bind modeled constants to verified installed bundles. The public source manifest records byte hashes, and publication rejects stale pins, nonexistent cited declarations or modified downloads. Regression tests deliberately alter each boundary in isolated temporary copies. The updated Specification page explains the guarantees and their assumptions without presenting validation as execution.

Verification commands and results are recorded with the final publication. Future quote revision, payment allocation and approval budget semantics are requirements decisions rather than changes to the installed profiles.

## Integrated verification

The root integration ran `formal/lean/check.py`: the pinned fatal-warning build and module-owned axiom audit passed for 1,539 declarations across seven modules, allowing only `propext` and `Quot.sound`. The finite bridge passed for 94 typed cases, 52 independently isolated conditions with two documented exemptions, and three structural sequences. These quantities describe the test corpus, not production coverage.

`unittest discover -s formal/lean -p 'test_*.py'` passed all translator, proof-gate and publication regressions. `publish.py --update` and `publish.py --check` refreshed and verified the public sources. `node website/tests/specification.cjs` passed static claims, source links, keyboard disclosures and narrow/enlarged-text reflow. A clean `lake --wfail build` of the downloadable Lean project passed without Python dependencies; its generated build cache was removed before publication.

GitHub rejected the first main-branch push because its OAuth login lacks `workflow` scope. The Actions definition was moved to `formal/lean/ci/lean-specification.yml` before publishing the commit. It is a reviewable template, not an enabled CI workflow. Existing credential helpers were preserved.
