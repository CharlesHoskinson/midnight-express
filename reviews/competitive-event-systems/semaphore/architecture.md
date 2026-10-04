Semaphore v4: independent Midnight Express architecture review
Evidence date 2026-10-03 America/Denver. Sources retrieved with Scrapling; manifest.json records hashes and repository commit38d99081d868acf85e19f217ba427fc3a9eb6111. Reviewed circuit, generation/verification SDK, identity/group implementations, Solidity verifier and current v4 specification. Documentary assessment only; no integration or benchmark performed.

Conclusion
YES: Semaphore is a credible reusable foundation for anonymous membership proof and scoped double-use detection. NO: stock Semaphore is not a drop-in implementation of the original PDF's committed per-class allowance, rate-limit-share and recoverable-member revocation relation. Retain RLN as the closer fit if that evidence-based accountability remains required; a simpler Semaphore allowance policy is an explicitly different design choice.

Primary evidence
1. Circuit (immutable inspected source): https://github.com/semaphore-protocol/semaphore/blob/38d99081d868acf85e19f217ba427fc3a9eb6111/packages/circuits/src/semaphore.circom
2. Proof generation: https://github.com/semaphore-protocol/semaphore/blob/38d99081d868acf85e19f217ba427fc3a9eb6111/packages/proof/src/generate-proof.ts
3. Off-chain verification: https://github.com/semaphore-protocol/semaphore/blob/38d99081d868acf85e19f217ba427fc3a9eb6111/packages/proof/src/verify-proof.ts
4. Contract: https://github.com/semaphore-protocol/semaphore/blob/38d99081d868acf85e19f217ba427fc3a9eb6111/packages/contracts/contracts/Semaphore.sol
5. Specification: https://github.com/ethereum/access-layer-specs/blob/main/specs/3-semaphore-v4/README.md
6. Proof guide: https://docs.semaphore.pse.dev/guides/proofs
7. License: https://github.com/semaphore-protocol/semaphore/blob/38d99081d868acf85e19f217ba427fc3a9eb6111/LICENSE

Observed relation
The circuit derives a Baby Jubjub public key from an identity secret scalar, hashes that public key with Poseidon, and proves the commitment's inclusion in its Merkle tree. It outputs the Merkle root and nullifier Poseidon(scope,secret). The message is an independent public input forced into the constraint relation, so changing its bound value invalidates the proof. It has no quota vector, credit bound, line/share output, or repeated-use identity-recovery step. The secret comparator constrains the identity scalar, not an allowance credit index.

The official SDK hashes external message/scope values before proving/verifying. MPE must specify exactly which canonical envelope digest is passed as message, including field mapping/hash/endianness. Do not confuse application scope with the already-hashed circuit scope. Pinned artifacts and depth/verification keys must match; automatic artifact fetching is a convenience, not a production trust policy.

Requirement mapping
MPE-ECO-004 membership registration: reusable identity commitment and group witness tooling, but Midnight Registry must store/maintain a root compatible with the chosen relation and finalized view. Stock Semaphore's plain identity leaf does not commit the MPE allowance vector. Reusing an existing Midnight membership tree without reconciling leaf/hash/tree/field parameters will not work automatically.

MPE-ECO-016 committed per-class limit: NOT stock. Public uniform limits can be checked by the verifier; hidden member-specific limits committed in a leaf need an extended circuit or another proof relation. Membership alone does not prove eligibility for any desired credit count.

MPE-ECO-017 class-bound nullifier: adaptable via a canonical scope containing network/genesis, Registry, admission window, class and credit index. The Bus Node must require that exact domain, current accepted window and valid credit range. Do not put envelope ID into scope; otherwise new envelopes generate new nullifiers and evade one-credit reuse detection. Do not add changing roots in a way that renews a member's credit mid-window.

MPE-ECO-018 content-bound rate-limit share: the message can bind a digest, but stock proof emits no recoverable share. Ordinary message binding is only the membership/content part of this requirement, not its RLN evidence relation.

MPE-ECO-028 evidence-based revocation: NOT stock. Distinct messages with the same nullifier show one identity reused that scope, but do not disclose which hidden identity commitment should be removed. Removing a known member can be a group-management operation; identifying an anonymous abusive member from paired shares is the absent mechanism. Adding it requires a new relation and review, not a configuration toggle.

MPE-ECO-030 no per-envelope ledger state: compatible with standalone off-chain proof verification and durable Bus Node replay/evidence caches. The SDK verifies a supplied root cryptographically; MPE must additionally require that root from authenticated finalized Registry state. Solidity validateProof stores the nullifier and emits proof details on-chain, so do not call it for each overlay envelope. The contract's view verifyProof and stateful validateProof differ; the former alone does not consume a credit.

MPE-ECO-048 proof/slot gate: neither byte size nor latency has been demonstrated for MPE. Benchmark full adapter encoding and verify at the named hardware conditions. The4096-byte limit concerns roundUp64(104+proof_length), not proof alone;10ms is the configured verification target. Do not treat raw Groth16 points or Ethereum gas figures as this benchmark.

MPE-ECO-052 Admission Slot layout: requires window8, root32, nullifier32, share-y32, then proof. Stock Semaphore lacks share-y. Setting it to zero/random bytes does not meet the rate-limit share relation. A membership-only profile needs an explicit requirement/wire revision or a genuinely reviewed extension; no silent adapter workaround.

Uniform-allowance experiment (proposed, not adopted)
Use a finite approved range0..N_c-1 for each class/window. Each credit maps to a fixed domain-separated scope. Require credit to be represented canonically and bound to the scope the verifier reconstructs. A valid member can then spend at most one accepted envelope per approved scope at each Bus Node's durable replay cache. This supplies a simple uniform local quota without custom hidden quota constraints, but diverges from committed per-member limits and recoverable RLN abuse. Multiple ingress nodes can accept a race before caches/evidence meet; this is not globally serialized admission. Root grace must not resurrect spent scopes.

Public scope need not reveal a business stream: use network-wide admission classes/windows shared across members. Avoid separate tenant groups or sparse quota categories that make membership recognizable. Use an admission identity separate from encryption, wallet spending, publisher signing and Signal/MLS session keys. Within one scope repeated use is deliberately linkable through the nullifier; between scopes cryptographic unlinkability still does not hide ingress IP, root timing, group size or registration economics. Small/sparse groups provide weak practical anonymity.

Midnight compatibility/adoption gate
Reuse proof generation and off-chain verification where useful; Solidity deployment on Ethereum is not required. A Midnight Registry adapter must publish and authenticate the same committed membership relation. Native Compact field/hash/tree formats and foreign Groth16 verifier support are separate questions; no claim that the Solidity circuit verifier directly compiles into Compact. Registry must enforce actual membership eligibility and accepted-root lifecycle. Dynamic witness distribution/recovery needs an authenticated, privacy-reviewed path.

Main inspected repository is MIT licensed. Existing audits and trusted-setup artifacts cover their actual stock versions/circuits; changing leaves, credit constraints or RLN share outputs requires new circuit review and matching proving/verification artifacts, including appropriate setup decisions. Pin commits, artifact checksums, supported depths and exact relation. Test unauthorized roots, tampered message, arbitrary scope, out-of-range credit, same-credit same/different envelopes, root update/revocation grace, crashes and concurrent ingress replay before selection.

Review of root synthesis /tmp/midnight-semaphore-option.md
Pass: it correctly separates membership, finite scope policy, private quota constraints, absent RLN recovery and off-chain versus stateful verification. Useful extra emphasis: the pure SDK's successful verifyProof does not establish that the supplied root is an authorized Midnight Registry root; that acceptance check is mandatory. No material correction beyond this explicit verifier-boundary reminder.

Concrete authorized extraction boundary
Approve extracting the membership interface patterns: dedicated admission identity ownership, commitment registration, authenticated witness/root updates, accepted finalized roots and supersession/revocation lifecycle. Keep one authoritative MPE membership root/profile and RLN as the per-envelope admission relation; do not attach a second Semaphore membership proof to every message. This extracts useful separation of responsibilities without changing evidence-driven quota/revocation semantics.

Define CommitmentProfile/TreeProfile explicitly before choosing code: identity-to-leaf derivation, field modulus, hash/serialization, tree shape/depth, zero-leaf conventions and revocation behavior. Semaphore's BabyJubjub-derived public-key commitment and LeanIMT are not presumed equivalent to RLN's secret commitment or Midnight's chosen tree. A generic membership interface should hold opaque commitments/witnesses under a named profile rather than assuming a Semaphore Identity instance supplies an RLN secret. Runtime group/identity toolkit reuse is conditional on exact relation compatibility and cross-implementation root/witness vectors. Otherwise adapt the interface around the existing RLN/Midnight implementation, without maintaining duplicate membership roots as a convenience.

Keep admission-secret recovery from RLN double-use entirely separate from wallet, group/session and spending identities; compromise or deliberate reveal of an admission secret must not reveal their keys. Membership registration eligibility, public registration disclosure, witness-request metadata, root freshness, local quota cache and evidentiary revocation remain explicit MPE duties. This concrete boundary is sound and preserves the original requirements; it is not a switch to stock Semaphore admission.
