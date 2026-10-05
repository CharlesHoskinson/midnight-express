# Wallet and application consumers

A wallet connection establishes a wallet session. It does not establish a Midnight Express publisher identity, transport shard membership, a private local watch grant, or authority to act for a human. A private watch grant binds a local principal and its authorized selector. Transport shard admission and local watch authorization are separate checks; neither follows from wallet connection.

## Verified Moth boundary

The public [Moth repository](https://github.com/shieldedtech/moth-wallet) describes an experimental, unsupported, unaudited reference wallet. Its browser extension actually injects `window.midnight.moth`, with `rdns: io.shielded.moth` and connector API version `4.0.1`. The [pinned injection source](https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/entrypoints/injected.ts) exposes `connect(networkId)`, returning a ConnectedAPI; the [constants](https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/connector/constants.ts) enumerate its capabilities.

The dashboard adapter makes only `connect` and `getConnectionStatus` calls. Discovery reads public provider metadata and never connects. An explicit user click requests a preprod, preview, or undeployed connection. A connection is accepted only when the identity, exact version, required status capability, and returned network match. It never requests balances, addresses, history, key derivation, signatures, proofs, or transactions. The raw ConnectedAPI is kept inside a closure.

**The adapter's read-only behavior is not a read-only wallet grant.** Moth's [permission implementation](https://github.com/shieldedtech/moth-wallet/blob/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/background/connector-handlers.ts) grants an origin as a whole. `hintUsage` also causes connection approval, rather than narrowing that origin grant. Existing grants and an unlocked session may reconnect without a fresh wallet popup. A click remains required by this dashboard.

Disconnect discards the local handle and invalidates pending asynchronous results. Moth does not expose a connector disconnect/revoke method. The user must revoke the site's origin in the extension to remove its persisted grant. A local dashboard disconnect cannot cancel a wallet approval already open. Status checks identify locking, revocation, network changes, and provider replacement; they do not read wallet data. No automatic wallet data access or balance watching is implemented. Metadata identity checks are compatibility checks, not proof that an installed extension is trustworthy.

## Subscription routes

The private profile fans out whole transport shards. The broker receives no business topic, category, or selective filter. A local authorized selector chooses records after whole-shard intake; categories and watch handles belong to the local interface.

| Consumer | Private route | Required separate consent and authority |
|---|---|---|
| Wallet | Whole-shard intake → local authorized selector → wallet notification inbox | User approves a local watch handle and destination. A private watch grant names the local principal; wallet connection alone grants nothing. |
| DApp | Whole-shard intake → local authorized selector → application inbox → presentation | Application principal, local category/selector, grant expiry, cursor, and destination policy. Wallet session is optional and independent. |
| Agent | Whole-shard intake → local authorized selector → durable agent inbox → tool/action gate | Dedicated local principal and watch grant, bounded retention and tool permissions, human approval for consequential actions. No inherited wallet origin grant. |
| Human | Whole-shard intake → local authorized selector → local web inbox | Local watch consent and unsubscribe control; an inbox does not require a wallet. Export to an external notification endpoint is a separate disclosure decision. |

A local watch record binds the consumer principal, local category/selector, network, cursor, grant expiry, and destination. It does not become a broker routing filter. Revocation stops local selection and delivery under a documented retention policy; transport shard membership has its own admission and revocation lifecycle. Removing one local watch does not imply leaving a transport shard, and leaving a shard does not revoke the wallet's persisted origin grant.

Transport shard discovery identifies transport coverage and intake endpoints, never a directory of business interests. Whole-shard replay, retries, and recovery must preserve that boundary. The static dashboard demonstrates intake, local selection, and watch controls with mock events; it implements neither a shard transport nor private authorization.

An optional remote selector or gateway is a weaker disclosure profile: its operator can learn selector interests and selected records. It must be explicitly chosen and labeled with that disclosure, and must not be represented as the private whole-shard default. External agent inboxes and notification services likewise require separate disclosure consent.

## Lifecycle comparison

| Interface | Discovery and consent | Lifecycle and network | Permission implication |
|---|---|---|---|
| Midnight connector / Moth | `window.midnight.<walletId>` metadata; `connect(networkId)` | Versioned InitialAPI → ConnectedAPI; `getConnectionStatus`; validate returned network | Standard API capabilities do not imply Express private local watch grants. Moth currently persists broad per-origin grants. |
| [Cardano CIP-30](https://cips.cardano.org/cip/CIP-0030) | `window.cardano.<wallet>`; `enable()` consent; extension negotiation | Initial API `apiVersion`, `isEnabled`; returned API `getNetworkId` and per-operation failures | Authorized wallet reads/signing interface; no general pubsub membership. Network identity is a number in this interface, not a Midnight network string. |
| [Ethereum EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) | Provider `request` interface; account access restrictions belong to wallet/RPC authorization | `connect`, `disconnect`, `chainChanged`, `accountsChanged`; chain ID is hexadecimal | Provider connection means ability to service RPC; not necessarily authorized account access. Never transplant these events onto Moth. |
| [Wallet Standard](https://github.com/wallet-standard/wallet-standard) used by Solana | Registered wallets and advertised features; `standard:connect` exposes authorized accounts | `standard:events` change listener; optional `standard:disconnect`; accounts advertise chains/features | Feature/version and account-scoped capability checks. Silent connect is only for prior authorization; the dashboard does not use it. |

Moth pins the older package spelling `@midnight-ntwrk/dapp-connector-api` at 4.0.1. The [official current repository](https://github.com/midnightntwrk/midnight-dapp-connector-api) on 2026-10-05 has `@midnightntwrk/dapp-connector-api` 4.1.0-beta.1. The dashboard accepts only the observed 4.0.1 implementation; unsupported versions fail closed until researched and tested.

## Browser adapter contract

Load `moth-connector.js` as a plain script, then create `MothReadOnlyConnector.create({networkId: 'preprod'})`. The object exposes `discover`, `connect`, `disconnect`, `checkStatus`, `getState`, and `subscribe(listener)`; subscription here means local state observation, not a private local watch or transport shard subscription. Call `connect()` synchronously from the trusted button handler and catch errors. State contains `status`, `networkId`, `wallet`, `capabilities`, and `error`. `checkStatus` is a metadata check for an already connected local session. There is no automatic reconnection, storage of wallet data, or raw wallet API escape hatch.

## Evidence and limits

Source snapshots, SHA-256 manifest, and PixelRAG tiles are in `sources/sol-wallet/`. The adapter was checked using synthetic provider fixtures; a real extension connection requires an installed, enabled, unlocked Moth extension and user consent. The screenshot confirms the exact injected identifier, reverse domain, version, and exposed method list. This documents a bounded interface demonstration, not production wallet security or a deployed pubsub service.

## Origin and private-state review

The [independent privacy review](agents/opus-privacy-authority.md) verifies that Moth grants are keyed to origin, persist until revoked in the extension, and allow balance/address/history reads from other scripts on that origin. GitHub Pages project paths under one owner share an origin. The demo therefore names the current origin and requires explicit acknowledgement before Connect. A dedicated production origin is recommended. The adapter never polls: connector activity refreshes Moth auto-lock.

Real watch selectors, revision history and processing dispositions reveal interests. Only the demonstration's synthetic state is nonsensitive. Production export, diagnostics and external callbacks require an explicit disclosure decision. Whole-shard intake stays independent of local matching, pause and consumer demand.
