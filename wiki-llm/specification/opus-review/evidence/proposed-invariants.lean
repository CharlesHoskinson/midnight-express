import MidnightExpress
open MidnightExpress

namespace Probe

/-! Rejection characterization: currently only derivable, not stated. -/
theorem validate_eq_some_iff (c : Context) (e : Event) (r : Result) :
    validate c e = some r ↔
      (CommonValid c e ∧ SemanticValid c e) ∧ r = observation (payloadVerdict e.payload) := by
  constructor
  · intro h
    refine ⟨validation_sound c e r h, ?_⟩
    have := validation_complete c e (validation_sound c e r h).1 (validation_sound c e r h).2
    rw [h] at this; exact (Option.some.inj this)
  · rintro ⟨⟨hc, hs⟩, rfl⟩; exact validation_complete c e hc hs

theorem validate_eq_none_iff (c : Context) (e : Event) :
    validate c e = none ↔ ¬ (CommonValid c e ∧ SemanticValid c e) := by
  constructor
  · intro h ⟨hc, hs⟩; rw [validation_complete c e hc hs] at h; cases h
  · intro h
    cases hv : validate c e with
    | none => rfl
    | some r => exact absurd (validation_sound c e r hv) h

/-! Envelope/payload agreement: accepted events cannot carry a payload of
another profile than the one the envelope dispatches to. -/
theorem accepted_payload_matches_envelope (c : Context) (e : Event) (r : Result)
    (h : validate c e = some r) : e.envelope.Matches e.payload.profile :=
  dispatch_requires_exact_envelope _ _ (validation_sound c e r h).1.2.1

theorem decodeProfile_sound (s : String) (p : Profile) (h : decodeProfile s = some p) :
    s = p.name := by
  unfold decodeProfile at h
  split at h
  · cases h; assumption
  · split at h
    · cases h; assumption
    · split at h
      · cases h; assumption
      · cases h

/-! Approval expiry rejection (only the RFQ version exists). -/
theorem expired_approval_rejected (c : Context) (e : Envelope) (a : Approval)
    (expired : a.validUntil ≤ c.now) : validate c ⟨e, .agent a⟩ = none := by
  cases result : validate c ⟨e, .agent a⟩ with
  | none => rfl
  | some r =>
    have := (accepted_approval_unexpired c e a r result).1
    omega

/-! Context monotonicity: adding a revocation never creates an acceptance. -/
theorem revocation_monotone (c : Context) (e : Event) (x : String) (r : Result)
    (h : validate { c with revokedActions := x :: c.revokedActions } e = some r) :
    validate c e = some r := by
  have ⟨hc, hs⟩ := validation_sound _ e r h
  have hr := (validate_eq_some_iff _ e r).mp h |>.2
  subst hr
  apply validation_complete
  · exact hc
  · unfold SemanticValid at hs ⊢
    cases hp : e.payload with
    | rfq q => rw [hp] at hs; exact hs
    | invoice i => rw [hp] at hs; exact hs
    | agent a =>
      rw [hp] at hs
      simp only [ApprovalValid, List.mem_cons, not_or] at hs ⊢
      exact ⟨hs.1, hs.2.1, hs.2.2.1, hs.2.2.2.1, hs.2.2.2.2.1, hs.2.2.2.2.2.1, hs.2.2.2.2.2.2.1,
        hs.2.2.2.2.2.2.2.1.2, hs.2.2.2.2.2.2.2.2⟩

/-! Replay invariants. -/
theorem lookup_cons_ne [DecidableEq α] (k k' : α) (v : β) (l : List (α × β)) (h : k ≠ k') :
    lookup k ((k', v) :: l) = lookup k l := by simp [lookup, h]

theorem replay_records_event (s s' : ReplayState) (key : String × String) (d i : String)
    (act : Option (String × String × String)) (v : Verdict) (r : Result)
    (h : replay s key d act i v = some (r, s')) : lookup key s'.events = some d := by
  unfold replay at h
  split at h
  · rename_i old hold; split at h
    · cases h; subst_vars; exact hold
    · contradiction
  · split at h
    · cases h; simp [lookup]
    · split at h
      · split at h
        · cases h; simp [lookup]
        · contradiction
      · cases h; simp [lookup]

theorem replay_preserves_events (s s' : ReplayState) (key k : String × String) (d i old : String)
    (act : Option (String × String × String)) (v : Verdict) (r : Result)
    (h : replay s key d act i v = some (r, s')) (known : lookup k s.events = some old) :
    lookup k s'.events = some old := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact known
    · contradiction
  · rename_i hnone
    have hk : k ≠ key := by intro eq; subst eq; rw [hnone] at known; cases known
    split at h
    · cases h; simp [lookup, hk, known]
    · split at h
      · split at h
        · cases h; simp [lookup, hk, known]
        · contradiction
      · cases h; simp [lookup, hk, known]

/-- After any successful replay carrying an action key, that key is bound
in memory unless the event was itself an exact duplicate occurrence. -/
theorem replay_binds_action (s s' : ReplayState) (key : String × String) (d i : String)
    (ak : String × String × String) (v : Verdict) (r : Result)
    (h : replay s key d (some ak) i v = some (r, s')) (notDup : r.verdict ≠ .duplicateEvent) :
    lookup ak s'.actions = some i := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact absurd rfl notDup
    · contradiction
  · simp only at h
    split at h
    · rename_i old hold; split at h
      · cases h; subst_vars; exact hold
      · contradiction
    · cases h; simp [lookup]

/-- Single-fresh-verdict property for a bound action: once bound, the action can
only yield duplicate verdicts or rejection, never a second fresh verdict. -/
theorem bound_action_never_fresh (s s' : ReplayState) (key : String × String) (d i old : String)
    (ak : String × String × String) (v : Verdict) (r : Result)
    (bound : lookup ak s.actions = some old)
    (h : replay s key d (some ak) i v = some (r, s')) :
    r.verdict = .duplicateEvent ∨ r.verdict = .duplicateAction := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact .inl rfl
    · contradiction
  · simp only [bound] at h
    split at h
    · cases h; exact .inr rfl
    · contradiction

/-- Actions are preserved by replay. -/
theorem replay_preserves_actions (s s' : ReplayState) (key : String × String) (d i old : String)
    (act : Option (String × String × String)) (v : Verdict) (r : Result)
    (ak : String × String × String)
    (h : replay s key d act i v = some (r, s')) (known : lookup ak s.actions = some old) :
    lookup ak s'.actions = some old := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact known
    · contradiction
  · split at h
    · cases h; exact known
    · rename_i k
      split at h
      · split at h
        · cases h; exact known
        · contradiction
      · rename_i hnone
        have hk : ak ≠ k := by intro eq; subst eq; rw [hnone] at known; cases known
        cases h; simp [lookup, hk, known]

end Probe

#print axioms Probe.validate_eq_some_iff
#print axioms Probe.revocation_monotone
#print axioms Probe.bound_action_never_fresh
#print axioms Probe.replay_preserves_actions
#print axioms MidnightExpress.changed_target_changes_intent
#print axioms MidnightExpress.expired_quote_rejected
#print axioms MidnightExpress.dispatch_iff_exact_envelope
#print axioms MidnightExpress.semanticCheck_iff
#print axioms MidnightExpress.product_valid_iff_within_bound
