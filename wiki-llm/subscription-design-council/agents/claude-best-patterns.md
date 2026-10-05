# Claude principal design review: subscription directory patterns

Reviewer role: principal design reviewer, independent of the other council reports (not read before writing). Focus: compare primary product patterns (notification inbox, channel sidebar, RSS reader, IDE explorer, event console) and propose an exact, opinionated Operate-mode design for the subscription page. This is a research proposal. It changes no UI code, product documents, design authority or Git state.

Method: read the incumbent HTML, CSS, JS, fixtures, Moth adapter, browser test, product requirement, design README, PRODUCT.md and the council brief; inspected the running page at `http://127.0.0.1:8876/subscriptions.html` with PixelRAG tiles and a scratch Playwright probe (`/tmp/mpe-subscription-design-council/claude-best-patterns/inspect.cjs`, `focus.cjs`); fetched public primary sources with Scrapling through `research.py`. Impeccable 4.5 guidance applied: SKILL.md (Operate mode), `reference/operate.md`, `clarify.md`, `optimize.md`, with `critique.md` and `adapt.md` consulted for structure. Root had already run Impeccable context; it was not rerun.

## Incumbent findings (inspected, not assumed)

Measurements come from the live page at 1440×900 and 390×844, Chromium 1243, 2026-10-05.

**Hierarchy and first viewport**
- The first feed starts at y=1414 px on desktop (viewport 900) and y=2190 px on mobile (viewport 844). Neither first viewport shows any feed. Document height is 4370 px desktop, 7294 px mobile.
- The order is: 80 px hero "Your local inbox." (40 px on mobile), three explanatory paragraphs, then the Moth wallet panel, then the directory. An optional wallet sits above the default workflow the user selected.
- The page has 39 buttons with identical visual weight. 26 of them are in the nine-record stream list. Each record has "Inspect example", "Simulate this occurrence" and "Subscribe to <category>". There are 15 tab stops before the first feed action.
- Nine scenario buttons ("Simulate intake and delivery", "Expire local permissions", "Revoke local permissions", "Reset demo", and others) sit in the same control row style as consumer actions. Simulator controls and user actions are visually indistinguishable.
- `#announcement` is `position:sticky; min-height:2.5rem` and renders as an empty 40 px teal band at the bottom of every viewport before any message (PixelRAG tiles 0–1 and mobile capture). It covers content and announces nothing.

**Feed identity and organization**
- A feed is a category. "Subscribe to payments" appears three times (Pending, Final assertion, Reversed), and all three create the same category watch. A second click says "This category already has a subscription." The page therefore cannot represent distinct feeds, let alone hundreds.
- There are no folders, pins, sections, sort, saved filters or read state. `localStorage` and `sessionStorage` are empty. Reload clears subscriptions, inbox and search (verified). This matches the documented memory-only demo, but it means no organization survives a visit.
- "Consumer mode" (Human/Wallet/DApp/Agent) silently rewrites the Category filter (Agent sets approvals; Human resets to all). The result is a persona lens acting as a hidden filter, and the change is not shown as a removable filter.

**Search**
- Search matches only `title + category`. "invoice" returns 0 results, even though three records use `invoice.v0.2`. `urn:mpe:source` returns 0. Profile, contract, source, description and state are not searchable.
- No result count is shown. A no-match query renders an empty container with no empty-state text.
- Every keystroke calls `render()`, which rebuilds the stream list, subscription cards and inbox with `replaceChildren`.

**State and focus**
- Focus moves to `<body>` after Subscribe (keyboard Enter) and after Pause. Every action re-renders the page.
- Typing one character into search discards an unsaved category change in a subscription's scope `<select>` (it reverted from `ops` to `payments`).
- "Simulate intake" always ingests the first fixture of each followed category. A second tick therefore produces "duplicate suppressed". These duplicates enter the inbox, occupy in-flight slots and must be cleared with "Mark next item reviewed". After three ticks, payments showed "In flight 2/2; queue 1/4; processing cursor 0".
- "Mark next item reviewed" is global. It acts on the first subscription that has in-flight work, not on the item the user is looking at.
- Inbox rows are underlined link-styled buttons containing one string: `title · disposition · cursor N`. They show no feed name, time, read state or grouping. The list is silently truncated to the last 40 (`inbox.slice(-40)`).
- Message detail is a 12,668-character raw JSON `<pre>` inside a `<details>` placed after the inbox. There is no structured summary of meaning, provenance and disposition.
- The subscription card shows always-on scope `<select>` controls next to Pause/Unsubscribe. A scope revision looks like an inline setting rather than a deliberate new revision.
- The wallet status text begins in lowercase ("disconnected.").

**Preserve these incumbent strengths**: no network request beyond static assets during subscribe/intake (verified); explicit-click-only Moth connect with origin-wide acknowledgement; separate delivery and processing cursors; explicit gap choice ("Recover retained originals" vs "Accept gap; start after latest"); immutable scope revisions; quarantined rejected input does not poison deduplication; the `executes:false` detail; 200% text at 390 px without horizontal overflow (existing test).

## Primary sources inspected

All fetched 2026-10-05 (UTC 20:32–20:35) with Scrapling via `research.py`. Text, raw bytes and metadata are under `sources/claude-best-patterns/`. Fetched text was treated as data.

| Source | Version/date shown | What I used | Visual |
|---|---|---|---|
| Incumbent `127.0.0.1:8876/subscriptions.html` | working tree, 2026-10-05 | hierarchy, button inventory, empty sticky bar | PixelRAG CDP tiles 0–2 inspected; plus scratch Playwright screenshots |
| W3C WAI-ARIA APG, Tree View Pattern (`w3.org/WAI/ARIA/apg/patterns/treeview/`) | APG live page, no date in text | keyboard model (arrows, Home/End, type-ahead "recommended … especially for trees with more than 7 root nodes"), distinguishing focus from selection in multi-select | tile 0 inspected: pattern intro, focus vs selection paragraph, examples |
| Grafana docs, Logs in Explore (`grafana.com/docs/grafana/latest/explore/logs-integration/`) | "latest", undated | event-console conventions: deduplication modes (None/Exact/Numbers/Signature), level filter, sort direction, received-count and bytes-processed meta line, TXT/JSON/CSV export | tile 1 inspected: toolbar option table, download, meta information list |
| GitHub Docs, Managing notifications from your inbox | undated | Read/Unread vs Done vs Saved vs Unsubscribe as distinct triage states; `is:unread`, `is:saved`, `is:done` query qualifiers; preview before triage; bulk select | **capture rejected**: tiles 0–1 are blank (render failure). Text only |
| GitHub Docs, Viewing your subscriptions | undated | "audit your subscriptions" as a separate view from the inbox | text only |
| Slack Help, Organize your sidebar with custom sections | undated | personal sections "only visible to you"; drag or menu move; bulk move; "Browse or search a section" finds filtered, muted, read conversations | **capture failed** (CDP "no close frame"); text only |
| Slack Help, Join a channel | undated | browse/search by name or description, preview a channel before joining | text only |
| VS Code Extension API, UX Guidelines: Views | undated | tree view for data; "Don't use tree items as single action items"; welcome views only when necessary, short; limit buttons in views | **capture rejected**: blank tile |
| Miniflux docs, Keyboard Shortcuts and Features | undated | RSS reader shortcuts `g u` unread, `g f` feeds, `j/k`/`n/p` next/previous, `o`/Enter open, `?` help, `+` add subscription | text only |
| Carbon Design System, Data table usage | "Last updated Sep 30, 2026" | toolbar location for search, filter and settings; selection with batch actions; expandable rows; consistent row heights | text only |
| W3C APG, Feed Pattern and Grid Pattern | undated | Page Down/Up article navigation, `aria-busy`/`aria-setsize` for loaded lists; grid only when cell navigation is needed | text only |
| web.dev, content-visibility | published 2020-08-05, updated 2025 | skipping offscreen rendering, `contain-intrinsic-size` | text only |

Accepted visual evidence: the incumbent and two primary sources (W3C APG Tree View, Grafana Explore logs). GitHub and VS Code captures came back blank and are not used as visual evidence. The Slack capture failed. PixelRAG ran CPU-only on the CDP backend; no GPU result is claimed.

## Pattern comparison

| Pattern | What transfers | What does not transfer |
|---|---|---|
| Notification inbox (GitHub) | Read/unread is a view marker, separate from Done/triage. Filter grammar (`is:unread`). An audit-your-subscriptions view separate from the inbox. | GitHub "Done" removes from inbox. In MPE, "Reviewed" is a processing disposition that advances a cursor; it is not a hide action. GitHub's automatic re-subscription on mention has no MPE equivalent. |
| Channel sidebar (Slack) | Personal sections visible only to you. Move one or many items to a section. Browse/search in a section. Preview before following. | "Join" changes membership on a server. MPE follow is a local watch; no server learns it. Slack's unread bold-by-default for every channel creates noise at hundreds of feeds. |
| RSS reader (Miniflux) | Feeds grouped in categories, unread counts per feed and folder, `j/k` reading, `g`-prefixed jumps, `?` help, `+` add. | RSS polls publishers over the network. MPE intake is whole-shard and local; no per-feed fetch exists or may be implied ("Refresh feed" would be a false affordance). |
| IDE explorer (VS Code, APG tree) | Compact tree with folders, collapsible state, type-ahead, item vs action separation, short empty welcome text. | File trees use drag-reorder heavily; drag is optional enhancement here, never the only way. |
| Event console (Grafana) | Dense monospaced log list, sort direction toggle, dedup modes, level-style disposition filter, meta line with received count and bytes, export formats. | Grafana dedup hides lines visually. MPE "duplicate suppressed" is a recorded disposition and must stay auditable. |
| Design-system table (Carbon) | Toolbar with search, filters and settings above the table; row selection with batch actions; expandable rows; one row height. | Pagination is optional; a windowed list with a stable count is better for type-to-filter. |

## Recommended information architecture

**Directory-first, three-region Operate workspace.** One page, three regions, one primary task per region:

1. **Feeds rail** (left, about 17rem): personal organization. Sections "Following", user folders, "Pinned"; and below a divider, "Browse catalog" grouped by declared family (Quotes · rfq.v0.2, Payments · invoice.v0.2, Approvals · agent.v0.2, Contracts · mock, Credentials · mock, Operations · mock). Pattern: APG tree, type-ahead, collapsible groups, counts on the right.
2. **Directory table** (centre, default): every catalog feed matching the current rail selection, query and facets. It uses one-line rows of fixed height with columns Feed, Family, Evidence, Scope, Status and Unread/Awaiting. The toolbar holds search, facet chips, sort and density. Selection checkboxes enable batch "Add to folder…" and "Pin". Batch Follow is deliberately absent (see decisions).
3. **Inspector** (right, about 26rem): the selected feed or item. Tabs: **About** (meaning, scope, example, evidence tier), **Items** (this feed's inbox), **Delivery** (cursor ribbon, queue gauges, revision history, gap decision).

Global regions:
- **Top bar**: page title "Subscriptions"; a one-line simulation banner "Simulation in this tab · synthetic and reference data · no network messages"; a compact "Moth wallet: Not connected" button opening the existing acknowledgement panel as a disclosure (not a modal), with its exact text and controls preserved.
- **View switch** in the centre header: `Directory` (default) · `Inbox` (all followed feeds, item-level) · `Delivery log` (event console across watches).
- **Scenario controls**: a separate, visibly different toolbar row labeled "Scenario controls (simulator, not consumer actions)". It holds Simulate intake, Rejected quote, Replay last, Retention gap, Expire permission, Revoke permission and Reset. It is styled as an outlined dashed strip, collapsed by default on mobile. It does not mix with Follow, Pause or Mark reviewed.

Remove the 80 px hero. Move the two simulation paragraphs into the banner's "What this simulates" disclosure. Remove the persona selector as a hidden filter. Replace it with an "Example journeys" menu in the rail footer ("Wallet: quotes then payments", "DApp: payments", "Agent: approvals for human review"). Choosing one applies visible, removable chips (`family:quotes`) and a one-line note: "Journeys are suggested filters. They are not a principal and grant nothing."

**Rejected alternatives**
- *Marketplace card grid* (App Store style tiles). Rejected: 3–6 cards per viewport cannot support hundreds of feeds. It invites faux-marketing cards and gives no comparable columns.
- *Inbox-first default* (GitHub notifications as landing). Rejected because the user chose the directory as default. The inbox is one switch away and the rail shows unread counts.
- *Single long scrolling page* (incumbent). Rejected: the first viewport shows no feed, and organization, reading and operations compete in one column.
- *Modal follow wizard*. Rejected per Operate guidance ("modal as first thought"). Follow is an inline form in the Inspector About tab.
- *Infinite-scroll feed for the directory*. Rejected: users need a stable total ("612 feeds · 37 match") and Home/End. APG feed suits reading articles, not choosing among records.

## Feed semantics (exact terms)

- **Feed**: a catalog entry with an explicit, distinct local scope `{family, profile, contract, sourceEquals, predicate}` and a human description. Categories/families are browse facets, never network topics.
- **Follow**: creates a local watch intent (revision 1, `requestedState: active`, start `latest`). The confirmation text is: "Following *Dealer 0042 · USD equity quotes*. Selection runs in this tab after simulated intake; no request left this browser."
- **Pin / Folder**: browser preference only. It creates no watch and changes no delivery.
- **Read / Unread**: a browser view marker on an item. It never advances a cursor.
- **Mark reviewed / Quarantine**: processing dispositions that advance the processing cursor contiguously.
- **Evidence tier** (text badge, never colour alone):
  - `Reference receipt`: the five canonical v0.2 records with an offline validator result at the fixed 2026-10-04T12:00Z context. The badge reads "Checked offline at fixed context · live source not verified".
  - `Rejected reference`: the expired quote. Quarantine reason shown.
  - `Mock contract`: contracts, credentials, ops (`mock.local.v1` / `mock-only`).
  - `Synthetic view`: generated catalog entries (below). "No validator receipt for this scope."
- **Status words** for a followed feed: `Following`, `Paused`, `Gap · decision needed`, `Expired`, `Revoked`, `Closed`, `Restored · not active`. Never use "Healthy", "OK", green check icons or a green dot for Following. Following shows two neutral numbers, unread and awaiting decision. Only states requiring a decision get the accent/warning treatment.

**Hundreds of feeds without fake wire acceptance.** Generate a deterministic synthetic catalog (seeded, about 600 entries) from the six declared scenario families. Each entry gets a distinct scope: for example, `rfq.v0.2` × dealer source handle × instrument; `invoice.v0.2` × payer handle × predicate `all|payment-final`; `agent.v0.2` × sandbox target × named human; mock families × team handle. Each synthetic feed's About tab says: "Synthetic view in the *Quotes (rfq.v0.2)* family. Example shown is the canonical reference record; this scope has no validator receipt and no authenticated source." The five canonical receipt records stay byte-identical. Synthetic occurrences reference them by hash; they are never copied with altered fields.

## Wireframes (annotated; not a UI edit)

Desktop ≥ 1200 px:

```
┌ Midnight Express · Subscriptions ─────────────────────────────── [Moth wallet: Not connected ▾] ┐
│ Simulation in this tab · synthetic and reference data · no network messages   [What this simulates]│
├───────────────┬───────────────────────────────────────────────────┬───────────────────────────────┤
│ Feeds      ⌕  │ Directory | Inbox | Delivery log                  │ Dealer 0042 · USD equity quotes│
│ ▾ Following 3 │ [⌕ Search feeds, profiles, sources…   /]  612 · 37 │ Quotes · rfq.v0.2 · Synthetic  │
│   Payments… 2•│ [family:quotes ×] [is:unfollowed ×] [+ Filter]     │ [About] Items  Delivery        │
│   Approvals 1 │ Sort: Name ▾   Density: Compact ▾                  │ Scope                          │
│ ▾ Treasury  4 │ ☐ Feed                Family  Evidence   Status    │  source  urn:mpe:source:d-0042 │
│ ▸ Pinned    2 │ ☐ Dealer 0042 · USD…  Quotes  Synthetic  —         │  profile rfq.v0.2 · sha256:8b5c…│
│ ─────────────  │ ☐ Dealer 0043 · USD…  Quotes  Synthetic  Following │  predicate all                 │
│ Browse catalog│ ☐ Shares / USD quote  Quotes  Ref. receipt —       │ Example (canonical record)     │
│ ▸ Quotes   104│ … windowed rows, fixed 36px …                      │  100 Share · 123.45 USD/Share  │
│ ▸ Payments  98│                                                    │ [Follow feed]  [Pin] [Folder ▾]│
│ ▸ Approvals 77│ 3 selected: [Add to folder…] [Pin] [Clear]         │ Follow creates a local watch.  │
│ Example journeys▾│                                                 │ Pin and folders are preferences│
├───────────────┴───────────────────────────────────────────────────┴───────────────────────────────┤
│ Scenario controls (simulator, not consumer actions) ┆ Simulate intake ┆ Retention gap ┆ Expire … ┆ │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
 status line (aria-live, no reserved empty band): "Following Dealer 0042 · USD equity quotes."
```

Annotations: `•` marks "decision needed" (gap/expired), not unread. Rail counts show unread, with awaiting-decision appended (`2 · 1 to decide`). Inspector Delivery tab:

```
Journal high-water 12 ── Received through 9 ── Decided through 7
In flight 2 of 2 · Queued 1 of 4 · 8.5 of 16 KiB          Revision 3 (since cursor 6)
Delivery and decision positions are local progress. Neither is an effect or ledger finality.
[Pause delivery]   [Edit scope… (creates revision 4)]   [Close feed]
```

Mobile ≤ 640 px: a single column with a bottom segmented control `Feeds | Directory | Inbox | Delivery`. The rail becomes the Feeds screen. The Inspector opens as a full-height pushed view with a Back button, not a modal. The toolbar collapses to search plus a "Filters (2)" button. Scenario controls collapse behind "Scenario controls" at the end of the Directory screen. At 640–1199 px the rail collapses to a toggle button and the Inspector overlays the right half.

```
┌ Subscriptions        [Wallet ▾]┐
│ Simulation · no network msgs   │
│ [⌕ Search feeds…   ] [Filters 2]│
│ 37 of 612 feeds                │
│ Dealer 0042 · USD equity quotes│
│ Quotes · Synthetic · —         │
│ Payment final assertion        │
│ Payments · Ref. receipt · Following · 1 unread │
│ …                              │
├────────────────────────────────┤
│ Feeds │ Directory │ Inbox │ Delivery │
└────────────────────────────────┘
```

Row snippet (semantic shape only):

```html
<table class="directory" aria-label="Feeds" aria-rowcount="612">
  <thead><tr><th scope="col"><input type="checkbox" aria-label="Select all 37 matching feeds"></th>
    <th scope="col" aria-sort="ascending">Feed</th><th scope="col">Family</th>
    <th scope="col">Evidence</th><th scope="col">Status</th></tr></thead>
  <tbody>
    <tr aria-rowindex="14" aria-selected="true">
      <td><input type="checkbox" aria-label="Select Dealer 0042 · USD equity quotes"></td>
      <th scope="row"><button type="button" class="row-open" aria-controls="inspector">Dealer 0042 · USD equity quotes</button>
        <span class="scope">urn:mpe:source:dealer-0042</span></th>
      <td>Quotes <span class="profile">rfq.v0.2</span></td>
      <td><span class="tier tier-synthetic">Synthetic view</span></td>
      <td>Not followed</td>
    </tr>
  </tbody>
</table>
```

## State contract

**Persisted in the browser** (single key `mpe.subscriptions.prefs.v1` in `localStorage`, versioned, schema-checked on load; an invalid or unknown version is discarded with the notice "Saved layout from an incompatible version was ignored."):

```json
{ "version": 1,
  "catalogSeed": "scenario-catalog-2026-10-04",
  "folders": [{"id":"folder:treasury","name":"Treasury","feedIds":["feed:syn/invoice/payer-0007"]}],
  "pinned": ["feed:ref/payments-final"],
  "collapsed": ["browse:approvals"],
  "view": {"mode":"directory","sort":"name","density":"compact"},
  "followHistory": [{"feedId":"feed:syn/rfq/dealer-0042","lastRevision":3,"lastRequestedState":"active","endedBy":"reload"}],
  "readMarkers": {"feed:ref/payments-final": ["[\"urn:mpe:source:payer\",\"event:payment-final\"]"]}
}
```

**Never persisted or restored**: permission state, wallet connection or grant, the Moth handle, runtime cursors, queue contents, the journal, in-flight items, gap decisions or revisions as active state. Exports remain the explicit "Export mock-only demo state" download.

**Reload behaviour.** Folders, pins, collapse, sort and density return silently. Previously followed feeds appear under Following as `Restored · not active` with the text: "Followed in an earlier visit. The simulated journal from that visit no longer exists, so delivery cannot continue from its cursor. [Follow again from latest] keeps your folder and starts a new watch revision; earlier items are history only." Restored read markers apply only to history labeled "From an earlier visit · history only". The wallet always shows "Not connected" on load, with no discovery or status call.

**URL state.** Query, facets and selected feed go in the hash fragment (`#q=dealer&family=quotes&feed=…`), not the query string. On a static host the query string reaches server logs; the fragment does not. Interest-revealing selectors stay in the browser, though they remain in local history. The hash is updated with `history.replaceState` to avoid history spam.

**Search.** Client-side index over title, description, family, profile id, contract commitment (prefix match ≥ 6 hex), source handle, folder name and status. The grammar mirrors GitHub qualifiers: `is:following`, `is:unread`, `is:decision`, `is:pinned`, `family:payments`, `tier:receipt|rejected|mock|synthetic`, `in:"Treasury"`. Chips and grammar stay in sync. Matching is case-insensitive and tokenised, with a highlighted match. The empty state distinguishes "No feeds match *invoice final*. [Clear search] [Show all families]" from "No feeds in Treasury yet. Add feeds from the directory with Add to folder." The result count is announced via the polite live region about 400 ms after typing stops.

**Folders.** A feed may be in many folders (labels, Slack-section-like) but appears once per folder. Deleting a folder never unfollows: "Delete folder Treasury? 4 feeds stay followed and remain in Following." Undo is preferred over confirmation for folder edits.

**Read / unread / decision.** Opening an item in the Inspector marks it read after 1 s visible or on explicit `m`. "Mark unread" exists. Unread counts are computed only over the reading inbox. "Duplicate suppressed" dispositions go to the Delivery log with a count ("1 duplicate suppressed"); they do not appear in the reading inbox and never count as unread. They still record a disposition and still advance the processing cursor when decided, as now. "Mark reviewed" acts on the selected item and is disabled with a reason when the item is not the next undecided item: "Decide cursor 7 first; decisions advance contiguously."

**Technical dispositions → display**

| Runtime disposition | Inbox label | Detail line |
|---|---|---|
| `awaiting review: offline reference only` | Awaiting review | Reference record checked offline at fixed context; not actionable here. |
| `awaiting local processing` | Awaiting review | Mock or synthetic item; no model validation. |
| `reviewed locally; no effect executed` | Reviewed | Reviewed in this tab. No action ran. |
| `quarantined: <reason>` | Quarantined · <reason> | Refused by the offline validator at fixed context. |
| `duplicate suppressed` | (Delivery log only) | Same source and occurrence id already received for this watch. |

**Focus and rendering.** Use keyed incremental updates (no whole-page `replaceChildren`). After Follow, focus stays on the Follow button, which becomes "Following ▾". After Pause, focus stays on the toggled button. Unsaved scope edits live in an explicit "Edit scope" draft that survives unrelated renders.

## Acceptance criteria

Scale and performance (Playwright, CPU-only, 4× CPU throttle, synthetic catalog):
- AC-SCALE-1: at 600 feeds, a search keystroke reaches the next paint in ≤ 50 ms (p95 over 30 keystrokes). At 5,000 feeds, ≤ 100 ms. INP ≤ 200 ms for Follow, Pin and folder actions.
- AC-SCALE-2: directory DOM row count ≤ visible rows + 20 overscan at any catalog size. Total DOM nodes ≤ 2,500 at 5,000 feeds.
- AC-SCALE-3: initial directory render ≤ 300 ms after fixture load at 600 feeds. No layout shift when the status line updates (no reserved empty band; CLS < 0.1).
- AC-SCALE-4: the five canonical receipt records are byte-identical (SHA-256 match) after catalog generation, follow, export and reload.

Keyboard and accessibility:
- AC-KB-1: `/` focuses search; `Esc` clears it, then returns focus to the list. `↑/↓` move the directory row; `Home/End` jump; `Enter` opens the Inspector; `f` toggles Follow on the open feed only after confirmation focus; `j/k` move inbox items; `?` lists shortcuts. Single-character shortcuts can be turned off (WCAG 2.1.4; the criterion is cited from knowledge, not fetched in this pass).
- AC-KB-2: the rail is an APG tree with arrows, type-ahead and `*` to expand siblings. In multi-select, selection is visually distinct from focus.
- AC-KB-3: after every Follow, Pause, Resume, Pin, folder move, Mark reviewed and scenario control, `document.activeElement` is the invoking control or its logical successor, never `<body>`.
- AC-KB-4: from page load, the first directory row is reachable in ≤ 5 Tab presses (incumbent: 15 to the first feed action).
- AC-A11Y-1: at 390 × 844 and 200% text, no horizontal overflow and no control under 44 × 44 CSS px on touch. Evidence tier and status are text, not colour alone.

Hierarchy:
- AC-IA-1: at 1440 × 900 and 390 × 844, at least 10 (desktop) / 4 (mobile) directory rows are visible in the first viewport with no scroll.
- AC-IA-2: scenario controls are in a separately labeled region (`role="region"`, name "Scenario controls") and visually distinct. No consumer action shares their container.
- AC-IA-3: no element in the initial view uses status words "Healthy", "OK", "All good" or a green success treatment for an active watch.

State truth:
- AC-STATE-1: reload restores folders, pins, sort, density and hash query. Previously followed feeds show `Restored · not active`. Zero watches are active, permission shows its default, and the wallet shows Not connected with `__walletCalls` `{connect:0,status:0}`.
- AC-STATE-2: Follow, search, folder edit and reload make zero network requests beyond the initial static assets. Nothing is placed in the URL query string.
- AC-STATE-3: marking read/unread never changes `deliveredCursor` or `processedCursor` in the export. Mark reviewed changes only `processedCursor`, contiguously.
- AC-STATE-4: "duplicate suppressed" items never appear in the reading inbox or unread counts, and they remain in the Delivery log and export.
- AC-STATE-5: a typing burst in search does not discard an open scope-edit draft.
- AC-STATE-6: all existing `website/tests/subscriptions.cjs` lifecycle assertions keep passing (gap recovery, paused-gap precedence, revision-boundary checkpoints, revoked/expired blocks, quarantine non-poisoning, explicit-click wallet).
- AC-STATE-7: deleting a folder leaves follows unchanged. Closing a feed records a tombstone and keeps its folder membership marked "Closed".

## Plain product prose (examples)

- Banner: "Simulation in this tab. Feeds, permissions and delivery are synthetic or offline reference data. Nothing is sent over a network."
- Follow help: "Follow creates a local watch. Selection would run on this device after authorized whole-shard intake; the demo simulates that intake."
- Synthetic feed: "Synthetic view in the Payments (invoice.v0.2) family. No validator receipt exists for this scope."
- Gap: "Delivery stopped at cursor 6. Cursors 7–9 are still retained. Recover them in bounded batches, or accept the gap and start after cursor 12. Accepting creates revision 4."
- Expired: "Local permission expired at 13:00. No new items will be received or decided until permission is granted again."
- Restored: "Followed in an earlier visit. That visit's simulated journal is gone, so this feed is not active."
- Wallet: "Moth wallet is optional and separate from feeds. Connecting does not grant or change any subscription."
- No results: "No feeds match *invoice final*. Search covers names, families, profiles, sources and folders."

## Consensus recommendations (proposed criteria for the root)

1. Directory table is the default centre view, with an organization rail and a three-tab Inspector. No hero; the first viewport shows feeds.
2. Feed equals a distinct explicit scope. Category/family is a facet. Hundreds of feeds come from a deterministic synthetic catalog labeled `Synthetic view`, and the canonical receipts stay immutable.
3. Four distinct verbs and states: Follow (watch), Pin/Folder (preference), Read (view marker), Review/Quarantine (disposition). Each is tested so it cannot change another's state.
4. Simulator controls are moved into a labeled, visually distinct region.
5. Persist preferences only. Restored follows are explicitly inactive. No permission, wallet or cursor restoration.
6. Search covers profile, contract, source, folder and status with a qualifier grammar, a result count and distinct empty states. View state lives in the URL fragment only.
7. Keyed rendering with focus retention, windowed rows, and the AC-SCALE and AC-KB thresholds above as merge gates.
8. Status vocabulary avoids generic green health. Only decision-needed states draw attention.

## Dissent and unresolved decisions

- **Can synthetic feeds be followed?** My position: yes, as mock watches whose occurrences are labeled synthetic, so scale is exercised end to end. The alternative is browse-only synthetic feeds, which is safer for truth but leaves Following and Inbox untested at scale. Root decision needed.
- **Selector profile for synthetic feeds in a v0.2 family**: use the real profile commitment with a synthetic `sourceEquals` handle, or `mock.local.v1`? The schema closes the profile list; the first option uses real commitments for unauthenticated sources. I lean toward `mock.local.v1` plus a display-only `family` attribute, to keep the closed contract honest. This needs design README authority.
- **Persisting `followHistory` at all.** A stricter view stores only folders and pins, so a reload shows no trace of earlier follows. My view: the restored-inactive state teaches the authority boundary better than silent loss. Real selectors reveal interests, so this needs a visible "Forget this browser's saved layout" control.
- **Batch Follow.** I excluded it, because each watch is a separately scoped intent and a 40-feed batch follow invites over-subscription (GitHub's own guidance recommends auditing subscriptions). Others may want it for scale testing.
- **Single-key shortcuts** (`f`, `j/k`, `m`) versus modifier-only: on by default with an off switch, or off by default?
- **Tablet (640–1199 px)**: overlay Inspector vs two-pane with collapsible rail; it needs a usability check.
- **Hash-fragment state** leaves interest terms in local browser history. Some reviewers may prefer no URL state.

Scratch artifacts (not deliverables): `/tmp/mpe-subscription-design-council/claude-best-patterns/` holds `inspect.json`, `desktop-*.png`, `mobile-*.png` and the probe scripts.
