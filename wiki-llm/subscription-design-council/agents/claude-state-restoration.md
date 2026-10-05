# Durable browser state for the subscription directory

Reviewer: Claude (Opus 5.5), role: stateful UX and durable browser engineer.
Scope: research and proposal only. No product, design-authority, UI-code, existing-document or Git changes were made.
Date: 2026-10-05. Repository head inspected: `7b728b7`.
Sources and probes: `wiki-llm/subscription-design-council/sources/claude-state-restoration/`. Scratch: `/tmp/mpe-subscription-design-council/claude-state-restoration/`.

## Summary

The incumbent page keeps no state at all: nothing is written to any browser store, a reload discards follows, inbox, search and lens, and a second tab sees nothing from the first. The product requirement asks for retained organization between visits without restoring authority. My proposal splits page state into three layers with different lifetimes and different meanings:

- **URL state** for what the user is looking at now (view, search query, filters, selected feed or item, lens). Shareable, survives reload, costs no storage.
- **Saved in this browser** (IndexedDB, synthetic data only) for organization the user built: followed feeds, folders, read and unread marks, saved items, saved searches, recently viewed history and display preferences.
- **This tab's simulation** (memory only, unchanged in principle) for everything the protocol simulation owns: mock permission, watches, intent revisions, journal, delivery and processing cursors, dispositions, gaps and the Moth adapter.

A followed feed is a bookmark, not a watch. After a reload the directory shows "Following" on the feeds the user chose, with "Simulation not running in this tab." A watch exists only after the user starts a simulation, which performs a fresh mock permission check and creates revision 1 from `latest`. Read means "I have looked at it"; it never advances the processing cursor and is never shown as Reviewed.

## Incumbent findings

Inspected by reading `website/dist/subscriptions.{html,css,js}`, `subscriptions-fixtures.json`, `moth-connector.js`, `website/tests/subscriptions.cjs`, by PixelRAG tiles of the live page (three CDP tiles, 875 px wide, viewed), by a Playwright probe (`incumbent-probe.cjs`, result in `incumbent-probe-result.json`) and by a 390 px mobile screenshot kept in scratch. The served HTML hash `3eb81bf4…` matches the repository file.

| Finding | Evidence |
|---|---|
| No persistence of any kind. | After subscribing to payments, ticking twice and reviewing one item: `localStorage` keys `[]`, `sessionStorage` keys `[]`, `indexedDB.databases()` `[]`, `storage.estimate().usage` 0. `subscriptions.js` contains no storage API call. |
| Reload discards everything, including harmless view state. | Before reload: 1 subscription, 2 inbox rows, search `payment`, consumer mode `dapp`. After reload: 0, 0, empty search, `human`. |
| Search and filters are not in the URL. | URL after typing `payment` is unchanged; a search cannot be shared, bookmarked or restored. |
| Tabs are isolated. | A subscription created in tab A does not appear in tab B (same context). This is correct for the simulation, but there is no shared organization either. |
| The directory lists examples, not feeds. | Nine fixture records render as "streams". `Subscribe to payments` appears three times because Payment pending, final and reversed are examples of one category. Subscription identity is the category (`subscriptions.some(s=>s.category===…)`), so there is nothing stable for a follow, folder or read mark to refer to. |
| Search is a substring over title plus category only. | `${f.title} ${f.category}`; description, profile status and validation status are not searched. Zero results render an empty container with no message and no result count. |
| No read or unread concept. | Opening an inbox row leaves its label unchanged (`Payment pending · duplicate suppressed · cursor 2` before and after) and opens a single global `<details>` at the page bottom. |
| "Mark next item reviewed" is not tied to the row the user selected. | The handler takes the first subscription with in-flight work. Reviewing is a processing disposition; there is no lighter "I read this" action. |
| The inbox silently truncates. | `inbox.slice(-40)` with no indication that older receipts exist. |
| Intake always delivers the first fixture of a category. | Second "Simulate intake" on payments produced `duplicate suppressed` for Payment pending; Final and Reversed only arrive through per-row "Simulate this occurrence". |
| The working surface is far below the fold. | At 1440 px the stream list begins at y≈1414, Subscriptions at 3779, Inbox at 4115 (document 4370). At 390 px the list begins at y≈2190 and the inbox at 7039 (document 7294). "Simulate intake" is focusable item 42. |
| An empty status bar covers content. | `#announcement` is `position:sticky`, 40 px, filled `rgb(20,44,53)` while empty; visible over stream text in tiles 0 and 1 and at the bottom of the 390 px viewport. |
| Wallet status begins lowercase. | Tile 0: "disconnected. Local disconnect cannot revoke Moth's origin grant." |
| What is right and must be kept. | Load makes no wallet calls (test asserts `{connect:0,status:0}`); connect requires `userActivation.isActive` and the acknowledgement checkbox; CSP `default-src 'self'`; copy separates delivery, processing and effects; Reset is honest about Moth grants. |

The origin matters for persistence. The PRD notes that the public site shares `CharlesHoskinson.github.io` with other project sites. IndexedDB and Web Storage are scoped to the origin, so every project page on that origin can read and modify whatever this page stores. Stored records must therefore be non-sensitive and must be validated on every read as untrusted input.

## Primary sources inspected

All fetched with Scrapling through `research.py`; robots.txt checked for each domain (MDN disallows only `/api/`, `/*/files/`, `/media`; web.dev and Miniflux allow all; WHATWG disallows snapshot paths only). Fetched text was treated as data.

| Source | Version or date | What I inspected | Used for |
|---|---|---|---|
| MDN, Storage quotas and eviction criteria | last modified 2026-01-05 | Text and PixelRAG tiles 1 and 5 viewed | Best-effort vs persistent; `persist()` prompts in Firefox and is auto-decided in Chromium and Safari; private browsing "stored data is usually deleted when the private browsing mode ends"; Web Storage 5 MiB local plus 5 MiB session; `QuotaExceededError` must be caught; LRU eviction of whole origins; Safari deletes script-created data after seven days without user interaction when tracking prevention is on; eviction deletes "all of its data, not parts of it". |
| WHATWG Storage Standard | Living Standard, last updated 2026-03-15 | Text | Buckets, persistent buckets cannot be cleared without user consent, `persist()` and `estimate()`. |
| MDN, Using IndexedDB | last modified 2026-09-11 | Text, section "Version changes while a web app is open in another tab" | `onblocked` on the upgrading page; `onversionchange` must close the database; prompt to reload. |
| MDN, IDBDatabase versionchange event | last modified 2025-05-02 | Text | Baseline since July 2015. |
| MDN, Web Locks API | last modified 2025-04-03 | Text | Exclusive and shared modes, `ifAvailable`, `steal`; locks span tabs and workers of one origin. |
| MDN, Broadcast Channel API | last modified 2025-02-21 | Text | Same-origin cross-tab messages; no protocol defined, app defines its own. |
| MDN, Window storage event | last modified 2026-08-21 | Text | `localStorage` changes notify other same-origin tabs; `sessionStorage` does not cross tabs. |
| web.dev, Storage for the web | last updated 2024-09-23 | Text only; PixelRAG capture failed (`no close frame received or sent`), rejected as visual evidence | Avoid `localStorage` (synchronous, about 5 MB, strings only); Chrome incognito quota about 5% of disk; about 300 MB when "clear site data on close" is set. |
| web.dev, Best practices for persisting application state with IndexedDB | last updated 2017-06-08 (old; principle still holds) | Text | Do not store the whole state tree as one record; structured clone runs on the main thread; split into records and write only what changed. |
| Chrome for Developers, Page Lifecycle API | last updated 2023-12-01 | Text | `hidden` is often the last reliably observable state, especially on mobile; persist unsaved state there; `unload`, `pagehide`, `beforeunload` may not fire. |
| Miniflux documentation, Keyboard Shortcuts | undated, retrieved 2026-10-05 | Text and PixelRAG tile 0 viewed | Incumbent feed-reader conventions: `g u` unread, `g b` starred, `g h` history, `j`/`k`, `m` toggle read and focus next, `A` mark page read, `f` star, `/` focus search, `Esc`. |
| Miniflux documentation, User Interface Usage | undated | Text | Star/unstar as bookmark distinct from read state. |

Not fetched in this pass and cited from standing knowledge only: WCAG 2.2 SC 2.1.4 Character Key Shortcuts.

A scratch benchmark (`storage-bench.cjs`, `storage-bench-result.json`) ran in a fresh headless Chromium 153 context on an Intel Core Ultra 9 275HX, CPU only, no GPU acceleration claimed. It created and then deleted a temporary database. Results: writing 600 follows, 40 folders and 20,000 read marks in one relaxed transaction 375 ms; reopening 0.3 ms; restoring all follows, folders and the header 3.7 ms; counting one feed's read marks through an index 0.3 ms; reading all 20,000 read-mark keys 34.8 ms; one read-mark write 1.0 ms; 100 searches over 600 titles 2.1 ms; rendering 600 simple rows 14.8 ms. `localStorage` threw `QuotaExceededError` after four strings of 1,048,576 characters. These are upper-end desktop numbers; acceptance criteria below assume a throttled mobile profile.

## Recommended state architecture

### Layers

| Layer | Holds | Lifetime | Survives reload | Shared across tabs |
|---|---|---|---|---|
| URL | `view`, `q`, `family`, `status`, `folder`, `feed`, `item`, `lens` | Address bar | Yes | Only if the URL is copied |
| Saved in this browser (IndexedDB `mpe-subscriptions-ui`) | Follows, folders, read marks, saved items, saved searches, recently viewed, display preferences | Until cleared by the user, evicted by the browser or capped | Yes, best effort | Yes, through BroadcastChannel notifications |
| This tab's simulation (memory) | Mock permission, watches, intents and revision history, journal, delivery and processing cursors, dispositions, gaps, queue and credit counters, export payload | Until reload, Reset simulation or tab close | No | No |
| Moth adapter (memory, existing) | Status, API handle, epoch | Until reload or Disconnect locally | No | No |

The URL wins over saved preferences when both describe the view. A bare `subscriptions.html` restores the last view from `prefs.lastView`; a URL with parameters ignores it. URL updates use `history.replaceState` for typing and filter changes and `pushState` only for moves the user would expect Back to undo (opening a feed or item on mobile).

### What is never persisted

The allowlist below is the complete set of stored record types. Anything not on it stays in memory. In particular, the following never enter IndexedDB, Web Storage, cookies, the URL or exports of saved data:

- The Moth wallet acknowledgement checkbox, status, provider reference, API handle, network or any wallet-returned value. Every connection needs a fresh acknowledgement and a genuine click, exactly as today.
- Mock permission state (`granted`, `expired`, `revoked`), watches, `LocalSubscriptionIntent` objects and their revision history, journal entries, cursors, gaps, dispositions (`reviewed locally`, `quarantined`, `duplicate suppressed`), queue and credit counters.
- Fixture event bodies, contexts and offline receipts. Saved records hold keys that point into the shipped fixtures and catalog; the long canonical records stay immutable in the shipped JSON.
- Keys, secrets, credentials, addresses or anything typed into a free-text field other than search queries and folder names.

The lens (`human`, `wallet`, `dapp`, `agent`) is URL state only. Restoring it from storage would let a returning visitor believe they had been identified as an agent or wallet. In the URL it is visibly a choice of view.

### Stable identities that state can refer to

Durable organization needs keys that survive reload and catalog updates. Without them, a follow is meaningless.

- `feedKey`: `demo:<family>:<slug>`, for example `demo:payments:invoice-acme-eu`. Assigned once in the synthetic catalog and never reused for a different feed. `family` is one of the declared scenario families (`quotes`, `payments`, `approvals`, `contracts`, `credentials`, `ops`); it is local organization, not a network topic.
- `catalogVersion`: integer in the catalog file; changes only when feed keys are added, renamed or removed. A rename maps the old key in a `renamedFrom` list.
- `occurrenceKey`: for v0.2 fixture-backed items, `occ:` plus the JCS of `[event.source, event.id]`, matching the deduplication identity the simulation already uses. For mock-only and synthetic catalog examples, `mock:<feedKey>:<sequence>` with a fixed sequence assigned in the catalog. Mock keys never claim source authentication; they identify a demo row, nothing more.

Catalog feeds at hundreds-scale are synthetic views over declared scenario families. Each catalog entry names which canonical fixture its examples reuse and whether that fixture is a v0.2 offline-checked reference or mock-only. The catalog never asserts that its feeds were accepted on the wire.

### IndexedDB schema, version 1

Database `mpe-subscriptions-ui`, object stores:

| Store | Key | Record (closed; unknown fields reject the record) | Cap and retention |
|---|---|---|---|
| `meta` | `'header'` | `{schema:1, createdAt, catalogVersionSeen, tabWriterId?}` | One record |
| `prefs` | name | `{name, value, updatedAt}`; names allowlisted: `lastView`, `density` (`comfortable`/`compact`), `sort` (`name`/`unreadFirst`/`recent`), `shortcutsEnabled` (boolean), `keepHistory` (boolean), `markReadOnOpen` (boolean) | Allowlist only |
| `follows` | `feedKey` | `{feedKey, folderId|null, followedAt, muted, updatedAt}` | 2,000 records. At the cap, Follow is disabled with a message; nothing is evicted. |
| `folders` | `id` | `{id, name (1–60 chars, trimmed), order, updatedAt}` | 200. Flat, one level. Deleting a folder moves its follows to Unfiled. |
| `readMarks` | `[feedKey, occurrenceKey]`, index `byFeed`, index `byUpdated` | `{feedKey, occurrenceKey, state:'read'|'unread', updatedAt}` | 50,000 or 180 days, whichever is smaller; trimmed oldest-first by `byUpdated` at startup and after bulk marks. Trimming only makes items appear unread again; it never hides content. |
| `saved` | `occurrenceKey` | `{occurrenceKey, feedKey, savedAt, note? (0–280 chars)}` | 1,000. Never auto-evicted; at the cap, Save is disabled with a message. |
| `savedSearches` | `id` | `{id, name, query (URL search string, ≤ 512 chars, parsed through the same allowlist), createdAt}` | 50 |
| `recent` | auto-increment | `{kind:'feed'|'item', key, viewedAt}` | 200 entries or 30 days; not written when `keepHistory` is false. |

Write pattern follows the web.dev guidance: one small record per change, never the whole state. Toggles write immediately in their own transaction with `{durability:'relaxed'}`. `lastView` and density are debounced by 500 ms and flushed on `visibilitychange` to `hidden`, the last reliable lifecycle signal per the Chrome Page Lifecycle guidance.

### Validation and corrupted storage

Every record read passes a closed validator before use: exact field set, types, string lengths, timestamp format, enum values, and for `follows`, `readMarks` and `saved` a `feedKey` grammar check. Records from other pages on the shared origin are possible, so validation does not assume the page wrote what it reads.

- Invalid record: skip it, count it, leave it in place until the user chooses Clear, and show one quiet notice: "Some saved items in this browser could not be read and were ignored." No silent repair that could mask a bug.
- Valid record whose `feedKey` is not in the current catalog (and not in `renamedFrom`): keep it, show it in the Following list under "No longer in the demo catalog" with Remove. Do not delete on load.
- `meta` missing or unreadable while other stores have data: treat the database as corrupted; open in memory mode and offer "Reset saved data".
- `open()` throws, never resolves within 1,500 ms, or `indexedDB` is absent: memory mode.

### Versioned migrations

- Each schema version has one pure migration function `vN → vN+1`, run in order inside `onupgradeneeded` using the upgrade transaction. Migrations may add stores and indexes, rename fields and drop records they cannot convert; they may never invent read marks, follows or saved items.
- Opening with a lower version than stored raises `VersionError`. The page then runs in memory mode with: "These saved items were created by a newer version of this page. Changes in this tab will not be saved." It never downgrades or deletes.
- Every open connection listens for `versionchange`, closes the database, stops writing and shows: "This page was updated in another tab. Reload to keep saving." The upgrading tab handles `blocked` with: "Close other tabs of this page to finish updating saved data."
- Catalog changes do not need a schema migration. `catalogVersionSeen` lets the page show "Feeds were renamed or removed since your last visit" once.

### Multi-tab behaviour

- After each committed write, the tab posts on `BroadcastChannel('mpe-subscriptions-ui')` a message `{type:'changed', store, keys, writerId}` or `{type:'cleared', stores}`. Receivers re-read only those keys and re-render. Messages carry keys, never values, so a forged message can only cause a re-read of validated data.
- Per-record last-writer-wins on `updatedAt` (then `writerId` as a tiebreak). Read marks are idempotent: two tabs marking the same item read converge without conflict.
- Operations that touch many records take the exclusive Web Lock `mpe-subscriptions-ui:bulk`: folder reorder, Mark feed as read, Clear, migration. Single-record toggles do not lock.
- Simulations do not synchronize. Two tabs may each run a simulation; each banner says "This tab's simulation". This prevents two tabs from appearing to share one cursor or one permission check.
- Where `BroadcastChannel` is absent, re-read on `visibilitychange` to `visible`.

### Quota, private browsing and eviction

- All writes are wrapped; `QuotaExceededError` or transaction abort keeps the change in memory, marks the state "not saved", and shows: "This browser refused to save more. Your latest changes last until you close this tab. Clear read history to free space." Read history is the only large store.
- Expected footprint at the caps is roughly 5–8 MB, far under every browser quota MDN lists. `storage.estimate()` is read once per session for the Manage panel and never polled.
- Do not call `navigator.storage.persist()`. Firefox would show a permission prompt for convenience data; Safari and Chromium decide silently. Best effort is the honest level for synthetic preferences.
- Private browsing and "clear site data on close": saving may work and then vanish, or fail. The Manage panel always says "Saved in this browser. Private windows, browser cleanup and Safari's seven-day rule can remove it." No feature depends on saved data surviving.
- Eviction removes the whole origin at once, so partial states are not expected; if `meta` exists, the rest is complete or deliberately cleared.

### Reset and clear

Two separate controls replace today's single Reset:

- **Reset simulation** (existing behaviour, renamed): clears this tab's journal, watches, cursors, dispositions, mock permission back to granted. Keeps follows, folders, read marks, saved items and history. Moth grants are unaffected, as today.
- **Manage saved data** (in the rail footer and in a settings sheet): Clear read history; Clear recently viewed; Remove all follows and folders; Clear everything saved in this browser. Each shows what it removes, takes the bulk lock, deletes, broadcasts `cleared`, and offers Undo for 10 seconds for all but Clear everything (implemented by holding the deleted records in memory). Clear everything calls `deleteDatabase` after closing connections and confirms in an inline panel, not a modal.

### Boot sequence on reload

1. Render the shell and skeleton rows; parse and validate the URL against the allowlist (unknown parameters are dropped from the address bar with `replaceState`).
2. Load `subscriptions-fixtures.json` and the synthetic catalog; open IndexedDB in parallel with a 1,500 ms ceiling.
3. Validate `meta` and the small stores (`prefs`, `follows`, `folders`, `savedSearches`). Read marks load per feed on demand through `byFeed`, plus one count pass for unread badges.
4. Render the view from the URL, or from `prefs.lastView` if the URL is bare.
5. Show the simulation banner: "Simulation not running in this tab. Following a feed does not start delivery." Start simulation runs the mock permission check and creates one watch per followed feed's family at revision 1 from `latest`.
6. Moth panel: Disconnected, acknowledgement unchecked, no calls. Identical to today.

## Interaction pattern and information architecture

Recommended: a three-region directory workspace with smart views, in the familiar feed-reader arrangement (rail, list, reader), with state badges that distinguish browser state from simulation state.

- **Rail**: Directory (all catalog feeds), Following, Unread, Saved, Recently viewed; then the user's folders with unread counts; then This tab's simulation (status, Start/Pause, journal high-water). Footer: "Saved in this browser · Manage".
- **List**: feeds when a directory or folder view is active; items when a feed or smart view is active. Each feed row: title, family, profile status (`v0.2 offline reference` or `Mock only`), follow state, unread count. Each item row: read dot, title, feed, simulation disposition if this tab delivered it.
- **Reader**: the selected feed's description and examples, or the selected item with business data, original example, offline check and the existing authority notice. Actions: Mark unread, Save, Follow feed, Inspect raw.

Rejected alternative: keeping the single scrolling page and adding a "Remember my choices" toggle that serializes the whole page state into `localStorage`. It would store authority-shaped data (permission, cursors, dispositions), rewrite one large string on every change on the main thread, hit the 5 MiB limit the benchmark reproduced, and restore a simulation that claims continuity it does not have. It also leaves the user's real complaint (directory below the fold, no stable feeds) untouched.

Rejected alternative: persisting the simulation and resuming it after reload. Even labelled "mock", a restored `granted` permission and advanced cursors would teach that a browser preference can reconstitute a watch. The PRD allows persisted inbox and read markers only as labelled history, so a later option is a read-only archive (see unresolved decisions), never a resumed watch.

### Desktop wireframe (≥ 1100 px)

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ M/E MIDNIGHT EXPRESS   Overview  Workflows  Architecture  Data model  Subscriptions …  │
├──────────────────────┬───────────────────────────────────┬────────────────────────────┤
│ [/ Search feeds   ]  │ Following › Treasury        12 ▾  │ Invoice evidence · Acme EU │
│                      │ ─────────────────────────────────  │ payments · v0.2 offline    │
│ Directory        612 │ ● Invoice evidence · Acme EU   3  │ reference  [Following ✓]   │
│ Following         34 │   Quote desk · Shares/USD      –  │                            │
│ Unread            19 │ ● Approval queue · reports     1  │ ● Payment final assertion  │
│ Saved              6 │   Contract renewals (mock)     –  │   250.00 USD against       │
│ Recently viewed      │   …                               │   500.00 USD payable.      │
│                      │                                   │   Source-observed status   │
│ FOLDERS              │                                   │   does not prove finality. │
│ Treasury          12 │                                   │                            │
│ Approvals          1 │                                   │ [Mark unread] [Save]       │
│ Unfiled            6 │                                   │ [Inspect original example] │
│ + New folder         │                                   │                            │
│                      │                                   │ Not delivered in this tab. │
│ THIS TAB'S SIMULATION│                                   │                            │
│ Not running          │                                   │                            │
│ [Start simulation]   │                                   │                            │
│                      │                                   │                            │
│ Saved in this        │                                   │                            │
│ browser · Manage     │                                   │                            │
└──────────────────────┴───────────────────────────────────┴────────────────────────────┘
  ● = unread (browser state).  "Reviewed"/"Quarantined" appear only on items this tab's
  simulation delivered, in a separate disposition chip; they are never inferred from read.
  The Moth wallet panel moves to a collapsible section under the simulation block.
```

### Mobile wireframe (390 px)

```
┌──────────────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────────────────┐
│ ☰  Subscriptions      ⌕      │   │ ‹ Treasury            ⋯      │   │ ‹ Invoice evidence     ⋯     │
│ [Directory|Following|Unread] │   │ ● Invoice evidence · Acme  3 │   │ payments · v0.2 offline ref. │
│ ──────────────────────────── │   │   Quote desk · Shares/USD  – │   │ ● Payment final assertion    │
│ Treasury                  12 │   │ ● Approval queue           1 │   │ 250.00 USD against 500.00    │
│ Approvals                  1 │   │                              │   │ USD payable. Source-observed │
│ Unfiled                    6 │   │                              │   │ status does not prove        │
│                              │   │                              │   │ finality.                    │
│ Simulation: not running      │   │                              │   │ [Mark unread] [Save]         │
│ Saved in this browser ›      │   │                              │   │ Not delivered in this tab.   │
└──────────────────────────────┘   └──────────────────────────────┘   └──────────────────────────────┘
  ?view=following                    ?folder=treasury                   ?feed=…&item=…  (pushState)
  Back returns to the previous pane with scroll position and focus restored from history.state.
```

### HTML mock snippet (illustration, not a UI edit)

```html
<aside class="rail" aria-label="Feeds and folders">
  <nav aria-label="Views">
    <a href="?view=directory" aria-current="page">Directory <span class="count">612</span></a>
    <a href="?view=following">Following <span class="count">34</span></a>
    <a href="?view=unread">Unread <span class="count">19</span></a>
    <a href="?view=saved">Saved <span class="count">6</span></a>
    <a href="?view=recent">Recently viewed</a>
  </nav>
  <section aria-labelledby="sim-h">
    <h2 id="sim-h">This tab's simulation</h2>
    <p>Not running. Following a feed does not start delivery.</p>
    <button type="button">Start simulation</button>
  </section>
  <p class="storage-status" role="status">
    Saved in this browser. <a href="?view=manage">Manage</a>
  </p>
</aside>

<!-- Shown only when storage is unavailable or refused -->
<p class="storage-warning" role="status">
  Saving is unavailable in this browser window. Follows, folders and read marks
  last until you close this tab.
</p>
```

The status line uses `role="status"` with text only when something changed; the incumbent's empty 40 px sticky bar is replaced by an announcer that is visually hidden when empty.

## State contract

| State | Location | Restored on reload | Search and filter | Cross-tab | Clear action | Technical disposition |
|---|---|---|---|---|---|---|
| Current view, query, filters, selected feed/item | URL | Yes, from URL | Defines it | No | Navigate | View only |
| Last view when URL is bare | `prefs.lastView` | Yes | Applies stored URL string after allowlist parse | Yes | Clear everything | View only |
| Lens (human, wallet, DApp, agent) | URL `lens` | Only if in URL | Adjusts default family filter | No | Remove parameter | Persona view, not a principal |
| Follow | `follows` | Yes, as "Following" | Following view, folder filter | Yes | Unfollow, Remove all follows | UI bookmark; creates no watch, grant or selector |
| Folder and membership | `folders`, `follows.folderId` | Yes | Folder view | Yes | Delete folder, Remove all | Local organization; not a topic or route |
| Read / unread | `readMarks` | Yes | Unread view, unread-first sort | Yes | Mark unread, Clear read history | Display state; never advances delivery or processing cursors; never shown as Reviewed |
| Saved item | `saved` | Yes | Saved view | Yes | Unsave, Clear everything | Bookmark; not an approval, receipt or effect |
| Saved search | `savedSearches` | Yes | Applies stored URL query | Yes | Delete, Clear everything | View only |
| Recently viewed | `recent` | Yes if `keepHistory` | Recently viewed view | Yes | Clear recently viewed, turn off history | Navigation history, not journal history |
| Density, sort, shortcuts on/off | `prefs` | Yes | Sort only | Yes | Clear everything | Display |
| Mock permission | Memory | No; fresh check on Start simulation | n/a | No | Reset simulation | Simulation authority stand-in |
| Watches, intents, revision history | Memory | No | Disposition filter within this tab only | No | Reset simulation | Simulation control plane |
| Journal, cursors, gaps, credits | Memory | No | n/a | No | Reset simulation | Processing checkpoint ≠ delivery ≠ effect |
| Dispositions (reviewed, quarantined, duplicate suppressed) | Memory | No | "Delivered in this tab" filter | No | Reset simulation | Processing decisions; distinct from read |
| Moth acknowledgement, status, handle | Memory | No | n/a | No | Disconnect locally (does not revoke grant) | Wallet grant is managed in Moth |
| Demo export | Download only | n/a | n/a | n/a | n/a | Mock simulation state; saved-data export is a separate file |

Read-marking rules: opening an item in the reader marks it read when `markReadOnOpen` is on (default on); scrolling past a row does not. "Mark feed as read" marks the items currently known for that feed and offers Undo for 10 seconds. Unread counts are computed from catalog examples plus items delivered in this tab, minus read marks; an item that was never shown cannot be unread in a hidden way.

## Search

- In-memory index built once after catalog load over: title, family, feed description, publisher label, profile status text (`v0.2 offline reference`, `mock only`), and folder name. Tokens are case- and diacritic-folded; matching is prefix-per-token with all tokens required.
- Filters as chips that map one-to-one to URL parameters: family, profile status, Following, Unread, folder.
- Results show a count ("37 feeds match ‘invoice eu’") and a teaching empty state: "No feeds match ‘invoce’. Check the spelling or clear the Payments filter." with Clear filters.
- The query is URL state with `replaceState` per keystroke after a 150 ms debounce; Save search writes the URL string to `savedSearches`.

## Keyboard

Following the Miniflux conventions inspected above, active only when focus is not in a text field, with a preference to turn character shortcuts off (WCAG 2.2 SC 2.1.4):

| Key | Action |
|---|---|
| `/` | Focus search |
| `j` / `k` | Next / previous row in the list (roving `tabindex`, `aria-activedescendant` not required) |
| `Enter` or `o` | Open row in reader; on mobile, push the reader pane |
| `m` | Toggle read/unread, move to next row |
| `s` | Save / unsave item |
| `f` | Follow / unfollow feed |
| `Shift+A` | Mark current feed as read (with Undo) |
| `g d`, `g f`, `g u`, `g s`, `g h` | Directory, Following, Unread, Saved, Recently viewed |
| `?` | Shortcut help |
| `Esc` | Close sheet or return focus to list |

All actions also have visible buttons; shortcuts are accelerators, never the only route. No shortcut starts a simulation, connects Moth or checks wallet status.

## Acceptance criteria

Scale fixture: synthetic catalog of 1,000 feeds over the six declared families, 200 folders, 2,000 follows, 50,000 read marks, 1,000 saved items. Device profile: Chromium with 4× CPU throttling at 390 × 844 and at 1440 × 900.

Performance:
- Directory interactive (first list rows focusable) ≤ 300 ms after fixture and catalog load with restored follows and folders; restoring `prefs`, `follows`, `folders`, `savedSearches` ≤ 50 ms at p95.
- Search keystroke to updated list ≤ 50 ms at p95 for 1,000 feeds; no layout shift of the search field.
- Read, save, follow toggles: visible change within one frame; IndexedDB write off the input path; no long task > 50 ms caused by storage.
- No single IndexedDB write larger than 64 KB during interaction; no whole-state serialization.
- Mounted list rows ≤ 200 at any time (windowing) or `content-visibility:auto` with total DOM ≤ 3,000 nodes at 1,000 feeds.
- No network request is made by any save, restore, clear, search or cross-tab notification (assert request count unchanged, as the incumbent test does for subscribe).

Restoration and authority:
- Follow two feeds, file one into a folder, mark three items read, save one, type a search, reload: all five are restored; URL query is restored; simulation shows Not running; mock permission is not displayed as granted until Start simulation; Moth shows Disconnected with the acknowledgement unchecked and `__walletCalls` remains `{connect:0,status:0}` after reload.
- Dump every IndexedDB record: no field name or value matches `moth|wallet|grant|permission|cursor|revision|disposition|journal|sink|principal|shard`; every record matches the closed allowlist.
- Reading an item never changes `processedCursor` or `deliveredCursor` in the demo export; Mark next item reviewed never changes read state.

Multi-tab and migration:
- Two pages in one context: follow in A appears in B within 500 ms; Clear everything in A empties B and B shows the cleared notice; simulations remain independent.
- Pre-create the database at version 99: page loads in memory mode with the newer-version notice and makes no writes.
- Open v1 in tab A, load a v2 build in tab B: A closes its connection on `versionchange` and shows the reload notice; B completes the upgrade or shows the blocked notice.

Failure handling:
- `delete window.indexedDB` via init script: page works in memory mode with the unavailable notice.
- Stub `IDBObjectStore.prototype.put` to throw `QuotaExceededError`: change stays visible, notice appears, no uncaught error.
- Inject a record with an extra field, a record with an unknown `feedKey`, and a non-object value: page loads, the first and third are ignored and counted, the second appears under "No longer in the demo catalog".
- Mobile 200% text at 390 px: no horizontal overflow (existing test), rail collapses to the segmented control, reader pane reachable by Back.

## Product prose examples

- Directory empty of follows: "You are not following any feeds yet. Follow a feed to keep it here between visits. Following does not start delivery."
- Banner after reload with follows: "Restored 34 followed feeds and your read marks from this browser. Simulation not running in this tab."
- Start simulation button help: "Checks the mock permission and creates local watches for the families you follow, starting after the latest item. Nothing is sent to a server."
- Read vs reviewed, in the reader: "Read in this browser. Not reviewed: review is a separate decision recorded only in this tab's simulation."
- Saved: "Saved in this browser. Saving does not approve, accept or act on this item."
- Feed no longer in catalog: "This feed is no longer in the demo catalog. Remove it from Following?"
- Manage panel: "Follows, folders, read marks, saved items and recent views are stored in this browser for this site. Other pages on the same site address can read them, so nothing sensitive is stored. Private windows, browser cleanup and Safari's seven-day rule can remove them."
- Clear everything confirmation: "Remove all follows, folders, read marks, saved items, saved searches and recent views from this browser? The simulation in this tab and any Moth wallet grant are not affected."

## Recommendations for consensus

1. Adopt the three-layer split (URL, saved in this browser, this tab's simulation) and the allowlist of stored record types; treat anything else as memory-only.
2. Introduce stable `feedKey` and `occurrenceKey` identities in a synthetic catalog over declared scenario families before building follows, folders or read state. The current category-keyed subscription cannot carry them.
3. Separate Follow from Watch and Read from Reviewed in labels, data and tests.
4. Use IndexedDB with per-record writes, closed validation on read, ordered migrations, `versionchange`/`blocked` handling, BroadcastChannel key notifications and a Web Lock for bulk operations. Do not use `localStorage` for organization data and do not request persistent storage.
5. Split Reset into Reset simulation and Manage saved data, with scoped clear actions and Undo.
6. Keep the Moth acknowledgement and status unpersisted; keep the incumbent wallet tests and extend them across reload.
7. Fix the incumbent empty sticky announcer, the silent inbox truncation and the missing empty-search state regardless of the wider redesign.

## Dissent and unresolved decisions

- **Archive of a past simulation.** The PRD permits persisted synthetic inbox items as labelled history. A read-only "Last simulation, 5 Oct 14:20, not running" archive (dispositions and receipts as text, no cursors that could be resumed) is defensible. I recommend deferring it: it doubles the stored surface and invites "why can't I resume this". Reviewers favouring continuity may disagree.
- **Shared origin.** Any page on `CharlesHoskinson.github.io` can read and write this database. The data is non-sensitive, but a hostile sibling page could plant follows or read marks. Validation limits harm to cosmetic state. A dedicated origin, already recommended for production wallet use, would also isolate saved data. Decision for the project owner.
- **Folders versus labels.** I recommend single-membership flat folders plus smart views because they map cleanly to unread counts and keyboard navigation. Multi-label organization is a reasonable alternative if the council's directory reviewers find feeds commonly belong to two workflows.
- **Import of saved data.** Export of follows, folders and saved items as a JSON file is low risk. Import requires the same closed validator plus a preview; I did not specify it and would leave it out of the first iteration.
- **Mark-read-on-open default.** Defaulting on matches feed readers; agents and reviewers may prefer explicit marking so that read state is never accidental. Kept as a preference.
- **Read-mark retention.** 180 days and 50,000 marks are judgement values sized to stay under about 8 MB; no customer data supports them.
- **Benchmark representativeness.** Numbers come from one high-end desktop CPU in headless Chromium. They show the design has headroom; they are not evidence for mobile Safari or Firefox, which need the throttled acceptance runs above.
