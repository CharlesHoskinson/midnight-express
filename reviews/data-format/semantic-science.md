# Semantic science review of the unified data format

Review date: 2026-10-03. Role: principal data scientist. Scope: the proposed unified model, three executable profiles, examples and validator, and the Ethereum/Solana vocabulary catalog. This review changes no contracts or runtime artifacts.

## Assessment

The bounded-context design is sound: common syntax, immutable interpretations and domain-owned economics are a stronger basis for agreement than a universal transaction object. The executable slice demonstrates exact arithmetic and deterministic rejection, but it does not yet demonstrate independently shared meaning. Several small current defects should be corrected before expanding the pilot. The chain catalog is a useful research inventory; its counts measure proposed vocabulary breadth, not validated economic coverage or data quality.

No production execution, source authentication, chain payload schemas, independent adapters or cross-language interoperability are implemented. These are explicitly declared future work, not discoveries of undocumented missing functionality. All successful checks below return `executes:false`.

## Evidence and reproducibility

Read `docs/product-requirements/unified-data-model.md`, `model/README.md`, all three schemas and five examples, `model/validator.py`, `model/test_conformance.py`, and all catalog records, metadata schema, README and tests. Examined primary-source archives for ERC-20, Solana transaction/RPC structures and pinned FINOS CDM measures. The archives distinguish successful captures from failed or redirected evidence; they are research snapshots rather than deployment trust roots.

Executed from the repository root:

```bash
/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py
/tmp/mpe-data-model-validation-env/bin/python model/domains/test_catalog.py
```

Observed: 51 reference checks pass, three schema self-checks pass, and 12 catalog tests pass. The five unsigned example sizes are 1116, 964, 971, 974 and 1252 bytes for agent, invoice-final, invoice-pending, invoice-reversed and RFQ respectively. They satisfy the raw 3926-byte limit; these sizes establish nothing about sealing overhead or wire acceptance.

A Python scan of `chain-event-catalog.json` measured:

| Chain | Native | Decoded | Derived | Intent | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ethereum | 32 | 41 | 14 | 40 | 127 |
| Solana | 35 | 53 | 13 | 39 | 140 |
| Both | 67 | 94 | 27 | 79 | 267 |

All 40 chain/family combinations are represented. 135 of 267 records use exactly the generic qualification `Candidate vocabulary; source evidence and adapter validation are required.` This is an inventory-specific specificity measurement, not a finding that those contracts are unsafe or incorrect. No real partner traffic, source accuracy, rejection rate, decoder precision or runtime coverage was measured.

## Current defects and ambiguities

### S1 — ASCII identity grammar admits a terminal newline

**Current reproducible defect; medium severity; small correction effort.** In `model/schemas/{agent,invoice,rfq}.v0.1.json`, identifier patterns use `$`. The reference JSON Schema implementation accepts a match immediately before a final newline. The README instead promises closed ASCII identity grammars and exact equality.

Starting with `event:rfq`, set `data.quoteId` to the decoded string `quote:demo\n`: the harness accepts `offchain-quote-valid`. Starting with `event:agent`, set `id` to `event:agent\n`: it accepts `sandbox-candidate-only`. No trusted fixture change is needed. JSON serialization encodes the newline as an escape, so raw UTF-8 parsing does not remove this defect. Exact equality makes these distinct IDs; trimming in another adapter would create disagreement.

Correct all affected identifier/coefficient/source patterns or add a portable exact grammar semantic check; do not silently strip whitespace. The validator already uses `re.fullmatch` for instants, so timestamps do not exhibit this particular escape. Validate terminal LF/CR, embedded whitespace and escaped newline variants across both independent interpreters. Changing pinned schemas or validator requires new commitments and review.

### S2 — Overpayment exclusion depends on payment status

**Current documented-boundary inconsistency; medium severity; small effort.** `model/README.md` says overpayment is outside the invoice profile. In `Harness._semantic`, the `status != 'Final'` return precedes the amount/payable comparison.

Counterexample: start with `event:invoice-pending`, retain payable coefficient `50000`, set amount coefficient `50001`, and set the matching trusted `paymentEvidence['payment:pending']` to the same complete data record. The harness accepts `payment-evidence-pending-or-reversed`. The identical amount/payable relationship under `Final`, with a matching trusted evidence record, rejects `overpayment-outside-profile`.

This does not demonstrate fabricated evidence bypassing trust: the experiment deliberately changes trusted context. It demonstrates that context agreement and profile arithmetic are different checks. Decide whether the exclusion applies to all observations or only final ones. Either move the constraint before the early return, or document that pending/reversed overpayment observations remain representable. Test all three statuses with equal, smaller and larger amounts.

### S3 — Invoice occurrence and observation times have no stated relationship

**Current semantic ambiguity; medium severity; small specification effort.** For `event:invoice-final`, change only envelope `time` from `11:00` to `2026-10-04T10:00:00.000Z` while `observedAt` and `effectiveAt` remain `11:00`. The harness accepts the complete fixture record. It checks `effectiveAt <= observedAt <= now` and separately `time <= now`, but relates neither timestamp to the other.

If occurrence means occurrence of this payment observation, an observation cannot occur before its observation time. If it means occurrence of the payment, the envelope may intentionally describe another clock, but that meaning needs to be explicit and separated from observation/report creation. Do not add an arbitrary ordering rule until domain ownership decides. Specify occurrence, effective, observation and ingestion time; include equality, delayed reporting and genuinely earlier effective dates in fixtures. Otherwise latency/freshness statistics mix different clocks.

### S4 — Compute-budget intent is classified as an RPC request

**Current catalog taxonomy defect; medium severity; small effort.** Record `mpe.solana.simulation.compute-budget-intent.v1` has `sourcePrimitive: 'ComputeBudget instructions'`, `sourceStandard: 'Chain RPC'`, `messageKind: 'rpc-request'`, and a generic RPC source URL. An instruction/configuration proposal is a different surface from an RPC request to simulate or submit the enclosing transaction. Existing catalog entries already distinguish application intent from `simulateTransaction` and `sendTransaction` requests.

The archived RPC transaction example contains ComputeBudget program invocations. Official [Solana compute-budget documentation](https://solana.com/docs/core/fees/compute-budget) further distinguishes instruction-based configuration from transaction-format-specific message configuration. Thus this record also needs an explicit format/version boundary; research documentation does not establish deployment support. Classify the proposal as intent with precise primitive/version provenance, or make it an actual named RPC request. Validate that RPC-request records name RPC methods, and separately review wildcard subscription controls rather than forcing them through that rule.

### S5 — Submission responses are not classified consistently with other responses

**Current taxonomy ambiguity; low-to-medium severity; small effort.** `mpe.ethereum.rpc.submission-response.v1` and `mpe.solana.rpc.submission-response.v1` have `messageKind: 'observation'`, whereas both chains' `rpc.read-query-response.v1` and `subscriptions.subscription-response.v1` use `rpc-response`.

A submission result can be normalized into an observation, but the catalog does not say that these are normalized events instead of direct responses. Their source primitives identify only hash/signature, with no method/result/correlation description. Consumers selecting `rpc-response` would miss these records. Choose and document the layer: use rpc-response for method outcomes, and a separate observation only if normalization creates one. Preserve correlation and null/error/unknown-outcome distinctions; retain the existing warning that returned identity does not prove inclusion or execution.

### S6 — Native account bytes versus decoded nonce state needs a boundary

**Current vocabulary ambiguity; low-to-medium severity; small clarification effort.** `mpe.solana.transactions.nonce-account-observed.v1` is native, sourced from `getAccountInfo`, while `mpe.solana.staking.stake-account-observed.v1` is decoded, sourced from `StakeState`. A native account observation may legitimately carry uninterpreted bytes for a queried nonce account. A claim about its nonce/authority/state requires program-specific interpretation. The catalog does not specify which meaning the nonce record intends; do not infer an incorrect implementation where no payload exists.

Clarify the qualification or separate raw-account and decoded-nonce claims. Require native records to identify retained source fields and decoded records to identify the interpretation boundary. The same issue arises when providers offer parsed account projections: provider-parsed is still decoded, even when returned through a native RPC transport.

The following reproduces S1–S3 without modifying repository files:

```python
import copy, json, sys
sys.path.insert(0, 'model')
from validator import Harness, Invalid
context = json.load(open('model/conformance/trusted-context.json'))
def run(event, ctx=context):
    try:
        return Harness(copy.deepcopy(ctx)).check(json.dumps(event))['status']
    except Invalid as err:
        return str(err)
r = json.load(open('model/examples/rfq.json'))
r['data']['quoteId'] = 'quote:demo\n'
assert run(r) == 'offchain-quote-valid'
a = json.load(open('model/examples/agent.json'))
a['id'] = 'event:agent\n'
assert run(a) == 'sandbox-candidate-only'
p = json.load(open('model/examples/invoice-pending.json'))
p['data']['amount']['coefficient'] = '50001'
c = copy.deepcopy(context)
c['paymentEvidence'][p['data']['paymentId']] = copy.deepcopy(p['data'])
assert run(p, c) == 'payment-evidence-pending-or-reversed'
f = json.load(open('model/examples/invoice-final.json'))
f['time'] = '2026-10-04T10:00:00.000Z'
assert run(f) == 'final-payment-evidence-only'
```

## Strengths to preserve

The RFQ fixes currency, denominator asset, denominator quantity, unit and requester perspective. Its sample computes 100 shares × 12345 cents exactly to 1234500 cents; it checks cash overflow after multiplication, beyond individual coefficient bounds. Unknown fees reject instead of assuming zero. Distinct buyer/seller and both requester perspectives receive executable checks. This is a persuasive application of unitful measures rather than syntactic decimal normalization. Archived [FINOS CDM measures](../../catalog/data-model/financial-semantics/cdm-math-pinned.txt), pinned to the recorded commit, provide conceptual precedent without establishing CDM conformance.

Closed required objects make pilot missingness explicit through rejection. The invoice validates the complete trusted record, retaining Pending/Final/Reversed as source claims. Approval commits target, input, expiry, budget and policy, and checks exact trusted proposal agreement even after a recomputed hash. Occurrence identity and logical action identity differ deliberately; new occurrence IDs do not renew an approval.

Chain records preserve distinct Ethereum safe/finalized and Solana processed/confirmed/finalized vocabulary. Derived reconciliation stays local; intent does not provide execution evidence. Explicit chain families, decoder warnings, failed-transaction diagnostics and bridge initiation/destination separation avoid several common category errors. All catalog entries are proposed and deny effect authority; the metadata schema prevents direct authority escalation.

## Declared future gaps and scientific acceptance criteria

These are design gates for future profiles, not current runtime defects.

**Missingness must carry a reason.** Preserve absent, JSON null, unsupported method, unavailable history, omitted projection, encrypted/unavailable value, failed decode and observed zero separately. Archived [ERC-20](../../catalog/data-model/ethereum/erc20.txt) makes decimals optional and permits zero-value transfers; absence cannot imply 18 decimals or zero holdings. Archived [Solana RPC structures](../../catalog/data-model/solana/rpc-structures.txt) distinguish nullable/omitted transaction metadata and raw integer amounts from UI amounts. A confidential amount must not be rendered as zero. Keep these cases outside positive-only pilot primitives.

**Economic units must precede aggregation.** Preserve integer raw quantity, asset identity, program/contract and network, metadata provenance and scale. Price needs numerator, denominator, signed direction and fee basis. Raw transfer, transfer instruction, successful state delta and beneficial-owner economic transfer are different measures. Token-2022 withheld fees, protocol fees, transfer hooks and failed transactions make gross input, net received and balance change non-interchangeable. The `spl-transfer` primitive explicitly names `TransferChecked`; do not interpret its presence as coverage of every SPL transfer form. Its bounded scope is not a defect in an explicitly nonexhaustive catalog.

**Provenance labels are not confidence scores.** Native/decoded/derived/intent mixes interpretation level with requested-action purpose, but can work if narrowly defined. Native does not imply true, decoded does not imply successful execution, and derived does not imply low reliability. Future schemas should retain raw evidence identity, execution outcome, source authenticity and uncertainty independently. A derived finality/reconciliation claim must identify inputs and policy; a decoded event must identify decoder/deployment/version. The four labels alone cannot establish those properties.

**Cross-chain comparison needs explicit estimands.** Do not compare 'confirmed transactions' across chains without stating native commitment, observation window, execution success, deduplication and rollback treatment. Ethereum block number and Solana slot are not interchangeable clocks; use concrete hash/slot ancestry and reporting-time provenance. Do not count a bridge source message and destination redemption as two settled transfers. Keep RPC identity, signed-transaction identity, occurrence identity and business-action identity separate.

**Step is not yet a measurable resource unit.** `agent.data.proposal.budget.unit = 'Step'` is closed and bounded, but no pinned definition says what consumes a step. It can constrain this simulated fixture, not compare work/cost across executors. Before execution, define charging boundaries, partial failures and retries. Test two implementations against identical traces; they must report identical budget consumption.

## Prioritized next work and minimal pilot measurements

| Priority | Recommendation | Effort | Validation |
| --- | --- | --- | --- |
| P1 | Correct S1 exact grammar and resolve S2 overpayment boundary | Small | Negative whitespace corpus across runtimes; three-status arithmetic matrix; reviewed new commitments |
| P1 | Resolve S3 clock meaning before freshness/latency metrics | Small | Event/effective/observed/ingested examples with explicit expected relations |
| P2 | Resolve S4–S6 provenance/message taxonomy | Small | Record-level review, explicit transformation layer, method/decoder counterexamples |
| P2 | Independently implement two RFQ source adapters and a second interpreter | Medium | Same economics and intent digest, or explicit refusal; include cents per 100 shares and reversed perspective |
| P2 | Implement one bounded observation profile per chain before adding more families | Medium | Zero/max integer, unknown decimals, null/error, rollback, failed execution and omitted projection fixtures |
| P3 | Define Step metering and richer evidence/missingness contracts when execution enters scope | Medium | Independent trace replay and loss-accounting agreement |

A minimal useful pilot can use a small stratified fixture set plus prospectively collected partner samples. Publish exact denominators and case composition; synthetic passes must never be reported as operational error rates.

1. **Semantic agreement:** per source convention, record both adapters' canonical quantity/price/cash/roles and commitments. Report agreements, safe refusals and accepted disagreements divided by attempted mappings. Require zero accepted disagreements in the adversarial fixture set; report sample uncertainty for live data rather than claiming universal agreement.
2. **Economic conservation:** exact arithmetic failures divided by eligible RFQs, and raw-unit balance-delta reconciliation residuals for one successful token path per chain. Exclude noncomparable fee/confidential/failed cases explicitly; never fill residuals from missing values.
3. **Missingness and loss:** for each projected field, record required/present/zero/null/omitted/unsupported/unavailable/decode-failed, plus omitted byte/record count where measurable. Compare adapter completeness conditional on provider, method/version, commitment and transaction outcome.
4. **Evidence precision:** manually review a stratified sample of decoded/derived claims against pinned raw evidence. Report unsupported claims and execution-success mislabels separately from decoder syntax failures. Audit failed Solana transactions specifically.
5. **Temporal recovery:** inject duplicate delivery, reordering, disconnect and rollback. Measure unique source facts recovered within a stated range/filter/source/commitment, false completion claims and invalidated descendants retained. A metadata family count is not the denominator.
6. **Adoption cost:** log partner engineering hours to first independently verified mapping, manual corrections and unsupported conventions. The five examples and 267 catalog entries cannot establish reduced integration effort.

The decisive experiment is independent agreement under deliberately conflicting conventions, with refusals preserved as observable outcomes. More catalog entries alone will not supply that evidence.
