# Semaphore membership option

**Semaphore v4 is a credible anonymous-membership foundation. Stock Semaphore does not implement the PDF's complete rate-limit and recoverable-abuse admission relation.** This option remains for consideration; it does not replace the current protocol register.

Three independent studies: [architecture](../../reviews/competitive-event-systems/semaphore/architecture.md), [privacy](../../reviews/competitive-event-systems/semaphore/privacy.md), [product](../../reviews/competitive-event-systems/semaphore/product.md). Sources were collected with Scrapling and are indexed in the [source catalog](../../catalog/event-systems/README.md).

## What we can borrow

Semaphore v4 proves that the holder of a private identity secret belongs to a Merkle group. A proof binds a public message and scope and outputs a scope-specific nullifier. A verifier that records consumed nullifiers can reject repeated use in that scope; stateless proof verification alone does not consume an allowance. The official Solidity contract distinguishes `verifyProof` from state-changing `validateProof`. [Overview](https://docs.semaphore.pse.dev/), [circuit](https://github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom), [contract](https://github.com/semaphore-protocol/semaphore/blob/main/packages/contracts/contracts/Semaphore.sol).

Useful mechanisms are private identity generation, group/merkle witness tooling, scoped anonymous signaling, proof generation and off-chain verification. Use the identity secret independently of wallet spending, encryption, signing and session keys (`MPE-ECO-006`). The official TypeScript implementation and Rust repository are MIT licensed, but audited components and versions must be checked separately from a new Rust integration or modified circuit. [Main repository](https://github.com/semaphore-protocol/semaphore), [Rust implementation](https://github.com/semaphore-protocol/semaphore-rs).

## Fit against the admission requirements

| Obligation | Stock fit | Additional work |
|---|---|---|
| Anonymous membership (`MPE-ECO-004/012`) | Useful core relation | Midnight Registry commitment/root format and finalized-root adapter; canonical proof codec |
| Scoped nullifier (`MPE-ECO-017`) | Useful mechanism | Fixed MPE domain including network, Registry, admission window, class and credit index |
| Committed class quota (`MPE-ECO-016`) | Not supplied | Public verifier policy can enforce a uniform finite set of credit scopes; private per-member limits committed in a leaf need an extended relation |
| Envelope binding (`MPE-ECO-018`) | Public message can bind a digest | Canonical MPE envelope-preimage mapping; stock proof does not produce a recoverable RLN share |
| Evidence-driven revocation (`MPE-ECO-028`) | Not supplied | Two distinct messages under one Semaphore nullifier show double-use, but do not reveal the responsible member for removal |
| No per-envelope chain state (`MPE-ECO-030`) | Compatible with off-chain verification | Distributed replay/equivocation state at Bus Nodes; no call to Solidity `validateProof` for each overlay event |
| Root freshness (`MPE-ECO-015/027/029/051`) | Root management is reusable | Finalized Midnight publication/supersession times and explicit old-root grace; removal is not immediate while stale roots remain accepted |
| Admission slot/performance (`MPE-ECO-048/052`) | Unmeasured | Encoded slot `roundUp64(104 + proof_length)` <= 4096 bytes; verify <= 10 ms on specified VM, including actual adapter encoding |

For a uniform allowance of N messages per class/window, an exploratory scheme uses N permitted credit indices and derives a scope from a domain-separated canonical tuple `(network, Registry, window, class, credit_index)`. The Bus Node must reconstruct/validate that scope and enforce `0 <= credit_index < N`. Accepting arbitrary client-selected scopes gives unlimited allowances. Bind the canonical envelope identifier as the message, **not the quota scope**: including the envelope ID in the scope gives each new envelope a new nullifier. Do not include changing membership roots in the quota domain in a way that resets credits mid-window. This scheme is a proposed policy, not a tested implementation.

Stock Semaphore commits an identity, not MPE's member-specific class allowance vector. A customized membership leaf and bound-check relation could support that vector, but changes the circuit, setup/keys and security review. Likewise adding RLN shares and secret recovery produces a custom admission construction rather than simply configuring Semaphore.

Repeated proofs by one member within one scope share a nullifier, so those actions are linkable. Different properly separated scopes support unlinkable signaling under the construction's assumptions, but IP address, registration timing, root selection, group size and application metadata remain possible identifiers. Semaphore does not provide Sybil-resistant eligibility, hide registration economics, encrypt events, authorize contracts or provide private retrieval. Do not expose tenant/business-group membership as the public bus admission group unless the selected privacy profile explicitly permits it.

## Recommended decision

1. **Membership-only prototype:** evaluate Semaphore's identity/group/witness tooling with finalized Midnight roots and off-chain Bus Node verification. No per-event ledger transaction or nullifier write. Test accepted-root removal/grace and identity recovery explicitly.
2. **Compare two admission relations:** (a) Semaphore with verifier-enforced uniform scopes and local duplicate rejection, and (b) RLN with committed per-class credits and recoverable double-use evidence. The first is simpler but changes the PDF's abuse/revocation behavior; label that divergence rather than claiming conformance.
3. **Preserve the existing target unless deliberately revised:** RLN-style evidence remains the closer match for `MPE-ECO-018/028/052`. If we keep it, reuse compatible membership tooling where helpful without stacking two membership proofs on every message by default.
4. **Benchmark and review before selection:** pin versions and proving parameters, reconcile BabyJubjub/Poseidon/field/tree assumptions with the Midnight Registry, measure proof generation and verification plus actual slot size, exercise malicious scopes/range checks, boundary replay, root updates and concurrent ingress double-use. Solidity contracts and audit reports do not automatically transfer to a Midnight verifier or custom circuit.

Semaphore is therefore worth adding to the shortlist. It could be the membership foundation; deciding whether it replaces RLN depends on whether accountable rate-limit abuse remains a product/protocol requirement.
