# Accessibility and Responsive Workflow Review
**Agent:** gemini-accessibility
**Focus:** WAI APG feed patterns, keyboard focus, screen reader announcements, responsive 200% at 320px, focus preservation at scale.

## 1. Precise Incumbent Findings
I inspected the current browser-local simulation at `http://127.0.0.1:8876/subscriptions.html`.
- **Structural Semantics:** The current inbox items are wrapped in `<div class="inbox-item">` and streams in `<article class="stream">`. There is no overarching ARIA structural role (such as `feed`, `grid`, or `listbox`) governing the list of items.
- **Screen Reader Interaction:** Because the structural semantic is missing, screen readers treat the inbox as a flat document. Users must tab through every interactive element sequentially instead of utilizing reading-mode commands to jump article-by-article.
- **Focus Management:** When new items are simulated via intake, they are injected into the DOM. There is no explicit focus management to prevent the browser or screen reader's virtual cursor from jumping unexpectedly, particularly if auto-scrolling triggers on arrival.
- **Live Regions:** An `aria-live="polite"` status region exists (`<p id="announcement">`). While correct in principle, simulating rapid intake can flood the region, causing screen reader announcements to overlap or be dropped entirely. A status region rate limit is missing.
- **Responsive 200% at 320px:** The CSS utilizes `max-width: 1100px` and basic `@media(max-width: 600px)` breakpoint logic that shifts controls to `flex: 1 1 10rem`. At 320px width scaled to 200% zoom (effectively 160px), fixed padding (`1.5rem`) and long unbroken text nodes can cause horizontal scrolling or text clipping, violating WCAG Reflow (1.4.10) guidelines.

## 2. Primary Sources & Provenance
- **Incumbent Application:** `http://127.0.0.1:8876/subscriptions.html` 
  - *Provenance:* Midnight Express local repository, `website/dist/subscriptions.html`.
  - *Inspection Method:* Local Scrapling visual extraction via PixelRAG (`--visual` rendering) and direct file inspection on 2026-10-05.
- **W3C WAI ARIA Authoring Practices Guide (APG) - Feed Pattern:** `https://www.w3.org/WAI/ARIA/apg/patterns/feed/`
  - *Provenance:* Official W3C accessibility guidelines.
  - *Inspection Method:* Accessed via Scrapling on 2026-10-05. Verified specific interoperability contracts between `role="feed"` and assistive technologies.

## 3. Recommended Information Architecture & Interaction Pattern
**Recommendation:** Implement the WAI APG **Feed Pattern** (`role="feed"`) for the inbox and subscription streams.
- **Why it wins:** A feed establishes an interoperability contract allowing screen readers to stay in "reading mode." Users can press `Page Down` to jump to the next article and `Page Up` for the previous, facilitating rapid skim reading. It maps perfectly to a chronological stream of dynamic events (like quotes, payments, and approvals).
- **Focus & Batch Flow:** Search interactions must actively move focus into the feed container. For batch operations, standardizing `Shift + Up/Down` or `Shift + Space` to select multiple contiguous items while preserving focus is critical. Focus must strictly remain on the currently inspected article even when new items prepend to the DOM.

**Rejected Alternative:** **Grid or Listbox Pattern**
- **Rationale for Rejection:** While a Grid provides robust two-dimensional keyboard navigation and batch selection, it forces the screen reader into "Forms/Application Mode." This strips away standard document reading commands, making it extremely difficult for visually impaired users to skim long-form text (like contract parameters or quote terms). A Listbox is meant for simple option selection, not rich, interactive event streams.

## 4. Annotated HTML Mock Snippet

```html
<!-- Annotated HTML Mock (Not a UI edit, demonstrating structural semantics) -->
<!-- role="feed" creates the interoperability contract. aria-busy manages load state. -->
<section 
  id="inbox-feed" 
  role="feed" 
  aria-labelledby="inbox-heading" 
  aria-busy="false">
  <h2 id="inbox-heading" class="visually-hidden">Local Inbox</h2>

  <!-- Each item is an article. tabindex="0" allows focus for reading mode keys -->
  <article 
    class="inbox-item" 
    role="article" 
    aria-posinset="1" 
    aria-setsize="-1" 
    aria-labelledby="item-1-title" 
    aria-describedby="item-1-desc"
    tabindex="0">
    <div class="item-header">
      <h3 id="item-1-title">Payment pending</h3>
      <span class="status-badge" aria-hidden="true">Pending</span>
    </div>
    <!-- Primary content linked by aria-describedby for skim reading -->
    <div id="item-1-desc" class="item-body">
      <p>250.00 USD against 500.00 USD payable. (payment:pending)</p>
    </div>
    <div class="item-actions">
      <!-- Actions remain focusable within the article -->
      <button type="button" aria-label="Review payment pending">Review</button>
    </div>
  </article>

  <!-- Subsequent articles... -->
</section>
```

## 5. State Contract & Technical Dispositions
- **Reload & Cursors:** On reload, the DOM resets. When the journal populates, `aria-posinset` must reflect the item's relative position. `aria-setsize` should be set to `-1` if the true total size of the filtered inbox is unknown, rather than reporting just the visible DOM count.
- **Search:** Executing a search must trigger a polite announcement of result counts and dynamically move programmatic focus to the first resulting `article` in the feed, ensuring the user doesn't have to navigate backwards out of the search input manually.
- **Folders / Unread / Read:** Changes in disposition (e.g., marking a quote "Reviewed") must update the item's `aria-labelledby` or inject hidden text so the screen reader announces the new state ("Reviewed: Payment pending") without forcing a DOM reload.
- **Rate-Limited Status Region:** Background deliveries must *not* trigger immediate `aria-live` announcements per item. Instead, queue incoming events and announce a batched summary ("3 new items received") at a maximum rate of once every 10 seconds.

## 6. Scale, Keyboard, and Performance Acceptance Criteria
- **Scale / Performance:** At hundreds of rows, the feed must employ DOM virtualization to prevent browser memory exhaustion. However, virtualized items must securely update `aria-posinset` to maintain the illusion of a contiguous feed. 
- **Keyboard Preservation:** When virtualization recycles a DOM node that currently holds focus, focus must be artificially preserved or seamlessly handed off to the newly positioned container. Auto-scroll jumps caused by prepending items must be disabled via CSS `overflow-anchor: none` or precise JS scroll-position locking.
- **Responsive 200% @ 320px:** No content may be visually clipped, and no horizontal scrollbars may appear. CSS Grid/Flexbox must wrap all metadata text, and interactive targets must remain a minimum of `44x44px` regardless of zoom level.

## 7. Plain Product Prose Examples
- **Current (Technical/Robotic):** "Historical offline payment assertion: Final (payment:demo); 250.00 USD against 500.00 USD payable."
- **Proposed (Human-Readable & Skimmable):** "Payment finalized: 250 USD of 500 USD paid. Validated offline."
*Note: Assistive technology users listen to text linearly. Front-loading the most critical state ("Payment finalized") improves comprehension speed over prefacing everything with "Historical offline payment assertion."*

## 8. Consensus Recommendations & Dissent
- **Recommendation 1:** Adopt WAI APG Feed Pattern immediately for the inbox to ensure native reading mode compatibility.
- **Recommendation 2:** Implement debounced/rate-limited live region announcements for incoming intake to avoid audio flooding.
- **Recommendation 3:** Replace technical prose with front-loaded state descriptors.
- **Unresolved Decision / Dissent:** DOM virtualization (required for hundreds of rows) inherently conflicts with native `Ctrl+End` (jump to end of feed) because the final nodes do not exist in the DOM. The council must decide whether to implement manual "Load More" pagination for accessibility, or attempt complex ARIA-managed virtualization intercepts. I strongly dissent against pure infinite scroll without a physical boundary; a manual "Load More" button at the boundary of virtualized chunks provides a much safer accessibility contract.
