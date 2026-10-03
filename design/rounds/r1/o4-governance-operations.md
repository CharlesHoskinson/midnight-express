# Midnight Private Events: Round 1 proposal (governance, compliance and operations)

## Summary of position

I propose a **hybrid bus**. Sealed envelopes of fixed size travel on a separate libp2p GossipSub overlay that runs as a sidecar next to Midnight nodes and needs no node fork. One Compact **Bus Registry contract** on Midnight holds everything that must be public and enforced: rate-limit memberships (RLN-v2) and their deposits, the relay registry, protocol parameters, the steward multisig, a pause flag, and a 32-byte batch root every 60 s so that contracts can consume events. Nothing a user writes is ever stored on the ledger. Abuse is handled in layers, and no layer needs anyone to read content in bulk. Volume abuse is stopped by RLN quotas with slashing. Unwanted contact is stopped by recipient-side consent lists. Abusive content in an application is reported by the recipient to a moderator that the application names, using franking. Lawful takedown works as delete-by-event-ID on short-lived off-chain storage. I **reject** key escrow, master viewing keys, protocol-level tracing and protocol-level bans by fiat. Governance is a public, time-locked steward multisig. Emergency powers mirror Midnight's own safe mode and expire after 7 days. Its end state hands control to Midnight's Council and Technical Committee or ossifies the contract. Launch has five gated phases and starts with a ledger-only mode. Every phase has measurable gates and named reasons to change course. My lean: privacy that has no credible answer for spam, harassment and takedown requests will be switched off, and Midnight has the switch (tx-pause and safe mode block all user transactions: `midnight-node/runtime/src/lib.rs:321,746`; `runtime/src/check_call_filter.rs:40-45`). So the bus must not rely on that switch staying off.

---

## D1 Event format

**Envelope v1.** The header has fixed offsets and is visible to relays. The body is sealed. Every field has a fixed length, and nothing in the payload drives dynamic type dispatch. PyBitmessage 0.6.2 was exploited remotely through an `eval()` on message-controlled type data (`design/evidence/bitmessage-guide.md:352-358`).

| Field | Bytes | Visible to relays | Purpose |
|---|---|---|---|
| version | 1 | yes | crypto and format agility (D7 upgrades) |
| size_class | 1 | yes | 0 = 512 B, 1 = 2 KiB, 2 = 8 KiB, 3 = 32 KiB sealed body |
| shard | 1 | yes | 0–7 at launch; derived from the topic key (autosharding, `2024-cornelius-waku-network-dapps` txt L54, L58-61) |
| flags | 1 | yes | anchor-requested, intro-inbox |
| expiry | 4 | yes | Unix seconds; at most now + `T_max` (default 24 h, governance maximum 7 d, hard ceiling 14 d = mainnet `global_ttl`, `ledger-parameters-config.json:176`) |
| tag | 32 | yes | pseudorandom routing tag (D3); all zeros for the intro inbox |
| RLN fields | 32 × 4 + 128 | yes | merkle_root, share_x, share_y, nullifier, Groth16 proof (`2021-vac-waku2-rln-relay-spec` txt L327-330) |
| sealed body | per class | no | HPKE-style ciphertext, padded to the class |

The header is **304 bytes**. `event_id = SHA-256(envelope)` and is never transmitted. Inside the sealed body: a schema hash (32 B), the sender's session or pseudonym material, a sequence number, the payload, and a **franking slot**. The franking slot is a 32-byte committing-AEAD tag in every class (`2017-grubbs-franking` txt L17-19, L697-704). Classes of 2 KiB and above may also carry an asymmetric franking token for sender-anonymous reporting: about 380 B for Hecate (`2021-issa-hecate` Table 4, txt L3466-3479).

**On-ledger formats** (Bus Registry contract; ledger-9/Compact 0.33 generation, see the D8 caveat):
- Anchor: the contract writes `window_id → batch_root` into a ledger `Map`. Contracts cannot read events (`notes/midnight-network-stack.md` §9.12). It also emits `Misc{name:"MPE/anchor/v1", payload: window_id‖shard_bitmap‖root‖count‖relay_id}` (≤ 256 B, `minokawa-compact/compiler/midnight-events.ss:17-74`) for off-chain readers.
- A parameter change emits `Misc{"MPE/param/v1", hash of the new parameter set}`. A pause emits the standard `Paused`/`Unpaused` events (`exports.md:386-403`).

**Encoding.** Fixed-offset binary header; deterministic length-prefixed binary body. The exact codec is an **assumption** left to the protocol designers. **Versioning:** a node accepts versions N and N−1 for at least 2 × `T_max` + 30 days (D7).

## D2 Definition of "private"

| # | Property | Holds against | Does not hold against |
|---|---|---|---|
| P1 | Content confidentiality | relays, store nodes, indexers, chain observers, stewards, global passive adversary (GPA) | recipients; the application moderator, for messages a recipient reports |
| P2 | Publisher unlinkability, event ↔ membership | everyone (RLN zero-knowledge membership, `2022-taheri-waku-rln-relay` txt L177-182) | nobody, unless the publisher exceeds its quota (its secret is then revealed, by design) |
| P3 | Publisher unlinkability, event ↔ IP | ordinary peers, only statistically (first-spy inference remains) | colluding relay minority (partial); GPA. A Dandelion++-style stem in Phase 4 (`2018-fanti-dandelionpp`) |
| P4 | Subscriber-interest privacy | relays and peers of full-shard subscribers (they learn the shard only) | store nodes queried by light clients (tags and IP leak, `2024-aztec-private-events-note-discovery` txt L516) until Phase 4 |
| P5 | Topic privacy | non-members (tags are PRF outputs) | members; volume per broadcast tag inside one rotation period |
| P6 | Relationship privacy | relays, indexers, chain observers | GPA; colluding minority with timing |
| P7 | Report-only disclosure | everyone: only a recipient can reveal a message, and only one it received, to the moderator its application names | the recipient itself (it holds the plaintext anyway) |
| P8 | Operator content-blindness | operators cannot read, search or classify content, so nobody can compel them to | n/a |
| P9 | Timing and volume privacy | padding to 4 size classes only | everyone who sees traffic; **no cover traffic at launch** |

**Leakage table**

| Observer | Learns | Does not learn |
|---|---|---|
| Single relay | peer IPs, headers (shard, class, expiry, tag, nullifier), first-seen time | content, membership, recipient |
| Store node | the above, plus the tags and IP of light clients that query it | content, membership |
| Indexer | which client watches the Bus Registry (one shared contract address, `schema-v4.graphql:548-580` requires one), anchors | events |
| Chain observer | which unshielded address deposited for a membership, membership count, slashes, anchors per window, parameters, relay registry | which events a member published |
| Colluding minority (fraction p of relays) | statistical source estimates; per-tag volume; first-seen correlation | content, membership |
| GPA | likely publisher-to-subscriber pairing by timing | content, membership. **Out of scope at launch.** |
| Application moderator | content and sender pseudonym of reported messages only | everything unreported (`2021-issa-hecate` txt L327-328) |

**Out of scope:** GPA resistance, endpoint compromise, compelled disclosure by users, ISP traffic classification, post-quantum confidentiality in v1 (a v2 hybrid KEM is a version bump; harvest-now-decrypt-later is a named risk in D9).

## D3 Publish and subscribe model

- **Topics → tags.** A broadcast topic has a topic key `K`, and `tag = PRF(K, "mpe-tag" ‖ hour)`, which rotates hourly. A direct channel uses `tag = PRF(S_pair, index)`, a fresh tag per message, in the Aztec pattern `poseidon2(secret, index)` (`2024-aztec-private-events-note-discovery` txt L417, L449). Topic rotation driven by ratchet state is also used in `2026-esposito-verbeth`. Shard = `H(K) mod 8`.
- **Discovery.** Applications publish a signed *topic manifest* off-protocol: shard, schema hashes, moderator franking key, retention class. The bus has no global topic directory, because a directory would leak interest.
- **First contact.** The intro inbox is a dedicated shard-0 tag. Recipients trial-decrypt it, which is Bitmessage's model. Senders need a stricter RLN tier for it (D4).
- **Subscribing without revealing interest.** Full subscribers join the whole shard mesh and filter locally, so only the shard (1/8) leaks. Light clients query store nodes by tag. This leaks; mitigations are decoy tags and rotating store nodes. Phase 4 evaluates OMR, which is server-cheap but has a 956-byte clue and a ~129 MB detection key (`2021-liu-omr` txt L28-29, L318, L3555), and sender-set FMD (`2022-penumbra-fmd-spec` L188-192).
- **Delivery semantics.** At-least-once and unordered. Consumers dedupe by `event_id`. Order within a sender comes from the sealed sequence number. Replay is stopped by expiry plus the GossipSub seen-cache plus the RLN nullifier map over `Thr` epochs (`2022-taheri-waku-rln-relay` txt L352-356, L398). Back-fill comes from store nodes, up to retention.
- **Contracts** cannot subscribe (§9.12). A relayer submits a transaction carrying the event, a Merkle path and `window_id`. The consumer contract cross-calls the Bus Registry to check the root (Compact 0.33 cross-contract calls, `toolchain-0.33.0.md:24, 98-104`). **Anchors prove existence by time, not authorization.** The consumer contract must verify publisher authority in-circuit itself, for example with `jubjubSchnorrVerify` (`exports.md:921-1010`).
- **Wallets.** The wallet SDK runs a light subscriber. The DApp connector has no event method today (`midnight-dapp-connector-api/src/api.ts:70-203`); add `subscribeEvents(manifest)` so DApps do not open their own connections that reveal the user's IP.
- **Agents** run full shard subscribers and may act as contract relayers.

## D4 Sustainable model

- **Publishers pay with capital at risk and a fee.**
  - Membership = RLN-v2 `rate_commitment` (`2024-vac-rln-v2-spec` txt L136-137), inserted into the Bus Registry.
  - Cost of a membership:
    - a refundable deposit `D_m`, held by the contract;
    - a non-refundable fee `F_m`, paid into the relay pool;
    - the DUST transaction fee.
  - The fee exists because deposits alone do not stop Sybil flooding *at* quota (open problem, `2022-taheri-waku-rln-relay` txt L488-493).
  - Withdrawal delay is 7 days, so a member cannot exit early to escape slashing (txt L498-503).
  - Slashing: anyone who submits the recovered secret takes `reward_portion`. It uses commit-reveal to stop front-running (txt L372-383). The remainder goes to the relay pool, not to the stewards.
- **Quota.** Epoch 60 s. Default tier: 20 messages per epoch. Intro-inbox tier: 2 per epoch. Higher tiers cost more `D_m` (RLN-Diff, `2024-vac-rln-v2-spec` txt L40-41, L49-50).
- **Privacy cost of payment.** NIGHT deposits are unshielded, so the depositing address is public. The leak is "address X is a publisher", never which events it published. Whether a shielded NIGHT form exists for `receiveShielded` is **unknown**; check with ledger maintainers.
- **Operators.** Midnight has no on-chain payment path for indexer, RPC or proof operators (§2.3). So:
  - Phase 2: grant-funded (off-protocol, **assumption**).
  - Phase 3: pool funded by `F_m`, the slash remainder and a per-anchor-request fee. Paid every 30 days in proportion to probe-measured service, capped at 1/k of the pool per operator (saturation idea from `2021-diaz-nym` txt L1685-1686).
  - Scoring uses several independent, randomized monitors. Nym's single central monitor enabled framing attacks that cut attack cost by 99% (`2026-cao-nymreputation` txt L429-433, L741-749, L1091-1096).
- **Anchor cost (inference, genesis prices).** About 6 KB per anchor transaction (§9.6) at 0.01 DUST/KB (§7.3) gives 0.06 DUST. One rotating anchorer per 60 s window gives 1,440 anchors/day ≈ **86 DUST/day**. DUST caps at 5 per NIGHT in about a week (`dust-architecture.mdx:109-111`), roughly 0.71 DUST per NIGHT per day, so the backing is ≈ **121 NIGHT** in total. The anchors use 0.06% of block usage (6,144 B per 10 blocks against 1,000,000 B per block). Live prices will differ (§7.2).
- **Low load.** The anonymity set is small. Canary traffic (D7) gives a floor. Broadcast privacy claims are not advertised until the Phase 3 gate (D10).
- **High load.** Stewards raise the shard count (`2024-cornelius-waku-network-dapps` txt L61-63) or tighten quotas through the time-locked process.

## D5 Performance requirements

Assumptions: launch load λ = 50 events/s network-wide sustained and 500/s peak. Mean on-wire size S = 2,048 B body + 304 B header + framing ≈ 2,400 B. GossipSub mesh degree D = 6 (`2020-gossipsub-v11-spec` txt L553). These loads are **assumptions** to be replaced by Phase 2 measurements.

| Node class | Arithmetic | Requirement |
|---|---|---|
| All-shard relay, sustained | λS = 120,000 B/s; worst case ≈ D × λS = 720 KB/s ≈ 5.8 Mbit/s each way | 25 Mbit/s symmetric |
| All-shard relay, peak | 10 × → ≈ 58 Mbit/s each way | 100 Mbit/s |
| Single-shard relay, peak | 58/8 ≈ 7.2 Mbit/s | 20 Mbit/s |
| RLN verification CPU | ≈ 30 ms per proof (`2022-taheri-waku-rln-relay` txt L430): 50/s → 1.5 cores; 500/s → 15 cores all-shard, 1.9 cores per shard | **relays serve at most 2 shards**; batch verification to be benchmarked |
| Publisher (phone) | proof ≈ 0.5 s on iPhone 8 (txt L428-429) | precompute proofs at idle |
| Full subscriber (one shard) | 6.25 ev/s × 2,400 B = 15 KB/s ≈ 1.3 GB/day | desktop and agents only; phones use the light path |

**Latency targets** (to be measured):
- Overlay delivery: p50 ≤ 1 s, p99 ≤ 5 s. **Inference**: about 3 hops for 200 relays at D = 6, each hop ≈ 30 ms of verification plus network time.
- Contract-visible delivery: p99 ≤ 90 s = 60 s window + 6 s block + about 18 s finality ([doc], `mps-0028…md:36-38`) + indexing.

**Fan-out:** 200 relays × 50 inbound subscriber slots = 10,000 directly connected subscribers at Phase 3. Store-node query throughput is **unknown** and must be load-tested.

## D6 Storage requirements

| Location | What | Size |
|---|---|---|
| Relay | mcache, seen-cache, nullifier map for `Thr` epochs | below 1 GB (**inference**) |
| Store node | envelopes until expiry, at most 7 d (default 24 h) | all shards, 7 d: 120,000 × 604,800 ≈ **72.6 GB**; per shard ≈ 9.1 GB; at peak ×10 |
| Bus Registry state | membership leaves; anchor map for the last 10,080 windows (7 d), oldest pruned on insert; parameters; relay registry | anchors ≈ 10,080 × 40 B ≈ 0.4 MB; leaves 32 B each (Merkle path write cost **unknown**; estimate ≤ 1 KB per registration, i.e. ≤ 0.2 DUST at genesis weights, §7.3) |
| Ledger events | anchor and parameter `Misc` events | churn only; indexer storage |
| Archive | **none by protocol** | applications archive their own decrypted data |

**Availability:**
- Each shard is stored by at least 3 operators in at least 2 jurisdictions.
- Back-fill completeness of at least 99.9% within retention is measured by canaries.
- The persistent budget is 50,000 B per block (`ledger-parameters-config.json:159`). Registrations alone cap near 50 per block, which is fine for this use.

**Governance reason for short retention:** each store node holds at most 7 days of ciphertext that it cannot read. That bounds its legal exposure, its data-protection footprint and the window in which a later key compromise or quantum break could expose stored data.

## D7 Infrastructure actors (lead)

### Actors

| Actor | Role | Admission | Trusted with | Paid by |
|---|---|---|---|---|
| Midnight validators | include registry and anchor transactions | unchanged: 10 permissioned seats (`system-parameters-config.json:6-9`) | liveness, no censorship of bus transactions | n/a |
| Relays | carry envelopes, verify RLN, peer scoring | P2: steward allowlist; P3: bond + evidence-only ejection; P4: bond only | availability, **not** confidentiality | P2 grants; P3+ pool |
| Store nodes | retention, back-fill, delete-by-ID | same as relays | availability; see light-client tags | pool |
| Anchorers | registered relays in round-robin; one anchor per window, enforced by the contract | relay registry | timeliness (a censoring anchorer delays an event by one window) | per-anchor fee |
| Indexers | read path for registry and anchors | none (public or self-run) | correct chain view | existing operators |
| Wallet providers, agents | clients, relayers into contracts | none | user keys stay local | users |
| Application moderators | judge franking reports; app-level blocklists | named in the topic manifest | reported content only | applications |
| Monitors (≥ 3 orgs) | canary probes, scoring input | steward appointment | measurement integrity | pool |
| Measurement share keepers (≥ 3 orgs) | PrivCount-style aggregation | steward appointment | at least one honest | grants |
| Bus Stewards (7 seats) | parameters, registry, pause, maintenance authority | genesis list; ≥ 4 organizations, ≥ 3 jurisdictions, ≤ 2 seats per organization | **no** access to content or identities | none (avoids conflicts) |

### Governance powers (all enforced by the Bus Registry contract; signatures verified in-circuit)

| Action | Threshold | Delay | Expiry |
|---|---|---|---|
| Parameter change (quota, `D_m`, `F_m`, shards, `T_max`) | 5-of-7 | 7 days, at least `T_max` so in-flight events are unaffected | n/a |
| Emergency tighten (quota down, `D_m` up, close one shard) | 3-of-7 | immediate | **7 days** unless ratified 5-of-7 (mirrors `SafeModeForceDuration = 7 * DAYS`, `runtime/src/lib.rs:758`) |
| Bus pause (new registrations and anchors) | 3-of-7 | immediate | 7 days. **Withdrawals and slashing are never pausable** |
| Relay ejection | P2: 5-of-7 with a published reason. P3+: only on evidence (probe failure at or above a threshold over 72 h, or a malformed anchor), 7-day appeal | | |
| Contract upgrade (`ContractMaintenanceAuthority`, `midnight-ledger/spec/contracts.md:20-37`) | 5-of-7 | 14 days' notice; whether Maintain can be time-locked on-ledger is **unknown**, so the notice is social plus a param event | |
| Steward set change | 5-of-7 | 14 days | |

**Outside steward power, by construction:**
- reading content;
- de-anonymizing anyone;
- revoking a membership by fiat (only an RLN proof slashes);
- blocking withdrawals.

This is deliberate. Powers that do not exist cannot be compelled. The model is Tor's: misbehaving infrastructure is removed by a small, accountable authority (2 of 9 directory authorities set BadExit, clients see it within 3 h, `2014-winter-spoiledonions` txt L85-95), while users are never touched.

### Abuse handling

| Abuse | Mechanism | Who acts | What they learn |
|---|---|---|---|
| Flooding or spam | RLN quota, slashing, GossipSub graylisting (`2020-gossipsub-v11-spec` txt L235-238, L628-643) | automatic | only the slashed secret |
| Unwanted contact | recipient allow/deny lists (`2023-xmtp-xip42-consent` txt L15, L44-45); per-message direct tags mean a blocked sender cannot reach the recipient without a new intro, which is rate-limited | recipient | nothing |
| Abusive content in an application | franking report → moderator → app-level ban of the sender's pseudonym or membership commitment, as a signed blocklist enforced by app clients. Phase 4: zk-promises callbacks to ban without linking (`2025-shih-zkpromises` txt L34-40) | moderator | the reported message and pseudonym |
| Illegal content reported from outside | the reporter supplies the event and the franking opening; stewards' legal desk issues a signed **tombstone** for `event_id`; store nodes delete it, relays drop it, and it is auto-gone at expiry anyway | legal desk | the event a reporter already has |
| Malicious relay | canary probes from fresh vantage points (spoiled-onions evasion lesson, txt L346-355), multi-monitor scoring, ejection | monitors, stewards | relay behavior |
| Sybil memberships | `F_m` + `D_m`, tier pricing | parameters | n/a |

**What the protocol cannot do (state publicly):**
- It cannot find content that no recipient reports.
- It cannot scan, and it cannot attribute an event to a person.

Franking has known limits: benign messages can be reported (`2021-issa-hecate` txt L3626-3629), and a moderator cannot prove why it banned someone (`2019-tyagi-messagefranking` txt L1282-1283). Hence app-level, threshold or multi-party moderation is recommended (txt L1284-1290), and protocol bans are excluded.

### Selective disclosure and audit hooks

- **User-held disclosure:** a sender or recipient can reveal one event's content key, its franking opening and an anchor inclusion proof. An auditor or court can then verify the content, sender binding and time. Nothing else is revealed.
- **Compliance recipient:** a regulated application may add its own audit key as a recipient on its topics. This is declared in its manifest and the protocol is neutral to it.
- **Public facts:** publisher-set membership, parameters, slashes and anchors.
- **Rejected:**
  - Master or escrowed viewing keys: a single point of compelled disclosure. They can also be evaded by anyone who surrenders keys while using out-of-band channels (`2026-cinal-viewingkeycompromise` txt L537-541, L687). A delegated detection key retroactively links past and future traffic (`2021-liu-omr` txt L215-229).
  - Traceable mixnets as a protocol feature: their own authors say not to deploy without a query-policy analysis (`2023-agrawal-traceablemixnets` txt L165, L172-176).

### Legal exposure for operators

- Design hygiene:
  - the ledger never holds user content (roots only);
  - off-chain copies expire in ≤ 7 days;
  - operators handle only ciphertext;
  - client IPs are not logged by default;
  - metrics are aggregated (D7 monitoring).
- Every relay and store operator signs an Operator Agreement covering the tombstone SLA (48 h), the abuse and legal contact, and a no-logging default.
- Quarterly transparency report: tombstones, ejections, emergency actions, slashes.
- **Unknown:** whether ciphertext-carrying relays qualify for intermediary-liability protection in each operator jurisdiction, and whether contract-held deposits raise custody issues. A counsel memo for each Phase 2 jurisdiction is a gate (D10), not an afterthought.

### Upgrades and key rotation

| Key or artifact | Rotation | Compromise procedure |
|---|---|---|
| Relay libp2p ed25519 | yearly; signed handover in the registry | steward ejection and re-registration |
| Steward keys (hardware-backed) | yearly | 5-of-7 replacement; the compromised seat is suspended 3-of-7 immediately |
| RLN circuit and Groth16 parameters (public multi-party ceremony, `2022-taheri-waku-rln-relay` txt L199) | new circuit = new envelope version | dual acceptance of N and N−1 |
| Membership root | accept the last 10 roots (≈ 60 s at 6 s blocks; lower bound `Network_Delay/block_time`, `2021-vac-waku2-rln-relay-spec` txt L384) | n/a |
| Topic and pair keys | tags rotate hourly or per message; topic keys rotate on member removal (application or session layer) | application |
| Envelope crypto | version byte; v2 adds a hybrid post-quantum KEM | client deny-list of versions (signed, 3-of-7) |

### Monitoring (privacy-preserving)

1. **On-chain signals, free:** registrations, slashes, anchor gaps per anchorer, parameters, pause state.
2. **Canaries:** at least 3 monitor organizations hold real memberships. Every 60 s, in every shard, they publish and subscribe with real size classes, so canaries look like ordinary traffic. They measure delivery ratio, p50/p99, back-fill completeness and tombstone compliance.
3. **Relay counters** (bytes, events, invalid proofs, graylists) aggregated with PrivCount: at least 3 share keepers, ε = 0.3, 24 h adjacency, at least 24 h between distinct measurements, no IP storage (`2016-jansen-safely-measuring-tor` txt L117-141, L771-782; `2018-mani-tor-usage-privacy-preserving` txt L383-385, L1125-1126).
4. **No per-user telemetry.** Debug logging needs an incident ticket and switches off after 72 h.

### Incident response

| Severity | Examples | Acknowledge | Mitigate |
|---|---|---|---|
| Sev1 | parser remote code execution, crypto break, deanonymization bug | 1 h | 4 h |
| Sev2 | network-wide spam or outage, anchor stall | 2 h | 12 h |
| Sev3 | single relay misbehaving | 24 h | 72 h |

Levers, least invasive first:
1. peer scoring;
2. ejection;
3. emergency tighten;
4. bus pause;
5. client version deny-list.

Last of all, and not ours: Midnight safe mode, which stops *all* user transactions (`check_call_filter.rs` `InherentCalls` comment) and therefore anchors and registrations. The overlay keeps running on cached roots, so a chain incident does not become a bus outage, and a bus incident never needs a chain-level lever.

Other practices:
- Public post-mortem within 14 days.
- Coordinated disclosure (90 days) and a bug bounty.
- Reproducible builds signed by at least 2 stewards.
- Memory-safe parser, continuous fuzzing, and an independent audit before Phase 3. PyBitmessage shipped with no audit and ran an unpatched release line for 8 years (`bitmessage-guide.md:373, 483-488`).

### Path to decentralization

- P2: 7 stewards, permissioned relays (at least 3 operators).
- P3: open admission by bond; ejection by evidence only; the pool replaces grants.
- P4: the maintenance authority moves to Midnight's federated governance (2/3 Council **and** 2/3 Technical Committee, 5-day motions, `runtime/src/lib.rs:789, 907-943`), or the contract is ossified. Stewards keep only the 7-day emergency powers, or lose them by vote. XMTP follows the same path from an owner-run registry to permissionless (`2024-xmtp-xip49-decentralized-backend` txt L437, L454-457).

## D8 Network tether

**Recommendation: hybrid.** Ledger for registry, deposits, parameters, governance and anchors. A **separate libp2p GossipSub v1.1 sidecar** for bulk traffic. The indexer is the read path for anchors.

**Fallback: ledger and indexer only** (Phase 1 mode). Ciphertext of at most 256 B goes in `Misc` with a rotating tag in `name`, read through `contractEvents` (`schema-v4.graphql:1971`). This fallback is permanent and public. Ciphertext on a ledger outlives every key, so its size is capped and the risk stated.

**Rejected: a node fork with a bus protocol** on `sc-network-gossip`.
- It needs every operator to run the fork (§8).
- It shares peer slots with consensus traffic.
- Above all for my role, it couples bus incidents to chain incidents and bus governance to runtime governance.

Separating the blast radius is the reason for my choice.

Also **rejected: inherent-based or off-chain-worker designs.** They are limited to the permissioned committee and not private (§8).

**Changes required:**
- **Node:** none.
- **Indexer:** optional name-prefix filter for `Misc` (filters today cover standard events only, `schema-v4.graphql:558-562`).
- **Wallet and DApp connector:** add `subscribeEvents`.
- **Compact:** none required. MIP-0019 (Proposed) helps the Phase 1 fallback.

**Generation caveat:** `emit` and `contractEvents` belong to ledger 9 / Compact 0.33. The docs list mainnet on ledger-8-era components (`support-matrix.json:14,38,82`). The ledger-9 activation date is **unknown** and blocks Phase 1.

## D9 Threats and open risks

| Threat | Defense | Residual |
|---|---|---|
| Spam at quota via many memberships | `F_m` (non-refundable), tier pricing, emergency tighten | well-funded attacker (`2025-logos-mix-dos-rln` txt L942); medium |
| Invalid-proof flooding | verify before forwarding; graylisting (`2022-taheri-waku-rln-relay` txt L416-422) | CPU cost, 30 ms per proof; medium until benchmarked |
| Slashing front-running or escape | commit-reveal; 7-day withdrawal delay | low |
| Sybil or eclipse on the overlay | permissioned relays in P2; bond in P3; graft diversity across IPs and subnets (`2024-vac-adversarial-models` txt L143-149) | medium in P3+ |
| Reputation framing of relays | several randomized monitors; scores averaged over 72 h; watch for clustered score drops (`2026-cao-nymreputation` txt L1505-1518) | medium |
| Deanonymization by timing | none at launch beyond padding; Dandelion stem and mixing in P4 | **high against GPA**; stated plainly |
| Light-client interest leak | decoy tags; OMR/FMD in P4 | high for light clients until P4 |
| Censorship by validators | 10 permissioned seats; tx-pause and safe mode exist | the overlay survives; anchors and registrations stall |
| Censorship by an anchorer | round-robin; the next window includes the event | one-window delay |
| Steward capture or coercion | 5-of-7 across ≥ 4 organizations and ≥ 3 jurisdictions; time-locks; powers excluded by construction | low for privacy; medium for liveness |
| Compelled operator disclosure | content-blindness; no IP logs; ≤ 7 d retention | metadata held by operators who log in breach of the agreement |
| Key compromise (user) | per-message tags; session ratchets (other designers) | v1 is not post-quantum: harvest-now-decrypt-later for ≤ 7 d store copies plus any copies kept by adversaries |
| Supply chain or parser RCE | reproducible signed builds; memory-safe parser; fuzzing; audit | low to medium |
| Moderator abuse | moderators exist per application, not per protocol; threshold moderators recommended | users choose applications |
| Regulatory shutdown | the abuse story above; transparency reports; counsel memos | **unknown**, the main reason for my lean |

## D10 Build and verification plan (lead)

**Phases and gates.** No phase starts until the previous gate passes.

| Phase | Scope | Gate to exit |
|---|---|---|
| P0: spec and simulation | Quint model of the Bus Registry governance; Tamarin or ProVerif for envelope and franking; network simulation (`2023-beres-ethp2psim`, or a discrete-event simulator as in `2021-diaz-trilemmasimulator`) | all invariants below hold; adversary simulation at p ∈ {0.05, 0.1, 0.2} reports first-spy precision |
| P1: anchored mode (needs ledger 9 on mainnet) | Bus Registry: memberships, parameters, stewards, pause, `Misc` ciphertext ≤ 256 B | 30 days without Sev1; pause→resume drill ≤ 1 h; runbooks rehearsed |
| P2: permissioned overlay | at least 3 relay operators, store nodes, canaries, PrivCount, tombstones | canary delivery ≥ 99.9% with p99 ≤ 5 s for 30 days; 24 h test at 500 ev/s with invalid or over-quota bytes < 1% of ingress under a red team using k = 100 memberships; counsel memos for every operator jurisdiction; independent audit with no open critical or high findings |
| P3: open admission and incentives | bonds, evidence-based ejection, pool payouts | ≥ 20 relays from ≥ 8 operators, none > 20% of relays; ≥ 1,000 memberships and ≥ 20 ev/s organic **before any broadcast anonymity claim is published** |
| P4: stronger anonymity and decentralized governance | Dandelion-style stem, OMR/FMD light clients, zk-promises, maintenance authority to Midnight governance | measured first-spy precision against a 10% coalition is lower than in P3 by the margin set in P0 |

**Invariants to check formally (Quint):**
- I1: no parameter takes effect before its delay.
- I2: every emergency action expires within 7 days unless ratified.
- I3: withdrawals and slashing are callable in every state, including paused.
- I4: at most one anchor per window.
- I5: a membership pays out its deposit at most once (slash or withdraw).
- I6: steward threshold changes need the old threshold.

The RLN commit-reveal slashing race also needs a model.

**Measurable acceptance criteria (beyond the gates):**
- Zero plaintext bytes in relay or store logs (automated audit).
- Tombstone compliance ≥ 99% within 48 h, measured by canary tombstones.
- Report-to-ban median ≤ 24 h in a pilot application.
- Sev1 drills twice a year.
- Cost per 1,000 events and DUST per day published monthly.

**Evidence that would change course:**
1. Counsel finds ciphertext carriage creates operator liability in core jurisdictions. Then keep relays steward-run in safe jurisdictions, or stop at P1.
2. RLN verification cannot reach ≤ 5 ms per proof with batching. Then move to fewer, larger shards with stake-based relays, or to a midnight-zk circuit if benchmarks favor it.
3. Organic load stays below 5 ev/s six months into P2. The anonymity set is then too small: fund cover traffic or drop the privacy claims.
4. Moderator report volume overwhelms pilot applications. Then evaluate threshold reporting (`2023-eskandarian-abusereporting`).
5. Midnight governance uses safe mode often. The bus then needs a non-ledger membership path.
6. Ledger 9 slips. Then P2 starts with a test-ledger registry, but no mainnet claims.

---

## Decision table

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 Event format | 304-byte fixed header; 4 padded classes (512 B–32 KiB); RLN fields; sealed body with franking slot; expiry ≤ 7 d (ceiling 14 d) | variable sizes; on-chain ciphertext by default; dynamic type dispatch | `2021-vac-waku2-rln-relay-spec` L327-330; `2017-grubbs-franking`; `2021-issa-hecate` Table 4; `bitmessage-guide.md:352-358`; `ledger-parameters-config.json:176` | medium | proof-size or bandwidth benchmarks favor a different RLN system |
| D2 Private | P1–P9 with the leakage table; GPA and post-quantum out of scope at launch; report-only disclosure | claiming GPA resistance; escrowed disclosure | `2022-taheri-waku-rln-relay`; `2024-aztec-private-events-note-discovery` L516; `2021-issa-hecate` L327-328 | high | measured anonymity sets far smaller than modeled |
| D3 Pub/sub | PRF tags (hourly or per-message), 8 shards, local filtering, intro inbox, anchors plus a relayer for contracts, wallet `subscribeEvents` | global topic directory; per-topic subscriptions at relays; contracts reading events | `2024-aztec-private-events-note-discovery` L417; `2024-cornelius-waku-network-dapps` L54-61; `notes/midnight-network-stack.md` §5.4, §9.12 | medium | OMR/FMD costs fall enough for P2 light clients |
| D4 Sustainable | RLN-v2 memberships with deposit, non-refundable fee and tiers; grants → pool paid on probe scores, capped at 1/k; one rotating anchorer, ≈ 86 DUST/day | PoW admission; deposit-only; stake-weighted selection with one monitor | `2004-laurie-proofofwork`; `2022-taheri-waku-rln-relay` L488-503; `2021-diaz-nym` L1685; `2026-cao-nymreputation`; notes §7.3 | medium | live DUST prices or a shielded-deposit path change the cost or privacy balance |
| D5 Performance | 50 ev/s sustained, 500 peak; relays ≤ 2 shards; overlay p99 ≤ 5 s; contract-visible p99 ≤ 90 s | all-shard relays as the default | `2020-gossipsub-v11-spec` L553; `2022-taheri-waku-rln-relay` L428-430; `mps-0028` L36-38 | low (loads assumed) | P2 measurements |
| D6 Storage | store nodes keep ≤ 7 d (72.6 GB all shards at launch); ≥ 3 operators per shard; ledger holds roots only; no protocol archive | long retention; on-ledger payloads | `bitmessage-guide.md:431-447`; `ledger-parameters-config.json:159` | medium | applications prove a need for longer back-fill |
| D7 Actors and governance | 7 stewards with time-locks and 7-day emergency expiry; powers excluded by construction; app-level moderation by franking; tombstones; PrivCount monitoring; handover to Council+TC or ossification | protocol bans; key escrow; traceable mixnet; single central monitor; node-fork operators | `runtime/src/lib.rs:758, 789, 907-943`; `2014-winter-spoiledonions` L85-95; `2016-jansen-safely-measuring-tor`; `2026-cinal-viewingkeycompromise`; `2023-agrawal-traceablemixnets` L172-176; `2024-xmtp-xip49-decentralized-backend` L437-457 | medium-high | counsel requires operator-side capabilities the design cannot give without breaking P7/P8 |
| D8 Tether | hybrid: sidecar libp2p GossipSub plus ledger registry and anchors; fallback ledger+indexer; no node change | node fork with `sc-network-gossip`; inherents or off-chain workers; ledger-only as the end state | notes §1.5, §8, §9.10; `schema-v4.graphql:558-562`; `api.ts:70-203` | high | Midnight ships a supported plugin protocol slot with separate peer budgets |
| D9 Threats | table above; GPA timing and light-client interest leak are the main residuals | n/a | `2024-vac-adversarial-models`; `2025-logos-mix-dos-rln` L942; `2026-cao-nymreputation` | medium | red-team results in P2 |
| D10 Plan | P0–P4 with gates, Quint invariants I1–I6, Tamarin/ProVerif, simulation, legal memos and audit as gates, anonymity claims gated on load | big-bang launch; claiming privacy before the anonymity set exists | `2018-mani-tor-usage-privacy-preserving` L383-385, L1808-1815; `bitmessage-guide.md:373` | high | the course-change triggers listed in D10 |
