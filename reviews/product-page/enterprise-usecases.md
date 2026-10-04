# Enterprise use cases: product manager review

Reviewed 2026-10-03: the [live page](https://charleshoskinson.github.io/midnight-express/), its published `app.js` and `use-cases.js`, and local `website/dist`. The three published files matched the local copies byte for byte. Also reviewed `docs/product-requirements/top-ten-use-cases.md` and `use-cases.json`. This is a content review from fetched HTML and JavaScript, not a rendered browser or usability test.

The page accurately keeps these use cases at recommendation stage, but its cards explain delivery scope and dependencies before showing an everyday situation. Although the data includes actors and triggers, `app.js` does not render them. A business reader therefore has to invent who uses the product and why. Add one illustrative story to each card, then show the initial scope and a short boundary. Keep technical gates in expandable detail. All examples below are hypothetical; their benefits are pilot hypotheses, not customer results.

## UC-07 · Procurement · Rank 5 · Next

**Suggested label:** Resolve a delayed delivery together.

**Actor:** A purchasing manager, supplier and delivery coordinator.

**Trigger:** A supplier reports that an order will arrive late.

**Story:** A manufacturer is waiting for parts. Its supplier posts a signed delay notice; the delivery coordinator shares a revised arrival estimate with the people handling that order. The purchasing manager acknowledges the update and records the agreed next step. Commercial details stay with the authorized participants rather than being copied through unrelated teams.

**Value to test:** Less chasing for updates and fewer missed handoffs. Measure time from exception notice to an agreed response, plus missed handoffs and integration effort.

**Boundary for the card:** “Coordinates reported delivery updates. A signed report identifies its source; it does not prove where the shipment is.”

**Scope and gate to retain:** Begin with signed milestones and restricted exception notices. Integrations must authenticate their sources; teams need explicit group access, archive and key policies. Avoid a temperature-sensor example as the lead story because it introduces a physical-truth question before the coordination value is clear.

## UC-08 · Insurance · Rank 10 · Sector-gated

**Suggested label:** Keep a claim moving between teams.

**Actor:** A claimant, claims handler and adjuster.

**Trigger:** The adjuster requests an additional document.

**Story:** After reporting damage, a claimant receives a request for a repair estimate. The claims handler shares an authorized reference to the document with the assigned adjuster. When the assessment is ready, the handler receives the status update and can move the claim to its next review step. Each participant gets the information their role permits.

**Value to test:** Fewer repeated document requests and less time spent asking which team has the claim. Measure handoff time and missing-document requests.

**Boundary for the card:** “Coordinates claim status and authorized document access. Claim decisions, payment authorization and retention policy stay with the insurer.”

**Scope and gate to retain:** Start with status updates and authorized references to encrypted documents, not documents broadcast inside events. Customer data policy, encrypted storage integration and longer-term history are prerequisites. Removing access can restrict future retrieval; it cannot erase copies already obtained. Payment execution should not appear in the lead story; duplicate-payment handling remains a separate acceptance concern.

## UC-10 · Incident operations · Rank 7 · Connector-gated

**Suggested label:** Share sensitive incident updates with responders.

**Actor:** An operations lead, service owner and authorized response team.

**Trigger:** A settlement service reports an interruption.

**Story:** A settlement service stops progressing. The operations lead sends the affected service owner and responders a private incident notice. They exchange status updates and record who owns the next investigation step. A responder returning after a disconnect can recover retained notices and resume the handoff.

**Value to test:** Clearer responsibility and less time reconstructing the incident across teams. Measure response handoff time, notices recovered after interruption and whether a failed handler disrupts other streams.

**Boundary for the card:** “Supports human-led coordination alongside an independent emergency channel.”

**Scope and gate to retain:** Begin with reviewed notices and scoped responses. Connector trust, chain finality assumptions, operator funding and service objectives remain open work. Do not imply that a network interruption always leaves MPE available, that incident delivery is guaranteed, or that it replaces the emergency response path. Avoid hard-real-time control and automatic incident remediation in the story.

## UC-04 · Portfolio alerts · Rank 9 · Freshness/mobile-gated

**Suggested label:** Review a collateral warning privately.

**Actor:** An account owner and the account's risk service.

**Trigger:** The risk service reports collateral below the owner's chosen threshold.

**Story:** An account owner receives an advisory warning in a desktop application. The warning shows when its source data was last updated. The owner checks the underlying account before deciding whether to add collateral. If the feed is stale or incomplete, the application shows that condition rather than presenting the warning as current.

**Value to test:** Help owners recognize a risk condition while keeping account details and watched positions out of relay-visible message content. Measure source age at alert delivery, gap detection and time to human review.

**Boundary for the card:** “Advisory alerts depend on source freshness and delivery. They do not guarantee liquidation prevention.”

**Scope and gate to retain:** Backend/desktop advisory alerts first; stale or gapped feeds block automated high-risk effects. Market adapters and their trust/finality assumptions need validation. Broad private mobile delivery remains research-dependent. Avoid “instant,” “real-time protection,” guaranteed intervention windows, or a phone notification as the lead illustration.

## UC-02 · Contract notifications · Rank 6 · Ledger-gated

**Suggested label:** Know when an escrow milestone is confirmed.

**Actor:** An application user, desktop wallet application and contract observer.

**Trigger:** The observer reports an escrow milestone event.

**Story:** A user is waiting for an escrow milestone. The desktop application shows an incoming update as pending verification, then marks the milestone confirmed only after the observer has verified the relevant ledger event and its successful application. Following a disconnect, the application retrieves missed retained updates rather than leaving the user to keep checking manually.

**Value to test:** Less manual status checking, clearer pending-versus-confirmed state and fewer missed updates. Measure correct finality labels, recovery after disconnection and integration time.

**Boundary for the card:** “Receiving a notice does not establish contract completion. Confirmation needs verified ledger evidence.”

**Scope and gate to retain:** Start on desktop/backend with public events or signed application notices. Private carried events depend on underlying Midnight capability; private mobile delivery is separately gated. Exact event bytes and position, plus successful application, must be verified before final status. Do not describe a signature or anchor receipt alone as proof that escrow completed.

## Recommended presentation pattern

Keep the stable identifiers, ranks and delivery stages from the requirements. Show the short label, a two-sentence illustrative story and a benefit framed as something to test. On expansion, use **Who is involved**, **What starts it**, **First useful scope**, **How we would measure it** and **What must be proven**. Render the existing actors and trigger fields, with these stories as an additional editorial field.

For all five cases, describe selective access and encrypted business content without claiming universal anonymity or hidden timing. Make recoverability conditional on retained history and tested endpoint recovery. Keep the page's overall “design and exploration stage” label visible near the use-case section as well as in the introduction, so visitors entering through `#use-cases` see the maturity context.
