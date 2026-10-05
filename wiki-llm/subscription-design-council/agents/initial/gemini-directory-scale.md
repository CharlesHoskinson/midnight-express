# Subscription Design Council: Gemini Directory & Scale Review

## Precise Incumbent Findings

Based on visual inspection of the incumbent dashboard (`http://127.0.0.1:8876/subscriptions.html`, captured via PixelRAG CDP tiles on 2026-10-05):
- The "Browse streams" section presents a flat, unpaginated stack of large UI cards.
- Search and categorization rely on three basic dropdowns/inputs stacked above the list.
- Each stream card redundantly repeats verbose metadata ("Historical offline quote", "Reference fixture") and exposes three generic buttons (Inspect, Simulate, Subscribe).
- The "Subscriptions" and "Inbox and quarantine" sections are detached from the browse experience, making context switching difficult when managing multiple streams.
- **Scale Deficiencies:** The flat card layout cannot accommodate hundreds of distinct feeds. The visual hierarchy lacks scannability. State information (subscribed vs unsubscribed, read vs unread) is not mapped directly to a persistent, compact catalog entry.

## Primary Sources & Provenance

1. **Incumbent:** `http://127.0.0.1:8876/subscriptions.html` (Local Demo). Inspected text and 3 generated image tiles via PixelRAG Scrapling on 2026-10-05.
2. **VS Code Extension API - Views UX Guidelines:** `https://code.visualstudio.com/api/ux-guidelines/views`. Inspected text via Scrapling on 2026-10-05 (Visual capture failed due to CDP connection closure, text retrieved successfully).
3. **Material Design 3 - Lists:** `https://m3.material.io/components/lists/overview`. Inspected text and 1 generated image tile via PixelRAG Scrapling on 2026-10-05.

## Information Architecture & Interaction Pattern

**Recommended Pattern: IDE-Style Navigational Drawer & Virtualized Master-Detail**
- **Sidebar (Left):** Navigational hierarchy containing "Pinned Feeds", "Custom Folders", and "Category Directory" (Quotes, Payments, Approvals, Contracts, Credentials, Ops).
- **Master List (Center):** A virtualized catalog of feed rows. Each row is a compact horizontal strip prioritizing: 1) Unread presence indicator (boolean, not a count), 2) Source/Profile semantic icon, 3) Stable feed identity (Title), 4) Reusable profile family text, 5) Trailing quick-actions (Pin, Subscribe).
- **Detail Panel (Right / Overlay):** Clicking a feed row opens the specific stream's details, simulation controls, and its dedicated inbox/quarantine.

**Rejected Alternative:**
- *Card-based Masonry or Grid:* Rejected because large catalogs require rapid vertical scanning. Grid layouts break the reading pattern and consume too much vertical space per item, making a 500-item catalog unnavigable.

## Annotated Desktop/Mobile Wireframe Snippet

```html
<!-- Desktop: Sidebar + Master-Detail -->
<div class="layout-app grid-cols-[240px_minmax(320px,1fr)_400px]">
  
  <!-- Sidebar Navigation -->
  <aside class="sidebar-nav overflow-y-auto">
    <div class="nav-section">
      <h3 class="nav-header text-sm font-semibold">Pinned</h3>
      <ul class="nav-list">
        <!-- Unread indicator (boolean dot), no decorative counts -->
        <li class="nav-item has-unread flex items-center gap-2">
          <span class="indicator-dot bg-blue-500 w-2 h-2 rounded-full"></span>
          <span class="icon text-gray-400">★</span> 
          Dealer Quotes
        </li>
      </ul>
    </div>
    <div class="nav-section">
      <h3 class="nav-header text-sm font-semibold">Catalog</h3>
      <ul class="nav-list">
        <li class="nav-item">Quotes (120)</li>
        <li class="nav-item">Payments (85)</li>
      </ul>
    </div>
  </aside>

  <!-- Feed Catalog (Master List) -->
  <main class="feed-catalog flex flex-col">
    <header class="catalog-toolbar p-4 border-b">
      <!-- Search supports facets like source:bank or status:subscribed -->
      <input type="search" class="search-input w-full" placeholder="Search feeds... (e.g. source:bank)" />
    </header>
    <!-- Virtualized container for hundreds of feeds -->
    <div class="virtual-list flex-1 overflow-y-auto">
      
      <!-- Reusable feed row -->
      <div class="feed-row flex items-center p-3 border-b hover:bg-gray-50">
        <div class="feed-indicator w-2 h-2 rounded-full bg-blue-500 mr-2"></div>
        <div class="feed-icon w-8 h-8 rounded bg-gray-200 mr-3"></div>
        <div class="feed-content flex-1 truncate">
          <div class="feed-title font-medium">Supplier Invoices</div>
          <div class="feed-desc text-xs text-gray-500 truncate">mpe.invoice.payment-observed.v0.2</div>
        </div>
        <div class="feed-actions opacity-0 hover:opacity-100 flex gap-2">
          <button class="btn-pin text-sm">Pin</button>
          <button class="btn-subscribe text-sm">Subscribe</button>
        </div>
      </div>

    </div>
  </main>
</div>
```

## State Contract & Technical Dispositions

To support hundreds of feeds without losing context across reloads, the local interface must maintain:

1. **UserPreferencesState:**
   - `pinnedFeeds`: `Array<FeedId>`
   - `customFolders`: `Record<FolderId, Array<FeedId>>`
2. **CatalogState:**
   - Static/Mock registry of 500+ distinct feeds grouped by `profileFamily` (e.g., `urn:mpe:model:rfq.v0.2`).
3. **SubscriptionIntentState (Local Overrides):**
   - Maps `FeedId` -> `{ status: 'active' | 'paused' | 'unsubscribed', hasUnread: boolean, readCursor: string }`.
   - **Crucial:** `hasUnread` is a boolean flag, avoiding decorative high-frequency unread counts which cause layout thrashing.
4. **Search/Filter State:**
   - `query`: `string` (supports textual facets).
   - `activeCategory`: `string | null`.

**Technical Disposition:** The UI state (pinned items, active subscriptions, read cursors) must be persisted to `localStorage` or `IndexedDB` in the demo so that browser reloads retain organizational structure.

## Scale, Keyboard, and Performance Acceptance Criteria

- **Scale:** The catalog must render a synthetic fixture list of 500 distinct feeds smoothly. Use DOM virtualization (e.g., sliding window rendering) to maintain `<16ms` frame times during scrolling.
- **Performance / Latency Proof:** The demo proves usability independently of protocol privacy throughput by executing all search filtering, sorting, and optimistic UI updates (pinning, subscribing) purely in memory within `10ms`. The backend simulation's network lag is decoupled from the UI response.
- **Keyboard Navigation:** The catalog list must be fully traversable using `ArrowUp` and `ArrowDown`. `Enter` selects a feed to open the detail view; `Space` toggles the subscription state. Search must be focusable via a global hotkey (e.g., `/` or `Ctrl+K`).

## Plain Product Prose Examples

*Instead of:* "Historical offline quote: 100 Share; 123.45 USD per Share; cash 12345.00 USD. Expires 2026-10-04T13:00:00.000Z. Off-chain coordination only."
*Use:* **"Dealer Quotes"** — *Firm off-chain share quotes.*

*Instead of:* "Historical offline payment assertion: Pending (payment:pending); 250.00 USD against 500.00 USD payable. Source-observed status does not prove consensus finality or execute a payment."
*Use:* **"Pending Supplier Payments"** — *Observed payment statuses pending finality.*

## Consensus Recommendations & Unresolved Decisions

**Recommendations:**
1. Move to a strictly dual-pane (or tri-pane) layout separating the catalog index from the stream content/simulation controls.
2. Implement boolean unread indicators instead of numerical badges to eliminate decorative counting and reduce cognitive load.
3. Use a static, heavily populated mock catalog (hundreds of items) purely for the front-end to prove search and filtering scale, backed by the limited set of executable offline fixtures for actual simulation.

**Unresolved Decisions / Dissent:**
- Should the "Consumer mode" (Human, Wallet, DApp, Agent) dictate entirely different catalog views, or just filter the available profiles? (I recommend it just acts as a global context filter, but this requires wider council consensus).
- How do we visualize the "quarantine" state compactly in a list without overloading the primary unread indicator? This requires further iteration on the feed row design.
