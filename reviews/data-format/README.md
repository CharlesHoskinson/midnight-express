# Five-role data format review

The user requested five data scientist/principal engineer reviewers of the unified data model and Ethereum/Solana vocabulary. Each review evaluates the actual artifacts and distinguishes reference defects from intentionally deferred runtime capabilities.

| Reviewer | Role | Focus |
| --- | --- | --- |
| [Semantic science](semantic-science.md) | Principal data scientist | Semantic consistency, quantities, missingness and data-quality measurements |
| [Chain science](chain-science.md) | Blockchain data scientist | Coverage, provenance, reorgs, temporal analytics and minimal chain slices |
| [Contract engineering](contract-engineering.md) | Principal engineer | Schema/validator agreement, identity, commitments and version evolution |
| [Execution safety](execution-safety.md) | Principal engineer | Authority, state/replay, budgets, approval boundaries and effect safety |
| [Interoperability](interoperability.md) | Principal engineer | Independent adapters/SDKs, operational cost, bounded wire/recovery and adoption |

Consolidated recommendations: [data-format-review.md](../../docs/product-requirements/data-format-review.md).

Independent counterexamples: [reproduce-findings.py](reproduce-findings.py) and [observed-counterexamples.json](observed-counterexamples.json). Run from any directory with the project's model dependencies installed:

```bash
/tmp/mpe-data-model-validation-env/bin/python reviews/data-format/reproduce-findings.py
```

The recorded report describes accepted cases that contradict intended rejection rules. It is not a security-pass report. The review leaves the pinned schemas, validator and semantic manifests unchanged; recommendations need implementation and additional negative/cross-language validation. Nothing here executes an effect.
