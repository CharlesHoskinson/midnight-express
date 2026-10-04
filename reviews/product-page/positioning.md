# Product positioning review

Reviewed the live page at https://charleshoskinson.github.io/midnight-express/, the local `website/dist/index.html`, and `docs/product-requirements/recommended-stack-and-use-cases.md` on 2026-10-03. The live and local HTML agree on the first-screen copy and section order.

## Main finding

The page explains the proposed components before it explains the customer's work. “The Midnight Express stack” identifies a technical subject, and “private event layer” assumes that readers already understand event infrastructure. A new visitor must infer the practical purpose from use cases far below the architecture and database sections.

Lead with private coordination across organizations and applications. Give the reader a concrete handoff, identify the initial audience, then let the architecture explain how the proposal could work. Preserve the design-stage label at the top.

## Plain-language definition

Midnight Express is a proposed coordination layer for applications that need to exchange confidential updates and act on them. It is designed to let participants share requests, responses and approvals while keeping message contents and the updates they follow away from delivery operators under the selected privacy profile.

“Event” means an update another application can respond to: a quote arrives, an invoice is paid, or a person approves an agent's next step. The product belongs between participating applications; their own policies still decide what an update permits them to do.

## Audience and core problem

The first audience is teams building institutional workflows on backend and desktop systems: developers and technical decision makers connecting quote applications, invoice systems and human-approved agents. Midnight application developers are a natural audience, but ordinary coordination does not require a ledger transaction for every update.

The problem is that confidential work crosses organizational and software boundaries. Teams manually pass updates, reconcile inconsistent records and check whether a response is current or authorized. The proposed product aims to reduce these handoffs while protecting the business details and subscription interests held at each endpoint. Customer demand, savings and operational economics remain unvalidated.

Use RFQ coordination as the initial product story. Spell it out as “requests for quotes” on first use. Invoice reconciliation and agent approvals demonstrate reuse; the other seven use cases are possible applications, not equivalent launch commitments.

## Recommended first-screen copy

**Eyebrow:** PRIVATE COORDINATION FOR BUSINESS APPLICATIONS

**Headline:** Keep sensitive work moving.

**Lead:** Midnight Express is a proposed private coordination layer for organizations, agents and Midnight applications. Exchange quotes, payment updates and approvals while keeping business details at the participating applications.

**Supporting explanation:** It is designed to keep message contents and the updates each participant follows away from delivery operators. Your application decides who can act; authorized ledger effects add a separate proof path.

**Audience line:** Starting with backend and desktop workflows for institutional requests for quotes, invoice reconciliation and human-approved agents.

**Visible status:** Design and exploration stage · Proposed architecture · Pilot priorities, not a production service

**Primary link:** See a quote workflow → a concrete explanation or the event journey

**Secondary link:** Explore the architecture → the existing system map

**Figure caption:** A proposed network for encrypted updates and local recognition.

Avoid “Get started,” “Start building” or a live-demo CTA until those destinations contain an actual usable implementation.

## Concrete explanation immediately after the hero

**Heading:** A quote request should not require a chain of manual handoffs.

**Copy:** A trading team requests a quote from approved counterparties. They return signed offers with expiry times. The receiving application checks permissions and tracks each response; proposed durable recovery lets it resume after an interruption. Acceptance can stay off-chain. Settlement requires additional authority and replay-protection work before it can be promised.

**Three parallel benefits, expressed as aims:**

- **Protect commercial context.** Keep requests, offers and subscription interests away from delivery operators under the selected privacy profile.
- **Recover interrupted work.** Track processing progress and handle expiry, gaps and duplicates; verify the proposed recovery implementation before relying on it.
- **Keep approval explicit.** Check signed intent and application policy before an action. Encryption alone does not grant permission.

**Evaluation line:** The first pilot should measure quote turnaround, manual handoffs, crash recovery, expiry and duplicate handling against the customer's current process.

## Recommended reading order

1. Definition, audience and design-stage status.
2. One quote scenario and three business aims.
3. First pilot priorities: quote coordination, invoice reconciliation, agent approval.
4. Event journey and interactive architecture for readers who want the mechanism.
5. Recovery implementation, production gates, other possible use cases and source evidence.

The detailed UmbraDB section is useful to implementers but interrupts the current product story. Keep its technical content available after readers know the workflow it supports. The component map and detailed technical names remain valuable there.

## Supporting copy

**Use-case heading:** Start with quotes. Reuse the foundation.

**Use-case introduction:** The recommended first pilot is confidential quote coordination. Invoice reconciliation and human-approved agents would test the same foundation next. Seven additional use cases remain candidates for exploration. Benefits and priorities still need customer evidence.

**Architecture introduction:** Participating applications create encrypted updates, receive relevant messages through local recognition, and apply their own rules before acting. Explore the proposed components and the integration work each still needs.

**Recovery heading:** Resume the workflow after an interruption.

**Recovery introduction:** The receiving application needs a durable record of what it processed and what remains to do. UmbraDB and PostgreSQL are the proposed backend foundation; SQLite serves standalone Rust nodes and clients. The full atomic processing capability still requires implementation and verification.

**Roadmap introduction:** The proposal begins with backend and desktop coordination. Production admission, retained delivery, recovery and operator funding need validation. Group security, ledger effects and private mobile reception have additional gates.

## Claims to preserve precisely

- Call this a proposed design, not an available production network, proven integration or ready-to-use SDK.
- Treat reduced handoffs and faster turnaround as hypotheses to measure, not promised outcomes or quantified savings.
- Scope privacy to event contents and subscription interests under the selected profile. Do not imply origin anonymity, hidden traffic patterns, automatic forward secrecy or private mobile reception.
- Keep admission, persistence, anchor inclusion/finality, local processing and business acknowledgement separate. None independently proves business completion.
- Do not promise exactly-once external actions: destination idempotency and reconciliation remain necessary.
- OpenMLS is a gated extension, and the first coordination pilot retains the original symmetric profile.
- UmbraDB's existing checkpoint/cursor capability does not establish the proposed atomic effects/dedup/outbox processing capability.
- Coordination can finish off-chain. Settlement and contract-origin private notifications have separate proof and platform gates.
