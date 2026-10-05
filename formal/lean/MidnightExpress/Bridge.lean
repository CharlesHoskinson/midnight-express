import MidnightExpress.Validation
namespace MidnightExpress.Bridge

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


def failingConditions (c : Context) (e : Event) : List String :=
  ((conj c e).filter (fun p => !p.2)).map Prod.fst

theorem decodeProfile_eq_name (s : String) (p : Profile) :
    decodeProfile s = some p ↔ s = p.name := by
  by_cases h₁ : s = "rfq.v0.2"
  · subst s; cases p <;> decide
  · by_cases h₂ : s = "invoice.v0.2"
    · subst s; cases p <;> decide
    · by_cases h₃ : s = "agent.v0.2"
      · subst s; cases p <;> decide
      · cases p <;> simp [decodeProfile, Profile.name, h₁, h₂, h₃]

theorem commonConj_iff (c : Context) (e : Event) :
    (commonConj c e).all Prod.snd = true ↔ commonCheck c e = true := by
  cases hs : lookup e.envelope.source c.sources with
  | none => simp [commonConj, commonCheck, hs]
  | some a =>
    rcases a with ⟨role, principal⟩
    simp [commonConj, commonCheck, hs, dispatch_iff_exact_envelope, Envelope.Matches,
      decodeProfile_eq_name, and_assoc, and_left_comm, and_comm]

theorem rfqConj_iff (c : Context) (e : Envelope) (q : RFQ) :
    (rfqConj c e q).all Prod.snd = true ↔ rfqCheck c e q = true := by
  simp [rfqConj, rfqCheck, and_assoc]

theorem invConj_iff (c : Context) (e : Envelope) (i : Invoice) :
    (invConj c e i).all Prod.snd = true ↔ invoiceCheck c e i = true := by
  simp [invConj, invoiceCheck, and_assoc]

theorem agConj_iff (c : Context) (e : Envelope) (a : Approval) :
    (agConj c e a).all Prod.snd = true ↔ approvalCheck c e a = true := by
  simp [agConj, approvalCheck, and_assoc]

theorem conj_iff (c : Context) (e : Event) :
    (conj c e).all Prod.snd = true ↔ (commonCheck c e && semanticCheck c e) = true := by
  cases hp : e.payload <;>
    simp only [conj, List.all_append, Bool.and_eq_true, commonConj_iff, hp,
      semanticCheck, rfqConj_iff, invConj_iff, agConj_iff]

end MidnightExpress.Bridge
