# Privacy and trust review: local catalog, separate grants

Independent privacy and trust review for the subscription design council. This file is a design proposal. It does not change the product, the design authority, the site, or git.

Impeccable 4.5 Operate, clarify, adapt, and optimize were applied as constraints. The critique command was not run. The page is an Operate surface: the visitor is here to find a workflow and keep a local watch, so the interface should be familiar, dense where the catalog needs it, and quiet everywhere else.

## Incumbent, as inspected

Live page `http://127.0.0.1:8876/subscriptions.html` returned 200 (5502 bytes). PixelRAG pixelshot 0.4.0, CDP, one worker, captured three tiles, `page_height` 4556, `complete: true`. I read all three tiles. I did not capture a mobile viewport, and I did not click through the running page. Button behavior below is from `website/dist/subscriptions.js`, `moth-connector.js`, and `website/tests/subscriptions.cjs`, which the page loads. The test file was read, not re-run.

The initial screen is one column, max width 1100px.

1. Header navigation, then eyebrow "BROWSER LOCAL SIMULATION", then the title "Your local inbox."
2. Three paragraphs. The simulation lives in this tab's memory. Reload or Reset clears it. Subscribing sends no server request. Selectors in the proposed design run after authorized decryption and do not hide a shard from an authorized reader. The demo has no decryption and no production permission service.
3. "Optional Moth wallet", before any catalog. The origin paragraph names `http://127.0.0.1:8876` and states that on `CharlesHoskinson.github.io` every project path shares that origin. Connect is present in the HTML as `disabled` until `#wallet-ack` is checked. The tile shows Discover, Connect, Check wallet status, and Disconnect locally together. Status text: "disconnected. Local disconnect cannot revoke Moth's origin grant."
4. "Browse streams", with Search streams, Category (All categories plus quotes, payments, approvals, contracts, credentials, ops), and Consumer mode (Human on the tile).
5. Nine example cards from `subscriptions-fixtures.json` (`records` length 9). Each v0.2 card offers Inspect example, Simulate this occurrence, and Subscribe to a category. The three payment cards each say "Subscribe to payments". The expired quote card has no subscribe button. Contract, credential, and ops cards are labeled "Unsigned local mock; no model profile validation".
6. "Subscriptions" is a simulation console: eight equal buttons (Simulate intake and delivery, Mark next item reviewed, Simulate rejected quote, Replay last occurrence, Simulate retention gap, Expire local permissions, Revoke local permissions, Reset demo, Export mock-only demo state). The status line on the tile reads "Mock local permission: granted. Wallet grants are separate. Simulated host journal high-water: 0; this does not measure whole-shard coverage." Empty copy: "Choose a stream to create a local subscription."
7. "Inbox and quarantine", empty: "No local receipts yet. Subscribe and simulate intake." Collapsed "Message detail". No journal list, no folders, no read or unread marks, no second tab.

There is no `localStorage`, `sessionStorage`, or `indexedDB` use in `subscriptions.html`, `subscriptions.js`, or `moth-connector.js`. Search, category, consumer mode, subscriptions, inbox, journal, and the mock permission flag are ordinary script variables. Reload drops them because they were never stored. That part of the privacy boundary is real.

Deficiencies that matter for trust:

- The title and the empty inbox teach a mailbox. The control on every card subscribes to a category. Three different payment examples are one action. The product requirement asks for distinct feed identities and says browse categories are navigation aids, not network topics. The screen does the opposite: the category is the only subscribable object, and the examples are aliases of it.
- "Simulate intake and delivery" runs only for categories that already have an active or paused subscription, then `ingest` appends to the host journal and enqueues matches. With zero watches, the host journal stays at 0. The requirement says whole-shard intake stays independent of which messages match. The demo teaches the reverse, and the empty inbox tells the person to subscribe in order to receive. `negative` likewise refuses the rejected quote until a quotes subscription exists.
- Consumer mode is a persona. `scope()` always writes `owner: 'principal:demo'`. Changing the select also forces the category (`wallet` to quotes, `dapp` to payments, `agent` to approvals). The help text for wallet says these are browsing defaults, not grants, and that connecting Moth does not unlock the simulation. The control still sits in the filter row under the name "Consumer mode", beside a real Connect button further up the page.
- Reset, Expire local permissions, and Revoke local permissions are peers in one button grid. Reset sets mock permission back to `granted`, clears the in-memory arrays, and announces "Demo memory cleared. Moth origin grants are unaffected." It does not call the connector. Disconnect clears the adapter handle only. The test expects the status line to match `/cannot revoke/`. The spatial grouping still makes the three "stop" words look like one authority.
- The wallet disclosure is the first interactive block on a page whose job is the catalog. Connect stays disabled until the checkbox, which is the right gate, and the facts in the paragraph match the Moth source below. It is long, it is above the task, and it merges silent reads with submitting a supplied transaction into one breath. Building a transfer is a separate Moth prompt. The current sentence can be read as silent spending.
- Search filters `title` and `category` in memory on each input event. The query is not stored. Nothing about the catalog scales past these nine cards. There is no folder model to be private or leaky, because there is no folder model.
- Export builds a JSON blob with an explicit mock-only notice and downloads `midnight-express-demo.json`. It includes intents, history, and dispositions. It does not include a wallet grant. The button sits in the simulation grid, so a later durable export could be mistaken for an ordinary console action.

`#connect` is disabled in the initial HTML. Discovery reads `window.midnight.moth` and does not call `connect`. `connect()` returns a failure unless `navigator.userActivation.isActive`. The connector calls `connect(networkId)` and `getConnectionStatus` only. The test asserts that loading the page leaves wallet call counts at zero, and that simulation does not poll.

Profiles in the closed local intent schema, which the demo must not pretend to extend: `quotes` / `rfq.v0.2`, `payments` / `invoice.v0.2`, `approvals` / `agent.v0.2`, and `contracts`, `credentials`, `ops` as `mock.local.v1` / `mock-only`. Fixture clock on the page is `2026-10-04T12:00:00.000Z`. Accepted v0.2 rows are offline reference checks. They are not live source authentication.

## Sources, and what was actually read

Retrieval was Scrapling Fetcher. Visual captures were PixelRAG pixelshot 0.4.0 over CDP, one worker. CPU only. No GPU path was used. Fetched text was treated as data.

Robots: `https://www.w3.org/robots.txt` (file id `$Id: robots.txt,v 1.106 2026/07/14`) allows `/TR/privacy-principles/` and `/TR/websub/`. The disallow entry `/TR/?` is the query-string index. `https://developer.mozilla.org/robots.txt` disallows `/api/`, `/*/files/`, and `/media`. The two MDN documents below are allowed. One page was fetched on each other host, except the GOV.UK warning-text URL, which was fetched twice (text, then the same URL with tiles).

| Slug | What it is | Result |
|---|---|---|
| `incumbent-subscriptions` | Live demo, 2026-10-05T20:27:22Z | Accepted. Text sha256 `4e565663b6cf3bab95199fd31723a040ad840336521cea195a012d7d8ac9104c`. Three tiles read. |
| `govuk-warning-text-visual` | GOV.UK Design System, Warning text. Same text sha256 `cb6e8f7a955ffc2dd2af60e46606cdc33ebf64f20801999592aa1ba6fa24ad2a` as the earlier non-visual fetch. Retrieved 2026-10-05T20:31:10Z | Accepted best-practice visual. Two tiles, page height 2427, complete. Tile 0 shows the component and "When to use this component". Tile 1 is the page footer. Crown copyright, Open Government Licence v3.0, no document revision date printed on the page. |
| `w3c-privacy-principles` | W3C Statement, 15 May 2025. This version `https://www.w3.org/TR/2025/STMT-privacy-principles-20250515/` | Accepted. Text read at the principles cited below. |
| `w3c-websub` | W3C Recommendation, 02 June 2026. This version `https://www.w3.org/TR/2026/REC-websub-20260602/` | Accepted. Sections 5.1 and the role definitions read. |
| `mdn-same-origin-policy` | MDN, final URL `.../Web/Security/Defenses/Same-origin_policy`. Retrieved 2026-10-05T20:28:27Z | Accepted. Origin definition and storage paragraph read. No publication date on the page. |
| `mdn-local-storage` | MDN `Window.localStorage`. Retrieved 2026-10-05T20:28:29Z | Accepted. Persistence contrast with `sessionStorage` read. |
| `github-pages-what-is` | GitHub Docs, "What is GitHub Pages?". Footer © 2026. Retrieved 2026-10-05T20:28:30Z | Accepted. URL types and the IP-log sentence read. |
| `rss-20-specification` | RSS Advisory Board, RSS 2.0. The page says the document follows RSS 2.0.1 (July 2003). Retrieved 2026-10-05T20:28:32Z | Accepted. "What is RSS?" and the required `channel` element read. |
| `moth-connector-handlers-d48206a` | `shieldedtech/moth-wallet` blob `d48206a1957af09bf17bf5e941c2b5bccb12db63`, `packages/extension/lib/background/connector-handlers.ts`. Retrieved 2026-10-05T20:31:10Z. Raw sha256 `7726712a87ab1d7f79a82b41f25b661dc030fb8f675d7c2f28ab9db5abb1b545` | Accepted. Grant, read methods, `submitTransaction`, and `permissionsRevoke` read. |
| `apple-hig-privacy` | Apple Human Interface Guidelines, Privacy. Retrieved 2026-10-05T20:28:24Z | Rejected as authority. Fetcher text is the noscript line "This page requires JavaScript." (154 bytes). The CDP tile is 1568px and marked complete. I read it: title, the lead "Privacy is paramount…", an illustration, two paragraphs about App Store privacy details, and a phone mock of nutrition labels. The sidebar lists Best practices and Requesting permission. Those sections are not in the captured article, so they are not cited. |

### What the accepted sources support

W3C Privacy Principles, 15 May 2025. Principle 2.2.1: sites restrict data they transfer to what is necessary for the user's goal. Principle 2.2.2: APIs minimize what sites must request, and provide granularity. Principle 2.4: sensitivity depends on the person and the context; designers do not treat unfamiliar categories as harmless. Section 1.2 names interests, opinions, and behaviour as reasons collection can harm. Principle 2.12.1: a consent request learns whether the person consents, and does not maximize the processing. Principle 2.12.2: do not interrupt the task for consent when an alternative exists. Principle 2.12.3: checking or withdrawing consent is as easy as giving it. The prose around lines 904–911 of the fetched text: permissions can be delayed; persistent access needs a visible indicator and a way to turn it off.

GOV.UK Design System, Warning text, as shown on tile 0: use that component for something important, such as legal consequences of an action the user might take. The ordinary catalog, the simulation, and the empty inbox do not meet that bar. The Moth origin grant does, because of what the pinned handler actually allows.

WebSub Recommendation, 02 June 2026, section 5.1. A subscriber POSTs `hub.callback`, `hub.mode` (`subscribe` or `unsubscribe`), and `hub.topic` to a hub. The subscription key is `(topic URL, callback URL)`. The publisher definition says the publisher is unaware of subscribers. The hub is not. A hosted directory that receives "what I watch" is this shape. It is the pattern the private transport refuses.

RSS 2.0. A channel is one element inside an XML document a client retrieves. Required children are title, link, and description. The specification contains no join, no membership list, and no callback. That is useful only as a limit on the word: in syndication, "channel" names a document. In a product UI it will be heard as a room. Midnight Express also does not work by polling a public URL, so RSS is not the interaction model to copy.

MDN same-origin policy. Origin is scheme, host, and port. `http://store.company.com/dir2/other.html` is the same origin as `http://store.company.com/dir/page.html` because only the path differs. Web Storage and IndexedDB are separated by origin: script in one origin cannot read another origin's storage. The inverse is the operational fact: every path on one origin shares that storage.

MDN `localStorage`. The storage object is for the document's origin and is saved across browser sessions. `sessionStorage` is cleared when the page session ends. I did not fetch a separate `sessionStorage` sharing document, so I do not claim `sessionStorage` is safe against a later same-origin page in the same tab.

GitHub Docs, What is GitHub Pages. A project site's default location is `http(s)://<owner>.github.io/<repositoryname>`. A user site is `http(s)://<owner>.github.io`. The page also says a visit logs and stores the visitor's IP address for security, signed in or not. The docs page does not say that project paths share storage. That conclusion is the MDN origin rule applied to the URL shape GitHub documents. Loading the static demo can be in GitHub's IP log. A local filter that never makes a request does not add the query to that log.

Moth `connector-handlers.ts` at `d48206a`. `ensureConnected` calls `grant(origin, networkId)`. `isAllowed(origin)` is the later check. The `hintUsage` comment in the file says Moth grants per origin all at once, and a hint is treated as a connection request. After that grant, these methods call `requireConnected` and do not call `requestApproval`: shielded, unshielded, and dust balances; shielded, unshielded, and dust addresses; `getTxHistory`; `getProvingProvider` and the prove calls; `submitTransaction` of a supplied transaction hex. `makeIntent` and `makeTransfer` call `requestApproval` before they build. `signData` calls `requestApproval` because signing uses the transaction key. `permissionsRevoke` is an extension `onMessage('permissionsRevoke')` handler, not a page connector method. The page cannot revoke the grant. There is no page `disconnect` in the method switch.

## Recommended information architecture

The default surface is a local catalog of scenario views. A scenario view is a synthetic row in a declared family. It is not a relay topic, not a shard, and not a new contract. Hundreds of rows are allowed only as views over the profiles the schema already closes.

| Row family | Selector the watch may use | Label on the row |
|---|---|---|
| Quote scenarios | `quotes` / `rfq.v0.2` and the schema contract | Offline reference. Live source is not verified. |
| Invoice scenarios | `payments` / `invoice.v0.2` and the schema contract | Same. Predicate `all` or `payment-final` is part of the watch, chosen on the watch, not a second feed. |
| Approval scenarios | `approvals` / `agent.v0.2` and the schema contract | Review records a local disposition. It grants no tool. |
| Contract, credential, ops reminders | `mock.local.v1` / `mock-only` | Unsigned local mock. No model profile. |

Many invoice scenarios share one watch. The row action on the second invoice scenario reads "Open the local payment watch" once that watch exists. The catalog does not create a watch per row, and it does not mint contract hashes for the extra rows.

Folders are a local sorting overlay. A folder has an id and a person-authored label. Placing a scenario in a folder does not change `selector.category`, profile, contract, predicate, or `sourceEquals`. The folder is absent from any intent document. It is also absent from export unless the person turns on a separate "include my folder labels" choice, which the public demo does not offer.

The inbox is a second region, fed only by local enqueue. It is not the home view. The host journal is a third, quieter region: a count and a bounded list of originals the simulation has accepted into the tab. Advancing that journal does not require a watch. A watch copies matches into the inbox under the existing bounds (2 in flight, 4 queued, 16384 bytes). Pause stops that copy. It does not stop the journal. Repair and whole-shard intake stay off the catalog. They are host machinery. They do not appear as business rows.

### Interaction

Desktop, wide viewport. Catalog list on the left, about 40 visible rows, the rest windowed. Selecting a row shows its text, its profile class, and one primary button, "Watch locally", in the right-hand pane. The pane states the principal handle the demo will write (`principal:demo`) and that this is a fixed demo owner, not the signed-in person and not the wallet account. Consumer journeys move to a select labeled "Example journey" inside the catalog toolbar. Changing it changes which family is suggested. It does not write `owner`, does not check the wallet box, and does not call `connect`.

The wallet control is a header status, "Wallet: not connected". Activating it opens an inline disclosure, not a modal, containing the one serious warning, the checkbox, and Discover, Connect, Check status, Disconnect locally. The catalog remains usable with that disclosure closed. That is principle 2.12.2: browsing has an alternative to the grant. The warning meets the GOV.UK bar and stays in that disclosure only.

Mobile, narrow viewport. I did not capture one. The proposed order is a single column: title, filter field, catalog, then the selected scenario's "Watch locally" in the lower thumb zone once a row is selected. Simulation controls sit in a closed `details` element, "Simulation". The wallet disclosure is the same component as desktop, reached from "Wallet: not connected" in the header. Warning text is inside it, in full, before Connect. Connect stays disabled until the checkbox. Touch targets for Watch, the checkbox, and Connect are at least 44 by 44 CSS pixels. Hover is not required. At 320px CSS width and 200% text, the column scrolls vertically and does not scroll horizontally. That last condition matches the existing test's intent at 390px; the new width is the acceptance bar for this layout.

Search is a persistent-label field, "Filter the catalog". The placeholder may show an example. The label remains. Each input event filters the in-memory views. It does not write storage, does not append a recent-search list, and does not call the network. Reload clears the field because it was never stored.

Read and unread, if the council keeps them, are presentation marks on inbox rows only. "Unread" means this tab has not opened the row. "Awaiting review" remains the disposition until "Mark reviewed" runs. Opening a catalog scenario does not create a read mark. A read mark does not move the delivery cursor or the processing cursor, and it is not an effect.

### Rejected alternative

A hosted feed reader, or a WebSub-style hub, where the directory operator receives the follow, the topic, and a callback, and folders sync to that operator. WebSub is explicit that the hub stores `(topic, callback)` even though the publisher may not see the subscriber. A Feedly-style account would store the follow list and the queries on someone else's origin. Both publish interests. Kafka or NATS subject subscription is the same disclosure with a different product name: the broker learns the selector. The requirement already refuses a broker that sees business selectors. The UI should not reintroduce that disclosure under the label "channel" or "follow".

Also rejected: one button that connects Moth, creates a watch, and approves a transfer. The handler shows those are different calls, and two of them have their own prompts. Also rejected: a wall of threat acknowledgements before the catalog. One serious warning belongs on the grant. The rest of the page stays ordinary product copy.

## Wireframe snippet

Proposal only. This is not an edit to `website/dist`.

```html
<!-- Desktop: catalog | detail. Mobile: the same regions stack in source order.
     Wallet and Simulation are disclosures. They are not the first task. -->
<header class="site">
  <a class="brand" href="index.html">Midnight Express</a>
  <nav aria-label="Main navigation"><!-- existing links --></nav>
  <button type="button" aria-expanded="false" aria-controls="wallet-panel">Wallet: not connected</button>
</header>

<section id="wallet-panel" hidden>
  <h2>Optional Moth wallet</h2>
  <p>Moth 4.0.1 is an experimental, unaudited reference wallet. Network: preprod.
     Connect asks Moth to allow this whole origin. This page will call connect and
     connection status only.</p>
  <p id="origin-warning"><!-- filled with location.origin, plus the Pages sentence --></p>
  <label>
    <input id="wallet-ack" type="checkbox">
    I understand Moth keeps this origin grant until I revoke it in Moth.
  </label>
  <button id="discover" type="button">Discover Moth</button>
  <button id="connect" type="button" disabled>Connect Moth</button>
  <button id="check-wallet" type="button">Check wallet status</button>
  <button id="disconnect" type="button">Disconnect locally</button>
  <p id="wallet-status">Disconnected. Disconnect on this page leaves the Moth grant in place.</p>
</section>

<main id="main-content">
  <h1>Local catalog</h1>
  <p>These are synthetic scenarios on this machine. Watching one keeps a local copy
     in this tab. It does not register a topic with a relay.</p>

  <form role="search">
    <label for="search">Filter the catalog</label>
    <input id="search" type="search" autocomplete="off" placeholder="Quote, invoice, approval">
    <label for="family">Profile class</label>
    <select id="family">
      <option value="all">All classes</option>
      <option value="rfq.v0.2">Quotes, rfq.v0.2</option>
      <option value="invoice.v0.2">Payments, invoice.v0.2</option>
      <option value="agent.v0.2">Approvals, agent.v0.2</option>
      <option value="mock.local.v1">Unsigned mocks</option>
    </select>
    <label for="journey">Example journey</label>
    <select id="journey" aria-describedby="journey-help">
      <option value="human">Human</option>
      <option value="wallet">Wallet</option>
      <option value="dapp">DApp</option>
      <option value="agent">Agent</option>
    </select>
    <p id="journey-help">Changes which family is suggested. The demo owner stays principal:demo.</p>
  </form>

  <!-- Folders, when a dedicated origin exists: a list of labels filtering the rows.
       Creating a folder does not call watch.create. Public Pages demo omits this. -->
  <div class="catalog" role="listbox" aria-label="Scenarios">
    <div role="option" aria-selected="true">
      <h2>Shares / USD quote</h2>
      <p>Scenario view of rfq.v0.2. Offline reference. Live source is not verified.</p>
    </div>
    <!-- Further invoice rows name the same invoice.v0.2 watch once it exists. -->
  </div>

  <section aria-labelledby="scenario-heading">
    <h2 id="scenario-heading">Shares / USD quote</h2>
    <p>Historical offline quote. Off-chain coordination only.</p>
    <p>Local watch selector: quotes, rfq.v0.2, predicate all, sources already authenticated locally.
       sourceEquals empty does not mean anonymous.</p>
    <button type="button">Watch locally</button>
    <!-- Second invoice scenario, after a payment watch exists:
         <button type="button">Open the local payment watch</button> -->
  </section>

  <section aria-labelledby="journal-heading">
    <h2 id="journal-heading">Host journal in this tab</h2>
    <p>High-water 0. This counter is intake. It is not inbox delivery, not a processing decision,
       and it does not measure a real shard.</p>
    <button type="button">Add the next scenario original</button>
  </section>

  <section aria-labelledby="inbox-heading">
    <h2 id="inbox-heading">Inbox and quarantine</h2>
    <p>Delivery cursor: local receipt. Processing cursor: contiguous reviewed or quarantined items.
       An effect needs a separate action, which this page does not prepare.</p>
    <!-- Unread is a mark on the row. Mark reviewed is a different button. -->
  </section>

  <details>
    <summary>Simulation</summary>
    <button type="button">Mark next item reviewed</button>
    <button type="button">Simulate rejected quote</button>
    <button type="button">Replay last occurrence</button>
    <button type="button">Simulate retention gap</button>
    <button type="button">Expire simulated local permission</button>
    <button type="button">Revoke simulated local permission</button>
    <button type="button">Clear this tab</button>
    <button type="button">Export mock-only demo state</button>
  </details>
</main>
```

On a narrow screen the detail section follows the selected row, and "Watch locally" is the primary control. The journal sentence stays visible. The simulation `details` stays closed. The wallet panel stays closed until the header button opens it.

## State contract

Presentation state is not a wire extension, not an MPE profile, and not a permission grant. Names below are for the UI. The durable intent, when a local service exists, remains `LocalSubscriptionIntent` as already schema-closed.

Tab memory, always, cleared by reload and by "Clear this tab":

| Field | Meaning |
|---|---|
| `query` | Current filter string. Never written to storage. Never added to a history list. |
| `family` | Profile-class filter. A UI grouping of the closed profiles. |
| `journey` | `human`, `wallet`, `dapp`, or `agent`. Persona. Does not write `owner`. |
| `selectedScenarioId` | Which synthetic view is open. |
| `folderDraft` | Unsaved folder label edits, if the dedicated-origin UI is showing them. |
| `walletPanelOpen` | Disclosure visibility. Not connection state. |
| `mockPermission` | `granted`, `expired`, or `revoked` for the simulation only. |
| `journal`, `inbox`, `watches` | The current in-memory demo. Watches use the existing intent shape, `owner: principal:demo`. |

Dedicated-origin organization store, off in the public demo and off on `*.github.io` project paths:

| Field | Meaning |
|---|---|
| `folders[]` | `{id, label}`. Person-authored. Local sorting only. |
| `placement[]` | `{scenarioId, folderId}`. |
| `readMarks[]` | `{occurrenceKey}` for inbox rows. Presentation. |
| `organizationNoticeSeen` | The person saw the one sentence about origin-readable storage. |

That store must not contain the query, query history, wallet status, Moth grant, principal, cursors, intents, dispositions, fixture bodies, or sealed wire. On reload it may restore folders and read marks. It must not restore `mockPermission`, watches, cursors, or a wallet session. A read mark must not satisfy "awaiting review".

Technical dispositions:

| Event | Result |
|---|---|
| Reload | Tab memory returns to the initial demo: no watches, empty journal and inbox, mock permission `granted`, journey `human`, query empty. No `connect`, no `getConnectionStatus`. Moth's stored origin grant is unchanged. Organization store, if a future dedicated origin has one, restores labels and read marks only. |
| Clear this tab | Same as reload for tab memory. Announcement states that the Moth grant is unchanged. Does not call `disconnect`. |
| Disconnect locally | Drops the adapter handle and cancels in-flight connector calls, as the adapter does today. Announcement: the grant remains until it is revoked in Moth. |
| Revoke simulated local permission | Sets `mockPermission` to `revoked` and blocks simulated intake, delivery, and processing. Leaves disclosed inbox rows visible. Does not call Moth. |
| Expire simulated local permission | Same shape, state `expired`. |
| Filter keystroke | Updates `query` and the visible window. No storage write. No request. |
| Create folder | Inserts a label in the organization store on a dedicated origin, or only in tab memory in the public demo. Does not create a watch. |
| Watch locally | Creates one in-memory intent for that closed selector if none exists. A second scenario of the same selector focuses the existing watch. |
| Mark unread / read | Toggles a presentation mark. Delivery cursor, processing cursor, and disposition stay put. |
| Mark reviewed | Records the local disposition and may advance the processing cursor, as the demo does today. Still `executes: false`. |
| Add the next scenario original | Appends one declared fixture to the journal even when no watch exists. Enqueue happens only for matching active watches. |
| Export | Downloads the mock document with the existing notice. Omits folder labels and the query unless a later, separate disclosure adds them. The public demo does not add them. |

`sourceEquals: []` continues to mean "sources the local policy has already authenticated", as the schema README says. The scenario pane says that in a sentence. Anonymous transport membership is not a business source. Unsigned mocks say they have no profile.

Processing checkpoint, delivery, and effect stay three sentences in the inbox header. The journal high-water is a fourth sentence, in the journal region, so an empty inbox cannot be read as an empty shard.

## Scale, keyboard, and performance acceptance

These are checks a later implementation can run. I did not run them against a 400-row build, because the live page has nine records.

- The scale harness is a declared scenario family: repeated views over `rfq.v0.2`, `invoice.v0.2`, `agent.v0.2`, and the three `mock.local.v1` profiles. It fabricates no contract hash, no wire acceptance, and no validator result. A metadata harness still does not replace independently selectable watches for the closed profiles.
- With 400 view records, the document holds a bounded window (target: 60 row nodes or fewer). Filtering does not mount the rest.
- An input listener on the filter, observed the way `subscriptions.cjs` counts requests, leaves the request count unchanged. No analytics call is added for the query.
- The same input listener leaves `localStorage.length` and `sessionStorage.length` unchanged on the public demo.
- Opening the page leaves Moth call counts at `{connect: 0, status: 0}`, as the current test requires.
- "Clear this tab" and reload leave those counts unchanged and leave any pre-existing extension grant unmentioned by a new `connect`.
- Keyboard: the skip link lands on the catalog heading. Tab order reaches the filter before the wallet disclosure. Slash focuses the filter only when focus is not in a field. Arrow keys move the listbox. Enter activates "Watch locally" for the selected row. Escape clears the query when the filter is focused, and closes the wallet disclosure when it is open. The wallet checkbox is not pre-checked. Connect cannot be activated while disabled.
- A watch, a folder label, and a read mark are three operations. Folder and read-mark controls are absent on the public demo, so they cannot be triggered by a shortcut there.
- Performance budget for this surface is interaction, not a hero image. The catalog window uses content visibility or an equivalent list window so a filter does not lay out 400 articles. No per-keystroke write. No new font and no display face. The existing product sans is enough (Operate). Motion, if any, is the disclosure opening, under 250ms, and it is not required to understand the state.
- Narrow layout: at 320 CSS pixels and at the existing 390 by 844 viewport with root font size 200%, `scrollWidth <= innerWidth`. The Watch control, the acknowledgement checkbox, and Connect are at least 44 by 44 CSS pixels. I did not verify that on a device. A resized screenshot would not verify the touch size either.

## Product prose

Use these sentences. They are the copy, not decorations around it.

Catalog title: "Local catalog."

Lead: "These are synthetic scenarios on this machine. Watching one keeps a local copy in this tab. It does not register a topic with a relay."

Profile class help, one line under the select: "Classes match the fixed profiles. A folder, if you add one later, only sorts this list."

Scenario, supported profile: "Offline reference for rfq.v0.2. The model check used the fixed test clock. This page has not verified a live source."

Scenario, mock: "Unsigned reminder. No business profile and no source authority."

Watch button: "Watch locally."

Watch already present: "Open the local payment watch."

Watch confirmation: "Local watch saved in this tab. Reload clears it. The host journal is separate."

Empty inbox: "No local copy has been delivered to this inbox."

Empty journal: "No scenario original has been added to this tab's journal."

Journal button: "Add the next scenario original."

Example journey help: "Changes which family is suggested. The demo owner stays principal:demo. Connecting a wallet is separate."

Wallet lead: "Connect asks Moth to allow this whole origin. This page will call connect and connection status only."

Origin sentence, after `location.origin`: "On CharlesHoskinson.github.io, every project path shares that origin. Scripts on those paths can read balances, addresses, and history, use the proving provider, and submit an already supplied transaction. Building a transfer or signing still asks in Moth."

Checkbox: "I understand Moth keeps this origin grant until I revoke it in Moth."

Disconnect status: "Disconnected. Disconnect on this page leaves the Moth grant in place."

Clear this tab announcement: "Cleared this tab. The Moth grant is unchanged."

Revoke simulated permission announcement: "Simulated local permission is revoked. Moth was not changed."

Unread: "Not opened in this tab."

Reviewed: "Reviewed locally. No effect was executed."

Folder sentence, dedicated origin only: "Folder labels stay in this browser for this site. Any page on this origin can read them. They do not turn a watch back on and they do not connect a wallet."

The public demo does not show the folder sentence, because it does not offer the store.

Export button stays "Export mock-only demo state." The file notice stays the one already in the script.

## Consensus recommendations

1. Make the catalog the home view. Keep the inbox, the host journal, and the simulation as separate regions with the four sentences above (intake, delivery, processing, effect).
2. Treat each closed profile as one local watch. Treat extra rows as scenario views in a declared family. Do not invent wire acceptance to pad the catalog to hundreds.
3. Keep categories and folders out of relay topics, out of the sealed envelope, and out of the intent's routing. A folder is a label. A profile class is a filter over the schema.
4. Keep four capabilities on separate controls: source class (offline reference, unsigned mock, or later a real authenticated source), shard membership and host intake, the local watch, and the Moth origin grant. The journey select is a persona and writes none of them.
5. Ship the public demo, including a future `github.io` build, with no `localStorage` and no `sessionStorage` for queries, folders, read marks, or watches. Queries are tab memory everywhere, including a later dedicated origin.
6. On a dedicated production origin, a local service may store watches and cursors. Browser storage may store folder labels and read marks only after the one folder sentence, and reload of that store must not resume delivery or call Moth. Until that origin exists, omit the store.
7. Leave Connect disabled until the checkbox, require the user gesture the adapter already requires, and keep calling only `connect` and `getConnectionStatus`. Do not add signing, account requests, or a page-level revoke.
8. Place the serious warning only in the wallet disclosure. Use ordinary text for the simulation. State the grant in two clauses: silent reads, history, proving, and submit of a supplied transaction; a further Moth prompt for building a transfer or signing.
9. Separate "Clear this tab", "Disconnect locally", and "Revoke simulated local permission" by label and by region. None of them is `permissionsRevoke`.
10. Make "Add the next scenario original" advance the journal with zero watches. Matching still fills the inbox only for an active watch. Pause still stops delivery and leaves intake alone.
11. Keep export mock-only, explicit, and free of folder labels and search text.
12. Window the catalog. Prove with a request counter and a storage-length counter that filtering is local.

## Dissent

I dissent from adopting a channel, follow, or hub-subscribe metaphor because the directory task is familiar. Familiarity can be the catalog layout. The object of the action has to stay a local watch over a closed profile. WebSub shows what "subscribe to a topic" costs as soon as a hub exists: the hub stores the topic and the callback. This product's privacy claim is that no such hub sees the selector.

I dissent from recent searches, suggested follows, and cloud-synced folders. A query log is a finer interest record than a folder list, and the task does not need it. Principle 2.4 and section 1.2 are why a folder called with a person's name is sensitive even though it is "just organization".

I dissent from a pre-catalog checklist of threats. The grant is the one warning. Repeating it on every scenario trains people to click through it.

## Unresolved

- Whether the council keeps the word "feed" for a scenario row. I can accept "feed" if the lead sentence defines it as a local scenario view and the interface never says channel, topic, join, or follow. I prefer "scenario" and "watch", because "feed" still arrives with a hosted-reader meaning.
- Whether retained folders are in scope for the public Pages demo. The requirement asks for organization between visits, and it also says the current demo does not yet provide that and that saved marks must not restore authority. My resolution is: retain organization only on a dedicated origin, in the limited store above. If the council requires retention on the shared Pages origin, the folder sentence has to be shown, and the store still cannot hold watches.
- The current `tick` path and `subscriptions.cjs` encode intake-through-subscription. The target journal button changes that teaching. It is a demo behavior change, not a protocol change, and it needs a test update when someone implements it. This proposal does not implement it.
- Read marks in the browser versus read marks beside a future service journal. I would omit browser read marks until the service exists, then store them as presentation next to that journal, still outside the processing cursor. If the inbox needs them earlier, they belong in tab memory only.

## Decision log

The directory stays, because the brief already chose it. The privacy work is the noun, the grant boundaries, and where state lives. Browser persistence cannot be the watch, the principal, or the wallet grant; the handler and the origin rule make that a hard boundary on `github.io`. Warning chrome stays on the one action that matches the GOV.UK criterion. Apple's permission-section guidance was not available in the capture, so it is not holding any of these choices up.
