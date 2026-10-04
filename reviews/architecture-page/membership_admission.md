# Membership and admission content review

Reviewed `proposed-stack.md`, `semaphore-membership-option.md` and the current `dist/index.html`. The page's “one admission proof,” “Membership & RLN,” and Semaphore lifecycle wording agree with the working recommendation. `dist/app.js`, referenced by the HTML, is absent at that path, so the interactive component and journey copy could not be reviewed.

## Concise corrections

- Change the map caption from “Membership supplies admission” to “RLN admission proves membership and committed class credits together.” Membership alone does not implement the required abuse and revocation relation.
- Use “Semaphore-derived lifecycle; RLN-style admission” in the membership detail. Do not imply stock Semaphore is a compatible Midnight tree, selected runtime library, or an additional publication proof.
- Explain that Bus Nodes own durable local duplicate/equivocation state. Verification alone does not consume credits; the system does not promise globally serialized quota or per-envelope ledger writes.
- Keep envelope identity outside the quota scope. Canonical quota scope binds network, Registry, window, class and credit index; changing roots must not renew credits.
- Distinguish identical-envelope duplicates from conflicting-envelope shares. Only the latter support recoverable abuse evidence and Registry revocation; a Semaphore nullifier alone cannot identify the member to remove.
- State that accepted finalized snapshots and bounded old-root grace govern removal. Revocation is not immediate while an accepted older root remains usable.
- Add measurable integration gates to the membership detail: encoded Admission Slot ≤ 4096 bytes; verification ≤ 10 ms on the specified VM; separately measure proving and witness updates. These are targets, not achieved performance.
- Preserve dedicated admission identities independently generated from wallet, encryption, signing and session keys. Exact commitment/hash/field/tree compatibility must be demonstrated before reusing Semaphore libraries.

## Suggested explanatory copy (100 words)

Admission combines anonymous Registry membership with accountable publication limits. Semaphore contributes identity, group and witness lifecycle patterns; RLN proves membership and committed class credits together in one envelope-bound admission proof. Each credit is scoped to the network, Registry, window and size class. Changing the membership root must never reset spent credits. Bus Nodes verify proofs and durably record duplicates or conflicting shares without a Registry transaction per envelope. Identical envelopes are idempotent; conflicting uses produce evidence that can recover the offending membership for revocation. Finalized roots and bounded grace govern eligibility. Profile compatibility, proof size and performance remain integration gates.
