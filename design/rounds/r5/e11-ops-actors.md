# MPE-OPS: Infrastructure actors, governance and operations

## 1. Scope of this area

This area covers decisions D7 and D10. It sets out who runs Bus Nodes, Store Nodes, anchorers, bootstrappers and monitors; how they are admitted and what they are trusted with; and how governance acts and where its power stops. It also covers upgrades, key rotation, monitoring, incident response and abuse handling. None of these may need anyone to read Event content. The area ends with the gated launch phases. Payment amounts and admission cryptography belong to the economics area (D4). Mesh parameters belong to the network area (D5/D8). This area states only the operational gates that depend on them.

Midnight facts this area relies on:
- Mainnet genesis has 10 permissioned validator seats and 0 registered seats (`midnight-node/res/mainnet/system-parameters-config.json:6-9`).
- Safe mode deliberately filters user transactions (`midnight-node/runtime/src/check_call_filter.rs:44-45`; `runtime/src/lib.rs:321`). A forced safe mode lasts 7 days (`lib.rs:758`).
- Preview, Preprod and Mainnet run ledger 8 (`midnight-docs/docs/concepts/how-midnight-works/building-blocks.mdx:79-83`). Ledger 9 "will be, but is not yet, deployed" (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:12`).

## 2. Parameters

| ID | Meaning | Default | Allowed range | Source |
|---|---|---|---|---|
| P-OPS-1 | Minimum number of independent organizations running listed relays | 8 | 5–16 | s1 D7 (16 relays, ≥ 8 orgs); o4 R2 amendment; s2, s4 propose 5 |
| P-OPS-2 | Maximum share of listed relays run by one organization | 20 % | 10–33 % | o4 D10 P3 gate |
| P-OPS-3 | Minimum number of MPE bootstrappers | 4 | 3–8 | g2 D7 |
| P-OPS-4 | Sybil peer identities held by the allow-list red-team | 1 × honest relay count | ≥ 1 × | g1 D10 Phase 3 |
| P-OPS-5 | Delivery ratio that counts as "not captured", and the canary delivery gate | 99.9 % | 99–99.99 % | o4 D10 P2; s3 D10 (99.9 %); g2 D10 (99 %) |
| P-OPS-6 | Delay before an approved parameter change takes effect | 7 d, and never less than the maximum Envelope lifetime | 7–30 d | o4 D7; o2 D7 (7-day timelock) |
| P-OPS-7 | Expiry of an emergency action that has not been ratified | 7 d | 1–7 d | o4 D7; `runtime/src/lib.rs:758` (`SafeModeForceDuration = 7 * DAYS`) |
| P-OPS-8 | Public notice period before a Registry maintenance update | 14 d | 7–30 d | o4 D7 |
| P-OPS-9 | Maximum steward seats held by one organization | 2 of 7 | 1–2 | o4 D7 |
| P-OPS-10 | Registry-view lag after which admission failures become Ignore | 60 s (10 blocks) | 30–300 s | **assumption** from o4's "last 10 roots ≈ 60 s"; 6 s slot at `runtime/src/lib.rs:292` |
| P-OPS-11 | Time from relay removal to the end of meshing by every Bus Node | 600 s | 60–10,800 s | **assumption**; Tor clients see BadExit within 3 h (`2014-winter-spoiledonions` txt L85-95) |
| P-OPS-12 | Evidence window for ejection in the open phase | probe failure above threshold sustained 72 h | 24–168 h | o4 D7 |
| P-OPS-13 | Deadline for deleting a tombstoned Envelope | 48 h | 24–72 h | o4 D7 |
| P-OPS-14 | Transparency-report period | 90 d | 30–90 d | o4 D7 (quarterly) |
| P-OPS-15 | Time after which debug logging switches itself off | 72 h | 1–72 h | o4 D7 |
| P-OPS-16 | Minimum number of independent monitor organizations and share keepers | 3 | 3–7 | o4 D7; `2026-cao-nymreputation` §1 |
| P-OPS-17 | Canary publication interval per Shard | 60 s | 10–600 s | o4 D7 |
| P-OPS-18 | Differential-privacy ε for published relay counters | 0.3 | ≤ 0.3 | `2018-mani-tor-usage-privacy-preserving` txt L505; o4 |
| P-OPS-19 | Period during which versions N and N−1 are both accepted | 2 × max lifetime + 30 d | ≥ 2 × max lifetime | o4 D1 |
| P-OPS-20 | Independent signers per release | 2 | 2–7 | o4 D7 |
| P-OPS-21 | Time to deploy a Sev1 mitigation (Sev2: 12 h; Sev3: 72 h) | 4 h | 1–12 h | o4 D7 (**assumption**) |
| P-OPS-22 | Maximum duration of a pause→resume drill | 1 h | 0.25–4 h | o4 D10 P1 |
| P-OPS-23 | Consecutive days at the canary gate needed to exit the permissioned phase | 30 d | 30–90 d | o4 D10 P2 |
| P-OPS-24 | Horizon of written operator funding commitments | 12 months | 6–36 months | o2 D4/D10 (12-month runway); s1 R2 D10 gate 6 |
| P-OPS-25 | Organic load below which no anonymity-set claim is published | 20 events/s | 5–50 events/s | o4 D10 P3 |
| P-OPS-26 | Distinct active publisher admissions below which no anonymity-set claim is published | 1,000 | 500–10,000 | o4 D10 P3 |
| P-OPS-27 | Deadline for publishing a post-mortem | 14 d | 7–30 d | o4 D7 |

## 3. Requirements

### Actors and admission

### MPE-OPS-001 No validator duty
MPE shall assign no relay, store, anchoring or bootstrapping duty to a Midnight block-authoring node.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; g1, g2, g3, o1, o2, o3, o4, s1, s2, s3, s4 (g4 keeps validators for inclusion only); `midnight-node/node/src/service.rs:614-618`; `2024-heimbach-deanon`
- Rationale: Bus traffic must not compete with authoring, and event gossip on the validator peer set would expose validator IPs.
- Verify: test. On a testnet validator, a packet capture on the consensus port shows no MPE protocol id, and stopping every Bus Node leaves GRANDPA finality time unchanged (g2 Phase 1).
- Status: settled

### MPE-OPS-002 Separate network identity
The Bus Node shall use a libp2p identity key distinct from every peer key and session key of any co-located midnight-node.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D7, D8; g1 D8, g2 D8, s1 D7 ("never assign validator consensus keys to privacy transport")
- Rationale: An event-mesh peer id must not be linkable to a chain peer id.
- Verify: test. Run the Prototype beside a node and check that the two `identify` responses carry different public keys.
- Status: settled

### MPE-OPS-003 Separate bootstrap set
The Bus Node shall bootstrap only from a published list of at least P-OPS-3 MPE bootstrappers that contains no Midnight chain bootnode.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D7; g2 D7; o1 R2 D7 vote; `2018-marcus-ethereumeclipse` via g2 (a poisoned DNS seed list)
- Rationale: A single seizure or eclipse must not hit consensus peering and event peering at the same time.
- Verify: inspection of the shipped list against the chain-spec bootnodes, plus a Prototype config-load test.
- Status: settled

### MPE-OPS-004 Bootstrapper profile
Where a Bus Node runs as a bootstrapper, the Bus Node shall apply the GossipSub v1.1 bootstrapper profile (`D = D_lo = D_hi = D_out = 0`, Peer Exchange with signed peer records).
- Pattern: optional
- Scope: POC
- Priority: SHOULD
- Source: D7; g2, o1 R2; `libp2p/specs/pubsub/gossipsub/gossipsub-v1.1.md:654-661`
- Rationale: Bootstrappers then hand out peers without becoming mesh chokepoints.
- Verify: test. A bootstrapper's mesh stays empty over 1 h while PX responses are returned.
- Status: settled

### MPE-OPS-005 Role trust disclosure
MPE shall publish, before the first Operator is admitted, a statement for each Operator role of what that role observes and what it can withhold, delay or forge.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; s3 D7 ("explicit trust disclosure"), s4 D7, o2 D7, o4 D7 actor table
- Rationale: Users and auditors need the trust boundary in writing, not inferred from code.
- Verify: inspection. Every role in the Glossary has a published statement.
- Status: settled

### MPE-OPS-006 Content-blind roles
MPE shall define no Operator role or governance role that holds a key able to open an Envelope body.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; o4 P8; s2 D7; g1 D7; rejected escrow per `2026-cinal-viewingkeycompromise` and `2023-agrawal-traceablemixnets` (via o4)
- Rationale: A power that does not exist cannot be compelled.
- Verify: inspection of the role definitions and key inventory; analysis of the Registry operations.
- Status: settled

### MPE-OPS-007 Allow-listed mesh at launch
While the relay allow-list is active, the Bus Node shall accept GRAFT only from peers whose identity is on the Registry relay list.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D7; g1 D7, o4 D7, s3 D7 (published roster), o1 R2 vote; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:1018,1106`
- Rationale: The Sybil resistance of open GossipSub meshes is not established (`2020-leastauthority-gossipsub-audit`; `2022-kumar-gossipsub-formal`).
- Verify: test. A non-listed Prototype peer that sends GRAFT is pruned, while it can still publish as a non-mesh peer.
- Status: open (DEC-OPS-1)

### MPE-OPS-008 Allow-list removal gate
MPE shall keep the relay allow-list active until a red-team holding P-OPS-4 peer identities fails to push honest delivery below P-OPS-5 under the production scoring parameters.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7, D10; g1 D7/D10; o4 R2 amendment; o1 R2; s1 R2 caveat
- Rationale: Passing the red-team is necessary but does not prove permissionless safety (s1 R2), so removal remains a separate decision.
- Verify: simulation and demonstration. A red-team run on the Phase 1 network with targeted placement at 1, 3 and 5 % (s3 D10).
- Status: open (DEC-OPS-1)

### MPE-OPS-009 Launch operator count
While the relay allow-list is active, MPE shall list relays run by at least P-OPS-1 independent organizations.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D7; s1 D7, s2 D7, s4 D7, g1 D7, o4 R2
- Rationale: Too few operators turns the mesh into a small cartel that can censor (g1 D9).
- Verify: inspection of the roster against operator attestations.
- Status: open (DEC-OPS-6)

### MPE-OPS-010 Concentration cap
MPE shall keep the share of listed relays run by any one organization at or below P-OPS-2.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D10 P3; o2 D7 (1/k saturation)
- Rationale: One operator holding most of the relays can capture the mesh.
- Verify: inspection of the roster each time the Registry relay list changes.
- Status: open (DEC-OPS-6)

### MPE-OPS-011 Gates counted per organization
MPE shall compute every decentralization-gate metric per verified organization, not per peer identity or bond key.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; s1 R2, s3 D7, s4 D7, o2 R2 (concedes key splitting); `2026-cao-nymreputation` Appendix D; `2002-douceur-sybil` §§1–3
- Rationale: Self-created identities do not prove independent operators.
- Verify: inspection of the gate report method.
- Status: settled

### Governance

### MPE-OPS-012 Parameter time-lock
When a Registry parameter change is approved, the Registry shall defer its effect by at least P-OPS-6.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7, o2 D7
- Rationale: Envelopes already in flight and existing members must not see the rules change underneath them.
- Verify: analysis using the Quint invariant I1 "no parameter takes effect before its delay" (o4), plus a devnet test.
- Status: open (DEC-OPS-2)

### MPE-OPS-013 Emergency expiry
If an emergency action is not ratified within P-OPS-7, then the Registry shall restore the value in force before that action.
- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7; `runtime/src/lib.rs:758`
- Rationale: This mirrors Midnight's own bounded safe mode, so emergency powers cannot become permanent.
- Verify: analysis using the Quint invariant I2 (o4), plus a devnet test with no ratification.
- Status: open (DEC-OPS-2)

### MPE-OPS-014 Exits survive a bus pause
Where the Registry holds Publisher deposits, while the bus pause flag is set, the Registry shall accept withdrawal and slashing calls.
- Pattern: complex
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7 (I3); s4 R2 (this holds only against the bus-local flag, not against chain safe mode, `check_call_filter.rs:44-45`)
- Rationale: A pause must not hold user funds hostage. Chain safe mode remains an inherited residual.
- Verify: analysis using the Quint invariant I3, plus a devnet test with the bus paused.
- Status: open (DEC-OPS-2)

### MPE-OPS-015 No revocation by fiat
The Registry shall provide no governance operation that revokes a Publisher admission credential without misuse evidence checked by the Registry circuit.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7, o1 D4 (`revoke(sk)` with proof), s3 D4 (revoke only proven equivocators)
- Rationale: Governance must not be able to target publishers. Only proven misuse removes a credential.
- Verify: inspection of the Registry entry points; analysis that every removal path checks evidence.
- Status: open (DEC-OPS-2)

### MPE-OPS-016 Maintenance notice
When a Registry maintenance update is prepared, MPE shall publish its full content at least P-OPS-8 before submitting it.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7; s2 R2; `midnight-ledger/ledger/src/structure.rs:2104-2113` (`ReplaceAuthority`, `VerifierKeyRemove`, `VerifierKeyInsert`)
- Rationale: A maintenance update can replace verifier keys, so it can change any "excluded" power. Notice is the only guard until enforcement on the ledger is known.
- Verify: inspection. The publication time of the notice precedes the transaction's block time by P-OPS-8.
- Status: open (DEC-OPS-2)

### MPE-OPS-017 Measure maintenance constraints
MPE shall determine on a ledger-9 network, before Phase 2, whether a `ContractMaintenanceAuthority` can enforce a delay on verifier-key replacement.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7, D10; o4 D7 (**unknown**); `midnight-ledger/spec/contracts.md:20-37` (authority left unspecified)
- Rationale: Whether governance powers are actually limited depends on this unknown.
- Verify: test on a devnet. Attempt a delayed maintenance update and record the outcome.
- Status: settled

### MPE-OPS-018 Public governance events
When the Registry applies a parameter change, pause, emergency action or relay ejection, the Registry shall emit a public event naming the action and its reason code.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D1/D7 (`Misc "MPE/param/v1"`), o2 D7 (gates readable from contract state)
- Rationale: Every governance act should be auditable from the chain alone.
- Verify: test. Each action type on a devnet produces one matching event in the `contractEvents` output.
- Status: settled

### MPE-OPS-019 Steward diversity
Where a steward set governs the Registry, MPE shall seat no more than P-OPS-9 stewards from any one organization.
- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7 (7 seats, ≥ 4 orgs, ≥ 3 jurisdictions)
- Rationale: A threshold signature spread across organizations resists capture and coercion.
- Verify: inspection of the steward roster at every steward-set change.
- Status: open (DEC-OPS-2)

### MPE-OPS-020 Governance end state
Before the open-admission phase exits, MPE shall either transfer the Registry maintenance authority to Midnight federated governance or remove that authority.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7, g1 D7 (Root via Council and TC), o3 D7 (immutable contracts); `runtime/src/lib.rs:789, 907-943` (5-day motions, 2/3 Council and 2/3 TC)
- Rationale: A bus-specific authority is a launch measure, not the end state.
- Verify: inspection of the Registry's maintenance authority in the ledger state.
- Status: open (DEC-OPS-2)

### Chain dependence and failure handling

### MPE-OPS-021 Overlay survives a chain pause
While the Midnight chain filters `send_mn_transaction`, the Bus Node shall continue relaying Envelopes admitted under its last cached Registry roots.
- Pattern: state
- Scope: POC
- Priority: MUST
- Source: D7, D9; o4 D7, g1 D7, g3 D9, s2 D9, s4 D9; `check_call_filter.rs:44-45`; `runtime/src/lib.rs:321`
- Rationale: A chain incident must not become a bus outage. New registrations and anchors still stop.
- Verify: test. With the mock Ledger Adapter frozen, admitted Envelopes keep reaching Subscribers.
- Status: settled

### MPE-OPS-022 Stale view gives Ignore
If the Bus Node's Registry view lags the chain head by more than P-OPS-10, then the Bus Node shall return Ignore, not Reject, for Envelopes whose admission check depends on that view.
- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D7, D9; o1 R2 D9; `rust-libp2p/protocols/gossipsub/src/types.rs:51-58` (only Reject triggers P₄)
- Rationale: A lagging indexer must not cause honest forwarders to be graylisted, which would partition the network.
- Verify: test. With a delayed mock adapter, the P₄ counters of honest peers stay at zero.
- Status: settled

### MPE-OPS-023 Ejection takes effect
When a relay is removed from the Registry relay list, the Bus Node shall stop meshing with that relay within P-OPS-11.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D7; o4 D7, g1 D7; `rust-libp2p/protocols/gossipsub/src/behaviour.rs:1035`; `2014-winter-spoiledonions` txt L85-95
- Rationale: Removal by governance needs a bounded, testable effect on the network.
- Verify: test. Remove a peer in the mock Registry, then measure the time until no Prototype has it in any mesh.
- Status: settled

### MPE-OPS-024 Evidence-only ejection when open
While the relay allow-list is inactive, MPE shall eject a relay only on published monitor evidence of probe failure above threshold sustained for P-OPS-12, or on a malformed anchor it signed.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7 (P3+, 7-day appeal); `2026-cao-nymreputation` §1
- Rationale: Removal at discretion invites framing and capture once admission is open.
- Verify: inspection. Every ejection event references published evidence.
- Status: open (DEC-OPS-2)

### Abuse handling

### MPE-OPS-025 Tombstone deletion
Where an Operator has signed the Operator Agreement, when its Store Node receives a tombstone for an Envelope identifier signed by the governance threshold, the Store Node shall delete that Envelope within P-OPS-13.
- Pattern: complex
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7 and R2 amendment; s4 R2 (cooperative deletion only)
- Rationale: The design needs a defined, auditable delete-by-ID path that reads no content. It does not remove copies held by an adversary.
- Verify: test. Canary tombstones; at least 99 % deleted within P-OPS-13 (o4 D10).
- Status: open (DEC-OPS-5)

### MPE-OPS-026 Tombstoned Envelope not relayed
When the Bus Node holds a valid tombstone for an Envelope identifier, the Bus Node shall Ignore that Envelope.
- Pattern: event
- Scope: POC
- Priority: SHOULD
- Source: D7; o4 D7
- Rationale: Ignore stops re-propagation without penalizing honest peers who forwarded the Envelope earlier.
- Verify: test. A replayed tombstoned Envelope is not forwarded, and the sender's P₄ count does not change.
- Status: open (DEC-OPS-5)

### MPE-OPS-027 Transparency report
MPE shall publish, every P-OPS-14, a report of the counts of tombstones, ejections, emergency actions and slashes in that period.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7 and R2 amendment
- Rationale: Public counts make it visible when takedown or governance power is misused.
- Verify: inspection. The report counts match the Registry events for the period.
- Status: open (DEC-OPS-5)

### MPE-OPS-028 Abuse report on explicit action only
The MPE client library shall send an abuse report only on an explicit request by the receiving user.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7, D2; o4 P7; s1 D10 (no network action that depends on recognition); o4 R2 D2 objection
- Rationale: An automatic report would reveal that the client recognized the Event.
- Verify: test. Paired clients with different interests emit identical traffic when no report is requested.
- Status: settled

### MPE-OPS-029 No IP persistence
The Bus Node shall not write peer IP addresses to persistent storage in its default configuration.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D7; o4 D7 (no-logging default)
- Rationale: Logs that do not exist cannot be compelled or leaked.
- Verify: test. After a 24 h Prototype run, a search of disk and logs finds no peer IP.
- Status: settled

### MPE-OPS-030 Debug logging expires
If debug logging is enabled on a Bus Node, then the Bus Node shall disable it after P-OPS-15.
- Pattern: unwanted
- Scope: POC
- Priority: SHOULD
- Source: D7; o4 D7
- Rationale: Logging used during an incident must not become permanent surveillance.
- Verify: test using a simulated clock.
- Status: settled

### Monitoring

### MPE-OPS-031 Canary probes
MPE shall run canary Publishers in every Shard from at least P-OPS-16 monitor organizations, each publishing one Envelope per P-OPS-17.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; g3 R2 (canary load ≈ 0.13 events/s with 8 Shards, negligible)
- Rationale: Delivery, latency, back-fill and tombstone compliance can then be measured without user telemetry.
- Verify: inspection of the monitor roster; demonstration from canary logs.
- Status: open (DEC-OPS-4)

### MPE-OPS-032 Canaries look ordinary
The MPE client library shall send canary Envelopes through the same size classes and admission path as other Envelopes.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; `2014-winter-spoiledonions` (relays that evaded probes)
- Rationale: Relays that can recognize probes can treat them differently from real traffic.
- Verify: analysis. A classifier trained on relay-visible fields does no better than chance at telling canaries from other Envelopes.
- Status: open (DEC-OPS-4)

### MPE-OPS-033 Aggregated counters only
Where Bus Node counters are published, the Bus Node shall release them only through secure aggregation across at least P-OPS-16 share keepers with ε ≤ P-OPS-18.
- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7; `2016-jansen-safely-measuring-tor`; `2018-mani-tor-usage-privacy-preserving` txt L505
- Rationale: Load can be measured without exposing any single relay's or user's activity.
- Verify: inspection of the counter-export path; test that no unaggregated counter leaves the node.
- Status: open (DEC-OPS-4)

### MPE-OPS-034 Multi-monitor decisions
MPE shall base each relay ejection or Operator payout on measurements from at least P-OPS-16 independent monitors.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D4/D7; `2026-cao-nymreputation` §1 (a single monitor allowed framing that cut attack cost by over 99 %)
- Rationale: Spreading measurement across monitors resists framing.
- Verify: inspection of each ejection and payout record.
- Status: open (DEC-OPS-4)

### Upgrades and key rotation

### MPE-OPS-035 Version overlap
When a new Envelope version is activated, the Bus Node shall accept both the new and the previous version for at least P-OPS-19.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D7, D1; o4 D1/D7; s4 D10 (separate upgrade trials)
- Rationale: Envelopes still in flight, and clients that upgrade late, must not be dropped.
- Verify: test. A mixed-version Prototype mesh delivers both versions through the overlap period.
- Status: settled

### MPE-OPS-036 Version deny-list
When the Bus Node receives a version deny-list entry signed by the governance threshold, the Bus Node shall Ignore Envelopes of that version.
- Pattern: event
- Scope: POC
- Priority: SHOULD
- Source: D7; o4 D7 (3-of-7 signed deny-list); o1 R2 (Ignore keeps honest peers off the graylist)
- Rationale: A broken crypto or parser version can be stopped without a chain lever.
- Verify: test. Envelopes of the denied version are dropped, and no peer's P₄ count changes.
- Status: open (DEC-OPS-2)

### MPE-OPS-037 Relay key handover
The Bus Node shall support replacing its identity key through a handover signed by the old key and recorded in the Registry relay list.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7 (yearly rotation)
- Rationale: Keys can then be rotated without the operator being ejected and admitted again.
- Verify: test on a devnet. After the handover the new key is grafted and the old key is not.
- Status: settled

### MPE-OPS-038 Signed reproducible releases
MPE shall publish each Bus Node release as a reproducible build signed by at least P-OPS-20 independent signers.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7; o4 D7; `design/evidence/bitmessage-guide.md:373` (an unaudited, unpatched release line)
- Rationale: This is the supply-chain defence for a binary that every operator runs.
- Verify: test. Two independent rebuilds match the release hash bit for bit.
- Status: settled

### Incident response

### MPE-OPS-039 Sev1 mitigation time
When an incident is classified Sev1, MPE shall deploy a mitigation within P-OPS-21.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7 (Sev1 covers parser RCE, a crypto break, a deanonymization bug)
- Rationale: A bounded response time is what lets operators and users rely on the bus.
- Verify: demonstration. Timed drills, at least two per year (o4 D10).
- Status: settled

### MPE-OPS-040 Post-mortem
When a Sev1 or Sev2 incident is closed, MPE shall publish a post-mortem within P-OPS-27.
- Pattern: event
- Scope: PROD
- Priority: SHOULD
- Source: D7; o4 D7
- Rationale: A public account of each serious incident lets others judge whether operators behaved as stated.
- Verify: inspection of the incident log against publication dates.
- Status: settled

### MPE-OPS-041 Pause drill
MPE shall complete a bus pause-to-resume drill within P-OPS-22 before exiting Phase 1.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; o4 D10 P1
- Rationale: The emergency lever must be shown to work in both directions.
- Verify: demonstration on the Phase 1 network, with timestamps from the Registry events.
- Status: settled

### Build, verification and launch phases

### MPE-OPS-042 Gated phases
MPE shall not start a launch phase until every exit gate of the preceding phase has passed with published evidence.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; o4, o2, o1, g1, g2, g3, s1, s3, s4
- Rationale: Every proposal gates phases on measurements rather than dates.
- Verify: inspection of the gate record for each phase transition.
- Status: settled

### MPE-OPS-043 Evidence freeze
Before Phase 0 exits, MPE shall record the deployed ledger version, the runtime `spec_version` and the pinned revisions of every Midnight component the bus depends on.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D10; s4 D10; o4 R2; o3 R2; `midnight-node/Cargo.lock:7894, 8460, 7609`
- Rationale: The tag, the lockfile and the docs disagree, for example on the 1 KiB log limit.
- Verify: inspection of the claim register against a live RPC `spec_version` query.
- Status: settled

### MPE-OPS-044 Ledger-generation gate
While the target network runs ledger 8, MPE shall make no production claim for a feature that needs ledger-9 contract events or cross-contract calls.
- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D10; o3 R2, o4 R2, g4 D10; `building-blocks.mdx:79-83`; `toolchain-0.33.0.md:12`
- Rationale: Anchors, `contractEvents` and contract consumption do not exist on today's mainnet.
- Verify: inspection of the published feature claims against the network's ledger version.
- Status: settled

### MPE-OPS-045 Prototype on a mock adapter
The Prototype shall run every Phase 0 test against a mock Ledger Adapter without a public Midnight network.
- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D10; Brief glossary; o3 R2 (measurements must run locally until a public network upgrades)
- Rationale: Phase 0 cannot wait for ledger 9 to be activated.
- Verify: demonstration. The full test suite passes offline.
- Status: settled

### MPE-OPS-046 Measured Registry costs
Before Phase 1 exits, MPE shall measure on a ledger-9 network the serialized bytes and DUST fee of one Registry admission transaction and of one anchor transaction.
- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D10; g3 D10 (gate ≤ 16 KiB, ≤ 0.5 DUST); o1, o2, o3, s4 R2, g3 R2
- Rationale: Every DUST and anchoring budget in the proposals is scaled from a transaction size nobody has measured.
- Verify: test on a devnet with the recorded `ledgerParameters`.
- Status: settled

### MPE-OPS-047 Scoring-CVE gate
Before any Bus Node peers outside a test network, MPE shall reproduce the CVE-2022-47547 score-manipulation attack against the pinned GossipSub implementation and observe it fail.
- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D10, D9; g2 D10; s2 R2 (a reproduction is stronger than a changelog); g3 R2; `2023-kumar-gossipsub-acl2s`
- Rationale: A known flaw in scoring would undermine both allow-list removal and ejection.
- Verify: test. Run the attack scenario on the Prototype and check that the attacker's score falls below the graylist threshold.
- Status: settled

### MPE-OPS-048 Audit gate
MPE shall not deactivate the relay allow-list while an independent audit of the Bus Node parser, admission check or Registry has an open critical or high finding.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; o4 D10 P2, s2 D10, s4 D10, s3 D10 Phase 2; `bitmessage-guide.md:352-358`
- Rationale: Bitmessage's remote code execution came from unaudited parsing of types chosen by the attacker.
- Verify: inspection of the audit report status.
- Status: settled

### MPE-OPS-049 Permissioned-phase exit
MPE shall not leave the permissioned-overlay phase until canary delivery has stayed at or above P-OPS-5 for P-OPS-23 consecutive days.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; o4 D10 P2
- Rationale: Admission should open only after the bus has proven itself on real operators.
- Verify: demonstration from the canary records (MPE-OPS-031).
- Status: settled

### MPE-OPS-050 Counsel-memo gate
MPE shall not admit an Operator in a jurisdiction without a counsel memo on the liability of relaying ciphertext in that jurisdiction.
- Pattern: ubiquitous
- Scope: PROD
- Priority: SHOULD
- Source: D7, D10; o4 D7/D10 (liability **unknown**); s4 R2 (legal consequences **unknown**)
- Rationale: Regulatory shutdown is the most likely way the bus ends (o4 R2 D9).
- Verify: inspection. One memo on file for each roster jurisdiction.
- Status: open (DEC-OPS-5)

### MPE-OPS-051 Funding gate
MPE shall not leave the permissioned-overlay phase without written funding commitments covering every launch Operator role for P-OPS-24.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D7, D10; s1 R2 D10 gate 6; o2 D10 (12-month runway); s4 D7 (prices **unknown**)
- Rationale: No on-chain payment exists for operators (`runtime/src/lib.rs:681-698` returns `(0, None)`), so availability rests on commitments.
- Verify: inspection of the signed commitments against the roster.
- Status: open (DEC-OPS-3)

### MPE-OPS-052 Anonymity-claim gate
MPE shall publish no broadcast anonymity-set claim while organic load is below P-OPS-25 or distinct active publisher admissions number fewer than P-OPS-26.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10, D2; o4 D10 P3; `2017-das-trilemma`
- Rationale: An empty network has no anonymity set to claim.
- Verify: inspection of published claims against aggregated load (MPE-OPS-033) and Registry counts.
- Status: settled

### MPE-OPS-053 Course-change register
MPE shall maintain a register in which each course-change trigger has a measurable threshold and a named response.
- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D10; g4 T1–T4, o4 D10 (6 triggers), o2 D10, o1 D10, g2 D10
- Rationale: A reason to change course should be decided before the evidence arrives, not argued afterwards.
- Verify: inspection. Every trigger has a numeric threshold and a response.
- Status: settled

### MPE-OPS-054 Launch sequencing
While no ledger-9 mainnet activation date precedes the Phase 1 start date, MPE shall run Phase 1 as a permissioned overlay whose Ledger Adapter targets a ledger-9 devnet.
- Pattern: state
- Scope: PROD
- Priority: SHOULD
- Source: D10, D8; o3 R2 (an explicit switch); o1 R2 (a ledger-8 branch is missing); g1, g2, g3, s1–s4 (overlay first); o4, o3, g4 (ledger first)
- Rationale: A ledger-first phase has no public network to run on today.
- Verify: inspection of the Phase 1 deployment against the network's ledger version.
- Status: open (DEC-OPS-7)

## 4. Decisions

**DEC-OPS-1: Relay admission at launch.**
- Options:
  - (a) A permissioned allow-list, removed only after a red-team fails to capture the mesh: g1, o4 (amended), o1 R2.
  - (b) Dedicated or contracted operators, with anyone else allowed to relay: s1, s2, s4, s3 (published roster).
  - (c) Open relays scored from the start or from phase 2: g2, g3, o1 R1, o2.
- Recommended default: (a).
- Reason:
  - Scoring is not a complete Sybil defence (`2020-leastauthority-gossipsub-audit`).
  - Formal work found configurations in which a peer keeps a positive score while withholding (`2022-kumar-gossipsub-formal`).
  - s1 R2's caveat is recorded: passing the red-team is necessary, not sufficient.
- Settling check: the MPE-OPS-008 red-team at 1/3/5 % targeted placement, run under the production scoring parameters.

**DEC-OPS-2: Governance authority.**
- Options:
  - (a) A bus steward set (7 seats; 5-of-7 normal, 3-of-7 emergency), with time-locks and 7-day emergency expiry. End state: hand over to Council and TC, or ossify. o4; s4 R2 votes for a reduced form.
  - (b) Midnight Root via Council and TC from day one: g1.
  - (c) A foundation multisig with a 7-day timelock: o2.
  - (d) Immutable contracts and no new governance role: o3 end state, g4.
- Recommended default: (a).
- Reason:
  - Federated motions take 5 days (`runtime/src/lib.rs:789`), which is too slow to eject a relay that is injecting malformed objects (o4 R2).
  - (d) offers no ejection or emergency path for an overlay.
- Settling check:
  - Quint invariants I1–I6 (o4) hold.
  - MPE-OPS-017 shows whether maintenance can be time-locked on the ledger. If it cannot, (a) relies on notice alone, and (d) gains weight.

**DEC-OPS-3: Who pays launch operators.**
- Options:
  - (a) Relays unpaid by the protocol: g1, g2, g3, o1, o2.
  - (b) A contracted service pool: s1, s2, s3, s4.
  - (c) Grants, then a pool paid on probe scores: o4.
  - (d) Bonded, paid stores and anchorers backed by a treasury: o2.
- Recommended default for this area: relays unpaid by the protocol in v1. Store, anchor and monitor roles are funded off-protocol, subject to the commitment gate in MPE-OPS-051. The protocol payment mechanism is left to the economics area's D4 decision.
- Reason:
  - No reward stream exists (`runtime/src/lib.rs:681-698`).
  - Paying on probe scores invites framing (`2026-cao-nymreputation`).
  - g2 R2 doubts that read-heavy relays will forward for free. That is why stores carry the funding gate.
- Settling check: operator bids (s1 D4) and o2's economic simulation, both before the permissioned phase exits.

**DEC-OPS-4: Monitoring method.**
- Options:
  - (a) Canaries from several monitor organizations plus PrivCount-style aggregated counters: o4.
  - (b) On-chain signals only: g4, and o2 for payouts.
  - (c) Per-key concentration reports: o2.
- Recommended default: (a), with monitors that measure only. Payouts are not tied to probe scores until a framing analysis exists.
- Reason: delivery cannot be verified without some measurement, and (a) needs no per-user telemetry.
- Settling check: a framing simulation with one malicious monitor out of P-OPS-16 shows no wrongful ejection.

**DEC-OPS-5: Takedown and legal exposure.**
- Options:
  - (a) Signed tombstones with a 48 h deadline, counsel memos and transparency reports: o4.
  - (b) No takedown path and no new role: g4. This works only because g4 puts ciphertext permanently on the ledger.
  - (c) Cooperative deletion only, with no claim of deletion from adversarial copies: s4 R2.
- Recommended default: (a), limited as in (c). Tombstones bind only operators who signed the Operator Agreement, and every tombstone is published.
- Reason: every store holds the same ciphertext, so a court order would otherwise reach every operator at once, and none could show compliance (o4 R2 D6).
- Settling check: counsel memos for the Phase 1 jurisdictions. If counsel requires capabilities that break MPE-OPS-006, the bus stops at the ledger-only fallback (o4 D10 trigger 1).

**DEC-OPS-6: Launch operator counts.**
- Options:
  - g1: 8–16 operators.
  - s1: 16 relays from at least 8 organizations.
  - s2: at least 5 organizations.
  - s4: 20 relays from at least 5 operators.
  - o2: at least 6 relays in at least 3 regions.
  - o4: at least 3 operators, amended to at least 8 organizations.
- Recommended default: at least 8 organizations, no organization above 20 %.
- Reason: this is the largest count that two proposals already back, and it keeps a single-operator cartel below the capture threshold of any shard.
- Settling check: s3's targeted-adversary simulation at 1/3/5 %, plus procurement showing that 8 organizations can actually be found.

**DEC-OPS-7: First production phase.**
- Options:
  - (a) Ledger-and-indexer lane first: o3, o4 P1, g4.
  - (b) Permissioned overlay first, with anchoring on a devnet: g1, g2, g3, o1, o2, s1–s4.
  - (c) An explicit switch on the ledger-9 date: o3 R2.
- Recommended default: (c), which today resolves to (b) for the Prototype.
- Reason: Preview, Preprod and Mainnet run ledger 8 (`building-blocks.mdx:79-83`).
- Settling check: the published ledger-9 hard-fork date, and the live `spec_version` on mainnet.

## 5. Cross-area dependencies

The area prefixes below are assumed and should be matched at merge.

- **Admission and economics (ECON, D4):**
  - the admission credential and the misuse evidence that MPE-OPS-015 relies on;
  - whether the Registry holds deposits (MPE-OPS-014);
  - the payment mechanism behind DEC-OPS-3;
  - the stricter first-contact tier and recipient consent (the abuse vector o4 R2 raised).
- **Network and tether (NET, D5/D8):**
  - the mesh profile;
  - flood-publish off (the default is `true`: `gossipsub-v1.1.md:549`; `rust-libp2p/.../config.rs:548`);
  - `D_out`;
  - Phase 0 stop conditions (g2: delivery below 99 %, or p99 above 6 s at N = 200).
- **Performance (PERF, D5):** the p99 target paired with the canary gate in MPE-OPS-049.
- **Storage (STORE, D6):** Envelope lifetime (P-OPS-6 and P-OPS-19 depend on it); the minimum number of Store Node organizations per Shard (o4: 3); retention and deletion semantics.
- **Envelope format (FMT, D1):** the version byte or protocol id used by MPE-OPS-035 and 036; the franking slot behind application-level reports.
- **Privacy definition (PRIV, D2):** P7/P8 (report-only disclosure, operator content-blindness) as named properties; the paired-execution test for MPE-OPS-028.
- **Registry and Ledger Adapter (REG):** relay-list storage; governance events (MPE-OPS-018); the root cache used by MPE-OPS-021 and 022.
- **Threats (THREAT, D9):** threat rows for regulatory shutdown, steward capture, compelled disclosure and reputation framing.
- **Verification (VERIF, D10):** the claim register format; Quint invariants I1–I6.

## 6. Glossary additions

| Term | Meaning |
|---|---|
| Relay allow-list | The Registry relay list. While it is active, only listed Bus Nodes may join a mesh. |
| Bootstrapper | A Bus Node with an empty mesh that only serves Peer Exchange. |
| Anchorer | An Operator that submits Anchors to the Registry. |
| Steward | The holder of one seat in the bus governance threshold set (DEC-OPS-2). |
| Emergency action | A governance action that takes effect immediately and expires unless ratified. |
| Monitor | An organization that runs canaries or holds an aggregation share. It sees no content. |
| Canary | A Publisher/Subscriber pair, operated by a Monitor, used to measure delivery. |
| Tombstone | A governance-signed instruction to delete one Envelope identifier. |
| Operator Agreement | The contract that binds an Operator to the tombstone deadline, the no-logging default and an abuse contact. |
| Organization | A legal entity verified off-chain. It is the unit of every diversity metric. |
| Sev1 / Sev2 / Sev3 | Incident classes: Sev1 is RCE, a crypto break or a deanonymization bug; Sev2 is network-wide spam, an outage or an anchor stall; Sev3 is a single misbehaving relay. |
| Phase 0–4 | Phase 0: models, simulation and the Prototype. Phase 1: permissioned pilot. Phase 2: permissioned production overlay. Phase 3: open admission. Phase 4: governance handover and stronger privacy profiles. |

## 7. Gaps

- **Operator independence.** No protocol mechanism can verify that two organizations are independent (`2002-douceur-sybil`; s1 R2). MPE-OPS-009–011 rest on attestations that can be falsified.
- **Intermediary liability.** Whether relaying ciphertext is protected in any given jurisdiction is **unknown** (o4). MPE-OPS-050 requires the memo but cannot require a favourable answer.
- **Chain safe mode.** Midnight governance can stop all registrations and anchors (`check_call_filter.rs:44-45`). This is an inherited residual, not a requirement the bus can meet. o4's trigger "safe mode is used often" has no agreed numeric threshold.
- **Lever ordering.** o4 orders its incident levers from least to most invasive: scoring, ejection, tightening, pause, deny-list. No pass/fail test separates a correct choice from an over-reaction, so this is guidance only.
- **Moderation quality.** Franking moderators belong to applications (s4 R2). Requirements on moderator behaviour, such as threshold moderation (`2019-tyagi-messagefranking`), are outside the bus.
- **Funding sustainability.** MPE-OPS-051 checks commitments, not whether they will be kept. o2 R2 notes that no third party can test the funding model before mainnet.
- **Tombstone effect.** Deletion by cooperating operators does not remove copies held by an adversary. Ciphertext already anchored on the ledger cannot be deleted at all.
