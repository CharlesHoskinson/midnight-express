import MidnightExpress
namespace MidnightExpress.Scratch
open MidnightExpress

/-- Replay memory holding complete structural values instead of caller-supplied tokens. -/
structure IntentReplay where
  events : List ((String × String) × Event) := []
  actions : List (ActionKey × BusinessIntent) := []

def _root_.MidnightExpress.Event.actionKey? (e : Event) : Option ActionKey :=
  match e.payload with
  | .agent a => some a.actionKey
  | _ => none

def replayS (s : IntentReplay) (e : Event) (fresh : Verdict) : Option (Result × IntentReplay) :=
  match lookup e.occurrenceKey s.events with
  | some old => if old = e then some (observation .duplicateEvent, s) else none
  | none =>
    let events := (e.occurrenceKey, e) :: s.events
    match e.actionKey? with
    | none => some (observation fresh, { s with events })
    | some k =>
      match lookup k s.actions with
      | some old => if old = e.intent then some (observation .duplicateAction, { s with events }) else none
      | none => some (observation fresh, { events, actions := (k, e.intent) :: s.actions })

def checkS (c : Context) (s : IntentReplay) (e : Event) : Option (Result × IntentReplay) :=
  match validate c e with
  | none => none
  | some r => replayS s e r.verdict

/-- A recorded action cannot be reused for a different complete intent. -/
theorem changed_intent_conflicts (c : Context) (s : IntentReplay) (e : Event) (a : Approval)
    (I : BusinessIntent) (hp : e.payload = .agent a)
    (fresh : lookup e.occurrenceKey s.events = none)
    (known : lookup a.actionKey s.actions = some I) (ne : I ≠ e.intent) :
    checkS c s e = none := by
  unfold checkS
  split
  · rfl
  · simp [replayS, fresh, Event.actionKey?, hp, known, ne]

/-- End-to-end consequence: retargeting a recorded approval is refused under its old key. -/
theorem retargeted_approval_conflicts (c : Context) (s : IntentReplay) (env env' : Envelope)
    (a : Approval) (target : String) (h : target ≠ a.proposal.target)
    (same : env'.source = env.source ∧ env'.eventType = env.eventType ∧
      env'.profile = env.profile ∧ env'.contract = env.contract)
    (fresh : lookup (env'.source, env'.id) s.events = none)
    (known : lookup a.actionKey s.actions = some (Event.mk env (.agent a)).intent) :
    checkS c s (Event.mk env' (.agent {a with proposal := {a.proposal with target := target}})) = none := by
  apply changed_intent_conflicts c s (Event.mk env' (.agent {a with proposal := {a.proposal with target := target}}))
    {a with proposal := {a.proposal with target := target}} _ rfl (by simpa [Event.occurrenceKey] using fresh)
  · simpa [Approval.actionKey] using known
  · intro eq
    have := changed_target_changes_intent env a target h
    apply this
    obtain ⟨h1, h2, h3, h4⟩ := same
    simp only [Event.intent] at eq ⊢
    rw [eq]; simp [h1, h2, h3, h4]

/-- Occurrence-only retry of an identical event never yields a fresh verdict. -/
theorem identical_retry_duplicate (c : Context) (s : IntentReplay) (e : Event) (r : Result)
    (hv : validate c e = some r) (seen : lookup e.occurrenceKey s.events = some e) :
    checkS c s e = some (observation .duplicateEvent, s) := by
  simp [checkS, hv, replayS, seen]

end MidnightExpress.Scratch
