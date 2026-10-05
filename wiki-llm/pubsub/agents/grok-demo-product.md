# Wallet and DApp subscription demo

Role: wallet and DApp product. Research date: 2026-10-05. Repository pin: `5ff9627c30d06837c931fc4783ca271455bdeb1a` (2026-10-04). The subscription page, `website/dist/moth-connector.js`, and `website/dist/subscriptions-fixtures.json` are untracked working-tree files. They are not part of that commit. This note recommends changes. It does not implement them.

## Research approach

Read the product README, website guide, model v0.2 guide, installed profile lock, candidate use cases, and the design's whole-shard rule. Read the same-day subscription drafts as drafts. Re-fetched the public Moth and Midnight connector sources with Scrapling. Discovery used the public GitHub API. PixelRAG CDP screenshots grounded the two Moth files that decide the permission story: the implemented method list and the origin-grant record. `accepted_source` only means HTTP 200 and a long body. The findings below are from reading those bodies and the screenshot tiles.

The first PixelRAG attempt on `permissions.ts` failed: CDP closed with "no close frame received or sent", exit 1, no tiles. That failure says nothing about the file. The retry captured two tiles. Tile 0 shows the grant source at commit `d48206a`. Tile 1 is the blank page tail. The constants capture also produced two tiles. Tile 0 shows `API_VERSION` `4.0.1` and the method list. Tile 1 shows only the trailing type union. Both captures are under `sources/grok-demo-product/`. The overwritten first attempt is recorded in `sources/grok-demo-product/visual-failure.json`.

No installed Moth extension was connected. No browser walk of `subscriptions.html` was run. UI findings are from reading the static script.

## Pins

| Source | Pin | What was checked |
|---|---|---|
| Midnight Express | `5ff9627c30d06837c931fc4783ca271455bdeb1a` | Product, model v0.2, design shard rule |
| Model profiles | `model/profiles/lock.json` and `installed.json` | `rfq.v0.2` `8b5c6b89…`, `invoice.v0.2` `dd3b68c4…`, `agent.v0.2` `beaf501a…`. v0.1 entries are `historical-read-only` |
| Moth `main` | `d48206a1957af09bf17bf5e941c2b5bccb12db63`, committer 2026-10-01T18:26:33Z | Injected API, constants, origin grants, connector dispatch, extension `package.json` `0.14.1`, README status |
| Midnight connector `main` | `612db2b62dbd78c079da62e57e7b8585a204b858`, committer 2026-09-29T15:44:34Z | `package.json` `@midnightntwrk/dapp-connector-api` `4.1.0-beta.1`, `src/api.ts` |

Moth's repo `pushed_at` is 2026-10-02T20:49:52Z. `commits/main` is still `d48206a`. The connector repo `pushed_at` is 2026-10-05T04:43:56Z. `commits/main` is still `612db2b`. Those later push times are not newer `main` commits.

Moth extension dependency: `@midnight-ntwrk/dapp-connector-api` `4.0.1`. Injected identity: `window.midnight.moth`, `rdns` `io.shielded.moth`, `apiVersion` `4.0.1`. GitHub's public description calls Moth a non-production reference. The README at this pin says experimental, unsupported, unaudited, and able to lose assets.

The connector package name at `612db2b` uses the spelling `@midnightntwrk/dapp-connector-api`. Moth still depends on `@midnight-ntwrk/dapp-connector-api`. The committed markdown under `docs/api/` still titles itself v4.0.1. `package.json` says `4.1.0-beta.1`. `src/api.ts` at that pin has `connect(networkId)` and no disconnect method. `ConnectionStatus` is `connected` plus `networkId`, or `disconnected`.

## What Moth actually grants

`permissions.ts` stores one record per origin: `networkId` and `grantedAt`. `isAllowed` is membership of that origin. There is no method allowlist. The screenshot of that file matches the fetched source.

`connect` and `hintUsage` share `ensureConnected`. If the origin is already allowed and the wallet is unlocked, Moth does not prompt, then writes the grant again. If the origin is new or the wallet is locked, the user must approve. Decline throws `Rejected` with "User rejected the connection request". A requested network that is not the wallet's current network throws `InvalidRequest` before the grant, with the wallet network and the requested network in the reason.

`hintUsage` does not read the method names. The handler comment says Moth grants the origin all at once and treats a hint as a connection request. Calling `hintUsage(['getConnectionStatus'])` still runs that origin grant.

After a grant, while the session is unlocked, these calls need no second approval: shielded, unshielded, and dust balances; shielded, unshielded, and dust addresses, including shielded public keys; transaction history; indexer, node, and prover configuration; proving-provider check and prove; `submitTransaction`.

These calls ask again each time: `signData`, `deriveAppSecret`, `balanceSealedTransaction`, `balanceUnsealedTransaction`, `makeIntent`, `makeTransfer`.

`deriveAppSecret` is listed as an extension method, not part of connector API 4.0.1. `submitTransaction` is in the standard API and, at this pin, submits after `requireConnected` with no second approval. An internal comment groups `signData` with balance reads for offscreen lifetime. That comment is not the permission rule. `signData` has its own approval.

`getConnectionStatus` returns `connected` only when the origin is allowed and a session exists. Otherwise it returns `disconnected`. Lock, revocation, and "never granted" are the same status. The spec type has the same two shapes. A connected status whose `networkId` differs from the page's requested network is a separate, visible mismatch. Moth returns the wallet's current network, not a private "granted network" field.

Revoke exists inside the extension (`permissionsRevoke` on an internal message). The page API has no disconnect or revoke method. `NOT_IMPLEMENTED_METHODS` is empty. Every implemented method is live.

A connector call from an already allowed origin records dApp activity (`recordActivity` in `dispatch`). The pinned commit message says auto-lock counts dApp use as activity. A status check is not a balance read. Repeated status checks are still wallet activity. The auto-lock interval was not read and is not specified here.

The current adapter calls only `connect` and `getConnectionStatus`, keeps the ConnectedAPI private, and requires a user activation. That is the right call set. It does not make the origin grant narrow. Any later script on the same origin can call `connect` and receive the full API. If the grant already exists and the wallet is unlocked, that call does not prompt.

## Current simulation, from the static script

The page is an in-memory simulation of local subscriptions. It does not decrypt, transport a shard, or run the model validator in the browser. Fixture rows carry offline receipt objects. This pass did not re-run the validator.

Useful fixture rows, all with `executes: false` on their offline receipts:

- Firm quote. `event:rfq` from `urn:mpe:source:dealer`. Profile `rfq.v0.2`, contract `sha256:8b5c6b89f6019fcb06b479e92f1b3bea340ac500cc218341e368e1ed2093071c`. 100 Share, 123.45 USD per Share, cash 12,345.00 USD, firm, valid 11:00–13:00 UTC, off-chain. Offline result `offchain-quote-valid` at the fixture clock.
- Same occurrence under the later clock. Same source and id. Offline result rejected, reason `quote-validity`.
- Payment observations on `invoice.v0.2`, contract `sha256:dd3b68c4f25c4ca87a57e5e5dda88cb8a1630fa9a1b0ab394744fdf984eb047a`, source `urn:mpe:source:bank`, invoice `invoice:supplier/demo`, payable 500.00 USD, observed amount 250.00 USD. Pending id `event:invoice-pending`, payment `payment:pending`. Final id `event:invoice-final`, payment `payment:demo`, offline result `final-payment-evidence-only`. Reversed id `event:invoice-reversed`, payment `payment:reversed`. Pending and reversed share the offline result name `payment-evidence-pending-or-reversed`. Their business status fields differ.
- Report-write candidate. `event:agent` from `urn:mpe:source:human`. Profile `agent.v0.2`, contract `sha256:beaf501a8fdeefe757c340b1945dcd3e9c7c6e3fb4e00612f724afab7605b330`. `WriteReport` to `sandbox:reports/demo`, budget 5 Step, `maxEffects` 1, human `human:alice`, valid until 13:00 UTC. Offline result `sandbox-candidate-only`.

Contract renewal, credential expiry, and the operations backlog are `unsigned-mock` with null event, context, and wire.

The script's consumer control only changes a help sentence. Wallet, DApp, human, and agent see the same rows and the same actions. The agent sentence says approval fixtures are quarantined until a validator exists. The accepted approval row takes the "awaiting review" path when `offlineCheck.validation` is `accepted`. The generic intake button uses the first row of each category, so a payments subscription receives the pending observation and not the final or reversed rows. Connect errors are collapsed to one sentence. On a disconnected status the page asserts lock, revocation, or a network change. The status value does not carry that cause. Discovery is announced and then replaced. The public constructor name is `MothReadOnlyConnector`. The eyebrow says "proof of concept" and the title says "private inbox". This tab does not decrypt.

A scope control can retarget a live subscription onto an unsigned category. Mock "revoke" and "expire" change a page variable. They do not call Moth. That separation is right, and the labels need to stay that blunt.

## Recommendation

Use one scenario, the buyer quote desk, with two sibling inboxes. Keep Moth connect on the page, pointed at preprod, and disclose the origin-wide grant before the button. Keep local subscriptions independent of that grant. Leave the wire protocol on whole-shard intake. Categories stay local labels.

### Buyer quote desk

The human and the wallet review one firm quote. The DApp reviews the three payment observations for the same invoice. The agent reviews one report-write candidate. Unsigned reminders are a separate group a human can open so the boundary is visible. Wallet, DApp, and agent views do not offer them.

This matches the three installed v0.2 profiles and the first three candidate workflows (quote coordination, payment-status observations, bounded approval). Contract, credential, and operations workflows have no v0.2 profile. Presenting them as equal streams teaches that a category string is a product.

Demo clock remains `2026-10-04T12:00:00.000Z`. On the machine date 2026-10-05 the quote and the approval are historical. The page says that and offers no accept, pay, sign, or execute control.

### Labels

Page title: "Local inbox". Lead: "In-memory simulation of local subscriptions. Nothing is signed, sealed, or sent." Drop "proof of concept" here. That phrase already names the protocol experiments.

Wallet panel title: "Moth connection". Body, in ordinary sentences:

"Moth 0.14.1 is an experimental, unaudited reference wallet. Connect grants the origin shown here, for every connector method this Moth build implements. This page calls connect and getConnectionStatus only. Other scripts on this origin can use the grant while the wallet is unlocked. Disconnect on this page drops the page's handle. Revoke the origin in Moth to remove the grant. The wallet must already be on preprod."

Print `location.origin` in that panel. Then two short groups, using the method names:

"After the grant, while unlocked, without another prompt: balances, addresses, transaction history, service configuration, proving, and submitTransaction."

"Asks each time: signData, deriveAppSecret, balancing a transaction, makeIntent, and makeTransfer. hintUsage does not narrow the grant."

Do not label the control "read-only". Rename the constructor if the page or a reviewer can see it. `MothConnection` matches the behavior.

Stream titles:

- "Firm quote, 100 Share at 123.45 USD"
- "Payment observation, pending, 250.00 of 500.00 USD"
- "Payment observation, final assertion, 250.00 of 500.00 USD"
- "Payment observation, reversed, 250.00 of 500.00 USD"
- "Report-write candidate, sandbox report"
- "Unsigned reminder, contract renewal"
- "Unsigned reminder, credential expiry"
- "Unsigned reminder, operations backlog"

The rejected quote is "Same quote occurrence, rejected at the later clock", with source `urn:mpe:source:dealer` and id `event:rfq` shown. It is not a second quote.

User-facing payment status is Pending, Final, or Reversed. The offline result can sit on a second line. Pending and reversed must not share one title just because their offline result name matches.

Consumer sentences:

- Human: "Review the quote, the payment observations, and the report-write candidate. Unsigned reminders are separate and have no profile."
- Wallet: "Show the firm quote and the payment observations. Connecting Moth does not subscribe and does not make the quote acceptable."
- DApp: "Show the three installed profiles and their contract ids. Unsigned reminders stay out of this view."
- Agent: "Show the report-write candidate. The offline result is a sandbox candidate. It executes nothing."

Keep the real bounds on a subscription: 2 in flight, 4 queued, 16,384 bytes, 64 journal originals. Those are limits. Do not add a count of streams, modes, or checks to the page. Do not write the agent as an AI persona. Moth's README mentions coding agents. That sentence stays out of this UI.

Each profile row shows the profile id and the contract sha256. Unsigned rows say "No model profile. mock-only."

### Discover, connect, errors, revocation

Discover reads `window.midnight.moth` and compares `rdns`, `apiVersion` `4.0.1`, and `connect`. It does not call `connect`. The result stays in the wallet panel, not only in a live announcement.

Connect runs from the button click, on preprod, and preserves distinct failures:

- No user activation: do not call the provider. Say "Connect requires a click."
- Extension missing, wrong `rdns`, or version other than `4.0.1`: name the observed version and say this page accepts 4.0.1 only.
- User decline: show Moth's `Rejected` reason.
- Wallet on another network: show Moth's `InvalidRequest` reason, including both network ids.
- Connected API without `getConnectionStatus`, or a status that is not connected to preprod: stay disconnected.
- Provider object replaced during the call: drop the handle and say to reconnect explicitly.
- Any other thrown reason: show that reason. Do not replace it with one generic sentence.

A successful connect shows connected, Moth, preprod, and the call actually made (`getConnectionStatus`). It adds no subscription, changes no mock permission, and displays no balance, address, history, or signature.

Do not promise a popup. If this origin is already granted and the wallet is unlocked, Moth reconnects without one.

"Disconnect locally" drops the page handle and pending results. The panel keeps the sentence that the origin grant remains until revoked in Moth.

"Check wallet status" is a button. Do not poll. If the status is `disconnected`, say "Moth reports disconnected. A locked wallet, a revoked origin, and no grant look the same here." If the status is `connected` to a different network, say the network changed and drop the local handle. The grant can still exist.

Mock "Expire local permission" and "Revoke local permission" stay, under the heading "Simulation permission". Their result text says the Moth grant was not changed. Connecting Moth while simulation permission is expired or revoked does not resume intake. Resetting the simulation does not revoke Moth.

### Local subscriptions

Wallet view offers the firm quote and the three payment observations. DApp view offers those plus the report-write candidate, each with its profile and contract. Agent view offers the report-write candidate only. Human view offers the three profiles and, below a separate heading, the unsigned reminders.

One local subscription per profile, not per decorative category list. Payments are one subscription whose inbox shows Pending, Final, and Reversed. A visible local control can narrow that inbox to the final assertion. The default is all three. That control is a local view. It is not a GossipSub topic and it is not sent anywhere.

Deliver buttons name the row: "Deliver firm quote", "Deliver pending observation", "Deliver final assertion", "Deliver reversed observation", "Deliver report-write candidate". Remove the generic intake button that silently selects the pending payment.

The same-occurrence rejected quote is an explicit action, "Review the same quote at the later clock". If the firm quote was already delivered, the inbox says both rows share `urn:mpe:source:dealer` and `event:rfq`, and the later clock rejects it. If the rejected row is delivered first, a later firm-quote delivery says the occurrence was already seen. Do not present that as a new quote the user missed.

Pause, resume, unsubscribe, gap, and the in-flight bounds stay. Unsubscribe is a tombstone. It does not claim to erase history or to leave a shard. There is no shard here. Gap text stays: the cursor does not jump, and accepting the gap is a new revision. "Mark reviewed" applies only to a row awaiting review, and the result is "Reviewed locally. Nothing executed." A quarantined row's action is "Record quarantine", and the label stays quarantined.

A scope change is a new revision. Rows already delivered keep their original titles. The scope control cannot move a profile subscription onto an unsigned reminder.

Export stays a nonsensitive simulation file: clock, consumer, simulation permission, local intents, cursors, dispositions. No wallet payload and no claim of authority.

## Testable requirements

These are checks for a later edit. This pass did not execute them.

- With no extension, Discover leaves a persistent "Moth extension not detected." The subscription list is unchanged and `connect` is not called.
- A provider with a different version or `rdns` is rejected by name. A provider with `io.shielded.moth` and `4.0.1` can be discovered without connecting.
- Connect from a handler without user activation throws before the provider is called.
- A declined approval and a network mismatch produce different visible sentences, matching Moth's `Rejected` and `InvalidRequest` reasons.
- A successful connect does not create a subscription, does not flip simulation permission, and does not render a balance or address.
- Local disconnect clears the handle. The panel still says the origin grant remains. A following status check does not use a discarded API object.
- A `disconnected` status does not claim a single cause. A connected status for another network names that network and clears the handle.
- Wallet view has no report-write subscribe button and no unsigned reminder. Agent view has no quote or payment button and no sign, prove, or transfer button. DApp view shows the three contract ids from the lock file.
- Delivering the firm quote shows 100 Share, 123.45 USD per Share, cash 12,345.00 USD, firm, valid until 2026-10-04T13:00:00.000Z, off-chain, historical relative to the machine date, `executes` false. There is no accept control.
- Delivering the three payment rows shows three ids (`event:invoice-pending`, `event:invoice-final`, `event:invoice-reversed`) and the statuses Pending, Final, and Reversed. The final row has no pay control.
- The report-write row shows `WriteReport`, `sandbox:reports/demo`, 5 Step, and `executes` false.
- Simulation revoke stops delivery. A later Moth connect does not resume it. Reset clears the inbox and does not claim to revoke Moth.
- The page copy contains no stream count, mode count, or test count, and it does not call this tab a proof of concept or a private decryption inbox.

## Data-model fit

The quote row fits `rfq.v0.2`. It is enough to show a person an exact firm price, a quantity, a cash total, and an exclusive expiry. It is an off-chain observation. The desk must not grow an accept or settle action. v0.2 does not execute one.

The payment rows fit `invoice.v0.2`. They are enough to show a treasury view that a 250.00 USD observation against a 500.00 USD payable is pending, a final assertion, or reversed. Final remains a source assertion. The desk must not mark the invoice paid and must not send a payment. Collapsing Pending and Reversed into the shared offline result name would hide the distinction the inbox is for. A final-only control is a visible local filter, defaulting to all three observations.

The approval row fits `agent.v0.2`. It is enough to show a named human, a sandbox target, a 5 Step budget, and an expiry. The result is a candidate. The agent view records review. It does not prepare a tool, derive a secret, or sign.

Unsigned reminders do not fit a profile. They stay out of model dispatch. Their contract label is `mock-only`. They have no occurrence identity. Replaying one can create another mock row. The UI says so.

v0.1 profiles stay historical. The demo does not offer them.

A subscription does not belong inside a business event. The local intent (profile, contract, predicate, cursor, sink, simulation permission) stays in the page. Selectors are local labels after a whole-shard intake that this page only pretends to have finished. They are not GossipSub topics. The design's shard topic is the shard, and carried topic values stay inside the sealed body (`MPE-FMT-058`). This page has no sealed body and must not invent one. `wire` stays null.

Candidate product rules that already match this desk, still unapproved: cancel stops further callbacks (`MPE-PRD-001`), demand bounds delivery (`MPE-PRD-003`), an expired quote is not executed (`MPE-PRD-005`), and notification consent is separate from authority (`MPE-PRD-013`). None of those is satisfied by this simulation. The simulation can illustrate the local half of the first, third, and fifth only.

## What is already enough

The static page, the three v0.2 fixtures, and a Moth adapter that calls `connect` and `getConnectionStatus` are enough for this mock, after the label, view, and error changes above. No NATS, MCP, A2A, WalletConnect, push service, IndexedDB, or signing library belongs in the mock. IndexedDB would look like a durable receipt the journal does not have. A second wallet API would hide the Moth grant this demo exists to show.

The real stack still needs, outside this mock: whole-shard intake, sealed envelopes, a permission service that is not a Moth origin grant, authenticated sources, and a human approval UI that can actually sign. Those are deployment gates in the model guide. This page must not grow them in miniature.

## Rejected alternatives

- Treat `hintUsage(['getConnectionStatus'])` as a read-only grant. At `d48206a` the names are ignored and the origin is granted.
- Describe the adapter as a read-only wallet permission because it refrains from calling other methods. The grant is origin-wide, and other scripts on the origin can call the rest.
- Import CIP-30 `enable`, EIP-1193 accounts, or Wallet Standard `standard:disconnect` as Moth's lifecycle. Moth's page API is `connect(networkId)` and `getConnectionStatus`. Revoke is inside the extension.
- Accept connector `4.1.0-beta.1` or the renamed package while Moth reports `4.0.1` on the older package spelling. `src/api.ts` at `612db2b` still has no disconnect. Fail closed on the observed version.
- Use the other public connector repositories returned by GitHub search (`losxhve/midnight-dapp-connector`, `LeastAuthority/midnight-dapp-connector-api`, `BossChaos/midnight-dapp-connector-demo`, `bochaco/react-mn-wallet-connect`). The canonical API repository is `midnightntwrk/midnight-dapp-connector-api`. The wallet under test is `shieldedtech/moth-wallet`.
- Make six categories equal streams, or let one "simulate intake" button stand for every payment status.
- Default the DApp to a final-only subscription. The useful invoice desk shows pending, final, and reversed. The final-only control can exist as a visible local filter.
- Poll wallet status, read balances after connect, or add a pay, accept, sign, or prove button.
- Put business categories onto the network. Shard fanout and local recognition stay the wire rule.
- Call this tab a protocol proof of concept, a private inbox, or an AI agent.

## Consensus proposals

1. The mock scenario is the buyer quote desk: one firm quote, three payment observations for one invoice, and one report-write candidate. Unsigned reminders are labeled and excluded from wallet, DApp, and agent views.
2. Local profile labels and the optional final-only payment view are page state. They are not network topics, broker filters, or fields inside a v0.2 event.
3. The genuine connector is Moth at `d48206a`, API `4.0.1`, `io.shielded.moth`, extension `0.14.1`, network preprod. The page calls `connect` and `getConnectionStatus` only. The disclosure lists the origin and the silent versus prompted capabilities above. `hintUsage` is not used to pretend the grant is narrow.
4. Local disconnect is not revocation. Disconnected status is ambiguous. Error text preserves Moth's reason. Simulation permission and the Moth grant are separate controls, and neither repairs the other.
5. The mock stays unsigned. No sealed wire is fabricated. Offline rows keep `executes: false`. The quote and the approval stay historical at the fixture clock. No signing or payment authority is added.
6. Versions other than Moth `4.0.1` fail closed until a later pin is read the same way.

## Unresolved objections

- A public page origin is a wide grant boundary. This recommendation keeps Connect and prints the origin, because the task is a genuine connector with an honest disclosure. The opposing position is to show Connect only on a loopback origin. That should be decided explicitly. Hiding the panel would avoid the disclosure rather than settle it.
- `submitTransaction` has no second prompt at this pin. A later Moth commit may add one. Do not document that behavior past `d48206a`. The same limit applies to proving without a second prompt.
- The connector package is `4.1.0-beta.1` while its committed API markdown still says v4.0.1. This pass did not review every change between those labels. Fail closed stands until Moth reports a new `apiVersion`.
- Same-day drafts (`wallet-consumers.md`, `subscription-contracts.md`, `data-model-fit.json`) agree that the adapter's call list is not a read-only grant and that categories are local. They were not treated as proof. The capability split, the ignored `hintUsage` names, the ambiguous status, and the buyer-quote scenario are from this pass.
- The fixture file embeds offline validator receipts. This pass did not re-execute the validator. The desk uses the profile lock, the model guide, and the fixture fields. A receipt label is not live authority.
- No live extension was connected. Popup timing, `file://` origins, and the auto-lock interval are unread. The activity hook is the `recordActivity` call in `dispatch`, which is enough to forbid polling.

## Source URLs

- https://github.com/shieldedtech/moth-wallet
- https://github.com/shieldedtech/moth-wallet/commit/d48206a1957af09bf17bf5e941c2b5bccb12db63
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/connector/constants.ts
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/permissions.ts
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/entrypoints/injected.ts
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/connector-handlers.ts
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/package.json
- https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/README.md
- https://github.com/midnightntwrk/midnight-dapp-connector-api
- https://github.com/midnightntwrk/midnight-dapp-connector-api/commit/612db2b62dbd78c079da62e57e7b8585a204b858
- https://github.com/midnightntwrk/midnight-dapp-connector-api/blob/612db2b62dbd78c079da62e57e7b8585a204b858/package.json
- https://github.com/midnightntwrk/midnight-dapp-connector-api/blob/612db2b62dbd78c079da62e57e7b8585a204b858/src/api.ts

Raw SHA-256 values for the fetched bodies are in the sibling `.json` files under `sources/grok-demo-product/`. Code was read from the `.raw` bodies. Text extraction drops TypeScript type punctuation, so the `.txt` extracts are not the source for method signatures.

Visual tiles that were inspected:

- `sources/grok-demo-product/moth-constants-visual-tiles/github.com_shieldedtech_moth-wallet_blob_d48206a1957af09bf17bf5e941c2b5bccb12db63_packages_extension_lib_connector_constants.ts.png.tiles/tile_0000.jpg` (`7b458234edb4d295dd4ac6fd39ed54bad32c5df955a2c20546a37df598eed3fa`)
- `sources/grok-demo-product/moth-constants-visual-tiles/.../tile_0001.jpg` (`49917f8645724e95edbbbde188623cd74bc12c2be4fbb7b5d95ae5ce7eed2893`)
- `sources/grok-demo-product/moth-permissions-visual-tiles/github.com_shieldedtech_moth-wallet_blob_d48206a1957af09bf17bf5e941c2b5bccb12db63_packages_extension_lib_background_permissions.ts.png.tiles/tile_0000.jpg` (`e8255694a67b18906ceb0b789b6baadd1e284a10ea1a08f6b59d6a9ac5ee7a7b`)
- `sources/grok-demo-product/moth-permissions-visual-tiles/.../tile_0001.jpg` (`8a0d749c02a9391f6d2f25c545eb274c18d9255642bcb81add3aae367c90f122`)

## Decision notes

The useful demo is the one a person can finish: see a firm quote that is already historical, see three different payment observations without paying, and see one sandbox candidate without running it. Moth is on that page only to make the wallet boundary real. The boundary at `d48206a` is an origin grant, not a read scope, and the copy has to say what that grant includes. The existing static stack can carry that mock. It cannot carry the protocol.
