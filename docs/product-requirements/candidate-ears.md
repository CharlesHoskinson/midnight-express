# Candidate product EARS requirements

Status: **for consideration**, reviewed against the three independent design studies. These are product/API extensions, not amendments to the protocol baseline or declarations of implemented behavior. `SHOULD` is a proposed priority; no requirement is approved by this file.

Existing authority: [consolidated register](../design-document/build/ears-consolidated.json) and [Appendix A](../design-document/build/appendix-a.md). Existing obligations are referenced rather than renumbered. IDs use the separate `PRD` area. All records wait on DEC-PRD-1 (product scope/semantics approval).

## Requirements

<a id="mpe-prd-001"></a>
### MPE-PRD-001 Listener cancellation
When an application cancels a subscription handle, the MPE client library shall stop scheduling callbacks for that handle.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); DOM/Node listeners; Reactive Streams; existing MPE-CON-055.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Cancel during pending dispatch, drain in-flight work under documented semantics, and assert no newly scheduled callback; repeated registration/cancellation returns resource counts to baseline.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-002"></a>
### MPE-PRD-002 Handler failure isolation
If an application handler fails, then the MPE client library shall isolate that failure from other subscriptions and infrastructure tasks.
- Pattern: unwanted
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Node events; Reactive Streams; existing MPE-CON-056.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Throw and reject promises in one handler; another subscriber continues; error does not become false processing success.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-003"></a>
### MPE-PRD-003 Bounded application demand
While an application subscription has zero outstanding demand, the MPE client library shall schedule no new Message callback for that subscription.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); NATS; Reactive Streams; existing MPE-PRF-034; MPE-PRV-003.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Slow-handler stress honors declared demand and bounded local queues; packet traces remain recognition-independent; saturation returns an explicit error or disk-spool state.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-004"></a>
### MPE-PRD-004 Encrypted failure quarantine
When an authenticated Message exhausts its configured handler retries, the MPE client library shall persist its failure record in the application's encrypted quarantine.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); EventBridge; RabbitMQ; existing MPE-CON-056; MPE-PUB-049.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Always-failing handler produces one recoverable record with identity, reason and deadline; storage-full is explicit; relay logs reveal no failure-specific business selector.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-005"></a>
### MPE-PRD-005 Retry expiry gate
If a quarantined Message has expired, then the MPE client library shall refuse an application request to execute it.
- Pattern: unwanted
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); EventBridge; existing MPE-CON-046.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Manual replay after expiry cannot authorize an effect; diagnostic inspection may remain available under configured retention. Retry counts and deadlines must be configured before execution.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-006"></a>
### MPE-PRD-006 Confidential standard event mapping
Where CloudEvents interoperability is enabled, the MPE client library shall encode event identity and semantic attributes inside the authenticated Sealed Body.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); CloudEvents; NEP-297; existing MPE-PRV-003; MPE-PUB-049; MPE-FMT-033.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Round-trip identity, source, type, version and registered schema; capture outer packets and verify no semantic attributes appear in routing/header metadata. Unknown authenticated schemas remain undecodable.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-007"></a>
### MPE-PRD-007 Versioned asynchronous API contract
The MPE client library shall publish a versioned AsyncAPI contract for its product messaging API.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); AsyncAPI; existing MPE-CON-055.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Generated examples interoperate with reference API; breaking changes are detected by compatibility checks; examples contain no real stream secrets or customer topology.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-008"></a>
### MPE-PRD-008 Receipt provenance
Where application processing receipts are enabled, the MPE client library shall verify the receipt issuer against the workflow's authorized processor set.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); RabbitMQ; Waku; Cosmos; existing MPE-CON-015; MPE-STO-039.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Forged, expired, wrong-workflow and replayed receipts cannot advance business status; relay acceptance, retained storage, inclusion/finality and processing remain separate dimensions. Receipts are explicitly authorized encrypted application messages. Strongest privacy mode emits no automatic recognition-triggered receipt; responding requires explicit application action with declared disclosure.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-009"></a>
### MPE-PRD-009 External effect idempotency
Where a workflow adapter invokes an external side-effect API, the MPE client library shall pass the workflow's stable idempotency key to that adapter.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Kafka; RabbitMQ; existing MPE-CON-033.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Crash after remote success but before checkpoint; recover without duplicate effect if destination honors key. Unsupported destinations expose uncertain completion and prohibit an exactly-once guarantee.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-010"></a>
### MPE-PRD-010 Connector trust descriptor
Where a source-chain connector is enabled, the MPE client library shall expose its origin-verification and finality policy in the connector descriptor.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Avalanche; Cosmos; Solana; Ethereum; existing MPE-FMT-054; MPE-CON-062; MPE-CON-063.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Wrong chain, wrong transaction/event position and forged origin are rejected under selected policy; gateway-attested mode is distinguishable from independently verified mode. No universal finality mapping.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-011"></a>
### MPE-PRD-011 Private-mode connector queries
While whole-Shard privacy mode is selected, the MPE client library shall issue no source-confirmation query selected by a recognized Message.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Aztec; Waku; source-chain adapters; existing MPE-PRV-013; MPE-PUB-030.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Swap recognized interests while holding scheduled workload constant; source and relay traces contain no recognition-dependent selectors. Confirmation uses approved independent batching or explicitly selected weaker mode.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-012"></a>
### MPE-PRD-012 Group epoch revocation
When an authorized group membership removal commits, the MPE client library shall activate a fresh group-key epoch excluding the removed member before accepting subsequent group publications.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Sui; XMTP; existing MPE-CRY-018; MPE-CRY-019; MPE-CRY-029.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Removal activates a fresh epoch before subsequent publications are accepted; concurrent sends follow that documented boundary; removed member cannot decrypt any message accepted after it. Previously readable history is not erased.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-013"></a>
### MPE-PRD-013 Consent-scoped notifications
If a sender lacks a recipient's application notification permission, then the MPE client library shall suppress that sender's user-visible notification.
- Pattern: unwanted
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Push; XMTP; Dialect; existing MPE-CRY-018; MPE-PRV-015.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Denied/revoked sender cannot trigger display; receipt and push behavior audited for new interest leakage. Consent does not alone establish instruction authority.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-014"></a>
### MPE-PRD-014 Private mobile capability gate
If a requested private mobile profile cannot satisfy its declared leakage policy, then the MPE client library shall refuse to enable that profile.
- Pattern: unwanted
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Waku; Aztec; Push; existing MPE-PRV-013; MPE-PRF-021.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Unavailable private retrieval cannot silently fall back to topic filtering. Measure bytes, energy, loss and recovery on named phone/network profiles; budget and supported threat model require product approval.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-015"></a>
### MPE-PRD-015 Actionable notification binding
Where an application displays an executable Message action, the MPE client library shall derive its effect inputs exclusively from the authenticated signed workflow payload.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Dialect; Sui; existing MPE-CON-043; MPE-CON-044a; MPE-CON-044b; MPE-CON-060.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Change amount, recipient, target chain, action or expiry in UI/connector and confirm rejection; duplicate confirmation cannot duplicate business effect.
- Status: open (DEC-PRD-1)

<a id="mpe-prd-016"></a>
### MPE-PRD-016 Recovery security profile
Where encrypted history recovery is enabled, the MPE client library shall document the recovery profile's key-retention consequences for forward secrecy.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: [three-agent extraction](../../reviews/competitive-event-systems/extraction.md); Sui/Walrus; XMTP; NATS; existing MPE-CRY-029; MPE-STO-025; MPE-PRV-040.
- Rationale: Product extension proposed from the comparison; preserve the existing protocol privacy and delivery boundaries.
- Verify: test/inspection: Restore within permitted retention and key scope; missing keys/history return explicit gaps. Test revoked-device and backup compromise assumptions; archives cannot silently restore deliberately erased ratchet secrets.
- Status: open (DEC-PRD-1)

## Decision DEC-PRD-1

Options: adopt individual candidates into product scope, defer with a named dependency, or reject with rationale. Each requires a product owner, engineering estimate, approved leakage profile and demonstrated acceptance gate. Avoid treating a source system's guarantees as inherited guarantees. Pilot priorities: lifecycle/recovery, confidential schemas, signed actionable workflows and bounded failure handling. Mobile private retrieval, ratcheted groups and source-chain verification require separate implementation experiments.

## Parameters and dependencies

Application demand, queue/spool capacity, maximum attempts, retry age and quarantine retention are configuration inputs; no production defaults are invented here. Group membership, cryptographic suites and private mobile budgets remain design decisions. External effects require destination idempotency or reconciliation; a local transaction cannot make an arbitrary remote service atomic.

## Verification status

No implementation acceptance test has run for these candidates. Documentation lint checks syntax only. Three studies establish research coverage, not engineering implementation or security sign-off.
