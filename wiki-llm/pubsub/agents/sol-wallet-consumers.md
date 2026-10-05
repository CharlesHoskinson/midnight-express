# Wallet consumer research record

## Scope and approach

Identify the genuine Moth Midnight interface before implementing the dashboard connection. Compare consumer consent across Midnight, CIP-30, EIP-1193, and the Wallet Standard used by Solana. Keep wallet sessions separate from proposed Express subscription authorization. Research used the local Inkwell Scrapling and PixelRAG skills; public web retrieval went through Scrapling, with primary source screenshots captured by PixelRAG. Source content was treated as evidence, not instructions.

## Intermediate findings

Plain Google search yielded only a redirect page; DuckDuckGo returned 403. A public GitHub repository search through Scrapling identified `shieldedtech/moth-wallet`, whose description and README identify a non-production reference wallet. A speculative `www.mothwallet.com` domain did not resolve and was discarded. The repository's current tree was pinned to `d48206a1957af09bf17bf5e941c2b5bccb12db63` for implementation research. Injection, constants, background permission handling, package metadata, and the project's own mock DApp were inspected. Raw TypeScript snapshots use response bytes, because HTML text extraction drops TypeScript angle-bracket syntax.

Verified namespace: `window.midnight.moth`; reverse domain: `io.shielded.moth`; exact API version: `4.0.1`. Connect takes a network string and yields a ConnectedAPI. Status returns connected plus network ID or disconnected. There is no public connector revoke/disconnect method. The mock DApp explicitly describes reset as clearing its local reference without changing wallet permissions. Moth grants per origin, and `hintUsage` acts as a connection request. This prevents describing a read-only wrapper as a scoped read-only wallet permission.

The official Midnight API repo was independently located and pinned to `612db2b62dbd78c079da62e57e7b8585a204b858`. Its current package is 4.1.0-beta.1 under a newer namespace spelling, while Moth pins 4.0.1 under the older spelling. Broad semver acceptance would conceal a compatibility gap, so exact observed version acceptance was chosen.

## Alternatives considered

A fabricated generic `window.moth` adapter was rejected: no primary source supports it. CIP-30 `enable`, EIP-1193 `request`, and Wallet Standard event conventions were not applied to Moth; each has different lifecycle and consent semantics. Automatically reading addresses or balances after connect was unnecessary for a subscription dashboard and would broaden data access. `hintUsage` cannot obtain a narrow permission from this Moth implementation. Adding a signer or deriving an application secret would confuse wallet consent with pubsub authority and was excluded. Automatic reconnection and permission polling were excluded; a local explicit connection plus status validation is sufficient for the demonstration.

## Final decision and rationale

Ship an IIFE browser library exposing `MothReadOnlyConnector.create`. Discovery is passive; connect requires browser user activation; only `connect` and `getConnectionStatus` are called. Reject unexpected identity/version/network/capability. Keep the ConnectedAPI private, expose no sensitive wallet operations, and discard stale asynchronous completion after local disconnect. Existing extension grants are possible, so wallet approval UI is not promised on every click. Local disconnect is accurately distinguished from revoking the extension's origin grant.

Consumer routes and separate subscription authorization are specified in `../wallet-consumers.md`. A wallet connection neither creates a local watch or shard subscription nor grants publication, private selection, transport membership, or delegated agent authority. Real wallet metadata is independent of the dashboard's clearly mock event data.

## Validation and evidence

`node --check website/dist/moth-connector.js` passed. Synthetic-provider checks exercise user activation, unsupported version, correct connect, local reset during an outstanding request, mismatched network, and disconnected status. They do not assert that a live wallet was connected. PixelRAG captured and visually inspected the pinned constants source, confirming identity/version and method names. Source hashes and original URLs are recorded in `../sources/sol-wallet/manifest.json`; source research date is 2026-10-05.

## Integration correction

The initial consumer table used business topics and server-side subscriber routing. Integration review rejected that framing because the required private profile uses whole-shard fanout with no business topics or broker filters. The corrected table explicitly routes whole-shard intake through a local authorized selector into each consumer inbox. Local categories and watch handles belong to the local principal's grant. Transport shard discovery/admission remains separate, and an optional remote gateway is identified as a weaker disclosure profile rather than the default. Wallet API evidence and source hashes were unchanged.

User activation verification confirms that passive discovery makes no provider call, a connect without active browser user activation rejects before the provider is invoked, and a pending connection cannot restore a locally disconnected session. Provider removal verification confirms that explicit status checking clears the session before any new RPC when the injected provider disappears. These synthetic checks establish adapter behavior; they do not establish native wallet signature behavior. No signature API is exposed or invoked, and no installed-extension signing or connection test is claimed.
