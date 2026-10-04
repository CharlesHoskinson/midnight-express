# Use-case portfolio review

Reviewed `dist/index.html` and `dist/app.js` against the canonical `use-cases.json`. No site edits made.

## Verified data integration

- **Current files now correctly load all ten cases.** `index.html` loads `use-cases.js` before `app.js`, using deferred scripts in order. Parsed `window.MPE_USE_CASES` is an exact match for the canonical JSON sorted by numeric rank; ranks are 1 through 10. The initial missing-data issue was fixed before this final review.

## Canonical top ten

| Rank | ID | Recommended title | Stage |
| --- | --- | --- | --- |
| 1 | UC-01 | Institutional RFQ and negotiated quote coordination | Pilot A |
| 2 | UC-03 | Invoice, payment-status and reconciliation workflows | Pilot B |
| 3 | UC-05 | Agent coordination with bounded human approvals | Pilot C |
| 4 | UC-06 | Credential and access-revocation coordination | Next |
| 5 | UC-07 | Procurement and supply-chain exception coordination | Next |
| 6 | UC-02 | Private contract lifecycle notifications | Ledger-gated |
| 7 | UC-10 | Confidential incident and cross-chain operations coordination | Connector-gated |
| 8 | UC-09 | Private governance review and approval workflows | Policy-gated |
| 9 | UC-04 | Portfolio and collateral risk alerts | Freshness/mobile-gated |
| 10 | UC-08 | Insurance claim handoffs and milestones | Sector-gated |

## Hypotheses and gates

- The use-case renderer references the correct canonical fields: `recommended_title`, `value_hypothesis`, `initial_delivery_scope`, `stack_dependencies`, `pilot_success_measure`, and `remaining_gate`. The bundled canonical data preserves the business hypotheses and proposed gates accurately.
- The section introduction explicitly says business value remains a hypothesis; the footer source section identifies the architecture as a recommendation rather than a production deployment. Keep those qualifications.
- Show each card’s canonical `delivery_stage` as a small label. Without it, the top ten can look equally ready despite distinct ledger, connector, policy, freshness/mobile and sector gates. This is a clarity improvement, not a conflicting source claim.

## Copy refinements

- “A / FIRST PILOTS” groups RFQ, invoices and agent approvals correctly, but A can be confused with the source’s distinct Pilot A/B/C labels. Use “FIRST PILOT CANDIDATES” or show Pilot A/B/C on the three cards.
- The roadmap’s first-pilot sentence should preserve the bounded scopes: RFQ coordination and off-chain acceptance; invoice matching and authenticated payment-status notices; agent proposals with expiring human approval and a sandbox executor. Automated settlement/payment should remain gated.
- “B / PRODUCTION CORE” can suggest the admission, retention and durability work follows real-world pilots. Make explicit that these are prerequisites for production use; initial design-partner pilots may validate narrower, controlled compositions.
- The visible value hypotheses use benefit language (“Reduce”, “Faster”, “Earlier”), matching the source. Because demand is unvalidated, an optional per-card “Unvalidated value hypothesis” label would strengthen the existing section-level qualifier.

## Per-case gate preservation

- **1. Institutional RFQ and negotiated quote coordination:** First design partner; CON-060 and contract adapter gate automated settlement.
- **2. Invoice, payment-status and reconciliation workflows:** ERP integration and authenticated payment evidence; destination idempotency for external effects.
- **3. Agent coordination with bounded human approvals:** Application capability enforcement and trusted human approval UI; contract effects require consumer proof.
- **4. Credential and access-revocation coordination:** Issuer authority, stale-cache policy and tested removal/rekey; event receipt is not revocation completion.
- **5. Procurement and supply-chain exception coordination:** Authenticated gateways and archive/key policy; sensor provenance does not prove physical truth.
- **6. Private contract lifecycle notifications:** Private carried-event capability, exact-byte/applied-phase verification; private mobile delivery is separately gated.
- **7. Confidential incident and cross-chain operations coordination:** Declared cross-chain trust/finality, funded operators and alternate emergency path.
- **8. Private governance review and approval workflows:** Threshold/multisig authority, selective disclosure and CON-060 before on-chain execution; no anonymous voting claim.
- **9. Portfolio and collateral risk alerts:** Reliable market connectors and proven budgets; no hard-real-time liquidation guarantee; private phones need retrieval.
- **10. Insurance claim handoffs and milestones:** Customer data/retention policy, encrypted object integration and authorized retrieval; expiry does not erase copies.

Additional source qualifications worth retaining if card copy is shortened: group removal/expiry does not erase old copies; governance has no anonymous voting guarantee; incident coordination needs an independent emergency route; portfolio alerts have no hard-real-time liquidation guarantee; sensor attribution does not prove physical shipment truth. The current proposed card fields already retain the latter four relevant gates or scopes.
