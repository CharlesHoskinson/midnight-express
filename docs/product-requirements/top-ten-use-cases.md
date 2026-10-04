# Ten use cases ranked against the recommended stack

Start with confidential quote coordination on backend and desktop applications. Invoice matching and human-approved agent work would reuse its signed events, permission checks and recovery. The remaining candidates need additional integrations or security capabilities.

This is a proposed portfolio. Ranking weighs confidentiality, reuse of the selected stack, measurable customer outcomes and remaining dependencies. Demand and revenue have not been validated. UC identifiers remain stable; the ranks replace the earlier exploratory order.

See the [consolidated recommendation](recommended-stack-and-use-cases.md), [working stack and interfaces](proposed-stack.md), [comparative event-systems research](../../reviews/competitive-event-systems/README.md), and [candidate requirements](candidate-ears.md).

| Rank | Use case | Stage |
|---|---|---|
| 1 | [Institutional RFQ and negotiated quote coordination](#uc-01) | Pilot A |
| 2 | [Invoice, payment-status and reconciliation workflows](#uc-03) | Pilot B |
| 3 | [Agent coordination with bounded human approvals](#uc-05) | Pilot C |
| 4 | [Credential and access-revocation coordination](#uc-06) | Next |
| 5 | [Procurement and supply-chain exception coordination](#uc-07) | Next |
| 6 | [Private contract lifecycle notifications](#uc-02) | Ledger-gated |
| 7 | [Confidential incident and cross-chain operations coordination](#uc-10) | Connector-gated |
| 8 | [Private governance review and approval workflows](#uc-09) | Policy-gated |
| 9 | [Portfolio and collateral risk alerts](#uc-04) | Freshness/mobile-gated |
| 10 | [Insurance claim handoffs and milestones](#uc-08) | Sector-gated |

<a id="uc-01"></a>
## UC-01: Institutional RFQ and negotiated quote coordination

A buyer asks authorized dealers for a price. The dealers return signed offers, and the buyer accepts one before its expiry. Compliance reviewers and settlement staff need the accepted terms and a record of who approved them. The pilot would test whether confidential quote exchange reduces disclosure of trade intent and counterparty relationships while shortening reconciliation and the settlement handoff.

**Stack fit:** MPE coordination + private schemas + signed roles + local recovery

**Initial delivery scope:** Start with requests, signed quotes, expiry and off-chain acceptance; enable settlement only after authority/replay/anchored-binding gates.

**Measure in the pilot:** Quote turnaround, reconciliation effort and successful outage recovery.

**Remaining gates:** First design partner; CON-060 and contract adapter gate automated settlement.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.

**Product requirements to consider:** Versioned RFQ/offer/accept/expire state machine, correlation policy, role/history permissions and explicit settlement handoff.

**Acceptance scenario for the full workflow:** Two dealers return independently signed offers; expired/altered/replayed acceptance cannot settle, authorized acceptance settles once; crash recovery preserves accepted offer, unauthorized party cannot read content. Transcript analysis assesses interest privacy without claiming global timing anonymity.

**Dependencies:** Proof-capable signed-consumption implementation, role/key management, contract adapter, pilot dealer workflows. Start on backend/desktop.

**Candidate platform links:** [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-03"></a>
## UC-03: Invoice, payment-status and reconciliation workflows

A supplier’s finance system and a purchaser’s treasury team need to agree whether an invoice has been issued, approved, paid, disputed or refunded. Signed invoice updates and authenticated notices from a bank, payment service or Midnight settlement adapter would give them records to match. The proposed benefit is less manual matching while keeping amounts, account relationships and invoice contents private.

**Stack fit:** MPE coordination + durable processing + ERP/payment adapter

**Initial delivery scope:** Match invoices and authenticated payment-status notices; no automatic payment execution in initial pilot.

**Measure in the pilot:** Unmatched invoices, manual handling time and duplicate postings.

**Remaining gates:** ERP integration and authenticated payment evidence; destination idempotency for external effects.

**Existing requirements:** MPE-FMT-022, MPE-FMT-026, MPE-FMT-034, MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033, MPE-CON-043, MPE-CON-046; MPE-SEC-032, MPE-SEC-038.

**Product requirements to consider:** Invoice/payment/receipt identifiers, ERP connector and signed reconciliation schema; invoice attachment remains explicit fetch.

**Acceptance scenario for the full workflow:** Same invoice emitted through retries is posted once; wrong-amount payment never marks paid; disconnect/restart catches up; failure receipt never executes payment; sensitive invoice data absent from broker logs.

**Dependencies:** ERP/treasury connector, payment-origin evidence, customer authorization policy and deployment funding.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-05"></a>
## UC-05: Agent coordination with bounded human approvals

An enterprise worker’s agent proposes a purchase, settlement, access grant or other bounded action. An approval officer reviews the proposal and signs the permitted target, budget and expiry; the executor must enforce those limits. The pilot would test whether protected instructions and explicit approvals let teams automate this work with fewer manual handoffs.

**Stack fit:** MPE coordination + signed action policy + durable processing

**Initial delivery scope:** Agent proposes a bounded action; human signs an expiring approval; sandbox executor enforces target and budget.

**Measure in the pilot:** Approval cycle time, manual handoffs and rejected unauthorized/replayed actions.

**Remaining gates:** Application capability enforcement and trusted human approval UI; contract effects require consumer proof.

**Existing requirements:** MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-048; MPE-SEC-032, MPE-SEC-037, MPE-SEC-038; MPE-CRY-022.

**Product requirements to consider:** Capability-scoped delegation, signed approval schema, action budgets and approval expiry.

**Acceptance scenario for the full workflow:** Agent requests action outside budget or to different target; reject despite valid message seal; approved in-scope action happens once; no arbitrary payload command execution.

**Dependencies:** Authority registry, application enforcement, human approval UI. MPE delivery itself cannot make AI output trustworthy.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-06"></a>
## UC-06: Credential and access-revocation coordination

An issuer updates a credential when it is issued, expires or is revoked. Employers and service verifiers also need to respond when a staff member or partner loses access. Authenticated updates would help the subject’s wallet and each verifier maintain current status without publishing their subscription relationships. The proposed benefit is a shorter interval in which stale evidence can support an access decision.

**Stack fit:** MPE coordination + issuer adapter + group/rekey policy

**Initial delivery scope:** Propagate authenticated issuer epochs to backend verifiers and mark stale state explicitly.

**Measure in the pilot:** Stale authorization interval, update coverage and membership-change recovery.

**Remaining gates:** Issuer authority, stale-cache policy and tested removal/rekey; event receipt is not revocation completion.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-SEC-020, MPE-SEC-028, MPE-SEC-033; MPE-CON-052, MPE-CON-058, MPE-CON-059.

**Product requirements to consider:** Versioned issuer lifecycle events and freshness/epoch semantics for verifier caches.

**Acceptance scenario for the full workflow:** Revocation arrives after a delayed grant; higher authenticated issuer epoch wins; removed user cannot decrypt future stream generation; offline verifier reports stale rather than granting high-risk access silently.

**Dependencies:** Issuer-origin verification, onboarding policy, group rekey; identity records and legal effect remain application-owned.

**Candidate platform links:** [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-013`](candidate-ears.md#mpe-prd-013).

<a id="uc-07"></a>
## UC-07: Procurement and supply-chain exception coordination

A buyer, supplier and logistics provider exchange milestones when an order is accepted or a delivery progresses. A delay or temperature anomaly may require a decision from the buyer and information for an authorized insurer or auditor. Restricted notices would let those participants resolve the exception while limiting disclosure of commercial counterparties and terms.

**Stack fit:** MPE coordination + group roles + connector schemas + history policy

**Initial delivery scope:** Share signed delivery milestones and restricted exception notices among buyer, supplier and logistics actors.

**Measure in the pilot:** Exception resolution time, missed handoffs and connector integration effort.

**Remaining gates:** Authenticated gateways and archive/key policy; sensor provenance does not prove physical truth.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033; MPE-STO-022, MPE-STO-025.

**Product requirements to consider:** Role-scoped milestone schema, selective disclosure and signed sensor/operator provenance.

**Acceptance scenario for the full workflow:** Authorized members recover milestones after outage within retention; unrelated member cannot read restricted events; sensor report is attributed but not falsely treated as proof the physical shipment occurred.

**Dependencies:** Enterprise/IoT gateway authentication, archived history policy if retention needed beyond ordinary window; commercially sensitive timestamps still require threat model.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-02"></a>
## UC-02: Private contract lifecycle notifications

A wallet user waits for a settlement, escrow milestone or authorization change. A contract observer sends an update that the application can check against ledger evidence before showing it as confirmed. The proposed benefit is useful, timely status without publishing the user’s subscription interests or private business data.

**Stack fit:** MPE coordination + finalized Midnight adapter + listener SDK

**Initial delivery scope:** Desktop/backend public-event or signed-application pilot first; private carried events follow underlying Midnight capability.

**Measure in the pilot:** Finality-label correctness, missed-event recovery and application integration time.

**Remaining gates:** Private carried-event capability, exact-byte/applied-phase verification; private mobile delivery is separately gated.

**Existing requirements:** MPE-FMT-054, MPE-FMT-055, MPE-FMT-056, MPE-FMT-057, MPE-FMT-058; MPE-CON-015, MPE-CON-016, MPE-CON-017, MPE-CON-058, MPE-CON-059, MPE-CON-062, MPE-CON-063; MPE-SEC-022, MPE-SEC-025, MPE-SEC-026.

**Product requirements to consider:** Wallet UX templates and app-permission manifest; explicit delivery-state UI.

**Acceptance scenario for the full workflow:** Delivered event remains provisional until exact bytes/position and successful applied phase are confirmed; failed fallible phase never final; revoked wallet app cannot decrypt future epochs after rekeying; previously readable messages remain readable.

**Dependencies:** Private event feature MPS-0005 Part 2 for private carried events, finalized-chain verification, mobile-efficient privacy profile for broad adoption. Public events can pilot earlier.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-011`](candidate-ears.md#mpe-prd-011), [`MPE-PRD-013`](candidate-ears.md#mpe-prd-013), [`MPE-PRD-014`](candidate-ears.md#mpe-prd-014).

<a id="uc-10"></a>
## UC-10: Confidential incident and cross-chain operations coordination

A service interruption, key compromise or delayed settlement brings operations staff, service owners and authorized responders into the same investigation. Chain adapters provide updates whose source and finality the team must assess. Confidential notices could speed response handoffs and reduce dependence on a single public notification provider, with an independent emergency channel available if MPE fails.

**Stack fit:** MPE coordination + failure isolation + encrypted quarantine + connector trust

**Initial delivery scope:** Coordinate human-reviewed response using an independent emergency channel alongside MPE.

**Measure in the pilot:** Response handoff time, recovered notices and failed-handler isolation.

**Remaining gates:** Declared cross-chain trust/finality, funded operators and alternate emergency path.

**Existing requirements:** MPE-SEC-028, MPE-SEC-032, MPE-SEC-036; MPE-CON-025a, MPE-CON-025b, MPE-CON-050, MPE-CON-051, MPE-CON-056; MPE-STO-022; MPE-CRY-026.

**Product requirements to consider:** Encrypted failure queue, scoped incident actions, cross-system adapters and private operational dashboard.

**Acceptance scenario for the full workflow:** Simulated ledger outage keeps gossip notices flowing while reaction returns typed failure; operator redrive cannot execute stale/unauthorized command; handler crash does not silence other incident streams.

**Dependencies:** Out-of-band emergency recovery route, operator funding and SLOs. Do not position unproven overlay as sole safety-critical incident path or millisecond industrial control.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-003`](candidate-ears.md#mpe-prd-003), [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-09"></a>
## UC-09: Private governance review and approval workflows

A board or DAO committee circulates a proposal for confidential review. Reviewers submit explicit approvals, and an execution agent checks whether the committee’s threshold has been met. The proposed workflow would give the committee auditable authorization evidence while protecting deliberations and reviewer subscription interests.

**Stack fit:** MPE coordination + group roles + signed threshold policy

**Initial delivery scope:** Coordinate confidential review and collect explicit approvals; execution policy remains application-owned.

**Measure in the pilot:** Review completion time, complete approval evidence and replay rejection.

**Remaining gates:** Threshold/multisig authority, selective disclosure and CON-060 before on-chain execution; no anonymous voting claim.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-033, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-052, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.

**Product requirements to consider:** Threshold approval/evidence schema, participant role policy and narrow disclosure package.

**Acceptance scenario for the full workflow:** Insufficient/expired approvals cannot authorize action; authorized threshold effect commits once; evidence disclosed to auditor excludes unrelated deliberation; receipt of proposal is not approval.

**Dependencies:** Application multisig/threshold authorization and governance policy; no implicit private voting anonymity guarantee.

**Candidate platform links:** [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-04"></a>
## UC-04: Portfolio and collateral risk alerts

An account owner needs to know about a margin breach, liquidation risk, expiring order or abnormal exposure. A risk engine would send advisory updates to the owner or an explicitly delegated agent, showing whether its underlying data is current. The candidate aims to support earlier intervention without broadcasting the portfolio or watchlist to notification infrastructure.

**Stack fit:** MPE coordination + source snapshot/delta adapters + freshness guards

**Initial delivery scope:** Backend advisory alerts first; block automated effects on stale/gapped feeds.

**Measure in the pilot:** Alert freshness, gap detection and recipient intervention time.

**Remaining gates:** Reliable market connectors and proven budgets; no hard-real-time liquidation guarantee; private phones need retrieval.

**Existing requirements:** MPE-CON-020, MPE-CON-024, MPE-CON-028, MPE-CON-039, MPE-CON-043, MPE-CON-046, MPE-CON-056; MPE-SEC-025, MPE-SEC-032, MPE-SEC-037; MPE-PRF-020.

**Product requirements to consider:** Snapshot/delta risk schema, freshness policy, authenticated source connectors and bounded delegation.

**Acceptance scenario for the full workflow:** Stale or gapped feed displays degraded status and blocks automated high-risk effect; replayed warning cannot trigger repeated action; timely processing measured under reference workload, no hard-real-time liquidation guarantee.

**Dependencies:** Hyperliquid/Solana/Ethereum adapters with declared trust/finality; mobile private delivery; external market data reliability.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-003`](candidate-ears.md#mpe-prd-003), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-011`](candidate-ears.md#mpe-prd-011), [`MPE-PRD-014`](candidate-ears.md#mpe-prd-014), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-08"></a>
## UC-08: Insurance claim handoffs and milestones

A claimant, insurer and adjuster exchange updates as a claim is submitted, evidence is requested and an assessment is completed. Authorized payment or reinsurance partners join the relevant handoffs when payment is approved. Restricting evidence to the assigned roles could reduce repeated document requests and processing delays while limiting exposure of claimant information.

**Stack fit:** MPE coordination + role-scoped attachments + long-history policy

**Initial delivery scope:** Exchange status and authorized encrypted-document references among claimant, insurer and adjuster.

**Measure in the pilot:** Claim handoff time, missing-document requests and duplicate payment prevention.

**Remaining gates:** Customer data/retention policy, encrypted object integration and authorized retrieval; expiry does not erase copies.

**Existing requirements:** MPE-FMT-038; MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-046, MPE-CON-052; MPE-SEC-032.

**Product requirements to consider:** Claims-state schemas, attachment grants and retention/data-handling policy; large documents live in authorized encrypted storage.

**Acceptance scenario for the full workflow:** Wrong role cannot open sensitive evidence; withdrawal blocks future access but does not promise deleting obtained copies; approval is authenticated and duplicate message cannot duplicate payment.

**Dependencies:** Sector-specific governance/privacy/legal review by customer, encrypted object service, long-history requirements. Do not assume protocol expiry erases copies.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

## Shared recovery choice

The proposed backend for these workflows uses UmbraDB/PostgreSQL in a trusted Node backend host for Midnight-aware temporal state, checkpoints and cursor recovery; standalone Rust/client deployments may use SQLite. The MPE atomic processing/protected-restore capability is a future UmbraDB release, not current 0.9.5 behavior. See [integration requirements](umbradb-recovery.md).

## Portfolio acceptance

The first three pilots share the same private event SDK, durable handling and authenticated workflow layer. Measure the value of off-chain coordination before enabling automatic contract effects. All production uses require real admission, finalized membership state, funded storage/operators, measured recovery and independent security evidence. Group security and on-chain effect authorization each retain their own gates.

For each pilot record the customer/owner, current process/cost, threat model, baseline measurement, numeric target agreed with the customer, engineering estimate and adoption decision. Large attachments remain authorized encrypted references. Delivery, persistence, anchoring, processing and business completion are distinct states; no transport-only exactly-once claim.
