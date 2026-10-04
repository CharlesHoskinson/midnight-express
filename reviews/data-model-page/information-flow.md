# Data Model page — information architecture review

Role: product manager reviewing reader comprehension and progression. Read the v0.2 model README, Overview and Implementation pages, and positioning/workflow reviews. These recommendations concern public prose and navigation, not new implementation claims.

## Recommended reading order

1. **Different formats. The same agreed meaning.** State the business problem in one sentence, then explain shared core, narrow workflow contracts and declared adapters in two sentences. Keep test counts out of the hero.
2. **A price needs a unit and a perspective.** Put the concrete quote example immediately after the introduction. The reader should understand the problem before meeting an envelope or digest.
3. **One small core. Separate agreements for each workflow.** Explain the three layers, then answer the original universal-schema concern. Describe additions as separately reviewed contracts with explicit supported terms.
4. **Three workflows, three precise boundaries.** Quote, invoice observation and sandbox approval cards each show ambiguity → agreed rule → intended benefit → current scope. These are reference-tested pilot profiles, whereas the Overview describes broader proposed pilots.
5. **A retry is not a new business action.** Explain delivery identity, business action identity, immutable contract history and append-only observations together. This is the natural bridge from meaning to durable processing.
6. **Chain events retain their native evidence.** Show Ethereum and Solana side by side. Explain the wider vocabulary and narrower executable transfer slices. Avoid exposing 291 entries as an undifferentiated list.
7. **What is implemented, and what must be proved next.** Separate finite synthetic evidence from remaining production and customer gates. Test counts belong here; intended business benefits need measurement rather than asserted savings.
8. **Questions teams will ask.** Native details/summary FAQ, followed by links to Implementation and Overview use cases. Private technical links are supplementary.

Use at most six section jump links: Why meaning matters, How it works, Pilot contracts, Replay & history, Chain events, Evidence. Each should target a real static section. Label the main navigation tab **Data model** consistently with the existing website sentence-case navigation and set `aria-current="page"` on this page.

## Direct answer to the original design concern

Recommended heading: **Extend the agreements without expanding one universal schema.**

Recommended copy: “The model fixes a small common mechanism for identifying an event and the agreement it uses. Business terms live in separate workflow contracts: a quote does not need an invoice’s status rules, and an invoice does not need an agent’s permission rules. Participant adapters translate only declared conventions that a contract can represent. If the contract cannot express a source’s currency, price basis, fee convention or action, the adapter refuses it. A new requirement earns a separately reviewed contract rather than a guessed default or an ever-growing universal object.”

Follow with: “This trades some flexibility for a reviewable integration agreement. It does not eliminate domain design or partner negotiation. The pilot must test whether supported contracts cover useful work and whether adding a partner costs less effort than the current process.”

This responds directly to both failure modes: permissive syntax that conceals incompatible meaning, and a committee-designed schema that tries to cover every domain. The refusal boundary and versioned extension process are part of the product proposition, not an inconvenience to hide.

## Useful static diagram

Use HTML/CSS cards with an ordered textual equivalent; SVG or animation is unnecessary. Keep the flow visible without JavaScript:

- Source A: $123.45 per share; 100 shares; USD; requester buys; no fees.
- Source B: 1,234,500 cents per 100 shares; same declared quantity, currency, roles and fees.
- Declared adapters → agreed RFQ meaning: 100 shares × $123.45 = $12,345.
- Missing price basis → refused.
- Checked interpretation → application checks source authority and policy → application decides next step.

Caption: “The reference compares declared formats for the same complete source-bound intent. Offers from different dealers keep different identities. An accepted quote is an observation; the diagram does not execute a trade.”

The last step should not be a payment icon, wallet signature or settlement tick. Explain authentication and authorization in the reader-visible caption, not solely in a disclosure.

For approval replay, use a compact second diagram only if space allows: delivery 1 + delivery 2 → same scoped action → one local sandbox report write. Caption that this is a fixture-authorized database prototype, not global exactly-once external execution.

## Translate jargon at first use

| Technical term | Reader-facing explanation |
| --- | --- |
| Event envelope | The shared identity, source, time and agreement attached to an update |
| Workflow profile / contract | The exact terms and rules applications agree to interpret |
| Canonicalization | A deterministic representation used to compare the same declared meaning |
| Contract commitment | A fingerprint identifying the exact reviewed agreement |
| Intent commitment | A fingerprint of the complete source-bound business meaning; it does not authenticate the source |
| Occurrence identity | Which specific update or delivery record this is |
| Scoped action identity | Which piece of approved work this is, even if delivered again |
| Adapter | A translator for one declared participant convention |
| Refusal | The application stops the unsupported message instead of inventing missing meaning |
| Reorg / invalidation | A prior chain observation no longer belongs to the current branch; its history stays visible |
| Known-as-of | What the observer had recorded by a particular intake time |
| OutcomeUnknown | A lost reply leaves completion uncertain until reconciliation |

Keep raw field names, SHA-256/JCS construction, strict timestamp grammar, 3,926-byte parsing limit and exact bundle directory layout inside a native expandable technical section. State that the raw parsing limit does not demonstrate fit in the encrypted wire. Do not require readers to expand details to discover the three-profile scope, source-assertion finality or absence of production authentication.

## Suggested FAQ copy

**Is this one schema for every application?**

“No. It is a shared event mechanism and separately versioned agreements for specific workflows. Each agreement has explicit supported terms. New domains receive their own reviewed contracts.”

**Can applications keep their existing formats?**

“Yes, when a declared adapter can represent their meaning exactly within a supported contract. Unsupported currencies, units, roles or fees are refused rather than filled in.”

**Can an AI agent infer missing fields?**

“The reference does not infer missing business terms. An AI may help propose a mapping for human review, but that proposal is not an accepted contract or permission to act.”

**Does a valid message permit an action?**

“No. Validation produces a checked candidate. Source authentication, current permission and application policy remain separate. The implemented executor is a fixture-authorized sandbox report write.”

**Does Final mean a payment or chain event is settled?**

“Final in the payment profile preserves what the source asserted. Chain commitments remain Ethereum- or Solana-specific source evidence. Neither label supplies verified consensus or bank settlement authority.”

**Are all 291 chain messages supported today?**

“No. The catalog proposes vocabulary for common application messages. Executable chain support is currently limited to read-only ERC-20 and legacy SPL TransferChecked fixture projections.”

**What happens when an agreement changes?**

“Changed meaning receives a new immutable contract. Historical messages retain their original agreement, and unknown contracts refuse. v0.1 is preserved as historical read-only material; no live workflow migration has been demonstrated.”

**What business value has been measured?**

“Finite synthetic tests establish specific reference behavior. Partner integration effort, correction rates and turnaround savings still need customer baselines and pilot measurements.”

## Public-page and navigation checks

The main explanation, quote arithmetic, three boundaries and evidence must all be readable without repository access or JavaScript. Link the evidence section to `implementation.html#reference`; link proposed next work to `implementation.html#sprint-1`; link wider use cases to `index.html#use-cases`. A private repository evidence link should explicitly say that access is required.

Use semantic heading order, descriptive diagram captions, native disclosure controls and a skip link. On mobile stack the quote cards in source → meaning → refusal order rather than relying on side-by-side arrows. A 200% text-size reader should retain all units, scope captions and navigation links without horizontal scrolling. Do not display “same meaning” only as a color or icon.
