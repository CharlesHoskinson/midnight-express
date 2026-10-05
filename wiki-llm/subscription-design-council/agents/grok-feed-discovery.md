# Feed discovery and information architecture

Reviewer: grok-feed-discovery. Mode: Operate (Impeccable 4.5). This is a design proposal. It does not change the dashboard, the local contract, product requirements, or git.

Root already loaded Impeccable context. This review used `operate.md`, `critique.md`, `clarify.md`, `optimize.md`, and `adapt.md` as lenses. `craft-floor.md` was left unread because no UI was edited. No subagents were launched.

The page under review is the browser-local simulation at `website/dist/subscriptions.html`, served at `http://127.0.0.1:8876/subscriptions.html`. Quote, payment, and approval examples are fixed v0.2 fixtures checked offline. Contract, credential, and operations examples are unsigned mocks. The journal, watches, and inbox live in tab memory. A persona lens is not a principal. A processing checkpoint, a delivery cursor, and an effect are three different facts. Local selectors and whole-shard intake stay independent. Browse categories are not network topics. Browser preferences cannot restore permission or a Moth grant. Moth on this page is API 4.0.1 `connect` / `getConnectionStatus` from a real click, after an origin-wide acknowledgement. This proposal adds no signing and no new connection behavior.

## Incumbent

### What the fresh tab shows

PixelRAG captured three desktop tiles of a fresh load (journal high-water 0). I read all three.

The first screen is the site nav (Subscriptions is the current item), the eyebrow "BROWSER LOCAL SIMULATION", the title "Your local inbox.", three paragraphs that correctly say reload or Reset clears tab memory and that subscribing sends nothing, then the whole Optional Moth wallet section: origin warning, acknowledgement, Discover / Connect / Check / Disconnect, and "disconnected". Browse starts only at the bottom of that tile: Search streams, Category, Consumer mode, and the clipped heading "Shares / USD quote".

The second tile is a single column of examples. Each row is a title, one readable sentence, an evidence line, and two or three buttons. I saw "Subscribe to payments" on Payment pending, Payment final assertion, and Payment reversed. Contract renewal, Credential expiry, and Operations backlog share the same sentence: "Unsigned demonstration reminder; no source authority or business profile is verified." The evidence line is the only distinction, and it sits under the sentence in the same weight as body text.

The third tile shows Operations backlog ending in three buttons, then Expired quote · rejected reference with Inspect example and Simulate this occurrence and no subscribe button. Below that, Subscriptions opens with the pinned demo clock, a 3×3 grid of simulation buttons (intake, review, rejected quote, replay, gap, expire, revoke, reset, export), "Mock local permission: granted… Simulated host journal high-water: 0", and "Choose a stream to create a local subscription." Inbox and quarantine explains the two cursors and the bounds (2 in flight, 4 queued, 16 KiB), then "No local receipts yet. Subscribe and simulate intake." Message detail is collapsed. A dark sticky strip sits at the bottom.

Source and `website/tests/subscriptions.cjs` agree with that picture and add behavior the fresh tiles cannot show:

- State is module variables. Nothing is written to `localStorage` or `sessionStorage`. Reload constructs an empty journal, empty watches, and an empty inbox. The catalog returns only because `subscriptions-fixtures.json` is fetched again.
- Search keeps the field (it is outside the redraw) but `render()` replaces `#streams`, `#subscriptions`, and `#inbox` on every keystroke. An unsaved scope `<select>` is rebuilt from the watch and the user's pending choice disappears. Focus inside the list is lost.
- Search matches `title` plus `category` only. The readable sentence and the evidence line are visible and not searchable. A query that matches nothing leaves `#streams` empty, with no empty-state sentence.
- Consumer mode writes the category select: wallet forces quotes, DApp forces payments, agent forces approvals, human forces all. That is a browse default, and the help text says so, but the control still throws away the family the person had selected.
- One non-tombstoned watch per category. A second "Subscribe to payments" announces "This category already has a subscription."
- The rejected quote fixture cannot be subscribed. Simulate still appears, and it refuses until a quotes watch is active.
- The inbox paints `inbox.slice(-40)` newest first. Older receipts have no Older control. The cap is silent.
- "Mark next item reviewed" advances a contiguous processing cursor. Opening Message detail does not. There is no read flag.
- Reset clears demo memory and says Moth origin grants are unaffected. Tests assert subscribe and intake add no network request, and that the page load does not call the wallet.

The catalog has nine records, not hundreds: two quotes (one accepted, one rejected), three payment statuses, one approval, and three unsigned mocks. Profiles are `rfq.v0.2`, `invoice.v0.2`, and `agent.v0.2`. Mocks have no profile. No record carries sealed wire in the fixture index I extracted. Those nine bodies stay immutable. A hundreds-scale directory has to be synthetic views over this scenario set.

### Heuristics for this surface

Scores are for discovery and navigation on the fresh page, 0–4. The simulation copy and the live region are ahead of the directory.

| # | Heuristic | Score | Finding |
|---|---|---|---|
| 1 | Visibility of system status | 2 | Permission and journal high-water are visible. A row does not show whether that family is already followed. Search has no count. The inbox cap of 40 is invisible. |
| 2 | Match to the task language | 2 | The title says inbox. The first task on screen is a wallet. Rows are called streams, grouped as categories, followed as subscriptions, and delivered as receipts. |
| 3 | User control | 2 | Reset, unsubscribe, and explicit gap acceptance exist. Search redraws destroy an in-progress scope edit. Persona overwrites the family filter. |
| 4 | Consistency | 2 | Evidence lines use a stable pair of phrases. The button names the family while the heading names one example. |
| 5 | Error prevention | 2 | The rejected fixture hides Subscribe. Simulate is still offered on every row and fails after the click if no watch exists. |
| 6 | Recognition rather than recall | 2 | Buttons have text. The person must remember that three payment rows are one watch. |
| 7 | Flexibility | 1 | No documented shortcut for preview or follow. No bulk follow. Search ignores the sentence the row shows. |
| 8 | Aesthetic and minimalist | 2 | The column is restrained and on-brand. The wallet essay and nine demo buttons take the viewport the directory needs. |
| 9 | Error recovery | 3 | The status line names the block: permission, subscribe first, scope edit blocked, tombstone. |
| 10 | Help | 2 | The intro is accurate. The words stream, predicate, cursor, and shard are not defined at the follow button. |

Total 20/40, acceptable, with the directory itself below that. Cognitive-load checklist: single focus, chunking, one decision at a time, minimal choices, working memory, and progressive disclosure all fail. Grouping and a visible title pass. That is high extraneous load. The intrinsic task (choose a family, inspect an example, follow locally, later review a receipt) is small.

Operate notes: the component vocabulary is already plain buttons, selects, and a disclosure. Keep that. The fluid `clamp` on `h1` and the sticky empty announcement bar are secondary. Do not invent a new visual world for the directory.

### Friction, as a person would meet it

Jordan opens the page to find something to follow. The first actions are wallet buttons. The catalog is below the fold. Three payment rows offer the same follow. The button does not say what will be bound (family, profile, predicate `all`, start at latest). Inspect example opens a JSON dump of the canonical record at the bottom of the page, which is the right audit surface and the wrong scent surface.

Alex wants the quotes family again after choosing agent by mistake. The family select jumps to approvals. There is no key to move between families. Typing "final" works only because that word is in a title. Typing "unsigned" or "USD" matches nothing, even though both are on screen.

Sam tabs the page. The skip link and the live region are real. Redrawing the list on each search character drops focus if it was on a row. An empty result is silence. Color is not the only evidence cue; the evidence sentence exists. It is easy to miss because every row has the same shape.

Casey on a 390px screen gets the same stack. I did not capture a mobile tile. `subscriptions.css` wraps controls under 600px, and `subscriptions.cjs` asserts no horizontal overflow at 390×844 with text at 200%. The follow buttons sit in the catalog, far above the thumb, and the sticky announcement occupies the bottom edge. The wallet acknowledgement is a long line above the work.

Riley reloads mid-review. The copy is true: the watch, the cursors, and the receipts are gone. The catalog comes back. There is no "this tab forgot the watch" banner after reload beyond the standing intro, because the empty inbox looks like first use. Those two empty states need different sentences.

## Sources

Retrieval was Scrapling `Fetcher` through `wiki-llm/subscription-design-council/research.py` on 2026-10-05. Metadata, raw bytes, and text live under `wiki-llm/subscription-design-council/sources/grok-feed-discovery/`. Text was treated as data.

PixelRAG is `pixelshot` 0.4.0, CDP, one worker, tile height 1568, network-idle wait. The helper's stderr reports `backend=cdp`. This review claims no GPU. I read every tile listed below with the image reader.

Visual, incumbent. `incumbent-subscriptions`, `http://127.0.0.1:8876/subscriptions.html`, HTTP 200, retrieved `2026-10-05T20:06:29Z`, text sha256 `4e565663b6cf3bab95199fd31723a040ad840336521cea195a012d7d8ac9104c`. Three tiles, all read: nav and wallet through the search row; the example stack through Operations backlog; rejected quote, the nine demo buttons, empty watches, empty inbox.

Visual, primary comparison. `github-inbox`, final URL `https://docs.github.com/en/subscriptions-and-notifications/how-tos/viewing-and-triaging-notifications/managing-notifications-from-your-inbox`, HTTP 200, retrieved `2026-10-05T20:08:34Z`, text sha256 `cda0ddeb61d7d0383564ca0525a5be00db79e76e63e4593cbada2d725d66c90c`. Three tiles, all read. Tile 0 is the article through the triage table (Save, Done, Unsubscribe, Read). Tile 1 is bulk selection, default filters, and custom-filter steps, including the query `repo:… reason:participating` and a tip to preview a query before saving it. Tile 2 is the Filters dialog: Assigned `reason:assign`, Participating, Mentioned, Team mention, Review requested, and a custom row `octo-project` / `repo:octo-corp/octo-project reason:participating`. Footer copyright is 2026. The HTML I searched had no `dateModified`.

Text, same GitHub docs tree. Robots on `docs.github.com` is `User-agent: *` with no Disallow. Three pages, then stop.

- `github-about-notifications`, `https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications`, `2026-10-05T20:08:34Z`, text sha256 `f0d2198451e38a7874241e86656120e1acb525c9aa51b6902aa822fc83d8b789`. A subscription is ongoing attention to a conversation, a repository, or a class of repository activity. A notification is one update for activity already subscribed. The inbox shows a reason label (`mention`, `subscribed`, `review requested`) and filters with `reason:review-requested`. Read, unread, Save, and Done are inbox states. Done is kept 3 months. Saved is kept until unsaved. Unread and Done are different.
- `github-viewing-subscriptions`, `https://docs.github.com/en/subscriptions-and-notifications/how-tos/managing-subscriptions-for-activity-on-github/viewing-your-subscriptions`, `2026-10-05T20:08:35Z`, text sha256 `1d835c895aecce4e1bec7e32b4dc8bafd7592731dd49a2710aba4e7f7b49a5e1`. The subscription list is a separate review surface from the inbox, with its own filters, a repository filter, and sort by least recently subscribed. Watch is the repository-level subscription. Custom on Watch chooses event types.

`wai-feed-pattern`, `https://www.w3.org/WAI/ARIA/apg/patterns/feed/`, HTTP 200, `2026-10-05T20:08:37Z`, text sha256 `56b462fd3f90c9f87c50a8eeff1271d2057ebb8ec3c41d57edcf1743696d8df6`. W3C robots do not disallow `/WAI/`. No machine-readable date in the fields I searched. The pattern is a reading structure of `article`s inside `feed`, often infinite. The page, not the screen reader, loads and removes articles as DOM focus moves, and sets `aria-busy` around that update. Each article has `aria-posinset` and `aria-setsize` (or `-1` if the total is unknown), plus `aria-labelledby` and, strongly recommended, `aria-describedby`. Page Down / Page Up move by article. The pattern has no inherited desktop key contract, so the keys must be documented. It also says a static Next that loads a fixed handful of items is the alternative to scroll-loading, and that an article full of buttons makes Tab a poor way to reach a nested feed.

`rss-20-specification`, `https://www.rssboard.org/rss-specification`, HTTP 200, `2026-10-05T20:08:40Z`, text sha256 `ce1d604ab02b49bfaa987fecf1b2ef00c24adb86f0a235672d5426ba8f9e3f96`. RSS Advisory Board, version 2.0.11, 30 March 2009. Robots disallow only `/cache/` and `/dev/`. A document has one `channel` (title, link, description, optional `category`) and any number of `item`s. An item needs a title or a description. `guid` is the identity an aggregator uses to avoid repeating an item. `category` is a label, and it may carry a domain. This is the terminology warning: RSS "channel" is the feed document, not a bus.

Feedly help (Help Scout). `docs.feedly.com/robots.txt` returned 404 "Not Found", so there was no disallow list. I did not fetch `feedly.com` app paths; `feedly.com/robots.txt` disallows `/i/`, `/f/`, `/v3/` except named API allows, and similar.

- `feedly-docs-index`, `https://docs.feedly.com/`, `2026-10-05T20:08:41Z`, text sha256 `cbf2853619ec6bc3daef27cc0c002fd697d0e88f99d405c78b344c3acbb00bcd`. Navigation shell. I used it only to confirm the help center mixes product how-tos with Threat Intelligence API links. Claims below come from the three articles.
- `feedly-organize-folders`, article 677, last updated 17 April 2026, `2026-10-05T20:09:13Z`, text sha256 `5b73cfbc1e3b40142d0c28c2c11889ff2219a810f6dcb64f481d891071703c14`. Keep filtered feeds out of folders of raw sources. Name folders by requirement, audience, or intelligence type. Follow and unfollow a folder for yourself without archiving it for everyone.
- `feedly-follow-sources`, article 768, last updated 31 July 2025, `2026-10-05T20:09:14Z`, text sha256 `da15530ed92ad580b38aea1c4417fef9f216cf09340bb4bd56e4bdf6c36ed327`. Discovery lives under Follow Sources: keyword search, a pasted URL, hashtags, and curated bundles. Bundles can follow many sources at once. Folders should separate `sources -` from `ai -`. Preview a bundle's feeds before following. Audit and remove noisy sources.
- `feedly-feeds-boards`, article 805, last updated 11 August 2025, `2026-10-05T20:09:16Z`, text sha256 `6a1a2c8f2c5f97a0c384f05adccab0be9139131f46d4fc7f0f04354da8d30253`. A team feed updates when content is published and sits in a folder. A board is a manual set of saved articles. Personal feeds and boards are private. Click a folder to read every article in it, or open one feed.

Inoreader. Robots disallow `/reader/`, `/folder/`, `/dashboard/`, `/features/`, `/api/`, and similar. I fetched blog how-tos only. Both pages include a cookie notice and a sign-in form in the extracted text. The how-to body is present above that chrome. I did not treat the sign-in form as the product UI, and I did not capture these pages visually.

- `inoreader-organize-2024`, 28 November 2024, `2026-10-05T20:09:17Z`, text sha256 `6bcd4a6ea0b2ea60b2eb26b5af1d402288653098d86bae23e09aa5f1fa0b7172`. Folders group feeds; one feed may sit in several folders; drag and drop. Tags label articles and live under Saved, separate from folders. Per-folder layout, newest-first or oldest-first, and grouping by feed or date.
- `inoreader-organize-2020`, 2 October 2020, `2026-10-05T20:09:19Z`, text sha256 `13bc76b6c718edd39d4cf476d0c6cb873930914086727277c69e4204e97aa547`. Sidebar shows feeds, folders, and unread counts. Clicking the unread count marks that feed's articles read. A broken feed is marked on the row. Default view is unread, with an All articles switch.

`nngroup-information-scent`, `https://www.nngroup.com/articles/information-scent/`, HTTP 200, full article (not a login wall), published `2020-02-02`, `dateModified` `2024-01-24T04:20:32Z`, retrieved `2026-10-05T20:08:43Z`, text sha256 `cf00122fdfc661ec50f5ea04c9f961c130940a4aead7191051f8436a400442cf`. NN/g robots disallow `/search/` and account paths, not `/articles/`. Scent is the reader's estimate that a link's destination will meet this need. It comes from the label, the nearby summary, the surrounding page, and what the reader already knows. The same label smells different for different tasks. A vague label fails even when the destination is right. Summaries should add a gist the label does not carry. On a small screen the surrounding context is often off-screen, so the label has to stand alone. A strong label wasted on a page that does not confirm the scent in the first screenful is a failed journey.

`carbon-filtering`, `https://www.carbondesignsystem.com/building-blocks/core/patterns/filtering`, HTTP 200, last updated 11 August 2026, retrieved `2026-10-05T20:08:44Z`, text sha256 `ed847e8c5f1ff329a9983f065dca2ab585513b114061e29c2db0cfd3953c2e12`. Robots disallow `/admin/*` only. A category is one topic of filter items. Several categories may apply together. Instant update fits one category or a fast local set. Batch apply fits slow data or a long cross-category decision. A collapsed filter shows how many are applied and can clear without reopening. Each category clears on its own, and the page clears every category at once.

Rejected fetches. DuckDuckGo HTML search returned 403 and an error interstitial for five queries. Those responses are not sources. Bing returned HTTP 200 and no extractable result links in the static HTML, so it contributed no URL. I did not use either page as a design authority. Brave Search returned the Feedly and Inoreader URLs above; the search page itself is not a cited design source.

## Vocabulary

Use these words in the UI and keep them stable.

| Word | Means | Does not mean |
|---|---|---|
| Feed | A declared local catalog identity (`feedId`) inside a scenario family. The nine fixtures are feeds. Further feeds are synthetic, with their own id, title, folder membership, and read markers. | A relay topic, an RSS channel, or a new wire record. |
| Family | The browse facet and the current selector category: quotes, payments, approvals, contracts, credentials, or ops. | A feed id. Several feeds share one family. |
| Watch | The local subscription intent for one family. Revision, selector, requested state, cursors, gap. Several feeds in that family share it. | The persona, the folder, a `feedId`, or the read flag. |
| Occurrence | One journal original. Fixture bodies stay immutable. | A watch, and not a network publication. |
| Receipt | One delivery of an occurrence into a watch, with a technical disposition. | Proof of an effect, and not a read flag. |
| View | How this tab is filtered, paged, folded, and marked read. | Permission, a cursor, a principal, or a Moth grant. |
| Persona | Human, wallet, DApp, or agent. A suggested starting feed. | The principal (`principal:demo` in the demo export). |

Do not use "channel" or "stream" in the directory. RSS uses channel for the document that contains items. On this product a channel-shaped word reads as a bus. The current heading "Browse streams" trains that misreading.

Predicate stays a word on the watch, with a plain gloss at the control: "Which examples this watch delivers." Permitted values remain `all`, `payment-final` on payments, and `approval-report` on approvals. The dashboard currently offers only the payment choice. The approvals choice belongs in the follow preview because the local contract already names it. It is a selector, not a facet of the public directory.

## Recommended pattern

Two tasks, one persistent watch strip.

**Directory** answers "what can I follow, and what would arrive?" **Inbox** answers "what has this tab delivered, and what is its disposition?" GitHub keeps the notification inbox and the subscription list apart, and gives each its own filters. Feedly's useful split is folder-of-feeds versus one feed versus a board of saved articles. Copy the split. Leave Feedly's AI feeds, bundle-follow of thousands of sources, and team-archive semantics behind. Those are server curation features this demo does not have.

Selection, search, folders, and read markers key off `feedId`, so each synthetic feed is its own directory object. The running demo still allows one non-tombstoned protocol watch per category, and that watch's selector is the family. Organizing a feed and holding a protocol watch are different. The directory must not emit two identical `LocalSubscriptionIntent` values and call them two watches.

### Directory facets

Four controls. Carbon's instant update fits: the catalog is local and small in the DOM even when the declared list is hundreds.

1. Scenario family. Single select. All, or one of the six families. This is the browse aid the requirements already describe.
2. Evidence. Single select. Any, Supported profile, Unsigned mock. Supported profile covers the v0.2 quote, payment, and approval fixtures. Unsigned mock covers contracts, credentials, and ops. This is the scent the current rows bury in a second paragraph. It is the same separation Feedly asks for when it says raw sources and filtered feeds should not share a folder.
3. Watch state. Single select. Any, Not followed, Active, Paused, Closed, Blocked. Blocked means the runtime state is expired, revoked, or gapped. Closed means the tombstone.
4. Text. Matches feed title, family name, evidence label, profile id (`rfq.v0.2`, `invoice.v0.2`, `agent.v0.2`), and the one-line gist. It does not match canonical JSON, hashes, or sealed fields.

Persona is not a fifth facet. It may highlight a suggested family ("Agent work often starts in Approvals") and it must not write the family select.

A collapsed filter summary reads "Quotes · Supported profile · 2 of 4 filters" and offers Clear filters. Each select has its own reset to Any or All. That is the Carbon collapsed-filter rule, on a local set, so there is no Apply button.

### Global search and in-feed search

Directory search and inbox search are different fields on different panes.

Directory search returns feeds and, when the query hits a family name, that family's header. It never returns receipts.

Inbox search returns receipts for the watches in the current strip. Suggested queries, documented beside the field: `is:unread`, `disposition:quarantine`, `disposition:review`, `feed:payments`. Combining them is allowed (`feed:payments is:unread`). Unknown tokens match titles only, and the pane says "Unknown filter word ignored" rather than returning a blank list with no explanation.

I did not retrieve a Feedly article that specifies one box switching between all-feeds and the current feed. GitHub's retrieved docs show the opposite structure: inbox queries such as `is:unread` and `reason:review-requested` on the notification list, and a different filter and sort on the subscription list. One combined box would put "Payment final assertion" the feed next to "Payment final assertion" the receipt. NN/g's point is that scent is relative to the need. Two needs, two result lists.

### Discover, preview, follow

1. The directory row shows a feed label that stands alone (NN/g: the small-screen context will be gone), the family name, the evidence badge, and one gist line. No Follow button on the row.
2. Activating the row opens preview inline. Desktop keeps the list. A narrow screen replaces the list and offers Back. Preview repeats the gist, names the profile or "unsigned mock", and shows the watch that Follow will write: family, predicate, start at latest, this tab only. The canonical JSON stays inside a closed disclosure labeled "Original example". Opening it does not follow, does not deliver, and does not mark a receipt read.
3. The primary button is Follow {feed} locally when that family has no watch, and Open family watch when it already has one. The second feed in a family is still selected, foldered, and previewed on its own. Helper text: "Creates a local watch for this family in this tab. Sends nothing. Does not connect a wallet or run an effect. Another feed in this family uses the same watch until a local feed handle exists."
4. Payments preview offers All payment assertions and Final assertions only. Approvals preview offers All approval candidates and Approval reports only. Other feeds omit the predicate control. Changing predicate before the first follow sets the initial intent. Changing it later is the existing Save scope revision, and it stays disabled while work is queued or permission is blocked.
5. After Follow, focus moves to that watch in the strip and the live region says "Following quotes in this tab. No receipt yet." The directory selection stays put.

Simulate this occurrence moves into the preview, enabled only when that feed is a real fixture and an active watch for the family exists. Synthetic rows do not offer Simulate. The nine demo buttons move into a closed disclosure, "Simulation controls", in the inbox pane. They keep their current behavior.

### Folders

A folder is a view over feeds the person has grouped. Inoreader and Feedly both use folders that way: a feed can sit in more than one folder, and opening a folder shows the articles inside it. Here, opening a folder filters the directory and the watch strip to those families. It does not revision an intent, does not change `sourceEquals`, and does not unsubscribe.

Removing a feed from a folder leaves the watch. Unfollow remains the tombstone button on the watch. Feedly's "Unfollow folder" is the wrong verb on this page, because unfollow already means a tombstone.

Default folders are not required. The six families already are the primary nav. A folder named "Month-end" that contains payments and contracts is a personal grouping, stored as a view.

### Read, unread, and dispositions

Inoreader's retrieved how-to marks a whole feed read by clicking its unread count, and defaults the article list to unread. GitHub separates Read, Unread, Save, and Done, and keeps Done for three months while Saved lasts until it is unsaved. Use the GitHub split, with this product's words.

- Unread means this tab has not opened the receipt. The count is a view. Clicking the count must not mark anything, because a count that changes cursors is the Inoreader gesture this page should not copy.
- Opening a receipt sets that receipt's read flag only. It does not move the delivery cursor, the processing cursor, or the journal high-water.
- "Mark next item reviewed" stays the explicit processing action. Its result is still "reviewed locally; no effect executed" or the existing quarantine disposition. Reviewed is not a synonym for read. A receipt can be read and still awaiting review, or unread and already quarantined.
- The inbox can filter to unread without hiding quarantined items unless the query says so.
- Demo retention is the in-memory journal, capped at 64 originals by the current script, not GitHub's three-month Done policy. Do not copy that retention number into this product.

Technical dispositions stay exactly the ones the script already assigns: `awaiting review: offline reference only`, `awaiting local processing`, `reviewed locally; no effect executed`, `quarantined: …`, `duplicate suppressed`. The directory never displays these. The inbox does, as the second line of the receipt, after the read state.

### Hundreds of feeds

The council brief asks for hundreds of synthetic feeds that a person can search and organize, and for that organization to survive a visit. A working-tree paragraph in `docs/product-requirements/pubsub-subscription-experience.md` (I did not write it) says the same thing more sharply: distinct feed identities, not hundreds of aliases for one category, and persisted synthetic read markers that cannot restore authority. This proposal follows that directory goal and does not pretend the closed intent schema already stores a feed id.

Declare each feed in memory: `feedId`, family, title, evidence class, and `exampleFixtureTitle` pointing at one of the nine records. The nine fixtures are real feeds and sort first, in file order. Synthetic feeds sort after them. They are independently selectable: selection, folders, pins, and read markers use `feedId`. A synthetic preview says which fixture it reuses and that no new profile or wire was created. No new hashes and no acceptance claim.

Follow writes one protocol watch per family, because that is the demo rule and the selector has no feed field. The directory still remembers every feed the person chose. The watch strip names the family and lists the feed titles pinned to it ("Payments · active · Payment pending, Desk example 12"). Receipts arrive through the family watch. Per-feed unread counts are views over those receipts plus a stored marker for feeds that have never delivered. They are labeled historical preferences. They do not recreate the journal after reload.

The DOM holds one window of 25 feeds. The status line is "Showing 1–25 of 80 feeds in Quotes." Next and Previous move the window. A query or facet change returns to page 1. At 25 rows, do not virtualize. `content-visibility` is optional and not required for acceptance. The optimize guidance is to virtualize very long lists and to measure first. This list is long in data and short in the DOM. Building 400 articles would be the regression.

The inbox uses the same kind of window, aligned to receipts: "Latest 40 of K" and Older / Newer. Older does not change either cursor. The current `slice(-40)` with no Older control is the bug to close. An infinite `role="feed"` is the rejected default for both panes. The WAI pattern allows removing off-screen articles as focus moves, and it is the right contract if a later inbox genuinely scroll-loads. It is a poor directory: directory rows are decisions, the total is known, and a static Next is the alternative the pattern itself describes. If an inbox feed role is adopted later, it needs `aria-busy` around DOM updates, `aria-posinset`, `aria-setsize` set to the full receipt count, Page Up / Page Down, documented keys, and loading that does not advance cursors.

### Rejected alternative

A Feedly-shaped three-column reader: folder tree, infinite article stream, and a follow button on every row, with the row marked read when opened.

That layout is familiar and wrong here. Folders would be mistaken for topics. Every synthetic row would look like its own subscription, but the demo cannot hold two watches for one family. Mark-on-open would be confused with the processing cursor. Infinite scroll would fight bounded delivery and the explicit gap. Bundle-follow ("follow dozens or thousands") would skip the preview that tells the person nothing is sent and nothing is executed. I keep Feedly's folder-versus-feed distinction and its demand that evidence classes not be mixed. I do not keep its reader shell.

## Wireframes

Desktop, about 1100px, the current `main` max-width. Two panes. The watch strip is one horizontal row, not a third column. A third column can wait until the viewport is at least 1280px wide; until then a third column crushes the gist.

```
Your local inbox.
Explore what you can follow locally, then review what this tab delivers.

[ Directory | Inbox ]          Persona: Human (suggestion only)

Watches: Quotes · active      Payments · paused      + Follow from the directory

Directory
[ Search feeds          ]  Family [ Quotes v ]  Evidence [ Supported profile v ]  Watch [ Any v ]  Clear
Showing 1–25 of 80 feeds in Quotes.  Page 1 of 4.   [ Previous ] [ Next ]

> Shares / USD quote                         Quotes · Supported profile
  Historical offline quote. 100 Share at 123.45 USD.     [ Preview ]
  Payment pending                            Payments · Supported profile
  ...

Preview
  Shares / USD quote
  Quotes · Supported profile · rfq.v0.2
  Historical offline quote… Off-chain coordination only.
  Follow binds a local quotes watch. Predicate: all. Start: latest. This tab only.
  [ Follow quotes locally ]
  [ Original example ]   (closed; immutable fixture JSON)
```

The `>` marks the selected feed. Preview is beside the list, so the gist and the follow consequence stay on screen together. NN/g's failed journey is a good label that lands on a page with no confirming scent. The preview is that confirmation.

Narrow, 390px. I did not capture this width. The structure follows the desktop tiles plus the existing single-column CSS.

```
Your local inbox.
[ Directory | Inbox ]

Watches (1)  Quotes · active          [ strip scrolls horizontally ]

[ Filter feeds · Quotes, supported profile ]
[ Search feeds ]

Shares / USD quote
Quotes · Supported profile
Historical offline quote…
[ Preview ]                           44px target

--- after Preview, the list is replaced ---

[ Back to feeds ]
Shares / USD quote
… gist and the follow sentence …
[ Follow quotes locally ]             in the lower half, above any status bar
[ Original example ]
```

Wallet and simulation controls are closed disclosures on both widths. "Optional Moth wallet" keeps today's acknowledgement and the four buttons inside it. Closed by default so the directory is the first task. Nothing in this proposal calls `connect` or polls status.

The sticky `#announcement` bar remains the live region. The preview's follow button needs `padding-bottom` at least the bar's height so a one-line status does not cover it. The bar is not a toolbar.

Annotated fragment for the directory window. This is a specification snippet, not a patch.

```html
<section aria-labelledby="directory-heading">
  <h2 id="directory-heading">Directory</h2>
  <!-- Family, evidence, and watch state are one category each. Instant local filter. -->
  <form role="search">
    <label>Search feeds <input id="feed-search" type="search" /></label>
    <label>Family <select id="family"><option value="quotes">Quotes</option></select></label>
    <label>Evidence <select id="evidence"><option value="supported">Supported profile</option></select></label>
    <label>Watch <select id="watch-state"><option value="any">Any</option></select></label>
    <button type="button">Clear filters</button>
  </form>
  <p id="window-status">Showing 1–25 of 80 feeds in Quotes.</p>
  <div role="listbox" aria-labelledby="directory-heading" aria-activedescendant="sit-quotes-0" tabindex="0">
    <!-- Roving tabindex: the listbox is one tab stop. Rows are options, not three buttons. -->
    <div role="option" id="sit-quotes-0" aria-selected="true">
      <p>Shares / USD quote</p>
      <p>Quotes · Supported profile</p>
      <p>Historical offline quote. 100 Share at 123.45 USD per Share.</p>
    </div>
  </div>
  <nav aria-label="Feed pages">
    <button type="button">Previous page</button>
    <button type="button">Next page</button>
  </nav>
</section>
<aside aria-labelledby="preview-heading">
  <h2 id="preview-heading">Shares / USD quote</h2>
  <p>Follow binds a local quotes watch in this tab. Sends nothing. Does not connect a wallet or run an effect.</p>
  <button type="button">Follow quotes locally</button>
  <details>
    <summary>Original example</summary>
    <!-- Immutable fixture JSON. Opening this disclosure is not follow, delivery, or review. -->
    <pre></pre>
  </details>
</aside>
```

On a narrow screen the `aside` replaces the listbox, and Back returns focus to the same option.

## State contract

```text
ViewState  // presentation only. Persist in sessionStorage. Cleared by Reset.
  pane: "directory" | "inbox"
  persona: "human" | "wallet" | "dapp" | "agent"   // suggestion. Never writes family by itself.
  directory:
    query: string
    family: "all" | "quotes" | "payments" | "approvals" | "contracts" | "credentials" | "ops"
    evidence: "any" | "supported" | "mock"
    watch: "any" | "none" | "active" | "paused" | "closed" | "blocked"
    page: number          // 1-based, window 25, reset to 1 when query or facets change
    selectedFeedId: string | null
  folders: { id, name, feedIds: string[] }[]      // membership is not an intent revision
  pinnedFeedIds: string[]                          // directory organization, not a second watch
  inbox:
    query: string         // is:unread, disposition:…, feed:… plus plain text
    feedId: string | "all"
    windowEnd: number     // receipt index. Older/Newer move this. Cursors do not.
    limit: 40
  read: { feedId, subscriptionId, cursor }[]       // view flag. Not a disposition.
  // After reload the journal is gone. Leftover read keys are labeled historical.
  // They do not restore receipts, cursors, permission, or a wallet grant.

Runtime  // unchanged meaning. Tab memory in the demo. Not ViewState.
  permission: granted | expired | revoked
  journal: originals[]    // high-water is length. Cap 64. Fixture records immutable.
  watches: LocalSubscriptionIntent + cursors + gap + queue + inFlight
  receipts: { subscriptionId, revision, cursor, disposition, replay }[]

Forbidden in any browser store:
  permission, journal, cursors, intent revisions, occurrence bodies,
  Moth grant, wallet status, principal.
```

Reload, today: the script keeps none of this. A fresh load shows the catalog, high-water 0, no watches, and the empty inbox. Recommended split: sessionStorage keeps ViewState (query, page, folders, pins, read keys). It does not keep the journal, watches, cursors, or permission. Copy when a reload finds no watches: "This tab has no watches. Reload clears local watches and receipts. Your folders and feed selection are still here, and they do not restore permission." First use of a watch stays "No receipts yet. Follow a feed, or simulate intake, to deliver an example into this tab."

Reset clears runtime and ViewState, and does not touch a Moth origin grant. The existing announcement can stay.

Search does not call intake, does not revision a watch, and does not rebuild the watch strip or the inbox DOM. That is the fix for the lost scope edit.

Folders do not create, pause, or tombstone watches.

Read does not enqueue, dispatch, or process. Processing does not clear or set read, so a reviewed receipt can remain unread until opened. That keeps the checkpoint honest.

Disposition text stays machine-stable for the export and tests. The visible gloss can sit beside it: "Awaiting review · offline reference only".

## Acceptance

Scale

- A declared list of 400 feeds (the nine fixtures plus synthetic feeds) paints at most 25 options.
- Each feed keeps its own `feedId` across search, folders, pins, and reload of ViewState.
- Real fixtures keep their titles and sort ahead of synthetic feeds.
- A synthetic row's preview names the fixture it reuses. Follow never writes a second intent for the same family.
- No synthetic row adds a profile, a contract hash, or a wire blob.
- Directory search across 400 rows does not replace the watch strip nodes. An unsaved predicate select survives a directory keystroke.
- Inbox Older reveals receipts before the latest 40 without changing `deliveredCursor` or `processedCursor`.

Keyboard

- The feed list is one tab stop. Down and Up move the active option and the preview. Home and End move inside the current window. Tab leaves the list.
- Enter or Space on the option keeps the preview. Follow is a separate button, reached by Tab, not a second control inside the option.
- Escape from preview returns focus to the same option.
- Inbox receipts use the same roving keys. They do not use Page Up / Page Down unless the pane is later rebuilt as a WAI feed, in which case those keys must be documented on the pane.
- `/` moves focus to the search field of the open pane when focus is not already in a field or the JSON disclosure.
- `f` activates Follow or Open watch when the preview is showing.
- Shortcuts are listed in a disclosure, "Keyboard", including these keys. The WAI note is that a feed has no inherited key contract; the same honesty applies to this listbox.
- Focus rings stay visible. The existing `:focus-visible` outline is the ring to keep.
- A query with zero feeds writes "No feeds match this search in Quotes." into the list and the live region. Focus stays in the search field.

Performance

- Do not virtualize a 25-row window. Do not mount 400 rows to measure it.
- Filtering is synchronous on the in-memory declaration. No batch Apply control.
- Fixture load reserves the directory status line ("Loading the local catalog") so the first paint does not jump the wallet block into a new position after the list appears. The catalog fetch is the current layout shift.
- The follow control remains fully visible above the live region at 390×844 with a one-line announcement.
- Touch targets for Preview, Follow, Back, Next, and Previous are at least 44×44 CSS pixels. Hover is not required to reveal Follow.
- Text at 200% with a 390px viewport does not scroll horizontally. That assertion already exists; the new row has to keep it.
- No new wallet calls. Discover, connect, status, and disconnect remain the current explicit buttons.

I have not measured INP or frame time on this page. The acceptance bar is the DOM cap and the focus rule, which fail today by construction (`render()` rebuilds the lists, and every fixture becomes a row).

## Product prose

Directory row, supported profile. "Shares / USD quote. Quotes · Supported profile. A historical offline quote: 100 Share at 123.45 USD per Share. You can inspect it. Following watches the quotes family in this tab."

Directory row, unsigned mock. "Contract renewal reminder. Contracts · Unsigned mock. A demonstration reminder. No profile is verified. Following still only creates a local watch."

Synthetic row. "Desk example 12. Payments · Supported profile. Synthetic view. The example is the existing Payment pending fixture. Following watches the payments family, not this label."

Preview, follow. "Follow payments locally. This watch starts at the latest local position. It sends nothing. It does not prove a payment or connect a wallet."

Preview, predicate. "Final assertions only. This watch delivers payment examples whose status is Final. Pending and reversed stay in the directory and do not enter this watch. Final on a receipt is not consensus finality."

Already followed. "Quotes already has a watch. Open that watch. A second follow is not created."

Empty directory search. "No feeds match “USD” in Contracts. Clear the search, or switch family to All."

Empty inbox, watch exists. "No receipts in Quotes yet. This watch is active. Simulate intake to deliver an example into this tab. Reload clears it."

Empty inbox after reload. "This tab has no watches. Reload clears watches and receipts. Choose a feed in the directory to follow locally again."

Unread gloss. "3 unread in Quotes. Unread means you have not opened them. It does not mean they are awaiting review."

Receipt. "Payment final assertion. Unread. Awaiting review: offline reference only. Opening this marks it read. Mark next item reviewed records a local disposition and does not run an effect."

Quarantine. "Expired quote. Unread. Quarantined: quote-validity. The quote stays visible. The watch does not treat it as accepted."

Blocked watch. "Payments · revoked. Local permission blocks intake and review. Receipts already in the inbox stay. Reset restores demo permission. A Moth grant is separate and is not restored here."

Folder. "Month-end contains Payments and Contracts. Removing Quotes from this folder leaves the quotes watch as it is."

Persona. "Persona: Agent. A suggestion to start in Approvals. The principal and the watches stay as they are."

## Consensus recommendations

1. Rename the directory to feeds. Remove "stream". Do not introduce "channel". Family is the facet and the current watch scope. `feedId` is the catalog identity.
2. Give every catalog row a stable local `feedId`. Search, folders, pins, and read markers use that id, so synthetic feeds are independently selectable. The protocol watch stays one per family until the intent schema has a non-routable local feed handle. Do not export two identical intents.
3. Put evidence class on every row as a badge with the words "Supported profile" or "Unsigned mock", and make it a facet.
4. Split Directory and Inbox. Give each its own search. Directory search covers labels, gists, families, evidence, and profile ids. Inbox search covers receipts and the documented `is:`, `disposition:`, and `feed:` words.
5. Window the directory at 25 and the inbox at 40, with visible ranges and Previous/Next or Older/Newer. Do not virtualize those windows. Do not use `role="feed"` on the directory.
6. Move Follow into preview, with the bind sentence (family, predicate, latest, this tab, sends nothing). Payments and approvals choose their existing predicates there.
7. Keep read as a view flag. Keep today's disposition strings as the processing record. Opening a receipt sets read only. The unread count does not mark read.
8. Treat folders as view membership over `feedId`s. A feed may sit in more than one folder. Adding or removing it does not revision the intent and does not tombstone the watch. Persist folders, pins, and read keys in sessionStorage. Reset clears them. They never restore a watch, a cursor, permission, or a Moth grant.
9. Stop persona changes from writing the family select.
10. Stop directory search from rebuilding the watch strip or the inbox.
11. Collapse Moth and the nine simulation buttons behind disclosures so the directory is the first task. Leave the Moth controls and their click rules as they are.
12. Generate any hundreds-scale catalog as declared synthetic feeds that point at the nine immutable fixtures. Sort real fixtures first. The preview names the reused fixture and the shared family watch.
13. After reload, use the "this tab has no watches" sentence so a cleared journal is distinct from a watch that has not delivered.

## Dissent and unresolved decisions

SessionStorage for ViewState is the recommendation, because the brief asks for organization that survives a visit and the requirements note allows labeled historical read markers. The opposing position is that any browser persistence makes the demo look durable. I would not store runtime state in either camp. Leftover read keys after reload stay labeled historical and reattach only if the same `feedId` and cursor come back from a host. This demo host does not bring them back.

A directory `feedId` is a local selection key. I am against putting that id in the sealed envelope, in relay metadata, or in two identical intent exports. A schema field for a non-routable local feed handle would make two feeds in one family into two watches. That field does not exist. Until it does, the watch strip must say the family is the delivery scope. A later allowlist of already-authenticated sources can narrow `sourceEquals` on that family watch. The demo has no such list. Until it does, the preview should say "all locally authorized sources" and offer no source picker. I would vote a source picker down.

I am against copying GitHub's three-month Done retention or Inoreader's click-the-count-to-mark-read. Both are real, documented behaviors of those products. Both collide with explicit cursors.

`approval-report` in the approvals preview is in the local contract and absent from the dashboard. If another reviewer owns predicate interaction, this proposal only needs the control placed in preview rather than in the directory facet row. I do not need a second predicate system.

A WAI `feed` for the inbox remains a legal alternative if someone measures a real need to scroll-load more than a window of 40 and implements `aria-busy`, positions, and documented Page Up / Page Down without moving cursors. I would not start there. The totals are known, and the product already thinks in bounded pulls.

Mobile layout is specified from the desktop tiles, the CSS breakpoint, and the existing 390px overflow test. I did not take a mobile PixelRAG tile, and I did not click Follow on the live page. Post-click behavior is from `subscriptions.js` and `subscriptions.cjs`.
