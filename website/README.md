# Midnight Express architecture page

Static architecture showcase assembled from ten agent assignments: system map, message journey, membership/admission, endpoint privacy, recovery/storage, ledger authority, developer experience, use-case portfolio, editorial/accessibility, and GPT visual generation.

Open `dist/index.html` or serve `dist` with any static HTTP server. The page requires no build. Use-case content in `dist/use-cases.js` is a snapshot of the canonical product register, sorted by recommended rank. Regenerate it when requirements change.

The interactive component map, event journey and ten expandable use cases distinguish existing primitives from proposed integrations and future-release capabilities. All technical diagrams and controls use HTML/CSS/JavaScript; generated visuals are conceptual metaphors.

## Visuals

Built-in GPT image generation produced exactly two illustrations, with no retries. Final project assets: `dist/assets/transport.webp` and `dist/assets/recovery.webp`. Full prompts and generation mode are recorded in [image-prompts.json](dist/assets/image-prompts.json). PNG masters remain in the local architecture work directory. ImageMagick converted the inspected outputs to WebP for the website.

## Review and validation

Nine written reviews are saved under `../reviews/architecture-page`; the tenth assignment produced the two visuals and prompt manifest. All review suggestions affecting factual correctness and control accessibility were incorporated. JavaScript syntax, local asset references, metadata, and ten-case canonical data ordering were checked. An attempted local headless browser capture did not complete; browser rendering and interaction QA remain unverified. No throughput, privacy or production-integration performance is claimed by this page.

Hosted source is maintained in a separate Sites checkout at `/home/hoskinson/Projects/midnight-express-architecture`. This directory preserves a reviewable copy in the research repository; future edits should synchronize both copies.
