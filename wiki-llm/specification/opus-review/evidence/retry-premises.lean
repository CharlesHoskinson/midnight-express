import MidnightExpress
open MidnightExpress MidnightExpress.Examples

/- Review of proposed theorem premises, not a change to the specification.
A successful *duplicate occurrence* alone need not bind an action in an arbitrary
ReplayState. A run theorem must start from empty/coherent state, or require that
the first verdict was a fresh candidate and preserve action bindings. -/
def occurrenceOnly : ReplayState :=
  { events := [(event1.occurrenceKey, "event-token")], actions := [] }
def laterOccurrence : Event :=
  { event1 with envelope := { event1.envelope with id := "event:review-retry" } }
example : laterOccurrence.intent = event1.intent := by decide
example : check context1 occurrenceOnly event1 "event-token" "intent-token" =
  some (observation .duplicateEvent, occurrenceOnly) := by decide
example : (check context1 occurrenceOnly laterOccurrence "other-event-token" "intent-token").map
  (fun result => result.1.verdict) = some .candidate := by decide
