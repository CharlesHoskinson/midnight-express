# Midnight branding review

The website now follows the [official Midnight Brand Hub](https://midnight.network/brand-hub): near-black `#0A0A0A`, white `#FFFFFF`, electric blue `#0000FE`, and Outfit. Lighter blue is reserved for readable small text and focus indicators. The project keeps its own Midnight Express wordmark and M/E monogram.

The shared system applies to Overview, Data model, Subscriptions, Specification and Implementation. Mint/teal surfaces are replaced with black and charcoal. Redundant eyebrow labels and header editions are removed. The subscription directory retains its native controls and state boundaries. The home page links directly to the directory.

## Generated visuals

The built-in GPT image-generation tool produced:

- [Network illustration](../../website/dist/assets/midnight-express-network-v2.webp): sealed event capsules and electric-blue paths against black.
- [Stack diagram](../../website/dist/assets/midnight-express-stack-v2.webp): publication admission and GossipSub, with parallel opaque-store, receiver and anchor branches. Source checks and consumer progress remain local.
- [Recovery diagram](../../website/dist/assets/midnight-express-recovery-v2.webp): reading markers are separate from processing decisions and contiguous progress. Recovery rechecks authority and preserves pause.

All labels and arrows were inspected against the existing design. These illustrations describe proposed integrations and consumer semantics; they establish no production deployment or formal proof. Diagrams have equivalent HTML descriptions and full-size links. Original generated files remain in Codex’s generated-image directory; project assets are saved locally as WebP. ImageMagick performs encoding only. No semantic raster edits were made.

Complete prompts, output dimensions and hashes are in [generated-assets.json](../../design/branding/generated-assets.json). The optimized visuals total about 233 KB; the locally served Outfit font is about 109 KB. Outfit’s SIL Open Font License is retained.

## Evidence

`website/tests/branding.cjs` checks the actual shared stylesheet and all website tabs. It verifies the black body background, Outfit family, the loaded font registry, image availability, removal of redundant labels, working workflow/component controls, and reflow at desktop, mobile and 320 CSS pixels with 200% text enlargement. A font-registry collision discovered during review was corrected; old font faces retain their original names and Outfit is the only loaded body/display family. Current captures and metrics were regenerated after that correction.

`website/tests/subscriptions.cjs` passes against the new typography and palette, including independent follow configuration, saved history, authority rechecks, read/processing separation, storage failure, stale-tab handling and the explicit wallet connection boundary. `website/tests/subscriptions-zoom.cjs` checks actual Chrome tab zoom at 200%, search/follow and representative computed contrast. The specification browser test and Lean publication guard also pass.

[Site evidence](site-evidence.json), [subscription checks](browser-evidence.json) and [zoom/contrast evidence](zoom-contrast.json) record the checks. Visual inspection covered desktop and mobile layouts, reading pages, the directory and the architecture illustration. Stored page captures include the final font registry cleanup. This is Chromium evidence; it does not establish screen-reader conformance or cross-engine/device coverage.

Impeccable’s detector is clean for the overview and shared brand layer. Its remaining subscription section-padding warning reflects the inherited global section rule; the workspace override removes that border and padding. The rendered directory was inspected. The earlier low-contrast skip-link hover was corrected to white on brand blue.

## Research provenance

Scrapling Fetcher and StealthyFetcher were used for direct Midnight requests, which returned HTTP 429/browser verification. Those challenge pages were discarded and were never treated as brand evidence. The official Brand Hub’s indexed content supplied the palette and typography. Scrapling successfully retrieved Outfit and its license from the Google Fonts upstream repository. [Source notes](../../design/branding/reference/source-notes.json) and [font hashes](../../design/branding/font-sources.json) preserve these distinctions.
