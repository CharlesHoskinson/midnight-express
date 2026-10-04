# First three prototype sprints: architecture and product sequence

## Recommendation

Build one backend/desktop RFQ reference slice, make its processing survive failure, then prove that invoices and bounded human approvals can reuse it. Run the anonymous-admission feasibility work from Sprint 1 rather than hiding the most difficult dependency behind three attractive demos. Every sprint ends with reproducible evidence and a scope decision; a negative feasibility result is useful evidence, not permission to claim the requirement passed.

Assume three **two-week timeboxes** for planning, with engineering capacity for a coordination stream and a tightly bounded cryptography/platform stream. Neither staffing nor start dates are established. These are proposed timeboxes, not six-week delivery commitments. If capacity supports only one stream, reduce application breadth or extend the calendar; retain the early feasibility gate. Scope each sprint before it begins and roll blocked work forward visibly.

The existing experiments are research inputs, not the prototype. Their README explicitly disclaims a maintained proof of concept. Rust runs use a secret-readable admission stand-in, in-memory stores and a mock ledger; Compact evidence is compilation and simulator execution, not network deployment. Promote only selected, reviewed modules into an isolated reference implementation with pinned dependencies and reproducible commands. Do not rename experimental coverage into production acceptance.

## Sprint 1 — RFQ walking skeleton and difficult dependency proof

**Objective:** A buyer and two approved dealers exchange confidential RFQs and signed offers, with local recognition and explicit off-chain acceptance; independently establish whether the selected admission profile has a credible integration path.

**Entry evidence:** Reviewed original wire/expiry obligations and recommended stack; inventory of reusable experiment modules; explicit mock ledger/admission label; chosen RFQ actors and signed-role policy. A design-partner interview is desirable but not a condition for an internal synthetic demonstration.

**Ordered backlog:**

1. Establish the reference workspace, reproducible build/test entrypoint and evidence manifest. Pin library/compiler versions actually used; record host and runtime. Mark mocks at the adapter boundary and in the demo.
2. Establish a shared minimal event core (event identity, source identity, schema/profile version, correlation/causation, occurrence time and expiry) with a strict RFQ domain profile. Separate event identity, business action identity, source version, envelope EID and replay/destination keys; document their mappings. Reject unknown or unsupported versions and incompatible required fields before dispatch; never infer a profile from loose payload shape. Explicit application-owned adapters map source identity, version, snapshot/delta and finality into this model. Define versioned CloudEvents-compatible private RFQ payloads and AsyncAPI operations: request, offer, decline, accept and signed acknowledgement. Keep source/type/correlation/role selectors inside encryption; distinguish business identity from envelope EID. Specify signed invitation/role checks and RFQ states, deadlines and offer revisions.
3. Extract minimal Rust MPE sealing, byte layout, EID, authentication and recognition modules against independent vectors. Connect actual GossipSub sidecars with whole-shard reception and a minimal TypeScript-facing client. No RFQ topics or upstream recognition filters. Test sender cache/queued flush expiry as well as receiver expiry.
4. Implement request/offer/accept off-chain policy. Invalid roles, modified terms, expired offers and competing accepts must fail or resolve under an explicit application rule. In-memory state is acceptable for this sprint and visibly labeled.
5. In the first few days, timebox an admission/Registry compatibility spike: compare Zerokit and the selected Midnight relation for identity commitment, field/hash, tree, quota leaf, scope and codec. Try a genuine content-bound proof, not the secret-readable stand-in; measure encoded slot and proof generation/verification separately. Document any adapter/circuit work rather than implying drop-in Semaphore or Zerokit compatibility. One RLN-style proof must include membership and committed class-credit bounds; no second per-event Semaphore proof.
6. Probe the actual target Midnight environment/toolchain capabilities and record whether finalized Registry root acquisition and witness update can be exercised there. A compiled contract or local runtime result does not pass this network gate. Keep a signed-authority/CON-060 design note for future settlement; do not implement settlement to inflate this sprint.
7. Establish workflow evaluation measures: quote turnaround, manual handoffs, reconciliation work and integration effort. Collect customer baselines if a partner is available; otherwise label synthetic observations without savings claims.

**Demo:** A buyer requests prices, two dealers reply, and the buyer accepts one signed valid offer. An irrelevant receiver cannot decrypt it; an unauthorized sender and expired quote are rejected. Show actual transport traces without exposing payloads, plus the separate genuine-proof feasibility report or explicit blocking mismatch.

**Exit evidence:** Reproducible three-party scenario; independent wire vector comparisons; negative signature/role/expiry tests; packet/topic inspection showing no business selectors; pinned admission parameter comparison and measured candidate outputs. The feasibility report names a compatible path or states the mismatch, required custom work and next experiment. A mocked RFQ demo can pass its functional goal while genuine admission remains red. It cannot pass an anonymous-admission acceptance gate.

**Decision:** Continue the coordination prototype with its mock boundary visible. If field/tree/slot compatibility is unresolved, re-plan the proof stream before expanding promises. Do not silently weaken the wire or quota requirements.

## Sprint 2 — Durable RFQ processing and measured recovery

**Objective:** The same RFQ workflow preserves accepted terms and explicit progress across duplicate delivery, process failure and reconnect, without mistaking transport delivery for business completion.

**Entry evidence:** Sprint 1 RFQ/schema/SDK scenario passes; state transitions and evidence labels are agreed; admission feasibility has a documented result and owner. A genuine proof is a prerequisite for an admission claim, not for testing bounded local workflow recovery.

**Ordered backlog:**

1. Implement the trusted Node >=24 workflow host with UmbraDB/PostgreSQL, one writer and one public transaction handle. For this prototype compose temporal records, dedup, local effect, outbox, checkpoint and watermark within the same `withTransaction` boundary. The proposed future MPE helper is unavailable; current `saveAndAdvance` alone does not supply this atomic composition and must not open a nested transaction. If public API composition fails, report the blocker and use an explicitly documented, verified caller implementation before making a recovery claim. Standalone Rust nodes use SQLite only for the durable state needed by this slice.
2. Prove recovery semantics against the shared model: immutable event identity, ordering/version rules, causation, source freshness, snapshot/delta catch-up and gap handling must survive restart. Persist an authenticated inbox before handling. Commit valid RFQ state, dedup key, signed acknowledgement outbox, checkpoint and cursor together. Reject concurrent duplicate acceptance; do not advance past an uncommitted local effect. Restrict restore to matching application/network/schema context and test an older checkpoint against newer durable dedup state.
3. Expose bounded demand, cancellable listeners and isolated handler errors in the SDK. `once` describes listener lifetime, not business exactly-once execution. Cancellation stays local; it does not transmit private subscription selectors. Separate admitted, retained, processed, acknowledged and business-accepted statuses.
4. Add bounded retry age and encrypted local quarantine. Keep the same EID/expiry on retransmission of the same envelope. Explicitly authorize redrive; expiry still applies. Exercise malformed/poison events without blocking unrelated handlers indefinitely.
5. Introduce one bounded persistent opaque store/replay fixture and disconnect/reconnect catch-up using whole-shard or whole-window inventories. Show expired history and gaps. Local persistent retention demonstrates a recovery slice; it does not demonstrate replicated retention, independent operator receipts or promised availability.
6. Continue the genuine admission path established in Sprint 1. Test canonical network/Registry/window/class/index scopes, quota bounds, envelope substitution, insertion/removal witnesses, stale roots and root-change quota non-renewal. If an actual finalized-root source exists, use it; otherwise preserve the simulator boundary. Test duplicate versus conflicting envelopes and restart-safe local admission state.

**Demo:** Accept a quote, kill the workflow host at selected commit/outbox boundaries, reconnect and replay the input. Recover one accepted record and its explicit acknowledgement, with no lost committed state or duplicate local effect. Show an expired retry, a gap and an isolated failing handler. Show admission progress separately.

**Exit evidence:** An automated fault matrix records outcomes before transaction commit, after commit before acknowledgement, and during retry. Concurrent duplicates produce one local accepted effect; rollback leaves no cursor beyond that effect. Restart/restore, gap, expiry and quarantine/redrive scenarios pass. Record recovery time, replay count and event age under declared synthetic conditions, not SLA claims. Admission report includes negative vectors, real/stand-in status and unresolved Registry integration gates.

**Decision:** Reuse the durable core only after its transaction/fault evidence passes. If recovery is incomplete, Sprint 3 fixes it before adding workflow breadth. Do not market exactly-once external execution from a local transaction.

## Sprint 3 — Reuse for invoices and bounded agent approvals

**Objective:** Demonstrate that a stable event/recovery core supports invoice status matching and human-approved sandbox actions without inventing a separate broker or authorization system for each workflow.

**Entry evidence:** Sprint 2 durable RFQ fault matrix passes; common signed-policy, event identity and destination-idempotency interfaces are stable; admission gaps remain visible. Select one invoice fixture and one sandbox action, rather than broad ERP or agent platform integrations.

**Ordered backlog:**

1. Reuse the minimal event core through strict invoice and agent domain profiles; do not extend the universal core with RFQ-, invoice- or agent-specific fields. Pin supported schema/profile versions, reject unknown versions, and publish explicit adapter mappings and domain transition rules. Add a minimal invoice/payment-status adapter with declared source identity, version/finality and authentication. A signed synthetic payment fixture must be labeled as such; an adapter signature authenticates its source claim, not the underlying bank payment. Reject wrong invoice, amount/currency, stale source versions and untrusted payment evidence. Keep unresolved matches for human review; no payment execution.
2. Feed invoice events through the same durable inbox/dedup/outbox/cursor transaction as RFQ. Send a sandbox ERP posting with a stable destination idempotency key and reconciliation path. Inject a failure after destination success before local confirmation; prove the receiver does not produce a second posting or exposes the ambiguity for reconciliation. If a destination cannot provide idempotency or queryable reconciliation, disable automatic retry and show manual resolution.
3. Define signed agent proposals and human approvals bound to exact proposal/action, target, budget, expiry and application/network context. Build a trusted approval view and sandbox executor; authentic message delivery alone grants no capability. Enforce policy at execution, including replay, changed target, excess budget, denied/revoked and expired approvals. An agent may be a deterministic fixture; LLM integration is not required to prove policy.
4. Reuse the same fault harness for invoices and approvals. Use shared SDK components and common evidence/status meanings; keep workflow-specific policy explicit. Measure adapter code/effort and fault coverage to support the reuse claim.
5. Close or disposition the admission feasibility gate. Record genuine encoded Admission Slot size against <=4096 bytes and verification against <=10 ms on the specified VM; record host, distributions/load, proving time and witness-update cost separately. A candidate result on a different host is preliminary. The exact original wire profile and fixed slot fit must also pass; the <=4096-byte ceiling is not authorization to enlarge a fixed wire field. Include commitment/tree vectors, conflicting-share recovery and finalized-root/revocation behavior where integrated. An incomplete custom circuit remains a blocker, never substituted by the stand-in.
6. Produce a pilot decision pack: customer baseline/evidence if available; observed turnaround and handling effort; integration cost; crash/duplicate results; privacy boundary and operator-cost assumptions; explicit red production gates. Choose whether to seek a constrained design-partner pilot, repeat a blocked sprint or commission the missing feasibility work.

**Demo:** An authenticated payment-status fixture matches an invoice; replay and an injected ambiguous destination completion do not double-post. A person approves one sandbox agent action; changed supplier, excess budget, expiry and replay all fail. Restart the host during each workflow and retain the same authorized state. Finish with an admission evidence dashboard that distinguishes genuine proofs, mocks and blocked gates.

**Exit evidence:** Both use cases run through the same durable core, with negative authority and destination-recovery cases. Record one local outcome per business action and destination reconciliation evidence for external outcomes. Evidence bundle includes commands, versions, environment, source-fixture labels, logs, traces and known gaps. Savings remain hypotheses until compared with a customer baseline. A pilot recommendation must state which privacy, admission, retention and ledger assurances it actually includes.

## Boundary after three sprints

Expected outcome: a reviewed backend/desktop reference slice for RFQ, invoice-status matching and bounded human approval; reproducible failure evidence; a measured admission feasibility result. This is sufficient to decide further investment or a explicitly constrained partner evaluation. It does not establish production readiness.

Remaining production gates include genuine anonymous admission against authoritative finalized Midnight Registry roots; exact profile/wire conformance and independent cryptographic review; durable replicated opaque retention with signed independent-operator receipts; measured WAN/load/failure behavior and funded operator economics; hardened keys/restore/access controls; and deployment/operations evidence. No replicated retention or availability claim follows from PostgreSQL or SQLite.

Settlement additionally requires signed business authority, atomic replay protection and CON-060 anchored-message binding. Existing inclusion-only consumer experiments cannot authorize business effects. Contract-origin private notifications additionally require underlying private-event capability and exact carried-byte/applied-phase checks. No automatic settlement, payment execution or unrestricted agent execution belongs in these three sprints.

Defer OpenMLS deployment until its identity, epoch/removal, metadata, MPE wire fit, crash recovery and erasure gates pass. Keep the initial symmetric profile's lack of forward secrecy and ingress anonymity visible. Signal is an alternative, not a parallel first dependency. Private mobile discovery/retrieval, Tor/Arti, additional chains and broad ERP connectors remain separate later tracks.

## Suggested Implementation tab presentation

Lead with: **“Three proposed prototype sprints. RFQ first; prove recovery; reuse the core.”** Put “Two weeks each: planning assumption, not a launch commitment” adjacent to the sequence. Each sprint card should present objective, build scope, demo and required evidence, with detail expansion for entry criteria and negative scenarios. Present the difficult admission work as a visible cross-sprint track starting in Sprint 1. Mark each item Proposed, Mock permitted for internal demo, Genuine proof required, or Blocked by platform capability as appropriate.

Provide a distinct production-gates block after the cards; do not label Sprint 3 a production release. Link the tab to the recommended stack, experiment disclaimers and exact requirement/evidence documents. The existing Delivery section describes broader product sequencing; Implementation should show this concrete prototype slice without converting the broader sequence into a six-week commitment.

## Local evidence reviewed

- `docs/product-requirements/recommended-stack-and-use-cases.md`: RFQ first; invoice and agent reuse; explicit production, OpenMLS, ledger and mobile gates.
- `docs/product-requirements/proposed-stack.md`: membership/witness API boundaries; single proof; compatibility, quotas and finalized roots.
- `docs/product-requirements/umbradb-recovery.md`: public transaction composition and distinction from `saveAndAdvance`, retention and finality.
- `experiments/README.md`, `COVERAGE.md`, `registry/README.md`, `registry/RESULTS.md`: exploratory scope, stand-in secrets, mock ledger and compiler/simulator limitations.
- `website/dist/index.html`: present design-stage language, workflows and Delivery/Architecture context for the new tab.
