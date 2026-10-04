# Ten candidate use cases

Status: **for consideration**. Ranking is a product judgment about privacy need, pilot feasibility and measurable value, not validated demand, revenue or an approved roadmap. Business value remains a hypothesis until customer interviews and pilots establish it. These are use cases, distinct from feature priorities.

The three independent reviewers studied every comparison system before this portfolio was added. See [review coverage](../../reviews/competitive-event-systems/README.md). Candidate platform requirements are in [candidate-ears.md](candidate-ears.md); existing protocol obligations remain authoritative.

## Ranked portfolio

| Rank | Use case | Proposed next step |
|---|---|---|
| 1 | [Confidential Institutional RFQ And Quote Acceptance](#uc-01) | Backend/desktop reference pilot |
| 2 | [Private Smart-Contract Status And Lifecycle Notifications](#uc-02) | Customer discovery and dependency assessment |
| 3 | [Confidential Invoice, Payment And Reconciliation](#uc-03) | Customer discovery and dependency assessment |
| 4 | [Private Portfolio And Collateral Risk Alerts](#uc-04) | Customer discovery and dependency assessment |
| 5 | [Delegated Agent Coordination And Human Approval](#uc-05) | Customer discovery and dependency assessment |
| 6 | [Credential, Membership And Access-Revocation Updates](#uc-06) | Customer discovery and dependency assessment |
| 7 | [Consortium Procurement And Supply-Chain Exceptions](#uc-07) | Customer discovery and dependency assessment |
| 8 | [Confidential Insurance Claim Handoff And Milestones](#uc-08) | Customer discovery and dependency assessment |
| 9 | [Private Governance Proposal, Review And Approval Workflow](#uc-09) | Customer discovery and dependency assessment |
| 10 | [Confidential Enterprise Incident And Cross-Chain Operations Coordination](#uc-10) | Customer discovery and dependency assessment |

## Use-case requirements and gates

<a id="uc-01"></a>
### UC-01: Confidential Institutional RFQ And Quote Acceptance

**Actors:** buyer, authorized dealers, compliance reviewer, settlement agent.

**Trigger:** buyer requests a priced offer; dealers reply; buyer accepts one signed offer.

**Business value hypothesis:** Less disclosure of trade intent and counterparties; shorter reconciliation and settlement handoff.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.

**Product requirements to consider:** Versioned RFQ/offer/accept/expire state machine, correlation policy, role/history permissions and explicit settlement handoff.

**Acceptance scenario:** Two dealers return independently signed offers; expired/altered/replayed acceptance cannot settle, authorized acceptance settles once; crash recovery preserves accepted offer, unauthorized party cannot read content. Transcript analysis assesses interest privacy without claiming global timing anonymity.

**Dependencies:** Proof-capable signed-consumption implementation, role/key management, contract adapter, pilot dealer workflows. Start on backend/desktop.

**Candidate platform links:** [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-02"></a>
### UC-02: Private Smart-Contract Status And Lifecycle Notifications

**Actors:** dapp user, wallet, contract observer.

**Trigger:** contract event such as settlement completion, escrow milestone or authorization change.

**Business value hypothesis:** Timely useful notifications without publishing subscription interests or exposing private business data.

**Existing requirements:** MPE-FMT-054, MPE-FMT-055, MPE-FMT-056, MPE-FMT-057, MPE-FMT-058; MPE-CON-015, MPE-CON-016, MPE-CON-017, MPE-CON-058, MPE-CON-059, MPE-CON-062, MPE-CON-063; MPE-SEC-022, MPE-SEC-025, MPE-SEC-026.

**Product requirements to consider:** Wallet UX templates and app-permission manifest; explicit delivery-state UI.

**Acceptance scenario:** Delivered event remains provisional until exact bytes/position and successful applied phase are confirmed; failed fallible phase never final; revoked wallet app cannot decrypt future epochs after rekeying; previously readable messages remain readable.

**Dependencies:** Private event feature MPS-0005 Part 2 for private carried events, finalized-chain verification, mobile-efficient privacy profile for broad adoption. Public events can pilot earlier.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-011`](candidate-ears.md#mpe-prd-011), [`MPE-PRD-013`](candidate-ears.md#mpe-prd-013), [`MPE-PRD-014`](candidate-ears.md#mpe-prd-014).

<a id="uc-03"></a>
### UC-03: Confidential Invoice, Payment And Reconciliation

**Actors:** supplier finance system, purchaser treasury, bank/payment or Midnight settlement adapter.

**Trigger:** invoice issued, approved, paid, disputed or refunded.

**Business value hypothesis:** Reduce manual matching while protecting amounts, account relationships and invoice contents.

**Existing requirements:** MPE-FMT-022, MPE-FMT-026, MPE-FMT-034, MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033, MPE-CON-043, MPE-CON-046; MPE-SEC-032, MPE-SEC-038.

**Product requirements to consider:** Invoice/payment/receipt identifiers, ERP connector and signed reconciliation schema; invoice attachment remains explicit fetch.

**Acceptance scenario:** Same invoice emitted through retries is posted once; wrong-amount payment never marks paid; disconnect/restart catches up; failure receipt never executes payment; sensitive invoice data absent from broker logs.

**Dependencies:** ERP/treasury connector, payment-origin evidence, customer authorization policy and deployment funding.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-04"></a>
### UC-04: Private Portfolio And Collateral Risk Alerts

**Actors:** account owner, risk engine, delegated agent.

**Trigger:** margin breach, liquidation risk, expiring order or abnormal exposure.

**Business value hypothesis:** Earlier intervention without broadcasting portfolio/watchlist to notification infrastructure.

**Existing requirements:** MPE-CON-020, MPE-CON-024, MPE-CON-028, MPE-CON-039, MPE-CON-043, MPE-CON-046, MPE-CON-056; MPE-SEC-025, MPE-SEC-032, MPE-SEC-037; MPE-PRF-020.

**Product requirements to consider:** Snapshot/delta risk schema, freshness policy, authenticated source connectors and bounded delegation.

**Acceptance scenario:** Stale or gapped feed displays degraded status and blocks automated high-risk effect; replayed warning cannot trigger repeated action; timely processing measured under reference workload, no hard-real-time liquidation guarantee.

**Dependencies:** Hyperliquid/Solana/Ethereum adapters with declared trust/finality; mobile private delivery; external market data reliability.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-003`](candidate-ears.md#mpe-prd-003), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-011`](candidate-ears.md#mpe-prd-011), [`MPE-PRD-014`](candidate-ears.md#mpe-prd-014), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-05"></a>
### UC-05: Delegated Agent Coordination And Human Approval

**Actors:** enterprise worker, AI/business agent, approval officer, effect executor.

**Trigger:** agent proposes purchase, settlement, access grant or other bounded action.

**Business value hypothesis:** Automate multi-party work with accountable approvals and protected instructions.

**Existing requirements:** MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-048; MPE-SEC-032, MPE-SEC-037, MPE-SEC-038; MPE-CRY-022.

**Product requirements to consider:** Capability-scoped delegation, signed approval schema, action budgets and approval expiry.

**Acceptance scenario:** Agent requests action outside budget or to different target; reject despite valid message seal; approved in-scope action happens once; no arbitrary payload command execution.

**Dependencies:** Authority registry, application enforcement, human approval UI. MPE delivery itself cannot make AI output trustworthy.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015).

<a id="uc-06"></a>
### UC-06: Credential, Membership And Access-Revocation Updates

**Actors:** issuer, subject wallet, employer/service verifier.

**Trigger:** credential issued/expired/revoked or staff/partner removed.

**Business value hypothesis:** Reduce stale authorization while avoiding public subscription graph.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-SEC-020, MPE-SEC-028, MPE-SEC-033; MPE-CON-052, MPE-CON-058, MPE-CON-059.

**Product requirements to consider:** Versioned issuer lifecycle events and freshness/epoch semantics for verifier caches.

**Acceptance scenario:** Revocation arrives after a delayed grant; higher authenticated issuer epoch wins; removed user cannot decrypt future stream generation; offline verifier reports stale rather than granting high-risk access silently.

**Dependencies:** Issuer-origin verification, onboarding policy, group rekey; identity records and legal effect remain application-owned.

**Candidate platform links:** [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-013`](candidate-ears.md#mpe-prd-013).

<a id="uc-07"></a>
### UC-07: Consortium Procurement And Supply-Chain Exceptions

**Actors:** buyer, supplier, logistics provider, insurer/auditor.

**Trigger:** purchase order accepted, delivery milestone reached, delay/temperature anomaly detected.

**Business value hypothesis:** Faster exception resolution with limited sharing of commercial counterparties and terms.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033; MPE-STO-022, MPE-STO-025.

**Product requirements to consider:** Role-scoped milestone schema, selective disclosure and signed sensor/operator provenance.

**Acceptance scenario:** Authorized members recover milestones after outage within retention; unrelated member cannot read restricted events; sensor report is attributed but not falsely treated as proof the physical shipment occurred.

**Dependencies:** Enterprise/IoT gateway authentication, archived history policy if retention needed beyond ordinary window; commercially sensitive timestamps still require threat model.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-007`](candidate-ears.md#mpe-prd-007), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-08"></a>
### UC-08: Confidential Insurance Claim Handoff And Milestones

**Actors:** claimant, insurer, adjuster, payment/reinsurance partner.

**Trigger:** claim submitted, evidence requested, assessment completed or payment approved.

**Business value hypothesis:** Faster multi-party processing with narrowed exposure of claimant facts.

**Existing requirements:** MPE-FMT-038; MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-046, MPE-CON-052; MPE-SEC-032.

**Product requirements to consider:** Claims-state schemas, attachment grants and retention/data-handling policy; large documents live in authorized encrypted storage.

**Acceptance scenario:** Wrong role cannot open sensitive evidence; withdrawal blocks future access but does not promise deleting obtained copies; approval is authenticated and duplicate message cannot duplicate payment.

**Dependencies:** Sector-specific governance/privacy/legal review by customer, encrypted object service, long-history requirements. Do not assume protocol expiry erases copies.

**Candidate platform links:** [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-006`](candidate-ears.md#mpe-prd-006), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-09"></a>
### UC-09: Private Governance Proposal, Review And Approval Workflow

**Actors:** board/DAO committee, reviewers, execution agent.

**Trigger:** proposal submitted, confidential review requested, approval threshold met.

**Business value hypothesis:** Coordinate sensitive deliberation and auditable authorization without exposing reviewer watchlists.

**Existing requirements:** MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-033, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-052, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.

**Product requirements to consider:** Threshold approval/evidence schema, participant role policy and narrow disclosure package.

**Acceptance scenario:** Insufficient/expired approvals cannot authorize action; authorized threshold effect commits once; evidence disclosed to auditor excludes unrelated deliberation; receipt of proposal is not approval.

**Dependencies:** Application multisig/threshold authorization and governance policy; no implicit private voting anonymity guarantee.

**Candidate platform links:** [`MPE-PRD-008`](candidate-ears.md#mpe-prd-008), [`MPE-PRD-012`](candidate-ears.md#mpe-prd-012), [`MPE-PRD-015`](candidate-ears.md#mpe-prd-015), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

<a id="uc-10"></a>
### UC-10: Confidential Enterprise Incident And Cross-Chain Operations Coordination

**Actors:** security/operations teams, service owner, chain adapter, authorized responders.

**Trigger:** service degradation, key compromise, delayed settlement or chain interruption.

**Business value hypothesis:** Faster coordinated response with protected incident details and less dependence on one public notification provider.

**Existing requirements:** MPE-SEC-028, MPE-SEC-032, MPE-SEC-036; MPE-CON-025a, MPE-CON-025b, MPE-CON-050, MPE-CON-051, MPE-CON-056; MPE-STO-022; MPE-CRY-026.

**Product requirements to consider:** Encrypted failure queue, scoped incident actions, cross-system adapters and private operational dashboard.

**Acceptance scenario:** Simulated ledger outage keeps gossip notices flowing while reaction returns typed failure; operator redrive cannot execute stale/unauthorized command; handler crash does not silence other incident streams.

**Dependencies:** Out-of-band emergency recovery route, operator funding and SLOs. Do not position unproven overlay as sole safety-critical incident path or millisecond industrial control.

**Candidate platform links:** [`MPE-PRD-001`](candidate-ears.md#mpe-prd-001), [`MPE-PRD-002`](candidate-ears.md#mpe-prd-002), [`MPE-PRD-003`](candidate-ears.md#mpe-prd-003), [`MPE-PRD-004`](candidate-ears.md#mpe-prd-004), [`MPE-PRD-005`](candidate-ears.md#mpe-prd-005), [`MPE-PRD-009`](candidate-ears.md#mpe-prd-009), [`MPE-PRD-010`](candidate-ears.md#mpe-prd-010), [`MPE-PRD-016`](candidate-ears.md#mpe-prd-016).

## Portfolio decision gate

For each use case, record customer/owner, current process and cost, privacy adversary, measurable success criterion, required integrations, pilot cost, and disposition (adopt/defer/reject). Only then set numeric service targets and delivery commitments. The RFQ pilot needs completed signed-consumption and replay/binding verification before settlement; a coordination-only demo can precede that gate. Broad mobile wallet delivery needs an approved private retrieval profile. Private carried contract events depend on the underlying Midnight capability; ordinary signed application messages do not.

Large documents and attachments remain encrypted references. Fetches require explicit authorization because retrieval can disclose recognition. Event commitments establish neither external physical facts nor validity of a commercial claim. Application adapters enforce business policy.
