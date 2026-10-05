# Accessibility and Responsive Workflow Review
**Agent:** gemini-accessibility
**Focus:** Native semantics vs ARIA patterns, keyboard focus, screen reader announcements, responsive 200% at 320px, focus preservation at scale.

## 1. Revision Decisions (Root Corrections Addressed)
- **Directory Default & Scale:** Shifted focus to a directory of hundreds of distinct trusted feed descriptors. The incumbent's six categories are treated as a defect.
- **State & Authority Boundaries:** Clarified that restoring requested state is not restoring authority. Reading an item is separate from a committed processing disposition (which is separate from a ledger effect). 
- **Pagination over Virtualization:** Replaced the mandate for DOM virtualization with bounded pagination as the default, robust accessibility choice for hundreds of rows. Virtualization is deferred until measured need.
- **Native HTML over ARIA:** Dialed back the strict requirement for the WAI APG Feed pattern. Native lists and buttons are prioritized; APG Feed remains an optional enhancement only if dynamic infinite-scroll is introduced.
- **Prose Integrity:** Reverted the proposal that stripped source/authority warnings from payment assertions. "Payment finalized" is an overstatement; original warnings regarding source-observed assertions must remain to preserve product truth.
- **Action Visibility:** Enforced that all actions must be visible to keyboard and touch (no hover-only actions) without using emoji or decorative counting.

## 2. Precise Incumbent Findings
I inspected the current browser-local simulation at `http://127.0.0.1:8876/subscriptions.html`.
- **Structural Semantics & Scale:** The incumbent relies on six static mock categories rather than independent feed descriptors. Items are wrapped in standard `<div>` and `<article>` tags without native list (`<ul>`/`<li>`) structuring. A catalog of aliases is only metadata testing, not fulfillment of the requirement for distinct trusted feed descriptor bindings (to principal/shard/profile/contract/source/predicate).
- **State & Actions:** The UI collapses the concepts of reading, disposition, and effect. Reading an item does not advance the delivery cursor. The demo currently lacks clear visual separation between a local folder "undo" and a committed checkpoint disposition. Furthermore, actions do not make it clear that no real execution is occurring (e.g., claiming finality).
- **Focus Management:** Dynamic intake injects items into the DOM without preserving reading focus or managing the viewport reliably. 
- **Responsive 200% at 320px:** Tested visually via PixelRAG tiles. Fixed paddings and multi-column flex layouts risk horizontal scrolling or text clipping on 320px screens at 200% zoom (WCAG 1.4.10 Reflow).
- **Interactive Controls:** Some actions are not optimally sized for mobile thumbs, and the UI lacks semantic native lists that naturally group items for screen readers.

## 3. Primary Sources & Provenance
- **Incumbent Application:** `http://127.0.0.1:8876/subscriptions.html`
  - *Provenance:* Midnight Express local repository, `website/dist/subscriptions.html`.
  - *Inspection Method:* Local Scrapling visual extraction via PixelRAG. I directly inspected `tile_0000.jpg`, `tile_0001.jpg`, and `tile_0002.jpg` from the `127.0.0.1_8876_subscriptions.html.png.tiles` capture on 2026-10-05.
- **W3C WAI ARIA Authoring Practices Guide (APG) - Feed Pattern:** `https://www.w3.org/WAI/ARIA/apg/patterns/feed/`
  - *Provenance:* Official W3C accessibility guidelines for dynamic feeds.
  - *Inspection Method:* Accessed via Scrapling on 2026-10-05. I inspected `tile_0000.jpg`, `tile_0001.jpg`, and `tile_0002.jpg` from the `www.w3.org_WAI_ARIA_apg_patterns_feed.png.tiles` capture.

## 4. Recommended Information Architecture & Interaction Pattern
**Recommendation:** Implement the Directory as the primary default destination, supported by the Inbox, using **Native HTML Semantics (Lists, Buttons, Checkboxes)**.
- **Why Native Wins:** A standard `<ul>` and `<li>` structure combined with standard bounded pagination is universally supported by assistive technologies. It requires no complex custom keyboard event handling (unlike ARIA grids) and naturally allows screen readers to enumerate items (e.g., "Item 1 of 50").
- **Directory and Distinct Feeds:** The directory must render independently selectable, distinct feed descriptors at a scale of hundreds. Pagination (e.g., 50 per page) provides a stable, measurable DOM size and a clear focus boundary without relying on unmeasured performance budgets or complex DOM virtualization.
- **Always-Visible Actions:** Primary controls (Subscribe, Review, Quarantine) must be visible at all times. Do not hide them behind mouse-hover states, as this breaks mobile touch and keyboard discoverability.

**Rejected Alternative:** **Mandatory Custom ARIA Feed or Grid Patterns**
- **Rationale for Rejection:** Implementing complex ARIA structures like grids forces assistive technologies into forms/application mode, breaking normal reading navigation. The APG Feed pattern, while suited for infinite scroll, introduces keyboard management overhead (PageUp/PageDown handling). Bounded pagination with native lists is superior, safer, and inherently accessible for this data type.

## 5. Annotated HTML Mock Snippet

```html
<!-- Annotated HTML Mock (Not a UI edit, demonstrating structural semantics) -->
<!-- Standard semantic lists support bounded pagination natively -->
<section id="directory" aria-labelledby="dir-heading">
  <h2 id="dir-heading">Feed Directory</h2>
  
  <ul class="feed-list" aria-label="Available Feeds">
    <li class="feed-item">
      <!-- Always-visible, distinct descriptor bindings -->
      <h3 class="feed-title">Payments: Alice's Node</h3>
      <p class="feed-meta">Source: node_123 | Contract: v1.payment</p>
      
      <div class="feed-actions">
        <!-- Native controls, no hover-only dependency, no emoji -->
        <button type="button" aria-pressed="false">Follow Feed</button>
      </div>
    </li>
    <!-- Paginated rows continue... -->
  </ul>
  
  <nav aria-label="Directory pagination">
    <button type="button" disabled>Previous Page</button>
    <span aria-current="page">Page 1</span>
    <button type="button">Next Page</button>
  </nav>
</section>

<section id="inbox" aria-labelledby="inbox-heading">
  <h2 id="inbox-heading">Local Inbox</h2>
  <ul class="inbox-list">
    <li class="inbox-item">
      <!-- Full source and authority warnings are preserved -->
      <h3 class="item-title">Payment Assertion: Final</h3>
      <p class="item-desc">
        Source-observed status: 250.00 USD against 500.00 USD payable. 
        Note: This does not prove consensus finality or execute a payment.
      </p>
      <div class="item-actions">
        <button type="button">Mark Reviewed</button>
        <button type="button">Quarantine</button>
      </div>
    </li>
  </ul>
</section>
```

## 6. State Contract & Technical Dispositions
- **Authority vs Request:** Restoring requested state on reload (e.g., "Active" feed) does not restore authority or reconnect wallets. Fresh local simulation checks are required.
- **Reading vs Disposition:** Moving focus to or reading a message does *not* advance the delivery cursor or record a processing disposition. Review and quarantine are explicit, committed decisions.
- **Execution Limits:** The demo must never offer "Approve" or "Authorize" action buttons that imply actual on-chain execution, nor should it claim actual source/finality has been verified. 
- **Undo Semantics:** Undoing a local folder move or toggling a "read" marker operates on personal organization metadata. This is entirely distinct from committed checkpoints, which require a separately specified correction mechanism.
- **Axis Separation:** Intent, read status, and runtime states must be tracked on independent axes. A preference status cannot collapse them into a single variable.

## 7. Scale, Keyboard, and Performance Acceptance Criteria
- **Pagination over Virtualization:** Bounded row pagination is the accepted architectural choice for managing hundreds of feeds. Virtualization should only be explored if future profiling strictly proves it necessary. Proposed performance budgets (e.g., "10ms renders") remain unmeasured targets, not proof of need.
- **Keyboard Preservation:** When paginating or executing a search, programmatic focus must be moved explicitly to the top of the new result set. Search must retain focus in the input field while typing, updating a bounded set of results safely.
- **Status Region:** Background intake must be managed carefully. A live status region should be rate-limited so as not to overwhelm screen reader audio output during rapid background updates.
- **Responsive 200% @ 320px:** No content clipping or horizontal scrolling permitted. Multi-column layouts must collapse gracefully to a single column, ensuring all text strings and buttons wrap or scale within the viewport constraints.

## 8. Plain Product Prose Examples
- **Preserved Product Truth:** Payment statuses are *source assertions*, not generic pending-finality. 
- **Correct Prose:** "Historical offline payment assertion: Final (payment:demo); 250.00 USD against 500.00 USD payable. Source-observed status does not prove consensus finality or execute a payment."
- *Note: We do not rewrite this into "Payment finalized" because doing so falsely claims execution authority and strips the necessary warning about source-observation limits. Full warnings must remain in relevant evidence components.*

## 9. Consensus Recommendations & Dissent
- **Recommendation 1:** Adopt semantic native HTML (`<ul>`, `<li>`, `<button>`) for both the directory and the inbox. Abandon custom ARIA grids and defer the APG Feed pattern unless unbounded infinite scroll becomes a strictly measured requirement.
- **Recommendation 2:** Enforce standard bounded pagination for handling hundreds of distinct feed descriptors to guarantee stable DOM accessibility and focus management.
- **Recommendation 3:** Ensure all interaction actions (Review, Quarantine, Follow) are always visible and distinct. Remove any reliance on hover-states or decorative emoji.
- **Recommendation 4:** Maintain strict separation between reading a message and committing a disposition. Expose clear warnings on all items to prevent users from mistaking a source assertion for an executed transaction.
