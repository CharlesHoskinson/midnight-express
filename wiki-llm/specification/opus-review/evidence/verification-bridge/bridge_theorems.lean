import MidnightExpress
open MidnightExpress
-- Feasibility: connect `check` to the structural intent through digest functions.
theorem same_intent_new_occurrence_duplicate (c : Context) (s : ReplayState) (e e' : Event)
    (a : Approval) (H₁ : Event → String) (H₂ : BusinessIntent → String) (r : Result)
    (hp : e'.payload = .agent a) (same : e'.intent = e.intent)
    (hv : validate c e' = some r) (fresh : lookup e'.occurrenceKey s.events = none)
    (known : lookup (a.authorityDomain, a.executionScope, a.actionId) s.actions = some (H₂ e.intent)) :
    (check c s e' (H₁ e') (H₂ e'.intent)).map (fun x => x.1.verdict) = some .duplicateAction := by
  simp [check, hv, hp, replay, fresh, known, same, observation]

theorem redelivery_duplicate_action (c : Context) (s : ReplayState) (e : Event) (a : Approval)
    (H₁ : Event → String) (H₂ : BusinessIntent → String) (id : String) (time : Int) (r : Result)
    (hp : e.payload = .agent a)
    (hv : validate c {e with envelope := {e.envelope with id := id, occurred := time}} = some r)
    (fresh : lookup (e.envelope.source, id) s.events = none)
    (known : lookup (a.authorityDomain, a.executionScope, a.actionId) s.actions = some (H₂ e.intent)) :
    (check c s {e with envelope := {e.envelope with id := id, occurred := time}}
      (H₁ {e with envelope := {e.envelope with id := id, occurred := time}})
      (H₂ ({e with envelope := {e.envelope with id := id, occurred := time}}).intent)).map
        (fun x => x.1.verdict) = some .duplicateAction :=
  same_intent_new_occurrence_duplicate c s e _ a H₁ H₂ r hp
    (occurrence_metadata_does_not_refresh_intent e id time) hv fresh known

theorem changed_intent_same_key_conflicts (c : Context) (s : ReplayState) (env : Envelope)
    (a a' : Approval) (H₁ : Event → String) (H₂ : BusinessIntent → String)
    (inj : Function.Injective H₂) (r : Result)
    (hint : (Event.mk env (.agent a')).intent ≠ (Event.mk env (.agent a)).intent)
    (hkey : a'.actionKey = a.actionKey)
    (hv : validate c ⟨env, .agent a'⟩ = some r)
    (fresh : lookup (env.source, env.id) s.events = none)
    (known : lookup (a.authorityDomain, a.executionScope, a.actionId) s.actions =
      some (H₂ (Event.mk env (.agent a)).intent)) :
    check c s ⟨env, .agent a'⟩ (H₁ ⟨env, .agent a'⟩) (H₂ (Event.mk env (.agent a')).intent) = none := by
  obtain ⟨h1, h2, h3⟩ : a'.authorityDomain = a.authorityDomain ∧
      a'.executionScope = a.executionScope ∧ a'.actionId = a.actionId := by
    simpa [Approval.actionKey] using hkey
  have hne : H₂ (Event.mk env (.agent a)).intent ≠ H₂ (Event.mk env (.agent a')).intent :=
    fun h => hint (inj h).symm
  simp [check, hv, Event.occurrenceKey, replay, fresh, h1, h2, h3, known, hne]

theorem changed_target_conflicts (c : Context) (s : ReplayState) (env : Envelope) (a : Approval)
    (target : String) (H₁ : Event → String) (H₂ : BusinessIntent → String)
    (inj : Function.Injective H₂) (ht : target ≠ a.proposal.target) (r : Result)
    (hv : validate c ⟨env, .agent {a with proposal := {a.proposal with target := target}}⟩ = some r)
    (fresh : lookup (env.source, env.id) s.events = none)
    (known : lookup (a.authorityDomain, a.executionScope, a.actionId) s.actions =
      some (H₂ (Event.mk env (.agent a)).intent)) :
    check c s ⟨env, .agent {a with proposal := {a.proposal with target := target}}⟩
      (H₁ ⟨env, .agent {a with proposal := {a.proposal with target := target}}⟩)
      (H₂ (Event.mk env (.agent {a with proposal := {a.proposal with target := target}})).intent) = none :=
  changed_intent_same_key_conflicts c s env a _ H₁ H₂ inj r
    (changed_target_changes_intent env a target ht) (changed_target_keeps_action_key a target) hv fresh known

#print axioms redelivery_duplicate_action
#print axioms changed_target_conflicts

-- Translator escape check: json.dumps emits \b and \f, Lean literals may not accept them.
#eval "aéb".length
