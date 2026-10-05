import MidnightExpress.Examples
open MidnightExpress MidnightExpress.Examples

/- A. The stateful conflict result depends on caller-supplied digests.
   Context c2 re-issues action:demo with a different target. Python rejects
   the second event (action-identity-conflict) because it hashes e.intent.
   Lean `check` returns duplicateAction when the caller reuses a digest. -/
def changedProposal : Proposal :=
  { environment := .sandbox, operation := .writeReport, target := "sandbox:reports/other",
    inputDigest := "sha256:2222222222222222222222222222222222222222222222222222222222222222",
    budget := { value := { coefficient := 5, scale := 0 }, unit := .step }, expires := 1791118800 }

def baseApproval : Approval :=
  { authorityDomain := "urn:mpe:sandbox:local", executionScope := "scope:fixture", budgetWindow := "window:fixture", actionId := "action:demo", proposalDigest := "sha256:94bdf0c08cd824de5432499e7bed3bf007cdc5b545dc089dc57b0eb5924ecb28", policyDigest := "sha256:3333333333333333333333333333333333333333333333333333333333333333", human := "human:alice", proposal := { environment := .sandbox, operation := .writeReport, target := "sandbox:reports/demo", inputDigest := "sha256:2222222222222222222222222222222222222222222222222222222222222222", budget := { value := { coefficient := 5, scale := 0 }, unit := .step }, expires := 1791118800 }, validFrom := 1791111600, validUntil := 1791118800, maxEffects := 1 }

example : event1.payload = .agent baseApproval := by decide

def reissuedApproval : Approval := { baseApproval with proposal := changedProposal, proposalDigest := "sha256:changed" }

def reissued : Event := { envelope := { event1.envelope with id := "event:agent-2" }, payload := .agent reissuedApproval }

def ctxR : Context := { context1 with proposals := [("action:demo", changedProposal)], sandboxTargets := ["sandbox:reports/other"], proposalDigest := fun _ _ => "sha256:changed" }

example : validate ctxR reissued = some (observation .candidate) := by decide
example : reissued.intent ≠ event1.intent := by decide

-- first acceptance, then a changed intent under the same key with a reused digest token
example :
    (match check context1 {} event1 "e1" "intent" with
     | some (_, s1) => (check ctxR s1 reissued "e2" "intent").map (·.1.verdict)
     | none => none) = some .duplicateAction := by decide

-- D. Same Final payment in two occurrences (event2 = fixture invoice-final): both fresh.
def invoiceAgain : Event := { envelope := { event2.envelope with id := "event:invoice-final-again" }, payload := event2.payload }

example :
    (match check context2 {} event2 "e1" "i1" with
     | some (_, s1) => (check context2 s1 invoiceAgain "e3" "i3").map (·.1.verdict)
     | none => none) = some .paymentFinal := by decide

/- E. At-most-once fresh verdict per action key, independent of digests. -/
theorem replay_records_action (s s' : ReplayState) (ek : String × String) (ed i : String)
    (key : String × String × String) (v : Verdict) (r : Result)
    (h : replay s ek ed (some key) i v = some (r, s')) :
    lookup key s'.actions ≠ none ∨ r = observation .duplicateEvent := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact Or.inr rfl
    · contradiction
  · simp only at h
    split at h
    · rename_i old hk
      split at h
      · cases h; left; simp [hk]
      · contradiction
    · cases h; left; simp [lookup]

theorem known_action_never_fresh (s s' : ReplayState) (ek : String × String) (ed i : String)
    (key : String × String × String) (v : Verdict) (r : Result)
    (known : lookup key s.actions ≠ none)
    (h : replay s ek ed (some key) i v = some (r, s')) :
    r = observation .duplicateEvent ∨ r = observation .duplicateAction := by
  unfold replay at h
  split at h
  · split at h
    · cases h; exact Or.inl rfl
    · contradiction
  · simp only at h
    split at h
    · split at h
      · cases h; exact Or.inr rfl
      · contradiction
    · rename_i hn; exact absurd hn known

/- B. Structural replay closes the gap without any hash assumption. -/
structure SReplay where
  events : List ((String × String) × Event) := []
  actions : List (ActionKey × BusinessIntent) := []

def MidnightExpress.Event.actionKey? (e : Event) : Option ActionKey :=
  match e.payload with
  | .agent a => some a.actionKey
  | _ => none

def scheck (c : Context) (s : SReplay) (e : Event) : Option (Result × SReplay) :=
  match validate c e with
  | none => none
  | some r =>
    match lookup e.occurrenceKey s.events with
    | some old => if old = e then some (observation .duplicateEvent, s) else none
    | none =>
      let events := (e.occurrenceKey, e) :: s.events
      match e.actionKey? with
      | none => some (r, { s with events })
      | some k =>
        match lookup k s.actions with
        | some old => if old = e.intent then some (observation .duplicateAction, { s with events }) else none
        | none => some (r, { events, actions := (k, e.intent) :: s.actions })

theorem scheck_changed_intent_conflicts (c : Context) (s : SReplay) (e : Event) (k : ActionKey)
    (old : BusinessIntent) (fresh : lookup e.occurrenceKey s.events = none)
    (hk : e.actionKey? = some k) (known : lookup k s.actions = some old)
    (changed : old ≠ e.intent) : scheck c s e = none := by
  unfold scheck
  split
  · rfl
  · simp [fresh, hk, known, changed]

example :
    (match scheck context1 {} event1 with
     | some (_, s1) => scheck ctxR s1 reissued
     | none => none) = none := by decide
