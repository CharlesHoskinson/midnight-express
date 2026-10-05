# Feed directory and state architecture proposal

Reviewer: `gpt-consensus-architecture`, GPT council cohort. Research performed October 5, 2026. This is an independent proposal for council synthesis, not a claim that consensus has already been reached. The user confirmed that discovering and organizing subscriptions is the default workflow; inbox and operator tools support it.

## Recommendation

Make **Directory → feed preview → Follow in demo → organize** the primary journey. Provide **My feeds**, **Inbox**, and **Diagnostics** as distinct destinations. A feed is one named catalog offering with an explicit local scope and several representative examples. A subscription is the consumer's watch over that scope. Folders and saved views organize what the person sees; they never change a subscription selector, grant, cursor, or protocol operation.

Keep the existing Midnight Express identity, but replace the long demonstration document with an Operate surface: searchable compact rows, persistent navigation, a selected-feed preview, and secondary details. The first viewport should contain usable catalog entries. Keep one visible simulation notice; place detailed evidence and permission explanations at the relevant decisions. Preserve all factual warnings without repeating every warning on every row.

## What the incumbent actually does

Inspected `website/dist/subscriptions.html`, `subscriptions.css`, the complete `subscriptions.js`, `subscriptions-fixtures.json`, `moth-connector.js`, `website/tests/subscriptions.cjs`, `docs/product-requirements/pubsub-subscription-experience.md`, `design/subscriptions/README.md`, and relevant fields in `local-subscription-intent.schema.json`. PRODUCT.md and DESIGN.md are absent at repository root; absence supplies no permission to invent product truth. The coordinator ran Impeccable context once. I read Impeccable 4.5.0 and its Operate, critique, clarify, optimize, adapt, shape, and new-work guidance. I applied Operate and planning guidance; I did not run the separate critique command, create a visual-direction contract, or change authority documents.

The current PixelRAG capture is the served route `http://127.0.0.1:8876/subscriptions.html`. I opened all three captured tiles. It is a tall dark single-column page. The large “Your local inbox” introduction and optional wallet section precede the discovery controls; at the captured 875px image width, Browse streams begins near the bottom of the first 1568px tile. The catalog, nine demonstration controls, subscriptions, inbox, and JSON detail occupy one scrolling document. This is direct visual evidence, not a hypothetical critique of a dashboard template.

The crucial architectural mismatch is that the catalog contains **nine event examples**, while following creates a watch for **one of six categories**. Payment pending, final, and reversed each have a separate row and the same “Subscribe to payments” action. The runtime rejects a second non-tombstoned watch for the category. The expired quote is another row with no subscribe action. These rows are examples of events, not independently selectable feeds. Grouping them into a Payments feed with three examples removes a misleading choice before any visual polishing.

Search matches only concatenated title and category strings. It has no publisher/source, scope summary, evidence tier, followed state, folders, saved views, sorting, pagination, or remembered route. Consumer mode changes the category default; it does not change principal or grants. Each input invokes `render()`, which replaces all stream, subscription, and inbox children. Moving a row's subscription controls into a larger catalog without changing this rendering strategy would recreate focus loss and unnecessary work.

All subscriptions, journal entries, deliveries, queues, deduplication state, and dispositions are in memory. Reload clears them. The journal has 64 originals, two in-flight items, four queued events, and 16 KiB queued per subscription; inbox rendering shows the latest 40 receipts. These bounds must not be mistaken for hundreds-feed production durability.

I ran `node website/tests/subscriptions.cjs`. It passed lifecycle guards, scope revisions, bounded recovery, processing checkpoints, exports, fixture quarantine/review, and the mobile 200% text check. It also verifies no server contact from subscription/intake actions and no automatic wallet RPC. This is useful behavioral evidence; it does not establish accessibility completeness, durable storage, real wallet integration, or production transport.

## Source evidence and its limits

All online retrieval used Scrapling. The coordinator's `research.py` archived raw responses, text, status, final URLs, retrieval times, and hashes under `sources/gpt-consensus-architecture/`. Visual captures used PixelRAG `pixelshot` 0.4.0 with CDP, one worker, and 1568px tiles. This was capture and manual visual inspection; I ran no GPU model or relevance scoring.

| Primary source | Version/date and inspected evidence | Applicable pattern and limit |
|---|---|---|
| [Feedly: find and follow sources](https://docs.feedly.com/article/287-how-to-find-and-add-follow-sources) | Updated July 16, 2022; retrieved 2026-10-05T20:08:31Z. Full extracted article text inspected. | A distinct discovery destination and topic/site search. This is older help text, not proof of the current logged-in layout. Do not copy its arbitrary URL ingestion into MPE. |
| [Feedly: follow a feed](https://docs.feedly.com/article/288-how-to-follow-a-feed-in-your-feedly-account) | Updated November 4, 2024; retrieved 2026-10-05T20:08:31Z. Full extracted article text inspected. | Search, follow, then choose a folder. MPE should allow Unfiled so organization is optional. RSS subscription semantics supply no authority model for private watches. |
| [Inoreader public product page](https://www.inoreader.com/) | Current public page, no release version; retrieved 2026-10-05T20:06:50Z. Text plus PixelRAG tiles 0000 and 0001 opened. | Its embedded product image visibly separates navigation, feed/folder list, content, and unread controls. This is a public marketing screenshot, not an authenticated session. Cookie overlay occludes lower portions; unobserved tiles are not evidence. |
| [Inoreader: redesigned search and monitoring feeds](https://www.inoreader.com/blog/2026/09/introducing-mentions-redesigned-search-and-smarter-monitoring-feeds.html) | Published September 14, 2026; retrieved 2026-10-05T20:08:04Z. Full article text and tiles 0002/0003 inspected. | The pictured configuration/preview split and explicit account-versus-public scope support preview before save and named search scopes. MPE's event predicates remain closed and allowlisted; do not import web-wide monitoring or free-form automation. |
| [GitHub: managing notifications](https://docs.github.com/en/subscriptions-and-notifications/how-tos/viewing-and-triaging-notifications/managing-notifications-from-your-inbox) | Current unversioned Docs page; retrieved 2026-10-05T20:08:55Z. Full extracted text inspected. | Read, unread, saved, and completed states are distinct; custom filters can be previewed before saving. Transfer the distinction, not GitHub's exact lifecycle or retention rules. |
| [GitHub: inbox filters](https://docs.github.com/en/subscriptions-and-notifications/reference/inbox-filters) | Current unversioned Docs page; retrieved 2026-10-05T20:08:55Z. Full extracted text inspected. | Explicit filter vocabulary and documented limitations support bounded queries. GitHub's inbox explicitly lacks full-text title search, so it is not evidence for universal search capability. |

Google discovery responses contained only redirect/trouble-access text and were rejected. Two guessed GitHub documentation paths returned 404 and were rejected. Valid GitHub URLs were discovered from its public documentation landing page through Scrapling. Feedly help URLs were discovered from official category indexes. These failures and the exact inspected tile list are recorded in `sources/gpt-consensus-architecture/research-notes.md`. No private browser accounts, paywalls, customer evidence, user study, or authenticated competitor UI were accessed. Proposed usability and performance thresholds below are acceptance targets, not measured improvements.

## Distinct objects and authority

| Object | Meaning | Owned state and boundary |
|---|---|---|
| Feed | A catalog offering: stable `feedId`, name, description, declared publisher label, category, exact profile/contract or mock family, permitted scope template, and reference-example links. | Discovery metadata. Display labels never authenticate business sources. Feed metadata is outside sealed business envelopes and outside the closed intent schema. |
| Channel | An optional publisher-facing grouping of feeds, such as a business workflow collection. | Do not make it a required second hierarchy. It is neither a relay topic nor a transport route. Prefer Publisher and Category labels in the first release. |
| Subscription | A principal-bound local watch, with immutable scope revisions and separate runtime outcome. | Existing `LocalSubscriptionIntent` plus service-owned runtime. `feedId → subscriptionId` belongs in UI/adapter metadata, not as an extra schema field. |
| Event occurrence | A source occurrence and its business evidence, referenced by one or more receipts. | Preserve canonical fixture records, original wire where available, occurrence identity, reference context, and rejection evidence. A pending/final/reversed example is an event within Payments. |
| Delivery receipt | One delivery under one subscription revision, with local receipt position and disposition. | Processing decisions and cursor advancement belong to the consumer service. Use a receipt key; do not collapse separate receipts merely because source/id match. |
| Folder | A person's grouping of feed references. | Presentation only. Rename/move/delete never pauses, broadens, closes, or reinstalls a watch. Delete folder moves references to Unfiled. |
| Saved view | A named query over Directory, My feeds, or already-disclosed Inbox content. | Includes a declared search scope. Saving a view installs no watch and grants no new evidence access. |
| Reading marker | Read/unread, favorite, or saved-for-later presentation state. | Opening a receipt may mark it read; it does not commit reviewed/quarantined, advance processing, or prepare effects. |

The label **Following** must mean that a current local watch exists, with its real outcome available. **Saved** means a retained feed reference. **Active**, **Paused**, **Gap**, **Expired**, **Revoked**, and **Closed** are subscription/runtime states; do not encode them as folder names or a single read/unread badge. Persona defaults must never masquerade as principal identity.

## Directory and discovery

The sidebar starts with Directory, My feeds, Inbox, and then user folders and saved views. Diagnostics is a secondary item below these. Directory is selected on first visit. Returning users can resume their last presentation route, with an obvious Directory link; do not force them into Inbox because it has unread content.

Use compact rows by default. Each row shows name, one-line purpose, declared publisher, category, evidence tier, and Saved/Following or Follow in demo. The name is a preview link; the button is a separate action. Do not make a whole row click swallow selection or button activation. Keep amounts, expiry timestamps, payload fields, cursor numbers, and simulation actions inside preview or supporting views.

Start with three visible catalog facets: **Category**, **Evidence** (v0.2 reference / Mock only), and **Following** (All / Following / Not following). Add Publisher only when meaningful metadata exists. My feeds additionally supports Folder and subscription State. Avoid facets for unavailable production source trust, popularity, uptime, or observed volume. Those would manufacture information scent from unsupported claims.

Default sorting is name A–Z. Search uses case-insensitive token matching across name, plain description, category, declared publisher, and supported-profile name; exact name/prefix matches rank above loose matches. It does not scan raw business JSON by default. Facet groups combine with AND; multiple selections within a group combine with OR. Show active filter chips, result count, Clear filters, and stable disabled zero-count options. Search and sort changes reset to page one; clearing search preserves the other selected facets.

Use **Search feeds** on Directory and My feeds, **Search this feed's examples** inside a feed, and **Search received items** on Inbox. Display the scope above results. Do not offer web-wide or relay-backed search. A global command launcher can navigate to feed names and destinations later; it must not mix catalog matches with private event bodies behind an ambiguous search box.

For 300–500 entries, use 50-row pages with Previous/Next and a visible range. This gives deterministic keyboard order, accessibility semantics, selection boundaries, and back-navigation restoration. Avoid infinite scroll as the default. Add virtualization only if measured event-history scale requires it, with logical positions, stable focus, and an accessible alternative. Hundreds of metadata rows do not justify a custom virtual grid before profiling.

## Preview, follow, and organize

Select a feed and open its preview beside the list on a wide desktop, or as a full route on narrow screens. Show name, purpose, declared scope, evidence tier, and two tabs: Overview and Examples. Examples link to the existing original records; the preview makes no deliveries and never advances a cursor.

For Payments, Overview says “Payment assertions selected locally. Source-observed status is separate from consensus finality.” Examples contains Pending, Final assertion, and Reversed. Final assertions only is a supported local predicate, not a new feed or claim that a payment executed. The expired quote belongs to Quotes' rejected-example section, not a separate subscribable offering.

Follow opens an inline configuration area in the preview: exact selected scope, supported predicate, start position, and optional folder, defaulting to Unfiled. Keep advanced bounded delivery/revision details collapsed. In the current demo, show its actual supported start behavior; do not offer an archive recovery or arbitrary source configuration that the runtime cannot implement. A single explicit **Follow in demo** action creates the memory-only watch and attaches the feed to the selected folder. It sends no subscription network request and does not require Moth.

After success keep the list position, update the row to Following, and show “Following Payments in this demo. New simulated deliveries appear in Inbox.” Offer Change folder and Open inbox. Previewing is optional: familiar users may follow from the row using the same inline configuration. Following an already-followed feed opens its existing configuration rather than creating an accidental duplicate.

For hundreds of entries, My feeds supports checkboxes and a contextual Move to folder / Favorite toolbar. Actions apply to explicitly selected rows on the current page; cross-page selection requires a separate “Select all 217 matches” choice. Moving feeds offers Undo. Do not add Pause or Close to an otherwise harmless organizational toolbar without exposing the distinct effect and selected count. Closing retains its service tombstone and previously disclosed receipts.

The current UI permits one watch per category; the schema itself is not a general feed catalog. Do not solve this by generating 300 fake profile commitments or pretending named publishers are authenticated `sourceEquals` values. For a scale demonstration generate a separate, clearly labeled **synthetic catalog scenario** of FeedDescriptors that reference the six declared families and immutable examples. Its preview must disclose shared scenario scope. Keep display-source names separate from authenticated source selection. **Only the six canonical demo scopes expose Follow controls.** Synthetic aliases expose Preview and Save to folder, plus a link to their canonical scenario; they must never render hundreds of Follow buttons implying independent subscriptions. Their detail says, for example, “Catalog layout example. Uses the shared Payments scenario; saving this entry creates no separate watch.” A 300-row search/layout test is not evidence that 300 genuine source subscriptions work. Independently defined local feed views require materially distinct reviewed selectors, bounded principal/source scope, their own stable IDs, and separately tested runtime support; labels and folders alone do not create that distinction.

## Annotated desktop wireframe

```text
M/E  Subscriptions                         [Demo settings] [Optional wallet]
Synthetic demo. No production delivery or execution.       [About this demo]
┌───────────────────┬─────────────────────────────────────┬────────────────────────┐
│ DIRECTORY         │ Directory                           │ Payments               │
│ My feeds          │ [Search feeds....................]  │ v0.2 reference         │
│ Inbox   4 unread  │ [Category] [Evidence] [Following]   │ Local payment evidence │
│                   │ 6 demo feeds     Sort: Name A–Z     │                        │
│ Folders           │                                     │ [Overview] [Examples]  │
│ ▸ Finance         │ Approvals · Sandbox requests        │ Pending                │
│ ▸ Operations      │ v0.2 reference       [Follow demo] │ Final assertion        │
│   Unfiled         │                                     │ Reversed               │
│ [+ New folder]    │ Credentials · Expiry reminders      │                        │
│                   │ Mock only            [Follow demo] │ Scope: payments        │
│ Saved views       │                                     │ All assertions ▾       │
│   Mock examples   │ Payments · Payment assertions       │ Folder: Finance ▾      │
│                   │ v0.2 reference       [Following]   │ [Follow in demo]       │
│                   │                                     │                        │
│ Diagnostics       │ Quotes · Off-chain quotes ...       │ View evidence details  │
└───────────────────┴─────────────────────────────────────┴────────────────────────┘
```

The preview appears only after selection, so the default list can use the available width. At approximately 1440px the navigation is about 220px, preview 380–440px, and the center flexible. At medium widths preview becomes its own route rather than compressing names. Counts above are illustrative mock state. No wallet consent text is buried: opening Optional wallet shows the existing origin-wide acknowledgement before Connect becomes enabled. Discovery can proceed without entering that flow.

## Mobile wireframe

```text
M/E   Directory                              [Menu]
Synthetic demo                         [Demo details]
[Search feeds.....................................]
[Filters (2)]                  Sort: Name A–Z
6 demo feeds                [v0.2 reference ×]

Payments                                  Following
Payment assertions · v0.2 reference
Declared scope: payments                    [Preview]
────────────────────────────────────────────────────
Quotes                               [Follow in demo]
Off-chain quotes · v0.2 reference            [Preview]

Directory             My feeds                  Inbox
```

Preview replaces the list with a real back link. Back restores query, facets, page, scroll anchor, and focused feed. Folder choices and filters use accessible dialogs/sheets with explicit Apply and Cancel; the main navigation drawer exposes folders and Diagnostics. Prefer labelled controls over icon-only actions. Follow remains an ordinary button in the preview; a fixed footer must not cover content at 200% text or when the keyboard opens. Touch targets are at least 44px, and all hover information has a touch and keyboard equivalent.

## State and persistence contract

| State | Current/demo redesign disposition | Production authority |
|---|---|---|
| Last destination, density, sorting, expanded folders | Versioned local presentation preferences; storage errors fall back to memory. | Preference store; never authorizes operations. |
| Saved feed references, folder membership, favorites, saved catalog views | May persist for public synthetic catalog. State banner explicitly says what is remembered. | Interests may be sensitive; principal-scoped local service storage or an explicitly chosen local device store. No external analytics or diagnostics export by default. |
| Current search, selected filters, page, focused row | Preserve through preview/back. Keep query in memory/session for private content; do not serialize private searches into shareable URL parameters. | Presentation state scoped to authenticated principal, with stale IDs handled gracefully. |
| Demo active watch, permission, journal, queues, processing dispositions | Continue clearing on reload under current documented behavior. Restored saved feed references display Saved / Demo subscription stopped, never Active. | Durable service owns current intent, revisions, runtime, retention, and dispositions; browser requests fresh authorized state. |
| Read/unread and saved receipt marker | Separate from processing; session-only while the synthetic journal remains ephemeral. | Separate principal-scoped presentation record keyed by durable receipt identity. Reading creates no effect or processing commitment. |
| Delivered/processed/retained positions, action deduplication | Never reconstructed from browser preferences. Simulated cursor strings remain mock values. | Service journal, atomic disposition/checkpoint updates, durable action ledger, and journal-bound cursor ownership. |
| Moth connection/grant | Do not persist an adapter handle or connect acknowledgement as reusable permission. No reconnect/status polling on reload. | Only the actual wallet/provider and explicit calls determine status. Local disconnect cannot revoke the origin grant. |

Boot sequence: load validated presentation preferences, load catalog metadata, initialize the demo runtime empty, and render a clear “Organization restored; demo subscriptions and inbox start empty” message if relevant. No automatic signing, wallet connection, status polling, or subscription installation follows from restored preferences. In production, after principal establishment, fetch the authoritative watch list and reconcile saved references; preference data can neither revive revoked watches nor invent permission. A disconnected service shows Last known / Unavailable, never a fabricated Active state.

The distinction between Saved and Following is a deliberate short-term cost of keeping current durability claims true. If council chooses persistent simulated subscriptions/receipts, that is a separate change to demo storage and documentation with an explicit mock-only namespace and no restored authority. Do not quietly ship persistence while the page says all state clears on reload.

Maintain separate stores/selectors for catalog, organization, navigation, runtime subscriptions, and receipt presentation. Give FeedDescriptor stable IDs; bind examples by reference rather than copying/mutating canonical records. Render keyed rows and update only changed regions. A successful folder move cannot cause runtime `watch.pause`, `watch.resume`, scope revision, or checkpoint write. Supported watch scope edits continue to create immutable revisions and retain each delivery's selecting revision. Retention gaps require explicit recovery or an explicit new start, never an automatic jump to latest.

Whole-shard intake and repair stay independent of selector matches. Pausing is a consumer-delivery operation, not a traffic-shaping instruction. All categories and catalog facets remain local navigation; no business topics or match acknowledgements go to relays. The browser does not validate live authority. The exact three v0.2 profiles, fixed October 4 noon context, and `executes:false` reference results remain visible in evidence detail. Contracts, credentials, and operations remain mock only.

## Acceptance criteria for implementation

- At 1440×900, Directory search and at least six compact feed rows are available without scrolling past wallet controls or simulation actions. At 390px and 200% text, no horizontal document overflow or obscured controls occurs.
- A newcomer can search payments, inspect three example statuses under one feed, follow the demo scope, and place it in Finance without interpreting a cursor or touching a wallet. Test this task with representative users; no completion-time claim is made yet.
- Each catalog row has a stable feed ID, a plain description, an explicit evidence tier, and a separate preview/action affordance. A synthetic scale catalog has a prominent label and no invented model commitment, authenticated publisher, usage metric, or live acceptance claim. Assert that only the six canonical scopes can create watches; all aliases have Save/Preview instead of Follow and disclose their shared scenario. Catalog stress tests and watch/protocol tests are separately named and reported.
- With deterministic 300- and 1000-entry catalog fixtures, category/evidence/followed combinations produce correct stable counts; queries and facets survive preview/back; search resets page one; no-results differs from catalog-load failure and inaccessible data.
- Search is local. Test that typing queries, previewing, following in demo, moving folders, and receipt filtering create no subscription or selector-bearing server requests. No business search terms appear in external URL parameters or telemetry.
- Tab reaches every control in meaningful order. Enter opens the focused preview link; Space toggles a native checkbox; Escape closes a sheet and returns focus to its trigger. Shortcuts are optional, documented, and disabled inside editable fields. Page changes and result counts are announced without announcing every row on each keystroke.
- Follow success updates its row without replacing the focused DOM node or stealing list position. Mobile back restores the prior row and scroll anchor. Loading reserves layout; failure offers Retry and never masquerades as an empty directory.
- Moving/deleting folders changes only organization. Closing a watch preserves its tombstone and disclosed receipts. Batch actions state the selected count and page scope; no action silently selects hidden matches.
- Opening or marking an item read leaves the processing cursor unchanged. Reviewed/quarantined is an explicit disposition action tied to a specific receipt, not the current global “next item” across unknown feeds. Neither action prepares an effect.
- Reload restores only the declared preference classes; simulation runtime starts empty and wallet calls remain zero. Corrupt/unknown preference versions, disabled storage, renamed/removed feed IDs, and reset distinctions produce comprehensible fallback states.
- Revoked/expired watches cannot resume because a browser preference says Following. Gapped/paused combinations retain their distinct delivery intent. Gap acceptance never drops queued undecided work or silently resets history. Preserve existing lifecycle test assertions and extend them for changed navigation/state contracts.
- On a recorded reference device, target p95 search/filter response below 150ms for 1000 lightweight descriptors and p95 input-to-next-paint below 200ms. Record browser/device/data size before reporting results. Limit rendered catalog rows to the selected 50-row page; do not load every canonical payload into every row or recompute JSON detail per keystroke.
- Run one desktop/mobile inspection batch and one confirmation batch after fixes, following Impeccable's bounded verification guidance. Measure performance before adopting virtualization. Real extension testing and production service durability remain separate integration gates.

## Product language examples

Directory notice: “Synthetic demo. Explore feeds and simulate local deliveries.”

Evidence label: “v0.2 reference · checked offline.” Detail: “Checked at the fixed demo context on October 4. Live source, permission, and finality are not verified. No effect executes.”

Mock label: “Mock only · no supported business profile.”

Reload notice: “Your folders and saved feeds were restored. Demo subscriptions and inbox start empty.”

Reading action: “Mark read.” Processing action: “Record reviewed — no effect.”

Paused state: “Delivery paused. Whole-shard intake is independent.” Gap state: “Some history is unavailable. Review the gap before choosing a new start.”

Empty filtered directory: “No feeds match these filters. Clear filters or change your search.” Unfiled empty state: “Newly saved feeds appear here until you choose a folder.”

Optional wallet entry: “Optional Moth connection.” Its consent view retains the full existing origin-wide exposure statement and local-disconnect limitation. Never rename the actual grant Read-only wallet permission merely because this adapter calls only connect and connection status.

## Council decisions and dissent

Strong recommendations for consensus: directory default; one row per feed rather than per occurrence; explicit Directory/My feeds/Inbox destinations; preview before follow; optional folder choice; local facets and named search scopes; separate reading and processing; preference persistence without authority restoration; and immutable canonical fixtures.

I dissent from an inbox-first homepage, a console of simulation controls as the default, a card wall with every payload visible, free-form network topic creation, unread-driven checkpoint advancement, and automatic wallet reconnection. Each undermines the confirmed directory task or a documented authority boundary.

Unresolved decisions for the coordinator: whether to expand the simulator to independently defined mock watches with reviewed distinct selectors; whether the public demo should persist synthetic runtime in a later explicitly documented phase; and whether Folder means one primary folder or multi-membership. My defaults are six canonical Follow actions with non-followable catalog aliases, preferences-only persistence, and one primary folder plus favorites, because these are understandable and implementable without pretending a production catalog exists.

For friction, the present route asks a person to pass the introduction and wallet section, choose among repeated payment occurrences, then find subscription/inbox controls elsewhere in the document. The proposed route makes search, selection, scope, and optional organization contiguous. This is a reasoned structural improvement supported by observed layouts and documented product patterns; it is not a measured business or usability result.
