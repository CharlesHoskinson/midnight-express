# GPT-6.1 review 3: workflow meaning and execution safety

The page already draws the correct boundaries, but readers must assemble them from several sections. Its strongest improvement would be one familiar sequence: understand the message, establish why its source and evidence are trusted, check permission now, then preserve the permitted effect and progress together. Explain that sequence before asking readers to reason about replay. Give invoices and approvals complete, bounded stories rather than suggesting that the three profiles form a complete request, offer and result runtime.

The prose below is suitable for insertion. It is grounded in `model/README.md`, `docs/product-requirements/data-format-implementation.md`, the current example events and the sandbox host. The examples support distinct invoice status observations; they do not demonstrate one payment moving through all three statuses. Keep that distinction visible.

## Placement: after the three layers in “The model”

### From a message to permitted work

An application answers four questions before a message can lead to work.

**What does it mean?** The installed workflow contract checks the declared terms. For a quote, that includes the currency, quantity, price basis and expiry. For an approval, it includes the exact report-writing proposal and its limits. A successful check gives the application a candidate interpretation. Every reference validator success returns `executes:false`.

**Why should we trust it?** A source name identifies whom the message claims to represent. It does not prove who sent it. The application needs authenticated source identity and evidence suitable for the claim. A digest helps check that content matches a commitment; it does not establish that a bank reported a payment or that a human approved an action. The current reference uses trusted test fixtures for these assumptions.

**May we act now?** The application checks current permission for the exact work, target and scope. An approval can expire or be revoked after a message arrives. A previously accepted interpretation therefore cannot stand in for permission at the moment of execution. The sandbox host checks its fixture permission before execution and again inside the transaction that writes the effect.

**How will we remember the outcome?** The application records permitted work and processing progress at the relevant effect boundary. In the local prototype, that boundary is one PostgreSQL transaction containing one report row and the records needed for replay and recovery. A remote destination has a separate boundary and needs its own agreement for duplicate requests and uncertain outcomes.

These questions connect meaning to action without making interpretation itself an authority to act. Production source authentication, human identity and permission services remain separate implementation work.

## Placement: expand “Payment observation,” with clocks directly underneath

### A payment report explains a claim

A supplier has issued a $500 invoice. The application receives an observation describing a $250 payment, with the invoice identity, payment identity, currency, source status and supporting evidence kept explicit. The contract checks that the complete observation matches the trusted fixture evidence and that the positive amount does not exceed the invoice payable.

Pending reports the source’s Pending status. Final reports its Final status. Reversed reports its Reversed status. Keeping these labels distinct lets an application explain what was reported without collapsing every payment message into “paid.” Final remains a source assertion; validating it does not verify bank settlement. Reversed describes a reported payment status, not an instruction to send money back.

The observation also distinguishes when the source says the payment took effect, when it was observed and when the event recording that observation was created. Those times must occur in that order and cannot exceed the trusted current time. For example, a source could say a payment took effect at 10:00, an observer could see it at 10:05, and the observation record could be created at 10:06. The contract refuses an impossible order rather than silently treating all three times as the same event.

The checked result is an explainable payment observation. Deciding whether to allocate that payment, reduce an outstanding balance or close the invoice needs accounting rules and authority beyond this pilot. The reference fixtures contain separate Pending, Final and Reversed examples with different payment identities; they are not a demonstrated payment-transition history.

## Placement: after “Sandbox approval,” before the replay section

### One approval, one bounded report write

In the sandbox example, Alice is the named human in an approval fixture for one WriteReport proposal. The proposal identifies its report target and input digest, allows a maximum of five Steps, and expires at 13:00. The approval also fixes the authority domain, execution scope, budget window and policy. These fields say exactly which work the fixture approves; Alice’s name in the event is not production identity verification.

Validation checks that agreement and returns a candidate. The separately authorized sandbox host then checks current fixture permission and available aggregate budget. It reserves the declared maximum, writes one database report row, charges one Step and releases unused capacity. The report write and its processing records commit together. The demonstrated effect is that single row, not an arbitrary tool call, payment or blockchain transaction.

If the same approved work arrives again, the host can recognize that it was already consumed. If its target or committed content changes, the host refuses the conflict. If permission has been revoked before execution, the earlier approval cannot authorize the write.

## Placement: replace or expand “Recovery has an effect boundary”

### A retry preserves the original work

An event identity distinguishes a delivery occurrence. A stable action identity distinguishes the approved work within its authority domain and execution scope. A retry may arrive in a new event or transport envelope, but that new delivery does not renew a consumed action or give it another budget. Changed content under an existing occurrence also conflicts.

Suppose the sandbox worker commits its report row, then crashes before acknowledging completion. On restart, the durable processing records identify the consumed action, so recovery retains one local report write. This is the boundary tested with Umbra and PostgreSQL.

Now suppose a separate destination fixture commits a request, but its reply is lost. The sender cannot conclude that the destination failed. It preserves the uncertainty as OutcomeUnknown and reconciles using the original idempotency key and matching request evidence. Missing evidence leaves the outcome unknown; reading history does not grant permission for another effect.

That destination is an acknowledgement fixture in a separate transaction. The tests exercise the lost-reply problem without claiming a live bank or tool integration. A real destination must provide verified idempotency and reconciliation behavior before the same recovery approach can support its effects. One local transaction cannot establish global exactly-once execution.
