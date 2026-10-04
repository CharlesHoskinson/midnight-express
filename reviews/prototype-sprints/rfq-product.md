# RFQ product validation across the first three prototype sprints

Status: proposed validation plan, 2026-10-03. This supplements [the sprint sequence](sequence.md), [financial semantics](../data-model/financial-semantics.md) and [UC-01](../../docs/product-requirements/top-ten-use-cases.md#uc-01). Three two-week timeboxes are planning assumptions, not a delivery commitment. No customer result, adapter implementation or measured saving is asserted here.

## Product question and boundary

Can a buyer and two authorized dealers privately exchange commercially meaningful quotes, independently understand the same obligations, choose a valid signed offer and recover an explicit off-chain acceptance with less handling work than their current process?

The first outcome is a signed offer and an application-recorded off-chain acceptance bound to its exact revision and economic terms. It is neither settled funds nor an executed on-chain trade. The business agreement must say what a firm offer and acceptance commit the parties to. UI wording, acknowledgements and evidence must distinguish delivery, processing, quote acceptance, execution confirmation and settlement. No payment or settlement instruction runs in these sprints.

Private commercial intent means RFQ product, size, prices, participants, roles and correlation selectors remain encrypted and absent from upstream topics, routing filters and broker logs. Approved recipients learn the terms necessary for their role. Whole-shard reception and local recognition must be demonstrated, with an irrelevant receiver unable to decrypt. Packet and topic inspection establish a bounded privacy result; timing, ingress identity, endpoint compromise, recipient onward disclosure and the symmetric profile's lack of forward secrecy remain outside that claim.

## Shared meaning is an acceptance gate

A private authenticated message can still produce the wrong trade if the two parties disagree about units or perspective. A shared event envelope solves identity and lifecycle plumbing, not economic meaning. A large common vocabulary can hide optionality and convention differences; a tiny home-grown field bag can omit obligations. A terms hash proves agreement on canonical bytes only after the adapters and displays agree on what those bytes mean.

Use the narrow, closed `mpe.rfq.asset-for-currency.v1` profile proposed in financial semantics. Reuse selected CDM concepts without claiming full CDM, FIX, FpML or ISO conformance. Before a partner trial, counterparties choose one real product and settle its conventions. Before that, use a visibly synthetic single asset against one fiat currency at an absolute unit price: one-way, all-or-none, no bond yield/clean-price conventions, inverse FX quotations or multi-leg structures. Do not treat a successful synthetic product as validation for an unsupported real product.

Required terms include asset scheme/identity and reference-data version; requester, dealer, buyer and seller; requester side tied to that asset; quantity and unit; exact decimal price, numerator currency, denominator asset/unit/base quantity and fee treatment; firm/indicative status; validity interval; immutable quote/revision and lineage; pinned settlement-policy/date context; and signer authority. A ticker, `Buy`, `price=99.5` or a schema ID alone cannot establish these meanings. Settlement terms describe agreed context, not a settlement effect.

For the synthetic example, 100 shares at USD 123.45 per share produce a USD 12,345.00 obligation before separately declared fees. The buyer owes USD and receives shares; the seller owes shares and receives USD. A dealer's reply must preserve those economic roles even though the message sender changes. Encode exact decimals as canonical coefficient/scale values; define precision, bounds, normalization and cash/fee rounding before hashes or calculations. Do not convert executable economics through binary floating point.

### Two independently specified participant formats

Require at least two genuinely distinct source formats: a buyer-side request format and a dealer-side quote format, specified and reviewed independently. Both dealers may use the same dealer format in the three-party demo; a second dealer adapter is additional scope. Two serializers generated from the same canonical struct do not establish interoperability. Without external participants, have separate internal owners author the fixture conventions and label the result internal; it remains weaker than customer integration evidence.

For example, the buyer fixture can express requester-side `purchase`, asset registry ID, quantity in shares and a maximum USD-per-share price. The dealer fixture can express dealer-side `sell`, a vendor instrument key, lots plus a pinned shares-per-lot multiplier, and a USD price per lot. Each source must carry an explicit convention/version; it is never inferred from field names. Mapping may convert lots and per-lot prices only when the pinned multiplier makes the obligation exact and within profile limits. The buyer's limit price is a constraint, not the dealer's signed offer price.

Publish a field-level mapping for each adapter: source field/schema/version, business meaning, cardinality, canonical field, units and denominator/base, perspective, reference-data lookup, precision/rounding, authority/provenance and rejection cases. Preserve source identity/version and authenticated source evidence separately from canonical economic terms. Test canonical-to-source reconstruction of the economic obligations where supported; require obligation equivalence rather than byte-for-byte round trips.

Any dropped fee, unknown economic field, unsupported product, missing multiplier, unresolved identity, ambiguous side or excess precision rejects the conversion before signing, display as actionable, or dispatch. Do not default missing fields or round away a mismatch. Retain the original authenticated payload in encrypted quarantine for authorized investigation. Non-economic annotations may be ignored only under a documented bounded rule. Error views must identify the unresolved meaning without exposing it to network operators.

### Conformance evidence

Both adapter owners produce expected obligations independently, then compare the canonical terms/hash and their participant-facing summaries. Positive fixtures must produce identical asset/currency obligations, units, sides, fees, validity and settlement-policy references. The signed acceptance binds the exact offer revision and terms hash; changed terms require a new immutable offer. A counterpart cannot accept a merely indicative quote under the firm-offer operation.

Negative vectors cover reversed requester/dealer perspective; conflicting buyer/seller identities; per-share versus per-lot/base-quantity mismatch; fiat USD versus similarly named token; wrong token network/scale; unknown asset or stale reference data; decimal equivalence, overflow and excess precision; omitted fees and unsupported rounding; inverse FX and bond yield rejection; unknown profile/version/economic fields; unauthorized signer; stale settlement policy; cancellation/replacement precedence; expiry at receipt versus acceptance; reordered duplicates and competing accepts. All must produce a typed rejection or explicitly unresolved state, never an apparently successful acceptance.

Transport expiry and business validity remain separate. Agree a receiving application's exclusive commit-before-expiry rule, clock uncertainty bound and offline/uncertain handling. Replay cannot renew validity. Acceptance at an uncertain deadline remains unresolved until policy permits a determination. Correlation, event identity, action identity, offer revision and envelope EID must not be conflated.

## Validate the product separately from the network

| Evidence lane | Test | What a pass supports |
|---|---|---|
| Meaning and workflow | Independent source adapters, offer comparison, user tasks and signed off-chain decision | Participants can coordinate this supported product under this profile |
| Transport and privacy | Actual sidecar exchange, local recognition, decryption negatives, expiry, packet/topic/log inspection | The tested transport and privacy boundary under the stated workload |
| Recovery | Restart/duplicate/concurrent acceptance and acknowledgement fault matrix | One committed local outcome and recoverable progress within this slice |
| Admission/platform | Genuine proof compatibility, wire fit, quota, finalized Registry and witness evidence | Only the admission/platform properties actually exercised |

A fast message round trip is not shorter quote handling. A stand-in admission demo may support workflow experimentation while admission remains red. Compiler/simulator results are not a Midnight network deployment. PostgreSQL persistence is not replicated retention, operator receipts or availability. Keep each lane's mock, synthetic, candidate, measured or blocked labels in the evidence manifest and demo.

## Baselines and task observations

With a design partner, document the current approved workflow before the trial: actors, channels, input formats, steps, waiting intervals, corrections and reconciliation handoff. Run comparable supported-product tasks in the current process and prototype; record training, familiarity, task difficulty, participants and sample size. If no partner is available, collect internal synthetic observations and a baseline collection plan. Leave customer savings and willingness to adopt unknown.

| Measure | Operational definition |
|---|---|
| Quote turnaround | Elapsed time from a complete authorized RFQ becoming available to the first valid comparable firm offer; separately measure RFQ-to-off-chain-acceptance |
| Handling minutes | Active human minutes creating/checking requests, normalizing terms, comparing offers, resolving errors, approving and reconciling; exclude waiting and report it separately |
| Handoffs/rework | Count manual transfers, duplicate entry, clarifications, rejected mappings and corrections per completed task |
| Comprehension | Before acceptance, user identifies asset identity, quantity/unit, buyer/seller, cash obligation and fees, validity, and whether funds have moved; record each answer and critical error |
| Recovery | Time to a trustworthy outcome after an injected outage, replay count, ambiguous cases and additional human minutes |
| Integration effort | Logged engineering hours by source-format analysis, mapping, reference data, authority, validation, UI, recovery and deployment; recurring change/support effort separately |

Use tasks that require comparing two valid offers, recognizing a per-lot/per-unit mismatch, refusing an expired/replaced offer and recovering after disconnect. Have participants explain the outcome in their own words. Any wrong economic obligation or belief that an off-chain acceptance moved funds blocks that task's product acceptance and triggers a display/profile review. Record failures and abandoned tasks, not just successful timings. Agree numeric improvement and comprehension thresholds with a partner before evaluation; do not invent a percentage saving, ROI, SLA or universal benchmark from the synthetic run.

## Three sprint checkpoints

| Checkpoint | Concrete product deliverable and required evidence | Decision |
|---|---|---|
| Sprint 1: meaningful RFQ slice | Buyer and two approved dealers run request, signed offer/decline and one off-chain acceptance. Publish closed profile, two independent source mappings, obligation/hash comparisons, negative conformance vectors, trusted term summaries and comprehension observations. Capture initial baseline or label its absence. Show actual transport/privacy traces and separate admission feasibility status. | Continue only with supported semantics and visible unresolved gates. Fix lossy mappings or misleading acceptance wording before broader workflow claims. An internal demo does not establish partner demand. |
| Sprint 2: recovered commercial outcome | Reuse the same profile/adapters. Crash before commit, after commit before acknowledgement, and during retry; replay/concurrent competing accepts preserve one accepted revision under the explicit application rule. Show late/uncertain outcomes and reconciliation view. Measure recovery and handling minutes, including manual resolution. | Continue reuse only after durable transaction/fault evidence passes. Repeat comprehension tasks on recovered/ambiguous states. A receipt alone cannot mark a quote accepted. |
| Sprint 3: reuse and pilot decision | Reuse the event/recovery core for one invoice fixture and one bounded human-approved sandbox action while preserving separate domain meanings. Report added adapter effort and profile changes, RFQ baseline comparison where available, unresolved production gates and admission disposition. Produce a constrained pilot decision pack. | Seek a scoped partner evaluation only with declared supported product, boundaries and owners; repeat blocked work or commission missing feasibility work otherwise. Sprint 3 is not production release or settlement readiness. |

## Integration cost and profile governance

Assign named owners before implementation: product owner for supported obligations and workflow wording; each participant's adapter owner for source semantics; profile maintainer for schema/canonicalization/conformance; authority owner for roles and signing; and operations owner for recovery/evidence. Unfilled roles are planning gaps. Log hours and dependency/licensing costs as incurred; record estimates with assumptions and uncertainty separately. Include onboarding and convention negotiation, key/role setup, reference-data maintenance, source-schema changes and support in the adoption decision. Common code reuse alone does not establish cheap integration.

Freeze a profile/version, reference-data snapshot, settlement-policy hash and accepted vectors at each checkpoint. A change to perspective, unit, denominator, rounding, fees, validity or authority requires semantic review, new vectors and an explicit version/migration decision. Unknown versions fail closed. Both participant owners approve mappings; neither can silently redefine shared obligations. Preserve original signed records and do not reinterpret accepted offers under a newer profile. Derivative CDM materials retain pinned source/version and artifact-specific notices; vocabulary adoption does not grant a standards-conformance claim.

The pilot pack contains the supported product and exclusions, customer owner or explicit absence, threat model, baseline/tasks/results, commands/versions/fixtures, comprehension failures, measured integration hours, fault matrix and production blockers. Automated settlement stays gated on independent signed business authority, atomic replay protection, CON-060 anchored-message binding and contract adapter evidence. The commercial coordination outcome remains useful on its own and must be evaluated on that basis.
