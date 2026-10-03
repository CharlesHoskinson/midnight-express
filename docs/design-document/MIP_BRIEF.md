# Brief for the Midnight Improvement Proposal (final section of the design document)

The proposal and the system are named **Midnight Express**. Use that name throughout (STYLE.md, 'The name').

The last section of the document is a Midnight Improvement Proposal (MIP) for the private event bus. It follows the MIP template used by the
Midnight Foundation's improvement-proposals repository (`mips/mip-template.md`; read it, and read MIP-0002, MIP-0017 and MIP-0019 as models
of tone and depth; MPS-0005 and MPS-0007 as the problem statements it relates to). It is a specification that a Midnight engineering team could
implement and that reviewers could accept or reject.

## Preamble (fixed)
```
MIP: "xxxx"
Title: Midnight Express: Private Event Delivery over a GossipSub Overlay with Ledger Anchoring
Authors:
  - Charles Hoskinson (@CharlesHoskinson)
Status: Draft
Category: Standards
Created: 2026-10-02
Requires: MIP-0002, MIP-0019
Replaces: none
MPS: MPS-0005, MPS-0007, MPS-xxxx (Private Events for Contracts, Agents and Wallets)
License: Apache-2.0
```

## Sections, in the template's order
Abstract; Motivation; Specification; Rationale; Path to Active (Acceptance Criteria, Implementation Plan); Backwards Compatibility Assessment;
Security Considerations; Implementation; Testing; References; Acknowledgements; Copyright Waiver (the template's text).
The Specification has these subsections: Terminology and conventions; Event envelope and sealing; Overlay protocol; Ledger interface; Consumer interface.

## Ownership (one drafter per part; do not write another part's content, cross-refer by section name)
| Part | Drafter | Content | Words |
|---|---|---|---|
| M1 | Opus | Abstract, Motivation, Rationale, Backwards Compatibility Assessment | 2,000 |
| M2 | Sol | Specification: Terminology and conventions; Event envelope and sealing | 2,500 |
| M3 | Sol | Specification: Overlay protocol | 2,500 |
| M4 | Opus | Specification: Ledger interface; Consumer interface | 2,500 |
| M5 | Sol | Security Considerations; Testing | 2,200 |
| M6 | Opus | Path to Active; Implementation; References; Acknowledgements; Copyright Waiver | 1,500 |

## Rules for the MIP
- Normative language per BCP 14 (RFC 2119 and RFC 8174): MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, in capitals, only in normative sentences.
- Every normative statement should be traceable: cite the requirement identifiers from Appendix A in parentheses, for example (MPE-FMT-001, MPE-FMT-050).
  Use the reconciled prototype values as the initial parameters and say where production values differ (FACTS.md, Appendix A.1).
- Byte layouts as tables with offsets and lengths; state machines or outcome tables where behaviour branches (Accept, Ignore, Reject); exact protocol
  identifiers; message formats.
- Be honest about what is not specified: the zero-knowledge admission proof system is a profile selected by a follow-up; the prototype uses a
  stand-in whose secrets relays can read, which is acceptable for devnet and testnet only. State that in the Specification and in Security Considerations.
- State what changes in Midnight (nothing in the node; a Registry contract in Compact; indexer and wallet additions) and what does not.
- Relate to the existing documents: MPS-0005 Part 2 plans on-chain private events (typed events with private fields and topic filtering); explain when
  that route and this one apply and how they compose. MPS-0007 (node-side visibility of ledger events) is a dependency for anchors and the fallback.
- Same voice and prohibitions as STYLE.md (no trace of how the document was made, no em dashes, no filler). Citations of literature use `[@key]`; the
  MIP's References section lists the specifications and proposals it depends on by name and link, and the works it relies on by key.
- Headings use `##` for template sections and `###` for subsections. Do not write the preamble block (the build inserts it) and do not number headings.

## Conformance (added after the first drafts began)
Also satisfy MIP_MPS_CHECKLIST.md in this folder. In particular: the MIP number and the MPS number are the literal `xxxx` (editors assign numbers); the MIP states how the
Specification is versioned (`### Versioning` under Specification); implementation code is linked, not included; resources go in a subdirectory named after the MIP; every
Acceptance Criterion is objective and maps to an experiment and a threshold; the Specification is implementable (state, signatures, errors).
