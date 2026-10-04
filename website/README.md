# Midnight Express architecture page

Static product and architecture showcase, first assembled from ten agent assignments: system map, message journey, membership/admission, endpoint privacy, recovery/storage, ledger authority, developer experience, use-case portfolio, editorial/accessibility, and GPT visual generation.

Open `dist/index.html` or serve `dist` with any static HTTP server. The page requires no build. Use-case cards are static HTML, so all ten remain readable without JavaScript. `dist/use-cases.js` preserves a snapshot of the canonical register. `dist/product-content.js` holds illustrative editorial scenarios and the three interactive business walkthroughs. After changing the register or editorial card copy, run `python3 website/build-content.py` from the repository root to regenerate the cards and canonical snapshot. There is no framework build or dependency installation.

The interactive component map, event journey and ten expandable use cases distinguish existing primitives from proposed integrations and future-release capabilities. All technical diagrams and controls use HTML/CSS/JavaScript; generated visuals are conceptual metaphors.

## Visuals

Built-in GPT image generation produced exactly two illustrations, with no retries. Final project assets: `dist/assets/transport.webp` and `dist/assets/recovery.webp`. Full prompts and generation mode are recorded in [image-prompts.json](dist/assets/image-prompts.json). PNG masters remain in the local architecture work directory. ImageMagick converted the inspected outputs to WebP for the website.

## Review and validation

Nine written reviews are saved under `../reviews/architecture-page`; the tenth assignment produced the two visuals and prompt manifest. All review suggestions affecting factual correctness and control accessibility were incorporated. JavaScript syntax, local asset references, metadata, and ten-case canonical data ordering were checked. The first capture attempt did not complete. During the eight-agent product rewrite, headless Chromium checks subsequently passed for desktop/mobile rendering, three workflow controls, nine component selectors, journey focus, ten native cards, 200% text without horizontal overflow or clipping, no script exceptions and core content with JavaScript disabled. No throughput, privacy or production-integration performance is claimed by this page.

GitHub Pages is now the publishing target requested by the user. The earlier Sites deployment is a historical architecture edition; its local checkout at `/home/hoskinson/Projects/midnight-express-architecture` can be synchronized for development, but GitHub Pages publishes this repository’s `website/dist`.

## GitHub Pages

The architecture page is published from the root of the dedicated `gh-pages` branch. That branch contains only `website/dist`, including `.nojekyll`; the research documents and original PDF are excluded. The site is public and the repository remains private.

After committing website updates on the research branch, publish the committed static files from the repository root:

```bash
git subtree push --prefix=website/dist origin gh-pages
```

GitHub Pages deploys pushes to `gh-pages`. Changes on the research branch alone do not update the hosted page.

## Product explanation review

[Eight product-manager reviews](../reviews/product-page/README.md) informed the product-first reading order, three business scenarios, expanded actor/trigger/example information across ten use cases, glossary, FAQ and clearer stage boundaries. These are editorial improvements, not customer validation.

## Unified meaning and prototype validation

The [unified model proposal](../docs/product-requirements/unified-data-model.md) synthesizes five Scrapling literature studies. The [reference model](../model/README.md) supplies closed schemas and unsigned conformance fixtures. The [three-sprint plan](../docs/product-requirements/prototype-sprints.md) synthesizes ten design reviews. The static Implementation tab is `website/dist/implementation.html`; it works without JavaScript. These are design/reference artifacts, not completed runtime sprints.

The Implementation page also summarizes Ethereum/Solana application domains: chain lifecycle and rollback, RPC/subscriptions, state, tokens/NFTs, wallets and program-specific DeFi/bridge semantics. These are proposed domain inventories; no chain adapter runtime is included.

Validation for this update: original workflow/component interaction checks and Implementation route/anchors/native details passed in headless Chromium at desktop/mobile widths, 200% text and with JavaScript disabled. Three model schemas self-validate and the reference's 51 conformance checks pass. Archive integrity: 140 fetch records, 253 raw/text hashes checked without mismatch. None of these checks establishes completed prototype sprints, deployed chain adapters, cryptographic acceptance or market demand.

## v0.2 reference release

The Implementation tab now distinguishes implemented conformance/local components from the proposed full protocol sprints: 80 Python checks, 35 independent RFQ vectors, 14 corrected-catalog checks, 28 read-only chain cases, nine immutable-bundle checks and 56 real PostgreSQL sandbox/recovery checks. Review defects reject under v0.2; the original v0.1 remains historical read-only. Source/authority are fixtures, not production authentication or consensus verification.

## Dedicated Data Model guide

`dist/data-model.html` explains the business interpretation layer independently of the implementation sprint plan. [Five product-manager reviews](../reviews/data-model-page/README.md) shaped the reading order: business ambiguity, concrete two-format quote, shared core/contracts/adapters, three pilot workflows, replay/versioning, Ethereum/Solana scope, finite implementation evidence and partner onboarding/FAQ.

Main-navigation links on Overview and Implementation reach the new tab. Quote cards, stack sequence and native disclosures remain readable without JavaScript or private repository access. The public page distinguishes the three v0.2 profiles, RFQ-only independent interpreters, 291 proposed vocabulary entries, two read-only chain fixture slices and tested fixture-authorized Umbra report-row recovery. Intended business benefits require partner measurements.

Validation: Data Model navigation from both existing pages, eight section targets, native disclosures, 320–1440px layouts, 200% text without horizontal overflow and JavaScript-disabled reading passed in Chromium. Existing product interactions and Implementation navigation/details still pass. Local assets/anchors/IDs and review/documentation links resolve.

## Expanded reader guidance

A second [nine-model editorial review](../reviews/data-model-page/round-2/README.md) uses three Gemini 3.1 Pro agents through `agy`, three Grok 4.7 CLI agents and three GPT-6.1 agents. The Data Model guide now includes a reader route, worked quote conversion/refusal, model/schema/protocol definitions, interpretation/evidence/permission/effect decisions, payment clock examples, exact contract versioning, lost-reply recovery, transfer lineage, partner review questions and an expandable glossary. The v0.2 runtime and its measured scope are unchanged; review suggestions were checked against the implementation before adoption.

Humanizer 3.1.0 was installed locally and applied to public page prose and dynamic editorial copy. The pass preserves the canonical use-case register, technical literals and current implementation boundaries; generated static cards remain synchronized with their editorial source. Raw review artifacts are preserved separately.
