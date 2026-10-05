# Stack feasibility for subscriptions: distributed systems review

Role: distributed systems architect. Owned outputs: this report and `../sources/opus-stack-feasibility/`. No implementation, model, website or other research files were edited. Research date 2026-10-05. Model: claude-opus-5-5.

Question: are GossipSub, symmetric recognition, RLN/Semaphore patterns, the Midnight Registry and UmbraDB/SQLite enough to give wallets, DApps, humans and agents a useful subscription experience? Which local components must be built, and does anything need a third protocol or a new dependency?

## Short answer

The existing stack is enough at the network layer. The project does not need a third pubsub protocol, a broker or a new wire field. The missing pieces are local software inside each recipient's trust domain:

- a whole-shard intake and recognition service;
- a durable consumer journal holding original sealed bytes, per-watch cursors and dispositions;
- a local control plane for watch intents and grants;
- an SDK over that journal, with MCP and other adapters on top;
- a store-feed client that repairs gaps by fetching whole-shard windows.

None of these change the MPE wire, the recognition rule or the Registry roots. Consumer slowness must never propagate upstream into GossipSub. Gaps are repaired from Store Nodes by shard window, never by stream or selector.

Three dependency decisions are still open and must be settled by measurement, not adoption: the Zerokit v3 RLN relation's fit to MPE per-class credits and Midnight's field/hash choices; negentropy-style reconciliation for store-to-store repair; and the move from the vendored GossipSub patch to upstream 0.51.

## Approach

I started with the repository's own claims: README, `docs/product-requirements/recommended-stack-and-use-cases.md`, the design draft (`docs/design-document/draft-final/`), `experiments/` (Cargo manifests, vendored GossipSub, COVERAGE/RESULTS), and the current research drafts `standards.md`, `subscription-contracts.md`, `wallet-consumers.md` and the sol agent reports. I treated those drafts as hypotheses.

I then pinned current versions and behaviour from primary sources, fetched only with Scrapling through `research.py`: GitHub REST API listings, raw spec and source files, crates.io, and sqlite.org. One primary page was captured visually with PixelRAG and inspected. Earlier fetches from the interrupted session were reused, not fetched again. For each claim I read the captured text myself; the helper's `accepted_source` flag is only an HTTP heuristic.

## Source findings and pins

| Component | Observed current state (2026-10-05) | Consequence |
|---|---|---|
| rust-libp2p | Release `v0.57.0`, 2026-09-11. Master head `2e3407e8166c21bfce7b354739c6f11e39a3fb2a` (dependency bumps). | `experiments/Cargo.toml` already pins `libp2p = 0.57`. No upgrade needed. |
| libp2p-gossipsub | crates.io max/stable `0.50.0` (2026-09-11); earlier `0.49.5` (2026-07-21). The 0.50.0 changelog has: a GRAFT topic-growth fix (GHSA-g3g5-x568-qvqx); a default `MaxCountSubscriptionFilter` with limits of 100; `max_control_message_size` defaulting to 16 KB; all subscriptions sent in one hello RPC. | The experiment vendors 0.50.0 with a small custom-Version patch for a network-scoped `/…/1.2.0` protocol id (COVERAGE MPE-NET-008). The subscription cap does not matter for a few shard topics, but relays that carry many shards must set it explicitly. |
| gossipsub master, unreleased `0.51.0` | Rejects messages carrying `key` in `ValidationMode::Anonymous`, matching `StrictNoSign` (PR 6621). IDONTWANT removal from the send queue becomes O(queue+ids). | Fits the MPE anonymous envelope directly. Rebase the vendored patch onto 0.51 when it is released, and add a conformance test that envelopes never carry from/seqno/signature/key. |
| GossipSub spec | v1.2 (IDONTWANT) is a Working Draft, r2 2026-08-30. v1.3 (Extensions control message) is a Candidate Recommendation. The Partial Messages extension is a Working Draft. The latest gossipsub-path commit is `9e9628a4f9a2be2ac79f40a162cd978c5b200b03` (2026-09-05, "downscore peers on protocol violations"). | v1.2 is the right profile. v1.3 and Partial Messages add nothing MPE needs (see rejected alternatives). |
| GossipSub implementation status (visual) | Pinned page at `9e9628a`: all listed implementations have v1.2. Rust v1.3 is "In Progress". Rust has no Choke or Partial Messages, has IDONTWANT on first publish, and has no batch publishing. The file's own last change shows "last year". | The status table may be stale. Use it as a lower bound, not as current Rust status. |
| Zerokit (RLN) | `v3.0.0` 2026-08-04 is a full redesign: runtime type-state `RLN<Stateful|Stateless>`, builder API, multi-message-id selected at runtime, unified serialization. `v2.0.2` (2026-05-29) documented a 290-byte proof wire layout used by waku-rln-relay. Nightly 2026-10-05 adds Poseidon2. The README models a leaf as `H(id_commitment, user_message_limit)` with `0 <= message_id < limit`. | The best evaluation engine, but its serialization changed across majors. The MPE wire must pin its own proof encoding and not inherit Zerokit's byte layout. |
| Waku RLN membership contract spec | Membership states include GracePeriod and Expired, and each membership has exactly one holder. Defaults: 600 s epoch, 20–600 messages per epoch per membership, 160000 total, 30-day grace period. | The lifecycle and holder patterns are worth reusing in the Registry design. The parameters do not carry over: MPE uses 60-second admission windows with per-size-class credits. |
| Waku relay sharding | Static shards: 1024 shards per cluster, 2^16 clusters. Content topics are assigned to shards by the app protocol. | Neutral numbered shard naming is a good convention. Waku content topics are application labels visible to relays, so they must not be copied. |
| Waku store-sync | Combines Store queries with the WAKU-SYNC protocol. Recommends a 1-hour sync window and a 6-hour cap on offline catch-up. | Confirms that real relay deployments expect routing loss and repair it out of band. MPE already specifies Store Nodes, retention receipts and repair, so this is a design reference, not a dependency. |
| negentropy | Range-based set reconciliation with fingerprint ranges and frame-size limits. Last commit `b36876529227…` 2026-08-01. | A candidate for Store-to-Store repair over opaque envelope IDs. Rust implementation maturity was not verified. |
| Semaphore | `v4.14.3` 2026-07-08 (lean-imt update). semaphore-rs at `v0.1.0`, last commit `ccf81861d4f1…` 2025-10-07. | Use the identity and witness lifecycle patterns only, as the stack document already says. The young Rust port is not a dependency. |
| Midnight DApp connector | Official repo head `612db2b62dbd78c079da62e57e7b8585a204b858`. `v4.1.0-beta.1` fixes packaging. `v4.1.0-beta.0` moves to the `@midnightntwrk` scope and adds an optional `signData` signature `scheme`. | No change to the subscription design. `signData` is signing authority and stays out of the dashboard connector. |
| Moth wallet | Head `d48206a1957af09bf17bf5e941c2b5bccb12db63` (2026-10-01), "auto-lock dapp activity". | Matches sol-wallet's pin. Auto-lock means connection status can change during a session, so the connector's explicit status check is necessary. |
| UmbraDB | Head `3c0c68b3d0397ee2e8344b77e9ed715132fef6ca` (2026-07-26), indexer-parallelism research: CPU-bound against indexer 4.3.3. | No MPE consumer-journal capability has been published. The future MPE capability named in the stack document is still to be built. |
| SQLite | Chronology lists 3.53.4 (2026-07-24) as latest. WAL documentation: one writer at a time, all processes on one host, no network filesystems, checkpoint starvation risk. | Suits a standalone node or client journal if exactly one local daemon writes it. Wallets, DApps and agents must reach it through the daemon, not by opening the file. |

Fetch failures, recorded honestly: `vacp2p/rfc-index` tree and contents returned 404 (`vac-rfc-tree`, `vac-rfc-waku-core-dir`), and `zerokit/CHANGELOG.md` returned 404. None of these is cited as evidence. The vac RFC paths referenced inside the Waku specs were not independently confirmed.

Visual grounding: `gossipsub-impl-status-visual` (Scrapling 200; PixelRAG 0.4.0 CDP, exit 0, two tiles). I inspected tile_0000 (SHA-256 `796db6604afbeaefdff18beb2ad95e31908d4f251cd9dfbeaed52de8fdff8fe9`). It shows the pinned commit selector `9e9628a`, the version, extension and improvement tables quoted above, and the file's "last year" change marker. Every other source in this report is grounded in text only.

## What already suffices

- **Transport:** rust-libp2p 0.57 with GossipSub 0.50 in the v1.2 profile, anonymous validation, peer scoring and IDONTWANT. The experiments already run this on TCP/Noise/Yamux. Whole-shard fan-out is ordinary topic subscription with one topic per shard, so the broker never learns business interests.
- **Recognition:** the salted 16-byte Recognition Tag (a keyed hash of a fresh salt under the stream key) is all the selection a recipient needs. No upstream filter, bloom filter or detection key is required.
- **Admission:** one RLN-style proof against finalized Registry roots, with Semaphore lifecycle patterns. The receiver never needs a second proof to subscribe.
- **Recovery storage:** SQLite (single writer, WAL) for standalone Rust nodes and clients; UmbraDB/PostgreSQL for backend hosts, once the MPE atomic capability exists.
- **Event meaning:** model v0.2 profiles inside the sealed body; CloudEvents-style `(source,id)` occurrence identity; the separate approval action ledger described in `subscription-contracts.md`.

## What must be built

These are local products. None of them is a protocol.

- **Intake and recognition service** (Rust, alongside `mpe-node`). It subscribes to assigned shard topics, verifies admission, and first appends each original sealed envelope to the journal. Only then does it try each authorized stream key against the tag. Because every envelope has a fresh salt, recognition costs one keyed hash per (envelope, stream key) pair and nothing can be indexed in advance. Cap the stream keys per local principal (the contracts draft already limits arrays to 16) and measure the cost against the class-0 shard rate.
- **Consumer journal.** It holds an append-only log of original envelopes; a decryption/recognition record per envelope; the `(source,id)` occurrence index with conflict detection; per-watch delivered and processed cursors; quarantine; and the action ledger. Cursors are local journal positions, never EIDs. Cursor and checkpoint updates commit atomically with dispositions (the SQLite transaction, or the planned Umbra MPE capability).
- **Local control plane.** It stores `LocalSubscriptionIntent` revisions and runtime state as already specified, plus grants that bind principal, selector, sink, expiry and readable fields. It is reachable only over local authenticated IPC. It has no network endpoint and never maps selectors to shard topics.
- **SDK.** A Rust core with a TypeScript-facing client offering `watch.create/list/read/pause/resume/close`, `consumer.commit` and `action.prepare`. The MCP adapter (current 2026-07-28 revision, per sol-standards) turns journal changes into `subscriptions/listen` invalidations, followed by a bounded `watch.read`. A wallet extension or DApp uses the same API. Wallet connection stays a separate session with no subscription rights.
- **Store-feed client.** It fetches whole-shard windows by time or cursor range from at least two Store Nodes, compares retention receipts, and records explicit gaps when coverage is missing. It is the only way to backfill before the local journal's retention starts.
- **Optional gateways,** each opt-in and labelled. A remote selector gateway is a weaker disclosure profile (as the wallet draft says). Outbound webhook export is a separate disclosure decision. An A2A task gateway serves commissioned work only.

## Compose plan

```
GossipSub shard topic(s) ──► admission verify (RLN vs finalized root window)
          │                                  │
   Store Nodes ── whole-shard window fetch ──┤
                                             ▼
                        journal.append(original sealed bytes)   ← never gated by consumers
                                             ▼
                 recognition (tag × authorized stream keys) → decrypt → v0.2 validate
                                             ▼
          occurrence index (source,id) · quarantine · action ledger
                                             ▼
        per-watch selectors (local only) → pull credits → wallet / DApp / human / agent
```

**Root compatibility.** Relays and receivers accept admission proofs against a bounded window of recent finalized Registry roots. The window must cover at least one admission window plus propagation and finality lag. A proof against an older root is rejected and logged; it never silently causes a refetch. A consumer joining an existing node needs no Registry interaction. A new node needs the current finalized root set before it validates traffic.

**Wire compatibility.** Nothing above adds or removes envelope bytes:

- Fixed size classes and the tag rule stay exactly as specified.
- GossipSub runs in anonymous mode with a content-derived message id.
- The local selector, category, watch handle and cursor are never written to the wire or to a Store request.
- Store requests name a shard and a window, never a stream.

**Consumer joining.**

- *A new watch on a running node* starts at `latest` (the journal high-water mark), at `earliest` (local retention, with coverage stated), or `after` a journal cursor. Starting before local retention requires an explicit whole-shard Store backfill, after which recognition runs locally.
- *A new node joining a shard* subscribes to the shard topic (participation is visible, as the README already concedes), backfills its retention window from Stores, and only then opens watches. Until backfill finishes, coverage reads "partial", never "complete".
- *A new stream key for an existing watch* requires re-running recognition over the retained journal. That is local CPU work with no network signal.

**Backpressure.** There are two separate loops.

- *Network intake* runs at shard rate and cannot be slowed by consumers. GossipSub has no consumer backpressure; stalling it costs mesh score and leaks timing. The existing validation bounds stay: FairQueue limits of 8 per peer and 128 per node, and a token bucket of 20/s per peer and shard ahead of proof checking (COVERAGE MPE-SEC-009/010). If the node falls behind, missed envelopes become a store-repair task, not dropped consumer events.
- *Journal to consumers* uses pull credits (`maxInFlight`) plus event and byte caps per watch. At capacity, delivery stops and backlog is shown. Undecided originals are never evicted. When journal retention overtakes a cursor, the watch becomes `gapped` and needs an explicit new revision or an authorized archive repair. Recognition and decryption may lag intake as a bounded internal backlog. If that backlog exceeds journal retention, every watch on the affected stream gets a gap record.

**Gap semantics.** There are three gap sources, recorded separately:

- transport loss, repairable from Stores within their retention;
- Store retention exhausted, permanent, with receipts showing who promised what;
- local journal retention exhausted, permanent for that consumer.

Quiet reception never means complete coverage. Repair fetches by shard window, so a gap does not reveal which stream was missing.

## Data-model fit

Model v0.2 fits inside the sealed body unchanged. `(source,id)` occurrence dedup and the `(authorityDomain,executionScope,actionId)` action ledger map directly onto the journal. Selector categories are local derived metadata, as the contracts draft requires.

The model has one sizing consequence. Measured as compact, key-sorted JSON (an approximation of JCS), the current examples are: `invoice-*` at 805–815 B, `rfq.json` at 973 B and `agent.json` at 1040 B. Class 1 carries 854 B of payload, so invoice observations fit class 1, but RFQ and approval events need class 2 (4096 B sealed body) unless they get a denser encoding. That is about four times the padding cost per quote or approval, and it uses class-2 credits under the per-class quota. The design should decide this explicitly, either by accepting class 2 for those profiles or by defining a canonical compact binary encoding of the same closed profiles. It should not trim fields.

The contracts, credentials and ops categories have no runtime profile and stay mock-only. Live source authentication, real evidence and Registry-backed authority remain deployment gates. Nothing in the subscription layer supplies them.

## Rejected alternatives

- **Third pubsub protocol or broker (NATS JetStream, Kafka, Waku Filter/Light Push style servers).** Each needs server-side subject or content filters, which break the whole-shard privacy property. Pull and acknowledge patterns are adopted locally, not as a network service.
- **Waku content topics as subscription labels.** They are visible to relays and act as interest labels. Only the neutral static-shard naming idea is kept.
- **GossipSub Partial Messages.** A Working Draft not implemented in Rust. Group IDs and part metadata express correlation between pieces, which works against unlinkable fixed-size envelopes.
- **GossipSub v1.3 Extensions as a home for MPE metadata.** No extension is needed. Advertising MPE-specific extensions would fingerprint nodes.
- **Detection keys, bloom filters or other server-side recognition offload.** These hand interest information to a third party. Any such offload must be a labelled, weaker gateway profile.
- **A second Semaphore proof per event, or a semaphore-rs dependency.** This duplicates admission. The Rust port is at v0.1.0.
- **Sharing a SQLite file across processes or hosts.** WAL forbids network filesystems and allows one writer. One daemon owns the journal.
- **Selector-driven Store queries** ("give me my stream since T"). This leaks interest to Store operators. Fetch by shard window only.
- **Consumer acknowledgements propagated to relays or Stores.** These leak match/no-match and timing. Acknowledgements stay local.

## Proposed consensus decisions

- Keep GossipSub v1.2 on rust-libp2p 0.57 and libp2p-gossipsub 0.50 in anonymous validation mode. Track 0.51 to shrink the vendored patch. Do not adopt v1.3 extensions or Partial Messages.
- Add no new network protocol for subscriptions. Every subscription concept (watch, selector, cursor, acknowledgement, category) is local and has no wire form.
- Every receiving node or client ships a single-writer journal daemon that owns cursors and dispositions. SQLite is used for standalone nodes and clients; UmbraDB/PostgreSQL for backend hosts once the MPE capability lands.
- Intake is never gated by consumer demand. Consumer backpressure ends at the journal.
- Gaps are explicit, typed (transport, Store retention, local retention) and repaired only by whole-shard window fetches from at least two Stores.
- Admission verification uses a bounded window of finalized Registry roots, with the window length derived from the admission window, finality and propagation.
- Wallet connection, transport shard admission, local watch grant and action authority remain four separate checks (agreeing with sol-wallet and sol-contracts).
- The dashboard stays an unsigned, memory-only mock with the Moth connector limited to `connect` and `getConnectionStatus`. It is not production evidence.

## Unresolved objections

- **RLN relation fit.** Zerokit's leaf binds one `user_message_limit`. MPE needs per-class credit bounds in one proof. Multi-message-id (runtime in v3) could express class-weighted units, or the leaf could commit to a class vector, but neither has been checked against the MPE requirement register. Field, curve and hash compatibility with Midnight's proving system and Registry root hash is also unverified here. This blocks dependency acceptance; it does not block the subscription design.
- **Recognition cost at scale.** O(envelopes × stream keys) per recipient has not been measured at realistic shard rates. A principal with many streams on a busy shard may need more shards, not more keys.
- **RFQ and approval sizing** (class 1 against class 2), described above. This needs a product decision, not only an engineering one.
- **Store repair protocol.** The custom MPE store protocol is specified but not implemented. Whether negentropy-style reconciliation belongs in Store-to-Store repair, and with which Rust implementation, is open.
- **Shard participation visibility.** Subscribing to a shard topic is visible to peers. That is accepted in the README, but joining a shard on demand when a watch is created would turn it into an interest signal. Shard membership should follow transport policy, not watch creation. This needs agreement.
- **Status table staleness.** The libp2p implementation-status page may lag actual Rust v1.3 work. It is not used to justify any timeline.

## Limitations

- No code was run against live networks.
- No Zerokit, negentropy or recognition benchmark was performed.
- Version observations are point-in-time API listings.
- Model example sizes are a JSON approximation, not the sealed encoding.
- The experiments' figures are unreplicated single-machine observations, as their own README says.
- Visual grounding covers only the GossipSub implementation-status page. Every other row is text-grounded.

## Source URLs

- https://crates.io/api/v1/crates/libp2p-gossipsub
- https://api.github.com/repos/libp2p/rust-libp2p/releases?per_page=8 and `/commits?per_page=3`
- https://raw.githubusercontent.com/libp2p/rust-libp2p/master/protocols/gossipsub/CHANGELOG.md, `src/config.rs`, `src/protocol.rs`
- https://api.github.com/repos/libp2p/specs/contents/pubsub/gossipsub and `/commits?path=pubsub/gossipsub`
- https://raw.githubusercontent.com/libp2p/specs/master/pubsub/gossipsub/gossipsub-v1.2.md, `gossipsub-v1.3.md`, `partial-messages.md`, `implementation-status.md`
- https://github.com/libp2p/specs/blob/9e9628a4f9a2be2ac79f40a162cd978c5b200b03/pubsub/gossipsub/implementation-status.md (visual)
- https://api.github.com/repos/vacp2p/zerokit/releases?per_page=5; https://raw.githubusercontent.com/vacp2p/zerokit/master/rln/README.md
- https://raw.githubusercontent.com/waku-org/specs/master/standards/core/rln-contract.md, `relay-sharding.md`, `store-sync.md`; https://api.github.com/repos/waku-org/specs/contents/standards/core
- https://raw.githubusercontent.com/hoytech/negentropy/master/README.md; https://api.github.com/repos/hoytech/negentropy/commits?per_page=3
- https://api.github.com/repos/semaphore-protocol/semaphore/releases?per_page=5; https://api.github.com/repos/semaphore-protocol/semaphore-rs/commits?per_page=3
- https://api.github.com/repos/midnightntwrk/midnight-dapp-connector-api/releases?per_page=5 and `/commits?per_page=5`
- https://api.github.com/repos/shieldedtech/moth-wallet/commits?per_page=5
- https://api.github.com/repos/CharlesHoskinson/UmbraDB/commits?per_page=5
- https://www.sqlite.org/chronology.html; https://www.sqlite.org/wal.html
- Failed (404, not evidence): https://api.github.com/repos/vacp2p/rfc-index/git/trees/main?recursive=1, https://api.github.com/repos/vacp2p/rfc-index/contents/waku/standards/core, https://raw.githubusercontent.com/vacp2p/zerokit/master/CHANGELOG.md

Per-source metadata (requested and final URL, UTC retrieval time, status, raw and text SHA-256) is in the matching `.json` files under `../sources/opus-stack-feasibility/`.
