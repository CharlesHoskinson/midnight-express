# Subscription Design Council: Gemini Directory & Scale Review

## Precise Incumbent Findings

Based on visual inspection of the incumbent dashboard (`http://127.0.0.1:8876/subscriptions.html`, captured via PixelRAG CDP tiles `tile_0000.jpg`, `tile_0001.jpg`, `tile_0002.jpg` on 2026-10-05):
- **Layout:** The "Browse streams" section presents a flat, unpaginated stack of large UI cards. The current six rigid categories are an incumbent defect, failing to scale for hundreds of distinct feeds.
- **Search & Navigation:** Search relies on a single input field above the list, with no faceted routing. The UI lacks folders, pins, or native pagination.
- **Controls & Semantics:** Cards expose hover-only or poorly grouped action buttons (Inspect, Simulate, Subscribe). The UI collapses intent, read state, and runtime delivery into confusingly blended states.
- **Messaging:** The demo problematically labels source-observed payment statuses as generic "pending" or "finality," and offers "Approve" actions despite lacking execution authority. 

## Primary Sources & Provenance

1. **Incumbent:** `http://127.0.0.1:8876/subscriptions.html` (Local Demo). Inspected 3 PixelRAG Scrapling tiles (`tile_0000.jpg`, `tile_0001.jpg`, `tile_0002.jpg`) on 2026-10-05.
2. **VS Code Extension API - Views UX Guidelines:** `https://code.visualstudio.com/api/ux-guidelines/views`. Text successfully fetched and inspected via Scrapling on 2026-10-05 (visual render closed the connection). Confirmed structural grouping principles.
3. **Material Design 3 - Lists:** `https://m3.material.io/components/lists/overview`. While the text output returned only an app-shell (69 bytes), PixelRAG tile inspection (`tile_0000.jpg`) on 2026-10-05 confirmed practical semantic list arrangements: leading indicators, clear primary text, and trailing, always-visible actions.

## Information Architecture & Interaction Pattern

**Recommended Pattern: Default Directory with Supporting Inbox**
The Directory is the default landing workspace. It organizes bounded paginated lists of feeds (distinct descriptor bindings, not just aliases). The Inbox is a supporting view for reading disclosed events.

- **Sidebar (Navigational Rail on Desktop / Drill-down on Mobile):** Contains User-defined Folders, Pinned Feeds, and a structural taxonomy of available feed descriptors (principal/shard/profile/contract/source/predicate).
- **Master Directory (Center):** A paginated, native HTML list of feeds. Each row features an always-visible trailing action button (no hover-only controls). Unread status is indicated by a simple boolean visual marker (no emoji, no decorative counting). 
- **Inbox/Reading View:** Opens explicitly when interacting with a feed. Reading an item is a separate action from a processing disposition. The delivery cursor does not advance merely by reading.

**Scale and Native Semantics:** 
Pagination using bounded rows is the correct working choice for hundreds of items. Virtualization should be deferred until a measured need is proven. Native semantic lists (`<ul>`/`<li>`), buttons (`<button>`), and checkboxes (`<input type="checkbox">`) must be used instead of custom ARIA keyboard grids.

**Separation of State and Authority:**
- **Stateful Information:** A local IndexedDB retains synthetic inbox history, read/unread markers, and folder organization.
- **Authority:** Restored requested-state is *not* restored authority. A reloaded browser retains historical metadata but requires fresh connection checks for new deliveries. The wallet origin-wide grant remains unchanged and no auto-connect occurs.

## Annotated Desktop/Mobile Wireframe Snippet

```html
<!-- Desktop: Sidebar + Paginated Directory + Supporting Inbox -->
<div class="layout-app grid-cols-[240px_1fr]">
  
  <!-- Sidebar Navigation -->
  <aside class="sidebar-nav overflow-y-auto">
    <div class="nav-section">
      <h3 class="nav-header text-sm font-semibold">Pinned Feeds</h3>
      <ul class="nav-list">
        <!-- Boolean unread indicator, always-visible native buttons -->
        <li class="nav-item flex items-center justify-between p-2">
          <div class="flex items-center gap-2">
            <span class="indicator-dot bg-blue-500 w-2 h-2 rounded-full" aria-label="Unread items present"></span>
            <span>Dealer Quotes</span>
          </div>
        </li>
      </ul>
    </div>
  </aside>

  <!-- Default Directory (Master List) -->
  <main class="feed-directory flex flex-col p-4">
    <header class="directory-toolbar mb-4">
      <input type="search" class="search-input w-full p-2 border" placeholder="Search descriptor metadata..." />
      <!-- Full source/authority warnings remain visible -->
      <div class="warning-banner text-xs text-amber-700 bg-amber-50 p-2 mt-2">
        Warning: Stored preferences do not authorize delivery. Fresh checks pending.
      </div>
    </header>
    
    <!-- Native Paginated List, NOT an ARIA grid -->
    <ul class="feed-list flex-1 border-t">
      <!-- Reusable feed row: distinct trusted feed descriptor -->
      <li class="feed-row flex items-center justify-between p-3 border-b">
        <div class="feed-metadata flex-1">
          <div class="feed-title font-medium">Pending Supplier Payments</div>
          <div class="feed-binding text-xs text-gray-600">Source assertion; pending finality (urn:mpe:source:bank)</div>
        </div>
        <!-- Always visible actions, no hover-states -->
        <div class="feed-actions flex gap-2">
          <button class="btn border px-3 py-1">Pin</button>
          <button class="btn border px-3 py-1">Subscribe</button>
        </div>
      </li>
    </ul>

    <!-- Pagination Controls -->
    <nav class="pagination flex justify-between mt-4">
      <button class="btn border px-3 py-1">Previous</button>
      <span>Page 1 of 5</span>
      <button class="btn border px-3 py-1">Next</button>
    </nav>
  </main>
</div>
```

## State Contract & Technical Dispositions

1. **Axes of State (Strictly Separated):**
   - **Intent:** `Followed`, `Pinned`, `Folder Assignment`. Handled by local IndexedDB. 
   - **Read/Organization:** Reading an event updates a local read marker. Undoing a read or moving a folder does NOT alter committed service checkpoints.
   - **Runtime/Authority:** `Delivery Paused`, `Active`, `Revoked`. Reloading marks delivery pending fresh checks.
   - **Processing Disposition:** Explicitly decoupled from reading. Actions are limited to `Review` and `Quarantine`. 
2. **Performance:** Performance budgets are unmeasured targets, not proof. Scale claims require rendering 500+ items and executing search filtering locally, utilizing pagination to maintain standard responsiveness.
3. **Execution Limits:** The UI must NEVER offer "Approve" or "Authorize" execution, nor claim that actual source/finality has been verified. 

## Plain Product Prose Examples

*Current Defect:* "Payment final assertion: Pending (payment:pending)... Source-observed status does not prove consensus finality or execute a payment."
*Target Prose:* **"Pending Supplier Payments"** — *Source-asserted payment status; pending consensus finality.*

*Current Defect:* Action buttons offering execution or generic approval.
*Target Prose:* **"Mark Reviewed"** or **"Quarantine"** — *Explicit local processing dispositions only.*

## Revision Decisions

- **Addressed the six categories:** Replaced the rigid 6-category structure with a generic catalog of distinct trusted feed descriptor bindings.
- **Clarified feed identity:** Explicitly defined feeds as distinct bindings to principal/shard/profile/contract/source/predicate, rejecting the "alias catalog" model.
- **Corrected Authority & State:** Clarified that restored state in IndexedDB does not equal restored authority; wallet origin grants remain unchanged and fresh checks are mandatory on reload.
- **Clarified Read vs Disposition vs Effect:** Explicitly decoupled reading (local preference) from processing disposition (review/quarantine) and effects. The delivery cursor is not advanced by reading.
- **Removed Authorize/Approve claims:** Removed all wireframe and prose references to authorizing effects or claiming actual finality. Payment statuses are explicitly labeled as "Source-asserted."
- **Removed Hover & ARIA Grids:** Updated the wireframe to use native `<ul>`/`<li>` tags, paginated navigation, and always-visible action buttons. Virtualization is deferred.
- **Removed Decorative Counting:** Specified that unread status uses a simple boolean indicator dot, rejecting numerical counts and emoji.
- **Performance Caveat Added:** Acknowledged that proposed performance budgets are unmeasured targets and not proof of actual protocol scale.
- **Warnings Maintained:** Added an explicit, visible warning banner regarding source authority and connection limits directly into the directory wireframe.
