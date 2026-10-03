# Conformance checklist: what the Foundation requires of a MIP and an MPS

Sources (public, in the midnightntwrk/midnight-improvement-proposals repository): README.md, CONTRIBUTING.md, `mips/mip-0001-mip-process.md`,
`mips/mip-template.md`, `mps/mps-template.md`, and the accepted proposals MIP-0002, MIP-0017, MIP-0019 and MPS-0005, MPS-0007, MPS-0043 as precedent.

## A. Process rules (MIP-0001, README)
| # | Requirement | Our status |
|---|---|---|
| A1 | A new MIP is added as `mips/mip-xxxx.md` with literal `xxxx`; the document says `xxxx`; an editor assigns the number. Same for an MPS (number "assigned by editors"). | Drafts used 0020 and 0044. **Fix: use `xxxx`.** |
| A2 | Status of a new MIP is **Draft**; a new MPS is **Proposed**. | Correct. |
| A3 | Resources (diagrams, images, vectors) go in a subdirectory with the MIP's basename (`mips/mip-xxxx/`). | **To do:** package figures and test vectors. |
| A4 | The MIP states how its Specification is versioned (subsection of Specification, or a top-level Versioning section). | **Gap:** envelope versioning exists; no whole-specification statement. Add `### Versioning`. |
| A5 | Pull requests must not include implementation code; code is linked from a repository. | Reference implementation is in this repository's `prototype/`. **Needs a public link:** the prototype is not yet pushed. |
| A6 | A proposal addressing an MPS is listed in that MPS ("Proposed Solutions"); the MIP preamble lists the MPS. | MPS names the MIP; MIP lists the MPS. Keep both. |
| A7 | Editors check: template adherence, clarity, **motivation**, technical soundness, minimum quality. Changes must be well motivated: "adding features has a cost that must be justified by a benefit." | See D. |
| A8 | Moving to Proposed needs a complete document with no later substantive change; community commentary of at least two weeks; editor vote. | Plan for it in Path to Active. |
| A9 | Contributors may use AI tools, but commits must be authored by the responsible human; commits must carry verified signatures. | Human-authored commits only; signing must be set up on the submitting account. |
| A10 | Category is one of Core, Standards, Networking, Governance, Informational. Final status is Active for Core, Standards and Networking. | Standards (the formats, contract interface and client API dominate); state the networking aspect. |

## B. MIP template completeness (`mip-template.md`)
Preamble: MIP, Title, Authors (name and GitHub handle, alphabetical), Status, Category, Created, Requires, Replaces, MPS, License.
Sections in order: Abstract (about 200 words); Motivation; Specification; Rationale; Path to Active (Acceptance Criteria, Implementation Plan);
Backwards Compatibility Assessment; Security Considerations; Implementation; Testing; References; Acknowledgements; Copyright Waiver (template text).
| # | Requirement | Status |
|---|---|---|
| B1 | Specification detailed enough to implement; intended behaviour clear and unambiguous. | Strong on envelope and overlay; **check** Registry contract in Compact and indexer and wallet interfaces for implementability (signatures, state, errors). |
| B2 | Rationale: decisions, reasons, alternatives and why rejected. | Five options with evidence. |
| B3 | Acceptance Criteria are objective milestones. | Must map to measurable experiments and thresholds; **verify one-to-one**. |
| B4 | Backwards compatibility: hard fork? compatibility issues? | No fork; additive. State precisely. |
| B5 | Security: new attack vectors and mitigations. | Threat model and residual risk exist; keep the admission stand-in limit explicit. |
| B6 | Testing: procedures that show it works and does not regress. | Ten scenarios, thresholds; **add test vectors and conformance suite definition**; real-network (devnet) tests are not yet done. |
| B7 | Implementation: which components change, dependencies. | Sidecar, Registry, indexer and wallet changes; upstream libp2p dependency; **be explicit about each repository**. |
| B8 | References and Acknowledgements; Copyright Waiver text exactly as the template. | In job M6. |

## C. MPS template completeness (`mps-template.md`)
Preamble: MPS, Title, Authors, Status Proposed, Category, Created (DD-MMM-YYYY), Requires, Replaces, MIP.
Sections: Abstract (about 200 words); Vision; Problem (factual, evidence-based, solution-agnostic); Use Cases; Goals (measurable where possible);
Expected Outcomes; Open Questions; Recommended MIPs; References.
| # | Requirement | Status |
|---|---|---|
| C1 | Problem section is solution-agnostic and evidence-based. | In job MPS; check that no design is smuggled in. |
| C2 | Goals measurable where possible, outcomes not implementations. | Tie each goal to a figure the experiments can measure. |
| C3 | Recommended MIPs lists this MIP and what else the problem implies. | In job MPS. |
| C4 | Related earlier problem statements (MPS-0005 Part 2, MPS-0007, MPS-0043) are addressed, not duplicated. | Required in both texts. |

## D. Evidence the editors will ask for (design, experiments, research)
| # | Question an editor asks | What answers it |
|---|---|---|
| D1 | Why is this needed and why not use what exists? | Measured Midnight limits (256 B payload, 1 KiB drop, 6 s blocks, fee per transaction), public leakage studies, MPS-0005 Phase 2 scope. |
| D2 | Does it work? | Reference implementation, ten scenarios and thresholds, pilot results; **gap: no run against real Midnight (devnet) with real DUST fees and a compiled Registry contract.** |
| D3 | What does it cost? | Per-event DUST cost, gateway and storage budgets, operator burden; **gap: fee model uses reconciled arithmetic, not a measured devnet fee.** |
| D4 | Is it secure? | Threat model, adversarial scenarios; **gap: admission proof is a stand-in; no audit.** |
| D5 | Is the research sound? | Cited, read works; claims traceable to requirements. |
| D6 | Is it implementable by others? | Normative byte layouts, test vectors, protocol identifiers; **gap: test vectors not yet published.** |
| D7 | What happens next? | Acceptance Criteria, phases, owners. |
