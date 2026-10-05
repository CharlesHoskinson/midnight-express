# Privacy and authority review: subscriptions, wallets and the Moth connector

Role: cryptography and privacy reviewer. Model: claude-opus-5-5. Research date: 2026-10-05.
Ownership: this report and `../sources/opus-privacy-authority/`. Nothing else was edited. No commit or push was made.

## Approach

I treated the current drafts (`../wallet-consumers.md`, `../subscription-contracts.md`, `../standards.md`) and the Sol reports as claims to check. The checks used:

- the original requirements text in `design/rounds/r5/e01-prv-privacy.md`, `design/ears/MPE-EARS-INDEX.md` and `design/ears/RECONCILE.md` (DEC-003, DEC-021);
- the shipped `website/dist/moth-connector.js`, `subscriptions.js` and `subscriptions.html`;
- Moth extension source pinned at the commit below.

All public retrieval used the project helper (Scrapling, then PixelRAG 0.4.0 CDP for visual captures). I also read Sol's archived copy of `connector-handlers.ts` from `../sources/sol-wallet/`. It has the same commit pin, and its URL is in that manifest. I did not refetch it. An earlier session ran out of turns before writing this report. This session reused those captures and fetched nothing new. Where this report says I looked at tiles, I opened and read the tile images. The helper's `accepted_source` HTTP heuristic is not treated as proof that a page is on topic.

## Pins and versions observed

| Item | Pin / version | Observed |
|---|---|---|
| Moth wallet `main` HEAD | `d48206a1957af09bf17bf5e941c2b5bccb12db63` (2026-10-01T18:26:33Z, merge of PR #162 `auto-lock-dapp-activity`) | `moth-commits.raw` |
| Midnight DApp connector API `main` HEAD | `612db2b62dbd78c079da62e57e7b8585a204b858` (2026-09-29T15:44:34Z) | `midnight-connector-commits.raw` |
| Moth connector identity | `window.midnight.moth`, `io.shielded.moth`, API `4.0.1` | Sol captures; matches `moth-connector.js` constants |
| Official package | `@midnightntwrk/dapp-connector-api` 4.1.0-beta.1 | Sol captures (not re-verified here) |

## Source findings

**Moth grants are origin-wide, have no expiry and ignore network.** `permissions.ts` stores `{networkId, grantedAt}` under the origin key. `isAllowed(origin)` is just `origin in grants`: it checks neither `networkId` nor age. `revoke(origin)` exists, but it is only reachable from the extension UI messages (`permissionsList`, revoke by `data.origin`). The DApp connector surface has no revoke or disconnect method. Text and tiles are visually confirmed (permissions tile_0000 shows lines 1–41).

**Read methods need no approval once connected.** In `connector-handlers.ts`, `getConfiguration`, `getShieldedBalances`, `getUnshieldedBalances`, `getDustBalance`, `getShieldedAddresses`, `getUnshieldedAddress`, `getDustAddress` and `getTxHistory` only call `requireConnected(origin)`. `signData`, `deriveAppSecret`, `makeIntent`, `makeTransfer` and balancing call `requestApproval`. The approval kinds in `approvals.ts` are `connect | transfer | signData | deriveAppSecret | balance`. So "connected" means any script running on the granted origin can silently read shielded balances, addresses and transaction history.

**`hintUsage` does not narrow anything.** It calls the same `ensureConnected` as `connect`. The comment says "Moth grants per origin all at once". This is allowed by the official spec, which says the DApp "should not assume any particular permission system and its granularity" (`SPECIFICATION.md`, Permissions section).

**Any connector call keeps the wallet unlocked.** After every dispatched method, `if (await isAllowed(origin)) await recordActivity(Date.now())` runs. The code comment says this stops auto-lock from firing between DApp requests, and `enforceAutoLock` reads that activity. A dashboard that polls `getConnectionStatus` would therefore hold the wallet unlocked indefinitely. That is both an authority problem and an exposure-window problem.

**Origin is bound by the wallet.** It comes from `sender.origin` or `new URL(sender.url).origin`, never from page parameters. `deriveAppSecret` folds `origin|domain` into HKDF `info`, and its spec says origin "must come from the connector session, never from DApp-supplied params" (`specs/003-derive-app-secret/spec.md`). This is sound wallet-side isolation. But it isolates by origin only, and that matters for the next finding.

**All Pages project sites under one owner share an origin.** GitHub Pages serves project sites at `<owner>.github.io/<repositoryname>` (GitHub Docs, "Types of GitHub Pages sites" table; visually confirmed in gh-pages tile_0000). The dashboard at `charleshoskinson.github.io/midnight-express/subscriptions.html` therefore has the origin `https://charleshoskinson.github.io`. That origin is shared with the owner's user site and with every other Pages project site of that account. A Moth grant given for the dashboard silently authorises balance, address and history reads from every page on that origin. It also lets those pages request approval-gated operations under an already-trusted origin label, and gives them the same `deriveAppSecret` namespace. I did not check which other Pages sites this account publishes. The risk is structural either way.

**Connector responses are visible to every script on the page.** `content.ts` returns results with `window.postMessage(response, '*')` to the page window. Any script on the page, including third-party scripts, can observe them. The dashboard loads no third-party script today, so this stays a deployment constraint rather than a live leak.

**The shipped adapter is correctly bounded.** `moth-connector.js` checks `navigator.userActivation.isActive` before connecting. It checks identity and exact version, and calls only `connect(networkId)` and `getConnectionStatus()`. It keeps the ConnectedAPI in a closure and invalidates stale results by epoch. It does not poll automatically. I agree with Sol that it does not create a read-only grant, and the dashboard copy says so. The copy does not say that the grant covers the whole `github.io` owner origin.

**The dashboard export is nonsensitive only because the data is mock.** `subscriptions.js` export writes `intents` (selectors), `intentHistory`, cursors, and per-receipt `category` plus `disposition`. Under the real private profile, exactly this data is the subscriber-interest information that MPE-PRV-006 and MPE-PRV-008 protect. The "Nonsensitive" label holds only for mock data.

**Original requirements that bind this work** (exact text from `e01-prv-privacy.md` and `M2`/EARS):
- MPE-PRV-008: private-profile requests must omit topic, Tag, recipient, detection-key and recognised-Envelope selectors.
- MPE-PUB-012: network message content, size and timing must not depend on which Envelopes match.
- MPE-PRV-010 / MPE-CON-039: no automatic network message, acknowledgement or transaction because an Event was recognised.
- MPE-PRV-011: explicit application authorisation before any Event-dependent external action.
- MPE-PRV-007: decryption, topic, recognition and wallet viewing secrets stay inside the subscriber's trusted endpoint.
- MPE-PRV-013: no fallback that changes the leakage contract without explicit selection.
- MPE-CON-006 / MPE-PUB-008: recognition keys and private topics are added only by invitation, through an explicit call.
- MPE-CON-048: no Bus, Store or Indexer output accepted as publisher-authorisation evidence.
- DEC-021: whole shard only for the prototype; selective modes only as labelled opt-in profiles.

## Recommendation: security invariants for the demo and the product

Each invariant names the requirement it protects. These should be written into `wallet-consumers.md` and `subscription-contracts.md` as normative text. The dashboard copy should be updated to match.

**Whole-shard intake and local selection**

- I1 (PRV-008, DEC-021): a local selector, category, `sourceEquals`, profile or contract value never appears in any network request, relay route, shard-discovery query, retention or back-fill request, or log that is shipped off the endpoint. Shard handles describe transport coverage only.
- I2 (PUB-012, PRV-012/013): local backpressure must not reach the network. Examples of local backpressure are `maxInFlight`, queue caps, pause, unsubscribe, quarantine and gap. Whole-shard intake keeps going regardless of local queue state, into its own bounded encrypted retention. If retention is exhausted, the result is a recorded local gap. Throttling or stopping shard intake because of match-dependent pressure would make network timing depend on recognition, so it must not happen. Throttling at shard level for resource reasons is allowed only if it is independent of matches, and it must be shown to the user as a change of profile.
- I3 (PRV-010, CON-039): delivery and processing receipts, cursors and checkpoints stay local. NATS-style "ack" vocabulary from `subscription-contracts.md` describes only local journal state, never a wire message. Any future acknowledgement to a publisher is a separate, explicitly authorised application action under I8, and it carries no recognition timing.
- I4 (PRV-006): selectors, intent history, cursors and per-record dispositions are sensitive local state under the private profile. The export, diagnostics and crash reports either leave them out or require explicit consent that names this disclosure. The demo export label should say "mock data only; real selection state reveals interests".
- I5 (PRV-013, DEC-021): a remote selector or gateway, or any selective reception mode, is a separately named profile. It needs explicit opt-in, a different label in the UI, and its own claim register. It can never be reached as a silent fallback for mobile, overload or retry.

**Membership, recognition keys and evidence**

- I6 (CON-006, PUB-008, PRV-007): recognition keys and private-topic membership enter only by importing an invitation through an explicit call. They are never derived from a wallet connection. They never come from Moth `deriveAppSecret`, whose output is returned to page JavaScript through `postMessage` on a possibly shared origin. They never come from shard discovery. Decryption and recognition secrets never leave the subscriber endpoint, and a browser page is not a trusted endpoint for production keys.
- I7 (CON-048, model `executes:false`): validation receipts, shard intake, anchors, Moth connection status and the dashboard's offline receipts are not evidence of publisher authorisation or of business authority. Category labels are derived local metadata, not sender claims.

**Separating wallet and business authority**

- I8 (PRV-011): connecting a wallet does not grant shard membership, a local watch grant, publisher identity, an agent tool permission or approval of a business action. A watch grant binds a local principal, selector, sink and expiry, and it is revoked locally. An agent's consequential action needs its own human approval that names the action identity `(authorityDomain, executionScope, actionId)`.
- I9 (wallet scope): the demo calls only `connect` and `getConnectionStatus`, and only from a trusted click. It never calls balance, address, history, configuration, `signData`, `deriveAppSecret`, intent, transfer or balancing methods, and it exposes no raw API. This is already true and should stay a tested invariant.
- I10 (wallet lifetime): no periodic or background wallet calls. Every Moth call from a granted origin resets auto-lock, so status checks run only on explicit user action. The current dashboard complies; the invariant is that no polling is ever added.
- I11 (wallet consent text): before the Connect button is enabled, the page names the exact origin being granted (`https://charleshoskinson.github.io` on the public site). It states that the grant covers every page on that origin and lets any page on it read shielded balances, addresses and history without another prompt. It states that the grant does not expire, and that only Moth's own site-permissions UI revokes it. "Disconnect locally" must keep saying that it does not revoke anything.
- I12 (deployment origin): the live Connect button should be enabled only on an origin dedicated to this dashboard, such as a custom domain or subdomain. On the shared `github.io` owner origin it should stay disabled by default or sit behind an explicit acknowledgement. The page should load no third-party script, because connector responses are broadcast to the page window.

**Source permissions and key revocation**

- I13 (revocation): revoking a watch grant stops local selection, decryption-to-delivery and effect preparation as soon as the trusted local system is notified. Queued callbacks recheck permission. Revocation does not imply leaving the shard, and leaving a shard does not revoke the wallet's origin grant. Revoking a source or publisher key affects only future acceptance. Already-disclosed records cannot be recalled. A replay after revocation is shown as history and cannot be acted on. Each revocation domain (wallet origin, watch grant, shard membership, recognition key, source admission) is shown and controlled separately.

## Where existing technology suffices

The shipped Moth adapter already satisfies I9 and I10 and the honest-disconnect part of I11. The dashboard's memory-only state is the right choice for a demo. Whole-shard intake followed by local selection needs no new stack: the existing design (DEC-003 salted PRF tags or trial decryption) supplies recognition. CloudEvents `(source, id)` deduplication and Reactive Streams demand semantics are adequate as long as they stay local (I3).

No new dependencies are needed. Two deployment additions are recommended:
- a dedicated origin for any live wallet connect (I12);
- a Content-Security-Policy that blocks third-party scripts. On GitHub Pages this would be a `<meta http-equiv>` tag, because Pages does not let you set custom headers. That last point is general knowledge, not verified in this session.

## Fit with the data model and its limits

The SubscriptionIntent, Runtime and IncomingRecord split in `subscription-contracts.md` fits the privacy requirements well. It is local, closed, refuses unknown fields, takes no remote URLs or executable selectors, and keeps original wire bytes separate from derived views. Every accepted result keeps `executes:false`. Two gaps remain:

- **Pause and backpressure:** "retained intake may continue" should be strengthened to "shard intake continues independent of local selection state" (I2).
- **Export:** the export path must follow I4.

Limitations of this review:
- I did not test a live Moth extension, any signing, or any network transport.
- The dashboard is unsigned mock data and does not prove production privacy.
- The shared-origin risk is inferred from the documented Pages URL structure plus Moth's origin keying. I did not list the account's other Pages sites.
- The official 4.1.0-beta.1 connector was not re-audited for permission granularity.
- Sol's `connector-handlers.ts` capture was read as archived text, without its own visual check by me. Its commit pin matches my visually confirmed `permissions.ts` capture.
- Side channels (timing at the proof server, envelope size classes, shard participation) are outside the claims made for the dashboard.

## Proposed consensus decisions

- **Adopt I1–I13** as normative text for the demo and the product.
- **Keep the dashboard's connector as it is** (connect plus status only, click-gated, no polling).
- **Fix the consent copy:** add the shared-origin and silent-read warning text (I11).
- **Gate live Connect** on a dedicated origin, or behind an explicit acknowledgement, on the public site (I12).
- **Relabel the export** so the mock-only nonsensitivity claim is explicit (I4).
- **Treat backpressure as local only,** with intake that does not depend on matches (I2).
- **Reject wallet-derived recognition keys** (I6).

## Unresolved objections

- **Disable Connect on `github.io`?** Sol's position is that it may stay, since the adapter is bounded. Mine is that adapter bounds do not limit what other pages on the same origin can do with the grant. This needs an owner decision.
- **Whole-shard bandwidth on mobile and light clients** remains open under DEC-021 / MPE-PRF-021. Any gateway profile must follow I5.
- **Agent consumers:** it is open how a local agent principal gets a recognition key without the key leaving the trusted endpoint (PRV-007), if the agent runs in another process or on another host.
- **Moth issues to report upstream:** grants have no expiry, `isAllowed` ignores network, and silent reads have no per-capability scope. These are allowed by the official spec, but they would warrant upstream issues if Moth is used beyond a demo. I filed nothing.

## Rejected alternatives

- **Using `hintUsage` as a read-only scope:** Moth treats it as a full connect.
- **Reading addresses or balances after connect to personalise the inbox:** this widens disclosure and is not needed.
- **`deriveAppSecret` as a subscription or recognition key:** the secret is exposed to page scripts and bound to the origin, and it conflicts with I6.
- **Server-side or relay category filters:** these violate PRV-008 and DEC-021.
- **Publisher acknowledgements of delivery:** these violate PRV-010 and CON-039.
- **Periodic wallet-status polling:** it keeps the wallet unlocked.
- **Treating local disconnect as revocation:** it does not revoke anything.

## Sources

Archived raw/text/metadata JSON with SHA-256 values are in `../sources/opus-privacy-authority/`. Retrieved 2026-10-05.

| Source | URL | raw SHA-256 (prefix) | Visual |
|---|---|---|---|
| Moth `permissions.ts` (blob view) | https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/permissions.ts | f14257d9… | tile_0000 e8255694…, inspected |
| Moth `content.ts` | https://raw.githubusercontent.com/shieldedtech/moth-wallet/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/entrypoints/content.ts | 6610cb83… | blob capture tile_0000 8b69ecd7… |
| Moth `handlers.ts` (auto-lock) | …/packages/extension/lib/background/handlers.ts | 571de8fd… | text |
| Moth `approvals.ts` | …/packages/extension/lib/background/approvals.ts | 575467d3… | text |
| Moth `background.ts` | …/packages/extension/entrypoints/background.ts | 3a4b4e02… | text |
| Moth `wxt.config.ts` | …/packages/extension/wxt.config.ts | 32642b98… | text |
| Moth derive-app-secret spec | …/specs/003-derive-app-secret/spec.md | 9a5102c7… | text |
| Moth `SECURITY.md` | …/SECURITY.md | 9c93fbc8… | text |
| Moth wallet-service threat model | …/docs/spec/wallet-service/09-threat-model.md | ca7e45f0… | text |
| Moth commits | https://api.github.com/repos/shieldedtech/moth-wallet/commits?per_page=5 | 64ada3bc… | API JSON |
| Midnight connector `SPECIFICATION.md` | https://raw.githubusercontent.com/midnightntwrk/midnight-dapp-connector-api/main/SPECIFICATION.md | d9056e6c… | text (`main`, not commit-pinned in URL; HEAD 612db2b at retrieval) |
| Midnight connector commits | https://api.github.com/repos/midnightntwrk/midnight-dapp-connector-api/commits?per_page=3 | d4a191f8… | API JSON |
| GitHub Pages site types | https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages | f6628a6f… | tile_0000 c010772d…, inspected |
| Moth `connector-handlers.ts` (Sol capture, read only) | https://raw.githubusercontent.com/shieldedtech/moth-wallet/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/connector-handlers.ts | see `../sources/sol-wallet/manifest.json` | none by me |

Recorded failures: GitHub blob-view HTML text extraction drops TypeScript generics and tokenises code into one token per line. For code semantics I relied on raw files or on visual tiles. In `content.ts` the `matches` array value `<all_urls>` was stripped by text extraction. `wxt.config.ts` raw line 70 confirms `<all_urls>` for `web_accessible_resources`.
