I recommend a separate, paid event overlay with one shared dissemination domain, encrypted application envelopes, local recipient recognition, and optional Midnight batch commitments. The initial privacy promise should cover content confidentiality and concealment of a connected subscriber’s interests from infrastructure; publisher anonymity, relationship privacy against traffic analysis, and timing privacy must remain explicitly unclaimed. My principal condition is an evidence gate: deployment facts must come from the deployed generation, performance must be measured for the proposed workload, and security results must retain their original adversary assumptions. **Inference:** this is the smallest useful starting point supported by the checked evidence; stronger anonymity and efficient private mobile retrieval require separate experiments.

## D1 — Event format

**Proposal; all format choices below are engineering assumptions pending implementation review.**

Use a fixed **2,048-byte record** in version 1:

| Region | Size | Contents |
|---|---:|---|
| Public header | 128 bytes | Magic, protocol version, cryptographic suite, network identifier, hourly expiry bucket, fresh salt, recipient-recognition hint, reserved bytes |
| Admission permit | 128 bytes | Issuer identifier, single-use serial, issuer signature |
| Sealed body | 1,792 bytes | Application metadata, authenticated session message, padding and outer authentication tag |

Specify field widths, byte order and reserved-byte rejection in the wire specification. Hash the public header and sealed body with domain separation to obtain the event identifier; the permit signs that identifier and its serial. Excluding the permit from the identifier permits transport deduplication when the same event is submitted through another admission service.

Keep **publisher identity, logical topic, schema identifier, application timestamp, sequence number, acknowledgement requests, fragment metadata and application payload sealed**. Expose no stable topic tag or recipient address.

A candidate recognition mechanism is a salted, truncated PRF under a secret discovery capability. Every subscriber receives every record and tests its own capabilities locally. **Inference:** fresh salts can prevent an outsider without the capability from directly grouping records by their hints. This construction is not a checked privacy protocol; its key rotation, domain separation, wrapper encryption and interaction with session security require analysis before release.

Use deterministic application encoding with explicit schema versions. Initially support:

- Typed application events with at most **1,024 bytes of application data**.
- Session and group control messages.
- Authenticated references to external objects, with the resulting fetch leakage declared.

Permit bounded fragmentation for control messages, initially at most **16 records per logical message**. Every fragment consumes admission capacity; reassembly limits apply before allocation. Unsupported versions fail explicitly. Do not infer forward secrecy from the outer wrapper.

Use an established session protocol inside the wrapper. For explicit membership groups, use MLS with a conservative initial cap of **100 members**. MLS’s group ID, epoch, some handshake fields and lengths are exposed unless additionally protected; an unwrapped MLS message would contradict the proposed topic privacy. [`2023-barnes-rfc9420`, §§16.3–16.4.]

Retain records for **48 hours after acceptance**, subject to a maximum permitted expiry bucket. Expiry governs service obligations, not deletion by observers.

**Checked Midnight constraint:** Compact’s custom `Misc` event is a 32-byte name plus a 256-byte payload. Ledger 9 separately permits a 512 KiB VM log argument but silently omits emitted events whose bounded serialized data exceeds 1 KiB. Neither limit provides a 512 KiB application event channel. [`minokawa-compact/compiler/midnight-events.ss:71`; `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:39`, `:43`, `:268`.]

Reject Bitmessage wire compatibility and ledger-carried bulk records. Preserve recipient-oblivious dissemination as an idea, not its historical cryptographic format. Bitmessage’s original design disseminates messages for local decryption; the supplied encryption specification uses a static destination key, so sender ephemerality does not itself yield forward secrecy. [`2012-warren-bitmessage-whitepaper`, §3; `2017-pybitmessage-repo-protocol-docs`, `docs/encryption.rst`, “Encryption”; latter conclusion **inference**.]

## D2 — Definition of “private”

**Proposal:** version 1 promises the following conditional properties:

1. **Content confidentiality and authenticity:** against infrastructure lacking endpoint secrets, conditional on the chosen session protocol, correct implementation and authenticated onboarding.
2. **Subscriber-interest privacy:** a connected client requests the complete shared stream rather than a topic, recipient mailbox or selected event set.
3. **Topic-label confidentiality:** logical topic names remain encrypted.
4. **Limited record unlinkability:** fresh discovery hints avoid a stable public topic identifier; protection is conditional on capability secrecy and wrapper analysis.

It does **not** promise publisher unlinkability, sender unobservability, timing privacy, volume privacy or relationship privacy against a global observer.

**Proposed leakage table; deductions are inference from the proposed interfaces.**

| Observer | Information available |
|---|---|
| Relay or retrieval gateway | Client IP and connection times; publication ingress; all record identifiers, sizes, expiry buckets and permit issuers; complete-stream cursors |
| Admission issuer | Its customer relationship, quotas, permit serials and signed event identifiers; it can recognize those events after publication |
| Midnight indexer | Anchor-contract queries, client network metadata, public batch commitments and any contract activity selected by the client |
| Chain observer | Anchor contract, transactions, batch cadence, roots, counts if disclosed, consumption effects and public fee declarations |
| Colluding minority | Union of their observations; first-seen correlation and targeted censorship opportunities; no generic anonymity threshold is claimed |
| Global observer | Network timing and volume, online population, publication ingress and downstream actions; potentially publisher and relationship correlations |
| Capability holder or group insider | Recognition of its own feed and plaintext authorized to it; it can disclose these to others |

Full-stream retrieval hides **selection**, not participation. Interest-dependent disconnects, acknowledgements, attachment fetches and contract calls can reintroduce correlations. **Inference.**

Dandelion++ is unsuitable as the basis of a global-observer guarantee. Its paper studies colluding spy nodes and mass deanonymization; ISP/AS adversaries and targeted guarantees are outside its stated scope. Theorem 1’s near-optimal first-spy result additionally assumes an unknown random four-regular anonymity graph. [`2018-fanti-dandelionpp`, §3.1 and §4.1, Theorem 1.]

Loopix is a candidate for a later stronger profile, but its model excludes unrestricted client Sybils, restricts corrupt providers to honest-but-curious behavior, and conditions important receiver protections on an honest provider. These are deployment obligations, not consequences of merely adopting Sphinx packets. [`2017-piotrowska-loopix`, §§2.2–2.3, 4.1.2.]

Out of scope initially: endpoint compromise, insider disclosure, secure deletion from adversarial archives, private public-directory searches, concealment of contract identity, and post-quantum confidentiality.

## D3 — Publish and subscribe model

**Proposal:** one shared transport domain; logical topics exist only inside authenticated invitations and encrypted records. Do not build transport meshes around application topics.

An invitation carries the network identifier, discovery capability, session onboarding material, authorized publisher policy and supported schemas. Discovery begins through an authenticated existing channel. **Unknown:** a suitable private, decentralized discovery service has not been established by this proposal.

Publishers obtain a permit and submit to independent relays. Subscribers download the complete stream, recognize candidates locally, verify session authentication, then dispatch typed events. Relays receive no topic subscriptions. This follows the original flood-and-scan principle while separating infrastructure operators from consumers. [`2012-warren-bitmessage-whitepaper`, §§3–4; architectural adaptation **inference**.]

Define delivery as:

- **At least once within retention**, conditional on a reachable honest retained copy.
- Deduplication by transport identifier, followed by application replay checks.
- Per-publisher authenticated sequence numbers and explicit gap reporting.
- No global application ordering.
- Backfill by complete time windows or complete manifests, never by requested logical topic.
- No automatic acknowledgement of recognition.

MLS commits need an application ordering policy. Initially designate one group commit coordinator, while allowing ordinary application messages from authorized members. Coordinator compromise or failure is a declared group liveness risk. MLS does not solve delivery-service censorship or commit suppression. [`2023-barnes-rfc9420`, §§14, 16.9.]

**Contract consumption requires a follow-up transaction.** An agent retrieves and authenticates an event, then supplies its relevant data through a witness or disclosed argument. The circuit checks application authorization, freshness and replay policy. An anchor inclusion proof establishes commitment to bytes; it does not establish that an event is true.

Compact witnesses execute outside the ledger; the checked VM operation set supplies no network subscription mechanism. **Inference:** contracts cannot autonomously consume the overlay. [`minokawa-compact/doc/compact-reference.mdx:3543`; `midnight-ledger@ledger-9.1.0.0-rc.5/onchain-vm/src/ops.rs:156`.]

Wallets receive a separate event SDK with local capability storage and decoding. Agents use durable cursors and transactional application deduplication.

Do not present existing `contractEvents` subscriptions as interest-private: they require a contract address; indexed-field filtering applies only to standard events. Inclusive cursors and reconnects also require deduplication. [`midnight-indexer/indexer-api/graphql/schema-v4.graphql:552`, `:558`, `:1967`; `midnight-js/packages/types/src/public-data-provider.ts:502`, `:507`.]

## D4 — Sustainable model

**Proposal:** sponsors purchase explicit relay and retention capacity. Launch admission uses issuer-signed, event-bound, single-use permits. It intentionally sacrifices anonymity from the admission issuer.

Assign each issuer a bounded permit range per epoch. Relays enforce signature validity, expiry, serial bounds, duplicate/conflicting serial handling, record size and local ingress budgets before forwarding. Honest issuance is a launch trust assumption; issuer equivocation must be detected and reported.

Separate three costs:

1. Publication admission.
2. Relay replication and subscriber egress.
3. Retention and optional archival.

Subscriber egress grows with connected consumers and cannot be funded from an unexamined fixed publication fee. Sponsors must reserve fan-out capacity; authenticated service accounts may enforce download quotas while receiving the same complete stream. Account identity does not disclose topic selection, but does disclose participation.

**Checked DUST boundary:** DUST is non-transferable gas capacity. It is not a payment token that publishers can transfer to relay operators. Sponsors pay DUST for anchoring and contract consumption; operator compensation needs a separate commercial or transferable-asset arrangement. [`midnight-docs/docs/concepts/dust-architecture.mdx:23`; `midnight-ledger/spec/dust.md`, opening and spend sections.]

At the checked mainnet genesis configuration:

- One NIGHT backs a maximum **5 DUST**.
- Generation is approximately **0.71427 DUST per NIGHT per day**.
- Capacity fills in approximately one week, and value decays after the backing NIGHT is spent.

The arithmetic uses 8,267 Specks per Star per second, \(10^6\) Stars/NIGHT and \(10^{15}\) Specks/DUST. [`midnight-node/res/mainnet/ledger-parameters-config.json:165`; `midnight-ledger@6abe9b16/ledger/src/dust.rs:294`, `:1364`; `midnight-ledger@6abe9b16/ledger/src/structure.rs:3362`.]

The checked fee function prices normalized read, compute and block usage through their maximum, then adds write and churn charges. Prices update with fullness. [`midnight-ledger@dc87cc8f/base-crypto/src/cost_model.rs:354`, `:408`.]

**Illustrative assumption:** an 8,192-byte anchor transaction each minute, genesis price 10, unit factors and block usage dominating:

\[
10(8192/1{,}000{,}000)=0.08192\ \text{DUST/anchor}.
\]

That gives **117.9648 DUST/day** for the block-usage contribution alone, corresponding to roughly **165.2 NIGHT** of sustained generation. Writes, churn, other transactions, safety margins and dynamic prices increase the requirement. This is not a live fee quotation. [`midnight-node/res/mainnet/ledger-parameters-config.json:158`, `:170`; arithmetic **inference**.]

Reject compulsory per-event chain payment and flat PoW as the main economic model. Laurie–Clayton’s result concerns email workloads, machine heterogeneity and stolen computation; it undermines the assumption that puzzle cost reliably distinguishes legitimate users from spammers, rather than proving every PoW use impossible. [`2004-laurie-proofofwork`, §§3–5.]

Anonymous rate-limited admission is a later project. Midnight’s documented commitment/nullifier example provides single-use authorization; epoch quotas are an extension requiring proof design and measurement. RLN-V2 is a separate protocol, not an existing Midnight feature. [`midnight-docs/docs/concepts/how-midnight-works/keeping-data-private.mdx:179`, `:209`; `2024-vac-rln-v2-spec`, “Abstract,” “Flow.”]

## D5 — Performance requirements

**Assumed workload and acceptance targets, not measured capabilities:** 10 admitted records/s sustained, 100/s for a 60-second burst, 10,000 simultaneous complete-stream consumers, 20 relays, average six forwarding copies per relay.

All control records and fragments count toward these rates.

For \(R=10\) and \(S=2048\):

\[
B_{\text{consumer}}=RS=20{,}480\ \text{bytes/s},
\]
\[
B_{\text{all consumers}}=NRS=204.8\ \text{MB/s}.
\]

With 500 consumers per relay:

\[
B_{\text{relay,out}}\approx500RS+6RS
=10.363\ \text{MB/s}=82.9\ \text{Mbit/s}.
\]

The burst raises this estimate to **829 Mbit/s**. These figures exclude transport overhead, inventory exchanges, retries and uneven client assignment. Reserve at least **30% additional bandwidth** and benchmark whether a 1 Gbit/s relay can sustain the burst. The six-copy model must be replaced with measured amplification.

| Node class | Proposed requirement |
|---|---|
| Dedicated relay | 8 vCPU, 16 GiB RAM, 100 GiB SSD, 1 Gbit/s; nominal service consumes at most 2 vCPU |
| Retrieval gateway | 500 concurrent complete-stream clients; bounded queues and explicit overload responses |
| Desktop wallet | 100 discovery capabilities; 20.48 kB/s nominal stream |
| Agent | Durable replay cursor, sequence-gap handling and application deduplication |
| Mobile wallet | Foreground complete-window retrieval initially; no continuous-background promise |
| Midnight validator | No overlay workload assigned by default |

A client with 100 capabilities performs **1,000 recognition tests/s** nominally, or 10,000/s during the burst. A target of 10 μs/test would consume approximately 1% and 10% of one core respectively; this is a benchmark target, not an implementation fact.

Latency targets, measured **after admission**:

- Relay propagation: p50 ≤1 s, p95 ≤3 s, p99 ≤10 s at nominal load.
- Burst: p99 ≤30 s without unbounded queue growth.
- Anchoring: separate measurements for submission, inclusion, finality and indexing.

Midnight’s checked slot duration is **6 seconds**. The proposal document’s “about 18 seconds” finality statement supplies neither an SLO nor a percentile. [`midnight-node/runtime/src/lib.rs:292`; `midnight-improvement-proposals/mps/mps-0028-pre-finality-state-visibility.md:36`.]

The genesis ledger allows 1,000,000 block-usage bytes per block. **Inference:** hypothetical 8 KiB transactions yield a byte-only ceiling of roughly 20 transactions/s at six-second slots, before runtime length, computation and other traffic constraints. The runtime separately sets 1 MiB block length with a 75% Normal ratio. [`midnight-node/res/mainnet/ledger-parameters-config.json:155`; `midnight-node/runtime/src/lib.rs:300`, `:313`.] This cannot justify a bus throughput claim.

Reject benchmark transplantation:

- Loopix’s evaluation uses six mixes, four providers, AWS instances and 500 client processes hosted on one machine. Its measured latency distribution with mean 1.93 s is not a p99 guarantee for this overlay. [`2017-piotrowska-loopix`, §5, Figures 8–10.]
- GossipSub’s 5,000-container experiments establish results for specified configurations and attacks, not privacy or arbitrary deployment capacity. [`2020-vyzovitis-gossipsub`, introduction, §§7–8.]
- OMR’s roughly 20 ms result is recipient decoding of 50 pertinent messages from a 500,000-message board. Detector work is separate. [`2021-liu-omr`, §§1, 10.]

## D6 — Storage requirements

**Proposal:** every launch relay retains the complete accepted stream for 48 hours. Three independently operated relays issue signed retention receipts before the publisher treats an event as durably accepted.

At the assumed workload:

\[
10\times2048\times172800
=3{,}538{,}944{,}000\ \text{bytes}
=3.296\ \text{GiB/relay}.
\]

There are **1,728,000 records** in the window. Assuming 64 bytes of dedup metadata per record adds approximately **110.6 MB**. A provisional 1.5× database multiplier gives **4.94 GiB** for records and ordinary indexing, before manifests, logs and operational headroom.

A 30-day archive contains **49.44 GiB raw** at the same rate. Archival is separately purchased and provides no deletion guarantee.

Wallet costs are substantial:

- Continuous download: **1.769 GB/day**.
- One hour of backfill: **73.728 MB**.
- Full 48-hour recovery: **3.539 GB**.

**Inference:** this baseline is unsuitable as an unrestricted background mobile service. That limitation is a design gate, not something hidden behind a “light client” label.

Prune records, permits, replay caches and incomplete fragment assemblies on bounded schedules. Retention receipts attest an obligation; they do not cryptographically prove future availability.

On the ledger, store only a bounded window of batch roots and necessary contract replay state. Root replacement and replay-state pruning must be specified explicitly; TTL does not imply application-state garbage collection.

**Checked correction:** MIP-0002 Appendix B derives its event-storage upper bound from the persistent-write budget. Ledger 9’s log implementation charges both written and deleted bytes, making logs churn. The appendix’s approximately 703 MB/day is therefore not an established event ceiling. [`midnight-improvement-proposals/mips/mip-0002-public-contract-log-emission.md:520`; `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:595`.]

The indexer’s 1,000-block ledger-state retention setting concerns loadable ledger states, not a verified retention promise for every contract-event row. [`midnight-indexer/chain-indexer/config.yaml:14`.]

## D7 — Infrastructure actors

**Proposal:** launch with independent dedicated relays, retrieval gateways, admission issuers, anchor submitters and self-hostable agents.

| Actor | Responsibility and trust |
|---|---|
| Relay | Validate admission, propagate and retain records; trusted for promised availability |
| Gateway | Serve complete windows; observes connections and cursors, receives no discovery secrets |
| Admission issuer | Enforce purchased quotas; observes customer-to-event linkage |
| Anchor submitter | Publish batch commitments; can omit or delay events, cannot establish their truth |
| Indexer | Supply chain-derived anchors; may censor or misreport unless independently checked |
| Wallet/agent | Hold secrets and verify application authenticity locally |
| Validator/full node | Ordinary Midnight duties; optional separately operated sidecar |

Use **20 launch relays across at least five operators** as a proposed operational target, not a proven anonymity threshold. Identity keys, operator independence and hosting diversity must be verified rather than inferred from distinct peer IDs.

Pay operators through service contracts covering reservation, retained bytes and client egress. Settlement evidence must avoid per-subscriber topic information.

Decentralization proceeds by publishing the protocol, reproducible implementations and conformance suite, permitting third-party relay services, and removing reliance on one admission issuer and one anchor submitter. Anonymous admission is required before advertising issuer-resistant publication.

**Unknown:** market-clearing relay prices, operator participation and independently verifiable service-payment mechanisms. Determine these through procurement, adversarial receipt testing and deployment measurements. Do not claim token rewards solve them.

## D8 — Network tether

Recommend a **hybrid: independent libp2p overlay for bulk transport; Midnight for optional commitments, authorization and consumption**.

Use one transport topic for the shared stream. GossipSub is a candidate dissemination component, not an anonymity mechanism.

The node selects `sc_network::NetworkWorker` and registers GRANDPA, BEEFY and custom ledger-sync protocols in code. Adding an application protocol through those registration points requires modifying the node integration. [`midnight-node/node/src/command.rs:327`; `midnight-node/node/src/service.rs:586`, `:607`, `:644`.] **Inference:** a sidecar avoids coupling initial bus development and resource exhaustion to consensus networking.

Required changes:

- **Node/runtime:** none for initial bulk delivery.
- **Compact:** ordinary anchor and consumption contracts; no new network primitive.
- **Indexer:** adapter for anchor observation, with optional independent re-execution.
- **Wallet:** local event capability/session store and complete-stream client.
- **Agent:** proof-generating consumption adapter.

Do not depend on mainnet contract-event activation merely because local source supports it. The support matrix lists mainnet toolchain 0.31.1; toolchain 0.33 release notes introduce ledger 9 and events. Actual activation is **unknown from these files**. [`midnight-docs/docs/relnotes/support-matrix.json:38`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22`, `:26`.]

Fallback: independent gateways serving the same complete encrypted stream, with roots read from contract state. This preserves content and selection privacy under the same conditions while declaring greater availability centralization.

Reject ledger/indexer-only bulk delivery and validator off-chain-worker integration. Contracts emitting public logs and an indexer re-executing finalized transactions do not provide an anonymous messaging transport. [`midnight-indexer/docs/architecture.md:15`; **inference**.]

## D9 — Threats and open risks

**Proposed defenses; residual risks remain explicit.**

| Threat | Defense | Residual risk |
|---|---|---|
| Eclipse/Sybil | Independent bootstrap operators, outbound diversity, peer limits and configuration-specific scoring tests | Operator or routing diversity can be falsified; no permissionless Sybil theorem claimed |
| Spam/resource exhaustion | Purchased permits, bounded issuer ranges, cheap early validation, ingress budgets and bounded parsing | Issuer abuse, stolen permits, invalid-signature floods and client egress attacks |
| Publisher deanonymization | No baseline defense beyond encrypted content; optional separately tested submission routing | Direct ingress and issuer linkage remain visible |
| Replay | Transport dedup, authenticated application sequences, contract replay state | Freshly wrapped duplicates and pruning-boundary mistakes |
| Censorship/data withholding | Three retention receipts, independent gateways, manifest comparison and gap alerts | Receipts can lie; complete coordinated suppression can persist |
| Key compromise | Authenticated onboarding, MLS updates, key deletion and explicit recovery | Insiders, stale offline members and suppressed commits undermine recovery |
| Indexer abuse | Independent anchor checks and contract-state reads | Completeness and availability still need independent observation |
| Topic/relationship analysis | Full-stream retrieval, sealed topic labels and salted hints | Insiders, timing, external-object retrieval and contract effects leak |
| Fragment/decoder abuse | Fixed records, size/count limits and authenticated reassembly | Authorized malicious publishers can consume their quota |
| Chain outage | Continue off-chain delivery; mark anchors pending | Contract effects and anchored assurance stop |

GossipSub scoring is configuration-sensitive. Formal work found violations of punishment properties in an Ethereum configuration despite earlier emulation and review. Passing common attacks is not a universal resilience proof. [`2022-kumar-gossipsub-formal`, introduction, §§3–5.]

MLS post-compromise recovery begins when the relevant commit is processed; an update proposal alone is insufficient. Forward secrecy also requires old-key deletion. [`2023-barnes-rfc9420`, §16.6.]

Reject fuzzy detection as an equivalent substitute for full-stream interest privacy. FMD provides detection ambiguity for honestly generated ciphertexts; subsequent analysis demonstrates relationship recovery under specified server observations and sender knowledge. [`2021-beck-fmd`, §1 and §4; `2021-seres-fmdfalsepositives`, §§3–4, 6.]

The anonymity trilemma is a model-specific lower bound involving communication rounds, bandwidth, latency and adversary capabilities. It is evidence against promising strong anonymity, negligible cover and negligible delay simultaneously—not a numerical design recipe. [`2017-das-trilemma`, §§III–VII.]

## D10 — Build and verification plan

I would lead D10 with **release gates tied to claims**, not feature completion alone. All numerical criteria below are proposed acceptance targets.

**Phase 0 — Freeze the evidence and model.**

Record immutable source revisions, deployed runtime version, ledger parameters, compiler and indexer schema. Resolve discrepancies before converting them into protocol guarantees.

The lockfile matters more than a current tag name: it pins ledger revision `6abe9b16`, VM revision `54a4e013` and base-crypto revision `dc87cc8f`. Locally resolved tags can differ. [`midnight-node/Cargo.lock:7894`, `:8460`, `:7609`.]

Maintain a claim register: claim, source, generation, checked scope, assumptions, contradicting evidence and reproduction procedure. Graph communities and catalog notes are navigation aids; conflicting catalog summaries must defer to the paper.

Acceptance: every shipped privacy and capacity statement has this record; deployment-dependent facts are confirmed on the target network.

**Phase 1 — Model before transport implementation.**

Model permit reuse/equivocation, relay crash recovery, expiry, fragment reassembly, duplicate delivery, reconnect cursors, MLS commit conflicts and contract replay-state pruning.

Define observational tests: two clients with identical connection/window schedules but different interests must produce identical retrieval requests and volumes. Test whether recognition causes acknowledgements, logs or external fetches.

Acceptance: no discovered safety violation in bounded exploration; crash/reconnect workloads produce explicit gaps or correct deduplicated delivery; malformed input has bounded memory and CPU effects. This is bounded assurance, not a general proof.

**Phase 2 — Build and measure the narrow service.**

Deploy the assumed 20-relay/10,000-consumer workload. Measure propagation percentiles, CPU, amplification, client recognition cost, egress, storage growth and catch-up.

Run 10 records/s for **72 hours**, then 100/s for 60 seconds; crash and partition relays; saturate admission with invalid traffic.

Acceptance:

- Meet D5’s latency and resource budgets.
- At least 99.9% of valid accepted records reach test consumers within the nominal p99 deadline in the stated non-partitioned workload.
- All receipt-backed records remain recoverable during retention when at least one honest receipt issuer remains reachable.
- Queue sizes recover after the burst.
- Parsing, wrapper cryptography and session integration have no unresolved critical or high-severity review findings.

Publish failures and conditions alongside successes.

**Phase 3 — Verify Midnight integration.**

Measure actual serialized transactions, cost dimensions, proving latency, finality and indexer delay. The DUST spend proof constant is 2,912 bytes, while the 4,832-byte call-proof estimate is not a measured universal contract transaction size. [`midnight-ledger@6abe9b16/ledger/src/dust.rs:2158`; `midnight-ledger@6abe9b16/ledger/src/structure.rs:1908`.]

Acceptance: invalid authorizations and replays never trigger contract effects in the tested model; fallible execution is handled correctly; malicious indexer results cannot authenticate nonexistent anchor state; consumption reveals only the explicitly reviewed public effects.

**Phase 4 — Compare retrieval and anonymity upgrades independently.**

Benchmark complete download, PIR and OMR on identical retained boards, update rates, payload sizes and subscriber workloads.

OMR privacy tolerates malicious collusion under its definition; correctness has separate honest-behavior and capacity conditions. It does not inherently require two non-colluding servers. [`2021-liu-omr`, §§4.1–4.3.]

Its approximately 0.065 s/message detector result is **per recipient served**. At 10 new records/s, naïve independent processing implies 0.65 detector-seconds per wall-clock second per recipient, or 6,500 for 10,000 recipients. This is an illustrative extrapolation, not a benchmark. [`2021-liu-omr`, §§1, 10–11.]

PerfOMR’s speedup depends on construction and parameters; its evaluation reports a parameter correction affecting the stated security level. [`2024-liu-perfomr`, §§7.1–7.2, footnote 18.] SimplePIR’s roughly 10 GB/s/core result uses a particular in-memory workload and hardware, with substantial hints and query communication. It is not small-record delivery throughput. [`2022-henzinger-simplepir`, §1, §8.]

Before claiming global-observer resistance, test an explicit mix profile including cover schedules, provider trust, malicious clients, low-load behavior, intersection attacks and retransmissions.

**Change-course conditions:** reject full-stream wallets if battery/data measurements fail; reject the assumed economics if reserved egress revenue does not cover measured service costs; change dissemination if amplification or adversarial scoring fails; postpone chain-event dependencies if activation is unconfirmed; withhold stronger anonymity claims if the combined protocol lacks a supported security argument.

| Decision | Choice | Rejected alternatives | Evidence | Confidence | What would change my mind |
|---|---|---|---|---|---|---|
| D1 | Fixed 2 KiB sealed records; session protocol inside reviewed wrapper | Bitmessage compatibility; bulk ledger logs | `2012-warren-bitmessage-whitepaper` §3; `2023-barnes-rfc9420` §16.4; `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:43` | Medium | Wrapper analysis or measured control-message sizes require another format |
| D2 | Content and subscriber-selection privacy; explicit metadata leakage | Unqualified anonymity; global-observer promise | `2018-fanti-dandelionpp` §3.1; `2017-piotrowska-loopix` §2.2 | High | A reviewed stronger profile supports additional properties |
| D3 | Secret invitations, complete-stream retrieval, local dispatch, follow-up contract transaction | Public topic filters; autonomous contract subscriptions | `2012-warren-bitmessage-whitepaper` §3; `midnight-indexer/indexer-api/graphql/schema-v4.graphql:552` | Medium | Private discovery or retrieval is validated for the workload |
| D4 | Reserved service capacity and permits; DUST pays chain execution | DUST transfers to operators; flat PoW; per-event chain payment | `midnight-ledger@dc87cc8f/base-crypto/src/cost_model.rs:408`; `2004-laurie-proofofwork` §§3–5 | Medium | Anonymous admission and sustainable settlement are demonstrated |
| D5 | Measured 10/s baseline, 100/s burst, 10,000 consumers | Imported throughput claims; finality constants as SLOs | `2017-piotrowska-loopix` §5; `2021-liu-omr` §10; `midnight-node/runtime/src/lib.rs:292` | Low | Proposed-system measurements establish attainable limits |
| D6 | 48-hour relay retention; separately paid archive; bounded ledger commitments | Ledger payload storage; TTL as deletion guarantee | `midnight-ledger@54a4e013/onchain-vm/src/vm.rs:595`; stated arithmetic assumptions | Medium | Recovery requirements or measured storage costs demand another window |
| D7 | Paid independent relays and gateways; progressive admission decentralization | Mandatory validator service; assumed token incentives | `midnight-node/node/src/service.rs:614`; operational assumptions | Low | Operator participation and service-payment evidence support another model |
| D8 | Independent overlay with optional Midnight anchoring | Node-network extension at launch; ledger/indexer-only bus | `midnight-node/node/src/service.rs:644`; `minokawa-compact/doc/release-notes/toolchain-0.33.0.md:22` | High | A deployed native extension demonstrates isolation and sufficient capacity |
| D9 | Configuration-specific defenses and declared residual risk | GossipSub, FMD or MLS as universal security guarantees | `2022-kumar-gossipsub-formal` §§3–5; `2021-seres-fmdfalsepositives` §§3–4; `2023-barnes-rfc9420` §16.9 | High | Combined-protocol analysis supports stronger guarantees |
| D10 | Immutable evidence, bounded models, measured gates and separate upgrade trials | Feature-led release; unchecked benchmark extrapolation | `midnight-node/Cargo.lock:7894`; `2024-liu-perfomr` §7.1; `2022-henzinger-simplepir` §8 | High | Reproducible evidence satisfies or overturns a stated gate |