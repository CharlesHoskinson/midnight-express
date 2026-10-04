# Product overview editorial review

Scope: index.html, product-content.js, app.js, top-ten-use-cases.md, recommended-stack-and-use-cases.md and feature-considerations.md. References below use the pre-edit baseline 04a2dc0. No voice profile is active. Generated card interiors are excluded; the parent editor regenerates them from the canonical source.

## Critical findings

1. **The product definition follows the slogan.** index.html:35–40 opens with “Keep sensitive work moving,” which could describe many products. Lead with private event coordination and explain the cross-organization record/approval problem before asking readers to inspect the stack.
2. **Workshop structure displaces the workflow.** top-ten-use-cases.md:23–49 and each subsequent use-case block divide a connected business story into thirteen labeled fragments. Readers need to understand who sends what, why another organization needs it, and what happens next. Give each candidate a narrative opening, then retain the useful requirement and acceptance reference fields.
3. **Proposal and implementation drift.** app.js:3–11 describes several proposed components in the present tense; top-ten-use-cases.md:290 says all workflows “use” the chosen database. Establish the architecture as proposed and preserve the narrower evidence of local report-row recovery. Library selection is not integration acceptance.

## Important findings

- **Abstract benefit wording (content).** “Narrowed exposure of claimant facts” at top-ten-use-cases.md:268 obscures the practical benefit. Describe sharing evidence with assigned roles while reducing repeated requests; retain hypothesis status.
- **Compressed technical inventory (language and style).** Slashes, plus signs and dense requirement vocabulary in the stack recommendation and app.js make the product story sound like implementation notes. Keep exact technical constraints in reference material and connect explanatory clauses in ordinary sentences.
- **Activity as authority (communication).** “Three-agent extraction/research” in the introductory research links foregrounds how the review was staffed. Keep the links, label them by their evidence subject.
- **Repeated framing (filler).** Feature considerations opens by explaining corrections to an earlier interpretation. Open with which work these candidates enable and retain unverified status.

## What works

The interactive quote/invoice/agent examples already explain concrete actions and distinguish receipts from decisions. The site's privacy caveat names visible metadata, and the final FAQ preserves the limited scope of local evidence. Retain these facts. Reference tables and requirement links serve comparison and traceability and should remain.

## Claim inventory

- MPE is proposed private event/workflow infrastructure; local conformance and recovery prototypes do not establish production integration.
- First priority is backend/desktop RFQ coordination, followed by invoice matching and bounded human approvals. Rankings and benefits are recommendations, not measured demand or savings.
- Authorized endpoints hold plaintext and keys; connection, shard, timing and size exposure remain. Launch symmetry does not provide forward secrecy or origin anonymity.
- Local recognition avoids semantic subscriptions upstream. Ordinary coordination requires no per-event ledger transaction.
- Midnight finalized Registry state governs admission; one proposed RLN proof combines membership/quota/abuse binding. Preserve the 4096-byte and 10-ms unmeasured targets and abuse limitations.
- Delivery, persistence, anchoring, processing and signed business acknowledgement are distinct. Contract effects require signed authority, atomic replay protection and anchored-message binding; carried events require exact bytes and successful applied phase.
- Baseline retention is 48 hours. History, attachment access, removal/rekeying and copies already obtained retain their separate limits.
- Umbra/PostgreSQL serves trusted Node hosts, SQLite standalone Rust/client deployments. saveAndAdvance covers checkpoint/cursor; local report-row composition is narrower than complete MPE processing, writer ownership and protected restore.
- Preserve every UC and requirement identifier, ranked ordering, acceptance condition, metric, link, schema key, UI hook and executable operation.

## Verdict

Rewrite the openings and the detailed use-case narratives. Preserve technical reference fields and the stronger existing scenarios. The main defect is fragmented explanation and uneven status language, not missing slogans or examples.

## Applied decisions and cadence

The website now defines the proposed product before explaining the record and permission problem. Each use case opens with its participants and workflow in connected prose; the technical acceptance conditions and links remain available beneath it. Component descriptions distinguish proposed integration from the narrower local prototype. The prose retains visible metadata, off-chain acceptance, destination duplicate protection, and all independent authorization and recovery requirements.

Cadence revision combined the repeated actor/trigger/benefit fragments and removed an unnecessary “In this scenario” opener introduced during editing. Exact HTML structure/attributes, generated card interiors, Markdown link targets and requirement identifiers were compared against baseline and preserved. Masking JS string literals leaves identical executable source in app.js. Both edited JS files pass syntax checks. These checks cover editorial preservation, not protocol correctness.

The displacement extraction uses HTML paragraphs outside generated cards, JS narrative fields (excluding controls and program text), and Markdown paragraphs outside tables, fenced code and traceability lists. Files use the checker's required ch*.md naming. This is the authored narrative sample, not the complete rendered website.

An initial displacement run returned exit 1 because fronted prepositions rose from 2.1 to 4.1 per thousand sentences after adding “In this scenario.” The opener was removed; the final run below returned exit 0.

- Before sentence_length_variance: 28.9.
- After sentence_length_variance: 30.0.

```text
before: 5,592 words in /tmp/mpe-overview-before
after : 6,113 words in /tmp/mpe-overview-after  (+9%)

habit                                before    after    change   per
repeated sentence openers              41.8     48.7      +16%     1,000 sentences
fronted participles                    31.4     32.5       +3%     1,000 sentences
fronted prepositional phrases           2.1      2.0       -3%     1,000 sentences
expletive openers (it/there is)         4.2      0.0     -100% dn  1,000 sentences
semicolons                            169.9    152.1      -10%     10,000 words
-ly adverbs                            64.4     58.9       -9%     10,000 words
paragraph-final aphorisms              34.3     28.6      -17%     100 paragraphs
very short sentences                   77.4     58.8      -24%     1,000 sentences
sentence length stdev                   5.2      5.3       +2%     words
mean sentence length                   11.6     12.3       +6%     words

Habits fell with none rising. That is what a revision should look like:
  down expletive openers (it/there is): 4.2 -> 0.0 (-100%)
```

## Unresolved material findings

No new technical defect was resolved as a prose edit. Production protocol integration, privacy/performance measurements, customer value and the independent extension requirements remain unvalidated as stated in the source. The parent editor must regenerate use-case cards and conduct the independent target-reader review; those activities are outside this file ownership. No voice conformance score applies because no profile is active.
