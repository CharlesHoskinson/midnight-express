# MIDNIGHT EXPRESS — INDEPENDENT REVIEW 3: PRODUCT AND DEVELOPER EXPERIENCE
Reviewer: design_review_product. Research: 2026-10-03 America/Denver.
Status: Research recommendations and candidate requirements; no implementation commitment.
Scope: Every named crypto design and traditional event-system design independently assessed.
Evidence: Original extracted design plus authoritative repo docs/design-document/build/ears-consolidated.json; existing primary-source Scrapling snapshots and current primary-source web verification. Older r5 indices are not authoritative. Documentary study, not deployed-system benchmark.

MAIN FINDINGS
The commercially useful product is confidential coordination with explicit evidence and lifecycle semantics. Customer success requires an application SDK and complete workflow. Familiar listeners should be wrappers around durable, privacy-preserving reception, not an illusion that an off-chain event runs a contract automatically.

Preserve four boundaries: (1) accepted by ingress is not durably stored; (2) stored is not application processed; (3) anchored is not authorized; (4) finalized anchoring is not proof that a carried event succeeded. Keep operational status local, inside encryption or recognition-independent aggregates. Public event type, organization, correlation identifier and acknowledgement would undermine subscription privacy.

The consolidated requirements already cover typed schemas, local recognition, portable cursors, crash-safe processOnce, key revocation, optional ratchets, finality transitions, publisher authentication, atomic replay protection and anchored-message binding. Many previously suggested top-ten FEATURES are implementation/promotion priorities, not new requirements. Product use cases should map these existing requirements and add only workflow/adapter/lifecycle gaps.

Important prose consistency finding: PDF introduction says binding signed instruction to anchored envelope is unspecified. Consolidated MPE-CON-060 explicitly requires this binding when Anchor inclusion proves publication. Treat implementation validation and prose reconciliation as needed; do not duplicate MPE-CON-060 as a newly invented security requirement.

ALL-DESIGN STUDY: MECHANISM -> EXTRACT -> LIMIT -> REQUIREMENT -> ACCEPTANCE
Each record below is a distinct independently reviewed design. Statements following 'candidate' are proposals for consideration, not assertions about existing Midnight Express behavior.

## 01 SUI STACK MESSAGING
Sources: https://github.com/MystenLabs/sui-stack-messaging ; https://github.com/MystenLabs/sui-stack-messaging/blob/main/docs/sui-stack-messaging/Security.md
Mechanism: SDK seals messages, off-chain relayer routes/stores them, Sui groups govern key access via Seal; optional Walrus archive. Per-message sender signatures.
Adopt: One coherent SDK combining invitations, groups, streaming, key versions and encrypted attachment references; removal-and-rekey as one business operation.
Limit: Beta toolkit, not consensus-native general delivery. Relayer sees group, sender and timing. Seal threshold trust and old-key access must be documented; no default per-message ratchet. Do not import public group routes into private MPE metadata.
Existing: MPE-CRY-018/019, MPE-CON-006, MPE-CON-052, MPE-FMT-038, MPE-SEC-020.
Candidate: Organizational SDK shall expose a transactional remove-and-rekey workflow and scoped read/send roles, with explicit history-access policy.
Acceptance: Remove employee while concurrent sends occur; excluded employee cannot decrypt the next key generation, existing authorized devices recover consistently, and policy states whether new members can read history. No assumption that old plaintext can be revoked.

## 02 SOLANA NATIVE EVENTS
Source: https://solana.com/docs/rpc/websocket/logssubscribe
Mechanism: WebSocket subscription to logs with address filters and commitment level.
Adopt: Explicit subscribe/unsubscribe handle and commitment-aware state.
Limit: Public transaction data and server-visible selectors; subscription alone supplies no durable history.
Existing: MPE-CON-015, MPE-CON-016, MPE-CON-017, MPE-CON-027, MPE-CON-028, MPE-CON-058, MPE-CON-059, MPE-CON-062, MPE-CON-063.
Candidate: Solana adapter shall persist a chain-specific cursor and emit normalized provisional/finalized/rolled-back observations with origin evidence.
Acceptance: Disconnect during a transaction, reconnect and backfill; duplicate is processed once and an observation that loses commitment cannot authorize final action.

## 03 DIALECT
Sources: https://www.dialect.to/ ; https://docs.dialect.to/
Mechanism: Wallet/app alerts with embedded actions/Blinks. Historical SDK evidence is distinct from current product positioning.
Adopt: Actionable notifications: typed action, context, expiry and clear confirmation, rather than an opaque text alert.
Limit: External URLs and actions can be malicious; current material does not establish MPE-like interest privacy. Legacy encrypted messaging SDK is not evidence of present hosted availability.
Existing: MPE-SEC-032, MPE-FMT-027, MPE-FMT-038, MPE-CON-043, MPE-CON-046, MPE-CON-048.
Candidate: UI SDK shall render registered action types with origin and expiry and require explicit authorization for effects.
Acceptance: Alter target/action/expiry, point to unregistered scheme or inject executable content; reject or display inertly, with no automatic network fetch or effect.

## 04 HYPERLIQUID WEBSOCKETS
Source: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions
Mechanism: Typed fills/orders/risk feeds; subscription acknowledgement may include isSnapshot-marked initial state.
Adopt: Snapshot-versus-delta separation, heartbeat health, account risk templates.
Limit: Service sees subscribed account; application-specific financial feeds, not a confidential general bus. Low latency is not a hard real-time guarantee.
Existing: MPE-CON-020, MPE-CON-024, MPE-CON-025a, MPE-CON-025b, MPE-CON-028, MPE-CON-056.
Candidate: Financial adapter shall label snapshots and incremental updates distinctly and preserve an authoritative recovery watermark.
Acceptance: Reconnect after fills; rebuild position from snapshot plus subsequent updates without applying fills twice; stale/gapped view blocks automatic trading action.

## 05 NEAR NEP-297
Source: https://github.com/near/NEPs/blob/master/neps/nep-0297.md
Mechanism: EVENT_JSON structured event record identifies standard, version and event name.
Adopt: Versioned business event schemas and codec registration.
Limit: Chain logs are public; schema labels belong inside MPE sealing.
Existing: MPE-FMT-025, MPE-FMT-026, MPE-FMT-027, MPE-FMT-034, MPE-CON-010, MPE-CON-011.
Candidate: Connector registry shall map external standard/version/event combinations to fixed locally registered codecs.
Acceptance: Unknown version becomes typed undecodable data; no remote schema code executes; sensitive type/subject never appears in visible MPE bytes.

## 06 NEAR LAKE
Source: https://github.com/near/near-lake
Mechanism: Indexer streams blockchain data backed by S3 data infrastructure.
Adopt: Independently resumable backfill adapter and explicit historic-coverage capabilities.
Limit: Indexer infrastructure and S3 access have cost and trust; no encrypted delivery implied.
Existing: MPE-CON-027, MPE-CON-028, MPE-CON-030, MPE-CON-032, MPE-STO-027.
Candidate: External indexer adapter shall declare coverage, continuity and operating cost separately from chain-origin verification.
Acceptance: Start outside coverage; report gap rather than silently starting at latest; restart at saved checkpoint with no skipped retained record.

## 07 ETHEREUM LOG SUBSCRIPTIONS
Source: https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub
Mechanism: Public filtered log notifications, including removed logs on reorganization; connection-scoped subscriptions are not history replay.
Adopt: Explicit rollback, live-plus-history boundary, finality state.
Limit: Filter reveals interests; replay needs separate history retrieval. Node stream is not authority.
Existing: MPE-CON-016, MPE-CON-027, MPE-CON-028, MPE-CON-048, MPE-CON-062, MPE-CON-063; MPE-SEC-022.
Candidate: Ethereum connector shall reconcile live events with bounded historical retrieval and maintain block-hash-based provenance.
Acceptance: Reorg removes a previously observed log; emit rollback once, reconcile replacement, never present removed log as final.

## 08 XMTP
Sources: https://docs.xmtp.org/protocol/security ; https://docs.xmtp.org/protocol/topics ; https://docs.xmtp.org/protocol/overview
Mechanism: MLS encrypted conversations with authenticated identities, group updates and topic delivery.
Adopt: Multi-device identity abstraction, interoperable content codecs, consent, explicit cryptographic posture and recovery.
Limit: Operators can analyze per-IP queries; welcome recipients remain visible. Conversation routing differs from whole-shard private recognition; deployment decentralization has phases.
Existing: MPE-CRY-026, MPE-CRY-028, MPE-CRY-029, MPE-CRY-030, MPE-CRY-031, MPE-CRY-032, MPE-SEC-028, MPE-SEC-030, MPE-SEC-031, MPE-SEC-033.
Candidate: SDK profile selector shall expose privacy, forward-secrecy, recovery and multi-device tradeoffs without silently weakening profiles.
Acceptance: Compromise current session state and test defined earlier-message secrecy and post-update recovery; missing state update fails safely; rollback from backup cannot reuse nonce/session state.

## 09 WAKU
Sources: https://docs.waku.org/learn/concepts/protocols ; https://docs.waku.org/learn/concepts/content-topics
Mechanism: Modular GossipSub Relay, RLN anti-spam, Store recovery, Filter and Light Push.
Adopt: Separately testable transport/storage/admission modules and capability negotiation.
Limit: Filter discloses content topics; Store does not guarantee availability; Light Push acknowledgement establishes one peer receipt, not whole-network delivery.
Existing: MPE-CON-004, MPE-CON-005a, MPE-CON-005b, MPE-CON-026, MPE-CON-036, MPE-CON-038; MPE-STO-039; MPE-SEC-026; MPE-ECO-012, MPE-ECO-048.
Candidate: SDK shall report each provider's actual reception/privacy/durability capabilities and reject unsupported requested guarantees.
Acceptance: Light gateway advertises only ingress receipt; UI never calls it durable/final; selective provider cannot silently replace private profile when resource budget is exhausted.

## 10 PUSH
Source: https://comms.push.org/
Mechanism: Cross-chain wallet notifications and encrypted chat with integration tooling.
Adopt: Wallet integration adapters and channel delivery templates with consent controls.
Limit: Consumer push infrastructure can expose device/timing and subscription metadata; cross-chain support is not verified remote-chain trustlessness.
Existing: MPE-CON-039, MPE-CON-052, MPE-SEC-025, MPE-SEC-032, MPE-SEC-033.
Candidate: Mobile wakeups shall use a declared privacy profile and avoid sensitive subjects/actions in platform notification payloads.
Acceptance: Inspect APNs/FCM-equivalent payload and callback traffic; no stream identifier, business subject or recognized-message-specific fetch appears in private mode.

## 11 LIGHTNING ONION MESSAGES
Source: https://github.com/lightning/bolts/blob/master/04-onion-routing.md
Mechanism: End-to-end encrypted onion messages and blinded routes; explicitly unreliable without intermediary storage obligation.
Adopt: Route-blinded first contact and request/reply designs as optional research, with expiry and bounded retry.
Limit: Routing confidentiality is not durable delivery or protection from global timing observers.
Existing: MPE-CRY-018, MPE-CON-026, MPE-SEC-032, MPE-SEC-033.
Candidate: First-contact adapter shall authenticate invitations and document delivery and metadata properties independently.
Acceptance: Unreachable recipient produces bounded failure rather than endless retry or success; spoofed invitation cannot replace pinned key or authorize action.

## 12 CARDANO CIP-83
Source: https://github.com/cardano-foundation/CIPs/blob/master/CIP-0083/README.md
Mechanism: Encrypted metadata compatible with CIP-20 transaction comments.
Adopt: Graceful wallet compatibility and explicit distinction between encrypted comment and authorized instruction.
Limit: Metadata remains on-chain; default public 'cardano' passphrase provides no confidentiality. Encryption here does not imply sender authentication.
Existing: MPE-FMT-025, MPE-FMT-026, MPE-CRY-022, MPE-CON-048.
Candidate: Legacy memo adapter shall label confidentiality/authenticity separately and refuse publicly known default secrets for private MPE use.
Acceptance: Public-default memo is never presented as confidential; unknown format displayed inertly; parsed payment instruction never executes without independent authorization.

## 13 TON ENCRYPTED COMMENTS AND MESSAGE LIFECYCLE
Sources: https://docs-next.ton.org/contracts/standard/wallets/interact ; https://github.com/ton-blockchain/ton/blob/master/doc/smc-guidelines.txt
Mechanism: Encrypted transfer comments; internal request/reply messages use operation/query identifiers, bounced responses; external messages require replay controls.
Adopt: Distinct request/response/error types, sealed correlation IDs and signed expiry.
Limit: Transfer context is on-chain; TON native execution semantics do not transfer to an off-chain MPE listener. First URL had local DNS retrieval failure; authoritative TON source guidelines verified independently for lifecycle/replay; encrypted-comment detail derives shared prior web verification.
Existing: MPE-FMT-034, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-SEC-037, MPE-SEC-038.
Candidate: Workflow templates shall distinguish commands, observations, replies and failures and prohibit failure replies being executed as original commands.
Acceptance: Replay reply or bounced request, tamper correlation ID, deliver late response; no duplicate effect or false success state.

## 14 AVALANCHE ICM
Source: https://build.avax.network/docs/cross-chain/avalanche-warp-messaging/overview
Mechanism: Source-validator BLS aggregate signatures authenticate interchain messages.
Adopt: Explicit origin-authentication verification policy in connectors.
Limit: Source quorum trust is not confidentiality, subscriber hiding or MPE's native contract authority.
Existing: MPE-CON-048, MPE-SEC-037; external-chain verifier is new scope.
Candidate: External connector shall identify origin chain, verifier policy, validator-set epoch and trust assumptions before any effect.
Acceptance: Wrong-chain message, stale validator set or insufficient threshold cannot authorize target action even when content parses.

## 15 COSMOS IBC
Source: https://docs.cosmos.network/ibc/latest/intro
Mechanism: Versioned chain interoperability, packet receive/acknowledgement/timeout lifecycle, relayed proofs.
Adopt: Separate delivery, acknowledgement and timeout state machine with idempotent recovery.
Limit: Public interoperability metadata; IBC classic/v2 differ. Do not conflate HTTP callback success, transport receipt and business settlement.
Existing: MPE-CON-026, MPE-CON-033, MPE-CON-046; MPE-SEC-038.
Candidate: Cross-chain workflow template shall record a terminal result only from application-defined authenticated success/failure evidence; uncertain cases remain unresolved.
Acceptance: Race timeout with delayed acknowledgement; never produce both successful settlement and refund; unsupported IBC version fails explicitly.

## 16 AZTEC NOTE DISCOVERY
Source: https://docs.aztec.network/developers/docs/foundational-topics/advanced/storage/note_discovery
Mechanism: Secret-derived note tags locate encrypted private logs without full trial-decryption of chain history.
Adopt: Benchmark discovery bandwidth and deterministic lookahead/recovery behavior.
Limit: Tag querying to serving nodes is different from recognition-independent whole-shard retrieval; cannot inherit equal metadata privacy without analysis. Private-note scope is narrower than generic off-chain bus.
Existing: MPE-CON-001, MPE-CON-003, MPE-CON-007, MPE-CON-008, MPE-CON-004; MPE-PRF-020; MPE-SEC-026.
Candidate: Any private retrieval research profile shall state what queried tags, access timing and server collusion disclose before adoption.
Acceptance: Equal public workload with differing recipient interests yields declared indistinguishability result under specified server observer; query-based profile must not be advertised as default whole-shard privacy.

## 17 ZCASH MEMOS
Source: https://zips.z.cash/zip-0302
Mechanism: Standardized memos attached to shielded notes with defined binary/text semantics.
Adopt: Conservative decoding, byte-size limits, text-versus-opaque distinction.
Limit: Transaction-associated messaging, not free-standing durable event stream; malformed or binary content must not become executable text.
Existing: MPE-FMT-015, MPE-FMT-025, MPE-FMT-026, MPE-CON-010, MPE-CON-011, MPE-SEC-032.
Candidate: Wallet renderers shall treat unsupported/binary application content as inert and enforce schema-size limits.
Acceptance: Invalid UTF-8, control characters, oversize content and malicious URLs render safely or return typed rejection without effects.

## 18 SECRET NETWORK
Source: https://docs.scrt.network/secret-network-documentation/development/development-concepts/secret-contract-fundamentals/privacy-essentials
Mechanism: Confidential contracts using encrypted inputs/state and permissioned viewing; metadata remains visible and execution has distinct trust assumptions.
Adopt: Privacy checklists and role-scoped viewing permissions, explicit metadata exposure.
Limit: TEE-dependent confidential execution is not automatically equivalent to MPE's proofs or off-chain recipient-interest properties. Sender/timing/size/event shape may leak.
Existing: MPE-CRY-026, MPE-CON-052, MPE-SEC-025, MPE-SEC-032.
Candidate: Workflow privacy manifest shall identify protected fields, allowed observers and unavoidable public metadata for each adapter and deployment mode.
Acceptance: Capture API, event, logging and metrics outputs for test workflow; each sensitive field appears only at permitted boundary and claimed omissions are demonstrably absent.

## 19 APACHE KAFKA
Source: https://kafka.apache.org/41/design/design/
Mechanism: Partitioned durable logs, offsets, consumer recovery; idempotent producer and transactional stream processing within defined boundaries.
Adopt: Durable replay, application-supplied atomic cursor/effect storage, bounded per-stream ordering and explicit reprocessing.
Limit: Broker knows topics/clients and plain data unless extra encryption; broker transaction is not exactly-once arbitrary external payment or blockchain effect. Public business-topic partitions unsuitable for default MPE.
Existing: MPE-CON-012, MPE-CON-013, MPE-CON-014, MPE-CON-020, MPE-CON-022, MPE-CON-027, MPE-CON-028, MPE-CON-033, MPE-CON-035; MPE-STO-025.
Candidate: SDK integration guide shall document transactional outbox/inbox patterns for external effects and distinguish transport redelivery from committed effect semantics.
Acceptance: Crash immediately before/after app commit and cursor save; same logical request causes one committed ledger/database effect, and failed effect remains retryable. Nontransactional external sink requires its own idempotency key or explicit uncertainty.

## 20 NATS JETSTREAM
Source: https://docs.nats.io/learn/jetstream/pull-consumers
Mechanism: Durable streams, explicit acknowledgements, redelivery and pull-consumer flow control.
Adopt: Bounded client demand and concurrency; visibility of unprocessed backlog; durable checkpoints.
Limit: Per-message infrastructure acknowledgements reveal recipient interest; service subject filters disclose subscriptions. NATS 'exactly once' claims have context and dedup boundaries.
Existing: MPE-CON-033, MPE-CON-039, MPE-SEC-025; MPE-STO-023.
Candidate: SDK asynchronous iterator shall bound local queue and expose pause/resume without changing default full-shard retrieval based on recognition.
Acceptance: Slow handler never grows unbounded memory or drops silently; overloaded mode emits typed Degraded; external fetch pattern remains independent of recognized messages.

## 21 RABBITMQ
Source: https://www.rabbitmq.com/docs/confirms
Mechanism: Publisher confirms and consumer acknowledgements solve separate safety problems; prefetch constrains in-flight work.
Adopt: Separate ingress/persistence/app-processing status and explicit application retry policy.
Limit: Consumer ack does not prove publisher completion; publisher confirm does not prove recipient processing. Copying automatic acks violates MPE-CON-039 and MPE-FMT-036.
Existing: MPE-CON-026, MPE-CON-033, MPE-CON-039, MPE-STO-011, MPE-STO-012, MPE-STO-039, MPE-STO-042, MPE-FMT-036.
Candidate: Status API shall never conflate accepted, stored, final, processed locally, or business acknowledged; business receipts use explicit signed application workflow, not protocol receipt kind.
Acceptance: Fail store after ingress acceptance; publisher still sees accepted, not stored. Recipient failure after storage cannot report processed. Default receiving sends no ack.

## 22 AWS EVENTBRIDGE
Source: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html
Mechanism: Event routing to targets with bounded retry/backoff/jitter and optional dead-letter destinations.
Adopt: Encrypted failed-work queue, bounded retries and operator redrive tooling.
Limit: Public matching and managed service visibility expose event interests; EventBridge retry numbers are service-specific, not MPE SLOs. DLQ is sensitive storage and action destination.
Existing: MPE-CON-032, MPE-CON-033, MPE-CON-039, MPE-CON-056, MPE-FMT-038, MPE-SEC-032.
Candidate: Application workflow adapter shall maintain a local encrypted failure queue with expiry and explicit redrive authorization, separate from overlay retries.
Acceptance: Poison event cannot block unrelated healthy events; retry exhausts at configured bound, retained failure contains no plaintext business data, redrive preserves authenticated logical ID.

## 23 CLOUDEVENTS
Source: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
Mechanism: Vendor-neutral event context; source+id identify event, type/specversion support tooling. Pin published release, not main's 1.0.3 work-in-progress.
Adopt: Structured CloudEvent INSIDE sealed payload for adapters, consistent identity/version mapping.
Limit: Binary binding places context in transport headers; source/type/subject/correlation must not be copied into public MPE metadata. Event format supplies no security or delivery guarantee.
Existing: MPE-FMT-003, MPE-FMT-004, MPE-FMT-022, MPE-FMT-026, MPE-FMT-027, MPE-FMT-034, MPE-CON-010, MPE-CON-014.
Candidate: Adapter profile shall map canonical external event identity to sealed logical identity and preserve required context entirely inside encryption.
Acceptance: Round trip preserves source/id/type and payload; same event retry maps consistently; inspection of visible header and relay logs reveals no source/type/subject.

## 24 ASYNCAPI
Source: https://www.asyncapi.com/docs/reference/specification/v3.0.0
Mechanism: Machine-readable operations/channels/messages/security/bindings describing event-driven interfaces.
Adopt: Generated SDKs, registered codecs and reviewed workflow API contracts.
Limit: API description is not enforcement; schema delivery cannot execute remote code; public logical channel identifiers may reveal business routing.
Existing: MPE-FMT-025, MPE-FMT-026, MPE-FMT-027, MPE-CON-010, MPE-CON-011, MPE-CON-055.
Candidate: Product shall publish an AsyncAPI profile describing sealed logical channels, operation semantics, privacy profile and lifecycle outcomes; generators shall not expose logical channels as public relay topics.
Acceptance: Generate publisher/listener against specification; incompatible schema rejected before publication; generated API reports gap/finality/error correctly and privacy metadata remains sealed.

## 25 REACTIVE STREAMS
Source: https://www.reactive-streams.org/
Mechanism: Asynchronous streams with nonblocking backpressure and bounded demand.
Adopt: Async iterator demand, bounded local processing buffer, cancellation and explicit terminal/error semantics.
Limit: Backpressuring only recognized upstream messages exposes interests; blocking a network handler can disrupt repair or ledger confirmation.
Existing: MPE-CON-005a, MPE-CON-005b, MPE-CON-025a, MPE-CON-025b, MPE-STO-023, MPE-PRF-020.
Candidate: Listener implementation shall separate recognition-independent reception from bounded application processing and report resource exhaustion without hidden privacy downgrade.
Acceptance: Handler intentionally stalled under max workload; memory stays configured bound, cancellation releases buffers/tasks and resume reports any retention gap. Resource health does not vary with recognition in infrastructure transcript beyond declared profile.

## 26 DOM EVENTTARGET
Source: https://dom.spec.whatwg.org/#interface-eventtarget
Mechanism: addEventListener/removeEventListener, once and AbortSignal lifecycle controls.
Adopt: Familiar explicit lifetime/disposable handle and once semantics for UI wrappers.
Limit: Local once means callback lifetime, not exactly-once business action or durable resumption. Browser dispatch is no distributed ordering/finality guarantee.
Existing: MPE-CON-013, MPE-CON-014, MPE-CON-033.
Candidate: UI listener wrapper shall support explicit disposal/AbortSignal and document once versus durable processOnce.
Acceptance: Mount/unmount component repeatedly; no surviving duplicate callbacks or task leakage; abort prevents later callbacks; processOnce remains crash-durable while once alone is documented ephemeral.

## 27 NODE EVENTEMITTER
Source: https://nodejs.org/api/events.html
Mechanism: Synchronous ordered local listener invocation, explicit error event, once/on/off APIs and listener lifetime issues.
Adopt: Familiar API with isolated error reporting and asynchronous work queue.
Limit: Node synchronous local delivery must not be misrepresented as distributed global ordering; listener exception must not stop network repair; unhandled error event can be process-fatal.
Existing: MPE-CON-022, MPE-CON-033, MPE-CON-056.
Candidate: Node SDK shall isolate handler exceptions, offer explicit failure callbacks and dispose listener resources; handler completion is not finality.
Acceptance: One handler throws/rejects while another processes; reception and inventory repair continue, error is surfaced once, retries/dedup and unsubscribe semantics remain defined.

TOP TEN USE CASES FOR PRODUCT-REQUIREMENTS CONSIDERATION
Ranking is product judgment: specificity of privacy need, feasible initial backend pilot, measurable economic value and dependencies. No validated market-size/revenue claims. UC identifiers below are candidate portfolio identifiers, not new normative MPE requirement numbers. Actor/trigger/value are business requirements; feature enablers stay separate.

### UC-01 CONFIDENTIAL INSTITUTIONAL RFQ AND QUOTE ACCEPTANCE
Actors: buyer, authorized dealers, compliance reviewer, settlement agent.
Trigger: buyer requests a priced offer; dealers reply; buyer accepts one signed offer.
Value hypothesis: Less disclosure of trade intent and counterparties; shorter reconciliation and settlement handoff.
Existing: MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.
Candidate gap: Versioned RFQ/offer/accept/expire state machine, correlation policy, role/history permissions and explicit settlement handoff.
Acceptance: Two dealers return independently signed offers; expired/altered/replayed acceptance cannot settle, authorized acceptance settles once; crash recovery preserves accepted offer, unauthorized party cannot read content. Transcript analysis assesses interest privacy without claiming global timing anonymity.
Dependencies: Proof-capable signed-consumption implementation, role/key management, contract adapter, pilot dealer workflows. Start on backend/desktop.

### UC-02 PRIVATE SMART-CONTRACT STATUS AND LIFECYCLE NOTIFICATIONS
Actors: dapp user, wallet, contract observer.
Trigger: contract event such as settlement completion, escrow milestone or authorization change.
Value hypothesis: Timely useful notifications without publishing subscription interests or exposing private business data.
Existing: MPE-FMT-054, MPE-FMT-055, MPE-FMT-056, MPE-FMT-057, MPE-FMT-058; MPE-CON-015, MPE-CON-016, MPE-CON-017, MPE-CON-058, MPE-CON-059, MPE-CON-062, MPE-CON-063; MPE-SEC-022, MPE-SEC-025, MPE-SEC-026.
Candidate gap: Wallet UX templates and app-permission manifest; explicit delivery-state UI.
Acceptance: Delivered event remains provisional until exact bytes/position and successful applied phase are confirmed; failed fallible phase never final; revoked wallet app loses stream access.
Dependencies: Private event feature MPS-0005 Part 2 for private carried events, finalized-chain verification, mobile-efficient privacy profile for broad adoption. Public events can pilot earlier.

### UC-03 CONFIDENTIAL INVOICE, PAYMENT AND RECONCILIATION
Actors: supplier finance system, purchaser treasury, bank/payment or Midnight settlement adapter.
Trigger: invoice issued, approved, paid, disputed or refunded.
Value hypothesis: Reduce manual matching while protecting amounts, account relationships and invoice contents.
Existing: MPE-FMT-022, MPE-FMT-026, MPE-FMT-034, MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033, MPE-CON-043, MPE-CON-046; MPE-SEC-032, MPE-SEC-038.
Candidate gap: Invoice/payment/receipt identifiers, ERP connector and signed reconciliation schema; invoice attachment remains explicit fetch.
Acceptance: Same invoice emitted through retries is posted once; wrong-amount payment never marks paid; disconnect/restart catches up; failure receipt never executes payment; sensitive invoice data absent from broker logs.
Dependencies: ERP/treasury connector, payment-origin evidence, customer authorization policy and deployment funding.

### UC-04 PRIVATE PORTFOLIO AND COLLATERAL RISK ALERTS
Actors: account owner, risk engine, delegated agent.
Trigger: margin breach, liquidation risk, expiring order or abnormal exposure.
Value hypothesis: Earlier intervention without broadcasting portfolio/watchlist to notification infrastructure.
Existing: MPE-CON-020, MPE-CON-024, MPE-CON-028, MPE-CON-039, MPE-CON-043, MPE-CON-046, MPE-CON-056; MPE-SEC-025, MPE-SEC-032, MPE-SEC-037; MPE-PRF-020.
Candidate gap: Snapshot/delta risk schema, freshness policy, authenticated source connectors and bounded delegation.
Acceptance: Stale or gapped feed displays degraded status and blocks automated high-risk effect; replayed warning cannot trigger repeated action; timely processing measured under reference workload, no hard-real-time liquidation guarantee.
Dependencies: Hyperliquid/Solana/Ethereum adapters with declared trust/finality; mobile private delivery; external market data reliability.

### UC-05 DELEGATED AGENT COORDINATION AND HUMAN APPROVAL
Actors: enterprise worker, AI/business agent, approval officer, effect executor.
Trigger: agent proposes purchase, settlement, access grant or other bounded action.
Value hypothesis: Automate multi-party work with accountable approvals and protected instructions.
Existing: MPE-CON-033, MPE-CON-042, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-048; MPE-SEC-032, MPE-SEC-037, MPE-SEC-038; MPE-CRY-022.
Candidate gap: Capability-scoped delegation, signed approval schema, action budgets and approval expiry.
Acceptance: Agent requests action outside budget or to different target; reject despite valid message seal; approved in-scope action happens once; no arbitrary payload command execution.
Dependencies: Authority registry, application enforcement, human approval UI. MPE delivery itself cannot make AI output trustworthy.

### UC-06 CREDENTIAL, MEMBERSHIP AND ACCESS-REVOCATION UPDATES
Actors: issuer, subject wallet, employer/service verifier.
Trigger: credential issued/expired/revoked or staff/partner removed.
Value hypothesis: Reduce stale authorization while avoiding public subscription graph.
Existing: MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-SEC-020, MPE-SEC-028, MPE-SEC-033; MPE-CON-052, MPE-CON-058, MPE-CON-059.
Candidate gap: Versioned issuer lifecycle events and freshness/epoch semantics for verifier caches.
Acceptance: Revocation arrives after a delayed grant; higher authenticated issuer epoch wins; removed user cannot decrypt future stream generation; offline verifier reports stale rather than granting high-risk access silently.
Dependencies: Issuer-origin verification, onboarding policy, group rekey; identity records and legal effect remain application-owned.

### UC-07 CONSORTIUM PROCUREMENT AND SUPPLY-CHAIN EXCEPTIONS
Actors: buyer, supplier, logistics provider, insurer/auditor.
Trigger: purchase order accepted, delivery milestone reached, delay/temperature anomaly detected.
Value hypothesis: Faster exception resolution with limited sharing of commercial counterparties and terms.
Existing: MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-FMT-038; MPE-CON-014, MPE-CON-027, MPE-CON-028, MPE-CON-033; MPE-STO-022, MPE-STO-025.
Candidate gap: Role-scoped milestone schema, selective disclosure and signed sensor/operator provenance.
Acceptance: Authorized members recover milestones after outage within retention; unrelated member cannot read restricted events; sensor report is attributed but not falsely treated as proof the physical shipment occurred.
Dependencies: Enterprise/IoT gateway authentication, archived history policy if retention needed beyond ordinary window; commercially sensitive timestamps still require threat model.

### UC-08 CONFIDENTIAL INSURANCE CLAIM HANDOFF AND MILESTONES
Actors: claimant, insurer, adjuster, payment/reinsurance partner.
Trigger: claim submitted, evidence requested, assessment completed or payment approved.
Value hypothesis: Faster multi-party processing with narrowed exposure of claimant facts.
Existing: MPE-FMT-038; MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-014, MPE-CON-033, MPE-CON-046, MPE-CON-052; MPE-SEC-032.
Candidate gap: Claims-state schemas, attachment grants and retention/data-handling policy; large documents live in authorized encrypted storage.
Acceptance: Wrong role cannot open sensitive evidence; withdrawal blocks future access but does not promise deleting obtained copies; approval is authenticated and duplicate message cannot duplicate payment.
Dependencies: Sector-specific governance/privacy/legal review by customer, encrypted object service, long-history requirements. Do not assume protocol expiry erases copies.

### UC-09 PRIVATE GOVERNANCE PROPOSAL, REVIEW AND APPROVAL WORKFLOW
Actors: board/DAO committee, reviewers, execution agent.
Trigger: proposal submitted, confidential review requested, approval threshold met.
Value hypothesis: Coordinate sensitive deliberation and auditable authorization without exposing reviewer watchlists.
Existing: MPE-CRY-018, MPE-CRY-019, MPE-CRY-022; MPE-CON-033, MPE-CON-043, MPE-CON-044a, MPE-CON-044b, MPE-CON-046, MPE-CON-052, MPE-CON-060; MPE-SEC-037, MPE-SEC-038.
Candidate gap: Threshold approval/evidence schema, participant role policy and narrow disclosure package.
Acceptance: Insufficient/expired approvals cannot authorize action; authorized threshold effect commits once; evidence disclosed to auditor excludes unrelated deliberation; receipt of proposal is not approval.
Dependencies: Application multisig/threshold authorization and governance governance policy; no implicit private voting anonymity guarantee.

### UC-10 CONFIDENTIAL ENTERPRISE INCIDENT AND CROSS-CHAIN OPERATIONS COORDINATION
Actors: security/operations teams, service owner, chain adapter, authorized responders.
Trigger: service degradation, key compromise, delayed settlement or chain interruption.
Value hypothesis: Faster coordinated response with protected incident details and less dependence on one public notification provider.
Existing: MPE-SEC-028, MPE-SEC-032, MPE-SEC-036; MPE-CON-025a, MPE-CON-025b, MPE-CON-050, MPE-CON-051, MPE-CON-056; MPE-STO-022; MPE-CRY-026.
Candidate gap: Encrypted failure queue, scoped incident actions, cross-system adapters and private operational dashboard.
Acceptance: Simulated ledger outage keeps gossip notices flowing while reaction returns typed failure; operator redrive cannot execute stale/unauthorized command; handler crash does not silence other incident streams.
Dependencies: Out-of-band emergency recovery route, operator funding and SLOs. Do not position unproven overlay as sole safety-critical incident path or millisecond industrial control.

RECOMMENDED DISPOSITION
Adopt now into candidate product requirements: Encrypted structured-event adapter profile; explicit listener lifetime/cancellation; locally bounded async processing; truthful statuses; workflow correlation/expiry; encrypted failure/redrive handling; SDK onboarding and workflow examples.
Adapt with privacy review: SDK group roles and membership changes; mobile push; external chain backfill; consent/directory; selective audit disclosure.
Research separately: Interest-private mobile retrieval, multi-device ratchet/key-recovery composition, route-blinded first contact, threshold remote-origin verification.
Avoid: Plaintext business topics, content-aware relay filtering as default, auto acknowledgements, automatic blob/URL fetch, exactly-once arbitrary-effect marketing, equating anchors with authority, assuming a native event listener automatically invokes a Midnight contract.

Verification note: This review changes documentation only. Its recommended tests are acceptance criteria to be evaluated if candidate requirements are adopted. Each cited design should receive the other two independent reviewers before repository consolidation.
