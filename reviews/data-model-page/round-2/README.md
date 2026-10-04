# Nine-model review — expanded Data Model guide

The requested reviewers were three Gemini 3.1 Pro agents through `agy`, three Grok 4.7 CLI agents and three GPT-6.1 agents. Each reviewed the same published baseline (`f0e3fc6`) and current implementation boundaries. The external CLI prompts included complete copies of the page, model README and implementation-status document. GPT reviewers read those repository artifacts; the architecture role also read the design proposal.

| Model | Perspective | Review | Applied explanation |
| --- | --- | --- | --- |
| Gemini 3.1 Pro (High) | Executive positioning | [Positioning](gemini31-positioning.md) | Explain the integration tradeoff and bounded agreements before technical inventories. |
| Gemini 3.1 Pro (High) | Technical teaching | [Teaching](gemini31-teaching.md) | Explain familiar labels/form/translator concepts, immutable meanings and terminology. |
| Gemini 3.1 Pro (High) | Business workflows | [Workflows](gemini31-workflows.md) | Narrate the quote conversion, explicit refusal and partial-payment constraints. |
| Grok 4.7 | Business value | [Business](grok47-business.md) | Partner decisions, integration costs and scope tradeoffs. |
| Grok 4.7 | Developer adoption | [Developer](grok47-developer.md) | Contract selection, review artifacts, replay and onboarding. |
| Grok 4.7 | Trust and operations | [Trust](grok47-trust.md) | Meaning/evidence/permission/effect sequence, lost acknowledgements and source assertions. |
| GPT-6.1 | Architecture education | [Architecture](gpt61-architecture.md) | Model versus schema versus protocol, exact version commitments and transfer lineage. |
| GPT-6.1 | Reader comprehension | [Reader](gpt61-reader.md) | Reader route, worked arithmetic/refusal, bridging paragraphs and glossary. |
| GPT-6.1 | Workflow authority | [Authority](gpt61-authority.md) | Payment clocks, bounded approval, current permission and recoverable local effects. |

## Editorial synthesis

The revised page retains its eight-section structure and existing navigation while adding connected explanations: why flexible formats and a universal schema both create integration work; the arithmetic and role translation in the RFQ example; a refused mapping; the relationship between model, schema and protocol; four decisions from interpretation to permitted work; payment clocks/status boundaries; exact contracts versus version labels; crash versus lost-destination-reply recovery; the life of one transfer through repeated delivery and invalidation; partner review questions; and a native expandable glossary.

The core's labels are event data inside the proposed encrypted body. Adapters and installed contract bundles are application-side components. This distinction was clarified in a final GPT-6.1 reader review. The current implementation remains unchanged.

These model recommendations are editorial inputs, not independent validation of runtime behavior or customer value. The raw reviews deliberately remain distinguishable from adopted copy. We rejected or corrected suggestions that described validation as authorization, the private event core as a public routing envelope, local fixture tests as universal guarantees, finality labels as settlement, or separate payment fixtures as a demonstrated lifecycle of one payment. Adapters cannot silently infer missing conventions, and source identities remain distinct.

The implementation counts and scope stay fixed: three bounded profiles; independent RFQ agreement on 35 vectors (four accepted, 31 refused); 291 proposed vocabulary entries; two read-only fixture chain slices with 28 checks; 56 PostgreSQL recovery checks and four process kills for a fixture-authorized report-row effect. Production authentication, live finality, full protocol integration and customer baselines remain separate work.

## Review provenance

`review-manifest.json` records the baseline/input hashes, selected models, capture method, completed artifacts and CLI execution metadata. Model choice is recorded from the orchestration tools/CLI arguments; this is local provenance rather than a signed provider attestation. Two long-running first Grok attempts were terminated before producing final text and restarted with explicit single-turn invocation; they are not counted as completed reviews. Successful final reports are the nine artifacts listed above.

## Humanizer pass

The user requested Humanizer for all public website prose and then its local installation. [Humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md), version 3.1.0, was installed with the Codex skill-installer into `/home/hoskinson/.codex/skills/humanizer`. Its source commit and skill hash are recorded in the manifest.

The pass covered Overview, Implementation and Data Model, plus the source prose used by workflow controls, use-case scenarios and architecture/journey panels. It replaced repeated paired slogans, staged contrasts and vague qualifiers with direct statements, then checked for lost facts and repeated sentences. Technical constraints, source assertions, proposed-versus-tested distinctions, formulas, identities, rankings, link targets and the canonical requirement register remain intact. Static use-case cards were regenerated from their editorial source. Raw model reviews remain evidence of what the reviewers said and were not rewritten.

Developer suggestions were also checked against actual paths and validation behavior. We linked the reproducible reference commands rather than copying an incorrect catalog-test path or suggesting that profile/hash matching alone establishes acceptance. Cleartext limits were not turned into a sealed-wire fit claim.

Validation passed after the prose pass: Data Model routes from the existing tabs, eight jump targets, native disclosures, 320–1440px layouts, 200% text without horizontal overflow and JavaScript-disabled reading; existing three workflows, nine components, ten native use-case cards, journey focus and three Implementation sprint sections. JavaScript syntax, static links/anchors/IDs, nine saved-review hashes and documentation references were checked. The canonical use-case register and its generated data snapshot are unchanged. These checks validate the presentation and provenance, not runtime production readiness.
