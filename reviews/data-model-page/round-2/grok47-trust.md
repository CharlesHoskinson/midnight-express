<!-- Review via Grok CLI; selected model: grok-4.7; baseline: f0e3fc6. Recommendations require editorial/factual review. -->

# Trust and operations review: data model page

The page states its limits, usually in a note under the section. A reader still has to connect them. The gaps are operational: how meaning, source evidence, permission, and effect come apart; what current authority is; what a finality label carries; and what happened when a worker died or a destination acknowledgement was uncertain. Seven insertions follow.

## 1. Ask four questions in the introduction

**Place.** After the paragraph that begins “A private message becomes useful,” before the version line.

**Reason.** Later stories can stay specific.

**Insert.**

An operator should be able to separate four questions on every event. Which installed contract assigned the meaning? What evidence did the named source supply? Who may act on that reading under current permission? What effect is already committed? The reference answers the first question for three narrow profiles: whole-share US-dollar quotes, payment observations, and a sandbox report approval. Source assertions stay with the evidence. Permission is a further check. Validation success returns `executes: false`. The one measured effect is a fixture-authorized report row in local PostgreSQL.

## 2. Teach the quote as an observation

**Place.** In “Quote example,” replace the note beginning “Two encodings have the same intent fingerprint.” Keep the coefficient disclosure.

**Reason.** The $12,345 case can carry acceptance, refusal, and the authority handoff.

**Insert.**

Format A is the buyer purchasing 100 shares at $123.45 a share. Format B is the dealer selling those shares at 1,234,500 cents per 100, and no fees. Reviewed adapters convert units and perspective. Acceptance requires the price and the cash total to agree exactly: 100 × $123.45 = $12,345. A missing currency, a contradictory total such as 1,234,501 cents, or any fee is refused. Independent Python, Rust, and TypeScript interpreters share the RFQ corpus of 35 vectors: 4 accepted and 31 safe refusals, with no accepted disagreement. The intent fingerprint covers the complete source-bound content, so another dealer with the same price keeps another fingerprint. The accepted output is an off-chain observation of an unsigned fixture. A decision to trade waits on source authentication and current policy. Execution and settlement are further authorities.

## 3. Narrate Pending, Final, and Reversed

**Place.** In “Pilot workflows,” after the three cards and before the note on RFQ-only cross-language agreement. Leave that note.

**Reason.** The status words need a single invoice story.

**Insert.**

A source reports $250 against a $500 invoice. Pending means the source still treats the payment as open. Final means the source treats it as complete. Reversed means the source treats it as undone. Each observation needs a positive amount no greater than the $500 payable. Effective time is when the source says the payment took effect, observed time is when it was seen, and record time is when this event was created. Those three instants and the trusted intake clock must stand in that order. A later event may record a reversal of the same payment. The profile explains the report. Applying cash, marking the invoice paid, and moving money are other work. Final here is the source assertion, with matching fixture evidence beside it.

## 4. Show the approval grant that exists today

**Place.** In the same section, after the payment paragraph.

**Reason.** Readers need the fixture capability that turns a candidate into one row.

**Insert.**

The fixture names a person and binds one WriteReport proposal: one target, one input, one authority domain, one execution scope, one budget window, one expiry. Validation stops at a candidate and returns `executes: false`. The host writes only when the test supplies a fixture capability for that scope. It checks that capability before the write and again inside the PostgreSQL transaction. The host reserves the approved maximum, charges one Step for the single report row, and releases unused capacity. A changed target conflicts with the action already consumed. The person’s name travels with the proposal. The capability is trusted test data supplied by the harness.

## 5. Say what the installed fingerprint authorizes

**Place.** Replace the paragraph in the box “An exact agreement.”

**Reason.** Operators need to see how a commitment becomes the meaning in force.

**Insert.**

A contract commitment is the fingerprint of the agreed definitions and rules, and it selects which meaning an event is checked under. The sender is authenticated elsewhere. The reference installs meaning through an operator-reviewed allowlist of exact commitments. Unknown commitments are refused, with no default and no downgrade. v0.1 stays available so historical results can be reproduced, and the current loader will not dispatch it. No live workflow has moved. The meaning in force today is the allowlist.

## 6. Recount the four worker kills and the uncertain reply

**Place.** Replace the body under “Recovery has an effect boundary.” Keep the heading.

**Reason.** This is the crash and acknowledgement story the notes only name.

**Insert.**

The host commits the report row and the progress that records the action as consumed in one PostgreSQL transaction. The suite uses PostgreSQL 17.11 and the reviewed Umbra checkout `f662822765247f0da553347c9819f958a1992d28`. It kills four worker processes: after the effect writes, before commit, after commit and before acknowledgement, and after a separate destination fixture commits. Across 56 PostgreSQL checks, recovery still shows one fixture-authorized report-row effect. The destination acknowledgement is its own transaction and only a fixture. A kill after that fixture commits leaves Dispatching and OutcomeUnknown until reconciliation by the original idempotency key. Reconciliation accounts for that key. A further effect waits on new authorization. The far side is local fixture state. Global exactly-once delivery stays a property of the real destination a deployment eventually uses.

## 7. Keep finality a source label, and separate the vocabulary from the projections

**Place.** In “Chain events,” replace the note beginning “291 entries are proposed vocabulary.” Leave the two column summaries.

**Reason.** Finality, re-inclusion, and the vocabulary count belong in one explanation.

**Insert.**

A supplied ERC-20 receipt projects a transfer in raw uint256 units, including a zero amount and the maximum amount, at its physical log position. A later removal of the log is an invalidation, and the earlier observation remains in the journal. Re-inclusion on another branch receives a new physical location. Several deliveries of one inclusion become one fact, while two inner transfers remain two facts. For legacy SPL TransferChecked, success is instruction-level evidence. A caught inner failure stays a failure even when the outer transaction succeeds. Ethereum labels such as safe and finalized, and Solana labels such as processed, confirmed, and finalized, are stored as the fixture source’s assertions. At a cutoff, the journal shows what that observer knew. A conflict between commitment assertions is recorded as a gap. Permission to release funds is a separate decision. Arrival on a destination chain is a separate observation.

The 291 entries are a proposed vocabulary of future messages. Two read-only projections are implemented, both from supplied fixtures: the ERC-20 slice, and legacy SPL Token Program TransferChecked. Token-2022 remains outside that slice. Live authenticated RPC and independently checked finality remain promotion gates.

**Leave.** Keep the evidence cards, 35 RFQ vectors, 28 fixture checks, and 56 PostgreSQL checks, plus the note under them on production authentication, live finality, and uncollected baselines.
