import MidnightExpress.Validation

/-! Structural equality of decoded content, without a digest oracle or hash
injectivity. Sequential candidate classification neither reserves nor executes effects. -/
namespace MidnightExpress

structure Journal where
  events : List ((String × String) × Event) := []
  actions : List (ActionKey × BusinessIntent) := []
  deriving Repr, BEq, DecidableEq

def structuralReplay (s : Journal) (e : Event) (fresh : Verdict) : Option (Result × Journal) :=
  match lookup e.occurrenceKey s.events with
  | some old => if old = e then some (observation .duplicateEvent, s) else none
  | none =>
    let events := (e.occurrenceKey, e) :: s.events
    match e.actionKey? with
    | none => some (observation fresh, { s with events })
    | some k =>
      match lookup k s.actions with
      | some old => if old = e.intent then
          some (observation .duplicateAction, { s with events }) else none
      | none => some (observation fresh, { events, actions := (k, e.intent) :: s.actions })

/-- Current-context validation always precedes replay classification. -/
def structuralCheck (c : Context) (s : Journal) (e : Event) : Option (Result × Journal) :=
  match validate c e with
  | none => none
  | some r => structuralReplay s e r.verdict

theorem structural_invalid_now_cannot_replay (c : Context) (s : Journal) (e : Event)
    (invalid : validate c e = none) : structuralCheck c s e = none := by
  simp [structuralCheck, invalid]

theorem structural_occurrence_conflict_rejected (c : Context) (s : Journal) (e old : Event)
    (known : lookup e.occurrenceKey s.events = some old) (changed : old ≠ e) :
    structuralCheck c s e = none := by
  unfold structuralCheck
  split <;> simp [structuralReplay, known, changed]

theorem structural_identical_occurrence_duplicate (c : Context) (s : Journal) (e : Event)
    (r : Result) (valid : validate c e = some r)
    (known : lookup e.occurrenceKey s.events = some e) :
    structuralCheck c s e = some (observation .duplicateEvent, s) := by
  simp [structuralCheck, valid, structuralReplay, known]

theorem structural_action_conflict_rejected (c : Context) (s : Journal) (e : Event)
    (k : ActionKey) (old : BusinessIntent)
    (fresh : lookup e.occurrenceKey s.events = none) (key : e.actionKey? = some k)
    (known : lookup k s.actions = some old) (changed : old ≠ e.intent) :
    structuralCheck c s e = none := by
  unfold structuralCheck
  split <;> simp [structuralReplay, fresh, key, known, changed]

theorem structural_same_action_new_occurrence_duplicate (c : Context) (s : Journal)
    (e : Event) (k : ActionKey) (r : Result) (valid : validate c e = some r)
    (fresh : lookup e.occurrenceKey s.events = none) (key : e.actionKey? = some k)
    (known : lookup k s.actions = some e.intent) :
    structuralCheck c s e = some (observation .duplicateAction,
      { s with events := (e.occurrenceKey, e) :: s.events }) := by
  simp [structuralCheck, valid, structuralReplay, fresh, key, known]

/-- Exhaustive successful transitions; insertion requires an unbound key. -/
theorem structuralReplay_cases (s s' : Journal) (e : Event) (v : Verdict) (r : Result)
    (h : structuralReplay s e v = some (r, s')) :
    (r = observation .duplicateEvent ∧ s' = s ∧ lookup e.occurrenceKey s.events = some e) ∨
    (lookup e.occurrenceKey s.events = none ∧ e.actionKey? = none ∧
      r = observation v ∧ s' = { s with events := (e.occurrenceKey, e) :: s.events }) ∨
    (∃ k, lookup e.occurrenceKey s.events = none ∧ e.actionKey? = some k ∧
      lookup k s.actions = some e.intent ∧ r = observation .duplicateAction ∧
      s' = { s with events := (e.occurrenceKey, e) :: s.events }) ∨
    (∃ k, lookup e.occurrenceKey s.events = none ∧ e.actionKey? = some k ∧
      lookup k s.actions = none ∧ r = observation v ∧
      s' = { events := (e.occurrenceKey, e) :: s.events, actions := (k, e.intent) :: s.actions }) := by
  unfold structuralReplay at h
  split at h
  · rename_i old known
    split at h
    · rename_i same
      subst old
      cases h
      exact Or.inl ⟨rfl, rfl, known⟩
    · contradiction
  · rename_i fresh
    split at h
    · rename_i key
      cases h
      exact Or.inr (Or.inl ⟨fresh, key, rfl, rfl⟩)
    · rename_i k key
      split at h
      · rename_i old known
        split at h
        · rename_i same
          subst old
          cases h
          exact Or.inr (Or.inr (Or.inl ⟨k, fresh, key, known, rfl, rfl⟩))
        · contradiction
      · rename_i freshAction
        cases h
        exact Or.inr (Or.inr (Or.inr ⟨k, fresh, key, freshAction, rfl, rfl⟩))

private theorem lookup_cons_preserves [DecidableEq α] (table : List (α × β))
    (insert key : α) (value old : β) (fresh : lookup insert table = none)
    (known : lookup key table = some old) : lookup key ((insert, value) :: table) = some old := by
  have distinct : key ≠ insert := by
    intro eq
    subst key
    rw [known] at fresh
    contradiction
  simp [lookup, distinct, known]

theorem structuralReplay_preserves_occurrence (s s' : Journal) (e old : Event)
    (key : String × String) (v : Verdict) (r : Result)
    (known : lookup key s.events = some old)
    (h : structuralReplay s e v = some (r, s')) : lookup key s'.events = some old := by
  rcases structuralReplay_cases s s' e v r h with
    ⟨_, rfl, _⟩ | ⟨fresh, _, _, rfl⟩ | ⟨_, fresh, _, _, _, rfl⟩ |
      ⟨_, fresh, _, _, _, rfl⟩
  · exact known
  all_goals exact lookup_cons_preserves _ _ _ _ _ fresh known

theorem structuralReplay_preserves_action (s s' : Journal) (e : Event)
    (key : ActionKey) (old : BusinessIntent) (v : Verdict) (r : Result)
    (known : lookup key s.actions = some old)
    (h : structuralReplay s e v = some (r, s')) : lookup key s'.actions = some old := by
  rcases structuralReplay_cases s s' e v r h with
    ⟨_, rfl, _⟩ | ⟨_, _, _, rfl⟩ | ⟨_, _, _, _, _, rfl⟩ |
      ⟨_, _, _, fresh, _, rfl⟩
  all_goals first | exact known | exact lookup_cons_preserves _ _ _ _ _ fresh known

theorem structuralCheck_preserves_occurrence (c : Context) (s s' : Journal)
    (e old : Event) (key : String × String) (r : Result)
    (known : lookup key s.events = some old)
    (h : structuralCheck c s e = some (r, s')) : lookup key s'.events = some old := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · exact structuralReplay_preserves_occurrence _ _ _ _ _ _ _ known h

theorem structuralCheck_preserves_action (c : Context) (s s' : Journal) (e : Event)
    (key : ActionKey) (old : BusinessIntent) (r : Result)
    (known : lookup key s.actions = some old)
    (h : structuralCheck c s e = some (r, s')) : lookup key s'.actions = some old := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · exact structuralReplay_preserves_action _ _ _ _ _ _ _ known h

theorem structural_fresh_candidate_binds_action (c : Context) (s s' : Journal) (e : Event)
    (k : ActionKey) (r : Result) (key : e.actionKey? = some k)
    (h : structuralCheck c s e = some (r, s')) (candidate : r.verdict = .candidate) :
    lookup k s.actions = none ∧ lookup k s'.actions = some e.intent := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · rcases structuralReplay_cases _ _ _ _ _ h with
      ⟨rfl, _, _⟩ | ⟨_, noKey, _, _⟩ | ⟨_, _, _, _, rfl, _⟩ |
        ⟨k', _, key', fresh, _, rfl⟩
    · cases candidate
    · rw [key] at noKey; contradiction
    · cases candidate
    · have eq : k' = k := Option.some.inj (key'.symm.trans key)
      subst k'
      exact ⟨fresh, by simp [lookup]⟩

theorem structural_known_action_never_candidate (c : Context) (s s' : Journal)
    (e : Event) (k : ActionKey) (old : BusinessIntent) (r : Result)
    (key : e.actionKey? = some k) (known : lookup k s.actions = some old)
    (h : structuralCheck c s e = some (r, s')) : r.verdict ≠ .candidate := by
  intro candidate
  have fresh := (structural_fresh_candidate_binds_action c s s' e k r key h candidate).1
  rw [known] at fresh
  contradiction

/-- Unique keys, correct occurrence keys, and bidirectional action/content coherence. -/
structure Journal.WellFormed (s : Journal) : Prop where
  uniqueOccurrences : (s.events.map Prod.fst).Nodup
  uniqueActions : (s.actions.map Prod.fst).Nodup
  occurrenceKeys : ∀ key e, (key, e) ∈ s.events → e.occurrenceKey = key
  occurrenceActions : ∀ key e, (key, e) ∈ s.events →
    ∀ k, e.actionKey? = some k → lookup k s.actions = some e.intent
  actionWitnesses : ∀ k intent, (k, intent) ∈ s.actions →
    ∃ e, (e.occurrenceKey, e) ∈ s.events ∧ e.actionKey? = some k ∧ e.intent = intent

private theorem lookup_none_not_key [DecidableEq α] (key : α) (table : List (α × β))
    (h : lookup key table = none) : key ∉ table.map Prod.fst := by
  induction table with
  | nil => simp
  | cons pair rest ih =>
    rcases pair with ⟨k, v⟩
    simp only [lookup] at h
    split at h
    · contradiction
    · rename_i distinct
      simp [distinct, ih h]

private theorem lookup_some_member [DecidableEq α] (key : α) (value : β)
    (table : List (α × β)) (h : lookup key table = some value) : (key, value) ∈ table := by
  induction table with
  | nil => contradiction
  | cons pair rest ih =>
    rcases pair with ⟨k, v⟩
    simp only [lookup] at h
    split at h
    · rename_i eq
      cases eq
      cases Option.some.inj h
      simp
    · exact List.mem_cons_of_mem _ (ih h)

theorem Journal.empty_wellFormed : Journal.WellFormed {} := by
  constructor <;> simp

private theorem Journal.record_occurrence_wellFormed (s : Journal) (e : Event)
    (wf : s.WellFormed) (fresh : lookup e.occurrenceKey s.events = none)
    (bound : ∀ k, e.actionKey? = some k → lookup k s.actions = some e.intent) :
    Journal.WellFormed { s with events := (e.occurrenceKey, e) :: s.events } := by
  refine ⟨?_, wf.uniqueActions, ?_, ?_, ?_⟩
  · simpa using List.nodup_cons.mpr ⟨lookup_none_not_key _ _ fresh, wf.uniqueOccurrences⟩
  · intro key old member
    rcases List.mem_cons.mp member with eq | member
    · cases eq; rfl
    · exact wf.occurrenceKeys key old member
  · intro key old member k action
    rcases List.mem_cons.mp member with eq | member
    · cases eq; exact bound k action
    · exact wf.occurrenceActions key old member k action
  · intro k intent member
    obtain ⟨old, event, action, same⟩ := wf.actionWitnesses k intent member
    exact ⟨old, List.mem_cons_of_mem _ event, action, same⟩

private theorem Journal.record_action_wellFormed (s : Journal) (e : Event) (k : ActionKey)
    (wf : s.WellFormed) (fresh : lookup e.occurrenceKey s.events = none)
    (key : e.actionKey? = some k) (freshAction : lookup k s.actions = none) :
    Journal.WellFormed { events := (e.occurrenceKey, e) :: s.events, actions := (k, e.intent) :: s.actions } := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simpa using List.nodup_cons.mpr ⟨lookup_none_not_key _ _ fresh, wf.uniqueOccurrences⟩
  · simpa using List.nodup_cons.mpr ⟨lookup_none_not_key _ _ freshAction, wf.uniqueActions⟩
  · intro eventKey old member
    rcases List.mem_cons.mp member with eq | member
    · cases eq; rfl
    · exact wf.occurrenceKeys eventKey old member
  · intro eventKey old member actionKey action
    rcases List.mem_cons.mp member with eq | member
    · cases eq
      have same : actionKey = k := Option.some.inj (action.symm.trans key)
      subst actionKey
      simp [lookup]
    · exact lookup_cons_preserves _ _ _ _ _ freshAction
        (wf.occurrenceActions eventKey old member actionKey action)
  · intro actionKey intent member
    rcases List.mem_cons.mp member with eq | member
    · cases eq
      exact ⟨e, by simp, key, rfl⟩
    · obtain ⟨old, event, action, same⟩ := wf.actionWitnesses actionKey intent member
      exact ⟨old, List.mem_cons_of_mem _ event, action, same⟩

theorem structuralReplay_preserves_wellFormed (s s' : Journal) (e : Event)
    (v : Verdict) (r : Result) (wf : s.WellFormed)
    (h : structuralReplay s e v = some (r, s')) : s'.WellFormed := by
  rcases structuralReplay_cases s s' e v r h with
    ⟨_, rfl, _⟩ | ⟨fresh, noKey, _, rfl⟩ | ⟨k, fresh, key, known, _, rfl⟩ |
      ⟨k, fresh, key, freshAction, _, rfl⟩
  · exact wf
  · apply Journal.record_occurrence_wellFormed s e wf fresh
    intro k hk
    rw [noKey] at hk
    contradiction
  · apply Journal.record_occurrence_wellFormed s e wf fresh
    intro k' hk
    have eq : k' = k := Option.some.inj (hk.symm.trans key)
    subst k'
    exact known
  · exact Journal.record_action_wellFormed s e k wf fresh key freshAction

theorem structuralCheck_preserves_wellFormed (c : Context) (s s' : Journal)
    (e : Event) (r : Result) (wf : s.WellFormed)
    (h : structuralCheck c s e = some (r, s')) : s'.WellFormed := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · exact structuralReplay_preserves_wellFormed _ _ _ _ _ wf h

/-- A reachable journal arises from successful checks under any sequence of contexts.
Rejected attempts leave the journal unchanged and therefore add no reachable states. -/
inductive Reachable : Journal → Prop where
  | empty : Reachable {}
  | accepted {s s' : Journal} {c : Context} {e : Event} {r : Result} :
      Reachable s → structuralCheck c s e = some (r, s') → Reachable s'

theorem reachable_wellFormed (s : Journal) (h : Reachable s) : s.WellFormed := by
  induction h with
  | empty => exact Journal.empty_wellFormed
  | accepted _ checked ih => exact structuralCheck_preserves_wellFormed _ _ _ _ _ ih checked

theorem reachable_occurrence_has_action (s : Journal) (key : String × String)
    (e : Event) (k : ActionKey) (reachable : Reachable s)
    (known : lookup key s.events = some e) (action : e.actionKey? = some k) :
    lookup k s.actions = some e.intent :=
  (reachable_wellFormed s reachable).occurrenceActions key e
    (lookup_some_member key e s.events known) k action

theorem structuralCheck_sound (c : Context) (s s' : Journal) (e : Event) (r : Result)
    (h : structuralCheck c s e = some (r, s')) : CommonValid c e ∧ SemanticValid c e := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · rename_i validated valid
    exact validation_sound c e validated valid

theorem structuralCheck_never_executes (c : Context) (s s' : Journal) (e : Event) (r : Result)
    (h : structuralCheck c s e = some (r, s')) : r.executes = false := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · rcases structuralReplay_cases _ _ _ _ _ h with
      ⟨rfl, _, _⟩ | ⟨_, _, rfl, _⟩ | ⟨_, _, _, _, rfl, _⟩ | ⟨_, _, _, _, rfl, _⟩
    all_goals rfl

/-- Sequential attempts, each with its own current context. Rejections record no
verdict and preserve the journal. The receipts are classification history only. -/
def run (s : Journal) : List (Context × Event) → List (Event × Option Result) × Journal
  | [] => ([], s)
  | (c, e) :: rest =>
    match structuralCheck c s e with
    | none => let tail := run s rest; ((e, none) :: tail.1, tail.2)
    | some (r, s') => let tail := run s' rest; ((e, some r) :: tail.1, tail.2)

theorem run_preserves_action (s : Journal) (trace : List (Context × Event))
    (k : ActionKey) (intent : BusinessIntent) (known : lookup k s.actions = some intent) :
    lookup k (run s trace).2.actions = some intent := by
  induction trace generalizing s with
  | nil => exact known
  | cons input rest ih =>
    rcases input with ⟨c, e⟩
    cases checked : structuralCheck c s e with
    | none => simpa [run, checked] using ih s known
    | some pair =>
      rcases pair with ⟨r, s'⟩
      simpa [run, checked] using ih s'
        (structuralCheck_preserves_action c s s' e k intent r known checked)

theorem run_preserves_occurrence (s : Journal) (trace : List (Context × Event))
    (key : String × String) (e : Event) (known : lookup key s.events = some e) :
    lookup key (run s trace).2.events = some e := by
  induction trace generalizing s with
  | nil => exact known
  | cons input rest ih =>
    rcases input with ⟨c, next⟩
    cases checked : structuralCheck c s next with
    | none => simpa [run, checked] using ih s known
    | some pair =>
      rcases pair with ⟨r, s'⟩
      simpa [run, checked] using ih s'
        (structuralCheck_preserves_occurrence c s s' next e key r known checked)

theorem run_preserves_wellFormed (s : Journal) (trace : List (Context × Event))
    (wf : s.WellFormed) : (run s trace).2.WellFormed := by
  induction trace generalizing s with
  | nil => exact wf
  | cons input rest ih =>
    rcases input with ⟨c, e⟩
    cases checked : structuralCheck c s e with
    | none => simpa [run, checked] using ih s wf
    | some pair =>
      rcases pair with ⟨r, s'⟩
      simpa [run, checked] using ih s'
        (structuralCheck_preserves_wellFormed c s s' e r wf checked)

theorem run_preserves_reachable (s : Journal) (trace : List (Context × Event))
    (reachable : Reachable s) : Reachable (run s trace).2 := by
  induction trace generalizing s with
  | nil => exact reachable
  | cons input rest ih =>
    rcases input with ⟨c, e⟩
    cases checked : structuralCheck c s e with
    | none => simpa [run, checked] using ih s reachable
    | some pair =>
      rcases pair with ⟨r, s'⟩
      simpa [run, checked] using ih s' (.accepted reachable checked)

def candidateCount (k : ActionKey) : List (Event × Option Result) → Nat
  | [] => 0
  | (_, none) :: rest => candidateCount k rest
  | (e, some r) :: rest =>
    if e.actionKey? = some k ∧ r.verdict = .candidate then
      1 + candidateCount k rest else candidateCount k rest

/-- A known action cannot yield any fresh candidate, even when contexts vary. -/
theorem run_known_action_no_candidates (s : Journal) (trace : List (Context × Event))
    (k : ActionKey) (intent : BusinessIntent) (known : lookup k s.actions = some intent) :
    candidateCount k (run s trace).1 = 0 := by
  induction trace generalizing s with
  | nil => rfl
  | cons input rest ih =>
    rcases input with ⟨c, e⟩
    cases checked : structuralCheck c s e with
    | none => simpa [run, checked, candidateCount] using ih s known
    | some pair =>
      rcases pair with ⟨r, s'⟩
      have tail := ih s' (structuralCheck_preserves_action c s s' e k intent r known checked)
      have noCandidate : ¬(e.actionKey? = some k ∧ r.verdict = .candidate) := by
        intro both
        exact structural_known_action_never_candidate c s s' e k intent r both.1 known checked both.2
      simp [run, checked, candidateCount, noCandidate, tail]

/-- At most one fresh candidate for an action throughout any sequential trace.
No reachability premise is needed: a fresh candidate itself creates the binding. -/
theorem run_at_most_one_fresh_candidate (s : Journal) (trace : List (Context × Event))
    (k : ActionKey) : candidateCount k (run s trace).1 ≤ 1 := by
  induction trace generalizing s with
  | nil => simp [run, candidateCount]
  | cons input rest ih =>
    rcases input with ⟨c, e⟩
    cases checked : structuralCheck c s e with
    | none => simpa [run, checked, candidateCount] using ih s
    | some pair =>
      rcases pair with ⟨r, s'⟩
      by_cases fresh : e.actionKey? = some k ∧ r.verdict = .candidate
      · have bound := (structural_fresh_candidate_binds_action c s s' e k r fresh.1 checked fresh.2).2
        have tail := run_known_action_no_candidates s' rest k e.intent bound
        simp [run, checked, candidateCount, fresh, tail]
      · simpa [run, checked, candidateCount, fresh] using ih s'

/-- After a fresh candidate and arbitrarily many intervening attempts, another
successful check for the same action cannot be a fresh candidate. -/
theorem structural_no_second_candidate_across_run (c later : Context)
    (s s₁ s₂ : Journal) (e next : Event) (r r' : Result) (k : ActionKey)
    (middle : List (Context × Event)) (key : e.actionKey? = some k)
    (nextKey : next.actionKey? = some k)
    (first : structuralCheck c s e = some (r, s₁)) (fresh : r.verdict = .candidate)
    (second : structuralCheck later (run s₁ middle).2 next = some (r', s₂)) :
    r'.verdict ≠ .candidate := by
  have bound := (structural_fresh_candidate_binds_action c s s₁ e k r key first fresh).2
  exact structural_known_action_never_candidate later (run s₁ middle).2 s₂ next k e.intent r'
    nextKey (run_preserves_action s₁ middle k e.intent bound) second

/-- Coherent journals reject changed business content under a bound action,
including the case where the occurrence key is already present. -/
theorem structural_bound_action_conflict_rejected (c : Context) (s : Journal)
    (e : Event) (k : ActionKey) (old : BusinessIntent) (wf : s.WellFormed)
    (key : e.actionKey? = some k) (known : lookup k s.actions = some old)
    (changed : old ≠ e.intent) : structuralCheck c s e = none := by
  cases occurrence : lookup e.occurrenceKey s.events with
  | none => exact structural_action_conflict_rejected c s e k old occurrence key known changed
  | some stored =>
    have different : stored ≠ e := by
      intro same
      subst stored
      have binding := wf.occurrenceActions e.occurrenceKey e
        (lookup_some_member _ _ _ occurrence) k key
      rw [known] at binding
      exact changed (Option.some.inj binding)
    exact structural_occurrence_conflict_rejected c s e stored occurrence different

theorem structural_reachable_action_conflict_rejected (c : Context) (s : Journal)
    (e : Event) (k : ActionKey) (old : BusinessIntent) (reachable : Reachable s)
    (key : e.actionKey? = some k) (known : lookup k s.actions = some old)
    (changed : old ≠ e.intent) : structuralCheck c s e = none :=
  structural_bound_action_conflict_rejected c s e k old (reachable_wellFormed s reachable)
    key known changed

/-- Altering an approval's actual expiry cannot be hidden by a reused replay token. -/
theorem structural_changed_approval_expiry_conflicts (c : Context) (s : Journal)
    (envelope : Envelope) (a : Approval) (expiry : Int) (wf : s.WellFormed)
    (known : lookup a.actionKey s.actions = some (Event.mk envelope (.agent a)).intent)
    (changed : expiry ≠ a.validUntil) :
    structuralCheck c s (Event.mk envelope (.agent { a with validUntil := expiry })) = none := by
  apply structural_bound_action_conflict_rejected c s _ a.actionKey _ wf (by rfl) known
  intro same
  have payloadEq := congrArg BusinessIntent.payload same
  have approvalEq : a = { a with validUntil := expiry } := Payload.agent.inj payloadEq
  exact changed (congrArg Approval.validUntil approvalEq).symm

/-- In a coherent journal, every successful approval check leaves its content bound.
This includes duplicate occurrences, closing the malformed-initial-state retry gap. -/
theorem structural_successful_approval_binds_action (c : Context) (s s' : Journal)
    (e : Event) (k : ActionKey) (r : Result) (wf : s.WellFormed)
    (key : e.actionKey? = some k) (h : structuralCheck c s e = some (r, s')) :
    lookup k s'.actions = some e.intent := by
  unfold structuralCheck at h
  split at h
  · contradiction
  · rcases structuralReplay_cases _ _ _ _ _ h with
      ⟨_, rfl, occurrence⟩ | ⟨_, noKey, _, _⟩ | ⟨k', _, key', known, _, rfl⟩ |
        ⟨k', _, key', _, _, rfl⟩
    · exact wf.occurrenceActions e.occurrenceKey e
        (lookup_some_member _ _ _ occurrence) k key
    · rw [key] at noKey; contradiction
    · have same : k' = k := Option.some.inj (key'.symm.trans key)
      subst k'
      exact known
    · have same : k' = k := Option.some.inj (key'.symm.trans key)
      subst k'
      simp [lookup]

theorem reachable_unique_keys (s : Journal) (reachable : Reachable s) :
    (s.events.map Prod.fst).Nodup ∧ (s.actions.map Prod.fst).Nodup :=
  ⟨(reachable_wellFormed s reachable).uniqueOccurrences,
    (reachable_wellFormed s reachable).uniqueActions⟩

end MidnightExpress
