# Working stack and membership integration

The first backend/desktop architecture combines opaque message transport, local recognition and interpretation, anonymous publication admission, durable workflow state and separate business authority. GossipSub carries envelopes; each recipient decides locally which ones it can recognize. Admission limits publication, while the recipient’s application checks what an event means and whether it may cause an effect. UmbraDB holds backend workflow progress so a restart can preserve that decision.

The table assigns these responsibilities to the working stack. A bounded local reference and recovery sandbox exist; the complete protocol integration remains proposed. The original protocol obligations still govern implementation.

| Layer | Working choice | Implementation boundary |
|---|---|---|
| Transport | Rust libp2p / GossipSub | MPE envelopes, whole-shard reception and expiry-aware cache/queue behavior |
| Recognition and launch confidentiality | Original MPE symmetric profile | Local recognition; no broadcast forward-secrecy claim |
| Membership | Semaphore-derived identity/group/witness lifecycle | One authoritative Midnight Registry root per selected admission profile; exact compatible libraries chosen after profile conformance |
| Publication admission | RLN-style proof, evaluate Zerokit | Anonymous membership plus committed class credits, envelope-bound shares and recoverable double-use evidence |
| Durable state | UmbraDB/Postgres backend workflow recovery; SQLite standalone Rust/client tier | Public-API local composition is demonstrated in a bounded sandbox; complete MPE recovery support remains a future release. One trusted Node writer; retained envelopes and persistence receipts require separate protocols. |
| Ledger/business authority | Midnight Registry, Anchor and consumer adapters | Finalized roots, independent signed instructions, replay protection and anchored-message binding |
| Optional session security | OpenMLS group-first extension; Signal deferred | Dedicated integration experiment, identity binding and durable ratchet/epoch recovery |
| Private mobile reception | Deferred PIR/OMR experiment | Discovery, authenticated retrieval and query scheduling must meet complete budget |

The [consolidated recommendation](recommended-stack-and-use-cases.md) selects OpenMLS for the group-first security extension and orders the candidate use cases. Membership integration follows the interfaces below.

## Membership mechanisms to adopt

Adopt these mechanisms in the membership module:

- **Dedicated private identity and public commitment.** Generate admission identity material independently of wallet/session keys. Only the selected profile's commitment leaves the client; do not publish the private scalar or seed. Preserve sponsored registration and shielded fee rules (`MPE-ECO-004/005/006/007/054`).
- **Incremental group and witness lifecycle.** Maintain membership insertion/removal, client-side Merkle witnesses and updates from authenticated Registry state. Reject mismatched tree profiles or a witness whose root does not match a permitted finalized snapshot (`MPE-ECO-004/026/029`).
- **Scoped nullifier discipline.** Bind network, Registry, window, class and credit index. Keep envelope identity in the content-binding relation, outside the quota scope. Membership root changes must not renew spent credits (`MPE-ECO-016/017/018`).
- **Explicit verification versus consumption.** Cryptographic verification is stateless; Bus Nodes own durable local duplicate/equivocation state. Preserve idempotent same-envelope handling and conflict evidence without a ledger write for each envelope (`MPE-PUB-028`, `MPE-ECO-020/030/031`).
- **Clear version/parameter boundary.** Pin identity, commitment, tree/hash/field, codec, proving/verifying keys and witness APIs as one admission profile. Reject mixed profiles rather than attempting implicit conversion.

The selected architecture reuses Semaphore’s membership lifecycle patterns within the RLN-style admission relation. RLN already proves membership, so each publication should carry one combined proof. A standalone Semaphore membership circuit beside it would add proofs, secrets or trees and complicate registration and revocation without satisfying another requirement.

Semaphore v4's BabyJubjub-derived identity commitment and Poseidon/LeanIMT tree are not presumed identical to an RLN or Midnight commitment/tree. Actual reuse of a Semaphore library requires byte-for-byte shared commitment/hash/field/tree semantics under the selected profile. If those differ, reuse its lifecycle and API patterns with an adapter or profile-native witness engine; never accept a Semaphore proof as membership in a different root. The Midnight finalized Registry remains authoritative.

## Membership module interfaces

Each interface assigns ownership of a step. The signatures describe responsibilities; language-specific bindings remain to be chosen:

| Operation | Input/output | Required invariant |
|---|---|---|
| `createAdmissionIdentity(profile)` | Local secret handle and profile-specific commitment | Fresh independent admission secret; no wallet secret derivation |
| `registerMembership(commitment, limits, period)` | Registration intent / finalized membership reference | Limits committed in the leaf selected by the admission circuit; sponsor need not know secret |
| `applyFinalizedMembershipUpdate(update)` | Verified snapshot and root history | Network/Registry/profile match; publication and supersession times from finalized blocks |
| `membershipWitness(identityHandle, snapshot)` | Private witness handle | Leaf matches identity and committed limits; root is accepted; no witness sent to untrusted remote prover |
| `proveAdmission(identityHandle, witness, context, eid)` | Existing MPE Admission Slot | Root membership, credit bound, domain, envelope-bound RLN share and nullifier proven together |
| `verifyAndRecordAdmission(slot, envelope)` | Accept / idempotent duplicate / ignore / reject plus evidence | Cheap freshness/duplicate checks first; bounded proof verification; concurrent state update; conflicting shares retained |

`context` includes the profile, network, Registry, admission window, size class and credit index. The verifier obtains limits and root policy through the proof/authoritative configuration, not a caller's unsupported allowance claim. A Semaphore-only uniform-quota comparator may enforce an explicit public index range and canonical scope, but cannot claim conformance with member-specific committed limits or recoverable-share revocation.

## Keep from RLN and Midnight

Retain the committed class-credit bounds, content-bound share, recovery of an offending membership on double-use and Registry revocation (`MPE-ECO-016/018/028/052`). Retain finalized root freshness and bounded grace (`MPE-ECO-015/027/029/051`). Scope nullifiers alone do not identify the member to revoke.

## First integration gates

- Cross-library test vectors for identity, commitment, membership roots and insertion/removal witnesses; any mismatch blocks runtime library reuse.
- Canonical scopes and credit bounds: reject arbitrary scopes, out-of-range credits, cross-network/Registry substitutions and root-change quota resets.
- Identical-envelope duplicate handling versus conflicting-envelope evidence; exercise concurrent ingress acceptance without claiming a globally serialized quota.
- Finalized root updates and revocation grace, including a frozen/stale ledger adapter.
- Encoded Admission Slot <= 4096 bytes and verification <= 10 ms on the specified VM; proof generation and witness updates measured separately.
- Secret/witness trust boundary and crash-safe local admission state; no per-envelope Registry write.

[Semaphore assessment](semaphore-membership-option.md), [original requirement fit](requirements-fit-and-open-source.md), and [source reviews](../../reviews/competitive-event-systems/semaphore/README.md) provide source evidence. Cryptographic profile compatibility and production performance remain unverified.
