# MPE-CON: Consumers (agents, contracts and wallets)

## 1. Scope of this area

This area covers what the MPE client library offers the parties that receive Events: agents and services, smart contracts (which react through a later transaction carrying a proof), wallets, and the DApps that wallets serve. It covers recognition, reception modes, the delivery labels `gossip` and `final`, deduplication, gaps, resume and back-fill, failure reporting, the contract consumption path and the SDK acceptance gates. It does not cover the Envelope layout, admission, mesh parameters, storage retention or Anchor production. Where a requirement here depends on those, it is listed under cross-area dependencies. Decision owned here: D3 (consumer side).

## 2. Parameters

| ID | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-CON-1 | Wait before a missing sequence number is reported as a suspected gap | 60 s | 10–600 s | o3 D3.3 (20 blocks on the ledger lane); adapted to the overlay p99 ≤ 10 s target of g1 D5 and o1 D5. **Assumption** |
| P-CON-2 | Retention of deduplication state beyond an Envelope's expiry | 1 h | 0–24 h | g1 D6 (ids kept one more hour); o1 D3 (seen-id cache for the expiry period) |
| P-CON-3 | Independent sources used by default per subscribed Shard | 2 | 1–5 | o3 r2 D7/D9; s1 D3; o4 r2 D3 |
| P-CON-4 | Interval between inventory comparisons with a second source | 60 s | 10–600 s | s1 D3 ("every minute") |
| P-CON-5 | Expected-Tag lookahead window per (stream, publisher) | 64 | 16–1,024 | o1 D3 (W = 64); o3 D3.1 (W = 32) |
| P-CON-6 | Recognition silence before a recognition-window gap is reported | 600 s | 60–86,400 s | **Assumption**; closes the defect o3 r2 D1 names and s4 r2 D3 asks for |
| P-CON-7 | Maximum recognition keys per client instance | 256 | 16–4,096 | s2 D3 (256-key cap) |
| P-CON-8 | Wait for an Anchor before an Event is reported unanchored | 300 s | 90–3,600 s | o1 D3 (60 s anchor window), read-out §1.7 (finality ≈ 18 s), o4 D5 (contract-visible p99 ≤ 90 s). **Assumption** |
| P-CON-9 | Pending-gap state per publisher, in sequence numbers | 1,000 | 32–10,000 | s2 D3 (`MAX_SKIP` = 1,000, s2's own constant per g1 r2) |
| P-CON-10 | Events in the Prototype chaos test | 10⁶ | ≥ 10⁵ | o3 D10 acceptance 2 |
| P-CON-11 | Upper bound of the random delay on helper-submitted reactions | 60 s | 0–3,600 s | o3 r2 D2 (asks for jitter but gives no number). **Assumption** |
| P-CON-12 | Concurrent reactors in the contract race test | 100 | ≥ 10 | o3 D10 acceptance 5 |
| P-CON-13 | Afternoon test: developers who must succeed, out of 5, and the time limit | 4 of 5, ≤ 4 h | 3–5 of 5, 2–8 h | o3 D10 acceptance 1; o3 r2 D10 |

## 3. Requirements

### A. Subscription and recognition

### MPE-CON-001 Local recognition
The MPE client library shall perform Tag recognition and decryption on the Consumer's host without sending any recognition key, decryption key, Tag set or topic identifier to a Bus Node, Store Node or Indexer.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g4, s1, s2, s3, s4, o3; `2020-vac-waku2-filter-spec` (Security Considerations); `2024-vac-adversarial-models` (Receiver Anonymity); read-out §4.4 (`connect(viewingKey)` discloses the key)
- Rationale: Interest-hiding from infrastructure is one of the agreed privacy claims, and a remote filter breaks it.
- Verify: test. Capture all client egress during a subscription and assert that no key, Tag or topic id appears in it.
- Status: settled

### MPE-CON-002 Whole-Shard retrieval by default
While in the default reception mode, the MPE client library shall retrieve every Envelope of each subscribed Shard.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g4, s1, s2, s3, s4, o3 r2; `1998-chor-pir` via g2 D2 (one-server privacy costs a full download)
- Rationale: Full retrieval hides which Events a Consumer selects. It does not hide that the Consumer participates.
- Verify: test. Compare the set of Envelope ids the source served with the set the client received over 1 h; they must be equal.
- Status: open (DEC-CON-1)

### MPE-CON-003 Recognition-independent requests
The MPE client library shall make the content and timing of its retrieval requests independent of which Envelopes it recognises.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1 D3 ("separate fetching from local recognition"); s3 D9 #10
- Rationale: Fetches that depend on matches leak selection to the source.
- Verify: test. Run two clients with disjoint key sets against the same feed and assert that their request traces are identical apart from transport noise.
- Status: settled

### MPE-CON-004 Opt-in for selective profiles
Where a selective-retrieval profile is present, the MPE client library shall activate it only when the application passes an explicit opt-in that names that profile.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D3; o1 r2 (reduced-privacy profile, separately labelled); o3 D3.2 (bucket mode); o2 D3 (S-FMD); g3 D3 (filter node); s1 r2
- Rationale: Mobile profiles leak more, so that leak must be a choice the developer makes and can see.
- Verify: inspection and test. A configuration without the opt-in must fail to start the profile.
- Status: open (DEC-CON-1)

### MPE-CON-005 No silent reception downgrade
If the active reception mode cannot be sustained, then the MPE client library shall raise a typed `degraded` error and shall keep the reception mode unchanged.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s3 D9 red-team block 4 ("silent fallback from whole-feed retrieval")
- Rationale: A silent switch to a leakier mode breaks the privacy claim without anyone noticing.
- Verify: test. Make every source unreachable and assert the `degraded` error and an unchanged mode.
- Status: settled

### MPE-CON-006 Keys only by invitation
The MPE client library shall add a recognition key only through an explicit application call that supplies an invitation.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1, s2, s3, s4 (invitations only), g4 (out-of-band key); o4 r2 D3 (harassment by unsolicited first contact)
- Rationale: With no unsolicited first contact at launch, a Consumer recognises only what it agreed to receive.
- Verify: inspection of the public API, plus a test that no code path adds keys from received data.
- Status: open (DEC-CON-8)

### MPE-CON-007 Tag lookahead window
The MPE client library shall hold, for each subscribed (stream, publisher) pair, the next P-CON-5 expected Tags.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o1 D3 (W = 64), o3 D3.1 (W = 32), o4 D3 (per-message PRF tags)
- Rationale: Recognition becomes a hash lookup instead of a trial decryption of every Envelope.
- Verify: test. After each recognised Event, assert that the lookahead set holds exactly the next P-CON-5 Tags.
- Status: open (DEC-CON-2)

### MPE-CON-008 Recognition-window gap
If no Event from a subscribed publisher is recognised for P-CON-6 while that publisher's Shard carries traffic, then the MPE client library shall emit `gap{reason:"recognition-window"}` for that publisher.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 r2 D1 (a publisher that abandons more than W numbers is never recognised again); s4 r2 D3 (needs a resynchronisation path)
- Rationale: The loss becomes visible instead of silent.
- Verify: test. The publisher skips 2 × P-CON-5 sequence numbers and the gap appears within P-CON-6 + 10 s.
- Status: open (DEC-CON-2)

### MPE-CON-009 Recognition key cap
If adding a recognition key would exceed P-CON-7 keys, then the MPE client library shall reject the addition with a typed `KeyLimit` error.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s2 D3; s3 D9 red-team block 5 (unbounded state)
- Rationale: Recognition cost and memory stay bounded per client.
- Verify: test. Add P-CON-7 + 1 keys and assert the error on the last addition.
- Status: settled

### MPE-CON-010 Generated codecs only
The MPE client library shall decode sealed bodies only with codecs generated from a schema the application registered.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4; `design/evidence/bitmessage-guide.md:354-358` via o3 (PyBitmessage `eval` RCE)
- Rationale: Decrypted data is attacker-controlled. Dynamic dispatch on it has led to remote code execution before.
- Verify: inspection. No reflective or dynamic decode path exists in the library.
- Status: settled

### MPE-CON-011 Undecodable Events delivered
When a recognised Event carries a schema identifier with no registered codec, the MPE client library shall deliver an `undecodable` item that carries the Envelope identifier.
- Pattern: event
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D1 (schema ids; "never dropped")
- Rationale: Schema upgrades must not look like message loss.
- Verify: test. Publish under an unregistered schema and assert one `undecodable` item.
- Status: settled

### B. Delivery semantics

### MPE-CON-012 At-least-once within retention
While at least one configured source retains an Envelope of a subscribed Shard, the MPE client library shall deliver each Event recognised in that Envelope to the application at least once.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; all twelve proposals (at-least-once); s4 D3 ("conditional on a reachable honest retained copy"); `midnight-js/packages/types/src/public-data-provider.ts:507-510`
- Rationale: This is the delivery promise every proposal makes, stated with its condition.
- Verify: test. Run fault injection with one retaining source and assert that every published Event reaches the handler.
- Status: settled

### MPE-CON-013 Deduplication by Envelope identifier
The MPE client library shall deliver each Envelope identifier to the application at most once per subscription for the Envelope's lifetime plus P-CON-2.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; g1, g2, g3, o1, o2, o4 (dedup by id); `rust-libp2p/protocols/gossipsub/src/config.rs:524` (`duplicate_cache_time` default 60 s)
- Rationale: The GossipSub seen-cache expires long before an Envelope does, so the overlay alone does not stop duplicates.
- Verify: test. Re-inject the same Envelope after 61 s and again near expiry, and assert a single delivery.
- Status: settled

### MPE-CON-014 Logical deduplication of retries
The MPE client library shall deliver at most one Event per authenticated logical event identifier to a `processOnce` handler.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1 D3 (retries keep the logical id); s3 D3; s2 D3
- Rationale: A sender's retry is a new Envelope with a new identifier, so Envelope dedup alone would apply the effect twice.
- Verify: test. Publish one logical Event as two Envelopes and assert one handler call.
- Status: settled

### MPE-CON-015 Delivery label on every Event
The MPE client library shall label every delivered Event with exactly one delivery label, `gossip` or `final`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 summary and D8 (each event labelled `final` or `gossip`); BRIEF area focus
- Rationale: Consumers must know whether an Event is ledger-backed before they act on it.
- Verify: test. Every delivered item has exactly one of the two labels.
- Status: settled

### MPE-CON-016 Meaning of `final`
The MPE client library shall label an Event `final` only after verifying that its Envelope identifier is included under an Anchor, or carried by a fallback `Misc` event, in a finalised Midnight block.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 (finalised only); o1 D3, o2 D3 (anchors); read-out §4.1 (indexer serves finalised blocks only)
- Rationale: `final` must mean ledger-anchored and finalised, checked by the client and not taken on a source's word.
- Verify: test with the mock Ledger Adapter. A forged inclusion path and an unfinalised Anchor must both leave the label at `gossip`.
- Status: settled

### MPE-CON-017 Upgrade notice from gossip to final
When an Event already delivered as `gossip` becomes covered by a verified finalised Anchor, the MPE client library shall emit a `finalised{eid}` notice.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D8 (same API, only labels change); o1 D3 (anchored order)
- Rationale: Agents act early on `gossip` and settle later on `final` without receiving the Event twice.
- Verify: test. Publish, observe `gossip`, anchor, and assert one `finalised` notice.
- Status: settled

### MPE-CON-018 Unanchored notice
If an Event delivered as `gossip` is not covered by a verified finalised Anchor within P-CON-8, then the MPE client library shall emit an `unanchored{eid}` notice.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o2 D9 (anchorer censorship residual); s3 D9 #8
- Rationale: Anchorer censorship or delay becomes visible to the Consumers that depend on finality.
- Verify: test. Suppress the anchorer and assert the notice after P-CON-8.
- Status: settled

### MPE-CON-019 One interface for both labels
The MPE client library shall deliver `gossip`-labelled and `final`-labelled Events through the same subscription call and the same item type.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D8 ("the consumer API stays the same; only the finality labels change"); o3 r2 D8
- Rationale: Applications survive a change of tether or a fallback without rewriting code.
- Verify: inspection of the API, plus a test that runs the same consumer against the overlay and against the fallback path.
- Status: settled

### MPE-CON-020 Suspected gap
When a recognised Event's sequence number leaves a missing lower sequence number for its publisher unfilled for P-CON-1, the MPE client library shall emit `gap{reason:"suspected"}` naming the publisher and the missing range.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 item 7; s3 D3, s4 D3 (explicit gap reporting); g1 D3 (gap is "not arrived" until expiry)
- Rationale: Omission on known streams becomes detectable.
- Verify: test. Drop sequence number n and assert the gap item after P-CON-1.
- Status: settled

### MPE-CON-021 Late fill
When an Event fills a range already reported as a gap, the MPE client library shall deliver it marked `late`.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 items 2 and 7
- Rationale: The application can reconcile a gap it already reported.
- Verify: test. Delay sequence number n beyond P-CON-1 and assert `gap`, then `late`.
- Status: settled

### MPE-CON-022 No hidden reordering
The MPE client library shall deliver each recognised Event without waiting for an earlier sequence number from the same publisher.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D3.3 item 2 ("hidden buffering is how consumers lose events when they crash"); against s3 D3 (bounded reordering)
- Rationale: An in-memory buffer loses Events on a crash. Gap and late markers expose order without holding Events back.
- Verify: test. Deliver n+1 before n and assert immediate delivery of n+1.
- Status: open (DEC-CON-4)

### MPE-CON-023 Bounded gap state
If a publisher's pending-gap state would exceed P-CON-9 sequence numbers, then the MPE client library shall emit `gap{reason:"overflow"}` and discard the oldest pending range.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s2 D3 (`MAX_SKIP`); s3 D9 red-team block 5; `2016-signal-double-ratchet-spec` §8.4 (via s2, s3)
- Rationale: A hostile publisher that sends very high sequence numbers must not be able to exhaust client memory.
- Verify: test. Inject a sequence jump of 10 × P-CON-9 and assert bounded memory plus the overflow item.
- Status: settled

### MPE-CON-024 Caught-up marker
When back-fill reaches the newest Envelope its source held at subscription time, the MPE client library shall emit one `head` item for that subscription.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 item 6; `nostr-nip-01` (EOSE); `midnight-indexer/indexer-api/graphql/schema-v4.graphql:1135-1137` (today only `maxId` comparison)
- Rationale: Consumers need to know when history ends and live delivery begins.
- Verify: test. Run back-fill of 1,000 Envelopes and assert exactly one `head`, placed after the last of them.
- Status: settled

### MPE-CON-025 Transport failures are typed
If a source connection fails, then the MPE client library shall surface a typed error to the subscription and shall not end the subscription as complete.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4; `midnight-js/packages/types/src/public-data-provider.ts:509-510`
- Rationale: A silent completion looks like "no more Events", which is loss.
- Verify: test. Kill the source mid-stream and assert an error, never completion.
- Status: settled

### MPE-CON-026 Closed publish result set
When a publish call returns, the MPE client library shall report exactly one of `accepted` (at least one mesh peer holds the Envelope), `final`, or `failed{reason}` from a closed reason set.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4 (typed `InsufficientDust`, `BusPaused`, `TooLarge`, `TxFailed`); g1 D3 (hot path returns when a mesh peer holds the object)
- Rationale: Publishers, including agents, must be able to tell what happened to a publication.
- Verify: test of each failure cause, asserting the matching reason.
- Status: settled

### C. Resume and back-fill

### MPE-CON-027 Portable cursor
The MPE client library shall express resume cursors in a form that any source serving the same Shard accepts.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D1 and r2 D1; `midnight-indexer/docs/re-indexing.md:78-95` (two instances, secondary re-indexed from empty)
- Rationale: A cursor tied to one instance can skip or repeat Events on failover. Whether indexer `id` values are stable across instances is **unknown**.
- Verify: test. Commit a cursor against source A, resume against source B, and assert no Event is lost.
- Status: settled

### MPE-CON-028 Inclusive resume
When the application subscribes from a committed cursor, the MPE client library shall deliver every retained recognised Event at or after that cursor that is absent from the committed deduplication state.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 item 5; s1 D3 ("inclusive resume cursors"); `schema-v4.graphql:1966-1971` (inclusive id)
- Rationale: An inclusive replay plus deduplication gives a crash-safe resume.
- Verify: test. Crash at random points and assert that the union of deliveries equals the set of published Events.
- Status: settled

### MPE-CON-029 Back-fill by complete window
The MPE client library shall request back-fill only as complete time windows of a Shard.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1, s3, s4 D3; g1 D3 ("never by topic"); g2 D3; g3 D3
- Rationale: Requests by Tag or by a subset of identifiers reveal selection to the Store Node.
- Verify: test. Inspect back-fill requests and assert they carry only a Shard and a time range.
- Status: settled

### MPE-CON-030 Back-fill window reported
The MPE client library shall report, through a capabilities call, the back-fill window as the minimum of source retention and local key retention.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D6 (`bus.capabilities()`); o3 r2 D6
- Rationale: Developers learn the offline limit before they hit it.
- Verify: test. Set retention to 48 h and key retention to 24 h, and assert a reported window of 24 h.
- Status: settled

### MPE-CON-031 Key-erased gap
If back-fill covers a period for which the client holds no key, then the MPE client library shall emit `gap{reason:"key-erased"}` for that period.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.3 item 5; s2 D3 ("storage availability does not imply decryptability")
- Rationale: Key deletion gives forward secrecy, and its cost must be visible rather than silent.
- Verify: test. Erase epoch keys, back-fill that epoch, and assert the gap.
- Status: settled

### MPE-CON-032 Retention gap
If a resume cursor is older than the oldest Envelope held by every configured source, then the MPE client library shall emit `gap{reason:"retention"}` with the uncovered time window.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 r2 D6 (a consumer offline over a weekend); g3 D3 (48 h horizon)
- Rationale: Without this, "at least once within retention" quietly becomes "at most once" for intermittent Consumers.
- Verify: test. Resume beyond retention and assert the gap with the correct bounds.
- Status: settled

### MPE-CON-033 Atomic processOnce
The MPE client library shall provide a `processOnce` call that commits the application effect, the cursor and the deduplication state in one atomic write to an application-supplied store.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D3.4–3.5; s2 D3 ("persist processing and cursor advancement atomically"); s3 D3
- Rationale: Exactly-once effects need atomicity; transport delivery alone is at least once.
- Verify: test. Kill the process between effect and commit and assert one effect after restart.
- Status: settled

### MPE-CON-034 Chaos acceptance
The Prototype shall complete a P-CON-10-Event run, with random Bus Node restarts, source failovers and client crashes, passing zero lost Events and zero duplicates to `processOnce` handlers.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D10 acceptance 2; o3 r2 D10
- Rationale: This tests delivery as consumers experience it, beyond the relays.
- Verify: test. Run the scripted chaos harness and compare handler logs with the publish log.
- Status: settled

### MPE-CON-035 Delivery model check
The MPE client library delivery state machine shall satisfy, in a bounded model check, that no committed cursor skips an undelivered retained Event and that `processOnce` passes each logical identifier at most once.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 D10 Phase 0 (e); o3 r2 D10; s3 D10 Phase 0
- Rationale: Model checking finds failover interleavings that tests miss.
- Verify: analysis. Quint model including source failover; both invariants hold to the stated depth.
- Status: settled

### D. Completeness

### MPE-CON-036 Independent sources by default
The MPE client library shall, by default, retrieve each subscribed Shard from at least P-CON-3 sources run by different Operators.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 r2 D7 and D9 ("cross-checking two independent sources as the default"); s1 D3; o4 r2 D3
- Rationale: A single source can omit Events undetectably, in particular first-contact Events and whole publishers.
- Verify: test. With default configuration, assert connections to P-CON-3 distinct Operators per Shard.
- Status: open (DEC-CON-5)

### MPE-CON-037 Inventory repair
While subscribed to a Shard, the MPE client library shall compare its Envelope-identifier inventory with a second source every P-CON-4 and fetch every Envelope it lacks.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; s1 D3 ("repair all differences, independent of private matches"); s3 D9 #10
- Rationale: This reduces omission by one source without revealing which Envelopes matter to the client.
- Verify: test. Source A withholds 1% of Envelopes; assert all of them are delivered within P-CON-4 + 10 s.
- Status: open (DEC-CON-5)

### MPE-CON-038 Anchor count check
When a verified finalised Anchor covers a subscribed Shard window, the MPE client library shall emit `incomplete{window}` if its inventory for that window lacks any anchored Envelope identifier.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D3; o1 D3 ("anchors let a client check completeness against the on-chain count"); o3 r2 D9
- Rationale: The ledger gives an omission check that does not rely on any one source.
- Verify: test. Withhold one anchored Envelope from all sources and assert the item.
- Status: settled

### E. Reactions and contract consumption

### MPE-CON-039 No automatic network action
The MPE client library shall send no network message, acknowledgement or transaction as a consequence of recognising an Event.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 r2 D2 ("no automatic reaction"); g1, g2, s1, s3 (no receipts); `design/evidence/bitmessage-guide.md:265-267` via o3
- Rationale: Reactions tied to matches link the Consumer to the Event by timing.
- Verify: test. Compare egress with and without matching keys; it must be identical.
- Status: settled

### MPE-CON-040 Reaction delay
Where the application submits a reaction through the library's reaction helper, the MPE client library shall delay submission by a uniformly random interval in [0, P-CON-11].
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 r2 D2 ("reactions batched or jittered by default"); s3 D9 #3 (delayed effects)
- Rationale: The delay weakens linkage between publication and reaction. It is not an anonymity property.
- Verify: test. Over 1,000 reactions, the delays fit uniform [0, P-CON-11] (KS test, p > 0.01).
- Status: open (DEC-CON-7)

### MPE-CON-041 Off-chain blob fetch is explicit
The MPE client library shall fetch an off-chain blob referenced by an Event only through a call whose type marks the fetch as observable.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 r2 D2 ("fetches of off-chain blobs flagged as a leak in the type system"); o3 D1 (blob references)
- Rationale: A blob fetch reveals interest to the blob host.
- Verify: inspection. No implicit blob fetch path exists.
- Status: settled

### MPE-CON-042 Contract reaction by later transaction
The MPE client library shall provide a reaction builder that produces a Midnight transaction calling a target contract circuit, with the Event supplied as private witness data.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; all proposals except g4 (contract via later transaction); read-out §5.4, §8, §9 item 12; `minokawa-compact/doc/compact-reference.mdx:1153` (witnesses are callbacks)
- Rationale: Contracts cannot read Events or call out. Consumption is a submitted transaction.
- Verify: demonstration on a local ledger-9 network, or test against the mock Ledger Adapter.
- Status: settled

### MPE-CON-043 Publisher authorisation in circuit
The MPE client library's consumption circuit shall assert a publisher signature over genesis, target contract, action, logical identifier, expiry and payload digest, against a publisher set committed in the target contract's state.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; s3 D3 and D9 #1; s2 D3; o3 r2 D3; o1 r2 D3; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:921` (`jubjubSchnorrVerify`), `:993` (`ed25519Verify`)
- Rationale: An Anchor proves bytes, not authority. A forged witness is the top-ranked consumer threat.
- Verify: test. Wrong key, wrong target, wrong action and wrong genesis each fail proof generation.
- Status: open (DEC-CON-3)

### MPE-CON-044 Exactly-once contract effect
The MPE client library's consumption circuit shall reject a reaction whose consumption nullifier is already in the target contract's nullifier set, and shall insert the nullifier in the same transaction as the effect.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; o3 D3.5 step 4; s3 D3; s2 D3; o1 D3
- Rationale: Replayed reactions produce no second effect.
- Verify: test. Submit the same reaction twice and assert that the second is rejected.
- Status: settled

### MPE-CON-045 Secret-derived nullifier
The MPE client library's consumption circuit shall derive the consumption nullifier from a secret carried inside the sealed Event, never from the public Envelope identifier alone.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; s1 r2 D3 and s4 r2 D3 (o1's `hash(ev.id ‖ domain)` is enumerable); o3 D3.5 (`H("consumed" ‖ event_secret)`)
- Rationale: A nullifier computed from the public id tells observers which Event was consumed.
- Verify: analysis. The nullifier is not computable from public data; a test tries all observed Envelope ids against it.
- Status: settled

### MPE-CON-046 Expiry enforced
The MPE client library's consumption circuit shall reject an Event whose signed expiry is earlier than the block time of the reacting transaction.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; s2 D3 (destination, expiry); s3 D3; `exports.md` block-time predicates via s2
- Rationale: This bounds how long a captured Event can drive a contract.
- Verify: test. React after expiry and assert the rejection.
- Status: settled

### MPE-CON-047 Optional publication proof
Where an application requires proof of publication before a time, the MPE client library's consumption circuit shall verify inclusion of the Envelope identifier under an Anchor root accepted by the Registry's historic-root check.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D3; o1 D3; o3 D3.5; o1 r2, o3 r2 (anchor optional); `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:96-104` (witness-free callee); g1 r2 D3 objection
- Rationale: A signature alone does not prove dissemination. Some applications need that proof.
- Verify: test on a local ledger-9 network. A forged path fails and a stale accepted root passes.
- Status: open (DEC-CON-3)

### MPE-CON-048 No infrastructure output as authority
The MPE client library shall offer no contract-consumption API that accepts output from a Bus Node, Store Node or Indexer as evidence of publisher authorisation.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D3; s3 D9 red-team block 3; s1 D3 ("a relayer's claim that it saw a message is insufficient")
- Rationale: Infrastructure can forge or replay. Authority comes only from in-circuit checks.
- Verify: inspection of the API surface.
- Status: settled

### MPE-CON-049 Reactor race test
The Prototype shall show, with the mock Ledger Adapter, exactly one contract effect when P-CON-12 reactors submit reactions for the same Event concurrently.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; o3 D10 acceptance 5; s3 D10 ("zero duplicate contract effects")
- Rationale: Exactly-once must hold under contention.
- Verify: test. Count the effects in the mock ledger state; the count must be 1.
- Status: settled

### MPE-CON-050 Ledger paused
If the Ledger Adapter reports that Midnight rejects user transactions, then the MPE client library shall return a typed `LedgerPaused` error to reaction and fallback-publish calls.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; o3 D9 (typed `BusPaused`); `midnight-node/runtime/src/check_call_filter.rs:44-45` (safe mode filters `send_mn_transaction`)
- Rationale: A governance pause is a known liveness boundary and must be reported, not retried silently.
- Verify: test. Set the mock adapter to paused and assert the error.
- Status: settled

### MPE-CON-051 Gossip continues while ledger unavailable
While the Ledger Adapter reports Midnight unavailable, the MPE client library shall continue delivering recognised Events labelled `gossip`.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; o3 D9 (Lane A stops during a pause; the overlay continues); o1 D8
- Rationale: The overlay keeps delivering when the ledger cannot.
- Verify: test. Pause the mock ledger and assert continued `gossip` delivery with no `final` labels.
- Status: settled

### F. Wallets, fallback path and ergonomics

### MPE-CON-052 Wallet grants
Where a wallet hosts the MPE client library, the client library shall release a stream's Events to a DApp only under a grant for that stream issued by the wallet user.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 D3.5; o1 D3 (U5 `bus` capability); o4 D3 (`subscribeEvents`); `midnight-dapp-connector-api/src/api.ts:70-203` (no event method today)
- Rationale: DApps never hold keys for streams they were not granted, and they do not open IP-revealing connections of their own.
- Verify: test. A DApp without a grant receives nothing; a DApp with a grant receives only that stream.
- Status: open (DEC-CON-6)

### MPE-CON-053 Fallback path read
While the fallback `Misc` path is active, the MPE client library shall read fallback Envelopes through the Indexer adapter using the bus contract address as the only filter.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D3; g4 D3; o3 D8; o1 D8; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:548-562` (address required; prefixes apply to standard events only)
- Rationale: The address filter is the same for every subscriber, so it reveals no interest.
- Verify: test. Inspect Indexer adapter queries; only the address and the `MISC` type appear.
- Status: settled

### MPE-CON-054 Consumer bandwidth metering
The MPE client library shall report to the application the bytes received per subscribed Shard per UTC day.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D3; o3 r2 D5 ("the per-consumer figure is never gated"); o3 D5 (≤ 60 MB/day); g4 D5 (56 MiB/day)
- Rationale: This lets a consumer bandwidth budget be gated with measurements.
- Verify: test. The reported count matches captured traffic within 1%.
- Status: settled

### MPE-CON-055 Afternoon test
The MPE client library shall enable P-CON-13 of 5 developers from outside the team, each using only its documentation, to build a publisher and a crash-resuming subscriber within the P-CON-13 time limit.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D3; o3 D10 acceptance 1; o3 r2 D10
- Rationale: Consumers who mishandle duplicates, gaps or cursors lose Events, whatever the relays do.
- Verify: demonstration. A timed study whose subscribers then pass a crash-resume check.
- Status: settled

## 4. Decisions

**DEC-CON-1 Default reception mode.** Options: (a) whole-Shard download only (g1, g2, g4, s1, s2, s3, s4, o3 r2); (b) whole-Shard by default, plus selective profiles behind an explicit opt-in that names them (o1 r2: tag index with decoys; o3 R1: bucket mode; g3: filter node; o4: store query by Tag); (c) S-FMD detection as a standard mobile mode (o2). **Recommended: (b), with no selective profile in the Prototype.** Full retrieval is the only mode with agreed selection privacy, but s1 r2, s4 r2 and o1 r2 all say it excludes mobile users. A labelled opt-in keeps that leak visible (s3 block 4). FMD-style recovery of the social graph is cited by o3 and s1. Settling check: measure per-consumer bytes per day at the performance area's target load (MPE-CON-054) against the ≤ 60 MB/day budget (o3, g4). A selective profile ships only with a reviewed leakage analysis from the privacy area.

**DEC-CON-2 Recognition mechanism.** Options: (a) PRF Tags with an expected-Tag lookahead (o1, o4, o3 R1, and the BRIEF glossary "Tag"); (b) trial AEAD on every Envelope (g1, g4, o3 r2, which withdrew tags); (c) encrypted-header trial under a capped key set (s2; s4 uses a recognition hint). **Recommended: (a) plus the recognition-window gap (MPE-CON-008) and the key cap (MPE-CON-009).** It matches the glossary, and lookup cost does not grow with the key count. The defect o3 r2 names, a publisher skipping more than W numbers, becomes a reported gap instead of silent loss. Settling check: benchmark recognition CPU per day under (a), (b) and (c) at the target load with 256 keys, and simulate publisher skips greater than W. The envelope-format area owns the Tag construction.

**DEC-CON-3 Contract consumption path.** Options: (a) an in-circuit publisher signature with a target-scoped, secret-derived nullifier and no Anchor (s3, s2, s1, o3 r2, o1 r2, o2 r2); (b) Anchor inclusion through a historic-root cross-contract check (o1 R1, o3 R1, o2, o4, g3); (c) `note(commitment)` (g1); (d) no contract consumption (g4). **Recommended: (a) by default and (b) as an option (MPE-CON-047).** (a) needs no cross-contract call, and it puts authority in the circuit, which s3 #1 and o4 D3 both require. (b) answers g1 r2's objection that a signature does not prove dissemination. o3 r2's property X (the publisher is hidden through a membership proof) is a SHOULD that awaits circuit cost data. Settling check: build both circuits on a local ledger-9 network (`building-blocks.mdx:79-83`: public networks run ledger 8) and measure circuit size and proving time. Then run the Phase-0 model, which must show zero unauthorised effects and zero duplicate effects.

**DEC-CON-4 Ordering and buffering.** Options: (a) arrival order with `gap` and `late` markers and no hidden buffer (o3); (b) bounded out-of-order processing (s3); (c) no ordering help, with order taken from the indexer or chain (g2, g4). **Recommended: (a).** Hidden buffers lose Events on a crash, and (a) still exposes every disorder. Settling check: the Quint model (MPE-CON-035) plus the afternoon test. If developers fail on ordering, add an opt-in, persisted reorder bound of at most P-CON-9.

**DEC-CON-5 Source cross-checking.** Options: (a) at least two independent sources by default, with periodic inventory repair (s1, o3 r2, o4 r2); (b) one source, with a second optional (g4, o3 R1). **Recommended: (a).** o3 r2 shows that the publisher-sequence check cannot detect first-contact or whole-publisher omission, and s3 #10 shows that selective omission is cheap for a source that controls the gateway. Settling check: an omission-injection test (detection rate) and the measured bandwidth overhead of inventory exchange at the target load.

**DEC-CON-6 Wallet integration.** Options: (a) the wallet holds bus keys and the DApp connector gains `subscribeEvents` with grants (o1, o3, o4, o2); (b) a local agent serves the wallet over localhost with no connector change (g1); (c) wallets unchanged, with mobile staying on the indexer (g2, g4). **Recommended: (a) for PROD and nothing in the Prototype.** DApp-opened connections reveal the user's IP (o4 D3), and DApps should not hold keys they were not granted (o3). Settling check: review by the wallet and connector maintainers, plus a grant-isolation test (MPE-CON-052).

**DEC-CON-7 Reaction timing.** Options: (a) a random delay by default on helper-submitted reactions (o3 r2); (b) no delay, with the leak documented (s1, g4). **Recommended: (a), which the application can override.** It is cheap and makes no anonymity claim. Settling check: the privacy area simulates timing linkage at the target load with and without the delay, against the contract-visible latency target (o4: p99 ≤ 90 s).

**DEC-CON-8 First contact.** Options: (a) invitations only at launch (s1, s2, s3, s4, g4); (b) an inbox, with a stricter admission tier for first contact (o1, o3, o4, g1). **Recommended: (a) for the client library at launch.** o4 r2's harassment objection and the undetectable omission of first-contact Events (o3 r2) both remain open. Settling check: a later, separately reviewed inbox profile with recipient consent controls and a measured abuse rate.

## 5. Cross-area dependencies

IDs are expected, not yet known. The merge step assigns the area codes.

- **Envelope format area:** the sealed body carries a per-publisher sequence number, an authenticated logical event id, a signed expiry, a schema id, a consumption secret and a publisher signature. The Envelope identifier is computable by any source (needed by 013, 014, 020, 043–046). Tag construction and its resynchronisation rule (DEC-CON-2).
- **Anchor/Registry area:** Anchors commit to the Envelope identifiers of a window, with inclusion paths and a per-Shard count. They expose a witness-free historic-root check. The anchoring cadence must meet P-CON-8 (needed by 016–018, 038, 047).
- **Storage area:** Store Node retention, complete-window back-fill by Shard and time, and an inventory listing of Envelope identifiers per window (needed by 012, 029, 032, 037).
- **Network area:** the Bus Node interface for a non-mesh client to stream one Shard, and the GossipSub message-id function (needed by 002, 013).
- **Ledger Adapter / tether area:** reporting of finalised blocks, pause status and the fallback `Misc` path (needed by 016, 050, 051, 053).
- **Performance area:** the consumer bandwidth budget and the target load (DEC-CON-1, 054).
- **Privacy area:** the leakage statement for full-Shard reception, reactions and selective profiles (DEC-CON-1, DEC-CON-7).
- **Admission area:** publish failure reasons (026).

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Delivery label | `gossip` (received from the overlay, not yet verified as anchored) or `final` (verified as included under a finalised Anchor, or carried by a finalised fallback `Misc` event) |
| Source | A Bus Node, Store Node or Indexer adapter endpoint that the client library retrieves Envelopes from |
| Stream | A sequence of Events from one or more publishers under one key, with a sequence per publisher |
| Invitation | An application-supplied object that carries stream keys, publisher keys and schema ids |
| Cursor | A resume position that any Source serving the same Shard accepts |
| Gap item | A delivered marker with reason `suspected`, `recognition-window`, `overflow`, `key-erased` or `retention` |
| Head item | A marker that back-fill has reached the Source's newest Envelope at subscription time |
| Logical event identifier | An authenticated identifier that is stable across a publisher's retries |
| Reaction | A Midnight transaction that consumes an Event in a contract circuit; the submitter is the Reactor |
| Consumption circuit | The Compact module shipped with the client library that checks authorisation, expiry and the consumption nullifier |
| Consumption nullifier | A secret-derived value that the target contract stores to make a Reaction effect exactly once |
| Reception profile | The retrieval mode: whole-Shard (default) or a named selective profile |

## 7. Gaps

- **Completeness against an adversarial source.** Per-publisher sequences cannot detect a withheld first-contact Event or a whole suppressed publisher (o3 r2 D9). Requirements 036–038 reduce the risk but cannot prove completeness: if every source colludes, nothing on the consumer side detects it. No testable requirement exists for that case.
- **"Honest source" in at-least-once delivery.** A consumer cannot check honesty. Requirement 012 is therefore conditioned on retention by a configured source, which a test can control and a deployment cannot.
- **Timing privacy of Reactions.** A public contract effect re-links the Reactor to the Event's time (s1 D3, g4 r2). The jitter in 040 is a heuristic. No requirement can promise unlinkability against an observer who sees both the overlay and the ledger.
- **Mobile private reception.** No profile with selection privacy equal to full download has a demonstrated cost (s4 r2, o1 r2). There is nothing to require until DEC-CON-1 is settled by measurement.
- **Source-contract provenance.** A publisher signature proves a key holder's statement, not that a contract executed (s2 D3, s3 D3). Contract-origin Events need a commitment in the source contract. That belongs to the application, not the client library.
- **Contract liveness.** No Event triggers a contract by itself (o3 D3.5). Bounties are an application pattern, so this area has no obligation to write.
- **Ledger generation.** The anchor-based option (047) needs ledger-9 cross-contract calls, and public networks run ledger 8 (`building-blocks.mdx:79-83`; `toolchain-0.33.0.md:10-12`). Whether the signature path (043) also runs on ledger 8 is **unknown**. The availability of `jubjubSchnorrVerify` or `ed25519Verify` on the ledger-8 toolchain has not been checked.
- **Indexer `id` stability across instances.** This is **unknown** (o3 D1). Requirement 027 avoids depending on it. A diff of primary and secondary `contractEvents` ids would settle it.
- **Read-side funding.** Full-Shard reception costs grow with the number of Consumers, and no payment path exists (o3 r2 D4, read-out §2.3). This is an operator-economics question, not a consumer requirement.
