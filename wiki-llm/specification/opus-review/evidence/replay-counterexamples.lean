import MidnightExpress
open MidnightExpress MidnightExpress.Examples

/-! Probe A: replay digests are unconstrained by the event.
An approval with a *different* business intent (validUntil shortened, still valid)
is labelled duplicateAction when the caller supplies the same intent token. -/
def eventAlt : Event :=
  { event1 with
    envelope := { event1.envelope with id := "event:agent-2" }
    payload := match event1.payload with
      | .agent a => .agent { a with validUntil := 1791118000 }
      | p => p }

example : eventAlt.intent ≠ event1.intent := by decide
example : (validate context1 eventAlt).isSome = true := by decide

def afterFirst : ReplayState :=
  match check context1 {} event1 "evt-1" "intent-token" with
  | some (_, s) => s
  | none => {}

-- Same caller-supplied intent token for structurally different intents.
example : (check context1 afterFirst eventAlt "evt-2" "intent-token").map (·.1.verdict) =
    some .duplicateAction := by decide
-- Conversely, identical intents with different tokens conflict (false rejection).
def eventRetry : Event :=
  { event1 with envelope := { event1.envelope with id := "event:agent-3" } }
example : eventRetry.intent = event1.intent := by decide
example : check context1 afterFirst eventRetry "evt-3" "other-token" = none := by decide

/-! Probe B: quotes have no logical-action identity; a re-sent quote with a new
occurrence ID is a second fresh `.quote`. (Python Harness behaves the same.) -/
def quoteAgain : Event :=
  { event0 with envelope := { event0.envelope with id := "event:rfq-2" } }
def afterQuote : ReplayState :=
  match check context0 {} event0 "q1" "qi" with
  | some (_, s) => s
  | none => {}
example : (check context0 afterQuote quoteAgain "q2" "qi").map (·.1.verdict) =
    some .quote := by decide

/-! Probe C: `lookup` is first-match; duplicate keys in a context list shadow.
Python contexts are JSON objects with duplicate keys rejected, so this is a
well-formedness assumption the Lean Context does not state. -/
def shadowed : Context :=
  { context0 with sources :=
      ("urn:mpe:source:dealer", ⟨.humanApprover, "party:dealer"⟩) :: context0.sources }
example : validate shadowed event0 = none := by decide
def staleProposal : Proposal := { environment := .sandbox, operation := .writeReport, target := "x", inputDigest := "", budget := { value := { coefficient := 5, scale := 0 }, unit := .step }, expires := 0 }
def shadowedRevoked : Context := { context1 with proposals := ("action:demo", staleProposal) :: context1.proposals }
example : validate shadowedRevoked event1 = none := by decide

/-! Probe D: `proposalDigest` is a context function; the only constraint is
equality with whatever it returns. A constant function makes the digest field
an arbitrary fixed string; the approval is still accepted. -/
def constDigest : Context := { context1 with proposalDigest := fun _ _ => "anything" }
def eventConst : Event :=
  { event1 with payload := match event1.payload with
      | .agent a => .agent { a with proposalDigest := "anything" }
      | p => p }
example : validate constDigest eventConst = some (observation .candidate) := by decide
