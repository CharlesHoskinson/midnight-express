# Specification page editorial record

Owned artifacts: `website/dist/specification.html`, `specification.css`, `website/tests/specification.cjs`, and this note.

The public explanation starts with concrete v0.2 workflow rules, then explains theorem implications and their assumptions. The examples use the existing whole-share USD quote, partial payment observation and sandbox WriteReport scope. Exact profile and event type names follow `model/README.md`. Watch controls are a proposed local control plane and are discussed separately from admitted business events.

The humanizer skill was applied to remove staged contrasts, numbered promotional headings, forced parallel lists and unsupported claims. Necessary distinctions between mathematical guarantees and implementation evidence remain explicit. Proof totals are not presented as product evidence.

The page is static HTML with native details/summary disclosures; all core explanations remain available with JavaScript disabled. Equations have adjacent definitions and ordinary-language examples. CSS extends the existing site theme and reflows navigation and mathematical expressions for narrow screens and enlarged text. Public copies of Lean sources are required so access to the private GitHub repository is optional.

## Evidence and proof alignment

Read `model/README.md`, `website/dist/data-model.html`, existing styles and subscription browser tests before drafting. The final proof inventory names actual theorems read from `formal/lean/MidnightExpress/Model.lean` and `Validation.lean`. Both module authors confirmed compilation. The inventory includes validation soundness/completeness, exact envelope dispatch, exact decimal quote multiplication and validity, complete invoice evidence, scoped approval predicates, sequential replay and non-execution. General claims are confined to the typed Lean definitions and supplied context.

Replay compares supplied digest strings; it does not derive them from the payload. This boundary is stated beside the replay proof explanation. Structural business-intent equality is explained separately. Local watch intent, delivery state and cursor behavior remain outside the verified business-profile model. No theorem counts or total test counts appear in the public page.

## Browser verification

`node website/tests/specification.cjs` runs its own temporary HTTP server and Chromium, with external resource requests blocked and JavaScript disabled. It checks native keyboard disclosures, skip navigation, exact navigation order/current-page indication, core rules and scope caveats, links and fragments, downloadable source files, draft-placeholder removal, and viewport reflow at 1440, 720, 390 and 320 pixels with 100% and 200% root text size. The first pre-publication run correctly failed on missing Lean source copies. Layout and keyboard checks passed before those copies were available.

Desktop and 390-pixel screenshots were also inspected using the local preview. The page matches the existing dark theme, keeps the current navigation visible, and wraps the introductory prose naturally. No page script or framework dependency was added.

Final verification passed after the root agent copied the checked Lean sources into `website/dist/formal/lean/`. The browser test successfully fetched every public source link and checked all local fragments. `git diff --check` also passed for the owned artifacts. Both the validation agent and root confirmed the full pinned Lean build, fixture bridge and axiom audit; the public proof status reflects those checks. The final theorem inventory was compared with the frozen source declarations.

External research was unnecessary for the page: its business claims derive from checked-in reference documentation. No external search was performed.
