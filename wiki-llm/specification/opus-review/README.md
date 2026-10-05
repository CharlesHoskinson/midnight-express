# Opus review of the Lean specification

Charles requested independent Claude Opus 5.5 reviews of the data-model specification. The reviewed release is `0dfee26`. The reports inspect actual Lean definitions, the Python reference, profile schemas and the reader guide. They distinguish confirmed in-scope gaps from intentionally deferred parsing, cryptographic, authority-provenance and durable execution boundaries.

Read the [synthesis and proposed work](synthesis.md) for the recommended order and the decisions that should remain separate from repairs to the current model.

| Review | Focus |
| --- | --- |
| [Model fidelity](model-fidelity.md) | Economic meaning, schemas, profile commitments and runtime agreement |
| [Proof strength](proof-strength.md) | Useful guarantees, assumptions, rejection properties and axiom checks |
| [Authority and replay](authority-replay.md) | Current policy, revocation, identity, journal traces and effect boundaries |
| [Verification bridge](verification-bridge.md) | Translation fidelity, mutations, drift and cross-language sequences |
| [Maintainability and reader guidance](maintainability-reader.md) | Reproduction, modularity, public sources and documentation claims |

[Provenance](provenance.json) records the requested model and the model identifiers returned by the Claude CLI. The original coordinator stopped during resume; completed CLI results were recovered and the remaining reviewers continued under a durable coordinator. Missing original process exit codes are recorded as unavailable rather than inferred.

[Review evidence](evidence/README.md) preserves kernel-checked examples, proposed lemmas and isolated negative build tests. [Parent verification](verification.json) records independently checked findings and artifact hashes. Prototype code in this review directory has not been adopted into the canonical specification. No runtime or public website behavior changes are part of this review.
