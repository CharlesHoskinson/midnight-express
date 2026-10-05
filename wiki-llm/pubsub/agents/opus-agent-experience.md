# Agent platform research: agent experience for local subscriptions

Role: agent platform principal engineer. Owned outputs: this report and `../sources/opus-agent-experience/`. No implementation, other document, commit or push was changed. Research date: 2026-10-05.

## Approach

I tested `../standards.md`, `../subscription-contracts.md` and `../wallet-consumers.md` against the current primary agent protocol sources, and checked them against the shipped mock dashboard and the Moth connector. All web retrieval used Scrapling through `research.py`. Each capture keeps its `.raw` bytes, the extracted `.txt`, and a `.json` record with the URL, UTC time, status and SHA-256 digests. Version pins come from GitHub public API captures of releases, tags and commits. I read the normative text myself; the helper's `accepted_source` flag is only an HTTP heuristic.

This session's earlier run reached its turn limit before it wrote this report. This report draws on that run's captures and doesn't refetch them. One primary page was captured visually in this pass (see below).

**Genuine failure recorded:** `https://modelcontextprotocol.io/specification/2026-07-28/server/discovery` returned 404 (`mcp-discovery.json`, `accepted_source: false`). The correct page is `server/discover` (`mcp-discover-md`). The 404 page isn't used as evidence. The security best-practices URL under `/specification/` redirected to `/docs/2026-07-28/tutorials/security/security_best_practices`, and the report cites the resolved page.

**Visual grounding:** PixelRAG pixelshot 0.4.0 used the CPU CDP backend to capture the [MCP Extension Support Matrix](https://modelcontextprotocol.io/extensions/client-matrix) as two tiles. I inspected `tile_0000.jpg` (SHA-256 `d2b6973e1c382566ff38cf76a2cb6d442bf8f76784ceb2a37eaeba5a2cf0942e`); its capture record is `mcp-client-matrix-visual.json`. This capture was needed because text extraction loses the checkmark icons in that table, so the text alone can't show which clients support what. The tile visibly shows four official extensions: MCP Apps (`io.modelcontextprotocol/ui`), OAuth Client Credentials, Enterprise-Managed Authorization and Skills. Claude (web), Claude Desktop, VS Code GitHub Copilot, Microsoft 365 Copilot, Goose, Postman, MCPJam, ChatGPT, Cursor, Archestra.AI and PostHog Code are checked for MCP Apps. ChatGPT, fast-agent and MCP Inspector show "Partial" for Skills. **The Tasks extension does not appear in the matrix at all.** The page labels the matrix community-maintained, so this is a support claim, not a conformance test. The sol-standards visuals of the MCP changelog and subscription pages already exist and weren't repeated. Every other source here is grounded in text only.

## Current versions and pins observed 2026-10-05

| Artifact | Pin | Evidence |
|---|---|---|
| MCP specification | `2026-07-28` tag → `5f5440bb26a6`. Prior tag `2025-11-25` → `38c84e9f93ad`. Repository head `75db1e987cbb` (2026-10-03) | `gh-mcp-spec-tags`, `gh-mcp-spec-commits` |
| MCP Python SDK | v2.3.0 (2026-10-02). Its release notes cover 2026-07-28 connections, `server/discover`, and `MCPServer(subscriptions=False)` for opting out of `subscriptions/listen`. The v1.30.0 line is still maintained | `gh-mcp-py-releases` |
| MCP TypeScript SDK | v2.3.1 and `@modelcontextprotocol/server@2.3.1` (2026-10-05). The 1.32.1 legacy line was released the same day. The captured release bodies don't name the 2026-07-28 features, so TS support for `subscriptions/listen` is **unverified** here | `gh-mcp-ts-releases` |
| MCP Tasks extension | `modelcontextprotocol/ext-tasks` v0.2.2, commit `5246bc3d0253` (2026-09-30) | `gh-mcp-ext-tasks` |
| MCP Apps extension | `modelcontextprotocol/ext-apps` v2.0.3 (2026-09-25) | `gh-mcp-ext-apps-releases` |
| A2A | v1.0.1 (2026-05-28), v1.0.0 (2026-03-12). Spec captured at the `v1.0.1` raw tag. `a2a-python` v1.2.2 (2026-10-05) | `gh-a2a-releases`, `a2a-spec-md`, `gh-a2a-py-releases` |
| AG-UI | Dated releases, latest `release/2026-10-05`; main `3092a4bea391`. Its `llms.txt` index now lists both `spec/1.0` and `spec/draft` pages | `gh-agui-releases`, `gh-agui-commits`, `agui-llms` |
| Moth wallet | `shieldedtech/moth-wallet` head `d48206a1957a` (2026-10-01), the same commit sol-wallet pinned | `gh-moth-commits` |
| Midnight DApp connector API | head `612db2b62dbd` (2026-09-29), matching the sol-wallet pin | `gh-dapp-connector-commits` |

`../standards.md` points at A2A `latest` and AG-UI without a version. Implementation should pin A2A v1.0.1 and AG-UI spec 1.0 plus a dated release instead.

## Source findings that change or sharpen the draft

**MCP 2026-07-28 is stateless and handle-oriented.** The [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) removes `initialize`, sessions and `Mcp-Session-Id`. Every request now carries its protocol version and client capabilities in `_meta`, and servers MUST implement [`server/discover`](https://modelcontextprotocol.io/specification/2026-07-28/server/discover). Servers that need state across calls use "explicit, server-minted handles passed as ordinary tool arguments". [SEP-2567](https://modelcontextprotocol.io/seps/2567-sessionless-mcp.md) (Final) gives the reason: deployed hosts scope sessions inconsistently, and some close a session after every tool call. This independently confirms the draft's opaque `watch` handle design. It also rules out any watch state tied to an MCP connection.

**Notifications are lossy invalidation, not delivery.** [`subscriptions/listen`](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions) replaces `resources/subscribe` and the HTTP GET stream. The server acknowledges with the subset of the filter it will honor. `notifications/resources/updated` carries only a URI and the subscription ID. On stdio, the server keeps no subscription state across reconnects. The changelog also **removes SSE resumability and `Last-Event-ID`**: a broken stream loses its in-flight request. A notification can therefore be lost with no replay, which makes the local durable cursor the only completeness mechanism. The draft's "invalidate, then bounded read" rule is correct. It should add that a missed notification is normal, and that the agent must also read on reconnect and on a timer.

**Tool and resource lists may vary by authorization, not by connection.** In the [tools spec](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), `tools/list` MUST NOT vary per connection or as a side effect of other requests. It MAY vary by the authorization presented on the request. The same spec makes tool annotations untrusted unless the server is trusted. It also warns that `x-mcp-header` values are visible to intermediaries, so sensitive parameters must not be mapped to headers. So a watch handle or selector must never become an `x-mcp-header`. Capability scoping has to come from per-request credentials, or on stdio from the identity of the server process, not from a "connected" flag.

**Caching is now normative.** [Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching) requires `ttlMs` and `cacheScope` on list and read results. `"private"` responses MUST NOT be shared across authorization contexts. The spec separately says servers MUST NOT rely on `cacheScope` alone for access control. Watch resources and their reads must be `private` with `ttlMs: 0`. The static `tools/list` may be `public` only if tool names and descriptions say nothing about a principal's interests.

**Server-initiated prompts can't come from event arrival.** [SEP-2260](https://modelcontextprotocol.io/seps/2260-Require-Server-requests-to-be-associated-with-Client-requests.md) (Final) and the [MRTR pattern](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr) allow elicitation and similar requests only inside an originating client request, as an `InputRequiredResult` with opaque `requestState`. An arriving MPE event therefore cannot make an MCP server ask the user anything. Agent wake-up is a host policy, outside the protocol. [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation) forbids collecting secrets or payment credentials in form mode and requires URL mode for them. The changelog deprecates Roots, Sampling and Logging (SEP-2577), so new Midnight Express adapters should not adopt them.

**The Tasks extension is real, but client support isn't demonstrated.** The [Tasks extension](https://modelcontextprotocol.io/extensions/tasks/overview) defines a durable `taskId` with a TTL and `pollIntervalMs`. Its states are `working`, `input_required`, `completed`, `failed` and `cancelled`, and cancellation is cooperative. Polling is the default, and `notifications/tasks` is opt-in via `subscriptions/listen`. The visual client matrix lists no client support for Tasks. The draft is right to confine Tasks to finite operations; additionally, nothing should require it.

**Local transport hardening is normative.** [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) servers MUST validate `Origin` against DNS rebinding and SHOULD bind to 127.0.0.1 when local. [SEP-1024](https://modelcontextprotocol.io/seps/1024-mcp-client-security-requirements-for-local-server-.md) (Final) requires clients with one-click local installation to show the exact, untruncated command and get consent. The [security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) forbid token passthrough and describe SSRF defenses: block private ranges and treat redirects as suspect.

**MCP Apps is the widely supported human-supervision surface.** [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) renders HTML in a host-controlled sandboxed iframe, and apps can ask the host to invoke tools subject to user consent. The visual matrix shows broad host support. That makes MCP Apps more broadly deployed today than AG-UI for the inside-the-agent-host case.

**A2A v1.0.1 is task-scoped.** In the [v1.0.1 specification](https://raw.githubusercontent.com/a2aproject/A2A/v1.0.1/docs/specification.md), `SubscribeToTask` is unavailable on terminal tasks. Its stream MUST begin with the current Task and MUST end at a terminal state. Push notifications are webhook POSTs to a URL the client registers. The extended Agent Card requires authentication with a declared scheme. [Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/) offers well-known URIs, curated registries and direct private configuration. None of this is an indefinite private feed, and only direct configuration avoids publishing a capability.

**AG-UI is a frontend event protocol.** It now exposes 1.0 pages for capabilities, interrupt/resume and its processing model ([AG-UI introduction](https://docs.ag-ui.com/introduction), [index](https://docs.ag-ui.com/llms.txt)). Its shared state can be read-write, and interrupts provide approve, edit and retry. An AG-UI interrupt approval is a UI decision, not a wallet signature or an MPE authority result.

## Challenges to the current drafts

- `../standards.md` describes MCP correctly but leaves out four consequences of the current spec: lost notifications are unrecoverable, private caching is mandatory, per-connection tool scoping is forbidden, and server-initiated prompts are impossible. Each changes adapter design.
- The draft's "No promise that host autonomously wakes an agent" is right. The UX should go further: give the agent a pull-first loop, and give the human a separate notification surface (dashboard or wallet inbox) that doesn't depend on the agent host at all.
- The draft treats MCP and AG-UI as the agent and human adapters. On the evidence above, MCP Apps should be the first candidate for in-host supervision, with AG-UI reserved for custom agent frontends.
- The draft's `action.prepare` needs a defined approval channel. MRTR URL-mode elicitation fits: the MCP client never sees the approval content, and the human approves in the local dashboard or the wallet. Form-mode elicitation and AG-UI interrupts must not count as consequential approval.
- `../wallet-consumers.md` correctly says the agent gets no inherited wallet origin grant. A new risk follows from MCP Apps: Moth grants per origin, and an MCP App runs in a host-chosen sandbox origin that other apps may share. Connecting Moth from inside an MCP App could bind a broad origin grant to a host sandbox origin. I did not verify how hosts assign those origins. **Recommendation:** don't call the Moth connector from inside MCP Apps or AG-UI frontends; wallet connection stays in the first-party dashboard origin.
- The shipped mock dashboard (`website/dist/subscriptions.js`) has no agent-facing API and keeps all state in browser memory, apart from loading its own fixture manifest. Using it for an agent demo needs a local adapter process. Browser globals or `postMessage` should not be exposed to agents.

## Recommendation: a safe agent experience

**One local consumer service, several thin adapters.** The durable journal and watch service from `../subscription-contracts.md` stays authoritative. The human dashboard, wallet inbox, an MCP 2026-07-28 adapter and an optional A2A gateway are all clients of that service. None of them extends the MPE wire. Selectors stay local and are never sent upstream.

**Discovery is explicit and local.** Use no mDNS, public Agent Card or well-known URI for private watches. An agent host learns about the service in one of two ways:
- A stdio launch command that the user consents to (SEP-1024 behavior). This is preferred, because each agent principal gets its own server process and grant.
- A loopback Streamable HTTP endpoint bound to 127.0.0.1 that enforces an `Origin` allowlist and requires a per-agent bearer credential.

`server/discover` advertises the exact protocol version `2026-07-28`, the capabilities and `extensions`. The legacy `2025-11-25` profile is a separate, separately tested build, offered only if a real client needs it.

**Capabilities are a grant object, not a connection.** Add an agent watch grant, kept separate from wallet sessions, with these closed fields:
- `grantId`, `principal` and `agentLabel`, where the label is informational. `clientInfo` is self-asserted and never identity.
- `watchHandles`
- `readableFields`, for example category, profile, validation status, `businessDigest` and display summary
- `maxRecordsPerRead`, `maxBytesPerRead` and `maxReadsPerMinute`
- `expiresAt`
- `actionScopes`, empty by default
- `transport`, either stdio or loopback HTTP

A stdio process is bound to exactly one grant. On HTTP, the grant is resolved from the per-request credential, so `tools/list` can vary by authorization as MCP allows. Revocation takes effect on the next request. A handle is opaque and unguessable but never sufficient on its own: the server checks that the presented authorization owns it.

**Tools (proposed application names, not MCP standard methods):**
- `watch_list`
- `watch_read(handle, cursor, limit, maxBytes)`. Returns `records`, `nextCursor`, and `coverage {highWater, oldestRetained, gap}`.
- `watch_commit(handle, cursor, dispositions)`. Changes only local processing state.
- `watch_pause` and `watch_resume`.
- `action_prepare(recordId, actionScope)`. Only when the grant has action scopes. Returns a pending approval and never executes.

`watch_create` and grant changes stay human-only in the dashboard, so an agent can't widen its own scope. Mark read tools `readOnlyHint`, while remembering that clients treat annotations as hints. Use `outputSchema` and `structuredContent`.

**Bounded pull with invalidation hints.** Resource `mpe-local://watch/{opaque}` reports changes through `subscriptions/listen`. The agent's loop is: read on startup, read on each notification, read on reconnect, and read on a slow timer. A notification is never a delivery receipt. Reads are capped by the grant. A stale cursor returns an explicit gap and never silently jumps to latest. All read results are `cacheScope: "private"`, `ttlMs: 0`.

**Untrusted content isolation.** Record fields that come from senders, such as display text, memos and names, are adversarial input to an LLM. The agent sees validated typed fields by default. Free text is length-capped, returned in a separately labeled `untrustedText` field, and never concatenated into tool descriptions or resource names. The validator's `executes:false` result passes through unchanged. An event can never add tools, change grants or carry instructions that the adapter acts on.

**Callback isolation.** There are no webhooks by default. A2A push or any outbound callback requires all of the following:
- an explicit disclosure decision
- a registered HTTPS endpoint
- the MCP/OWASP SSRF defenses (private-range blocking, no redirect following)
- payload minimization to a handle plus a coverage hint, so the receiver reads back over an authenticated pull
- per-endpoint credentials that are never passed through

Local callbacks run outside the journal's transaction and recheck the grant before each effect.

**Consequential actions leave the agent channel.** `action_prepare` records an action with the stable identity `(authorityDomain, executionScope, actionId)`. It answers with an MRTR URL-mode input request pointing at the local dashboard approval page on the first-party loopback origin. The human approves there. Anything needing a signature goes through the wallet's own UI. The agent then retries and sees the outcome. Neither MCP elicitation form mode, AG-UI interrupts nor MCP Apps buttons count as authority.

**Long work and remote agents.** Use the MCP Tasks extension only for finite, explicitly requested work such as historical re-validation, and only after negotiating it in `extensions`, with polling as the baseline. Use an A2A v1.0.1 gateway only for commissioned remote agent tasks. Its Agent Card is privately configured, authenticated and minimal, and task streams end with the task.

## Where existing technology suffices and what to add

These suffice, used as published: the MCP 2026-07-28 core (stateless metadata, `server/discover`, `subscriptions/listen`, caching hints, MRTR, URL-mode elicitation), the Python SDK v2.3.x (its notes confirm 2026-07-28 subscriptions and discovery), MCP Apps for in-host supervision, and the existing static dashboard and read-only Moth connector for the human and wallet side.

Additions needed:
- A small local adapter process (Python SDK is the lowest-risk choice given the release evidence) that wraps the journal and watch service.
- The agent watch grant record.
- A dashboard approval page reachable on a first-party loopback origin.
- Pinned interoperability tests against at least one real host.

Nothing on the network side is added. A2A, AG-UI, Tasks and webhooks are optional and off by default. No new identity registry or DID dependency is needed for local agents.

## Data-model fit and limitations

The existing closed records fit the agent experience well. `LocalSubscriptionIntent` already has the owner, opaque handles, bounded sinks and an exclusive cursor. The runtime record exposes `gap`, `inFlight` and queue bounds, which map directly to `coverage` and read limits. `IncomingRecord` distinguishes `unsigned-mock` from `v0.2-fixture` and keeps `validation` separate. The validation result's `executes:false` is exactly the property an agent channel needs. Approval occurrence and action identity rules prevent replay from renewing authority.

Gaps:
- There is no record for a principal that is an agent, or for read and rate limits per grant. The grant above fills this.
- `display` mixes trusted labels with sender-influenced text; the untrusted portion should be split out.
- Contracts, credentials and ops categories are unsigned mocks, and agents must see that label.
- The fixture clock is pinned to 2026-10-04, so an agent asked "what is actionable now" on real time will correctly find expired quotes and approvals.

Limitations of this research:
- The client matrix is community-maintained, and a checkmark is not a conformance result.
- TS SDK support for 2026-07-28 wasn't verified.
- I did not test any MCP host's behavior on notifications, its MCP Apps sandbox origin, or its handling of URL elicitation for loopback URLs.
- The Moth origin risk inside MCP Apps is inferred from Moth's per-origin grants, not observed.
- The mock dashboard is unsigned, memory-only and no evidence of production behavior.
- The Moth connector is an origin-wide permission with no signing or payment authority, and its local disconnect doesn't revoke the grant.
- None of this establishes MPE privacy, membership, finality or exactly-once effects.

## Proposed consensus decisions

- The local durable watch/journal API is the single source of truth. MCP, A2A, AG-UI and MCP Apps are adapters, and none of them carries selectors upstream.
- Pin MCP `2026-07-28` and do not depend on any legacy or deprecated feature (sessions, `resources/subscribe`, Sampling, Roots, Logging, HTTP+SSE).
- MCP notifications are invalidation hints. Completeness comes from `watch_read` cursors with explicit gap reporting.
- Agent capability is a revocable grant bound to a principal and checked on every request. Watch creation and grant widening are human-only.
- Default discovery is user-consented stdio or loopback HTTP with `Origin` checks. Private watches have no public Agent Card or well-known endpoint.
- Sender-supplied text reaches agents only as labeled, capped untrusted data.
- Consequential approval happens on a first-party surface or in the wallet, reached via URL-mode MRTR. Agent-protocol UI approvals never count as authority.
- No webhook or push by default.
- Tasks, A2A and AG-UI are optional and each needs its own pinned interop test.
- Wallet connection stays out of agent-host frames.

## Unresolved objections

- **Developer ergonomics vs. pull-first.** Agent builders will want events to wake the agent. MCP gives hosts no standard way to do that, and host behavior varies. A host-specific wake integration might be needed later, which would fragment the experience.
- **Loopback URL elicitation.** It's unclear whether hosts open `http://127.0.0.1` URL-mode elicitations, and whether a remote agent host can reach them at all. Remote hosts may need a different approval path, such as wallet push or a phone. Undecided.
- **Stdio vs. HTTP.** One stdio process per grant isolates principals cleanly but can't serve remote hosts. Loopback HTTP needs credential issuance and storage that isn't designed yet.
- **MCP Apps sandbox origin.** If hosts give each server a distinct, stable origin, a narrowly scoped wallet flow inside an App might become acceptable. This needs host-specific evidence.
- **Selector leakage through MCP.** Even with opaque handles, `watch_list` output and read timing are visible to the agent host and potentially to the model provider. Users must understand that granting a cloud-hosted agent a watch discloses the selected records to that host. This is a weaker disclosure profile, like the remote gateway in `../wallet-consumers.md`, and the dashboard should label it as such.

## Rejected alternatives

- **Indefinite subscriptions as MCP Tasks.** Rejected: Tasks are finite with TTLs, and no listed client supports them.
- **Using A2A `SubscribeToTask` as a feed.** Rejected: the stream ends at a terminal state.
- **Relying on SSE resumability.** Rejected: it was removed in 2026-07-28.
- **Per-connection tool lists as scoping.** Rejected: the spec forbids them.
- **Form-mode elicitation or AG-UI interrupts for approval.** Rejected: neither is an authority channel.
- **Exposing the dashboard's browser state to agents via `postMessage` or globals.** Rejected: no origin-bound grant.
- **Public Agent Card, mDNS or well-known discovery for private watches.** Rejected: it publishes interests.
- **Using MCP Sampling to let the server run model reasoning on events.** Rejected: Sampling is deprecated and would move private records into a server-initiated model call.

## Source URLs (captures under `../sources/opus-agent-experience/`)

MCP: [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog), [subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions), [resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [discover](https://modelcontextprotocol.io/specification/2026-07-28/server/discover), [caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching), [pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination), [MRTR](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr), [elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation), [stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio), [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http), [authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [authorization security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations.md), [security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices), [versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning), [deprecated registry](https://modelcontextprotocol.io/specification/2026-07-28/deprecated), [SDKs](https://modelcontextprotocol.io/docs/2026-07-28/sdk), [extensions overview](https://modelcontextprotocol.io/extensions/overview), [client matrix](https://modelcontextprotocol.io/extensions/client-matrix) (visual), [Tasks extension](https://modelcontextprotocol.io/extensions/tasks/overview), [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview), SEPs [1024](https://modelcontextprotocol.io/seps/1024-mcp-client-security-requirements-for-local-server-.md), [2260](https://modelcontextprotocol.io/seps/2260-Require-Server-requests-to-be-associated-with-Client-requests.md), [2567](https://modelcontextprotocol.io/seps/2567-sessionless-mcp.md), [2577](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging.md).

A2A: [v1.0.1 specification](https://raw.githubusercontent.com/a2aproject/A2A/v1.0.1/docs/specification.md), [specification (latest)](https://a2a-protocol.org/latest/specification/), [agent discovery](https://a2a-protocol.org/latest/topics/agent-discovery/), [streaming and async](https://a2a-protocol.org/latest/topics/streaming-and-async/), [enterprise readiness](https://a2a-protocol.org/latest/topics/enterprise-ready/), [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/).

AG-UI: [introduction](https://docs.ag-ui.com/introduction), [llms.txt index](https://docs.ag-ui.com/llms.txt).

GitHub API pins: `modelcontextprotocol/{modelcontextprotocol,python-sdk,typescript-sdk,ext-tasks,ext-apps}`, `a2aproject/{A2A,a2a-python}`, `ag-ui-protocol/ag-ui`, `shieldedtech/moth-wallet`, `midnightntwrk/midnight-dapp-connector-api`.
