import Lean
import MidnightExpress
open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Quot.sound, ``Classical.choice]
  let mut count : Nat := 0
  let mut bad : Array (Name × Array Name) := #[]
  for (name, info) in env.constants.map₁.toList do
    if (`MidnightExpress).isPrefixOf name && !name.isInternal then
      if let .thmInfo _ := info then
        count := count + 1
        let axs ← liftCoreM (collectAxioms name)
        if axs.any (fun a => !allowed.contains a) then bad := bad.push (name, axs)
  logInfo m!"theorems scanned: {count}; outside allowed set: {repr bad.toList}"
