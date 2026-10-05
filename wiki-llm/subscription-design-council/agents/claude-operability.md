# Operator experience and error recovery

Reviewer: Claude (Opus 5.5), operability and error-recovery role. This is an independent design proposal for council consolidation. It changes no product code, design authority, existing docs or Git state.

Impeccable mode: **Operate** (the visitor completes a task). Read: `SKILL.md` 4.5.0, `reference/operate.md`, `reference/clarify.md`. Root ran `impeccable context`; I did not rerun it.

## What I inspected

- Code: `website/dist/subscriptions.html`, `subscriptions.css`, `subscriptions.js` (61 lines, 18,610 bytes), `subscriptions-fixtures.json` (9 records), `moth-connector.js`, `website/tests/subscriptions.cjs`.
- Requirements: `docs/product-requirements/pubsub-subscription-experience.md`, `design/subscriptions/README.md`, council `brief.md` and `resolution-draft.md` (to avoid restating settled directory decisions).
- Running incumbent at `http://127.0.0.1:8876/subscriptions.html`: one PixelRAG capture (3 tiles, all inspected) and two Playwright probes (`/tmp/mpe-subscription-design-council/claude-operability/probe.cjs`, `probe2.cjs`) at 1280×900 and 390×844, with 100% and 200% root font size. The probes pressed simulation and lifecycle buttons only. No wallet extension was present and no wallet button was pressed.
- Primary sources: see the table under "Sources". Index with hashes: `sources/claude-operability/index.md`.

## Incumbent findings

Each finding was observed in the running page or read directly in the code. Line numbers refer to `website/dist/subscriptions.js`.

### Task and technical layers are fused

1. **One flat stack, task content far down.** Order is intro → wallet → streams → subscriptions → inbox. Measured page offsets: streams at 1,414 px (desktop) and 2,190 px (mobile); inbox at 4,328 px and 7,039 px. The 390 px first viewport contains no task control. Reaching the first "Subscribe" button takes **19 Tab presses** past wallet controls.
2. **Nine global simulation buttons sit beside user actions** (`#tick`, `#process`, `#negative`, `#duplicate`, `#gap`, `#stale`, `#revoke`, `#reset`, `#export`). "Mark next item reviewed" (a user disposition) looks the same as "Simulate retention gap" (a fault injector). Nothing marks which controls belong to the product and which belong to the simulator.
3. **Technical counters lead the subscription row.** Each row's primary paragraph is `Local predicate all. Revision 1. Delivered cursor 2; processing cursor 0. In flight 2/2; queue 4/4 (632/16384 bytes).` (line 20). Inbox rows are labelled `Title · disposition · cursor N` (line 21). No sentence states what the person should do.
4. **Message detail is a JSON dump** (line 12) inside a `<details>` element at the end of the page, far from the row that opened it (7,039+ px on mobile). It shows `occurrence.source` (`urn:mpe:source:dealer`), the trusted test context, and the full event. That is useful for technical inspection, but it is also the *only* detail view.

### State model defects

5. **Backpressure is reported as a "Replay gap".** When a fourth queued item would exceed credits, `ingest` sets `state='gapped'` with `reason:'missing-range'` and `oldestRetainedCursor:'cursor:demo/000001'` (line 44). Observed text after 7 intake clicks: `contracts · gapped … Replay gap: requested cursor:demo/000006; oldest retained cursor:demo/000001`. Nothing is missing: every original is retained. The row then offers **"Accept gap; start after latest"**. That lets a person discard fully recoverable history in a state that is really "behind". The guard (line 20) only requires decided queued work, not an actual loss.
6. **One field carries three independent facts.** `s.state` holds requested state, authority outcome and coverage. Expire or revoke overwrites every non-closed subscription's `state` (line 53). The row then cannot say "paused and revoked" or "gap and expired". `requestedState` survives, but it is not rendered.
7. **Permission is one global variable** (`permission`, line 4). It cannot represent per-watch expiry. The only way out of `expired`/`revoked` is **Reset demo**, which also erases journal, inbox, revisions and dedup memory (line 54). No path shows the real recovery: a new grant check followed by a new revision.
8. **The routine intake button produces duplicates.** `#tick` ingests `fixtures.find(f=>f.category===s.category)` every time (line 48). From the second click on, every v0.2 subscription receives `duplicate suppressed`. Observed inbox after two clicks: `Shares / USD quote · duplicate suppressed · cursor 2` above `… awaiting review … cursor 1`. Duplicates become the normal outcome of the main demo action.
9. **Duplicates consume delivery credits and human attention.** A duplicate is queued, enters `inFlight` and the inbox, and needs "Mark next item reviewed" before the processing cursor can pass it (lines 25–28, 50).
10. **Duplicates, conflicts and re-evaluations are not distinguished.** The dedup key is `[source,id]` only (line 41), with no content comparison, so a same-ID/different-content conflict would be silently labelled a duplicate. The fixtures contain no such conflict. They do contain a different case. `Expired quote · rejected reference` has an event **byte-identical** to the accepted `Shares / USD quote` (checked: `event` equal). Only the trusted context differs: `now` is 2026-10-05T12:00Z instead of 2026-10-04T12:00Z, so the quote is outside its validity window. The UI says only `quarantined: quote-validity`. It never says "this is the same quote, checked at a later clock". The good guard is that rejected input does not poison dedup (tested). The explanation is missing.
11. **Review is global, not per item.** `#process` takes the first subscription with in-flight work, and from it the oldest item (line 50). Inbox buttons only open detail. A person cannot decide the item they are reading.
12. **Closing orphans undecided items.** `Unsubscribe` empties `queue` and `inFlight` (line 20). Delivered items stay in the inbox as `awaiting review` and can never be decided or relabelled.
13. **Dead controls on terminal or blocked rows.** A closed (tombstoned) row still renders `Pause`, `Unsubscribe`, `Save scope revision` and the category select (observed). Under `expired`, pressing Pause reports `Cannot resume: permission, tombstone or replay gap requires attention.` That is the wrong verb for the button pressed.
14. **One follow per category.** Three payment rows each offer "Subscribe to payments"; the second click says `This category already has a subscription.` The predicate select appears only after `payments` has been *saved*, which turns one edit into two steps.
15. **"Consumer mode" silently changes the Category filter** (line 47). It reads like an identity switch but is a persona preset. That conflicts with "persona is not principal".
16. **Search covers title and category only.** `bank` and `invoice` return 0 results, even though both appear in the readable payment text.

### Feedback, focus and resilience

17. **Focus is lost after almost every action.** `render()` rebuilds `#streams`, `#subscriptions` and `#inbox` with `replaceChildren` (line 14). Measured: after Enter on "Subscribe to quotes" and after Enter on "Pause", `document.activeElement` is `BODY`. APG names exactly this case: when the active element is removed, the browser moves focus to the body, "effectively causing a loss of focus".
18. **One sticky live region carries everything.** `#announcement` (`role=status`, `position:sticky; bottom:0`) is visible even when empty (an empty teal bar appears on every incumbent tile). Each message overwrites the last. Errors, confirmations and fault-injection results share this region. At 390 px and 200% text, one message made it **414 px tall, 49% of the viewport**. In 70 Tab presses I measured no control *entirely* hidden behind it, so SC 2.4.11 did not fail in this run. It is still the sticky-notification shape the WCAG Understanding text warns about.
19. **Reload discards everything silently.** That matches the stated memory-only demo, and the intro says so. The UI still gives no "what you would lose" signal before Reset.
20. **Tests guard semantics well but not operability.** `subscriptions.cjs` asserts guards (revoked blocks pause, scope edits and gap acceptance; recovery preserves paused intent; new-scope checkpoint boundaries; rejected input not poisoning dedup; no wallet RPC on load). These are the right invariants and must survive. It asserts nothing about focus, per-region feedback, read state or reasons shown on blocked actions.

### What the incumbent gets right (keep)

- Explicit gap choice with no silent jump. Recovery preserves occurrence identity and intent revision. Bounded recovery batches.
- Scope edits create revisions and move checkpoints to the revision boundary. History is kept in `intentHistory`.
- Paused intent wins over a gapped runtime: recovery while paused delivers nothing (tested).
- Processing cursor advances only over contiguous decided items. Delivery and processing are separate counters.
- The Moth adapter connects only from a trusted click (`userActivation.isActive`), checks status only on request, and states that the grant is origin-wide.

## Sources

| Source | Version / date | Inspected | Used for |
|---|---|---|---|
| GOV.UK Design System, Notification banner | Live page, retrieved 2026-10-05 | Text; PixelRAG tiles 0 and 2 viewed | "Avoid showing more than one notification banner on the same page"; neutral banners use `role="region"`; success banners use `role="alert"` and move focus |
| W3C WAI APG, Developing a Keyboard Interface | Live page, retrieved 2026-10-05 | Text | When the active element is removed, set focus on the item that follows it, or the browser drops focus to the body |
| W3C, Understanding WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum) | WCAG 2.2 Understanding | Text | Sticky notifications fail if they entirely obscure focus; fixes are scroll padding or making the banner modal |
| GitHub Docs, Managing notifications from your inbox | Live page, retrieved 2026-10-05 | Text; visual capture **failed** (CDP close-frame error) | Read, Unread, Saved, Done and Unsubscribe are distinct verbs with distinct retention |
| IBM Carbon, Notifications pattern | Page states "Last updated Aug 12, 2026" | Text (visual rejected: blank client render) | Inline notifications persist until resolved; toasts are transient; actionable notifications persist until acted on |
| Google Cloud Pub/Sub, Replay and purge overview | Live page (redirected to docs.cloud.google.com) | Text | Replay needs configured retention; snapshot lifetime is bounded (≤ 7 days minus oldest unacked age); seek changes ack state in bulk |
| AWS SQS, Dead-letter queue redrive | Live page, retrieved 2026-10-05 | Text | "All redriven messages are considered new messages with a new messageID" (cited as the pattern to reject) |
| Incumbent page | Working tree at `7b728b7` with local edits | Text; PixelRAG 3 tiles viewed; Playwright probes | All findings above |

Rejected: a GitHub tutorial URL returned 404 (tiles deleted); Carbon visual capture was a blank tile (deleted). The GitHub inbox doc has text evidence only.

## Recommended architecture: two layers, one status voice per feed

The directory-first structure in `resolution-draft.md` stands: Directory → My feeds → Inbox, wallet optional. My recommendation sits inside that structure. It defines how state, permission and recovery reach the person.

### Layer 1: the task layer (default, always visible)

The task layer answers "what is this, am I following it, is anything waiting, what do I do next". It uses:

- the feed name, purpose, declared publisher label and evidence label (`Reference example, checked offline` or `Mock only`);
- one **status line** per followed feed, derived by the precedence rules in the state contract below, in plain words;
- at most **one primary recovery action** per status (Resume, Review waiting items, Catch up, Choose how to continue, Check permission);
- inbox triage verbs: Open, Mark unread, Save, Review, Hold (quarantine).

It never shows cursors, revisions, credit counts, handles (`principal:`, `shard:`, `sink:`, `cursor:demo/…`) or source URNs.

### Layer 2: technical details (progressive disclosure per feed and per item)

Technical details are a disclosure inside the feed panel ("Delivery details") and the item panel ("Original record"). They show:

- Received through item *N* (delivery cursor) · Decided through item *M* (processing cursor) · Effects: none, because this demo prepares no actions. These are three separate lines and are never merged.
- Intent revision and its history: what changed, when (demo clock), and which items were selected under which revision.
- Delivery credits: in flight 2 of 2, waiting 4 of 4, 632 of 16,384 bytes.
- Coverage: the oldest retained item, and the requested start or gap boundary.
- The original record (JSON) with a notice that source labels and display text are not authority.

### Layer 3: the simulation console (fenced)

All fault injectors move into one region headed **"Simulation controls: not part of the product"**. It is collapsed by default on mobile and visually distinct (for example a dashed border and a neutral surface). Per-feed injectors (deliver next example, replay last, retention gap, expire, revoke) act on **the selected feed** rather than on every subscription at once. Global ones stay global: Reset simulation, and Export mock-only state.

Three resets that the incumbent conflates are separated:

- **Reset simulation** clears journal, inbox and runtime. If persistence ships, it keeps folders and saved views.
- **Erase saved local data** removes persisted organization and history. It is a separate, confirmed action.
- **Disconnect wallet locally** is unchanged, keeps its copy, and is never triggered by either reset.

### Rejected alternatives

- **The incumbent single stack with global simulators and one sticky live region.** It fails findings 1, 2, 17 and 18. Per-region inline status replaces it. A single polite live region may still announce outcomes, but it is visually off-screen or non-sticky.
- **Toast-only errors.** Carbon defines toasts as transient. Gap, expiry, revocation and conflict states need persistent inline status that stays until resolved. Toasts are acceptable only for reversible presentation outcomes ("Moved to Finance · Undo").
- **A permission wizard or modal on first visit.** It blocks discovery, and `operate.md` names "modal as first thought" as a product constraint. Permission is disclosed when following and when it changes.
- **Recovery modelled on SQS redrive.** Redrive mints new message IDs. MPE recovery must keep the original occurrence identity and the revision under which an item was selected.
- **An automatic "skip to latest" on gap,** in the spirit of Pub/Sub seek-to-timestamp. A jump is a person's explicit choice that creates a revision. The default never moves a cursor.
- **ARIA `grid` or `feed` for the inbox.** A native list of rows with real buttons and links is enough at hundreds of items with pagination. APG's feed pattern targets infinite scroll and adds reading-mode complexity this surface does not need.

## Wireframes (annotated, not UI edits)

### Desktop (≥ 1024 px)

```
┌ M/E  Overview  Workflows … Subscriptions …                              ┐
│ ⓘ Simulation in this tab. Saved locally: folders, read marks, history.  │  ← one neutral banner (role=region);
│   Delivery and permission are re-checked each visit.  [What's stored]   │    never stacked
├──────────┬───────────────────────────────┬──────────────────────────────┤
│ Directory│ Search feeds  [payment      ] │ Payments · Acme Bank example │
│ My feeds │ Category ▾  Evidence ▾  Clear │ Declared publisher: Acme Bank│
│  Finance │ 38 feeds                      │ (catalog label, not verified)│
│  Ops     │ ┌───────────────────────────┐ │ Reference example, checked   │
│ Inbox  3 │ │ Acme Bank payments        │ │ offline                      │
│  Held  1 │ │ Following · 2 waiting     │◀┼─ status line (derived)       │
│          │ ├───────────────────────────┤ │ ┌──────────────────────────┐ │
│ ──────── │ │ Northwind payments        │ │ │ ⚠ Behind: 2 items waiting │ │  ← inline, persistent;
│ Wallet   │ │ Not following             │ │ │ for review. Nothing lost; │ │    one primary action
│ (optional│ │                 [Follow]  │ │ │ 3 newer items retained.   │ │
│ )        │ └───────────────────────────┘ │ │ [Review waiting items]    │ │
│          │  ‹ Prev  1 2 3 … 10  Next ›   │ └──────────────────────────┘ │
│          │                               │ [Pause] [Edit scope] [Close] │
│          │                               │ ▸ Delivery details           │  ← Layer 2, collapsed
├──────────┴───────────────────────────────┴──────────────────────────────┤
│ ▸ Simulation controls: not part of the product                          │  ← Layer 3, fenced
└─────────────────────────────────────────────────────────────────────────┘
```

### Mobile (390 px, works at 200% text)

```
┌──────────────────────────┐   ┌──────────────────────────┐
│ Subscriptions            │   │ ‹ Back to results        │ ← restores query, page,
│ [Directory|My feeds|Inbox]│   │ Acme Bank payments       │   scroll and focused row
│ Search feeds [payment  ] │   │ Following                │
│ 38 feeds · Filters (1) ▸ │   │ ⚠ Behind: 2 items waiting │
│ ┌──────────────────────┐ │   │ Nothing lost.            │
│ │Acme Bank payments    │ │   │ [Review waiting items]   │
│ │Following · 2 waiting │ │   │ [Pause]  [More ▾]        │
│ ├──────────────────────┤ │   │ ▸ Delivery details       │
│ │Northwind payments    │ │   │ ▸ Example item           │
│ │Not following [Follow]│ │   └──────────────────────────┘
│ └──────────────────────┘ │
│ ▸ Simulation controls    │  ← below results, never sticky
└──────────────────────────┘
```

The first viewport at 390 px must show the search field and at least one result row at 200% text. Wallet moves to My feeds › Wallet (optional) or the page end, never ahead of the directory.

### Feed status panel (HTML sketch)

```html
<section class="feed-panel" aria-labelledby="feed-title">
  <h2 id="feed-title">Acme Bank payments</h2>
  <p class="evidence">Reference example, checked offline. Declared publisher: Acme Bank
     (catalog label, not verified).</p>

  <!-- One status block per feed; persists until the state changes. Not a live region:
       outcome announcements go to a single visually-hidden polite region. -->
  <div class="feed-status" data-status="behind" id="feed-status" tabindex="-1">
    <h3>Behind: 2 items waiting for review</h3>
    <p>Nothing was lost. 3 newer items are kept and arrive after you decide the waiting ones.</p>
    <button type="button">Review waiting items</button>
  </div>

  <div class="feed-actions">
    <button type="button" aria-describedby="pause-note">Pause</button>
    <button type="button">Edit scope</button>
    <button type="button">Close feed</button>
  </div>

  <details>
    <summary>Delivery details</summary>
    <dl>
      <dt>Received through</dt><dd>item 6</dd>
      <dt>Decided through</dt><dd>item 4</dd>
      <dt>Effects</dt><dd>None. This demo prepares no actions.</dd>
      <dt>Scope revision</dt><dd>3 (changed category filter, demo clock 12:00)</dd>
      <dt>Delivery credits</dt><dd>2 of 2 in flight · 4 of 4 waiting · 632 of 16,384 bytes</dd>
    </dl>
  </details>
</section>
```

## State contract

### Orthogonal axes (replace the single `state` field)

| Axis | Values | Persisted? | Who changes it |
|---|---|---|---|
| `requested` | `active` · `paused` · `closed` | Yes, as part of each intent revision | Person (Follow, Pause, Resume, Close) |
| `authority` | `unchecked` · `granted` · `expired` · `revoked` | **Never restored.** It is `unchecked` after every load | Trusted local check (simulated); expiry clock; revocation notice |
| `coverage` | `continuous` · `behind` (credits full, range retained) · `gap-retained` (range retained, needs bounded recovery) · `gap-lost` (range unavailable) | The historical boundary may be stored; after reload it is shown as last known | Intake, retention, recovery, explicit gap acceptance |
| `work` | in-flight, waiting and undecided counts | Undecided items persist as history | Delivery and dispositions |

**Display precedence** (first match wins; each one sentence plus at most one primary action):

`closed` → `revoked` → `expired` → `unchecked` → `gap-lost` → `gap-retained` → `behind` → `paused` → `undecided > 0` ("N waiting") → "Up to date".

Secondary facts appear as a second line ("Also paused", "Also behind"), never hidden. Example: `Permission revoked. Also paused.`

### Item-level state (inbox)

| Field | Values | Meaning | Changes processing cursor? | Allowed without current authority? |
|---|---|---|---|---|
| Read marker | `unread` · `read` | Presentation only. Set on explicit open, never on scroll. "Mark unread" is always available. | No | Yes. The item was already disclosed. |
| Saved | `true` · `false` | Presentation only. A saved item survives history pruning. | No | Yes |
| Folder | a user folder id, or none | Feed-level organization only. Deleting a folder moves its feeds to Unfiled and never pauses or closes them. | No | Yes |
| Disposition | `undecided` · `reviewed` · `held` (quarantine) · `duplicate` · `conflict-held` · `not-reviewed-closed` | Local processing decision | Yes, contiguous only | **No** (except `not-reviewed-closed`, set by Close) |
| Effect | always `none` in this demo | Displayed as a fact, not a status | — | — |

Duplicates and conflicts:

- **Duplicate** means the same declared source, the same occurrence ID and identical canonical content as an item already received under this watch. It is recorded automatically as `duplicate`. It does not consume a review slot, does not appear as a new inbox row, and is shown as "Repeated once; not added again" on the original row. It counts as decided for the processing cursor.
- **Conflict** means the same source and occurrence ID with different content. It is held as `conflict-held` and always needs a person's decision. Neither version is treated as authoritative. No current fixture exercises this. A conflict example needs a new reviewed fixture; it must not be made by mutating the immutable canonical records.
- **Validator rejection** produces `held` with its reason. When the event equals an already-known occurrence and only the trusted context differs (the expired-quote fixture), the hold says so and links to that item. It keeps the incumbent guard: a held rejection does not poison dedup for the accepted record. Whether a validator-held item counts as decided without a human acknowledgement is an open question (see "Unresolved decisions").

### Reload, search and organization

- **Persisted locally** (versioned, labelled "synthetic, this browser"): followed feed intents and their revision history, requested state, folders, saved views (query plus filters), read and saved markers, and inbox history with dispositions.
- **Never persisted:** authority results, wallet connection and handle, the origin-grant acknowledgement checkbox, in-flight credits, announcements, and any wallet RPC result.
- **After reload:** every followed feed shows "Shown from your last visit. Delivery is off until you check permission." A single **Check permission** action on the page runs the *simulated* local check. It never calls Moth. The wallet panel shows "Not connected" and makes no discover or status call (the existing test already asserts no wallet calls on load). Previously in-flight items reappear as "Undecided (from an earlier visit)". Reviewing them requires a granted check.
- **Search state** lives in `history.state` and `sessionStorage`, so Back and Forward and same-tab reload restore the query, filters, page and selected feed. It is **not** written to the URL query or `document.title`, because a user's search terms reveal interests. Deep links, if any, are created only by an explicit "Copy link" and use the catalog's local feed id, never selectors or source handles.
- **Directory search and inbox search** are separate, labelled inputs. Directory search covers name, description, declared publisher label, category and supported profile name. Inbox search covers item title and readable summary within the visible history.
- **Storage failure** (open error, parse error, version mismatch, quota) loads nothing partially. The page shows "Saved organization couldn't be loaded. The directory still works and nothing was deleted." with **Try again** and **Erase saved local data**. A failed disposition write reverts the row and says so. It never reports durable progress.
- **Multiple tabs:** one tab holds the writer lock (Web Locks API). Other tabs read history but show "Reviewing is available in the other open tab" on disposition buttons.

### Source and handle hygiene

- Never render `urn:mpe:source:*`, `principal:*`, `shard:*`, `sink:*` or `cursor:demo/*` in row labels, status lines, announcements, `document.title`, URLs, storage keys or folder names.
- Publisher names come from catalog display labels and always carry "(catalog label, not verified)" on first mention in a panel.
- Handles appear only in **Original record** and in **Export mock-only state**. Export keeps its existing notice and is a deliberate action.

## State-action matrix

Legend: **✓** allowed, with the outcome stated · **⊘** blocked, shown with the reason (`aria-disabled`, focusable, reason in `aria-describedby`) · **—** not shown.

| Display state | Open / unread / save | Review / Hold | Pause | Resume | Catch up / Recover | Start after latest | Edit scope | Close | Check permission |
|---|---|---|---|---|---|---|---|---|---|
| Up to date / N waiting | ✓ | ✓ advances the processing cursor contiguously | ✓ new revision | — | — | — | ✓ only if no waiting or in-flight work, else ⊘ "Decide 2 waiting items first" | ✓ with confirmation listing undecided items | — |
| Paused | ✓ | ✓ for already delivered items | — | ✓ rechecks authority and coverage first | — | — | ✓ same rule | ✓ | — |
| Behind (credits full, nothing lost) | ✓ | ✓ (this is the recovery) | ✓ | — | ✓ "Catch up" enqueues retained items in bounded batches once credits free up | **—** (the incumbent offers it here; remove) | ⊘ "Decide waiting items first" | ✓ | — |
| Gap, history retained | ✓ | ✓ | ✓ | ⊘ "Recover or choose how to continue first" | ✓ bounded batch; same identity and revision; honours Paused | ✓ only after all waiting work is decided; creates a revision | ⊘ | ✓ | — |
| Gap, history lost | ✓ | ✓ | ✓ | ⊘ same | ⊘ "This range is no longer kept anywhere in this demo" | ✓ same guard; copy names the lost range | ⊘ | ✓ | — |
| Permission expired | ✓ | ⊘ "Permission expired. Reviews are paused until permission is granted again" | ✓ (see unresolved decision U1) | ⊘ | ⊘ | ⊘ | ⊘ | ✓ | ✓ simulated grant check → new revision if granted |
| Permission revoked | ✓ | ⊘ same, plus "Queued items won't be delivered" | ✓ (U1) | ⊘ | ⊘ | ⊘ | ⊘ | ✓ | ✓ as above; a regrant never reuses the revoked revision |
| Not checked since reload | ✓ | ⊘ "Check permission to continue reviewing" | ✓ (U1) | ⊘ until checked | ⊘ | ⊘ | ⊘ | ✓ | ✓ primary action |
| Closed | ✓ (history) | — (undecided items become `not-reviewed-closed`) | — | — | — | — | — | — | — |
| Mock-only feed (any state) | as above | ✓ "Reviewed locally; mock only, no source authority" | as above | as above | as above | as above | as above | as above | as above |

Global rules:

- **Stopping is never harder than starting.** Close is always available. Pause is proposed to be always available (U1).
- **Starting needs current authority.** Resume, Catch up, Recover, Start after latest, Edit scope and Review all re-evaluate authority **at activation time**, not at render time. If authority changed since the button was drawn, the action is refused with the reason, nothing is partially written, and focus stays on the button.
- **Closing with undecided items** names the count in its confirmation. The items become `not-reviewed-closed`, never `reviewed`.
- **Reading never requires authority.** Already disclosed information cannot be recalled, and showing it again discloses nothing new.

## Keyboard resilience scenarios (acceptance tests)

Each scenario must also hold with a screen reader running and at 200% text.

| # | Scenario | Expected result |
|---|---|---|
| K1 | Tab to "Follow" on a directory row, press Enter | Focus stays on the same control, now labelled "Following" (or moves to that row's Pause). The row is not rebuilt. One polite announcement: "Following Acme Bank payments. Check permission to start delivery." |
| K2 | Press Enter on Pause | Focus stays on the button, now "Resume". The status line updates in place. |
| K3 | Press Enter on Close feed, then confirm | Focus moves to the feed's status heading (`tabindex=-1`), now "Closed". It never lands on `body`. |
| K4 | Review the selected inbox item | Focus moves to the next undecided item. If none remain, it moves to the "All caught up" heading (APG: the item following the removed one). |
| K5 | A simulated revocation arrives while focus is on Review | Focus is not moved. The button becomes `aria-disabled` with its reason. The feed status block updates. One announcement. |
| K6 | Type in directory search | Focus stays in the input and only the results region updates. The count is announced after 500 ms idle ("38 feeds match"). Escape clears the query on the first press. |
| K7 | Mobile: open a feed, then press Back | Query, filters, page, scroll position and the focused row are all restored. |
| K8 | Activate Catch up repeatedly until done | Focus stays on Catch up while it exists, with the label updated ("Catch up 2 more"). When the range is complete, focus moves to the status heading. |
| K9 | Press Enter twice quickly on Review or Catch up | Idempotent: one disposition, one batch. The second activation re-evaluates the guards and is a no-op. |
| K10 | Tab through the whole page at 390 px and 200% text | No focused control is even partly covered by sticky content. Status is not sticky, or `scroll-padding-bottom` reserves its height (WCAG 2.4.11). |
| K11 | Optional inbox shortcuts (`j`/`k` move, `o` open, `u` toggle unread, `s` save) | Active only while focus is inside the inbox list, can be turned off (WCAG 2.1.4), and announced in the help. **No single-key shortcut** for Review, Hold, Close, Start after latest, Follow or wallet actions. |
| K12 | Reload with followed feeds | Focus starts at the skip link. The first heading in main is followed by the "Shown from your last visit" status. No wallet call is made. |

## Scale and performance acceptance criteria

- **Catalog:** at least 500 synthetic feed descriptors generated from declared scenario families (`quotes-reference`, `payments-reference`, `approvals-reference`, `contracts-mock`, `credentials-mock`, `ops-mock`). Each descriptor references existing canonical fixture records by id and inherits its family's evidence label. **No descriptor claims new accepted wire.** The canonical records stay byte-identical.
- **Per-feed intake honesty:** a v0.2 family feed can deliver only its distinct canonical occurrences (quotes: 1 accepted, plus the same quote re-checked at a later clock and rejected; payments: 3; approvals: 1). After that, "Deliver next example" says "No new reference examples for this feed. Further deliveries would be repeats." Replay is a separate, labelled injector.
- **Rendering:** at most 50 directory rows per page. Input-to-results paint is ≤ 100 ms at p95 on a documented CPU-only device profile (Chromium 4× CPU throttle). Total DOM elements stay ≤ 1,500. A state change replaces only the affected row and panel. Verify this by checking that unaffected row nodes keep their identity (MutationObserver count, or node identity across an action).
- **Inbox history:** 2,000 stored items, paginated or windowed at 50. Unread and Held counts come from an index and are not recomputed by scanning on every keystroke.
- **Network:** zero requests on search, follow, review, recovery or simulation. The existing request-count assertion is extended to these actions.
- **Layout:** no horizontal overflow at 390 px and 200% text (existing test). The search field and the first result row are in the first viewport under the same conditions.

## Plain product copy

| State | Status line | Supporting text | Primary action |
|---|---|---|---|
| Up to date | Up to date | — | — |
| Waiting | 2 items waiting for review | — | Review waiting items |
| Behind | Behind: 2 items waiting for review | Nothing was lost. 3 newer items are kept and arrive after you decide the waiting ones. | Review waiting items |
| Gap, retained | Some items haven't arrived yet | Items 7–9 are still kept. Bring them in a few at a time. | Catch up |
| Gap, lost | Some history is no longer available | Items after item 8 were not kept and can't be recovered in this demo. Items you already have stay here. | Choose how to continue → "Start from newest. This records that items after 8 were not seen." |
| Expired | Permission expired | Items you already received stay readable. New items and reviews are stopped until permission is granted again. | Check permission |
| Revoked | Permission revoked | Waiting items won't be delivered. Items you already received stay readable. | Check permission |
| Not checked | Shown from your last visit | Delivery is off until you check permission. | Check permission |
| Closed | Closed | You won't receive new items. 2 items were not reviewed before closing. | — |
| Duplicate (item note) | Repeated once; not added again | Same declared source, ID and content as this item. | — |
| Conflict (item; no current fixture) | Held: conflicting version | Same declared source and ID as an item you already have, but different content. Neither version is treated as authoritative. | Review |
| Validator hold (expired-quote fixture) | Held by offline reference check | Same quote as "Shares / USD quote", checked at a later fixture clock (5 Oct 12:00). By then it was outside its validity window. | Review |
| Blocked Resume | — | Can't resume: permission was revoked. Check permission first. | — |
| Close confirmation | Close Acme Bank payments? | You'll stop receiving new items. 2 unreviewed items will be marked "Not reviewed: feed closed". Your history stays. | Close feed / Keep following |
| Reset simulation | Reset the simulation? | Clears simulated deliveries, inbox and permission state in this tab. Folders and saved views stay. Your Moth grant is unaffected. | Reset simulation / Cancel |

Glossary, fixed across the surface: **feed** (catalog entry), **follow** (the user verb; the technical term is "watch" or "subscription intent", used in details only), **item** (a delivered receipt), **review** and **hold** (dispositions), **read** (marker), **pause**, **resume**, **close**, **catch up** (recover retained items), **start from newest** (accept gap), **check permission** (simulated local check, never wallet), **revision**. "Consumer mode" becomes **"Example journey: Person · Wallet app · DApp · Agent"**. It sets a visible, removable filter chip and never silently changes filters.

## Recommendations for consensus

1. Split the task layer from technical details. Fence the simulation console. Cursors, credits, revisions and handles move into per-feed "Delivery details" and per-item "Original record".
2. Replace the single `state` with the axes `requested`, `authority`, `coverage` and `work`, plus a published display precedence. Every status line is one sentence with at most one primary action.
3. Distinguish **Behind** (backpressure, nothing lost) from **Gap, retained** and **Gap, lost**. Remove "Start after latest" from Behind.
4. Make Review and Hold per-item actions. Retire "Mark next item reviewed" as a user control (it can stay as a simulator shortcut).
5. Auto-record identical repeats as `duplicate` without a review slot. Compare content, not just source and ID, so a conflict is held for a decision instead of being counted as a duplicate. Explain re-evaluations (same event, later trusted clock) as such.
6. Close turns undecided items into `not-reviewed-closed`. Tombstoned rows show history only.
7. Authority is never restored from storage. After reload, follows show "Shown from your last visit" and need an explicit simulated Check permission. Wallet state is never restored and never polled.
8. Read, unread, saved and folder changes need no authority and never move the processing cursor. Dispositions need current authority, evaluated at activation.
9. Manage focus for every action (K1–K12). Update regions in place instead of calling `replaceChildren` on whole sections. Use one non-sticky inline status per feed, plus one visually hidden polite region for outcome announcements.
10. Keep search terms and source or handle identifiers out of URLs, titles and announcements. Use `history.state` and `sessionStorage` for restoration.
11. Keep every existing semantic test and add operability tests: focus target after each action, blocked-action reasons, read state across reload, no wallet call across reload, and no source handle in visible task text.

## Dissent and unresolved decisions

- **U1. Pause without current authority.** The incumbent blocks Pause when permission is expired or revoked. I recommend allowing it: pausing only reduces delivery, and a person should always be able to stop. It still writes a new intent revision, so the council must decide whether a revision may be recorded while authority is absent. The existing test (`contracts · revoked` remains after pressing Pause) passes either way, because the display precedence keeps "revoked" first.
- **U2. Validator holds and the processing cursor.** The PRD counts "explicit quarantine" as decided. It is unclear whether a validator's automatic hold is explicit enough, or whether a person must acknowledge it before the cursor advances. I lean toward requiring acknowledgement for conflicts and allowing automatic decision only for identical duplicates.
- **U3. URL state vs privacy.** Other reviewers may prefer shareable `?q=` URLs. I recommend against writing search terms or feed selection to the URL by default. An explicit "Copy link" is the compromise.
- **U4. Folders vs labels.** Folders (one per feed) are simpler to restore and announce. Labels (many per feed) fit hundreds of feeds better. Either one is presentation-only and must never change intent revisions.
- **U5. Showing credit counts to people.** I keep in-flight and waiting counts in technical details only. The status line says "2 items waiting". The council may prefer a compact credit meter for DApp and agent journeys.
- **U6. Does Reset simulation keep persisted organization?** I propose yes, with "Erase saved local data" as a separate action. This depends on persistence shipping at all. The current demo is memory-only and the PRD says so.
- **Not addressed** (out of scope for this role): wallet signing or authentication features, network topics, and any claim that browser storage supplies durable journal or database evidence.
