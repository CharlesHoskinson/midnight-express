# Subscription directory workspace

Status: recommended design from the subscription council. The existing website remains the tab-memory demonstration; this plan has not replaced its interface. The user selected discovering and organizing feeds as the default workflow and requires search, hundreds of independently selectable feeds and retained information.

The [council record](../../wiki-llm/subscription-design-council/README.md) links the model reviews, primary sources, measurements and disagreements. This design uses Impeccable’s guidance for operational interfaces and preserves Midnight Express’s current product and protocol boundaries.

## Start with the directory

The first viewport should show feeds and search. Use a compact navigation rail, a result list and a selected-feed preview. Directory is the first-visit destination. My feeds organizes subscriptions; Inbox reads delivered items; Delivery tools explains pauses, permissions, coverage and recovery. Returning visitors may restore their last view, with Directory always available.

The optional Moth connection opens from a supporting control. Browsing and following the local demo do not require it. Simulation controls belong in their own disclosure, apart from Follow, Mark read and Record review. Remove the large introductory stack and empty sticky announcement bar. Keep a short simulation notice and put detailed evidence at the decisions where it matters.

On desktop, selecting a feed opens the preview beside the results. On narrow screens, preview becomes a separate view. Back restores the query, filters, result page, scroll anchor and focused feed. Filters use a disclosure with explicit controls; they do not need a wizard. Preserve the existing site identity and use compact, readable rows.

```text
Midnight Express · Subscriptions                  Optional wallet · Demo settings
Synthetic demo · no production delivery or execution

Directory       Directory                               Selected feed
My feeds        Search feeds                            Purpose and scope
Inbox           Category · Evidence · Following         About · Examples
Delivery tools  Active filters · Sort                   Declared source
                Feed name · purpose · source            Evidence and limitations
Folders         Evidence · follow state · Preview       Choose folder: Unfiled
Saved views     Feed name · purpose · source            Follow in demo
                Previous · visible range · Next         Delivery details
```

The centre shows catalog results in Directory and event receipts in Inbox. A sidebar full of individual feeds must not become the only way to search a large catalog. Mobile keeps the same destinations and tasks without compressing the desktop panes into narrow columns.

## Give each object a clear meaning

| Object | Meaning | What changing it does |
|---|---|---|
| Profile | An installed contract defining business meaning and interpretation. | Requires an authenticated release and explicit compatibility. |
| Feed | A stable catalog identity with a purpose and explicit local scope. | Resolves to a bounded local watch; a title does not authenticate a source. |
| Channel | An optional publisher collection of feeds. | Organizes discovery; it is not a relay topic or permission boundary. |
| Subscription | A principal-bound intent with immutable revisions, start position and limits. | Controls local delivery under current authorization. |
| Folder | A personal grouping of feed references. | Changes organization only. Deleting it moves entries to Unfiled. |
| Saved view | A named query over a declared search scope. | Changes presentation; installs no watch and widens no permission. |
| Item | A receipt delivered under a subscription revision. | Has separate reading markers and processing disposition. |

A feed descriptor contains stable identity, name, description, declared publisher/source label, category, evidence class and example references. A trusted local resolver binds it to the existing principal, shard, exact profile/contract, allowed sources and predicate. The adapter keeps the feed-to-subscription mapping outside the closed intent and sealed business envelope.

Multiple feeds in the same category must be independently selectable and pausable. Changing a descriptor cannot silently change an installed subscription. Scope edits show the old and new binding and create a revision. Aliases disclose their shared scope and follow a consistent duplicate policy; aliases do not count as independent subscriptions.

Use the currently allowed predicates. Instrument, invoice, target or named-human selectors suggested by some reviewers require a reviewed contract extension before installation. A feed name cannot smuggle an unsupported selector into the existing schema.

## Make discovery useful at scale

Each row shows a name, short purpose, declared source/scope, category, evidence and follow state. Preview and Follow are distinct controls. Payment Pending, Final and Reversed are examples inside the relevant payment feed; they are not repeated buttons for the same category subscription. Preserve the distinction between an offline source assertion and finality or execution.

Search Directory by name, description, declared source/publisher, category and supported profile. Search received items separately within already disclosed history. Show the scope, active filters, stable result count and clear no-results recovery. Do not search raw payload JSON by default. Match query terms deterministically, combine facet groups with AND and choices within a group with OR, and document that behavior.

Start with Category, Evidence and Following facets. Add a searchable source facet when meaningful source metadata exists. My feeds adds Folder and delivery attention state. Default sorting is name; search or facet changes return to the first result page. Clearing the query preserves other facets.

Render a bounded page, initially 50 rows, with Previous/Next and a visible range. Keep selection by identity and update affected rows rather than rebuilding the inbox or subscription controls on each keystroke. This is the working choice for hundreds of lightweight descriptors. Virtualization remains an option after profiling substantially larger histories; it is not required merely because a catalog is large.

Feed-reader discovery/folder patterns and GitHub’s distinct subscription and notification views inform this flow. Their remote polling and automatic subscription behaviors do not transfer to Midnight Express. [Feedly discovery](https://docs.feedly.com/article/287-how-to-find-and-add-follow-sources), [Feedly folders](https://docs.feedly.com/article/288-how-to-follow-a-feed-in-your-feedly-account), [GitHub inbox guidance](https://docs.github.com/en/subscriptions-and-notifications/how-tos/viewing-and-triaging-notifications/managing-notifications-from-your-inbox).

## Follow, organize and read

Preview presents purpose, exact scope in readable language, evidence class and representative examples. Follow uses an inline configuration area with the supported predicate, start behavior and optional folder. Default to Unfiled. Advanced limits and revision history remain available in Delivery details.

After following, preserve focus and list position, update the row and offer Open inbox. Following an existing resolved scope opens its current configuration or explains the alias; it never creates an accidental duplicate. Personal organization supports pins, folders and saved views. Batch moves and pin changes name the selected page scope and offer Undo. Cross-page selection requires an explicit choice. Bulk follow, scope changes and processing are deferred until their authorization and partial-failure semantics are defined.

Opening an item may mark it read. Mark unread and Save are presentation operations. Record review and Quarantine target the selected receipt and are explicit processing decisions. Reading changes neither cursor. A disposition advances processing only across contiguous decided work. None of these actions authorizes an effect; this demo offers no execution approval.

Show a readable summary and evidence before raw JSON. Keep original records, receipt revision, offline check and exact context in details. Use “Final asserted by the source,” never “Payment finalized” or “Paid” where the fixture provides only an observation. Identical valid repeats remain auditable without appearing as fresh business information. Validation precedes identity checks: changed context alone is not an occurrence-content conflict.

## Remember information without recreating authority

Use IndexedDB for a bounded, versioned synthetic history and per-record transactional updates. Small view preferences may use a separate device store. Browser persistence is best effort and untrusted on read. It is neither the production consumer journal nor a wallet grant. Production history comes from the authenticated local consumer service backed by the selected database tier.

| State | Restore after reload | Required boundary |
|---|---|---|
| Folders, pins, saved views, query, filters, sort and selection | Yes, with validated identities and bounds. | Organization never modifies a selector or grant. Private queries stay out of default URLs and telemetry. |
| Follow intent identity, revision references and requested pause | Yes, as last-known intent. | Reconcile with the service; current delivery starts unchecked. |
| Historical synthetic items, read/saved markers and recorded dispositions | Yes, explicitly labeled historical. | Already disclosed records do not authorize delivery, processing or effects. |
| Journal positions, queues, deduplication and coverage | May be retained as a bounded simulation snapshot. | No automatic continuation. Validate identity and atomically reconcile continuity before use. |
| Current permission, authenticated principal claim or wallet adapter/grant | No trusted restoration. | Require fresh checks. Moth starts locally disconnected with no RPC or polling. |

After reload: “Saved demo restored. Check the simulation before resuming delivery.” Retain requested pause through checks and recovery. A mock check creates only simulation authority; it cannot establish a production grant. Viewing historical disclosures stays separate from committing a new processing decision.

Version migrations must handle open tabs through `versionchange`/`blocked`; writes must handle quota failures and corruption. Use a writer lock plus transactional revision checks, with cross-tab notifications as hints to reread records. A failed write must not report durable progress. Do not serialize the entire state tree after every action or depend on unload to save it. [IndexedDB lifecycle](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), [storage limits and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria).

Separate Reset simulation, Clear saved history, Forget organization and Disconnect locally. None revokes an origin-wide Moth grant. On the shared GitHub Pages origin, persist synthetic material only and explain device storage in Manage data. A dedicated origin and authenticated service are required before treating this as a place for real private consumer records.

## Show what needs attention

Model requested intent, current authority, coverage and outstanding work separately. A feed can be paused and behind, or revoked and gapped. Its primary status names the blocking problem and one useful next action; details preserve the other facts.

Full queue credits mean behind, not missing history. Distinguish retained work that can be recovered from an unavailable interval. Never silently discard undecided work or offer a new start as the default for full credits. Explicit new-start acceptance records a revision and preserves requested pause. Intake and whole-shard repair remain independent of selectors and follow state.

Persistent problems stay beside the affected feed. Transient confirmations may be brief. Closing retains a tombstone and relabels outstanding disclosed work as historical instead of leaving unreachable “awaiting review” actions. Allowing a verified local owner to stop an expired watch is a proposed control-policy improvement requiring revised lifecycle tests; it does not permit reactivation or scope expansion.

## Accessibility and verification

Use native lists, headings, links/buttons and checkboxes. Do not assign ARIA feed, tree or grid roles without implementing and testing their interaction contract. Keep search focus while typing, preserve focus after Follow and restore it after preview. Batch announcements; incoming items must not jump the reading position. Character-only shortcuts are optional, can be disabled or remapped, and stay within a focused component. They never commit dispositions or wallet operations. [WAI keyboard guidance](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/), [character key shortcuts](https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html).

Validate discovery and all core actions at desktop/mobile widths, enlarged text, actual browser zoom and 320 CSS-pixel reflow. Test real assistive technology before claiming accessibility conformance. A lack of horizontal overflow alone does not establish usability.

Acceptance work must cover:

- A newcomer searches, previews, follows and files a feed without wallet setup or interpreting a cursor. Search and initial results are usable in the first viewport.
- Independently scoped same-category feeds receive only their matching sources. Pause/unfollow affects only the selected feed; descriptor changes require revisions.
- A deterministic large catalog exercises the actual renderer. Proposed target: p95 settled-query-to-render opportunity within 200 ms at 600 descriptors on a documented device, with at most 50 catalog rows rendered. Report throttled/device results separately; this is not a measured achievement.
- A separate mock-watch campaign exercises hundreds of distinct scopes, fan-out, per-watch limits and an aggregate host budget. A metadata-only catalog does not satisfy this gate.
- Reload retains declared history and organization while delivery is unchecked and wallet calls remain zero. Test expiry, revocation, pause, gaps, replay, quota failure, migration, corrupted records and stale-tab writes.
- Read changes leave processing untouched; dispositions are receipt-specific and atomically recorded. Recovery preserves requested pause and never skips unavailable work silently.
- Follow, search, organization and recovery produce no selector-bearing relay request. Original canonical fixtures and genuine receipts remain unchanged.

For an honest functional scale demo, generate distinct synthetic sources within the declared mock-only families and test their bindings. Keep canonical v0.2 examples and their sources immutable. A fictitious scope without a truthful event-to-scope binding is preview-only; it has no fabricated validator receipt or wire. New business predicates/profiles require separate conformance work. Catalog usability, simulation correctness and production transport performance remain separate evidence.

## Implementation order

First correct identity and state boundaries: descriptor resolution, independent watches, authority/coverage axes and receipt-specific actions. Then build the directory, preview and personal organization using stable keyed regions. Add bounded persistence and restoration gates before claiming stateful use. Complete scale, failure, keyboard and responsive checks before publishing the replacement interface.

The selected transport stack remains unchanged. This design adds a catalog/resolver and consumer presentation layer plus native browser storage for the synthetic prototype. It introduces no remote interest broker or additional privacy protocol. The local service and durable journal remain implementation work, not capabilities supplied by a prettier page.
