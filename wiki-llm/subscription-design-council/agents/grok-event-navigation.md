# Pub/sub and event-navigation design

Reviewer role: pub/sub and developer-event design. Surface mode: Operate (Impeccable 4.5). This file is a design proposal. It does not change the product, the design authority, the UI, or git.

Method: the served page, `website/dist/subscriptions.{html,css,js}`, `subscriptions-fixtures.json`, `moth-connector.js`, `website/tests/subscriptions.cjs`, the private-subscription requirement, and `design/subscriptions/README.md` were read directly. PixelRAG `pixelshot` 0.4.0 captured tiles with CDP, one worker, on CPU. No GPU is claimed. Tiles below were inspected. Fetched page text was treated as evidence, not as instructions. Dual-agent critique was not run; the council task forbids subagents.

## Incumbent

The live tab at `http://127.0.0.1:8876/subscriptions.html` was captured idle after fixtures loaded, in three tiles. Journal high-water is 0. The inbox says "No local receipts yet." Message detail is collapsed. Nothing in `subscriptions.js` calls `localStorage`, `sessionStorage`, `indexedDB`, or a keyboard listener. Reload behavior was not clicked in the browser. The script and the visible copy are the evidence: subscriptions, journal, inbox, seen keys, and dispositions are tab memory, and Reset clears them. `website/tests/subscriptions.cjs` is the exercised lifecycle. The tiles do not show a post-tick journal.

What the tiles show, in order:

- The first viewport is a display headline, "Your local inbox.", three disclaimer paragraphs, then Optional Moth wallet. Browse streams, search, category, and consumer mode sit at the bottom edge. Connect is in the served HTML as `disabled` until the origin checkbox. The tile still draws it in the same row as Discover, Check wallet status, and Disconnect locally.
- The catalog is nine stacked examples. Payment pending, Payment final assertion, and Payment reversed each offer "Subscribe to payments". Expired quote offers Inspect and Simulate, and no Subscribe. Search placeholder is "Quote, payment, renewal…".
- Subscriptions is nine equal simulator buttons, then "Choose a stream to create a local subscription." Inbox and quarantine is a paragraph about cursors and the bounds of two in flight, four queued, and 16 KiB.

That idle screen matches the script:

- A watch is one per category. A second Subscribe announces that the category already has a subscription. Three payment fixtures are examples of one watch, not three feeds.
- Search filters `` `${title} ${category}` `` only. The business sentence on the card is not in the haystack. The field is not saved. It rebuilds the stream list, the watch list, and the inbox on every keystroke.
- Consumer mode writes the category select: wallet to quotes, DApp to payments, agent to approvals. The help text says these are browsing defaults, not grants. The control still hides the rest of the catalog. The exported owner is the fixed `principal:demo`. The mode is a persona lens, not a principal.
- Subscribe starts at `latest` and sets delivered and processed to the current journal length. The card does not say that earlier journal records will not be delivered.
- Intake appends the journal first, then offers the original to active or paused watches whose category matches. A payment-final predicate also requires an accepted offline check and status Final. Unmatched records stay in the journal. Selectors do not run on a network.
- Pause sets `requestedState` and stops `dispatch`. Enqueue still runs. The test pauses contracts, ticks five times, and expects `gapped` with delivered cursor 0. Queue credit, not retention, created that gap. Resume is what allows delivery.
- Both gap reasons render one paragraph and both buttons, Recover retained originals and Accept gap. Retention recover always announces that the range is unavailable. Accept gap sets `requestedState` to `active`, so a paused watch would be unpaused. The test accepts a gap only after resume, so it does not catch that.
- Scope edit is refused while permission is expired or revoked, while the watch is gapped, or while queue or in-flight work remains. Unsubscribe writes a tombstone, clears that watch's queue and in-flight list, and leaves disclosed inbox rows.
- "Mark next item reviewed" takes the first watch with in-flight work, not the opened row. It rewrites only dispositions that start with "awaiting". A quarantined or duplicate row stays worded as it is, and still counts as decided so the contiguous processing cursor can pass. The button label still says reviewed.
- Inbox renders `inbox.slice(-40).reverse()`. Older receipts disappear with no count. The row button calls `detail(record)`, so the pane is the fixture JSON. Disposition, cursor, revision, replay, and subscription id are not in that object.
- Quarantine of the rejected quote uses `offlineCheck.reason` and does not set the occurrence seen-key. The test then delivers the accepted quote with the same source and id as awaiting review. That gate is real and easy to miss, because the inbox is one mixed list.
- Journal cap 64 stops intake and does not evict. Bounds are two in flight, four queued, 16 KiB. Backpressure sets `reason: "missing-range"` while saying originals remain from cursor 1.
- Profiles on the nine records: `rfq.v0.2`, `invoice.v0.2`, and `agent.v0.2` are offline reference fixtures, including one rejected quote. Contracts, credentials, and ops are `unsigned-mock` / `not-model-validated` with null event, context, and wire. The page does not run a browser validator.
- Moth, API 4.0.1, network preprod: Discover does not connect. Connect runs only from a click with `userActivation`, and only `connect` plus `getConnectionStatus`. Check wallet status is a second click. There is no poll. Local disconnect clears the adapter handle. The status line says it cannot revoke the origin grant. The test asserts load and simulation do not call the wallet.

Operate failures that matter: the task is buried under a marketing `clamp()` headline and a wallet panel; nine simulator buttons are the control system; feed, category, and watch are the same row; read, delivery, processing, and effect are not separately visible. The explanatory copy is the strongest part of the page. It already says the right boundaries, in the wrong place, at the wrong length.

Heuristic reading of this idle tool, scored 0–4: visibility 2, real-world match 2, user control 2, consistency 2, error prevention 2, recognition 2, flexibility 1, minimal design 2, error recovery 2, help 3. Total 20/40, acceptable only as a protocol demo. Extraneous load is high: wallet, catalog, simulator, and inbox compete, and the decision point under Subscriptions shows more than four actions.

## Sources inspected

| Source | Provenance | What was inspected |
|---|---|---|
| Incumbent page | Scrapling 200, 2026-10-05T20:20:10Z, raw sha256 `3eb81bf4…1d5e79`. PixelRAG CDP, 3 tiles, verified. | Idle loaded tab, top through inbox. Not a clicked lifecycle. |
| NATS JetStream pull consumers | Requested `docs.nats.io/nats-concepts/jetstream/consumers`. Final URL `https://docs.nats.io/learn/jetstream/pull-consumers`, 200, 2026-10-05T20:21:56Z, raw sha256 `63c5c9d3…b82d7fda`. | Text. Fetch versus consume, explicit ack, bounded batch. No server version on the page. |
| NATS pausing a consumer | `https://docs.nats.io/learn/jetstream/pausing`, 200, text 2026-10-05T20:23:19Z and visual recapture 2026-10-05T20:25:27Z, raw sha256 `7c60d122…ee8bbbe`. One CDP tile sha256 `a8bf7f4c…1470f8a`. | Tile shows the article through "Pause until a deadline" and the CLI sample. Later sections were read as text. |
| NATS filtering | `https://docs.nats.io/learn/jetstream/filtering`, 200, 2026-10-05T20:23:19Z, raw sha256 `2dddcbfd…403021082`. | Text. Filter lives on the consumer. A typo filter is silent. |
| NATS delivery and acknowledgment | `https://docs.nats.io/learn/jetstream/delivery-and-acknowledgment`, 200, 2026-10-05T20:23:19Z, raw sha256 `1326ff99…31f666a3e`. | Text. Explicit ack, at-least-once, redelivery when there is no ack. |
| CloudEvents 1.0.2 | `https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/spec.md`, 200, 2026-10-05T20:21:56Z, raw sha256 `e327435c…d16a1aa3`. Heading: CloudEvents - Version 1.0.2. | Required `id` and `source`, optional `subject` and `dataschema`, privacy section. No separate release-date page fetched. |
| AsyncAPI 3.1.0 | GitHub release API `v3.1.0`, `published_at` 2026-01-31T11:24:10Z. Spec `https://raw.githubusercontent.com/asyncapi/spec/v3.1.0/spec/asyncapi.md`, 200, 2026-10-05T20:23:19Z, raw sha256 `983a9c0c…0cd91869`. | Channel address versus operation `send`/`receive`. |
| Apache Kafka 4.3 design | `https://kafka.apache.org/43/design/design/`, 200, 2026-10-05T20:27:25Z, raw sha256 `bcca1c2a…72531ef4`. Version 4.3 is the newest entry on the documentation nav fetched just before. | "The Consumer", consumer position, delivery semantics. This page does not document a pause API. |
| Confluent Control Center consumers | Requested the platform Control Center consumers URL. Final `https://docs.confluent.io/control-center/current/clients/consumers.html`, 200, 2026-10-05T20:26:24Z, raw sha256 `155a2126…3e3a5589`. Page says last published Jan 26, 2026. One CDP tile sha256 `81bde631…af0fd8e`. | Documentation page, not the product UI. Sidebar shows Control Center 2.6 (current), Consumer Groups, and a separate Reset Offsets item. Body describes group id, status, protocol, lag, truncation, and `currentOffset` placeholder `-999`. A chat control overlaps that paragraph in the tile. |

`docs.nats.io/robots.txt` returned 404, so no robots policy was published. Four JetStream learn pages were fetched after that. No second page was fetched from kafka.apache.org except the documentation redirect and the 4.3 design page. No second Confluent page.

Rejected fetches: AsyncAPI docs path `/docs/concepts/asyncapi-document/channels` is 404. Kafka ` /41/getting-started/consuming/` is 404. `api.github.com/repos/apache/kafka/releases/latest` is 404; the project version list was taken from the documentation site instead. None of these were used as design evidence.

## Terms

Use these words in the interface. Do not rotate them for variety.

| Term | Meaning on this product | Where it must not appear |
|---|---|---|
| Authorized private shard | The whole shard the host already holds after intake. | A channel, topic, subject, or route. |
| Journal high-water | How far local intake has stored originals. | A delivery or processing position. |
| Feed | One directory identity: id, title, summary, scenario family, evidence class. | A watch, a wire acceptance, or a broker address. |
| Category | Browse facet: quotes, payments, approvals, contracts, credentials, ops. | The watch id, and any network subject. |
| Local watch | Durable consumer for one principal, revision, local selector, start, and bounds. | A remote consumer group or an AsyncAPI channel address. |
| Timeline | Journal order for that watch, including not-yet-delivered and skips. | The inbox. |
| Inbox | Items that crossed the delivery cursor into the local sink. | The whole shard. |
| Delivery cursor | Received into the inbox. In flight counts toward the bound of two. | Reviewed, final, or executed. |
| Processing cursor | Contiguous decided dispositions, including quarantine. | An effect receipt or ledger finality. |
| Read / unread | This browser has opened the delivered item. | A disposition or a cursor. |
| Folder | Named set of feed ids on this browser. | A selector or a shard. |
| Paused | Requested stop of delivery. Cursor and decisions stay. | A gap, a tombstone, or an expired grant. |
| Gap | The watch cannot silently skip a missing range. | An empty predicate result. |
| Quarantine | Decided, not actionable, still visible. | Deletion, or "reviewed". |
| Persona | Human, wallet, DApp, or agent copy lens. | The principal. |
| Effect | A later action contract. Out of this screen. | Any label on delivery or review. |

CloudEvents 1.0.2 requires `source` + `id` to identify one occurrence, and says consumers may treat the same pair as a duplicate. The fixtures already use that pair. The same section says `type` is often used for routing, and `subject` exists so middleware that cannot read `data` can filter. The privacy section says intermediaries may log context attributes, and that sensitive information should not be carried there. A category, feed id, or selector published as `type`, `subject`, or an AsyncAPI channel address would be that leak. AsyncAPI 3.1.0 defines a channel address as the topic name, routing key, event type, or path, and defines an operation as `send` or `receive` on a channel reference. Those are two objects. Midnight's feed title may be as human as a channel title. The address must stay unknown to every relay.

Kafka 4.3's consumer chapter is pull: the consumer names an offset and receives a bounded chunk. Saving that position before processing is at-most-once. Processing and then saving is at-least-once. The same chapter uses "committed" for a replicated log record and, later, for the consumer position, and it calls that second use confusing. This screen should not say committed at all.

NATS documents the split this product already wants. The stream keeps every matching subject. The filter lives on the consumer. Pull fetch is a bounded batch with explicit ack. Pause stops delivery to that consumer. The cursor does not move, acks stay acks, and the stream keeps accepting publishes. Deleting the consumer is the act that throws the cursor away. A filter that matches nothing is accepted and then silent. The page says an empty pull is not an empty stream.

Control Center 2.6's consumers doc is an operator list: search a group id, then open lag, members, topics, and partitions. Reset offsets is a different nav item from the list. When the offset is not available it shows `-999` rather than a guessed number, and it says large lists are truncated. That is the delivery disclosure, not the home page. The floating Ask control over the offset paragraph is the pattern to avoid.

## Recommended pattern

Directory first. Reader second. Delivery is a strip on the open watch. One information architecture at every width. Desktop shows the reader beside the directory once a feed is open. Mobile replaces the directory with the reader, then with the detail. The wallet block and the nine simulator buttons stay in the page, with the same ids and the same Moth rules, after the directory in document order.

### Directory

Each row is one feed id.

Installable feeds are the current distinct examples, not the category:

- `feed:rfq-shares-usd` — Shares / USD quote — `rfq.v0.2` — offline reference
- `feed:invoice-pending` — Payment pending — `invoice.v0.2`
- `feed:invoice-final` — Payment final assertion — `invoice.v0.2`
- `feed:invoice-reversed` — Payment reversed — `invoice.v0.2`
- `feed:agent-writereport` — WriteReport approval candidate — `agent.v0.2`
- `feed:contract-renewal`, `feed:credential-expiry`, `feed:ops-backlog` — unsigned mock, `mock.local.v1` / `mock-only`
- `feed:rfq-rejected` — inspect and simulate only; no Follow, matching today's missing Subscribe

A local watch is installed per feed id, not per category. Payment pending and Payment final are two watches. The payment-final predicate remains a selector on a payments watch, not a second copy of the category. The closed intent schema has no feed id today. Until it grows a local-only field, the demo export keeps today's category intent for the watches the simulator can run, and synthetic follows stay in the preference document. They are not written into `intents` as fake categories.

Hundreds of further rows are declared scenario views: unique `feedId`, family (`rfq.v0.2`, `invoice.v0.2`, `agent.v0.2`, or `mock.local.v1`), title, and one summary sentence. They do not copy canonical JSON and they cannot be ingested. Follow on those rows is enabled as a distinct empty watch preference. The reader says no sealed record has matched this feed id. A canonical tick must not fan out to every row in the family. That would make them aliases of one category, which the requirement forbids.

Facets are category, evidence class (offline reference, rejected reference, unsigned mock, scenario view), and folder. Consumer mode highlights a suggested feed and changes the help sentence. It does not write the category facet and it does not change the principal.

### Reader: timeline and inbox

A segmented control on the open feed:

- Timeline. Journal order for originals this watch's selector matches, plus explicit skip rows and gap markers. The journal high-water sits in the delivery strip, with the sentence that an authorized shard reader still sees unmatched records.
- Inbox. Delivered rows only. Default filter is undecided. Other filters: unread, quarantine, duplicate, decided. The list states "showing 40 of N" when it windows. It does not drop older rows silently.

Opening a row reveals, in order: the business sentence; read state and disposition; occurrence `source` and `id`, type, time, profile, contract, evidence class; the offline check, including `executes: false` when present; then a closed disclosure for context and sealed wire. Unsigned mocks say there is no occurrence identity, so replay creates another mock item. The raw object is the last disclosure and includes the delivery envelope: subscription id, revision, cursor, disposition, replay.

"Mark read" is opening the row. "Record as reviewed" is a separate button, enabled only when the disposition starts with "awaiting" and local permission is granted. It does not say the effect ran.

A payment-final watch shows non-final timeline rows as "Skipped by local predicate payment-final." They are not inbox items and they do not move the delivery cursor. Silence here is the NATS typo-filter failure.

### Delivery strip

One status line, then four numbers: journal high-water, scheduled, delivered, processed. Then the bounds in flight, queued, and bytes. Unknown numbers stay blank with "not loaded". They are never shown as 0 unless the journal is actually empty.

Actions, each disabled with a reason:

- Pause delivery / Resume delivery. Resume rechecks the mock permission. There is no deadline that resumes by itself. NATS can resume at a deadline; this product must not, because resume has to recheck permission and an unattended resume would look like a grant.
- Unsubscribe. Tombstone. Disclosed rows remain.
- Save scope revision. Disabled while gapped, while expired or revoked, and while queue or in-flight work remains.
- Recover retained originals. Present only for `missing-range`, where the journal still holds the bytes. Bounded by the same credits. Does not change revision. If `requestedState` is paused, recover refills the local queue and does not dispatch.
- Accept new start. Present for `retention`. Disabled until queue and in-flight are decided. Creates the next revision and an `after` cursor. Leaves `requestedState` as it was. A paused watch stays paused.

Pause matches the NATS page: intake continues, the delivery cursor stays, decided work stays decided, and pause does not spend queue credit. The current "pause, then tick, then gap" behavior is a demo defect relative to that rule. A full queue on an active watch remains a `missing-range` gap with recovery, and the copy says the originals are still retained. Retention is the only gap that offers a new start, and the copy says no authorized archive exists in this demo.

Quarantine stays a decided disposition. It can advance the processing cursor. It stays listed. It does not set the occurrence seen-key. The reviewed action does not rewrite it.

Expired and revoked still block intake, dispatch, processing, pause, resume, and scope edit. Already disclosed rows stay readable. Reset is the demo's way back, and the announcement keeps saying Moth's origin grant is untouched.

Demo controls move into a closed disclosure after the directory, same button ids, so the existing harness can click them. The disclosure summary is "Demo controls. These simulate intake. They are not a live bus."

### Rejected alternative

Publish each category or feed as a Kafka topic or a NATS subject, and join a remote consumer group whose filter is the user's interest. AsyncAPI would record that as the channel address. CloudEvents would put the interest in context attributes that intermediaries may log. Control Center would then be the natural home screen, because the broker would know the group. The requirement forbids that route. The useful parts of those systems are the local ones: pull, explicit position, pause without deleting the consumer, and a visible unknown when a number is missing.

Also rejected: one inbox where mark-read saves the consumer position. Kafka's own chapter treats that order as at-most-once and as a different act from processing.

## Wireframe

Desktop is a directory with an optional reader. Below 40rem the reader replaces the directory. The snippet is a mock, not an edit.

```html
<!-- Directory is the default. Wallet and demo controls stay later in DOM order. -->
<main>
  <header class="product-title">
    <p>Browser-local simulation</p>
    <h1>Subscriptions</h1>
    <p>Search feeds, follow one, then read what was delivered. Reviewing an item does not run an effect.</p>
  </header>

  <section aria-label="Feed directory">
    <form role="search">
      <label>Search feeds <input type="search" placeholder="Title, feed, or profile"></label>
      <label>Category <select><option>All categories</option></select></label>
      <label>Evidence <select><option>All evidence</option></select></label>
      <label>Folder <select><option>All feeds</option><option>Local watches</option></select></label>
    </form>
    <p id="dir-status">Showing 20 of 400 feeds. Saved on this browser. This does not restore a watch.</p>
    <!-- row: name, evidence, follow state. One subscribe control per feed id. -->
    <div role="listbox" aria-label="Feeds" aria-activedescendant="feed-invoice-final">
      <div role="option" id="feed-invoice-final">
        <h2>Payment final assertion</h2>
        <p>Historical offline payment assertion. Source status is not settlement.</p>
        <p>invoice.v0.2 · offline reference · feed:invoice-final</p>
        <p>Local watch active · unread 0</p>
        <button type="button">Open</button>
      </div>
    </div>
  </section>

  <section aria-label="Reader" hidden>
    <p>Payment final assertion · local watch · principal is not the persona</p>
    <div role="tablist">
      <button type="button" role="tab" aria-selected="true">Timeline</button>
      <button type="button" role="tab">Inbox</button>
    </div>
    <!-- Timeline rows include skips. Inbox rows are delivered only. -->
    <article>
      <h2>250.00 USD against 500.00 USD payable</h2>
      <p>Unread. Awaiting review: offline reference only. Delivered cursor 3. Processing cursor 2.</p>
      <button type="button">Record as reviewed</button>
      <details><summary>Occurrence and offline check</summary>
        <p>source urn:mpe:source:bank · id event:invoice-final · executes false</p>
      </details>
      <details><summary>Original record</summary><pre>sealed fixture, opened only here</pre></details>
    </article>
    <aside aria-label="Delivery">
      <p>Active. Journal high-water 3. Scheduled 3. Delivered 3. Processed 2.</p>
      <p>In flight 1/2 · queue 0/4 · 0/16384 bytes.</p>
      <button type="button">Pause delivery</button>
      <!-- Recover only for missing-range. Accept new start only for retention. -->
    </aside>
  </section>
</main>
<style>
  @media (max-width: 40rem) {
    /* Reader becomes the page. Decision buttons sit at the end of the article, in the thumb zone. */
    section[aria-label="Reader"] { display: block; }
    section[aria-label="Feed directory"] { display: none; }
  }
  @media (pointer: coarse) {
    button, [role="option"] { min-height: 44px; }
  }
</style>
```

Mobile keeps search, one feed list, and a status line. Opening a feed hides the directory. Timeline and Inbox stay the same two tabs. Delivery collapses to the status line and a disclosure. The origin warning and the Moth checkbox remain above Connect, in the wallet section after the directory, not inside a new connect flow.

## State contract

Two stores. Mixing them is the defect to design out.

Browser view preference, may survive reload, never authority:

- directory query, category facet, evidence facet, open folder
- folder id, name, and feed ids; a feed may be in several folders
- read marks: feed id + occurrence key (`source`,`id`) or, for unsigned mocks, feed id + journal cursor, plus `readAt`
- collapsed disclosures and the last open feed id
- `wantsWatch` feed ids for scenario views the closed schema cannot install

On load, if this document exists, restore those fields and show: "Saved on this browser. This does not restore a watch, a wallet grant, or a cursor." Do not put the query, folder, or feed id in the URL. A shared link on the public Pages origin would publish the interest. Clearing site data clears preferences only.

Tab simulation, cleared on reload and on Reset:

- journal originals and high-water
- installed watches, revisions, requested state, runtime state, cursors, gaps, queue, in flight
- inbox envelopes and dispositions
- mock permission: granted, expired, revoked
- seen-keys and decided-keys

Moth's origin grant is in the wallet, not in either store. Disconnect and Reset do not revoke it. Preferences must not call `connect` or `getConnectionStatus`.

| Reload or action | Directory search and folders | Read marks | Watches, cursors, inbox | Permission and wallet |
|---|---|---|---|---|
| Reload | Restored as preference | Restored as preference | Gone. Empty journal. | Mock permission back to granted only because the script restarts. Wallet unchanged until a click. |
| Reset demo | Cleared with the form | Cleared | Cleared | Mock permission granted. Moth grant unchanged. |
| Change search or folder | Updated preference | Unchanged | Unchanged | Unchanged |
| Open an inbox row | Unchanged | That row read | Delivery and processing cursors unchanged | Unchanged |
| Record as reviewed | Unchanged | Unchanged | Processing cursor may advance contiguously | Requires granted |
| Pause | Unchanged | Unchanged | `requestedState` paused. Delivered cursor unchanged. No new queue credit consumed. | Resume rechecks permission |
| Retention gap accept | Unchanged | Unchanged | New revision, `after` cursor. `requestedState` unchanged. | Requires granted, and no queued work |
| Expired or revoked | Unchanged | Unchanged | Runtime state follows permission. Disclosed rows remain. | Blocks intake, delivery, processing, scope, pause |

Dispositions, kept as the current strings so the gates stay testable:

- `awaiting review: offline reference only`
- `awaiting local processing`
- `quarantined: ` plus the offline reason
- `duplicate suppressed`
- `reviewed locally; no effect executed`

Runtime state remains `active`, `paused`, `gapped`, `expired`, `revoked`, `unsubscribed`. Requested state remains `active`, `paused`, `unsubscribed`. Expired, revoked, and gapped are outcomes. Gap reason is `missing-range` or `retention`. Start remains `latest` with an empty cursor, or `after` with an exclusive cursor on this journal.

## Acceptance

Scale

- A harness can render 400 scenario-view rows plus the installable feeds. Row data is id, title, family, evidence class, and summary. Canonical fixture JSON is parsed only for the nine records.
- The directory paints a window of about 20 rows. Off-screen rows are not laid out (`content-visibility` or a window). Search does not call `replaceChildren` on the watch list or the inbox.
- Filtering 400 precomputed haystacks finishes as a task under 200 ms on the main thread. This review did not measure the current page.
- A scenario view cannot be exported as an accepted receipt. Tick does not deliver it a canonical sibling's event.
- Inbox copy includes the total when the visible window is shorter than the list.
- Opening "Original record" is the first time that row's sealed JSON is stringified.
- A missing cursor renders as "not loaded", never as a sentinel number.

Keyboard

- The directory and each reader list are one tab stop with arrow keys, Home, and End. Enter opens. Escape closes detail, then the reader.
- `/` focuses directory search when focus is not in a field. The field supports Escape to clear.
- `r` records reviewed only for an awaiting row with permission granted. It does nothing on quarantine, duplicate, or mock-only rows that are already decided.
- `p` pauses or resumes the open watch when the existing permission rules allow.
- No shortcut is active while typing in search or a folder name.
- Every button keeps a visible `:focus-visible` ring. The existing mint outline on buttons is the start.
- Demo controls are not before the directory in tab order.

Pointer, width, and performance

- At 320 px and at 390 px, with root font size 200%, `scrollWidth <= innerWidth` for the page. The existing test uses 390 px; keep that and add 320.
- Coarse pointer: buttons and list options at least 44 px, with a gap that prevents adjacent mistakes.
- Hover reveals nothing that the row does not already show.
- The directory does not move when the fixture file returns. A failed fixture load keeps the current announcement and an empty directory that says the file is unavailable.
- Wallet RPC count on load, search, follow, review, pause, and reload stays at zero unless the user clicks Connect or Check wallet status.

## Product sentences

Directory empty of watches: "No local watches yet. Follow a feed to install a watch on this device. Following sends nothing to the network."

Scenario view: "Harbor quote 18 is a scenario view of the quote family. It has no sealed wire. A watch here stays empty until a record is addressed to this feed."

Latest start: "This watch starts at the current journal end. Earlier local records stay in the journal and are not delivered."

Paused: "Paused. Delivery is stopped. The journal can still take records. 0 queued for this watch. Resume checks permission before anything is delivered."

Queue gap: "This watch stopped at cursor 000004 because the local queue was full. The records are still in the journal from cursor 000001. Deliver the retained originals. A new start is not offered while they are still here."

Retention: "The journal no longer has the range this watch asked for. No authorized archive is in this demo. Decide the items already delivered, then accept a new start if you want one. Accepting does not resume a paused watch."

Skipped predicate: "Payment pending was stored in the journal and skipped by the local predicate Final assertions only. It was not delivered."

Read versus review: "Marked read. Still awaiting your decision. Recording a review does not settle the payment or call a tool."

Quarantine: "Quarantined: the offline check rejected this quote. It stays in the quarantine list. It does not block a later accepted event with the same source and id. Nothing was executed."

Duplicate: "This source and id were already seen for this watch. The repeat was suppressed. No new authority was created."

Unsigned replay: "This reminder has no authenticated occurrence id. Replaying it creates another mock item."

Permission: "Local permission is revoked. New intake, delivery, and review are blocked. Items already shown stay on this device."

Preference: "Folder Finance is saved on this browser. It does not follow a feed and it does not restore a wallet grant."

Wallet, unchanged in meaning: "Disconnected. Local disconnect cannot revoke the origin grant. Connect is a separate click and is not permission to subscribe."

## Consensus recommendations

- Make the feed directory the first task. Keep the truthful simulation copy, shortened to one lead sentence, with the shard and wallet limits in disclosures beside the controls they govern.
- Give every installable example its own feed id and its own local watch. Stop offering "Subscribe to payments" on three cards.
- Ship the reader as Timeline plus Inbox. Put the delivery cursors, bounds, pause, recover, and accept-start on that watch's strip.
- Keep read marks, folders, and search in a browser preference that is labeled non-authoritative and is omitted from the URL and from the mock intent export.
- Keep the processing cursor for contiguous decided work only. Quarantine counts as decided. Review does not. Neither is an effect.
- Split gap recovery from gap acceptance, and do not let acceptance clear pause.
- Make pause stop delivery without consuming queue credit or moving the cursor. Keep intake independent of match.
- Show predicate skips on the timeline so an empty inbox is not read as an empty journal.
- Render hundreds of feeds as declared scenario views with distinct ids and no copied wire. Do not let a canonical event match every sibling.
- Leave Moth at Discover, Connect, Check wallet status, and Disconnect locally. Connect stays behind the origin checkbox and a genuine click. Add no signing and no polling.
- Keep the simulator buttons for the harness, off the primary tab order, in a demo disclosure.
- Do not adopt a broker-side channel, subject, or consumer group for business interest.

## Dissent and unresolved

Pause versus the current test. The NATS pause page supports freezing delivery and keeping the cursor. The subscriptions test expects five ticks on a paused watch to produce a gap with delivered cursor 0. The proposal follows NATS, and treats a full queue as `missing-range` only while the watch is actively pulling. If the council keeps the demo's queue-credit gap, the copy must say "local queue full" and must not offer "accept a new start" while cursor 1 is still retained.

Feed id versus the closed schema. The requirement asks for distinct selectable feeds, and the current intent schema is category, profile, contract, source, and predicate. This proposal stores synthetic follows as preferences and does not overload category. The unresolved implementation choice is when to add a local-only `feedId` to that schema. It must not become a relay field either way.

Automatic resume. NATS pause ends at a deadline without a second command. This proposal requires an explicit Resume because permission has to be rechecked. A deadline is unresolved only if a later local service can recheck at that moment and surface a failure. It should not be the demo.

Read marks across reloads. This proposal restores them as preference. A stricter reading of "the demo clears on reload" would clear them too. They are not cursors. The council can drop them without touching the gate design.

Persona facet. This proposal stops consumer mode from writing the category select. The requirement's four journeys remain as suggested feeds and help text. If a reviewer wants the select to keep jumping, the previous facet has to be restorable in one step, and the control has to keep the words "not a grant".

Cross-device folders and a durable journal are out of this demo. The preference document is not that journal.
