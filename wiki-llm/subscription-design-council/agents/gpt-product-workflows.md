# GPT product workflows review

Reviewer: `gpt-product-workflows`. Reviewed 2026-10-05. Scope: human, wallet, DApp and agent journeys for the user-confirmed default, **a feed directory for discovering and organizing subscriptions**. Inbox and operator activity support that task. This is a research proposal; it changes no product code, model contracts, fixtures or design authority.

## Recommendation

Make Discover the initial view within Subscriptions. Give people a searchable feed list, an adjacent semantic preview, a clearly scoped **Follow in demo** action, folders, and saved discovery searches. Keep Inbox and Activity as explicit destinations. Move optional Moth connection into Connections. The browser demo remains usable without connecting a wallet.

Keep four concepts separate: a feed is a discoverable description of a local scope; a subscription is the installed watch; an update is a delivered occurrence; a view is an organizational or search projection. Categories and folders are local navigation aids. They are not network topics, authorization scopes or new business profiles.

The current canonical runtime supports one non-closed subscription per category. Preserve that while redesigning the directory. A large synthetic catalog is a UX stress fixture, not evidence of hundreds of distinct authenticated feeds. Each synthetic catalog view must name its canonical scenario family and disclose that following it follows the family. An alias must show **Already following this family** when its family watch exists. Do not turn a synthetic business name into a fake `sourceEquals` identity.

## Evidence and limits

Read the actual HTML, CSS, JavaScript, fixture records, Moth adapter, subscription tests, product requirements and proposed intent contract. Executed `node website/tests/subscriptions.cjs`; it passed lifecycle guards, bounded replay, checkpoints, fixture review/quarantine, exports, explicit wallet calls and its mobile 200% text overflow assertion. This verifies the incumbent, not the proposal. It supplies no real wallet-extension, durable journal, physical-device or production authorization evidence.

Used Impeccable 4.5.0 Operate, Clarify, Optimize and Adapt guidance: familiar controls, one task per surface, complete interaction states, responsive structural changes and measurement before optimization. Root had already loaded context. This review did not run the full `/critique` command or claim independent detector assessments. `PRODUCT.md` and `DESIGN.md` are absent at the repository root; the requirements and code provide product truth.

All online retrieval used Scrapling. PixelRAG `pixelshot` 0.4.0/CDP captured local and public pages; images were inspected with `view_image`. No GPU or retrieval-quality benchmark is claimed. Per-source URLs, retrieval UTC, HTTP status, raw/text hashes and capture hashes are in [this review's source directory](../sources/gpt-product-workflows/). Fetched text was evidence, not instructions.

| Source actually inspected | Date/version | Observation and limit |
|---|---|---|
| [Local subscription page](http://127.0.0.1:8876/subscriptions.html), `incumbent` text and tiles 0000–0002 | Retrieved 2026-10-05; repository implementation | The default 875px-wide capture puts discovery below a large introduction and full wallet panel. This is a current local capture, not a mobile or 1440px test. |
| [GitHub: managing notifications from your inbox](https://docs.github.com/en/subscriptions-and-notifications/how-tos/viewing-and-triaging-notifications/managing-notifications-from-your-inbox), text and tiles 0000–0001 | Retrieved 2026-10-05; no publication date shown in extracted page | Read/unread, Save, Done and Unsubscribe are separate actions. A query can be previewed before saving a custom filter. Documentation with embedded product screenshots, not an authenticated live account. |
| [Feedly: following a feed](https://docs.feedly.com/article/288-how-to-follow-a-feed-in-your-feedly-account), text and tile 0000 | Updated 2024-11-04; retrieved 2026-10-05 | Discover search → Follow → choose folder, across desktop/mobile. The inspected screenshot is a documentation page with historical embedded app images; it does not establish current signed-in layout. |
| [Feedly: finding sources](https://docs.feedly.com/article/287-how-to-find-and-add-follow-sources), text | Updated 2022-07-16; retrieved 2026-10-05 | Discovery searches topics/names separately from reading subscribed content. Old documentation; use the conceptual pattern, not its exact UI or typo-bearing labels. |
| [Feedly: searching within Feedly](https://docs.feedly.com/article/78-how-can-i-search-within-my-feedly), text | Updated 2024-05-09; retrieved 2026-10-05 | Search scope is explicit: all feeds, particular feeds, boards and other content. Supports scoped search rather than a single ambiguous Search field. |

Feedly's documentation index was used to discover those articles; its archive is retained, but it is not additional outcome evidence. Scrapling fetching Google search returned a redirect/error interstitial; rejected as evidence. No logged-in competitor account was inspected. Findings are design inferences, not customer research or conversion measurements.

## Incumbent findings

1. **P1: the landing hierarchy contradicts the default task.** H1 says “Your local inbox”; the full wallet panel appears before Browse streams. The actual capture requires substantial scrolling before the directory. Replace the hero with a compact “Explore feeds” heading, concise persistent demo status and contextual help. Keep the complete wallet disclosure at its actual decision point.
2. **P1: event samples masquerade as feeds.** Nine fixture rows represent six categories. Payment pending, final assertion and reversed each offer the same Subscribe to payments action. The rejected quote is another row. The runtime allows only one category watch. Group accepted/rejected payment/quote examples inside one family preview; rows should represent discoverable scope, not lifecycle states.
3. **P1: preview does not answer the next decision.** Inspect example opens JSON in a details section below the directory, subscriptions and inbox. It provides useful evidence, but no nearby follow decision, folder choice or scope summary. Keep readable example first; evidence and unchanged original JSON second.
4. **P1: “Mark next item reviewed” selects an invisible target.** The global action chooses the first subscription with in-flight work, not an item selected by the person. Keep explicit review on a selected delivered item; display the item title and disposition before commit. Opening or marking it read must not commit that disposition.
5. **P2: organization/search cannot scale.** Search only tests title plus category; there are no folders, saved searches, result counts, scoped update search, stable list anchors or batch organization. Every render replaces the streams/subscription/inbox DOM, so new interactions need stable IDs and deliberate focus restoration.

Preserve the strong boundaries: explicit demo clock and reference provenance; no browser validator; `executes:false`; guard checks on revoked/expired/gapped state; bounded credits; retention-gap acknowledgement; immutable revisions; original occurrences retained during pressure; wallet calls only after explicit actions; no automatic wallet polling.

## Information architecture and vocabulary

Within the existing Subscriptions product section:

- **Discover**: default; catalog search, category/profile-availability facets, previews and following state.
- **Following**: installed canonical family watches with folders and clear runtime status.
- **Folders**: optional single-level organization. One folder per family watch for the first release, including Unfiled. Moving or deleting a folder never pauses, closes or changes a watch. Delete a folder moves its members to Unfiled and offers Undo.
- **Saved searches**: directory queries that find feed descriptions. Saved update queries are named **Saved views** inside Inbox; do not silently mix their result types.
- **Inbox**: delivered occurrences, read/unread/bookmarked presentation and explicit dispositions.
- **Activity**: delivery/processing/checkpoint/retention diagnostics and demo simulation controls.
- **Connections**: optional Moth status and explicit connection actions; separate local permission status.

| Term | Meaning | Product wording |
|---|---|---|
| Feed | Discoverable description of a local selector/scope; synthetic aliases share a canonical family | “Invoice payment observations” |
| Subscription/watch | Local intent installed for a principal with revision, scope, start and delivery bounds | “Following · This demo tab” |
| Update | Delivered occurrence with identity/provenance and disposition | “Payment final assertion · Historical reference” |
| Folder | Personal organization of a family watch | “Move to Finance” |
| Saved search | Named directory query; never installs subscriptions | “Save this search” |
| Saved view | Named query over already accessible local updates | “Save inbox view” |
| Read | Personal reading state | “Mark read” |
| Reviewed | Explicit local processing disposition | “Record review · No effect” |

Avoid “live,” “verified publisher,” “secure,” “approved,” “payment completed,” “synced,” and “healthy” unless the corresponding independent evidence exists. A source assertion of Final remains **Final assertion**, not a guarantee of consensus finality. An offline accepted fixture remains **Reference fixture · Checked offline**, not an authenticated current business source. Mock contracts, credential reminders and operations notices show **Mock-only · No supported business profile**.

## Journeys

**Human.** Discover → search “payment” → preview Invoice payment observations → see pending/final/reversed examples, amounts, reference date and no-effect label → Follow in demo using the visible family scope and default latest start → optionally choose Finance → confirmation keeps the directory in place and offers Open following. Folder is optional; default Unfiled avoids forcing a taxonomy before the person understands their feeds.

**Wallet user.** Browse with a Wallet suggestion preset if desired; that changes discovery filters only. Quotes/payment evidence preview and demo following work without Moth. Connections → reveal current origin, network `preprod`, experimental status and origin-wide capabilities → explicit acknowledgement → Connect Moth → explicit Check wallet status when needed. Connection does not unlock feeds or authenticate a watch owner. Loading/reload/navigation/search never connects, polls, signs or prepares effects. Local disconnect says that revocation still occurs in Moth.

**DApp developer.** Discover or use a payment suggestion preset → preview semantic status plus exact v0.2 profile/contract and unchanged reference JSON → Follow in demo → inspect receipt/provenance and proposed integration notes. Make clear that application watch/read/commit adapters are proposed, not working SDK buttons. Do not call browser display state a finality oracle. Scope changes and callback permission checks are separate from application action policy.

**Agent operator.** Use an approvals suggestion preset → preview candidate, target, budget, named human and expiry → inspect no-tool/no-effect result → follow the canonical approvals family in the demo. A human-provisioned production watch is a future service boundary. Reading notification text cannot widen scope, install tools or authorize an effect. “Record review” does not mean human approved the business action. A separate proposed action contract remains outside this UI redesign.

Presets should be labeled **Suggested for: Everyone / Wallet / DApp / Agent**, not principal selection. Changing a preset must not replace an existing watch's owner, revision, scope, wallet handle or permission. Keep manually changed facets when returning to a view; show an explicit Reset suggestions action.

## Annotated wireframes

Desktop, approximately 1280px and above; dimensions are starting constraints, not tested breakpoints:

```text
Subscriptions                    Browser-local demo · Resets on reload   Connections
┌ 200px navigation ┐ ┌ flexible directory ≥420px ┐ ┌ preview ≈360px ───────┐
│ Discover          │ │ Explore feeds             │ │ Invoice observations │
│ Following         │ │ Search feed names… [label]│ │ Reference fixture     │
│ Folders           │ │ Category [Payments]       │ │ Pending / Final /     │
│   Finance         │ │ Type [All]  Suggested for │ │ Reversed examples     │
│   Unfiled         │ │ [Save search] 12 results  │ │ readable amount/status│
│ Saved searches    │ │                          │ │ Sources: canonical    │
│   Payment feeds   │ │ Invoice observations     │ │ demo payments family  │
│ Inbox             │ │ payment lifecycle summary│ │ Start: Latest         │
│ Activity          │ │ Reference · Following    │ │ Folder: [Unfiled]     │
│                   │ │ [Preview]                 │ │ [Follow in demo]      │
│                   │ │ … rows                    │ │ or Following [Manage]│
│                   │ │ Previous 1/… Next         │ │ Scope / Evidence      │
└───────────────────┘ └──────────────────────────┘ └───────────────────────┘
```

The result title and explicit Preview control open the same adjacent detail. Follow is consistently located in that detail; a row shortcut may reveal the same inline configuration, with no hidden installation. No repeated large fixture disclaimers or metrics cards. Persistent demo status remains visible; scope/evidence detail holds full privacy, clock/hash and validation qualifications. Wallet-specific disclosure appears before wallet acknowledgement, not before ordinary discovery.

At medium widths, keep navigation plus list, and replace the content area with a detail route when opened. On narrow screens:

```text
[Menu] Subscriptions                     [Connections]
Explore feeds
Browser-local demo · Resets on reload [About]
Search feed names…
[Payments ×] [Reference fixtures ×] [Filters 2]
12 results                                 [Save search]
Invoice observations              [Preview]
Reference fixture · payments family
Pending, final and reversed assertions
… list …
[Previous] Page 1 [Next]
```

Preview becomes a full-width content view with **Back to results**. Preserve query, page, scroll anchor and focus target. Its persistent bottom action area contains Follow in demo and optional folder selection, with safe-area space; scope/evidence remain reachable above it. Long JSON scrolls only inside evidence detail, never forces horizontal page scrolling. Avoid treating a phone as a compressed three-pane desktop.

## State contract

Maintain independent stores, even if all are in memory for this demo:

| State | Authority and lifetime | Required behavior |
|---|---|---|
| Catalog descriptor | UI metadata, including `catalogId`, canonical `scenarioFamilyId`, title, taxonomy and example references | An alias never creates another model profile/source identity. Canonical JSON/receipts remain unchanged. |
| Navigation/preferences | UI-only query, facets, sort, page, selected preview, folder memberships and saved searches | Do not become a principal, cursor capability, wallet grant or permission decision. |
| Watch intent | Existing canonical subscription ID, principal, revision, selector, start, bounds and requested state | Only runtime operations change it. One non-closed watch per category remains in this demo. Scope edits create new immutable revisions. |
| Runtime | Permission result, gap, checkpoints, credit/queue state, requested vs effective state | Folder/search/read changes cannot write this store. Paused + gap is representable simultaneously. |
| Reading state | Per-person presentation read/unread/bookmark for a delivered occurrence | Explicit Mark read/Unread is reversible. Preview alone changes nothing. Never advances processing. |
| Disposition | Existing reviewed/quarantined/duplicate states for subscription, revision and occurrence | Only explicit processing commits a decided disposition. Respect contiguous checkpoints and permission guards. |
| Effects | Separate action/effect evidence, currently absent | Always “No effect executed” here. Do not invent success or retry signing. |

Search has two explicit scopes: **Search feeds** searches catalog titles, descriptions, category and disclosed metadata; **Search updates** searches only locally available permitted inbox records, with optional family/folder scope. A no-results message states which scope and active filters caused it. Scope changes do not silently reuse an incompatible query. Searching/organizing sends no selectors to remote topics, telemetry or business routing.

Save search stores a versioned name, query, supported facets, sort and scope. Save changes only that preference. Loading it reruns against currently accessible metadata; it must not auto-follow newly matching feeds. Renaming preserves the query; editing shows Save changes versus Save as new. Removing a search removes no subscriptions. Reject unsupported query syntax with guidance; do not quietly convert a sender expression into executable routing. Plain search plus visible facets is the first-release path; a complex Boolean language is optional later.

**Reload/reset:** retain the incumbent memory-only contract for this release: demo watches, journal, reading state, folders, saved searches and view state clear on reload/reset, with a compact honest notice. If root opts to persist presentation preferences, label that separately and test it; restoring labels or folder assignments must not recreate a trusted watch, grant, wallet connection, disposition or checkpoint. A future durable service must read its journal and reauthorize; browser storage is not that service.

**Pause/resume/close:** Pause stops consumer delivery, not whole-shard intake. Resume checks permission/expiry/retention and keeps gaps visible. Stop following closes the canonical family watch and records a tombstone; prior disclosed records remain. An alias-management action must say it affects every directory alias of that family. Do not offer unrelated folder deletion as a close operation.

**Pressure/gaps:** Activity and Following show orthogonal labels, e.g. “Paused · Retained range waiting” or “Permission expired · 2 disclosed updates.” For retained pressure, offer Recover retained originals in bounded batches. For actual simulated retention, state that no archive exists; do not imply that the recovery button fetches missing history. Accept missing history is a deliberate consequence-bearing action after outstanding work is decided; never a convenient silent jump to latest.

## Copy examples

- Header: “Explore feeds.” Status: “Browser-local demo. Changes clear when you reload.” About: “Examples and permissions are simulated. Following sends no server request. No signing, payment or execution runs.”
- Follow form: “Follow invoice payment observations in this demo.” Scope: “Includes the canonical payments family; catalog scenario labels do not narrow the source.” Start: “New simulated occurrences from now.”
- Alias state: “Already following the payments family. This catalog entry uses the same local watch.” Action: “Manage family subscription.”
- Preview evidence: “Checked offline at the supplied October 4 test clock. Current source, permission and business authority are not verified.”
- Review: “Record review of Payment final assertion.” Consequence: “Updates the local processing disposition. No payment or other effect runs.”
- Gap: “Some history is unavailable in this demo. Review outstanding items, then choose a new start. No archive recovery is connected.”
- Expiry: “Demo permission expired. Further delivery and processing are blocked. Already disclosed updates remain visible.” Action: “Reset demo permissions.”
- Wallet disconnect: “Disconnected locally. This did not revoke the origin grant. Manage that grant in Moth.”

## Acceptance criteria

1. At desktop and 390px-wide mobile, discovery search and at least the first result are visible without scrolling past wallet controls or a marketing hero. A person can search, preview, follow one canonical family and file it without visiting Activity or Connections. Test this flow with first-time and experienced users; do not claim a measured time saving before observation.
2. Render 300 and 1,000 synthetic catalog descriptors with declared scenario-family mapping, long names, duplicate aliases and reference/mock distinctions. These are directory stress cases, not wire-acceptance vectors. Rejected canonical fixtures appear only as preview evidence. All family aliases accurately reflect the same watch state.
3. Use stable sort and 50-row pagination initially. Filtering resets to page one and announces result count; Back restores prior page and anchor. Virtualization is optional only after measurement and assistive-technology testing; hundreds of interactive rows do not require infinite scrolling. No whole-directory DOM replacement may steal focus after following or editing a folder.
4. Measure filtering/sorting/follow feedback on the supplied desktop and a throttled browser: target p95 input-to-paint under 200ms at 1,000 descriptors; record device/browser and timings. Keep raw JSON out of collapsed preview DOM where possible. Do not promote this desktop result into a low-end phone claim.
5. Native controls allow keyboard completion of the whole flow. `/` may focus scoped search outside editable fields; Enter activates the selected preview; Escape closes an overlay and returns focus; optional shortcuts have visible help and never shadow text entry. Selected/result state and runtime status use text, not color alone. Result updates announce counts without reading the whole list.
6. At 320px, 390px, 200% text and long/localized labels, no horizontal page overflow; core actions remain available; touch targets at least 44px. Test focus order and screen-reader names. Physical mobile gestures and real extension dialogs remain manual gates.
7. Folder move/rename/delete, saved search changes, preview, Mark read and Mark unread must leave intent revision, permission, checkpoints, queues and effects byte-for-byte unchanged. Mark read followed by Record review changes only their respective stores. A new delivered receipt may be unread regardless of processing outcome; duplicate handling retains its identity/disposition and cannot create authority.
8. Keep the existing lifecycle tests passing. Add targeted regressions for alias-family following, explicit selected-item review, query/anchor restoration, empty vs unavailable catalogs, and preference/runtime separation. Do not mirror every component with superficial tests.
9. Load/reload/search/follow/preview/preset changes make zero wallet RPC calls. Unsupported API/network/provider change and cancellation remain actionable explicit states. Moth API 4.0.1 connect/getConnectionStatus are the only adapter calls; no autosigning or timer-based status checks.
10. No synthetic catalog label, sender text, persona or saved search widens a grant, becomes a network business topic, changes whole-shard intake scheduling by match result, or prepares a tool/effect. Exports remain deliberately mock-only; production selectors/receipts would need separate disclosure.

## Council candidates, dissent and open decisions

Strong candidates for agreement: directory-first; feed/example distinction; local search and folders; adjacent/full-width preview; separate supporting Inbox/Activity; explicit demo truth; orthogonal read, disposition, coverage and effect states; wallet optional and gesture-bound.

My dissent to watch for: do not use GitHub's Done semantics as a business-processing shortcut, auto-mark read on preview, bulk-commit reviews merely because a list is selected, or restore watches from browser preference storage. Bulk folder operations and read/unread are useful; bulk processing needs its own reviewed atomicity and scope requirements. Avoid a universal green Connected/Healthy badge that collapses wallet, local permissions, delivery coverage and evidence validity.

Open decisions: whether presentation preferences remain entirely ephemeral or are explicitly persisted; whether future trusted feed descriptors support genuinely different source scopes; whether folder membership later becomes multi-folder; and whether complex query syntax is justified by user tests. None blocks improving this demo's discovery hierarchy. This reviewer proposes these positions; only root's synthesis can claim council consensus.
