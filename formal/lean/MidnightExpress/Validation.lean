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
def CommonValid (c : Context) (e : Event) : Prop :=
  c.trusted = true ∧ dispatch e.envelope = some e.payload.profile ∧
  e.envelope.occurred ≤ c.now ∧
  lookup e.envelope.source c.sources =
    some ⟨e.payload.profile.role, e.payload.principal⟩

def commonCheck (c : Context) (e : Event) : Bool :=
  c.trusted && decide (dispatch e.envelope = some e.payload.profile) &&
  decide (e.envelope.occurred ≤ c.now) &&
  decide (lookup e.envelope.source c.sources =
    some (SourceAuthority.mk e.payload.profile.role e.payload.principal))

theorem commonCheck_iff (c : Context) (e : Event) :
    commonCheck c e = true ↔ CommonValid c e := by
  simp [commonCheck, CommonValid, and_assoc]

def RFQValid (c : Context) (e : Envelope) (q : RFQ) : Prop :=
  lookup q.rfqId c.rfqs = some (true, q.terms) ∧
  q.buyer = q.expectedBuyer ∧ q.seller = q.expectedSeller ∧ q.buyer ≠ q.seller ∧
  q.price.assetRef = q.terms.asset ∧ q.price.unit = q.terms.quantity.unit ∧
  q.price.currency = q.terms.currency ∧ q.price.baseQuantity = 1 ∧
  q.terms.quantity.unit = .share ∧
  q.terms.quantity.value.ValidAt 0 ∧ q.price.value.ValidAt 2 ∧ q.cash.ValidAt 2 ∧
  e.occurred ≤ q.validFrom ∧ q.validFrom ≤ c.now ∧ c.now < q.validUntil ∧
  q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient

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
  simp [rfqCheck, RFQValid, and_assoc]

def InvoiceValid (c : Context) (e : Envelope) (i : Invoice) : Prop :=
  lookup i.invoiceId c.invoices = some i.terms ∧
  lookup i.paymentId c.paymentEvidence = some i ∧
  i.effectiveAt ≤ i.observedAt ∧ i.observedAt ≤ e.occurred ∧
  i.amount.coefficient ≤ i.terms.payable.coefficient ∧
  i.amount.ValidAt 2 ∧ i.terms.payable.ValidAt 2 ∧ i.rail = "fixture-bank-v1"

def invoiceCheck (c : Context) (e : Envelope) (i : Invoice) : Bool :=
  decide (lookup i.invoiceId c.invoices = some i.terms) &&
  decide (lookup i.paymentId c.paymentEvidence = some i) &&
  decide (i.effectiveAt ≤ i.observedAt) && decide (i.observedAt ≤ e.occurred) &&
  decide (i.amount.coefficient ≤ i.terms.payable.coefficient) &&
  decide (i.amount.ValidAt 2) && decide (i.terms.payable.ValidAt 2) &&
  decide (i.rail = "fixture-bank-v1")

theorem invoiceCheck_iff (c : Context) (e : Envelope) (i : Invoice) :
    invoiceCheck c e i = true ↔ InvoiceValid c e i := by
  simp [invoiceCheck, InvoiceValid, and_assoc]

def ApprovalValid (c : Context) (e : Envelope) (a : Approval) : Prop :=
  a.authorityDomain = c.authorityDomain ∧ a.executionScope = c.executionScope ∧
  a.budgetWindow = c.budgetWindow ∧
  a.proposalDigest = c.proposalDigest a.proposal e.contract ∧
  lookup a.actionId c.proposals = some a.proposal ∧ a.policyDigest = c.policyDigest ∧
  a.human ∈ c.humans ∧ a.actionId ∉ c.revokedActions ∧
  e.occurred ≤ a.validFrom ∧ a.validFrom ≤ c.now ∧ c.now < a.validUntil ∧
  a.validUntil ≤ a.proposal.expires ∧ a.proposal.target ∈ c.sandboxTargets ∧
  a.proposal.budget.value.coefficient ≤ c.maxSteps ∧
  a.proposal.budget.value.ValidAt 0 ∧ a.proposal.budget.unit = .step ∧ a.maxEffects = 1 ∧
  a.authorityDomain = "urn:mpe:sandbox:local" ∧ a.budgetWindow = "window:fixture"

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
  simp [approvalCheck, ApprovalValid, and_assoc]

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
  (validation_sound c e r h).1.2.2.1

theorem accepted_source_role_principal (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : lookup e.envelope.source c.sources =
      some ⟨e.payload.profile.role, e.payload.principal⟩ :=
  (validation_sound c e r h).1.2.2.2

theorem accepted_quote_cash (c : Context) (e : Envelope) (q : RFQ) (r : Result)
    (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.cash.coefficient = q.terms.quantity.value.coefficient * q.price.value.coefficient := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  simp only [SemanticValid, RFQValid] at hs
  exact hs.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2

theorem accepted_invoice_complete_evidence (c : Context) (e : Envelope) (i : Invoice)
    (r : Result) (h : validate c ⟨e, .invoice i⟩ = some r) :
    lookup i.paymentId c.paymentEvidence = some i :=
  (validation_sound c ⟨e, .invoice i⟩ r h).2.2.1

theorem accepted_approval_current_policy (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    lookup a.actionId c.proposals = some a.proposal ∧ a.policyDigest = c.policyDigest := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.2.2.2.2.1, hs.2.2.2.2.2.1⟩

theorem accepted_approval_not_revoked (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    a.actionId ∉ c.revokedActions :=
  (validation_sound c ⟨e, .agent a⟩ r h).2.2.2.2.2.2.2.2.1

theorem accepted_approval_unexpired (c : Context) (e : Envelope) (a : Approval)
    (r : Result) (h : validate c ⟨e, .agent a⟩ = some r) :
    c.now < a.validUntil ∧ a.validUntil ≤ a.proposal.expires := by
  have hs := (validation_sound c ⟨e, .agent a⟩ r h).2
  exact ⟨hs.2.2.2.2.2.2.2.2.2.2.1, hs.2.2.2.2.2.2.2.2.2.2.2.1⟩

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
  exact ⟨hs.2.2.2.2.2.2.2.2.2.2.2.2.1,
    hs.2.2.2.2.2.2.2.2.2.2.2.2.2.1, hs.2.2.2.2.2.2.2.2.2.2.2.2.2.2.1⟩

theorem accepted_quote_exact_decimal_product (c : Context) (e : Envelope)
    (q : RFQ) (r : Result) (h : validate c ⟨e, .rfq q⟩ = some r) :
    q.cash = q.terms.quantity.value.product q.price.value := by
  have hs := (validation_sound c ⟨e, .rfq q⟩ r h).2
  have quantityScale := hs.2.2.2.2.2.2.2.2.2.1.2.2
  have priceScale := hs.2.2.2.2.2.2.2.2.2.2.1.2.2
  have cashScale := hs.2.2.2.2.2.2.2.2.2.2.2.1.2.2
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
  exact ⟨hs.2.2.2.2.2.2.2.2.2.2.2.2.1,
    hs.2.2.2.2.2.2.2.2.2.2.2.2.2.1, hs.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.1⟩

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
  exact ⟨hs.2.1, hs.2.2.1, hs.2.2.2.1, hs.2.2.2.2.1,
    hs.2.2.2.2.2.1, hs.2.2.2.2.2.2.1⟩

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

end MidnightExpress
