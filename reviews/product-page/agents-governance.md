# Product-page review: agents, revocation and governance

Reviewed on 2026-10-03 against the [live page](https://charleshoskinson.github.io/midnight-express/), local `website/dist/index.html`, `app.js` and `use-cases.js`, and the canonical [use-cases.json](../../docs/product-requirements/use-cases.json) and [top-ten-use-cases.md](../../docs/product-requirements/top-ten-use-cases.md). Live `app.js` and `use-cases.js` match the local distribution byte for byte. This is a content and product review using HTTP retrieval and source inspection; it does not assess browser layout or interaction behavior.

## Main finding

The three use cases are appropriately scoped in the canonical requirements, but the visible cards leave important meaning inside undisplayed data. The card renderer presents stage, initial scope, measurement and remaining gate; it does not present the actors, trigger, acceptance scenario or dependencies. Readers therefore see technical gates without a concrete person, decision or outcome to attach them to.

Keep the technical safeguards, and add a short workflow story to each card. A consistent sequence of **Who → Trigger → Example → Intended outcome → Limitation** would explain what the proposed coordination layer contributes and what the customer's application must enforce. These remain candidate workflows and unvalidated value hypotheses.

## UC-05: human-approved agent coordination

Rank 3 · Pilot C. The proposed initial scope is an agent's bounded request, a human's signed expiring approval, and a sandbox executor that enforces target and budget.

**Who:** An enterprise worker, an AI or business agent, an approval officer and the application that executes the action.

**Trigger:** The agent proposes a purchase, settlement, access grant or another action that needs explicit permission.

**Illustrative example:** A procurement agent proposes buying from a named supplier for up to $500 before a stated deadline. The officer reviews the actual action and signs that scope. The executor checks the signer’s authority, supplier, amount and expiry. A request for $700, a different supplier or an expired approval is rejected even when the message has a valid signature and encryption seal. Retries must not cause the purchase to happen again; an external purchasing system needs idempotency or reconciliation.

**Intended outcome:** Fewer manual handoffs, a recoverable record of the proposed action and approval, and enforcement of the human's limits. Measure approval cycle time, handoffs and rejection of unauthorized or replayed actions against a customer baseline.

**Limitation:** Midnight Express carries protected instructions and approval evidence. It does not make AI output correct or trustworthy. A trusted approval interface, authority registry and application capability enforcement still need implementation. A message payload must never become an arbitrary executable command. Contract effects add the separate consumer-proof, replay and anchored-message-binding gates.

**Suggested card copy:** “An agent proposes a specific action. A person approves its target, budget and deadline; the executing application checks those limits before acting. The proposed workflow protects the request and preserves approval evidence. It does not guarantee the agent's judgment or replace application enforcement.”

## UC-06: credential and access-revocation coordination

Rank 4 · Next. The initial scope is authenticated issuer updates to backend verifiers, with explicit stale-state reporting.

**Who:** A credential issuer, the holder's wallet, and an employer or service that checks access.

**Trigger:** A credential is issued, expires or is revoked, or a staff member or partner leaves a group.

**Illustrative example:** An employer removes a contractor. The issuer sends a revocation with a newer authenticated version than the earlier grant. A verifier receives the revocation and then a delayed copy of the grant; it keeps the newer revocation. An offline verifier marks its cached status stale instead of silently permitting high-risk access. Where group encryption is enabled and removal/rekeying is correctly completed, the contractor cannot decrypt future stream generations.

**Intended outcome:** Reduce the interval during which services rely on stale access state, while protecting the sensitive update and the services following it under the selected privacy profile. Measure stale-authorization intervals, update coverage and recovery after membership changes.

**Limitation:** Receiving a revocation notice does not establish that every service has enforced it. Issuer authority, cache freshness rules and tested removal/rekeying remain prerequisites. Application owners retain responsibility for identity records, access decisions and legal effects. Rekeying restricts future access; it does not delete previously obtained plaintext or copies. OpenMLS group security remains a gated extension, not a completed launch capability.

**Suggested card copy:** “When an issuer revokes a credential or an employer removes a member, participating services receive an authenticated status update. Newer issuer versions override delayed older grants, and stale verifiers show degraded status. Enforcement and future-key removal must be tested; notice receipt alone is not completed revocation.”

## UC-09: confidential governance review and approvals

Rank 8 · Policy-gated. The initial scope is confidential review and explicit approval collection; execution policy remains application-owned.

**Who:** A board or DAO committee, authorized reviewers and an execution agent.

**Trigger:** A proposal is submitted, confidential review is requested, or the required approval threshold is reached.

**Illustrative example:** A committee privately reviews a proposed vendor contract. Its illustrative policy requires three current authorized approvals tied to the proposal. Two approvals, an expired approval or a simple delivery receipt cannot authorize the action. Once valid policy requirements are met, the executor checks the evidence before acting and rejects a replay. An auditor can receive the approval evidence without receiving unrelated deliberation, subject to the application's selective-disclosure design.

**Intended outcome:** A clearer confidential review process and a complete record of who authorized a specific action. Measure review completion time, completeness of approval evidence and replay rejection.

**Limitation:** Encrypted review is not anonymous voting. Midnight Express does not supply the customer's governance rules or automatically implement multisig/threshold authority. Participant roles, approval validity and selective disclosure must be defined and enforced by the application. On-chain execution additionally requires the signed-authority, replay and CON-060 anchored-message-binding gates. External execution still needs destination idempotency or reconciliation.

**Suggested card copy:** “A board or committee shares a confidential proposal and collects explicit approvals from authorized reviewers. Its application checks the required threshold and expiry before an action, and can prepare a limited evidence package for an auditor. Receiving a proposal is not approval, and private review does not guarantee anonymous voting.”

## Shared boundaries to keep visible

The existing journey correctly separates source authentication from permission to act. Bring that distinction into these cards: a valid signature identifies an authenticated source under the identity policy; the executor must separately check whether that source may authorize this particular action now. Publication admission, encryption, decryption ability and ledger inclusion each establish different facts; none grants business permission.

Use “requested,” “approved,” “executed” and “acknowledged” as distinct workflow states. Similarly, separate a revocation notice received from verifier policy updated and future access removed. Signed business acknowledgement is an application event, not an automatic consequence of local recognition or transport receipt.

Do not expand the page into claims of trustworthy autonomous AI, instantaneous universal revocation, deletion of past information or anonymous voting. Describe the intended value, then place the relevant unfinished application enforcement or integration gate beside it.
