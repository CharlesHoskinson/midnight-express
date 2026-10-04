# UmbraDB: three independent recovery studies

Source: [CharlesHoskinson/UmbraDB](https://github.com/CharlesHoskinson/UmbraDB), commit `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca`, package 0.9.5. This is the Midnight PostgreSQL/TypeScript library. All reviewers independently inspected source before this addition.

- [Architecture/API composition](architecture.md)
- [Privacy, durability and trust](privacy.md)
- [Product/release fit](product.md)
- [Recovery integration and future release](../../../docs/product-requirements/umbradb-recovery.md)
- [Recommended stack](../../../docs/product-requirements/recommended-stack-and-use-cases.md)

Conditional PASS for trusted single-writer backend recovery; production MPE composition remains gated. Local build/typecheck and 38 API-surface tests passed. PostgreSQL crash suites were not rerun locally because the Docker socket is unavailable to the current user. Existing baseline CI is recorded separately, not presented as a new integration test.
