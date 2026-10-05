import MidnightExpress
namespace MidnightExpress.Examples
open MidnightExpress
def failing (c : Context) (ev : Event) : List String :=
  let e := ev.envelope
  let common : List (String × Bool) := [("trusted", decide (c.trusted = true)), ("dispatch", decide (dispatch ev.envelope = some ev.payload.profile)), ("notFuture", decide (ev.envelope.occurred ≤ c.now)), ("sourceRole", decide (lookup ev.envelope.source c.sources = some (SourceAuthority.mk ev.payload.profile.role ev.payload.principal)))]
  let sem : List (String × Bool) := match ev.payload with
    | .rfq q => [("rfq.rfqOpenTerms", decide (lookup q.rfqId c.rfqs = some (true, q.terms))), ("rfq.buyer", decide (q.buyer = q.expectedBuyer)), ("rfq.seller", decide (q.seller = q.expectedSeller)), ("rfq.distinct", decide (q.buyer ≠ q.seller)), ("rfq.assetRef", decide (q.price.assetRef = q.terms.asset)), ("rfq.priceUnit", decide (q.price.unit = q.terms.quantity.unit)), ("rfq.priceCurrency", decide (q.price.currency = q.terms.currency)), ("rfq.baseQty", decide (q.price.baseQuantity = 1)), ("rfq.shareUnit", decide (q.terms.quantity.unit = .share)), ("rfq.qtyValid", decide (q.terms.quantity.value.ValidAt 0)), ("rfq.priceValid", decide (q.price.value.ValidAt 2)), ("rfq.cashValid", decide (q.cash.ValidAt 2)), ("rfq.occBeforeFrom", decide (e.occurred ≤ q.validFrom)), ("rfq.fromNow", decide (q.validFrom ≤ c.now)), ("rfq.nowUntil", decide (c.now < q.validUntil)), ("rfq.cashProduct", decide (q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient))]
    | .invoice i => [("inv.invoiceTerms", decide (lookup i.invoiceId c.invoices = some i.terms)), ("inv.evidence", decide (lookup i.paymentId c.paymentEvidence = some i)), ("inv.effBeforeObs", decide (i.effectiveAt ≤ i.observedAt)), ("inv.obsBeforeOcc", decide (i.observedAt ≤ e.occurred)), ("inv.amountLePayable", decide (i.amount.coefficient ≤ i.terms.payable.coefficient)), ("inv.amountValid", decide (i.amount.ValidAt 2)), ("inv.payableValid", decide (i.terms.payable.ValidAt 2)), ("inv.rail", decide (i.rail = "fixture-bank-v1"))]
    | .agent a => [("agent.domain", decide (a.authorityDomain = c.authorityDomain)), ("agent.scope", decide (a.executionScope = c.executionScope)), ("agent.window", decide (a.budgetWindow = c.budgetWindow)), ("agent.proposalDigest", decide (a.proposalDigest = c.proposalDigest a.proposal e.contract)), ("agent.proposalRecord", decide (lookup a.actionId c.proposals = some a.proposal)), ("agent.policy", decide (a.policyDigest = c.policyDigest)), ("agent.human", decide (a.human ∈ c.humans)), ("agent.notRevoked", decide (a.actionId ∉ c.revokedActions)), ("agent.occBeforeFrom", decide (e.occurred ≤ a.validFrom)), ("agent.fromNow", decide (a.validFrom ≤ c.now)), ("agent.nowUntil", decide (c.now < a.validUntil)), ("agent.untilExpires", decide (a.validUntil ≤ a.proposal.expires)), ("agent.target", decide (a.proposal.target ∈ c.sandboxTargets)), ("agent.budgetLe", decide (a.proposal.budget.value.coefficient ≤ c.maxSteps)), ("agent.budgetValid", decide (a.proposal.budget.value.ValidAt 0)), ("agent.stepUnit", decide (a.proposal.budget.unit = .step)), ("agent.maxEffects", decide (a.maxEffects = 1)), ("agent.domainConst", decide (a.authorityDomain = "urn:mpe:sandbox:local")), ("agent.windowConst", decide (a.budgetWindow = "window:fixture"))]
  (common ++ sem).filterMap (fun (k, b) => if b then none else some k)
#eval ("0 fixture_rfq offchain-quote-valid", failing context0 event0)
#eval ("1 fixture_agent sandbox-candidate-only", failing context1 event1)
#eval ("2 fixture_invoice-final final-payment-evidence-only", failing context2 event2)
#eval ("3 fixture_invoice-pending payment-evidence-pending-or-reversed", failing context3 event3)
#eval ("4 fixture_invoice-reversed payment-evidence-pending-or-reversed", failing context4 event4)
#eval ("5 corpus_side reject", failing context5 event5)
#eval ("6 corpus_cash reject", failing context6 event6)
#eval ("7 corpus_expired reject", failing context7 event7)
#eval ("8 corpus_expired-approval reject", failing context8 event8)
#eval ("9 corpus_price-asset reject", failing context9 event9)
#eval ("10 corpus_payment-final-invention reject", failing context10 event10)
#eval ("11 corpus_missing-payment-evidence reject", failing context11 event11)
#eval ("12 corpus_unauthorized-human reject", failing context12 event12)
#eval ("13 corpus_changed-target reject", failing context13 event13)
#eval ("14 corpus_changed-input reject", failing context14 event14)
#eval ("15 corpus_profile-hash reject", failing context15 event15)
#eval ("16 corpus_unknown-profile reject", failing context16 event16)
#eval ("17 context_no-trust reject", failing context17 event17)
#eval ("18 context_revoked reject", failing context18 event18)
#eval ("19 context_low-budget reject", failing context19 event19)
#eval ("20 context_no-role reject", failing context20 event20)
#eval ("21 context_wrong-principal reject", failing context21 event21)
#eval ("22 context_no-proposal reject", failing context22 event22)
#eval ("23 context_unknown-target reject", failing context23 event23)
#eval ("24 context_wrong-policy reject", failing context24 event24)
#eval ("25 quote_at_validFrom offchain-quote-valid", failing context25 event25)
#eval ("26 quote_at_validUntil reject", failing context26 event26)
#eval ("27 approval_at_validFrom sandbox-candidate-only", failing context27 event27)
#eval ("28 approval_at_validUntil reject", failing context28 event28)
#eval ("29 sell_side offchain-quote-valid", failing context29 event29)
#eval ("30 cash_overflow reject", failing context30 event30)
#eval ("31 rehashed_changed_proposal reject", failing context31 event31)
#eval ("32 observation_after_occurrence reject", failing context32 event32)
#eval ("33 complete_evidence_overpayment reject", failing context33 event33)
#eval ("34 future_occurrence reject", failing context34 event34)
#eval ("35 closed_rfq reject", failing context35 event35)
end MidnightExpress.Examples
