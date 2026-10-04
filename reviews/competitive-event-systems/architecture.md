# Midnight Express — independent architecture and delivery review (reviewer 1 of 3)
Reviewed 2026-10-03 America/Denver. Status: design research and candidate requirements, not implementation or production assurance.

Evidence reviewed: original design-document-extracted.txt, all relevant competitive-research primary-source snapshots and manifests; current official traditional-system documentation verified with web tools and downloaded with Scrapling into review-architecture-sources/. No runtime benchmarks performed. Existing document already has retention, receipt, repair and flow rules: proposals below should extend their product contract, not duplicate or silently override existing numbered requirements.

Baseline constraints
The proposed overlay distributes fixed-size ciphertext through one GossipSub v1.2 shard, retaining envelopes for 48h. Local salted-tag recognition provides conditional interest privacy only when client network behavior does not depend on recognition. Traffic timing, publishers' ingress connections and coarse shard membership remain exposed. Registry Anchors establish commitments, not complete delivery, authority or valid business actions. The exploratory consumer circuit does not yet bind authenticated instructions, effects, consumption nullifiers and anchored envelopes. Signed-instruction and envelope binding are already normative obligations (MPE-CON-043, MPE-CON-044a/b and MPE-CON-060 in the current authoritative build/appendix-a.md); their design/implementation remains open. This review proposes acceptance evidence and product adaptations, not their reintroduction as missing requirements. Global total order and exactly-once network delivery are not established. These limits govern all adaptations below.

Each item states mechanism, desired adaptation, incompatibility, and a proposed acceptance gate. Requirement identifiers ARC-Rxx are research identifiers for mapping to the repository's authoritative numbering.

## 1. Sui Stack Messaging — ecosystem toolkit, not Sui consensus messaging
Sources: https://github.com/MystenLabs/sui-stack-messaging ; https://github.com/MystenLabs/sui-stack-messaging/blob/main/docs/sui-stack-messaging/Security.md
Mechanism: client-side AES-GCM, threshold-key Seal policies, on-chain group membership/key history, off-chain ciphertext relayer, sender signatures, optional Walrus archives.
Adopt/adapt: separate policy, delivery and encrypted archival interfaces; one SDK exposes group membership and atomic remove-and-rotate operations.
Limit: relayer sees sender/group/timing; threshold server collusion is a separate trust assumption; no per-message forward-secrecy ratchet. Do not expose Midnight stream IDs as group routing metadata.
ARC-R01: versioned group epochs and atomic removal/rekey. Gate: removed member cannot decrypt any new-epoch message; concurrent sends use an explicitly accepted epoch; already readable history remains outside revocation promise.

## 2. Solana native events
Source: https://solana.com/docs/rpc/websocket/logssubscribe
Mechanism: live RPC log subscription with address filters and commitment selection.
Adopt/adapt: explicit observed/confirmed/finalized event states and typed adapters.
Limit: public filters disclose interests to RPC provider; notification does not prove a transaction succeeded at the required finality.
ARC-R02: every carried event identifies exact source transaction, event position and finality state. Gate: an event from a failed or rolled-back transaction never activates a finalized-action handler.

## 3. Dialect — application notification/action service
Sources: https://www.dialect.to/ ; https://docs.dialect.to/
Mechanism: wallet/application alerts with embedded Blinks actions and integration tooling. Legacy SDK metadata documents encrypted messaging, but current homepage emphasizes Alerts/Blinks, so current encrypted-thread deployment is not assumed.
Adopt/adapt: actionable notification payloads and turnkey business workflow components.
Limit: notification channels and subscriptions are not evidence of interest hiding; a displayed action must not authorize itself.
ARC-R03: typed notification-to-action binding requiring explicit consent/signature and expiry. Gate: changing amount, destination, network or expiry causes action rejection; duplicate UI clicks do not create duplicate effects.

## 4. Hyperliquid WebSockets
Source: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions
Mechanism: user-specific and market feeds; some initial deliveries marked isSnapshot, followed by live updates.
Adopt/adapt: distinguish snapshots from deltas; reconcile on reconnect before applying new risk decisions.
Limit: user address subscription is visible to server; live WebSocket receipt is not durable or final proof.
ARC-R04: adapter snapshots carry a watermark and updates are reconciled/deduplicated across reconnect. Gate: disconnect during fill delivery yields the same final application state as uninterrupted processing, with gaps surfaced rather than silently guessed away.

## 5. NEAR NEP-297
Source: https://github.com/near/NEPs/blob/master/neps/nep-0297.md
Mechanism: standardized EVENT_JSON logs with standard/version/event/data fields.
Adopt/adapt: standard/version/event schema for decrypted carried events.
Limit: public JSON labels belong inside Midnight ciphertext; serialization standards do not confer origin authentication.
ARC-R05: schema registry and explicit version compatibility. Gate: known versions decode consistently; unsupported major version is quarantined without causing an action or exposing its private type in relay metadata.

## 6. NEAR Lake
Source: https://github.com/near/near-lake
Mechanism: chain data exported as block/shard JSON to S3 for decoupled indexing and replay.
Adopt/adapt: deterministic checkpoints, reproducible source adapters and encrypted batch archives.
Limit: immutable public archive is unsuitable for secret messages; expired storage is not cryptographic erasure from prior readers. Indexer is not the source of chain authority.
ARC-R06: checkpoints bind source chain, height/hash and schema. Gate: restart from checkpoint reproduces event identity; substituted archive data is rejected against authoritative chain data; expired/unavailable history returns an explicit gap.

## 7. Ethereum native Geth subscriptions
Source: https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub
Mechanism: connection-bound live subscriptions; logs may be repeated and marked removed on reorganizations; historical recovery requires a separate query path.
Adopt/adapt: event retraction and disconnect recovery as first-class SDK states.
Limit: log filters disclose interests; new subscription alone cannot recover missing history.
ARC-R07: provisional event handlers receive retraction/finality transitions with persistent cursor recovery. Gate: disconnect-plus-reorg cannot leave a provisional event mislabeled finalized or produce duplicate finalized business effects.

## 8. XMTP — independent messaging protocol
Sources: https://docs.xmtp.org/protocol/overview ; https://docs.xmtp.org/protocol/security ; https://docs.xmtp.org/protocol/topics
Mechanism: MLS encrypted group epochs, wallet-authorized identities/installations, routed group topics, replay/cursor delivery; documented forward secrecy and compromise recovery.
Adopt/adapt: separate installation keys from wallet authority, recoverable identity management, standard ratcheted group cryptography.
Limit: group routing and per-IP queries remain observable; recovery assumes fresh honest key updates and key erasure. Adoption of MLS would require a wire/security compatibility decision, not a casual cipher swap.
ARC-R08: scoped installation lifecycle and ratchet security profile. Gate: revoked installation cannot decrypt subsequent epoch traffic; state rollback/replayed commits are rejected; compromise experiment tests past-key erasure and recovery after fresh updates.

## 9. Waku — independent GossipSub messaging network
Sources: https://docs.waku.org/learn/concepts/protocols ; https://docs.waku.org/learn/concepts/content-topics
Mechanism: Relay, RLN spam proofs, Store, Filter and LightPush separate transport responsibilities.
Adopt/adapt: modular relay/store/light-client roles and explicit receipt semantics; this is already architectural ancestry in the design.
Limit: content topics and Filter/Store queries reveal interest metadata. LightPush acceptance is not full-network delivery; Store does not guarantee availability.
ARC-R09: capability-negotiated clients declare privacy mode and delivery meaning. Gate: no private mode emits per-stream selectors; tests distinguish relay acceptance, store commitment, recipient recognition and processing rather than conflating them.

## 10. Push — wallet communication service
Source: https://comms.push.org/
Mechanism: subscribed channels, notifications, encrypted chat, groups and application SDKs.
Adopt/adapt: consent, channel lifecycle and application integration widgets.
Limit: channel subscription and external push endpoints can identify recipients; generic wakeups need careful coalescing/padding.
ARC-R10: per-application consent and revocable notification permissions. Gate: denied sender cannot cause a user-visible notification; revocation stops later display; push-provider payload reveals no sender, stream, event label or plaintext.

## 11. Lightning onion messages — Bitcoin ecosystem routed communication
Source: https://github.com/lightning/bolts/blob/master/04-onion-routing.md
Mechanism: onion-encrypted routed messages and route blinding, explicitly unreliable; intermediaries need not store or report errors.
Adopt/adapt: optional blinded introduction/reply paths with clear threat model.
Limit: routing anonymity is not delivery reliability; onion routes do not defeat global timing analysis.
ARC-R11: optional publisher ingress/reply privacy profile with bounded retries and explicit unsupported-state behavior. Gate: ingress cannot read final endpoint routing information provided by profile; packet capture verifies no ordinary stream label; deliberate route failure produces timeout, never a false delivery receipt.

## 12. Cardano CIP-83
Source: https://github.com/cardano-foundation/CIPs/blob/master/CIP-0083/README.md
Mechanism: passphrase encryption of transaction metadata; published default passphrase is public.
Adopt/adapt: versioned encrypted envelope interoperability and explicit key-source rules.
Limit: CBC/passphrase defaults should not replace modern authenticated encryption; encrypted metadata remains on-chain with transaction context.
ARC-R12: SDK production APIs prohibit public/default secrets and identify cryptographic suite versions. Gate: default/test key material is rejected in production profile; modified ciphertext fails authentication; unknown suite fails closed.

## 13. TON encrypted comments and internal-message conventions
Sources: https://docs-next.ton.org/contracts/standard/wallets/interact ; https://github.com/ton-blockchain/ton/blob/master/doc/smc-guidelines.txt
Evidence note: encrypted-comment documentation was verified in the official web search index; that host failed direct DNS retrieval. Internal op/query_id/bounce conventions were verified in the downloaded smc-guidelines snapshot.
Mechanism: encrypted transfer comments, operation identifiers, query_id correlation and bounced internal messages.
Adopt/adapt: encrypted correlation IDs, explicit request/response operations and failure responses.
Limit: on-chain endpoints remain visible; blockchain contract internal messages execute under a different economic/finality model. Never expose a stable conversation identifier in outer routing.
ARC-R13: private request/response correlation with deadlines. Gate: out-of-order replies map to their intended request, duplicate replies do not complete twice, expired replies are rejected, and packet capture exposes no correlation ID.

## 14. Avalanche ICM
Source: https://build.avax.network/docs/cross-chain/avalanche-warp-messaging/overview
Mechanism: source validator aggregate BLS signatures authenticate cross-L1 messages.
Adopt/adapt: explicit source-network identity, domain separation and validator-set/finality verification for connectors.
Limit: validator signature attests within its trust model; encryption and subscriber privacy are not inherent; cross-chain receipt is not universal finality.
ARC-R14: connector declares verifiable origin/trust model. Gate: wrong network, stale/inapplicable validator set, altered payload or insufficient signature weight is rejected; trusted-gateway mode is visibly distinguished from verified mode.

## 15. Cosmos IBC
Sources: https://docs.cosmos.network/ibc/latest/intro ; https://github.com/cosmos/ibc/blob/main/spec/core/ics-004-channel-and-packet-semantics/README.md
Mechanism: light-client proof verification, packets, acknowledgements and timeouts; versions differ in channels, ordering and timeout details.
Adopt/adapt: explicit packet identity, success/failure acknowledgement and timeout state machine.
Limit: remote-chain proof assumptions remain; no confidential transport guarantee. Do not import IBC v1 channel ordering as a universal guarantee of newer versions.
ARC-R15: typed connector state machine forbids contradictory terminal outcomes. Gate: timeout races, duplicate receives and forged acknowledgements cannot produce both settled and timed-out status for one workflow; origin proof and accepted version are recorded.

## 16. Aztec note discovery
Source: https://docs.aztec.network/developers/docs/foundational-topics/advanced/storage/note_discovery
Mechanism: handshake-derived shared secrets, indexed secret tags, bounded scan windows and finalized-index tracking.
Adopt/adapt: explicit recognition state recovery, scan-window bounds and migration handling.
Limit: official docs acknowledge that tag queries expose IP-to-transaction interest; efficient tag lookup alone is not Midnight's whole-shard privacy.
ARC-R16: gap recovery is documented for tag/key epochs and client loss of state. Gate: out-of-window events produce detectable recovery need; tests restore a client from backup without skipping authorized messages or sending per-stream recognition tags to a private-mode server.

## 17. Zcash memos
Source: https://zips.z.cash/zip-0302
Mechanism: typed encrypted shielded-transaction memos with reserved values and safe textual decoding.
Adopt/adapt: reserved content type ranges, explicit empty/unknown states and safe rendering.
Limit: memos travel with transactions, not a general off-chain bus. New memo-bundle proposals are not assumed activated.
ARC-R17: decrypted content is parsed defensively and never implicitly rendered as executable HTML/action. Gate: malformed UTF-8, reserved types and arbitrary binary data produce safe display or opaque content; unknown future types remain recoverable without execution.

## 18. Secret Network
Source: https://docs.scrt.network/secret-network-documentation/development/development-concepts/secret-contract-fundamentals/privacy-essentials
Mechanism: confidential smart-contract execution under trusted-enclave assumptions; viewing/access controls and explicit privacy-design guidance.
Adopt/adapt: application threat-model worksheet covering response size, timing, event shape and query patterns.
Limit: confidential computation does not automatically conceal sender, timing or access pattern; enclave trust differs from Midnight proofs.
ARC-R18: each workflow supplies a privacy leakage budget and observable-metadata review. Gate: packet/chain trace review measures declared leaks; secret-dependent message sizes or response timing are rejected or explicitly approved as a weaker profile.

Traditional industry: design adaptations

## 19. Apache Kafka
Source: https://kafka.apache.org/43/design/design/
Mechanism: retained partition logs, offsets, consumer groups, idempotent production and transactional consumption/output within defined Kafka boundaries.
Adopt/adapt: replay cursors, transactional application outbox/inbox and monotonic encrypted stream sequence numbers.
Limit: broker topics/groups/offsets reveal subscriptions; partition order is not global order; external side effects require cooperation from destination systems.
ARC-R19: persistent consumer checkpoint is atomically paired with local business effect/outbox. Gate: crash injected before/after commit yields no skipped message and no duplicate local effect; external side effects use stable idempotency keys. No unconditional exactly-once delivery claim.

## 20. NATS JetStream
Source: https://docs.nats.io/learn/jetstream/pull-consumers
Mechanism: durable consumers, pull batches, explicit acknowledgement, redelivery, bounded pending messages and deduplication mechanisms.
Adopt/adapt: bounded demand-driven SDK consumption, durable local progress and documented dedup horizon.
Limit: server-side subjects, acknowledgements and consumer state identify interests. Application queue demand must not selectively alter private-mode network fetches.
ARC-R20: async iterators expose demand/cancellation with fixed memory bounds while reception/storage operates independently of recognized payloads. Gate: slow-handler stress cannot grow memory without bound, suppress network cover traffic based on matching, or silently drop messages; duplicate-after-horizon behavior is specified.

## 21. RabbitMQ
Source: https://www.rabbitmq.com/docs/confirms
Mechanism: publisher confirms and consumer acknowledgements are separate; prefetch limits outstanding deliveries and redelivery can follow failure.
Adopt/adapt: separate acceptance/storage/processing receipts, finite outstanding work and idempotent handlers.
Limit: queue names/routing keys and acknowledgements expose relationship metadata; publisher confirmation does not prove consumer business completion.
ARC-R21: SDK returns typed receipt levels with attester and expiry. Gate: store-accepted envelope cannot be reported processed; processor crash causes recoverable replay; forgery or replay of receipt cannot advance status.

## 22. AWS EventBridge
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html
Mechanism: managed rules and target delivery with bounded retries/jitter, dead-letter handling and optional archive/replay elsewhere in its service model.
Adopt/adapt: per-workflow retries, encrypted local dead-letter quarantine and controlled replay.
Limit: centrally evaluated routing rules require visibility into labels/body; retry copies and timestamps leak patterns. Dead-letter storage needs access control and retention.
ARC-R22: explicit maximum age/attempts, encrypted quarantine and replay authorization. Gate: always-failing handler eventually quarantines once with reason and original identity; manual replay does not bypass expiry/signature/idempotency checks; private routing labels remain encrypted.

## 23. CloudEvents
Source: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
Mechanism: standard event identity, source, type and specversion with optional subject, time, schema and content-type metadata, independent of transport.
Adopt/adapt: logical interoperability envelope within encrypted application payload; stable event IDs identify retries.
Limit: standard HTTP/binary-mode headers expose type/source/subject; copying these into MPE outer metadata defeats sealed labels.
ARC-R23: confidential CloudEvents mapping keeps identity and semantic metadata inside authenticated ciphertext. Gate: semantically identical events round-trip between supported adapters; outer packet metadata exposes only declared transport fields; identity collisions across sources are not merged.

## 24. AsyncAPI
Source: https://www.asyncapi.com/docs/reference/specification/v3.0.0
Mechanism: machine-readable asynchronous operations, messages, schemas, security declarations and protocol bindings, distinct from runtime delivery guarantees.
Adopt/adapt: executable API contracts with examples and generated client integration tests.
Limit: public API documents must use generic templates, not customer secrets, private stream IDs or unapproved relationship topology; specification is not enforcement.
ARC-R24: product APIs have versioned AsyncAPI contracts plus runtime schema checks. Gate: generated client/server examples pass interoperability tests; breaking contract changes fail compatibility review; sample docs contain no real keys or private topic IDs.

## 25. Reactive Streams
Source: https://www.reactive-streams.org/
Mechanism: asynchronous stream subscription, positive demand, bounded delivery, cancellation and terminal signals with nonblocking backpressure.
Adopt/adapt: consistent application-level demand/error/complete/cancel semantics and bounded buffering.
Limit: transport-wide selective pause would reveal recognition or damage GossipSub mesh; demand concerns decrypted local processing, not private network interest.
ARC-R25: SDK stream contract specifies bounded buffering, terminal behavior and cooperative cancellation. Gate: no application item is delivered beyond declared demand; cancellation frees listener and key references; slow subscriber cannot block other handlers or produce unbounded queue growth.

## 26. DOM EventTarget and Node EventEmitter
Sources: https://dom.spec.whatwg.org/#interface-eventtarget ; https://nodejs.org/api/events.html
Mechanism: local listener registration/removal, one-shot listeners and abortable EventTarget subscriptions; Node EventEmitter listeners execute synchronously in registration order and error handling has explicit semantics.
Adopt/adapt: familiar on/once/unsubscribe or AbortSignal APIs over verified events, with async-iterator alternative.
Limit: these are in-process dispatch, not durable networking. Synchronous callbacks can block dispatch; listener exceptions and forgotten listeners create failure/leak risks.
ARC-R26: lifecycle-safe SDK subscriptions with distinct provisional/finalized message events and isolated async handler errors. Gate: repeated mount/unmount and cancellation restore baseline listener/resource counts; once fires once despite replay; a throwing/slow listener does not disable unrelated subscribers; finalized actions cannot be registered on provisional events without explicit policy.

Synthesis: what to extract
Highest-return common layer: encrypted versioned event schema; first-class lifecycle/finality states; persistent replay cursors; signed authority separate from proof of inclusion; idempotent workflow effects; bounded local backpressure; explicit receipt levels; group epoch management; consent; confidential connectors. Preserve recognizer-independent transport behavior as a separate invariant tested alongside functional behavior.

Avoid importing visible broker topics, server-side content filters, public consumer-group offsets, conventional per-message acknowledgements or raw push notification content into the default privacy profile. Offer weaker convenience profiles only through explicit choices with precise leakage documentation.

Candidate pilot acceptance matrix
Run offline recovery within retained history; missed-history expiry; duplicate and reorder delivery; crash before/after effect commit; malformed and unsupported payloads; wrong origin and forged signature; unauthorized group epoch; reorg/retraction; slow-handler memory pressure; selective-recognition traffic traces. Passing these does not establish 99%/p99 latency or global adversary privacy: those require measured deployment experiments and separate threat-model tests.
