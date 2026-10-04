# MIDNIGHT EXPRESS — INDEPENDENT REVIEW 2 OF 3
Privacy, security, authorization and trust review
Reviewed 3 October 2026, America/Denver. Research verified against primary-source documentation and public repositories, including fresh Scrapling retrievals. This is a design study, not a protocol audit or deployment benchmark.

BASELINE AND INTERPRETATION
Read the PDF extraction, existing competitive assessment and source snapshots, and current consolidated appendix docs/design-document/build/appendix-a.md in the cloned repository. Preserve the distinction between already-designed obligations, incomplete implementation, open decisions, and proposed product extensions. In particular, MPE-CRY-020/021/022 already specify publisher authentication, signed context and authorized delivery; MPE-CRY-028/029/030 contemplate ratcheting and erasure. These are completion/decision priorities, not newly discovered absent requirements.

The present compiled consumer demonstrates inclusion, not complete instruction authorization. The PDF introduction/prose says version 1 does not specify a signed-statement-to-anchored-envelope binding, but the authoritative consolidated baseline MPE-CON-060 explicitly requires anchoredEID/commitSealedBody to bind the opened signed statement to the anchored envelope (PROD, MUST, open DEC-022). Treat this as an EXISTING normative target with an unresolved design decision and incomplete implementation, and reconcile the prose/baseline discrepancy. Borrowed features should complete that obligation rather than add a duplicate missing requirement. An Anchor must never be equated with authority, availability, business acceptance or semantic correctness.

Interest privacy is conditional: full-shard local recognition must not change subscriptions, repair, queries, retries, telemetry, receipts or automatic actions. MPE-CON-039 prohibits automatic network action triggered by recognition. MPE-PUB-016 requires explicit reduced-privacy opt-in. Do not add a default read receipt, broker-visible private stream filter, recipient-specific push token content or selective dead-letter upload while claiming unchanged interest privacy. Timing, shard membership and connection metadata remain visible; the design makes no global-observer guarantee.

EACH DESIGN STUDIED
Each entry includes mechanism, useful extraction, mismatch, proposed requirement and acceptance experiment. Requirements below are candidate product additions or strengthened evidence obligations, not an automatic amendment of the normative protocol.

## 1. SUI STACK MESSAGING
Mechanism: client AES-GCM with Seal threshold-managed keys, Sui group policies, signed canonical ciphertext and group/key-version/sender AAD, off-chain relayer and optional Walrus recovery. Borrow atomic remove-and-rotate, independently verified sender status, explicit permission/key-history policy, transport/storage adapters.
Mismatch: relayer observes sender/group/timing; threshold collusion affects content trust; no per-message ratchet. Default new readers can obtain historical keys; removal alone does not rotate. On-chain group state exposes membership-related information.
Candidate: group removal and rotation must be one safe operation; history access is separately authorized; authentication failure is never delivered as business instruction. Explicitly document key-server assumptions if adopting external key release.
Acceptance: removed reader with old state cannot open post-rotation messages; newly admitted reader without history grant cannot obtain earlier keys; swap sender/group/version and verify rejection.
Sources: https://github.com/MystenLabs/sui-stack-messaging ; https://github.com/MystenLabs/sui-stack-messaging/blob/main/docs/sui-stack-messaging/Security.md

## 2. SOLANA EVENTS
Mechanism: logsSubscribe returns transaction signature, slot, error/logs and processed/confirmed/finalized commitment; mentions filter selects one address. Borrow explicit lifecycle and transaction outcome labels.
Mismatch: public payload and address filter disclose subscriber interests. A transport notification cannot independently establish finalized authorized execution.
Candidate: adapter output includes chain, transaction identity, log position, commitment and verification source inside the encrypted payload; privileged actions require finalized successful execution.
Acceptance: failed transaction, provisional observation and mismatched position cannot authorize settlement; duplicate delivery does not duplicate action.
Source: https://solana.com/docs/rpc/websocket/logssubscribe

## 3. DIALECT
Mechanism: actionable alerts/Blinks embed wallet actions in existing experiences. Borrow user-facing event-to-action templates and confirmation context. Current product material supports alerts/actions; historical SDK encryption is not treated as verified current production architecture.
Mismatch: an alert can be phishing, stale or redirected. Embedded transaction convenience is not authority or concealed recipient interests.
Candidate: encrypted action payload declares verified issuer, target network/contract, complete effect, expiry and required consent; display the verified transaction effects before wallet signing.
Acceptance: substituted destination, expired alert and untrusted signer are rejected; listener receipt never silently signs or sends a transaction.
Sources: https://www.dialect.to/ ; https://docs.dialect.to/

## 4. HYPERLIQUID WEBSOCKETS
Mechanism: typed userFills/userEvents/orderUpdates subscriptions and initial snapshot marker. Borrow a clear snapshot-versus-update boundary and reconciliation of trading state.
Mismatch: watched address is supplied to service; feed state is provider-origin data rather than an end-to-end signed business instruction.
Candidate: listeners distinguish snapshot, incremental observation and reconciled authoritative state; risk alert payloads carry stable identifiers and freshness conditions.
Acceptance: reconnect snapshot cannot trigger repeated liquidation/payment instruction; malformed or out-of-order updates enter reconciliation rather than authorizing an irreversible action.
Source: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions

## 5. NEAR EVENTS / LAKE
Mechanism: NEP-297 versioned JSON event convention; Lake exports block/shard data to object storage. Borrow standard schemas and restartable chain-indexing adapters.
Mismatch: indexing public data provides no confidential event transport; cloud data provenance must be distinguished from independent chain validation.
Candidate: every adapter specifies schema version, supported chain finality, recovery source and validation trust; adapter credentials never become message decryption keys.
Acceptance: unknown schema version, forged object-store row and missing block interval produce an explicit error/gap; adapter cannot label unverified data as verified-final.
Sources: https://github.com/near/NEPs/blob/master/neps/nep-0297.md ; https://github.com/near/near-lake

## 6. ETHEREUM / GETH LOG LISTENERS
Mechanism: subscriptions expose new logs, including removed logs during reorganizations; connection subscriptions are not historical delivery. Borrow removed/provisional lifecycle and historical reconciliation.
Mismatch: filters and logs are public; new block notification is not finality. Reorgs can re-emit a transaction/event.
Candidate: external Ethereum adapter preserves chain/transaction/log identity and removal status, and permits provisional UI separately from finalized privileged reaction.
Acceptance: fork replacement retracts provisional state; reconnect plus historical recovery produces one logical event; revoked fork event never enters the final authorized reaction path.
Source: https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub

## 7. XMTP
Mechanism: MLS encrypted groups, authenticated messages, erased ratchet state, fresh commits for recovery, encrypted welcomes, topic routing. Borrow installation identity, authenticated invitation, consent and tested cryptographic state transitions.
Mismatch: operators can analyze per-IP topic queries; welcome recipients remain observable. Recovery requires uncompromised fresh key material and correct erasure, not merely relabeling a session.
Candidate: complete explicit security capability records and erased-state inventory; recovery is authenticated and describes retained skipped-key exposure. Never rebuild erasable message keys deterministically from the wallet recovery seed.
Acceptance: after verified erasure a current-state compromise cannot open earlier non-retained messages; authorized fresh update prevents old-state decryption; invalid packet never advances durable ratchet state.
Sources: https://docs.xmtp.org/protocol/security ; https://docs.xmtp.org/protocol/topics

## 8. WAKU
Mechanism: GossipSub relay, RLN admission/rate control, Store, Filter and LightPush. Borrow component separation, costed spam controls, offline retrieval and clearly scoped acknowledgements.
Mismatch: Filter/Store/LightPush expose content topics and can link IP to interest; Store is not guaranteed availability; LightPush acceptance is not network-wide receipt. Topic hashing/bucketing reduces disclosure but does not make selection invisible.
Candidate: production anonymous admission and private mobile retrieval need explicit adversary/cost profiles; no selector-based optimization is silently enabled.
Acceptance: replayed rate proof cannot exceed quota; capture complete egress under matching/nonmatching recognition keys and compare; offline recovery exposes gaps without a matching-message selective repair request.
Sources: https://docs.waku.org/learn/concepts/protocols ; https://docs.waku.org/learn/concepts/content-topics

## 9. PUSH COMMUNICATIONS
Mechanism: opt-in notification channels, encrypted chat, groups and SDK/application delivery integration. Borrow consent-first onboarding, channel controls and action templates.
Mismatch: channel subscription relationships and notification timing can reveal interests; marketing confidentiality is not proof of concealed subscriptions.
Candidate: authenticated invitations, per-application consent/revocation, and generic push wakeups with no private stream identity. Separate notification delivery provider visibility from message encryption.
Acceptance: revoked consent prevents app-level delivery; push payload contains no sender/topic/action data; strongest profile maintains wakeup schedule independent of message recognition.
Source: https://comms.push.org/

## 10. BITCOIN / LIGHTNING ONION MESSAGES
Mechanism: layered onion routing, route blinding and end-to-end encrypted off-chain communication. Borrow blinded reply routes and separation of payload confidentiality from routing visibility.
Mismatch: specification explicitly allows unreliable delivery without required intermediary persistence. Blinding does not establish durable receipt or hide all traffic correlation.
Candidate: any onion/proxy option publishes failure, routing, latency and correlation assumptions; availability remains a separate replicated retention service.
Acceptance: an unavailable path cannot return a storage/delivery success; a blinded route does not expose destination in intermediary packet fields; retries obey bounded nonrecognition-dependent policy.
Source: https://github.com/lightning/bolts/blob/master/04-onion-routing.md

## 11. CARDANO CIP-83
Mechanism: convention for encrypted transaction message metadata, using password-derived encryption. Borrow ecosystem-wide versioned envelope interoperability and backward-compatible parsing.
Mismatch: ciphertext and transfer context are public; known default passphrase cardano provides no secret. Password encryption is not authenticated publisher authority.
Candidate: imported metadata is labelled as external unverified content until chain and issuer verification; cryptographic APIs forbid public default secrets.
Acceptance: public-default encrypted input never gains confidential status; wrong credentials/tampering do not produce executable instructions; unknown metadata is handled as opaque rather than trusted event.
Source: https://github.com/cardano-foundation/CIPs/blob/master/CIP-0083/README.md

## 12. TON ENCRYPTED COMMENTS
Mechanism: transfer body opcode 0x2167da4b, sender/recipient key agreement and encrypted memo; wallet networks have domain-specific replay protection. Borrow payment-associated encrypted context and strict payload type discrimination.
Mismatch: memo rides an on-chain transfer and preserves visible transaction context; static recipient-key handling is not ratcheted content forward secrecy. Do not transplant bespoke CBC construction in place of MPE authenticated encryption.
Candidate: payment receipt schema binds network, exact transaction, recipient, amount/asset, invoice identity and finality under verified issuer signature.
Acceptance: replay on a different network, substituted payment or malformed comment opcode cannot satisfy an invoice; memo alone does not prove payment settlement.
Source: https://github.com/ton-blockchain/docs/blob/main/content/contracts/standard/wallets/interact.mdx

## 13. AVALANCHE ICM
Mechanism: source L1 validator BLS signatures are aggregated for cross-chain verification. Borrow verifiable source attestation and clearly identified validator/trust set.
Mismatch: verified origin does not make payload secret or action permitted; validity depends on the specified validator set and destination policy.
Candidate: external message evidence must bind source network/domain, destination, payload, replay identity and the supported validator-set snapshot; expose trust model to the application.
Acceptance: signature under wrong source set, destination or payload is rejected; a valid source message from an unauthorized business issuer cannot trigger a privileged MPE action.
Source: https://build.avax.network/docs/cross-chain/avalanche-warp-messaging/overview

## 14. COSMOS IBC
Mechanism: packet commitments, client verification, acknowledgement and timeout/nonreceipt proofs. Borrow explicit packet lifecycle and timeout/error semantics for cross-system workflows.
Mismatch: ordinary packet contents/context are observable; client security assumptions vary. Transport acknowledgement is not counterparty business acceptance.
Candidate: cross-chain adapters specify verification client, packet identity, timeout and destination; expose observed, verified, expired and rejected separately.
Acceptance: duplicate packet cannot execute twice; timeout followed by late delivery follows one documented outcome; bad client state cannot label packet verified.
Source: https://docs.cosmos.network/ibc/latest/intro

## 15. AZTEC PRIVATE NOTE DISCOVERY
Mechanism: encrypted logs discovered through shared-secret-derived tags/counters rather than trial-decrypting everything. Borrow costed, asynchronous private recipient discovery and counter resynchronization.
Mismatch: querying a tag reveals that retrieval selector to the serving node (an inference from the documented API), even though the tag does not publicly reveal recipient identity. Efficient discovery and MPE recognition invariance are different guarantees.
Candidate: prototype oblivious/PIR retrieval against tagged discovery as a cost benchmark; classify non-oblivious tag lookup as an explicit privacy profile rather than preserving strongest guarantees.
Acceptance: server-visible transcript and indexer confirmations are measured; counter gaps are recovered without revealing individual matches under strongest profile; compare bytes/day and latency for identical workload.
Source: https://docs.aztec.network/developers/docs/foundational-topics/advanced/storage/note_discovery

## 16. ZCASH MEMOS
Mechanism: standardized encrypted memo formats in shielded transactions. Borrow typed private payment-associated metadata and strict version/empty-value interpretation.
Mismatch: transaction-associated memo is not a relay network. ZIP-302 does not itself establish application-level sender authority; readable memo does not authorize a payment.
Candidate: confidential receipt schema separates payment evidence, issuer identity and user text; codecs enforce bounds and reject ambiguous executable fields.
Acceptance: memo tampering/unknown formats never execute a workflow; a receipt references the exact verified transfer; only intended decryption authority receives receipt content.
Source: https://zips.z.cash/zip-0302

## 17. SECRET NETWORK
Mechanism: encrypted contract state/inputs/queries and permissioned viewing, with explicit contextual leakage documentation. Borrow narrow viewing grants and honest leakage inventories.
Mismatch: TEE/hardware trust differs from client end-to-end encryption/zero-knowledge proof assumptions; timing, query patterns, shapes and storage accesses can remain exposed.
Candidate: selective disclosure is message/time/field scoped, auditable locally and independent of master stream secret; any enclave-assisted option is separately named and specified.
Acceptance: auditor key cannot decrypt unrelated messages; disclosure test enumerates revealed fields; revocation blocks new grants but does not claim to erase already learned plaintext.
Source: https://docs.scrt.network/secret-network-documentation/development/development-concepts/secret-contract-fundamentals/privacy-essentials

## 18. APACHE KAFKA
Mechanism: partition logs/offsets, consumer groups, idempotent producers and transactional offset/output writes. Borrow durable local inbox/outbox and partition-scoped sequence rather than global-order assumptions.
Mismatch: brokers see topics, clients and offsets; TLS/ACLs do not provide end-to-end payload secrecy against the broker. Kafka transaction guarantees do not make arbitrary external side effects exactly once.
Candidate: private inbox and application effect must have an atomic/idempotent boundary; recovery checkpoints remain local encrypted state. Broker adapters are explicitly trusted enterprise edges.
Acceptance: crash before/after effect and checkpoint yields one effect with repeated delivery; broker snapshot contains no private MPE payload or stream selector; cross-partition ordering is not falsely assumed.
Sources: https://kafka.apache.org/41/design/design/ ; https://github.com/apache/kafka/blob/trunk/docs/security/security-model.md

## 19. NATS JETSTREAM
Mechanism: durable consumers, acknowledgements/redelivery, bounded pending delivery, message-ID deduplication; TLS and store encryption. Borrow bounded retry/flow control and stable authenticated logical IDs.
Mismatch: server consumer/subject state exposes interest; encryption at rest is not secrecy from server. A finite deduplication window cannot establish indefinite business-effect replay prevention.
Candidate: persist authenticated logical replay state for application lifetime independently of transport seen-set lifetime; pull scheduling is shard/bucket based and independent of recognition.
Acceptance: replay after transport cache/dedup-window expiry cannot repeat a payment; bounded buffers under slow handler; no network cursor or subject changes when different keys recognize the same shard.
Sources: https://docs.nats.io/learn/jetstream/pull-consumers ; https://github.com/nats-io/nats.docs/blob/master/using-nats/jetstream/model_deep_dive.md ; https://docs.nats.io/learn/security/encryption

## 20. RABBITMQ
Mechanism: publisher confirms, separate consumer acknowledgements, manual ack/requeue and prefetch bounds. Borrow precise ownership/status semantics and bounded handler concurrency.
Mismatch: confirm covers broker custody, not recipient processing; consumer ack identifies consumed deliveries. Brokers observe queues and consumers.
Candidate: SDK status vocabulary separates ingress acceptance, storage receipt, anchor finality, local delivery and optional business response; strongest profile exports no recognition-triggered ack. Business response is an explicit application interaction with its own disclosure.
Acceptance: ingress acceptance is never displayed as recipient receipt; a lost confirm can cause retransmission without double effect; matching versus nonmatching consumers have identical default egress.
Source: https://www.rabbitmq.com/docs/confirms

## 21. AWS EVENTBRIDGE
Mechanism: rule-based routing, retry policies with bounded age/attempts, target dead-letter queues and encrypted-at-rest event buses. Borrow bounded failure handling, failure classification and replay tooling.
Mismatch: provider evaluates routing against event attributes and can process event contents; customer-managed encryption-at-rest is not MPE end-to-end secrecy. Dead-letter metadata may reveal target/error/relationship information.
Candidate: private dead-letter handling stays local/encrypted; operator metrics contain shard-level operational data only, with aggregation/privacy budgeting as appropriate. Expiry is enforced on replay.
Acceptance: malformed recognized message creates no remote selective diagnostic upload; expired event replays as rejected; logs and DLQ contain no plaintext action, recipient or private stream identifiers.
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html

## 22. CLOUDEVENTS
Mechanism: standard event context; source+id identify a distinct event and retransmissions may preserve that identity. Borrow versioned interoperability and deduplication convention.
Mismatch: ordinary source/type/subject headers reveal business identity. Producer-supplied identity is not cryptographic authority and unsigned headers can be rewritten.
Candidate: CloudEvents mapping is inside authenticated ciphertext; event identity and workflow correlation are signature-bound. Public envelope exposes only existing allowed MPE fields.
Acceptance: packet capture reveals no event source/type/subject; swapping any effect-relevant context fails validation; equal authenticated source+id from retransmission produces one logical item.
Source: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md

## 23. ASYNCAPI
Mechanism: machine-readable channels, operations, messages, correlation IDs, schemas and security schemes. Borrow generated SDKs, contract testing and discoverable protocol capabilities.
Mismatch: a schema/security declaration is not enforcement; public channel names may expose private subjects. Authentication requirement does not prove data confidentiality or delivery guarantees.
Candidate: document separate transport and decrypted application schemas; publish verifiable guarantees and required profiles per operation; generated private listeners only accept authenticated, canonical, supported messages.
Acceptance: generated compatibility tests reject unknown major schema and invalid required fields; no public channel is derived from secret/private stream; declared guarantee matches runtime evidence.
Source: https://www.asyncapi.com/docs/reference/specification/v3.0.0

## 24. REACTIVE STREAMS
Mechanism: asynchronous nonblocking backpressure with bounded demand. Borrow demand-aware local handler execution, cancellation and bounded memory.
Mismatch: if network fetch demand changes according to recognized messages, backpressure becomes an interest side channel. A slow handler is not allowed to stall the whole shard silently.
Candidate: separate shard acquisition from local decrypted-event processing; bounded private processing queues surface explicit local lag/gap; network acquisition cadence does not depend on recognized handler load in strongest profile.
Acceptance: vary matching-message ratio and handler speed while keeping shard workload fixed; egress selector/cadence remains unchanged within the declared model, buffers stay bounded and any missed retention is explicit.
Source: https://www.reactive-streams.org/

## 25. DOM EVENTTARGET
Mechanism: listener registration/removal, once, AbortSignal and explicit dispatch semantics. Borrow familiar lifecycle and deterministic cleanup for browser SDK.
Mismatch: DOM listeners run within one trust/runtime boundary; dispatch does not authenticate a remote sender. Event.isTrusted relates to user-agent dispatch, not issuer authorization.
Candidate: verify/decrypt before emitting application events; async durable processing is separate from UI dispatch; AbortSignal unsubscribes local handlers without leaking private selector changes.
Acceptance: forged CustomEvent cannot enter verified business reaction API; aborted callback never fires; cleanup leaves no private state/listener retention or stream-specific network notification.
Source: https://dom.spec.whatwg.org/#interface-eventtarget

## 26. NODE EVENTEMITTER
Mechanism: synchronous callbacks in registration order; explicit error event behavior; once/removal and async-iterator APIs. Borrow familiar developer interface with explicit exceptions and listener cleanup.
Mismatch: emit is not delivery durability or authorization; listener exception/reentrancy can affect other handlers. Synchronous heavy callbacks can block acquisition and generate traffic timing leakage.
Candidate: verified message dispatch is isolated from intake; bounded async processing with typed local error outcomes; cancellation and listener limits are documented and tested.
Acceptance: one throwing/reentrant listener cannot suppress intake or invoke duplicate effect; unhandled rejection becomes typed error; slow handler does not alter recognition-dependent network behavior or grow memory without bound.
Source: https://nodejs.org/api/events.html

PRIORITY SECURITY EXTRACTIONS FOR PRODUCT CONSIDERATION
A. Complete canonical authenticated effect binding and replay-safe contract reaction, including message-to-anchor binding when claimed; map to MPE-CRY-020/021/022/025 and MPE-CON-060, DEC-022 and implementation evidence. This is completion of existing normative requirements, not a newly absent binding requirement.
B. Preserve strongest interest-privacy invariants across filtering, mobile wakeups, telemetry, retries, blobs, dead letters, acknowledgement and chain-confirmation queries; map to MPE-CON-039 and MPE-PUB-016. Measure leaks and publish opt-in profile boundaries.
C. Finish group epoch rotation and explicitly scoped history/auditor grants; couple revoke with rekey and distinguish revoked permission from erasing already delivered plaintext.
D. Complete ratchet/profile decisions and failure-atomic erasure; report retained-key/backfill tradeoff instead of promising both unrestricted restore and full forward secrecy.
E. Distinguish event observation, authenticated publisher assertion, storage custody, anchor commitment, finalized chain execution, user consent and business acceptance throughout APIs and product language.
F. Use outbox/inbox, authenticated IDs and crash recovery for at-least-once delivery with idempotent effects; avoid network-wide exactly-once claims or treating transport seen-set as business replay protection.
G. Keep external adapters as explicit provenance/trust boundaries with chain/network identity, event position, finality, issuer authority and timeout semantics.

The strongest traditional-industry lesson is reliability engineering and API contracts. The strongest cryptographic lesson is that confidentiality, metadata protection, authority, freshness, durability and execution correctness are separate properties with separate evidence. Copy useful mechanisms only with that separation intact.
