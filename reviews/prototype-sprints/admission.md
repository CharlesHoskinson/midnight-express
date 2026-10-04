# Admission feasibility across the first three prototype sprints

This is a proposed workstream and decision framework, not integration or benchmark evidence. The first three sprints should determine whether a single RLN admission relation can express the required MPE statement and interoperate with Midnight Registry state. They should also deliver a clearly labeled admission seam for the coordination prototype. They cannot be treated as a promise of production admission, a deployed Registry, an audited modified circuit or complete revocation integration.

Sources: [working stack](../../docs/product-requirements/proposed-stack.md), [Semaphore assessment](../../docs/product-requirements/semaphore-membership-option.md), [requirements fit](../../docs/product-requirements/requirements-fit-and-open-source.md), and [authoritative requirement register](../../docs/design-document/build/appendix-a.md). No new upstream-version review or executable experiment was performed for this plan.

## Fixed architectural boundary

- One RLN-style publication proof, evaluating Zerokit as the engine, proves membership, committed per-class credits and envelope-bound shares together. Do not add a standalone Semaphore membership proof to every publication.
- Borrow Semaphore identity/group/witness lifecycle patterns. Reuse its actual libraries only after commitment, hash, field, tree, leaf encoding and witness vectors match the chosen admission profile byte for byte. An adapter may implement the lifecycle using profile-native primitives; it may not certify membership in a different root.
- Finalized Midnight Registry state is authoritative for membership, limits, period and root policy. A local Merkle tree is a derived witness cache. A mock adapter supplies fixtures for tests and makes no real-finality claim.
- Admission identities are independent of wallet, encryption, signing and session keys. Secrets and private proving witnesses stay inside the client trust boundary. Registration sponsorship need not disclose the secret.
- Cryptographic verification and allowance consumption are separate. Bus Nodes atomically maintain durable local duplicate/equivocation state without a Registry write for each envelope. Multiple nodes may initially accept different first uses; there is no globally serialized admission count.

## Evidence labels used by every demo and report

| Label | What it demonstrates | What it does not demonstrate |
|---|---|---|
| Mock admission | Prototype interface, deterministic failure paths and workflow behavior | Anonymous membership, cryptographic quotas, recoverable abuse evidence or actual Registry finality |
| Stock Zerokit proof + fixture root | Real proving/verification under pinned upstream relation and parameters | Accepted MPE per-class leaf, canonical domain/EID binding or Midnight profile compatibility |
| Candidate MPE relation + mock finalized snapshots | Real cryptographic proof of the documented candidate statement, exercised against fixture roots | Accepted Midnight Registry encoding/finality, independent security review or live revocation |
| Accepted MPE relation + finalized Midnight snapshots | Proven statement, compatible profile and root acceptance demonstrated for the named environment | Production readiness, audited security, registration economics or all protocol obligations |

These labels are cumulative only when the corresponding evidence exists. A cryptographic proof with a mock root is a real proof and a mocked ledger; report both. If a sprint demonstrates only a subset of the candidate statement, list exactly that subset rather than using the complete candidate label.

## Sprint 1: front-load the relation and compatibility spike

Run this work alongside the envelope/transport skeleton so admission feasibility can change the plan before substantial integration work. Pin the Zerokit release/commit, dependency versions, circuit source, field/hash/tree parameters, proving/verifying keys and setup provenance. Write down public inputs and private witnesses of the stock relation before proposing any adaptations.

Produce a statement matrix for the required single relation: identity membership; committed class-limit vector; `0 <= credit_index < leaf_limit[class]`; canonical admission window; network/Registry/profile domain; nullifier; share bound to canonical envelope identifier; and recovery of the offending membership from two valid conflicting shares. For each item mark stock-supported, adapter-only, circuit change or unresolved, with a code/vector reference. Adapter logic cannot substitute for a missing private leaf-bound inequality or a missing recoverable-share relation.

Freeze a candidate profile manifest and shared vectors for identity commitment, leaf serialization, class limits, tree depth/shape, hash/field encoding, insertion/removal and witness updates. Include a prospective Midnight Registry root vector or explicitly mark that correspondence unavailable. Define canonical tuple encoding and domain separation; envelope ID belongs to the content/share input, not the quota domain. Membership root remains a proof input but cannot reset quota or the relevant slope/nullifier when a root changes. Verify the EID preimage avoids a circular dependency on the proof itself; an arbitrary payload digest is not an accepted envelope-ID mapping.

Coordinate this mapping with the data-model workstream: exact schema identity/version, canonical payload bytes and their hash must be bound in the signed/authorized application statement and carried envelope according to the selected format. Include mutation vectors for schema version and payload bytes, and reject ambiguous encodings that give the same authorized statement different action semantics. Admission binds the canonical EID; it does not itself prove business authorization or that decrypted plaintext has the intended action semantics. Any claimed anchored application effect needs the separate exact-byte and plaintext/authority binding evidence.

Deliver a minimal proof harness and stock baseline size/verification/proving numbers. Record any missing setup artifact or build blocker. No need to integrate the complete transport or Registry to obtain this first feasibility result.

**Gate 1:** Continue toward real candidate admission only if the statement mapping, domain design, EID mapping and compatible root strategy have no hidden assumption. If required constraints need a new circuit, explicitly schedule circuit/setup/security work with an owner and estimate. If compatibility is unknown, block runtime reuse of Semaphore libraries. A workflow demo may continue with labeled mock admission; it must not be presented as anonymous quota enforcement. Stock benchmark success alone cannot pass this gate for the MPE relation.

## Sprint 2: exercise candidate proofs and lifecycle separately

Where Gate 1 permits, implement the candidate profile's local identity/witness/proving path and verifier behind the prototype seam. Keep a separate mock implementation with a visibly different configuration. Consume authenticated finalized-snapshot fixtures through the same Registry adapter contract intended for Midnight: network, Registry, profile, period, root, publication/supersession times and finality provenance. Fixtures must not let callers supply an unverified allowance or substitute their own root.

Build an adversarial vector corpus with these outcomes:

- A member with class-2 limit four can use indices zero through three; index four and invalid class/index encodings fail. Altering an asserted limit without changing the committed leaf cannot pass.
- Equal index in different classes yields different nullifiers. Cross-network and cross-Registry use fails in the target context and yields separately scoped slope/nullifier values. Profile substitution and client-chosen arbitrary scopes fail.
- Root replacement within a window leaves a used credit used. EID substitution invalidates content binding; two valid distinct EIDs under one allowance produce distinct shares and recover the intended offender identity/commitment. Verify recovered evidence against membership before using it for revocation.
- Same-envelope retransmission is idempotent. Invalid proof is rejected; a valid conflicting envelope is ignored with both valid envelopes/shares retained and no P4 penalty. Do not manufacture revocation evidence from an unverified conflicting slot.
- Test window boundary tolerance, current roots without recent updates, superseded-root grace, period-ended stale roots, insertion/removal witness updates, profile mismatch and a frozen adapter. A removed member may remain eligible under an accepted old root until its permitted grace expires.

Instrument length/window/root/duplicate checks before expensive verification (`MPE-ECO-013`). A duplicate conflict still needs sufficient cryptographic validation to constitute evidence; specify the bounded deferred-validation path if cheap classification skips the inline verifier. Persist verified consumption/evidence atomically and exercise concurrent first uses plus crash/restart replay. Report local behavior and distributed exposure separately; a multi-ingress fixture does not establish a global quota.

**Gate 2:** Only claim candidate cryptographic admission when the entire documented statement and its negative vectors pass under the pinned profile. Mark the Registry as mocked until live finalized-state provenance and encoding are demonstrated. If constraints or compatibility fail, retain the workflow mock, report the blocker, and revise the admission milestone rather than weakening the accepted requirement silently. A uniform-quota Semaphore comparator is optional research and remains a divergent relation without member-specific limits or recoverable revocation.

## Sprint 3: measure the candidate and decide the next increment

Integrate the successful candidate path with the prototype envelope and Bus Node seam. Exercise the actual slot codec, proof verification, durable replay/evidence handling and root adapter together. Obtain finalized Midnight snapshots where a usable environment and compatible Registry exist; otherwise preserve the fixture boundary and explicitly move real Registry integration beyond sprint three. Recoverable double-use demonstrated in a harness is separate from submitting evidence, enforcing removal and observing finalized Registry revocation.

Publish three independently labeled measurements:

1. **Stock Zerokit baseline:** upstream relation and root fixtures; useful for library/toolchain feasibility only.
2. **Candidate or accepted MPE relation benchmark:** actual chosen relation, actual profile inputs and actual Admission Slot encoding. Do not substitute baseline timings when the candidate requires a different circuit, parameters or public inputs.
3. **Composed prototype behavior:** parsing, cheap checks, root lookup, durable state transition, contention, valid conflict validation and end-to-end ingress behavior. Report throughput and latency without confusing them with isolated proof verification.

For measurement 2, use one core of a 4-vCPU VM and 10,000 proofs, documenting CPU model, VM/provider, affinity, compiler/build mode, parameters, corpus construction and warm/cold methodology. Report median and p99 verification latency, failures and sample count. Freeze the latency gate policy before running; a conservative prototype gate requires p99 at most 10 ms, while also reporting median. No mean-only or fastest-sample success claim. Benchmark valid proofs and malformed/invalid inputs separately so a fast early rejection does not lower valid-proof timings.

Serialize the full slot in its required order: 8-byte window, 32-byte root, 32-byte nullifier, 32-byte share y-coordinate and proof. Report proof bytes and `roundUp64(104 + proof_length)` including padding. The 4,096-byte ceiling permits at most 3,992 proof bytes under that formula. Required extra relation inputs need a documented canonical derivation/encoding; silently appending fields is a profile/layout change, and omitting them from the statement is not a valid size optimization.

Measure proving latency/memory, witness construction/update, identity/registration path, key loading and state I/O separately. None substitutes for the verification target. `MPE-ECO-048` makes the 4,096-byte slot and 10-ms verification targets a **POC MUST gate**, despite the fit narrative calling them production gates. A mock coordination demo can continue, but cannot claim to pass that admission gate. Registration devnet cost and production readiness remain separate gates.

**Gate 3:** Record one of: proceed to real Registry/revocation integration; continue candidate circuit/profile work; or stop this admission candidate and revisit the construction. Proceed only with explicit passing vectors and a passing candidate benchmark, or state precisely which missing evidence restricts the next experiment. If only stock proofs or mocks exist, say so. Do not declare all admission obligations complete after three sprints.

## Reviewable sprint-three handoff

The handoff contains the pinned profile/statement matrix; compatibility and EID/domain vectors; labeled executable harness results; candidate benchmark and slot samples; adapter finality/root-policy contract; durable replay/evidence tests; and a blocker/owner list. It explicitly lists unfinished live registration, evidence submission/revocation, setup/key acceptance, independent cryptographic review, cross-implementation interoperability, secret lifecycle/recovery and production operations. This supports a concrete next decision without turning dependency selection or an attractive demo into a conformance claim.
