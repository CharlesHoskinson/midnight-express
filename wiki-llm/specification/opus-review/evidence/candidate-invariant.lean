import MidnightExpress
open MidnightExpress

def agentKey (e : Event) : Option (String × String × String) :=
  match e.payload with
  | .agent a => some (a.authorityDomain, a.executionScope, a.actionId)
  | _ => none

theorem replay_preserves_action_binding (s s' : ReplayState) (ek : String × String)
    (ed : String) (act : Option (String × String × String)) (i : String) (v : Verdict)
    (r : Result) (k : String × String × String) (old : String)
    (hk : lookup k s.actions = some old)
    (h : replay s ek ed act i v = some (r, s')) : lookup k s'.actions = some old := by
  unfold replay at h
  split at h
  · split at h <;> first | (cases h; exact hk) | contradiction
  · split at h
    · cases h; exact hk
    · rename_i key
      split at h
      · split at h <;> first | (cases h; exact hk) | contradiction
      · rename_i hnone
        cases h
        have hne : k ≠ key := by intro e; subst e; rw [hk] at hnone; contradiction
        simpa [lookup, hne] using hk

theorem check_preserves_action_binding (c : Context) (s s' : ReplayState) (e : Event)
    (ed i : String) (r : Result) (k : String × String × String) (old : String)
    (hk : lookup k s.actions = some old) (h : check c s e ed i = some (r, s')) :
    lookup k s'.actions = some old := by
  unfold check at h
  split at h
  · contradiction
  · exact replay_preserves_action_binding _ _ _ _ _ _ _ _ _ _ hk h

theorem replay_candidate_binds (s s' : ReplayState) (ek : String × String) (ed : String)
    (k : String × String × String) (i : String) (v : Verdict) (r : Result)
    (hv0 : v ≠ .duplicateEvent ∧ v ≠ .duplicateAction)
    (h : replay s ek ed (some k) i v = some (r, s')) (hv : r.verdict = v) :
    lookup k s.actions = none ∧ lookup k s'.actions = some i := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact absurd hv.symm hv0.1
    · contradiction
  · simp only at h
    split at h
    · split at h
      · cases h; exact absurd hv.symm hv0.2
      · contradiction
    · rename_i hnone; cases h; exact ⟨hnone, by simp [lookup]⟩

/-- At-most-once fresh candidate per action key across two threaded steps. -/
theorem no_second_candidate (c c' : Context) (s s₁ s₂ : ReplayState) (e e' : Event)
    (ed ed' i i' : String) (r r' : Result) (k : String × String × String)
    (hk : agentKey e = some k) (hk' : agentKey e' = some k)
    (h₁ : check c s e ed i = some (r, s₁)) (hr : r.verdict = .candidate)
    (h₂ : check c' s₁ e' ed' i' = some (r', s₂)) : r'.verdict ≠ .candidate := by
  -- step 1 binds k
  have bind₁ : lookup k s₁.actions = some i := by
    unfold check at h₁
    split at h₁
    · contradiction
    · rename_i r0 hv0
      have hr0 : r0.verdict = .candidate := by
        unfold validate at hv0; split at hv0
        · cases hv0; cases he : e.payload <;> simp_all [agentKey, payloadVerdict, observation]
        · contradiction
      simp only [agentKey] at hk
      cases he : e.payload <;> simp [he] at hk h₁
      subst hk
      exact (replay_candidate_binds _ _ _ _ _ _ _ _ (by rw [hr0]; decide) h₁ (by rw [hr, hr0])).2
  intro hr'
  unfold check at h₂
  split at h₂
  · contradiction
  · rename_i r1 hv1
    have hr1 : r1.verdict = .candidate := by
      unfold validate at hv1; split at hv1
      · cases hv1; cases he : e'.payload <;> simp_all [agentKey, payloadVerdict, observation]
      · contradiction
    simp only [agentKey] at hk'
    cases he : e'.payload <;> simp [he] at hk' h₂
    subst hk'
    have := (replay_candidate_binds _ _ _ _ _ _ _ _ (by rw [hr1]; decide) h₂ (by rw [hr', hr1])).1
    rw [bind₁] at this; contradiction
