# Research record

Reviewer: gpt-consensus-architecture. October 5, 2026. Concise approaches and decisions, not private reasoning transcripts.

Approach: read the running implementation and behavioral tests first; distinguish event examples from subscribable scope; inspect current visual output; inspect primary feed-reader discovery/search patterns; design presentation-state ownership separately from protocol and wallet authority. The user-confirmed feed-directory default was treated as settled.

Intermediate findings:

- Nine stream rows map to six category watches. Payment examples are repeated catalog choices that produce the same watch.
- Current UI has no persistence API, catalog entities, or organization data model. Runtime guards and replay/checkpoint tests pass.
- Existing subscription schema is closed, so feed/folder IDs belong in presentation metadata rather than being appended to intent JSON.
- Feedly documents discover → follow → folder. Inoreader's September 2026 primary article shows a configuration/preview split and explicit account/public search scopes. GitHub documents read/unread separately from done and saved.
- Chose deterministic pagination before virtualization, optional organization after/beside follow, and separate saved references from active runtime state. Only six canonical demo scopes receive Follow controls. Hundreds of synthetic aliases receive Save/Preview and explicit shared-scenario disclosure; catalog stress does not establish independent watches or protocol conformance. These are proposed dispositions, not measured performance results.

Exact visual inspections:

- `incumbent-tiles/127.0.0.1_8876_subscriptions.html.png.tiles/tile_0000.jpg`
- `incumbent-tiles/127.0.0.1_8876_subscriptions.html.png.tiles/tile_0001.jpg`
- `incumbent-tiles/127.0.0.1_8876_subscriptions.html.png.tiles/tile_0002.jpg`
- `inoreader-product-tiles/www.inoreader.com.png.tiles/tile_0000.jpg`
- `inoreader-product-tiles/www.inoreader.com.png.tiles/tile_0001.jpg`
- `inoreader-search-2026-tiles/www.inoreader.com_blog_2026_09_introducing-mentions-redesigned-search-and-smarter-monitoring-feeds.html.png.tiles/tile_0002.jpg`
- `inoreader-search-2026-tiles/www.inoreader.com_blog_2026_09_introducing-mentions-redesigned-search-and-smarter-monitoring-feeds.html.png.tiles/tile_0003.jpg`

Other captured tiles were not inspected or relied upon. Inoreader's cookie banner occludes some lower content, so only visible embedded UI and extracted article text support the report. No authenticated competitor session was examined. PixelRAG was used for CDP capture with one CPU-side worker, not GPU inference or scoring.

Online discovery, all through Scrapling Fetcher:

- `https://www.google.com/search?q=site%3Adocs.feedly.com+add+feed+organize+folders` and `https://www.google.com/search?q=site%3Ainoreader.com%2Fblog+folders+discover+feeds`: HTTP 200 but redirect/trouble-access content only. Rejected as sources.
- `https://docs.feedly.com/`, `/category/482-organizing-feeds-add-remove`, and `/category/439-websites`: HTTP 200, official article links inspected. Landing/category pages were used to discover URLs, not as evidence for authenticated layout.
- `https://www.inoreader.com/blog/`: HTTP 200, official September 14, 2026 search article link discovered.
- `https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/managing-notifications-from-your-inbox`: HTTP 404. Rejected.
- `https://docs.github.com/en/subscriptions-and-notifications/how-tos/manage-notifications/manage-your-inbox`: HTTP 404. Rejected.
- `https://docs.github.com/en/subscriptions-and-notifications`: HTTP 200, canonical inbox and filter URLs discovered from actual links.

Accepted sources: incumbent, inoreader-product, inoreader-search-2026, feedly-discover-follow, feedly-follow-folder, github-inbox, github-filters. Each corresponding `.json` contains exact request/final URLs, retrieval timestamp, tool, status, hashes, and capture paths where applicable. The report records publication/update dates and the inspection scope. No browser/WebSearch/WebFetch substitute was used.

Validation run: `node website/tests/subscriptions.cjs`, passed. No product edits, shared provenance edits, commits, external messages, secret access, or subagents. Source artifacts and the reviewer report are the only deliverable writes.
