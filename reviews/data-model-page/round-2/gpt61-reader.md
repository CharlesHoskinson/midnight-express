# Reader comprehension review — GPT-6.1, round 2

The page has a sound central explanation: applications keep their formats, declare their conventions, and refuse interpretations they cannot justify. The quote example makes that claim tangible. The main editorial problem is that the reader moves too quickly from a comprehensible price conversion into a dense collection of contract fingerprints, event identities, branch locations, finality assertions, and recovery boundaries. More explanation should connect these concepts to decisions a reader already understands. Adding another technical inventory would increase the burden.

## Give the reader a route and a destination

The opening should answer three questions immediately: what is being agreed, what changes for an application, and what can be evaluated today? “Three narrow pilot contracts” currently sounds like three customer deployments. “Conformance reference” will mean little to a business reader. Explain that this is runnable local reference software with synthetic examples, before describing benefits to test.

Suggested insertion after the lead:

> Imagine receiving a quote with a price of 123.45. Before using it, your application needs to know the currency, the quantity that price covers, who is buying, and whether fees are included. Midnight Express makes those assumptions part of an explicit agreement. Each application translates its own format into that agreement; the receiver checks the result before considering any action.
>
> The current release is a local reference implementation. It demonstrates three narrowly defined workflows with synthetic test cases: quote observations, payment observations, and approval for a sandbox report write. It gives developers something concrete to inspect and reproduce while production transport, authenticated sources, and partner validation remain further work.

Add a short route beside the jumps: “Start with the quote example to understand the idea. Read the three workflow contracts to see its scope. Use Evidence and Getting started to assess an integration.” Engineers can still open technical details. Everyone else gets permission to follow a shorter path.

## Explain the quote transformation as a sequence

The two quote cards are useful, but “1,234,500 cents per 100 shares” requires deliberate arithmetic. Narrate the conversion and its dependencies before introducing fingerprints. Readers also need an example of refusal that shows the practical outcome.

Suggested insertion after the agreed total:

> Format B gives a price for a block of 100 shares. Its adapter divides 1,234,500 cents by 100 to obtain 12,345 cents per share, or $123.45. It also translates the dealer’s selling perspective into the buyer’s purchasing perspective. With the declared currency and no-fee convention, both formats describe the same $12,345 quote from the same source.
>
> If Format B omitted “per 100 shares,” the adapter would refuse the message. A plausible-looking number would not tell it whether the total covered one share or the full block. The integration would need a clarified source convention before that message could proceed.

This is the clearest before/after example on the page: implicit convention becomes declared meaning; missing convention becomes a visible integration issue. Keep “intent fingerprint” in the expandable technical explanation, where its source-identity qualification can receive enough attention.

## Build a bridge between the three layers

The layer cards introduce components but leave readers to reconstruct their relationship. “Contract” can suggest a legal agreement or a blockchain smart contract. “Profile” later appears as an unexplained synonym. Establish a consistent public term, such as “workflow contract,” and explain that the reference calls its three bounded variants profiles.

Suggested bridge before the layer cards:

> An adapter answers, “How does this application express the information?” A workflow contract answers, “Which information is required, and which combinations make sense?” The shared core records which event and agreement are being used. Together they make a message interpretable without requiring every application to use the same internal database or API format.

Avoid making “contract commitment” the next conceptual hurdle. First say that the receiver must have reviewed and installed the exact agreement. Then explain the fingerprint as an identifier for those definitions, rather than a substitute for review.

## Separate interpretation, evidence, permission, and effect

The page correctly states these boundaries repeatedly, but the cumulative caveats become difficult to remember. Introduce one concrete sequence and use the later sections to elaborate it.

Suggested insertion near the workflows:

> A checked message answers a limited question: does this information fit the agreed meaning? Other checks answer different questions. Did the claimed source actually send it? Is its evidence sufficient and current? Does this application have permission to act? If it acts, how will it recover after an interrupted reply? The data model makes interpretation explicit; the application must connect that interpretation to the appropriate authority and recovery rules.

Use payment as the boundary example: “A reported $250 payment against a $500 invoice is a payment observation. It does not by itself decide the remaining accounting balance or mark the invoice paid.” Use approval as the effect example: “The local host can write one fixture-authorized report row. Passing validation alone does not perform that write.” These examples should precede technical names such as `executes:false`.

## Reduce vocabulary load and answer the next questions

Add a small expandable glossary rather than expanding every paragraph. Define RFQ as request for quote; adapter as a reviewed format translator; profile as a bounded workflow contract; canonicalization as producing one agreed byte representation; replay as processing previously seen information again; and effect as the change an application actually makes. Spell out MPE, RPC, ERC-20, SPL, and CPI on first use or keep them inside technical details. “Projection” needs the plain explanation “a bounded transfer record extracted from supplied chain evidence.”

Add two FAQs:

> **What happens when a message uses an unsupported term?** The current contracts refuse unknown fields and unsupported conventions. Partners can review a new contract instead of silently assigning a default meaning.
>
> **What do the test counts tell us?** The three RFQ interpreters agree on 35 synthetic cases: four accepted and 31 refused. The PostgreSQL sandbox has 56 recovery checks, including four worker kills, for a fixture-authorized report write. These establish behavior in the tested examples; they do not estimate customer error rates, integration savings, or production reliability.

Keep the chain section secondary in the reading route. Its 291 entries are proposed vocabulary, while implemented chain projections are read-only and fixture-based. That distinction should appear before the inventory, so readers interpret the impressive count correctly. The page should leave a reader able to explain one successful mapping, one refusal, and one authority boundary before asking them to absorb the broader architecture.
