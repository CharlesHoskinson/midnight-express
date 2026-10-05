# Subscription workspace audit

The council design is implemented as a browser-local synthetic workspace. Directory is the default; My feeds, Inbox and Delivery tools separate discovery, organization, reading and operational state. The optional wallet and simulation controls are disclosures. The existing site identity is preserved.

The catalog contains three immutable offline business reference feeds and 600 distinct synthetic source scopes across contracts, credentials and operations. Each feed resolves to the unchanged closed local intent. These are functional mock bindings, rather than category aliases. Names and source labels establish no publisher authentication. Canonical examples, contexts, wires, validator receipts and the Moth adapter are unchanged.

## What was checked

| Area | Evidence | Result |
|---|---|---|
| Independent watches | `node website/tests/subscriptions-core.cjs` | A 600-watch campaign delivers each source only to its bound feed. Same-category watches operate independently. Intake works without followers. Per-watch queues and aggregate history have explicit bounds. |
| Intent contract | `python website/tests/subscriptions-intents.py` in the model environment | All 2,412 generated follow, pause, recovery and close revisions satisfy the existing closed schema. No business profile or selector extension. |
| Reading and processing | Core and browser tests | Read/save leave processing unchanged. Review/quarantine targets a receipt; out-of-order decisions cannot cross undecided work. Closing relabels outstanding disclosures as historical. No effect action exists. |
| Backpressure and recovery | Core tests | Full credits are behind with retained work, separate from a simulated unavailable interval. Recovery and explicit new-start acceptance preserve requested pause. |
| Replay | Core tests | Valid identical repeats become audit receipts. A rejected quote is quarantined before identity checks and cannot poison the later valid occurrence. |
| Persistence | `node website/tests/subscriptions.cjs` | Per-record IndexedDB writes are atomic and revision checked. Quota injection aborts the write; stale revisions refuse. Privileged operations recheck simulation authority inside the write transaction, and a failed guard leaves the revision unchanged. Other tabs invalidate current delivery authority and editing until reload. Version changes close the connection, and unknown database versions fail closed. |
| Reload | Browser and restore validation tests | Historical disclosures, organization and requested state restore. Current authority remains unchecked. Changed bindings, invalid continuity, limits and altered reference records refuse restoration. Wallet RPC count remains zero. |
| Discovery | Browser tests | Search preserves focus; filters and 50-row pagination are bounded. Reload does not accumulate duplicate DOM rows. Mobile preview Back restores the selected result’s focus and the prior scroll position. |
| Responsive layout | Browser checks and batched visual inspection | 1440, 390 and 320 CSS pixels, plus 200% text enlargement, have no horizontal overflow. Search and navigation remain available. |
| Browser zoom and contrast | `node website/tests/subscriptions-zoom.cjs` | Actual Chrome tab zoom 200% changes a 1440-pixel viewport to 720 CSS pixels; search and follow succeed. Representative computed text contrast exceeds 4.5:1, including button hover. This script uses the existing local preview at port 8876. |
| Wallet boundary | `node website/tests/moth-connector.cjs` and browser tests | Explicit acknowledgment and genuine click are required. Only connect and requested status calls occur; no automatic reconnect, polling, signing or grant revocation. |
| Existing evidence | Fixture checker, specification browser test and Lean publication guard | Genuine fixed-context reference receipts and public proof/source publication checks pass. This does not formally verify the new browser controller. |
| Repository | GitHub repository and license API | Public visibility; Apache-2.0 recognized. Imported sources and fonts retain their own attribution and licenses. |

Commands run from the repository root. The Python checks use the existing model validation environment. [Browser evidence](browser-evidence.json) records engine version, reflow geometry, errors and a small query timing sample. [Zoom and contrast evidence](zoom-contrast.json) records computed values. Screenshots show the inspected directory layout; later fixes to restored row bookkeeping were checked through DOM assertions.

Local query timing was below the proposed 200 ms threshold in the small unthrottled sample, including the 120 ms search debounce and preference write. The test machine is Linux x86_64 with an Intel Core Ultra 9 275HX; headless Chromium was 153.0.8010.12. This is a desktop smoke measurement, not a mobile-device benchmark or a production throughput result. The separate 600-watch campaign exercises actual mock delivery logic, not browser transport.

## Findings corrected

Credit exhaustion previously appeared as missing history. Delivery state now separates requested pause, current authority, coverage and outstanding work. Source-bound feed identity replaces the category-wide subscription limit. Restored history cannot resume delivery automatically.

Storage exceptions are caught inside the transaction and force an abort before reporting progress. Reloading saved state clears the old row registry and DOM together. Receipt controls preserve their focus through reading changes. Search updates avoid rebuilding preview and inbox controls. Enlarged headings wrap without extending the viewport.

Impeccable’s manual detector flagged a thick accent border; it was removed. Its remaining font warning is accepted to preserve the approved existing site identity. Its section-padding warning comes from the inherited global section rule; the workspace override removes that top border and padding, as inspected in the browser. Computed contrast checks resolve the earlier heuristic hover warning. Humanizer guidance was applied to product copy; headings contain no decorative counting.

## Limits and follow-up

This is synthetic IndexedDB history on a shared GitHub Pages origin. It establishes no authenticated service journal, production authorization, source identity, decryption, transport, signing or execution. Current simulation authority is an explicit mock check at a fixed reference clock. Private real-world records require a dedicated origin and the authenticated local consumer service.

Inbox renders the most recent 100 matching disclosed summaries; older stored receipts remain in the bounded export. The demo stops intake at its history budget rather than silently evicting undecided work. Undo for organization is session-local. Bulk follow and bulk processing remain excluded until their partial-failure and authorization semantics are specified.

Native controls, labels, focus handling, zoom and reflow are checked. Real assistive-technology testing, low-powered mobile measurements and additional browser engines remain necessary before claiming accessibility conformance or broad device performance. Future database versions need reviewed migrations; this release closes old connections and refuses unknown versions rather than guessing a migration.

Production restart/crash behavior, authenticated retention repair, external effect reconciliation and transport privacy need their own integration evidence. Browser simulation tests cannot establish those properties.
