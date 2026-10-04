window.MPE_PRODUCT = {
  "workflows": {
    "quotes": {
      "label": "PROPOSED FIRST DEMONSTRATION / QUOTE COORDINATION",
      "title": "A buyer asks two approved dealers for prices.",
      "context": "A request for quote (RFQ) asks a dealer for terms on a specified transaction. In this illustration, the buyer compares offers and hands an accepted quote to settlement.",
      "who": "Buyer · approved dealers · compliance reviewer · operations team",
      "steps": [
        [
          "Request",
          "The buyer sends a confidential request with a response deadline to approved dealers."
        ],
        [
          "Compare",
          "Dealers return signed offers with expiry times. The buyer’s application checks the signer, role and current terms."
        ],
        [
          "Accept and hand off",
          "The buyer explicitly accepts one valid offer. The agreed terms go to the separately authorized settlement process."
        ]
      ],
      "value": "Test whether the team spends less time checking versions and reconstructing the accepted terms.",
      "measure": "Quote turnaround, staff reconciliation effort, manual handoffs and recovery after a simulated outage.",
      "scope": "Backend and desktop requests, signed quotes, expiry and off-chain acceptance. Acceptance is a business decision; automatic settlement needs the separate authority, replay and anchored-message proof path.",
      "component": "sdk"
    },
    "invoices": {
      "label": "PROPOSED FOLLOW-ON PILOT / INVOICE MATCHING",
      "title": "A finance team connects an invoice to verified payment status.",
      "context": "Reconciliation means checking that invoice, payment and accounting records agree. A company finance system (ERP) remains its system of record.",
      "who": "Supplier finance team · customer treasury · bank/payment integration",
      "steps": [
        [
          "Issue",
          "The supplier sends a signed invoice notice with a reference and amount. Documents are fetched only through explicit authorized access."
        ],
        [
          "Verify",
          "The customer pays through its existing process. An authenticated bank or payment notice identifies the payment and the invoice it relates to."
        ],
        [
          "Match or investigate",
          "The receiving application checks the reference and amount. A mismatch remains unresolved; duplicate protection prevents repeated notices from adding another accounting entry."
        ]
      ],
      "value": "Test whether finance staff spend less time chasing status and matching payments by hand.",
      "measure": "Unmatched invoices, staff handling time, incorrect matches, duplicate postings and restart catch-up.",
      "scope": "Match invoices and authenticated payment-status notices. The initial pilot exchanges and reconciles status; payment execution stays in the existing authorized process. Destination duplicate protection and source evidence still need validation.",
      "component": "recovery"
    },
    "agents": {
      "label": "PROPOSED FOLLOW-ON PILOT / BOUNDED AGENT WORK",
      "title": "A person approves the limits of an agent’s proposed action.",
      "context": "An approval should identify a target, a budget and a deadline. The agent’s message is a proposal; the application must verify what the person actually authorized.",
      "who": "Enterprise worker · software agent · approval officer · sandbox executor",
      "steps": [
        [
          "Propose",
          "An agent requests a purchase from a named supplier for up to an illustrative $500 before a stated deadline."
        ],
        [
          "Approve",
          "A person reviews the actual proposal and signs an expiring approval tied to that supplier, budget and action."
        ],
        [
          "Enforce and record",
          "The sandbox executor checks signer authority and scope. A $700 request, a changed supplier or an expired approval is rejected. The workflow records its authorized result."
        ]
      ],
      "value": "Test whether explicit scoped approvals reduce manual handoffs and clarify who authorized each action.",
      "measure": "Proposal-to-decision time, staff handoffs and rejection of unauthorized, expired or replayed actions.",
      "scope": "Bounded proposals, signed human approval and a sandbox enforcing target and budget. Application capability enforcement and a trusted approval interface are required. Contract effects have a separate consumer-proof gate.",
      "component": "authority"
    }
  },
  "cases": {
    "UC-01": {
      "title": "Request and compare confidential quotes",
      "summary": "A buyer requests prices from approved dealers, compares signed offers and records an explicit acceptance.",
      "who": "Buyer, approved dealers, compliance reviewer and settlement operations.",
      "example": "Two dealers respond to the same request. The buyer accepts one valid offer before it expires and hands the agreed terms to the existing settlement process. The proposed recovery layer should preserve that accepted record after an interruption.",
      "boundary": "The first scope coordinates quotes and off-chain acceptance. A receipt does not mean the trade settled."
    },
    "UC-03": {
      "title": "Match invoices to payment status",
      "summary": "Finance teams connect signed invoice updates to authenticated payment notices and investigate mismatches.",
      "who": "Supplier finance team, customer treasury and a bank or payment-service integration.",
      "example": "A supplier receives a payment notice for a particular invoice. The application checks the reference and amount before marking it paid. A wrong amount remains unresolved, and repeated notices must not create extra accounting entries.",
      "boundary": "The initial scope matches status and records. Authenticated payment evidence, finance integration and destination duplicate protection are required."
    },
    "UC-05": {
      "title": "Coordinate agents with human approval",
      "summary": "An agent proposes a bounded action; a person approves a specific target, budget and expiry.",
      "who": "Enterprise worker, AI or business agent, approval officer and sandbox executor.",
      "example": "A procurement agent requests a purchase from one supplier within a budget. A person signs that exact scope. The executor rejects a different supplier, an excessive amount or an expired approval, even when the message is authentic.",
      "boundary": "The application must verify agent output and enforce permission before acting on a delivered message."
    },
    "UC-06": {
      "title": "Keep credential and access status current",
      "summary": "An issuer or employer sends authenticated changes so verifiers can update their access decisions.",
      "who": "Credential issuer, subject wallet and service or employer verifier.",
      "example": "A contractor’s credential is revoked. Services receive a newer authenticated issuer version that overrides a delayed earlier grant. A service with outdated evidence reports stale status and blocks high-risk access.",
      "boundary": "Receiving a notice is not completed revocation. Tested enforcement and rekeying govern future access; past copies remain possible."
    },
    "UC-07": {
      "title": "Resolve procurement and delivery exceptions",
      "summary": "A buyer, supplier and logistics team share restricted milestones and agree the next step after a delay.",
      "who": "Purchasing manager, supplier, logistics provider and authorized insurer or auditor.",
      "example": "A supplier reports that required parts will arrive late. The logistics team shares a revised estimate with the people handling the order. The buyer records an acknowledged next step without spreading unrelated commercial terms.",
      "boundary": "A signature identifies the report’s source. Physical shipment evidence, partner integrations and history policies need separate validation."
    },
    "UC-02": {
      "title": "Follow contract milestones privately",
      "summary": "A desktop application distinguishes a received notice from a verified contract milestone.",
      "who": "Application user, desktop wallet or application and contract observer.",
      "example": "A user is waiting for an escrow milestone. The application shows an update as pending, then confirms it only after checking the exact ledger event and successful application. Retained notices can support catch-up after a disconnect.",
      "boundary": "Start with public-event or signed-application notices. Private carried events and private mobile reception require further platform work."
    },
    "UC-10": {
      "title": "Coordinate sensitive incident response",
      "summary": "Authorized responders exchange incident updates and record who owns the next investigation step.",
      "who": "Operations lead, service owner, chain or service integration and response team.",
      "example": "A settlement service stops progressing. Responders exchange private status updates and assign a human-reviewed investigation step. A returning responder recovers retained notices to catch up on the handoff.",
      "boundary": "Keep an independent emergency channel. Delivery, source trust, funding and failure isolation must be validated."
    },
    "UC-09": {
      "title": "Review proposals and collect approvals",
      "summary": "A board or committee coordinates confidential review and records explicit approvals under its own rules.",
      "who": "Board or DAO committee, authorized reviewers and execution agent.",
      "example": "A committee reviews a vendor proposal under an illustrative three-approval policy. Two approvals, an expired approval or a delivery receipt cannot satisfy that policy. The application checks valid authority before execution and prepares narrowly scoped audit evidence.",
      "boundary": "The customer defines and enforces the approval threshold. Anonymous voting and ledger execution require separate evidence; ledger execution also needs consumer proof."
    },
    "UC-04": {
      "title": "Review portfolio and collateral warnings",
      "summary": "An account owner receives advisory risk updates with visible source age and gap status.",
      "who": "Account owner, risk service and an explicitly authorized delegated agent.",
      "example": "A desktop risk application reports collateral below the owner’s threshold. The owner checks the underlying account before deciding whether to add collateral. A stale or incomplete feed is shown as such and blocks high-risk automated effects.",
      "boundary": "Advisory backend/desktop alerts first. Freshness and market integrations must be measured; there is no liquidation-prevention guarantee."
    },
    "UC-08": {
      "title": "Keep insurance claim handoffs moving",
      "summary": "Claims handlers and adjusters exchange status updates and authorized references to encrypted documents.",
      "who": "Claimant, insurer, adjuster and authorized payment or reinsurance partner.",
      "example": "An adjuster requests a repair estimate. The claims handler shares an authorized document reference with the assigned adjuster. An assessment update moves the claim to its next review step while role permissions limit the evidence shared.",
      "boundary": "Claims decisions, payment permission and retention policy remain with the insurer. Access withdrawal or event expiry does not erase copies already obtained."
    }
  }
};
