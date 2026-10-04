# Product review: reader progression and information flow

Reviewed the [live page](https://charleshoskinson.github.io/midnight-express/), `website/dist/index.html`, its interaction content in `app.js` and `use-cases.js`, and [the recommended stack and use cases](../../docs/product-requirements/recommended-stack-and-use-cases.md). Live HTML retrieved on 2026-10-03 matches the local section order. This is a content and information architecture review; it does not establish visual rendering or usability results.

## Main finding

The page makes a technically credible architecture argument before establishing the product need. Its hero supplies one useful definition, but the next substantive content asks readers to understand nine components. The technical journey and a dedicated UmbraDB section add more implementation detail before the first business workflow appears. A prospective design partner reaches “what would I use this for?” only after learning much of “how would it work?”

Lead with the recommendation already present in the source document: private coordination between organizations, with backend/desktop RFQ coordination as the first demonstration and invoice reconciliation and human-approved agent work as reuse candidates. Preserve the architecture explorer as the technical depth that supports that proposition.

## Proposed progression

| Order / anchor | Reader question | Content and exit |
|---|---|---|
| 1. Definition / `#overview` | What is Midnight Express? | Concrete definition, intended users, stage and links to the example and architecture. |
| 2. Problem / `#problem` | What coordination problem is it intended to solve? | Manual handoffs, reconciliation and sensitive event/subscription information; distinguish the business objective from the selected distribution approach. |
| 3. Example / `#example` | What would a customer actually do? | One RFQ workflow in business language, with the first scope and measurement visible. |
| 4. Use cases / `#use-cases` | Does this fit my work? | Three recommended pilot candidates, then the remaining seven in the existing rank order. |
| 5. Architecture / `#architecture` | How is that outcome supported? | Three plain-language responsibilities, then the existing component explorer and optional protocol journey. |
| 6. Delivery / `#roadmap` | What is being proposed first, and what must be proven? | Demonstration, reusable pilots, production gates and separately gated extensions. Finish with requirements and evidence links. |

The problem and example can be compact neighboring blocks. This change need not create a longer page: move existing content, replace repeated implementation paragraphs and disclose technical details progressively.

## Concrete copy changes

### Definition

Change the browser title from **“Midnight Express — The architecture”** to **“Midnight Express — Private workflow coordination”**. Replace the headline **“The Midnight Express stack.”** with:

> Private events for coordinated work.

Replace the lead with:

> Midnight Express is a proposed private event and workflow coordination layer for organizations, agents, wallets and Midnight applications. Exchange signed events, keep business context at the endpoints, and recover workflow progress after interruptions.

Retain a compact **“Design and exploration stage”** marker. Replace **“Recommended architecture”** with **“First proposed pilot: RFQ coordination”**, making the intended starting point visible before the technical explorer. Add two links: **“Follow an RFQ example”** → `#example` and **“Explore the architecture”** → `#architecture`.

“Recover workflow progress” is a design objective here, not a statement that the proposed atomic processing integration has shipped. Keep the stage label next to the definition, and keep the actual recovery capability boundary in the architecture detail and delivery gate.

### Problem

Add heading:

> Coordinate the next step without exposing the whole workflow.

Suggested paragraph:

> Quotes, invoice updates and approval requests cross organizational boundaries. Teams need to know who sent an instruction, whether it is still valid, and what happened after an interruption. Midnight Express is intended to reduce manual handoffs and reconciliation while keeping event contents and subscription interests away from delivery infrastructure under its selected privacy profile.

Use three compact needs, not a second benefits manifesto:

- **Confidential exchange:** share workflow information with authorized participants.
- **Recoverable progress:** catch up after interruptions and handle duplicate events.
- **Explicit authority:** require application policy and signed instructions before an action.

Do not imply that existing event platforms cannot encrypt payloads or that the network hides all traffic metadata. If expanding privacy claims, expose the current design's connection, shard, timing and size visibility beside that explanation.

### Example

Add heading:

> A buyer requests quotes. Dealers respond. The buyer accepts one.

Add a short context sentence:

> The proposed first demonstration runs on backend and desktop systems. It coordinates quotes and off-chain acceptance; automated settlement has separate proof gates.

Present four visible steps without requiring clicks:

1. **Request:** the buyer sends an expiring RFQ to authorized dealers.
2. **Respond:** dealers return signed offers; authorized recipients recognize and open relevant events locally.
3. **Accept:** the buyer selects a valid offer under the application's role and expiry policy.
4. **Resume:** after an interruption, the endpoint recovers retained events and workflow progress within the supported retention horizon; external actions still need idempotency or reconciliation.

Close with one outcome line:

> Evaluate quote turnaround, manual handoffs and outage recovery against the customer's current process.

The example should identify the business actors and visible actions before introducing SDKs, proofs or stores. Link **“See what supports this workflow”** to `#architecture`. Include one scope note: **“A receipt or anchor inclusion does not mean a quote was accepted.”** Leave the five-part evidence taxonomy in technical depth.

### Use cases

Change **“Ten uses. One shared foundation.”** to:

> Start with three coordination workflows.

Suggested introduction:

> RFQ coordination is the first proposed demonstration. Invoice reconciliation and bounded human-approved agent work test reuse of the same foundation. Seven further candidates add customer, integration or protocol dependencies.

Make the top three candidates a visible first group; place ranks 4–10 under **“Further candidates”**, preserving stable UC IDs and rank order. This grouping signals recommendation strength without representing the candidates as validated demand.

Use short titles: **“RFQ and quote coordination”**, **“Invoice reconciliation”**, **“Agent work with human approval.”** Each summary should show its own concrete first scope and one measure, so the closed state already answers what the pilot does. Keep the remaining gate in expanded details. Avoid repeating “MPE coordination + …” in every card: the architecture section owns the shared foundation. Keep candidate-specific integrations where they change feasibility.

Use one section-level qualification: **“Business value and customer demand remain hypotheses to validate.”** Do not repeat that sentence inside all ten cards. Link the ranking basis and complete requirements to the source register rather than reproducing them throughout the page.

### Architecture and technical journey

Keep **“One event layer. Distinct responsibilities.”** Introduce it with:

> Applications create signed events. The overlay distributes sealed envelopes. Authorized endpoints recognize relevant events and process them under their own policy. Midnight evidence supports a separate contract path when one is required.

Move the existing three principles here as the transition from product explanation into technical depth. Use them once; the earlier problem block names needs, while these paragraphs explain the selected response.

Keep the nine-component explorer, its explicit integration gates and component links. Rename **“Event journey”** to **“Protocol journey”** and place it after the responsibility map as a secondary exploration link or disclosure. Its nine steps serve the reader who now wants implementation detail; they should not compete with the four-step RFQ example.

Merge the standalone **“Umbra understands Midnight. Express needs more.”** recovery section into the recovery component detail, with a focused delivery prerequisite. The current component panel and standalone section explain almost the same Node/PostgreSQL, checkpoint/cursor and future atomic processing boundary. Maintain one authoritative detailed explanation, then summarize the readiness dependency in delivery. If retaining the archive image, attach it to the architecture/recovery area without adding another narrative stage.

Keep ordinary coordination and the optional ledger branch visibly separate. The RFQ example ends in off-chain acceptance; its existence must not imply that CON-060 binding, replay protection or automated settlement have been completed.

### Delivery

Change **“Prove coordination. Then expand the promise.”** to:

> Demonstrate the workflow. Validate the production gates.

The present “first pilot candidates” card flattens the ordered delivery recommendation. Replace it with three concise readiness groups:

- **First demonstration — RFQ coordination:** requests, signed quotes, expiry and off-chain acceptance on backend/desktop. Clearly labeled mock Registry/admission is permitted only for an internal demonstration. Measure turnaround, handoffs, crash recovery and duplicate handling.
- **Reuse pilots — invoices and agent approvals:** establish customer baselines; validate authenticated source evidence, bounded permissions and idempotent or reconciled external effects.
- **Before production — coordination core:** real finalized Registry roots, accepted RLN profile and measured limits, replicated retention with signed receipts, funded operators and verified durable endpoint processing.

Follow with **“Separately gated extensions”**: OpenMLS group security; authorized ledger effects and private contract-origin events; private mobile reception. Explain that these tracks may proceed alongside coordination work, but each needs its own evidence before the related promise. Do not present every extension as a sequential phase that must finish before coordination is useful.

Retain the source links and recommendation-stage disclosure at the end. Consolidate **“Deliberate choices”** into an architecture disclosure such as **“Why these components?”**; dependency exclusions are most useful while evaluating the system, rather than after the delivery story.

## Navigation and interaction

Change the primary navigation to **Overview · Example · Use cases · Architecture · Delivery**, linking to `#overview`, `#example`, `#use-cases`, `#architecture` and `#roadmap`. The problem section flows naturally from overview and does not need a sixth navigation item. The protocol journey remains reachable within architecture and retains its existing deep link.

Change **“Skip to architecture”** to **“Skip to main content”**, targeting the start of `main`. Keep the hero's direct architecture link for technical visitors. Preserve existing architecture, use-case and roadmap anchors so incoming links remain useful. Update section numbering to match the new progression; the current 01–05 sequence should not survive a reordered page unchanged.

Neither the definition, RFQ example nor first pilot scope should require expanding an accordion or operating the component map. Interactions should reveal supporting technical detail, rather than hold the product proposition. Each “Explore this component” action can retain its present selected-component navigation and focus behavior.

## Acceptance criteria for the rewrite

- Within the first screen's text, a reader can identify the proposed product, intended users and design stage.
- Before the component map, the reader sees the coordination problem, one concrete RFQ flow, and the absence of an initial automated settlement claim.
- The first three recommended candidates are distinguishable from the broader portfolio without opening every card.
- Architecture and delivery preserve the existing privacy, durability and authority boundaries; benefits remain evaluation hypotheses.
- Recovery detail has one primary home; the business example and protocol journey have different levels of detail and do not repeat the same sequence.
- A technical reader can still jump directly to the architecture, inspect every component gate and reach the source requirements.
- Ask prospective design partners to explain the product, the first pilot and its unresolved gates after reading; assess comprehension rather than inferring improvement from rearrangement alone.
