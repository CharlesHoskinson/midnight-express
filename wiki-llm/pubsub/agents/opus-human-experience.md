# Human subscription experience: research record

Role: human subscription product designer. Model: claude-opus-5-5. Research date: 2026-10-05. Scope: making browsing, consent, cursor/gap/paused/expired states, wallet and DApp personas, and accessibility understandable in the local subscription dashboard. The work had to keep the original MPE whole-shard encrypted wire, keep the Moth connector boundary, and avoid ambiguous delivery or completion language.

## Approach

I read the current drafts (`standards.md`, `subscription-contracts.md`, `wallet-consumers.md`), the sol-wallet and sol-dashboard agent records, `website/dist/subscriptions.{html,js}` and `moth-connector.js`. I treated them as drafts to check, not as settled facts. Public primary sources were retrieved only with Scrapling through `research.py`, and discovery used the GitHub public search API through the same fetcher. Raw bytes, extracted text, UTC timestamps and SHA-256 digests for each source are in `../sources/opus-human-experience/`. I checked each accepted source's topic and content myself, beyond the helper's HTTP heuristic. The Moth facts come from the verified sol-wallet corpus (`../sources/sol-wallet/manifest.json`, pinned commit `d48206a1957af09bf17bf5e941c2b5bccb12db63`). I did not refetch them.

Visual grounding: PixelRAG 0.4.0 (CDP backend) captured the WalletConnect Notify Subscription page as one tile (`walletconnect-notify-subscription-visual.json`, tile sha256 `a1eefa46db2a981826173f37ea7c36be3d104b86beec680ed5f7447e07c4ae76`, raw sha256 `0c4ab15c…b79259`). I inspected the tile. It shows the subscription definition, the did:web key and registry flow, and the subscribe protocol steps, including "Notify Server triggers webhook to notify Dapp of new registered address". I chose this page because its Scrapling text extraction was truncated at "Protocol", so the visual was needed to confirm the steps. No other source in this group has a visual capture, so their claims rest on archived text only.

## Source findings and pins

| Source (retrieved 2026-10-05) | What it actually shows | Design consequence |
|---|---|---|
| [WalletConnect Notify subscription spec](https://specs.walletconnect.com/2.0/specs/clients/notify/notify-subscription), visually verified; [Notify overview](https://specs.walletconnect.com/2.0/specs/clients/notify) last updated Sep 22, 2024 | Subscription is "an agreement between a dapp and a wallet". Wallet browses a dapp registry, subscribes remotely, Notify Server decrypts `subscriptionAuth` and webhooks the dapp with the registered address. | A good browse-then-subscribe gesture. Its disclosure model is the opposite of the MPE private default: the sender learns who subscribed. Adopt the browse-and-consent UX only. Reject the remote-registration transport. |
| GitHub search: [WalletConnect/web3inbox](https://github.com/WalletConnect/web3inbox) and `web3inbox-client` | API reports `archived: true` for both (last pushed 2025-12-05 and 2024-05-13). | The reference wallet inbox for Notify is archived. Do not cite it as a living pattern or as an interoperability target. |
| [MetaMask Snaps notifications](https://docs.metamask.io/snaps/features/notifications/) | `snap_notify` requires a manifest permission. Types are `inApp` and `native`, with in-app recommended. The docs list rate limits of five in-app notifications per minute and two native per five minutes, plus an optional expanded view. | Wallet-hosted notification permission is a separate install-time grant, and the wallet applies its own rate limits. Our wallet persona must stay in-app by default, show a bounded summary with an expanded detail, and never assume an OS alert was seen. |
| [XMTP user consent](https://docs.xmtp.org/chat-apps/user-consent/user-consent), [support guide](https://docs.xmtp.org/chat-apps/user-consent/support-user-consent) | Unknown, Allowed and Denied consent per peer. New inbound conversations start as Unknown. The consent list is encrypted on the network and shared across all apps the user authorized. | The three-state source consent is worth adopting locally ("Requests", "Allowed", "Blocked" sources). The cross-app network-synced list is a disclosure we do **not** adopt by default. |
| [GitHub notifications REST API](https://docs.github.com/en/rest/activity/notifications), [configuring notifications](https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications) | Each thread carries a `reason` (subscribed, mention, approval_requested …), and the reason can change per thread. Polling uses `Last-Modified`/`304` and a server-set `X-Poll-Interval`. Watching is separate from participating. | Every inbox item should show *why it is here*: the local watch handle and the matched local category. Separate "watching" from "needs my decision". Reason labels are local derivations, not sender claims. |
| [Matrix Client-Server API v1.16](https://spec.matrix.org/v1.16/client-server-api/) | Sync timeline has `limited: true` when events were omitted, plus a `prev_batch` token for backfill. | Precedent for an explicit, machine-readable "there is a hole here" flag with a recovery handle. This maps onto our `gap` object. Matrix's server-side room filters are not adopted. |
| [Midnight indexer API v4 docs](https://raw.githubusercontent.com/midnightntwrk/midnight-indexer/456fa193184a1b269513f006e9dd5a2739566ec6/docs/api/v4/api-documentation.md) and [schema-v4.graphql](https://raw.githubusercontent.com/midnightntwrk/midnight-indexer/456fa193184a1b269513f006e9dd5a2739566ec6/indexer-api/graphql/schema-v4.graphql), pinned main `456fa193` (commit date 2026-10-05T08:43:47Z) | `connect(viewingKey)` gives a session. `shieldedTransactions(sessionId, index)` emits progress with `highestZswapEndIndex` (chain known), `highestCheckedZswapEndIndex` (scanned for relevance) and `highestRelevantZswapEndIndex` (relevant to this wallet). Nullifier subscriptions filter by prefix and take `fromBlock`/`toBlock`. Several streams resume from an offset or ID. | Strong Midnight-native precedent for showing **coverage separately from matches**: known head, checked through, last relevant. The indexer session receives a viewing key, so it is a ledger-observation service with its own disclosure. It is not an MPE pubsub path and must not be relabeled as one. |
| [Android notification channels](https://developer.android.com/develop/ui/views/notifications/channels) (redirected to the Compose page) | A channel has an ID, a user-visible name and importance. The app cannot change importance or behavior after registration, and the user controls the channel in system settings. | Categories should be user-named, user-controlled units, and the sender cannot raise their urgency. This supports local categories whose alert level only the user sets. |
| [WAI-ARIA APG feed pattern](https://www.w3.org/WAI/ARIA/apg/patterns/feed/) | `article` items with `aria-posinset`/`aria-setsize` (−1 when unknown), `aria-busy` during updates, and Page Up/Page Down between articles. | Inbox structure and keyboard model. Set size is −1 because a private whole-shard feed has no meaningful total. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 4.1.3 Status Messages (AA): announced without moving focus. The Enough Time criteria (2.2.x) and 3.3.4 Error Prevention (Legal, Financial, Data) are present in the index. | Announce state transitions via a status region. Expiry countdowns must not force time-limited decisions without warning. Reversible and confirmable actions are required for anything with financial meaning. |
| [W3C Push API](https://www.w3.org/TR/push-api/), [WHATWG Notifications](https://notifications.spec.whatwg.org/) (the W3C TR URL redirected there) | Push subscriptions go through a third-party push service endpoint, and `userVisibleOnly` governs silent pushes. | An OS or browser push path is an external disclosure (push service operator, timing). It may only be an explicit opt-in export and never the default. |
| Push Protocol docs `push.org/docs/notifications/` and `/build/subscribe-to-channel/` | **HTTP 404**, recorded as failures and not used as evidence. The GitHub org listing returned an empty body (`accepted_source: false`). The repo search found `pushchain/push-notifications-sdk`, last pushed 2025-06-04, which was not inspected further. | No Push Protocol claims are made. |

Moth (from the verified sol-wallet corpus): `window.midnight.moth`, `rdns io.shielded.moth`, connector API `4.0.1`, `connect(networkId)` → ConnectedAPI, `getConnectionStatus`. Grants are **per origin**. `hintUsage` triggers connection approval and does not narrow it. Moth has no connector revoke or disconnect method. The official connector repo is at `4.1.0-beta.1` under the `@midnightntwrk` package spelling. The dashboard connector correctly calls only connect/status and fails closed on version.

## Recommendation

Keep the dashboard as a local, unsigned simulation and reshape its human-facing model around four ideas that are each grounded in a source above.

**Coverage is distinct from matches (Midnight indexer, Matrix).** Each subscription card shows three local positions in plain words:
- "Received through" is the journal high-water mark from whole-shard intake.
- "Checked through" is the delivery cursor after the local selector.
- "Reviewed through" is the processing cursor.

It also shows a gap line whenever `gap ≠ null`. Never show "up to date", "all caught up", "complete" or "0 new" unless the received and checked positions are equal *and* no gap or pause exists. Even then, say "No matching items received through position N", because quiet is not completeness.

**Every item says why it is here and what has not happened (GitHub reason).** Each inbox row shows the matched local watch and category, its validation mode ("unsigned mock", or "offline reference, live source not verified") and a disposition. The disposition vocabulary is fixed:

| State shown | Means | Never implies |
|---|---|---|
| Received | Original stored in the local journal | Sender authenticity, finality |
| Matched | Local selector chose it for this watch | Sender targeted you; any network filtering |
| Reviewed | A person or handler recorded a disposition | Action executed, payment made |
| Quarantined | Rejected locally, with a reason | Sender notified |
| Historical | Past its expiry or permission window | Actionable approval |

Remove "delivered" from user-facing copy entirely, because in messaging products it implies a remote recipient acknowledgement. The internal field name can remain `deliveredCursor`, but the label should be "checked through". Rename the "Mark next item reviewed" button to "Record review of next item". Rename "Simulate intake and delivery" to "Simulate whole-shard intake".

**Subscription states use plain language plus a single next action (Matrix `limited`, WCAG 4.1.3):**

| Runtime state | Headline | Next action offered |
|---|---|---|
| active | Watching locally | Pause |
| paused | Paused. Intake continues within storage limits, nothing is matched for you | Resume |
| gapped | Missing history between positions A and B (reason: retention / missing range / conflict) | Accept gap as a new revision, or recover from archive (not available in demo) |
| expired | Watch ended at time T. Earlier items stay readable as history | Create new revision |
| revoked | Local permission withdrawn. Queued items will not be shown or acted on | Review permissions |
| unsubscribed | Stopped. Occurrence history kept for duplicate protection | Create new subscription |

Every transition is announced through the existing `role="status"` region, and focus does not move. Gap acceptance is a confirmable step: it creates a new revision and states what will never be shown.

**Consent is layered and each layer is named (WalletConnect browse/consent, XMTP three-state, Android user-owned channels, MetaMask separate notify permission).** Browsing streams needs no permission and lists local categories derived from installed profiles, never network topics. Subscribing is one confirmation sheet that states, in order:
- what will be matched (category and profile)
- from which admitted sources (default "all admitted sources on this shard", with Requests/Allowed/Blocked per-source states kept locally)
- start position (earliest retained / latest / after cursor) and what history that includes
- expiry
- destination inbox
- explicitly, that this sends nothing to the network

Wallet connection is a separate, optional panel. Its copy keeps the existing accurate statement that Moth grants the whole origin and that local disconnect does not revoke it. A notification or alert level is a user setting per category, and the sender cannot escalate it.

### Personas

- **Human (no wallet)**: browse categories, subscribe with the confirmation sheet, read the inbox, record reviews. This is the default persona, and it needs no wallet.
- **Wallet user**: as above, plus optional Moth connection status shown as "Connected to Moth on preprod (status only)". The inbox stays in-app. OS alerts are an explicit future export, labeled with push-service disclosure. No balance, address, signing or payment calls are made.
- **DApp operator**: an application principal with its own grant and expiry. The dashboard shows the app's watch handles and the inbox it is allowed to read. The wallet session is independent.
- **Agent supervisor**: sees the agent's durable inbox and candidates. Approval candidates are always "Historical" in the pinned-clock demo. The dashboard prepares no tools or effects.

### Accessibility changes

- Render the inbox as an APG feed: a `role="feed"` container, one `article` per item labeled by title and disposition, `aria-setsize="-1"`, and `aria-busy` while simulated intake mutates the list.
- Support Page Up/Page Down and document the keys on the page.
- State is never conveyed by color alone: use text badges with the fixed vocabulary.
- Expiry is shown as an absolute UTC time with a relative hint. No live countdown that re-announces.
- The confirmation sheet uses `fieldset`/`legend`, and errors are announced via the status region.
- Keep the existing 390px at 200% text check. Add a keyboard-only pass covering subscribe → gap → accept → unsubscribe.

## Existing technology suffices; stack additions

Existing pieces suffice for the demo: static HTML/CSS/JS, the fixture manifest, `moth-connector.js`, the LocalSubscriptionIntent and runtime records in `subscription-contracts.md`, and the browser `role="status"` region. Every recommendation above is copy, state presentation and ARIA markup over the existing runtime fields: `deliveredCursor`, `processedCursor`, `oldestRetainedCursor`, `gap`, `state`. The demo needs **no new stack component**.

One data-model addition is proposed: a local journal high-water field `receivedCursor` on the runtime record, so the "received through / checked through" distinction is not inferred. It is local control-plane only and does not touch the wire. No web push, service worker, WalletConnect/Notify, XMTP SDK or indexer client should be added to the dashboard.

## Data-model fit and limits

The v0.2 model's three closed profiles (rfq, invoice, agent) give useful finite scenarios for quotes, payments and approvals. Contracts, credentials and ops remain unsigned mock categories, and the UI must badge them as such. Expiry fixed at 2026-10-04T13:00Z means quotes and approvals are always Historical on any real clock, which is correct and should be explained once on the page rather than per item. The fit is therefore good for demonstrating state comprehension and weak for demonstrating real-time usefulness. The page must not claim the latter.

Limitations:
- No live Moth extension was connected in this research.
- No user testing was done, so the recommendations are design inferences from primary patterns.
- WalletConnect and Web3Inbox status reflects only the spec page and the GitHub archived flag.
- MetaMask rate limits are documented values, not observed behavior.
- The Midnight indexer's progress semantics come from schema doc comments at the pinned commit.
- Matrix, GitHub and Android are analogies for UX, not protocol targets.

## Proposed consensus decisions

- The user-facing vocabulary is Received / Matched / Reviewed / Quarantined / Historical. The word "delivered" is not shown to humans. No completion claim appears without equal received/checked positions and no gap or pause, and even then it is phrased as "no matching items received through N".
- Subscription cards show coverage (received, checked, reviewed) separately from matches, following the Midnight indexer's known/checked/relevant progress fields.
- Each item shows its local reason (watch handle and category) and validation mode.
- Consent stays layered: browse with no grant, then a local subscribe confirmation sheet, then optional wallet connection described accurately as an origin-wide grant, then any external export as a separate disclosure decision. Wallet connection never gates or implies subscription.
- Source consent is local three-state (Requests/Allowed/Blocked) and is never synced to a network.
- Alert level belongs to the user per category, and the sender cannot raise it.
- Gap acceptance is an explicit, announced, confirmable revision.

## Unresolved objections

- **Showing positions to non-technical users.** Raw cursor numbers may confuse people. A counter-proposal is to show positions only in an expandable detail and lead with "Missing history: yes/no". I prefer the visible numbers in the demo because the product point is the coverage distinction, but this needs a user test.
- **Requests/Allowed/Blocked versus admitted sources.** Admitted shard sources are already authorized at the transport layer. Some reviewers may view a per-source local block list as redundant or as implying authentication the demo lacks. It must be labeled as a local display preference, not sender verification.
- **"Paused while intake continues."** Storage-bounded intake during pause may surprise users who expect pause to mean "stop receiving". The copy has to be precise, and the retention consequence needs agreement with the stack-feasibility research.
- **Wallet-hosted inbox.** A future Moth in-wallet inbox (similar to MetaMask's in-app notifications) would put the local selector inside the wallet. Moth's current origin-wide grant gives no narrower permission for that, so the dashboard should not hint at it.

## Rejected alternatives

- WalletConnect Notify / Web3Inbox: it uses remote subscription registration and a webhook that reveals the subscriber to the dapp, and the inbox repos are archived.
- XMTP network-synced consent list: it discloses consent across apps.
- Browser Web Push as the default alert path: the push service is a third party and adds timing disclosure.
- Midnight indexer viewing-key sessions as an MPE subscription path: it is a separate ledger service with its own disclosure.
- Matrix and GitHub server-side filters and reasons as routing: they would turn local interests into network topics.
- An unread-count badge as the headline: it reads as completeness over a feed with no knowable total.
- A live expiry countdown: it is a WCAG timing and announcement burden.
- An IndexedDB-persisted demo: it would imply durable receipts (agreeing with the sol-dashboard decision).

## Sources

All retrieved 2026-10-05 via Scrapling, with metadata and hashes in `../sources/opus-human-experience/*.json`:
- https://specs.walletconnect.com/2.0/specs/clients/notify/notify-subscription (text and PixelRAG visual)
- https://specs.walletconnect.com/2.0/specs/clients/notify
- https://api.github.com/search/repositories?q=web3inbox+org:WalletConnect
- https://docs.metamask.io/snaps/features/notifications/
- https://docs.xmtp.org/chat-apps/user-consent/user-consent
- https://docs.xmtp.org/chat-apps/user-consent/support-user-consent
- https://docs.github.com/en/rest/activity/notifications
- https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications
- https://spec.matrix.org/v1.16/client-server-api/
- https://api.github.com/repos/midnightntwrk/midnight-indexer/commits/main (pin `456fa193184a1b269513f006e9dd5a2739566ec6`)
- https://raw.githubusercontent.com/midnightntwrk/midnight-indexer/456fa193184a1b269513f006e9dd5a2739566ec6/docs/api/v4/api-documentation.md
- https://raw.githubusercontent.com/midnightntwrk/midnight-indexer/456fa193184a1b269513f006e9dd5a2739566ec6/indexer-api/graphql/schema-v4.graphql
- https://developer.android.com/develop/ui/views/notifications/channels (resolved to the Compose channels page)
- https://www.w3.org/WAI/ARIA/apg/patterns/feed/
- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/TR/push-api/
- https://notifications.spec.whatwg.org/ (W3C TR URL redirected here)
- Failures, not evidence: https://push.org/docs/notifications/ (404), https://push.org/docs/notifications/build/subscribe-to-channel/ (404), https://api.github.com/orgs/push-protocol/repos (empty body)
- Moth facts: `../sources/sol-wallet/manifest.json`, github.com/shieldedtech/moth-wallet at `d48206a1957af09bf17bf5e941c2b5bccb12db63`
