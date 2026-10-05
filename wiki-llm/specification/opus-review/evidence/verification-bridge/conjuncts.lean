import MidnightExpress.Examples
open MidnightExpress MidnightExpress.Examples

def commonConj (c : Context) (e : Event) : List (String × Bool) :=
  let env := e.envelope
  let p := e.payload.profile
  [("c.trusted", c.trusted),
   ("c.profileDecodes", decide (decodeProfile env.profile = some p)),
   ("c.specversion", decide (env.specversion = "1.0")),
   ("c.contentType", decide (env.contentType = "application/json")),
   ("c.contract", decide (env.contract = p.contract)),
   ("c.eventType", decide (env.eventType = p.eventType)),
   ("c.dataSchema", decide (env.dataSchema = p.dataSchema)),
   ("c.notFuture", decide (env.occurred ≤ c.now)),
   ("c.sourceKnown", (lookup env.source c.sources).isSome),
   ("c.sourceRole", decide ((lookup env.source c.sources).map (·.role) = some p.role)),
   ("c.sourcePrincipal", decide ((lookup env.source c.sources).map (·.principal) = some e.payload.principal))]

def rfqConj (c : Context) (e : Envelope) (q : RFQ) : List (String × Bool) :=
  [("q.openTerms", decide (lookup q.rfqId c.rfqs = some (true, q.terms))),
   ("q.buyer", decide (q.buyer = q.expectedBuyer)), ("q.seller", decide (q.seller = q.expectedSeller)),
   ("q.distinct", decide (q.buyer ≠ q.seller)), ("q.assetRef", decide (q.price.assetRef = q.terms.asset)),
   ("q.priceUnit", decide (q.price.unit = q.terms.quantity.unit)), ("q.priceCurrency", decide (q.price.currency = q.terms.currency)),
   ("q.baseQuantity", decide (q.price.baseQuantity = 1)), ("q.shareUnit", decide (q.terms.quantity.unit = .share)),
   ("q.qtyValid", decide (q.terms.quantity.value.ValidAt 0)), ("q.priceValid", decide (q.price.value.ValidAt 2)),
   ("q.cashValid", decide (q.cash.ValidAt 2)), ("q.occ≤from", decide (e.occurred ≤ q.validFrom)),
   ("q.from≤now", decide (q.validFrom ≤ c.now)), ("q.now<until", decide (c.now < q.validUntil)),
   ("q.cashProduct", decide (q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient))]

def invConj (c : Context) (e : Envelope) (i : Invoice) : List (String × Bool) :=
  [("i.terms", decide (lookup i.invoiceId c.invoices = some i.terms)),
   ("i.evidence", decide (lookup i.paymentId c.paymentEvidence = some i)),
   ("i.eff≤obs", decide (i.effectiveAt ≤ i.observedAt)), ("i.obs≤occ", decide (i.observedAt ≤ e.occurred)),
   ("i.notOver", decide (i.amount.coefficient ≤ i.terms.payable.coefficient)),
   ("i.amountValid", decide (i.amount.ValidAt 2)), ("i.payableValid", decide (i.terms.payable.ValidAt 2)),
   ("i.rail", decide (i.rail = "fixture-bank-v1"))]

def agConj (c : Context) (e : Envelope) (a : Approval) : List (String × Bool) :=
  [("a.domain", decide (a.authorityDomain = c.authorityDomain)), ("a.scope", decide (a.executionScope = c.executionScope)),
   ("a.window", decide (a.budgetWindow = c.budgetWindow)),
   ("a.digest", decide (a.proposalDigest = c.proposalDigest a.proposal e.contract)),
   ("a.proposal", decide (lookup a.actionId c.proposals = some a.proposal)), ("a.policy", decide (a.policyDigest = c.policyDigest)),
   ("a.human", decide (a.human ∈ c.humans)), ("a.notRevoked", decide (a.actionId ∉ c.revokedActions)),
   ("a.occ≤from", decide (e.occurred ≤ a.validFrom)), ("a.from≤now", decide (a.validFrom ≤ c.now)),
   ("a.now<until", decide (c.now < a.validUntil)), ("a.until≤expires", decide (a.validUntil ≤ a.proposal.expires)),
   ("a.target", decide (a.proposal.target ∈ c.sandboxTargets)), ("a.budget≤max", decide (a.proposal.budget.value.coefficient ≤ c.maxSteps)),
   ("a.budgetValid", decide (a.proposal.budget.value.ValidAt 0)), ("a.stepUnit", decide (a.proposal.budget.unit = .step)),
   ("a.maxEffects", decide (a.maxEffects = 1)), ("a.domainLit", decide (a.authorityDomain = "urn:mpe:sandbox:local")),
   ("a.windowLit", decide (a.budgetWindow = "window:fixture"))]

def conj (c : Context) (e : Event) : List (String × Bool) :=
  commonConj c e ++ match e.payload with
  | .rfq q => rfqConj c e.envelope q | .invoice i => invConj c e.envelope i | .agent a => agConj c e.envelope a


def cases : List (String × Context × Event) := [
  ("fixture_rfq", context0, event0),
  ("fixture_agent", context1, event1),
  ("fixture_invoice-final", context2, event2),
  ("fixture_invoice-pending", context3, event3),
  ("fixture_invoice-reversed", context4, event4),
  ("corpus_side", context5, event5),
  ("corpus_cash", context6, event6),
  ("corpus_expired", context7, event7),
  ("corpus_expired-approval", context8, event8),
  ("corpus_price-asset", context9, event9),
  ("corpus_payment-final-invention", context10, event10),
  ("corpus_missing-payment-evidence", context11, event11),
  ("corpus_unauthorized-human", context12, event12),
  ("corpus_changed-target", context13, event13),
  ("corpus_changed-input", context14, event14),
  ("corpus_profile-hash", context15, event15),
  ("corpus_unknown-profile", context16, event16),
  ("context_no-trust", context17, event17),
  ("context_revoked", context18, event18),
  ("context_low-budget", context19, event19),
  ("context_no-role", context20, event20),
  ("context_wrong-principal", context21, event21),
  ("context_no-proposal", context22, event22),
  ("context_unknown-target", context23, event23),
  ("context_wrong-policy", context24, event24),
  ("quote_at_validFrom", context25, event25),
  ("quote_at_validUntil", context26, event26),
  ("approval_at_validFrom", context27, event27),
  ("approval_at_validUntil", context28, event28),
  ("sell_side", context29, event29),
  ("cash_overflow", context30, event30),
  ("rehashed_changed_proposal", context31, event31),
  ("observation_after_occurrence", context32, event32),
  ("complete_evidence_overpayment", context33, event33),
  ("future_occurrence", context34, event34),
  ("closed_rfq", context35, event35)]

#eval do
  let mut killedAlone : List String := []
  let mut failedEver : List String := []
  for (n, c, e) in cases do
    let fails : List String := ((conj c e).filter (fun (p : String × Bool) => !p.2)).map (fun (p : String × Bool) => p.1)
    let v : Option Verdict := (validate c e).map Result.verdict
    IO.println s!"{n}: validate={repr v} failing={fails}"
    if fails.length == 1 then killedAlone := fails ++ killedAlone
    failedEver := fails ++ failedEver
  IO.println s!"ALONE: {killedAlone.eraseDups}"
  IO.println s!"EVER: {failedEver.eraseDups}"
