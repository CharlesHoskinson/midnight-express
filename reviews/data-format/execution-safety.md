# Execution safety review of the unified data format

Review date: 2026-10-03. Role: principal engineer, execution safety. Scope: the unified model, its three pinned Python reference profiles, proposed Ethereum/Solana catalog, and the documented future recovery boundary. This review changes no runtime, contract, catalog or product requirement.

## Assessment

The format has a defensible safety direction: exact installed contracts, closed proposals, independent occurrence and action identities, and explicit separation of observations from authority. **There is no effect executor.** Every reference success returns `executes:false`; the 267 chain entries are proposed metadata with `effectAuthority:false`. Missing production authentication, durable replay, chain proof verification and atomic execution are documented deferred capabilities, not undisclosed executor vulnerabilities.

Two current reference defects matter before this model becomes a template for execution: exact primitive grammars admit terminal newlines, and duplicate actions fail to reserve their new occurrence identity. Neither currently causes a payment or tool call. The larger future risk is connecting a successful validation result to an executor without a small, durable action state machine and a fresh, authenticated authorization decision at the effect boundary.

## Evidence and observed behavior

Read [unified model](../../docs/product-requirements/unified-data-model.md), [model README](../../model/README.md), all schemas and pinned profiles/rules, [validator](../../model/validator.py), [conformance tests](../../model/test_conformance.py), trusted context, [catalog README](../../model/domains/README.md) and execution-relevant catalog entries, [semantic review](semantic-science.md), and [observed counterexamples](observed-counterexamples.json). Read [Umbra recovery requirements](../../docs/product-requirements/umbradb-recovery.md) to establish its proposed integration boundary; no Umbra implementation or live chain was tested.

Executed the unchanged reference with `/tmp/mpe-data-model-validation-env/bin/python`:

| Check | Observed |
| --- | --- |
| `model/test_conformance.py` | 51 checks, three schema self-checks pass |
| `model/domains/test_catalog.py` | 12 metadata tests pass; 267 proposed entries |
| `reviews/data-format/reproduce-findings.py` | Three counterexamples present at this review reproduce; the consolidated report subsequently adds the numeric-token case |
| Additional in-memory checks | Existing approval rejects after clock reaches expiry, policy changes, action revocation, or maximum budget falls below proposal budget |

The additional checks mutate trusted fixture context deliberately. They show how the reference responds to an authority change; they do not show that an attacker can alter trusted state. No cryptography, effect execution, durable recovery, concurrent writer behavior or external delivery was exercised.

## Current defects

### E1 — Duplicate action occurrences escape occurrence conflict tracking

**Current reference defect; medium severity; small effort.** `Harness.check` compares `(source,id)` first, but its `duplicate-action` branch returns before `self.events[identity] = eventhash`. Thus a new occurrence that duplicates an existing action is never recorded. This contradicts the stated rule that reuse of an occurrence identity with changed complete content is a conflict.

Reproduction, using the existing agent example and one harness:

1. Accept the original event: `sandbox-candidate-only`.
2. Change only `id` to `event:second`: `duplicate-action`.
3. Retain `event:second`, change only `time` to `2026-10-04T10:59:59.000Z`: `duplicate-action`, although the expected result is `event-identity-conflict`.

Occurrence time is excluded from the business digest, so the action comparison cannot detect this change. The recorded counterexample and the additional check agree; `(source,'event:second')` is absent from `h.events`. The logical action itself remains deduplicated. This is an occurrence integrity/bookkeeping defect, not a demonstrated repeat effect.

Reserve every successfully validated occurrence, including those classified as duplicate actions, before returning. Retain the separation between occurrence hash and action commitment. Acceptance: unchanged repetition of the second occurrence becomes `duplicate-event`; any complete-content mutation under that identity rejects; another occurrence with identical intent remains `duplicate-action`. Rejected inputs must reserve neither identity. Review new validator/manifest commitments after correction.

### E2 — Exact grammar admits identifiers and amounts with terminal LF

**Current reference defect; medium severity; small effort.** Schema patterns end in `$`, which the Python schema implementation can match before a terminal newline. Both `event:rfq\n` and price coefficient `12345\n` pass the reference; `int()` accepts trailing whitespace in the coefficient. This violates the documented closed ASCII/canonical coefficient rules. The semantic review independently identifies the same pattern problem.

The danger at a future effect boundary is disagreement: one consumer preserves the string as a distinct action/asset identity, another trims it, or a second interpreter refuses it. The current reference uses exact identity equality and does not normalize IDs, so a trimming collision is a threat counterexample, not an observed reference behavior.

Reject forbidden characters with portable exact semantic checks or reviewed cross-runtime patterns; never repair by stripping whitespace. Acceptance: terminal LF/CR, embedded whitespace, escaped equivalent forms and signed/exponent/leading-zero coefficient alternatives reject across both interpreters. Check every primitive pattern, including business IDs, sources and digests. No expansion of accepted vocabulary is necessary.

The semantic review's pending/reversed overpayment inconsistency is also current, but is an evidence-profile boundary issue rather than payment authorization. Resolve its all-status arithmetic rule before any future allocation state machine. The invoice clock relationship needs a domain decision before freshness can be inferred; neither issue creates execution authority today.

## Identity and authority boundaries to preserve

**Stable action, occurrence and EID have different jobs.** `(source,id)` binds immutable complete event content. The business digest excludes occurrence ID/time and all outer EID bytes, while including source, exact contract and complete typed business data. A new EID therefore cannot refresh an approval. EID is an opaque, unused optional harness parameter; this is consistent with the model's boundary, not missing replay protection in an implemented transport executor.

The current action key is `(proposal.target,actionId)`. Its namespace is a destination, not source or contract version. A second authenticated source delivering the same action cannot bypass that key: changing source changes intent and conflicts. Conversely, changing the trusted proposal to a different target and allowlisting that target permits another candidate with the same `actionId`. I reproduced two keys, `('sandbox:reports/demo','action:demo')` and `('sandbox:reports/other','action:demo')`, after deliberate trusted-context replacement. This follows the declared destination-key semantics, so it is not E3. Before execution, specify whether retargeting denotes a distinct action or a forbidden amendment. Prefer an immutable stable action namespace with destination included in its committed content; if destination scopes identity, authorized migration must link predecessor/successor keys and forbid duplicate economic effects. Contract upgrades and policy changes must never erase consumed-action records or silently re-key them.

**A trusted fixture marker is not authentication.** `fixtureTrust` and source role/principal maps are simulated inputs. The CLI accepts a caller-selected context file; anyone able to choose that file can create a permissive simulation. Production must obtain context from a protected local authority service, separately from sender bytes, and bind source, principal, role, domain, capability and freshness to verified provenance. MPE sender authenticity alone cannot establish bank evidence, wallet control or chain consensus. Do not accept a sender's `Final`, human name or catalog source URL as a trust root.

**Approval is a bounded proposal decision.** Exact trusted proposal comparison defeats target/input substitution even after recomputing `proposalDigest`. Policy digest, named human/principal, revocation, target allowlist and exclusive expiry are checked; changed current policy and expiry reject even when replaying an already seen event. Preserve these checks at dispatch. A hash is a commitment, not approval; an approved input digest requires the executor to verify the actual bytes it consumes. Target resolution must be capability-scoped and stable: an allowlisted `sandbox:` label must not become an arbitrary filesystem path, URL or script.

`maxEffects:1` currently describes a candidate; it does not meter real effects. `Step` has no executable charging definition. Before execution, bound the exact operation and target, define charge/reservation/refund rules for failure and retry, and distinguish per-action from aggregate budgets. Parallel approvals can each satisfy `maxSteps` while collectively exceeding a daily cap unless the same transaction reserves aggregate capacity. A policy change may invalidate dispatch, but must not imply that a committed effect never occurred.

**Invoice evidence does not authorize payment or posting.** Exact complete fixture evidence prevents relabeling Pending as Final without corresponding trusted evidence. Final remains a source assertion. Multiple occurrence IDs reporting one payment could be legitimate observations; they must not become multiple invoice allocations. A future allocator needs rail/network-scoped payment identity, invoice revision, unique allocation identity and explicit reversal lineage. A source status change must refer to the same underlying payment rather than erase historical allocations. Supplier/customer identity and document digest must not select an arbitrary destination account.

## Future threat counterexamples and acceptance gates

These are deferred design gates, not evidence of currently implemented unsafe calls.

| Counterexample | Required bounded control and acceptance |
| --- | --- |
| Validate approval, then revoke capability or change input before queued dispatch | Recheck current capability, proposal bytes/target, policy, revocation and trusted time inside the local commit boundary; inject each change between validation and dispatch and require no effect |
| Restart with empty replay state, restore an older snapshot, or upgrade contract and drop old action keys | Durable replay horizon independent of transport EID/profile upgrade; protected domain-bound restore with trusted freshness; replay after restart, restore and migration yields prior result/conflict without a second effect |
| Two workers race the same action, or a stale writer commits after lease loss | Create-only/CAS action claim and versioned transition on one transaction handle; one writer assumption or enforced fencing; race and stale-writer tests show one local result and no extra cursor/outbox progress |
| RPC endpoint switches network; wallet switches account; subscription ID is reused on reconnect | Bind authenticated endpoint/session and request correlation, exact network/genesis, account, selector and concrete evidence location; network/account/session mismatch rejects or invalidates pending dispatch |
| Same token symbol or contract address appears on another network; proxy/program changes after decode | Deployment identity includes network, contract/program and approved code/ABI/decoder revision at the relevant state point; recheck execution-sensitive upgrade assumptions and reject changed bindings |
| Allowance/operator/delegate observation is interpreted as agent permission | Separate chain asset permission from application executor capability; valid allowance without application approval cannot sign or broadcast |
| Successful simulation, submission hash, failed-transaction log, or bridge source message triggers economic effect | Preserve request/result/unknown, execution success, native commitment and origin/destination evidence separately; negative fixtures never promote these observations to settled evidence or authority |
| External destination commits but response times out; worker rebroadcasts a freshly signed transaction | Durable `OutcomeUnknown`, stable destination idempotency key and exact attempt identity; reconcile original outcome before automatic retry, replacement or new signing; fault test commits remote effect then loses response and produces one economic effect |

Catalog `scope` values such as chain/standard/program/local classify vocabulary; they are not capability scopes. `native`, `decoded` and `derived` likewise do not establish authentication, execution success or finality. The catalog already warns that cancellation is local, returned transaction identity is not settlement, and source bridge evidence is not destination redemption. Keep these warnings executable in future narrow profiles rather than constructing one universal `Confirmed` or permission enum.

## Minimal state contracts and the Umbra boundary

Execution safety need not require a generic workflow engine. Start with one local `WriteReport` operation and a few closed records owned by that domain:

- **Occurrence record:** trust domain, `(source,id)`, complete event hash, validation disposition and linked action key. Preserve accepted duplicate occurrences as E1 requires.
- **Action record:** immutable stable key, contract/proposal/intent commitments, destination identity, approval/capability reference, current version, expiry, reserved budget and a small state enum. Terminal records retain result digest or refusal reason; conflicts never advance state.
- **Dispatch record:** action key, immutable request digest, stable destination idempotency key, attempt identity, dispatch deadline and known/unknown outcome evidence. An attempt is not a new action. A changed signed transaction or replacement requires an explicitly linked, authorized transition.
- **Progress record:** source/domain/profile-bound cursor and bounded coverage/gap assertion. A cursor is not finality, action completion or proof that omitted history was examined.

For a local effect, compare current authority and action state, reserve budget, apply the effect, and commit action result, outbox, optional checkpoint and cursor through one supported transaction handle. A duplicate returns the recorded result without applying another effect. Historical result retrieval and permission to start a new effect are different decisions; retain committed results even after expiry or revocation. Denied/conflicting inputs do not consume unrelated progress.

For external effects, the local transaction stages dispatch; it cannot atomically commit an arbitrary remote service. A minimal dispatch state machine is `Ready → Dispatching → Succeeded / Failed / OutcomeUnknown`, with guarded transitions. Crash after entering Dispatching requires reconciliation unless the destination provides a verified idempotent replay guarantee. Unknown does not mean Failed. Expiry stops new dispatch; it does not undo an already submitted request or justify a compensating transaction. Bounded read-only reconciliation may continue after expiry without renewing effect authority.

The [Umbra design](../../docs/product-requirements/umbradb-recovery.md) explicitly says current `saveAndAdvance` only composes checkpoint/cursor, and opens its own transaction. The proposed MPE atomic capability is future work. Its documented prototype route uses public `withTransaction` with all participating handles and create-only/CAS records; no nested `saveAndAdvance`. This review does not certify that composition. Test full state-vector recovery, actual connection durability, lease loss, stale restore and expired dispatch. At-rest encryption, freshness, replay retention and ratchet erasure remain separate responsibilities. SQLite can implement the same bounded contracts for standalone clients; backend brand does not supply authorization or remote exactly-once delivery.

## Prioritized feasible work

Effort is relative engineering size, not a measured estimate; production cryptographic/chain auditing is separate.

| Priority | Recommendation | Effort | Acceptance |
| --- | --- | --- | --- |
| P1, current | Correct E1 occurrence recording and E2 exact grammar | Small | Dedicated counterexamples reject/conflict as specified; independent interpreter agrees; reviewed replacement commitments |
| P1, before an executor | Specify stable action namespace, retarget/version migration, typed authority context and Step/budget semantics for one sandbox operation | Small–medium | Retarget, source change, policy/contract upgrade, stale authority and concurrent aggregate-budget fixtures have explicit outcomes |
| P1, before an executor | Implement bounded local action/inbox/outbox state and one atomic effect path | Medium | Concurrent replay, process death around every commit stage, durability misconfiguration and stale restore cause no second local effect or skipped progress |
| P1, before external dispatch | Add stable idempotency/attempt binding and OutcomeUnknown reconciliation | Medium | Lost response after remote commit, expiry during send and replacement attempts cannot trigger an unlinked second effect |
| P2 | Promote one observation contract per chain with endpoint/network/deployment/evidence binding | Medium | Wrong network/account/session, changed deployment, rollback, failed execution and submission-only evidence safely refuse downstream action |
| P2 | Add explicit allocation/reversal state only if invoice accounting enters scope | Medium | Repeated payment observations allocate once; revised/reversed evidence retains lineage and never becomes payment permission |

Keep the current model usable for deterministic validation while these gates remain closed. The next convincing execution demonstration is one bounded effect with independently interpreted commitments and crash/replay evidence, not more event names or a broader executor tool dictionary.
