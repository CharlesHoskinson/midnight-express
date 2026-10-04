# Implementation page experience review

Recommend a separate `website/dist/implementation.html`, reached by an **Implementation** link in the existing main navigation. Treat “tab” as a normal page link: use `aria-current="page"`, not ARIA tab roles, and do not force a new browser window. On Implementation, existing section links point to `index.html#…`; the brand returns to the overview. Preserve the current visual language and make this page useful with JavaScript disabled.

## Reading order and copy

1. **Three proposed prototype sprints. RFQ first; prove recovery; reuse the core.** Add immediately: “Three two-week timeboxes are a planning assumption, not a launch commitment. The outcome is a bounded reference prototype and evidence for the next decision.” Provide anchor links to shared meaning, each sprint, admission work and remaining gates.
2. **Different systems, the same understood meaning.** Explain the small shared core and strict domain profiles before the sprint cards. Show a short vertical flow: participant format → explicit deterministic adapter → pinned RFQ/invoice/agent profile → shared processing core → application policy. Keep the arrow flow readable as ordinary ordered text.
3. Three sequential sprint articles with permanently visible **Hypothesis / Build / Demo / Required evidence / Decision**. Use one native `<details>` per article for entry conditions and negative scenarios. A reader must understand the proposed outcome without opening anything.
4. A distinct admission track and production-gates section; then evidence/source links. Admission starts in Sprint 1 and stays visible through Sprint 3. Do not visually present it as a fourth sprint or a completed capability.

### Shared meaning: recommended wording

“The shared core identifies an update and the contract that gives it meaning. Each workflow adds a small, closed profile: a quote, a payment observation or a bounded approval. Explicit adapters map known participant formats into those profiles. Unknown versions, ambiguous units and unsupported terms are rejected rather than guessed.”

Use the concrete quote: **100 shares × USD 123.45 per share = USD 12,345.00**, then explain who owes shares and who owes dollars. Sender identity does not change buyer/seller meaning. A proposed independent buyer/dealer mapping comparison makes interoperability assessable; two serializers of the same structure do not.

A compact “What is pinned?” detail can name schema, rules, reference validator and profile manifest digests. Keep manifest syntax and coefficient/scale JSON out of the main story. Say that pinning makes the selected contract explicit; it does not establish sender authority. All modeled business fields remain inside the encrypted message body; the model adds no outer routing fields or transport changes. CloudEvents-compatible structure and selected CDM/UBL concepts are vocabulary reuse, not standards certification. No live schema discovery, RDF reasoning or LLM interpretation decides meaning.

## Sprint copy to implement

| Sprint | Hypothesis | Build | Demo | Required evidence and decision |
| --- | --- | --- | --- | --- |
| **1 — Understand and exchange a quote** | Approved participants can agree on the same supported economic terms and record an explicit off-chain acceptance. | Buyer plus two dealers; independently specified buyer/dealer mappings; closed RFQ profile; signed request/offer/accept policy; real transport and local recognition. Start genuine admission and Midnight capability spikes immediately. | Compare two valid offers and accept one exact revision. Show rejection of ambiguous units, unauthorized sender and expired offer; an irrelevant receiver cannot decrypt. | Reproducible scenario, obligation/hash comparisons, role/expiry negatives and packet/topic inspection. Show admission feasibility separately; a mock workflow pass cannot pass anonymous admission. Fix meaning/display errors before broadening. |
| **2 — Recover the same accepted quote** | Duplicates, restart and reconnect can preserve one committed local outcome and its explicit acknowledgement. | Durable authenticated inbox, RFQ state, dedup, acknowledgement outbox and cursor within one verified transaction boundary; bounded retries, gap handling and encrypted quarantine. | Kill the host around commit and acknowledgement, reconnect and replay. Show one accepted revision, an expired retry, a gap and an isolated failing handler. | Fault matrix before commit, after commit before acknowledgement and during retry; concurrency, restore and expiry evidence. Report synthetic recovery measurements. Reuse only after transaction/fault gates pass; local atomicity does not prove exactly-once external effects. |
| **3 — Reuse without losing authority** | The same core can serve invoice observations and bounded human approvals while each workflow keeps its own rules. | One invoice fixture and sandbox ERP posting with destination idempotency/reconciliation; one exact human-approved sandbox action. Keep invoice and agent fields in their closed profiles. | Replay a payment observation without a second posting; inject destination success before local confirmation. Approve one action, then reject changed target, excess budget, expiry and replay. Restart both workflows. | Shared recovery harness, source labels, authority negatives, destination reconciliation and measured adapter effort. Disposition admission feasibility and produce a constrained pilot decision pack. Repeat blocked work where necessary; this is not a production release. |

Use “proposed” on every sprint header. Do not put green completion ticks on future build items. Show customer baseline collection as work: quote turnaround, handling minutes, comprehension, rework and integration effort. Internal fixtures support observations; they cannot support customer savings claims.

## Evidence distinctions must be visible

Place a small current-status block above the sprint sequence, with plain text labels rather than color alone:

- **Designed:** reviewed architecture, closed profiles and sprint acceptance plan.
- **Reference-tested:** bounded Python model behavior against unsigned events and separately supplied trusted test context. Link to `model/README.md`; any count or pass claim needs a matching run/report. These tests check selected meaning, canonicalization and fixture duplicate rules.
- **Proposed runtime work:** signed participants, actual adapters, transport integration, durable recovery and sandbox execution in the sprint plan. The Python validator executes no action; cryptography, finality, authenticated authority, durable atomic replay/effect state and Rust/TypeScript agreement remain pending.

The present model has only quote, payment-observation and approval event types. Request/accept, invoice posting and action execution in the sprint demos are proposed additions, not existing model capabilities. Keep the proposed wider RFQ profile name separate from the installed `rfq.v0.1` fixture contract. Never imply its unsigned intent hash is a verified signature, its “Final” observation is settlement proof, or its approval result executes a capability.

Admission detail should distinguish genuine proof, secret-readable stand-in, compiler/simulator result and actual finalized-root integration. Display unresolved feasibility as unresolved, including exact wire/slot fit and performance measured on the specified host. The closing boundary names replicated opaque retention, independent operator receipts, network/load evidence, hardened operations and cryptographic review. Settlement needs its separate business-authority/replay/CON-060 gates. No payment execution or unrestricted agent execution is in scope.

## Interaction and acceptance checks

Use native anchors for the contents and native `<details><summary>` for deeper material. One `h1`, ordered `h2` sections and sprint `h3`s; unique stable fragment IDs; skip link to focusable main. Links to documents need descriptive labels and a visible underline. Retain current mint focus outline, sufficient contrast and reduced-motion behavior. Avoid copying the architecture's button/selected-panel pattern: the sequence is linear reading, not a simulated dashboard.

Use fluid single-column articles with a readable text measure around 65–75 characters. A small desktop summary grid is optional; switch to stacked blocks before text becomes cramped. Set `min-width:0`, allow navigation and long source labels to wrap, and avoid fixed heights, sticky detail panes and forced `<br>` headings. Prefer rem-based type and padding; never shrink body copy to fit.

Check at 320 CSS pixels and with text enlarged to 200%: every heading, nav link, evidence label and summary remains visible; no horizontal page scrolling or clipped contents; details remain keyboard operable; focus is visible. Verify no-JavaScript reading, fragment navigation, keyboard order and reduced motion. Essential status and scope cannot depend on hover, color, an expanded detail or a diagram.

Sources reviewed: [sprint sequence](sequence.md), [RFQ product review](rfq-product.md), [bounded model](../../model/README.md), and the current `website/dist/index.html` / `styles.css`. This review proposes page content and layout; it asserts no newly implemented runtime or test result.
