# Gemini Inbox Interaction Report (Revised)

**Incumbent Findings and Structural Defects**
Inspected the current `subscriptions.html` local dashboard via Scrapling PixelRAG (`http://127.0.0.1:8876/subscriptions.html`, accessed 2026-10-05, visual tiles `tile_0000.jpg`, `tile_0001.jpg`, `tile_0002.jpg` inspected). 
The current interface vertically stacks the control plane (streams and subscriptions) with the consumption plane (inbox and quarantine) into a single scrolling document. This structural defect prevents high-throughput reading and triage. Event details are hidden behind an expander (`<details>`), adding friction to the review process. Actionable tasks share the exact same visual weight and layout flow as purely informational updates. 

Critically, the incumbent design relies on six fixed category watches. This is an incumbent defect and not the permanent target. The actual requirement is to support a catalog of hundreds of independent feeds. The current UI fails to separate the concept of discovering a feed in a directory from the act of processing events in an inbox. Furthermore, the dashboard's simulated presentation of state obscures the strict boundaries between intent, runtime delivery, and local read status. 

**Primary Sources and Provenance**
Research is grounded in the following public primary sources, fetched exclusively via Scrapling and visually inspected using PixelRAG:
1. **Apple Human Interface Guidelines (Split Views):** Scraped `https://developer.apple.com/design/human-interface-guidelines/split-views` (accessed 2026-10-05). Visual tile `tile_0000.jpg` confirmed the canonical 3-pane structure: Sidebar (navigation/feeds), Canvas/List (primary pane of items), and Inspector/Detail (content and actions). This pattern is mandatory for separating directory navigation from event queues and detailed evidence inspection.
2. **Apple Human Interface Guidelines (Lists and Tables):** Scraped `https://developer.apple.com/design/human-interface-guidelines/lists-and-tables` (accessed 2026-10-05). Visual tile `tile_0000.jpg` confirmed the requirement for native, semantic lists that provide persistent feedback for selection and hierarchy, explicitly prioritizing native OS and browser semantics over custom grid implementations.

**Information Architecture: Feed Directory Default**
**Recommendation:** The Feed Directory must be the default first-visit destination and the primary operational workspace, replacing the long introductory stack of the incumbent dashboard. The application must adopt a 3-pane split view for desktop (Sidebar, Item List, Detail View), which collapses to a drill-down navigation stack on narrow mobile screens.

* **Sidebar (Directory & Destinations):** Organizes followed and saved offerings. This is not just a list of six categories; it is a scalable directory supporting hundreds of synthetic feeds. A row in this sidebar represents a stable feed with a useful name, purpose, declared source/scope, and category. 
* **Item List (Primary Pane):** Displays the events for the selected feed using bounded row pagination. Virtualization is strictly deferred until empirical profiling of substantially larger event histories dictates measured need. 
* **Detail View (Secondary Pane):** Renders the full payload of the selected event, separating the event's business data from local processing actions.

**Trusted Feed Descriptor Bindings**
The target architecture must support independently selectable feed scopes. Each offering in the directory resolves through trusted local metadata to a specific, unique binding. A trusted feed descriptor binds explicitly to `principal/shard/profile/contract/source/predicate`. 
Feed metadata (such as a channel grouping a publisher's collection of feeds) remains strictly outside the sealed business envelope and outside the closed intent schema. Multiple subscriptions within the same category must be independently pausable and receive only their matching source scope. An alias in the catalog is merely for metadata presentation and discovery; it does not constitute a distinct functional feed or a cryptographic permission boundary.

**State Contract, Cursors, and Dispositions**
The design must rigorously enforce the boundaries between intent, read status, and runtime execution. Preference status must never collapse the intent/read/runtime axes.

* **Restored Requested-State vs. Restored Authority:** The application must retain synthetic organization, intent identities and revisions, historical inbox receipts, and disclosed processing state in a versioned local store (e.g., IndexedDB). However, restored requested-state is *not* restored authority. Reloading the application requires fresh local simulation checks for pending deliveries. The wallet (Moth) must **never** auto-connect on startup; connection is an explicit, separate user gesture, and the origin-wide grant warning remains unchanged and fully visible.
* **Read != Processing Disposition != Effect:** 
  * "Unread" is a local consumption state indicating the payload has not been viewed. 
  * Opening an item to read it does **not** automatically advance the delivery cursor, nor does it commit a business disposition. 
  * Recording a review or a quarantine is an explicit service disposition (advancing the processing cursor). 
  * Neither reading nor processing authorizes an execution effect. The demo must never offer "Approve" or "Authorize execution" buttons, nor may it claim that actual source authentication or consensus finality is verified. Actionable buttons must be strictly limited to "Mark Reviewed" and "Quarantine".
* **Undo Semantics:** Moving an item to a folder or toggling its local "read/unread" status are distinct local presentation changes that can be easily undone. In contrast, committed processing checkpoints (review, quarantine) are durable service dispositions and are not casually undoable. Reversing them requires a separately specified correction mechanism.
* **Payment Statuses as Assertions:** Payment statuses (Pending, Final, Reversed) appearing in the feed are historical offline assertions observed by the source. They are explicit business envelope payloads representing the source's observation, not generic, protocol-level pending-finality states. 

**Interaction, Accessibility, and Performance Constraints**
* **Native Semantics:** The UI must employ native semantic HTML elements (`<nav>`, `<ul>`, `<li>`, `<button>`, `<input type="checkbox">`) rather than custom ARIA keyboard grids. This guarantees inherent accessibility and robust reflow behavior.
* **Always Visible Actions:** Keyboard and touch actions must be persistently visible. Hover-only primary controls are explicitly forbidden, as they fail accessibility standards for touch devices and keyboard users.
* **No Decorative Elements:** The interface must use exact, practical terms. Emoji icons and decorative counting headers are prohibited.
* **Source and Authority Warnings:** Full source and authority warnings must remain persistently visible in relevant evidence views and connection decisions. The user must constantly be reminded that the UI reflects a local simulation and unverified source assertions.
* **Performance Budgets:** Proposed performance metrics (e.g., detail pane rendering in under 50ms) serve strictly as unmeasured targets to guide engineering discipline, never as proof of protocol scale or rendering finality.

**Revision Decisions**
This report has been revised to explicitly integrate the root quality review corrections:
1. **Feed-directory default:** Restructured the Information Architecture section to explicitly mandate the Feed Directory as the default first-visit destination, discarding the incumbent's stacked dashboard.
2. **Target distinct trusted feed descriptor bindings:** Added a dedicated section detailing how feeds strictly bind to `principal/shard/profile/contract/source/predicate`.
3. **Restored state is not restored authority:** Explicitly documented that reload requires fresh delivery checks and that wallet auto-connect is forbidden.
4. **Read != processing != effect:** Clarified the strict separation of local read state, processing cursors, and the absolute prohibition of execution effects in the demo.
5. **No execution authority:** Removed all references to "Approve" or "Authorize" in UI mocks and prose; limited actions to Review and Quarantine.
6. **Wallet grant unchanged:** Maintained the requirement for the full origin-wide grant warning.
7. **Folder/read undo distinct:** Explicitly defined the difference between casual local undo (read state) and committed checkpoint correction (processing).
8. **Payment statuses:** Defined Pending/Final/Reversed strictly as source-observed payload assertions.
9. **Preference status separation:** Mandated that intent, read, and runtime axes remain uncollapsed in the data model and UI representation.
10. **Pagination over virtualization:** Replaced the previous virtualization requirement with bounded row pagination as the working choice, deferring virtualization.
11. **Native semantics:** Replaced ARIA grid recommendations with strict native semantic HTML requirements (`<ul>`, `<li>`).
12. **Always visible actions:** Banned hover-only controls; updated the mock to reflect persistent actions.
13. **No emoji/decorative counting:** Stripped all decorative badges and emojis from the design language.
14. **Performance budgets:** Clarified that stated performance goals are unmeasured targets, not proof of capability.
15. **Full warnings:** Ensured mock and prose reflect the necessity of persistent offline/unverified warnings.

**Plain Product Prose Examples**
* "Select a payment assertion to review its details and mark it as locally reviewed."
* "3 items quarantined due to missing validation context."
* "Historical offline reference only; live source and permission are not verified."
* "This origin-wide grant persists until revoked in the Moth wallet."

**Consensus Recommendations & Dissent**
* **Consensus:** Adopt the 3-pane split view for desktop (collapsing to drill-down on mobile) with bounded row pagination to separate navigation, queue management, and reading.
* **Dissent/Unresolved:** The strict separation of read state from the processing cursor may introduce perceived friction for users accustomed to traditional email clients where reading automatically marks an item as processed. However, consensus holds that business event triage requires explicit disposition to prevent accidental acknowledgment.

**Annotated HTML Mock Snippet**
```html
<div class="split-view-container">
  <!-- Sidebar Navigation: Feed Directory -->
  <nav class="sidebar" aria-label="Feed Directory">
    <div class="section-heading">My Feeds</div>
    <ul class="directory-list">
      <li class="folder active">
        <button aria-current="page">Approvals Queue</button>
      </li>
      <li class="folder">
        <button>Payments (Final)</button>
      </li>
    </ul>
  </nav>
  
  <!-- Primary Pane: Item List (Bounded Pagination) -->
  <section class="item-list" aria-label="Inbox Queue">
    <ul class="message-list">
      <li class="list-item unread selected">
        <div class="item-sender">System Node</div>
        <div class="item-summary">Payment final assertion: 250.00 USD</div>
        <div class="item-time">10:42 AM</div>
        <div class="persistent-actions">
          <input type="checkbox" aria-label="Select item for bulk action">
        </div>
      </li>
      <!-- Paginated items continue -->
    </ul>
    <nav class="pagination" aria-label="Queue pagination">
      <button disabled>Previous</button>
      <span>Page 1 of 4</span>
      <button>Next</button>
    </nav>
  </section>
  
  <!-- Secondary Pane: Detail View -->
  <main class="detail-pane" aria-label="Message Detail">
    <header class="detail-header">
      <h2>Payment final assertion: 250.00 USD</h2>
      <div class="warning-banner" role="alert">
        Historical offline payment assertion. Source-observed status does not prove consensus finality or execute a payment.
      </div>
      <div class="visible-actions">
        <button class="btn-primary">Mark Reviewed</button>
        <button class="btn-secondary">Quarantine</button>
      </div>
    </header>
    <div class="detail-content">
      <!-- Read-only payload evidence rendered here -->
      <pre>
{
  "profile": "payment:demo",
  "status": "Final",
  "amount": "250.00 USD",
  "executes": false
}
      </pre>
    </div>
  </main>
</div>
```
