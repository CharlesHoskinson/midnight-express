I recommend an agent-first, capacity-capped private event overlay, with Midnight used for authorization and explicit contract interactions. Preserve Bitmessage’s recipient-oblivious delivery, but replace static message keys and flat proof-of-work. Treat content confidentiality, subscriber-interest privacy and publisher anonymity as separate properties. Ordinary gossip does not meet our intermittent global-observer threat model; a padded mix path should remain experimental until independently tested. My principal D9 position is to block any claim of strong relationship privacy based solely on encryption, flooding, Dandelion++ or relay diversity.

## D1 — Event format

**Proposed requirements; numerical defaults are assumptions pending measurement.**

Use one common dissemination domain per Midnight genesis hash. No public application topics, recipient addresses, sender keys, contract addresses or stable session identifiers appear in the transport envelope.

One event occupies a **4,096-byte cell**:

| Area | Bytes | Relay-visible contents |
|---|---:|---|
| Fixed header | 128 | Magic, protocol version, cryptographic suite, genesis hash, admission epoch, expiry, random nonce, reserved padding |
| Admission area | 1,152 | Authorized membership root, nullifier, RLN share, bounded proof and padding |
| Protected data | 2,816 | Encrypted session header, authenticated payload and padding |

The proof must fit the admission area; reject oversized proofs before allocating proportional memory. Define one canonical binary encoding, fixed field widths and zero-valued reserved bytes. Authenticate the immutable header and protected data together. Bind the admission proof to their hash, excluding the proof itself. Define the transport identifier as a domain-separated hash of that canonical, proof-independent event representation.

**Inference:** excluding proof serialization from the identifier prevents alternative proofs for the same event from defeating deduplication. Admission nullifiers separately prevent an attacker from changing the nonce to obtain another accepted event for the same allowance.

Inside encryption place: application protocol and schema versions, logical event identifier, authenticated publisher, channel, sequence number, predecessor commitment, creation and expiration times, payload type, payload, and optional contract authorization or receipt. Supported payloads are bounded application data, acknowledgements, session/group control and contract-call authorization. Never execute payload-supplied code or automatically fetch attachments.

Retain accepted cells for **48 hours**, with no sender-selected extension. Larger objects require a separately authorized transfer; a sealed reference does not make the referenced object available.

Pairwise sessions use the **header-encryption Double Ratchet variant**. The specification explicitly addresses hiding session association and ordering through encrypted headers, while leaving session discovery to the application. Use authenticated, pre-established sessions for the first release; do not invent a public-key discovery protocol. [Literature: `2016-signal-double-ratchet-spec`, §4.1.]

Groups use MLS later, inside an additional metadata-hiding wrapper. MLS alone exposes group IDs, epochs and other metadata. A shared group wrapper key is for recognition and metadata concealment; it must not replace MLS authentication or per-message keys. [Literature: `2023-barnes-rfc9420`, §§16.4–16.6.]

**Rejection:** static-key ECIES and passphrase-derived shared identities. The original Bitmessage design supplies flooding, trial decryption and offline retention, but these transport ideas do not establish forward secrecy. [Literature: `2012-warren-bitmessage-whitepaper`, §§3–7; `2016-signal-double-ratchet-spec`, §§2, 8.1.]

## D2 — Definition of “private”

**Threat assumptions:** motivated attackers control 1–5% of relay identities in normal experiments, can concentrate resources on particular users, acquire publisher allowances, run indexers and application endpoints, and observe the entire network on some days. Node share, bandwidth share, operator share and publisher-allowance share are different quantities.

The release makes these distinct claims:

- **Content confidentiality and integrity:** against relays, indexers and network observers, conditional on authenticated session establishment, uncompromised endpoints and the cryptographic assumptions of the selected suite.
- **Subscriber-interest privacy:** whole-feed retrieval contains no topic or recipient filter. This is a protocol-level property conditional on retrieval schedules and application reactions being independent of matches.
- **Topic privacy:** topics are sealed. Known publishers, insiders, contract commitments and application behavior can still reveal topic associations.
- **Publisher unlinkability:** ordinary gossip offers no strong guarantee. The mix profile is a separate experimental claim.
- **Timing, volume and relationship privacy:** no general release guarantee. Fixed download schedules conceal some activity differences, but source traffic and application effects remain observable.
- **Forward secrecy and recovery:** conditional on key deletion and fresh uncompromised updates. Persistent device compromise and suppression of updates defeat recovery. [Literature: `2016-signal-double-ratchet-spec`, §§8.1–8.4; `2023-barnes-rfc9420`, §§16.6, 16.9.]

**Proposed leakage table; entries describe the design, not a proved anonymity theorem.**

| Observer | What it learns |
|---|---|
| Relay | Neighbor IPs and identities; arrival times; cell bytes, IDs, epochs, expiry, admission roots and nullifiers; local forwarding behavior. Direct ingress exposes the submitting endpoint. |
| Bus store/gateway | Client IP or proxy, connection schedule, whole-feed intervals requested, catch-up volume and service account. It receives no message or detection key. |
| Midnight indexer | Queried contract addresses and filters; chain metadata. A server-assisted wallet path can disclose its viewing key. |
| Chain observer | Enrollment/checkpoint activity; contract address and entry point; disclosed transcripts, commitments and public fee information. It does not obtain off-chain plaintext merely from the bus. |
| Colluding minority | Combined relay observations, targeted connection control, selective dropping and admission equivocations. It can attempt topology learning and first-spy classification. |
| Global observer | Participation, online intervals, traffic timing and volume, direct publication sources, payment/enrollment correlations and downstream actions. Mix-profile correlation resistance remains unproved for this construction. |

Midnight’s indexer requires a contract address for `contractEvents`; its wallet-assisted architecture stores viewing keys. Contract calls contain addresses, entry points and transcripts, and DUST spends expose `v_fee`. [Code: `midnight-indexer/indexer-api/graphql/schema-v4.graphql:548`; `midnight-indexer/docs/architecture.md:20`; `midnight-ledger@ledger-9.1.0.0-rc.5/ledger/src/structure.rs:2646`; `midnight-ledger@ledger-9.1.0.0-rc.5/ledger/src/dust.rs:469`.]

**Out of scope:** anonymity from intended recipients or authorized group members; hiding participation; compromised devices; indefinite archival secrecy; guaranteed delivery during partition; and concealment of public contract effects.

Do not apply the anonymity trilemma as a numerical proof for this asynchronous overlay. Its bounds demonstrate necessary latency/bandwidth tradeoffs within its model, not sufficient security for our parameters. [Literature: `2017-das-trilemma`, §§I, III–IV.]

## D3 — Publish and subscribe model

**Proposed requirements.**

A subscription is local possession of authenticated session or group state. Consumers retrieve the common feed and recognize messages locally. Discovery uses authenticated invitations outside the bus, identifying the application, publisher and expected keys. No directory query should return “who subscribes to topic X.”

Wallets and agents use the same feed protocol. They persist transport deduplication state and application processing state separately. Default behavior generates no immediate acknowledgement; optional acknowledgements are encrypted events subject to the normal publication policy.

Delivery is **best-effort, at-least-once within retention**, with:

- Per-publisher logical sequencing; no global event order.
- Duplicate suppression by transport ID and authenticated logical ID.
- Bounded out-of-order processing; missing sequences become explicit gaps.
- Whole-interval backfill, never selective retrieval of matching IDs.
- Exact-cell retransmission during its live admission window.
- Later retries using a fresh allowance but the original authenticated logical ID.

Bound skipped-key storage and delete expired keys. The Double Ratchet specification identifies both memory exhaustion and later-compromise risks from retained skipped keys. [Literature: `2016-signal-double-ratchet-spec`, §8.4.]

A **smart contract consumes through a submitted transaction**. An off-chain agent supplies the event as witness data. The circuit must verify an authorized publisher signature over the payload, genesis, target contract, allowed action, logical ID and expiry; enforce its application predicate; and consume a replay nullifier atomically with the effect.

A witness is a callback controlled by the application, not an authenticity guarantee. Compact provides signature verification functions that must be asserted, and its documented authorization example explicitly binds the witness path to the secret key. [Code: `minokawa-compact/doc/compact-reference.mdx:1153`; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:921`; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:996`; `midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:209`.]

**Inference:** a signed off-chain statement proves authorization by that key, not the truth of an arbitrary ledger event. Applications requiring ledger provenance must verify it through application-specific committed state or a separately reviewed receipt mechanism. Generic private proofs of indexed event inclusion are **unknown** here.

Contract publication has two explicitly different semantics:

1. An application agent publishes an off-chain attestation.
2. A contract commits to the encrypted object during execution, and an agent distributes it afterward.

**Inference:** the second binds provenance but exposes the originating contract and can link the cell to that action. Label this leakage in the API.

## D4 — Sustainable model

**Proposed launch model:** prepaid service agreements fund relay bandwidth, retrieval and 48-hour storage. Publishers buy uniform admission leases; subscribers buy retrieval capacity. Launch subsidy pays for low-load cover traffic. Actual operating prices are **unknown** until benchmark and operator quotes exist.

Use **RLN-style anonymous admission**, with a dedicated admission secret that is never a wallet, identity or message key. Initially allow **300 active credentials**, each permitted one cell per **30-second epoch**: nominal maximum `300 / 30 = 10 cells/s`.

The registry authorizes exactly one bounded membership snapshot for each epoch. Nullifiers are independent of membership-root changes, preventing an allowance reset through root rotation. Accept only current or immediately previous epochs. Every relay verifies message binding, membership and epoch validity, then forwards at most one event per nullifier.

RLN exposes an admission secret after conflicting signals and supports detection and economic punishment in its Waku construction. Its concrete paper uses Groth16 and an Ethereum registration/slashing contract; that mechanism is not already supplied by Midnight. [Literature: `2022-taheri-waku-rln-relay`, §§II-B, III-D–F.]

**Launch limitation:** charge for leases and revoke proven equivocators from future snapshots; do not promise automatic slashing. A transferable deposit, evidence validation and safe payout contract require separate design. Conflicting signals can reach different honest relays before detection, so this is a local bound rather than instant global serialization.

Before proof verification impose fixed frame limits, bounded queues, per-connection verification budgets and connection admission limits. Valid proofs do not protect against a flood of invalid proofs.

Use DUST for Midnight transactions only. DUST is documented as non-transferable gas capacity derived from NIGHT; it cannot be the relay payment token. Its generation ratio, rate and grace period appear in the node parameters. [Code/documentation: `midnight-docs/docs/concepts/dust-architecture.mdx:21`; `midnight-docs/docs/concepts/dust-architecture.mdx:102`; `midnight-node/res/mainnet/ledger-parameters-config.json:164`.]

Ledger fees depend on normalized read, compute, block usage, writes and churn, with prices updated from fullness. Quote enrollment and contract-consumption costs against actual ledger parameters. Never present genesis values as live prices. [Code: `midnight-ledger@ledger-9.1.0.0-rc.5/base-crypto/src/cost_model.rs:354`; `midnight-ledger@ledger-9.1.0.0-rc.5/base-crypto/src/cost_model.rs:408`.]

**Rejection:** flat proof-of-work as the principal economic defense. Laurie–Clayton demonstrates the tension between honest-user cost and stolen attacker compute; its historical monetary figures are not contemporary estimates. [Literature: `2004-laurie-proofofwork`, §§2–4.]

## D5 — Performance requirements

**All figures are proposed targets or arithmetic on assumptions, not measured capacity.** Count control traffic, duplicate transmission, cover traffic, backfill and proof verification separately.

Launch assumptions: 10 admitted real cells/s, capacity for 20 unique cells/s during recovery, 4,096-byte cells, 10,000 concurrent subscribers, and 20 gateways serving 500 subscribers each.

| Node class | Required capacity and budget |
|---|---|
| Validator | No mandatory bus traffic, storage or verification. |
| Dedicated relay: 4 cores, 8 GB RAM, 1 Gbit/s | 20 unique cells/s; 48-hour retention; independently limited verification queues. |
| Retrieval gateway: 8 cores, 16 GB RAM, 1 Gbit/s | 500 subscribers at 20 padded cells/s; bounded backfill queues and authenticated interval manifests. |
| Agent/desktop client | 81,920 bytes/s live download; at most 32 active subscriptions initially; bounded recognition and skipped-key work. |
| Experimental mix | Separate process and budget; no sharing of consensus keys or validator worker pools. |

Arithmetic:

- Subscriber feed: `20 × 4,096 = 81,920 bytes/s`, or **7.078 GB/day**.
- Gateway payload: `500 × 81,920 = 40.96 MB/s`; with an assumed 25% overhead, **51.2 MB/s**, or **409.6 Mbit/s**.
- Network subscriber payload: `10,000 × 81,920 = 819.2 MB/s`, or **6.554 Gbit/s**, before overhead.
- Relay budgeting example: six payload copies in each direction gives `12 × 20 × 4,096 = 983,040 bytes/s`; adding 25% gives **1.229 MB/s** aggregate traffic.
- Proof-verification target: at most **5 ms** per valid admission proof on the reference relay. At 20/s that consumes **0.1 CPU core**; invalid-proof work receives a separate hard budget.

Latency targets, measured from first honest ingress to client delivery: **p50 ≤5 s, p95 ≤20 s, p99 ≤35 s**, including a synchronized 300-publisher epoch burst. Mix-profile target: **p99 ≤90 s**, measured separately. Contract execution adds proving, transaction inclusion, finality and indexing; no universal contract latency promise.

The node targets six-second slots, has a 1 MiB block-length configuration and separate ledger budgets including 1,000,000 bytes of block usage and 50,000 persistent bytes. These do not establish event-bus throughput. [Code: `midnight-node/runtime/src/lib.rs:292`; `midnight-node/runtime/src/lib.rs:312`; `midnight-node/res/mainnet/ledger-parameters-config.json:155`.]

For an illustrative mix experiment, 1,000 online clients send scheduled replacement-or-dummy packets at `1/30 s` and loops at `1/60 s`; 30 mixes generate loops at `1/10 s`. That is approximately **53 packets/s**. Assuming five link transfers per route and 8,192-byte padded packets, traffic is `53 × 5 × 8,192 ≈ 2.171 MB/s`, before retransmissions. These parameters require security analysis; Loopix’s use of Poisson scheduling, loops and padded pulls is evidence for the mechanisms, not these settings. [Literature: `2017-piotrowska-loopix`, §§3.1–3.3.]

**Scaling boundary:** at 100 real cells/s, each full-feed client receives **35.389 GB/day**, before recovery overhead. Do not solve this by quietly revealing application topics. Mobile delivery requires a separately verified retrieval profile.

## D6 — Storage requirements

**Proposed requirements and calculated budgets.**

Conservatively provision accepted-cell storage at 20 cells/s:

- 48-hour payload: `20 × 172,800 × 4,096 = 14.156 GB`.
- Assuming 128 bytes of index data per cell: **442 MB**.
- Reserve **32 GB per relay** for payloads, indices, database overhead, manifests and bounded recovery buffers.
- Seven-day optional archive: `20 × 604,800 × 4,096 = 49.545 GB`, before overhead.

Gateway-generated padding need not be persisted. Ordinary relays prune by authenticated protocol expiry, not access time or sender request. An archive accepts a separately paid, bounded retention agreement; archiving cannot renew an event’s eligibility for contract execution.

Live admission permits are short-lived. Backfill validates historical admission against the appropriate registry snapshot, without treating the cell as a fresh publication. Archive queries and live ingress have separate budgets.

Publishers obtain signed storage receipts from three independently selected operators. These receipts identify object, retention deadline and operator. **Inference:** they make promises attributable; they do not prove continued availability or operator independence.

Availability is conditional: retrieval succeeds while at least one reachable honest holder retains the object and the client has enough catch-up capacity. A partition longer than retention loses this guarantee. No unconditional delivery or deletion guarantee is claimed.

Put enrollment configuration, application commitments and necessary consumption replay state on the ledger. Keep cells, relay indices and plaintext off it. Rotate bounded replay buckets only after the circuit makes old events permanently ineligible; never delete replay state while an old authorization remains usable.

Ledger-9 `log` arguments may reach 512 KiB, but emitted events over 1 KiB are silently swallowed; logs charge churn. Compact’s custom `Misc` event has only a 32-byte name and 256-byte payload. Those are reasons to use a small commitment rather than ledger-carried bulk cells. [Code: `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:38`; `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:268`; `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:595`; `minokawa-compact/compiler/midnight-events.ss:71`.]

## D7 — Infrastructure actors

**Proposed admission and trust model.**

- **Validators:** retain existing consensus responsibilities. They authorize registry transactions and contract execution, not off-chain delivery.
- **Relays/stores:** accept and retain valid cells. Trusted for availability only; never receive content keys.
- **Gateways/wallet providers:** supply the entire feed. Learn participation and service-account metadata, but receive neither topic filters nor detection keys.
- **Agents:** decrypt, validate application policy and submit authorized contract calls. Their signatures and circuit constraints determine their authority.
- **Mix operators:** transform packets and add delays/cover traffic. Separate keys, administration and processes from bus stores wherever practical.
- **Registry administrators:** control launch capacity and admission. Their censorship power is explicit.
- **Archives:** optional paid storage outside the default delivery guarantee.

Launch with a small published operator roster and explicit trust disclosure. Require authenticated peer records, independently maintained bootstrap lists, outbound connections and operator/network diversity. Reserve exploratory connections so accumulated scores cannot permanently lock a node into attacker peers.

GossipSub v1.1 specifies outbound mesh quotas, explicit peers and opportunistic grafting. Its audit documents score manipulation and discovery-dependent vulnerabilities. Use these mechanisms as tested resilience tools, not proofs of honest peer sampling. [Literature: `2020-gossipsub-v11-spec`, “Outbound Mesh Quotas,” “Explicit Peering Agreements,” “Opportunistic Grafting”; `2020-leastauthority-gossipsub-audit`, Issues A–D.]

**Inference:** open relay IDs do not establish independent operators, and paid publisher admission does not solve relay Sybils. Douceur’s analysis rules out treating self-created identities as dependable independent entities without additional assumptions. [Literature: `2002-douceur-sybil`, §§1–3.]

Decentralization means removing the administrator’s discretionary membership authority through audited, resource-priced enrollment and verifiable capacity rules. Admission caps remain necessary. Publish operator concentration and availability measurements; do not declare decentralization from node count alone.

## D8 — Network tether

Choose a **hybrid: independent libp2p overlay for bulk delivery; Midnight contracts for authorization and application commitments**.

Use GossipSub resilience features within the common bus domain. Suppress application-level public author/sequence metadata; authenticate application publishers inside encryption. Normal clients must not accidentally bypass the selected ingress profile through direct flood publication.

Keep the bus outside the node’s consensus network and resource pools. Midnight currently registers GRANDPA, BEEFY and ledger-sync protocols through its network service. The ledger-sync implementation itself warns that costly service work can compete with authoring/finality. [Code: `midnight-node/node/src/service.rs:574`; `midnight-node/node/src/service.rs:610`.]

Required changes:

- New relay/gateway sidecar and client event SDK.
- Wallet integration for local session state and whole-feed retrieval.
- Compact application contracts for registry authorization and checked event consumption.
- No mandatory node fork or new indexer event transport.
- Self-run or independently checked chain access for security-critical registry state.

**Fallback:** one common ledger announcement contract containing small encrypted objects or commitments, retrieved without application-specific filters. Explicitly label its public contract/activity linkage and restricted throughput.

Generation matters. The local node identifies ledger 9.1.0.0-rc.5 dependencies, while the support matrix lists Compact 0.31.1 for mainnet. Compact 0.33 release notes introduce ledger 9 and events. **Unknown:** activation on the actual deployment; verify it before enabling any event-dependent path. [Code/documentation: `midnight-node/Cargo.toml:472`; `midnight-docs/docs/relnotes/support-matrix.json:38`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`.]

Indexer subscriptions backfill and then follow indexed blocks. They are a delivery API, not an independently verifiable completeness proof. [Code: `midnight-indexer/indexer-api/src/infra/api/v4/subscription/contract_event.rs:98`; `midnight-indexer/docs/architecture.md:15`.]

## D9 — Threats and open risks

The following ranking is **red-team inference**, conditional on the stated adversary. “Low cost” means little marginal expenditure after obtaining the assumed observation or endpoint access; it is not a dollar estimate.

| Priority | Attack and impact | Attacker cost | Defense and residual risk |
|---|---|---|---|
| 1 | **Malicious contract/agent accepts forged data:** unauthorized state changes | Low if validation is defective | Bind signature to genesis, target, action, payload and expiry; assert authorization and consume replay state atomically. A circuit proves only its implemented predicate. |
| 2 | **Indexer or discovery substitutes keys:** content interception and impersonation | Low with service control | Authenticated invitations, pinned identities, explicit key changes. Initial authentication remains a trust boundary. |
| 3 | **Global timing correlation:** identify publishers and relationships | Low marginal cost on observer days | Mix ingress, scheduled client traffic and delayed effects. Ordinary gossip remains exposed; experimental profile has no inherited theorem. |
| 4 | **Endpoint compromise:** plaintext, impersonation and future surveillance | Variable; no large node fraction needed | Separate keys, secure deletion, reauthentication and fresh ratchet updates. Persistent compromise defeats recovery. |
| 5 | **Targeted eclipse/Sybil capture:** censorship, stale views and source attribution | Medium; targeted resources outperform random placement | Multiple bootstrap sources, outbound quotas, retained honest peers and exploratory connections. ASN/operator diversity is only a heuristic. |
| 6 | **Proof-verification flood:** CPU exhaustion before admission | Low to medium | Fixed frames, cheap checks, bounded verification queues and fair scheduling. Distributed connection floods remain possible. |
| 7 | **Allowance saturation/storage exhaustion:** consume all paid capacity | Cost of leases; motivation may exceed economic deterrence | Hard enrollment/retention caps and paid bandwidth. Valid traffic can still crowd out useful traffic. |
| 8 | **Operator/registry censorship:** drop cells or refuse admission | Low for controlling operators | Multi-store receipts, alternative operators and explicit administrator trust. Receipts cannot force service. |
| 9 | **First-spy and topology learning:** link repeated publications | Low with a few well-placed relays | Mix before gossip; keep direct ingress separately labeled. Dandelion++ is insufficient for the global-observer claim. |
| 10 | **Selective-feed tagging/indexer abuse:** give a victim unique omissions and observe reactions | Low with gateway control | Compare whole-interval manifests from independent sources; avoid immediate match-triggered traffic. Signatures authenticate a manifest, not its completeness. |
| 11 | **Replay, proof malleability, cross-chain reuse:** duplicate effects or resource use | Low | Proof-independent IDs, genesis binding, epoch nullifiers, logical deduplication and contract replay checks. Restart recovery must preserve these properties. |
| 12 | **RLN equivocation/key extraction:** expose admission identity and partition delivery | One credential plus conflicting proofs | Dedicated admission keys; evidence-based revocation; conflicts trigger alarms. Never reuse the RLN secret for message encryption. |
| 13 | **Suppressed ratchet/MLS updates:** prolong a compromise | Low with delivery control | Detect missing updates, impose update age limits and stop sensitive sends. Availability attacks can prevent recovery. |
| 14 | **Mix replay or tagging:** correlate routes and amplify work | Low with packet access | Audited packet format, per-hop replay caches, bounded lifetime and coordinated key/cache rotation. Restart handling is security-critical. |
| 15 | **Group insider:** leak plaintext, membership or forge application claims | Membership access | Individual authenticated keys and checked application roles. No protocol can prevent an authorized recipient copying plaintext. |

Relevant evidence:

- Eclipse attacks monopolize a victim’s connections through address poisoning; random node-fraction calculations are inadequate for targeted attacks. [Literature: `2015-heilman-eclipse`, §§1, 3–6.]
- Dandelion++ studies Byzantine spy nodes but explicitly places ISP/AS-level adversaries outside its scope. [Literature: `2018-fanti-dandelionpp`, §3.1.]
- Loopix includes global observation and malicious mixes, but excludes unrestricted client Sybils and assumes conditions on providers. We must supply our own enrollment and gateway analysis. [Literature: `2017-piotrowska-loopix`, §§2.2–2.3.]
- MLS delivery-service compromise permits selective suppression, including suppression that defeats post-compromise recovery. [Literature: `2023-barnes-rfc9420`, §16.9.]
- Mix restart protection requires either persistent replay state or destruction of the associated routing keys. [Literature: `spec-katzenpost-packetreplay`, “System overview,” pp.2–3.]
- Midnight safe mode deliberately permits filtering user transactions. Mainnet configuration lists ten permissioned and zero registered candidate seats. Thus ledger-dependent enrollment and consumption inherit an explicit censorship/liveness boundary. [Code: `midnight-node/runtime/src/check_call_filter.rs:39`; `midnight-node/res/mainnet/system-parameters-config.json:6`.]

**Red-team blocks:**

1. Strong global-observer privacy without an analyzed traffic policy.
2. “Few-percent attacker” claims based on nominal peer count.
3. Contract execution authorized by unverified witness or indexer output.
4. Silent fallback from mix ingress or whole-feed retrieval.
5. Unbounded state, proof queues, historical retrieval or skipped-key retention.

Reject FMD as an unnoticed mobile shortcut: its detection server obtains an approximate matching set, rather than oblivious retrieval. Investigate OMR/PIR separately, including malformed-input and retrieval denial-of-service behavior. [Literature: `2021-beck-fmd`, §1; `2021-liu-omr`, Abstract, §§4.2, 8.]

## D10 — Build and verification plan

**Proposed gates; acceptance thresholds are assumptions to be reviewed before implementation.**

**Phase 0 — security model and simulations.**

Model authorization, root transitions, epoch boundaries, conflicting nullifiers, restarts, expiry and contract replay. Formally check that no unauthorized event causes a contract effect, no logical event causes the same effect twice, and no root transition resets an allowance.

Simulate random and targeted adversaries at 1%, 3% and 5% relay share, plus concentrated bandwidth, compromised gateways, poisoned bootstrap lists and synchronized publishers. Sweep publisher-allowance share independently. Measure eclipse duration, delivery tails, omissions, storage growth and classifier precision/recall.

**Phase 1 — bounded agent pilot.**

Ship pairwise sessions, capped anonymous admission, whole-feed retrieval and storage receipts. Run the D5 workload for seven days, including restart and network partitions. Acceptance requires:

- D5 latency and bandwidth budgets at the specified load.
- Storage remains within the 32 GB relay provision.
- Invalid traffic cannot expand queues or caches beyond configured limits.
- At least 99.9% of honest publications reach honest clients within 35 seconds in the declared connected test topology.
- Zero unauthorized or duplicate contract effects in the model and adversarial test suite.
- Recovery from one failed gateway/store while another honest holder remains reachable.

Keep these test results scoped to their topology and workloads.

**Phase 2 — independent cryptographic and parser review.**

Audit admission message binding, proof setup/verifier, session initialization, encrypted headers, serialization, key separation and restart persistence. Fuzz all unauthenticated parsing. Verify that malformed application payloads cannot trigger downloads, commands or unbounded cryptographic work.

**Phase 3 — experimental global-observer profile.**

Introduce a reviewed Sphinx-based mix transport with delays, client replacement traffic, loops and replay protection. Sphinx supplies packet transformations and active-attack protections; it does not choose a sufficient traffic policy. [Literature: `2009-danezis-sphinx`, §§1–2; `2017-piotrowska-loopix`, §§3–4.]

Test low traffic, repeated conversations, churn, observation-day intersections, compromised ingress/egress and selective dropping. An initial empirical gate is classifier advantage ≤0.05 in preregistered balanced challenges with confidence intervals. Passing is evidence for those experiments, not cryptographic proof.

**Phase 4 — groups, mobile retrieval and open admission.**

Add MLS only after group-state forks, membership authentication and update suppression tests. Compare whole-feed retrieval with a reviewed OMR/PIR construction under malicious-server and overload conditions. Remove discretionary enrollment only after funding, capacity and resource-priced admission are concrete.

Change course if publisher attribution remains effective, independent retrieval sources repeatedly disagree, proof verification exceeds its budget, subscriptions cannot fund replication, or target clients cannot afford whole-feed bandwidth. Revisit architecture before weakening advertised privacy.

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Fixed 4 KiB cells; sealed metadata; header-encrypted ratchets | Static recipient keys; visible application topics; arbitrary bulk envelopes | `2016-signal-double-ratchet-spec` §4; `minokawa-compact/compiler/midnight-events.ss:71` | Medium | Audited proof/session formats cannot fit, or recognition costs exceed budget |
| D2 | Separate confidentiality, interest privacy and anonymity claims | Undifferentiated “private”; inherited global-observer guarantees | `2017-das-trilemma` §§I–IV; `2023-barnes-rfc9420` §16.4 | High | A security proof covers the actual composition and traffic policy |
| D3 | Local subscriptions; whole-feed backfill; checked transaction consumption | Remote topic filters; automatic contract subscriptions; unchecked witnesses | `minokawa-compact/doc/compact-reference.mdx:1153`; `2016-signal-double-ratchet-spec` §8.4 | High | A verified private retrieval or ledger-receipt mechanism becomes available |
| D4 | Paid service leases plus capped anonymous admission; DUST for chain gas | Flat PoW; DUST relay payments; assumed native slashing | `2022-taheri-waku-rln-relay` §§II–III; `midnight-docs/docs/concepts/dust-architecture.mdx:23` | Medium | Reviewed deposits/slashing and operator economics support open enrollment |
| D5 | Agent-first 10 cells/s launch; explicit 20 cells/s recovery budget | Unmeasured throughput claims; mobile full-feed default | Arithmetic assumptions; `midnight-node/runtime/src/lib.rs:292` | Medium | Benchmarks or client economics invalidate the budgets |
| D6 | 48-hour bounded storage; optional paid archives; small ledger commitments | Permanent universal retention; bulk ledger storage | `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:268` | High | Offline-use requirements justify a funded longer window |
| D7 | Dedicated operators with explicit launch trust and measured diversity | Validator mandate; peer-count decentralization | `2002-douceur-sybil` §§1–3; `2020-gossipsub-v11-spec`, outbound quotas | Medium | Verifiable resource-priced admission supports less discretionary trust |
| D8 | Independent overlay plus ledger authorization; ledger fallback | Consensus-network integration; ledger/indexer-only bulk bus | `midnight-node/node/src/service.rs:610`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22` | High | An isolated native extension demonstrates operational benefit |
| D9 | Block unsupported anonymity and authorization claims; test targeted attacks | Random-fraction reasoning; Dandelion-only global privacy | `2015-heilman-eclipse` §§3–6; `2018-fanti-dandelionpp` §3.1; `2017-piotrowska-loopix` §2 | High | Independent analysis and attack experiments cover each claimed adversary |
| D10 | Model first; bounded pilot; independent audit; experimental mix; later retrieval/groups | Combined unaudited production launch | Proposed gates; `spec-katzenpost-packetreplay` pp.2–3; `2023-barnes-rfc9420` §16.9 | High | Evidence shows a simpler construction meets the same explicit properties |