# Sol standards engineering research

Owned outputs: this report and `../standards.md`. No runtime edits, commits or network deployment.

## Hypotheses and approach

A shared durable local consumer API can serve wallet, DApp, human and agent subscribers while preserving whole-shard reception and local business selectors. Agent protocols should be adapters, not replacements for the MPE privacy and evidence model. Public identity/discovery can improve interoperability but does not establish private membership or action permission.

Fetched primary protocol pages using Scrapling Fetcher, saved HTML/text separately with UTC fetch times and SHA-256 metadata under `../sources/sol-standards/`, and inspected relevant lifecycle/security/version text. Reviewed existing `docs/product-requirements/recommended-stack-and-use-cases.md` and prototype sprint requirements for the local-recognition constraint. No alternative fetcher or web search service was used. Broad inventory includes event standards, MCP, A2A, both ACP meanings, AG-UI, ANP, W3C DID/VC, CAIP-10, ERC-8004, OpenAI Agents and LangGraph.

## Intermediate observations and corrections

The first historical MCP 2025-11-25 resource page showed URI-only invalidation and optional subscriptions; its tasks page called tasks experimental. Checking the official versioning page then revealed current **2026-07-28**, materially changing the recommended adapter: stateless metadata, mandatory `server/discover`, `subscriptions/listen` instead of `resources/subscribe`, and tasks moved to the official extension. Historical source artifacts remain because stale examples are a real implementation risk. Current resource notifications remain URI invalidation, not the durable event log.

Current A2A documentation identifies v1.0, ordered active task streams and independent task/stream lifecycles. It supplies task-oriented collaboration, not private business-event subscription semantics. Its HTTP push path exposes endpoint/task relationships, so it cannot be adopted silently for private watch delivery. BeeAI Agent Communication Protocol officially merged into A2A; Agent Client Protocol is a separate editor/coding-agent protocol.

ANP is not simply an undifferentiated draft: its current project index labels released v1.2 identity/authentication/naming/description/discovery specifications, draft authorization v0.6 and draft meta-protocol. ERC-8004 remains a Draft EIP. OpenAI Agents and LangGraph are frameworks, not equivalent wire standards.

One initial fetch script failed because its output directory was absent at the absolute target; no result was presented as successful from that failed run. The corrected run saved all main sources successfully. Any supplementary URL failures retain HTTP status metadata and body instead of disappearing.

## Objections and alternatives

**Use MCP alone for all pubsub:** convenient but resource invalidation does not define retained occurrence identity, consumer acknowledgment, coverage or business idempotency. Keep the local durable read/commit contract and expose it through MCP.

**Use A2A as the network envelope:** task lifecycle and remote endpoint model do not substitute for encrypted MPE recipient recognition. Wrap explicitly commissioned tasks after local validation; do not change wire classes.

**Adopt agent registry/DID as authority:** discoverability and identifier ownership cannot imply admitted membership, recipient authorization or wallet consent. Retain distinct proofs and explicit mappings.

**Make every event a task:** adds orchestration state and assumes host support. Most wallet notifications are ordinary events; task creation is justified only for finite requested work.

**Webhook default:** works well for reachable backend services but leaks endpoint/task interests and adds inbound security burden. Offer only under explicit policy; local polling/notification adapter is the default.

## Final recommendation

Adopt CloudEvents-compatible encrypted metadata, AsyncAPI contract documentation and one local durable consumer API first. Deliver the human/wallet API before optional protocol adapters. Implement MCP **current 2026-07-28** with pinned compatibility and an optional separate historical profile only if an actual client needs it. Use `subscriptions/listen` for local resource invalidation, `watch.read` for bounded durable consumption, and the Tasks extension only for finite long-running operations. Keep A2A v1.0 behind an optional task gateway; AG-UI is frontend event presentation. Track ANP and ERC-8004 without mandatory identity dependencies. Select an orchestration SDK separately from protocol decisions.

Reference demo and full protocol remain separate gates: fixtures can demonstrate consumer ergonomics; only network traces, independent vectors, evidence verification and wallet action authorization justify full-protocol claims. See `../standards.md` for detailed table, API shape, privacy constraints and authoritative URLs.

## Source ledger and visual grounding

Each primary source has `.html`, `.txt`, `.metadata.json` artifacts. Metadata contains requested URL, UTC timestamp, method, HTTP status and body/text hashes. Historical MCP pages and current replacements are deliberately separate. Redirect targets observed in fetch logs include current MCP tasks extension and current versioning page; recommendations link those canonical pages.

PixelRAG skill was read at `/home/hoskinson/Projects/inkwell/skills/pixelrag/SKILL.md`. Its required CPU screenshot tool `pixelshot` was absent from PATH and no binary was located in the searched local/plugin paths at initial research. The coordinator subsequently installed PixelRAG 0.4.0 in the Scrapling venv and provided `research.py`; capture used the actual CPU CDP backend with tile height 1568 and network-idle waiting. The MCP current changelog produced three tiles; tile_0000.jpg was inspected with view_image. It visibly confirms removal of protocol sessions/initialize, mandatory server/discover, subscriptions/listen replacement and the redesigned Tasks extension in one page. Tile_0000 SHA-256: `246b45d8acbf6bbea243a45b8b34185313de9c2ffd0f8a04540df86214d6e44d`; source capture metadata is `mcp-current-visual.metadata.json`. No GPU semantic index was attempted or claimed. Other inventory sources remain text-grounded unless a separate visual capture is recorded.

The current MCP subscription-pattern page also produced three tiles. Inspected tile_0001.jpg (SHA-256 `dfaf21fb080a6de34fe8cc9f6d425a8e72e97733dcf2b76b2d25023a1a3d4e2a`) visibly confirms acknowledgment filter checking, notification subscription-ID correlation and URI-only resource update payload. Metadata: `mcp-subscriptions-visual.metadata.json`. Capture does not establish conformance of any SDK or host implementation.
