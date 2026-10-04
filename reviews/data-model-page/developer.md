# Developer product-manager review

## Recommended visitor journey

Start with the adoption problem: participants need to agree on meaning without replacing their existing applications. Show one concrete mapping, explain the three supported pilot contracts, then introduce chain coverage and how the model connects to transport/recovery. Place identities and versioning in expandable implementation detail after their practical benefits. End with an honest implementation boundary and developer next steps.

Use headings such as “Agree on what a message means,” “Keep your application. Make the mapping explicit,” “Three workflows to validate first,” “Chain evidence keeps its own meaning,” “A retry must not become a second action,” and “Add a contract without changing every workflow.” These explain the job to be done before introducing technical vocabulary.

## Suggested lead prose

**Agree on meaning before acting.** Midnight Express applications share a small message core and an exact contract for each workflow. A quote, a payment observation and an approved action have different rules. Participants agree to those rules explicitly, while keeping their own application formats behind reviewed adapters.

The model is intended to reduce ambiguous integrations and make replay auditable. A valid message still does not establish who sent it or grant permission to execute it. Authentication, current authority and evidence quality remain separate checks.

## Adapters: show the onboarding benefit

**Keep your application. Make the mapping explicit.** One system quotes a price in dollars per share; another uses cents per hundred shares. An adapter can map both to 100 shares at $123.45 each, or $12,345 in total, when currency, price basis, buyer/seller perspective and fees are declared. Missing or inconsistent meaning is refused rather than guessed.

The reference compares two RFQ source adapters and independent Python, Rust and TypeScript interpreters. Agreement is demonstrated for a finite synthetic corpus, not all possible financial messages. Different dealers keep distinct source identities even when their prices match. Transformation does not transfer a signature from the original bytes to the translated message.

For developer onboarding, explain this sequence: choose an existing contract; declare source conventions; build and review a deterministic adapter; run accepted and rejected fixtures; install the exact approved contract; then integrate authenticated transport and authorized recovery. An unsupported source format should trigger a mapping discussion, not automatic default insertion.

## Three current pilot profiles

Present these as three cards with parallel “What it means / What it does not authorize” language.

- **Quote:** a tightly bounded share quote in USD with explicit price basis, requester perspective, fees and expiry. An observation for coordination; no trade settlement.
- **Payment observation:** a positive partial or full amount associated with an invoice, with Pending, Final and Reversed evidence and explicit timestamps. A source's Final assertion is not bank finality or payment permission.
- **Sandbox approval:** a precise WriteReport proposal tied to an authority domain, execution scope, budget and expiry. Validation produces a candidate. The local recovery fixture exercises one database report-row write under test authority.

Avoid claiming independent Rust/TypeScript validation of invoices or approvals: cross-language implementation currently covers RFQ only.

## Chain domain: distinguish inventory from implemented projections

**Chain evidence keeps its own meaning.** The proposed Ethereum and Solana vocabulary inventories 291 messages and events: queries, wallet requests, transaction outcomes, transfers, approvals, subscription controls and application observations. It gives future contracts a shared starting point; it is not 291 executable schemas or complete chain support.

The implemented read-only slices are narrower: Ethereum ERC-20 receipt/log transfers and Solana legacy SPL Token TransferChecked instructions. They preserve exact raw quantities, network and transaction location, decoder identity and supplied evidence. Token-2022, arbitrary program instructions and live authenticated RPC integration are outside these admitted slices.

Ethereum safe/finalized and Solana processed/confirmed/finalized retain their chain-specific meanings. A failed transaction does not establish an ordinary successful transfer; Solana inner instructions need their own outcome evidence. A bridge source message does not prove destination settlement. These distinctions prevent a convenient common name from erasing important evidence.

Display an explicit three-row status table: “291 vocabulary entries — proposed inventory”; “ERC-20 / legacy SPL transfers — read-only fixture projections”; “Live authenticated chain contracts — additional implementation and evidence required.”

## Identities: connect each to a recognizable failure

**A retry must not become a second action.** The model separates four identities because one identifier cannot safely answer every replay question:

| Identity | Practical question | Consequence |
| --- | --- | --- |
| Message occurrence: source + message ID | Have we already received this exact event? | An exact repeat is a duplicate; changed content under the same occurrence conflicts. |
| Business action: authority domain + execution scope + action ID | Has this authorized operation already been consumed? | A new message or transport ID cannot authorize the operation again. Changing its target or contract conflicts. |
| Physical chain fact: concrete inclusion/instruction location | Is this the same transfer in the same chain location? | Repeated delivery counts once; repeated CPI instructions remain distinct; re-inclusion is a new location. |
| Observer delivery | How and when did this observer receive the evidence? | Subscription, polling and backfill deliveries remain auditable without multiplying the physical fact. |

An append-only journal also records invalidations and gaps. It can distinguish what the system knew at an earlier cutoff from what arrived later. A rollback does not silently erase history, and incomplete evidence does not become a trustworthy total.

Outer transport EIDs should be introduced only as another delivery identity, not as the business action key.

## Immutable contracts: explain upgrade safety

**Add a contract without changing every workflow.** Each profile commits its schema, semantic rules and common primitives in an immutable bundle. Participants select an exact installed contract; an unknown contract is refused. No sender-provided schema URL triggers a download.

Meaning and implementation releases are tracked separately. Changing invoice-specific rules need not change the quote contract. Historical v0.1 artifacts remain available for reading and reproducing the review; the current loader will not execute them. The local reference demonstrates integrity and exact contract selection. Authenticated distribution and live workflow migration still require implementation.

## Stack fit: proposed architecture, implemented boundary

Use a plain sequence rather than an undifferentiated component list:

1. An application adapter translates declared source conventions into a selected workflow contract.
2. The validator checks structure, exact values, semantic rules and replay identity. It returns a candidate, not permission.
3. In the proposed protocol, encrypted messages travel through Midnight Express's private whole-shard GossipSub transport. Membership/admission and sealed-wire authentication remain separate protocol gates.
4. Read-only chain adapters contribute explicitly qualified evidence. They do not mint authority or consensus finality.
5. An authorized host uses Umbra recovery to commit inbox, action, local effect, budget, outbox and progress together. Uncertain remote completion remains uncertain until reconciliation.

Keep the data model visually inside the encrypted message body: it does not replace GossipSub routing, anonymous admission or Midnight Registry authority. Signal-derived sealing/private messaging and separately gated OpenMLS belong to the transport/security layer, not the business schema. The implemented Umbra fixture is a PostgreSQL transaction composition, not proof of network-wide exactly-once effects.

## Evidence and visitor next action

Use evidence as a compact supporting panel: “Three closed pilot event types; independent RFQ interpreters and two source adapters; read-only chain projections; 56 Umbra/PostgreSQL checks, including four actual worker kills.” Link to Implementation for detailed counts and remaining protocol gates. Do not make test counts the headline or present synthetic agreement as measured customer savings.

The public page should stand alone. Private repository links are optional developer evidence and must be labeled as requiring access. Recommended primary CTA: “Explore the prototype plan”; secondary CTA: “Review the stack.”

## Source correction noticed

`model/domains/README.md` still says “existing v0.1 model” in a paragraph describing the three currently accepted pinned profiles. The active reference is v0.2; this stale label should be corrected during page work so developers do not mistake the historical read-only release for current runtime support.
