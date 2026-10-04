# Reader comprehension review

Reviewed 3 October 2026: the live GitHub Pages HTML, local `website/dist/index.html`, `app.js`, `use-cases.js`, and `docs/product-requirements/recommended-stack-and-use-cases.md`. Live and local HTML matched the architecture edition at review time. This review targets a business owner or application builder who understands confidential workflows but does not know Midnight, event infrastructure or cryptographic proof terminology.

## Main finding

The current page explains how a proposed system fits together before establishing why a reader would choose it. The opening names a “private event layer,” “stack,” “endpoints,” and “local recognition.” It then asks the reader to select nine components. A non-specialist cannot yet tell whether this is a messaging app, a database, a blockchain, or infrastructure their application team would integrate. Product priorities arrive after architecture, nine journey steps and a database release proposal.

Preserve the page's careful separation of transport, authorization, recovery and ledger evidence, but express the product story first. The recommendation document already contains the necessary direction: organizations and agents coordinate confidential work across systems; the first candidate is institutional request-for-quote coordination, followed by invoice reconciliation and human-approved agent work; savings and demand remain unvalidated.

## Six answers that must be visible without interaction

| Reader's question | Recommended answer |
|---|---|
| Who is it for? | Teams building workflows across organizations, business systems and software agents, especially where requests, interests and approvals are commercially sensitive. First pilots target backend and desktop applications. |
| What is it? | Proposed infrastructure for exchanging private business updates and coordinating the next authorized step. Applications integrate it; it is not yet a production service. |
| What problem does it solve? | A quote request, invoice update or approval often crosses separate systems and organizations. Teams repeat information, reconcile status by hand and recover uncertain progress after interruptions. Express is designed to share those updates privately and preserve recoverable workflow progress. |
| Why choose it over a conventional broker? | Conventional brokers can be appropriate when one operator may know the routing topics and subscribers. Express is intended for cases where delivery infrastructure should carry encrypted updates without learning their business meaning or which business events a receiver follows. Receivers identify relevant updates locally. This carries bandwidth, integration and operating costs that pilots must evaluate. |
| What does Midnight do? | Midnight supplies authoritative membership state and optional ledger evidence. Batches of sealed-message identities can be committed to the ledger. Ordinary coordination does not need a transaction for every message. A contract action requires separate proof of permission and protection against repeated execution. Recording a message's inclusion does not establish its delivery or business completion. |
| Is it ready? | The repository is a design and exploration project. The stack is a recommendation and the use cases are pilot candidates. Demand, savings and operating economics are unvalidated; integration and security work remain before production. |

The broker comparison should describe a selection criterion, not claim all brokers expose plaintext or cannot be configured securely. Express also does not promise that network operators cannot observe connections, shard participation, timing or size information.

## Recommended opening copy

**Private updates. Coordinated business workflows.**

“Midnight Express is proposed infrastructure for applications that coordinate confidential work across organizations and software agents. Exchange quote requests, invoice updates and approvals while keeping their contents—and which business events you follow—away from delivery infrastructure under the selected privacy profile.”

“Start with requests and signed quotes, then reuse the same foundation for invoice reconciliation and human-approved agent work. The goal is fewer manual handoffs and clearer recovery after interruptions. These benefits still need customer validation.”

Visible status: **Design and exploration · Proposed pilots · Not a production service**.

Useful first actions: **Explore the first workflows** and **Read the proposed architecture**. Avoid “Get started,” “Deploy” or “Try now” unless a concrete supported experience exists.

## Explain the product with one ordinary journey

Use a buyer requesting a quote as the first walkthrough:

1. A buyer's application sends an encrypted request to authorized dealers.
2. Delivery infrastructure relays the sealed update; each dealer's application identifies relevant requests locally.
3. Dealers return signed offers. The buyer's application applies its permissions and expiry rules before accepting one.
4. The applications record recoverable progress and exchange an explicit outcome. Receipt alone does not mean acceptance.
5. If settlement is required, a separate contract path must prove the instruction is authorized and cannot be reused. Automated settlement is outside the first coordination scope until those gates pass.

Show who acts, what changes and what the buyer gains before adding component names. The same foundation supports invoice notices and expiring human approvals; it does not grant an agent authority simply because the agent received a message.

## Plain-language glossary and FAQ

Only define terms needed to make a choice. Introduce the ordinary phrase before its technical name.

- **Event:** a business update such as “invoice approved” or “quote expires.”
- **Endpoint:** the application or device where an authorized participant opens and processes the update.
- **Local recognition:** an application identifies relevant updates on its own system instead of asking delivery infrastructure to select business topics for it.
- **Envelope:** the sealed package carrying an encrypted update.
- **Broker or relay:** infrastructure that distributes messages between applications.
- **Admission:** checks that a sender is eligible to publish and meets the protocol's allowance rules; it does not authorize a business action.
- **Ledger anchor:** a ledger commitment to a batch of sealed-message identities, providing inclusion evidence rather than delivery or completion evidence.
- **Recovery:** resuming workflow progress after an interruption, within supported retention and replay limits.
- **Idempotency:** ensuring repeated requests do not repeat a business effect. In overview copy say “prevent duplicate actions”; reserve the term for technical detail.

Keep RLN, MPE, AEAD, OpenMLS, Registry roots, nullifiers, shards, cursors, outbox and atomic commits in the architecture material. When RFQ first appears, spell out **request for quote**.

Recommended visible FAQ answers:

**Do I need Midnight for every update?** Ordinary coordination does not need a ledger transaction for each event. Midnight has membership and optional evidence/contract roles in the proposed architecture.

**Who can read a message?** Authorized endpoints hold the relevant keys and process the contents. Delivery and retained-store operators are intended to carry opaque envelopes; privacy still has observable-network-metadata limits.

**Does delivery trigger an automatic payment or agent action?** Applications decide what is allowed. Ledger effects require additional authorization, message binding and replay protection. Initial invoice pilots exchange and reconcile status rather than automatically execute payments.

**What happens if an application goes offline?** The design combines retained encrypted messages with durable local progress to support catch-up. Recovery is bounded by retention and must expose missing data; production reliability has not yet been established.

**Can I use this on a phone?** First pilots are backend and desktop workflows. Strong private mobile discovery and retrieval remain a separate research track.

**Is this a replacement for our ERP or message broker?** It is proposed coordination infrastructure integrated through application-owned adapters. Its value depends on the confidentiality boundary and workflow; existing systems can remain the systems of record.

## Accessible information flow

Recommended sequence: purpose and status → concrete buyer workflow → first three pilot candidates → privacy and broker choice → Midnight's role → readiness → expandable architecture and sources. This lets a reader decide relevance before being asked to learn implementation details.

The key answers and first pilot examples should be static HTML, readable with JavaScript disabled. The present use-case grid, journey and selected component content depend on JavaScript; a failed script leaves substantial content absent. Keep optional interactives as enhancements. Use descriptive navigation such as “Why Express,” “Workflows,” “How it works,” “Readiness” and “Architecture.” A skip link should lead to the main product content rather than bypass the introduction straight into architecture.

For interactive details, maintain keyboard access, visible focus, meaningful headings and selected-state announcements. Do not require clicking every map component to understand the product. Pair diagrams with short textual descriptions; label conceptual imagery as illustration rather than evidence of a deployed network. Avoid using color alone for current versus proposed capabilities.

## Completion checks for the rewritten page

A reader scanning the heading, introduction and first example should be able to identify the product category, intended user, sensitive information protected and first useful workflow. Before reaching architecture, they should understand why a conventional broker may remain sufficient, why Express may matter across trust boundaries, what Midnight contributes and what is still proposed.

Ask a test reader to explain whether “message received” means “payment completed,” whether every update needs an on-chain transaction, whether phones are supported, and whether the product is ready to deploy. The page succeeds only if their answers match the boundaries above without consulting the design document.
