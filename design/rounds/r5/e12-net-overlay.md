# NET: GossipSub overlay and Midnight tether (MPE-NET)

## 1. Scope of this area

This area covers decision D8. It specifies how Envelopes move between Bus Nodes: the sidecar process boundary, the GossipSub v1.1 router configuration (signature policy, message ids, mesh degree, timing, flood publishing, validation outcomes and scoring), peer discovery and bootstrapping, transports, shard topics, and the publish ingress hop. It also specifies the Ledger Adapter (how a Bus Node reads the Registry and when its chain view counts as stale), the Registry and Anchor interface as the overlay sees it, the fallback paths, and what MPE requires to change in `midnight-node`, the Indexer, Compact and the wallet. The required answer to that last question is "nothing". Envelope layout belongs to FMT, admission cryptography to ECO and CRY, load and latency targets to PRF, and retention to STO.

## 2. Parameters

| ID | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-NET-1 | GossipSub mesh degree `D` | 8 | 6–12 | g2 D5; `2020-vyzovitis-gossipsub` (evaluated profile, lines confirmed by o1 R2); rust default is 6 (`rust-libp2p/protocols/gossipsub/src/config.rs:83`). DEC-NET-3 |
| P-NET-2 | `D_lo` | 6 | 4 to P-NET-1 | g2 D5; rust default 5 (`config.rs:84`) |
| P-NET-3 | `D_hi` | 12 | P-NET-1 to 16 (upper bound is an **assumption**) | g2 D5; `specs/pubsub/gossipsub/gossipsub-v1.0.md:197` |
| P-NET-4 | `D_out` (outbound mesh quota) | 4 | 1 to min(P-NET-2 − 1, ⌊P-NET-1/2⌋) | g2 D5; `specs/pubsub/gossipsub/gossipsub-v1.1.md:192-193,552`; o1 R2 confirms the 1–4 range for `D` = 8 |
| P-NET-5 | Heartbeat interval | 1 s | 0.5–2 s (**assumption**) | `2020-vyzovitis-gossipsub`; `config.rs:521` |
| P-NET-6 | Gossip factor | 0.25 | 0.25–0.4 | `gossipsub-v1.1.md:177`; g2 D5 (0.4 is the first knob to turn) |
| P-NET-7 | Prune backoff | 60 s | 60–300 s (**assumption**) | g2 D5; `config.rs:545` |
| P-NET-8 | Largest GossipSub RPC accepted | 65,536 bytes | from the largest FMT class wire size up to 262,144 bytes | `rust-libp2p/.../protocol.rs:100`; g2 D1 (256 KiB ceiling) |
| P-NET-9 | Shard count | 1 | 1–8 | g1 D3; s1, s2, s3, s4 (one topic); g2, g3 (≤ 8). DEC-NET-4 |
| P-NET-10 | Per-peer Envelope rate before verification | 20 Envelopes/s | 5–100 (**assumption**) | g2 D4 |
| P-NET-11 | Minimum published bootstrappers | 4 | ≥ 4 | g2 D7 |
| P-NET-12 | Warm-up before local injection | 600 s | 0–900 s | g2 D9; Vyzovitis recovery of about 90 heartbeats (g2 D9) |
| P-NET-13 | Tolerated difference between local clock and latest finalized block timestamp | 120 s | 30–300 s | g1 D1; finality of about 18 s ([doc] `mps-0028` via notes §1.7) |
| P-NET-14 | Independent chain sources per Ledger Adapter | 2 | 1 (POC) to 5 | o1 R2 D8; o3 D9; s3 D8 |
| P-NET-15 | IP-colocation (P6) threshold | 10 | 1–10 | crate default, not tuned (`peer_score/params.rs:171`); `gossipsub-v1.1.md:322` |
| P-NET-16 | Heartbeats within which a continuously misbehaving mesh peer is pruned | 90 | 30–300 (**assumption**, derived from the recovery time g2 cites) | `2022-kumar-gossipsub-formal`; g2 D9 |
| P-NET-17 | Anchor window | 60 s | 60–300 s | o1 D3, D10 (fallback to 5 min) |
| P-NET-18 | IDONTWANT message-size threshold | 1,000 bytes | 0 to P-NET-8 | `config.rs:563`; `gossipsub-v1.2.md:71-75` |

## 3. Requirements

### MPE-NET-001 Sidecar process
The Bus Node shall run as a process separate from `midnight-node` and shall link no code into the node binary.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1, g2, g3, o1, o2, o4, s1, s2, s3, s4; notes §8; `midnight-node/Cargo.lock` (no `libp2p-gossipsub`; `sc-network-gossip` at :14548)
- Rationale: The node has no GossipSub and no plugin slot. A protocol inside the node would be a fork that every relaying operator has to run.
- Verify: inspection. The Prototype is its own binary, and the `midnight-node` dependency tree is unchanged.
- Status: settled

### MPE-NET-002 Overlay at launch
MPE shall carry Envelopes over the GossipSub overlay from the first release phase.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1, g2, g3, o1, o2, o4, s1, s2, s3, s4 (overlay first); o3 (ledger first); g4 (ledger only); `ledger-parameters-config.json:158`; `runtime/src/lib.rs:292`
- Rationale: The ledger lane is public, carries bodies of about 256 bytes, waits for finality and shares 1,000,000 block-usage bytes per 6 s slot.
- Verify: demonstration. The Prototype delivers Envelopes with no Midnight transaction per Envelope.
- Status: open (DEC-NET-1)

### MPE-NET-003 No node change
MPE shall operate with an unmodified `midnight-node` binary, runtime and pallet set.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D8; all twelve proposals; notes §8 (the P2P registry needs a custom binary; new pallets need a governance runtime upgrade)
- Rationale: Keeps bus incidents off chain levers and avoids a runtime upgrade (o4 D8).
- Verify: inspection. The Prototype runs against a stock local devnet node.
- Status: settled

### MPE-NET-004 Validators not required
MPE shall deliver Envelopes with no Bus Node running on any Midnight block-authoring host.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D8, D7; g1, g2, g3, o1, s1–s4; `midnight-node/node/src/service.rs:610-619`; `2024-heimbach-deanon`
- Rationale: Event work competes with authoring CPU, which is the reason the node already refuses ledger-sync serving on validators. Putting events on validators would also expose the consensus graph.
- Verify: test (g2 D10). On a devnet, a capture on validator P2P ports shows zero MPE protocol ids, and stopping all Bus Nodes leaves GRANDPA finality unchanged.
- Status: settled

### MPE-NET-005 Distinct peer identity
The Bus Node shall use a libp2p identity key distinct from the network key of any Midnight node on the same host.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D8; g2 D7
- Rationale: A shared key would link event-mesh identity to chain identity.
- Verify: test. The Prototype refuses to start when given the co-located node's network key file.
- Status: settled

### MPE-NET-006 Network-scoped names
The Bus Node shall derive every protocol id and topic name from the Midnight genesis hash and the MPE major version.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D1 (`/midnight-pe/1`); g3 D8; notes §1.2 (Substrate protocol names embed the genesis hash)
- Rationale: Keeps testnet and mainnet meshes apart, and lets a new layout run as a separate mesh.
- Verify: test. Two swarms with different genesis hashes share a bootstrapper, and no Envelope crosses between them.
- Status: settled

### MPE-NET-007 Transport baseline
The Bus Node shall support TCP with Noise encryption and Yamux multiplexing as its mandatory transport stack.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g2 D8 (QUIC optional); notes §1.1; o1 R2 and o2 R2 (the sidecar's Yamux is independent of the node's patched Yamux)
- Rationale: A common baseline for interoperability. QUIC can be added without being required.
- Verify: test. Two Prototype nodes built with only TCP, Noise and Yamux exchange Envelopes.
- Status: settled

### MPE-NET-008 GossipSub v1.1 with scoring
The Bus Node shall relay Envelopes using a GossipSub v1.1 router with peer scoring enabled.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8 (decided); g2; `gossipsub-v1.1.md`; `rust-libp2p/.../behaviour.rs:1051` (`with_peer_score`)
- Rationale: Scoring, outbound quotas and opportunistic grafting are the v1.1 defences for keeping messages flowing. They are not anonymity mechanisms (s1, s2).
- Verify: inspection of the configuration, plus a test that per-peer scores appear in metrics.
- Status: settled

### MPE-NET-009 StrictNoSign policy
The Bus Node shall run GossipSub under the StrictNoSign policy and shall reject any message carrying `from`, `seqno`, `signature` or `key`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D1; g2 D1; s2 D8; s3 D8; `specs/pubsub/README.md:272-321`; `rust-libp2p/.../protocol.rs:421-442` (`ValidationMode::Anonymous`); `CHANGELOG.md:1-4` (the `key` rejection arrived in 0.51.0)
- Rationale: Removes the peer-id author stamp from the gossip layer. Publisher authentication lives inside the seal (CRY).
- Verify: test. An injected message carrying any one of the four fields is dropped and lowers the sender's P4 score.
- Status: settled

### MPE-NET-010 Content-addressed message id
The Bus Node shall set the GossipSub message id to the FMT Envelope identifier computed over the received Envelope bytes.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D1; g1 D1; g2 D1; `README.md:317-318`; `rust-libp2p/.../config.rs:526-539`
- Rationale: The crate's default id is source plus seqno. Under StrictNoSign both are absent, so every message would get the same id and be dropped as a duplicate.
- Verify: test. 1,000 distinct Envelopes from one client are all delivered; resending identical bytes delivers once.
- Status: settled

### MPE-NET-011 Mesh degree
The Bus Node shall set `D`, `D_lo`, `D_hi` and `D_out` to P-NET-1, P-NET-2, P-NET-3 and P-NET-4.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D5; g2; g1, g3 (D = 6); `gossipsub-v1.1.md:192-193`; `config.rs:1125-1129`
- Rationale: These are the parameters actually evaluated. The crate accepts `D_out` = `D_lo`, while the spec requires `D_out` < `D_lo`; P-NET-4 follows the spec.
- Verify: inspection of the configuration dump, plus a test that a configuration with `D_out` ≥ `D_lo` fails at startup.
- Status: open (DEC-NET-3)

### MPE-NET-012 Timing parameters
The Bus Node shall set the heartbeat interval, gossip factor and prune backoff to P-NET-5, P-NET-6 and P-NET-7.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D8, D5; g2 D5; `gossipsub-v1.1.md:177`; `config.rs:519-545`
- Rationale: These match the profile tested under Sybil cold start in `2020-vyzovitis-gossipsub`.
- Verify: inspection of the configuration dump.
- Status: open (DEC-NET-3)

### MPE-NET-013 Flood publishing off
The Bus Node shall disable GossipSub flood publishing on every MPE topic.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D3; g1 D5; g2 D3; s3 D8; g3 R2; `gossipsub-v1.1.md:145-158,549` (default on); `config.rs:548`; `2017-fanti-anonymitybitcoin`
- Rationale: Flooding a node's own messages hands their origin to every neighbour and multiplies egress. The eclipse resistance lost by turning it off is covered by `D_out`.
- Verify: test. A node with 30 connected peers sends a fresh Envelope to at most P-NET-3 first-hop peers.
- Status: settled

### MPE-NET-014 RPC size cap
If a received GossipSub RPC exceeds P-NET-8 bytes, then the Bus Node shall drop it without forwarding.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8, D1; g1 D1; g2 D1 (refuses 1 MiB mesh messages; `2025-farooq-staggering`); `protocol.rs:100,379`
- Rationale: Bounds per-message amplification and memory.
- Verify: test. An RPC of P-NET-8 + 1 bytes is neither delivered nor forwarded.
- Status: settled

### MPE-NET-015 Validate before forwarding
The Bus Node shall forward an Envelope only after its application validator has returned Accept.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D1; g2 D1; `config.rs:525` (`validate_messages` defaults to false); `behaviour.rs:949`
- Rationale: With the crate default, messages are forwarded before admission is checked.
- Verify: test. An Envelope held in validation is not seen by any downstream peer until Accept.
- Status: settled

### MPE-NET-016 Reject outcome
If an Envelope fails a layout or admission check that does not depend on chain state, then the Bus Node shall return Reject.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8, D9; g1 D1; g2 D1; `gossipsub-v1.1.md:535`
- Rationale: Reject applies the P4 penalty, so peers that forward invalid traffic lose score.
- Verify: test. Every entry of the FMT mutated-header list gets Reject, and the sender's P4 term falls.
- Status: settled

### MPE-NET-017 Ignore outcome
If an Envelope is a duplicate, is expired on arrival, or carries an unknown version, then the Bus Node shall return Ignore.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8; g1 D1; g2 D1; `gossipsub-v1.1.md:536`
- Rationale: These are not proof of a faulty peer. Penalising them would split the mesh during upgrades.
- Verify: test. Each case is neither forwarded nor penalised.
- Status: settled

### MPE-NET-018 Stale chain view yields Ignore
While the Ledger Adapter view is stale, the Bus Node shall return Ignore for every Envelope whose admission check depends on chain state.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D8, D9; o1 R2 D9(d); g1 D1
- Rationale: A lagging or eclipsed chain source must not lead honest relays to graylist honest forwarders under P4.
- Verify: test. Freeze the mock adapter; valid Envelopes cause no P4 change and no graylisting.
- Status: settled

### MPE-NET-019 Clock and stall detection
If the local clock and the latest finalized block timestamp differ by more than P-NET-13 seconds, then the Ledger Adapter shall mark its view stale.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8; g1 D1; o1 R2 D8(d) (an indexer can withhold); notes §4.1
- Rationale: One check covers a stalled source, a withholding source and a wrong local clock.
- Verify: test. Pause the mock chain, or shift the local clock by P-NET-13 + 1 s; the view becomes stale.
- Status: settled

### MPE-NET-020 Source disagreement
If two configured chain sources report different Registry admission roots for the same finalized block, then the Ledger Adapter shall mark its view stale.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D8, D9; o1 R2 D8; o3 D9 (cross-checked indexers); s3 D8 (independently checked chain access); g1 D6
- Rationale: Detects an Indexer or RPC operator that lies about admission state.
- Verify: test. Two mock sources diverge at one height; the view becomes stale and an alarm metric is raised.
- Status: settled

### MPE-NET-021 Score penalty signs
The Bus Node shall configure negative weights for the invalid-message (P4) and IP-colocation (P6) score terms, with P6 threshold P-NET-15.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D9; `gossipsub-v1.1.md:322,585`; `peer_score/params.rs:171,206`
- Rationale: These penalise invalid forwarding and Sybils placed on one IP address.
- Verify: test. P-NET-15 + 2 peers on one IP all get a negative P6 contribution.
- Status: settled

### MPE-NET-022 Eviction of misbehaving peers
When a mesh peer has delivered only Rejected Envelopes or no first deliveries for P-NET-16 consecutive heartbeats, the Bus Node shall prune that peer from its mesh.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D9; `2022-kumar-gossipsub-formal` §§1, 3–5 (s4 R2: under some configurations, continuous withholding keeps a positive score); `2023-kumar-gossipsub-acl2s` (CVE-2022-47547)
- Rationale: The CVE comes from the parameter set, so the property has to be checked on MPE's own parameters.
- Verify: simulation with withholding and invalid-only peers; each is pruned within P-NET-16 heartbeats.
- Status: settled

### MPE-NET-023 Per-peer rate limit
If a peer sends more than P-NET-10 Envelopes per second, then the Bus Node shall drop the excess before signature or proof verification.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D4; s3 D9 (proof-verification flood is rank 6); g3 D9
- Rationale: Stops one neighbour from spending the relay's verification budget.
- Verify: test. At 5× P-NET-10 from one peer, the verifier invocation count stays at or below P-NET-10 per second for that peer.
- Status: settled

### MPE-NET-024 Bootstrapper mode
Where a Bus Node runs as a bootstrapper, it shall set `D`, `D_lo`, `D_hi` and `D_out` to zero with Peer Exchange enabled.
- Pattern: optional
- Scope: POC
- Priority: SHOULD
- Source: D8, D7; `gossipsub-v1.1.md:656-660`; g2 D4, D8; o1 R2 D7; `config.rs:541` (`do_px` defaults to false)
- Rationale: Bootstrappers introduce peers without becoming mesh members.
- Verify: test. A bootstrapper forwards no Envelopes and returns peer records on PRUNE.
- Status: settled

### MPE-NET-025 Bootstrapper set
MPE shall publish at least P-NET-11 bootstrappers, each run by a distinct Operator on a host that is not a Midnight chain bootnode.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D8, D7; g2 D7, D8; notes §1.3 (four DNS bootnodes); `2018-marcus-ethereumeclipse` (via g2)
- Rationale: Keeps the event and chain peer sets apart, so that one seizure or eclipse does not hit both, and avoids a single seeder lever.
- Verify: inspection of the published list against Operator records and `res/mainnet/bootnodes-config.json`.
- Status: settled

### MPE-NET-026 Bootstrap list authenticity
When the Bus Node loads a bootstrap list, it shall verify the list hash against the bootstrap-list hash in the Registry.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D8; g2 D7; o1 D7; `rust-libp2p/.../types.rs:266,517` (Peer Exchange carries no signed peer record)
- Rationale: Peer Exchange records are not authenticated in the chosen crate, so the list is the trust anchor.
- Verify: test. A list with one substituted address is refused and not dialed.
- Status: settled

### MPE-NET-027 Peer Exchange acceptance
The Bus Node shall accept Peer Exchange records only from peers whose score reaches `AcceptPXThreshold`, a value attainable only through the bootstrapper application score.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D8; `gossipsub-v1.1.md:238-240,659-660`; `behaviour.rs:1106` (`set_application_score`)
- Rationale: Stops Sybil mesh peers from steering new connections.
- Verify: test. Peer Exchange from a high-scoring non-bootstrapper is ignored.
- Status: settled

### MPE-NET-028 Outbound quota sources
The Bus Node shall fill its `D_out` quota only with peers it dialed from the bootstrap list, bootstrapper Peer Exchange or the Registry relay list.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D9; g2 D8, D10; `2015-heilman-eclipse`; `2022-prunster-ipfseclipse`
- Rationale: DHT tables have been cheaply eclipsed. DHT-supplied peers must not own the outbound quota.
- Verify: test. With a DHT full of attacker ids, every `D_out` slot holds a non-DHT peer.
- Status: settled

### MPE-NET-029 No local-network discovery
While running outside a development profile, the Bus Node shall not discover or dial peers on private, link-local or loopback addresses.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D8; g2 D7 (mDNS off; `--no-private-ip` posture); notes §1.3
- Rationale: Copies the chain operator posture and removes mDNS as a source of peer injection.
- Verify: test. Production profile: no mDNS traffic, and private-address dials are refused.
- Status: settled

### MPE-NET-030 Warm-up before injection
While the Bus Node has not held at least `D_out` outbound mesh peers continuously for P-NET-12 seconds, it shall refuse local client publications with a not-ready error.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: D8, D9; g2 D9 (cold-boot and covert flash); `2020-vyzovitis-gossipsub`
- Rationale: A freshly booted node may sit in a Sybil-heavy mesh.
- Verify: test. A publication during warm-up returns not-ready and is not injected.
- Status: settled

### MPE-NET-031 Shard topics from the Registry
The Bus Node shall subscribe to the shard topics defined by the shard count P-NET-9 read from the Registry.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8, D3; g1 D3; s1, s2, s3, s4; g2, g3, o4 (8); o1, o2 (16)
- Rationale: Each split divides the anonymity set (g3 D5; o2 R2 D3).
- Verify: test. Changing the mock Registry value changes the subscribed topic set.
- Status: open (DEC-NET-4)

### MPE-NET-032 Shard-count transition
When the Registry shard count changes, the Bus Node shall keep relaying the previous shard topics until the maximum Envelope lifetime has elapsed after the activation height.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D8, D3; g1 D3
- Rationale: Envelopes already in flight keep their old mapping until they expire.
- Verify: test. An Envelope published under the old mapping just before activation is still delivered.
- Status: settled

### MPE-NET-033 Publish ingress hop
When the MPE client library publishes an Envelope, it shall send it to exactly one Bus Node chosen at random from at least two Bus Nodes the client dialed itself.
- Pattern: event
- Scope: POC
- Priority: SHOULD
- Source: D8, D3; g2 D3 (one-hop outbound stem); g3 D3; g1 D1 (two hops); o1, o2 (Dandelion++); s3 D8
- Rationale: Hides the source from peers other than the chosen node. No Dandelion++ bound is claimed (s1 R2, s4 R2; `2018-fanti-dandelionpp` §3.1).
- Verify: test. Across 1,000 publications, each one reaches exactly one first Bus Node, and the choice spans at least two nodes.
- Status: open (DEC-NET-6)

### MPE-NET-034 Relay allow-list
Where the relay allow-list is enabled, the Bus Node shall exclude from its mesh every peer whose identity is absent from the Registry relay list.
- Pattern: optional
- Scope: POC
- Priority: SHOULD
- Source: D8, D7; g1 D7; o1 R2 D7(d); s3 D7; g2, g3 (open, kept in the mesh by score)
- Rationale: Permissioned launch until a red-team fails to capture the mesh.
- Verify: test. GRAFT from an unlisted peer is refused, and that peer never enters any mesh.
- Status: open (DEC-NET-7)

### MPE-NET-035 Ledger Adapter interface
The Ledger Adapter shall expose finalized Registry reads and Midnight transaction submission through one interface that has a mock implementation.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; brief glossary; o1 D7 (RPC or Indexer reads, normal submission); g3 D8 (`send_mn_transaction`)
- Rationale: The Prototype must run without a live ledger-9 network.
- Verify: test. The full Prototype suite passes against the mock adapter, and a subset passes against a devnet adapter.
- Status: settled

### MPE-NET-036 Finalized state only
The Ledger Adapter shall return Registry state only from finalized blocks.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D3 (relays must not accept mempool state); `midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128-181`
- Rationale: The Registry view stays consistent with the Indexer, and a reorg cannot revoke an accepted admission.
- Verify: test. A Registry write that is included but not finalized is invisible to the adapter.
- Status: settled

### MPE-NET-037 Contract-state read path
The Ledger Adapter shall obtain admission roots and network parameters from Registry contract state without depending on `contractEvents`.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g3 D4, D8; o2 D8; o1 R2 finding 1 (`midnight-node/ledger/src/ledger_9/mod.rs:460-470`); `midnight-docs/docs/concepts/how-midnight-works/building-blocks.mdx:79-83`; `toolchain-0.33.0.md:10-12`; notes §3.3, §4.7
- Rationale: Public networks run ledger 8, the node discards logs, and `contractEvents` is `@beta` with no capacity benchmark.
- Verify: demonstration. The adapter reads a root via `midnight_contractState` on a ledger-8 devnet.
- Status: open (DEC-NET-5)

### MPE-NET-038 Relaying during a governance pause
While safe mode filters Midnight user transactions, the Bus Node shall keep relaying Envelopes admitted under previously accepted Registry roots until those admissions expire.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D8, D9; g1 D7; g3 D9; o4 R2 D8; `midnight-node/runtime/src/check_call_filter.rs:44-45`
- Rationale: A chain pause stops new enrolment. It should not delete the bus.
- Verify: test. With safe mode entered on a devnet, existing admissions deliver and new registrations fail.
- Status: settled

### MPE-NET-039 Registry fields
The Registry shall expose as public ledger state the shard count, its activation height, the maximum MPE protocol version, the current admission root and the bootstrap-list hash.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D6 (`shard_count`, `pe_version_max`); g2 D7; g3 D8 (root cell); o1 D3
- Rationale: These are the only chain facts the overlay needs. ECO defines the root format.
- Verify: inspection of the contract, plus a test that the adapter reads each field.
- Status: settled

### MPE-NET-040 Fixed `Misc` names
The Registry shall emit only `Misc` events whose `name` is a fixed MPE protocol constant.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D8, D1; o1 D1; g4 D1; `minokawa-compact/compiler/midnight-events.ss:71-74`; `schema-v4.graphql:1125-1165` (via o1)
- Rationale: The Indexer exposes `name` in clear. A topic placed there leaks interest.
- Verify: inspection of every `emit` site, plus a test over 100 emits showing one distinct `name` per event kind.
- Status: settled

### MPE-NET-041 Anchor cadence
Where a Bus Node acts as anchorer, it shall submit at most one Anchor per shard per non-empty P-NET-17 window, carrying that window's batch root and Envelope count.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D8, D6; o1 D3, D4; o2 D6; o4 D4; g3 D4 (empty shards not anchored); g2 D8
- Rationale: The count lets clients detect withheld traffic; empty windows cost nothing.
- Verify: test. Ten windows, three of them empty, produce seven Anchors with correct counts.
- Status: settled

### MPE-NET-042 Explicit fallback label
When the MPE client library carries an Event over a fallback path, it shall label that Event with the fallback mode it used for the Consumer.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D8; s1 R2 D8; s3 D9 (blocks silent fallback); o3 D8 (labels)
- Rationale: A fallback with different leakage cannot inherit the overlay's privacy label.
- Verify: test. With the overlay disabled, every delivered Event carries a non-overlay label.
- Status: settled

### MPE-NET-043 Gateway fallback
Where the gateway fallback is enabled, the Bus Node shall serve the complete Envelope stream of a shard in overlay framing and shall accept no topic or Tag filter.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D8; s1 D8; s2 D8; s4 D8; o1 R2 D8 (first fallback)
- Rationale: Keeps the whole-feed interest property while concentrating ingress on fewer operators (g1 R2).
- Verify: test. The byte streams from the overlay and the gateway match, and a filter parameter is rejected.
- Status: open (DEC-NET-2)

### MPE-NET-044 Ledger fallback
Where the ledger fallback is enabled, the MPE client library shall publish each fallback Event as one `Misc` under a name shared by all MPE fallback publications.
- Pattern: optional
- Scope: PROD
- Priority: MAY
- Source: D8; g2 D8; o2 D8; o4 D8; s3 D8; g4 D1; s4 R2 (rotating names change leakage)
- Rationale: A public, ledger-9-only escape channel. Per-topic names would expose interest.
- Verify: test on a ledger-9 devnet: fallback publications show one `name` and a payload of at most 256 bytes.
- Status: open (DEC-NET-2)

### MPE-NET-045 Unmodified Indexer
The Indexer adapter shall use only queries and subscriptions present in the unmodified Indexer `schema-v4` API.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1 D8; g3 D8; o1 D8 (U4 optional); o4 D8; `schema-v4.graphql:548-562`
- Rationale: No Indexer change is required. A `Misc` name filter is only a nice-to-have.
- Verify: inspection. Every GraphQL operation in the adapter validates against `schema-v4.graphql`.
- Status: settled

### MPE-NET-046 Unmodified Compact toolchain
The Prototype shall build its Registry contract with an unmodified released Compact toolchain.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D8; g1, g2, g3, o1, o4 (no compiler change); `toolchain-0.33.0.md:10-12`
- Rationale: The Registry uses existing ledger types and `Misc`. The U2 size-limit fix is a request, not a dependency.
- Verify: inspection. The build log names a released toolchain version with no patches.
- Status: settled

### MPE-NET-047 IDONTWANT measurement
The Prototype shall report per-node bytes sent with GossipSub v1.2 IDONTWANT enabled at threshold P-NET-18 and with IDONTWANT disabled.
- Pattern: ubiquitous
- Scope: POC
- Priority: SHOULD
- Source: D8, D5; g2 D5; o1 D10; g3 R2; `CHANGELOG.md:163-166`; `gossipsub-v1.2.md:71-72`
- Rationale: The crate supports IDONTWANT, but capacity planning takes no credit until the saving is measured, and small messages may lose.
- Verify: test. Paired runs report the egress difference per size class.
- Status: settled

## 4. Decisions

**DEC-NET-1. Launch tether order.**
- Options:
  - (a) Overlay from phase 1, with the ledger used for membership and anchors: g1, g2, g3, o1, o2, o4, s1, s2, s3, s4.
  - (b) Ledger and Indexer first, overlay in phase 2: o3. o4 R2 also asks for g4's ledger mode as phase 1.
  - (c) Ledger and Indexer only: g4.
- Recommended default: (a).
- Reason: Ten of twelve proposals choose it. Preview, Preprod and Mainnet run ledger 8 (`building-blocks.mdx:81-82`), so (b) and (c) have no public network until ledger 9 activates, while (a) with MPE-NET-037 runs on ledger 8.
- Strongest objection (g2 R2, o3 R2): if a product accepts about 1 event/s and about 1 minute of delay, the Indexer lane needs no second network, and the overlay adds an unfunded Sybil set.
- Settling check: the ledger-9 mainnet date compared with the phase-1 date; a written product need for latency under one slot or bodies over 205 bytes (g4 T1); the Prototype meets delivery ≥ 99% with p99 ≤ 6 s at N = 200 (g2).

**DEC-NET-2. Fallback.**
- Options:
  - (a) Replicated whole-feed gateways using the same framing: s1, s2, s4, and o1 R2 as its first fallback.
  - (b) `Misc` plus `contractEvents`: g2, o2, o4, s3; o1 R2 keeps it only as a last resort.
  - (c) A default-off Substrate notification protocol on non-validators: g1, g3.
  - (d) A self-run Indexer with no overlay: g4.
- Recommended default: (a) first and (b) as a labelled last resort (MPE-NET-042); (c) is rejected.
- Reason: (a) keeps the interest property. (b) depends on ledger 9 and is public and permanent. (c) is a fork that operators would run unpaid (o2 R2), although only participating operators would need it (s4 R2).
- Settling check: the Prototype switches from overlay to gateway behind the same Subscriber API, and PRV signs the leakage note.

**DEC-NET-3. Mesh profile.**
- Options:
  - (a) `D` 8 / 6 / 12, `D_out` 4, heartbeat 1 s, gossip factor 0.25: g2, and o1 R2 votes for this method.
  - (b) `D` 6, `D_out` 2, `D_lo`/`D_hi` from the crate (5/12): g1, g3, o1 R1, s2; `2024-revuelta-waku-latency` measured D = 6 at under 1 s for messages of 25 KB or less.
- Recommended default: (a).
- Reason: (a) is the evaluated attack-resilient profile, and `D_out` = 4 maximises protection against an eclipse that needs every outbound slot (`2015-heilman-eclipse`). The cost is an egress multiplier of 7 instead of 5.
- Settling check: PRF/VER simulation of both profiles at 50, 200 and 1,000 nodes with a 20% Sybil cold start. Choose the cheaper profile that meets the targets; if scoring is unstable, set `D_out` to 2.

**DEC-NET-4. Launch shard count.**
- Options:
  - (a) One topic: g1, s1, s2, s3, s4.
  - (b) Up to 8 shards: g2, g3, o4.
  - (c) 16 buckets: o1, o2.
- Recommended default: (a), with a shard field reserved in the Envelope (FMT).
- Reason: Shards cut the anonymity set, and `H(contract) mod 8` exposes per-contract volume (o2 R2).
- Settling check: split only after one shard exceeds the PRF per-shard cap for 7 days (g1 D3, g3 D7).

**DEC-NET-5. Admission read path.**
- Options:
  - (a) Contract-state roots: g3, o2, o1 (`HistoricMerkleTree` roots).
  - (b) Per-ticket `Misc` events through `contractEvents`: g1.
  - (c) A standalone re-executing Indexer per operator: o1 R2, g1 D6.
- Recommended default: (a).
- Reason: The node discards logs, `contractEvents` is beta, and the networks are on ledger 8. Under MIP-0002's reading, g1's per-ticket events at 50/s may exceed `bytesWritten` (o1 R2); that is **unknown**.
- Settling check: read roots on a ledger-8 devnet; on ledger 9, measure read latency for (a) and (b).

**DEC-NET-6. Publish ingress.**
- Options:
  - (a) A one-hop outbound stem: g2, g3.
  - (b) A two-hop stem: g1.
  - (c) Dandelion++: o1, o2.
  - (d) Mix ingress, later: s3.
  - s1 and s4 claim no anonymity from either mechanism.
- Recommended default: (a), with no privacy claim.
- Reason: It is the simplest option and adds about one link latency (g2 D5). The Dandelion++ bound does not transfer to these meshes (g1 R2, s1 R2, s4 R2).
- Settling check: a VER spy run with 10% of relays logging first-seen peers, comparing the first-spy precision of (a), (b) and direct publishing. Keep the stem only if it measurably lowers precision.

**DEC-NET-7. Relay admission at launch.**
- Options:
  - (a) A Registry allow-list until a red-team fails to capture the mesh: g1, s3, o1 R2.
  - (b) Open relaying kept in check by score: g2, g3, o1 R1.
- Recommended default: (a) at production launch; the Prototype supports both.
- Reason: Scoring does not create independent operators (s1 R2), and the scoring audit asked for more simulation (`2020-leastauthority-gossipsub-audit`). OPS owns the policy.
- Settling check: a red-team holding as many peer ids as the honest set (g1 D10).

## 5. Cross-area dependencies

- **FMT:** the Envelope identifier definition (used by MPE-NET-010); the largest class wire size (P-NET-8); the version field and unknown-version rule (MPE-NET-017); the expiry field; the reserved shard field (DEC-NET-4).
- **ECO:** the admission-root format and per-Envelope admission check; which admission failures depend on chain state (MPE-NET-016, MPE-NET-018); the admission epoch length (MPE-NET-038).
- **CRY:** domain separation for identifiers and topic-name derivation (MPE-NET-006).
- **PRF:** load profiles, latency SLOs and per-shard caps (DEC-NET-3, DEC-NET-4); amplification targets (MPE-NET-047).
- **STO:** seen-set retention behind Ignore (MPE-NET-017); Store Node back-fill; Anchor durability (MPE-NET-041).
- **PUB:** shard mapping; the full-feed stream protocol and its per-node cap; retry after ingress failure (MPE-NET-033).
- **CON:** delivery labels (MPE-NET-042); contract consumption of Anchors.
- **PRV:** the non-claims attached to MPE-NET-013 and MPE-NET-033; the leakage of each fallback (DEC-NET-2).
- **SEC:** targeted eclipse and Sybil tests (MPE-NET-022, MPE-NET-028); bounded validation queues.
- **OPS:** relay admission policy (DEC-NET-7); bootstrapper Operators (MPE-NET-025); Registry governance for shard-count and list-hash writes.
- **VER:** the 50/200/1,000-node harness, stop conditions and spy runs (DEC-NET-1, DEC-NET-3, DEC-NET-6).

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Bootstrapper | A Bus Node with mesh degree 0 that serves only Peer Exchange |
| Outbound peer | A peer that the Bus Node dialed itself |
| Stale chain view | Ledger Adapter state entered under MPE-NET-019 or MPE-NET-020 |
| Gateway | A Bus Node role in the fallback that serves the complete Envelope stream |
| Anchorer | A party that submits Anchors to the Registry |
| Registry relay list | The peer ids allowed in meshes when the allow-list is enabled |
| Mesh profile | The parameter set P-NET-1 to P-NET-7 |

## 7. Gaps

1. **Score weights.** The v1.1 spec leaves weights to the application, and no proposal gives them. Only the eviction property (MPE-NET-022) is testable.
2. **CVE-2022-47547.** `rust-libp2p/protocols/gossipsub/CHANGELOG.md` has no entry naming it, and go-libp2p-pubsub was not checked. Whether it is fixed is **unknown**, so g2's "changelog names a fix" gate is replaced by MPE-NET-022.
3. **AS-level eclipse.** g2 and s3 name it as a residual, and `2018-fanti-dandelionpp` §3.1 places it out of scope. No defence for it is testable here.
4. **Upstream register.** o1's U0 (ledger-9 activation), U2 (log-size alignment), U7 (`contractEvents` GA and a capacity benchmark) and the packaging of a standalone Indexer belong to Midnight teams, not MPE. U0 still gates Anchors and contract consumption.
5. **Node-protocol fallback.** This is g1's and g3's option. It is not written because it is a fork and no operator constraint against running a second process is in evidence.
6. **First bootstrap trust.** The Registry hash catches a substituted list only after the node has chain access. The first list a user receives remains a trust point (g2 D9).
7. **Censorship of Registry writes by the ten permissioned validators.** This is inherited from the chain. MPE-NET-038 covers only continued relaying during a pause.
8. **Node peer limits.** The upstream defaults of 8 outbound and 32 inbound are unverified on the pinned fork (notes §0.1). They do not affect a sidecar.
