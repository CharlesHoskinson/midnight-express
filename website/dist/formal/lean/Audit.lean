import Lean
import MidnightExpress

open Lean Elab Command

/-- Audit every declaration owned by a project module, even outside its namespace.
The audit command itself lives in this separate tooling module. -/
elab "#audit_project" : command => do
  let env ← getEnv
  let mut count : Nat := 0
  for (name, info) in env.constants.toList do
    let owned : Bool := match env.getModuleIdxFor? name with
      | some idx => (`MidnightExpress).isPrefixOf env.header.moduleNames[idx.toNat]!
      | none => false
    if owned then
      count := count + 1
      if info.isUnsafe then
        throwError "project declaration {name} is unsafe"
      if let .axiomInfo _ := info then
        throwError "project declaration {name} is an explicit axiom"
      let axioms ← collectAxioms name
      let unwanted := axioms.filter (fun a => a != ``propext && a != ``Quot.sound)
      unless unwanted.isEmpty do
        throwError "project declaration {name} has forbidden proof dependencies: {unwanted}"
  if count == 0 then throwError "project axiom audit found no declarations"
  logInfo m!"PROOF_AUDIT_OK: {count} project declarations; allowed axioms: propext, Quot.sound"

#audit_project
