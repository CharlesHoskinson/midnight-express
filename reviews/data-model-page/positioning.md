# Data Model page — product positioning review

Role: product manager reviewing executive buyer comprehension. Evidence: current model README, unified-data-model proposal, implementation status and the Overview/Implementation pages. No new external research or operational ROI evidence.

## Recommendation

Lead with the coordination problem and the design choice. A buyer needs to understand why another format is useful before seeing schemas, hashes or test counts. The central promise is **shared meaning for a declared workflow**, with explicit refusal when the parties cannot agree. Show one concrete price example before introducing the three layers. Describe what is implemented separately from what still requires deployment evidence.

The tab should be named **Data Model**. Suggested reading order: why it matters → one concrete example → three layers → pilot workflows → business value → current evidence and next gates. Preserve links to the technical implementation page for readers who want the test detail.

## Proposed hero

Eyebrow: DATA MODEL / SHARED MEANING

Heading: **Different applications. The same agreed meaning.**

Lead: Midnight Express proposes a small shared event core, precise contracts for each workflow and adapters for each participant’s format. Applications agree on what a message means before their business rules decide what may happen next.

Supporting copy: A private message is useful only if its recipients understand the same price, amount, status and permission. The model makes those assumptions explicit. Missing units, conflicting roles or an unsupported contract cause refusal rather than a guessed interpretation.

## Proposed section: Why a shared format is not enough

Applications can exchange valid JSON and still disagree about the transaction. One dealer quotes dollars per share; another quotes cents per hundred shares. An invoice system records a payment observation; another treats “Final” as permission to mark an invoice paid. An agent sees an approval but lacks authority for the proposed target.

Midnight Express addresses these differences with bounded workflow contracts. Each contract names the terms, units, lifecycle and rules that participating applications agree to interpret. Teams can add a separately reviewed workflow without expanding one schema to describe every organization.

## Proposed example: Same quote, two declared formats

**100 shares at $123.45 per share means $12,345.** A source quoting 1,234,500 cents per hundred shares can represent the same price when currency, price basis, quantity and buyer/dealer perspective are all declared. An adapter checks those declarations and maps them into the agreed RFQ contract.

If the source omits the price basis, the adapter refuses the quote. Matching economics also does not erase identity: two different dealers remain two different sources and offers.

Design suggestion: show Source A → agreed RFQ meaning ← Source B, with a separate “Missing price basis → refused” outcome. Avoid showing a valid quote going directly to “trade executed.”

## Proposed section: Three layers, one agreement

**Shared event core.** Every event has an identity, source, time, exact type and commitment to the contract it uses. This common mechanism stays inside the encrypted message body.

**Workflow contracts.** A quote, payment observation and agent approval each have their own closed rules. A quote declares its currency and price basis. A payment observation distinguishes Pending, Final and Reversed. A sandbox approval binds its action, target, scope, budget and expiry.

**Participant adapters.** Each adapter translates one explicitly declared source convention. It preserves source meaning and refuses information it cannot represent safely. It does not infer a currency, invent a permission or quietly insert a missing business term.

Supporting copy: The agreement is pinned to an exact, immutable contract. Changing a workflow’s meaning requires a new contract; it does not silently reinterpret old messages. Current and historical contracts remain distinguishable during replay and review.

## Proposed section: What this provides to the business

**A clearer integration agreement.** Partners can review the supported terms and refusal conditions before connecting their systems. Teams can resolve a price-basis or status mismatch at the boundary instead of discovering it downstream.

**More dependable automation.** Applications receive a checked interpretation rather than an invitation to guess. A valid message is still subject to authentication, business policy and permission checks; validation alone never authorizes an action.

**A reviewable history.** Exact contract identity and separate occurrence/action identity help explain which meaning was accepted and whether a delivery is a repeat. Read-only chain journals preserve observations and invalidations instead of overwriting history.

**A controlled path to more workflows.** Shared parsing, contract verification and recovery mechanisms can be reused while domain-specific rules stay separate. The pilot should measure how much engineering effort that reuse actually saves.

Do not claim reduced costs, fewer errors or faster settlement as measured outcomes. Partner integration hours, manual corrections and turnaround baselines remain uncollected. Present these as intended benefits to evaluate in a customer pilot.

## Proposed section: What is available now

The v0.2 reference implements three narrow profiles: quote observations, invoice payment observations and approval of one sandbox report-writing operation. Independent Python, Rust and TypeScript interpreters agree across 35 RFQ test vectors; two adapters exercise explicitly different price formats. These are synthetic conformance cases, not a live market error-rate measurement.

The wider Ethereum/Solana vocabulary contains 291 proposed entries. Current executable chain support is a read-only ERC-20 transfer slice and a legacy SPL TransferChecked slice. The vocabulary is a planning map, not 291 supported runtime contracts.

An Umbra/PostgreSQL prototype passes 56 recovery checks, including four worker kills. That evidence covers a fixture-authorized database report write and an acknowledgement fixture. Authentication, live-chain finality, full protocol integration and external financial execution still require their own evidence.

## Prose constraints

- Say “unified agreement mechanism” or “shared core and workflow contracts”; do not promise one universal schema.
- Say “payment observation,” not “payment settled”; a source’s Final assertion is not consensus or bank authority.
- Say “independent RFQ interpreters,” not “all domains independently verified.”
- Say “refuses unsupported meaning,” not “understands any format” or “AI resolves ambiguity.”
- Keep `executes:false`, JSON field lists and cryptographic details in a compact technical disclosure or on Implementation; explain the business boundary in plain language first.
- Maintain current reference evidence versus proposed protocol sprint gates. The existing Overview FAQ says only design/exploration; update that sentence to acknowledge the bounded local reference so the tabs tell a consistent story.
