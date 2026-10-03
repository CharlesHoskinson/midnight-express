I recommend a bounded, capability-based event bus with end-to-end encryption, one common dissemination feed, and recipient-side recognition. Its initial privacy claim should be **content confidentiality and subscriber-interest privacy conditional on identical fetching behavior**, not publisher anonymity or communication unobservability. Bulk ciphertext belongs in a separate overlay; Midnight supplies authorization, settlement and application commitments. Full-feed reception deliberately pays bandwidth to avoid revealing interests. Mixnet publishing and private retrieval are later, separately verified profiles. I would block any specification that describes gossip, rotating tags, fuzzy detection or public contract logs as providing strong anonymity without the corresponding adversary model and proof.

## D1 — Event format

**Proposal; all format choices and limits below are design assumptions.**

Use one fixed **4,096-byte cell**, comprising:

| Component | Size | Visibility |
|---|---:|---|
| Fixed header | 128 bytes | Protocol version, cryptographic profile, network identifier, admission epoch, fresh nonce, reserved bytes |
| Admission record | 128 bytes | Issuer identifier, capacity slot and signature binding the header and ciphertext |
| Sealed body | 3,840 bytes | Capability wrapper containing the complete authenticated session packet and padding |

Admission epochs last 60 seconds. Cells expire 48 hours after their admission epoch begins; publishers cannot purchase arbitrary retention. Unknown versions, nonzero reserved fields, malformed records and incorrect lengths are rejected before cryptographic processing.

Define the cell identifier as a domain-separated hash of its header and sealed body, excluding the admission signature. Reannouncing an identical cell therefore preserves its identifier. The admission signature binds that identifier, network, epoch and capacity slot.

Inside the sealed body place:

- Application protocol and schema version.
- Private channel/session identifier and publisher authentication.
- Logical event identifier, sender sequence, application deadline and causal references.
- Payload type and actual length.
- Fragment number/count when required.
- Payload and authenticated padding.

Use canonical CBOR for application records; preserve the session protocol’s native encoding inside its wrapper. Application payload types include notifications, signed attestations, job requests/results, contract-consumption requests and session/group control messages. Relay validation never depends on the application schema.

Each cell carries at most **2,048 application bytes**. A logical event may use at most 16 cells, giving a 32-KiB payload ceiling. Fragment identity is sealed; incomplete events never execute. Large attachments are excluded initially because selective external fetching would introduce another interest channel.

The outer capability wrapper hides session headers and permits local trial recognition. **Assumption requiring cryptographic review:** the selected construction provides key hiding and robust recognition across multiple candidate keys. Ordinary authenticated encryption alone is not evidence of recipient anonymity; anonymity and robustness require separate analysis (`2001-bellare-keyprivacy`, §1.1; `2022-grubbs-anonrobustpq`, §1).

Use an established ratchet for pairwise content and MLS for managed groups. Seal the **entire** MLS packet: its ordinary `PrivateMessage` exposes group ID, epoch and other header fields (`2023-barnes-rfc9420`, §§6.3, 16.4). Authenticate the public header as associated data and bind negotiated versions to the session.

Reject Bitmessage’s static-key content encryption and shared-identity chans as the session-security model. The starting guide’s review explicitly identifies the missing forward secrecy and distinguishes a chan from a membership-managed group (`reviews/bitmessage-technical-guide-review.md`, “Checked and correct”).

## D2 — Definition of “private”

### Adversaries

**Proposed model:**

- **R — Local relay/service observer:** sees its connections, requests, objects and operational state.
- **C — Colluding infrastructure:** combines R’s observations across an arbitrary set of relays, admission issuers, indexers and wallet providers. No privacy claim follows merely from “minority.”
- **G — Global passive observer:** observes endpoint and infrastructure links, timing, sizes and volumes; may also obtain C’s records.
- **A — Active network adversary:** injects valid or malformed cells, delays, replays, drops, partitions, eclipses and creates identities.
- **I — Insider/endpoint adversary:** holds an authorized channel capability, receives plaintext, compromises endpoint state or controls application behavior.

All cryptographic claims assume secure primitives, authenticated key establishment and uncompromised challenge endpoints. These are assumptions, not findings about a future implementation.

### Named properties and games

Privacy must specify which differences two executions permit, rather than treat “encrypted” as a synonym for “anonymous” (`2019-kuhn-privacynotions`, §2).

| Property | Proposed definition | Initial claim |
|---|---|---|
| **Content confidentiality** | Equal-length payload substitution is computationally indistinguishable, subject to identical declared public leakage | Against R, C, G and A; excludes intended recipients and compromised keys |
| **Subscriber-interest privacy** | Replace a consumer’s interest/key set while holding online schedule, fetched feed, public actions and external application responses fixed; its network transcript remains indistinguishable | Against R, C and G; against A only when fetching/error behavior remains independent of recognition |
| **Topic-label confidentiality** | Relay-visible objects contain no topic name, recipient address or session/group identifier | Conditional on reviewed wrapper security; excludes capability holders and application disclosures |
| **Publisher-message unlinkability** | Swap which honest publisher originates challenge cells without distinguishable observations | **Not provided** |
| **Recipient-message unlinkability** | Swap which matched consumer recognizes a cell without distinguishable transport observations | Conditional consequence of whole-feed reception and hidden recognition; **inference**, requiring composition proof |
| **Relationship privacy** | Swap communicating pairs while preserving allowed activity leakage | Only the preceding restricted, non-reactive reception game; no general end-to-end relationship claim |
| **Timing/volume privacy** | Hide real publication activity and communication counts | **Not provided**; cell padding hides individual plaintext lengths within a cell, not cell counts |
| **Forward secrecy / recovery** | Later compromise does not expose deleted past content keys; security can recover after appropriate uncompromised updates | Session-layer claims only, with erasure/update conditions |

Retaining skipped keys weakens forward secrecy for their corresponding messages. Recovery does not defeat persistent endpoint control or an ongoing active impersonation attack (`2016-signal-double-ratchet-spec`, §§8.1–8.4). Discovery-capability compromise may expose historical channel membership even when inner ratchet content remains protected. **Metadata forward secrecy is therefore not an initial guarantee.**

### Leakage table

**The following is the proposed leakage contract; deductions from the architecture are marked inference.**

| Observer | Learns | Protected, subject to stated assumptions |
|---|---|---|
| Relay / feed server | Neighbor/client IPs, online periods, cursor and catch-up range, cell identifiers, admission issuer/slot, epoch, propagation timing and aggregate traffic; direct uploads can identify publishers | Payload, sealed topic/session identifiers and which cells a full-feed client recognizes |
| Admission issuer | Purchasing account/payment, quota, submitted cell identifiers and issuance timing | Payload and recognition results; publisher identity is **not** hidden from this actor |
| Indexer | Public contract calls/commitments; filters and addresses requested from its APIs | Off-chain payload and interests of consumers using the separate whole-feed interface |
| Chain observer | Registry changes, settlement transactions, commitment timing, public contract addresses/transcripts and DUST fee values | Sealed payload and private witnesses; application-dependent deductions remain possible |
| Colluding minority | Union of local observations; publisher attribution, enrollment correlations and targeted partitions may become possible | Content and conditional interest privacy do not depend on a numerical honest-majority threshold |
| Global observer | Endpoint participation, publication timing/volume, feed-download patterns, catch-up behavior and likely publisher origins; public application reactions enable correlation | Content; recognition results in the restricted fixed-behavior reception game |

The existing indexer’s `contractEvents` filter requires a contract address; this reveals that query interest to the serving indexer (`midnight-indexer/indexer-api/graphql/schema-v4.graphql:548`). Its server-assisted wallet path stores viewing keys and performs detection centrally (`midnight-indexer/docs/architecture.md:20`). Neither is the private subscription interface proposed here.

### What the bounds forbid us to claim

1. **Anonymity trilemma.** In the synchronized model, with latency \(\ell<N\), dummy rate \(\beta\) per user per round and \(\beta N\ge1\), strong anonymity is impossible when \(2\ell\beta<1-\epsilon(\eta)\). These are necessary constraints, not sufficient conditions (`2017-das-trilemma`, §V-B, Theorem 2). For illustration, \(\ell=10,\beta=0.01\) gives \(0.2\), not approximately 1; this is arithmetic in model rounds, **not a ten-second engineering bound**. Unsynchronized behavior has its own constraints (§VII, Theorem 7).

2. **Coordination is not a free escape.** The broader synchronized model excludes strong anonymity when \(\hat\ell(B+1)<N-\epsilon(\eta)\), under Theorem 2’s conditions. The paper also explains why sender-side shares do not eliminate recipient packet-tracking bounds (`2020-das-comprehensivetrilemma`, §5.2, Theorem 2; pp.4–5). These results cover defined protocol classes, not every possible cryptographic construction.

3. **Gossip has intrinsic source leakage.** For an undirected connected graph and \(f>1\) curious nodes, any gossip protocol satisfying the paper’s source \(\epsilon\)-DP requires \(\epsilon\ge\ln(f-1)\). If vertex connectivity is at most \(f\), no finite worst-case \(\epsilon\) is possible (`2023-guerraoui-inherent-anonymity-gossiping`, §4.2, Theorem 5). Thus a six-neighbor mesh cannot acquire a worst-case anonymity guarantee from a generic “minority honest” argument.

4. **Receiver privacy has costs.** Perfect, information-theoretic single-server PIR requires linear communication in the classical model; that lower bound does **not** prohibit computational single-server PIR (`1998-chor-pir`, §§1.3, 5.1). OMR satisfying strong detection-key unlinkability implies PIR with essentially corresponding online costs (`2026-fisch-unifomr`, §5.1, Theorem 5.1). This does not establish a universal linear-computation lower bound for all retrieval schemes.

Whole-feed reception chooses replication cost to obtain conditional interest privacy. It does not establish strong sender anonymity or defeat the trilemma.

Out of scope initially: hidden participation, global publisher anonymity, coercion resistance, malicious recipient confidentiality, persistent endpoint compromise, quantum-resistant guarantees and privacy of application actions deliberately disclosed on-chain.

## D3 — Publish and subscribe model

**Proposal.** A topic is an application capability, not an overlay routing label. Invitations carry authenticated session initialization and recognition secrets through an existing trusted channel. Public contact discovery and unsolicited first contact are excluded from the initial release.

All relays carry one common transport topic. Consumers request every cell since their transport cursor at a fixed one-second cadence while online. They never submit topic filters, keys or recognition results.

Separate fetching from local recognition so decryption success, key count and malformed matched messages cannot change network requests. Every minute, obtain a complete recent inventory from a second operator and repair **all** differences, independent of private matches. This mitigates omission; it does not prove completeness.

Wallets recognize locally and notify their user. Agents recognize locally, validate application authorization and deadlines, then execute idempotent handlers. A provider that receives capabilities or viewing keys becomes a trusted interest observer. A bandwidth-constrained wallet may delegate to a user-controlled desktop, but privacy then terminates at that desktop.

Midnight already supplies a useful implementation pattern: the checked shielded-wallet path obtains global Zswap events and applies them with local secret keys (`midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:243`, `:266`, `:295`). Extending that pattern to this bus is a **proposal**, not an existing wallet capability.

Delivery semantics:

- At-least-once retrieval within retention; deduplicate cells by identifier and logical events by authenticated event identifier.
- Sender-local sequence and explicit causal references; no total bus order.
- Inclusive resume cursors; no exactly-once execution promise across crashes.
- Transport acknowledgment means storage acceptance, never recipient recognition.
- No automatic receiver acknowledgments in the privacy profile.
- Sender retries use the same logical identifier; newly encrypted retries remain countable publications.
- Back-fill retrieves complete time windows, including unrelated traffic.

For groups, use MLS membership changes rather than shared signing identities. Wrap control traffic as well as application traffic. Rotation and out-of-order recovery must preserve the D2 fetching invariant. **Assumption:** the initial supported group ceiling is 32 members, conditional on control-message fragmentation tests; do not infer it from MLS’s asymptotic costs.

**Contract consumption requires an explicit transaction.** An off-chain consumer submits an event-derived witness; the receiving circuit checks an authorized commitment, application predicate and replay nullifier before changing state. A relayer’s claim that it saw a message is insufficient. The checked VM exposes operations such as `Log`, not a network subscription primitive; requiring an off-chain transaction bridge is an **inference** from the execution model (`midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/ops.rs:156`).

For contract-originated events, an authorized circuit records a commitment to the event; an off-chain publisher distributes its opening privately. Distinguish **contract-authorized**, **chain-finalized** and **off-chain signed** provenance. Compact supplies commitment-style hashing (`example-bboard/contract/src/bboard.compact:58`), but the event-specific authorization circuit must be implemented and verified.

Contract consumption reveals its public transaction effects and may confirm a relationship. The restricted reception guarantee ends at that disclosure.

## D4 — Sustainable model

**Proposal.** Launch with prepaid, signed admission records. Independent issuers receive explicitly allocated capacity slots and sign the final cell identifier after charging a publisher. Relays enforce issuer authorization, slot allocation, expiration and deduplication. Conflicting signatures for one slot constitute publicly checkable issuer equivocation.

This intentionally trusts launch issuers for admission availability and allocated capacity. It does not conceal publishers from them. Do not attach a stable publisher identifier to forwarded cells.

Publishers fund dissemination and 48-hour storage. Feed subscribers fund egress through whole-feed service plans. Application sponsors buy minimum idle capacity. Archives sell longer retention independently. Operator contracts settle in fiat or an explicitly supported transferable asset; no assumption of transferable DUST.

**Midnight facts:** DUST is documented as non-transferable gas capacity (`midnight-docs/docs/concepts/dust-architecture.mdx:23`). Ledger-9 spends expose `v_fee`, a nullifier, new commitment and proof, and decrease the private output value by that fee (`midnight-ledger@ledger-9.1.0.0-rc.5/ledger/src/dust.rs:469`, `:1763`). Its resource-price calculation charges the maximum normalized read/compute/block-use component plus write and churn components (`midnight-ledger@ledger-9.1.0.0-rc.5/base-crypto/src/cost_model.rs:408`).

With the checked genesis parameters and atomic units, the cap is:

\[
5{\times}10^9\ \text{Specks/Star}\times10^6\ \text{Stars/NIGHT}
/10^{15}\ \text{Specks/DUST}=5\ \text{DUST/NIGHT}.
\]

Time to cap is approximately \(5{\times}10^9/8267=604{,}814\) seconds. These are **inferences by arithmetic**, not live deployment prices (`midnight-node/res/mainnet/ledger-parameters-config.json:164`; `midnight-ledger@ledger-9.1.0.0-rc.5/ledger/src/structure.rs:3362`).

Registry, settlement and contract-bridge callers pay their own DUST costs. That expenditure does not constitute relay compensation. The checked runtime’s block-reward hook returns `(0, None)`; do not assume an existing relay reward stream (`midnight-node/runtime/src/lib.rs:681`).

At low load, sponsors pay the idle floor. At high load, sell bounded admission slots and raise quoted capacity prices; reject excess publication explicitly. **Proposed pricing equation:**

\[
\text{required revenue}\ge
\text{idle operations}+\text{validated cells}+\text{replication}
+\text{retention}+\text{subscriber egress}.
\]

Actual monetary coefficients are **unknown**; obtain operator bids and measured traffic costs before launch.

Reject PoW as the sole funding/spam mechanism: it does not pay storage operators. Retain connection quotas, cheap parsing, signature checks and bounded queues against invalid traffic.

Evaluate RLN for decentralized quota admission later. Its misuse reveals the dedicated admission identity secret, so never reuse a session or wallet secret (`2022-taheri-waku-rln-relay`, §II-B). The paper’s prototype reports approximately 30-ms verification: at 100 unique cells/s, that is **3 CPU-seconds/s**, before other work (§IV; arithmetic inference). RLN does not make an unlimited population of paid identities free of spam risk.

## D5 — Performance requirements

**Proposed acceptance targets, not measured capacity.** Count cells, including fragments and control traffic.

- Normal planning load: 10 cells/s.
- Sustained capacity test: 100 cells/s.
- 1,000 simultaneous whole-feed consumers.
- One cell reaches every connected consumer; this fan-out does not mean every consumer is an intended recipient.
- Off-chain single-cell latency, measured from admission completion: p50 ≤2 seconds, p95 ≤5 seconds, p99 ≤15 seconds.
- Admission/payment latency reported separately.
- No-chain logical events of 16 cells: p95 ≤10 seconds, p99 ≤30 seconds.
- Chain consumption reports finality and indexing separately, with no initial percentile promise.

Arithmetic:

\[
B=r\times4096.
\]

| Quantity | 10 cells/s | 100 cells/s |
|---|---:|---:|
| Unique feed bandwidth | 40,960 B/s | 409,600 B/s |
| Feed per day | 3.539 GB | 35.389 GB |
| Feed for 48 hours | 7.078 GB | 70.779 GB |

For 16 launch relays, allocate at most 63 consumers each. With six overlay neighbors:

\[
(63+6)\times100\times4096
=28.2624\ \text{MB/s outbound}
=226.10\ \text{Mbit/s}.
\]

A 50% allowance for protocol overhead and repair gives approximately 339.15 Mbit/s. Budget a 1-Gbit/s interface. With 32 relays and 32 consumers each, the corresponding allowance is approximately 186.78 Mbit/s. These estimates assume one payload copy per outbound neighbor/client; verify actual propagation amplification.

| Node class | Proposed budget |
|---|---|
| Dedicated relay | 8 CPU cores, 16 GiB RAM, 1-Gbit/s networking; admission/replication CPU ≤4 cores at target load |
| Desktop wallet/agent | 32 simultaneously tested recognition keys; ≤0.5 CPU core for recognition at 100 cells/s |
| Archive | Relay resources plus D6 storage; separately rate-limited back-fill |
| Mobile direct consumer | Same feed cost; no low-bandwidth privacy promise |
| Validator/full node without bus role | Zero bulk-bus bandwidth or scanning obligation |

With 32 recognition keys, scanning 100 sealed bodies/s examines at most:

\[
32\times100\times3840=12.288\ \text{MB/s}.
\]

A half-core budget allows roughly 156 microseconds per recognition attempt. This is a **benchmark threshold**, not a cryptographic performance claim.

Whole-feed traffic is 3.54 GB/day even at normal planning load. This is the central deployment limitation. Sharding by interests would change the privacy claim; it is not an invisible optimization.

## D6 — Storage requirements

**Proposal.** Dedicated relays retain every admitted cell for 48 hours. Consumers prune unmatched cells after local processing, retaining cursors, deduplication state and bounded session recovery state. Archives offer seven-day retention initially.

At sustained capacity:

- Relay raw ciphertext: 70.779 GB.
- Proposed 128-byte index record per cell: \(100\times172800\times128=2.212\) GB.
- Allocate 120 GB usable bus storage per relay, excluding OS and unrelated chain data.
- Seven-day archive raw ciphertext: 247.726 GB; allocate 400 GB.
- Unpruned annual ciphertext: 12.917 TB.

All are **inferences from D5 assumptions**. Every replica bears its own storage cost.

An admission receipt becomes **stored** after three distinct operators acknowledge persistence through expiry. Distinct operators are an operational diversity requirement, not proof of independent failure probabilities.

Availability is conditional: a consumer returns before expiry, can reach at least one honest surviving holder, and has sufficient catch-up capacity. Complete partition, coordinated deletion or prolonged offline operation defeats delivery. Receipts and commitments do not prove continuing data availability.

Prune ciphertext at expiry; retain equivocation evidence and bounded admission audit records longer under explicit operator policy. Clients must not assume remote pruning deletes an adversary’s copy.

The ledger contains issuer authorization, settlement and application-selected commitments/nullifiers. It contains neither the ordinary ciphertext feed nor subscriber lists. Application commitments require fresh high-entropy openings to resist guessing; **cryptographic assumption** to verify for the chosen construction.

Ledger-9 logs above the emitted-size limit can disappear: the checked limit is 1 KiB and decoding invokes bounded serialization (`midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:41`, `:268`). This reinforces using small commitments rather than bulk log transport.

## D7 — Infrastructure actors

**Proposal.**

| Actor | Responsibility / trust | Payment |
|---|---|---|
| Dedicated relays | Validate admission, disseminate and retain opaque cells; trusted conditionally for availability | Capacity and egress contracts |
| Admission issuers | Sell allocated slots and endorse cells; know purchasing publishers | Publication charges |
| Validators/full nodes | Existing ledger duties; optional separate relay process | Existing arrangements; no assumed bus subsidy |
| Indexer adapters | Observe public commitments and finalized application actions; prove/check provenance | Application service contracts |
| Wallet providers | Whole-feed delivery only; trusted with interests if given capabilities | Whole-feed plans |
| Agents | Local recognition and application execution; authorized agents know plaintext | Application-specific |
| Archives / third parties | Longer retention and additional independent feed sources | Archive plans/sponsorship |

Launch assumptions: 16 relay instances operated by at least eight organizations, multiple admission issuers and two archive operators. These are desired deployment requirements, **not claims about existing Midnight operators**.

Any third party may serve validated feed data. Relay identities authenticate operations; they do not imply anonymity or one-person-one-node admission.

The decentralized end state has open relay operation, multiple funding counterparties and ledger-governed issuer admission without a single required gateway. Replacement of issuer signatures by independently verified anonymous quotas is desirable, but gated on proof costs, enrollment economics and safe revocation. Decentralization remains incomplete while a closed issuer set can deny all publication.

Keep network identities, admission credentials and session identities separate. Never assign validator consensus keys to privacy transport.

The checked mainnet genesis D-parameter selects ten permissioned candidates and zero registered candidates (`midnight-node/res/mainnet/system-parameters-config.json:6`). This is genesis configuration, not evidence of the live operator population or independence.

## D8 — Network tether

Choose a **hybrid: separate libp2p overlay for ciphertext; Midnight for authorization, settlement and application commitments**. Use one common GossipSub topic, hash-based message identifiers and no application-publisher identity in GossipSub envelopes.

The checked node selects `sc_network::NetworkWorker`; its explicit registrations include GRANDPA, BEEFY and ledger-sync, not this application bus (`midnight-node/node/src/command.rs:326`; `midnight-node/node/src/service.rs:574`). Bulk bus integration would therefore be new node work. The ledger-sync implementation itself avoids serving expensive snapshots on validators by default to protect authoring/finality resources (`midnight-node/node/src/service.rs:614`).

Use GossipSub scoring, outbound-peer quotas and multiple initial connections for dissemination resilience; these are availability mechanisms (`2020-gossipsub-v11-spec`, “Outbound Mesh Quotas,” “Peer Scoring”). They supply no D2 publisher-anonymity claim.

**Fallback:** independently operated replicated feed servers exposing the identical whole-feed API. This preserves the restricted interest property if fetching behavior remains identical, while concentrating availability and ingress observation.

Changes:

- **Node/runtime:** none for bulk transport.
- **Compact:** application contracts for authorization, commitments and consumption; no language change initially.
- **Indexer:** optional public-commitment adapter; no private filters/viewing keys.
- **Wallet/agent SDK:** local capabilities, session processing, whole-feed synchronization and explicit privacy-profile reporting.

Generation boundary matters. Local node manifests pin ledger 9 (`midnight-node/Cargo.toml:472`). Compact 0.33 release notes introduce events alongside ledger-8-to-9 migration (`minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`). The local support matrix still lists mainnet Compact 0.31.1 (`midnight-docs/docs/relnotes/support-matrix.json:38`). **Unknown:** actual activation status. Verify deployed runtime/toolchain compatibility before enabling the event adapter.

Compact’s custom `Misc` event contains a 32-byte name and 256-byte payload (`minokawa-compact/compiler/midnight-events.ss:71`). Publishing there exposes the emitting contract and public commitment; it does not turn the ledger into a private mailbox.

## D9 — Threats and open risks

| Threat | Proposed defense | Residual risk |
|---|---|---|
| Eclipse / Sybil | Independent bootstraps, outbound selection, operator/network diversity, peer scoring, second-source complete inventories | Economic admission limits publications, not malicious network identities; fully eclipsed consumers lose availability |
| Spam / valid quota saturation | Paid capacity slots, fixed cell size/TTL, per-connection queues, early validation | Wealthy attackers can buy capacity; issuers can censor or equivocate |
| Publisher deanonymization | Accurately disclose direct-ingress and first-seen leakage | Initial profile deliberately provides no publisher anonymity |
| Selective omission / censorship | Three storage receipts, independent inventory comparison, full missing-set repair | No globally canonical completeness proof; all reachable holders may censor |
| Replay / duplicate execution | Bound network/epoch, cell deduplication, authenticated logical IDs and persistent application nullifiers | State rollback or handler crashes can repeat effects without transactional deduplication |
| Active recipient probing | No recognition-dependent requests, error responses, acknowledgments or fetching changes | Authorized senders may induce revealing application replies or chain actions |
| Key compromise | Ratchets, secure deletion, bounded skipped keys, authenticated capability rotation | Offline-key retention weakens past secrecy; persistent compromise defeats recovery |
| Indexer / proof-service abuse | Local recognition; verify finalized application state and transaction provenance | Remote proving privacy is **unknown** until witness exposure and service behavior are audited |
| Group forks / malicious insiders | MLS validation, serialized membership commits and explicit transcript agreement policy | MLS does not guarantee unrestricted group transcript consistency; insiders know group metadata |
| Malformed fragments / parsing DoS | Fixed framing, 16-cell limit, bounded reassembly and cryptographic checks before execution | Valid authorized traffic still consumes receiver work |
| Downgrade | Authenticate profile/version negotiation; reject silent fallback | Migration coordination can become a denial-of-service point |

These defenses are proposals; effectiveness against the stated active adversaries remains to be tested.

I reject a launch claim that Dandelion++ supplies global-observer resistance. Its evaluated botnet adversary can create many connections, but the paper distinguishes mass deanonymization from targeted attacks and excludes the ISP/AS adversary from its principal model (`2018-fanti-dandelionpp`, §3.1). Flooding and randomized diffusion also exhibit poor source anonymity in the analyzed regular-tree models (`2017-fanti-anonymitybitcoin`, §§3–5).

A later mix profile should require an entire security specification, including enrollment, cover generation, replay protection, endpoint schedules, compromised-node placement and low-load behavior. Loopix explicitly depends on cover traffic and excludes unrestricted user Sybils through assumptions about genuine users (`2017-piotrowska-loopix`, §2.2). Installing a mix hop alone does not inherit its guarantees.

I also reject “fuzzy detection equals private subscription.” With \(t\) genuine messages among \(M\), false-positive probability \(p\) yields approximately \(t+p(M-t)\) returned messages; traffic history can still reveal relationships (`2021-seres-fmdfalsepositives`, §2 and Introduction). It may be a separately labeled reduced-bandwidth profile, never an equivalent replacement.

## D10 — Build and verification plan

**All thresholds below are proposed acceptance criteria.**

1. **Property and construction review.** Before implementation, instantiate the D2 games and leakage function; select the exact wrapper/session suites; prove or obtain reviewed reductions for content, recognition and header hiding. Model malicious cells, retries, key rollover and fragment recovery. Any recognition-dependent network action blocks the private-reception release.

2. **Simulation.** Simulate normal/peak traffic, idle periods, 32 recognition keys, churn, partitions, six-neighbor meshes, issuer equivocation, targeted eclipses and correlated operator outages. Verify resource ceilings and quantify omission detection. Run first-spy attacks as evidence of expected leakage, not as a test that establishes anonymity.

3. **Interoperable prototype.** Implement fixed cells, bounded admission, whole-feed retrieval, local ratchets, deduplication and receipts. Require independent parser implementations and shared malformed-input vectors. At 100 cells/s and 1,000 consumers, meet D5 latency/CPU/storage targets over a continuous 48-hour capacity run.

4. **Privacy and failure testing.** For paired executions differing only in interests, compare requests, cursors, timing policy, error behavior and repair decisions. Test crash recovery, malformed matched cells and queue pressure. Every externally visible difference must either be removed or added explicitly to the leakage contract. Traffic-classifier results are diagnostic; they are not proofs.

5. **Midnight bridge.** Test finalized commitment verification, failed transaction phases, wrong-network replay and repeated consumption. Reject missing/misbound commitments; demonstrate that a false indexer response cannot authorize contract execution. The checked indexer follows finalized blocks (`midnight-indexer/chain-indexer/src/infra/subxt_node.rs:128`), and re-executes transactions against its own ledger state (`midnight-indexer/docs/architecture.md:15`); bridge correctness must not rely solely on trusting its event response.

6. **Funded pilot.** Obtain bids covering idle capacity, 100-cell/s retention and measured egress. Publish the restricted guarantee and actual bandwidth costs. If consumer devices cannot sustain the feed or funding cannot cover it, reduce admitted capacity or postpone production.

7. **Separate advanced profiles.** Benchmark mix publishing and PIR/OMR reception before adding claims. UnifOMR reports approximately 25 seconds and 4 MB communication for \(2^{19}\) messages of 612 bytes in its evaluated configuration (`2026-fisch-unifomr`, Abstract, §8). That is evidence to investigate, not a prediction for this bus’s larger cells and workload. A retrieval profile must address message discovery, fixed request scheduling, capacity overflow and malicious-server behavior.

Change course if full-feed costs exclude intended wallet users; if wrapper key hiding cannot be established; if active omission probes violate the reception game; or if no viable operator funding exists. Source anonymity becoming a launch requirement would require a redesigned, costed transport profile rather than a wording change.

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|
| D1 | Fixed padded cells; sealed session headers; bounded fragmentation | Static content keys, public group/topic headers | `2023-barnes-rfc9420` §§6.3,16.4; `2022-grubbs-anonrobustpq` §1 | Medium | Wrapper proof failure or control messages exceeding practical bounds |
| D2 | Confidentiality and conditional subscriber-interest privacy; explicit activity leakage | Unqualified “anonymous/private” claims | `2017-das-trilemma` Thm.2; `2023-guerraoui-inherent-anonymity-gossiping` Thm.5; `2026-fisch-unifomr` Thm.5.1 | High | A reviewed construction under a materially different model |
| D3 | Capability discovery, whole-feed reception, explicit transaction consumption | Server topic filters, autonomous contract subscriptions, exactly-once transport | `midnight-wallet/packages/shielded-wallet/src/v1/Sync.ts:243`; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:548` | Medium | Verified private discovery/retrieval with adequate costs |
| D4 | Paid admission and egress; sponsor-funded idle floor; DUST only for ledger work | PoW-only funding, DUST relay payments | `midnight-ledger@ledger-9.1.0.0-rc.5/base-crypto/src/cost_model.rs:408`; `2022-taheri-waku-rln-relay` §§II-B,IV | Medium | Audited anonymous quotas and sustainable operator bids |
| D5 | 10-cell/s planning load; 100-cell/s capacity; 1,000 consumers | Uncosted scale claims, concealed topic sharding | Explicit arithmetic in D5; trilemma constraints | Medium | Measurements violating budgets or demand requiring private thin clients |
| D6 | 48-hour relay retention; seven-day archive; conditional availability | Permanent ordinary feed storage, commitment-as-availability claims | D5 arithmetic; `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/vm.rs:41` | Medium | Required offline duration or correlated storage failures |
| D7 | Dedicated independent operators; open relay service; staged admission decentralization | Mandatory validator carriage, identity-count anonymity assumptions | `midnight-node/node/src/service.rs:614`; `midnight-node/res/mainnet/system-parameters-config.json:6` | Medium | Operational evidence supporting a stronger decentralized launch |
| D8 | Separate overlay plus ledger authorization/commitments; whole-feed-server fallback | Consensus-network bulk traffic, ledger/indexer-only private bus | `midnight-node/node/src/service.rs:574`; `minokawa-compact/compiler/midnight-events.ss:71` | High | A measured native isolated transport with equal privacy |
| D9 | Treat ingress attribution, probing, compromise and censorship as explicit residual risks | Dandelion-as-global-anonymity, FMD-as-equivalent-reception-privacy | `2018-fanti-dandelionpp` §3.1; `2021-seres-fmdfalsepositives` Introduction | High | Reviewed defenses covering the stronger adversaries |
| D10 | Proof gates, simulations, capacity tests, funded pilot; advanced profiles separately | Benchmark-as-proof, inherited security by component name | `2019-kuhn-privacynotions` §2; `2017-piotrowska-loopix` §2.2; `2026-fisch-unifomr` §8 | High | Failed property, capacity, usability or funding gates |