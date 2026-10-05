# Durable consumer lifecycle: resume, replay, and expired delivery

Role: durable consumer engineer. Model: Grok. Research date: 2026-10-05. Owned outputs: this report and `../sources/grok-recovery-lifecycle/`. No implementation, website, or other research files were edited.

The question is how a private Midnight Express watch survives disconnect, reload, retention loss, and duplicate delivery without treating an inbox handoff, a local disposition, or a business effect as the same fact. The current product draft at `docs/product-requirements/pubsub-subscription-experience.md` matches the website proof of concept. Research drafts in `wiki-llm/pubsub/` were treated as hypotheses and checked against primary captures.

## Research approach

Compared the local subscription page, the proposed control-plane contract, and the product draft with primary sources already retrieved by Scrapling into this lane: NATS server `v2.15.0` consumer configuration and the current pull-consumer documentation, Reactive Streams JVM `v1.0.4`, gossipsub v1.1 at the pinned libp2p spec commit, the WHATWG Storage and Web Storage standards, Chrome's extension service-worker lifecycle, Moth origin-grant storage at the pinned wallet commit, and the public UmbraDB branch tips. Kafka's design document at tag `4.3.1` was fetched after the first pass and checked on PixelRAG tiles. The first screenshot was a network-error page and is recorded as a failure. The second capture rendered the document.

`accepted_source` in the helper is an HTTP heuristic. Each claim below was checked against the saved text. Discovery responses, directory listings, and HTTP 404 bodies are pins or failures, not protocol semantics. No builtin web search was used. Local repository tip used for the proof of concept is `5ff9627c30d06837c931fc4783ca271455bdeb1a` (2026-10-04, "Remove counted framing from product prose and website controls"). The worktree had unrelated modifications; they were not edited.

## Intermediate findings and pins

### Local proof of concept

`website/dist/subscriptions.js` keeps fixtures, watches, the inbox, the journal, the seen-set, and the decided-set in module memory. Reload and Reset drop all of them. Reset's own status line says Moth origin grants are unaffected. Nothing in the page calls `localStorage`, `sessionStorage`, IndexedDB, or a service worker.

What the page actually does:

- A journal append assigns a monotonic local cursor. At 64 originals, intake stops. Undecided originals are not evicted.
- Dispatch moves a queued original into an in-flight set capped at 2 and a queue capped at 4 events or 16384 bytes. The delivery cursor becomes that original's cursor at handoff. Pause stops dispatch. Already in-flight items can still be dispositioned.
- The process control records an in-memory decision. The processing cursor advances only across a contiguous prefix of decided cursors for that watch. The recorded disposition of an ordinary item is "reviewed locally; no effect executed".
- A repeated fixture with `source` and `id` is suppressed for that watch. An unsigned mock has no authenticated occurrence identity, so a replay creates another item. A changed-clock quote fixture is labeled quarantined. The processing cursor still waits for the explicit process control.
- A retention gap is a visible state. The page refuses to invent an archive and refuses a silent jump. Recovery from a non-retention gap replays originals still held in the same memory. Permission is a mock flag, separate from the wallet. Consumer persona is copy. The page says connecting Moth does not unlock the simulation.
- Export writes a JSON blob labeled mock-only synthetic state.

The page is a faithful vocabulary demo of the product draft: two cursors, bounded pull, explicit gap, occurrence suppression for fixtures, and a hard line between review and effect. It is not evidence of restart-safe checkpoints, crash atomicity, cross-tab isolation, lease expiry, archive recovery, or wallet resume.

The proposed contract in `wiki-llm/pubsub/subscription-contracts.md` already separates `deliveredCursor`, `processedCursor`, `gap`, and action deduplication that survives unsubscribe. The page implements the first three only in RAM, and it has no action ledger at all. Proposed service maxima in that draft are larger than the page caps. The page caps are demo bounds.

### NATS JetStream, server v2.15.0

Release `v2.15.0` was published 2026-09-17. `server/consumer.go` and `server/jetstream.go` were fetched at that tag. The live pull-consumer page `https://docs.nats.io/learn/jetstream/pull-consumers` returned HTTP 200 and its navigation labels 2.15 as latest. Docs repository `nats-io/nats.docs` defaults to `master`, last pushed 2026-08-24. `SUMMARY.md` on `main` returned HTTP 404 (14 bytes). That 404 is a branch miss, not a statement about JetStream.

From `consumer.go` at that tag:

- `DeliverPolicy` selects a start: all, last, new, start sequence, start time, or last per subject.
- `AckPolicy` is `none`, `all`, `explicit`, or `flow_control`. `AckAll` implicitly acknowledges every sequence below the acked one. `AckExplicit` requires an ack or nack per message.
- Default `AckWait` for explicit or all policies is 30 seconds. Default `MaxAckPending` for explicit consumers that omit the field is 1000. Default `MaxDeliver` is unlimited (`-1`).
- Ack subjects accept `+ACK`, `-NAK`, `+WPI` (progress), `+NXT`, and `+TERM`. Documented term reasons include "Message deleted by stream limits" and "Unacknowledged message was deleted".
- `ReplayPolicy` is instant or original timing. It controls replay pacing of messages the stream still holds. It is not an effect receipt.

The pull-consumer page says a durable consumer keeps its identity across worker restarts, fetch asks for a bounded batch and returns on batch size or timeout, and the consumer cursor advances as messages are acked. Consume is the same pull, driven in a loop by the client library. A fetch timeout is a poll bound. It does not acknowledge anything.

Useful local mapping: a named watch plus an acknowledgement of a durable disposition, with redelivery while the ack floor has not moved. The 30-second ack wait, subject names, and server-side consumer are not local requirements. `AckAll` can slide a floor across a hole; the Midnight Express processing cursor must not.

### Reactive Streams 1.0.4

GitHub `releases/latest` for `reactive-streams/reactive-streams-jvm` returned HTTP 404 with the same 144-byte body as the Kafka releases endpoint. The tag `v1.0.4` exists at commit `944163a4b2477a2bebaaada86b0ba910b6302f2f`. The README at that tag is the spec that was read.

The spec governs demand across an asynchronous boundary. Publisher rule 1.1: `onNext` signals stay within the subscriber's requested demand. The subscriber must `request(n)` to receive elements and must `cancel()` when it no longer needs the subscription. Cancellation must eventually stop signals. `onComplete` and `onError` cancel the subscription. There is no cursor, no retention, no identity, and no replay.

This is the right model for `maxInFlight` and for pause/close as local cancellation. It is not a journal. Mapping watch expiry onto `onComplete` would be a mistake, because a terminal signal in Reactive Streams drops the subscription, while effect deduplication has to outlive the watch.

### Gossipsub

Spec file `pubsub/gossipsub/gossipsub-v1.1.md` was fetched at libp2p commit `98c5aa9421703fc31b0833ad8860a55db15be063` (committer date 2023-11-12, message "mispelling"). The v1.1 text limits `IWANT` responses per peer and caps `IHAVE` advertisements. It refers to a message cache as the place an `IWANT` can still be answered. The v1.0 document body was not fetched, so cache size, cache time, and seen-cache behavior are not established here.

What is established is enough for the lifecycle decision. Gossipsub repair is a short relay cache plus mesh gossip. It is not a consumer ack floor, and it must not become one. A missed envelope is a store-repair or explicit gap, as the product draft and the stack-feasibility report already require. Stalling intake to apply consumer backpressure would couple private match behavior to network timing. Intake stays independent of which watches match.

### Browser and extension ephemerality

WHATWG Storage (`https://storage.spec.whatwg.org/`, fetched 2026-10-05, text sha256 `45adfe63e47b490417cdead764e2b7d0bc10c7c71acfc5a42ef18d2e6a4eb2f1`): the default bucket is best-effort. Under storage pressure the user agent should clear best-effort local buckets. Persistent mode requires the `persistent-storage` permission. Revoking that permission sets the default bucket back to best-effort. Session storage buckets are cleared as traversable navigables close. Quota is an implementation-defined estimate. A page that stored a journal in the Storage API without a granted persistent bucket would still be allowed to lose it.

WHATWG Web Storage (`https://html.spec.whatwg.org/multipage/webstorage.html`, text sha256 `b2a400556925e7dee7f4fccc3d1c3aec6134bb2cf73a7e2667e4980ad1e5e86f`): `sessionStorage` is the `Storage` object for that window origin's session storage area. The privacy section says user agents may expire stored data, may treat third-party local storage as session-only, and should treat the data as sensitive. A quota or policy failure throws. This API is a small origin-scoped map. It is not an atomic multi-record journal.

Chrome's extension service-worker lifecycle page (HTTP 200, final URL unchanged): Chrome normally terminates the worker after 30 seconds of inactivity, when one event or API call runs longer than 5 minutes, or when a `fetch()` response takes more than 30 seconds. Global variables die with the worker. The page states that the Web Storage API is not available in extension service workers, and tells authors to use `browser.storage` or IndexedDB. An incoming event restarts the worker. It does not restore globals.

### Moth grant is not a watch checkpoint

`packages/extension/lib/background/permissions.ts` at `shieldedtech/moth-wallet` commit `d48206a1957af09bf17bf5e941c2b5bccb12db63` (commit date 2026-10-01, current tip of the commits listing) stores per-origin grants in `browser.storage.local` under `permissions.origins`. The record is `{ networkId, grantedAt }`. The module can `grant`, `revoke`, `isAllowed`, and `listAll`. The stored value has no method list, no watch id, no cursor, and no read-only bit.

That storage does survive service-worker termination, unlike a page global. It survives as an origin allow-record. The product draft, which this lane did not re-verify against the connector TypeScript, says the website adapter calls connection and status methods only, that disconnect clears the page handle, and that the grant itself is origin-wide and includes capabilities beyond those calls. The permissions file is consistent with the origin-wide part: nothing in the grant narrows authority. A disconnected tab cannot resume a watch from this record, and must not treat the record as permission to sign or pay. Reconnect is a new explicit gesture. The watch, if it is to resume, resumes from the local consumer service after a fresh permission check.

The same commit message on the wallet tip is the auto-lock refresh for DApp activity. Status polling is therefore not a free read. It can keep the wallet unlocked. The lifecycle service should poll status on an explicit cadence, not on every journal read.

### UmbraDB and the local stack

Public UmbraDB `main` and `release/1.0.0` are both `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca` (2026-07-26). The commits at that tip are indexer-parallelism research notes. Branch `design/midnight-express-recovery` is `f662822765247f0da553347c9819f958a1992d28` (2026-10-04, message "Resolve verified historical graph secret-scan false positive"). The root listing at that commit is a normal repository tree (`src`, `design`, `docs`, and the rest). This lane did not read a consumer-journal implementation there. The branch name is not evidence of atomic watch cursors.

The product draft's storage plan stands: Umbra/PostgreSQL for the backend composition and SQLite for the standalone tier, with inbox dispositions, cursors, and effect state committed together. The stack-feasibility report's SQLite constraint also stands: one writer, on one host, reached through a local daemon. Browser pages and the wallet extension do not open that file.

### Kafka 4.3.1 design

`apache/kafka` default branch `trunk`, repository `pushed_at` 2026-10-05T17:01:55Z. `releases/latest` returned HTTP 404 (144 bytes, sha256 `3be3b9547eef51cc49a1de5d482554e118735d9b860dd24f5cf1b6eccc3ab69e`). The tags page of eight entries returned ancient `0.7.x` names and is not a version oracle. Matching refs for `tags/4.` include `4.3.1` at `a07059eb9b5bac1bfdbb1e74313f2fae4ca20fd9`, plus `4.3.2-rc0` and `4.4.0-rc3`. The design directory at that tag lists `_index.md`, `design.md`, and `protocol.md`.

`https://github.com/apache/kafka/blob/4.3.1/docs/design/design.md` returned HTTP 200 on both fetches. Extracted text sha256 is `9e525df25017ee5e7a482aecf881f175b2911f75c2c40b90679b34ef5dcf244b` both times. The rendered page header shows ref `4.3.1`, path `docs/design/design.md`, 511 lines, and file commit `b368e39` ("KAFKA-20366"). That short sha is what the page header displays. It is the last change to the file at the pinned ref, not the tag object `a07059eb`.

The Consumer Position section, visible on tile 4 of the successful capture, says each partition is consumed by one member of a group at a time, so the consumed position is a single integer: the offset of the next message. That integer is checkpointed periodically, which is how Kafka makes acknowledgements cheap. A consumer may rewind to an older offset and read the same records again. The same section says marking a message consumed at send time loses it if the consumer crashes, and waiting for an acknowledgement can deliver it twice if the consumer crashes after processing and before the ack.

The Message Delivery Semantics section, visible across tiles 5 and 6, separates publish durability from consumption:

- Save the position, then process: at-most-once. A crash after the save skips unprocessed records.
- Process, then save the position: at-least-once. A crash after processing redelivers. A primary key makes the second application overwrite the same record.
- Exactly-once inside Kafka, since 0.11.0.0, writes the consumer offset and the output records in one producer transaction. On abort the stored offset stays at the old value, and the consumer does not rewind by itself. It has to refetch the committed offset.
- An external destination gets the same property when the offset is stored with the output. Otherwise the default is at-least-once. Producer idempotence, a producer id plus a sequence number, stops duplicate log appends. It does not by itself make an external effect exactly-once.

"Committed" on the publish path means every in-sync replica has the record. "Committed offset" on the consume path means the consumer's stored position. The design document uses both phrases. They are different facts. Tile 9 shows the later replication rule that only committed records are given to consumers, and that Kafka's failure model is fail-recover, not Byzantine.

This confirms the local rule already recommended: a checkpoint saved before the disposition is durable drops work; a checkpoint saved after a side effect without a shared commit can repeat the effect; a single next-offset integer cannot also remember an in-flight lease or an uncertain external effect. Kafka's own remedy for an external system is to store the position with the output. The daemon journal should do that for the disposition and the effect key. Kafka itself stays off the network path, because a partition key or topic that carried a business selector would publish interests.

### Failures that are not evidence

| Capture | Result |
|---|---|
| `https://api.github.com/repos/apache/kafka/releases/latest` | HTTP 404, 144 bytes |
| `https://api.github.com/repos/reactive-streams/reactive-streams-jvm/releases/latest` | HTTP 404, same 144-byte body |
| `https://raw.githubusercontent.com/nats-io/nats.docs/main/SUMMARY.md` | HTTP 404, 14 bytes. `master` succeeded |
| Gossipsub v1.0 body | Not fetched. Only the v1.0 commit tip was listed |
| Umbra `design/midnight-express-recovery` tree | Root names only. No journal semantics read |
| First PixelRAG pass of the Kafka design page | Tile is Chrome `ERR_NETWORK_CHANGED` ("Your connection was interrupted"). Page height 543. Helper still set `verified_capture` true because the process exited 0 and wrote a JPEG. Inspection overrides that flag. Tile sha256 `5fec0f8957ecef54b1d2db9a41b18bef8ed8153e4fb1369605e4deabc4f3def7` |

Redirects that still returned the requested document were accepted only after the final URL and the text were checked. The NATS pull-consumer page stayed on `https://docs.nats.io/learn/jetstream/pull-consumers`.

## Recommendation

Keep one local consumer service as the only component allowed to advance a checkpoint. Give it four durable facts, committed in the same transaction as the disposition they depend on:

- An append-only journal of original sealed envelopes, with a host-wide high-water mark. Intake appends before recognition fan-out. Consumer pause, queue pressure, and wallet lock do not stall that append and do not change Gossipsub timing.
- Per watch, a delivery cursor: the highest journal position handed to that watch's inbox, plus the in-flight set. Handoff is not an acknowledgement.
- Per watch, a processing checkpoint: the contiguous prefix of journal positions whose dispositions are durably recorded. Dispositions include reviewed, quarantined, and outcome-unknown. A hole holds the checkpoint. An explicit quarantine can take its place in the prefix only after that disposition is in the same commit. This is the local analogue of an ack floor, stricter than NATS `AckAll`.
- An occurrence index on `(source, id)` and an effect ledger on `(authorityDomain, executionScope, actionId)`. Close, expiry, unsubscribe, and page reset do not delete these. Replay of the same occurrence does not mint a new effect.

`consumer.commit` acknowledges a local disposition and advances the processing checkpoint only in the same commit as that disposition. Kafka's design page states the two crash orders directly: saving the position first is at-most-once, and processing first is at-least-once. The Midnight Express commit follows the second order for local dispositions, and follows Kafka's external-system remedy for effects: the effect key is stored with the checkpoint. The commit does not assert ledger finality or source authenticity. If `action.prepare` has been recorded and the outcome is uncertain, the disposition is outcome-unknown and the effect key blocks a second execution. If no prepare exists, lease expiry puts the same original back in the eligible set and leaves the checkpoint where it is. A rewind, which Kafka treats as a supported operation, replays the original sealed bytes and hits the same occurrence and effect keys. Do not adopt NATS's 30-second default as the lease. The lease is a local liveness parameter. Business expiry stays inside the sealed payload and the validator, which already refuses an expired trusted context.

Retention that no longer holds an undecided original produces a gap (`retention` or `missing-range`) and stops dispatch. The checkpoint stays. The operator either accepts a new revision whose start is explicit, or recovers from an authorized whole-shard archive and then re-runs local recognition. A NATS `+TERM` of "Unacknowledged message was deleted" is the behavior to avoid copying: deleted unacked data must not look like a successful acknowledgement.

Resume rechecks watch expiry, local permission, and coverage, then reports a gap if the retained range no longer covers the checkpoint's successor. Wallet disconnect clears the page's adapter handle only. The origin grant remains until the wallet's own revoke path deletes it. Reconnect does not restore tab memory and does not authorize signing or payment.

Reactive Streams demand is how the service bounds `watch.read`. NATS durable pull with explicit ack is the conceptual shape of that service. Neither binary is a dependency. Selectors, categories, and cursors stay in the local control plane and off the sealed wire and off any relay subject.

## What the dashboard demonstrates and cannot

Demonstrates, on one page load, with unsigned or offline-fixture data: category navigation that is not a network topic; pause that stops new handoff; resume that refuses when permission or a gap needs attention; a delivery cursor that moves at inbox handoff; a processing cursor that moves only across a contiguous decided prefix; bounded in-flight and queue caps; a full journal that refuses eviction; a retention gap with no silent jump and no fake archive; fixture `(source, id)` suppression without new authority; a second item for an unsigned mock; quarantine text for a rejected offline fixture; a mock permission flag distinct from the wallet; an export labeled synthetic; reset that leaves Moth grants alone.

Cannot demonstrate: survival across reload, a second tab, or a crashed daemon; an atomic commit of cursor plus disposition plus effect key; lease expiry and redelivery; real retention or store repair; cross-principal isolation (persona is a label); wallet disconnect and reconnect as a recovery path; origin-grant revoke; signing or payment; transport, admission, or decryption. An unsigned green path on this page is not production proof. Acceptance still requires the product draft's restart-safe checkpoint exercise, run separately from uncertain external effects.

## Where existing technology suffices

Suffices and should stay:

- Whole-shard encrypted intake, local recognition, and Gossipsub as the dissemination mesh. No consumer ack belongs on that mesh.
- Model v0.2 occurrence identity for the installed quote, invoice-observation, and sandbox-approval profiles, with `executes: false` on accepted validation. Payload expiry and changed authority stay validator failures, distinct from a delivery lease.
- The proposed local operations `watch.create`, `watch.list`, `watch.read`, `watch.pause`, `watch.resume`, `watch.close`, `consumer.commit`, and separately authorized `action.prepare`.
- SQLite as the standalone journal once a single local daemon owns it. Umbra/PostgreSQL remains the backend target when an atomic multi-row capability exists. Neither is replaced by a browser API.
- Moth's current connector, used as an explicit connect-and-status session. Origin persistence in `browser.storage.local` is the right place for that grant and the wrong place for watch cursors.
- The static dashboard as a review of the state vocabulary.

Add:

- The daemon-owned journal and the two cursors plus the two ledgers above, with one transaction covering a disposition and any cursor move.
- An in-flight lease that requeues only when the effect ledger has no prepare record.
- A host-wide journal high-water, separate from each watch's delivery cursor, so "received by the host" and "handed to this inbox" can be shown without overloading `deliveredCursor`. This agrees with the human-experience report's coverage split and stays off the wire.
- A display cache, if a wallet or browser must show already disclosed items while the daemon is unreachable. The cache is marked coverage-unknown. It cannot advance the daemon checkpoint. A review made offline is an intent submitted when the daemon returns, and it loses to a checkpoint the daemon already committed.

Do not add NATS, Kafka, a webhook bus, `localStorage` as the journal, or service-worker globals as the journal.

## Data-model fit and limits

Cursors, gaps, leases, permissions, and connection state fit the local control plane. They do not fit the sealed business envelope. Putting a delivery cursor or an ack into the wire would publish interest and would still not prove an effect.

`(source, id)` fits occurrence suppression for authenticated fixtures. The dashboard already shows the complementary case: mocks have no such identity, so replay creates another row. Production code must not synthesize a mock key and then treat it as deduplication.

The effect key is not an event field. The product draft keeps `action.prepare` as a separate authorization. The journal should store that key beside the watch, not inside a new event profile.

Expired delivery has three different clocks, and the model already has room for only one of them inside a payload:

- Payload or credential expiry is a validation result on the decrypted body. The fixed test clock in the fixtures is this clock. It does not move a cursor.
- Permission or watch expiry stops further handoff. It does not advance the processing checkpoint and does not erase the effect ledger.
- Retention expiry of an undecided original is a gap. It is a storage fact, not a business event.

Contracts, credentials, and operations remain unsigned mocks. Their renewal banners are not a lifecycle profile. Ethereum and Solana observations stay evidence vocabularies. A displayed finality label does not fill in a missing checkpoint.

This lane did not re-run the validator. `wiki-llm/pubsub/data-model-fit.json` and the product draft remain the record that accepted fixtures carry `executes: false`. That result supports "review is not an effect". It does not prove live source authenticity.

## Rejected alternatives

- A NATS or Kafka cluster as the subscription bus. Durable pull and explicit ack are worth copying locally. A broker subject or partition key that carried business selectors would publish interests to operators. The privacy constraint in the product draft forbids that default.
- NATS `AckAll` or a single consumer offset as the only progress field. One number cannot simultaneously mean "handed to the inbox", "disposition recorded", and "effect succeeded". Hole-skipping acknowledgement hides a gap.
- Treating `+TERM` after stream deletion as a successful commit.
- Reactive Streams completion as watch teardown that deletes effect identity.
- Gossipsub's message cache and `IWANT` as the replay log.
- `localStorage`, `sessionStorage`, or extension-worker globals as the authoritative journal. Storage pressure, navigable close, and worker termination are specified loss events. The Chrome document additionally removes Web Storage inside the extension worker.
- Resuming a watch from the Moth origin grant. The grant is `{networkId, grantedAt}` for an origin. It is not read-only, not a cursor, and not a signing session.
- Declaring the in-memory dashboard durable because it shows the word cursor.
- Adopting Umbra branch `design/midnight-express-recovery` as an implemented journal. The pinned commit message is a secret-scan false-positive fix, and the body of that branch was not reviewed here.
- Adopting Kafka as a broker, or adopting its single next-offset integer as the only local progress field. The 4.3.1 design page is useful exactly because it shows what that one integer costs: periodic checkpointing is cheap, and the order of checkpoint versus processing chooses at-most-once or at-least-once. External exactly-once needs the offset stored with the output. Copy that transaction shape locally. Leave the broker, the consumer group, and the partition key out of the private transport.

## Proposed consensus

- The authoritative checkpoint is the contiguous processing cursor in the local daemon journal. Delivery handoff and effect outcome are different fields. None of the three is chain finality.
- `consumer.commit` is the only ack, and it acks a disposition. Uncertain external work is outcome-unknown plus an effect-ledger entry. Subscription recovery tests stay separate from effect recovery tests.
- Pause stops new handoff. It does not roll back in-flight items and it does not stop host intake. Resume rechecks permission and coverage.
- A gap is mandatory when retention or a missing range sits under an undecided cursor. Accepting the gap creates a new revision. It does not rewrite old dispositions.
- Close and expiry keep the occurrence index and the effect ledger.
- Browser and wallet surfaces are clients. They may cache disclosed items as non-authoritative. The website proof of concept remains memory-only and unsigned.
- Moth connection stays a user gesture. Origin grant persistence is not watch recovery and grants no payment or signing authority to the subscription service.
- No new network protocol and no new sealed field for cursors or acks.

## Unresolved objections

- Lease versus a second device. Requeue-when-no-prepare is safe for items that never left the host. A reviewer may want automatic retry after `action.prepare`. Automatic retry can double an external effect whose outcome was only uncertain. The conservative rule is outcome-unknown and a human reconciliation. That will feel slow for payments. It should stay conservative until an effect-specific idempotency contract exists for that profile.
- Offline review inside a wallet extension. A disconnected reviewer can still want to mark an item. If that mark is allowed, it has to be a queued intent. The daemon may already have quarantined the same cursor. The intent must lose. The objection is that a wallet then shows a review that "does not stick". The status line has to say the daemon checkpoint won.
- Whether pause freezes processing as well as handoff. The page allows a disposition of an already in-flight item while paused. The product sentence "pause stops consumer delivery" supports that. A user who reads pause as "hold everything" will be surprised. Copy can say that already handed items remain reviewable. The checkpoint rule should not change.
- Journal high-water naming. Adding `journalHighWater` beside `deliveredCursor` and `processedCursor` is a local schema change. The human-experience report asked for a received-through mark. This report agrees with the distinction and objects to overloading the delivery cursor to get it. The wire stays unchanged. If the contract draft wants one fewer field, the high-water can live only on the host journal, not on every watch record.
- Umbra capability timing. Backend atomicity is still a plan. Shipping the SQLite daemon journal does not wait on the recovery branch. Claiming Umbra already commits watch state would over-read a branch name.
- Gossipsub v1.0 cache size and retention remain unread. The v1.1 text only shows that an `IWANT` can be answered from a cache and that those answers are limited. That is enough to refuse the cache as a consumer journal. It is not a parameter recommendation.
- In-flight work during a Moth auto-lock. A status refresh can extend unlock. A journal sync must not. If the wallet locks mid-review, in-flight items stay leased until the lease ends, then follow the no-prepare requeue rule. No hidden sign request.

## Source URLs

Primary pages and objects this lane retrieved:

- https://docs.nats.io/learn/jetstream/pull-consumers
- https://github.com/nats-io/nats-server/releases/tag/v2.15.0
- https://raw.githubusercontent.com/nats-io/nats-server/v2.15.0/server/consumer.go
- https://raw.githubusercontent.com/nats-io/nats-server/v2.15.0/server/jetstream.go
- https://raw.githubusercontent.com/reactive-streams/reactive-streams-jvm/v1.0.4/README.md
- https://raw.githubusercontent.com/libp2p/specs/98c5aa9421703fc31b0833ad8860a55db15be063/pubsub/gossipsub/gossipsub-v1.1.md
- https://storage.spec.whatwg.org/
- https://html.spec.whatwg.org/multipage/webstorage.html
- https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle
- https://raw.githubusercontent.com/shieldedtech/moth-wallet/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/permissions.ts
- https://api.github.com/repos/CharlesHoskinson/UmbraDB/branches?per_page=30
- https://api.github.com/repos/apache/kafka/contents/docs/design?ref=4.3.1
- https://github.com/apache/kafka/blob/4.3.1/docs/design/design.md

Hashes, byte lengths, and retrieval times are in the sibling `../sources/grok-recovery-lifecycle/*.json` files. Text worth citing is in the matching `.txt` files. Raw response bytes are in the `.raw` files.

Cross-checked local documents, not re-fetched as external primaries: `docs/product-requirements/pubsub-subscription-experience.md`, `wiki-llm/pubsub/subscription-contracts.md`, `website/dist/subscriptions.js`, `wiki-llm/pubsub/agents/opus-stack-feasibility.md`, `wiki-llm/pubsub/agents/opus-human-experience.md`, `wiki-llm/pubsub/agents/sol-subscription-contracts.md`.

## Visual grounding

The first-pass corpus had `visual_tool` null on every file. The page chosen for PixelRAG was the Kafka 4.3.1 design document, because the lifecycle comparison needed its offset and delivery text and the first pass had only a directory listing.

PixelRAG pixelshot 0.4.0, CDP backend, tile height 1568. First attempt (`kafka-design-431-tiles`, 2026-10-05T18:28:13Z) wrote one tile, page height 543, process exit 0. The helper recorded `verified_capture: true`. The tile itself is Chrome's error page: "Your connection was interrupted", "A network change was detected.", `ERR_NETWORK_CHANGED`, and a Reload button. Tile sha256 `5fec0f8957ecef54b1d2db9a41b18bef8ed8153e4fb1369605e4deabc4f3def7`. That image is not the design document. The Scrapling text fetch on the same call did return HTTP 200, and its text hash matches the later good fetch, so the prose was available even though the screenshot was not.

Second attempt (`kafka-design-431-view-tiles`, captured in about 6.8s, page height 24614, 16 tiles, `tiles.json` `complete: true`) rendered the GitHub file view. Inspected tiles:

- `tile_0000.jpg`, sha256 `6a7b4197c9d777ec7a6bad59fc3b6f6f0a22d77d8ee94a9efd76b8bf3eba9d77`. Public `apache/kafka`, ref `4.3.1`, path `kafka / docs / design / design.md`, Preview tab, 511 lines, 74.6 KB, file commit `b368e39`. The visible opening is the Motivation section and the start of Persistence. This is the design document, not a redirect or an error page.
- `tile_0004.jpg`, sha256 `c364289977819c7544b1cf6175db96899e512d48856e1a4e3e911ff5e03ff1fa`. Heading "Consumer Position". Visible prose: the consumed position is a single integer, the offset of the next message, one number per partition, periodically checkpointed; a consumer can rewind and re-consume; an acknowledgement that arrives after processing can still mean the message is consumed twice if the process dies before the ack.
- `tile_0005.jpg`, sha256 `6a6f0dc05d2b682db9efd65e7e3cd92674f6c09101429419a29559248da5a328`. Heading "Message Delivery Semantics", with at-most-once, at-least-once, and exactly-once defined, and the producer idempotence option since 0.11.0.0 (producer id and sequence number).
- `tile_0006.jpg`, sha256 `1f69838287d68f8089cda6b65412ae9f9512da5b28286b63b1786cf34690a968`. The two consumer crash orders, transactional offset-plus-output exactly-once, the note that an aborted transaction does not auto-rewind the consumer, and the external-system requirement to store the offset with the output. Default remains at-least-once.
- `tile_0009.jpg`, sha256 `04f76f6132ea49c87bf327c3be844fe6a2bfc870f4e7aaf14f031a53279172c4`. Later replication section: only committed messages are given to consumers; fail-recover rather than Byzantine faults. Included to confirm the capture continued past the semantics section. Not used as a subscription-lifecycle requirement.

Tiles 1–3, 7–8, and 10–15 were not inspected. Claims about consumer position and delivery semantics are limited to the inspected tiles plus the matching text extract. No GPU index was built. The helper's `verified_capture` flag is not treated as proof; the tile images were read.
