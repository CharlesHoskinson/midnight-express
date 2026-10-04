# Financial workflow review

Reviewed 3 October 2026. Evidence: [live page](https://charleshoskinson.github.io/midnight-express/), its `use-cases.js`, local `website/dist/index.html`, `website/dist/app.js`, `website/dist/use-cases.js`, and canonical [use cases](../../docs/product-requirements/use-cases.json) and [ranked portfolio](../../docs/product-requirements/top-ten-use-cases.md). The fetched live use-case data matched the local distribution byte for byte. This is a text and product-content review, not a browser usability test.

The first two pilots are understandable business opportunities, but their page cards describe implementation scope before giving readers a recognizable workday. The canonical data already contains actors and triggers; the card renderer omits both. It shows a title, value hypothesis, delivery stage, first scope, shared stack, measure and remaining gate. Thus a visitor meets “RFQ,” “reconciliation,” “ERP,” and “anchored-binding” without seeing who needs the product or what they do with it.

Add one concrete story to each financial card and expand jargon at first use. Label these as illustrative pilot scenarios: the current portfolio marks both demand and business value as unvalidated hypotheses. Keep current scope and gating visible immediately after the story. The copy below preserves UC-01 and UC-03 and does not imply a live product or proven savings.

## UC-01: Request and compare confidential trade quotes

**Suggested summary:** An investment firm's trader requests prices from selected dealers, compares signed offers and records an acceptance without exposing the trade details to delivery infrastructure.

**Actor:** An investment firm's trader, two approved dealers, the firm's compliance reviewer and the team that completes the trade.

**Trigger:** The trader needs a price for a planned asset purchase and asks the two approved dealers for offers. A request for quote, or RFQ, asks “What price will you offer for this transaction?”

**Illustrative three-step story:**

1. The trader sends a confidential request describing the asset, amount and response deadline to the two approved dealers. Each dealer returns an offer signed by an authorized representative, including a price and an expiry time.
2. The trader compares the offers, completes the firm's required review and signs acceptance of one offer before it expires. The workflow preserves which exact offer was accepted, so a changed offer or a repeated acceptance cannot silently become a new agreement.
3. The firm's operations team recovers that same accepted record after a connection interruption and hands the agreed terms to its existing settlement process. The pilot ends with a clear handoff; the asset and money still move through the firm's separately authorized process.

**Why this might matter:** Trade intent and offer terms stay within the authorized workflow rather than being readable by message relays. The trader and operations team may spend less time finding the accepted version and checking that both sides agree. This is a hypothesis to measure, not an anonymity or savings guarantee.

**Value measures:** Compare the median time from request to first valid quote and from request to accepted quote with the design partner's current process. Count staff minutes spent checking accepted terms and preparing the settlement handoff. During an outage exercise, verify that the accepted quote is recovered without loss or a second acceptance. Agree numeric targets with the customer before the pilot; the requirements provide no observed improvement percentage.

**Initial scope boundary:** Backend and desktop coordination of requests, signed quotes, expiry and acceptance outside the blockchain. Acceptance is a recorded business decision, not evidence that settlement completed. Automatic settlement requires a contract integration, proven signer authority, protection against repeated execution and evidence linking the action to the exact anchored message. A first design partner is still needed. Confidential content does not imply that network timing, connections or all counterparties are invisible.

**Short card version:**

> A trader asks two approved dealers for prices. Each returns a signed offer with an expiry; the trader accepts one and the operations team receives the agreed terms. An interruption should preserve the accepted offer. The first pilot coordinates the agreement and handoff; automatic settlement comes after separate authorization and contract checks. Measure quote turnaround, staff checking time and recovery after an outage.

## UC-03: Match an invoice to confirmed payment status

**Suggested summary:** A supplier and customer exchange confidential invoice updates and verified payment notices, helping finance teams see what is paid and what still needs attention.

**Actor:** A supplier's finance system, the customer's finance and treasury teams, and a bank or payment-service integration that supplies authenticated payment evidence. Treasury is the team that manages the company's cash and payments.

**Trigger:** The supplier issues an invoice; subsequent approval, payment, dispute or refund changes its status.

**Illustrative three-step story:**

1. A supplier issues invoice INV-104 for $12,000. Its finance system sends the customer a signed notice with the invoice reference, amount and status. If someone needs the invoice document, they explicitly retrieve it from authorized encrypted storage; receiving the notice does not automatically download the attachment.
2. The customer approves the invoice through its existing finance process and pays through its existing bank or payment service. An authenticated notice reports which payment corresponds to INV-104. Express coordinates these updates; the pilot does not initiate the payment.
3. The supplier's finance system checks the reference and amount before recording the invoice as paid. A $10,000 payment against the $12,000 invoice stays unresolved rather than being marked fully paid. Repeated notices must not create a second accounting entry, and after a disconnect the system catches up on retained updates or reports a gap that needs attention.

**Why this might matter:** Finance teams may spend less time comparing email, bank records and accounting entries to discover which invoice a payment covers. Invoice details, amounts and customer relationships remain protected from delivery infrastructure. Source authentication and matching rules determine whether the status can be trusted; encryption alone does not prove that money arrived.

**Value measures:** Count invoices still unmatched at the end of the same agreed reporting period, staff minutes per invoice requiring investigation, and duplicate accounting entries caused by retry or recovery. Exercise a repeated invoice notice, a wrong-amount payment and a disconnect/restart. Compare against the customer's baseline and agree targets before the pilot; do not promise universal matching rates or automatic elimination of manual work.

**Initial scope boundary:** Match invoices with authenticated payment-status notices in a backend workflow. The first pilot does not execute payments. Connecting the customer's accounting system and validating payment evidence are remaining requirements. External accounting updates need destination duplicate protection: the receiving system must recognize an already recorded update. A delivery receipt or failed processing notice is neither proof of payment nor permission to send money. Disputes, refunds and accounting policy remain under the customer's authority; longer history needs a separate retention plan.

**Short card version:**

> A supplier sends a $12,000 invoice notice. The customer pays through its existing bank, and a verified payment notice lets the supplier match the payment to that invoice. A wrong amount stays unresolved; repeated notices should create one accounting entry. The first pilot tracks and matches payment status without sending payments. Measure unmatched invoices, staff investigation time and duplicate entries.

## Explain the finance terms where they appear

| Term | Plain-language explanation | Suggested placement |
|---|---|---|
| RFQ | Request for quote: asking selected dealers what price they will offer for a specified transaction. | Spell out in the card title or first sentence. |
| Dealer | An approved firm that offers a price and can take the other side of the trade. | First RFQ actor description. |
| Settlement | Completing the agreed exchange of assets and money. | At the distinction between acceptance and completion. |
| ERP | Enterprise resource planning software: a company's system for records such as invoices, purchases and accounting. | Write “company finance system (ERP)” when introducing the integration. |
| Reconciliation | Checking that the invoice, payment and accounting records agree. | Prefer “match invoices to payments” in the heading; explain reconciliation in detail. |
| Payment adapter | An integration that brings payment status and evidence from a bank or payment service into the workflow. | Integration gate, after the business story. |
| Idempotency | Recording the same update once even if it arrives repeatedly. | Explain as “duplicate protection” alongside retries; retain the technical term in developer material. |
| Signed offer or notice | A record whose origin and integrity can be checked against an authorized sender. | First signed record; avoid implying that a signature alone establishes policy approval or payment truth. |

## Content decisions for the page

Put “Who uses it,” “What starts it,” and the three-step story before stack dependencies. Keep the one-sentence value hypothesis in the summary and the existing pilot status, measurement and remaining gate in the expanded card. Readers should be able to answer “Who does what differently?” before learning the protocol names.

Use explicit business states in both examples: a quote is requested, offered, accepted and handed off; an invoice is issued, approved, matched to payment or left unresolved. Keep delivered, recovered, accepted and completed distinct. In particular, “accepted quote” must not become “settled trade,” and “received payment notice” must not become “paid invoice” without authenticated evidence and successful matching.

The examples introduce fictional amounts and identifiers only to make the workflow tangible. They are not supported transaction types, production capabilities, pricing claims or customer references. Before turning either into a launch claim, record a real design partner, present process and cost, threat model, baseline, agreed numeric target, integration estimate and adoption decision, as required by the canonical portfolio.
