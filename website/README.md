# Midnight Express website

The website explains the proposed product, its shared data model and the evidence needed to build the full protocol. It publishes static files from `dist`; no framework build or dependency installation is required.

## Edit and preview

Open `dist/index.html` or serve `dist` with a static HTTP server. The public reading routes are:

- `dist/index.html`: workflows, architecture, use cases, glossary and FAQ.
- `dist/data-model.html`: business meaning, contracts, adapters, versioning and the current reference’s limits.
- `dist/implementation.html`: current local evidence, proposed protocol sprints and acceptance gates.

Use-case cards are generated static HTML and remain readable without JavaScript. `dist/use-cases.js` preserves a snapshot of the canonical register; `dist/product-content.js` supplies editorial scenarios and interactive business walkthroughs. Changes to the register or editorial card copy require regeneration of the cards and canonical snapshot. Run this from the repository root:

```bash
python3 website/build-content.py
```

Technical diagrams and controls use HTML, CSS and JavaScript. The generated illustrations, `dist/assets/transport.webp` and `dist/assets/recovery.webp`, are conceptual images. Their prompts and generation mode are in [image-prompts.json](dist/assets/image-prompts.json); the PNG masters remain in the local architecture work directory.

## Check meaning and behavior

Keep current implementation evidence distinct from proposed capabilities. The [reference model](../model/README.md) implements bounded conformance and local prototypes. The [unified model proposal](../docs/product-requirements/unified-data-model.md) defines the intended interpretation layer; the [sprint plan](../docs/product-requirements/prototype-sprints.md) describes protocol work still to complete. Ethereum/Solana domain coverage remains a proposed inventory. Existing read-only chain projections consume supplied fixtures, and the Umbra sandbox performs a fixture-authorized database report-row write.

Verify navigation, section anchors, native disclosures, workflow controls, component selection and journey focus after an edit. Check desktop and mobile layouts, enlarged text and core reading with JavaScript disabled. Look for horizontal overflow, clipping and script exceptions; also check JavaScript syntax, local assets, IDs, metadata and canonical use-case ordering. Prior Chromium checks covered those behaviors, but each change needs appropriate verification.

These website checks establish presentation behavior. They do not establish throughput, privacy, cryptographic acceptance, production integration or customer demand. Claims about the reference must remain within its fixture scope, and intended business benefits need partner measurements.

## Publish to GitHub Pages

GitHub Pages serves the root of the dedicated `gh-pages` branch. That branch contains only `website/dist`, including `.nojekyll`; it excludes the research documents and original PDF. The site is public and the repository remains private, so public readers cannot follow repository links without access.

After committing website updates on the research branch, publish the committed static files from the repository root:

```bash
git subtree push --prefix=website/dist origin gh-pages
```

GitHub Pages deploys pushes to `gh-pages`. A commit on the research branch alone does not update the hosted page. The earlier Sites deployment is a historical architecture edition; its checkout at `/home/hoskinson/Projects/midnight-express-architecture` can be synchronized for development. This repository’s `website/dist` is the GitHub Pages source.

## Editorial sources and history

The [architecture reviews](../reviews/architecture-page/), [product explanation reviews](../reviews/product-page/README.md), [Data Model reviews](../reviews/data-model-page/README.md) and [expanded reader-guidance reviews](../reviews/data-model-page/round-2/README.md) explain earlier design decisions. They are editorial evidence, not customer validation.

The [Inkwell implementation review](../reviews/inkwell-product/implementation.md) records the current structural findings and protected technical claims. An [archived website account](../reviews/inkwell-product/implementation-before/website-readme.md) preserves earlier review assignments, validation reports, image-generation details and Humanizer provenance.
