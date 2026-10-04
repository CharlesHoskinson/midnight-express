# What to extract from competing and traditional event systems

Recommendations below are **inferences for product consideration**, based on three independent reviews per system. See [coverage.json](coverage.json), [architecture](architecture.md), [privacy](privacy.md), and [product](product.md). Evidence dates: 3 October 2026, America/Denver. No runtime benchmark, security audit or validated market demand is implied.

## Design baseline reconciliation

The repo at `dd40bbb35c10e7c7db8e2969a40112ab04c6c65c` is the reference baseline. [Appendix A](../../docs/design-document/build/appendix-a.md) and [consolidated requirements](../../docs/design-document/build/ears-consolidated.json) already require signed publisher authority (`MPE-CON-043`), atomic replay protection (`MPE-CON-044a/b`), effect/checkpoint atomicity (`MPE-CON-033`), and anchored Sealed Body/signed-statement binding (`MPE-CON-060`, open DEC-022). They are existing targets with unresolved implementation/design checks. Some PDF/prose passages describe binding as unspecified; reconciliation is required, not a claim that the normative requirement is absent. The compiled exploratory consumer has not demonstrated these production obligations.

The current requirement set also addresses ratchets, invitations, selective disclosure, storage receipts, cursors and onboarding. Study recommendations classify them as complete/validate, extend, or explore. This addition leaves adopted protocol requirements and the generated PDF unchanged; new product candidates have separate IDs and an explicit consideration gate.

## Extraction decisions

“Adopt” and “adapt” here recommend a candidate direction; they are not approvals to implement or replacements for the existing design decision register. PRD numbers refer to [candidate-ears.md](../../docs/product-requirements/candidate-ears.md).

| System and primary evidence | Disposition | Useful mechanism | Boundary to preserve | Candidate mapping |
|---|---|---|---|---|
| [sui](https://github.com/MystenLabs/sui-stack-messaging) | Adapt | Separate policy, transport and encrypted archives; atomic removal/rekey | Relayer observes sender/group/timing; history policy and threshold trust must be explicit | 012,016 |
| [solana](https://solana.com/docs/rpc/websocket/logssubscribe) | Adapt | Exact source event identity and finality-aware adapters | Public RPC filters reveal interest; event observed does not mean successful finalized effect | 010,011 |
| [dialect](https://www.dialect.to/) | Adapt | Actionable notification components and workflow templates | UI action needs signed intent, consent, expiry and replay protection; legacy encrypted SDK deployment unverified | 013,015 |
| [hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions) | Adapt | Snapshot/delta distinction and reconnect reconciliation | Address subscriptions reveal watchers; stale/gapped feed cannot authorize risk actions | 010; UC-04 |
| [near](https://github.com/near/NEPs/blob/master/neps/nep-0297.md) | Adapt | Versioned event schemas and reproducible block/shard checkpoints | Logs and Lake are public; store semantic labels inside encryption; origin verification is separate | 006,010 |
| [ethereum](https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub) | Adapt | Provisional/retracted/finalized lifecycle and historical catch-up | Connection-only subscriptions lose history; public filters are not private discovery | 010,011 |
| [xmtp](https://docs.xmtp.org/protocol/security) | Adapt after crypto decision | Scoped installation keys, MLS-style ratchet lifecycle, consent | Topic queries observable; compromise recovery needs fresh honest updates and erasure; archive composition matters | 012,013,016 |
| [waku](https://docs.waku.org/learn/concepts/protocols) | Adapt; acknowledge existing ancestry | Modular relay/store/light roles and real spam-proof admission | Filter/Store selectors leak interests; acceptance does not imply recipient delivery or persistence | 008,011,014 |
| [push](https://comms.push.org/) | Adapt | Per-app consent, notification lifecycle and embedded integration | External push endpoints and channels leak metadata; generic wakeups alone do not solve timing correlation | 013,014 |
| [lightning](https://github.com/lightning/bolts/blob/master/04-onion-routing.md) | Defer privacy-routing experiment | Blinded introductions/reply paths with explicit failure semantics | Onion messages are unreliable; not global traffic-analysis protection | Existing privacy profile decisions |
| [cardano](https://github.com/cardano-foundation/CIPs/blob/master/CIP-0083/README.md) | Borrow versioning; reject insecure defaults | Clear cryptographic profile and interoperable encrypted content conventions | Public default passphrase gives no secrecy; do not replace MPE AEAD with CBC convention | Existing MPE-CRY-001/018 |
| [ton](https://docs-next.ton.org/contracts/standard/wallets/interact) | Adapt | Sealed request/reply correlation, deadlines and explicit failed responses | On-chain transfer context stays public; native internal-message execution differs from off-chain bus | 006,015; UC-01 |
| [avalanche](https://build.avax.network/docs/cross-chain/avalanche-warp-messaging/overview) | Adapt for connector profiles | Domain-separated source-network and validator-set verification | Validator attestations inherit source trust; no inherent confidentiality or universal finality | 010 |
| [cosmos](https://docs.cosmos.network/ibc/latest/intro) | Adapt for connector profiles | Origin proofs, packet identity, acknowledgement/timeout state machines | Version-specific ordering/trust; packet success is not every downstream business effect | 008,010 |
| [aztec](https://docs.aztec.network/developers/docs/foundational-topics/advanced/storage/note_discovery) | Adapt recovery; research retrieval | Bounded tag/key windows and explicit recognition-state recovery | Query-by-tag can expose interest; do not inherit privacy claim from encrypted logs | 011,014 |
| [zcash](https://zips.z.cash/zip-0302) | Adapt parser conventions | Reserved content types, safe text rendering and unknown-version handling | Transaction memos are not a separate message bus; no activated memo-bundle assumption | 006; existing MPE-PUB-049 |
| [secret](https://docs.scrt.network/secret-network-documentation/development/development-concepts/secret-contract-fundamentals/privacy-essentials) | Adapt threat-model discipline | Per-workflow review of timing, sizes, query and event-shape leakage | TEE trust differs from Midnight proofs; encryption does not hide access patterns | 011; existing privacy register |
| [kafka](https://kafka.apache.org/43/design/design/) | Adapt semantics | Persistent checkpoints, local inbox/outbox and destination idempotency | Partition order is not global order; arbitrary remote effects need destination cooperation | 009; existing MPE-CON-033 |
| [nats](https://docs.nats.io/learn/jetstream/pull-consumers) | Adapt SDK contract | Durable progress, bounded demand and explicit redelivery horizon | Consumer subject, state and ack cannot be exposed in default private mode | 003,016 |
| [rabbitmq](https://www.rabbitmq.com/docs/confirms) | Adapt semantics | Separate publisher/storage/processing confirmations and bounded work | Confirm is not business completion; automatic per-message ack would reveal recognition | 004,008,009 |
| [eventbridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html) | Adapt application layer | Bounded retry age/attempts, encrypted quarantine and authorized redrive | Rules reveal semantic labels; retries and quarantine must preserve identity and expiry | 004,005 |
| [cloudevents](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) | Adapt inside encryption | Published structured event identity/source/type/version mapping | Binary-mode headers expose metadata; spec format provides no authorization or delivery assurance | 006 |
| [asyncapi](https://www.asyncapi.com/docs/reference/specification/v3.0.0) | Adopt API documentation approach | Versioned machine-readable operations, schemas, examples and compatibility checks | Description is not enforcement; customer topology and logical channels remain private | 007 |
| [reactive-streams](https://www.reactive-streams.org/) | Adapt SDK layer | Demand, cancellation, bounded buffers and terminal signals | Application backpressure must not selectively affect upstream private traffic | 001,003 |
| [node-events](https://nodejs.org/api/events.html) | Adapt SDK ergonomics | on/once/off plus explicit error handling and async work isolation | Synchronous local invocation is not durable delivery; once is not processOnce | 001,002 |
| [dom-events](https://dom.spec.whatwg.org/#interface-eventtarget) | Adapt SDK ergonomics | Disposable handles, AbortSignal and UI lifetime controls | Local listener lifetime is not crash recovery or once-only business execution | 001 |

## Three shared conclusions

1. **Standardize the private application contract.** Keep source, type, schema, correlation and business IDs inside authenticated encryption. Version codecs and map external event identity deterministically. Preserve fixed Envelope classes and reject unsupported sizes; a familiar enterprise schema is not permission to grow the wire format.
2. **Make handling recoverable and observable to the application.** Separate reception from local demand; persist checkpoints/effects; distinguish admission, storage, inclusion/finality, local processing and signed business acknowledgement. These are independent dimensions, not one monotonic delivery ladder. Quarantine failures locally under encryption. Explicitly report gaps, expiry, uncertain external completion and retractions.
3. **Treat privacy as an invariant across conveniences.** Strong-profile reception, source confirmation, telemetry and recovery must not vary with recognized interest. No automatic business acknowledgements or attachment fetches. Group removal requires rekeying; past access cannot be revoked. Ratcheted history recovery needs an explicit erasure tradeoff. External-source authenticity does not authorize a business effect.

## What not to copy into the default privacy profile

Public business topics or group routing, content-aware broker filters, exposed subscriber offsets, per-recognition acknowledgements, message-specific push content and uploaded plaintext dead-letter payloads. Less-private convenience modes require explicit selection and declared leakage. Do not claim global anonymity, global total order, guaranteed data availability from a commitment, or exactly-once arbitrary remote side effects.

## Proposed first delivery

A backend RFQ reference workflow plus listener SDK, local recovery, authenticated action handling and encrypted schema adapters. Measure integration time, duplicate/crash behavior, gaps, operator costs and observable privacy leakage. Customer interviews must validate commercial savings. Broader mobile adoption depends on private retrieval measurements; an ordinary filtered webhook gateway must not be sold as the strongest privacy profile.

## Unresolved decisions

- Final private mobile retrieval and bandwidth/energy budgets.
- Group/installation key management and backup/ratchet composition.
- Connector proof versus trusted-gateway modes and confirmation-query leakage.
- Local processing limits and recovery behavior under retained-history exhaustion.
- Paid operator model, service targets and customer willingness to pay.
- PDF/prose versus consolidated signed-consumption implementation reconciliation.

## Follow-up composition study

The user's proposed GossipSub + Signal combination has a [separate three-agent feasibility assessment](../../docs/product-requirements/gossipsub-signal-option.md). Recommendation: off-chain pairwise backend experiment using serialized Signal ciphertext inside the existing MPE application payload. Session security, recognition privacy, business authority and nested contract proof binding remain separately tested properties.
