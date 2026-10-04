# Implementation and delivery prose review

Baseline: `04a2dc0`. Profile: none. Existing drafts receive a Gottlieb structural edit followed by a Le Guin cadence pass, using Inkwell's reader-first guide. Line references below identify the baseline. The graph query for “Clutter” returned the simplicity rule and its connection to specific detail; no missing source tile was used as evidence.

## Critical findings

1. **Stale scope contradicts current evidence.** `docs/product-requirements/prototype-sprints.md:75` says “Python-only” and lists adapters, cross-language agreement and durable processing as future work. The v0.2 evidence document describes independent RFQ interpreters and an actual PostgreSQL sandbox. Explain that finite evidence before the sprint plan, preserving the uncompleted transport/admission/finality integration.
2. **Activity counts as authority.** `website/README.md:3,11,15,31,35,39,43,47,51,55` foreground assignment, review and test totals. The maintenance reader needs source files, build/publish commands, behavioral checks and claim boundaries. Preserve the old account separately; replace the accumulation with a maintenance guide. `website/dist/implementation.html:3` repeats “35 RFQ vectors”, “56 recovery checks” and “28 fixture checks” where the public reader needs the tested behaviors and fixture limits.
3. **Historical evidence presented as a present limit.** `umbradb-recovery.md:9` says no integration ran, without distinguishing the original 0.9.5 study from the later sandbox. Retain the original unrun crash check and advisory-check scope, then link the later evidence with its separate pinned baseline and report-row limitation. `proposed-stack.md:3,11` likewise needs to distinguish the selected full architecture from local composition already demonstrated.

## Important findings

1. **Voice slips into the workshop.** `docs/product-requirements/README.md:3,10,12,14`, `gossipsub-signal-option.md:5`, `semaphore-membership-option.md:5`, `requirements-fit-and-open-source.md:5,94`, and `prototype-sprints.md:83` use reviewers and synthesis as the organizing account. Keep the linked sources but introduce documents by the decision they inform.
2. **Disconnected sprint lists.** `prototype-sprints.md:9,27,45` and `implementation.html:4` state hypotheses without explaining how the preceding result enables the next experiment. Add short causal transitions; keep the build tasks and acceptance gates as useful lists.
3. **Staged contrasts and repeating conclusions.** `requirements-fit-and-open-source.md:3,77,90`, `semaphore-membership-option.md:3,39`, and `umbradb-recovery.md:59` repeatedly close on “not a complete system” after detailed limitations. State each component's responsibility directly and retain concrete privacy, authorization and persistence limits where they matter.
4. **Fragment-heavy component account.** `proposed-stack.md:5–16` and `implementation.html:3` introduce responsibilities as noun lists. Explain how transport, local interpretation, admission, recovery and business authority fit together before the reference tables.

## What works

The price-convention example (`prototype-sprints.md:17`) connects the model to an actual trade. The admission paragraph (`:65`) preserves an unusually useful distinction between the 4096-byte ceiling, fixed 512-byte fixture slot and a project-selected p99 policy. The detailed recovery table (`umbradb-recovery.md:13–22`) states exact public APIs and the nested-transaction hazard. Preserve these details and the useful comparison tables.

## Verdict

These documents contain substantial technical evidence and careful boundaries, but mix a changing reference implementation with earlier feasibility studies and a running account of reviews. Rewrite the introductions, connections and decision passages; retain exact obligations, technical tables and acceptance steps. Consolidate the website history into a separate record so its README can guide maintenance.

## Protected claim inventory

- All HTML IDs, attributes, controls, anchors, asset paths and existing citations/link targets; all code blocks, signatures and requirement identifiers.
- Proposed three-sprint status; two-week assumption; no staffing/start commitment; genuine admission, sealed wire, signing, finality and partner evidence remain gates.
- v0.2 finite unsigned reference: exact meaning/canonical intent, RFQ cross-language agreement, immutable contracts, refusals and `executes:false`; separately fixture-authorized PostgreSQL WriteReport recovery. No financial, blockchain or arbitrary tool execution claim.
- Fixed wire classes; no implicit fragmentation; `roundUp64(104 + proofBytes) <= 4096`, 10,000 genuine proofs, one core of a 4-vCPU VM, 10-ms gate and explicit p99 policy provenance; existing 512-byte fixture distinction.
- Local recognition, clear salt/nonce/tag prefix, whole-shard reception, no recognition-dependent controls; launch symmetric profile has no broadcast forward-secrecy or ingress-anonymity claim; mobile budget/discovery constraints.
- Semaphore identity/witness patterns plus RLN-style committed credits and recoverable abuse evidence; compatibility unverified, no stacked proof, no scope reset by EID/root changes; Registry authoritative; concurrent ingress is not globally serialized quota.
- Separate business signatures, finality/replay and CON-060 anchored-plaintext binding; Signal/MLS authentication is insufficient; Signal experiment is optional and off-chain first.
- Umbra inspected commit/package/source evidence; original Docker crash tests not rerun; current sandbox separately scoped; public transaction handle and no nested saveAndAdvance; one trusted writer, no HA/replicated retention inference; encryption/erasure/freshness and destination idempotency/reconciliation requirements.
- Original requirement inventory, source hashes, quantified performance/mobile parameters, license qualifications and upstream support caveats remain evidence from the source studies, not newly verified external claims.

## Historical website account

The complete baseline [website README](implementation-before/website-readme.md) preserves previous assignments, review totals, checks, image-generation provenance, deployment history and Humanizer provenance. Relative link targets have been rebased from the original `website/` location so the archive remains navigable. The current website guide retains actionable review links and deployment instructions.


## Applied edit and cadence findings

The rewritten introductions explain the component roles and the dependency between sprints. The old Python-only claim now points to the finite v0.2 reference and the separate fixture-authorized PostgreSQL sandbox. Umbra's original source assessment retains its pinned 0.9.5 baseline and unrun Docker crash check; the later sandbox is separately identified by commit and scope. No production gate was promoted to completed work.

A cadence pass joined adjacent short sentences in the implementation introduction and replaced repeated “The…” openings where the subject or relationship offered a clearer start. The website maintenance guide now gives direct instructions instead of repeating “After…” clauses. Necessary technical lists, the price example, public API details and privacy/authorization qualifications remain.

The first measured revision displaced repetition into sentence openings and fronted prepositional phrases; see [initial diagnostic](implementation-displacement-initial.txt). The repaired draft's [displacement diagnostic](implementation-displacement.txt) exits 0 at the default 25% floor. Sentence-length variance is 46.6 before and 40.8 after under `compute_kpis.py`; these technical-document observations are not a prose-quality score. Full panels: [before](implementation-before-kpis.json), [after](implementation-after-kpis.json).

Measurement uses the owned files only, in the file order listed in the assignment: implementation HTML, website README, product README, prototype sprints, stack, requirement fit, Signal, Semaphore and Umbra. HTML extraction retains paragraph and list-item text without tags/navigation. Markdown extraction removes fenced code, headings and table rows, keeps ordinary paragraphs/list content, and replaces links with their visible labels. The same extraction is applied to baseline `04a2dc0` and the revision. Files are named `ch01.md` through `ch09.md` for the displacement tool. Commands:

```bash
python3 /home/hoskinson/Projects/inkwell/narrative/metrics/displacement.py /tmp/inkwell-implementation/before /tmp/inkwell-implementation/after
python3 /home/hoskinson/Projects/inkwell/RSI/metrics/compute_kpis.py /tmp/inkwell-implementation/before.md
python3 /home/hoskinson/Projects/inkwell/RSI/metrics/compute_kpis.py /tmp/inkwell-implementation/after.md
```

The protected-content comparison found identical HTML tag/attribute sequences, retained original Markdown link targets, unchanged fenced technical code and unchanged requirement-ID sets. The website README adds its regeneration command while retaining its publication command. `git diff --check` passed. The parent run owns the fresh-reader check and browser validation; neither is claimed here.
