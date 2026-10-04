<!-- Review via agy; selected model: gemini-3.1-pro-high; baseline: f0e3fc6. Recommendations require editorial/factual review. -->

# Product Management Review: Midnight Express Data Model

## Assessment & Strategy

The current Data Model page introduces the core concept of shared meaning effectively but leans too heavily on structural summaries. To successfully onboard integration partners, the copy must shift from abstract architecture to concrete workflow behaviors. Partners need to understand exactly how the model treats missing terms, duplicate actions, and partial data.

We must also align the marketing copy precisely with the v0.2 implementation reality. We must eliminate any ambiguity between the 291 proposed vocabulary terms and the two actually implemented read-only chain slices. We must clearly define the boundaries of the integration: the data model guarantees interpretation, but production authentication, live finality, and external financial execution remain the application's responsibility.

Below are six specific, insertion-ready improvements designed to deepen the quote, payment, and approval stories while remaining strictly bound to the tested evidence.

---

## 1. Clarify Missing Terms and the Cost of Refusal

**Context:** The "ONE QUOTE, TWO DECLARED FORMATS" section mentions that missing terms are refused, but it lacks a concrete example of *why* this is a feature, not a bug. We need to explicitly reference the 35 tested RFQ vectors to show that safe refusals protect the business.

**Placement:** Replace the paragraph directly under the **Agreed RFQ Meaning** result box (starting with "Declared adapters convert...").

**Insertion-Ready Copy:**
> Declared adapters convert the units and perspective, producing deterministic bytes that represent the agreed interpretation. In the 35 tested RFQ vectors across independent Python, Rust, and TypeScript interpreters, only four cases are accepted. The remaining 31 cases represent safe refusals. For example, if a quote arrives with a valid price and quantity but omits an explicit buyer/seller perspective or assumes an unsupported fee convention, the adapter refuses it. It does not guess a default direction. This strictness ensures that a misunderstood format is caught during integration rather than becoming a live business error.

## 2. Enforce Source-Bound Quote Identity

**Context:** Partners often assume that identical prices from different sources can be deduplicated or treated as fungible. We need to clarify that business meaning and cryptographic identity remain distinctly tied to the source.

**Placement:** Replace the first `.section-note` paragraph at the bottom of the **02 / ONE QUOTE** section (starting with "Two encodings have the same...").

**Insertion-Ready Copy:**
> Two encodings only share an intent fingerprint when the complete source-bound intent matches. If Dealer A and Dealer B both offer 100 shares at $123.45, they retain distinct source identities and generate different cryptographic commitments. The protocol does not make independent quotes fungible. Furthermore, the checked quote remains an off-chain observation. The receiving application must still verify the sender's authentication and current business policy before acting; the data model guarantees the interpretation of the price, but trade execution and settlement require their own authority.

## 3. Deepen the Partial Payment Reconciliation Story

**Context:** The "PAYMENT OBSERVATION" workflow description is too brief. Invoice reconciliation is notoriously difficult due to mismatched timelines and partial payments. We need to highlight how the three exact clocks and the amount bounds resolve this ambiguity.

**Placement:** Replace the text inside the **PAYMENT OBSERVATION** article in section **04 / THREE REFERENCE-TESTED PILOT CONTRACTS**.

**Insertion-Ready Copy:**
> ### Explain what was reported.
> A $500 invoice can receive an observation of a $250 partial payment. The payment observation contract strictly bounds this relationship: the reported amount must be positive and cannot exceed the total invoice payable, whether the status is Pending, Final, or Reversed. The contract also enforces a logical timeline using three explicit clocks to track reconciliation. The time the payment took effect (`effectiveAt`) must precede the time it was seen (`observedAt`), which must precede the creation of this observation record (`event.time`). Finality remains a source assertion; this observation neither allocates the funds nor guarantees bank execution.

## 4. Detail the Narrow Sandbox Approval Scope

**Context:** The current "SANDBOX APPROVAL" text vaguely promises "recoverable progress for agent workflows." To set proper expectations, we must define the exact constraints of the sandbox and what the approval actually permits.

**Placement:** Replace the text inside the **SANDBOX APPROVAL** article in section **04 / THREE REFERENCE-TESTED PILOT CONTRACTS**.

**Insertion-Ready Copy:**
> ### Keep approval tied to its action.
> A human approval fixture tightly binds a single WriteReport proposal to its target, input, and execution scope. It commits a specific authority domain and a strict budget window. Validation produces an approved candidate that authorizes exactly one database report-row effect, costing exactly one Step. If an agent attempts to change the target, alter the policy, or replay a consumed action identifier, the contract safely conflicts rather than renewing the approval. The validator strictly returns `executes:false`; genuine production human identity and current permissions require their own enforcement outside the data model.

## 5. Distinguish Proposed Vocabulary from Implemented Slices

**Context:** The "ETHEREUM & SOLANA APPLICATIONS" section introduces 291 vocabulary entries, which reads like massive cross-chain support. We must temper this by explaining the difference between the proposed taxonomy and the two strictly bounded, offline fixture projections currently implemented.

**Placement:** Replace the introductory paragraph of section **06 / ETHEREUM & SOLANA APPLICATIONS** (starting with "The proposed vocabulary inventories 291...").

**Insertion-Ready Copy:**
> The model relies on a proposed vocabulary of 291 common messages—covering queries, token transfers, state changes, and wallet permissions—which guides future event classification and establishes a lifecycle support matrix. However, these are not deployed runtime payload contracts. The implemented read-only slice is deliberately narrow, supporting exactly two offline fixture projections: bounded Ethereum ERC-20 transfers and Solana legacy SPL Token Program TransferChecked events. These projections rely exclusively on supplied static fixtures to verify physical inclusion identity and exact raw amounts. They do not consume live authenticated RPCs, support Token-2022, or verify independent consensus finality.

## 6. Quantify the Effect Boundary and Recovery Routine

**Context:** "Recovery has an effect boundary" is an abstract concept. We have hard data proving the idempotency of the system via rigorous database worker termination tests. Injecting these facts transforms a theoretical architecture claim into a proven engineering baseline.

**Placement:** Replace the paragraph inside the `.midnight-role` block in section **05 / RECOVERY & CHANGE** (under the heading "Recovery has an effect boundary").

**Insertion-Ready Copy:**
> Recovery relies on a strictly bounded effect transaction. In 56 real PostgreSQL checks, four actual worker processes were killed at critical boundaries: after the effect write, before the commit, and surrounding the destination acknowledgement. The recovery routine consistently retained exactly one fixture-authorized report-row effect. Uncertain delivery statuses safely expose an OutcomeUnknown state until reconciled by the original idempotency key. While this proves the local integration agreement, genuine external effects still require the actual destination’s idempotency guarantees rather than relying on the local database.
