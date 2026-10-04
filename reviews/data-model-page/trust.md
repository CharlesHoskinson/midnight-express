# Data Model page review — trust and readiness product manager

Reviewed the active model README, recommendation implementation status, positioning/workflow reviews and saved interoperability, recovery, chain and measurement evidence. This review recommends public prose and claim boundaries; it introduces no new implementation or external research.

## Recommendation

Explain trust as a sequence of decisions, not a wall of caveats. The page should make three questions easy to answer: Do we agree on the message's meaning? Do we trust its source and evidence? Is this particular action permitted now? The reference implements bounded checks for the first question and a fixture-authorized local prototype for the third. Those distinctions should appear where the reader encounters the relevant capability, with one compact readiness section collecting the next gates.

The strongest credible claim is shared, reviewable meaning for an explicitly supported workflow. Do not turn successful parsing, matching hashes, a source's Final status or a local database transaction into authority over an external payment or chain.

## Recommended section: Meaning, evidence and permission

**Agree on meaning.** A workflow contract checks required terms, exact units, roles, status and expiry. An unsupported format or an incomplete declaration is refused. A successful check produces a candidate for the application to consider.

**Check the source and evidence.** A matching commitment lets applications identify the exact contract and intent. Authentication must separately establish who supplied the message and whether its supporting evidence is trusted. A payment source reporting Final is still making a source assertion.

**Authorize the action.** A permitted action must match its target, scope, policy, budget and expiry when it is performed. The sandbox rechecks fixture permission inside the transaction that writes its report row. Validation itself never performs the business action; its result explicitly carries `executes:false`.

Placement: use three short cards or a small sequence after the pilot workflow examples. Avoid an arrow from “valid message” directly to “settled payment.”

## Recommended section: Evolve without rewriting history

Each workflow agreement has an exact, immutable identity. Changing its meaning creates a new contract rather than quietly changing how an old message is interpreted. Applications select an installed, supported contract; an unknown contract is refused instead of downgraded or filled with default terms.

Semantic contracts and implementation releases have separate identities. A software change that preserves the agreed rules can be reviewed as an implementation change; a change in business meaning needs a new agreement. The v0.1 release remains available for historical review, including its known defects, and the current loader cannot activate it for new work.

Small supporting disclosure: The reference verifies locally installed bundles and compares exact supported commitments. Authenticated distribution and migration of live workflows are deployment work still to be validated.

Use “old meanings stay identifiable” rather than “automatic backward compatibility.” Coexistence is an explicit installation decision, not a promise that every old message can drive a current action.

## Recommended section: Shared meaning stays inside the private message

The common event fields and workflow data remain inside the proposed encrypted Midnight Express message body. The data model does not require publishing a quote, invoice or approval as a public schema lookup. Contract selection uses installed resources rather than fetching an arbitrary URL supplied in a message.

Privacy remains a property of the complete system: transport, authorized evidence access and retention must be validated together. The data-model reference does not establish that encrypted network delivery or permissioned retrieval has already been deployed.

Placement: keep this beside the three-layer description. Do not claim the reference offers implemented end-to-end encryption, anonymous membership or private chain evidence retrieval.

## Recommended section: What the evidence shows today

**Three narrow reference profiles.** The v0.2 implementation supports an off-chain quote observation, an invoice payment observation and approval of one sandbox report-writing operation. These profiles deliberately specify their supported terms instead of accepting every currency, fee, tool or accounting convention.

**Independent agreement for RFQ.** Python, Rust and TypeScript implementations were compared on 35 synthetic quote vectors: four accepted cases agreed, and 31 cases were refused. Two declared source-format adapters were exercised in 15 cases. This is finite conformance evidence for RFQ, rather than an error rate measured across all domains or live market traffic.

**Recovery tested on a real database.** The Umbra/PostgreSQL sandbox passed 56 checks, including four actual worker kills. Its effect was one database report-row write under fixture permission. A lost acknowledgement from a separately committed destination fixture remained uncertain until reconciliation; the test did not execute an external payment or arbitrary agent tool.

**A planning vocabulary with bounded chain support.** The catalog contains 291 proposed Ethereum/Solana entries. Executable chain support currently covers read-only ERC-20 transfer observations and legacy SPL TransferChecked observations, tested in 28 fixture checks. Native finality assertions are supplied evidence, and the journal preserves invalidations and gaps. These are not 291 deployed runtime contracts or independently verified live-chain finality.

**Customer value still to measure.** The intended benefits are a clearer integration agreement, fewer opportunities for silent reinterpretation and reviewable recovery. Partner engineering hours, correction rates, turnaround and ROI have not yet been measured.

Suggested presentation: four compact evidence cards with the scope in the same card as the number. Keep customer value as prose below the cards rather than introducing unmeasured headline percentages.

## Recommended section: Next promotion gates

The next pilot should establish authenticated sources and approvals, authorized evidence retrieval, live-chain decoder/finality policy and integration with the full encrypted protocol. Real partner formats and operational baselines should then test whether explicit workflow contracts reduce integration effort and manual corrections. External actions require the destination's own verified idempotency and reconciliation behavior.

This paragraph describes work needed to promote the local reference, not completion of the three proposed protocol sprints. Link to the Implementation tab for the sprint plan and technical evidence.

## Claim edits to enforce during page review

| Avoid | Prefer |
| --- | --- |
| “Three implementations verify our entire data model” | “Independent Python, Rust and TypeScript RFQ implementations agree on the synthetic test corpus.” |
| “Zero errors” | “Zero accepted disagreements across these 35 RFQ vectors.” |
| “291 supported events” | “291 proposed vocabulary entries, with two bounded read-only chain slices implemented.” |
| “Final means settled” | “Final records the source's assertion; finality and authority are separate.” |
| “Exactly-once actions” | “One local report effect recovered in the tested transaction and replay scenarios.” |
| “Private by default” without scope | “Model fields remain inside the proposed encrypted body; full privacy integration remains a protocol gate.” |
| “Hash proves approval” | “A commitment identifies exact meaning; authentication and permission are checked separately.” |
| “Already reduces integration costs” | “The pilot will measure integration effort and manual corrections.” |

Every key limitation should be adjacent to the capability it qualifies. A single compact next-gates paragraph is enough to collect deployment scope; repeating a long warning under every card would obscure the product explanation.
