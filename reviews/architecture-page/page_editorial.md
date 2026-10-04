# Page editorial and accessibility review

Reviewed `dist/index.html`, `dist/app.js`, `dist/styles.css`, and `dist/use-cases.js`. Static review only.

## Necessary corrections

1. **Move keyboard focus when “Explore this component” navigates.** In `app.js`, the journey button selects a component and calls `scrollIntoView()`, but focus remains on the journey button below the viewport. Focus the corresponding architecture component button after scrolling, or a focusable detail heading. The next Tab must continue from the architecture content that has just been revealed.

2. **Expose the relationship between selectors and detail panels.** Add `aria-controls="component-detail"` to the architecture buttons and `aria-controls="journey-detail"` to journey buttons. Give the detail regions meaningful accessible names. Both panels currently announce updates with `aria-live`, but selector state alone does not identify which content the controls change. On mobile the architecture panel follows all nine nodes, so this association is especially useful.

3. **Correct the map’s implied serial and endpoint placement.** The receiving-endpoint lane contains OpenMLS, although the detail copy correctly places group payload protection before sealing and applies group state at both endpoints. The vertical connector then leads from receiving processing to the anchor/authority row, implying that anchor production follows reception. Label OpenMLS as endpoint session security used at sender and receiver; distinguish the parallel anchor branch from the optional consumer effect path. A visible map annotation is sufficient if restructuring the diagram is impractical. The detail text already states the correct relationships, but the map needs to agree.

4. **Use requirement links that actually reach the named material.** The component links labelled “Read the store requirements,” “Read the ledger requirements,” and “Read the authority requirements” all open the repository root. Point them at the requirement/design source section supporting the corresponding component, or change the labels to “Open the project repository.” Likewise, “Read the MPE design” should reach the design document rather than the repository root. Existing source links at the bottom demonstrate that direct document destinations are available.

5. **Keep the future recovery guarantee visibly conditional inside its connection copy.** `components.recovery.connection` states that local effects, deduplication, outbox, checkpoint and cursor are “committed together,” while its gate and the journey identify that capability as proposed. Change this sentence to “Proposed atomic processing: … committed together” so a reader inspecting only “How it connects” does not infer that current UmbraDB supplies this transaction boundary.

## No additional necessary copy corrections found

The page consistently labels the architecture as proposed, use-case value as unvalidated, distinguishes persistence/inclusion/processing/business acknowledgement, identifies destination idempotency, and preserves mobile, authority, group-security and ledger capability gates. Native buttons and `details` provide baseline keyboard operation; focus-visible and reduced-motion styles are present. Responsive rules retain visible control text.
