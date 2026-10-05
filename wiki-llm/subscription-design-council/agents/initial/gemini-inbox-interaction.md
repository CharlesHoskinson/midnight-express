# Gemini Inbox Interaction Report

**Incumbent Findings**
Inspected the current `subscriptions.html` local dashboard via Scrapling PixelRAG (`http://127.0.0.1:8876/subscriptions.html`, accessed 2026-10-05).
* The current UI vertically stacks the control plane (streams and subscriptions) with the consumption plane (inbox and quarantine).
* Event details are hidden behind an expander (`<details>`) rather than a dedicated reading pane, adding friction to the review process.
* Actionable tasks (review, quarantine) share the same visual weight and layout flow as informational updates.
* Lack of standard inbox interaction patterns: no bulk actions, no keyboard navigation sequences, and no clear split view for high-throughput review.
* Loading and empty states are absent or rely on text-based placeholders (e.g., "No local receipts yet"), failing to provide structural feedback.

**Primary Sources**
* **Apple Human Interface Guidelines (Split Views):** Scraped via Scrapling PixelRAG (`https://developer.apple.com/design/human-interface-guidelines/split-views`, accessed 2026-10-05). Inspected visual tile `tile_0000.jpg`, confirming the canonical 3-pane structure: Sidebar (navigation/feeds), Canvas/List (primary pane of items), Inspector/Detail (content and actions).

**Information Architecture & Interaction Pattern**
* **Recommendation:** A 3-pane split view (Sidebar, Item List, Detail View) for desktop, collapsing to a drill-down navigation stack on mobile.
* **Sidebar:** Feed directory grouped by category (quotes, payments, approvals) or user-defined folders. Includes unified views like "All Unread" and "Quarantine".
* **Item List (Primary Pane):** Chronological list of events in the selected feed. Displays event preview (sender, summary, timestamp). Unread items are bolded.
* **Detail View (Secondary Pane):** Full payload of the selected event, explicitly separating the event's business data from local processing actions (Approve, Reject, Quarantine, Mark Read).
* **Rejected Alternative:** A single-column vertical feed (similar to a social timeline). Rejected because it fails for high-throughput business data where detail inspection and distinct dispositions (quarantine vs review) are required without losing the context of the queue.

**State Contract & Dispositions**
* **Read/Unread vs Processing:** "Unread" is a local consumption state indicating the payload hasn't been viewed in the Detail pane. "Processing" (reviewed, quarantined, approved) refers to the contiguous decided dispositions (the processing cursor). Reading an item does *not* automatically commit a business disposition.
* **Search/Folders:** Searches execute locally against the retained journal. Folders are local organizational groupings of subscription handles, independent of the network shard.
* **Reload/Rollback:** Reloading the app restores state from the local consumer journal. Rollback (undo) for a disposition is permitted locally *only* if the action hasn't been committed to the external protocol (or if it's purely a quarantine label).

**Scale, Keyboard & Performance Acceptance Criteria**
* **Keyboard:** Native-feeling sequences. `j`/`k` (or up/down arrows) to navigate the Item List. `Enter` to focus Detail. `e` to mark reviewed/archive, `Shift+q` to quarantine.
* **Scale:** The Item List must render 1,000+ items smoothly using DOM virtualization.
* **Performance:** Switching selected items in the list must update the Detail pane in < 50ms without layout thrashing.
* **Empty/Loading States:** Skeleton loaders for the Item List during bounded pulls. Explicit empty states illustrating "No pending approvals" or "Quarantine is empty" rather than a blank pane.
* **Bulk Actions:** Shift-click selection in the Item List with bulk "Mark Reviewed" or "Quarantine" actions in a floating toolbar.

**Plain Product Prose Examples**
* "Select an approval request to review its details and authorize execution."
* "3 items quarantined due to missing validation context."
* "You have reached the end of the unread queue."

**Consensus Recommendations & Dissent**
* **Consensus:** Adopt the 3-pane split view for desktop to separate navigation, queue management, and reading.
* **Dissent/Unresolved:** Should "Mark Read" automatically advance the delivery cursor if no business disposition is required? Dissenting view: The processing cursor should only advance upon explicit review, even for informational feeds, to ensure no event is silently acknowledged by scrolling.

**Annotated HTML Mock Snippet**
```html
<div class="split-view-container">
  <!-- Sidebar Navigation -->
  <nav class="sidebar" aria-label="Mailboxes">
    <div class="folder active">Approvals <span class="badge">12</span></div>
    <div class="folder">Payments</div>
  </nav>
  
  <!-- Primary Pane: Item List -->
  <section class="item-list" aria-label="Message List">
    <div class="list-item unread selected" tabindex="0">
      <div class="item-sender">System</div>
      <div class="item-summary">Payment final assertion</div>
      <div class="item-time">10:42 AM</div>
    </div>
    <!-- Virtualized items continue -->
  </section>
  
  <!-- Secondary Pane: Detail View -->
  <main class="detail-pane" aria-label="Message Detail">
    <header class="detail-header">
      <h2>Payment final assertion</h2>
      <div class="actions">
        <button class="btn-primary" aria-label="Acknowledge Receipt">Acknowledge</button>
        <button class="btn-secondary" aria-label="Quarantine Item">Quarantine</button>
      </div>
    </header>
    <div class="detail-content">
      <!-- Read-only payload rendered here -->
    </div>
  </main>
</div>
```
