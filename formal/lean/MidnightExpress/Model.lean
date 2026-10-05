import Std

/-!
Typed semantic abstraction of the installed Midnight Express v0.2 profiles.
Wire parsing, lexical bounds, JCS, hashes, signatures and context provenance are
outside this module. Strings and integer instants are already decoded values.
No transport, ledger, payment or tool execution operation is provided.
-/
namespace MidnightExpress

inductive Profile where
  | rfq | invoice | agent
  deriving BEq, DecidableEq, Repr

def Profile.name : Profile → String
  | .rfq => "rfq.v0.2"
  | .invoice => "invoice.v0.2"
  | .agent => "agent.v0.2"

def Profile.eventType : Profile → String
  | .rfq => "mpe.rfq.quote.v0.2"
  | .invoice => "mpe.invoice.payment-observed.v0.2"
  | .agent => "mpe.agent.approval.v0.2"

def Profile.dataSchema : Profile → String
  | .rfq => "urn:mpe:model:rfq.v0.2"
  | .invoice => "urn:mpe:model:invoice.v0.2"
  | .agent => "urn:mpe:model:agent.v0.2"

-- Exact installed fixture commitments from model/profiles/lock.json.
def Profile.contract : Profile → String
  | .rfq => "sha256:8b5c6b89f6019fcb06b479e92f1b3bea340ac500cc218341e368e1ed2093071c"
  | .invoice => "sha256:dd3b68c4f25c4ca87a57e5e5dda88cb8a1630fa9a1b0ab394744fdf984eb047a"
  | .agent => "sha256:beaf501a8fdeefe757c340b1945dcd3e9c7c6e3fb4e00612f724afab7605b330"

def decodeProfile (s : String) : Option Profile :=
  if s = Profile.rfq.name then some .rfq
  else if s = Profile.invoice.name then some .invoice
  else if s = Profile.agent.name then some .agent
  else none

inductive Role where
  | dealer | paymentAdapter | humanApprover
  deriving BEq, DecidableEq, Repr

def Profile.role : Profile → Role
  | .rfq => .dealer
  | .invoice => .paymentAdapter
  | .agent => .humanApprover

inductive Side where
  | buy | sell
  deriving BEq, DecidableEq, Repr

inductive Currency where
  | usd
  deriving BEq, DecidableEq, Repr

inductive Unit where
  | share | step
  deriving BEq, DecidableEq, Repr

inductive Fee where
  | none
  deriving BEq, DecidableEq, Repr

inductive Environment where
  | sandbox
  deriving BEq, DecidableEq, Repr

inductive Operation where
  | writeReport
  deriving BEq, DecidableEq, Repr

def decodeOperation (s : String) : Option Operation :=
  if s = "WriteReport" then some .writeReport else none

def decodeCurrency (s : String) : Option Currency :=
  if s = "iso4217:USD" then some .usd else none

def decodeUnit (s : String) : Option Unit :=
  if s = "Share" then some .share else if s = "Step" then some .step else none

inductive PaymentStatus where
  | pending | final | reversed
  deriving BEq, DecidableEq, Repr

def decodePaymentStatus (s : String) : Option PaymentStatus :=
  if s = "Pending" then some .pending
  else if s = "Final" then some .final
  else if s = "Reversed" then some .reversed
  else none

structure Decimal where
  coefficient : Nat
  scale : Nat
  deriving BEq, DecidableEq, Repr

def maxCoefficient : Nat := 999999999999999999

def Decimal.ValidAt (d : Decimal) (scale : Nat) : Prop :=
  0 < d.coefficient ∧ d.coefficient ≤ maxCoefficient ∧ d.scale = scale

instance (d : Decimal) (scale : Nat) : Decidable (d.ValidAt scale) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

-- Exact arithmetic: the represented value is numerator / denominator.
-- Keeping the pair avoids introducing floating point or a rounding operation.
def Decimal.denominator (d : Decimal) : Nat := 10 ^ d.scale

def Decimal.product (a b : Decimal) : Decimal :=
  ⟨a.coefficient * b.coefficient, a.scale + b.scale⟩

structure Quantity where
  value : Decimal
  unit : Unit
  deriving BEq, DecidableEq, Repr

structure Price where
  value : Decimal
  currency : Currency
  assetRef : String
  unit : Unit
  baseQuantity : Nat
  fees : Fee
  deriving BEq, DecidableEq, Repr

structure RFQTerms where
  requester : String
  dealer : String
  requesterSide : Side
  asset : String
  quantity : Quantity
  currency : Currency
  deriving BEq, DecidableEq, Repr

structure RFQ where
  rfqId : String
  quoteId : String
  terms : RFQTerms
  buyer : String
  seller : String
  price : Price
  cash : Decimal
  validFrom : Int
  validUntil : Int
  deriving BEq, DecidableEq, Repr

-- The typed RFQ constructor represents Firm / AbsolutePerUnit /
-- OffchainCoordinationOnly. Other wire tags must fail decoding.
def RFQ.expectedBuyer (q : RFQ) : String :=
  match q.terms.requesterSide with
  | .buy => q.terms.requester
  | .sell => q.terms.dealer

def RFQ.expectedSeller (q : RFQ) : String :=
  match q.terms.requesterSide with
  | .buy => q.terms.dealer
  | .sell => q.terms.requester

structure InvoiceTerms where
  supplier : String
  customer : String
  documentDigest : String
  currency : Currency
  payable : Decimal
  deriving BEq, DecidableEq, Repr

structure Invoice where
  invoiceId : String
  terms : InvoiceTerms
  paymentId : String
  amount : Decimal
  status : PaymentStatus
  observedAt : Int
  effectiveAt : Int
  rail : String
  deriving BEq, DecidableEq, Repr

structure Proposal where
  environment : Environment
  operation : Operation
  target : String
  inputDigest : String
  budget : Quantity
  expires : Int
  deriving BEq, DecidableEq, Repr

structure Approval where
  authorityDomain : String
  executionScope : String
  budgetWindow : String
  actionId : String
  proposal : Proposal
  proposalDigest : String
  policyDigest : String
  human : String
  validFrom : Int
  validUntil : Int
  maxEffects : Nat
  deriving BEq, DecidableEq, Repr

structure Envelope where
  specversion : String
  id : String
  source : String
  eventType : String
  occurred : Int
  contentType : String
  dataSchema : String
  profile : String
  contract : String
  deriving BEq, DecidableEq, Repr

inductive Payload where
  | rfq (quote : RFQ)
  | invoice (payment : Invoice)
  | agent (approval : Approval)
  deriving BEq, DecidableEq, Repr

def Payload.profile : Payload → Profile
  | .rfq _ => .rfq
  | .invoice _ => .invoice
  | .agent _ => .agent

def Payload.principal : Payload → String
  | .rfq q => q.terms.dealer
  | .invoice i => i.rail
  | .agent a => a.human

structure Event where
  envelope : Envelope
  payload : Payload
  deriving BEq, DecidableEq, Repr

def Envelope.Matches (e : Envelope) (p : Profile) : Prop :=
  e.specversion = "1.0" ∧ e.contentType = "application/json" ∧
  e.profile = p.name ∧ e.contract = p.contract ∧
  e.eventType = p.eventType ∧ e.dataSchema = p.dataSchema

instance (e : Envelope) (p : Profile) : Decidable (e.Matches p) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

def dispatch (e : Envelope) : Option Profile :=
  match decodeProfile e.profile with
  | none => none
  | some p => if e.Matches p then some p else none

structure ActionKey where
  authorityDomain : String
  executionScope : String
  actionId : String
  deriving BEq, DecidableEq, Repr

def Approval.actionKey (a : Approval) : ActionKey :=
  ⟨a.authorityDomain, a.executionScope, a.actionId⟩

/-- Only approvals have logical action identity; observations use occurrence identity. -/
def Event.actionKey? (e : Event) : Option ActionKey :=
  match e.payload with
  | .agent a => some a.actionKey
  | _ => none

-- Full, unhashed intent. Digest implementations are an explicit boundary.
-- Equality here neither assumes hash injectivity nor proves SHA-256 security.
structure BusinessIntent where
  source : String
  eventType : String
  profile : String
  contract : String
  payload : Payload
  deriving BEq, DecidableEq, Repr

def Event.intent (e : Event) : BusinessIntent :=
  ⟨e.envelope.source, e.envelope.eventType, e.envelope.profile,
    e.envelope.contract, e.payload⟩

def Event.occurrenceKey (e : Event) : String × String :=
  (e.envelope.source, e.envelope.id)

theorem unknown_profile_rejected (s : String)
    (hr : s ≠ Profile.rfq.name) (hi : s ≠ Profile.invoice.name)
    (ha : s ≠ Profile.agent.name) : decodeProfile s = none := by
  simp [decodeProfile, hr, hi, ha]

theorem decode_profile_roundtrip (p : Profile) : decodeProfile p.name = some p := by
  cases p <;> decide

theorem unknown_operation_rejected (s : String) (h : s ≠ "WriteReport") :
    decodeOperation s = none := by
  simp [decodeOperation, h]

theorem dispatch_requires_exact_contract (e : Envelope) (p : Profile)
    (h : dispatch e = some p) : e.contract = p.contract := by
  unfold dispatch at h
  split at h
  · contradiction
  · rename_i found hf
    split at h
    · rename_i hm
      cases Option.some.inj h
      exact hm.2.2.2.1
    · contradiction

theorem dispatch_requires_exact_envelope (e : Envelope) (p : Profile)
    (h : dispatch e = some p) : e.Matches p := by
  unfold dispatch at h
  split at h
  · contradiction
  · split at h
    · rename_i hm
      cases Option.some.inj h
      exact hm
    · contradiction

theorem dispatch_iff_exact_envelope (e : Envelope) (p : Profile) :
    dispatch e = some p ↔ e.Matches p := by
  constructor
  · exact dispatch_requires_exact_envelope e p
  · intro hm
    have hp : decodeProfile e.profile = some p := by
      rw [hm.2.2.1]
      exact decode_profile_roundtrip p
    simp [dispatch, hp, hm]

theorem product_denominator (a b : Decimal) :
    (a.product b).denominator = a.denominator * b.denominator := by
  simp [Decimal.denominator, Decimal.product, Nat.pow_add]

theorem whole_shares_times_cents (shares cents : Decimal)
    (hs : shares.scale = 0) (hp : cents.scale = 2) :
    (shares.product cents).scale = 2 ∧
    (shares.product cents).coefficient = shares.coefficient * cents.coefficient := by
  simp [Decimal.product, hs, hp]

theorem positive_product (a b : Decimal) (ha : 0 < a.coefficient)
    (hb : 0 < b.coefficient) : 0 < (a.product b).coefficient := by
  exact Nat.mul_pos ha hb

-- Positivity and scale survive multiplication; only the exact 18-digit
-- product bound can fail when multiplying an admitted quantity and price.
theorem product_valid_iff_within_bound (shares cents : Decimal)
    (hs : shares.ValidAt 0) (hp : cents.ValidAt 2) :
    (shares.product cents).ValidAt 2 ↔
      shares.coefficient * cents.coefficient ≤ maxCoefficient := by
  have hpos := Nat.mul_pos hs.1 hp.1
  simp [Decimal.ValidAt, Decimal.product, hs.2.2, hp.2.2, hpos]

theorem requester_side_determines_distinct_roles (q : RFQ)
    (h : q.terms.requester ≠ q.terms.dealer) :
    q.expectedBuyer ≠ q.expectedSeller := by
  cases hs : q.terms.requesterSide with
  | buy => simpa [RFQ.expectedBuyer, RFQ.expectedSeller, hs] using h
  | sell => simpa [RFQ.expectedBuyer, RFQ.expectedSeller, hs] using Ne.symm h

theorem cash_unique (shares cents cash₁ cash₂ : Nat)
    (h₁ : cash₁ = shares * cents) (h₂ : cash₂ = shares * cents) : cash₁ = cash₂ := by
  omega

theorem occurrence_metadata_does_not_refresh_intent (e : Event) (id : String)
    (time : Int) :
    ({e with envelope := {e.envelope with id := id, occurred := time}}).intent =
      e.intent := by
  rfl

theorem changed_target_keeps_action_key (a : Approval) (target : String) :
    ({a with proposal := {a.proposal with target := target}}).actionKey = a.actionKey := by
  rfl

theorem changed_target_changes_intent (e : Envelope) (a : Approval) (target : String)
    (h : target ≠ a.proposal.target) :
    (Event.mk e (.agent {a with proposal := {a.proposal with target := target}})).intent ≠
      (Event.mk e (.agent a)).intent := by
  intro eq
  have hp : ({a.proposal with target := target}).target = a.proposal.target := by
    injection eq with _ _ _ _ payloadEq
    injection payloadEq with approvalEq
    exact congrArg (fun x : Approval => x.proposal.target) approvalEq
  exact h hp

theorem changed_contract_changes_intent (e : Event) (contract : String)
    (h : contract ≠ e.envelope.contract) :
    ({e with envelope := {e.envelope with contract := contract}}).intent ≠ e.intent := by
  intro eq
  exact h (congrArg BusinessIntent.contract eq)

end MidnightExpress
