# Adversarial consensus review

Reviewer: Grok 4.7, independent principal-engineer pass. Completed 2026-10-05 from captures already stored by the interrupted runs. No new web search, no runtime edits, no other agents.

This review checks version identity and the Moth grant/activity claims in `docs/product-requirements/pubsub-subscription-experience.md` and `wiki-llm/pubsub/decisions-draft.md`. Snapshots below are retrieval facts. They do not settle a version for every later commit.

## Research approach

Primary sources are Scrapling captures under `wiki-llm/pubsub/sources/grok-adversarial-consensus/`. Each `*.json` sidecar records `retrieved_utc`, URL, HTTP status, and `raw_sha256` / `text_sha256`. Bodies are the sibling `.txt` files. One PixelRAG tile was read: `mcp-versioning-visual-tiles/.../tile_0000.jpg`, with `tiles.json` marking that page complete (`page_height` 1935, two tiles). Tile 0001 was not read. The text extract of the same page matches the rendered tile.

Compared, for each stack: the public docs banner, the GitHub tag or release the banner might be confused with, and `main` at retrieval. Moth was read at the blob commit the captures name, then checked against `main`.

## Intermediate findings

### MCP: date label, tag, and main are three snapshots

The versioning page says the current protocol version is **2026-07-28**, and that this date is the last backwards-incompatible change. The same page says the version is not incremented for backwards-compatible edits. PixelRAG tile 0000 shows that sentence and the callout. Negotiation text on that page: each request carries `io.modelcontextprotocol/protocolVersion` in `_meta`; Streamable HTTP also sends `MCP-Protocol-Version`; `server/discover` is a mandatory RPC and calling it is optional; handshake revisions `2025-11-25` and earlier are a separate compatibility case.

GitHub tag `2026-07-28` points at commit `5f5440bb26a62e2cf3440b92da5a667efa03b267` (committer 2026-07-28T16:44:35Z, merge of PR #3158, subscriptions/listen result naming and response envelope). Tag `2026-07-28-RC` is a different commit, `9d700ed62dcf86cb77475c9b81930611a9182f46`. Schema `schema/2026-07-28/schema.ts` at the release commit contains the strings `server/discover` (10) and `subscriptions/listen` (21), and also `resources/subscribe` (1). Deprecation context for that last string was not read.

`main` at compare time is `75db1e987cbbba6d170315dc99d0dfc440754aef` (tip commit 2026-10-03, dependency bump #3411). Compare `5f5440bb…75db1e98`, retrieved 2026-10-05T18:19:05Z: `ahead_by` 267, `behind_by` 0, `status` ahead. Those 267 commits were not diffed for protocol compatibility. The versioning policy allows the label 2026-07-28 to remain while bytes move. That policy is not a per-commit proof.

The product requirement cites `https://modelcontextprotocol.io/specification/2026-07-28/changelog`. That changelog body is not in this capture set. What was retrieved for “current version” is `https://modelcontextprotocol.io/specification/versioning`, which resolved to `https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning`. The authorization page chrome also says “Version 2026-07-28 (latest)”.

A raw URL under `modelcontextprotocol/specification` returned the same body hash as the tag schema (`raw_sha256` `742750af0bb8c716e7030c4977c992b55d1adc4407e9e66997db5846baedc2cd`). Tags and commits in this review were listed from `modelcontextprotocol/modelcontextprotocol`.

### A2A: `/latest/` banner says 1.0.0; newest GitHub release is v1.0.1; main is neither

`https://a2a-protocol.org/latest/specification/`, retrieved 2026-10-05T18:22:02Z, states:

- Latest Released Version: **1.0.0**
- Previous Versions: 0.3.0, 0.2.6, 0.1.0

Section 3.6 of that same page says the on-wire version is Major.Minor (example `1.0`). Patch numbers should not be sent and should not affect protocol compatibility.

GitHub releases `per_page=5`, retrieved 2026-10-05T18:19:05Z: newest release is **v1.0.1**, `prerelease: false`, published 2026-05-28T11:34:36Z, `target_commitish` `3303592588e388e62e0f69f701af531d2f4e3991`. The release API body dates the notes 2026-05-26 and lists three spec bugfixes: `application/a2a+json` (#1753), transcoding errors (#1627), and TaskStatus values (#1801). The commit object at `v1.0.1` is that same SHA, but its message dates the notes 2026-04-23 and lists only #1753 and #1627. The tag commit message and the published release body disagree with each other.

`main`, retrieved 2026-10-05T18:21:30Z, is `679ab3afc6f95ef47bb969d511053d0f63bca2a2` (2026-10-05T16:25:13Z, docs link-checker fix #2298). An ahead-count from v1.0.1 to that main SHA was not captured.

### Connector: release commit, main, and the version string do not name one tree

Releases `per_page=5`, retrieved 2026-10-05T18:18:14Z:

| Tag | Prerelease | Published | Role in this snapshot |
|---|---|---|---|
| `v4.1.0-beta.1` | true | 2026-07-02T13:19:16Z | Newest GitHub release. Packaging fix for declaration emit. |
| `v4.1.0-beta.0` | true | 2026-07-01T15:50:55Z | Scope move to `@midnightntwrk`, optional `signData` `scheme`. |
| `v4.0.1` | false | 2026-02-17T11:48:59Z | Newest non-prerelease. `payFees` options. |

Annotated tag `v4.1.0-beta.1` is tag object `8ed5f51e6e6d9135879d0460412bef6cb27fd5a6`, tagger MidnightCI 2026-07-02T13:19:13Z, target commit `da90f631d45338d640365fb3d868e095130b4d6d` (“Version Packages (beta) (#52)”).

`main`, retrieved 2026-10-05T18:18:13Z, is `612db2b62dbd78c079da62e57e7b8585a204b858` (2026-09-29T15:44:34Z, merge PR #95, DCO docs). Compare `da90f631…612db2b`, retrieved 2026-10-05T18:21:28Z: `ahead_by` 44, `behind_by` 0. Subjects on that range include “Improve consumer-side compatibility and add InsufficientFunds error” (PR #61). `package.json` fetched from `main` at 2026-10-05T18:18:16Z still says `"name": "@midnightntwrk/dapp-connector-api"` and `"version": "4.1.0-beta.1"`. The version string matches the prerelease tag name and does not identify `da90f631`. `SPECIFICATION.md` in the capture was fetched at `612db2b`, not at the tag. The InsufficientFunds sentence is a commit subject; the spec paragraph was not line-checked.

### Moth: origin grant, no dApp revoke, activity on every successful allowed call

`moth-wallet` `main`, retrieved 2026-10-05T18:18:12Z, is `d48206a1957af09bf17bf5e941c2b5bccb12db63` (2026-10-01T18:26:33Z, merge PR #162, `auto-lock-dapp-activity`). The permissions, constants, and handler blobs were fetched at that same SHA. Equality with `main` holds for this retrieval only.

`permissions.ts`: `OriginGrant` is `{ networkId, grantedAt }` under `permissions.origins`. `isAllowed` is `origin in grants`. It does not compare `networkId` or a method list. `grant` overwrites the origin entry. `revoke` deletes the origin key.

`connector-handlers.ts`: the page origin comes from the extension sender. `ensureConnected` prompts when the origin is not allowed or the wallet is locked, then `grant(origin, networkId)`. Later methods call `requireConnected`, which uses `isAllowed` plus an unlocked session. `permissionsRevoke` is an extension message (`onMessage('permissionsRevoke')`), not a connector method. `IMPLEMENTED_METHODS` has no revoke. `EXTENSION_METHODS` is `deriveAppSecret`, commented as outside `@midnight-ntwrk/dapp-connector-api` v4.0.1. `API_VERSION` is the string `'4.0.1'`. The comment names the legacy scope `@midnight-ntwrk`, while the handler imports `@midnight-ntwrk/dapp-connector-api`. Upstream’s beta.0 notes moved publishing to `@midnightntwrk` and kept the old scope as an alias. `NOT_IMPLEMENTED_METHODS` is empty at this commit.

`dispatch` calls `recordActivity(Date.now())` after a successful `dispatchMethod` when `isAllowed(origin)` is true. The comment says a connected dApp counts as the user at work so auto-lock does not fire between requests. Thrown connector errors skip `recordActivity` because the call sits before `return`, not in `finally`. This is every successful allowed method, including status, and also transfers and signing if those succeed.

`connect()` itself continues after `getSettings()` at line 270. A wallet-settings network mismatch inside `connect` was not fully read. The later-method path does not re-check stored `networkId`.

### Other captured standards, only as version pins

CloudEvents GitHub releases, retrieved 2026-10-05T18:19:06Z: newest listed tag `ce@v1.0.2`, published 2022-02-06T00:48:06Z, not a prerelease. `cloudevents/spec.md` commits `per_page=3`: `6862e1dc673ca57ababe2dd076ee3a925e2c129f` (2026-03-12, “fix typo”), then `f88346fce75d63f7ec880940e6ad4b69373b6cde` (2025-08-20). The 2022 release tag and the 2026 spec.md commit are different objects.

WHATWG Notifications, retrieved 2026-10-05T18:19:09Z: “Living Standard — Last Updated 5 October 2026.” The page links a snapshot commit; that hash was not extracted. No frozen version number belongs on this citation.

## Claims the root must correct

Correct these sentences. Leave the surrounding decisions (no new mandatory broker, private local watch, optional adapters, Pages acknowledgement, demo-only dashboard) as they stand.

1. Product requirement: “Current MCP 2026-07-28 uses `server/discover` and `subscriptions/listen`,” linked to the changelog URL. Correct to: at tag `2026-07-28` = `5f5440bb26a62e2cf3440b92da5a667efa03b267`, the schema text contains both names. The docs page calls 2026-07-28 current and allows later compatible edits under that same label. On 2026-10-05, `main` (`75db1e98`) was 267 commits ahead of the tag. The changelog URL was not the retrieved body. `resources/subscribe` still occurs in the tag schema; do not describe the legacy method as absent from that file.

2. Any inventory line that treats A2A “latest” as v1.0.1, or the v1.0.1 release as `main`. Correct to: the `/latest/specification/` banner retrieved 2026-10-05 says Latest Released Version **1.0.0**. The newest GitHub release is **v1.0.1** at `3303592588e388e62e0f69f701af531d2f4e3991`. `main` is `679ab3afc6f95ef47bb969d511053d0f63bca2a2`. On-wire identity in that spec text is major.minor `1.0`. The v1.0.1 release body and the v1.0.1 commit message do not list the same fixes.

3. Product requirement: Moth “API 4.0.1” plus “The beta connector API is not silently accepted.” Keep both gates. Correct the referent of “beta”: `v4.1.0-beta.1` the release is commit `da90f631d45338d640365fb3d868e095130b4d6d`. `main` `612db2b62dbd78c079da62e57e7b8585a204b858` still carries package version `4.1.0-beta.1` and is 44 commits ahead, including an InsufficientFunds change. `4.0.1` is Moth’s `API_VERSION` and the newest non-prerelease tag. It is not the version string on connector `main`.

4. Decisions draft: “the exact Moth connector contract” and “no narrow grant or DApp revoke method.” Keep the no-narrow-grant and no-dApp-revoke conclusion for commit `d48206a1`. Correct “exact” so it names that commit, which matched `main` only at 2026-10-05T18:18:12Z. Add: `isAllowed` does not enforce `networkId` or method; `revoke` exists for the extension message `permissionsRevoke` only. `deriveAppSecret` is outside the v4.0.1 surface the constant names.

5. Product requirement: “Status checks are explicit, since Moth connector activity refreshes auto-lock.” The mechanism is real at `d48206a1` (PR #162). Correct the scope: `recordActivity` runs after every successful `dispatch` from an already allowed origin, not only after status methods, and not after thrown errors. Explicit status polling is still required for freshness. Activity refresh is a side effect of successful connector calls, which is why a watch adapter should not poll.

6. If the standards inventory equates CloudEvents `ce@v1.0.2` with the current spec text, correct it: release published 2022-02-06; captured `spec.md` head is `6862e1dc` on 2026-03-12. Cite WHATWG Notifications as a living standard last updated 5 October 2026, with no version number from this capture.

## Recommendations

- Pin MCP claims used for implementation to schema commit `5f5440bb` until someone diffs the 267 later commits and accepts them. Keep `server/discover` and `subscriptions/listen` as names present in that schema. Keep legacy resource subscription behind a separate compatibility adapter only after the tag schema’s `resources/subscribe` entry is classified; the string is still there.
- Pin A2A adapter work to a named commit. Say “docs banner 1.0.0, GitHub release v1.0.1 at `33035925`, main `679ab3af`” whenever a version is required. Send major.minor `1.0` on the wire if following section 3.6 of the captured `/latest/` page. Re-read v1.0.0 versus v1.0.1 before relying on TaskStatus or `application/a2a+json`.
- Keep the Moth demo adapter on API string `4.0.1`, connection and status only, explicit gesture, no signing, no polling. Refuse both connector artifacts that say `4.1.0-beta.1`: tag `da90f631` and main `612db2b`.
- Treat a Moth grant as origin-wide for every implemented method, including transfer, balance, prove, and `deriveAppSecret`. Local disconnect must not be described as revoke. Production origin stays dedicated. Demo on the shared Pages origin stays an explicit acknowledgement. A live extension session stays a manual gate. Add a test that an allowed origin is not re-checked against `networkId` on a later method, and finish reading `connect()` before claiming network mismatch behavior.
- Leave sealed-size, recognition cost, RLN class credit, Store repair, and mobile whole-shard feasibility open. Do not cite JSON example sizes as wire fit.

## Source pins

Times are sidecar `retrieved_utc`. Hashes are sidecar `raw_sha256` of the retrieved body. All HTTP statuses were 200. Tool: Scrapling, except the one PixelRAG tile noted.

| Pin | Retrieved (UTC) | Identity | raw_sha256 |
|---|---|---|---|
| MCP versioning, final URL `…/docs/2026-07-28/learn/versioning` | 2026-10-05T18:19:08Z and again 18:22:02Z | Docs current version 2026-07-28. Same hash both fetches. | `2d707c5db5f8d27a530a87e1c6ccd48f9a78f796c8aebdf7bbfd6b380c7ca233` |
| MCP tags | 2026-10-05T18:18:12Z | Newest tag name `2026-07-28` → `5f5440bb26a62e2cf3440b92da5a667efa03b267` | `70f55ded01f17bdfd70d89c34224d78a1467bf6aea1febeb9ab2ba48a839399c` |
| MCP commit `2026-07-28` | 2026-10-05T18:18:15Z | `5f5440bb…`, 2026-07-28T16:44:35Z | `6acfcc1a14dbd3ec13d9d6171ea4b9103aa83ea60f57c4be40484030a81bfb85` |
| MCP schema at that commit | 2026-10-05T18:20:51Z | `schema/2026-07-28/schema.ts` | `742750af0bb8c716e7030c4977c992b55d1adc4407e9e66997db5846baedc2cd` |
| MCP compare tag…main | 2026-10-05T18:19:05Z | ahead 267, tip `75db1e987cbbba6d170315dc99d0dfc440754aef` | `773cfed4b342ccde44347564b4fb9a0d0b9420fdfe40d2e7663f6cdaaf4f70e6` |
| A2A `/latest/specification/` | 2026-10-05T18:22:02Z | Banner: Latest Released Version 1.0.0 | `0e6a4625fb6a4958f86ea15248887cb6ea04f4267b0d1a1f4ba7eea877ce2ee4` |
| A2A releases | 2026-10-05T18:19:05Z | Newest: v1.0.1, published 2026-05-28T11:34:36Z | `3cc234474c8c38cdc224a4462b9ca39aafb42576d39cd2e3dce3ebfd6bd64b52` |
| A2A commit `v1.0.1` | 2026-10-05T18:20:55Z | `3303592588e388e62e0f69f701af531d2f4e3991` | `564d713ec06ddbf67795e28c2a31759b9e85596473e5bc6a9d9658cd5415d3ce` |
| A2A `main` | 2026-10-05T18:21:30Z | `679ab3afc6f95ef47bb969d511053d0f63bca2a2` | `06868ef61eeec3e3edf27ec7765007bd6640225795aa3c1e58755cc80af52b9e` |
| Connector releases | 2026-10-05T18:18:14Z | Newest v4.1.0-beta.1; newest stable v4.0.1 | `5334f9800420225e1b9edc986d9a7cfacaedfce137ec2fe91606d1122eb3b2ef` |
| Connector tag ref + annotated tag | 2026-10-05T18:19:07Z and 18:20:50Z | Tag object `8ed5f51e…` → commit `da90f631…` | ref `cb641209bae2512b15f8849b99316b0fde92ad94d211e9c806d1853d1e707fca`; tag `9a3a8714756090810cfb17356900cc26dcaef6349c70587134d9b5f7eea34cbd` |
| Connector `main` and `package.json` | 2026-10-05T18:18:13Z and 18:18:16Z | `612db2b6…`; version string still `4.1.0-beta.1` | commit `e766d61a28fd107f244d7b04af218d73f8d418cc88da58c4b16f07f55f14b9dd`; package `39eb6f71cd6d0a5164abc8369002781628c3f8a921f3f578b9ced70cc0210c0f` |
| Connector compare release…main | 2026-10-05T18:21:28Z | ahead 44 | `742c668b863d06ba3adf89280a806358468f2f92aa4f55095b24303582d1dc98` |
| Moth `main` | 2026-10-05T18:18:12Z | `d48206a1957af09bf17bf5e941c2b5bccb12db63` | `9042a25ee9bee8665ee7fa3883b191099de100515ee257c12faa373ac4e54e82` |
| Moth `permissions.ts` | 2026-10-05T18:19:05Z | Same commit, raw blob | `4c4ef867c50067dc0dc5de945d239ae454c2b90d3ea30a879d95b4359b19bb35` |
| Moth `constants.ts` | 2026-10-05T18:19:06Z | `API_VERSION = '4.0.1'` | `248bb5c08c0a2cd66cd39c1ccd27086fa062312a6f404f7d0574974194fa2c32` |
| Moth `connector-handlers.ts` | 2026-10-05T18:23:30Z | `recordActivity` after successful dispatch | `7726712a87ab1d7f79a82b41f25b661dc030fb8f675d7c2f28ab9db5abb1b545` |
| CloudEvents releases / spec.md commits | 2026-10-05T18:19:06Z / 18:19:08Z | `ce@v1.0.2` (2022-02-06); spec.md `6862e1dc` (2026-03-12) | `d536ec8c9b0b74fdb990dbd9005533e10305ee3a54623ac22a4634f077beab4c` / `380466dcfbaa70095e476c04312b1096fe751b88c4f909d010d867045657ccae` |
| WHATWG Notifications | 2026-10-05T18:19:09Z | Living Standard, last updated 5 October 2026 | `bd9f070b4a44cab1543dc4a2ca729999c533b89632b1ca0f563385a77aa1837f` |

PixelRAG: `tiles.json` for `https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning` (`complete: true`). Visual confirmation is tile 0000 only.

URLs: `https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning`, `https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization`, `https://github.com/modelcontextprotocol/modelcontextprotocol` (tags, commit `2026-07-28`, compare above), `https://a2a-protocol.org/latest/specification/`, `https://github.com/a2aproject/A2A/releases/tag/v1.0.1`, `https://github.com/midnightntwrk/midnight-dapp-connector-api/releases/tag/v4.1.0-beta.1`, `https://github.com/midnightntwrk/midnight-dapp-connector-api/releases/tag/v4.0.1`, `https://raw.githubusercontent.com/midnightntwrk/midnight-dapp-connector-api/main/package.json`, `https://github.com/shieldedtech/moth-wallet/commit/d48206a1957af09bf17bf5e941c2b5bccb12db63`, `https://github.com/cloudevents/spec/releases/tag/ce%40v1.0.2`, `https://notifications.spec.whatwg.org/`.

## Rejected alternatives

- One MCP artifact covering the changelog URL, the learn/versioning page, tag `2026-07-28`, tag `2026-07-28-RC`, and `main`.
- Reading the A2A `/latest/` banner as v1.0.1, or reading v1.0.1 as `main`.
- Treating connector `package.json` version `4.1.0-beta.1` as proof the tree is the beta.1 release commit.
- Treating Moth `API_VERSION` `'4.0.1'` as the version of connector `main`.
- Treating `isAllowed` as a network grant or a method grant.
- Treating `permissionsRevoke` as a dApp connector method.
- Treating the legacy scope string in the Moth comment as the npm scope upstream publishes at beta.0 and later (`@midnightntwrk`, with the old scope described there as an alias).
- Treating `modelcontextprotocol/specification`’s schema URL as a different document: the retrieved body hash matched the tag schema. Tags were still taken from `modelcontextprotocol/modelcontextprotocol`.
- Treating CloudEvents `ce@v1.0.2` (2022-02-06) as `spec.md` commit `6862e1dc` (2026-03-12).
- Assigning WHATWG Notifications a numeric version, or using it as the durable watch.
- Reopening, from this evidence, a mandatory network broker or wallet topic routing. This pass did not re-collect transport evidence; those decisions stay as written.

## Unresolved dissent

- Whether each of the 267 commits after MCP tag `2026-07-28` is backwards compatible. The versioning page allows the label to stick. This review did not diff them. The website can keep saying 2026-07-28 while `main` differs from `5f5440bb`.
- Whether `resources/subscribe` in the tag schema is a legacy method, a deprecated feature, or a live one. One string count is not a classification. The changelog page was not captured.
- Whether A2A v1.0.1’s TaskStatus and content-type notes change behavior relative to the 1.0.0 spec the banner still names. Section 3.6 says patch numbers should not matter. The release notes exist anyway. No v1.0.0-to-v1.0.1 spec diff was read. No ahead-count from v1.0.1 to main `679ab3af` was captured.
- The v1.0.1 Git commit message omits bugfix #1801 and dates the notes 2026-04-23; the GitHub release body includes #1801 and says 2026-05-26. Which list the tagged tree actually contains was not file-checked beyond those two API objects.
- `connect()` after `getSettings()` may still reject a network mismatch. `isAllowed` does not. Those are different claims; only the second is closed.
- Whether `SPECIFICATION.md` at `612db2b` documents InsufficientFunds. The compare subject says the change landed on main after `da90f631`. The spec text was not quoted.
- WHATWG snapshot commit hash on the 5 October 2026 living standard.
- Behavior of a real Moth extension session, Pages origin sharing, and wallet rejection. Source reading supports the grant warning; it does not replace the manual session gate.
- Dissent inside the other agent reports was not re-read. This file does not vote their unrelated conclusions up or down.

## Stack and data-fit gaps

Preserved from the product requirement and the decisions draft. This pass adds no measurement.

- Whole-shard recognition CPU cost and real sealed payload sizes are still open. JSON example sizes do not establish fixed-class wire fit.
- Store repair, finalized-root freshness, and RLN per-class credit compatibility stay original protocol gates.
- Mobile whole-shard feasibility stays unresolved.
- The dashboard and the subscription page show local interaction over synthetic or in-memory state. They do not show transport, decryption, live permission, a browser validator, durable database, or a business effect. Umbra/PostgreSQL and SQLite atomic cursor requirements are unimplemented integration work.
- Quote, invoice-observation, and sandbox-approval fixtures with `executes: false` stay the only accepted profiles. Other categories stay mocks.
- MCP host compatibility and adapter language stay gates. They are not admission dependencies.
- A Moth connection on the shared Pages origin exposes every implemented connector method to that origin, not the connection and status calls the demo intends to make. Acknowledgement does not shrink the grant.
