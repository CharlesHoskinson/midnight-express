# Subscription design council

The user asked for a design council to improve Midnight Express’s subscription experience, with reviewers from Grok, Gemini, GPT and Claude. They confirmed a feed directory for discovering and organizing subscriptions as the default. Search, hundreds of independent feeds and stateful information are required.

The [recommended workspace](../../design/subscriptions/directory-workspace.md) is the coordinator’s synthesis of the independent reviews. It resolves disagreements against those requirements and the protocol boundaries. The current website remains the earlier tab-memory demo; this research does not claim that a replacement interface or production service has shipped.

## Design recommendation

Use Directory, My feeds, Inbox and Delivery tools as clear destinations. Desktop has navigation, compact results and an optional selected-feed preview; mobile uses a drill-down view with reliable Back and focus restoration. Search and initial results belong in the first viewport. Optional wallet connection and fault-injection controls support the workflow without preceding discovery.

A feed has a stable identity and explicitly resolved local scope. Payment statuses are examples inside a feed. Channels can collect a publisher’s feeds; personal folders and saved views change organization. These objects never become business routing topics. Multiple same-category feeds must work independently.

Retain bounded synthetic history, follow intent references, folders and read/saved markers. After reload, show historical state and require a fresh check before delivery or new processing. Reading, recording a disposition and authorizing an effect remain separate. IndexedDB is the proposed browser store; the authenticated consumer service owns production continuity.

Use local scoped search, facets and stable bounded result pages. Default to pagination and native semantics. Measure the actual renderer before choosing virtualization. Queue pressure, retained-range recovery and lost history are different states. Recovery preserves requested pause. No new remote interest broker or privacy transport is selected.

## Reviewer record

Model families have distinct reviewer assignments. Invocations, report hashes, model options and available provider usage metadata are in [provenance.json](provenance.json). External reviewers ran in a durable service with staged concurrency. GPT used collaboration model overrides. A server restart interrupted completion notifications; the GPT usability report and evidence were recovered from disk. No provider was substituted.

| Reviewer | Focus | Report |
|---|---|---|
| Grok | Discovery and information architecture | [Feed discovery](agents/grok-feed-discovery.md) |
| Grok | Pub/sub and developer event patterns | [Event navigation](agents/grok-event-navigation.md) |
| Grok | Privacy and trust | [Adversarial privacy](agents/grok-adversarial-privacy.md) |
| Gemini | Inbox interaction | [Inbox interaction](agents/gemini-inbox-interaction.md) |
| Gemini | Large directories | [Directory scale](agents/gemini-directory-scale.md) |
| Gemini | Accessibility and responsive workflows | [Accessibility](agents/gemini-accessibility.md) |
| GPT | Interface and state architecture | [Architecture](agents/gpt-consensus-architecture.md) |
| GPT | Human, wallet, DApp and agent journeys | [Product workflows](agents/gpt-product-workflows.md) |
| GPT | Usability and verification | [Usability](agents/gpt-usability-verification.md) |
| Claude | Browser persistence and restoration | [State restoration](agents/claude-state-restoration.md) |
| Claude | Operation and recovery | [Operability](agents/claude-operability.md) |
| Claude | Independent product pattern comparison | [Best patterns](agents/claude-best-patterns.md) |

Grok requested `grok-4.7` with xhigh reasoning, Gemini `gemini-3.1-pro-high` with high effort, GPT `gpt-6.1-sol` with high reasoning and Claude `claude-opus-5-5` with high effort. Claude reports backend model usage IDs. Gemini and Grok provide different metadata, so their invocation options are recorded without inventing backend identity fields.

## Evidence and limitations

All online retrieval used Scrapling. PixelRAG pixelshot/CDP supplied visual captures, and reports identify the tiles actually inspected. Capturing a tile does not mean it was inspected or that it contains useful evidence. Blank captures, error pages and app-shell extraction failures are recorded rather than treated as substantive sources. CPU capture is not GPU inference.

The [source index](source-index.json) records URLs, retrieval time, hashes and capture metadata. Accepted artifact hashes were checked against saved bytes. Some rejected or duplicate captures retain only metadata explaining why their payload was removed. Reviewer source notes distinguish text from visual evidence. [Intermediate findings](intermediate.md), [resolution draft](resolution-draft.md) and per-reviewer notes preserve approaches, observations and decision rationale rather than private chain-of-thought.

The reviewers used primary material from feed readers, GitHub notifications, Slack, VS Code, Grafana, NATS, Kafka, AsyncAPI, CloudEvents, design systems, W3C/WAI and browser storage documentation. Patterns transfer selectively: remote polling, public topic subscription and automatic joining do not become Midnight Express behavior.

Browser probes found discovery below the first viewport, keyboard focus falling to BODY after follow/pause, unsaved scope edits lost during search, blank no-results, repeated category subscriptions, silent inbox truncation and reload loss. Existing semantic tests pass; they do not cover the replacement experience. Scratch storage and search measurements describe the recorded device and corpus, not large-catalog production performance. Acceptance budgets in the design are proposed targets.

## Resolved disagreements

| Question | Resolution and reason |
|---|---|
| Inbox or directory first? | Directory, following the user’s explicit choice. Inbox supports reading. |
| Persist only organization? | Retain bounded historical information as well. Preferences alone do not satisfy the stateful requirement. Never restore authority as a trusted fact. |
| Hundreds of aliases or independent feeds? | Independent scopes are required. Aliases are labeled and excluded from functional scale claims. |
| Share search through the URL? | Private query/selection stays in device state by default. Public synthetic sharing can be an explicit later action. |
| Virtualization or pagination? | Bounded native rows and pagination first. Virtualization requires measurements and focus/assistive-technology work. |
| ARIA feed/tree/grid everywhere? | Choose semantics for the interaction, with native lists first. APG patterns carry obligations; they are not automatic accessibility. |
| Read means processed? | Read is presentation. Review/quarantine is an explicit receipt disposition. Neither authorizes effects. |
| Full credits mean missing history? | No. Show behind/retained work separately from a genuinely unavailable range. Recovery and new-start acceptance preserve pause. |
| Extra predicates inferred from feed names? | No. Existing allowed predicates remain exact; additional selectors require reviewed contracts. |

The Gemini drafts underwent a correction pass in the same conversations. Original reports remain under [agents/initial](agents/initial/), with hashes and revision provenance. Revisions addressed execution language, state restoration, directory default, independent scopes, accessibility claims and unsupported performance conclusions.

Root independently checked an operability claim about the quote examples: accepted and expired-context records contain identical event values. They differ in context and receipts, so that example does not establish an occurrence-content conflict. Validation-context rejection and changed-content conflict are separate scenarios. The final design records that correction while preserving the independent report. The revised Gemini scale draft also claims the incumbent offers Approve actions; the inspected HTML contains no such control. Preventing execution approval is a continuing requirement, not an observed incumbent defect. Native semantics and a split view support usability but do not automatically guarantee accessibility.

Remaining implementation decisions include descriptor discovery/trust ownership, alias policy, service authorization for stopping blocked watches, aggregate host resource limits and real-device/assistive-technology support. The recommended design states acceptance gates instead of presenting those decisions as implemented capability.
