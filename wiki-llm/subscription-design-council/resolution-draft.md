# Directory design resolution in progress

Historical working proposal from the council’s research phase. The [final workspace recommendation](../../design/subscriptions/directory-workspace.md) incorporates all completed reviews. This record follows the confirmed directory workflow and captures how disagreements were resolved against product requirements.

## Directory and destinations

Directory is the first-visit destination. My feeds organizes followed and saved offerings. Inbox reads disclosed events. Delivery tools explain pause, permissions, coverage gaps and recovery. Optional Moth connection is a supporting task, not a prerequisite to discovering feeds.

On desktop, use a compact navigation rail, searchable feed results and an optional selected-feed preview. On narrow screens, preview becomes a drill-down destination with Back restoring the query, result position and focused row. Preserve the site's established identity; replace the long introductory stack with an operational workspace.

A row represents a stable feed, with a useful name, purpose, declared source/scope, category and evidence label. Pending, Final and Reversed payment assertions are examples inside a Payments feed, not separate follow buttons for the same category. A channel can name a publisher's collection of feeds; it does not become a relay topic or cryptographic permission boundary. Folders and saved views are personal organization.

## Search and scale

Search feeds by name, description, declared publisher/source, category and supported profile. Directory search and received-item search are different scopes. Facets combine predictably, selected filters are visible and no-results offers a clear recovery. Sort and pagination remain stable. Render a bounded result page, keep selection by stable identity and update only affected regions.

Pagination is the default for hundreds of lightweight descriptors. Virtualization remains an option after profiling substantially larger event histories. A source label must never imply authenticated provenance. The directory is locally available metadata; discovery must not transmit business interests to relays or fetch sender-controlled schema URLs.

The target needs independently selectable feed scopes. Each offering resolves through trusted local metadata to a principal/shard/profile/contract/source/predicate-bound intent. Feed metadata stays outside the sealed business envelope and outside the closed intent schema. Multiple same-category subscriptions must be independently pausable and receive only their matching source scope. Aliases disclose the shared binding and do not count as distinct functional feeds.

## Stateful information

Retain synthetic organization, intent identities and revisions, historical inbox receipts, read/saved markers and disclosed processing state in a versioned local store. IndexedDB is the candidate for transactional records; localStorage may hold small presentation preferences. Browser storage is untrusted input and a local privacy surface.

Restored information is labeled historical. Requested active/paused state may be retained, but current authority, wallet connection and delivery availability are not restored as trusted facts. A fresh local simulation check is explicit. Production state comes from an authenticated principal-bound consumer service. Historical viewing does not authorize delivery or effects.

Opening an item may mark it read. Recording a review or quarantine is an explicit service disposition. These operations have different storage, receipts and semantics. Neither authorizes an effect. Undo may reverse folder moves or reading markers; committed processing decisions require a separately specified correction mechanism.

Persistence must handle schema migration, corruption, quota failure, retention bounds and stale-tab writes. Disposition/checkpoint updates need atomic transactions; a failed write cannot report successful durable progress. Retention loss produces an explicit gap and preserves outstanding work. Reset simulation, erase local history and disconnect wallet are different actions; no local action claims to revoke a Moth origin grant.

## Verification that matters

The directory must be usable in the first viewport, including enlarged text. Search cannot redraw unrelated controls, lose unsaved scope edits or move focus to the body. Native lists, links, buttons and checkboxes come first; an ARIA feed or grid is not a generic performance shortcut.

Exercise a realistic large descriptor catalog and a separate independently scoped mock-watch campaign. Verify two same-category sources, wrong-source refusals, independent pause/unfollow, descriptor changes creating revisions and duplicate alias handling. Measure actual renderer response on a documented device; catalog row count is not proof of protocol scale.

Reload after following, organizing and reading must preserve the declared records while making delivery authority pending. Revocation, expiry, gaps, queued work, deduplication, quota failures and multi-tab conflicts need separate tests. No wallet RPC occurs on startup. Real Moth interoperability, source authentication, private transport and durable production effects remain separate gates.

## Storage disagreement to resolve

The Claude storage reviewer supports IndexedDB organization with a fresh simulation check, but recommends deferring historical inbox persistence. The GPT usability reviewer requires retained synthetic inbox and explicit intent identity to satisfy the user’s stateful requirement. The working resolution retains a bounded, read-only historical archive and requested intent references, while forbidding cached grant restoration or automatic cursor restart. Service-owned checkpoint continuity remains separately authenticated and reconciled. A bookmark is labeled Saved; Following reflects a retained follow intent and shows delivery as stopped or unchecked after reload. The UI must not imply that a bookmark alone is an active watch.

Private queries and feed identifiers stay in device state by default, not shareable URL parameters. URLs may name static destinations. A later explicit share flow for public synthetic examples cannot become a default for private production queries. Browser state is best-effort local persistence, not the durable consumer service or protection from sibling applications sharing the origin.

## Operability corrections

The operability review identifies an important distinction: full local credits mean delivery is behind; they do not establish that retained originals are missing. Show backpressure separately from a retained-range recovery requirement and a genuinely lost interval. Never offer a discard/new-start action as the default response to a full queue.

Root checked the quote fixtures directly: accepted and expired-reference records contain exactly the same event and differ in validation context and receipts. The expired context therefore does not establish an occurrence-content conflict, despite that claim in the operability draft. Current validation precedes journal identity checks. A true conflict requires the same source/occurrence identity with different complete event content. Context rejection and structural conflict need separate examples and explanations.

Review actions target the selected receipt. Identical repeated occurrences must not appear as fresh business information; repetition diagnostics and processing bookkeeping remain distinct. Closing preserves a tombstone and gives existing disclosed work an explicit historical disposition instead of orphaning an actionable-looking queue.

The developer-event reviewer independently found that accepting a new start can overwrite the paused requested state. Recovery and explicit new-start acceptance must preserve requested pause. A watch may be paused and behind, or revoked and gapped, at the same time; requested intent, current authority, coverage and outstanding work require separate axes. Ordinary pause stops consumer delivery while whole-shard intake and repair remain independent of local matches. A local owner's ability to stop an expired or revoked watch is a proposed control-policy improvement, not existing behavior; any change needs authenticated ownership and revised lifecycle tests.

## Reader explanation

A profile defines the business meaning of an event. A feed defines which supported information a consumer follows. Adding a feed does not install a new profile or prove a publisher’s identity. Keep human-readable purpose and source/scope in the directory; place exact commitments, fixture context and original records in evidence details. Categories help discovery. Channels can collect a publisher’s feeds. Personal folders change organization only.

## Accessibility draft corrections

The initial Gemini accessibility draft overstates several conclusions. A source-observed Final assertion cannot be rewritten as “Payment finalized” or “paid”; the fixture supplies no live finality or payment execution evidence. Preserve source-assertion meaning in readable prose.

Use native list semantics for paginated directory and inbox views. APG’s feed pattern is an optional interaction contract for appropriate dynamic article feeds, not a required role for all pub/sub lists. Hundreds of rows do not by themselves require virtualization or establish memory exhaustion. Search must retain input focus while typing; announcing settled results is separate from explicitly moving to a chosen result. Background arrivals preserve the selected row and reading position.

The initial accessibility report contains hypothetical reflow concerns, not measured WCAG failures. The actual usability probes found no horizontal overflow at the tested text settings but found discovery buried far down the page. Keep text enlargement, CSS-pixel reflow and browser zoom as distinct tests. Touch target size is a proposed product target, not a universal claim about every WCAG criterion.

Root fetched W3C’s WCAG 2.2 Understanding Character Key Shortcuts page with Scrapling and inspected PixelRAG tile 0. Character-only shortcuts need a turn-off/remap mechanism or activation restricted to a focused component. No global single-character command should create a watch, commit a disposition, accept a gap or connect a wallet.

The Material Lists capture has only an app-shell text extraction, but root inspected tile 0 and found a substantive rendered page. It supports short, logically ordered rows with consistent text/actions. It provides no evidence for the draft’s claimed ten-millisecond performance or mandatory virtualization.
