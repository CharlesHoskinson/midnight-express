# Local subscription contracts for the wallet, DApp and agent demo

Status: proposed local control-plane design, not an implemented MPE wire extension. Model v0.2 accepts only its three installed closed profiles. A subscription never grants shard membership, source authenticity, execution authority or a new event vocabulary. The original whole-shard encrypted wire remains intact; filtering happens locally after authorized decryption, with the original wire retained separately from derived views. Cleartext business selectors must not appear in relay routes, public topics or transport acknowledgements.

## Exact demo SubscriptionIntent record

All objects below are closed: every listed member is required and unknown members refuse. JSON integers use the model's portable nonnegative lexical integer discipline; clocks use its strict UTC seconds grammar. IDs are local opaque handles, never remote URLs. Arrays have at most 16 entries. This is a control-plane schema specification, not a model profile.

```json
{
  "kind": "LocalSubscriptionIntent",
  "version": 1,
  "subscriptionId": "subscription:quotes",
  "revision": 1,
  "owner": "principal:demo",
  "shardHandle": "shard:demo-private",
  "selector": {
    "category": "quotes",
    "profile": "rfq.v0.2",
    "contract": "sha256:8b5c6b89f6019fcb06b479e92f1b3bea340ac500cc218341e368e1ed2093071c",
    "sourceEquals": ["urn:mpe:source:dealer"],
    "predicate": "all"
  },
  "start": {"mode": "after", "cursor": "cursor:demo/000000"},
  "expiresAt": "2026-10-04T13:00:00.000Z",
  "sink": {"handle": "sink:local-inbox", "maxInFlight": 8, "maxQueuedEvents": 64, "maxQueuedBytes": 262144},
  "requestedState": "active"
}
```

Exact enums: `category` is quotes/payments/approvals/contracts/credentials/ops; `profile` is rfq.v0.2/invoice.v0.2/agent.v0.2/mock.local.v1. `predicate` is all/payment-final/approval-report; profile and predicate compatibility is checked before installation. `sourceEquals` empty means all sources already authenticated and authorized by local business validation policy; anonymous transport admission alone authenticates no business source. `contract` must equal an installed exact profile commitment; mock.local.v1 uses literal `mock-only`, and can never enter model dispatch. `start.mode` is after/earliest/latest: after requires a journal-issued cursor, earliest/latest require empty cursor. `requestedState` is active/paused/unsubscribed. Positive revision and positive sink limits have demo maxima 9007199254740991, 64, 1024 and 4194304 respectively. Handle strings match `^[a-z][a-z0-9-]*:[a-z0-9][a-z0-9._/-]*$` and are 1–80 characters; cursor handles are opaque and journal-bound. `sourceEquals` entries use the model source grammar. Display title is at most 120 characters and summary at most 512 characters; no HTML interpretation. `receivedAt` is trusted local intake time, separate from sender time. `revision` is at least 1; mock category/profile combinations are contracts/credentials/ops only, and accepted categories map quotes→rfq.v0.2, payments→invoice.v0.2, approvals→agent.v0.2. Subscription IDs and revisions cannot be reused for different content. Sink handles resolve only through a local allowlist; arbitrary network endpoints and executable selectors refuse.

A selector is convenience for the authorized recipient. The wallet uses quote expiry and observed payment status to inform a person; the DApp selects exact business profiles for its private inbox; the agent receives only report approval candidates. No selector hides messages from an already authorized whole-shard reader. Local `category` labels are derived metadata and not signed sender claims.

## Separate runtime and incoming records

The closed runtime record has fields `subscriptionId`, `revision`, `state`, `deliveredCursor`, `processedCursor`, `oldestRetainedCursor`, `gap`, `inFlight`, `queuedEvents`, `queuedBytes`. State is active/paused/gapped/expired/revoked/unsubscribed. Gap is null or the closed object `{requestedCursor,oldestRetainedCursor,reason}`, with reason retention/missing-range/conflict. Cursors are local journal positions, not EIDs or business event timestamps. Counters are nonnegative bounded integers. This mutable runtime state is separate from intent revision history.

The closed demo IncomingRecord has fields `recordId`, `category`, `mode`, `wireRef`, `eventRef`, `contextRef`, `receivedAt`, `validation`, `display`. Mode is `unsigned-mock` or `v0.2-fixture`. References resolve through a local manifest only; there is no sender-controlled file read or fetch. For unsigned mocks, wireRef/eventRef/contextRef are null and validation is `not-model-validated`. For v0.2 fixtures, eventRef and contextRef are required, wireRef is null unless original sealed bytes actually exist, and validation begins `pending`. Never fabricate an original signed wire for a model JSON example. `display` is a closed `{title,summary}` object of bounded plain strings; it cannot carry an execution instruction. Derived data and source bytes are separate stores, with no claim that local display text authenticates a sender.

Accepted local validation result is a separate closed record `{recordId,status,businessDigest,executes}`, directly obtained from the validator; every success retains `executes:false`. Failed attempts create a quarantine record `{recordId,reason,attemptedAt,originalRef}` instead. Validation status is not editable UI state.

## Lifecycle and delivery semantics

Creation checks the local owner's permission to configure this shard and sink, exact contract installation and valid cursor scope. Latest begins after a captured atomic journal high-water mark; earliest begins at the oldest retained entry and visibly states historical coverage. After is strictly exclusive. A cursor older than retention enters gapped; it never silently jumps to latest. An operator can explicitly create a new revision accepting the recorded gap, or recover from an authorized archive.

Pause stops new deliveries and keeps the cursor; retained intake may continue within separate bounded storage. Resume rechecks subscription expiry, shard permission and retention. Unsubscribe stops scheduling and records a tombstone; it does not erase action deduplication history or imply erasure of replicas. Expiration stops new delivery at the exclusive boundary. Permission revocation stops decryption/delivery and effect preparation immediately upon trusted local notification; queued callbacks must recheck current permission. Already disclosed data cannot be clawed back. An in-progress committed effect remains an outcome to reconcile.

Backpressure uses bounded pull credits (`maxInFlight`) and both event/byte queue caps. At capacity, stop scheduling and expose a backlog; never silently drop or evict undecided work. If upstream retention overtakes the cursor, emit a gap. Retry uses original occurrence identity and action idempotency key, with bounded attempts and quarantine. A poison item can advance a contiguous local delivery checkpoint only after its explicit quarantine disposition is durably recorded. Processing checkpoints advance through contiguous decided dispositions, including explicit quarantines; they never represent successful execution for every item.

Replay creates a new local delivery attempt over retained originals, revalidates against the exact installed historical contract and current permission, and keeps the existing action ledger. Historical display can show expired/revoked evidence with a clear historical label; it cannot produce a fresh actionable approval. New event IDs or outer EIDs do not renew consumed actions.

Occurrence identity is `(source,id)`: changed content under the same pair is conflict. For approvals, stable action identity is `(authorityDomain,executionScope,actionId)`; changed proposal/target/contract conflicts rather than becoming new authority. Quote/payment records have their existing profile identities and evidence rules; do not invent executable action keys for them.

A delivery receipt means original input and disposition are durably journaled locally. A processing receipt means the local handler reached a stated outcome, such as displayed/quarantined/sandbox-committed/outcome-unknown. Neither receipt proves consensus finality or global exactly-once delivery. Keep processing receipts private locally; external acknowledgements, if later designed, must avoid revealing selected profile, match/no-match, human decision or timing. Padding/batching is an unimplemented mitigation, not a demonstrated privacy guarantee.

## Useful finite scenarios and limits

| Category | Useful demonstration | Real v0.2 scope / UI limitation |
|---|---|---|
| Quotes | Wallet alerts to an unexpired exact Shares/USD quote; paused inbox resumes | `model/examples/rfq.json`; open matching RFQ and dealer authority from supplied context; off-chain only |
| Payments | DApp inbox distinguishes Pending, Final, Reversed and duplicate replay | invoice example files plus matching complete paymentEvidence; Final is a source assertion, no payment execution |
| Approvals | Agent queues a WriteReport candidate; revoke before preparation; repeat occurrence cannot repeat action | agent example, sandbox scope/policy/proposal/human/budget checks; candidate never grants arbitrary tools |
| Contracts | UI shows renewal reminder and retention gap | unsigned mock only; no runtime contract-lifecycle profile |
| Credentials | Wallet shows credential-expiry reminder | unsigned mock only; no credential issuance/verification/revocation semantics |
| Ops | Operator sees backlog, quarantine and subscription expiry | local control-plane state or unsigned mock only; no newly supported MPE event |

Pin fixture clock to `2026-10-04T12:00:00.000Z` using `model/conformance/trusted-context.json`. Quotes and approvals expire at 13:00 on October 4; machine time on October 5 cannot make them currently valid. Payment scenarios require their exact corresponding evidence context, not merely a source label. A source URI, unsigned digest, JSON schema pass or UI category never establishes authority. Production source admission, sealing/signatures, current permission service and real evidence remain deployment gates.

## Comparison and design decision

[CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) supplies envelope context and source+id occurrence deduplication; it does not supply action permission, durable consumers or private subscription routing. Keep its event vocabulary inside the private business body as v0.2 already does.

[AsyncAPI 3.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) can document channels/messages/operations and bindings; use it for an eventual local adapter API, without interpreting public channel names as safe private business topics. [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core) provides structural schemas; separately implement cursor ownership, installed commitments, expiry, authority, action conflicts and byte limits. Reject network `$ref` resolution in received data.

[Reactive Streams 1.0.4](https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.4/README.md) motivates explicit demand and cancellation. Demand bounds local dispatch; it is not durable replay, network admission or storage retention. [NATS pull consumers](https://docs.nats.io/learn/jetstream/pull-consumers) illustrate explicit pulls, bounded batches and acknowledgements driving a durable consumer cursor. Adopt those concepts locally, without importing cleartext subjects or claiming NATS acknowledgement semantics implement MPE privacy or global exactly-once effects.

Primary sources were fetched with Scrapling; raw bytes, text extractions and SHA-256 metadata are under `sources/sol-contracts/`. The NATS consumers URL redirected to its current pull-consumer guide; citations follow the resolved page. PixelRAG 0.4.0 CDP captured eight CloudEvents page tiles. Tiles 2 and 3 were visually inspected: the v1.0.2 branch, context-attribute discussion and source+id duplicate rules are visible. Raw/visual hashes are recorded in `sources/sol-contracts/cloud-events-visual.json`. Other standards comparisons use archived textual evidence; their individual visual grounding is not claimed.

Actual offline validation is recorded in `data-model-fit.json`: 19 finite cases, 11 accepted, all accepted with `executes:false`, plus five dashboard receipts for exact event/context pairs. The fixed clock, RFC8785 event/context hashes and unsigned synthetic evidence remain explicit. The current conformance script also passed 80 checks and three schema self-checks. Browser presentation of these receipts is an offline precheck, never a browser authority service.

## Reconciled privacy constraints

Consumer credits and pause govern local delivery only. Whole-shard intake, shard discovery and repair scheduling must remain independent of recognition results; consumer saturation must not produce match-dependent network timing. Recognition keys arrive by explicit invitation, not through wallet-derived secrets or remote agent handles. Whole-shard readers may still observe the entire authorized shard.

Private selectors, watch history, cursor positions and per-record processing decisions are sensitive local state. An export or remote callback is a separate disclosure decision. The demonstration export contains mock state only. [The proposed closed schema](../../design/subscriptions/README.md) defines structural configuration boundaries; runtime grants, revision CAS, durability and evidence remain separate acceptance work.
