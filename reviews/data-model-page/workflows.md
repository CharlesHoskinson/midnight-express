# Data Model page review — workflow product manager

Reviewed the active v0.2 model README, implementation status, RFQ/invoice/agent fixtures, independent adapter campaign and current Implementation page. This review recommends public prose; it does not extend implementation claims.

## Recommendation

Lead with the expensive business mistake the model prevents: two applications can accept the same JSON while disagreeing about the transaction it describes. Present three concrete stories before implementation metrics. Each story should identify a real ambiguity, the explicit rule that resolves it, the practical benefit and what the current reference actually does.

Keep the main concept small: a common event envelope plus separately versioned workflow agreements. Readers do not need a field glossary before they understand why units, roles, clocks and action identity matter. Label the three profiles as reference-tested pilot contracts. Treat other currencies, fees, tools and full invoice accounting as separate contracts requiring their own agreed rules.

## Recommended page prose

### Same message. Same meaning.

A quote, payment update or agent approval can travel successfully and still be misunderstood. Midnight Express gives each workflow an explicit agreement about what its data means: who is involved, which units apply, when the information is valid and which action it describes. Applications keep their own internal formats; declared adapters translate them into a specific supported contract. Missing or contradictory meaning causes refusal rather than a guessed default.

### A quote that cannot hide its price basis

A buyer requests 100 shares. One format quotes $123.45 per share; another quotes 1,234,500 cents per 100 shares. Both describe $12,345 of cash when their currency, quantity basis, buyer/seller perspective and no-fee convention are declared. The reference adapters make those conventions explicit and check the arithmetic exactly. A quote missing its denominator or using an unsupported fee convention is refused.

The benefit is a quote that applications can compare and review without silently multiplying the wrong price or reversing the trading direction. This pilot coordinates an off-chain quote; it does not execute or settle the trade.

Two encodings produce the same intent commitment only when they describe the same complete source-bound intent. Matching prices from different dealers remain different intents. A content hash neither authenticates a dealer nor authorizes a trade.

### A payment observation that preserves its evidence

A supplier has a $500 invoice and receives an observation of a $250 payment. The model records the invoice, payment identity, amount and source status separately. Pending, Final and Reversed retain their distinct meanings, and the observed amount cannot exceed the invoice's payable amount. It also distinguishes when the payment was effective, when it was observed and when the observation record was created.

The benefit is a reconciliation record that can explain what a source reported and when. Final remains the source's assertion. This profile does not establish bank finality, allocate payments across invoices or decide that an invoice is paid; changing a status string cannot grant those conclusions.

### An approval that cannot become a different action on replay

A human approval fixture names one sandbox report-writing proposal, its exact target and input, execution scope, expiry and maximum Step budget. Changing the target changes the proposed action and conflicts with the already consumed action identity. Delivering the same approved action again under a new event ID cannot make it new work.

The bounded Umbra/PostgreSQL prototype checks fixture permission again inside the effect transaction. It commits the report row and its progress together, charges one Step for that report-row write and releases unused reserved capacity. Crash and replay tests recover one local report effect. A lost reply from the separately committed destination fixture remains uncertain until reconciliation.

The benefit is a reviewable action boundary and recoverable progress. The validator itself returns an accepted candidate with `executes:false`. Human identity and permissions are supplied trusted test fixtures; production approval authentication and arbitrary agent tools remain separate work.

### Delivery identity and business identity answer different questions

An event ID asks, “Have I seen this occurrence before?” A scoped action ID asks, “Has this work already been consumed?” Keeping both prevents a reconnect or retry from turning an old approval into a new action. For chain observations, physical inclusion identity also distinguishes a repeated delivery from a transfer re-included on a different branch.

## Placement and wording checks

- Place the quote comparison early, ideally as two simple cards with one shared cash total. Include “same complete source-bound intent” near any statement about equal commitments.
- Put invoice clocks in an expandable example or small sequential diagram after the story; keep each clock's business meaning visible.
- Show approval → validation candidate → separately authorized sandbox write, rather than drawing a direct approval-to-payment arrow.
- Say “three reference-tested profiles” and “291 proposed vocabulary entries.” Do not imply 291 executable payload contracts.
- Reserve recovery counts and cross-language corpus counts for an evidence section. They show finite reference behavior, not measured customer savings or real-world error rates.
- Link deeper technical material after the public explanation. Private repository access must not be necessary to understand the page.
