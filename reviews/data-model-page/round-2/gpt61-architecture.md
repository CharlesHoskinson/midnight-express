# GPT-6.1 review 1 — architecture and product education

Role: principal engineer and product educator. Reviewed the current `website/dist/data-model.html`, `model/README.md`, `docs/product-requirements/data-format-implementation.md` and `docs/product-requirements/unified-data-model.md`. This review recommends explanatory copy only; it does not change implementation claims.

## Assessment

The page has a sound teaching sequence: a concrete price mismatch, three architectural layers, bounded workflows, identity and recovery, then chain evidence and adoption. Its strongest feature is that authority and evidence boundaries sit next to the claims they qualify. The reader can distinguish a checked quote from a trade and a payment observation from payment execution.

The next improvement should add connective explanation, rather than more feature cards. A newcomer still has to infer what “data model” includes, how it differs from a schema or protocol, and why a contract fingerprint matters beyond ordinary version numbers. The adoption list names the work but gives little guidance for deciding whether a source format is suitable. The chain section names provenance concepts without walking through the history they preserve.

Keep the existing headings, quote example and evidence counts. Add five short prose passages at the placements below. Most should be visible paragraphs; put the version detail behind the existing recovery disclosure if vertical space is constrained. Readers should learn the architectural argument before opening technical details.

## Priority recommendations

1. **Define the three layers of agreement before introducing their components.** Place the first passage after the lead in `#contracts`. Explain the model, schema and protocol through the quote example. Avoid implying that all business semantics can be expressed by JSON Schema. The reference checks structural and semantic rules separately.

2. **Explain why the core stays small.** Add the second passage below `.model-layers` in `#contracts`. The current labels identify components; this paragraph explains their relationship and the cost of forcing unrelated domains into shared fields. Describe adapters as reviewed translations, without suggesting automatic universal interoperability or authenticated adapter installation.

3. **Distinguish a release label from an exact semantic commitment.** Add the third passage to “Preserve the original meaning” in `#replay`, or its disclosure. A software fix can leave the agreed definitions unchanged; a changed interpretation needs a new commitment. Do not imply that a hash supplies trust, or that the offline intersection helper performs a live negotiation. Preserve the explicit v0.1 read-only boundary.

4. **Teach lineage with one transfer history.** Put the fourth passage after the Ethereum/Solana columns in `#chains`. Explain observer delivery, physical fact and later invalidation as different records. This makes the existing journal claims understandable without adding another generic “blockchain event” abstraction. Retain the missing-history and fixture-finality qualifications.

5. **Make onboarding a review exercise.** Place the fifth passage before the ordered steps in `#start`. Give a partner a concrete artifact to assemble: representative source examples and a declaration of conventions. End with a decision about coverage and integration effort, not an implied promise of immediate deployment.

## Status discipline

Use `data-format-implementation.md` and `model/README.md` for present-tense implementation claims. Some earlier paragraphs in `unified-data-model.md` describe the original Python-only slice or planned cross-language work; its final implementation section supplies the updated boundary. The site correctly states three profiles, independent Python/Rust/TypeScript agreement for RFQ only, 291 proposed vocabulary entries, two bounded read-only fixture projection slices, and 56 PostgreSQL recovery checks. None should become “all workflows are portable,” “291 supported contracts,” live chain support, or production exactly-once execution.

The extra prose should clarify these distinctions without repeating every disclaimer in every section. Explain what each layer establishes once, then point readers toward the evidence section. Keep the canonical number example and concrete refusal conditions: they supply better educational evidence than broad claims of standardization.

## Proposed reader copy

### Insert in `#contracts`, after the lead

A data model describes the meaning applications agree to share: what a quote refers to, which party is buying, how an amount is measured and what a status claims. A schema describes the permitted structure of a message: its fields, types and allowed values. The workflow contract combines that structure with explicit definitions and rules, such as requiring the quoted cash total to match quantity multiplied by price.

The delivery protocol has a different job. It carries messages and provides its own membership and security mechanisms. Successful delivery does not tell an application whether “123.45” means dollars per share or cents per hundred shares. Midnight Express proposes to carry the agreed event inside its encrypted message body; the data model supplies a checked interpretation, and the application decides whether it has authority to act.

### Insert in `#contracts`, below the three layer cards

The shared core gives every event a recognizable identity and an exact contract reference. Each workflow then adds the terms that make sense for its own work. An invoice observation needs payment evidence and clocks; a quote needs units, perspective and expiry. Keeping those rules separate lets a domain develop its agreement without changing unrelated workflows.

An adapter connects a participant’s existing format to one of those agreements. It must declare the source convention and preserve every required term. If a source omits the price denominator, the adapter cannot repair that omission by guessing. The integration needs better source information or a different reviewed contract.

### Insert in `#replay`, with “Preserve the original meaning”

A version name is a convenient label; a contract commitment identifies the exact installed definitions and rules. Two applications should not assume agreement merely because both say “v0.2.” The offline reference checks the exact commitment against locally installed bundles and refuses an unknown contract rather than choosing a nearby version or fetching definitions from a sender’s URL.

Software and meaning can change independently. Fixing an implementation to follow the existing agreement need not change its semantic identity. Changing a unit, role or interpretation does. Historical events retain their original commitment, so replay can preserve the agreement that governed them. The reference preserves v0.1 read-only; authenticated installation and migration of live workflows remain deployment work.

### Insert in `#chains`, after the chain columns

Suppose polling and a subscription both report the same transfer. Those are two deliveries of one physical fact, not two transfers. If the transfer’s block is later invalidated, the journal preserves that earlier observation and records the invalidation. If it appears again at another physical location, that new inclusion has its own identity.

This lineage lets an application ask what was known at a particular cutoff and which evidence supports the current view. It also preserves uncertainty: a coverage gap or conflicting source assertion remains visible. The current journal demonstrates this behavior with supplied fixtures; it does not prove complete chain history or independently verify consensus finality.

### Insert in `#start`, before the ordered steps

Begin with representative messages from one useful workflow, including cases that should be refused. Write down the source’s units, party perspective, status meanings, identifiers and timing conventions. Compare them with a bounded contract before building the adapter. A missing term is a question for the source owner, not a default to add silently.

Use the pilot to establish both agreement and practical coverage. Which cases map without losing meaning? Which require a new contract? How much effort does another participant need? The current reference gives reproducible examples for that review. Production adoption also needs authenticated installation and sources, current authority, protocol integration and the destination’s recovery rules.
