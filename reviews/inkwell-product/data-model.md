# Data model prose review

Baseline: `04a2dc0`. Scope: the public data-model page, unified-model and data-format requirements, Ethereum/Solana studies, and the two current model READMEs. Historical releases and source archives are excluded. No voice profile is active. Applied Inkwell reader-first, Gottlieb structural editing and Le Guin cadence guidance.

## Initial findings

Critical findings:

- **Version ambiguity:** `docs/product-requirements/unified-data-model.md:3,63,87` describes a Python slice and says cross-language agreement is unestablished, although `:43,91` reports the independent v0.2 campaign. Separate the original review from current behavior. `model/evidence/interoperability-results.json` records RFQ-only agreement, unsigned fixtures and no execution.
- **Implementation ambiguity:** `docs/product-requirements/ethereum-application-domain.md:3,77` and `solana-application-domain.md:3,145` describe unimplemented designs without locating the later bounded fixture projections. Keep the proposed comprehensive domains distinct from `model/chains/observations.py` and avoid either erasing that work or promoting it into a live adapter.
- **Activity counts as authority:** `website/dist/data-model.html:118–123` leads evidence cards with “35 RFQ vectors”, “28 fixture checks” and “56 recovery checks”. Lead with the observed behavior, retain finite coverage numbers below it, and keep synthetic-source and production limits adjacent.

Important findings:

- **Undefined machinery:** the opening of `model/README.md:3` stacks profiles, adapters, bundles and projections before saying what an integrator can do. The unified model's `:7–9` has the same problem. Introduce workflow agreements and source translation through their purpose.
- **Workshop residue:** `model/README.md:5` opens with a change log; `data-format-review.md:3,64` repeatedly describes the act of reviewing. Orient the reader to the historical decision and link the current status, then preserve the actual defect and recommendation evidence.
- **Compressed chains of nouns:** `data-format-implementation.md:23–29`, Ethereum `:69–75`, Solana `:137–145` combine evidence, authority and recovery into dense lists. Group them by the decision the integrator must make, without removing any precondition.
- **Repeated framing:** the page repeats the model/schema/profile explanation around `:62–75` and uses “reference-tested” as a benefit label. Define the terms once, replace process labels with what the contract checks, and preserve the RFQ-only independent campaign boundary.
- **Scope obscured by volume:** `model/domains/README.md:3–7` gives entry counts before explaining how to use the catalog. Begin with its role in selecting future contracts and retain counts as inventory scope.

Voice and cadence: the quote arithmetic and lost-reply example on the page are concrete and useful. Technical tables in both chain studies are reference material, not a list-style defect. Preserve their coverage, exact method names and linked provenance. Five-family audit found communication and language problems above; no unsupported promotional importance needs to replace the existing cautious claim boundaries. Necessary uncertainty and domain distinctions stay.

Verdict: retain the technical substance and the worked examples. Rewrite orientation, evidence headings and dense decision paragraphs. A shorter requirements document is not the goal; a reader should know which rules are proposed, which behavior is implemented locally, and what still prevents production use.

## Protected claim inventory

- v0.2 has exactly RFQ, invoice-observation and sandbox-approval event profiles; only RFQ is independently interpreted by Python/Rust/TypeScript. Validation always returns `executes:false`.
- RFQ: whole shares, USD scale 2, exact coefficient arithmetic, declared price basis/perspective, no fees, complete source-bound intent, expiry. Different dealers retain distinct identities/digests.
- Invoice: all three statuses bounded by payable; `effectiveAt <= observedAt <= event.time <= trustedNow`; source assertion does not establish bank finality or accounting allocation.
- Approval: complete proposal, authority domain, execution scope, budget window, stable action identity; a fresh occurrence cannot renew consumption; current permission is checked at the effect boundary.
- Raw grammar, numeric/byte bounds, all code and formulas, schema/type/profile IDs, hashes, paths and link targets are protected.
- Immutable bundles commit definitions/rules independently of implementation bytes. v0.1 remains historical read-only with known defects. Offline hash verification is not authenticated installation or live migration.
- Chain vocabulary has 291 proposed entries, 20 families per chain; original review concerns 267 entries (127 Ethereum/140 Solana; 67 native/94 decoded/27 derived/79 intent). Metadata tests do not validate runtime payloads.
- Read-only Ethereum ERC-20 and Solana legacy TransferChecked fixture projections preserve physical identity, exact zero-inclusive uint256/u64, source/context/decoder evidence and append-only history. No live authenticated RPC, consensus verification or spending authority.
- Recovery is a fixture-authorized report-row sandbox using Umbra commit `f662822765247f0da553347c9819f958a1992d28` and PostgreSQL 17.11. Local atomicity and destination-fixture reconciliation do not establish external exactly-once execution.
- Recorded finite evidence: 80 Python checks; 35 RFQ vectors (4 accepted/31 refused), 15 adapter cases, 3 replay cases; 14 catalog checks; 9 bundle tests; 28 chain fixture checks; 56 recovery checks/4 worker kills. Counts describe coverage, not quality. Partner integration hours, real error rates and ROI are uncollected.
- Chain study method inventories, native finality terms, failure/nonce/fee qualifications, wallet authority distinctions, evidence bounds and privacy requirements remain intact. These are dated research/design requirements, not live capability claims.

## Grounding and verification

Read current validator, chain projector, sandbox host and machine-readable measurement/interoperability/chain/recovery evidence. The evidence supports local fixture behavior only. Graph grounding first returned no matching node for the broad reader-clarity query, then an ambiguous Gottlieb query; the explicit-node attempt and measurement results follow below. No runtime tests were rerun for these prose-only changes.

## Applied revision and cadence check

The public page now introduces the business need and defines adapters at first use. Contract bundles get an application-level explanation. Evidence headings describe matching interpretation, preserved transfer history and one report write; the original finite sample counts remain in the supporting paragraphs. Current model documentation explains what a developer can run before listing the strict rules. The two chain studies identify the later fixture projections without promoting their broad proposed inventories to implemented support.

The unified-model status now matches v0.2: independent interpretation is RFQ-only; other profile checks remain local reference evidence. Historical review language identifies the original corpus and pre-correction defects. The implementation matrix leads with the behavior observed and keeps coverage in the same row. Technical reference tables remain because their distinctions are useful to implementers.

The explicit graph node `gottlieb_existing_pattern_1_review` resolved successfully, including machinery in prose, workshop voice, sentence uniformity and repeated contrast findings. No profile overrides were applied.

Le Guin pass: read the connected prose after structural changes, split long authority/precondition runs at the point where interpretation turns into execution, and repair newly repeated fronted conditions. The first actual displacement invocation exited 1: fronted prepositional phrases rose from 5.6 to 13.2 per 1,000 sentences (+136%), while expletive openings fell. Direct subject-led repairs removed that new tic without deleting its preconditions. The final invocation exited 0. This is an editorial diagnostic, not a quality certificate.

Extraction: `/tmp/inkwell-data-model/extract.py` creates `ch01.md`–`ch08.md` in `/tmp/inkwell-data-model/{before,after}`. Baseline originals were saved before editing. HTML extraction uses paragraph text only, excluding tags, navigation and cards’ headings. Markdown extraction removes headings, table rows, fenced commands, and list scaffolding; it retains connected prose, removes link destinations and inline-code delimiters. Technical tables and all code were reviewed separately for preservation.

Actual command:

```bash
python3 /home/hoskinson/Projects/inkwell/narrative/metrics/displacement.py /tmp/inkwell-data-model/before /tmp/inkwell-data-model/after
```

Final output:

```text
before: 10,708 words in /tmp/inkwell-data-model/before
after : 11,254 words in /tmp/inkwell-data-model/after  (+5%)

habit                                before    after    change   per
repeated sentence openers              40.4     48.6      +20%     1,000 sentences
fronted participles                    18.1     18.4       +2%     1,000 sentences
fronted prepositional phrases           5.6      5.3       -6%     1,000 sentences
expletive openers (it/there is)         8.4      3.9      -53% dn  1,000 sentences
em dashes                               5.6      5.3       -5%     10,000 words
semicolons                            145.7    143.1       -2%     10,000 words
-ly adverbs                            96.2     90.6       -6%     10,000 words
paragraph-final aphorisms              17.7     16.4       -7%     100 paragraphs
polysyndeton (3+ ands)                  8.4      5.3      -37% dn  1,000 sentences
very short sentences                   29.2     25.0      -15%     1,000 sentences
sentence length stdev                   6.2      6.0       -4%     words
mean sentence length                   14.5     14.4       -1%     words

Habits fell with none rising. That is what a revision should look like:
  down expletive openers (it/there is): 8.4 -> 3.9 (-53%)
  down polysyndeton (3+ ands): 8.4 -> 5.3 (-37%)
```

`compute_kpis.py` was also run on the public page’s extracted before/after prose: sentence-length variance 33.0 → 33.3. These measurements describe the sample; they do not assess technical correctness or reader comprehension.

Preservation comparison found identical multisets of Markdown link targets, HTML hrefs/IDs, inline code, and fenced code across every owned file. Requirements, native method inventories, numbers, formulas and authority/evidence limits were checked against the protected inventory. The semantic clarifications above are supported by the current validator, chain projector and recorded evidence. `git diff --check` passed. Runtime behavior was not changed and runtime tests were not rerun. Parent owns browser and independent target-reader review.
