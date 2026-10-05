import Lean
import MidnightExpress
open Lean Elab Command
elab "#audit_all" : command => do
  let env ← getEnv
  let mut bad : Array (Name × Array Name) := #[]
  let mut count : Nat := 0
  for (name, _) in env.constants.toList do
    if (`MidnightExpress).isPrefixOf name && !name.isInternal then
      count := count + 1
      let axs ← collectAxioms name
      let extra := axs.filter (fun a => a != ``propext && a != ``Quot.sound)
      if !extra.isEmpty then bad := bad.push (name, extra)
  logInfo m!"audited {count} MidnightExpress declarations; axioms outside propext/Quot.sound: {bad.toList}"
#audit_all
