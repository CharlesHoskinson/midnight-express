<!-- Review via Grok CLI; selected model: grok-4.7; baseline: f0e3fc6. Recommendations require editorial/factual review. -->

# Data model page: decisions a partner still cannot make

The data model page gives a partner the three pilot profiles, a worked quote, and a precise evidence block. Adoption is still hard to judge from the page alone. The integration cards stop before the tradeoff a team would accept. The three workflow cards look equally mature, while independent Python, Rust, and TypeScript agreement covers RFQ only. Chain coverage is easy to overread: the reference implements two read-only fixture projections, and the 291 entries remain proposed vocabulary. The rule for moving a term into the shared core is easy to miss. The closing steps say to measure effort and leave the design-partner record undefined. Paste the drafts below at the places given.

## 1. State the quote contract as an integration tradeoff

The integration card promises that assumptions become visible. A dealer still needs the list of assumptions this pilot will leave unsupported, and a plain account of what the first connection includes. Place the paragraph in `#contracts`, immediately after the note that begins “This choice trades some flexibility…”.

> A dealer can quote 100 shares at $123.45 as dollars per share or as cents per hundred shares. The adapter records that declared conversion, the buyer or seller perspective, and the statement that the quote carries no fee. This pilot admits whole shares, US dollars at a scale of two, one explicit perspective, and a fee convention of none. Fractional shares, a second currency, or a commission are a separate contract, with a separate adapter and its own tests. One partner’s request leaves the shared core unchanged. For the first connection, send the quotes this contract already describes, and hold every other message for that separate review.

## 2. Make the quote example decide whose offer it is

The result line, 100 shares times $123.45 equals $12,345, shows that two encodings can meet. A buyer’s integration owner still has to see why equal economics from two desks stay different offers. Place the paragraph in `#example`, after the “AGREED RFQ MEANING” block and before the section note.

> The cash total is the start of the agreement. Two dealers can each describe a purchase of 100 shares at $123.45, so each cash total is $12,345, and the reference still keeps two intents, because each intent names its source. The buyer can compare the figures and can tell which desk made which offer. One dealer’s dollars-per-share file and that same dealer’s cents-per-hundred file agree when the adapter preserves the full attested intent: price basis, quantity, perspective, and no fee. A missing currency, a total that contradicts price times quantity, or a fee this contract cannot represent stops that message. Later steps receive a refused quote, with the basis still absent.

## 3. Allocate the proof across the three profiles

Under “Different business rules. The same agreement mechanism.”, the cards look like one finished set. The cross-language limit appears only in a note at the bottom of `#workflows`. Place this paragraph directly under that heading, before the cards.

> The three pilot profiles share one agreement mechanism and rest on different evidence. Quote observation is the profile interpreted independently in Python, Rust, and TypeScript. That campaign is 35 RFQ vectors, four accepted and 31 safe refusals, with no accepted disagreement in the set, plus fifteen adapter cases for the two declared formats. Payment observation and sandbox approval are reference-tested v0.2 contracts, with closed fields and conformance checks of their own. The three-language campaign covers RFQ. A design partner should start with quotes when the mismatches in front of them are price basis, units, and perspective. Payment and approval are sound later candidates for a partner who has read the written contract and the reference tests that exist for that profile today.

## 4. Read 291 names beside two projections

The `#chains` lead puts the vocabulary inventory and the chain families in one breath, so a partner can think the lists are integrable surface area. Place this paragraph after that lead and before the Ethereum and Solana columns.

> The number 291 counts proposed vocabulary: queries, subscriptions, transaction outcomes, state, tokens, wallet permissions, and application-specific activity. It is a map of distinctions for contracts that are still ahead. The reference implements two read-only projections over supplied fixtures. One projects ERC-20 transfers from receipts and logs. The other projects legacy SPL Token Program TransferChecked transfers. Token-2022 lies outside the Solana slice. Both keep raw amounts, zero included, and a physical inclusion identity. Twenty-eight fixture checks cover zero and maximum amounts, failed execution, repeated inner calls, rollback, re-inclusion, and replay. A design partner who already reconciles token movements from exported receipts can compare one projection with that export. Every vocabulary entry without a projection remains a proposal.

## 5. Give governance a stability a partner can schedule

The two-profile promotion rule sits inside a collapsed detail in `#contracts`, yet it decides how long a reviewed adapter stays valid. Place this paragraph in the open, after the three layer cards and before “An exact agreement”.

> An adapter is reviewed against one installed commitment, and that commitment is the meaning the partner’s tests apply. Events already accepted keep it. A change of terms, units, or rules is a new commitment. The v0.1 bundle remains in the archive as a read-only historical release, and the current loader will not run it. A software fix that preserves the agreement ships under its own release identity, so a parser correction can go out while the business terms stay put. Domain owners propose new profiles themselves. A term enters the shared core after it has proved useful in at least two independent profiles and the cost of maintaining it is known. Until that happens, quote quantities, invoice amounts, and chain transfer amounts keep their own rules. Pin the installed commitment for the life of the pilot, and run a fresh acceptance pass when a new commitment is offered. Authenticated installation, and migration of a workflow already in progress, sit in a later deployment process.

## 6. Replace the payment and approval slogans with the partner’s remaining work

“Clearer reconciliation” and “reviewable limits” name aims. Each card needs the concrete case and the step the partner’s own team still performs. In `#workflows`, replace the “Value to test” line in the payment card and in the sandbox-approval card. Keep the scope sentence that already follows each line.

Payment card:

> Take an invoice whose payable amount is $500 and a source report of a $250 payment. The observation keeps the amount, a payment identity, and a status of Pending, Final, or Reversed. It also keeps effective time, observed time, and record time, checked in that order against a trusted current time. The amount has to be positive and no greater than the payable amount for every status. A reviewer can explain the partial payment and can point to a clock or an amount that fails. Posting the $250 to a ledger line, and treating Final as settled at the bank, remain the treasury team’s own controls. The contract stores the source’s assertion so those controls have an explicit input.

Approval card:

> The approval profile binds one sandbox action. A named person approves a single WriteReport proposal, including the authority domain, execution scope, input, target, policy, budget window, and expiry. A change of target conflicts with the action already consumed. In the PostgreSQL sandbox the authorized effect is one report row, committed with the record of progress. The host reserves the approved maximum, charges one Step for that write, and releases unused capacity. Fifty-six checks include four worker kills at the effect, commit, and acknowledgement boundaries. Recovery retained one fixture-authorized report row. A design partner can judge whether a named approval, a one-write budget, and recovery that preserves that single row are the control they want to pilot.

## 7. Define the design-partner evaluation

The four steps in `#start` end on “Measure real integration effort” and never say which record would earn a second profile. Place this paragraph after the ordered list and before the FAQ.

> Run one partner, one profile, and one source format beside the handling that partner uses now. Keep three lists: fields copied unchanged, fields produced from a declared convention such as cents per hundred shares, and messages refused. For each refusal, name the missing or contradictory term and the remedy, which is a source correction, a finished adapter declaration, or a new contract. Record the hours spent reviewing the adapter and explaining refusals. That log is the pilot result. Open a second profile when the first profile’s terms covered messages the partner was willing to exchange, and when every refusal still had a remedy that went through a reviewed contract. Use quote observation as the first profile where the partner’s mismatches are price basis, units, and perspective, because that is where the 35-vector campaign already exists. Consider the payment observation or the single report-row approval only after that log meets the test above. Where the partner already reconciles transfers from exported receipts, compare those exports with the ERC-20 projection or the legacy SPL projection as a separate read-only exercise. Report the hours and the refusal classes. Leave any saving unstated: this record describes the sample in the pilot, and customer baselines are still uncollected.
