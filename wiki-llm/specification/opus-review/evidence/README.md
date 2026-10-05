# Review reproductions

These files preserve examples and proposed lemmas from the independent Opus reviews. They are review evidence, outside the canonical Lean project and its published sources. The structural replay prototype is a proposal, not an adopted implementation or a runtime refinement proof.

From `formal/lean`, run each Lean file with the pinned toolchain, for example:

```bash
lake env lean ../../wiki-llm/specification/opus-review/evidence/replay-counterexamples.lean
```

`proposed-invariants.lean` checks reflection, rejection, revocation monotonicity and state preservation lemmas. `candidate-invariant.lean` proves a two-step limit on fresh candidates for one action key. This is a classification property; it proves no effect execution or durability. `retry-premises.lean` demonstrates why a stronger retry theorem needs a fresh-candidate premise or a reachable, coherent journal.

From the repository root, run `python wiki-llm/specification/opus-review/evidence/replay_tokens.py` in the model dependency environment. It confirms that the Python runtime computes the changed intent and rejects it under the old action key. The Lean counterexample supplies a reused opaque token to `check`, demonstrating the missing connection between the structural event and that token.

`build_gate_negative.py` copies the Lean project to a temporary directory. It checks the current build's response to a proof placeholder and an unaudited project axiom. Both deliberately invalid declarations remain in that temporary copy. A hardened proof gate should change the expected outcomes; these tests describe the reviewed baseline.

The reviewer subdirectories preserve the original mutation generators, condition-coverage probes and alternative proof sketches. Their original machine and scratch paths remain unchanged for provenance; set those paths for a new checkout before rerunning them. Large generated randomized Lean files are reproducible from the generators and are not copied here. The expanded randomized runs use compiled `#eval`, while the targeted examples use kernel `by decide`.

The scratch namespace audits print findings; they are not failing CI gates as written. The proposed production audit must fail explicitly on unexpected dependencies and cover project declarations outside the expected namespace as well. The digest-function theorem sketch assumes injectivity explicitly; the synthesis recommends structural replay instead of treating that hypothesis as a proved property of SHA-256.
