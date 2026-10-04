# Financial semantics: reuse industry concepts, constrain the first profile

Research date: 2026-10-03. Scope: the institutional RFQ and invoice reconciliation pilots selected in [recommended-stack-and-use-cases.md](../../docs/product-requirements/recommended-stack-and-use-cases.md) and [proposed-stack.md](../../docs/product-requirements/proposed-stack.md). This is a proposed domain profile, not a delivered integration or a claim of standards conformance.

## Recommendation

Use a small, closed, versioned **MPE RFQ profile** with an explicit mapping to selected FINOS Common Domain Model (CDM) concepts. Reuse its measures, price/quantity relationship, party roles, settlement terms and negotiation lineage. Select the first tradable product with the pilot counterparties; for an internal demonstration, limit the example to a single asset exchanged for one currency at an absolute unit price. Keep multi-leg derivatives, bond yield/clean-price quoting, optional settlement elections and arbitrary structured products outside that profile until a separate economic model is selected.

Use a separate **invoice evidence profile** based on a restricted UBL mapping. Carry claims about an invoice, reconciliation and payment observations; a payment instruction or settlement effect needs a different operation and independently verified authority. A common authenticated event envelope can contain both profiles, but cannot make an RFQ quote and an invoice payable amount interchangeable.

This is a choice to reuse an established conceptual model and introduce narrow application contracts around it. Do not begin by inventing an unconstrained `terms: object`, nor require the entire CDM runtime for every consumer. CDM's namespace documentation expressly describes selective adoption; the repository describes normalization, composition, mappings and embedded processes as design principles. That makes CDM a credible reusable foundation while leaving deployment size and supported products to the application. [CDM namespaces](https://cdm.finos.org/docs/namespace/), [FINOS repository](https://github.com/finos/common-domain-model).

## What the sources establish

| Source family | Useful contribution | Limit on adoption |
|---|---|---|
| FINOS CDM | Normalized economics and executable lifecycle concepts; composed product models rather than arbitrary field bags | Broad domain coverage does not settle the pilot's product, authority, reference-data or settlement policy |
| ISDA FpML | Product-specific economic descriptions and pretrade message design; quote validity is a separate concept | Do not copy an old RFQ flow and label it current 5.x conformance |
| FIX and SBE | Trade/message vocabulary and precise decimal encoding conventions | SBE is an encoding, not agreement on which asset, side or settlement obligation a value denotes |
| ISO 20022 | Distinction between shared business concepts, message components and message-specific constraints | Map a named message/version/usage context when integrating; “ISO 20022 compatible” alone is too vague |
| OASIS UBL | Established supplier/customer, invoice line and monetary-total vocabulary | An invoice is a commercial document, not proof that a bank or ledger completed payment |

The [CDM product documentation](https://cdm.finos.org/docs/product-model/) describes measures as values associated with units, qualifies prices with a denominator and price expression, and explains settlement direction through buyer and seller. Its [math model source](https://github.com/finos/common-domain-model/blob/9e036949e273a2f29a6a40aa222c5dd33c39b3ad/rosetta-source/src/main/rosetta/base-math-type.rosetta) makes quantity units mandatory. Those are the concepts to adopt; the pilot should tighten optional general-model fields into mandatory product-specific fields.

[CDM pretrade processing](https://cdm.finos.org/docs/pre-trade-processing/) models proposals, approvals, rejection, previous workflow steps and a resulting business event. That supports preserving negotiations rather than rewriting a quote in place. It does not establish that a Midnight event itself executes a trade or payment.

[FpML 5.12 quote expiry](https://www.fpml.org/spec/fpml-5-12-4-rec-1/html/pretrade/schemaDocumentation/schemas/fpml-asset-5-12_xsd/groups/QuotationCharacteristics.model/expiryTime.html) defines the time after which a quote is invalid. The archived [FpML 4.4 introduction](https://www.fpml.org/spec/fpml-4-4-12-rec-1/html/fpml-4-4-intro.html), sections 3.3.1–3.3.2, discusses loosely defined quotable products, one/two-way prices, maker updates, expiry and acceptance followed by trade execution. Use this historical text as design precedent. The [current FpML standards index](https://www.fpml.org/the_standard/) lists separate versions and views, including 5.13 Recommendation 2 and 5.14 Trial Recommendation; choose an actual view/schema before claiming an adapter is conformant.

The [FIX Trading Community SBE field specification](https://github.com/FIXTradingCommunity/fix-simple-binary-encoding/blob/master/v2-0-RC1/doc/02FieldEncoding.md) distinguishes semantic types from encoding and describes prices as a signed integer mantissa with a decimal exponent. It requires a matching schema to decode a message. These numerical and schema principles are useful even if MPE retains its existing wire and selects another payload codec. This archived file is a 2.0 release-candidate document, not evidence that the candidate is a ratified production version.

[ISO 20022's business model](https://www.iso20022.org/iso20022-repository/business-model) provides common definitions across financial messages; its [data dictionary explanation](https://www.iso20022.org/understanding-data-dictionary) describes message choices, multiplicity and constraints. This supports shared vocabulary plus bounded message profiles, rather than a single universal “financial event” type.

## RFQ profile: required semantics

The following is an application design recommendation. Its names are illustrative, not existing CDM or FIX field names.

| Area | Required profile contents and validation |
|---|---|
| Contract identity | Profile ID/version, immutable terms ID/hash, RFQ ID, quote ID, revision, prior revision, workflow ID; each event refers to a precise version |
| Parties | Requester, dealer, buyer and seller as distinct references; principal/agent capacity and signing authority context; each economic role maps to a participant identity |
| Perspective | `requesterSide = BuyAsset` or `SellAsset`; state which asset the side concerns. Dealer side is the opposite in this single exchange; roles remain fixed when message direction changes |
| Asset identity | Registry/scheme plus identifier; token assets additionally bind network and contract/asset identity. A symbol or ticker is display text, never sufficient identity |
| Quantity | Exact decimal, explicit unit, asset reference; positive and within profile precision/range. A token's atomic scale and a contract multiplier come from pinned reference data |
| Price | Exact decimal, price kind `AbsolutePerUnit`, numerator currency/asset, denominator unit/asset, quantity base, and whether fees are included |
| Currency | Explicit scheme/code and approved reference-data version. ISO currency codes and ledger token assets use distinct tagged types; a stablecoin symbol does not denote fiat settlement |
| Quote terms | `Indicative` or `Firm`, issued time, valid-from time, valid-until time, requested quantity and offered quantity; first profile is all-or-none and one-way |
| Settlement context | Agreed value date, settlement method/rail/network, DvP/PvP/non-atomic policy where applicable, business-calendar reference and rule, named settlement-policy version/hash; sensitive account references stay encrypted |
| Acceptance | Accepting party, quote revision/hash, quantity and price hash, expiry evaluation and relevant authority context. Counteroffers create new immutable terms, never mutate accepted ones |
| Evidence | Signature/signer binding, source provenance, authorized role, canonical signed bytes/hash, observed vs effective timestamps and applicable finality/context |

Do not overload `Buy` to mean “the sender buys.” The requester may buy the asset and a dealer's reply still describes that same proposed exchange. Carry both the requester perspective and resolved buyer/seller references; verify consistency. For two-way quoting, introduce a later explicit bid/offer union with sizes and dealer perspective rather than two unlabeled decimals. The CDM settlement model's buyer/seller direction is a useful base, but participant agreement on perspective must be part of the MPE profile, not inferred from a field label.

A demonstration can encode these economic obligations as:

```json
{
  "profile": "mpe.rfq.asset-for-currency.v1",
  "requester": "party:A",
  "dealer": "party:B",
  "requesterSide": "BuyAsset",
  "buyer": "party:A",
  "seller": "party:B",
  "asset": {"scheme": "pilot-registry-v1", "id": "asset:42"},
  "quantity": {"coefficient": "100", "scale": 0, "unit": "Share"},
  "price": {
    "kind": "AbsolutePerUnit",
    "coefficient": "12345", "scale": 2,
    "numerator": {"kind": "FiatCurrency", "code": "USD"},
    "denominator": {"assetRef": "asset:42", "unit": "Share", "baseQuantity": "1"},
    "fees": "Excluded"
  },
  "quoteKind": "Firm",
  "validUntil": "2026-10-04T16:00:00Z",
  "settlementPolicyRef": "pilot-policy:usd-share-exchange:v1"
}
```

This excerpt is not a complete quote; IDs, validity start, signatures, settlement date and policy resolution are omitted for readability. Its arithmetic is 100 × 123.45 = 12,345.00 USD before fees. Buyer A owes that currency amount and seller B owes 100 shares. A profile can derive those two obligations deterministically and compare them at both endpoints. It cannot derive a complete bond cash amount from an unlabeled `price=99.5`, nor safely invert an FX pair or turn a yield into a cash price without the correct product convention.

Define decimal value as `coefficient × 10^-scale`; bound both coefficient digits and scale, serialize coefficient as a canonical integer string, and reject floating-point conversions, locale formatting, ambiguous exponent strings and excess precision. Normalize equivalent decimal forms before hashing. Define a deterministic rounding stage and mode for cash obligations, fees and tax separately; reject unsupported input rather than silently round it. Currency minor units are not a universal price-precision limit. Profile arithmetic must prevent overflow and enforce a single canonical representation across Rust, TypeScript, database and proof adapters.

Use separate transport expiry and business validity. A quote received before its valid-until time can be invalid when a human accepts it later; replay must not refresh validity. Define acceptance as valid only if the designated receiving application commits the authorized acceptance before the exclusive expiry boundary under the agreed clock policy. Record late/uncertain outcomes instead of retrospectively claiming success. The pilot must specify maximum clock uncertainty, offline behavior, cancellation/replacement precedence and whether firm status creates an obligation under its business agreement.

Pin settlement policy with the terms. A message proves what a party stated; the application must still check allowed product, size, counterparties, settlement venue, account authority and policy. Off-chain `QuoteAccepted`, trade execution confirmation, invoice posting and settled funds are distinct states. A Midnight consumer effect additionally requires the selected stack's signed authority, replay protection and anchored-message binding.

## Invoice evidence profile

Use UBL's named concepts as a mapping target, then publish a small profile containing invoice identity/version, supplier and customer references, issue/due dates, document currency, line references and quantities, payable amount, taxes/allowances/charges/prepayments/rounding where present, document digest and source evidence. Preserve external purchase-order and ERP identifiers with their issuer/scheme. Corrections or credit notes reference prior documents and create new events.

The [UBL 2.3 Invoice model](https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html) distinguishes document, tax, pricing and payment currencies; it defines invoice lines and monetary totals including prepaid and payable amounts. Do not assume those currencies coincide. The first profile can require one currency and reject multi-currency documents pending a specified exchange-rate mapping. Tax calculation and monetary reconciliation require a named invoice usage profile; generic UBL vocabulary alone does not determine jurisdiction-specific rounding or totals.

Keep `InvoiceIssued`, `InvoiceMatched`, `PostingRecorded`, `PaymentObserved` and `PaymentReconciled` separate. A payment observation includes provider/rail, payment identifier, amount/currency, payer/payee references, status, source sequence/version, observation time, effective time, finality and reversal linkage. It is evidence of a source's assertion. Match partial payments, overpayments, fees and refunds explicitly; do not equate invoice payable amount with settled amount. A connector must authenticate its source, while destination idempotency and accounting policy control postings. Issuing or matching an invoice must never dispatch a payment implicitly.

## Adoption, mappings and verification

Implement typed Rust/TypeScript unions and deterministic validators from the selected profile, with no generic extension map inside executable economic terms. Unsupported fields or products fail validation; preserve the original authenticated payload in encrypted quarantine for authorized investigation. Separate non-economic annotations may be bounded and ignored under an explicit rule. A signature over bytes is insufficient if two consumers assign different meaning to the bytes.

Build participant-specific adapters that map into the shared profile, record source schema/version and convention set, and reject ambiguous conversions. Maintain a field-level table with cardinality, source meaning, canonical meaning, unit conversion, precision, perspective and unsupported cases. A dropped economic field is a failed conversion, not a warning. Hash the canonical economic terms and require counterparties to agree on that hash before acceptance; schema ID alone does not establish shared semantics.

Acceptance vectors should cover requester/dealer perspective reversal; quantity unit and token-scale disagreement; inverted FX pair and bond price/yield rejection; exact decimal equivalence and overflow; fees and rounding; expiry on receipt versus acceptance; replaced/cancelled quotes and reordered duplicates; stale settlement-policy references; unauthorized signer; and crash recovery after acceptance. Invoice vectors cover conflicting supplier IDs, tax/payment currency differences, document correction, partial/reversed payment and duplicate ERP posting. These are integration gates, not transport tests.

FINOS licensing needs artifact-specific handling. The [repository README](https://github.com/finos/common-domain-model) identifies Community Specification License 1.0 for specifications. The [license text](https://github.com/finos/common-domain-model/blob/master/LICENSE.md) distinguishes specifications and code, requires attribution for derivative specification materials, and contains patent-license acceptance and distribution provisions; section 4 treats source-code licensing separately. Preserve name, version, source and relevant notices when deriving a profile or distributing generated artifacts. Do not assume every tool, generated library or downstream dependency has the same license. This is an adoption checklist from the text, not legal clearance.

## Evidence archive and limitations

Online search preceded collection. Primary pages and code were collected with `/tmp/midnight-scrapling-env/bin/python` and `Fetcher.get(url, timeout=25)`. The [archive manifest](../../catalog/data-model/financial-semantics/manifest.json) records source URLs, extracted text files, fetch status, timestamps and SHA-256 hashes. These hashes identify archived extracted text, not original HTTP response bytes. CDM docs reported 7.0.0; inspected repository master was observed at commit `9e036949e273a2f29a6a40aa222c5dd33c39b3ad`, and additional model files were fetched at that commit. Documentation and master are not presumed to be the same release; select a release before implementation.

Failures are retained, not silently substituted: guessed `product-common.rosetta` returned 404; the guessed FpML 5.13 introduction returned 404; the FIX development implementation guide failed DNS resolution after Scrapling's retries; the official FIX introduction returned 202 with empty content. A corrected CDM common file contained only a namespace header, so substantive model checks used the pinned math/observable/settlement sources and full product documentation. Official legacy FIXimate links redirected to Orchimate; those rendering snapshots are archived as supplemental evidence, without claiming a verified primary standard publication or using them to settle side conventions. No authored finding above depends on search snippets or failed fetches.
