# Independent usability verification

Author: GPT usability verification reviewer. Research date: 2026-10-05. Scope: advisory design and acceptance criteria; no product UI, shared authority documents, canonical fixtures or Git history changed.

The subscription page should open on a searchable feed directory and preserve meaningful synthetic subscription and reading state. Its replacement must first make feeds independently scoped. A directory containing hundreds of aliases for six category watches does not meet the requested experience.

## Approach and evidence

I read `website/dist/subscriptions.{html,css,js}`, `subscriptions-fixtures.json`, `moth-connector.js`, `website/tests/subscriptions.cjs`, the product requirements, `design/subscriptions/README.md` and `PRODUCT.md`. I used Impeccable 4.5.0's Operate, adapt, clarify and optimize guidance: prioritize task access, familiar controls, structural mobile adaptation and measured performance. This is a research review, not the skill's full critique command/detector workflow. The parent already loaded project context; I did not rerun it or create design authority.

Public sources were retrieved exclusively with the council's Scrapling helper. PixelRAG pixelshot 0.4.0 used CDP with one worker; no GPU inference claim is made. I viewed all three incumbent tiles and the first two W3C reflow tiles with the image viewer. The incumbent capture clearly shows the large introduction and optional-wallet material before search, event-shaped cards, and simulation controls above inbox details. The W3C tiles show the 320 CSS-pixel requirement and examples of reflow. Capturing later W3C tiles does not mean I visually inspected them.

| Primary source | Retrieved | Inspected and applied |
| --- | --- | --- |
| [WCAG 2.2 Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | 2026-10-05 20:13 UTC | Text plus tiles 0–1. Preserve content and functionality at 320 CSS pixels; full browser zoom and text enlargement are different checks. |
| [WAI APG Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) | 20:14 UTC | Text. Keep focus visible and predictable; ordinary components use Tab, while composites require deliberate internal focus management. |
| [WCAG 2.2 Understanding Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) | 20:14 UTC | Text. Announce result-count/no-result summaries without moving focus; the result list itself is not a status message. |
| [WCAG 2.2 Understanding Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) | 20:15 UTC | Text. Enlarge text to 200% without losing content or functionality. |

These Understanding/APG pages are explanatory guidance, not a claim that this proposal or the incumbent conforms to WCAG. All fetches returned HTTP 200 with substantive source content; no blocked page was accepted. Per-source raw/text hashes, URLs, retrieval times and capture metadata are in [my source directory](../sources/gpt-usability-verification/). The WCAG pages use the WCAG22 documentation path; publication/version dates were not independently established. Do not attribute a new publication date to the retrieval date.

For local behavioral verification only, I ran the existing browser tests and a separate Playwright script against `127.0.0.1:8876`. This was not external research retrieval. The complete measurements are in [local-verification.json](../sources/gpt-usability-verification/local-verification.json), with a reproducible script beside it. Baseline Git HEAD: `7b728b783e3e8c6672d269bb8e9aa848b85f0046`; JS SHA-256: `1be631c77c883984fc545eeea83041594f3421d86e971cbf418901aa49b9a02c`.

## Incumbent findings

The existing `subscriptions.cjs` passed. It usefully checks no automatic wallet RPCs, lifecycle guards, retained recovery, immutable intent revisions, duplicate/quarantine behavior and mobile overflow. Passing it does not establish directory usability, independent-source identity or persistence.

| Finding | Evidence | Implication |
| --- | --- | --- |
| Directory is below the initial task viewport | At Chromium 153, 1440×900, search begins at y=1304.56 CSS px. PixelRAG independently shows wallet controls before search. | Move directory search and first results into the initial viewport; keep concise simulation context visible and full wallet disclosure with the optional wallet action. |
| Cards represent events, watches represent categories | Nine fixture records; payment Pending/Final/Reversed cards all say Subscribe to payments. Matching and duplicate-subscription checks use category. | Feed identity must be separate from occurrence identity and category. The six-watch limitation is an incumbent defect. |
| Search omits source identity and offers no no-result explanation | Filter matches lowercased title/category only. A deliberately unmatched query leaves `#streams` text empty. | Search should match bounded catalog metadata and clearly explain zero results with reset controls. |
| Follow breaks keyboard continuity | Focus Subscribe to payments, press Enter: `document.activeElement` becomes BODY after full `replaceChildren`. | Update keyed rows, preserve the activating button, or deliberately move focus to the replacement Following control. |
| Every search input rebuilds unrelated sections | `render()` replaces streams, subscriptions and inbox. | Separate directory rendering from runtime/inbox rendering; user typing must not discard focused controls or an open item. |
| Reload discards subscriptions and reading history | Follow payments, reload: “Choose a stream to create a local subscription.” All arrays/maps are memory-only. | Persist meaningful synthetic state; do not restore permission from it. |
| Overflow-only mobile check masks poor task access | At 200% root font, width320 has scrollWidth320 but search y=7734.5; width390 has scrollWidth390 but search y=6252.58. | Test reachable search, controls, focus and decisions, not only document width. These are emulated CSS text-size checks, not physical-device or browser-zoom evidence. |

The current nine-record search is fast: 30 alternating queries produced handler median about 0.2 ms and p95 about 0.3 ms; input-to-second-rAF proxy median about 33.3 ms and p95 about 33.5 ms. Initial DOM count was 154 elements. This is one local headless Chromium run with nine records. Second rAF is a render-opportunity proxy, not INP, physical-display latency, a real mobile benchmark or evidence for hundreds of independent feeds. No large-directory performance result exists yet.

## Recommended directory and wireframes

Use a stable directory route with normal navigation links: Discover, Following, Inbox, and a short Folders list. Category is a facet, never the feed's identity. Consumer persona changes recommendations only when explicitly selected; it does not represent the principal or silently replace an existing search.

Desktop: compact header with “Subscriptions” and “Synthetic demo · saved on this device.” Below it, a persistent search labeled “Search feeds” spans the directory column. Sidebar contains Discover, Following, Inbox and folders. Main column contains Category, Source and Follow status controls, visible applied-filter chips, result count, sort, and 50 rows per page. A row contains feed name, publisher/source display name, one-line purpose, category and evidence label, plus Preview and Follow/Following. A right-side detail panel opens on Preview and contains scope, supported/mock status, sample updates and folder choice. Technical JSON is a separate disclosure in that panel. Simulation scenario controls live in an explicit Demo tools disclosure, not in the default reading path.

```text
Subscriptions                       Synthetic demo · saved on this device
Discover | Following | Inbox        Optional wallet / About this demo
Folders       [ Search feeds: bank invoices_______________________ ]
 Finance      Category [Payments]  Source [Any]  Following [Any]
 Work         [Payments ×]          26 feeds · Sort: Name
              Bank A invoice observations    Payments · Synthetic source
              Pending, final and reversed assertions.  [Preview] [Follow]
              Bank B invoice observations    Payments · Synthetic source
              Same workflow; independently scoped.      [Preview] [Follow]
              Showing 1–26 of 26         [Previous] [Next]
              Preview: source scope, local selector, samples, folder
```

Mobile and enlarged layout: keep the same destinations; a Folders button expands local navigation inline. Search precedes an expandable Filters section with an active-filter count. Rows stack source/evidence under the title; Preview and Follow remain visible without hover. Preview becomes a normal detail route with “Back to results”, preserving query, facets, page and scroll anchor. The browser Back button works. Avoid a full-screen modal as the only way to inspect or follow. Long source IDs wrap in technical detail, while display names remain readable. The optional wallet disclosure keeps the full origin-wide acknowledgment before Connect; opening directory/following/inbox never invokes wallet APIs.

Use a semantic list of feed articles or a native table on desktop, with real links/buttons. Do not casually add `role=grid`: it introduces an application keyboard model and extra verification. Conventional pagination bounds the DOM and provides predictable focus, page position and screen-reader traversal. Infinite scrolling, masonry cards and aggressive row virtualization are rejected as the default because they complicate selection, focus restoration and returning to an item. If later measurements justify virtualization, test it separately with assistive technology and dynamic row heights.

## Feed identity and honest scale fixtures

Introduce a versioned `FeedDescriptor`, separate from event records and `LocalSubscriptionIntent`. It needs stable `feedId`, human-readable title/description, category, source display metadata, exact local binding to shard/profile/contract/source/predicate, supported/mock status, catalog revision, and sample references. Source labels and IDs are not authentication. The descriptor is descriptive; the trusted local service resolves its binding and checks principal permission before installing an intent. Categories, folders and feeds stay local; none become network business topics.

Follow must resolve one stable descriptor and save an immutable binding snapshot with intent revision. A renamed feed preserves its identity. A changed source or profile is a scope change requiring a new explicit intent revision, never a silent catalog refresh. Duplicate detection uses canonical resolved scope for the same principal/sink, not display name or category alone. Whether two distinct named feeds with identical resolved scope intentionally share one watch is an unresolved policy; the UI must disclose the relationship if they do.

An honest 600-entry scenario uses new, declared unsigned `mock.local.v1` feed descriptors and independently scoped synthetic sources. Give each stable mock source its own deterministic occurrence sequence and meaningful metadata. Include duplicate names, long names, zero-sample feeds and different sources in the same category. A smaller six-feed functional core should include at least two payment sources and two approval sources, so isolation is observable before testing scale. Remaining entries may be metadata-only catalog fixtures, clearly marked and not followable until a real mock binding exists. Counting those entries tests discovery, not independent subscriptions.

Do not rewrite canonical quote/payment/approval events to manufacture authenticated sources. Their long fixed-context receipt records remain immutable. Original checked v0.2 examples can be linked as references; changing source or ID invalidates the existing validation evidence. Contract/credential/ops synthetic examples still have no installed production profile. A synthetic source ID never supports a “verified publisher” badge. Directory scale, simulation correctness and production transport are three separate evidence sets.

## Persistence and state contract

Persist a versioned synthetic demo in IndexedDB: stable descriptors, immutable intent revisions and requested state, mock journal occurrences, inbox receipt/disposition records, read flags, saved items, folders and membership, query/facets/sort/page and selected-item ID. Persist occurrence identity and source scope, not a mutable title as the key. Folder deletion moves memberships to Unfiled without unsubscribing; rename changes no scope. Follow under an active Unfollowed facet keeps feedback and focus predictable before the row disappears, with a route to Following.

Read/unread is presentation state. Opening an inbox item can mark it read; “Mark unread” reverses that flag. “Record local review” is a separate explicit disposition action. Neither advances a durable processing checkpoint by itself, grants effects, or asserts consensus finality. A quarantined item may be read while its quarantine remains intact. The processing cursor advances only over contiguous decided dispositions under the runtime rules. Store delivery and processing cursors separately from read flags.

Reload restores historical synthetic inbox contents and organization immediately, with “Saved demo state; delivery needs a fresh simulation check.” Requested active/paused state survives, but runtime permission/coverage is unknown until fresh resolution and expiration/revocation/retention checks. Do not load cached `permission:granted`, a wallet API handle or a principal claim as trusted authority. Resuming the browser's mock session is explicit and creates only local simulation authority. Production needs a trusted principal-bound service and durable journal before delivery resumes. Moth starts locally disconnected and performs no automatic status polling or reconnect; the origin grant may separately remain in Moth.

Validate loaded storage by closed versioned schema, size limits and identity consistency. Treat it as untrusted. On corruption/migration failure, preserve a recoverable snapshot and offer “Start a new demo”; do not silently erase state. On storage failure, show “Changes are only saved for this tab” and keep working memory. Save failures must never show a durable-success claim. Use transactions/revision checks for intent history, inbox disposition and checkpoints; test crashes and stale-tab writes. Session identifiers and mock-only namespace prevent synthetic receipts from becoming production records. Production data sensitivity and durable storage design require separate review.

## Acceptance matrix

These are implementation gates, not claims that the replacement already passes.

| Scenario | Required result |
| --- | --- |
| First visit at1440×900 and390×844 | Directory heading, search, simulation label and first result are available without traversing the wallet introduction. |
| Search by feed title, source name and description | Deterministic expected IDs; normalize case/whitespace consistently. Document whether accents/token order are supported. |
| Combine query + category + source + status | Intersect facets; show chips and result count; clearing one facet preserves the others. Categories within a multi-select facet use documented OR semantics. |
| Query produces0 rows | Announced “No feeds match…” plus clear-search/clear-filters actions. No empty unexplained region. |
| Rapid queries / late asynchronous result | Only latest query updates results; no stale overwrite or duplicate announcement. IME composition is not interrupted. |
| 600-entry directory / page50 | At most50 rendered feed rows; stable count, next/previous navigation, and no hidden full duplicate list. Selected item survives filter/page changes by ID. |
| Two same-category independently scoped feeds | Follow both; inject sourceA occurrence; only A receives it. Unfollow/pause A leaves B unchanged. Two sources with identical titles remain distinguishable. |
| Wrong source or shard | No delivery to the selected feed; no source label alone is accepted as authority. |
| Descriptor source changes after Follow | Existing binding remains unchanged; explicit revision flow shows old/new scope. |
| Alias descriptors with same resolved scope | Relationship disclosed and duplicate policy enforced consistently; aliases do not count as independent functional sources. |
| Follow/Following and folder rename with keyboard | Visible focus remains on the resulting control; announcements identify the affected feed. Tab order stays logical. |
| Preview and Back/Escape | Restore exact triggering row focus and results anchor. Escape closes transient controls without clearing filters. No keyboard trap. |
| Open inbox, mark unread, record review | Three separate state transitions; read toggle does not change delivery/processing checkpoint or quarantine. |
| Reload after Follow, folder move and read change | Restore intent identity/revisions, inbox and organization exactly; runtime authority remains pending fresh checks; wallet RPC count remains0. |
| Permission expires/revokes while open or on reload | Historical disclosures remain visible; new intake/delivery/processing blocked; no automatic jump to latest or erased warning. |
| Gap/backpressure across reload | Preserve earliest outstanding work and explicit missing range. Recovery/accept-new-start are separate actions; paused requested state remains paused. |
| Synthetic duplicate replay | Same source/occurrence retains identity; per-intent deduplication survives reload; mock repeats are not relabeled authentic wire. |
| Storage unavailable, corrupt, oversized, stale-tab write | Explain persistence failure; reject unsafe data and stale intent revisions; no silent reset or trusted-state restoration. |
| 200% text enlargement and browser zoom | Search/facets/preview/follow/inbox/recovery remain operable, labels not clipped, focused controls visible. Test real browser zoom in addition to CSS text enlargement. |
| 320 CSS-pixel reflow and landscape | Ordinary directory content needs only vertical scrolling; narrow details retain every core action and source/evidence label. |
| Screen reader + keyboard pass | Native headings/list structure, complete names, result summary announced once after settled search, current page/folder and Following state conveyed. Verify manually in actual supported AT; automation alone is insufficient. |
| Optional wallet | No automatic connect/status/signing/polling; explicit acknowledgment and genuine Connect click remain required; local disconnect never claims grant revocation. |

Prefer touch targets of at least44×44 CSS px as an internal product target from adaptation guidance; this is not an assertion that every WCAG target-size criterion mandates44px. Sticky headers/status bars must not obscure the focused control, especially with the on-screen keyboard.

## Performance protocol

Measure directory rendering on the replacement's real renderer, not a standalone toy array filter. Use deterministic catalog sizes9/100/600 and a separately labeled5000 stress case. Record browser/version, device/CPU, viewport, font/zoom, throttling, payload sizes, warm/cold storage and exact data fixture hash. Measure input event to results committed and next render opportunity; capture trace for long tasks and layout shifts. Distinguish handler CPU, debounce delay and storage/query delay. Report median/p95/max for at least60 post-warmup interactions, including broad/no-match queries, facet toggles, page changes and preview while updates arrive.

Proposed gates: at most50 directory rows and1500 total document elements including one open preview; no monotonically growing DOM/listeners over100 navigation cycles; p95 settled-query-to-results render opportunity within200 ms at600 descriptors on the documented reference device, including any debounce. Repeat at4× CPU slowdown and report separately; choose the final mobile budget after a physical-device baseline. These budgets are design targets, not measured achievements or formal web-vital conformance. A slow query cannot rerender an entire stored inbox. Render only a bounded inbox page and lazy technical JSON for the selected item.

Delivery scale needs a separate600-watch mock test with independently bound sources, bounded per-watch queues and an aggregate host memory/event/byte budget. Per-watch16 KiB alone does not bound total600-watch allocation. Verify pause/revoke/gap/recovery under fan-out and persisted checkpoints. This remains local synthetic service evidence; production whole-shard recognition cost, repair intake and sealed wire sizes require real integration measurements.

## Product prose and council position

Useful strings: “Search feeds”; “Synthetic source · no live publisher verified”; “Following · Finance”; “No feeds match ‘bank invoices’. Clear a filter or search another source”; “Saved demo restored. Check the simulation before resuming delivery”; “Read” and “Record local review” as separate controls; “Missing history. Recover retained originals or choose a new start.” Detail copy should say “Local source scope” rather than imply a network channel or cryptographic segmentation.

I support directory-first navigation, compact rows, explicit source identity, preview before following, folders as local organization, persistent synthetic inbox/read state, and inline attention states. Keep the incumbent's careful distinctions between receipt, processing, effects and source authority, while moving uncommon technical explanation into relevant detail.

My dissent is against shipping a visual scale demo as a completed subscription redesign: preferences-only persistence and hundreds of category aliases leave the central workflow unimplemented. I also favor pagination over immediate virtualization or an ARIA grid until measured needs justify their interaction costs. Remaining decisions are descriptor trust/discovery ownership, duplicate resolved-scope policy, real private-service persistence and supported browsers/assistive technologies. The next implementation should prove two independent same-category sources and restart-safe reading state before claiming the hundred-feed gate.
