SEMAPHORE V4 — INDEPENDENT PRODUCT/INTEGRATION REVIEW
Date:2026-10-03 America/Denver. Reviewer: design_review_product.
Disposition: Yes for anonymous membership experiments; not a drop-in replacement for MPE's existing RLN admission obligations. Documentary assessment, not implementation or performance acceptance.

THE USER'S MEMBERSHIP QUESTION
Semaphore can prove a publisher belongs to an approved Merkle group without revealing which identity commitment is theirs. This is a useful reusable membership foundation. It also binds a message and scope and produces a deterministic per-identity/per-scope nullifier. Application state makes that nullifier single-use. The off-chain verifyProof function validates cryptography; it does not authenticate the root against Midnight or remember whether the allowance was consumed. Solidity verifyProof versus validateProof illustrates the difference, but MPE can verify off-chain and does not need a Signal or Ethereum service account.

Product value: controlled participation without showing the publisher's registered identity to every relay. Membership privacy does not supply sender network anonymity, recipient private retrieval, payload encryption, Sybil-resistant enrollment or signed business authority.

CURRENT COMPONENTS
Official TypeScript identity/group/proof packages and Circom/Groth16 circuit are in semaphore-protocol/semaphore, MIT. Retrieved main package.json reports proof package4.14.3, while retrieved generator selects circuit artifacts4.13.0; pin library AND actual prover/verification artifact versions, do not infer version equality. This is main-branch metadata, not a claim of installed or latest released package availability.

Official semaphore-protocol/semaphore-rs explicitly implements v4, MIT; retrieved Cargo.toml version0.1.0 with Circom prover and arkworks dependencies. It is a concrete Rust candidate, not evidence of a production-certified or independently audited Rust implementation. Test interoperability against the pinned TypeScript circuit/output format.

worldcoin/semaphore-rs is a distinct MIT workspace, currently main version0.6.0, whose README uses signal/external_nullifier examples and a separate circuit setup. Do not treat its name or popularity as proof of v4 compatibility. Verify exact identity commitment, nullifier/hash/tree parameters and proving artifacts before using it instead of the explicit v4 implementation.

AUDIT SCOPE
Official overview lists a v4.0.0 PSE audit spanning circuits/contracts/libraries. Downloaded report is more precise: March2024 review of v4.0.0-beta.1 commit8eb19e83fda62644872b2fcfbd85011d3b2c21e2, plus specified zk-kit commit215dfb30ba548918181419df5598d0a652901b7c. It contains findings and implemented fixes. That does not establish every current4.14.3 dependency, Rust port, modified circuit, Midnight adapter or application policy is audited. Review selected revisions/fixes and trusted-setup provenance, not just an 'audited' badge.

FIT AGAINST ORIGINAL MPE
- MPE-ECO-012 proof-backed admission: useful core, but accepted finalized root/domain/codec checks are MPE adapter responsibility.
- MPE-ECO-016 private member-specific class quota: stock identity-only membership leaf contains no quota vector or private credit<committed-limit assertion. Uniform PUBLIC quota can be enforced by a finite external scope policy; heterogeneous committed limits need extended circuit/credential relation or another admission instrument.
- MPE-ECO-017 domain: application must prescribe scope from network, Registry, window, class and allowed credit index; arbitrary caller scopes bypass finite allowance. Don't include envelope ID in scope or each message gets a fresh credit domain. Bind envelope ID as message. Root changes must not reset quota within one window.
- MPE-ECO-018 content-bound rate-limit share: stock message binding does not output RLN y-share; changing message under same nullifier proves duplicate use but does not extract member secret/commitment for evidence-driven removal. This is a product/protocol divergence, not a configuration flag.
- MPE-ECO-019/021/022 duplicate and retention: off-chain Bus Node state rejects/reports repeated allowance locally and persists until eligibility expires. Concurrent isolated ingresses can initially accept conflicts; Semaphore does not add global serialization.
- MPE-ECO-028 accountable revocation: anonymous double-use evidence is not identification of the offending member. If recovery/removal remains required, retain RLN or design and review additional accountable credentials; do not promise tracing from Semaphore nullifier alone.
- MPE-ECO-015/051 root freshness: check accepted finalized membership roots/supersession in Midnight. Removal remains ineffective under accepted old roots until the applicable grace ends. Caller-selected valid-but-unapproved root must fail.
- MPE-ECO-048/052 encoding/performance: exact current slot includes window/root/nullifier/y-share/proof, so absence of y-share changes wire/statement unless separate approved profile. Measure actual bytes and verify time, not generic Solidity gas benchmark.

MINIMAL EXPERIMENT TO RECOMMEND
First compare Semaphore anonymous-membership plus a uniform finite PUBLIC credit policy against the intended RLN relation. Use pinned official TS generation, official v4 Rust off-chain verification and synthetic group/root fixtures before adding live Registry plumbing. Hold admission secrets separate from wallet/encryption/signing keys and bind declared envelope identifier through canonical field/hash mapping.

Checks: member versus nonmember; wrong root/network/Registry/window/class; stale root after membership removal/grace; arbitrary/out-of-range credit scopes; same-nullifier same-message retries versus distinct-message conflicts; root update mid-window; malformed scalars/points/encoding; prover/parameter mismatch; crash/restart and two separated ingresses. Show exactly which checks are cryptographic and which are durable external state. Then add finalized Midnight root adapter and benchmark construction on required machine/profile. No per-overlay-message transaction to Ethereum or Midnight is necessary solely to perform off-chain cryptographic membership verification.

Choose outcomes deliberately:
A. Membership-only component retained within broader RLN/admission construction if commitments are compatible. Avoid two redundant proofs on every event by default.
B. Uniform-scope prototype adopted as explicitly nonconformant to current private heterogeneous-quota/share/accountable-revocation targets, followed by conscious requirements decision if desired.
C. Extended Semaphore circuit to include quotas/recoverable shares: now a new construction needing modified artifacts/setup and independent review, not stock audited Semaphore.

Keep tiny groups, issuer knowledge, root-selection fingerprinting, IP/timing, nullifier reuse and directory/witness retrieval in privacy assessment. Never reuse sensitive business/tenant groups as public bus admission groups without explicit leakage permission. Enrollment eligibility and economic anti-Sybil policy remain application-owned. The strongest recommendation is to add Semaphore to the MEMBERSHIP shortlist while retaining RLN as closer fit for the complete currently specified admission relation.

PRIMARY SOURCES (all retrieved with Scrapling and recorded in source-manifest.json)
https://docs.semaphore.pse.dev/
https://docs.semaphore.pse.dev/technical-reference/circuits
https://docs.semaphore.pse.dev/guides/proofs
https://github.com/semaphore-protocol/semaphore
https://github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom
https://github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/generate-proof.ts
https://github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/verify-proof.ts
https://github.com/semaphore-protocol/semaphore/blob/main/packages/contracts/contracts/Semaphore.sol
https://github.com/semaphore-protocol/semaphore-rs
https://github.com/worldcoin/semaphore-rs
https://semaphore.pse.dev/Semaphore_4.0.0_Audit.pdf

ROOT DRAFT REVIEW
/tmp/midnight-semaphore-option.md is materially accurate. Suggested precision: mention specific audit commit/scope and that current official Rust port is not covered automatically; main TypeScript package and prover artifact versions differ, so pin both. Neither changes overall conclusion or introduces a deployment blocker for a scoped experiment.
