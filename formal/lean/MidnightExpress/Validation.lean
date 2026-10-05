import MidnightExpress.Model

namespace MidnightExpress

/-- Verdicts describe modeled observations; none grants an execution capability. -/
inductive Verdict where
  | quote | paymentFinal | paymentOther | candidate | duplicateEvent | duplicateAction
  deriving Repr, BEq, DecidableEq

structure Result where
  verdict : Verdict
  executes : Bool
  deriving Repr, BEq, DecidableEq

def observation (v : Verdict) : Result := ⟨v, false⟩

/-- Trusted, sequential fixture memory. Digests are opaque equality tokens here. -/
structure ReplayState where
  events : List ((String × String) × String) := []
  actions : List ((String × String × String) × String) := []
  deriving Repr, BEq, DecidableEq

def lookup [DecidableEq α] (key : α) : List (α × β) → Option β
  | [] => none
  | (k, v) :: rest => if key = k then some v else lookup key rest

/-- Occurrence identity has precedence over logical-action identity. This is called
only after current-context validation; it never reauthorizes stale input. -/
def replay (s : ReplayState) (eventKey : String × String) (eventDigest : String)
    (action : Option (String × String × String)) (intentDigest : String)
    (fresh : Verdict) : Option (Result × ReplayState) :=
  match lookup eventKey s.events with
  | some old => if old = eventDigest then some (observation .duplicateEvent, s) else none
  | none =>
    let events := (eventKey, eventDigest) :: s.events
    match action with
    | none => some (observation fresh, { s with events })
    | some key =>
      match lookup key s.actions with
      | some old => if old = intentDigest then
          some (observation .duplicateAction, { s with events }) else none
      | none => some (observation fresh, { events, actions := (key, intentDigest) :: s.actions })

theorem occurrence_conflict_rejected (s : ReplayState) (key : String × String)
    (old changed : String) (action : Option (String × String × String))
    (intent : String) (v : Verdict) (h : lookup key s.events = some old)
    (different : old ≠ changed) : replay s key changed action intent v = none := by
  simp [replay, h, different]

theorem identical_occurrence_duplicate (s : ReplayState) (key : String × String)
    (digest : String) (action : Option (String × String × String))
    (intent : String) (v : Verdict) (h : lookup key s.events = some digest) :
    replay s key digest action intent v = some (observation .duplicateEvent, s) := by
  simp [replay, h]

theorem action_conflict_rejected (s : ReplayState) (eventKey : String × String)
    (actionKey : String × String × String) (eventDigest old changed : String)
    (v : Verdict) (newOccurrence : lookup eventKey s.events = none)
    (knownAction : lookup actionKey s.actions = some old) (different : old ≠ changed) :
    replay s eventKey eventDigest (some actionKey) changed v = none := by
  simp [replay, newOccurrence, knownAction, different]

theorem same_action_new_occurrence_duplicate (s : ReplayState)
    (eventKey : String × String) (actionKey : String × String × String)
    (eventDigest intent : String) (v : Verdict)
    (newOccurrence : lookup eventKey s.events = none)
    (knownAction : lookup actionKey s.actions = some intent) :
    replay s eventKey eventDigest (some actionKey) intent v =
      some (observation .duplicateAction,
        { s with events := (eventKey, eventDigest) :: s.events }) := by
  simp [replay, newOccurrence, knownAction]



structure SourceAuthority where
  role : Role
  principal : String
  deriving Repr, BEq, DecidableEq

structure Context where
  trusted : Bool
  now : Int
  sources : List (String × SourceAuthority)
  rfqs : List (String × (Bool × RFQTerms))
  invoices : List (String × InvoiceTerms)
  paymentEvidence : List (String × Invoice)
  authorityDomain : String
  executionScope : String
  budgetWindow : String
  proposals : List (String × Proposal)
  policyDigest : String
  humans : List String
  revokedActions : List String
  sandboxTargets : List String
  maxSteps : Nat
  /-- Externally supplied commitment function; no cryptographic assertion. -/
  proposalDigest : Proposal → String → String

/-- Explicit semantic specification, separate from executable Boolean gates. -/
structure CommonValid (c : Context) (e : Event) : Prop where
  trustedContext : c.trusted = true
  exactDispatch : dispatch e.envelope = some e.payload.profile
  notFuture : e.envelope.occurred ≤ c.now
  sourceAuthority : lookup e.envelope.source c.sources =
    some ⟨e.payload.profile.role, e.payload.principal⟩

def commonCheck (c : Context) (e : Event) : Bool :=
  c.trusted && decide (dispatch e.envelope = some e.payload.profile) &&
  decide (e.envelope.occurred ≤ c.now) &&
  decide (lookup e.envelope.source c.sources =
    some (SourceAuthority.mk e.payload.profile.role e.payload.principal))

theorem commonCheck_iff (c : Context) (e : Event) :
    commonCheck c e = true ↔ CommonValid c e := by
  simp only [commonCheck, Bool.and_eq_true, decide_eq_true_eq, and_assoc]
  constructor
  · rintro ⟨h0, h1, h2, h3⟩
    exact ⟨h0, h1, h2, h3⟩
  · intro h
    exact ⟨h.trustedContext, h.exactDispatch, h.notFuture, h.sourceAuthority⟩

structure RFQValid (c : Context) (e : Envelope) (q : RFQ) : Prop where
  openTerms : lookup q.rfqId c.rfqs = some (true, q.terms)
  buyerRole : q.buyer = q.expectedBuyer
  sellerRole : q.seller = q.expectedSeller
  distinctParties : q.buyer ≠ q.seller
  priceAsset : q.price.assetRef = q.terms.asset
  priceUnit : q.price.unit = q.terms.quantity.unit
  priceCurrency : q.price.currency = q.terms.currency
  baseQuantity : q.price.baseQuantity = 1
  shareQuantity : q.terms.quantity.unit = .share
  quantityDecimal : q.terms.quantity.value.ValidAt 0
  priceDecimal : q.price.value.ValidAt 2
  cashDecimal : q.cash.ValidAt 2
  occurredLeFrom : e.occurred ≤ q.validFrom
  fromLeNow : q.validFrom ≤ c.now
  nowLtUntil : c.now < q.validUntil
  cashProduct : q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient

def rfqCheck (c : Context) (e : Envelope) (q : RFQ) : Bool :=
  decide (lookup q.rfqId c.rfqs = some (true, q.terms)) &&
  decide (q.buyer = q.expectedBuyer) && decide (q.seller = q.expectedSeller) &&
  decide (q.buyer ≠ q.seller) && decide (q.price.assetRef = q.terms.asset) &&
  decide (q.price.unit = q.terms.quantity.unit) && decide (q.price.currency = q.terms.currency) &&
  decide (q.price.baseQuantity = 1) && decide (q.terms.quantity.unit = .share) &&
  decide (q.terms.quantity.value.ValidAt 0) && decide (q.price.value.ValidAt 2) &&
  decide (q.cash.ValidAt 2) && decide (e.occurred ≤ q.validFrom) &&
  decide (q.validFrom ≤ c.now) && decide (c.now < q.validUntil) &&
  decide (q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient)

theorem rfqCheck_iff (c : Context) (e : Envelope) (q : RFQ) :
    rfqCheck c e q = true ↔ RFQValid c e q := by
  simp only [rfqCheck, Bool.and_eq_true, decide_eq_true_eq, and_assoc]
  constructor
  · rintro ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15⟩
    exact ⟨h0, h1, h2, h3, h4, h5, by cases q.price.currency; cases q.terms.currency; rfl, h7, h8, h9,
      h10, h11, h12, h13, h14, h15⟩
  · intro h
    exact ⟨h.openTerms, h.buyerRole, h.sellerRole, h.distinctParties, h.priceAsset, h.priceUnit,
      True.intro, h.baseQuantity, h.shareQuantity, h.quantityDecimal, h.priceDecimal, h.cashDecimal,
      h.occurredLeFrom, h.fromLeNow, h.nowLtUntil, h.cashProduct⟩

structure InvoiceValid (c : Context) (e : Envelope) (i : Invoice) : Prop where
  trustedTerms : lookup i.invoiceId c.invoices = some i.terms
  completeEvidence : lookup i.paymentId c.paymentEvidence = some i
  effectiveLeObserved : i.effectiveAt ≤ i.observedAt
  observedLeOccurred : i.observedAt ≤ e.occurred
  amountBounded : i.amount.coefficient ≤ i.terms.payable.coefficient
  amountDecimal : i.amount.ValidAt 2
  payableDecimal : i.terms.payable.ValidAt 2
  fixtureRail : i.rail = "fixture-bank-v1"

def invoiceCheck (c : Context) (e : Envelope) (i : Invoice) : Bool :=
  decide (lookup i.invoiceId c.invoices = some i.terms) &&
  decide (lookup i.paymentId c.paymentEvidence = some i) &&
  decide (i.effectiveAt ≤ i.observedAt) && decide (i.observedAt ≤ e.occurred) &&
  decide (i.amount.coefficient ≤ i.terms.payable.coefficient) &&
  decide (i.amount.ValidAt 2) && decide (i.terms.payable.ValidAt 2) &&
  decide (i.rail = "fixture-bank-v1")

theorem invoiceCheck_iff (c : Context) (e : Envelope) (i : Invoice) :
    invoiceCheck c e i = true ↔ InvoiceValid c e i := by
  simp only [invoiceCheck, Bool.and_eq_true, decide_eq_true_eq, and_assoc]
  constructor
  · rintro ⟨h0, h1, h2, h3, h4, h5, h6, h7⟩
    exact ⟨h0, h1, h2, h3, h4, h5, h6, h7⟩
  · intro h
    exact ⟨h.trustedTerms, h.completeEvidence, h.effectiveLeObserved, h.observedLeOccurred,
      h.amountBounded, h.amountDecimal, h.payableDecimal, h.fixtureRail⟩

structure ApprovalValid (c : Context) (e : Envelope) (a : Approval) : Prop where
  authorityDomain : a.authorityDomain = c.authorityDomain
  executionScope : a.executionScope = c.executionScope
  budgetWindow : a.budgetWindow = c.budgetWindow
  proposalCommitment : a.proposalDigest = c.proposalDigest a.proposal e.contract
  currentProposal : lookup a.actionId c.proposals = some a.proposal
  currentPolicy : a.policyDigest = c.policyDigest
  authorizedHuman : a.human ∈ c.humans
  notRevoked : a.actionId ∉ c.revokedActions
  occurredLeFrom : e.occurred ≤ a.validFrom
  fromLeNow : a.validFrom ≤ c.now
  nowLtUntil : c.now < a.validUntil
  untilLeExpires : a.validUntil ≤ a.proposal.expires
  permittedTarget : a.proposal.target ∈ c.sandboxTargets
  stepBound : a.proposal.budget.value.coefficient ≤ c.maxSteps
  budgetDecimal : a.proposal.budget.value.ValidAt 0
  stepUnit : a.proposal.budget.unit = .step
  oneEffect : a.maxEffects = 1
  fixtureDomain : a.authorityDomain = "urn:mpe:sandbox:local"
  fixtureWindow : a.budgetWindow = "window:fixture"

def approvalCheck (c : Context) (e : Envelope) (a : Approval) : Bool :=
  decide (a.authorityDomain = c.authorityDomain) && decide (a.executionScope = c.executionScope) &&
  decide (a.budgetWindow = c.budgetWindow) &&
  decide (a.proposalDigest = c.proposalDigest a.proposal e.contract) &&
  decide (lookup a.actionId c.proposals = some a.proposal) && decide (a.policyDigest = c.policyDigest) &&
  decide (a.human ∈ c.humans) && decide (a.actionId ∉ c.revokedActions) &&
  decide (e.occurred ≤ a.validFrom) && decide (a.validFrom ≤ c.now) &&
  decide (c.now < a.validUntil) && decide (a.validUntil ≤ a.proposal.expires) &&
  decide (a.proposal.target ∈ c.sandboxTargets) &&
  decide (a.proposal.budget.value.coefficient ≤ c.maxSteps) &&
  decide (a.proposal.budget.value.ValidAt 0) && decide (a.proposal.budget.unit = .step) &&
  decide (a.maxEffects = 1) && decide (a.authorityDomain = "urn:mpe:sandbox:local") &&
  decide (a.budgetWindow = "window:fixture")

theorem approvalCheck_iff (c : Context) (e : Envelope) (a : Approval) :
    approvalCheck c e a = true ↔ ApprovalValid c e a := by
  simp only [approvalCheck, Bool.and_eq_true, decide_eq_true_eq, and_assoc]
  constructor
  · rintro ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18⟩
    exact ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18⟩
  · intro h
    exact ⟨h.authorityDomain, h.executionScope, h.budgetWindow, h.proposalCommitment, h.currentProposal,
      h.currentPolicy, h.authorizedHuman, h.notRevoked, h.occurredLeFrom, h.fromLeNow, h.nowLtUntil,
      h.untilLeExpires, h.permittedTarget, h.stepBound, h.budgetDecimal, h.stepUnit, h.oneEffect,
      h.fixtureDomain, h.fixtureWindow⟩

def semanticCheck (c : Context) (e : Event) : Bool :=
  match e.payload with
  | .rfq q => rfqCheck c e.envelope q
  | .invoice i => invoiceCheck c e.envelope i
  | .agent a => approvalCheck c e.envelope a

def SemanticValid (c : Context) (e : Event) : Prop :=
  match e.payload with
  | .rfq q => RFQValid c e.envelope q
  | .invoice i => InvoiceValid c e.envelope i
  | .agent a => ApprovalValid c e.envelope a

def payloadVerdict : Payload → Verdict
  | .rfq _ => .quote
  | .invoice i => if i.status = .final then .paymentFinal else .paymentOther
  | .agent _ => .candidate

def validate (c : Context) (e : Event) : Option Result :=
  if commonCheck c e && semanticCheck c e then
    some (observation (payloadVerdict e.payload)) else none

theorem semanticCheck_iff (c : Context) (e : Event) :
    semanticCheck c e = true ↔ SemanticValid c e := by
  cases hp : e.payload <;> simp [semanticCheck, SemanticValid, hp, rfqCheck_iff,
    invoiceCheck_iff, approvalCheck_iff]

theorem validation_sound (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : CommonValid c e ∧ SemanticValid c e := by
  unfold validate at h
  split at h
  · rename_i gate
    have gates : commonCheck c e = true ∧ semanticCheck c e = true := by simpa using gate
    exact ⟨(commonCheck_iff c e).mp gates.1, (semanticCheck_iff c e).mp gates.2⟩
  · contradiction

theorem validation_complete (c : Context) (e : Event)
    (hc : CommonValid c e) (hs : SemanticValid c e) :
    validate c e = some (observation (payloadVerdict e.payload)) := by
  simp [validate, (commonCheck_iff c e).mpr hc, (semanticCheck_iff c e).mpr hs]

theorem acceptance_never_executes (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : r.executes = false := by
  unfold validate at h
  split at h
  · cases Option.some.inj h
    rfl
  · contradiction

theorem accepted_occurrence_not_future (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : e.envelope.occurred ≤ c.now :=
  (validation_sound c e r h).1.notFuture

theorem accepted_source_role_principal (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : lookup e.envelope.source c.sources =
      some ⟨e.payload.profile.role, e.payload.principal⟩ :=
  (validation_sound c e r h).1.sourceAuthority

theorem accepted_quote_cash (c : Context) (e : Envelope) (q : RFQ) (r : Result)
    (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  exact hs.cashProduct

theorem accepted_invoice_complete_evidence (c : Context) (e : Envelope) (i : Invoice)
    (r : Result) (h : validate c ⟨e, .invoice i⟩ = some r) :
    lookup i.paymentId c.paymentEvidence = some i :=
  (validation_sound c ⟨e, .invoice i⟩ r h).2.completeEvidence

theorem accepted_approval_current_policy (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    lookup a.actionId c.proposals = some a.proposal ∧ a.policyDigest = c.policyDigest := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.currentProposal, hs.currentPolicy⟩

theorem accepted_approval_not_revoked (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    a.actionId ∉ c.revokedActions :=
  (validation_sound c ⟨e, .agent a⟩ r h).2.notRevoked

theorem accepted_approval_unexpired (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    c.now < a.validUntil ∧ a.validUntil ≤ a.proposal.expires := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.nowLtUntil, hs.untilLeExpires⟩

/-- Stateful classification always rechecks the current context first. -/
def check (c : Context) (s : ReplayState) (e : Event)
    (eventDigest intentDigest : String) : Option (Result × ReplayState) :=
  match validate c e with
  | none => none
  | some r => replay s e.occurrenceKey eventDigest
      (match e.payload with
       | .agent a => some (a.authorityDomain, a.executionScope, a.actionId)
       | _ => none) intentDigest r.verdict

theorem invalid_now_cannot_replay (c : Context) (s : ReplayState) (e : Event)
    (eventDigest intentDigest : String) (h : validate c e = none) :
    check c s e eventDigest intentDigest = none := by
  simp [check, h]

theorem accepted_quote_half_open (c : Context) (e : Envelope) (q : RFQ) (r : Result)
    (h : validate c ⟨e, .rfq q⟩ = some r) :
    e.occurred ≤ q.validFrom ∧ q.validFrom ≤ c.now ∧ c.now < q.validUntil := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  exact ⟨hs.occurredLeFrom,
    hs.fromLeNow, hs.nowLtUntil⟩

theorem accepted_quote_exact_decimal_product (c : Context) (e : Envelope)
    (q : RFQ) (r : Result) (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.cash = q.terms.quantity.value.product q.price.value := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  have quantityScale := hs.quantityDecimal.2.2
  have priceScale := hs.priceDecimal.2.2
  have cashScale := hs.cashDecimal.2.2
  have coefficient := accepted_quote_cash c e q r h
  cases hc : q.cash with
  | mk coeff scale =>
    simp only [hc, Decimal.mk.injEq, Decimal.product] at *
    exact ⟨coefficient, by omega⟩

/-- Cross multiplication states equality of the exact rational values, with no rounding. -/
theorem accepted_quote_rational_cash (c : Context) (e : Envelope) (q : RFQ)
    (r : Result) (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.cash.coefficient *
      (q.terms.quantity.value.denominator * q.price.value.denominator) =
    (q.terms.quantity.value.coefficient * q.price.value.coefficient) * q.cash.denominator := by
  rw [accepted_quote_exact_decimal_product c e q r h, product_denominator]
  rfl

theorem accepted_approval_bounded (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    a.proposal.target ∈ c.sandboxTargets ∧
    a.proposal.budget.value.coefficient ≤ c.maxSteps ∧ a.maxEffects = 1 := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.permittedTarget,
    hs.stepBound, hs.oneEffect⟩

theorem replay_never_executes (s s' : ReplayState) (key : String × String)
    (eventDigest intent : String) (action : Option (String × String × String))
    (v : Verdict) (r : Result) (h : replay s key eventDigest action intent v = some (r, s')) :
    r.executes = false := by
  unfold replay at h
  split at h
  · split at h
    · cases h; rfl
    · contradiction
  · split at h
    · cases h; rfl
    · split at h
      · split at h
        · cases h; rfl
        · contradiction
      · cases h; rfl

theorem stateful_check_never_executes (c : Context) (s s' : ReplayState)
    (e : Event) (eventDigest intent : String) (r : Result)
    (h : check c s e eventDigest intent = some (r, s')) : r.executes = false := by
  unfold check at h
  split at h
  · contradiction
  · exact replay_never_executes _ _ _ _ _ _ _ _ h

theorem accepted_quote_units_and_roles (c : Context) (e : Envelope) (q : RFQ)
    (r : Result) (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.buyer = q.expectedBuyer ∧ q.seller = q.expectedSeller ∧ q.buyer ≠ q.seller ∧
    q.price.assetRef = q.terms.asset ∧ q.price.unit = q.terms.quantity.unit ∧
    q.price.currency = q.terms.currency := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  exact ⟨hs.buyerRole, hs.sellerRole, hs.distinctParties, hs.priceAsset,
    hs.priceUnit, hs.priceCurrency⟩

theorem expired_quote_rejected (c : Context) (e : Envelope) (q : RFQ)
    (expired : q.validUntil ≤ c.now) : validate c ⟨e, .rfq q⟩ = none := by
  cases result : validate c ⟨e, .rfq q⟩ with
  | none => rfl
  | some r =>
    have bounds := accepted_quote_half_open c e q r result
    omega

theorem revoked_approval_rejected (c : Context) (e : Envelope) (a : Approval)
    (revoked : a.actionId ∈ c.revokedActions) : validate c ⟨e, .agent a⟩ = none := by
  cases result : validate c ⟨e, .agent a⟩ with
  | none => rfl
  | some r => exact False.elim (accepted_approval_not_revoked c e a r result revoked)

theorem unknown_profile_validation_rejected (c : Context) (e : Event)
    (unknown : decodeProfile e.envelope.profile = none) : validate c e = none := by
  simp [validate, commonCheck, dispatch, unknown]

theorem final_verdict_requires_final_record (c : Context) (e : Envelope) (i : Invoice)
    (h : validate c ⟨e, .invoice i⟩ = some (observation .paymentFinal)) :
    i.status = .final ∧ lookup i.paymentId c.paymentEvidence = some i := by
  refine ⟨?_, accepted_invoice_complete_evidence c e i _ h⟩
  unfold validate at h
  split at h
  · simp only [payloadVerdict] at h
    split at h
    · assumption
    · cases h
  · contradiction

/-- The exact rejection characterization complements soundness and completeness. -/
theorem validation_rejected_iff (c : Context) (e : Event) :
    validate c e = none ↔ ¬ (CommonValid c e ∧ SemanticValid c e) := by
  constructor
  · intro rejected valid
    have accepted := validation_complete c e valid.1 valid.2
    rw [rejected] at accepted
    contradiction
  · intro invalid
    cases result : validate c e with
    | none => rfl
    | some r => exact False.elim (invalid (validation_sound c e r result))

theorem expired_approval_rejected (c : Context) (e : Envelope) (a : Approval)
    (expired : a.validUntil ≤ c.now) : validate c ⟨e, .agent a⟩ = none := by
  cases result : validate c ⟨e, .agent a⟩ with
  | none => rfl
  | some r =>
    have bounds := accepted_approval_unexpired c e a r result
    omega

theorem stale_policy_approval_rejected (c : Context) (e : Envelope) (a : Approval)
    (changed : a.policyDigest ≠ c.policyDigest) : validate c ⟨e, .agent a⟩ = none := by
  cases result : validate c ⟨e, .agent a⟩ with
  | none => rfl
  | some r => exact False.elim (changed (accepted_approval_current_policy c e a r result).2)

theorem accepted_invoice_clocks_and_amount (c : Context) (e : Envelope) (i : Invoice)
    (r : Result) (h : validate c ⟨e, .invoice i⟩ = some r) :
    i.effectiveAt ≤ i.observedAt ∧ i.observedAt ≤ e.occurred ∧
    i.amount.coefficient ≤ i.terms.payable.coefficient := by
  have hs := (validation_sound c ⟨e, .invoice i⟩ r h).2
  exact ⟨hs.effectiveLeObserved, hs.observedLeOccurred, hs.amountBounded⟩

theorem accepted_approval_authority (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    a.authorityDomain = c.authorityDomain ∧ a.executionScope = c.executionScope ∧
    a.budgetWindow = c.budgetWindow ∧ a.human ∈ c.humans := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.authorityDomain, hs.executionScope, hs.budgetWindow, hs.authorizedHuman⟩

/-- Removes permissions, adds revocations, and lowers a budget at a fixed clock,
policy and trusted-record snapshot. Freshness changes have separate rejection laws. -/
def narrowAuthority (c : Context) (humans targets revoked : List String) (steps : Nat) : Context :=
  { c with humans := humans, sandboxTargets := targets, revokedActions := revoked, maxSteps := steps }

/-- Acceptance in a narrowed authority context implies acceptance in the original
context. The converse is deliberately unnecessary: removed permission cannot grant it. -/
theorem authority_narrowing_preserves_validity (c : Context) (e : Event)
    (humans targets revoked : List String) (steps : Nat)
    (humanSubset : ∀ x, x ∈ humans → x ∈ c.humans)
    (targetSubset : ∀ x, x ∈ targets → x ∈ c.sandboxTargets)
    (revokedSuperset : ∀ x, x ∈ c.revokedActions → x ∈ revoked)
    (stepBound : steps ≤ c.maxSteps)
    (valid : CommonValid (narrowAuthority c humans targets revoked steps) e ∧
      SemanticValid (narrowAuthority c humans targets revoked steps) e) :
    CommonValid c e ∧ SemanticValid c e := by
  refine ⟨⟨valid.1.trustedContext, valid.1.exactDispatch, valid.1.notFuture, valid.1.sourceAuthority⟩, ?_⟩
  cases hp : e.payload with
  | rfq q =>
    have h : RFQValid (narrowAuthority c humans targets revoked steps) e.envelope q := by
      simpa [SemanticValid, hp] using valid.2
    simp only [SemanticValid, hp]
    exact ⟨h.openTerms, h.buyerRole, h.sellerRole, h.distinctParties, h.priceAsset, h.priceUnit,
      h.priceCurrency, h.baseQuantity, h.shareQuantity, h.quantityDecimal, h.priceDecimal, h.cashDecimal,
      h.occurredLeFrom, h.fromLeNow, h.nowLtUntil, h.cashProduct⟩
  | invoice i =>
    have h : InvoiceValid (narrowAuthority c humans targets revoked steps) e.envelope i := by
      simpa [SemanticValid, hp] using valid.2
    simp only [SemanticValid, hp]
    exact ⟨h.trustedTerms, h.completeEvidence, h.effectiveLeObserved, h.observedLeOccurred,
      h.amountBounded, h.amountDecimal, h.payableDecimal, h.fixtureRail⟩
  | agent a =>
    have h : ApprovalValid (narrowAuthority c humans targets revoked steps) e.envelope a := by
      simpa [SemanticValid, hp] using valid.2
    simp only [SemanticValid, hp]
    exact {
      authorityDomain := h.authorityDomain, executionScope := h.executionScope,
      budgetWindow := h.budgetWindow, proposalCommitment := h.proposalCommitment,
      currentProposal := h.currentProposal, currentPolicy := h.currentPolicy,
      authorizedHuman := humanSubset _ h.authorizedHuman,
      notRevoked := fun revoked => h.notRevoked (revokedSuperset _ revoked),
      occurredLeFrom := h.occurredLeFrom, fromLeNow := h.fromLeNow,
      nowLtUntil := h.nowLtUntil, untilLeExpires := h.untilLeExpires,
      permittedTarget := targetSubset _ h.permittedTarget,
      stepBound := Nat.le_trans h.stepBound stepBound,
      budgetDecimal := h.budgetDecimal, stepUnit := h.stepUnit,
      oneEffect := h.oneEffect, fixtureDomain := h.fixtureDomain,
      fixtureWindow := h.fixtureWindow }

theorem authority_narrowing_cannot_reauthorize (c : Context) (e : Event)
    (humans targets revoked : List String) (steps : Nat)
    (humanSubset : ∀ x, x ∈ humans → x ∈ c.humans)
    (targetSubset : ∀ x, x ∈ targets → x ∈ c.sandboxTargets)
    (revokedSuperset : ∀ x, x ∈ c.revokedActions → x ∈ revoked)
    (stepBound : steps ≤ c.maxSteps) (rejected : validate c e = none) :
    validate (narrowAuthority c humans targets revoked steps) e = none := by
  apply (validation_rejected_iff _ _).mpr
  intro valid
  exact (validation_rejected_iff c e).mp rejected
    (authority_narrowing_preserves_validity c e humans targets revoked steps
      humanSubset targetSubset revokedSuperset stepBound valid)

/-- Authority maps are unambiguous. This is an explicit fixture quality predicate,
not an unproved assertion that external records have unique keys. The executable
validator retains its documented first-match lookup semantics for every context. -/
structure Context.WellFormed (c : Context) : Prop where
  sourceKeys : (c.sources.map Prod.fst).Nodup
  rfqKeys : (c.rfqs.map Prod.fst).Nodup
  invoiceKeys : (c.invoices.map Prod.fst).Nodup
  paymentKeys : (c.paymentEvidence.map Prod.fst).Nodup
  proposalKeys : (c.proposals.map Prod.fst).Nodup


/-- Unique-key authority maps make membership agree with executable lookup. -/
theorem lookup_of_mem_unique [DecidableEq α] (entries : List (α × β))
    (key : α) (value : β) (unique : (entries.map Prod.fst).Nodup)
    (member : (key, value) ∈ entries) : lookup key entries = some value := by
  induction entries with
  | nil => simp at member
  | cons head tail ih =>
    rcases head with ⟨headKey, headValue⟩
    simp only [List.map_cons, List.nodup_cons] at unique
    simp only [List.mem_cons] at member
    rcases member with same | inTail
    · cases same
      simp [lookup]
    · by_cases equal : key = headKey
      · have tailKey : headKey ∈ tail.map Prod.fst := by
          exact List.mem_map.mpr ⟨(key, value), inTail, equal⟩
        exact False.elim (unique.1 tailKey)
      · simp [lookup, equal, ih unique.2 inTail]

end MidnightExpress
