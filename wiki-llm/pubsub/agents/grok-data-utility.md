# Data-model skeptic: does v0.2 actually enable pub/sub?

Role: data-model skeptic. Ownership: this note and `../sources/grok-data-utility/`. No runtime, model, or other-doc edits. Drafts in this surge are evidence of what was written, not automatic truth. The helper `accepted_source` flag is only an HTTP 200 plus text-length heuristic; each item below was read.

## Approach

Read the untracked product draft `docs/product-requirements/pubsub-subscription-experience.md`, `model/README.md`, `model/profiles/lock.json`, `wiki-llm/pubsub/subscription-contracts.md`, `unified-data-model.md`, and `data-model-fit.json`. Compared that local shape with primary CloudEvents, CESQL, AsyncAPI 3.1.0, and JSON Schema 2020-12 texts retrieved by Scrapling. Treated search failures, the v1.0.2 subscriptions 404, and a PDF the extractor could not decode as non-evidence. Sol's subscription-contracts note and the privacy note were used as peer drafts, then checked against the same model files and fit report. PixelRAG grounding of the Subscriptions API page is recorded in the visual section after the first text pass.

## Intermediate findings and pins

Repo HEAD while reading: `5ff9627c30d06837c931fc4783ca271455bdeb1a`. `model/profiles/lock.json` and `model/README.md` are in that tree. Last commit that touched them is `f5edf05284b6888b1fa3dce2e92cf8605991000c` (2026-10-04). The product draft, `subscription-contracts.md`, and `data-model-fit.json` are untracked working-tree drafts as read on 2026-10-05.

Installed aliases, which are not themselves the contract identity:

| Alias | Commitment |
|---|---|
| `rfq.v0.2` | `sha256:8b5c6b89f6019fcb06b479e92f1b3bea340ac500cc218341e368e1ed2093071c` |
| `invoice.v0.2` | `sha256:dd3b68c4f25c4ca87a57e5e5dda88cb8a1630fa9a1b0ab394744fdf984eb047a` |
| `agent.v0.2` | `sha256:beaf501a8fdeefe757c340b1945dcd3e9c7c6e3fb4e00612f724afab7605b330` |

Exact types in `model/README.md`: `mpe.rfq.quote.v0.2`, `mpe.invoice.payment-observed.v0.2`, `mpe.agent.approval.v0.2`. Every documented success keeps `executes:false`. The loader refuses unknown contracts and reference keywords. Chain catalog entries and v0.1 stay outside runtime dispatch. Independent Python/Rust/TypeScript agreement is described for the RFQ campaign only.

`data-model-fit.json` (`generatedUtc` 2026-10-05T18:10:35Z, trusted now `2026-10-04T12:00:00.000Z`, context sha256 `ddbfa27d8b450dbf03da8183538e4fbdcff9916208fbb7f797f502aa4e769ffc`) is an offline `Harness.check` log. Its useful split is qualitative. Validation can succeed while `localMatch` is false (`payment-final` against a pending observation). A second occurrence of the same approval action can succeed as `duplicate-action` and still match `all`. Changed approval content conflicts. Current-day quote and approval clocks, missing dealer role, missing payment evidence, a new type stuffed under the RFQ profile, and a subscription field inside the business envelope are refused. The file's own limits say there is no subscription runtime, no browser validator, and no live authority. A conformance tally is not evidence that a consumer product exists.

### CloudEvents 1.0.2

Pin: tag `v1.0.2` via `https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/spec.md`. Retrieved 2026-10-05T18:17:55Z. Raw sha256 `e327435c858d19fd171e4ab9781a01fc22dfa949d23c4220976529ebd16a1aa3`.

Producers must keep `source` + `id` unique per distinct event. Consumers may treat the same pair as a duplicate. `specversion` for this document is the string `1.0`; patch 1.0.2 does not change that attribute. `type` is producer-defined and often used for routing. `dataschema` is an optional URI; incompatible schema changes should use a different URI. `subject` is optional and is described as helpful precisely when middleware cannot interpret `data` and wants a string filter. That is a cleartext routing hint.

Primer, same tag, raw sha256 `e547028f1e4f509ba3b713333eb4d2f53ec71bb79cc034db82520ece082a88ca`. Non-goals include protocol-level routing, event persistence, and any mechanism for authorization, integrity, or confidentiality. `type` stays stable across compatible data changes and should change across incompatible ones. `dataschema` is informational for tooling. Neither attribute is a commitment of schema bytes.

JSON format, same tag, raw sha256 `30778f995a2c82f3ac6c4f7cd56415d675111990151c9ab67bd0a2de1d0e1ce5`. Envelope media type `application/cloudevents+json`. Extensions are top-level JSON properties. That mapping is for a CloudEvents message, not for an MPE cleartext header.

Partitioning extension, same tag, raw sha256 `38b5bf2b9e46a52917710f5ca2bba3cc3b5d91649f7a463293b6cd67634fa94e`. `partitionkey` is a broker scaling attribute. The text says a hop may change or remove it. It is not a stable consumer identity.

`https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/subscriptions/spec.md` returned HTTP 404, body `404: Not Found`, raw sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`. The released 1.0.2 tree fetched here has no subscriptions specification.

### Subscriptions API 0.1-wip and CESQL

Subscriptions spec at commit `2ed3806b4ad8fda35813263cfefb2d73098b7655`, path `subscriptions/spec.md`. Retrieved 2026-10-05T18:17:55Z. Raw sha256 `fc189ca4cbd65ea8fd11373b38d83f49e69563398b06a7d8caf7643454d4852e`. Title: CloudEvents Subscriptions API, version 0.1-wip. It defines a subscription manager, push and pull delivery, a subscription object with `filters`, `sink` URI, `protocol`, and `protocolsettings`, and it says subscription offers are published in a CloudEvents Registry service. The relationship between producer and manager is explicitly not formalized. Required filter dialects are `exact`, `prefix`, `suffix`, `all`, `any`, and `not`, matched on CloudEvents attributes. Optional dialect `sql` points at CESQL. Create and Delete are SHOULD; only Retrieve is REQUIRED. A filter the manager does not support must reject the subscription.

The README at that same commit is 99 bytes and only points at `spec.md`. The helper marked it rejected for length. The bytes are a real short index, not a second specification. Raw sha256 `b8f4736b4df4e51d9ad04979fd662b6d85cefae52c5641cc5bdaa5048b78aaae`.

CESQL at a different commit, `a89841854a6e070f28316e82e151da159bb87b1a`, path `cesql/spec.md`. Retrieved 2026-10-05T18:17:55Z. Raw sha256 `c799d84fe5e31665edd4506652421a5da91d621f4a5f79979707f960a315e03a`. Header says version 1.0.0. Expressions must not mutate the event. As a subscription filter, the output must be boolean, and any error fails the match. No Git tag object was fetched, so the pin is this commit plus the document's own version string. It is not the same commit as the Subscriptions API text, and it is not part of the v1.0.2 tag fetch above.

Registry discovery failed, so no registry specification is in evidence:

- GitHub code search `https://api.github.com/search/code?q=repo:cloudevents/spec+CloudEvents+Registry` returned HTTP 401 `Requires authentication`. Raw sha256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`.
- DuckDuckGo HTML for `CloudEvents Registry service specification` returned HTTP 403. Raw sha256 `203a52e8ce75829b48a6f9f83314e04c0acebde094d3b8ecea6dbac6799f37f2`.
- `docs/share/2021-06-24-DiscoveryOverview.pdf` at the subscriptions commit returned HTTP 200, raw sha256 `e9462ff09c20b5678c436a08bf45689e4468fa8a5de7f4cb1132c0321b53e933`, 188761 bytes. Text extraction failed on page 1 with a FlateDecode error. The helper still set `accepted_source` because the error string is longer than 120 characters. Those bytes were not read as a registry design.

### AsyncAPI 3.1.0 and JSON Schema 2020-12

AsyncAPI `https://raw.githubusercontent.com/asyncapi/spec/v3.1.0/spec/asyncapi.md`. Retrieved 2026-10-05T18:19:30Z. Raw sha256 `983a9c0ccb35412d4f6f254ab1ae9ea09a560664b1e41efb0109b12d0cd91869`. The document describes operations an application performs. It states that it assumes no topology. A channel used to receive is not guaranteed to be the channel another application uses to send. Bindings carry protocol detail. The local subscription draft cites AsyncAPI 3.0; the text verified here is 3.1.0. Those are different pins.

JSON Schema index `https://json-schema.org/specification` says the current version is 2020-12 and the previous was 2019-09. Retrieved 2026-10-05T18:22:06Z. Raw sha256 `6fdee9b204c2d77b0c46aa6d63637337216f5b1724fbe7bd033a541f64032931`.

Core `https://json-schema.org/draft/2020-12/json-schema-core`. Raw sha256 `7f63860fc1ede15acdc7eaba5ec64f96bc6a2d6e2358776ae07604291949612c`. `$ref` and `$dynamicRef` are URI references. The resolved URI is an identifier. Implementations should not perform a network operation when they see a network-addressable URI. A schema need not be downloadable from that URL.

Validation `https://json-schema.org/draft/2020-12/json-schema-validation`. Raw sha256 `b5a807b322902b4baec82a39a10457569355aff67e3005c83784046d8f65930e`. Structural keywords do not encode cursor ownership, installed commitments, clocks, or action conflicts.

### Moth connector, as a consumer-boundary check

Commit `d48206a1957af09bf17bf5e941c2b5bccb12db63`, `packages/extension/lib/connector/constants.ts`. Retrieved 2026-10-05T18:22:03Z. Raw sha256 `248bb5c08c0a2cd66cd39c1ccd27086fa062312a6f404f7d0574974194fa2c32`. `API_VERSION` is `4.0.1`. `IMPLEMENTED_METHODS` includes `makeTransfer`, `submitTransaction`, `signData`, `makeIntent`, `balanceSealedTransaction`, and `balanceUnsealedTransaction`, plus read methods. `deriveAppSecret` is listed as an extension method outside the 4.0.1 standard. Package `@shieldedtech/moth-extension` at that commit is version `0.14.1`, described as experimental and unaudited. A watch over quotes or payment observations does not select among these methods. The connector surface that exists is wider than a read-only inbox.

## Recommendation

Keep pub/sub state out of the business envelope. Use the three installed v0.2 profiles only as local interpretation of quote, payment-observation, and sandbox-approval payloads. Put watches, revisions, cursors, gaps, and dispositions in a closed local control-plane record whose contract identity is the sha256 commitment, not the alias string.

The exact intersection to install is small:

| Profile commitment | Category label | Predicates | What a match may do |
|---|---|---|---|
| RFQ lock above | quotes | `all` | Show an off-chain quote that already passed dealer role, economics, and the pinned clock |
| Invoice lock above | payments | `all`, `payment-final` | Show Pending, Final, or Reversed as source assertions. `payment-final` selects only the Final assertion |
| Agent lock above | approvals | `all`, `approval-report` | Queue a WriteReport candidate. `approval-report` selects report candidates only |
| none (`mock-only`) | contracts, credentials, ops | no model predicate | Unsigned UI fixtures and local runtime status. Never enter `Harness.check` |

`payment-final` on a quote, `approval-report` on an invoice, and any model predicate on `mock.local.v1` fail at intent installation. `sourceEquals` empty means the shard's already admitted sources. It does not mean anonymous senders. Category strings are local navigation labels. They are not signed claims and they are not relay subjects.

A match is computed only after validation success, and it still leaves `executes:false`. Wallet and DApp screens can render that result. They cannot call Moth transfer, submit, sign, or intent methods because a selector matched.

Promote a fourth profile only when all of these exist together: closed schema and rules, a new commitment, units and lifecycle, source evidence the validator can check, an action boundary that stays `executes:false` until a separate authorized effect exists, and at least one independent interpreter agreeing on a shared corpus. The RFQ campaign is the only profile the model README describes that way. Invoice and agent selectors are useful inside this repository's Python validator. They are not yet a multi-party payment or approval standard.

Missing events belong in the control plane. A cursor behind retention becomes a gap with reason retention, missing-range, or conflict. Resume does not jump to latest. Replay uses the revision's stored commitment, not whatever `lock.json` now aliases. Delivery and processing cursors stay distinct from occurrence `(source,id)` and from approval action `(authorityDomain, executionScope, actionId)`.

## Where the current stack is enough

CloudEvents 1.0.2 already matches the occurrence rule the model uses: `(source,id)` is the duplicate identity, and a changed body under that pair is a different event, which the model treats as conflict. The ten business fields, including `mpeprofile` and `mpecontract`, already sit inside the proposed encrypted body. No new CloudEvents context attribute is required for the pilot.

JSON Schema 2020-12, used as an offline closed schema with the loader's reference-keyword ban, is enough structure for the three profiles. The model already refuses unknown contracts, duplicate keys, and extension fields.

The fit report already shows the consumer-relevant split for fixtures: pending payment validates and does not match `payment-final`; expired quote and approval fail closed; a subscription field in the envelope fails closed; approval conflict fails closed; duplicate action is visible without executing.

Moth 4.0.1 at the pinned commit is enough to discover a wallet and read connection status after a gesture. It is the wrong layer for subscription filters.

No message broker, registry, CESQL engine, or AsyncAPI channel catalog is required for the private local inbox.

## Stack additions that are actually required

A local control-plane schema, separate from the three profiles, with the intersection table above checked before a watch is stored. Immutable revisions that store the commitment, the predicate, the owner, the sink allowlist entry, and the start cursor. A journal that can emit a gap instead of skipping. Quarantine as a durable disposition. Principal isolation so one watch's selector is not another principal's filter.

That schema is an application contract. It is not a fourth `mpe.*` event type and it is not an MPE wire change.

An AsyncAPI 3.1.0 file may later describe the local operations (`watch.create`, `watch.read`, `consumer.commit`, and a separate `action.prepare`). If it is written, its channels are local handle names. They must not be published as bus topics. Do not write that file until the control-plane schema is frozen; the 3.0 citation in the subscription draft and the 3.1.0 text fetched here should not both be treated as the pin.

## Rejected alternatives

CloudEvents Subscriptions API 0.1-wip as the MPE subscription model. It is absent from the v1.0.2 tag, it sends filters and sink URIs to a subscription manager, and it assumes a registry that was not retrieved. Its `exact`/`prefix`/`suffix` dialects filter cleartext attributes, which is the disclosure profile this system is trying to avoid on the relay.

CESQL 1.0.0 as a network or even a first local selector language. The optional `sql` dialect in the wip spec evaluates expressions over event attributes in the manager. A predicate language that can say `source LIKE '%cloudevents%'` will grow into an interest oracle and an injection surface. The three enum predicates cover the only distinctions the validator already computes.

`subject`, `type`, and `partitionkey` as routing keys. The primer excludes protocol routing from the event. `subject` exists for middleware that cannot read `data`. `partitionkey` may change per hop. Putting a business profile or a wallet interest in any of them publishes the subscription.

A universal registry of profiles, chain vocabulary, or AsyncAPI channels. The model README already has a 291-entry catalog that runtime does not admit. Publishing it, or the wip subscription offers, as a discoverable registry makes every interest and every unfinished chain word look like a supported event.

Remote `$ref` and `$dynamicRef` in received events or in installed bundles. JSON Schema says a URI is an identifier and should not be fetched. The loader already rejects reference keywords. Keep that ban. Schema bytes travel inside the reviewed bundle.

Stuffing cursors, sink URLs, webhook credentials, or watch revisions into the business envelope. The fit report already rejects a subscription field there. CloudEvents persistence and authorization are non-goals, so the envelope cannot become the consumer journal.

Using the Moth method list as the wallet subscription API. `makeTransfer`, `submitTransaction`, `signData`, and `makeIntent` are implemented on the origin grant. A quote watch must not enable them. Local disconnect does not narrow that grant.

Treating `lock.json` aliases as version identity. `specversion` `1.0` intentionally hides the 1.0.2 patch. MPE meaning changes need a new commitment even when the alias string looks compatible. Delivery resolves the hash stored on the revision.

Silent promotion of contracts, credentials, ops, ERC-20 observations, or Solana transfer observations into the same selector enum. Those are either unsigned mocks or read-only prototype slices. The invoice profile's `Final` is already easy to over-read; adding chain words beside it would make the inbox look like a general blockchain subscription.

## Data-model fit and limits

The bounded model fits three local consumer readings:

- A wallet can show a Shares/USD quote while the supplied context gives the dealer role and the trusted clock is inside the quote window. The pinned fixtures expire at 13:00Z on 2026-10-04. On 2026-10-05 the same bytes are a historical refusal (`quote-validity`), not a live alert.
- A DApp can separate Pending, Final, and Reversed payment observations when the context carries matching complete evidence. `Final` remains a source assertion. The base-context acceptances in the fit report use that supplied fixture evidence. They do not show a live sender proving payment.
- An agent can queue one sandbox WriteReport candidate and can see `duplicate-action` versus `action-identity-conflict`. The candidate does not authorize a tool, a signature, or a second effect.

It does not fit a general pub/sub product:

- There is no subscription event, no cursor, and no gap in the business schemas. Until the control plane exists, a consumer cannot tell a quiet counterparty from a missed invoice.
- Invoice and agent lack the multi-implementation campaign the README describes for RFQ. One Python validator agreeing with itself does not promote those profiles.
- `payment-final` and `approval-report` are local predicates over validator status, not CloudEvents filter dialects and not ledger queries.
- Display title and summary in the proposed incoming record are local strings. They do not authenticate the sender.
- The website demonstration the product draft describes is in-memory mock delivery. Unsigned contract, credential, and ops cards are not model events. An offline receipt embedded in a page is not a browser authority service.
- Raw event size limits in the model README do not measure sealed MPE payloads.
- No customer workflow baseline is in these sources. Usefulness here means the fixtures express a coherent quote, payment observation, or approval candidate. It does not mean a wallet user or a DApp integrator has adopted it.

## Proposed consensus

Adopt the three-profile business vocabulary and the local control plane as separate objects. Selectors store a commitment hash plus a predicate from the table above. Installation rejects every other intersection. Evaluation runs only after validation, and every accepted business result keeps `executes:false`.

Keep occurrence identity and approval action identity on their existing ledgers. Do not invent action keys for quotes or payments.

Record gaps explicitly. Do not advance a cursor across a retention hole. Do not treat latest-start as recovery.

Leave contracts, credentials, ops, the chain catalog, and any new CloudEvents extension out of runtime dispatch until the promotion conditions above are met.

Do not implement the Subscriptions API, CESQL, a CloudEvents Registry, or public AsyncAPI business channels in this stack.

Wallet connection and a local watch stay separate grants. The watch does not authorize Moth signing or payment methods.

## Unresolved objections

The invoice `Final` label will be read as money that moved. Keeping `payment-final` as a selector is still right for the observation inbox, and the screen has to say that the source asserted it. If the product cannot show that distinction, the selector should stay in the DApp fixture view and off the wallet's primary alert.

A local "unexpired only" predicate is tempting for the wallet. Expiry is already a validation failure under the trusted clock. A second predicate would hide the historical row and start a filter language. Prefer a display mode over another enum value until a real product asks for it.

Invoice and agent watches are ahead of their interoperability evidence. Consensus can allow them as single-implementation demo selectors. Calling them partner-ready payment or agent contracts overclaims the README.

The Subscriptions API text mentions a registry, and the overview PDF at that commit did not yield text. Someone can still claim a registry spec exists. It is not adopted here, and it is not refuted by a decoded document either.

CESQL's header says 1.0.0 while the Subscriptions API that references it is 0.1-wip at another commit. Their relationship is one optional dialect pointer, not a stable pair this project should implement.

The subscription draft's AsyncAPI 3.0 citation and the 3.1.0 text fetched here disagree. Neither should be implemented until the control-plane fields stop moving.

The fit report and the product draft were untracked when this note was written. A later edit to either can invalidate the clock, the commitments, or the `executes:false` claim. Re-read the lock file and the fit report before promoting a selector.

## Source URLs

Used as text evidence:

- https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/spec.md
- https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/primer.md
- https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/formats/json-format.md
- https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/extensions/partitioning.md
- https://raw.githubusercontent.com/cloudevents/spec/2ed3806b4ad8fda35813263cfefb2d73098b7655/subscriptions/spec.md
- https://raw.githubusercontent.com/cloudevents/spec/2ed3806b4ad8fda35813263cfefb2d73098b7655/subscriptions/README.md
- https://raw.githubusercontent.com/cloudevents/spec/a89841854a6e070f28316e82e151da159bb87b1a/cesql/spec.md
- https://raw.githubusercontent.com/asyncapi/spec/v3.1.0/spec/asyncapi.md
- https://json-schema.org/specification
- https://json-schema.org/draft/2020-12/json-schema-core
- https://json-schema.org/draft/2020-12/json-schema-validation
- https://raw.githubusercontent.com/shieldedtech/moth-wallet/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/lib/connector/constants.ts
- https://raw.githubusercontent.com/shieldedtech/moth-wallet/d48206a1957af09bf17bf5e941c2b5bccb12db63/packages/extension/package.json

Visually inspected, same subscriptions commit:

- https://github.com/cloudevents/spec/blob/2ed3806b4ad8fda35813263cfefb2d73098b7655/subscriptions/spec.md

Recorded failures, not evidence:

- https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/subscriptions/spec.md (404)
- https://api.github.com/search/code?q=repo:cloudevents/spec+CloudEvents+Registry (401)
- https://html.duckduckgo.com/html/?q=CloudEvents+Registry+service+specification (403)
- https://raw.githubusercontent.com/cloudevents/spec/2ed3806b4ad8fda35813263cfefb2d73098b7655/docs/share/2021-06-24-DiscoveryOverview.pdf (HTTP 200, text extraction failed)

Local pins, not primary web sources: repo `5ff9627c30d06837c931fc4783ca271455bdeb1a`, `model/profiles/lock.json`, untracked `docs/product-requirements/pubsub-subscription-experience.md`, `wiki-llm/pubsub/subscription-contracts.md`, and `wiki-llm/pubsub/data-model-fit.json`.

## Visual grounding

PixelRAG 0.4.0 CDP captured the public GitHub preview of the Subscriptions API at the same commit as the raw markdown. URL `https://github.com/cloudevents/spec/blob/2ed3806b4ad8fda35813263cfefb2d73098b7655/subscriptions/spec.md`. Scrapling HTTP 200 on 2026-10-05T18:26:57Z. HTML raw sha256 `c33de040d21c77175fdefd9cf685aaac4a20615bddaaecc5b9a7bd05441cceed`. Fifteen tiles, renderer exit 0, `verified_capture` true. The page chrome shows commit `2ed3806`, path `spec/subscriptions/spec.md`, Preview selected, and "1062 lines (774 loc) · 35.5 KB". The rendered text agrees with the raw markdown on the points below. Tiles 0, 1, 8, 9, and 10 were read. The other ten tiles are hashed in `cloudevents-subscriptions-visual.json` and were not inspected.

Tile 0, sha256 `87ccca74b69c15a3a642f34d108c9bc9013952075507beaf92e469c98d4b8b40`, shows the title "CloudEvents Subscriptions API - Version 0.1-wip", the abstract naming a subscription manager, and the introduction sentence that subscription offers are published in a CloudEvents Registry service. The same tile says the document does not formalize how the manager obtains events. It also says native MQTT, and the other bound transports, remain in scope, and that a CloudEvents-specific MQTT subscription would only complicate implementations.

Tile 1, sha256 `6b7c39ebb4b5d8bb3c6930b5d62dd9a3aee5d8a0e2ea828e2134bf10fe1d963e`, defines Subscription as the consumer's interest plus the delivery method, and Subscription Manager as the entity that distributes events to registered consumers. It requires a compliant manager to support at least one referenced transport. Pull delivery is consumer-initiated. Push delivery must carry everything the manager needs to open the channel. The visible example is an MQTT topic acting as the manager.

Tile 8, sha256 `7c339b574ffb3a08efbf390976b22846e37c36a8e8037897ed72ea2a923e7de2`, is protocol settings, not a business schema. Kafka `topicname` is the topic to publish to. `partitionkeyextractor` is an expression. NATS `subject` is required and is "the name of the NATS subject to publish to." Sink credentials begin on this tile.

Tile 9, sha256 `a30bd91526239ba1158feb25493f9892f0f4fdc933c137fbd6d89808e34ce5f3`, continues sink credentials: PLAIN identifier and secret, access token, refresh token, and a refresh endpoint URL. Secrets and access tokens are marked as not returned on retrieval. That is still a subscription object that carries delivery secrets to a manager.

Tile 10, sha256 `2c274bf9f8893bd0d637e14755af6f222b0799507dc02bdd7e7fed567268ce97`, shows section 3.2.4. A false filter means the event must not be sent to the sink. An unsupported dialect must reject the subscription. It then says six filter dialects must be supported by every implementation, and the visible ones are `exact`, `prefix`, and `suffix` on CloudEvents attributes. The `exact` example matches `type` `com.github.push` and a `subject` URL. `prefix` and `suffix` match the same kind of cleartext attributes. This is manager-side interest filtering, which is the disclosure profile the local MPE selector is supposed to avoid.

No other primary page was tiled for this note. The v1.0.2 core spec, CESQL, AsyncAPI 3.1.0, and JSON Schema 2020-12 remain text captures. The discovery PDF is still an undecoded HTTP 200, not a visual source. The v1.0.2 subscriptions URL remains a 14-byte 404. GitHub code search remains 401, and the DuckDuckGo query remains 403.
