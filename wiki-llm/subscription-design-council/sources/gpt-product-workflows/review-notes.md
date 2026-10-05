# Review record

2026-10-05; reviewer gpt-product-workflows.

Approach: inspect implementation and exact contract first; compare primary discovery/triage practices; inspect captured images; propose journeys and orthogonal state behavior; run incumbent lifecycle tests. No UI edit or Git commit.

Intermediate findings: nine event fixtures map to six categories; three payment examples repeat one followable category; inspect opens distant raw JSON; optional Moth precedes discovery; one non-closed subscription per category; title/category-only search; all runtime/preferences currently in tab memory. Existing tests passed via `node website/tests/subscriptions.cjs`.

Decisions: choose directory-first because user confirmed it; borrow Feedly's discover/follow/folder sequence and GitHub's explicit read versus completion distinction; retain canonical category runtime; treat hundreds of synthetic aliases as catalog stress only; preserve whole-shard/local-selection and separate authority boundaries. Reject auto-read/auto-processing and pretending alias labels are authenticated sources.

Actually inspected images: incumbent tiles 0000, 0001, 0002; GitHub inbox tiles 0000 and 0001; Feedly follow tile 0000. Other captured tiles were not used as inspected visual evidence. Local capture default width is 875px. Documentation screenshots establish documented patterns, not current authenticated competitor experience. PixelRAG pixelshot 0.4.0 CDP captures; no GPU/embedding-performance claim.

Failed discovery: Scrapling Google search `https://www.google.com/search?q=site%3Adocs.feedly.com+organize+feeds+folders+follow` returned HTTP 200 redirect/trouble-accessing interstitial with no useful results. Rejected as research evidence. Feedly's public documentation index/category links supplied article discovery instead.

Limits: no customer usability study; no actual wallet extension session; no physical phone/gesture test; proposal not implemented or performance-tested; no durable journal integration; no verified multi-source catalog. Root will synthesize independently authored council reports.
